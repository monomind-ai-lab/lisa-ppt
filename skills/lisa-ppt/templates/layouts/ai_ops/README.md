# ai_ops

A structure-only 16:9 Layout: thin top strip, split two-color left block,
light summary bands, square numbered badges indexing tag chips, dashed module
panels, and a dense one-page architecture overview. The contract is
[`templates/design_spec.md`](./templates/design_spec.md); the six prototypes
beside it are complete Slide previews.

**Names**: AI Ops · AI 운영 · AI 維運

## Provenance and migration

Ported into Lisa's PPT from byungjunjang/slide-master (`166472b`), where it was one of seven PPT Master v2–v3 layouts (present upstream at
v2.0.0 and v3.0.0, replaced by v4) that slide-master kept after upstream
replaced its layout set. Migrated to the v6.1.0 structured contract here:

- Roster renumbered to the documented five-page order (`01_cover`, `02_toc`,
  `03_chapter` was `02_chapter`, `04_content` was `03_content`, `05_ending`
  was `04_ending`) plus the renamed sixth page below; Layout keys are `cover`,
  `toc`, `chapter`, `content`, `ending`, `architecture_overview` on one
  Master, `ai_ops_master` (the legacy root used `ai_ops-master` and repeated
  the file stems as layout keys).
- The XML declaration was added; legacy `data-pptx-placeholder-bounds` /
  `-carrier` / `-idx` spellings became `data-pptx-bounds` /
  `data-pptx-carrier` / `data-pptx-idx`; XML comments were removed; every
  fixed visual (strips, blocks, bands, badges, chip rects, panels, rules, the
  overview triangle) is a direct Layout atom with a stable id; quoted
  `'Microsoft YaHei', Arial` font stacks and `font-weight="bold"` were
  normalised to the preview stack and numeric weights.
- Text that was Slide-local in the legacy files (author, date, agenda items
  and summary, chapter number and description, section name, source, closing
  tagline, contact and copyright) became typed slots. The fixed `目 录`
  heading on the agenda panel became a `{{PAGE_TITLE}}` title slot and its
  fixed `CONTENTS` eyebrow a `{{PAGE_TITLE_EN}}` subtitle slot. The five
  fixed cover chips and four closing chips with Simplified-Chinese words
  became `{{TAG_1..5}}` / `{{TAG_1..4}}` object slots; the chip rects stay
  atoms and the badge numbers `1`–`5` are Layout-owned ordinal atoms.
- The content page's `{{CONTENT_AREA}}` moved from a centered `body` carrier
  to an `object` slot whose carrier starts upper-left; its dashed
  template-guide frame and the invisible white header rect were dropped, and
  the page-number slot keeps a 90 px strip centered on the 30 × 24 badge, tall enough for the badge text.
- The chapter page's 160 px watermark echo of `{{CHAPTER_NUM}}` was dropped:
  the marker now lives once, in the 80 × 80 badge (the legacy file painted the
  watermark over the badge, so nothing legible is lost).
- The prototype paint is the legacy palette kept as preview values; the spec
  names no color, typeface, or scale.

## Renamed page

`reference_style.svg` — a fully written sample slide with real telecom copy —
became `06_architecture_overview.svg` (`git mv`), Layout key
`architecture_overview`, picker name "Architecture Overview", so `page_types`
ends `…, ending, architecture_overview`. The composition is unchanged: title
with accent bar, summary band, pale triangle backdrop, rounded target bar, six
KPI chips, four tag chips, the dashed orchestration panel with its header band
and three dashed sub-panels, the warm side panel, and three base boxes with
corner badges and dashed title rules. Every sample line became a slot —
`{{PAGE_TITLE}}` title, `{{KEY_MESSAGE}}` body, and `{{TARGET}}`,
`{{KPI_1..6}}`, `{{TAG_1..4}}`, `{{BLOCK_SUMMARY}}`, `{{BLOCK_1..3}}`,
`{{SIDE_CONTENT}}`, `{{CARD_1..3}}` object slots — and the row labels
(成效, 应用场景, 智能体编排, 开放, 基础能力), the starburst, and the cost box
were removed.

## Gaps

The sample copy of `reference_style.svg` was removed by contract: a Layout
carries no example content, so the page now shows markers where the source
showed a finished telecom architecture. Three consequences of that removal
cannot be carried as structure: the KPI chips' two-color figure (black label,
red number) is one single-run slot per chip; the small light-blue item chips
inside the orchestration sub-panels, the gray entries in the side panel, and
the gray capability chips inside the base boxes are Slide-local content
rather than Layout atoms (their count was content, not structure); and the
chapter watermark number is not reproduced because one marker owns one slot.
