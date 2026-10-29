# S7 — end-to-end orchestration dry-run decision trace (recorded, non-CI)

Date: 2026-10-20. This is a recorded decision trace, not a nested driver launch
(the skill's Hard Requirement 6 forbids nested driving). The deterministic
components were actually executed; the LLM-orchestrated stage sequence is the
documented decision path. The trace is non-CI evidence.

## Line A — entry carries `fast-lane=opt-in` (fast lane)

| Step | Decision | Evidence |
|------|----------|----------|
| U0 entry | literal `fast-lane=opt-in` present; recorded in the state spine | medium fixture `entry.md` |
| U1 | requirements → clarify → plan → tasks chain runs | stage chain, `references/dispatch-recipes.md` Recipe 4 |
| tasks U4 | pass (artifacts exist) | tasks U4 program |
| admission point | `admission-check.py` → exit `0`, `decision=fast-lane`, `measured.fr_count=12`, `measured.task_count=25`, seven criteria `a…g` all `pass` | actual run, see below |
| E1 record | write admission record + `checklist=skipped(fast-lane)` before dispatch | `references/efficiency-model.md` §1.3 |
| checklist | **skipped** (authorized) | E1 record + skip marker |
| analyze | dispatched, gate unchanged | fast lane keeps analyze |
| implement | dispatched; E2 baseline full suite at start (`run-tests.sh --names-out`); no second full suite | efficiency-model §2 |
| review | dispatched with the fast-lane conditional block; gate unchanged | stage-prompts fast-lane blocks |
| closure | driver runs the closure full suite after review, `comm -13` name diff, appends E2 closure to the same spine, audits | S3 evidence |
| merge | local merge after closure; push remains gated | Recipe 4 |

Actual admission output (2026-10-20):

```json
{"decision": "fast-lane",
 "entry_evidence": "# Entry\n\nfast-lane=opt-in",
 "criteria": [{"id":"a","verdict":"pass","evidence":"FR definitions=12 in [8,30]; task rows (narrow)=25 in [10,40]"},
              {"id":"b","verdict":"pass"},{"id":"c","verdict":"pass"},
              {"id":"d","verdict":"pass"},{"id":"e","verdict":"pass"},
              {"id":"f","verdict":"pass"},{"id":"g","verdict":"pass"}],
 "measured": {"fr_count": 12, "task_count": 25},
 "checklist": "skipped(fast-lane)",
 "checklist_marker": "checklist=skipped(fast-lane)"}
```

Exit `0`.

## Line B — control without the literal (full chain)

Same fixture and branch, entry replaced with `no opt-in here`:

```json
{"decision": "full-chain",
 "entry_evidence": "# Entry\n\nno opt-in here",
 "measured": {"fr_count": 12, "task_count": 25},
 "checklist": "executed",
 "checklist_marker": "checklist=executed",
 "reasons": ["entry evidence does not carry fast-lane=opt-in"]}
```

Exit `1`. Expected sequence: `requirements → clarify → plan → tasks →
checklist → analyze → implement (baseline) → review → closure → merge`; no E1
fast-lane record and no skip marker.

## Deterministic components referenced by this trace

- S1/S2 (`notes/quickstart-run.md`) — admission/refusal.
- S3 — two-slot ledger audit (`slots=baseline:1 closure:1`, `stages=N complete=N`).
- S4 — derived live log sentinel behavior (INCOMPLETE for non-terminal wording,
  DONE only from the terminal result).
- S5 — local nohup survival and `--once` verification.
- S6 — plan change classification (undeclared → exit 1).
- SC-010 replay — `notes/stall-behavior-baseline-final.json`, `differences: []`
  (see below).

## SC-010 behavior replay (same fixture, `initial_retries=0`)

```text
PASS: replay matches baseline
timeout      TIMEOUT    {"watcher": 14, "runner": 124} stalled-timeout      retries=0 dispatch=no
retry-limit  FAILED     {"watcher": 12, "runner": 1}   stalled-retry-limit retries=2 dispatch=no
fake-done    INCOMPLETE {"watcher": 15, "runner": 0}   incomplete-fake-done retries=0 dispatch=no
```

Normalization removes timestamps, PIDs, absolute paths and durations; the
comparison is field-by-field. Recorded trace is supplemental; the executable
fixture produced the tuples (SB-2/SB-5).

## Non-CI statement

The stage sequence above was not replayed by a real nested driver. CI covers the
deterministic scripts and contract clauses only; this trace is labelled as
recorded evidence in `verification.md`.
