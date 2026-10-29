# SDD Routing Definitions — 授权路由与 SDD 调用分类

**Owner（唯一所有者）**: 本文件 `shared/definitions/sdd-routing-definitions.md` 是「一次变更何时走 SDD、何时直接修改、何时必须裁定」这条路由规则的唯一所有者。它拥有**四项事实**，且只有本文件可以把它们写出来：

| # | 事实 | 本文件落点 |
|---|------|-----------|
| F-1 | 五项声明输入的封闭取值域 | § Inputs |
| F-2 | 三值裁决表（`[[STR-004]]` / `[[STR-005]]` / `[[STR-006]]`） | § Verdict table |
| F-3 | 固定优先级 | § Precedence |
| F-4 | 理由码词表（封闭） | § Reason codes |

**引用纪律**: 其他任何位置——命令模板、技能、驱动入口、裁决记录形状、契约、测试——MUST 以「路径 + 章节锚」引用本文件，MUST NOT 复制上表任一项，MUST NOT 以表格 / YAML / JSON / 代码常量的形式再声明一份「输入 → 裁决」的映射；仓库中 MUST NOT 出现第二份路由数据文件或常量表。判据与两份合法重复的唯一真源是 `.specify/shared/guidelines/one-source-of-truth.md`。

**机读面**: 唯一的读取者是只读 stdlib 引擎 `scripts/python/sdd-route.py`（动作 `route` / `authorize` / `golden`）。它在运行时解析本文件，MUST NOT 自带第二份取值域、裁决表、优先级或理由码；引擎的接口与退出码归 `contracts/routing-decision.md` C-28 所有。

**字面量登记处**: `[[STR-001]]` … `[[STR-010]]` 的取值与语义 owner 是 Feature 074 切片 `074a-authorized-routing` 的 `requirements.md` § Shared Strings；本文件以 `[[STR-NNN]]` 引用其语义，不另立第二张字面量表。

**不在本文件（只给指针，不复述）**:

| 主题 | 所有者 |
|------|--------|
| 复杂度层级名、判定信号与思考深度处方 | `.specify/shared/guidelines/task-complexity-rubric.md` |
| 质量门与确认门集合 | `.specify/shared/guidelines/confirmation-gates.md` 与宪法质量原则 |
| Goal / Target 的身份、状态机与绑定 | `shared/definitions/goal-definitions.md` |
| 驱动的阶段名册、状态脊、哨兵、U0–U6 | `skills/external/sdd-loop-driver/SKILL.md` |
| 反嵌套义务与其派发前探针 | `shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation；`skills/internal/run-agent/SKILL.md` |
| 中立元数据键集（`[[STR-001]]` 的取值域与缺省） | `src/specify_cli/__init__.py` `NEUTRAL_AGENT_METADATA_KEYS` |
| `team.md` frontmatter schema（`[[STR-010]]` 块映射） | `skills/internal/create-team/references/create-mode.md` § Persisted `team.md` schema |

## Hierarchy

控制层级只有一条，且有唯一一条边界：

1. **Goal** 是最高层：它陈述一个目标与可验证的成功判据（身份与状态机归 `shared/definitions/goal-definitions.md`）。
2. **Team** 绑定一个 Goal，编排 Agent 成员；Team 不重写 Goal，只把 Goal 拆成成员职责。
3. **Agent** 执行一条职责（duty）；职责是路由与授权的计量单位——一次裁决对应一条职责，而不是一个文件或一次提交。
4. **SDD 运行**（`sdd-loop-driver`）是从属执行路径：它由**已获有效授权的 Agent** 启动，为一条职责产出 SDD 工件链，并在 review 完成后交回 handoff。

**边界**: 任何 SDD 运行 MUST NOT 创建、重绑、改范围或终止 Goal、Target、Team 或 roster。下层不得改写上层的定义；需要改变上层的动作 MUST 返回给上层执行者（Goal 侧归 `/speckit.goal`，Team 侧归 `/speckit.team` 的既有写线），而不是在运行内就地改写。层级不新增结构字段、不新增强制绑定。

## Direct modification

**直接修改** = 执行一次变更而**不产生 SDD 工件链**：不建立工件链、不经过驱动的阶段与哨兵、不产出 handoff。

它与 SDD 运行只在这一件事上不同，**不是减免**：

- 直接修改仍受**全部适用的质量门与确认门**约束——门禁集合按路径引用 `.specify/shared/guidelines/confirmation-gates.md` 与宪法质量原则，本文件不复述其中任何一条；
- 直接修改仍留下可复核的执行证据（改了什么、按什么判据、谁做的）；
- 「改动看起来很小」不是走直接修改的理由：理由只有一项——裁决值（F-2），由声明的五项输入推出，不由改动规模、文件数量或作者身份推出。

两者的区分因此是可判定的：SDD 运行留下工件链与 handoff，直接修改不留下；而**是否应当**走其中一条，由本文件的三值裁决表回答，不由调用方自行判断。

## Invocation kinds

一个 Agent 在启动一项工作前，只有**四种**调用类型可选，且四者的身份不得混用：

| # | 调用类型 | 入口 | 是否 SDD 调用 |
|---|----------|------|---------------|
| 1 | **SDD 开发流程**（development flow） | `sdd-loop-driver` | 是——且只有它是 |
| 2 | **框架引导**（bootstrap） | `sdd-project-setup` | 否 |
| 3 | **周期性维护**（house-keeping） | `sdd-house-keeping` | 否 |
| 4 | **直接修改**（direct modification） | 无技能、无驱动 | 否 |

规则：

- **引导与维护不同于开发流程**：`sdd-project-setup` 与 `sdd-house-keeping` 是框架的引导与维护路径，它们各自有既定职责，MUST NOT 被读作「轻量的 SDD 运行」，也 MUST NOT 取代开发流程。
- **只有驱动构成 SDD 调用**：在嵌套入口契约下（`skills/external/sdd-loop-driver/references/nested-invocation.md`），只有 `sdd-loop-driver` 的调用算作一次 SDD 调用。
- **无 `.specify/` 结构的目标项目走引导路径**：当一次被分流为 SDD 的变更落到尚无 `.specify/` 结构的目标项目时，路由是**引导路径**（`sdd-project-setup`），MUST NOT 把 SDD 分流降级为直接修改——降级会让该变更永久失去工件链与 handoff，而这两件正是它被分流为 SDD 的原因。
- **引导与维护派发子代理时适用同一有效授权谓词**：当 `sdd-project-setup` 或 `sdd-house-keeping` 派发子代理时，该派发与一次 SDD 调用适用**同一个**有效授权谓词——同一个键 `[[STR-001]]` 的两个半边（Agent 定义能力 AND 席位策略，席位侧载体为 `[[STR-010]]` 块映射），按 (team, seat) 解析，可执行形态是 `python3 scripts/python/sdd-route.py --action authorize`。谓词不是第二个谓词，其义务位点归 `shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation。
