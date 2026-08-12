# Data Model: 039-session-export

实体清单:3 个(导出目录、会话描述文档、支持矩阵)+ 1 个运行时输入面(宿主会话存储,只读)。

## Entity 1: 导出目录(Export Bundle)

**持久化位置**: `<项目根>/.session-export/<name>/`(STR-001)。

### Fields

| 字段 | 类型 | 必填 | 约束 |
|------|------|------|------|
| `name`(身份) | string | 是 | 目录名 = 用户指定值;安全路径段文法(首字符字母/数字,其余 `[A-Za-z0-9_.-]`,同 goal 身份文法);导出根内唯一,冲突默认拒绝 |
| `main.<ext>` | file | 是 | 会话主记录,保留宿主原生形态(jsonl 等);运行中会话为截至导出时点的快照 |
| `subagents/` | dir | 否 | 子代理日志(宿主有则导出,无则缺省) |
| `state/` | dir | 否 | 状态目录与段日志(宿主有则导出) |
| `large-results/` | dir | 否 | 超大工具结果(既有分段机制迁移,不因体积静默丢弃) |
| `request-ids.jsonl` | file | 否 | 仅可提取 requestId 的 CLI 附带(既有能力面保持) |
| `session-meta.json` | file | 是 | 元信息机读形态(Entity 2 的确定性半体) |
| `SESSION.md` | file | 是 | 会话描述文档(Entity 2) |

### Lifecycle

```text
(无) ──export --name N──▶ 存在(preview 门禁 + 冲突检查后写入)
存在 ──同名再导出──▶ 默认拒绝 ──交互确认覆盖──▶ 清空后重写
```

- 导出对宿主会话存储**只读**;导出目录自身的生命周期由用户管理(入库与否、删除与否均不由机制代决)。

## Entity 2: 会话描述文档(Session Description)

**持久化位置**: 导出目录内 `SESSION.md`(固定文件名)+ `session-meta.json`(机读元信息)。

### Fields(元信息节,全部脚本确定性提取)

| 字段 | 类型 | 来源 |
|------|------|------|
| `tool` | string | 识别/指定的工具(STR-002 六家规范名) |
| `session_id` | string | 宿主会话 ID |
| `model` | string | 记录内最后使用的模型(既有 `_last_model` 语义) |
| `workspace` | string | 会话工作区路径(记录内 cwd) |
| `started_at` / `ended_at` | ISO-8601 | 记录首末事件时间;运行中会话 `ended_at` = 快照时点且 `snapshot: true` |
| `message_count` / `turn_count` | int | 记录规模计数 |
| `exported_at` | ISO-8601 | 导出执行时间 |
| `over_summary_budget` | bool | 预算判定(行数 > 50,000 或字节 > 32 MB) |

### 结构化总结节(agent 补写)

三段:**任务脉络**、**关键决策**、**产物清单**。约束:忠实于原始记录(FR-013/FR-014);`over_summary_budget: true` → 骨架总结 + 显式声明降级原因与触发阈值;MUST NOT 虚构。

### Validation Rules

1. `SESSION.md` 与 `session-meta.json` MUST 同出——元信息两形态逐字段一致(机读为权威)。
2. 元信息字段与原始记录可对照(抽查语义,契约测试以构造夹具断言)。
3. 总结节存在性强制;降级声明与 `over_summary_budget` 判定一致。

## Entity 3: 支持矩阵(Support Matrix)

**持久化位置**: `skills/export-session/SKILL.md` 的支持矩阵表(人读)+ `export.py` 的 `PARSERS` 注册表(机读事实源)。

| 工具(STR-002) | 会话存储形态 | 可导出性(本环境探测) | requestId |
|----------------|--------------|------------------------|-----------|
| `claude-code` | `~/.claude/projects/**.jsonl` | ✅ 既有适配器,适配目录形态 | ✅ |
| `codex-cli` | `~/.codex/sessions/**` | ✅ 既有适配器,适配目录形态 | ✅(既有可提取者保持) |
| `qoder-cli` | `~/.qoder/**`(含 workspace db) | ✅ 既有适配器,适配目录形态 | ✅(既有可提取者保持) |
| `opencode` | `~/.local/share/opencode/opencode.db`(SQLite) | ✅ 既有适配器,适配目录形态 | 按既有能力面 |
| `copilot` | **未探测到落盘**(本机 ~/.copilot / ~/.config/github-copilot 等不存在) | ⚠ 探测式适配器:available() 按候选路径探测,无源 → 退出码 4 + 诚实声明 | — |
| `hermes` | **未探测到落盘**(本机 ~/.hermes 等不存在) | ⚠ 同上 | — |

- 矩阵外产品(qwen-code / qoder-IDE / qoderwork / oh-my-pi / kimi-code / codex-app)MUST 零残留。
- 探测式适配器未来探测到真实落盘 → 升级为完整适配器(独立迭代,不在本需求)。

## 输入面: 宿主会话存储(只读)

六家 CLI 各自的会话落盘位置为**外部输入**,机制只读;导出前后存储文件字节不变(SC-005 断言面)。
