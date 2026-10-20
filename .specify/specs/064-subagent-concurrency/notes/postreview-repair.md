# Post-review Repair Record — Feature 064

**Date**: 2026-10-20
**Review HEAD**: `c9a0d132` (review.md)
**Authority**: `review.md` findings F1–F12; independent P0 validator verdict CONFIRM; user authorization = P0 + key P1, no push.
**Rule**: every review finding below carries an evidence_kind (`behavior`, `doc/static`, `design-only`) and a named test or artifact. An unclosed slice is a recorded waiver, never a silent `Closed`.

## 1. P0-01 — promotion fail-open (CLOSED, behavior)

**Defect**: `promote-waiting` / `ownership-check` skipped holders in `closed|stale|orphaned`, so `deregister --reason stale-cleanup` (which wrote `closed`) silently released overlapping ownership and a second waiting line became `active`. `ownership-check` also auto-promoted without any explicit action.

**Fix** (`skills/external/sdd-loop-driver/scripts/line-registry.py`):

| Change | Location | Effect |
|--------|----------|--------|
| Holder closure gate | `_ownership_conflicts` + `_entry_manifest_view` + `_ownership_release_record` + `_closure_is_evidenced` | A holder stops blocking only when its manifest has `released_at` **and** an ownership-history `released` record with `evidence_ref`, or it is `closed` with `integration_result.status=merged`. `stale`/`orphaned`/closed-without-evidence keep blocking. A deleted manifest falls back to the entry's `owned_paths` projection. |
| No implicit promotion | `action_ownership_check` | Waiting stays waiting; response carries `promotion_required=true`; `last_event=ownership-clear-awaiting-promotion`. Promotion is explicit only. |
| Explicit promotion gate | `action_promote_waiting` | Runs the same conflict gate; `ownership-overlap` without a manifest is refused (exit 3, `manifest-missing`). |
| stale-cleanup is not a release | `action_deregister` | `--reason stale-cleanup` writes `state=stale`, `stale_at`, `stale_from_state`; keeps manifest, worktree and reservations; never writes `closed`; resource release happens only for `closed`. |
| Explicit disposition | `action_release_ownership` | `stale`/`orphaned` → `closed` with `ownership_released_at` and evidence; resources released only then. |
| Worktree evidence retained | `_ensure_unique_worktree` | stale/orphaned and retained-closed worktrees remain owned (no path reuse). |

**Tests** (`tests/contract/test_workspace_isolation_contract.py`):
`test_p0_stale_cleanup_is_not_an_ownership_release` (stale-cleanup → promote exit 3, waiter remains waiting, zero active lines), `test_p0_explicit_release_unblocks_waiter`, `test_p0_merged_u6_close_unblocks_waiter`, `test_p0_close_without_evidence_still_blocks`, `test_p0_ownership_check_never_auto_promotes`.
Existing `test_lr_10_stale_detection_explicit_cleanup`, `test_lc_14_stale_explicit`, `test_lc_13_orphan_*` were updated to the new state semantics.

**Mutation evidence**: engine copy with the old state-skip restored → `4 failed, 24 passed` (`notes/postreview-logs/mutation-p0-red.log`); real engine → `28 passed` (`mutation-p0-green.log`).

**Independent audit follow-up (2026-10-20)**: a fresh-context read-only agent rejected the first repair and reproduced four bypasses. All four are now closed and covered:

| Bypass | Fix | Regression test |
|--------|-----|-----------------|
| `update --state active` promoted a waiting line without any conflict scan | `action_update` runs `_raise_if_ownership_conflict` on every non-active → active transition | `test_p0_update_state_active_cannot_bypass_the_gate` |
| `register --state active --manifest` skipped the conflict scan | `action_register` runs the same gate before writing | `test_p0_register_active_with_overlap_is_rejected` |
| After `release-ownership`, an `ownership-check` re-acquisition was still skipped forever because the old release history was treated as permanent | `ownership-check` writes `claimed_at` and clears `released_at`/`release_reason`/`evidence_ref`; conflict scanning trusts the stored manifest when present and only falls back to history when no manifest exists | `test_p0_reacquired_ownership_blocks_again` |
| `integration_result` could be forged through `update --integration-result` (and `integration-record --commit deadbeef` was unverified) | removed the `update` field; `integration-record --result merged` requires the commit to exist in the repo **and** be reachable from HEAD | `test_p0_forged_merge_evidence_is_rejected`; `test_p0_merged_u6_close_unblocks_waiter` now uses a real commit |

The audit also flagged F2/F4 gaps; those fixes are recorded in their sections below.

**Second independent audit (fresh context) — three further bypasses, all closed:**

| Bypass | Fix | Regression test |
|--------|-----|-----------------|
| A completed line with a released manifest could `update --state active`, then a new overlapping line could register → two active lines | `action_update` refuses a released manifest on entry into active; the line must `ownership-check` (re-acquire) first | `test_p0_released_line_cannot_reactivate_without_reacquire` |
| `integration-record --result merged` accepted any commit when `repo_root` was not a git repo (ownership line) | a line with `owned_paths`/`worktree_path` requires a verifiable git repo; `merged` also requires the commit to contain the line's worktree HEAD | `test_p0_non_git_forged_merge_with_ownership_rejected`; strengthened `test_p0_merged_u6_close_unblocks_waiter` (real ff-merge) |
| `integrate-lines.py` could abort a pre-existing rebase/merge in the worktree/repo | pre-flight refuses a worktree already rebasing (`rebase-in-progress`, worktree retained) and a trunk repo with an in-progress merge/rebase; abort runs only for operations this executor started | `test_integration_executor_refuses_preexisting_rebase` |

Re-acquisition ordering was also tightened to **current-claim FIFO**: `claimed_ns` (nanoseconds; `created_at` fallback) is the ordering key, `ownership-check` refreshes it, and a re-acquired line queues behind existing waiters instead of preempting by original `created_at`. This refinement is recorded in requirements FR-021, data model V-LR-13 and WI-06.

**Third independent audit — state-machine edges, all closed:**

| Gap | Fix | Regression test |
|-----|-----|-----------------|
| A waiting line could `release-ownership` (released_at set) and still `promote-waiting` itself to active; a released manifest passed to `register` also entered active as a non-blocking owner | `promote-waiting` refuses a released self-manifest; `register` treats the call as a fresh claim and clears `released_at`/evidence fields | `test_p0_released_waiting_line_cannot_promote`, `test_p0_register_reclaims_a_released_manifest` |
| An *active* holder could release ownership and stay active while the next line registered, yielding two active writers | `release-ownership` demotes active/waiting lines to `stalled` (explicit U5/U6 disposition); the released manifest only stops blocking for non-active states | `test_p0_active_release_demotes_holder` |
| `closed` was not terminal: `update --state active` could revive a merged+closed line | `update` rejects any state change out of `closed` | `test_p0_closed_is_terminal` |
| A caller could inject `claimed_ns: 0` through `update --ownership-manifest-path` and jump the FIFO; concurrent `register` gates had no cross-line lock | the update field is removed; ownership-affecting actions serialize on the environment-level `.ownership.lock` | `test_p0_concurrent_overlapping_registration_single_winner` |
| Merge containment was skipped when the worktree existed but `git rev-parse HEAD` failed; `update` could erase `owned_paths`/`worktree_path` to dodge the non-git check | a durable `write_line` flag (set at register, never updatable) drives verification; every write line must retain a worktree with a verifiable HEAD; the worktree HEAD must be contained in the claimed merge commit | `test_p0_merged_requires_worktree_containment`, `test_p0_non_git_forged_merge_with_ownership_rejected` |

**Fourth independent audit — remaining state/path edges, all closed:**

| Gap | Fix | Regression test |
|-----|-----|-----------------|
| `allocate-resources` could move a closed line to `waiting`, then `promote-waiting` activated it | allocation requires `state=active`; allocation and orphan marking now take the ownership lock | `test_p0_closed_not_revived_by_allocate` |
| `update --state active` could revive `stale`/`orphaned`/`completed` lines (only closed was guarded) | entry into active is allowed only from `waiting`/`stalled` (or already active) | `test_p0_update_cannot_revive_stale_or_completed` |
| `--owned-paths` was stored raw while only the gate view was normalized; `update --owned-paths` was ungated | normalize at register/update, normalize legacy projections on read, and gate active-line ownership changes | `test_p0_owned_paths_are_normalized_at_register_and_update` |
| `worktree_path` was rewritable to the repo root, making merge containment trust the trunk itself | worktree must resolve outside `repo_root`/`project_dir` (register/update/validate); merged rejects worktree==repo | `test_p0_worktree_must_be_outside_repo_roots`, `test_p0_merged_requires_real_head_containment` |
| The `promote-waiting` released-manifest branch was only reachable in legacy states and untested | crafted released waiting manifest refuses promotion | `test_p0_promote_refuses_a_released_waiting_manifest` |

**Fifth independent audit — ownership mutation edges, all closed:**

| Gap | Fix | Regression test |
|-----|-----|-----------------|
| `update --owned-paths` let an earlier bare-active line add paths overlapping an already-active owner (FIFO preemption) | any conflicted competitor that is already `active` blocks unconditionally (FIFO only orders waiting lines) | `test_p0_earlier_active_cannot_add_overlapping_paths` |
| `update --owned-paths '[]'` silently released projection-only claims; updating owned_paths shadowed an existing manifest | emptying is refused (release must be explicit); manifest-owned path sets can only change via `ownership-check` | `test_p0_owned_paths_cannot_be_emptied_or_shadow_a_manifest` |
| A manifest-less line released ownership, then `update --state active` (the release check only looked at the manifest) | `_entry_released` checks the manifest file, falling back to release history when no manifest exists; re-acquisition creates a manifest | `test_p0_manifestless_release_blocks_reactivation` |
| `worktree_path`/`branch` repointing allowed a decoy worktree to satisfy merge containment | worktree/branch/base_sha are immutable once set; merged also requires the worktree branch to match the registered branch | `test_p0_worktree_path_is_immutable`, `test_p0_merged_requires_real_head_containment` (real containment) |
| `lease-acquire`/`reserve` accepted closed lines | both refuse closed/stale/orphaned entries | `test_p0_lease_and_reserve_refuse_closed_lines` |

**Evidence kind**: behavior + five independent audits + mutation. **Status**: CLOSED (required P0 scope; residual hardening tracked as waivers below).

## 2. Key P1 closures

### F2 — watcher consumes Registry identity and platform start tokens (CLOSED, behavior)

- `watch-target.sh` gains `--registry DIR` (or `SPECIFY_LINE_REGISTRY_DIR`). It reads `<line_id>.json`, accepts only the registered `runner_pid` or `cli_pid`, takes the registry start token as authoritative, and rejects an unregistered PID or a missing entry as `DEAD pid=unregistered`. When a branch is registered it compares the worktree branch (`pid=branch-mismatch`).
- Start tokens now work without `/proc`: macOS uses normalized `ps -p <pid> -o lstart=`; zombie detection uses `ps -p <pid> -o stat=` (Z). The four recorded self-test baseline failures are fixed.
- Independent audit follow-up: a `present` entry with **no** registered PID no longer trusts an ambient pid file (`DEAD pid=unregistered`); an unreadable entry is treated as missing; `--registry` without `--line-id` is a usage error; a registered branch whose worktree is missing/unverifiable is a mismatch.
- Tests: `test_en_07_watcher_consumes_registered_identity` (own RUNNING; foreign live PID → DEAD unregistered; wrong token → DEAD reused; missing registry → DEAD unregistered), `test_en_07_registered_line_without_pids_rejects_ambient_pid`, `test_en_07_watcher_rejects_branch_mismatch`; self-test `reg-identity`, `reg-unregistered`, `reg-missing`, real `pid-reuse`, real `zombie`.
- **Evidence kind**: behavior. **Status**: CLOSED.

### F3 — executable integration queue (CLOSED, behavior)

- New `scripts/integrate-lines.py` executes WI-14: rebase → gate → `merge --ff-only` → `integration-record merged --commit` → `archive-runtime` → `git worktree remove` (no `--force`), records failures and continues, requires the repository to be on trunk (never switches branches), and runs `--mirror-cmd` exactly once per batch.
- Tests: `test_integration_executor_merges_queue_and_replay_is_identical` (two real worktrees, two independent replays → identical merged tree SHA; `archive_calls=2`; `mirror_calls=1`; worktrees removed; `git fsck` clean), `test_integration_executor_failure_retains_worktree_and_continues` (gate failure retains the worktree, records `failed`, next line still merges).
- **Evidence kind**: behavior. **Status**: CLOSED.

### F4 — delivered detach runner + end-to-end kill/reattach (CLOSED, behavior; remote slice Partial)

- New `scripts/run-stage.sh`: writes the four-piece evidence, launches the CLI child under `nohup` (SIGHUP-proof), projects `runner_pid`/`cli_pid` + tokens into the Registry, writes atomic status with the sentinel flag, and on a failed registry projection writes `ANOMALY: registry-update-failed`, terminates the CLI and exits 4.
- Independent audit follow-up: `--engine` is now required (a runner without registry projection could leave an untracked stage and exit 0).
- Tests: `test_delivered_runner_recipe_survives_driver_kill_and_reattaches` uses the documented `nohup … & disown` recipe, kills the driver process group, asserts runner **and** CLI survival, heartbeat continuation, `verify-identity=ok`, `--once RUNNING → DONE`, reservation attach, and unchanged PIDs (zero redispatch). `test_run_stage_fails_loud_when_registry_update_fails` and `test_run_stage_requires_the_engine` cover the fail-loud paths.
- **Remote slice**: `classify-remote`/`remote-unreachable` behavior remains covered; executing `ssh+su+nohup` on a real remote host is not available in this environment → recorded as Partial (see §4).
- **Evidence kind**: behavior (local). **Status**: CLOSED (local), Partial (remote execution).

### F5 — behavior vs doc/meta tests (CLOSED, behavior + doc split)

- Removed the three meta tests that only grepped other test files: `test_en_15_integration_delegate`, `test_wi_21_two_write_line_delegate`, `test_lc_18_kill_reattach_delegate`; their claims are now actual e2e behavior in F3/F4.
- Renamed doc-only checks to `test_doc_*` (`test_doc_wi_02`, `test_doc_wi_11`, `test_doc_wi_12`, `test_doc_wi_16`, `test_doc_wi_17`, `test_doc_lc_01_02`, `test_doc_clp_10`).
- `test_en_13_clarification_non_blocking` now runs a live heartbeat writer during `resolve-message`, asserts the writer keeps advancing, that clarification returns immediately, and that no Registry entry is mutated.
- Verification reports behavior evidence separately (§12) and cannot cite doc/static checks as behavior.
- **Evidence kind**: behavior (EN-13, WI-21/LC-18 replacements), doc/static (renamed tests). **Status**: CLOSED.

## 3. Remaining P1/P2 dispositions

| Finding | Disposition | Evidence kind | Status |
|---------|-------------|---------------|--------|
| F6 stale/orphaned states | `deregister --reason stale-cleanup` writes `stale`; `orphan-check --mark` writes `orphaned` (+ `orphaned_at`, `orphan_evidence`); `release-ownership` is the explicit disposition to `closed` | behavior: `test_lc_13_orphan_mark_writes_state`, `test_lc_14_stale_explicit`, `test_lr_10_*` | CLOSED |
| F7 lease cadence enforcement | default watch window 200 s (= ttl/3); explicit `--lease-ttl N` fails a window > N/3 without a renewal hook; `lease-renew` records `lease-cadence-violation` in lease history and sets Registry `last_event` | behavior: `test_lc_05_cadence_violation_is_recorded`, self-test `lease-window-over-ttl` | CLOSED |
| F8 CLI observation fixture | executable `tests/fixtures/cli_observation.py`; `test_clp_10_observation_fixture_cardinality` proves spine → provenance → exactly one feedback (and zero on no-fact); qodercli rows record `qodercli --version` → 1.1.73 | behavior: named test | CLOSED |
| F9 branch-aware 063 guard | `scripts/check-063-overlap.py` inspects the 063 branch tree (`pending-merge-obligation` / merged `dual-owner` exit 3); `--strict-premerge` turns it into a merge-gate failure; documented in `notes/063-overlap-adjudication.md` §5 | behavior: `test_clp_17_no_063_duplicate_owner` executes both modes | CLOSED (pre-merge guard); 063 branch itself untouched by design |
| F10 closure ledger evidence kinds | verification §7 banner + §12; this record carries `evidence_kind` per finding | doc/static (governance) | CLOSED |
| F11 full-capture evidence | this repair's matrix/full-suite/watcher/mutation runs are captured under `notes/postreview-logs/` with exact commands in §5 | doc/static | CLOSED for new runs; historical red-first logs Partial/waived (§4) |
| F12 `at` type conflict | data-model: `at` is epoch seconds (explicit exception); EN-01 states the same | doc/static | CLOSED |

## 4. Waivers and Partial slices (not silently retained)

1. **F4 remote execution — Partial.** The remote topology (`ssh+su+nohup`, same registry fields) is protocol/classification-tested only; no reachable remote host was available. Local detach/reattach is behavior-tested end to end.
2. **F11 historical red-first/mutation artifacts — Partial (waived).** Implement-time ephemeral logs (quickstart `/tmp/run-s5.sh`, mutation copies) are gone and cannot be reproduced from HEAD. New runs for this repair are fully captured; the historical numbers remain disclosed as unreproducible rather than re-marked green.
3. **SC-001/SC-003 "100%" metrics.** These are aggregate assertions over deterministic fixtures (all events classified, zero cross-attribution), not statistical samples; no sampling claim is made.
4. **063 branch assets remain by design.** The provisional 063 contract still exists on the unmerged branch; the guard reports it as `pending-merge-obligation` and `--strict-premerge` fails until the recorded deletions happen at merge time.
5. **Mirror script modes.** `sync-mirrors.py` compares/publishes content; executable bits on `run-stage.sh` in `.specify/skills/` may differ from the source. All invocations use `bash <script>`/`python3 <script>`, so behavior is unaffected.

## 5. Test evidence (this repair)

| Run | Command | Result | Log |
|-----|---------|--------|-----|
| Feature matrix (first pass, 11 files) | `SPECKIT_PYTHON=… bash scripts/bash/run-tests.sh <unit + 5 contracts + skill + non-regression + 3 integration> -q` | **160 passed, 0 failed** (126.07 s) | `notes/postreview-logs/feature-matrix.log` |
| Feature matrix (final tree, + neutrality file) | same 11 files + `test_shipped_surface_client_neutrality.py` | **188 passed, 0 failed** (128.63 s) | `notes/postreview-logs/feature-matrix-final.log` |
| Watcher self-test | `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` | **26 passed, 0 failed** | §3 of verification.md |
| P0 mutation (red) | mutated engine copy (old state-skip restored), `-k p0_` | **4 failed, 24 passed** | `notes/postreview-logs/mutation-p0-red.log` |
| P0 green | real engine, `-k p0_` | **28 passed** | `notes/postreview-logs/mutation-p0-green.log` |
| Full suite (first pass) | `run-tests.sh tests -q --names-out current-failed.txt` | **70 failed / 4085 passed / 1 skipped** (440.20 s) | `notes/postreview-logs/full-suite.log`, `current-failed.txt` |
| Baseline (review HEAD `c9a0d132`, detached worktree) | same suite at `c9a0d132` | **69 failed / 4077 passed / 1 skipped** (300.36 s) | `notes/postreview-logs/baseline-full.log`, `notes/postreview-logs/baseline-failed-review-head.txt` |
| Baseline diff (first pass) | `comm` on sorted FAILED lists | **1 NEW**: `test_shipped_surface_client_neutrality.py::test_shipped_surface_has_no_framework_runtime_references` (caused by `Feature 0NN` wording in two new script docstrings); **0 fixed** | — |
| Neutrality fix | rewrote the two docstrings to bare `063/064` references; re-ran the test + mirror sync | **1 passed**, 0 drift | — |
| Full suite (final tree) | same suite on the fully repaired tree | **69 failed / 4113 passed / 1 skipped** (495.20 s) | `notes/postreview-logs/full-suite-final.log`, `current-failed-final.txt` |
| Baseline diff (final) | `comm` final FAILED names vs the `c9a0d132` rerun | **0 NEW / 0 fixed** (69 = 69; +36 newly passing feature tests) | `notes/postreview-logs/current-failed-final.txt` vs `notes/postreview-logs/baseline-failed-review-head.txt` |
| Mirrors | `sync-mirrors.py --check --only skills/external/sdd-loop-driver` | **ok — 15 files byte-identical (0 drift)** | — |
| Probe/compile | `probe-utils.py --action probes --validate`; `--action compile-embeds --check` | **probe: 10 classes, 114 internal + 0 external; compile: 74 units, zero drift** | — |

## 6. Files changed (repair)

Engine/scripts: `line-registry.py`, `watch-target.sh`, new `run-stage.sh`, `integrate-lines.py`, `check-063-overlap.py` (+ `.specify/skills/` mirrors), `references/dispatch-recipes.md`, `references/watch-model.md`, `references/cli/index.md`, `references/cli/qodercli.md`.
Tests: `tests/fixtures/line_fixtures.py`, `tests/fixtures/cli_observation.py` (new), the five 064 contract/integration files.
Spec artifacts: `contracts/workspace-isolation.md`, `contracts/line-envelope-and-ingress.md`, `contracts/line-registry.md`, `data-model.md`, `verification.md`, `feature-ref.md`, `notes/063-overlap-adjudication.md`, `notes/quickstart-run.md`, this record and `notes/postreview-logs/`.
