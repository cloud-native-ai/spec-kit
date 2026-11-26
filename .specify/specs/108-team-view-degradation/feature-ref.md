# Feature Reference — 108-team-view-degradation

## Binding

| Field | Value |
|-------|-------|
| Requirement key | `108-team-view-degradation` |
| Bound Feature | **027 — Team Management** |
| Binding basis | 027 owns the `/speckit.team` command surface (create / modify / run / view) and the team archive layer; 108 revises only the `view` read program, its skill wording and tests — the direct successor slice of `103-team-view` (feature binding precedent: 036 / 042 / 103). |
| Registry posture | Slice row `108` registered `Draft` at clarify; parent 027 stays `Ready for Review` (no status regression). The `Draft → Planned` advance is the driver's close-out duty for this line (stage brief: no feature-registry edit by the plan executor). |
| Feature detail | `.specify/features/027-team-management.md` |
| Predecessor spec | `.specify/specs/103-team-view/` (view program, six groups, skill) — consumed as the live predecessor; superseded only where the 108 contracts say so |

## Delivery surface (framework source → runtime mirror)

| # | Source path | Role | Mirror / copies |
|---|-------------|------|-----------------|
| 1 | `scripts/python/team-view.py` | the single reader: closed timestamp grammar, three-way file classifier, latest selection + normalization, degradation reasons, per-group presentation | `.specify/scripts/python/team-view.py` (sync-mirrors) |
| 2 | `skills/internal/view-team/SKILL.md` | error-navigation row 5 names both reasons + owner pointer; additive-presentation wording | `.specify/skills/internal/view-team/SKILL.md` (sync-mirrors) |
| 3 | `docs/reference/commands/team.md` | View Mode: recognition rules, degradation reasons / exit codes, repair pointers | none — `docs/` is development documentation, never shipped |
| 4 | `tests/unit/test_team_view_report_recognition.py` | NEW unit pinning: grammar, classifier, latest, residue bound, uncertainty predicate | none |
| 5 | `tests/contract/test_team_view_degradation_contract.py` | NEW contract pinning: reason set, exit map, envelope keys, single entry, label closure, three-surface consistency | none |
| 6 | `tests/integration/test_team_view_degradation.py` | NEW integration pinning: production replica, corpus replica, residue-only, degraded definition, healthy fidelity, overview, snapshot | none |
| 7 | `.specify/specs/108-team-view-degradation/contracts/` | the feature's live contract face (program / recognition / presentation / labels) | none (spec artifact) |

Not touched: `templates/commands/team.md` (no per-tool command copy changes), `skills/internal/create-team/**` (report-naming owner unchanged), `scripts/python/goal-utils.py` (zero modification), `.specify/teams/**` (read-only), `.specify/features.md` and `.specify/features/027-team-management.md` (driver duty).

## FR → surface map

| FR | Delivering surface |
|----|--------------------|
| FR-001, FR-002, FR-003, FR-004, FR-005, FR-006 | program (classifier / latest / normalization / residue / uncertainty) + `report-recognition` contract + unit & integration tests |
| FR-007, FR-008, FR-009, FR-010 | program (ledger / spine / unreadable latest / four-state) + `presentation` contract + integration tests |
| FR-011, FR-012, FR-013, FR-014 | program (binding / goal states) + `presentation` contract + integration tests |
| FR-015, FR-016 | program (matrix anomaly / roster) + `presentation` + `view-labels` + integration |
| FR-017, FR-018 | program + `team-view-program` contract + contract & integration tests |
| FR-019 | `presentation` contract + source scan + degraded fixture |
| FR-020 | program declaration + skill row 5 + docs View Mode + contract test |
| FR-021, FR-006 (single entry) | program source scan + contract test |
| FR-022 | healthy-fidelity integration test (machine diff) + program contract C-107 |
| FR-023 | program contract C-108 + corpus-replica coverage (28 + 13) |
| FR-024 | `view-labels` contract (single live owner) + closure test |
| FR-025 | byte-fidelity + degraded six-group assertion + skill re-emission wording |

## SC → evidence map

| SC | Evidence |
|----|----------|
| SC-001 | `test_production_replica_latest_is_the_parsed_maximum` (+ `::test_auxiliary_artifact_never_becomes_latest`) |
| SC-002 | `test_corpus_style_reports_are_recognized` (13/13; state ≠ 为空/缺失; exit 0) |
| SC-003 | `test_degraded_definition_names_every_state` (six states, 9/9 members, repair pointer, zero fabricated values) |
| SC-004 | `test_healthy_fixture_is_byte_identical_to_the_baseline_program` |
| SC-005 | contract tests (`reason set`, `exit mapping two-of-two`, `--help`/`--version` zero writes) |
| SC-006 | `test_overview_matches_single_view_and_discloses_uncertainty` + `test_single_recognition_entry_source_scan` |
| SC-007 | `test_view_degradation_leaves_tree_byte_identical` (three scenario families) |
| SC-008 | the targeted-set run record through `scripts/bash/run-tests.sh` |

## Supersession and dated records

- `108/contracts/team-view-program.contract.md` supersedes `103/contracts/team-view-program.contract.md` on the exit-5 trigger surface, the state-vocabulary owner, report ordering/bounds and the normalized latest value; the 103 file is untouched.
- `108/contracts/view-labels.contract.md` supersedes `.specify/specs/103-team-view/data-model.md` § Rendering Line Types as the live label owner; the 103 data model is untouched and becomes a dated record.
- No report-naming or `team.md` schema change: `skills/internal/create-team/SKILL.md` § Report contract and `references/create-mode.md` keep their text.

## Handoff to `/speckit.tasks`

- Tests Mode: ON (execution class, Principle IV); tests precede the engine edit; reverse samples for the closed sets.
- The three new test files carry the FR/SC coverage above; the existing four team-view test files form the regression surface and are expected to pass unmodified.
- Re-measure list: `research.md` § Re-measure list (corpus counts, baseline git object, mirror baselines, `SPECKIT_PYTHON`, the 103 test surface, engine messages).
- Wrap-up duties for the implement stage: targeted set through the runner with `--names-out`, name-level new-failure diff against the implement-entry baseline, no full suite.

## Overlap Adjudication (driver record, plan U4, 2026-11-26)

- Trigger: post-plan `overlap-check.py` → `decision=overlap`, `checked_specs=90`, `overlaps=72`; clarify-time run was vacuous (no declaration artifact).
- Reading: relations are historical path declarations (top: `templates/commands/team.md`, `scripts/python/team-view.py`, `scripts/python/goal-utils.py`, `skills/internal/create-team/SKILL.md`, `skills/internal/view-team/SKILL.md`, docs). No concurrent writer: the only active line is 108; 101 is a stale registry entry.
- Ruling: **108 is the sole current writer** for the view-recognition/degradation changes; 103-team-view and 027 Team Management keep their delivered behavior and dated records; additions are pointer-only or in-place edits within the existing owner; no scope removed.
- Residual: `overlap=72, historical/non-concurrent`; the engine cannot clear without falsifying delivery surfaces; tasks MUST NOT start if a new concurrent writer activates.
- Evidence: `.specify/state/u4-team-view-degradation-plan.txt`.
