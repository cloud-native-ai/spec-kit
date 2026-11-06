# Line State — 086-efficient-test-execution

<!-- loop-state:begin -->
spine_state: running
run_id: r20261106T033959Z-086a
slice: 086
stage: clarify
stage_started_at: 1793937900
stage_deadline_epoch: 1793948700
stage_base_commit: 2a88a9e7
attempt: 0
retry_limit: 3
last_verdict: requirements U4 pass after 3 in-passing repairs; temp goal created and spec-local; checkpoint 01 written; clarify dispatch next
<!-- loop-state:end -->

- line_id: `086-efficient-test-execution`
- run_id: `r20261106T033959Z-086a`
- project_dir: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- repo_root: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- worktree: `none（本地拓扑，主工作区；feature branch 由 requirements 阶段从 master 创建）`
- base_sha: `24cb4edc`
- trunk: `master`（`docs/git-workflow.md`；`main` 为上游世系，不参与合并）
- topology: `local`（宿主原生子代理；MUST NOT 启动 qodercli）
- line_role: `coordinator`
- state: `running`

## U0 入口声明

- **目标项目**：spec-kit 框架源码仓（本地 `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`）。
- **执行拓扑**：本地（宿主原生子代理；阶段派发不启动 qodercli）。
- **运行模式**：**无人值守**——不逐阶段等待用户确认；U0–U6 自动续环，只在里程碑/阻塞/停线时上报；U6 缺省本地合并回 `master`，**不 push**。
- **终态权威文档**：
  - 用户本轮两条需求（测试高效执行 + 把原则固化到 constitution/instructions）；
  - 用户追加指令（先拉取上游，再无人值守走 SDD；保留并使用 085 的 team/并发机制）；
  - 已批准计划 `/Users/liuqiming.lqm/.qoder-cli/plans/glacial-ledge-bull.md`；
  - `.specify/memory/constitution.md`（v1.16.0）与 `.specify/instructions.md`；
  - `.specify/specs/085-sdd-temporary-goal-team/{requirements.md,plan.md,contracts/}`；
  - `.specify/specs/067-loop-efficiency-hardening/contracts/runner-contract.md` RC-03；
  - `.specify/memory/todo/20261030-suite-speed-optimizations.md`；
  - `docs/git-workflow.md`。
- **特性切片**：**086 Efficient Test Execution (Concurrent by Default)** ——（a）spec-kit 自身测试套件默认并发执行（pytest-xdist 进程级并行），保留显式 serial 路径与 name-level 失败捕获；（b）新增 owner guideline，把「测试覆盖不够、测试还必须能高效执行；同步/子进程/CPU-bound 用进程并行，I/O-bound 用 async 并发」固化进 constitution（template + live）与 instructions（template + live），随框架分发；（c）保留 085 的临时 Goal/Team、stage agents、24 并发、worktree/集成队列、checkpoint，并用本次 086 运行做真实场景 dogfood + 085 SC-010 证据补全。预期下一可用 Feature ID = 086；不拆片，除非 plan/tasks 门判 split-required。
- **断点**：U1 自动探测；初始事实为新拉取的树无 `086-*` spec 目录，预期断点 = `requirements`。
- **阶段计划**：`requirements → clarify → plan → tasks → checklist → analyze → implement → review → closure（review 后全量）→ 工作树清扫 → 本地合并 master`；完整链，无快车道。
- **快车道**：入口未声明 `fast-lane=opt-in` → 不走快车道，checklist/analyze/review 必经。
- **拆解开关**：`decomposition: auto`；`decomposition_stages: plan=auto, implement=auto, review=auto`；`decomposition_slot_cap: 2`。
- **测试预算**：implement 起点一次全量 baseline、review 后一次 closure；中间阶段用定向集。改造后的 canonical runner 在 closure 默认并行，baseline 可用 `--serial` 取串行口径，二者按失败名称差集比较。
- **合并**：本地合并到 `master`；**不 push**（用户未授权 push）。

## 085 机制保留与实测（本次运行即 085 的真实场景 dogfood）

- **临时 Goal（085）**：**已创建** `.specify/specs/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md`（slug `086-efficient-test-execution`，status `active`，engine `validate: valid`）；创建时曾因参数顺序误写全局 `.specify/goal/`，已删除该错误目录并重建 spec-local。
- **临时 Team（085）**：clarify + plan U4 通过后，经 `/speckit.team create --scope spec --spec-dir <spec>` 创建 spec-local 临时 Team；写入 `temp_team_slug`；全局 `.specify/teams/**` 为 forbidden。
- **并发度（085）**：`agent_concurrency_requested: 24`；`agent_concurrency_effective: 24`（初值；host capacity 未声明 → 记录 `host-capacity-undeclared`；每阶段按 ready packages / stage max_parallel / resource capacity 重算）；`verifier_reserve: 6`（`max(1, ceil(24/4))`）；executor slots = 18；任何降级必须具名写入状态脊。
- **写隔离（085）**：`write_isolation=worktree`（temporary-team 运行 opt-in）；写 agent 各占 child line + 独立 worktree + 集成队列；读-only agent 可共享；child worktree 位于 `.specify/.tmp/sdd-loop/worktrees/<child_line_id>`，分支 `line/<child_line_id>`；不 push。
- **Checkpoint（085）**：每阶段 U4 后、下一阶段派发前执行四步 checkpoint（产物核验 / 临时 Goal 进度 / 至多一条 team 配置提案 / 下一阶段并发与 roster），写 `<spec-dir>/checkpoints/<NN>-<stage>.md`；回滚规则按 checkpoint-protocol。
- **保留义务**：不删除、不禁止、不绕过、不重写 085 的 goal/team/checkpoints/contracts 与历史记录；086 改动必须 additive；086 落地后重跑 085 的 contract/integration 测试；085 SC-010 只有在取得完整 dogfood 证据后才可 pass，否则保持 partial 并写明缺口。
- **本次 dogfood 证据**：requested/effective 并发、至少一个阶段实际并发派发数、临时 Goal/Team slug、每阶段 checkpoint、stage agents 名单、新 runner 在真实 SDD 运行中的 baseline/closure wall-clock 与失败名称差集。

## Phase 0 事实与证据（已完成）

- 上游 `gitlab/master` 已 fast-forward：`master` = `24cb4edc`（48 个提交）；工作区在 pull 后干净。
- 上游已有 084/085；`features.md` 80 行 / `Total Features: 80`；新特性后 81；下一 Feature ID = 086。
- `constitution` v1.16.0 / live 19 条；instructions template 32 节 / live 33 节。
- 085 的 goal/team/checkpoints/contracts 已随 pull 落地；085 `verification.md` 的 `SC-010_status=partial`（缺完整 8 阶段 driver run with LLM stage agents）。
- 上游 `run-tests.sh` / `pyproject.toml` 无 xdist；已有 suite-speed TODO 与 067 RC-03（串行默认、xdist 准入但未采用）。
- 旧树方向性证据：7347 collected / 0 async / 167 subprocess；unit 116s → 47s；full serial 797s / 20 failed；full parallel 235s / 21 failed（唯一新增 `test_c22_watch_target_hook_selftest`，watch-target 自测在并行负载下超 60s）。
- 预拉取工作区的 085 运行时刷新是生成物；已用唯一 stash `4a6a7a7e3d31f901d42e0a2e9cc8ebb608cf0298`（message `086-pre-pull-generated-runtime-20261106T1135`）保存，未 pop；上游 085 是权威版本，待 085 核对后决定是否丢弃该 stash。
- 更新后树的 **Phase 0 对照已完成**（见下）；工作区仅多出本 U0 状态脊。

### Phase 0 baseline vs parallel（post-pull，2026-11-06T03:54Z）

| 口径 | 命令 | 结果 | 耗时 |
|---|---|---|---|
| 串行 baseline | `run-tests.sh --names-out .specify/.tmp/086/baseline-failed.txt -q` | 7475 passed / **19 failed** / 7 skipped | **1031.48s（17:11）** |
| 并行对照 | `run-tests.sh -n auto --names-out .specify/.tmp/086/parallel-failed.txt -q` | 7474 passed / **20 failed** / 7 skipped | **201.87s（3:21）** |

- 加速比：约 **5.1×**（同一 runner、同一 selection、同一 names-out 口径）。
- `comm -13 baseline parallel` 唯一新增：`tests/contract/test_sdd_loop_driver_skill.py::test_c22_watch_target_hook_selftest`——watch-target 自测在并行负载下超 60s；串行约 28s（067 已记录）。
- `comm -23` 无修复项；两个失败集除该新增外完全一致。
- 工作区：`git status --porcelain` 仅 `?? .specify/state/086-efficient-test-execution.md`；无镜像/生成物污染。
- 结论：进程级并行方向成立；requirements/plan 必须把 watch-target 自测作为**显式 serial 例外或超时修复**处理，最终 closure 的并行 run 必须做到相对该 baseline 零名称级新增失败。

## U1 PROBE（2026-11-06T03:40Z）

- branch: `master`；HEAD: `24cb4edc`；最近提交：`merge(085): integrate the temporary Goal/Team line`。
- spec 目录：无 `.specify/specs/086-*`；`requirements.md` 缺失。
- 终态文档：`.specify/memory/constitution.md`、`.specify/instructions.md`、`docs/git-workflow.md` 均存在。
- 断点判定：**requirements**。
- 下一动作：等待 post-pull serial baseline（后台）结束后再派发 U2，避免 requirements 创建 feature branch/spec 目录污染预特性基线。
- registry：coordinator line `active`；`update --stage` 在本地原生派发下要求 runner_pid，当前不设置 stage；U4 以状态脊 + 子代理返回 + 产物校验为准。

## U4 requirements（2026-11-06T04:04Z）

- sentinel: `REQUIREMENTS-DONE`；stage commit `2a88a9e7`；branch `086-efficient-test-execution`。
- artifacts: `requirements.md` / `checklists/requirements.md` / `test-evidence/requirements-gates.txt` / `features.md` row 086 / `features/086.md`。
- driver independent gates: `pre-analyze` pass errors=0 advisories=1（唯一 advisory 是未来才创建的 owner guideline）；`validate-requirements` 0/0；`decomposition --mode plan` proceed（fr_count=33 ≤ 60）。
- repairs: RS-002/RS-005 Contract cells；requirements Wrap-up 记录缺失 → 驱动者补跑 run-determination/exec-quant/feedback；临时 Goal 首次误写全局 → 删除错误目录并重建 spec-local。全部披露于 checkpoint 01 §Anomalies。
- temporary goal: `.specify/specs/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md`。
- checkpoint: `.specify/specs/086-efficient-test-execution/checkpoints/01-requirements.md`。
- wrap-up records: `.specify/memory/session/20261106T040443Z-run-determination-skill-create-requirements-r20261106t033959.md`、`.specify/memory/feedback/20261106T040443Z-skill-create-requirements.md`、`.specify/memory/exec-quant/records/20261106T040443520576Z-7ea40fdc.json`。
- next: `clarify` dispatch（effective 2 = 1 clarify executor + 1 verifier reserve；临时 Team 待 clarify+plan U4 后创建）。

## U0.5 自检

1. 目标、拓扑、权威、切片、断点已写入状态脊：**是**。
2. 尚未直接编辑目标仓库产品文件（仅创建本状态脊并登记环境级 line registry）：**是**。
3. 未加载 improve-skills/create-skills 维护路径：**是**。
4. 阶段计划（下一阶段 requirements + 本地原生派发形态）已写出：**是**。
5. 085 的 team/concurrency 机制与测试未被本特性改动破坏：**待 U1 核对**；本状态脊已声明保留与实测义务。

## 框架观察

- 暂无（U4/U6 时按三要素记录）。
