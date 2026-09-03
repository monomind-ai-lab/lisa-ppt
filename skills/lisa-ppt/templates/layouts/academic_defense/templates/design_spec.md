---
layout_id: academic_defense
kind: layout
category: scenario
summary: Thesis defense, academic presentations, research progress reports, grant applications — a 16:9 header-band system with a key-message strip, a two-column card agenda, and a full-bleed chapter divider.
summary_ko: 학위 논문 심사, 학술 발표, 연구 진행 보고, 연구비 신청 — 상단 띠 아래 핵심 메시지 줄, 2열 카드 목차, 전면 챕터 구분 페이지로 이루어진 16:9 구조.
summary_zh_tw: 學位論文答辯、學術簡報、研究進度報告、研究經費申請——頂部色帶配核心訊息列、雙欄卡片目錄與滿版章節分隔頁的 16:9 結構。
display_name: Academic Defense
display_name_ko: 학위 논문 심사
display_name_zh_tw: 學位論文答辯
keywords: [academic, defense, research, header-band, key-message]
canvas_format: ppt169
canvas_width: 1280
canvas_height: 720
canvas_viewbox: "0 0 1280 720"
source_canvas_width: 1280
source_canvas_height: 720
source_viewbox: "0 0 1280 720"
replication_mode: fidelity
native_structure_mode: structured
page_count: 5
page_types: [cover, toc, chapter, content, ending]
placeholders:
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{AUTHOR}}", "{{ADVISOR}}", "{{INSTITUTION}}", "{{DATE}}", "{{BRAND_LOGO}}"]
  02_toc: ["{{PAGE_TITLE}}", "{{BRAND_LOGO}}", "{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_1_DESC}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_2_DESC}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_3_DESC}}", "{{TOC_ITEM_4_TITLE}}", "{{TOC_ITEM_4_DESC}}", "{{TOC_ITEM_5_TITLE}}", "{{TOC_ITEM_5_DESC}}", "{{TOC_ITEM_6_TITLE}}", "{{TOC_ITEM_6_DESC}}", "{{PAGE_NUM}}"]
  03_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_DESC}}", "{{FOOTER_NOTE}}"]
  04_content: ["{{PAGE_TITLE}}", "{{BRAND_LOGO}}", "{{KEY_MESSAGE}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}"]
  05_ending: ["{{THANK_YOU}}", "{{ENDING_SUBTITLE}}", "{{CONTACT_INFO}}", "{{EMAIL}}", "{{INSTITUTION}}", "{{COPYRIGHT}}", "{{PAGE_NUM}}", "{{BRAND_LOGO}}"]
---

# Academic Defense — Design Specification

## IV. Signature Design Elements

Academic Defense is a header-band system for material that is examined rather
than pitched: a thesis defense, a research progress report, a grant
application. Every page reads top-down from a dark header band to an open
content field; the structure separates *what this page claims* (the
key-message strip) from *the evidence for it* (the content field). The
prototype paint (a dark header, a warm-red accent bar, pale panels) exists
only to expose hierarchy and slot geometry; it is not an identity segment.
Color, typography, logo, voice, and icon treatment remain downstream
decisions.

| Element | Template-specific behavior |
|---|---|
| One Master, four page planes | `academic_defense_master` carries a white plane. `cover` and `ending` raise a 100 px header band; `toc` and `content` use a 70 px band; `chapter` overrides the plane with a full-bleed dark Layout background carrying a wedge and an edge strip. |
| Header band with accent bar | Every light page opens with a full-width band and a 6 px accent bar flush left — the one motif the roster repeats. The band holds the page title (28 px on 70 px bands) and a reserved 140 × 30 (140 × 50 on covers) logo zone at the right edge, typed `object` so a Brand can place its mark without the Layout owning it. |
| Key-message strip | `content` places a 50 px strip under the header, with its own 6 px accent, carrying one-line `body` text at 18 px: the claim the page makes before the evidence. Its 40 px inset matches the content field. |
| Open content field | `content` leaves `40 135 1200 515` as one `object` slot with no panel; the page's own composition (columns, cards, timeline, table) is Slide-local. The object carrier starts upper-left at 22 px. |
| Card agenda | `toc` sets six 540 × 90 cards in two columns at a 115 px vertical rhythm. Cards 1–4 are filled panels with a 6 px left bar; cards 5–6 are dashed outlines, the same slot contract in muted paint, so a four-item agenda leaves the last row visibly optional. Ordinal indices `01`–`06` are Layout-owned atoms at 36 px; each card's `object` slot carries the item title (24 px) over its description (14 px) as one two-line frame starting at x 185. |
| Ghost chapter number | `chapter` places a 280 px `object` slot behind the title at 8 % alpha, with the 56 px title and a 24 px description column starting at x 380 beside a 12 px accent bar and a short 6 px rule above the title. A `footer` slot at the lower right echoes the deck title. |
| Centered cover and closing | `cover` and `ending` center every role: 56 px title, 28 / 24 px subtitle, a 440 px divider with a center dot, then a stacked presenter block (three `object` lines: author, advisor, institution) on the cover and a 560 × 130 contact card (one three-line `object` frame) on the closing page. A 55 px footer band carries `date` on the cover and `footer` copyright on the closing page. |
| Footer chrome | Light pages end with a hairline at y 665; `content` carries a `object` source line at the left, a centered `footer` section name, and a right-aligned `slide-number`, all at 12–14 px inside `676 … 32` frames. |
| Text entry | Header, key-message, content, and source slots begin at the left; centered alignment is reserved for the cover, the closing page, and the section name. |

## V. Page Roster

| SVG | Layout key | PowerPoint picker name | Purpose |
|---|---|---|---|
| `01_cover.svg` | `cover` | Cover | Centered title and subtitle above a divider, a three-line presenter block, a date in the footer band, and a logo zone in the header band |
| `02_toc.svg` | `toc` | Table of Contents | Header band with page title and logo zone over a two-column, six-card agenda with Layout-owned ordinals and a page number |
| `03_chapter.svg` | `chapter` | Chapter | Full-bleed dark divider with a ghost chapter number, title with rule, description, and a footer echo |
| `04_content.svg` | `content` | Content | Header band, key-message strip, open content field, and a source / section / page-number footer |
| `05_ending.svg` | `ending` | Closing | Centered closing message and tagline above a divider, a contact card, and copyright with page number in the footer band |
