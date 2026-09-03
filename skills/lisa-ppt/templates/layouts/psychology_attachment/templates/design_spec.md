---
layout_id: psychology_attachment
kind: layout
category: scenario
summary: Psychotherapy training, counseling case analysis, academic lectures, professional sharing — a 16:9 system pairing full-bleed soft-gradient planes (cover, chapter, closing) with a left-rail light plane (agenda, content), a quote block and tag-chip row on the cover and chapter pages, and a dual-column agenda with a learning-goals panel.
summary_ko: 심리치료 교육, 상담 사례 분석, 학술 강의, 전문가 공유 — 전면 소프트 그라디언트 면(표지·챕터·마무리)과 왼쪽 레일의 밝은 면(목차·본문)을 짝지우고, 표지와 챕터 페이지에는 인용 블록과 태그 칩 줄을, 목차에는 학습 목표 패널을 갖춘 2열 구성을 두는 16:9 구조.
summary_zh_tw: 心理治療培訓、諮商個案分析、學術講座、專業分享——以滿版柔和漸層底面（封面、章節、結尾）搭配左側直條的淺色頁面（目錄、內文），封面與章節頁設有引言區塊與標籤膠囊列，目錄則為附學習目標面板的雙欄結構之 16:9 版式。
display_name: Psychology Attachment
display_name_ko: 심리 애착
display_name_zh_tw: 心理依附
keywords: [psychology, counseling, gradient, quote, dual-column]
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
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{TITLE_EN}}", "{{QUOTE}}", "{{QUOTE_AUTHOR}}", "{{TAG_1}}", "{{TAG_2}}", "{{TAG_3}}", "{{TAG_4}}", "{{PAGE_NUM}}"]
  02_toc: ["{{PAGE_TITLE}}", "{{PAGE_TITLE_EN}}", "{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_1_DESC}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_2_DESC}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_3_DESC}}", "{{TOC_ITEM_4_TITLE}}", "{{TOC_ITEM_4_DESC}}", "{{TOC_ITEM_5_TITLE}}", "{{TOC_ITEM_5_DESC}}", "{{RIGHT_TITLE}}", "{{GOAL_1}}", "{{GOAL_1_DESC}}", "{{GOAL_2}}", "{{GOAL_2_DESC}}", "{{GOAL_3}}", "{{GOAL_3_DESC}}", "{{GOAL_4}}", "{{GOAL_4_DESC}}", "{{PAGE_NUM}}"]
  03_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_EN}}", "{{QUOTE}}", "{{QUOTE_AUTHOR}}", "{{TAG_1}}", "{{TAG_2}}", "{{TAG_3}}", "{{TAG_4}}", "{{PAGE_NUM}}"]
  04_content: ["{{PAGE_TITLE}}", "{{TITLE_EN}}", "{{CONTENT_AREA}}", "{{PAGE_NUM}}"]
  05_ending: ["{{THANK_YOU}}", "{{ENDING_SUBTITLE}}", "{{THANK_YOU_EN}}", "{{CLOSING_MESSAGE}}", "{{CONTACT_INFO}}", "{{CONTACT_LINE_2}}", "{{COPYRIGHT}}"]
---

# Psychology Attachment — Design Specification

## IV. Signature Design Elements

Psychology Attachment is a two-plane system for material that is taught and
reflected on rather than pitched: a psychotherapy training module, a
counseling case analysis, an academic lecture. The framing pages (cover,
chapter, closing) are full-bleed soft-gradient planes that center every role
and frame it with a quote block; the working pages (agenda, content) are a
light plane with a narrow left rail and a left-aligned title stack. The
prototype paint (a blue-to-teal gradient, a warm rule, a muted-white quote
card, translucent chips) exists only to expose hierarchy and slot geometry; it
is not an identity segment. Color, typography, logo, voice, and icon treatment
remain downstream decisions.

| Element | Template-specific behavior |
|---|---|
| One Master, two page planes | `psychology_attachment_master` carries a light plane. `cover`, `chapter`, and `ending` lay a full-canvas gradient rect over it as the first Layout atom (a gradient is never a background); `toc` and `content` keep the light plane and add an 8 px rail flush left. |
| Gradient framing pages | `cover` and `chapter` share one decorative field: three concentric rings anchored upper right (r 200 / 150 / 100 at 1100, 150), two rings lower left (r 120 / 80 at 180, 600), and two diagonal hairline pairs in the lower-right and upper-left corners. `ending` replaces the rings with a radial network — a center node, fourteen satellite nodes, fourteen spokes, six outer links — all Layout atoms behind the text. |
| Centered title stack with a warm rule | Framing pages stack, centered on x 640: the page title (52 px on the cover, 48 px on the chapter page, 56 px on the closing page), a 28 px secondary line typed `object`, and an 18–24 px secondary-language echo line typed `subtitle`, closed by a short rounded rule (200 × 3 px on cover and chapter, 300 × 4 px on the closing page). |
| Quote block | `cover` and `chapter` place an 800 × 100 translucent card with a 4 px accent bar on its left edge. Its interior (`264 … 752 72`) is one two-line `object` slot: an 18 px italic quote line over a 14 px attribution line, starting at x 270. |
| Tag-chip row | Below the quote block, four rounded chips (80–120 × 28 px, rx 14) sit in one row; each chip rect is a Layout atom and each chip label is its own `object` slot with the chip rect as its bounds, so a deck can fill one to four keywords without moving chrome. |
| Ghost chapter number and badge | `chapter` carries the chapter number twice: a 120 px ghost `object` slot at 15 % alpha centered above the title, and a 160 × 40 capsule badge whose label is a second `object` slot with the same marker. |
| Cover picture frame | `cover` reserves one full-canvas `picture` slot painted above the gradient plane and the ring field at 25 % alpha, so a placed photograph reads as a wash beneath the centered text rather than replacing the plane. |
| Left-rail working pages | `toc` and `content` open with a 32 / 28 px left-aligned title at x 60, a 16 px `subtitle` echo line beneath it, and a 2 px rule (340 px on the agenda, 440 px on the content page) under the stack. |
| Dual-column agenda | `toc` splits at a dashed vertical divider at x 620. The left column lists five items on an 80 px rhythm: a 50 × 50 rounded badge (rx 8) with a Layout-owned Roman ordinal, then one two-line `object` slot (20 px title over 14 px description) starting at x 130. The right column carries an `object` heading slot at y 150 over a 520 × 420 panel (rx 12) holding four learning goals on a 70 px rhythm, each an 8 px dot with a Layout-owned index and one two-line `object` slot (17 px goal over 14 px description) starting at x 740. |
| Open content field | `content` leaves `60 140 1180 490` as one `object` slot with no panel; the page's own composition (three columns, a left–right split, a stacked hierarchy, a quadrant) is Slide-local. The object carrier starts upper-left at 22 px. |
| Closing contact card | `ending` places a 32 px `object` closing line under the rule and a 400 × 100 translucent card whose interior (`460 536 360 64`) is one two-line centered `object` slot; a 12 px `footer` copyright line sits centered at y 680. |
| Page number | `cover`, `toc`, `chapter`, and `content` carry a right-aligned 14 px `slide-number` slot ending at x 1220 inside a `1100 … 124 24` frame; the closing page has none. |
| Text entry | Working-page titles, echo lines, the content field, agenda items, and goal lines begin at the left; every framing-page role and the chip labels are centered. |

## V. Page Roster

| SVG | Layout key | PowerPoint picker name | Purpose |
|---|---|---|---|
| `01_cover.svg` | `cover` | Cover | Gradient plane with ring field and a full-canvas picture wash; centered title, secondary line, and echo line over a rule; quote block, four tag chips, and a page number |
| `02_toc.svg` | `toc` | Table of Contents | Left-rail light plane; title and echo line over a rule; five badge-indexed agenda items left of a dashed divider, a headed learning-goals panel with four indexed goals on the right, and a page number |
| `03_chapter.svg` | `chapter` | Chapter | Gradient plane with ring field; ghost chapter number and capsule badge above the centered title, echo line, and rule; quote block, four tag chips, and a page number |
| `04_content.svg` | `content` | Content | Left-rail light plane; title and echo line over a rule; open content field and a page number |
| `05_ending.svg` | `ending` | Closing | Gradient plane with a radial network; centered closing title, secondary line, echo line, and rule; a closing message, a two-line contact card, and a copyright footer |
