# Git Workflow

Use short-lived branches and reviewable commits.

Suggested branch names:

```text
feature/<task>
fix/<task>
docs/<task>
chore/<task>
```

Commits should represent one understandable change. Avoid commits such as `updates`, `changes`, or `agent work`.

Before opening a pull request:

- run required validation
- review the diff
- remove accidental or generated files
- update project state if the implementation changed it
- record follow-up work separately
