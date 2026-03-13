from __future__ import annotations

from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lerni.document_model import Block, InteractionReference
from lerni.interaction_runtime import InteractionRuntimeError, create_slide_runtime
from lerni.parser import parse_document
from lerni.template_resolution import ResolvedSlot, ResolvedTemplateSlide, resolve_deck_templates


class InteractionRuntimeTests(unittest.TestCase):
    def test_initial_quiz_snapshot_hides_feedback_until_revealed(self) -> None:
        runtime = self._build_quiz_runtime_from_fixture()

        snapshot = runtime.snapshot()

        self.assertEqual(snapshot.active_mode, "question")
        self.assertTrue(snapshot.can_advance_reveal)
        self.assertFalse(snapshot.feedback_visible)
        self.assertEqual(snapshot.current_reveal_step, 0)
        self.assertEqual(snapshot.slot_visibility["feedback"].visible_block_ids, [])
        self.assertEqual(snapshot.slot_visibility["feedback"].hidden_block_ids, ["slide-2-feedback-1"])

    def test_answer_selection_then_feedback_reveal_exposes_feedback_for_browser_consumers(self) -> None:
        runtime = self._build_quiz_runtime_from_fixture()

        runtime.select_answer(1)
        snapshot = runtime.reveal_feedback()

        self.assertEqual(snapshot.selected_answer_index, 1)
        self.assertTrue(snapshot.feedback_visible)
        self.assertEqual(snapshot.active_mode, "feedback")
        self.assertEqual(snapshot.current_reveal_step, 1)
        self.assertEqual(snapshot.slot_visibility["feedback"].visible_block_ids, ["slide-2-feedback-1"])

    def test_rejects_invalid_answer_selection(self) -> None:
        runtime = self._build_quiz_runtime_from_fixture()

        with self.assertRaises(InteractionRuntimeError) as context:
            runtime.select_answer(5)

        self.assertEqual(context.exception.code, "invalid_answer_selection")

    def test_rejects_feedback_reveal_before_answer_selection(self) -> None:
        runtime = self._build_quiz_runtime_from_fixture()

        with self.assertRaises(InteractionRuntimeError) as context:
            runtime.reveal_feedback()

        self.assertEqual(context.exception.code, "feedback_requires_answer")

    def test_reset_clears_reveal_and_feedback_state(self) -> None:
        runtime = self._build_quiz_runtime_from_fixture()

        runtime.select_answer(0)
        runtime.reveal_feedback()
        snapshot = runtime.reset()

        self.assertEqual(snapshot.current_reveal_step, 0)
        self.assertIsNone(snapshot.selected_answer_index)
        self.assertFalse(snapshot.feedback_visible)
        self.assertEqual(snapshot.active_mode, "question")
        self.assertEqual(snapshot.slot_visibility["feedback"].visible_block_ids, [])

    def test_rejects_unsupported_interaction_kind(self) -> None:
        resolved_slide = ResolvedTemplateSlide(
            slide_id="slide-x",
            template_id="title-overview",
            slide_kind="overview",
            slot_bindings={
                "title": ResolvedSlot(
                    slot_name="title",
                    region_name="title",
                    blocks=[Block(block_id="slide-x-title-1", kind="heading", text="Unsupported")],
                ),
                "explanation": ResolvedSlot(
                    slot_name="explanation",
                    region_name="explanation",
                    blocks=[Block(block_id="slide-x-explanation-1", kind="paragraph", text="Body")],
                ),
            },
            interactions=[InteractionReference(kind="custom_runtime", region_names=["explanation"])],
        )

        with self.assertRaises(InteractionRuntimeError) as context:
            create_slide_runtime(resolved_slide)

        self.assertEqual(context.exception.code, "unsupported_runtime_shape")

    def test_rejects_reveal_advance_when_no_steps_remain(self) -> None:
        runtime = self._build_quiz_runtime_from_fixture()

        runtime.select_answer(0)
        runtime.reveal_feedback()

        with self.assertRaises(InteractionRuntimeError) as context:
            runtime.advance_reveal()

        self.assertEqual(context.exception.code, "reveal_exhausted")

    def _build_quiz_runtime_from_fixture(self):
        source = (REPO_ROOT / "tests" / "fixtures" / "mvp_deck.md").read_text(encoding="utf-8")
        deck = parse_document(source, deck_id="fixture-deck")
        resolved_slides = resolve_deck_templates(deck)
        return create_slide_runtime(resolved_slides[1])


if __name__ == "__main__":
    unittest.main()