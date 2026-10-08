# Data Model — 054-agent-registration-wiring

实体与关系为本特性的持久/概念面。既有三层分类法(Agent Template / Instance / Execution)由 `shared/definitions/agent-definitions.md` 拥有,本文引用不重定义。

## Entity 1: Seat Instance(席位实例)

Agent Instance 的子类型:由团队建队/modify 流程从 stage 帧实例化而来、绑定到某团队席位的职责定义。

**字段**(frontmatter = 中性元数据契约,键集 owner 为 `src/specify_cli/__init__.py` 的 `NEUTRAL_AGENT_METADATA_KEYS`):

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` / `description` | 是 | 中性必填键(既有校验规则) |
| `model-tier` / `capability-tools` / `skills` / `run-turn-budget` / `display-color` | 否 | 中性可选键,渲染时映射为宿主字段(既有映射) |
| `team-scope` | **席位必填** | 新增 framework-only 中性键(`renders_to_tools=False`,先例 `role-scope`);值 = 所属团队的 slug;不渲染到任何工具,仅供来源追溯与孤儿检测 |
| `capacity-scope` | 否 | 仅当实例派生自**已注册** capacity template 时设置;stage 帧非已注册 template,故席位实例**不设**此键 |

**正文(body)**:stage 帧实例化后的文本,占位符全部解析(渲染器拒绝未解析占位符的不变量随之满足)。

**校验规则**:
- 必须整体通过 `validate_agent_metadata`(未知键拒绝、占位符拒绝、Qoder 方言键禁止——均为既有行为)。
- `team-scope` 值必须等于一个持久团队的 slug(`.specify/teams/<slug>/team.md` 存在);格式与 team slug 相同(小写连字符)。

**关系**: belongs-to **Team**(经 `team-scope`,多席位对一团队);rendered-to **Host Registration Surface**(经渲染,逐工具)。

**生命周期**: `created`(建队步或 modify 回填)→ `active`(团队在册)→ `orphaned`(团队目录消失而实例仍在)——孤儿态经 `team-scope` 指向不存在的团队而可机检;检测与清理的执行形态属 `/speckit.tasks` 阶段(FR-013 把 WHAT 钉在可检,不钉清理形态)。

**唯一性**: 文件名 slug 在 `.specify/agents/instances/` 内唯一;与既有持久定义同名时建队流程冲突披露、不静默覆写。

## Entity 2: Render Trigger Command(渲染触发命令)

新增 CLI 子命令,把既有渲染器暴露为窄入口。

**字段**:

| 字段 | 说明 |
|---|---|
| 调用形 | `specify render-agents --ai <tool>`(`--ai` 必填) |
| 值域约束 | `<tool>` 必须是 `_AGENT_METADATA_MAPPING` 中 `mode == "render"` 的工具(qoder/claude/copilot/opencode);annotated 模式工具(codex/hermes)或未知名 → 参数错误退出 |
| 行为 | 委派 `render_agents_for_tool(project_path, tool)`;项目路径解析与 init 相同;语义(真文件、manifest 漂移备份、陈旧修剪、legacy 链接替换)不变 |
| 输出 | 既有 stats 投影:`rendered`(数)、`backups`(列表)、`unmapped`(映射失败项);人读 + 机读一行摘要 |
| 退出码 | 0 = 渲染完成(含 rendered=0);非 0 = 元数据校验失败(`AgentMetadataError` 上抛,点名文件与键)或参数错误 |

**关系**: consumes **Seat Instance / Agent Instance / Agent Template**(经 `load_project_agent_definitions`);produces **Host Registration Surface** 上的渲染产物 + **Render Manifest** 更新。

**不变量**: 单次调用渲染一个工具;对同一项目重复调用幂等(产物稳定、manifest 增量);不触碰 manifest 未记录的用户自有文件。

## Entity 3: Host Registration Surface(宿主注册面)

概念实体(非新运行时机制):某工具实际读取 agent 定义的目录,渲染的目标面。定义 owner:`shared/definitions/agent-definitions.md`(2026-10-08 clarify 裁定)。

**属性**: 每渲染模式工具一个,路径取自 `_AGENT_METADATA_MAPPING[tool]["target_dir"]`(如 qoder 的项目级 `.qoder/agents/`——CLI 与 IDE 共享,用户级 `~/.qoder/agents/` 不归框架管);产物为真实文件(非符号链接)。

**关系**: projected-from 中性层(`.specify/agents/{templates,instances}/`,instance 优先);逐工具独立;**对应性**(SC-003):面上的**框架渲染产物**(manifest 所记录)与中性层持久定义集一一对应;用户自有/第三方 agent 共存于同目录但不计入对应性。

## Entity 4: Render Manifest(渲染清单)

既有实体,语义不变(`.specify/agents/.render-manifest.json`;entries `{rel_path: {source, sha256}}`;漂移检测→备份、陈旧修剪、legacy 迁移)。本特性不修改其结构,只把它显名化为两个新消费场景的判定面:SC-003 的「框架渲染产物」集合 = manifest 记录集;守卫测试的对应性断言以它区分框架产物与用户资产。

**关系**: written-by 渲染器(既有);read-by 对应性守卫(新,只读)。
