# Analyze Repair Record — Feature 070

**Date**: 2026-10-25
**Stage**: analyze-repair (one bounded repair round after the analyze gate)
**Authority**: `test-evidence/analyze-report.md` — verdict NOT READY, 1 CRITICAL + 7 HIGH after independent validation
**Scope**: spec-only. No implementation code, no full test suite, no implement start.
**Frozen counts**: 30 FR / 8 SC / 39 task rows — unchanged; no task row added, removed, or renumbered.

## Plan revision declaration

This repair is authorized as a **plan revision** under the 063 plan-constraint branch (a). The analyze-repair plus the re-run analyze serve as the plan re-review. The plan-owned edits below are all classified **substantive** because they change authored design/owner statements, not typo-level wording.

```text
PLAN-EDIT: .specify/specs/070-subagent-task-teams/plan.md — analyze findings C-01, G-01, A-01, A-02, A-03, A-18; 分类=substantive
PLAN-EDIT: .specify/specs/070-subagent-task-teams/research.md — analyze findings C-01, A-01, A-02, A-03; 分类=substantive
PLAN-EDIT: .specify/specs/070-subagent-task-teams/data-model.md — analyze findings C-01, I-02, A-02, A-03, G-01, A-15; 分类=substantive
PLAN-EDIT: .specify/specs/070-subagent-task-teams/contracts/work-package-model.md — analyze findings C-01, I-02, A-02, G-01, A-15; 分类=substantive
PLAN-EDIT: .specify/specs/070-subagent-task-teams/contracts/wp-gate.md — analyze findings I-02, G-01, A-15; 分类=substantive
PLAN-EDIT: .specify/specs/070-subagent-task-teams/contracts/observability-and-retry.md — analyze findings A-01, A-02, A-03, A-15, A-18; 分类=substantive
PLAN-EDIT: .specify/specs/070-subagent-task-teams/contracts/verification-and-integration.md — analyze finding G-01; 分类=substantive
PLAN-EDIT: .specify/specs/070-subagent-task-teams/contracts/fallback-and-nonregression.md — analyze finding I-02; 分类=substantive
PLAN-EDIT: .specify/specs/070-subagent-task-teams/quickstart.md — analyze finding A-03; 分类=substantive
PLAN-EDIT: .specify/specs/070-subagent-task-teams/feature-ref.md — analyze findings C-01, A-01, A-02, A-03, G-01, I-02, L-01; 分类=substantive
```

The transport spine (`/home/agent/sdd-070/spine-070.md`) carries the matching `plan_revision` entry with the finding ids, the commit hash, and the re-review statement.

## Blocking findings (all repaired)

### C-01 (CRITICAL) — duplicate authored owners

- `plan.md` § Mirror Obligations now declares itself the **sole mirror owner**; `feature-ref.md` §7 is a pointer with no table; `tasks.md` § Mirror Obligations and the runtime owner document point to the same owner.
- `data-model.md` E13 now declares itself the **sole required-output inventory owner**; `research.md` R18 is a dated rationale with no table; WP-15 points to E13; T012 instructs the runtime doc to reference the owner and not restate either inventory.
- `plan.md` Phase 1 summary no longer assigns mirror obligations to `feature-ref.md`; it records both pointer relationships.
- T033 gains the owner-agreement check (only complete mirror table, only complete inventory, pointers name the owners, runtime doc restates neither) without adding a task row.

### I-02 (HIGH) — SC-005 decision vocabulary

- SC-005 now uses the four values (`decomposed`, `single-package`, `disabled`, `fallback`), names the **plan fence** as the canonical decision record, and requires the ledger `plan` event to reference it.
- Gate verdict per value is owned by FN-08 (`admit`, `single-package`, literal `no-gate-run` for `disabled`/`fallback`); E2/V-DEC.7 project it; WP-13 and WG-18 point to FN-08; plan, feature-ref, and T035 reference the owner.

### A-01 (HIGH) — SC-001 baseline and interval

- SC-001 now uses the A5/OR-13 conservative anchor (plan 70 min → ≤56 min; review 37 min → ≤29.6 min), the exact FR-022/OR-04 interval (first package dispatch to stage U4 completion), and the same-interval comparison basis.
- At least three comparable samples on the same host class and topology are required for a median; a re-measured baseline uses the OR-04 interval and replaces the anchor; fewer samples or a mismatch → `not_evaluated`. A5, OR-13, R19, feature-ref, and plan are aligned.

### A-02 (HIGH) — SC-002 numerator and comparator

- The numerator is now **stage dispatch attempts**: distinct `(stage, stage_attempt)` pairs that dispatched at least one package, not `plan` events. A post-repair `plan` event never adds an attempt (OR-07, WP-10, V-CLOSE.3, V-LED.11, plan § 8).
- SC-002 states the comparator explicitly: at most 1.5 (absolute) and at least 40% below the 2.6× worst measured baseline; package retries are reported separately and never enter the numerator (OR-08 preserved).

### A-03 (HIGH) — SC-006 denominator

- The denominator is **per session**: the baseline is 30/29 ≈ 1.03 interventions per session, compared to the same per-session rate.
- The intervention count and the run's driver-session count come from the run record; `--sessions` is an OR-11 input; `sessions` and `manual_interventions_per_session` are E4/E11 fields; FR-022, OR-09, OR-11, OR-12, E12, T028, T038, quickstart Scenario E, and feature-ref are aligned.

### G-01 (HIGH) — integrator output ownership

- FR-003(b) and SC-004 now allow the plan's `integrator_outputs` to be owned by the single integrator seat instead of a package; every other required output is still owned by exactly one package.
- E2 adds `integrator_outputs`; V-PLAN.13 and WG-08 enforce subset/disjointness and exclude those outputs from package coverage; VI-06/VI-11 state the integrator produces them (at minimum clarify's write-back) and stage U4 still verifies them.
- WP-15 and the E13 clarify row are aligned; T022 covers the contract test. No task row was added.

### A-15 (HIGH) — recursive split-retry evasion

- A split is permitted once per lineage. Children **inherit the parent's attempt count**; their sole dispatch is the lineage's retry attempt; split depth is one; a child is never split again or retried, and a child failure goes directly to the stage gate/U5.
- FR-013, A4, the split edge case, WP-08, WG-17, OR-14, OR-15, OR-16, V-AMD.4, V-DELTA.2, V-DELTA.5, and T016/T017 are aligned.
- The budget delta is **strictly greater** in FR-013 and A4, matching OR-15/V-DELTA.3 and the new WG-17 check.

### A-18 (HIGH) — all-`not_evaluated` acceptance consequence

- FR-023 now defines the consequence: an all-`not_evaluated` benchmark blocks closure until a comparable benchmark exists, unless the user records an explicit waiver naming SC-001 and/or SC-002 and its reason; the met result or waiver is carried into verification/closure evidence.
- OR-10, V-REP.7, plan § 8, feature-ref, DoD-4, GATE-8, T038, and T039 are aligned. `not_evaluated` alone never satisfies SC-001/SC-002.

## Coupled MEDIUM/LOW fixes (kept inside the blocking findings' blast radius)

- **I-06**: GATE-2 no longer uses the obsolete `--waive` flags; § Validator Status (post-repair) records the waiver-free raw run.
- **I-07**: T033's `[P]` marker was removed (it is `[blockedBy: T032]`); the Parallel Opportunities text now matches the dependency edges.
- **L-01**: plan.md and feature-ref §2 state that the feature registry row/detail update is governance bookkeeping outside FR-027's delivery surface.
- **L-04**: DoD-5 and the Clause Coverage Model intro now say "at least one contract-test task", and explain WG-18's two pins (T005 CLI envelope, T016 preflight/fallback).

## MEDIUM/LOW dispositions (not expanded in this round)

| ID | Severity | Disposition | Owner / rationale |
|----|----------|-------------|-------------------|
| I-01 | MEDIUM | deferred | Requirements revision: FR-002 `tasks` rule vs the first-slice single-subagent stance (already stated in R18/FR-024/V-RULE.3). |
| I-03 | MEDIUM | deferred | Requirements revision: add "repository-relative" to FR-011 (behavior already fixed by WP-11/VI-02). |
| G-02 | MEDIUM | deferred | Tasks/implement revision: freeze a baseline that can express domain-prefixed clauses and replace T039's id-presence check with a behavior-level assertion; T039 remains the closure net. |
| A-04 | MEDIUM | deferred | SC-007 "ready" is already SD-02; require a design clarification in a later requirements/clarify round. |
| A-05 | MEDIUM | deferred | FR-009 any/all and `parallel_safe` effect; design currently chooses any-one (WG-16) and a concurrency predicate. |
| A-07 | MEDIUM | deferred | Contradictory-output classes; verification contract owner. |
| A-08 | MEDIUM | deferred | Name both dispatch forms / the runner selection rule in FR-010 in a later requirements round. |
| A-09 | MEDIUM | deferred | `driver-u4` naming and the adversarial trigger; requirements/design round. |
| A-11 | MEDIUM | deferred | `on` resolution for every gate outcome; FN-04/V-DEC.4 owner. |
| A-12 | MEDIUM | deferred | Parenthesize the parallelism formula and add attempt identity/`stage_u4_at` to FR-020; adjacent to A-02/A-03 but outside this round's scope. |
| A-19 | MEDIUM | deferred | Dry-run proof scope and scenario-list closure; tests/design round (R4 limitation is disclosed). |
| U-02 | MEDIUM | deferred | Stage-specific size ceiling for `artifacts`/`acceptance`; WP-09/WG-09 owner. |
| U-04 | MEDIUM | deferred | Gate repair budget/second-reject outcome in FR-003/A12; design already says one repair then fallback. |
| U-05 | MEDIUM | deferred | Evidence-loss fallback decision rule and the unrepresentable-contract cause; FN-06/VI-04 owner. |
| U-06 | MEDIUM | deferred | Closed topology set and materiality rule in FR-013; OR-15 lists the set. |
| U-07 | MEDIUM | deferred | U4-failure commit disposition and empty-commit rule; FR-018/VI owner. |
| U-08 | MEDIUM | deferred | Integrator as sentinel emitter for decomposed stages vs 058's stage prompt; requirements/058 interface round. |
| I-05 | MEDIUM | deferred | Define "auto-merge" as package-level only; FR-019/VI-14 owner. |
| I-06 | MEDIUM | **fixed** | Tasks-file truthfulness, coupled to T033/GATE edits. |
| I-07 | MEDIUM | **fixed** | Tasks-file parallel/dependency contradiction. |
| F-01 | MEDIUM | deferred | Feature registry owner: index row/detail refresh belongs to the next lifecycle command (`/speckit.implement`), not this repair. |
| G-03 | MEDIUM | accepted | Overlap re-check obligation is already carried by `research.md` R20 item 3 and `feature-ref.md` §5; no task row added (40-row ceiling). Implementation executes the re-check after the first driver-source edit. |
| L-01 | LOW | **fixed** | Delivery-surface note added with C-01's pointer edits. |
| L-02 | LOW | deferred | Red-first evidence field list is owned by FN-15; task text already carries command/output/rc. |
| L-03 | LOW | deferred | FR-025 preservation clause for 060/061; requirements revision. |
| L-04 | LOW | **fixed** | Clause-coverage wording corrected. |
| I-04 | rejected | no action | The analyze appendix's rejected claim; the cited contract reconciles the rules. |

## Validation (re-run 2026-10-25)

| Check | Command | Result |
|-------|---------|--------|
| Requirements validator | `python3 scripts/python/validate-requirements.py .specify/specs/070-subagent-task-teams/requirements.md --json` | rc 0, `status=ok`, 0 errors / 0 warnings, 320 lines / 38 definition rows (`test-evidence/analyze-repair-validate-requirements.json`) |
| Tasks validator | `python3 scripts/python/validate-tasks.py .specify/specs/070-subagent-task-teams/tasks.md` | rc 0, 0 errors / 0 warnings (`test-evidence/analyze-repair-validate-tasks.txt`) |
| Decomposition gate (plan) | `python3 /home/agent/sdd-070/tools/decomposition-check.py --mode plan --requirements .specify/specs/070-subagent-task-teams/requirements.md` | rc 0, `proceed`, fr_count 30 / ceiling 30 (`test-evidence/analyze-repair-decomposition-plan.txt`) |
| Decomposition gate (tasks) | `python3 /home/agent/sdd-070/tools/decomposition-check.py --mode tasks --requirements … --tasks …` | rc 0, `proceed`, fr_count 30, task_count 39 / ceiling 40 (`test-evidence/analyze-repair-decomposition-tasks.txt`) |
| Pre-analyze | `python3 /home/agent/sdd-070/tools/pre-analyze-check.py --spec-dir .specify/specs/070-subagent-task-teams --stage tasks --repo .` | rc 0, `decision=pass`, errors 0, waived 0, advisories 118 (all `missing-path` for planned deliverables), fr 30 / sc 8 / tasks 39 / clauses 110 (`test-evidence/analyze-repair-pre-analyze.txt`) |
| Overlap | `python3 /home/agent/sdd-070/tools/overlap-check.py --spec-dir .specify/specs/070-subagent-task-teams --repo .` | rc 1, `decision=overlap`, 21 relations (15 same-path + 6 nested-path) against 11 predecessor specs; **identical to the adjudicated Groups A–C** (`test-evidence/analyze-repair-overlap.txt`) |

**Overlap comparison**: Group A = `skills/external/sdd-loop-driver/SKILL.md` (9 same-path + 1 nested); Group B = `docs/reference/skills/sdd-loop-driver.md` (6 same-path + 1 nested); Group C = the four new driver files (4 nested). No relation outside A–C exists, so no unadjudicated relation blocks.

**Counts confirmed**: 30 FR / 8 SC / 39 task rows; 110 contract clauses; no new task row.

## Test budget

Docs-only stage: the full suite was not run (the two slots remain the implement baseline T002 and closure T039). The E3 transport row is `status=not-run-docs-only` in `test-evidence/analyze-repair.jsonl`.

## Anomaly

None. The overlap rc 1 is the already-adjudicated state, not a new relation; the plan-owned edits are declared above and in the transport spine.
