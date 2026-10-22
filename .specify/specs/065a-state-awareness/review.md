# SDD Process Review — 065a-state-awareness

**Date**: 2026-10-22
**Branch**: `065-loop-interruption-recovery` (43 commits ahead of `master`; no merge/push performed)
**Review scope**: `.specify/specs/065a-state-awareness` (Feature 065 active slice). Parent 065 and archived 066 are context only; 067 is a process-improvement reference, not a review target. Read-only review; no pytest run, no subagents, no code/spec edits.
**User test waiver (verbatim)**: 「用户已显式授权**忽略测试**：不要运行/修复完整 pytest 套件，不追求红转绿；只做 docs/镜像/verification/gates 与 smoke。」 Implement-stage variant recorded at `notes/red-first-evidence.md:268`: 「以忽略测试的方法尽快完成当前的sdd周期」.

## Verdict

**PASS WITH WAIVER** — 0 P0. The 065a implementation, owner reference, docs, mirrors and deterministic gates are present and internally consistent at the requirement level. The 26-test acceptance surface is explicitly waived, never reported as passing. Three P1 evidence/process defects are non-functional and fixable by a docs-only commit; none blocks a waiver-based merge.

## Findings

| ID | Severity | Finding | Evidence | Disposition |
|----|----------|---------|----------|-------------|
| P1-01 | P1 | Full pytest suite not run; DoD-4 unmet, GATE-3 `waived/void`; 26 tests last observed red (T015×18, T016×5, T018×3); SC-006 and T027 NEW-failure count are `not-evaluated`, not 0. This is the central accepted risk of the test waiver. | `verification.md:8-14,52,87,99,104`; `tasks.md:27,33` | **Accepted-risk** under the user's explicit waiver. Merge may proceed only as "implementation-complete with test waiver", never as test-verified. |
| P1-02 | P1 | Test-status wording overstates what was measured: `tasks.md` says "红用例未修复" and `verification.md` says "26 个红测试保持", but the last pytest run (`35aa0192`, 26 failed / 57 passed) predates the T015–T018 implementation; no post-implementation run exists. Current red/green is unknown, so "未修复" is an unmeasured negative claim (the mirror image of a false green). | `tasks.md:27,172,173,175,179,215`; `notes/red-first-evidence.md:266-281`; `verification.md:12,104` | Reword to "last observed 26 failed before T015–T018; not re-run; current red/green not evaluated". No code change; correct before or immediately after merge. |
| P1-03 | P1 | `tasks.md` T015 evidence contradicts the shipped code and owner reference: it says the C-47 cap only rewrites `resume`/`retry` and an existing `stop` keeps its own reason. The engine applies the cap to `stop` as well, and the reference states the original reason yields to `attempts-exhausted`. Commit `12294c0e` fixed code/reference/red-first but missed this task line. | `tasks.md:172`; `skills/external/sdd-loop-driver/scripts/loop-state.py:1790-1798`; `skills/external/sdd-loop-driver/references/state-awareness.md:149` | Correct the task evidence sentence to the literal C-47 reading. Behaviour itself is contract-conformant; no functional blocker. |
| P2-01 | P2 | C-47 reason masking: at `attempt >= retry_limit`, every `stop` candidate is relabelled `attempts-exhausted`, including row 2 `remote-unreachable`, row 3 `evidence-gap`, row 11 `stalled-handoff` and row 13 fallback. The root cause survives in `loop_state_reason` and `interruptions[]`, but the action reason no longer names it. | `loop-state.py:1790-1798`; `references/state-awareness.md:149`; `contracts/interruption-and-action.md:77` | Accept for 065a (literal owner text). 065c must read `loop_state_reason`/`interruptions[]` before executing `stop`, or the contract should add a preserved-original-reason field. |
| P2-02 | P2 | RP-1 (directory artifact `contracts/` now resolves against the slash-less git pathspec) is smoke- and self-test-verified only; no pytest run confirms no hidden unit assertion depends on the old behaviour. | `verification.md:106-112`; `notes/quickstart-run.md:77-83`; `loop-state.py:1301-1335` | Do not revert without re-reading C-59. Re-run the directory-artifact and uncommitted-artifact tests when pytest is restored. |
| P2-03 | P2 | Feature 065 correctly remains `Planned` (065b/065c queued), but the implement-stage feature-integration record was not discharged: `features/065.md` Latest Review/Last Updated (2026-10-21) stops at tasks and does not record 065a implementation-complete, the waiver, or the 30/30 closure. Commit `0860092a` touches no `features*` file. | `.specify/memory/features.md:74`; `.specify/memory/features/065.md:5,69` | Append a dated 065a progress note while keeping Status `Planned`; do not flip the umbrella to `Implemented`. |
| P2-04 | P2 | Contract ambiguity: C-36 reads absolutely ("spine missing after dispatch ⇒ UNKNOWN + stop"), while C-37/C-38 put watcher-verbatim precedence ahead of the derived short-circuits. The engine follows C-38 (watcher wins when `watch_verdict.present=true`). | `contracts/interruption-and-action.md:30,34-35`; `loop-state.py:1514-1523` | Clarify C-36 as applying only when no watcher verdict exists; align the contract in a later revision. Not an implementation defect. |

## Implementation State

- **Tasks**: 30/30 `[X]`, 0 open/claimed/deferred (`grep` re-run: 30 closed, 0 other sigils). Several `[X]` rows (T019–T021, T024, T026–T027) are closed under the waiver, not by test-verified execution; the verification states this.
- **Artifacts exist**: `skills/external/sdd-loop-driver/scripts/loop-state.py` (118 KB), `references/state-awareness.md`, `SKILL.md` Hard Requirement 8, `docs/reference/skills/sdd-loop-driver.md` §状态感知快照, and all three `.specify/skills/sdd-loop-driver/` mirrors.
- **Deterministic gates re-run in this review**: `validate-tasks.py` PASS 0/0; `pre-analyze-check.py --stage tasks` `decision=pass errors=0 advisories=0 (fr=25 sc=6 tasks=30)`; `account-clause-coverage.py` `claimed 60 / FR 25 of 25 / uncovered 0 / status ok`; `sync-mirrors.py --check` `ok … (28 files)`; three source/mirror pairs `cmp` IDENTICAL; `watch-target.sh --self-test` 38/0; `loop-state.py --self-test` 36/0. These match `verification.md` §T030.
- **Feature status**: Feature 065 is `Planned` in `features.md` and `features/065.md`; that is correct because 065b (watchbeat write / heartbeat-stalled / lifecycle-spine-violation) and 065c (recover / salvage persistence / isolation) are not done. The gap is the missing progress record (P2-03), not a wrong status.
- **Forbidden surfaces**: no diff against `watch-target.sh`, `line-registry.py`, `templates/commands`, `.specify/templates`, `pyproject.toml`, 066/067/068, or the parent 065 directory across the 065a commit range.

## Analyze R3 and Consistency

Analyze r3's **GREEN still holds at the requirement/plan/tasks/contract level**: requirements, plan and the four contracts were last changed before the analyze pass (01:00–01:12), the task structure re-validates 0/0, FR coverage is 25/25, and all 60 clauses remain claimed. It does **not** cover implementation-level evidence added later: the stale T015 C-47 sentence (P1-03) and the unmeasured "未修复" wording (P1-02) are post-analyze drifts. Cite r3 as requirement-level green, not as an implement or test verdict.

## Test Waiver Audit

- `verification.md` GATE-3 is **`waived/void`**, explicitly "不计为 pass"; DoD-4 is **not** claimed; SC-006 is **`not-evaluated`**; T027 NEW-failure count is **`not-evaluated` (not 0)**. No waived item is written as pass or green.
- 26 last-observed red tests are disclosed with per-owner counts, and T019/T020/T021/T024/T026/T027 pytest portions are included in the waiver scope. The only defect is the tense/state wording in P1-02, not a secret green.
- The 30/30 `[X]` closure is a waiver decision, not evidence that the acceptance tests pass. Read `verification.md` §Test waiver and §未测量与剩余风险 together with the task list.

## Merge Readiness

**Mergeable under the user's explicit test waiver** (verdict `PASS WITH WAIVER`, not `BLOCKED`):

1. 065a code, reference, docs and mirrors are committed, byte-identical, and deterministic gates pass; no forbidden surface changed; no push/merge/kill/delete occurred.
2. The branch is 43 commits ahead of `master` and carries non-065a work (066 archive `8aef663f`, 067 requirements `37b651d8`, executor budget `696d5f4b`). Merge scope must be confirmed by the user; this review only validates the 065a range.
3. Preferred pre-merge cleanup: a docs-only commit for P1-02 and P1-03 (task/verification wording). If the user accepts them as immediate post-merge follow-ups, they are not functional blockers.
4. The merge must be described as "065a implementation-complete with test waiver"; it must not be described as tested or ready for production until the full cycle is restored.

**Restore the full test cycle after merge**: (a) run the three 065a test files plus the full regression against the T001 baseline and replace the 26-test "last observed" figure with measured results; (b) execute the SC-006 mutations (remove `unwatched` detection and the C-48 salvage gate) and record the red node IDs; (c) re-run RP-1 directory-artifact / C-59 cases under pytest; (d) re-check C-47 stop-reason masking before 065c implements executed stops; (e) record the 065a completion/waiver in `features/065.md` while keeping Feature 065 `Planned`; (f) then proceed to 065b and 065c.

## Review Notes

- No code, spec, task, verification or mirror file was modified. This review added only this report.
- No pytest was executed in this review; all test-face claims above are read from committed evidence, not re-measured.
- The three implementation commits reviewed: `cd8d3206`, `12294c0e`, `0860092a`; earlier 065a commits (`55bc4ec4`, `0ac387eb`, `35aa0192`, `0989d804`) were read via the branch diff and red-first evidence.

REVIEW-DONE
