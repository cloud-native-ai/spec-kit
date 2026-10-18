# Contract: `exec-quant.py` v2 & `collect-dispatch`（Feature 061, US2/US4）

**Owner (behavior)**: `scripts/python/exec-quant.py`（框架源；镜像 `.specify/scripts/python/exec-quant.py`）
**Data model**: [../data-model.md](../data-model.md) E6；V13–V15
**Consumers**: run-agent 派发后采集；`list-records` / `score` 查询；059 既有 unit 级记录

本契约只描述 **增量**；059 已实现且未在此改写的语义（run 判定采纳、端点白名单、凭据脱敏、64 KiB 封顶、非阻塞失败）继续有效，行为 owner 仍是同一引擎。

## C-EQ-01 Schema v2 & value domains

- `SCHEMA_VERSION` MUST be `2`；两种动作写出的新记录都带 `schema_version: 2`。
- `ACTIONS` closed set MUST become `collect / list-records / score / collect-dispatch` (both the `ACTIONS` constant and argparse `choices`).
- `PROVENANCES` MUST add `configured`: `measured / carried / user-given / configured`.
- `UNIT_TYPES` MUST add `agent`: `command / skill / custom-unit / agent`.
- `unit_id` grammar MUST add `agent:<slug>` (slug: `[a-z0-9][a-z0-9._-]*`); `agent:` units resolve to `unit_type=agent`.
- Every measurable leaf keeps the 059 law: either `not_evaluated` or a `{value, provenance}` object; `config` group leaves are plain values or `not_evaluated` (they are identity/declaration fields, not measured leaves).

## C-EQ-02 `collect` (unit records) under v2

- `collect` MUST write v2 records for `command / skill / custom-unit`.
- Each record MUST gain a `config` group with all 11 leaves set to `not_evaluated`, and `quality.exit_code = not_evaluated`.
- `collect` MUST reject `agent:` units with exit 2 (usage error): agent records are written only by `collect-dispatch`.
- All 059 behavior (run-id resolution, storage bootstrap, duplicate check, masking, cap, append-only) MUST remain unchanged.

## C-EQ-03 `collect-dispatch` — input contract

Required arguments:

- `--action collect-dispatch`
- `--unit-id agent:<slug>`
- `--run-id <dispatch-label>` (exactly the label used by `dispatch.sh`; the triplet files are `<log-dir>/<label>.{jsonl,live.log,status}`)
- `--snapshot <path>` (the snapshot written by `resolve`; a workspace-relative path is resolved against `--workspace-root`)
- `--config-id <id>` (the `config_id` returned by the same resolve; required — it is the "current resolution" side of FR-012's snapshot check)

Optional: `--workspace-root`, `--format text|json`, `--unit-type agent` (if provided, it must agree).

Validation order:

1. Unit id grammar + `agent:` form; a non-agent unit → exit 2.
2. `--run-id`, `--snapshot`, and `--config-id` present → otherwise exit 2.
3. Snapshot readable, JSON object, `kind=speckit.execution-config-snapshot`, `schema_version=1`, `effective` object → otherwise exit 1 (`ExecQuantError`), no record.
4. Recompute `sha256(canonical_json(snapshot.effective))[:16]`; it MUST equal `snapshot.config_id` and MUST equal the required `--config-id`. Any mismatch → exit 1, no record, reason printed (non-blocking, append-only storage untouched).
5. Bootstrap storage; acquire the store lock; check `(unit_id, run_id)`; on duplicate print the duplicate line and return 0 without a second append.

## C-EQ-04 `config` group (exactly 11 fields)

`config_id / source_chain / method_requested / method_resolved / mode / cli / model / reasoning_effort / context_window / extra_flags / snapshot`

- Values come from the snapshot: `config_id`, `source_chain`, `quantification.{requested,resolved}`, `effective.{mode,cli,model,reasoning_effort,context_window,extra_flags}`, and the snapshot path string.
- A null effective value MUST land as `not_evaluated` (never null/empty string/missing key); a null in `source_chain` MUST NOT occur (inline/derived entries omit `path`).
- No field may be added or renamed.

## C-EQ-05 `llm` group by resolved method

- `declared`: `model` / `reasoning_effort` / `context_window` MUST echo the effective values as `{value, provenance:"configured"}`; `config_source` MUST be `{value:"execution-config:<config_id>", provenance:"configured"}`; `endpoint_candidates` and `connection_evidence` MUST be `not_evaluated`.
- `qoder-settings`: the engine MUST reuse the qoder settings reader extracted from 059's `collect_llm()` (same file `~/.qoder/settings.json`, same `model.name` / `model.preferences[<name>].contextWindow` / `reasoning.effort` mapping); present values are `measured`; a missing/unreadable file leaves them `not_evaluated`. `config_source` is the settings path with `measured` when the file was read. `endpoint_candidates` / `connection_evidence` remain `not_evaluated` (no child-process evidence at collect time).
- `none`: all six `llm` fields MUST be `not_evaluated`.

## C-EQ-06 `quality` group

- `exit_code`: from `<log-dir>/<label>.status` (last `exit=<int>` occurrence). Present → `{value:int, provenance:"measured"}`; absent/unparseable → `not_evaluated`.
- `errors`: exit code 0 → `[]`; non-zero → exactly one `{"source":"dispatch.exit_code","count":1}` (059's exact key shape; the code value lives in `quality.exit_code`); no status → `not_evaluated`.
- `elapsed_ms`: scan `<log-dir>/<label>.jsonl` as NDJSON; for each JSON object, recursively collect integer `duration_ms` values; the **last** occurrence in file order wins → `{value, provenance:"measured"}`. If none, use `status_mtime − snapshot.resolved_at` when both are parseable and the difference is non-negative; else `not_evaluated`.
- `tokens`: within a single JSON object (file order, last such object wins), both `input_tokens` and `output_tokens` MUST exist as integers; then `{value: input+output, provenance:"measured"}`; otherwise `not_evaluated`. No guessing of event shape or ordering beyond this key search.
- `satisfaction`: `not_evaluated`.

`qualification` remains a **top-level** record field (not inside `quality`) and MUST be `not_evaluated` for agent records.

## C-EQ-07 Idempotency & concurrency

- Idempotency key MUST be `(unit_id, run_id)`.
- Duplicate check and append MUST happen under one exclusive POSIX `fcntl.flock` on `<store>/records.jsonl.lock` (the lock file is created in the store; it is not a record).
- A repeated call MUST print a duplicate notice, return 0, and leave `records.jsonl` byte-identical.
- On platforms without `fcntl`, the engine MUST document the degraded check-then-append semantics in code; it MUST NOT claim atomicity it does not have.

## C-EQ-08 `list-records`, `score`, and v1 normalization

- `list-records` MUST accept `--unit-type agent` (choices become `command / skill / custom-unit / agent`) and `--config-id <id>`.
- `--config-id` MUST filter on `record.config.config_id`; records without a config group (v1) do not match a non-empty `--config-id`.
- v1 records MUST participate read-only through an output-only normalization: add a `config` group (all 11 leaves `not_evaluated`) and `quality.exit_code=not_evaluated`; `schema_version` stays `1`; `records.jsonl` MUST NOT be rewritten.
- `score` MUST work for `agent:` records (same precondition: an existing `(unit_id, run_id)` record); score entries remain `provenance=user-given`.
- The JSON full-schema key set gains `config`; the existing keys remain.

## C-EQ-09 Error surfaces

- Usage/input errors (bad unit id/type, missing `--run-id`/`--snapshot`/`--config-id`, collect on agent unit, collect-dispatch on non-agent unit): exit 2 with the usage line.
- Snapshot integrity failures and I/O failures: exit 1 with a `exec-quant:` message; no record written.
- Whatever the failure, the engine MUST NOT raise into the caller's dispatch path (non-blocking guarantee preserved).

## C-EQ-10 Defenses unchanged

- Append-only `records.jsonl` / `scores.jsonl`.
- Credential masking (D9 patterns) applies to the whole v2 record including `config` and `llm`.
- 64 KiB per-record cap: largest string fields halved until it fits; identity fields (`kind, schema_version, unit_id, unit_type, run_id, collected_at, config.config_id`) MUST survive.
- `truncated` lists the shortened paths.
- Framework-repo state MUST NOT be written by tests (explicit `--workspace-root` in every test).

## C-EQ-11 Test pins & intentional extensions

New file `tests/contract/test_exec_quant_dispatch.py` MUST cover C-EQ-02..C-EQ-10 with fixture dispatch artifacts (`<label>.jsonl`, `<label>.status`, snapshot).

Intentional extensions in existing pins (register each in `verification.md`):

| File | Existing pin | Intentional change |
|------|--------------|--------------------|
| `tests/contract/test_exec_quant_engine.py` | `ACTIONS_CLOSED_SET` | add `collect-dispatch` |
| same | `PROVENANCE_DOMAIN` | add `configured` |
| same | `MEASURABLE_PATHS` | add `("quality","exit_code")` |
| same | `schema_version == 1` | `== 2` |
| same | list-records key set | add `config` |
| same | unit-id/type domain fixtures | add `agent:` / `agent` |
| `tests/contract/test_probe_engine_action_sets.py` | exec-quant exact action set | add `collect-dispatch` |

Existing pre-baseline failures (frozen in `notes/baseline-failed.txt`) MUST NOT be counted as regressions; the implementation MUST compare sorted nodeids and only accept the registered intentional extensions as newly passing/failing nodes.
