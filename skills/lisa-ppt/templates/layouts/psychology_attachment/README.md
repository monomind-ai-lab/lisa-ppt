# psychology_attachment

A structure-only 16:9 Layout: full-bleed soft-gradient framing pages (cover,
chapter, closing) that center a title stack over a warm rule, a quote block,
and a tag-chip row; left-rail working pages (agenda, content) with a
left-aligned title and echo line; a dual-column agenda with badge-indexed
items and a learning-goals panel; an open content field. The contract is
[`templates/design_spec.md`](./templates/design_spec.md); the five prototypes
beside it are complete Slide previews.

**Names**: Psychology Attachment · 심리 애착 · 心理依附

## Provenance and migration

Ported into Lisa's PPT from byungjunjang/slide-master (`166472b`), where it
was one of seven PPT Master v2–v3 layouts (present upstream at v2.0.0 and
v3.0.0, replaced by v4) that slide-master kept after upstream replaced its
layout set. Migrated to the v6.1.0 structured contract here:

- Roster renumbered to the documented five-page order (`01_cover`, `02_toc`,
  `03_chapter` was `02_chapter`, `04_content` was `03_content`, `05_ending`
  was `04_ending`); Layout keys are `cover`, `toc`, `chapter`, `content`,
  `ending` on one Master, `psychology_attachment_master` (was
  `psychology_attachment-master` with file-stem layout keys).
- The XML declaration and root `width` / `height` were added; legacy
  `data-pptx-placeholder-bounds` / `-carrier` / `-idx` spellings became
  `data-pptx-bounds` / `data-pptx-carrier` / `data-pptx-idx`; the
  `master-bg` rect became `master-background`; every fixed visual (gradient
  planes, rings, diagonals, the network, rails, rules, badges, chips, cards,
  panels, dots) is a direct Layout atom with a stable id; the translated
  item groups and the shared-font groups were resolved into atoms and slots,
  so no ordinary groups remain. Badge paths became equivalent rounded rects.
- Text that was Slide-local in the legacy files became typed slots: the
  echo lines (`{{TITLE_EN}}`, `{{CHAPTER_EN}}`, `{{THANK_YOU_EN}}`) as
  `subtitle`; the cover `{{SUBTITLE}}`, `{{ENDING_SUBTITLE}}`,
  `{{CLOSING_MESSAGE}}`, the ghost `{{CHAPTER_NUM}}` and the capsule badge,
  the quote block (`{{QUOTE}}` over `{{QUOTE_AUTHOR}}`, one two-line slot),
  the four `{{TAG_n}}` chip labels, every agenda item and learning goal (one
  two-line slot each), and the contact card as `object`; `{{THANK_YOU}}` as
  the closing `title`; `{{COPYRIGHT}}` as `footer`.
- The legacy content page typed its field `body`; it is now the `object`
  slot `{{CONTENT_AREA}}` with an upper-left carrier, and the dashed
  content-area guide frame and the layout-hint comment were dropped.
- The fixed `内容概览` / `Contents Overview` heading became `{{PAGE_TITLE}}`
  (`title`) and `{{PAGE_TITLE_EN}}` (`subtitle`); the fixed `📎 学习目标`
  column heading became the `object` slot `{{RIGHT_TITLE}}` (emoji dropped).
  The fixed `01` / `02` page-number samples on the cover and agenda became
  `slide-number` slots `{{PAGE_NUM}}`. The `CHAPTER ` label baked in front of
  the capsule `{{CHAPTER_NUM}}`, the quotation marks around `{{QUOTE}}`, and
  the `—— ` dash before `{{QUOTE_AUTHOR}}` were removed — the marker carries
  the whole line. Roman numerals Ⅰ–Ⅴ and goal indices 1–4 are Layout-owned
  ordinal atoms.
- `{{COVER_BG_IMAGE}}`, which existed only as a comment naming an optional
  background image, became a typed full-canvas `picture` slot carrying the
  shared 1 × 1 PNG carrier at `opacity="0.25"` — the alpha the legacy spec
  prescribed for that image, now a native picture-alpha mapping rather than
  the overlay scrim the legacy toolchain required.
- Fonts became the preview stack `Arial, Microsoft YaHei, sans-serif`;
  `font-weight="bold"` became `700`; gradient stops use attributes; the
  dashed divider uses `stroke-dasharray="6 4"`. The prototype paint is the
  legacy palette kept as preview values; the spec names no color, typeface,
  or scale.

## Gaps

None. Every legacy page and text role is represented. The legacy intent of
an optional cover photograph fading beneath the ring field cannot be
reproduced by z-order alone (a Slide placeholder always paints above Layout
atoms), so the picture slot carries the fade itself at 25 % alpha; the rings
and diagonals sit beneath it as the legacy comment intended.
