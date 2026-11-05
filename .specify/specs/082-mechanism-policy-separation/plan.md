# Implementation Plan: 机制/策略分离（Mechanism–Policy Separation）

**Branch**: `082-mechanism-policy-separation` | **Date**: 2026-11-05 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `082-mechanism-policy-separation` → Feature 082 机制/策略分离（Mechanism–Policy Separation）
**Input**: Specification from `.specify/specs/082-mechanism-policy-separation/requirements.md` (clarified 2026-11-05; 18 FR / 5 SC / 3 STR / A1–A10 / C1–C8 / Runtime Stack 5 行）

## Summary

把「机制/能力」与「策略/职责」的归档边界立成一条一等原则，并让它**只经由元层**生效：一个 owner 文档定义边界，三个元技能在**既有**步骤里加一条同源判定，六个契约测试把形态钉成可判事实。技术路线：

- **1 个 owner 文档**：`shared/definitions/mechanism-policy-definitions.md`（[[STR-003]]）——两层的判别口径、双向边界测试与成员表、两类误置症状、归档规则、消费侧提示形态、元层谓词与封闭成员表、与相邻 owner 的边界、附录题集（`contracts/owner-document.contract.md` OD-01…OD-10）。
- **3 个元技能接线**：`create-skills` § 6（收尾校验，SW-01）、`improve-skills` § 2/§ 3（调研问题 + 候选类别，SW-02）、`merge-skills` § 5/§ 8（前置判断 + 验证项，SW-03）。每条判定 = **一行判定语 + 一个 owner 路径引用**（C5 / FR-015）。
- **1 个 create-skills 自有 reference**：`skills/external/create-skills/references/mechanism-policy-check.md`（判定步骤 + 两类误置的定位方法，≤ 12 行，SW-01）。
- **6 个契约测试模块**：`tests/contract/test_mechanism_policy_{owner_doc,ownership,skill_wiring,guard,missing_policy,decidability}.py`（GM-01），承载 SC-001/SC-003/SC-004/SC-005 的可判部分与 SC-002 的形态前置。
- **零新增**：零新增命令、零新增门禁脚本、零新增目录根、零新增环境变量、零新增配置键（A3 / A5 / A6 / C4 / C8 / FR-011 / FR-016）。
- **单包交付**：18 FR / 5 SC，自然任务估计 ≈ 21 < 40，不切片（D8）。

判定的写面与判定面刻意分离（GM-02）：**语义**判定（这段文字归哪一层）只由人/模型做，落 SC-001 双判定者与 SC-002 流程实录；**形态**判定（章节存在、字面存在/不存在、字节相等、题集可解析）才进 pytest。`research.md` § R7 实测了这个分工的每一个载体，结论是「零新脚本」可兑现而无需牺牲可判定性。

## Technical Context

**Language/Version**: Markdown（owner 文档 / 技能正文 / 合同文本）+ Python 3（**仅既有的** pytest 契约测试；不新增依赖、不新增引擎）。实测解释器 `CPython 3.14.6`（`scripts/bash/run-tests.sh` 解析到的 `.venv/bin/python`），`pyproject.toml` 的 `requires-python = ">=3.8"` 不变、不新增 pin。
**Primary Dependencies**: 既有引擎 `scripts/python/sync-mirrors.py`（镜像再生成）、`scripts/python/regen-command-copies.py`（按工具命令副本）、`.specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py`（阶段门）；既有技能脚本 `skills/external/improve-skills/scripts/{skill-shape,redline-check}.py`（被改技能的体积与红线判定）；运行时 `git`（SC-003 的逐字节比较与漂移守卫）。
**Storage**: 无数据库、无服务、无运行时状态。判定输入是 Markdown（owner 文档、四个技能文件、合同文本）；证据落 `<spec-dir>/test-evidence/`（`plan2026-11-05-plan-gates.txt`、`plan2026-11-05-baseline.txt`、`plan2026-11-05-stage-status.jsonl`、SC 各面的测量记录）；无新增数据文件、无第二套分类数据文件（FR-016）。
**Testing**: `env -u PYTHONPATH bash scripts/bash/run-tests.sh …` → `pytest 9.2.0` on `CPython 3.14.6`（`env -u PYTHONPATH` 是本机的运行前提，见 EP-001 与 `research.md` § R1）；基线判据是**定向集失败名差集**而不是绝对全绿（GM-08）。
**Target Platform**: 任何受支持的 agent 宿主（`docs/reference/cli/supported-agent-tools.md` 的 roster，`AGENT_CONFIG` 为准）。仓内可判定的部分只要求 POSIX shell + `python3` + `git`；SC-002 需一个受支持宿主执行真实元技能流程（EP-002）。
**Project Type**: single（框架源码 + 自举运行时双帽：改 `shared/`、`skills/`、`tests/`，`.specify/` 同名文件由 `sync-mirrors.py` 产出；命令模板零改动）。
**Performance Goals**: 无吞吐目标。六个新契约模块的读盘面是 1 份 owner 文档 + 4 个技能文件 + 1 个基线树清单，整组应在秒级完成；owner 文档新增文本走「一行判定 + 路径引用」形态，不把判据表复制进四个技能（C5）。
**Constraints**: 零新脚本 / 零新命令 / 零新门禁 / 零新目录根（A3 / A5 / A6 / C4 / C8）；owner 之外零复制（FR-015）；成员表之外的既有技能与全部命令模板逐字节不变（SC-003，[[STR-002]]）；策略缺失时零写入（SC-004）；不 push。
**Scale/Scope**: 4 条用户故事；18 FR / 5 SC；改动/新增源面 **13** 个（框架源 7：owner 文档 1 新增 + 技能文件 6；契约测试 6。逐类加总 = 13）+ 3 处**登记行**（`glossary.md` / `framework-map.md` / `CHANGELOG.md`，均为既有单文件注册表上的行，不是新文件、不是新目录）+ 2 类镜像再生成入口（`sync-mirrors.py` 覆盖前两组共 7 个文件，`regen-command-copies.py` 预期零变化）；自然任务估计 **≈ 21** < 40（见 § Decomposition & Ceiling）。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.15.0, 18 principles in file order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每条设计决定追到一个 FR：`contracts/owner-document.contract.md` / `skill-wiring.contract.md` / `guard-and-measurement.contract.md` 的可追溯性表是 FR→条款→测试的唯一映射；18 条 FR 全部有落点（DR-001 表）；被判据拒绝的替代方案留在 § Design Decisions 而不是消失 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 082（`feature-ref.md`，clarify 已落 `features.md` 082 行与 `features/082.md`）；本阶段只把状态从 `Draft` 解读为 **Planned**，`Implemented` 由 `/speckit.implement` 拥有；本阶段**不改**注册表（D9 把 `Last Updated` 更新留给 implement 收口） |
| III | Intent-Driven Development | ✅ Pass | Summary 先给「元层生效、零回溯改造」的用户可见差别，机制细节留给 `contracts/`；D1–D10 逐条记录被否决的替代方案 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 六个契约模块在 GM-01 里先于实现定义，且「红先行形态」被钉死（artifact missing 红，MUST NOT import/collection error 红）；GM-07 要求每个模块至少一条反例断言，防止绿得与命题无关；SC-001…SC-005 的采集方法在 § Measurement Plan 逐条声明 |
| V | AI Agent Integration Standards | ✅ Pass | 不动 `AGENT_CONFIG` / `_ASSISTANT_TIERS`、不动任何 agent 配置；命令模板零改动因而零按工具副本变化（`## Mirror Obligations` 第 2 行）；SC-002 的宿主取自既有 roster，不新造集成面 |
| VI | Continuous Quality & Observability | ✅ Pass | 关闭判据是**名字级差集**与可复算的记录，而不是「看起来绿」：SC-003 的守卫必须报出 `compared=575` 形态的计数（GM-04，实测 575），因为一个比较了 0 个文件的守卫会永远绿；既有债务（三个技能改动前就 exit 10，`research.md` § R4）按根因披露为 EP-003，不当作本特性的通过条件 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 只推进到 plan；Pre-Status-Flip Gate 的判据 owner 保持 `templates/feature-details-template.md` § Canonical Status State Machine，本文件只负责 plan 侧的产物与两张表 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 设计前实测而非引用记忆：`ALLOWED_POST_BASELINE_CHANGES` 的真实键集与 `WIRING_SKILLS`（`research.md` § R3）、`skill-shape.py` 三份 10 分（§ R4）、镜像基线六对（§ R5）、基线路径集 575（§ R6）、`PYTHONPATH` 报错原文（§ R1）。`coaching-skills` / `run-skills` 在冻结清单里的真实位置是**实测**并写进 D7 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 一份文档 + 四条判定行 + 六个测试模块；无运行时、无守护进程、无新依赖、无第二套门禁（D2 / SW-07）；被否决的「抽出确定性探针脚本」（D2）与「新增命令面」（D3）均记录理由 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新文件全部小写 kebab-case 且路径即语义：`shared/definitions/mechanism-policy-definitions.md`、`skills/external/create-skills/references/mechanism-policy-check.md`、`tests/contract/test_mechanism_policy_*.py`；不触保留名、不改 `SKILL.md` 的既有命名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | **两顶帽子已点名**：框架源 = `shared/`、`skills/`、`tests/`；`.specify/` 同名文件由 `sync-mirrors.py` 产出，MUST NOT 手改镜像。本特性自身按其新规则走：`data-model.md` 与 `contracts/` 只写机制（判定形态），路径、落点与样本位置一律写成参数或运行环境取值（`feature-ref.md` 末节自用声明） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用而不新建：`sync-mirrors.py`（镜像）、`regen-command-copies.py --check`（证明命令副本零变化）、`pre-analyze-check.py`（阶段门）、`skill-shape.py` / `redline-check.py`（被改技能体积与红线）、既有 `tests/conftest.py` 的 `tmp_path` 与 `_disable_git_config`；无一个既有 Tool 覆盖的能力需要新写代码，故本特性不产出新 Tool 记录 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Change Validation（元流程在作者侧拦误置）与 Reliable Delivery（策略缺失时在任何副作用之前停下），对应 `shared/guidelines/better-harness.md` 的五个工作环维度中的两项；证据纪律在 GM-02 落地——「配置了就存在」不等于「用起来了」，故 SC-002 记宿主实录而不是断言「判定已接入」 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 新 owner = `shared/definitions/mechanism-policy-definitions.md`（[[STR-003]]），其余位置只带路径 + 章节锚；九个「不复制」边界逐个落成机械断言（`contracts/owner-document.contract.md` OD-08 的邻接表 + `test_mechanism_policy_ownership.py`）；允许差异集只有 `data-model.md` § GM-03 一个路径落点，`guard-and-measurement.contract.md` 只陈述计数（GM-03 要件 3）；`§ Decision Tensions` 的表格形态不在此复制 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | owner § Consumption Contract 的提示形态是可复制的骨架（三行字段 + 一个示例），字段名用**用户可识别的名字**而不是内部变量名（OD-06）；面向人的产出（收尾报告、SC 证据说明）按 `shared/guidelines/user-facing-comprehension.md` 写作；机读字面量（`included` / `excluded` / `command-surface`）原样英文，翻译只发生在人的一侧 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 判定是二值（机制 / 策略），MUST NOT 引入严重度或「视情况」中间层（OD-02 / V-5）；本文件已把 `research.md` § R2 与两份契约引用到的 `test-evidence/plan-baseline.txt`（上一 attempt 未落盘）就地纠正：本阶段重跑该基线并写入 `test-evidence/plan2026-11-05-baseline.txt`，四处引用同趟改为该路径（DC-001）；既有债务（exit 10）记为 EP-003 而不是静默例外 |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | **不新增任何目录**（C4）：owner 进既有 `shared/definitions/`，引用文档进既有 `skills/external/create-skills/references/`，测试进既有 `tests/contract/`；`directory-governance.md` § 2 目录图因此零改动，`framework-map.md` 只需给既有 `definitions/` 行补一个文件（D9），临时产物落 `.specify/.tmp/` |
| XVIII | Grounded Naming | ✅ Pass | 名字全部来自已记录来源：用户原话逐字给出 `Mechanism–Policy Separation` 与 `机制/策略分离`（[[STR-003]]，用户指令优先）；owner 文件名与兄弟 `derivation-definitions.md` / `dogfooding-definitions.md` 同形；测试模块与既有 `test_mechanism_policy_*` 同族形态；不新造第三套名字（A2 / FR-018） |

**Gates Status**: ✅ All gates pass — no Fail, no Partial, no Complexity Tracking row.

**Re-check after Phase 1**: 2026-11-05, re-run against the landed Phase 1 artifacts (`research.md`、`data-model.md`、`contracts/` ×3、`quickstart.md`、`feature-ref.md`) — all 18 rows stay ✅ Pass. The two rows whose evidence moved: **IV**（六个模块的「红先行形态」已由 GM-01 钉死，且 GM-07 补了反例断言）与 **XIV**（九个 N-xx 边界从散文变成机械断言，允许差异集收敛到单一路径落点）。

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md` — one pointer, read from the repository root; this section MUST NOT restate the owner's criteria table, rejection list or threshold table.*

Fields: `decision`, `antithesis`, `binding_constraints` (with `pole_a` and `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; record identifier `tension_id` (`T-NNN`).

`research.md` § R9 实测了门槛：三条触发（跨团队、高爆炸半径、触及宪法 MUST）全部成立，故本计划记录 **T-001 … T-003**。

### T-001 — owner 文档是唯一判据载体，元技能只带「一行判定 + 路径」

- **decision**: 判据、成员表、症状表、提示骨架、题集全部只住在 `shared/definitions/mechanism-policy-definitions.md`；三个元技能各加**一行**判定语 + 一个 owner 路径引用，`create-skills` 的定位方法落它自己的 `references/mechanism-policy-check.md`（≤ 12 行）。元技能正文 MUST NOT 内联判据表或症状全表（SW-01）。
- **antithesis**: 把判据表直接写进三个元技能正文（每个技能自带一份可读的判定清单）。当元技能的读者几乎不会打开被引用的文档、而判据表足够短时它更优——Agent 执行时少一次读盘，判据就在眼前。
- **binding_constraints**:
  - pole_a: 判据只有一份——四份副本必然漂移，而漂移在「作者走了哪条路」这种只落产物不落日志的流程里不可见（Principle XIV 的失效面）。
  - pole_b: 判定必须能在不打开另一个文件的前提下**可执行地**开始——纯指针会让元技能的执行者跳过判定。
- **discriminating_evidence**: 对同一段误置样本，让执行者在「只读到元技能那一行」的条件下判定；结果二值：执行者能说出该去哪个文件看判据并给出可定位结论 / 执行者因信息不足直接放行。
- **expected_sacrifice**: 三个被改 `SKILL.md` 的 `skill-shape.py` 已全部 exit 10（≈5354 / 5584 / 5096 可控 tokens vs 5000 预算），本决策的「一行」形态是唯一不把体积债务进一步恶化的写法；代价是每次判定多一次读盘。
- **revision_trigger**: 连续两个下游项目的元技能流程出现「执行者没打开 owner 就给了通过判定」≥ 2 次 → 重开，评估把最小判据（一句话，不含成员表）内联进 `create-skills` § 6。

### T-002 — 作者侧判定挂在既有校验步骤，不抽成确定性脚本

- **decision**: 机制/策略判定落 `create-skills` § 6、`improve-skills` § 2/§ 3、`merge-skills` § 5/§ 8 的**既有**步骤；不新增脚本、不新增门禁、不新增第二套清单（A6 / C8 / SW-07）。
- **antithesis**: 写一个 `mechanism-policy-check.py`（stdlib-only、只读、退出码三态），把所有可正则化的形态（绝对路径、盘符路径、用户目录名）抽成确定性检查，元技能只调用它。当误置的多数形态确实是可 grep 的字面量时它更优——判定结果可复算，且元技能体积只加一行调用。
- **binding_constraints**:
  - pole_a: 判定必须覆盖**语义**面——「可复用逻辑是否住在运行环境的说明里」无法用正则判定，`research.md` § R7 实测的唯一载体是模型/人（GM-02）。
  - pole_b: 本特性 MUST NOT 新增第二套门禁或第二个检查器（C8 / FR-016 的「不新增」边界是 SC-003 与零新机器的共同前提）。
- **discriminating_evidence**: 拿 US1 场景 2 的机制误置样本（判定规则写在一份运行说明里）跑一个正则检查器，看它能否点名该行；结果二值：能（脚本方案成立）/ 不能（脚本只覆盖策略误置一侧，US1 场景 2 未覆盖）。
- **expected_sacrifice**: SC-002 的检出率只能靠宿主实录测量（证据而非测试），不能靠一次 pytest 断言；`research.md` § R7 已把这条代价记为该决策的直接后果。
- **revision_trigger**: 三个元技能的判定在宿主实录里对「策略误置」侧出现 ≥ 2 次漏检且均由同一个可正则化形态造成 → 重开，评估只把该侧抽成确定性预览器（不成为门禁，只产出候选清单）。

### T-003 — 「零新增命令面」压过「给作者一条直接可调的入口」

- **decision**: 不新增 `/speckit.*` 命令，`templates/commands/skills.md` 零改动；`/speckit.skills` 只在 owner 成员表里作为 `command-surface` 声明接线位（SW-06 / OD-07）。
- **antithesis**: 新增 `/speckit.mechanism`（或给 `/speckit.skills` 加一个 `check` 子意图），让作者在提交前主动对任一技能跑一次判定。当判定被证明是高频动作、且元流程的收尾点太晚时它更优——作者可以随时自查，不必重跑整个创建流程。
- **binding_constraints**:
  - pole_a: 命令面每加一条，就有第二套入口需要与元技能保持一致，一致性本身要一条守卫（C1 的「不新增第二套判定」）。
  - pole_b: 原则必须能在**真实创建/改进路径上自动生效**，而不是依赖作者记得去调一个命令（A7：对既有技能零回溯改造，元流程是唯一自动通道）。
- **discriminating_evidence**: 统计一个真实创建流程里判定被触发的时机；结果二值：判定在作者仍在改技能的上下文里就触发（收尾点足够早）/ 作者需要在草稿写完后另行调用才触发（收尾点太晚，需新入口）。
- **expected_sacrifice**: SC-003 的封闭因此可以覆盖全部 27 个命令模板（逐字节），代价是没有一条「作者主动自查」的便捷路径；作者侧的自查入口留给 `improve-skills` 的对账通道。
- **revision_trigger**: 连续两个下游项目报告「提交前无法自查、只能等元流程收尾」并因此返工 ≥ 2 次 → 重开，评估给 `/speckit.skills` 增加一个只读 `check` 意图（仍不新增命令）。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/082-mechanism-policy-separation/
├── requirements.md           # /speckit.requirements output — this spec's What（本阶段 MUST NOT 修改）
├── plan.md                   # This file (/speckit.plan output)
├── research.md               # Phase 0 output — R1…R9 实测与可行性
├── data-model.md             # Phase 1 output — 7 实体 / 21 校验规则 / 2 状态转移 / GM-03 允许差异集
├── contracts/                # Phase 1 output — 3 份契约（owner-document / skill-wiring / guard-and-measurement）
├── quickstart.md             # Phase 1 output — 9 个场景，逐例标注 run / deferred 与前提
├── feature-ref.md            # Phase 1 output — Feature 082 绑定与交付面
├── checklists/requirements.md # /speckit.requirements 的规格质量清单
├── test-evidence/            # 证据：plan 门禁输出、定向集基线、SC 各面的测量记录
├── tasks.md                  # Phase 2 output (/speckit.tasks — 不在本阶段产出)
└── verification.md           # 实现输出 (/speckit.implement)
```

### Source Code (repository root)

```text
# 框架源（本特性实际改/建的面；.specify/ 侧是 sync-mirrors.py 产出的镜像）
shared/
└── definitions/mechanism-policy-definitions.md   # NEW 唯一 owner（[[STR-003]]）；OD-01…OD-10 九个章节
skills/
└── external/
    ├── create-skills/
    │   ├── SKILL.md                              # 改写（SW-01）：§ 6 Minimum checks 末行之后 +1 条 checklist 项
    │   └── references/mechanism-policy-check.md  # NEW（SW-01）：判定步骤 ≤ 12 行 + 两类误置的定位方法
    ├── improve-skills/
    │   ├── SKILL.md                              # 改写（SW-02）：§ 2 调研问题 + § 3 候选类别 policy source missing or ambiguous
    │   └── references/loop-playbook.md           # 改写（SW-02）：批量模式以一次批口径执行
    └── merge-skills/
        ├── SKILL.md                              # 改写（SW-03）：§ 5 no-loss gate 之后前置判断 + § 8 一条验证项
        └── references/provenance-record.md       # 改写（SW-03）：how to verify 一栏可写层归属判定（不新增列）
tests/
└── contract/
    ├── test_mechanism_policy_owner_doc.py        # NEW — OD-01…OD-10 形态 + owner 镜像逐字节（GM-01）
    ├── test_mechanism_policy_ownership.py        # NEW — 一源与九个邻接边界（FR-015 / OD-08 + FR-004）
    ├── test_mechanism_policy_skill_wiring.py     # NEW — SW-01…SW-03 的位置、唯一性、owner 引用、通过分支
    ├── test_mechanism_policy_guard.py            # NEW — SC-003 逐字节封闭集（GM-03 五要件 + GM-07 反例）
    ├── test_mechanism_policy_missing_policy.py   # NEW — SC-004 零写入 + 补齐后逐字节一致（GM-05 主面）
    └── test_mechanism_policy_decidability.py     # NEW — SC-001/SC-005 分母（附录题集可解析、依据只引 OD-02）

# 计划期义务（登记行落在既有单文件注册表上；不是本特性的代码交付面，D9）
.specify/memory/glossary.md             # +1 词条 `机制/策略分离 (Mechanism–Policy Separation)`（Origin user / Status proposed）
.specify/shared/definitions/framework-map.md  # 既有 `definitions/` 行追加本 owner 的文件名（不新增行、不新增目录）
CHANGELOG.md                            # implement 收口时 +1 条

# 明确不改（SC-003 的比较单元内必须逐字节不变的部分）
templates/commands/**                   # 27 个模板全部零改动（SW-06 / T-003）
skills/external/coaching-skills/**      # 排除成员，零改动（SW-05）
skills/internal/run-skills/**           # 排除成员，零改动（SW-05）
```

**Structure Decision**: 全部落在既有目录形状上，**不新建任何目录、不新建任何目录根**（C4 / FR-016 / Principle XVII）：owner 进 `shared/definitions/`（与 `derivation-definitions.md` / `dogfooding-definitions.md` / `flow-class-definitions.md` 同族的概念锚点层），判定方法进 `create-skills` 自己的 `references/`（技能自有资源，随技能分发，A3），测试进 `tests/contract/`（与既有 `test_expression_compatibility.py` / `test_one_source_of_truth.py` 同族）。`.specify/` 侧的同名文件全部由 `sync-mirrors.py` 产出、MUST NOT 手改。

> 机制/策略分离在本文件的自用：`data-model.md`、`contracts/` 与上表只写**机制**（形态、判据、断言口径）；路径、落点、样本位置一律写成运行环境取值。这是本特性按自己的新原则写的证据（`feature-ref.md` 末节）。

### Mirror Obligations

Baseline measured **before** any edit on this branch (2026-11-05, `research.md` § R5 / `quickstart.md` § S3): `sync-mirrors.py --check` exit 0, six pairs all `ok` (templates 22 / skills-external 409 / skills-internal 138 / agents 3 / scripts 119 / shared 62); `regen-command-copies.py --check` exit 0. Baseline drift is zero, so an absolute `exit 0` criterion is legitimate **because it was measured**, not by expectation — and the one expected count movement (`shared/` 62 → 63 after the new owner doc) is a post-sync baseline, MUST NOT be hard-coded into any assertion (`quickstart.md` § S3 判据).

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/mechanism-policy-definitions.md` (NEW) | `.specify/shared/definitions/mechanism-policy-definitions.md` | `python3 scripts/python/sync-mirrors.py` 然后 `--check`；判据 = 该对 `ok` 且**无新增漂移**（基线六对全 ok）。所有新增断言 MUST NOT 钉 `shared/` 的文件计数 |
| `skills/external/{create-skills,improve-skills,merge-skills}/SKILL.md`（改写）与 `skills/external/create-skills/references/mechanism-policy-check.md`（NEW）、`skills/external/{improve-skills,merge-skills}/references/*.md`（改写） | `.specify/skills/{create-skills,improve-skills,merge-skills}/**`（平铺层，`sync-mirrors.py` 的 `skills/external → .specify/skills` 对） | 同一条再生成 + `--check`；判据 = `ok` 且无新增漂移 |
| `templates/commands/**`（**本特性零改动**） | `.claude/commands/speckit.*.md`、`.github/prompts/speckit.*.prompt.md`、`.qoder/commands/speckit.*.md`、`.opencode/command/speckit.*.md`（`regen-command-copies.py` 的按工具副本；`.specify/templates/commands/` 已退役） | `python3 scripts/python/regen-command-copies.py --check` → exit 0（本特性预期**零变化**）。这条义务的用途正是**证明**命令面零改动（SW-06），而不是等它漂移 |
| `tests/**`、`CHANGELOG.md`、`.specify/memory/glossary.md`、`.specify/shared/definitions/framework-map.md` | 无镜像（`tests/` 不在 `MIRROR_PAIRS`；`glossary.md` 与 `.specify/shared/definitions/framework-map.md` 是**本仓的项目运行时产物**，无框架源对） | n/a。注意后者：`framework-map.md` 只存在于 `.specify/shared/definitions/`，**没有** `shared/definitions/framework-map.md` 源文件，因此它是一条「只在此处」的登记行，不是镜像漂移 |

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises — this section carries the column set and the values only.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | 一套可用的 **Python 3 + pytest + git** 运行环境存在，且是仓内既有入口 `scripts/bash/run-tests.sh` 能解析到的那一套；六个新契约模块与 SC-003 的逐字节比较都压在这条前提上 | `research.md` § R1 实测：`.venv/bin/python` → `Python 3.14.6` / `pytest 9.2.0`；`git version 2.54.0 (Apple Git-157)`；`pyproject.toml` `requires-python = ">=3.8"`。**运行形态前提**：本机 shell 的 `PYTHONPATH` 指向一套内部 lib，其 `platformdirs` 缺 `pytest_plugin`，使 `.venv/bin/python -m pytest` 启动前即报 `ModuleNotFoundError: No module named 'platformdirs.pytest_plugin'`；处置 = 测试一律以 `env -u PYTHONPATH` 前缀运行（`quickstart.md` § S2 逐字命令），MUST NOT 修改 `run-tests.sh` 或 `pyproject.toml` 来绕开 | verified | — |
| EP-002 | 至少一个**受支持的 agent 宿主**可用于 SC-002 的检出率 / 误报数测量（该项只能以流程实录为证据，不能以 pytest 断言替代，`research.md` § R7） | 本次 plan 运行**所在宿主** = 本仓约定内的原生子代理执行环境（`flow_class=execution` / `local` 拓扑，`state` spine 的派发前置检查 ③ 记 `n/a — 本地原生子代理`；④ 记 `execution-config.py --action resolve --agent …` exit 0，`mode=native`），宿主 roster 取自 `docs/reference/cli/supported-agent-tools.md`（`AGENT_CONFIG` 为准）。**可用性探针**：同一宿主上的 SDD 执行链在 requirements / clarify / 本 plan 阶段均已实跑（三次阶段产物落盘、门禁实跑），说明「能加载并执行框架流程」成立；**版本原文尚未采集**（本阶段未跑宿主 CLIs 的 `--version`），故本条按 `verified` 记「宿主可用」，`Pin` 列的「宿主名 + 版本原文」由实现期 SC-002 实录按 RS-005 的 `Contract` 单元格同趟记录 | verified | — |
| EP-003 | 三个被改的 `SKILL.md` 在**改动前**即已超出 `skill-shape.py` 的 5000 可控 tokens 预算（exit 10），因此本特性的通过条件不能写成「被改技能的 `skill-shape.py` exit 0」 | `research.md` § R4 + 本阶段实跑：`create-skills` ≈ 5354、`improve-skills` ≈ 5584（已扣除契约强制块 466）、`merge-skills` ≈ 5096，三份 `skill-shape.py` 均 exit **10**；同批 `redline-check.py` 三份均 rc **0** / `PASS — no red line triggered`（`coaching-skills` 对照：shape rc 0 / redline rc 0）。这是**既有债务**，不是本特性引入的缺陷；按 `improve-skills` Hard Constraint 3 的例外情形 (a) 处理：实现期 MUST 为每个被改文件记录 before/after 两个 `est_tokens_controllable` 数与 delta，且新增文本保持「一行判定 + 路径引用」形态 | verified | — |
| EP-004 | SC-003 的比较单元在基线上**非空且可枚举**，且当前工作树与基线[[STR-002]]在该单元内零差异 | 本阶段实跑（`quickstart.md` § S4 的同一形态）：`git ls-tree -r --name-only 3ffeb26e -- skills/ templates/commands/` → **575** 个路径（`skills/` 548 + `templates/commands/` 27）；带允许差异集的补集比较输出 `compared=575 complement=570 allowed_in_unit=5 frozen_mismatches=0`。`allowed_in_unit=5` 正是「6 条允许路径中，`references/mechanism-policy-check.md` 尚未创建」——它是新增路径的下限证据，不是漏项。`research.md` § R6 同批测得 `git diff --stat aaee504c..HEAD -- skills/ templates/ commands/` 为空 | verified | — |
| EP-005 | 两处再生成入口在动手前零漂移，因此「本特性关闭时 `--check` exit 0」是可达判据 | `research.md` § R5 + `quickstart.md` § S3 实测：`sync-mirrors.py --check` 六对全 `ok`（templates 22 / skills-external 409 / skills-internal 138 / agents 3 / scripts 119 / shared 62）、`regen-command-copies.py --check` `OK: all per-tool command copies match the source templates`，二者 rc 0 | verified | — |
| EP-006 | 「零新脚本」在实现期**可兑现**：所有可判定的部分都有既有载体（pytest + git + 两个既有技能脚本），不可判定的部分本来就不该变成门禁 | `research.md` § R7 的逐判定载体表（七行）；GM-02 给出了写出/判定分离的边界；EP-001 证明 pytest + git 可用，`skill-shape.py` / `redline-check.py` 实测可跑（EP-003 同批） | verified | — |

## Inherited Blockers

Owner of this table's shape, its `Disposition` domain (`resolved | inherited | not-applicable`), the `Source row` / `Carrier` / `Carrier slice` grammar and the carrier's eligibility rule: `shared/workflow/acceptance-hardening.md` § Inherited Blockers — this section carries the column set and the extraction readings only.

**Dependency set: none.** Derivation (measured 2026-11-05): 本特性不消费任何既有 Feature 的未决测量——它不修改任何既有特性建立的契约面（命令模板零改动、既有技能零回溯改造），SC-001…SC-005 全部分母由本特性自己的 owner 附录题集与自己的样本集给出。因此依赖集为空，按规则写这一句而不是留一句含糊的「无既有依赖」。

**Extraction readings (the closed three-source set, measured)** — 三个源各测一次，结论是**零行**，而零行是一个读数、不是一种处置，故本表没有处置行。读数写成列表而不是表：本节的表形态只属于处置表，一张读数列在它前面的表会被守卫读成「一串没有处置的行」（本阶段实测：`pre-analyze-check.py --stage plan` 曾把该表的三行读成 `row-1`/`row-2`/`row-3` 的 undisposed 错误，DC-003）。

- **`## Deferred` 节** — `grep -rn "^## Deferred" .specify/memory/features/` → **0 命中**（`.specify/memory/features/` 下没有任何特性详情携带该节）。
- **`verification.md` 的 `blocked` / `deferred` / `partial` 状态行** — `grep -rln "SC-001_status" .specify/memory/features/` → **0 命中**（特性详情不承载 status 行；status 行只住在各 spec 目录的 `verification.md`，而依赖集为空，故不在抽取范围内）。
- **非空的 `deferred_tasks=`** — `grep -rn "^deferred_tasks=" .specify/memory/features/` → **0 命中**。

**结论**：本特性**无继承 blocker**——依赖集为空，且三个源各产零行。MUST NOT 为一个不存在的行发明 locator（那正是 join key 要防的缺陷），也不为不存在的依赖写 `not-applicable` 行（`not-applicable` 要一个真实的 `Source row` 才有意义）。因此本节没有处置表，只有这一句零行结论。

## Design Decisions (D1–D10)

### D1 — owner 放 `shared/definitions/` 而不是 `shared/guidelines/`

`shared/definitions/` 装的是**概念锚点**（`derivation-definitions.md`、`dogfooding-definitions.md`、`flow-class-definitions.md`、`tool-definitions.md`…），每个文件回答「这个词是什么意思、边界在哪」；`shared/guidelines/` 装的是**工作流纪律**（`fast-fail.md`、`one-source-of-truth.md`、`directory-governance.md`…），每个文件回答「做这件事时该怎么走流程」。本特性交付的是**定义**而非流程：判别口径、成员表、症状分类、归档规则、提示形态、谓词。被否决的替代方案：放 `shared/guidelines/`（因为它约束元技能的流程）——否决理由是那会让「引用它 = 引用一段方法论」与「引用它 = 引用一个术语的定义」混成一种动作，而 FR-018 要求的恰恰是术语层的锚定（A2）。

落点：`shared/definitions/mechanism-policy-definitions.md`（框架源）→ `.specify/shared/definitions/`（镜像）。

### D2 — 零新脚本（依据 A6 / C8 / FR-016，判定依据是 `research.md` § R7 的实测，不是偏好）

`research.md` § R7 逐个判定逐条列出载体，七项里五项有既有确定性载体（pytest / git / 两个既有技能脚本），一项（语义判定）本来就不该被正则化（GM-02），一项（`references/` 的定位方法）是文本。**因此 A6 的「若 plan 证明书面判定不可判定，再决定是否抽成确定性脚本」在这个计划里的答案是：需要模型判断的那一半不可正则化，可正则化的那一半已被 GM-07 的反例断言覆盖在测试里。** 结论：不新增脚本。

这条决策的可判定形态：六个新契约模块全部是 `tests/contract/` 下既有的 pytest 模块形态，不引入 `scripts/` 下的任何新文件；GM-01 的清单是封闭的（六个），任何第七个模块或任何新脚本都必须先推翻本节。

### D3 — 成员谓词与封闭集

谓词逐字沿用 requirements § Constraints C1（clarify 已 ratified、全表复算无翻转，本阶段**不改一行**）：

| 流程 | verdict | 依据 | 本特性的动作 |
|---|---|---|---|
| `create-skills` | `included` | 产出新技能 | SW-01（§ 6 + `references/mechanism-policy-check.md`） |
| `improve-skills` | `included` | 产出变更后的技能 | SW-02（§ 2 + § 3 + `references/loop-playbook.md`） |
| `merge-skills` | `included` | 产出合并后的目标技能并下线源技能 | SW-03（§ 5 + § 8 + `references/provenance-record.md`） |
| `coaching-skills` | `excluded` | 产出是观察与计划，不改写受训技能；真实改写仍经 `improve-skills`，故其作者侧义务已被纳入者覆盖 | 零改动（SW-05） |
| `run-skills` | `excluded` | 产出是目标技能按其自身流程执行，不改变任何技能的定义或行为 | 零改动（SW-05） |
| `/speckit.skills` | `command-surface` | 命令模板的 Routing 表把 create/merge/coach 意图**转发**给上述元技能，故只声明接线位 | 零改动（SW-06） |

**一处实测定位（不是变更谓词，是可执行性的修正）**：`run-skills` 的实际路径是 `skills/internal/run-skills/SKILL.md`（不在 `skills/external/`）。本计划的 SW-05 守卫与 GM-03 的结构不变量因此按**真实路径**写；owner 成员表只写流程名 `run-skills`，不带路径前缀，避免把「层」写成位置。这属纠正（恰有一种读法与已记录意图一致：requirements 的 C1 表按**流程**裁定，从不按目录裁定），已在 DC-002 披露。

### D4 — 成员表放 owner 文档，不建第二份注册表

`data-model.md` E-6 的封闭成员表是 owner § Meta-layer Membership 的**形态投影**（可收窄、不可扩大），不是第二个定义点：机器可读的唯一落点在 owner 正文，`data-model.md` 的投影只用于让 `test_mechanism_policy_guard.py` 做交叉断言（V-19：`included` 集合 == 允许差异集的流程子集）。被否决的方案：`tests/` 里维护一份 `MEMBERS = (...)` 常量作为判定源——那会把「谁是元技能」变成只有测试知道的事实，而下游项目拿不到测试。允许的重复形态是既有三种之一：**literal pinned in a test**（`data-model.md` E-6 的表与 owner 保持字面相等，由 `test_mechanism_policy_owner_doc.py` 断言），不是第三套数据文件。

### D5 — 消费侧提示形态 owner 化，元技能只引用，不回溯改造

FR-006 要求「形态 owner 唯一，其余位置以路径引用」。落点 = owner § Consumption Contract（OD-06）；接线点 = SW-04 的四处「即将执行副作用之前」（`create-skills` § 2 writability pre-flight 与 § 7/§ 8 写入之前、`improve-skills` § 7 编辑之前、`merge-skills` § 7 decommission 之前）。被否决的方案：为每个命令写一份提示模板——那既违反 FR-015（复制形态）也违反 FR-011（命令面零改动）。对既有 15 个 external / 38 个 internal 技能的正文：**零改动**（A7 / FR-011 / SC-003）。

### D6 — 六个契约测试模块 + 夹具；SC-001 / SC-005 的人工样本记录在 test-evidence

模块清单与断言面 = GM-01（封闭的六个，各对应一条契约条款组）。夹具策略：**不新建 `tests/fixtures/` 子目录**——`test_mechanism_policy_missing_policy.py` 用 pytest 既有 `tmp_path` 就地造「假技能 + 假运行目录」，`test_mechanism_policy_guard.py` 用 `tmp_path` 复制补集内一个文件并注入一字节破坏来断言转红（GM-07）。被否决的方案：在 `tests/fixtures/` 下新建 `mechanism-policy/` 声明式夹具集——那是「第一个新种类目录」，按 Principle XVII 要同趟登记目录图，而本特性的夹具全部是一次性的最小树、没有跨模块复用价值，登记一个只用一次的目录是净负担。

人工样本（双判定者 SC-001、读者作答 SC-005、宿主实录 SC-002 / SC-004 支撑面）落 `test-evidence/`，**不入 pytest**——它们判的是模型/人的行为，不是形态（GM-02）。

### D7 — 冻结哈希模块 `tests/contract/test_expression_compatibility.py` 需为被改文件追加行

`research.md` § R3 实测：三个被改的 `SKILL.md` 在 `ALLOWED_POST_BASELINE_CHANGES` 的补集（冻结哈希）里，登记机制是活的（`test_c5_non_wiring_files_keep_their_frozen_hashes` 通过，`WIRING_SKILLS` 恰为 `create-docs` / `humanize`）。实现期 MUST 追加三行 `reason` + `markers`（`markers` 取该技能新判定里唯一的字面，如 owner 路径或判定 id），MUST NOT 放宽哈希清单本身、MUST NOT 删除或跳过断言。

**本阶段实测补一条 R3 未覆盖的事实**（用于让实现期不踩）：该模块还有两处会**被本特性触发**的既有登记面——

1. `RENAMED_SKILL_REL = "skills/external/coaching-skills/SKILL.md"`：`_retired_skill_register` 断言「清单里恰好一个路径从磁盘消失」。`coaching-skills` 是本特性的**排除**成员，零改动，所以该断言不受影响——但它是「`coaching-skills` 必须原样存在」的机械证据，实现期 MUST NOT 触碰该目录。
2. `skills/internal/run-skills/SKILL.md` 已是 `ALLOWED_POST_BASELINE_CHANGES` 的一条既有键（Feature 078 的路由指针）。它是本特性的**排除**成员，实现期 MUST NOT 追加、修改或删除该键。

六条 `references/` 的层归属：`loop-playbook.md`（`improve-skills`）与 `provenance-record.md`（`merge-skills`）**不在**该模块的冻结哈希清单内（清单只覆盖 `SKILL.md` 与已登记的少数文件），因此不需要追加行；这一点由 `test_mechanism_policy_guard.py` 的逐字节断言覆盖（它们落在 GM-03 的允许差异集内，属**允许变化**而非冻结）。

### D8 — 单包交付（估算 ≈ 21 任务 < 40；不切片）

| 分组 | 自然任务估计 |
|---|---|
| Setup（目录/镜像基线确认、冻结清单登记面核对） | 2 |
| Foundational：owner 文档九个章节（OD-01…OD-10，含附录题集 ≥ 12 条） | 4 |
| US1（`create-skills` § 6 + `references/mechanism-policy-check.md`） | 2 |
| US2（`improve-skills` § 2/§ 3 + `references/loop-playbook.md`） | 2 |
| US3（消费侧提示形态接线四处 + owner § Consumption Contract 复核） | 2 |
| US4（成员表 + 谓词 + 排除理由 + 命令面接线位） | 1 |
| 六个契约测试模块（含 GM-07 每模块一条反例断言） | 6 |
| 镜像再生成 + 两处 `--check` | 1 |
| 测量与收口（SC-001…SC-005 样本记录、`ALLOWED_POST_BASELINE_CHANGES` 三行、`skill-shape` before/after 记录） | 3 |
| **合计** | **≈ 21** |

低于 40 的上限，故 **`single-package`**：不声明切片、不丢弃任何 FR / SC；`tasks.md` 可以是一张 21 行左右的清单。若 `/speckit.tasks` 自己的分解检查给出 > 40 的读数，回落到「按 US1→US4 自然顺序切 082a/082b」的预案，而不是压缩任务粒度。

### D9 — glossary / framework-map / CHANGELOG 是计划期义务（登记，本阶段不写）

- `.specify/memory/glossary.md`：+1 词条 `机制/策略分离 (Mechanism–Policy Separation)`，Origin `user`、Status `proposed`（按 `shared/workflow/glossary.md` 的协议）。它是跨特性共享的**单文件注册表**，按本阶段「只提交本特性产物」的边界不写。
- `.specify/shared/definitions/framework-map.md`：既有 `| Shared definitions & conventions |` 行追加本 owner 的文件名——**不新增行、不新增目录**（C4；该文件不在 `sync-mirrors.py` 的 `MIRROR_PAIRS` 内，是本仓项目运行时产物，无框架源对）。
- `CHANGELOG.md`：implement 收口时 +1 条（frame: 新 owner + 三条元技能判定 + 六个契约模块）。

### D10 — 镜像与命令副本再生成

源码改动全部落框架源（`shared/`、`skills/`、`tests/`），然后恰两次再生成入口：`python3 scripts/python/sync-mirrors.py`（+ `--check`）与 `python3 scripts/python/regen-command-copies.py`（+ `--check`）。**本特性不改命令模板**，故命令副本预期**零变化**；`--check` 仍要跑，用来证明这一点（SW-06）。`.specify/` 侧永不手改为主改动。

## Complexity Tracking

N/A — the Constitution Check has no Fail and no Partial row; no violation needs justification.

## Phase 0: Research Review

Research 以独立文件记录（超出内联阈值且携带环境实测）：[`research.md`](./research.md) § R1–R9。本阶段由它决定的四件事：运行器与 `PYTHONPATH` 前缀前提（R1 → EP-001）、三个被改技能的既有体积债务（R4 → EP-003）、封闭集分母 575 与「守卫必须报计数」（R6/GM-04）、以及「零新脚本可兑现」的逐判定载体表（R7 → D2）。本阶段对 R3 做了一处**补测**并把结果写进 D7（`coaching-skills` / `run-skills` 在冻结清单里的真实位置），§ Inherited Blockers 的零行结论另行实跑三个源取证（同一节内）。

## Decomposition & Ceiling

- **FR**：18 条（FR-001…FR-018），**全部**落入本包，无一条被切片丢弃。
- **SC**：5 条（SC-001…SC-005），全部落入本包；其中 SC-001 / SC-002 / SC-005 的度量是人工样本（`test-evidence/`），SC-003 / SC-004 的主面是可判测试。
- **自然任务计数**：≈ 21（D8 的分组读数之和），低于上限 40。
- **结论**：`single-package`，无切片，无 FR / SC 丢弃。

## Measurement Plan

测量方法、样本/夹具与证据落点的条款 owner 是 `contracts/guard-and-measurement.contract.md`（GM-01…GM-09）与 `contracts/owner-document.contract.md`（OD-09 题集）。本表只把每条 SC 指向那两组条款，**不复制** GM 的表格。

| SC | Path | 测量方法（指向条款） | 样本 / 夹具 | 证据落点 |
|----|------|----------------------|-------------|----------|
| SC-001 | final | 两位 fresh-context 只读判定者**仅凭 owner 文档**对附录题集逐条作答，比较一致率（OD-09 + GM-02；题集可解析性由 `test_mechanism_policy_decidability.py` 守） | owner § Worked Examples 的封闭题集（≥ 12 条，`data-model.md` E-7 / V-21） | `test-evidence/sc-001-<date>.txt`（题集快照 + 两份结论 + 一致率） |
| SC-002 | final | 一个受支持宿主上，改动前/后各跑一次纳入的元技能流程；比较检出（含文件与位置）与误报（GM-09） | 误置样本 ×2（策略误置 / 机制误置）+ 正确分层样本 ×2（GM-09） | `test-evidence/sc-002-<date>.txt`（宿主名 + 版本原文 + 输入草稿路径 + 输出原文 + 逐样本 verdict 表） |
| SC-003 | final | 基线[[STR-002]] 与 HEAD 的逐字节补集断言 + 路径集断言 + `compared=575` 形态的计数（GM-03 五要件 / GM-04 / GM-07 反例） | 允许差异集 = `data-model.md` § GM-03 的唯一路径落点（单元内 6 条） | `tests/contract/test_mechanism_policy_guard.py`（可复算）+ `test-evidence/sc-003-<date>.txt`（一次真实运行的逐字输出） |
| SC-004 | final | 主面 = `tmp_path` 内的路径集 + sha256 快照前后比较与补齐后产物哈希比较；支撑面 = 一次宿主实录（GM-05 两个面） | `tmp_path` 造的假技能 + 假运行目录（无持久夹具，D6） | `tests/contract/test_mechanism_policy_missing_policy.py` + `test-evidence/sc-004-<date>.txt`（支撑面，含宿主名 + 版本） |
| SC-005 | supporting | 一位**未参与本特性**的读者仅凭 owner 文档作答同一题集，正确数 vs 题集全集（OD-09） | 同一份封闭题集（与 SC-001 共用分母，MUST NOT 另起一份） | `test-evidence/sc-005-<date>.txt`（作答记录，可复算：同一题集重测） |

**定向集与基线（TEST BUDGET 的 plan 侧读数）**：本阶段是 docs-only，`plan.md` 与上一 attempt 的 7 个附属产物都不落在 `test_files` 的选中面内，故按 `not-run-docs-only` 记录（六项缩减字段，`test-evidence/plan2026-11-05-stage-status.jsonl`）。实现期的定向集命令与基线（`892 passed` / 失败名集为空）已在 `research.md` § R2 与 `test-evidence/plan2026-11-05-baseline.txt` 逐字记录，判据是**差集**而不是绝对全绿（GM-08）。

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

**留给 tasks / implement 重测的（`deferred`）**：S5 的 after 半（被改文件的新体积与红线判定）、S6（SC-004 零写入模块）、S7（SC-002 宿主实录）、S8（SC-001 / SC-005 题集作答）。每条 `deferred` 场景在 `quickstart.md` 各节末尾的 **Premises** 里写清它假设的前提，供下一阶段重新测量而**不是继承**。

## Phase 1: Design Artifacts Summary

Backfilled after the artifacts landed; every count below is read from the files, not from memory.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | 7 实体（E-1 Principle … E-7 Decidability Sample）/ 21 条校验规则（V-1…V-21）/ 1 个封闭谓词（C1）/ 1 张封闭成员表（`included` 3 / `excluded` 2 / `command-surface` 1）/ 2 条状态转移（SM-1 / SM-2）/ GM-03 允许差异集 12 行（其中属比较单元者 6） |
| Contracts | [`contracts/`](./contracts/) | 3 份：`owner-document.contract.md`（OD-01…OD-10 + DR-001 追溯）、`skill-wiring.contract.md`（SW-01…SW-08 + 追溯）、`guard-and-measurement.contract.md`（GM-01…GM-09 + 追溯） |
| Quickstart | [`quickstart.md`](./quickstart.md) | 9 个场景（S1–S9）；`run` 6 / `deferred` 3（S5 前后各半计入 `run` 与 `deferred`） |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | Feature 082 绑定 + 交付面（新增 1 / 改写 5 / 新增测试 6 / 计划期义务 3 / 再生成入口 2 / 明确不新增 7 类） |
| Research | [`research.md`](./research.md) | R1–R9（R3 由本阶段补测了冻结清单的排除成员位置，结论落在 D7） |

**Drift from the Phase 0 expectation**: 一处已披露的纠正——`research.md` / `contracts/skill-wiring.contract.md` / `contracts/guard-and-measurement.contract.md` 把基线证据路径写成 `test-evidence/plan-baseline.txt`，而该文件在上一 attempt 的 turn budget 耗尽时**未曾落盘**（`ls test-evidence/` 实测无此文件）。本阶段把它就地纠正为本阶段实际写入的 `test-evidence/plan2026-11-05-baseline.txt`（见 DC-001），并把 S2 的基线重新实跑一次以保证该文件与其引用一致。

## Delivery Review (DR-001 覆盖复核 + DC 披露)

**DR-001 — 18 条 FR 的落点覆盖（本阶段自检，防「改了但没覆盖某条 FR」）**：

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

**DC-001 — 基线证据路径纠正（RP-1 明显近似错，已就地修复并披露）**：`research.md` § R2 与两份契约的 4 处引用写作 `test-evidence/plan-baseline.txt`，该路径在上一 attempt 未落盘。恰有一种读法与已记录意图一致（意图是「本阶段实测的定向集基线」），本阶段以 `env -u PYTHONPATH bash scripts/bash/run-tests.sh …` 重跑该基线并写入 `test-evidence/plan2026-11-05-baseline.txt`，同时把 4 处引用改为该路径。未改动基线的**内容**（`892 passed`、失败名集为空与上一 attempt 的读数一致）。

**DC-002 — `run-skills` 的真实路径（RP-1 路径近似错，已就地修复并披露）**：requirements § Constraints C1 把 `run-skills` 与 `skills/external/` 同段提及，实际文件在 `skills/internal/run-skills/SKILL.md`。恰有一种读法（C1 按**流程**裁定，从不按目录裁定），本计划的守卫与结构不变量按真实路径写；谓词与成员表**未改一行**（改谓词会触发 C1 末句的「全表重算」义务，本阶段不触发）。

**DC-003 — `## Inherited Blockers` 读数形态纠正（RP-1 装配错，已就地修复并披露）**：本文件初稿在该节先放一张「三源抽取读数」表、再放处置表；`pre-analyze-check.py --stage plan` 实测把前者读成 `row-1`/`row-2`/`row-3` 三条 `inherited-blocker` 且 Disposition 为空 → `decision=fail, errors=3`（守卫的 `section_rows()` 取该节**第一张**表）。恰有一种读法与已记录意图一致：意图是「处置表」，读数是证据不是处置；且零行结论本身不构成任何待处置项（`.specify/memory/features/082.md` 无继承阻塞记录，三源实测零行）。故把读数改写为列表、把空处置表改写为一句零行结论，语义未变、守卫复跑 `decision=pass, errors=0`。

## Constraints & Assumptions 记录位置

本阶段为访谈式问题自行的裁决（无向用户提问）落三处：`research.md` § R1–R9 与 § 未决与交下一阶段（实测结论与可行性）、`## Design Decisions` D1–D10（含被否决的替代方案）与 `## Decision Tensions` T-001…T-003（承重决策的对立面与重开条件）、以及本文件的 EP-001…EP-006（执行前提及其证据）。三条就地纠正 DC-001 / DC-002 / DC-003 见上节。
