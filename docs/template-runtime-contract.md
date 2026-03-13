# Template Runtime Contract

## Purpose

The template runtime contract defines how normalized semantic content binds into reusable slide templates after parsing and normalization, but before renderer-specific implementation details take over. Its purpose is to make template resolution predictable, enforceable, and narrow enough that the MVP remains structurally coherent without turning templates into a general layout programming system.

This contract is the layer that answers a practical technical question: given a normalized slide with named regions, blocks, reveal groups, and bounded interaction references, how does the system determine whether a template can accept that content and how it should expose the resulting structure to later rendering code?

## Pipeline Position And Responsibilities

At MVP level, template resolution sits after the semantic document model and before interaction-aware rendering behavior.

The relevant pipeline can be framed as:

1. authored source
2. semantic document model
3. template resolution
4. interaction-aware rendering runtime

Template resolution is responsible for:

- identifying which template contract applies to a slide
- validating whether the normalized slide content satisfies that contract
- binding named regions and structured blocks into the template's expected slots
- determining how required, optional, and unsupported content should be handled
- exposing a stable resolved structure for downstream rendering layers

Template resolution is not responsible for:

- parsing authored source
- inventing missing semantic meaning that was never normalized
- executing interaction state or event behavior
- choosing renderer libraries, component frameworks, or visual styling mechanisms

## Design Principles

### Contract Over Heuristics

Template binding should rely on explicit, reviewable contracts rather than fragile inference. The system should know why a slide matches a template, not guess loosely from arbitrary content shape.

### Semantic Inputs, Structural Outputs

The template layer should consume semantic regions and content blocks, then produce a resolved structural mapping suitable for rendering. It should not require raw Markdown knowledge.

### Predictable Validation

Authors and future tooling should be able to understand why a slide satisfies or violates a template contract. Required content, optional content, and incompatible content should be distinguishable clearly.

### MVP Strictness

The MVP should prefer a small number of well-defined template contracts over highly dynamic composition. Strictness is useful if it improves consistency and author feedback.

### Separation From Interaction Execution

Templates may expose structural affordances for quizzes, reveals, or feedback, but they should not become the system that decides how interaction state transitions execute.

## Template Contract Shape And Slot Semantics

Each template should declare a structural contract made of named slots. These slots are the runtime-facing counterpart to semantic regions from the document model.

At MVP level, a template contract should define:

- template identity
- supported slide kind or intended structural class
- named slots expected by the template
- which slots are required and which are optional
- what categories of semantic content are valid for each slot
- whether certain slot combinations are mutually required or mutually exclusive

Examples of slot names are likely to align with semantic regions such as:

- title
- explanation
- figure
- example
- comparison_left
- comparison_right
- question
- answer_choices
- feedback
- annotation

The key rule is that slots should remain semantically meaningful. A slot should not be a disguised pixel container.

## Binding Model

Binding should map normalized slide regions into template slots according to explicit rules.

In the MVP, binding should proceed conceptually like this:

1. determine slide kind or explicit template intent from the normalized slide
2. select a matching template contract
3. compare the slide's semantic regions and content blocks against the template's declared slots
4. bind compatible regions into the corresponding slots
5. record validation failures, unsupported content, or missing required slots before downstream rendering continues

The result of binding should be a resolved template instance that preserves:

- which template was selected
- which slots were satisfied
- which source regions mapped into which slots
- whether optional regions were omitted
- whether any incompatibilities or fallback conditions occurred

This resolved structure should be specific enough for renderer implementation later, but it should not itself become renderer-specific code.

## Validation Model

Template validation should happen at the point of binding rather than being deferred entirely to later rendering failure.

At MVP level, validation should cover:

- required slot presence
- region-to-slot compatibility
- unsupported extra regions for a given template
- invalid combinations of regions or block categories where the contract disallows them
- template applicability against slide kind or declared structural intent

Validation should not try to solve every future quality issue, but it must be strong enough that the MVP does not silently coerce structurally incompatible slides into misleading layouts.

## Failure And Fallback Behavior

The template runtime contract should define failure behavior explicitly rather than leaving it to renderer accident.

The MVP should distinguish at least three cases:

### Valid Resolution

All required slots are satisfied, all bound regions are compatible, and optional omissions are acceptable.

### Recoverable Incompatibility

The slide mostly matches the template contract, but a small number of issues can be surfaced without hiding the structural intent. This might include optional slot omission or non-fatal extra content that can be reported clearly.

### Hard Contract Failure

Required slots are missing, incompatible content is placed into critical slots, or the slide does not actually satisfy the template's declared structural class. In this case, the system should not pretend the slide resolved correctly.

For the MVP, fallback behavior should remain narrow:

- prefer explicit reporting over silent coercion
- allow only bounded fallback paths that are intentionally documented
- avoid a generic catch-all layout that hides contract problems

This keeps template behavior trustworthy and makes later author feedback possible.

## Relationship To The Semantic Document Model

The semantic document model is the input contract for template resolution.

Template resolution should rely on the document model for:

- slide identity and slide kind
- explicit template intent or normalized template reference
- named semantic regions
- structured block categories within each region
- reveal and interaction references where they affect structural affordances

Template resolution should not need to reopen source parsing or reason about raw author syntax. If template matching depends on details that were never normalized, the document-model boundary is too weak.

## Relationship To Interaction Runtime

Templates may expose slots that are structurally relevant to interaction, such as question, answer_choices, feedback, or annotation. However, the interaction runtime remains responsible for what those slots do over time.

Template resolution may therefore express:

- that a resolved template includes interactive regions
- that certain slots are intended to support reveal or feedback affordances
- that the rendered structure contains the necessary places for interaction-capable content

Template resolution should not define:

- event handling
- state transitions
- answer evaluation behavior
- reveal sequencing logic at runtime

This preserves the separation between structure and behavior established in the earlier product documents.

## Output Of Resolution

The output of template resolution should be a stable resolved structure that downstream rendering code can consume without having to repeat template selection or semantic validation.

At design level, that resolved structure should capture:

- selected template identity
- resolved slot map
- bound semantic content for each slot
- validation status
- any documented fallback or incompatibility notes

That output should be thought of as a runtime-facing structural contract, not as a final renderer tree.

## Non-Goals

The template runtime contract should explicitly not become:

- a rendering-framework selection document
- a CSS or styling system specification
- a general-purpose visual layout builder
- a hidden interaction engine
- an excuse to weaken semantic validation through broad automatic coercion
- a frozen code-level API for a specific implementation stack

These exclusions keep the task focused on the structural contract rather than on downstream implementation choices.

## Open Questions For Implementation Design

- Should explicit template references always win over slide-kind-derived defaults, or should some templates be inferred only when no explicit choice is present?
- How strict should the MVP be about extra unmatched regions that a template does not declare?
- Which fallback conditions are helpful for author ergonomics, and which ones would merely hide structural mistakes?
- How should resolved template output represent validation messages so future tooling can surface them clearly?
- How much slot-level type checking is necessary before template contracts become too rigid for the MVP?

## Summary

The template runtime contract should define a strict but practical binding layer between the semantic document model and downstream rendering code. It should select templates from explicit structural intent, bind normalized regions into semantic slots, validate contract satisfaction, report incompatibilities clearly, and stay separate from both raw rendering choices and interaction execution behavior.