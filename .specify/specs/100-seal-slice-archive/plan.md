# Implementation Plan: 100-seal-slice-archive

**Branch**: `100-seal-slice-archive` | **Date**: 2026-11-11 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `100-seal-slice-archive` → Feature 099 Speckit Seal
**Input**: Specification from `.specify/specs/100-seal-slice-archive/requirements.md`

> **Concurrency obligation (执行义务，按指针抵达)**: this plan authorizes execution bodies. Each one follows the framework's single concurrency obligation — consider concurrency first, default to it when the class and capability allow, and name a reason code plus record the `requested` / `effective` / `effective_reason` reading when serial. The obligation's authored text is `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; its class table is `shared/declarations/facts/concurrency-class.yaml`, its reason codes `shared/declarations/facts/serial-reason.yaml`, and its reading fields `shared/declarations/facts/effective-concurrency.yaml`. This template restates none of their rules.

## Summary

为 `/speckit.seal` 增加**分片归档步骤**：在 merge-apply 成功后（`Sealed` 或具名阻断均可），把每个已完成合并回写的分片目录整体 `git mv` 到 `<父 spec>/slices/<原分片目录名>/`，产出一份按父 spec 的 `archive-manifest.json`，确定性改写全部活引用、日期化记录保持原字节并只经清单 `from → to` 映射解析，最终在声明的扫描根上「未解析引用 = 0」作为 apply 的合取前置。流程固化在既有三件产物（命令模板、`seal-artifact` 技能、`seal-utils.py` 引擎）内，动作集由四扩为六（+ `archive-plan` / `archive-apply`），不新增命令、不新增第二套归档机制、不删除任何记录，回滚由文档化的 git 级步骤承担。

**设计要点**：① 归档触发取合并清单状态（`merge.status == "merged"`、零开放冲突、分片已闭合、树干净、每片恰在一侧），不取「命令刚写过盘」，也不取 `Sealed`；② 引用分类按「载体封闭集 → 章节/行谓词 → 解析测试」三步程序判定，活引用改写、日期化记录原字节，封闭集外命中 fail closed；③ 归档后 `merge-plan` / `merge-apply` / `seal` 先读归档清单，把归档分片读成同一分片集；④ 引擎写面用数据表表达（白名单 + 归档目标形态），静态审计可判；⑤ 074 回合是本特性的真实验收，读数全部由运行期探针产生、不写死点值。

## Technical Context

**Language/Version**: Python `>=3.8`（`pyproject.toml` `requires-python`）用于 `scripts/python/seal-utils.py` 与契约测试；Markdown 用于命令模板、技能、owner 页与契约。
**Primary Dependencies**: 零新增第三方依赖（引擎 stdlib-only）。按指针复用：`script_interface_cli.py`（`--help`/`--version` 守卫）、`sync-mirrors.py`（镜像投影）、`regen-command-copies.py`（命令副本）、`scripts/bash/run-tests.sh`（唯一测试入口）、`git`（`mv` / `status --porcelain` / `diff --name-status -M`）、既有 099 契约与 non-disposable owner（原地修订，不建第二套）。
**Storage**: 文件系统既有面——父 spec 根的 `archive-manifest.json`（每 spec 一文件）与 `merge-manifest.json`（只改路径字段并重算摘要）；分片目录整体移动；运行期 `.specify/state/**` 可选更新（git-ignored，缺席不阻断）。无数据库、无服务、无共享可变聚合。
**Testing**: pytest（`contract` / `integration` 标记）；Tests Mode ON。入口唯一 `bash scripts/bash/run-tests.sh`（默认并行）；判据是「对实现入口基线零新增失败 + 本特性全部新测试绿」，基线在实现入口实测并记名。
**Target Platform**: macOS/Linux 维护者主机与所有由本框架初始化的下游项目；框架源编辑经 publish → install → `specify init` 抵达客户运行时。
**Project Type**: SDD 框架（命令模板 + 技能 + Python 引擎 + 契约测试）；无运行时平台、无调度器、无守护进程。
**Performance Goals**: 无墙钟承诺。质量属性是**确定性**与**幂等**：同输入两次 `archive-plan` 逐字节一致；成功 `archive-apply` 重跑 `already-archived` 且零 diff；拒绝清单顺序稳定。
**Constraints**: 动作集封闭六值；退出码封闭 `0`（成功/幂等/`not-applicable`）/ `1`（前置拒绝）/ `2`（输入或环境错误）；纯移动（每文件一条重命名对、零纯删除）；清单字段封闭、无墙钟字段；`--help`/`--version` 零副作用、未声明选项 `2`（宪法 XXI）；不删除、不 push、不改注册状态/`seal.md`、不碰 goal/team 树、不写 `.specify/archive/`。
**Scale/Scope**: 28 FR / 10 SC；1 个引擎文件的六动作扩展 + manifest-aware 发现；1 个命令模板 + 1 个 internal 技能（内容扩展，非新建）；2 份既有 owner 页与 6 条 099 契约条款原地修订；3 份新契约页（约 40 条款）；074 回合 = 2 分片 / 112 文件 / 约 1.77 MB；8 个工作包（每包 ≤16 行）。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md`, 22 principles in document order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每条设计裁决引用 FR id；`feature-ref.md` § Delivery map 覆盖 28/28 FR；074 回合由 FR-025/FR-026/SC-001 直接规定。 |
| II | Feature-Centric Development | ✅ Pass | 本阶段不新建 Feature：`100-seal-slice-archive` 经 clarify Mode A 绑定 Feature 099；`features.md` 099 行与详情文件 Last Updated 更新，状态保持 `Ready for Review`（不回退、不推进）。 |
| III | Intent-Driven Development | ✅ Pass | 设计全部追溯到用户原话（归档进父 spec 子目录 + 固化进 seal 流程）与 clarify 五条裁决；六条承重取舍记为 T-001…T-006 并附反题。 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Tests Mode ON；`contracts/archive-actions` 收尾条款给出 SC→红先模块映射；`feature-ref.md` § Measurement map 逐 SC 点名首红模块与变异取证。 |
| V | AI Agent Integration Standards | ✅ Pass | 不触碰 `AGENT_CONFIG` / `_ASSISTANT_TIERS`；`seal.md` 的逐工具副本由 `regen-command-copies.py` 生成，命令名集合不变。 |
| VI | Continuous Quality & Observability | ✅ Pass | 三值退出码 + 封闭 reason 集；清单稳定键序 + 自摘要；拒绝只经 stdout、零持久化；写入中途失败按原字节恢复。 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify → plan 链完整；本阶段状态上限为「绑定 Feature 不推进」；`Implemented` 仍归 `/speckit.implement`。 |
| VIII | Code as the Single Source of Truth | ✅ Pass | research.md R-01…R-14 全部带 file:line 或本日实测；074 读数（58/54 文件、`merge.status=merged`、清单摘要）取自本日解析。 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 恰两个新动作、一份新清单、三份契约页；无第二命令/第二引擎/第二词表/调度器；回滚不新增动作。 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 清单名 `archive-manifest.json`（[[STR-002]]）与 `merge-manifest.json` 同构；`slices/` 为父 spec 内 lowercase 数据目录；命令参考只改既有 `docs/reference/commands/seal.md`；不新建顶层目录，不新增无文档目录（C-113 的 `framework-map.md:38` 登记）。 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子已点名：框架源（`templates/`、`skills/`、`shared/`、`scripts/`、`tests/`）+ `.specify/` 镜像经 `sync-mirrors.py` 再生；本特性自身走本仓 SDD 链。 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 `script_interface_cli.py` 守卫、`sync-mirrors.py`、`regen-command-copies.py`、`run-tests.sh`、C-034 摘要算法；命令模板与技能是 099 已建三件套的内容扩展（C-114），不新建命令或 Tool；仅三件真正新增（归档计划器、引用分类器、清单 schema）。 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Reliable Delivery（合并后残留在流程内收口）与 Change Validation（零丢失哈希 + 未解析=0 双读数）；证据纪律由程序给出。 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 处置词表 owner 唯一（non-disposable § Disposition Set，原地扩目的地）；动作集 owner 唯一（099 C-001，原地扩六）；清单 schema owner 唯一（本特性契约页）；命令模板与命令参考按 099 先例引用 `seal-utils.py --help` 与契约条款，不复述动作集/字段集（C-114）。 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 拒绝报告逐条点名全部未满足条件 + 修复路径 + 重跑命令；`quickstart.md` 首次出现处定义归档、清单、活引用、日期化记录。 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | `partial-archive` / `slice-missing` / `archive-drift` / `unclassified-reference` 全部具名阻断或退出 2；不猜测哪一侧为准。 |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | `slices/` 语义登记进 `framework-map.md:38` 行（FR-002）；无临时目录新增；运行期 state 沿用既有忽略规则。 |
| XVIII | Grounded Naming | ✅ Pass | 名称来自用户词面（`slices/`、归档）或房内同族先例（`archive-plan` / `archive-apply` ← `merge-plan` / `merge-apply`；`archive-manifest.json` ← `merge-manifest.json`）。 |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | 用户视图只有一问「合并完成的分片是否已经归档、引用是否全部可解析」——`quickstart.md` S-2…S-6 只展示 plan / apply / rerun / rollback 四个用户动作，一个命令、一份清单、一个退出码回答；分类器与载体名册留作内部结构（`contracts/reference-classification`）。 |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | 全部测试走 `run-tests.sh` 默认并行；新测试无共享全局状态；判据按失败名单比较，不按墙钟。 |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | 六动作仍复用 `script_interface_cli.py` 守卫（owner：`shared/definitions/script-interface-definitions.md`）；`--help`/`--version` 零副作用、未声明选项 `2`，由 C-115 与引擎契约测试钉住。 |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | 本 plan 携带任务锚（28 FR / 10 SC / 074 回合）与规则锚（门禁、fast-fail、预算）；§ Execution Model 的 P1…P8 每包派发均要求注入 fast-fail 条款并返回异常行或「无事可报」行。 |

**Gates Status**: ✅ 22 行全部 Pass。无 ❌ / ⚠ 行；§ Complexity Tracking 记 `N/A`。flow-class 读取：`spec:100-seal-slice-archive → execution`（`flow-class-check.py --action lookup`，2026-11-11）。

**Re-check after Phase 1**: 2026-11-11 — 对照已落盘的 `data-model.md`、3 份契约、`quickstart.md`、`feature-ref.md` 重读。第 I/IV/XIV 行按新产物刷新：FR→条款映射由 `feature-ref.md` 从契约引用组再生（28/28）、SC→红先模块补齐（10/10）、处置词/动作集/清单 schema 三处 owner 各只出现一次。无行改判。

## Decision Tensions

Owner of the record shape, admissibility, rejection forms and the load-bearing threshold:
`.specify/shared/guidelines/decision-tension.md`. Fields: `decision`, `antithesis`, `binding_constraints`
(`pole_a` / `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; id `T-NNN`.

### T-001 — 归档目的地取父 spec 内的 `slices/`，不复用退休归档

- **decision**: 分片归档的目的地固定为 `<父 spec>/slices/<原分片目录名>/`，是父 spec 内的位置迁移，不写 `.specify/archive/`、不查 `archive-gate`。
- **antithesis**: 把已合并分片直接交给 `/speckit.sanitize` 的退休归档 lane，移入 `.specify/archive/spec/`；当「分片确认终结、且组织习惯把所有不再变更的载体收进单一归档根」时它更优——归档目的地只有一个，读者只需记住一处，且复用现成的准入与执行通道。
- **binding_constraints**:
  - pole_a: 处置词汇与归档通道必须保持单一 owner 与单一机制（non-disposable 四值 + C-036），不得长出第二套退休语义。
  - pole_b: 074 的归档必须在「合并完成、封装阻断」的当下可执行，且归档后的旧路径仍能从父 spec 附近解析。
- **discriminating_evidence**: 对同一 074 夹具分别按两种目的地跑 `archive-plan`：退休模型对分片执行 `archive-gate` 查询。结果二值：退休模型因分片无状态载体被 gate 拒绝 / `slices/` 模型给出零未解析且 apply 成功。
- **expected_sacrifice**: SC-009 Source ↓ 单一机制审计需接受 non-disposable 的 `archive` 目的地由一个扩为封闭二形，代码与审计表各多一处分支。
- **revision_trigger**: 出现「同一父 spec 的 `slices/` 与 `.specify/archive/` 两份归档记录就同一分片给出不同处置」≥2 次 → 重开，评估把分片处置整体移交退休 lane 并扩展其准入对分片的可判定形态。
- **tension_id**: T-001

### T-002 — 归档触发取合并清单状态，且先于最终封装判定

- **decision**: 归档在 merge-apply 成功之后、seal 判定之前执行；触发谓词只读合并清单与工作树，`Sealed` 与具名阻断两种终态都放行，最终判定不阻断归档。
- **antithesis**: 只在 `Sealed` 之后归档，把归档定义为终态的后置动作；当「任何未封装的 spec 都不应移动文件、树应保持封装判定的原样」时它更优——不变量更简单，归档永远不会成为封装拒绝的替罪羊。
- **binding_constraints**:
  - pole_a: 074 今天必须可归档，而它的封装终态是具名阻断。
  - pole_b: 归档不得掩盖或改变封装判定的输入，同一输入在归档前后必须给出同一条阻断清单。
- **discriminating_evidence**: 在阻断态夹具上先跑 seal 记录阻断清单，再跑 archive-apply，再跑 seal。结果二值：两次阻断清单逐条一致且归档成功 / 任一不一致或归档被 `not-sealed` 拒绝。
- **expected_sacrifice**: SC-004 Source ↓ 一次 `/speckit.seal` 运行从 4 个步骤面增为 7 步（新增 `archive-plan`、`archive-apply` 与 archive 批次提交），每次运行多出两个引擎调用与一次提交。
- **revision_trigger**: 归档后重跑 seal 连续 2 次出现阻断清单变化 → 重开，把归档后移到 `Sealed` 之后并重新评估 074 的处置时点。
- **tension_id**: T-002

### T-003 — 日期化记录保持原字节，只经清单映射解析

- **decision**: 分片内部文件、`.specify/memory/**`、`.specify/history/**`、`features.md` 叙述与详情时间线一律不改写；它们的旧路径只经 `archive-manifest.json` 的 `from → to` 前缀映射解析。
- **antithesis**: 把所有文本中的旧路径机械改写为新路径，使 `grep` 与任何不读清单的读者都能直接命中；当「下游工具不查清单、且历史记录被允许统一迁移」时它更优——解析不再需要第二跳，仓库里的路径只有一个形态。
- **binding_constraints**:
  - pole_a: 日期化记录 MUST NOT 被改写（non-disposable / 099 C-020 的 dated-record 红线），运行前后哈希必须一致。
  - pole_b: 「未解析引用 = 0」必须是机器可判的单一读数，不能靠人读语义判断哪段文字算历史。
- **discriminating_evidence**: 对 074 夹具跑 archive-apply 前后逐文件取 sha256，并对日期化命中执行映射解析。结果二值：dated 文件哈希全部不变且每条旧路径经映射落到存在的归档路径 / 任一哈希变化或任一路径不可解析。
- **expected_sacrifice**: SC-003 Source ↓ 解析成为两步查询（先看树、再看清单），任何外部读者要自己实现映射才能解析历史文本。
- **revision_trigger**: 连续两个真实回合出现「外部工具因不读映射而把历史路径读成悬空」≥2 次 → 重开，评估在归档根提供只读路径别名或生成派生索引。
- **tension_id**: T-003

### T-004 — 归档清单是独立单文件，不并入合并清单

- **decision**: 新建父 spec 根的 `archive-manifest.json` 作为归档事实的唯一承载；`merge-manifest.json` 只更新路径形态值并重算摘要，不承载归档字段。
- **antithesis**: 把归档字段并入 `merge-manifest.json`，保持「一 spec 一份合并/归档清单」；当「读者只愿读一个文件、且清单数量越少越好」时它更优——少一次打开、少一个 schema、少一份摘要。
- **binding_constraints**:
  - pole_a: 合并清单的合并结论、计数、冲突、ID 映射与分片顺序必须保持不变（FR-018），归档不得借清单扩展改写合并语义。
  - pole_b: 归档事实必须能被独立复核与回滚，且合并清单的既有摘要在每次合并后仍可复算。
- **discriminating_evidence**: 在同一夹具上分别构造两版实现并对合并清单执行 C-034 摘要复算。结果二值：独立清单方案下合并清单除路径值与摘要外逐字段不变、归档清单自摘要稳定 / 并入方案下需新增字段才能表达归档且合并清单键集扩大。
- **expected_sacrifice**: SC-007 Source ↓ 每个父 spec 多一份文件、多一个 schema 与一组闭环算术需要核验。
- **revision_trigger**: 出现「读者需要同时携带两份清单才能回答一次归档问题」≥2 次 → 重开，评估在合并清单增加只读指针行（不改其结论字段）。
- **tension_id**: T-004

### T-005 — 活引用改写出引擎执行，限定封闭文本形态

- **decision**: 活引用改写由引擎按声明形态（spec-root 全路径、父 spec 内相对路径、`tests/**` 路径构造行上的 slug 字面量）做确定性替换；形态之外的命中一律 `unclassified-reference` 阻断，不改由代理临场手改。
- **antithesis**: 由代理按 `archive-plan` 的编辑清单逐条手工改写，覆盖代码构造、缩写与不常见载体；当「载体少而异质、且需要理解上下文才能安全改写」时它更优——不受文本形态限制，一次能处理任意写法。
- **binding_constraints**:
  - pole_a: 同输入必须产生逐字节一致的引用台账与改写结果，重跑零 diff（确定性、幂等）。
  - pole_b: 代码中的路径构造（如测试常量）必须被正确迁移，不能因为形态不匹配而静默漏改。
- **discriminating_evidence**: 对含三类形态的夹具连跑两次 `archive-plan` 与 `archive-apply`，并注入一条第四形态命中。结果二值：两次清单逐字节一致、重跑零 diff、第四形态被 `unclassified-reference` 阻断 / 任一项不成立。
- **expected_sacrifice**: SC-006 Source ↓ 遇到未声明的引用形态时流程 fail closed 停下，需先把形态纳入契约再重跑。
- **revision_trigger**: 连续两个真实回合出现「同一类引用形态被反复判为 unclassified」≥2 次 → 重开，把该形态纳入封闭集并补变异腿。
- **tension_id**: T-005

### T-006 — 归档后分片发现先读归档清单

- **decision**: `merge-plan` / `merge-apply` / `seal` 的分片发现与载体解析先读 `archive-manifest.json`，把归档分片读成同一分片集（slug、顺序、原始记录都不变）；无清单时回退既有同级目录扫描。
- **antithesis**: 保持同级目录扫描不变，归档后把分片集读为空并让后续动作按「无分片」短路；当「归档即终结、之后不再跑合并或封装」时它更优——零新增读取路径，引擎行为面最小。
- **binding_constraints**:
  - pole_a: 归档后重跑 `merge-apply` 必须幂等成功且零写入，`seal` 的 P0 与闭合判定必须继续读归档后的分片原始记录（FR-019）。
  - pole_b: 分片顺序与合并语义不得因归档而改变，且不得把 `slices/` 目录读成新的分片候选。
- **discriminating_evidence**: 归档后依次跑 `merge-plan` / `merge-apply` / `seal`。结果二值：`merge-plan` 报告同一分片集且零待移动、`merge-apply` exit 0 且零 diff、seal 阻断清单与归档前一致 / 任一项读成空集或结论改变。
- **expected_sacrifice**: SC-002 Source ↓ 每次分片发现多一次清单读取与 schema 校验，引擎多一条回退分支。
- **revision_trigger**: 归档清单损坏导致三个动作连续 2 次不可用 → 重开，评估把分片集快照写入 `merge-manifest` 的只读指针行（仍由归档清单拥有事实）。
- **tension_id**: T-006

## Project Structure

### Documentation (this spec)

```text
.specify/specs/100-seal-slice-archive/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — owner file:line measurements (this run)
├── data-model.md        # Phase 1 output — archive entities and validation rules
├── quickstart.md        # Phase 1 output — archive walkthrough, rerun and rollback
├── contracts/           # Phase 1 output — archive-actions / archive-manifest / reference-classification
├── feature-ref.md       # Phase 1 output — Feature 099 binding, delivery surface, FR/SC maps
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
scripts/python/seal-utils.py                       # engine: actions 4 → 6, manifest-aware discovery, archive planner/applier
templates/commands/seal.md                         # command template: archive stage after merge-apply (thin entry unchanged in shape)
skills/internal/seal-artifact/SKILL.md             # internal skill: archive orchestration steps + report discipline
shared/definitions/non-disposable-definitions.md   # owner: archive destination closed two-forms + disposal record
shared/definitions/framework-map.md                # owner: `slices/` semantics on the Feature specs row
.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md          # C-001 / C-008 in-place amendment
.specify/specs/099-speckit-seal/contracts/merge-back.contract.md           # C-019 / C-023 in-place amendment
.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md  # C-035 / C-036 in-place clarification
.specify/specs/100-seal-slice-archive/contracts/   # new: archive-actions / archive-manifest / reference-classification
docs/reference/commands/seal.md                    # command reference: archive stage walkthrough + rollback pointer
tests/contract/test_seal_*.py                      # updated pins (six actions, write allowlist) + new archive guards
tests/integration/test_seal_archive_round.py       # NEW: 074 round replay + rollback fixture
tests/integration/test_seal_074_round.py           # manifest-aware merge-plan after archive
tests/contract/test_sdd_compat_containment.py      # live carrier: slice dir constructor → archived path
tests/contract/test_sdd_diffusion.py               # live carrier: slice dir constructor → archived path
tests/fixtures/seal-archive/                       # NEW fixture trees: clean pair, unclassified ref, partial archive, rollback
.specify/specs/074-goal-team-sdd-unification/      # round target: slices/ + archive-manifest.json + path-field updates
.specify/register.md                               # five REC-074a rows rewritten to archived paths
.specify/features/074-goal-team-sdd-unification.md # live pointer section rewritten (timeline untouched)
.specify/features.md                               # 074 row Last Updated narrative untouched (dated)
shared/definitions/sdd-routing-definitions.md      # one live pointer rewritten (source + mirror)
```

**Structure Decision**: 本特性沿「命令模板 → internal 技能 → 确定性引擎」的既有三分形态落点（099 已建立的形态），不新增目录层级与命令。唯一新增目录是**数据面**的 `<父 spec>/slices/`（语义登记进 `framework-map.md`）与 **fixture 主题目录** `tests/fixtures/seal-archive/`（与既有 `tests/fixtures/` 主题目录同构）。074 回合的写面被限制在父 spec 树、`register.md`、详情活区、`shared` 源/镜像与两个测试文件内。

### Mirror Obligations *(mandatory — every changed file has mirrors or generated copies)*

Baseline measured 2026-11-11 before any edit: `sync-mirrors.py --check` exit 2 with exactly one pre-existing, unrelated drift (`.specify/templates/gitignore-specify-template`); every pair this spec touches reads `ok`. `regen-command-copies.py --check` exit 0. Evidence: `test-evidence/plan-stage-checks.txt`. The Verify criterion is therefore **no NEW drift** on the pairs this spec touches — never a bare global exit 0.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/seal.md` | `.claude/commands/speckit.seal.md`; `.github/prompts/speckit.seal.prompt.md`; `.opencode/command/speckit.seal.md`; `.qoder/commands/speckit.seal.md` — via `regen-command-copies.py`; NO `.specify/templates/commands/` mirror (retired) | `python3 scripts/python/regen-command-copies.py --check` reports no drift for the four copies (baseline exit 0) |
| `skills/internal/seal-artifact/SKILL.md` | `.specify/skills/internal/seal-artifact/SKILL.md` | `sync-mirrors.py --check` no NEW drift on `skills/internal` (baseline ok) |
| `scripts/python/seal-utils.py` | `.specify/scripts/python/seal-utils.py` (strict pair) | `sync-mirrors.py --check` no NEW drift on `scripts` (baseline ok) |
| `shared/definitions/non-disposable-definitions.md` | `.specify/shared/definitions/non-disposable-definitions.md` | `sync-mirrors.py --check` no NEW drift on `shared` (baseline ok) |
| `shared/definitions/framework-map.md` | `.specify/shared/definitions/framework-map.md` | same |
| `shared/definitions/sdd-routing-definitions.md` | `.specify/shared/definitions/sdd-routing-definitions.md` | same; the 074 live pointer lands in both copies in one batch |
| `.specify/specs/099-speckit-seal/contracts/*.md` | none (feature-internal contract pages; no mirror) | re-read the three amended clause groups; `clause_extract.py` still parses the pages |
| `.specify/specs/100-seal-slice-archive/contracts/*.md` | none (feature-internal) | `clause_extract.py` parses all three pages; clause ids globally unique in this feature |
| `.specify/constitution.md` | none (live governance file) | untouched by this feature (no principle change) |

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | 074 的合并清单已处于 `merged`、零开放冲突，两分片条目存在，`retention=pending-review` | `merge-manifest.json` 解析：`merge.status=merged`、`conflicts=[]`、`slices` 2 行（R-07） | verified | — |
| EP-002 | CPython ≥3.8 标准库足够实现归档计划器与改写器（零第三方依赖） | `pyproject.toml` `requires-python`；引擎现有 import 集合（`argparse/datetime/hashlib/json/re/subprocess/sys/pathlib`）实测 | verified | — |
| EP-003 | `pytest` 与唯一测试入口可用；既有 seal 守卫可作红先载体 | `bash scripts/bash/run-tests.sh tests/contract/test_seal_engine_contract.py -q` 在本阶段实跑（读数入 `test-evidence/plan-stage-checks.txt`） | verified | — |
| EP-004 | 099 契约与 non-disposable owner 的修订位置如 R-01/R-06 所测，均为单文件原地条款 | 逐条 file:line 实测（R-01、R-06） | verified | — |
| EP-005 | 引用面按 path-form 正则可在声明的扫描根上稳定枚举；裸 slug 与路径形态可机械区分 | 本日三次独立运行同一检测式，计数一致（R-08）；`merge-manifest` 中 identity 值与路径值可区分（R-07 解析） | verified | — |
| EP-006 | 本 worktree 无 `.specify/state/`；主仓存在父与 074b 两个 state 文件、074a 缺席 | `ls`/`grep` 实测（R-10）；`.specify/.gitignore` 覆盖 state 根 | verified | — |
| EP-007 | 镜像对基线仅有一条与本特性写面无关的漂移；命令副本零漂移 | `sync-mirrors.py --check` exit 2（唯一 DIFF gitignore 模板）；`regen-command-copies.py --check` exit 0（R-11） | verified | — |
| EP-008 | `git mv` 语义可用：仓库为 git 工作树，非 git 工作树按输入错误退出 2 | `git rev-parse --is-inside-work-tree` 实测；`git status --porcelain` 与 `diff --name-status -M` 可用 | verified | — |
| EP-009 | `COMMAND_BASELINE` 恰 31 个命令，新增第 32 个时守卫转红 | `tests/contract/test_migration_distribution.py:104,134,275-278`（R-12） | verified | — |
| EP-010 | 074 详情文件的活区/时间线章节边界稳定（`## Related Specifications/Requirements` 为活区） | 详情文件 `:16-89` 章节实测（R-08）；clarify Q2 已裁定混合载体按章节切分 | verified | — |
| EP-011 | 归档清单的 `pinned_commit` 可在 apply 前从 `git rev-parse HEAD` 取得，且 apply 本身不提交 | 引擎既有 `_run_git` 封装（`:2075-2080`）与任务简报的批次提交约定 | verified | — |

## Inherited Blockers

Dependency set: none — 本特性不消费任何既有 Feature 的 `## Deferred` 行或 `verification.md` 的
`blocked`/`deferred`/`partial` 行。Feature 099 是**绑定对象**（同一命令/引擎/技能的增量），074 是**验收对象**，
二者都不是依赖：本特性读取的是它们的当前契约文本与实测树状态（EP-001…EP-010），不消费其未完成的交付项。

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| — | (none) | not-applicable | — | — | 依赖集已声明为 `none`；若实现期发现真实依赖，按 owner 的提取集三来源补行并改此声明。 |

## Disclosed Rulings

1. **`destination-exists` 与「部分归档」的退出码分层**（requirements Edge Cases 两条相邻规则的收敛）：同一分片在源与目标同时存在 → `destination-exists` 拒绝（exit 1，两侧不动）；跨分片的半归档状态（一片已在目标、另一片仍在源）或清单声称的分片两处都找不到 → 输入缺陷（exit 2，`partial-archive` / `slice-missing`）。判据是「同一分片的双侧冲突是前置拒绝；分片集内部不自洽是输入缺陷」。
2. **`merge-manifest.retention` 不改**（FR-018 的「只改路径字段」）：099 写入的 `retention: pending-review` 是非路径字段，归档不触碰它；处置决定由 `archive-manifest.json` 的逐片 `{slug, from, to}` 行承载——封闭 schema 以 `from` / `to` 两字段表达 non-disposable 的 `moved = {from, to}` 记录形态，不新增 `moved` 键（C-203 的封闭集）。
3. **扫描根是封闭集，不覆盖其他 spec 的历史记录**：`.specify/specs/<other>/**`（例如 099 的 `test-evidence/` 中引用 074 分片的记录）不在本特性的解析声明内；它们是其他 spec 的日期化记录，保持原字节，且归档清单的 `from → to` 映射对它们同样可用。FR-015 的「覆盖声明的扫描根」按此声明执行，不把「全仓所有历史文件」偷换进声明。
4. **既有镜像漂移不修**：`.specify/templates/gitignore-specify-template` 的既有 DIFF 早于本特性且不在写面，按「不修、不掩」记录在案；本特性的判据是「触及的镜像对零新增漂移」。
5. **074 回合在主 worktree 的 `.specify/state/` 缺席环境下执行**：运行期载体 3 条全部记 `absent`；这不改变 FR-017 的算术（`runtime-updated + absent = 3`），主仓环境下则为 2 更新 + 1 缺席。

## Execution Model

### Stage execution record（本 plan 阶段）

- `requested`: 0 — 本阶段为单作者 in-process 撰写（plan / research / data-model / contracts / quickstart / feature-ref），未声明可并发的派发单元。
- `effective`: 0 — 未派发任何子代理执行单元；按 owner 的 carrier 定义，in-process 工作不计入派发读数。
- `effective_reason`: `single-unit` — 可表示的被派发单元集为空（enumerated unit set size 0；单作者 in-process 不构成派发单元）；同时宿主未启用子代理派发载体。同作者评分按 `objective-analysis-gate.md` 处置（评分证据为直接读取，逐行标注）。

### Work packages（8 包，每包 ≤16 行）

依赖边（→ 表示先行）：`P1 ∥ P5`；`P1 → P2 → P3 → P4`（同一引擎文件，写域相交，串行链）；`P1 → P6`；`P4 → P7`；`P5 → P7`；`P6 → P7`；`P7 → P8`。并发窗口：P1 与 P5 可同时启动；P3 推进时 P5 的 owner 文案与 P6 的命令面可并行；P7 的 074 回合必须等 P4（引擎写面）、P5（owner 文案）与 P6（流程入口）全部落定。每个包的派发 MUST 注入 fast-fail 条款并要求返回异常行与「无事可报」行。

| 包 | 主题 | 写域（文件级） | 行数上限 | 验收锚 |
|----|------|----------------|----------|--------|
| P1 | 动作集 4→6 与 CLI 表面 | `scripts/python/seal-utils.py`（常量/解析/派发/守卫）、`tests/contract/test_seal_engine_contract.py`（六动作 pin）、`tests/contract/test_seal_boundaries.py`（动作表审计） | 16 | 契约 C-101、C-103、C-115；`--help`/`--version`/未声明选项/退出码封闭；命令名集合不变 |
| P2 | manifest-aware 分片发现 | `seal-utils.py`（`_discover_slices` / `_derive_order` / `_merge_state` / 清单读取）、`tests/contract/test_seal_merge_plan.py`、`tests/integration/test_seal_merge_determinism.py`、`tests/integration/test_seal_074_round.py` | 14 | 契约 C-112；归档后 merge-plan 同一分片集、merge-apply 幂等零写、seal P0 列表不变 |
| P3 | `archive-plan`：前置条件 + 引用分类 + 清单 | `seal-utils.py`（plan 段）、`tests/fixtures/seal-archive/`、`tests/contract/test_seal_archive_plan.py`、`tests/contract/test_seal_archive_manifest.py` | 16 | 契约 C-102、C-104、C-201…C-212、C-301…C-307、C-312；两跑逐字节、闭环算术、unclassified 阻断 |
| P4 | `archive-apply`：两阶段批次 + 移动 + 改写 + 原子恢复 | `seal-utils.py`（apply 段）、`tests/contract/test_seal_archive_apply.py`、`tests/integration/test_seal_archive_idempotency.py` | 16 | 契约 C-105、C-106、C-108…C-111、C-308…C-311；重命名对、零纯删除、失败按原字节恢复、`already-archived` |
| P5 | owner 原地修订 | `shared/definitions/non-disposable-definitions.md`、`shared/definitions/framework-map.md`、099 三份契约（C-001/C-008/C-019/C-023/C-035/C-036） | 12 | 契约 C-113；处置词表仍四值、目的地封闭二形；动作集唯一 owner；布局行登记 `slices/` |
| P6 | 命令面与技能面 | `templates/commands/seal.md`、`skills/internal/seal-artifact/SKILL.md`、4 份 per-tool 副本（生成）、`docs/reference/commands/seal.md` | 14 | 契约 C-114；`regen --check`/`sync --check` 无新增漂移；模板只引用引擎判定 |
| P7 | 074 真实回合 | `.specify/specs/074-goal-team-sdd-unification/`（`slices/` + `archive-manifest.json` + 路径字段）、`.specify/register.md`、`.specify/features/074-…md` 活区、`shared/definitions/sdd-routing-definitions.md` + 镜像、两个测试载体、`test-evidence/074-archive-round.txt` | 14 | 契约 C-107；SC-001/SC-002/SC-003/SC-005/SC-006/SC-010 的读数；注册状态与封装结论不变 |
| P8 | 收尾验证与记录 | 全量测试基线对照、镜像/副本复核、回滚夹具、`verification.md`、`feature-ref.md` 复算、registry 收尾（implement 阶段）、run determination | 10 | 契约 C-116；十项 SC 的 Measurement Sources 各有落点；无新增失败名单；回滚逐字节恢复 |

## Complexity Tracking

N/A — Constitution Check 无 Fail / Partial 行，无需要辩护的违规项。

## Phase 1: Design Artifacts Summary

Backfilled 2026-11-11 after the Phase 1 artifacts landed (all counts taken from the files on disk, not from memory):

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 10 entities (E1–E10); 14 validation rules (V1–V14) |
| Contracts | [`contracts/`](contracts/) | 3 files, 40 clauses globally numbered C-101…C-116 / C-201…C-212 / C-301…C-312 (16 / 12 / 12); all `md-bold-closed` |
| Quickstart | [`quickstart.md`](quickstart.md) | 6 scenarios (S-1…S-6): plan preview, apply, rerun, blocked-seal flow, rejection, rollback |
| Research | [`research.md`](research.md) | R-01…R-14, all file:line or measured reading |
| Feature reference | [`feature-ref.md`](feature-ref.md) | 28/28 FR → clause map generated from the contracts' citation groups; 10/10 SC → red-first module map |
| Feature registration | `.specify/features.md` + `.specify/features/099-speckit-seal.md` | 099 row Last Updated refreshed; status remains `Ready for Review`; no new Feature row (binding, not a new Feature) |

Drift from the Phase 0 expectation: none in artifact inventory. The one measured correction: the declared runtime carrier count is 3 (1 parent + 2 slices), and in this worktree all three read `absent`.
