# Task Lifecycle

## Statuses

- `proposed`: Initial request captured. Scope may be incomplete. No execution permitted.
- `triaged`: Ownership, broad scope, and urgency assigned. No execution permitted.
- `specified`: Detailed specification written and mandatory artifacts created.
- `risk-assessed`: Risk assessment completed and controls identified.
- `approved`: Required approvals obtained. Execution may start only within approved scope.
- `in-progress`: Execution is active and being logged.
- `in-review`: Execution complete enough for formal review. No further scope expansion without re-approval.
- `accepted`: Review completed successfully and findings resolved or accepted.
- `rejected`: Task will not proceed or output is not accepted.
- `closed`: Administrative closure completed, evidence indexed, and final disposition recorded.
- `superseded`: Replaced by another task or ADR. The successor must be referenced.
- `archived`: Historical record moved to a dormant state after closure or supersession.

## Canonical transitions

Allowed forward transitions:

- `proposed -> triaged`
- `triaged -> specified`
- `specified -> risk-assessed`
- `risk-assessed -> approved`
- `approved -> in-progress`
- `in-progress -> in-review`
- `in-review -> accepted`
- `accepted -> closed`
- `proposed|triaged|specified|risk-assessed|approved|in-progress|in-review -> rejected`
- `closed|rejected -> archived`
- `approved|in-progress|in-review|accepted|closed -> superseded`

Allowed limited regressions:

- `risk-assessed -> specified` if scope changes invalidate the risk assessment
- `approved -> specified` if approvals lapse or the spec materially changes
- `in-review -> in-progress` if requested changes are accepted and execution resumes
- `accepted -> in-review` only if a post-acceptance defect is discovered before closure

Any other transition is invalid unless documented in an approved waiver.

## Minimum artifacts by state

- `proposed`: `task.yaml`
- `triaged`: `task.yaml` with owners and initial summary
- `specified`: `spec.md`, `task.yaml`, initial `evidence-index.md`
- `risk-assessed`: `risk.md`, `task.yaml` with `risk_tier`, `required_approvals`, `allowed_agent_actions`, `prohibited_agent_actions`
- `approved`: named approvals recorded in `task.yaml` or referenced approval artifacts
- `in-progress`: append-only `execution-log.md`
- `in-review`: `review.md`
- `accepted`: review decision recorded as accepted
- `closed`: `closure.md`, completed evidence index, final disposition in `task.yaml`
- `superseded`: successor task or ADR reference
- `archived`: no new execution allowed; record remains read-only in practice

## Execution gate rules

- No execution before `approved`, except clerical drafting of task records.
- `low` risk tasks may be approved by a single qualified human approver distinct from the requester where practical.
- `medium` risk tasks require explicit human approval before execution and distinct executor and approver identities.
- `high` risk tasks require segregated proposer, reviewer, and approver where feasible, plus a rollback plan.
- `critical` risk tasks require human-owned execution. Agents may only assist under documented, tightly constrained steps.

## Closure rules

A task may move to `closed` only when all of the following are true:

- the review decision is final
- evidence references are present for meaningful commands, tests, and approvals
- any required ADRs are linked
- exceptions or waivers are resolved, expired, or explicitly carried forward
- `final_disposition` is set in `task.yaml`
- closure notes capture residual risk and follow-up actions

## Audit expectations

- Corrections must be additive. Do not silently erase history from logs.
- If a record is wrong, append a corrective note with timestamp and actor.
- Auditors may sample any task at any state, but `closed`, `superseded`, and `critical` tasks should be prioritized.