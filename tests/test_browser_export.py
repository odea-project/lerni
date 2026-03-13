from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lerni.browser_export import build_browser_payload_from_source, write_browser_payload


class BrowserExportTests(unittest.TestCase):
    def test_builds_browser_payload_from_fixture(self) -> None:
        source = (REPO_ROOT / "tests" / "fixtures" / "mvp_deck.md").read_text(encoding="utf-8")

        payload = build_browser_payload_from_source(source, deck_id="browser-fixture")

        self.assertEqual(payload["deckId"], "browser-fixture")
        self.assertEqual([slide["templateId"] for slide in payload["slides"]], ["title-overview", "quiz-feedback"])
        quiz_slide = payload["slides"][1]
        self.assertEqual(quiz_slide["runtime"]["maxRevealStep"], 1)
        self.assertEqual(quiz_slide["runtime"]["answerCount"], 2)
        self.assertFalse(quiz_slide["runtime"]["initialSnapshot"]["feedbackVisible"])
        self.assertEqual(quiz_slide["runtime"]["initialSnapshot"]["slotVisibility"]["feedback"]["hiddenBlockIds"], ["slide-2-feedback-1"])

    def test_writes_browser_payload_file(self) -> None:
        source_path = REPO_ROOT / "tests" / "fixtures" / "mvp_deck.md"
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "deck.json"

            written_path = write_browser_payload(source_path, output_path, deck_id="written-fixture")

            self.assertEqual(written_path, output_path)
            content = output_path.read_text(encoding="utf-8")
            self.assertIn('"deckId": "written-fixture"', content)
            self.assertIn('"templateId": "quiz-feedback"', content)


if __name__ == "__main__":
    unittest.main()