# AI Governance Overview

This repository uses `.aitask` as the operating model for AI-assisted work.

## What it does

- requires a task record before significant AI-assisted execution
- classifies risk before execution
- applies stronger approvals and segregation of duties as risk increases
- captures execution, review, audit, and waiver records as repository artifacts
- validates key records in CI

## Where to start

- read `.aitask/README.md`
- use `.aitask/templates/` to open a new task
- review `.aitask/governance/` for policy and approval rules

## Key control boundary

Repository files and CI can enforce structure and static validation. GitHub branch protection, required reviews, and permissions still need manual configuration by maintainers.