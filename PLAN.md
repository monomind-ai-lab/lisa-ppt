# Plan — Lisa's PPT

Written 2026-09-02, rewritten 2026-09-03 after the fork target changed. The
build session reads this file and executes it: one branch per workstream,
never on main, subagents doing the work under a lead that reviews.

## What Daren decided

PowerPoint is an **affiliated feature** of Hi Ted, Meet Lisa: surfaced through
the same website (html.monomind.one), served from this repository, distributed
as an **install-only skill**. The fork target is
**[byungjunjang/slide-master](https://github.com/byungjunjang/slide-master)** —
a Korean refinement of hugohe3/ppt-master, chosen for its quality, visual and
workflow-wise — and its Korean copy is a **resource to leverage** for an
audience that speaks English, Korean and Traditional Chinese, not
localization to undo. Keep its capabilities, rebrand it as **Lisa's PPT**,
rebuild its intake UI to the Ted & Lisa brand experience without losing a
feature, and ship it MIT.

## The one decision to confirm before starting

slide-master is a single squashed commit (`166472b`, 2026-08-04) with no
upstream remote and no merge base, on a late-July, v6.0-era upstream. Upstream
(`hugohe3/ppt-master`, v6.1.0, 2026-08-31) has since added the OMML/LaTeX
formula subsystem (8 modules), hyperlink preservation, `canvas_contract.py`,
the `svg_quality/` package refactor (slide-master still runs a 188 KB
single-file checker), `skia-pathops` merge-shapes, `uharfbuzz` shaping,
`templates/styles/`, and a restructured SKILL.md. The two trees are diverging
structurally.

- **Path A — fork the work, not the snapshot (recommended).** Base the engine
  on a fresh clone of upstream v6.1.0 with `upstream` as a remote, and port
  every slide-master contribution (the list below) as its own commit. Future
  upstream fixes are a `git merge`.
- **Path B — fork the snapshot.** Import slide-master as-is and hand-port
  upstream's v6.1 modules into it. Faster to start; a manual-merge tax that
  grows.

The plan below is written for A; every step also works under B with W1
adjusted. **Daren confirms A or B; nothing else waits on it.**

## What Lisa's PPT keeps from slide-master (verified from source)

| Contribution | Where in slide-master |
| --- | --- |
| Codex-OAuth image backend as the zero-config default: `codex exec` → built-in `image_gen` (gpt-image-2), no API key; `IMAGE_BACKEND` unset falls back to it | `scripts/image_backends/backend_codex.py`, `scripts/image_gen.py:334` |
| The gpt-image-2 transparency workaround (the model paints a checkerboard when asked for transparency): prompt rewrite + hard rule + honest guidance | `.claude/skills/codex-image/SKILL.md` step 2.5, `backend_codex.py:81` |
| Version-numbered exports `exports/<title>_ver<N>.pptx` (+ `_native_charts`, `_narrated`), auto-incrementing | `SKILL.md:789–794` |
| Seven Korean-domain layouts: `academic_defense`, `government_blue`, `government_red`, `medical_university`, `psychology_attachment`, `ai_ops`, `pixel_retro` | `templates/layouts/` |
| Korean confirm-UI and live-editor strings; Korean router triggers | `scripts/confirm_ui/static/{catalogs.json,app.js}`, `scripts/svg_editor/static/app.js`, `ppt-template-fill/SKILL.md` |
| Korean README (the seed of the KO README) | `README.md` |
| The house-font lock as a pattern: declared once in `CLAUDE.md`, enforced in `references/strategist.md`, exempted from the "≥3 candidates" rule, hierarchy by weight/size/tracking/colour never by family; converter registers the family for Latin and East-Asian slots | `CLAUDE.md:50–52`, `references/strategist.md:193–204`, `scripts/svg_to_pptx/drawingml/theme_fonts.py` |
| `instagram` 1080×1350 canvas | `references/canvas-formats.md`, `scripts/config.py` |
| Vendoring pattern for `diagram-design`: integration note disables the upstream standalone flow; disabled text kept verbatim in `references/diagram-onboarding-legacy.md` as a provenance record | `.claude/skills/diagram-design/` |
| Dual-host stub sync: `.claude/skills` canonical → `.codex/skills` stubs (`sync_codex_stubs.py`, `preflight.py` fails when stale) | `.codex/skills/_GENERATED.md` |
| `docs/rules/` prompt-style and code-style (prescriptive, not descriptive) | `docs/rules/` |
| The five-skill split: `ppt-master`, `codex-image`, `diagram-design`, `native-enhance-pptx`, `ppt-template-fill` | `.claude/skills/` |

The full analysis, including what is behind upstream and what was verified,
is the study kept in the Lisa workspace (`slide-master-study-2026-09-03.md`).

## What must change before publishing under monomind-ai-lab

1. `docs/faq.md:170` — a live affiliate link (PackyCode, `aff=ppt-master`). Delete.
2. `templates/brands/jangpm`, `templates/decks/jangpm` — the author's personal brand, a 164 KB character image committed twice, registered in both indexes. Remove, and unregister.
3. `apple`, `naver`/`naver_ir`, `mckinsey`, `google`, `anthropic` brand and deck presets — real corporate identities to the exact hex. A named-org repo does not ship these. Remove; keep the mechanism and the seven layouts; add `brands/monomind`.
4. The attribution guard is gone while upstream's LICENSE is kept. Lisa's PPT carries no runtime guard; NOTICE says so, and the licence chain is the attribution.
5. Add `Copyright (c) 2026 MonoMind AI Lab` to LICENSE for the new work; keep Hugo He's line; credit slide-master by name, URL and imported commit (it asserts no line of its own).
6. ~15 upstream-pointing URLs in `docs/` and two scripts (`scripts/image_sources/provider_common.py:44` user agent, `scripts/update_repo.py:54` clone URL) — repoint or remove.
7. "On this machine" wording in `references/strategist.md` and `CLAUDE.md` — a single-user assumption; nothing installs the bundled fonts for a fresh cloner, and the prompt claims nine weights where six are bundled. Reword to policy; add a font-install step; bundle exactly the weights the prompts may name.
8. `formula_policy` in the confirm-UI catalog while the formula modules are absent (moot under Path A): runtime check.
9. Fallback stack `Pretendard, "Malgun Gothic", sans-serif` is Windows-Korean; give every language a cross-platform stack.
10. `.gitattributes` and `.gitignore` reference the author's local tooling; tidy.

## Workstreams (one branch each, one subagent each)

### W1 · Import, licence, attribution
1. Add remotes: `upstream` (hugohe3/ppt-master) and `slidemaster`
   (byungjunjang/slide-master); fetch both. **Path A:** bring in upstream
   `main` at v6.1.0 as the base branch, then port each contribution in the
   table above as one commit, named for what it ports and citing the
   slide-master file it came from. **Path B:** import slide-master's tree, then
   port the missing upstream modules named above. Either way, record both
   imported commits in NOTICE.
2. LICENSE and NOTICE as in the bootstrap, filled in; the vendored skills keep
   their own licence files; font licences beside the font files.
3. Apply "What must change" items 1–10; grep for `jangpm`, `packy`,
   `hugohe3`, `aff=`, and each removed brand until clean.
4. Trim: `templates/icons/` is 47 MB of 11,801 SVGs — keep, but state the
   size and consider a release-asset download for the plugin path; drop
   `references/ai-image-comparison/` (keep a pointer); no example projects
   (already true).
5. Verify the pipeline runs end to end on this machine after the cut. Python
   here is 3.14 — check that `skia-pathops` and `uharfbuzz` have wheels; if
   not, document the supported range.

### W2 · Rebrand
- Names: "PPT Master" and "Slide Master" → **Lisa's PPT**; the skill
  directory `ppt-master` → `lisa-ppt`; command `/lisa-ppt`; keep the other
  four skill names. Add `.claude-plugin/plugin.json` and `marketplace.json`
  mirroring `hi-ted-meet-lisa`'s, plus `.codex-plugin/`; keep the
  `.codex/skills` stubs and the sync script.
- README in three languages: **KO** from slide-master's README (its register
  is the model — honest, concrete, no adjectives doing sales work), **EN**
  written in Lisa's voice, **ZH-TW** translated from the EN. Same install
  shapes as Lisa: plugin marketplace, `npx skills add`, clone.
- Every prose reference to the old names in `workflows/`, `references/`,
  `stages/`, `scripts/docs/` — grep and replace; keep the attribution lines.
- House entries: `brands/monomind/templates/design_spec.md` (MonoMind
  tokens: ink `#102033`, page `#eef6ff`, accent `#4f8cff`; every colour with a
  `fact`/`approx` provenance mark) and `styles/` or `decks/` entries mirroring
  Lisa's `evidence-deck` (argue from numbers) and `paper-brief` (chaptered
  briefing). Register them with `register_template.py`.
- Fonts: the lock becomes **one house family per language** — Pretendard
  (KO), Noto Sans TC (ZH-TW), one Latin face for EN (Pretendard's Latin keeps
  one family per deck; Plus Jakarta Sans matches Lisa) — bundled with their
  OFL texts, weights named in the prompts exactly as bundled, converter
  registered for both slots, an install step in the README, and the rule kept
  verbatim: hierarchy through weight, size, tracking and colour, never by
  switching families.

### W3 · Intake UI rebuilt to the Ted & Lisa experience — nothing lost
Keep, unchanged: the three-stage flow (direction → design system →
images/execute), every question and option in `catalogs.json`, the receipts
model and file ownership, the bundled design directions, the daemon/wait/
shutdown CLI, live preview with click annotations.

Change:
1. **Languages:** EN, KO and ZH-TW first-class — restore `zh-TW` from
   upstream's dictionary (slide-master swapped it out for `ko`), keep
   slide-master's `ko`, keep `zh` and `ja` where they cost nothing. Lisa's
   rule (D-030): the UI language never reaches the payload; an answer is the
   same id in every language.
2. **Tokens and type** in `style.css` from Lisa's intake panel — deep ink,
   page `#eef6ff`, accent `#4f8cff`, Plus Jakarta Sans, JetBrains Mono for
   ids, Noto Sans KR/TC for CJK. Take the values from
   `monomind-ai-lab/hi-ted-meet-lisa` → `assets/tedandlisa-intake.html`.
3. **Shell:** Lisa's fixed-height app shell with a left rail (D-029) and
   chaptered screens (D-028); output-configuration answers last (D-042).
4. **Gallery cards** for brands/layouts/decks in Lisa's card grammar; the SVG
   previews become the thumbnails.
5. **Copy** in Lisa's register; the figures and the MonoMind mark; the
   "Made with Hi Ted, Meet Lisa" colophon.
6. **Receipt display** shows the ids, like Lisa's Copy JSON fallback.
7. No web mode: install-only.
Verify at 1280 and 375 px, in EN/KO/ZH-TW, both stages, one full round trip
that produces `result.json`.

### W4 · The two Lisa lanes
- **Lane B — handoff from Lisa** (in `hi-ted-meet-lisa`, after this repo
  works): registry entry `{ id: "lisa-ppt", kind: "external", type:
  "present", skill: "/lisa-ppt", requires: "Lisa's PPT plugin", badge:
  "PPTX" }`; the handoff passes Lisa's brief and `answers.contract` as the
  Stage-1 contract and selects `brands/monomind`.
- **Lane A — a Lisa HTML deck to PPTX** (here): `scripts/lisa_html_intake.py`
  reads a Lisa file's `LISA:CONTENT-START/END` fences (eyebrow, statement,
  lead, `dg-canvas` components as named in Lisa's `references/slide-patterns*.md`)
  into the project's source Markdown and a pre-filled `design_spec.md` from
  the file's token block, so `/lisa-ppt deck.html` yields a matching PPTX.

### W5 · Website surface (in `monomind-ai-lab/ted-and-lisa`, after the push)
One appended gallery card — "Lisa's PPT · PPTX · install-only" — linking
here; one line in `site/llms.txt`. Append, never insert (D-035); no second
paid surface (D-025).

### W6 · Staying in step
Two upstreams. Under Path A, `git merge upstream/main` on a schedule and a
NOTICE ledger of what was ported from slide-master; under Path B, a ledger of
upstream modules ported by hand. Either way, a monthly check that both
upstreams' HEADs are recorded.

## Acceptance
- End-to-end run on this machine from a one-paragraph brief to an opened
  `.pptx`, with the rebranded UI, in EN, KO and ZH-TW.
- `grep -ri "ppt master\|ppt-master\|slide master\|jangpm\|packy\|aff="` returns
  only NOTICE/README attribution lines.
- LICENSE and NOTICE carry the full chain; no guard; fonts with OFL texts.
- Repository size stated in the README; icons strategy stated.
- CI smoke on every PR: Python matrix, import the converter, run the quality
  checker on a fixture, run the stub-sync check.
- Report which `skill` name and install command Lane B in `hi-ted-meet-lisa`
  should reference.
