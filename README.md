# backlog

跨会话任务追踪 Skill for Claude Code。

## 特性

- **持久化存储**：任务保存在 `docs/backlog.json`，跨会话保留
- **简单命令**：`/backlog`、`/backlog add`、`/backlog done`
- **结构化任务**：支持 why/what/checklist，记录完整上下文
- **优先级管理**：high/medium/low 优先级分类

## 安装

1. 复制 `.claude/skills/backlog/` 到你的项目：

```bash
mkdir -p .claude/skills
cp -r path/to/backlog/.claude/skills/backlog .claude/skills/
```

2. 创建任务文件：

```bash
mkdir -p docs
cp path/to/backlog/examples/backlog.json docs/backlog.json
```

3. （可选）在 `CLAUDE.md` 中添加说明：

```markdown
## Skills

- **/backlog** - 待办队列管理（查看待办、添加任务、标记完成）
```

## 使用

| 命令 | 说明 |
|------|------|
| `/backlog` | 显示所有待办任务 |
| `/backlog add "任务标题"` | 添加新任务 |
| `/backlog start <id>` | 开始任务 |
| `/backlog done <id>` | 完成任务 |

## 任务结构

```json
{
  "id": "short-id",
  "title": "任务标题",
  "status": "pending | in_progress | completed",
  "priority": "high | medium | low",
  "why": "为什么要做",
  "what": "具体做什么",
  "checklist": ["步骤1", "步骤2"]
}
```

## 与 Claude Code 内置 Task 的区别

| 特性 | /backlog | Claude Code Task |
|------|----------|------------------|
| 存储 | 文件持久化 | 会话内存 |
| 生命周期 | 跨会话 | 会话结束消失 |
| 用途 | 长期待办队列 | 当前工作步骤分解 |

## License

MIT
