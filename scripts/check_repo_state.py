#!/usr/bin/env python3
"""Small structural check for repositories using this framework."""

from pathlib import Path
import sys

REQUIRED = (
    "AGENTS.md",
    "docs/README.md",
    "docs/development/WORKFLOW.md",
    "docs/development/CONTEXT_POLICY.md",
    "docs/development/CHECKPOINTS.md",
    "docs/architecture/decisions/ADR_TEMPLATE.md",
    "development-state/CURRENT_STATE.yaml",
    "development-state/ACTIVE_WORK.yaml",
    "development-state/UNRESOLVED_UNKNOWNS.yaml",
    "development-state/HANDOFF_TEMPLATE.yaml",
    "development-state/blueprint/project-model.yaml",
    "tasks/TASK_TEMPLATE.yaml",
)

root = Path(__file__).resolve().parents[1]
missing = [path for path in REQUIRED if not (root / path).exists()]

if missing:
    print("Missing required framework files:")
    for path in missing:
        print(f"  - {path}")
    sys.exit(1)

print("Repository framework structure: OK")
