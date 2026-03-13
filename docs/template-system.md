# Template System

## Purpose

The template system exists to make slide structure reusable, consistent, and teaching-oriented. Its role is not to give authors an unrestricted layout canvas. Its role is to provide named slide patterns with stable semantic regions so that recurring educational structures do not have to be rebuilt manually.

In this product, templates are one of the main ways the framework distinguishes itself from generic presentation tooling. They turn recurring pedagogical patterns into reusable building blocks rather than one-off layout work.

## Design Principles

### Reuse Over Ad-Hoc Composition

Templates should replace repeated custom layout work for common slide types. If authors still need to reconstruct the same two-column explanation slide, comparison slide, or quiz-feedback slide from scratch every time, the system is not doing enough.

### Opinionated Enough To Improve Quality

Templates should not be so loose that they become a generic page builder abstraction. They should encode useful structure and constrain slide composition enough to support clearer, more consistent teaching material.

### Lightweight Core

The template system should stay small and comprehensible in the MVP. The product does not need a large library of highly dynamic layout primitives before it proves the value of a focused core set of educational slide patterns.

### Separation Of Concerns

Templates are responsible for reusable structural patterns and region contracts. They are not responsible for owning the authored content itself, and they should not absorb all interaction logic.

### Educational Relevance First

Template value should be evaluated primarily by whether it improves lecture, workshop, explanation, and feedback-driven teaching flows, not by how much visual freedom it exposes.

## What A Template Is

A template is a reusable slide pattern that defines:

- a structural intent
- a set of expected content regions or slots
- a predictable relationship between those regions
- a stable rendering pattern for a class of educational slides

Examples of structural intent include explanation, comparison, question-and-feedback, figure-led explanation, or staged annotation.

A template is therefore more than a visual style preset. It is a reusable semantic layout contract for a kind of slide.

## What A Template Is Not

A template is not:

- a free-form screen editor
- an arbitrary nested container system
- a full runtime behavior definition
- a substitute for authored content semantics
- a generic plugin platform by default

Those exclusions matter because the product direction depends on keeping templates meaningful and bounded.

## Template Responsibilities

At product level, templates should be responsible for:

- defining reusable slide patterns
- defining expected content regions or slots
- establishing how a slide kind is structurally organized
- supporting visual consistency across decks
- reducing repeated layout work for authors

Templates should not be responsible for:

- creating the content itself
- making authors hand-author low-level geometry
- owning broad interaction runtime state
- replacing the authoring model with configuration-heavy layout logic

## Content Regions And Slot Concepts

Templates should expose named regions or slots that correspond to meaningful author intent, not purely presentational fragments.

Good region concepts are likely to look like:

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

The important property is semantic clarity. A region should tell both the author and the system what kind of content belongs there.

Poor region concepts would be highly visual but semantically weak, such as arbitrary x/y positioning or unnamed boxes that force authors to remember layout meaning themselves.

## Relationship To The Authoring Model

The authoring model should let authors indicate template intent and supply content for template regions. The template system should then provide the reusable structural pattern that interprets that intent.

This means:

- authoring defines content and semantic purpose
- templates define reusable structural arrangement

An author might indicate that a slide uses a comparison template and then provide content for the left and right regions. The template system should own the reusable structure, not force the author to simulate it manually.

## Relationship To The Interaction Model

Templates must coexist with interaction, but they should not absorb all behavior logic. A quiz-feedback template, for example, may define that a question region and a feedback region exist, but it should not by itself define the full runtime interaction system.

The interaction model should later determine:

- how state changes occur
- how feedback is triggered
- how reveals behave over time
- what remains declarative and what requires controlled extensibility

The template system should therefore define structural affordances for interaction without becoming the interaction engine.

## MVP Template Scope

The MVP should start with a narrow set of high-value templates rather than a large taxonomy.

Reasonable early candidates include:

- title and overview slide
- explanation slide with supporting figure
- comparison slide
- example slide
- code-and-commentary slide
- quiz-and-feedback slide
- staged explanation or annotation slide

The goal of the MVP is not to cover every slide type. The goal is to prove that reusable, semantically meaningful templates reduce authoring friction for educational material.

## Template Contract At Product Level

The product-level template contract should answer these questions consistently:

- what type of slide pattern is this?
- which semantic regions are expected?
- which regions are required versus optional?
- how much content variation should a template tolerate before a different template is needed?
- how do templates stay stable enough to be reusable across many decks?

This contract should remain conceptual at this stage. Exact file formats, API signatures, and runtime representations belong to later technical design work.

## Examples Of Template Categories

### Explanation Templates

For concept introduction, theory explanation, figure-supported explanation, and structured walkthroughs.

### Comparison Templates

For contrasting approaches, before-versus-after explanations, concept-versus-example layouts, or alternative solution framing.

### Practice And Feedback Templates

For quizzes, prompts, answer-choice layouts, and guided feedback display.

### Technical Teaching Templates

For code-and-explanation slides, formula-with-interpretation slides, or stepwise annotation of technical material.

### Workshop Flow Templates

For task instructions, staged reveals, guided checkpoints, and reflection prompts.

## Non-Goals

The template system should not try to become:

- a general-purpose visual builder
- a layout engine optimized for every possible presentation style
- a substitute for the interaction runtime
- a place to lock in low-level rendering APIs prematurely
- a giant template catalogue before the MVP proves itself

## Open Questions

- How many templates are enough for the MVP to demonstrate real value?
- How opinionated should required versus optional regions be?
- Should templates be versioned or packaged later, and if so, how?
- How much variation should one template tolerate before a second template is justified?
- Which educational slide classes deserve first-class templates from day one?

## Summary

The template system should provide reusable, semantically meaningful slide patterns that reduce layout friction and improve consistency for educational presentations. It should stay opinionated, lightweight, and clearly separated from both authored content and the future interaction runtime.