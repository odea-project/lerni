from __future__ import annotations

from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lerni.parser import ParseError, parse_document


class ParserTests(unittest.TestCase):
    def test_parses_representative_deck_fixture(self) -> None:
        source = (REPO_ROOT / "tests" / "fixtures" / "mvp_deck.md").read_text(encoding="utf-8")

        deck = parse_document(source, deck_id="fixture-deck")

        self.assertEqual(deck.deck_id, "fixture-deck")
        self.assertEqual(len(deck.slides), 2)

        first_slide = deck.slides[0]
        self.assertEqual(first_slide.kind, "overview")
        self.assertEqual(first_slide.template, "title-overview")
        self.assertEqual([region.name for region in first_slide.regions], ["title", "explanation", "example"])
        self.assertEqual(first_slide.regions[1].blocks[0].text, "Normalization keeps semantic intent stable across authored source variations.")
        self.assertEqual(first_slide.regions[2].blocks[0].items, ["explicit regions", "explicit reveal groups"])

        second_slide = deck.slides[1]
        self.assertEqual(second_slide.kind, "quiz")
        self.assertEqual(second_slide.template, "quiz-feedback")
        self.assertEqual(len(second_slide.reveal_groups), 1)
        self.assertEqual(second_slide.reveal_groups[0].step, 1)
        self.assertEqual([interaction.kind for interaction in second_slide.interactions], ["question_flow", "guided_reveal"])
        feedback_block = next(region for region in second_slide.regions if region.name == "feedback").blocks[0]
        self.assertEqual(feedback_block.reveal_step, 1)

    def test_rejects_content_before_region(self) -> None:
        source = "# Bad Slide\nThis paragraph is not inside a region."

        with self.assertRaises(ParseError):
            parse_document(source)

    def test_rejects_unclosed_reveal_block(self) -> None:
        source = "# Slide\n::region explanation\n::reveal step=1\nStill open"

        with self.assertRaises(ParseError):
            parse_document(source)

    def test_rejects_duplicate_regions(self) -> None:
        source = "# Slide\n::region explanation\nOne\n::region explanation\nTwo"

        with self.assertRaises(ParseError):
            parse_document(source)

    def test_rejects_unsupported_directive_inside_region(self) -> None:
        source = "# Slide\n::region explanation\n::unknown value=yes"

        with self.assertRaises(ParseError):
            parse_document(source)


if __name__ == "__main__":
    unittest.main()