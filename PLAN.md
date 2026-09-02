# Plan — Lisa's PPT

Written 2026-09-02 by the Hi Ted, Meet Lisa orchestration session; the build
session reads this file and executes it: one branch per workstream, never on
main, subagents doing the work under a lead that reviews.

## What Daren decided (2026-09-02)

PowerPoint is an **affiliated feature** of Hi Ted, Meet Lisa: surfaced through
the same website (html.monomind.one), served from a **separate repository**,
distributed as an **install-only skill**. Hard-fork `hugohe3/ppt-master`, keep
its capabilities, rebrand it as **Lisa's PPT**, rebuild its intake UI to the
Ted & Lisa brand experience without losing any of its features, and push to a
new MIT-licensed public repository: **`monomind-ai-lab/lisa-ppt`** (org
confirmed by Daren, 2026-09-03).

Background: the four-repo study kept in the Lisa workspace (its section 3
is the PPT Master analysis). Clone upstream fresh.

## Facts that shape the fork (verified from source, 2026-09-02)

- **Upstream:** `hugohe3/ppt-master`, MIT, v6.1.0, last commit 2026-08-31.
  Python 3.10+, 106-line `requirements.txt` (python-pptx, XlsxWriter,
  skia-pathops, uharfbuzz, PyMuPDF, Pillow, numpy, PyYAML, requests, bs4,
  curl_cffi, mammoth, markdownify, ebooklib, nbconvert, openpyxl, edge-tts,
  google-genai, flask). Optional Playwright (visual review), Pandoc (legacy
  formats). No Node, no LibreOffice.
- **Pipeline:** sources → Markdown (`source_to_md.py`) → project init →
  template candidates → Stage 1 confirm → Stage 2 confirm → `design_spec.md`
  + `spec_lock.md` → optional images → the main agent hand-writes one SVG per
  slide → `finalize_svg.py` → `svg_to_pptx.py` (own SVG→DrawingML converter)
  → native editable PPTX. Quality gate (`svg_quality_checker.py`, 360 KB of
  rules) is mandatory before export.
- **Intake UI:** Flask app at `scripts/confirm_ui/` — `server.py` (120 KB),
  `static/app.js` (235 KB), `static/catalogs.json` (57 KB), `style.css`, 18
  SVG style previews. EN / 中文 / 繁體中文 / 日本語. Two stages; the agent
  writes `template_options.json`, `recommendations.stage{1,2}.json`; the user's
  submission writes `template_selection.json` and `result.json`. Hard rule:
  *the agent never confirms on the user's behalf; silence confirms nothing.*
- **Images:** Path A `image_gen.py --manifest` with 15 API backends; Path B
  host-native image tool (Codex, Claude Code); Offline Manual. Contract:
  `images/image_prompts.json` with per-item `status`.
- **Templates:** four orthogonal kinds — `brands/` (21), `styles/` (13),
  `layouts/` (8), `decks/` (3); each a `design_spec.md` (YAML + tables with
  a `fact`/`approx` provenance column), discovered through `*_index.json`.
- **Attribution guard:** `scripts/attribution_guard.py` verifies exact
  `SKILL.md` frontmatter, a SHA-256 of `LICENSE`, the presence of
  `SPONSORS.md`/`SPONSORS_CN.md`, and (by AST) that `require_skill_integrity()`
  is called in `svg_to_pptx.py`, `svg_quality_checker.py`,
  `svg_quality/cli.py`, `svg_to_pptx/pptx_package/cli.py`,
  `register_template.py`, `template_preview_pptx.py`, plus
  `_require_official_distribution_identity()` in `console_encoding.py`. Any
  failure stops the skill. **A rebrand trips it by design.**
- **Bulk (250 MB):** `.git` 99 MB · `templates/icons/` 48 MB (12,027 SVGs
  from tabler, simple-icons, phosphor) · `references/ai-image-comparison/`
  43 MB (55 PNGs, documentation) · `docs/assets/` 33 MB (screenshots, one
  19 MB GIF) · `templates/sounds/` 12 MB (186 WAVs, optional) · `scripts/`
  8.7 MB (the engine). Upstream's own release zip is ~56 MB.
- **Prompt bulk:** ~269 Markdown files; README says to use a ~1M-token model.

## Workstreams (one branch each, one subagent each)

### W1 · Fork, licence, guard
1. `git clone https://github.com/hugohe3/ppt-master lisa-ppt`; add
   `upstream` remote; record the forked commit in `NOTICE`. Keep history
   (attribution and future cherry-picks) unless the push size is a problem;
   if squashing, keep the upstream hash in the first commit message.
2. **Licence:** stays MIT. `LICENSE` keeps upstream's copyright line
   (`Copyright (c) Hugo He`) and adds MonoMind's. `NOTICE` states: based on
   PPT Master by Hugo He (link, commit), what was changed, and that sponsor
   material was removed. README opens with the same one-line credit.
3. **Guard:** remove `attribution_guard.py`, every `require_skill_integrity()`
   call-site listed above, `_require_official_distribution_identity()`, and
   `SPONSORS*.md`. Remove affiliate links and the "never surface sponsor"
   rule from `SKILL.md` (nothing to surface). MIT permits this; the NOTICE
   is the attribution that replaces it.
4. **Trim:** drop `docs/assets/`, `references/ai-image-comparison/` (keep a
   Markdown pointer to upstream's copies), and `templates/sounds/` (or move
   to a release asset). Keep `templates/icons/` — the pipeline reads it —
   but consider a release-asset download for the plugin path.
5. Verify the pipeline still runs end to end on this machine after the cut
   (`python3` here is 3.14 — check that `skia-pathops` and `uharfbuzz` have
   wheels for it; if not, document the supported Python range).

### W2 · Rebrand
- Names: "PPT Master" → **Lisa's PPT**; `skills/ppt-master/` →
  `skills/lisa-ppt/`; command `/lisa-ppt`; `.claude-plugin/plugin.json` name
  `lisa-ppt`, `marketplace.json` owner MonoMind AI Lab (mirror
  `hi-ted-meet-lisa`'s manifests); `.codex-plugin/` too.
- README: rewrite in Lisa's voice (short declaratives, concrete nouns, no
  adjectives doing sales work). Keep `README_CN.md` (upstream is Chinese-
  first); Lisa's own set is EN / KO / ZH-TW, so add KO and decide whether CN
  becomes ZH-TW or stays beside it. Same install shapes as Lisa: plugin
  marketplace, `npx skills add`, clone.
- Every prose reference to "PPT Master" in `workflows/`, `references/`,
  `stages/`, `scripts/docs/` — grep and replace; keep the attribution line.
- House entries: `brands/monomind/templates/design_spec.md` (MonoMind
  tokens: ink `#102033`, page `#eef6ff`, accent `#4f8cff`, Plus Jakarta Sans,
  JetBrains Mono, Noto Sans KR/TC; every colour with a `fact`/`approx`
  provenance mark) and `styles/` entries mirroring Lisa's `evidence-deck`
  (argue from numbers) and `paper-brief` (chaptered briefing). Register them
  with `register_template.py`.

### W3 · Intake UI rebuilt to the Ted & Lisa experience — nothing lost
Keep, unchanged: the two-stage flow; every question and option in
`catalogs.json`; the receipts model and file ownership; the three-direction
bundles in Stage 2; the five-language dictionary (add KO to EN/中/繁/日 —
Lisa's rule D-030: the UI language never reaches the payload, an answer is
the same id in every language); the daemon/wait/shutdown CLI.

Change, to match `monomind-ai-lab/hi-ted-meet-lisa` → `assets/tedandlisa-intake.html`:
1. **Tokens and type** in `style.css`: deep-ink ground, page `#eef6ff`,
   accent `#4f8cff`, Plus Jakarta Sans display/body, JetBrains Mono for
   ids and code, Noto Sans KR/TC for CJK. Take the values from Lisa's panel,
   not from memory.
2. **Shell:** Lisa's fixed-height app shell with a left rail that is how you
   move (D-029) and chaptered screens (D-028): Stage 1 = *Brief · Grounds ·
   Template*, Stage 2 = *Direction · Look · Production · Preferences*
   (output-configuration answers last, D-042).
3. **Gallery cards** for brands/styles/layouts/decks in the same card
   grammar as Lisa's template gallery: thumbnail, type flag, tagline,
   "best for", a preview link — the 18 SVG previews become the thumbnails.
4. **Copy** in Lisa's register; the figures and the MonoMind mark in the same
   corners as Lisa's panel; "Made with Hi Ted, Meet Lisa" colophon.
5. **Payload display:** the receipt the user submits shows the ids, like
   Lisa's "Copy JSON" fallback, so a session without a browser can still
   paste it.
6. **Do not** port Lisa's web mode: this skill is install-only.
Verify in a browser at 1280 and 375 px, all five languages, both stages,
one full round trip that produces `result.json`.

### W4 · The two Lisa lanes
- **Lane B — handoff from Lisa (in `hi-ted-meet-lisa`, after this repo
  exists):** registry entry `{ id: "lisa-ppt", kind: "external",
  type: "present", skill: "/lisa-ppt", requires: "Lisa's PPT plugin",
  badge: "PPTX" }`; the handoff passes Lisa's brief and answers as the
  Stage-1 contract and selects `brands/monomind`. This is a small PR in the
  Lisa repo and is **feasible** as arranged.
- **Lane A — a Lisa HTML deck to PPTX (in this repo):** add
  `scripts/lisa_html_intake.py`: read a Lisa file's `LISA:CONTENT-START/END`
  fences (eyebrow, statement, lead, `dg-canvas` components as named in
  `references/slide-patterns*.md`) into the project's source Markdown and a
  pre-filled `design_spec.md` from the file's token block, so
  `/lisa-ppt path/to/deck.html` yields a PPTX that matches the deck. This
  keeps Lisa itself stdlib-only and is **feasible** as arranged — better
  here than in Lisa, because the converter and quality gate already live
  here.

### W5 · Website surface (in `monomind-ai-lab/ted-and-lisa`, after the push)
One appended gallery card (D-035: append, never insert — the `T` dictionary
uses positional selectors): "Lisa's PPT · PPTX · install-only", linking to
the repo; one line in `site/llms.txt`. No second paid surface (D-025).

## Acceptance
- End-to-end run on this machine from a one-paragraph brief to an opened
  `.pptx`, with the rebranded UI, in at least EN and KO.
- `grep -ri "ppt master\|ppt-master\|sponsor"` returns only NOTICE/README
  attribution lines.
- Guard and sponsor files gone; `LICENSE` + `NOTICE` correct; MIT.
- Repo size after trim stated in the README; icons strategy stated.
- `gh repo create monomind-ai-lab/lisa-ppt --public` (org confirmed), push
  `main`; a CI smoke test (Python matrix; import the converter; run the
  quality checker on a fixture) on every PR.
- Report which `skill` name and install command Lane B in
  `hi-ted-meet-lisa` should reference.
