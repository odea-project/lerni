# Retention And Audit

## Retention principles

- task, review, audit, and waiver records remain in version control as the primary system of record
- logs should be append-oriented
- corrections should be additive and attributable
- external evidence references must note retention location and owner

## Auditability requirements

- each closed task must be reconstructable from repository records
- reviewers and auditors must be able to identify who did what, when, and under which approval
- changes to governance files require review through CODEOWNERS and pull request records

## Audit cadence guidance

- audit `critical` tasks before acceptance
- sample `high` tasks before or shortly after closure
- review waiver expiry at least weekly
- review governance policy and control matrices at least quarterly