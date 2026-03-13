# Browser Renderer MVP

The first browser renderer MVP makes the web target concrete without replacing the existing Python pipeline. The Python side remains responsible for parsing, template resolution, and bounded runtime modeling. The browser side consumes an exported payload and executes only the already-supported interactive behavior.

## Delivery Shape

The MVP browser path consists of two pieces:

- a Python export step that turns the representative authored deck into a browser payload
- a static browser renderer that consumes that payload and executes reveal, answer-selection, feedback, reset, and slide navigation behavior

## Export Contract

The browser payload contains:

- `deckId`
- ordered slides
- per-slide slot sequence and slot content blocks
- interaction kinds
- runtime metadata, including initial snapshot, maximum reveal step, and answer count

The browser does not parse Markdown and does not reinterpret semantic structure from scratch.

## Browser Scope

The static renderer currently supports:

- `title-overview`
- `quiz-feedback`
- previous and next slide navigation
- reveal advancement
- single answer selection
- explicit feedback reveal
- slide reset

The browser layer remains intentionally bounded. It is not a framework, editor, backend, or general state platform.

## Demo Path

Run the payload build step:

```text
c:/Users/PCUser/github/lerni/.venv/Scripts/python.exe tools/build_browser_demo.py
```

Then serve the `web/` directory with a static HTTP server such as Python's built-in `http.server` and open the resulting page in a browser.

## Relationship To Existing Contracts

- parser and semantic model own authored-source interpretation
- template resolution owns slot binding
- interaction runtime defines the bounded event and visibility model
- browser renderer maps the exported contract onto visible UI and user interaction

This keeps the end-to-end web path explicit without collapsing the architecture into one large layer.