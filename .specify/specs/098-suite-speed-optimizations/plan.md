# Implementation Plan: 098 Suite Speed Optimizations

**Branch**: `098-suite-speed-optimizations` | **Date**: 2026-11-10 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `098-suite-speed-optimizations` → Feature 086 Efficient Test Execution (Concurrent by Default)
**Input**: Specification from `.specify/specs/098-suite-speed-optimizations/requirements.md`

> **Concurrency obligation (执行义务，按指针抵达)**: this plan authorizes execution bodies. Each one follows the framework's single concurrency obligation — consider concurrency first, default to it when the class and capability allow, and name a reason code plus record the `requested` / `effective` / `effective_reason` reading when serial. The obligation's authored text is `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; its class table is `shared/declarations/facts/concurrency-class.yaml`, its reason codes `shared/declarations/facts/serial-reason.yaml`, and its reading fields `shared/declarations/facts/effective-concurrency.yaml`. This template restates none of their rules.

## Summary

Feature 098 removes four remaining cost sources from the spec-kit test suite without changing what the suite
checks: (1) it verifies and fixes the already-default xdist parallel mode by name-level comparison, starting
with `tests/contract`; (2) it introduces a `slow` marker tier so the default feedback loop excludes
process-boundary integration tests and full-corpus contract tests while the two-slot budget keeps running
the full tier explicitly via `--full`; (3) it converts repeated whole-corpus scans in two contract files to
per-session (per-worker) read-only snapshots; (4) it replaces fixed sleeps with an injected clock, explicit
file mtimes, and deadline-bounded event waits; (5) it converts non-boundary `subprocess.run` calls to
in-process engine calls, keeping process-boundary subjects as subprocesses.

The technical approach is additive on the 086 runner contract: the tier is a selection composition
(`-m "not slow"` by default, `--full` to lift it), the exclusion count is measured by marker enumeration,
and every disclosure line keeps its 086 prefix. No second runner, no new dependency, no CI workflow, and no
change to the two-slot count/timing/order.

### Acceptance preservation (the five optimizations)

| # | Optimization | Criterion-preserving acceptance | Contract | SC |
|---|--------------|----------------------------------|----------|----|
| 1 | xdist verification | `tests/contract` first, then full tree at closure: same-tree default-parallel vs `--serial` `--names-out` lists, bidirectional `comm` empty; a non-parallel-safe fixture must turn the comparison red; missing-engine branch completes serially with `reason=no-xdist` | parallel-consistency C-001…C-012 | SC-002, SC-003 |
| 2 | slow tier | default collection set = full collection set − marked set; excluded count derived by enumeration and disclosed; `--full` restores the full set; both slots run with `--full`; no test deleted or renamed | tier-selection C-001…C-016; slow-membership C-001…C-009 | SC-004, SC-005, SC-006, SC-010 |
| 3 | session scan cache | `build_count = 1` per worker with more than one consumer; same assertion set green; cross-session mutation drill turns the affected assertion red; mutable fixtures never share the cache | scan-cache C-001…C-011 | SC-007 |
| 4 | sleep removal | zero synchronization `time.sleep` in scope (AST scan); every wait has an explicit deadline (default 30 s) and interval ≤ 0.2 s; timeout is a named failure, never skip/xfail/retry; same worker-count before/after wall pair | event-wait C-001…C-010 | SC-008 |
| 5 | in-process conversion | manifest closed over the AST census; every keep row carries a boundary class; reverting a converted point turns the guard red and names it; same assertions green before/after | inprocess-conversion C-001…C-010 | SC-009 |

No optimization may be cashed in via any means the criterion owner prohibits
(`.specify/shared/guidelines/test-execution-efficiency.md` §「不可采纳的提速手段」; this plan does not restate
that list); the 098-specific detection increments are enforced by the SC-010 diff scan (FR-021, SC-010).

## Technical Context

**Language/Version**: Python `>=3.8` (project floor); host interpreter 3.11.11 (probe 2026-11-10)
**Primary Dependencies**: pytest 8.4.2 and pytest-xdist 3.8.0 (dev-only, existing); typer (CLI); no new dependency
**Storage**: files only — in-memory session cache, `test-evidence/` records; no database
**Testing**: canonical runner `scripts/bash/run-tests.sh`; default `-n <effective> --dist load`; two-slot budget (baseline/closure)
**Target Platform**: developer hosts (Linux/macOS); downstream Python 3.8 without xdist takes the `reason=no-xdist` serial branch
**Project Type**: single repository — framework source plus its own client runtime (`.specify/`)
**Performance Goals**: default tier wall ≤ 50 % of the implement-start full default-parallel baseline (SC-004); full tier ≤ 110 % of the same baseline (SC-005); `test_client_metrics.py` wall drops by the removed fixed waits at equal worker count; corpus pair builds once per worker
**Constraints**: two-slot budget (no third full run for measurement); 086 C-001…C-016 unchanged; script interface contract; no CI workflow; no selection shrink
**Scale/Scope**: 8543 collected tests; 6 contract files; 9 work packages; conversion manifest spans ~495 discovered `subprocess.run` sites (228 files) with a measured keep/convert split

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md` v1.19.0):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | `contracts/tier-selection.contract.md` C-001…C-016 and `feature-ref.md` delivery rows trace every FR |
| II | Feature-Centric Development | ✅ Pass | `feature-ref.md` binding block; `.specify/features/086-efficient-test-execution.md` § Related Specifications (098 row); no new feature id |
| III | Intent-Driven Development | ✅ Pass | `requirements.md` states what/why; `plan.md` § Decision Tensions records the how-level alternatives |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | `contracts/*.md` § Test obligations; WP-1/WP-2/WP-5/WP-6/WP-7 order guard tests before behavior change; equivalence runs recorded |
| V | AI Agent Integration Standards | ✅ Pass | `feature-ref.md` § Out of scope (no agent roster/tier/provider change); `requirements.md` RS-001…RS-004 pins are pytest-only |
| VI | Continuous Quality & Observability | ✅ Pass | `quickstart.md` S-0 measured baselines (incl. pre-existing failures); `test-evidence/corpus-write-hazard.txt`; no `.bak` copies |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | `plan.md` (this artifact) plus `feature-ref.md`; 086 status not flipped |
| VIII | Code as the Single Source of Truth | ✅ Pass | `research.md` B-1…B-10 measured from runner/engine/source; mirror table read from `scripts/python/sync-mirrors.py` MIRROR_PAIRS |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | `requirements.md` § Runtime Stack (zero new third-party deps); `feature-ref.md` § Out of scope (no new runner/CI/directory) |
| X | Documentation Naming & Location Conventions | ✅ Pass | `plan.md` § Project Structure (lowercase conventional names inside the spec directory; no reserved ALL-CAPS names) |
| XI | Dogfooding (Self-Application) | ✅ Pass | `feature-ref.md` § Disclosure decisions (framework source edits plus mirror regeneration — both hats named) |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | `plan.md` § Technical Context reuses `run-tests.sh`, `wait_until`, the importlib house pattern and `sync-mirrors.py` |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | `requirements.md` SC-001…SC-011 Measurement Sources plus `research.md` § Re-measure list (evidence-grade improvement claims) |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | `contracts/tier-selection.contract.md` owns the tier; `plan.md` § Mirror Obligations references `sync-mirrors.py` MIRROR_PAIRS instead of restating it |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | `data-model.md` E-1…E-8 define every field/domain at first use; `quickstart.md` scenario text uses the same terms |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | `research.md` B-4/B-5 and `plan.md` § Risks R-2/R-3 surface anomalies instead of silently repairing them |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | `plan.md` § Project Structure adds no directory; `research.md` § Probe transcripts used the sanctioned `.specify/.tmp/` root |
| XVIII | Grounded Naming | ✅ Pass | `plan.md` § Technical Context and `requirements.md` § Shared Strings carry [[STR-001…003]] verbatim; new test names follow siblings |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | `data-model.md` E-7 (tier + excluded count on the runner's own line) and E-2 registry columns |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | `plan.md` § Summary acceptance-preservation table and `contracts/*.md` mutation legs (no selection shrink, skip, or retry) |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | `contracts/tier-selection.contract.md` C-005 and `contracts/event-wait.contract.md` C-004 (help-documented, zero-side-effect flags) |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | `plan.md` § Execution Record keeps the anchor and reading; `research.md` R-10 records the same-author delegation |

**Gates Status**: ✅ All gates pass (no Fail/Partial rows; Complexity Tracking is N/A).

**Re-check after Phase 1**: 2026-11-10 — re-run against the landed design artifacts; rows unchanged because
the contracts, data model and quickstart each cite the same requirement/contract pair, and no design choice
introduced a new violation. Delegated fresh-context review recorded in `test-evidence/plan-verification.txt`.

## Decision Tensions

Fields and rejection criteria are owned by `.specify/shared/guidelines/decision-tension.md` (read from the
repository root); this section records three load-bearing decisions and nothing else.

### T-001 — 缺省档排除慢档，全量档由 `--full` 显式请求

- **decision**: 缺省档（`fast`）排除慢档，全量档必须由 `--full` 显式请求；两槽位命令改为显式全量。
- **antithesis**: 「缺省全量 + 显式 fast 档」——当维护者已习惯全量缺省、且 CI/本地循环不追求反馈速度时它更优：所有人默认拿到完整覆盖，无需记住一个开关。
- **binding_constraints**:
  - pole_a: 缺省运行必须是完整覆盖——任何人无参数运行都不会少跑测试。
  - pole_b: 日常反馈的缺省墙钟必须显著下降，否则本特性没有收益（SC-004）。
- **discriminating_evidence**: 同一棵树、同主机同日、同一 runner 形态下运行缺省档与 `--full` 全量档并记录墙钟与收集集合：缺省档墙钟 ≤ 基线 50% 且收集集合 = 全量 − 慢档集合（判绿）；任一不成立或全量档新增失败名非零（判红）。
- **expected_sacrifice**: SC-004 Source ↑ 缺省运行不再覆盖全量：未读披露的用户会漏跑慢档测试；两槽位显式全量与排除数披露是补偿，不消除该代价。
- **revision_trigger**: 下游项目把缺省档误当全量 ≥ 2 次（反馈登记），或 closure 出现一个可归因于缺省档漏跑的失败名 ≥ 1 → 重开，改为缺省全量并把 `fast` 做成显式档。

### T-002 — 注入时钟落在引擎可选 `--now` 参数

- **decision**: 顺序确定性通过 `feedback-utils.py` 的可选 `--now` 注入时钟实现，测试仍经引擎的 `record`/`mark-submitted` 路径产生真实条目。
- **antithesis**: 纯测试侧构造——直接写条目文件或回写 `created` 字段，并 `os.utime` 控制 mtime；当被验证对象只是 metrics 计算、且引擎 CLI 面应完全冻结时它更优：产品代码零改动。
- **binding_constraints**:
  - pole_a: 产品引擎的 CLI 面必须保持冻结——不新增被分发的选项。
  - pole_b: 被测条目必须保持引擎真实产出形态，测试侧构造不得到达（断言强度不得下降）。
- **discriminating_evidence**: 带 `--now` 的转换后 `test_client_metrics.py` 全绿且 `grep -c 'time.sleep'` 为 0（判绿）；不传 `--now` 时引擎产生与变更前相同的 `created`/id 形态且既有引擎契约测试全绿（判绿）；任一断言需改写才绿或默认输出改变（判红）。
- **expected_sacrifice**: SC-008 Source ↑ 引擎 CLI 新增一个选项面，需要 `--help` 文档、默认关闭回归与后续维护。
- **revision_trigger**: 任一调用方无法注入时间戳，或 `--now` 出现在生产调用记录 ≥ 1 → 重开，退回测试侧构造并移除选项。

### T-003 — 进程内直调按「清单 + 二值边界类」逐点转换

- **decision**: 非边界调用点按清单逐点转为进程内直调；携带 `cwd`/`env` 且无法恢复的 fixture 层调用保留子进程，保留点逐条给出边界类。
- **antithesis**: 全部保持子进程——当测试套件的价值主要来自「真实进程边界」且解释器启动成本可接受时它更优：零转换风险、零断言改写。
- **binding_constraints**:
  - pole_a: 非边界调用的解释器启动成本必须消除（SC-009）。
  - pole_b: 每个调用都应保留真实进程边界，以保证断言与进程行为一致。
- **discriminating_evidence**: 清单守卫在任一已转换点改回 `subprocess.run` 时转红并指名文件与调用点（二值）；同一断言集在转换前后全绿（判绿）；任一点只能靠改写断言才绿（判红）。
- **expected_sacrifice**: SC-009 Source ↑ 约两百个转换点失去真实进程边界，存在误分类风险；清单、边界类与等价证据是补偿。
- **revision_trigger**: 任一转换点出现无法用断言集等价解释的行为差异 ≥ 1（回退该点并记录），或 fixture 层必须进程内化才能达到 SC-009（重开边界判据）。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/098-suite-speed-optimizations/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output: measurements B-1…B-10, decisions R-1…R-10
├── data-model.md        # Phase 1 output: entities E-1…E-8
├── quickstart.md        # Phase 1 output: scenarios S-0…S-11
├── contracts/           # Phase 1 output: 6 files (see Phase 1 summary)
├── feature-ref.md       # Phase 1 output: delivery surface + disclosures
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
├── verification.md      # Implementation output (/speckit.implement command)
└── test-evidence/       # measurements and guards' evidence
```

### Source Code (repository root)

```text
scripts/bash/                    # canonical runner source (tier flags and disclosure)
scripts/python/                  # feedback-utils.py (optional --now clock)
.specify/scripts/                # projected/mirrored runtime copies (bash + python pairs)
skills/external/sdd-loop-driver/references/   # budget owner + stage prompts (framework source)
.specify/skills/sdd-loop-driver/references/   # runtime mirrors of the same references
pyproject.toml                   # slow marker registration
tests/conftest.py                # session scan-cache fixtures
tests/contract/                  # new guards + converted corpus/client-metrics tests
tests/integration/               # runner-related event waits
tests/fixtures/                  # wait helper defaults
.specify/specs/098-suite-speed-optimizations/ # this artifact set
.specify/features.md             # Feature 086 index row note (status unchanged)
.specify/features/086-efficient-test-execution.md  # dated plan-stage note
.specify/register.md             # T-001/T-002/T-003 registration
```

**Structure Decision**: extends the existing test-infrastructure surface — the canonical runner, one
existing engine, the shared test fixtures, and the driver reference docs. No new top-level directory and no
new script are introduced; new contract tests land beside their siblings under `tests/contract/`.

### Mirror Obligations

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/bash/run-tests.sh` | `.specify/scripts/bash/run-tests.sh` via projected `bash-version-guard` (`sync-mirrors.py`) | `python3 scripts/python/sync-mirrors.py --check` shows no NEW drift on this pair; the C-016 projection case stays green. Baseline measured 2026-11-10: all pairs `ok`, exit 0 |
| `scripts/python/feedback-utils.py` | `.specify/scripts/python/feedback-utils.py` (pair `scripts/`, byte-identical) | same `--check` run; no NEW drift |
| `skills/external/sdd-loop-driver/references/efficiency-model.md` | `.specify/skills/sdd-loop-driver/references/efficiency-model.md` (pair `skills/external/`) | same `--check` run; regenerate with `--write --only skills/external` |
| `skills/external/sdd-loop-driver/references/stage-prompts.md` | `.specify/skills/sdd-loop-driver/references/stage-prompts.md` | same |
| No `templates/commands/` edit | no per-tool command copies touched | not applicable |

## Execution Premises

Column shape and value domains are owned by `.specify/shared/workflow/acceptance-hardening.md` § Execution
Premises; this table carries values only.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The default-tier injection composes with the existing serial two-pass model without changing any 086 C-001…C-016 semantics: the 086 contract fixture trees register only `serial` and contain no slow markers, so their selections and disclosures are unchanged by the new field | `test-evidence/runner-contract-pretest.txt` (40 passed, exit 0) + `tests/contract/test_run_tests_runner_contract.py:56-79` fixture builder | verified | — |
| EP-002 | The resolved interpreter can import pytest-xdist and a session-scoped fixture is built once per xdist worker (upper bound = worker count, not test count) | `test-evidence/plan-baseline-probe.txt` (xdist 3.8.0) + `test-evidence/session-fixture-probe.txt` (3 tests on `-n 2` produced exactly 2 builds, `gw0`/`gw1`) | verified | — |
| EP-003 | `scripts/python/feedback-utils.py` reads time only through `now_iso()`/`timestamp_id()`, so one optional injected-clock option covers every ordering site (`record` created/id, `mark-submitted` submitted_at, package stamps) | source read: `scripts/python/feedback-utils.py:125,129,879,881,1056,2071,2075`; no other clock source in the record path | verified | — |
| EP-004 | The write surface is complete for the four in-scope groups (runner tier, slow registry, scan cache, sleep scope) without touching production code outside `feedback-utils.py`; the conversion manifest's denominator is enumerable from source | `test-evidence/plan-baseline-probe.txt` (scope sleep counts, 0 session fixtures) + subprocess census (495 real calls / 228 files) + `test-evidence/overlap-check-plan.txt` (decision=overlap, adjudicated as additive coexistence in `feature-ref.md` § Disclosure decisions) | verified | — |

## Inherited Blockers

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:
- `086`: `.specify/features/086-efficient-test-execution.md`, `.specify/specs/086-efficient-test-execution/verification.md`

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| — | — | not-applicable | — | — | 086 has no `## Deferred` section and no `blocked`/`deferred`/`partial` verification row: every status row in its `verification.md` is `pass` and `deferred_tasks=` is empty |

## Complexity Tracking

N/A — the Constitution Check has no Fail or Partial rows.

## Phase 0: Research Review

Standalone `research.md` (measurements exceed 50 lines and include measured baselines): B-1…B-10 record the
interpreter/xdist/marker baseline, the pre-change runner-contract green run, the client-metrics and
corpus-pair timings, the two pre-existing baseline failures, the corpus-write hazard, the per-worker session
probe, the sleep/subprocess censuses, and the two-slot owner surfaces. R-1…R-10 record the decisions this
plan stands on (tier composition matrix, count/disclosure method, empty-selection diagnosis, registry
format, cache key/factory, injected clock, event-wait scope, conversion boundary classes, budget surfaces,
same-author delegation). The re-measure list names what implement must measure rather than inherit.

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | 8 entities (E-1…E-8), 2 state lists, no transition table |
| Contracts | [`contracts/`](./contracts/) | 6 files, 68 clauses: `tier-selection.contract.md` (C-001…C-016), `slow-membership.contract.md` (C-001…C-009), `parallel-consistency.contract.md` (C-001…C-012), `scan-cache.contract.md` (C-001…C-011), `event-wait.contract.md` (C-001…C-010), `inprocess-conversion.contract.md` (C-001…C-010) |
| Quickstart | [`quickstart.md`](./quickstart.md) | 14 scenarios S-0…S-13; S-0.1…S-0.6 executed with real output; every later scenario carries a per-example premise list |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | 26 delivery-surface rows; disclosures and out-of-scope list |
| Research | [`research.md`](./research.md) | B-1…B-10 measurements; R-1…R-10 decisions; re-measure list |

Drift from Phase 0 expectation: none — the intended artifact set landed; the only surprise is the
pre-existing baseline failure pair and the corpus-write hazard, both recorded as evidence and risk.

## Work Packages (tasks handoff)

Each package is bounded at ≤10 work items; packages are ordered by dependency and sized so `/speckit.tasks`
can map them to task rows without re-partitioning. Tests precede behavior changes inside each package.

### WP-1 — Runner tier mechanism (`scripts/bash/run-tests.sh`)

1. Author tier contract cases first (fixture trees; obligations 1–10 of tier-selection §E).
2. Parse `--full`; update the script-interface usage text and `--help` output.
3. Detect caller `-m` in both spellings; resolve `tier=caller`.
4. Implement default exclusion and the two-pass fast composition.
5. Implement the serial-mode tier composition (`--serial` orthogonal).
6. Implement marker enumeration + `excluded_slow` measurement (exit 5 = zero).
7. Append `tier=`/`excluded_slow=` to mode lines; extend the header truthfully.
8. Implement the empty-after-exclusion named error and exit 2.
9. Regenerate the projected mirror via `sync-mirrors.py --write --only scripts`.
10. Run the 086 contract suite (40 cases) and the new tier cases; record both.

### WP-2 — Slow registry and guard

1. Register the `slow` marker in `pyproject.toml`.
2. Measure candidate durations (process-boundary and corpus-scan pools) and record.
3. Write `test-evidence/slow-members.md` (id/category/reason/date).
4. Apply `@pytest.mark.slow` to the measured members.
5. Author registry↔collect identity guard (no hardcoded count).
6. Author real-tree collection equality + disclosure arithmetic + `--full` restore cases.
7. Run the guard in the default tier and record; confirm it is not itself a member.

### WP-3 — Two-slot commands request the full tier

1. Update `efficiency-model.md` §2 baseline row with `--full`.
2. Update its closure row with `--full`.
3. Update `stage-prompts.md` baseline restatement.
4. Update `stage-prompts.md` closure restatement.
5. Regenerate skill mirrors (`--write --only skills/external`) and run `--check`.
6. Add a doc assertion (guard case) that both owner rows carry `--full`.

### WP-4 — Parallel consistency verification

Write surface: `tests/contract/test_parallel_consistency_contract.py` and `test-evidence/parallel-*`.

1. Author the non-parallel-safe fixture drill (shared-path writer) and prove the comparison reddens.
2. Author the comparison-discipline guard (same-tree, bidirectional, no wall-clock).
3. Run contract-subset default-parallel with `--names-out` (bounded workers).
4. Run contract-subset `--serial`; two-way `comm`; record.
5. Run the no-xdist shim over `tests/contract`; record names list and mode line.
6. Record all commands, exits, durations and lists under `test-evidence/`.
7. Map results to SC-002/SC-003 and leave the closure full-tree comparison to the driver.

### WP-5 — Session scan cache

1. Author the cache guard (build count, consumers, immutability) first.
2. Add the session fixture factory in `tests/conftest.py` with counter and deep copy.
3. Convert `test_coverage_receipt.py` real-repo reads to the session surface.
4. Convert the five real-corpus callers in `test_clause_coverage.py` to the payload.
5. Keep `form_exit_code_table`'s subprocess exit-code leg.
6. Add the tmp-corpus cross-session mutation drill.
7. Run both files before/after; compare pass/fail names; record.
8. Record the traversal/build-count probe output for SC-007.

### WP-6 — Clock injection and event waits

1. Author the sleep-scan guard and exemption registry first.
2. Add `--now` to `feedback-utils.py` (help documented, default off); regenerate the `scripts/` mirror pair after this edit (`sync-mirrors.py --write --only scripts`).
3. Convert the 8 sleeps in `test_client_metrics.py` to injected clock + explicit `os.utime`.
4. Convert `test_feedback_probe_cli.py`'s ordering sleep.
5. Convert `test_store_state_protocol.py`'s two ordering sleeps.
6. Align `wait_until` defaults and adopt it in `test_sdd_loop_efficiency_runner.py`.
7. Replace fixed graces in `test_session_kill_reattach.py` with event predicates.
8. Replace heartbeat waits in `test_line_envelope_contract.py` with event predicates.
9. Run the guard + the six scope files; record before/after wall pair for `test_client_metrics.py`.

### WP-7 — In-process conversion infrastructure and contract-area groups

1. Write the AST scanner that enumerates `subprocess.run` sites under `tests/`.
2. Write the manifest guard (completeness + revert-red) against the scanner.
3. Add the in-process engine invocation helper (importlib load + stdout/stderr capture + exit code).
4. Pilot-convert one contract file with local `_run` wrappers; run before/after equivalence.
5. Convert contract-area engine groups A (goal/flow/concurrency/confirmation engines).
6. Convert contract-area engine groups B (docs/probe/trigger/summary engines).
7. Convert contract-area engine groups C (mirror/measure/state engines) where non-boundary.
8. Record keep rows with boundary classes for the contract-area fixture/copy cases.
9. Fill the manifest rows for all converted and kept sites in these groups.
10. Run the guard and the converted files; record equivalence evidence.

### WP-8 — In-process conversion: integration/unit areas and evidence

Write surface: the integration/unit files enumerated by the WP-7 scan (grouped into at most 10 file
groups), `tests/conftest.py` only if the scan reveals a cwd-independent fixture call, and
`test-evidence/inprocess-conversion.md`.

1. Convert the integration-area docs-scenario group's non-boundary engine calls (file list from the WP-7 scan).
2. Convert the integration-area evidence-lane group's non-boundary engine calls (same source list).
3. Convert the unit-area engine-call group (same source list).
4. Record integration/unit keep rows (venv installs, `ps`/signal, different interpreter, copy topology).
5. Run the guard over the full manifest; fix any unclassified site.
6. Revert one converted point as a drill; capture the red guard output; restore.
7. Record equivalence evidence for both areas.
8. Update the manifest's evidence pointers.
9. Run the complete manifest guard once; record.

### WP-9 — Measurement, forbidden shortcuts, interface evidence

1. Run the baseline slot with `--full --names-out`; record.
2. Measure the default-tier wall on the same host/day; record the ratio.
3. Record the anti-measurement (slow members re-merged) disclosure.
4. Produce the SC-001 collection diff against the implement-start baseline.
5. Run the SC-010 diff scan (skip/xfail/retry/parametrize removals = zero).
6. Run the SC-011 interface cases (`--help` lists `--full`, `--version`, undeclared option).
7. Write the `test-evidence/` index linking each SC to its evidence path.

## Execution Record

- **One-shot assessment**: class `concurrent-by-default` (command body), carrier probe via
  `concurrency-check.py`; duty partitioned into six authoring units (research, decisions, data model,
  contracts, quickstart/feature-ref, plan/verification).
- **Partition outcome**: six authoring units with strict dependency edges — U1 research (settled:
  `research.md`) → U2 decisions R-1…R-10 (settled: same file) → U3 data model (settled: `data-model.md`) →
  U4 contracts (settled: `contracts/`) → U5 quickstart + feature-ref (settled: both files) → U6 plan +
  verification (settled: this file and `test-evidence/plan-verification.txt`). At dispatch time every unit
  had an unsatisfied predecessor edge, so the execution shape is **serial** with reason
  `dependency-edge`.
- **Reading triple**: `requested=24` (from the run's spine `agent_concurrency_requested`), `effective=0`
  (no dispatched units exist, so the interval-overlap computation over an empty unit set is 0; the literal
  `not_evaluated` applies only to a dispatched unit missing its interval, of which there are none),
  `effective_reason=dependency-edge: U2 blocked on U1, U3 on U2, U4 on U3, U5 on U4, U6 on U5; each
  predecessor's completion is the named artifact pointer; host-native fan-out is not a carrier and is not
  counted`. The record claims no concurrency.

## Risks

| # | Risk | Mitigation |
|---|------|------------|
| R-1 | The exclusion enumeration adds ~2 s to every default run | Measured and disclosed; it buys the marked-set arithmetic and is dwarfed by the reclaimed slow-test time |
| R-2 | Two pre-existing failures (c5, c10) appear in every full run | Compared by name only; the closure comparison treats equal names as unchanged (parallel-consistency C-004) |
| R-3 | Writing files under `.specify/specs` during a full run flips `test_c20` | Evidence lands outside the corpus during runs and is copied afterward; the driver's `--names-out` is written post-pass |
| R-4 | `--now` widens a shipped engine's CLI | Default-off byte-equality regression + help documentation + T-002 revision trigger |
| R-5 | Converting a boundary call weakens a contract test | Closed keep classes, manifest guard, equivalence runs, and the inprocess-conversion C-007 revert-red leg |
| R-6 | A converted test still sleeps elsewhere in its file | The scan guard is AST-based over the whole scope file, not per converted test |
| R-7 | A slow-marked test is also `serial` and drifts out of both fast passes | Dedicated tier case 7 covers the serial+slow intersection |
| R-8 | The session cache returns a stale payload inside one session after a corpus write | Mutable writers are excluded by scan-cache C-005; the cross-session drill proves freshness; `test_c20` stays cache-free |
| R-9 | The conversion census and the manifest disagree after edits | The guard re-scans source and treats the manifest as incomplete when a site is unclassified |
| R-10 | Full-tree closure comparison is mistaken for a budget slot | parallel-consistency C-007/C-010 and the driver's efficiency-model §2.5 keep the validation run out of the ledger |
