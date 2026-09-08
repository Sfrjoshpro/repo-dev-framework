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

BLUEPRINT_MARKERS = (
    "schema_version:",
    "node_types:",
    "edge_types:",
    "flow_types:",
    "status_values:",
    "nodes:",
    "edges:",
    "flows:",
)

root = Path(__file__).resolve().parents[1]
missing = [path for path in REQUIRED if not (root / path).exists()]

if missing:
    print("Missing required framework files:")
    for path in missing:
        print(f"  - {path}")
    sys.exit(1)

blueprint_path = root / "development-state/blueprint/project-model.yaml"
blueprint = blueprint_path.read_text(encoding="utf-8")
missing_markers = [marker for marker in BLUEPRINT_MARKERS if marker not in blueprint]

if missing_markers:
    print("Blueprint is missing required sections:")
    for marker in missing_markers:
        print(f"  - {marker.rstrip(':')}")
    sys.exit(1)

print("Repository framework structure: OK")
print("Blueprint structure: OK")
