---
style_id: paper-brief
kind: style
summary: Chaptered briefing method for a document read at desk distance and forwarded — inverted chapter pages as seams, one conclusion per page, bar charts and decision boxes that say what was decided and why.
keywords: [briefing, chapters, decision, read-first, paper]
---

# Paper Brief — Style Specification

> Method and design defaults only. No project communication contract, brand identity, page structure, or SVG prototypes.

## I. Style Overview

| Property | Value |
|---|---|
| Style Name | Paper Brief |
| Best Fit | A briefing that will be read rather than presented, then forwarded or printed: a planning input, a review, a recommendation for a committee, a report someone reads at a desk |
| Reusable Intent | Pace a long argument in chapters with visible seams, give every page one conclusion and the figures behind it, and close each chapter with a decision box that records what was decided and why — leaving identity, geometry, and the current communication contract to the project |
| Sources | The `paper-brief` template of [monomind-ai-lab/hi-ted-meet-lisa](https://github.com/monomind-ai-lab/hi-ted-meet-lisa) (`references/slide-patterns-paper-brief.md`, read 2026-09-03): light paper ground on a faint twelve-column grid, inverted chapter pages, mega numbers, bar charts, decision boxes, numbered spec lists |
| Summary (KO) | "책상에서 읽고 전달되는 문서를 위한 장(章) 단위 브리핑 방식 — 반전된 장 표지가 이음새가 되고, 페이지마다 결론 하나, 무엇을 왜 결정했는지 적는 막대 차트와 결정 상자" |
| Summary (ZH-TW) | "供在桌前閱讀並轉寄的文件所用的分章簡報方法——反白的章節頁作為接縫，每頁一個結論，加上說明決定了什麼、為什麼的長條圖與決策框" |

## II. Communication Method

- **Preferred Mode**: briefing
- **Argument Flow**: A title page that names the report, its sources and its period; then chapters. Each chapter opens on an inverted page that states the chapter's claim and what downstream work it feeds, runs through pages that each carry one conclusion with its figures, and closes on a decision box. A closing page lists the decisions in chapter order. The chapter count follows the material; a chapter with one page is folded into its neighbour.
- **Page Message Discipline**: One conclusion per page, written as a sentence in the title, with the paragraph, table, chart or list beneath it as the support. Because the page is read rather than projected, four to eight items are acceptable — an eight-row table, a bar chart of six, a spec list of eight — but still one conclusion.
- **Claim Discipline**: Observations, interpretations and decisions stay distinguishable: the figure says what was measured, the paragraph says what it means, the decision box says what was decided and why, with the date and owner when the source has them. Settled matters are marked as settled so the reader does not re-argue them; contested ones say what would change the decision.

## III. Page Role Vocabulary

| Role | Communication Job | Evidence Obligation | Composition Tendency |
|---|---|---|---|
| Title page | Name the report, its type, sources, period and date | The meta row lists source, period and date | A rule at the head, the title and one lead sentence centred, the meta row at the foot; no page number |
| Chapter page | Open a chapter with its claim and what it feeds | One supporting sentence; no data | The page inverts to near-black; chapter number large, claim in two lines; no grid |
| Conclusion page | State one conclusion and support it | A paragraph, a table, a chart or a list directly under the conclusion | Title as a sentence, support below, the page number at the foot |
| Mega number | Make one figure the page | The figure, its unit, and the comparison beneath | The number at display size on the light ground; caption small |
| Bar chart | Compare a handful of quantities | Six bars at most, each labelled with its value; unit and period stated | Horizontal bars, value labels at the bar end, no legend |
| Spec list | Enumerate requirements, findings or steps | Numbered items, each verifiable, up to eight | Numbered, one column, the number in the accent colour |
| Decision box | Record what was decided and why | The decision, its rationale, the date and owner when known; what would reopen it | A bordered box at the foot of the chapter's last page; the word "Decision" as its label |
| Closing page | List every decision in chapter order | Each item traceable to its chapter | One list; no page number |

## IV. Evidence & Data Expression

- **Argument Trace**: Every decision box traces back to a conclusion page in its chapter, and every conclusion to a figure on the same page. The closing list repeats the decision boxes verbatim.
- **Charts**: Bar charts by default, because the comparison is the argument; a line only for a genuine time series. Values labelled at the bar end, unit and period on the chart, no legend, no gridlines. Colour separates the settled from the contested, not one series from another. Never invent a baseline, a peer or a target.
- **Tables**: Up to eight rows on a page, columns following the comparison; tabular figures so Latin numerals align inside CJK sentences; a problem row and a settled row carried by colour and a word in the row. A longer table is split by the argument.
- **Sources**: Source, period and scope in the title page's meta row for the whole report, and in the caption when a page's figures come from somewhere else. Estimates and proxies are labelled in the cell.
- **Native Editability**: Tables and charts export as editable native objects when the supported interface fits; otherwise as editable shapes. Decision boxes and spec lists are text and shapes, never images.

## V. Visual System Defaults

- **Preferred Visual Style**: editorial
- **Composition**: A white paper ground under a faint twelve-column grid; content on the grid, the page number at the foot. Chapter pages invert and drop the grid so the seams are visible when the reader scrolls or leafs. Read at desk distance, so the type is smaller than a projected deck's and the page holds more — bounded by a phone width and a short viewport in both languages, not by a projector.
- **Density**: Medium. Four to eight items on a page; one conclusion.
- **Decoration**: Rules and boxes only: a rule at the head of the title page, a border on the decision box, the grid. No shadows, gradients or ornament.
- **Color Behavior**: Near-black ink on white; one accent for what is a problem, one for what is already settled; chapter pages invert to near-black with off-white text and the accent unchanged. A confirmed Brand identity replaces these tendencies.
- **Typography Character**: A sturdy grotesque for titles and figures over a CJK-capable body face; hierarchy through weight, size and the inversion of chapter pages, never a third family. Tabular figures throughout. Exact families follow the resolved identity and the repository font policy.

## VI. Image & Icon Direction

- **Preferred Image Rendering**: editorial
- **Image Usage**: Occasional. A photograph or diagram earns a page when it is the evidence or the thing being decided about; never as a chapter opener's atmosphere.
- **Image Treatment**: Placed on the grid with a caption naming subject, source and date; hard edges, no scrim, no full bleed.
- **Icon Treatment**: None by default. If a state needs a glyph, one stroke family, small, in the ink colour.

## VII. Review Focus
<!-- visual-review-trigger: explicit-user-only -->
> Apply this section only after the user explicitly activates visual review. It never triggers that stage.

- Every chapter opens on an inverted page and closes on a decision box; no chapter is one page long.
- Each page carries one conclusion as its title and the support for that conclusion beneath it.
- Bar values, units and periods are on the chart; tables stay within eight rows; Latin figures align inside CJK text.
- Chapter pages carry no grid; content pages carry the page number; the title and closing pages carry none.
- The problem colour and the settled colour each mean one thing throughout.
- Nothing is clipped in either language at the smallest page the brief will be read at.
