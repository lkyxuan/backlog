---
name: backlog
version: "6.0.0"
description: File-first Backlog workflow skill for repo-local AI project management
user-invocable: true
---

# /backlog - file-first workflow skill

Backlog is a skill/protocol, not a required program. It stores long-lived project workflow state in the host repository so multiple agents can share the same task memory.

Preferred data file:

```text
backlog/backlog.json
```

Legacy fallback:

```text
docs/backlog.json
```

## Commands as user intent

These slash commands describe intent. You may satisfy them by directly editing Backlog files according to `SPEC.md` and `AGENT_PROTOCOL.md`.

| Command | Meaning |
|---|---|
| `/backlog` | Show open tasks |
| `/backlog add "title"` | Add a task |
| `/backlog start <id>` | Mark task `in_progress` |
| `/backlog block <id>` | Mark task `blocked` with reason |
| `/backlog review <id>` | Mark task `review` after implementation, before validation/merge |
| `/backlog done <id>` | Mark task `completed` |
| `/backlog cancel <id>` | Mark task `cancelled` |

## Task model

```json
{
  "id": "short-id",
  "title": "Human-readable title",
  "status": "pending | in_progress | blocked | review | completed | cancelled",
  "priority": "high | medium | low",
  "type": "bug | feature | chore | research | docs | ops",
  "area": "project-specific area",
  "why": "Why this task exists",
  "what": "What should be done",
  "acceptance": ["Acceptance criterion"],
  "checklist": ["Implementation step"],
  "depends_on": ["other-task-id"],
  "related": ["related-task-id"],
  "context_refs": ["context-id"],
  "prs": [],
  "events": []
}
```

## Agent behavior

1. Read host project rules first.
2. Locate Backlog data, preferring `backlog/backlog.json`.
3. Show or select open tasks when asked.
4. Before implementation, set the task to `in_progress` and append a short `start` event.
5. If human input is needed, set `blocked` and write `blocked_reason`.
6. When implementation is ready for validation/PR/merge, set `review`.
7. Set `completed` only after the host project's validation criteria pass.
8. Keep GitHub PR numbers, if any, as optional references in `prs`.

## Context loading

For a named task, do not load the entire Backlog by default. Load:

- the task itself
- tasks in `depends_on`
- tasks in `related`
- files referenced by `context_refs`
- host project rules and relevant module docs

## Editing rules

- Preserve valid JSON.
- Preserve unknown fields.
- Keep events short.
- Put long-lived context in `backlog/contexts/`.
- Prefer appending events over rewriting history.
