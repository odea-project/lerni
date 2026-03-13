# Parser And Normalizer MVP Scope

## Purpose

This document describes the intentionally narrow authoring subset implemented by the first parser and normalization slice under TASK-2026-0008.

## Supported Slice

The current MVP parser supports:

- slides separated by a line containing only `---`
- an optional `::slide` directive at the top of a slide with `kind=` and `template=` metadata
- an optional first-level `#` heading that becomes the `title` region
- explicit semantic regions declared with `::region <name>`
- paragraph blocks inside regions
- unordered list blocks using `- item`
- fenced code blocks using triple backticks
- reveal blocks using `::reveal step=<n>` and `::endreveal`
- inferred `question_flow` interactions from `question`, `answer_choices`, and `feedback` regions
- inferred `guided_reveal` interactions from revealed blocks

## Deliberately Unsupported In This Slice

The current parser does not support:

- arbitrary Markdown outside declared semantic regions except the initial title heading
- nested directives beyond the defined reveal block
- multiple declarations of the same region in one slide
- broad authoring syntax coverage for every concept described in the long-term design docs
- template resolution or runtime execution behavior

## Error Behavior

The parser raises explicit errors when:

- content appears outside supported regions
- directives are malformed or unsupported in position
- reveal blocks are not closed
- code fences are not closed
- a slide repeats the same region name

## Why The Slice Is Small

This first implementation exists to establish a trustworthy semantic boundary. It is intentionally smaller than the eventual authoring surface so later template and runtime work can build on explicit, tested behavior rather than on speculative parser breadth.