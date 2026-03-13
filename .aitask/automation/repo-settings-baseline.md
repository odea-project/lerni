# Repository Settings Baseline

Use this as the target baseline for manual configuration and periodic attestation.

## Recommended Baseline

| Setting Area | Baseline | Reason |
| --- | --- | --- |
| Default branch | Protected | Prevent direct unreviewed changes |
| Pull requests | Required for default branch | Preserve review trail |
| Required checks | `aitask-validate` and any build/test checks | Block invalid governed changes |
| Code owner review | Required | Enforce governance oversight |
| Force push | Disabled on protected branches | Preserve auditability |
| Deletion of protected branches | Disabled | Preserve continuity |
| Merge queue | Recommended when repository volume justifies it | Keep required checks stable |
| Merge strategy | Squash or rebase preferred | Improve traceability |
| Tag protection | Enabled for release tags | Protect release integrity |
| Actions permissions | Least privilege | Reduce automation risk |
| Secret management | Organization-managed with restricted write access | Reduce credential exposure |

## Review Guidance

- review this baseline quarterly
- record deviations through a governed task or waiver