# Task Specification

## Context

The browser viewer is now visually calmer, but it still needs stronger projector readability and more explicit slide-to-slide motion to function well as a beamer presentation surface. The next bounded step is to increase slide typography and add swipe-style transitions when slides change.

This task exists to improve presentation quality without widening into a full presentation framework.

## Objective

Implement the first presentation-oriented browser refinement MVP so slides read better from a distance and slide navigation is accompanied by bounded swipe-style motion.

## In Scope

- increase slide-oriented typography and spacing for better projector readability
- add swipe-style transitions when moving between slides
- preserve current slide controls, URL-state behavior, and browser interactions
- keep reveal and quiz interactions functional inside the refined presentation viewer
- add lightweight automated validation for any new transition-direction helper logic without introducing a browser framework
- update minimal documentation for the presentation-oriented viewer behavior
- capture validation evidence through repository validation and browser-serving checks

## Out Of Scope

- fullscreen APIs, presenter notes, or remote controls
- advanced animation choreography beyond bounded slide transitions
- audio, video, or media synchronization
- backend or persistence features
- broader presentation-suite behavior

## Assumptions

- larger typography should apply primarily to slide content rather than all viewer chrome
- simple directional swipe motion is sufficient for the MVP
- animation duration should remain short enough not to feel sluggish during live presentation

## Constraints

- stay aligned to the current static browser interaction model
- preserve current controls and metadata access
- avoid motion that hides content too long or interferes with reading
- avoid introducing dependencies beyond the repository's current lightweight tooling

## Deliverables

- presentation-oriented larger slide typography
- bounded swipe-style slide transition behavior
- lightweight automated validation for transition helper logic
- minimal documentation update
- validation evidence for browser rendering and repository checks
- updated task records and evidence trail

## Key Questions To Answer

- which text scales should increase for projector readability without overwhelming the layout?
- how should slide direction be represented in a bounded swipe animation?
- how can transition behavior be validated without adding a browser automation framework?

## Suggested Structure Of The Target Change

1. scale viewer typography for presentation readability
2. add transition-direction state and swipe animation classes
3. lightweight automated validation for transition helper behavior
4. documentation and evidence updates

## Acceptance Criteria

- executable browser code exists for larger presentation-friendly slide typography
- slide changes visibly animate with a bounded directional swipe effect
- current slide controls and interactions remain functional
- lightweight automated validation exists for any new transition helper logic without adding a browser framework
- documentation explains the presentation-oriented viewer behavior
- scope remains bounded and does not become a broader presentation framework

## Dependencies

- TASK-2026-0019 closed and available as the current browser visual precursor
- human approval before execution

## Review Expectations

- verify that slide readability is materially improved for projected viewing
- verify that swipe transitions are directional, bounded, and do not obscure content too long
- verify that current browser controls remain intact

## Rollback Plan

Revert the readability or motion refinement if it harms viewer clarity or introduces distracting transitions, preserve records, and reopen the task with a narrower presentation behavior set.

## Required Evidence

- linkage to the existing browser renderer docs
- validation output demonstrating the larger viewer typography and swipe-style transitions in the served browser page
- review decision and implemented file paths

## Approvals Needed

- `approver`: `human:repository.owner` before execution starts