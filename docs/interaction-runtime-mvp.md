# Interaction Runtime MVP

The first executable interaction-runtime slice consumes `ResolvedTemplateSlide` instances from template resolution and maintains a bounded runtime state that a browser renderer can observe. It does not render DOM itself; it produces serializable snapshot data about visible and hidden block ids per slot.

## Supported Runtime Behaviors

- guided reveal progression by ordered reveal step
- bounded answer selection for `question_flow`
- explicit feedback reveal after answer selection
- full slide reset back to initial runtime state

## State Surface

The runtime keeps only the minimum state needed by the MVP:

- `current_reveal_step`
- `selected_answer_index`
- `feedback_visible`
- derived `active_mode`

Every state transition returns a `SlideRuntimeSnapshot` with:

- current reveal position
- whether another reveal step remains
- selected answer, if any
- feedback visibility
- slot-level visible and hidden block ids

## Event Rules

- `advance_reveal()` advances one reveal step and fails when no steps remain
- `select_answer(index)` is valid only for `question_flow` slides and only once before reset
- `reveal_feedback()` requires a selected answer and makes feedback learner-visible; if feedback blocks are gated by reveal steps, the runtime advances to the first required feedback step
- `reset()` returns the slide to its initial state

## Browser Handoff

The runtime output is intended as a handoff contract for a later web runtime layer:

- template resolution continues to own structural slot binding
- interaction runtime owns event handling and visibility state
- a browser renderer can map the visible and hidden block ids onto actual DOM or component output without reimplementing runtime transitions

## Failure Boundaries

The MVP runtime fails explicitly for:

- unsupported interaction kinds
- incomplete question-flow structure
- invalid answer indices
- feedback reveal before answer selection
- reveal advancement after the final step

This keeps the runtime narrow and predictable instead of drifting toward a general scripting system.