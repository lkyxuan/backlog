# Backlog Agent Protocol

This protocol tells AI agents how to use Backlog inside a host repository.

## Priority order

When working in a host project:

1. Follow the host project's rules first (`CLAUDE.md`, `AGENTS.md`, Hermes profile, etc.).
2. Follow Backlog `SPEC.md` and this protocol for workflow state.
3. If there is a conflict, the host project rules win.

## Session start

1. Locate Backlog data:
   - preferred: `backlog/backlog.json`
   - legacy fallback: `docs/backlog.json`
2. Read open tasks: any task whose status is not `completed` or `cancelled`.
3. If the user names a task, load that task plus its `depends_on`, `related`, and `context_refs`.
4. If no task exists for the work, create one before making durable changes.

## Before implementation

Set the task to `in_progress` and append a short event:

```json
{
  "time": "2026-01-28T10:00:00Z",
  "actor": "agent-name",
  "event": "start",
  "text": "Started implementation"
}
```

## During implementation

- Use current-session todo tools for small implementation steps.
- Use Backlog only for durable workflow state.
- Keep long logs out of `backlog/backlog.json`.
- Store reusable context in `backlog/contexts/` and reference it with `context_refs`.

## Blocking

If a human decision is required, set:

```json
"status": "blocked",
"blocked_reason": "short reason"
```

Append a `block` event. Do not keep coding around a real product decision.

## Review

When implementation is complete but validation, PR review, or merge is not complete, set:

```json
"status": "review"
```

If there is a PR, add it as a reference:

```json
"prs": [20]
```

## Completion

Set `completed` only when the host project's definition of done is satisfied. Usually that means tests/lint pass and the relevant PR is merged or the change is otherwise accepted.

## Context loading

Agents should not blindly load every task. For a named task, load only:

- the task itself
- tasks in `depends_on`
- tasks in `related`
- files referenced by `context_refs`
- host project rules and relevant module docs

This is the main reason Backlog exists: route AI context instead of dumping the whole project history.

## Editing rules

- Preserve valid JSON.
- Preserve unknown fields.
- Keep events concise.
- Prefer appending events over rewriting history.
- Do not delete completed tasks unless archiving is explicitly requested.
