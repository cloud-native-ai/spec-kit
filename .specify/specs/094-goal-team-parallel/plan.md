# Implementation Plan: goal/team 与 spec 的平行关系（重定义 085 的作用域与绑定模型）

**Branch**: `094-goal-team-parallel` | **Date**: 2026-11-09 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `094-goal-team-parallel` → Feature 094 goal/team 与 spec 的平行关系（Goal/Team × Spec Parallelism）
**Input**: Specification from `.specify/specs/094-goal-team-parallel/requirements.md` (43 FR / 12 SC; requirements + clarify validated 2026-11-09, commit `8badbd03`)

## Summary

Feature 085 hung the goal/team mechanism *below* the SDD flow: one scope resolver with a `spec` member
(`<spec-dir>/goal/`, `<spec-dir>/team/`), one pair of "Temporary Goal / Temporary Team" concepts, and one routing
carve-out that made `.specify/goal/**` and `.specify/teams/**` forbidden paths for a run. Feature 094 deletes that
subordination and replaces the directory-position criterion with a **binding model**:

```text
archive layers (STR-002 "archive-scope", closed three rows)
  .specify/anchoring/<slug>/goal.md   goal archive  ─┐  (dir renamed from .specify/goal/ upstream 2026-11-09;
  .specify/teams/<slug>/team.md       team archive   ├─ the ONLY write targets (FR-007)
  .specify/.tmp/                      run scratch    ┘  (not an archive row; FR-037)

binding record (STR-001), carried inside each definition:
  owner: sdd-run | command-run | human
  owner_id: <state-spine run_id>            origin: null | <spec dir name>
lifecycle: goal active|achieved|abandoned   team active|archived
writability = deterministic function(binding, archive layer)   (FR-038; not a declared dimension)
```

Both lines become peers: a plain SDD run and a bare goal+team each finish a delivery without the other (FR-014,
SC-005). Complex work gets a **handoff contract** (STR-004 `handoff.md`) written by `tasks` and consumed by
`implement`: spec keeps design plus sole ownership of `requirements.md` / `tasks.md` / `verification.md`, the crew
gets the contract's territory expanded into `territory.write`, and the three spec artifacts land in
`territory.forbidden` (FR-016…FR-020, FR-034…FR-036).

The mechanism stays inside the existing engines and owners: `scripts/python/goal-utils.py` grows the binding,
migration, residual-probe and archive-writability actions; `skills/internal/create-team/` grows `handoff_ref` and
territory expansion; `shared/declarations/facts/` grows exactly two facts; the two concept owners are rewritten
rather than duplicated (FR-024, FR-031, RS-003, RS-004).

Delivery uses **6 concurrent plan packages** for this stage and, after `tasks`, dispatches **up to 6 implement executors
concurrently** in isolated git worktrees folded through the existing integration queue; the package partition and each
package's row count are declared in `tasks.md` § Package Map, not here — the shape 091 measured as the fix for the
single-agent bottleneck (§ Execution Model).

## Technical Context

**Language/Version**: Python `>=3.8` (`pyproject.toml` `requires-python`) for `scripts/python/goal-utils.py`, the two declaration facts and the new contract/unit suites; Markdown for concept owners, command templates, skills and contracts. Host interpreter measured `3.11.11` (pytest 8.4.2).
**Primary Dependencies**: none new. Consumes `declaration_reader.py` (fact reader), `flow-class-check.py` (existing command-class entry, left unmodified), `sync-mirrors.py` + `regen-command-copies.py` (mirror/copy projection), `scripts/bash/run-tests.sh` (serial runner), and the pre-analyze / decomposition / decision-tension gates.
**Storage**: `.specify/anchoring/<slug>/goal.md` and `.specify/teams/<slug>/team.md` (unified archive, STR-002; the goal directory was renamed from `.specify/goal/` upstream 2026-11-09, definition filename unchanged); `.specify/archive/goal-team/` (migration receipts + archived source trees, STR-003); `<spec-dir>/handoff.md` (STR-004); `<spec-dir>/test-evidence/` (dated records). No new top-level directory; `.specify/.tmp/` is the existing git-ignored scratch row.
**Testing**: pytest (`contract` / `integration` / `serial` markers registered in `pyproject.toml`); Tests Mode ON. Serial baseline captured at plan entry in `test-evidence/plan-baseline-names.txt` (46 pre-existing failing ids, identical across three consecutive serial runs); GATE-1 compares against that serial `FAILED` set, never a parallel-mode reading.
**Target Platform**: macOS/Linux maintainer hosts and every downstream project initialised from this framework; framework sources are edited here and reach client runtimes through publish → install → `specify init`.
**Project Type**: SDD framework (shared definitions, declaration facts, skills, command templates, Python engines, tests) — no runtime platform, no scheduler, no daemon.
**Performance Goals**: no wall-clock promise. The measurable target is execution shape: plan = 6 concurrent packages; implement = at least one stage dispatching several packages concurrently under `write_isolation=worktree`, every dispatch recording requested/effective concurrency.
**Constraints**: no new `/speckit.*` command; no second goal/team engine or schema; archive-not-delete for every migration; no new top-level directory; no push; framework template neutrality preserved; `flow-class-check.py` and the driver scripts are not modified by the new declaration entries.
**Scale/Scope**: 43 FR / 12 SC; 1 engine file extended (`goal-utils.py`) with about 9 new actions; 2 concept owners rewritten; 2 declaration facts plus their registration; 3 command templates; 6 skill/reference surfaces; 1 new contract artifact (`handoff.md`) with a three-way key pair; about 8 new test modules plus 11 dispositioned existing modules; spec-local definitions measured 2026-11-09 at analyze-repair round 4: the residual probe's own form (`*/goal/*/goal.md`, `*/team/*/team.md`, C-43) reads goal 9 / team 8 = 17, and the full census adds two one-level non-conforming team files (`088-speckit-visualization/team/team.md`, `092-non-disposable/team/team.md`), goal 9 / team 10 = 19 definition files; the earlier readings keep their dates — plan entry 7 goal / 7 team = 14 (`test-evidence/requirements-baseline-probe.txt`, 2026-11-09) and tasks stage 8 / 8 = 16 (tasks.md N-4, 2026-11-09) — and the residual probe remains the authority over every number.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md`, 22 principles in document order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design ruling cites FR ids; `contracts/` maps 43/43 FR in `feature-ref.md` § Delivery map. |
| II | Feature-Centric Development | ✅ Pass | Feature 094 row created in `.specify/features.md` and `.specify/features/094-goal-team-parallel.md`; this stage advances `Draft → Planned` only. |
| III | Intent-Driven Development | ✅ Pass | The same-objective binding record and the peer model come from the user's verbatim brief; the two open variants are recorded as T-004 / T-005 with named antitheses. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Tests Mode ON; every SC and every FR group has a red-first module named in `contracts/owner-rewrites-and-tests.md` X; § Complexity Tracking records the pre-implement baseline as a ruling, not as pre-written red. |
| V | AI Agent Integration Standards | ✅ Pass | No agent roster or neutral-metadata-key change; the crew/handoff design consumes existing `team.md` seats untouched. |
| VI | Continuous Quality & Observability | ✅ Pass | Each migration writes a per-entry receipt; the residual probe is read-only and enumerable; archived source trees move into STR-003 instead of `.bak` copies. |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify → plan respected; status ceiling for this stage is `Planned`; tasks / checklist / analyze / review still ahead. |
| VIII | Code as the Single Source of Truth | ✅ Pass | § Execution Premises and § Phase 0 cite live reads: the `goal-utils.py` action list, `resolve_scope` closed set, `create_goal` collision behaviour, `MIRROR_PAIRS`, and the 46-id serial baseline. |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One engine extended, two fact files, two owners rewritten, one new contract artifact; no scheduler, daemon, registry or second queue. |
| X | Documentation Naming & Location Conventions | ✅ Pass | `handoff.md` is lowercase and path-semantic (STR-004); `receipts/` and `trees/` under STR-003 are registered in `framework-map.md` (FR-029). |
| XI | Dogfooding (Self-Application) | ✅ Pass | Framework-source edits only (`scripts/`, `skills/`, `shared/`, `templates/`); `.specify/` copies regenerate through `sync-mirrors.py` / `regen-command-copies.py`; the 094 run itself is migrated by the mechanism it ships (A8). |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses `goal-utils.py`, `declaration_reader.py`, `flow-class-check.py`, `sync-mirrors.py`, `create-team` / `run-team` / `improve-team`; migration and probe are actions of the existing engine (RS-004), never a second executable. |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Task Understanding (one binding vocabulary) and Reliable Delivery (handoff contract, territory as mechanism, archive-not-delete); every evidence claim is bounded to a measured reading. |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Binding / scope / lifecycle owned by `goal-definitions.md` and `conceptual-model.md` (FR-024); the scope value set has one owner doc (FR-025); both facts are owned by `shared/declarations/facts/`; every other surface cites by path. |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | `quickstart.md` defines binding, archive layer, handoff contract and the designer/crew metaphor at first use; every command carries its premises and evidence paths. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Collision, unbound definition, non-`human` write on a bound goal, cross-layer write and terminal-goal rebind are named refusals with exit codes (C-4, C-11, C-16, C-18); no silent fallback. |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | One new directory kind under an existing tree (`.specify/archive/goal-team/`), registered in `framework-map.md`; no ad-hoc directory; receipts and runs stay per-entry files. |
| XVIII | Grounded Naming | ✅ Pass | `owner` / `owner_id` / `origin` / `binding` / `archive-scope` / `handoff.md` are carried verbatim from the spec's `[[STR-NNN]]` literals; no invented synonym. |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | The user-visible surface is one question — where does this goal live, who owns it, who may write it — answered by the binding line; receipt columns and engine actions stay internal. |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | GATE-1 baseline is the serial `FAILED` id set in `test-evidence/plan-baseline-names.txt`; targeted suites per package during implement; `serial`-marked tests stay out of the parallel pass. |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | Every new `goal-utils.py` action inherits the existing `guard_argv` plus `--help` / `--version`; RS-004's joint acceptance pins it. |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | § Execution Model carries the re-anchor duty into every package brief (rules before goal), matching the 094 driver contract. |

**Gates Status**: ✅ All 22 rows Pass. No ❌ and no ⚠ row; § Complexity Tracking records one **ruling** (the pre-implement test baseline), which is not a violation.

**Re-check after Phase 1**: 2026-11-09 — re-read against the landed Phase 1 artifacts (5 contracts, 13-entity data model, 9-scenario quickstart, `feature-ref.md`). Rows I, IV and XIV were refreshed in place: the FR→contract map is complete (43/43, regenerated from the contracts rather than hand-maintained), every SC names its red-first module, and the declaration-owner row cites both fact files. No row changed verdict.

## Decision Tensions

Owner of the record shape, admissibility, rejection forms and the load-bearing threshold:
`.specify/shared/guidelines/decision-tension.md`. Fields: `decision`, `antithesis`, `binding_constraints`
(`pole_a` / `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; id `T-NNN`.

### T-001 — 把「临时 goal」升格为统一档案里的一条绑定记录，而不是保留两层档案

- **decision**: 删除 spec-local 档案层级与「临时/全局」分类，所有定义落 `.specify/anchoring/<slug>/goal.md` 与 `.specify/teams/<slug>/team.md`，归属只由 [[STR-001]] 记录的 `owner` / `owner_id` / `origin` 回答。
- **antithesis**: 保留两层档案，只把 spec-local 路径改名并继续用目录位置回答归属；当仓库只需要「一眼看出哪些 goal 属于活跃 spec」、且没有任何命令运行需要 goal/team 时它更优——无需迁移、无需绑定重写、无需改动既有 spec-local 定义（plan-entry 14 条）。
- **binding_constraints**:
  - pole_a: 归属必须可判定且只有一处回答；目录位置一旦参与回答，两条线就再次变成从属。
  - pole_b: 既有 spec-local 定义（plan-entry 14 条；2026-11-09 最新读数见 EP-002：probe 形 17、全量普查 19）与全部 scope 测试必须可迁移、可解释，不能一次改动就丢失历史。
- **discriminating_evidence**: 在同一棵树上创建 `owner=command-run` 与 `owner=sdd-run` 两条定义后断言：`goal-utils.py resolve-scope --json` 的两个根是否恒为 `.specify/anchoring` 与 `.specify/teams`；结果二值：恒等 / 出现 spec 根。
- **expected_sacrifice**: SC-003 Source ↓ 一次性迁移全部 spec-local 定义（plan-entry 14 条；2026-11-09 最新读数见 EP-002：probe 形 17、全量普查 19）必须产出逐条回执，迁移证据面从零变为逐条。
- **revision_trigger**: 迁移后出现「同一 slug 两条候选」或任一调用方仍能从路径推断归属（契约测试转红）≥2 次 → 重开，恢复分层档案并把它声明为 `origin` 的唯一来源。
- **tension_id**: T-001

### T-002 — 可写性写成绑定 × 档案层级的确定性函数，而不是一张 forbidden-paths 禁令

- **decision**: goal 档案在「被任意 team 绑定时只由 `human`（`/speckit.goal`）可写」，team 档案由其 owner 身份可写，越权写以退出码拒绝；不再用 `.specify/anchoring/**` forbidden path 表达防线（rename 前该字面为 `.specify/goal/**`）。
- **antithesis**: 保留 085 的禁令文本（运行与 child line 不得写 `.specify/goal/**`、`.specify/teams/**`）并在派发前检查；当只有一个运行、且所有写入都经 `/speckit.goal` 时它更优——没有新的判定函数要测，也没有跨线失权的意外。
- **binding_constraints**:
  - pole_a: 平行线必须能各自写自己的档案，禁令式防线会把「谁的档案」变成文档解释问题。
  - pole_b: 一条运行不得污染另一条线的共享档案，且拒绝必须机器可判定，不能靠自觉。
- **discriminating_evidence**: 用 `owner=command-run` 的身份对一条已被 sdd-run team 绑定的 goal 执行写动作，读退出码与拒绝文本；结果二值：非 0 退出并点名绑定 team / 静默成功。
- **expected_sacrifice**: SC-009 Source ↓ 可写性从「读一行禁令」变为「读一个函数」，且同一 goal 被另一线 team 绑定时原 owner 失权（A10 有意接受）。
- **revision_trigger**: 出现「合法写入方被误拒」≥2 次且无法用 `human` 通道解除 → 重开，改为显式的逐定义写权限名单。
- **tension_id**: T-002

### T-003 — 绑定拆成 `owner` + `owner_id` + `origin` 三维，而不是一个 `owner` 字段

- **decision**: 归属记录由 `owner`（`sdd-run` / `command-run` / `human`）、`owner_id`（状态脊 `run_id` 同名同义）与 `origin`（`null` 或 spec 目录名）三部分组成。
- **antithesis**: 单个 `owner: <spec|command|global>` 字段；当只需要区分「有没有 spec」、且一次运行从不跨 spec 复用时它更优——记录更短、重写更少、迁移比较更简单。
- **binding_constraints**:
  - pole_a: 「谁发起的哪个运行」和「源自哪个 spec」是两件事，合并会把「被 spec 派生」误读成「属于 spec」。
  - pole_b: 每多一个维度就多一个值域 owner、一条重写规则与一条契约测试。
- **discriminating_evidence**: 取一条 `origin` 非空且被另一线 team 绑定的定义并查询归属；结果二值：三个维度分别可读且互不覆盖 / 任一维度丢失或被另一维度推出。
- **expected_sacrifice**: SC-009 Source ↓ 定义文件的绑定区从一行变三行，字节不变性必须在绑定重写时显式保持，比较器要排除整段绑定区。
- **revision_trigger**: 绑定重写后 `origin` 与 `owner` 出现「同一事实两种写法」≥2 次 → 重开，合并为两维并给 `origin` 另立读取面。
- **tension_id**: T-003

### T-004 — 引擎作用域取值收窄为 `goal` / `teams` / `auto`（`global` 与 `spec` 一并出域），而不是保留位置命名成员

- **decision**: `resolve-scope` 的 `--scope` 只保留封闭三成员 `goal` / `teams` / `auto`：前两个直接命名 [[STR-002]] 的两条档案行，`auto` 表示引擎在两条档案行之间唯一解析；`spec` 按 FR-008 删除，`global` 随单一全局档案行拆分为两条并列档案行而不再有对应成员——两个旧取值名一并出域，旧调用以 argparse 既有形态 `invalid choice: <value>` 退出 2。`--spec-dir` 仍被接受，只用于解析 `origin` 与 `auto` 的输入有效性，不再决定落点。**成员名命名档案行/定义种类，不命名目录**：上游 2026-11-09 已把 goal 档案行目录从 `.specify/goal/` 改名为 `.specify/anchoring/`（`ARCHIVE_DIRNAME` 实测），定义文件名仍是 `goal.md`（`DEFINITION_FILENAME` 实测），故 `goal` 成员不随目录改名 `anchoring`——改名会同时撕开 FR-025 / 本条 / 契约 C-9 的三面同一取值集，并把「取值 = 目录名」的旧读法重新引入 FR-025 明文禁止的位置语义。引擎现值仍为 `global|spec|auto`，这是本特性要改写的事实起点，不是本条的退让。〔本条的取值集与 FR-025、契约 [[C-9]] 是同一份；Q13 判读见 requirements.md Clarifications；D4 裁决记录见 requirements.md § Notes 的 round-3 小节〕
- **antithesis**: 保留 `global` / `auto` 两个取值名并只收窄其含义（`global` 不再指「全局目录」而指「档案层」），从而既有 8 个 scope 测试与全部调用脚本的文本几乎不动；当「一次性改完所有调用面」的成本高于「一个名字带着旧含义继续存活」的风险时它更优——零调用方修改。
- **binding_constraints**:
  - pole_a: 一个取值的**名字**就是它的含义面。让 `global` 改名后继续接受，等于让「全局/临时」这套被本特性判定为误读的词汇以取值名的形状回流，与 FR-025「不含任何以 spec 位置命名的成员」同源的判据对它一样成立。
  - pole_b: 删除成员会让既有调用以退出 2 失败，必须一次性改完 8 个测试模块与全部调用面，包括 `test_scope_resolution.py` 与 `test_goal_scope_engine.py` 的 `global` / `spec` 断言。
- **discriminating_evidence**: 对 `--scope global`、`--scope spec` 与 `--scope <任意未登记值>` 各执行一次 `resolve-scope`；结果二值：三者以同一 `invalid choice` 形态退出 2 / 任一被接受。反向读数：`--scope goal`、`--scope teams` 各退出 0。
- **expected_sacrifice**: SC-010 Source ↓ `test_scope_resolution.py` 与 `test_goal_scope_engine.py` 的 22 处 `global` / `spec` 断言全部进入处置清单，其中一部分从断言改为「拒绝该取值」；`goal-utils.py` 中七处 `"global"` 字面量与两处 guidance 字符串一并改动（任务 T013 / T014）。
- **revision_trigger**: 下游项目报告「一次性迁走既有 `--scope global` / `--scope spec` 调用」阻塞 ≥2 次 → 重开，提供一版只读别名并在声明的版本点移除。另一条重开条件（D4 成员名裁决）：下游调用方把成员名当作目录名逐字映射（例如把 `--scope goal` 映射到 `.specify/goal/`）≥2 次 → 重开，把首成员改名为 `anchoring` 并同步 C-9 / 命令模板 / 8 个 scope 测试。
- **tension_id**: T-004

### T-005 — 复杂度判定与 goal/team 创建时机绑同一组声明值（任务数门槛）

- **decision**: 交接判定与「运行是否创建 goal/team」由同一条声明事实（任务数阈值，边界为「任务数 > 阈值 才复杂」）决定；直接执行的运行不创建，交接的运行在 `tasks` U4 之后创建并落 [[STR-004]]。
- **antithesis**: 让 goal/team 在每个 SDD 运行都创建（085 现状），复杂度只决定是否产出交接契约；当 goal 的价值在「每轮都留一份终态记录」而不在「施工交接」时它更优——记录一致，没有「有的运行没有 goal」的空档。
- **binding_constraints**:
  - pole_a: 简单工作必须能只走一条线（SC-005 要求以判定结果而非跳过来证明平行），凡是「无条件创建」都会让 SDD 线暗含对 goal 线的依赖。
  - pole_b: 「有 team 没 goal」与「有 goal 没 team」都不可解释，两条线必须有由同一判据给出的创建时点。
- **discriminating_evidence**: 对同一份 requirements 用两份 tasks 夹具（任务数 = 阈值、阈值 + 1）各跑一次判定并读产物；结果二值：前者无 goal/team 且无 [[STR-004]]、后者两者兼有 / 任一形态错配。
- **expected_sacrifice**: SC-005 Source ↓ 「只有 SDD」的夹具必须由判定结果产生而不是跳过创建；门槛成为一条新的单点事实，改动它就要同时改两个消费点。
- **revision_trigger**: 出现「需要为一次简单运行留 goal 记录」的真实诉求 ≥2 次 → 重开，把创建时机与复杂度判定解耦，并另立一条记录型绑定。
- **tension_id**: T-005

### T-006 — 迁移归 `/speckit.goal migrate-archive`，而不是 `/speckit.sanitize`

- **decision**: 档案搬移与回执是 `goal-utils.py` 的一个写动作，命令入口是 `/speckit.goal` 的新 `migrate-archive` 模式（team 一并处理）；`/speckit.sanitize` 只提供只读残余探测。
- **antithesis**: 把迁移交给 `/speckit.sanitize` 的 archive 处置族；当一次收尾已经在跑 sanitize、且档案整理天然属于「材料归档」时它更优——一个命令做完两类归档。
- **binding_constraints**:
  - pole_a: goal 档案只有一个写入口（`/speckit.goal` 与 `goal-utils.py`），第二个写入口会撕开 FR-007 的单一落点纪律。
  - pole_b: 迁移是破坏性风险动作，必须有人工可见的入口与回执，不能藏在整理类命令的后台处理里。
- **discriminating_evidence**: 检索「写 `.specify/anchoring/**`（rename 前字面 `.specify/goal/**`）的可执行路径」；结果二值：只有 `goal-utils.py` 的登记动作集合 / 出现第二个可执行体。
- **expected_sacrifice**: SC-002 Source ↓ 两个命令面各要一份说明（迁移归 goal，探测归 sanitize），读者需要知道去哪执行。
- **revision_trigger**: sanitize 的调用频率显著高于 goal 且迁移长期未执行 ≥2 轮 → 重开，在 sanitize 里加一个只转调的入口（仍不新增写路径）。
- **tension_id**: T-006

### T-007 — 复杂度门槛写成声明层事实，而不是引擎常量

- **decision**: 两条判定（命令族入族、交接复杂度阈值）落 `shared/declarations/facts/` 的独立事实文件，由既有读取入口消费，并在 `shared/declarations/contract.yaml` 登记。
- **antithesis**: 把阈值写成 `goal-utils.py` 的模块常量并在 `--help` 里显示；当只有一个消费点、且判定从不被别的引擎读取时它更优——零声明层成本、改动即生效。
- **binding_constraints**:
  - pole_a: 阈值必须有唯一 owner 且边界语义确定，引擎常量会被两处复制（引擎与驱动正文）。
  - pole_b: 声明层条目未登记就是 `owner-unavailable`，等于交付了一个不生效的判据，必须连同登记一起交付。
- **discriminating_evidence**: 删除或改写该事实文件后运行两个消费点的契约测试；结果二值：两处同时以 `owner-unavailable` 失败 / 任一仍以默认值通过。
- **expected_sacrifice**: SC-006 Source ↓ 声明层多两个文件与一次登记，任何取值改动都要走声明面而非模块常量。
- **revision_trigger**: 声明层读取无法表达边界语义（例如需要区间而非单值）≥2 次 → 重开，降级为引擎常量并在 owner 文档写明。
- **tension_id**: T-007

## Project Structure

### Documentation (this spec)

```text
.specify/specs/094-goal-team-parallel/
├── plan.md                 # this file (/speckit.plan output)
├── research.md             # Phase 0 output — 31 rulings R-01…R-31 (standalone: exceeds 50 lines)
├── data-model.md           # Phase 1 output — 13 entities, validation rules, state transitions
├── contracts/              # Phase 1 output — 5 files, 113 clauses
│   ├── binding-and-lifecycle.md           # C-1…C-30  binding record, scope values, writability, lifecycle, parallelism
│   ├── unified-archive-and-migration.md   # C-31…C-52, C-112…C-113  archive layers, receipts, migration, probe, idempotency, resident backfill
│   ├── handoff-contract.md                # C-53…C-70  handoff.md shape, three-way keys, territory, writeback
│   ├── command-family-and-declarations.md # C-71…C-90  command family, two facts, contract.yaml registration
│   └── owner-rewrites-and-tests.md        # C-91…C-111  owner rewrites, driver protocol, 085 disposal, evidence
├── quickstart.md           # Phase 1 output — 9 scenarios S-0…S-8
├── feature-ref.md          # Phase 1 output — binding, delivery surface, FR→contract map, disclosed rulings
├── notes/                  # execution lessons (read-only input) + overlap adjudication
├── test-evidence/          # dated records: baseline probe, serial FAILED ids, gate readings
├── tasks.md                # /speckit.tasks output — NOT created here
└── verification.md         # /speckit.implement output — NOT created here
```

### Source Code (repository root)

```text
scripts/python/goal-utils.py                       # EDIT: binding read/write, scope value set, migrate-archive, residual probe, archive writability, legacy-key alias
shared/declarations/facts/goal-team-command-family.yaml    # NEW: command-family fact (FR-005, FR-006, FR-031)
shared/declarations/facts/goal-team-handoff-threshold.yaml # NEW: complexity threshold + creation timing (FR-018, FR-031, FR-039)
shared/declarations/contract.yaml                  # EDIT: register both facts (subset id + value domain)
shared/definitions/goal-definitions.md             # EDIT: binding/scope/lifecycle owner; Temporary Goal section replaced
shared/definitions/sdd-routing-definitions.md      # EDIT: carve-out rewritten (no "Temporary"; hierarchy ban kept verbatim)
shared/definitions/framework-map.md                # EDIT: Goals / Teams / archive rows; specs row no longer implies goal/team
skills/internal/create-team/references/conceptual-model.md # EDIT: binding model, team lifecycle, handoff_ref
skills/internal/create-team/references/create-mode.md      # EDIT: team.md schema gains binding + handoff_ref + archive path
skills/internal/create-team/SKILL.md               # EDIT: creation timing, archive path, handoff territory expansion
skills/internal/manage-goal/SKILL.md               # EDIT: migrate-archive mode, binding rewrite mode
skills/internal/run-team/SKILL.md                  # EDIT: archive-scope load, archived team refuses to run
skills/internal/improve-team/SKILL.md              # EDIT: handoff_ref / territory edits under binding discipline
templates/commands/goal.md                         # EDIT: migrate-archive mode, scope values by pointer
templates/commands/team.md                         # EDIT: scope values by pointer
templates/commands/feedback.md                     # EDIT: declare its goal/team creation timing (FR-040)
skills/external/sdd-loop-driver/SKILL.md           # EDIT: § Temporary Goal/Team → binding model; creation timing by declaration
skills/external/sdd-loop-driver/references/checkpoint-protocol.md # EDIT: goal/team paragraphs to the new model
skills/external/sdd-loop-driver/references/decomposition-model.md  # EDIT: implement packages <=6 concurrent, per-package ceiling 16, worktree writes
tests/contract/, tests/unit/, tests/integration/   # NEW + EDIT: contract suites, 085 disposal, structural invariants
docs/reference/                                    # EDIT: command/engine/skill references for the new surfaces
```

**Structure Decision**: this spec extends the existing framework layout and creates **no new top-level directory**.
The only new directory kind is `.specify/archive/goal-team/` (receipts one file per entry, plus archived source
trees), registered in `framework-map.md` under `directory-governance.md` § 3. Framework sources live in `scripts/`,
`shared/`, `skills/` and `templates/`; every `.specify/` copy is produced by `sync-mirrors.py` or
`regen-command-copies.py` and never hand-edited.

### Mirror Obligations

Drift is measured **before** any edit: `sync-mirrors.py --check` already reports the tree's pre-existing drift, so the
criterion below is "no NEW drift on the pairs this spec touches". An absolute "all green" criterion would be
unpassable whenever unrelated drift predates this spec.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/python/goal-utils.py` | `.specify/scripts/python/goal-utils.py` (MIRROR_PAIRS `scripts`, strict) | `python3 scripts/python/sync-mirrors.py --check` — no NEW drift on `scripts` |
| `shared/definitions/{goal-definitions,sdd-routing-definitions,framework-map}.md` | `.specify/shared/definitions/…` (MIRROR_PAIRS `shared`) | same — no NEW drift on `shared` |
| `shared/declarations/facts/*.yaml`, `shared/declarations/contract.yaml` | `.specify/shared/declarations/…` | same — no NEW drift on `shared`; `declaration_reader.py --action get --fact <slug>` returns the new entry |
| `skills/internal/{create-team,manage-goal,run-team,improve-team}/**` | `.specify/skills/internal/…` (MIRROR_PAIRS `skills/internal`) | same — no NEW drift on `skills/internal` |
| `skills/external/sdd-loop-driver/**` | `.specify/skills/sdd-loop-driver/**` (MIRROR_PAIRS `skills/external`) | same — no NEW drift on `skills/external` |
| `templates/commands/{goal,team,feedback}.md` | per-tool copies `.claude/commands/speckit.*.md`, `.github/prompts/speckit.*.prompt.md`, `.qoder/commands/speckit.*.md`, `.opencode/command/speckit.*.md` via `regen-command-copies.py`; NO `.specify/templates/commands/` mirror (retired) | `python3 scripts/python/regen-command-copies.py --check` — regenerated copies contain the edit and no other copy moves |

## Execution Premises

Owner of this table's shape, its `Status` / `Decision` domains and the invalid-row rule:
`shared/workflow/acceptance-hardening.md` § Execution Premises.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | `python3` >= 3.8 with `pytest` is available and the suite runs without network or a daemon. | `pyproject.toml` `requires-python`; host `python3 --version` = 3.11.11; `test-evidence/plan-baseline-names.txt` produced by `scripts/bash/run-tests.sh` in this session | verified | — |
| EP-002 | The spec-local definitions the residual probe enumerates are the migration subject — the count is the probe's reading, not a frozen constant: plan-entry 7 goal / 7 team = 14, tasks-stage 8 / 8 (tasks.md N-4), analyze-repair round 4 (2026-11-09) probe-form reading goal 9 / team 8 = 17, with the full census at goal 9 / team 10 = 19 definition files (two one-level non-conforming team files: `088-speckit-visualization/team/team.md`, `092-non-disposable/team/team.md`) — and their slugs collide with none of the 6 goal / 12 team archive entries. | `test-evidence/requirements-baseline-probe.txt` (goal 7 / team 7); re-measured on this tree 2026-11-09 during analyze-repair round 4 (probe form goal 9 / team 8 = 17; full census goal 9 / team 10 = 19, two files at one-level non-conforming paths); programmatic overlay of the two archive trees against the spec-local trees returned two empty intersections | verified | — |
| EP-003 | `create_goal` and `definition_path` already refuse duplicate definitions, so the single-archive collision refusal (FR-021 and the Edge Case) needs no second detector. | `scripts/python/goal-utils.py` `create_goal` raises `GoalError` when `definition_path(...).exists()`; `definition_path` resolves `archive_root(repo_root)/slug/goal.md` | verified | — |
| EP-004 | The declaration layer is readable through one entry point and an unregistered fact surfaces as `owner-unavailable`, so two new facts can be consumed without touching `flow-class-check.py`. | `declaration_reader.py --action get --fact flow-class-classes` returns the entry; `load_fact` raises the absent finding for an unknown slug; `flow-class-check.py --action lookup --unit-id spec:094-goal-team-parallel` exits 0 | verified | — |
| EP-005 | Implement-stage concurrency (up to 6 executors, per-package ceiling 16, worktree writes) has an existing integration queue in 064 and is safe to reuse. | the execution-lessons record `notes/execution-lessons-2026-11-09.md` § 1 (3-package fix loop, zero integration conflicts); `skills/external/sdd-loop-driver/references/decomposition-model.md` § 13 and § 16 | verified | — |
| EP-006 | The serial `FAILED` id set is a stable comparison surface and the 46 baseline failing ids are unrelated to goal/team behaviour. | `test-evidence/plan-baseline-names.txt` (46 fully qualified ids) and `plan-baseline-stability.txt` (empty diff between consecutive runs); goal/team suites are green on this tree — `test_scope_resolution.py` 8 passed, the 7-module goal/team set 171 passed | verified | — |

## Inherited Blockers

Dependency set: none.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|

## Document Structure

Not produced: this is an `execution`-class line (`flow-class-check.py --action lookup --unit-id
spec:094-goal-team-parallel` → `flow_class: execution`), and the `## Document Structure` section is required of
expression-class lines only. The section is omitted rather than left empty.

## Complexity Tracking

N/A — no ❌ Fail and no ⚠ Partial row in the Constitution Check. One ruling is recorded for the reader rather than as
a violation: Principle IV's red-first evidence can only be *measured* once `tasks` / `implement` land the failing
modules (Tests Mode is on and every SC names its red-first module in `contracts/owner-rewrites-and-tests.md`
X); at plan time the baseline is the 46-id serial `FAILED` list.

## Phase 0: Research Review

Findings are recorded in [research.md](research.md) as R-01…R-31. The rulings that shaped the design:

- **R-01 / R-02**: the binding record lives *inside* the definition file (no second store), and one objective carries
  both the `sdd-run` and `command-run` families, which removes the reason 085's scope-ambiguity branch existed.
- **R-05**: archive layout is `.specify/archive/goal-team/receipts/<kind>-<slug>.yaml` plus
  `.specify/archive/goal-team/trees/<spec>/<kind>/<slug>/`; receipts are one file per entry, never one shared
  `.jsonl` (Concurrent Development Safety).
- **R-06**: `goal.md` / `team.md` frontmatter is read by a new, small, closed-subset reader inside `goal-utils.py`
  (`key: value` plus inline lists, four scalar kinds). `declaration_reader.parse_subset` is deliberately NOT reused:
  its refusing grammar would reject the very key set it is asked to read.
- **R-09**: the `run_id` vocabulary is not re-declared; `owner_id` references the existing state-spine field and the
  contract test asserts the *name*, not a second schema copy.
- **R-16 / R-19**: `archive-scope` keeps its name (it is the spec's `[[STR-002]]` literal and already names the archive
  layers); its value set is the archive-layer names plus `auto`, with `spec` deleted.
- **R-21**: the complexity decision returns `direct | handoff` rather than yes/no, so one computation answers both
  "is this complex" and "does this run create a goal/team".
- **R-28**: the 085 disposal list is measured, not inherited from assumption A7 — 11 modules carry spec-local or scope
  assertions, and `tests/contract/test_goal_writeset.py` carries none.

## Execution Model

The plan is executed under the user's large-concurrency instruction, and the same model is designed into `implement`:

| Stage | Packages | Concurrency | Write isolation | Evidence rule |
|-------|----------|-------------|-----------------|---------------|
| plan | 6 (`plan-wp01`…`plan-wp06`) | 6 | shared tree with disjoint file sets (table below) | each package records its own gate reading |
| tasks | 1 | 1 | shared tree | one `tasks.md`; the implement packages and their row counts are declared in its own § Package Map |
| implement | ceil(tasks/10), cap 6 concurrent | 6 | `write_isolation=worktree` (child line plus its own worktree), integrated through the 064 queue in declared order | targeted package suite per package; two full-suite slots only (implement start and after review) |
| review | 4 segments | 4 | read-only | one fresh-context verifier per package; a package verdict never substitutes for stage U4 |

Rules carried into every package brief, from `notes/execution-lessons-2026-11-09.md`:

1. **Clean before closure**: fix and integration worktrees under `.specify/.tmp/` are removed *before* the closure
   suite runs, otherwise goal-migration, isomorphism and script-interface tests see duplicate repo copies (lesson 2).
2. **The serial baseline is the comparison face**: GATE-1 compares the serial `FAILED` id set against
   `test-evidence/plan-baseline-names.txt`; a parallel-runner reading is never used (lesson 3).
3. **added is not modified**: a tracked `test-evidence/*.txt` record is a dated record, not a live face, and a modified
   command file is not a new command; tests encode that distinction (lesson 4).
4. **Machine-readable acceptance block**: `verification.md` emits `SC-NNN_status=` lines, the only form
   `closure-acceptance-check.py` reads (lesson 5).
5. **Gate and engine argument shapes**: `pre-analyze-check` cell rules (`clean_cell` = paired code span plus prose,
   `EP-NNN` ids, closed `Status` / `Decision` domains), `overlap-check` vacuous `clear`, and the `run-determination`
   `--collected` / `--names-*` / `--green-check` shapes (lesson 6).
6. **Record writeback after renumber or acceptance**: any id renumber or second acceptance updates verification,
   notes and evidence pointers in the same commit (lesson 7).
7. **Cost discipline**: per-package ceiling 16 rows, never 60+ in one executor; every package brief names
   its `owned_paths` so two worktrees never write the same path (lesson 1).

### Plan packages (this stage, 6 concurrent, disjoint write sets)

| Package | Owns | Outputs |
|---------|------|---------|
| `plan-wp01` | Phase 0 research | `research.md` |
| `plan-wp02` | Phase 1 data model | `data-model.md` |
| `plan-wp03` | binding/lifecycle contract; archive/migration contract | `contracts/binding-and-lifecycle.md`, `contracts/unified-archive-and-migration.md` |
| `plan-wp04` | handoff contract; command-family/declarations contract | `contracts/handoff-contract.md`, `contracts/command-family-and-declarations.md` |
| `plan-wp05` | owner-rewrites/tests contract; quickstart | `contracts/owner-rewrites-and-tests.md`, `quickstart.md` |
| `plan-wp06` | feature reference and index/detail registration | `feature-ref.md` |

Integration is the coordinator's own act in the declared order `wp01 → wp02 → wp03 → wp04 → wp05 → wp06`; every
package reads this `plan.md` as its frame and never re-derives the delivery surface.

## Implementation Slicing

| Slice | Scope | Exit evidence |
|-------|-------|---------------|
| S0 | Preflight: serial baseline, drift baseline, real-data probe | `test-evidence/plan-baseline-names.txt`; recorded `sync-mirrors --check` reading; `requirements-baseline-probe.txt` |
| S1 | Binding model and scope value set in `goal-utils.py` (C-1…C-30) | `test_binding_model.py`; rewritten `test_scope_resolution.py` / `test_goal_scope_engine.py` |
| S2 | Unified archive, `migrate-archive`, residual probe, resident backfill (C-31…C-52, C-112…C-113) | `test_archive_migration.py`, `test_residual_probe.py`, `test_migration_interruption.py` |
| S3 | Two declaration facts, their registration, command family (C-71…C-90) | `test_declaration_facts.py`, `test_command_family.py` |
| S4 | Handoff contract, territory expansion, writeback (C-53…C-70) | `test_handoff_contract.py`, `test_handoff_territory.py` |
| S5 | Owner rewrites, driver and checkpoint protocol, command templates (C-91…C-97) | binding-model owner assertions; `test_checkpoint_protocol.py` updates; `regen-command-copies --check` |
| S6 | 085 test disposal and structural invariants (C-98…C-104) | disposal table plus the `pytest -m contract` reading; `test_no_spec_local_writes.py` |
| S7 | Real-data dry run, migration, closure | `test-evidence/migration-dryrun.txt`, `migration-applied.txt`, `verification.md` |

Decomposition gate at plan entry returned `proceed` (43 FR, ceiling 120). No split is required; if `tasks` later
exceeds the 160-row ceiling the driver's split gate owns that decision, not this plan.

## Phase 1: Design Artifacts Summary

Backfilled after the artifacts landed on disk; counts are taken from the files, never pre-written.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | R-01…R-31 (31 rulings) |
| Data model | [`data-model.md`](data-model.md) | 13 entities: E-1 binding record, E-2 goal definition, E-3 team definition, E-4 archive layer, E-5 migration receipt, E-6 residual probe reading, E-7 archive receipt, E-8 handoff contract, E-9 command-family fact, E-10 handoff threshold fact, E-11 legacy key alias, E-12 territory set, E-13 writability decision |
| Contracts | [`contracts/`](contracts/) | 5 files, 113 clauses (C-1…C-113; D1 rename): `binding-and-lifecycle.md` C-1…C-30, `unified-archive-and-migration.md` C-31…C-52 + C-112…C-113, `handoff-contract.md` C-53…C-70, `command-family-and-declarations.md` C-71…C-90, `owner-rewrites-and-tests.md` C-91…C-111 |
| Quickstart | [`quickstart.md`](quickstart.md) | 9 scenarios: S-0 preflight, S-1 command-run goal/team, S-2 migration dry run, S-3 migration apply, S-4 idempotent re-run and conflict, S-5 binding rewrite, S-6 handoff on a complex spec, S-7 crew write refusal and writeback, S-8 residual probe |
| Feature ref | [`feature-ref.md`](feature-ref.md) | binding, delivery surface, FR→contract map (43/43, generated by `clause_extract.clause_citations`), SC→measurement map (12/12), disclosed rulings |
