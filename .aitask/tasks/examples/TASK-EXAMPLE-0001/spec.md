# Task Specification

## Context

The repository needs a production-grade `.aitask` operating system so future AI-assisted work can be governed, reviewed, and audited without relying on undocumented practices.

## Objective

Establish repository-local governance, templates, schemas, examples, and CI validation for AI task management.

## In Scope

- `.aitask` governance documentation
- machine-readable schemas
- templates for repeatable records
- a complete example task
- GitHub templates and workflows

## Out Of Scope

- changing organization-level GitHub settings directly
- integrating external approval systems
- modifying unrelated product code

## Assumptions

- repository maintainers will apply manual GitHub hardening settings
- human roles will be mapped to real team identities after bootstrap

## Constraints

- keep the framework human-readable and machine-validatable
- minimize hidden state
- preserve existing repository content

## Deliverables

- complete `.aitask/` framework
- GitHub-native templates and workflows
- example records showing full lifecycle traceability

## Acceptance Criteria

- required directory structure and templates exist
- task metadata validates against schema
- validation workflow runs in GitHub Actions
- documentation distinguishes file-enforced and manually enforced controls

## Dependencies

- human approver availability
- repository branch protection configuration by maintainers

## Rollback Plan

Revert the bootstrap commit if the framework proves unusable, then open a follow-up task documenting the reason and replacement approach.

## Required Evidence

- repository diff
- validation workflow definition
- example task evidence index
- review and audit records

## Approvals Needed

- human:repo.approver for execution approval