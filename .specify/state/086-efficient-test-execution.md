# Line State — 086-efficient-test-execution

<!-- loop-state:begin -->
spine_state: running
run_id: r20261106T033959Z-086a
slice: 086
stage: implement
stage_started_at: 1793940960
stage_deadline_epoch: 1793951760
stage_base_commit: 3855f2fb
attempt: 0
retry_limit: 3
last_verdict: analyze U4 pass (read-only; 1 CRITICAL / 5 HIGH / 13 MEDIUM / 5 LOW); implement blocked; driver repair pass in progress (C-01 contracts, H-01 085 carve-out, H-02..H-05)
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
- **临时 Team（085）**：**已创建** `.specify/specs/086-efficient-test-execution/team/086-efficient-test-execution/team.md`（`scope: spec`、`goal_slug: 086-efficient-test-execution`、8 个 stage_seats、14 个 seats、`config.agent_concurrency` 24 requested / 18 effective、`isolation: worktree`、checkpoint policy standing）；schema 校验通过。
- **085 live status exception（T041）**：只允许更新 `.specify/specs/085-sdd-temporary-goal-team/verification.md` 的 SC-010 status 行；由 FR-030/A12/A17 授权（live reference），不得扩散到 085 的 goal/team/checkpoints/contracts/history。最终验证须证明只改了 SC-010 行。
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

## U4 clarify（2026-11-06T04:12Z）

- sentinel: `CLARIFY-DONE`；stage commit `fee3f874`；branch `086-efficient-test-execution`；base `3afe10df`。
- mode: A（post-requirements；`plan.md` 不存在）；target `requirements.md`；writability probe `WRITABLE:true`；MODE=A。
- artifacts:
  - `requirements.md`：§ Related Feature 绑定 Feature 086；§ Clarifications 追加 4 条 Q/A（共 10 条）；§ Assumptions 新增 A13–A19；FR-024 补四个并行开关字面量（无 FR/SC 计数变化）。
  - `checklists/requirements.md`：Feature Scope 与行数注记同步到绑定后状态（332 行；FR/SC/STR 不变）。
  - `test-evidence/clarify-gates.txt`：覆盖率扫描、绑定记录、门禁原始输出、overlap 裁决、in-passing repairs、框架观察。
  - `features.md` row 086 / `features/086.md`：绑定记录；`Related Specifications/Requirements` 一节；状态保持 `Draft`。
- clarifications（自裁，无用户提问）：
  1. 默认并发：`-n auto` + `--dist load`；优先级 `--workers` > `SPECKIT_TEST_WORKERS` > `auto`；不重复注入调用者 `-n`/`--numprocesses`；`PYTEST_XDIST_WORKER` 存在时自动串行；xdist 缺失时串行 + 具名 stderr 回退；cap/loadfile 只在实测证据后调整（A13）。
  2. watch-target 唯一新增失败：优先具名可枚举串行标记 + 运行器仍产出完整一份 `--names-out` 清单与单一退出码；仅当无法保真时用测试级、有实测依据的超时上调；禁止 skip/xfail/静默全局串行（A14）。
  3. 原则落点：标题 `Efficient Test Execution (Concurrent by Default)`；template XIX / live XX；版本 1.16.0→1.17.0；instructions 章节插在 `## Single-Run Evidence Discipline` 后；计数 19/20/12、watchlist 7、章节 33/34；预算仅在实测超过 34,816 B 时调整；镜像重新生成。
  4. 收口比较：名称差集对实现起点 SDD 基线槽位，双向记录新增/消失；19 个串行既存失败按名称排除；最终并行收口新增名必须为 0；消失项不追认为修复。
- gates: `validate-requirements` ok（332 行 / 45 definition rows / 7 STR，0 error / 0 warning）；`pre-analyze --stage requirements` pass errors=0 advisories=1（未来 owner guideline）；`decomposition --mode plan` proceed（fr=33 ≤ 60）；`flow-class` execution / declaration；`overlap-check` clear（checked=1, overlaps=0, note: no declaration artifact）。
- overlap 裁决：067 RC-03 与 085 保留面是**概念边界**而非文件级重叠，已在 requirements § Boundary and Ownership 记明；067 结论未改写；`git diff --name-only -- .specify/specs/085-sdd-temporary-goal-team` 为空。未静默清除任何 overlap。
- 085 dogfood：requested 24；clarify effective 2（1 executor + 1 verifier reserve，按 checkpoint 01）；临时 Team 仍待 clarify + plan U4 后创建（085 C-008）；085 goal/team/checkpoints/contracts/历史零改动。
- in-passing repairs：checklist 与 feature registry 的“待 clarify 绑定”注记、requirements-stage 行数注记更新为绑定后事实；无 FR/SC 增减、无状态翻转。
- wrap-up records：run-determination `skill:clarify-artifact` + `/speckit.clarify`；exec-quant 两条；feedback 两条；`should_prompt=true`（282/283 ≥ 10，非阻断通知，未自动发送）。
- docs sync eval：`无需记录`（clarify 只收敛既有规格，无用户可见能力变化）。
- next: `plan` dispatch（driver；临时 Team 在 clarify+plan U4 后创建）。

## U4 clarify（2026-11-06T04:13Z）

- sentinel: `CLARIFY-DONE`；stage commits `fee3f874` + `554d8333`。
- Feature 086 已绑定（无新建/改号）；4 条自裁 Q/A + A13–A19；FR-024 增加 `-n`/`--numprocesses`/`--dist`/`--maxprocesses`。
- driver independent re-runs: `overlap-check` clear（checked=1, overlaps=0）；`validate-requirements` 0/0；`pre-analyze --stage requirements` pass（advisories=1 future owner guideline）。
- 085 diff in `3afe10df..HEAD` = empty；Wrap-up records present（session/feedback for `skill:clarify-artifact` and `speckit:clarify`）。
- checkpoint: `.specify/specs/086-efficient-test-execution/checkpoints/02-clarify.md`。
- next: `plan` dispatch（effective 2 = 1 plan coordinator + 1 verifier；carrier `SDD Executor`；临时 Team 待 plan U4 后创建）。

## U4 plan（2026-11-06T04:23Z）

- sentinel: `PLAN-DONE`；stage commit `67bbae51`。
- artifacts: `plan.md` / `research.md` / `data-model.md` / `feature-ref.md` / `quickstart.md` + 4 contracts；Feature 086 Draft → Planned。
- driver independent gates: `pre-analyze --stage plan` pass errors=0 advisories=25（均为未来交付路径）；`validate-requirements` 0/0；`decomposition --mode plan` proceed（fr=33 ≤ 60）。
- 085 diff `3afe10df..67bbae51` = empty；plan stage Wrap-up records present（session/feedback for `speckit:plan` and `skill:create-plan`）。
- temporary Team: `.specify/specs/086-efficient-test-execution/team/086-efficient-test-execution/team.md` — `scope: spec`、`goal_slug: 086-efficient-test-execution`、8 stage_seats、14 seats、`agent_concurrency` 24/18、`isolation: worktree`、checkpoint standing；schema check passed。
- checkpoint: `.specify/specs/086-efficient-test-execution/checkpoints/03-plan.md`。
- next: `tasks` dispatch（effective 2 = 1 task executor + 1 verifier；team tasks max_parallel 12 not binding）。

## U4 tasks（2026-11-06T04:41Z）

- sentinel: `TASKS-DONE`；stage commit `f3105c98`。
- artifacts: `tasks.md`（50 tasks / 9 phases；52/52 contract clauses；Tests Mode ON；GATE-086 + GATE-1…8）、`coverage-baseline.txt`（575 行，base `0f4b203e`）、`test-evidence/tasks-gates.txt`。
- driver independent gates: `validate-tasks` PASS 0/0；`decomposition --mode tasks` proceed（33 FR / 50 tasks ≤ 60/80）；`pre-analyze --stage tasks` pass（errors=0, advisories=39 future paths）。
- 085 diff `67bbae51..f3105c98` = empty；T041 为 085 `verification.md` SC-010 live-status 单点例外（FR-030/A12/A17）。
- accounting: tasks stage session records present；driver filled `skill:create-tasks` feedback/exec-quant；`speckit:tasks` feedback skipped because the engine expects `/speckit.tasks` and the skill identity satisfies U4.
- checkpoint: `.specify/specs/086-efficient-test-execution/checkpoints/04-tasks.md`。
- next: `checklist` dispatch（effective 2 = 1 checklist executor + 1 verifier）。

## U4 checklist（2026-11-06T04:46Z）

- sentinel: `CHECKLIST-DONE`；stage commit `5cbc757b`。
- artifact: `checklists/requirements-quality-2026-11-06.md`（44 CHK，44/44 traceable）；`test-evidence/checklist-gates.txt`（13 probes）。
- driver U4: no source/template/test/085 edits；worktree clean；checklist stage 未留 Wrap-up → driver 补跑 `skill:create-checklist` 的 run-determination/exec-quant/feedback。
- findings handed to analyze: CHK017（FR-027/FR-030 085 live-status carve-out）、CHK036（PYTHONPATH 前提）、CHK007/CHK008（two-pass/mode 未进 FR）。
- checkpoint: `.specify/specs/086-efficient-test-execution/checkpoints/05-checklist.md`。
- next: `analyze` dispatch（effective 2 = 1 analyze executor + 1 verifier）。

## U4 analyze（2026-11-06T04:56Z）

- sentinel: `ANALYZE-DONE`；只读，无 requirements/plan/tasks/contracts/source/test/085 改动。
- findings: **1 CRITICAL / 5 HIGH / 13 MEDIUM / 5 LOW**；digest `test-evidence/analyze-findings.md`。
  - C-01：四份契约无 FR 引用组，`account-clause-coverage` 0/33；必须先修。
  - H-01：FR-027/FR-030 的 085 live-status carve-out 未落 requirements，且 C-041/GATE-5/M-16/team/WP-C2/R-8 字面禁止 T041。
  - H-02：PYTHONPATH 是 run-derived SC 的未声明前提。
  - H-03：M-8…M-15/M-18/M-19 无任务；T042 错位。
  - H-04：baseline 在 T014（源码改动后）迟到；须移到 T001a。
  - H-05：计划 ≥9 次全量 vs 两槽位；缺 out-of-slot-exception；closure names 路径不符 TB-04。
- repair pass: 驱动者按 findings 修复 artifacts；先 C-01，再 H-01/H-04/H-05/H-02/H-03 与 M/L；随后重跑 validate/coverage/pre-analyze/decomposition，再派发 implement。
- checkpoint: `.specify/specs/086-efficient-test-execution/checkpoints/06-analyze.md`。
- next: repair pass → implement（plan-first wave WP-A1…A4 + WP-B1…B3，planned effective 10；WP-C after）。

## U0.5 自检

1. 目标、拓扑、权威、切片、断点已写入状态脊：**是**。
2. 尚未直接编辑目标仓库产品文件（仅创建本状态脊并登记环境级 line registry）：**是**。
3. 未加载 improve-skills/create-skills 维护路径：**是**。
4. 阶段计划（下一阶段 requirements + 本地原生派发形态）已写出：**是**。
5. 085 的 team/concurrency 机制与测试未被本特性改动破坏：**待 U1 核对**；本状态脊已声明保留与实测义务。

## 框架观察

- **requirements scaffold 短暂创建 `087-` 分支（2026-11-06，A19a）**：脚本在正确 `086` 分支之前短暂创建了 `087-` 分支，随后由驱动清理并以 `086` 重建。本特性不修改该脚本；建议 improve 流程复核编号推导顺序。
- **宿主阶段 agent 承载降级（2026-11-06，A19b）**：宿主未暴露 085 的阶段 agent 类型；requirements 以 `SDD Requirements Executor`、clarify 以宿主原生 `general-purpose` 承载 `sdd-clarify-analyzer` 角色。085 的 team/concurrency/checkpoint 机制仍被使用；此承载降级不记为 085 失败，登记为观察。
