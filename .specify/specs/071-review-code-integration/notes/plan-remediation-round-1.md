# Plan-side remediation round 1 (071) — what was edited, what the programs said, what stays unclaimed

**Date**: 2026-10-27 | **Stage**: plan (remediation round 1 of max 1) | **Trigger**: `test-evidence/analyze-report.md` → `GATE: CRITICAL=0 HIGH=6`
**Authority for the edit**: the driver's explicit authorization of a substantive revision to plan-owned artifacts in this round, on top of the requirement-layer adjudications landed in `14a1c6ec`.
**Worklist executed**: `notes/remediation-round-1.md` (every plan-owned row, plus the rows the requirements-layer adjudications imply).

## 1. Deterministic checks, run after the edits

```text
$ python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
    --spec-dir .specify/specs/071-review-code-integration --stage plan --repo .
pre-analyze-check: stage=plan decision=pass errors=0 advisories=43 waived=0
summary: fr=28 sc=7 tasks=36 clauses=0 files=15          (exit 0)

$ python3 .specify/scripts/python/clause_extract.py .specify/specs/071-review-code-integration/contracts/*.md
code-review-skill.md         14   command-orchestration.md  16   coverage-receipt.md  15
feedback-and-boundaries.md   10   status-gate-ownership.md  10   tests-and-docs-sync.md 9
total_clauses = 74 ; every clause block has a non-empty citation group ; distinct FR cited = 28

$ python3 .specify/scripts/python/account-clause-coverage.py \
    --spec-dir .specify/specs/071-review-code-integration
FR universe: 28   FR claimed: 28   FR uncovered: 0
companion: claimed clauses 73, scanned files 197, clause universe 1109, FR universe 28
  [clause-uncovered] fail (496) — 496 uncovered, 1 beyond the frozen baseline
  [fr-uncovered] pass (0) — 28 of 28 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms
  [coverage-baseline-delta] fail (1) — baseline holds 495 names
status: uncovered (exit 1)
UNCOVERED / BEYOND-BASELINE: 071-review-code-integration/contracts/coverage-receipt.md#C-74
```

Files: `test-evidence/plan-remediation-pre-analyze.{json,stdout,stderr}`, `test-evidence/plan-remediation-clause-extraction.txt`, `test-evidence/plan-remediation-clause-coverage.txt`. All three were re-run verbatim when the round was committed (same commands, same repository state, nothing edited between the two runs) and produced byte-identical verdicts: `decision=pass errors=0 advisories=43` (`fr=28 sc=7 tasks=36 clauses=0 files=15`), `total_clauses = 74` across the 16+14+15+10+10+9 split, and `FR claimed 28 / FR uncovered 0` with `C-74` the single name beyond the frozen baseline.

**How to read the two non-green numbers, so a later stage does not mistake them for defects:**

- **`advisories=43` (was 42) is expected.** Every advisory is the same `missing-path` check against a deliverable this plan designs and has not built — the six contract test files and `tests/fixtures/review_git_repo.py`. The one added advisory is the new no-TTY quickstart case citing `tests/contract/test_code_review_skill_contract.py`, a path that already appears in the same list. `clauses=0` remains a property of the checker's legacy two-to-four-letter prefix pattern, not of the contract set; the clause lane is accounted by the two extractors above.
- **The clause lane's one red item is the price of the ID discipline.** C-74 was **appended** rather than inserted so that every clause id already cited by a `tasks.md` row still resolves. No `tasks.md` row claims an id that did not exist when the rows were written, and this stage does not edit `tasks.md`; therefore C-74 shows as the single name beyond the frozen baseline. The FR lane — the one this gate owns — is 28/28.

## 2. Pending claim (handed to `/speckit.tasks`)

| Clause | File | Obligation | Disposition |
|--------|------|------------|-------------|
| C-74 | `contracts/coverage-receipt.md` | the receipt block is the single source of the four counts; both disclosures copy it; a contract test asserts the three agree | **unclaimed** — needs one `[green: contracts/coverage-receipt.md#C-74]` tag on a receipt-task row (the natural home is the row that already claims C-31…C-44) |

Nothing else is unclaimed: `claimed clauses 73` matches the 73 pre-existing clauses one-for-one.

## 3. Constitution re-check (16 principles, `constitution.md` v1.13.0)

Same-author condition as before: this execution environment exposes no subagent dispatch, so every row is a direct read and says so.

| # | Principle | Verdict | What the remediation did to it |
|---|-----------|---------|--------------------------------|
| I | SDD as Foundation | Pass | every amended clause keeps its FR citation group; the FR lane is 28/28 after the edit |
| II | Feature-Centric Development | Pass | no second Feature row; the round records itself in the existing row/detail |
| III | Intent-Driven Development | Pass | each change traces to a finding id in the contract amendment logs; no alternative was re-litigated silently |
| IV | Test-First & Contract-Driven | Pass | the round adds obligations to tests it does not run (docs-only); the six-group plan is unchanged and C-66 now demands a recorded failing run per group |
| V | AI Agent Integration Standards | Pass | no provider, config key, roster or per-tool copy touched |
| VI | Continuous Quality & Observability | Pass | the receipt's exit alphabet is now closed (`0/1/2`, one meaning each) instead of "non-zero" |
| VII | Spec-Plan-Task-Implementation Workflow | Pass | status stays `Planned`; `tasks.md` untouched; the pending claim is routed to the tasks stage rather than absorbed here |
| VIII | Code as the Single Source of Truth | Pass | the code-path predicate and the archive naming cite the live script behaviour, including the measured difference between `%Y%m%d-%H%M%S` and the required `YYYYMMDDTHHMMSSZ` |
| IX | Framework Scope Discipline | Pass | specification documents only; no engine, dependency, command, skill, agent, template, test or task row added |
| X | Documentation Naming & Location Conventions | Pass | no new file name invented beyond the stage-notes convention already in use |
| XI | Dogfooding | Pass | the round is disclosed in the plan's change log, the contract amendment logs, the feature registry and the quickstart, not absorbed silently |
| XII | Tool Reuse Over Ad-Hoc Generation | Pass | no new script; every capability lands on the existing `git-delta-review.sh` entity |
| XIII | Better-Harness Orientation | Pass | the changes make the gate and the receipt checkable rather than adding a scoring layer |
| XIV | One Source of Truth | Pass | counts → one block + equality assertion; code-path predicate → one owner; skip reasons and forbidden phrases → cited from `requirements.md`, not copied into contracts; head's missing source tier is declared out of scope explicitly instead of left ambiguous |
| XV | User-Facing Comprehension | Pass | quickstart scenarios state execution status and premises per block; new literals are referenced by id, so a reader is not asked to match two spellings |
| XVI | Fast Fail | Pass | the round is itself the repair of surfaced findings; the one place where intent had to be chosen rather than derived (head carries no source tier) is recorded as a decision with its reason in `data-model.md` V31 and `research.md` § R2 |

No ❌ and no ⚠ row, so no Complexity Tracking entry is required.

## 4. What this round deliberately did not do

- No edit to `tasks.md` (the pending claim is listed above rather than pre-claimed here).
- No edit to any framework source, template, skill, script or test — so the mirror table in `plan.md` § Mirror Obligations and its measured baselines stay valid and were not re-measured.
- No re-opening of the driver's six adjudications; they are encoded as the only mechanical reading in `requirements.md` and cited here.
- No fifth Shared String for the skip-reason set or the forbidden-phrase list: both are multi-value sets owned by a single requirement row (FR-014, SC-003), and the contracts cite that owner instead of keeping a second copy.
