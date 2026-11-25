# Implementation Plan: Runtime Store Layout — 运行期存储迁出 `.specify/memory/`

**Branch**: `105-runtime-store-layout` | **Date**: 2026-11-25 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `105-runtime-store-layout` → Feature 024 Specification Workspace Versioning
**Input**: Specification from `.specify/specs/105-runtime-store-layout/requirements.md`

> **Concurrency obligation (执行义务，按指针抵达)**: this plan authorizes execution bodies. Each one follows the framework's single concurrency obligation — consider concurrency first, default to it when the class and capability allow, and name a reason code plus record the `requested` / `effective` / `effective_reason` reading when serial. The obligation's authored text is `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; its class table is `shared/declarations/facts/concurrency-class.yaml`, its reason codes `shared/declarations/facts/serial-reason.yaml`, and its reading fields `shared/declarations/facts/effective-concurrency.yaml`. This plan restates none of their rules.

## Summary

Turn `.specify/memory/` from a catch-all runtime bucket into a retired container: every current store becomes a first-class top-level `.specify/<store>/` root, the two memory tiers stay the only seeded stores, and "memory" survives only as the memory system's name. The transition is one dimension added to the existing `specify migrate` engine (`store-layout`, ordered last), reusing its dry-run → `--apply` → archive-first → per-run-receipt structure: a store with authoritative content only in the old root is relocated per a pre-move manifest (digest + from→to, no byte duplication — the reviewed 097 `relocate` precedent); a store with authoritative content on both sides refuses and names both paths; symlinks and unwritable paths refuse by name; unknown residue is reported and preserved; the empty container is removed last; a second run is a no-op. The repository itself is migrated by that same command (dogfood), its mirrors are regenerated, and every live reference moves while dated records stay byte-identical.

The design defers no semantics to implementers: the closed store roster and its machine declaration, the planner's state table, the refusal classes, the receipt v2 shape, the live-reference allowlist, and the red-first fixture/assertion set are fixed in `contracts/` and `data-model.md`. See § Decision Tensions for the six load-bearing choices and their antitheses; full Phase 0 readings are in `research.md`.

## Technical Context

**Language/Version**: Python `>=3.8`（`pyproject.toml` 既有 `requires-python`）；零新增第三方依赖，零新增运行时。
**Primary Dependencies**: 标准库 + 仓内既有引擎（`memory-utils.py`、`feedback-utils.py`、`evidence-utils.py`、`exec-quant.py`、`sanitize-utils.py`、`renumber-utils.py`、`seal-utils.py`、`tools-utils.py`、`skills-utils.py`、`declaration_reader.py`）；CLI 侧既有 `typer`；测试侧既有 `pytest`。
**Storage**: 纯文件系统。14 个顶层存储根（`session`、`knowledge`、`feedback`、`evidence`、`exec-quant`、`trigger`、`retention`、`renumber`、`sanitize`、`housekeeping`、`coaching`、`todo`、`tools`、`migrate`）+ 退役容器 `.specify/memory/`；迁移回执 `.specify/migrate/receipts/<run-id>.json`（逐运行一文一件）；不新增数据库、索引文件或共享聚合。
**Testing**: `pytest`，唯一入口 `bash scripts/bash/run-tests.sh`（默认并行）；新增 contract / integration / unit 测试与两组夹具（`tests/fixtures/store-layout-105/`、既有 migrate-097 夹具的布局更新）；夹具在 `tmp_path` 或 `.specify/.tmp/` 内生成。
**Target Platform**: 支持符号链接的 Linux/macOS CLI 环境；无符号链接平台按既有降级语义 `refuse`；迁移要求源与目标同文件系统（rename），跨设备时以 `shutil.move` 的复制删除语义执行并同样受 manifest 保护。
**Project Type**: 单包框架 CLI + 模板/技能/共享定义分发（`src/specify_cli/`、`templates/`、`skills/`、`shared/`、`scripts/`）。
**Performance Goals**: dry-run 全程零写入；迁移 2,971 个受跟踪条目时不做字节复制，按存储写 manifest + 逐条 move；单次 dry-run 与既有 097 同量级；`sync-mirrors` 收敛为既有工具行为，无新增扫描器。
**Constraints**: 不推送；无运行时旧路径回退（A-8）；dated record 不改写（A-11）；条目格式/写入协议零修改（FR-025）；Python 3.8 语法；不支持符号链接时拒绝而非崩溃。
**Scale/Scope**: 1 个新迁移维度、17 行封闭清点、14 个目标根 + 1 个墓碑、1 个机器声明、4 份契约、10 个实体、约 89 个测试文件需归类/更新、15 个工作包。

## Constitution Check

**Core Principles Compliance** (rendered from `.specify/constitution.md` v1.20.0):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每个 WP 与契约条款回溯到 FR-001…FR-026（`feature-ref.md` 的 FR→WP 矩阵，26/26 覆盖） |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 024；本阶段推进 slice 105 `Draft → Planned`，父行保持 `Ready for Review`（`feature-ref.md` § 绑定） |
| III | Intent-Driven Development | ✅ Pass | 只交付用户请求的布局迁移与行为保持；非目标在 `contracts/store-layout.contract.md` C-8 明确 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 契约先行；`plan.md` § Test-First Coverage 为每个 SC 定义红先夹具与变异转红断言 |
| V | AI Agent Integration Standards | ✅ Pass | 不新增 agent/工具；每工具命令副本由既有 `regen-command-copies.py` 再生成（L-6） |
| VI | Continuous Quality & Observability | ✅ Pass | 逐运行回执 v2 + manifest + `test-evidence/` 实测；失败前向续跑、不掩盖 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本工件集即 plan 产物；WP 与依赖顺序供 `/speckit.tasks` 切分；状态推进不越权 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 引擎路径常量以代码为现实；测量以工作树/提交为准（`research.md` R-1/R-3/R-4） |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 复用 migrate 引擎与既有 declaration reader；零新运行时、零新评分/登记系统 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新根为 lowercase kebab-case 且与既有子目录同名；文档页落既有 `docs/reference/**` |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子显式：源面编辑 + 镜像再生成；本仓用同一 `specify migrate` 完成 dogfood（WP14） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 迁移复用 `specify migrate` 与既有检查器；不新写第二迁移/扫描实现（C-6、M-1） |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Reliable Delivery / Learning Capture：布局可判定、回执可恢复、边界可验证 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 单一机器声明 `runtime-store-layout.yaml`；框架地图与测试为受守卫投影（C-6） |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 拒绝/修复文案按全局基准读者书写，点名两侧路径与修复入口（M-5） |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 并存/未知残留/符号链接/权限一律确定性拒绝或保留，不静默修平（M-2/M-3/M-5） |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | 每个新根在框架地图登记并写入声明；临时面用 `.specify/.tmp/`（C-5） |
| XVIII | Grounded Naming | ✅ Pass | 根名沿用基线子目录名；`seed/` 来自需求词汇「种子布局」；无自创别名 |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | 顶层根即用户视图；墓碑行给出唯一含义；不增加额外面 |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | 只用 `run-tests.sh`；夹具 `tmp_path` 隔离；不新增 runner/全局慢夹具 |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | 既有脚本保持 `-h/--help/--version`；迁移为 CLI 子命令，无新脚本副作用 |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | 阶段检查点记录方向审计与并发读数；不新增机制 |
| XXIII | AI-Generated Code Review Policy | ✅ Pass | 本变更由 AI 产生，按 AI 评审流（合并后读 git 历史）；SDD 评审门禁仍在 |

**Gates Status**: ✅ All gates pass（无 Fail / Partial，Complexity Tracking 为 N/A）。

**Re-check after Phase 1**: 2026-11-25 — Phase 1 工件（data-model / 4 契约 / quickstart / feature-ref）落盘后复核：23 行维持 Pass；XIV/XVII 的证据由「计划意图」升级为「声明 + 框架地图守卫 + 契约」，无新增违规。

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md` — this section carries records in that shape and does not restate its rules.*

### T-001 — 以「第六维」扩展现有 migrate 引擎，而不是独立迁移步骤

- **decision**: 在 `MIGRATE_DIMENSIONS` 末尾追加 `store-layout`，复用既有 item 模型、执行器、回执与续跑；097 的五个 token 保持为有序前缀。
- **antithesis**: 在 migrate 之外做独立的一次性存储迁移步骤（新 CLI 子命令或新引擎），有自己的计划/回执格式；当维度集被声明为封闭且其 owner 是 dated record 时它更优——不改动任何既有维度契约。
- **binding_constraints**:
  - pole_a: 复用——计划/执行/回执/续跑只有一份实现（用户请求与 A-6 明令复用）。
  - pole_b: 既有封闭契约的稳定性——097 C-1 声明维度集封闭，扩维须修订 requirements。
- **discriminating_evidence**: 逐项核对既有引擎对维度的耦合：`MigrateItem._validate` 只校验成员身份；`_migrate_plan_and_run` 按 `MIGRATE_DIMENSIONS` 迭代；执行器按 `mechanism` 分派，不按维度。结论二值：执行机制维度无关（真）→ 独立步骤会复制全部机制（伪优势）。实测见 `research.md` R-3。
- **expected_sacrifice**: 触碰一个 dated record 所记载的封闭集；两个 097 维度 pin 测试必须改为「前缀保持 + 本契约全集」守卫；本特性承担该 owner 转移的说明成本。
- **revision_trigger**: 若评审判定维度集不可由后续 feature 扩展（要求先改 097 requirements），则回退为独立步骤并新建其回执 schema。

### T-002 — 重命名包内种子目录 `memory/` → `seed/`

- **decision**: 包内种子资产根改名 `seed/`（含两个锚点占位与 `session/`、`knowledge/` 占位）；`pyproject` force-include 与 init 复制同步；安装后不再出现任何名为 `memory` 的目录。
- **antithesis**: 保留包内 `memory/` 作为「种子来源目录」，仅改变其运行时投影（锚点 → `.specify/`，子目录 → `.specify/session|knowledge`）；当改动面最小化优先时它更优——不改 packaging、不动构建脚本。
- **binding_constraints**:
  - pole_a: 语义——A-2 裁定 memory 是系统名，不再作任何目录名。
  - pole_b: 变更成本——包目录名不进入运行时，改名只影响安装器与打包。
- **discriminating_evidence**: 实测包内 `memory/` 只含 4 个条目（2 锚点 + 2 tier 占位）且没有其它消费者；`grep -rn '"memory"' src/` 的命中全部是本特性要更新的安装路径。二值：改名是否只触及 `pyproject.toml` + `copy_local_templates` + `migrate_placeholder_dir` + 测试夹具——是（改名成本可控）。
- **expected_sacrifice**: 触及打包清单与 `tests/contract/test_upgrade_end_state.py` 等夹具；实现期需重跑安装夹具。
- **revision_trigger**: 若打包/构建链无法在不破坏 wheel 资产定位的前提下改名，则回退为保留 `memory/` 种子目录并记录其唯一含义。

### T-003 — SC-007 采用「成员集无新增漂移」的实测口径，而不是绝对 `--check` rc 0

- **decision**: 镜像判据为「本特性触及的源文件镜像均已再生成，且触及面的漂移成员集相对基线无新增成员」；绝对 rc 0 作为实测事实如实报告，不由本特性声明达成（除非收敛全部成员）。
- **antithesis**: 坚持 SC-007 的字面 `--check` rc 0，要求本特性把 450 个既有漂移成员全部收敛（一次全量 `sync-mirrors --write`）。
- **binding_constraints**:
  - pole_a: 诚实测量——基线实测 450 DIFF，绝对绿不可由本特性单独达成。
  - pole_b: 变更面纪律——把 450 个无关成员拖入本特性会淹没真实改动，且可能把无关内容改写进本变更。
- **discriminating_evidence**: 实测基线：`sync-mirrors --check` rc 2，450 DIFF（skills 262 / shared 103 / scripts 65 = 59 plain + 6 projected / agents 20 / templates 0），0 MISS / 0 ORPHAN；regen rc 0。项目既有教训 `docs/reference/history/00-cross-cutting-lessons.md:154` 明确：既有漂移先于特性存在时，判据必须写成「无新增成员」而不是条数或绝对绿。二值：绝对 rc 0 是否需要收敛与本特性无关的 450 成员——是。
- **expected_sacrifice**: SC-007 的字面 rc-0 子句在基线不可满足；评审需按本口径裁决。若实现顺带收敛了某些 scope，记录成员集差值即可（可改善，不可回归）。
- **revision_trigger**: 若评审坚持绝对 rc 0，则追加一次全量镜像收敛任务并把 450 成员纳入本特性变更面。

### T-004 — `docs/archive|static|notes` 归入 dated record 类

- **decision**: SC-006 的「现行文档类」在测量时排除 `docs/archive/**`（append/archive-only）、`docs/static/**`（冻结生成报告）与带日期快照语义的 `docs/notes/**`；三类实测成员仅 3 个文件，均不被改写。
- **antithesis**: 按 SC-006 的字面类定义（`docs/**` 仅排除 `history/`、`decisions/`），把这三个文件也改写到新路径。
- **binding_constraints**:
  - pole_a: 不伪造历史——改写归档快照会声称当时的事实不是当时的样子（A-11 的同一原则）。
  - pole_b: 判据的可判定性——允许集必须与「现行文档」的真实集合一致，否则守卫要么假红要么假绿。
- **discriminating_evidence**: `docs/concepts/documentation-model.md` 明写正式目录 append/archive-only、`notes/` 为生命周期短存；三个文件的定位实测为一个归档提议、一份冻结验收报告、一份带 `created/expires/status` 的对账快照。二值：改写它们是否会制造与文档模型冲突的「现行化」——是。
- **expected_sacrifice**: SC-006 的 measured class 比字面多排除三个子树；守卫测试必须显式声明该扩展与依据。
- **revision_trigger**: 若评审判定 `docs/archive` 属现行面，则改为更新这三个文件并把三类从排除集移除。

### T-005 — 搬迁以「manifest 先写 + 逐条 move」为归档形态，不做字节复制归档

- **decision**: 每个存储先写 `entries[]` manifest（相对路径 + 摘要 + from→to + 类别），再逐条 `shutil.move`；manifest 写入回执并充当 `recover` 索引；不向 `.specify/archive/migrate/` 复制任何字节。
- **antithesis**: 先把整个旧存储复制进 `.specify/archive/migrate/<run-id>/` 再移动；当「archive-first」被读作「必须先有一份字节副本」时它更优——恢复不依赖回执。
- **binding_constraints**:
  - pole_a: 零丢失与可恢复——每个对象在每一步都存在于旧位或新位，恢复按 manifest 逆序进行。
  - pole_b: 仓库成本——2,971 文件 / 18 MB 的字节副本会翻倍存储并进入 git 历史。
- **discriminating_evidence**: 097 的 `relocate` 已以「move + digest + from→to + recover」被评审 r2 接受（`src/specify_cli/__init__.py:4179-4197`）；实测量级见 R-1。二值：字节副本是否增加数据安全——否（move 不销毁内容），只增加存储。
- **expected_sacrifice**: 「archive」在此维度是 manifest 而非副本树；恢复依赖回执完整写入（manifest 在首次 move 前落盘）。
- **revision_trigger**: 若评审要求字节副本，则改为 copy→verify→remove 并接受存储翻倍。

### T-006 — 跨存储枚举收敛为单一机器声明，而不是各消费者各持一份常量

- **decision**: 新建 `shared/declarations/facts/runtime-store-layout.yaml`（kind `mapping`），由 `declaration_reader.py` 读取；六个跨存储消费者（sanitize、renumber、seal、concurrency-check、migrate、init）改为读声明；non-disposable 回顾面保留自有闭集并由守卫断言成员相等；单存储引擎保留自有的单根常量（其存储即其事实）。
- **antithesis**: 每个消费者各持有自己的根清单，由测试钉住彼此相等；当不想引入新 fact 注册时它更优——零声明层改动。
- **binding_constraints**:
  - pole_a: 单一 owner——同一存储集出现在七个位置必然漂移（宪法 XIV）。
  - pole_b: 机制成本——新 fact 需要 schema 注册、消费者改造与降级标注。
- **discriminating_evidence**: 实测跨存储清单 7 处（sanitize MATERIAL_ROOTS、renumber 前缀、seal dated trees、concurrency-check surfaces、non-disposable review surface、migrate planner、init seeder），逐处硬编码时一次布局变更需 7 处同步；声明 mechanism 已存在且支持 `mapping`（`shared/declarations/facts/driver-stage-artifacts.yaml` 为同形先例）。二值：是否存在一个已注册且可被所有消费者读取的单一 owner 机制——是。- **expected_sacrifice**: 新 fact 的注册与降级标注；消费者在声明缺失时以 `owner-unavailable` 标注，不退化为第二份清单。
- **revision_trigger**: 若声明层无法装载该结构（subset/注册限制），回退为代码常量 + 跨消费者相等守卫。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/105-runtime-store-layout/
├── requirements.md      # 上游规格（已完成，含 clarify 裁定）
├── research.md          # Phase 0 调查读数（本阶段产出）
├── plan.md              # 本文件（/speckit.plan 产出）
├── data-model.md        # Phase 1：10 实体 + 状态迁移 + 10 不变量
├── contracts/           # Phase 1：4 份契约
│   ├── store-layout.contract.md          # 目标布局、退役根、登记、忽略、声明（C-1…C-8）
│   ├── migrate-store-layout.contract.md  # 第六维、判定表、执行器、回执、续跑、夹具（M-1…M-9）
│   ├── memory-and-injection.contract.md  # 记忆两层/持久化/边界/注入载荷保持（P-1…P-6）
│   └── live-reference-migration.contract.md # 路径映射、dated 边界、允许集、镜像（L-1…L-8）
├── quickstart.md        # Phase 1：8 个场景（含逐例前提与验证路径）
├── feature-ref.md       # Phase 1：Feature 024 绑定 + FR/SC 矩阵
├── tasks.md             # 下一阶段（/speckit.tasks）产出
└── verification.md      # 实现阶段产出
```

### Source Code (repository root)

```text
shared/declarations/facts/runtime-store-layout.yaml   # NEW machine owner of the store set
shared/declarations/contract.yaml                     # + fact registration
shared/declarations/facts/{memory-types,non-disposable-review-surface}.yaml  # path notes / membership
shared/declarations/exclusions/no-machine-fact.yaml   # comment repaired
shared/definitions/framework-map.md                   # 14 store rows + 1 tombstone
shared/definitions/{tool-definitions,non-disposable-definitions,probe-definitions,
 subagent-definitions,derivation-definitions,self-explanatory-definitions}.md
shared/workflow/{feedback-step,evidence-step,artifact-commit-step,agent-configuration,
 acceptance-hardening,tool-reuse-gate,runtime-mode,target-resolution}.md
shared/guidelines/{todo-in-context,reporting-obligations,critique-and-self-critique,confirmation-gates}.md
shared/patterns/{interview-pattern,self-improvement-pattern}.md
scripts/python/{memory-utils,feedback-utils,evidence-utils,exec-quant,run-determination,
 sanitize-utils,renumber-utils,trigger-utils,tools-utils,skills-utils,seal-utils,probe-utils,
 record-retention,concurrency-check,role-edge-check,non-disposable-check,anchor-layout-migrate}.py
scripts/bash/create-new-tools.sh                      # records at .specify/tools/
src/specify_cli/__init__.py                           # seed/init/core-assets/rewrite_paths + migrate store-layout dimension
seed/                                                 # NEW package seed root (replaces memory/): anchors + session/ + knowledge/
pyproject.toml                                        # force-include memory -> seed
templates/commands/{tools,todo,sanitize,review,migrate,interview,instructions,improve,feedback}.md
templates/{instructions-template,tools}.md
templates/{gitignore-specify,claudeignore,codexignore}-template
skills/**                                             # 40 live files + sdd-{house-keeping,project-setup}/scripts/mechanism-inventory.py
agents/sdd-debt-governor.agent.md                     # read-scope path
docs/**                                               # 19 live pages (R-2.3 inventory); dated trees untouched
.specify/instructions.md                              # regenerated from templates/instructions-template.md
.specify/glossary.md                                  # 7 entries updated
.specify/.gitignore                                   # tools/*.json, sanitize/, trigger/telemetry.jsonl
.specify/skills/ .specify/shared/ .specify/scripts/
.specify/templates/ .specify/agents/templates/        # regenerated mirrors
.github/prompts/ .claude/commands/ .qoder/commands/ .opencode/command/  # regenerated command copies
.specify/session/ .specify/knowledge/ … .specify/migrate/  # migrated runtime stores (dogfood)
tests/contract/{test_runtime_store_layout,test_store_layout_live_refs,test_tools_domain}.py   # NEW
tests/integration/{test_store_layout_migration_us1_us2,test_store_layout_migration_us3_us6,
 test_memory_preservation,test_dispatch_injection_paths,test_init_new_layout}.py               # NEW
tests/fixtures/store-layout-105/builders.py           # NEW declaration-built fixtures
tests/contract|unit|integration|fixtures/**            # 89 files classified/updated (L-3)
```

**Structure Decision**: extends the existing single-module CLI, the declaration layer, and the existing runtime engines; one new packaged seed root (`seed/`) replaces the `memory/` seed namespace; 14 new runtime roots are created by migration/lazy owners, not by this plan. No new command, engine, or service.

### Mirror Obligations

Baseline measured **before** the edit on 2026-11-25 (`test-evidence/sync-mirrors-baseline.txt`): `sync-mirrors.py --check` rc 2 with 450 DIFF members (skills 262 / shared 103 / scripts 65 = 59 plain + 6 projected / agents 20 / templates 0), 0 MISS, 0 ORPHAN; `regen-command-copies.py --check` rc 0. The criterion for every touched pair is **no NEW drift member** plus regeneration of every touched file; scope syncs may cure pre-existing members (recorded as a member-set delta). Absolute rc 0 is reported against this baseline, not asserted from it (T-003).

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/**` (definitions, guidelines, workflow, patterns, declarations) | `.specify/shared/**` via `sync-mirrors.py --write --only shared` | touched files byte-identical after regeneration; member set has no NEW drift vs baseline |
| `skills/**` (+ two `mechanism-inventory.py`) | `.specify/skills/**` via `--only skills` | same |
| `agents/sdd-debt-governor.agent.md` | `.specify/agents/templates/sdd-debt-governor.agent.md` | same |
| `scripts/**` | `.specify/scripts/**` (strict pair) via `--only scripts` | same; no new ORPHAN |
| `templates/**` | `.specify/templates/**` via `--only templates` | same |
| `templates/commands/*.md` | `.github/prompts/`, `.claude/commands/`, `.qoder/commands/`, `.opencode/command/` via `regen-command-copies.py` | regenerated copies contain the edit; `regen --check` rc 0 |
| `src/specify_cli/__init__.py`, `seed/`, `pyproject.toml` | none (wheel assets) | build/import smoke (`python -c "from specify_cli import main"`) |
| `docs/**` live pages | none (project development docs, not distributed) | docs consistency check at review |
| `.specify/instructions.md` | generated from `templates/instructions-template.md` by the instructions generator | generated file contains the new paths; no hand edit |
| `.specify/.gitignore` | byte-identical to `templates/gitignore-specify-template` | `cmp` |
| `tests/**` | none | contract/integration runs |

### Work Packages (15, for `/speckit.tasks`)

| WP | 内容 | FR | Depends |
|----|------|-----|---------|
| WP01 | 机器声明 `runtime-store-layout.yaml` + 注册 + 框架地图 14 行 + 墓碑行 | FR-001, FR-002, FR-004, FR-005, FR-021 | — |
| WP02 | 引擎路径常量 + 跨存储消费者改读声明 | FR-018, FR-025 | WP01 |
| WP03 | 记忆系统与注入保持：`memory-utils` 解读声明根、memory 两技能、`run-determination` 路径、`memory-recall` 注入来源、边界反向夹具 | FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012 | WP02 |
| WP04 | tools 域合并：记录+清单同居、忽略收窄、`tools-utils`/`skills-utils`/`create-new-tools.sh`/`tool-definitions`、sanitize 旧检查移除 | FR-003, A-5 | WP01 |
| WP05 | 安装器/种子：`seed/`（移除包内 `memory/`）、init 播种、core assets、`rewrite_paths` 去 memory、`pyproject`、placeholder 目录 | FR-017, FR-019 | WP01 |
| WP06 | 忽略面：模板+已装副本、claude/codex 放行、tracked/ignored 守卫 | FR-020 | WP04 |
| WP07 | migrate 规划器：第六维、状态判定表、拒绝类、回执规划、顺序 | FR-002, FR-013, FR-015 | WP01, WP02 |
| WP08 | migrate 执行器：manifest、逐条 move、容器移除、未知残留、续跑、回执 v2 | FR-002, FR-014, FR-015, FR-016 | WP07 |
| WP09 | migrate 命令面：模板 + 4 副本、`docs/reference/commands/migrate.md`、维度/回执文案 | FR-013, FR-022 | WP08 |
| WP10 | 活引用面重写：templates/skills/shared/agents/docs/glossary/instructions 按 L-1…L-3 | FR-018, FR-021, FR-023 | WP02…WP09 |
| WP11 | 镜像与命令副本再生成；成员集基线对比（SC-007） | FR-022 | WP10 |
| WP12 | 新测试：布局守卫、活引用守卫、工具域、记忆保持、注入、初始化；89 文件归类/更新 | FR-007, FR-008, FR-010, FR-011, FR-024, FR-025, FR-026 | WP01…WP11（红先于实现） |
| WP13 | 夹具：legacy / seeded-legacy / dual / residue / symlink / readonly / partial（由声明构建） | FR-024 | WP07 |
| WP14 | dogfood：本仓 `specify migrate --apply` + 回执 + 旧根消失 + `git log --follow` 证据 | FR-016, SC-001/SC-004 | WP05…WP11 |
| WP15 | 验收证据包：SC-001…SC-008 逐条读数、变异转红 drills、全量套件名级基线 | FR-026 | WP12…WP14 |

**Implementation order**: WP01 → WP02 → {WP03, WP04, WP05} → WP06 → WP07 → WP08 → WP09 → WP10 → WP11 → WP13 → WP12 红先/转绿 → WP14 → WP15。WP12 的守卫与记忆/初始化测试在实现前落地（红）；WP14 让本仓守卫转绿。WP13 的迁移夹具在 WP07 前可先建（它们只依赖声明）。

**Rollback / recovery**: 实现层用 git 提交序列（每 WP 一个逻辑提交）；运行时搬迁不提供全局 undo，恢复路径是回执 `recover[]` 的逐条逆 move；被替换/移除类处置仍走 `.specify/archive/migrate/<run-id>/`；本仓 dogfood 前的状态由 `0cde03ef9` 可达。

## Test-First Coverage (SC-001…SC-008)

| SC | Test (new/updated) | Fixture | Red-first assertion | Red-ability drill |
|----|--------------------|---------|---------------------|-------------------|
| SC-001 | `tests/contract/test_runtime_store_layout.py` | repo tree + requirements table pin | inventory covers every baseline member once; declaration == table == code consumer sets; `test ! -d .specify/memory` (dogfood) | remove one inventory row / add an unlisted member → red |
| SC-002 | `tests/integration/test_memory_preservation.py` | `tmp_path` init fixture | record→recall both tiers; prune/reindex; determination persisted + recalled | point one scope at the old root → red |
| SC-003 | `tests/integration/test_dispatch_injection_paths.py` | dispatch fixture + seeded memory | injected refs under the two new roots; 7/4/5 sets; reverse-token boundary | inject a feedback path as a "memory" source → red |
| SC-004 | `tests/integration/test_store_layout_migration_us1_us2.py` | legacy / seeded-legacy / dual / rerun | zero-write dry-run; byte-identical move; deterministic refuse; idempotent rerun | delete conflict check / make move byte-copy silently → red |
| SC-005 | `tests/integration/test_init_new_layout.py` | empty dir | session+knowledge seeded; no memory; other stores lazy | make init create `.specify/memory` → red |
| SC-006 | `tests/contract/test_store_layout_live_refs.py` | repo tree | measured allowlist == declared; zero outside; context match | add a literal to an unlisted file/line → red |
| SC-007 | `tests/contract/test_runtime_store_layout.py::test_mirror_member_set` + raw checks | repo tree | no NEW drift member on touched files; touched pairs byte-identical | skip one mirror regeneration → red |
| SC-008 | `tests/contract/test_tools_domain.py`, `test_specify_gitignore_template.py` | tmp git fixture | `*.json` ignored, `*.md` tracked; template == installed | revert `tools/*.json` to `tools/` → red |

Every new test is authored in WP12/WP13 **before** its implementing WP (red), and its mutation drill is recorded in `test-evidence/`. Full suite: baseline capture at implement start, final run must show no new name-level failures (`run-tests.sh` mandatory, parallel by default).

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises — this skeleton carries the column set and nothing else.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | CPython `>=3.8` 的标准库足以完成路径解析、目录移动、摘要与回执写入 | `pyproject.toml` `requires-python`；本环境 3.11 实测（`research.md` R-10） | verified | — |
| EP-002 | 本环境存在同时具备 pytest 与 typer 的解释器，测试入口可执行 | `/usr/local/bin/python3`：pytest 8.4.2 / typer 0.19.2；`SPECKIT_PYTHON=... run-tests.sh` 两次实测 rc 0（`test-evidence/plan-baseline-*.txt`） | verified | — |
| EP-003 | `specify migrate` 可在本仓以 framework-source 形态运行且 dry-run 零写入 | `research.md` R-11 实测（450 replace items，rc 1，树未变） | verified | — |
| EP-004 | 声明层 reader 可装载 `mapping` fact，且 `shared/` 随 wheel 分发 | `declaration_reader.py` 支持 `mapping`；`pyproject.toml` force-include `shared` | verified | — |
| EP-005 | 本仓 `.specify/` 与源面共享同一文件系统，存储目录可原子 rename | 同一工作树；`_migrate_execute_relocate` 既有行为 | verified | — |
| EP-006 | 迁移执行期间没有旧版引擎并发写入同一存储 | 无全局锁；以 manifest 摘要检测并发写并 `failed`+`aborted` | unverified | — |
| EP-007 | git 能识别目录搬迁并支持 `git log --follow` 追溯 | 未实测（dogfood 后验证；`git mv` 语义） | unverified | — |
| EP-008 | 全量测试套件的名级基线可在实现起点一次采集 | 唯一入口支持 `--names-out`（`run-tests.sh` 既有能力）；本阶段未跑全量 | unverified | — |

## Inherited Blockers

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:
- `097`: `.specify/features/024-specification-workspace-versioning.md`, `.specify/specs/097-speckit-migrate-command/verification.md`

本特性依赖 097 已落地的 `specify migrate`（plan/apply/receipt/resume）及其 `Ready for Review` 状态；025/055/015 不构成依赖（055 的协议保持不变、015 的命令面不扩展）。097 的 `verification.md` 无 `blocked`/`deferred`/`partial` 行，`deferred_tasks=` 为空；024 详情无 `## Deferred` 节——提取集为空。

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | — | not-applicable | — | — | 声明的依赖集不携带 blocked/deferred/partial 记录；无行可处置 |

## Complexity Tracking

N/A — Constitution Check 无 Fail / Partial 行，无需豁免。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | `data-model.md` | 10 entities（E-1…E-10）+ 状态迁移 + 10 不变量 |
| Contracts | `contracts/` | 4 files：`store-layout.contract.md`（C-1…C-8）、`migrate-store-layout.contract.md`（M-1…M-9）、`memory-and-injection.contract.md`（P-1…P-6）、`live-reference-migration.contract.md`（L-1…L-8） |
| Quickstart | `quickstart.md` | 9 scenarios（0 基线实测 / 1 旧布局收敛 / 2 并存拒绝 / 3 全新初始化 / 4 记忆保持 / 5 注入 / 6 tools 域 / 7 dogfood / 8 活引用守卫）；逐例列前提与验证路径（route a/b） |
| Feature ref | `feature-ref.md` | Feature 024 绑定 + FR→WP 26/26 + SC→证据 8/8 |

与 Phase 0 预期的漂移：research 按预期独立成文（> 50 行且含实测引擎解剖）；契约数量 4（Phase 0 未预设数量，按规则面边界落地）。计数均取自落盘文件，非预写。
