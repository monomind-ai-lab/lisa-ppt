---
brand_id: monomind
kind: brand
summary: MonoMind house identity — Hi Ted, Meet Lisa decks in PowerPoint; deep ink on a pale blue page, one blue accent, one house family per language (Plus Jakarta Sans, Pretendard, Noto Sans TC)
primary_color: "#4F8CFF"
---

# MonoMind Brand Specification

> Identity-only preset. No SVG page roster — pages are composed freely under these constraints.

> Provenance marks: `fact` is read verbatim from the `:root` block of `assets/tedandlisa-template.html` (the MonoMind deck template) or from `assets/monomind-mark-white.svg`, both in `monomind-ai-lab/hi-ted-meet-lisa`, read 2026-09-03. `approx` is derived from a `fact` value for a solid-fill medium and says how. The template writes its hex values in lower case; the HEX column normalises to upper case, the value is the same.

## I. Brand Overview

| Property | Value |
|---|---|
| Brand Name | MonoMind AI Lab |
| Use Cases | Hi Ted, Meet Lisa decks that have to be a `.pptx`: project and product briefings, roadmap and evidence decks, technical talks; the handoff from `/lisa` (Lane B) and the import of a Lisa HTML deck (Lane A) |
| Tone | Plain, declarative, concrete nouns and numbers, no adjectives doing sales work; conclusion first |
| Sources | `assets/tedandlisa-template.html` `:root` blocks (lines 23–92: contract tokens and the font layer) and `assets/monomind-mark-white.svg` in `monomind-ai-lab/hi-ted-meet-lisa` |

## II. Color Scheme

| Role | HEX | Provenance | Notes |
|---|---|---|---|
| primary | `#4F8CFF` | fact | `--accent` (the template's `--meta` carries the same value). Buttons, links, eyebrows, the one signal colour on a page; `accent-on` text sits on it |
| neutral-dark | `#102033` | fact | `--fg`. Body text on the page; the fill of the deep-ink slides (cover, section openers, closing) |
| bg | `#EEF6FF` | fact | `--bg`. The page |
| text-2 | `#34465F` | fact | `--fg-2`. Second-level text, leads, subtitles |
| muted-text | `#60708A` | fact | `--muted`. Captions, chart labels, footers, page numbers |
| accent-on | `#FFFFFF` | fact | `--accent-on`. Text on the accent and on the ink; the mark on deep-ink slides |
| surface | `#FBFDFF` | approx | `--surface` is `rgba(255, 255, 255, 0.74)` (`fact`); flattened over `bg` because a PPTX card here is a solid fill. Card and panel background |
| border | `#C1CCD9` | approx | The template's `--hair` is `--fg-2` at 24 % over transparent (`fact`); flattened over `bg`. Card borders, dividers, table rules |
| accent-wash | `#DEEBFF` | approx | The template's `--accent-wash` is `--accent` at 10 % over transparent (`fact`); flattened over `bg`. Tinted panels, highlighted table rows, chart backgrounds |
| positive | `#22C55E` | fact | `--success`. Recommended options, success states |
| alert (warn) | `#F59E0B` | fact | `--warn`. Cautions |
| alert (risk) | `#EF4444` | fact | `--danger`. Risks, failures |

The first six rows are the identity. The three `approx` rows are what the template's translucent layers read as once flattened onto the page; use them, do not derive others. The three status colours are the template's own tokens and are used for status only, never as a second accent. Deep-ink slides invert: `neutral-dark` as the fill, `accent-on` for text, `primary` unchanged. Strategist may set the dominance of ink and page per section, but every deck opens and closes on ink.

## III. Typography

One house family per language. Hierarchy comes from weight, size, tracking and colour, never from switching families. A deck is set in the family of its language; the other two families are companions for a foreign word, not a second voice.

| Role | Family | Weight |
|---|---|---|
| title (EN) | `"Plus Jakarta Sans", "Segoe UI", "Helvetica Neue", Arial, sans-serif` | 600–700 |
| body (EN) | `"Plus Jakarta Sans", "Segoe UI", "Helvetica Neue", Arial, sans-serif` | 400–500 |
| title (KO) | `Pretendard, "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", sans-serif` | 600–700 |
| body (KO) | `Pretendard, "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", sans-serif` | 400–500 |
| title (ZH-TW) | `"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", "Noto Sans CJK TC", sans-serif` | 600–700 |
| body (ZH-TW) | `"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", "Noto Sans CJK TC", sans-serif` | 400–500 |
| mono (ids, code, figures in tables) | `"JetBrains Mono", Menlo, Consolas, monospace` | 400–600 |

> `fact`: the template's `--font-display` and `--font-body` are `"Plus Jakarta Sans"`, its `--font-mono` is `"JetBrains Mono"`, and its Google Fonts link loads Plus Jakarta Sans at 400/500/600/700 and JetBrains Mono at 400/500/600. Display tracking is `-0.03em` (`--tracking-display`), display leading 1.04, body leading 1.65. Pretendard for Korean and Noto Sans TC for Traditional Chinese are the house decision recorded in the repository `AGENTS.md` font policy, not template tokens. The fallback tails after each house family are `approx`: the repository's cross-platform stacks (`AGENTS.md`, `assets/fonts/README.md`), so a machine without the family degrades to its own system face rather than to a Windows-only one.

> Lisa's PPT embeds no fonts and PowerPoint does not follow a CSS fallback chain. The house family must be installed on the machine that opens the deck (`scripts/install_fonts.py`), and the converter registers the CJK families for both the Latin and the East-Asian slot. All four families, JetBrains Mono included, are bundled under `assets/fonts/`; prompts name only the weights that are bundled: Pretendard and Plus Jakarta Sans 300–800 in six cuts, Noto Sans TC 300 / 400 / 500 / 700, JetBrains Mono 400 / 500 / 600.

## IV. Logo

One mark, no wordmark. The bundled file is the MonoMind mark with `fill="currentColor"` on both of its paths (`fact`): it carries no literal colour and takes the colour set where it is placed.

| File | Form | Usage |
|---|---|---|
| `../images/monomind-mark-white.svg` | MonoMind mark, square, `viewBox="0 0 512 512"`, two paths, `currentColor` fill | Cover and closing slide on the deep-ink fill, coloured `#FFFFFF`; a header or footer corner on the page, coloured `#102033` |

- Cover: the mark once, on the deep-ink fill, between 0.5× and 1× the title's cap height; set the colour to `#FFFFFF` at placement
- Closing slide: the mark once, the same way
- Per-page: optional, one corner, small; do not stamp every page
- Clearspace: at least 0.5× mark height of empty space on all sides; never over text or a photograph
- A converter that needs a literal fill gets one at placement (`#FFFFFF` on ink, `#102033` on the page). Do not edit the SVG to hard-code a colour; the file's own header says so
- Never distort, outline, or add a drop shadow to the mark

## V. Voice & Tone

- Formality: plain and direct; short declaratives, concrete nouns and numbers
- Person: we / you (English), 저희 / 여러분 (Korean), 我們 / 您 (Traditional Chinese)
- Emoji: avoid
- Abbreviations: spell-out-first-use
- Headings name a thing; no em dashes in headings
- A figure the agent does not have stays a bracketed slot; it never becomes an invented number

## VI. Icon Style

- Preference: stroke

> Presentation convention, not a brand token. Prefer the `tabler` or `lucide` stroke families in `templates/icons/`; keep one icon family per deck, stroke weight matched to the body weight, coloured `neutral-dark` on the page and `accent-on` on ink, `primary` only for the one icon a page is about.
