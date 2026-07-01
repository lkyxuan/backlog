# backlog

Repo-local cross-session task tracking for Claude Code, Hermes, and other coding agents.

Backlog is a tiny workflow layer installed inside a host project. It keeps long-lived task state in `docs/backlog.json`, exposes a shared CLI at `scripts/backlog_cli.py`, and provides a Claude Code skill as a natural-language wrapper.

Backlog does **not** manage external project-management platforms. Host projects may still use GitHub PRs for code review, CI, version history, and merging.

## Features

- **Repo-local source of truth**: task state lives in `docs/backlog.json`
- **Cross-session**: agents can recover context after restarts
- **Cross-agent**: Hermes, Claude Code, and other workers use the same CLI
- **Workflow states**: `pending`, `in_progress`, `blocked`, `review`, `completed`, `cancelled`
- **Structured context**: `why`, `what`, `acceptance`, `checklist`, `depends_on`, `related`, `context_refs`
- **No platform lock-in**: no external project-management dependency

## Install into a host project

From the host project root:

```bash
# 1. Install the Claude Code skill
mkdir -p .claude/skills
cp -r /path/to/backlog/.claude/skills/backlog .claude/skills/

# 2. Install the shared CLI
mkdir -p scripts
cp /path/to/backlog/scripts/backlog_cli.py scripts/backlog_cli.py

# 3. Create initial task data if the project does not have one yet
mkdir -p docs
cp /path/to/backlog/examples/backlog.json docs/backlog.json

# 4. Optional: copy workflow docs
cp /path/to/backlog/docs/agent-workflow.md docs/agent-workflow.md
```

Add this to the host project's `CLAUDE.md` or equivalent agent rules:

```markdown
## Backlog

`docs/backlog.json` is the project workflow source of truth.
Use `python3 scripts/backlog_cli.py` or `/backlog` to update task state.
GitHub PRs may be used for code review/versioning, but Backlog remains the workflow source of truth.
```

## CLI usage

```bash
python3 scripts/backlog_cli.py list --open
python3 scripts/backlog_cli.py show <id>
python3 scripts/backlog_cli.py start <id> --kanban-task <t_xxx>
python3 scripts/backlog_cli.py block <id> --reason "needs human decision" --kanban-task <t_xxx>
python3 scripts/backlog_cli.py review <id> --summary "implementation ready for validation" --kanban-task <t_xxx>
python3 scripts/backlog_cli.py done <id> --summary "validated and merged" --kanban-task <t_xxx>
python3 scripts/backlog_cli.py cancel <id> --reason "obsolete"
```

## Task structure

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

## Recommended agent flow

```text
Backlog task → implementation worker → review/validation → optional PR merge → backlog done
```

1. Locate the task with `list --open` or `show <id>`.
2. Mark it `in_progress` before implementation.
3. Mark it `blocked` if a human decision is needed.
4. Mark it `review` after implementation, before validation/merge.
5. Mark it `completed` only after the host project's validation criteria pass.

## Difference from Claude Code's built-in Task/Todo tool

| Feature | Backlog | Claude Code Task/Todo |
|---|---|---|
| Storage | Repo file | Session memory |
| Lifecycle | Cross-session, cross-agent | Current session only |
| Purpose | Long-lived project workflow state | Current implementation steps |
| Detail | why/what/acceptance/checklist/context | Short task descriptions |

## License

MIT
