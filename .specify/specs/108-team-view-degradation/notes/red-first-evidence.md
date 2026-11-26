# Red-first evidence — 108-team-view-degradation (T004 skeleton)

One slot per planned red-first test. Each slot records, when the test is authored and run
**before** its subject lands: the command (the single entry `scripts/bash/run-tests.sh` with the
test file), the real output (the failing reading, trimmed to the discriminating lines; the raw
untrimmed capture lands in the slot's evidence file under `test-evidence/`), and the exit status.
A slot is complete only with all three; prefilled fields below are the skeleton.

- **Runner**: every execution goes through the single entry `scripts/bash/run-tests.sh`
  (interpreter pinned per tasks.md § Environment Prerequisites: `SPECKIT_PYTHON=/usr/local/bin/python3`).
- **Failing-name baseline**: the capture/comparison form (path and flag) is owned by
  `/speckit.implement` § Test runs; this note references that owner and never restates its path
  or flag. The implement-entry full-suite baseline is recorded once in
  `test-evidence/implement-baseline.log` + `baseline-failed.txt` and the spine's test-budget fence.
- **Red-first order**: T006/T007 (US1) → T013/T014 (US2) → T019 (US3 contract). T020's two
  guards are regression guards (green after implementation) and appear here only as a note,
  not as red slots.

## US1 unit — `tests/unit/test_team_view_report_recognition.py` (authored T006)

### Slot U-GRAMMAR — five accepted stamp forms, rejected samples

- **Planned node ids**: `test_stamp_grammar_accepts_exactly_the_five_forms`
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_team_view_report_recognition.py -q` (2026-11-26; whole-file run, red before T008)
- **Real output**: `E AttributeError: module 'team_view_program_recognition' has no attribute 'parse_stamp'`; summary `1 failed` for this node among `6 failed in 6.60s` (subject absent at red time)
- **Exit status**: 1
- **Evidence file**: `test-evidence/us1-red-unit.txt`
- **Subject matcher**: FR-001 closed five-form set; rejects date-only prefix, month 13, Feb 30, hour 24, non-Z zone, stamp not at name start.

### Slot U-CLASSIFIER — fixed three-way order

- **Planned node ids**: `test_classification_order_is_fixed` (incl. `-<4hex>-report.md` / `-<4hex>-stage.md`)
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_team_view_report_recognition.py -q` (2026-11-26; whole-file run, red before T008)
- **Real output**: `E AttributeError: module 'team_view_program_recognition' has no attribute 'classify_run_file'`; summary `1 failed` for this node among `6 failed in 6.60s`
- **Exit status**: 1
- **Evidence file**: `test-evidence/us1-red-unit.txt`
- **Subject matcher**: FR-003 order — residue / report / auxiliary by filename only.

### Slot U-LATEST — maximum parsed timestamp + name tie-break, single normalized token

- **Planned node ids**: `test_latest_is_maximum_parsed_timestamp_with_name_tiebreak`, `test_normalized_token_is_the_single_value`
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_team_view_report_recognition.py -q` (2026-11-26; whole-file run, red before T008)
- **Real output**: both nodes `E AttributeError: module 'team_view_program_recognition' has no attribute 'classify_runs'`; summary `2 failed` among `6 failed in 6.60s`
- **Exit status**: 1
- **Evidence file**: `test-evidence/us1-red-unit.txt`
- **Subject matcher**: FR-002 / FR-006 — latest = max parsed timestamp, name-ascending ties; one normalized `YYYYMMDDThhmmssZ` token.

### Slot U-RESIDUE — bounded residue line

- **Planned node ids**: `test_residue_presentation_is_bounded`
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_team_view_report_recognition.py -q` (2026-11-26; whole-file run, red before T008)
- **Real output**: `E AttributeError: module 'team_view_program_recognition' has no attribute 'classify_runs'`; summary `1 failed` among `6 failed in 6.60s`
- **Exit status**: 1
- **Evidence file**: `test-evidence/us1-red-unit.txt`
- **Subject matcher**: FR-004 — total count, at most 3 examples, omitted count.

### Slot U-UNCERTAINTY — uncertainty predicate

- **Planned node ids**: `test_uncertainty_predicate_needs_readable_runs_and_residue`
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_team_view_report_recognition.py -q` (2026-11-26; whole-file run, red before T008)
- **Real output**: `E AttributeError: module 'team_view_program_recognition' has no attribute 'classify_runs'`; summary `1 failed` among `6 failed in 6.60s`
- **Exit status**: 1
- **Evidence file**: `test-evidence/us1-red-unit.txt`
- **Subject matcher**: FR-005 — readable `runs/` plus residue count ≥ 1 only.

## US1 integration — `tests/integration/test_team_view_degradation.py` (authored T007)

### Slot I-PRODUCTION-REPLICA

- **Planned node ids**: production-replica test (old compact report, newer `20261125T121924Z-93cc-stage.md`, newer ISO-dashed report, same-stamp `-seat-result.md`, two date-only residue names)
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q` (2026-11-26; whole-file run, red before T008)
- **Real output**: `test_production_replica_latest_is_the_parsed_maximum` → `AssertionError: Team View: Fixture Team prod-replica（prod-replica）` (the latest group names no report because the narrow template hides the ISO-dashed name; residue line is the unbounded old form); summary `6 failed in 6.31s`
- **Exit status**: 1
- **Evidence file**: `test-evidence/us1-red-integration.txt`
- **Subject matcher**: latest = parsed maximum, 5/5 classification, bounded residue line, exit 5.

### Slot I-CORPUS-REPLICA

- **Planned node ids**: corpus-replica test (5 × `YYYY-MM-DDThh-mm-ssZ-report.md`, 7 × `YYYY-MM-DDThhmmssZ-report.md`, 1 × `YYYYMMDDThhmmZ-report.md`)
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q` (2026-11-26; whole-file run, red before T008)
- **Real output**: `test_corpus_style_reports_are_recognized` → `E AssertionError: assert '运行报告: 已列出（共 13 份' in 'Team View: Fixture Team corpus-replica…'` (the narrow template reads all 13 as `未识别`/`为空`); summary `6 failed in 6.31s`
- **Exit status**: 1
- **Evidence file**: `test-evidence/us1-red-integration.txt`
- **Subject matcher**: 13/13 recognition, state neither `为空` nor `缺失`, exit 0.

### Slot I-RESIDUE-ONLY

- **Planned node ids**: residue-only state test
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q` (2026-11-26; whole-file run, red before T008)
- **Real output**: `test_residue_only_runs_state_is_not_empty_or_missing` → `AssertionError: Team View: Fixture Team residue-only（residue-only）` (the old reader renders `运行报告: 为空` at exit 0); summary `6 failed in 6.31s`
- **Exit status**: 1
- **Evidence file**: `test-evidence/us1-red-integration.txt`
- **Subject matcher**: `未识别（unrecognized）—— 仅残留，最新不可确定`.

### Slot I-AUX-SAMESTAMP

- **Planned node ids**: auxiliary-never-latest + same-stamp tie-break tests
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q` (2026-11-26; whole-file run, red before T008)
- **Real output**: `test_auxiliary_artifact_never_becomes_latest` → `E AssertionError: assert '辅助产物（auxiliary）: 共 2 份' in …`; `test_same_stamp_tie_break_is_name_ascending` → `E AssertionError: assert '最近报告（latest_report）: 20260101T000000Z-93cc-report.md' in …`; summary `2 failed` among `6 failed in 6.31s`
- **Exit status**: 1
- **Evidence file**: `test-evidence/us1-red-integration.txt`
- **Subject matcher**: FR-003 auxiliary never latest; same-stamp name-ascending tie-break.

### Slot I-OVERVIEW-REUSE

- **Planned node ids**: overview-vs-single token equality with inline `（report-recognition-uncertain：残留 N）` marker
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q` (2026-11-26; whole-file run, red before T008)
- **Real output**: `test_overview_matches_single_view_and_discloses_uncertainty` → `E AssertionError: assert '20260103T083000Z（report-recognition-uncertain：残留 1）' in 'Team Overview: 2 teams …'` (the residue row's cell is `未记录` today); summary `6 failed in 6.31s`
- **Exit status**: 1
- **Evidence file**: `test-evidence/us1-red-integration.txt`
- **Subject matcher**: FR-006 — same normalized token in overview and single view; marker at exit 0.

## US2 integration — same file, appended (authored T013/T014)

### Slot I-DEGRADED-DEFINITION (T013)

- **Planned node ids**: production-shape degraded fixture (no `binding` block, partial-keys variant, inline `goal` with `anchor_slug`, matrix without `agent` column, missing `items.jsonl`, `pattern: iteration` with three missing spine files, nine frontmatter members)
- **Node ids (authored)**: `test_degraded_definition_names_every_state`, `test_binding_unreadable_carries_engine_reason_and_repair_pointers`, `test_partial_binding_keys_name_the_missing_keys`, `test_inline_goal_is_a_named_state_with_repair_pointers`, `test_slug_form_goal_under_readable_binding_adds_no_state_line`, `test_matrix_without_agent_column_is_malformed_and_roster_not_comparable`, `test_missing_ledger_carries_its_consequences`, `test_spine_applicability_follows_declared_pattern`
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "degraded_definition or binding_unreadable or partial_binding or inline_goal or slug_form_goal or matrix_without or missing_ledger or spine_applicability"` (2026-11-26; subject classes absent at red time)
- **Real output**: `7 failed, 1 passed in 6.33s`; discriminating lines — `AssertionError: assert 'goal 需归一为 anchor_slug' in …` (goal named state absent), `assert None is not None` on `- 绑定修复（binding repair）:` (repair pointer line absent), `assert '正文矩阵: 形态异常（缺列: agent）' in …` (matrix state absent), `assert '按声明 pattern 不适用' in '- constraints.md 缺失（…）'` (spine annotation absent), `assert '后果：无台账聚合计数、无非终态信号' in '- 台账: 缺失（…）'` (ledger consequences absent). The one pass is `test_slug_form_goal_under_readable_binding_adds_no_state_line`, which pins the unchanged healthy half of C-302 (slug-form `goal` under a readable binding adds no line) — a guard, not a red slot.
- **Exit status**: 1
- **Evidence file**: `test-evidence/us2-red-degraded.txt`
- **Subject matcher**: binding `不可读` + verbatim engine reason + `/speckit.team modify` & `goal-utils.py bind` pointers; `goal 需归一为 anchor_slug`; matrix `形态异常（缺列: agent）`; `roster_delta` 不可比对; ledger `缺失` with consequences; spine `按声明 pattern 不适用` + `operating-loops.md` § 8 pointer; 9/9 members; exit 5; ≥ 1 modify pointer; zero fabricated values.

### Slot I-UNREADABLE-LATEST (T014)

- **Planned node ids**: unreadable latest report (mode 000)
- **Node ids (authored)**: `test_unreadable_latest_report_is_named_not_unrecorded` (also `test_four_state_discipline_on_new_surfaces` carries the 不可读 member)
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "unreadable_latest or four_state or undeclared_pattern"` (2026-11-26; red before T015–T017)
- **Real output**: `AssertionError: assert '不可读' in '- 最近报告（latest_report）: 20260101T000000Z-report.md'` — the amended lines are absent and the group still renders as if the report were readable; summary `3 failed in 6.64s`
- **Exit status**: 1
- **Evidence file**: `test-evidence/us2-red-states.txt`
- **Subject matcher**: `不可读` with path and `不可读` field lines, not silent `未记录`; exit code unchanged by a file-level state alone.

### Slot I-LEDGER-SPINE-STATES (T014)

- **Planned node ids**: undeclared pattern → `适用性不可判定`; zero-line `items.jsonl` stays `为空`; six group headings present and in order with additive lines
- **Node ids (authored)**: `test_undeclared_pattern_and_zero_line_ledger_states`, `test_four_state_discipline_on_new_surfaces`
- **Command**: same single-entry command as the slot above (2026-11-26; red before T015–T017)
- **Real output**: `AssertionError: assert '适用性不可判定' in 'Team View: Degraded Fixture Team（undeclared-degraded）…'` — the undeclared-pattern spine state is absent; the four-state test fails on the `不可读` member; summary `3 failed in 6.64s`
- **Exit status**: 1
- **Evidence file**: `test-evidence/us2-red-states.txt`
- **Subject matcher**: FR-007…FR-010, FR-025.

## US3 contract — `tests/contract/test_team_view_degradation_contract.py` (authored T019)

### Slot C-CLOSED-SETS

- **Planned node ids**: `test_reason_set_is_closed`, `test_envelope_keys_unchanged_with_nested_additions`, reverse samples
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_team_view_degradation_contract.py -k "closed or envelope"`
- **Real output**: _(filled by T019)_
- **Exit status**: _(filled by T019)_
- **Evidence file**: `test-evidence/us3-red-contract.txt`
- **Subject matcher**: `{engine-degraded, report-recognition-uncertain}` 2/2 exit-5 mapping; `0/2/3/4/5` unchanged; ten-key envelope with nested additions only; `degraded` true iff a reason is active; reason-outside-set reverse sample.

### Slot C-SINGLE-ENTRY

- **Planned node ids**: `test_single_recognition_entry_source_scan`, `test_script_interface_stays_closed`
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_team_view_degradation_contract.py -k "single_recognition or script_interface"`
- **Real output**: _(filled by T019)_
- **Exit status**: _(filled by T019)_
- **Evidence file**: `test-evidence/us3-red-contract.txt`
- **Subject matcher**: exactly one `def classify_runs(` and one compiled timestamp grammar; overview calls the same entry; closed CLI surface with zero-write `-h`/`--help`/`--version`.

### Slot C-LABEL-CLOSURE

- **Planned node ids**: `test_label_closure_both_directions` and the label subset member tests (`test_missing_state_subset_members` … `test_no_substitute_label_or_empty_reason`)
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_team_view_degradation_contract.py -k "label or subset_members or residue_line_form or roster_not_comparable or substitute_label"`
- **Real output**: _(filled by T019)_
- **Exit status**: _(filled by T019)_
- **Evidence file**: `test-evidence/us3-red-contract.txt`
- **Subject matcher**: label constants ↔ `contracts/view-labels.contract.md` in both directions; label-outside-owner reverse sample; every member has an emitting site.

### Slot C-THREE-SURFACE-CONSISTENCY

- **Planned node ids**: `test_three_surfaces_cite_the_owner`, `test_report_naming_owner_and_schema_unchanged_since_baseline`, import-root audit
- **Command**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_team_view_degradation_contract.py -k "three_surfaces or naming_owner or import"`
- **Real output**: _(filled by T019)_
- **Exit status**: _(filled by T019)_
- **Evidence file**: `test-evidence/us3-red-contract.txt`
- **Subject matcher**: docs page / skill / program declaration each name both reason ids and cite `contracts/team-view-program.contract.md`; `git show 54c6efa8c:` equality for the naming owner and `create-mode.md`; import-root audit (stdlib ∪ repo-local ∪ pytest, zero new third-party).

## Green reading (T012, 2026-11-26)

Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_team_view_report_recognition.py tests/integration/test_team_view_degradation.py -q` → exit 0, `12 passed in 6.59s` (full capture `notes/us1-green.txt`).

| Slot | Node | Red (T006/T007) | Green (T012) |
|------|------|-----------------|--------------|
| U-GRAMMAR | `test_stamp_grammar_accepts_exactly_the_five_forms` | AttributeError `parse_stamp` | pass |
| U-CLASSIFIER | `test_classification_order_is_fixed` | AttributeError `classify_run_file` | pass |
| U-LATEST | `test_latest_is_maximum_parsed_timestamp_with_name_tiebreak` | AttributeError `classify_runs` | pass |
| U-TOKEN | `test_normalized_token_is_the_single_value` | AttributeError `classify_runs` | pass |
| U-RESIDUE | `test_residue_presentation_is_bounded` | AttributeError `classify_runs` | pass |
| U-UNCERTAINTY | `test_uncertainty_predicate_needs_readable_runs_and_residue` | AttributeError `classify_runs` | pass |
| I-PRODUCTION-REPLICA | `test_production_replica_latest_is_the_parsed_maximum` | latest hidden by the narrow template | pass (latest = parsed maximum, 5/5, exit 5) |
| I-CORPUS-REPLICA | `test_corpus_style_reports_are_recognized` | all 13 read as unrecognized | pass (13/13, exit 0) |
| I-RESIDUE-ONLY | `test_residue_only_runs_state_is_not_empty_or_missing` | rendered `运行报告: 为空` | pass (residue-only state, exit 5) |
| I-AUX-SAMESTAMP | `test_auxiliary_artifact_never_becomes_latest`, `test_same_stamp_tie_break_is_name_ascending` | auxiliary line absent / tie not applied | pass |
| I-OVERVIEW-REUSE | `test_overview_matches_single_view_and_discloses_uncertainty` | residue row `未记录` | pass (token equality + inline marker, exit 0) |

Test-side correction during T012 (disclosed): the U-LATEST fixture originally mixed stamp forms, so an ISO-dashed name beat the intended name-ascending tie; the fixture now uses two same-form same-stamp names (`20261125T140000Z-report.md` / `20261125T140000Z-93cc-report.md`). The production rule was not changed, and the red reading above was taken on the pre-correction fixture of the same node (the failure cause is the absent `classify_runs`, independent of fixture data).

Supporting real-corpus smoke (read-only, same tree): `viz-skill-arena` now reads `运行报告: 已列出（共 5 份…）` with latest `2026-09-15T090000Z-report.md` at exit 0; `session-driven-self-improvement` exits 5 with the bounded auxiliary/residue lines and the `降级（degraded）` block naming `report-recognition-uncertain`; the overview row for it carries `20261008T090000Z（report-recognition-uncertain：残留 2）` at exit 0.

## Regression guards (not red slots)

- T020's healthy byte-fidelity and read-only snapshot guards are regression guards: their green
  is meaningful only after the engine amendment, so they are authored/run after implementation
  per the tasks.md migration/regression exception. Readings land in `test-evidence/us3-guards.txt`.
