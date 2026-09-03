#!/usr/bin/env python3
"""
Lisa's PPT - Visual Review Renderer

Renders project SVGs at their root viewBox dimensions to PNGs for an agent's
own visual self-check: <use data-icon> references inlined from the project icon
set, relative <image href> resolved against the project, and the browser's full
font fallback chain including CJK. The pure renderer for the visual-review
stage — does not edit SVGs, does not interpret the rubric.

Standalone: the SVGs are read straight off disk. Nothing has to be started
first — no server, no port, no service lock to discover. (The renderer still
takes its own <project>/.preview/.render.lock so concurrent runs serialize.)

Backend: Playwright (Chromium). The cairosvg backend was evaluated and rejected
because cairo's text API has no font-fallback chain — CJK characters render as
tofu boxes for any deck whose font-family list relies on system fallback.

Usage:
    python3 scripts/visual_review.py <project_path>
    python3 scripts/visual_review.py <project_path> --pages 02 03

Exit codes (contract in scripts/docs/svg-pipeline.md#visual_reviewpy):
    0 — all requested pages rendered
    2 — project path or svg_output/ unusable for this run
    3 — rendering backend (playwright + chromium) missing or unable to launch
    4 — one or more page-level render failures (details in stderr)

Output: JSON summary printed to stdout, PNGs written to <project>/.preview/.
"""

from __future__ import annotations

import argparse
import html
import io
import json
import math
import os
import re
import sys
import time
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from xml.etree import ElementTree as ET

from console_encoding import configure_utf8_stdio
from resource_paths import icon_dir_for_project
from slide_roster import discover_slide_svgs
from svg_finalize.embed_icons import (
    extract_paths_from_icon,
    generate_icon_group,
    parse_use_element,
    resolve_icon_path,
)
from svg_to_pptx.canvas_contract import parse_project_svg_root
from svg_to_pptx.geometry_properties import materialize_inline_geometry_properties

configure_utf8_stdio()

_SVG_NS = 'http://www.w3.org/2000/svg'
_XLINK_NS = 'http://www.w3.org/1999/xlink'
_XLINK_HREF = f'{{{_XLINK_NS}}}href'
_USE_ICON_PATTERN = re.compile(r'<use\s+[^>]*data-icon="[^"]*"[^>]*/>')

# Serialize the SVG namespace as the default one. Without this ElementTree
# emits ns0:svg / ns0:use, which the HTML parser does not treat as SVG at all
# and which the icon-inlining regex below would silently skip.
ET.register_namespace('', _SVG_NS)
ET.register_namespace('xlink', _XLINK_NS)


# Histogram threshold: PNG counts as "all background" if a single quantized
# color bucket holds >= ALL_BG_THRESHOLD of pixels. Guards against blank
# renders without false-firing on legitimate sparse dark layouts.
ALL_BG_THRESHOLD = 0.99


def _safe_print(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


@contextmanager
def file_lock(lock_path: Path, timeout: float = 30.0):
    """POSIX advisory lock via fcntl. Falls back to lockless on Windows."""
    try:
        import fcntl
    except ImportError:
        yield
        return

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    fp = open(lock_path, 'w')
    deadline = time.monotonic() + timeout
    while True:
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except BlockingIOError:
            if time.monotonic() >= deadline:
                fp.close()
                raise TimeoutError(f"render lock contended for {timeout}s at {lock_path}")
            time.sleep(0.1)
    try:
        fp.write(str(os.getpid()))
        fp.flush()
        yield
    finally:
        fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
        fp.close()
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def is_all_background(png_bytes: bytes) -> bool:
    """Histogram check: quantize each channel to 4 bits, count dominant bucket.
    Returns True only when the PNG is essentially monochrome (blank render)."""
    try:
        from PIL import Image
    except ImportError:
        # PIL not installed — skip this check, the rubric subagent will
        # re-validate visually.
        return False

    img = Image.open(io.BytesIO(png_bytes)).convert('RGB')
    pixels = img.getdata()
    total = img.width * img.height
    if total == 0:
        return True
    counts: dict[tuple[int, int, int], int] = {}
    for r, g, b in pixels:
        key = (r >> 4, g >> 4, b >> 4)
        counts[key] = counts.get(key, 0) + 1
    dominant = max(counts.values())
    return dominant / total >= ALL_BG_THRESHOLD


def _xml_attr(value: object) -> str:
    """Escape a value for safe insertion into generated render-only markup."""
    return html.escape(str(value), quote=True)


def normalize_render_hrefs(root: ET.Element) -> None:
    """Normalize legacy XLink references in the render-only SVG copy.

    ElementTree otherwise serializes an unregistered/legacy namespace with an
    arbitrary prefix. The HTML SVG parser only gives special namespace handling
    to ``xlink:href``; an arbitrary prefix can therefore render as an inert
    attribute after ``innerHTML`` insertion. SVG 2 ``href`` works for both
    images and local ``use`` references and avoids that parser boundary.
    """
    for elem in root.iter():
        legacy_href = elem.get(_XLINK_HREF)
        if legacy_href is None:
            continue
        if elem.get('href') is None:
            elem.set('href', legacy_href)
        elem.attrib.pop(_XLINK_HREF, None)


def inline_icons(
    content: str,
    icons_dir: Path,
    target_dir: Path,
) -> tuple[str, list[dict]]:
    """Replace <use data-icon="..."/> with a rendered <g> for the browser.

    Icons resolve only from the prepared project icon directory. Returns
    ``(rewritten_content, warnings)``; each warning is
    ``{"icon": <name>, "reason": <str>}`` so a missing icon shows up in the
    render record instead of silently disappearing from the PNG.
    """
    warnings: list[dict] = []
    matches = list(_USE_ICON_PATTERN.finditer(content))
    if not matches:
        return content, warnings
    new_content = content
    for match in reversed(matches):
        use_str = match.group(0)
        icon_name: str = ''
        try:
            attrs = parse_use_element(use_str)
            icon_name = str(attrs.get('icon') or '')
            if not icon_name:
                warnings.append({'icon': '', 'reason': 'missing data-icon attribute'})
                continue
            icon_path, _ = resolve_icon_path(icon_name, icons_dir)
            color = str(attrs.get('fill', '#000000'))
            elements, style, base_size = extract_paths_from_icon(
                icon_path,
                color,
                target_dir=target_dir,
            )
        except Exception as exc:  # noqa: BLE001 — one bad icon must not fail the page
            warnings.append({'icon': icon_name, 'reason': f'{type(exc).__name__}: {exc}'})
            continue
        if not elements:
            warnings.append({'icon': icon_name, 'reason': 'no renderable paths in icon'})
            continue
        replacement = generate_icon_group(attrs, elements, style, base_size)
        id_match = re.search(r'\bid="([^"]+)"', use_str)
        if id_match:
            replacement = replacement.replace(
                '<g ',
                f'<g id="{_xml_attr(id_match.group(1))}" '
                f'data-icon="{_xml_attr(icon_name)}" ',
                1,
            )
        new_content = new_content[:match.start()] + replacement + new_content[match.end():]
    return new_content, warnings


def load_slide_content(svg_file: Path, icons_dir: Path) -> tuple[str, list[dict]]:
    """Return one slide's render-ready SVG markup, read straight off disk."""
    root = ET.parse(str(svg_file)).getroot()
    materialize_inline_geometry_properties(root)
    normalize_render_hrefs(root)
    content = ET.tostring(root, encoding='unicode', xml_declaration=False)
    return inline_icons(content, icons_dir, svg_file.parent)


def _json_number(value: Decimal) -> int | float:
    """Keep integral canvas values compact while preserving fractional input."""
    if value == value.to_integral_value():
        return int(value)
    return float(value)


def parse_slide_canvas(svg_content: str, page_name: str) -> dict:
    """Read the authoritative canvas from one inlined SVG root viewBox."""
    try:
        root = ET.fromstring(svg_content)
    except ET.ParseError as exc:
        raise ValueError(f'{page_name}: unable to parse root SVG: {exc}') from exc

    viewbox = parse_project_svg_root(root, context=page_name)
    width = _json_number(viewbox.width)
    height = _json_number(viewbox.height)
    return {
        'view_box': [_json_number(value) for value in viewbox.values],
        'width': width,
        'height': height,
        'png_width': math.ceil(float(viewbox.width)),
        'png_height': math.ceil(float(viewbox.height)),
    }


def render_pages(
    svg_dir: Path,
    icons_dir: Path,
    pages: list[str],
    preview_dir: Path,
) -> list[dict]:
    """Render all requested pages in a single browser session.

    Each render loads the slide from disk (inlining <use data-icon> against the
    project icon set), then injects it into a throwaway HTML document that
    lives *inside* ``svg_dir``. Anchoring the document there is what makes the
    SVG's own relative <image href="../images/..."> resolve to the same file
    the exporter will embed.
    """
    from playwright.sync_api import sync_playwright

    preview_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []

    inject_js = """
({svgContent, width, height}) => {
    document.documentElement.innerHTML =
        '<head><style>html,body{margin:0;padding:0;background:#0E1116;overflow:hidden}'
        + ' svg{display:block;width:' + width + 'px;height:' + height + 'px}</style></head>'
        + '<body>' + svgContent + '</body>';
    return { len: svgContent.length };
}
"""

    # The base document must sit in svg_dir so that "../images/..." resolves
    # exactly as it does from the SVG's own location. Dot-prefixed and removed
    # on the way out; discover_slide_svgs() only ever picks up *.svg anyway.
    base_html = svg_dir / f'.visual_review_base.{os.getpid()}.html'
    base_html.write_text(
        '<!doctype html><meta charset="utf-8"><title>visual review</title>',
        encoding='utf-8',
    )
    base_url = base_html.as_uri()

    try:
        with sync_playwright() as p:
          browser = p.chromium.launch()
          try:
              context = browser.new_context()
              for page_name in pages:
                  rec: dict = {'page': page_name, 'ok': False}
                  try:
                      svg_content, warnings = load_slide_content(
                          svg_dir / page_name, icons_dir,
                      )
                      canvas = parse_slide_canvas(svg_content, page_name)
                      rec['canvas'] = canvas
                      if warnings:
                          rec['icon_warnings'] = warnings
                  except Exception as e:  # noqa: BLE001
                      rec['error'] = f'{type(e).__name__}: {e}'
                      records.append(rec)
                      continue

                  stem = page_name[:-4] if page_name.endswith('.svg') else page_name
                  out_path = preview_dir / f'{stem}.png'

                  pg = None
                  try:
                      pg = context.new_page()
                      pg.set_viewport_size({
                          'width': canvas['png_width'],
                          'height': canvas['png_height'],
                      })
                      pg.goto(base_url, wait_until='domcontentloaded')
                      pg.evaluate(inject_js, {
                          'svgContent': svg_content,
                          'width': canvas['width'],
                          'height': canvas['height'],
                      })
                      # Wait one frame so font/text shaping settles before capture.
                      pg.wait_for_timeout(100)
                      png_bytes = pg.screenshot(type='png', full_page=False)

                      out_path.write_bytes(png_bytes)
                      rec['path'] = str(out_path)
                      rec['bytes'] = len(png_bytes)
                      rec['all_background'] = is_all_background(png_bytes)
                      rec['ok'] = True
                  except Exception as e:  # noqa: BLE001 — best-effort per-page
                      rec['error'] = f'{type(e).__name__}: {e}'
                  finally:
                      if pg is not None:
                          try:
                              pg.close()
                          except Exception:  # noqa: BLE001 — cleanup is best-effort
                              pass
                  records.append(rec)
          finally:
              browser.close()
    finally:
        try:
            base_html.unlink()
        except OSError:
            pass

    return records


def svg_dir_for_project(project_path: Path) -> Path:
    """Return the project's authored-SVG directory, or raise if it is absent."""
    svg_dir = project_path / 'svg_output'
    if not svg_dir.is_dir():
        raise FileNotFoundError(f'no svg_output/ in {project_path}')
    return svg_dir


def discover_pages(project_path: Path, requested: list[str] | None) -> list[str]:
    svg_dir = svg_dir_for_project(project_path)
    all_svgs = [path.name for path in discover_slide_svgs(svg_dir)]
    if not requested:
        return all_svgs
    selected: list[str] = []
    for token in requested:
        match = next((n for n in all_svgs if n.startswith(token) or n == token), None)
        if match is None:
            raise ValueError(f'no SVG matches token {token!r} in {svg_dir}')
        selected.append(match)
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Render project SVGs to PNGs for visual review.',
    )
    parser.add_argument('project_path', help='Path to project directory (contains svg_output/)')
    parser.add_argument(
        '--pages', nargs='+', default=None,
        help='Page tokens to render (default: all SVGs in svg_output/). '
             "Accepts '02', '02_three_steps', or '02_three_steps.svg'.",
    )
    parser.add_argument(
        '--lock-timeout', type=float, default=30.0,
        help='Seconds to wait for render lock (default: 30)',
    )
    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()
    if not project_path.is_dir():
        _safe_print(f'project path not found: {project_path}')
        return 2

    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        _safe_print(
            'playwright not installed. Install with:\n'
            '    pip install playwright\n'
            '    python3 -m playwright install chromium\n'
            '(see skills/lisa-ppt/requirements.txt)'
        )
        return 3

    try:
        svg_dir = svg_dir_for_project(project_path)
        pages = discover_pages(project_path, args.pages)
    except (FileNotFoundError, ValueError) as e:
        _safe_print(str(e))
        return 2

    icons_dir = icon_dir_for_project(project_path)

    preview_dir = project_path / '.preview'
    lock_path = preview_dir / '.render.lock'

    with file_lock(lock_path, timeout=args.lock_timeout):
        try:
            records = render_pages(svg_dir, icons_dir, pages, preview_dir)
        except Exception as e:  # noqa: BLE001 — browser launch failure
            _safe_print(f'browser session failed: {type(e).__name__}: {e}')
            _safe_print(
                'try:  python3 -m playwright install chromium'
            )
            return 3

    for rec in records:
        if not rec['ok']:
            _safe_print(f"[FAIL] {rec['page']}: {rec.get('error')}")
        elif rec.get('all_background'):
            _safe_print(f"[WARN] {rec['page']}: PNG rendered but is all-background")

    summary = {
        'project': str(project_path),
        'rendered': sum(1 for r in records if r['ok']),
        'failed': sum(1 for r in records if not r['ok']),
        'all_background': sum(1 for r in records if r.get('all_background')),
        'pages': records,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if summary['failed']:
        return 4
    return 0


if __name__ == '__main__':
    sys.exit(main())
