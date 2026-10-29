# Checklist stage checks — 076-decision-tension-contract

**Date**: 2026-10-29 18:16 CST
**Branch**: `076-decision-tension-contract`
**HEAD at run**: `051c1e81aaee27215453afb081f7c2fab6e4427a` (tasks wrap-up)
**Stage base commit (spine)**: `920e0f8d`
**Working tree before checklist generation**: clean (`git status --short` empty)

## 1. Required structure check

Command:

```bash
python3 scripts/python/validate-requirements.py .specify/specs/076-decision-tension-contract/requirements.md
```

Verbatim output:

```text
file: .specify/specs/076-decision-tension-contract/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 287 lines, 34 definition rows, 4 shared strings
0 error(s), 0 warning(s)
```

Exit code: `0`.

Interpretation: all five structural propositions pass. 34 definition rows = 26 FR + 8 SC; 4 shared strings; no marker, duplicate-id, document-order or reference-resolution error. The checklist stage may proceed.

## 2. Deterministic cross-checks used by the checklist

### 2.1 Declared counts

```text
FR=26
SC=8
US=5
STR=4
MEASUREMENT_SOURCES=8
MIRROR_ROWS=7
TASK_ROWS=27
```

### 2.2 Clause coverage

Command:

```bash
python3 scripts/python/account-clause-coverage.py .specify/specs/076-decision-tension-contract
```

Filtered output (full output is large because it enumerates the frozen baseline):

```text
claimed clauses (this feature): 34
uncovered beyond baseline: 0
FR claimed: 26
companion (must be non-empty on a green run): claimed clauses 34, scanned files 223, clause universe 1349, FR universe 26
  [clause-uncovered] pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [coverage-baseline-delta] pass (0) — baseline holds 495 names; 495 uncovered items are baseline-internal and do not block
status: ok
```

Exit code: `0`.

### 2.3 Mirror baseline

Commands:

```bash
python3 scripts/python/sync-mirrors.py --check
python3 scripts/python/regen-command-copies.py --check
```

Verbatim output:

```text
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (406 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (115 files)
ok    shared/ == .specify/shared/ (59 files)
```

`regen-command-copies.py --check` output:

```text
OK: all per-tool command copies match the source templates.
```

Both exit codes: `0`. This is the pre-edit baseline the plan and tasks cite; the checklist does not treat the bare exit code as an absolute criterion.

### 2.4 Source surfaces measured

```text
templates/plan-template.md: ## Constitution Check line 31, ## Project Structure line 62 (currently adjacent; T005 inserts between them)
docs/decisions/template.md: ## Alternatives line 15 (no tension_id slot yet; T020 adds it)
skills/internal/analyze-artifacts/references/detection-and-severity.md: ## The seven passes line 39, subsections A–G
skills/internal/analyze-artifacts/SKILL.md: "Seven passes ... plus one checklist pass (H)"
shared/guidelines/decision-tension.md: absent (T004/T006 create it)
scripts/python/validate-decision-tensions.py: absent (T007/T008 create it)
scripts/python/validate-falsification-quartet.py: absent (T015 creates it)
tests/contract/test_decision_tension_contract.py: absent (T002/T009/T013/T017/T019/T021 create it)
tests/contract/test_decision_tension_validator.py: absent (T003 creates it)
tests/contract/test_falsification_quartet_validator.py: absent (T012 creates it)
```

### 2.5 Terminology baseline

Command shape: `grep -rF "<alias>" shared templates skills | wc -l` for each A3 alias.

```text
矛盾论: 0
主要矛盾: 0
矛盾的主要方面: 0
对抗性矛盾: 0
矛盾转化条件: 0
```

The A3 alias list is still present in `requirements.md` line 42, so the zero-hit check has a positive control and is not vacuous.

## 3. Dated-record note: 255 vs 287 lines

The requirements-stage evidence file `.specify/specs/076-decision-tension-contract/test-evidence/validate-requirements.txt` records `scanned: 255 lines, 34 definition rows, 4 shared strings`. The current run records `287 lines` because the clarify round added prose. The definition counts are unchanged at 34 rows and 4 shared strings, so no derived FR / SC / STR count is stale. Both numbers are dated measurements, not competing current facts.

## 4. Zero-modification statement

- No `requirements.md`, `plan.md`, `data-model.md`, `contracts/*`, `tasks.md`, `quickstart.md`, `research.md` or `feature-ref.md` was edited by this stage.
- No `PLAN-EDIT:` declaration was made.
- The only new paths are the checklist and this evidence file.
- `tasks.md` remains at 27 unchecked task rows; no task was executed.

## 5. Result

- Checklist file: `.specify/specs/076-decision-tension-contract/checklists/readiness-2026-10-29.md`
- Items: 37 (27 pass / 10 fail)
- Structure check: `status: ok`, exit 0
- Clause coverage: `claimed 34`, `uncovered beyond baseline 0`, `FR claimed 26`, `status: ok`
- Mirror baseline: six pairs `ok`, command-copy check `OK`, both exit 0
