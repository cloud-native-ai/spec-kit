# Quickstart: 状态感知快照（Feature 065 / Slice 065a）

**Plan**: [`plan.md`](./plan.md) · **Contracts**: [`contracts/`](./contracts/)
本文件给出 065a 的调用形态与可验收场景。**凡标注 “Planned example” 的命令在 plan 阶段尚不可执行**——引擎在 implement 阶段才落地；每条均列出其所依赖的前提，供 `/speckit.implement` 重新测量，而不是继承。

## 1. 基线检查（可执行性逐条标注）

### 1.1 watcher 判定零回归

```bash
bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test
```

**Expected**: 退出码 `0`，汇总行为 `SELF-TEST: N passed, 0 failed`。
**Measured at plan time (2026-10-21)**: `SELF-TEST: 38 passed, 0 failed`，exit 0。本切片 MUST NOT 改动该脚本；该命令在实现前后应给出相同的 `0 failed`。

### 1.2 plan 阶段结构门

```bash
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py \
  --spec-dir .specify/specs/065a-state-awareness --stage plan --repo .
```

**Expected**: 退出码 `0`，且 stderr 汇总为 `decision=pass`。`missing-path` advisory 可因“引擎与测试尚未创建”而存在，不构成阻挡；`error` 必须为 0。

### 1.3 镜像基线（实现阶段首次编辑前必做）

```bash
python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver
```

**未在 plan 阶段执行**：并发隔离策略拒绝调用该路径上的脚本，因此没有本次实测值。实现阶段 MUST 在首次编辑前运行并记录基线；由于工作树已含外部同步产生的驱动技能改动，判据是**相对该基线无新增漂移**，不是绝对 exit 0。

## 2. Planned example：事故回放（SC-001）

**Premises**（实现阶段 MUST 重新测量，不得继承）：
- 引擎位于 `skills/external/sdd-loop-driver/scripts/loop-state.py`，参数面如 `LS-04`。
- 夹具目录：state dir 含 `pid-<line>-plan`（指向已死进程、`pid=... start=... at=... line=<line> stage=plan event=pid`）、`status-<line>-plan`（`exit=1 at=<epoch> sentinel=0 line=<line> stage=plan event=status`，与现行 `stage-runner.sh` 一致，不含 `run=`）、`log-<line>-plan.log`（末行非 `ANOMALY:`、无 `PLAN-DONE`）、`heartbeat-<line>-plan.log`；**无** watchbeat。
- 状态脊含 `stage_base_commit`、`attempt=1` 与可读的 `stage_deadline_epoch`；已试次数未达 `retry_limit`（上限归 `references/stage-prompts.md` § Stall Handling）。
- spec dir 含 `plan.md`、`data-model.md`、`contracts/plan.md`、`quickstart.md`、`feature-ref.md`；repo 为该目录所在的临时 git 仓库，`stage_base_commit` 之后的提交不触及这些文件。
- `--watch-script` 指向不存在的路径，用于确定性地走 derived 映射；可调用 watcher 时同一夹具应得到 `verdict_source=watcher` 与相同的 `loop_state=FAILED`。无 `run=` 的 status 属于 `legacy` 归属形态（`LS-14`）。

```bash
python3 skills/external/sdd-loop-driver/scripts/loop-state.py \
  --action snapshot --line-id <line> \
  --state-dir <state-dir> --spec-dir <spec-dir> --repo <repo> --stage plan \
  --spine <spine> --watch-script <missing>
```

**Expected envelope**（字段级断言，不写不存在的数值）：
- `schema_version=1`，`loop_state=FAILED`，`verdict_source=derived`（本夹具显式使 watcher 不可用）。
- `interruptions[]` 含 `artifacts-without-completion`（产物齐备、无哨兵）。
- `recovery_action=retry`（产物齐备、无哨兵、无 salvage 记录）；若夹具记录完整 salvage，则允许 `resume`。
- `uncommitted_artifacts[]` 列出全部存在但基线后未提交的必需产物。
- 退出码 `0`。

**为什么这里不是 `resume`**：A-6 的 salvage 门要求驱动者显式记录独立校验；未记录时一律 `retry`。

## 3. Planned example：正常运行中的线

**Premises**：以 §2 夹具为底，**移除 status 与终止日志**（只保留存活 pid、新鲜 heartbeat、匹配的 watchbeat，以及可读 `stage_started_at`）；`attempt=1` 且未达上限；`--watch-script` 指向不存在的路径或可调用的 watcher 均可。

```bash
python3 skills/external/sdd-loop-driver/scripts/loop-state.py \
  --action snapshot --line-id <line> --state-dir <state-dir> \
  --spec-dir <spec-dir> --repo <repo> --stage plan --spine <spine>
```

**Expected**: `loop_state=RUNNING`；`interruptions[]` 不含 `unwatched`；`recovery_action=watch`。若 watcher 判定可得，`verdict_source=watcher` 且 `loop_state` 等于 watcher 字面量。

## 4. Planned example：未派发的线

**Premises**：Registry 条目存在但无 `stage`；state dir 与 spec dir 均无该线的四件套、哨兵与提交证据；状态脊缺失或无 `stage_started_at`；调用方不提供 `--stage`。

```bash
python3 skills/external/sdd-loop-driver/scripts/loop-state.py \
  --action snapshot --line-id <line> --state-dir <state-dir> --repo <repo>
```

**Expected**: `loop_state=UNKNOWN`、`loop_state_reason=not-dispatched`、`recovery_action=none`；MUST NOT 判 `NO_SIGNAL`。若 Registry 已有 `stage` 而状态脊缺失，则同一命令 MUST 改为 `UNKNOWN` + `recovery_action=stop`（证据缺口）。

## 5. Planned example：远端不可达 probe

**Premises**：probe 文件为合法 JSON `{"schema_version": 1, "reachable": false, "reason": "ssh-255"}`；调用时不得同时提供 `--spine/--state-dir/--spec-dir/--repo/--watch-script`（同时提供 MUST exit 2 且不读取任何本地证据）；probe 模式不读取 Registry，因此 §4 的“Registry 有 stage”分支不适用于本场景。

```bash
python3 skills/external/sdd-loop-driver/scripts/loop-state.py \
  --action snapshot --line-id <line> --probe <probe.json>
```

**Expected**: `loop_state=STALLED`、`loop_state_reason=remote-unreachable`、`interruptions[]` 含 `remote-unreachable`、`recovery_action=stop`、`evidence.evidence_source=probe`；MUST NOT 判 `DEAD`。退出码 `0`。

## 6. Planned example：probe 快照整份消费

**Premises**：probe 文件为形状 (a)——`schema_version=1` + `watch_verdict` + `evidence`（与快照同信封）；本地 state dir 放置与 probe 冲突的 `status`/`pid` 文件，用于证明本地证据未被混入。

```bash
python3 skills/external/sdd-loop-driver/scripts/loop-state.py \
  --action snapshot --line-id <line> --probe <snapshot.json>
```

**Expected**: `evidence.evidence_source=probe`；所有取值来自 probe；本地冲突文件 MUST NOT 改变 `loop_state`/`interruptions`/`recovery_action`。probe 不可解析或 `schema_version≠1` 时退出码 `2`；与本地路径参数同时提供时同样退出码 `2`，且 MUST NOT 读取本地证据。

## 7. Planned example：自测

**Premises**：引擎可执行；`--self-test` 不接受其它参数；夹具由引擎自建临时目录，不读取本仓库的状态目录或网络。

```bash
python3 skills/external/sdd-loop-driver/scripts/loop-state.py --self-test
```

**Expected**: 逐例 `ok <case>`，末行 `SELF-TEST: N passed, 0 failed`，退出码 `0`。覆盖范围见 `LS-18`；失败时退出码 `1` 并打印 `FAIL <case> — <detail>`。

## 8. Planned example：`--out` 边界

**Premises**：`--out` 目标位于 state dir 或 repo 工作树之外。

```bash
python3 skills/external/sdd-loop-driver/scripts/loop-state.py \
  --action snapshot --line-id <line> --state-dir <state-dir> \
  --spec-dir <spec-dir> --repo <repo> --stage plan --spine <spine> \
  --out /tmp/loop-state-<line>.json
```

**Expected**: 文件内容与 stdout 信封逐字相同（原子写入）；目标与其父目录 MUST 先 `realpath`/`Path.resolve` 规范化，再与解析后的 state dir / repo 比较；目标（含相对路径或经 symlink 指向 state dir / repo）若落在两者内，退出码 `2` 且不写任何文件。除 `--out` 外，快照 MUST NOT 改变任何 mtime 或工作树状态。

## 9. 验收映射

| 场景 | 覆盖 |
|------|------|
| §2 事故回放 | SC-001、US1-4、`artifacts-without-completion`、salvage 门 |
| §3 正常窗口 | US1-2、SC-003、`unwatched` 逆样本 |
| §4 未派发 / 脊缺失 | A-14、Q4 判据 |
| §5 远端不可达 | Edge Cases「远端 ssh 不可达」、SC-003（不得判 `DEAD`） |
| §6 probe 隔离 | FR-002、Q3 |
| §7 自测 | FR-012（六类形态与快照检查的自测覆盖） |
| §8 只读边界 | SA-4、SC-002 |
| §1.1 watcher 基线 | SC-004、US5-1 |
| §1.3 镜像基线 | SC-005（源/镜像无新增漂移） |
| 变异演练（命令与转红用例见 `plan.md` §Testing Strategy，本文件不重复给出） | SC-006 |
