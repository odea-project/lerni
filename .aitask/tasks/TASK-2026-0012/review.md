# Review Record

## Review Scope

- multi-deck browser export and manifest alignment with the current browser renderer contract
- bounded browser selection behavior via picker and URL parameter
- separation from backend, authoring-platform, and unrelated packaging concerns

## Checks Performed

- verified that the static site build exports multiple deck payloads plus a manifest from a bounded repository deck directory
- verified that the browser now selects decks by manifest entry, URL parameter, and visible picker rather than a hard-coded payload path
- verified that tests cover multi-deck export behavior, manifest generation, and relative source-path behavior
- verified that no backend service, persistence, or browser-side reparsing of Markdown was introduced under this task

## Findings

- none

## Requested Changes

- none

## Decision

Accepted.

## Reviewer Sign-Off

- reviewer: human:repository.owner
- reviewed_at: 2026-03-13T21:51:00Z
- rationale: The deck-loading path is static, explicit, and portable, and it extends the browser renderer without blurring the core contract boundaries.