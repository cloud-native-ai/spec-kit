# Implementation Plan: Background Dispatch Settlement — 后台派发静默退出结算契约（Background Dispatch Settlement）

**Branch**: `106-background-silent-failure` | **Date**: 2026-11-25 | **Spec**: `.specify/specs/106-background-silent-failure/requirements.md`
**Requirement → Feature**: `106-background-silent-failure` → Feature 095 Super Agent Role
**Input**: Specification from `.specify/specs/106-background-silent-failure/requirements.md` (41 FR / 9 SC / 4 Shared Strings; Clarifications Session 2026-11-25: Feature 095 binding, glossary proposal channel, `role-edge-check.py` as the single settlement judgment engine, legacy/refusal split; Runtime Stack RS-001…RS-004)

> **Concurrency obligation (执行义务，按指针抵达)**: this plan authorizes execution bodies. Each one follows the framework's single concurrency obligation — consider concurrency first, default to it when the class and capability allow, and name a reason code plus record the `requested` / `effective` / `effective_reason` reading when serial. The obligation's authored text is `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; its class table is `shared/declarations/facts/concurrency-class.yaml`, its reason codes `shared/declarations/facts/serial-reason.yaml`, and its reading fields `shared/declarations/facts/effective-concurrency.yaml`. This template restates none of their rules.

## Summary

A background dispatch must end in **exactly one settlement value backed by positive evidence**, and both silent success and silent failure must be visible. The contract today has half a sentence: `superagent-definitions.md` § Termination names `completed` / `failed` / `cancelled` and says "silent orphaning is a defect", but it does not name silent termination as an observable state, gives no per-value evidence requirement, and no guard turns it red. This feature closes that gap with **one owner, one judgment engine, additive carrier evidence, and reaction obligations** — no second mechanism:

1. **Single owner** — amend `shared/definitions/superagent-definitions.md` § Termination with the closed settlement value set (`completed` / `failed` / `anomaly` / `cancelled` / `running` / `silent-end` / `unknown`), the positive-evidence requirement per value, the settlement-time liveness rule, the reaction obligations, the contract-version/legacy split, the carrier evidence table, and the extended closed violation set (four edge kinds unchanged + three settlement kinds). `silent-end` and `unknown` semantics are owned there and reached by pointer everywhere else.
2. **Single judgment engine** — extend `scripts/python/role-edge-check.py` additively with a read-only `--action settle` whose exit codes 0/1/2 already carry clean / violation / unreadable-`unknown`. `report` and `query` keep their schema byte-for-byte; no second engine is introduced (A-6; the "existing owner does not cover" ruling is therefore not triggered).
3. **Carrier conformance** — C1 keeps the four-piece and watcher verdicts unchanged and maps its verdicts onto settlement values; C2 gains additive `<label>.attempt` / `<label>.end` records plus pid and a TERM/INT/HUP trap while the `.status` line format stays unchanged; C3 adds the `end_state` + evidence columns to the run-report mapping table, a seat start record (E2 `<label>.attempt`, carrier `c3-team-seat`, or the same label's C1/C2 start evidence) so a seat that dies before its row can still settle, and a settlement-coverage declaration in `## Verification`; C4 leaves a parent-side attempt record and settles on return or declared deadline; C5 virtual is explicitly excluded with the "unfinished never reported completed" duty; C6 recipes are restricted to a compliant runner background form or a foreground-terminal form, and the ambiguous stall wording becomes per-value dispositions.
4. **Enforcement** — new contract tests pin the owner page, the engine's settlement action and violation kinds, every carrier's silent-death fixture plus live/reverse fixtures, the version/legacy split, the preserved watcher token/exit-code/sentinel sets, and a mutation drill records at least one red per removed detection. No behavior-class clause is claimed as contract-covered.
5. **Compatibility** — every new field/file is additive; existing `.status` lines, report formats, sentinel literals, watcher judgments/exit codes/`--self-test`, the five-element uplink, the seven-field downlink, the confirmation-gate budget and the two-slot test budget keep an **empty allowed-delta set**. Legacy records are annotated read-only in audit output and never counted as compliant; unreadable evidence keeps the single deterministic refusal (`unknown`, exit 2).

## Technical Context

**Language/Version**: Markdown (definition/owner page, skills, command templates, reference docs, contracts) + CPython `>=3.8` standard library (engine action and tests) + POSIX bash (`dispatch.sh`). No new third-party dependency.
**Primary Dependencies**: existing, consumed read-only unless named as edited: `scripts/python/role-edge-check.py` (judgment engine — extended additively), `skills/internal/create-team/scripts/dispatch.sh` (C2 carrier — extended additively), `skills/external/sdd-loop-driver/scripts/watch-target.sh` + `stage-runner.sh` (C1 evidence — unchanged), `scripts/python/exec-quant.py` (run-agent dispatch records), `scripts/python/sync-mirrors.py`, `scripts/python/regen-command-copies.py`, `scripts/bash/run-tests.sh` (unique test entry), `scripts/python/scan-confirmation-gates.py` (budget measurement).
**Storage**: no new store, registry, scheduler, queue, daemon or notification channel. Attempt/end/settlement records reuse the existing dispatch artifact directory (`.specify/agents/execution/logs/`, already git-ignored) as one file per attempt; team settlement rides the existing run report and the additive seat start record in that directory; C1 rides the existing four-piece and stage sidecar/spine.
**Testing**: `pytest` through the unique entry `scripts/bash/run-tests.sh` (targeted set `targeted-set-v1`; parallel default; this plan stage is docs-only and records `not-run-docs-only`). New tests are static text/structure pins, deterministic fixture trees under `tests/fixtures/settlement/`, one short-lived live child process for the liveness/reverse fixture (no fixed sleeps; bounded event polling), and read-only engine invocations. The runner resolves pytest only with `SPECKIT_PYTHON=/usr/local/bin/python3` on this host (measured; the repo `.venv` carries no pytest) — the implement stage MUST pass that override.
**Target Platform**: Linux/macOS developer and CI hosts with Python 3.8+ and bash; `/proc`-based zombie/pid-reuse checks are used where available and degrade to `kill -0` elsewhere.
**Project Type**: framework toolkit (owner definition + skill/report contracts + engine action + docs + tests) — no application runtime, no new script.
**Performance Goals**: no steady-state runtime path is added. The `settle` action reads a bounded directory set per invocation; the targeted settlement suite stays in the seconds range (95 % file reads + a handful of subprocess calls).
**Constraints**: zero second mechanism (no new store / scheduler / registry / renderer / channel); owner is `superagent-definitions.md` § Termination; watcher file content is unchanged (sha equality with `fbab7a45c` measured); `.status` line format unchanged; five-element uplink and seven-field downlink unchanged; two-slot test budget unchanged; `scan-confirmation-gates.py` per-file hit set MUST NOT grow on touched files (the frozen `total == 27` equality is a disclosed pre-existing red — see EP-005).
**Scale/Scope**: 1 owner page amendment, 2 shared/owner-adjacent edits, 1 engine extension, 1 carrier script, 5 skill/report text edits, 2 command templates (with per-tool copies regenerated), 4 coordinator templates, 3 docs/reference pages, 6 new test modules + 1 fixture tree, 3 contracts, 9 data-model entities, 1 Feature-detail plan note, 1 glossary proposal.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md` v1.20.0, 23 principle headings in order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every FR-001…FR-041 is carried by one of the three contracts (`settlement-contract`, `carrier-conformance`, `enforcement-and-migration`) or by `data-model.md`; `research.md` R-01…R-08 name the FRs they serve; quickstart scenarios map to US1–US5. |
| II | Feature-Centric Development | ✅ Pass | Bound to parent Feature 095 (its first slice, row 106); this stage advances the **slice** `Draft → Planned` and only adds a plan note to the 095 detail; parent status stays `Ready for Review` (no status regression). |
| III | Intent-Driven Development | ✅ Pass | Requirements A-1…A-18 and the Clarifications session carry the what/why; the design encodes them as the closed value set + evidence matrix (contract C-01/C-02), the three reaction routes (C-09), and the zero-second-mechanism boundary (carrier contract C-24). |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Three contracts carry `C-NN` clauses and each names its pinning test; the implement stage writes those tests red-first (A-14); behavior-class clauses are named in the enforcement contract and never claimed as machine coverage. |
| V | AI Agent Integration Standards | ✅ Pass | No `AGENT_CONFIG` / `_ASSISTANT_TIERS` change; per-tool command copies regenerate through `regen-command-copies.py`, never by hand. |
| VI | Continuous Quality & Observability | ✅ Pass | Baselines were measured, not assumed: mirror `--check` rc 0 (`.venv/bin/python`), self-test 39/0, watcher sha equality with `fbab7a45c`, engine report schema pinned by its existing test. The pre-existing confirmation-gate red (`31 != 27`) is disclosed as EP-005 `falsified`/`fallback`, not skipped or muted. |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Phases run in order; this stage lands plan artifacts only and owns no `Implemented` transition; Inherited Blockers declares `Dependency set: none` with its measured basis; no `[~]` task is invented. |
| VIII | Code as the Single Source of Truth | ✅ Pass | Current state was measured in code: the Termination sentence (`superagent-definitions.md:58`), `dispatch.sh`'s missing trap/pid and end-only `.status`, the engine's `report|query` action set and exit codes, the 5-column mapping table requirement, Recipe 4's ambiguous stall sentence. Docs are corrected toward code. |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Definition + report fields + one engine action + tests; no runtime, scheduler, daemon or transport. The one engine call in tests reuses the existing read-only engine; T-001 and T-002 record why the simpler alternatives were rejected. |
| X | Documentation Naming & Location Conventions | ✅ Pass | Every edited path is an existing lowercase file; no reserved ALL-CAPS name and no new directory is coined (the only new directory is the existing-pattern `tests/fixtures/settlement/`). |
| XI | Dogfooding (Self-Application) | ✅ Pass | Two hats named: all distributing edits land in `shared/`, `skills/`, `templates/`, `scripts/`; `.specify/` mirrors and per-tool copies regenerate through the existing flow. No runtime mirror is hand-edited. |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Every capability reuses an existing engine/script (role-edge-check, dispatch.sh, watch-target.sh, exec-quant, sync-mirrors, regen-command-copies, run-tests, scan-confirmation-gates); no helper script is created. |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Controlled Execution (settlement instead of silence) and Change Validation (red-first carrier fixtures + mutation drill) with no new scoring surface; evidence states are kept honest (`Unobserved` is never read as a defect or an improvement). |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | The settlement set and evidence matrix have exactly one owner (`superagent-definitions.md` § Termination); every other surface — requirements, tests, skills, docs — reaches it by pointer; only test pins duplicate the literals (legitimate duplicate). |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | Reaction and migration wording names the actionable path (`silent-end` / `unknown` are explained once at the owner and referenced); quickstart declares its reader baseline and per-example premises; behavior claims are not dressed as machine coverage. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Falsified premise EP-005 is recorded with a Decision instead of a silent workaround; the engine's unreadable-evidence path is `unknown` (exit 2), never green; the mutation drill obligation (FR-030) exists precisely to prove checks can go red. |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new top-level directory; `tests/fixtures/settlement/` follows the existing `tests/fixtures/<feature>/` pattern; attempt records live in the already-ignored `.specify/agents/execution/logs/`. |
| XVIII | Grounded Naming | ✅ Pass | `silent-end` comes from the spec's new concept (glossary proposed in wrap-up); `settle` / `settlement` follow the requirements' vocabulary; test names follow the `test_<area>_*.py` siblings (`test_settlement_*.py`). |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | The judgment output is per-attempt and names its evidence pointers; the team report's `end_state` column carries the settlement at the place a reader already looks. One information dimension is added (settlement), not several. |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | New test modules are isolated (tmp dirs / committed fixture trees / one short-lived child) and parallel-safe under the runner default; no reduced selection, skip, flake declaration or retry-until-green is introduced; the two-slot budget is untouched. |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | The extended engine keeps its `-h` / `--version` and undeclared-option rejection before any read; the new `settle` action is read-only (zero write points, asserted by AST and tree-hash legs). `dispatch.sh` keeps its guard block and adds only trap/record writes it already owns as a carrier. |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | The stage re-reads its rules after each core step and records `on-track` / `correction-applied` / `decision-needed` in the stage evidence; no approval request is raised. |
| XXIII | AI-Generated Code Review Policy | ✅ Pass | AI-authored change follows `.specify/workflow/git.md` (temp-branch model; merge to the declared trunk by the orchestrator); review reads merged history; no PR and no separate ledger. |

**Gates Status**: ✅ All 23 gates pass. No `Partial` or `Fail` row, so Complexity Tracking is `N/A`. One **pre-existing** red (confirmation-gate total `31 != 27`) is disclosed as a `falsified`/`fallback` premise, not a plan-induced failure.

**Re-check after Phase 1**: re-judged after the Phase 1 artifacts landed (2026-11-25) — every row remains ✅ Pass. Two facts sharpened during design: (a) the engine's `report` schema must stay byte-identical, so the settlement face is a **new action** rather than new report keys (row XIV/XXI); (b) the team report column addition is an **engine-accepted 7-column header** in addition to the legacy 5-column header, never a replacement (row VIII/XIV).

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md`.*

### T-001 — 结算判定面复用 `role-edge-check.py` 的新动作，而不是新建独立结算引擎

- **decision**: 结算判定落在 `scripts/python/role-edge-check.py` 的加性 `--action settle` 上，不新建第二个引擎。
- **antithesis**: 新建 `scripts/python/settlement-check.py` 专用引擎；当结算判定需要频繁独立演进（例如按载体拆成多文件 reader、或需要与边判定不同节奏发布）时它更优——接口可以只服务结算，不受既有 report/query schema 的兼容约束。
- **binding_constraints**:
  - pole_a: 单一判定面——同一 owner 页只能被一个引擎实现，新增违规种类不得产生第二张状态值表或第二份证据矩阵（A-6 / FR-028 / FR-038）。
  - pole_b: 既有边判定契约不得被结算逻辑牵动——`report` / `query` 的 schema、退出码语义与其契约测试必须保持原样（FR-033 空允许差异集）。
- **discriminating_evidence**: 在 `report`/`query` 夹具上对同一输入先后运行基线引擎与扩展引擎，`json` 输出逐字节比较；结果二值：完全相同 / 不完全相同。
- **expected_sacrifice**: SC-007 Source ↓ 引擎输入层增大（增加 try-record / end-record / 报告列 reader），共享解析代码面扩大，settle 的缺陷可能影响同一进程的读取；由 report/query 字节相等与独立解析入口约束。
- **revision_trigger**: 连续两个切片出现「settle 改动导致 report/query 回归」≥2 次 → 重开，拆分为独立引擎（届时必须先落 A-6「既有 owner 不覆盖」裁定）。

### T-002 — C2 的起点/终止证据走加性旁路文件，而不是扩写 `.status` 行

- **decision**: `dispatch.sh` 在既有三件套旁新增 `<label>.attempt` / `<label>.end` 两个加性文件，`.status` 行保持 `<label> exit=<code>` 不变。
- **antithesis**: 把 pid、start、signal 等字段直接追加到 `.status` 行；当所有消费方都由本仓库控制且能同步升级时它更优——每尝试只有一个证据文件，读取与解析路径最短。
- **binding_constraints**:
  - pole_a: 旧消费者必须零改动继续工作——`.status` 行的字面格式、三件套语义与既有读取器（`journal-utils.py`、`status-digest.py`、`exec-quant.py` 的 dispatch quality）不加修改即可读（FR-015 / FR-033）。
  - pole_b: 结算必须能证明「执行主体已消失」——没有 pid/start/终止记录，静默死亡与仍在运行无法区分（FR-016 / SC-001）。
- **discriminating_evidence**: 用基线版 `.status` 读取器（`journal-utils.py --action`/`status-digest.py` 的同一解析函数）分别读取一份新 `.status` 与一份基线 `.status`；结果二值：读取结果相同 / 不同。
- **expected_sacrifice**: SC-002 Source ↓ 每个尝试的证据文件从 3 个增至 5 个，目录读取面变大；由「一尝试一文件、时间戳/标签命名」的并发安全布局与只读判定吸收。
- **revision_trigger**: 任一旧消费者在读取新 `.status` 时出现解析失败 ≥1 次 → 重开，改为在 `.status` 行尾追加字段并同步升级全部消费方与测试。

### T-003 — legacy 记录仍可被推导结算，但永不计为符合新契约

- **decision**: 对没有 `settlement_version` 的旧尝试/旧报告，判定面仍从原始证据推导结算值并在输出中标 `legacy`，但 `legacy` 行永不计为「符合新契约」，且标注本身不产生失败退出码。
- **antithesis**: 对未声明版本的记录一律拒绝结算（只输出 `unknown` 并要求迁移）；当旧记录量小、且误判代价高于无法结算的代价时它更优——判定面不需要理解任何历史形态。
- **binding_constraints**:
  - pole_a: 历史记录是当时事实，不改写、也不假装合规——旧证据必须仍可解释，否则「升级前看不出来」变成「升级后假装看得出来」（A-10 / FR-034）。
  - pole_b: 新契约必须可判——任何声称合规的记录都必须携带版本与证据指针，否则契约退化为散文（FR-034 / SC-006）。
- **discriminating_evidence**: 对同一份旧格式夹具运行判定面，检查输出是否同时满足「有推导结算值」「行带 legacy 标注」「退出码非 1（标注不是拒绝）」；结果二值：三者全满足 / 任一不满足。
- **expected_sacrifice**: SC-006 Source ↓ 判定面需长期兼容一种「无版本」读法，输入解析分支多一条；由「legacy 不计合规 + 不改写 + 拒绝只归 unknown」三分约束。
- **revision_trigger**: 出现一次「legacy 推导结算被父侧记录推翻」→ 重开，改为对无版本记录只输出 `unknown` 与迁移提示。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/106-background-silent-failure/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (B-01…B-14 measurements, R-01…R-08 decisions)
├── data-model.md        # Phase 1 output (E1–E9, INV01…INV12)
├── contracts/           # Phase 1 output (3 files: settlement-contract, carrier-conformance, enforcement-and-migration)
├── quickstart.md        # Phase 1 output (S-0…S-7, per-example premises and pins)
├── feature-ref.md       # Phase 1 output (Feature 095 binding, delivery surface, unit-registration verdict)
├── test-evidence/       # stage readings (pre-analyze, gate/scan/mirror baselines, stage-status row, wrap-up records)
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md      # Implementation output (/speckit.implement — NOT created here)
```

### Source Code (repository root)

```text
shared/definitions/superagent-definitions.md        # § Termination amendment: closed settlement set + per-value evidence + reaction + legacy + violation kinds
shared/definitions/subagent-definitions.md          # § Three Execution Modes: virtual exclusion sentence + settlement-owner pointer
shared/workflow/external-dispatch-recipes.md        # Recipe 4 stall wording → per-value dispositions; Recipe 7 wave settlement pointer
scripts/python/role-edge-check.py                   # additive --action settle (read-only; report/query unchanged)
skills/internal/create-team/scripts/dispatch.sh     # C2: additive .attempt/.end records, pid, TERM/INT/HUP trap; .status format unchanged
skills/internal/create-team/SKILL.md                # report contract: 7-column mapping table (end_state, evidence) + Verification settlement coverage
skills/internal/run-team/SKILL.md                   # one settlement-owner pointer line for the seat dispatch entry
skills/internal/run-agent/SKILL.md                  # attempt record at dispatch, settle-before-report, native background/foreground branches, virtual exclusion
skills/external/sdd-loop-driver/SKILL.md            # one settlement-owner pointer line (C1 mapping consumed)
templates/commands/agents.md                        # one settlement-owner pointer line (entry)
templates/commands/team.md                          # one settlement-owner pointer line (entry)
agents/sdd-plan-coordinator.agent.md                # one settlement-owner pointer line (coordinator class)
agents/sdd-task-coordinator.agent.md                # one settlement-owner pointer line (coordinator class)
agents/sdd-implement-coordinator.agent.md           # one settlement-owner pointer line (coordinator class)
agents/sdd-review-coordinator.agent.md              # one settlement-owner pointer line (coordinator class)
docs/reference/skills/sdd-loop-driver.md            # settlement section: owner pointer + C1 verdict mapping pointer
docs/reference/commands/agents.md                   # run-mode settlement pointer
docs/reference/teams/orchestration.md               # seat end_state / settlement coverage pointer
tests/fixtures/settlement/                          # new fixture tree: C1 state dir, C2 logs, C3 reports, legacy vs versioned
tests/contract/test_settlement_contract_definitions.py
tests/contract/test_settlement_engine.py
tests/contract/test_settlement_carriers.py
tests/contract/test_settlement_migration.py
tests/contract/test_settlement_preservation.py
tests/contract/test_settlement_scope.py
.specify/features.md                                # row 106 → Planned; clause count/date
.specify/features/095-superagent-role.md            # plan note for slice 106; parent status unchanged
.specify/glossary.md                                # `silent-end` proposal (origin=auto, status=proposed) via glossary-utils
```

**Structure Decision**: the feature extends the existing framework layout in place — one owner definition amended, one shared modes section touched, one recipes file corrected, one engine action added, one carrier script extended, five skill/report text surfaces and two command templates edited (with per-tool copies regenerated), four coordinator templates receiving one pointer line each, three existing reference pages updated, six new test modules plus one fixture tree inside the existing `tests/fixtures/` convention, and the Feature registry rows updated. No new top-level directory, no new skill, no new script, no runtime service. `watch-target.sh`, `stage-runner.sh`, `exec-quant.py`, `sync-mirrors.py`, `regen-command-copies.py` and `scan-confirmation-gates.py` are consumed and **not edited**.

### Unit Registration Verdict

**No new unit row is registered.** The feature adds no skill and no command. The edited command templates (`/speckit.agents`, `/speckit.team`) and skills (`run-agent`, `run-team`, `create-team`, `sdd-loop-driver`) already hold their per-unit registrations in `shared/definitions/flow-class-definitions.md` and `shared/definitions/probe-definitions.md`; `role-edge-check.py` is an engine, not a registered unit. Therefore no flow-class row, probe row or new Feature row is added — the Feature registry receives only the slice status advance (106) and the plan note on 095.

### Mirror Obligations *(mandatory — several edited files have mirrors or generated copies)*

**Baseline drift measured before any edit** (2026-11-25, `.venv/bin/python`): `python scripts/python/sync-mirrors.py --check` rc 0 (six pairs ok, six projected rows ok) and `python scripts/python/regen-command-copies.py --check` rc 0 (`OK: all per-tool command copies match the source templates`). Evidence: `test-evidence/mirror-check-baseline.txt`. The Verify cells mean **no NEW drift on the pairs this spec touches**, judged against that baseline — never "all green" as an absolute claim.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/superagent-definitions.md`, `shared/definitions/subagent-definitions.md`, `shared/workflow/external-dispatch-recipes.md` | `.specify/shared/definitions/…`, `.specify/shared/workflow/…` (pair `shared` ↔ `.specify/shared`) | `.venv/bin/python scripts/python/sync-mirrors.py --write --only shared` then `--check`; pair `ok`; `diff -q` on the three files empty |
| `scripts/python/role-edge-check.py` | `.specify/scripts/python/role-edge-check.py` (pair `scripts`, strict) | `.venv/bin/python scripts/python/sync-mirrors.py --write --only scripts` then `--check`; `cmp` source/mirror rc 0 (existing engine test also asserts byte equality) |
| `skills/internal/create-team/scripts/dispatch.sh`, `skills/internal/create-team/SKILL.md`, `skills/internal/run-team/SKILL.md`, `skills/internal/run-agent/SKILL.md` | `.specify/skills/internal/…` (pair `skills/internal`) | `.venv/bin/python scripts/python/sync-mirrors.py --write --only skills/internal` then `--check`; pair `ok`; `diff -q` on the four files empty |
| `skills/external/sdd-loop-driver/SKILL.md` | `.specify/skills/sdd-loop-driver/SKILL.md` (pair `skills/external` ↔ `.specify/skills`, excludes `internal`/`site`) | `.venv/bin/python scripts/python/sync-mirrors.py --write --only skills/external` then `--check`; pair `ok`; `diff -q` empty |
| `agents/sdd-plan-coordinator.agent.md`, `agents/sdd-task-coordinator.agent.md`, `agents/sdd-implement-coordinator.agent.md`, `agents/sdd-review-coordinator.agent.md` | `.specify/agents/templates/…` (pair `agents`) | `.venv/bin/python scripts/python/sync-mirrors.py --write --only agents` then `--check`; pair `ok`; `diff -q` on the four files empty |
| `templates/commands/agents.md`, `templates/commands/team.md` | `.claude/commands/speckit.agents.md`; `.claude/commands/speckit.team.md`; `.github/prompts/speckit.agents.prompt.md`; `.github/prompts/speckit.team.prompt.md`; `.qoder/commands/speckit.agents.md`; `.qoder/commands/speckit.team.md`; `.opencode/command/speckit.agents.md`; `.opencode/command/speckit.team.md` (via `regen-command-copies.py`; NO .specify/templates/commands mirror — retired) | `.venv/bin/python scripts/python/regen-command-copies.py` then `--check` rc 0; each copy contains the added pointer line |

`docs/**`, `tests/**`, `.specify/specs/106-background-silent-failure/**` and `.specify/features*` have no mirror; `.specify/features*` and `.specify/glossary.md` are single-owner registries and are never split.

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises. The ids below are the targets cited by `requirements.md` RS-001…RS-004.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The C1 carrier (stage-runner four-piece + watch-target verdicts) is byte-stable since the requirements baseline and can be consumed as the settlement evidence source without changing its judgments, exit codes, sentinel literals or `--self-test`. | `sha256(watch-target.sh at HEAD) = sha256(fbab7a45c)` = `955ddf7820a80cb3afad5af25877f2f8d7093e4fb08c46ec59dfe948ec3f2479`; `--self-test` 39 passed / 0 failed; extracted verdict tokens `{DONE,RUNNING,ANOMALY,FAILED,DEAD,TIMEOUT,INCOMPLETE,NO_SIGNAL}`, exit codes `{0,2,10,11,12,13,14,15,16}`, sentinel literals `{STAGE-DONE}` — `test-evidence/watch-*.txt`, `watch-target-fbab7a45c.sh`. | verified | — |
| EP-002 | `dispatch.sh` is the only C2 wrapper, and no consumer reads beyond the `.status` line format, so additive `.attempt` / `.end` files plus a pid and a signal trap can be added without breaking existing readers. | `dispatch.sh:142-151` (pipeline; `.status` written once at normal end; no trap/pid/heartbeat); triplet consumers are `journal-utils.py:515` (`label.status` existence), `status-digest.py:1806` (`.status` line), `exec-quant.py dispatch_quality` (exit code from `.status`); no consumer globs or parses other triplet suffixes. | verified | — |
| EP-003 | `role-edge-check.py` can gain an additive `--action settle` without disturbing `report` / `query`: its action choices are not exhaustively pinned, and the report schema is pinned by its own test, which the additive action leaves untouched. | `role-edge-check.py:961` (`choices=("report","query")`), `:976-1000` (exit codes 0/1/2); `tests/contract/test_role_edge_engine.py` pins `--action` presence and report/query keys, not the exhaustive choice list; engine is read-only (AST-scan test C6). | verified | — |
| EP-004 | The unique test entry resolves a pytest interpreter and can run this feature's targeted sets in parallel with deterministic fixtures and no fixed sleeps. | `scripts/bash/run-tests.sh` `resolve_python()`; measured `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_superagent_definitions.py -q` → 10 passed rc 0 (`test-evidence/test-entry-smoke.txt`). Host caveat: repo `.venv` carries no pytest, so the implement stage MUST pass `SPECKIT_PYTHON=/usr/local/bin/python3`. | verified | — |
| EP-005 | The confirmation-gate frozen total is 27 and its equality test is green, so FR-039's "keep it green" is satisfiable as written. | `python3 scripts/python/scan-confirmation-gates.py --root . --json` → **total 31** (governance_kept 7 / destructive 23 / reversible 1); `tests/contract/test_user_facing_comprehension_doc.py::test_gn_c2_gate_scan_total_unchanged` **fails** `31 != 27` at the stage base — `test-evidence/scan-confirmation-gates-baseline.json`, `test-evidence/confirmation-total-red-at-base.txt`. | falsified | fallback |

**EP-005 fallback criterion (the substituted measurement)**: FR-039 is measured as **zero NEW blocking hits on the files this feature touches** — per-file hit count after ≤ per-file count at base (base hits: `shared/definitions/superagent-definitions.md:58` and `skills/external/sdd-loop-driver/SKILL.md:189`; every other touched file 0). The `== 27` equality remains a disclosed pre-existing red reported to `/speckit.analyze` and review; this feature never claims it green.

## Inherited Blockers

Dependency set: none

No dependency artifact is declared. Feature 095 is this feature's **parent** (the owner page and engine being amended), not a dependency whose `verification.md` or deferred rows this plan inherits from: its record carries `deferred_tasks=none`, `final_path_blocked=0`, `final_path_deferred=0`, `final_path_partial=0` and no `## Deferred` items (measured 2026-11-25), so the extraction set is empty. Features 058 / 065a / 093 / 096 contribute owners and read-only carriers (driver watch model, state snapshot, concurrency facts, observer) consumed by reference; none is declared as a dependency artifact.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | — | not-applicable | — | this-slice | No dependency artifact was declared; nothing is inherited. |

## Complexity Tracking

N/A — the Constitution Check has no `Fail` or `Partial` row, so there is nothing to justify.

## Phase 1: Design Artifacts Summary

Backfilled after the Phase 1 artifacts landed on disk (2026-11-25). Counts were taken from the files, not from the Phase 0 expectation.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | `data-model.md` | 9 entities (E1–E9) + 12 invariants (INV01…INV12) + one attempt state-transition table |
| Contracts | `contracts/` | 3 files / 34 clauses — `settlement-contract.contract.md` C-01…C-12 (12), `carrier-conformance.contract.md` C-13…C-24 (12), `enforcement-and-migration.contract.md` C-25…C-34 (10) |
| Quickstart | `quickstart.md` | 8 scenarios (S-0…S-7): 5 mixed/not-implemented with per-example premises + pinning tests, 1 run-now preserved-surface scenario with observed outputs, 1 run-now mirror scenario, 1 reading scenario |
| Research | `research.md` | 14 measurements (B-01…B-14) + 8 decisions (R-01…R-08) |
| Feature reference | `feature-ref.md` | 35 delivery-surface items; unit-registration verdict = no new unit |
| Test evidence | `test-evidence/` | pre-analyze plan JSON+stdout, flow-class lookup, watcher baseline (file/help/self-test + byte copy), mirror baseline, gate-scan baseline + red proof, test-entry smoke, workspace snapshots, stage-status row, wrap-up records |

**Drift from the Phase 0 expectation**: none in scope; one disclosed baseline fact changed the enforcement reading — the confirmation-gate frozen `total == 27` equality is already red at the stage base (live total 31), so the plan records EP-005 as `falsified` with a `fallback` criterion (zero NEW hits on touched files) instead of claiming a green that does not exist. This is recorded in `research.md` B-10 and `test-evidence/scan-confirmation-gates-baseline.json`.

