# Semantic Document Model

## Purpose

The semantic document model is the normalization layer between authored source and downstream interpretation. Its job is to turn Markdown-first slide source plus project-specific extensions into a stable internal representation that preserves teaching intent without leaking raw author syntax into template resolution or interaction execution.

This model exists because authored source is optimized for human readability, while later systems need a cleaner and more explicit contract. The document model is therefore not the authoring surface, not the template system, and not the interaction runtime. It is the semantic bridge between them.

## Pipeline Position And Parse Boundary

At MVP level, the processing pipeline should be understood as four distinct layers:

1. authored source
2. semantic document model
3. template resolution
4. interaction and rendering runtime

The parse boundary sits between authored source and the semantic document model.

Before the boundary:

- the source remains author-oriented
- Markdown carries most prose and simple structure
- project-specific extensions express slide, region, reveal, question, and feedback intent
- some syntactic variation may remain acceptable if it improves author ergonomics

After the boundary:

- the structure should be normalized into a predictable semantic form
- equivalent author expressions should map to the same conceptual entities
- downstream systems should not need to reason about raw Markdown quirks or author shorthand
- slide meaning should be explicit enough for template and interaction layers to consume consistently

The semantic document model should therefore be the first system-facing representation that is stable enough to support validation, template binding, and interaction interpretation.

## Design Principles

### Normalize Meaning, Not Surface Syntax

The model should preserve what the author meant, not every incidental detail of how it was written. Two different source forms that express the same slide meaning should normalize to the same semantic structure where practical.

### Stay Above Rendering

The document model should not become a rendering tree. It should not describe geometry, DOM structure, CSS strategy, or screen composition details.

### Stay Below Product Vagueness

The model must be more concrete than the product documents. It should identify explicit entities and relationships that later implementation work can rely on.

### Preserve Teaching Intent

The model should retain the parts of source that matter to teaching flow: slide kind, semantic regions, reveal grouping, question structure, feedback intent, and bounded interaction references.

### Keep Layer Boundaries Hard

The model should not absorb template-specific layout rules or runtime-specific state execution. It should carry the semantic inputs those later layers need, no more.

## Core Semantic Entities

The MVP document model should remain small but explicit. A useful baseline entity set is:

### Deck

The deck is the top-level authored teaching unit. It contains ordered slides plus deck-scoped metadata that affects interpretation globally.

The deck should be able to express:

- deck identity
- optional deck metadata
- ordered slide sequence
- deck-level defaults that later layers may inherit

### Slide

The slide is the primary unit of authored teaching flow. A slide should exist as a semantic object rather than as a bag of raw Markdown fragments.

At minimum, a slide should be able to express:

- slide identity or stable reference
- slide kind or structural intent
- optional template intent or template reference
- ordered semantic content regions
- slide-level metadata
- reveal and interaction references associated with the slide

### Region

A region is a named semantic content area within a slide. Regions are the main bridge between author intent and later template binding.

Examples include:

- title
- explanation
- example
- figure
- question
- answer_choices
- feedback
- annotation

Regions should be semantic rather than purely visual. A region says what role content plays, not where pixels should go.

### Block

Within a region, content may still need structure beyond raw text. The model should allow normalized blocks for content types such as prose, lists, code, figures, notes, definitions, prompts, or feedback bodies.

Blocks matter because downstream systems should be able to distinguish conceptually different content forms without reparsing raw Markdown.

### Reveal Group

The model should represent reveal intent as a semantic structure rather than as animation instructions. A reveal group identifies content that belongs to a staged disclosure step or ordered explanation sequence.

This entity should preserve:

- reveal membership
- reveal ordering or step association
- the relationship between revealable content and its containing slide or region

It should not define actual runtime animation mechanics.

### Interaction Reference

The document model should carry bounded references to supported interaction concepts, such as question flow, answer-choice structures, feedback mappings, or simple state-dependent content switching.

An interaction reference should indicate that a slide contains interpretable interaction semantics. It should not itself become the full runtime state machine.

## Normalization Rules And Preserved Author Intent

The semantic document model should perform enough normalization to make later systems predictable, while still preserving the author's teaching meaning.

The model should preserve:

- ordered deck and slide flow
- slide kind or structural intent
- template intent where explicitly authored
- named semantic regions
- semantic content type distinctions where they matter later
- reveal grouping and ordering intent
- question, answer, and feedback intent
- slide and deck metadata that affects interpretation

The model should abstract away:

- incidental Markdown syntax differences that express the same meaning
- low-level formatting trivia that does not affect semantic interpretation
- renderer-specific structure
- presentation-specific scripting details
- layout geometry or visual placement instructions

The normalization goal is not to erase nuance. It is to remove accidental complexity so later layers consume consistent meaning.

## Relationship To Templates

Templates consume the semantic document model; they do not replace it.

The model should provide templates with:

- slide kind or template intent
- named semantic regions
- structured content blocks within those regions
- reveal and interaction references where relevant to structural affordances

Templates should remain responsible for:

- reusable structural layout patterns
- required and optional slot expectations
- the arrangement of regions into a coherent slide pattern

This means the document model should know that a slide has a question region and a feedback region, but it should not know whether those appear left-right, stacked, tabbed, or otherwise arranged by a template.

## Relationship To Interaction Definitions

The semantic document model should expose the authored meaning needed for interaction, while leaving execution behavior to later runtime design.

The model should preserve concepts such as:

- a revealable step sequence exists
- a question prompt has answer choices
- feedback blocks are associated with certain outcomes or states
- some content is conditionally associated with a bounded learning-flow state

The model should not define:

- runtime event handling
- transition algorithms
- widget behavior
- persistence or scoring logic
- arbitrary code hooks

This keeps the model expressive enough for interaction-aware decks without allowing it to become a hidden runtime API.

## Model Stability And Extensibility

The MVP should prefer a narrow, stable semantic vocabulary over a highly dynamic node system. That does not mean the model must be rigid forever, but it should begin with a constrained set of entities that map directly to the product's intended teaching patterns.

Extensibility should therefore follow two rules:

- new semantic entity types should only be introduced when existing entities cannot represent an important teaching pattern cleanly
- future extension should preserve normalization discipline rather than exposing arbitrary nested structures by default

This makes the model easier to validate, easier to implement, and easier to reason about across authoring, templates, and runtime.

## Non-Goals

The semantic document model should explicitly not become:

- a raw parser AST exposed as the main system contract
- a rendering tree or layout description format
- a template contract in disguise
- an interaction execution engine
- a general-purpose content graph for every conceivable presentation use case
- a code-level API specification frozen too early

These exclusions matter because the document model is only valuable if it protects the boundaries between layers rather than dissolving them.

## Open Questions For Implementation Design

- How much block-level normalization is necessary before the model becomes too heavy for the MVP?
- Which slide and deck metadata fields should be first-class in normalization, and which should remain opaque for later tasks?
- Should template intent be represented as an explicit normalized reference, a slide-kind-derived default, or both?
- How should cross-slide references or reusable authored fragments enter the model, if they are needed at all?
- What is the smallest normalized representation that still supports high-quality validation feedback to authors?

## Summary

The semantic document model should be the stable, system-facing representation that sits between author-oriented source and downstream template or runtime layers. It should normalize deck, slide, region, block, reveal, and bounded interaction meaning while staying clearly separate from rendering layout and runtime execution behavior.