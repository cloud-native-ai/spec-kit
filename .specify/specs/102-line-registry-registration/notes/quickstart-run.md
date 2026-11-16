# Quickstart run — S-1, S-2, S-3 (102, T016)

Executed 2026-11-16 in `/cws_data/cloud-native-ai/spec-kit` on branch
`102-line-registry-registration`, with the wrapper at `scripts/bash/line-run.sh` and its
generated mirror at `.specify/scripts/bash/line-run.sh` (T014/T015).

Scratch root: `.specify/.tmp/line-registry-registration/` only (git-ignored via
`.specify/.gitignore` line 30, `.tmp/`). The operator's own registry was never touched:
every command sets `SPECIFY_LINE_REGISTRY_DIR` to that scratch root.

```bash
SCRATCH=.specify/.tmp/line-registry-registration
REG=$SCRATCH/registry
mkdir -p "$REG"
printf '#!/usr/bin/env bash\nset -e\necho "batch start"\nsleep 2\necho "batch done"\n' > "$SCRATCH/batch.sh"
chmod +x "$SCRATCH/batch.sh"
```

## S-1 — Wrap the script (normal path)

```bash
SPECIFY_LINE_REGISTRY_DIR="$REG" \
bash scripts/bash/line-run.sh --line-id batch-apply --run-id r20261116T090000Z-a001 -- bash "$SCRATCH/batch.sh" &
# sample while the wrapper is running:
SPECIFY_LINE_REGISTRY_DIR="$REG" python3 scripts/python/status-digest.py --action digest --workspace "$PWD"
```

Digest sampled while the child was still running (rc 0):

```text
状态摘要 · 生成于 2026-11-16T10:44:29.982236Z（UTC）· 最多 20 条 · 注册目录 /cws_data/cloud-native-ai/spec-kit/.specify/.tmp/line-registry-registration/registry

执行体             所属 spec                           父边  角色  深度  在做什么  状态  已执行时间
-----------------  ----------------------------------  ----  ----  ----  --------  ----  ----------
—（无存活执行体）  batch-apply-r20261116T090000Z-a001  -     -     -     -         活跃  0 秒  efficiency=unit=/speckit.analyze elapsed=not-evaluated tokens=not-evaluated invocations=not-evaluated
```

Wrapper output: stdout `batch start` / `batch done`, stderr empty, `wrapper_rc=0`.

Entry after the run:

```text
{
  "line_id": "batch-apply-r20261116T090000Z-a001",
  "run_id": "r20261116T090000Z-a001",
  "state": "closed",
  "last_event": "completed",
  "project_dir": "/cws_data/cloud-native-ai/spec-kit",
  "repo_root": "/cws_data/cloud-native-ai/spec-kit",
  "run_history": [
    {
      "ended_at": "2026-11-16T10:44:31Z",
      "outcome": "completed",
      "run_id": "r20261116T090000Z-a001",
      "started_at": "2026-11-16T10:44:29Z"
    }
  ]
}
```

Digest after close: `nothing-running`, rc 3 (the engine's existing empty-set rendering; the
closed entry is hidden by the digest's own rule).

## S-2 — Failure path

```bash
SPECIFY_LINE_REGISTRY_DIR="$REG" \
bash scripts/bash/line-run.sh --line-id demo-fail --run-id r20261116T090000Z-a002 -- bash -c 'exit 7'
```

`wrapper_rc=7`; entry:

```text
{
  "line_id": "demo-fail-r20261116T090000Z-a002",
  "state": "closed",
  "last_event": "failed",
  "run_history": [
    {
      "ended_at": "2026-11-16T10:44:40Z",
      "outcome": "failed",
      "run_id": "r20261116T090000Z-a002",
      "started_at": "2026-11-16T10:44:40Z"
    }
  ]
}
```

## S-3 — Wrapper killed (residue stays visible)

```bash
SPECIFY_LINE_REGISTRY_DIR="$REG" \
bash scripts/bash/line-run.sh --line-id demo-kill --run-id r20261116T090000Z-a003 -- sleep 60 &
wpid=$!            # 2578657
# wait until the entry reads active, then:
child_pid=$(pgrep -P "$wpid")   # 2578668, the `sleep 60` child
kill -9 "$wpid"                 # wrapper_killed_rc=137
```

Entry after the kill:

```text
{
  "line_id": "demo-kill-r20261116T090000Z-a003",
  "state": "active",
  "last_event": "registered"
}
```

Digest after the kill (rc 0):

```text
状态摘要 · 生成于 2026-11-16T10:44:45.521656Z（UTC）· 最多 20 条 · 注册目录 /cws_data/cloud-native-ai/spec-kit/.specify/.tmp/line-registry-registration/registry

执行体             所属 spec                         父边  角色  深度  在做什么  状态  已执行时间
-----------------  --------------------------------  ----  ----  ----  --------  ----  ----------
—（无存活执行体）  demo-kill-r20261116T090000Z-a003  -     -     -     -         活跃  0 秒  efficiency=unit=/speckit.analyze elapsed=not-evaluated tokens=not-evaluated invocations=not-evaluated
最近完成：last_completion=line_id=demo-fail-r20261116T090000Z-a002 age=5s
```

The `最近完成` line is the digest's existing rendering for the closed S-2 entry; the wrapper
added no cleanup, staleness threshold or deletion.

## Teardown

```bash
kill -9 "$child_pid" 2>/dev/null || true    # no surviving child of the wrapper was observed
rm -rf .specify/.tmp/line-registry-registration
```

`pgrep -P "$wpid"` after the child kill printed nothing ("no surviving child of wrapper"),
and the scratch root was removed with the command above after the SC readings were captured
(T017 evidence). Nothing was written outside `.specify/.tmp/`.
