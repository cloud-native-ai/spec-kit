# Requirements Stage Evidence — 109-prompt-adherence

**Run**: `r20261127T053750Z-109a` · **Stage**: `requirements` · **Date**: 2026-11-27
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/prompt-adherence` · **Branch**: `109-prompt-adherence` · **Baseline**: `0419adae5`

Each section below is a captured reading from this run; nothing is hand-scored.

## R-1 — Source-to-target path verification (A-3/A-4)

Input surfaces (must pre-exist; all PRESENT, measured 2026-11-27):

- `scripts/python/declaration_reader.py`, `scripts/python/run-determination.py`,
  `scripts/python/exec-quant.py`, `scripts/python/feedback-utils.py`,
  `scripts/python/evidence-utils.py`, `scripts/python/probe-utils.py`
- `shared/declarations/facts/runtime-store-layout.yaml`,
  `shared/declarations/facts/quant-record-schema.yaml`,
  `shared/declarations/facts/evidence-seven-states.yaml`
- `shared/workflow/symlink-model.md`, `shared/guidelines/better-harness.md`,
  `shared/guidelines/confirmation-gates.md`,
  `shared/definitions/script-interface-definitions.md`
- `scripts/bash/run-tests.sh`, `scripts/python/sync-mirrors.py`, `.specify/instructions.md`

Deliverable paths (ABSENT by design before implementation; this feature creates them):

- `scripts/python/prompt-adherence.py`
- `shared/definitions/prompt-adherence-definitions.md`
- `shared/declarations/facts/prompt-adherence-*.yaml` (five facts)

Read-API and field verification (measured, A-4):

```
run-determination.py: SCHEMA_VERSION=1; COMPARISON_VERDICTS=("improved","unchanged","regressed","not_evaluated");
  CORRECTNESS_VERDICTS=("ok","regressed","not_evaluated"); GOOD_VERDICTS=("improved","unchanged","ok","accepted");
  GREEN_UNPROVEN_VERDICT=("not_evaluated","green_unproven"); FINDINGS_PROJECTION_FIELDS=("id","lane","evidenceState","summary","signals");
  load_determinations(workspace_root); record fields run_id / determined_at
exec-quant.py: KIND="speckit.exec-quant"; SCHEMA_VERSION from quant-record-schema.yaml (=2); load_records(workspace_root);
  record fields run_id / collected_at; storage .specify/exec-quant/ (legacy records.jsonl + records/*.json)
feedback-utils.py: scan_entries(workspace_root) -> frontmatter metadata (id / run_id / created / file); store .specify/feedback/
evidence-utils.py: FINDINGS_KIND="speckit.evidence-findings"; SCHEMA_VERSION=1; SEVEN_STATES from evidence-seven-states.yaml;
  load_index(root) -> entries with file / runId / created; store .specify/evidence/
probe-utils.py: PROBE_DEFS_REL=.specify/shared/definitions/probe-definitions.md; load_probe_registry(workspace_root)
confirmation-gates.md line 93: --run-id "gate:<gate_id>:<UTC ts>"
runtime-store-layout.yaml: stores.* carry NO `root` key; roots are `.specify/<store-name>/` projections (session / feedback /
  evidence / exec-quant present); NO `scripts/python/store_layout.py` in this tree -> A-5 / FR-030 adaptation
```

## Scaffold deviation (A-13)

`create-new-requirements.sh` derives the next number from `.specify/specs/`, archived specs,
local and remote branches. The worktree is already on branch `109-prompt-adherence`, so the
script would derive 110 and create a second branch — incompatible with this line's topology.
Following the 108 A-16 precedent, the spec directory and `requirements.md` were scaffolded
manually from `.specify/templates/requirements-template.md` (verified byte-identical to the
mirror), skipping only the number derivation and branch creation.

## Gate-1 — validate-requirements.py (verbatim, final run)

```
file: .specify/specs/109-prompt-adherence/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
  [path-marker] pass (0)
scanned: 296 lines, 39 definition rows, 2 shared strings
0 error(s), 0 warning(s)
EXIT=0
```

## Gate-2 — pre-analyze-check.py --stage requirements (verbatim, final run)

```
pre-analyze-check: stage=requirements decision=pass errors=0 advisories=3 waived=0
{"stage": "requirements", "decision": "pass", "findings": [{"check": "missing-path", "severity": "advisory", "path": "requirements.md", "line": 160, "message": "path does not exist under the repo: shared/definitions/prompt-adherence-definitions.md"}, {"check": "missing-path", "severity": "advisory", "path": "requirements.md", "line": 160, "message": "path does not exist under the repo: .specify/shared/definitions/prompt-adherence-definitions.md"}, {"check": "missing-path", "severity": "advisory", "path": "requirements.md", "line": 194, "message": "path does not exist under the repo: .specify/scripts/python/prompt-adherence.py"}], "summary": {"errors": 0, "advisories": 3, "waived": 0, "fr": 30, "sc": 9, "tasks": 0, "clauses": 0, "files": 2}, "checked_at": "2026-11-27T05:44:06Z"}
EXIT=0
```

The three advisories are the deliverables this feature creates (owner document, its installed
mirror path, the engine); the gate treats missing deliverable paths as non-blocking advisories.
An earlier run carried a fourth advisory for the source tool's Python package path; the spec
now states the mapping without a dead path literal, and that advisory is gone.

## Gate-3 — decomposition-check.py --mode plan (verbatim)

```
{"mode": "plan", "decision": "proceed", "measured": {"fr_count": 30, "task_count": null, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": [], "checked_at": "2026-11-27T05:43:59Z"}
EXIT=0
```

**Decomposition decision**: `proceed` — one spec, no split required (30 FR rows below the
ceiling; no task rows at this stage).

## Gate-4 — workspace-guard.py (snapshot before gates, check after)

```
python3 scripts/python/workspace-guard.py --snapshot .specify/specs/109-prompt-adherence/test-evidence/workspace-requirements.json --repo .
recorded .specify/specs/109-prompt-adherence/test-evidence/workspace-requirements.json
EXIT=0

python3 scripts/python/workspace-guard.py --check .specify/specs/109-prompt-adherence/test-evidence/workspace-requirements.json --repo .
clean
EXIT=0
```

## Flow-class reading

Dispatch quartet: `flow_class=execution; source=default; marker=; error=owner-unavailable`.
Local lookup: `flow-class-check.py --action lookup --unit-id "/speckit.requirements"` →
`{"flow_class": "execution", "source": "ledger", "marker": null, "basis": "behavior-oracle", "neutral": false, "error": null}`.
Spec header declares `**Flow Class**: execution`, `**Flow Type**: -`. Class agrees; the two
readings differ only in the `source` field.

## Checklist

`.specify/specs/109-prompt-adherence/checklists/requirements.md` — all 17 items pass; counts
derived from the Gate-1 run (296 lines / 39 definition rows / 2 shared strings / 0 errors /
0 warnings), stamped after that run.