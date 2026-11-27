# Implement Package P1 Stage Evidence — 2026-11-27

Line `decision-batch-panel`; run `r20261127T081500Z-112a`; stage `implement` package **P1** (tasks T001–T015); baseline `78a60309b`; branch `112-decision-batch-panel` (worktree `.specify/.tmp/sdd-loop/worktrees/decision-batch-panel`); HEAD at package start `e4692034e`.

## Scope executed

| Task | Result |
|------|--------|
| T001 | `tests/fixtures/decision-batch/` — 28 case directories, each with `.gitkeep`; runtime-evidence dir `.specify/specs/112-decision-batch-panel/notes/` created |
| T002 | `notes/pre-change-measurements.md` (M1–M14: 17 open register rows, 0 blocks, 30/0 gate scan, mirrors/copies rc 0, 32/60 baselines, probe 130 vs stale literal 122, 30 docs, owner inventory 9/12/9/7/9, 6 conditional fields / 15 admitted lines, 0 `decision-batch-` knowledge entries, 1,276 B section); verbatim gate capture refreshed in `test-evidence/scan-confirmation-gates-baseline.txt` |
| T003 | `notes/red-first-evidence.md` — one slot per planned red-first test (S1–S7), failing-name list referenced (`notes/red-first-names.txt`) |
| T004 | `coverage-baseline.txt` frozen (`--freeze`, 785 uncovered names over 344 files, header records command + date); live accounting run: `uncovered beyond baseline: 0`, `coverage-baseline-delta pass (0)`; FR-043 remains uncovered by contract citations (pre-existing design property — its carrier is the command doc, T053) |
| T005 | `tests/contract/test_decision_batch_contract.py::test_engine_interface_contract` authored red-first (C-608) — red run recorded |
| T006 | `scripts/python/decision-batch.py` skeleton — closed actions `scan`/`record`/`replay`, declared flags, `-h`/`--help`/`--version` on entry and every action, undeclared options refused (exit 2), unimplemented action exit 2 with a message, no writes; T005 green |
| T007 | Owner page: ownership declaration names the batch faces (ten faces), vocabulary 9 → 17 (eight bilingual terms), P-13 producer row; dependent pins moved in the same change (vocabulary/producer pins in `test_decision_governance_contracts.py`, inventory pin in `test_decision_governance_guards.py`) |
| T008 | `templates/commands/decide.md` thin entry (User Input Protocol, closed actions, delegation, exit semantics by pointer, no restated criteria) |
| T009 | `skills/internal/decide-batch/SKILL.md` (presentation relay, verbatim reply capture, engine delegation, boundaries, pointers; `## Wrap-up` compiled by T010) |
| T010 | Probe Object `skill-decide-batch-wrapup` (class `skill-wrapup`, unit `skill:decide-batch`) registered; `probe-utils.py --action compile-embeds` compiled 87 units (1 written); registry validates 11 classes / 131 internal + 0 external; `--reconcile` zero-gap; `--check` zero drift |
| T011 | `test_migration_distribution.py` 32 → 33 commands (`decide`) / 60 → 61 skills (`decide-batch`); `test_probe_nonentity_catalog.py` pin re-measured to **131** (not 122 + 1); dependent census pins moved with them (`test_flow_class_ledger.py` 92 → 94 rows / 33 + 61 inventory; `test_humanize_command_surface.py` WC-16 approved additions + 33; `test_migrate_distribution_assembly.py` 33) — FR-042 inventory closure |
| T012 | `regen-command-copies.py` regenerated the four per-tool copies (all contain the edit); `sync-mirrors.py --write` projected owner page/probe/flow-class/engine/skill; both `--check` modes rc 0; both engine copies answer `--help`/`--version` |
| T013 | `tests/unit/test_decision_batch_engine.py` — 21 US1 tests authored; nine US1 fixtures populated (`two-source`, `incomplete-block`, `autonomous`, `class-conflict`, `resolution-join`, `grounding-grounded`, `grounding-none`, `prior-conflict`) plus `absent-root`/`unreadable-register` needed by `test_source_presence_levels` |
| T014 | `tests/contract/test_decision_batch_contract.py` — `test_block_grammar_owner_extension` (C-103), `test_presentation_identifier_boundary` (C-204), `test_skill_does_not_recompute` (C-307) |
| T015 | Owner page § 待决策项来源清单（Pending Source Roster）: closed two-source table, four closed scan roots, candidacy≠qualification split, named exclusion families, register↔block linkage, byte-equal identity/dedupe, presence readings with the carrier/block boundary |

Task states closed in `tasks.md`: T001–T015 all `[X]` (15 rows).

## Gate readings (all executed this package)

| Check | Command | Result |
|-------|---------|--------|
| Engine interface contract | `run-tests.sh tests/contract/test_decision_batch_contract.py::test_engine_interface_contract -q` | red at T005 (`missing engine`, rc 1) → green at T006 (`1 passed`, rc 0) |
| US1 red-first | `run-tests.sh tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py -q --names-out …/red-first-names.txt` | **23 failed, 2 passed** (rc 1); all failures are behaviour assertions on the unimplemented scan / missing owner section; names in `notes/red-first-names.txt` |
| 107 governance suites | `run-tests.sh tests/contract/test_decision_governance_contracts.py tests/contract/test_decision_governance_guards.py -q` | **34 passed** (rc 0) — owner-page extension and its moved pins hold |
| Census/ledger suites | `run-tests.sh test_migration_distribution.py test_probe_nonentity_catalog.py test_flow_class_ledger.py test_migrate_distribution_assembly.py test_humanize_command_surface.py -q` | 140 passed; 5 failures are **pre-existing environment failures** (`FileNotFoundError: .specify/memory/features.md`; the file is untracked and absent in this worktree, and the tests touch no feature-112 file) — names captured below |
| Probe surface | `probe-utils.py --action probes --validate` / `--reconcile` / `compile-embeds --check` | 11 classes / **131** objects / 0 errors; zero-gap (88 embeds); zero drift |
| Flow-class ledger | `flow-class-check.py --action check --format json`; `--action lookup` for both new units | `units 94`, `findings []`; both resolve `flow_class: execution`, `basis: behavior-oracle` |
| Mirrors / copies | `sync-mirrors.py --check`; `regen-command-copies.py --check` | rc 0 both (`shared/ == .specify/shared/`, 123 files byte-identical); four copies contain the body edit |
| Gate neutrality | `scan-confirmation-gates.py --summary` | `30 blocking (22/7/1) / 0 violations` — unchanged vs the frozen baseline; zero hits in the new files |
| Workspace guard | `workspace-guard.py --snapshot` at start; `--check` at wrap-up | snapshot recorded; see `test-evidence/workspace-implement-p1-check.txt` |

Pre-existing failure names (baseline for later regression comparison): `test_c06_registry_rows_resolve`, `test_wc13_stage_class_pin_remeasured`, `test_wc07_skill_body_budget`, `test_wc10_feature_062_status_held`, `test_wc11_feature_row_name_description` (all in `tests/contract/test_humanize_command_surface.py`, all reading the untracked `.specify/memory/features.md`). Recorded in `test-evidence/implement-p1-baseline-failed.txt`.

## Red/green pointers

- Red-first evidence: `notes/red-first-evidence.md` (S1 R-608 red → green; S2 23 red; S7 slots pending for P4).
- Failing-name list owner: `notes/red-first-names.txt`.
- Green at package end: engine interface test; skill non-recompute guard; all moved pins; governance suites; probe/ledger/mirror checks.

## Boundaries held

- `.specify/register.md`, `.specify/instructions.md`, `.specify/.gitignore`, `.specify/glossary.md`, `.specify/features.md` and the driver state spine untouched; no edits to the main tree; no push.
- No new runtime store root; the batch record carrier (existing knowledge store) untouched by this package.
- Preserved boundaries: the A-26 read/write split is reflected in the US1 read-time-join test (prior-batch reads are the declared read-only via); the A-27 bounded append is not touched by P1 tests beyond the prior-conflict fixture design.
- Zero network access; zero feedback-store transmission.

## Concurrency

`requested=1`; `effective=1`; `effective_reason=write-conflict` — the shared write surfaces (owner page, engine, skill, probe registry, flow-class ledger) are single-writer; the package is one serial unit.

## Disclosures (corrections applied in passing)

1. **Interpreter resolution**: the worktree had no pytest interpreter on the bare ladder rungs; resolved through the runner's first rung `SPECKIT_PYTHON=/usr/local/bin/python3` (pytest 8.4.2). All test runs use the single entry.
2. **Dependent pins beyond T011's two files**: the flow-class ledger owner page and three further census pins (`test_flow_class_ledger.py`, `test_humanize_command_surface.py`, `test_migrate_distribution_assembly.py`) had to move with the new command/skill or they would have gone red — FR-042's "frozen baselines move in the same change" is the recorded intent. The ledger rows for `/speckit.decide` and `skill:decide-batch` were added to `shared/definitions/flow-class-definitions.md`.
3. **Extra fixtures**: `absent-root` and `unreadable-register` were populated in T013 (T013's test list includes `test_source_presence_levels`, whose fixtures the row's fixture enumeration omitted; the same fixtures serve US4's T040).
4. **Probe HandlerBinding**: no new binding row was added for `skill-decide-batch-wrapup` — the existing `@point:wrap-up | all` subscriptions cover the unit (precedent: Feature 103's `skill:view-team` row), and the compiled Wrap-up carries the six standard steps. The object row is registered.
5. **`test_skill_does_not_recompute` (C-307) is green at authoring** because its subject (T009) precedes T014 in this package; disclosed, not claimed as red-first.

## Re-anchoring

Rules reloaded at each core step (unattended, no approval request, U4 → next, spine before action, workspace guard, fast-fail, budget/report discipline); territory held to this feature's artifacts; verdict `on-track`.

## Anomalies

- `ANOMALY:` none beyond the five disclosures above; no decision-class anomaly was met (the HandlerBinding reading follows precedent and is disclosed). The 5 humanize failures are pre-existing environment failures, recorded as the regression baseline rather than repaired (out of this feature's territory).