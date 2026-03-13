# Task Specification

## Context

The browser renderer now supports `deck` and `slide` deep-linking through query parameters, but direct slide jumps still require manual URL editing or repeated next/previous navigation. The next implementation step is to add a bounded in-page slide-jump control.

This task exists to improve browser navigation ergonomics without widening into a richer presentation-control system.

## Objective

Implement the first browser slide-jump UI MVP aligned to the existing browser URL-state model, together with minimal documentation updates and validation evidence.

## In Scope

- implement a browser UI control for jumping directly to a slide within the current deck
- keep the control synchronized with the existing `slide` URL parameter
- ensure the control updates when the active deck changes
- update minimal documentation for the supported browser navigation behavior
- capture validation evidence through browser-serving checks and repository validation

## Out Of Scope

- keyboard shortcuts or remote presentation controls
- general client-side routing systems
- browser history orchestration beyond the existing query-parameter model
- backend or persistence features
- large-scale browser UI redesigns

## Assumptions

- a select-style slide picker is sufficient for the MVP
- 1-based slide labels are clearer for users than zero-based indices
- existing previous/next buttons remain part of the navigation model

## Constraints

- stay aligned to the current static browser URL-state model
- keep the navigation UI small and readable
- avoid introducing a wider presentation-control architecture than needed
- preserve static hosting compatibility

## Deliverables

- browser slide-jump UI and synchronization behavior
- minimal documentation update
- validation evidence for browser navigation behavior
- updated task records and evidence trail

## Key Questions To Answer

- where should direct slide-jump UI live relative to the current deck selector?
- how should slide labels be presented for overview versus quiz slides?
- when should the slide picker update in response to deck and slide changes?

## Suggested Structure Of The Target Change

1. slide picker UI
2. browser synchronization logic
3. documentation update
4. validation evidence

## Acceptance Criteria

- executable browser code exists for direct slide selection within the current deck
- the selected slide remains synchronized with the `slide` URL parameter
- the control updates correctly when the user changes decks
- documentation explains the supported slide-jump behavior
- scope remains bounded and does not become a broader presentation-control system

## Dependencies

- TASK-2026-0014 closed and available as browser URL-state precursor
- human approval before execution

## Review Expectations

- verify that the UI stays small and aligned to the existing URL-state model
- verify that synchronization is explicit and static-host-friendly
- verify that code does not widen into unrelated browser navigation systems

## Rollback Plan

Revert slide-jump UI changes if they overcomplicate browser navigation or conflict with the existing query-parameter model, preserve records, and reopen the task with a narrower control surface.

## Required Evidence

- linkage to the existing browser renderer docs
- validation output demonstrating direct slide-jump behavior
- review decision and implemented file paths

## Approvals Needed

- `approver`: `human:repository.owner` before execution starts