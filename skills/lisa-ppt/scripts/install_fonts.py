#!/usr/bin/env python3
"""
Lisa's PPT - Bundled Font Installer

Installs the font families bundled under assets/fonts/ at user level on
macOS, Windows and Linux, so a deck authored here and a deck opened here both
render with the family the prompts name. PPTX does not embed fonts: run this
on every machine that authors or opens the decks.

Usage:
    python3 scripts/install_fonts.py [--dry-run] [--check] [--family NAME] [--force]

Examples:
    python3 scripts/install_fonts.py --dry-run      # show what would be copied where
    python3 scripts/install_fonts.py                # install every bundled family user-level
    python3 scripts/install_fonts.py --check        # report which bundled files are installed
    python3 scripts/install_fonts.py --family Pretendard --force

Dependencies:
    None (only uses standard library)
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from console_encoding import configure_utf8_stdio  # noqa: E402

SKILL_DIR = _SCRIPTS_DIR.parent
FONTS_DIR = SKILL_DIR / "assets" / "fonts"
FONT_SUFFIXES = {".otf", ".ttf", ".ttc"}


def bundled_families() -> dict[str, list[Path]]:
    """Map each bundled family directory name to its font files."""
    families: dict[str, list[Path]] = {}
    if not FONTS_DIR.is_dir():
        return families
    for family_dir in sorted(p for p in FONTS_DIR.iterdir() if p.is_dir()):
        files = sorted(p for p in family_dir.iterdir() if p.suffix.lower() in FONT_SUFFIXES)
        if files:
            families[family_dir.name] = files
    return families


def user_font_dir(family: str) -> Path:
    """User-level font directory for this platform (created on install)."""
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Library" / "Fonts"
    if sys.platform == "win32":
        local = os.environ.get("LOCALAPPDATA") or str(home / "AppData" / "Local")
        return Path(local) / "Microsoft" / "Windows" / "Fonts"
    return home / ".local" / "share" / "fonts" / family


def _registry_name(font_file: Path) -> str:
    """Windows per-user font registry value name, e.g. 'Pretendard SemiBold (OpenType)'."""
    stem = font_file.stem.replace("-", " ")
    kind = "OpenType" if font_file.suffix.lower() == ".otf" else "TrueType"
    return f"{stem} ({kind})"


def _register_windows(font_file: Path, installed: Path) -> None:
    """Register a per-user font so Office sees it without a reboot."""
    try:
        import winreg  # type: ignore[import-not-found]
    except ImportError:  # not Windows
        return
    key = winreg.CreateKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows NT\CurrentVersion\Fonts",
    )
    with key:
        winreg.SetValueEx(key, _registry_name(font_file), 0, winreg.REG_SZ, str(installed))


def _same_file(a: Path, b: Path) -> bool:
    return a.is_file() and b.is_file() and a.stat().st_size == b.stat().st_size


def plan(families: dict[str, list[Path]]) -> list[tuple[Path, Path, str]]:
    """Return (source, destination, state) rows; state is installed | missing | differs."""
    rows = []
    for family, files in families.items():
        dest_dir = user_font_dir(family)
        for src in files:
            dest = dest_dir / src.name
            if _same_file(src, dest):
                state = "installed"
            elif dest.exists():
                state = "differs"
            else:
                state = "missing"
            rows.append((src, dest, state))
    return rows


def install(rows: list[tuple[Path, Path, str]], *, force: bool, dry_run: bool) -> int:
    copied = 0
    for src, dest, state in rows:
        if state == "installed" and not force:
            print(f"  = {dest.name}: already installed")
            continue
        print(f"  + {src.name} -> {dest}" + (" (dry run)" if dry_run else ""))
        if dry_run:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        if sys.platform == "win32":
            _register_windows(src, dest)
        copied += 1
    if copied and sys.platform not in ("darwin", "win32") and shutil.which("fc-cache"):
        subprocess.run(["fc-cache", "-f"], check=False)
    return copied


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install the bundled font families user-level (macOS / Windows / Linux).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--family", action="append", metavar="NAME",
                        help="only this bundled family directory (repeatable); default: all")
    parser.add_argument("--dry-run", action="store_true", help="print the plan; copy nothing")
    parser.add_argument("--check", action="store_true",
                        help="report installed/missing files and exit 1 when any is missing")
    parser.add_argument("--force", action="store_true", help="re-copy files that are already installed")
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_utf8_stdio()
    args = build_parser().parse_args(argv)
    families = bundled_families()
    if args.family:
        unknown = [f for f in args.family if f not in families]
        if unknown:
            print(f"[install_fonts] unknown family: {', '.join(unknown)}; bundled: "
                  f"{', '.join(families) or '(none)'}", file=sys.stderr)
            return 2
        families = {k: v for k, v in families.items() if k in args.family}
    if not families:
        print(f"[install_fonts] no bundled fonts under {FONTS_DIR}", file=sys.stderr)
        return 2

    rows = plan(families)
    print(f"[install_fonts] {len(rows)} file(s) in {len(families)} family(ies): {', '.join(families)}")
    if args.check:
        missing = 0
        for src, dest, state in rows:
            mark = "ok " if state == "installed" else "-- "
            print(f"  {mark}{src.name}: {state} ({dest})")
            missing += state != "installed"
        print(f"[install_fonts] {len(rows) - missing} installed, {missing} missing")
        return 1 if missing else 0

    copied = install(rows, force=args.force, dry_run=args.dry_run)
    if args.dry_run:
        print("[install_fonts] dry run — nothing copied")
    else:
        print(f"[install_fonts] {copied} file(s) copied; restart PowerPoint/Keynote to pick them up")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
