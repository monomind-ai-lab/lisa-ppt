---
style_id: evidence-deck
kind: style
summary: Argue-from-numbers method for a case someone will push back on — tables that flag their own rows, stat rows, one number at display size, and a verdict bar that says what to do about it.
keywords: [evidence, numbers, verdict, audit, data-tables]
---

# Evidence Deck — Style Specification

> Method and design defaults only. No project communication contract, brand identity, page structure, or SVG prototypes.

## I. Style Overview

| Property | Value |
|---|---|
| Style Name | Evidence Deck |
| Best Fit | An argument that will meet resistance and has to show its measurements: an audit, a diagnosis, a post-incident finding, a recommendation defended by data in a room |
| Reusable Intent | Make every page a measured claim — the number, the table row, the comparison it rests on — and end each section with a verdict the audience can act on, while leaving identity, geometry, and the current communication contract to the project |
| Sources | The `evidence-deck` template of [monomind-ai-lab/hi-ted-meet-lisa](https://github.com/monomind-ai-lab/hi-ted-meet-lisa) (`references/slide-patterns-evidence-deck.md`, read 2026-09-03): dark full-bleed slides, flagged data tables, stat rows and mega numbers, verdict bars, section cards |
| Summary (KO) | "숫자로 논증하는 방식 — 반박이 예상되는 주장을 위해, 문제 행을 스스로 표시하는 표, 스탯 행, 디스플레이 크기의 숫자 하나, 그리고 무엇을 할지 말하는 판정 바" |
| Summary (ZH-TW) | "用數字論證的方法——為會被質疑的主張準備：自己標出問題列的表格、統計列、一個放大到展示字級的數字，以及一條說明該怎麼做的裁決欄" |

## II. Communication Method

- **Preferred Mode**: pyramid
- **Argument Flow**: Open with the verdict and the one measurement that earns it. Then work section by section: each section opens on a card that names its claim, shows the evidence as rows and numbers, and closes on a verdict bar — what is wrong, what is working, what to do. The last page repeats every section verdict as one list. Adapt the section count to the material; never pad a section to fill a rhythm.
- **Page Message Discipline**: One measured claim per page, as an assertion title. The claim names the quantity and the direction (higher, lower, missing, late), and the proof — a table, a stat row, a single number — sits directly under it. A page with two claims is two pages.
- **Claim Discipline**: Facts carry their unit, period and source. A flagged row says why it is flagged in the row itself, not in a footnote. Implications are set apart from the measurement that produced them, and a recommendation always follows a verdict, never precedes it. A number the source does not contain stays a bracketed slot; it never becomes an invented figure.

## III. Page Role Vocabulary

| Role | Communication Job | Evidence Obligation | Composition Tendency |
|---|---|---|---|
| Opening verdict | State the conclusion and the one number that decides it | The number, its unit, period and source; the comparison it beats or misses | The number at display size, the verdict as the title, everything else small |
| Section card | Name the next part of the argument and what it feeds | One sentence of support; no data yet | One full-bleed card in the signal colour; one per section, never consecutive |
| Data table | Prove a claim across rows | Every row labelled; problem rows and working rows flagged in the row; units and period in the header | The table dominant, the claim above it, at most one emphasis colour per row state |
| Stat row | Compare a handful of measurements at a glance | Three to five numbers, each with a label and unit; a delta only when the baseline is on the page | Equal cells in one row; the alarming cell in the signal colour |
| Mega number | Make one measurement unmissable | The number, its unit, and the comparison in one line beneath | The figure fills the page; the caption stays small |
| Spec list | Enumerate what was checked, decided or required | Numbered items, each verifiable | Numbered, two columns at most, no icons doing the numbering's job |
| Verdict bar | Close a section with the action | The verdict restates the evidence it rests on; the action names an owner or a next step when the source has one | A full-width bar in the signal colour at the foot of the page |
| Closing list | Repeat every verdict in one place | Each item traceable to its section | One list, numbered by section, nothing new |

## IV. Evidence & Data Expression

- **Argument Trace**: Every verdict bar traces back to a flagged row, a stat cell or a mega number on the pages before it, and forward to the closing list. A verdict with no measurement on the page is not written.
- **Charts**: Prefer the table and the stat row; use a chart only when the shape of the data — a trend, a distribution — is the evidence. Direct labels, the decision-relevant point annotated, units and period on the chart, no legend when direct labels do the job, no gridlines or effects. Never invent a baseline, a peer or a target.
- **Tables**: Columns follow the comparison; the key column reads first, the number column is right-aligned with tabular figures, paths and identifiers are set in the mono face. A row state — problem, working — is carried by the row's colour and a one-word reason inside the row, never by a symbol alone. Keep the row count within one page; a longer table is split by the argument, not by the page.
- **Sources**: Source, period and scope sit in the table header or the caption, adjacent to the data. Estimates and proxies are labelled as such in the cell.
- **Native Editability**: Tables and charts export as editable native objects when the supported interface fits; otherwise as editable shapes. Stat rows and mega numbers are text, never images.

## V. Visual System Defaults

- **Preferred Visual Style**: data-journalism
- **Composition**: A dark, full-bleed field with one column of content and generous margins; the claim at the top, the evidence in the middle, the verdict bar at the foot. Numbers set at display size; body text never below the base size, because the deck is read across a room. One idea per page, one to three bullets where bullets are needed at all.
- **Density**: Low. A table of six to eight rows, a stat row of three to five cells, one mega number. A page that needs more is two pages.
- **Decoration**: None beyond the section card and the verdict bar. Flat fills, hairline rules, no shadows, gradients or badges.
- **Color Behavior**: A near-black ground with off-white text; one signal colour for what is alarming and what must be done; one second colour for what is already working; the mono face in a third, muted tone for paths and identifiers. Nothing else carries colour. A confirmed Brand identity replaces these tendencies.
- **Typography Character**: A heavy display face for titles, numbers and verdicts against a plain grotesque body; hierarchy through weight and size, never through a third family. Exact families follow the resolved identity and the repository font policy.

## VI. Image & Icon Direction

- **Preferred Image Rendering**: minimalist-swiss
- **Image Usage**: Rare. An image appears only when it is itself evidence — a screenshot of the failing state, a photograph of the measured thing. No atmosphere, no stock.
- **Image Treatment**: Cropped to the evidentiary subject, hard edges, a caption naming what is shown and when; no scrim, no full-bleed hero.
- **Icon Treatment**: Almost none. One stroke family if a role or state genuinely needs a glyph; never as bullets, never as decoration on cards.

## VII. Review Focus
<!-- visual-review-trigger: explicit-user-only -->
> Apply this section only after the user explicitly activates visual review. It never triggers that stage.

- The verdict on each section-closing page follows from a measurement visible on the pages before it.
- Every flagged table row states its reason inside the row, and the flag colour means one thing throughout the deck.
- Numbers carry unit and period; no figure appears without its comparison or its source.
- Text at the rendered slide size reads from across a room; nothing falls below the base size to fit.
- The signal colour appears only on what is alarming or actionable; the working colour only on what works.
- No bracketed slot has become a number.
