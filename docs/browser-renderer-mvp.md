# Browser Renderer MVP

The first browser renderer MVP makes the web target concrete without replacing the existing Python pipeline. The Python side remains responsible for parsing, template resolution, and bounded runtime modeling. The browser side consumes an exported payload and executes only the already-supported interactive behavior.

## Delivery Shape

The MVP browser path consists of two pieces:

- a Python export step that turns repository-authored Markdown decks into browser payloads plus a manifest
- a static browser renderer that consumes the manifest and selected payload and executes reveal, answer-selection, feedback, reset, and slide navigation behavior

## Export Contract

The browser payload contains:

- `deckId`
- ordered slides
- per-slide slot sequence and slot content blocks
- interaction kinds
- runtime metadata, including initial snapshot, maximum reveal step, and answer count

The browser does not parse Markdown and does not reinterpret semantic structure from scratch.

The static site build also emits a manifest containing:

- `defaultDeckId`
- ordered deck entries with `deckId`, `title`, `payloadPath`, `sourcePath`, and `slideCount`

## Browser Scope

The static renderer currently supports:

- `title-overview`
- `quiz-feedback`
- previous and next slide navigation
- reveal advancement
- single answer selection
- explicit feedback reveal
- slide reset
- manifest-driven deck selection by picker or `?deck=` URL parameter

The browser layer remains intentionally bounded. It is not a framework, editor, backend, or general state platform.

## Demo Path

Run the payload build step:

```text
c:/Users/PCUser/github/lerni/.venv/Scripts/python.exe tools/build_browser_demo.py
```

Then serve the `web/` directory with a static HTTP server such as Python's built-in `http.server` and open the resulting page in a browser.

The browser will load the default deck from the manifest unless a specific `deck` query parameter is provided.

Supported URL parameters:

- `?deck=<deck-id>` selects a deck from the manifest
- `?slide=<n>` selects a 1-based slide index inside the chosen deck

If `deck` or `slide` is invalid, the browser falls back predictably and shows a visible message instead of breaking the page.

The page now also exposes a direct slide picker, which stays synchronized with the current deck and writes the selected slide back into the `slide` URL parameter.

For the simplified local workflow, use:

```text
c:/Users/PCUser/github/lerni/.venv/Scripts/python.exe tools/run_browser_site.py
```

Optional bounded flags:

- `--host 0.0.0.0`
- `--port 9000`
- `--skip-build`

This helper rebuilds the static site by default and then serves `web/` at a printed local URL.

## Relationship To Existing Contracts

- parser and semantic model own authored-source interpretation
- template resolution owns slot binding
- interaction runtime defines the bounded event and visibility model
- browser renderer maps the exported contract onto visible UI and user interaction

This keeps the end-to-end web path explicit without collapsing the architecture into one large layer.