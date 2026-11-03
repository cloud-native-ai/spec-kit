# Analyze-Fix Report — Feature 081, slice 081a

**Analyze input**: C=0 H=3 M=11 L=6 (gate fail)
**Result**: 3 HIGH and the gate-affecting MEDIUMs repaired spec-only; `analyze-r2` is the verification step.
**Executed by**: analyze-fix subagent (edits), completed/validated/committed by the driver after the subagent reached its 120-turn limit before commit. This is disclosed, not hidden.

## HIGH

| Finding | Change | Landing |
|---|---|---|
| H-01 (CHK017) `inherited` obligation | FR-011 now defines `resolved` / `inherited` / `not-applicable`; `inherited` MUST name a reachable carrier (mandatory task+test or gate) and MUST NOT be a deferrable `supporting` SC. SC-005 measures carrier existence. Plan IB-004/006/007 name actual carriers (`test_acceptance_review_composition.py`, `test_acceptance_premises.py`) instead of supporting SCs. | requirements.md FR-011/SC-005; plan.md § Inherited Blockers |
| C-01 `in-scope` obligations | FR-009 now requires three duties for every `in-scope` row: valid in-spec FR reference; a task citing that FR; a verification joint-acceptance row naming the RS. Missing/invalid FR is input error exit 2; missing task/joint acceptance is `runtime-dependency-not-owned: RS-NNN`. FR-012 absorbs these under the existing runtime-row class (no eighth reason). SC-005 measures all three; 081b carrier is `tests/contract/test_acceptance_premises.py`. | requirements.md FR-009/FR-012/SC-005; plan 081b row |
| E-01 orphan fixtures | T007 now asserts `smoke-mutation` → `status-claims-implemented-but-blocked` (exit 1) and `execution-without-final` → `zero-final-path-pass` (exit 1, `final_path.total=0`); the FR-007 coverage row says all seven fixtures are asserted, so neither is merely “delivered”. | tasks.md T007 + coverage table |

## MEDIUM (gate-affecting)

| Finding | Change |
|---|---|
| B-01 | Shared Strings now distinguish template form from instance form; membership = template match + argument grammar, not byte equality. C-09 and T007 updated. |
| E-02 | Missing test carriers named: `test_acceptance_premises.py` (081b), `test_line_state_blocked.py` (081d), `test_review_code_composition.py` (081c). |
| E-03 | `templates/plan-template.md` named in 081b; `templates/commands/checklist.md` named in 081c/081d. |
| F-01 | Line/slice cardinality fixed: closure runs at the **feature line** closure (one line spans 081a–081d); slice merges use the review gate. FR-017/GW-03 and plan D6 updated. |
| F-02 | `test_status_gate_owner.py` added to the R3 guard list and 081c/081d rows; `all required` wording and condition count 3→4 recorded. |
| F-04 | T022 + GATE-7 run the full suite at slice close with `--names-out` and id-level set difference; DoD-6 is assessable at 081a close. |
| F-05 | A6 items 1–8 are the obligation authority; `line-registry.py` + `test_line_state_blocked.py` are the runtime/test carriers; data-model E-9 and plan D6 are pointers. |
| F-08 | T024 adds `Blocked` to `skills/internal/manage-features/SKILL.md` before T020 writes the registry value; feature-index-template vocabulary remains 081d work. |
| H-02 | Pin validity defined: re-read `pytest --version` / `git --version` before each comparison; mismatch invalidates the comparison as input error exit 2, never new failures. |
| H-03 | Artifact-review denominator is the **expected** artifact set; missing expected artifacts are findings. `expected_artifacts` added to data-model E-10. |

## LOW

- F-06: T018 registers `tests/fixtures/` in `.specify/instructions.md` § Key Directories.
- F-07: `requirements.md` FR-003 recorded as a declaration-site exemption in SC-009 ④ with a reason.
- F-09: `checklists/requirements.md` Notes now carries a superseded-snapshot note.
- F-10: T003/T021 no longer use a backticked `data-model.md` path; `validate-tasks.py` reports 0 warnings.
- F-11: plan source-surface count and split recomputed to 43 (10/3/11/2/1/16).
- E-04: T023 freezes the coverage baseline and records the `account-clause-coverage.py` verdict; the FR lane’s citation-group form remains an open measurement, not papered over.

## Validation

- `validate-requirements.py` → `status: ok`, 0 errors / 0 warnings; scanned 270 lines, 34 definition rows, 17 shared strings.
- `validate-tasks.py` → PASS, 0 errors / 0 warnings.
- `validate-decision-tensions.py --spec` → 6/6 pass, 5 records, 0 errors.
- `pre-analyze-check.py --stage tasks` → `decision=pass`, errors=0, advisories=114 (all planned deliverables).
- `decomposition-check.py --mode tasks` → `proceed`, task_count=24 ≤40, fr_count=25.
- No full test suite re-run at this stage; the plan-stage baseline (39F/6970P/7S) remains the comparison baseline and T022 owns the slice-close head run.
