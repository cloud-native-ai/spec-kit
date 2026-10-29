# Feature Reference — 070

**Requirement key**: `070-subagent-task-teams`
**Bound Feature**: **Feature 070** — 驱动子代理的任务拆解与配合机制（Task Decomposition & Team Coordination for Subagent-Driven SDD）
**Status at plan**: Draft → **Planned** (`/speckit.implement` owns the move to Implemented)
**Spec**: `.specify/specs/070-subagent-task-teams/requirements.md`
**Plan**: `.specify/specs/070-subagent-task-teams/plan.md`

## 1. Mapping to the Feature Index

| Dimension | Mapping |
|-----------|---------|
| Feature row | `.specify/memory/features.md` row `070` (Draft → Planned at this plan) |
| Feature detail | `.specify/memory/features/070.md` (Latest Review / Key Changes / Implementation Notes updated by the plan) |
| Related features | 058 (loop U0–U6, spine, sentinels, U4 — preserved), 060 (`run-agent` dispatch — reused), 061 (`CAPABILITY_MATRIX` — read-only), 063 (fast lane, test budget, plan constraint, detach — preserved), 064 (line registry, Ownership Manifest, worktree, integration queue — reused read-only), 067 (part brief, dispatch log, test economics — extended), 068 (exec-quant channel — preserved) |
| Team substrate | `create-team` / `run-team` vocabulary is consumed through a schema-compatible preset; neither skill is modified |

## 2. Delivered Surface (planned)

All paths are framework-source paths. The `.specify/skills/sdd-loop-driver/` copies of the changed driver files are **generated mirrors** and are never hand-edited.

### New files

| Path | Change | Purpose |
|------|--------|---------|
| `skills/external/sdd-loop-driver/references/decomposition-model.md` | new | Runtime owner: WP model, plan/ledger, scheduler, verification, integration, retry, metrics, opt-out |
| `skills/external/sdd-loop-driver/templates/stage-team-preset.md` | new | Schema-compatible stage-team preset (four seats, pattern rules) |
| `skills/external/sdd-loop-driver/scripts/wp-gate.py` | new | Deterministic decomposition gate (`--check plan|preflight|retry`) |
| `skills/external/sdd-loop-driver/scripts/wp-report.py` | new | Deterministic coordination report and metric derivation |
| `tests/fixtures/wp_fixtures.py` | new | Plan/spine/manifest/ledger builders for tests |
| `tests/fixtures/wp_driver_sim.py` | new | Deterministic simulator of the declared scheduler for dry runs |
| `tests/unit/test_wp_gate.py` | new | Gate check coverage (plan, preflight, retry) |
| `tests/unit/test_wp_report.py` | new | Metric derivation and `not_evaluated` coverage |
| `tests/contract/test_sdd_loop_driver_wp_model.py` | new | WP-01…WP-18 pins |
| `tests/contract/test_sdd_loop_driver_wp_gate.py` | new | WG-01…WG-18 pins and stdlib guard |
| `tests/contract/test_sdd_loop_driver_wp_coordination.py` | new | SD-01…SD-16 and FN-01…FN-16 pins |
| `tests/contract/test_sdd_loop_driver_wp_preset.py` | new | ST-01…ST-12 pins |
| `tests/contract/test_non_regression_070.py` | new | 058/063/064/067/068 non-regression pins |
| `tests/contract/test_wp_mutation_drills.py` | new | Mutation drills proving the guards go red |
| `tests/integration/test_wp_coordination_dry_runs.py` | new | Concurrent read-only, write serialization, ownership rejection, deterministic integration, failure isolation, fallback, no nested driver, no team directory |

### Modified files

| Path | Change | Purpose |
|------|--------|---------|
| `skills/external/sdd-loop-driver/SKILL.md` | new H2 section + pointers | Entry to the decomposition layer; no rule duplication |
| `docs/reference/skills/sdd-loop-driver.md` | new section | User-facing entry, pointers only |
| `tests/contract/test_sdd_loop_driver_skill.py` | pin update | Intentional H2 set update for the new SKILL section |

### Generated (not hand-edited)

| Path | Generator |
|------|-----------|
| `.specify/skills/sdd-loop-driver/SKILL.md` and the mirrored new files | `scripts/python/sync-mirrors.py` (`skills/external` → `.specify/skills`) |

No new command template, agent role, engine, dependency, service, daemon, model API, registry, ownership model, integration queue, brief format, ledger, or persisted team directory is added. The feature registry row and feature detail update required by the `data-model.md` E13 `plan` inventory are governance bookkeeping outside FR-027's delivery surface (they are neither driver source, documentation page, nor canonical test suite).

## 3. FR Coverage

| FR group | Owning contract clauses |
|----------|-------------------------|
| FR-001…FR-005 (model and gate) | WP-01…WP-18; WG-06…WG-13; FN-04…FN-08 |
| FR-006…FR-009 (team mapping and preflight) | ST-01…ST-12; WG-14…WG-16; SD-04; SD-14 |
| FR-010…FR-015 (dispatch and coordination) | SD-01…SD-16; WP-09; WP-10; WP-12 |
| FR-016…FR-019 (verification and integration) | VI-01…VI-14 |
| FR-020…FR-023 (observability and metrics) | OR-01…OR-13 |
| FR-024…FR-027 (compatibility and fallback) | FN-01…FN-16; ST-09…ST-12 |
| FR-028…FR-030 (tests and evidence) | FN-14…FN-16 |

Every FR is covered; no FR is re-owned from a predecessor feature.

## 4. Success Criteria Coverage

| SC | Evidence plan |
|----|---------------|
| SC-001 | Benchmark record from spine timestamps and `wp-report.py` outputs; the comparison uses the OR-04 interval against the conservative plan-70/review-37 anchor; a median requires ≥3 comparable samples; otherwise `not_evaluated`; closure needs met evidence or a recorded user waiver naming SC-001. No claim from this plan run. |
| SC-002 | Stage dispatch attempts (one per `(stage, stage_attempt)` pair, not plan events) from the same benchmark record, divided by 8; at most 1.5 and ≥40% below the 2.6× baseline; otherwise `not_evaluated`; closure needs met evidence or a recorded waiver. |
| SC-003 | Stage sentinel and U4 in the non-regression tests; name-level failure set from `run-tests.sh --names-out` at implement baseline and closure. |
| SC-004 | `wp-gate --check preflight` ownership/output checks plus dry-run ownership-violation case; fixture asserts zero orphan outputs (including the `integrator_outputs` assignment) and zero out-of-territory writes. |
| SC-005 | Every stage's plan fence carries the decision, reason, and gate verdict per FN-08; the ledger `plan` event references the fence; dry-run asserts no silent partial run. |
| SC-006 | Manual-intervention count and the run's driver-session count recorded at run close; benchmark record compares the per-session rate against 30/29; `not_evaluated` when either input is unavailable. |
| SC-007 | `wp-report.py` outputs; dry-run asserts the overlapping-interval test; a claim without two overlapping intervals is invalid. |
| SC-008 | Dry-run suite plus non-regression suite; each record carries command, exit code, pass/fail counts, changed paths, and an evidence pointer. |

## 5. Overlap Declaration and Adjudication

**Declared shared delivery surface (current feature)**: the specific modified and new file paths listed in § 2 under the driver skill directory, plus the driver documentation page. The declaration is file-level, not a whole-directory claim; test paths and spec-local paths are not part of the shared delivery surface.

**Deterministic check**: `python3 /home/agent/sdd-070/tools/overlap-check.py --spec-dir .specify/specs/070-subagent-task-teams --repo .`

**Recorded result** (2026-10-24, exit 1): `decision=overlap`, 21 relations against 11 predecessor specs — 15 `same-path` and 6 `nested-path`. The relations fall into three groups: the driver `SKILL.md` (9 same-path predecessors plus 1 nested relation from 067's historical whole-directory declaration), the driver documentation page (6 same-path predecessors plus 1 nested relation from 056's `docs/reference` declaration), and the four new driver files (4 nested relations from 067's historical whole-directory declaration). The raw JSON and the full table are stored in `test-evidence/overlap-plan.json` and adjudicated in `notes/overlap-adjudication-plan.md`.

**Adjudication**:

| Overlapping path group | Other features | Owner for this change | Disposition |
|------------------------|----------------|-----------------------|-------------|
| `skills/external/sdd-loop-driver/SKILL.md` | 058, 059, 060, 062, 063-review-p1-governance, 075-sdd-loop-efficiency, 064, 065, 066 (same-path); 067 (nested whole-directory declaration) | 070 for the new section; predecessor sections unchanged | Additive edit only; no predecessor rule is redefined; non-regression tests pin their behavior |
| `docs/reference/skills/sdd-loop-driver.md` | 056 (nested `docs/reference` declaration); 058, 060, 075-sdd-loop-efficiency, 064, 065, 066 (same-path) | 070 for the new section; predecessor sections unchanged | Additive documentation entry with pointers only |
| `skills/external/sdd-loop-driver/references/decomposition-model.md`, `.../scripts/wp-gate.py`, `.../scripts/wp-report.py`, `.../templates/stage-team-preset.md` | 067 (nested whole-directory declaration) | 070 (new files) | No content conflict: 067 touched no file at these paths; its delivered files remain untouched |

No live concurrent writer exists: every overlapping predecessor's commits are already in the base history (`git log --grep` finds them on `master`), and 070 is the only active line. The administrative index status of a predecessor is not the test — its code being merged into the base is. No ownership transfer is required for a registry, ownership model, integration queue, or ledger — 070 creates none. The check therefore does not require a second adjudication round; it requires the recorded disposition above, and implementation must re-run the check after the first driver-source edit to confirm no new overlap beyond these known same-path relations.

**Interpretation note (disclosed)**: a literal `clear` is not achievable for an additive change to an already-delivered skill surface, because the deterministic check compares paths, not time. The ratified adjudication from `notes/clarify-decisions.md` D9.2 already treats same-skill sequential evolution as non-conflicting; this plan extends that ruling to 063 and 065 and records it rather than narrowing the declaration to manufacture a green result.

## 6. Non-Goals Preserved

- No nested driver or second orchestrator; no subagent loads `sdd-loop-driver`.
- No change to stage command internals, sentinel literals, U4 semantics, or quality gates.
- No second line registry, ownership model, worktree model, integration queue, ledger, or brief format.
- No parallel write packages; read-only parallelism only.
- No persisted `.specify/teams/<slug>/team.md`; no `create-team`/`run-team` modification.
- No `continuous` pattern, long-lived team loop, service, daemon, external dependency, or model API.
- No push, force merge, or confirmation-gate bypass.

## 7. Mirror Obligations

**Pointer only**: the mirror source/mirror/verify obligations are owned by `plan.md` § Mirror Obligations, which is the sole authoritative copy of the table (Constitution XIV). This section records no separate table; `tasks.md` § Mirror Obligations and the runtime owner document reference the plan owner as well. `docs/` and `tests/` have no mirror, and `.specify/skills/sdd-loop-driver/` is regenerated by the existing generator, never by hand.
