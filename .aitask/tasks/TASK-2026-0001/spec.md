# Task Specification

## Context

This repository now has governance for AI-assisted work, but it still lacks a formal product-definition document. The project direction has now been clarified at a high level: the product is intended to be a presentation and learning platform for lecture slides, conceptually adjacent to reveal.js but differentiated by Markdown-first authoring, lightweight design, template-driven slides, interaction-native learning support, and a stronger didactic orientation.

Without a formal vision document, future architecture, authoring-model, and product-scope decisions risk drifting or being defined implicitly in implementation work. This task exists to create a clear foundational product description before product code begins.

## Objective

Produce the first formal project description and product vision document for this repository, expected at `docs/project-vision.md`, so future contributors can understand what the product is, why it exists, who it serves, how it differs from tools like reveal.js, and what the likely MVP and non-goals are.

## In Scope

- define the product identity in clear repository documentation
- articulate the problem statement and intended value proposition
- describe target users and teaching-oriented use cases
- explain how the product differs from reveal.js and similar tools
- define design principles for authoring, templates, and interaction
- identify likely MVP scope and explicit non-goals
- capture open strategic questions that should guide later design work

## Out Of Scope

- implementing product code, parsers, renderers, templates, or widgets
- committing to detailed technical architecture beyond product-level direction
- selecting exact runtime, framework, or plugin-system implementation details
- producing polished marketing copy for external publication
- replacing future ADRs for architecture decisions that need stronger technical commitments

## Assumptions

- the current project intent supplied by the requester is authoritative enough to draft a first formal vision
- the first vision document is an internal foundational document, not a final public specification
- architectural decisions beyond product direction can be deferred to later tasks and ADRs
- a lightweight documentation path under `docs/` is the right location for the initial vision artifact

## Constraints

- keep the document concise, structured, and usable as a decision anchor
- preserve a clear separation between product vision and implementation detail
- do not let the document collapse into generic slide-tool language
- explicitly describe didactic and interaction-native differentiators
- keep claims honest where product details are still undecided

## Deliverables

- `docs/project-vision.md` containing the first formal product description and vision
- updated task records capturing execution, evidence, review, and closure

## Key Questions To Answer

- What is the product, in one precise description?
- Why should this project exist instead of using an existing presentation framework directly?
- Which authoring problems does Markdown-first, template-driven slide design solve?
- Which kinds of teaching and workshop scenarios should the product support especially well?
- How should content, layout templates, and interaction behavior be separated conceptually?
- What kinds of interactive learning elements belong in scope for the initial product direction?
- What belongs in the MVP, and what should be explicitly out of scope for now?
- Which strategic questions remain open after the first vision document is written?

## Suggested Structure Of The Target Document

1. Project overview
2. Problem statement
3. Vision
4. Product principles
5. Core differentiators
6. Primary use cases
7. Target users
8. Authoring model direction
9. Template and interaction model direction
10. MVP direction
11. Non-goals and out-of-scope items
12. Open strategic questions

## Acceptance Criteria

- `docs/project-vision.md` exists and is readable as a standalone foundational document
- the document clearly states what the product is and why it exists
- the document explicitly distinguishes the product from reveal.js-style slide tooling
- Markdown-first authoring, lightweight core, template-driven slides, interaction-native learning, and didactic orientation are all covered explicitly
- the document includes concrete example use cases for lectures, workshops, quizzes, and visual explanation slides
- the document defines likely MVP boundaries and explicit non-goals
- open strategic questions are captured instead of hidden behind vague wording
- task evidence shows the reasoning, review, and approval trail for the resulting document

## Dependencies

- human approval to start execution
- reviewer availability for product-definition review
- stable repository path for the target document under `docs/`

## Review Expectations

- review for clarity, scope discipline, and differentiation quality
- verify that the document is product-defining rather than implementation-heavy
- verify that the MVP direction is specific enough to guide later tasks
- verify that non-goals prevent premature scope expansion
- verify that unresolved questions are made explicit rather than implied away

## Rollback Plan

If the drafted vision document proves misleading or low quality, revert the document changes, retain the task evidence, and reopen the task in review or specified state with updated guidance.

## Required Evidence

- task metadata and specification records
- risk assessment rationale
- execution log entries describing document framing and assumptions
- review decision and findings
- final vision document diff or path reference

## Approvals Needed

- `approver`: `human:repository.owner` before execution starts