# Contract — Gate Wiring (where the new judgements attach)

**Status**: designed (this stage); implemented by `/speckit.implement`
**Owner of the criteria**: `shared/workflow/acceptance-hardening.md` + `templates/feature-details-template.md` § Canonical Status State Machine. This contract is the **wiring map**: which surface calls which judgement, and which regeneration entry must run afterwards.

## The three call sites of the closure verdict

- **GW-01**: `/speckit.implement` MUST run the closure checker before `Planned → Implemented`; on `block` it MUST land `Blocked` and MUST NOT write `Implemented`. The four conditions and their owner stay where they are; the command only calls.
- **GW-02**: `/speckit.review` MUST run the checker for its Acceptance Reality Check before judging `Implemented → Ready for Review`; on `block`, or on `F-ACCEPTANCE` with zero `final`-path pass, the transition MUST be refused with a named condition.
- **GW-03**: the `sdd-loop-driver`'s closure/merge step MUST run the checker before merging: `skills/external/sdd-loop-driver/scripts/integrate-lines.py` MUST default its quality gate to the checker (using the existing `--gate-cmd` hook, not a second code path), and on `block` it MUST record `integration-record --result failed --reason closure-blocked`, mark the line `blocked`, and MUST NOT leave the line `completed`.
- **GW-04**: no call site MAY substitute a model judgement, a different script, or an ad-hoc grep for the checker's verdict; a fourth implementation of the judgement is a defect.

## The four deterministic findings (no second gate system)

- **GW-05**: The four findings (`runtime-dependency-not-owned: RS-NNN`, `falsified-premise-undecided: EP-NNN`, `inherited-blocker-undisposed: <feature>:<row>`, and the runtime-row emptiness check that maps onto the first) MUST be implemented in the existing `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`; the literals are quoted verbatim from `requirements.md` § Shared Strings ([[STR-011]]…[[STR-013]]), never re-spelled here.
- **GW-06**: They MUST be surfaced through the existing gate rows in `shared/workflow/expression-gates.md` (`G-req-clarity` for the requirements stage, `G-plan-fact` for the plan stage) and MUST NOT create a new gate registry row, a new checker script or a parallel blocking path.
- **GW-07**: Each finding MUST carry the same `check` / `severity` / `path` / `line` / `message` shape the script already emits, and MUST be waivable through the existing `--waive CHECK:REL_PATH:LINE` form.

## Determinism and program-first duty

- **GW-08**: Every new gate MUST have a deterministic verdict produced by a program. A gate whose only judge is a model MUST NOT be introduced; where a judgement is inherently semantic (severity assignment, finding prose), the gate itself stays deterministic and the prose is a report, not a gate.
- **GW-09**: `templates/tasks-template.md` GATE-4 MUST be upgraded to require, for every `final`-path SC, a `pass` status **and** the presence of the smoke record (command / exit code / evidence path), or an explicit user waiver naming the SC.
- **GW-10**: The `tasks.md` § Environment Prerequisites boundary (A13) MUST be stated there by pointer to the owner, and this feature MUST NOT introduce a second environment-verdict landing point.

## Two Hats: source, mirror, per-tool copies

- **GW-11**: Every edit MUST land in the framework source (`templates/`, `shared/`, `skills/`, `scripts/`, `src/`, `tests/`); `.specify/` copies are generated and MUST NOT be hand-edited as the primary change.
- **GW-12**: After the source edits, `python3 scripts/python/regen-command-copies.py` MUST be run (then `--check` → exit 0) for the four per-tool command copy trees, and `python3 scripts/python/sync-mirrors.py` MUST be run (then `--check` → exit 0) for the six mirror pairs.
- **GW-13**: `src/` and `tests/` have no mirror; a `--check` failure on any pair this feature touches is a defect to fix by regeneration, never by editing the mirror.

## Documentation and registry surfaces

- **GW-14**: `CHANGELOG.md` MUST carry this feature; `docs/reference/commands/review.md` MUST describe four segments plus ARC; `.specify/instructions.md` § Key Directories MUST list `tests/fixtures/` so the new fixture directory is registered where directory governance requires it.
- **GW-15**: The feature registry and the bound feature detail MUST move `Draft → Planned` in this stage and MUST NOT reach `Implemented`; historical statuses and historical verification records MUST NOT be rewritten by this feature.

## Traceability

| FR | Clauses | Test |
|---|---|---|
| FR-005 | GW-09 | `tests/integration/test_acceptance_smoke.py`, `tests/contract/test_acceptance_state_machine.py` |
| FR-008 | GW-01, GW-02, GW-03, GW-04 | `tests/contract/test_gate_wiring_081.py` |
| FR-012 | GW-05, GW-06, GW-07 | `tests/contract/test_acceptance_premises.py` |
| FR-021 | GW-11, GW-12, GW-13 | the two `--check` runs recorded in `verification.md` |
| FR-023 | GW-09 (`smoke_command`/`exit`/`evidence`), `## Mirror Obligations` of `plan.md` | `tests/integration/test_acceptance_smoke.py` + `verification.md` baseline comparison |
| FR-024 | GW-11, GW-12, GW-13 | the two `--check` runs |
| FR-025 | GW-08, GW-14 | `tests/contract/test_acceptance_premises.py` |
| FR-022 | GW-14, GW-15 | `tests/contract/test_acceptance_schema_ownership.py` |
