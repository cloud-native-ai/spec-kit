# Implementation Plan: /speckit.seal — 按 review 结论封装 spec 与分片合并回写（Split Merge-Back & Seal）

**Branch**: `099-speckit-seal` | **Date**: 2026-11-10 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `099-speckit-seal` → Feature 099 Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写）
**Input**: Specification from `.specify/specs/099-speckit-seal/requirements.md`（28 FR / 9 SC，requirements + clarify 已校验，2026-11-10）

## Summary

框架的状态机在 `Ready for Review` 之后只有一条从未被任何程序执行的声明式出口（`→ Completed`；
带箭头的 `grep` 命中只有 `summarize-project` 的叙述映射，模板以表格行声明同一转移，无执行面，见 research R-03），
归档入口也从不查询状态（R-04）。更具体的缺口是
**拆分交付**：074 的两片已各自闭合（32/32、26/26）却从未并回父级，父 `tasks.md` 仍挂 57 个
`[ ]`（本日实测），父级没有 `review.md`/`code-review.md`，且父 requirements 的 SC 行缺 `**Path**`
标记使闭包引擎实测 exit 2（R-09）。

本特性交付 **`/speckit.seal`**：一个命令模板、一个 internal 技能、一个 stdlib-only 确定性引擎
`scripts/python/seal-utils.py`（四个动作 `merge-plan` / `merge-apply` / `seal` / `archive-gate`），
以及两个按 spec 的记录文件：封装回执 `seal.md` 与合并清单 `merge-manifest.json`。状态面只在
既有 owner 上新增一个值 `Sealed` 与一条转移 `Ready for Review → Sealed`；`Sealed` 是新工作唯一的
终态，`Completed` 只作为遗留记录值保留；任何归档/退休入口通过 `archive-gate` 查询「只有 `Sealed`
可归档」，准入判定只有 seal 引擎一个 owner。

合并回写按「同名输出件」为单位、按声明顺序逐分片合并：编号按分片声明的映射表复用父 ID、
分片独有 ID 按合并顺序追加，所有引用改写为合并后 ID；共享字符串解析到合并后的唯一父级注册表；
一切无法确定性归并的差异进入冲突清单并阻断封装——**不静默择一**。散文类产物以父级文本为权威、
分片独有章节进入带来源标注的区块；语义等价由分片声明的映射表证成，引擎不以模型转述判断「意思相同」。

**074 真实回合**（SC-006）是本特性的第一次验收：以 `.specify/specs/074-goal-team-sdd-unification/`
为目标执行 split → merge-back → seal 全流程，五项实测输入缺陷（缺 `Path` 标记、STR 同号不同义、
出厂文档引用分片本地 ID、驱动者记录的 P0 豁免、57 行拆前记录）逐条显式处置；回合终态是二值：
`Sealed` 或至少逐条覆盖五项、并逐条点名额外阻断的拒绝清单。

零新增重复机制：不新增第二套状态机/注册表/归档机制/调度器/并行 spec 树（FR-024，静态可核验）。

## Technical Context

**Language/Version**: Python `>=3.8`（`pyproject.toml` `requires-python`）用于 `scripts/python/seal-utils.py` 与契约测试；Markdown 用于命令模板、技能、owner 页、契约与记录。
**Primary Dependencies**: 零新增第三方依赖（引擎 stdlib-only）。按指针复用：`closure-acceptance-check.py`（验收裁决唯一来源，子进程调用并逐字复用负载）、`validate-requirements.py` / `validate-tasks.py`（合并后事后校验）、`declaration_reader.py`（若读声明事实）、`script_interface_cli.py`（`--help`/`--version` 共享守卫）、`sync-mirrors.py` + `regen-command-copies.py`（镜像与副本投影）、`scripts/bash/run-tests.sh`（唯一测试入口）。
**Storage**: 文件系统既有面——父 spec 目录的 `seal.md` 与 `merge-manifest.json`（每 spec 一文件、并发不相交）；状态只写 `.specify/features.md` 行与 `.specify/features/<ID>.md`；分片目录在 `requirements.md` 头部获得一行 `**Merged into**:` 标注。无数据库、无服务、无共享可变聚合。
**Testing**: pytest（`contract` / `integration` / `serial` 标记）；Tests Mode ON。入口唯一：`bash scripts/bash/run-tests.sh`（默认并行，参数透传）。判据是「对基线零新增失败 + 本特性全部新测试绿」，基线在实现入口实测并记名。
**Target Platform**: macOS/Linux 维护者主机与所有由本框架初始化的下游项目；框架源编辑经 publish → install → `specify init` 抵达客户运行时。
**Project Type**: SDD 框架（命令模板 + 技能 + Python 引擎 + 状态 owner + 契约测试）；无运行时平台、无调度器、无守护进程。
**Performance Goals**: 无墙钟承诺。质量属性是**确定性**与**幂等**：同输入逐字节同输出；`merge-apply` / `seal` 重跑零 diff 或幂等返回。
**Constraints**: 引擎仅标准库；动作封闭集恰四动作；退出码封闭集 `0` 成功/幂等 · `1` 前置条件拒绝 · `2` 输入或环境错误；每次判定由程序给出；不移动/删除/归档 spec 目录、不 push、不触碰 goal/team 树；`--help`/`--version` 零副作用、未声明选项非零拒绝（宪法 XXI）。
**Scale/Scope**: 28 FR / 9 SC；1 个新引擎（约 4 动作 + 内部合并器）；1 个命令模板 + 1 个 internal 技能；6 处状态声明 carrier + 3 处现有测试 pin 同步；2 个既有引擎消费面扩展（闭包判定家族、non-disposable 状态表）；9 个工作包（每包 ≤16 行，见 § Execution Model）。074 回合的输入规模：2 分片、15 类候选输出件、3 份 requirements、3 份 tasks（57/32/26 行）。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md`, 22 principles in document order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每条设计裁决引用 FR id；`feature-ref.md` § Delivery map 覆盖 28/28 FR；074 回合由 FR-026/SC-006 直接规定。 |
| II | Feature-Centric Development | ✅ Pass | 本阶段创建 Feature 099 注册行与 `.specify/features/099-speckit-seal.md`，状态 `Draft → Planned`；同步复核无新增/废弃 Feature。 |
| III | Intent-Driven Development | ✅ Pass | 设计全部追溯到 D-074-R1/R2/R3 访谈裁定（转述见 research R-21）与 clarify 十条裁定；两条开放形态（散文合并边界、阻断验收）记为 T-001/T-005 并附反题。 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Tests Mode ON；`contracts/records-and-boundaries` C-045 给出 SC→红先模块映射；`feature-ref.md` § Measurement map 逐 SC 点名首红模块与变异取证。 |
| V | AI Agent Integration Standards | ✅ Pass | 不触碰 `AGENT_CONFIG` / `_ASSISTANT_TIERS`；新命令副本由 `regen-command-copies.py` 生成，六工具映射原样复用。 |
| VI | Continuous Quality & Observability | ✅ Pass | 引擎三值退出码 + 封闭理由码；manifest 稳定键序与自摘要；拒绝只经 stdout、零持久化；无 `.bak` 备份（回滚靠 git 与原子恢复）。 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify → plan 链完整；本阶段状态上限 `Planned`；`Implemented`/review 门仍归后续阶段。 |
| VIII | Code as the Single Source of Truth | ✅ Pass | research.md R-01…R-20 全部带 file:line 或实测命令；074 读数（57/32/26、exit 2、STR 表）取自本日实测。 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 恰好一个命令、一个技能、一个引擎、两个按 spec 记录文件；无第二注册表/台账/调度器；散文不做「智能合并」。 |
| X | Documentation Naming & Location Conventions | ✅ Pass | `seal.md`、`merge-manifest.json` 为 spec 目录内 lowercase 路径语义名；`seal-artifact` 技能同级命名（先例 `clarify-artifact`）；不新建顶层目录。 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子已点名：框架源编辑（`templates/`、`skills/`、`shared/`、`scripts/`）+ `.specify/` 镜像经 `sync-mirrors.py` 再生；本特性自身走本仓 SDD 链。 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 验收裁决复用闭包引擎（子进程 + 逐字负载）、ID/引用校验复用 `validate-requirements.py`/`validate-tasks.py`、状态表复用 non-disposable owner；仅三件真正新增（拆分记录解析、合并写入器、准入查询）。 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Reliable Delivery（可判定的终态与归档准入）与 Change Validation（闭包回执逐字入证）；证据纪律：`sealed` 只由程序判定。 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 状态值域 owner 唯一（FR-001 指定 `acceptance-hardening.md` § Feature Status；`non-disposable-definitions.md:196` 现行旧指向由 P1 同批收敛，见 research R-01）；归档准入 owner 唯一（seal 引擎）；回执只引用测量、不复述。 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 拒绝报告必须逐条点名全部未满足条件 + 修复路径 + 重跑方式；`quickstart.md` 首次出现处定义 `Sealed`、merge-back、manifest。 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 冲突、state-drift、closure exit 2、dirty-spec-tree 全部具名阻断或退出 2；无静默默认；驱动者豁免不被读作用户裁定。 |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | `skills/internal/seal-artifact/` 是既有目录 kind；`tests/fixtures/seal/` 是既有 fixtures 树下的新主题目录，随本特性说明；无临时目录新增。 |
| XVIII | Grounded Naming | ✅ Pass | 名称全部来自用户词面（`/speckit.seal`、`Sealed`、`seal.md`）或最近同族先例（`seal-artifact` ← `clarify-artifact`；`merge-manifest.json` ← `CONSOLIDATION-LEDGER` 词汇）。 |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | 用户视图只有一问「这条 spec 能否封装/归档」——由一个命令与一份回执回答；动作、ID 家族与检查器留作内部结构。 |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | 全部测试走 `run-tests.sh` 默认并行；新测试无共享全局状态；判据按失败名单比较，不按墙钟。 |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | `seal-utils.py` 的 `--help`/`--version` 零副作用、未声明选项非零拒绝（复用 `script_interface_cli.py` 守卫），由引擎契约测试钉住。 |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | 本 plan 携带任务锚（FR/SC + 074 回合）与规则锚（无人值守、门禁、fast-fail、预算）；§ Execution Model 把 fast-fail 注入条款写进每个包派发要求。 |

**Gates Status**: ✅ 22 行全部 Pass。无 ❌ / ⚠ 行；§ Complexity Tracking 记 `N/A`。

**Re-check after Phase 1**: 2026-11-10 — 对照已落盘的 Phase 1 产物（`data-model.md`、4 份契约、
`quickstart.md`、`feature-ref.md`）重读。第 I/IV/XIV 行按新产物刷新：FR→条款映射由 `feature-ref.md`
从契约引用组再生（28/28）、SC→红先模块补齐（9/9）、状态与准入两处 owner 各只出现一次。无行改判。

## Decision Tensions

Owner of the record shape, admissibility, rejection forms and the load-bearing threshold:
`.specify/shared/guidelines/decision-tension.md`. Fields: `decision`, `antithesis`, `binding_constraints`
(`pole_a` / `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; id `T-NNN`.

### T-001 — 合并确定性只覆盖结构化单元，散文以声明规则合并且映射表是唯一语义依据

- **decision**: 合并只对声明了 ID 家族的结构化单元做确定性归并；散文类产物以父级文本为权威、分片独有章节进入带来源标注区块，语义等价由分片声明的映射表证成，引擎不以模型或文本相似度判断「意思相同」。
- **antithesis**: 由模型做逐段语义合并（三方文本合并 + LLM 判同义），在「只合并一次、每处由人复核」的场合它更优——产物更可读、分片内容能真正融入父级行文，而不必以附录区块形态并列。
- **binding_constraints**:
  - pole_a: 同一输入必须产出逐字节相同的合并产物与冲突清单，重跑零 diff。
  - pole_b: 父级既有章节必须吸收分片对该章节的修订（分片内容融入父级行文），而不是只在附录区块并存。
- **discriminating_evidence**: 对同一夹具树连跑两次比较 sha256，并把任一排序键改为「返回时刻」注入变异，跑契约套件；结果二值：两次一致且变异转红 / 任一不成立。
- **expected_sacrifice**: SC-003 Source ↓ 散文不再获得语义润色，分片独有内容只能以带来源标注的区块出现在父级，读者需跨区块阅读。
- **revision_trigger**: 连续两个真实回合出现「按声明规则产出的合并视图无法使用、必须人工重写 >50% 章节」≥2 次 → 重开，评估引入经声明的语义合并步骤（附独立验证与可复现输入）。
- **tension_id**: T-001

### T-002 — `Sealed` 成为新工作唯一终态，`Ready for Review → Completed` 对新转移关闭

- **decision**: 状态值域新增 `Sealed` 并把它定为新工作唯一终态；`Completed` 仅作为遗留记录值保留（不追溯、不降级），全部面向新工作的「终态」表述改说 `Sealed`。
- **antithesis**: 直接复用 `Completed` 表示封装终态（零值域改动），或让双终态并存；当「既有外部消费面只认 `Completed` 且无法同批扩展」时它更优——零迁移、零叙述收敛。
- **binding_constraints**:
  - pole_a: 归档准入必须由一个可判定状态回答，终态不能是二义的。
  - pole_b: 既有 21 条 `Completed` 行与下游叙述不能被追溯改写或一夜失效。
- **discriminating_evidence**: 在注册表行与特性详情各写入 `Sealed` 后运行三处漂移守卫与 `archive-gate` 查询；结果二值：全部识别且准入放行 / 任一处未识别或准入拒绝。
- **expected_sacrifice**: SC-001 Source ↓ 一次性同步 6 处声明 carrier、3 处测试 pin 与叙述面（含宪法生命周期段），变更面显著大于一次字段赋值。
- **revision_trigger**: 出现「合法的新工作因外部工具只认 `Completed` 而无法归档」≥2 次 → 重开，评估在消费端增加只读映射（仍不恢复第二终态）。
- **tension_id**: T-002

### T-003 — 编号重排采用「父映射复用 + 分片独有按合并顺序追加」

- **decision**: 有父映射的分片 ID 一律改用父 ID；无父映射的分片独有 ID 按合并顺序追加到父序列（连续、无洞、无重复），映射表写入合并清单；合并视为一次新分配，不经过 `renumber-utils.py`「不压缩空洞」的道义。
- **antithesis**: 保留分片本地 ID 并加命名空间前缀（如 `074b-T001`）；当「合并产物主要供人读、机器 ID 连续性不是判据」时它更优——零重编号、来源一眼可见。
- **binding_constraints**:
  - pole_a: 合并后的父级必须能被既有验证器（连续性、引用可解析）原样判绿。
  - pole_b: 分片来源必须可追溯，原文行文本（除 ID 前缀外）逐字保留。
- **discriminating_evidence**: 合并后对父级运行 `validate-requirements.py` 与 `validate-tasks.py`；结果二值：两项均 0 error / 任一报 error。
- **expected_sacrifice**: SC-004 Source ↓ 任务行与条目的 ID 前缀被机械改写，合并 diff 面变大；追溯依赖 manifest 而非肉眼 ID。
- **revision_trigger**: 合并后出现「分片原 ID 无法在 manifest 之外还原」≥2 次 → 重开，改用命名空间前缀并同步扩展验证器。
- **tension_id**: T-003

### T-004 — 归档准入门只有一个 owner：seal 引擎的 `archive-gate` 只读查询

- **decision**: 「只有 `Sealed` 可归档」的判定只在 seal 引擎实现一次；`/speckit.sanitize` 归档 lane、docs lane、`/speckit.feature` 归档指针与 `/speckit.goal` 之外的任何退休入口都只按指针查询，不自判。
- **antithesis**: 每个归档 lane 各自读状态自行判定（或复制一份 `status == Sealed` 检查）；当「lane 数量少且引擎不可调用」时它更优——零跨组件依赖、零子进程成本。
- **binding_constraints**:
  - pole_a: 准入必须单一实现，复制到第二处时守卫测试必须转红。
  - pole_b: lane 在引擎暂时缺席时必须给出可诊断的拒绝而不是静默放行。
- **discriminating_evidence**: 把准入判定复制进第二个消费脚本并运行单一 owner 契约测试；结果二值：测试转红 / 不转红。
- **expected_sacrifice**: SC-007 Source ↓ 每个归档 lane 增加一次子进程查询与一条拒绝路径。
- **revision_trigger**: 引擎缺席导致归档 lane 连续 2 个迭代不可用 → 重开，评估把查询降级为声明式事实文件（owner 仍唯一）。
- **tension_id**: T-004

### T-005 — 074 回合的验收对象是完整裁决，允许以具名阻断结束

- **decision**: 074 回合的通过标准是「可执行、可复现、逐条点名的完整裁决」；驱动者记录的 P0 豁免不构成用户豁免，回合可以合法地以阻断终态收尾，归档推迟。
- **antithesis**: 把回合验收定义为「必须 `Sealed`」，必要时由本特性临时修复 P0 或自判豁免；当「用户明确要求 074 必须在本期内归档」时它更优——一次收口、无外部依赖。
- **binding_constraints**:
  - pole_a: 绿只能来自用户裁定或修复证据，代理的确认与「无人反对」不是豁免。
  - pole_b: 回合必须可执行到底并给出二值终态，不能停在「无法判定」。
- **discriminating_evidence**: 在 074b P0 仍只有驱动者记录的状态下运行 `seal`；结果二值：`Sealed` / 至少逐条覆盖五项实测输入、并逐条点名额外阻断的拒绝清单。
- **expected_sacrifice**: SC-006 Source ↓ 074 的归档时点后移到用户裁定或修复落地之后。
- **revision_trigger**: 用户对 P0 给出显式裁定，或修复证据落地 → 立即重跑同一回合（同一确定性清单机制），不改变判定代码。
- **tension_id**: T-005

### T-006 — 合并写面封闭：父 spec 目录 + 分片标注 + 已记录的出厂文档修正

- **decision**: 合并与封装只写父 spec 目录、分片 `requirements.md` 的一行 `**Merged into**` 标注、以及 FR-016 记录过解决方式的出厂文档引用修正；不移动/删除/归档 spec 目录，不触碰 goal/team 树，不 push。
- **antithesis**: 合并完成后即把分片目录移入 `.specify/archive/specs/`（一次动作完成合并与收编）；当「分片价值已确认终结、用户要求即时清理」时它更优——仓库不留下悬挂目录。
- **binding_constraints**:
  - pole_a: dated record 不可改写，分片承载物的保留/退役必须经 non-disposable 复核后决定。
  - pole_b: 仓库不能因为合并而长期保留无主目录。
- **discriminating_evidence**: 静态审计引擎动作表并对运行前后分片目录做路径与哈希对照；结果二值：动作表无 move/delete 且分片内容哈希不变 / 任一出现。
- **expected_sacrifice**: SC-008 Source ↓ 分片退役需要另走非一次性处置复核路径，收尾不在 seal 内一步完成。
- **revision_trigger**: 连续 2 个回合结束时 review 要求清理分片且仍无退役决定 → 重开，评估把「退役建议」作为 manifest 字段输出（仍不执行移动）。
- **tension_id**: T-006

## Project Structure

### Documentation (this spec)

```text
.specify/specs/099-speckit-seal/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (R-01…R-20, all measured 2026-11-10)
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (4 pages)
├── feature-ref.md       # Phase 1 output
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
templates/commands/seal.md                        # NEW command template (thin entry + delegation)
skills/internal/seal-artifact/SKILL.md            # NEW internal skill (orchestration + reporting)
scripts/python/seal-utils.py                      # NEW deterministic engine (4 actions, stdlib-only)
shared/workflow/acceptance-hardening.md           # status schema owner: Sealed domain + transition conditions
shared/workflow/feature-integration.md            # protocol table: /speckit.seal → Ready for Review → Sealed row
shared/definitions/non-disposable-definitions.md  # 7-value domain line + status×verdict table owner (add Sealed)
shared/definitions/flow-class-definitions.md      # ledger rows: /speckit.seal + skill:seal-artifact
shared/definitions/probe-definitions.md           # wrap-up probe entry for the new skill
templates/feature-details-template.md             # carrier: transition row + Status bullet + status-token glossary row
templates/feature-index-template.md               # carrier: closed vocabulary line
skills/internal/manage-features/SKILL.md          # status vocabulary + archive-pointer gate query
skills/internal/sanitize-materials/SKILL.md       # archive lane: archive-gate query step
scripts/python/closure-acceptance-check.py        # consumer extension: Sealed joins the completion-claim family
scripts/python/non-disposable-check.py            # consumer extension: status×verdict rows for Sealed
templates/constitution-template.md                # lifecycle narrative convergence (downstream copy)
.specify/constitution.md                          # lifecycle narrative convergence (live copy) + version bump
tests/contract/test_seal_*.py                     # NEW guard suite (engine, merge, seal, gate, status, boundary)
tests/fixtures/seal/                              # fixture trees (single spec, split pair, conflict injections)
docs/reference/commands/seal.md                   # command reference page
.specify/specs/074-goal-team-sdd-unification/     # round target: merge outputs + seal.md + merge-manifest.json
.specify/features/099-speckit-seal.md             # feature detail (this stage)
.specify/features.md                              # registry row (this stage)
```

**Structure Decision**: 本特性沿「命令模板 → internal 技能 → 确定性引擎」的既有三分形态落点，不新增
目录层级：命令在 `templates/commands/`，技能在既有 `skills/internal/`，引擎在既有 `scripts/python/`，
记录落在既有 spec 目录约定内。`tests/fixtures/seal/` 是既有 `tests/fixtures/` 下的新主题目录（与
`acceptance-hardening/`、`non-disposable/` 同构）。074 回合写面被限制在父 spec 目录与两片各自
`requirements.md` 的一行标注上。

### Mirror Obligations *(mandatory — every changed file has mirrors or generated copies)*

Baseline measured 2026-11-10 before any edit: `sync-mirrors.py --check` exit 0 and
`regen-command-copies.py --check` exit 0 (zero pre-existing drift on every pair below, evidence:
`test-evidence/plan-stage-checks.txt`). The Verify criterion is therefore **no NEW drift** on the pairs
this spec touches — never a bare "all green" re-statement of a pre-measured pass.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/seal.md` | `.claude/commands/speckit.seal.md`; `.github/prompts/speckit.seal.prompt.md`; `.opencode/command/speckit.seal.md`; `.qoder/commands/speckit.seal.md` — via `regen-command-copies.py`; NO `.specify/templates/commands/` mirror (retired) | `python3 scripts/python/regen-command-copies.py --check` reports no drift for the four copies (baseline 0) |
| `skills/internal/seal-artifact/SKILL.md` | `.specify/skills/internal/seal-artifact/SKILL.md` | `sync-mirrors.py --check` no NEW drift on `skills/internal` |
| `scripts/python/seal-utils.py` | `.specify/scripts/python/seal-utils.py` (strict pair) | `sync-mirrors.py --check` no NEW drift on `scripts` (strict extras) |
| `shared/workflow/acceptance-hardening.md` | `.specify/shared/workflow/acceptance-hardening.md` | byte-identical via `sync-mirrors.py --check` |
| `shared/workflow/feature-integration.md` | `.specify/shared/workflow/feature-integration.md` | same |
| `shared/definitions/non-disposable-definitions.md` | `.specify/shared/definitions/non-disposable-definitions.md` | same |
| `shared/definitions/flow-class-definitions.md` | `.specify/shared/definitions/flow-class-definitions.md` | same |
| `shared/definitions/probe-definitions.md` | `.specify/shared/definitions/probe-definitions.md` | same |
| `templates/feature-details-template.md` | `.specify/templates/feature-details-template.md` | same |
| `templates/feature-index-template.md` | `.specify/templates/feature-index-template.md` | same |
| `skills/internal/manage-features/SKILL.md` | `.specify/skills/internal/manage-features/SKILL.md` | same |
| `skills/internal/sanitize-materials/SKILL.md` | `.specify/skills/internal/sanitize-materials/SKILL.md` | same |
| `scripts/python/closure-acceptance-check.py` | `.specify/scripts/python/closure-acceptance-check.py` | same (strict pair) |
| `scripts/python/non-disposable-check.py` | `.specify/scripts/python/non-disposable-check.py` | same (strict pair) |
| `templates/constitution-template.md` | `.specify/templates/constitution-template.md` | same |
| `.specify/constitution.md` | none (live governance file; edited by `/speckit.constitution`) | re-read version/amend date + guard tests green |
| `.specify/skills/internal/seal-artifact/SKILL.md` | generated from the source skill above | regenerated by `sync-mirrors.py --write`, never hand-edited |

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | CPython ≥3.8 标准库足够实现引擎（无第三方依赖） | `pyproject.toml` `requires-python`；本机 `python3` 实测（research R-07） | verified | — |
| EP-002 | pytest 与唯一测试入口可用 | `bash scripts/bash/run-tests.sh tests/contract/test_status_gate_owner.py -q` → 32 passed in 6.17s（2026-11-10 实测） | verified | — |
| EP-003 | 既有状态与验收引擎可就地扩展消费面 | `closure-acceptance-check.py` / `non-disposable-check.py` 调用面与状态表已实测（R-01、R-09） | verified | — |
| EP-004 | 074 实测状态：父 57 开行 / 074a 32 闭 / 074b 26 闭；父 `verification.md` 为聚合指针集；父级无 `review.md`/`code-review.md` | `grep -cE '^- \[ \]'` / `'^- \[X\]'` 实测（R-10）；父 verification.md 为提交 `91726a641` 落盘 | verified | — |
| EP-005 | 074 拆分顺序的声明位于 `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（`proposed_slices` 有序列表） | 该文件 :128–140 实测（R-11） | verified | — |
| EP-006 | 074b 本地 STR-004/005/006 与父级同号不同义 | `.specify/specs/074b-nested-governance/requirements.md:229–237` 与其 Parent Mapping 实测（R-12） | verified | — |
| EP-007 | 出厂文档 `skills/internal/create-team/SKILL.md:99,101` 以 `[[STR-004..006]]` 引用 outcome 字面量 | 两处行内容实测（R-12） | verified | — |
| EP-008 | 074b 的 P0 豁免只有驱动者记录（非 user-authored） | `.specify/features/074-goal-team-sdd-unification.md` § Latest Review 文字实测（R-17） | verified | — |
| EP-009 | 计划入口时 099 尚未注册（bound-but-unregistered；本阶段已创建行与详情） | 入口读数：`.specify/features.md` 89 个特性行、末号 094，`features/099-*.md` 不存在（R-17）；出口读数：注册行 + 详情已落盘（本阶段输出） | verified | — |
| EP-010 | 新增 `Sealed` 会使三处测试 pin 转红（漂移守卫现成） | `test_status_gate_owner.py:396–428`、`test_acceptance_state_machine.py:90–99,491–517`、`test_acceptance_schema_ownership.py:279–318`（R-02） | verified | — |
| EP-011 | 新增命令模板不需要改 `src/specify_cli/`（运行时 glob） | `src/specify_cli/__init__.py:1599–1633` 实测（R-19） | verified | — |
| EP-012 | 父 `requirements.md:5` 的 `**Status**: Draft` 是规格文档状态行，不参与特性状态漂移判定 | 闭包引擎 `resolve_claimed_status` 只读详情与注册表（R-09、R-10） | verified | — |

## Inherited Blockers

Dependency set: none — 本特性不消费任何既有 Feature 的 `## Deferred` 行或 `verification.md` 的
`blocked`/`deferred`/`partial` 行；074 在本特性中是**验收对象**而非依赖：回合所需的 074 输入已全部
实测为可用（EP-004…EP-008），回合结果的处置属本特性自身的验收结论（T-005）。

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| — | (none) | not-applicable | — | — | 依赖集已声明为 `none`；若实现期发现真实依赖，按 owner 的提取集三来源补行并改此声明。 |

## Disclosed Rulings

1. **散文合并的「同一锚点」解释**（T-001）：映射单元（FR/SC/STR）在父级与分片中的**文本差异本身不是冲突**——
   FR-015 已规定映射表是语义对齐的唯一依据，引擎被禁止判断「意思相同」。冲突只发生在映射层
   （无映射 / 目标缺失 / 重复映射）与共享字符串层（同号不同义）；散文冲突只在分片**声明**改写父级
   同一章节时产生（以 `## Parent Mapping` 中的章节行为准）。若后续回合证明该解释不成立，按 T-001 的重开条件回修。
2. **Feature 详情文体**（R-17）：新建 `.specify/features/099-speckit-seal.md` 采用 090/094 的近邻文体
   （Overview / Key Changes / Plan Notes / Related Files），字段与状态语义仍以模板为准；不复写模板的
   Canonical Status State Machine 表，避免在状态域扩展落地前产生一份陈旧副本。
3. **`Sealed` 进入 completion-claim 家族**：`closure-acceptance-check.py` 的 `CLAIMED_IMPLEMENTED`
   扩为含 `Sealed`（封装即声明全部 final 判据已过），使「`Sealed` 行 + block 裁决」成为可检出的矛盾；
   audit 家族随之覆盖 `Sealed` 行。该扩展由 P1 的同批测试pin 与新增守卫固定。
4. **归档准入的调用形态**：`archive-gate` 是只读子进程查询；消费 lane 在引擎不可执行时必须**拒绝放行**并
   显示读取错误（退出 2 的标签透传），不得退化为「未查询即允许」。
5. **回合记录的承载**：FR-026 的「回合记录」= `merge-manifest.json`（冲突与处置）+ `seal.md`（回执或
   豁免引用）；被阻断时 stdout 拒绝清单逐字落 `test-evidence/074-round-*.txt`。不新建第三份台账。

## Execution Model

### Stage execution record（本 plan 阶段）

- `requested`: 4 — 探索波次声明 4 个只读 Explore 作用域（状态面 / 引擎与命令先例 / 074 树 / 合并先例与助手）。
- `effective`: 4 — 四个单元在同一消息内派发并全部 settle；随后进入作者波次。
- `effective_reason`: —（effective 等于 requested，无需理由码）。
- 作者波次（research / plan / data-model / contracts / quickstart / feature-ref）由本会话在同一
  in-process 作者内完成；按 owner 的 carrier 定义，in-process 工作不是被派发单元，不产生区间，不计入读数。

### Work packages（9 包，每包 ≤16 行）

依赖边（→ 表示先行）:`P1 ∥ P2`；`P2 → P3 → P4 → P5`（同一引擎文件，写域相交，串行链）；
`P5 → P6`；`P1 → P7`（P7 的测试基线依赖状态域落定）；`P6 → P7-tests`；`P2…P7 → P8`；`P8 → P9`。
并发窗口：P1 与 P2 可同时启动；P2 链推进时 P7 的文档作者可并行；P6 与 P7 的测试面在 P5 后可并行。
每个包的派发 MUST 注入 fast-fail 条款并要求返回异常行；每包 ≤16 个任务行。

| 包 | 主题 | 写域（文件级） | 行数上限 | 验收锚 |
|----|------|----------------|----------|--------|
| P1 | 状态值域扩展与消费面同步 | `shared/workflow/acceptance-hardening.md`、`feature-integration.md`、`non-disposable-definitions.md`、`templates/feature-details-template.md`、`templates/feature-index-template.md`、`skills/internal/manage-features/SKILL.md`、`scripts/python/{closure,non-disposable}`（状态面）、constitution 两副本（经 manage-constitution 程序）、2 个六值 pin + 1 个域内投影断言复核 + 新漂移守卫 | 16 | `contracts/status-sealed` C-024…C-031；`test_sealed_status_domain.py` 绿、三处旧 pin 更新后绿 |
| P2 | 引擎骨架与 CLI 契约 | `scripts/python/seal-utils.py`（解析/守卫/派发/IO）、`tests/contract/test_seal_engine_contract.py` | 8 | C-001…C-010；`--help`/`--version`/未声明选项/退出码封闭集 |
| P3 | 分片识别与 `merge-plan`（只读） | `seal-utils.py`（plan 段）、`tests/fixtures/seal/`、`tests/contract/test_seal_merge_plan.py` | 14 | C-011…C-018（plan 面）；夹具含「只命中一半条件」与冲突注入 |
| P4 | `merge-apply` 确定性写面 | `seal-utils.py`（apply 段）、`tests/contract/test_seal_merge_apply.py`、`tests/integration/test_seal_merge_determinism.py` | 16 | C-013…C-023；两跑逐字节、重跑零 diff、变异转红 |
| P5 | `seal` 判定与两阶段写入 | `seal-utils.py`（seal 段）、`tests/contract/test_seal_seal.py`、`tests/contract/test_seal_concurrency_and_readonly.py` | 16 | C-005…C-010、C-032…C-039；八类拒绝夹具 + 幂等 + 原子恢复 |
| P6 | `archive-gate` 与既有 lane 接线 | `seal-utils.py`（gate 段）、`skills/internal/sanitize-materials/SKILL.md`、`skills/internal/manage-features/SKILL.md`、`tests/contract/test_seal_archive_gate.py` | 10 | C-030；单 owner 复制注入转红；遗留 `Completed` 路径 |
| P7 | 命令面与名册装配 | `templates/commands/seal.md`、`skills/internal/seal-artifact/SKILL.md`、`probe-definitions.md`、`flow-class-definitions.md`、4 份 per-tool 副本（生成）、名册/台账 pin 测试、`docs/reference/commands/seal.md` | 14 | C-041；`regen --check` 与 `sync --check` 无新增漂移；名册/台账测试绿 |
| P8 | 074 真实回合 | `.specify/specs/074-goal-team-sdd-unification/`（回合产物）、两片 `requirements.md` 标注、`test-evidence/074-round-*.txt`、`tests/integration/test_seal_074_round.py` | 12 | C-043；SC-006 逐项；阻断清单逐条覆盖 FR-027 五项（下限），额外具名阻断逐条点名 |
| P9 | 收尾验证与记录 | 全量测试基线对照、镜像复核、`verification.md`、registry 收尾（implement 阶段）、`tests/contract/test_seal_boundaries.py`、run determination | 8 | SC-001…SC-009 的 Measurement Sources 各有落点；无新增失败名单 |

## Complexity Tracking

N/A — Constitution Check 无 Fail / Partial 行，无需要辩护的违规项。

## Phase 1: Design Artifacts Summary

Backfilled 2026-11-10 after the Phase 1 artifacts landed (all counts taken from the files on disk,
not from memory):

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 14 entities (E1–E14); 16 validation rules (V1–V16); 1 state-transition sketch |
| Contracts | [`contracts/`](contracts/) | 4 files, 45 clauses globally numbered C-001…C-045 (`seal-engine` 10 / `merge-back` 13 / `status-sealed` 8 / `records-and-boundaries` 14); all `md-bold-closed` |
| Quickstart | [`quickstart.md`](quickstart.md) | 9 scenarios (S-1…S-9); S-1 executed at plan time with pasted output; S-2…S-8 carry per-example non-execution disclaimers with premises; S-9 teardown |
| Research | [`research.md`](research.md) | R-01…R-21, all file:line or measured reading |
| Feature reference | [`feature-ref.md`](feature-ref.md) | 28/28 FR → clause map generated from the contracts' citation groups via `clause_extract.py`; 9/9 SC → red-first module map |
| Feature registration | `.specify/features.md` + `.specify/features/099-speckit-seal.md` | Row created, status `Planned`; Total Features 89 → 90 |

Drift from the Phase 0 expectation: none in artifact inventory; the quickstart's file-level execution note
was corrected to `P2–P6` (archive-gate lands in P6), and S-1.3's quoted stderr was corrected to the
verbatim backtick placement measured in this run.
