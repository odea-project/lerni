# Conventions

## Naming

- Task IDs: `TASK-YYYY-NNNN`, for example `TASK-2026-0001`
- Example task IDs: `TASK-EXAMPLE-NNNN`
- ADR IDs: `ADR-YYYY-NNNN`
- Audit IDs: `AUDIT-YYYY-NNNN`
- Waiver IDs: `WAIVER-YYYY-NNNN`

## Metadata field style

All machine-readable keys use `snake_case`.

## Timestamp format

- Use ISO 8601 in UTC.
- Preferred format: `YYYY-MM-DDTHH:MM:SSZ`
- Example: `2026-03-13T14:30:00Z`

## Identity notation

- Humans: `human:<account>`
- Agents: `agent:<name>`
- Service identities: `svc:<system>`

Examples:

- `human:jane.doe`
- `agent:repo-bootstrapper`
- `svc:github-actions`

## File rules

- `task.yaml` is the canonical metadata source for each task.
- Markdown files are human-readable working records.
- Logs are append-oriented and should not be rewritten to hide prior content.
- If a task is superseded, preserve the original folder and link the successor.

## Append-only log entry format

Each execution, review, or audit log entry should include, in order where practical:

1. timestamp
2. actor
3. action or step performed
4. reason or trigger
5. files changed or records inspected
6. commands or checks performed
7. outputs or evidence references
8. deviations or exceptions
9. follow-up actions

## ADR linkage

- Use `linked_adr` in `task.yaml` for primary ADR linkage.
- If multiple ADRs apply, store an array.
- ADR references must either be `not-required` or point to an existing file under `.aitask/adrs/`.

## Evidence references

- Prefer repository-relative paths.
- Use stable identifiers for external systems.
- If evidence is stored outside the repository, include a durable reference, owner, and retention note.

## Status history

Store status history in `task.yaml.status_history` as an ordered list. Each entry should include:

- `from_status`
- `to_status`
- `changed_at`
- `changed_by`
- `reason`

This supports lifecycle validation without hidden state.