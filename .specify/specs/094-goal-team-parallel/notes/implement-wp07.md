# Implement wp07 — closure readings and verification

**Package**: `wp07-closure` (read-only + evidence) · **Rows**: T079–T080 ·
**Branch**: `094-wp07` (base `03efbb1f6`, master @ wp01–wp06 + wp04b) · **Date**: 2026-11-09

**ANOMALY: the worktree lives under the main repo's `.specify/.tmp/`, so engines that self-resolve through a literal `.specify` path component resolve the MAIN repo — `test_ask_record_repeat.py::test_canonical_engine_does_not_self_resolve_to_the_framework_repo` fails exactly on the trap, the trigger family (52 ids) is red for that reason, and the runs mutated the main repo's live `.specify/memory/trigger/index.json` (`updated` 12:30:05Z → 13:04:27Z); the final GATE-1 reading must be re-run serially in the main tree after every `.specify/.tmp` fixture and worktree is removed. Additionally, `migrate-archive --apply` was refused before execution by the host action classifier under this package's read-only dispatch, so T079's applied half and SC-003 remain outstanding.**

## Rows — 1 closed / 2, 1 partially delivered

| Row | State | What landed |
|-----|-------|-------------|
| T079 | **partial** | probe-residual before (goal 8 / teams 8), the baseline comparison against `requirements-baseline-probe.txt`, `migrate-archive --dry-run` (16 decisions = 8 goal + 8 team, 0 conflict, 0 interrupted, receipt bodies rendered) — all recorded one file per reading. `migrate-archive --apply` refused pre-execution by the host action classifier (read-only dispatch); recorded verbatim in `wp07-T079-apply-blocked.txt`. The applied readings (after-probe, existence assertions) do not exist and were not fabricated |
| T080 | **closed** | teardown precondition read (`.specify/.tmp` absent inside the worktree), `sync-mirrors.py --check` OK (the wp06 anomaly is closed by wp04b), `regen-command-copies.py --check` OK, full suite via the canonical runner (205 failed / 8174 passed / 2 skipped; 205-id names list), name-level deltas (161 new vs plan's stale 46; 94 new / 2 fixed vs the 113-id implement-entry baseline), per-module attribution digest, the validation/decomposition/pre-analyze/script-interface gates, the per-criterion status block and the closure verdict — all in `notes/closure-readings.md` |

## Closure verdict (verbatim, `wp07-closure-acceptance.txt`)

```
verdict: block
final_path: pass=6 blocked=1 deferred=0 partial=1 fail=1 unknown=0 total=9
reason: final-path-not-pass: SC-001
reason: final-path-not-pass: SC-002
reason: final-path-not-pass: SC-003
```

Criteria: SC-001 fail (no guard module, no create-binding write — wp03's blocked
T016–T019), SC-002 partial (stale `EXPECTED_WRITE_ACTIONS` pin vs wp04b's `handoff-ref`),
SC-003 blocked (apply unauthorized), SC-004…SC-009, SC-011, SC-012 pass, SC-010 fail
(disposal rewrites unowned + disposal-table exclusion drift).

## Readings (one file per reading, under `test-evidence/`)

- Suite: `wp07-closure-suite.out` / `.err` / `-meta.txt`, `closure-failed.txt`,
  `wp07-closure-new-vs-plan.txt`, `wp07-closure-new-vs-implementation.txt`,
  `wp07-closure-fixed-vs-implementation.txt`, `wp07-closure-attribution.txt`,
  `wp07-trigger-family-serial.txt` (63-id serial probe proving the family is not a
  scheduling artifact).
- T079: `wp07-T079-probe-before.txt`, `wp07-T079-dryrun.txt`, `migration-dryrun.json`,
  `wp07-T079-apply-blocked.txt`, `wp07-T079-baseline-comparison.txt`.
- Gates: `wp07-validate-requirements.txt`, `wp07-validate-tasks.txt`,
  `wp07-validate-decision-tensions.txt`, `wp07-pre-analyze-{requirements,plan,tasks}.{txt,json}`,
  `wp07-decomposition-{plan,tasks}.{txt,json}`, `wp07-mirror-check.txt`,
  `wp07-copy-check.txt`, `wp07-script-interface.txt`.
- Smoke: `wp07-smoke.txt` (command + exit 0) and `wp07-smoke.out` (**54 passed**).
- Verdict: `wp07-closure-acceptance.txt` / `.json`.

## Residual risks for the driver

Full list and evidence in `notes/closure-readings.md` § 3. The load-bearing ones:

1. T079's apply (SC-003) needs explicit authorization; the dry-run plan is ready.
2. SC-001 has neither guard nor implementation; T016–T019 need an owner or a re-scope.
3. SC-002 needs one pin line (`handoff-ref`); SC-010 needs the disposal wave and the
   exclusion-list repair; two further feature-introduced reds are one-line repairs
   (`qoder_command_frontmatter` goal.md description, `summary_trigger` retired path pin).
4. GATE-1 cannot be read from a nested worktree; re-run it in the main tree after teardown.
   The main repo's `.specify/memory/trigger/index.json` was mutated by the contaminated
   runs; wp07 did not restore it (shared-tree write outside its guard) — the driver decides.
5. All 85 task sigils remain `- [ ]`; the row-state sweep belongs to integration close-out.

## Commits

- `docs(094-wp07): closure readings and verification statuses` — this note, the closure
  readings, `verification.md` and the `wp07-*` evidence files (explicit paths; no push).
