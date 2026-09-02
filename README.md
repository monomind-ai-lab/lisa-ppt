# Lisa's PPT

> **Natively editable PowerPoint for [Hi Ted, Meet Lisa](https://github.com/monomind-ai-lab/hi-ted-meet-lisa).**
> An affiliated feature, served from this repository, installed as a skill.

Hi Ted, Meet Lisa makes one standalone HTML file. Some rooms want a `.pptx`
instead — editable text, native charts and tables, a file that opens in
PowerPoint with nothing else installed. Lisa's PPT is that: a hard fork of
[PPT Master](https://github.com/hugohe3/ppt-master) by Hugo He (MIT),
rebranded and rebuilt to the Ted & Lisa experience, with a route that takes a
finished Lisa deck's content straight into the pipeline.

**Status: the plan is here; the fork is not yet.** [`PLAN.md`](PLAN.md) is
the brief the build follows — fork and licence, rebrand, the intake rebuilt
without losing a feature, the two lanes back to Lisa, and what counts as
done. Nothing in this repository runs until that work lands.

## What it will be

- **Install-only.** Python 3.10+ and `pip install -r requirements.txt`; no
  Node, no LibreOffice. Distributed as a plugin (`/lisa-ppt`) and as a skill.
- **The same intake experience as Lisa**, in Lisa's tokens and shell, in
  English, Korean, Traditional Chinese, Chinese and Japanese — every question
  and receipt the upstream asks, nothing dropped.
- **Two lanes to Lisa.** A registry handoff from `/lisa` for PowerPoint-first
  work, and an importer that reads a Lisa deck's content regions so
  `/lisa-ppt deck.html` yields a matching `.pptx`.
- **Surfaced on [html.monomind.one](https://html.monomind.one)** as an
  affiliated feature, beside the HTML templates.

## Licence

MIT. Upstream attribution is recorded in [`NOTICE`](NOTICE) and joins
[`LICENSE`](LICENSE) when the fork lands.
