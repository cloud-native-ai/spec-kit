# Verification Log — 061-subagent-cli-config

baseline_commit=3a62cb28
baseline_date=2026-10-18
baseline_branch=061-subagent-cli-config

baseline_failed_nodeids=24
baseline_passed=3288
baseline_skipped=1
baseline_affected_file_nodes=7

implementation_date=2026-10-18
post_change_commit=be491b33

post_change_failed_nodeids=24 (the baseline set exactly; comm -13 empty, comm -23 empty)
post_change_passed=3417
post_change_new_failures=0
post_change_generation_sync=templates 22 / skills.external 369 / skills.internal 136 / agents 3 / scripts 109 / shared 51 — all ok
post_change_compile_embeds=73 units, zero drift
post_change_defaults_layer=present, byte-equal to the template, seeding idempotent

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=cli_args == ["--model","DeepSeek-Flash","--reasoning-effort","max","--context-window","1000000"]; config_id stable at 72ae1cc218e8aca8 across repeated runs; source_chain covers mode/cli/model/reasoning_effort/context_window/quantification.method, all defaults
SC-001_note=Quickstart S2 + tests/contract/test_execution_config_engine.py::TestResolveMerge (literal assertions)

SC-002_status=pass
SC-002_value=All negative fixtures exit 2 with field + supported set/conflict list (identity conflict, claude flags, codex/opencode external, unknown CLI, external w/o cli, YAML subset, context_window, log_dir, extra_flags, quantification constraints)
SC-002_note=Quickstart S3 (cases 3–6) + TestIdentityConflict/TestSchemaValidation/TestYamlSubset/TestCapabilityMatrix

SC-003_status=pass
SC-003_value=Exactly one agent record per (agent:sample-agent, demo-label); repeat call byte-identical (sha 935e4c37…); config group 11 fields; list-records --unit-type agent --config-id returns it; score works
SC-003_note=Quickstart S4 + tests/contract/test_exec_quant_dispatch.py (38 tests)

SC-004_status=pass
SC-004_value=comm -13 baseline current = empty (0 NEW failing nodeids); 7 affected nodes individually reconciled below
SC-004_note=T027/T028; no gate exclusion used

SC-005_status=pass
SC-005_value=compile-embeds: 73 units / 0 written; regen-command-copies: OK; sync-mirrors: all pairs ok; init seeds when absent, byte-identical when present, user edit preserved, explicit missing source raises
SC-005_note=T026/T029 + quickstart S5 + tests/integration/test_init_execution_config.py (6 passed)

SC-006_status=pass
SC-006_value=claude+none: qoder literal set count 0 in effective config / cli_args / record config group; claude+declared: count 0 in the error surface; auto excluded from counting; record agent group excluded
SC-006_note=TestCapabilityMatrix::test_claude_none_positive_zero_qoder_leak / test_claude_declared_rejection_zero_qoder_leak + TestConfigGroup::test_claude_none_config_group_has_zero_qoder_literals

# -- Success Criteria table (GATE-5 form) --

| SC | Evidence | Status |
|----|----------|--------|
| SC-001 | Quickstart S2 (verbatim cli_args, stable config_id, source_chain) + US1 contract tests | pass |
| SC-002 | Quickstart S3 negative matrix + US1 contract tests (exit 2 + field/supported set) | pass |
| SC-003 | Quickstart S4 (one row, idempotent, 11 config fields, query/score) + US2 contract tests | pass |
| SC-004 | T027 name-level comparison (comm -13 empty) + T028 7-node reconciliation | pass |
| SC-005 | T026 generation trio + T029 byte-identity + S5 seeding idempotency | pass |
| SC-006 | Dual-path zero-leak tests in US1/US2 contract suites | pass |

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=Nothing deferred. S6 (real qodercli dispatch) is authorization-gated by the spec and was not executed; it is not a task and does not block any SC.

# -- Completion Gate --

GATE-1_status=pass
GATE-1_note=Full suite rerun on the final tree: 24 failed, 3417 passed, 1 skipped in 203.69s. Sorted FAILED nodeids vs notes/baseline-failed.txt: `comm -13` printed nothing (0 NEW) and `comm -23` printed nothing (0 gone). The one transitional NEW failure found on the first post-implementation run (`test_shipped_surface_has_no_framework_runtime_references`, caused by framework feature-number references in two shipped files) was repaired by removing the feature references and re-syncing; the rerun is the gate of record.

GATE-2_status=pass
GATE-2_note=sync-mirrors --check exit 0; byte-identical diff for all eight touched pairs (scripts ×2, template ×1, internal skill trees ×2 + their reference files, shared definition ×1). See T029.

GATE-3_status=pass
GATE-3_note=compile-embeds --check: 73 units, zero drift; regen-command-copies --check exit 0; probe write run: “compiled 73 units: 0 written, 73 unchanged”.

GATE-4_status=pass
GATE-4_note=No `- [ ]` or `- [>]` rows remain in tasks.md (all 33 `[X]`).

GATE-5_status=pass
GATE-5_note=Six SC rows above, each carrying an explicit pass/fail/not-run token; structured SC-NNN_status keys also present. All pass.

GATE-6_status=pass
GATE-6_note=notes/quickstart-run.md carries `## S1`–`## S5` (5 sections) and the explicit S6 not-executed authorization note.

GATE-7_status=pass
GATE-7_note=Commit surface: `git show --stat --name-only be491b33` lists exactly the 42 intended files — feature spec, framework sources, generated mirrors, tests, docs, and the runtime defaults layer; no excluded dirty file. `test -f .specify/agents/execution/configs/_defaults.yaml` exit 0. T030's four FR-027 fields are recorded above.

# -- Intentional extensions (registered, never gate exceptions) --

| File | Pin | Extension |
|------|-----|-----------|
| tests/contract/test_exec_quant_engine.py | ACTIONS_CLOSED_SET | + collect-dispatch |
| same | PROVENANCE_DOMAIN | + configured |
| same | MEASURABLE_PATHS | + ("quality","exit_code") |
| same | schema_version | 1 → 2 |
| same | list-records key set | + config |
| same | collect record assertions | config group 11 × not_evaluated; quality.exit_code not_evaluated |
| same | identity fixtures | collect rejects agent:; --unit-type agent accepted for listing |
| tests/contract/test_probe_engine_action_sets.py | exec-quant exact action set | + collect-dispatch |

All eight extensions are same-nodeid edits; none surfaced as a new failing nodeid.

# -- T028: 7 pre-existing affected-file failures, before/after --

Baseline (frozen) and final run both fail these exact 7 nodeids in `tests/contract/test_exec_quant_engine.py`; each is unchanged (macOS has no `/proc`, so the wrapper-host impersonation cannot resolve the host process; this is the pre-existing environment limitation, not a 061 defect):

| Node | Before | After | Disposition |
|------|--------|-------|-------------|
| TestAgentCollection::test_resolved_agent_fields_from_wrapper_host | fail | fail | unchanged (requires Linux `/proc`) |
| TestCredentialDefense::test_engine_masks_credential_shaped_config_values | fail | fail | unchanged (depends on resolved qoder host) |
| TestLLMCollection::test_endpoint_candidates_origin_only | fail | fail | unchanged (host environ read needs `/proc`) |
| TestLLMCollection::test_missing_config_face_degrades_to_marker | fail | fail | unchanged (wrapper host unresolved) |
| TestLLMCollection::test_qoder_adapter_reads_config_face | fail | fail | unchanged |
| TestLLMCollection::test_qoder_adapter_reads_per_model_effort_when_set | fail | fail | unchanged |
| TestSizeCap::test_oversized_record_is_field_truncated_and_capped | fail | fail | unchanged (oversize argv path needs wrapper host) |

None is counted as a regression; none was silently dropped.

# -- T026/T029: generation faces and mirror obligations --

- Fixed order executed: `probe-utils.py --action compile-embeds` → `regen-command-copies.py` → `sync-mirrors.py --write`.
  **Premise correction**: tasks.md/doc used `compile-embeds --write`, but the probe CLI has no
  `--write` flag (write is the default; `--check` verifies). The first invocation exited 2 with
  “unrecognized arguments: --write”; the corrected form ran successfully. This is a premise
  decay, corrected in practice and disclosed here.
- Write results: compile-embeds “0 written, 73 unchanged”; regen “Regenerated command copies for
  4 tools” (no command-template change); sync-mirrors wrote 8 files across templates/internal
  skills/scripts/shared, then a final re-sync after the neutrality fix wrote 2 more.
- `--check` results after all edits: all exit 0; counts templates 22 / external 369 / internal
  136 / agents 3 / scripts 109 / shared 51.
- Byte-identity: all eight touched source↔mirror pairs diff clean.
- `## Wrap-up` sections in run-agent and create-agent SKILL.md are byte-identical to HEAD
  (verified by extracting the section from HEAD and the working tree).

# -- T033 / DoD-7: runtime defaults layer --

- `.specify/agents/execution/configs/_defaults.yaml` exists (exit 0 for `test -f`).
- Content is byte-equal to `templates/execution-config-defaults.yaml`.
- Seeding is idempotent (second invocation leaves bytes unchanged); `git check-ignore` exits 1,
  so the file is trackable and is included in the 061 commit surface.

# -- T030 / FR-027: driver re-read (four decision fields) --

1. **Re-read surfaces**: `skills/internal/run-agent/SKILL.md` (Run Mode), `skills/internal/run-agent/references/dispatch-preflight.md` (row ④), `shared/definitions/subagent-definitions.md` (Execution Topology Declaration).
2. **Contract diff**: run-agent gains a mandatory configuration-resolution step (resolve → disclose → stop on non-zero → external `-- <cli_args>` pass-through with absolute `DISPATCH_LOG_DIR` → post-dispatch `collect-dispatch`, target-side for remote). Preflight ④ changes from host-CLI config-face inspection to “resolved configuration” (resolve exit 0 + non-empty `config_id`; external requires `requires_external=true`), retaining the `model`/`effort`/`context`/`待补` literals. `subagent-definitions` adds the three-layer precedence, coverage-vs-conflict, defaults whole-layer skip, and snapshot/quantification provenance, and repoints the schema to `references/execution-config.md`. The Visibility Contract, fast-fail injection, and anti-nesting obligations are unchanged.
3. **Driver's actual dispatch path**: this line runs a **direct runner** (`/tmp/run-061-implement.sh`, per `.specify/agents/execution/logs/061-line-state.md`), which bypasses `run-agent`; the loop-driver's `dispatch-recipes.md` also provides direct ssh/qodercli shapes and only references preflight ④ by pointer. So the updated run-agent resolve/collect sequence was not on this line's dispatch path.
4. **Affected? verdict**: the driver's dispatch shape is **not broken** — it neither calls the new resolver nor the new collect action, and preflight ④ still accepts its existing evidence form under the new “resolved configuration” wording once a defaults layer exists. Verdict: **compatible, no fast-fail**. Runtime defaults layer (from T033) exists as the FR-027 prerequisite; a future run-agent-mediated dispatch will resolve successfully because the file is present.

# -- T031: plan decisions and open points --

| Item | Verdict | Evidence |
|------|---------|----------|
| Defaults layer may provide `mode` (C-EC-06) | confirmed | `execution-config.py` `evaluate()` mode derivation; tests `test_shared_defaults_mode…`/`test_native_first_when_no_mode_declared`; S3 case 1 |
| claude + declared is unreachable by design (C-EC-09 / FR-008 / US1-5) | confirmed | explicit claude model/effort/context → exit 2 at the matrix; missing values → exit 2 at the declared constraint; test `test_claude_declared_rejection_zero_qoder_leak` |
| Exist-only stream-json extraction | confirmed | `_iter_json_objects` / `_find_int_fields` take only integer keys present in the object; no shape guessing; TestQuality |
| macOS `/proc` host detection via `--host-cli` / `SPECKIT_HOST_CLI` | confirmed | `detect_host_cli` fallback order; `--host-cli` test; direct probe `SPECKIT_HOST_CLI=qodercli` → `qoder-settings` |
| Same-id snapshot overwrite window | confirmed | atomic `os.replace` overwrite; run-agent/SKILL + schema reference require collect before another same-id resolve |
| Absolute log dirs | confirmed | run-agent dispatch step requires absolute `DISPATCH_LOG_DIR`; snapshot carries workspace-relative `log_dir` resolved against the target project |
| L-04: matrix application when `cli=null` (native/virtual) | explicitly adjudicated | the matrix quantification-method check is skipped when no CLI is effective; `declared`/`qoder-settings` constraints still apply. Probe: `mode=native`, `cli=null`, `method=declared` + all three values → resolves `declared` (exit 0) |

# -- T025: single-owner audit of edited surfaces --

- Field-level schema lives only in `skills/internal/create-agent/references/execution-config.md`.
- `shared/definitions/subagent-definitions.md` and both docs point at the schema authority; they do not copy the field table.
- CLI capability values (external support, flags, methods) appear only in `CAPABILITY_MATRIX` (`scripts/python/execution-config.py`); the reference and docs name the owner without reproducing values.
- Defaults content is owned only by `templates/execution-config-defaults.yaml`; the seeded copy is a runtime instance, never a second source.
- The capability matrix is not copied into `dispatch-preflight.md`; the row names the engine check only.

# -- Checklist / registry / traceability refresh (M-03, L-01..L-05) --

- **M-03**: both checklists refreshed — config-quant's 36 CHK boxes are checked with a post-remediation disposition table (G1–G22 → closing location); requirements checklist's stale 241-line note corrected to 253 lines.
- **L-01**: plan risk 3, feature-ref FR-027, and C-DW-11 now carry the four decision fields and the runtime defaults precondition.
- **L-02**: GATE-7 no longer uses the `<061 commits>` placeholder; it references the SHA recorded here (filled in the metadata commit).
- **L-03**: features/061.md status/Last Review and the features.md row refreshed to Implemented (see the metadata commit).
- **L-04**: recorded above (explicit adjudication).
- **L-05**: T022 reworded so the task validator no longer sees it as writing the create-agent SKILL.md (the old pointer is named indirectly).

# -- Notes --

- S6 (real qodercli dispatch) was not executed: explicit authorization was not given in this
  unattended run and real model calls are excluded by the entry instructions. This is not a
  blocking omission (SC-001..SC-006 are covered by deterministic fixtures).
- The 061 run touched only the feature's framework sources, generated mirrors, tests, docs, spec
  artifacts, and the runtime defaults layer; pre-existing dirty files (instructions mirrors,
  `records.jsonl`, `glossary.md`, session/feedback records, progress-reporting guideline) were
  not modified by this run and are excluded from the 061 commits.
- No push was performed.
