# Checklist-Stage Evidence — Feature 082

**Stage**: `/speckit.checklist` | **Date**: 2026-11-05 | **Stage base**: `24c27f81`
**Unit**: `spec:082-self-explanatory-integration` (`flow_class=execution`, `source=declaration`,
`marker=null`, `error=-`; read once via `flow-class-check.py --action lookup`, exit 0)

## E-0 — Stage character

Documentation-only. The stage produces one Markdown checklist plus this evidence file. No executable
surface (`.py`, `.sh`, `.md` consumed as a test fixture, or mirrored artifact) is changed, so the
behavioural test selection is not owed. The checklist itself is an instrument for judging requirement
text; running it is a review activity, never a program execution.

## E-1 — Inputs re-measured (not inherited)

Every figure below was produced by a command in this run, per
`shared/workflow/objective-analysis-gate.md` rule 8 (derive briefing premises mechanically).

```console
$ python3 scripts/python/flow-class-check.py --action lookup --unit-id "spec:082-self-explanatory-integration"
unit_id: spec:082-self-explanatory-integration
flow_class: execution
source: declaration
EXIT=0

$ bash scripts/bash/check-prerequisites.sh --json
REQUIREMENTS_DIR=/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration
AVAILABLE_DOCS=[research.md, data-model.md, contracts/, quickstart.md, checklists/, feature-ref.md]

$ grep -cE '^- \*\*FR-00[0-9]\*\*' requirements.md      → 12 FR
$ grep -cE '^- \*\*SC-00[0-9]\*\*' requirements.md      →  9 SC
$ grep -cE '^\| `STR-00[0-9]`' requirements.md          →  4 Shared Strings
$ grep -cE '^- \*\*A[0-9]+' requirements.md             → 11 assumptions
$ grep -cE '^- \[ \] T[0-9]{3}' tasks.md                → 53 task rows
$ contract clause ids parsed from contracts/*.md        → 34 (C-1…C-34)
$ [green:] claims parsed from tasks.md                  → 45 markers / 34 unique; 0 unclaimed, 0 phantom
$ mutation legs parsed from contracts/*.md              →  6 (M-1…M-6)
```

Task/contract reconciliation was program-derived (set difference both directions), not read off the
task narrative: all 34 clauses are claimed exactly once and no `[green:]` marker names a clause that
does not exist.

## E-2 — Baseline facts the checklist leans on

```console
$ grep -cF 'Self-Explanatory Structure (不言自明)' templates/constitution-template.md \
      .specify/memory/constitution.md templates/instructions-template.md .specify/instructions.md
templates/constitution-template.md:0
.specify/memory/constitution.md:0
templates/instructions-template.md:0
.specify/instructions.md:0
# pre-change state; the feature's landing obligation is unfulfilled by construction

$ grep -cE '^### [IVXLC0-9]+\. ' templates/constitution-template.md .specify/memory/constitution.md
templates/constitution-template.md:17
.specify/memory/constitution.md:18

$ wc -c .specify/instructions.md                  → 32739
$ grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh
38:INSTRUCTIONS_BUDGET_BYTES=32768

$ python3 scripts/python/sync-mirrors.py --check | grep -E '^(ok|OK)'
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (65 files)
```

All six pairs report `ok` — including `shared/`, which carries the three owner documents — and the
per-tool command-copy line is `OK`. This confirms the plan-stage baseline (`--check` exit 0, 65
`shared` files) still holds at this stage base.

## E-3 — Checklist artifact invariants (machine-checked)

Re-parsed after the last edit, with hard-wrapped continuation lines joined:

```console
items: 36
sequential CHK001…CHK036: True   duplicates: False
traceable ([Req §…] / [Gap] / [Ambiguity] / [Assumption] / [Coverage]): 36/36 = 100.0%  (floor 80%)
every item in question form: True
prohibited openers (Verify/Test/Confirm/Check + behaviour): none
soft cap (<= 40): satisfied (36)
```

## E-4 — E3 stage-status row

```json
{"stage": "checklist", "row_type": "stage-status", "status": "not-run-docs-only", "selection_basis": "targeted-set-v1 with stage_base=24c27f81: the checklist stage produces one Markdown checklist plus this evidence file and touches no executable or mirrored surface, so the selection program yields the docs-only branch (spec: 'checklist 是 docs-only, 记录 status=not-run-docs-only 与六个精简字段到 EVIDENCE_DIR 的 E3 stage-status 行'); behavioural checks were replaced by the deterministic input re-measurements in E-1/E-2 and the artifact-invariant parse in E-3", "changed_paths": [".specify/specs/082-self-explanatory-integration/checklists/requirements-quality-20261105.md", ".specify/specs/082-self-explanatory-integration/test-evidence/checklist-stage-checks.md", ".specify/state/082-self-explanatory-integration.md"], "selection_resolution": "docs-only (no test set selected)", "test_command": "not-run-docs-only", "test_exit_code": "n/a", "test_duration_ms": "n/a", "evidence_ptr": "this file (test-evidence/checklist-stage-checks.md) + the checklist-stage commit"}
```

Six trimmed fields carried: `selection_basis`, `selection_resolution`, `test_command`,
`test_exit_code`, `test_duration_ms`, `evidence_ptr`.

## E-5 — Pre-existing red carried forward (not repaired here)

`tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` remains red at
this stage base (frozen 23 vs live scan 27). Per `plan.md` § Execution Premises EP-003
(`Decision: fallback`) it is named by identity here rather than reported as clean. Nothing in this
stage ran or repaired it.

## E-6 — Observations for the next stage

- The checklist file is the **only** new spec artifact; `checklists/requirements.md` (the upstream
  specification-quality checklist) is untouched, as required.
- Items CHK001, CHK002, CHK012, CHK014, CHK026 and CHK032 flag places where `requirements.md` is
  silent about an obligation that plan-stage contracts or tasks-stage notes carry. Those are
  **requirement-text gaps**, not plan defects: the repair, if any, belongs to a future requirements
  revision and must not be folded into the plan-owned artifacts.
