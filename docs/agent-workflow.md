# Agent workflow with Backlog

Backlog is a small repo-local workflow layer for AI-assisted projects.

```text
docs/backlog.json        = source of truth for workflow state
scripts/backlog_cli.py   = shared command surface for all agents
.claude/skills/backlog   = Claude Code natural-language wrapper
GitHub PRs              = optional code review/versioning layer in the host project
```

Backlog does not manage external project-management platforms.

## Recommended flow

1. Pick or create a backlog task.
2. Mark it `in_progress` before implementation starts.
3. Use the host project's coding agent / worker to implement.
4. Mark it `blocked` if a human decision is needed.
5. Mark it `review` when implementation is complete but not validated or merged.
6. Mark it `completed` only after validation/merge criteria pass.

## Generic worker prompt template

```text
You are working in <host-project-path>.
Read the host project's agent rules first.

Source of truth:
- backlog-id: <id>
- execution queue task: <optional kanban/task id>

Task:
<what to implement>

Acceptance criteria:
- <criterion 1>
- <criterion 2>

Rules:
- docs/backlog.json is the workflow source of truth.
- Use python3 scripts/backlog_cli.py start/block/review/done to reflect task state.
- Do not commit unless explicitly asked or the host project workflow requires it.
- Report changed files and verification run.
```
