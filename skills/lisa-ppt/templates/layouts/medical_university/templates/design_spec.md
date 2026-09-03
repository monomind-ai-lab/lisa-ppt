---
layout_id: medical_university
kind: layout
category: scenario
summary: Medical academic reports, case discussions, research presentations, hospital work reports, medical education and training — a 16:9 header-band system with a key-message strip, a two-column card agenda, cross and pulse-trace accents, and a full-bleed chapter divider.
summary_ko: 의학 학술 보고, 증례 토의, 연구 발표, 병원 업무 보고, 의학 교육·연수 — 상단 띠 아래 핵심 메시지 줄, 2열 카드 목차, 십자·심전도 장식, 전면 챕터 구분 페이지로 이루어진 16:9 구조.
summary_zh_tw: 醫學學術報告、病例討論、研究簡報、醫院工作報告、醫學教育與培訓——頂部色帶配核心訊息列、雙欄卡片目錄、十字與心電圖裝飾及滿版章節分隔頁的 16:9 結構。
display_name: Medical University
display_name_ko: 의과대학·병원
display_name_zh_tw: 醫學大學
keywords: [medical, hospital, clinical, header-band, key-message]
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
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{AUTHOR}}", "{{DEPARTMENT}}", "{{ADVISOR}}", "{{INSTITUTION}}", "{{DATE}}", "{{BRAND_LOGO}}"]
  02_toc: ["{{PAGE_TITLE}}", "{{PAGE_TITLE_EN}}", "{{BRAND_LOGO}}", "{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_1_DESC}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_2_DESC}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_3_DESC}}", "{{TOC_ITEM_4_TITLE}}", "{{TOC_ITEM_4_DESC}}", "{{TOC_ITEM_5_TITLE}}", "{{TOC_ITEM_5_DESC}}", "{{TOC_ITEM_6_TITLE}}", "{{TOC_ITEM_6_DESC}}", "{{INSTITUTION}}", "{{PAGE_NUM}}"]
  03_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_DESC}}", "{{INSTITUTION}}"]
  04_content: ["{{PAGE_TITLE}}", "{{BRAND_LOGO}}", "{{KEY_MESSAGE}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}"]
  05_ending: ["{{THANK_YOU}}", "{{ENDING_SUBTITLE}}", "{{INSTITUTION}}", "{{DEPARTMENT}}", "{{CONTACT_INFO}}", "{{COPYRIGHT}}", "{{PAGE_NUM}}", "{{BRAND_LOGO}}"]
---

# Medical University — Design Specification

## IV. Signature Design Elements

Medical University is a header-band system for clinical and academic
material that is reviewed rather than sold: a case discussion, a research
presentation, a hospital work report, a teaching session. Every page reads
top-down from a header band to an open content field; the structure separates
*what this page claims* (the key-message strip) from *the evidence for it*
(the content field), and threads a small set of medical motifs — a pulse
trace in the band, cross marks, concentric rings — through the chrome. The
prototype paint (a deep header, a warm accent bar, pale blue and pale green
panels) exists only to expose hierarchy and slot geometry; it is not an
identity segment. Color, typography, logo, voice, and icon treatment remain
downstream decisions.

| Element | Template-specific behavior |
|---|---|
| One Master, four page planes | `medical_university_master` carries a white plane. `cover` and `ending` raise a 100 px header band; `toc` and `content` use a 70 px band; `chapter` overrides the plane with a full-bleed dark Layout background carrying a wedge, an edge strip, a translucent cross, and three concentric rings at the lower right. |
| Header band with accent bar and pulse trace | Every light page opens with a full-width band and a 6 px accent bar flush left — the one motif the roster repeats. On the 100 px cover and closing bands a 240 px pulse-trace path sits in the left half as a Layout atom; 70 px bands hold the page title at 26–28 px instead. The `toc` band also carries a 16 px `subtitle` echo line (`{{PAGE_TITLE_EN}}`) beside a 300 px title column, so a secondary-language heading has its own frame. |
| Logo zone | Each band reserves a right-edge `object` slot for the Brand mark: a framed 160 × 50 zone on the cover (centered carrier), an unframed 160 × 50 zone on the closing page, and a 140 × 42 zone on 70 px bands (end-anchored carrier). The Layout owns the zone; the Brand owns the mark. |
| Key-message strip | `content` places a 50 px strip under the header, with its own 6 px accent in a second tone, carrying one-line `body` text at 18 px: the claim the page makes before the evidence. Its 40 px inset matches the content field. |
| Open content field | `content` leaves `40 135 1200 515` as one `object` slot with no panel; the page's own composition (case timeline, lab-value cards, imaging with captions, treatment comparison, flowchart) is Slide-local. The object carrier starts upper-left at 22 px. |
| Card agenda | `toc` sets six 540 × 95 cards in two columns at a 120 px vertical rhythm. Rows one and two are filled panels with a 6 px left bar in alternating tones (blue row, green row); row three is a pair of dashed outlines, the same slot contract in muted paint, so a four-item agenda leaves the last row visibly optional. Ordinal indices `01`–`06` are Layout-owned atoms at 36 px; each card's `object` slot carries the item title (22 px) over its description (14 px) as one two-line frame starting at x 190 / 770, to the right of the ordinal. A translucent cross mark sits centered below the grid. |
| Ghost chapter number | `chapter` places a 280 px `object` slot behind the title at 8 % alpha, with the 52 px title and a 22 px description column starting at x 380 beside a 12 px accent bar (y 260–460), under a short 6 px rule capped by a dot. A `footer` slot at the lower right carries the institution name above a faint hairline. |
| Centered cover and closing | `cover` and `ending` center every role: 52 px title, 26 / 22 px subtitle, then a divider (440 px on the cover, 360 px on the closing page) with a center dot and end caps. The cover stacks a presenter block below the divider — an `object` author line, then department and advisor as two half-width `object` frames split by a hairline at x 640 (end-anchored left, start-anchored right), then an `object` institution line. The closing page sets a 600 × 150 contact card with a 6 px left bar holding one three-line `object` frame (institution, department, contact). |
| Footer chrome | `cover` and `ending` close with a 55 px footer band under a 3 px rule, carrying `date` on the cover and `footer` copyright on the closing page. `toc`, `content`, and `chapter` end with a hairline at y 665; `content` carries an `object` source line at the left, a centered `footer` section name, and a right-aligned `slide-number`; `toc` carries a `footer` institution line at the left and the `slide-number`, all at 12–16 px inside `676 … 32` frames. |
| Text entry | Header, key-message, content, source, and institution-footer slots begin at the left; centered alignment is reserved for the cover, the closing page, and the section name; the chapter footer and the department half of the presenter line end at the right. |

## V. Page Roster

| SVG | Layout key | PowerPoint picker name | Purpose |
|---|---|---|---|
| `01_cover.svg` | `cover` | Cover | Centered title and subtitle above a capped divider, a presenter block (author; department and advisor side by side; institution), a date in the footer band, and a framed logo zone in the header band beside the pulse trace |
| `02_toc.svg` | `toc` | Table of Contents | Header band with page title, echo subtitle, and logo zone over a two-column, six-card agenda with Layout-owned ordinals, a cross mark, and an institution / page-number footer |
| `03_chapter.svg` | `chapter` | Chapter | Full-bleed dark divider with a ghost chapter number, title under a capped rule, description, cross and ring decorations, and an institution footer |
| `04_content.svg` | `content` | Content | Header band, key-message strip, open content field, and a source / section / page-number footer |
| `05_ending.svg` | `ending` | Closing | Centered closing message and tagline above a capped divider, a barred contact card, flanking cross marks, and copyright with page number in the footer band |
