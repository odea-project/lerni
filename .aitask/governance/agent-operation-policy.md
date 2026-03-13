# Agent Operation Policy

## Conservative operating posture

Agents may assist with drafting, implementation, validation, and evidence capture only within the bounds of an approved task and only for actions explicitly allowed by that task.

## Agents may autonomously

- draft or update repository text records within task scope
- run declared validation or test commands for approved work
- prepare pull request materials and evidence indexes
- propose ADR text when the task explicitly requires it

## Agents require human approval before

- changing risk tier, approvals, or waiver state
- altering governance policy, CODEOWNERS, branch protection guidance, or workflow enforcement
- changing security controls, secrets handling, production deployment paths, release configuration, or repository permissions
- performing actions outside `allowed_agent_actions`
- any `medium`, `high`, or `critical` task execution if explicit approval is not already recorded

## Agents must not do without explicit approval

- self-approve work
- conceal uncertainty or omit meaningful evidence
- widen task scope silently
- bypass required reviewers or required status checks
- perform destructive operations not covered by the approved rollback plan
- execute `critical` changes autonomously

## Uncertainty and deviations

When uncertainty exists, agents must:

- log the uncertainty in `execution-log.md`
- state assumptions explicitly
- stop when the uncertainty could affect risk, scope, approvals, or correctness

When controls conflict with productivity, controls win. The conflict should be logged and, if necessary, escalated through a waiver or governance update.