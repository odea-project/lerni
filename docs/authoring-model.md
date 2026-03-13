# Authoring Model

## Purpose

The authoring model defines how people write slide content for this project. Its job is not to describe parser internals or runtime behavior. Its job is to make the authored source understandable, structured, and suitable for teaching-oriented slide design.

The central design requirement is that authors should be able to express learning content, slide structure, and teaching intent without being pushed into raw HTML, ad-hoc CSS layout work, or presentation-specific scripting.

## Design Principles

### Markdown-First, Not Markdown-Only

Markdown should remain the primary writing surface because it is readable, familiar, and well suited for structured text. At the same time, plain Markdown alone is not expressive enough for all of the concepts this product needs. The authoring model therefore starts from Markdown and extends it with project-specific syntax only where educational slide authoring actually needs more structure.

### Semantic Before Visual

Authors should describe meaning and teaching intent first. The source should communicate what a slide section is, what role a block plays, or what kind of reveal or feedback is intended before it communicates low-level layout or styling instructions.

### Readable By Authors, Not Only By Implementers

The authored source should stay legible to lecturers, trainers, and technical educators who are not frontend developers. If the authoring format becomes difficult to read without knowing implementation details, the model has failed one of its core goals.

### Minimal Escape Into Raw Markup

Raw HTML or low-level custom markup may still exist as an escape hatch eventually, but it should not be the primary authoring path. The preferred path is semantic source that maps cleanly to templates and interactions.

### Clear Separation Of Concerns

The authoring model is responsible for content and semantic intent. It is not responsible for final visual composition, low-level rendering mechanics, or broad interaction runtime design.

## What Authors Need To Express

At minimum, the authoring model needs to support expression of the following conceptual units:

- slide boundaries
- slide purpose or slide kind
- headings, subheadings, and explanatory text
- semantic content blocks such as examples, questions, notes, or definitions
- references to template choice or template intent
- reveal intent or staged disclosure intent
- placeholders for interactive elements or feedback regions
- metadata that influences interpretation at slide level

These concepts should be expressible in a way that still looks like authored teaching material rather than a UI configuration file.

## Role Of Markdown

Markdown should carry the parts of the source where it already works naturally well:

- prose
- headings
- lists
- emphasis
- code blocks
- quotations
- simple links and references
- tables where they remain readable

Markdown is valuable because it keeps educational content compact and maintainable. It should remain the default language of the source rather than being buried under a heavy custom wrapper.

## Role Of Project-Specific Extensions

Project-specific extensions should exist only for concepts that plain Markdown cannot express cleanly enough. Their purpose is not to create a general-purpose slide programming language. Their purpose is to represent teaching- and slide-specific semantics explicitly.

Extensions are likely needed for:

- slide-level declarations
- template selection or template intent
- named content regions
- staged reveal intent
- question and answer structures
- feedback blocks
- parameterized or state-sensitive content hooks

The guiding rule is that extensions should expose semantic concepts, not arbitrary rendering instructions.

## Semantic Layers In The Source

The authoring model should distinguish several conceptual layers even if they later appear in a single source file.

### Content Layer

This is the teaching substance itself: explanations, examples, questions, prompts, formulas, code, and narrative flow.

### Structural Layer

This describes how content is grouped into slides, sections, regions, and ordered steps. It should tell the system what belongs together without requiring the author to define the final layout directly.

### Intent Layer

This captures author intent that matters for presentation behavior or teaching flow, such as “this block is feedback,” “this slide uses a comparison pattern,” or “this section is revealed in stages.”

The purpose of these layers is not to make authoring more abstract for its own sake. It is to keep the source expressive while enabling later template and interaction systems to do their work without demanding low-level author control.

## What Authors Should Not Need To Write

The authoring model should actively reduce the need for authors to write the following kinds of detail manually:

- raw layout geometry
- hand-crafted column or spacing structures
- repeated visual scaffolding for common slide types
- presentation-specific JavaScript for routine reveals or quiz feedback
- renderer-specific DOM structure
- implementation-centric configuration for ordinary educational slide patterns

If ordinary lecture or workshop slides still require those things routinely, the product has failed to deliver on its core promise.

## Relationship To Templates

The authoring model should be able to refer to template intent, but it should not become the template system itself.

Authoring should answer questions like:

- what kind of content is this?
- what kind of slide pattern is intended?
- which content belongs in which semantic region?

The template system should answer questions like:

- how is this semantic structure laid out visually?
- which regions exist in a reusable slide pattern?
- how should repeated structure be rendered consistently?

This means authors may indicate that a slide is a comparison slide or a quiz-feedback slide, but they should not need to manually rebuild the template structure every time.

## Relationship To Interactions

The authoring model should allow authors to express interaction intent, but it should not own the full interaction runtime.

Authoring should be able to represent concepts such as:

- this slide contains a quiz
- this block is feedback
- this content is revealed in stages
- this example depends on a parameter or state transition

The interaction model should later define:

- what interaction classes exist
- how state transitions behave
- how feedback is triggered or displayed
- what remains declarative and what requires controlled extensibility

The key boundary is that authoring captures meaning and intent; interaction design captures behavior classes and runtime expectations.

## Readability And Ergonomics

The source should remain readable in three ways:

- locally: one slide should be understandable on its own
- structurally: the flow of a deck should be easy to scan
- semantically: special constructs should communicate intent instead of looking like opaque implementation directives

Good ergonomics means an author can revisit a deck later and still understand the learning logic quickly. It also means common authoring patterns should feel consistent rather than improvised.

## Example Authoring Patterns

The exact syntax is still open, but the model should support patterns conceptually like these:

- a lecture slide with title, explanation, and example block
- a comparison slide with two semantic regions rather than two manually coded columns
- a quiz slide that declares question, answer choices, and feedback blocks semantically
- a visual explanation slide that references a known slide kind with predefined content regions
- a stepwise explanation where reveal intent is declared without hand-written animation logic

These examples matter because they show the kind of authoring experience the product is trying to optimize.

## Non-Goals

The authoring model should not try to become:

- a full programming language for slide behavior
- a low-level renderer configuration format
- a general-purpose page builder syntax
- a substitute for future technical parser design documentation
- a place where every visual detail must be declared explicitly

## Open Questions

- How much slide-level metadata should be author-visible in the first version?
- Which semantic blocks should be first-class in the initial authoring surface?
- How should optional escape hatches be introduced without undermining the primary semantic model?
- Should one source file represent one deck only, or should authoring units be composable across files?
- How much authoring structure should be standardized before template work begins?

## Summary

The authoring model should let authors write educational slide content in a Markdown-first, semantically structured, and readable way. It should expose teaching-relevant intent clearly, minimize manual frontend work, and maintain a hard boundary between authored meaning and lower-level implementation detail.