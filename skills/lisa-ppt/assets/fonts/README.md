# Bundled Fonts

One house family per language, plus one mono face, each in its own directory
beside its SIL Open Font License 1.1 text. PPTX does **not** embed fonts: a
deck authored or opened on a machine without the family falls back to a
system face, so install the bundled families user-level wherever decks are
authored or opened:

```bash
python3 skills/lisa-ppt/scripts/install_fonts.py --dry-run   # show the plan
python3 skills/lisa-ppt/scripts/install_fonts.py             # macOS / Windows / Linux, user-level
python3 skills/lisa-ppt/scripts/install_fonts.py --check     # report what is installed
```

The policy — one house family per language, hierarchy through weight, size,
tracking and colour, never by switching families — is declared once in the
repository `AGENTS.md` and enforced in `references/strategist.md` §g.
`preflight.py` warns when any bundled family is not installed.

| Language | Family | Directory | Bundled weights | Source |
|---|---|---|---|---|
| Korean | Pretendard v1.3.9 | `Pretendard/` | Light 300, Regular 400, Medium 500, SemiBold 600, Bold 700, ExtraBold 800 | [orioncactus/pretendard](https://github.com/orioncactus/pretendard) |
| Traditional Chinese | Noto Sans TC (Noto Sans CJK 2.004, TC subset OTF) | `NotoSansTC/` | Light 300, Regular 400, Medium 500, Bold 700 | [notofonts/noto-cjk](https://github.com/notofonts/noto-cjk) tag `Sans2.004` |
| English | Plus Jakarta Sans | `PlusJakartaSans/` | Light 300, Regular 400, Medium 500, SemiBold 600, Bold 700, ExtraBold 800 | [tokotype/PlusJakartaSans](https://github.com/tokotype/PlusJakartaSans) `18d1cd2` |
| ids and code, any language | JetBrains Mono v2.304 | `JetBrainsMono/` | Regular 400, Medium 500, SemiBold 600 | [JetBrains/JetBrainsMono](https://github.com/JetBrains/JetBrainsMono) tag `v2.304` |

Prompts, specs and locks may name only these weights; no other cut exists in
this repository.

## How to author a weight

Every family follows the same rule, because that is how the static cuts name
themselves: **Regular and Bold fold into the plain family name** and are
authored with `font-weight` 400 / 700; **every other cut is its own installed
family name**, authored at normal weight.

| Family | `font-weight` 400 / 700 | Own family names (normal weight) |
|---|---|---|
| Pretendard | `Pretendard` | `"Pretendard Light"`, `"Pretendard Medium"`, `"Pretendard SemiBold"`, `"Pretendard ExtraBold"` |
| Noto Sans TC | `"Noto Sans TC"` | `"Noto Sans TC Light"`, `"Noto Sans TC Medium"` |
| Plus Jakarta Sans | `"Plus Jakarta Sans"` | `"Plus Jakarta Sans Light"`, `"Plus Jakarta Sans Medium"`, `"Plus Jakarta Sans SemiBold"`, `"Plus Jakarta Sans ExtraBold"` |
| JetBrains Mono | `"JetBrains Mono"` (400 only) | `"JetBrains Mono Medium"`, `"JetBrains Mono SemiBold"` |

## Fallback stacks

The tail after the house family is a browser-preview aid and a courtesy to a
machine that has not run the installer; the converter never exports it. One
stack per language, cross-platform:

| Language | `font-family` |
|---|---|
| Korean | `Pretendard, "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", sans-serif` |
| Traditional Chinese | `"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", "Noto Sans CJK TC", sans-serif` |
| English | `"Plus Jakarta Sans", "Segoe UI", "Helvetica Neue", Arial, sans-serif` |
| ids and code | `"JetBrains Mono", Menlo, Consolas, monospace` |

## What the converter does

`DUAL_SCRIPT_FONTS` in `scripts/svg_to_pptx/drawingml/utils.py` lists
Pretendard and Noto Sans TC with their bundled cuts: both cover Latin as well
as their script, so the converter writes them into **both** the Latin and the
East-Asian typeface slots and a mixed run stays in one family. Plus Jakarta
Sans and JetBrains Mono are Latin-only and fill the Latin slot; an English
deck that needs a CJK companion names it after the Latin face
(`"Plus Jakarta Sans", Pretendard` → Latin Plus Jakarta Sans, East-Asian
Pretendard). None of the four is mapped to a Windows substitute.
