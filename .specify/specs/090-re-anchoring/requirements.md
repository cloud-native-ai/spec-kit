# Requirements Specification: Re-Anchoring（不忘初心 · 温故而知新）

**Requirement Branch**: `090-re-anchoring`
**Created**: 2026-11-08
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

**Input**: 用户裁定（逐字要点）：「将『开局加载一次』的动作，变成『每执行完一个核心步骤就再加载一次』，使用 session compact + reload + evaluation 来明确和最开始的方向是否存在偏差；在核心概念中针对 agent 加入『不忘初心：一直记得最开始的任务和规则』和『温故而知新：通过不断复习来强化记忆和回顾目标』」。后续纠正（逐字要点）：「回顾的重点应该是规则而不是目标，因为当前正在做和下一步要做就已经隐含了目标在内，经常会被遗漏的是规则；以『无人值守』被忽略而工作仍一步步推进为例。」

## Related Feature

**Feature ID**: 090
**Feature Name**: Re-Anchoring（不忘初心 · 温故而知新）

## Overview

长会话中规则会静默丢失：目标由当前/下一步隐含，而「无人值守」「不征求继续」「U4→下一阶段」「先写脊后行动」等规则一旦被丢弃，不再在任何动作里显形。本特性把「开局加载一次」改为**按核心步骤重载**：agent 在入口固化**任务锚 + 规则锚**，每完成一个核心步骤执行 compact → reload → evaluate，先问规则、后问任务，给出 `on-track` / `correction-applied` / `decision-needed` 三值判定。

## Functional Requirements

- **FR-001**: 框架 MUST 提供 Re-Anchoring 的唯一 owner 文档 `shared/definitions/re-anchoring-definitions.md`，拥有两个概念、重载分层与 agent 义务。
- **FR-002**: 宪法模板与本仓宪法 MUST 各新增一条 Re-Anchoring 原则，标题一致，正文以指针引用 owner 文档。
- **FR-003**: 指令模板与 `instructions.md` MUST 各新增一条常驻段（摘要 + owner 指针）。
- **FR-004**: 方向锚 MUST 同时包含任务锚（目标逐字、非目标、验收权威、阶段计划、裁定门）与**规则锚**（无人值守/不征求继续/U4→下一阶段/先写脊后行动/workspace guard/fast-fail/确认门/预算）。
- **FR-005**: 每个核心步骤后的五问 MUST **规则优先**：本步受哪些规则约束且是否仍生效 → 上一动作是否在规则下完成 → 下一步是否为计划命名的那一步 → 状态载体是否更新 → 领地/工作区签名是否干净。
- **FR-006**: 重载 MUST 分层：T0（方向锚摘要，每核心步骤）、T1（规则摘要，阶段边界/压缩后/子代理轮次上限后）、T2（全文，仅在派发形态不清或处置卡死时）；MUST NOT 每工具调用重载全文。
- **FR-007**: 审计结论是陈述，MUST NOT 以征求用户「继续」收尾；只有 `decision-needed` 上送。
- **FR-008**: `agent-definitions.md` MUST 声明 agent 侧义务：入口复述方向锚，核心步骤后先重读规则并记录五问判定；派发简报携带锚摘要。
- **FR-009**: `manage-constitution` 的 MUST include 清单 MUST 新增该原则条目。
- **FR-010**: 既有双落地/快失败计数 pin MUST 与新增原则同批移动，并有契约测试守护。（clarify C-4：本特性实际使用**两个**守护测试文件——`tests/contract/test_reanchoring_contract.py` 管五处面的存在性与指针，`tests/contract/test_sdd_loop_driver_reanchor.py` 管 checkpoint 协议第 5 部分、分层与三值判定；两者同属 FR-010 的守护面。）

### Runtime Stack & Dependency Ownership

本特性自身的运行时栈与依赖所有权表（`execution` 类必填；`Premises` 指向 plan 阶段将定义的执行前提）。
本特性不新增运行时：它消费的解释器与测试运行器都是既有框架已声明的依赖。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | Python 3 解释器（运行本特性的契约测试与既有引擎） | signed-contract | CPython 上游（本仓只消费） | `requires-python >= "3.8"`（`pyproject.toml` 已声明；本特性零新增第三方依赖） | `pyproject.toml` | `tests/contract/test_reanchoring_contract.py` 在 `>=3.8` 解释器上通过；本特性零新增 import | FR-010 | EP-001 |
| RS-002 | pytest（契约测试运行器） | signed-contract | pytest 上游（本仓只消费） | `pytest 9.0.3`（2026-11-09 实测 `/usr/bin/python3 -m pytest --version`；closure 比较前须重新核对） | `scripts/bash/run-tests.sh` | `test_constitution_double_landing` 与 `test_fast_fail_discipline` 全绿，合并树对 `origin/master` 基线零新增失败 | FR-010 | EP-001 |

## Success Criteria

- **SC-001**: owner 文档、两侧宪法、两侧指令面、agent 条款五处同时存在且以指针互引（契约测试）。 **Path**: final
- **SC-002**: 五问顺序在 checkpoint 协议中明确为「规则优先」，并有契约测试钉住。（clarify C-4 收紧判据：协议侧已满足——Q1 即规则；「钉住」不得以任意 `Q1` 字面命中或「三值判定存在」代为满足，必须在同一测试内同时断言 Q1 问的是规则**且**判定/动作先于目标；落地归属见 FR-010 与 C-4。） **Path**: final
- **SC-003**: 双落地计数与 watchlist 同批移动；`test_constitution_double_landing` 与 `test_fast_fail_discipline` 绿。 **Path**: final
- **SC-004**: 方向审计的 T0/T1/T2 分层在 owner 文档与 checkpoint 协议中一致。 **Path**: final

### Measurement Sources & Collection Methods

- **SC-001 Source**: 契约测试 `tests/contract/test_reanchoring_contract.py`（五面存在性 + 指针）与 `tests/contract/test_sdd_loop_driver_reanchor.py`（协议第 5 部分），逐面记录命令、退出码与命中行到 `test-evidence/`。
- **SC-002 Source**: 同一契约测试模块内对 checkpoint 协议的新增顺序断言：断言 Q1 问的是规则且判定/动作先于目标（被改回目标优先时转红）；命令、退出码与失败复现记录进 `test-evidence/`。
- **SC-003 Source**: `test_constitution_double_landing.py` 的 `TEMPLATE_COUNT` / `LIVE_COUNT` / `COMMAND_COUNT` / `DOUBLE_LANDING_WATCHLIST` 与 `test_fast_fail_discipline.py::test_x15` 的 `len(entries)` 读数，按名与 `origin/master` 基线比较。
- **SC-004 Source**: owner 文档 §2 的 T0/T1/T2 表与 `checkpoint-protocol.md` §5 的 reload tier 行逐项比对，记录两侧路径与行号。

## Clarifications

<!-- 由 /speckit.clarify 填充：- Q: <question> → A: <answer> -->

### Session 2026-11-09

本会话模式 **A（post-requirements）**，目标文件本文件。无人值守运行：全部疑点由本代理自行裁定，依据是仓库实测 + 既定裁定（状态脊 `direction_contract`）+ 相邻兄弟特性的惯例，不向用户提问。每条裁定都注明落点；**未改写任何已实现的规则文本**——本特性实现已预落地，clarify 只校准规格面。

**前置实测**（澄清的事实基座，均为本次实跑）：`/usr/bin/python3 --version` → `Python 3.11.0rc1`；`/usr/bin/python3 -m pytest --version` → `pytest 9.0.3`（与 RS-002 记录一致）；`pyproject.toml:5` → `requires-python = ">=3.8"`；`test_reanchoring_contract.py` + `test_sdd_loop_driver_reanchor.py` + `test_constitution_double_landing.py` 合计 **27 passed in 0.15s**；`shared/` 与 `.specify/shared/` 两份 definitions、以及 checkpoint-protocol 的两份镜像 `diff` 全部 IDENTICAL。

- Q: 五处面（owner 文档、两侧宪法、两侧指令面、agent 条款）是否真的同时存在，且以指针互引？ → A: **是，全部实测存在且互引。** owner `shared/definitions/re-anchoring-definitions.md`（63 行，头部声明它拥有「概念定义 / 重载分层 / agent 侧义务」并把执行步骤指给 `checkpoint-protocol.md § Direction audit`）；宪法两侧 `templates/constitution-template.md:389` 与 `.specify/memory/constitution.md:490` 标题逐字相同；指令两侧 `templates/instructions-template.md:106` 与 `.specify/instructions.md:118` 的 `## Re-Anchoring (不忘初心 · 温故而知新)` 段均含 owner 指针；`shared/definitions/agent-definitions.md:107` 起有 `## Re-Anchoring Obligation` 段。**Why**：SC-001 是存在性 + 指针命题，必须逐面取证而非凭提交信息。**落点**：SC-001、FR-001…FR-003、FR-008。

- Q: 宪法两侧的**条号**不同（模板 `XXI.` vs 本仓 `XXII.`），而计数 pin 也不同（`TEMPLATE_COUNT = 21` vs `LIVE_COUNT = 22`）——这是漂移还是正当差异？ → A: **裁定：正当差异，不是缺陷，MUST NOT 被「修齐」。** 实测两侧 rostor 逐条比对：本仓宪法含 13 条项目自身原则（SDD as Foundation、Intent-Driven、Code as SSOT、Dogfooding、Tool Reuse 等）在模板中不存在，故同一条 Re-Anchoring 在模板是第 21 条、在本仓是第 22 条。FR-002 只要求**标题一致**与指针引用，未要求条号相同；把条号强行对齐会反过来破坏两份文档各自的自洽。**落点**：FR-002 的解释口径、A2。

- Q: FR-009 要求 `manage-constitution` 的 MUST include 清单新增该原则——是否本当落地？ → A: **已落地。** `skills/internal/manage-constitution/SKILL.md:259`（及镜像）在 `- **MUST include**` 子条目块内新增 `Re-Anchoring (不忘初心 · 温故而知新)`，`test_constitution_double_landing.py` 的 C-7 通过其 `generator_names` 集合守卫该清单。**落点**：FR-009。

- Q: SC-002 声称「五问顺序在 checkpoint 协议中明确为『规则优先』，**并有契约测试钉住**」——这一命题是否成立？ → A: **裁定：命题前半句成立、后半句不成立，SC-002 的「钉住」在当前树上无对应守卫。** 实测：`checkpoint-protocol.md § Direction audit` 明确写明「The audit's primary object is the RULES, not the goal」，且五问的 Q1 即「Which rules govern this step…」（`checkpoint-protocol.md:102` 的 `- Q1 rules:`），顺序正确；但全仓 `tests/` 内对「规则优先 / rule-first / rules first / Q1」的检索**没有任何一处**断言该顺序（唯一命中 `tests/unit/test_measure_unit.py` 的 Q2 与本特性无关，其余命中是 humanize 夹具正文里的「Q1/Q2 季度」字样）。`test_sdd_loop_driver_reanchor.py` 断言的是五部分存在、T0/T1/T2 出现、三值判定与「禁止每步全量重载」，**不含顺序断言**；按本项目 fast-fail「机器给出的绿同样受判据约束」，这些绿不能代偿 SC-002。**裁定处置**：不改写 SC-002 的意图，而是在其权威位置收紧判据（已就地补记），并把「补一条顺序断言」作为一件**可验证的缺口**移交 plan/tasks——本阶段不新增测试（clarify 不产生实现）。**Why**：这正是本特性要防的失败模式——声明了「规则优先」却没有任何东西在它被改回「目标优先」时报红；若在此默默放过，SC-002 就成了一条永远为真的空声明。**落点**：SC-002（判据收紧）、FR-010（守护面归属）、A5。

- Q: FR-010 与 RS-002 只点名 `test_reanchoring_contract.py` 与 `test_constitution_double_landing.py` / `test_fast_fail_discipline.py`，但树上还存在第三个守护测试 `test_sdd_loop_driver_reanchor.py`——它是本特性的还是他特性的？ → A: **它是本特性的守护面，此前被规格漏记。** 实测其 docstring 逐字描述本特性要修的事故（「driver manual was loaded once at session start … package boundaries ended in approval requests, the spine lagged」），`pytestmark = pytest.mark.contract`，路径为 `tests/contract/test_sdd_loop_driver_reanchor.py`，守护 `skills/external/sdd-loop-driver/` 的 SKILL 与 checkpoint 协议（含 `test_minimal_shape_has_part_five` 检查 minimal shape 模板第 5 部分）。**裁定**：它是 FR-010 的第二条守护面，已补记进 FR-010；RS-002 的联合验收句只列两条测试名，属**枚举不全而非事实错误**，其验收结论（「零新增失败」）不受影响，故不在 clarify 改写 RS 行，交由 plan 的 Premises/验收口径统一。**落点**：FR-010、SC-003、A5。

- Q: 「既有双落地/快失败计数 pin 与新增原则同批移动」是否真的同批？ → A: **是，实测同批。** `test_constitution_double_landing.py`：`TEMPLATE_COUNT` 20→21、`LIVE_COUNT` 21→22、`COMMAND_COUNT` 13→14，三行均带 `# stale-pin update (2026-11-09, 090)` 注释；`DOUBLE_LANDING_WATCHLIST` 新增 `"Re-Anchoring (不忘初心 · 温故而知新)",  # 090: 8 -> 9`，`test_fast_fail_discipline.py::test_x15` 以 `len(entries) == 9` 钉住。`test_x13` 的三个期望值由制品自身推导而非字面复述，故本条「同批」是**可复算**的。**落点**：FR-010、SC-003。

- Q: 「来源面」多处并存（`shared/` 源、`.specify/shared/` 运行时投影、`skills/external/...`、`.specify/skills/...`），clarify 的裁定写入哪一面？ → A: **裁定：本阶段只写本特性规格面 `.specify/specs/090-re-anchoring/requirements.md`，MUST NOT 触碰任何实现或镜像。** 依据 Two Hats：实现已预落地于框架源并已同步为镜像（实测 `diff` 全部 IDENTICAL），clarify 不是授权改动它们的阶段；任何对 owner/协议/测试的修改都必须走后续 plan→implement→review 的门。**落点**：本会话的写入边界、A6。

- Q: RS-001 / RS-002 的 `Premises` 列引用 `EP-001`，而本特性没有 `plan.md`——`EP-001` 是否悬空？ → A: **裁定：悬空是预期的、且不构成 clarify 缺陷。** 兄弟特性（084/085/089）的一致惯例是：`requirements.md` 的 RS 表引用 `EP-xxx`，其定义落在**该特性的 `plan.md`**（如 `085/plan.md:161` 定义 EP-001 为「Python 3.8+ and pytest are available；合同测试本地可跑」）。090 尚处 clarify、plan 未生成，故 EP-001 必待 plan 落地；本行 `Runtime Stack & Dependency Ownership` 节头也自述「Premises 指向 plan 阶段将定义」。本特性两个 RS 所指的 EP-001 内容与 085 同形（Python 3.8+ / pytest 可本地跑），实测已满足（3.11.0rc1 + pytest 9.0.3 + 27 passed 无网络依赖）。**落点**：A3、plan 阶段义务。

- Q: `flow_class=execution` 的运行时栈表（RS-001/RS-002）是否满足「零新增依赖」并可实测复算？ → A: **是。** `pyproject.toml` 无新增依赖行（本特性零新增第三方依赖，RS-001 pin 为既有 `requires-python >= "3.8"`）；RS-002 的 `pytest 9.0.3` 为 2026-11-09 实测，与文本记载一致。**落点**：RS-001、RS-002、A1。

## Assumptions

- **A1（环境实测量）**: 本阶段全部事实取自本次实跑：CPython 3.11.0rc1、pytest 9.0.3、27 项契约测试全绿。若后续 closure 比较时读数变动，以 plan/implement 阶段的重新测量为准，并以 `pytest --version` 原文入 test-evidence（RS-002 已要求「closure 比较前须重新核对」）。
- **A2（条号差异是正当的）**: 模板与本仓宪法对同一原则使用不同罗马数字（XXI / XXII）与不同计数（21 / 22），原因是本仓宪法比模板多 13 条项目自身原则；FR-002 的约束面是**标题一致 + 指针引用**，不是条号。
- **A3（EP-001 由 plan 落地）**: RS 表引用的 `EP-001` 是本特性将在 `plan.md` 定义的执行前提（Python 3.8+ 与 pytest 本地可跑），当前悬空属预期；plan 阶段 MUST 把它写成可验证行（形如 `085/plan.md` 的 Premises 表）。
- **A4（clarify 不产生实现）**: 本阶段只把核定答案写回规格面；任何被发现的实现缺口（含 SC-002 的顺序守卫缺失）都不在 clarify 修复，而作为可验证条目移交 plan/tasks。
- **A5（守护面共两个文件 + 两个计数守卫测试）**: 本特性的契约守护面是 `tests/contract/test_reanchoring_contract.py`（五面存在性与指针）与 `tests/contract/test_sdd_loop_driver_reanchor.py`（协议第 5 部分、分层、三值判定、禁全量重载），另由既有的 `test_constitution_double_landing.py`（C-7 watchlist / C-13 计数 pin）与 `test_fast_fail_discipline.py`（C-15 watchlist 条数）承担 FR-010 的计数与登记面。
- **A6（写入边界）**: 本阶段唯一写入对象是 `.specify/specs/090-re-anchoring/requirements.md`；已实现的规则文本（owner 文档、宪法、指令、agent 定义、checkpoint 协议、测试）一律不改写以迁就规格。

## Note

本特性的实现在本分支上**预先落地**（提交 `5a1041e4`、`55776937`（原 087 线，已重放到 090）），需求规格在 2026-11-08 从 086 中拆出（原编号 087，因远端占用重编号为 090）后建立；后续按 SDD 链补齐 clarify/plan/tasks 与 review。
