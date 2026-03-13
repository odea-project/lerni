# Segregation Of Duties

## Core rules

- For `medium`, `high`, and `critical` tasks, the same identity must not both execute and approve.
- For `high` and `critical` tasks, reviewer and approver must be distinct wherever possible.
- Agents must never self-approve their own `high` or `critical` work.
- If separation is infeasible in a small team, the exception must be documented as a waiver with compensating controls.

## Prohibited combinations

- `executor` and `approver` for `medium` or above
- `agent executor` and `approver` for any task above `low`
- `reviewer` and `approver` for `critical` without a waiver

## Compensating controls when separation is constrained

- add a second human reviewer
- require maintainer sign-off at merge time
- increase evidence detail and audit sampling
- limit agent permissions and reduce autonomy