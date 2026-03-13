from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


class AITaskLoader(yaml.SafeLoader):
    pass


for first_letter, mappings in list(AITaskLoader.yaml_implicit_resolvers.items()):
    AITaskLoader.yaml_implicit_resolvers[first_letter] = [
        mapping for mapping in mappings if mapping[0] != "tag:yaml.org,2002:timestamp"
    ]


ROOT_REQUIRED_FILES = [
    ".aitask/README.md",
    ".aitask/glossary.md",
    ".aitask/lifecycle.md",
    ".aitask/conventions.md",
    ".aitask/governance/charter.md",
    ".aitask/governance/policy.md",
    ".aitask/governance/roles-and-responsibilities.md",
    ".aitask/governance/approval-matrix.yaml",
    ".aitask/governance/risk-classification.md",
    ".aitask/governance/control-matrix.yaml",
    ".aitask/governance/segregation-of-duties.md",
    ".aitask/governance/exceptions-and-waivers.md",
    ".aitask/governance/retention-and-audit.md",
    ".aitask/governance/agent-operation-policy.md",
    ".aitask/governance/human-oversight-policy.md",
    ".aitask/governance/change-control-policy.md",
    ".aitask/schemas/task.schema.json",
    ".aitask/schemas/review.schema.json",
    ".aitask/schemas/execution-log.schema.json",
    ".aitask/schemas/audit-log.schema.json",
    ".aitask/schemas/adr-link.schema.json",
    ".aitask/schemas/waiver.schema.json",
    ".aitask/templates/task.md",
    ".aitask/templates/task.metadata.yaml",
    ".aitask/templates/review.md",
    ".aitask/templates/execution-log.md",
    ".aitask/templates/audit-log.md",
    ".aitask/templates/waiver.md",
    ".aitask/templates/evidence-index.md",
    ".aitask/templates/adr.md",
    ".aitask/templates/risk-assessment.md",
    ".aitask/templates/closure-report.md",
    ".aitask/templates/pull-request-checklist.md",
    ".aitask/tasks/README.md",
    ".aitask/tasks/_index.yaml",
    ".aitask/adrs/README.md",
    ".aitask/audits/README.md",
    ".aitask/audits/findings-register.yaml",
    ".aitask/reports/README.md",
    ".aitask/automation/README.md",
    ".aitask/automation/manual-github-hardening.md",
    ".aitask/automation/repo-settings-baseline.md",
    ".github/CODEOWNERS",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/ai-task.yml",
    ".github/ISSUE_TEMPLATE/governance-change.yml",
    ".github/workflows/aitask-validate.yml",
    ".github/workflows/aitask-audit-reminder.yml",
    "docs/ai-governance.md",
]

TASK_REQUIRED_FILES = [
    "task.yaml",
    "spec.md",
    "risk.md",
    "execution-log.md",
    "review.md",
    "audit.md",
    "evidence-index.md",
    "closure.md",
]

VALID_TRANSITIONS = {
    (None, "proposed"),
    ("proposed", "triaged"),
    ("triaged", "specified"),
    ("specified", "risk-assessed"),
    ("risk-assessed", "approved"),
    ("approved", "in-progress"),
    ("in-progress", "in-review"),
    ("in-review", "accepted"),
    ("accepted", "closed"),
    ("proposed", "rejected"),
    ("triaged", "rejected"),
    ("specified", "rejected"),
    ("risk-assessed", "rejected"),
    ("approved", "rejected"),
    ("in-progress", "rejected"),
    ("in-review", "rejected"),
    ("closed", "archived"),
    ("rejected", "archived"),
    ("approved", "superseded"),
    ("in-progress", "superseded"),
    ("in-review", "superseded"),
    ("accepted", "superseded"),
    ("closed", "superseded"),
    ("risk-assessed", "specified"),
    ("approved", "specified"),
    ("in-review", "in-progress"),
    ("accepted", "in-review"),
}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=AITaskLoader)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def assert_required_paths(root: Path, errors: list[str]) -> None:
    for relative in ROOT_REQUIRED_FILES:
        if not (root / relative).exists():
            errors.append(f"Missing required repository file: {relative}")


def find_task_directories(root: Path) -> list[Path]:
    task_root = root / ".aitask" / "tasks"
    task_dirs: list[Path] = []
    for child in task_root.iterdir():
        if child.is_dir() and child.name.startswith("TASK-"):
            task_dirs.append(child)
    examples_root = task_root / "examples"
    if examples_root.exists():
        for child in examples_root.iterdir():
            if child.is_dir() and child.name.startswith("TASK-"):
                task_dirs.append(child)
    return sorted(task_dirs)


def validate_yaml_and_json_syntax(root: Path, errors: list[str]) -> None:
    for path in root.rglob("*.yaml"):
        try:
            load_yaml(path)
        except Exception as exc:
            errors.append(f"Invalid YAML syntax in {path.relative_to(root).as_posix()}: {exc}")
    for path in root.rglob("*.yml"):
        try:
            load_yaml(path)
        except Exception as exc:
            errors.append(f"Invalid YAML syntax in {path.relative_to(root).as_posix()}: {exc}")
    for path in root.rglob("*.json"):
        try:
            load_json(path)
        except Exception as exc:
            errors.append(f"Invalid JSON syntax in {path.relative_to(root).as_posix()}: {exc}")


def validate_task_index(root: Path, task_dirs: list[Path], errors: list[str]) -> None:
    index_path = root / ".aitask" / "tasks" / "_index.yaml"
    index_data = load_yaml(index_path)
    indexed_ids = {entry["id"] for entry in index_data.get("tasks", [])}
    actual_ids = {path.name for path in task_dirs}
    missing = actual_ids - indexed_ids
    if missing:
        errors.append(f"Task index missing task ids: {', '.join(sorted(missing))}")


def validate_tasks(root: Path, task_dirs: list[Path], errors: list[str]) -> None:
    schema = load_json(root / ".aitask" / "schemas" / "task.schema.json")
    validator = Draft202012Validator(schema)
    seen_ids: set[str] = set()

    for task_dir in task_dirs:
        for required in TASK_REQUIRED_FILES:
            if not (task_dir / required).exists():
                errors.append(f"Task {task_dir.name} missing required file {required}")

        task_path = task_dir / "task.yaml"
        if not task_path.exists():
            continue

        task_data = load_yaml(task_path)
        validation_errors = sorted(validator.iter_errors(task_data), key=lambda item: list(item.path))
        for validation_error in validation_errors:
            field = ".".join(str(part) for part in validation_error.path) or "<root>"
            errors.append(
                f"Schema validation failed for {task_path.relative_to(root).as_posix()} at {field}: {validation_error.message}"
            )

        task_id = task_data.get("id")
        if task_id in seen_ids:
            errors.append(f"Duplicate task id found: {task_id}")
        if task_id:
            seen_ids.add(task_id)
        if task_id and task_id != task_dir.name:
            errors.append(
                f"Task folder name mismatch: folder {task_dir.name} does not match id {task_id}"
            )

        status_history = task_data.get("status_history", [])
        for entry in status_history:
            transition = (entry.get("from_status"), entry.get("to_status"))
            if transition not in VALID_TRANSITIONS:
                errors.append(
                    f"Invalid lifecycle transition in {task_path.relative_to(root).as_posix()}: {transition[0]} -> {transition[1]}"
                )

        if status_history:
            final_status = status_history[-1].get("to_status")
            if task_data.get("status") != final_status:
                errors.append(
                    f"Task status mismatch in {task_path.relative_to(root).as_posix()}: status is {task_data.get('status')} but history ends at {final_status}"
                )

        linked_adr = task_data.get("linked_adr")
        if isinstance(linked_adr, list):
            for adr_path in linked_adr:
                if not (root / adr_path).exists():
                    errors.append(f"Linked ADR does not exist for {task_id}: {adr_path}")

        risk_tier = task_data.get("risk_tier")
        required_approvals = task_data.get("required_approvals", [])
        if risk_tier in {"medium", "high", "critical"}:
            if not required_approvals:
                errors.append(f"Task {task_id} requires explicit approvals for risk tier {risk_tier}")
            approver_states = [entry.get("state") for entry in required_approvals if entry.get("role") == "approver"]
            if not approver_states:
                errors.append(f"Task {task_id} requires an approver entry for risk tier {risk_tier}")
        if task_data.get("evidence_required") and not (task_dir / "evidence-index.md").exists():
            errors.append(f"Task {task_id} requires evidence-index.md")
        if risk_tier in {"high", "critical"} and linked_adr == "not-required":
            errors.append(f"Task {task_id} is {risk_tier} and must link an ADR or use a waiver")


def validate_governance_placeholders(root: Path, errors: list[str]) -> None:
    codeowners = (root / ".github" / "CODEOWNERS").read_text(encoding="utf-8")
    if "@ORG/" not in codeowners:
        return
    # Placeholder owners are allowed at bootstrap time, but the repository should flag them clearly.
    hardening_doc = (root / ".aitask" / "automation" / "manual-github-hardening.md").read_text(encoding="utf-8")
    if "map CODEOWNERS placeholders" not in hardening_doc:
        errors.append("CODEOWNERS contains placeholders without corresponding manual hardening guidance")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate .aitask repository records.")
    parser.add_argument("--root", default=".", help="Repository root path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []

    assert_required_paths(root, errors)
    validate_yaml_and_json_syntax(root, errors)
    task_dirs = find_task_directories(root)
    validate_task_index(root, task_dirs, errors)
    validate_tasks(root, task_dirs, errors)
    validate_governance_placeholders(root, errors)

    if errors:
        print("AITASK VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("AITASK VALIDATION PASSED")
    print(f"Validated {len(task_dirs)} task directories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())