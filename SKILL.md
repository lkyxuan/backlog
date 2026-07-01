---
name: backlog
version: "8.1.0"
description: Generic file-first Backlog skill for repo-local AI project management
user-invocable: true
---

# Backlog skill

Backlog is a generic skill/protocol for long-lived project workflow state in a host repository. Multiple agents can share the same task memory through the same Backlog files.

## Data location

Preferred:

```text
backlog/backlog.json
```

Legacy fallback:

```text
docs/backlog.json
```

Optional context directories:

```text
backlog/contexts/       durable background context
backlog/decisions/      durable decisions and tradeoffs
backlog/archive/        archived or split task files
```

## Top-level file shape

```json
{
  "version": "1.0",
  "description": "Project workflow state",
  "tasks": []
}
```

## Task model

Required fields:

```json
{
  "id": "short-id",
  "title": "Human-readable title",
  "status": "pending",
  "priority": "medium"
}
```

Recommended fields:

```json
{
  "type": "bug | feature | chore | research | docs | ops",
  "area": "project-specific area",
  "created": "2026-01-28T10:00:00Z",
  "why": "Why this task exists",
  "what": "What should be done",
  "acceptance": ["Acceptance criterion"],
  "checklist": ["Implementation step"],
  "depends_on": ["task-id"],
  "related": ["task-id"],
  "context_refs": ["context-id"],
  "prs": [1],
  "events": []
}
```

## Status values

```text
pending
in_progress
blocked
review
completed
cancelled
```

Meanings:

- `pending`: planned.
- `in_progress`: currently being worked on.
- `blocked`: waiting for a human decision or external dependency.
- `review`: implementation is complete; validation/PR/merge remains.
- `completed`: validated and done.
- `cancelled`: intentionally abandoned.

## Relationships

- `depends_on`: hard dependency. Start the task after dependencies are complete, unless a human explicitly allows it.
- `related`: relevant task context.
- `context_refs`: references durable context files, usually under `backlog/contexts/`.
- `prs`: optional PR references for code review/version history.

## User intents

These commands describe intent. An agent may satisfy them by directly editing Backlog files.

| Intent | Meaning |
|---|---|
| `show backlog` / `/backlog` | Show open tasks |
| `add backlog task` / `/backlog add "title"` | Add a task |
| `start <id>` / `/backlog start <id>` | Mark task `in_progress` |
| `block <id>` / `/backlog block <id>` | Mark task `blocked` with reason |
| `review <id>` / `/backlog review <id>` | Mark task `review` after implementation, before validation/merge |
| `done <id>` / `/backlog done <id>` | Mark task `completed` |
| `cancel <id>` / `/backlog cancel <id>` | Mark task `cancelled` |

## Agent behavior

1. Follow the host project's rules first.
2. Locate Backlog data, preferring `backlog/backlog.json`.
3. Read open tasks: tasks with active statuses such as `pending`, `in_progress`, `blocked`, or `review`.
4. If the user names a task, load that task plus its `depends_on`, `related`, and `context_refs`.
5. If the work has no task yet, create one before making durable changes.
6. Before implementation, set the task to `in_progress` and append a short `start` event.
7. Use current-session todo/task tools for small implementation steps only.
8. If human input is needed, set `blocked`, write `blocked_reason`, and append a `block` event.
9. When implementation is ready for validation/PR/merge, set `review`.
10. Set `completed` after the host project's validation criteria pass.

## Event format

Agents should append compact events when changing task status:

```json
{
  "time": "2026-01-28T10:30:00Z",
  "actor": "agent-name",
  "event": "start | block | review | done | cancel | note",
  "text": "Short summary"
}
```

Keep events short. Put long-lived context in `backlog/contexts/` or `backlog/decisions/` and reference it with `context_refs`.

## Context loading

For a named task, load focused context:

- the task itself
- tasks in `depends_on`
- tasks in `related`
- files referenced by `context_refs`
- host project rules and relevant module docs

Backlog routes AI context instead of dumping the whole project history.

## Editing rules

- Preserve valid JSON.
- Preserve unknown fields.
- Keep events concise.
- Prefer appending events over rewriting history.
- Archive completed tasks when cleanup is explicitly requested.
