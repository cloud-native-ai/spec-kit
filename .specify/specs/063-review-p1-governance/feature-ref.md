# Feature Reference: 063 Review P1 Governance（评审 P1 治理）

**Spec**: `.specify/specs/063-review-p1-governance/requirements.md` | **Plan**: `.specify/specs/063-review-p1-governance/plan.md`
**Source findings**: `.specify/specs/062-humanize-command/review.md` § 3 (F1–F8; evidence only, never edited — FR-029)

## FR → contract clause map

| FR | Finding | Contract clause(s) | Primary artifact |
|----|---------|--------------------|------------------|
| FR-001 | F1 | C-1 | shared/definitions/contract-clause-definitions.md § 4 rule 2 |
| FR-002 | F1 | C-2 | scripts/python/clause_extract.py; tests/contract/test_clause_forms.py |
| FR-003 | F1 | C-5, C-7 | skills/internal/analyze-artifacts/SKILL.md; templates/commands/analyze.md |
| FR-004 | F1 | C-6, C-7 | skills/internal/create-tasks/SKILL.md |
| FR-005 | F2 | C-3, C-4 | skills/internal/analyze-artifacts/SKILL.md; templates/commands/analyze.md |
| FR-006 | F2 | C-8 | skills/internal/create-checklist/SKILL.md |
| FR-007 | F2 | C-9 | skills/internal/implement-feature/SKILL.md § Step 2 |
| FR-008 | F2 | C-10 | skills/internal/implement-feature/SKILL.md § Step 2 |
| FR-009 | F3 | C-11 | templates/commands/review.md § Handoffs |
| FR-010 | F3 | C-12 | templates/instructions-template.md § ID Register |
| FR-011 | F3 | C-13 | shared/workflow/feedback-step.md § Scope guard |
| FR-012 | F3 | C-14 | templates/review-template.md § 5 + Replacement Rule 3 |
| FR-013 | F3/E2 | C-15 | shared/workflow/feature-integration.md |
| FR-014 | F4 | C-20, C-21, C-22 | scripts/python/probe-utils.py; probe-definitions.md |
| FR-015 | F4 | C-23 | run-determination.py; feedback-utils.py |
| FR-016 | F4 | C-25 | all compiled units; .specify/memory/feedback/backlog.md |
| FR-017 | F4/E1 | C-24 | run-determination.py (unchanged idempotency, pinned) |
| FR-018 | F5 | C-16, C-17 | create-tasks SKILL § item 2; templates/tasks-template.md |
| FR-019 | F6 | C-26 | templates/verification-log-template.md |
| FR-020 | F6 | C-27, C-28 | shared/definitions/probe-definitions.md; implement SKILL § Step 9 |
| FR-021 | F6 | C-28 | verification log semantics |
| FR-022 | F7 | C-29 | skills/internal/implement-feature/SKILL.md (new pre-flight) |
| FR-023 | F7 | C-30 | templates/commands/implement.md |
| FR-024 | F7 | C-19 | create-tasks SKILL § Re-freeze timing |
| FR-025 | F8 | C-18 | create-tasks SKILL § Runtime-evidence landing points (owner-file correction, see C-18 note) |
| FR-026 | cross | C-31 | mirror/sync obligations (plan § Mirror Obligations) |
| FR-027 | cross | C-32 | per-mechanism contract tests + mutation drills (tasks) |
| FR-028 | cross | C-33 | no new deps/network/daemons (S10) |
| FR-029 | cross | C-34 | 062 artifacts untouched (S10) |
| FR-030 | cross | C-7, C-22, C-29 | derived sets: engine parser / directory / accountant default |

## SC → verification map

| SC | Verified by | Measurement source |
|----|-------------|--------------------|
| SC-001 | quickstart S1 + tests/contract/test_clause_forms.py + test_clause_coverage.py | dual-width fixture; owner-text assertion |
| SC-002 | S2 | accountant run on fixture; `find` baseline census; wired-caller grep |
| SC-003 | S3 | seed checklist + analyze gate report |
| SC-004 | S4 | recheck file; waiver text audit; original-file git diff empty |
| SC-005 | S5 | register.md rows + same-commit check; clean-clone resolution; entry grep |
| SC-006 | S5 | transition-table contract test; one-row-per-command invariant |
| SC-007 | S6 | isolated verbatim face execution; `--check` zero drift; backlog row |
| SC-008 | S6 | one-error listing fixture; duplicate/idempotency fixture |
| SC-009 | S7 | seed tasks row + carrier-rule check |
| SC-010 | S8 | evidence-binding gate on 3 mutation fixtures |
| SC-011 | S9 | drift fixture; classification output; write-back diff |
| SC-012 | S10 + C-18 rule | seed red-first note; renumbered-gate fixture |
| SC-013 | S10 | `comm -13` vs frozen 63-name baseline; `sync-mirrors.py --check`; dep/deps diff (clause pins: C-31/C-32/C-33) |
| SC-014 | S10 | `git diff -- .specify/specs/062-humanize-command/` empty; sync `--check`; owner-reference audit (clause pins: C-31/C-34) |

## Shared strings consumed

| ID | Value | Where |
|----|-------|-------|
| [[STR-001]] | `gate-implement-evidence-binding` | C-27; probe-definitions row |
| [[STR-002]] | `coverage-baseline.txt` | C-6/C-7/C-29; create-tasks freeze duty |
| [[STR-003]] | `REC-` | C-11/C-12; review handoff + ID Register |

## Deliverable surface (framework sources this feature edits)

1. shared/definitions/contract-clause-definitions.md (C-1)
2. scripts/python/clause_extract.py (C-2)
3. tests/contract/test_clause_forms.py, test_clause_coverage.py (C-2, S1/S2 pins)
4. skills/internal/analyze-artifacts/SKILL.md (C-3, C-4, C-5)
5. templates/commands/analyze.md (C-3, C-5)
6. skills/internal/create-tasks/SKILL.md (C-6, C-16, C-18, C-19)
7. templates/tasks-template.md (C-17)
8. skills/internal/create-checklist/SKILL.md (C-8)
9. skills/internal/implement-feature/SKILL.md (C-9, C-10, C-27, C-29)
10. templates/commands/review.md (C-11)
11. templates/instructions-template.md (C-12) + generated .specify/instructions.md
12. shared/workflow/feedback-step.md (C-13)
13. templates/review-template.md (C-14)
14. shared/workflow/feature-integration.md (C-15)
15. scripts/python/probe-utils.py (C-20, C-21, C-22, C-25)
16. shared/definitions/probe-definitions.md (C-20, C-22, C-27)
17. scripts/python/run-determination.py (C-22, C-23, C-24)
18. scripts/python/feedback-utils.py (C-22, C-23, C-24)
19. scripts/python/exec-quant.py (C-22 manifest only)
20. templates/verification-log-template.md (C-26)
21. templates/commands/implement.md (C-30)
22. tests/contract/* (per-mechanism pins: engine face, transition table, waiver format, recheck form, carrier list, evidence gate, baseline pre-flight)
23. .specify/memory/feedback/backlog.md (C-25 status flip)

## Baseline records (frozen before any change, 2026-10-19)

| Baseline | Path / command | Result |
|----------|----------------|--------|
| Failed tests (name-level) | `.specify/specs/063-review-p1-governance/notes/baseline-failed-tests.txt` via `bash scripts/bash/run-tests.sh --names-out …` | 63 failed / 3954 passed; 63 sorted names |
| Clause-coverage lane | `account-clause-coverage.py --spec .specify/specs/062-humanize-command` | `status: baseline-missing`, 512 errors (dark lane live) |
| Coverage-baseline census | `find .specify/specs -name coverage-baseline.txt` | exactly one (053) |
| Compile-embeds check | `probe-utils.py --action compile-embeds --check` | 74 units, zero drift |
