# Task Specification

## Context

The repository now has a static browser renderer MVP, but it currently loads a single generated payload from a fixed path. The next implementation step is to add a bounded deck-loading path so the browser can select among multiple authored decks exported from the repository.

This task exists to make the web path feel like a real static site rather than a single hard-coded demo file.

## Objective

Implement the first browser deck-loading and static site build slice aligned to the existing browser renderer contract, together with focused tests and any minimal supporting documentation updates needed to explain implemented behavior.

## In Scope

- implement a bounded source deck directory for browser-exportable Markdown decks
- implement a static site build step that exports multiple deck payloads and a manifest
- implement browser-side deck selection via URL parameter and visible deck picker
- add focused tests for manifest and multi-deck export behavior
- add or update minimal docs describing implemented support
- capture evidence of validation and tests

## Out Of Scope

- backend APIs or dynamic database-backed deck loading
- full authoring workflows or browser editing
- authentication, persistence, or analytics
- replacing the existing browser renderer interaction model
- generalized asset pipelines beyond the bounded static site build

## Assumptions

- a small repository deck directory is sufficient for the MVP
- browser selection can remain static and manifest-driven
- the current renderer controls remain valid once deck loading is generalized

## Constraints

- stay aligned to the existing browser payload contract and renderer behavior
- keep the static site build readable and framework-light
- avoid reintroducing parsing or semantic inference in the browser
- keep the browser deck selector bounded to manifest-driven static content

## Deliverables

- multi-deck export and manifest build code
- browser deck-selection behavior and UI updates
- representative authored decks under a repository deck directory
- focused tests and updated task records

## Key Questions To Answer

- what manifest shape is sufficient for browser deck selection?
- how should deck ids map to exported payload files?
- which authored deck set is enough to prove multi-deck loading without widening scope?
- how should the browser behave when a requested deck id is missing?

## Suggested Structure Of The Target Change

1. repository deck directory
2. site build and manifest export
3. browser deck selection flow
4. focused tests
5. minimal documentation updates if needed

## Acceptance Criteria

- executable code exists for a bounded static site build that exports multiple decks and a manifest
- the browser renderer can load a requested deck by URL parameter or picker selection
- tests cover manifest and multi-deck export behavior
- scope remains static and bounded without backend drift
- the result is concrete enough to prove a real static browser deck-loading path

## Dependencies

- TASK-2026-0011 closed and available as browser renderer precursor
- human approval before execution

## Review Expectations

- verify that the deck-loading path stays static and manifest-driven
- verify that browser behavior remains bounded and readable
- verify that code does not widen into backend or authoring-platform concerns

## Rollback Plan

Revert multi-deck loading changes if they misrepresent the static browser contract, preserve records, and reopen the task with a narrower manifest or single-directory scope.

## Required Evidence

- linkage to the browser renderer MVP docs
- test results and validation output
- review decision and implemented file paths

## Approvals Needed

- `approver`: `human:repository.owner` before execution starts