# Verification — 065a-state-awareness（Feature 065 / Slice 065a）

**Run**: 2026-10-22T04:0xZ · Python 3.9.6 · branch `065-loop-interruption-recovery`
**Slice status**: `065a slice implementation-complete with test waiver`
**Feature 065 status**: 保持 `Planned` —— 065a 只是 active slice，065b / 065c 仍排队；本文件不把 Feature 065 推进到 Implemented。
**deferred_tasks=**: none（无 `[~]` 任务；未运行的测试按豁免在任务行内与本节记 `waived/not-run`，不记为 deferred）

## Test waiver（用户显式授权，2026-10-22）

**原文**：「用户已显式授权**忽略测试**：不要运行/修复完整 pytest 套件，不追求红转绿；只做 docs/镜像/verification/gates 与 smoke。」

- **范围**：本切片 26 个测试记 `waived/not-run`（T015×18、T016×5、T018×3），另含 T019 / T020 / T021 / T024 / T026 / T027 与 GATE-3 的 pytest 部分。**实测口径**：last observed 26 failed before T015–T018 implementation (commit 35aa0192); not re-run after T015–T018; current red/green is not evaluated。
- **纪律**：未运行的测试一律记 `waived/not-run`，**不得**写 `pass` / `green`；`--self-test`、watcher 自测、镜像检查、smoke 夹具的证据按 `smoke-evidence` 记录，与测试面区分。
- **不受豁免的部分**：确定性门（`validate-tasks.py`、`pre-analyze-check.py`、`account-clause-coverage.py`、`sync-mirrors.py --check`）、`watch-target.sh --self-test`、`loop-state.py --self-test` 与手工 smoke 全部实跑。

## T024 — 兼容性回归（US5 A1–A3 的测量面）

| 命令 | 结果 | 状态 |
|------|------|------|
| `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` | `SELF-TEST: 38 passed, 0 failed`，exit 0 | **smoke-evidence**（与 plan 期基线 38/0 逐字相同，判定与退出码零差异） |
| `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` | `ok skills/external/ == .specify/skills/ (28 files)`，exit 0 | **smoke-evidence**（基线 26 files → 28 files，新增两份即 `references/state-awareness.md` 与 `scripts/loop-state.py`；无新增漂移） |
| `bash scripts/bash/run-tests.sh tests/unit/test_line_registry_engine.py tests/contract/test_sdd_loop_driver_skill.py -q` | 未执行 | `waived/not-run` |
| 名字级比较（相对 T001 基线，形态 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs） | 无可比较对象（本轮无 pytest 运行） | `waived/not-run` |

## T025 — US5 兼容性验收

- **US5-A1**: watcher 判定与退出码零差异 —— **smoke-evidence**。命令 `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` → `SELF-TEST: 38 passed, 0 failed`，exit 0，与 `tasks.md` § Environment Prerequisites 记录的基线（38 passed / 0 failed @ 2026-10-21）逐字一致；`git status --short skills/external/sdd-loop-driver/scripts/watch-target.sh` 为空、`git diff --stat` 对该文件无输出 → 脚本本体未被本切片改动。
- **US5-A2**: 四件套与 Registry 旧条目可读（含无 `run=` 信封）—— **smoke-evidence**。临时夹具（`/tmp`，非仓库交付面）写入 legacy Registry 条目（`schema_version=1`，**无 `run_id`**，`stage=tasks`）与无 `run=` 的四件套：`registry.status=present`、`registry.stage=tasks`、`paths.state_dir` 由 Registry 运行目录解析成功；`evidence.status.status=present`、`attribution=legacy`、`stale_signals=0`（旧信封未被误判 stale），exit 0。未请求 `--stage` 时 `stage` 仍取 Registry 的 `tasks`，映射可建立。
- **US5-A3**: 源/镜像字节一致与漂移为零 —— **smoke-evidence**。`sync-mirrors.py --write --only …` 报告 `MISS references/state-awareness.md`、`DIFF SKILL.md`、`DIFF scripts/loop-state.py`，`sync … (3 files)`；随后 `--check` → `ok … (28 files)` exit 0；三对文件 `cmp -s` 全部 IDENTICAL，sha256 逐对相等（`loop-state.py b472e52d…`、`state-awareness.md 910e4fe2…`、`SKILL.md 5216a08f…`）。镜像由生成器产出，未手改 `.specify/skills/sdd-loop-driver/`。
- **US5-A4**: 既有 `/speckit.*` 命令三段骨架 / 哨兵字面量 / 确认门 / no-push 策略无改动 —— **范围审计证据**（见 §T029）。`git status --short` 与 `git diff --stat` 显示命令模板（`templates/commands/`、`.specify/templates/`）零改动；本切片未改哨兵字面量（`<STAGE>-DONE`）与 watcher 判定码 10–16；未执行 push / merge / kill / 删除。

## T026 — SC-006 变异演练

`waived/not-run`。用户豁免明令不运行 pytest，而本任务的两处变异（移除 `unwatched` 检测分支、移除 C-48 salvage 完整记录门）唯一的读数就是「对应用例是否转红」，无法在无 pytest 的情况下测量。**未伪造计数**。因此：

- 移除点 1：`skills/external/sdd-loop-driver/scripts/loop-state.py` 的 `unwatched` 检测分支 —— 未移除、未测量，`waived/not-run`。
- 移除点 2：同文件 C-48 / `IA-16` salvage 完整记录门 —— 未移除、未测量，`waived/not-run`。
- 备份/恢复与 sha256 校验：**未发生**（没有实施变异，故无恢复动作）。
- 直接后果：SC-006 的「移除行为 → 至少 1 条转红」**not-evaluated**，不得记为满足。

## T027 — 全量名字级回归

`waived/not-run`。命令 `SPECKIT_PYTHON=… bash scripts/bash/run-tests.sh --names-out /tmp/065a-current-failed.txt -q` 未执行；`comm -13` 差集无可比较对象；**NEW 失败计数为 not-evaluated，不是 0**。本轮唯一可得的失败面证据是 `tasks.md` § Environment Prerequisites 记录的 26 个用例，它们在用户豁免下记 `waived/not-run`（实测口径：last observed 26 failed before T015–T018 implementation (commit 35aa0192); not re-run after T015–T018; current red/green is not evaluated）。

## T028 — SC 证据矩阵

- **SC-001**: 状态 = **smoke-verified（子集）**；度量命令 = `python3 /tmp/065a_smoke.py`（一次性夹具，见 `notes/quickstart-run.md` §2）；输出摘要 = `rc=0 loop_state=FAILED verdict_source=derived action=retry reason=salvage-not-recorded forms=[artifacts-without-completion] uncommitted=5`；单次调用即给出中断形态与 `retry` 建议，「人工逐文件检查次数 = 0」成立。完整字段级断言（含 `resume` 分支）属被豁免的 `test_sc001_accident_replay_suggests_resume_or_retry`，该部分 `waived/not-run`。证据路径 `notes/quickstart-run.md` §2。
- **SC-002**: 状态 = **smoke-verified**；度量命令 = 同一夹具连续两次 snapshot 后剔除 `evaluated_at` 比较 + 全信封退化值扫描；输出摘要 = `evaluated_at` 相同（04:08:02Z）且剔除后信封完全相等（差异数 0）；扫描得 `status=missing` 7 项、`value_state=unknown` 1 项、`status=na` 1 项、零值/`ok` 猜测 0 项。证据路径 `notes/quickstart-run.md`（§2/§6 的缺失值形态）与本条。
- **SC-003**: 状态 = **部分 smoke / 部分 `waived/not-run`**。正常窗口误报 `unwatched` 次数：`--self-test` 的 `unwatched-*` 正逆用例全通过（`SELF-TEST: 36 passed, 0 failed`）→ 观测到的误报数为 0；但计数型断言（三组夹具的逐条计数）与「活进程不得建议立即终止」的动作断言由 `test_watch_only_for_live_*` / `test_timeout_live_process_watch` 等被豁免用例承载 → `waived/not-run`。动作面另有 smoke 支撑：活进程 `TIMEOUT` 在 `--self-test` 中落到 `watch`（非 kill），引擎动作封闭集内不存在 kill/terminate 取值。
- **SC-004**: 状态 = **smoke-verified（watcher 面） / `waived/not-run`（测试面）**。`watch-target.sh --self-test` → 38 passed / 0 failed，exit 0，与基线零差异；四件套与 Registry 兼容读取由 US5-A2 的 smoke 证明可读。驱动技能契约测试与 `line-registry` 引擎测试**未运行** → `waived/not-run`。
- **SC-005**: 状态 = **smoke-verified**。源/镜像字节一致率 100%（3/3 对 IDENTICAL，sha256 相等），`sync-mirrors --check` exit 0（28 files）；文档入口已更新（`skills/external/sdd-loop-driver/SKILL.md` Hard Requirement 8 + References 行；`docs/reference/skills/sdd-loop-driver.md` §状态感知快照）；新增 daemon / 外部依赖数 = 0（仅标准库；无新增 `pyproject.toml` 依赖，见 §T029）。
- **SC-006**: 状态 = **not-evaluated**。逆样本覆盖率与变异转红均需 pytest 运行，用户豁免下 `waived/not-run`（见 §T026）。**不得**读作满足。

## T029 — 只读与范围审计

**`git status --short`**（本段收尾前，逐字）：

```
 M .specify/skills/sdd-loop-driver/SKILL.md
 M .specify/specs/065a-state-awareness/notes/state-spine.md
 M docs/reference/skills/sdd-loop-driver.md
 M skills/external/sdd-loop-driver/SKILL.md
 M skills/external/sdd-loop-driver/scripts/loop-state.py
 M tests/contract/test_loop_state_contract.py
 M tests/contract/test_sdd_loop_driver_skill.py
?? .specify/skills/sdd-loop-driver/references/state-awareness.md
?? .specify/skills/sdd-loop-driver/scripts/loop-state.py
?? .specify/specs/065a-state-awareness/notes/quickstart-run.md
?? .specify/specs/065a-state-awareness/verification.md
```

**`git diff --stat`**：7 files changed, 133 insertions(+), 7 deletions(-)（明细见上表同名文件；`verification.md` / `quickstart-run.md` / 两份新镜像为未跟踪新增）。

- **镜像改动来源**：`.specify/skills/sdd-loop-driver/` 的 3 个路径（`SKILL.md` 修改、`references/state-awareness.md` 与 `scripts/loop-state.py` 新增）全部由 `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 产出；`--check` 复验 `ok skills/external/ == .specify/skills/ (28 files)` exit 0，三对 `cmp -s` IDENTICAL。**未手改任何镜像**。
- **禁改面零命中**（`git status --short -- <path> | wc -l` 均为 0）：`.specify/specs/066-`、`067-`、`068-`、`.specify/specs/065-loop-interruption-recovery`、`skills/external/sdd-loop-driver/scripts/watch-target.sh`、`skills/external/sdd-loop-driver/scripts/line-registry.py`、`templates/commands`、`.specify/templates`、`pyproject.toml`。
- **无 daemon / 外部依赖**：`loop-state.py` 仅标准库；无新增依赖、无网络轮询、无常驻进程；`pyproject.toml` 零改动。
- **无 push / merge / kill / 删除**：本段只有本地 `git` 读操作（status/log/diff）与 `sync-mirrors --write`（生成器）；未执行 push、merge、分支操作、进程终止或文件删除。
- **写入面 mtime 审计**（临时夹具，30 个既有文件）：snapshot 前后既有文件 `mtime_ns` 变化数 = **0**；新增文件全部落在两处非证据面 —— 一次性夹具的 `repo/.git/`（`git log` 读操作刷新索引/对象）与重定向 `HOME` 下解释器自身的 `.pyc` 缓存；`state/` 目录**无新增文件**（未创建 watchbeat、未写脊）。仓库工作树在全部 smoke 运行后 `git status` 无意外变化。
- **结论**：改动集合 = 本特性源（`skills/external/sdd-loop-driver/` 的 `loop-state.py`、`SKILL.md`、`references/state-awareness.md` 为新）、本特性测试（两份 contract 测试）、本特性 docs（`docs/reference/skills/sdd-loop-driver.md`）、生成面镜像、本特性 evidence（`notes/quickstart-run.md`、`verification.md`、`notes/state-spine.md`）。无越界。

## T030 — Completion Gate 复验

| Gate | 命令 | 退出码 | 关键输出 | 状态 |
|------|------|--------|----------|------|
| GATE-1 | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/065a-state-awareness/tasks.md` | 0 | `PASS … 0 error(s), 0 warning(s)` | **pass** |
| GATE-2 | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/065a-state-awareness --stage tasks --repo .` | 0 | `stage=tasks decision=pass errors=0 advisories=0 waived=0`；`fr=25 sc=6 tasks=30 files=14` | **pass** |
| GATE-3 | `bash scripts/bash/run-tests.sh tests/unit/test_loop_state_engine.py tests/contract/test_loop_state_contract.py tests/contract/test_sdd_loop_driver_skill.py -q` | — | 未执行 | **waived/void**（用户豁免原文见本文件 § Test waiver；不计为 pass） |
| GATE-4 | `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` | 0 | `SELF-TEST: 38 passed, 0 failed` | **pass** |
| GATE-5 | `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` | 0 | `ok skills/external/ == .specify/skills/ (28 files)`；`plan.md` § Mirror Obligations 三对 `cmp` 全 IDENTICAL | **pass** |
| GATE-6 | `grep -cE '^- \[[ >]\]' .specify/specs/065a-state-awareness/tasks.md` | 1（= 零命中；`grep -c` 无匹配即计数 0、退出码 1） | 计数输出 `0`；`[X]` 行数 `30` | **pass**（计数为 0，代价是 `grep` 的零匹配退出码 1，不是失败） |
| GATE-7 | `grep -cE '^- \*\*SC-00[1-6]\*\*' verification.md` / `grep -cE '^- \*\*US5-A[1-4]\*\*' verification.md` | 0 | `6` / `4` | **pass** |

**附加确定性门**（T030 的清单项）：

| 检查 | 命令 | 退出码 | 关键输出 | 状态 |
|------|------|--------|----------|------|
| 条款认领 | `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/065a-state-awareness` | 0 | `claimed clauses 60`、`FR claimed 25 / universe 25 / uncovered 0`、`uncovered beyond baseline: 0`、`status: ok` | **pass** |

**未通过项声明**：GATE-3 在用户测试豁免下**未执行**，因此本切片**不声称 DoD-4 达成**；其余六道 Gate 与条款认领实跑通过。Feature 065 仍为 `Planned`，本文件只记录 `065a slice implementation-complete with test waiver`。

## 收口统计

- 任务：30/30 `[X]`（T001–T018 前段完成，T019–T030 本段完成）；`[~]` = 0；`deferred_tasks=` 为空。
- 测试面：26 个用例记 `waived/not-run`（T015×18、T016×5、T018×3）；T019 / T020 / T021 / T024 / T026 / T027 的 pytest 部分同样 `waived/not-run`；GATE-3 `waived/void`。实测口径：last observed 26 failed before T015–T018 implementation (commit 35aa0192); not re-run after T015–T018; current red/green is not evaluated。

## 就地修复披露（fast-fail 顺手修复：RP-1 近似错）

`skills/external/sdd-loop-driver/scripts/loop-state.py` 的 `uncommitted_artifacts_of()` 原以 `candidate.endswith(rel)` / `("/" + rel) in candidate` 匹配 pathspec，而 git 输出的 pathspec 条目无尾斜杠（`…/contracts`），导致目录类必需产物（`contracts/`）永远进不了 `uncommitted_artifacts[]`——与 `contracts/stage-artifact-map.md` C-59「必需产物存在但基线之后没有提交触及它 → 列入」及 `missing_artifacts` 侧已用尾斜杠的对称写法不符。

- **判据**：纠正侧（唯一读法 = C-59 + `STAGE_ARTIFACTS` 的目录类产物声明）；局部且可逆（单函数内 5 行）；未证伪下游前提（可见测试断言均不覆盖目录类产物的该分支，已逐条核对 `tests/unit/test_loop_state_engine.py` 的 `uncommitted_artifacts` 断言）；爆炸半径 = 本切片源文件。
- **验证**：`--self-test` 修复后复跑 `36 passed, 0 failed` exit 0；§2 smoke 的 `uncommitted_artifacts` 由 4 → 5（含 `contracts/`）。pytest 面按豁免未运行 → 「无新增红」**未经测量**，不作声明。
- **痕迹**：`notes/quickstart-run.md` §就地修复；本段提交记录。

## 未测量与剩余风险

1. **26 个用例（`35aa0192` 时 last observed 红；T015–T018 实施后未复测，current red/green not evaluated）+ 本轮三份测试文件的运行**全部未执行：字段级断言、probe 隔离、salvage 门、动作阶梯的 pytest 级验收仍是账面外的验收面；`--self-test` 与 smoke 只覆盖其中一部分。
2. **SC-006 变异演练未做** → 新增检查的逆样本有效性未经变异证明。
3. **T027 全量回归未做** → 相对 T001 基线的 NEW 失败数不可知（不是 0）。
4. **就地修复未经 pytest 验证**：若未来发现某绿用例依赖旧的目录类产物行为，需按 RP-1 的判据复核而非回退本修复。
5. **Feature 065 仍在 `Planned`**：065b（watchbeat 写入 / heartbeat-stalled / lifecycle-spine-violation）与 065c（`recover` / salvage 落盘 / 物理隔离）承接本切片显式保留的形态与动作。

