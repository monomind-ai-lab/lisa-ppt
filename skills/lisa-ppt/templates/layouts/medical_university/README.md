# medical_university

A structure-only 16:9 Layout: header band with accent bar and pulse trace,
key-message strip, open content field, two-column card agenda, full-bleed
chapter divider with cross and ring decorations. The contract is
[`templates/design_spec.md`](./templates/design_spec.md); the five prototypes
beside it are complete Slide previews.

**Names**: Medical University · 의과대학·병원 · 醫學大學

## Provenance and migration

Ported into Lisa's PPT from byungjunjang/slide-master (`166472b`), where it was one of seven PPT Master v2–v3 layouts (present upstream at
v2.0.0 and v3.0.0, replaced by v4) that slide-master kept after upstream
replaced its layout set. Migrated to the v6.1.0 structured contract here:

- Roster renumbered to the documented five-page order (`01_cover`, `02_toc`,
  `03_chapter`, `04_content`, `05_ending`); Layout keys are `cover`, `toc`,
  `chapter`, `content`, `ending` (the legacy keys were the file stems, with
  picker names Agenda and Section) on one Master, `medical_university_master`
  (was `medical_university-master`).
- Legacy `data-pptx-placeholder-bounds` / `-carrier` / `-idx` spellings became
  `data-pptx-bounds` / `data-pptx-carrier` / `data-pptx-idx`; every fixed
  visual (bands, accent bars, pulse-trace paths, dividers and their caps,
  agenda cards and bars, cross marks, rings, footer bands and rules) is a
  direct Layout atom with a stable id — most legacy chrome carried no layer
  attribute at all; no ordinary groups or XML comments remain.
- Text that was Slide-local in the legacy files (presenter lines, date,
  contact card, chapter number and description, source, section name, agenda
  descriptions, institution footers) became typed slots. Simplified-Chinese
  labels baked into carriers (`汇报人：`, `指导老师：`, `数据来源：`), the
  fixed `目 录` heading with its `CONTENTS` eyebrow, the `可用布局…` hint, the
  two sample `数据卡片` frames, and the dashed content-area guide were
  removed — the marker now carries the whole line, the agenda heading is a
  `title` slot, and the eyebrow is a `subtitle` slot `{{PAGE_TITLE_EN}}`.
- The content title `{{SECTION_NUM}} {{PAGE_TITLE}}` collapsed to
  `{{PAGE_TITLE}}`.
- The cover's `{{DEPARTMENT}}　｜　{{ADVISOR}}` line became two half-width
  `object` slots (department end-anchored to x 628, advisor starting at
  x 652) with a Layout hairline at x 640 in place of the `｜` glyph, so each
  marker is its own native frame.
- Agenda cards: the description moved from under the ordinal (x 120) to under
  the title (x 190 / 770) as one two-line `object` frame, because a native
  text frame cannot indent only its first line; cards 5–6, which the legacy
  drew as a centered title alone, gained ordinals `05` / `06` and a
  description line so all six cards share one contract in muted paint.
- The `{{LOGO}}` text with `data-pptx-role="logo"` became a reserved
  `object` slot named `{{BRAND_LOGO}}`; the Layout owns the zone, the Brand
  owns the mark.
- Three invisible legacy rects were dropped (the agenda container
  `80 100 1120 520` and the content logo zone `1100 20 140 30`, both
  `fill="none"` with no stroke, and the content field's white panel on the
  white plane); their geometry survives as slot bounds where relevant.
- Attribute spellings normalised: `font-weight="bold"` → `700`,
  `stroke-dasharray="4,4"` → `"4 4"`, the preview font stack, and explicit
  `x`/`y`/`width`/`height` on the root and the master background.
- The prototype paint is the legacy palette kept as preview values; the spec
  names no color, typeface, or scale.

## Gaps

None. Every legacy page is represented; the two "optional" agenda cards are
now the same slot contract as the other four, in muted paint.
