from __future__ import annotations

import argparse
import os
from datetime import date, datetime
from pathlib import Path

import yaml


ACTIVE_STATUSES = {"approved", "in-progress", "in-review", "accepted"}


class AITaskLoader(yaml.SafeLoader):
    pass


for first_letter, mappings in list(AITaskLoader.yaml_implicit_resolvers.items()):
    AITaskLoader.yaml_implicit_resolvers[first_letter] = [
        mapping for mapping in mappings if mapping[0] != "tag:yaml.org,2002:timestamp"
    ]


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=AITaskLoader)


def iter_task_files(root: Path):
    task_root = root / ".aitask" / "tasks"
    for directory in task_root.rglob("task.yaml"):
        yield directory


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate audit reminder summary for .aitask records.")
    parser.add_argument("--root", default=".", help="Repository root path")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    today = date.today()
    active_tasks: list[str] = []
    overdue_waivers: list[str] = []

    for task_file in iter_task_files(root):
        task = load_yaml(task_file)
        task_id = task.get("id", task_file.parent.name)
        if task.get("status") in ACTIVE_STATUSES:
            active_tasks.append(f"- {task_id}: status={task.get('status')} risk={task.get('risk_tier')}")
        for exception_ref in task.get("exceptions", []):
            waiver_path = root / exception_ref
            if waiver_path.exists() and waiver_path.suffix in {".yaml", ".yml"}:
                waiver = load_yaml(waiver_path)
                expiry = waiver.get("expiry")
                if expiry:
                    expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
                    if expiry_date < today:
                        overdue_waivers.append(f"- {task_id}: {exception_ref} expired {expiry}")

    summary_lines = ["# AI Task Audit Reminder", "", "## Active Tasks"]
    summary_lines.extend(active_tasks or ["- none"])
    summary_lines.extend(["", "## Expired Waivers"])
    summary_lines.extend(overdue_waivers or ["- none"])
    summary = "\n".join(summary_lines)

    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        step_summary_path = Path(step_summary)
        step_summary_path.write_text(summary + "\n", encoding="utf-8")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())