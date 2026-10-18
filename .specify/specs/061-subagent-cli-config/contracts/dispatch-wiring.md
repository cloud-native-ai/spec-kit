# Contract: 派发接线、真源扩展与默认层播种（Feature 061, US3/US4）

**Data model**: [../data-model.md](../data-model.md) E7；V13–V15
**Mirror source of truth**: `scripts/python/sync-mirrors.py` `MIRROR_PAIRS`（实测于 2026-10-18）

本契约固定「框架源 → 镜像/生成面」的每一个落点。所有编辑 MUST 落在左列框架源；右列由生成命令投影，MUST NOT 手改。

## C-DW-01 run-agent：派发前解析并展示

`skills/internal/run-agent/SKILL.md` § Run Mode MUST add a configuration step before dispatch:

- Invoke `python3 .specify/scripts/python/execution-config.py --action resolve --agent <slug> [inline overrides] --workspace-root <project-dir> --format json`.
- Present (disclosure, not a blocking gate): `config_id`, `mode`, `cli`, effective `model / reasoning_effort / context_window`, `source_chain`, `skipped_layers`, `quantification.{requested,resolved}`, and `requires_external`.
- If `resolve` exits non-zero: stop before dispatch and report the engine's field/support-set message. A missing defaults layer points at `specify init`.
- The inline override argument names passed to the engine MUST be exactly: `--mode`, `--cli`, `--model`, `--reasoning-effort`, `--context-window`, `--extra-flags`, `--log-dir`, `--quantification-method`.
- The skill MUST state that the engine is the only resolver; it MUST NOT merge or normalize configuration itself.

## C-DW-02 run-agent：external 派发透传

- External dispatch MUST reuse `skills/internal/create-team/scripts/dispatch.sh` (no new dispatcher).
- Invocation shape: `DISPATCH_CLI=<cli> DISPATCH_LOG_DIR=<absolute-log-dir> bash <dispatch.sh> <label> <workdir> <prompt-file> -- <cli_args...>`.
- The log dir MUST be absolute: `dispatch.sh` runs `mkdir -p "$LOG_DIR"` **before** `cd "$WORKDIR"`, so a relative value would create/tee in the caller's cwd. Resolve the snapshot's workspace-relative `log_dir` against the target project directory (or default `.specify/agents/execution/logs`) before invoking.
- `<cli_args...>` MUST be the `cli_args` array from `resolve`, in its given order; the skill MUST NOT reorder, re-quote, or filter them.
- The dispatch label MUST be used verbatim as the later `run_id`.
- Remote topology: `resolve` (pre-dispatch) and `collect-dispatch` (post-dispatch) MUST run on the target project side (through the same `ssh` family), so the snapshot, logs, and store are the target project's. The dispatch and log paths are target-host absolute paths.
- The Visibility Contract and the fast-fail injection / anti-nesting obligations in `shared/definitions/subagent-definitions.md` remain unchanged and continue to apply.

## C-DW-03 run-agent：派发后非阻塞采集

- After `dispatch.sh` returns, the skill MUST invoke:
  `python3 .specify/scripts/python/exec-quant.py --action collect-dispatch --unit-id agent:<slug> --run-id <label> --snapshot <snapshot-path> --config-id <config_id> --workspace-root <project-dir>`.
- A non-zero exit from `collect-dispatch` MUST be reported (reason included) and MUST NOT change the dispatch result, re-run the dispatch, or delete any artifact.
- The AUTO-GENERATED `## Wrap-up` section MUST NOT be edited; the new calls are body text, not compiled embeds.

## C-DW-04 `dispatch-preflight.md` ④

`skills/internal/run-agent/references/dispatch-preflight.md` row ④ MUST become an "已解析配置" check:

- Command form: run `execution-config.py --action resolve --agent <slug> [the same inline topology/override inputs the dispatch will use, at minimum `--mode external` for an external dispatch] --workspace-root <project-dir>` on the **target project** (remote: through the existing `ssh` family; local: direct).
- Pass criterion: exit 0 and a non-empty `config_id`; external dispatch additionally requires `requires_external=true`.
- Failure: list the missing/illegal fields from the engine's message (待补清单) and re-run after repair; a missing defaults layer points at `specify init`.
- The words `model`, `effort`, `context` MUST remain in the row (060 C-17 compatibility), and `待补` MUST remain in the failure chain. The row MUST NOT copy the capability matrix.

## C-DW-05 create-agent schema reference & validate-after-write

`skills/internal/create-agent/references/execution-config.md` MUST become the schema authority:

- Field-level schema for the defaults layer, agent config, and inline parameters.
- Layering and precedence; clear sentinels (`""` / `auto` for the five value fields).
- Identity vs override fields; cross-layer conflict rejection; defaults-layer skip.
- Quantification methods and the auto order (reference the engine for exact resolution).
- Defaults layer path/content owner and init seeding.
- Snapshot semantics and its role in `collect-dispatch`.
- CLI capability status by reference to `CAPABILITY_MATRIX` (name the code owner; do not copy the table).
- `skills/internal/create-agent/SKILL.md` § Execution Config Capability MUST add a "write then validate" obligation: after writing `configs/<slug>.yaml`, run `execution-config.py --action validate --agent <slug>` and do not report success on exit 2.

## C-DW-06 `subagent-definitions.md` topology additions

`shared/definitions/subagent-definitions.md` § Execution Topology Declaration MUST add:

- The three configuration layers and their precedence (defaults < agent config < inline).
- Which fields are override fields vs topology identity (`mode` / `cli`), and the distinction between **coverage** (a value overrides a lower layer) and **conflict** (identity fields disagree → reject with the fields listed).
- The defaults layer is skippable as a whole when another CLI is selected; no qoder default may leak.
- Config snapshot and quantification method (`requested` vs `resolved`) as the record's provenance.
- The existing pointer that names `skills/internal/create-agent/SKILL.md` as the schema owner MUST be updated to `skills/internal/create-agent/references/execution-config.md` (the field-level schema authority).
- A pointer to the schema owner and the engine; it MUST NOT copy the field table or the capability matrix.
- Existing heading order (Visibility Contract → Dispatch-Time Governance Obligation → Terminology Boundaries) and the 5 numbered visibility obligations MUST remain intact (060 pins).

## C-DW-07 init seeding & idempotency

- `templates/execution-config-defaults.yaml` MUST be the single template owner. Its initial content is a dated record (2026-10-18: `cli: qodercli`, `model: DeepSeek-Flash`, `reasoning_effort: max`, `context_window: 1000000`, `quantification.method: auto`); consumers MUST read the template, not this contract, for the current values.
- `ensure_agent_layer_dirs(root_path, defaults_source=None)` MUST, when `.specify/agents/execution/configs/_defaults.yaml` is absent, copy from `defaults_source` if given, else from `get_resource_path()/templates/execution-config-defaults.yaml` when available.
- An explicitly supplied source that does not exist MUST raise (packaging defect visible), not silently skip.
- An existing target MUST NOT be overwritten; repeated init leaves it byte-identical.
- `copy_local_templates` MUST pass `resource_path / "templates" / "execution-config-defaults.yaml"` to the call so `specify init` always seeds from the packaged owner.

## C-DW-08 Documentation

- `docs/reference/cli/qoder-cli.md` MUST add a dated-record section listing the verified qodercli 1.1.73 dispatch flags (`-m/--model`, `--reasoning-effort`, `--context-window`), settings path/fields, and a pointer to the engine. The section MUST mark the observation as a dated record, not a runtime guarantee.
- `docs/reference/agents/templates-and-agents.md` MUST add a short section pointing at: the defaults layer + seeding, the three-layer precedence, the schema owner, and per-dispatch quantification (`collect-dispatch`). It MUST NOT copy the field table or capability matrix.

## C-DW-09 Mirror & generation obligations

Fixed order and expected effect:

1. `python3 scripts/python/probe-utils.py --action compile-embeds --write` — expected no-op for this feature (no Wrap-up/registry edit); `--check` must stay at 73 units / zero drift.
2. `python3 scripts/python/regen-command-copies.py` — expected no-op (no command-template edit).
3. `python3 scripts/python/sync-mirrors.py --write` — projects the framework-source edits.

| Framework source (edit) | Mirror / generated copies | Verify |
|-------------------------|---------------------------|--------|
| `scripts/python/execution-config.py` (new), `scripts/python/exec-quant.py` | `.specify/scripts/python/<same>` | scripts pair零 NEW drift |
| `templates/execution-config-defaults.yaml` (new) | `.specify/templates/execution-config-defaults.yaml` | templates pair零 NEW drift |
| `skills/internal/run-agent/{SKILL.md,references/dispatch-preflight.md}` | `.specify/skills/internal/run-agent/**` | internal pair零 NEW drift; `## Wrap-up` unchanged |
| `skills/internal/create-agent/{SKILL.md,references/execution-config.md}` | `.specify/skills/internal/create-agent/**` | 同上 |
| `shared/definitions/subagent-definitions.md` | `.specify/shared/definitions/subagent-definitions.md` | shared pair零 NEW drift |
| `src/specify_cli/__init__.py` | none (CLI package) | pytest + installed-init integration |
| `docs/reference/{cli/qoder-cli.md,agents/templates-and-agents.md}` | none (dev docs, not distributed) | content audit |

Baseline measured 2026-10-18 before any 061 edit: `sync-mirrors --check` exit 0 (all pairs ok), `regen-command-copies --check` exit 0, `compile-embeds --check` 73 units zero drift. The Verify criterion is "no NEW drift", not a pre-written exit code.

## C-DW-10 Non-regression & test strategy

- New files: `tests/contract/test_execution_config_engine.py`, `tests/contract/test_exec_quant_dispatch.py`, `tests/integration/test_init_execution_config.py`.
- Intentional extensions: `tests/contract/test_exec_quant_engine.py` (schema/provenance/action/measurable paths/list key set/unit domains), `tests/contract/test_probe_engine_action_sets.py` (action set). Each extension MUST be registered in `verification.md`; assertions MUST be tightened to the new contract, never loosened.
- 059 unit behaviors, 060 dispatch texts (C-15/C-16/C-17/C-18/C-19/C-20/C-22 and the fast-fail subsection pins), probe/action-set, and preflight literals MUST have zero NEW failures against `notes/baseline-failed.txt` (25 pre-existing failures, measured 2026-10-18).
- **Affected-file baseline**: 7 of the 25 pre-existing failures are in `test_exec_quant_engine.py` (qoder reader, endpoint, masking, size cap, agent collection) on surfaces this feature edits. The global "zero NEW" comparison is blind there; implementation MUST record a before/after nodeid comparison for that file and explain each changed node as fixed / intentionally changed / unchanged. `verification.md` MUST list them.
- Implementation order: freeze/confirm the baseline → write the new contract tests (red) → implement engines → wire skills/docs/init → run the full suite and compare sorted nodeids.
- `tests/integration/test_init_execution_config.py` MUST cover: seeds when absent; byte-identical when present; no overwrite after user edit; explicit missing source raises.

## C-DW-11 Driver re-read after implementation

After implementation and before dispatching the review stage, the driving loop MUST re-read the updated dispatch contract surfaces (`run-agent` SKILL + preflight + `subagent-definitions`) and record four decidable fields in `verification.md`: (1) the re-read surfaces, (2) the contract diff, (3) the driver's actual dispatch path (direct runner vs run-agent), and (4) whether the dispatch shape is affected plus the verdict. The existence of the runtime defaults layer `.specify/agents/execution/configs/_defaults.yaml` (seeded by T033) MUST be recorded as the FR-027 prerequisite evidence. If the dispatch shape changed in a way the driver cannot follow, the run MUST fast-fail and surface the anomaly; silent adaptation is prohibited (FR-027).
