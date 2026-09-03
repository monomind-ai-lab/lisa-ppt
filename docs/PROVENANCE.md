# Provenance

The itemised ledger behind [`NOTICE`](../NOTICE): where every imported or
ported file came from, and what was removed. Kept current by hand; a later
backport adds a row here with the upstream commit it came from.

## Import points

| Source | Commit | Date | How |
|---|---|---|---|
| [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) tag `v6.1.0` | `c40bca58e168fcef2facdc7612cc352d1233679b` | 2026-08-31 | Whole tree copied once (`.git` not carried) — commit "Import PPT Master v6.1.0 (c40bca58)" |
| [byungjunjang/slide-master](https://github.com/byungjunjang/slide-master) | `166472bd2a22de9aa9fb6c8cdf8b0cdfc6b698ef` | 2026-08-04 | Contributions ported file by file, one commit each ("Port: …") |

Layout decision: upstream's `skills/<name>/` tree is kept (plugin-friendly,
matches Lisa's own repository), not slide-master's `.claude/skills/`. Codex
discovers the skills through generated stubs under `.codex/skills/`.

## Ported from slide-master

Paths on the right are inside slide-master at commit `166472bd`; paths on the
left are in this repository.

| Here | From slide-master | Notes |
|---|---|---|
| `skills/lisa-ppt/scripts/image_backends/backend_codex.py` | `.claude/skills/ppt-master/scripts/image_backends/backend_codex.py` | usage hint path adapted |
| `skills/lisa-ppt/scripts/image_gen.py` (codex registry entry, unset → codex) | `.claude/skills/ppt-master/scripts/image_gen.py` | bounded diff on the v6.1.0 file |
| `skills/codex-image/{SKILL.md,LICENSE,.gitignore}` | `.claude/skills/codex-image/` | verbatim |
| `skills/lisa-ppt/scripts/svg_to_pptx/pptx_package/cli.py` (`_next_export_version`, `_ver<N>` naming) | `.claude/skills/ppt-master/scripts/svg_to_pptx/pptx_package/cli.py` | upstream's `_native_charts_tables` suffix kept |
| `skills/lisa-ppt/templates/layouts/{academic_defense,ai_ops,government_blue,government_red,medical_university,pixel_retro,psychology_attachment}/` | `.claude/skills/ppt-master/templates/layouts/<same>/` | verbatim; v6.0-era `native_structure_mode: template` contract (see open questions) |
| `skills/lisa-ppt/templates/layouts/layouts_index.json` (7 entries) | `.claude/skills/ppt-master/templates/layouts/layouts_index.json` | merged beside upstream's 7 |
| `skills/lisa-ppt/scripts/confirm_ui/static/catalogs.json` (`*_ko` fields, `instagram` canvas row) | `.claude/skills/ppt-master/scripts/confirm_ui/static/catalogs.json` | merged by option id |
| `skills/lisa-ppt/scripts/confirm_ui/static/app.js` (`ko` dictionary, registration) | `.claude/skills/ppt-master/scripts/confirm_ui/static/app.js` | 113 keys verbatim; `t()` falls back to English |
| `skills/lisa-ppt/scripts/confirm_ui/static/index.html` (한국어 menu item) | `.claude/skills/ppt-master/scripts/confirm_ui/static/index.html` | |
| `skills/lisa-ppt/scripts/svg_editor/static/{app.js,index.html}` (`ko`) | `.claude/skills/ppt-master/scripts/svg_editor/static/{app.js,index.html}` | 73 keys, full coverage |
| `skills/lisa-ppt/assets/fonts/Pretendard/` (6 OTF + `LICENSE.txt`) | `.claude/skills/ppt-master/assets/fonts/Pretendard/` | verbatim |
| `skills/lisa-ppt/assets/fonts/README.md` | `.claude/skills/ppt-master/assets/fonts/README.md` | rewritten as policy |
| `skills/lisa-ppt/scripts/svg_to_pptx/drawingml/utils.py` (`DUAL_SCRIPT_FONTS`, PPT-safe names) | `.claude/skills/ppt-master/scripts/svg_to_pptx/drawingml/utils.py` | six bundled cuts only |
| `AGENTS.md` "Font Policy" | `CLAUDE.md:50-52` | reworded from "on this machine" to repository policy |
| `skills/lisa-ppt/references/strategist.md` §g lock | `.claude/skills/ppt-master/references/strategist.md:193-204` | reworded; doctrine verbatim |
| `skills/lisa-ppt/scripts/install_fonts.py` | — (new) | stdlib installer the policy references |
| `skills/lisa-ppt/scripts/config.py`, `project_utils.py`, `svg_position_calculator.py`, `generate_examples_index.py` (`instagram`) | `.claude/skills/ppt-master/scripts/config.py` | |
| `skills/lisa-ppt/references/canvas-formats.md` (`instagram` rows) | `.claude/skills/ppt-master/references/canvas-formats.md` | type-scale row derived by the section's formula |
| `skills/diagram-design/` (68 files) | `.claude/skills/diagram-design/` | verbatim; one path in the integration note adapted; `references/diagram-onboarding-legacy.md` byte-identical |
| `skills/lisa-ppt/workflows/routing.md`, `SKILL.md` (Korean trigger phrases) | `.claude/skills/ppt-template-fill/SKILL.md` description, `AGENTS.md:29` | native-enhance-pptx / ppt-template-fill themselves are covered by upstream's Edit Native PPTX route and were not vendored |
| `skills/lisa-ppt/scripts/sync_codex_stubs.py`, `.codex/skills/` | `.claude/skills/ppt-master/scripts/sync_codex_stubs.py`, `.codex/skills/_GENERATED.md` | canonical tree `skills/` |
| `skills/lisa-ppt/scripts/preflight.py` | `.claude/skills/ppt-master/scripts/preflight.py` | officecli check dropped (no such path in v6.1.0) |
| `docs/upstream/README.slide-master.ko.md` | `README.md` | verbatim; W2's KO README seed |

## Removed from the imported PPT Master tree

| Path | Why |
|---|---|
| `skills/lisa-ppt/scripts/update_repo.py` (+ references in `requirements.txt`, `docs/faq.md`, `docs/zh/faq.md`, `scripts/README.md`, the parked READMEs) | self-update from upstream; the repository is independent |
| `skills/lisa-ppt/scripts/attribution_guard.py`; `require_skill_integrity()` in `svg_to_pptx.py`, `svg_quality/cli.py`, `register_template.py`, `project_management/cli.py`, `svg_quality_checker.py`, `template_preview_pptx.py`, `project_manager.py`, `svg_to_pptx/pptx_package/cli.py`, `console_encoding.py` (also `_require_official_distribution_identity()`); `metadata.official_repository` / `sponsors` in `SKILL.md` | no runtime guard; attribution is LICENSE + NOTICE |
| `SPONSORING.md`, `SPONSORING_CN.md`, `skills/lisa-ppt/SPONSORS.md`, `SPONSORS_CN.md`, `.github/FUNDING.yml`; affiliate lines in `docs/faq.md`, `docs/zh/faq.md`; sponsor entries in `prompt_audit_manifest.json`; the sponsor rule in `SKILL.md`; sponsor sections in `docs/upstream/README*.ppt-master.md` | sponsor and affiliate material |
| `index.html` | redirect to upstream's examples site |
| `skills/lisa-ppt/templates/brands/{accenture,alibaba,anthropic,aws,bain,bcg,deloitte,google,huawei,ibm,jpmorgan,mckinsey,microsoft,nvidia,pwc,tencent,xiaomi,中国电信,中国电建,中汽研}/` and their `brands_index.json` entries | real corporate identities to the exact hex |
| `skills/lisa-ppt/templates/decks/{中国电信,中汽研}/` and their `decks_index.json` entries | built on those identities |
| `docs/assets/` (33 MB) | trimmed; pointer README |
| `skills/lisa-ppt/references/ai-image-comparison/` (43 MB) | trimmed; pointer README; nothing reads it |
| `skills/lisa-ppt/templates/sounds/{bigsoundbank,kenney-interface,kenney-ui}/` (12 MB) | trimmed; vocabulary, index and notices kept; README says where the files are |

**Removed later, 2026-09-03 — the live preview / SVG editor surface.**
`skills/lisa-ppt/scripts/svg_editor/`, `scripts/check_annotations.py`,
`scripts/docs/svg_editor.md` and `workflows/stages/live-preview.md`, with the
`live_preview/` project directory and the Step 6 auto-startup that drove them.
The deliverable is a `.pptx` and PowerPoint already edits it, so a browser
editor annotating intermediate SVGs was redundant work in the middle of the
pipeline. This does not retract anything recorded above: the port rows,
including the Korean `svg_editor` strings and the credit to upstream PR #85,
stand as the record of what was imported. `scripts/visual_review.py` was made
standalone and kept.

Parked untouched under `docs/upstream/` as the record of what was imported:
`README.ppt-master.md` and `README_CN.ppt-master.md` (sponsor sections
stripped, noted at the top) and `README.slide-master.ko.md`. Their relative
links may not resolve there. Upstream's `why-ppt-master.md`,
`project-positioning.md`, `what-is-ppt.md`, `roadmap.md` (+ `zh/`) and
`MAINTAINER_PLAYBOOK.ppt-master.md` were parked by the import and deleted by
the rebrand: they describe upstream's product direction and maintenance, not
this repository's; the two READMEs and NOTICE carry the attribution.

Repointed to `monomind-ai-lab/lisa-ppt` because the text is about this
repository: the image-search user agent (`LisaPPT/1.0`), `marketplace.json`,
`plugin.json`, the issue templates, `CONTRIBUTING.md`, `SECURITY.md`,
`CODE_OF_CONDUCT.md`, the clone / ZIP / `npx skills add` instructions in
`docs/getting-started.md`, `docs/windows-installation.md`, `docs/faq.md` and
their `zh/` twins. Left as attribution: contributor credits for upstream PR
#85, #155 and #191, and the `consulting-decision` style's source issue.

## Not taken from slide-master

`templates/brands/jangpm`, `templates/decks/jangpm` (the author's personal
brand); the `apple`, `naver`, `naver_ir`, `mckinsey`, `google`, `anthropic`
brand and deck presets; the PackyCode affiliate link in its `docs/faq.md`;
`native-enhance-pptx` and `ppt-template-fill` as separate skills (upstream
v6.1.0's Edit Native PPTX route covers both); the
`Pretendard, "Malgun Gothic", sans-serif` fallback stack as-is (Windows-Korean;
the per-language cross-platform tail is the rebrand's).

## Bundled fonts

Fetched once from the upstream repositories at the commits below; the OFL
text beside each family is the upstream licence file verbatim.

| Here | Source | Files |
|---|---|---|
| `skills/lisa-ppt/assets/fonts/Pretendard/` | slide-master `166472bd` (see above), originally [orioncactus/pretendard](https://github.com/orioncactus/pretendard) v1.3.9 | 6 OTF + `LICENSE.txt` |
| `skills/lisa-ppt/assets/fonts/NotoSansTC/` | [notofonts/noto-cjk](https://github.com/notofonts/noto-cjk) tag `Sans2.004` (`523d033d`), `Sans/SubsetOTF/TC/` | `NotoSansTC-{Light,Regular,Medium,Bold}.otf` + `LICENSE.txt` (repository `LICENSE`) |
| `skills/lisa-ppt/assets/fonts/PlusJakartaSans/` | [tokotype/PlusJakartaSans](https://github.com/tokotype/PlusJakartaSans) `18d1cd2f` (master, 2024-01-18), `fonts/ttf/` | `PlusJakartaSans-{Light,Regular,Medium,SemiBold,Bold,ExtraBold}.ttf` + `LICENSE.txt` (`OFL.txt`) |
| `skills/lisa-ppt/assets/fonts/JetBrainsMono/` | [JetBrains/JetBrainsMono](https://github.com/JetBrains/JetBrainsMono) tag `v2.304` (`cd5227bd`), `fonts/ttf/` | `JetBrainsMono-{Regular,Medium,SemiBold}.ttf` + `LICENSE.txt` (`OFL.txt`) |

## Backports

None yet. A backport is a deliberate, hand-made change from a fresh clone of
the source, reviewed like any other PR, and recorded here as
`<path> ← <source> <commit>`.
