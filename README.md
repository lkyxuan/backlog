# backlog

Backlog is a generic, file-first workflow skill for AI-assisted projects.

It is not a task app, server, or CLI product. It is a small skill plus a template that a host repository installs so agents can share the same long-lived project workflow state.

```text
Backlog skill + backlog file + host project rules = shared AI workflow memory
```

## Core files

```text
SKILL.md                                   # skill logic and task schema
templates/simple/backlog/backlog.json      # starter backlog data
README.md                                  # human-facing overview
LICENSE
```

## Install into a host project

Install Backlog with your agent or skill-system installer. The installer should use:

```text
SKILL.md
templates/simple/backlog/backlog.json
```

The host project should end up with its own workflow data file:

```text
backlog/backlog.json
```

Backlog does not encode agent-specific install paths. Claude Code, Hermes, or other systems should place `SKILL.md` wherever their own skill mechanism expects it.

Add this to the host project's `CLAUDE.md`, `AGENTS.md`, Hermes profile, or equivalent agent rules:

```markdown
## Backlog

This project uses Backlog.
`backlog/backlog.json` is the project workflow source of truth.
Agents may edit Backlog files directly if they follow the Backlog skill.
PRs are for code review/versioning only; Backlog remains the workflow source of truth.
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

## License

MIT
