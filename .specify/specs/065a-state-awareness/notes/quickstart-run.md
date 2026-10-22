# Quickstart Run — 065a-state-awareness（T019 smoke 子集）

**Run**: 2026-10-22T04:04Z · Python 3.9.6 · HEAD `12294c0e`（修复前基线）
**Tests mode**: 用户豁免 —— 本文件只记录 smoke 与手工场景；`tests/unit/test_loop_state_engine.py`、`tests/contract/test_loop_state_contract.py` 的 pytest 运行记 `waived/not-run`，**未运行、未判绿**。
**豁免原文（用户指令，2026-10-22）**: 「用户已显式授权**忽略测试**：不要运行/修复完整 pytest 套件，不追求红转绿；只做 docs/镜像/verification/gates 与 smoke。」

## 覆盖矩阵（quickstart §1–§9）

| 场景 | 状态 | 证据 |
|------|------|------|
| §1.1 watcher 自测 | 由 T024 承接（本段 smoke 见 `verification.md` §T024） | — |
| §1.2 plan 结构门 | 由 T030 GATE-2 承接 | — |
| §1.3 镜像基线 | 由 T023 承接（写入后 `--check`） | — |
| §2 事故回放 | **smoke 已跑**（见下 §2） | 本文件 |
| §3 正常窗口 | `waived/not-run` | 未用手工夹具复现；`unwatched` 逆样本由 `--self-test` 覆盖（`unwatched-*` 用例） |
| §4 未派发 / 脊缺失 | `waived/not-run` | `--self-test` 覆盖 `not-dispatched` 与 `registry-missing-continues`；手工夹具未做 |
| §5 远端不可达 probe | **smoke 已跑**（见下 §5） | 本文件 |
| §6 probe 隔离 | **smoke 已跑**（形状 (a) 逐字消费 + 本地路径互斥） | 本文件 |
| §7 `--self-test` | **smoke 已跑**（36/36） | 本文件 |
| §8 `--out` 边界 | **smoke 已跑**（stdout 相等 + 落在 state dir 内 exit 2 且不落文件） | 本文件 |
| §9 验收映射 | 由 `verification.md` 的 SC/US5 条目承接 | — |

## §7 `--self-test`（smoke）

```
$ python3 skills/external/sdd-loop-driver/scripts/loop-state.py --self-test
...
SELF-TEST: 36 passed, 0 failed
exit 0        # 耗时约 9.2s，全程临时目录 + 一次性 git 仓，无网络
```
覆盖 `LS-18` 六类形态、`unwatched` 两分支、旧信号污染、产物齐备无哨兵、进程死无退出记录、TIMEOUT 活进程、legacy 脊、不可达证据、`not-dispatched`、Registry 缺失继续求值、probe 两形状与五条拒绝、本地路径互斥、未实现动作拒绝、确定性与 `--help` 阶梯。
**修复后复跑**：同输出 `SELF-TEST: 36 passed, 0 failed`，exit 0（见下 §就地修复）。

## 手工夹具（`/tmp/065a_smoke.py`，不属于仓库交付面）

一次性临时目录：`git init` 的临时仓库 + spec dir（`plan.md`、`data-model.md`、`contracts/plan.md`、`quickstart.md`、`feature-ref.md`）+ state dir 四件套（`pid` 指向 `2147483646` 的已死进程、`status` 为 legacy 无 `run=` 的 `exit=1 sentinel=0`、`log` 无末行哨兵、`heartbeat`）+ v1 脊（`stage_started_at=now-600`、`stage_deadline_epoch=now+3600`、`stage_base_commit=HEAD`、`attempt=1`、`retry_limit=2`）；`--watch-script` 指向不存在路径以确定性走 derived。

### §2 事故回放

```
$ python3 skills/external/sdd-loop-driver/scripts/loop-state.py --action snapshot \
    --line-id smoke-line --state-dir <state> --spec-dir <spec> --repo <repo> \
    --spine <spine> --watch-script <missing> --stage plan
exit 0
loop_state=FAILED  verdict_source=derived  recovery_action=retry  recovery_reason=salvage-not-recorded
interruptions=[artifacts-without-completion]  uncommitted_artifacts=5
```
判据对齐：`loop_state=FAILED`（status `exit=1`）、`verdict_source=derived`（watcher 不可用）、产物齐备但无末行哨兵且无完整 salvage → C-46 行 9 `retry`/`salvage-not-recorded`；`uncommitted_artifacts` 列出 5 个必需产物（含目录类 `contracts/`）。

### §5 远端不可达 probe

```
$ ... --action snapshot --line-id smoke-line --probe probe-b.json      # {"schema_version":1,"reachable":false,"reason":"ssh-255"}
exit 0
loop_state=STALLED  loop_state_reason=remote-unreachable  recovery_action=stop
evidence.evidence_source=probe  interruptions=[remote-unreachable]
```

### §6 probe 隔离

```
$ ... --action snapshot --line-id smoke-line --probe probe-a.json      # 上一场景的完整信封
exit 0
loop_state=FAILED  recovery_action=retry  evidence.evidence_source=probe
paths.state_dir=null  paths.probe=<probe-a 绝对路径>
```
本地同线 `status` 已被改写为 `exit=0 sentinel=1`，但 `loop_state` 仍为 `FAILED` —— 本地证据未混入。
互斥检查：`--probe` 与 `--state-dir` 同时给出 → `exit 2`。

### §8 `--out` 边界

```
$ ... --out /tmp/.../out.json        → exit 0，文件信封 == stdout 信封（逐键相等）
$ ... --out <state-dir>/out.json     → exit 2，且未落任何文件
```

## 就地修复（RP-1 近似错，已披露）

**现象**：§2 首跑 `uncommitted_artifacts=4`，缺目录类产物 `contracts/`；`missing_artifacts` 侧则正常输出 `contracts/`（对称性断裂）。
**根因**：`uncommitted_artifacts_of()` 以 `candidate.endswith(rel)` / `("/" + rel) in candidate` 匹配 pathspec，而 git 输出的 pathspec 条目为 `…/contracts`（无尾斜杠），与 `item["path"]="contracts/"` 恒不相等 → 目录类产物被跳过。
**纠正是唯一读法**：`contracts/stage-artifact-map.md` C-59 要求“必需产物存在但基线之后没有提交触及它 → 列入”，`STAGE_ARTIFACTS` 把 `contracts/` 声明为 plan 的必需产物，`missing_artifacts` 已用尾斜杠形态。
**改动**：`skills/external/sdd-loop-driver/scripts/loop-state.py` `uncommitted_artifacts_of()` 内将 pathspec 与产物路径两侧去尾斜杠后按边界匹配（`key == rel_key` 或 `key.endswith("/" + rel_key)`）；局部、可逆、未触及任何其它函数。
**验证**：`--self-test` 36/36 复跑仍 exit 0；§2 smoke 复跑 `uncommitted_artifacts=5`。可见测试面（`tests/unit`、`tests/contract`）按豁免未运行，故“无新增红”未经测量，不在此声称。

## 未运行项（明确记 `waived/not-run`）

- `bash scripts/bash/run-tests.sh tests/unit/test_loop_state_engine.py tests/contract/test_loop_state_contract.py -q` —— 用户豁免，未执行，**不声称全绿**。
- quickstart §3、§4 的手工夹具复现 —— 未执行，仅由 `--self-test` 的对应用例间接覆盖。
