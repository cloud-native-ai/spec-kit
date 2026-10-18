# Quickstart run evidence — Feature 061

All scenarios ran on 2026-10-18 from the repository root
(`/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`) with temp workspaces (`mktemp -d`);
the framework repository's `.specify/` was never a fixture target. S1–S5 executed; S6 is
authorization-gated and was **not** executed.

## S1 — 生成面基线（executed）

Commands and actual output at implementation start (before any 061 edit):

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (21 files)
ok    skills/external/ == .specify/skills/ (369 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (108 files)
ok    shared/ == .specify/shared/ (51 files)
# exit 0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
# exit 0

$ python3 scripts/python/probe-utils.py --action compile-embeds --check
compile-embeds --check: 73 units, zero drift
# exit 0
```

Full pre-change record: `notes/pre-change-measurements.md`.

## S2 — 默认层解析与 `cli_args` 逐字相等（executed）

```bash
WS=$(mktemp -d)
mkdir -p "$WS/.specify/agents/execution/configs"
cp templates/execution-config-defaults.yaml "$WS/.specify/agents/execution/configs/_defaults.yaml"
printf 'mode: external\n' >> "$WS/.specify/agents/execution/configs/_defaults.yaml"
python3 scripts/python/execution-config.py --action resolve \
  --agent sample-agent --workspace-root "$WS" --format json
```

Actual output (exit 0):

```json
{
  "agent": "sample-agent",
  "config_id": "72ae1cc218e8aca8",
  "effective": {
    "mode": "external",
    "cli": "qodercli",
    "model": "DeepSeek-Flash",
    "reasoning_effort": "max",
    "context_window": 1000000,
    "extra_flags": null,
    "log_dir": null,
    "quantification": {"requested": "auto", "resolved": "qoder-settings"}
  },
  "source_chain": {
    "model": {"layer": "defaults", "path": ".specify/agents/execution/configs/_defaults.yaml"},
    "reasoning_effort": {"layer": "defaults", "path": ".specify/agents/execution/configs/_defaults.yaml"},
    "context_window": {"layer": "defaults", "path": ".specify/agents/execution/configs/_defaults.yaml"},
    "mode": {"layer": "defaults", "path": ".specify/agents/execution/configs/_defaults.yaml"},
    "cli": {"layer": "defaults", "path": ".specify/agents/execution/configs/_defaults.yaml"},
    "quantification.method": {"layer": "defaults", "path": ".specify/agents/execution/configs/_defaults.yaml"}
  },
  "skipped_layers": [],
  "cli_args": ["--model", "DeepSeek-Flash", "--reasoning-effort", "max", "--context-window", "1000000"],
  "requires_external": true,
  "quantification": {"requested": "auto", "resolved": "qoder-settings"},
  "warnings": [],
  "snapshot": ".specify/agents/execution/logs/config-snapshots/72ae1cc218e8aca8.json"
}
```

Repeated resolution: `config_id_1=72ae1cc218e8aca8`, `config_id_2=72ae1cc218e8aca8`,
`stable=yes`; snapshot exists at the returned workspace-relative path. STR-013 is matched
verbatim by `cli_args`.

## S3 — 覆盖、清除与拒收（executed）

Same temp-workspace setup; each case's actual exit code:

| Case | Command | Actual result |
|------|---------|---------------|
| 1 agent overrides model, inline overrides reasoning_effort | `resolve --agent sample-agent --reasoning-effort high` | exit 0; `model=override-model`, `reasoning_effort=high`; `source_chain.model.layer=agent-config`, `source_chain.reasoning_effort.layer=inline`; mode derives `external` |
| 2 clear sentinel `model: ""` | `resolve` | exit 0; `"model": null`; `source_chain` has no `model`; `cli_args` omits `--model` and stays `["--reasoning-effort","max","--context-window","1000000"]` |
| 3 cross-layer `cli` conflict | agent `cli: claude` + inline `--cli qodercli` | exit 2; `conflicting field 'cli': agent-config='claude' inline='qodercli'` |
| 4 claude + explicit model | agent `cli: claude`, `mode: external`, `model: some-model` | exit 2; `field 'model' is not supported by cli 'claude' (supported CLIs for model: qodercli)` |
| 5 codex external | agent `cli: codex`, `mode: external` | exit 2; `cli 'codex' does not support external dispatch (supported external CLIs: claude, qodercli)` |
| 6 missing defaults | remove `_defaults.yaml` | exit 2; names the absolute missing path and `specify init` / template repair |

Case 1 excerpt (actual):

```text
"model": "override-model",
"reasoning_effort": "high",
"source_chain": {
  "model": {"layer": "agent-config", "path": ".specify/agents/execution/configs/sample-agent.yaml"},
  "reasoning_effort": {"layer": "inline"},
  ...
},
"cli_args": ["--model", "override-model", "--reasoning-effort", "high", "--context-window", "1000000"]
```

## S4 — `collect-dispatch` 落一条 `agent:<slug>` 记录（executed）

Sequence: resolve → fixture `<label>.status` / `<label>.jsonl` → `collect-dispatch` twice →
`list-records --unit-type agent --config-id` → `score`.

Actual output:

```text
config_id=72ae1cc218e8aca8
snapshot=.specify/agents/execution/logs/config-snapshots/72ae1cc218e8aca8.json
$ collect-dispatch (first)
exec-quant: recorded agent:sample-agent run=demo-label config_id=72ae1cc218e8aca8 -> <ws>/.specify/memory/exec-quant/records.jsonl
exit=0
$ collect-dispatch (repeat)
exec-quant: duplicate record for (agent:sample-agent, demo-label); no second row written -> <ws>/.specify/memory/exec-quant/records.jsonl
exit=0
records_sha_before=935e4c37d9feb10b96f654142b6804f903e919599ebeeccd253fc0a20eb05d69
records_sha_after=935e4c37d9feb10b96f654142b6804f903e919599ebeeccd253fc0a20eb05d69
byte_identical=yes
$ list-records --unit-type agent --config-id
```

The listed record (actual excerpt) carries `schema_version: 2`, `unit_type: "agent"`,
`run_id: "demo-label"`, the 11-field `config` group with `config_id=72ae1cc218e8aca8` and
`method_resolved=qoder-settings`, `llm.model={"value":"dfmodel","provenance":"measured"}`
(host settings), `quality.exit_code={"value":0,"provenance":"measured"}`,
`quality.elapsed_ms={"value":1234,"provenance":"measured"}`,
`quality.tokens={"value":15,"provenance":"measured"}`, `quality.errors=[]`,
`qualification="not_evaluated"`. `row_count=1` after the repeat call; `score` appended one
`user-given` entry.

## S5 — `specify init` 播种默认层（executed）

Command shape (from `quickstart.md` § S5, `PYTHONPATH=src` makes the in-repo package
importable; `$WS` is a fresh temp directory):

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
ensure_agent_layer_dirs(ws, defaults_source=src)
print("second_init_byte_identical:", target.read_bytes() == before)
target.write_text("# user edit\n")
ensure_agent_layer_dirs(ws, defaults_source=src)
print("preserved:", target.read_text() == "# user edit\n")
missing = ws / "no-such-template.yaml"
try:
    ensure_agent_layer_dirs(ws / "ws2", defaults_source=missing)
except RuntimeError as exc:
    print("explicit_missing_raises:", True)
    print("missing_message:", str(exc))
PY
```

Actual output:

```text
seeded: True True
second_init_byte_identical: True
preserved: True
explicit_missing_raises: True
missing_message: execution-config defaults template not found: <tmp>/no-such-template.yaml
```

The packaged fallback path is covered separately by
`tests/integration/test_init_execution_config.py::test_packaged_fallback_is_used` (monkeypatched
`get_resource_path`), and the no-source/no-packaged case fabricates nothing. All six
integration tests are green:

```text
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/integration/test_init_execution_config.py -q --no-header -p no:cacheprovider
......                                                                   [100%]
6 passed in 0.17s
```

Single-owner audit of the edited schema/definition/doc surfaces (recorded in
`verification.md`): the field-level schema lives only in
`skills/internal/create-agent/references/execution-config.md`; `subagent-definitions.md` and
both docs point at it; CLI capability values appear only in the engine's
`CAPABILITY_MATRIX` and are referenced, never copied; defaults content is owned only by
`templates/execution-config-defaults.yaml`.

## S6 — 一次极短 qodercli 实派（NOT executed — authorization gate）

Not executed: no explicit authorization for a real external dispatch was given in this
unattended run, and consuming real model calls for testing is excluded by the entry
instructions. The conditional runbook stays in `quickstart.md` § S6. This is not a blocking
omission: S1–S5 plus the contract suites cover SC-001..SC-006.
