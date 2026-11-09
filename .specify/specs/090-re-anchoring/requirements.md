# Requirements Specification: Re-Anchoring（不忘初心 · 温故而知新）

**Requirement Branch**: `090-re-anchoring`
**Created**: 2026-11-08
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

**Merge Note (092 → 090, 2026-11-09)**: 本节正文之后追加了 **`## Non-Disposable (092) — merged`** 一节：092 线的 65 条 FR 与 20 条 SC 以 `ND-` 前缀（`ND-FR-001`…/`ND-SC-001`…）机械搬运进来，保持 092 原号以避开本文件的 `FR-001`…；092 原文文件保留未删，本节为合并视图。本节其余内容未因合并而改动。

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
| RS-002 | pytest（契约测试运行器） | signed-contract | pytest 上游（本仓只消费） | `pytest 9.0.3`（2026-11-09 实测 `/usr/bin/python3 -m pytest --version`；closure 比较前须重新核对） | `scripts/bash/run-tests.sh` | `test_constitution_double_landing` 与 `test_fast_fail_discipline` 对冻结基线零新增失败（基线 = 失败 node-id 集合；两个既有失败不计） | FR-010 | EP-001 |

## Success Criteria

- **SC-001**: owner 文档、两侧宪法、两侧指令面、agent 条款五处同时存在且以指针互引（契约测试）。 **Path**: final
- **SC-002**: 五问顺序在 checkpoint 协议中明确为「规则优先」，并有契约测试钉住。（clarify C-4 收紧判据：协议侧已满足——Q1 即规则；「钉住」不得以任意 `Q1` 字面命中或「三值判定存在」代为满足，必须在同一测试内同时断言 Q1 问的是规则**且**判定/动作先于目标；落地归属见 FR-010 与 C-4。） **Path**: final
- **SC-003**: 双落地计数与 watchlist 同批移动；`test_constitution_double_landing` 与 `test_fast_fail_discipline` 对冻结基线**零新增失败**（基线按失败 node-id 集合比较；两个既有失败 `test_i11…` 与 `test_g9…` 不在本特性判据内）。 **Path**: final
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

---

## Non-Disposable (092) — merged

**Source**: `.specify/specs/092-non-disposable/requirements.md`（092 线，原文保留，不删除）。
**Merge rule**: 本次合并为**机械搬运**，不是重写。092 的 **65 条 FR** 与 **20 条 SC** 逐条原样进入本节，
编号保持 092 原号并加 `ND-` 前缀（`ND-FR-001`…`ND-FR-065`、`ND-SC-001`…`ND-SC-020`），以免与本文件
既有的 `FR-001`…`FR-010` 冲突。**本节内**所有对 092 内部编号的引用（含 § Runtime Stack 表的 `FR` 列、
A–H 映射表、Measurement Sources）同样加 `ND-` 前缀，故本节内不存在指向 090 编号的歧义引用。
A–H 映射表与 Measurement Sources 两节按 092 原文一并搬运，未做内容改写。
092 的正文标题在本节内逐级降级以保持嵌套：`### Functional Requirements` → `####`，其下十个分组小标题
（`### 处置词汇共存与映射` 等，092 原文的 `####`）→ `#####`，`## Success Criteria *(mandatory)*` → `###`，
其下 `### Measurable Outcomes` / `### Measurement Sources` → `####`。这样全部 `##` 章节仍属于 090，
且本节内标题锚点不与 090 既有同名标题（如 § Measurement Sources）重名。

#### Functional Requirements

##### Non-Disposable 的机制层（US2/US1）

- **ND-FR-001**: 框架 MUST 提供 Non-Disposable 的**唯一 owner 文档** `shared/definitions/non-disposable-definitions.md`（本仓运行时投影 `.specify/shared/definitions/non-disposable-definitions.md`），文件头部 MUST 声明它拥有的条目：理念定义、封闭处置集与豁免形态、检测类别的封闭集、回顾面定义、取代协议、重编号判据、报告 schema、与历史存储的边界。
- **ND-FR-002**: 一个状态 MUST 被判为「过期 / 无用 / 延期」，当且仅当它满足 owner 文档中的可判定判据；判据 MUST 是有限项并可被程序或带引用的语义判定复算，MUST NOT 以「作者认为」或「读者感觉」为判据。
- **ND-FR-003**: 三类状态 MUST 各自有**可观察定义**、**判定主体**与**不可判定时的降级形态**，三者都由 owner 文档封闭声明；MUST NOT 只写类别名而不写这三项（「过期 / 无用 / 延期」是可判定状态的名称，不是形容词）。可观察定义 MUST 落到可判定的读物上：过期 = 载体与当前事实不符（其引用 / 计数 / 状态字段与树不符）；无用 = 载体对当前任何消费者都无输入作用（无入向引用、不在任何注册表或索引、不被任何引擎读取）；延期 = 载体上存在一处**未附到期条件**的留存声明。
- **ND-FR-004**: 判定主体 MUST 从封闭的 `{deterministic, semantic}` 两值中取一（术语与 sanitize 的 `DETECTIONS` 同名同义，按指针引用，不另造词）：断言对象为文件 / 行 / 字段 / 字面量 / 计数 / 路径 / 可解析引用 → `deterministic`，由只读检出引擎判定；断言只有在理解了自然语言断言的含义之后才成立（谁在语义上取代了谁、两处独立陈述是否说同一件事）→ `semantic`，由 subagent 判定且 MUST 携带两处路径 + 行号。MUST NOT 由语义判定产生一个自称确定性的条目。
- **ND-FR-005**: 不可判定 MUST 有降级形态且 MUST NOT 降级为「干净」：`deterministic` 类输入缺失、不可解析或引擎读取失败 → 该条目落 `unevaluated`；`semantic` 类 subagent 返回缺失或不合规 → 该片落 `unevaluated`（与「未评估」同一形态）。`unevaluated` MUST 在报告中可见并计入「未闭合」，MUST NOT 被计为「无检出」。
- **ND-FR-006**: `exempt` 的**到期条件类型封闭为三值**：`on-date`（绝对日期 `YYYY-MM-DD`）/ `on-condition`（具名可判定谓词 + 其判据指针）/ `on-review`（绝对日期，强制复查时点）。`exempt` MUST 同时携带 `reason`、`expiry_kind`（三值之一）、`expiry_value`、`expiry_recheck`（**绝对日期**，其距复核日的上限由 owner 文档给出）。MUST NOT 存在无到期形态；MUST NOT 存在恒真的到期条件（如 `condition: true`）——`on-condition` 的谓词 MUST 被一次**引擎求值**消费，不可求值即 `unevaluated`，MUST NOT 默认为「仍有效」。
- **ND-FR-007**: `exempt` MUST 同时携带**理由**与**到期条件或复核时点**，缺任一即处置不成立；到期条件不再成立时该条目 MUST 重新成为未处置条目。MUST NOT 存在「永久豁免」形态。
- **ND-FR-008**: 每一条被判定的状态 MUST 落入**封闭处置集**之一：`archive`（移入归档并留指针）/ `supersede`（由新载体承担，旧载体标记被取代并指向新载体）/ `correct`（就地修正）/ `exempt`（显式豁免）。集合 MUST 只在 owner 文档中定义，其它位置引用它。
- **ND-FR-009**: 「留在原处不做任何事」MUST NOT 表示为一个处置值，也 MUST NOT 被默认为闭合；未声明处置的条目 MUST 被检出并以非零退出码报出。
- **ND-FR-010**: 框架 MUST 提供一个**只读、确定性**的检出引擎，覆盖可判定的检测类别（文档结构/引用/计数/状态字段/路径拼写/常量重复/重编号活绑定），输出人读与机器可读两种形态，退出码 MUST 区分「无检出」「存在检出」「参数或环境错误」三类。
- **ND-FR-011**: 检出引擎 MUST 输出一次**覆盖声明**：扫描根集合、候选计数、被排除项及其理由；「什么都没扫到于是全绿」MUST NOT 出现——空候选与全绿 MUST 是不同结论。**空候选集的唯一读法**由 `contracts/detection-engine-cli.contract.md` C-603 定死：退出码 `2`（环境/声明缺陷）并点名声明路径，既不是 `0` 也不是 `1`；本条不复述该码，只要求「不被读成全绿」。

##### 处置词汇共存与映射（US2；clarify D-1）

- **ND-FR-012**: 本特性处置集与既有材料卫生处置集（`sanitize-utils.py` 的 `DISPOSITIONS`，owner 为 Feature 047 `045-sanitize-command` 的契约）MUST 是**两个各自封闭、互不合并的集合**；两集之间的全部允许关系 MUST 由 owner 文档中的**两张封闭映射表**声明——(i) **逐值映射表**（每一对 `(ND 处置, sanitize 处置)` 的对应关系，允许一对多与多对一），(ii) **不可映射项表**（某个处置值在另一集中**没有**对应项时的规定归宿）。MUST NOT 存在「一个值既不在逐值映射表也不在不可映射项表」的第三态；MUST NOT 在任一引擎里就地追加映射条目而不改 owner 文档。
- **ND-FR-013**: 当一次**具体**的检出同时被两个引擎视为自己的候选对象时，处置 MUST 按一条**单一、确定性的裁决规则**决定归属（「检出来源引擎决定处置词汇」：材料卫生引擎报告的候选只走 sanitize 处置集，Non-Disposable 引擎报告的只走本特性处置集），**同一候选 MUST NOT 被两个引擎各处置一次**；该规则 MUST 只在 owner 文档写一次，两个引擎 MUST 引用它，MUST NOT 各自实现一套优先级表。
- **ND-FR-014**: 由于存在**不可映射项**，owner 文档 MUST 为其逐个声明**承接面**，并 MUST 显式声明两条禁止：`exempt` 在材料卫生集中**不存在**（材料卫生类候选必须处置，不得豁免）；`dismiss` MUST NOT 被读作「延期处置」（其语义是「判定为不需要处置」），故不可映射到 `exempt`。

##### 取代协议（US4）

- **ND-FR-015**: 当一个特性取代另一个特性的正文、守卫或证据路径时，取代方 MUST 回收被取代方的**三类落点**：正文（标记被取代 + 指向新载体）、守卫（旧行为的守护断言被替换或被删除）、证据路径（旧拼写留有指针，不保留第二份真相）。
- **ND-FR-016**: 回收不完整 MUST 可被机械检出：一条被标记为被取代的正文，若其守卫仍要求旧行为、或其证据路径存在第二种拼写、或缺「指向新载体」的指针，检查 MUST 报红并点名路径与行号。
- **ND-FR-017**: 取代 MUST 被记录在 owner 文档规定的登记形态中（被取代项 → 取代项 → 处置 → 证据路径），且登记 MUST 可被检出引擎读取；MUST NOT 只存在于 commit message 或会话记录里。

##### 单 owner 登记（US5）

- **ND-FR-018**: 一个事实（含义、规则、阈值、枚举、配置值、计数）MUST 只有一处定义（owner），其余位置 MUST 为指针（引用 owner 路径与具名条目），MUST NOT 各自复写。
- **ND-FR-019**: 多 owner MUST 可被机械检出，判据 MUST 落在可判定读物上（同一名字/常量在给定轴上下文中被独立赋值或独立陈述），MUST NOT 依赖「两份文本读起来像不像」的人工判断。
- **ND-FR-020**: 检出 MUST 区分**内容重复**（第二份定义，MUST 报红）与**合法重复**（机器再生成的副本、测试内 pin 的字面量、带日期的记录），后者 MUST 由 owner 文档点名的封闭清单定义，不是自由裁量。
- **ND-FR-021**: 指针 MUST 可解析：指向的 owner 路径不存在或指向的具名条目不存在时，检查 MUST 报红并点名悬空指针。

##### 重编号协议（US6）

- **ND-FR-022**: **活绑定**（权威文件中的特性号、任务清单头部的需求号/特性号、团队目录名与 slug、契约头部声明的特性号、特性引用文件的行、注册表行）MUST 跟随目录的实际编号；出现不一致 MUST 被检出并点名文件与行号。
- **ND-FR-023**: **历史记录**（`test-evidence/`、日期化回顾报告、`## Clarifications` 中的既往文字、`.specify/state/` 的既往记录）MUST NOT 被改写以迁就新编号；对它们的改写 MUST 被检出。
- **ND-FR-024**: 活绑定与历史记录的**判据面** MUST 在 owner 文档中封闭列举（按路径与按章节位置），MUST NOT 由「看起来像历史」推断。判据面的两腿归属见 `contracts/renumber-and-supersede.contract.md` C-505：路径腿取自 `renumber-utils.py` 的既有谓词，章节腿（`## Clarifications`）由 Markdown 章节定位扫描承担——路径谓词对该形态结构性不可达，故该腿的判据所有者是本特性。

##### 状态与验证的机器可读契约（US7）

- **ND-FR-025**: 一个特性的 `verification.md` MUST 携带机器可读的逐条判据状态与 smoke 字段，字段名与取值域由既有 owner（`shared/workflow/acceptance-hardening.md` § Verification Vocabulary）拥有，本特性 MUST 引用而不复写。
- **ND-FR-026**: 注册表状态与闭环裁决 MUST 一致；宣称 `Implemented` / `Ready for Review` 而闭环裁决为 `block` MUST 被检出为矛盾状态并点名该特性（复用既有 reason code `status-claims-implemented-but-blocked`）。
- **ND-FR-027**: 一份声称含闭集恒等式（如 `applicable + exempt == candidates`）的验证记录，当恒等式两侧读数不成立时 MUST 被检出并给出两侧读数；MUST NOT 存在「声明了闭集却无人复算」的验证条目。
- **ND-FR-028**: 状态一致性检查 MUST 复用既有闭环引擎的裁决与 reason code 词表，MUST NOT 在检出引擎中重建第二套裁决逻辑或第二套 reason 词表。

##### 命令执行形态：回顾 → 设计 → 确认 → 执行（US1/US3）

- **ND-FR-029**: `/speckit.history` 的执行形态 MUST 是四段：**回顾 → 设计（方案）→ 用户确认 → 执行**。回顾与方案段 MUST 零写盘；执行段 MUST 只在用户确认之后发生。
- **ND-FR-030**: 回顾面 MUST 恰为当前 HEAD 工作树中 `.specify/{archive,derive,goal,history,memory,project,review,specs,state,teams}` 十个目录下的文件；MUST NOT 读取 git 历史（commit / blame / 旧版本 diff）作为回顾输入；MUST NOT 以「git 历史里也有」作为条目来源。
- **ND-FR-031**: **零写盘的验证方式 MUST 是工作树状态的逐字节比较**，不是命令自己的一句声明：回顾段开始前与方案段结束后各取一次快照（`git status --porcelain=v1` 全文 + 受管路径集合的内容哈希），两次快照 MUST 逐字节相同；报告与方案在**未确认**状态下 MUST NOT 落盘到任何被追踪路径。若实现需要落盘一份方案以承载确认，该落点 MUST 位于 `.gitignore` 已匹配的临时根（`.specify/.tmp/`）且 MUST 由执行段清理。
- **ND-FR-032**: **确认粒度封闭为三值**：`group`（按检测类别分组确认，一次确认覆盖该组全部条目）/ `item`（逐条确认）/ `none-of`（全部提出但只确认被点名者）；未提供时 MUST 取 `group`。MUST NOT 存在第四种粒度，MUST NOT 存在「一次确认 = 全部执行」——全量执行只能由用户逐组或逐条确认构成。
- **ND-FR-033**: **部分确认后的未确认项 MUST 在报告中以 `unconfirmed` 状态可见**（既不是「尚未给方案」，也不是任何处置值），MUST NOT 被静默丢弃、MUST NOT 在下一轮被自动重试、MUST NOT 计入「本轮已闭合」。
- **ND-FR-034**: **执行段 MUST 逐组可逆或明示不可逆**：(i) `correct` 与 `supersede` 的标记类改动 MUST 可经一次 `git checkout -- <path>` 回退（只改被确认的既有文件内容）；(ii) `archive` 终为**移动**（`git mv` 语义），其可逆性 MUST 以「源路径 → 归档路径」的显式映射记录在处置记录中；(iii) 执行段 MUST 按**分组边界**落盘并在每组结束时记录一次证据，使中断停在组边界而非条目中间；(iv) 删除 MUST NOT 出现在任何处置中（`archive-not-delete`，与「修复 lane MUST 保持历史证据不被删除」同一义务）。
- **ND-FR-035**: **执行段证据的落点 MUST 是单一通道**：`.specify/specs/<spec-dir>/test-evidence/`（本特性即 `.specify/specs/092-non-disposable/test-evidence/`）下**一次运行一个文件**；证据 MUST 含四段：前后两次检出读数、被改动路径清单、语料条目编号、处置类别。MUST NOT 把处置结论写进 `.specify/memory/sanitize/findings.json` 或 `.specify/history/`，MUST NOT 新建第二个证据存储。
- **ND-FR-036**: 回顾 MUST NOT 扩大或缩小到该十目录之外；范围 MUST 由一份声明式的根集合定义（与既有事实声明层同构），MUST NOT 由散落在提示文本里的目录名清单决定。
- **ND-FR-037**: 该声明 MUST 是 `shared/declarations/facts/` 下的一个**事实声明文件**（本仓投影 `.specify/shared/declarations/facts/`），其 `kind` MUST 取自 `shared/declarations/contract.yaml` 的封闭 `fact_kinds`（不新增 kind），MUST 携带该契约要求的全部 `required_fact_keys`，且 MUST 经**唯一读入口**（`scripts/python/declaration_reader.py`）读取。MUST NOT 在检出引擎里内联一份目录字面量清单，MUST NOT 在命令模板或技能里再写一份。
- **ND-FR-038**: 根集合的**计数** MUST 与该声明同处声明一次（当前为 10）；任何把该数字写成字面量的位置 MUST 按指针引用该声明。增删目录 MUST 只改该声明一处。
- **ND-FR-039**: 声明读失败 MUST NOT 静默降级：声明文件缺失 → 检出引擎以退出码 `2` 报环境 / 参数错误并点名缺失路径（**不是**「零候选于是全绿」）；声明存在但其 `kind` 或必填键不合规 → 同样退出码 `2` 并点名违规键；降级读取的标签沿用既有 `STR-014`，MUST NOT 另造一套。
- **ND-FR-040**: **目录缺失**（声明中列出但树上不存在）MUST 被逐目录区分并报出，且 MUST NOT 导致整体失败：以「声明存在、树中缺失」的形式进入覆盖声明并从候选计数中显式排除（附理由），MUST NOT 被计入「0 文件」从而与「目录存在但为空」混同。
- **ND-FR-041**: **未登记目录** MUST 被报告为一次覆盖提示并停止扩围；MUST NOT 因「看起来像历史目录」而被自动纳入——范围只由声明决定，不由启发式决定。
  判据 MUST 是程序可读的三条，全部依赖**已声明根集合** `S`（`shared/declarations/facts/non-disposable-review-surface.yaml` 的十个路径）而**不依赖任何形态推断**：
  (i) **声明但缺失**：`p ∈ S` 且该目录在本树不存在 → 缺失根读数（点名 `p`）；
  (ii) **存在但未声明**：`.specify/` 下某个一级目录名 `d ∉ S` → 报告一次（不点名「像什么」）；
  (iii) **声明后新增的同层目录**：`d` 在两次运行之间出现且 `d ∉ S` → 与 (ii) 同一条读数，不另立类别。
  原文的「名字落在十目录形态内」是循环判据（用待判定的形态去定义判据），此处删除；「不扩围」的落实是：**未声明目录的子树不被扫描**，其条目数为 `0` 且以「未声明」为理由记在覆盖声明里，绝不静默计入 `candidates`。
- **ND-FR-042**: 方案段 MUST 逐条给出拟处置、影响路径、可逆性，并以一次确认请求结束该段；确认 MUST 支持部分确认（按分组或按条目），未确认项 MUST 保持未处置并可见。
- **ND-FR-043**: 命令的既有能力（把当前工具的会话历史蒸馏为主题聚合知识库、增量 manifest）MUST 保留为回顾/执行面的一部分，MUST NOT 被移除或另立第二个入口。
- **ND-FR-044**: 命令 MUST NOT 新建第二套历史存储；蒸馏产物仍归 `.specify/history/` 所有，本特性只**读取**它作为回顾输入之一，并新增「回顾/方案/处置」三段产物。
- **ND-FR-045**: `/speckit.history` MUST NOT 成为「批量改写他人已交付正文」的旁路：任何对既有 spec 正文、owner 文档或守卫的改动 MUST 属于用户确认的方案条目，并 MUST 留下前后读数证据。

##### team / 大并发编排义务（US8）

- **ND-FR-046**: 回顾的语义判定面 MUST 由 team 的大并发 subagent 承担；编排 MUST 复用既有 `085` 的 spec-local Temporary Goal/Team 与既有并发机制，MUST NOT 新建第二套 team/并发/调度设施。
- **ND-FR-047**: 每个 subagent MUST 只读其被分配的片，MUST 返回 owner 文档定义的固定字段集的结构化条目；分配 MUST 互不重叠且并集覆盖候选集合。
- **ND-FR-048**: subagent 返回不合规时，该片 MUST 被标记为「未评估」并在报告中可见；MUST NOT 被计为「无检出」（未评估不等于干净）。
- **ND-FR-049**: 回顾结果 MUST 与并发度无关：同一棵树上不同并发度 MUST 得到按名相同的条目集合。

##### 修复 lane（US9）

- **ND-FR-050**: 「大并发」MUST 只在既有机制内表达：所需并发度取状态脊声明的 `agent_concurrency_requested`（本线为 24），有效值按既有声明计算（`min(requested, host capacity, stage max_parallel, ready packages + verifier reserve, resource capacity)`），降级 MUST 带具名理由并记录，MUST NOT 静默。MUST NOT 新增第二个调度器、第二个并发上限常量或第二套派发协议。
- **ND-FR-051**: 回顾 / 修复 lane 的 team MUST 是 `085` 的 spec-local Temporary Team（本线 slug `092-non-disposable`），且 MUST 遵守其创建时机：MUST 在 `clarify` 与 `plan` **两者都**通过 U4 之后才创建；MUST NOT 在 clarify 阶段或 plan U4 之前预建 team 目录。
- **ND-FR-052**: 执行段 MUST 是一个**修复 lane**：按用户确认的方案逐条处置，MUST NOT 是「一次性清理脚本」——处置动作只经由 owner 文档定义的处置途径执行，MUST NOT 引入一条独立的批量删除/批量改写通道。
- **ND-FR-053**: 修复 lane MUST 优先消费 `notes/input-review-080-090.md` 的 A–H 八组语料，且每一条语料 MUST 在规格内显式映射为一条 FR/SC 或一条带理由的排除；MUST NOT 存在未映射条目。
- **ND-FR-054**: 每一次修复 MUST 留下可复核证据：修复前后两次检出读数、被改动路径清单、对应语料条目编号、以及该改动的处置类别；缺任一项该修复 MUST 被判为不成立。
- **ND-FR-055**: 修复 lane 结束后，被处置类别的检出集合 MUST 按名为空，或仅剩已登记豁免及其到期条件；MUST NOT 以「已被人工看过」作为归零依据。
- **ND-FR-056**: A–H 八组条目的处置归属 MUST 按**类别判据**（不是逐条心情）分流为封闭两档，且该判据 MUST 写进 A–H 映射表：
  - **档 I（本特性交付，含首轮修复）**：缺陷形态是**跨特性、对全树成立的机制缺失**——检不出、无处置词汇、无判据面、无四段形态、无并发承载、无 owner 指针、两处字面量真冲突且无 owner。本特性 MUST 交付机器 + 首轮修复；修复后该条 MUST 可被本特性检出复现并归零。
  - **档 II（移交对应特性线）**：缺陷形态是**某一条既有特性的正文陈述错误**（数字、结论、措辞与树不符），且修复它的正确位置就是那条特性的正文。本特性 MUST 交付**检出能力 + 一条 shift 清单**（语料编号 → 承接特性 → 应当改哪个文件），并在该正文文件留下一条可复核的移交标记；MUST NOT 在本特性的实现里直接改写该正文，MUST NOT 把它计入本特性的「归零」。
  - 两档都有**上报义务**：档 II 项 MUST 在 A–H 映射表或 Open Items 中可见，MUST NOT 因移交而消失。
- **ND-FR-057**: 下列归属已由 clarify 裁定为**默认分配**；plan 阶段 MUST 逐条落表并给出可复核行号，若某条被实测证明不属于该档，MUST 以一次显式改判记录，MUST NOT 静默挪档：A → 档 I（补齐机器可读块与状态对账，属记录补充而非改写结论）；B → 档 I（正文回收，正是取代协议的首次真实使用）；C → 档 I（活绑定跟随新编号）；D → 档 II（081 / 084 / 088 / 090 各自正文）；E → 档 II（083 / 089 / 084 正文）；F → 档 I（无 owner 的重复常量建 owner + 指针）与档 II（历史正文里的陈旧复制）；G → 档 I（守卫回收）；H → 档 II（086 / 082 / 085 正文），`.specify/.tmp/086-*` 登记为**排除**（正当历史）。
- **ND-FR-058**: 修复 lane MUST 保持历史证据不被删除：归档而非删除（`archive-not-delete`），被取代正文保留其旧文本并加被取代标记。

##### 落点与复用（A1–A3 裁定、A20；clarify 改判见 D-2）

- **ND-FR-059**: 本特性的机制 MUST 复用既有面：历史蒸馏入口 `manage-history`、材料卫生引擎 `sanitize-utils.py`、闭环裁决 `closure-acceptance-check.py`、特性注册表 reconcile、并发 team 机制；MUST NOT 建造第二套 history 入口或第二套存储。
- **ND-FR-060**: `sanitize-utils.py` 的 `CATEGORIES` / `DISPOSITIONS` / `STATES` / `DETECTIONS` **MUST NOT 被本特性修改**：它们是 Feature 047 已交付的封闭集，改动会证伪其契约与台账。本特性对它们的义务只有两条——按其契约**引用**，以及在 owner 文档里写清「处置映射」一节的两张表与裁决规则。本特性新增的检出类别 MUST **只**登记在自己的 owner 文档里，MUST NOT 追加进 `CATEGORIES`。
- **ND-FR-061**: 检出引擎的确定性部分 MUST 落在 `scripts/python/` 下的新增只读单文件引擎（与 `sanitize-utils.py` / `closure-acceptance-check.py` 同形态：argparse、只读、退出码 0/1/2、stdout 人读 + `--json` 机器读），并由既有镜像机制生成 `.specify/scripts/python/` 投影。
- **ND-FR-062**: 本特性的验证守卫 MUST 落在既有 `pytest -m contract` 集合内（新增契约测试文件），MUST NOT 新增独立的确认门或独立门禁步骤。
- **ND-FR-063**: Non-Disposable 的落点 MUST 是**下列七面同批落地**，且 owner 唯一（ND-FR-001 的 `shared/definitions/non-disposable-definitions.md`，本仓投影 `.specify/shared/definitions/`）——**本特性 MUST NOT 新增宪法原则，MUST NOT 改动宪法模板与本仓宪法的原则名单**：
  1. **owner 文档**（新）：理念定义、封闭处置集与豁免形态、检测类别封闭集、三类状态的可观察定义与判定主体、回顾面定义、取代协议、重编号判据面、报告 schema、与历史存储 / sanitize 的边界（含「处置映射」一节的两张映射表与裁决规则）。
  2. **声明层**（新）：`shared/declarations/facts/` 下的回顾面根集合声明（`kind: closed-set`），经 `declaration_reader.py` 读取；若另需机器事实同样落该目录，MUST NOT 新造第四个声明目录。
  3. **术语表**（本仓 `.specify/memory/glossary.md`）：四条术语条目——`Non-Disposable` / `Disposition（处置）` / `Review Surface（回顾面）` / `Exemption（豁免）`；每条指向 owner 文档，MUST NOT 复写其判据。
  4. **特性注册表**（`.specify/memory/features.md` + `.specify/memory/features/092.md`）：本特性行与详情文件同步登记，含「与宪法 XI『机制修复』子条的边界」一行。
  5. **既有守卫**（零新增门禁步骤）：本特性的契约测试断言「owner 文档存在且非空、声明文件可被唯一读入口读出、术语表四条存在、三份历史面指针存在、`sanitize-utils.py` 的四个封闭集逐字未变」；两条宪法计数 pin（`test_constitution_double_landing.py` 的 template / live / mandate 三计数与 watchlist、`test_fast_fail_discipline.py` 的同批 pin）MUST **保持原值**。
  6. **三份历史面指针**（只在既有章节追加一行指针，不改其正文）：`templates/instructions-template.md` 与 `.specify/instructions.md` 各一行指向 owner 文档的常驻指针、`AGENTS.md`（经 `/speckit.instructions` 生成，随之流动）、`skills/internal/manage-history/SKILL.md` 的回顾段指针。MUST NOT 新增常驻顶级 `##` 章节——否则两条指令面计数 pin（模板 35 / 现网 36）抖动。
  7. **决定台账**：`.specify/memory/register.md` 一条指向 owner 文档的条目；决定的记录形态归本次 clarify 会话条目，MUST NOT 在 requirements 之外再写第二份决定正文。
- **ND-FR-064**: ND-FR-063 的**连带义务**（由 clarify 显式认领，MUST NOT 留作隐含）：(i) 新增文件 MUST 在目录治理的既有登记处可见（`shared/definitions/framework-map.md` 或声明层的既有登记）；(ii) 落地点 5 的契约测试 MUST 在**被守物损坏时变红**，即至少一条变异腿；(iii) `AGENTS.md` 的指针 MUST 只经 `/speckit.instructions` 生成，MUST NOT 手改；(iv) owner 文档 MUST 留一节「与宪法的关系」，写明本次**未**新增原则及其理由，否则下一位读者会把「理念没有原则」读成遗漏。
- **ND-FR-065**: 若用户日后裁定**补一条宪法原则**（OI-4），届时 MUST 按宪法既有五处落点 + 三计数 pin + Sync Impact Report 的完整流程作为一次独立的 MINOR 修订执行；本特性的 FR/SC MUST NOT 预写其条号或 pin 数值。

### Key Entities *(include if data involved)*

- **Non-Disposable 状态（Non-Disposable State）**：一个被判定为「过期 / 无用 / 延期」的载体或其局部；属性为位置（文件:行）、检测类别、检测主体（`deterministic` / `semantic`）、证据引用、严重度、条目状态（`open` / `unevaluated` / `unconfirmed` / `disposed`）、处置、处置证据路径、到期条件（仅 `exempt`：`expiry_kind` ∈ `on-date` / `on-condition` / `on-review`，加 `expiry_value` 与 `expiry_recheck`）。
- **处置（Disposition）**：封闭集 `archive` / `supersede` / `correct` / `exempt` 的成员；它是「状态已闭合」的唯一凭据，缺它则该状态仍然开着。它与材料卫生处置集的关系（两张映射表 + 一条裁决规则）由 owner 文档拥有，不由本清单拥有。
- **处置映射（Disposition Bridge）**：owner 文档「处置映射」一节的两张封闭表——逐值映射表与不可映射项表——加上一条「检出来源引擎决定处置词汇」的裁决规则；它使两套封闭集**共存而不合并**。
- **检出类别（Detection Category）**：封闭集，至少含 `superseded-live`（被取代仍活）、`multi-owner`（多 owner）、`renumber-live-binding`（重编号活绑定残留）、`status-unreadable`（状态不可读）、`false-closed-set`（闭集恒等式不成立）、`stale-constant`（常量/计数漂移）、`orphan-path`（路径拼写残留/不存在路径）、`deferral-marker`（延期措辞与无到期条件的留存）。成员集只在 owner 文档中定义。
- **回顾面（Review Surface）**：十个 `.specify/` 历史目录的声明式根集合（载体：`shared/declarations/facts/` 下的根集合声明）；它是回顾的唯一输入范围，且不含 git 历史。目录缺失 → 覆盖声明里显式排除；目录未登记 → 只报提示，不扩围。
- **Non-Disposable 报告（NDR）**：回顾的产物；含条目列表、覆盖声明、按类别的计数、未评估片标记；机器可读形态承载核对与闭合判定。
- **修复 lane 证据（Repair Evidence）**：一次处置的前后读数、改动路径、语料编号与处置类别；它是「修复成立」的判据。
- **A–H 映射表（Corpus Mapping）**：`notes/input-review-080-090.md` 八组条目到 FR/SC 或排除理由的显式映射。

#### Runtime Stack & Dependency Ownership

本特性不新增运行时依赖：检出引擎、状态一致性与历史蒸馏消费的都是既有框架已声明的解释器与既有引擎；并发面复用既有 team 机制。`Premises` 指向 plan 阶段将定义的执行前提（同 `090` 的 EP 惯例）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|----|----------|
| RS-001 | Python 3 解释器（运行检出引擎、状态一致性与既有镜像/闭环引擎） | signed-contract | CPython 上游（本仓只消费） | `requires-python = ">=3.8"`（`pyproject.toml` 既有声明；本特性零新增第三方依赖） | `pyproject.toml` | 新增检出引擎与契约测试在 `>=3.8` 解释器上通过；本特性零新增 import | ND-FR-006, ND-FR-039 | EP-001 |
| RS-002 | pytest 契约测试运行器（承载 ND-FR-040 的守卫） | signed-contract | pytest 上游（本仓只消费） | 以 closure 比较时刻实测 `python3 -m pytest --version` 为准（`090` 记录 2026-11-09 为 `pytest 9.0.3`） | `scripts/bash/run-tests.sh` | `pytest -m contract` 在冻结基线上零新增失败（基线 = 失败 node-id 集合） | ND-FR-040 | EP-001 |
| RS-003 | 既有闭环裁决引擎（`closure-acceptance-check.py` 的 verdict 与 reason code 词表） | signed-contract | 既有 owner `shared/workflow/acceptance-hardening.md` § Closure Verdict | 以该引擎的退出码与 `--json` 输出为读数 | `shared/workflow/acceptance-hardening.md` | 状态一致性检查在 `Implemented` 但对 `block` 的副本树上判红，在两者一致时判绿 | ND-FR-019, ND-FR-021 | EP-002 |
| RS-004 | 既有材料卫生引擎（`sanitize-utils.py` 的类别/处置/台账词汇） | signed-contract | 既有 owner（Feature 047 契约 `045-sanitize-command`） | 其 `CATEGORIES` / `DISPOSITIONS` / `STATES` 字面为其自身 owner，本特性按指针引用 | `.specify/specs/045-sanitize-command/contracts/sanitize-findings.md` | 本特性处置词汇与 sanitize 台账的一致性由一次联合比对取证（相同写作不同写作 MUST 被阐明） | ND-FR-038 | EP-003 |
| RS-005 | 既有 spec-local Temporary Goal/Team 与多 agent 并发机制 | signed-contract | 既有 owner（Feature 085 契约） | 以 `085` 契约的 roster/并发上限声明为读数 | `.specify/specs/085-sdd-temporary-goal-team/contracts/concurrency-and-worktrees.md` | 一次分片回顾的派发数 ≤ 声明的并发上限，分区并集覆盖候选集合 | ND-FR-029, ND-FR-030 | EP-004 |
| RS-006 | 检出引擎（本特性交付的只读确定性能力） | in-scope | 本特性 | — | 本特性 `contracts/`（plan 阶段定义） | 检出引擎在 A–H 语料树上复现各检测类别的发现 | ND-FR-006, ND-FR-008 | EP-001 |
| RS-007 | 回顾→方案→确认→执行 的命令形态（`/speckit.history` 新执行段） | in-scope | 本特性 | — | 本特性 `contracts/`（plan 阶段定义） | 回顾段与方案段零写盘、未确认不执行，由契约测试取证 | ND-FR-022, ND-FR-025 | EP-001 |

### Success Criteria *(mandatory)*

#### Measurable Outcomes

- **ND-SC-001**: 在 `notes/input-review-080-090.md` 的 A–H 语料树上，检出引擎对每一组的发现**可被复现**：A–H 映射表 100% 条目有对应检出或显式排除理由，逐组给出检出读数（条目数、类别、路径）。 **Path**: final
- **ND-SC-002**: 回顾面恰为十个 `.specify/` 历史目录，且回顾不消费 git 历史：注入只在 git 历史中存在的旧措辞后，条目集合按名不变；目录之一缺失时报点名该目录且不静默跳过。 **Path**: final
- **ND-SC-003**: 任一条目若处置为空、或 `exempt` 缺理由缺到期条件，校验以非零退出码报红并点名该条目；四条合法处置（含带到期条件的 `exempt`）全部转绿；「原样保留」不被接受为处置值。 **Path**: final
- **ND-SC-004**: 回顾段与方案段零写盘：在一次有未处置条目的运行中，回顾与方案结束后的 `git status --porcelain` 为空；用户未确认时执行段不发生；用户确认后才发生写盘。 **Path**: final
- **ND-SC-005**: 取代回收可被机械证伪：把一条契约改为与既有守卫相反的要求（未回收的取代）后检查报红并同时点名正文与守卫；同步回收后转绿；三种落点（正文/守卫/证据路径）各有至少一次变异腿。 **Path**: final
- **ND-SC-006**: 多 owner 可被机械检出：注入同一常量的第二个独立定义后检查报红并点名两处与两个值；改成指针后转绿；指针悬空时报红并点名目标。 **Path**: final
- **ND-SC-007**: 重编号协议双向可判：活绑定残留（任务头部/契约头部/团队 slug/特性引用）各报红并点名行号；历史记录中的旧编号不报红；被改写的判据面内历史记录报红。 **Path**: final
- **ND-SC-008**: 状态矛盾被检出：注册表 `Implemented` 而闭环 `block` 时报 `status-claims-implemented-but-blocked`；`verification.md` 缺机器可读状态块或 smoke 字段时报红并点名缺失字段；闭集恒等式不成立时给出两侧读数。 **Path**: final
- **ND-SC-009**: 分片回顾的分区互不重叠且并集覆盖候选集合；不同并发度两次运行得到按名相同的条目集合；一个返回不合规的片被标为「未评估」且不计为干净。 **Path**: final
- **ND-SC-010**: 修复 lane 后重跑同一组检出：被处置类别按名归零或仅剩已登记豁免及其到期条件；每次修复的证据含前后读数、改动路径、语料编号与处置类别，缺任一即该修复不成立。 **Path**: final
- **ND-SC-011**: Non-Disposable 的七个落点同批落地并可被机械核对：owner 文档与声明文件存在且可经唯一读入口读出、术语表四条存在、三份历史面指针存在、`sanitize-utils.py` 的四个封闭集逐字未变、两条宪法计数 pin 保持原值、`register.md` 有对应条目；且这一组断言在破坏任一落点后变红。 **Path**: final
- **ND-SC-012**: 无第二个 history 入口、无第二套历史存储、无第二套并发机制：一次结构检查证明 `manage-history` 仍是唯一蒸馏入口、`.specify/history/` 仍是唯一蒸馏存储、team 机制仍是唯一并发面。 **Path**: supporting
- **ND-SC-013**: 检出引擎与契约测试的既有行为零回归：`pytest -m contract` 与 `pytest -m integration` 相对冻结基线（失败 node-id 集合）零新增失败。 **Path**: supporting
- **ND-SC-014**: 十个历史目录在回顾范围内被完整覆盖：覆盖声明给出的候选计数与一次独立枚举的逐目录计数一致（clarify 实测基线 `4,352` 个文件；requirements 阶段读数为 `4,345`，两次测量时点不同；基线是参照物不是阈值）。 **Path**: supporting
- **ND-SC-015**: 两套处置词汇共存而可裁：owner 文档的两张封闭表覆盖四个 ND 处置值与五个 sanitize 处置值的**每一对**（无第三态），不可映射项有具名承接面，且「同一候选被两个引擎各处置一次」在一条变异腿上判红。 **Path**: final
- **ND-SC-016**: 三类状态的判定主体与降级形态可判：每条检出条目携带 `detection ∈ {deterministic, semantic}`；把一条 `deterministic` 输入造成不可解析后该条目落 `unevaluated`（不是「无检出」）；把一片 `semantic` 返回造成不合规后该片落 `unevaluated`；两次都仍在「未闭合」计数内。 **Path**: final
- **ND-SC-017**: 豁免不可静默续期：`exempt` 缺 `reason` / `expiry_kind` / `expiry_value` / `expiry_recheck` 任一即判红并点名缺失项；`expiry_kind=on-condition` 的谓词不可求值时报 `unevaluated` 而非「仍有效」；到期后该条目重新进入未处置集合且报告不自称闭合。 **Path**: final
- **ND-SC-018**: 声明式回顾面可判：声明文件存在且 `kind` / 必填键合规（经唯一读入口读出）；删除声明文件 → 检出引擎退出码 `2` 并点名缺失路径（不是零候选全绿）；移除一个目录 → 覆盖声明点名该目录并显式排除（与「存在但为空」可区分）；放一个未登记的兄弟目录 → 只报提示、不纳入候选。 **Path**: final
- **ND-SC-019**: 四段形态的确认语义可判：零写盘（回顾前 / 方案后两次快照逐字节相同）、三种确认粒度各有一条用例、部分确认后未确认项在报告中以 `unconfirmed` 可见且不计入闭合、执行段证据四段齐备并落在本特性 `test-evidence/`。 **Path**: final
- **ND-SC-020**: 大并发只在既有机制内表达且 A–H 移交边界可判：team 目录在 clarify / plan 双 U4 之前不存在、之后以其 slug 存在；有效并发度取既有声明公式且降级带理由；A–H 八组逐条落在档 I 或档 II，档 II 项在 shift 清单中可见并指向承接特性，且本特性的「归零」统计不含档 II 项。 **Path**: final

#### Measurement Sources & Collection Methods

- **ND-SC-001 Source**: 检出引擎对 A–H 语料树的逐组 `--json` 输出（类别、路径、行号、严重度）；A–H 映射表与其检出读数的对照表落盘 `test-evidence/`；每组至少一次运行记录命令、退出码与命中行。
- **ND-SC-002 Source**: 两次运行的条目集合差集（`comm -13` / `comm -23` 风格按名比较）：一次在原树、一次在注入了仅在 git 历史中存在的旧措辞的副本树；另一次在删除一个十目录之一的副本树上读点名行；两次读数落盘 `test-evidence/`。
- **ND-SC-003 Source**: 对副本树报告中处置字段的变异实验（留空 / `exempt` 缺理由 / `exempt` 缺到期条件 / 四种合法处置），逐次读校验退出码与点名行，落盘 `test-evidence/`。
- **ND-SC-004 Source**: 每次运行前后 `git status --porcelain` 与受管目录文件哈希快照；分别在回顾结束、方案结束、确认后三个时点各取一次快照，三次快照落盘并逐字比较。
- **ND-SC-005 Source**: 三条副本树变异腿（正文未标记被取代 / 守卫仍要求旧行为 / 证据路径出现第二种拼写），每条腿记录变异内容、检查退出码、点名行，落盘 `test-evidence/`。
- **ND-SC-006 Source**: 副本树中注入常量第二定义、改成指针、制造悬空指针三次变异前后的检查 `--json` 输出对比，落盘 `test-evidence/`。
- **ND-SC-007 Source**: 四类活绑定各一次变异 + 判据面内历史记录各一次变异（旧编号保留、被改写），读检查退出码与点名行，落盘 `test-evidence/`。
- **ND-SC-008 Source**: `closure-acceptance-check.py --json` 的 `verdict` / `reasons` 与注册表行的对照读数；`verification.md` 字段扫描的缺失字段清单；闭集恒等式两侧的实计数器读数；三者分开记录，MUST NOT 合并成一句「状态一致」。
- **ND-SC-009 Source**: 一次分片回顾的分区清单（片 → 路径集合）与候选集合的差集；两次不同并发度的条目集合差集；一片不合规注入后的「未评估」标记读数；落盘 `test-evidence/`。
- **ND-SC-010 Source**: 修复 lane 前后两次检出引擎的 `--json` 输出按名差集；每次修复的证据包（前后读数、改动路径清单 `git diff --name-only` 范围、语料编号、处置类别）落盘 `test-evidence/`。
- **ND-SC-011 Source**: 一次落点核对（七面逐面的存在性 + 内容断言，命令与读数落盘 `test-evidence/`）；取 `sanitize-utils.py` 四个封闭集字面与其 owner 契约逐字比对；两条宪法守卫的 pin 读数（MUST 与 clarify 前同值）；变异腿 = 删除 owner 文档 / 删除声明文件 / 向 `CATEGORIES` 追加一项，三次各自断言变红。
- **ND-SC-012 Source**: 一次结构检索的读数：`manage-history` 的入口唯一性、`.specify/history/` 作为唯一蒸馏存储、team 机制的唯一性；检索命令与命中清单落盘 `test-evidence/`。
- **ND-SC-013 Source**: `pytest -m contract` 与 `pytest -m integration` 的失败 node-id 集合，与冻结基线按名比较（`comm -13` / `comm -23` 两向），两向皆空即零新增失败；读数落盘 `test-evidence/`。
- **ND-SC-014 Source**: 覆盖声明的候选计数与一次独立枚举（逐目录 `find` / `rglob` 计数）的对照表；逐目录计数落盘 `test-evidence/`，基线计数注明测量时点（clarify 读数 `4,352`）。
- **ND-SC-015 Source**: owner 文档两张映射表的程序化核对——把 ND 四值与 sanitize 五值的**笛卡尔积**逐对查表，每一对 MUST 命中某一张表（读数为「未覆盖对 = 0」）；列出不可映射项的承接面清单；变异腿 = 让同一候选被两个引擎各产出一次（断言判红）。三份读数落盘 `test-evidence/`。
- **ND-SC-016 Source**: 报告 `--json` 中每条条目的 `detection` 字段分布；两次 `unevaluated` 注入前后的条目集合差集与「未闭合」计数（MUST 只增不减）；读数落盘 `test-evidence/`。
- **ND-SC-017 Source**: 对一份 `exempt` 记录的四个字段逐项置空的变异实验 + 一次 `on-condition` 不可求值 + 一次到期（把 `expiry_recheck` 设为过去日期），逐次读校验退出码与点名行；落盘 `test-evidence/`。
- **ND-SC-018 Source**: 四次副本树变异（删声明 / 移目录 / 增未登记目录 / 声明 `kind` 改为域外值）后的 `--json` 输出与退出码；落盘 `test-evidence/`。
- **ND-SC-019 Source**: 三次快照（回顾前 / 方案后 / 确认后）的 `git status --porcelain=v1` 与受管路径哈希；三种确认粒度各一次运行读数；`unconfirmed` 计数；执行段证据文件四段字段核对；落盘 `test-evidence/`。
- **ND-SC-020 Source**: `<spec-dir>/team/` 在 clarify / plan 双 U4 前后的两次 `ls` 读数；`team.md` 的 `config.agent_concurrency` 与状态脊 `agent_concurrency_requested` / `effective` 的对照；A–H 映射表的档列与 shift 清单行数；落盘 `test-evidence/`。
## Non-Disposable (092) — A–H Corpus Mapping *(合并搬运，随 `ND-FR` 编号)*

> 下表原样取自 092；表中 `承接 FR` / `承接 SC` 列已按本节规则加 `ND-` 前缀。
> 092 原文的 `档` 列说明文字引用 092 编号 `FR-036` / `FR-034`，在本节内分别对应 `ND-FR-036` / `ND-FR-034`。

| Group | 代表发现 | 检测类别 | 承接 ND-FR | 承接 ND-SC | 档 |
|-------|----------|----------|-----------|-----------|----|
| A 状态与裁决自相矛盾 | 089 注册 `Implemented` 而闭环 `block`；`verification.md` 无机器可读块；090 注册 `Planned` 而闭环 `accept`；080 无 `**Path**` 标记 | `status-unreadable` | ND-FR-018, ND-FR-019 | ND-SC-008 | I（补齐机器可读块、状态对账；不改其结论） |
| B 取代未回收 | 086 仍要求字节一致（089 已改投射）；085 契约四部分（owner 已五部分）；067 串行缺省未修订；088 证据路径陷阱与三种拼写 | `superseded-live`, `orphan-path` | ND-FR-007, ND-FR-009, ND-FR-010 | ND-SC-005 | I（首轮修复；088 按 OI-3 分流：文件存在 → `superseded-live`，不存在 → `orphan-path`） |
| C 重编号残留 | 089 绑定 `Feature ID: 086`、任务头部 086、T081 指向 086 的注册行、团队目录 `086-…`；088 八个契约写 `Feature: 087` | `renumber-live-binding` | ND-FR-015, ND-FR-016, ND-FR-017 | ND-SC-007 | I（活绑定跟随新编号；历史记录不动） |
| D 一事实多 owner | 081 状态机三 owner、reason set 两 owner；084 判据两处互斥；088 汇报周期 15 分钟 vs 30 秒；090「规则锚八成员」四种拼写 | `multi-owner` | ND-FR-011, ND-FR-012, ND-FR-013, ND-FR-014 | ND-SC-006 | II（逐条移交 081 / 084 / 088 / 090 正文；本特性交付检出） |
| E 闭集声明被测量证伪 | 083 范围自相矛盾与基线三值；083 声称宪法第一条原则实不存在；089 恒等式 `367+737≠751`；084 排除行 8 vs 38 | `false-closed-set` | ND-FR-020 | ND-SC-008 | II（083 / 089 / 084 正文修复；本特性交付恒等式复算检出） |
| F 常量与计数漂移 | 分解上限 40/60/80/30/120/160 六处；指令预算 37888 vs 38400；宪法 roster 陈旧计数；特性总数算术陈旧 | `stale-constant`, `multi-owner` | ND-FR-011, ND-FR-012, ND-FR-013 | ND-SC-006 | I（无 owner 的重复常量建 owner + 指针）与 II（历史正文的陈旧复制） |
| G 守卫有语义缺口 | 090 顺序守卫丢失位置比较；`first_no == "1"` 同义反复；`RULE_SET` 漏 ⑧ | `superseded-live`（守卫侧） | ND-FR-009 | ND-SC-005 | I（首轮修复 + 守卫回收检出） |
| H 路径与证据残留 | 086 写不存在的 `.specify/skills/external/…`；082/085 指向不存在的证据文件；`.specify/.tmp/086-*` 属正当历史 | `orphan-path` | ND-FR-009, ND-FR-016 | ND-SC-005, ND-SC-007 | II（正文路径字面量移交 086 / 082 / 085）；`.specify/.tmp/086-*` 登记为排除 |

**双向校验（092 原文保留）**：无 ND-FR 承接的组（空集）与无组承接的检测类别（`deferral-marker` 目前只由理念层 ND-FR-002…ND-FR-005 承接、无 A–H 代表条目）都 MUST 在 plan 阶段显式说明——后者是预期，因为 A–H 回顾不专门检查延期措辞。
