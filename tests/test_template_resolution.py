from __future__ import annotations

from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lerni.parser import parse_document
from lerni.template_resolution import TemplateResolutionError, resolve_deck_templates, resolve_slide_template


class TemplateResolutionTests(unittest.TestCase):
    def test_resolves_representative_fixture_deck(self) -> None:
        source = (REPO_ROOT / "tests" / "fixtures" / "mvp_deck.md").read_text(encoding="utf-8")

        deck = parse_document(source, deck_id="fixture-deck")
        resolved_slides = resolve_deck_templates(deck)

        self.assertEqual([slide.template_id for slide in resolved_slides], ["title-overview", "quiz-feedback"])
        self.assertEqual(sorted(resolved_slides[0].slot_bindings.keys()), ["example", "explanation", "title"])
        self.assertEqual(sorted(resolved_slides[1].slot_bindings.keys()), ["answer_choices", "feedback", "question", "title"])
        self.assertEqual([interaction.kind for interaction in resolved_slides[1].interactions], ["question_flow", "guided_reveal"])

    def test_defaults_template_from_slide_kind(self) -> None:
        source = (REPO_ROOT / "tests" / "fixtures" / "overview_without_explicit_template.md").read_text(
            encoding="utf-8"
        )

        deck = parse_document(source)
        resolved_slide = resolve_slide_template(deck.slides[0])

        self.assertEqual(resolved_slide.template_id, "title-overview")
        self.assertEqual(resolved_slide.omitted_optional_slots, ["example"])

    def test_rejects_missing_required_slot(self) -> None:
        source = "::slide kind=overview template=title-overview\n# Missing Explanation"

        deck = parse_document(source)

        with self.assertRaises(TemplateResolutionError) as context:
            resolve_slide_template(deck.slides[0])

        self.assertEqual([issue.code for issue in context.exception.issues], ["missing_required_slot"])
        self.assertEqual(context.exception.issues[0].slot_name, "explanation")

    def test_rejects_unsupported_extra_region(self) -> None:
        source = (
            "::slide kind=overview template=title-overview\n"
            "# Extra Region\n"
            "::region explanation\n"
            "Supported explanation.\n"
            "::region question\n"
            "This region does not belong here."
        )

        deck = parse_document(source)

        with self.assertRaises(TemplateResolutionError) as context:
            resolve_slide_template(deck.slides[0])

        self.assertEqual([issue.code for issue in context.exception.issues], ["unsupported_region"])
        self.assertEqual(context.exception.issues[0].region_name, "question")

    def test_rejects_incompatible_block_kind(self) -> None:
        source = (
            "::slide kind=quiz template=quiz-feedback\n"
            "# Bad Quiz\n"
            "::region question\n"
            "Which region must be a list?\n"
            "::region answer_choices\n"
            "This should have been written as a list.\n"
            "::region feedback\n"
            "Use a list block for answer choices."
        )

        deck = parse_document(source)

        with self.assertRaises(TemplateResolutionError) as context:
            resolve_slide_template(deck.slides[0])

        self.assertEqual([issue.code for issue in context.exception.issues], ["incompatible_block_kind"])
        self.assertEqual(context.exception.issues[0].slot_name, "answer_choices")

    def test_rejects_empty_region_for_required_slot(self) -> None:
        source = (
            "::slide kind=overview template=title-overview\n"
            "# Empty Explanation\n"
            "::region explanation\n"
            "\n"
            "::region example\n"
            "A non-empty optional region does not rescue an empty required slot."
        )

        deck = parse_document(source)

        with self.assertRaises(TemplateResolutionError) as context:
            resolve_slide_template(deck.slides[0])

        self.assertEqual([issue.code for issue in context.exception.issues], ["empty_slot_region"])
        self.assertEqual(context.exception.issues[0].slot_name, "explanation")


if __name__ == "__main__":
    unittest.main()