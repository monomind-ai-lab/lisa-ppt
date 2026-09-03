---
layout_id: government_blue
kind: layout
category: government
summary: Public-sector briefings, plan presentations, work summaries, investment promotion, policy explanation — a 16:9 gradient-plane system with a top strip and left side bar, a numbered-badge agenda, a badge-and-title header over an open content field, and full-bleed dark chapter and closing pages.
summary_ko: 공공기관 브리핑, 계획 발표, 업무 보고, 투자 유치, 정책 설명 — 상단 띠와 왼쪽 세로 바, 번호 배지 목차, 배지·제목 헤더 아래 열린 콘텐츠 영역, 전면 짙은 챕터·마무리 페이지로 이루어진 16:9 그라데이션 구조.
summary_zh_tw: 公部門簡報、計畫發表、工作總結、招商推廣、政策說明——頂部色帶與左側直條、編號徽章目錄、徽章加標題的頁首配開放內容區，以及滿版深色章節與結尾頁的 16:9 漸層結構。
display_name: Government Blue
display_name_ko: 공공기관 블루
display_name_zh_tw: 政府藍
keywords: [government, briefing, gradient-plane, side-bar, badge-agenda]
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
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{PRESENTER}}", "{{ORGANIZATION}}", "{{DATE}}", "{{BRAND_LOGO}}"]
  02_toc: ["{{PAGE_TITLE}}", "{{PAGE_TITLE_EN}}", "{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_1_DESC}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_2_DESC}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_3_DESC}}", "{{TOC_ITEM_4_TITLE}}", "{{TOC_ITEM_4_DESC}}", "{{TOC_ITEM_5_TITLE}}", "{{TOC_ITEM_5_DESC}}", "{{PAGE_NUM}}"]
  03_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_SUBTITLE}}", "{{ORGANIZATION}}"]
  04_content: ["{{PAGE_TITLE}}", "{{CHAPTER_NUM}}", "{{BRAND_LOGO}}", "{{CONTENT_AREA}}", "{{PAGE_NUM}}", "{{FOOTER_NOTE}}"]
  05_ending: ["{{THANK_YOU}}", "{{THANK_YOU_EN}}", "{{CLOSING_MESSAGE}}", "{{ORGANIZATION}}", "{{CONTACT_INFO}}"]
---

# Government Blue — Design Specification

## IV. Signature Design Elements

Government Blue is a gradient-plane system for material that is reported
upward or outward: a public-sector briefing, a plan presentation, a work
summary, an investment or policy explanation. Dark full-bleed pages open and
close the deck and divide its chapters; light pages carry the agenda and the
content, each anchored by a 6 px strip along the top and a vertical bar at the
left edge. The prototype paint (a deep blue plane, a bright accent strip, pale
light-page washes) exists only to expose hierarchy and slot geometry; it is not
an identity segment. Color, typography, logo, voice, and icon treatment remain
downstream decisions.

| Element | Template-specific behavior |
|---|---|
| One Master, two planes | `government_blue_master` carries a white plane. `cover`, `chapter`, and `ending` lay a full-bleed diagonal-gradient plane over it as the first Layout atom, with soft translucent orbs (2–5 % alpha) in the corners; `toc` and `content` lay a pale near-white gradient wash instead. Every page starts with the same 6 px gradient strip across the top edge. |
| Left side bar | `cover` runs an 8 px gradient bar from y 180 to 540 with a 3 px hairline at x 16; `toc` runs the bar the full height beside a faint wedge (`0 0 → 280 0 → 200 720`) and a 520 px hairline; `chapter` and `ending` move the pair inboard (x 80 / 100) as a 6 px bar with a 3 px echo. The bar is the one motif every page repeats. |
| Cover title band | `cover` darkens a 900 × 180 band at y 260 (25 % black) with an 8 px accent at its left edge; the `title` (52 px) and `subtitle` (26 px) sit inside its 60 px inset (`60 288 820 72` / `60 372 820 44`). A 340 px rule at y 480 separates the band from a stacked presenter block: three left-aligned `object` / `object` / `date` lines (20 / 18 / 16 px) at a 40 px rhythm. A 20 px footer band with a 400 px gradient cap closes the page; the 200 × 30 logo zone above its right end is typed `object` so a Brand can place its mark. |
| Numbered-badge agenda | `toc` sets five items on a 100 px vertical rhythm (centers at y 200 … 600). Each item has a Layout-owned 32 px badge circle with its `01`–`05` ordinal (24 px), a 790 px rule from x 390 with a 5 px dot at its start, and one `object` slot (`420 … 760 64`) carrying the item title (22 px) over its description (14 px) as a two-line frame. The heading is a `title` slot (38 px) over a tracked `subtitle` eyebrow (18 px) and a two-tone 200 px rule at y 135. |
| Badge-and-title header | `content` opens with a 50 × 50 rounded badge at `60 30` carrying the chapter number as an `object` slot beside the 28 px `title` slot (`130 30 950 50`); the 120 × 26 logo zone at the top right, typed `object`, sits above a 2 px gradient underline. A dashed hairline at y 95 closes the header. |
| Open content field | `content` leaves `60 110 1160 550` as one `object` slot with no panel; the page's own composition (columns, cards, timeline, table) is Slide-local. The object carrier starts upper-left at 22 px. |
| Ghost chapter number | `chapter` centers a 180 px `object` slot (`340 150 600 226`) at 5 % fill with a 20 % outline, above a 120 px rule with a shorter echo at y 370 / 382, the centered 48 px `title` and a tracked 22 px `subtitle` at a 50 px step. Faint grid lines at thirds (y 240 / 480, x 426 / 854) sit under everything. |
| Centered closing | `ending` centers every role: a tracked 64 px `title`, a tracked 26 px `subtitle`, a split 300 px divider with a center dot at y 400, then a 28 px `object` message line, an 18 px `footer` organization line, and a 14 px `object` contact line at a 40–60 px rhythm. Three wave paths cross the lower third under the text. |
| Footer chrome | Light pages end with a 4 px rule at y 716 and a centered `slide-number` in a `540 676 200 32` frame; `content` adds a right-aligned `footer` note at 12 px. Dark pages end with a 40 px band (20 px on the cover) capped by a 400 px gradient at the left; `chapter` centers its `footer` organization line inside that band. |
| Text entry | Cover, agenda, and content slots begin at the left; centered alignment is reserved for the chapter and closing pages, the badge ordinals, and the page number. |

## V. Page Roster

| SVG | Layout key | PowerPoint picker name | Purpose |
|---|---|---|---|
| `01_cover.svg` | `cover` | Cover | Dark gradient plane with a darkened title band carrying title and subtitle, a three-line presenter block with date, a footer band, and a logo zone at the lower right |
| `02_toc.svg` | `toc` | Table of Contents | Light wash with page title and eyebrow over five badge-numbered agenda rows, each a two-line item slot beside a Layout-owned ordinal, and a centered page number |
| `03_chapter.svg` | `chapter` | Chapter | Full-bleed dark divider with a ghost chapter number, a centered title with rule, a tracked subtitle, and an organization line in the footer band |
| `04_content.svg` | `content` | Content | Light wash with a chapter-number badge, page title, logo zone, dashed header rule, open content field, centered page number, and a right-aligned footer note |
| `05_ending.svg` | `ending` | Closing | Full-bleed dark closing with a tracked thank-you title and echo subtitle above a split divider, a message line, an organization line, and a contact line over wave decoration |
