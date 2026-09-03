# AGENTS.md

This file is the project entry point for general AI agents.

**You MUST read [`skills/lisa-ppt/SKILL.md`](skills/lisa-ppt/SKILL.md) before any PPT generation task or repo modification.** It owns global execution discipline and points to the route selector; after routing, the selected runtime authority owns its steps, gates, and commands.

**Repository execution anchor**: resolve the absolute repository root from this
file's supplied path and retain the absolute `skills/lisa-ppt` root before the
first command. Paths in this file are repository-relative notation only; invoke
them through those absolute roots, retain the absolute project path returned by
initialization, and never issue `cd skills/lisa-ppt` or `cd projects/...`.
When parsing machine-readable stdout, keep stderr separate and never place
`2>&1` upstream of a JSON or XML parser. Invoke each such command once per
concrete argument set; never encode its executable or flag list in scalar shell
strings, batch it through a shell loop, or add a downstream parser when the
command provides a compact view.

## Project Overview

Lisa's PPT turns source material into natively editable DrawingML PPTX. Generate has two mutually exclusive runtimes: Default Strategist → Image_Generator → Executor, and self-contained Quick without separate strategy/confirmation. Beautify selects from explicit Quick intent; Image to PPTX always uses Quick.

**Route selection authority**: [`skills/lisa-ppt/workflows/routing.md`](skills/lisa-ppt/workflows/routing.md) owns the three top-level artifact routes: Generate PPTX, Create Template, and Edit Native PPTX. Child workflows, profiles, stages, and governance documents refine one selected route; they are not competing top-level routes.

- Topic-only or fact-insufficient inputs run [`topic-research`](skills/lisa-ppt/workflows/stages/topic-research.md) inside the selected Generate profile's source intake; its facts URLs are not auto-expanded. After normal image search fails, one relevant webpage may be fetched as a source package and only reviewed selections enter the runtime image pool.
- Default Generate prepares template candidates internally in Step 3, then confirms the communication contract and free-design/template choice together in Stage 1. Template content stays unread until that confirmation; selected roots are installed before template-aware Stage 2. Quick skips this interaction.
- Raw PPTX template plus new material/topic routes to [`edit-native-pptx`](skills/lisa-ppt/workflows/edit-native-pptx.md): a `pptx_to_svg.py --roundtrip` workspace where unchanged pages are referenced byte-for-byte and only planned pages are edited; it never enters Generate.
- Raw PPTX cannot be consumed as a Generate template workspace; run [`create-template`](skills/lisa-ppt/workflows/create-template.md) first and return with the generated workspace root as a Stage-1 candidate. Never add Master/Layout structure directly to an existing PPTX/SVG; generate new structured SVG pages from the workspace.
- Explicit quick/fast or skip-strategy generation uses [`quick-generate`](skills/lisa-ppt/workflows/profiles/quick-generate.md): prepare sources/resources as needed, decide without interaction, omit Strategist/confirmation/spec/lock, hand-author `svg_output/`, pass its lockless final checker, and export.
- Recorded, self-running, or video-directed Generate work conditionally loads [`video-design`](skills/lisa-ppt/references/video-design.md) inside the selected Default or explicit Quick runtime before page planning. It changes scene, script, and motion design—not the runtime/profile or artifact route.
- PPTX beautify is a strict 1:1 Generate [`profile`](skills/lisa-ppt/workflows/profiles/beautify-pptx.md), not a separate route. Explicit Quick intent uses the Quick runtime; otherwise it uses Default. Any split/merge/drop/reorder disables Beautify and returns to ordinary Generate in the selected runtime.
- Page-image reconstruction uses the Codex-supported, Quick-only [`image-to-pptx`](skills/lisa-ppt/workflows/profiles/image-to-pptx.md) profile. Normalize input page frames; one frame becomes one slide. Restore text natively, reconstruct low-resolution graphics without changing identity, and derive registered clean-base/scene layers. Padded-bbox-disjoint objects may share a generated plate and become independent crops. Never use a full-slide screenshot skin. Other hosts are unsupported.
- Finished PPTX notes / narration / timings / transitions with visible slides untouched also use [`edit-native-pptx`](skills/lisa-ppt/workflows/edit-native-pptx.md); export must report `rebuilt=0`.
- [`visual-review`](skills/lisa-ppt/workflows/stages/visual-review.md), [`customize-animations`](skills/lisa-ppt/workflows/stages/customize-animations.md), and [`generate-audio`](skills/lisa-ppt/workflows/stages/generate-audio.md) are supporting stages; their trigger rules remain explicit/conditional.

## Execution Requirements

- For any `brand`, `style`, `layout`, or `deck` workspace creation from PPTX/SVG, images/PDFs, documents/websites, brand assets, direct text, or mixed references, enter [`skills/lisa-ppt/workflows/create-template.md`](skills/lisa-ppt/workflows/create-template.md); it keeps the fixed Create Template name and dispatches exactly one of [`create-brand`](skills/lisa-ppt/workflows/create-template/create-brand.md), [`create-style`](skills/lisa-ppt/workflows/create-template/create-style.md), [`create-layout`](skills/lisa-ppt/workflows/create-template/create-layout.md), or [`create-deck`](skills/lisa-ppt/workflows/create-template/create-deck.md).
- Always-on SVG constraints and shared visual-quality defaults live in [`skills/lisa-ppt/references/shared-standards-core.md`](skills/lisa-ppt/references/shared-standards-core.md). Default and Quick Generate load [`svg-effects.md`](skills/lisa-ppt/references/svg-effects.md) on the executor-base routing trigger (the everyday effects live in the executor core); other routes load it, [`native-data-interface.md`](skills/lisa-ppt/references/native-data-interface.md), and [`pptx-structure-interface.md`](skills/lisa-ppt/references/pptx-structure-interface.md) only when their documented execution triggers apply.
- Canvas choices live in [`skills/lisa-ppt/references/canvas-formats.md`](skills/lisa-ppt/references/canvas-formats.md).
- Icon library details live in [`skills/lisa-ppt/templates/icons/README.md`](skills/lisa-ppt/templates/icons/README.md).

## Font Policy (one house family per language)

- **One house family per language, bundled** (SIL OFL 1.1, licence text beside the files) under [`skills/lisa-ppt/assets/fonts/`](skills/lisa-ppt/assets/fonts/): **Pretendard** for Korean (Light 300, Regular 400, Medium 500, SemiBold 600, Bold 700, ExtraBold 800), **Noto Sans TC** for Traditional Chinese (Light 300, Regular 400, Medium 500, Bold 700), **Plus Jakarta Sans** for English (Light 300, Regular 400, Medium 500, SemiBold 600, Bold 700, ExtraBold 800), and **JetBrains Mono** for ids and code in any language (Regular 400, Medium 500, SemiBold 600). Prompts, specs and locks may name only these weights; no other cut of any family exists in this repository.
- **Author it as** the plain family name with `font-weight` 400 / 700, and every other cut as its own family name at normal weight — `"Pretendard Light"`, `"Noto Sans TC Medium"`, `"Plus Jakarta Sans SemiBold"`, `"JetBrains Mono Medium"`; the full table is in [`assets/fonts/README.md`](skills/lisa-ppt/assets/fonts/README.md). The converter writes Pretendard and Noto Sans TC into both the Latin and East-Asian typeface slots (`DUAL_SCRIPT_FONTS` in [`scripts/svg_to_pptx/drawingml/utils.py`](skills/lisa-ppt/scripts/svg_to_pptx/drawingml/utils.py)), so mixed runs stay in one family; Plus Jakarta Sans and JetBrains Mono fill the Latin slot, and an English deck that needs a CJK companion names it after the Latin face.
- **A deck is set in the family of its language.** The other families are companions for a foreign word or an id, never a second voice. **Hierarchy through weight, size, tracking and colour, never by switching families.** Every SVG-authored deck uses its house family as its fixed stack unless the user names another face in the current conversation or a selected template declares its own; Strategist presents one weight-role plan and size ramp, not alternative families ([`strategist.md` §g](skills/lisa-ppt/references/strategist.md)). Direct-PPTX routes preserve source fonts.
- **Cross-platform fallback stacks**, one per language, for browser preview and for a machine that has not run the installer: Korean `Pretendard, "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", sans-serif`; Traditional Chinese `"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", "Noto Sans CJK TC", sans-serif`; English `"Plus Jakarta Sans", "Segoe UI", "Helvetica Neue", Arial, sans-serif`; ids and code `"JetBrains Mono", Menlo, Consolas, monospace`. The tail is never exported.
- **Install them wherever decks are authored or opened**: `python3 skills/lisa-ppt/scripts/install_fonts.py` (user-level on macOS, Windows and Linux; `--dry-run` shows the plan, `--check` reports, `--family` narrows). `preflight.py` warns when a bundled family is missing. PPTX does not embed fonts; a deck shared to a machine without its family falls back to a system face — record "requires <family>" in the Design Spec when a deck will travel.

## Required Conventions

- **Repo-wide style rules** — when editing prompt files under [`skills/lisa-ppt/references/`](skills/lisa-ppt/references/), Python under [`skills/lisa-ppt/scripts/`](skills/lisa-ppt/scripts/), or any other code/prose in the repo, follow the matching style rule in [`docs/rules/`](docs/rules/).
- **Prompt content layers** — follow [`docs/rules/prompt-layers.md`](docs/rules/prompt-layers.md): a prompt file holds craft (design judgment) and the minimal contract the model writes; enforced grammar, importer behavior, and restated procedure live in [`scripts/docs/`](skills/lisa-ppt/scripts/docs/), one owner per rule with pointers elsewhere.
- **Prompt decision ownership** — follow [`docs/rules/prompt-style.md`](docs/rules/prompt-style.md) §4.1. Default Strategist prepares project-local resources and Executor realizes them; Quick's current agent decides and prepares before SVG authoring. This is not downstream acquisition. Every project icon is prepared material; `icons.inventory` indexes the default plan's curated bundled pool, not page usage or an execution whitelist. Sounds follow [`animations.md`](skills/lisa-ppt/references/animations.md) §2.2.
- **Markdown language consistency** — follow [`docs/rules/language.md`](docs/rules/language.md): one language per file, mirroring the siblings in that directory; a non-English string may appear in an English file only as quoted content (user trigger text, sample values, rendered labels, proper nouns), never as the wording of a rule; never hard-code which language the model replies in. Chat replies are unaffected.

## Compatibility Boundary

- This repository is a workflow/skill package, not an app or service scaffold.
- Do NOT assume generic-project conventions like `.worktrees/`, `tests/`, or mandatory branch setup unless the user explicitly requests them.
- On conflict with a generic coding skill, prioritize [`skills/lisa-ppt/SKILL.md`](skills/lisa-ppt/SKILL.md) inside this repository.

## Command Quick Reference

Convenience summary only — route selection starts in [`SKILL.md`](skills/lisa-ppt/SKILL.md). Image to PPTX always uses [`quick-generate.md`](skills/lisa-ppt/workflows/profiles/quick-generate.md); Beautify uses it only when Quick is explicit, otherwise [`generate-pptx.md`](skills/lisa-ppt/workflows/generate-pptx.md).

```bash
python3 skills/lisa-ppt/scripts/preflight.py [--needs-images]                     # once per session: deps, house font, Codex stubs
python3 skills/lisa-ppt/scripts/source_to_md.py <file_or_URL_or_dir> [...]          # source conversion
python3 skills/lisa-ppt/scripts/project_manager.py init <project_name>              # --format only for an exact registered canvas
python3 skills/lisa-ppt/scripts/project_manager.py import-sources <project_path> <sources...>
python3 skills/lisa-ppt/scripts/project_manager.py validate <project_path>
python3 skills/lisa-ppt/scripts/icon_sync.py <project_path> <lib/name> [...]        # missing names -> non-zero = re-pick
python3 skills/lisa-ppt/scripts/confirm_ui/server.py <project_path> --daemon        # then --wait-only --wait-stage stage1
python3 skills/lisa-ppt/scripts/analyze_images.py <project_path>/images
python3 skills/lisa-ppt/scripts/image_gen.py --manifest <project_path>/images/image_prompts.json   # in-pipeline AI images, even for 1
python3 skills/lisa-ppt/scripts/svg_quality_checker.py <project_path> --canonical-authoring
python3 skills/lisa-ppt/scripts/pptx_to_svg.py <source.pptx> -o projects/<slug>_<YYYYMMDD> --inheritance-mode both --roundtrip   # Edit Native PPTX
python3 skills/lisa-ppt/scripts/svg_to_pptx.py projects/<slug>_<YYYYMMDD> --roundtrip
```

Every other command (sound sync, slicing, template materialization and preview, animation config, authoring-view refresh) is listed by the route or stage that owns it and in [`svg-pipeline.md`](skills/lisa-ppt/scripts/docs/svg-pipeline.md).

For Generate PPTX serial post-processing and export, follow [`generate-pptx.md`](skills/lisa-ppt/workflows/generate-pptx.md) Step 7 exactly; Edit Native PPTX exports through its own §7. See [`svg-pipeline.md`](skills/lisa-ppt/scripts/docs/svg-pipeline.md) for tool flags and behavior.

## Core Directories

- `skills/lisa-ppt/SKILL.md` — global discipline and route-entry authority.
- `skills/lisa-ppt/workflows/generate-pptx.md` — Generate PPTX Step 1–7 authority.
- `skills/lisa-ppt/references/` — role cores plus conditionally loaded role and technical modules.
- `skills/lisa-ppt/scripts/` — runnable tool scripts.
- `skills/lisa-ppt/scripts/docs/` — topic-focused script docs.
- `skills/lisa-ppt/templates/` — layout templates, chart templates, icon library, brand presets.
- `skills/lisa-ppt/workflows/` — top-level route authorities plus supporting child workflows, profiles, stages, and governance runbooks.
- `docs/` — user-facing documentation (FAQ, installation, technical design, templates guide, audio narration).
- `docs/rules/` — repo-wide style rules.
- `projects/` — user project workspace.
