---
name: backlog
version: "7.0.0"
description: Claude Code adapter for the generic Backlog skill
user-invocable: true
---

# /backlog - Claude Code adapter

This is the Claude Code adapter for the generic Backlog skill.

Canonical skill definition in the Backlog product repo:

```text
SKILL.md
```

Canonical data/spec files:

```text
SPEC.md
templates/simple/backlog/backlog.json
```

When installed into a host project, this adapter usually lives at:

```text
.claude/skills/backlog/SKILL.md
```

## Behavior

Follow the generic Backlog skill behavior:

1. Read host project rules first.
2. Locate Backlog data, preferring `backlog/backlog.json`.
3. Use `/backlog` commands as user intent, not as a requirement for a program.
4. Edit Backlog JSON directly according to the skill/spec.
5. Preserve valid JSON and unknown fields.
6. Keep durable workflow state in Backlog; use Claude Code todo/task tools only for current-session implementation steps.

## Command intents

| Command | Meaning |
|---|---|
| `/backlog` | Show open tasks |
| `/backlog add "title"` | Add a task |
| `/backlog start <id>` | Mark task `in_progress` |
| `/backlog block <id>` | Mark task `blocked` with reason |
| `/backlog review <id>` | Mark task `review` after implementation, before validation/merge |
| `/backlog done <id>` | Mark task `completed` |
| `/backlog cancel <id>` | Mark task `cancelled` |

## Install

From a host project root:

```bash
mkdir -p .claude/skills/backlog
cp /path/to/backlog/adapters/claude-code/SKILL.md .claude/skills/backlog/SKILL.md
cp -r /path/to/backlog/templates/simple/backlog ./backlog
```
