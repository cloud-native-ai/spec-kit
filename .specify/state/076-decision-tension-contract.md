# Line State — 076-decision-tension-contract

<!-- loop-state:begin -->
spine_state: running
run_id: r20261029T172918Z-076a
slice: 076
stage: tasks
stage_started_at: 1793267858
stage_deadline_epoch: 1793273258
stage_base_commit: 246eba85
attempt: 0
retry_limit: 2
last_verdict: plan DONE — 8 contracts / 34 clauses；FR 26/26；宪法 18 行全 Pass；pre-analyze pass；镜像与命令副本 clean；DTR 试点 2 条；wrap-up 由驱动者补跑
<!-- loop-state:end -->

- line_id: `076-decision-tension-contract`
- run_id: `r20261029T172918Z-076a`
- project_dir: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- repo_root: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- worktree: `none（本地拓扑，单工作区）`
- base_sha: `ac63fe8c`（Feature 076 立项提交）
- trunk: `master`（`docs/git-workflow.md` 声明；`main` 是上游世系，不参与合并）
- topology: `local`（宿主原生子代理；MUST NOT 启动 qodercli）
- state: `running`

## U0 入口声明

- **目标项目**：spec-kit 框架源码仓（本地 `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`，`.specify/` 存在且合法）
- **执行拓扑**：本地（宿主原生子代理；阶段派发不启动 qodercli）
- **终态权威文档**：`.specify/memory/features/076.md`（Feature 详情，含 A+B 范围与术语裁决）、`.specify/memory/constitution.md`（合规底线）、`.specify/instructions.md`、`docs/concepts/prompt-to-graph.md` §6（缺口一 counter-metric）、`shared/guidelines/critique-and-self-critique.md`（B 的既有 owner）、`shared/definitions/derivation-definitions.md` §Contradiction Handling（形态先例）、`08_工具开发/artifacts/designs/speckit-decision-dialectic/research-report.md`（外部证据与拒收项）
- **特性切片**：Feature 076 = A（计划阶段决策反题与反指标契约 DTR）+ B（SI-3C 证伪执行化）。**不拆片**：A/B 各自独立可测，但共同服务同一判据（决策/提案必须能被证伪或被代价约束），且 A 的结构校验与 B 的四元组共享 `would_go_red_if` 语义；FR 预算控制在 ≤30，任务 ≤40。
- **用户裁决（2026-10-29）**：① 立项 A+B；② 允许「矛盾论」作为**仅供内部理解**的别名，对外一律工程词；③ 立项后由本 skill 无人值守推进到 review 并合并 master。
- **断点**：U1 自动探测（结果见下）→ `requirements`
- **阶段计划**：`requirements → clarify → plan → tasks → checklist → analyze → implement → review → closure（review 后全量）→ 工作树清扫 → 本地合并 master`；全程本地原生子代理，不启动 qodercli
- **快车道**：入口未声明 `fast-lane=opt-in` → **完整链**，checklist 必经，不启用快车道块
- **拆解开关**：`decomposition: auto`；`decomposition_stages: plan=auto, implement=auto, review=auto`；`decomposition_slot_cap: 2`
- **测试预算**：implement 起点一次全量 baseline；review 后一次 closure 全量；中间阶段用 targeted set（`efficiency-model.md` §2.3）
- **Plan 只小修**：`PLAN-EDIT:` 声明制，tasks 之后对 plan-owned 面的实质改动须走两分支处置
- **合并**：本地合并（缺省）；**不 push**（用户未授权）

## U1 断点探测（2026-10-29 17:29）

| 探测项 | 实测 |
|--------|------|
| 当前分支 | `076-decision-tension-contract`（自 `master` @ `26731b67` 切出） |
| HEAD | `ac63fe8c docs(076-decision-tension-contract): register Feature 076 (Draft)` |
| Feature 注册 | `.specify/memory/features.md` 第 85 行已登记 076（Draft），Total Features 72 |
| Feature 详情 | `.specify/memory/features/076.md` 存在 |
| spec 目录 | `.specify/specs/076-decision-tension-contract/` **不存在** |
| 编号冲突核查 | `.specify/specs/075-sdd-loop-efficiency/` 已被占用（Feature 058 的演化 spec），故立项编号由 075 实改为 **076** |
| 结论 | **断点 = requirements**（首个待跑阶段） |

## 阶段计划（逐阶段门）

| # | 阶段 | 派发形态 | U4 门 |
|---|------|---------|-------|
| 1 | requirements | 本地原生子代理 | `pre-analyze-check --stage requirements` pass；`decomposition-check --mode plan` ≠ split-required |
| 2 | clarify | 本地原生子代理 | `overlap-check --spec-dir` clear（跨特性重叠裁决） |
| 3 | plan | 本地原生子代理 | `pre-analyze-check --stage plan` pass |
| 4 | tasks | 本地原生子代理 | `decomposition-check --mode tasks` ≠ split-required；`pre-analyze-check --stage tasks` pass |
| 5 | checklist | 本地原生子代理 | 清单文件落盘 + 记账 |
| 6 | analyze | 本地原生子代理（只读变体） | CRITICAL/HIGH 阻断须修复复跑；记账三步照跑 |
| 7 | implement | 本地原生子代理 | tasks 全 `[X]`/`[~]`；`verification.md` 逐 SC 状态；测试预算 E2/E3 |
| 8 | review | 本地原生子代理 | 过程段 + 代码段；`code-review.md` 无 `blocking` |
| 9 | closure | 驱动者亲自 | review 后一次全量；工作树清扫；本地合并 `master` |

## 阶段记录

### requirements — DONE（2026-10-29）

- 提交：`da7256e1` → `1b426e1a` → `0518c7ef`
- 产物：`.specify/specs/076-decision-tension-contract/{requirements.md,checklists/requirements.md,test-evidence/}`
- 计数：26 FR（≤30）/ 8 SC / 5 user stories / 4 shared strings
- 确定性门：`decomposition-check --mode plan` = proceed；`pre-analyze-check --stage requirements` = pass（errors=0 / advisories=2，均为本特性将新建的 `shared/guidelines/decision-tension.md`）
- 独立校验：哨兵 ✓ / 产物 ✓ / 纪律（未 push、未提交脏文件）✓ / Wrap-up 由驱动者补跑 ✓
- 偏差：A1 脚手架分支动作被抑制；A2 编号 075→076；A4 绑定提前到 requirements
- Related Feature：绑定 076（reuse-first 六候选逐条核验，A 无既有 owner、B 的 owner 未被任何 Feature 收编）

### clarify — DONE（2026-10-29）

- 提交：`2c208998`（requirements.md 单文件）+ `80d26698`（wrap-up 记录与状态脊）
- 六处裁定：① 模板锚点 = Constitution Check 直接后继；② analyze 只判当前 spec 的 plan.md，历史计划无豁免、无 advisory 档；③ 校验器 `scripts/python/validate-decision-tensions.py --spec <dir> [--json]`，退出码 0/1/2，六个封闭检查标签；④ `expected_sacrifice` 封闭语法 `<SC-NNN> Source <↓|↑>`；⑤ 四元组拒收由 `scripts/python/validate-falsification-quartet.py` 确定性判定，六类拒收原因；⑥ 七行镜像对（工具命令副本面为空）
- 回修 FR：008 / 009 / 010 / 011 / 016 / 021 / 025；计数不变 26 FR / 8 SC / 4 STR
- 门：`validate-requirements` ok（287 行 / 34 定义行）；`overlap-check` clear；`pre-analyze --stage requirements` pass（6 expected advisories，均为待建文件）
- 披露：两处语义判据被换成形状判据（`raw:` 标记代理「非转述」、反引号输入 + 具名红色信号代理「反空真」）；脚本不重放 `attempt`

### plan — DONE（2026-10-29）

- 提交：`246eba85`；产物 `plan.md` / `research.md`（R-1…R-11）/ `data-model.md`（E1–E8 + 6 校验规则 + 6 状态迁移）/ `contracts/` 8 文件 34 条款 / `quickstart.md`（5 场景）/ `feature-ref.md` / `test-evidence/`（6 份）
- 门：`pre-analyze --stage plan` pass（errors=0 / advisories=25 全是待建文件）；镜像六对 ok；命令副本 OK；宪法 18 行全 Pass；定向 70 passed
- 结构：`## Constitution Check` → `## Decision Tensions` → `## Project Structure` 三行相邻（FR-008 锚点已在本计划内生效）
- DTR 试点：T-001（四元组判定者＝确定性脚本 vs agent，expected_sacrifice = `SC-004 Source ↓`）、T-002（封闭文法 vs 自由文本，`SC-002 Source ↑`），六字段齐备、反题为可独立采纳方案
- 偏差：`create-new-plan.sh` 因缺 `CWS_LIB_BASH_HOME` 退出 1（未产生分支动作）；模板尚无该章节属本特性待实现面；同作者门按 direct-read 标记回退；pytest 走 profiles venv

## 框架观察

（U4/U6 时补记：现象 / 框架位置 / 对驱动的影响。）

## Wrap-up

（per-stage 记账指针在 U4 写入。）
