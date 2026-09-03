#!/usr/bin/env python3
"""
Lisa's PPT - Lisa HTML Deck Intake

Read a finished Hi Ted, Meet Lisa slide deck — an HTML file made from the
`monomind-deck`, `evidence-deck`, or `paper-brief` template — into a PPT
Master project: one Markdown source per language under `sources/` (one `##`
per slide, every canvas component typed and preserved as a Markdown table or
list) plus a pre-filled `design_spec.md` carrying the deck's own `:root`
colour tokens (with `fact` provenance), font stacks, languages, and page
count, so the Strategist starts from the deck's look instead of a blank spec.

Nothing the markup does not carry is invented: a value the deck does not state
stays a `[fill]` placeholder, and every omission and every unclassified
element is listed in the summary the command prints.

Usage:
    python3 scripts/lisa_html_intake.py <deck.html> --project <path> [--format <canvas>] [--force]
    python3 scripts/lisa_html_intake.py <deck.html> --dry-run [--json]

Examples:
    python3 scripts/lisa_html_intake.py ~/decks/evidence-deck.html --project projects/evidence
    python3 scripts/lisa_html_intake.py ~/decks/paper-brief.html --dry-run
    python3 scripts/lisa_html_intake.py ~/decks/monomind-deck.html --dry-run --json

Dependencies:
    None (only uses standard library)
"""

from __future__ import annotations

import argparse
import base64
import contextlib
import json
import re
import shutil
import struct
import sys
from dataclasses import dataclass, field
from datetime import datetime
from html.parser import HTMLParser
from math import gcd
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
_SOURCE_TO_MD_DIR = _SCRIPTS_DIR / "source_to_md"
if str(_SOURCE_TO_MD_DIR) not in sys.path:
    sys.path.insert(0, str(_SOURCE_TO_MD_DIR))

from console_encoding import configure_utf8_stdio  # noqa: E402

configure_utf8_stdio()

CONVERTER_NAME = "lisa_html_intake.py"
CONVERSION_TYPE = "lisa-html"
INTAKE_SCHEMA = "lisa-ppt.lisa_html_intake.v1"

LText = dict[str, str]

_VOID_TAGS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
})
_SKIP_TAGS = frozenset({"script", "style", "svg", "button", "template", "noscript"})
_SKIP_CLASSES = frozenset({
    "brand-mark", "pagenum", "colophon", "deck-colophon", "copy-btn",
    "frame-head", "title-rule", "nav-dots", "progress-bar", "deck-chrome",
})
_LANG_SPAN_CLASSES = ("en", "ko", "zh", "ja", "zh-TW", "zh-Hant")
_EMPHASIS_CLASSES = frozenset({"hl", "sig", "red", "cyan", "blue", "warn"})
_CODE_CLASSES = frozenset({"mono", "code"})
_LAYOUT_CLASSES = frozenset({
    "grid-2", "grid-3", "grid-4", "grid-img", "dg-flow-h", "dg-workflow-cols",
    "reveal", "slide-content", "wf", "specs", "close-grid", "cover-title",
    "cover-kicker",
})
_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})$")
_ROOT_BLOCK_RE = re.compile(r":root\s*\{([^}]*)\}", re.DOTALL)
_TOKEN_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;]+);")
_CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_LANG_FONT_RULE_RE = re.compile(
    r"body\[data-lang=\"([A-Za-z-]+)\"\]\s*\{([^}]*)\}", re.DOTALL,
)
_CONTENT_MAP_RE = re.compile(r"<!--\s*LISA:CONTENT-MAP(.*?)-->", re.DOTALL)
_FENCE_START = "LISA:CONTENT-START"
_FENCE_END = "LISA:CONTENT-END"
_PART_EYEBROW_RE = re.compile(r"^\s*(Part\s+\d+)\s*[·•\-—–:]\s*(.+?)\s*$", re.IGNORECASE)
_SCREEN_LABEL_RE = re.compile(r"^\s*(\d+)\s+(.*?)\s*$")
_WIDTH_VAR_RE = re.compile(r"--w\s*:\s*([0-9.]+)%")
_DATA_URI_RE = re.compile(r"^data:image/([a-zA-Z0-9.+-]+);base64,(.+)$", re.DOTALL)
_CJK_GAP_RE = re.compile(
    r"(?<=[　-〿぀-ヿ㐀-鿿豈-﫿＀-￯])"
    r" (?=[　-〿぀-ヿ㐀-鿿豈-﫿＀-￯])"
)


# ---------------------------------------------------------------------------
# HTML tree
# ---------------------------------------------------------------------------


class Node:
    """One element in a minimal DOM: tag, attributes, ordered children."""

    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag: str, attrs: dict[str, str], parent: Optional["Node"]) -> None:
        self.tag = tag
        self.attrs = attrs
        self.children: list[Any] = []
        self.parent = parent

    @property
    def classes(self) -> list[str]:
        return (self.attrs.get("class") or "").split()

    def has_class(self, *names: str) -> bool:
        classes = set(self.classes)
        return any(name in classes for name in names)

    def elements(self) -> list["Node"]:
        return [child for child in self.children if isinstance(child, Node)]

    def descendants(self) -> Iterable["Node"]:
        for child in self.children:
            if isinstance(child, Node):
                yield child
                yield from child.descendants()

    def find(self, predicate: Callable[["Node"], bool]) -> Optional["Node"]:
        for node in self.descendants():
            if predicate(node):
                return node
        return None

    def find_all(self, predicate: Callable[["Node"], bool]) -> list["Node"]:
        return [node for node in self.descendants() if predicate(node)]

    def descriptor(self) -> str:
        classes = ".".join(self.classes)
        return f"{self.tag}.{classes}" if classes else self.tag


class Comment:
    """An HTML comment kept in the tree (the Lisa fences are comments)."""

    __slots__ = ("data",)

    def __init__(self, data: str) -> None:
        self.data = data


class _TreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("#document", {}, None)
        self._stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        node = Node(tag, {key: (value or "") for key, value in attrs}, self._stack[-1])
        self._stack[-1].children.append(node)
        if tag not in _VOID_TAGS:
            self._stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        node = Node(tag, {key: (value or "") for key, value in attrs}, self._stack[-1])
        self._stack[-1].children.append(node)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self._stack) - 1, 0, -1):
            if self._stack[index].tag == tag:
                del self._stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if data:
            self._stack[-1].children.append(data)

    def handle_comment(self, data: str) -> None:
        self._stack[-1].children.append(Comment(data))


def parse_html(text: str) -> Node:
    """Parse HTML text into the minimal DOM."""
    builder = _TreeBuilder()
    builder.feed(text)
    builder.close()
    return builder.root


# ---------------------------------------------------------------------------
# Structured outline
# ---------------------------------------------------------------------------


@dataclass
class Component:
    type: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class Slide:
    number: int
    kind: str
    label: LText
    eyebrow: LText = field(default_factory=dict)
    statement: LText = field(default_factory=dict)
    lead: LText = field(default_factory=dict)
    components: list[Component] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)
    part: LText = field(default_factory=dict)
    page_number: Optional[str] = None


@dataclass
class Deck:
    source: Path
    family: str
    title: LText
    primary_language: str
    languages: list[str]
    tokens: dict[str, str]
    language_fonts: dict[str, dict[str, str]]
    content_map: str
    fenced: bool
    dark: bool = True
    slides: list[Slide] = field(default_factory=list)
    images: list[dict[str, Any]] = field(default_factory=list)
    omitted: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)


class IntakeError(RuntimeError):
    """A deck this importer refuses to read."""


# ---------------------------------------------------------------------------
# Family knowledge
# ---------------------------------------------------------------------------

FAMILY_INFO: dict[str, dict[str, Any]] = {
    "monomind-deck": {
        "name": "MonoMind deck",
        "type": "present",
        "tagline": "Horizontal presentation deck, dark ink and accent halos.",
        "reading_mode": "presentation",
    },
    "evidence-deck": {
        "name": "Evidence deck",
        "type": "present",
        "tagline": "Dark full-bleed slides that argue from numbers — tables, stat rows, verdict bars.",
        "reading_mode": "presentation",
    },
    "paper-brief": {
        "name": "Paper brief",
        "type": "read",
        "tagline": "Light paper slides paced in chapters — mega numbers, bar charts, decision boxes.",
        "reading_mode": "text",
    },
}

# Role -> (candidate tokens in preference order, purpose text)
COLOR_ROLES: dict[str, list[tuple[str, tuple[str, ...], str]]] = {
    "monomind-deck": [
        ("Background", ("--fg",), "the deep-ink ground every `.dark` slide paints"),
        ("Secondary background", ("--surface",), "frosted card fill"),
        ("Primary", ("--accent",), "the MonoMind blue — halos, accent edges, links"),
        ("Accent", ("--accent",), "emphasis and the accent-edged panel"),
        ("Secondary accent", ("--meta",), "metadata and kicker colour"),
        ("Body text", ("--accent-on",), "text on the dark ground"),
        ("Secondary text", ("--muted-inv",), "captions and secondary lines on the dark ground"),
        ("Divider", ("--glass-hair", "--border"), "hairlines and card borders on the dark ground"),
        ("Status success", ("--success",), "status colour"),
        ("Status warning", ("--warn",), "status colour"),
        ("Status danger", ("--danger",), "status colour"),
    ],
    "monomind-deck-light": [
        ("Background", ("--bg",), "the page ground"),
        ("Secondary background", ("--surface",), "frosted card fill"),
        ("Primary", ("--accent",), "the MonoMind blue — halos, accent edges, links"),
        ("Accent", ("--accent",), "emphasis and the accent-edged panel"),
        ("Secondary accent", ("--meta",), "metadata and kicker colour"),
        ("Body text", ("--fg",), "body text"),
        ("Secondary text", ("--muted",), "captions and secondary lines"),
        ("Divider", ("--border", "--border-soft"), "hairlines and card borders"),
        ("Status success", ("--success",), "status colour"),
        ("Status warning", ("--warn",), "status colour"),
        ("Status danger", ("--danger",), "status colour"),
    ],
    "evidence-deck": [
        ("Background", ("--bg",), "the near-black ground"),
        ("Secondary background", ("--panel",), "cards and table panels"),
        ("Primary", ("--sig",), "the signal orange — section cards, flagged rows, verdict bars"),
        ("Accent", ("--sig",), "the alarming part of a sentence"),
        ("Secondary accent", ("--cyan",), "the part that already works"),
        ("Body text", ("--fg",), "body text and the load-bearing phrase"),
        ("Secondary text", ("--fg-soft",), "eyebrows, notes, mega-number notes"),
        ("Divider", ("--rule",), "table rules and hairlines"),
        ("Tertiary text", ("--fg-faint",), "page numbers and the faintest labels"),
        ("Panel 2", ("--panel-2",), "second panel tone"),
        ("Warning", ("--warn",), "amber — paths, identifiers, the warn stat"),
        ("On-signal ink", ("--on-sig",), "ink that sits on the signal colour"),
    ],
    "paper-brief": [
        ("Background", ("--paper",), "white paper"),
        ("Secondary background", ("--decision-bg",), "decision-box ground"),
        ("Primary", ("--red",), "the red that argues — flags, accent bars, mega numbers"),
        ("Accent", ("--red",), "the part that is a problem"),
        ("Secondary accent", ("--blue",), "the part that already works"),
        ("Body text", ("--ink",), "ink"),
        ("Secondary text", ("--ink-soft",), "eyebrows and notes"),
        ("Divider", ("--rule",), "table rules"),
        ("Tertiary text", ("--ink-faint",), "footnotes and faint labels"),
        ("Amber", ("--amber",), "the warn bar"),
        ("Bar track", ("--track",), "bar-chart channel"),
        ("Chapter ground", ("--invert-bg",), "inverted chapter pages"),
        ("Chapter ink", ("--invert-ink",), "text on chapter pages"),
    ],
}


def _lang_tag(raw: str, html_lang: str) -> str:
    """Map a Lisa language span class to a canonical BCP-47 tag."""
    if raw == "zh":
        lowered = html_lang.lower()
        if "hant" in lowered or lowered.endswith("-tw"):
            return "zh-TW"
        return "zh"
    if raw == "zh-Hant":
        return "zh-TW"
    return raw


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------


class TextExtractor:
    """Pull language-keyed Markdown text out of a subtree."""

    def __init__(self, languages: list[str], html_lang: str) -> None:
        self.languages = languages
        self.html_lang = html_lang

    def _lang_of(self, node: Node) -> Optional[str]:
        if node.tag != "span":
            return None
        for cls in node.classes:
            if cls in _LANG_SPAN_CLASSES:
                return _lang_tag(cls, self.html_lang)
        return None

    def text(self, node: Optional[Node], *, br: str = " ", preserve_newlines: bool = False) -> LText:
        buffers: dict[str, list[str]] = {lang: [] for lang in self.languages}
        if node is not None:
            self._walk(node, buffers, None, br, preserve_newlines)
        result: LText = {}
        for lang, parts in buffers.items():
            joined = "".join(parts)
            if preserve_newlines:
                cleaned = "\n".join(
                    re.sub(r"[ \t\u00a0]+", " ", line).strip() for line in joined.split("\n")
                ).strip("\n")
            else:
                cleaned = re.sub(r"\s+", " ", joined.replace("\u00a0", " ")).strip()
            cleaned = re.sub(r"\*\* +\*\*", " ", cleaned)
            # A <br> between two CJK characters carried no space in the deck.
            cleaned = _CJK_GAP_RE.sub("", cleaned)
            if cleaned:
                result[lang] = cleaned
        return result

    def _walk(
        self,
        node: Node,
        buffers: dict[str, list[str]],
        lang: Optional[str],
        br: str,
        preserve_newlines: bool,
    ) -> None:
        for child in node.children:
            if isinstance(child, Comment):
                continue
            if isinstance(child, str):
                targets = [lang] if lang else list(buffers)
                for target in targets:
                    if target in buffers:
                        buffers[target].append(child)
                continue
            if child.tag in _SKIP_TAGS or child.has_class(*_SKIP_CLASSES):
                continue
            if child.tag == "br":
                targets = [lang] if lang else list(buffers)
                for target in targets:
                    if target in buffers:
                        buffers[target].append("\n" if preserve_newlines else br)
                continue
            child_lang = self._lang_of(child) or lang
            if child_lang and child_lang not in buffers:
                # A language the deck never declared: keep it under the
                # primary buffer so the text is not silently lost.
                child_lang = self.languages[0]
            marker = self._marker(child)
            if marker:
                inner: dict[str, list[str]] = {key: [] for key in buffers}
                self._walk(child, inner, child_lang, br, preserve_newlines)
                for key, parts in inner.items():
                    text = "".join(parts)
                    stripped = text.strip()
                    if stripped:
                        lead_ws = text[: len(text) - len(text.lstrip())]
                        tail_ws = text[len(text.rstrip()):]
                        buffers[key].append(f"{lead_ws}{marker}{stripped}{marker}{tail_ws}")
                continue
            self._walk(child, buffers, child_lang, br, preserve_newlines)

    @staticmethod
    def _marker(node: Node) -> str:
        if node.tag in {"b", "strong"} or node.has_class(*_EMPHASIS_CLASSES):
            return "**"
        if node.tag == "code" or (node.tag == "span" and node.has_class(*_CODE_CLASSES)):
            return "`"
        if node.tag in {"i", "em"} and not node.parent.has_class("st"):
            return "*"
        return ""


def _merge(*texts: LText) -> LText:
    """Join several LText values with an em dash, language by language."""
    result: LText = {}
    for text in texts:
        for lang, value in text.items():
            if not value:
                continue
            result[lang] = f"{result[lang]} — {value}" if result.get(lang) else value
    return result


def _pick(text: LText, lang: str) -> str:
    return text.get(lang, "")


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------


def parse_tokens(styles: Iterable[str]) -> dict[str, str]:
    """Collect `--token: value` pairs from every `:root {}` block, later wins."""
    tokens: dict[str, str] = {}
    for style in styles:
        cleaned = _CSS_COMMENT_RE.sub("", style)
        for block in _ROOT_BLOCK_RE.findall(cleaned):
            # The last declaration in a block may omit its semicolon.
            for name, value in _TOKEN_RE.findall(block + ";"):
                tokens[name] = value.strip()
    return tokens


def parse_language_fonts(styles: Iterable[str]) -> dict[str, dict[str, str]]:
    """Collect per-language font overrides such as body[data-lang="ko"]{--font-body:...}."""
    result: dict[str, dict[str, str]] = {}
    for style in styles:
        cleaned = _CSS_COMMENT_RE.sub("", style)
        for lang, block in _LANG_FONT_RULE_RE.findall(cleaned):
            fonts = {
                name: value.strip()
                for name, value in _TOKEN_RE.findall(block + ";")
                if name.startswith("--font-")
            }
            if fonts:
                result.setdefault(lang, {}).update(fonts)
    return result


def resolve_token(tokens: dict[str, str], name: str, depth: int = 0) -> Optional[str]:
    """Return a token's value with one level of var() indirection resolved."""
    value = tokens.get(name)
    if value is None or depth > 3:
        return value
    match = re.fullmatch(r"var\((--[A-Za-z0-9_-]+)\)", value.strip())
    if match:
        return resolve_token(tokens, match.group(1), depth + 1)
    return value


def normalize_hex(value: str) -> Optional[str]:
    """Return an uppercase #RRGGBB for a flat hex value, else None."""
    value = value.strip()
    if not _HEX_RE.match(value):
        return None
    if len(value) == 4:
        value = "#" + "".join(ch * 2 for ch in value[1:])
    return value.upper()


def split_font_stack(value: str) -> list[str]:
    """Split a CSS font-family value into bare family names."""
    families = []
    for part in value.split(","):
        family = part.strip().strip("'\"").strip()
        if family:
            families.append(family)
    return families


def detect_family(document: Node, tokens: dict[str, str], content_map: str) -> tuple[str, list[str]]:
    """Return (family id, evidence lines) or raise IntakeError."""
    sections = document.find_all(lambda n: n.tag == "section" and n.has_class("slide"))
    pages = document.find_all(lambda n: n.tag == "section" and n.has_class("page"))
    scores: dict[str, list[str]] = {family: [] for family in FAMILY_INFO}

    if any("data-screen-label" in s.attrs for s in sections):
        scores["monomind-deck"].append("sections carry data-screen-label")
    if document.find(lambda n: n.has_class("dg-canvas")):
        scores["monomind-deck"].append("div.dg-canvas present")
    if all(name in tokens for name in ("--accent", "--fg", "--bg")):
        scores["monomind-deck"].append(":root carries --accent/--fg/--bg")
    if "data-screen-label" in content_map:
        scores["monomind-deck"].append("LISA:CONTENT-MAP names data-screen-label")

    if any("data-label-ko" in s.attrs for s in sections):
        scores["evidence-deck"].append("sections carry data-label-en/ko")
    if all(name in tokens for name in ("--sig", "--cyan", "--panel")):
        scores["evidence-deck"].append(":root carries --sig/--cyan/--panel")
    if "data-label-en/ko" in content_map:
        scores["evidence-deck"].append("LISA:CONTENT-MAP names data-label-en/ko")

    if any("data-label-zh" in s.attrs for s in sections):
        scores["paper-brief"].append("sections carry data-label-zh/en")
    if all(name in tokens for name in ("--paper", "--ink", "--red")):
        scores["paper-brief"].append(":root carries --paper/--ink/--red")
    if "data-label-zh/en" in content_map:
        scores["paper-brief"].append("LISA:CONTENT-MAP names data-label-zh/en")

    best = max(scores, key=lambda key: len(scores[key]))
    if len(scores[best]) >= 2 and sections:
        return best, scores[best]
    if pages and not sections:
        raise IntakeError(
            "this is a Lisa document-kind file (section.page, hash-routed pages), not a slides "
            "deck; only the monomind-deck, evidence-deck, and paper-brief families are importable"
        )
    if not sections:
        raise IntakeError("no section.slide elements found; not a Lisa slide deck")
    raise IntakeError(
        "could not identify the Lisa template family from the LISA:CONTENT-MAP header, the "
        ":root tokens, and the slide attributes; supported families: "
        + ", ".join(FAMILY_INFO)
    )


def _fence_positions(node: Node, region: str) -> Optional[tuple[Node, int, int]]:
    """Locate the LISA:CONTENT-START/END pair for a region: (parent, start, end)."""
    start_index = end_index = None
    for index, child in enumerate(node.children):
        if isinstance(child, Comment):
            words = child.data.split()
            if words[:2] == [_FENCE_START, region]:
                start_index = index
            elif words[:2] == [_FENCE_END, region]:
                end_index = index
    if start_index is not None and end_index is not None and end_index > start_index:
        return node, start_index, end_index
    for child in node.elements():
        found = _fence_positions(child, region)
        if found:
            return found
    return None


def slide_sections(document: Node) -> tuple[list[Node], bool]:
    """Return the slide sections, preferring the LISA:CONTENT fenced region."""
    body = document.find(lambda n: n.tag == "body") or document
    fence = _fence_positions(body, "slides")
    if fence:
        parent, start_index, end_index = fence
        sections = [
            node for node in parent.children[start_index + 1:end_index]
            if isinstance(node, Node) and node.tag == "section" and node.has_class("slide")
        ]
        if sections:
            return sections, True
    return body.find_all(lambda n: n.tag == "section" and n.has_class("slide")), False


# ---------------------------------------------------------------------------
# Component parsing
# ---------------------------------------------------------------------------


class SlideParser:
    """Walk one slide's markup into typed components."""

    def __init__(self, deck: Deck, extractor: TextExtractor) -> None:
        self.deck = deck
        self.extractor = extractor
        self.image_counter = 0

    # -- helpers ----------------------------------------------------------

    def text(self, node: Optional[Node], **kwargs: Any) -> LText:
        return self.extractor.text(node, **kwargs)

    def child(self, node: Node, *classes: str, tag: Optional[str] = None) -> Optional[Node]:
        for elem in node.elements():
            if tag and elem.tag != tag:
                continue
            if not classes or elem.has_class(*classes):
                return elem
        return None

    def first(self, node: Node, *classes: str, tag: Optional[str] = None) -> Optional[Node]:
        return node.find(lambda n: (tag is None or n.tag == tag) and (not classes or n.has_class(*classes)))

    # -- slides -----------------------------------------------------------

    def parse_slide(self, section: Node, number: int) -> Slide:
        family = self.deck.family
        if family == "monomind-deck":
            return self._parse_monomind(section, number)
        return self._parse_content_slide(section, number)

    def _label(self, section: Node, number: int) -> LText:
        label: LText = {}
        if "data-screen-label" in section.attrs:
            match = _SCREEN_LABEL_RE.match(section.attrs["data-screen-label"])
            text = match.group(2) if match else section.attrs["data-screen-label"]
            label[self.deck.primary_language] = text.strip()
            return label
        for key, value in section.attrs.items():
            if key.startswith("data-label-"):
                lang = _lang_tag(key[len("data-label-"):], self.extractor.html_lang)
                if lang in self.deck.languages:
                    label[lang] = value.strip()
        if not label:
            label[self.deck.primary_language] = f"Slide {number:02d}"
        return label

    def _parse_monomind(self, section: Node, number: int) -> Slide:
        classes = set(section.classes)
        if "cover-hero" in classes or ("hero" in classes and number == 1):
            kind = "cover"
        elif "hero" in classes:
            kind = "closing"
        else:
            kind = "content"
        slide = Slide(number=number, kind=kind, label=self._label(section, number))
        canvas = self.first(section, "dg-canvas")

        def visit(node: Node) -> None:
            for elem in node.elements():
                if elem is canvas or elem.tag in _SKIP_TAGS or elem.has_class(*_SKIP_CLASSES):
                    continue
                if elem.has_class("eyebrow") and not slide.eyebrow:
                    slide.eyebrow = self.text(elem)
                elif elem.tag in {"h1", "h2"} and not slide.statement:
                    slide.statement = self.text(elem)
                elif elem.has_class("lead") and not slide.lead:
                    slide.lead = self.text(elem)
                elif elem.has_class("cover-meta"):
                    items = [self.text(span) for span in elem.elements() if span.tag == "span"]
                    slide.components.append(Component("meta", {"items": [i for i in items if i]}))
                elif elem.has_class("close-links"):
                    links = [
                        {"text": self.text(a), "href": a.attrs.get("href", "")}
                        for a in elem.elements() if a.tag == "a"
                    ]
                    slide.components.append(Component("links", {"items": links}))
                elif elem.has_class("cover-title", "cover-kicker", "close-grid") or elem.tag == "div":
                    visit(elem)
                else:
                    self._unknown(slide, elem)

        visit(section)
        if canvas is not None:
            slide.components.extend(self.parse_components(canvas, slide))
        if _PART_EYEBROW_RE.match(_pick(slide.eyebrow, self.deck.primary_language)):
            # The kicker names the part ("Part 1 · Why"); keep it verbatim.
            slide.part = dict(slide.eyebrow)
        return slide

    def _parse_content_slide(self, section: Node, number: int) -> Slide:
        classes = set(section.classes)
        content = self.child(section, "slide-content")
        chapter = self.first(section, "chapter", "section-card")
        if "title-slide" in classes:
            kind = "cover" if number == 1 else "closing"
        elif chapter is not None:
            kind = "section"
        elif number == 1 and section.find(lambda n: n.tag == "h1") is not None:
            kind = "cover"
        else:
            kind = "content"
        slide = Slide(number=number, kind=kind, label=self._label(section, number))
        pagenum = self.first(section, "pagenum")
        if pagenum is not None:
            slide.page_number = _pick(self.text(pagenum), self.deck.primary_language) or None

        if chapter is not None:
            slide.components.append(self._section_card(chapter))
            head = chapter.find(lambda n: n.tag in {"h1", "h2"})
            if head is not None:
                slide.statement = self.text(head)
            lead = self.first(chapter, "lead")
            if lead is not None:
                slide.lead = self.text(lead)
            if content is not None:
                for elem in content.elements():
                    holds_chapter = elem is chapter or any(node is chapter for node in elem.descendants())
                    if not holds_chapter:
                        self._content_child(slide, elem)
            return slide

        if content is not None:
            for elem in content.elements():
                self._content_child(slide, elem)
        meta = self.first(section, "title-meta")
        if meta is not None:
            items = [self.text(span) for span in meta.elements() if span.tag == "span"]
            items = [item for item in items if item and not self._is_colophon(item)]
            if items:
                slide.components.append(Component("meta", {"items": items}))
        return slide

    @staticmethod
    def _is_colophon(text: LText) -> bool:
        return any("Hi Ted, Meet Lisa" in value or "monomind ai lab" in value.lower() for value in text.values())

    def _content_child(self, slide: Slide, elem: Node) -> None:
        if elem.tag in _SKIP_TAGS or elem.has_class(*_SKIP_CLASSES):
            return
        if elem.has_class("eyebrow") and not slide.eyebrow:
            slide.eyebrow = self.text(elem)
        elif elem.tag in {"h1", "h2"} and not slide.statement:
            slide.statement = self.text(elem)
        elif elem.has_class("lead") and not slide.lead:
            slide.lead = self.text(elem)
        else:
            slide.components.extend(self.parse_components_of([elem], slide))

    def _section_card(self, node: Node) -> Component:
        head = node.find(lambda n: n.tag in {"h1", "h2"})
        lead = self.first(node, "lead")
        if lead is None:
            # The evidence section card carries a bare <p> after its heading.
            lead = next(
                (p for p in node.elements() if p.tag == "p" and not p.has_class("sfor", "cfor")),
                None,
            )
        return Component("section", {
            "for": self.text(self.first(node, "sfor", "cfor")),
            "number": self.text(self.first(node, "sn", "cnum")),
            "statement": self.text(head),
            "lead": self.text(lead),
        })

    # -- components -------------------------------------------------------

    def parse_components(self, container: Node, slide: Slide) -> list[Component]:
        return self.parse_components_of(container.elements(), slide)

    def parse_components_of(self, elems: list[Node], slide: Slide) -> list[Component]:
        components: list[Component] = []
        for elem in elems:
            if elem.tag in _SKIP_TAGS or elem.has_class(*_SKIP_CLASSES):
                continue
            component = self.classify(elem, slide)
            if component is None:
                continue
            for item in component if isinstance(component, list) else [component]:
                previous = components[-1] if components else None
                if (
                    previous is not None
                    and item.type in _MERGEABLE_TYPES
                    and previous.type == item.type
                ):
                    # Sibling rows of one list (leader rows, chips, steps, flags)
                    # are separate elements in the markup but one component.
                    previous.data["items"].extend(item.data["items"])
                else:
                    components.append(item)
        return components

    def classify(self, elem: Node, slide: Slide) -> Component | list[Component] | None:  # noqa: C901
        tag = elem.tag
        classes = set(elem.classes)
        text = self.text

        # Mega number: the wrapper is the reveal, the number and note are inside.
        mega = self.child(elem, "mega")
        if mega is not None:
            return Component("mega", {
                "value": text(mega),
                "note": text(self.child(elem, "mega-note")),
                "tone": self._tone(mega, ("red", "compact")),
            })
        if "mega" in classes:
            return Component("mega", {"value": text(elem), "note": {}, "tone": self._tone(elem, ("red",))})

        if tag == "table":
            return self._table(elem)
        if "statrow" in classes:
            return Component("stat_row", {"items": [
                {"value": text(self.child(s, "n")), "label": text(self.child(s, "l")),
                 "tone": self._tone(s, ("accent", "warn", "cyan", "blue"))}
                for s in elem.elements() if s.has_class("stat")
            ]})
        if classes & {"split", "split3"}:
            return Component("cards", {"items": [
                {"title": text(self.child(c, "ct")), "value": text(self.child(c, "cn")),
                 "detail": text(self.child(c, "cd")), "tone": self._tone(c, ("bad", "good"))}
                for c in elem.elements() if c.has_class("card")
            ]})
        if "verdict" in classes:
            return Component("verdict", {"text": text(elem), "tone": self._tone(elem, ("cyan-v", "dark"))})
        if "decision" in classes:
            return Component("decision", {"heading": text(self.child(elem, "dq")), "action": text(self.child(elem, "da"))})
        if "bars" in classes:
            return Component("bars", {"items": [self._bar(bar) for bar in elem.elements() if bar.has_class("bar")]})
        if "specs" in classes or "spec" in classes:
            specs = [elem] if "spec" in classes else [s for s in elem.elements() if s.has_class("spec")]
            return Component("specs", {"items": [self._spec(spec) for spec in specs]})
        if tag == "ul" and "pts" in classes:
            return Component("points", {"items": [
                {"marker": li.attrs.get("data-n", ""), "text": text(li)}
                for li in elem.elements() if li.tag == "li"
            ]})
        if classes & {"section-card", "chapter"}:
            return self._section_card(elem)
        if "body" in classes and tag == "p":
            return Component("paragraph", {"text": text(elem)})

        # MonoMind deck components
        if "qcard" in classes:
            return Component("card_grid", {"items": [self._qcard(elem)]})
        if any(c.startswith("grid-") for c in classes) and any(e.has_class("qcard") for e in elem.elements()):
            return Component("card_grid", {"items": [self._qcard(q) for q in elem.elements() if q.has_class("qcard")]})
        if "dg-frame" in classes:
            return self._frame(elem, slide)
        if "dg-chip-row" in classes:
            return Component("chips", {"items": [
                {"name": text(self.child(c, "nm")), "desc": text(self.child(c, "ds")), "optional": c.has_class("is-optional")}
                for c in elem.elements() if c.has_class("dg-chip")
            ]})
        if "dg-chip" in classes:
            return Component("chips", {"items": [{"name": text(self.child(elem, "nm")), "desc": text(self.child(elem, "ds")), "optional": elem.has_class("is-optional")}]})
        if "dg-treeview" in classes:
            return Component("tree", {"items": self._tree(elem)})
        if "dg-leader-row" in classes:
            return Component("leader_rows", {"items": [{"name": text(self.child(elem, "dg-leader-name")), "desc": text(self.child(elem, "dg-leader-desc"))}]})
        if "dg-step" in classes:
            return Component("steps", {"items": [self._step(elem)]})
        if "wf-row" in classes:
            return Component("workflow", {"rows": [self._wf_row(elem)]})
        if "wf" in classes:
            return Component("workflow", {"rows": [self._wf_row(r) for r in elem.elements() if r.has_class("wf-row")]})
        if tag == "ul" and "bullets" in classes:
            return Component("bullets", {"items": [text(li) for li in elem.elements() if li.tag == "li"]})
        if tag == "ol":
            return Component("ordered", {"items": [text(li) for li in elem.elements() if li.tag == "li"]})
        if tag == "ul":
            return Component("bullets", {"items": [text(li) for li in elem.elements() if li.tag == "li"]})
        if "code" in classes and tag in {"p", "pre"}:
            return Component("code", {"text": text(elem, preserve_newlines=True), "id": elem.attrs.get("id", "")})
        if tag == "pre":
            return Component("code", {"text": text(elem, preserve_newlines=True), "id": elem.attrs.get("id", "")})
        if "dg-loop" in classes:
            return Component("callout", {"text": text(elem), "role": "loop"})
        if "dg-endbar" in classes:
            return Component("callout", {"text": text(elem), "role": "endbar"})
        if "dg-startbar" in classes:
            return Component("callout", {"text": text(elem), "role": "startbar"})
        if "dg-flag-row" in classes:
            return Component("flags", {"items": [self._flag(f) for f in elem.elements() if f.has_class("dg-flag")]})
        if "dg-flag" in classes:
            return Component("flags", {"items": [self._flag(elem)]})
        if "dg-arrow" in classes:
            return Component("arrow", {"caption": text(elem)})
        if "dg-map" in classes:
            return self._map(elem)
        if "dg-map-summary" in classes or "dg-frame-note" in classes or "plate-cap" in classes:
            return Component("note", {"text": text(elem)})
        if "dg-phase-label" in classes:
            return Component("phase_label", {"text": text(elem)})
        if "plate" in classes or tag == "img":
            img = elem if tag == "img" else elem.find(lambda n: n.tag == "img")
            return self._image(img, slide) if img is not None else None
        if tag == "p" and classes & {"lead", "eyebrow"}:
            return Component("paragraph", {"text": text(elem)})
        if tag in {"h3", "h4", "h5"}:
            return Component("heading", {"text": text(elem)})

        # Transparent layout wrappers (every class is a layout class): recurse.
        if tag == "div" and all(c.startswith("grid-") or c in _LAYOUT_CLASSES for c in classes):
            return self.parse_components(elem, slide)

        if tag == "p":
            return Component("paragraph", {"text": text(elem)})

        return self._unknown(slide, elem)

    def _unknown(self, slide: Slide, elem: Node) -> Optional[Component]:
        content = self.text(elem)
        meaningful = [c for c in elem.classes if c not in _LAYOUT_CLASSES]
        descriptor = f"{elem.tag}.{'.'.join(meaningful)}" if meaningful else elem.tag
        slide.unknown.append(descriptor)
        self.deck.omitted.append(
            f"slide {slide.number:02d}: unclassified markup `{descriptor}` — its text is kept as a "
            "plain paragraph, its component type is not guessed"
        )
        if not content:
            return None
        return Component("unclassified", {"text": content, "markup": descriptor})

    @staticmethod
    def _tone(node: Node, tones: tuple[str, ...]) -> str:
        for tone in tones:
            if node.has_class(tone):
                return tone
        return ""

    def _table(self, table: Node) -> Component:
        headers: list[LText] = []
        rows: list[dict[str, Any]] = []
        for tr in table.find_all(lambda n: n.tag == "tr"):
            cells = [cell for cell in tr.elements() if cell.tag in {"th", "td"}]
            if not cells:
                continue
            if all(cell.tag == "th" for cell in cells) and not headers:
                headers = [self.text(cell) for cell in cells]
                continue
            rows.append({
                "cells": [self.text(cell) for cell in cells],
                "tone": self._tone(tr, ("flag", "good")),
                "kinds": [self._tone(cell, ("k", "m", "num")) for cell in cells],
            })
        return Component("table", {"headers": headers, "rows": rows})

    def _bar(self, bar: Node) -> dict[str, Any]:
        fill = bar.find(lambda n: n.has_class("fill"))
        width = None
        if fill is not None:
            match = _WIDTH_VAR_RE.search(fill.attrs.get("style", ""))
            if match:
                width = float(match.group(1))
        return {
            "label": self.text(self.child(bar, "lab")),
            "value": self.text(self.child(bar, "val")),
            "width_percent": width,
            "tone": self._tone(bar, ("accent", "blue", "warn", "cyan")),
        }

    def _spec(self, spec: Node) -> dict[str, Any]:
        st = self.child(spec, "st")
        sub: LText = {}
        main: LText = {}
        if st is not None:
            # <em> is the block sub-line; strip it out of the main text.
            ems = st.find_all(lambda n: n.tag == "em")
            sub = self.text(ems[0]) if ems else {}
            main = self.extractor.text(_without(st, lambda n: n.tag == "em"))
        return {"number": self.text(self.child(spec, "si")), "text": main, "sub": sub}

    def _qcard(self, card: Node) -> dict[str, Any]:
        return {
            "number": self.text(self.child(card, "qn")),
            "title": self.text(self.child(card, tag="h4")),
            "text": self.text(self.child(card, tag="p")),
        }

    def _step(self, step: Node) -> dict[str, Any]:
        return {
            "number": self.text(self.child(step, "nb-circle") or self.child(step, "n")),
            "title": self.text(step.find(lambda n: n.tag == "h4")),
            "text": self.text(step.find(lambda n: n.tag == "p")),
        }

    def _wf_row(self, row: Node) -> dict[str, Any]:
        phase = self.child(row, "wf-phase")
        sub = phase.find(lambda n: n.tag == "span") if phase is not None else None
        phase_text = self.extractor.text(_without(phase, lambda n: n.tag == "span")) if phase is not None else {}
        track = self.child(row, "wf-track")
        nodes = [self._step(n) for n in (track.elements() if track else []) if n.has_class("wf-node")]
        return {"phase": phase_text, "sub": self.text(sub), "nodes": nodes}

    def _flag(self, flag: Node) -> dict[str, Any]:
        return {"flag": self.text(self.child(flag, "fl")), "desc": self.text(self.child(flag, "fd"))}

    def _tree(self, ul: Node) -> list[dict[str, Any]]:
        items = []
        for li in ul.elements():
            if li.tag != "li":
                continue
            name = self.child(li, "nm")
            desc = self.child(li, "dsc")
            sub = self.child(li, tag="ul")
            items.append({
                "name": self.text(name),
                "desc": self.text(desc),
                "root": li.has_class("root"),
                "children": self._tree(sub) if sub is not None else [],
            })
        return items

    def _map(self, node: Node) -> Component:
        headers = [self.text(h) for h in node.elements() if h.has_class("dg-map-h")]
        rows = []
        left: Optional[LText] = None
        for elem in node.elements():
            if elem.has_class("dg-map-row-l"):
                left = self.text(elem)
            elif elem.has_class("dg-map-row-r"):
                rows.append({"left": left or {}, "right": self.text(elem)})
                left = None
        return Component("map", {"headers": headers, "rows": rows})

    def _frame(self, frame: Node, slide: Slide) -> Component:
        label = self.child(frame, "dg-frame-label")
        head = self.child(frame, "frame-head")
        if label is None and head is not None:
            label = self.child(head, "dg-frame-label")
        children_nodes = [
            e for e in frame.elements()
            if e is not label and e is not head and not e.has_class("dg-frame-note")
            and e.tag not in _INLINE_TAGS
        ]
        note = self.child(frame, "dg-frame-note")
        # Free text sitting directly inside the frame.
        free = self.extractor.text(_only_text(frame))
        return Component("frame", {
            "label": self.text(label),
            "accent": frame.has_class("is-accent"),
            "text": free,
            "children": [c.__dict__ for c in self.parse_components_of(children_nodes, slide)],
            "note": self.text(note),
        })

    def _image(self, img: Node, slide: Slide) -> Optional[Component]:
        src = img.attrs.get("src", "")
        alt = img.attrs.get("alt", "").strip()
        match = _DATA_URI_RE.match(src)
        self.image_counter += 1
        if not match:
            self.deck.omitted.append(
                f"slide {slide.number:02d}: image `{src[:60]}` is an external reference, not embedded; not imported"
            )
            return Component("image", {"alt": alt, "file": "", "src": src[:120]})
        ext = match.group(1).lower().replace("jpeg", "jpg").replace("svg+xml", "svg")
        filename = f"slide{slide.number:02d}-{self.image_counter:02d}.{ext}"
        try:
            payload = base64.b64decode(match.group(2), validate=False)
        except (ValueError, TypeError):
            self.deck.omitted.append(f"slide {slide.number:02d}: embedded image could not be decoded; not imported")
            return Component("image", {"alt": alt, "file": "", "src": "data:"})
        width, height = image_dimensions(payload, ext)
        self.deck.images.append({
            "filename": filename, "alt": alt, "slide": slide.number, "bytes": payload,
            "width": width, "height": height, "format": ext,
        })
        return Component("image", {"alt": alt, "file": filename, "width": width, "height": height})


def _without(node: Optional[Node], predicate: Callable[[Node], bool]) -> Optional[Node]:
    """Shallow-copy a subtree, dropping the elements matching predicate."""
    if node is None:
        return None
    clone = Node(node.tag, node.attrs, node.parent)
    for child in node.children:
        if isinstance(child, Node):
            if predicate(child):
                continue
            clone.children.append(_without(child, predicate))
        else:
            clone.children.append(child)
    return clone


_INLINE_TAGS = frozenset({"b", "strong", "i", "em", "code", "span", "a", "br"})
_MERGEABLE_TYPES = frozenset({"leader_rows", "chips", "steps", "flags", "card_grid", "specs"})


def _only_text(node: Node) -> Node:
    """A copy of node keeping only its direct text and inline (non-block) children."""
    clone = Node(node.tag, node.attrs, node.parent)
    for child in node.children:
        if isinstance(child, str):
            clone.children.append(child)
        elif isinstance(child, Node) and child.tag in _INLINE_TAGS:
            clone.children.append(child)
    return clone


def image_dimensions(payload: bytes, ext: str) -> tuple[Optional[int], Optional[int]]:
    """Read width/height from a PNG or JPEG header without third-party code."""
    try:
        if ext == "png" and payload[:8] == b"\x89PNG\r\n\x1a\n":
            width, height = struct.unpack(">II", payload[16:24])
            return int(width), int(height)
        if ext in {"jpg", "jpeg"} and payload[:2] == b"\xff\xd8":
            index = 2
            while index + 9 < len(payload):
                if payload[index] != 0xFF:
                    index += 1
                    continue
                marker = payload[index + 1]
                if marker in {0xD8, 0x01} or 0xD0 <= marker <= 0xD7:
                    index += 2
                    continue
                length = struct.unpack(">H", payload[index + 2:index + 4])[0]
                if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                    height, width = struct.unpack(">HH", payload[index + 5:index + 9])
                    return int(width), int(height)
                index += 2 + length
    except (struct.error, IndexError):
        pass
    return None, None


# ---------------------------------------------------------------------------
# Deck reading
# ---------------------------------------------------------------------------


def read_deck(path: Path) -> Deck:
    """Parse one Lisa HTML file into a Deck outline."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    document = parse_html(raw)
    styles = [
        "".join(child for child in style.children if isinstance(child, str))
        for style in document.find_all(lambda n: n.tag == "style")
    ]
    tokens = parse_tokens(styles)
    language_fonts = parse_language_fonts(styles)
    map_match = _CONTENT_MAP_RE.search(raw)
    content_map = map_match.group(1).strip() if map_match else ""

    family, evidence = detect_family(document, tokens, content_map)

    html = document.find(lambda n: n.tag == "html")
    body = document.find(lambda n: n.tag == "body")
    html_lang = (html.attrs.get("lang") if html else "") or "en"
    body_lang = (body.attrs.get("data-lang") if body else "") or ""

    sections, fenced = slide_sections(document)

    # Languages: inline span classes are the evidence; the body's data-lang is the primary.
    span_langs: list[str] = []
    for span in document.find_all(lambda n: n.tag == "span"):
        for cls in span.classes:
            if cls in _LANG_SPAN_CLASSES:
                tag = _lang_tag(cls, html_lang)
                if tag not in span_langs:
                    span_langs.append(tag)
    if body_lang:
        primary = _lang_tag(body_lang, html_lang)
    elif html_lang.lower().startswith("zh"):
        primary = _lang_tag("zh", html_lang)
    else:
        primary = html_lang.split("-")[0].lower()
    languages = [primary] + [lang for lang in span_langs if lang != primary]
    if primary not in span_langs and span_langs:
        # data-lang names a language the spans do not carry; keep the spans' order.
        languages = span_langs

    extractor = TextExtractor(languages, html_lang)

    title: LText = {}
    if body is not None:
        for key, value in body.attrs.items():
            if key.startswith("data-title-"):
                lang = _lang_tag(key[len("data-title-"):], html_lang)
                if lang in languages:
                    title[lang] = re.sub(r"\s+", " ", value).strip()
    if not title:
        title_node = document.find(lambda n: n.tag == "title")
        text = extractor.text(title_node)
        if text:
            title = text
        else:
            title = {languages[0]: path.stem}

    deck = Deck(
        source=path, family=family, title=title, primary_language=languages[0],
        languages=languages, tokens=tokens, language_fonts=language_fonts,
        content_map=content_map, fenced=fenced, evidence=evidence,
        dark=bool(sections) and all("dark" in section.classes for section in sections),
    )
    if not fenced:
        deck.omitted.append(
            "no LISA:CONTENT-START/END slides fence in this file (finished decks may drop it); "
            "every section.slide in the body was walked instead"
        )
    if family == "monomind-deck":
        deck.omitted.append(
            "monomind-deck carries one language inline (others come from the runtime translator), "
            "so only the primary language was imported"
        )

    parser = SlideParser(deck, extractor)
    for index, section in enumerate(sections, start=1):
        deck.slides.append(parser.parse_slide(section, index))

    # Parts: the eyebrow "Part N · name" (MonoMind) or the section/chapter slides.
    current_part: LText = {}
    for slide in deck.slides:
        if slide.part:
            current_part = slide.part
        elif slide.kind == "section":
            section_component = next((c for c in slide.components if c.type == "section"), None)
            number = section_component.data["number"] if section_component else {}
            current_part = {
                lang: " · ".join(part for part in (_pick(number, lang), _pick(slide.statement, lang)) if part)
                for lang in deck.languages
            }
            current_part = {lang: value for lang, value in current_part.items() if value}
            slide.part = current_part
        elif current_part and slide.kind == "content":
            slide.part = current_part
    return deck


# ---------------------------------------------------------------------------
# Rendering — source Markdown
# ---------------------------------------------------------------------------


def _md_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    if not headers and rows:
        headers = [""] * len(rows[0])
    lines = ["| " + " | ".join(_md_cell(h) for h in headers) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        padded = list(row) + [""] * (len(headers) - len(row))
        lines.append("| " + " | ".join(_md_cell(c) for c in padded[:len(headers)]) + " |")
    return lines


def render_component(component: Component, lang: str, asset_dir: str) -> list[str]:  # noqa: C901
    """Render one typed component as Markdown lines."""
    data = component.data
    kind = component.type
    p = lambda text: _pick(text, lang)  # noqa: E731
    lines: list[str] = []

    if kind == "paragraph":
        lines.append(p(data["text"]))
    elif kind == "heading":
        lines.append(f"**{p(data['text'])}**")
    elif kind == "note":
        lines.append(f"_{p(data['text'])}_")
    elif kind == "phase_label":
        lines.append(f"**{p(data['text'])}**")
    elif kind == "meta":
        lines.append("- Meta: " + " · ".join(p(item) for item in data["items"] if p(item)))
    elif kind == "links":
        for item in data["items"]:
            lines.append(f"- [{p(item['text'])}]({item['href']})")
    elif kind == "bullets":
        lines.extend(f"- {p(item)}" for item in data["items"] if p(item))
    elif kind == "ordered":
        lines.extend(f"{index}. {p(item)}" for index, item in enumerate(data["items"], start=1) if p(item))
    elif kind == "table":
        headers = [p(h) for h in data["headers"]]
        rows = []
        toned = any(row["tone"] for row in data["rows"])
        for row in data["rows"]:
            cells = [p(c) for c in row["cells"]]
            if toned:
                cells.append({"flag": "flagged", "good": "good"}.get(row["tone"], ""))
            rows.append(cells)
        if toned:
            headers = headers + ["Row tone"] if headers else headers
        lines.extend(_md_table(headers, rows))
    elif kind == "stat_row":
        toned = any(item["tone"] for item in data["items"])
        headers = ["Value", "Label"] + (["Tone"] if toned else [])
        rows = [[p(i["value"]), p(i["label"])] + ([i["tone"] or ""] if toned else []) for i in data["items"]]
        lines.append("Stat row:")
        lines.append("")
        lines.extend(_md_table(headers, rows))
    elif kind == "mega":
        note = p(data["note"])
        lines.append(f"**{p(data['value'])}**" + (f" — {note}" if note else ""))
    elif kind == "cards":
        toned = any(item["tone"] for item in data["items"])
        headers = ["Card", "Figure", "Detail"] + (["Tone"] if toned else [])
        rows = [[p(i["title"]), p(i["value"]), p(i["detail"])] + ([i["tone"] or ""] if toned else []) for i in data["items"]]
        lines.extend(_md_table(headers, rows))
    elif kind == "card_grid":
        for item in data["items"]:
            number = p(item["number"])
            title = p(item["title"])
            head = " · ".join(part for part in (number, title) if part)
            text = p(item["text"])
            lines.append(f"- **{head}**" + (f" — {text}" if text else ""))
    elif kind == "verdict":
        tone = {"cyan-v": " (resolved)", "dark": " (closing note)"}.get(data["tone"], "")
        lines.append(f"> **Verdict{tone}:** {p(data['text'])}")
    elif kind == "callout":
        lines.append(f"> {p(data['text'])}")
    elif kind == "decision":
        lines.append(f"> **{p(data['heading'])}** — {p(data['action'])}")
    elif kind == "bars":
        rows = [[p(i["label"]), p(i["value"]),
                 f"{i['width_percent']:g}%" if i["width_percent"] is not None else "",
                 i["tone"] or ""] for i in data["items"]]
        lines.append("Bar chart (values as printed; bar width as the markup's `--w`):")
        lines.append("")
        lines.extend(_md_table(["Item", "Value", "Bar width", "Tone"], rows))
    elif kind == "specs":
        for index, item in enumerate(data["items"], start=1):
            number = p(item["number"]) or str(index)
            sub = p(item["sub"])
            lines.append(f"{index}. **{number}** {p(item['text'])}" + (f" — {sub}" if sub else ""))
    elif kind == "points":
        for item in data["items"]:
            marker = item["marker"]
            lines.append(f"- **{marker}** {p(item['text'])}" if marker else f"- {p(item['text'])}")
    elif kind == "section":
        number = p(data["number"])
        lines.append(f"- Section{(' ' + number) if number else ''}: **{p(data['statement'])}**")
        if p(data["for"]):
            lines.append(f"- Section kicker: {p(data['for'])}")
        if p(data["lead"]):
            lines.append(f"- Lead: {p(data['lead'])}")
    elif kind == "chips":
        for item in data["items"]:
            flag = " (optional)" if item.get("optional") else ""
            desc = p(item["desc"])
            lines.append(f"- **{p(item['name'])}**{flag}" + (f" — {desc}" if desc else ""))
    elif kind == "tree":
        def walk(items: list[dict[str, Any]], depth: int) -> None:
            for item in items:
                desc = p(item["desc"])
                lines.append("  " * depth + f"- `{p(item['name'])}`" + (f" — {desc}" if desc else ""))
                walk(item["children"], depth + 1)
        walk(data["items"], 0)
    elif kind == "leader_rows":
        for item in data["items"]:
            lines.append(f"- **{p(item['name'])}** — {p(item['desc'])}")
    elif kind == "steps":
        for index, item in enumerate(data["items"], start=1):
            number = p(item["number"]) or str(index)
            text = p(item["text"])
            lines.append(f"{number}. **{p(item['title'])}**" + (f" — {text}" if text else ""))
    elif kind == "workflow":
        for row in data["rows"]:
            phase = p(row["phase"])
            sub = p(row["sub"])
            lines.append(f"**{phase}**" + (f" ({sub})" if sub else ""))
            lines.append("")
            for index, node in enumerate(row["nodes"], start=1):
                number = p(node["number"]) or str(index)
                text = p(node["text"])
                lines.append(f"{number}. **{p(node['title'])}**" + (f" — {text}" if text else ""))
            lines.append("")
    elif kind == "code":
        lines.append("```")
        lines.append(p(data["text"]))
        lines.append("```")
    elif kind == "flags":
        for item in data["items"]:
            lines.append(f"- `{p(item['flag'])}` — {p(item['desc'])}")
    elif kind == "arrow":
        caption = p(data["caption"])
        lines.append(f"→ {caption}" if caption else "→")
    elif kind == "map":
        headers = [p(h) for h in data["headers"]]
        if len(headers) < 2:
            headers = ["From", "To"]
        lines.extend(_md_table([headers[0], "→", headers[-1]], [[p(r["left"]), "→", p(r["right"])] for r in data["rows"]]))
    elif kind == "frame":
        label = p(data["label"])
        if label:
            lines.append(f"**{label}**" + (" (accent panel)" if data.get("accent") else ""))
            lines.append("")
        if p(data["text"]):
            lines.append(p(data["text"]))
            lines.append("")
        for child in data["children"]:
            lines.extend(render_component(Component(child["type"], child["data"]), lang, asset_dir))
            lines.append("")
        if p(data["note"]):
            lines.append(f"_{p(data['note'])}_")
    elif kind == "image":
        if data.get("file"):
            lines.append(f"![{data['alt']}]({asset_dir}/{data['file']})")
        else:
            lines.append(f"Image (not imported): {data.get('alt') or data.get('src', '')}")
    elif kind == "unclassified":
        lines.append(f"<!-- unclassified markup: {data['markup']} -->")
        lines.append(p(data["text"]))
    else:
        lines.append(json.dumps(data, ensure_ascii=False))
    return [line for line in lines if line is not None]


def render_markdown(deck: Deck, lang: str, stem: str) -> str:
    """Render the deck as the source Markdown the Strategist reads."""
    p = lambda text: _pick(text, lang)  # noqa: E731
    asset_dir = f"{stem}_files"
    info = FAMILY_INFO[deck.family]
    lines = [f"# {p(deck.title) or stem}", ""]
    lines.append(
        f"<!-- {INTAKE_SCHEMA}: source={deck.source.name}; family={deck.family}; "
        f"language={lang}; slides={len(deck.slides)} -->"
    )
    lines.append("")
    others = [other for other in deck.languages if other != lang]
    if lang == deck.primary_language:
        sibling_note = "".join(f"; `{stem}.{other}.md` carries `{other}`" for other in others)
    else:
        sibling_note = f"; `{stem}.md` carries the primary `{deck.primary_language}`"
    lines.append(
        f"Imported from the Hi Ted, Meet Lisa `{deck.family}` deck `{deck.source.name}` "
        f"({info['name']}, a `{info['type']}` template): {len(deck.slides)} slides; "
        f"languages {', '.join(deck.languages)} ({deck.primary_language} primary). "
        f"This file carries the `{lang}` text{sibling_note}. Components are rendered as Markdown "
        "lists and tables in slide order; the deck chrome (brand mark, page numbers, menu, "
        "language switch, colophon) is not content and was left out."
    )
    lines.append("")
    for slide in deck.slides:
        label = p(slide.label) or f"Slide {slide.number:02d}"
        lines.append(f"## Slide {slide.number:02d} — {label}")
        lines.append("")
        lines.append(f"- Kind: {slide.kind}" + (f" · {p(slide.part)}" if p(slide.part) else ""))
        if p(slide.eyebrow):
            lines.append(f"- Eyebrow: {p(slide.eyebrow)}")
        if p(slide.statement):
            lines.append(f"- Statement: {p(slide.statement)}")
        if p(slide.lead):
            lines.append(f"- Lead: {p(slide.lead)}")
        lines.append("")
        for component in slide.components:
            rendered = render_component(component, lang, asset_dir)
            if rendered:
                lines.extend(rendered)
                lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Rendering — design_spec.md
# ---------------------------------------------------------------------------


def color_rows(deck: Deck) -> tuple[list[tuple[str, str, str]], list[str]]:
    """Resolve the family's colour roles to (role, hex, purpose) rows plus omissions."""
    family = deck.family
    if family == "monomind-deck":
        roles = COLOR_ROLES["monomind-deck" if deck.dark else "monomind-deck-light"]
    else:
        roles = COLOR_ROLES[family]
    rows: list[tuple[str, str, str]] = []
    omitted: list[str] = []
    for role, candidates, purpose in roles:
        chosen = None
        for token in candidates:
            value = resolve_token(deck.tokens, token)
            if value is None:
                continue
            hex_value = normalize_hex(value)
            if hex_value:
                chosen = (token, hex_value)
                break
            omitted.append(f"colour role {role}: `{token}` is `{value}` (not a flat #RRGGBB); left `[fill]`")
        if chosen:
            rows.append((role, chosen[1], f"`fact` — `{chosen[0]}` in the deck's `:root`; {purpose}"))
        else:
            missing = ", ".join(f"`{t}`" for t in candidates)
            rows.append((role, "[fill]", f"the deck declares no flat hex for this role ({missing})"))
    return rows, omitted


def font_plan(deck: Deck) -> dict[str, Any]:
    tokens = deck.tokens
    display = split_font_stack(resolve_token(tokens, "--font-display") or "")
    body = split_font_stack(resolve_token(tokens, "--font-body") or "")
    mono = split_font_stack(resolve_token(tokens, "--font-mono") or "")
    english_body = body
    english_display = display
    for lang, fonts in deck.language_fonts.items():
        if lang == "en":
            if "--font-body" in fonts:
                english_body = split_font_stack(fonts["--font-body"])
            if "--font-display" in fonts:
                english_display = split_font_stack(fonts["--font-display"])
    return {
        "display": display, "body": body, "mono": mono,
        "english_display": english_display, "english_body": english_body,
        "per_language": {
            lang: {name: split_font_stack(value) for name, value in fonts.items()}
            for lang, fonts in deck.language_fonts.items()
        },
    }


def render_design_spec(deck: Deck, project_name: str, canvas: Optional[dict[str, str]]) -> str:  # noqa: C901
    """Pre-fill the Design Spec from the deck's own tokens; leave the rest `[fill]`."""
    info = FAMILY_INFO[deck.family]
    lang = deck.primary_language
    p = lambda text: _pick(text, lang)  # noqa: E731
    rows, _ = color_rows(deck)
    fonts = font_plan(deck)
    non_primary = [l for l in deck.languages if l != lang]
    is_english = lang == "en"

    def stack(families: list[str]) -> str:
        return ", ".join(families) if families else "[fill]"

    def tail(families: list[str]) -> str:
        return ", ".join(families[1:]) if len(families) > 1 else "[fill]"

    canvas_name = canvas["name"] if canvas else "[fill: confirm at Stage 1 — the HTML deck is a 16:9 screen, ppt169 recommended]"
    canvas_dims = canvas["dimensions"] if canvas else "[fill]"
    canvas_viewbox = f"`{canvas['viewbox']}`" if canvas else "[fill]"

    lines = [
        "<!-- ppt-master-schema: design-spec/v1 -->",
        f"# {project_name} - Design Spec",
        "",
        "## I. Project Information",
        "",
        "| Item | Value |",
        "| --- | --- |",
        f"| Project Name | {project_name} |",
        f"| Canvas Format | {canvas_name}{(' (' + canvas_dims + ')') if canvas else ''} |",
        f"| Page Count | {len(deck.slides)} |",
        f"| Primary Language | {lang} |",
        "| Target Audience | [fill] |",
        "| Communication Intent | [fill] |",
        "| Desired Audience Outcome | [fill] |",
        "| Core Message / Ask / Action | [fill] |",
        "| Delivery Context | [fill] |",
        "| Artifact Afterlife | [fill] |",
        f"| Reading Mode | [fill: recommended {info['reading_mode']} — the Lisa template is a `{info['type']}` shape] |",
        "| Content Strategy | [fill] |",
        f"| Design Style | Lisa `{deck.family}` ({info['name']}): {info['tagline']} — `fact`, the deck's own template |",
        "| AI Image Acquisition Path | [fill or not applicable] |",
        "| Generation Mode | [fill] |",
        "| Spec Refinement | [fill] |",
        "| Speaker Notes | [fill enabled/disabled plus provenance] |",
        "| Custom Animations | [fill enabled/disabled plus provenance] |",
        "| Narration Audio | [fill enabled/disabled plus provenance] |",
        f"| Created Date | {datetime.now().strftime('%Y-%m-%d')} |",
        "",
        f"- **Source deck (fact)**: `{deck.source.name}`, template family `{deck.family}`, "
        f"{len(deck.slides)} slides, languages {', '.join(deck.languages)}"
        + (f"; the `{non_primary[0]}` text is in `sources/{deck.source.stem}.{non_primary[0]}.md`" if non_primary else "")
        + ". Pre-filled by `lisa_html_intake.py`; every remaining placeholder is a Stage-1/Stage-2 "
        "decision the markup does not carry.",
        "",
        "## II. Canvas Specification",
        "",
        "| Property | Value |",
        "| --- | --- |",
        f"| Format | {canvas_name if canvas else '[fill]'} |",
        f"| Dimensions | {canvas_dims} |",
        f"| viewBox | {canvas_viewbox} |",
        "| Margins | [fill] |",
        "| Content Area | [fill] |",
        "",
        "## III. Visual Theme",
        "",
        "### Theme Style",
        "",
        "- **Mode**: [fill]",
        "- **Visual style**: [fill]",
        f"- **Theme**: {info['tagline']} (`fact` — the `{deck.family}` template's own description)",
        "- **Tone**: [fill]",
        "",
        "### Color Scheme",
        "",
        "| Role | HEX | Purpose |",
        "| --- | --- | --- |",
    ]
    for role, hex_value, purpose in rows:
        lines.append(f"| {role} | {hex_value} | {purpose} |")
    lines.extend([
        "",
        "## IV. Typography System",
        "",
        "### Font Plan",
        "",
        "| Role | Character (Reference) | Primary | English if non-English | Fallback tail |",
        "| --- | --- | --- | --- | --- |",
        f"| Title | [fill] | {fonts['display'][0] if fonts['display'] else '[fill]'} | "
        f"{'n/a (English primary)' if is_english else (fonts['english_display'][0] if fonts['english_display'] else '[fill]')} | {tail(fonts['display'])} |",
        f"| Body | [fill] | {fonts['body'][0] if fonts['body'] else '[fill]'} | "
        f"{'n/a (English primary)' if is_english else (fonts['english_body'][0] if fonts['english_body'] else '[fill]')} | {tail(fonts['body'])} |",
        "",
        f"- **Title stack**: {stack(fonts['display'])}",
        f"- **Body stack**: {stack(fonts['body'])}",
    ])
    if fonts["mono"]:
        lines.append(f"- **Code stack**: {stack(fonts['mono'])}")
        lines.append("- **Role rationale**: `code` — the deck sets paths, identifiers, and commands in `--font-mono` (`fact`)")
    for other_lang, per in fonts["per_language"].items():
        parts = [f"{name[7:]} {', '.join(families)}" for name, families in per.items()]
        lines.append(f"- **Language stacks (fact, `body[data-lang=\"{other_lang}\"]`)**: " + "; ".join(parts))
    lines.append(
        "- **Font provenance (fact)**: every family above is the deck's own `--font-*` token, loaded from "
        "Google Fonts in the HTML; the PPTX export flags non-PPT-safe faces — keep them and record "
        "\"requires <family>\" here, or substitute the house family at Stage 2."
    )
    lines.extend([
        "",
        "### Font Size Hierarchy",
        "",
        "| Purpose | Anchor Size (px) |",
        "| --- | ---: |",
        "| Body | [fill] |",
        "| Title | [fill] |",
        "| Subtitle | [fill] |",
        "| Annotation | [fill] |",
        "",
        "## V. Layout Principles",
        "",
        "### Deck-wide Direction",
        "",
        "- **Hierarchy direction**: [fill]",
        "- **Composition tendency**: [fill]",
        f"- **Cross-page continuity**: {_continuity(deck)}",
        "- **Spacing posture**: [fill]",
        "- **Spacing anchors**: [fill]",
        "",
        "## VI. Icon Usage Specification",
        "",
        "- **Primary bundled library**: [fill]",
        "",
        "| Icon Path | Suitable Scenarios |",
        "| --- | --- |",
        "",
        "## VIII. Image Resource List",
        "",
        "| Filename | Dimensions | Ratio | Purpose | Type | Layout pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for image in deck.images:
        width, height = image["width"], image["height"]
        dims = f"{width}x{height}" if width and height else "[fill]"
        ratio = _ratio(width, height) if width and height else "[fill]"
        lines.append(
            f"| {image['filename']} | {dims} | {ratio} | {image['alt'] or '[fill]'} | photo | [fill] | "
            f"[fill] | user | Existing | embedded in `{deck.source.name}` slide {image['slide']:02d} (`fact`) | [fill] | [fill] |"
        )
    lines.extend(["", "## IX. Content Outline", ""])
    current_part: Optional[str] = None
    part_index = 0
    for slide in deck.slides:
        part_name = p(slide.part)
        if part_index == 0 or part_name != current_part:
            part_index += 1
            current_part = part_name
            lines.append(f"### Part {part_index}: {part_name or '[fill]'}")
            lines.append("")
        label = p(slide.label) or f"Slide {slide.number:02d}"
        lines.append(f"#### Slide {slide.number:02d} - {label}")
        lines.append("")
        lines.append("- **Audience move**: [fill]")
        lines.append("- **Relationships**: [fill]")
        lines.append(f"- **Title**: {p(slide.statement) or label}")
        core = _core_message(slide, lang)
        lines.append(f"- **Core message**: {core}")
        lines.append("- **Content**:")
        if p(slide.eyebrow):
            lines.append(f"  - Eyebrow: {p(slide.eyebrow)}")
        if p(slide.lead):
            lines.append(f"  - Lead: {p(slide.lead)}")
        for component in slide.components:
            lines.append(f"  - {_brief(component, lang)}")
        if not p(slide.eyebrow) and not p(slide.lead) and not slide.components:
            lines.append("  - (the slide carries only its statement)")
        images = [c for c in slide.components if c.type == "image" and c.data.get("file")]
        if images:
            lines.append("- **Images**: " + "; ".join(f"`{c.data['file']}` — {c.data['alt']}" for c in images))
        lines.append("")
    lines.extend([
        "## X. Speaker Notes Requirements",
        "",
        "- **Generation**: [fill enabled or disabled]",
        "- **Filename**: match each SVG filename under `notes/`",
        "- **Content**: [fill]",
        "",
    ])
    return "\n".join(lines)


def _ratio(width: int, height: int) -> str:
    divisor = gcd(width, height)
    return f"{width // divisor}:{height // divisor}"


def _continuity(deck: Deck) -> str:
    facts = []
    if deck.family == "monomind-deck":
        facts.append("the brand mark on every slide")
        facts.append("kicker → statement → lead → canvas on every content slide")
    else:
        facts.append("the page number bottom-left on content slides")
        facts.append("eyebrow → statement → body on every content page")
    if deck.family == "paper-brief":
        facts.append("inverted chapter pages marking the seams")
    if deck.family == "evidence-deck":
        facts.append("orange section cards opening each part")
    return "; ".join(facts) + " (`fact` — observed in the markup)"


def _core_message(slide: Slide, lang: str) -> str:
    for component in slide.components:
        if component.type == "verdict" and _pick(component.data["text"], lang):
            return f"{_pick(component.data['text'], lang)} (from the deck's verdict bar)"
        if component.type == "decision" and _pick(component.data["action"], lang):
            return f"{_pick(component.data['action'], lang)} (from the deck's decision box)"
    for component in slide.components:
        if component.type == "callout" and component.data.get("role") in {"loop", "endbar"} and _pick(component.data["text"], lang):
            return f"{_pick(component.data['text'], lang)} (from the deck's takeaway line)"
    return "[fill]"


def _brief(component: Component, lang: str) -> str:  # noqa: C901
    """One §IX block-list line per component, at `brief` depth."""
    data = component.data
    p = lambda text: _pick(text, lang)  # noqa: E731
    kind = component.type
    if kind == "table":
        headers = " / ".join(p(h) for h in data["headers"]) or "no header"
        flagged = sum(1 for r in data["rows"] if r["tone"] == "flag")
        return f"Table ({len(data['rows'])} rows): {headers}" + (f"; {flagged} flagged row(s)" if flagged else "")
    if kind == "stat_row":
        return "Stat row: " + " · ".join(f"{p(i['value'])} {p(i['label'])}".strip() for i in data["items"])
    if kind == "mega":
        return f"Mega number: {p(data['value'])}" + (f" — {p(data['note'])}" if p(data["note"]) else "")
    if kind == "cards":
        return "Cards: " + " / ".join(f"{p(i['title'])} {p(i['value'])}".strip() for i in data["items"])
    if kind == "card_grid":
        return "Card grid: " + " / ".join(f"{p(i['number'])} {p(i['title'])}".strip() for i in data["items"])
    if kind == "verdict":
        return f"Verdict bar: {p(data['text'])}"
    if kind == "callout":
        return f"Takeaway line: {p(data['text'])}"
    if kind == "decision":
        return f"Decision box ({p(data['heading'])}): {p(data['action'])}"
    if kind == "bars":
        return "Bar chart (" + ", ".join(f"{p(i['label'])} = {p(i['value'])}" for i in data["items"]) + ")"
    if kind == "specs":
        return f"Spec list ({len(data['items'])}): " + " / ".join(p(i["text"]) for i in data["items"])
    if kind == "points":
        return f"Numbered points ({len(data['items'])}): " + " / ".join(f"{i['marker']} {p(i['text'])}".strip() for i in data["items"])
    if kind == "section":
        return f"Section card {p(data['number'])}: {p(data['statement'])}" + (f" — {p(data['lead'])}" if p(data["lead"]) else "")
    if kind == "paragraph":
        return f"Body: {p(data['text'])}"
    if kind == "bullets":
        return f"Bullets ({len(data['items'])}): " + " · ".join(p(i) for i in data["items"])
    if kind == "ordered":
        return f"Ordered list ({len(data['items'])}): " + " · ".join(p(i) for i in data["items"])
    if kind == "chips":
        return "Chips: " + " / ".join(p(i["name"]) for i in data["items"])
    if kind == "tree":
        return f"File tree rooted at `{p(data['items'][0]['name']) if data['items'] else ''}`"
    if kind == "leader_rows":
        return "Leader rows: " + " / ".join(p(i["name"]) for i in data["items"])
    if kind == "steps":
        return f"Steps ({len(data['items'])}): " + " → ".join(p(i["title"]) for i in data["items"])
    if kind == "workflow":
        return "Workflow: " + " | ".join(f"{p(r['phase'])}: " + " → ".join(p(n["title"]) for n in r["nodes"]) for r in data["rows"])
    if kind == "code":
        return "Code block: " + p(data["text"]).replace("\n", " ")[:120]
    if kind == "flags":
        return "Flags: " + " / ".join(p(i["flag"]) for i in data["items"])
    if kind == "arrow":
        return f"Connector: {p(data['caption'])}"
    if kind == "map":
        return f"Mapping ({len(data['rows'])} rows): " + " / ".join(f"{p(r['left'])} → {p(r['right'])}" for r in data["rows"])
    if kind == "frame":
        inner = "; ".join(_brief(Component(c["type"], c["data"]), lang) for c in data["children"])
        return f"Panel {p(data['label'])}: {inner or p(data['text'])}"
    if kind == "image":
        return f"Image: {data.get('alt') or data.get('file') or 'external'}"
    if kind == "meta":
        return "Meta: " + " · ".join(p(i) for i in data["items"])
    if kind == "links":
        return "Links: " + " / ".join(p(i["text"]) for i in data["items"])
    if kind == "note":
        return f"Note: {p(data['text'])}"
    if kind == "unclassified":
        return f"Unclassified markup ({data['markup']}): {p(data['text'])}"
    if kind in {"heading", "phase_label"}:
        return f"{kind.replace('_', ' ').capitalize()}: {p(data['text'])}"
    return f"{kind}: {json.dumps(data, ensure_ascii=False)[:100]}"


# ---------------------------------------------------------------------------
# Outline / summary
# ---------------------------------------------------------------------------


def outline_json(deck: Deck) -> dict[str, Any]:
    def component_dict(component: Component) -> dict[str, Any]:
        return {"type": component.type, "data": component.data}

    return {
        "schema": INTAKE_SCHEMA,
        "source": str(deck.source),
        "family": deck.family,
        "family_evidence": deck.evidence,
        "title": deck.title,
        "primary_language": deck.primary_language,
        "languages": deck.languages,
        "fenced": deck.fenced,
        "page_count": len(deck.slides),
        "tokens": deck.tokens,
        "language_fonts": deck.language_fonts,
        "colors": [{"role": r, "hex": h, "purpose": p} for r, h, p in color_rows(deck)[0]],
        "fonts": font_plan(deck),
        "slides": [
            {
                "number": s.number, "kind": s.kind, "part": s.part, "label": s.label,
                "page_number": s.page_number, "eyebrow": s.eyebrow, "statement": s.statement,
                "lead": s.lead, "components": [component_dict(c) for c in s.components],
                "unclassified": s.unknown,
            }
            for s in deck.slides
        ],
        "images": [{k: v for k, v in image.items() if k != "bytes"} for image in deck.images],
        "omitted": deck.omitted,
    }


def component_census(deck: Deck) -> dict[str, int]:
    census: dict[str, int] = {}

    def count(component: Component) -> None:
        census[component.type] = census.get(component.type, 0) + 1
        if component.type == "frame":
            for child in component.data["children"]:
                count(Component(child["type"], child["data"]))

    for slide in deck.slides:
        for component in slide.components:
            count(component)
    return dict(sorted(census.items()))


def render_summary(deck: Deck, outputs: list[Path], dry_run: bool) -> str:
    lang = deck.primary_language
    lines = [
        f"Lisa deck: {deck.source.name}",
        f"  family:     {deck.family} ({'; '.join(deck.evidence)})",
        f"  title:      {_pick(deck.title, lang)}",
        f"  languages:  {', '.join(deck.languages)} (primary {lang})",
        f"  slides:     {len(deck.slides)}" + ("" if deck.fenced else "  [no content fence; walked section.slide]"),
        "  components: " + (", ".join(f"{k} ×{v}" for k, v in component_census(deck).items()) or "none"),
    ]
    rows, color_omissions = color_rows(deck)
    facts = [f"{role} {hex_value}" for role, hex_value, _ in rows if hex_value.startswith("#")]
    lines.append("  colours:    " + (", ".join(facts) or "none as flat hex"))
    fonts = font_plan(deck)
    lines.append(
        f"  fonts:      display {', '.join(fonts['display']) or '—'} | body {', '.join(fonts['body']) or '—'}"
        + (f" | mono {', '.join(fonts['mono'])}" if fonts["mono"] else "")
    )
    if deck.images:
        lines.append(f"  images:     {len(deck.images)} embedded image(s) written to sources/<stem>_files/")
    lines.append("")
    lines.append("Slides:")
    for slide in deck.slides:
        label = _pick(slide.label, lang)
        statement = _pick(slide.statement, lang)
        kinds = ", ".join(c.type for c in slide.components) or "—"
        lines.append(f"  {slide.number:02d} [{slide.kind}] {label}: {statement[:80]}")
        lines.append(f"      components: {kinds}")
    lines.append("")
    omissions = list(deck.omitted) + color_omissions + [
        "font sizes: the deck sizes type with clamp() relative to the viewport, not canvas px; §IV sizes left `[fill]`",
        "canvas, audience, intent, outcome, delivery context, mode, visual style, tone, spacing, icons, "
        "speaker notes: not in the markup; left `[fill]` for Stage 1/Stage 2",
        "chrome not imported: brand mark, page numbers, progress bar, nav dots, menu, language switch, "
        "colophon, copy buttons; CSS background photography stays with the template",
    ]
    lines.append("Not invented (left [fill] or listed):")
    for item in omissions:
        lines.append(f"  - {item}")
    lines.append("")
    if dry_run:
        lines.append("Dry run: nothing written.")
    else:
        lines.append("Written:")
        for path in outputs:
            lines.append(f"  - {path}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Project integration
# ---------------------------------------------------------------------------


def resolve_project(project_arg: str, canvas_format: Optional[str]) -> tuple[Path, bool]:
    """Return (project_path, created). An existing project dir is reused."""
    from project_manager import ProjectManager  # noqa: E402 — sibling script

    path = Path(project_arg).expanduser()
    if path.exists():
        if not path.is_dir():
            raise IntakeError(f"--project is not a directory: {path}")
        markers = ("svg_output", "sources", "README.md", "validation")
        if not any((path / marker).exists() for marker in markers):
            raise IntakeError(
                f"{path} exists but is not a Lisa's PPT project (no svg_output/, sources/, or README.md); "
                "pass a new path to create one"
            )
        return path.resolve(), False
    # `init` appends `_<format>_<YYYYMMDD>`; a re-run with the same --project
    # reuses the directory it created rather than creating a second one.
    dated = re.compile(rf"^{re.escape(path.name)}(?:_[a-z0-9]+)?_\d{{8}}$")
    if path.parent.is_dir():
        matches = sorted(p for p in path.parent.iterdir() if p.is_dir() and dated.match(p.name))
        if len(matches) == 1:
            return matches[0].resolve(), False
        if len(matches) > 1:
            raise IntakeError(
                f"{path} matches several projects ({', '.join(m.name for m in matches)}); pass the exact path"
            )
    manager = ProjectManager()
    with contextlib.redirect_stdout(sys.stderr):
        created = manager.init_project(path.name, canvas_format, base_dir=str(path.parent))
    return Path(created).resolve(), True


def canvas_info(project_path: Path) -> Optional[dict[str, str]]:
    """Return the registered canvas encoded in the project directory name, if any."""
    try:
        from project_utils import CANVAS_FORMATS, get_project_info  # noqa: E402
    except ImportError:
        return None
    info = get_project_info(str(project_path))
    fmt = info.get("format")
    if not fmt or fmt == "unknown" or fmt not in CANVAS_FORMATS:
        return None
    entry = CANVAS_FORMATS[fmt]
    return {
        "id": fmt,
        "name": entry.get("name", fmt),
        "dimensions": entry.get("dimensions", ""),
        "viewbox": entry.get("viewBox") or entry.get("viewbox") or f"0 0 {entry.get('dimensions', '').replace('x', ' ')}",
    }


def write_outputs(deck: Deck, project_path: Path, *, force: bool, archive: bool) -> list[Path]:
    """Write sources, design_spec.md, analysis, and the workflow note."""
    outputs: list[Path] = []
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", deck.source.stem).strip("._") or "lisa_deck"
    sources_dir = project_path / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    spec_path = project_path / "design_spec.md"
    if spec_path.exists() and not force:
        raise IntakeError(f"{spec_path} already exists; pass --force to overwrite the pre-filled spec")

    primary_md = sources_dir / f"{stem}.md"
    primary_md.write_text(render_markdown(deck, deck.primary_language, stem), encoding="utf-8")
    outputs.append(primary_md)
    for lang in deck.languages[1:]:
        sibling = sources_dir / f"{stem}.{lang}.md"
        sibling.write_text(render_markdown(deck, lang, stem), encoding="utf-8")
        outputs.append(sibling)

    if deck.images:
        asset_dir = sources_dir / f"{stem}_files"
        asset_dir.mkdir(parents=True, exist_ok=True)
        manifest = []
        for image in deck.images:
            target = asset_dir / image["filename"]
            target.write_bytes(image["bytes"])
            outputs.append(target)
            manifest.append({
                "filename": image["filename"], "alt": image["alt"], "slide": image["slide"],
                "width": image["width"], "height": image["height"], "format": image["format"],
                "source": deck.source.name,
            })
        manifest_path = asset_dir / "image_manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        outputs.append(manifest_path)

    if archive:
        archived = sources_dir / f"{stem}.html"
        if archived.resolve() != deck.source.resolve():
            shutil.copy2(deck.source, archived)
            outputs.append(archived)

    try:
        from _conversion_profile import write_conversion_profile_best_effort  # noqa: E402
        profile = write_conversion_profile_best_effort(
            input_path=str(deck.source), markdown_path=primary_md, converter=CONVERTER_NAME,
            conversion_type=CONVERSION_TYPE, warnings=list(deck.omitted),
        )
        if profile is not None:
            outputs.append(profile)
    except ImportError:
        pass

    canvas = canvas_info(project_path)
    spec_path.write_text(render_design_spec(deck, project_path.name, canvas), encoding="utf-8")
    outputs.append(spec_path)

    analysis_dir = project_path / "analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    outline_path = analysis_dir / "lisa_intake.json"
    outline_path.write_text(json.dumps(outline_json(deck), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    outputs.append(outline_path)

    try:
        from workflow_log import append_note  # noqa: E402
        append_note(
            project_path,
            f"lisa_html_intake: imported {deck.source.name} (family={deck.family}, slides={len(deck.slides)}, "
            f"languages={','.join(deck.languages)}) into sources/ and pre-filled design_spec.md",
        )
    except (ImportError, OSError):
        pass
    return outputs


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import a Hi Ted, Meet Lisa HTML slide deck into a Lisa's PPT project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 scripts/lisa_html_intake.py deck.html --project projects/deck
  python3 scripts/lisa_html_intake.py deck.html --project projects/deck --format ppt169
  python3 scripts/lisa_html_intake.py deck.html --dry-run
  python3 scripts/lisa_html_intake.py deck.html --dry-run --json
""",
    )
    parser.add_argument("deck", help="Lisa HTML deck (monomind-deck, evidence-deck, or paper-brief family)")
    parser.add_argument("--project", help="Project directory: reused when it exists, created via project_manager.py otherwise")
    parser.add_argument("--format", default=None, help="Registered canvas format for a newly created project (e.g. ppt169)")
    parser.add_argument("--dry-run", action="store_true", help="Print the outline and summary; write nothing")
    parser.add_argument("--json", action="store_true", help="Print the machine-readable outline instead of the text summary")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing design_spec.md")
    parser.add_argument("--no-archive", action="store_true", help="Do not copy the original HTML into sources/")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.dry_run and not args.project:
        parser.error("--project <path> is required unless --dry-run is given")

    deck_path = Path(args.deck).expanduser()
    if not deck_path.is_file():
        print(f"[ERROR] deck not found: {deck_path}", file=sys.stderr)
        return 1
    try:
        deck = read_deck(deck_path.resolve())
    except IntakeError as exc:
        print(f"[ERROR] {deck_path.name}: {exc}", file=sys.stderr)
        return 2

    outputs: list[Path] = []
    if not args.dry_run:
        try:
            project_path, created = resolve_project(args.project, args.format)
            print(
                f"[>>] {'created' if created else 'using'} project {project_path}", file=sys.stderr,
            )
            outputs = write_outputs(deck, project_path, force=args.force, archive=not args.no_archive)
        except (IntakeError, FileExistsError, ValueError, OSError) as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            return 1
        print(f"[OK] imported {deck.source.name}: {len(deck.slides)} slides -> {project_path}", file=sys.stderr)

    if args.json:
        payload = outline_json(deck)
        payload["outputs"] = [str(path) for path in outputs]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_summary(deck, outputs, args.dry_run))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
