# Line State — 076-decision-tension-contract

<!-- loop-state:begin -->
spine_state: running
run_id: r20261029T172918Z-076a
slice: 076
stage: review
stage_started_at: 1793276657
stage_deadline_epoch: 1793282057
stage_base_commit: 7d3ebb58
attempt: 0
retry_limit: 2
last_verdict: implement DONE — 27/27 任务闭合（4 段）；8/8 SC pass 且 sha256 绑定；66 特性契约测试 + 70 邻近守卫绿；零新增命令/依赖/进程；镜像逐字节一致；quickstart S1–S5 实跑；Feature 076 `Planned → Implemented`；下一步 review（过程段 + 代码段）
<!-- plan-fence: decomposition=single-package reason=not-beneficial (27 tasks <= 40, tightly coupled, shared files) test-budget=baseline@implement-start + closure@post-review -->
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

### tasks — DONE（2026-10-29）

- 提交：`920e0f8d`；产物 `tasks.md`（27 行，T001–T027）/ `coverage-baseline.txt`（495 名，base `412b4245b461`）/ 5 份 test-evidence
- 分组：Setup 1 / US1 7 / US2 3 / US3 5 / US4 2 / US5 2 / Polish 7；无 Foundational 相位
- 条款：34 条各认领恰好一次；`account-clause-coverage` status=ok / FR 26/26 / beyond baseline 0
- 门：`validate-tasks` PASS（0 error / 0 warning）；`decomposition --mode tasks` proceed（26 FR / 27 tasks）；`pre-analyze --stage tasks` pass（41 advisories 全为待建文件）
- 偏差：无 `[P]` 行（同文件写读被判非并行安全）；US1 行序重标号一次；两条认领是「实现后守卫」非红先行

### checklist — DONE（2026-10-29）

- 提交：`cde66c0b`；产物 `checklists/readiness-2026-10-29.md`（37 项：27 pass / 10 fail）+ `test-evidence/checklist-stage-checks.md`
- 覆盖：26 FR / 8 SC 全覆盖，100% 带可追溯锚点
- 10 项 fail 及继承面：CHK004 语义拒绝形态无裁决者（T004/T008）；CHK011 方向记号未绑定指标轴（T008）；CHK014 SC-003 夹具的 N/A 保留歧义（T017/T018）；CHK018 断链无真实 ADR 入口（T019/T020）；CHK020 缺章节时双标签重复（T007/T010）；CHK022 逆样本未覆盖六字段逐个删除（T003/T007）；CHK026 attempt 不可重放未被执行（T014/T015）；CHK027 `would_go_red_if` 无机械形态（T012/T015）；CHK029 SC-004 与 FR-021 拒收集不一致（T012/T015）；CHK031 披露局限未落到 owner（T014/T016）
- 零修改面成立：requirements / plan / tasks / contracts 一字未改
- 结构检查：`validate-requirements` ok（287 行 / 34 定义行 / 4 shared strings）

### analyze #1 — BLOCKED（2026-10-29）

- 只读合规：无制品改动、无提交
- 结论：0 CRITICAL / **4 HIGH** / 8 MEDIUM / 4 LOW；按判定口径阻断 implement
- 4 HIGH：
  - **A-01** SC-003「补入不可逆决策后恰 1 条 HIGH」未钉死合规 `N/A` 去留 → 修复面 `requirements.md` SC-003 + US4 AS2、`tasks.md` T017
  - **A-02** 缺章节时 `dtr-anchor` 与 `dtr-section-missing` 双标签同红，无跨标签优先级；六标签「一一对应」措辞不成立 → FR-016 + `data-model.md` E1 R1/R2 + `contracts/validator.md` C-2
  - **A-03** `would_go_red_if` 的「具名红色信号」无机械形状，`tautology` 不可确定性判定 → FR-021 + `contracts/falsification-quartet.md` C-3 + `data-model.md` E5
  - **A-04** SC-004 的六个不合格载荷与 FR-021/T012 的六个拒收原因码不是同一集合，6/6 无法同时成立 → SC-004 + T012 + `quickstart.md` S4
- 8 MEDIUM：A-05 语义拒绝无裁决者；A-06 方向记号未绑定指标；A-07 断链无真实入口；A-08 attempt 可重放无执行者；A-09 逆样本缺跳号/逐字段；A-10 披露局限无承接任务；A-11 `[[STR-NNN]]` 约定空转；A-12 别名白名单与 A3 自相矛盾
- 4 LOW：A-13 引用不存在的 plan 章节；A-14 缺 checklist 阶段记录；A-15 T016 与 SI-3C 现状不符；A-16 覆盖表未标流程行
- 框架观察：验证波派发失败（qodercli SDK auth），4 条 HIGH 均按 objective-analysis-gate rule 7 标记 direct-read，独立验证器确认数 0/4

### analyze #1 修复轮 — DONE（2026-10-29）

- 提交：`16a44ea0 fix(076-decision-tension-contract): remediate analyze #1 findings`
- 16/16 修：4 HIGH（SC-003 夹具三子场景 / 跨标签优先级 / `red:` 机械形状 / SC-004 六原因码 6/6）+ 8 MEDIUM（判定者、方向记号记录性、断链调用面、attempt 复核者规则、跳号夹具、限制承接、STR 约定收窄、别名白名单）+ 4 LOW（引用、checklist 记录、T016 指针核验、流程行标注）
- 计数保持：26 FR / 8 SC / 34 条款 / 27 任务 / 4 STR；`coverage-baseline.txt` 未重冻结
- 门：validate-requirements ok / validate-tasks PASS / account-clause-coverage ok（34 claimed / FR 26/26）/ pre-analyze tasks pass（44 advisories）/ mirrors ok / command copies OK
- `## Plan Edits` 17 行，全部 `minor`，无 substantive

### analyze #2 — PASS（2026-10-29）

- 只读合规；HEAD `16a44ea0`
- 裁决：**0 CRITICAL / 0 HIGH** → 放行 implement；4 MEDIUM / 3 LOW
- 4 HIGH 全关：A-01（SC-003 三子场景）/ A-02（跨标签优先级 + 4+2 划分）/ A-03（`red:` 两半机械形状）/ A-04（六原因码 6/6）
- 遗留 7 条：A-12（别名白名单与 FR-024 自相矛盾，carried）/ A-17（空值双报无优先级）/ A-18（research R-5/R-9 未回填）/ A-19（SC-002/SC-003 缺报告快照承载任务）/ A-20（quickstart「前者」措辞反向）/ A-21（`red:` 切分位置未钉死）/ A-22（「七行」副本与 FR-025「改写」措辞）
- 系统性观察：本轮残留均属「钉主用例、留同类边界」；修复自身连带面未回填

### analyze #2 修复轮 — DONE（2026-10-29）

- 提交：`8a5f7aea fix(076-decision-tension-contract): remediate analyze #2 findings`（16 files，+647/−55）
- 7/7 修：A-12 白名单收为两处（owner 不再写术语注记）/ A-17 第三条优先级（空值与 `none` 只报 `dtr-rejected-form`）/ A-18 research R-5/R-9 回填 + PLAN-EDIT minor / A-19 T017/T026 增 analyze 报告快照步 / A-20 quickstart 措辞纠正 / A-21 `red:` 首次切分 + 双 `red:` 夹具 / A-22 两处计数改指针 + FR-025 措辞
- 计数保持：26 FR / 8 SC / 34 条款 / 27 任务 / 4 STR；baseline 未重冻结
- 六道门全过（输出在 `test-evidence/*-fix2.txt`）

### analyze #3 — PASS（2026-10-29）+ 微修复

- 终裁：0 CRITICAL / 0 HIGH / 1 MEDIUM（A-23）/ 4 LOW（A-24..A-27）→ **放行 implement**
- 7 条遗留全部关闭（A-12/A-17/A-18/A-19/A-20/A-21/A-22）
- 微修复 `d4479500`：A-23 覆盖表补 T026；A-24 标签范围限定；A-25 裸 `N/A` 标为附加断言；A-26 quickstart 抑制条件限定；A-27 features/076.md 非 § 附 别名改工程词
- 计数保持 26 FR / 8 SC / 34 条款 / 27 任务；validate-requirements / validate-tasks / pre-analyze 全过

## Implement 分段计划

- **拆解决策**：`single-package`（reason=not-beneficial）——27 任务 ≤ 40、A/B 共享判据与文件、拆包无收益
- **测试预算**：implement 起点一次全量（`baseline-failed.txt`，后台 b2mkejfup）；中间阶段用定向集；review 后一次 closure 全量
- **分段**（每段 ≤8 任务，串行）：
  1. **P1**：T001–T007（证据槽 / owner 判据段 / 模板锚点 / 校验器骨架）
  2. **P2**：T008–T013（校验器解析与拒绝形态 / analyze 通道 / 四元组 owner 与测试）
  3. **P3**：T014–T020（四元组正文 / 四元组校验器 / SI-3C 核验 / N/A 判据 / ADR）
  4. **P4**：T021–T027（术语与闭合面守卫 / 零新增机制集合差 / 镜像收尾 / quickstart 实跑 / Feature 集成）
- 每段产出：任务行闭合、定向测试、红先行证据、commit；段间由驱动者独立校验后续派发

## 测试预算（E2/E3）

| seq | slot | stage | selection_basis | command | rc | passed/failed | failed_names_path | evidence_ptr |
|-----|------|-------|-----------------|---------|----|---------------|-------------------|--------------|
| 1 | baseline | implement | full-suite | `SPECKIT_PYTHON=<profiles-venv> bash .specify/scripts/bash/run-tests.sh --names-out .specify/specs/076-decision-tension-contract/baseline-failed.txt` | 1（39 既有失败） | 6514 passed / 39 failed / 7 skipped（622.70s） | `.specify/specs/076-decision-tension-contract/baseline-failed.txt`（39 名） | 本行 + 基线文件 |

中间阶段一律用定向集，禁止第二次全量；closure 全量在 review 之后。

### implement P1 — DONE（2026-10-29）

- 提交：`c69dbb81 feat(076-decision-tension-contract): implement T001-T007 with the instruction-surface pointer`
- 闭合任务：T001–T007（证据槽 / 场景 A 契约测试 11 条 / 校验器契约测试 16 条 / owner 判据与门槛段 / plan 模板 `## Decision Tensions` / 校验器骨架与四检查）
- 定向：35 passed / 3 failed（3 条恰为 T008 范围的逆样本：`sacrifice-none` / `undecidable-wording` / `unmapped-measurement-source`）
- 门：`validate-tasks` PASS（34 claims）；`sync-mirrors --check` 六对 ok；`regen-command-copies --check` OK
- **C-11(b) 异常裁决**：新增 `decision-tension.md` 触发 Feature 051 余集断言。C-11(b) 明文禁止第 4 个名字、并明文预期「补指针只会让余集变小」，故**补指令面指针**（`templates/instructions-template.md` § Task Complexity Rubric 一行），**不改 051 契约、不改 `UNPOINTED_BY_STRUCTURE`**；guard 复跑 11 passed
- 生成器实测：`generate-instructions.sh` 为**段级非破坏合并**，已存在节不改写 → live `.specify/instructions.md` 暂不含该行（新项目 init 会带；本仓待该节整段收敛）
- PLAN-EDIT：`templates/instructions-template.md` 一行指针，分类 `substantive`（交付面 +1 行，无 FR/SC/条款/任务增删）

### implement P2 — DONE（2026-10-29）

- 提交：`b99b3670 feat: T008–T013`、`4c532433 test: 三条跨标签优先级守卫`
- 闭合：T008（`expected_sacrifice` 封闭解析 + 第三条优先级 + 两条拒绝标签）/ T009–T011（analyze 第 I 通道 + `seven→eight passes` + 允许差异集）/ T012（四元组契约测试，12 红）/ T013（场景 C，5 红）
- 定向：`17 failed / 37 passed` —— 17 红全部属 T012/T013 设计内，待 T014/T015 实现；五个既有守护套件 70 passed 零新增失败
- 门：validate-tasks PASS；account-clause-coverage ok（34/26/26）；镜像六对 ok；命令副本 OK
- 披露：新增三条优先级守卫（变异验证）；`missing-field` 矩阵取双字段缺失避免重复计数；owner 标题用半角冒号以磁盘为准；四元组 `--json` 信封由测试钉住

### implement P3 — DONE（2026-10-29）

- 提交：`3c1a288c feat(076-decision-tension-contract): implement T014-T020`
- 闭合：T014（四元组小节，只增不改 + 两处限制）/ T015（`validate-falsification-quartet.py`，六原因码 + 首次 `red:` 切分）/ T016（SI-3C 指针形核验，非改写）/ T017（场景 D 三子场景 + 裸 `N/A` 附加断言）/ T018（`N/A` 判据与来源缺失分叉）/ T019（场景 E 断链经 `index_records()`）/ T020（ADR `tension_id` 槽位）
- 定向：三个特性文件 **60 passed / 0 failed**；P2 遗留 17 红全清；邻近守护 71 passed
- 门：validate-tasks PASS；镜像六对 ok（scripts 117）；命令副本 OK
- 披露：`verification.md` 在 T016 种下，8 条 SC 置 `unknown`（不预支结论）；四元组键重复归 `missing-field`（封闭集无第七原因）

### implement P2–P4 — DONE（2026-10-29）

- P2 `b99b3670` + `4c532433`：T008–T013（`expected_sacrifice` 解析 / 三条优先级 / analyze 第 I 通道 / 四元组与场景 C 测试）
- P3 `3c1a288c`：T014–T020（四元组 owner 小节 / 四元组校验器 / SI-3C 指针核验 / 场景 D 三子场景 + 裸 N/A / `N/A` 判据 / 场景 E / ADR `tension_id`）；三个特性测试 60 passed / 0 failed
- P4 `84de4ddf` + `7d3ebb58`：T021–T027（场景 F/G 守卫 / 零新增机制集合差 / 术语复测 / 镜像收尾 / 闭合面终判 / quickstart S1–S5 / Feature 集成）；**Feature 076 → Implemented**
- 终验：0 open tasks；8/8 SC pass；66 特性契约测试 + 70 邻近守卫绿
- 披露：tasks.md T027「状态保持 Planned」与状态机 owner 冲突 → 裁决 void 并就地标注；SC-002/SC-003 快照是「程序 verdict 在通道 HIGH-or-0 映射下的渲染」，`/speckit.analyze` 叙事层未整链跑，无 SC 依赖它；四元组键重复归 `missing-field`

## 框架观察

（U4/U6 时补记：现象 / 框架位置 / 对驱动的影响。）

## Wrap-up

（per-stage 记账指针在 U4 写入。）
