# Tasks: 子代理 CLI 配置管理与按派发量化（Subagent CLI Config Management & Per-Dispatch Quantification）

**Requirement ID**: 061
**Requirement Key**: 061-subagent-cli-config
**Related Feature**: 061 子代理 CLI 配置管理与按派发量化（from `.specify/memory/features.md`，status Planned at tasks time）
**Input**: Design documents from `.specify/specs/061-subagent-cli-config/`
**Prerequisites**: plan.md, requirements.md, data-model.md, contracts/ (3), quickstart.md, feature-ref.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is MUST-level (pure functions need unit tests, critical flows need regression coverage, cross-service/external contracts need contract/integration tests), and plan.md's Constitution Check locks three new red-first test files plus registered intentional extensions. Principle VII's template-only gate does NOT apply: this feature ships executable runtime code (`scripts/python/execution-config.py`, `scripts/python/exec-quant.py` extension).

**Organization**: Tasks are grouped by user story so each story has an independently testable checkpoint. All implementation edits land in framework sources (left column of plan.md's Mirror Obligations); `.specify/` mirrors are projected only by the fixed generation trio.

## Premise Measurements (generation-time, 2026-10-18; never cached)

Re-measured immediately before writing this file; commands and real output are reproduced so a later reader can re-derive each claim. The naive trap form is written next to the number where a naive count would disagree.

| Premise | Re-derivation command | Measured output |
|---------|----------------------|-----------------|
| New files absent | `for f in scripts/python/execution-config.py templates/execution-config-defaults.yaml tests/contract/test_execution_config_engine.py tests/contract/test_exec_quant_dispatch.py tests/integration/test_init_execution_config.py; do test -e "$f" \|\| echo "MISSING $f"; done` | all five `MISSING` |
| Existing files present | same loop over `scripts/python/exec-quant.py`, `src/specify_cli/__init__.py`, the four skill/reference files, `shared/definitions/subagent-definitions.md`, both docs, and the two pinned test files | all `EXISTS` |
| exec-quant v1 anchors | `grep -nE '^(ACTIONS\|SCHEMA_VERSION\|PROVENANCES\|UNIT_TYPES)' scripts/python/exec-quant.py` | `33:ACTIONS = ("collect", "list-records", "score")`, `36:SCHEMA_VERSION = 1`, `38:PROVENANCES = ("measured", "carried", "user-given")`, `39:UNIT_TYPES = ("command", "skill", "custom-unit")`, `_UNIT_ID_RE` at 54 |
| Existing pin lines | `grep -n 'ACTIONS_CLOSED_SET\|PROVENANCE_DOMAIN\|MEASURABLE_PATHS\|schema_version == 1' tests/contract/test_exec_quant_engine.py`; `grep -n 'expected = {"collect"' tests/contract/test_probe_engine_action_sets.py` | pins at 54 / 57 / 61 / 265; probe action set at 91 |
| Frozen failing baseline | `grep -c '^FAILED' .specify/specs/061-subagent-cli-config/notes/baseline-failed.txt`; `grep -c 'test_exec_quant_engine.py' …/notes/baseline-failed.txt` | **25** FAILED lines; **7** of them in `test_exec_quant_engine.py` (the affected-file set). Capture/comparison form stays owned by `.specify/skills/internal/implement-feature/SKILL.md` § **Test runs** — this row is a dated record, not a second owner |
| Current test tree (re-run at generation) | `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract tests/integration -q --no-header -p no:cacheprovider` | `25 failed, 3287 passed, 1 skipped, 1 warning in 266.98s`. **Trap**: the pass count is 3287, not the plan's 3278 (+9), because the untracked `tests/contract/test_progress_reporting.py` is collected. The FAILED set still has 25 names and still has 7 in `test_exec_quant_engine.py`, but it differs from the frozen record by one unrelated swap: new `tests/contract/test_goal_migration.py::TestLiveSurfacesAreMigrated::test_no_live_face_file_retains_the_old_path` (measured cause: a transient `.baseline-check/` directory existed during the run and was gone afterwards — the node passes when re-run alone), gone `tests/contract/test_instructions_section_propagation.py::test_c1_live_instructions_carry_all_template_sections` (consistent with the excluded dirty instructions changes). Neither is 061; T002 MUST re-freeze against the current tree before any 061 edit |
| Generation baseline | `python3 scripts/python/sync-mirrors.py --check`; `python3 scripts/python/regen-command-copies.py --check`; `python3 scripts/python/probe-utils.py --action compile-embeds --check` | all exit 0; templates 21 / scripts 108 / shared **51**; regen OK; compile-embeds 73 units, zero drift. **Trap**: plan.md's dated record says shared 50 — the current 51 includes the untracked `shared/guidelines/progress-reporting.md` + mirror pair, which are excluded from 061. 061's criterion is zero NEW drift on its own touched pairs, never the absolute shared count |
| Feature registry | `awk -F'\|' '$2 ~ /^ *061 *$/ {…}' .specify/memory/features.md`; `grep -n 'Total Features' .specify/memory/features.md` | 061 status = `Planned`; `Total Features: 60` |
| Dirty files excluded from 061 | `git status --short` | `progress-reporting` guideline + test, instructions mirrors/templates, `records.jsonl`, `glossary.md`, session/feedback records — none is a task target or commit target |

## Definition of Done (DoD)

- DoD-1: All task rows are `[X]` (or `[~]` with a recorded reason and `deferred_tasks=` entry); no `[ ]`/`[>]` remains.
- DoD-2: The three new test files are green; both intentional pin extensions are registered; the full suite shows zero NEW failures against the frozen baseline; the 7 affected-file pre-existing failures are individually reconciled.
- DoD-3: The generation trio ran in the fixed order with recorded exit codes; every mirror obligation is byte-identical; both `## Wrap-up` sections are unchanged.
- DoD-4: Quickstart S1–S5 evidence is recorded in `notes/quickstart-run.md`; S6 is explicitly not executed (authorization-gated).
- DoD-5: The two plan decisions (defaults layer may provide `mode`; claude+declared is unreachable) are confirmed in code/tests; the listed open points are confirmed or explicitly revised in `verification.md`.
- DoD-6: Only 061 framework sources, generated mirrors, tests, docs, and spec artifacts were touched; no unrelated dirty file entered any 061 commit.
- DoD-7: The repository's runtime defaults layer exists at `.specify/agents/execution/configs/_defaults.yaml` (seeded by T033, byte-equal to the template, idempotent), and T030 records the driver's actual dispatch path plus the runtime defaults existence as the FR-027 prerequisite evidence in `verification.md`.

**DoD Status**: pending

## Completion Gate

- GATE-1: Zero NEW failures vs the frozen baseline — check: `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract tests/integration -q --no-header -p no:cacheprovider > /tmp/061-current-pytest.txt 2>&1; grep '^FAILED ' /tmp/061-current-pytest.txt | sed 's/ - .*//' | sort > /tmp/061-current-failed.txt; comm -13 <(grep '^FAILED' .specify/specs/061-subagent-cli-config/notes/baseline-failed.txt | sed 's/ - .*//' | sort) /tmp/061-current-failed.txt` prints nothing (empty output, exit 0); any printed nodeid is a NEW failure. The registered intentional extensions (T012/T013) are same-nodeid pin edits and MUST NOT surface as new nodeids; their registration in `verification.md` is a separate disclosure step and MUST NOT be used as a gate exception.
- GATE-2: Every mirror obligation byte-identical — check: `python3 scripts/python/sync-mirrors.py --check` exit 0 plus `diff -q` on each of the six touched pairs (two scripts, one template, two internal skill trees, one shared definition).
- GATE-3: Generation faces clean — check: `python3 scripts/python/probe-utils.py --action compile-embeds --check` reports 73 units zero drift and `python3 scripts/python/regen-command-copies.py --check` exits 0.
- GATE-4: No open task rows — check: `grep -cE '^- \[[ >]\]' .specify/specs/061-subagent-cli-config/tasks.md; true` returns 0.
- GATE-5: Per-SC coverage with status in verification — check: `for sc in SC-001 SC-002 SC-003 SC-004 SC-005 SC-006; do grep -qE "^\| *$sc *\|.*\b(pass|fail|not-run)\b" .specify/specs/061-subagent-cli-config/verification.md || { echo "missing status: $sc"; exit 1; }; done` exits 0.
- GATE-6: Quickstart evidence — check: `grep -c '^## S[1-5]' .specify/specs/061-subagent-cli-config/notes/quickstart-run.md` returns 5 and the S6 not-executed note is present.
- GATE-7: Commit surface and runtime-precondition audit — check: `git show --stat --name-only <061 commits>` lists only the feature's spec, framework sources, generated mirrors, tests, docs, and the runtime defaults layer (`.specify/agents/execution/configs/_defaults.yaml`); no excluded dirty file appears; `test -f .specify/agents/execution/configs/_defaults.yaml` exits 0; `verification.md` carries T030's four FR-027 fields.

## Environment Prerequisites

- `qodercli 1.1.73`: available — probe: `qodercli --version` @ 2026-10-18; affected: quickstart S6 only (optional real dispatch, explicit authorization; never blocking).
- Test interpreter `/Users/liuqiming.lqm/project/profiles/.venv/bin/python` (pytest 9.1.1): available — probe: `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest --version` @ 2026-10-18; the repo `.venv` lacks pytest. Affected: T002, T010, T017, T025, T027.
- Docker / registry / live cluster / network: not required by any task.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different write targets, no dependencies).
- **[Story]**: Which user story this task belongs to (US1–US4); Setup, Foundational, and Polish rows carry no story label.
- **[blockedBy: Txxx]** (optional): explicit dependency tag; the executor refuses to start the row until every listed row is `[X]`.

---

## Phase 1: Setup (Shared Measurement Evidence)

**Purpose**: Freeze the pre-change measurements and the failing-test baseline before any 061 edit.

- [ ] T001 Record the generation-face pre-change baseline in `.specify/specs/061-subagent-cli-config/notes/pre-change-measurements.md` by running `python3 scripts/python/sync-mirrors.py --check`, `python3 scripts/python/regen-command-copies.py --check`, and `python3 scripts/python/probe-utils.py --action compile-embeds --check`; paste commands, exit codes, and real output, including the trap note that the current shared count is 51 (untracked `shared/guidelines/progress-reporting.md` pair, excluded from 061) while plan.md's dated record says 50, and state that 061's verify criterion is zero NEW drift on its own touched pairs.
- [ ] T002 [blockedBy: T001] Confirm or re-freeze the failing-test baseline at implementation start from the owner procedure in `.specify/skills/internal/implement-feature/SKILL.md` § **Test runs**: first append the plan-time frozen list (25 FAILED, 7 in `tests/contract/test_exec_quant_engine.py`) plus the generation-time one-node swap explanation to `.specify/specs/061-subagent-cli-config/notes/pre-change-measurements.md`, then re-freeze the spec-dir baseline against the current tree so T027 compares like with like; the swap (`test_goal_migration.py::TestLiveSurfacesAreMigrated::test_no_live_face_file_retains_the_old_path` new — a transient `.baseline-check/` directory during the generation run, passing when re-run alone; `test_instructions_section_propagation.py::test_c1_live_instructions_carry_all_template_sections` gone — consistent with the excluded dirty instructions changes) is not caused by 061.

**Checkpoint**: Measurements are frozen and every later "before/after" claim has a recorded pre-change side.

---

## Phase 2: Foundational (Blocking Prerequisite)

- [ ] T003 Create `templates/execution-config-defaults.yaml` as the single defaults-layer template owner with the dated initial content from contract C-DW-07 (`cli: qodercli`, `model: DeepSeek-Flash`, `reasoning_effort: max`, `context_window: 1000000`, `quantification.method: auto`; no `mode` key — quickstart S2 appends it in its fixture). Acceptance: the file contains exactly those five keys and no built-in default value exists anywhere else.

**Checkpoint**: The defaults-layer content owner exists; US1 fixtures and US3 seeding can build on it.

---

## Phase 3: User Story 1 - 配置分层解析与 CLI 能力矩阵 (Priority: P1) 🎯 MVP

**Goal**: A stdlib-only engine at `scripts/python/execution-config.py` resolves the three layers, validates every value against the code-side capability matrix, and emits effective config, `config_id`, `source_chain`, `skipped_layers`, `cli_args`, `requires_external`, a snapshot path, and `quantification{requested,resolved}`.

**Independent Test**: Call `resolve` / `validate` / `list-configs` on fixture workspaces with no real dispatch; assert merge results, provenance chains, `config_id` stability, STR-013 verbatim `cli_args`, and exit 2 with field + supported set for every negative matrix case.

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T004 [US1] [blockedBy: T003] Author `tests/contract/test_execution_config_engine.py` with one test class per clause group covering C-EC-01..C-EC-15 (identity/actions, paths/defaults, YAML subset, schema/validation, merge/clear/source_chain, identity conflicts, capability matrix, quantification, `cli_args`, `config_id`, snapshot, `validate`, `list-configs`, errors/warnings, and both claude zero-leak paths), using temp workspaces and explicit `--workspace-root` only; the SC-001 fixture's defaults layer MUST declare `mode: external`; cover the F-03 precedence (defaults `mode: native|virtual` + agent/inline override resolves `external` with `requires_external=true`; explicit agent/inline `mode: native|virtual` + any override exits 2), the external + null `cli` rejection, and `qodercli`/`claude` `auto` positive resolutions (requested `auto` is resolved first and never matrix-rejected); paste the red-first run (command, real output, exit code) into `.specify/specs/061-subagent-cli-config/notes/red-first-evidence.md`. Acceptance: failure is caused by the missing engine, not test syntax; STR-013 and `config_id` stability are literal assertions; the precedence, null-cli, and auto-positive cases are present and red for the right reason.

### Implementation for User Story 1

- [ ] T005 [US1] [blockedBy: T004] Implement in `scripts/python/execution-config.py`: stdlib-only argparse with `--action resolve|validate|list-configs` and the 0/1/2 exit contract, workspace-root resolution through the sibling `memory-utils.py`, the C-EC-03 YAML subset parser (comments, `key: value`, one `quantification:` level; reject tabs/lists/deeper nesting/duplicates), layer loading, and schema/type/enum/log_dir/extra_flags validation. Acceptance: the C-EC-01..C-EC-04 cases in `tests/contract/test_execution_config_engine.py` turn green.
- [ ] T006 [US1] [blockedBy: T005] Implement in `scripts/python/execution-config.py`: `defaults < agent-config < inline` merge, `""`/`auto` clear sentinels for the five value fields, effective config always holding eight keys (cleared/absent = `null`), `source_chain` (file layers carry workspace-relative `path`; inline/derived omit it), `skipped_layers`, whole-defaults-layer skip on a different explicit CLI, `mode`/`cli` identity conflict rejection, native-first derivation, and `requires_external`. Acceptance: the C-EC-05..C-EC-07 cases turn green.
- [ ] T007 [US1] [blockedBy: T006] Implement in `scripts/python/execution-config.py`: the single-owner `CAPABILITY_MATRIX` (qodercli / claude / codex / opencode / unknown), field + supported-set rejection messages, fixed-order `cli_args` generation, quantification `requested`/`resolved` with the four-step auto order (resolve `auto` first, then apply the matrix to the **resolved** method only), host detection (`--host-cli` → `SPECKIT_HOST_CLI` → `exec-quant.collect_agent()` → `unknown`), the external + null `cli` rejection, and `declared`/`qoder-settings` constraints (declared covers explicit and auto-resolved) with no downgrade. Acceptance: the C-EC-08..C-EC-10 cases turn green, including both claude zero-leak paths and `qodercli`/`claude` `auto` positive resolutions.
- [ ] T008 [US1] [blockedBy: T007] Implement in `scripts/python/execution-config.py`: canonical `config_id` (sha256 of sorted/compact UTF-8 JSON, first 16 hex), atomic snapshot write under `config-snapshots/<config_id>.json`, `validate` (no snapshot, `{target, valid, errors[]}`), `list-configs` (sorted, excludes `_defaults.yaml`, reports invalid entries without aborting), and the exit 2 / exit 1 / warning surfaces including the auto→`none` warning. Acceptance: the C-EC-11..C-EC-15 cases turn green.
- [ ] T009 [P] [US1] [blockedBy: T008] Run quickstart S2 and S3 against fresh temp workspaces and paste commands, exit codes, and actual output into `.specify/specs/061-subagent-cli-config/notes/quickstart-run.md` under `## S2` and `## S3`; assert STR-013 verbatim `cli_args`, stable `config_id`, snapshot path, and that every negative case exits 2 naming the field and supported set (including the missing-defaults path and `specify init` repair hint).
- [ ] T010 [P] [US1] [blockedBy: T008] Run `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_execution_config_engine.py -q` and append the green run (command, output, exit code) plus the red→green transition to `.specify/specs/061-subagent-cli-config/notes/red-first-evidence.md`; every C-EC-01..C-EC-15 clause group must be green.

**Checkpoint**: US1 is independently deployable: the engine resolves, validates, lists, snapshots, and rejects unsupported combinations without any dispatch.

---

## Phase 4: User Story 2 - 每次派发一条量化记录 (Priority: P1)

**Goal**: `exec-quant.py` v2 gains `unit_type=agent`, the `collect-dispatch` action, the 11-field `config` group, method-dependent `llm`, and `quality.exit_code`; one dispatch label produces exactly one idempotent record, queryable by unit type and `config_id`.

**Independent Test**: Feed fixture `<label>.jsonl` / `<label>.status` / snapshot artifacts to `collect-dispatch` with no real CLI; assert one row, the config group, method-specific `llm`, measured quality leaves, idempotency, list filters, v1 read-only normalization, and score support.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T011 [US2] [blockedBy: T003] Author `tests/contract/test_exec_quant_dispatch.py` covering C-EQ-02..C-EQ-10 with fixture snapshots, `<label>.jsonl`, and `<label>.status` under temp workspaces (never a real dispatch or the framework repo's store), including a `claude + none` snapshot whose resulting record's `config` group contains zero "qoder defaults" literals (`DeepSeek-Flash` / `max` / `1000000` / `qodercli`; `auto` and the host-evidence `agent` group excluded); paste the red-first run into `.specify/specs/061-subagent-cli-config/notes/red-first-evidence.md`. Acceptance: red because `collect-dispatch` is absent from `ACTIONS`/argparse; fixture snapshots are written by the test with canonical JSON, not by the engine.
- [ ] T012 [US2] [blockedBy: T011] Extend the intentional pins in `tests/contract/test_exec_quant_engine.py`: `ACTIONS_CLOSED_SET` (L54) add `collect-dispatch`; `PROVENANCE_DOMAIN` (L57) add `configured`; `MEASURABLE_PATHS` (L61) add `("quality","exit_code")`; `schema_version == 1` (L265) → `== 2`; full-schema key set (L549) add `config`; unit-id/type fixtures add `agent:`/`agent`; tighten every assertion to the v2 contract and list each extension in `.specify/specs/061-subagent-cli-config/notes/red-first-evidence.md`.
- [ ] T013 [US2] [blockedBy: T012] Extend `tests/contract/test_probe_engine_action_sets.py::test_exec_quant_action_set_exact` (L91) expected set to add `collect-dispatch`; append the red-first evidence to `.specify/specs/061-subagent-cli-config/notes/red-first-evidence.md`.

### Implementation for User Story 2

- [ ] T014 [US2] [blockedBy: T011,T012] Extend `scripts/python/exec-quant.py`: `SCHEMA_VERSION=2`, `ACTIONS` and argparse add `collect-dispatch`, `PROVENANCES` add `configured`, `UNIT_TYPES` add `agent`, the `agent:<slug>` unit-id grammar, `collect` writing the v2 `config` group (11 leaves `not_evaluated`) and `quality.exit_code=not_evaluated`, and `collect` rejecting `agent:` units with exit 2. Acceptance: the C-EQ-01/C-EQ-02 cases and the extended pins turn green.
- [ ] T015 [US2] [blockedBy: T014] Implement `collect-dispatch` in `scripts/python/exec-quant.py`: required `--unit-id agent:<slug> --run-id <label> --snapshot <path> --config-id <id>`, snapshot kind/schema/recomputed-id integrity checks (exit 1, no record), the exact 11-field `config` group from the snapshot (null effective values → `not_evaluated`), `llm` by `declared`/`qoder-settings`/`none`, and `quality.exit_code`/`elapsed_ms`/`tokens`/`errors` using the exist-only stream/status extraction rules. Acceptance: the C-EQ-03..C-EQ-06 cases turn green.
- [ ] T016 [US2] [blockedBy: T015] Implement in `scripts/python/exec-quant.py`: idempotency key `(unit_id, run_id)` under one POSIX `fcntl.flock` with a documented non-POSIX degradation, `list-records --unit-type agent --config-id`, v1 read-only output normalization, `score` for agent records, and unchanged masking / 64 KiB cap / append-only / non-blocking guarantees. Acceptance: the C-EQ-07..C-EQ-10 cases turn green.
- [ ] T017 [US2] [blockedBy: T016,T008] Run quickstart S4 (resolve → fixture jsonl/status → collect-dispatch twice → list-records → score) and paste commands/output into `.specify/specs/061-subagent-cli-config/notes/quickstart-run.md` under `## S4`; assert exactly one row, `method_resolved=qoder-settings`, all 11 config fields, measured exit code/tokens/elapsed, and a byte-identical repeat call; also run `tests/contract/test_exec_quant_dispatch.py` green and append the red→green evidence to `.specify/specs/061-subagent-cli-config/notes/red-first-evidence.md`.

**Checkpoint**: US2 is independently testable with fixture artifacts, and in production consumes US1's snapshot to land one `agent:<slug>` record per dispatch label.

---

## Phase 5: User Story 3 - 派发接线、schema 真源扩展与默认值播种 (Priority: P2)

**Goal**: run-agent resolves/discloses configuration and passes `cli_args` through `dispatch.sh` before collecting; preflight ④ checks the resolved configuration; create-agent's execution-config reference becomes the schema authority; subagent-definitions gains the three-layer/quantification pointers; `specify init` seeds `_defaults.yaml` once; both docs record the verified facts.

**Independent Test**: Run the init integration test with and without an existing `_defaults.yaml`; audit the run-agent / preflight text and dispatch command shape; no real external dispatch is required.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T018 [US3] [blockedBy: T003] Author `tests/integration/test_init_execution_config.py`: seeds when absent, byte-identical when present, a user edit is never overwritten, an explicitly supplied missing source raises, and the packaged fallback path is used; paste the red-first run into `.specify/specs/061-subagent-cli-config/notes/red-first-evidence.md`. Acceptance: red because `ensure_agent_layer_dirs` has no `defaults_source` parameter.

### Implementation for User Story 3

- [ ] T019 [P] [US3] [blockedBy: T018] Wire `skills/internal/run-agent/SKILL.md` § Run Mode: resolve before dispatch with the exact inline argument names; a non-zero `resolve` MUST stop before dispatch and report the engine message; disclose `config_id`/`mode`/`cli`/`model`/`reasoning_effort`/`context_window`/`source_chain`/`skipped_layers`/`quantification`/`requires_external`; dispatch externally through `skills/internal/create-team/scripts/dispatch.sh` with `-- <cli_args>` in the engine's order (no reorder/re-quote/filter) and an absolute `DISPATCH_LOG_DIR`; for remote topology run resolve and `collect-dispatch` on the target project side; then call `collect-dispatch` non-blockingly; the engine is the only resolver and `## Wrap-up` MUST NOT be edited. Acceptance: a text audit shows the resolve/stop-on-error/disclose/`-- <cli_args>`/absolute-log-dir/collect sequence and the target-side note for remote topology; `git diff` on the `## Wrap-up` region is empty.
- [ ] T020 [P] [US3] [blockedBy: T018] Rewrite row ④ in `skills/internal/run-agent/references/dispatch-preflight.md` to the "已解析配置" check (resolve exit 0 + non-empty `config_id`; external requires `requires_external=true`; the same inline topology/override inputs, at minimum `--mode external`), keep the `model`, `effort`, `context`, and `待补` literals, and do not copy the capability matrix. Acceptance: the row names the engine check, keeps the four literals, and contains no matrix table.
- [ ] T021 [P] [US3] [blockedBy: T018] Expand `skills/internal/create-agent/references/execution-config.md` into the schema authority (layer precedence, clear sentinels, identity vs override, coverage vs conflict, defaults skip, quantification methods by engine reference, defaults path/seeding, snapshot semantics, `CAPABILITY_MATRIX` by code-owner reference) and add the write-then-validate obligation to `skills/internal/create-agent/SKILL.md` § Execution Config Capability. Acceptance: the reference covers every listed schema topic by pointer and the SKILL states the write-then-validate exit-2 rule.
- [ ] T022 [P] [US3] [blockedBy: T018] Extend `shared/definitions/subagent-definitions.md` § Execution Topology Declaration with the three configuration layers, coverage vs conflict, defaults whole-layer skip, and snapshot/quantification provenance; update the schema pointer from `skills/internal/create-agent/SKILL.md` to `references/execution-config.md`; preserve heading order and the five visibility obligations. Acceptance: the section contains the three-layer/coverage-vs-conflict/defaults-skip/snapshot topics, the new schema pointer, and an unchanged heading order.
- [ ] T023 [P] [US3] [blockedBy: T018] Extend `ensure_agent_layer_dirs(root_path, defaults_source=None)` and `copy_local_templates` in `src/specify_cli/__init__.py`: seed `execution/configs/_defaults.yaml` only when absent from the explicit source or the packaged `templates/execution-config-defaults.yaml`; never overwrite; an explicitly supplied missing source raises. Acceptance: `tests/integration/test_init_execution_config.py` turns green.
- [ ] T024 [P] [US3] [blockedBy: T018] Add the dated qodercli 1.1.73 verified-flags/settings section to `docs/reference/cli/qoder-cli.md` and the defaults-layer / three-layer / schema-owner / `collect-dispatch` pointers to `docs/reference/agents/templates-and-agents.md`; neither document may copy the capability matrix or field table. Acceptance: both documents carry the dated record/pointers and no copied table.
- [ ] T025 [US3] [blockedBy: T019,T020,T021,T022,T023,T024] Run quickstart S5 (seed, second init byte-identical, user edit preserved, explicit missing source raises) and paste commands/output into `.specify/specs/061-subagent-cli-config/notes/quickstart-run.md` under `## S5`; run `tests/integration/test_init_execution_config.py` green and append the red→green evidence; audit the edited schema/definition/doc surfaces for single-owner pointers and record the audit in `.specify/specs/061-subagent-cli-config/verification.md`.

**Checkpoint**: A downstream project can init, receive the defaults layer idempotently, discover the schema, and dispatch with the resolved configuration.

---

## Phase 6: User Story 4 - 既有机制非回归与生成面一致性 (Priority: P2)

**Goal**: Prove that 059 unit records, 060 dispatch contracts, probe/action-set/preflight pins, the generation trio, and the driver's dispatch shape all survive the change; reconcile every affected existing failure by name.

**Independent Test**: Compare sorted FAILED nodeids against the frozen baseline, reconcile the 7 affected-file nodes, run the generation trio, and re-read the dispatch contract — no real external dispatch required.

- [ ] T026 [US4] [blockedBy: T008,T016,T019,T020,T021,T022,T023,T024] Run the generation trio in the fixed order from repo root: `python3 scripts/python/probe-utils.py --action compile-embeds --write` (expect no-op), `python3 scripts/python/regen-command-copies.py` (expect no-op), `python3 scripts/python/sync-mirrors.py --write`; then re-run all three `--check` forms and record exit codes/output in `.specify/specs/061-subagent-cli-config/verification.md`. Acceptance: `--check` exit 0, 73 units zero drift, and no generated file was hand-edited.
- [ ] T027 [US4] [blockedBy: T026] Re-run the full contract+integration suite with `/Users/liuqiming.lqm/project/profiles/.venv/bin/python`, compare sorted FAILED nodeids against `.specify/specs/061-subagent-cli-config/notes/baseline-failed.txt`, and require `comm -13` to be empty — no exclusion applies at the gate; the T012/T013 pin edits are same-nodeid edits and MUST NOT surface as new nodeids; register each extension in `.specify/specs/061-subagent-cli-config/verification.md` as a separate disclosure step.
- [ ] T028 [US4] [blockedBy: T027] Reconcile the 7 pre-existing failures in `tests/contract/test_exec_quant_engine.py` with a before/after nodeid comparison and explain each as fixed / intentionally changed / unchanged in `.specify/specs/061-subagent-cli-config/verification.md`; none may be counted as a regression or silently dropped.
- [ ] T029 [US4] [blockedBy: T026] Verify byte-identity for every Mirror Obligations row (`scripts/python/execution-config.py`, `scripts/python/exec-quant.py`, `templates/execution-config-defaults.yaml`, run-agent SKILL + preflight, create-agent SKILL + reference, `shared/definitions/subagent-definitions.md`) and confirm both `## Wrap-up` sections are unchanged; record the diffs in `.specify/specs/061-subagent-cli-config/verification.md`.
- [ ] T033 [US4] [blockedBy: T023] Seed this repository's runtime defaults layer before any driver dispatch can hit the new resolve/preflight path: invoke `ensure_agent_layer_dirs` (or `specify init`) against the repo root with `templates/execution-config-defaults.yaml` as the source so `.specify/agents/execution/configs/_defaults.yaml` exists; assert `test -f .specify/agents/execution/configs/_defaults.yaml` exits 0, its bytes equal the template's, and a second invocation leaves it byte-identical; confirm the seeded file is tracked (not gitignored) and include it in the 061 commit surface as the runtime defaults layer. Acceptance: the repo has a working defaults layer, seeding is idempotent, and the evidence line is recorded in `.specify/specs/061-subagent-cli-config/verification.md`.
- [ ] T030 [US4] [blockedBy: T019,T020,T022,T033] Re-read the updated dispatch contract surfaces (`skills/internal/run-agent/SKILL.md`, `skills/internal/run-agent/references/dispatch-preflight.md`, `shared/definitions/subagent-definitions.md`) and verify the driving loop's dispatch shape still matches; record four judgement fields in `.specify/specs/061-subagent-cli-config/verification.md`: (1) the re-read surfaces, (2) the contract diff, (3) the driver's actual dispatch path — this line runs the direct runner, so state explicitly whether it bypasses run-agent, (4) whether the dispatch shape is affected plus the verdict; the runtime defaults layer existence (`test -f .specify/agents/execution/configs/_defaults.yaml` → exit 0, from T033) MUST be recorded as the FR-027 prerequisite evidence. If the contract changed incompatibly, stop and fast-fail per FR-027 instead of adapting silently.

**Checkpoint**: Non-regression, mirror consistency, and driver compatibility are evidenced by name and by diff.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T031 [blockedBy: T027] Audit the two plan decisions in code/tests — the defaults layer may provide `mode` (C-EC-06) and claude + `declared` is unreachable by design (C-EC-09, FR-008/US1-5) — plus the open points: exist-only stream-json extraction, macOS `/proc` host detection via `--host-cli`, the same-id snapshot overwrite window, and absolute log dirs; record each as confirmed or explicitly revised in `.specify/specs/061-subagent-cli-config/verification.md` using `scripts/python/execution-config.py` and `scripts/python/exec-quant.py` as the evidence surfaces. A required change is a fast-fail, never a silent adaptation. Acceptance: every listed item has a confirmed or explicitly revised line in `verification.md`.
- [ ] T032 [blockedBy: T009,T017,T025] Consolidate `.specify/specs/061-subagent-cli-config/notes/quickstart-run.md`: S1–S5 each present with real output and teardown, S6 explicitly marked not executed (authorization-gated); map SC-001..SC-006 to their evidence in `.specify/specs/061-subagent-cli-config/verification.md` as a table with exactly six rows of the form `| SC-001 | <evidence> | pass|fail|not-run |` (the third column is one of the three tokens). Acceptance: five `## S1`–`## S5` sections, an explicit S6 note, and six SC rows each carrying an explicit status token.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001 → T002; no feature edit before both are recorded.
- **Foundational (Phase 2)**: T003 blocks every story that consumes the defaults template.
- **US1 (Phase 3, P1, MVP)**: T004 → T005 → T006 → T007 → T008 → T009/T010.
- **US2 (Phase 4, P1)**: T011 → T012 → T013; T014 → T015 → T016; T017 additionally needs T008 (quickstart S4 resolves through the engine). US2 tests use fixture snapshots, so its test-authoring rows can start after T003, in parallel with US1.
- **US3 (Phase 5, P2)**: T018 → T019..T024 (parallel, distinct write targets) → T025.
- **US4 (Phase 6, P2)**: T026 → T027 → T028; T029 after T026; T033 after T023; T030 after the wiring rows and T033. All depend on the implementation rows being green.
- **Polish (Phase 7)**: T031 after T027; T032 after S2/S4/S5 evidence exists.

### User Story Dependencies

- **US1**: independent after T003.
- **US2**: independent for contract tests after T003; production integration consumes US1's snapshot.
- **US3**: independent after T003; its quickstart S5 does not need US1/US2, but the dispatch wiring describes their behavior.
- **US4**: cross-cutting; depends on US1–US3.

### Within Each User Story

- Tests are authored and observed RED before implementation; the only allowed post-implementation test rows are the migration/regression extensions (T012/T013) and the final reconciliation (T027/T028), which are tagged with their blockers.
- Implementation rows run in dependency order; every row that changes the same engine file is sequential by construction.

### Parallel Opportunities

- T009 and T010 (different evidence files).
- T019, T020, T021, T022, T023, T024 (six distinct framework-source surfaces).
- No parallel marker is used where two rows would append to the same evidence file (T011→T012→T013, T026→T027→T028).

---

## Parallel Example: User Story 3

```bash
# Six wiring surfaces can be edited concurrently after the init test is RED:
Task: "Wire run-agent SKILL.md § Run Mode"
Task: "Rewrite dispatch-preflight.md row ④"
Task: "Expand create-agent execution-config.md schema + SKILL.md validate obligation"
Task: "Extend subagent-definitions.md § Execution Topology Declaration"
Task: "Extend ensure_agent_layer_dirs + copy_local_templates"
Task: "Update qoder-cli.md and templates-and-agents.md"
```

---

## Implementation Strategy

### MVP First

**Suggested MVP**: User Story 1 alone — it is independently testable via the contract fixtures and quickstart S2/S3, and it repairs the "configuration written but not effective" gap without any dispatch. The two P1 stories (US1 + US2) are the feature's core pair; US2 is delivered immediately after US1 because its production path consumes US1's snapshot, while its contract tests remain fixture-based and independent.

1. Complete Setup + Foundational.
2. Complete US1 (T004–T010); run its checkpoint.
3. Complete US2 (T011–T017); run its checkpoint.
4. Complete US3 (T018–T025); run its checkpoint.
5. Complete US4 (T026–T030 plus T033); run the full non-regression and generation gates.
6. Complete Polish (T031–T032); then `/speckit.implement` wrap-up.

### Incremental Delivery

- After US1: the resolver is usable by any caller; no dispatch change.
- After US2: dispatch records land with configuration provenance; 059 unit records are unaffected.
- After US3: downstream projects get init seeding and dispatch wiring.
- After US4: the change is proven non-regressive and mirror-consistent.

### Two-Hats Discipline

- Implementation tasks edit only framework sources (`scripts/`, `templates/`, `skills/`, `shared/`, `src/specify_cli/`, `docs/`, `tests/`).
- Mirror/generated surfaces are produced only by T026's fixed order `compile-embeds → regen-command-copies → sync-mirrors`; T029 verifies byte-identity. Never hand-edit `.specify/` mirrors.

---

## Notes

- Tests Mode is ON because Principle IV is MUST-level and the plan explicitly locks red-first test files; this is not a template-only feature, so Principle VII's partial-test gate does not apply.
- The failing-test baseline's path, capture flag, and comparison form are owned by `.specify/skills/internal/implement-feature/SKILL.md` § **Test runs**; `.specify/specs/061-subagent-cli-config/notes/baseline-failed.txt` is the dated baseline record, and T002 preserves the plan-time list in `notes/pre-change-measurements.md` before re-freezing it against the current tree.
- Two plan decisions are registered and must be confirmed, not silently revised: (1) the defaults layer may provide `mode` as a default while it participates (C-EC-06); (2) claude + `declared` is currently unreachable because FR-008/US1-5 rejects explicit model/effort/context on claude (C-EC-09).
- Implementation-time open points are audited by T031: stream-json `duration_ms`/usage fields are exist-only (no guessed shapes), macOS has no `/proc` so native/virtual `qoder-settings` needs `--host-cli`/`SPECKIT_HOST_CLI`, same-id re-resolve can refresh `resolved_at` (collect before re-resolve), and `log_dir` must be absolute for `dispatch.sh`.
- Feature-list review at tasks time: 061 remains `Planned`, `Total Features: 60`, and the task breakdown exposed no new or invalidated feature; no registry edit is required by this phase.
- Unrelated dirty files are excluded from all task targets and commits: the `progress-reporting` guideline + its test, instructions mirrors/templates, `.specify/memory/exec-quant/records.jsonl`, `.specify/memory/glossary.md`, and session/feedback records.
- No task pushes to a remote; commits are explicit-path, single-purpose, and never `git add -A`.
