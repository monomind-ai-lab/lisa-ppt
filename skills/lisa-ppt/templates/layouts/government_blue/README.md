# government_blue

A structure-only 16:9 Layout: full-bleed gradient planes on the cover,
chapter, and closing pages, pale washes on the agenda and content pages, a
6 px top strip and a left side bar on every page, a numbered-badge agenda, a
badge-and-title header over an open content field. The contract is
[`templates/design_spec.md`](./templates/design_spec.md); the five prototypes
beside it are complete Slide previews.

**Names**: Government Blue · 공공기관 블루 · 政府藍

## Provenance and migration

Ported into Lisa's PPT from byungjunjang/slide-master (`166472b`), where it was
one of seven PPT Master v2–v3 layouts (present upstream at v2.0.0 and v3.0.0,
replaced by v4) that slide-master kept after upstream replaced its layout set.
Migrated to the v6.1.0 structured contract here:

- Roster renumbered to the documented five-page order (`01_cover`, `02_toc`,
  `03_chapter`, `04_content`, `05_ending`); Layout keys are `cover`, `toc`,
  `chapter`, `content`, `ending` on one Master, `government_blue_master`
  (was `government_blue-master` with `01_cover`-style layout keys).
- Legacy `data-pptx-placeholder-bounds` / `-carrier` / `-idx` spellings became
  `data-pptx-bounds` / `data-pptx-carrier` / `data-pptx-idx`; every fixed
  visual is a direct Layout atom with a stable `id`; the five ordinary agenda
  groups and the chapter page's `translate(640, 360)` group were resolved into
  absolute-coordinate atoms and slots, so no unbounded groups remain.
- Text that was Slide-local in the legacy files (presenter, organization,
  date, agenda heading and eyebrow, agenda items, chapter number, title,
  subtitle and organization, content-page chapter badge number, footer
  organization, closing title, echo, message, organization and contact)
  became typed slots; the Simplified-Chinese label baked into the presenter
  carrier (`汇报人：`), the fixed `目 录` heading and `CONTENTS` eyebrow, and
  the fixed closing line `欢迎批评指正` were replaced by markers — the agenda
  heading is a `title` slot `{{PAGE_TITLE}}`, the eyebrow a `subtitle` slot
  `{{PAGE_TITLE_EN}}`, the closing line an `object` slot `{{CLOSING_MESSAGE}}`.
- The `{{ORG_SHORT}}` corner marks (cover lower right, content header) became
  a reserved `object` slot named `{{BRAND_LOGO}}`; the content page's footer
  `{{ORG_SHORT}}` became a `footer` slot `{{FOOTER_NOTE}}`. The Layout owns
  the zone, the Brand owns the mark.
- The chapter number lost its baked `0` prefix (`0{{CHAPTER_NUM}}` →
  `{{CHAPTER_NUM}}`); its two overlaid legacy texts (a 5 % fill and a 20 %
  outline) are one carrier that carries both the fill and the stroke.
- The legacy content page's `body` slot became the `object` content field
  `{{CONTENT_AREA}}` with an upper-left carrier; the dashed content-area frame
  and the `(由 Executor …)` hint were dropped as template-only guides.
- The cover's `<pattern>` grid texture was dropped (no native mapping); every
  gradient, orb, diagonal, side bar, band, grid line, and wave path is kept as
  a Layout atom with its legacy opacity. Gradient coordinates are written in
  unitless `0..1` object-bounding-box form.
- The prototype paint is the legacy palette kept as preview values; the spec
  names no color, typeface, or scale.

## Gaps

None. Every legacy page is represented; the cover's grid texture is the only
visual not carried, because `<pattern>` fills have no native mapping and the
6 px strip, side bar, orbs and diagonals already carry the composition.
