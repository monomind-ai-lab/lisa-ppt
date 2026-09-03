# Documentation Index

[English](./README.md) | [Chinese](./zh/README.md)

---

User-facing documentation lives in this directory: English files are the canonical source, with synchronized Chinese translations in [`zh/`](./zh/README.md). Workflow and technical references consumed by the AI itself live under [`skills/lisa-ppt/`](../skills/lisa-ppt/SKILL.md).

## Getting Started

| Document | Description |
|---|---|
| [Getting Started](./getting-started.md) | First deck in 3 steps, plus templates, live preview, animations, narration, voice cloning |
| [Windows Installation](./windows-installation.md) | Step-by-step setup guide for Windows users |
| [FAQ](./faq.md) | Model selection, cost, layout troubleshooting, custom templates — updated from real user reports |

## Capabilities in Depth

| Document | Description |
|---|---|
| [Audio Narration](./audio-narration.md) | Speaker notes to per-slide narration: providers, voice cloning, timing, PPTX embedding |
| [Transitions & Animations](./animations.md) | Default behavior and customization for page transitions and per-element object animations |
| [Templates Guide](./templates-guide.md) | Creating and applying brand / style / layout / deck templates |

## Architecture & Internals

| Document | Description |
|---|---|
| [Technical Design](./technical-design.md) | Architecture, design philosophy, why SVG → DrawingML |
| [PowerPoint–SVG Mapping](./powerpoint-svg-mapping.md) | Feature-by-feature mapping between PowerPoint constructs and the pipeline |
| [Templates Architecture](./templates-architecture.md) | Design of the brand / style / layout / deck template system |

## Project Direction

Lisa's PPT's own direction is [`PLAN.md`](../PLAN.md); its provenance is [`PROVENANCE.md`](./PROVENANCE.md) and the root [`NOTICE`](../NOTICE). The two upstream READMEs and slide-master's Korean README are parked under [`upstream/`](./upstream/) as the record of what was imported (their relative links may not resolve there); upstream's positioning, roadmap and maintainer documents were not carried over.

| Document | Description |
|---|---|
| [Provenance](./PROVENANCE.md) | Import points, every ported file, what was removed, the bundled fonts, and how a backport is recorded |
| [PPT Master README](./upstream/README.ppt-master.md) | The upstream README at v6.1.0, parked for reference |
| [slide-master README (Korean)](./upstream/README.slide-master.ko.md) | The slide-master README at the ported commit, parked for reference |

## Contributor Rules

| Document | Description |
|---|---|
| [Style Rules](./rules/README.md) | Contributor style rules for prompt references and Python scripts |
