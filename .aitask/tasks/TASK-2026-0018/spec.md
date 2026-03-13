# Task Specification

## Context

The browser renderer is functionally useful, but the current layout keeps deck controls, runtime state, and browser handoff information persistently visible in side boxes. The next bounded implementation step is to make the viewer feel more like a slide surface with optional controls rather than a debug dashboard.

This task exists to improve browser presentation focus without widening into a broader presentation framework.

## Objective

Implement the first minimal browser viewer layout MVP so the slide uses most of the viewport by default while metadata and secondary controls remain quickly available on demand.

## In Scope

- redesign the viewer layout toward a content-first slide surface
- replace persistently visible side metadata blocks with an on-demand control and details panel
- keep primary slide actions and navigation available in a compact, non-dominating dock
- preserve current deck selection, slide selection, runtime state visibility, and browser handoff information behind the optional panel
- update minimal documentation for the new viewer layout behavior
- capture validation evidence through repository validation and browser-serving checks

## Out Of Scope

- presentation mode, fullscreen APIs, or remote control support
- major theming or branding systems
- route-based layouts or multi-page browser shells
- backend or persistence features
- large-scale visual redesign of slide content semantics

## Assumptions

- a small header and compact dock are acceptable as always-visible chrome
- runtime and browser handoff data can move behind a user-triggered panel without harming current debugging needs
- preserving the current action set is more important than keeping the existing panel structure

## Constraints

- stay aligned to the current static browser interaction model
- keep controls accessible on desktop and mobile
- do not remove supported navigation, reveal, feedback, reset, or URL-state behavior
- avoid introducing dependencies beyond the repository's current lightweight tooling

## Deliverables

- minimal content-first browser layout
- on-demand panel for deck selectors, runtime state, and browser handoff metadata
- minimal documentation update
- validation evidence for browser rendering and repository checks
- updated task records and evidence trail

## Key Questions To Answer

- which information must remain immediately visible, and which can move behind an on-demand panel?
- how can navigation and runtime actions stay available without visually dominating the slide?
- how can the on-demand panel remain quick to open and dismiss without becoming a new app shell?

## Suggested Structure Of The Target Change

1. minimal viewer chrome
2. compact action dock
3. on-demand control panel
4. documentation and evidence updates

## Acceptance Criteria

- executable browser code exists for a content-first viewer layout where the slide takes most of the viewport
- runtime and deck metadata are hidden by default and available through an explicit on-demand panel
- primary slide actions remain available without persistent heavy side panels
- documentation explains the minimal viewer behavior
- scope remains bounded and does not become a broader presentation framework

## Dependencies

- TASK-2026-0017 closed and available as the current browser interaction precursor
- human approval before execution

## Review Expectations

- verify that the layout prioritizes slide content over surrounding metadata chrome
- verify that the on-demand panel still exposes the previously available metadata and selectors
- verify that the compact controls remain usable and accessible

## Rollback Plan

Revert the layout refinement if it hides necessary controls or overcomplicates the browser viewer structure, preserve records, and reopen the task with a narrower presentation change.

## Required Evidence

- linkage to the existing browser renderer docs
- validation output demonstrating the minimal viewer and on-demand panel in the served browser page
- review decision and implemented file paths

## Approvals Needed

- `approver`: `human:repository.owner` before execution starts