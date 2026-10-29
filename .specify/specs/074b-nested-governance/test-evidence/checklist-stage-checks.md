# Checklist-stage deterministic checks — 074b-nested-governance

**Stage**: `/speckit.checklist` · **Slice**: `074b-nested-governance` · **Feature**: 074
**Stage base**: `61496b869` (tasks DONE) · **Captured**: 2026-10-29
**Single-run evidence discipline**: every command below was executed once in this stage and its
decisive output is pasted here, so no follow-up question needs a re-run. No expensive test run
was performed — see § 5 for the test-budget rows and their stated basis.

---

## 1. Structural validator — `validate-requirements.py`

```text
$ python3 .specify/scripts/python/validate-requirements.py .specify/specs/074b-nested-governance/requirements.md
file: .specify/specs/074b-nested-governance/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 308 lines, 10 definition rows, 7 shared strings
0 error(s), 0 warning(s)
exit=0
```

`ref-resolvable` is bidirectional, so this single result establishes both halves of CHK028:
every `[[STR-nnn]]` citation resolves, and no Shared Strings row is defined-but-uncited.

---

## 2. Cross-artifact gate — `pre-analyze-check.py`

The gate accepts `--stage {requirements,plan,tasks}` only; `--stage checklist` is rejected:

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
    --spec-dir .specify/specs/074b-nested-governance --stage checklist --repo .
pre-analyze-check.py: error: argument --stage: invalid choice: 'checklist'
                            (choose from 'requirements', 'plan', 'tasks')
```

Recorded as a fact rather than worked around: the closest available cross-artifact read is the
last stage's view, which was executed and is pasted next.

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
    --spec-dir .specify/specs/074b-nested-governance --stage tasks --repo .
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=21 waived=0
{"stage": "tasks", "decision": "pass", ... "summary": {"errors": 0, "advisories": 21,
 "waived": 0, "fr": 8, "sc": 2, "tasks": 26, "clauses": 0, "files": 11},
 "checked_at": "2026-10-29T04:58:07Z"}
exit=0
```

All 21 advisories are `missing-path` on three planned, not-yet-created test files —
`tests/contract/test_nested_run_report.py` (7 rows), `tests/contract/test_sdd_diffusion.py`
(5 rows), `tests/contract/test_sdd_compat_containment.py` (4 rows), plus repetitions across
`plan.md` / `tasks.md` / `quickstart.md` / `research.md` / `feature-ref.md` / `contracts/*.md`.
Every one is the expected pre-implementation state (tasks' red-first rows T004 / T010 / T019
create them), so none is a requirement defect and none is waived.

---

## 3. Decomposition gate — `decomposition-check.py --mode tasks`

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks \
    --requirements .specify/specs/074b-nested-governance/requirements.md \
    --tasks .specify/specs/074b-nested-governance/tasks.md
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 8, "task_count": 26,
 "fr_ceiling": 30, "task_ceiling": 40}, "reasons": [], "checked_at": "2026-10-29T04:58:07Z"}
exit=0
```

---

## 4. Structural recounts behind the checklist's counts

Every number quoted inside `checklists/readiness-2026-10-29.md` is one of these, re-derived at
this stage rather than copied from another artifact.

```text
$ cd .specify/specs/074b-nested-governance
FR definition rows      : grep -cE '^\- \*\*FR-[0-9]{3}\*\*:' requirements.md          -> 8
SC definition rows      : grep -cE '^\- \*\*SC-[0-9]{3}\*\*:' requirements.md          -> 2
Shared-Strings rows     : grep -cE '^\| .STR-[0-9]{3}.' requirements.md               -> 7
Parent Mapping FR rows  : grep -cE '^\| .FR-[0-9]{3}. \| Parent FR' requirements.md   -> 8
Parent Mapping SC rows  : grep -cE '^\| .SC-[0-9]{3}. \| Parent SC' requirements.md   -> 2
Parent Mapping STR rows : grep -cE '^\| STR-[0-9]{3} \|' requirements.md              -> 7
Given scenarios         : grep -c '\*\*Given\*\*' requirements.md                     -> 6
User stories            : grep -cE '^### User Story' requirements.md                  -> 2
Edge-case rows          : sed -n '/### Edge Cases/,/## Requirements/p' | grep -cE '^- \*\*' -> 5
Assumption rows         : grep -cE '^- \*\*A[0-9]+\*\*' requirements.md               -> 5
NEEDS CLARIFICATION     : grep -c 'NEEDS CLARIFICATION' requirements.md               -> 0
lines                   : wc -l < requirements.md                                     -> 307 (+1 trailing-newline count in the validator's 308)
STR citation census     : grep -oE '\[\[STR-[0-9]{3}\]\]' requirements.md | sort | uniq -c
                          -> 001:2  002:4  003:2  004:2  005:2  006:2  007:2
```

---

## 5. Test Budget Record (targeted-set-v1, `stage_base=checklist`)

**E3 stage-status row (docs-only)** — `stage=checklist`, `row_type=stage-status`,
`status=not-run-docs-only`, `selection_basis=no executable surface changed by this stage（本阶段只新增
一份检查单与这份证据文件，未触碰任何被测试的 owner、引擎或测试文件，故全量与定向套件都无新主体）`,
`changed_paths[]=.specify/specs/074b-nested-governance/{checklists/readiness-2026-10-29.md,test-evidence/checklist-stage-checks.md}`,
`evidence_ptr=.specify/specs/074b-nested-governance/test-evidence/checklist-stage-checks.md`.
Run fields do not apply and are not reported as `unknown`.

**Full-suite row** — same shape, `status=not-run-docs-only`, same `selection_basis` and
`evidence_ptr`; the full baseline / closure slots belong to the `implement` and `review` stages
and are not pre-empted here.

No targeted set was executed: the three program checks in § 1–§ 3 are deterministic validators,
not tests, and the requirements file they read is unchanged by this stage (verified in § 7).

---

## 6. Suite-membership derivation check (the mechanical basis for CHK018)

```text
$ grep -nE '^## S[0-9]' test-evidence/compat-baseline-nodeids.txt
## S1-pre-dispatch-governance        (2 files)
## S2-standalone-driver-entry        (1 file)
## S3-070-stage-team-preset          (2 files)
## S4-064-line-worktree-ownership    (3 files)
## S5-058-u0-u6                      (2 files)
## S6-team-suites                    (4 files)
## S7-agent-suites                   (3 files)

$ grep -rn 'test_non_regression_070|contract-suite case set' \
    .specify/specs/074-goal-team-sdd-unification/contracts/diffusion-and-compat.md
C-61 ... contract-suite case set is a superset of the pre-change case set captured at the baseline commit
C-62 ... The case set of each named suite is its collected test-node-id set
  -> no per-surface file list anywhere in the parent contracts

$ grep -n 'belongs to 074b-nested-governance' \
    .specify/specs/074a-authorized-routing/test-evidence/targeted-set-v1-baseline.txt
... the slice makes no superset claim over them (that claim is parent FR 027's and belongs to
    074b-nested-governance).
```

Conclusion carried into the checklist: the seven sets and their 17 files exist **only** in this
slice's own evidence carrier; neither the parent design nor `074a`'s committed baseline maps a
named surface to a file set at requirement level. That is why CHK018 is scored `fail` even
though this slice's clarify stage had recorded the item as settled.

---

## 7. Edits-not-made audit

```text
$ git status --short .specify/specs/074b-nested-governance .specify/specs/074-goal-team-sdd-unification .specify/specs/074a-authorized-routing
?? .specify/specs/074b-nested-governance/checklists/readiness-2026-10-29.md
?? .specify/specs/074b-nested-governance/test-evidence/checklist-stage-checks.md
```

Only the two new files. `requirements.md`, `plan.md`, `data-model.md`, `contracts/**`,
`quickstart.md`, `research.md`, `feature-ref.md`, `tasks.md`, `checklists/requirements.md`, the
parent spec and the sibling slice are untouched — no `PLAN-EDIT` is declared because no
plan-owned line was changed.
