from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lerni.browser_export import write_browser_payload

SOURCE_PATH = REPO_ROOT / "tests" / "fixtures" / "mvp_deck.md"
OUTPUT_PATH = REPO_ROOT / "web" / "data" / "mvp_deck.json"


def main() -> None:
    output_path = write_browser_payload(SOURCE_PATH, OUTPUT_PATH, deck_id="browser-demo")
    print(f"Wrote browser demo payload to {output_path}")


if __name__ == "__main__":
    main()