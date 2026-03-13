# MVP Interaction Runtime

## Purpose

The MVP interaction runtime defines the bounded execution layer that turns normalized, declarative interaction meaning into learner-visible behavior. Its purpose is to support reveals, question flows, feedback display, and simple state-based content switching without expanding the system into a general scripting or application-runtime platform.

This runtime exists because the product now has three adjacent contracts already defined:

- the interaction model defines which learning interactions are first-class
- the semantic document model defines how those interactions are represented after normalization
- the template runtime contract defines how interaction-capable content is structurally placed into resolved templates

The interaction runtime is the layer that interprets those inputs over time.

## Pipeline Position And Responsibilities

At MVP level, the relevant pipeline should be understood as:

1. authored source
2. semantic document model
3. template resolution
4. interaction runtime
5. rendering and presentation output

The interaction runtime is responsible for:

- maintaining the bounded interaction state needed by supported educational patterns
- interpreting supported runtime events
- applying allowed state transitions for reveals, answer selection, feedback display, and simple content switching
- exposing resolved runtime state so rendering can show the correct content at the correct time

The interaction runtime is not responsible for:

- reparsing source or recovering semantic meaning that should already be normalized
- selecting templates or resolving structural slot mappings
- introducing arbitrary script execution as a default behavior path
- becoming a general application-state architecture unrelated to slide-based learning flow

## Design Principles

### Declarative Inputs, Bounded Execution

The runtime should execute only the bounded interaction patterns the product explicitly supports. It should interpret declarative meaning, not arbitrary program logic.

### Teaching Flow First

Runtime behavior should exist to support explanation, practice, and feedback. It should not optimize first for animation spectacle or broad UI programmability.

### Small State Surface

The MVP should use a small number of well-defined state concepts. Fewer state dimensions make runtime behavior easier to validate, explain, and implement.

### Predictable Transitions

The runtime should make it obvious which events can occur, which state changes are allowed, and what learner-visible outcomes those changes affect.

### Separation From Structure

The interaction runtime should operate on already resolved structural affordances rather than trying to redefine template layout or document normalization at execution time.

## MVP State Concepts

The MVP does not need a general state machine platform. It needs a bounded set of state concepts aligned to the supported educational interactions.

### Reveal State

Reveal state tracks progression through a guided sequence on a slide.

At MVP level, reveal state should support:

- current reveal step
- whether additional reveal steps remain
- association between revealable content and its visible or hidden status

Reveal state should not model arbitrary animation choreography. It should model ordered disclosure only.

### Question State

Question state tracks the minimal execution context for a question interaction.

At MVP level, question state should support:

- whether a question is unanswered or answered
- which bounded choice or outcome has been selected
- whether a response should trigger feedback availability

The MVP does not need advanced assessment or scoring state here.

### Feedback State

Feedback state determines whether feedback content is hidden, revealed, or switched based on a bounded outcome.

At MVP level, feedback state should support:

- whether feedback is currently visible
- which feedback branch or outcome is active
- whether an explanatory follow-up or hint has been revealed

Feedback state should remain tightly coupled to supported learning outcomes rather than becoming a generic conditional-rendering engine.

### Content-Switch State

Some slides will need a small amount of bounded state-based content switching beyond basic reveal. This should remain a narrow concept used for educational flow transitions such as prompt-to-answer, answer-to-feedback, or hint progression.

At MVP level, content-switch state should support:

- a bounded current mode or view
- a finite set of authored content outcomes tied to supported interaction meaning

This is not a general application-state store.

## Events And Transition Model

The interaction runtime should respond only to a small number of explicit event categories.

Reasonable MVP event classes are:

- reveal advance
- reveal reset
- answer selection
- feedback reveal
- bounded mode switch

These events should map to allowed transitions in predictable ways.

### Reveal Transitions

Reveal advance should move a slide from one reveal step to the next if another step exists. Reveal reset should return the reveal sequence to its initial state when allowed by the surrounding presentation flow.

### Question Transitions

Answer selection should move question state from unanswered to answered and bind the selected outcome needed for later feedback or content switching.

### Feedback Transitions

Feedback reveal should make the appropriate feedback branch visible based on the currently selected or derived outcome. If the MVP supports staged hints, those should be represented as additional bounded transitions rather than custom logic.

### Content-Switch Transitions

Mode switching should allow only authored, bounded transitions that correspond to supported educational meaning. The runtime should not allow arbitrary transitions into ungoverned states.

## Relationship To The Semantic Document Model

The semantic document model provides the normalized interaction meaning the runtime consumes.

The runtime should rely on it for:

- reveal group definitions
- question and answer structures
- feedback associations
- bounded interaction references
- slide-level meaning needed for supported transitions

If runtime execution depends on raw author syntax or Markdown quirks, the semantic boundary is too weak.

## Relationship To Template Resolution

The template runtime contract determines where interaction-capable content appears structurally. The interaction runtime determines how that content behaves over time.

The interaction runtime should rely on resolved template structure for:

- where interactive regions exist
- which resolved slots are interaction-relevant
- which content groupings correspond to reveal, question, answer, or feedback affordances

The runtime should not attempt to repair missing template bindings or reinterpret slot structure dynamically.

## Validation And Failure Boundaries

The interaction runtime should not silently compensate for missing semantic or structural prerequisites.

At MVP level, runtime validation should distinguish at least these cases:

### Valid Executable State

All required semantic inputs and structural affordances exist for the supported interaction pattern.

### Incomplete Executable State

The slide is structurally present, but required interaction inputs are missing or inconsistent. In this case, the runtime should surface the issue rather than inventing behavior.

### Unsupported Runtime Shape

The slide expresses interaction semantics that the MVP runtime does not support. In this case, the runtime should fail clearly rather than broadening execution behavior implicitly.

This boundary is important because runtime tolerance can otherwise become a back door for scope creep.

## What Must Remain Outside The Runtime

The following concerns should remain outside the MVP interaction runtime:

- arbitrary user scripting
- plugin-defined event systems
- global application-state orchestration
- persistence of learner progress across sessions
- analytics pipelines
- scoring and assessment engines
- multiplayer or networked coordination
- advanced animation systems unrelated to teaching flow

These exclusions protect the runtime from turning into a general platform before the product proves its narrow educational value.

## Non-Goals

The MVP interaction runtime should explicitly not become:

- a frontend framework within the slide system
- a generic finite-state-machine toolkit for arbitrary use cases
- an execution sandbox for custom code
- a substitute for template resolution or document normalization
- a broad orchestration layer for all future product capabilities

The runtime is only successful if it stays small, explicit, and strongly aligned to supported learning interactions.

## Open Questions For Implementation Design

- Should reveal advancement always be externally triggered, or can some supported runtime contexts trigger bounded automatic progression?
- What is the smallest useful representation of answer outcomes for feedback branching in the MVP?
- How should invalid runtime state be surfaced to authors and future tooling without leaking too much implementation detail?
- Which accessibility requirements will most strongly shape runtime event handling and visible state transitions?
- How should slide reset behavior work across reveals, question selection, and feedback visibility in different presentation contexts?

## Summary

The MVP interaction runtime should be a bounded execution layer for reveal progression, question answering, feedback display, and simple state-based content switching. It should interpret declarative semantic inputs and resolved template structure, expose a small set of predictable state concepts and transitions, and remain clearly separate from both template resolution and any general scripting or application-runtime ambition.