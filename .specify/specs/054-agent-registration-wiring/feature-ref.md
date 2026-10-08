# Feature Reference — 054 → Feature 044

**Requirement**: `054-agent-registration-wiring`(`.specify/specs/054-agent-registration-wiring/requirements.md`)
**Bound Feature**: **Feature 044 Agent Metadata Portability**(`.specify/memory/features/044.md`;绑定裁定 2026-10-08 via /speckit.clarify:渲染器与三目录分类法是 044 的交付物,本 spec 补它未接完的输入面与触发面,与既绑 spec 040 并列;绑定不回退 044 的 Implemented 状态——Principle VII 无回退门)

## 本计划如何映射到 Feature 044

| spec 040 交付的(既有) | spec 054 补上的(本计划) |
|---|---|
| 中性元数据契约 + 校验器(`load_project_agent_definitions`/`validate_agent_metadata`) | `team-scope` framework-only 键入键集(席位来源追溯,FR-013) |
| `render_agents_for_tool` 真文件渲染(manifest 漂移/修剪/legacy 迁移) | 渲染输入面接线:建队时席位实例化(方案 b,FR-004/006) |
| `_AGENT_METADATA_MAPPING` 四渲染工具映射 + provenance | 触发面接线:`specify render-agents --ai <tool>` 窄子命令(FR-004) |
| 三目录分类法(agent-definitions.md) | 「宿主注册面」概念定义 + 席位实例分类学条目(owner 落 044 既有的 agent-definitions.md) |
| spec 040 退役了 symlink 模型(renderer 端) | 教学面跟上退役(FR-001..003,F-A02 死信终结)+ IDE agent 面文档(FR-009/010) |

## FR → 制品 → 落点

| FR | 契约/制品 | 实现落点 |
|---|---|---|
| FR-001..003 | `contracts/teaching-and-guards.md` A-1..A-3 | `templates/commands/agents.md`(+4 工具副本)、`skills/create-agent/SKILL.md` |
| FR-004(实例化)/FR-006/008/013 | `contracts/seat-instantiation.md` C-1..C-5 | `skills/create-team/`、`skills/create-agent/SKILL.md`(键集段)、`src/specify_cli/__init__.py`(键集) |
| FR-004(触发)/FR-005 | `contracts/render-trigger-cli.md` C-1..C-5 | `src/specify_cli/__init__.py`(子命令) |
| FR-007 | (裁定记录)spec FR-007 + Clarifications;`teaching-and-guards.md` §D 引用 | 无新落点(方案 b 已是全计划前提) |
| FR-009/010 | `contracts/teaching-and-guards.md` B-1..B-4 | `shared/definitions/agent-definitions.md`、`shared/workflow/symlink-model.md`、`docs/reference/cli/supported-agent-tools.md` |
| FR-011/012(+SC-003 守卫化) | `contracts/teaching-and-guards.md` C-7..C-10 | `tests/contract/`(守卫 + 变异演练取证) |
| FR-014 | `contracts/modify-backfill.md` C-1..C-4 | `skills/improve-team/`(modify 流程) |

## Feature 登记义务(本计划执行)

- `features/044.md`:Last Updated 增 plan 注记;Key Changes/notes 记录本计划的接线面(已在 clarify 轮登记绑定,plan 轮补 plan 产出)。
- `features.md`:044 行 Last Updated 同步;状态保持 Implemented(无回退)。
- 本计划不新建、不废弃、不合并任何 Feature(复用优先门:044 已覆盖)。
