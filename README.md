# backlog

Backlog is a file-first workflow skill for AI-assisted projects.

It is not a task app, server, or CLI product. It is a small protocol plus templates that a host repository installs so agents can share the same long-lived project workflow state.

```text
Backlog skill + backlog files + host project rules = shared AI workflow memory
```

## Core idea

Backlog keeps workflow state inside the host repository:

```text
backlog/backlog.json        # task state source of truth
backlog/contexts/           # durable task context, optional
backlog/decisions/          # durable decisions, optional
.claude/skills/backlog/     # Claude Code adapter, optional
```

Agents may edit the files directly as long as they follow `SPEC.md` and `AGENT_PROTOCOL.md`.

GitHub PRs can still be used by the host project for code review, CI, version history, and merges. PRs are references from Backlog, not the workflow source of truth.

## Install into a host project

From the host project root:

```bash
# 1. Install the Claude Code adapter if the project uses Claude Code
mkdir -p .claude/skills
cp -r /path/to/backlog/.claude/skills/backlog .claude/skills/

# 2. Install the simple Backlog template
cp -r /path/to/backlog/templates/simple/backlog ./backlog

# 3. Optional: copy protocol docs for local reference
cp /path/to/backlog/SPEC.md ./backlog/SPEC.md
cp /path/to/backlog/AGENT_PROTOCOL.md ./backlog/AGENT_PROTOCOL.md
```

Add this to the host project's `CLAUDE.md`, `AGENTS.md`, Hermes profile, or equivalent agent rules:

```markdown
## Backlog

This project uses Backlog.
`backlog/backlog.json` is the project workflow source of truth.
Agents may edit Backlog files directly if they follow `backlog/SPEC.md` and the Backlog skill rules.
GitHub PRs are for code review/versioning only; Backlog remains the workflow source of truth.
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

## Repo layout

```text
README.md
SPEC.md
AGENT_PROTOCOL.md
templates/simple/backlog/backlog.json
.claude/skills/backlog/SKILL.md
```

## License

MIT
