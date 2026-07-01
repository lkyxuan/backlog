# Backlog Spec

Backlog is a file-first workflow protocol for AI-assisted repositories.

## Source of truth

The host project owns its Backlog data:

```text
backlog/backlog.json
```

This file is the workflow source of truth. Agents may edit it directly, but must preserve valid JSON and the task schema below.

## Optional directories

```text
backlog/contexts/       durable background context
backlog/decisions/      durable decisions and tradeoffs
backlog/archive/        archived or split task files
```

## Top-level schema

```json
{
  "version": "1.0",
  "description": "Project workflow state",
  "tasks": []
}
```

## Task schema

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

Only these status values are valid:

```text
pending
in_progress
blocked
review
completed
cancelled
```

Meanings:

- `pending`: planned, not started.
- `in_progress`: currently being worked on.
- `blocked`: cannot proceed without a human decision or external dependency.
- `review`: implementation is complete, but validation/PR/merge is not done.
- `completed`: validated and done.
- `cancelled`: intentionally abandoned.

## Relationship fields

- `depends_on`: hard dependency. Do not start the task until dependencies are complete unless a human explicitly allows it.
- `related`: relevant task context, not a blocker.
- `context_refs`: references durable context files, usually under `backlog/contexts/`.
- `prs`: optional PR references for code review/version history.

## Events

Agents should append compact events when changing task status:

```json
{
  "time": "2026-01-28T10:30:00Z",
  "actor": "hermes | claude-code | codex | human",
  "event": "start | block | review | done | cancel | note",
  "text": "Short summary"
}
```

Keep events short. Put long context in `backlog/contexts/` or `backlog/decisions/` and reference it with `context_refs`.

## File-first rule

Backlog has no required runtime. A host project can use plain text editors, Claude Code, Hermes, Codex, or future agents. The durable contract is the files and this spec.
