# Layout Templates

**Layout = a structure-only reusable template bundle**: canvas, Master/Layout structure, page types, slot geometry, semantic text roles, alignment/wrapping/capacity behavior, and the SVG roster — no brand color, typeface/weight identity, final type scale, logo, voice, or icon style (those come from a Brand/Deck or the confirmation stage). A layout may describe the content shapes and delivery conditions its geometry supports but never owns a communication objective, audience outcome, narrative sequence, boilerplate, or example content downstream must preserve — a structurally useful "board update" page stays a Layout; a board-update sequence with required decision, risk, and action roles is a Deck. Neutral colors, safe fonts, and provisional sizes in prototypes are preview values, not identity or a locked scale; Strategist inspects the prototypes and content, decides how much structure to reuse, and writes the exporter plan automatically. The shared kind and workspace model lives in the parent [`README.md`](../README.md).

| Axis | Layout behavior |
|---|---|
| Template kind | `layout`: structure only |
| Internal creation strategy | AI-derived `standard` / `fidelity` for a new system or `mirror` for validated source materialization; tool provenance, not a user choice — Layout mirror additionally requires a brand-neutral, application-neutral source (otherwise author through `standard` / `fidelity` or create a Deck; removing rules is never mirror) |
| Application planning | Strategist decides literal, structural, or style-only use and any strict/adaptive value |
| PPTX structure | The workspace is `structured`; the plan decides whether pages compile its structure or use it as visual reference |

[`layouts_index.json`](./layouts_index.json) (`layout_id → { summary, canvas_format, page_count, page_types }`) is the discovery source of truth; selection reads only the index. This README defines the kind; the roster at the end is documentation of what the index holds, never a selection source or a trigger.

## Selection and identity boundary

Selection follows the parent contract: Layout choices come only from the index (no directory scan or bare-ID/style-phrase match); a supplied exact root joins the selector and is preselected only when sole; [`apply-template-workspace`](../../workflows/stages/apply-template-workspace.md) installs it before Stage 2; Quick applies a supplied exact root directly and authors the installed Master/Layout/slot contract as lockless structured Slides unless the user explicitly requests visual-only flat use.

## `design_spec.md` contract

Portable structural metadata plus rules unique to this layout; no Template Overview, application contract, or identity section — the frontmatter `summary` carries selection context.

```markdown
---
layout_id: <slug>
kind: layout
category: general | scenario | government | special
summary: <one-line structural use case>
canvas_format: ppt169
canvas_width: 1280
canvas_height: 720
canvas_viewbox: "0 0 1280 720"
replication_mode: standard | fidelity | mirror
native_structure_mode: structured
page_count: <N>
page_types: [cover, toc, chapter, content, ending]
---

# [Layout Name] — Design Specification

## IV. Signature Design Elements
## V. Page Roster
## VII. Placeholder Overrides      # omit when none
```

`replication_mode` records how the workspace was produced. `Signature Design Elements` describes only reusable structure (grids, zones, image behavior, density rhythm, text roles, alignment/wrapping/capacity, slot conventions) and introduces no palette, typeface identity, type scale, objective, or narrative sequence; `Page Roster` lists every SVG with Layout key, picker name, content shape, and slot behavior.

## Structured SVG and slot contract

Every SVG is a complete preview declaring one root Master and Layout; fixed visuals are direct atoms; a slot is a top-level `<g id>` with positive design-zone bounds and exactly one compatible carrier; zero-slot Layouts are valid; a typed `picture` / `chart` / `table` slot promises no inserted picture or native object — the generated Slide supplies content and native replacement stays an explicit export choice. Use canonical `{{PLACEHOLDER}}` names ([`template-designer.md`](../../references/template-designer.md#4-placeholder-reference-canonical-convention-overridable-per-template)) with a `placeholders:` frontmatter map for overrides. `standard` / `fidelity` author new SVGs and structure; `mirror` preserves source identities, parentage, assignments, placeholder facts, and supported visuals without synthesis; legacy contracts are never upgraded in place, and a flat directory shape alone is not a legacy signal.

## Workspace and creation

`templates/` (spec + prototypes), optional `images/` (`../images/<name>`), optional `icons/imported/`, and `exports/<layout_id>_template_preview.pptx` as review evidence. Library scope writes `skills/lisa-ppt/templates/layouts/<layout_id>/` and updates the index; project scope uses an initialized `projects/<name>/` root without registration. Enter [`create-template.md`](../../workflows/create-template.md) (dispatching to [`create-layout.md`](../../workflows/create-template/create-layout.md)), validate with `svg_quality_checker.py --template-mode`, run `template_preview_pptx.py` on request and always for multiple Masters, and in library scope register with `register_template.py <id> --kind layout`. General SVG/PPT rules stay in [`shared-standards-core.md`](../../references/shared-standards-core.md) and [`pptx-structure-interface.md`](../../references/pptx-structure-interface.md); see [`styles/`](../styles/) to combine method and direction with this structure.

## Roster

Fourteen registered layouts, all `native_structure_mode: structured`. Seven are upstream PPT Master v6.1.0 systems; seven came through byungjunjang/slide-master (PPT Master v2–v3 stock that upstream replaced in v4) and were re-authored to the structured contract in this repository — each of those carries a `README.md` at its root with provenance, migration notes, and gaps, and its `design_spec.md` frontmatter carries `summary_ko` / `summary_zh_tw` and `display_name*` beside the English `summary` the index reads. Names are English · Korean · Traditional Chinese.

| Layout | Names | One line |
|---|---|---|
| `presentation_core` | Presentation Core · 프레젠테이션 코어 · 簡報核心 | 16:9, 20 Layouts: the general vocabulary — title, content, comparison, caption, picture, hero, card, KPI, process, data, chart and table pages |
| `presentation_core_43` | Presentation Core 4:3 · 프레젠테이션 코어 4:3 · 簡報核心 4:3 | 4:3, 16 Layouts: the same vocabulary for projector, classroom, academic and meeting-room decks |
| `report_core` | Report Core · 리포트 코어 · 報告核心 | 16:9, 13 Layouts across two Masters: persistent header/footer chrome, page-number placeholders, dense analytical pages |
| `editorial_bleed` | Editorial Bleed · 에디토리얼 블리드 · 編輯出血 | 16:9, 10 Layouts: images bleed to the canvas edge with text on a scrim |
| `moments_square` | Moments Square · 모먼츠 스퀘어 · 朋友圈方形 | 1:1, 8 Layouts: horizontal and vertical division on a square canvas |
| `story_vertical` | Story Vertical · 스토리 세로형 · 限時動態直式 | 9:16, 9 Layouts: text geometry inside the top and bottom story safe zones |
| `xiaohongshu_post` | Xiaohongshu Post · 샤오홍슈 포스트 · 小紅書貼文 | 3:4, 10 Layouts: single-column image-text posts on a tall social canvas |
| `academic_defense` | Academic Defense · 학위 논문 심사 · 學位論文答辯 | 16:9, 5 Layouts: header band with accent bar, key-message strip, open content field, two-column card agenda, full-bleed chapter divider |
| `government_blue` | Government Blue · 공공기관 블루 · 政府藍 | 16:9, 5 Layouts: gradient planes, numbered title bar with a badge, ordinal-circle agenda, full-bleed dividers |
| `government_red` | Government Red · 공공기관 레드 · 政府紅 | 16:9, 5 Layouts: two-tone accent chrome, numbered title bar, agenda with statistic callouts, full-bleed dividers |
| `medical_university` | Medical University · 의과대학·병원 · 醫學大學 | 16:9, 5 Layouts: header band with accent bar, key-message strip, card agenda, full-bleed chapter plane, medical-cross decorations |
| `psychology_attachment` | Psychology Attachment · 심리 애착 · 心理依附 | 16:9, 5 Layouts: soft gradient planes, left rail, tag chips, quote block, dual-column agenda with goals, a picture-typed cover frame |
| `ai_ops` | AI Ops · AI 운영 · AI 維運 | 16:9, 6 Layouts: red/blue block chrome, numbered badges, scenario tags, left-panel agenda, and a dense architecture-overview page |
| `pixel_retro` | Pixel Retro · 픽셀 레트로 · 像素復古 | 16:9, 5 Layouts: dark plane, neon glow accents, pixel-block corners, dual rules, monospace roles, stat-strip agenda, summary closing page |
