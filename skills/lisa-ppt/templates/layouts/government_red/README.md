# government_red

A structure-only 16:9 Layout: a 6 px two-tone top bar on every page, a
badge header over the light pages, a side-bar agenda beside a two-cell
statistics panel, an open content field, and full-bleed dark cover, chapter,
and closing planes with an orb-and-grid texture and a footer band. The
contract is [`templates/design_spec.md`](./templates/design_spec.md); the
five prototypes beside it are complete Slide previews.

**Names**: Government Red · 공공기관 레드 · 政府紅

## Provenance and migration

Ported into Lisa's PPT from byungjunjang/slide-master (`166472b`), where it
was one of seven PPT Master v2–v3 layouts (present upstream at v2.0.0 and
v3.0.0, replaced by v4) that slide-master kept after upstream replaced its
layout set. Migrated to the v6.1.0 structured contract here:

- Roster renumbered to the documented five-page order (`01_cover`, `02_toc`,
  `03_chapter`, `04_content`, `05_ending`); Layout keys are `cover`, `toc`,
  `chapter`, `content`, `ending` on one Master, `government_red_master`
  (was `government_red-master` with `01_cover`-style keys and the picker
  names Agenda / Section).
- Legacy `data-pptx-placeholder-bounds` / `-carrier` / `-idx` spellings became
  `data-pptx-bounds` / `data-pptx-carrier` / `data-pptx-idx`; every fixed
  visual (gradient planes, orbs, grid hairlines, bars, badges, panel, rules,
  bands) is a direct Layout atom with a stable id; the ordinary item groups
  and the chapter page's `translate(640, 360)` group were resolved into
  absolute atoms and slots, so no unbounded groups remain. Gradient
  definitions keep the legacy stops in attribute form on `0..1` coordinates.
- Text that was Slide-local in the legacy files (presenter lines, date,
  organisation line, chapter number and subtitle, statistics cells, agenda
  items, contact line, closing band line) became typed slots. The fixed
  `目 录` heading became a `{{PAGE_TITLE}}` title slot and its `CONTENTS`
  eyebrow a `{{PAGE_TITLE_EN}}` subtitle; the fixed `目` glyph inside the
  agenda badge became a `{{PAGE_BADGE}}` object slot (the badge rect stays an
  atom, matching the content page where the same badge carries
  `{{CHAPTER_NUM}}`). The baked `0` in front of `{{CHAPTER_NUM}}` was removed
  so the marker carries the whole number.
- The dashed content frame and the `(由 Executor …)` hint were dropped; the
  content field is one `object` slot `{{CONTENT_AREA}}` (was a `body` slot)
  whose carrier starts upper-left. The top-right `{{ORG_SHORT}}` mark became
  the `{{BRAND_LOGO}}` object zone; the footer `{{ORG_SHORT}}` became a
  `{{FOOTER_NOTE}}` footer slot. Every `_EN` echo (`{{AUTHOR_EN}}`,
  `{{THANK_YOU_EN}}`) keeps its name.
- The redundant white full-canvas Layout rect on the agenda and content pages
  was dropped (the Master plane is already white); the dark pages keep their
  gradient rect as the first Layout atom rather than a background, because
  only a solid rect may own a background.
- The legacy comments named a real regional government office; no comment
  and no organisation name survive. Fonts are the preview stack, `bold`
  became `700`, and `letter-spacing` on the two echo lines is kept as
  unitless px.
- The prototype paint is the legacy palette kept as preview values; the spec
  names no color, typeface, or scale.

## Gaps

None. Every legacy page is represented. The cover carries no logo zone
because the legacy cover drew no corner mark; a deck that needs one uses the
content page's `{{BRAND_LOGO}}` zone.
