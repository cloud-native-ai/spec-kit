# Implementation Plan: subagent 并发作为框架基本属性（默认并发）

**Branch**: `093-concurrency-by-default` | **Date**: 2026-11-09 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `093-concurrency-by-default` → Feature 093 Concurrency by Default（subagent 并发作为框架基本属性）
**Input**: Specification from `.specify/specs/093-concurrency-by-default/requirements.md` (33 FR / 12 SC / 11 shared strings; requirements + clarify validated 2026-11-09, commits `11d49f18` + `6b291bb7`)

## Summary

The framework already ships concurrency machinery — Feature 064's write lines, worktrees and integration queue,
Feature 070's Work Packages and `wp-gate.py`, Feature 092's goal/team parallelism — but that machinery is a
*privilege of a few executors*, not a property of the framework. Feature 093 turns it into the default shape of
every execution body and makes serial execution an exception that must be named.

Three things land together, because landing one without the others reproduces the defect the user described:

```text
1. scope is a closed set, derived by filesystem enumeration         (FR-001…FR-004, SC-001)
     54 skills + 29 command templates + 17 agent definitions
     + 12 team definitions + 6 archived goals  = 5 enumeration roots
2. the default is concurrent; serial carries a named reason code    (FR-005…FR-009, SC-002, SC-003)
     condition <-> reason-code one-to-one, ordered reason list
     effective concurrency = maximum overlap of unit time spans
3. declaration must equal execution                                 (FR-021…FR-025, SC-005)
     dispatch capability, explicit handoff, or external process — else red
```

and the seven things a concurrent unit owes — partition rule, file-level write domain, slot cap with verifier
reserve, independent verification by a different id, declared-order integration, failure isolation, re-entry
(FR-010…FR-020, SC-004) — plus the high-order executors goal / team / loop (FR-026…FR-029, SC-007, SC-008).

Nothing new is invented for scheduling. The delivery is **eight declaration-layer fact entries** (the same
`shared/declarations/` substrate Feature 092 just proved), **one new read-only checker engine**
(`scripts/python/concurrency-check.py`) that is the only program turning those facts into verdicts, **ten new
contract test modules**, and **rewrites of the concept owners that already own this vocabulary** —
`subagent-definitions.md`, `decomposition-model.md`, `conceptual-model.md`, `goal-definitions.md`,
`stage-team-preset.md`, the agent definitions, and the command/skill surfaces. No second registry, no second
dispatcher, no new `/speckit.*` command, no change to the stage chain or its sentinels (spec Assumption A5).

The spec's own run is covered by FR-033 / [[STR-010]]: until this mechanism lands, a stage that declares
concurrency and runs serially records `mechanism-not-yet-landed`; it never presents a serial run as evidence.

## Technical Context

**Language/Version**: Python `>=3.8` (`pyproject.toml` `requires-python`) for `scripts/python/concurrency-check.py`, the eight declaration facts and the ten new test modules; Markdown for the concept owners, agent definitions, command templates, skills and contracts. The new engine is standard-library only and is exercised on the lower bound the project declares.
**Primary Dependencies**: none new. The engine consumes `scripts/python/declaration_reader.py` — the one read entry for `shared/declarations/` (measured 2026-11-09: `--action list` returns the nine `contract.yaml` keys plus 23 `facts/` slugs; `--action get --fact concurrency-class` currently exits 1 with `no declaration for fact`). Mirrors ride `scripts/python/sync-mirrors.py`; command copies ride `scripts/python/regen-command-copies.py`; existing gates ride `pre-analyze-check.py`, `decomposition-check.py`, `overlap-check.py`, `validate-decision-tensions.py`, `wp-gate.py`.
**Storage**: `shared/declarations/facts/*.yaml` (eight new fact entries, one per judgement surface); `<spec-dir>/test-evidence/` (dated records, one file per entry); the run's existing state-spine fences (owned by 070 — this feature reads them and adds no fence). No new directory kind, no ledger, no registry (Constitution XVII).
**Testing**: pytest with the project's registered markers (`contract` / `integration` / `serial`); Tests Mode ON. The serial baseline for GATE-1 is captured at plan entry under `test-evidence/` and compared by failure *name*, never by count and never against a parallel-mode reading (092 execution lesson 3).
**Target Platform**: maintainer hosts (macOS/Linux) and every downstream project initialised from this framework; the framework sources are edited here and reach client runtimes only through publish → install → `specify init`.
**Project Type**: SDD framework — declaration facts, one Python engine, concept-owner documents, agent definitions, command templates, skills, contract tests. No runtime platform, no scheduler, no daemon.
**Performance Goals**: no wall-clock promise is the release criterion. The measurable target is **execution shape**: every enumeration-root member mapped to exactly one declaration class, every serial record carrying a resolvable reason code, and at least one real run (not a fixture) reporting an effective concurrency `>= 2` measured as maximum interval overlap (SC-006).
**Constraints**: no new `/speckit.*` command; no second dispatch engine or registry; no unconditional parallelism; the SDD stage chain and its sentinels byte-unchanged; no push; `templates/` stays project-neutral (no repo-specific path facts); the new engine satisfies the script interface contract (Constitution XXI).
**Scale/Scope**: 33 FR / 12 SC; 1 new engine (~5 read-only actions); 8 declaration facts plus their registration probe; 11 concept/owner documents rewritten; 17 agent definitions judged (rewritten only where the coordinator verdict requires it); 29 command templates + 54 skills judged; 10 new contract test modules; 8 existing test modules dispositioned; 6 contract files carrying 92 clauses.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, 22 principles in document order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design ruling here cites FR ids; `feature-ref.md` § 1 maps 33/33 FR to contract clauses. |
| II | Feature-Centric Development | ✅ Pass | Feature 093 row and `.specify/memory/features/093.md` advance `Draft → Planned` in this stage; no new Feature invented; the four related Features (064/070/086/092) are dispositioned, never renumbered. |
| III | Intent-Driven Development | ✅ Pass | The five load-bearing choices carry named antitheses and reopening conditions in § Decision Tensions T-001…T-005, each traced to the user's verbatim brief. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Tests Mode ON; every SC and every FR group names a red-first module in `contracts/executor-obligations.contract.md` C-060; the 092-shaped fixture must be red before the fix and green after (SC-005). |
| V | AI Agent Integration Standards | ✅ Pass | No change to `AGENT_CONFIG` / `_ASSISTANT_TIERS`; the 17 agent definitions keep their neutral frontmatter schema — only the *judgement* of `capability-tools` is added, never a new key. |
| VI | Continuous Quality & Observability | ✅ Pass | Every verdict is machine-readable (`--json-out`), every serial exception carries a resolvable evidence pointer, and nothing is muted: the 092 defect is judged red, never tolerated. |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify → plan respected; this stage's status ceiling is `Planned`; the Pre-Status-Flip Gate is untouched. |
| VIII | Code as the Single Source of Truth | ✅ Pass | § Execution Premises and § Phase 0 cite live measurements (reader exit codes, 23 facts, 17 agent frontmatters, 12 teams / 10 with territory, `wp-gate.py --slot-cap-ceiling` default 4, 6 archived goals); numbers are measured, not remembered. |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One read-only engine, eight data-only facts, owner rewrites, tests. No scheduler, daemon, registry, queue or dispatcher; the runtime rule stays "the scheduler is prompt logic" (`decomposition-model.md` § 13). |
| X | Documentation Naming & Location Conventions | ✅ Pass | No reserved filename added; the fact slugs are lowercase kebab-case; the new test modules live where the existing suites live; `test-evidence/` keeps its per-entry naming. |
| XI | Dogfooding (Self-Application) | ✅ Pass | All edits land in the framework sources (`skills/`, `shared/`, `scripts/`, `agents/`, `templates/`) and reach the `.specify/` runtime through `sync-mirrors.py` / `regen-command-copies.py`; the 093 run itself is the first consumer (A4). |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses `declaration_reader.py`, `sync-mirrors.py`, `regen-command-copies.py`, `wp-gate.py`, the three stage gates and the existing contract-test helpers; the new engine covers a judgement no existing Tool performs. |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Controlled Execution (a declared, checkable default) and Change Validation (a check that goes red when concurrency disappears); the expected sacrifice is named in T-002 and T-005. |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Each judgement face has exactly one owner (§ Fact Owners), the semantic names live in the facts, and every other surface reaches them by path + anchor; T-001 is precisely the act of collapsing four restatements into one owner plus projections. |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | `quickstart.md` defines declaration class, serial reason code, effective concurrency and dispatch capability at first use; every command there carries its premises and evidence path. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | F-093-001/002/003 are carried as declared dispositions, not silently absorbed; the 092-shaped fixture is a red-by-design case; the coordinator verdict is explicitly blocked on its owner (T-004). |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory kind: facts go in the existing `shared/declarations/facts/`, evidence in the existing `<spec-dir>/test-evidence/`, tests in the existing `tests/contract/`. |
| XVIII | Grounded Naming | ✅ Pass | `concurrency-class`, `serial-reason`, `effective-concurrency`, `dispatch-capability`, `concurrency-contract`, `decomposition-coverage`, `executor-enumeration-roots`, `coordinator-dispatch-verdict` are carried verbatim from the spec's `[[STR-NNN]]` literals; no synonym is invented. |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | A reader opening any execution body finds the class it belongs to and the obligation that class imposes; the class member names are the user-facing vocabulary, not an internal enum. |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | This feature is the general case of the principle 086 already owns for tests: same criterion family, different subject. The new suites are parallel-safe by construction (read-only file assertions); the criterion itself is not restated here — 086 keeps its owner. |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | `concurrency-check.py` answers `--help` / `--version` before acting, rejects undeclared options with a non-zero exit, declares its side effects (writes only through `--json-out`) and its exit taxonomy (0/1/2). |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | § Execution Premises EP-010 records what this run keeps re-reading across stage boundaries; the user's verbatim sentence stays the anchor in the Summary's opening paragraph. |

**Gates Status**: ✅ All gates pass — no Fail, no Partial row, therefore no Complexity Tracking row is required.

**Re-check after Phase 1** (2026-11-09, after `contracts/`, `data-model.md`, `quickstart.md`, `feature-ref.md`
landed): the table was re-derived against the six contract files and the data model. Two rows were re-examined and
stayed Pass — XIV (the T-001 adjudication adds one owner and demotes three restatements to projections; the fact
files remain the only definition points) and XIX (the class table exists so that a reader opening a skill or a
command finds its obligation, not so that an implementation internal becomes visible). No row moved to Partial,
so `## Complexity Tracking` remains `N/A` and nothing downstream inherits a broken verdict.

## Decision Tensions

Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold:
`.specify/shared/guidelines/decision-tension.md` — one pointer. This section lists the field names and points at
that file; it MUST NOT restate the criteria table, the rejection list or the threshold table.

Fields: `decision`, `antithesis`, `binding_constraints` (with `pole_a` and `pole_b`), `discriminating_evidence`,
`expected_sacrifice`, `revision_trigger`; record identifier `tension_id` (`T-NNN`).

### T-001 — 槽位上限与天花板的 owner 收敛到两处，其余三处降为投影

- **decision**: 槽位上限的取值由 `shared/declarations/facts/concurrency-slot-and-reserve.yaml` 拥有，天花板由 `wp-gate.py` 的 `--slot-cap-ceiling` 拥有；`stage-team-preset.md`、`decomposition-model.md` § 22 与 § 20 的三处写法一律改写为指向这两处的投影，本特性不新增第四处取值。
- **antithesis**: 保留「按运行模式各带一套天花板」（临时 team 模式 `min(effective_concurrency, 24)`、普通运行 `min(4, line remaining)`、preset `min(6, …)`），让每个执行体按自己的模式读自己那一条；当各模式的天花板确实应当不同、且下游项目需要不改引擎就能调高上限时它更优——零迁移、零共享 owner。
- **binding_constraints**:
  - pole_a: FR-014 要求「唯一定义点 + 不出现第三处取值」；四处并存时任何一处漂移都不会被另一处发现，这正是本特性要关掉的失效模式。
  - pole_b: 天花板是运行期安全上界，把它整条绑进静态声明会让「宿主只剩 4 个槽位」这类运行事实被写成配置，从而在另一台宿主上给出错误结论（A3）。
- **discriminating_evidence**: 在仓库内检索 `slot_cap_ceiling|slot-cap-ceiling` 与 `min(4, line remaining)` / `min(effective_concurrency, 24)` 两类字面量：结果二值——除 `wp-gate.py` 的一处定义与 `concurrency-slot-and-reserve.yaml` 的一处取值外再无独立可赋值处（判绿）/ 仍存在两处及以上可独立赋值的数值（判红）。
- **expected_sacrifice**: SC-010 Source ↓ `test_sdd_loop_driver_wp_gate.py` 与 070 的 `WG-16` 断言从「各自持有上限」改写为「读取唯一 owner」，其中至少 3 条断言是重写而非删除，处置成本记入 070 的处置表。
- **revision_trigger**: 连续两次实现期出现「同一 manifest 在两种模式下被判出不同上限、且两次都没有工具发现」→ 重开，把上限改为 owner 条目内的命名成员（`default` / `temporary-team`），引擎按模式索引。
- **tension_id**: T-001

### T-002 — 并发度判据取「区间最大重叠数」，而不是「区间宽度和 ÷ 总时长」

- **decision**: 实际生效并发度 = 各单元 `[派发时刻, 返回时刻]` 时间区间的最大重叠计数；任一时间区间缺失时该次运行记「未评估」（FR-008、SC-006）。
- **antithesis**: 用平均并发度（各区间宽度之和 ÷ 观察窗口总时长），或直接取「派发过的单元数」；当运行时长差异极大、读者关心的是资源平均占用而非峰值同时在跑几个时它更优——一个数就把整段运行压平，不必逐单元留时间表。
- **binding_constraints**:
  - pole_a: SC-006 的取证必须区分「6 个单元真的同时在跑」与「6 个单元顺序跑完刚好占满同一段墙钟」；平均值与计数都区分不了。
  - pole_b: 最大重叠数要求每个单元留下两个时刻，缺失即无法判定；而原生派发未必会给出返回时刻。
- **discriminating_evidence**: 喂两条构造记录：6 个单元、每个区间 1 分钟、依次首尾相接共 6 分钟；以及 3 个单元互相重叠 1 分钟。结果二值——前者判 `effective=1`、后者判 `effective=3`（判绿）/ 前者被判出 `>= 2`（判红）。
- **expected_sacrifice**: SC-006 Source ↓ 每个并发单元必须额外记录两个时刻并接受「区间缺失即未评估」，这让原生派发在拿不到返回时刻时无法声称并发——本特性的 implement 阶段首次运行很可能因此落在未评估（与 A4 一致）。
- **revision_trigger**: 若连续两轮真实运行因「宿主不提供返回时刻」只能报未评估，且第二轮的宿主能力探针（RS-005）确认该宿主支持并行 → 重开，补充一个由派发方可观测的等价对（如 `spawned_at` / `settled_at`）并重判 SC-006 的取证面。
- **tension_id**: T-002

### T-003 — 写域取文件级路径集，拒绝目录级区域声明

- **decision**: 每个并发单元的写域是可写文件路径集；以目录名（`skills/internal`、`shared/`）为写域的单元判红；只读单元声明空写域（FR-012）。
- **antithesis**: 允许目录级区域（`skills/internal/` 表示整个目录随便写），由调度器在派发前做目录重叠判定；当一个包要写几十个文件、逐文件枚举声明成本过高时它更优——声明便宜，调度器只需一次前缀比较。
- **binding_constraints**:
  - pole_a: 目录级声明会把「同目录下不同文件」误判成相交，从而在可并发的场景上强制串行——这正是本特性要消灭的默认串行。
  - pole_b: 文件级声明要求每个单元在计划期就知道自己要写哪些文件；计划期不知道时只能保守缩小范围。
- **discriminating_evidence**: 构造两个包分别写 `skills/internal/create-plan/SKILL.md` 与 `skills/internal/create-team/SKILL.md`：结果二值——目录级判据报相交、文件级判据报不相交且实际运行零冲突（判绿）/ 两者给出同一结论（则文件级没有信息增益，应改写本条）。
- **expected_sacrifice**: SC-004 Source ↓ 每个 write 包的 `owned_paths` 必须逐文件列出，`wp-gate.py` 的 `WG-15` 相交判定改为文件级，因此 070 夹具里凡以目录名声明写域的包都需逐条改写（改写清单进 070 处置表，处置口径见 feature-ref.md § Overlap adjudication）。
- **revision_trigger**: 实现期出现「两个包分别声明同目录下不同文件、运行时仍互相踩踏」≥1 次 → 重开，说明冲突源不在路径声明，需退回目录级并另找隔离手段。
- **tension_id**: T-003

### T-004 — 「协调者是否可派发」不自裁，登记为 [[STR-011]] 的 owner 条目并阻塞于其裁定

- **decision**: 本特性只要求「单一裁定处存在且可读」，裁定面登记为 `shared/declarations/facts/coordinator-dispatch-verdict.yaml`；FR-021 三条满足任一即通过，裁定为 `forbid` 时派发责任归驱动者/主代理、为 `allow` 时协调者能力集须增派发工具；本特性 MUST NOT 预设裁定结果。
- **antithesis**: 在 plan 里直接裁定「协调者可派发」并把派发工具加进 13 个协调者/执行者的 `capability-tools`；当框架已经决定让协调者自行派发、且交付不必等待任何外部裁定时它更优——一次改完，FR-021 立即可判绿。
- **binding_constraints**:
  - pole_a: F-093-003 记录的是两读都相容的矛盾（正文禁令与静态能力一致，与 092 的 6 包声明矛盾）；plan 自行选一极等于发明工件未记录的意图。
  - pole_b: FR-021 的可判定性依赖裁定存在；把裁定无限期推迟会让 SC-005 无法收口。
- **discriminating_evidence**: 对 `declaration_reader.py --action get --fact coordinator-dispatch-verdict` 在登记前后各执行一次：结果二值——登记后返回属于封闭集 `{allow, forbid}` 的裁定（判绿）/ 仍以退出码 1 报 `no declaration for fact`（判红，即 SC-009 的未登记形态）。
- **expected_sacrifice**: SC-005 Source ↓ 静态侧断言在裁定落地前只能判「未登记」，该判据因此分成两半：反例夹具（092 形态）可先判红，静态侧断言需裁定后闭合。
- **revision_trigger**: 若裁定所有者给出的裁定与 `agents/**` 的 `capability-tools` 现状冲突且无法在同一变更内同时修正 → 重开，把该裁定降级为「本特性的实现期行动项」并在 tasks 阶段登记为具名阻塞。
- **tension_id**: T-004

### T-005 — 五个判定面用既有声明层承载，不新建并发专用清单

- **decision**: 并发类别、串行理由码、槽位与保留位、单元划分规则标识、枚举根映射五者各落一条 `fact`，经 `declaration_reader.py` 读取；不新增清单文件、不新增类别表（FR-002、FR-031、SC-009）。
- **antithesis**: 新建一份人读的 `concurrency-contract` 正文并内嵌表格作为唯一 owner，由各引擎用正则读取；当读者主要是人、且五个面需要大量散文解释相互关系时它更优——可读性最好，也不必理解 `fact_kinds` 五值的约束。
- **binding_constraints**:
  - pole_a: FR-002 要求判定面经既有声明入口消费，MUST NOT 新增第二份清单；`shared/declarations/` 已经是机器可读值的唯一定义点。
  - pole_b: `facts/` 的 `kind` 只有五值，把一段散文塞进 `statement` 会挤掉真正的机器读值；解释性正文必须留在 owner 文档里。
- **discriminating_evidence**: 对八个 slug 各执行 `declaration_reader.py --action get --fact <slug>`：结果二值——全部返回结构化 body 且退出 0、并从 `--action list` 的 `facts` 数组中可见（判绿）/ 任一以退出 1 报 `no declaration for fact`（判红）。
- **expected_sacrifice**: SC-009 Source ↓ 每条 fact 的 `statement` 必须压成纯值，全部解释性文字转由 owner 文档承担，于是「为什么」与「是什么」被分到两个文件，读者需要各开一次。
- **revision_trigger**: 若某条 fact 的 `statement` 实现期需要写成超过约 60 行的嵌套映射才能表达（例如串行理由码的依据形态需要逐码内嵌 schema）→ 重开，把该面拆成「值」与「校验 schema」两条 fact，而不是放弃声明层。
- **tension_id**: T-005

## Project Structure

### Documentation (this spec)

```text
.specify/specs/093-concurrency-by-default/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — measured baseline + rulings
├── data-model.md        # Phase 1 output — entities, validation rules, state transitions
├── quickstart.md        # Phase 1 output — executed and routed scenarios
├── contracts/           # Phase 1 output — six contract files
│   ├── declaration-facts.contract.md
│   ├── judgement-engine.contract.md
│   ├── executor-obligations.contract.md
│   ├── high-order-executors.contract.md
│   ├── existing-semantics-disposal.contract.md
│   └── concurrency-contracts.md        # clause index and clause count
├── feature-ref.md       # Phase 1 output — binding, delivery surface, overlap adjudication
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
shared/declarations/facts/                   # new fact entries (the only new machine-read values)
├── concurrency-class.yaml                   # [[STR-001]] class table + [[STR-002]] semantic name + FR-004 rule
├── serial-reason.yaml                       # [[STR-003]] closed codes, condition-bound vs factual groups
├── effective-concurrency.yaml               # [[STR-005]] reading schema + interval-overlap rule
├── concurrency-slot-and-reserve.yaml        # FR-014/FR-015/FR-020 slot cap, ceiling projection, verifier reserve
├── decomposition-coverage.yaml              # [[STR-007]] per-stage coverage + relation to the three spine keys
├── executor-enumeration-roots.yaml          # [[STR-008]] five enumeration roots -> declaration class
├── concurrency-contract.yaml                # [[STR-006]] landing discipline + FR-033 disposal surface
└── coordinator-dispatch-verdict.yaml        # [[STR-011]] the single coordinator-dispatch adjudication (T-004)
scripts/python/concurrency-check.py           # new: the only program that turns the facts into verdicts
shared/definitions/subagent-definitions.md    # [[STR-004]] dispatch capability (new section)
shared/definitions/goal-definitions.md        # FR-026 goal/target concurrency (rewritten)
skills/external/sdd-loop-driver/references/decomposition-model.md   # slot owner projection, coverage, integration order
skills/external/sdd-loop-driver/templates/stage-team-preset.md      # slot cap projection, seat territory judgement
skills/external/sdd-loop-driver/SKILL.md                            # the driver loop's concurrency obligation
skills/external/sdd-loop-driver/scripts/wp-gate.py                  # ceiling owner (WG-16) + file-level write domain
skills/internal/create-team/SKILL.md                                # team seat binding-time judgement
skills/internal/create-team/references/conceptual-model.md          # team/seat territory owner
skills/internal/run-agent/SKILL.md                                  # dispatch-capability preflight + routing (FR-024)
skills/internal/run-team/SKILL.md                                   # team executor default-concurrent
skills/internal/create-plan/SKILL.md                                # plan-stage default-concurrent (this pipeline)
agents/*.agent.md (17 files)                                        # dispatch capability judged; verdict applied
templates/commands/*.md (the command surfaces this feature judges)  # each command's concurrency obligation
templates/plan-template.md                                          # records a stage's concurrency plan
tests/contract/test_concurrency_class_table.py                      # FR-001…FR-004, SC-001
tests/contract/test_concurrency_serial_reason.py                    # FR-005…FR-009, SC-002, SC-003
tests/contract/test_concurrency_units.py                            # FR-010…FR-020, SC-004
tests/contract/test_concurrency_dispatch_capability.py              # FR-021…FR-025, SC-005, SC-011
tests/contract/test_concurrency_high_order.py                       # FR-026…FR-029, SC-007, SC-008
tests/contract/test_concurrency_declarations.py                     # FR-002, FR-031, SC-009
tests/contract/test_concurrency_disposal.py                         # FR-033, SC-010
tests/contract/test_concurrency_reproduction_092.py                 # SC-005 red-first reproduction fixture
tests/contract/test_concurrency_real_run_evidence.py                # FR-030, SC-006, SC-012
tests/unit/test_concurrency_check_engine.py                         # the engine's own actions
```

**Structure Decision**: this feature extends the existing declaration-layer + engine + contract-test shape the
repository already uses (092 delivered facts and one engine the same way). It adds **no** new top-level directory
and no new directory kind; the only new file kinds are `shared/declarations/facts/*.yaml` entries (an established
kind) and one Python engine under the established `scripts/python/` root. What this adds for a reader: "which
class is this executor in, and what does that class owe?" becomes a machine-checkable question answered by one
engine, instead of eleven documents that must agree by luck.

### Mirror Obligations

Baseline measured **before** any edit of this spec: `python3 scripts/python/sync-mirrors.py --check` → exit `0`,
no drift on any pair (`test-evidence/mirror-baseline-plan.txt`: `templates/` 22 files, `skills/external/` 417,
`skills/internal/` 139, `agents/` 17, `scripts/` 121, `shared/` 98, all byte-identical; five projected pairs `ok`;
per-tool command copies ok). The Verify column is therefore "no NEW drift", judged against this measured baseline.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/**` | `.specify/shared/**` (98 files) | `sync-mirrors.py --check` — no NEW drift vs `test-evidence/mirror-baseline-plan.txt` |
| `scripts/python/concurrency-check.py` and every `scripts/**` touched | `.specify/scripts/**` (121 files) | same run; the engine prints the pair it compared |
| `skills/external/sdd-loop-driver/**` | `.specify/skills/sdd-loop-driver/**` plus the flat `.specify/skills/<name>/**` layer (417 files) | same run |
| `skills/internal/**` | `.specify/skills/internal/**` (139 files) | same run |
| `agents/*.agent.md` | `.specify/agents/templates/*.agent.md` (17 files) | same run |
| `templates/commands/<stem>.md` | `.claude/commands/speckit.<stem>.md`; `.qoder/commands/speckit.<stem>.md`; per-tool copies via `regen-command-copies.py`; NO `.specify/templates/commands/` mirror (retired) | copies regenerated; `sync-mirrors.py --check` reports the per-tool line ok |
| `templates/plan-template.md` | `.specify/templates/plan-template.md` | same run |

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule:
`shared/workflow/acceptance-hardening.md` § Execution Premises — this table carries the column set and the measured
values only.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | CPython `>=3.8` delivers everything the engine needs (filesystem enumeration, YAML-subset parsing through the shared reader, JSON verdicts) with zero new third-party dependency. | `pyproject.toml` `requires-python`; `declaration_reader.py` is standard-library only and already parses the five-`kind` subset. | verified | — |
| EP-002 | `pytest` contract/integration/serial markers exist and the suite is runnable on the declared lower bound. | `pyproject.toml` marker registration; `scripts/bash/run-tests.sh`; `tests/contract/` holds 299 modules on this tree. | verified | — |
| EP-003 | `declaration_reader.py` is the single read entry and its registration behaviour is what SC-009 must judge: `--action list` returns the nine `contract.yaml` keys plus the `facts/` slugs (23 entries measured); `--action get --fact concurrency-class` exits `1` with `no declaration for fact`. | Measured 2026-11-09 on this tree: `--action list --repo .` → `contract` 9 keys + `facts` 23 entries; `--action get --fact success-criterion-path-values` → exit 0 with body; `--action get --fact concurrency-class` → exit 1. | verified | — |
| EP-004 | `wp-gate.py` is the existing Work-Package gate and the natural owner of the slot-cap ceiling; `--slot-cap-ceiling` defaults to `4` and `WG-16` enforces `1 <= slot_cap <= ceiling`. | `skills/external/sdd-loop-driver/scripts/wp-gate.py`: `parser.add_argument("--slot-cap-ceiling", type=int, default=4)`; `decomposition-model.md` § 12 lists WG-16. | verified | — |
| EP-005 | The host's parallel dispatch capability is a runtime fact and cannot be frozen into a file; a probe result drives FR-005(d). | `shared/definitions/subagent-definitions.md` § Three Execution Modes and § Mode Selection (native / virtual / external; parallelism is runtime-dependent). | verified | — |
| EP-006 | The 17 agent definitions carry `capability-tools: [Read, Grep, Glob, Bash]` (9), `[…, Write, Edit]` (7) or `[Read, Grep, Glob, Write]` (1) — none carries a dispatch tool — while 14 of them carry the sentence "Never dispatch another agent". | Measured 2026-11-09 over `agents/*.md`: 9 / 7 / 1 split; `grep -c "Never dispatch another agent"` → 1 in 14 files, 0 in `reporter`, `skill-verifier`, `structure-adjuster`. | verified | — |
| EP-007 | Team definitions: 12 on disk, 10 carrying a `territory` field; `demo-seat-dispatch` and `requirement-implement-monitor` carry none. | Measured 2026-11-09: `ls .specify/teams` → 12 directories; `grep -l territory .specify/teams/*/team.md` → 10. The spec's Edge Cases already require the undeclared case to be judged red (FR-012). | verified | — |
| EP-008 | The new literals (`concurrency-class`, `serial-reason`, `effective-concurrency`, `decomposition-coverage`, `executor-enumeration-roots`, `dispatch-capability`, `coordinator-dispatch-verdict`) have no existing occupancy outside this spec, so the feature adds obligation on a blank surface rather than rewriting vocabulary. | Measured 2026-11-09: repository-wide grep for the literals excluding `specs/093-*` and `memory/features/093*` returns only one unrelated hit (`specs/085-…/tasks.md` uses the prose words, not the slugs). | verified | — |
| EP-009 | The existing concurrency-adjacent suites will keep running: `test_non_regression_064.py`, `test_non_regression_070.py`, `test_sdd_loop_driver_wp_{model,gate,preset,coordination}.py`, `test_wp_mutation_drills.py`, `test_test_execution_efficiency.py`, `test_agent_dispatch_mechanism.py`, `test_agent_chain_guards.py`. | `ls tests/contract` on this tree; FR-033's disposal table names them. | verified | — |
| EP-010 | This run's own stage concurrency cannot be claimed until the mechanism lands; the correct record is `mechanism-not-yet-landed` ([[STR-010]]), never a serial run presented as concurrent. | Spec FR-033 final sentence and Assumption A4; § Concurrency plan for this run below records the measured shape of this stage. | verified | — |

## Inherited Blockers

Owner of this table's shape, its `Disposition` domain, the `Source row` / `Carrier` / `Carrier slice` grammar and
the carrier's eligibility rule: `shared/workflow/acceptance-hardening.md` § Inherited Blockers.

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:

- `064`: `.specify/memory/features/064.md`, `.specify/specs/064-subagent-concurrency/verification.md`
- `070`: `.specify/memory/features/070.md`, `.specify/specs/070-subagent-task-teams/verification.md`
- `086`: `.specify/memory/features/086.md`, `.specify/specs/086-efficient-test-execution/verification.md`
- `092`: `.specify/memory/features/092.md`, `.specify/specs/092-goal-team-parallel/verification.md`

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | `086:SC-010_status` | inherited | `gate:GATE-093` | this-slice | 086 left SC-010 `partial` with its gap carried by GATE-086; 093 neither closes nor inherits that gap — it only guarantees 086's criterion keeps its owner (FR-033, SC-010). |
| 2 | `092:deferred:plan-parallelism-not-delivered` | resolved | `contracts/executor-obligations.contract.md` | this-slice | FR-021/FR-023 make "declare N packages, run them serially inside one coordinator" a red defect; the 092 shape becomes the reproduction fixture `test_concurrency_reproduction_092.py` (SC-005). The 092 deferral is therefore closed **in this slice** — the `resolved` disposition records that the carrier is inside Feature 093's own contract set, not a later slice. |
| 3 | `064:SC-006_status` | not-applicable | — | — | 064's SC-006 measures line-registry ownership envelopes, not a concurrency default; 093 reuses that mechanism read-only and changes none of its assertions. |
| 4 | `070:SC-006_status` | not-applicable | — | — | 070's SC-006 measures Work-Package gate outcomes; 093 changes the ceiling *owner* (T-001) and the write-domain granularity (T-003), both dispositioned through FR-033 and SC-010 rather than by rewriting 070's criterion. |

## Phase 0: Research Review

Full findings: [research.md](research.md) — 14 sections, each with the measurement it rests on. The five findings
that changed the design in this stage:

1. **Registration is a reader behaviour, not a file's existence** (EP-003). The probe runs before the facts are
   written; SC-009's mutation is "make the slug invisible to `--action list`", not "delete the file".
2. **The ceiling has four restatements today** (`stage-team-preset.md` `min(6, …)`, `wp-gate.py` default 4 with
   `WG-16`, `decomposition-model.md` § 22 `min(effective_concurrency, 24)`, and `min(4, line remaining)`), so
   T-001 is a collapse, not an addition.
3. **No agent definition carries a dispatch tool** and 14 of 17 forbid dispatching in prose (EP-006). The
   coordinator verdict (T-004, [[STR-011]]) decides which reading governs; this plan refuses to pick one.
4. **`capability-tools` is a neutral metadata key with a fixed value domain** already consumed by
   `src/specify_cli/__init__.py` and eight contract modules. Judging that field costs no schema change; adding a
   new key would.
5. **The 092 execution lessons bind this stage's evidence rules**: the `id-contiguous` renumber trap, the
   `overlap-check` worktree relativization trap (F-093-002), the "fresh-context verifier reads `SC-NNN_status=`"
   format, and the "serial `FAILED`-prefixed list is the comparison surface" rule.

## Phase 1: Design Artifacts Summary

Backfilled after the artifacts landed (2026-11-09). Every count below is taken from the file it names, not from
memory.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | 14 sections (R-1…R-14), each with a measured reading |
| Data model | [`data-model.md`](data-model.md) | 11 entities (E-1…E-11), 26 validation rules (V-1…V-26), 5 state machines (SM-1…SM-5) |
| Contracts | [`contracts/`](contracts/) | 6 files: `declaration-facts.contract.md` (C-001…C-018), `judgement-engine.contract.md` (C-019…C-040), `executor-obligations.contract.md` (C-041…C-062), `high-order-executors.contract.md` (C-063…C-078), `existing-semantics-disposal.contract.md` (C-079…C-092), `concurrency-contracts.md` (index only, no clause bodies) |
| Contract clauses | `contracts/*.contract.md` | 92 clauses (C-001…C-092), counted by `grep -c '^- \*\*C-[0-9][0-9][0-9]\*\*'` over the five clause-bearing files — the pattern matches only a clause definition line anchored at column 0 |
| Quickstart | [`quickstart.md`](quickstart.md) | 7 scenarios (S-0…S-6): S-0 executed against the live tree; S-1…S-6 are **not executable yet** (the engine and facts land at implement) and each names the clause that pins it and the premises it assumes |
| Feature ref | [`feature-ref.md`](feature-ref.md) | 33 FR map rows, 12 SC map rows, one delivery-surface table, and the 064/070/086/092 overlap adjudication (F-093-001) |
| Execution premises | this file | 10 rows, all `verified` |
| Gates run at this stage | [`test-evidence/`](test-evidence/) | `pre-analyze-check --stage plan` pass (0 error / 44 missing-path advisories, every one a path this feature creates), `validate-decision-tensions` pass (5 records), `decomposition-check --mode plan` proceed (33 FR), `overlap-check` reading retained with the file-level adjudication above |

Drift from the Phase 0 expectation: the expectation was "five facts, one engine, about ten contract files"; the
actual is eight fact entries (the extra three are `concurrency-slot-and-reserve.yaml`, `concurrency-contract.yaml`
and `coordinator-dispatch-verdict.yaml` — FR-014's slot owner, FR-031's landing discipline, and T-004's refused
self-adjudication) and 92 clauses against an expected ~70; the extra clauses are the per-stage obligations of
FR-028 (three loop executors with three advancing grains) and the FR-033 disposal table, both of which are
assertion surfaces rather than prose.

## Concurrency plan for this run (this stage and the next)

This feature's own stage must not repeat the defect it fixes. Measured facts, recorded rather than asserted:

- **Partition ready**: five independent work packages — `P1` declaration facts, `P2` engine, `P3` owners and agent
  definitions, `P4` contracts and tests, `P5` evidence and overlap adjudication — with `P1 → P2` and
  `P1/P2 → P4` as the only dependency edges; five ready at entry under a permissive reading, three after the
  dependency edges are honoured.
- **Execution shape actually used**: **serial, one agent, no sibling dispatch**. The executing agent's tool set is
  `Read, Grep, Glob, Bash, Write, Edit` — it has no Agent/Task tool, so it cannot dispatch siblings. This is
  precisely the F-093-003 / 092 defect. The honest record is `mechanism-not-yet-landed` ([[STR-010]]),
  `effective_concurrency = 1`, and **no claim of concurrency**.
- **What that costs**: SC-006's real-run evidence is deferred to a later run and written as `not_evaluated` here.
  Spec Assumption A4 permits exactly this and forbids substituting fixture data; FR-030/F-093-003 forbid calling
  the serial run a concurrent one.

## Complexity Tracking

N/A — no Constitution Check violation exists (no Fail, no Partial row), so no justification row is required and
none is invented.

## Risks and Mitigations

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|-----------|
| R-1 | The fact entries restate values that existing owners already hold and drift on the next edit. | Medium | High | T-001 and FR-033: every existing restatement becomes a projection in the same change; `test_concurrency_declarations.py` asserts there is no second assignable value per face. |
| R-2 | "Every enumerated executor maps to exactly one class" turns red for executors nobody has classified. | High | Medium | The class table's decision rule is mechanical (layer plus produced shape); an unsatisfiable input reports `uncovered` and goes red by design — that is SC-001's requirement, and the red list is P3's task list. |
| R-3 | The 092 reproduction fixture cannot go green because the host still has no dispatch tool. | Medium | High | The fixture asserts the *static* side (declaration without capability and without handoff ⇒ red) and the *record* side (all units by one executor with no overlap ⇒ inconsistency); neither needs a live dispatch. |
| R-4 | `concurrency-check.py` becomes a fifth gate engine whose exit taxonomy drifts from `wp-gate.py`. | Medium | Medium | C-019 reuses the 0/1/2 taxonomy and the script interface contract; the engine is read-only except `--json-out` and never writes the spine. |
| R-5 | SC-006's real-run evidence cannot be produced inside this feature's implement stage. | High | Medium | Declared `not_evaluated` with the carrier named (A4); stated in § Concurrency plan rather than filled with fixtures. |
| R-6 | Downstream projects inherit facts their `shared/declarations/` cannot read. | Low | Medium | Facts use only the allowed YAML subset (`contract.yaml` `yaml_subset: block-subset/v1`); `declaration_reader.py` is the same file downstream receives. |

## Document Structure

Not produced, by decision: the line is `execution` class (`flow-class-check.py --action lookup --unit-id
"spec:093-concurrency-by-default"` → `flow_class: execution`, `source: declaration`), and
`shared/workflow/expression-gates.md` § 阶段算子表 requires the `## Document Structure` chapter only for an
expression-class line. The heading above is kept as a one-line record so a later reader can see the omission was
decided rather than forgotten; `doc-consistency-check.py --action structure` reports `not-applicable` here.

## Fact Owners

| 事实 | owner 路径 | 章节锚 |
|------|------------|--------|
| 并发类别表成员集、语义名与判定规则 | `shared/declarations/facts/concurrency-class.yaml` | `statement` |
| 串行理由码封闭词表、条件绑定分组与声明次序 | `shared/declarations/facts/serial-reason.yaml` | `statement` |
| 生效并发度的读数 schema 与区间重叠判据 | `shared/declarations/facts/effective-concurrency.yaml` | `statement` |
| 槽位上限取值与校验者保留位 | `shared/declarations/facts/concurrency-slot-and-reserve.yaml` | `statement` |
| 槽位上限的天花板与 `1 <= slot_cap <= ceiling` | `skills/external/sdd-loop-driver/scripts/wp-gate.py` | `WG-16` |
| 阶段拆解覆盖与状态脊三键的关系 | `shared/declarations/facts/decomposition-coverage.yaml` | `statement` |
| 五个枚举根到执行体声明类别的映射 | `shared/declarations/facts/executor-enumeration-roots.yaml` | `statement` |
| 并发契约的落点纪律与既有语义处置面 | `shared/declarations/facts/concurrency-contract.yaml` | `statement` |
| 协调者可派发的单一裁定 | `shared/declarations/facts/coordinator-dispatch-verdict.yaml` | `statement` |
| 派发能力的定义与三种执行模式 | `shared/definitions/subagent-definitions.md` | `## Three Execution Modes` |
| 反嵌套许可链深度 2 | `shared/definitions/subagent-definitions.md` | `## Dispatch-Time Governance Obligation` |
| goal 与 target 的概念及目标持久化位置 | `shared/definitions/goal-definitions.md` | `## Target Decomposition (目标切片)` |
| Work Package 记录形态、集成顺序、重入与重试 | `skills/external/sdd-loop-driver/references/decomposition-model.md` | `## 2. ID assignment, layers, and tie-break (WP-04)` |
| 席位的写领地与团队概念 | `skills/internal/create-team/references/conceptual-model.md` | `## Collaboration patterns (the dynamic structure)` |
