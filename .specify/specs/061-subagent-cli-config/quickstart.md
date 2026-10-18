# Quickstart: 子代理 CLI 配置管理与按派发量化（Feature 061）

**Feature**: 061 | **Plan**: [plan.md](plan.md) | **Contracts**: [contracts/](contracts/)
**Environment premise**: repo root = spec-kit checkout; Python 3.8+; qodercli 1.1.73 on PATH (S6 only); all fixture scenarios use a temporary workspace (`$WS`) and MUST NOT write into the framework repo's `.specify/`.

## Verification status legend

- **Route (a) — executed in the plan phase**: the command was run against the real tool on 2026-10-18 and the actual output is pasted.
- **Route (b) — pinned by contract test**: the engine is not implemented at plan time; the exact command and its expected result are pinned by the named contract test that the implementation MUST author before implementing. Each such example lists its premises; implementation MUST run the example and paste the output in `verification.md`.
- A file-level disclaimer does NOT cover an example: each unrun example carries its own status and premises.

---

## S1 — 生成面基线（route a，实跑）

Premises: repo sources and mirrors are at the 2026-10-18 checkout; no 061 edit has landed yet.

```bash
python3 scripts/python/sync-mirrors.py --check
python3 scripts/python/regen-command-copies.py --check
python3 scripts/python/probe-utils.py --action compile-embeds --check
```

Actual output (2026-10-18, truncated to the meaningful lines):

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (21 files)
ok    skills/external/ == .specify/skills/ (369 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (108 files)
ok    shared/ == .specify/shared/ (50 files)
# exit 0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
# exit 0

$ python3 scripts/python/probe-utils.py --action compile-embeds --check
compile-embeds --check: 73 units, zero drift
# exit 0
```

These are dated observations, not a runtime guarantee. The implementation MUST re-run the three commands after edits and compare against this baseline (no NEW drift).

Test baseline (route a, executed 2026-10-18; repo `.venv` lacks pytest, so the measured interpreter is recorded):

```bash
/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract tests/integration -q --no-header -p no:cacheprovider
```

Actual result: `3278 passed, 25 failed, 1 skipped in 193.94s`. The sorted failed nodeids are frozen in [notes/baseline-failed.txt](notes/baseline-failed.txt). After implementation the same command MUST be re-run; `comm -13` against the frozen list MUST be empty except the registered intentional extensions.

---

## S2 — 默认层解析与 `cli_args` 逐字相等（route b）

**Status**: not executed in the plan phase — `scripts/python/execution-config.py` is not implemented yet. Pinned by `tests/contract/test_execution_config_engine.py::TestResolveMerge::test_defaults_only_explicit_qodercli` (to be authored before implementation). Implementation MUST run this scenario and paste the output.

**Premises**: the engine exists at the locked path; the defaults fixture declares `mode: external` and `cli: qodercli` in addition to the template's `model=DeepSeek-Flash`, `reasoning_effort=max`, `context_window=1000000`; there is no agent config and no inline override (the defaults layer is the only configuration layer); `$WS` is a fresh temp workspace.

```bash
WS=$(mktemp -d)
mkdir -p "$WS/.specify/agents/execution/configs"
cp templates/execution-config-defaults.yaml "$WS/.specify/agents/execution/configs/_defaults.yaml"
printf 'mode: external\n' >> "$WS/.specify/agents/execution/configs/_defaults.yaml"
python3 scripts/python/execution-config.py --action resolve \
  --agent sample-agent \
  --workspace-root "$WS" --format json
python3 scripts/python/execution-config.py --action resolve \
  --agent sample-agent \
  --workspace-root "$WS" --format json | python3 -c 'import json,sys; print(json.load(sys.stdin)["config_id"])'
rm -rf "$WS"
```

Expected (contract): `cli_args == ["--model","DeepSeek-Flash","--reasoning-effort","max","--context-window","1000000"]`; the two `config_id` values are identical; `source_chain` covers `mode/cli/model/reasoning_effort/context_window/quantification.method` and every entry points at the defaults layer; `requires_external == true`; a snapshot exists at `.specify/agents/execution/logs/config-snapshots/<config_id>.json`.

---

## S3 — 覆盖、清除与拒收（route b）

**Status**: not executed — engine not implemented. Pinned by `tests/contract/test_execution_config_engine.py::TestResolveMerge`, `::TestIdentityConflict`, `::TestCapabilityMatrix`, `::TestYamlSubset`, `::TestValidation` (clauses C-EC-03..C-EC-10, V1–V12). Implementation MUST run each command and paste exit codes.

**Premises**: same temp-workspace setup as S2; the agent config file is optional; `auto`/`""` are clear sentinels only for the five value fields; error exits are `2`.

```bash
WS=$(mktemp -d)
mkdir -p "$WS/.specify/agents/execution/configs"
cp templates/execution-config-defaults.yaml "$WS/.specify/agents/execution/configs/_defaults.yaml"

# 1) agent config overrides model; inline overrides reasoning_effort
cat > "$WS/.specify/agents/execution/configs/sample-agent.yaml" <<'YAML'
cli: qodercli
model: override-model
YAML
python3 scripts/python/execution-config.py --action resolve \
  --agent sample-agent --reasoning-effort high \
  --workspace-root "$WS" --format json

# 2) clear sentinel removes a lower-layer value
cat > "$WS/.specify/agents/execution/configs/sample-agent.yaml" <<'YAML'
mode: external
cli: qodercli
model: ""
YAML
python3 scripts/python/execution-config.py --action resolve \
  --agent sample-agent --workspace-root "$WS" --format json

# 3) cross-layer identity conflict -> exit 2 listing "cli"
cat > "$WS/.specify/agents/execution/configs/sample-agent.yaml" <<'YAML'
cli: claude
YAML
python3 scripts/python/execution-config.py --action resolve \
  --agent sample-agent --cli qodercli --workspace-root "$WS" --format json
echo "exit=$?"

# 4) claude + explicit flags -> exit 2 with field + supported set
cat > "$WS/.specify/agents/execution/configs/sample-agent.yaml" <<'YAML'
cli: claude
mode: external
model: some-model
YAML
python3 scripts/python/execution-config.py --action resolve \
  --agent sample-agent --workspace-root "$WS" --format json
echo "exit=$?"

# 5) codex external -> exit 2
cat > "$WS/.specify/agents/execution/configs/sample-agent.yaml" <<'YAML'
cli: codex
mode: external
YAML
python3 scripts/python/execution-config.py --action resolve \
  --agent sample-agent --workspace-root "$WS" --format json
echo "exit=$?"

# 6) missing defaults -> exit 2 naming the path and "specify init"
rm "$WS/.specify/agents/execution/configs/_defaults.yaml"
python3 scripts/python/execution-config.py --action resolve \
  --agent sample-agent --workspace-root "$WS" --format json
echo "exit=$?"
rm -rf "$WS"
```

Expected (contract): (1) effective model=`override-model`, effort=`high`, `source_chain` shows `agent-config` for model and `inline` for effort, mode derives `external` from the override; (2) `model` is `null` in effective config and no model flag is generated; (3) exit 2 naming `cli`; (4) exit 2 naming `model` and the supported set; (5) exit 2 naming the unverified external capability; (6) exit 2 naming the defaults path and `specify init`.

---

## S4 — `collect-dispatch` 落一条 `agent:<slug>` 记录（route b）

**Status**: not executed — `exec-quant.py` v2 is not implemented yet. Pinned by `tests/contract/test_exec_quant_dispatch.py` (C-EQ-02..C-EQ-10). Implementation MUST run this scenario and paste the output.

**Premises**: `resolve` already wrote a snapshot under `$WS/.specify/agents/execution/logs/config-snapshots/`; the fixture reuses the defaults layer and an explicit qodercli choice; the dispatch label is `demo-label`; the status/jsonl shapes are fixtures, not claims about qoder's real stream.

```bash
WS=$(mktemp -d)
mkdir -p "$WS/.specify/agents/execution/configs" \
         "$WS/.specify/agents/execution/logs"
cp templates/execution-config-defaults.yaml "$WS/.specify/agents/execution/configs/_defaults.yaml"
SNAP_JSON=$(python3 scripts/python/execution-config.py --action resolve \
  --agent sample-agent --mode external --cli qodercli --workspace-root "$WS" --format json)
SNAP=$(printf '%s' "$SNAP_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["snapshot"])')
CID=$(printf '%s' "$SNAP_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["config_id"])')

printf '%s\n' 'demo-label exit=0' > "$WS/.specify/agents/execution/logs/demo-label.status"
printf '%s\n' '{"type":"result","duration_ms":1234,"usage":{"input_tokens":10,"output_tokens":5}}' \
  > "$WS/.specify/agents/execution/logs/demo-label.jsonl"

python3 scripts/python/exec-quant.py --action collect-dispatch \
  --unit-id agent:sample-agent --run-id demo-label \
  --snapshot "$WS/$SNAP" --config-id "$CID" \
  --workspace-root "$WS"
# repeat the same call -> no second row
python3 scripts/python/exec-quant.py --action collect-dispatch \
  --unit-id agent:sample-agent --run-id demo-label \
  --snapshot "$WS/$SNAP" --config-id "$CID" \
  --workspace-root "$WS"
python3 scripts/python/exec-quant.py --action list-records \
  --unit-type agent --config-id "$CID" --workspace-root "$WS" --format json
python3 scripts/python/exec-quant.py --action score \
  --unit-id agent:sample-agent --run-id demo-label --score 4 \
  --workspace-root "$WS"
wc -l < "$WS/.specify/memory/exec-quant/records.jsonl"
rm -rf "$WS"
```

Expected (contract): exactly one record in `records.jsonl`; `unit_type=agent`, `run_id=demo-label`, `config` has the 11 fields with `config_id=<CID>`; `method_resolved=qoder-settings` (external, no explicit overrides, qodercli); `quality.exit_code={"value":0,"provenance":"measured"}`, `errors=[]`, `tokens={"value":15,"provenance":"measured"}`, `elapsed_ms={"value":1234,"provenance":"measured"}`; `list-records --unit-type agent --config-id` returns it; `score` appends one user-given entry.

---

## S5 — `specify init` 播种默认层（route b）

**Status**: not executed — seeding is not implemented yet. Pinned by `tests/integration/test_init_execution_config.py`. Implementation MUST run it and paste the output.

**Premises**: the test harness calls `ensure_agent_layer_dirs(tmp_path, defaults_source=repo/templates/execution-config-defaults.yaml)` because a source checkout has no packaged `MODULE_DIR/templates`; an installed `specify` resolves the packaged template automatically; `_defaults.yaml` is tracked, only `logs/` is gitignored; `PYTHONPATH=src` makes the in-repo package importable.

```bash
WS=$(mktemp -d)
PYTHONPATH=src python3 - "$WS" "$PWD/templates/execution-config-defaults.yaml" <<'PY'
import sys
from pathlib import Path
from specify_cli import ensure_agent_layer_dirs

ws = Path(sys.argv[1])
src = Path(sys.argv[2])
ensure_agent_layer_dirs(ws, defaults_source=src)
target = ws / ".specify/agents/execution/configs/_defaults.yaml"
print("seeded:", target.is_file(), target.read_bytes() == src.read_bytes())
before = target.read_bytes()
target.write_text("# user edit\n")
ensure_agent_layer_dirs(ws, defaults_source=src)
print("preserved:", target.read_text() == "# user edit\n")
PY
rm -rf "$WS"
```

Expected (contract): `seeded: True True`; `preserved: True`. A second init on an untouched file leaves it byte-identical; an explicitly supplied missing source raises.

---

## S6 — 一次极短 qodercli 实派（optional, explicit authorization only）

**Status**: NOT executed and MUST NOT run without explicit user authorization for a real external dispatch. This is a conditional runbook, not a verified executable example; no expected output is claimed here. When authorized, the operator follows the shape below and records the actual result in `verification.md`.

**Premises**: qodercli 1.1.73 on PATH; a prompt file exists; the project has a seeded defaults layer; `dispatch.sh` is available; the label is unique for the run.

**Runbook** (prose, authorization-gated):

1. In a temp workspace, seed `_defaults.yaml` from the template and write a one-line prompt file.
2. Resolve with `--mode external --cli qodercli`; keep the returned `cli_args`, `snapshot`, `config_id`, and the effective `log_dir`.
3. Invoke `dispatch.sh <label> <ws> <prompt-file> -- <cli_args...>` with `DISPATCH_CLI=qodercli` and `DISPATCH_LOG_DIR=<absolute log dir>`.
4. Invoke `collect-dispatch --unit-id agent:sample-agent --run-id <label> --snapshot <snapshot> --config-id <config_id> --workspace-root <ws>`.
5. Verify the triplet files exist, the flags were accepted (exit 0), and exactly one agent record landed; unknown stream fields must degrade to `not_evaluated` rather than failing the collection.
6. Remove the temp workspace.
