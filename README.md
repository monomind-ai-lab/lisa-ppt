# Lisa's PPT

<p align="left">
  <img src="assets/tedandlisa-cover.jpg" alt="Hi Ted, Meet Lisa" style="width: 100%; max-width: 100%;">
</p>

**English** · [한국어](README_KO.md) · [繁體中文](README_ZH-TW.md)

> **Natively editable PowerPoint for [Hi Ted, Meet Lisa](https://github.com/monomind-ai-lab/hi-ted-meet-lisa).**
> One `.pptx`. Every shape, text box and chart is a PowerPoint object.
> Installed as a skill; there is no web mode.

Hi Ted, Meet Lisa makes one standalone HTML file. Some rooms want a `.pptx`
instead: text you click and retype, a chart with an Edit Data button, a file
that opens in PowerPoint with nothing else installed. Lisa's PPT makes that
file.

It is a hard fork. The engine is [PPT Master](https://github.com/hugohe3/ppt-master)
v6.1.0 by Hugo He (MIT), imported once. On top of it sit the refinements of
[slide-master](https://github.com/byungjunjang/slide-master) by byungjunjang
(MIT): images through Codex's own image tool, version-numbered exports, seven
Korean-domain layouts, a house-font rule, a Korean intake. From that point the
repository is independent. Nothing is pulled from either source again; a later
backport is a hand-made change, recorded in [`NOTICE`](NOTICE) with the commit
it came from.

The intake speaks English, Korean and Traditional Chinese. So does this README.

---

## Start here

Python 3.10 to 3.14, then the requirements. No Node required: the Codex CLI,
which draws the images, is an optional Node tool, and the export check is
Python.

```sh
pip install -r requirements.txt
```

Install the plugin once. `/lisa-ppt` is then a command you have for good.

```sh
/plugin marketplace add monomind-ai-lab/lisa-ppt
/plugin install lisa-ppt@monomind-ppt
```

In Codex, the two steps are one:

```sh
codex plugin marketplace add monomind-ai-lab/lisa-ppt
```

For any agent that follows the Agent Skills convention:

```sh
npx skills add monomind-ai-lab/lisa-ppt
```

Or clone the repository and open the folder in your agent. The skills live
under `skills/`, with generated stubs under `.codex/skills/` so Codex finds the
same three.

**Images are optional and need no API key.** Install the Codex CLI and sign in
once. Lisa's PPT then draws through Codex's own `image_gen`; leave
`IMAGE_BACKEND` unset and that is the default. An API-key backend can be set
by environment variable instead.

```sh
npm install -g @openai/codex
codex login
```

**A `.pptx` embeds no fonts.** Install the house family for each language on
every machine that opens the deck: Pretendard for Korean, Noto Sans TC for
Traditional Chinese, Plus Jakarta Sans for English, JetBrains Mono for ids and
code. The files are bundled in this repository with their SIL OFL texts; one
command installs them user-level on macOS, Windows and Linux.

```sh
python3 skills/lisa-ppt/scripts/install_fonts.py            # --dry-run shows the plan, --check reports
```

**Then, whenever you need something:**

```text
/lisa-ppt projects/q3/sources/report.pdf, about 10 pages for the board, restrained
```

Reads the source, opens the intake in your browser, writes one SVG per page
with a live preview, checks the geometry, and exports
`projects/q3/exports/<title>_ver1.pptx`.

```text
/lisa-ppt a deck that explains RAG to non-engineers; research it yourself
```

No source? The agent researches first, then runs the same pipeline.

```text
/lisa-ppt deck.html
```

A finished Lisa deck? Its slides become the project's source Markdown and
its own colour tokens a pre-filled `design_spec.md`, so the `.pptx` starts
from the deck's own look.

Say the rest in plain words; the router picks the route:

```text
Fill sources/company-template.pptx with the plan in sources/plan.md
```

```text
Add speaker notes and narration to exports/deck_ver2.pptx
```

Both are the Edit Native PPTX route. The first keeps a template's design and
fills it, page by page, with unchanged pages copied byte for byte. The second
writes notes and narration into the file and exports a `_narrated` sibling.

**What you get**

- **One `.pptx`** of native DrawingML shapes, text boxes and charts. Click any
  element in PowerPoint and change it.
- **Native charts and tables on request.** Export with
  `--native-charts-and-tables` and eligible groups become PowerPoint Chart and
  Table objects with Edit Data, in a `_native_charts_tables` sibling. The
  default keeps them as editable shapes that render the same in every app.
- **Versioned exports.** `<title>_ver1.pptx`, then `_ver2`, never over the last.
- **Seven layouts** from slide-master: `academic_defense`, `government_blue`,
  `government_red`, `medical_university`, `psychology_attachment`, `ai_ops`,
  `pixel_retro`, beside the seven upstream ships. Plus the `monomind` brand in
  Lisa's own tokens, and two house styles, `evidence-deck` and `paper-brief`.
- **Canvases** beyond 16:9: 4:3, A4, banner, story, the social formats
  upstream ships, and `instagram` at 1080×1350.
- **One house font per language.** Hierarchy by weight and size, not by
  switching families.

---

## How a deck gets built

1. **You hand over a source.** A PDF, a DOCX, Markdown, a URL, a spreadsheet,
   or one paragraph. The agent makes `projects/<name>/` and reads it.
2. **The intake opens in your browser**, in English, Korean or Traditional
   Chinese (Simplified Chinese and Japanese are kept from upstream). Two
   stages: the communication contract first, then the final plan and
   production. Canvas, page count, layout or brand, font, image policy; every
   question with a default. Every option is an id in the catalog, so the
   language you read the questions in never reaches the deck.
3. **Images**, if you asked for them, through Codex's `image_gen`.
4. **One SVG per page**, written in the confirmed design system, with a live
   preview. Click a spot in the preview to annotate it and the agent fixes
   that page.
5. **The geometry gate.** Overlapping text, shapes off the canvas and awkward
   line breaks are found from glyph widths and fixed; flagged pages are
   rendered to pixels and looked at again. Ask, and it runs a visual review
   per page.
6. **Export.** The converter turns each SVG into DrawingML and writes
   `projects/<name>/exports/<title>_ver<N>.pptx`. A delivery check reads the
   file back for package integrity and portability.

---

## Fonts

One family per language. Pretendard for Korean, Noto Sans TC for Traditional
Chinese, Plus Jakarta Sans for English; JetBrains Mono for ids and code.
Hierarchy comes from weight, size, tracking and colour, never from switching
families. The converter registers the CJK families for both the Latin and the
East-Asian slot, so PowerPoint does not substitute one of them in a mixed run.

The prompts name only the weights that are bundled: six of Pretendard and of
Plus Jakarta Sans (Light to ExtraBold), four of Noto Sans TC (Light, Regular,
Medium, Bold), three of JetBrains Mono (Regular, Medium, SemiBold). A `.pptx`
embeds none of them: install the family on every machine that opens the deck,
or the deck opens in whatever that machine substitutes. The policy in full is
in [`AGENTS.md`](AGENTS.md) and
[`skills/lisa-ppt/assets/fonts/README.md`](skills/lisa-ppt/assets/fonts/README.md).

---

## Two lanes to Lisa

Both are in progress in their own branches; neither is in this tree yet.

- **From Lisa to here.** The `/lisa` intake will list Lisa's PPT as an
  external card with a `PPTX` badge. Pick it, and the brief and the answers
  you gave Lisa arrive as the first stage's contract, with the `monomind`
  brand selected. It will need this plugin installed.
- **From a Lisa file to here.** `/lisa-ppt deck.html` will read a finished
  Lisa deck: its `LISA:CONTENT-START/END` regions become the project's source
  Markdown, and its token block becomes a pre-filled `design_spec.md`, so the
  `.pptx` matches the HTML.

---

## The `projects/` folder

Every deck is a folder. Nothing is written outside it.

| Path | What is there |
| --- | --- |
| `projects/<name>/sources/` | What you handed over, and its Markdown conversion |
| `projects/<name>/design_spec.md` | The confirmed design system and content outline for this deck |
| `projects/<name>/notes/` | One Markdown note per page, and `total.md` |
| `projects/<name>/images/` | Generated, sourced and supplied images |
| `projects/<name>/svg_output/` | One SVG per page, as written |
| `projects/<name>/svg_final/` | The self-contained preview SVGs |
| `projects/<name>/exports/` | `<title>_ver<N>.pptx` and its `_native_charts_tables` and `_narrated` siblings |

`analysis/`, `templates/` and `validation/` hold extracted facts, project-level
templates and the workflow log. `projects/` is yours and is not committed. Move
it when you move machines.

---

## What it does not do

- **Finish in one shot.** The model sets the ceiling; a large-context Claude
  is the recommendation. Plan on a polish pass, in the preview or in
  PowerPoint.
- **Embed fonts.** See above.
- **Promise formulas outside PowerPoint.** Formulas export as OMML and edit in
  PowerPoint; Keynote, WPS and LibreOffice are outside the contract.
- **SmartArt.** Left out on purpose.
- **Resume quick mode.** Quick mode is one pass without the confirmation
  stage and without a resumable design record.
- **Transparent images from gpt-image-2.** Asked for a transparent background,
  the model paints a checkerboard. The `codex-image` skill rewrites the prompt
  and says so; ask for a flat background when you can.
- **Stay small — but know what "small" means here.** A full clone is 210 MB
  and `--depth 1` is 131 MB; the measured breakdown is in
  [How big it is](#how-big-it-is) below. `templates/icons/` alone is
  12,027 SVGs — only about 13 MB of content, but ~48 MB once the filesystem
  rounds 12,027 tiny files up to blocks — kept in the tree rather than moved
  to a release download so a plugin install is complete; the bundled fonts are
  32 MB.
- **Run on every Python.** 3.10 is the floor and 3.14 is verified:
  `skia-pathops` and `uharfbuzz` ship abi3 wheels, and the pipeline is
  exercised on 3.11.

---

<p align="left">
  <img src="assets/ted-and-lisa.jpg" alt="Ted and Lisa" width="460">
</p>

---

## What is included

- **`lisa-ppt`**: the pipeline. Intake, SVG pages, quality gate, export, and
  the Edit Native PPTX route that fills a template or adds notes, narration
  and transitions to a finished file.
- **`codex-image`**: images through the Codex CLI, with the transparency
  workaround. Based on wjb127/codex-image.
- **`diagram-design`**: diagram composition rules, vendored from
  cathrynlavery/diagram-design. Its standalone flow is switched off and the
  disabled text is kept verbatim as a record.
- **The confirm UI**, the SVG editor with live preview, the DrawingML
  converter, the quality checker, and the `.codex/skills` stub sync.
- **Templates**: fourteen layouts, the `monomind` brand, the `evidence-deck`
  and `paper-brief` styles beside upstream's twelve, the chart and table
  templates, and the icon library.

---

## How big it is

Measured on `main`, 2026-09-03:

| | |
|---|---|
| `git clone` | **210 MB** — a 94 MB checkout plus 116 MB of history |
| `git clone --depth 1` | **131 MB** — the same checkout, 37 MB of history |
| The checkout alone | 12,869 files, 55 MB of content, about 94 MB on disk |

Two directories account for 80 of those 94 MB, and both are deliberate:

- **`skills/lisa-ppt/templates/icons/`** — 12,027 SVGs. Only 13 MB of content,
  but roughly 48 MB on disk: every file is under a kilobyte and every file
  still takes a filesystem block. Kept as files, because a deck that has to
  stop and fetch an icon is a deck that stops.
- **`skills/lisa-ppt/assets/fonts/`** — 32 MB, 19 weights across four
  families. PPTX does not embed fonts, so the family a page names has to exist
  on the machine that opens it. `install_fonts.py` puts them there.

The history is heavier than the checkout because the v6.1.0 import brought in
upstream's `docs/assets/` (33 MB, a hero GIF) and its AI-image comparison
gallery (43 MB of PNGs), and both were removed in the same series of commits.
They are gone from the tree and still in the history; each is now a README
pointing at where it went. `--depth 1` skips them, and nothing in the pipeline
needs them.

---

## Where it comes from

Two imports, then independence.

1. **PPT Master v6.1.0** (`hugohe3/ppt-master`, commit `c40bca58`,
   2026-08-31), brought in as one commit: the SVG-per-page pipeline, the
   DrawingML converter, the OMML formula subsystem, hyperlink preservation,
   the `svg_quality` checker, merge-shapes and text shaping.
2. **slide-master** (`byungjunjang/slide-master`, commit `166472b`,
   2026-08-04), ported file by file as its own commits: the Codex image
   backend and its transparency rule, `_ver<N>` exports, the seven layouts,
   the `instagram` canvas, the Korean intake strings and README, the
   house-font rule, the stub sync, the `diagram-design` vendoring pattern.

There is no upstream remote, no update script and no runtime attribution
guard. `NOTICE` is the ledger: both import points, every ported file, and any
later backport with the upstream commit it came from.

---

## Licence

[MIT](LICENSE). The chain, in full in [`NOTICE`](NOTICE):

- PPT Master, Copyright (c) 2025-2026 Hugo He, MIT
- slide-master by byungjunjang, MIT; credited by name, URL and imported commit
- `codex-image`, Copyright (c) 2026 wjb127, MIT; licence shipped in the skill
- `diagram-design`, Copyright (c) 2025 Cathryn Lavery, MIT; licence shipped in
  the skill
- Pretendard, Noto Sans TC, Plus Jakarta Sans and JetBrains Mono, SIL Open
  Font License 1.1; texts beside the files
- Lisa's PPT, Copyright (c) 2026 MonoMind AI Lab, MIT

Lisa's PPT will be surfaced beside the HTML templates on
[html.monomind.one](https://html.monomind.one).
