#!/usr/bin/env python3
"""Repo-local Backlog CLI.

Shared automation surface for Hermes, Claude Code, and future operators.
The source of truth is docs/backlog.json in the host project.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKLOG_PATH = REPO_ROOT / "docs" / "backlog.json"
VALID_STATUSES = {"pending", "in_progress", "blocked", "review", "completed", "cancelled"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_backlog() -> dict[str, Any]:
    with BACKLOG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_backlog(data: dict[str, Any]) -> None:
    tmp = BACKLOG_PATH.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(BACKLOG_PATH)


def find_task(data: dict[str, Any], task_id: str) -> dict[str, Any]:
    for task in data.get("tasks", []):
        if task.get("id") == task_id:
            return task
    raise SystemExit(f"Task not found: {task_id}")


def append_event(task: dict[str, Any], event: str, text: str | None, kanban_task: str | None) -> None:
    events = task.setdefault("events", [])
    item: dict[str, Any] = {"time": now_iso(), "event": event}
    if text:
        item["text"] = text
    if kanban_task:
        item["kanban_task"] = kanban_task
        task["kanban_task"] = kanban_task
    events.append(item)


def cmd_list(args: argparse.Namespace) -> None:
    data = load_backlog()
    for task in data.get("tasks", []):
        status = task.get("status", "pending")
        if args.status and status != args.status:
            continue
        if args.open and status in {"completed", "cancelled"}:
            continue
        print(f"{task.get('id')}\t{status}\t{task.get('priority', '-')}\t{task.get('title')}")


def cmd_show(args: argparse.Namespace) -> None:
    data = load_backlog()
    task = find_task(data, args.id)
    print(json.dumps(task, ensure_ascii=False, indent=2))


def cmd_start(args: argparse.Namespace) -> None:
    data = load_backlog()
    task = find_task(data, args.id)
    task["status"] = "in_progress"
    task["started"] = task.get("started") or now_iso()
    append_event(task, "start", args.note, args.kanban_task)
    save_backlog(data)
    print(f"started {args.id}")


def cmd_block(args: argparse.Namespace) -> None:
    data = load_backlog()
    task = find_task(data, args.id)
    task["status"] = "blocked"
    task["blocked_at"] = now_iso()
    task["blocked_reason"] = args.reason
    append_event(task, "block", args.reason, args.kanban_task)
    save_backlog(data)
    print(f"blocked {args.id}")


def cmd_review(args: argparse.Namespace) -> None:
    data = load_backlog()
    task = find_task(data, args.id)
    task["status"] = "review"
    task["review_at"] = now_iso()
    if args.summary:
        task["review_summary"] = args.summary
    append_event(task, "review", args.summary, args.kanban_task)
    save_backlog(data)
    print(f"review {args.id}")


def cmd_done(args: argparse.Namespace) -> None:
    data = load_backlog()
    task = find_task(data, args.id)
    task["status"] = "completed"
    task["completed"] = now_iso()
    if args.summary:
        task["result"] = args.summary
    append_event(task, "done", args.summary, args.kanban_task)
    save_backlog(data)
    print(f"completed {args.id}")


def cmd_cancel(args: argparse.Namespace) -> None:
    data = load_backlog()
    task = find_task(data, args.id)
    task["status"] = "cancelled"
    task["cancelled_at"] = now_iso()
    if args.reason:
        task["cancelled_reason"] = args.reason
    append_event(task, "cancel", args.reason, args.kanban_task)
    save_backlog(data)
    print(f"cancelled {args.id}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage docs/backlog.json, the project source of truth")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("--status", choices=sorted(VALID_STATUSES))
    p_list.add_argument("--open", action="store_true", help="hide completed/cancelled tasks")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show")
    p_show.add_argument("id")
    p_show.set_defaults(func=cmd_show)

    p_start = sub.add_parser("start")
    p_start.add_argument("id")
    p_start.add_argument("--kanban-task")
    p_start.add_argument("--note", default="")
    p_start.set_defaults(func=cmd_start)

    p_block = sub.add_parser("block")
    p_block.add_argument("id")
    p_block.add_argument("--reason", required=True)
    p_block.add_argument("--kanban-task")
    p_block.set_defaults(func=cmd_block)

    p_review = sub.add_parser("review")
    p_review.add_argument("id")
    p_review.add_argument("--summary", default="")
    p_review.add_argument("--kanban-task")
    p_review.set_defaults(func=cmd_review)

    p_done = sub.add_parser("done")
    p_done.add_argument("id")
    p_done.add_argument("--summary", default="")
    p_done.add_argument("--kanban-task")
    p_done.set_defaults(func=cmd_done)

    p_cancel = sub.add_parser("cancel")
    p_cancel.add_argument("id")
    p_cancel.add_argument("--reason", default="")
    p_cancel.add_argument("--kanban-task")
    p_cancel.set_defaults(func=cmd_cancel)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
