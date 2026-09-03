---
layout_id: government_red
kind: layout
category: government
summary: Government and public-sector briefings, policy explanations, work reports, project introductions, investment promotion — a 16:9 two-tone system with a top gradient bar, a badge header, a side-bar agenda beside a statistics panel, and full-bleed dark cover, chapter, and closing planes.
summary_ko: 정부·공공기관 브리핑, 정책 해설, 업무 보고, 사업 소개, 투자 유치 — 상단 그라데이션 바, 배지 헤더, 통계 패널 옆의 세로 바 목차, 전면 다크 표지·챕터·마무리 페이지로 이루어진 16:9 투톤 구조.
summary_zh_tw: 政府與公部門簡報、政策說明、工作報告、專案介紹、招商引資——頂部漸層條、標章頁首、統計面板旁的側邊直條目錄，以及滿版深色封面、章節與結尾頁的 16:9 雙色調結構。
display_name: Government Red
display_name_ko: 공공기관 레드
display_name_zh_tw: 政府紅
keywords: [government, briefing, policy, badge-header, side-bar]
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
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{AUTHOR}}", "{{AUTHOR_EN}}", "{{DATE}}", "{{ORGANIZATION}}"]
  02_toc: ["{{PAGE_TITLE}}", "{{PAGE_BADGE}}", "{{PAGE_TITLE_EN}}", "{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_1_DESC}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_2_DESC}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_3_DESC}}", "{{TOC_ITEM_4_TITLE}}", "{{TOC_ITEM_4_DESC}}", "{{TOC_ITEM_5_TITLE}}", "{{TOC_ITEM_5_DESC}}", "{{STAT_NUMBER_1}}", "{{STAT_LABEL_1}}", "{{STAT_NUMBER_2}}", "{{STAT_LABEL_2}}", "{{PAGE_NUM}}"]
  03_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_SUBTITLE}}", "{{ORGANIZATION}}"]
  04_content: ["{{PAGE_TITLE}}", "{{CHAPTER_NUM}}", "{{BRAND_LOGO}}", "{{CONTENT_AREA}}", "{{PAGE_NUM}}", "{{FOOTER_NOTE}}"]
  05_ending: ["{{THANK_YOU}}", "{{THANK_YOU_EN}}", "{{AUTHOR}}", "{{AUTHOR_EN}}", "{{CONTACT_INFO}}", "{{ENDING_SUBTITLE}}"]
---

# Government Red — Design Specification

## IV. Signature Design Elements

Government Red is a two-plane system for material that is reported upward or
outward: a briefing, a policy explanation, a work report, a promotion deck.
Three pages (cover, chapter, closing) sit on a full-bleed dark plane with a
faint orb-and-grid texture; two pages (agenda, content) sit on the light
plane under a badge header. Every page opens with the same 6 px two-tone bar
across the top and closes with a band or rule in the second tone. The
prototype paint (a deep-blue diagonal plane, a dark-red accent, a gold
hairline, a pale statistics panel) exists only to expose hierarchy and slot
geometry; it is not an identity segment. Color, typography, logo, voice, and
icon treatment remain downstream decisions.

| Element | Template-specific behavior |
|---|---|
| One Master, two planes | `government_red_master` carries a white plane. `toc` and `content` build directly on it; `cover`, `chapter`, and `ending` lay a full-canvas gradient rect over it as the first Layout atom, then three large low-alpha orbs and a 2 × 2 (2 × 3 on the closing page) hairline grid as texture. |
| Top bar and bottom band | Every page opens with a 6 px full-width two-tone gradient bar at y 0 — the one motif the whole roster repeats. Light pages close with a 4 px rule at y 716; dark pages close with a 30 px (cover) or 40 px (chapter, closing) translucent band that carries one centered 14 px line: an `object` organisation line on the cover, a `footer` slot on the chapter and closing pages. |
| Badge header | `toc` and `content` open with a 50 × 50 badge at `60 30`, the page title at 28 px from x 130 inside a `130 38 950` frame, and a right-edge zone at x 1107–1220. The badge is a Layout atom; what sits inside it is an `object` slot (`{{PAGE_BADGE}}` on the agenda, `{{CHAPTER_NUM}}` on content pages). The agenda adds a 14 px `subtitle` eyebrow under the title; the content page adds a 113 × 30 `object` logo zone over a 2 px hairline. |
| Side-bar agenda | `toc` runs a 4 px bar with a 2 px accent echo at x 280–290 from y 140 to 620 and stacks five items on a 90 px rhythm from y 160. Each item pairs a 40 × 40 Layout badge with a Layout-owned ordinal `01`–`05` at 20 px and one `object` slot (`370 … 490 60`) whose carrier holds the item title (22 px) over its description (14 px) as a two-line frame. |
| Statistics panel | The agenda's right column is a 320 × 440 panel at `880 160` with a 6 px left bar and a hairline at y 360 splitting it into two cells. Each cell is one `object` slot (`900 … 280 150`) whose carrier stacks a display number (72 px above the rule, 48 px below, both at low alpha) over a 16 px label. |
| Open content field | `content` leaves `60 100 1160 560` as one `object` slot with no panel; the page's own composition (columns, cards, table, timeline) is Slide-local. The carrier starts upper-left at 22 px. |
| Ghost chapter number | `chapter` centers a 160 px `object` number at 6 % alpha inside `320 150 640 200`, a 100 × 6 rule at y 360, the 48 px title at y 430, and a tracked 22 px `subtitle` echo line at y 480; a 6 px side bar at x 100 marks the block's left edge. |
| Centered cover and closing | `cover` and `ending` center every role on x 640: 52 / 64 px title, 28 / 26 px subtitle echo, a 400 / 300 px gold divider, then a stacked presenter block of `object` lines (author, author echo, and on the closing page a contact line). The cover places a `date` slot at y 620; both pages mark the block with a 6 px side bar at x 60 / 100. |
| Footer chrome | Light pages carry a centered `slide-number` in a `540 680 200 24` frame; the content page adds a right-aligned 12 px `footer` note ending at x 1220. |
| Text entry | Header titles, the agenda items, and the content field begin at the left; centered alignment is reserved for the dark planes, the badge glyphs, the statistics cells, and the page number. |

## V. Page Roster

| SVG | Layout key | PowerPoint picker name | Purpose |
|---|---|---|---|
| `01_cover.svg` | `cover` | Cover | Dark plane with centered title and subtitle above a divider, a two-line presenter block, a date, and an organisation line in the footer band |
| `02_toc.svg` | `toc` | Table of Contents | Badge header with title and eyebrow, a five-item side-bar agenda with Layout-owned ordinals, a two-cell statistics panel, and a page number |
| `03_chapter.svg` | `chapter` | Chapter | Dark plane with a ghost chapter number, rule, centered title and tracked subtitle echo, and a footer band line |
| `04_content.svg` | `content` | Content | Badge header with chapter number, page title and logo zone, an open content field, a page number, and a footer note |
| `05_ending.svg` | `ending` | Closing | Dark plane with centered closing message and echo line above a divider, a presenter block with contact line, and a footer band line |
