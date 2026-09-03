#!/usr/bin/env python3
"""Tests for the Lisa HTML deck importer (lisa_html_intake.py)."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import lisa_html_intake as intake  # noqa: E402


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "lisa_html_intake"
EVIDENCE = FIXTURES / "evidence-deck.sample.html"
PAPER = FIXTURES / "paper-brief.sample.html"
MONOMIND = FIXTURES / "monomind-deck.sample.html"
SYNTH_EVIDENCE = FIXTURES / "synthetic-evidence.html"
SYNTH_MONOMIND = FIXTURES / "synthetic-monomind.html"


def _components(slide: intake.Slide, kind: str) -> list[intake.Component]:
    return [c for c in slide.components if c.type == kind]


def _make_project(root: Path) -> Path:
    """A minimal existing project directory (the importer reuses it as-is)."""
    project = root / "proj"
    (project / "sources").mkdir(parents=True)
    (project / "svg_output").mkdir()
    return project


class FamilyDetectionTests(unittest.TestCase):
    def test_each_sample_resolves_to_its_family(self) -> None:
        for path, family in (
            (EVIDENCE, "evidence-deck"),
            (PAPER, "paper-brief"),
            (MONOMIND, "monomind-deck"),
            (SYNTH_EVIDENCE, "evidence-deck"),
            (SYNTH_MONOMIND, "monomind-deck"),
        ):
            with self.subTest(path=path.name):
                deck = intake.read_deck(path)
                self.assertEqual(deck.family, family)
                self.assertTrue(deck.evidence)
                self.assertTrue(deck.fenced, "fixtures carry the LISA:CONTENT fence")

    def test_document_kind_file_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "doc.html"
            page.write_text(
                '<html lang="en"><body data-lang="en"><section class="page active">'
                "<h1>A web document</h1></section></body></html>",
                encoding="utf-8",
            )
            with self.assertRaises(intake.IntakeError) as ctx:
                intake.read_deck(page)
            self.assertIn("document-kind", str(ctx.exception))

    def test_non_lisa_html_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "plain.html"
            page.write_text("<html><body><p>Hello</p></body></html>", encoding="utf-8")
            with self.assertRaises(intake.IntakeError):
                intake.read_deck(page)


class EvidenceSampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.deck = intake.read_deck(EVIDENCE)

    def test_languages_and_title(self) -> None:
        self.assertEqual(self.deck.languages, ["en", "ko"])
        self.assertEqual(self.deck.primary_language, "en")
        self.assertEqual(self.deck.title["en"], "Hi Ted, Meet Lisa · Many shapes, one system")
        self.assertEqual(self.deck.title["ko"], "Hi Ted, Meet Lisa · 형태는 여럿, 체계는 하나")
        self.assertEqual(len(self.deck.slides), 2)

    def test_cover_slide(self) -> None:
        cover = self.deck.slides[0]
        self.assertEqual(cover.kind, "cover")
        self.assertEqual(cover.label, {"en": "Title", "ko": "표지"})
        self.assertEqual(cover.statement["en"], "Many shapes. One system. Zero installs.")
        self.assertEqual(cover.statement["ko"], "형태는 여럿. 체계는 하나. 설치는 없음.")
        self.assertIn("finished HTML file", cover.lead["en"])
        verdicts = _components(cover, "verdict")
        self.assertEqual(len(verdicts), 1)
        self.assertEqual(verdicts[0].data["text"]["en"], "A template carries the machinery. It never carries the material.")

    def test_table_slide(self) -> None:
        slide = self.deck.slides[1]
        self.assertEqual(slide.kind, "content")
        self.assertEqual(slide.eyebrow["en"], "The registry, as it stands")
        self.assertEqual(slide.statement["en"], "Shape first, subject never")
        self.assertEqual([c.type for c in slide.components], ["table", "paragraph", "verdict"])
        table = slide.components[0].data
        self.assertEqual([h["en"] for h in table["headers"]], ["Template", "How it reads", "Skeleton"])
        self.assertEqual([h["ko"] for h in table["headers"]], ["템플릿", "어떻게 읽히는가", "골격"])
        self.assertEqual(len(table["rows"]), 4)
        self.assertEqual(table["rows"][3]["tone"], "flag")
        self.assertEqual(table["rows"][3]["cells"][0]["en"], "MonoMind deck")
        # A cell written once (a number) reaches both languages.
        self.assertEqual(table["rows"][3]["cells"][2], {"en": "193 KB", "ko": "193 KB"})
        paragraph = slide.components[1].data["text"]["en"]
        self.assertIn("**reading mode**", paragraph)
        self.assertIn("`techdoc`", paragraph)
        self.assertEqual(slide.components[2].data["tone"], "cyan-v")


class PaperBriefSampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.deck = intake.read_deck(PAPER)

    def test_languages(self) -> None:
        self.assertEqual(self.deck.languages, ["zh-TW", "en"])
        self.assertEqual(self.deck.primary_language, "zh-TW")
        self.assertTrue(self.deck.title["zh-TW"].startswith("Lumen Docs"))

    def test_cards_and_decision(self) -> None:
        slide = self.deck.slides[0]
        self.assertEqual(slide.label, {"zh-TW": "兩種算法", "en": "Two readings"})
        cards = _components(slide, "cards")[0].data["items"]
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]["value"], {"zh-TW": "78%", "en": "78%"})
        self.assertEqual(cards[1]["tone"], "bad")
        decision = _components(slide, "decision")[0].data
        self.assertEqual(decision["heading"], {"zh-TW": "建議做法", "en": "Recommendation"})
        self.assertIn("Publish only the sync rate", decision["action"]["en"])

    def test_bar_chart_carries_numbers(self) -> None:
        slide = self.deck.slides[1]
        bars = _components(slide, "bars")[0].data["items"]
        self.assertEqual([b["width_percent"] for b in bars], [92.0, 68.0, 44.0, 22.0, 8.0])
        self.assertEqual([b["tone"] for b in bars], ["blue", "blue", "", "warn", "accent"])
        self.assertEqual(bars[0]["label"]["en"], "Locale A")
        self.assertEqual(bars[0]["value"]["zh-TW"], "6 人")
        self.assertEqual(bars[0]["value"]["en"], "6")

    def test_cjk_line_breaks_do_not_gain_spaces(self) -> None:
        # The statement is written with <br> between CJK characters in the deck.
        for slide in self.deck.slides:
            self.assertNotIn("， ", slide.statement.get("zh-TW", ""))


class MonoMindSampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.deck = intake.read_deck(MONOMIND)

    def test_single_language(self) -> None:
        self.assertEqual(self.deck.languages, ["en"])
        self.assertTrue(self.deck.dark)
        self.assertTrue(any("one language inline" in item for item in self.deck.omitted))

    def test_cover_and_card_grid(self) -> None:
        cover, cards = self.deck.slides
        self.assertEqual(cover.kind, "cover")
        self.assertEqual(cover.label["en"], "Cover")
        self.assertEqual(cover.statement["en"], "The complete guide to Project Context.")
        meta = _components(cover, "meta")[0].data["items"]
        self.assertEqual([m["en"] for m in meta], ["18 pages", "Install · Operate · Extend", "github.com/monomind-ai-lab"])
        self.assertEqual(cards.part["en"], "Part 1 · Why")
        grid = _components(cards, "card_grid")[0].data["items"]
        self.assertEqual([g["number"]["en"] for g in grid], ["Q1", "Q2", "Q3", "Q4"])
        self.assertEqual(grid[0]["title"]["en"], "What is true now?")
        loop = _components(cards, "callout")[0].data
        self.assertEqual(loop["role"], "loop")
        self.assertTrue(loop["text"]["en"].startswith("**Unlike chat history"))


class DesignSpecTokenTests(unittest.TestCase):
    def test_evidence_tokens(self) -> None:
        deck = intake.read_deck(EVIDENCE)
        rows = {role: (hex_value, purpose) for role, hex_value, purpose in intake.color_rows(deck)[0]}
        self.assertEqual(rows["Background"][0], "#141414")
        self.assertEqual(rows["Primary"][0], "#FF5722")
        self.assertIn("`fact`", rows["Primary"][1])
        self.assertIn("`--sig`", rows["Primary"][1])
        self.assertEqual(rows["Secondary accent"][0], "#22D3EE")
        self.assertEqual(rows["Divider"][0], "#2E2E2E")
        fonts = intake.font_plan(deck)
        self.assertEqual(fonts["display"], ["Archivo Black", "sans-serif"])
        self.assertEqual(fonts["body"], ["Space Grotesk", "sans-serif"])
        self.assertEqual(fonts["mono"][0], "JetBrains Mono")
        self.assertIn("Noto Sans KR", fonts["per_language"]["ko"]["--font-body"])

    def test_paper_tokens(self) -> None:
        deck = intake.read_deck(PAPER)
        rows = {role: hex_value for role, hex_value, _ in intake.color_rows(deck)[0]}
        self.assertEqual(rows["Background"], "#FFFFFF")
        self.assertEqual(rows["Primary"], "#FF3300")
        self.assertEqual(rows["Secondary accent"], "#0044FF")
        self.assertEqual(rows["Chapter ground"], "#0D0D0D")
        fonts = intake.font_plan(deck)
        self.assertEqual(fonts["body"][0], "Noto Sans TC")
        self.assertEqual(fonts["english_body"][0], "Archivo")

    def test_monomind_dark_deck_tokens(self) -> None:
        deck = intake.read_deck(MONOMIND)
        rows, omissions = intake.color_rows(deck)
        by_role = {role: hex_value for role, hex_value, _ in rows}
        self.assertEqual(by_role["Background"], "#102033")
        self.assertEqual(by_role["Body text"], "#FFFFFF")
        self.assertEqual(by_role["Accent"], "#4F8CFF")
        self.assertEqual(by_role["Secondary background"], "[fill]")
        self.assertTrue(any("--surface" in item for item in omissions))
        fonts = intake.font_plan(deck)
        self.assertEqual(fonts["display"][0], "Plus Jakarta Sans")

    def test_rendered_spec_shape(self) -> None:
        deck = intake.read_deck(PAPER)
        spec = intake.render_design_spec(deck, "paper_demo", None)
        self.assertTrue(spec.startswith("<!-- ppt-master-schema: design-spec/v1 -->\n# paper_demo - Design Spec"))
        self.assertIn("| Page Count | 2 |", spec)
        self.assertIn("| Primary Language | zh-TW |", spec)
        self.assertIn("| Target Audience | [fill] |", spec)
        self.assertIn("| Background | #FFFFFF | `fact` — `--paper`", spec)
        self.assertIn("- **Title stack**: Archivo, Noto Sans TC, sans-serif", spec)
        for heading in ("## I. Project Information", "## II. Canvas Specification", "## III. Visual Theme",
                        "## IV. Typography System", "## V. Layout Principles", "## VI. Icon Usage Specification",
                        "## VIII. Image Resource List", "## IX. Content Outline", "## X. Speaker Notes Requirements"):
            self.assertIn(heading, spec)
        self.assertIn("#### Slide 01 - 兩種算法", spec)
        self.assertIn("#### Slide 02 - 審閱人力", spec)
        self.assertEqual(spec.count("- **Relationships**: [fill]"), 2)
        self.assertEqual(spec.count("- **Audience move**: [fill]"), 2)
        self.assertIn("(from the deck's decision box)", spec)
        self.assertIn("Bar chart (語系 A = 6 人", spec)
        # Every "[fill" is a placeholder the Strategist resolves; the prose
        # bullet never carries the literal, or validate would flag a
        # completed spec forever.
        source_line = next(line for line in spec.splitlines() if line.startswith("- **Source deck"))
        self.assertNotIn("[fill", source_line)
        for line in spec.splitlines():
            if "[fill" in line:
                self.assertTrue(line.startswith(("| ", "- **", "### Part")), line)

    def test_spec_uses_registered_canvas_when_known(self) -> None:
        deck = intake.read_deck(EVIDENCE)
        canvas = {"id": "ppt169", "name": "PPT 16:9", "dimensions": "1280×720", "viewbox": "0 0 1280 720"}
        spec = intake.render_design_spec(deck, "evidence_demo", canvas)
        self.assertIn("| Canvas Format | PPT 16:9 (1280×720) |", spec)
        self.assertIn("| viewBox | `0 0 1280 720` |", spec)


class BilingualSplitTests(unittest.TestCase):
    def test_primary_and_sibling_files(self) -> None:
        deck = intake.read_deck(EVIDENCE)
        with tempfile.TemporaryDirectory() as tmp:
            project = _make_project(Path(tmp))
            outputs = intake.write_outputs(deck, project, force=False, archive=False)
            names = sorted(path.name for path in outputs)
            self.assertIn("evidence-deck.sample.md", names)
            self.assertIn("evidence-deck.sample.ko.md", names)
            self.assertIn("design_spec.md", names)
            self.assertIn("lisa_intake.json", names)
            self.assertIn("evidence-deck.sample.conversion_profile.json", names)
            en = (project / "sources" / "evidence-deck.sample.md").read_text(encoding="utf-8")
            ko = (project / "sources" / "evidence-deck.sample.ko.md").read_text(encoding="utf-8")
            self.assertIn("## Slide 02 — The registry", en)
            self.assertIn("## Slide 02 — 레지스트리", ko)
            self.assertIn("Shape first, subject never", en)
            self.assertIn("형태가 먼저, 주제는 아님", ko)
            self.assertNotIn("Shape first, subject never", ko)
            self.assertIn("| 193 KB |", en)
            self.assertIn("| 193 KB |", ko)
            self.assertIn("language=ko", ko)
            self.assertIn("`evidence-deck.sample.ko.md` carries `ko`", en)
            profile = json.loads((project / "sources" / "evidence-deck.sample.conversion_profile.json").read_text(encoding="utf-8"))
            self.assertEqual(profile["converter"], "lisa_html_intake.py")
            self.assertEqual(profile["conversion_type"], "lisa-html")

    def test_string_written_once_is_not_invented_in_the_other_language(self) -> None:
        deck = intake.read_deck(SYNTH_EVIDENCE)
        en = intake.render_markdown(deck, "en", "synth")
        ko = intake.render_markdown(deck, "ko", "synth")
        self.assertIn("This sentence was written in English only.", en)
        self.assertNotIn("This sentence was written in English only.", ko)
        self.assertNotIn("written in English only", ko)


class UnknownMarkupTests(unittest.TestCase):
    def test_unknown_element_is_reported_not_typed(self) -> None:
        for path, slide_index in ((SYNTH_EVIDENCE, 4), (SYNTH_MONOMIND, 2)):
            with self.subTest(path=path.name):
                deck = intake.read_deck(path)
                slide = deck.slides[slide_index]
                self.assertIn("div.mystery", slide.unknown)
                self.assertTrue(any("div.mystery" in item for item in deck.omitted))
                unclassified = _components(slide, "unclassified")
                self.assertEqual(len(unclassified), 1)
                self.assertEqual(unclassified[0].data["markup"], "div.mystery")
                self.assertIn("never seen", unclassified[0].data["text"]["en"])
                known = {c.type for c in slide.components} - {"unclassified"}
                self.assertNotIn("div.mystery", str(known))
                markdown = intake.render_markdown(deck, "en", "synth")
                self.assertIn("<!-- unclassified markup: div.mystery -->", markdown)
                summary = intake.render_summary(deck, [], True)
                self.assertIn("unclassified markup `div.mystery`", summary)


class SyntheticCoverageTests(unittest.TestCase):
    def test_evidence_family_components(self) -> None:
        deck = intake.read_deck(SYNTH_EVIDENCE)
        census = intake.component_census(deck)
        for kind in ("section", "table", "cards", "mega", "stat_row", "verdict", "specs",
                     "points", "decision", "bars", "paragraph", "unclassified"):
            self.assertIn(kind, census, kind)
        self.assertEqual(census["verdict"], 3)
        self.assertEqual(deck.slides[1].kind, "section")
        section = _components(deck.slides[1], "section")[0].data
        self.assertEqual(section["number"]["en"], "01")
        self.assertEqual(section["statement"]["en"], "Tables and numbers")
        self.assertEqual(section["lead"]["en"], "The part that argues from data.")
        self.assertEqual(deck.slides[2].part["ko"], "01 · 표와 숫자")
        table = _components(deck.slides[2], "table")[0].data
        self.assertEqual([r["tone"] for r in table["rows"]], ["", "flag", "good"])
        self.assertEqual(table["rows"][0]["cells"][1], {"en": "/etc/alpha", "ko": "/etc/alpha"})
        self.assertEqual(table["rows"][1]["cells"][1]["en"], "**the problem**")
        paragraph = _components(deck.slides[2], "paragraph")[0].data["text"]["en"]
        self.assertEqual(paragraph, "The **load-bearing** phrase, **the alarming part**, and a `path/to/thing`.")
        mega = _components(deck.slides[3], "mega")[0].data
        self.assertEqual(mega["value"]["en"], "3.4×")
        self.assertIn("tracker", mega["note"]["en"])
        stats = _components(deck.slides[3], "stat_row")[0].data["items"]
        self.assertEqual([s["value"]["en"] for s in stats], ["9", "22 KB", "31%", "0"])
        self.assertEqual([s["tone"] for s in stats], ["accent", "warn", "cyan", ""])
        specs = _components(deck.slides[4], "specs")[0].data["items"]
        self.assertEqual(len(specs), 2)
        self.assertEqual(specs[0]["text"]["en"], "Publish the sync rate")
        self.assertEqual(specs[0]["sub"]["en"], "The two differ by 47 points")
        points = _components(deck.slides[4], "points")[0].data["items"]
        self.assertEqual([p["marker"] for p in points], ["Q1", "Q2"])
        self.assertEqual(points[0]["text"]["en"], "**Which shape?** Asked first.")
        bars = _components(deck.slides[4], "bars")[0].data["items"]
        self.assertEqual([b["width_percent"] for b in bars], [88.0, 41.0])
        # The colophon is chrome, never content.
        self.assertNotIn("Made with", intake.render_markdown(deck, "en", "synth"))

    def test_monomind_family_components(self) -> None:
        deck = intake.read_deck(SYNTH_MONOMIND)
        census = intake.component_census(deck)
        for kind in ("meta", "card_grid", "callout", "frame", "arrow", "chips", "tree", "leader_rows",
                     "steps", "workflow", "bullets", "code", "flags", "ordered", "map", "phase_label",
                     "image", "note", "links", "table", "unclassified"):
            self.assertIn(kind, census, kind)
        canvas = deck.slides[2]
        frames = _components(canvas, "frame")
        self.assertEqual(len(frames), 2)
        self.assertEqual(frames[0].data["label"]["en"], "A table in a panel")
        self.assertTrue(frames[0].data["accent"])
        self.assertEqual(frames[0].data["children"][0]["type"], "table")
        self.assertEqual(frames[0].data["children"][0]["data"]["headers"][0]["en"], "File")
        self.assertEqual(frames[0].data["note"]["en"], "Two rows, one key column.")
        self.assertEqual(frames[1].data["text"]["en"], "People & agents — read **NOW.md** to start.")
        chips = frames[1].data["children"][0]
        self.assertEqual(chips["type"], "chips")
        self.assertEqual([c["optional"] for c in chips["data"]["items"]], [False, True])
        tree = _components(canvas, "tree")[0].data["items"]
        self.assertTrue(tree[0]["root"])
        self.assertEqual(tree[1]["children"][0]["name"]["en"], "SKILL.md")
        leaders = _components(canvas, "leader_rows")
        self.assertEqual(len(leaders), 1, "consecutive leader rows merge into one list")
        self.assertEqual(len(leaders[0].data["items"]), 3)
        steps = _components(canvas, "steps")
        self.assertEqual(len(steps), 1)
        self.assertEqual([s["title"]["en"] for s in steps[0].data["items"]], ["Read NOW.md", "Search decisions"])
        workflow = _components(canvas, "workflow")[0].data["rows"][0]
        self.assertEqual(workflow["phase"]["en"], "Install")
        self.assertEqual(workflow["sub"]["en"], "once")
        self.assertEqual(len(workflow["nodes"]), 2)
        code = _components(canvas, "code")[0].data["text"]["en"]
        self.assertEqual(code.splitlines()[0], "Install Project Context using")
        flags = _components(canvas, "flags")[0].data["items"]
        self.assertEqual([f["flag"]["en"] for f in flags], ["--dry-run", "--apply"])
        mapping = _components(canvas, "map")[0].data
        self.assertEqual([h["en"] for h in mapping["headers"]], ["Primary artifacts", "Context files"])
        self.assertEqual(mapping["rows"][1]["right"]["en"], "Lessons")
        callouts = _components(canvas, "callout")
        self.assertEqual([c.data["role"] for c in callouts], ["startbar", "endbar"])
        image = _components(canvas, "image")[0].data
        self.assertEqual((image["width"], image["height"]), (1, 1))
        self.assertEqual(image["file"], "slide03-01.png")
        self.assertEqual(deck.images[0]["alt"], "A one-pixel plate")
        closing = deck.slides[3]
        self.assertEqual(closing.kind, "closing")
        self.assertEqual([l["href"] for l in _components(closing, "links")[0].data["items"]],
                         ["https://example.invalid/repo", "https://example.invalid/license"])

    def test_embedded_image_is_written_and_listed(self) -> None:
        deck = intake.read_deck(SYNTH_MONOMIND)
        with tempfile.TemporaryDirectory() as tmp:
            project = _make_project(Path(tmp))
            intake.write_outputs(deck, project, force=False, archive=False)
            image = project / "sources" / "synthetic-monomind_files" / "slide03-01.png"
            self.assertTrue(image.is_file())
            self.assertEqual(image.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            manifest = json.loads((project / "sources" / "synthetic-monomind_files" / "image_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest[0]["filename"], "slide03-01.png")
            markdown = (project / "sources" / "synthetic-monomind.md").read_text(encoding="utf-8")
            self.assertIn("![A one-pixel plate](synthetic-monomind_files/slide03-01.png)", markdown)
            spec = (project / "design_spec.md").read_text(encoding="utf-8")
            self.assertIn("| slide03-01.png | 1x1 | 1:1 | A one-pixel plate | photo |", spec)


class CliTests(unittest.TestCase):
    def _run(self, argv: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = intake.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = self._run([str(EVIDENCE), "--dry-run"])
            self.assertEqual(code, 0)
            self.assertIn("Dry run: nothing written.", out)
            self.assertIn("family:     evidence-deck", out)
            self.assertIn("Not invented", out)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_dry_run_json(self) -> None:
        code, out, _ = self._run([str(PAPER), "--dry-run", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["schema"], intake.INTAKE_SCHEMA)
        self.assertEqual(payload["family"], "paper-brief")
        self.assertEqual(payload["page_count"], 2)
        self.assertEqual(payload["outputs"], [])

    def test_project_is_created_reused_and_protected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            code, out, err = self._run([str(EVIDENCE), "--project", str(target), "--format", "ppt169"])
            self.assertEqual(code, 0, err)
            created = [p for p in Path(tmp).iterdir() if p.name.startswith("sample_ppt169_")]
            self.assertEqual(len(created), 1, "project_manager.py init names the directory")
            project = created[0]
            self.assertTrue((project / "design_spec.md").is_file())
            self.assertTrue((project / "sources" / "evidence-deck.sample.md").is_file())
            self.assertTrue((project / "sources" / "evidence-deck.sample.html").is_file())
            self.assertIn("| Canvas Format | PPT 16:9 (1280×720) |", (project / "design_spec.md").read_text(encoding="utf-8"))
            self.assertIn("Written:", out)
            # A second run resolves the same project and refuses to clobber the spec.
            code, _, err = self._run([str(EVIDENCE), "--project", str(target)])
            self.assertEqual(code, 1)
            self.assertIn("already exists", err)
            code, _, err = self._run([str(EVIDENCE), "--project", str(target), "--force"])
            self.assertEqual(code, 0, err)

    def test_unsupported_deck_exits_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "plain.html"
            page.write_text("<html><body><p>Hello</p></body></html>", encoding="utf-8")
            code, _, err = self._run([str(page), "--dry-run"])
            self.assertEqual(code, 2)
            self.assertIn("not a Lisa slide deck", err)


if __name__ == "__main__":
    unittest.main()
