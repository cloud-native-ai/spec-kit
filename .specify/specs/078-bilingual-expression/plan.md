# Implementation Plan: 双语表述（Bilingual Expression）

**Branch**: `078-bilingual-expression` | **Date**: 2026-10-30 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `078-bilingual-expression` → Feature 078 双语表述（Bilingual Expression）
**Input**: Specification from `.specify/specs/078-bilingual-expression/requirements.md`

## Summary

把「核心概念 / 关键流程在**定义处**使用中英双语」从自发实践固化为四件套交付：

1. **约定本体**：新建唯一 owner 文档 [[STR-001]]（框架源 `shared/guidelines/`，镜像 `.specify/shared/`），承载六组事实（方向规则、唯一形态、覆盖定义面封闭集、豁免面封闭集、一致性规则、迁移边界）与「定义处」可判定信号清单 S1…S4。
2. **ambient 分发**：`templates/instructions-template.md` 新增 `## Bilingual Expression (双语表述)` 小节——一句话摘要 + owner 路径指针，零枚举复述（FR-008/FR-012）。
3. **机械守卫**：新建确定性检查器 `scripts/python/bilingual-expression-check.py`（动作 `scan` / `coverage` / `census`，退出码 0/1/2，finding 码封闭四值），复用 `glossary-utils.py` 读取模式，不并入 `doc-consistency-check.py`（R-7），不绑定阶段门禁算子（FR-010）。
4. **测量与登记**：SC-001 关键词表机械派生自 owner 四组枚举 + 交付日快照；SC-002 用 `--scope changed` 只测新写内容；SC-005 取 100% census（R-11）；漂移守卫 = 契约测试 `tests/contract/test_bilingual_expression.py`（C-006）。

零新命令、零新门禁面、零运行时/服务/后台进程（FR-015）。18 条 FR / 5 条 SC / 4 个用户故事。存量 1383 处全角形态不追溯（FR-006，A4 的裁决组成部分）。

## Technical Context

**Language/Version**: Markdown 约定面（owner 文档 + 模板）+ Python ≥3.8 仅标准库（检查器）；测试为仓库既有 pytest 契约层
**Primary Dependencies**: 既有 `scripts/python/glossary-utils.py`（读取模式复用，不改行为）、`sync-mirrors.py`（六对镜像）、`generate-instructions.sh`（instructions 产出）、`scan-confirmation-gates.py`（预算核量）；**不新增**任何第三方依赖、不引入网络或模型 API
**Storage**: owner 文档与 ambient 小节为框架源文件；E6 存量差异清单与 E7 关键词快照为 dated record，按执行日落 `test-evidence/`（一文一件，append-only）；无新机器管理存储
**Testing**: Tests Mode ON。`tests/contract/test_bilingual_expression.py` red-first（对象见 quickstart 各 Pinned by）；plan 期定向集 = 仅文档改动，`not-run-docs-only`（targeted-set-v1 输出见 `test-evidence/plan.jsonl`）
**Target Platform**: 仓库工具链（Linux/macOS），Python ≥3.8；检查器为只读扫描、无常驻、无平台分支
**Project Type**: 框架源（两顶帽子：编辑面 = `shared/`、`templates/`、`scripts/`、`tests/`；`.specify/` 副本经 `sync-mirrors.py` 产出，`.specify/instructions.md` 与根 `AGENTS.md` 经 `generate-instructions.sh` 产出，均 MUST NOT 手改）
**Performance Goals**: 单次 `scan` 为覆盖面清单内文件的线性读取（R-11：census 全查墙钟 > 60s 触发抽样决策重开）；无递归全仓遍历、无轮询、无后台进程
**Constraints**: 唯一形态逐字为 [[STR-002]] / [[STR-003]]（半角、紧贴，A4 用户裁决）；ambient 小节 MUST NOT 含枚举复述 / 本仓专属路径 / 阻断式确认句（R-4/R-5：模板 27,940 B、live 32,259 B，预算只报 warning 但报告须留档）；检查器 MUST NOT 进入围栏代码块与行内代码（C-004）、MUST NOT 判语义（C-012）；镜像判据 = 相对 plan 期基线无新增漂移（不以绝对全绿为判据）
**Scale/Scope**: 1 份 owner 文档 + 1 个 ambient 小节 + 1 个检查器脚本 + 1 个契约测试文件（含夹具）+ Feature/ID 登记；镜像三面（shared/templates/scripts）；`--scope changed` 的 SC-002 分母只含改动路径信号行

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（动态枚举自 `.specify/memory/constitution.md`，共 18 项；同作者降级说明见本节末）:

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | Pass | 18 条 FR 逐条映射到设计落点（`feature-ref.md` FR 表）；形态/入口/测量三处 plan 期决定各有研究记录（research.md R-10/R-11）与契约条款（contracts/checker.md、contracts/measurement.md） |
| II | Feature-Centric Development | Pass | 绑定新建 Feature 078（requirements § Related Feature 复核五候选）；本 plan 只推进 `Draft → Planned`，不新建/合并/废弃其他 Feature；索引行与详情同阶段更新 |
| III | Intent-Driven Development | Pass | 先定「约定归属谁、守卫判什么不判什么、测量从哪采」，再定形态；四条承重取舍以 DTR 留反面与代价（## Decision Tensions T-001…T-004） |
| IV | Test-First & Contract-Driven Implementation | Pass | `test_bilingual_expression.py` red-first，起点 = 本次实测的红（检查器、owner 文档、ambient 小节均不存在）；夹具合规/违规对（quickstart S2）先行钉定期望 |
| V | AI Agent Integration Standards | Pass | 不改 `AGENT_CONFIG` / `_ASSISTANT_TIERS`；本特性显式排除命令模板改写，per-tool 命令副本面零触碰（feature-ref.md FR-008 落点只在 instructions 模板） |
| VI | Continuous Quality & Observability | Pass | 判定全走退出码与封闭 finding 码；plan 期证据按执行时全量捕获落 `test-evidence/`（镜像基线、docs-utils 基线、确认门、S4 管道冒烟）；判据用「相对基线无新增漂移」而非绝对绿；无 `.bak` 类副本 |
| VII | Specification-Plan-Task-Implementation Workflow | Pass | reuse-first 已在 requirements 完成并登记绑定；本阶段不落 `Implemented`；Pre-Status-Flip Gate 留给 implement；template-only 交付物的 Test-First 按宪法 VII 条款判 Partial 的路径不存在——本特性有真实可执行检查器，测试对象是它 |
| VIII | Code as the Single Source of Truth | Pass | 全部现状以实测校准：M-1…M-7、镜像六对文件数、docs-utils violations=4、确认门 27/0、instructions 字节数均有 2026-10-30 原始输出（test-evidence/），未凭印象断言 |
| IX | Framework Scope Discipline (No Over-Engineering) | Pass | 交付物 = owner 文档 + ambient 小节 + 检查器 + 契约测试 + 登记（FR-015）；检查器为单文件 stdlib 脚本，无引擎、无服务、无第二份台账；`census` 超限的重开条件是改测量方式而非加平台 |
| X | Documentation Naming & Location Conventions | Pass | owner 文档走 `shared/guidelines/`（同类兄弟 guidelines 目录的 kebab-case 命名，`bilingual-expression` 为 requirements 既定 slug）；契约测试走 `tests/contract/test_<subject>.py`；夹具走 `tests/fixtures/bilingual/`；不碰保留文件名 |
| XI | Dogfooding (Self-Application) | Pass | 改动全落框架源，`.specify/` 副本经既有机制产出（contracts/distribution.md C-001）；本线自身走完整阶段链并在 requirements 头部先行自用双语形态（`双语表述（Bilingual Expression）`） |
| XII | Tool Reuse Over Ad-Hoc Generation | Pass | 复用 `glossary-utils.py` 读取模式、`sync-mirrors.py`、`generate-instructions.sh`、`doc-consistency-check.py`（只读判定，不并入）；`.specify/memory/tools/` 无同能力记录，新检查器即「无 Tool 时写代码」的预期结果 |
| XIII | Better-Harness Orientation (Improvement North Star) | Pass | 强化 Task Understanding（定义处信号 S1…S4 让作者可自判）与 Change Validation（机械守卫把人工核验降为程序判定，但语义面留评审，configured ≠ used）；证据区分程序判决与评审判断（measurement.md C-004） |
| XIV | One Source of Truth (Authority & Reference Discipline) | Pass | 六组事实唯一 owner = [[STR-001]]；ambient/契约/测试只引用不复述（owner-document.md C-007、distribution.md C-003）；关键词表程序派生不手写（measurement.md C-001）；漂移守卫 = 契约测试（distribution.md C-006） |
| XV | User-Facing Comprehension (No-Jargon, With Context) | Pass | owner 文档头部按全局基准读者声明 Readers/Reading scenario（C-001，复用 `user-facing-comprehension.md` 基准，不新建第二套）；检查器 finding 行 `file:line [code] message` 自带定位，读者无需内部知识即可行动 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | Pass | 承重裁决（A2/A4 及其重开条件）在 requirements 留痕并在本 plan 以 DTR 承接；「检查器不签字语义」的绿被显式标注为读者-oracle 而非充分条件（A7、checker.md C-012）；本 plan 无静默就地修平的裁定类异常（§ Assumptions 记录两项自行裁决） |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | Pass | 不新建目录：owner 文档落既有 `shared/guidelines/`，夹具落既有 `tests/fixtures/`，plan 期临时产物落受认可根 `.specify/.tmp/078-bilingual-expression/`（`.specify/.gitignore` 已匹配 `.tmp/`，S4 pilot 已拆除留档） |
| XVIII | Grounded Naming | Pass | 命名来源序：用户词「双语表述」→ slug `bilingual-expression`（requirements 既定）→ 同类兄弟（`doc-consistency-check.py` 的 `<domain>-check.py` 形态定检查器名）；[[STR-001]]/[[STR-002]]/[[STR-003]] 经 `[[STR-NNN]]` 引用不复制字面量 |

**Gates Status**: 全部 18 项 Pass，无 Fail / Partial；## Complexity Tracking 记 N/A。

**Re-check after Phase 1**: 2026-10-30——Phase 1 产物（`research.md`、`data-model.md`、4 份契约、`quickstart.md`、`feature-ref.md`）落盘后复核：18 项维持 Pass；新增证据 = 4 份契约全部 `md-bold-closed`、FR 车道 uncovered = 0（`test-evidence/plan-account-clause-coverage.txt`）、S4 管道冒烟实测成功。复核无 Partial 行。

**Same-author gate**（`.specify/shared/workflow/objective-analysis-gate.md`）：本 run 从 requirements 到 plan 无断点，被评分工件由本 agent 在本会话内产出，按该 owner 应委派新鲜上下文只读子代理。本执行环境未向执行 agent 暴露子代理派发工具（工具面只有文件读写、检索与命令执行），按该 owner 的 subagent-unavailable 降级形态，本表与 Post-Generation Quality Gate 均走直接受限读，标记为 **(detected: direct read, subagent unavailable)**——逐行自我评分，可信度低于委派路径，读者应据此折算权重。

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing
threshold: `.specify/shared/guidelines/decision-tension.md` — one pointer, read from the repository
root. This section lists the field names and points at that file; it does not restate the criteria
table, the rejection list or the threshold table.*

### T-001 — owner 文档新建独立 guidelines 文件，而不是扩展词汇表/读者理解纪律的既有 owner

- **decision**: 双语约定的六组事实落在新建 [[STR-001]]，不扩展 `shared/workflow/glossary.md` 或 `shared/guidelines/user-facing-comprehension.md`。
- **antithesis**: 扩展 `shared/workflow/glossary.md` 承接方向/形态规则（它是术语相关协议的既有 owner）；当「双语形态被读作术语登记纪律的一部分、且维护者已习惯改术语时只开词汇表」时它更优——规则与词条同文件，一次编辑完成两处维护。
- **binding_constraints**:
  - pole_a: 约定必须有一个可整体引用的单文件 owner（FR-001），消费方以「路径 + 锚」到达；owner 的自我声明必须能逐字点名拥有的六组事实。
  - pole_b: 概念上双语形态属词汇/写作纪律，放错 owner 会让词汇表协议文件的自我声明失真（glossary 协议 owner 的声明面是 Closed-Set 的登记协议，不含写作形态规则）。
- **discriminating_evidence**: 把豁免面七项枚举写进 `shared/workflow/glossary.md` 头部，检查该文件的 owner 声明是否需要随之修订；结果二值——其声明面仍逐字成立（是／否）。成立（是）说明协议文件未被规则撑大，独立 owner 是正确的；不成立（否）说明规则只能找新 owner。
- **expected_sacrifice**: SC-001 Source ↓ `shared/guidelines/` 目录文件数 +1（60 → 61，2026-10-30 实测），跨纪律检索多一个打开目标。
- **revision_trigger**: 两个迭代内出现 ≥2 次「修订双语规则时同时必须修订词汇表协议文件、且两处修订总是同批提交」→ 重开，评估合并 owner；合并时 MUST 走两份 owner 文件的自我声明修订，MUST NOT 静默搬移。

### T-002 — 新建独立检查器脚本，而不是给 doc-consistency-check.py 加动作

- **decision**: 双语形态检查落新建 `scripts/python/bilingual-expression-check.py`；MUST NOT 给 `doc-consistency-check.py` 增加 `--action bilingual`。
- **antithesis**: 给 `doc-consistency-check.py` 加 `--action bilingual`（077 加 `--action structure` 的同款路径）；当「所有文档类机械判定收敛在一个 CLI、维护者只需记一个入口」时它更优——命令面不增殖，测试基建直接复用。
- **binding_constraints**:
  - pole_a: 六面门禁的守卫引擎 MUST NOT 被非门禁判定牵动——双语扫描的一个缺陷不该让表达类阶段门禁连带转红（其契约测试群钉了 `--faces` 封闭语义）。
  - pole_b: 判定对象与生命周期不同：门禁引擎判**落文文档**（阶段时点、blocking），本检查器判**框架源定义行**（维护者自跑 + review 采证、advisory），耦合后 advisory 缺陷会污染 blocking 面。
- **discriminating_evidence**: 在仓库临时副本中使双语扫描抛异常，分别观察 `doc-consistency-check.py --faces reader`（既有门禁）是否连带不可用；结果二值——仍可用（是／否）。独立脚本答「是」，同文件加动作答「否」。
- **expected_sacrifice**: SC-002 Source ↓ 命令面 +1（多一个 CLI 入口与其契约测试），复用收益只保留在「读取模式」层（glossary-utils 的表解析）。
- **revision_trigger**: 两个迭代内出现 ≥2 次「维护者因入口太多跑漏了双语扫描、且 SC-002 采证因此缺失」→ 重开，评估把 scan 判定迁入 doc-consistency-check 的独立动作（守卫面隔离测试先行），但 `--faces` 封闭语义不动。

### T-003 — 检查器本特性内不接线门禁，SC-002 用 --scope changed 采证

- **decision**: 检查器只交付退出码契约（0/1/2）与运行入口，不绑定任何阶段门禁算子；SC-002 由 review 阶段对改动路径跑 `--scope changed` 采证，存量差异只进 E6 清单。
- **antithesis**: 把 `scan` 接线为表达类某阶段的 blocking 算子（如 implement 的 G-implement-structure 子行）；当「合规率 100% 必须有强制门、否则靠自觉」成为团队共识时它更优——不合规提交在阶段面被拦下。
- **binding_constraints**:
  - pole_a: SC-002 的分母必须只含新写内容（FR-006/FR-016：存量 1383 处全角不追溯），而阶段门禁无法区分「存量面」与「新写面」的语义——全量 blocking 必然把存量差异判红，违反 FR-006。
  - pole_b: 机械守卫 MUST NOT 签字语义（A7/C-012），blocking 化会被读成「结构绿 = 内容合格」，而表达类的最终验收归读者 oracle（A2）。
- **discriminating_evidence**: 在基线提交上对整个覆盖面清单跑一次全量 scan，数 finding 数；结果二值——finding 数 > 0（是／否）。是（现状实测必然 > 0，M-1/M-2），证明全量 blocking 今日即红，只能靠 changed-scope 或基线豁免机制；两条路里 changed-scope 不动门禁接线。
- **expected_sacrifice**: SC-002 Source ↓ 采证依赖 review 阶段的执行纪律（无门禁强制），漏跑的风险由 E3 台账的 `stage-status` 行完整性兜底。
- **revision_trigger**: 一个迭代内出现 ≥1 次「改动路径上的全角形态随提交进入 master」→ 重开，评估把 `--scope changed` 包装为提交前钩子或 stage 子行（存量面显式豁免、只判新增行）。

### T-004 — SC-005 取 100% census 全查，不做抽样

- **decision**: SC-005 的总体 = 词汇表全部双语 Canonical 词条，测量方式为检查器 `census` 动作全查（抽样比例 100%）。
- **antithesis**: 程序抽样（如系统抽样 1/3 条目）+ 人工复核；当「词条规模增长到全查成本不可忽略、且评审时间成为瓶颈」时它更优——成本随总体线性下降。
- **binding_constraints**:
  - pole_a: SC-005 声明「不一致处数为 0」，且 SC-002 已声明「误差 0」——抽样引入的统计误差与「处数为 0」的封闭声明不可兼得。
  - pole_b: 测量成本必须有限：总体 132 条（M-7，dated record）量级下全查必须是单次线性扫描可完成的。
- **discriminating_evidence**: 跑一次 census 并读检查器自报的墙钟；结果二值——≤ 60s（是／否）。是则全查可行且更简；否则重开抽样。
- **expected_sacrifice**: SC-005 Source ↓ 单次测量墙钟随词条数线性增长（现状预计秒级）；词汇表双语条目显著增长后全查成为 review 阶段的时间成本。
- **revision_trigger**: census 墙钟 > 60s（检查器自报，实测）→ 重开，改为程序系统抽样 + 披露抽样比与置信边界，修订 contracts/measurement.md C-007。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/078-bilingual-expression/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — R-1…R-12 实测与研究裁决（无独立外部调研，<50 行结论外加测量留档）
├── data-model.md        # Phase 1 output — E1…E7 实体与校验规则
├── quickstart.md        # Phase 1 output — S1…S8 场景（S4/S5/S6 本次实测，S2/S3/S7/S8 Pinned by）
├── contracts/           # Phase 1 output — 4 份契约（md-bold-closed）
│   ├── owner-document.md   # owner 文档结构与可判定性（C-001…C-009）
│   ├── checker.md          # 检查器行为契约（C-001…C-012）
│   ├── distribution.md     # 分发与两顶帽子（C-001…C-006）
│   └── measurement.md      # SC 测量程序（C-001…C-008）
├── feature-ref.md       # Phase 1 output — 18 FR → 落点 + 5 SC → 证据来源
├── checklists/          # requirements 阶段质量清单（requirements.md）
├── test-evidence/       # plan 期 10 份全量捕获 + plan.jsonl（见 Phase 1 表 Evidence 行）
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement)
```

### Source Code (repository root)

```text
shared/guidelines/bilingual-expression.md        # owner 文档（新建；implement 落文，本 plan § Document Structure 为结构源）
templates/instructions-template.md               # 新增 ambient 小节（## Bilingual Expression (双语表述)，implement 落文）
scripts/python/bilingual-expression-check.py     # 确定性检查器（新建；stdlib only）
tests/contract/test_bilingual_expression.py      # 契约测试（red-first；漂移守卫 C-006 + 夹具断言）
tests/fixtures/bilingual/                        # 夹具（合规/全角违规/同向违规定义行，implement 随测试建立）
.specify/specs/078-bilingual-expression/         # 本特性 spec 产物（非分发载荷，无镜像义务）
```

**Structure Decision**: 本特性是**框架源的约定 + 守卫交付**，不是新组件：一份 owner 文档、一个模板小节、一个单文件检查器、一个契约测试文件。编辑面 = `shared/`、`templates/`、`scripts/`、`tests/`；`.specify/` 同名副本一律经 `sync-mirrors.py` 产出，`.specify/instructions.md` / 根 `AGENTS.md` 经 `generate-instructions.sh` 产出（distribution.md C-001/C-005）。不新建任何目录（夹具落既有 `tests/fixtures/`）。

### Mirror Obligations

镜像对清单的 owner 是 `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS`（六对）；本节登记本特性触碰的三对与命令副本面。**基线**：改动前实测 `sync-mirrors.py --check` 退出码 0、六对全 ok（templates 22 / skills/external 406 / skills/internal 136 / agents 3 / scripts 117 / shared 60 文件），per-tool 命令副本 `OK`；原始输出 `test-evidence/plan-sync-mirrors-baseline.txt`（2026-10-30）。

| # | Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|---|----------------------|---------------------------------------------------|--------|
| 1 | `shared/guidelines/bilingual-expression.md` | `.specify/shared/guidelines/bilingual-expression.md` | 改动后跑 `sync-mirrors.py --check`，判据「shared 对相对基线无新增漂移」且镜像文件存在；绝不手改镜像 |
| 2 | `templates/instructions-template.md` | `.specify/templates/instructions-template.md`；运行时 `.specify/instructions.md` 与根 `AGENTS.md` 由 `generate-instructions.sh` 产出（非镜像对，C-005） | 同 #1（templates 对）+ 生成器 size report 留档 `test-evidence/` |
| 3 | `scripts/python/bilingual-expression-check.py` | `.specify/scripts/python/bilingual-expression-check.py` | 同 #1（scripts 对） |
| 4 | 命令模板面 | 本特性**不触碰** `templates/commands/**`（显式排除项）：per-tool 副本零改动；未来命令/技能引用约定时只走「路径 + 锚」指针形态（FR-001 消费纪律） | `regen-command-copies.py --check` 相对基线无新增漂移（基线实测 `OK`，plan-sync-mirrors-baseline.txt 首行） |

**无镜像面**：`tests/**` 不入任何镜像对；`.specify/specs/078-bilingual-expression/**` 是规格产物、不是分发载荷（`MIRROR_PAIRS` 无此对），只做源文件改动。

## Assumptions（plan 期自行裁决，登记备查）

- **P1（owner-path-missing 的先行裁决）**：`## Document Structure` 的 Fact Owners 表如实引用交付前尚不存在的未来交付物路径（[[STR-001]] 与 `scripts/python/bilingual-expression-check.py`）；`doc-consistency-check.py --action structure` 的 plan 侧解析因此报 `owner-path-missing`（本次实测 3 条，见 `test-evidence/plan-structure-judgement.txt`）直至 implement 落盘。裁决：保持如实引用，不把 owner 伪造为既有文件；该 finding 是**已声明的排期内预期**（implement 首个任务即消），且本阶段结构算子（G-plan-structure）只取 docs-utils「零新增违规」，不以 `--action structure` 为阻断入口。若 tasks/checklist 阶段出现以 structure 为阻断的消费方，由该阶段重新裁决。
- **P2（ambient 小节位置）**：新小节插在 `templates/instructions-template.md` 的 `## Grounded Naming` 之后（同为「写作纪律」族，与既有 ambient 小节惯例一致）；不改动其他小节的文字。
- **P3（检查器命名）**：`bilingual-expression-check.py`（同类兄弟 `doc-consistency-check.py` 的 `<domain>-check.py` 形态）；动作名 `scan` / `coverage` / `census` 与既有 `--action` 惯例一致。

## Document Structure

*本节是交付文档 [[STR-001]] 的结构源：章节树登记交付文档必须出现的顶层章节；implement 落文后由 `doc-consistency-check.py --action structure --spec-dir <spec dir> --path <delivered>` 做两向比对。*

### Chapter Tree

| 节名 | 父节 | 目的 | 边界 |
|------|------|------|------|
| 头部与 owner 声明 | — | 读者确认本文件是双语表述约定的唯一 owner、拥有六组事实，并知读者基准与阅读场景 | 不含规则正文；正文全部在下属章节 |
| 定义处与可判定信号 | — | 判断一行是否「定义处」、命中 S1…S4 哪个信号；知道「首次定义」语义判断不在机械范围 | 不判定提及处；不判语义 |
| 方向规则与唯一形态 | — | 判断方向（随文档主语言）、括号宽度（半角）、紧贴形态、大小写逐字匹配是否合规 | 不判翻译质量（显式排除项） |
| 覆盖定义面（封闭集） | — | 判断某定义面是否必须双语；封闭集增删只能经本文件修订 | 清单本身之外的面不受约束 |
| 豁免面（封闭集） | — | 判断某处内容是否豁免（代码标识符、路径、命令字面量、API 名、YAML/JSON 键、第三方专名、公认缩写首次定义后） | 豁免不取消「首次定义处双语」（第三方专名条款除外） |
| 一致性与词汇表 | — | 判断跨文档用词冲突时以谁为准（词汇表 Canonical 中文侧逐字一致，不一致以词汇表为准并登记变体） | 不承载词条本身；词汇表协议归 `shared/workflow/glossary.md` |
| 迁移边界与存量差异 | — | 判断存量不合规内容是否需要改（不追溯；随自然修订收敛） | 不承载差异清单（指针到检查器输出 E6） |
| 与相邻纪律的交界 | — | 判断本约定与 jargon 白名单、One Source Of Truth 的交界处理 | 不重述相邻纪律正文，只给指针 |
| 检查器与守卫 | — | 知道机械守卫的入口、能判什么（三类机械判定）与不能判什么（语义） | 行为契约全文归 `contracts/checker.md`，本节只指针 |

### Reader Baseline

**Readers**: 框架维护者（编写与评审 `shared/`、`templates/` 文档的作者）、词汇表维护者、下游项目使用者——复用 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者，不新建第二套读者定义
**Reading scenario**: 判断一处概念/流程的定义行是否必须双语、其形态（方向/括号宽度/紧贴/用词）是否合规时打开 owner 文档核对对应章节，并据其决定提交或放行

### Evidence List

| 断言 | 证据等级 | as-of | source |
|------|----------|-------|--------|
| 现状双语形态分布（M-1…M-7：1609 半角 / 1383 全角 / 32 混用文件 / 37 EN-first / 31 无双语 / 词汇表 132/161） | 实测 | 2026-10-30 | `requirements.md` § 现状锚点（重算脚本文字描述见该节；parser 行为归 `glossary-utils.py`） |
| 镜像六对基线全 ok（22/406/136/3/117/60 文件），命令副本 OK | 实测 | 2026-10-30 | `test-evidence/plan-sync-mirrors-baseline.txt`（`sync-mirrors.py --check` 原始输出） |
| docs-utils 既有 violations = 4（broken-link 3 + note-frontmatter 1） | 实测 | 2026-10-30 | `test-evidence/plan-docs-utils-validate-baseline.txt`（`docs-utils.py --action validate` 原始输出） |
| 确认门 blocking 27（destructive 20 / governance_kept 7），violations 0 | 实测 | 2026-10-30 | `test-evidence/plan-scan-confirmation-gates.txt`（`scan-confirmation-gates.py --summary` 原始输出） |
| instructions 模板 27,940 B / live 32,259 B；预算机制只报 warning | 实测 | 2026-10-30 | `research.md` R-5（`wc -c` 实测 + `generate-instructions.sh` 的 `INSTRUCTIONS_BUDGET_BYTES` 为数值唯一 owner） |
| 下游 instructions 生成管道可达（pilot 28,005 B / 30 小节，setup 与 teardown 均验证） | 实测 | 2026-10-30 | `test-evidence/s4-pilot-pipeline-smoke.txt` |
| 三项基线：门禁调用 2 / 人工确认 0 / 墙钟 null（analyze 未运行） | 实测 | 2026-10-30 | `research.md` R-8（`exec-quant.py --action list-records` + `feedback-utils.py --action list` + `git log --diff-filter=A` 三通道实测） |
| 077 表达类 plan 形制先例（contracts/FR 车道/Mirror Obligations 基线法） | 引用 | 2026-10-30 | `.specify/specs/077-doc-sdd-integration/plan.md` |
| 检查器不绑定门禁算子、SC-005 抽样推迟至 plan 属规格内分阶段授权 | 引用 | 2026-10-30 | `requirements.md` FR-010 + § Clarifications Session 2026-10-30 末行 |

### Fact Owners

| 事实 | owner 路径 | 章节锚 |
|------|------------|--------|
| 双语规则六组事实（方向、形态、覆盖面、豁免、一致性、迁移） | `shared/guidelines/bilingual-expression.md` | § 方向规则与唯一形态 / § 覆盖定义面 / § 豁免面 / § 一致性与词汇表 / § 迁移边界（落文时逐节成锚；plan 期章节名见 Chapter Tree） |
| 定义处可判定信号 S1…S4 | `shared/guidelines/bilingual-expression.md` | § 定义处与可判定信号 |
| 读者基准 | `.specify/shared/guidelines/user-facing-comprehension.md` | § 基准读者与覆盖协议 |
| 词汇表登记协议 | `shared/workflow/glossary.md` | 整文件（协议即判据） |
| 跨文档一致性判定基准（词条） | `.specify/memory/glossary.md` | Canonical 列 |
| 检查器行为（入口/退出码/扫描规则/判定边界） | `scripts/python/bilingual-expression-check.py` | 整文件（代码与契约并读；行为契约 contracts/checker.md 并参） |
| SC 测量程序 | `.specify/specs/078-bilingual-expression/contracts/measurement.md` | 整文件 |
| ambient 小节形态 | `templates/instructions-template.md` | § Bilingual Expression (双语表述) |
| 镜像对清单 | `scripts/python/sync-mirrors.py` | `MIRROR_PAIRS` 常量 |

*P1（§ Assumptions）已声明：六组事实与信号的 owner 行引用交付前尚不存在的 [[STR-001]]，plan 侧 `--action structure` 的 `owner-path-missing` 为排期内的预期 finding，implement 落文即消。*

## Complexity Tracking

N/A——Constitution Check 18 项全部 Pass，无 Fail / Partial 行需要理由。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | R-1…R-12 条（10 条实测 + 1 条裁决输入 + 1 条基线冻结 + 3 条披露）；三项基线冻结于 R-8 |
| Data model | [`data-model.md`](data-model.md) | 7 entities（E1 约定 / E2 定义处 / E3 术语条目 / E4 检查器 / E5 ambient 小节 / E6 存量差异清单 / E7 关键词基线快照） |
| Contracts | [`contracts/`](contracts/) | 4 files：`owner-document.md`(9) / `checker.md`(12) / `distribution.md`(6) / `measurement.md`(8) = **35 条款**（`clause_extract.py` 实测，见 `test-evidence/plan-clause-extract.txt`） |
| Quickstart | [`quickstart.md`](quickstart.md) | 8 scenarios（S1 读者核对 / S2 形态判定×3 / S3 覆盖面 / S4 下游生成 / S5 镜像漂移 / S6 结构面 / S7 关键词扫描 / S8 census）；S4/S5/S6 本次实测，S2/S3/S7/S8 Pinned by 具名测试 |
| Feature reference | [`feature-ref.md`](feature-ref.md) | 18 条 FR → 设计落点 + 5 条 SC → 证据来源 |
| Evidence | `test-evidence/` | plan 期 10 份 + E3 行：基线 4 份（`plan-sync-mirrors-baseline.txt`、`plan-docs-utils-validate-baseline.txt`、`plan-scan-confirmation-gates.txt`、`s4-pilot-pipeline-smoke.txt`）+ 判定 4 份（`plan-clause-extract.txt`、`plan-account-clause-coverage.txt`、`plan-decision-tensions.txt`、`plan-pre-analyze-check.txt`）+ 复核 2 份（`plan-docs-utils-validate-postedit.txt`、`plan-structure-judgement.txt`）+ `plan.jsonl`（E3 stage-status，not-run-docs-only） |

**与 Phase 0 预期的偏差**：契约份数（4）与章节预设在写契约前未钉数字，条款数（35）落盘后由 `clause_extract.py` 读数回填；FR 车道实测 uncovered = 0（18/18），无偏差。
