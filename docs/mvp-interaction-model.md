# MVP Interaction Model

## Purpose

The MVP interaction model defines the small set of learning-oriented behaviors that belong in the first useful release of the product. Its job is to keep interaction first-class without turning the framework into a general application runtime.

This document answers three product-level questions:

- which interaction patterns are essential for the MVP
- how declarative those interactions should be
- where the boundary lies between authored content, templates, and future runtime behavior

## Interaction Design Principles

### Teaching Value Over Presentation Effects

Interactions should exist because they improve explanation, practice, feedback, or guided attention. Decorative animation and generic slide theatrics are not the target.

### Declarative First

The MVP should prefer structured author intent over arbitrary code hooks. If a common educational interaction can be described semantically, that should be the default product direction.

### Small But Complete Core

The first release does not need many interaction types. It needs a narrow set that is clearly useful in lectures, workshops, and technical teaching material.

### Separation Of Concerns

Interaction should not absorb content structure or template structure. Content expresses what is being taught. Templates express reusable slide arrangement. The interaction model expresses how learner-visible behavior unfolds.

### Predictable Behavior

The MVP should avoid interaction forms that are too open-ended to reason about. Authors should be able to anticipate what a defined interaction will do without reading or writing runtime code.

## What Interaction-Native Means In The MVP

Interaction-native does not mean every slide is interactive. It means the product treats a core set of teaching interactions as first-class slide behavior rather than as afterthoughts bolted on through custom scripts.

In practical terms, the MVP should allow authors to describe slides that:

- reveal information in guided teaching steps
- ask a learner a question and represent answer choices clearly
- show feedback based on a learner choice or answer state
- switch visible content based on a bounded interaction state
- structure practice and explanation flows without manual scripting

## MVP Interaction Categories

### Guided Reveals

Guided reveal is the most fundamental interaction category for the MVP. It supports staged explanations, progressive disclosure, and controlled attention.

The MVP should treat guided reveals as a first-class declarative concept for:

- stepwise bullet or region reveal
- staged annotation or emphasis
- progressive explanation sequences
- teacher-controlled or slide-controlled reveal order

Guided reveal belongs in scope because it is useful in almost every teaching deck and does not require broad runtime generality.

### Question And Choice Interactions

The MVP should support at least one clear question flow where a prompt is presented together with a bounded set of answer choices.

This category should cover:

- multiple-choice question slides
- single-correct or multiple-valid answer framing at content level
- explicit answer-choice structures that the runtime can interpret predictably

The product goal is not advanced assessment logic in the MVP. The goal is a stable educational question pattern that can anchor practice and feedback.

### Feedback Reveal

Feedback should be a first-class interaction category rather than a manual visual hack. After an answer selection or defined reveal step, the system should be able to show response-specific or state-specific feedback.

MVP feedback scope should include:

- correct or incorrect response feedback
- explanation text tied to an answer state
- optional staged hints or follow-up commentary

This keeps the interaction model anchored in teaching value rather than bare input handling.

### State-Based Content Switching

The MVP should include a narrow notion of interaction state so the system can switch between a small number of authored content outcomes.

This should support cases such as:

- showing different feedback blocks after a choice
- revealing a hint after a defined step
- toggling between prompt, answer, and explanation states

This is not a general state machine platform. It is a bounded product concept for educational flow transitions.

## Declarative Behavior Boundaries

The MVP should define a clear product boundary between declarative interaction and open-ended scripting.

Declarative interaction should cover:

- reveal sequences
- question definitions and answer-choice structures
- feedback mappings to bounded answer or progression states
- simple state transitions required for teaching flows
- interaction hooks that are intrinsic to supported educational patterns

The MVP should not require authors to write arbitrary JavaScript to achieve these core behaviors.

Custom scripting should remain out of scope for the MVP because it would:

- widen the product into a generic runtime platform
- weaken consistency and predictability across decks
- make interaction behavior harder to review, reuse, and teach

If a future escape hatch is ever introduced, it should come later and under explicit governance as an exception path, not as the default interaction model.

## Relationship To Authored Content

Authored content should describe the pedagogical meaning of an interaction.

At product level, authored content is responsible for:

- the question prompt
- answer choices
- hint text
- feedback text
- revealable explanation steps
- semantic markers that indicate intended learning flow

Authored content should not be responsible for hand-defining low-level event logic, timing systems, or state management code. The content should declare intent; the interaction model should define the supported behavior contract.

## Relationship To Templates

Templates provide structural affordances for interaction, but they are not the interaction model themselves.

For example:

- a template may define that a slide has a question region and a feedback region
- the interaction model defines how those regions are activated, revealed, or switched based on bounded state

This separation matters because the same interaction pattern may appear in multiple templates, and the same template family may support more than one interaction pattern.

Templates therefore own structure, while the interaction model owns allowed behavior classes.

## Relationship To Future Runtime Design

Later implementation work will need runtime mechanisms to interpret the supported interaction model. This document does not define APIs, rendering internals, or storage formats.

What it does define is the product contract those later tasks should preserve:

- keep guided reveals first-class
- keep quiz and feedback behavior narrow and educationally meaningful
- treat bounded interaction state as a tool for learning flow, not general application logic
- avoid making arbitrary scripting the baseline path

## Non-Goals

The MVP interaction model should explicitly exclude:

- general-purpose scripting as the primary authoring path
- open plugin-style behavior injection for slide logic
- complex scoring or assessment engines
- multiplayer or networked collaboration interactions
- drag-and-drop, free-form simulation, or game-like interaction systems
- highly animated non-educational transition effects as product priorities
- broad application-style state orchestration unrelated to teaching flow

These exclusions protect the MVP from becoming too broad before the core educational value is proven.

## Open Questions For Later Technical Design

- How should reveal state be represented technically without leaking runtime complexity into authored content?
- What is the smallest useful feedback model that still supports both live teaching and self-paced review?
- Should short-answer interactions enter the product before or after the first multiple-choice flow is proven?
- How much runtime extensibility is necessary before it starts undermining declarative consistency?
- Which accessibility constraints will most strongly shape reveal, question, and feedback interactions?

## Summary

The MVP interaction model should center on guided reveals, bounded question flows, feedback reveal, and simple state-based content switching. These interactions should be declarative by default, clearly separated from authored content and templates, and tightly scoped to teaching use cases rather than generic runtime ambition.