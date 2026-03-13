# Task Specification

## Context

The browser renderer can now load decks from a manifest and local workflow helper, but the URL state still only partially reflects the current browser state. The next implementation step is to make deck and slide selection deep-linkable and to handle invalid URL parameters predictably.

This task exists to improve browser navigation quality without widening into a general routing system.

## Objective

Implement the first browser URL-state and parameter-fallback MVP aligned to the existing browser renderer contract, together with focused validation evidence and any minimal supporting documentation updates needed to explain implemented behavior.

## In Scope

- implement deep-linking for current deck and current slide through URL parameters
- implement predictable fallback behavior for invalid or missing `deck` and `slide` parameters
- implement visible browser messaging for parameter fallback cases
- add minimal documentation updates for the supported URL-state behavior
- capture validation evidence through tests where already available and browser-serving checks where appropriate

## Out Of Scope

- general client-side routing frameworks
- browser history orchestration beyond bounded query-parameter state
- persistence of reader progress across sessions
- backend redirects or server-side routing
- unrelated browser UI redesign work

## Assumptions

- `deck` and `slide` query parameters are sufficient for the MVP
- slide deep-linking can be 1-based for readability
- visible fallback messaging is enough without adding a general notification system

## Constraints

- stay aligned to the current manifest-driven deck-loading model
- keep URL handling small, explicit, and readable
- avoid introducing a broader router abstraction than needed for the MVP
- preserve static hosting compatibility

## Deliverables

- browser URL-state and fallback code
- updated documentation for supported parameters
- validation evidence for deep-link and fallback behavior
- updated task records and evidence trail

## Key Questions To Answer

- how should invalid deck ids fall back without hiding the problem completely?
- how should invalid slide indices be interpreted or clamped?
- when should the browser write updated deck/slide state back into the URL?

## Suggested Structure Of The Target Change

1. URL parameter parsing and normalization
2. browser fallback messaging
3. URL write-back on state change
4. validation evidence
5. documentation update

## Acceptance Criteria

- executable browser code exists for deck and slide deep-linking
- invalid parameters fall back predictably and visibly without breaking the page
- documentation explains the supported URL-state behavior
- scope remains bounded and does not turn into a general routing system

## Dependencies

- TASK-2026-0012 closed and available as browser site build precursor
- TASK-2026-0013 closed and available as local browser workflow precursor
- human approval before execution

## Review Expectations

- verify that URL-state handling remains bounded and static-host-friendly
- verify that fallback behavior is explicit and user-visible
- verify that code does not widen into routing-framework concerns

## Rollback Plan

Revert URL-state changes if they overcomplicate browser navigation or misrepresent the static-site model, preserve records, and reopen the task with a narrower parameter set.

## Required Evidence

- linkage to the existing browser renderer docs
- validation output demonstrating deep-link and fallback behavior
- review decision and implemented file paths

## Approvals Needed

- `approver`: `human:repository.owner` before execution starts