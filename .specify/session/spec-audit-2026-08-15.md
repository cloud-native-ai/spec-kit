# Spec 全量落地审计 — 2026-08-15

**目标**: 核查 `.specify/specs/` 全部 spec 的交付落地情况（防 032-Dogfooding 类
"交付断链"复发),废弃 spec 归档至 `.specify/archive/spec/`(用户新约定;旧
`.specify/specs/.archive/` 已由用户并行提交 a7318075/d70b0519 平除)。

## 方法

程序化审计(脚本): 每 spec 提取 Feature 绑定、verification SC 计数、tasks 开行、
plan.md Source-Tree 路径存在性探测;可疑项逐个深查。

## 结论总表(41 个活跃 spec)

### 归档 8 个(明确废弃 → .specify/archive/spec/)

| Spec | 废弃依据 |
|------|----------|
| 002-mcp-tool-call | MCP Tool Call Command 从未落地;该能力域 2026 由 mcp-config 技能另行覆盖 |
| 004-speckit-tools-command | 被 016-refactor-tools-command 取代(Feature 016 自述 "replacing discovery-driven approach") |
| 005-tool-skill-ids | 被 016 的 `<TOOL:>`/`<SKILL:>` ID 体系取代 |
| 011-ai-tools-support | Feature 022 的现行绑定是 021;原面被 018/021/024 演进取代 |
| 014-agent-framework-refactor | 023-agent-framework-redesign 的前身(被其取代) |
| 015-role-based-agents | 同上,023 前身 |
| 019-tier2-hermes-iflow | iFlow 已随 v1.9.1 下线;Hermes 由 Feature 022/AGENT_CONFIG 治理;48 个交付路径缺失 |
| 026-agent-team-management | Feature 027 notes 明示 historical;被 036-team-summary 绑定取代 |

### 留存 33 个 — 三类疑点全部消解

- **039-session-export** `skills/export-session` 缺失 = **改名** export-session→archive-session,已注册 OBSOLETE-ASSET-REGISTRY ✓
- **017-consolidate-draft-skills** `draft/skills` 缺失 = **其自身目的**(合并 9 草稿为 3 正式技能后删除草稿,SC 6/6)✓
- **001-unify-command-handoffs** `## Handoffs` 已在全部 23 个命令模板落地;仅 features.md 行陈旧(已修)✓

### 良性缺失(改名/搬迁,均有据)

docs/skills→docs/reference/skills、docs/commands→docs/reference/commands、
docs/installation→docs/tutorials/installation(033 文档再分类);skills/agent-setup→
agent-cli-setup(024);analysis-project→summarize-project(030);organize-agents→
create-team(023);skills/sdd-workflow→shared/workflow(028 自身完成的重定位);
update-agent-context.sh 按 v1.9.1 SIR 删除(018);.specify/goal 与
.specify/memory/feedback/probes 为运行时目录(037/041 设计如此)。

## 数据修复(features.md)

- Feature 019 行 spec 路径: `.specify/specs/.archive/023-...` → `.specify/specs/023-...`(平档后死链)
- Feature 027 行历史提法: `.archive/026` → `.specify/archive/spec/026`
- Feature 001 行: Planned → Completed(spec 路径补全,交付已实证)

## 防复发机制(宪法 XI v1.10.0 机制侧)

- 新守护契约 `tests/contract/test_spec_feature_binding_integrity.py`:
  C-1 features.md 引用的每个 spec 路径必须存在(本次正是它抓出 019 死链);
  C-2 活跃 spec 的数字 Feature 绑定必须有对应 features.md 行。
- 与既有 `test_instructions_section_propagation.py`(模板节传播守护)共同覆盖
  两类已知断链形态。

## verification 状态备注

留存 spec 中 SC 有 fail=0;partial/deferred 共 8 处均为已记录的待实跑项
(036 SC-006/010 等待真实团队 run;016/020/029/031 deferred 为交付后度量),
无未记录缺口。早期 spec(001/003/007-013)无 verification.md(先于该约定),
其交付面由现行守护契约与 features.md 绑定覆盖。
