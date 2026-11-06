# Review Report — 085-sdd-temporary-goal-team

## 0. Portable Project Context

| Field | Value |
|-------|-------|
| Repository | spec-kit |
| Branch | `085-sdd-temporary-goal-team` |
| Base commit | `97995525` (updated trunk after the remote 084 line) |
| Head | `2cb68c44` (feature commit; record updates follow) |
| Review date | 2026-11-06 |
| Reviewer | Qoder agent (session) |
| Environment | Linux x64, Python 3.11.11, pytest 8.4.2 |
| Flow class | execution |

**Artifact inventory**: requirements.md (50 FR / 10 SC), plan.md (19-principle check, 3 decision tensions, 4 execution premises), research.md (R1–R8), data-model.md (E1–E8 + V-1…V-24), contracts/ (5 files, 65 clauses), quickstart.md (S1–S6), feature-ref.md (20 delivery rows), tasks.md (26 rows), verification.md, checklists/requirements.md, test-evidence/ (requirements/plan/tasks gates, smoke, full-suite).

**Reachability**: the head is `2cb68c44`; the code delta is `97995525..2cb68c44`. The review was produced before the commit, so the code segment remains `not-evaluated`; the commit is now available for a follow-up code review.

## 1. Process Execution Timeline

1. Requirements authored and validated (`validate-requirements.py` status ok, 0 error / 0 warning; `pre-analyze-check.py --stage requirements` pass).
2. Clarifications recorded in requirements § Clarifications (scope/hierarchy, lifecycle, stage agents, 500 budget, per-agent worktrees, generic executor removal, concurrency 24).
3. Plan + research + data-model + 5 contracts + quickstart + feature-ref authored; `pre-analyze-check.py --stage plan` pass; FR clause coverage 50/50.
4. Tasks authored; `validate-tasks.py` 0 error / 0 warning; `pre-analyze-check.py --stage tasks` pass; clause coverage 65/65; decomposition `proceed` (50 FR / 26 tasks).
5. Implementation: scope resolver, temporary goal/team, stage agents + generic executor removal, child lines + integration queue, wp-gate extensions, checkpoint protocol and rollback drill.
6. Smoke 43/43 pass; full suite 7356 passed / 25 failed / 1 skipped (excluding the Docker/Hugo test). The 085-introduced guard failures were fixed; the remaining 24 are pre-existing/environmental and reproduce at `aafbf5a8`.

## 2. Findings Summary

| ID | Severity | Category | Summary |
|----|----------|----------|---------|
| F1 | P2 | Workflow | The working tree is uncommitted, so the code segment cannot review a committed `base..head` delta; this review records `not-evaluated` rather than claiming a code verdict. |
| F2 | P2 | Automation | The full suite has 24 pre-existing/environmental failures (Docker/Hugo test excluded separately); they are not caused by 085 but make a clean-suite claim impossible. |
| F3 | P2 | Documentation | The 083 GM-03 allowed set was extended with 22 085 in-unit rows so the cross-feature containment guard stays decidable; this is a deliberate baseline record, not a silent exception. |
| F4 | P3 | Workflow | No live unattended driver run with the temporary team was executed; SC-010 is honestly `partial` (supporting path). |

### 2.1 Code Segment (Verdict and Pointers)

- triage: `not-evaluated` — this report was produced before the commit; the delta `97995525..2cb68c44` is now committed and can be reviewed in a follow-up run.
- basis: review produced pre-commit; the current commit is `cbbf6dda`.
- record: no `code-review.md` is created for a non-`run` triage; this subsection is the carrier.
- no `blocking` entry exists; the non-conclusion is disclosed, not a pass over code.

### 2.2 Artifact Review Segment

- coverage: 7 / 7 expected standard members present (`requirements.md`, `plan.md`, `tasks.md`, `contracts/`, `data-model.md`, `quickstart.md`, `verification.md`), plus `research.md`, `feature-ref.md`, `checklists/requirements.md`.
- traceability: 50/50 FRs cited from contract citation groups; 65/65 clauses claimed by task rows; every SC has a verification row.
- findings: none new. F3 is a baseline-record disclosure, not an artifact defect.

### 2.3 Implementation Review Segment

- base..head: `97995525..2cb68c44`.
- smoke: `python3 -m pytest -q tests/unit/test_goal_scope_engine.py tests/contract/test_scope_resolution.py tests/contract/test_temp_goal_contract.py tests/contract/test_temp_team_schema.py tests/contract/test_line_registry_child_lines.py tests/contract/test_checkpoint_protocol.py tests/unit/test_wp_gate_085.py tests/integration/test_temp_team_worktree_queue.py tests/integration/test_checkpoint_rollback.py`; exit `0`; evidence `.specify/specs/085-sdd-temporary-goal-team/test-evidence/smoke.txt`.
- live dogfood: two child lines, real worktrees, integration queue, fsck clean; evidence `test-evidence/live-dogfood.txt`, report `team/085-sdd-temporary-goal-team/runs/20261106T024600Z-report.md`, checkpoint `checkpoints/05-live-dogfood.md`.
- scope/regression: the targeted 070/064 suites (1048 cases) pass; mirror checks are clean; the full-suite delta is pre-existing/environmental (F2).
- finding: F1 (uncommitted delta).

### 2.4 Acceptance Reality Check

Copied verbatim from `closure-acceptance-check.py --spec-dir .specify/specs/085-sdd-temporary-goal-team --json`:

`pass [7] · blocked [0] · deferred [0] · partial [0] · fail [0] · unknown [0] · total [7]`

Checker verdict: `accept`; claim: the final-path criteria are all pass; claim comparison: `agree`.

## 3. Findings

### F1 — Code segment was produced pre-commit

- **Why**: this report was written while the tree was uncommitted; the code segment therefore recorded `not-evaluated`.
- **Status**: resolved by commit `2cb68c44`; a follow-up `/speckit.review` can run the code segment against `aafbf5a8..cbbf6dda`.

### F2 — Pre-existing full-suite failures

- **Why**: 24 failures reproduce at `aafbf5a8` (8 representative cases re-run in a detached worktree) or are in the 083 baseline; they are environmental/stale-pin failures, not 085 defects.
- **Proposed fix**: handle them in a separate maintenance feature; do not fold them into 085.

### F3 — 083 GM-03 baseline extended

- **Why**: the cross-feature containment guard needs every 085 in-unit path registered; the 22 rows are the deliberate baseline record.
- **Proposed fix**: none for this feature; a future cleanup can move the allowed set to a dedicated 085 record.

### F4 — No live driver dogfood

- **Why**: the component tests prove the mechanisms, not a live unattended driver run.
- **Status**: a bounded live dogfood executed (two child lines + worktrees + queue + checkpoints); the full 8-stage driver chain remains the unblocking step for SC-010.

## 4. What Worked — Preserve

- One scope resolver owned by `goal-utils.py`; all consumers reuse it.
- Temporary Goal/Team are spec-local and do not touch the global stores.
- Stage-specific agents replace the generic executor; the role grammar keeps the roster dynamic.
- Child lines reuse 064's worktree/integration queue; the two-child fixture merges in declared order with no lost work.
- The checkpoint protocol and rollback drill are byte-restorable, not prose-only.

## 5. Recommendations

1. Commit the 085 change set (F1) and re-run the code segment.
2. Run a live temporary-team dogfood (F4).
3. Track the 24 pre-existing failures as a separate maintenance item (F2).
4. When a future feature extends GM-03 again, add a dated sub-registration instead of editing 083 rows (F3).

## 6. Priority Roadmap

| Priority | Action |
|----------|--------|
| P1 | Commit the change set and re-run `/speckit.review` for the code segment. |
| P2 | Run the live temporary-team dogfood to close SC-010. |
| P3 | Separate maintenance for the pre-existing full-suite failures. |

## 7. Self-Containment Check

- All cited evidence paths are repo-relative and exist (except the intentionally absent code-review record for a non-`run` triage).
- No local-only URL is used; the head is the working tree, disclosed.
- The report does not reproduce artifact bodies; it cites paths and verdicts.

## 8. Feedback

- Framework friction: the pre-existing full-suite failures make a clean-suite claim hard; the Docker/Hugo test is environment-blocked.
- 085-specific friction: the 083 GM-03 guard requires a cross-feature baseline extension for every new in-unit file; a dedicated per-feature allowed-set record would be less coupled.
