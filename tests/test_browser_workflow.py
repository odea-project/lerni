from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools import run_browser_site


class BrowserWorkflowTests(unittest.TestCase):
    def test_parse_args_defaults(self) -> None:
        args = run_browser_site.parse_args([])

        self.assertEqual(args.host, run_browser_site.DEFAULT_HOST)
        self.assertEqual(args.port, run_browser_site.DEFAULT_PORT)
        self.assertFalse(args.skip_build)

    def test_parse_args_overrides(self) -> None:
        args = run_browser_site.parse_args(["--host", "0.0.0.0", "--port", "9000", "--skip-build"])

        self.assertEqual(args.host, "0.0.0.0")
        self.assertEqual(args.port, 9000)
        self.assertTrue(args.skip_build)

    def test_build_site_url(self) -> None:
        self.assertEqual(run_browser_site.build_site_url("127.0.0.1", 8123), "http://127.0.0.1:8123/index.html")

    def test_build_local_browser_site_uses_repository_decks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            original_source_dir = run_browser_site.SOURCE_DIR
            original_output_dir = run_browser_site.OUTPUT_DIR
            try:
                run_browser_site.SOURCE_DIR = temp_root / "decks"
                run_browser_site.OUTPUT_DIR = temp_root / "web" / "data" / "decks"
                run_browser_site.SOURCE_DIR.mkdir(parents=True)
                (run_browser_site.SOURCE_DIR / "sample.md").write_text(
                    "::slide kind=overview template=title-overview\n# Sample\n::region explanation\nBody.",
                    encoding="utf-8",
                )

                manifest = run_browser_site.build_local_browser_site()

                self.assertEqual(manifest["defaultDeckId"], "sample")
                self.assertEqual(manifest["decks"][0]["payloadPath"], "./data/decks/sample.json")
                self.assertTrue((run_browser_site.OUTPUT_DIR / "sample.json").exists())
            finally:
                run_browser_site.SOURCE_DIR = original_source_dir
                run_browser_site.OUTPUT_DIR = original_output_dir


if __name__ == "__main__":
    unittest.main()