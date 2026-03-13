from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lerni.browser_export import build_browser_site


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8123
SOURCE_DIR = REPO_ROOT / "content" / "decks"
OUTPUT_DIR = REPO_ROOT / "web" / "data" / "decks"
WEB_DIR = REPO_ROOT / "web"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build and serve the local Lerni browser site.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host interface to bind the local static server to.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port for the local static server.")
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Serve the current web/ output without rebuilding the browser site data first.",
    )
    return parser.parse_args(argv)


def build_local_browser_site() -> dict[str, object]:
    return build_browser_site(SOURCE_DIR, OUTPUT_DIR)


def build_site_url(host: str, port: int) -> str:
    return f"http://{host}:{port}/index.html"


def run_server(host: str, port: int) -> None:
    handler = partial(SimpleHTTPRequestHandler, directory=str(WEB_DIR))
    with ThreadingHTTPServer((host, port), handler) as server:
        print(f"Serving Lerni browser site at {build_site_url(host, port)}")
        server.serve_forever()


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if not args.skip_build:
        manifest = build_local_browser_site()
        print(f"Built browser site for {len(manifest['decks'])} decks into {OUTPUT_DIR}")
    run_server(args.host, args.port)


if __name__ == "__main__":
    main()