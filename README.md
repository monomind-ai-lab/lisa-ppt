# Lisa's PPT

> **Natively editable PowerPoint for [Hi Ted, Meet Lisa](https://github.com/monomind-ai-lab/hi-ted-meet-lisa).**
> An affiliated feature, served from this repository, installed as a skill.
> English · 한국어 · 繁體中文.

Hi Ted, Meet Lisa makes one standalone HTML file. Some rooms want a `.pptx`
instead — editable text, native charts and tables, a file that opens in
PowerPoint with nothing else installed. Lisa's PPT is that.

It is built from [slide-master](https://github.com/byungjunjang/slide-master)
by byungjunjang (MIT), a Korean refinement of
[PPT Master](https://github.com/hugohe3/ppt-master) by Hugo He (MIT): the
same SVG-per-page pipeline and native DrawingML converter, plus what
slide-master added on top — images through Codex's own `image_gen` with no
API key, version-numbered exports, seven Korean-domain layouts, a house-font
doctrine where hierarchy comes from weight and size rather than switching
families, and a Korean confirm UI and README. Lisa's PPT keeps all of that,
rebrands it to the Ted & Lisa experience, and adds English and Traditional
Chinese beside the Korean.

**A hard fork.** The engine is imported once from PPT Master v6.1.0, slide-master's refinements are ported on top, and from then on the repository is independent: nothing is pulled from either source again, and any later backport is a deliberate hand-made change recorded in `NOTICE`.

**Status: the plan is here; the import is not yet.** [`PLAN.md`](PLAN.md) is
the brief the build follows — which tree the engine sits on, licence and
attribution, what has to go before publishing, the rebrand, the intake
rebuilt without losing a feature, the two lanes back to Lisa, and what counts
as done. Nothing in this repository runs until that work lands.

## What it will be

- **Install-only.** Python 3.10+ and `pip install -r requirements.txt`; no
  Node, no LibreOffice. Codex CLI is optional and gives image generation with
  a `codex login`. Distributed as a plugin (`/lisa-ppt`) and as a skill, for
  Claude Code and Codex alike.
- **The same intake experience as Lisa**, in Lisa's tokens and shell, in
  English, Korean and Traditional Chinese first, with the upstream's other
  languages kept where they cost nothing — every question and receipt the
  upstream asks, nothing dropped.
- **One house family per language**, bundled with its licence: Pretendard for
  Korean, Noto Sans TC for Traditional Chinese, and one Latin face for
  English. A deck opened on another machine needs the family installed there;
  the install step says so and does it.
- **Two lanes to Lisa.** A registry handoff from `/lisa` for PowerPoint-first
  work, and an importer that reads a Lisa deck's content regions so
  `/lisa-ppt deck.html` yields a matching `.pptx`.
- **Surfaced on [html.monomind.one](https://html.monomind.one)** as an
  affiliated feature, beside the HTML templates.

## Licence

MIT. The chain — PPT Master, slide-master, the two vendored skills, the
fonts — is recorded in [`NOTICE`](NOTICE) and joins [`LICENSE`](LICENSE) when
the import lands.
