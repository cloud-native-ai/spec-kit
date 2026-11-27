# Verification Input — 110-context-management (crew-side input for `verification.md`)

**Purpose**: T039's assembly. This file is the implement package's evidence-backed input for
the success-criterion log; `verification.md` is **derived from it spec-side under the
implement command** (condition-set owner: `shared/workflow/acceptance-hardening.md` § Gates,
and the key=value vocabulary owner: `templates/verification-log-template.md`). Deriving
`verification.md` is **not this package's duty** — it is recorded here as an explicit hand-off.

Every status below is backed by a captured run in `test-evidence/` or `notes/`; commands were
executed through the single entries declared in the task file (engine CLI for readings,
`scripts/bash/run-tests.sh` for tests).

## Baseline (recorded at the implement-entry commit)

baseline_commit=2cbbb3c8a4d3751533a2d6ad067e3b02235ed53c
baseline_date=2026-11-27
baseline_branch=110-context-management
baseline_note=instrumented baseline: full-suite failing-name list captured at this commit (223 names, test-evidence/implement-baseline.log); no other baseline existed before this package

## Implementation result block

implementation_date=2026-11-27
post_change_commit_pending=true
post_change_note=the deriving implement step stamps the final package commit; this file is committed inside that package and cannot name it

## Success criteria (SC-001 … SC-011)

SC-001_status=pass
SC-001_value=repo check exit 0 / zero findings; four SC-001 fixtures each exact (1,1,1,2 findings at exit 1); reruns byte-identical
SC-001_note=command="python3 .specify/scripts/python/context-audit.py --action check [--workspace-root <fixture>]"; evidence=test-evidence/audit-fixtures.txt, test-evidence/determinism.txt

SC-002_status=pass
SC-002_value=per-action SHA-256 tree manifests identical before/after on the three fixture trees and the repository tree; added=[] removed=[] changed=[]
SC-002_note=command=run-tests.sh tests/contract/test_context_management_readonly.py::test_containment_claims_are_decidable; evidence=test-evidence/guard-convergence.txt, notes/quickstart-run.md (scenario 6)

SC-003_status=pass
SC-003_value=absence-mixed reads absent/empty/unreachable with reasons, no row omitted; all-present reads every row present
SC-003_note=command=run-tests.sh tests/contract/test_context_management_engine.py::test_manifest_reads_genuine_absences_with_reasons; evidence=test-evidence/guard-convergence.txt, test-evidence/us2-green.txt

SC-004_status=pass
SC-004_value=merged layer-form fixture yields exactly two layer-form-illegal findings and nothing else; repository layout zero violations
SC-004_note=command="python3 .specify/scripts/python/context-audit.py --action check --workspace-root tests/fixtures/context-management/violation-layer-form"; evidence=test-evidence/audit-fixtures.txt

SC-005_status=pass
SC-005_value=fresh init tree: check exit 0; manifest exit 0 with explicit absence lines; socket attempts 0; nothing transmitted
SC-005_note=command=run-tests.sh tests/integration/test_context_management_init.py::test_fresh_init_distributes_and_audits_offline; evidence=test-evidence/us3-green.txt, notes/quickstart-run.md (scenario 5)

SC-006_status=pass
SC-006_value=7/7 bounded-index cap references resolve by path+section; 0 numeric bound fields in the four facts; 0 numeric cap literals in the increments
SC-006_note=command=numeric-bound + cap-resolution scan (guard pattern CAP_UNIT_RE); evidence=test-evidence/cap-scan.txt

SC-007_status=pass
SC-007_value=every declared member of categories/layers/forms exercised (mutation produces observable difference); unknown or missing declaration member exits 2 with no partial verdict
SC-007_note=command=run-tests.sh tests/contract/test_context_management_declarations.py; evidence=test-evidence/guard-convergence.txt, test-evidence/us2-green.txt

SC-008_status=pass
SC-008_value=full suite 223 failed both at baseline and current (comm -13 = 0 new, comm -23 = 0 disappeared); mirrors byte-identical; three protected surfaces equal their pre-change captures
SC-008_note=command="bash scripts/bash/run-tests.sh --full --names-out …"; evidence=test-evidence/full-suite.txt, test-evidence/implement-baseline.log, test-evidence/full-suite.log

SC-009_status=pass
SC-009_value=ambient heading verbatim in template (40 sections) and live (41); generator budget within (40,533 B of 40,960 B); fresh-tree instructions carry the section in pointer shape
SC-009_note=command="bash scripts/bash/generate-instructions.sh"; evidence=test-evidence/us4-green.txt, test-evidence/mirror-final.txt, notes/quickstart-run.md

SC-010_status=pass
SC-010_value=repo project manifest lists project-vocabulary/concept-definitions/concept-explanations each present (7/7 project rows present); concept-missing fixture keeps the roster row set with not-evaluated + unreachable and the affected structure Unobserved, no agreement claim; protocol-boundary guard shows the item set unchanged
SC-010_note=command="python3 .specify/scripts/python/context-audit.py --action manifest --layer project"; evidence=test-evidence/concept-presence.txt, test-evidence/guard-convergence.txt

SC-011_status=pass
SC-011_value=landing contract declares exactly three legal cells and three forbidden pairs; layout header is the fixed six columns (no category column); every layout row lands in a legal cell; repository check clean
SC-011_note=command=run-tests.sh tests/contract/test_context_management_owner.py (landing/matrix legs); evidence=test-evidence/guard-convergence.txt, test-evidence/audit-fixtures.txt

## Smoke record (exactly one)

smoke_command=python3 .specify/scripts/python/context-audit.py --action check
smoke_exit_code=0
smoke_evidence_path=.specify/specs/110-context-management/test-evidence/audit-fixtures.txt

## Completion Gate re-validation (run at this package's final tree)

| Gate | Verdict | Reading |
|------|---------|---------|
| GATE-1 | pass | `validate-tasks.py` exit 0 — 0 error(s), 0 warning(s) (`test-evidence/tasks-validator.txt`) |
| GATE-2 | pass | `pre-analyze-check.py --stage tasks` → `decision=pass errors=0` (25 advisories, all previously adjudicated classes: external-clause label collisions and intentional absence paths) |
| GATE-3 | pass | FR 29/29 and SC 11/11 in the coverage map; 39 clauses claimed exactly once; validator reports zero green-* errors |
| GATE-4 | pending-derivation | `verification.md` is derived from this input by the implement command; the deriving step must re-run this gate against the derived file (HAND-OFF, below) |
| GATE-5 | pass | `sync-mirrors.py --check` rc 0; feature pairs `cmp`-identical (`test-evidence/mirror-final.txt`) |
| GATE-6 | pass | generator: 40,533 B / 40,960 B → `within`; heading verbatim in template, mirror and live (`test-evidence/mirror-final.txt`) |
| GATE-7 | pass | repo check exit 0 zero findings; four fixtures exact; reruns byte-identical (`test-evidence/audit-fixtures.txt`, `determinism.txt`) |
| GATE-8 | pass | `grep -cE '^- \[[ >]\]' tasks.md` → 0 after T039 closes |
| GATE-9 | pass | zero NEW failure names vs the entry baseline (`test-evidence/full-suite.txt`) |
| GATE-10 | pass | one red guard verdict per rule (nine) in `test-evidence/mutation-drill.txt`; engine `git diff` empty after the drill |

## Hand-offs (recorded, not performed here)

1. **`verification.md` derivation** — derive it from this file's key=value block under the
   implement command; re-run GATE-4 on the derived file. The `final`-path rows all read
   `pass` above and the smoke record is complete, so the derivation is mechanical.
2. **Feature 110 registration / status** — this line's constraint (requirements A-2; plan
   § Feature Integration; tasks.md header) makes `.specify/features.md`, the feature detail
   file and the registry status **read-only to this stage**. The registration set (index row,
   `.specify/features/110-context-management.md` detail from the template, the status advance)
   is the line close-out's Feature Integration Protocol recovery point; the absent row MUST
   NOT be read as "the feature does not exist" — the binding is Feature 110.
3. **DoD Status** — flipped to `green` in `tasks.md`: every DoD-N row is satisfied at this
   tree (evidence above), while the registry status advance awaits the hand-off in item 2.

## Deferred work

deferred_tasks=none (no task row is `[~]`; all 39 rows read `[X]`)