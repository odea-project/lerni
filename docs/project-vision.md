# Project Vision

## Project Overview

This project is a Markdown-first presentation and learning framework for lecture slides, workshops, and structured teaching material. It is intended to help authors create clear, reusable, and interaction-capable slide experiences without centering the authoring process on raw HTML, custom CSS layout work, or presentation-specific scripting.

The product sits near the same problem space as tools like reveal.js, but it is not intended to be just another generic slide engine. Its center of gravity is educational authoring: content structure, reusable slide patterns, didactically meaningful interaction, and a lightweight core that stays understandable over time.

## Problem Statement

Many slide tools are strong at presentation delivery but weak at teaching-oriented authoring discipline. Authors often end up doing one or more of the following:

- mixing teaching content with layout implementation details
- rebuilding the same slide patterns manually from deck to deck
- embedding ad-hoc interaction logic that is hard to maintain and reuse
- optimizing for visual slides rather than guided learning experiences

This creates friction for educators, workshop facilitators, and technical instructors who need more than a sequence of static slides. They need a system that helps them express learning structure, repeated pedagogical patterns, and interactive moments in a way that remains readable and maintainable.

## Vision

The vision is to provide a lean framework for writing presentation-based learning material in a semantic, reusable, and interaction-aware way.

Authors should be able to:

- write slides primarily in Markdown extended with project-specific syntax
- assemble slides from reusable templates rather than manual layout construction
- declare interactive learning behavior without dropping immediately into arbitrary frontend code
- produce slide decks that support explanation, questioning, feedback, and guided progression

The framework should make it easier to build learning material that is pedagogically structured, visually consistent, and technically maintainable.

## Product Principles

### Content Over Manual Frontend Work

Authors should spend most of their effort on meaning, explanation, sequence, and learning logic. Raw HTML, CSS, and bespoke layout work should be the exception rather than the default.

### Reusable Templates Over One-Off Layout Hacks

Common slide forms should be expressed as named, reusable templates. A lecture author should not have to reconstruct a two-column explanation slide, comparison slide, or quiz-feedback layout every time from scratch.

### Declarative Interaction Over Ad-Hoc Scripting

Interactive behavior should be described in a structured and semantically meaningful way where possible. The long-term direction is to make common teaching interactions expressible without requiring slide authors to write presentation-specific JavaScript for each deck.

### Maintainable Structure Over Presentation-Specific Complexity

The product should remain lean. New features should strengthen clarity and reuse, not turn the framework into a sprawling presentation platform with a complex operational center.

### Strong Author Ergonomics

The authoring model should be easy to read, easy to teach, and easy to revisit later. A slide source file should communicate what the author is trying to teach, not just how the screen is arranged.

### Consistency In Slide Design

Templates, semantic structure, and constrained interaction models should help authors create slide decks that feel coherent rather than improvised page by page.

## Core Differentiators

### Not A reveal.js Clone

The project may share some presentation concerns with reveal.js, but its goal is different. reveal.js is a general-purpose presentation framework. This project is aimed more specifically at presentation-based learning and teaching workflows.

### Template-Driven Slide Construction

Instead of treating each slide as a largely free-form HTML canvas, the framework should prefer reusable templates with clear semantics. This supports consistency, maintainability, and faster authoring.

### Interaction-Native Learning Model

Interactivity is not an add-on. The framework should treat quizzes, dynamic feedback, guided reveals, and other teaching-oriented interactions as first-class design targets.

### Stronger Separation Of Concerns

The product direction favors a clearer split between:

- content
- layout templates
- interactive behavior

This is important both for maintainability and for future extensibility.

### Didactic Orientation

The product is not merely trying to display slides. It should help authors build teaching material that supports explanation, practice, guided attention, and structured learning progression.

## Primary Use Cases

### Classical Lecture Slides

Structured lecture decks with headings, definitions, examples, figures, comparison layouts, and progressive reveals.

### Interactive Teaching Slides

Slides that ask a question, collect or display a choice, and reveal guided feedback in the flow of the teaching session.

### Quizzes With Dynamic Feedback

Slides where answer selection, parameterized values, or staged hints change what the learner sees next.

### Visual Explanation Slides

Reusable layouts for diagrams, code-plus-explanation, figure-with-commentary, or side-by-side conceptual comparisons.

### Workshop Material With Guided Interaction

Instructor-led or self-paced workshop slides where participants move through tasks, prompts, reveals, and feedback in a structured way.

### Scientific And Technical Teaching Content

Teaching material that combines explanation, formulas, figures, code, and interactive checks in a consistent structure.

## Target Users

Primary target users likely include:

- lecturers in higher education
- technical trainers and workshop facilitators
- instructors producing structured teaching decks
- authors of scientific or technical learning material

Secondary target users may include teams that need reusable internal teaching material, onboarding slide flows, or workshop content with interaction built in.

## Authoring Model Direction

The authoring model should be Markdown-first, but not Markdown-only in the narrowest sense. Plain Markdown is too limited to express all of the structure and interactivity this project cares about, so the long-term direction is Markdown extended by project-specific syntax.

That syntax should help authors express concepts such as:

- slide types or template selection
- semantic content regions
- reveal sequencing
- questions and answer structures
- feedback blocks
- parameter-driven or state-driven interactive elements

The important principle is that the syntax should stay readable and author-oriented, not become an opaque programming language disguised as markup.

## Template And Interaction Model Direction

Templates should define common slide structures and content regions. Examples might include:

- two-column explanation slide with header and figure
- concept-versus-example slide
- quiz on the left with feedback on the right
- code sample with staged annotation
- visual explanation slide with predefined emphasis regions

The interaction model should support educational use cases first. Likely interaction forms include:

- guided reveals
- multiple-choice or short-answer quiz flows
- dynamic feedback text
- state-based content switching
- parameter-driven examples or demonstrations

The product direction should prefer declarative patterns for these interactions before exposing low-level custom behavior.

## MVP Direction

The initial MVP should probably focus on a narrow but strong core.

Likely MVP scope:

- Markdown-first slide authoring with a small project-specific extension model
- a minimal but well-designed template system
- a focused set of high-value educational slide patterns
- guided reveals and at least one quiz or feedback interaction model
- consistent rendering of lecture and workshop-oriented decks
- clear separation between content source and template behavior

The MVP should aim to prove that the product can generate meaningful educational presentations with much less layout friction than a generic presentation framework.

## Non-Goals For Now

At this stage, the following should be treated as out of scope unless later tasks change that decision:

- becoming a full general-purpose website or app framework
- supporting unlimited free-form visual composition as a primary authoring model
- solving every presentation use case outside teaching and structured explanation
- exposing a broad, low-level scripting model as the main path to interactivity
- building a large platform with heavy runtime complexity before the core authoring model is clear
- optimizing first for branding, animations, or marketing presentations over learning workflows

## Open Strategic Questions

- Who is the primary target user for the first release: lecturers, workshop facilitators, or technical trainers more broadly?
- How opinionated should the template system be in the first version?
- How far should declarative interaction go before custom scripting is allowed?
- Should templates be repository-local, package-based, or both?
- What is the right boundary between core functionality and future plugin or extension mechanisms?
- Which single educational interaction model is the most important to prove early in the MVP?
- How much rendering and export flexibility is necessary for the first useful release?

## Summary

The product direction is a lightweight, Markdown-first framework for creating presentation-based learning material through reusable templates and interaction-oriented teaching structures. Its purpose is not just to render slides, but to help authors build clearer, more reusable, and more pedagogically meaningful presentation experiences.