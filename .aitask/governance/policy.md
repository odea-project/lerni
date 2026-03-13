# AI Task Governance Policy

## Policy statements

1. No governed work may be executed without a task record.
2. No task may enter execution before risk assessment and required approvals are complete.
3. Higher-risk tasks must satisfy segregation-of-duties requirements.
4. Agents must operate only within explicitly allowed actions and must log their work.
5. Exceptions must be documented as waivers, with justification, expiry, approval, and compensating controls.
6. Reviews and audits are records, not informal conversations.
7. Architectural or governance-relevant decisions must be captured as ADRs when applicable.
8. Repository settings required for enforcement must be configured manually if not enforceable by files alone.

## Policy precedence

In case of conflict, precedence is:

1. legal or regulatory obligations
2. repository protection settings and organization policy
3. `.aitask/governance/policy.md`
4. task-specific controls and approvals
5. operational convenience

If a conflict remains unresolved, execution must stop and the issue must be logged in the task records.