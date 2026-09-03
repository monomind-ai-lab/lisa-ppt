---
layout_id: ai_ops
kind: layout
category: scenario
summary: AI operations architecture reviews, IT system overviews, digital transformation proposals, smart infrastructure reports — a 16:9 red/blue block system with a split left block on cover and closing, warm-gray summary bands, square numbered badges indexing tag chips, dashed module panels, and a dense one-page architecture overview.
summary_ko: AI 운영 아키텍처 보고, IT 시스템 개요, 디지털 전환 제안, 스마트 인프라 보고서 — 표지와 마무리 페이지의 분할 좌측 블록, 웜 그레이 요약 띠, 태그 칩을 가리키는 정사각 번호 배지, 점선 모듈 패널, 고밀도 단일 페이지 아키텍처 개요로 이루어진 16:9 레드/블루 블록 구조.
summary_zh_tw: AI 維運架構檢討、IT 系統總覽、數位轉型提案、智慧基礎設施報告——封面與結尾頁的分割左側色塊、暖灰摘要色帶、指向標籤方塊的方形編號徽章、虛線模組面板，以及高密度單頁架構總覽所構成的 16:9 紅藍色塊結構。
display_name: AI Ops
display_name_ko: AI 운영
display_name_zh_tw: AI 維運
keywords: [ai-ops, architecture, badges, dense, red-blue]
canvas_format: ppt169
canvas_width: 1280
canvas_height: 720
canvas_viewbox: "0 0 1280 720"
source_canvas_width: 1280
source_canvas_height: 720
source_viewbox: "0 0 1280 720"
replication_mode: fidelity
native_structure_mode: structured
page_count: 6
page_types: [cover, toc, chapter, content, ending, architecture_overview]
placeholders:
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{TAG_1}}", "{{TAG_2}}", "{{TAG_3}}", "{{TAG_4}}", "{{TAG_5}}", "{{AUTHOR}}", "{{DATE}}"]
  02_toc: ["{{PAGE_TITLE}}", "{{PAGE_TITLE_EN}}", "{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_4_TITLE}}", "{{TOC_ITEM_5_TITLE}}", "{{TOC_SUMMARY}}"]
  03_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_DESC}}"]
  04_content: ["{{PAGE_TITLE}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}"]
  05_ending: ["{{THANK_YOU}}", "{{ENDING_SUBTITLE}}", "{{CONTACT_INFO}}", "{{COPYRIGHT}}", "{{TAG_1}}", "{{TAG_2}}", "{{TAG_3}}", "{{TAG_4}}"]
  06_architecture_overview: ["{{PAGE_TITLE}}", "{{KEY_MESSAGE}}", "{{TARGET}}", "{{KPI_1}}", "{{KPI_2}}", "{{KPI_3}}", "{{KPI_4}}", "{{KPI_5}}", "{{KPI_6}}", "{{TAG_1}}", "{{TAG_2}}", "{{TAG_3}}", "{{TAG_4}}", "{{BLOCK_SUMMARY}}", "{{BLOCK_1}}", "{{BLOCK_2}}", "{{BLOCK_3}}", "{{SIDE_CONTENT}}", "{{CARD_1}}", "{{CARD_2}}", "{{CARD_3}}"]
---

# AI Ops — Design Specification

## IV. Signature Design Elements

AI Ops is a red/blue block system for dense operations and architecture
reporting: a thin strip along the top edge, a two-color block split at
mid-height down the left edge of the cover and the closing page, light bands
that hold a page's one-line summary, square numbered badges that index the
chip beside them, and dashed panels that zone a page into modules. The
prototype paint (a deep red, a mid blue, a lighter blue for small chips,
light-gray and pale warm panels) exists only to expose hierarchy and slot
geometry; it is not an identity segment. Color, typography, logo, voice, and
icon treatment remain downstream decisions.

| Element | Template-specific behavior |
|---|---|
| One Master, six page planes | `ai_ops_master` carries a white plane; every page keeps it and adds its own Layout chrome. `cover`, `toc`, `chapter`, and `ending` open with an 8 px top strip and close with a 10 px accent over a 30 px band at y 680–720; `content` uses a 4 px strip and a 40 px footer band; `architecture_overview` has no bottom chrome so its base row can reach y 690. |
| Split left block | `cover` and `ending` carry a 60 px block down the left edge, split at y 360 into an upper and a lower half in the two accent paints. `toc` widens it into a 320 px panel that carries the agenda `title` (56 px, centered) and a `subtitle` eyebrow (20 px) beneath it. `chapter` reduces it to 120 px side blocks with an 8 px edge bar on each side. |
| Badge + chip rows | Square badges (40 × 40 on the cover and agenda, 30 × 30 on the closing page and the overview base row, 30 × 25 on the overview side panel) carry Layout-owned ordinals `1`–`5` at 22 / 16 / 18 px. Each badge indexes a chip rect 10 px to its right whose text is an `object` slot (`{{TAG_n}}` on the cover and closing page, `{{TOC_ITEM_n_TITLE}}` on the agenda); the chips sit on a 200 px horizontal pitch (cover, closing) or an 80 px vertical pitch (agenda). Chip rects are Layout atoms; the chip label is centered on the rect. |
| Summary bands and warm panels | A 60 px light band directly under the title (cover at y 280, overview at y 80) carries one centered line — `subtitle` on the cover, `body` `{{KEY_MESSAGE}}` on the overview. Warm panels with a 2 px border hold the agenda summary (420 × 400, one centered `object`), the closing message (720 × 320, four centered lines), and the overview side column (160 × 300, one open `object` field). |
| Dashed module panels | `architecture_overview` zones the orchestration row with a 940 × 150 dashed outer panel whose 30 px header band is a centered `object` (`{{BLOCK_SUMMARY}}`), and three 280 × 90 dashed sub-panels on a 300 px pitch, each an open `object` field (`{{BLOCK_1..3}}`) whose carrier starts upper-left at 14 px. A single ordinal badge sits outside the panel at the left edge. |
| Architecture overview ladder | The signature page reads top-down: title with a 10 × 40 accent bar (36 px), summary band, a 680 × 40 rounded target bar (`object`, centered 20 px), six 140 × 35 KPI chips on a 150 px pitch (one `object` each, centered 14 px), four 220 × 40 tag chips on a 240 px pitch (one `object` each, centered 16 px), the orchestration row, the side panel, and three 300 × 110 base boxes on a 320 / 330 px pitch, each with a badge on its upper-left corner, a dashed title rule at y 605, and one `object` slot (`{{CARD_n}}`) whose carrier is a centered 14 px title line above the rule. A pale triangle behind the KPI and tag rows is a Layout atom. |
| Chapter divider | `chapter` centers an 80 × 80 badge whose number is an `object` slot at 48 px, a 48 px `title` in a `140 372 1000 72` frame, a paired thick / thin rule at y 450 / 458, and a 20 px `object` description line. |
| Content page | `content` opens with an 8 × 40 accent bar beside a 32 px `title` and a hairline at y 80, leaves `50 95 1180 560` as one `object` field with no panel (carrier upper-left at 22 px), and ends with a 40 px footer band carrying a `footer` section name at the left, a centered `object` source line, and a 30 × 24 square badge holding the `slide-number`. |
| Cover and closing | `cover` centers a 56 px `title`, the `subtitle` band, the five-chip row, a 1040 px dashed divider at y 480, then an `object` author line and a `date` line. `ending` centers a 64 px `title`, a tracked 22 px `subtitle`, a 320 px hairline at y 400, an `object` contact line and a `footer` copyright line inside the warm panel, with a four-chip echo row at y 580. |
| Text entry | The content field, the section name, and the open overview fields (sub-panels, side panel) begin at the left; every other role — cover, agenda, chapter, closing, chip labels, KPI chips, target bar, card titles — is centered on its zone. |

## V. Page Roster

| SVG | Layout key | PowerPoint picker name | Purpose |
|---|---|---|---|
| `01_cover.svg` | `cover` | Cover | Split left block, centered title over a subtitle band, a five-badge tag row above a dashed divider, then author and date lines |
| `02_toc.svg` | `toc` | Table of Contents | Left panel with the agenda title and eyebrow, five badge-indexed item chips, and a warm summary panel at the right |
| `03_chapter.svg` | `chapter` | Chapter | Side blocks with edge bars, a centered badge holding the chapter number, title with paired rules, and a description line |
| `04_content.svg` | `content` | Content | Accent-bar title over an open content field, with a section / source / badge page-number footer band |
| `05_ending.svg` | `ending` | Closing | Split left block, a warm panel with closing message, tagline, hairline, contact and copyright lines, and a four-badge tag echo row |
| `06_architecture_overview.svg` | `architecture_overview` | Architecture Overview | Dense one-page ladder: accent-bar title, summary band, target bar, six KPI chips, four tag chips, a dashed orchestration panel with three sub-panels, a side panel, and three base boxes |
