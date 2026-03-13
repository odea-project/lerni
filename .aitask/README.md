# .aitask Operating System

`.aitask` is the repository operating system for proposing, approving, executing, reviewing, and auditing AI-assisted work under explicit governance. It is designed for repositories that expect frequent AI-agent participation but require deterministic workflows, strong traceability, and clear human accountability.

This framework separates:

- policy in `.aitask/governance/`
- procedure in `.aitask/README.md`, `.aitask/lifecycle.md`, `.aitask/conventions.md`, and templates
- records in `.aitask/tasks/`, `.aitask/adrs/`, `.aitask/audits/`, and `.aitask/reports/`

## Who this is for

- requesters proposing work
- human and agent proposers drafting task records
- executors performing approved work
- reviewers and approvers applying control gates
- auditors inspecting the completeness and integrity of records
- repository maintainers enforcing repository settings and branch protection

## Task lifecycle

Every AI task has a canonical metadata file at `.aitask/tasks/<TASK-ID>/task.yaml` and must move through the lifecycle defined in `.aitask/lifecycle.md`.

Standard statuses:

- `proposed`
- `triaged`
- `specified`
- `risk-assessed`
- `approved`
- `in-progress`
- `in-review`
- `accepted`
- `rejected`
- `closed`
- `superseded`
- `archived`

Transition rules, mandatory artifacts, and closure conditions are documented in `.aitask/lifecycle.md`.

## How to create a new task

1. Create a folder at `.aitask/tasks/TASK-YYYY-NNNN/`.
2. Copy the templates from `.aitask/templates/` into the task folder.
3. Populate `task.yaml` first. This is the canonical machine-readable record.
4. Draft `spec.md` and `risk.md`.
5. Obtain the approvals required by the risk tier and update `task.yaml`.
6. Only after approval, begin execution and append entries to `execution-log.md`.
7. Complete review, audit, and closure records before marking the task `closed`.

## How AI agents must operate

AI agents are subject to `.aitask/governance/agent-operation-policy.md` and must:

- read `task.yaml`, `spec.md`, `risk.md`, and any linked ADRs before acting
- stay within `allowed_agent_actions`
- refuse actions listed in `prohibited_agent_actions`
- log meaningful commands, decisions, assumptions, uncertainty, and deviations in `execution-log.md`
- stop for human approval whenever the task, policy, or risk tier requires it
- create additive records rather than silently rewriting history

## What requires human approval

Human approval is mandatory for:

- all `medium`, `high`, and `critical` tasks before execution
- any task that changes governance policy, repository protection settings, security controls, privacy posture, production infrastructure, or release configuration
- any exception or waiver
- any architectural decision that requires a new ADR or materially updates an existing ADR
- any action outside the declared task scope or outside `allowed_agent_actions`

`critical` tasks must not be autonomously executed by an agent. Agents may assist only within tightly bounded, human-directed steps.

## Where audit records live

- task-specific review and audit records live in each task folder
- central audit materials live in `.aitask/audits/`
- repository-level summaries and periodic reports live in `.aitask/reports/`

## How ADRs connect to tasks

Tasks link ADRs through the `linked_adr` field in `task.yaml`. The ADR record captures the decision itself; the task record captures the proposal, execution, and evidence trail. Architectural or governance-relevant work must not be closed without either a linked ADR or an explicit `not-required` justification in the task evidence.

## CI enforcement

GitHub Actions validates the repository on every relevant pull request and push. The validation workflow checks:

- required `.aitask` files and directories
- YAML and JSON syntax
- `task.yaml` schema conformance
- task ID uniqueness
- required task folder contents
- linked ADR reference format and existence where declared
- lifecycle transition history where statically checkable
- higher-risk approval fields and evidence requirements

Static validation cannot prove that a human actually performed a review, that a shell command output is truthful, or that branch protection is enabled. Those controls are documented as manual hardening requirements.

## File-enforced vs manually enforced controls

File-enforced or CI-enforced controls:

- required metadata and task records
- schema validation
- lifecycle state and evidence checks that are statically checkable
- CODEOWNERS review targeting for governance files
- pull request disclosure requirements via templates

Manually enforced GitHub or organizational controls:

- protected branches and required status checks
- restrictions on direct push and force-push
- environment protections and deployment approvals
- team membership and role assignment
- retention policies beyond repository history

See `.aitask/automation/manual-github-hardening.md` and `.aitask/automation/repo-settings-baseline.md`.