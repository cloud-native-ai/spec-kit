# Implementation Plan: 元技能治理：机制/策略分离与技能引用归一化（Meta-Skill Governance）

**Branch**: `083-mechanism-policy-separation` | **Date**: 2026-11-05 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `083-mechanism-policy-separation` → Feature 083「元技能治理：机制/策略分离与技能引用归一化」
**Input**: Specification from `.specify/specs/083-mechanism-policy-separation/requirements.md` (clarified 2026-11-05, scope update clarify 2026-11-05; two capabilities, one Feature — FR / SC / STR / 假设 / 约束的**当前计数以 requirements 的 `validate-requirements.py` 实测为准**，本文件不手抄)

> **scope update 的处置（2026-11-05 plan 更新）**：本文件在 `58d3dc5b` 上**增量更新**，把第二个能力「技能引用归一化」纳入同一个计划。
> - **被撤回的早改**：不再有 `083a` / `083b` 两个切片。原 `## Scope Snapshot` 与 `## Slice 083b` 两节（工作树里未提交的早改，写于 FR 上限仍为 30 时）被替换为 § Decomposition & Ceiling 的单包结论；撤回依据是 clarify 裁决 ③（30 FR < 60 上限，切片前提消失）与 `decomposition-check.py --mode plan` 的实测读数（见 § Scope Update Record）。
> - **被改写的既有行**：凡是「`coaching-skills` / `run-skills` 零改动」「允许差异集 6 条」「四个技能文件」，以及 FR / SC 的**前值**计数（见 § Scope Update Record 的变更台账）表述都已被第二能力证伪，本次逐条改写并在 § Scope Update Record 的 `SU-nn` 行披露。**D1–D7、T-001–T-003、EP-001–EP-006 的内容未被改写**，只做复核。本轮 repair（M3，2026-11-05）对 D2 / D6 / D7 / D13 的计数表述做了与实测对齐的更正，逐条记在 § Delivery Review 的 DC-008。

## Summary

把「机制/能力」与「策略/职责」的归档边界立成一条一等原则，并让它**只经由元层**生效；同时把「元技能怎么命名它要操作的那个技能」收成一份唯一文法——两者共享同一元技能范围与同一消费面。技术路线：

- **2 个 owner 文档**：`shared/definitions/mechanism-policy-definitions.md`（[[STR-003]]——两层判别、误置症状、归档规则、消费侧提示形态、元层谓词与封闭成员表、附录题集，OD-01…OD-10）与 `shared/definitions/skill-reference-definitions.md`（[[STR-004]]——接受形式、归一化顺序、消歧、失败语义、嵌套链，GR-01…GR-10）。
- **元技能接线**：`create-skills` § 6（机制/策略收尾校验，SW-01）、`improve-skills` § 2/§ 3（调研问题 + 候选类别，SW-02）、`merge-skills` § 5/§ 8（前置判断 + 验证项，SW-03）。每条判定 = **一行判定语 + 一个 owner 路径引用**（C5 / FR-015）。
- **5 个消费方接线**：`run-skills` / `create-skills` / `improve-skills` / `merge-skills` / `coaching-skills` 各**只声明自己的参数** + 一条指向 [[STR-004]] 的**源路径**引用（SR-01…SR-06，clarify 裁决 ②）。
- **1 个 create-skills 自有 reference**：`skills/external/create-skills/references/mechanism-policy-check.md`（判定步骤 + 两类误置的定位方法，≤ 12 行，SW-01）。
- **11 个契约测试模块**：机制/策略 6 个（GM-01，`test_mechanism_policy_*`）+ 技能引用 5 个（GM-11，`test_skill_reference_*`），承载 SC-001/SC-003/SC-004/SC-005/SC-006/SC-007/SC-008/SC-009 的可判部分与 SC-002 的形态前置；另有 **1 个 test-only 辅助** `tests/contract/skill_reference_matrix.py`（归一化的单一可执行实现，被 5 个引用模块 import，不是 pytest 模块、不是门禁，D11），它与 11 个模块合计 12 个 `tests/` 新增文件。
- **零新增**：零新增命令、零新增门禁脚本、零新增目录根、零新增环境变量、零新增配置键（A3 / A5 / A6 / C4 / C8 / FR-011 / FR-016 / FR-029）。
- **单包交付**：30 FR / 9 SC，自然任务估计 ≈ 36 < 80（`decomposition-check.py --mode plan` 实测 `fr_count=30`、`fr_ceiling=60`、`decision=proceed`），不切片（D8 / § Decomposition & Ceiling）。

判定的写面与判定面刻意分离（GM-02）：**语义**判定（这段文字归哪一层、这条引用说的是哪个技能）只在能用确定性程序表达时才进 pytest；机制/策略侧的人工样本落 SC-001 双判定者与 SC-002 流程实录，引用归一化侧则**整体可判定**（固定形态规则），全部进 pytest。`research.md` § R7（机制/策略）与 § R10–R15（技能引用）实测了这个分工的每一个载体，结论是「零新脚本」在两侧都成立。

## Technical Context

**Language/Version**: Markdown（owner 文档 / 技能正文 / 合同文本）+ Python 3（**仅既有的** pytest 契约测试；不新增依赖、不新增引擎、不新增 `scripts/` 下的文件）。实测解释器 `CPython 3.14.6`（`scripts/bash/run-tests.sh` 解析到的 `.venv/bin/python`），`pyproject.toml` 的 `requires-python = ">=3.8"` 不变、不新增 pin；11 个新契约模块 MUST 在该解释器下与 `>=3.8` 语法面内均通过（RS-001）。
**Primary Dependencies**: 既有引擎 `scripts/python/sync-mirrors.py`（镜像再生成，覆盖 `shared/definitions/` 两份 owner 与 `skills/` 五个消费方）、`scripts/python/regen-command-copies.py`（按工具命令副本，本特性预期零变化）、`.specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py`（阶段门）；既有技能脚本 `skills/external/improve-skills/scripts/{skill-shape,redline-check}.py`（被改技能的体积与红线判定）；运行时 `git`（SC-003 的逐字节比较与漂移守卫）。
**Storage**: 无数据库、无服务、无运行时状态。判定输入是 Markdown（两份 owner 文档、五个消费方 `SKILL.md`、两个 `references/` 文件、合同文本）+ 一个 JSON fixture（归一化矩阵）；证据落 `<spec-dir>/test-evidence/`（`plan-scope-update-*`、`plan2026-11-05-*`、SC 各面的测量记录）；无新增数据文件、无第二套分类数据文件（FR-016 / FR-029）。
**Testing**: `env -u PYTHONPATH bash scripts/bash/run-tests.sh …` → `pytest 9.2.0` on `CPython 3.14.6`（`env -u PYTHONPATH` 是本机的运行前提，见 EP-001 与 `research.md` § R1）；基线判据是**定向集失败名差集**而不是绝对全绿（GM-08）。
**Target Platform**: 任何受支持的 agent 宿主（`docs/reference/cli/supported-agent-tools.md` 的 roster，`AGENT_CONFIG` 为准）。仓内可判定的部分只要求 POSIX shell + `python3` + `git`；SC-002 需一个受支持宿主执行真实元技能流程（EP-002）。
**Project Type**: single（框架源码 + 自举运行时双帽：改 `shared/`、`skills/`、`tests/`，`.specify/` 同名文件由 `sync-mirrors.py` 产出；命令模板零改动）。
**Performance Goals**: 无吞吐目标。11 个新契约模块的读盘面是 2 份 owner 文档 + 5 个消费方 `SKILL.md` + 2 个 `references/` 文件 + 1 份 JSON fixture + 1 个基线树清单，整组应在秒级完成；owner 文档新增文本走「一行判定 + 路径引用」形态，不把判据表或失败表复制进技能正文（C5 / FR-023 / FR-026）。
**Constraints**: 零新脚本 / 零新命令 / 零新门禁 / 零新目录根 / 零新环境变量（A3 / A5 / A6 / C4 / C8 / FR-029）；两份 owner 之外零复制（FR-015 / FR-023）；成员表之外的既有技能与全部命令模板除 **5 个消费方的引用归一化接线**外逐字节不变（SC-003 的允许差异集 + SC-007 的包含性声明）；策略缺失时零写入（SC-004）；归一化结果恰为三值（FR-030）；不 push。
**Scale/Scope**: 5 条用户故事（US1–US5）；30 FR / 9 SC；改动/新增源面 **23** 个 —— ① owner 文档 **2** 新增；② 技能正文改写 **9**（`create-skills` / `improve-skills` / `merge-skills` / `coaching-skills` / `run-skills` 五份 `SKILL.md` + `improve-skills` / `merge-skills` 两份 `references/`）；③ 新增技能自有资源 **1**（`references/mechanism-policy-check.md`）；④ 契约测试 **11**；⑤ JSON fixture **1**。①+②+③ = 12 个是 `sync-mirrors.py` 的覆盖面，④+⑤ = 12 不镜像；两侧在 § Project Structure 的树内与 `feature-ref.md` § Delivery surface 逐项同口径。另有 3 处**登记行**（`glossary.md` / `framework-map.md` / `CHANGELOG.md`，均为既有单文件注册表上的行，不是新文件、不是新目录）+ 2 类镜像再生成入口（`sync-mirrors.py` 覆盖 12 个文件，`regen-command-copies.py` 预期零变化）；自然任务估计 **≈ 36** < 80（见 § Decomposition & Ceiling）。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.15.0, 18 principles in file order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每条设计决定追到一个 FR：`contracts/owner-document.contract.md` / `skill-wiring.contract.md` / `guard-and-measurement.contract.md` / `skill-reference.contract.md` 的可追溯性表是 FR→条款→测试的唯一映射；30 条 FR 全部有落点（DR-001 表，第二个能力的 FR-019…FR-030 由 GR-01…GR-10 + SR-01…SR-06 + GM-11 承载）；被判据拒绝的替代方案留在 § Design Decisions 而不是消失 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 083（`feature-ref.md`，clarify 已落 `features.md` 083 行与 `features/083.md`，并在 scope update clarify 中把两处改名到覆盖两个能力的完整名）；本阶段只把状态从 `Draft` 解读为 **Planned**，`Implemented` 由 `/speckit.implement` 拥有；本阶段**不改**注册表（D9 把 `Last Updated` 更新留给 implement 收口） |
| III | Intent-Driven Development | ✅ Pass | Summary 先给两个能力各自面向使用者的可感差别（「误置当场被拦下」「同一写法在五个元技能里得到同一答案」），机制细节留给 `contracts/`；D1–D14 逐条记录被否决的替代方案 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 11 个契约模块在 GM-01 / GM-11 里先于实现定义，且「红先行形态」被钉死（artifact missing 红，MUST NOT import/collection error 红）；GM-07 要求每个模块至少一条反例断言，防止绿得与命题无关；SC-001…SC-009 的采集方法在 § Measurement Plan 逐条声明 |
| V | AI Agent Integration Standards | ✅ Pass | 不动 `AGENT_CONFIG` / `_ASSISTANT_TIERS`、不动任何 agent 配置；命令模板零改动因而零按工具副本变化（`## Mirror Obligations` 第 3 行）；SC-002 的宿主取自既有 roster，不新造集成面。第二个能力**只改技能正文里的坐标与参数声明**，不新增宿主可发现的入口（FR-029） |
| VI | Continuous Quality & Observability | ✅ Pass | 关闭判据是**名字级差集**与可复算的记录，而不是「看起来绿」：SC-003 的守卫必须报出 `compared=575` 形态的计数（GM-04，实测 575），因为一个比较了 0 个文件的守卫会永远绿；SC-006 的分母是 fixture 行数（≥ 12，实测 14），SC-007 的扫描必须报命中路径与行号（GM-11 / GM-12）；既有债务（三个技能改动前就 exit 10，`research.md` § R4）按根因披露为 EP-003，不当作本特性的通过条件 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 只推进到 plan；Pre-Status-Flip Gate 的判据 owner 保持 `templates/feature-details-template.md` § Canonical Status State Machine，本文件只负责 plan 侧的产物与两张表 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 设计前实测而非引用记忆：`ALLOWED_POST_BASELINE_CHANGES` 的真实键集与 `WIRING_SKILLS`（`research.md` § R3）、`skill-shape.py` 三份 10 分（§ R4）、镜像基线六对（§ R5）、基线路径集 575（§ R6）、`PYTHONPATH` 报错原文（§ R1）。`coaching-skills` / `run-skills` 在冻结清单里的真实位置是**实测**并写进 D7。第二个能力的现状同样先实测：owner 文档现有六步顺序的逐行分类（§ R10，14 行探针）、五个消费方 8 处引用串的**源路径 vs 镜像路径**实测（§ R11）、`tests/` 对 `skill-reference` 零命中（§ R12） |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 两份 owner 文档 + 五条判定/引用行 + 11 个测试模块 + 1 份 JSON fixture；无运行时、无守护进程、无新依赖、无第二套门禁（D2 / SW-07 / GR-10）；被否决的「抽出确定性探针脚本」（D2）、「新增命令面」（D3）、「把归一化实现成 `scripts/` 下的新脚本」（D11）均记录理由 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新文件全部小写 kebab-case 且路径即语义：`shared/definitions/mechanism-policy-definitions.md`、`shared/definitions/skill-reference-definitions.md`（与兄弟 `derivation-definitions.md` / `dogfooding-definitions.md` 同形）、`skills/external/create-skills/references/mechanism-policy-check.md`、`tests/contract/test_mechanism_policy_*.py`、`tests/contract/test_skill_reference_*.py`、`tests/fixtures/skill-reference/normalization-matrix.json`；不触保留名、不改 `SKILL.md` 的既有命名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | **两顶帽子已点名**：框架源 = `shared/`、`skills/`、`tests/`；`.specify/` 同名文件由 `sync-mirrors.py` 产出，MUST NOT 手改镜像——第二个能力在这条上**踩过一次**（工作树里的并发起点在五份 `SKILL.md` 里写的是**镜像**路径，clarify 裁决 ② 已改判为源路径，D11 记录处置）。本特性自身按其新规则走：`data-model.md` 与 `contracts/` 只写机制（判定形态），路径、落点与样本位置一律写成参数或运行环境取值（`feature-ref.md` 末节自用声明） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用而不新建：`sync-mirrors.py`（镜像）、`regen-command-copies.py --check`（证明命令副本零变化）、`pre-analyze-check.py`（阶段门）、`skill-shape.py` / `redline-check.py`（被改技能体积与红线）、`overlap-check.py` / `decomposition-check.py`（plan 门）、既有 `tests/conftest.py` 的 `tmp_path` 与 `_disable_git_config`；无一个既有 Tool 覆盖的能力需要新写代码，故本特性不产出新 Tool 记录 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Change Validation（元流程在作者侧拦误置；引用在进入流程前就被收成一个标识）与 Reliable Delivery（策略缺失或引用零命中时在任何副作用之前停下），对应 `shared/guidelines/better-harness.md` 的五个工作环维度中的两项；证据纪律在 GM-02 / GM-12 落地——「配置了就存在」不等于「用起来了」，故 SC-002 记宿主实录、SC-007 记扫描的命中路径与行号，而不是断言「判定已接入」 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 两个新 owner：`shared/definitions/mechanism-policy-definitions.md`（[[STR-003]]）与 `shared/definitions/skill-reference-definitions.md`（[[STR-004]]），其余位置只带路径 + 章节锚；两份 owner 互不复制（C9 / GR-09）；「不复制」边界逐个落成机械断言（`contracts/owner-document.contract.md` OD-08 + `test_mechanism_policy_ownership.py`；`contracts/skill-reference.contract.md` GR-03 + `test_skill_reference_consumers.py` 的**包含性扫描**）；允许差异集只有 `data-model.md` § GM-03 / § GM-11 两个路径落点，两份测量契约只陈述计数（GM-03 要件 3）；`§ Decision Tensions` 的表格形态不在此复制 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | owner § Consumption Contract 的提示形态是可复制的骨架（三行字段 + 一个示例），字段名用**用户可识别的名字**而不是内部变量名（OD-06）；引用归一化的报告形态同时给**原始写法**、**归一化后的标识**与**判定类**（FR-025 / FR-030），使用者能直接看出「我写的东西被读成了什么」；面向人的产出按 `shared/guidelines/user-facing-comprehension.md` 写作；机读字面量（`included` / `excluded` / `command-surface` / `skill` / `failure`）原样英文，翻译只发生在人的一侧 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 判定是二值（机制 / 策略；命令面 / 技能标识 / 失败），MUST NOT 引入严重度或「视情况」中间层（OD-02 / V-5 / FR-030）；本文件在 `58d3dc5b` 的 plan 里把 `test-evidence/plan-baseline.txt`（上一 attempt 未落盘）就地纠正（DC-001）；本轮把第二能力并入时发现的三处**已记录预期不符**均按二分流处置并逐条披露（§ Scope Update Record：SU-01 范围矛盾→纠正、SU-02 镜像路径→纠正、SU-03 分类冲突→**裁决缺失**，作为 EP-007 记 `verified`） |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | **不新增任何目录根**（C4 / FR-029）：两份 owner 进既有 `shared/definitions/`，引用文档进既有 `skills/external/create-skills/references/`，测试进既有 `tests/contract/`；新增的 `tests/fixtures/skill-reference/` 是 `tests/fixtures/` 下第 13 个按特性命名的夹具目录（既有先例 `tests/fixtures/acceptance-hardening/`；同根 `ls -d tests/fixtures/*/` 实测已有 12 个，新目录加入后为 13 个），属既有根下的新子目录，按 `.specify/shared/guidelines/directory-governance.md` 的「既有根下的特性夹具」形态登记理由（D13），**不新增目录根、不改 `directory-governance.md` § 2 目录图**；`framework-map.md` 只需给既有 `definitions/` 行补一个文件名（D9），临时产物落 `.specify/.tmp/` |
| XVIII | Grounded Naming | ✅ Pass | 名字全部来自已记录来源：用户原话逐字给出 `Mechanism–Policy Separation` / `机制/策略分离`（[[STR-003]]）与「技能引用归一化」；第二个 owner 的文件名 `skill-reference-definitions.md` 由并发实现给出并在 clarify 裁决 ② 中以 [[STR-004]] 落定（用户裁定 + 最近同族先例）；测试模块 `test_skill_reference_*` 与既有 `test_mechanism_policy_*` 同族；不新造第三套名字（A2 / FR-018） |

**Gates Status**: ✅ All gates pass — no Fail, no Partial, no Complexity Tracking row.

**Re-check after Phase 1**: 2026-11-05（`58d3dc5b` 的 plan 收尾），重跑于已落地的 Phase 1 产物（`research.md`、`data-model.md`、`contracts/` ×3、`quickstart.md`、`feature-ref.md`）——18 行保持 ✅ Pass。行 **IV**（模块的「红先行形态」由 GM-01 钉死 + GM-07 反例断言）与 **XIV**（九个 N-xx 边界从散文变成机械断言）的证据有移动。

**Re-check after the scope update（2026-11-05，本文件）**: 逐条重读 18 行，**无一行翻转为 Fail / Partial**。证据有移动的行：I / II / III / IV / V / VI / VIII / IX / X / XI / XII / XIII / XIV / XV / XVII / XVIII（计数从 18 FR / 5 SC / 6 模块变为 30 FR / 9 SC / 11 模块；两份 owner；五消费方；新增夹具子目录）。结论未动、表述更明确的两行：**VII**（仍只推进到 plan）与 **XVI**（二值判定经 FR-030 的三值封闭后仍是二分流：命令面/技能标识走「正常继续」、失败走「关闭」，没有中间层）。没有任何行需要 Complexity Tracking。

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md` — one pointer, read from the repository root; this section MUST NOT restate the owner's criteria table, rejection list or threshold table.*

Fields: `decision`, `antithesis`, `binding_constraints` (with `pole_a` and `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; record identifier `tension_id` (`T-NNN`).

`research.md` § R9 实测了门槛：三条触发（跨团队、高爆炸半径、触及宪法 MUST）全部成立，故本计划记录 **T-001 … T-003**；第二个能力的门槛在 § R15 实测同样全部成立，故追加 **T-004**（T-004 是唯一一条「重开代价 = 一次跨仓坐标迁移」的记录，其余三条的重开代价都限于本仓文本）。

### T-001 — owner 文档是唯一判据载体，元技能只带「一行判定 + 路径」

- **decision**: 判据、成员表、症状表、提示骨架、题集全部只住在 `shared/definitions/mechanism-policy-definitions.md`；三个元技能各加**一行**判定语 + 一个 owner 路径引用，`create-skills` 的定位方法落它自己的 `references/mechanism-policy-check.md`（≤ 12 行）。元技能正文 MUST NOT 内联判据表或症状全表（SW-01）。
- **antithesis**: 把判据表直接写进三个元技能正文（每个技能自带一份可读的判定清单）。当元技能的读者几乎不会打开被引用的文档、而判据表足够短时它更优——Agent 执行时少一次读盘，判据就在眼前。
- **binding_constraints**:
  - pole_a: 判据只有一份——四份副本必然漂移，而漂移在「作者走了哪条路」这种只落产物不落日志的流程里不可见（Principle XIV 的失效面）。
  - pole_b: 判定必须能在不打开另一个文件的前提下**可执行地**开始——纯指针会让元技能的执行者跳过判定。
- **discriminating_evidence**: 对同一段误置样本，让执行者在「只读到元技能那一行」的条件下判定；结果二值：执行者能说出该去哪个文件看判据并给出可定位结论 / 执行者因信息不足直接放行。
- **expected_sacrifice**: SC-002 Source ↓ 三个被改 `SKILL.md` 的 `skill-shape.py` 已全部 exit 10（≈5354 / 5584 / 5096 可控 tokens vs 5000 预算），本决策的「一行」形态是唯一不把体积债务进一步恶化的写法；代价是每次判定多一次读盘。
- **revision_trigger**: 连续两个下游项目的元技能流程出现「执行者没打开 owner 就给了通过判定」≥ 2 次 → 重开，评估把最小判据（一句话，不含成员表）内联进 `create-skills` § 6。

### T-002 — 作者侧判定挂在既有校验步骤，不抽成确定性脚本

- **decision**: 机制/策略判定落 `create-skills` § 6、`improve-skills` § 2/§ 3、`merge-skills` § 5/§ 8 的**既有**步骤；不新增脚本、不新增门禁、不新增第二套清单（A6 / C8 / SW-07）。
- **antithesis**: 写一个 `mechanism-policy-check.py`（stdlib-only、只读、退出码三态），把所有可正则化的形态（绝对路径、盘符路径、用户目录名）抽成确定性检查，元技能只调用它。当误置的多数形态确实是可 grep 的字面量时它更优——判定结果可复算，且元技能体积只加一行调用。
- **binding_constraints**:
  - pole_a: 判定必须覆盖**语义**面——「可复用逻辑是否住在运行环境的说明里」无法用正则判定，`research.md` § R7 实测的唯一载体是模型/人（GM-02）。
  - pole_b: 本特性 MUST NOT 新增第二套门禁或第二个检查器（C8 / FR-016 的「不新增」边界是 SC-003 与零新机器的共同前提）。
- **discriminating_evidence**: 拿 US1 场景 2 的机制误置样本（判定规则写在一份运行说明里）跑一个正则检查器，看它能否点名该行；结果二值：能（脚本方案成立）/ 不能（脚本只覆盖策略误置一侧，US1 场景 2 未覆盖）。
- **expected_sacrifice**: SC-002 Source ↓ 该检出率只能靠宿主实录测量（证据而非测试），不能靠一次 pytest 断言；`research.md` § R7 已把这条代价记为该决策的直接后果。
- **revision_trigger**: 三个元技能的判定在宿主实录里对「策略误置」侧出现 ≥ 2 次漏检且均由同一个可正则化形态造成 → 重开，评估只把该侧抽成确定性预览器（不成为门禁，只产出候选清单）。

### T-003 — 「零新增命令面」压过「给作者一条直接可调的入口」

- **decision**: 不新增 `/speckit.*` 命令，`templates/commands/skills.md` 零改动；`/speckit.skills` 只在 owner 成员表里作为 `command-surface` 声明接线位（SW-06 / OD-07）。
- **antithesis**: 新增 `/speckit.mechanism`（或给 `/speckit.skills` 加一个 `check` 子意图），让作者在提交前主动对任一技能跑一次判定。当判定被证明是高频动作、且元流程的收尾点太晚时它更优——作者可以随时自查，不必重跑整个创建流程。
- **binding_constraints**:
  - pole_a: 命令面每加一条，就有第二套入口需要与元技能保持一致，一致性本身要一条守卫（C1 的「不新增第二套判定」）。
  - pole_b: 原则必须能在**真实创建/改进路径上自动生效**，而不是依赖作者记得去调一个命令（A7：对既有技能零回溯改造，元流程是唯一自动通道）。
- **discriminating_evidence**: 统计一个真实创建流程里判定被触发的时机；结果二值：判定在作者仍在改技能的上下文里就触发（收尾点足够早）/ 作者需要在草稿写完后另行调用才触发（收尾点太晚，需新入口）。
- **expected_sacrifice**: SC-003 Source ↓ 该封闭因此可以覆盖全部 27 个命令模板（逐字节），代价是没有一条「作者主动自查」的便捷路径；作者侧的自查入口留给 `improve-skills` 的对账通道。
- **revision_trigger**: 连续两个下游项目报告「提交前无法自查、只能等元流程收尾」并因此返工 ≥ 2 次 → 重开，评估给 `/speckit.skills` 增加一个只读 `check` 意图（仍不新增命令）。

### T-004 — 消费方引用**源路径**，不引用 `.specify/` 镜像路径

- **decision**: 五个消费方（`run-skills` / `create-skills` / `improve-skills` / `merge-skills` / `coaching-skills`）在正文里一律以 [[STR-004]] 的**源路径** `shared/definitions/skill-reference-definitions.md` 引用 owner；`.specify/shared/definitions/skill-reference-definitions.md` 只作为 `sync-mirrors.py` 的生成物存在，MUST NOT 被任何正文引用（clarify 裁决 ② 的落地形态；SR-05 / GR-08）。
- **antithesis**: 引用**运行时镜像**路径。对**已安装**的下游项目而言，镜像路径是唯一真实存在的坐标——下游项目里没有 `shared/` 这个框架源根，所以一个引用 `shared/definitions/...` 的技能在安装态会指向一个不存在的文件，而引用 `.specify/shared/definitions/...` 在所有 Spec Kit 项目里都解析得到。当「技能只在安装态被执行」这一前提成立时，它明显更优。
- **binding_constraints**:
  - pole_a: 镜像由 `sync-mirrors.py` 生成，改源后忘记再生成就会读到旧文；正文引用镜像等于把「读到的是哪一版」交给一次人为记得的再生成（本次并发起点正是这个状态：两边逐字节相同，只因为刚生成过）。SC-007 的允许差异集把「生成镜像」定义为**产物面**而非**坐标面**，两者一旦混成同一串文字就不可区分。
  - pole_b: 引用必须在本仓的**源码树**里可解析，否则框架源内的读者与守卫（`pre-analyze-check.py` 的 missing-path、`test_skill_reference_consumers.py`）会读到一条指向生成物的坐标。
- **discriminating_evidence**: 在**安装态**（仅 `.specify/`，无 `shared/` 源根）跑一次五个消费方的引用解析；结果二值：五处引用都能解析到 owner（镜像路径方案成立）/ 全部落空（源路径方案不可直接移植，需要相对框架根解析）。**本计划已给出二值判定的立场**：clarify 裁决 ② 明写 standalone 与安装态下「消费方**不改写引用**、以相对框架根解析」，故本条的证据面是「相对框架根能否把源路径解析到安装镜像」——这一条**尚未实测**，交 implement 期由 SR-05 的断言与一次安装态实跑给出（§ EP-007）。
- **expected_sacrifice**: SC-007 Source ↓ 安装态读者多一跳心智（源路径 → 框架根 → 镜像），且本仓的 five-file 改写必须同时改掉并发起点里的 8 处镜像路径串——这一步是纯文本替换，可逆，且被该扫描项钉住。
- **revision_trigger**: 若安装态实跑证明「相对框架根」无法把源路径解析到镜像（SR-05 断言失败），或连续两个下游项目报告「技能正文里的引用在安装态打不开」≥ 2 次 → 重开，评估改为「owner 文档在两处各留一个坐标行，且由 `sync-mirrors.py` 生成第二行」（仍不新增手写第二 owner）。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/083-mechanism-policy-separation/
├── requirements.md           # /speckit.requirements output — this spec's What（本阶段 MUST NOT 修改）
├── plan.md                   # This file (/speckit.plan output)
├── research.md               # Phase 0 output — R1…R9 实测与可行性（机制/策略）；R10…R15（技能引用，scope update）
├── data-model.md             # Phase 1 output — 10 实体 / 34 校验规则 / 3 状态转移 / GM-03 + GM-11 允许差异集
├── contracts/                # Phase 1 output — 4 份契约（owner-document / skill-wiring / skill-reference / guard-and-measurement）
├── quickstart.md             # Phase 1 output — 14 个场景（S1–S14），逐例标注 run / deferred 与前提
├── feature-ref.md            # Phase 1 output — Feature 083 绑定与交付面（两个能力合并后的单包口径）
├── checklists/requirements.md # /speckit.requirements 的规格质量清单
├── test-evidence/            # 证据：plan 门禁输出、定向集基线、SC 各面的测量记录（plan-scope-update-* 为本轮）
├── tasks.md                  # Phase 2 output (/speckit.tasks — 不在本阶段产出)
└── verification.md           # 实现输出 (/speckit.implement)
```

### Source Code (repository root)

```text
# 框架源（本特性实际改/建的面；.specify/ 侧是 sync-mirrors.py 产出的镜像）
shared/
├── definitions/mechanism-policy-definitions.md   # NEW 唯一 owner（[[STR-003]]）；OD-01…OD-10 九个章节
└── definitions/skill-reference-definitions.md    # NEW 唯一 owner（[[STR-004]]）；GR-01…GR-10 十一节（起点 = 工作树未提交版，FR-027 核验/补齐）
skills/
├── external/
│   ├── create-skills/
│   │   ├── SKILL.md                              # 改写（SW-01 + SR-02）：§ 6 Minimum checks 末行之后 +1 条 checklist 项；§ 1 Case A「只命名不解析」+ owner 源路径引用
│   │   └── references/mechanism-policy-check.md  # NEW（SW-01）：判定步骤 ≤ 12 行 + 两类误置的定位方法
│   ├── improve-skills/
│   │   ├── SKILL.md                              # 改写（SW-02 + SR-03）：§ 2 调研问题 + § 3 候选类别；Input Contract 的 Target identifier 只声明参数 + owner 源路径
│   │   └── references/loop-playbook.md           # 改写（SW-02）：批量模式以一次批口径执行
│   ├── merge-skills/
│   │   ├── SKILL.md                              # 改写（SW-03 + SR-04）：§ 5 no-loss gate 之后前置判断 + § 8 一条验证项；Source/Target 只声明参数 + owner 源路径
│   │   └── references/provenance-record.md       # 改写（SW-03）：how to verify 一栏可写层归属判定（不新增列）
│   └── coaching-skills/
│       └── SKILL.md                              # 改写（SR-06，仅引用归一化接线）：§ Inputs 参数声明 + § 2 解析一行 + § Nested 一节；**机制/策略侧零改动**（SW-05 仍成立）
└── internal/
    └── run-skills/
        └── SKILL.md                              # 改写（SR-01，仅引用归一化接线）：Input Contract + § 1 第 0 步；**位置阶梯（§ 1 第 1–4 步）逐字节不变**（FR-022 / SW-05 仍成立）
tests/
├── contract/
│   ├── test_mechanism_policy_owner_doc.py        # NEW — OD-01…OD-10 形态 + owner 镜像逐字节（GM-01）
│   ├── test_mechanism_policy_ownership.py        # NEW — 一源与六个邻接 owner 的边界（FR-015 / OD-08：dogfooding / directory-governance / create-skills § 2 / one-source-of-truth / bilingual-expression / temp-directory-discipline）
│   ├── test_mechanism_policy_skill_wiring.py     # NEW — SW-01…SW-03 的位置、唯一性、owner 引用、通过分支
│   ├── test_mechanism_policy_guard.py            # NEW — SC-003 逐字节封闭集（GM-03 五要件 + GM-07 反例）
│   ├── test_mechanism_policy_missing_policy.py   # NEW — SC-004 零写入 + 补齐后逐字节一致（GM-05 主面）
│   ├── test_mechanism_policy_decidability.py     # NEW — SC-001/SC-005 分母（附录题集可解析、依据只引 OD-02）
│   ├── skill_reference_matrix.py                 # NEW — 归一化的**单一可执行实现**（stdlib-only，被 5 个引用模块 import；不是 pytest 模块）
│   ├── test_skill_reference_grammar.py           # NEW — GR-01…GR-06 / GR-08：owner 章节、接受形式封闭集、归一化顺序、三值输出、大小写多命中（GM-11）
│   ├── test_skill_reference_matrix.py            # NEW — SC-006：固定 fixture 逐行复算（GM-13，分母 = fixture 行数 ≥ 12）
│   ├── test_skill_reference_consumers.py         # NEW — SC-007：五消费方接线齐备 + 除 owner 零复制的包含性扫描（GM-12）
│   ├── test_skill_reference_command_surface.py   # NEW — SC-008：命令面正例 + 至少 1 条负例（GM-11 正负例成对）
│   └── test_skill_reference_failures.py          # NEW — SC-009：四类失败各一条 + 成对报告 + 不串味（GM-11 / GR-05）
└── fixtures/
    └── skill-reference/normalization-matrix.json # NEW — SC-006…SC-009 的唯一矩阵（唯一允许落点，GM-11 要件 3）

# 既有契约模块的登记面（D7：不是新文件，是既有单文件模块上的行）
tests/contract/test_expression_compatibility.py  # ALLOWED_POST_BASELINE_CHANGES 5 处登记面（D7：机制/策略侧三份新增 + 引用侧一份新增 + 一份既有键更新），MUST NOT 改哈希清单

# 计划期义务（登记行落在既有单文件注册表上；不是本特性的代码交付面，D9）
.specify/memory/glossary.md             # +1 词条 `机制/策略分离 (Mechanism–Policy Separation)`（Origin user / Status proposed）
.specify/shared/definitions/framework-map.md  # 既有 `definitions/` 行追加两份 owner 的文件名（不新增行、不新增目录）
CHANGELOG.md                            # implement 收口时 +1 条

# 明确不改（SC-003 / SC-007 的比较单元内必须逐字节不变的部分）
templates/commands/**                   # 27 个模板全部零改动（SW-06 / T-003）
skills/internal/run-skills/SKILL.md     # 只在其 § 1 加第 0 步；位置阶梯（第 1–4 步）与信任边界段逐字节不变（FR-022）
shared/definitions/derivation-definitions.md    # 既有 owner 零改动（GR-09 邻接边界的代表行；其余同族 definitions 同样零改动）
```

**Structure Decision**: 全部落在既有目录形状上，**不新建任何目录根**（C4 / FR-016 / FR-029 / Principle XVII）：两份 owner 进 `shared/definitions/`（与 `derivation-definitions.md` / `dogfooding-definitions.md` / `flow-class-definitions.md` 同族的概念锚点层），判定方法进 `create-skills` 自己的 `references/`（技能自有资源，随技能分发，A3），11 个测试进 `tests/contract/`（与既有 `test_expression_compatibility.py` / `test_one_source_of_truth.py` 同族），矩阵夹具进 `tests/fixtures/` 下按特性命名的子目录（D13 的理由：夹具跨两个模块复用〔`test_skill_reference_matrix.py` 与 `test_skill_reference_failures.py` 读同一份文件〕，且它是 SC-006 的分母本身——写成散文或一次性运行记录即不满足 FR-030 的「真实仓内位置」）。`.specify/` 侧的同名文件全部由 `sync-mirrors.py` 产出、MUST NOT 手改。

> 机制/策略分离在本文件的自用：`data-model.md`、`contracts/` 与上表只写**机制**（形态、判据、断言口径）；路径、落点、样本位置一律写成运行环境取值。这是本特性按自己的新原则写的证据（`feature-ref.md` 末节）。

### Mirror Obligations

Baseline measured **before** any edit on this branch (2026-11-05, `research.md` § R5 / `quickstart.md` § S3): `sync-mirrors.py --check` exit 0, six pairs all `ok` (templates 22 / skills-external 409 / skills-internal 138 / agents 3 / scripts 119 / shared 62); `regen-command-copies.py --check` exit 0. Baseline drift is zero, so an absolute `exit 0` criterion is legitimate **because it was measured**, not by expectation — and the count movement the second capability causes (`shared/` 62 → 63 after the concurrent owner doc landed) is a post-sync baseline, MUST NOT be hard-coded into any assertion (`quickstart.md` § S3 判据；本轮实测复跑六对全 `ok`、`shared/` 已是 63，逐字见 `test-evidence/plan-scope-update-gates.txt`)。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/mechanism-policy-definitions.md`（NEW）与 `shared/definitions/skill-reference-definitions.md`（起点已在工作树，本轮由 implement 定稿） | `.specify/shared/definitions/{mechanism-policy,skill-reference}-definitions.md` | `python3 scripts/python/sync-mirrors.py` 然后 `--check`；判据 = 该对 `ok` 且**无新增漂移**（基线六对全 ok）。所有新增断言 MUST NOT 钉 `shared/` 的文件计数 |
| `skills/external/{create-skills,improve-skills,merge-skills,coaching-skills}/SKILL.md`（改写，四份全部改动：前三份加载机制/策略判定与引用归一化，`coaching-skills` 只加引用归一化接线）、`skills/internal/run-skills/SKILL.md`（改写：只加引用归一化接线）、`skills/external/create-skills/references/mechanism-policy-check.md`（NEW）、`skills/external/{improve-skills,merge-skills}/references/*.md`（改写） | `.specify/skills/{create-skills,improve-skills,merge-skills,coaching-skills}/**`（平铺层，`skills/external → .specify/skills` 对）与 `.specify/skills/internal/run-skills/**`（嵌套层，`skills/internal → .specify/skills/internal` 对） | 同一条再生成 + `--check`；判据 = `ok` 且无新增漂移。**两个能力在这一行合流**：`coaching-skills` 与 `run-skills` 是机制/策略侧的排除成员（SW-05，零改动），同时是技能引用侧的消费方（SR-06 / SR-01，必改）——两者的差集为空，故 SW-05 的可判形态改写为「正文中**机制/策略判定的字面**零命中」，而不是「文件零改动」（§ Scope Update Record 的 SU-01） |
| `templates/commands/**`（**本特性零改动**） | `.claude/commands/speckit.*.md`、`.github/prompts/speckit.*.prompt.md`、`.qoder/commands/speckit.*.md`、`.opencode/command/speckit.*.md`（`regen-command-copies.py` 的按工具副本；`templates/commands/` 已退役） | `python3 scripts/python/regen-command-copies.py --check` → exit 0（本特性预期**零变化**）。这条义务的用途正是**证明**命令面零改动（SW-06），而不是等它漂移 |
| `tests/**`、`CHANGELOG.md`、`.specify/memory/glossary.md`、`.specify/shared/definitions/framework-map.md` | 无镜像（`tests/` 不在 `MIRROR_PAIRS`；`glossary.md` 与 `.specify/shared/definitions/framework-map.md` 是**本仓的项目运行时产物**，无框架源对） | n/a。注意后者：`framework-map.md` 只存在于 `.specify/shared/definitions/`，**没有** `shared/definitions/framework-map.md` 源文件，因此它是一条「只在此处」的登记行，不是镜像漂移 |

## Scope Update Record (2026-11-05, plan 更新)

本节的用途：逐条记录 plan 更新阶段**实测到的「与已记录预期不符」**及其二分流处置（`.specify/shared/guidelines/fast-fail.md`），以及本阶段对既有行的**变更台账**。没有任何一条被静默修平。

### 二分流处置（纠正 / 裁定）

| ID | 发现了什么 | 判定 | 处置 |
|----|-----------|------|------|
| SU-01 | 第二个能力并入后，plan 里「`coaching-skills` / `run-skills` **零改动**」「允许差异集 **6** 条」与 FR-026（五个消费方 MUST 接线）**直接矛盾**——按旧文字实现，五个消费方中两个不许动，SC-007 必失败 | **纠正**：恰有一种读法与已记录意图一致——C1 谓词裁的是「要不要加载机制/策略判定」，从不裁「文件能不能被另一条 FR 改」；requirements 的 `§ Constraints C1` 表与 FR-026 在同一份文件里并存，唯一自洽读法是两者按不同面各管一段 | 改写 SW-05 的可判形态为「机制/策略判定字面零命中」；允许差异集由「单元内 6 条」扩到 `data-model.md` § GM-03 登记的 **10 条（单元内：8 feature + 2 absorbed）/ 20 条（登记表全量）**；冻结哈希登记面 +2 行（D7） |
| SU-02 | 五个消费方与 `coaching-skills` § Nested 的 **8 处**引用串写的是 `.specify/shared/definitions/skill-reference-definitions.md`（镜像路径），而本规格以源路径 [[STR-004]] 引用 | **纠正**：clarify 裁决 ② 已把口径裁成 source-canonical，且裁决本身给出了理由与影响面（8 处）；这是「已记录意图 vs 工作树产物」的偏差，不是两种读法之间的选择 | 不改工作树（派发边界）；写进 SR-05 / GR-08 / D11 / T-004 与 `data-model.md` E-8 / E-9，由 implement 执行替换并由 SC-007 的扫描项核对 |
| SU-03 | `speckit.skills` → NAME 与 `speckit.skills/SKILL.md` → PATH 的**分类冲突**在 owner 侧怎么解，规格只给了约束（FR-030 三值、§ Edge Cases 一条）而未给解法 | **不是纠正**：可在多种解法间取舍（新增「命令面」通道 / 在 name 通道后置命中 / 把带后缀写法移出接受形式）。本阶段选择「剥前缀与后缀先于通道判定」并说明为何它不引入第四值 | 记为 D12 的第一行 + GR-04；此外把「安装态下源路径能否解析到镜像」这一条**无法在本阶段实测**的前提显式记作 EP-007(a) `unverified`，并给出闭合任务（SR-05） |
| SU-04 | plan 与 `feature-ref.md` 里的 `083a` / `083b` 切片（未提交早改）写于 FR 上限 = 30 时，而本轮 `decomposition-check.py --mode plan` 实测 `fr_ceiling=60` | **纠正**：clarify 裁决 ③ 已裁定撤回，且判据可从实测复现 | 删除 `## Scope Snapshot` / `## Slice 083b` 两节，改写为 § Decomposition & Ceiling 与 D8 的单包结论；`feature-ref.md` § Slices 同趟改 |
| SU-05 | `feature-ref.md` 的交付声明里有 `shared/workflow/glossary.md` 的裸路径 token，使 overlap 检查把它算作交付面（3 条重叠来自它） | **纠正**：clarify U4 的 overlap 裁决明写「083 只按 glossary 协议新增一行，**不作为交付面**」；但记录该裁决本身必须点名此文件，而 `overlap-check.py` 按 token 识别路径，故 token **无法移除**（移除即无法记录裁决）。故处置从「移除 token」改为「如实登记残留」 | `feature-ref.md` 把它移出「改写框架源」交付清单、改述为**共享注册表的登记义务**，并**明写**「本行不声称已移除该 token」；复跑 overlap 得 **18 条**（3 glossary + 4 `run-skills` + 三份 SKILL.md 各 3 + 2 `coaching-skills`），全部对**已完成**特性的历史交付面，按状态脊 § Overlap adjudication 原样记录，不为追求 `clear` 删掉真实交付路径 |

### 变更台账（既有 → 本轮）

| 面 | `58d3dc5b` 时的值 | 本轮值 | 依据 |
|---|---|---|---|
| 用户故事 | 4（US1–US4） | 5（+US5） | requirements scope update |
| FR / SC | 18 / 5 | 30 / 9 | `validate-requirements.py` 实测（本文件不手抄） |
| owner 文档 | 1 | 2 | FR-019 / C9 |
| 契约测试模块 | 6 | 11（+5 引用侧） | SC-006…SC-009 |
| 允许差异集（比较单元内） | 6 | 8（`data-model.md` § GM-03 第 1–8 行：`create-skills` 的 1 条新增引用文档 + 五个消费方 `SKILL.md` + `improve-skills` / `merge-skills` 各 1 份 `references/`；登记表共 18 行，其余 10 行落在 `tests/`、本就不属比较单元） | `data-model.md` § GM-03（单一路径落点）；`contracts/guard-and-measurement.contract.md` GM-03 要件 3 / GM-12 只陈述计数 |
| 自然任务估计 | ≈ 21 | ≈ 36 | D8 |
| 切片 | `083a` / `083b` | `single-package` | SU-04 / clarify ③ |
| 执行前提 | EP-001…EP-006 | EP-001…EP-007（+ EP-007，其中 (a) 记 `unverified`） | 本文件 § Execution Premises |
| 承重决策 | T-001…T-003 | T-001…T-004（+ T-004 源路径口径） | clarify ② |

## Clarifications（本阶段裁定，2026-11-05 repair pass）

> 本节的裁定对象是 analyze 门（Fail；CRITICAL=0 / HIGH=2 已在本轮修复）之后残留的两条 **MEDIUM**。每条给出裁定结果、唯一 owner 与不许出现的写法；裁定本身不改任何 FR / SC / 模块清单。

| ID | 问题 | 裁定 | Owner（唯一） | 禁止写法 | 依据 |
|----|------|------|---------------|----------|------|
| **CL-01** | 技能引用归一化的**失败类数**：`contracts/guard-and-measurement.contract.md` GM-12 要件 3/4 一度写「三类允许」，而 `requirements.md` FR-024 给出**四类**（零命中 / 越界路径 / 不可读 / 两层同名） | **四类**。失败语义的唯一 owner 是 FR-024；GM-12 要件 3 的「允许差异集来源」三类是**另一件事**（允许的重复落在哪里），与失败类数无关，两者不得合并表述 | `requirements.md` FR-024（失败类）；`data-model.md` E-10 / V-31（四值）；`contracts/skill-reference.contract.md` GR-05（失败语义表） | 契约或 data-model 中「三类失败」「三个失败类」「三种失败」一类表述；把 GM-12 的允许差异三类误读为失败类 | requirements FR-024 的四条条件各带必需报告项；SC-009 的「四类各一条」已可判 |
| **CL-02** | `checklists/` 下 89 个未勾选的 `[ ]` 项是否构成本阶段的阻塞 | **不构成**。checklist 的条目是**问题项**（供人回答），不是 pass/fail 判定；清单文件的存在与形态是 checklist 阶段的产物判据，**清单项的满足判定由 implement 阶段的 checklist 豁免门接管**（`skills/external/sdd-loop-driver/references/dispatch-recipes.md` 的 checklist 门：产物 = 新增清单文件，满足判定不在本门裁决） | `shared/workflow/acceptance-hardening.md` § Gates（门与豁免的记录形态）；门的行为 owner 为 `dispatch-recipes.md` 的 checklist 门条目 | 给 checklist 项补 `disposition:` 字段；把未勾选项数写成 analyze 或 plan 的 Fail 依据；为「清单未勾完」造 waiter | `tasks.md` 的 GATE / DoD 不含「checklist 全勾」；`pre-analyze-check.py` 的 summary 也不含 checklist 计数 |

| **CL-03** | `account-clause-coverage.py` 的 FR citation groups 为 0（`fr-uncovered 30`） | **不阻塞本门**：四份 contracts 声明 `md-none` 条款形态，accountant 无法从条款 citation group 取 FR；FR 覆盖由 plan § Delivery Review 的 DR-001 逐条映射与 tasks 的每行交付面人工核验（30/30 已逐条确认），MUST NOT 为刷绿伪造 citation group 或改契约条款形态；`coverage-baseline.txt` 已冻结，`clause-uncovered` 为 pass（0 beyond baseline） | `requirements.md` FR-001…FR-030；`plan.md` § Delivery Review；`tasks.md` 的每行交付面 | 把 `fr-uncovered 30` 读成特性未覆盖；为它造第二份覆盖表；重新 freeze baseline | 30 条 FR 各自在 tasks 与 plan DR-001 有落点；`account-clause-coverage` 的 `clause-uncovered` 为 pass |

| **CL-04** | 吸收的并发 coaching 文件与 GM-03 允许集 | **已吸收**：`skills/external/coaching-skills/data-model.md` 与 `references/prompt-templates.md` 属于并入 083 的 skill-reference 工作（A11），登记进 GM-03 行 19–20（比较单元内共 10）；GM-03 表是唯一 owner，解析器按 `是/否` 列读取；其它工作线（083 / ssh-utils / sdd-project-setup）由 `feature_commits`（提交信息含 `083`）排除，不入本特性的允许集 | `data-model.md` § GM-03 rows 19–20；`tests/contract/test_mechanism_policy_guard.py` 的 `feature_commits` / `registered_allowed_set` | 把 083 / ssh-utils 路径塞进 083 允许集；用工作树全量代替 083 提交选择 | guard 9/9；in-unit 10；`feature_commits` 仅选 `(083)` 提交 |

**与既有披露的关系**：CL-01 是 analyze 门之后的残留计数冲突，修正在契约侧（`contracts/guard-and-measurement.contract.md` GM-12），披露记 `DC-009`；CL-02 不给 checklist 造新状态，也不改 `checklists/` 任何文件——「禁止写法」一列已把这一点写成禁止项。

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises — this section carries the column set and the values only.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | 一套可用的 **Python 3 + pytest + git** 运行环境存在，且是仓内既有入口 `scripts/bash/run-tests.sh` 能解析到的那一套；11 个新契约模块与 SC-003 / SC-007 的逐字节比较都压在这条前提上 | `research.md` § R1 实测：`.venv/bin/python` → `Python 3.14.6` / `pytest 9.2.0`；`git version 2.54.0 (Apple Git-157)`；`pyproject.toml` `requires-python = ">=3.8"`。**运行形态前提**：本机 shell 的 `PYTHONPATH` 指向一套内部 lib，其 `platformdirs` 缺 `pytest_plugin`，使 `.venv/bin/python -m pytest` 启动前即报 `ModuleNotFoundError: No module named 'platformdirs.pytest_plugin'`；处置 = 测试一律以 `env -u PYTHONPATH` 前缀运行（`quickstart.md` § S2 逐字命令），MUST NOT 修改 `run-tests.sh` 或 `pyproject.toml` 来绕开。**scope update 复核（2026-11-05）**：新增的 5 个引用模块只用 stdlib（`json` / `pathlib` / `re`），不引入第二个运行前提；结论不变 | verified | — |
| EP-002 | 至少一个**受支持的 agent 宿主**可用于 SC-002 的检出率 / 误报数测量（该项只能以流程实录为证据，不能以 pytest 断言替代，`research.md` § R7） | 本次 plan 运行**所在宿主** = 本仓约定内的原生子代理执行环境（`flow_class=execution` / `local` 拓扑，`state` spine 的派发前置检查 ③ 记 `n/a — 本地原生子代理`；④ 记 `execution-config.py --action resolve --agent …` exit 0，`mode=native`），宿主 roster 取自 `docs/reference/cli/supported-agent-tools.md`（`AGENT_CONFIG` 为准）。**可用性探针**：同一宿主上的 SDD 执行链在 requirements / clarify / 本 plan 阶段均已实跑（三次阶段产物落盘、门禁实跑），说明「能加载并执行框架流程」成立；**版本原文尚未采集**（本阶段未跑宿主 CLIs 的 `--version`），故本条按 `verified` 记「宿主可用」，`Pin` 列的「宿主名 + 版本原文」由实现期 SC-002 实录按 RS-005 的 `Contract` 单元格同趟记录 | verified | — |
| EP-003 | 三个被改的 `SKILL.md` 在**改动前**即已超出 `skill-shape.py` 的 5000 可控 tokens 预算（exit 10），因此本特性的通过条件不能写成「被改技能的 `skill-shape.py` exit 0」 | `research.md` § R4 + 本阶段实跑：`create-skills` ≈ 5354、`improve-skills` ≈ 5584（已扣除契约强制块 466）、`merge-skills` ≈ 5096，三份 `skill-shape.py` 均 exit **10**；同批 `redline-check.py` 三份均 rc **0** / `PASS — no red line triggered`（`coaching-skills` 对照：shape rc 0 / redline rc 0）。这是**既有债务**，不是本特性引入的缺陷；按 `improve-skills` Hard Constraint 3 的例外情形 (a) 处理：实现期 MUST 为每个被改文件记录 before/after 两个 `est_tokens_controllable` 数与 delta，且新增文本保持「一行判定 + 路径引用」形态 | verified | — |
| EP-004 | SC-003 的比较单元在基线上**非空且可枚举**，且当前工作树与基线[[STR-002]]在该单元内零差异 | 本阶段实跑（`quickstart.md` § S4 的同一形态）：`git ls-tree -r --name-only 3ffeb26e -- skills/ templates/commands/` → **575** 个路径（`skills/` 548 + `templates/commands/` 27）；带允许差异集的补集比较输出 `compared=575 complement=570 allowed_in_unit=5 frozen_mismatches=0`。`allowed_in_unit=5` 正是「6 条允许路径中，`references/mechanism-policy-check.md` 尚未创建」——它是新增路径的下限证据，不是漏项。`research.md` § R6 同批测得 `git diff --stat aaee504c..HEAD -- skills/ templates/ commands/` 为空 | verified | — |
| EP-005 | 两处再生成入口在动手前零漂移，因此「本特性关闭时 `--check` exit 0」是可达判据 | `research.md` § R5 + `quickstart.md` § S3 实测：`sync-mirrors.py --check` 六对全 `ok`（templates 22 / skills-external 409 / skills-internal 138 / agents 3 / scripts 119 / shared 62）、`regen-command-copies.py --check` `OK: all per-tool command copies match the source templates`，二者 rc 0。**scope update 复核（2026-11-05，本轮实跑）**：同一命令六对仍全 `ok`，`shared/` 已从 62 变为 **63**（并发 owner 文档已生成镜像，`cmp` 通过），`regen-command-copies.py --check` rc 0——结论不变，且这条复核正是「计数不得钉死」的现场证据 | verified | — |
| EP-006 | 「零新脚本」在实现期**可兑现**：所有可判定的部分都有既有载体（pytest + git + 两个既有技能脚本），不可判定的部分本来就不该变成门禁 | `research.md` § R7 的逐判定载体表（七行）；GM-02 给出了写出/判定分离的边界；EP-001 证明 pytest + git 可用，`skill-shape.py` / `redline-check.py` 实测可跑（EP-003 同批）。**scope update 复核**：第二个能力的**全部**判定都是固定形态规则（前缀、后缀、大小写、集合归属），`research.md` § R10 的 14 行探针已证明它们可以由一个 stdlib 程序逐行复算——因此这一侧不需要「语义判定 vs 形态判定」的分离，直接进 pytest（GM-11）；「零新脚本」因此不只是在 083a 一侧成立，而是**加强**成立 | verified | — |
| EP-007 | 第二个能力的三条落地前提同时成立：**(a)** 安装态下「以相对框架根解析」能把源路径 [[STR-004]] 解析到一份镜像（clarify 裁决 ② 的 standalone 降级条款）；**(b)** `speckit.skills` 与 `speckit.skills/SKILL.md` 的分类冲突在 owner 侧有解且不引入第四个结果（FR-030）；**(c)** `run-skills`「名字可省扩展名」与「名字通道不剥 `.md`」的冲突由 owner 消歧、不改 `run-skills` § 1 的位置阶梯（FR-022） | (a) **`unverified`**——本阶段没有安装态样本。可达性证据只有两条间接读数：`sync-mirrors.py --check` 证明 `shared/ ↔ .specify/shared/` 逐字节一致（EP-005 本轮复核），且 `.specify/skills/` 与 `skills/` 的相对拓扑相同（`scripts/python/sync-mirrors.py` 的 pair 表）。**(b) `verified`**——clarify 的 14 行探针（§ R10）实测：同一命令名的两种写法今天分落 NAME / PATH 两类；裁决 ① 的第 3–5 步把「剥前缀」移到「通道判定」之前，于是 `speckit.skills/SKILL.md` 剥完 `SKILL.md` 后余值 `speckit.skills` 不含 `/` → name 通道 → 命令面；`/speckit.skills` 剥完 `/` 后同样 → 命令面。两写法收敛为一类，且**不产生第四个结果**（GR-04 / GR-05 的封闭三值是唯一出口）。**(c) `verified`**——裁决 ① 第 5 步明写 `.md` **不由归一化剥除**，故 `my-draft.md` 走 name 通道、名字即 `my-draft.md`，是否成立由阶梯判定；owner 的消歧句 MUST 明写「省略扩展名是**结算约定**、不是归一化步骤」，从而两处归属不重叠——这是**文本条款**，非运行时保证 | unverified | (a) 由 SR-05 的断言 + implement 期一次安装态实跑闭合（`quickstart.md` § S12 的 Premises）；(b)(c) 已实测成立、不需要处置，但整行取三者中**最弱**的状态，故记 `unverified`——一个不会因 (b)(c) 成立而变绿的格子 |

## Inherited Blockers

Owner of this table's shape, its `Disposition` domain (`resolved | inherited | not-applicable`), the `Source row` / `Carrier` / `Carrier slice` grammar and the carrier's eligibility rule: `shared/workflow/acceptance-hardening.md` § Inherited Blockers — this section carries the column set and the extraction readings only.

**Dependency set: none.** Derivation (measured 2026-11-05，scope update 复核后仍成立): 本特性不消费任何既有 Feature 的未决测量——它不修改任何既有特性建立的契约面（命令模板零改动；机制/策略侧对既有技能零回溯改造；技能引用侧只改五个消费方**自己的参数声明与引用坐标**，不改任何其它 owner），SC-001…SC-009 全部分母由本特性自己的 owner 附录题集、自己的 fixture 矩阵与自己的样本集给出。唯一与既有特性相接的面是冻结哈希模块的**登记行**（D7：`ALLOWED_POST_BASELINE_CHANGES` 追加 5 行），而登记行是本特性的交付义务、不是从别处继承的未决项。因此依赖集为空，按规则写这一句而不是留一句含糊的「无既有依赖」。

**Extraction readings (the closed three-source set, measured)** — 三个源各测一次，结论是**零行**，而零行是一个读数、不是一种处置，故本表没有处置行。读数写成列表而不是表：本节的表形态只属于处置表，一张读数列在它前面的表会被守卫读成「一串没有处置的行」（本阶段实测：`pre-analyze-check.py --stage plan` 曾把该表的三行读成 `row-1`/`row-2`/`row-3` 的 undisposed 错误，DC-003）。

- **`## Deferred` 节** — `grep -rn "^## Deferred" .specify/memory/features/` → **0 命中**（`.specify/memory/features/` 下没有任何特性详情携带该节）。
- **`verification.md` 的 `blocked` / `deferred` / `partial` 状态行** — `grep -rln "SC-001_status" .specify/memory/features/` → **0 命中**（特性详情不承载 status 行；status 行只住在各 spec 目录的 `verification.md`，而依赖集为空，故不在抽取范围内）。
- **非空的 `deferred_tasks=`** — `grep -rn "^deferred_tasks=" .specify/memory/features/` → **0 命中**。

**结论**：本特性**无继承 blocker**——依赖集为空，且三个源各产零行。MUST NOT 为一个不存在的行发明 locator（那正是 join key 要防的缺陷），也不为不存在的依赖写 `not-applicable` 行（`not-applicable` 要一个真实的 `Source row` 才有意义）。因此本节没有处置表，只有这一句零行结论。

## Design Decisions (D1–D14)

### D1 — owner 放 `shared/definitions/` 而不是 `shared/guidelines/`

`shared/definitions/` 装的是**概念锚点**（`derivation-definitions.md`、`dogfooding-definitions.md`、`flow-class-definitions.md`、`tool-definitions.md`…），每个文件回答「这个词是什么意思、边界在哪」；`shared/guidelines/` 装的是**工作流纪律**（`fast-fail.md`、`one-source-of-truth.md`、`directory-governance.md`…），每个文件回答「做这件事时该怎么走流程」。本特性交付的是**定义**而非流程：判别口径、成员表、症状分类、归档规则、提示形态、谓词。被否决的替代方案：放 `shared/guidelines/`（因为它约束元技能的流程）——否决理由是那会让「引用它 = 引用一段方法论」与「引用它 = 引用一个术语的定义」混成一种动作，而 FR-018 要求的恰恰是术语层的锚定（A2）。

落点：`shared/definitions/mechanism-policy-definitions.md`（框架源）→ `.specify/shared/definitions/`（镜像）。

### D2 — 零新脚本（依据 A6 / C8 / FR-016，判定依据是 `research.md` § R7 的实测，不是偏好）

`research.md` § R7 逐个判定逐条列出载体，七项里五项有既有确定性载体（pytest / git / 两个既有技能脚本），一项（语义判定）本来就不该被正则化（GM-02），一项（`references/` 的定位方法）是文本。**因此 A6 的「若 plan 证明书面判定不可判定，再决定是否抽成确定性脚本」在这个计划里的答案是：需要模型判断的那一半不可正则化，可正则化的那一半已被 GM-07 的反例断言覆盖在测试里。** 结论：不新增脚本。

这条决策的可判定形态：11 个新契约模块全部是 `tests/contract/` 下既有的 pytest 模块形态，不引入 `scripts/` 下的任何新文件；两份清单各自封闭（GM-01 六个机制/策略模块、GM-11 五个引用侧模块 + 一个 test-only 辅助），任何第十二个模块、任何新辅助文件或任何新脚本都必须先推翻本节。

### D3 — 成员谓词与封闭集

谓词逐字沿用 requirements § Constraints C1（clarify 已 ratified、全表复算无翻转，本阶段**不改一行**）：

| 流程 | verdict | 依据 | 本特性的动作 |
|---|---|---|---|
| `create-skills` | `included` | 产出新技能 | SW-01（§ 6 + `references/mechanism-policy-check.md`） |
| `improve-skills` | `included` | 产出变更后的技能 | SW-02（§ 2 + § 3 + `references/loop-playbook.md`） |
| `merge-skills` | `included` | 产出合并后的目标技能并下线源技能 | SW-03（§ 5 + § 8 + `references/provenance-record.md`） |
| `coaching-skills` | `excluded` | 产出是观察与计划，不改写受训技能；真实改写仍经 `improve-skills`，故其作者侧义务已被纳入者覆盖 | 机制/策略判定**零加载**（SW-05 的改写形态）；技能引用接线**必加**（SR-06） |
| `run-skills` | `excluded` | 产出是目标技能按其自身流程执行，不改变任何技能的定义或行为 | 机制/策略判定**零加载**（SW-05 的改写形态）；技能引用接线**必加**（SR-01） |
| `/speckit.skills` | `command-surface` | 命令模板的 Routing 表把 create/merge/coach 意图**转发**给上述元技能，故只声明接线位 | 零改动（SW-06）；且它是**技能引用**的「命令面命中」标杆（SC-008） |

**一处实测定位（不是变更谓词，是可执行性的修正）**：`run-skills` 的实际路径是 `skills/internal/run-skills/SKILL.md`（不在 `skills/external/`）。本计划的 SW-05 守卫与 GM-03 的结构不变量因此按**真实路径**写；owner 成员表只写流程名 `run-skills`，不带路径前缀，避免把「层」写成位置。这属纠正（恰有一种读法与已记录意图一致：requirements 的 C1 表按**流程**裁定，从不按目录裁定），已在 DC-002 披露。

**scope update 之后的第二处（同一判据，不是新裁决）**：C1 的谓词只裁定**机制/策略**这一侧的义务，不裁定技能引用的消费面。`run-skills` 与 `coaching-skills` 是 `excluded`，因此**此前的「零改动」读法**在第二个能力并入后自相矛盾（FR-026 点名五个消费方含这两者）。处置是收紧 SW-05 的可判形态而不是翻转谓词：`excluded` 成员在**机制/策略判定字面**上零命中，在引用坐标上按 SR-01 / SR-06 接线——一处纠正（恰有一种读法：C1 裁的是「要不要加载机制/策略判定」，不是「文件能不能被另一条 FR 改」），已披露（SU-01）。谓词本身、成员表、排除理由**未改一行**。

### D4 — 成员表放 owner 文档，不建第二份注册表

`data-model.md` E-6 的封闭成员表是 owner § Meta-layer Membership 的**形态投影**（可收窄、不可扩大），不是第二个定义点：机器可读的唯一落点在 owner 正文，`data-model.md` 的投影只用于让 `test_mechanism_policy_guard.py` 做交叉断言（V-19：`included` 集合 == 允许差异集的流程子集）。被否决的方案：`tests/` 里维护一份 `MEMBERS = (...)` 常量作为判定源——那会把「谁是元技能」变成只有测试知道的事实，而下游项目拿不到测试。允许的重复形态是既有三种之一：**literal pinned in a test**（`data-model.md` E-6 的表与 owner 保持字面相等，由 `test_mechanism_policy_owner_doc.py` 断言），不是第三套数据文件。

### D5 — 消费侧提示形态 owner 化，元技能只引用，不回溯改造

FR-006 要求「形态 owner 唯一，其余位置以路径引用」。落点 = owner § Consumption Contract（OD-06）；接线点 = SW-04 的**五处**「即将执行副作用之前」——`create-skills` 三处（§ 2 writability pre-flight、§ 7 写入之前、§ 8 报告前的写入）、`improve-skills` § 7 编辑之前、`merge-skills` § 7 decommission 之前（D6 与 SW-04 的「四处 / 四处」口径由此统一为**五处**，见 DC-008）。被否决的方案：为每个命令写一份提示模板——那既违反 FR-015（复制形态）也违反 FR-011（命令面零改动）。对既有 15 个 external / 38 个 internal 技能的正文：**零改动**（A7 / FR-011 / SC-003）。

### D6 — 机制/策略侧的六个契约测试模块不建声明式夹具；SC-001 / SC-005 的人工样本记录在 test-evidence

模块清单与断言面 = GM-01（封闭的六个，各对应一条契约条款组）。夹具策略：**机制/策略侧的六个模块不新建 `tests/fixtures/` 子目录**——`test_mechanism_policy_missing_policy.py` 用 pytest 既有 `tmp_path` 就地造「假技能 + 假运行目录」，`test_mechanism_policy_guard.py` 用 `tmp_path` 复制补集内一个文件并注入一字节破坏来断言转红（GM-07）。被否决的方案：在 `tests/fixtures/` 下新建 `mechanism-policy/` 声明式夹具集——那是「第一个新种类目录」，按 Principle XVII 要同趟登记目录图，而这一侧的夹具全部是一次性的最小树、没有跨模块复用价值，登记一个只用一次的目录是净负担。

**引用侧**是另一件事，不属本节：SC-006 的矩阵是**跨模块复用的期望值表且本身就是分母**（`test_skill_reference_matrix.py` 与 `test_skill_reference_failures.py` 读同一份文件），故它落 `tests/fixtures/skill-reference/normalization-matrix.json`，由 **D13** 登记理由。本节的「不用夹具」结论只覆盖机制/策略侧的六个模块。

人工样本（双判定者 SC-001、读者作答 SC-005、宿主实录 SC-002 / SC-004 支撑面）落 `test-evidence/`，**不入 pytest**——它们判的是模型/人的行为，不是形态（GM-02）。

### D7 — 冻结哈希模块 `tests/contract/test_expression_compatibility.py` 需为被改文件追加行

`research.md` § R3 实测：三个被改的 `SKILL.md` 在 `ALLOWED_POST_BASELINE_CHANGES` 的补集（冻结哈希）里，登记机制是活的（`test_c5_non_wiring_files_keep_their_frozen_hashes` 通过，`WIRING_SKILLS` 恰为 `create-docs` / `humanize`）。实现期 MUST 追加三行 `reason` + `markers`（`markers` 取该技能新判定里唯一的字面，如 owner 路径或判定 id），MUST NOT 放宽哈希清单本身、MUST NOT 删除或跳过断言。

**本阶段实测补一条 R3 未覆盖的事实**（用于让实现期不踩）：该模块还有两处会**被本特性触发**的既有登记面——

1. `RENAMED_SKILL_REL = "skills/external/coaching-skills/SKILL.md"`：`_retired_skill_register` 断言「清单里恰好一个路径从磁盘消失」。`coaching-skills` 在**机制/策略侧**零加载、**文件必须原样存在**，所以该断言不受影响——它是「`coaching-skills` 必须仍在磁盘」的机械证据，实现期 MUST NOT 移动或删除该目录。**scope update 更正**：该路径现在**会**被第二个能力改写（SR-06），因此它**必须**作为新键追加进 `ALLOWED_POST_BASELINE_CHANGES`（下一条），否则 `test_c5_non_wiring_files_keep_their_frozen_hashes` 会转红——这正是「零改动」读法被收紧后必须同趟处理的登记面。
2. `skills/internal/run-skills/SKILL.md` 已是 `ALLOWED_POST_BASELINE_CHANGES` 的一条既有键（Feature 078 的路由指针）。实现期 MUST **更新这条既有键**（把 `reason` 扩成同时含引用归一化接线，并把新接线行的唯一字面并入 `markers`），MUST NOT 追加第二条同名键、MUST NOT 删除该键。

**scope update 的冻结面追加清单（恰 5 行，封闭）**：`skills/external/{create-skills,improve-skills,merge-skills,coaching-skills}/SKILL.md` 四行新增（`reason` 注明所属 FR 组，`markers` 取该技能新接线里**唯一的**字面：`shared/definitions/mechanism-policy-definitions.md` 或 `shared/definitions/skill-reference-definitions.md`，视该技能实际加载哪一侧而定）+ 上面第 2 条的**更新**一行 = 5 处登记面。`references/*.md` 与 `create-skills/references/mechanism-policy-check.md` 不在冻结清单内（清单只覆盖 `SKILL.md` 与已登记的少数文件），无需追加；这一点由 `test_mechanism_policy_guard.py` 与 `test_skill_reference_consumers.py` 的逐字节断言覆盖（它们落在 GM-03 / GM-11 的允许差异集内，属**允许变化**而非冻结）。`WIRING_SKILLS`（`create-docs` / `humanize`）与哈希清单本身 MUST NOT 改动。

两份 `references/` 的层归属：`loop-playbook.md`（`improve-skills`）与 `provenance-record.md`（`merge-skills`）**不在**该模块的冻结哈希清单内（清单只覆盖 `SKILL.md` 与已登记的少数文件），因此不需要追加行；这一点由 `test_mechanism_policy_guard.py` 的逐字节断言覆盖（它们落在 GM-03 的允许差异集内，属**允许变化**而非冻结）。

### D8 — 单包交付（估算 ≈ 36 任务 ≤ 80；不切片）

| 分组 | 自然任务估计 |
|---|---|
| Setup（目录/镜像基线确认、冻结清单登记面核对、两处 owner 起点核验） | 2 |
| Foundational A：机制/策略 owner 文档九个章节（OD-01…OD-10，含附录题集 ≥ 12 条） | 4 |
| Foundational B：技能引用 owner 定稿（GR-01…GR-10；起点已在工作树，按裁决 ① 修正顺序 + 补齐三处残留） | 3 |
| US1（`create-skills` § 6 + `references/mechanism-policy-check.md`） | 2 |
| US2（`improve-skills` § 2/§ 3 + `references/loop-playbook.md`） | 2 |
| US3（消费侧提示形态接线五处 + owner § Consumption Contract 复核） | 2 |
| US4（成员表 + 谓词 + 排除理由 + 命令面接线位） | 1 |
| US5（五个消费方的引用接线 5 处 + 8 处镜像路径串改为源路径） | 4 |
| 11 个契约测试模块（6 + 5；含 GM-07 每模块一条反例断言）、1 份矩阵 fixture、矩阵驱动源 `tests/contract/skill_reference_matrix.py` | 12 |
| 镜像再生成 + 两处 `--check` | 1 |
| 测量与收口（SC-001…SC-009 样本记录、`ALLOWED_POST_BASELINE_CHANGES` 5 处登记面、`skill-shape` before/after 记录） | 3 |
| **合计** | **≈ 36** |

低于 80 的任务上限（`decomposition-check.py --mode plan` 的 `task_ceiling`），且 FR 侧落在 `fr_count=30 / fr_ceiling=60`，故 **`single-package`**：不声明切片、不丢弃任何 FR / SC；`tasks.md` 是一张约 36 行的清单。**撤回记录**：原早改按「30 FR == 30 上限、零余量」切成 `083a`/`083b` 两片，该前提在预算校准（FR 上限 30 → 60）后消失（clarify 裁决 ③），本阶段据此撤回，§ Scope Snapshot / § Slice 083b 两节删除、`feature-ref.md` § Slices 同步改写为单包。**回退条件**：若 `/speckit.tasks` 自己的分解检查给出 `split-required`，按「US1 → US2 → US3 → US4 → US5 的**用户故事自然顺序**」切片（不是按能力切），且两次切片的 FR 集必须**互斥且并集为全集**——而不是压缩任务粒度。

**为什么不是「两个能力各一包」**：两个能力共享同一范围判据（C1）、同一消费面（五个元技能）、同一批文件（`create-skills` / `improve-skills` / `merge-skills` 三份 `SKILL.md` 同时被两侧改写）与同一份冻结清单登记面。按能力切会把**同一批文件**拆进两个交付单元，使 SC-003 的逐字节封闭集与 SC-007 的包含性扫描各要跑两次、且中间态两边都不成立——这正是单包的全部理由。

### D9 — glossary / framework-map / CHANGELOG 是计划期义务（登记，本阶段不写）

- `.specify/memory/glossary.md`：+1 词条 `机制/策略分离 (Mechanism–Policy Separation)`，Origin `user`、Status `proposed`（按 `shared/workflow/glossary.md` 的协议）。它是跨特性共享的**单文件注册表**，按本阶段「只提交本特性产物」的边界不写，也**不作为交付面**声明（clarify U4 的 overlap 裁决：083 只按协议追加一行、把它当共享注册表，交付声明只写 `framework-map.md` 里自己的那行）。
- `.specify/shared/definitions/framework-map.md`：既有 `| Shared definitions & conventions |` 行追加**两份** owner 的文件名——**不新增行、不新增目录**（C4；该文件不在 `sync-mirrors.py` 的 `MIRROR_PAIRS` 内，是本仓项目运行时产物，无框架源对）。
- `CHANGELOG.md`：implement 收口时 +1 条（frame: 两份 owner + 五条元技能判定/引用行 + 11 个契约模块 + 1 份矩阵 fixture）。

### D10 — 镜像与命令副本再生成

源码改动全部落框架源（`shared/`、`skills/`、`tests/`），然后恰两次再生成入口：`python3 scripts/python/sync-mirrors.py`（+ `--check`）与 `python3 scripts/python/regen-command-copies.py`（+ `--check`）。**本特性不改命令模板**，故命令副本预期**零变化**；`--check` 仍要跑，用来证明这一点（SW-06），并作为 `/speckit.skills` 仍是命令面这一事实的机械证据（SC-008 的标杆不受本特性影响）。`.specify/` 侧永不手改为主改动。**第二个能力的镜像面由同一入口覆盖**（FR-028）：owner 镜像与五份技能镜像一起再生成；`.specify/` 侧的 owner 文件**不得**被任何正文引用（D11 / SR-05），这只是「不进引用面」，不是「不进镜像面」。

### D11 — 技能引用两侧都**不新增脚本**；归一化由一个 test-only 的 stdlib 模块承载

`research.md` § R10–R14 的实测结论：归一化的每一步都是固定形态规则（trim、剥引号、剥标签、剥一段前缀、剥 `SKILL.md` / 尾 `/`、含 `/` 判通道、`/speckit.*` 集合归属、精确→不分大小写两轮匹配），全部可由一个纯函数逐行复算。**落点选择**：这个纯函数写进 `tests/contract/skill_reference_matrix.py`，**只被测试 import**，不进入 `scripts/`、不成为门禁、不新增命令（FR-029）。被否决的三个方案：① 写进 `scripts/python/`（成为第二个「框架可执行面」，与 A6 / C8 / FR-029 的「零新门禁」撞；且一个没有门禁挂点的脚本只会漂移）；② 只写进 `SKILL.md` 散文、测试按字面断言（**今天就是这个状态**，而 § R10 的探针证明散文里的顺序本身有缺陷、机器无法复算它）；③ 让每个消费方各实现一份（正是 SC-007 要禁止的复制）。保留的代价：这个模块**不是**运行时实现，元技能执行时仍按 owner 正文现场归一化——**测试与运行之间存在一次人读**，这是 GM-02 在引用侧的对应面，已在 § Measurement Plan 披露。

### D12 — 归一化顺序与三值输出：按 clarify 裁决 ① 落地，不重写既有正文

owner 文档当前六步顺序的缺陷已被 14 行探针钉住（`test-evidence/clarify-scope-update-fixture-probe.txt`：输出只有 NAME / PATH 两类，FAILURE 无法从过程里产生；`/improve-skills` 在步骤 2 被判为 PATH，永不到达步骤 3）。实现期 MUST 把步骤改成 **形态判定 → 去空白与一对包裹引号 → 剥一段 `skill:` 标签 → 剥一段 `@` 或 `/` 前缀（接受 `@/name`）→ 剥 `SKILL.md` / 尾 `/` → 通道判定 → 三值输出**，并补齐三处残留：

| 残留（clarify 交 plan） | 本计划的处置 | 条款 |
|---|---|---|
| `speckit.skills`（NAME）与 `speckit.skills/SKILL.md`（PATH）分类冲突 | 剥前缀与后缀**先于**通道判定，于是两种写法都收敛到同一个不含 `/` 的余值 → name 通道 → 命中 `/speckit.*` → **命令面**。这不是新增一类，而是把两个输入送进同一个出口 | GR-04 / GR-05 |
| name / path 通道集合未闭合 | 通道由**余值是否含 `/`** 单一判据决定（`/` 只可能来自未被剥掉的部分）；name 通道 **MUST NOT** 再对字符类另作断言（点号名合法，否则把本应报命令面的输入变成失败） | GR-04 |
| `run-skills`「名字可省扩展名」与名字通道不剥 `.md` 冲突（fixture R14） | 归一化**不剥** `.md`；`my-draft.md` 是 name 通道的一个名字，是否成立由位置阶梯结算。owner MUST 明写「省略扩展名是**结算约定**、不是归一化步骤」，从而两处归属不重叠；`run-skills` § 1 的位置阶梯**逐字节不改**（FR-022） | GR-04 / GR-09 |
| 形态判定（cli / invocation）步骤的落点（C11 交给 plan） | 落 **owner 正文的第 1 步**（一条显式步骤 + 一张两形态差异表：invocation 剥前缀、cli 下 `@name` 走「零命中」失败类并增记「该形式在 CLI 形态下不可达」）；**同时**由 `skill_reference_matrix.py` 作为一个输入参数复算。两处不是双 owner：正文是规则 owner，程序是它的可复算投影（同 `data-model.md` 对 owner 的既有形态） | GR-02 / GR-06 |
| SC-006…SC-009 尚无测试（`tests/` 对 `skill-reference` 零命中） | 落在 `tests/fixtures/skill-reference/normalization-matrix.json`（矩阵）+ 5 个 `tests/contract/test_skill_reference_*.py`；矩阵以 clarify 的 14 行 fixture 为**起点**并扩到覆盖 SC-006 要求的全部形态（≥ 12 行下限，实际行数由 implement 冻结并写进证据） | GM-11 / GM-13 |

### D13 — 矩阵夹具落 `tests/fixtures/skill-reference/`（既有根下的新子目录，登记理由）

`tests/fixtures/` 下已有 **12** 个按特性命名的夹具目录（`ls -d tests/fixtures/*/` 实测，2026-11-05：`acceptance-hardening/`、`bilingual/`、`coaching/`、`docs_command/`、`expression_line/`、`flow_class/`、`humanize/`、`sanitize/`、`sdd_loop_efficiency/`、`skill-layout/`、`teams/`、`todo-workspaces/`；`__pycache__` 不计），本计划的 `skill-reference/` 是第 **13** 个，属**既有根下的新子目录**，不新增目录根（FR-029 / Principle XVII）。为什么不能像 D6 那样用 `tmp_path` 就地造：SC-006 的**分母就是这份矩阵本身**（FR-030 要求「真实仓内位置」，MUST NOT 以散文或一次性运行记录冒充），而它同时被两个模块读（矩阵复算与失败语义断言），一次性构造成本高于一份受版本控制的 JSON。被否决的方案：把矩阵塞进 `data-model.md`（判据形态与夹具数据混在一份文档里，且 JSON 才是可逐行复算的载体）。

### D14 — 证据与测量：三个 SC 的载体重排，一个不新增

- SC-006 / SC-008 / SC-009 的主面全部是可判测试（`test_skill_reference_matrix.py` / `..._command_surface.py` / `..._failures.py`），证据 = 一次真实运行的逐字输出；
- SC-007 的主面是可判测试（`test_skill_reference_consumers.py` 的包含性扫描），证据 = 扫描报告的命中路径与行号；
- **不新增**任何测量脚本或证据生成器：所有输出由 pytest 自身的 `-q` / `-v` 原文落盘（与 GM-08 的定向集同一条入口）。

## Complexity Tracking

N/A — the Constitution Check has no Fail and no Partial row; no violation needs justification.

## Phase 0: Research Review

Research 以独立文件记录（超出内联阈值且携带环境实测）：[`research.md`](./research.md) § R1–R9。本阶段由它决定的四件事：运行器与 `PYTHONPATH` 前缀前提（R1 → EP-001）、三个被改技能的既有体积债务（R4 → EP-003）、封闭集分母 575 与「守卫必须报计数」（R6/GM-04）、以及「零新脚本可兑现」的逐判定载体表（R7 → D2）。本阶段对 R3 做了一处**补测**并把结果写进 D7（`coaching-skills` / `run-skills` 在冻结清单里的真实位置），§ Inherited Blockers 的零行结论另行实跑三个源取证（同一节内）。

## Decomposition & Ceiling

**实测读数**（本轮实跑 `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/083-mechanism-policy-separation/requirements.md`，逐字输出存 `test-evidence/plan-scope-update-gates.txt`）：

```json
{"mode": "plan", "decision": "proceed", "measured": {"fr_count": 30, "task_count": null, "fr_ceiling": 60, "task_ceiling": 80}, "reasons": []}
```

- **FR**：30 条（FR-001…FR-030），**全部**落入本包，无一条被切片丢弃；30 ≤ 60，余量 30。
- **SC**：9 条（SC-001…SC-009），全部落入本包；其中 SC-001 / SC-002 / SC-005 的度量是人工样本（`test-evidence/`），SC-003 / SC-004 / SC-006 / SC-007 / SC-008 / SC-009 的主面是可判测试。
- **用户故事**：5 条（US1–US5），按 US1 → US2 → US3 → US4 → US5 的自然顺序推进；`create-skills` / `improve-skills` / `merge-skills` 三份 `SKILL.md` 同时承载 US1–US4 的判定接线与 US5 的引用接线，**一次改写两处落点**，不排两遍。
- **自然任务计数**：≈ 36（D8 的分组读数之和），低于上限 80。
- **结论**：`single-package`，无切片，无 FR / SC 丢弃。**回退条件**：`/speckit.tasks` 自己的分解检查若给出 `split-required`，按用户故事自然顺序切（互斥且并集为全集的 FR 集），而不是压缩任务粒度。

**被撤回的早改（SU-04）**：`58d3dc5b` 之后工作树里那两节（`## Scope Snapshot` 与 `## Slice 083b: Skill Reference Grammar`）写于 FR 上限仍为 30 时，其唯一前提是「30 == 30 零余量」。预算校准把上限提到 60 之后前提消失（clarify 裁决 ③），本阶段删除两节并把内容并入本节、D8、§ Design Decisions D11–D14 与 `feature-ref.md` § Slices。**被并入而非丢弃的事实**：第二能力的起点是工作树里的未提交实现（A11 / FR-027）、镜像全由 `sync-mirrors.py` 生成（FR-028 / D10）、零新增边界（FR-029）。**被彻底删除的一条**：原「083a 已钉的冻结哈希面与 083b 要改的 `SKILL.md` 相交，其处理留给 083b plan」——两个能力已在同一份 plan 里，该交集不再跨越阶段边界，处置落在 D7 的追加清单。

## Measurement Plan

测量方法、样本/夹具与证据落点的条款 owner 是 `contracts/guard-and-measurement.contract.md`（GM-01…GM-09 机制/策略侧；GM-10…GM-14 技能引用侧）与 `contracts/owner-document.contract.md`（OD-09 题集）、`contracts/skill-reference.contract.md`（GR-06 矩阵、GR-04 三值）。本表只把每条 SC 指向那组条款，**不复制**它们的表格。

| SC | Path | 测量方法（指向条款） | 样本 / 夹具 | 证据落点 |
|----|------|----------------------|-------------|----------|
| SC-001 | final | 两位 fresh-context 只读判定者**仅凭 owner 文档**对附录题集逐条作答，比较一致率（OD-09 + GM-02；题集可解析性由 `test_mechanism_policy_decidability.py` 守） | owner § Worked Examples 的封闭题集（≥ 12 条，`data-model.md` E-7 / V-21） | `test-evidence/sc-001-<date>.txt`（题集快照 + 两份结论 + 一致率） |
| SC-002 | final | 一个受支持宿主上，改动前/后各跑一次纳入的元技能流程；比较检出（含文件与位置）与误报（GM-09） | 误置样本 ×2（策略误置 / 机制误置）+ 正确分层样本 ×2（GM-09） | `test-evidence/sc-002-<date>.txt`（宿主名 + 版本原文 + 输入草稿路径 + 输出原文 + 逐样本 verdict 表） |
| SC-003 | final | 基线[[STR-002]] 与 HEAD 的逐字节补集断言 + 路径集断言 + `compared=575` 形态的计数（GM-03 五要件 / GM-04 / GM-07 反例） | 允许差异集 = `data-model.md` § GM-03 的唯一路径落点（18 条登记；**比较单元内 8 条** = 2 新增 + 6 改写，单元外 10 条为 `tests/` 下的新模块与矩阵 fixture） | `tests/contract/test_mechanism_policy_guard.py`（可复算）+ `test-evidence/sc-003-<date>.txt`（一次真实运行的逐字输出） |
| SC-004 | final | 主面 = `tmp_path` 内的路径集 + sha256 快照前后比较与补齐后产物哈希比较；支撑面 = 一次宿主实录（GM-05 两个面） | `tmp_path` 造的假技能 + 假运行目录（无持久夹具，D6） | `tests/contract/test_mechanism_policy_missing_policy.py` + `test-evidence/sc-004-<date>.txt`（支撑面，含宿主名 + 版本） |
| SC-005 | supporting | 一位**未参与本特性**的读者仅凭 owner 文档作答同一题集，正确数 vs 题集全集（OD-09） | 同一份封闭题集（与 SC-001 共用分母，MUST NOT 另起一份） | `test-evidence/sc-005-<date>.txt`（作答记录，可复算：同一题集重测） |
| SC-006 | final | 用 `tests/contract/skill_reference_matrix.py`（stdlib-only 纯函数，D11）逐行复算 `tests/fixtures/skill-reference/normalization-matrix.json`，**每一行**比对其 `expect` 三值判定与「原始 + 归一化」成对形态；分母 = fixture 行数（≥ 12），任一行不匹配即失败（GR-03 / GR-06 / GM-13） | 矩阵 fixture 本身；起点 = clarify 的 14 行探针（`test-evidence/clarify-scope-update-fixture.json`），扩展覆盖 SC-006 点名的全部形态 | `tests/contract/test_skill_reference_matrix.py` + `test-evidence/sc-006-<date>.txt`（逐行结果原文 + `rows=N matched=N failed=0` 形态的计数） |
| SC-007 | final | ① 逐份读五个消费方 `SKILL.md` 的接线行，断言**每份恰一条**指向 [[STR-004]] 的**源路径**引用、且只声明自己的参数（SR-01…SR-06）；② 确定性全仓扫描：对 `skills/` 源树全部 `SKILL.md` 计数「复制了归一化步骤或失败表条目」的命中（GM-12 的包含性声明五要件：基线参照物 / 比较单元 `skills/**/SKILL.md` / 允许差异集三类 / 补集断言「除 owner 外零份」/ 未定义聚合词清零） | 五份被测文件 + 扫描分母 = `skills/` 源树 `SKILL.md` 全集（镜像层不计入，由 `sync-mirrors.py --check` 另证） | `tests/contract/test_skill_reference_consumers.py` + `test-evidence/sc-007-<date>.txt`（命中路径与行号 + 分母计数） |
| SC-008 | final | 命令面正例：`speckit.skills` 与 `/speckit.skills` 归一化后判定类 = `command-surface` 且指向命令模板；**负例**：一个与命令同形但不是命令的名字（例 `skills.external`）或其镜像写法，证明判定不是「带点/带斜杠一律当命令」（GM-11 正负例成对规则） | 矩阵里 SC-008 的 `surface` 子段（正例 ≥ 2 行 + 负例 ≥ 1 行） | `tests/contract/test_skill_reference_command_surface.py` + `test-evidence/sc-008-<date>.txt` |
| SC-009 | final | 四类失败（零命中 / 越界路径 / 目录无 `SKILL.md` / 两层同名）各一条断言，每条同时断言**报告含原始与归一化标识**，并断言四类**互不串味**（越界不得报成零命中，GM-11 的 `failure_class` 互斥断言） | 矩阵里 SC-009 的 `failure` 子段（四类各 ≥ 1 行）+ `tmp_path` 造的两层同名树 | `tests/contract/test_skill_reference_failures.py` + `test-evidence/sc-009-<date>.txt` |

**引用侧的「测试 vs 运行」缺口（如实披露）**：`skill_reference_matrix.py` 是测试侧的可执行实现，元技能执行时仍按 owner 正文**现场**归一化（D11）。因此 SC-006…SC-009 证明的是「owner 正文所规定的过程可以被一台机器逐行复现且结果一致」，**不**证明每个宿主执行体真的照做了——后者只有 SC-002 那种宿主实录能证明，而第二个能力**没有**被排进宿主实录的测量面（它不需要模型判断，见 GM-14）。这一条按 GM-02 的同一条纪律写成显式缺口，而不是留白。

**职责划分不重不漏（与 requirements 的分工对齐）**：requirements 把 `tests/contract/skill_reference_matrix.py`（确定性实现）与 `tests/fixtures/skill-reference/normalization-matrix.json`（期望值）记为**表外已知项**（它们不是量级指标，故不进 § Runtime Stack）；本计划把 `test_skill_reference_consumers.py` 的全仓扫描作为 SC-007 的可执行载体。三者的落点都在 `tests/` 下，且都不新增运行时能力——这也是 § Runtime Stack 五行**不需要**因第二个能力而新增行的原因。

**定向集与基线（TEST BUDGET 的 plan 侧读数）**：本阶段是 docs-only，`plan.md` 与六个附属产物都不落在 `test_files` 的选中面内，故按 `not-run-docs-only` 记录（六项缩减字段，`test-evidence/plan-scope-update-stage-status.jsonl`）。实现期的定向集命令与基线（`892 passed` / 失败名集为空）已在 `research.md` § R2 与 `test-evidence/plan2026-11-05-baseline.txt` 逐字记录，判据是**差集**而不是绝对全绿（GM-08）。

## Post-Generation Quality Gate

执行状态与前提的 owner 是 [`quickstart.md`](./quickstart.md)：每个场景标注 `run`（本阶段实跑过）或 `deferred`（依赖尚未落地的产物，并逐条列出它假设的 flags / ID 形态 / 文件位置 / 工具行为）。

**本阶段实际跑过的（`run`）**：

| 场景 | 覆盖 | 实测结果 |
|------|------|----------|
| S1 — 运行器与测试入口 | EP-001 | `Python 3.14.6` / `pytest 9.2.0` / `git version 2.54.0 (Apple Git-157)` |
| S2 — 定向集基线 | GM-08 的基线 | `892 passed`，失败名集为空（`env -u PYTHONPATH` 前缀） |
| S3 — 镜像与命令副本基线 | EP-005 / GM-06 | 两条 `--check` rc 0；`shared/` 62 文件 |
| S4 — SC-003 封闭集预演 | EP-004 / GM-04 | `compared=575 complement=570 allowed_in_unit=5 frozen_mismatches=0` |
| S5 — 元技能形状与红线（before 半） | EP-003 | 三份 `skill-shape.py` rc 10；三份 `redline-check.py` rc 0 |
| S9 — 阶段门 | 本阶段门 | 见 `test-evidence/plan2026-11-05-plan-gates.txt`（本阶段逐字输出，含 exit code） |

**本轮（plan scope update）新跑过的（`run`）**：

| 场景 | 覆盖 | 实测结果 |
|------|------|----------|
| S3（复跑） | EP-005 / GM-06 | `sync-mirrors.py --check` 六对全 `ok`、`shared/` **63**（并发 owner 镜像已生成且 `cmp` 通过）；`regen-command-copies.py --check` rc 0 |
| S9（复跑） | 本阶段门 | `pre-analyze-check.py --stage plan` → `decision=pass, errors=0`（advisories=127，全部为 missing-path 的 to-be-created 产物，允许；tasks.md 落地后的 repair pass 复跑读数，见 quickstart S9）；`decomposition-check.py --mode plan` → `proceed, fr_count=30, fr_ceiling=60`；`overlap-check.py --repo .` → 18 条，全部 `same-path`、全部对已完成特性（3 条 `shared/workflow/glossary.md`〔029 / 044 / 051〕+ 4 条 `skills/internal/run-skills/SKILL.md`〔057 / 059 / 062 / 063〕+ 三份 `SKILL.md` 各 3 条〔059 / 062 / 063〕+ 2 条 `skills/external/coaching-skills/SKILL.md`〔078〕），按状态脊 § Overlap adjudication 原样记录，不删真实交付路径；`validate-requirements.py` → `status ok`。逐字输出与逐路径分解：`test-evidence/plan-scope-update-gates.txt` |
| S10 — 归一化顺序探针的读数复核 | D12 / § R10 | 直接消费 clarify 已落盘的 `test-evidence/clarify-scope-update-fixture-probe.txt`（14 行、两类输出），本阶段**不重跑探针代码**（其时的一次性脚本不在仓内）；改用「读其逐行输出 + 与声明顺序逐条对账」的静态复核，结论一致：当前六步顺序产生 NAME / PATH 两类，无法产生 FR-030 的第三值 |
| S13 — 五消费方的引用坐标实测 | SU-02 / GR-08 | `git diff` 实测 5 份 `SKILL.md` 共 **8 处** `skill-reference-definitions.md` 引用串，**全部**是 `.specify/` 镜像路径；`cmp shared/definitions/skill-reference-definitions.md .specify/shared/definitions/skill-reference-definitions.md` 一致（说明只是引用坐标错，内容未漂移） |
| S14 — 引用侧测试现状 | SC-006…SC-009 | 全仓对 `skill-reference` 的检索在 `tests/` 下**零命中** → 引用侧测试**尚不存在**，属本计划的真正新增工作量（不是「核验已有测试」） |

**留给 tasks / implement 重测的（`deferred`）**：S5 的 after 半（被改文件的新体积与红线判定）、S6（SC-004 零写入模块）、S7（SC-002 宿主实录）、S8（SC-001 / SC-005 题集作答）、S11（SC-006 矩阵首次全绿）、S12（安装态下「相对框架根」能否把源路径解析到镜像——EP-007(a) 的唯一闭合点）。每条 `deferred` 场景在 `quickstart.md` 各节末尾的 **Premises** 里写清它假设的前提，供下一阶段重新测量而**不是继承**。

## Phase 1: Design Artifacts Summary

Backfilled after the artifacts landed; every count below is read from the files, not from memory.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | 10 实体（E-1 Principle … E-7 Decidability Sample；E-8 Skill Reference … E-10 Failure Class）/ 34 条校验规则（V-1…V-34）/ 2 个封闭谓词（C1 元层、C2 引用接受形式）/ 1 张封闭成员表（`included` 3 / `excluded` 2 / `command-surface` 1）/ 3 条状态转移（SM-1 / SM-2 / SM-3）/ GM-03 允许差异集 18 行（其中属比较单元者 **8**：2 新增 + 6 改写；其余 10 行落在 `tests/`）/ 1 条归一化管线（NP-1…NP-8） |
| Contracts | [`contracts/`](./contracts/) | 4 份：`owner-document.contract.md`（OD-01…OD-10 + DR-001 追溯）、`skill-wiring.contract.md`（SW-01…SW-08 + 追溯，SW-05 已按 SU-01 收紧）、`skill-reference.contract.md`（GR-01…GR-10 + SR-01…SR-06 + 追溯）、`guard-and-measurement.contract.md`（GM-01…GM-09 机制/策略侧 + GM-10…GM-14 引用侧 + 追溯） |
| Quickstart | [`quickstart.md`](./quickstart.md) | 14 个场景（S1–S14）；`run` 10 / `deferred` 6（S1–S4 / S9 / S10 / S13 / S14 共 8 个整段 `run`，S5 前后各半计 2，合计 10；S6 / S7 / S8 / S11 / S12 共 5 个整段 `deferred` + S5 的 after 半 = 6。S10 / S13 / S14 为本轮新跑，S11 / S12 为本轮新增的 `deferred`；每节含命令逐字、判据与 Premises） |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | Feature 083 绑定（完整名：元技能治理：机制/策略分离与技能引用归一化）+ 交付面（新增 3〔2 owner + 1 技能自有资源〕+ 改写 7 + 新增测试 11 + 矩阵 fixture 1 = 22；另列计划期义务 3 / 再生成入口 2 / 明确不新增 7 类）+ 5 行冻结登记面 + 单包 `Slices` + `glossary.md` 非交付面的 overlap 注记 |
| Research | [`research.md`](./research.md) | R1–R9（机制/策略；R3 由 plan 补测了冻结清单的排除成员位置，结论落在 D7）+ R10–R15（技能引用，scope update 新增；R10 归一化顺序探针读数、R11 引用坐标、R12 测试现状、R13 消费方接线点、R14 镜像口径、R15 承重门槛） |

**Drift from the Phase 0 expectation**: 一处已披露的纠正——`research.md` / `contracts/skill-wiring.contract.md` / `contracts/guard-and-measurement.contract.md` 把基线证据路径写成 `test-evidence/plan-baseline.txt`，而该文件在上一 attempt 的 turn budget 耗尽时**未曾落盘**（`ls test-evidence/` 实测无此文件）。本阶段把它就地纠正为本阶段实际写入的 `test-evidence/plan2026-11-05-baseline.txt`（见 DC-001），并把 S2 的基线重新实跑一次以保证该文件与其引用一致。

**Drift from the scope update**: 三处（SU-01 范围矛盾 / SU-02 镜像路径 / SU-04 切片前提消失）已按纠正处置并披露，一处（SU-03 分类冲突）按裁定记录在 D12——全部见 § Scope Update Record。本轮收尾 pass 另发现两处装配错并按纠正处置：DC-006（「比较单元内」计数 12 → 8，登记表 18）与 DC-007（技能引用测试模块名与 GM 编号的陈旧引用）。

**Phase 1 收尾状态（本轮）**：上表五份产物与本文件同趟对齐——`contracts/skill-reference.contract.md` 为本轮**新建**（GR-01…GR-10 + SR-01…SR-06 + 追溯），`contracts/guard-and-measurement.contract.md` 追加 GM-10…GM-14（GM-01…GM-09 原文未改），`quickstart.md` 补齐 **S1–S14** 的逐例条目（含本轮新增的 S11 / S12 `deferred` 与 S10 / S13 / S14 `run`），`feature-ref.md` 改为单包口径与本节的计数，`data-model.md` 的模块名与计数同趟纠正。

## Delivery Review (DR-001 覆盖复核 + DC 披露)

**DR-001 — 30 条 FR 的落点覆盖（本阶段自检，防「改了但没覆盖某条 FR」）**：

| FR | 落点 | FR | 落点 |
|----|------|----|------|
| FR-001 | owner OD-01 / OD-07 | FR-010 | owner OD-07（V-18 / V-19 / V-20） |
| FR-002 | owner OD-02 / OD-03 / OD-04 | FR-011 | SW-05 / SW-06 / SW-07 + `test_mechanism_policy_guard.py` |
| FR-003 | owner OD-03 | FR-012 | SW-01 + `references/mechanism-policy-check.md` |
| FR-004 | owner OD-05 + `test_mechanism_policy_ownership.py` | FR-013 | SW-02 |
| FR-005 | owner OD-06 | FR-014 | SW-03 / SW-05 + owner 成员表 |
| FR-006 | owner OD-06 | FR-015 | owner OD-01 / OD-08 + `test_mechanism_policy_ownership.py` |
| FR-007 | owner OD-06（两类措辞与后续动作可区分） | FR-016 | OD-05 / OD-09 + GM-01（零新脚本）+ GM-03 |
| FR-008 | SW-04 + OD-06（读-判-停，副作用前） | FR-017 | `requirements.md` 头部类别声明（本阶段 MUST NOT 修改该文件） |
| FR-009 | SW-01 / SW-02 | FR-018 | owner OD-02（两个 canonical 词逐字） |
| FR-019 | GR-01（owner 声明它拥有 / 不拥有什么）+ GR-09（不拥有位置阶梯） | FR-025 | GR-03（成对报告：原始 + 归一化 + 判定类）+ SR-01…SR-06 的接线行 |
| FR-020 | GR-02（封闭接受形式集合，每行带示例与含义）+ `test_skill_reference_grammar.py` | FR-026 | SR-01…SR-06（五个消费方各只声明参数 + 一条源路径引用；`create-skills` 的「只命名不解析」特例在 SR-02 写明）+ `test_skill_reference_consumers.py` |
| FR-021 | GR-03（确定性顺序 + 输出形态：不含被剥掉的前缀/后缀、无网络、无交互） | FR-027 | GR-07（起点 = 工作树未提交实现；核验结论与缺口清单落 `test-evidence/`）+ § Scope Update Record 的 SU-02 / SU-03 |
| FR-022 | GR-09（位置阶梯以路径引用交出）+ `run-skills` § 1 第 1–4 步逐字节断言 | FR-028 | GM-14（镜像由 `sync-mirrors.py` 再生成，`--check` 证明，不手改、不作为源提交） |
| FR-023 | GR-05（消歧四条 a–d）+ GR-04（通道判定，FR-023(b) 的命令面出口） | FR-029 | GR-10（零新命令 / 零新门禁 / 零新目录根 / 零新环境变量；接受形式的增长是一次 owner 修订） |
| FR-024 | GR-05（失败语义表四类，每类的必需报告项逐项可核对、关闭不降级）+ `test_skill_reference_failures.py` | FR-030 | GR-04（三值封闭 + 无第四值）+ GM-13（矩阵落在真实仓内位置 `tests/fixtures/skill-reference/normalization-matrix.json`） |

**DC-001 — 基线证据路径纠正（RP-1 明显近似错，已就地修复并披露）**：`research.md` § R2 与两份契约的 4 处引用写作 `test-evidence/plan-baseline.txt`，该路径在上一 attempt 未落盘。恰有一种读法与已记录意图一致（意图是「本阶段实测的定向集基线」），本阶段以 `env -u PYTHONPATH bash scripts/bash/run-tests.sh …` 重跑该基线并写入 `test-evidence/plan2026-11-05-baseline.txt`，同时把 4 处引用改为该路径。未改动基线的**内容**（`892 passed`、失败名集为空与上一 attempt 的读数一致）。

**DC-002 — `run-skills` 的真实路径（RP-1 路径近似错，已就地修复并披露）**：requirements § Constraints C1 把 `run-skills` 与 `skills/external/` 同段提及，实际文件在 `skills/internal/run-skills/SKILL.md`。恰有一种读法（C1 按**流程**裁定，从不按目录裁定），本计划的守卫与结构不变量按真实路径写；谓词与成员表**未改一行**（改谓词会触发 C1 末句的「全表重算」义务，本阶段不触发）。

**DC-003 — `## Inherited Blockers` 读数形态纠正（RP-1 装配错，已就地修复并披露）**：本文件初稿在该节先放一张「三源抽取读数」表、再放处置表；`pre-analyze-check.py --stage plan` 实测把前者读成 `row-1`/`row-2`/`row-3` 三条 `inherited-blocker` 且 Disposition 为空 → `decision=fail, errors=3`（守卫的 `section_rows()` 取该节**第一张**表）。恰有一种读法与已记录意图一致：意图是「处置表」，读数是证据不是处置；且零行结论本身不构成任何待处置项（`.specify/memory/features/083.md` 无继承阻塞记录，三源实测零行）。故把读数改写为列表、把空处置表改写为一句零行结论，语义未变、守卫复跑 `decision=pass, errors=0`。

**DC-004 — `## Decomposition & Ceiling` 读数形态（本轮，装配错，已就地纠正并披露）**：本节初稿沿用上一版的「引用一段 `decomposition-check.py` 输出」写法，把 `fr_ceiling` 写成 30（那是预算校准**前**的读数）。本轮实跑输出为 `fr_ceiling=60`。恰有一种读法与已记录意图一致（意图是「本阶段实测的读数」），故把本节的数字整段替换为本次的逐字 JSON，并把证据指针改为 `test-evidence/plan-scope-update-gates.txt`。

**DC-005 — `shared/` 镜像计数（本轮，陈旧读数，已就地纠正并披露）**：`## Mirror Obligations` 与 S3 行写作 `shared/` 62 文件并把「62 → 63」当作**将来**的移动；本轮实跑显示并发 owner 文档的镜像**已经**生成，计数**已是 63**。恰有一种读法与已记录意图一致（基线是「实测值」而非「期望值」），故就地改为 63 并把「不得钉死计数」的理由从「将来的移动」改为「已经发生的移动」。

**DC-006 — 允许差异集「比较单元内」的计数（本轮，对前一 attempt 的纠正，已披露）**：§ Measurement Plan 的 SC-003 行、§ Scope Update Record 的变更台账与 § Scope Update Record 的 SU-01 行都把「comparison-unit 内的允许路径」写成 12（前一 attempt 另把登记表全量写成 24），而 `data-model.md` § GM-03 第 1–8 行（单元内 2 新增 + 6 改写）与第 9–18 行（单元外，`tests/`）给出的实测值是 **8 / 18**。12 这个数把「单元内 8」与「`SKILL.md` + 矩阵」混成一句，属装配错。恰有一种读法与已记录意图一致（`data-model.md` 是路径的唯一落点、`contracts/` 只陈述计数），故本阶段改为 8 / 18（登记表），`contracts/guard-and-measurement.contract.md` GM-03 要件 3 与 `data-model.md` 的 Census 同趟对齐。

**DC-007 — 技能引用测试模块名与 GM 编号的陈旧引用（本轮，装配错，已就地纠正并披露）**：`data-model.md` E-8 / E-10 与 § GM-03 第 18 行、`contracts/skill-wiring.contract.md` SW-05 的守卫形态引用了两个**并不存在**的模块名（`test_skill_reference_owner_doc.py` / `test_skill_reference_wiring.py`）与一句未定义的 GM-11 半句；`plan.md` § Phase 1 摘要又把 GM-01 / GM-11 的划分写成「`test_skill_reference_*` 五个」而漏掉 test-only 辅助。恰有一种读法与已记录意图一致（`plan.md` § Project Structure 与 § Measurement Plan 的模块表是实测落点），故统一改为 `test_skill_reference_{grammar,consumers,failures}` 等真实模块名，并在 § Summary 补一句「另有 1 个 test-only 辅助」。

## Constraints & Assumptions 记录位置

本阶段为访谈式问题自行的裁决（无向用户提问）落四处：`research.md` § R1–R15 与 § 未决与交下一阶段（实测结论与可行性）、`## Design Decisions` D1–D14（含被否决的替代方案）、`## Decision Tensions` T-001…T-004（承重决策的对立面、判别证据与重开条件）、以及本文件的 EP-001…EP-007（执行前提及其证据；EP-007(a) 记 `unverified` 并给出闭合任务）。十条就地纠正 / 裁定披露：DC-001 / DC-002 / DC-003（`58d3dc5b` 阶段）+ DC-004 / DC-005 / DC-006 / DC-007 + SU-01 / SU-02 / SU-04（本轮，见 § Scope Update Record 与本文件 § Delivery Review）。
