from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lerni.browser_export import build_browser_site

SOURCE_PATH = REPO_ROOT / "tests" / "fixtures" / "mvp_deck.md"
SOURCE_DIR = REPO_ROOT / "content" / "decks"
OUTPUT_DIR = REPO_ROOT / "web" / "data" / "decks"


def main() -> None:
    manifest = build_browser_site(SOURCE_DIR, OUTPUT_DIR)
    print(f"Built browser site payloads for {len(manifest['decks'])} decks into {OUTPUT_DIR}")


if __name__ == "__main__":
    main()