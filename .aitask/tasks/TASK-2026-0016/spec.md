# Task Specification

## Context

The browser renderer now supports button navigation, query-parameter URL state, and direct slide picking, but it still requires pointer interaction for the main runtime actions. The next bounded implementation step is to add a small keyboard layer over the existing controls.

This task exists to improve browser navigation ergonomics without widening into a broader hotkey system or presentation controller.

## Objective

Implement the first browser keyboard-navigation MVP aligned to the existing static browser interaction model, together with minimal documentation updates and lightweight validation.

## In Scope

- implement keyboard shortcuts for the existing previous, next, advance reveal, show feedback, and reset actions
- ensure shortcuts do not override focused form controls or buttons
- keep the existing button and picker navigation model intact
- add lightweight automated validation for shortcut resolution behavior without introducing a browser framework
- update minimal documentation for the supported browser keyboard behavior
- capture validation evidence through repository validation and browser-serving checks

## Out Of Scope

- configurable hotkeys or a general keyboard-command registry
- keyboard-driven deck selection or answer-choice focus management
- general client-side routing systems
- backend or persistence features
- large-scale browser UI redesigns

## Assumptions

- a minimal fixed shortcut set is sufficient for the MVP
- visible shortcut guidance should remain lightweight and secondary to the existing buttons
- ignoring shortcuts while controls are focused is safer than globally hijacking every keypress

## Constraints

- stay aligned to the current static browser interaction model
- do not break pointer-driven navigation or answer selection
- avoid introducing dependencies beyond the repository's current lightweight tooling
- preserve static hosting compatibility

## Deliverables

- browser keyboard-navigation behavior and lightweight UI hinting
- a dependency-free automated test for shortcut resolution logic
- minimal documentation update
- validation evidence for browser rendering and repository checks
- updated task records and evidence trail

## Key Questions To Answer

- which shortcut set is small enough for the MVP without becoming a general hotkey system?
- when should browser shortcuts be ignored because focus is inside an interactive control?
- how can shortcut behavior be validated without introducing a full browser automation stack?

## Suggested Structure Of The Target Change

1. keyboard shortcut mapping and guarded event handling
2. shared action helpers for buttons and keyboard
3. lightweight automated test coverage for shortcut resolution
4. documentation and evidence updates

## Acceptance Criteria

- executable browser code exists for bounded keyboard access to the existing navigation and runtime actions
- shortcuts are ignored while interactive controls are focused
- the browser UI exposes lightweight shortcut guidance
- automated validation exists for shortcut resolution logic without adding a browser framework
- documentation explains the supported keyboard shortcuts
- scope remains bounded and does not become a broader presentation-control system

## Dependencies

- TASK-2026-0015 closed and available as the current browser-navigation precursor
- human approval before execution

## Review Expectations

- verify that the shortcut set stays small and aligned to the current browser action model
- verify that focus guards prevent accidental shortcut hijacking inside controls
- verify that automated validation remains lightweight and dependency-free

## Rollback Plan

Revert keyboard-navigation changes if they interfere with existing browser controls or widen the browser control model beyond the task intent, preserve records, and reopen the task with a narrower shortcut set.

## Required Evidence

- linkage to the existing browser renderer docs
- validation output demonstrating shortcut-resolution coverage and served browser rendering
- review decision and implemented file paths

## Approvals Needed

- `approver`: `human:repository.owner` before execution starts