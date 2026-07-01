# backlog

Backlog is a generic, file-first workflow skill for AI-assisted projects.

It is not a task app, server, or CLI product. It is a small skill/protocol plus templates that a host repository installs so agents can share the same long-lived project workflow state.

```text
Backlog skill + backlog files + host project rules = shared AI workflow memory
```

## Core idea

Backlog keeps workflow state inside the host repository:

```text
backlog/backlog.json        # task state source of truth
backlog/contexts/           # durable task context, optional
backlog/decisions/          # durable decisions, optional
```

Agents may edit the files directly as long as they follow `SKILL.md` and `SPEC.md`.

GitHub PRs can still be used by the host project for code review, CI, version history, and merges. PRs are references from Backlog, not the workflow source of truth.

## Repository layout

```text
README.md
SKILL.md                         # generic Backlog skill, the product core
SPEC.md                          # Backlog data/file format
adapters/claude-code/SKILL.md    # Claude Code adapter
AGENT_PROTOCOL.md                # detailed generic agent behavior
LICENSE
templates/simple/backlog/backlog.json
```

## Install into a host project

### Generic skill installation

Install these into the host project or the host agent's skill system:

```text
SKILL.md
templates/simple/backlog/backlog.json
```

The host project should end up with:

```text
backlog/backlog.json
```

### Claude Code installation

From the host project root:

```bash
mkdir -p .claude/skills/backlog
cp /path/to/backlog/adapters/claude-code/SKILL.md .claude/skills/backlog/SKILL.md
cp -r /path/to/backlog/templates/simple/backlog ./backlog
```

Add this to the host project's `CLAUDE.md`, `AGENTS.md`, Hermes profile, or equivalent agent rules:

```markdown
## Backlog

This project uses Backlog.
`backlog/backlog.json` is the project workflow source of truth.
Agents may edit Backlog files directly if they follow the Backlog skill and `SPEC.md`.
PRs are for code review/versioning only; Backlog remains the workflow source of truth.
```

## Minimal task

```json
{
  "id": "short-id",
  "title": "Human-readable title",
  "status": "pending",
  "priority": "medium",
  "type": "feature",
  "area": "api",
  "why": "Why this task exists",
  "what": "What should be done",
  "acceptance": [],
  "checklist": [],
  "depends_on": [],
  "related": [],
  "context_refs": [],
  "events": []
}
```

## Workflow states

```text
pending       planned, not started
in_progress   currently being worked on
blocked       needs a human decision or external unblock
review        implementation done; waiting for validation/PR/merge
completed     validated and done
cancelled     intentionally abandoned
```

## Recommended agent flow

```text
Backlog task → implementation worker → review/validation → optional PR merge → Backlog completed
```

1. Read host project rules first.
2. Read `backlog/backlog.json`.
3. Pick or create a task.
4. Mark it `in_progress` before implementation.
5. Mark it `blocked` when a human decision is required.
6. Mark it `review` when implementation is complete but not validated/merged.
7. Mark it `completed` only after the host project's validation criteria pass.

## License

MIT
