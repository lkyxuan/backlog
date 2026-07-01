---
name: backlog
version: "5.0.0"
description: Cross-session repo-local Backlog workflow management
user-invocable: true
---

# /backlog - repo-local workflow management

Backlog stores long-lived project workflow state in `docs/backlog.json`. It is designed to be installed inside a host project, so any agent can recover task state across sessions.

External project-management platforms are not part of Backlog. Host projects may still use GitHub PRs for code review, version history, CI, and merging.

## Commands

| Command | Meaning |
|---|---|
| `/backlog` | Show open tasks |
| `/backlog add "title"` | Add a task to `docs/backlog.json` |
| `/backlog start <id>` | Mark task `in_progress` |
| `/backlog block <id>` | Mark task `blocked` with reason |
| `/backlog review <id>` | Mark task `review` after implementation, before validation/merge |
| `/backlog done <id>` | Mark task `completed` |
| `/backlog cancel <id>` | Mark task `cancelled` |

## Data model

```json
{
  "id": "short-id",
  "title": "Human-readable title",
  "status": "pending | in_progress | blocked | review | completed | cancelled",
  "priority": "high | medium | low",
  "type": "bug | feature | chore | research | docs | ops",
  "area": "spider | consumer | storage | monitoring | infra | api | frontend",
  "why": "Why this task exists",
  "what": "What should be done",
  "acceptance": ["Acceptance criterion 1", "Acceptance criterion 2"],
  "checklist": ["Step 1", "Step 2"],
  "depends_on": ["other-task-id"],
  "related": ["related-task-id"],
  "context_refs": ["context-id"],
  "events": []
}
```

Field notes:
- `id`: short English identifier, e.g. `merge-queues`.
- `title`: concise title that humans understand quickly.
- `depends_on`: hard dependency; do not start current task before these are done.
- `related`: relevant context only; not a blocking relationship.
- `context_refs`: references to durable project context docs, often under `docs/backlog/contexts/` in the host project.

## Agent behavior

1. Session start: read open backlog tasks.
2. Before work: locate the backlog task; create one if missing.
3. Starting work: set `status → in_progress`.
4. Implementation finished but not validated/merged: set `status → review`.
5. Human decision needed: set `status → blocked` with a clear reason.
6. Validation/merge done: set `status → completed`.
7. Work abandoned: set `status → cancelled`.
8. Code changes should still go through the host project's branch/PR workflow when applicable.

## Shared CLI

All agents can use the repo-local CLI instead of depending on a specific slash-command runtime:

```bash
python3 scripts/backlog_cli.py list --open
python3 scripts/backlog_cli.py show <id>
python3 scripts/backlog_cli.py start <id> --kanban-task <t_xxx>
python3 scripts/backlog_cli.py block <id> --reason "..." --kanban-task <t_xxx>
python3 scripts/backlog_cli.py review <id> --summary "..." --kanban-task <t_xxx>
python3 scripts/backlog_cli.py done <id> --summary "..." --kanban-task <t_xxx>
python3 scripts/backlog_cli.py cancel <id> --reason "..."
```

This skill is the natural-language wrapper for that CLI. If uncertain, use the CLI directly.

## Difference from Claude Code's built-in Task/Todo tool

| Feature | Backlog | Claude Code Task/Todo |
|---|---|---|
| Storage | Repo file | Session memory |
| Lifecycle | Cross-session, cross-agent | Current session only |
| Purpose | Long-lived project workflow state | Current implementation steps |
| Detail | why/what/acceptance/checklist/context | Short task descriptions |
