# Manual GitHub Hardening Steps

These controls are not fully enforceable by repository files alone. Repository maintainers must implement and periodically verify them in GitHub settings.

## Branch Protection

- protect the default branch
- require pull requests before merge
- require status checks to pass before merge
- require the `.github/workflows/aitask-validate.yml` check
- require code owner review
- dismiss stale approvals when new commits are pushed
- block force-push and branch deletion

## Pull Request Governance

- require linked task IDs in pull requests
- require at least one human review for low-risk tasks
- require at least two qualified human approvals for high or critical tasks where policy demands it

## Merge Strategy

- prefer squash merge or rebase merge to preserve traceability from task to final change
- disable merge methods that obscure review history if that conflicts with organizational standards

## Tags And Releases

- protect release tags if releases are security or compliance relevant
- restrict release creation rights to maintainers

## Environments And Deployments

- require deployment approvals for protected environments
- ensure production secrets and environment rules are outside agent write access unless explicitly approved

## Teams And Permissions

- map CODEOWNERS placeholders to actual GitHub teams
- restrict admin rights to a minimal set of maintainers
- review bot and app permissions periodically

## Caveat

This document describes recommended hardening. It does not claim the repository already enforces these settings.