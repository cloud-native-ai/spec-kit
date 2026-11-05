# Analyze-stage checks — 082-self-explanatory-integration

**Stage**: analyze | **Date**: 2026-11-05 | **stage_base**: `2f5ab4bd` (HEAD) | **Branch**: `082-self-explanatory-integration`
**Mode**: read-only on artifacts — no artifact, checklist, registry row or plan-owned file was modified.

## E-1 — Deterministic inputs re-measured this run

```text
$ bash scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
{"REQUIREMENTS_DIR":".../082-self-explanatory-integration","REQUIREMENT_ID":"082","FEATURE_ID":"082",
 "FEATURE_NAME":"Self-Explanatory Framework Integration（不言自明的框架集成）",
 "AVAILABLE_DOCS":["research.md","data-model.md","contracts/","quickstart.md","checklists/","feature-ref.md","tasks.md"],
 "MODE":"C","WRITABLE":true}

$ python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:082-self-explanatory-integration"
flow_class: execution | flow_type: - | source: declaration | marker: null | exit 0

$ python3 .specify/scripts/python/validate-requirements.py .../requirements.md
status: ok | 0 error(s), 0 warning(s) | 194 lines, 21 definition rows, 4 shared strings

$ python3 .specify/scripts/python/validate-tasks.py .../tasks.md
PASS (with warnings): 0 error(s), 32 warning(s)   # every warning class already adjudicated in tasks.md

$ python3 .specify/scripts/python/validate-decision-tensions.py --spec .../082-self-explanatory-integration --json
status: ok, all six labels pass, 0 errors (2 records T-001, T-002)

$ python3 .specify/scripts/python/account-clause-coverage.py --spec .../082-self-explanatory-integration   # never --freeze
claimed clauses (this feature): 34 | baseline: coverage-baseline.txt (513 names)
uncovered beyond baseline: 1 -> constitution-double-landing.contract.md#C-20
FR universe: 12 | FR claimed: 1 | UNCOVERED-FR: FR-001…FR-011 (11)
status: uncovered

$ python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .../082-... --stage plan|tasks
stage=plan  decision=pass errors=0 advisories=0 (fr=12 sc=9 tasks=53)
stage=tasks decision=pass errors=0 advisories=0 (fr=12 sc=9 tasks=53)

$ python3 -m pytest tests/contract/test_constitution_double_landing.py \
      tests/contract/test_instructions_section_propagation.py -q
21 passed in 1.67s
# Load-bearing: this run FALSIFIES tasks.md T006's stated red expectation (see L-02).
```

## E-2 — Read-only proof (validation wave)

```text
$ git status --porcelain | sort > /tmp/git-status-analyze-before.txt   # sha256 f658ef54…4d5e, 27 lines
$ <validation wave: 7 external read-only validators>
$ git status --porcelain | sort | diff /tmp/git-status-analyze-before.txt -
READONLY-PROOF: IDENTICAL
```

One in-passing self-repair is disclosed: an empty `…/082-.../notes/` directory was created by this run
and removed immediately (`rmdir`); the `git status --porcelain` comparison above is byte-identical, so
the wave remains valid. `notes/` is a tasks-stage write target, not an analyze artifact.

## E-3 — stage-status row (six condensed fields)

```json
{"stage": "analyze", "row_type": "stage-status", "status": "not-run-docs-only", "selection_basis": "targeted-set-v1 with stage_base=2f5ab4bd: the analyze stage is read-only on artifacts and produces no executable or mirrored surface change, so the selection program yields the docs-only branch; the one targeted run below was executed as a load-bearing premise test (T006), not as a regression gate", "selection_resolution": "docs-only (no regression set selected)", "test_command": "not-run-docs-only (load-bearing exception: python3 -m pytest tests/contract/test_constitution_double_landing.py tests/contract/test_instructions_section_propagation.py -q)", "test_exit_code": "0 (21 passed)", "test_duration_ms": "1670", "evidence_ptr": "this file (test-evidence/analyze-stage-checks.md) + analyze-stage commit d4d6a396"}
```

## E-4 — Coverage summary

| Metric | Value |
|--------|-------|
| Functional requirements | 12 (FR-001…FR-012) |
| Task rows | 53 |
| Clauses claimed by `[green:]` | 34 of 34 ids |
| Clause lane beyond frozen baseline | 1 (`constitution-double-landing.contract.md#C-20` — declaration-shaped pointer, see L-08) |
| FR lane via clause citation groups | 1 of 12 (the accountant's claimed-FR lane does not read task rows — reported, not treated as a requirement gap; the task→FR lane is verified by inspection in `pre-analyze-check` `fr=12`) |
| Mutation legs | 6 (M-1…M-6) |
| Unchecked `[Gap]` checklist items | 36 of 36 |
| `unchecked + unraised + undispositioned` | **0** (all 36 raised or dispositioned, see H-04) |

## E-5 — Validation wave accounting

| Sent | confirm | downgrade | reject |
|------|---------|-----------|--------|
| 7 (H-01…H-07) | 1 (H-01, already capped at MEDIUM by its propagation surface) | 4 (H-02 → LOW, H-03 → MEDIUM, H-04 → MEDIUM, H-05 → MEDIUM) | 2 (H-06, H-07) |

**Downgrade+reject rate: 6 of 7.** This is reported as a detection-quality signal, not as a clean run:
five of the seven candidates were over-rated before validation, and the two rejects (H-06 glossary path
either/or, H-07 decision-tension census completeness) were claims whose premise the artifacts contradict.
The remediations in the report accordingly tighten the propagation-surface requirement rather than
take the CRITICAL/HIGH count at face value.
