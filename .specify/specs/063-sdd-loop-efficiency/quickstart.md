# Quickstart: sdd-loop-driver 运行效率优化（SDD Loop Efficiency）

**Feature**: 063 → Feature 058（演化）
**前置**: bash、`git`、`python3`（≥3.8，仅标准库）；目标项目具备 `.specify/` 结构；项目有规范测试运行器（本仓 = `scripts/bash/run-tests.sh`）。远端拓扑另需 `ssh` 与 `su`。

> **术语**：`[[STR-006]]` = 字面量 `fast-lane=opt-in`（引用编号见 requirements.md § Shared Strings；本文只在此处给出一次字面量）。**U4** = 驱动对阶段的独立校验（哨兵 + 产物核验 + 纪律抽查），与阶段执行子代理分离。`state_spine_path` = U0 入口声明记录的线状态脊路径；阶段提示词骨架用 `STATE_SPINE_PATH` 引用同一路径。CLI 能力档案的术语、场景与观测程序由 Feature 064 拥有（`contracts/cli-profiles.md`）；本文不复述。
>
> **执行验证声明（逐例）**：下列命令在 plan 阶段尚无实现脚本，因此按 `/speckit.plan` Post-Generation Quality Gate 的 route (b) 处理——每条示例由指定的契约/单元/集成测试钉住，并在实现阶段执行一次。文件级免责不适用：每条示例单独列出前提；实现阶段 MUST 把「钉住」落实为真实测试，未能落实的示例 MUST 删除而不是保留。
>
> **退出码约定**：仅对本文新增的 Python 工具（admission-check / derive-live-log / audit-*）约定 `0` 成功或可录取、`1` 拒绝或审计失败、`2` 输入或解析错误。watch-target.sh 的退出码以该脚本 `--help`/`--self-test` 为准（本文不复写数值）。

## 准备（所有场景共用）

```bash
export WORK063=$(mktemp -d)
cp -R tests/fixtures/sdd_loop_efficiency/medium "$WORK063/medium"
cp -R tests/fixtures/sdd_loop_efficiency/large "$WORK063/large"
cp -R tests/fixtures/sdd_loop_efficiency/plan-repo "$WORK063/plan-repo"
cp tests/fixtures/sdd_loop_efficiency/state-spine-valid.md /tmp/063-line-state.md

for d in medium large plan-repo; do
  git -C "$WORK063/$d" init -q
  git -C "$WORK063/$d" add -A
  git -C "$WORK063/$d" -c user.name=fixture -c user.email=fixture@example.com commit -qm "fixture base"
done
git -C "$WORK063/medium" checkout -q -b 012-medium
git -C "$WORK063/large" checkout -q -b 013-large

FIXTURE="$WORK063/medium"
FIXTURE_LARGE="$WORK063/large"
FIXTURE_REPO="$WORK063/plan-repo"
BASE=$(git -C "$FIXTURE" rev-parse HEAD)
BASE_LARGE=$(git -C "$FIXTURE_LARGE" rev-parse HEAD)
PLAN_BASE=$(git -C "$FIXTURE_REPO" rev-parse HEAD)
```

- **前提**：夹具树由 `tests/fixtures/sdd_loop_efficiency/` 提供；`medium` 含 12 条 FR / 25 条任务、全绿需求清单、`entry.md`（含 `fast-lane=opt-in`）与 `lines.manifest`（按 `data-model.md` E1「lines.manifest 行语法」实例化的恰一条本线记录）；`large` 含 60 条任务；`state-spine-valid.md` 含 baseline/closure 台账围栏；`plan-repo` 含 plan 六件套。
- **钉住**：`tests/unit/test_admission_check.py` 的夹具构造与 `tests/unit/test_audit_test_budget.py` 的台账夹具。

## S1 — 中型特性快车道准入（录取）

```bash
python3 skills/external/sdd-loop-driver/scripts/admission-check.py \
  --project "$FIXTURE" --base-ref "$BASE" --expected-branch 012-medium \
  --requirements "$FIXTURE/.specify/specs/012-medium/requirements.md" \
  --tasks "$FIXTURE/.specify/specs/012-medium/tasks.md" \
  --checklists "$FIXTURE/.specify/specs/012-medium/checklists/requirements.md" \
  --entry-evidence "$FIXTURE/.specify/specs/012-medium/entry.md" \
  --lines-manifest "$FIXTURE/.specify/specs/012-medium/lines.manifest" \
  --json-out /tmp/063-admission.json
```

- **前提**：七判据全部机械可判；FR 定义行与任务行的计数语法 owner 为 `requirements.md` FR-003(a)（本示例不复写正则），区间 owner 同为 FR-003，脚本常量为运行时 owner；`lines.manifest` 行语法 owner 为 `data-model.md` E1。
- **预期**：exit 0；`/tmp/063-admission.json` 的 `decision=fast-lane`、七项判据齐全、`measured.fr_count=12`、`measured.task_count=25`。
- **钉住**：`tests/unit/test_admission_check.py::test_medium_fixture_admitted` + `tests/contract/test_sdd_loop_driver_efficiency.py::test_fl_08_admission_script_interface`。
- **清理**：`rm -f /tmp/063-admission.json`。

## S2 — 大型特性准入（拒绝，fail-closed）

```bash
python3 skills/external/sdd-loop-driver/scripts/admission-check.py \
  --project "$FIXTURE_LARGE" --base-ref "$BASE_LARGE" --expected-branch 013-large \
  --requirements "$FIXTURE_LARGE/.specify/specs/013-large/requirements.md" \
  --tasks "$FIXTURE_LARGE/.specify/specs/013-large/tasks.md" \
  --checklists "$FIXTURE_LARGE/.specify/specs/013-large/checklists/requirements.md" \
  --entry-evidence "$FIXTURE_LARGE/.specify/specs/013-large/entry.md" \
  --lines-manifest "$FIXTURE_LARGE/.specify/specs/013-large/lines.manifest"
```

- **前提**：夹具含 60 条任务（越出 FR-003 冻结的任务行区间）；入口字面量仍在。
- **预期**：exit 1；输出 `decision=full-chain`，criterion `a` 为 `fail`，`evidence` 给出实测 `task_count=60` 与区间引用。
- **钉住**：`tests/unit/test_admission_check.py::test_large_fixture_denied` + 边界用例 `test_task_count_boundary_edges`。

## S3 — 两槽位台账与收口审计

```bash
python3 skills/external/sdd-loop-driver/scripts/audit-test-budget.py \
  --spine /tmp/063-line-state.md --spec-dir "$FIXTURE/.specify/specs/012-medium"
```

- **前提**：`/tmp/063-line-state.md` 由准备步骤复制；含 baseline 与 closure 两条 JSONL、closure 带 `comm -13` 结果；`<spec-dir>/baseline-failed.txt` 与 `final-failed.txt` 存在。若夹具同时含快车道授权跳过的 checklist，E3 记 `not-applicable-skipped-stage`（[[STR-008]]），以 E1 准入记录与 [[STR-003]] 联结。真实运行时 `--spine` 必须是 U0 入口声明的 `state_spine_path`；远端拓扑（`spine_write_mode=transport`）下，执行侧先写 `<spec-dir>/test-evidence/implement.jsonl` 传输行，驱动合并进状态脊并记 `merge_source`/`merged_at`，合并前不审计。
- **预期**：exit 0；摘要 `slots=baseline:1 closure:1 reruns=N exceptions=0 unknown=0 stages=N complete=N`；授权跳过阶段不得计入 `unknown` 或完整性分母；`not-run-docs-only` 按缩减字段集计入完整，不报 `unknown`；整阶段缺失 `stage-status` 行必须使 `complete` 小于 `stages`。若增删槽位、缺 `exception_reason`、用计数比较替代名称级差集、或漏掉 docs-only 缩减字段，审计 MUST exit 1。
- **钉住**：`tests/unit/test_audit_test_budget.py`（合法台账、槽外例外、槽内重跑、环境失败、缺证据 unknown、日志扫描未入账命中、docs-only 缩减字段、缺失 stage-status 行、合并来源）。
- **清理**：`rm -f /tmp/063-line-state.md`。

## S4 — 派生实时日志与哨兵判定

```bash
# 4a. 非终止事件里出现哨兵字样：不得判 DONE（status 由 runner 语义模拟：exit=0、sentinel=0）
python3 skills/external/sdd-loop-driver/scripts/derive-live-log.py \
  --events tests/fixtures/sdd_loop_efficiency/stream/non_terminal_sentinel.jsonl \
  --out /tmp/063-live-a.log
printf 'exit=0 at=1 sentinel=0 progress=stream\n' > /tmp/063-status-a
bash skills/external/sdd-loop-driver/scripts/watch-target.sh \
  --label demo-a --log /tmp/063-live-a.log --status-file /tmp/063-status-a \
  --sentinel PLAN-DONE --window 0 --start-grace 0

# 4b. 终止 result 事件携带哨兵：不提供 status，watcher 只凭派生日志最后非空行判 DONE
python3 skills/external/sdd-loop-driver/scripts/derive-live-log.py \
  --events tests/fixtures/sdd_loop_efficiency/stream/result_sentinel.jsonl \
  --out /tmp/063-live-b.log
bash skills/external/sdd-loop-driver/scripts/watch-target.sh \
  --label demo-b --log /tmp/063-live-b.log \
  --sentinel PLAN-DONE --window 0 --start-grace 0
```

- **前提**：4a 的派生输出最后一行是带前缀的进度行（哨兵字样只出现在中间事件）；4b 的派生输出最后非空行是 `PLAN-DONE`。watcher 只认日志最后非空行，不解析 JSON。
- **预期**：4a 判 `INCOMPLETE`（伪完成候选，因为配置了哨兵且 status 明示 sentinel=0）；4b 判 `DONE`（`reason=sentinel`，仍待 U4 独立校验）。
- **钉住**：`tests/unit/test_derive_live_log.py` + `watch-target.sh --self-test` 的 stream 用例。
- **清理**：`rm -f /tmp/063-live-a.log /tmp/063-live-b.log /tmp/063-status-a`。

## S5 — 本地 nohup 脱离存活

```bash
TMP063=$(mktemp -d)
export TMP063
bash -c 'nohup bash skills/external/sdd-loop-driver/scripts/stage-runner.sh \
  --cli "$PWD/tests/fixtures/sdd_loop_efficiency/stub-cli.sh" --cli-args "" \
  --project-dir "$TMP063" --prompt-file /dev/null \
  --sentinel PLAN-DONE --line demo --stage plan --state-dir "$TMP063" \
  --mode stream </dev/null >"$TMP063/runner-log-demo-plan.log" 2>&1 & \
  echo $! >"$TMP063/runner.pid"'
# 启动它的 bash -c 已退出；runner 被重新挂到 init，必须继续跑完
sleep 3
[ -f "$TMP063/status-demo-plan" ] || { echo "runner did not finish"; exit 1; }
cat "$TMP063/status-demo-plan"
cat "$TMP063/log-demo-plan.log"
rm -rf "$TMP063"
```

- **前提**：stub CLI 产出 `system(init)`、`assistant` 与终止 `result` 事件，其 `result` 文本最后一行是 `PLAN-DONE`；`--project-dir` 与 `--state-dir` 为临时目录；启动用的 `bash -c` 在后台进程拉起后立即退出。
- **预期**：`status-demo-plan` 含 `exit=0`、`sentinel=1`、`progress=stream`；`log-demo-plan.log` 最后非空行 = `PLAN-DONE`；`rm -rf` 只在 status 存在后执行。
- **钉住**：`tests/integration/test_sdd_loop_efficiency_runner.py::test_local_nohup_survives_parent_exit`。

## S6 — Plan 改动分类（未声明 → 门失败）

```bash
printf '\n<!-- plan repair -->\n' >> "$FIXTURE_REPO/.specify/specs/012-medium/plan.md"
git -C "$FIXTURE_REPO" add -A
git -C "$FIXTURE_REPO" -c user.name=fixture -c user.email=fixture@example.com commit -qm "plan repair"
PLAN_HEAD=$(git -C "$FIXTURE_REPO" rev-parse HEAD)
: > /tmp/063-plan-edits.txt
python3 skills/external/sdd-loop-driver/scripts/audit-plan-changes.py \
  --repo "$FIXTURE_REPO" --base "$PLAN_BASE" --head "$PLAN_HEAD" \
  --plan-owned plan.md --plan-owned data-model.md --plan-owned contracts \
  --plan-owned quickstart.md --plan-owned research.md --plan-owned feature-ref.md \
  --declarations /tmp/063-plan-edits.txt
```

- **前提**：`PLAN_BASE..PLAN_HEAD` 内有一个提交修改 `plan.md`，阶段回传未包含 `PLAN-EDIT:` 行（`/tmp/063-plan-edits.txt` 为空）；六个 plan 拥有路径全部传入；U4 分类记录写 E4 最新的 `approved_baseline_commit`（初始 = `plan_commit`，re-baseline 后 = 最新基线），分流判定以该提交的 `requirements.md` 为比较对象。若 `requirements.md` 在 plan U4 后发生变更（如 analyze 路由修复），在下一个依赖基线的 U4 分类前必须已有 E4 `rebaseline_events[]` 记录；未提交或无法定位提交时不得 re-anchor，受影响 plan 改动按 FR-022(b) 上送。本特性自身实例：plan U4 在 `5ab8a5e7`，requirements-repair 第 1 轮在 `0c719b80`、第 2 轮在 `864940de`，plan-repair-2 在 `bcf27c77`；tasks-repair-2 的 CLI-profile 收口 requirements 提交是下一个锚点候选。
- **预期**：exit 1；输出 `touched_paths=["plan.md"]`、`undeclared=true`；驱动据此判该阶段门失败并进入 PC-06 分流。若删除 re-baseline 记录并以旧 `plan_commit` 比较，分类 MUST 判不可信。
- **钉住**：`tests/unit/test_audit_plan_changes.py::test_undeclared_plan_change_flagged`（含未提交改动用例）；契约 `test_pc_11_reanchoring`。
- **清理**：`rm -f /tmp/063-plan-edits.txt`。

## S7 — 端到端编排演练（LLM 驱动；录制证据）

按 `references/efficiency-model.md` 的 U0–U6 流程，用一个中型夹具跑一次「入口携带 `fast-lane=opt-in` → tasks 后准入 → 跳过 checklist → analyze → implement（起点全量）→ review → 收口全量 → 合并」；同时跑一个未携带字面量的对照，确认完整链。记录派发序列、状态脊、台账与收尾汇总。

- **证据形态**：实现期在 `verification.md` 粘贴两份录制 trace（快车道/完整链）的路径与要点；CI 只自动验证确定性组件与契约条款，不冒充端到端证明（better-harness 证据纪律）。SC-002/SC-003/SC-006/SC-008 的非自动部分以该 trace 为证据并如实标注。
- **卡死行为基线（SC-010）**：在实现首个行为面提交之前，于冻结提交 `ba2a18db` 的只读 worktree 上，用驱动侧可执行夹具 `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` 录制 [[STR-007]] 的三类处置元组（超时 / 重试上限 / 伪完成）：stub runner 产生受控 status/rc，真实 `watch-target.sh` 提供 U3 判定，夹具执行文档化 U4/U5 程序并观测七个字段；`initial_retries=0`，`exit_code` 分 `{watcher, runner}`；夹具不得从判定表转录或硬编码期望值。收口用同一夹具重放，归一化剔除时间戳、PID、绝对路径与耗时后逐字段比较，零差异为通过。该录制不是全量测试运行，不消耗两个全量槽位；名称级基线只服务 SC-012。
- **钉住**：`tests/contract/test_sdd_loop_driver_efficiency.py::test_fl_10_self_application_exclusion` 只钉住「本特性自身不走快车道」；trace 本身不是 CI 测试。

> **CLI 能力档案场景（归属 064）**：派发前查档、U2/U4/U5 观测、known/unknown 与 feedback 标记的执行示例由 Feature 064 的 quickstart 与 `contracts/cli-profiles.md` 拥有；本文不复制、不重测。

## 清理（全部场景结束后）

```bash
rm -f /tmp/063-admission.json /tmp/063-line-state.md \
      /tmp/063-live-a.log /tmp/063-live-b.log /tmp/063-status-a /tmp/063-plan-edits.txt
rm -rf "${TMP063:-}" "${WORK063:-}"
```

- **前提**：S1–S7 各自已清理其临时文件；本步骤兜底移除共享准备目录。
- **验证**：`test -z "$(ls -d /tmp/063-* 2>/dev/null)"` 输出为空（S5 的 `$TMP063` 已在其步骤内删除）。

## 执行验证状态（plan 期）

| 示例 | 路由 | 钉住者 | 前提清单 |
|------|------|--------|----------|
| S1/S2 | (b) 计划测试 | `test_admission_check.py` | 脚本 CLI、exit 语义、夹具 git 布局、lines manifest 行语法 owner、FR-003(a) 计数 owner、窄/宽任务计数边界 |
| S3 | (b) 计划测试 | `test_audit_test_budget.py` | 台账围栏、JSONL 字段、names 文件、状态脊夹具、not-applicable 跳过语义、docs-only 缩减字段、`stages=N complete=N`、远端 merge_source |
| S4 | (b) 计划测试 | `test_derive_live_log.py` + self-test | 事件形状、result 字段、bash 调用、4b 日志-only 判定 |
| S5 | (b) 计划测试 | runner 集成测试 | stub CLI 形状、nested bash 退出、nohup 形态、status 字段、删除前校验 |
| S6 | (b) 计划测试 | `test_audit_plan_changes.py` + `test_pc_11_reanchoring` | git 区间、六个 plan 路径、`PLAN-EDIT:` 声明格式、最新 `approved_baseline_commit`、re-baseline 事件 |
| S7 | 录制证据（非 CI） | verification.md + driver-stall-fixture | 中型夹具、入口字面量、阶段链、[[STR-007]] 驱动侧可执行夹具录制/重放、`initial_retries=0`、`exit_code: {watcher, runner}` |

> CLI 能力档案的查档/观测场景由 Feature 064 拥有，不在本表；本文件不重复其钉住者或前提。
