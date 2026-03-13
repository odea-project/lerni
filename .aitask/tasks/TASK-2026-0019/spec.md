# Task Specification

## Context

The browser viewer is now content-first, but the visual language still leans too heavily on nested bordered boxes and a visually blunt header. The next bounded step is to keep the minimalist structure while making the presentation calmer, cleaner, and more modern.

This task exists to improve visual quality without widening into a full design system or interaction redesign.

## Objective

Implement the first modern minimal browser viewer refinement MVP so the slide remains dominant while surrounding chrome becomes lighter, flatter, and visually cleaner.

## In Scope

- reduce heavy nested card styling in both the main slide surface and the on-demand panel
- slim the persistent header chrome and make it visually quieter
- refine typography, spacing, and surfaces toward a more modern minimal aesthetic
- preserve current viewer structure, controls, and on-demand panel behavior
- update minimal documentation for the refined viewer presentation behavior
- capture validation evidence through repository validation and browser-serving checks

## Out Of Scope

- major behavior changes to browser navigation or runtime actions
- a broader design system, theme switcher, or component library
- fullscreen or presentation-mode logic
- backend or persistence features
- radical content model changes

## Assumptions

- a quieter header and flatter surfaces will better support the slide-first experience
- reduced box treatment should still leave enough structure for readability
- preserving the current content templates is more important than inventing a new editorial layout language in this task

## Constraints

- stay aligned to the current static browser interaction model
- preserve all supported controls and metadata access
- keep the design usable on desktop and mobile
- avoid introducing dependencies beyond the repository's current lightweight tooling

## Deliverables

- refined modern minimal browser styling
- slimmer persistent viewer chrome and calmer panel presentation
- minimal documentation update
- validation evidence for browser rendering and repository checks
- updated task records and evidence trail

## Key Questions To Answer

- how can the slide feel cleaner without stripping away too much structural hierarchy?
- which surfaces should remain softly elevated versus fully flat?
- how can the header and dock remain useful without reading as bulky UI furniture?

## Suggested Structure Of The Target Change

1. refine viewer chrome
2. flatten and simplify surface styling
3. tune slide template presentation
4. documentation and evidence updates

## Acceptance Criteria

- executable browser code exists for a calmer, more modern minimal viewer presentation
- the default view has visibly less heavy box nesting and a slimmer header feel
- current controls and metadata access remain intact
- documentation explains the refined viewer presentation behavior
- scope remains bounded and does not become a broader design-system effort

## Dependencies

- TASK-2026-0018 closed and available as the current browser layout precursor
- human approval before execution

## Review Expectations

- verify that the visual refinement clearly reduces heavy chrome and nested boxiness
- verify that functionality and metadata access are preserved
- verify that the result still feels minimal rather than decorative or noisy

## Rollback Plan

Revert the visual refinement if it harms readability or overcomplicates the viewer style, preserve records, and reopen the task with a narrower styling pass.

## Required Evidence

- linkage to the existing browser renderer docs
- validation output demonstrating the refined viewer in the served browser page
- review decision and implemented file paths

## Approvals Needed

- `approver`: `human:repository.owner` before execution starts