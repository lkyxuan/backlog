---
name: backlog
version: "3.0.0"
description: 跨会话任务追踪 - 长期待办队列管理
user-invocable: true
---

# /backlog - 待办队列管理

基于 `docs/backlog.json` 的跨会话任务追踪。

## 命令

| 命令 | 说明 |
|------|------|
| `/backlog` | 显示所有待办任务 |
| `/backlog add "标题"` | 添加新任务 |
| `/backlog start <id>` | 开始任务（status → in_progress） |
| `/backlog done <id>` | 完成任务（status → completed） |

## 任务结构

```json
{
  "id": "简短英文ID（用于引用）",
  "title": "任务标题（一眼能看懂）",
  "status": "pending | in_progress | completed",
  "priority": "high | medium | low",
  "why": "为什么要做这个任务",
  "what": "要做什么",
  "checklist": ["步骤1", "步骤2"]
}
```

## 命名规范

- **id**: 简短英文，用于命令引用，如 `merge-queues`
- **title**: 让用户一眼看懂，如 `合并 Celery 队列为单一维护队列`

**示例**：
```json
{
  "id": "merge-queues",
  "title": "合并 Celery 队列为单一维护队列"
}
```

## AI 行为

1. **会话开始**：读取 backlog.json，显示待办任务
2. **开始任务**：设置 status → in_progress
3. **完成任务**：设置 status → completed，显示剩余待办
4. **更新后提交**：提醒用户 git push

## 与 Claude Code 内置 Task 的区别

| 特性 | /backlog | Claude Code Task |
|------|----------|------------------|
| 存储 | 文件持久化 | 会话内存 |
| 生命周期 | 跨会话 | 会话结束消失 |
| 用途 | 长期待办队列 | 当前工作步骤分解 |
| 信息量 | why/what/checklist | 简单描述 |
