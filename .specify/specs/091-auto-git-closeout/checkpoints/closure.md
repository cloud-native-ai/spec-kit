# Closure — 091-auto-git-closeout

## 1. Terminal goal degree table
| criterion | degree | evidence |
|---|---|---|
| 四种工作流模型各自的收口序列可在夹具仓库中复现 | 100% | `tests/contract/test_git_closeout_contract.py` (45 passed); four-model arms; `test-evidence/fix-p1-evidence.txt` |
| 托管块缺失或 Closeout=ask 时，收口呈报并等待，不自行推送 | 100% | contract arms for `ask`/absent; review's ask/absent pass |
| 推送被拒或合并冲突时，收口在首个失败处停下并记录状态，不自动强推、不二次重试 | 100% | failure fixtures + mutation arms (T030/T041); review's fail-stop pass |
| 产物命令与无人值守运行使用同一条收口步骤（无第二套机制） | 100% | `shared/workflow/artifact-commit-step.md` § Close-out + every command's step 7; role-scoped negative search (P1) |

## 2. Review findings disposition
| ID | Severity | Disposition | Evidence |
|---|---|---|---|
| F1 | P0 | resolved — status claim is a gate product | P2: `templates/commands/implement.md`, `templates/verification-log-template.md`; `fix-p2-evidence.txt` |
| F2 | P0 | resolved — published-state check mandatory at checkpoint/closure; the live refs converge in this closure's merge/push and are verified post-push | P3: `references/checkpoint-protocol.md` § 5b; `fix-p3-evidence.txt` |
| F-ACCEPTANCE | P0 | resolved — machine-readable `SC-NNN_status=` block | P2: `verification.md`; closure-acceptance-check accept |
| C1 | blocking | resolved — full role-filtered target set pushed; `remote_name=` request-not-override | P1: `tests/fixtures/git_closeout/repo.py`; mutation M1/M2 |
| C2/C3 | blocking | resolved — SC-005 guard role-scoped; read-only branch exercised (three removal modes) | P1: `test_git_closeout_contract.py` |
| R-36a | pre-existing | carried — three sandbox-red contract modules A/B-proven red at HEAD with the feature stashed; not caused by this feature | `verification.md` § Residuals; `run-note-sandbox.txt` |

Non-blocking review findings (review P1/P2 and code P1/P2) are recorded as dated pointers in the owning artifacts (P3's checkpoint-protocol § pointers; `verification.md` § Residuals); they are not silently dropped.

## 3. Acceptance
- `closure-acceptance-check.py --spec-dir .specify/specs/091-auto-git-closeout --repo .` → **accept** (exit 0), final_path pass=6 blocked=0 deferred=0 partial=0 fail=0 unknown=0, claimed_status=Implemented; the closure flips the registry to Completed.

## 4. Full-suite closure reading
- Baseline: `test-evidence/baseline-failed.txt` (36 ids, serial).
- Parallel-runner reading (`closure-full.txt`): 49 bare ids; **not comparable** — the runner's parallel mode and its bare-id `--names-out` format differ from the serial baseline's `FAILED`-prefixed list. Kept as an exploratory record, never the verdict.
- Serial run 1 (`closure-serial-full.txt`): 48 failed / 8060 passed; NEW 20 vs baseline. Classification: 16 lie in R-36a's three modules (`test_compile_embeds.py` 4, `test_compile_reconcile_guards.py` 7, `test_engine_face_contract.py` 5); 2 `test_isomorphism_map.py` and 2 others were **driver-scratch contamination** — the three fix worktrees under `.specify/.tmp/sdd-loop/worktrees/` were still present and the tree-scanning tests saw their repo copies; 2 were **test-expectation defects** exposed by legitimate 091 changes (`test_goal_migration` counted a tracked `test-evidence/*.txt` run log as a live face; `test_t078` treated modified command files as added commands).
- Corrective actions: worktrees removed (HR11 cleanup); `test_goal_migration` now excludes `/test-evidence/*.txt|.log` run logs; `test_t078` uses `git diff --diff-filter=A` (added commands only); both corrected tests pass.
- Final serial closure run (`closure-final-full.txt`): **44 failed / 8064 passed / 2 skipped**; vs the baseline: NEW 16 / CLEARED 8. Every NEW id lies inside R-36a's three modules (`test_compile_embeds.py` 4, `test_compile_reconcile_guards.py` 7, `test_engine_face_contract.py` 5), A/B-proven red at HEAD with the feature stashed; with R-36a applied **NEW=0**. The earlier four worktree-induced and two test-expectation failures are gone. GATE-1/DoD-4: **pass (zero new with R-36a)**.

## 5. Smoke
- `test-evidence/T062-smoke.txt`: smoke_command / smoke_exit_code=0 / smoke_evidence_path present (see `verification.md`).

## 6. Team archive
- `.specify/specs/091-auto-git-closeout/team/091-auto-git-closeout/team.md` lifecycle_state archived; the spec-local temporary team is run-scoped.

## 7. Published refs
- Verified (2026-11-09): local `master` at **4420076c**; `gitlab/master`, `github/master` and `gitee/master` all equal **4420076c**; `origin` untouched (read-only); the `091-auto-git-closeout` feature branch deleted after the fast-forward merge. The later 092 commits are a separate local line on the same trunk, not part of 091.
