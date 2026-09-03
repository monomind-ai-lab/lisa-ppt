---
description: Generate-route intake stage that reads a Hi Ted, Meet Lisa HTML deck into sources plus a pre-filled Design Spec before the Strategist's confirmation.
---

# Lisa Deck Intake

> Load only after [`routing.md`](./routing.md) §3 matches the source as a Hi Ted, Meet Lisa HTML slide deck. This stage replaces Default Generate Steps 1–2 (conversion and import) and returns to [`generate-pptx.md`](./generate-pptx.md) Step 3. It changes what the Strategist starts from, never who confirms: Stage 1 and Stage 2 stay ⛔ BLOCKING.

**Trigger**: one HTML file made by Lisa's `monomind-deck`, `evidence-deck`, or `paper-brief` template — recognisable by its `LISA:CONTENT-MAP` header, `section.slide` elements carrying `data-screen-label` or `data-label-*`, and the template's `:root` token block — or the user runs `/lisa-ppt <deck>.html` or asks for a PPTX from a Lisa deck. Lisa's document-kind files (`web-document`, `project-website`, `motion-website`, `sitemap-ia`, `architecture`, `mermaid-master`) are not decks: the importer refuses them, and they enter Step 1 as ordinary HTML.

**Hard rule — runtime paths**: expand `${SKILL_DIR}` inside each tool call; never change CWD.

---

## 1. What the importer reads, writes, and refuses to invent

| Reads | Writes | Refuses to invent |
|---|---|---|
| The `LISA:CONTENT-START/END slides` fence, or every `section.slide` when a finished deck dropped the fence | `sources/<stem>.md` — one `##` per slide: kind, eyebrow, statement, lead, then every canvas component as a Markdown table or list (tables with flagged rows, stat rows, mega numbers, cards, verdict and decision bars, spec lists, numbered points, bar-chart values and bar widths, card grids, chips, file trees, leader rows, steps, workflows, bullets, code, flags, connectors, mappings, panels) | Slide content the markup does not carry — no filler, no summaries, no invented numbers |
| Inline language spans (`.en` / `.ko` / `.zh`) and the body's `data-lang` | `sources/<stem>.<lang>.md` per non-primary language, same slides in that language | A translation: a string written in one language only appears only in that language's file; `monomind-deck` carries one language inline, so it yields one file |
| The `:root` tokens and the per-language `body[data-lang]` font rules | `design_spec.md` pre-filled: page count, primary language, the family's look as Design Style, every colour role that resolves to a flat `#RRGGBB` with `` `fact` `` provenance naming its token, the title/body/code stacks, cross-page continuity observed in the markup, one `#### Slide NN` block per slide with `Title`, a `Core message` only when the deck states one (verdict bar, decision box, takeaway line), and a `brief`-depth `Content` block list | Every Stage-1/Stage-2 decision — audience, intent, outcome, delivery, canvas, reading mode, mode, visual style, tone, sizes, spacing, icons, notes, animations, narration, `Audience move`, `Relationships` — stays `[fill]`; a token that is `rgba()` or `color-mix()` stays `[fill]` and is listed |
| Embedded `data:` images inside the slides | `sources/<stem>_files/<slideNN-MM>.<ext>` plus `image_manifest.json`, and one §VIII row (`Acquire Via: user`, `Status: Existing`) each | CSS background photography (template artwork) and external image URLs — listed, not fetched |
| The whole file | `sources/<stem>.html` (the archived original), `sources/<stem>.conversion_profile.json`, `analysis/lisa_intake.json` (the typed outline), one `validation/workflow.log` note | Chrome: brand mark, page numbers, progress bar, nav dots, menu, language switch, colophon, copy buttons |

Anything the importer could not classify keeps its text as a plain paragraph marked `<!-- unclassified markup: <tag.class> -->`, and the printed summary names it; the component type is never guessed.

---

## 2. Procedure

### Step L1 — Import (replaces Generate Steps 1–2)

🚧 **GATE**: the user named one Lisa HTML deck; further materials (a brief, data, a second document) are ordinary Step 1 inputs.

```bash
python3 ${SKILL_DIR}/scripts/lisa_html_intake.py <deck.html> --project projects/<name> [--format <registered_format>]
```

The importer creates the project through `project_manager.py init` when the path does not exist (the directory gains the usual `_<format>_<YYYYMMDD>` suffix; re-running with the same `--project` reuses it) and refuses to overwrite an existing `design_spec.md` without `--force`. `--format` follows the truthful-canvas rule of Generate Step 2: pass it only when the canvas is already an exact registered fact; otherwise Stage 1 confirms the canvas and the pre-filled §II stays `[fill]`. `--dry-run` prints the outline without writing; `--json` prints the machine-readable outline.

**Hard rule — never `import-sources` the deck itself**: `import-sources` routes `.html` to `doc_to_md.py` and would add a second, flat Markdown of the same slides beside the typed one; the importer already archived the original under `sources/`. Other materials still go through `import-sources`.

**Mandatory — read the summary, keep it**: the printed summary carries the family, the languages (primary first), the slide count, the component census, the colour and font facts, and the `Not invented` list. That list is the agenda of Stage 1: every item is a question the deck cannot answer.

**Images**: for each `sources/<stem>_files/` file listed, copy it into `<project_path>/images/` before Stage 2 (it is a `user` asset the Strategist places, not a Step 5 acquisition), then run `python3 ${SKILL_DIR}/scripts/analyze_images.py <project_path>/images`.

**✅ Checkpoint** — `sources/<stem>.md` (and one sibling per other language), the archived `.html`, `analysis/lisa_intake.json`, and `design_spec.md` exist; `project_manager.py validate` reports only unresolved `[fill]` placeholders and the missing lock. Proceed to Generate Step 3.

### Step L2 — Continue Default Generate from Step 3

Step 3 is unchanged: the deck is a source, never a template candidate; `default_mode` is `free_design` unless the user supplied a workspace root (for example `brands/monomind`).

Step 4 changes only where the deck supplies a fact:

| Stage | With a Lisa deck |
|---|---|
| Stage 1 | Recommend `primary_language` from the importer's primary; the deck's slide count as the roster range; reading mode from the family (`present` → `presentation`, `read` → `text`) as the recommendation. The `[fill]` rows of §I are the open questions to recommend on. The deck's tokens and fonts are not Stage-1 evidence — Stage 1 stays template-independent and user-confirmed |
| Stage 2 | The first `design_direction` is the deck's own look: the `fact` colour rows of §III as its palette and the deck's title/body/code stacks as its typography, so the confirm UI shows the deck's colours and fonts as the recommended direction. State on that direction that its faces are web fonts the export flags as non-PPT-safe; the user's confirmation decides between keeping them (record `requires <family>` in §IV) and the house family. Directions two and three follow the ordinary Strategist rules. When the confirmed direction keeps the deck's faces, the user has named them in this conversation, which is the house-font lock's own exception |
| Design Spec | Author the complete Design Spec by completing the pre-filled file: resolve every `[fill…]` from the retained confirmation, keep each `fact` row unless the confirmation changed it, keep the §IX roster ids, count, and order equal to the deck's slides unless Stage 1 changed the range, write `Audience move` and `Relationships` for every page, and keep the `Core message` lines the deck stated. `sources/<stem>.md` is the content authority; `analysis/lisa_intake.json` is the typed view of the same facts |
| Second language | The sibling `sources/<stem>.<lang>.md` is a translation resource, not a second roster: one deck carries one `primary_language`; a deck in the other language is a second run with that language confirmed, never two languages merged into one page |

Gate 1, the lock, `validate`, and Steps 5–7 are unchanged. Quick Generate on explicit Quick intent runs Step L1, then [`quick-generate`](./profiles/quick-generate.md) §2 from `sources/` and `analysis/lisa_intake.json`; the importer's `design_spec.md` is reference input there, never a lock.

---

## ✅ Lisa Deck Intake Complete

- [x] `sources/<stem>.md` exists with one `##` per slide; every other language has its sibling
- [x] `design_spec.md` exists with the deck's `fact` colour and font rows and `[fill]` everywhere the markup is silent
- [x] The printed `Not invented` list is retained as the Stage-1 agenda
- [ ] **Next**: [`generate-pptx.md`](./generate-pptx.md) Step 3, then the ⛔ Stage-1 / Stage-2 confirmation
