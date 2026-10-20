# Verification — Feature 064 (implement, 2026-10-20)

**Branch**: `064-subagent-concurrency` · **Tests Mode**: ON · **Test runner**: `scripts/bash/run-tests.sh` with `SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python3` (pytest 9.1.1).

> **Post-review repair (2026-10-20)**: Review finding P0-01 plus the key P1 findings F2–F5 (and F6–F12 dispositions) changed the engine, watcher, tests and several earlier "Closed" claims. Section 12 and `notes/postreview-repair.md` are the current disposition; where §3–§7 conflict with §12, §12 wins.

## 1. Test environment (disclosed correction)

The tasks/plan premise "pytest unavailable" was falsified at implement time: the system `python3` has no pytest, but a pytest-capable interpreter exists at `/Users/liuqiming.lqm/project/profiles/.venv/bin/python3`. Every test run uses the canonical `run-tests.sh` with `SPECKIT_PYTHON` set, so green is **observed**, not fabricated. The system interpreter remains pytest-free, so the runner's loud-fail contract is unchanged.

The watcher self-test's `dead` case was made deterministic (`pid=999999`) instead of spawning and waiting for a process that macOS could recycle; this removes a PID-reuse flake without changing the verdict machine or exit codes. The four baseline failures remain exactly the recorded macOS degradations.

## 2. Red-first evidence

| Evidence | Location | Result |
|----------|----------|--------|
| R1 foundational engine unit tests | `notes/red-first-evidence.md` § R1 | `9 failed` — engine missing |
| R2 US1 contract/integration/unit | `notes/red-first-evidence.md` § R2 | `24 failed, 24 passed` — ingress/attribution/docs missing |
| R3 US2 workspace isolation | `notes/red-first-evidence.md` § R3 | `26 failed, 16 passed` — ownership/queue/resources/docs missing |
| R4 US3 lifecycle | `notes/red-first-evidence.md` § R4 | `21 failed, 20 passed` — lease/reservation/identity/docs missing |
| R5 US4 CLI profiles | `notes/red-first-evidence.md` § R5 | `19 failed, 21 passed` — profiles/H2/probe/docs/mirrors missing |

Each red run was captured before its implementation; every story ended with a green run (see § 3).

## 3. Test results

| Run | Command | Result |
|-----|---------|--------|
| Feature matrix (11 files) | `run-tests.sh <unit + 5 contracts + skill + non-regression + 3 integration> -q` | **151 passed, 0 failed** (56.45 s) |
| Full suite | `run-tests.sh tests -q --names-out current-failed.txt` | **4077 passed, 69 failed, 1 skipped** (307.71 s); baseline 71 failed; a second full run after the non-behavioral engine-import cleanup and the 3.8-compatible stdlib guard reproduced the identical failure set |
| Baseline diff | `comm -13 baseline-failed.txt current-failed.txt` | **0 NEW failures**; 2 baseline failures fixed (`test_c12_mirror_byte_identical`, `test_c18_mirror_pair_no_drift`) |
| Watcher self-test | `watch-target.sh --self-test` | **18 passed, 4 failed** — exactly the recorded baseline (`pid-reuse`, `zombie`, `manifest`, `pgrep-zero-match-trap-reproduced`); new attribution and lease-renew-hook cases pass |
| Confirmation gates | `run-tests.sh tests/contract/test_confirmation_gates_sweep.py -q` | **45 passed, 1 failed** — the failure is in the recorded baseline (unchanged) |
| Single-line compatibility | LR-13 / EN-16 / NG-07 named cases | **3 passed** |
| Post-review feature matrix (11 files) | same file set as above, after the P0/P1 repair | **160 passed, 0 failed** (126.07 s) — full log `notes/postreview-logs/feature-matrix.log` |
| Post-review matrix, final tree (12 files) | 11 feature files + `test_shipped_surface_client_neutrality.py`, after the independent-audit bypass fixes | **168 passed, 0 failed** (93.95 s) — full log `notes/postreview-logs/feature-matrix-final.log` |
| Post-review full suite | `run-tests.sh tests -q --names-out current-failed.txt` | see §12 (full log `notes/postreview-logs/full-suite.log`) |
| Post-review watcher self-test | `watch-target.sh --self-test` | **26 passed, 0 failed** (all four prior baseline failures fixed: real pid-reuse, zombie, manifest freshness, pgrep trap assertion) |

## 4. Success Criteria

| SC | Status | Evidence |
|----|--------|----------|
| SC-001 | **Pass** | `test_two_lines_same_sentinel_no_cross_attribution`: two lines, identical `PLAN-DONE`, identical CLI; both `DONE`, `attribution=own`; zero cross-attribution |
| SC-002 | **Pass** | `test_unlabelled_message_exactly_one_clarification_and_no_process_scan`: 2 active lines → `clarify`, exactly one `？`, 2 candidates; PATH-stub `ps`/`pgrep`/`pidof` calls = 0; `ambiguous-stop` counted as a correct terminal outcome |
| SC-003 | **Pass** | `test_foreign_status_pid_and_meta_never_change_state`: `RUNNING` (never DONE), state/updated_at unchanged, `attribution=foreign`; `test_en_04_classification` covers `foreign`/`stale-run`/`unattributed`/`legacy` |
| SC-004 | **Pass (behavior, post-review)** | `test_integration_executor_merges_queue_and_replay_is_identical`: the delivered `integrate-lines.py` merges two real worktrees; merged **tree SHA identical across two replays**, `archive_calls=2`, `mirror_calls=1`, worktrees removed, `git fsck` exit 0; failure case retains the worktree and continues. Earlier plan-only evidence is superseded. |
| SC-005 | **Pass (behavior, post-review)** | `test_delivered_runner_recipe_survives_driver_kill_and_reattaches`: the documented `nohup … & disown` recipe launches the delivered `run-stage.sh`; driver-group SIGHUP leaves runner **and** CLI alive, heartbeat advances, new session `lease → verify-identity ok → --once RUNNING → DONE`, reservation attach, PIDs unchanged (zero redispatch). Fixture-only survival evidence is superseded. |
| SC-006 | **Pass (behavior, post-review)** | `test_clp_10_observation_fixture_cardinality` executes `tests/fixtures/cli_observation.py`: no new fact → 1 spine event, 0 feedback, profile unchanged; mismatch → spine + provenance + exactly 1 retrievable `cli-profile:qodercli` entry. qodercli known rows carry `qodercli --version` → `1.1.73`. |
| SC-007 | **Pass** | confirmation gate suite unchanged (1 pre-existing baseline failure); push-stub scenario records zero `push`; watcher exit-code constants/help pinned in `test_ng_04` |
| SC-008 | **Pass** | 11 planned/additive test files present; three mutation drills each turned ≥1 test red (§ 5) |
| SC-009 | **Pass** | `test_lr_12_concurrent_registration`: N=12 writers + interleaved reader; 100% parseable, 0 lost, 0 duplicates, no half-write observed |
| SC-010 | **Pass** | `test_lc_16_u6_no_active_residue`: closed, lease/reservation removed, `list --active` empty; failed/abandoned worktree retained; reattach always sets `snapshot_required` and docs mandate `--once`; duplicate start → attach |

## 5. Mutation drills

| Drill | Red run | Green re-run |
|-------|---------|--------------|
| 1. Attribution filter removed (watcher copy) | `2 failed, 4 passed` in `test_two_line_isolation.py` (foreign and stale-run cases consumed) | copy deleted → `6 passed` |
| 2. Detach removed (`SDD_RUNNER_MODE=foreground`) | `4 failed` in `test_session_kill_reattach.py` (runner dies with the driver group) | default detached → `4 passed` |
| 3. Reservation exclusivity removed (engine copy: check-then-create + race window) | `1 failed, 15 passed` (`test_lc_04_reservation_concurrent_single_winner`) | copy deleted → `16 passed` |
| 4. Ownership closure gate removed (post-review, engine copy: closed/stale/orphaned skipped again) | `2 failed, 3 passed` in the five P0 tests — `test_p0_stale_cleanup_is_not_an_ownership_release` and `test_p0_close_without_evidence_still_blocks` (full log `notes/postreview-logs/mutation-p0-red.log`) | real engine → `5 passed` (`notes/postreview-logs/mutation-p0-green.log`) |

## 6. Completion Gates

| Gate | Command | Result |
|------|---------|--------|
| GATE-1 | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/064-subagent-concurrency/tasks.md` | **PASS** — 0 errors, 0 warnings |
| GATE-2 | `run-tests.sh tests -q --names-out …` + `comm -13 baseline current` | **PASS** — 69 current vs 71 baseline; 0 NEW failures |
| GATE-3 | `grep -cE '^- \[[ >]\]' tasks.md` | **0** (all 82 rows `[X]`) |
| GATE-4 | SC-001…SC-010 present in this file | **PASS** (§ 4 lists all ten) |
| GATE-5 | `sync-mirrors.py --check --only skills/external/sdd-loop-driver` / `--only shared/definitions/probe-definitions.md`; 9 shared DIFFs unchanged | **PASS** — both exit 0; shared diff set still exactly the 9 baseline files |
| GATE-6 | `probe-utils.py --action probes --validate`; `--action compile-embeds --check` | **PASS** — `10 classes, 114 internal + 0 external`; `74 units, zero drift` |
| GATE-7 | `grep -R "git push" skills/external/sdd-loop-driver/scripts/` | **0 matches** |
| GATE-8 | `grep -cE '^### S[1-6]\.' notes/quickstart-run.md` | **6** |
| GATE-9 | `run-tests.sh tests/contract/test_sdd_loop_driver_cli_profiles.py -q -k test_clp_17_no_063_duplicate_owner` | **1 passed** |
| GATE-10 | `test_non_regression_064.py` stdlib proof | **passed** (`test_ng_05_stdlib_only_engine`: stdlib imports only; watcher is bash) |

## 7. Carried-over analyze findings — disposition

Original implement claim: all 22 carried-over/new findings were closed. **Review F10 re-read this ledger**: several dispositions (I-04, I-15, G-01, G-06 and others) were backed by doc/string or plan-only evidence. The post-review status is in §12 and `notes/postreview-repair.md`; the rows below remain as the implement-time record with the §12 overrides.

| ID | Severity | Disposition |
|----|----------|-------------|
| I-01 | MEDIUM | **Closed** — `legacy` restricted to single-active-line / 058 compatibility in watch-model §11, stage-prompts, EN-16; multi-line legacy calls MUST NOT bypass attribution (driver layer; ingress already routes deterministically) |
| I-05 | MEDIUM | **Closed** — LR-13/NG-07 carry the registration/deregistration failure carve-out |
| I-06 | MEDIUM | **Closed** — FR-030 now says `--once` before any redispatch/去向 decision, referencing LC-08/V-ID-4 |
| I-07 | MEDIUM | **Closed** — LC-12: `identity=unknown` is never dead; dead/mismatch → U5 → explicit `stalled`; `stale` only by explicit cleanup |
| I-09 | MEDIUM | **Closed** — FR-013 wording aligned; platform exemption + `skipped` definition added to Assumptions |
| I-10 | MEDIUM | **Closed** — watcher output now carries `line/run/stage/event=watcher-verdict/at/attribution`; EN-06 updated; `test_en_02` asserts the fields |
| I-12 | MEDIUM | **Closed** — provenance `feedback_id` backfill, U4 buffering comparison, and per-event feedback rule documented in `references/cli/index.md` |
| I-13 | MEDIUM | **Closed** — standalone feedback exception approved in requirements Assumptions |
| I-17 | MEDIUM | **Closed** — feature detail Key Changes corrected to per-line Registry + batch mirrors once |
| I-19 | MEDIUM | **Closed** — lease renew cadence ≤ ttl/3; watch window ≤ ttl/3 or `--lease-renew-cmd` hook (watcher implementation + self-test `lease-renew-hook` + docs) |
| U-01 | MEDIUM | **Closed** — data-model E1 gains `run_history`, stage-null note, resources active_count/cap; E9 gains `profile_version`; R1 reference named |
| U-02 | LOW | **Closed** — `slugify` = lower + non-alphanumeric → `-`, trimmed, ≤20 chars; unit-tested |
| U-03 | MEDIUM | **Closed** — reservation PID = launcher identity (LC-04 + dispatch-recipes); runner only updates Registry |
| U-05 | MEDIUM | **Closed** — `resources.active_count/cap` written and reported; tested in `test_wi_18_19_20_resources` |
| U-06 | LOW | **Closed** — `integration_result.status` is `merged|failed` only (data-model + engine validation) |
| G-01 | MEDIUM | **Closed** — EN-13 named assertion in `test_en_13_clarification_non_blocking` (heartbeat and other-line state keep advancing) |
| G-04 | MEDIUM | **Closed** — SC-003 stale-run/unattributed and SC-005 orphan/stalled/remote-unreachable evidence added (tests + feature-ref) |
| G-05 | MEDIUM | **Closed** — SC-009 N=12 + interleaved reader assertion |
| G-06 | MEDIUM | **Closed** — SC-004 comparison level named: plan JSON byte equality + ordered line list + commit SHA membership + fsck |
| A-01 | MEDIUM | **Closed** — "safe default dispatch" defined in `references/cli/index.md`: skeleton + matrix acceptance; no matrix entry (hermes) → no dispatch |
| D-01 | LOW | **Closed** — duplicate NG traceability rows removed |
| F-01 | LOW | **Closed** — feature detail records checklist/analyze stages and lists the concurrency checklist + evidence files |

## 8. Implement-time assumptions and corrections

- **pytest interpreter** (§ 1) — disclosed; no fake green.
- **watcher `dead` self-test fixture** — deterministic PID 999999 replaces a process-reuse race; verdict/exit semantics untouched.
- **`branch_check=skipped`** — only when no branch is registered or git metadata is unavailable; macOS cwd → `unsupported` (FR-030/LC-07 exemption).
- **`integration_result.status`** — `skipped` removed; engine rejects it.
- **Client-neutral shipped surface** — shipped skill files use bare `061/063/064` references (no `Feature 0NN`), keeping `test_shipped_surface_client_neutrality` green.
- **Feature 063 overlap** — branch-verification record appended to `notes/063-overlap-adjudication.md`; merge-time deletion/pointer steps remain recorded; 063 worktree untouched.

## 9. Boundary audit (T082)

- **No automatic push**: zero `git push` in engine/watcher; push-stub records zero push actions; all scenarios are local.
- **No deletion of uncommitted work**: `archive-runtime` only copies; engine has no `shutil.rmtree`/`--force`; failed integration and U6 retain worktrees.
- **No new daemon/service/runtime dependency/model API**: engine imports stdlib only (`test_ng_05`); watcher is bash; no new command/skill.
- **No duplicate 063 owner**: repository-wide guard green; one CLI-profile contract, one Probe Object for `skill:sdd-loop-driver`.
- **Docs/mirrors consistent**: skill mirror and probe mirror byte-identical; docs entry references (not copies) the skill references; compile-embeds zero drift.

## 10. Deferred tasks

None — all T001–T082 are `[X]`.

## 11. Commit chain (implement)

`9e69f3de` US1 → `ba785b0a` US2 → `a100d560` US3 → `c37d7614` US4 → `30439f53` US5/Polish (verification, S6, task closure, analyze carry-over closure) → docs closure commit (DoD status).

## 12. Post-review repair (2026-10-20)

Authoritative detail and waivers: `notes/postreview-repair.md`. Review findings were re-read against the repaired tree; evidence kinds are explicit.

| Finding | Status after repair | evidence_kind | Named evidence |
|---------|--------------------|---------------|----------------|
| P0-01 promotion fail-open | **CLOSED (incl. five independent-audit rounds)** | behavior + mutation + independent audit | twenty-eight `test_p0_*` tests (update/register/re-acquire/forged-merge/released-reactivation/non-git/terminal-state/concurrency/ownership-mutation bypasses included); mutation red `4 failed, 24 passed` → green `28 passed` |
| P1-F2 watcher identity/macOS token | **CLOSED** | behavior | `test_en_07_watcher_consumes_registered_identity`, `test_en_07_watcher_rejects_branch_mismatch`; self-test 26/0 |
| P1-F3 executable integration queue | **CLOSED** | behavior | `test_integration_executor_merges_queue_and_replay_is_identical`, `test_integration_executor_failure_retains_worktree_and_continues` |
| P1-F4 detach/reattach product evidence | **CLOSED (local)** / Partial (remote) | behavior | `test_delivered_runner_recipe_survives_driver_kill_and_reattaches`, `test_run_stage_fails_loud_when_registry_update_fails` |
| P1-F5 behavior/doc separation | **CLOSED** | behavior + doc/static | delegate meta tests removed; `test_en_13` live-writer; `test_doc_*` renames |
| P1-F6 stale/orphaned states | **CLOSED** | behavior | `test_lc_13_orphan_mark_writes_state`, `test_lc_14_stale_explicit` |
| P1-F7 lease cadence | **CLOSED** | behavior | `test_lc_05_cadence_violation_is_recorded`, self-test `lease-window-over-ttl` |
| P1-F8 CLI observation fixture | **CLOSED** | behavior | `test_clp_10_observation_fixture_cardinality` |
| P1-F9 063 guard | **CLOSED (pre-merge guard)** | behavior | `check-063-overlap.py` + `test_clp_17_no_063_duplicate_owner` |
| P1-F10 closure ledger | **CLOSED** | doc/static | this §12 + repair record evidence kinds |
| P2-F11 evidence capture | **CLOSED for new runs** / historical Partial waiver | doc/static | `notes/postreview-logs/*.log` |
| P2-F12 `at` type | **CLOSED** | doc/static | data-model exception + EN-01 |

**Analyze carry-over re-read (F10)**: I-04 (integration), I-15 (lease), G-01 (EN-13), G-06 (SC-004) were Partial in the original ledger and are now backed by the behavior tests above; CHK012 (P0) and CHK031 (stale/orphaned) are now closed. The remaining original Partial items (CHK004 legacy multi-line, CHK022 feedback backfill prose, CHK026 063 branch, CHK038 macOS PID reuse, CHK040 NG-03 text) have either been upgraded (CHK026/CHK038) or remain doc/protocol-level with the waiver recorded in `notes/postreview-repair.md` §4.

**Repair test results**: final feature matrix **188 passed / 0 failed**; watcher self-test **26 passed / 0 failed**; P0 mutation red `4 failed, 24 passed` → green `28 passed`; full suite **69 failed / 4113 passed / 1 skipped** with **0 NEW / 0 fixed** against the review-HEAD `c9a0d132` rerun (69 = 69); mirrors 15 files byte-identical; probe 114 objects valid; compile-embeds 74 units zero drift. Logs: `notes/postreview-logs/`.
