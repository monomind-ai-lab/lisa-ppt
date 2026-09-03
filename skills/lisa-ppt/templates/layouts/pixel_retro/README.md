# pixel_retro

A structure-only 16:9 Layout: one dark plane framed by neon dual rules and
pixel-block corners, a console mark and chip row on the cover, a tagged card
agenda beside a stat panel, a framed chapter number, an open content field,
and a three-card closing summary with a call-to-action card. The contract is
[`templates/design_spec.md`](./templates/design_spec.md); the five prototypes
beside it are complete Slide previews.

**Names**: Pixel Retro · 픽셀 레트로 · 像素復古

## Provenance and migration

Ported into Lisa's PPT from byungjunjang/slide-master (`166472b`), where it
was one of seven PPT Master v2–v3 layouts (present upstream at v2.0.0 and
v3.0.0, replaced by v4) that slide-master kept after upstream replaced its
layout set. Migrated to the v6.1.0 structured contract here:

- Roster renumbered to the documented five-page order (`01_cover`, `02_toc`,
  `03_chapter` was `02_chapter`, `04_content` was `03_content`, `05_ending`
  was `04_ending`); Layout keys are `cover`, `toc`, `chapter`, `content`,
  `ending` on one Master, `pixel_retro_master` (was `pixel_retro-master` with
  filename-shaped keys such as `01_cover`).
- Legacy `data-pptx-placeholder-bounds` / `-carrier` / `-idx` spellings became
  `data-pptx-bounds` / `data-pptx-carrier` / `data-pptx-idx`; every
  translated group (console, chip row, agenda cards, stat panel, chapter
  frame, progress tracks, summary cards, call-to-action card) was flattened
  into direct Layout atoms with absolute coordinates, so no ordinary `<g>`
  remains. The unfilled zero-width progress fill on the agenda page was
  dropped.
- The legacy glow filters (bare `feGaussianBlur` + `feMerge` on
  `SourceGraphic`) were rewritten as the sanctioned blur + flood + composite +
  merge glow graph in the same accent colors; unused filter definitions were
  removed and `stdDeviation` values below 4 were raised to 4.
- Text that was Slide-local in the legacy files (subtitles, author, version,
  chapter number and title, the closing title and subtitle, summary cards,
  feature list, comparison table, call-to-action and contact lines) became
  typed slots. Fixed sample chips became `object` slots: the cover's four
  labelled buttons are `{{TAG_1}}`–`{{TAG_4}}`, and the agenda's
  Simplified-Chinese importance tabs are `{{TAG_1}}`–`{{TAG_4}}`; the cover
  prompt line became `{{CTA_TEXT}}`; the agenda panel heading became a
  `body` `{{KEY_MESSAGE}}` slot and each stat tile carries `{{STAT_n}}` over a
  `{{STAT_n_LABEL}}` tspan in place of its fixed Chinese label; the agenda
  footer's fixed `Table of Contents` became a `footer` `{{SECTION_NAME}}`
  slot.
- Emoji prefixes baked in front of markers (`📍 {{PAGE_TITLE}}`,
  `🎯 {{THANK_YOU}}`, `🎮 {{CTA_TEXT}}`) were removed so the marker carries
  the whole line; the fixed `01/` page prefix on the cover became the
  `{{PAGE_NUM}}` field; the chapter, content and closing page counters keep
  `{{PAGE_NUM}} / {{TOTAL_PAGES}}` in one `slide-number` carrier.
- Template-only guides (the dashed content-area frame and its Executor hint
  comments) were dropped; the content field is one `object`
  `{{CONTENT_AREA}}` slot starting upper-left. Fixed Chinese sample strings
  with no structural role (`0% 完成`, `█ 点击章节开始学习`) were dropped, as
  were the sample `90%` bar label on the closing page and the `- Thank You!
  🎉` tail of the closing footer label (now `THE END`).
- The agenda's three stat tiles were re-spaced from a 120 px pitch (tiles 1
  and 2 overlapped by 20 px in the legacy file) to a 160 px pitch so the three
  140 px tiles fill the 460 px track width without overlapping.
- Font stacks were normalized to the preview values (`Consolas, Monaco,
  monospace` for display and chrome roles, `Arial, Microsoft YaHei,
  sans-serif` for reading roles) and `font-weight="bold"` became `700`; the
  prototype paint is the legacy palette kept as preview values; the spec
  names no color, typeface, or scale.

## Gaps

None. Every legacy page is represented; the genre chrome the legacy pages
drew as fixed text (`CHAPTER`, `▶ START`, `LOADING...`, `GAME SAVED ✓`,
`CONTINUE →`, `THE END`) stays as Layout text atoms because it labels page
structure rather than deck content.
