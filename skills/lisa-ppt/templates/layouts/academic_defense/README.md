# academic_defense

A structure-only 16:9 Layout: header band with accent bar, key-message strip,
open content field, two-column card agenda, full-bleed chapter divider. The
contract is [`templates/design_spec.md`](./templates/design_spec.md); the
five prototypes beside it are complete Slide previews.

**Names**: Academic Defense · 학위 논문 심사 · 學位論文答辯

## Provenance and migration

Ported into Lisa's PPT from byungjunjang/slide-master (`166472b`), where it
was one of seven PPT Master v2–v3 layouts (present upstream at v2.0.0 and
v3.0.0, replaced by v4) that slide-master kept after upstream replaced its
layout set. Migrated to the v6.1.0 structured contract here:

- Roster renumbered to the documented five-page order (`01_cover`, `02_toc`,
  `03_chapter`, `04_content`, `05_ending`); Layout keys are `cover`, `toc`,
  `chapter`, `content`, `ending` on one Master, `academic_defense_master`.
- Legacy `data-pptx-placeholder-bounds` / `-carrier` / `-idx` spellings became
  `data-pptx-bounds` / `data-pptx-carrier` / `data-pptx-idx`; every fixed
  visual is a direct Layout atom; every ordinary root group was resolved into
  atoms or slots, so no unbounded groups remain.
- Text that was Slide-local in the legacy files (presenter lines, date,
  contact card, chapter number and description, source and section name)
  became typed slots; Simplified-Chinese labels baked into carriers
  (`答辩人：`, `指导老师：`, `数据来源：`, the fixed `目 录` heading and the
  dashed-guide hint) were removed — the marker now carries the whole line and
  the agenda heading is a `title` slot.
- The `{{LOGO}}` text with `data-pptx-role="logo"` became a reserved
  `object` slot named `{{BRAND_LOGO}}`; the Layout owns the zone, the Brand
  owns the mark.
- The prototype paint is the legacy palette kept as preview values; the spec
  names no color, typeface, or scale.

## Gaps

None. Every legacy page is represented; the two "optional" agenda cards are
now the same slot contract as the other four, in muted paint.
