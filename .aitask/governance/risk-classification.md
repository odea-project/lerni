# Risk Classification

## Risk tiers

### Low

Limited change scope, easy rollback, no sensitive data handling, no production or externally visible effect, and minimal autonomous discretion.

### Medium

Moderate change scope, internal user impact possible, configuration or code changes with manageable rollback, and bounded autonomous action.

### High

Material impact to code, security posture, privacy, infrastructure, customer-facing behavior, or compliance obligations. Rollback may be non-trivial or time-sensitive.

### Critical

Potential for severe service disruption, irreversible data impact, material compliance exposure, security boundary changes, or high-consequence autonomous action. Human-owned execution is mandatory.

## Risk factors

Assess all tasks against these factors:

- code impact
- security impact
- privacy or data sensitivity
- external user impact
- infrastructure impact
- regulatory or compliance relevance
- ability to roll back
- degree of autonomy granted to the agent

## Classification guidance

- Classify to the highest relevant tier.
- If evidence is incomplete, classify at least `medium` until clarified.
- If an agent is allowed to change security controls, secrets handling, production deployment, or repository protections, classify at least `high`.
- If rollback is impossible or unclear, classify at least `high`.
- If personal data, regulated data, or legal obligations are implicated, do not classify below `high` without documented rationale.