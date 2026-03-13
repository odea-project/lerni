# AI Task Governance Charter

## Purpose

This charter establishes the minimum governance standard for AI-assisted work in this repository. The objective is to enable productive use of AI agents while preserving human accountability, traceability, and defensible control evidence suitable for regulated environments.

## Scope

This charter applies to:

- repository changes proposed, drafted, or executed with AI assistance
- governance, documentation, configuration, code, and automation changes tracked through `.aitask`
- humans, agents, and service identities interacting with governed task records

## Governance outcomes

- every significant AI-assisted change is traceable to an approved task
- risk is classified before execution
- incompatible duties are separated for higher-risk work
- evidence is captured as work occurs
- reviews and audits can reconstruct what happened and why

## Authority

Repository maintainers own enforcement of repository settings and branch controls. Approvers and auditors exercise delegated control authority according to the approval and control matrices.

## Operating principles

- default deny for risky actions
- explicit human ownership of approvals and risk acceptance
- additive records over silent overwrites
- minimal ambiguity in task metadata
- proportionate controls by risk tier