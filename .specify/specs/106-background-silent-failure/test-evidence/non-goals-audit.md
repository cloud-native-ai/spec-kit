# Non-Goals and Zero-Second-Mechanism Audit (T036, spec 106)

Scope: FR-038 (no new mechanism), FR-039 (confirmation-gate budget), FR-040 (non-goals
stay), FR-041 (enforcement honesty, cross-referenced). Every reading below is real output
of the command above it, taken 2026-11-26 on branch `106-background-silent-failure` at
`1f0e9dee5`.

## 1. Zero automatic kill / stop / retry

- `grep -n "os.kill" scripts/python/role-edge-check.py` →
  `1013:        os.kill(pid, 0)` — the single signal is `0` (a liveness probe). The scope
  guard asserts this mechanically: `test_engine_has_no_write_kill_retry_delete_or_push_call`
  also fails if that probe disappears.
- `grep -nE "\bgit\b|push|merge|branch|killall|pkill|retry|unlink|rmtree|delete|notify|smtp|slack|webhook" scripts/python/role-edge-check.py`
  → two hits only: a docstring about retry-as-new-label and a `(candidate / ".git").exists()`
  repo-root check — **no** kill/stop/retry/delete/notify call exists.
- Engine-created attempts: `test_retry_is_a_new_label_and_the_old_attempt_keeps_its_value`
  asserts `summary.attempts == 2` from exactly the two fixture attempts and
  `old_row["claim"] is None` (a stale return is never consumed); the reaction drill
  (`test-evidence/reaction-drill.md`) records engine-created attempts 0, non-zero `os.kill`
  signals 0.
- `grep -nE "\bgit\b|push|merge|retry|kill " skills/internal/create-team/scripts/dispatch.sh`
  → comment/none only; the script's own TERM/INT/HUP traps `exit` the script itself (its
  own process), never another process.
- Only test harnesses kill processes, and only their own children (`DispatchRun.cleanup`,
  the S-1 demo's process-group teardown) — harness hygiene, not product authority.

## 2. Zero push / merge / branch delete / remote rewrite

- The delivered scripts contain **no git invocation** (the scans above cover the engine
  and dispatch.sh; no other script was added by this feature).
- This implement stage performed no `git push`, no merge and no branch deletion (the
  branch is advanced only by local commits; push remains outside the crew's authority).

## 3. Zero evidence deletion / rewrite / history rewrite

- Engine write authority: `test_engine_has_no_write_kill_retry_delete_or_push_call` (AST)
  bans `write_text` / `write_bytes` / `unlink` / `mkdir` / `rename` / `replace` /
  `os.remove` / `os.rename` / … and non-read `open()` modes; the scope module passes
  (below).
- Settlement runs are tree-hash neutral: `test_legacy_annotated_not_compliant` and
  `test_versioned_claim_is_audited` assert fixture hashes before == after; T008 recorded
  `fixture_tree_unchanged=yes`; the T021 drill asserts old-evidence hashes equal.
- Dated records untouched: no source edit rewrote a historical report, spec, or evidence
  file; the only deletions in this stage were its own `.specify/.tmp/` scratch trees
  (`notes/quickstart-run.md` § Teardown).

## 4. Zero new scheduler / registry / queue / storage / notification channel / child list

- `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_scope.py -q`
  → `10 passed in 6.25s` (rc 0). The module mechanically pins:
  - engine imports stay inside the stdlib allowlist (`argparse`, `json`, `os`, `pathlib`,
    `re`, `sys`, `time`, …) — no scheduler/queue/network library;
  - the engine CLI option set is exactly the declared 15 options — no storage root or
    channel gained;
  - `dispatch.sh` still has a single `mkdir -p "${LOG_DIR}"` and writes `.attempt` /
    `.end` only inside that existing log dir;
  - `probe-definitions.md` gained no probe class; the observer stays optional;
  - the carrier inventory stays closed C1…C6.
- `grep -n "mkdir -p\|\.attempt\|\.end\|tee \"" skills/internal/create-team/scripts/dispatch.sh`
  → the single `mkdir -p "${LOG_DIR}"` (line 146) and additive records/lines under it.
- The only new files on the deliverable surface are the additive `tests/` modules and
  fixtures, the docs pointers and the evidence records — no runtime store was created.

## 5. `.status` line, sentinel literals and the preserved surfaces unchanged

- `tests/contract/test_settlement_preservation.py` → `6 passed in 23.27s` (SC-003 run):
  watcher verdict-token / exit-code / sentinel-literal sets equal to `fbab7a45c`
  member-for-member; `--self-test` 39/0; five-element uplink and seven-field downlink text
  unchanged; `report` byte-identical to the baseline; two-slot ledger unchanged.
- `.status` shape: the T011 old-vs-new comparison in `notes/red-first-evidence.md`
  (byte-identical files, identical readings from `journal-utils._field` and the engine)
  plus `test_status_line_shape_is_read_by_the_baseline_reader` remain green in the S-5 run
  (`57 passed`).

## 6. Confirmation-gate budget (EP-005 fallback)

```text
$ python3 scripts/python/scan-confirmation-gates.py --root . --json | head -3
{ "total": 30, ...
```

- Total **30** (base 31; the frozen `== 27` equality was already red at base —
  `test-evidence/confirmation-total-red-at-base.txt` — and is reported as-is).
- Per touched file: **zero NEW** blocking hits — owner page 0 (≤ 1 at base), driver SKILL
  line 190 = 1 (≤ 1 at base), every other touched file 0; pinned by
  `test_settlement_preservation.py::test_confirmation_gate_scan_adds_no_hits_on_touched_files`
  (in the 6-passed run above). No exemption set was widened; wording avoidance only.

## 7. Clause coverage accountant (read-only, recorded as-is)

```text
$ python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/106-background-silent-failure
companion (must be non-empty on a green run): claimed clauses 34, scanned files 329, clause universe 2452, FR universe 41
  [clause-uncovered] pass (785) — 785 uncovered, 0 beyond the frozen baseline
  [fr-uncovered] fail (4) — 37 of 41 FRs cited from citation groups
  [clause-unparsable] fail (111) — 111 files yield no clause id under the owner's forms; …
status: uncovered
```

- `claimed clauses 34` with `clause-uncovered` beyond-baseline **0** — the GATE-3
  criterion.
- `fr-uncovered` 37/41 (FR-036 / FR-037 / FR-039 / FR-040 are not cited by any contract
  clause) and `clause-unparsable` 111 are the frozen structural facts GATE-3 declares as
  reported-not-decisive; the FR-coverage authority remains the tasks file's
  § Requirement Coverage Map (41/41) and the pre-analyze `runtime-stack-row` gate
  (re-run in the final-gate record). Identical to the tasks-stage frozen reading — no
  drift.
