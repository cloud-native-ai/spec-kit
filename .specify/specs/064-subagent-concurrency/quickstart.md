# Quickstart — Feature 064（验证场景）

**Feature**: 064 Subagent 并发归属、CLI 能力档案与生命周期解耦
**Date**: 2026-10-20
**Status**: 本文件同时承担两层用途——§ A 是**本次 plan 已实跑**的基线命令与真实输出；§ B 是 implement 阶段要执行的验收场景，其中的引擎命令在 plan 时**尚不存在**，逐例标注设计前提（premise），不冒充已执行。

约定：`REG=${SPECIFY_LINE_REGISTRY_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/spec-kit/lines}`；`SKILL=skills/external/sdd-loop-driver`；所有 fixture 在临时目录/临时 git 仓库中构造，不触碰真实 registry 与真实项目。

---

## A. 本次 plan 已执行的基线命令（真实输出）

> 这些命令在 2026-10-20 的本工作树实跑，输出逐字粘贴。`sync-mirrors --check` 与 `watch-target --self-test` 在基线本就是非零，属已知漂移/平台退化，不是本特性引入。

### A1. 需求校验

```bash
python3 .specify/scripts/python/validate-requirements.py .specify/specs/064-subagent-concurrency/requirements.md
```

```text
file: .specify/specs/064-subagent-concurrency/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 351 lines, 78 definition rows, 4 shared strings
0 error(s), 0 warning(s)
```

### A2. Probe 注册表校验

```bash
python3 .specify/scripts/python/probe-utils.py --action probes --validate
```

```text
Probe registry valid: 10 classes, 113 internal + 0 external objects
```

### A3. 编译嵌入零漂移

```bash
python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check
```

```text
compile-embeds --check: 74 units, zero drift
```

### A4. 镜像基线（已知漂移，供 implement 对比）

```bash
python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver
```

```text
scope --only: skills/external/sdd-loop-driver
DIFF  .specify/skills/sdd-loop-driver/SKILL.md
DIFF  .specify/skills/sdd-loop-driver/references/dispatch-recipes.md
DIFF  .specify/skills/sdd-loop-driver/references/watch-model.md
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
```

```bash
python3 scripts/python/sync-mirrors.py --check --only shared/definitions
```

```text
scope --only: shared/definitions
DIFF  .specify/shared/definitions/agent-definitions.md
DIFF  .specify/shared/definitions/contract-clause-definitions.md
DIFF  .specify/shared/definitions/derivation-definitions.md
DIFF  .specify/shared/definitions/dogfooding-definitions.md
DIFF  .specify/shared/definitions/framework-map.md
DIFF  .specify/shared/definitions/goal-definitions.md
DIFF  .specify/shared/definitions/self-improvement-definitions.md
DIFF  .specify/shared/definitions/subagent-definitions.md
DIFF  .specify/shared/definitions/tool-definitions.md
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
```

> 判据：implement 只对 `probe-definitions.md` 与本特性编辑的技能文件负责；其它漂移保持基线。

### A5. Watcher 既有自测基线（已知 4 项平台退化）

```bash
bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test
```

```text
ok done
ok fake-done
ok anomaly
ok failed
ok anomaly-precedence
ok dead
ok running
ok timeout
ok no-signal
ok stale-heartbeat
FAIL pid-reuse — exit 10 != 13; output: WATCH label=reused verdict=RUNNING pid=alive heartbeat=na anomaly=no sentinel=no rc=na elapsed=1 reason=alive
FAIL zombie — exit 10 != 13; output: WATCH label=zombie verdict=RUNNING pid=alive heartbeat=na anomaly=no sentinel=no rc=na elapsed=1 reason=alive
ok sentinel-only
ok async-exit-ok
FAIL manifest — rc=13 out=WATCH label=m1 verdict=DONE pid=missing heartbeat=na anomaly=no sentinel=yes rc=0 elapsed=0 reason=exit-record-sentinel
WATCH label=m2 verdict=DEAD pid=dead heartbeat=na anomaly=no sentinel=no rc=na elapsed=0 reason=pid-dead
EVIDENCE label=m1 last="PLAN-DONE" status="exit=0 sentinel=1"
EVIDENCE label=m2 last="" status=""
FAIL pgrep-zero-match-trap-reproduced — expected two 0 lines, got: 0
SELF-TEST: 12 passed, 4 failed
```

> macOS 无 `/proc` 时的平台退化由 063 plan 记录；本特性只要求「新增归属自测用例通过、既有失败数不增加」。新增用例独立运行、单独计数。

---

## B. implement 阶段验收场景（引擎命令为设计目标，未在 plan 时执行）

> **逐例前提（premise）声明**：以下 `line-registry.py` 与扩展后的 `watch-target.sh` 在 plan 阶段尚不存在；命令参数名、输出 JSON 结构由 `contracts/` 定义，`line_id`/`run_id` 为示例形态（`<slug>-<UTCSTAMP>-<4hex>` / `r<UTCSTAMP>-<4hex>`），端口缺省 39000+20/线，registry 缺省 `${XDG_STATE_HOME:-$HOME/.local/state}/spec-kit/lines`。每个场景在实现后必须真实执行一次；在此之前不得引用为通过证据。对应的契约测试在第 4 列注明。

### S1. 单线兼容 + 信封（回归）

**Premise**: `TMP=$(mktemp -d)`；预先 `mkdir -p "$TMP/proj/.specify" "$TMP/reg"`；四件套（pid/status/log/heartbeat）与 `log-….meta.jsonl` 由测试 fixture 写入（S1 不启动真实 CLI）；`<line_id>`/`<run_id>` 用上文格式示例；退出码语义的 owner 是 `scripts/watch-target.sh`，本表不重列数值。

| 步骤 | 命令（设计目标） | 期望 |
|------|------------------|------|
| 1 | `SPECIFY_LINE_REGISTRY_DIR=$TMP/reg python3 $SKILL/scripts/line-registry.py --action register --line-id demo-20261020T120000Z-a1b2 --run-id r20261020T120000Z-a1b2 --project-dir $TMP/proj --repo-root $TMP/proj --state active --format json` | 生成 `$TMP/reg/<line_id>.json`，`state=active` |
| 2 | fixture 写入四件套后：`python3 $SKILL/scripts/line-registry.py --action update --line-id <line_id> --stage plan --runner-pid <pid> --runner-start-token <tok> --cli-pid <cli_pid> --cli-start-token <tok2> --format json`；再 `… --action list --active --format json` | 返回 1 条摘要；四件套路径与 PID 齐备 |
| 3 | `bash $SKILL/scripts/watch-target.sh --once --line-id <line_id> --run-id <run_id> --label <line_id> --pid-file … --status-file … --log … --sentinel PLAN-DONE --heartbeat … --meta …/log-….meta.jsonl` | 退出码与 058 基线一致（owner：watcher 代码）；`attribution=own`；哨兵仍为日志最后一行 |

对应测试：`test_line_registry_contract.py`（LR-13）、`test_line_envelope_contract.py`（EN-01/02/03/06/16）。

### S2. 双线同哨兵 + 无标识消息 + foreign 事件

**Premise**: 两条 line 注册在同一 `SPECIFY_LINE_REGISTRY_DIR`；两条阶段日志最后一行都写 `PLAN-DONE`；消息入口由 `resolve-message` 判定；`ps`/`pgrep` 以 PATH 桩替换并计数。

| 步骤 | 命令（设计目标） | 期望 |
|------|------------------|------|
| 1 | `… --action resolve-message --message "继续推进"` | `decision=clarify`，`question` 恰好 1 个，候选 2 条 |
| 2 | 同消息加 `--clarified` 且回答仍不唯一 | `decision=ambiguous-stop`，无第二个问题 |
| 3 | `… --action resolve-message --message "继续 <line_id>"` | `decision=route`，`target_line_id=<line_id>` |
| 4 | watcher 监听 L1，注入 L2 的 status/pid/meta | `attribution=foreign`；verdict 不变；L1 状态无转移 |
| 5 | 计数 PATH 桩调用 | `ps`/`pgrep` 调用次数 0 |

对应测试：`tests/integration/test_two_line_isolation.py`；契约 EN-10/EN-11/EN-14/EN-15、SC-001…003。

### S3. 同仓双写线：worktree、所有权与集成队列

**Premise**: 临时 git 仓库 + trunk `main`；两条写线 Manifest 一条重叠、一条不相交；集成者按 `integration-plan` 顺序执行；不 push。

| 步骤 | 命令（设计目标） | 期望 |
|------|------------------|------|
| 1 | 注册两条写线并提供 Manifest | 各自 `worktree_path=/…/.spec-kit/worktrees/<repo>/<line_id>`、`branch=line/<line_id>` |
| 2 | `… --action ownership-check --line-id <line> --manifest …` | 无重叠线 `decision=proceed`、`overlaps=[]`；重叠线 `decision=waiting` 且 `holder_line_id` 指向先到线，Registry 条目 `state=waiting` |
| 3 | 两线提交后 `git -C <trunk> fsck --no-dangling` | 无错误；两条提交图完整 |
| 4 | `… --action integration-enqueue --line-id L1 --at …`（两线） | — |
| 5 | `… --action integration-plan --format json` | 同层按 `(ready_for_merge_at, line_id)`；依赖先行；重复执行输出逐字相同 |
| 6 | 集成执行 + `… --action archive-runtime …` | 运行时记录只归档一次、冲突保留双方；`sync-mirrors`/`regen-command-copies` 各执行一次 |
| 7 | 合并成功后 `git worktree remove <wt>`（无 `--force`） | worktree 移除；未合并/uncommitted 线保留 |

对应测试：`tests/integration/test_worktree_integration_queue.py`；契约 WI-01…WI-21、SC-004/SC-010。

### S4. 主会话 kill / 重接线

**Premise**: 用 `setsid`/`nohup` 启动一个带心跳的模拟阶段进程；驱动会话为一个可被 kill 的 shell；重接线的「新会话」用新的 shell 进程代表；registry 用临时目录。

| 步骤 | 命令（设计目标） | 期望 |
|------|------------------|------|
| 1 | 派发模拟阶段（脱离启动） | runner/cli PID + token、status/log/heartbeat 写入 |
| 2 | kill 驱动 shell | 模拟子代理继续写心跳 |
| 3 | `… --action lease-acquire --line-id L --session new --pid $$` | 若旧 lease 仍「活着」→ exit 3；旧会话已死 → 允许或需显式 break |
| 4 | `… --action verify-identity --line-id L` | `identity=ok`；start token 匹配 |
| 5 | `watch-target.sh --once …` | 判定 `RUNNING` → 只恢复监听（零重派）；`DONE` → U4/U5；进程已死 → `dead` 分支 |
| 6 | 第二次启动同 `(line,stage)` | reservation 冲突 → attach 或拒绝；不产生第二个进程 |
| 7 | 远端子代理场景（ssh 断连） | `identity=remote-unreachable` → `stalled`，不判 dead、不重派 |

对应测试：`tests/integration/test_session_kill_reattach.py`；契约 LC-01…LC-18、SC-005。

### S5. CLI 档案观测 → 恰好一条反馈

**Premise**: 档案文件已按 CLP-01…CLP-07 落地；Registry/状态脊可用；`feedback-utils.py` 的 runtime-mode gate 满足（存在 `.specify/`）；观测为模拟的 U4 行为差异。

| 步骤 | 命令（设计目标） | 期望 |
|------|------------------|------|
| 1 | 查阅 `$SKILL/references/cli/qodercli.md` 的八维度 | 每维 `known/unknown`；known 带日期/版本/证据 |
| 2 | 模拟 U4：「0/负值超时语义」仍为 `unknown`，无新事实 | 不产生反馈（`--contains cli-profile:qodercli` 计数不变） |
| 3 | 模拟 U4：`-p` 行为与 `known` 不符 | 状态脊先写 `cli_observations` → 档案 provenance 更新 → 新增恰好 1 条反馈 |
| 4 | `python3 .specify/scripts/python/feedback-utils.py --action list --contains "cli-profile:qodercli"` | 步骤 2 后计数 N；步骤 3 后 N+1 |
| 5 | `python3 .specify/scripts/python/probe-utils.py --action probes --validate` | exit 0，含 `skill-sdd-loop-driver-cli-profile` |

对应测试：`tests/contract/test_sdd_loop_driver_cli_profiles.py`；契约 CLP-08…CLP-12、SC-006。

### S6. 非回归收口

**Premise**: implement 环境具备 pytest（本机不具备，见 `research.md` § 0）；既有测试套件可用。

```bash
bash scripts/bash/run-tests.sh tests/unit/test_line_registry_engine.py \
  tests/contract/test_sdd_loop_driver_skill.py \
  tests/contract/test_line_registry_contract.py \
  tests/contract/test_line_envelope_contract.py \
  tests/contract/test_workspace_isolation_contract.py \
  tests/contract/test_lifecycle_detach_reattach.py \
  tests/contract/test_sdd_loop_driver_cli_profiles.py \
  tests/integration/test_two_line_isolation.py \
  tests/integration/test_worktree_integration_queue.py \
  tests/integration/test_session_kill_reattach.py -q --names-out /tmp/064-failed.txt
```

**期望**: 本特性测试全绿；既有套件失败名单与基线 `comm -13` 差异仅为本特性新增修复（若有）；`watch-target.sh --self-test` 既有失败数不增加；三项变异演练各使至少一条测试转红（记录在 `verification.md`）。
