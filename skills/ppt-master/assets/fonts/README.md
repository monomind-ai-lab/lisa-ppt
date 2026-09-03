# Bundled Fonts

Fonts bundled with the skill, each beside its licence text. PPTX does **not**
embed fonts: a deck authored or opened on a machine without the family falls
back to a system face, so install the bundled families user-level wherever
decks are authored or opened:

```bash
python3 skills/ppt-master/scripts/install_fonts.py --dry-run   # show the plan
python3 skills/ppt-master/scripts/install_fonts.py             # macOS / Windows / Linux, user-level
python3 skills/ppt-master/scripts/install_fonts.py --check     # report what is installed
```

The house-font policy — one fixed family, hierarchy through weight, size,
tracking and colour, never by switching families — is declared once in the
repository `AGENTS.md` and enforced in `references/strategist.md` §g.

## Pretendard

[Pretendard](https://github.com/orioncactus/pretendard) v1.3.9 —
SIL Open Font License 1.1 (`Pretendard/LICENSE.txt`). Korean + Latin coverage
in one family.

Exactly six static cuts (OTF) are bundled, and prompts may name only these:

| File | Weight | SVG `font-family` to author |
|---|---|---|
| `Pretendard-Light.otf` | 300 | `"Pretendard Light"` at normal weight |
| `Pretendard-Regular.otf` | 400 | `Pretendard` with `font-weight: 400` |
| `Pretendard-Medium.otf` | 500 | `"Pretendard Medium"` at normal weight |
| `Pretendard-SemiBold.otf` | 600 | `"Pretendard SemiBold"` at normal weight |
| `Pretendard-Bold.otf` | 700 | `Pretendard` with `font-weight: 700` |
| `Pretendard-ExtraBold.otf` | 800 | `"Pretendard ExtraBold"` at normal weight |

Regular and Bold fold into the `Pretendard` family; the other four are
separate installed family names. The converter exports Pretendard into both
the Latin and East-Asian typeface slots (`DUAL_SCRIPT_FONTS` in
`scripts/svg_to_pptx/drawingml/utils.py`), so mixed Korean/Latin runs stay in
one family. Any CSS tail after `Pretendard` in a stack is a browser-preview
aid only; the cross-platform per-language tail is decided in the rebrand.
