# Agent workflow with Backlog

Backlog is a file-first workflow skill for AI-assisted projects.

```text
backlog/backlog.json      = workflow state source of truth
backlog/contexts/         = durable context, optional
backlog/decisions/        = durable decisions, optional
.claude/skills/backlog    = Claude Code adapter, optional
GitHub PRs                = optional code review/versioning references
```

## Recommended flow

1. Pick or create a Backlog task.
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
- Backlog file: backlog/backlog.json
- Backlog task id: <id>
- Execution queue task: <optional kanban/task id>

Task:
<what to implement>

Acceptance criteria:
- <criterion 1>
- <criterion 2>

Rules:
- Backlog is file-first; edit Backlog JSON directly according to SPEC.md.
- Use current-session todo tools for implementation steps only.
- Mark the Backlog task review/completed according to host project validation rules.
- Do not commit unless explicitly asked or the host project workflow requires it.
- Report changed files and verification run.
```
