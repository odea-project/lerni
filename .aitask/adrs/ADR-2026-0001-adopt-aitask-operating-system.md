# ADR-2026-0001 Adopt The .aitask Operating System

- status: accepted
- date: 2026-03-13
- deciders:
  - human:repo.approver
  - human:repo.maintainer
- consulted:
  - human:governance.reviewer
- informed:
  - human:repository.owner
- supersedes: none
- superseded_by: none

## Context

The repository lacked a durable, auditable operating model for AI-assisted work. Future use of AI agents needs explicit governance artifacts, lifecycle controls, and evidence requirements.

## Decision

Adopt the `.aitask` operating system in-repository as the canonical mechanism for proposing, approving, executing, reviewing, and auditing AI-assisted work.

## Consequences

- contributors must open governed tasks for significant AI-assisted work
- repository maintainers must enforce the documented GitHub settings manually
- AI agents can be used productively, but within explicit task-level bounds and human approvals