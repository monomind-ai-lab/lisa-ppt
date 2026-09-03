---
layout_id: pixel_retro
kind: layout
category: special
summary: Tech talks, programming tutorials, game introductions, geek-style showcases — a 16:9 dark-plane system with neon dual rules and pixel-block corners, a framed chapter number, a tagged card agenda beside a stat panel, an open content field, and a three-card closing summary.
summary_ko: 기술 발표, 프로그래밍 튜토리얼, 게임 소개, 긱 스타일 쇼케이스 — 네온 이중 괘선과 픽셀 블록 모서리, 프레임에 담긴 챕터 번호, 통계 패널 옆의 태그 카드 목차, 열린 콘텐츠 영역, 3장 카드 마무리 요약으로 이루어진 16:9 다크 플레인 구조.
summary_zh_tw: 技術分享、程式教學、遊戲介紹、極客風格展示——霓虹雙線與像素方塊邊角、加框章節編號、統計面板旁的標籤卡片目錄、開放內容區與三張卡片結尾摘要所構成的 16:9 深色版面結構。
display_name: Pixel Retro
display_name_ko: 픽셀 레트로
display_name_zh_tw: 像素復古
keywords: [pixel, retro, neon, dark-plane, arcade]
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
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{TAG_1}}", "{{TAG_2}}", "{{TAG_3}}", "{{TAG_4}}", "{{CTA_TEXT}}", "{{AUTHOR}}", "{{VERSION}}", "{{PAGE_NUM}}", "{{TOTAL_PAGES}}"]
  02_toc: ["{{PAGE_TITLE}}", "{{PAGE_TITLE_EN}}", "{{TAG_1}}", "{{TAG_2}}", "{{TAG_3}}", "{{TAG_4}}", "{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_4_TITLE}}", "{{KEY_MESSAGE}}", "{{STAT_1}}", "{{STAT_1_LABEL}}", "{{STAT_2}}", "{{STAT_2_LABEL}}", "{{STAT_3}}", "{{STAT_3_LABEL}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}", "{{TOTAL_PAGES}}"]
  03_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_TITLE_EN}}", "{{PAGE_NUM}}", "{{TOTAL_PAGES}}"]
  04_content: ["{{PAGE_TITLE}}", "{{PAGE_TITLE_EN}}", "{{CONTENT_AREA}}", "{{PAGE_SUBTITLE}}", "{{PAGE_NUM}}", "{{TOTAL_PAGES}}"]
  05_ending: ["{{THANK_YOU}}", "{{END_SUBTITLE}}", "{{SUMMARY_1_TITLE}}", "{{SUMMARY_1_LINE_1}}", "{{SUMMARY_1_LINE_2}}", "{{SUMMARY_1_LINE_3}}", "{{SUMMARY_1_STAT}}", "{{SUMMARY_2_TITLE}}", "{{FEATURE_1}}", "{{FEATURE_2}}", "{{FEATURE_3}}", "{{FEATURE_4}}", "{{SUMMARY_3_TITLE}}", "{{COMPARE_A}}", "{{ROW_1_A}}", "{{ROW_2_A}}", "{{ROW_3_A}}", "{{COMPARE_B}}", "{{ROW_1_B}}", "{{ROW_2_B}}", "{{ROW_3_B}}", "{{CTA_TEXT}}", "{{CONTACT_INFO}}", "{{PAGE_NUM}}", "{{TOTAL_PAGES}}"]
---

# Pixel Retro — Design Specification

## IV. Signature Design Elements

Pixel Retro is a dark-plane system for material that is demonstrated rather
than reported: a tech talk, a programming tutorial, a game or product
walkthrough. Every page sits on one dark plane framed by a neon dual rule at
the top and bottom, with pixel-block clusters in the corners and faint
horizontal scanlines behind the content; structure comes from bordered cards,
tab chips, and framed counters rather than from bands. The prototype paint (a
near-black plane, a neon primary with three accents, glow on display text)
exists only to expose hierarchy and slot geometry; it is not an identity
segment. Color, typography, logo, voice, and icon treatment remain downstream
decisions.

| Element | Template-specific behavior |
|---|---|
| One Master, one plane | `pixel_retro_master` carries a dark plane that no page overrides. Every page repeats the neon dual rule top and bottom (an 8 + 4 px pair, inset 40 px on the cover and full-bleed on the chapter page; a 4 + 2 px full-bleed pair on the agenda and closing page; a single 4 px hairline on content pages) and a faint scanline grid. |
| Pixel-block corners | Three-step block clusters sit at the corners as Layout atoms, fading away from the corner: 16 px blocks at the cover's top corners, 12 px blocks at the bottom corners of the cover and closing page, and two 20 px six-block matrices on the chapter page. |
| Console mark | The cover centers a 200 × 80 console shell with two keys and a glowing lamp above the title as a fixed Layout atom; it is not a logo zone. |
| Chip row | The cover sets four 140 × 40 outlined chips at a 160 px pitch under a 400 px divider; each chip is one `object` slot (`{{TAG_1}}`–`{{TAG_4}}`, 16 px centered) with the chip rect as an atom. A centered `object` prompt line (24 px) and a presenter `object` line (18 px) follow below. |
| Tagged card agenda | `toc` stacks four 560 × 80 bordered cards at a 100 px vertical rhythm on the left. Each card carries a 100 × 24 tab chip at its top-left (one `object` slot per chip, 12 px centered), a 40 × 40 ordinal block with a Layout-owned `01`–`04` at 24 px, and the item title as an `object` slot starting at x 140 (20 px). The fourth card is the same slot contract in muted paint. |
| Stat panel | Beside the agenda, `toc` reserves a 540 × 380 dashed panel: a centered `body` message line (20 px), a 460 × 30 progress track, three 140 × 80 stat tiles at a 160 px pitch (each one `object` slot: a 32 px number over a 14 px label as tspans), and a fixed start button. |
| Framed chapter number | `chapter` places the number in a 200 × 200 framed box at x 150 with eight pixel corner brackets (one `object` slot, 96 px centered, glow), beside a `CHAPTER` tag, the 48 px title, a 24 px echo `subtitle`, and a 400 px rule; two thin spines run down the left edge and a five-step progress track with Layout-owned step ordinals runs across the bottom. |
| Open content field | `content` leaves `60 140 1160 500` as one `object` slot with no panel; the page's own composition (cards, progress bars, tables, timelines) is Slide-local. The object carrier starts upper-left at 22 px. |
| Three-card closing summary | `ending` sets three 380 × 280 bordered cards at a 400 px pitch, each with a 60 × 60 ordinal block (Layout-owned `1`–`3`) and a 22 px title at x + 80. Card 1 carries a three-line `object` frame (18 px lines at a 35 px pitch) above a 320 × 25 pixel bar atom and a 12 px `object` stat line under the bar; card 2 adds a four-row feature list (one `object` slot, 16 px tspans at a 42 px pitch over cell atoms); card 3 adds a two-column comparison (one `object` slot per 155 px column: a 16 px header over three 14 px rows, cells as atoms). |
| Call-to-action card | Under the cards, a 1160 × 120 outlined card with a 50 px highlight band carries a centered `object` line (24 px, glow) and a centered `footer` contact line (18 px) above two fixed 180 × 25 buttons. |
| Footer chrome | Every page ends with a left `slide-number` carrying `{{PAGE_NUM}} / {{TOTAL_PAGES}}` and a right-aligned echo at 14 px inside `… 674 … 22` frames (`… 646 … 20` on the cover): a `{{VERSION}}` object on the cover, a `footer` section name on the agenda, a `{{PAGE_SUBTITLE}}` object on content pages, and fixed `LOADING...` / `THE END` labels on the chapter and closing pages. |
| Text entry | Page titles, agenda items, the content field, and the summary cards begin at the left; centered alignment is reserved for the cover, chips, stat tiles, the comparison columns, and the closing page's title and call-to-action. |

## V. Page Roster

| SVG | Layout key | PowerPoint picker name | Purpose |
|---|---|---|---|
| `01_cover.svg` | `cover` | Cover | Console mark over a centered title and subtitle, a divider, four chip slots, a prompt line, a presenter line, and a version / page-number footer between pixel-block corners |
| `02_toc.svg` | `toc` | Table of Contents | Page title with echo subtitle over four tagged agenda cards with Layout-owned ordinals, a dashed stat panel with a message line, three stat tiles and a start button, and a section / page-number footer |
| `03_chapter.svg` | `chapter` | Chapter | Framed glowing chapter number beside a `CHAPTER` tag, title, echo subtitle and rule, pixel matrices, a five-step progress track, and a page-number footer |
| `04_content.svg` | `content` | Content | Page title with echo subtitle and short rule, an open content field, and a page-number / page-subtitle footer |
| `05_ending.svg` | `ending` | Closing | Centered closing title and subtitle over three summary cards (lines and bar, feature list, two-column comparison), a call-to-action card with contact line and fixed buttons, and a page-number footer |
