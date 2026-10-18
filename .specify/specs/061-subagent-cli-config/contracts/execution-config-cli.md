# Contract: `execution-config.py` CLI（Feature 061, US1）

**Owner (behavior)**: `scripts/python/execution-config.py`（框架源；镜像 `.specify/scripts/python/execution-config.py`）
**Data model**: [../data-model.md](../data-model.md) E1–E5, E7；V1–V12
**Consumers**: run-agent、dispatch-preflight ④、create-agent schema reference、`specify init` seeding

本契约中的 MUST / MUST NOT 为实现与测试的共同判据。所有命令示例都带显式 `--workspace-root`（两顶帽子：不得把测试状态写进框架仓库）。

## C-EC-01 Engine identity & actions

- The engine MUST be a stdlib-only Python 3.8+ script at `scripts/python/execution-config.py`.
- `--action` MUST accept exactly `resolve`, `validate`, `list-configs` (argparse `choices`).
- Exit codes: `0` success; `2` usage / input / configuration error (`InputError`); `1` unexpected or I/O failure.
- Output: human text by default; `--format json` emits one JSON document on stdout. Diagnostics and warnings go to stderr.

## C-EC-02 Paths & defaults layer

- Defaults layer: `<workspace>/.specify/agents/execution/configs/_defaults.yaml`.
- Agent config: `<workspace>/.specify/agents/execution/configs/<slug>.yaml` (optional; absence is not an error).
- Snapshot root: `<workspace>/.specify/agents/execution/logs/config-snapshots/`.
- `resolve` MUST fail with exit 2 when the defaults layer is missing, naming the absolute path and the repair action (`specify init` seeds it from `templates/execution-config-defaults.yaml`). It MUST NOT substitute built-in defaults.
- `--workspace-root` overrides workspace discovery; otherwise the engine resolves it through the shared `memory-utils.py` resolver (sibling engine), matching `exec-quant.py`.

## C-EC-03 YAML subset

The parser MUST accept only:

- blank lines and full-line comments (`#` as the first non-space character);
- top-level `key: value` lines;
- exactly one level of nesting under a top-level `quantification:` line (`method: value`).

The parser MUST reject (exit 2, naming the file and line/key): tab characters anywhere; list syntax (`- ` items or a value beginning with `[`); nesting deeper than one level; a nested line without an active `quantification:` parent; duplicate keys within a section; a non-comment line without `:`; more than one `quantification:` section.

Values MAY be bare or wrapped in one matching pair of single/double quotes. Inline comments are not interpreted (`#` inside a value is part of the value). An empty value (`""` or nothing after `:`) is the clear sentinel where the field allows it.

## C-EC-04 Schema keys & types

- Allowed top-level keys — defaults: `mode, cli, model, reasoning_effort, context_window, extra_flags, log_dir, quantification`; agent config: the same plus `agent`. Any other key MUST be rejected (V3).
- `mode` in the defaults layer is a default value (not a declaration); it participates only while the defaults layer participates and is skipped with the whole layer.
- `quantification` MAY contain only `method`.
- `agent`, if present, MUST equal the requested slug.
- `context_window` MUST be a positive integer (reject booleans, 0, negatives, non-integers).
- `log_dir` MUST resolve inside `<workspace>/.specify/agents/execution/logs` after path resolution (reject `..` escapes and absolute paths outside).
- `extra_flags` MUST be a single line and MUST tokenize with `shlex.split`; tokens equal to `-m` (or a short `-m...` cluster), or beginning `--model`, `--reasoning-effort`, `--context-window` (including `=` forms), MUST be rejected. It MUST NOT contain a newline.
- All loaded layers are validated before merge; an invalid value is rejected even if a higher layer would override it.

## C-EC-05 Layer merge & clear sentinels

- Precedence MUST be `defaults < agent-config < inline`.
- For `model, reasoning_effort, context_window, extra_flags, log_dir`: a missing key inherits the lower layer; a non-empty value overrides; the clear sentinels `""` and `auto` remove the lower-layer value. The effective config MUST always contain all eight keys; a cleared or absent field MUST be `null`. A cleared field MUST NOT appear in `source_chain` or `cli_args`.
- `quantification.method=auto` is a method value, never a clear sentinel; `""` for the method is an invalid enum.
- `source_chain` MUST map every non-null effective field (and `quantification.method`) to `{layer}` with layer ∈ `defaults|agent-config|inline|derived`; file-layer entries additionally carry `path` (workspace-relative). Inline/derived entries MUST omit the `path` key (no null, no empty string).
- When the defaults layer is skipped, `skipped_layers` MUST contain `"defaults"` and none of its keys (including `cli` and `quantification.method`) may participate.

## C-EC-06 Topology identity (`mode` / `cli`)

- `mode ∈ {native, virtual, external}`; no `auto` value is added.
- If agent-config and inline both declare `mode` differently, or both declare `cli` differently, `resolve` MUST exit 2 naming the conflicting field(s).
- `mode` is resolved as: explicit agent-config/inline value; else the defaults layer's `mode` while that layer participates; else `external` when any non-clear override exists at agent-config or inline; else `native` (060 native-first). An explicit `cli` alone MUST NOT switch the mode to external.
- An explicit `cli` combined with an effectively `native`/`virtual` mode MUST be rejected (exit 2): `cli` applies to external dispatch only, so the pair is an identity contradiction. Callers that want qodercli external dispatch MUST declare `mode: external` explicitly (or set it in the participating defaults layer).
- An explicit `mode: native|virtual` combined with any non-clear override from agent-config or inline MUST be rejected (exit 2) with a message directing the caller to `external`.
- The defaults layer's `cli` is a default value, not a declaration: when an explicit `cli` differs from it, the whole defaults layer (including its `mode` and `quantification.method`) is skipped; when equal or absent, defaults participate.
- A `mode` declared in the defaults layer MUST NOT trigger the cross-layer conflict rule; only agent-config vs inline declarations are compared.

## C-EC-07 `requires_external`

`requires_external` MUST be `true` exactly when the effective `mode` is `external`. The mode is external when (a) agent-config/inline declares `mode: external`, (b) the participating defaults layer declares `mode: external` and no higher layer overrides it, or (c) no layer declares `mode` and any non-clear override exists at agent-config or inline. Otherwise the mode is the effective explicit/default `native`/`virtual` value when present, else `native`; `requires_external` is `false`.

## C-EC-08 CLI capability matrix (single owner in code)

- The authoritative **runtime** matrix MUST live in `CAPABILITY_MATRIX` inside the engine. This contract is the dated design specification of the required behavior; the shipped schema reference, `subagent-definitions.md`, and `docs/` MUST reference the code owner and MUST NOT restate the matrix values.
- Behavior the matrix enforces (design specification, 2026-10-18):
  - `qodercli`: external supported; `--model`, `--reasoning-effort`, `--context-window` supported; methods `qoder-settings / declared / none`.
  - `claude`: external supported (visibility contract); the three flags are unverified, so any explicit `model`/`reasoning_effort`/`context_window` value MUST be rejected (exit 2); methods `declared / none` (declared is currently unreachable — see C-EC-09).
  - `codex` / `opencode`: external stream-json unverified; `requires_external=true` MUST be rejected (exit 2); capability extension point retained.
  - Any other CLI value MUST be rejected (exit 2).
- Every rejection message MUST name the offending field and the supported set (CLI or flag or method list), e.g. `field 'model' is not supported by cli 'claude' (supported: none for model; see qodercli)`; no silent drop.

## C-EC-09 Quantification resolution

- Registered methods MUST be exactly `auto / declared / qoder-settings / none`.
- `requested` = highest-layer explicit method; if absent or the defaults layer is skipped, `auto`.
- Auto order MUST be: (1) external + any non-clear override at agent/inline → `declared`; (2) external + no explicit override + `cli=qodercli` → `qoder-settings`; (3) native/virtual + qoder host → `qoder-settings`; (4) otherwise `none` with a warning.
- The "explicit override" set for (1) is exactly `model, reasoning_effort, context_window, extra_flags, log_dir` set to non-clear values at agent/inline; defaults and `quantification.method` do not count.
- Host detection order: `--host-cli` → `SPECKIT_HOST_CLI` → `exec-quant.collect_agent()` (when `/proc` is available) → `unknown`. `unknown` is not qoder and yields `none` + warning.
- Explicit `declared` requires effective model + reasoning_effort + context_window; missing any → exit 2, no downgrade.
- Explicit `qoder-settings` requires qoder support (external qodercli, or native/virtual with qoder host); otherwise exit 2, no downgrade.
- A method outside the selected CLI's `quantification_methods` MUST be rejected (exit 2).
- Consequence (documented adjudication): because C-EC-08 rejects explicit model/effort/context on claude, `declared` on claude is unreachable and always exits 2 (missing values or rejected values). The matrix still registers it for a future flag verification. SC-006's zero-leak goal is therefore tested on two paths: `claude + none` positive resolution (effective config/cli_args/record contain zero qoder defaults) and `claude + declared` rejection (error surface contains zero qoder defaults).

## C-EC-10 `cli_args`

- Only `mode=external` produces CLI arguments; native/virtual MUST produce `[]`.
- Order MUST be `--model <v>` (if present), `--reasoning-effort <v>` (if present), `--context-window <v>` (if present), then the `shlex.split` tokens of `extra_flags` (if present).
- With a defaults-only fixture whose defaults layer declares `mode: external` and `cli: qodercli`, `model=DeepSeek-Flash`, `reasoning_effort=max`, `context_window=1000000` (no agent config, no inline overrides), the list MUST equal `["--model", "DeepSeek-Flash", "--reasoning-effort", "max", "--context-window", "1000000"]` (STR-013 verbatim when joined by spaces).

## C-EC-11 `config_id`

- `config_id` MUST be `hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()[:16]`.
- `canonical_json` MUST be `json.dumps(effective, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`.
- `effective` MUST contain exactly the eight keys `mode, cli, model, reasoning_effort, context_window, extra_flags, log_dir, quantification{requested,resolved}`; absent/cleared value fields are `null`. It MUST exclude `agent`, paths, `resolved_at`, warnings, `cli_args`.
- Repeated resolution of the same effective input MUST yield the same id; changing any effective field (including a null ↔ value transition) MUST change it.

## C-EC-12 Config snapshot

- Every successful `resolve` (including `--format json`) MUST write `<workspace>/.specify/agents/execution/logs/config-snapshots/<config_id>.json`.
- The `snapshot` output key MUST be the workspace-relative POSIX path of that file; `log_dir` in the snapshot is also workspace-relative.
- Write MUST be atomic: write a temp file in the same directory, then `os.replace`.
- Snapshot content MUST include: `kind="speckit.execution-config-snapshot"`, `schema_version=1`, `config_id`, `resolved_at` (ISO Z), `agent`, `effective`, `source_chain`, `skipped_layers`, `requires_external`, `cli_args`, `log_dir` (effective or `.specify/agents/execution/logs`).
- Recomputing the id from `snapshot.effective` MUST reproduce `snapshot.config_id`.
- A same-id re-resolve overwrites the snapshot (latest `resolved_at`); consumers MUST collect before another same-id resolve when the elapsed fallback matters.

## C-EC-13 `validate`

- `--action validate --agent <slug>` MUST parse the defaults layer + the agent config, run the same merge/capability/quantification validation as `resolve`, and MUST NOT write a snapshot.
- It MUST emit `{target, valid, errors[]}` in JSON form; invalid → exit 2. Each error names the field and the supported set/constraint.
- A missing/invalid defaults layer is an error (exit 2) with the repair path.

## C-EC-14 `list-configs`

- `--action list-configs` MUST scan `<workspace>/.specify/agents/execution/configs/*.yaml`, excluding `_defaults.yaml`, sorted by filename.
- For each file it MUST run the `validate` pipeline and report `{file, agent, valid, errors[]}`; a missing defaults layer is a top-level error (exit 2).
- Discovery MUST NOT write any file; a valid config is listed with `valid=true`; an invalid one with its errors. The command exits 0 when listing succeeds, even if entries are invalid. SC-002's "100% non-zero exit" applies to `resolve` and `validate`; `list-configs` is a discovery surface that reports invalid entries instead of aborting.

## C-EC-15 Errors & warnings

- Missing defaults, invalid YAML/schema/value/identity/capability/quantification: exit 2, stderr names the file and field(s).
- Snapshot I/O failure: exit 1.
- Auto → `none`: a warning MUST appear on stderr and in the JSON `warnings` array; resolution still succeeds.
- Skipping the defaults layer is recorded in `skipped_layers`, not as a warning (it is a normal outcome of a different CLI selection).
- No code path may silently drop an unsupported combination or substitute a built-in value for a missing layer.

## Test pins (implementation)

- `tests/contract/test_execution_config_engine.py` MUST cover C-EC-01..C-EC-15 (one test class per clause group).
- The exact `cli_args`/`config_id`/`source_chain`/`skipped_layers` assertions MUST be mechanical (literal comparisons), not snapshots of text output.
- The engine examples in `quickstart.md` are pinned by this test file; each quickstart command carries its premises per the Post-Generation Quality Gate.
