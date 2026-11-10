# Review-Repair Dispositions — r1 (2026-11-10)

- **Dispatch**: review-repair r1 for `096-sdd-observer-agent` (review.md 2 P0 + 2 P1; code-review.md BLOCKING / IMPORTANT / SUGGESTION).
- **Base commit**: `86f3a546a` (worktree `096-sdd-observer-agent`).
- **Category quadruple (this run)**: `flow_class=execution`; `source=declaration`; `marker=`（空）; `error=-`.
- **State spine**: `/storage/project/cloud-native-ai/spec-kit/.specify/state/096-sdd-observer-agent.md` — read only by this repair; no spine write was performed here (spine carriage is the driver's own duty).
- **Evidence dir**: `.specify/specs/096-sdd-observer-agent/test-evidence/`.
- **Scope**: only the repair products below are committed; the pre-existing untracked `checkpoints/` directory is not touched.

## 1. AF-1 (P0) — `verification.md` written; closure checker rerun to `accept`

- **Action**: created `.specify/specs/096-sdd-observer-agent/verification.md` — one `SC-001…SC-007_status=` row per Success Criterion (statuses drawn from the closed six-value vocabulary), each with `value` / `note` evidence pointers; `RS-003_joint_acceptance=pass` for the one `in-scope` runtime-stack row; the smoke triple `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`. The statuses are the verdict-justified ones; no status was changed after the checker ran.
- **Reading**: `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/096-sdd-observer-agent --json` → `"verdict": "accept"`, exit `0`; `reasons: []`; `final_path: pass=4 / total=4`; `completion_conditions`: all four `true`; `smoke.evidence_exists: true`.
- **Evidence**: `test-evidence/review-repair-r1-closure-acceptance.txt`; smoke capture `test-evidence/review-repair-r1-smoke.txt`.
- **Assertion strength**: unchanged — GATE-4 is now actually decidable and reads pass; the checker remains the sole judge.

## 2. IM-1 (P0) — anomaly projection scans the log's last `ANOMALY:` line

- **Root cause**: `_project_candidates` read only the final non-empty log line, so an `ANOMALY:` line followed by a green stage's completion sentinel was silently dropped (FR-012 / US1 AS2).
- **Change**: new `_last_anomaly()` (`scripts/python/journal-utils.py:202`) returns the log's last `ANOMALY:` line; the anomaly projection now tests it (`:632`) instead of `last_line.startswith(...)`. The stage-verdict sentinel rule is untouched (still "last non-empty line == sentinel").
- **Contract case**: `tests/contract/test_journal_engine.py:367` `test_anomaly_before_sentinel_is_recorded` feeds a log whose `ANOMALY:` line precedes the completion sentinel and asserts exactly one `anomaly` row (stage + runtime log pointer) **and** that the same stage still yields its `stage-verdict` row; `check` stays exit 0.
- **Owner sync**: `data-model.md` E-6 `anomaly` row now reads "the stage log's last `ANOMALY:` line, even when a completion sentinel follows it" (the old wording described the defect).
- **Red/green probe** (`test-evidence/review-repair-r1-red-green-probe.txt`): pre-fix engine (`git show HEAD:…`) → `anomaly_rows: 0` with the sentinel present; fixed engine → `anomaly_rows: 1`, `stage_verdict_rows: 8`.

## 3. IM-2 (P1) — indented owner record block parses

- **Root cause**: `OBSERVER_HEADING_RE` anchored at column 0, while the shape owner (`skills/external/sdd-loop-driver/SKILL.md` § SDD Observer, fenced block) indents the heading by two spaces; a verbatim copy made `append` exit 2 (`identity-mismatch: no observer record section`).
- **Change**: `read_spine()` strips leading whitespace before matching the observer heading and before the `## ` section-reset test (`scripts/python/journal-utils.py:227` region). Both the indented owner text and unindented spines parse; the owner text itself is unchanged, so no SKILL.md edit and no mirror re-sync of the skill was needed (mirror parity re-verified below).
- **Contract case**: `tests/contract/test_journal_engine.py:295` `test_owner_literal_record_block_is_accepted` extracts the fenced block **from the owner file itself**, substitutes the fixture identity, strips the fixture's unindented record so the indented block is the only section, asserts the block really is indented (teeth), and requires `append` exit 0 + an `observer-start` row + clean `check`.
- **Red/green probe**: pre-fix engine → exit `2`, `journal-utils: identity-mismatch: no observer record section`; fixed engine → exit `0`.

## 4. AF-2 (P1) — DoD-4 / GATE-1 aligned on one decidable criterion

- **Criterion now stated identically in both places**: `/speckit.implement` Step 0 first captures the implement-entry baseline (`run-tests.sh --names-out <baseline>` before the first edit); the per-name delta against that file must then be empty. The re-interpretation "zero NEW = attributable to this line" is removed.
- **This line's reading**: `DEFERRED` — no Step 0 baseline was captured; the same-day reconstructed baseline leaves a literal 11-id delta (`test-evidence/full-suite.txt` §B–§C). Every one of the 11 ids is now named with its owner in new tasks.md § GATE-1 DEFERRED set (9 trigger-suite order/store-sensitive ids that pass targeted; 2 ids failing identically at the base tree, owner: repo-level `.specify/memory/trigger/index.json`). Zero 096 module id is in the delta.
- **DoD Status** updated: `6 of 8 met, 2 deferred with named owners`; DoD-4's runner half is met, its delta half is `DEFERRED`; DoD-7 (GATE-4) is recorded as discharged by `verification.md`.
- **Structural re-checks**: `validate-tasks.py` → exit 0, `0 error(s)`, same 4 disclosed warnings as § Green Attribution; `pre-analyze-check.py --stage tasks` → `decision=pass`, 47 task rows.

## 5. Code SUGGESTION — title parsing has no consumer

- **Choice**: **drop `title` from the parsed structure** (option 2 of the two the review offers), not a new V rule. Evidence: `grep -n "self.title" scripts/python/journal-utils.py` → 0 hits after the change (before: the two write-only assignments); no test, finding, contract clause or report reads `Journal.title`. A checker V rule would need a new rule number beyond the counted `V-1…V-20` inventory (plan / feature-ref / tasks count 20 rules), a wider change than this repair warrants.
- **Behavior**: unchanged — the title was never compared with `title_template`; the dead attribute only implied a validation that did not exist. The first-line skip in `_parse` is preserved (index still starts at 1).

## 6. Re-run readings (final tree)

| Command | Reading | Evidence |
|---------|---------|----------|
| `bash scripts/bash/run-tests.sh tests/contract/test_journal_engine.py tests/contract/test_sdd_observer_lifecycle.py -q` (mandated) | `41 passed`, exit 0, 8 s | `test-evidence/review-repair-r1-mandated-suite.txt` |
| Feature smoke: `… test_journal_engine.py test_sdd_observer_agent.py test_sdd_observer_lifecycle.py test_sdd_loop_driver_skill.py -q` | `77 passed` + `1 passed` (serial), exit 0, 28 s | `test-evidence/review-repair-r1-smoke.txt` |
| `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/096-sdd-observer-agent --json` | `verdict: accept`, exit 0 | `test-evidence/review-repair-r1-closure-acceptance.txt` |
| `python3 scripts/python/sync-mirrors.py --check` | exit 0, no NEW drift (journal-utils source/mirror byte-identical) | this record; `sync-mirrors.py --write --only scripts` ran before the check |
| GATE-6: `journal-utils.py --version` / `--bogus-option` | `journal-utils.py 0.0.22` / exit 2 | this record |
| `python3 .specify/scripts/python/validate-tasks.py .specify/specs/096-sdd-observer-agent/tasks.md` | exit 0, `0 error(s)`, 4 disclosed warnings | this record |

## 7. Anomalies and in-passing repairs (fast-fail disclosure)

- **Unhandled anomalies: 0.**
- In-passing repair 1 (probe harness): the first pre-fix engine probe omitted the sibling `declaration_reader.py`, so the copy degraded to `owner-unavailable` (the engine's declared C-11 behavior) instead of exercising the defect. Fixed by copying the reader beside the probe copy; disclosed in the probe evidence header.
- In-passing repair 2 (test teeth): the first owner-block drill appended the indented section after the fixture's existing unindented record, which masked the parse failure. The drill and the probe now strip the unindented record so the indented block is the only section — this is what makes the red leg reproducible.

## 8. Committed files (this repair only)

- `scripts/python/journal-utils.py` + `.specify/scripts/python/journal-utils.py` (mirror, byte-identical)
- `tests/contract/test_journal_engine.py`
- `.specify/specs/096-sdd-observer-agent/verification.md` (new)
- `.specify/specs/096-sdd-observer-agent/tasks.md` (DoD-4, DoD Status, GATE-1, § GATE-1 DEFERRED set)
- `.specify/specs/096-sdd-observer-agent/data-model.md` (E-6 `anomaly` row)
- `.specify/specs/096-sdd-observer-agent/test-evidence/review-repair-r1-*.txt` (4 readings)
- this disposition record

Not committed: `skills/external/sdd-loop-driver/SKILL.md` (unchanged — the parser adapts to the owner, not the reverse), review.md / code-review.md (review records, not repair products), the untracked `checkpoints/` directory (not this repair's artifact).
