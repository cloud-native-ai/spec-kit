# Implementation Plan: Re-Anchoring（不忘初心 · 温故而知新）

**Branch**: `master` | **Date**: 2026-11-09 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `090-re-anchoring` → Feature 090 Re-Anchoring（不忘初心 · 温故而知新）
**Input**: Specification from `.specify/specs/090-re-anchoring/requirements.md` (10 FR / 4 SC / 2 runtime rows, clarify settled 2026-11-09)

## Summary

Feature 090 turns "load the rules once at session start" into "re-load and re-confirm the rules after every core step":

```text
entry        -> 方向锚 = 任务锚 (goal) + 规则锚 (rules in force), persisted (spine / brief)
core step    -> compact -> reload (T0/T1/T2) -> evaluate (five questions, RULES first)
verdict      -> on-track | correction-applied | decision-needed   (only the last is surfaced)
```

The review's primary object is the **rules**: the current and next action already carry the goal, while a dropped
rule (the canonical failure: `unattended`) leaves no trace in them. The landed tree is a *reviewing habit*, not machinery:
one owner page (`shared/definitions/re-anchoring-definitions.md`), one constitution principle on each surface
(template `XXI`, live `XXII`), one ambient section on each instruction surface, one agent obligation
(`agent-definitions.md`), one entry in the constitution generator's mandate list, and one rewritten rule-first
`§ Direction audit` inside the existing checkpoint protocol. Four contract tests guard those faces plus the
governance count pins.

**Nothing here is newly designed.** The implementation was pre-landed (commits `5a1041e4`, `55776937`, replayed and
reconciled as `137adb7f`, then merged `e2119d1d` / `05b109b7` / `9af8418e`). This plan's job is to *describe and
anchor the tree that exists*, measure it, and hand `/speckit.tasks` a work list whose deliverables are the still-missing
guards and the closure evidence — not a re-implementation.

## Technical Context

**Language/Version**: Markdown for every rule surface (owner page, both constitutions, both instruction surfaces, agent
definitions, checkpoint protocol, generator mandate); Python `>=3.8` for the four contract guards and the stage gates
(`pyproject.toml:5`; measured interpreter CPython 3.11.0rc1).
**Primary Dependencies**: none new — zero third-party imports added by this feature. The guards consume `pytest`
(measured `9.0.3`) and the stage gates consume the stdlib only.
**Storage**: none. The discipline's carriers are the *existing* state spine (`.specify/state/<line>.md`), the checkpoint
files under `.specify/specs/<key>/checkpoints/`, the subagent assignment brief and the fast-fail channel. No new store,
ledger, scorer, scheduler or second checkpoint system (FR-001 / constitution XXII last bullet).
**Testing**: pytest contract guards — `tests/contract/test_reanchoring_contract.py` (five faces, pointers),
`tests/contract/test_sdd_loop_driver_reanchor.py` (checkpoint part 5, tiers, three-valued verdict, no-full-reload
ban), plus the pre-existing counting guards `test_constitution_double_landing.py` (watchlist + three count pins) and
`test_fast_fail_discipline.py` (watchlist length, version pins).
**Target Platform**: any host that loads the framework — the surfaces are plain Markdown shipped by `specify init`;
the guards run on Linux/macOS with CPython.
**Project Type**: SDD framework (shared definitions + `templates/` + `skills/` + `tests/`), self-hosting repository.
**Performance Goals**: no runtime performance surface. The measurable cost target is **bounded reload**: T0 ≈1 KB per
core step, T1 ≈5 KB at stage boundaries, T2 only on ambiguity/stall — a full reload after every tool call is
forbidden (FR-006), so the discipline cannot degrade into ceremony.
**Constraints**: zero new `/speckit.*` command; zero new engine action, service or gate; zero new runtime dependency;
MUST NOT restate the owner page's criteria in any consumer (pointer only); the reload MUST NOT become an approval
request (FR-007).
**Scale/Scope**: 10 FR / 4 SC / 5 rule faces + 1 protocol face + 4 guard tests; 2 mirrors pairs (`shared` → `.specify/shared`,
`templates` → `.specify/templates`) plus two `skills/` pairs.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Rendered by enumerating every `### <numeral>. <name>` heading of `.specify/memory/constitution.md` (v1.19.0) in file
order; the `(NON-NEGOTIABLE)` annotation is carried verbatim where the principle block holds it (principle VII alone).

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | The pre-landed tree is now specified by `requirements.md` (10 FR / 4 SC) and planned here; every design row below cites FR/SC. |
| II | Feature-Centric Development | ✅ Pass | Feature 090 registered in `.specify/memory/features.md` (:98) and `.specify/memory/features/090.md`; this plan advances `Draft → Planned` and adds no new feature row. |
| III | Intent-Driven Development | ✅ Pass | The user's correction ("review the RULES, not the goal") is the load-bearing decision and is recorded verbatim in `requirements.md` § Input and as `T-001` below. |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | Four contract guards already exist and pass on the landed faces; **SC-002's rule-first *ordering* assertion is missing** (clarify C-4). The red-first obligation for that one gap is carried as task work, not discharged here. |
| V | AI Agent Integration Standards | ✅ Pass | No host-specific field is hand-written; `agent-definitions.md` is the neutral template the renderer consumes, and this feature adds one Markdown section to it. |
| VI | Continuous Quality & Observability | ✅ Pass | The verdict is recorded in the checkpoint (`§ 5 Direction audit`), not only in conversation; no fabricated metric is introduced. |
| VII | Specification-Plan-Task-Implementation Workflow (NON-NEGOTIABLE) | ✅ Pass | requirements → clarify (settled, U4 pass) → this plan; feature status advances to `Planned` only, never `Implemented`. |
| VIII | Code as the Single Source of Truth | ✅ Pass | Every claim in § Design Decisions was measured against the tree today (paths, counts, `diff -q` mirror pairs, test runs), not inferred from commit messages. |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Zero new command / engine / gate / store; the change is one owner page, one principle, one ambient section, one obligation, one mandate entry, one protocol section. |
| X | Documentation Naming & Location Conventions | ✅ Pass | `re-anchoring-definitions.md` follows the existing `shared/definitions/<topic>-definitions.md` shape; no new directory is created. |
| XI | Dogfooding (Self-Application) | ✅ Pass | Framework-source edits (`shared/`, `templates/`, `skills/`) are projected into `.specify/` by the mirror machinery; § Mirror Obligations forbids hand-editing either copy. |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses `sync-mirrors.py`, `regen-command-copies.py`, `workspace-guard.py`, the four existing guards and the stage gates; no second engine for the same predicate. |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Targets Controlled Execution (rules re-confirmed at core steps) and Reliable Delivery (drift escalation is a *statement* recorded in the checkpoint). |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Owner page owns concepts/tiers/agent obligation; the checkpoint protocol owns the executable five questions; every other surface is a pointer (measured: six pointer sites, zero restated tables). |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | `quickstart.md` defines `方向锚` / `T0/T1/T2` / the three verdicts at first use and names the evidence path for each scenario. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | The discipline is *adjacent* to fast-fail and boundary-delegates to it; two real anomaly classes (C-4 ordering gap, the pre-existing red set) are surfaced in § Design Decisions F-1 and EP-003, not patched. |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory; evidence lands in the already-sanctioned `test-evidence/` under this spec. |
| XVIII | Grounded Naming | ✅ Pass | `Re-Anchoring` / `不忘初心` / `温故而知新` are the user's own words; `T0/T1/T2` and the verdicts follow the checkpoint protocol's existing `<n>. <part>` vocabulary. |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | The user-visible surface is the checkpoint, whose part 5 already exists; this plan adds no new user-facing dimension — § Document Structure is therefore omitted (execution class). |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | The guards are pure file reads (~0.2 s for the four modules); no new serial/parallel decision is introduced. |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | This feature adds **no** script; the four guards are pytest modules, which the rule's owner places outside the *required* set. |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | This plan *is* the discipline's subject: § Execution Premises carries its premises, and the stage's own U4 runs the checkpoint's part 5. |

**Gates Status**: ⚠ One Partial row (IV) with a matching Complexity Tracking entry. No ❌ Fail.

**Re-check after Phase 1** (2026-11-09, after `data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md`
landed): the table above was re-read against the Phase 1 artifacts — no row moved. Principle IV stays ⚠ Partial for
the same single reason (SC-002's ordering guard is a *task*, and a plan cannot claim a guard it did not land); the
entry in Complexity Tracking was left in place.

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold:
`.specify/shared/guidelines/decision-tension.md` — read from the repository root. This section lists the field names
and points at that file; it does not restate the criteria table, the rejection list or the threshold table.*

### T-001 — 复习的对象是规则，而不是目标

- **decision**: 方向锚固化「任务锚 + 规则锚」两部分，五问的第一问是「本步受哪些规则约束、是否仍生效」；目标不单独追问，因为它由当前与下一步隐含。
- **antithesis**: 把「回顾目标」作为周期审计的主问题（每核心步骤先复述用户目标、再对照偏差）；当一个 agent 的主要漂移形态是**目标被悄悄替换**（例：把「实现 X」做成「调研 X」）而操作规则始终忠实执行时它更优——审计直接命中被丢弃的那一项。
- **binding_constraints**:
  - pole_a: 审计 MUST 命中最常被丢弃的一类事实；本项目实测的丢弃项是规则（`无人值守` 被忽略：包边界开始征求「继续」、状态脊停在包 1，而工作本身一步步正常推进，目标从未丢失）。
  - pole_b: 审计 MUST 低成本可重复（T0 ≈1 KB，每核心步骤一次）；把目标与规则都逐条复述会把成本翻倍，并让锚淹没在噪声里（FR-006 禁止的正是这种仪式）。
- **discriminating_evidence**: 在一份长会话记录上标记「下一次动作已经隐含、从而无需复述」的审计项与「下一次动作不隐含、一旦丢弃就不可见」的审计项，数两类各自命中过的真实漂移次数；结果二值——规则类命中数严格大于目标类（是／否）。为「是」时规则优先成立；为「否」时两问需并列。
- **expected_sacrifice**: SC-002 Source ↓ 「目标被整体替换」这一类漂移不再有专门的问题去拦截，只剩 Q3「下一步是否仍是计划命名的那一步」这一间接信号承担。
- **revision_trigger**: 两个迭代内出现 ≥2 次「审计三值全为 `on-track`，但事后发现目标已被替换、而所有规则都在执行」→ 重开，在五问前增加一条目标问，并按 T-001 与 FR-006 的成本上限重新定 T0 预算。

### T-002 — 审计挂在既有 checkpoint 协议的第 5 部分，而不是独立的审计机制

- **decision**: 方向审计作为 `checkpoint-protocol.md` § The five parts 的第 5 部分落地，复用检查点文件、状态脊与 fast-fail 通道作为唯一载体。
- **antithesis**: 新建一个独立的方向审计记录（自有文件形态、自有触发点、自有台账，可被单独查询与统计）；当需要跨线统计漂移率、或需要在检查点之外按任意节奏触发审计时它更优——审计数据成为一等观测面。
- **binding_constraints**:
  - pole_a: 本纪律 MUST NOT 引入新的评分系统、日志服务或调度器（FR-001 / 宪法 XXII 末条）：多一个机制就多一处会与检查点漂移的第二定义点。
  - pole_b: 审计 MUST 在每个阶段边界都真正发生（SC-004 要求分层在 owner 与协议两侧一致且可被守卫）；「可以不做」的可选附加物在长会话里必然退化为不做。
- **discriminating_evidence**: 在临时副本中删除协议第 5 部分，跑现有契约测试群；结果二值——有测试转红（是／否）。为「是」说明既有机制已足以承载审计的强制力；为「否」说明需要一个独立机制来提供守卫点。
- **expected_sacrifice**: SC-004 Source ↓ 漂移只能按检查点粒度聚合（一个检查点一条判定），无法给出「每 N 步的漂移曲线」这类细粒度统计。
- **revision_trigger**: 两个迭代内出现 ≥2 次「需要跨线横向比较漂移频率，但检查点粒度不足以回答」→ 重开，评估在既有 checkpoints 目录下新增一个只读聚合视图（MUST NOT 新增写路径或第二套记录形态）。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/090-re-anchoring/
├── plan.md              # this file
├── requirements.md      # input (10 FR / 4 SC / clarify settled)
├── research.md          # Phase 0 — why the tree is measured, not re-derived
├── data-model.md        # Phase 1 — the six governed entities and their validation rules
├── contracts/           # Phase 1 — four contract pages (faces, checkpoint, governance, guards)
├── quickstart.md        # Phase 1 — seven executable scenarios
├── feature-ref.md       # Phase 1 — Feature 090 binding, delivery surface, FR/SC map
├── checkpoints/         # driver records (01-clarify.md landed; the plan checkpoint follows U4)
├── test-evidence/       # measurements (baseline suite, gate readings, workspace snapshots)
├── tasks.md             # /speckit.tasks output — NOT created here
└── verification.md      # /speckit.implement output — NOT created here
```

### Source Code (repository root)

Every row below is an **existing** file this feature owns or edits; the tree was measured on 2026-11-09, not planned
from scratch.

```text
shared/definitions/re-anchoring-definitions.md        # NEW owner page (63 lines): two concepts, T0/T1/T2, agent obligation
shared/definitions/agent-definitions.md               # EDIT: `## Re-Anchoring Obligation` section (agent-side duty)
templates/constitution-template.md                    # EDIT: `### XXI. Re-Anchoring (不忘初心 · 温故而知新)`
templates/instructions-template.md                    # EDIT: ambient `## Re-Anchoring (不忘初心 · 温故而知新)` section
skills/internal/manage-constitution/SKILL.md          # EDIT: one more `- **MUST include**` entry (13 -> 14)
skills/external/sdd-loop-driver/references/checkpoint-protocol.md  # EDIT: part 5 rewritten rule-first; minimal shape carries it
skills/external/sdd-loop-driver/SKILL.md              # EDIT: Hard Requirement 14 (direction audit) names the owner
.specify/memory/constitution.md                       # EDIT: `### XXII. Re-Anchoring ...` + Sync Impact Report (v1.19.0)
.specify/instructions.md                              # EDIT: same ambient section (regenerated, never hand-edited)
tests/contract/test_reanchoring_contract.py           # NEW guard: the five faces + pointers
tests/contract/test_sdd_loop_driver_reanchor.py       # NEW guard: checkpoint part 5, tiers, verdict, min-shape
tests/contract/test_constitution_double_landing.py    # EDIT: template 21 / live 22 / mandate 14, watchlist -> 9
tests/contract/test_fast_fail_discipline.py           # EDIT: watchlist length pin + section-count pins
scripts/bash/generate-instructions.sh                 # EDIT: INSTRUCTIONS_BUDGET_BYTES raised for the ambient section
docs/reference/history/                              # unchanged: the incident this feature answers is cited, not rewritten
```

**Structure Decision**: this spec extends the existing SDD framework layout — it creates **no** new top-level
directory and **no** new runtime component. The single new authored file is one page under the existing
`shared/definitions/` topic directory; every other row is an edit to a surface that already existed (principle list,
ambient instruction section, agent template, generator mandate list, checkpoint protocol). Runtime carriers are the
state spine and the checkpoint files, both of which predate this feature.

### Mirror Obligations

Baseline drift was measured **before** defining any Verify cell (`diff -q` over each pair this feature touches,
2026-11-09): all six pairs are currently byte-identical (`AGENT_SAME`, `CONST_TPL_SAME`, `INSTR_TPL_SAME`,
`MANAGE_CONST_SAME`, `CP_SAME`, `DRIVER_SKILL_SAME`). The criterion below is therefore "no NEW drift" on these pairs,
never a bare exit code — unrelated drift elsewhere in the tree must not be attributed to this feature.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/re-anchoring-definitions.md` | `.specify/shared/definitions/re-anchoring-definitions.md` via `sync-mirrors.py` | `diff -q` on the pair — byte-identical, no new drift vs the pre-change baseline above |
| `shared/definitions/agent-definitions.md` | `.specify/shared/definitions/agent-definitions.md` via `sync-mirrors.py` | same |
| `templates/constitution-template.md` | `.specify/templates/constitution-template.md` via `sync-mirrors.py` | same |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md` via `sync-mirrors.py` | same |
| `skills/internal/manage-constitution/SKILL.md` | `.specify/skills/internal/manage-constitution/SKILL.md` via `sync-mirrors.py` | same |
| `skills/external/sdd-loop-driver/**` (`SKILL.md`, `references/checkpoint-protocol.md`) | `.specify/skills/sdd-loop-driver/**` (flat, host-discoverable) via `sync-mirrors.py` | same |
| `.specify/memory/constitution.md` | none — live governance file, single copy | n/a (not a mirror) |
| `.specify/instructions.md` | none — produced by `scripts/bash/generate-instructions.sh` from the template | regenerated content carries the section; the script's `INSTRUCTIONS_BUDGET_BYTES` is the only allowed edit |

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule:
`shared/workflow/acceptance-hardening.md` § Execution Premises — this skeleton carries the column set and nothing
else.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | Python 3.8+ and pytest are available locally; the contract guards run without network, daemon or cluster. | `/usr/bin/python3 --version` → `Python 3.11.0rc1`; `/usr/bin/python3 -m pytest --version` → `pytest 9.0.3`; `pyproject.toml:5` → `requires-python = ">=3.8"`; four guard modules green in 1.92 s (see `test-evidence/`) | verified | — |
| EP-002 | The five rule faces exist and are byte-reachable through the mirror pairs this feature owns, so a guard can assert them by path. | Six `diff -q` pairs identical (2026-11-09); `wc -l shared/definitions/re-anchoring-definitions.md` → 63 | verified | — |
| EP-003 | The repository's pre-existing contract-suite red set is stable enough to serve as a comparison baseline, so "no NEW failure" is decidable for this feature's guards. | `.specify/specs/090-re-anchoring/test-evidence/plan-contract-baseline-raw.txt`: `49 failed, 6368 passed, 2 skipped in 486.38s`; the two `test_fast_fail_discipline.py` failures and the `test_acceptance_premises.py` pin mismatch predate this stage | verified | — |
| EP-004 | A checkpoint can be produced for every stage without a human in the loop: the driver writes the spine and the checkpoint, and the audit's verdict is a statement. | `.specify/specs/090-re-anchoring/checkpoints/01-clarify.md` (landed); `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` § Rules | verified | — |

## Inherited Blockers

Dependency set: none — this feature consumes no dependency artifact.

**Dependency artifacts (declared, never implied)** — none. The rule surfaces this feature touches are framework files
inside this repository, not another feature's deliverables; the incident this feature answers is cited in
`shared/definitions/re-anchoring-definitions.md` § 1.1 rather than inherited from an earlier slice. Feature 089
(`.specify/memory/features/089.md`, `.specify/specs/089-script-interface-contract/verification.md`) is the trunk this
feature was rebased onto, but it carries no unresolved `blocked` / `deferred` / `partial` row that this plan would
need to dispose of, so it is not part of the dependency set.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| IV — Test-First & Contract-Driven Implementation (⚠ Partial) | SC-002 claims the rule-first *ordering* is pinned by a contract test; the landed guards assert that Q1 exists and that the three verdicts exist, but nothing reds if Q1 is reworded to ask the goal first. Compliant evidence cannot be written, because no such guard exists. | Writing "✅ Pass" and letting the existing greens stand is the exact failure mode the feature is built against ("a green check is a claim, not an evidence"); the missing ordering assertion is therefore carried as explicit task work (`feature-ref.md` § 3, `contracts/guard-tests.contract.md` C-7) with a red-first obligation, and this row stays until it lands. |

## Phase 0: Research Review

No standalone `research.md` dependency — the Phase 0 findings are brief and fully resolvable from this repository, so
they are inlined here and elaborated in [research.md](research.md). The research question was not "what should we
design" but "what does the pre-landed tree actually contain, and does it match the settled requirements".

1. **The tree is measured, never re-derived.** Every face was read on 2026-11-09 with a path plus a line anchor:
   owner page (63 lines), template principle `XXI` (`templates/constitution-template.md:389`), live principle `XXII`
   (`.specify/memory/constitution.md:490`), both ambient sections, `agent-definitions.md:104` (`## Re-Anchoring
   Obligation`), `manage-constitution/SKILL.md` mandate entry, and checkpoint protocol § 5 (lines 36–58).
2. **The numeral difference is legitimate, not drift** (clarify A2 / R1). Template holds 21 principles, the live
   constitution 22; the live roster carries 13 project-specific principles the template does not, so the same rule is
   `XXI` in the template and `XXII` live. FR-002 constrains the **title and the pointer**, not the numeral; forcing
   the numerals equal would break each document's own self-consistency.
3. **Six pointer sites, zero restatement** (R2). `grep -rn re-anchoring-definitions.md` over the tree outside the spec
   directory returns the owner page plus six consumers (`manage-constitution/SKILL.md:264`, both constitution
   surfaces, both instruction surfaces, `agent-definitions.md:107`) — each a path reference, none a copied table.
4. **The counting pins moved in the same batch** (R3). `TEMPLATE_COUNT = 21`, `LIVE_COUNT = 22`, `COMMAND_COUNT = 14`
   each carry a `# stale-pin update (2026-11-09, 090)` comment; `DOUBLE_LANDING_WATCHLIST` gained the Re-Anchoring
   title as its 9th entry and `test_x15` pins `len(entries) == 9`. `test_x13` derives its three expected values from
   the artifacts, so the "same batch" claim is recomputable.
5. **The gap is ordering, not presence** (R4 — the clarify C-4 ruling, re-measured). The protocol states "The audit's
   primary object is the RULES, not the goal" (line 43) and prints `- Q1 rules:` in its minimal shape (line 102), but no
   test in `tests/` asserts that ordering. This is the single compliance gap this plan carries.
6. **Delegation was not available** (R5). The same-author detection gate
   (`.specify/shared/workflow/objective-analysis-gate.md`) delegates fresh-context scoring to read-only subagents; this
   run is a stage worker with no dispatch authority, so the Constitution Check reports what it measured and escalates
   the one Partial row here and in Complexity Tracking rather than silently marking it Pass. This is a disclosed
   degraded evidence path, not a clean pass.
7. **The baseline is red before this stage touches anything** (R6). `tests/contract/` measured
   `49 failed, 6368 passed, 2 skipped` on an untouched tree; the failures are spread over 22 modules (25 alone in
   `test_run_tests_runner_contract.py`). Two of them sit in `test_fast_fail_discipline.py`, the module this feature
   edits — so a "the suite is green" acceptance criterion is unpassable and the only honest criterion is **no NEW
   failure against this measured baseline**.

## Inherited design decisions (recorded, not re-decided)

The six rulings below were made before this stage and are carried here so `/speckit.tasks` reads them from one place
rather than re-deriving them from three documents.

| # | Decision | Status | Where it stands |
|---|----------|--------|-----------------|
| D-1 | Owner page under `shared/definitions/`, not a new `shared/guidelines/` entry | decided | `requirements.md` FR-001, `features/090.md`; rationale: it owns *concepts + tiers + obligation*, which is the `definitions/` shape |
| D-2 | Five faces + one protocol section; no new command, engine or gate | decided | FR-002…FR-009, constitution XXII last bullet |
| D-3 | Template numeral `XXI` / live numeral `XXII` — per-surface numbering is legal | decided | clarify A2; `contracts/governance-landing.contract.md` C-3 |
| D-4 | `test_sdd_loop_driver_reanchor.py` is this feature's second guard, not a foreign test | decided | clarify A5; FR-010 amended 2026-11-09 |
| D-5 | SC-002's ordering assertion is a **gap**, handed to tasks with a red-first obligation | open (carried) | clarify C-4; Complexity Tracking row IV; `contracts/guard-tests.contract.md` C-7 |
| D-6 | EP-001 (Python 3.8+ / pytest / no network) is the premise the runtime rows cite | decided | `requirements.md` A3; § Execution Premises EP-001 |

## Phase 1: Design Artifacts Summary

Counts below were backfilled after the artifacts landed on disk (never pre-written).

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | R1–R9, the measurement record behind § Phase 0 |
| Data model | [`data-model.md`](data-model.md) | Re-anchoring slice: 6 entities (E-1…E-6), 12 validation rules (V-1…V-12). Non-Disposable slice: 9 entities (ND-E-1…ND-E-9), the entry state machine, the expiry model, the human-facing output shape, the fact-owner table, 11 validation rules (ND-V-1…ND-V-11) |
| Contracts | [`contracts/`](contracts/) | 12 files, two namespaces. Re-anchoring (4, as recorded when they landed): `re-anchoring-faces.contract.md` (C-1…C-8), `direction-audit.contract.md` (C-1…C-9), `governance-landing.contract.md` (C-1…C-6), `guard-tests.contract.md` (C-1…C-8). Non-Disposable, absorbed from 092 (8, clause ids `ND-C-NNN`): `nd-detection-categories` (ND-C-101…108), `nd-status-and-verification` (ND-C-201…207), `nd-disposition` (ND-C-301…308), `nd-four-stage-command` (ND-C-401…410), `nd-renumber-and-supersede` (ND-C-501…507), `nd-detection-engine-cli` (ND-C-601…608), `nd-report-schema` (ND-C-701…707), `nd-acceptance-readability` (ND-C-801…807) |
| Quickstart | [`quickstart.md`](quickstart.md) | 7 scenarios (S-0…S-6) |
| Feature ref | [`feature-ref.md`](feature-ref.md) | binding, delivery surface, FR→contract map, SC→measurement, disclosed rulings |

**Stage gate readings (run during this stage, evidence in `test-evidence/`)**:

| Command | Reading |
|---------|---------|
| `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/090-re-anchoring/requirements.md` | `{"mode": "plan", "decision": "proceed", "measured": {"fr_count": 10, "task_count": null, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": []}` — proceed, no split required |
| `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/090-re-anchoring --stage plan --repo .` | `stage=plan decision=pass errors=0 advisories=2 waived=0` — both advisories are `missing-path` on `requirements.md:72`, where the file writes the two source roots with a literal `...` ellipsis; the same two tokens quoted in this table add two more advisories of their own (the re-run reads `advisories=4`). Verbatim reading: `test-evidence/pre-analyze-plan.txt` |
| `/usr/bin/python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/090-re-anchoring --json` | `status: error`; five of six labels pass (`dtr-anchor`, `dtr-section-missing`, `dtr-record-incomplete`, `dtr-tension-id`, `dtr-rejected-form` all `pass 0`); `expected-sacrifice-unmapped` fires **2** (at the two `expected_sacrifice` field lines of T-001 and T-002) because `requirements.md` carries no `### Measurement Sources & Collection Methods` section to resolve `SC-002 Source` / `SC-004 Source` — a defect of the requirements artifact, recorded as `research.md` R9 and `feature-ref.md` F-2, not repaired from this stage |
| `/usr/bin/python3 scripts/python/validate-requirements.py .specify/specs/090-re-anchoring/requirements.md` | `status: error`, `path-marker` ×4 (SC-001…SC-004 carry no `**Path**` marker); same territory boundary — `research.md` R9, `feature-ref.md` F-1 |

## Non-Disposable slice (092)

Feature **092-non-disposable** is absorbed into this feature as a **second slice**. It is not a revision of the
re-anchoring discipline: it adds a review mechanism (`回顾 → 设计 → 确认 → 执行`) with its own owner page, its own
read-only engine and its own contract pages. That slice's five-stage artifacts stay where they are — its
`requirements.md`, `research.md`, `quickstart.md`, `feature-ref.md`, `tasks.md` and its `test-evidence/` remain under
`.specify/specs/092-non-disposable/` and are read **in place**, never copied here. What moves is exactly what the table
below names:

| 092 artifact | Where it now lives in 090 | Transformation |
|---|---|---|
| `contracts/*.contract.md` (8 files, 62 clauses — 55 `##` headings plus the 7 `- **C-NNN**` bullets of `acceptance-readability`) | `contracts/nd-<name>.contract.md` | every clause id `C-NNN` → `ND-C-NNN` (62 definitions, 1:1, no id added or dropped); intra-slice cross-references repointed at the `nd-` file names; the header's `**Feature**` line names this feature |
| `data-model.md` entities E-1…E-9 | [`data-model.md`](data-model.md) § Entities `ND-E-1`…`ND-E-9` | entity ids prefixed; the entry state machine, the human-facing output shape and the fact-owner table carried as `ND-`-headed sections; the ND validation rules land as `ND-V-1`…`ND-V-11` |
| `plan.md` summary, technical context, seven decision tensions, package proposal, risk register, corpus mapping, shift list | **this section** | summarised here; the verbatim bodies stay in `092-non-disposable/plan.md` |

**Name collision, resolved by prefix, not by renumbering.** Both slices use `contracts/C-N`. The re-anchoring slice
keeps its bare `C-1`…`C-10` identifiers on the four pages it already shipped (its `test-evidence/` and guard tests
cite them); the absorbed slice takes `ND-C-NNN`. No delivered clause id changes meaning, which is what makes the merge
reviewable by name: a reader who sees `C-` reads re-anchoring, `ND-C-` reads non-disposable.

### What the slice delivers (summary only — one statement per object, the owner's text is elsewhere)

- **Review surface**: exactly ten declared `.specify/` historical roots, held as a `closed-set` fact in
  `shared/declarations/facts/non-disposable-review-surface.yaml` and read through `declaration_reader.py`. A sibling
  directory that is not declared produces a hint, never a candidate.
- **One deterministic engine**: `scripts/python/non-disposable-check.py`, stdlib-only, read-only, exit codes 0/1/2,
  `--json`, `--scope`. It emits eight closed detection classes and a coverage declaration; a `unevaluated` seam is a
  visible non-clean state, never a pass.
- **One owner page**: `shared/definitions/non-disposable-definitions.md` — the disposition set
  (`archive` / `supersede` / `correct` / `exempt`), the exemption form, the detection classes and their subjects, the
  review-surface definition, the supersede protocol, the report schema, the bridge to `sanitize-utils.py`'s
  `DISPOSITIONS`, and the boundary with `.specify/history/`.
- **The four-stage command shape** inside the one existing `/speckit.history` entry
  (`templates/commands/history.md` + `skills/internal/manage-history/SKILL.md`): a zero-write review, a zero-write
  design, an explicit confirmation (`group` / `item` / `none-of`), and an execute segment writing four evidence
  segments per group into `test-evidence/`.
- **Seven landing faces, zero new principle** (the slice's D-2): owner page · declaration fact · four glossary terms ·
  registry row + detail · the existing `pytest -m contract` guards with a mutation leg per closed set · three
  history-surface pointer lines · one `register.md` decision row.

### Decision tensions of the slice

The slice's seven records are **carried verbatim in `092-non-disposable/plan.md` § Decision Tensions** (`T-001`…`T-007`)
and are NOT restated here, for a mechanical reason that is worth stating because it constrains the merge: the
validator that judges tension records (`scripts/python/validate-decision-tensions.py`) requires `T-NNN` identifiers to
be **unique and increasing in document order** inside one `## Decision Tensions` section, and this plan's section
already holds `T-001`/`T-002`. Copying the slice's records into that section would either collide on `T-001`/`T-002`
or force the re-anchoring records to be renumbered — a change to delivered identifiers, which the naming discipline
forbids. The slice's records therefore keep their owner file, and this section carries the **index**, not the bodies:

| Slice tension | Decision (one line) | Reaches this feature as |
|---|---|---|
| `T-001` | The detecting engine is a local read-only script, not a resident review service | no second store, scheduler or daemon — the same shape `T-002` here protects for the anchor |
| `T-002` | No new constitutional principle; the gap stays open as OI-4/OI-5 | the slice lands seven faces instead of a principle — § Seven landing faces above |
| `T-003` | Deterministic vs semantic is decided by the assertion's subject; the seam degrades to `unevaluated` | § ND entry state machine (`unevaluated` is a visible state) |
| `T-004` | The two disposition vocabularies coexist; one mapping table plus one adjudication rule | § ND-E-5 (`DispositionBridge`) |
| `T-005` | The A–H corpus is tiered I/II by **where the repair belongs**, not by defect size | § ND Shift List below |
| `T-006` | The semantic face reuses the 085 spec-local team; no second concurrency facility | the slice's shard contract (`ND-E-6`) |
| `T-007` | An exemption is always time-bounded; there is no permanent exemption | § ND-E-3 (expiry model) |

**Load-bearing tension of the merge itself — `T-ND-001`, prefix versus renumber.** `decision`: the absorbed slice's
clause ids gain a `ND-` prefix and the re-anchoring ids keep their spelling. `antithesis`: renumber the whole set into
one continuous clause sequence (`C-1`…`C-68`), giving a reader one numbering domain and one place to count clauses.
`binding_constraints`: pole_a — the re-anchoring slice's clause ids are cited by delivered guard tests and by every
file in `test-evidence/`, so renumbering them would silently break those citations in the same change that claims to
merge; pole_b — a prefix that is only decorative would leave two `C-101`-shaped ids that a reader cannot tell apart,
so every ND cross-reference inside the absorbed pages had to be repointed at the `nd-` file names in the same edit.
`discriminating_evidence`: `grep -rn 'C-[0-9]' tests/contract/ .specify/specs/090-re-anchoring/test-evidence/`
resolved before and after the merge — a renumbering is admissible only if that command returns the same resolution
count; the prefix is admissible iff the count stays identical because no id moved.
`expected_sacrifice`: **SC-002 Source ↓** — this record is not one the validator parses (it lives outside the
`## Decision Tensions` section, whose two records and their `T-001`/`T-002` ids are untouched), and `SC-002` here means
the Non-Disposable slice's criterion, read against that slice's own `requirements.md`, because both features number
their criteria `SC-NNN` and the slice's set stays where it is. The cost paid: a reader must know two numbering
conventions, and the clause count of the merged feature is a sum (`62` ND clauses beside the re-anchoring pages)
rather than one sequence.
`revision_trigger`: a third absorbed feature, or ≥2 guard tests that must cite both domains in one assertion → reopen,
move to a single continuous numbering with a recorded migration map.

### Verification basis of the slice (carried, not re-derived)

- **A–H corpus**: 35 entries (`notes/input-review-080-090.md`), tiered I (19) / II (15); the per-entry table with the
  tier and the detection class that must reproduce it is the slice's `plan.md` § A–H Corpus Mapping, and it is the
  table a guard reads. Tier I entries reach name-level zero inside the slice; tier II entries reach a shift row.
- **Shift List (档 II handoff)**: 12 rows = 12 receiving bodies = 12 markers, because the mapping is many-to-one
  (`081` carries D1+D2, `083` carries E1+E2+E3+F5, and so on). The rows are owned by the slice's plan; the marker's
  literal form is owned by `contracts/nd-acceptance-readability.contract.md` `ND-C-805`. Two of those rows land on
  **this** feature — `090` carries `D5` (the rule anchor's four spellings) and `F2` (the instructions budget block's
  arithmetic) — so the absorbed slice's own handoff includes this spec's body.
- **Baseline**: the slice's `notes/baseline-failed-tests.txt` is the frozen failed-node-id set its guards compare
  against; a count read at another moment is never evidence against it.

### Boundaries this merge does not move

- **092 is not deleted, and not stubbed.** Its directory stays intact and remains the place a reader finds the slice's
  requirements, research, quickstart, tasks and evidence. Deleting it, or leaving a redirect file behind, is a later
  decision recorded in `.specify/archive/specs/092-non-disposable/notes/refactor-anchoring-merge.md` — not this section's.
- **The 092→090 registry merge is out of scope here.** `.specify/memory/features.md` and `features/092.md` are
  single-owner registries; this section states what the merged feature *contains*, and does not edit a registry.
- **No code lands here.** The engine, the owner page, the declaration and the guards are the slice's own implement
  deliverables; this stage merges artifacts only.
