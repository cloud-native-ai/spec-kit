# Analyze Report — 088-speckit-visualization（/speckit.analyze，2026-11-06）

**Unit**: `/speckit.analyze` · **Run ID**: `r20261106T040353Z-087a` · **Stage**: analyze（Round 1）
**Spec dir**: `.specify/specs/088-speckit-visualization`（`REQUIREMENT_ID=087`，`FEATURE_ID=087`，`MODE=C`）
**Flow class**: `execution` / `source=declaration`（`flow-class-check.py --action lookup --unit-id "spec:088-speckit-visualization"` → exit 0；非表达类，既有门禁集不变）
**Prior report**: 无（本特性首次 analyze，rerun delta = N/A）
**性质**: 严格只读。本报告是本阶段唯一写入产物；requirements / plan / tasks / contracts / data-model / quickstart / checklists / 注册表零修改。

## 0. 门禁结论（Gate Verdict）

**未通过（FAIL）**：1 条 CRITICAL（宪法冲突，不可降级）+ 3 条 HIGH 未处置。

| 严重度 | 条数 | 处置要求 |
|--------|------|----------|
| CRITICAL | 1 | 必须在 `/speckit.implement` 前修复；归属 **plan**（contracts / data-model / quickstart），并连带 tasks 的 T043 措辞 |
| HIGH | 3 | 同上；归属 **plan**（F-01）、**requirements**（F-02）、**requirements + plan**（E-01） |
| MEDIUM | 13 | 不阻断实施；建议在对应阶段一并收敛（逐条给出归属阶段） |
| LOW | 5 | 建议性 |

说明：驱动者要求「未处置 CRITICAL/HIGH → 报告逐条给出归属阶段与建议修复」，本文 §2.1–§2.4 逐条满足。

### 0.1 验证波状态（显式降级，非静默）

- **同一作者门（objective-analysis-gate）**: **未触发**——requirements/clarify/plan/tasks/checklist 由本无人值守链的**其它阶段运行**产出，本 analyze worker 未在本会话撰写它们（gate owner: `.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires，第二条）。
- **CRITICAL/HIGH 独立验证子代理**: **不可派发**（本层为 bounded assignment，brief 明确禁止派发子代理）。按 SKILL `validation-and-report.md` § Subagent-unavailable fallback 执行**直接受限重读**，每条 C/H 行标注 `(validated: direct re-read, subagent unavailable)`，并给出 evidence_supported / evidence_not_supported 边界。
- **降级率**: n/a（无第三方 validator）；**读侧一致性**: 本报告每条 C/H 断言均由 §2 引用的原文逐字支撑，未引用推断。
- **只读证明**: 本报告写入前 `git status --porcelain` 的既有脏文件集合在本报告写入后不变（报告本身是新文件）；本轮未运行任何写命令、未 `--freeze`、未改状态脊。

## 1. 方法与执行轨迹

| 步骤 | 命令 / 动作 | 结果 |
|------|-------------|------|
| 前置脚本 | `bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` | exit 0；`AVAILABLE_DOCS` 含 research/data-model/contracts/quickstart/checklists/feature-ref/tasks |
| 类别读取 | `flow-class-check.py --action lookup --unit-id "spec:088-speckit-visualization"` | `flow_class: execution`，`source: declaration` |
| 覆盖核算（固定步骤） | `python3 .specify/scripts/python/account-clause-coverage.py --spec .specify/specs/088-speckit-visualization`（**未** `--freeze`） | `status: baseline-missing`；`claimed clauses 36`；`[fr-uncovered] fail (20)`；`[clause-uncovered] fail (589)`；`[clause-unparsable] warn (107)` → §5、E-04、E-05 |
| 确定性校验 | `validate-requirements.py` | `status: ok`，六标签全 pass，0 error 0 warning |
| 确定性校验 | `validate-tasks.py tasks.md` | `PASS (with warnings)`：0 error / 13 warning（9 green-cross-phase + 4 green-path-divergence，作者已在 tasks.md § Dependencies 裁决） |
| 确定性校验 | `validate-decision-tensions.py --spec … --json` | `status: ok`，六标签 0 命中 |
| 确定性校验 | `pre-analyze-check.py --spec-dir … --stage tasks` | `decision=pass errors=0 advisories=0`，`fr=22 sc=10 tasks=50` |
| 检测通道 A–I | 逐产物交叉读（§2） | 22 条 findings |
| 检查清单 H 通道 | 60 条逐条分诊（§3） | 17 条 `[Gap]`：6 covered-by + 11 raised，`undispositioned=0` |

**读入的权威面**：requirements.md（22 FR / 10 SC / 15 假设 / 12 边界情形 / 5 条澄清裁决）、plan.md（19 行宪法检查 / T-001–T-002 / EP-001–EP-009 / D1–D12 / 9 行 Mirror Obligations）、tasks.md（50 行，T001–T046 + T051–T054）、contracts ×6（52 条款 C-01…C-52）、data-model.md（E1–E7 + INV-01…INV-12）、quickstart.md（A–H）、checklists ×2、feature-ref.md、`features.md` 087 行、`features/088.md`、`constitution.md` v1.16.0（19 原则）。

## 2. Findings

`propagation_surface` 是每条的第一个字段，severity 由它派生（owner: `objective-analysis-gate.md` rule 3）。`none` 行按规则封顶 MEDIUM。

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| D-01 | D 宪法对齐 | 计划产物（contracts → data-model → quickstart）→ 守卫实现 | **CRITICAL** | `contracts/reporting-obligations.contract.md:102`（C-09）；`contracts/status-digest.contract.md:96`（C-46）；`quickstart.md:204` | 十三条 RO 命题清单有两个定义点且 RO-09 主体相反：C-09 定义「RO-09 = 摘要契约」，C-46 定义「RO-09 = 行集携带 profile 与切换记录」。这是 Principle XIV（枚举/清单唯一 owner）的 MUST 冲突；plan.md § Constitution Check 第 XIV 行因此断言 Pass 不成立 | 指定唯一 owner（建议 C-01…C-13 的标题清单），把 C-46 表格改为按 RO-id 引用 + 只写「what it reads」而不再重述主体；同步 quickstart F 前提 1 的「one vocabulary」断言 |
| F-01 | F 不一致 | 守卫实现（T033/T043）与 contract tests | **HIGH** | `contracts/status-report.contract.md:22,43,55,106`；`contracts/supervision-report.contract.md:28`；`data-model.md:164,165,170,173,175`；`tasks.md:189` | 8 处「Judged by」/INV 映射指到主体不同的命题：C-22（归因）→RO-08、C-24→RO-09、C-25（触发器）→RO-09、C-30（profile）→RO-09（与 C-09 相反）、C-33（存在性闭包）→RO-11；INV-01→RO-07（应 RO-05）、INV-02→RO-08、INV-07→RO-11（应 RO-06）、INV-10→RO-12、INV-12→OM-05（应 OM-04/C-50）；T043 把 RO-09 槽位写成「profile plus recorded switch」 | 以唯一 owner 为准逐条改指针；`INV-10` 的 cap 命题在 13 条中无槽位，需新增 DG 命题或明确挂到 RO-05；T043 明确「RO-09 判什么」 |
| F-02 | F 不一致 | SC-003 → verification.md → GATE-4 | **HIGH** | `requirements.md:317`（SC-003）vs `:230-232`（FR-009）、`:98-100`（US2 AS2）、`contracts/supervision-report.contract.md:37-44`（C-35） | SC-003 写「marks the one **below** the declared stall threshold as stalled」，与 FR-009「below threshold = slow，beyond = stalled」、C-35「below → **slow**，not stalled」方向相反；SC-003 是 final-path 验收判据，据此验收会断言错误方向 | 改 SC-003 为「silence **beyond** the declared stall threshold → stalled，just-under fixture → slow」，与 US2 Independent Test 的「stalling past the declared threshold」对齐 |
| E-01 | E 覆盖 | 交付集 → 守卫 RO-04 → GATE/SC-002/SC-009 | **HIGH** | `contracts/status-digest.contract.md:91`（RO-04）；`requirements.md:220-223`（FR-006）、`:378-381`（A7）；`tasks.md:66`（T003）、`:172`（T035）、`:113`（T018）；`feature-ref.md` § Delivered paths（28 行） | RO-04 的默认群体是 `.specify/teams/*/team.md`（现测 12 个，**0** 个含 `reporter`），而 FR-006 只约束「created through the team-creation entry」；A7 承诺既有 team 不会「unrunnable」靠的是逐 team 记录 reason——那需要改 12–13 个 roster 文件，而 28 条交付路径里没有任何 `.specify/teams/*` 路径，DoD-1 也不覆盖它们。结果：T037/T044 跑守卫时 RO-04 必然 fail，且没有任务认领修复；T035 还要求「population read from the T003 baseline」，而 T003 只记录两个计数（12 / 1），不是名单 | 在 requirements/contracts 二选一：把 RO-04 的群体收敛为「本次创建/修改的 roster + 显式传入路径」，或把 12 个既有 roster 的 `reporting-reason` 回填列入交付路径与任务；同时把 T003 的基线改成名单形式 |
| A-01 | A 重复 | requirements（无下游继承：C-24/E6 已选定一种读法） | MEDIUM | `requirements.md:209`（FR-003）、`:271`（FR-020）、`:30`、`:47`、`:50`、`:343`、`:361`、`:466-470` | 30 秒缺省在 requirements 内出现 9 次（含两条规范 FR，且 FR-003 的「every in-scope structure … default 30 s」与 FR-020 的「long-run 档仅在存在 live receiver 时使用」在适用范围上冲突）；A6 自己声称「a single declared literal and is referenced, never copied」。**事实纠正**：CHK052 所述「SC-006 也写了该数字」不成立——SC-006 只写「the default cadence value」，未出现 30 | 保留 FR-020 为唯一规范值来源，FR-003 改为「by the profile FR-020 selects」；SC-006 补一句「universe = framework sources（`shared/ templates/ skills/ agents/`）」，与 EP-008/T034 一致 |
| C-01 | C 欠指定 | status-digest 脚本（DG-04 判定）→ 实现 | MEDIUM | `requirements.md:319`（SC-005）、`:236-240`（FR-011）；`contracts/status-digest.contract.md:53-57`（C-44）；`data-model.md:105,118`；`tasks.md:151`（T027）、`:154`（T030） | 「declared stale bound」没有声明点：cap 有 owner（C-47 末行指派脚本常量），stale bound 既无 owner 也无数值来源，T027/T030 只能自行发明 | 在 C-47 的 ownership 表增加一行「stale bound default → `scripts/python/status-digest.py` 常量」，或在 owner 文档声明并让 data-model E5 引用 |
| C-02 | C 欠指定 | 摘要实现（T030）→ SC-005 | MEDIUM | `requirements.md:236-240`（FR-011）、`:400-403`（A11）；`data-model.md:142-158`（E7） | 多项目场景未定：注册表是 per-user 目录（entry 带 `project_dir`），摘要按目录解析后会把别的项目的 line 一并列出，而没有任何 requirement/contract 规定「只看当前项目 / 全看并标注」 | 在 FR-011（或 owner 的摘要契约）加一句 workspace 规则：默认只列 `project_dir == 当前工作区` 的条目，其余以 `other-project` 标注或排除 |
| C-03 | C 欠指定 | 席位守卫（T013）→ SC-002 | MEDIUM | `data-model.md:30,166`（E1 / INV-03）；`contracts/reporting-obligations.contract.md:56-58`（C-04）；`contracts/reporter-seat.contract.md:39-59`（C-16/C-17）；`tasks.md:105`（T011）、`:107`（T013） | data-model 说「Two reporter rows is a named defect」，但 C-16 的具名缺陷只列「缺席位 / agent 不可解析」，T011 的三组 fixture 与 T013 的接受逻辑都没有两席位情形——两席位 roster 会通过守卫 | 把「两席位 = 具名缺陷」写进 C-16 的缺陷集，并在 T011 fixture 与 T013 判定中加入该分支 |
| C-04 | C 欠指定 | owner 文档（T008）声明面 | LOW | `requirements.md:208-210,270-274,165-168`；`tasks.md:87`（T008 清单） | 四个 owner 级口径缺 requirement 锚点：① idle tick 是否可抑制（无文字，而 T043 的「suppressed tick」mutation 隐含「不得抑制」）；② long-run 档的计时锚点（start / previous tick / boundary）；③ 阈值与周期的数量关系（阈值 < 周期时首 tick 即 stalled）；④ 宿主时钟跳变/挂起时「tick 序列缺口」与「reporter 停滞」如何区分 | 在 owner 文档把这四条各写一句声明（T008 的清单相应加 4 项），不必改 FR |
| C-05 | C 欠指定 | 行级策略（owner + 渲染器） | LOW | `requirements.md:174-175`（预算耗尽）、`:253-255`（FR-016）、`:241-243`（FR-012）；`contracts/status-report.contract.md:91-97`（C-29） | 三条行级策略缺声明：① `reporter-failure` 行是否也须携带四要素（INV-01 说「every Status Report」，RO-05 对「captured line set」逐行检查，二者可能冲突出红）；② 派发载荷缺 reporting 字段时的失败模式（C-40 只说「carries by injecting」）；③ 预算耗尽「仍然报告」只有 Edge Case，无 FR/契约条款 | 在 C-29 明确 failure 行的最小内容，在 C-40 增加一个具名条件，并把预算规则升为一句契约条款 |
| C-06 | C 欠指定 | owner 文档（C-11/RO-11） | LOW | `requirements.md:253-255`（FR-016）、`:185-188`（Edge Case）、`:415-421`（A15）；`contracts/reporting-obligations.contract.md:120-127`（C-11） | FR-016 未界定「whose reporting loop」：reporter 自身死亡时它无法自报，A15/Edge Case 把它交给编排者的既有 liveness 信号；而 C-29 的 `reporter-failure` 行是「本流程自身无法发射」时的产物。两种读法并存，FR-016 文本未择一 | FR-016 加一个限定语（「the emitting flow's own loop; a reporter that stops growing is judged by the visibility contract's liveness signal」），或让它直接指向 A15 |
| E-02 | E 覆盖 | tasks → implement 的验证面 | MEDIUM | `tasks.md:109`（T015 `[covers:]`）、`:136`（T053）、`:110`（T017，实现但未 `[covers: FR-016]`）、`:49`（格式规则） | FR-021 **没有任何 `[covers:]`**（只在 T015 描述文字里出现）；FR-016 唯一的 covers 行 T053 验的是「触发器 + profile 切换」，**不验** reporter-failure 具名条件（真正实现者是 T017，其 covers 为 FR-010/FR-020）。按 tasks.md 自己声明的机器口径（line 49），两条需求的认领是错误的 | T015 加 `[covers: … FR-021]`；T017 加 FR-016 或把 T053 的 covers 改成 FR-010/FR-020 并新增一条验 reporter-failure 的行 |
| E-03 | E 覆盖 | tasks 覆盖台账 → analyze/implement 门 | MEDIUM | `tasks.md:223`（15/37 声明）、`:276`；`contracts/reporter-seat.contract.md:61`（C-18）、`:13`（C-14）；`tasks.md:105`（T011）、`:108`（T014）、`:185`（T039） | 台账写「37 claimed / 15 unclaimed」，实测 **36 claimed / 16 unclaimed**；被漏掉的正是 `reporter-seat#C-18`（运行期省略条件必须被 test 断言），它**没有任何行排程该断言**；`C-14` 的「Phase 1 基线 + T014」理由不成立（Phase 1 五项基线都不读 `agents/reporter.agent.md`；T014 只是撰写），其 key-set 断言同样无人认领 | 修正 15→16 并把 C-18 列入清单；新增/扩写一行断言 C-18 的两个合取式，以及 C-14 的 frontmatter key set（可并入 T011/T012） |
| E-04 | E 覆盖 | 覆盖核算门 → 本阶段 coverage 结论 | MEDIUM | 核算脚本输出；`create-tasks/SKILL.md:383-386`；全 spec 目录 grep 无 `coverage-baseline` 命中 | `coverage-baseline.txt` 缺失 → `status: baseline-missing`，`[clause-uncovered] fail (589)`（589 条为语料内其它 feature 的条款，本应由基线豁免）。tasks 阶段的 runtime-evidence 落地职责未完成，且 tasks.md 未把 freeze 排进任何行 | 由 **tasks** 阶段补做：`python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/088-speckit-visualization --freeze > .specify/specs/088-speckit-visualization/coverage-baseline.txt`（analyze 侧不得代冻） |
| E-05 | E 覆盖 | 契约 → FR 覆盖核算（analyze/implement 门） | MEDIUM | `account-clause-coverage.py` 输出 `FR claimed: 2` / `UNCOVERED-FR` ×20；`shared/definitions/contract-clause-definitions.md:52`（§4 rule 3）；如 `contracts/status-report.contract.md:16` | 本特性 6 份契约把 FR id 全部写成行内代码（`` `FR-007` ``），按 owner 语法它们只是 **mention** 不是 citation group，于是 `[fr-uncovered]` 判 20/22 未覆盖（可见者仅 FR-005、FR-021）。实质性映射存在（文件头 `**Covers**:` 未加反引号），但机器通道读不到 | 在每个条款块末补一个非代码跨度的引用组（如 `(FR-003, FR-004)`），或统一去掉条款正文里 FR id 的反引号；二者都是契约层（plan）修复 |
| E-06 | E 覆盖 | verification.md / T042 | LOW | `requirements.md:323`（SC-009）；`tasks.md:188`（T042）、`:113`/`:134`/`:155`（T018/T026/T031 均为 fixture 或只读运行） | SC-009 要求「a real multi-minute run reports on cadence + a supervised subordinate flow is reported by its master」，但没有任何行产出真实多分钟运行；T042 只能按自己的规则把它记成 `not-measured` | 在 T042 显式写「SC-009 → not-measured（无真实长跑行）」并接受，或新增一条 dogfood 运行行（须有可执行前提） |
| F-03 | F 不一致 | tasks → implement 的 red-first 锚点 | MEDIUM | `tasks.md:89`（T010）、`:133`（T025）、`:152`（T028）、`:185`（T039）、`:189`（T043） | 5 条 `[green:]` 与行的实际动作不符：T010（指针行）claim C-12（三模式），C-40（载荷通道/指针）却由 T043 claim；T025（REQUIRED_FIELDS pin）claim C-38（forbidden/return），该条款实际由 T020 断言；T028（命令模板+四份拷贝）claim C-42（摘要读取），其内容是 C-41 的命令半边；T039（镜像）claim C-13（零机械禁令），实现者是 T036/T008；T043（守卫命题）claim C-40 | 按本表逐条改挂；validate-tasks 只验「可解析/不重复」，不验「行内容是否就是该条款」（objective-analysis-gate rule 4），建议 tasks 阶段修复后复跑 |
| F-04 | F 不一致 | 无下游继承（计数仅供读者/后续门引用） | MEDIUM | `plan.md:74`（C-1…C-50）、`:95`（6 files / 50 clauses；6 scenarios）、`:169-171`（Three files are new … five existing）、`:303`（6 scenarios A–F）；`tasks.md:185`（the eight rows）、`:28`（GATE-1 deselect 引用 docker/hugo suites） | 计数/引用漂移：条款 50 vs 实测 52（两处）；「Three files are new」后列 4 个；「five existing files」实测 6 个（subagent-definitions / external-dispatch-recipes / create-team SKILL / create-mode / patterns / coaching SKILL）；quickstart 6 场景 vs 文件 A–H 共 8 个；Mirror Obligations 8 行 vs 表内 9 行；GATE-1 的 deselect 占位指向 `notes/pre-change-measurements.md` 里并不存在的 docker/hugo 套件（T002 只采 progress-reporting） | 以文件为准重算并改写；plan § Phase 1 Summary 声称「counts taken from files on disk」，需让该声称成立 |
| F-05 | F 不一致 | 实现读入（T030）与后续阶段的读法 | MEDIUM | `requirements.md:400-403`（A11）、`:348`（Boundary 行）；`features/088.md:35`、`:68`；对照：`plan.md:42-46`、`:254-258`（D6）、`research.md:81-104`（RO-06）、`contracts/status-digest.contract.md:26-38`（C-42）、`data-model.md:142-158`（E7） | RS-004/A11 的路径前提仍残留矛盾：requirements A11 与 features/088.md 两处仍写「摘要读取 `.specify/state/` 下的状态脊与逐条状态文件」，而 plan D6/RO-06/C-42/E7 已实测并声明「registry 在仓库外（`$SPECIFY_LINE_REGISTRY_DIR` → XDG → `~/.local/state/spec-kit/lines`），从不 hardcode `.specify/state/`」。plan 的披露是正确动作，但它不是引用——权威文本仍是旧读法 | requirements 阶段把 A11/Boundary 行改为「registry（owner: line-registry.py）为机器可读来源；spine 仅供人读」，features 阶段同步 features/088.md 两处；或在 requirements 就地加「superseded by plan D6」指针 |
| F-06 | F 不一致 | data-model 实体 + contracts → 实现命名 | MEDIUM | `requirements.md:28,209,211`（status line / status report）；`data-model.md:35`（E2 Status Report）；`contracts/status-report.contract.md:4` | 同一对象四个名词（status line / status report / report / line）无一处定义二者关系，checklist CHK053 已指出；契约正文以「status line」为主，data-model 实体名是「Status Report」 | 在 owner 文档或 data-model E2 加一句「Status Report = 一次 tick（或触发）发出的一条 line；Supervision Report 是它的子类形态」，其余位置按该句引用 |
| G-01 | G 特性联动 | feature registry 行与 detail → 后续阶段读法 | MEDIUM | `features.md:94`；`features/088.md:8,20,82` | 阶段记录陈旧：index 行 Last Updated 只列「requirements + clarify + plan」，detail 的 Latest Review 写「任务拆解由 `/speckit.tasks` 承接」、Status Tracking 写「Planned: 当前态 … 下一步由 `/speckit.tasks` 拆解」，而 tasks.md 与 checklist 都已落盘。Status=Planned 本身合法（不得回退，tasks/checklist 都不改状态），但 feature-integration § Core Protocol step 2（每个 lifecycle 命令都更新 Last Updated）与 step 3（tasks 阶段在 detail 记录 key changes）未被履行 | 由 feature/tasks 侧补一条 dated 记录（tasks + checklist 两阶段）并更新 index 行 Last Updated；不要动 Status |
| H-01 | H 清单问责 | checklist 证据（`checklist-selfcheck.json` / § Notes） | LOW | `checklists/framework-visualization-2026-11-06.md:141-145`；`test-evidence/checklist-selfcheck.json` `dimension_hits` | 清单自称「measured」的维度计数与文件不符：`Gap` 声称 19、实测 17；`Ambiguity` 13→11；`Conflict` 6→4；`Assumption` 3→2（`Assume:` 1 条未计入 `Assumption`）。60 items、100% 可追溯、0 非问句三项成立 | 重算四个数字并就地加一行更正；或修 selfcheck 的统计口径（把 legend/正文命中排除） |

合计 22 条：CRITICAL 1 / HIGH 3 / MEDIUM 13 / LOW 5。

### 2.1 D-01（CRITICAL）证据

**evidence_supported**：
- `contracts/reporting-obligations.contract.md:102` —— `## C-09 · RO-09 — The digest contract, by shape`；该文件 C-01…C-13 逐条定义 RO-01…RO-13。
- `contracts/status-digest.contract.md:96` —— C-46 的命题表第 9 行：`| RO-09 | a captured line set carries the profile field and a recorded profile switch |`。
- `quickstart.md:204` —— `the thirteen proposition ids are exactly the RO-01…RO-13 names contract C-46 enumerates, and they are the same names contracts/reporting-obligations.contract.md uses for its clauses (one vocabulary, two uses …)` —— 该断言与上两条互斥。
- 两表其余 12 行主体一致（已逐行比对），分歧仅在 RO-09 —— 典型的「复制后单行漂移」形态。

**evidence_not_supported**：不能判定实现者会以哪一份为准（两份都是规范文本）；也不声称这会导致某条 SC 必然失败（SC-009/SC-007 只要求守卫给出具名裁决）。

**宪法裁定**：`constitution.md` § XIV「Every fact — … an enumerated list … MUST have exactly one authoritative definition point (its owner)」，且「Only three duplicates are legitimate」（镜像 / 测试钉值 / 日期化记录）——命题清单的两份表格都不属于三者，因此按 Constitution Authority 记 **CRITICAL**，不接受 downgrade。`plan.md:84` 第 XIV 行「✅ Pass」因此为不成立的自评。

### 2.2 F-01（HIGH）证据

**evidence_supported**：见上表 8 处定位；代表性原文 `contracts/status-report.contract.md:55`「*Judged by*: guard proposition **RO-09** (line set contains both trigger kinds …)」——C-46 的 RO-08 才是「the three transition classes and their pre-tick timing」；`data-model.md:164`「INV-01 … guard proposition **RO-07**」——C-46 的 RO-05 才是四要素；`tasks.md:189` 把 RO-05…RO-12 八项依次写成「content labels / closure / stall / transitions / **profile plus recorded switch** / no interrogative / reporter-failure / carrier」，即 RO-09 = profile，与 C-09 相反、与 C-46 一致。

**evidence_not_supported**：不声称这些指针错误会让某条守卫命题消失（13 个 id 都还在），只影响「哪个命题判哪条条款」的可执行性；`C-32/C-34/C-35` 的指针正确，未列入。

### 2.3 F-02（HIGH）证据

**evidence_supported**：`requirements.md:317` 原文含 `marks the one below the declared stall threshold as stalled`；`requirements.md:230-232`（FR-009）要求 `MUST distinguish "slower than the threshold" from "stalled"`；`contracts/supervision-report.contract.md:39-41`「A sub-flow below the threshold is reported as **slow** … and a sub-flow beyond it is `stalled` — the two MUST NOT be merged」；`requirements.md:98-100`（US2 AS2）以「has not grown beyond the declared stall threshold → stalled」表述，方向与 FR-009 一致、与 SC-003 相反。

**evidence_not_supported**：不判定 fixture 的期望值本身（US2 Independent Test 的「stalling past the declared threshold」支持 stalled）；此条只针对 SC-003 的比较方向。

### 2.4 E-01（HIGH）证据

**evidence_supported**：`ls -d .specify/teams/*/` → 12；`grep -rl "reporter" .specify/teams/*/team.md` → 0（2026-11-06 实测）；`contracts/status-digest.contract.md:91` RO-04 的群体写作 `.specify/teams/*/team.md`；`requirements.md:220-223` FR-006 写作「Every team **created** through the framework's team-creation entry」；`requirements.md:378-381` A7 以「recorded reason」承诺既有 team 不被置于不可运行状态；`feature-ref.md` 28 行交付路径无 `.specify/teams/*`；`tasks.md:172` T035 要求人口来自 T003 基线，而 `tasks.md:66` T003 只记录 `12` 与 `1` 两个计数。

**evidence_not_supported**：不声称 RO-04 的实现方式（可用 `not-evaluated`、可限定群体）；不声称作者有意回填 12 个 roster——只指出「按现文本，交付集无法让 RO-04 变绿，且无人认领」。

## 3. 检查清单问责（§ H pass）

`unchecked [Gap] 17 + unraised 0 + undispositioned 0`；60 条全部未勾选，故 17 条 `[Gap]` 全部给出口径（标记形式机器可检）：

| CHK | 标签 | disposition |
|-----|------|-------------|
| CHK003 | Gap | `CHK003 disposition: covered-by requirements.md § FR-021 + § Clarifications Q4`（orchestrator 自带 duty 已定义「无席位时谁汇报」） |
| CHK005 | Gap | `CHK005 disposition: raised-as-finding C-02` |
| CHK006 | Gap | `CHK006 disposition: covered-by plan.md D2 + contracts/reporter-seat.contract.md C-14/C-19`（A13 已显式把内容形状交 plan） |
| CHK007 | Gap | `CHK007 disposition: covered-by requirements.md § Edge Cases "Two cadence profiles in one session" + contracts/status-report.contract.md C-30 + data-model.md E6 selection_record` |
| CHK009 | Gap | `CHK009 disposition: raised-as-finding C-01` |
| CHK017 | Gap | `CHK017 disposition: raised-as-finding C-04` |
| CHK018 | Gap | `CHK018 disposition: raised-as-finding C-04` |
| CHK021 | Gap | `CHK021 disposition: raised-as-finding C-03` |
| CHK023 | Gap | `CHK023 disposition: covered-by contracts/reporter-seat.contract.md C-15 + data-model.md E1`（`reporting-territory` read/write 已声明） |
| CHK032 | Gap | `CHK032 disposition: raised-as-finding C-04` |
| CHK034 | Gap | `CHK034 disposition: raised-as-finding C-05` |
| CHK036 | Gap | `CHK036 disposition: raised-as-finding C-04` |
| CHK039 | Gap | `CHK039 disposition: covered-by contracts/status-digest.contract.md C-45 + C-42 + tasks.md T027`（不可解析条目 → exit 2；任何写入即缺陷） |
| CHK040 | Gap | `CHK040 disposition: covered-by data-model.md E5 profile_summary + contracts/status-digest.contract.md C-41`（按需两次 action，不参与周期选择） |
| CHK044 | Gap | `CHK044 disposition: raised-as-finding E-01` |
| CHK046 | Gap | `CHK046 disposition: raised-as-finding C-05` |
| CHK058 | Gap | `CHK058 disposition: raised-as-finding C-05` |

**逐条处置的落点**：C-02 / C-01 / C-04（4 项）/ C-03 / C-05（3 项）/ E-01 = 11 条 raised；covered-by = 6 条。

## 4. 清单点名的四条裁决（含事实纠正）

| CHK | 裁决 | Severity | 证据 |
|-----|------|----------|------|
| CHK012（FR-002「single」的两种读法） | **不构成 finding**（disposition: `covered-by requirements.md § Edge Cases "A single-dispatch supervisor judged against the predicate" + § A9 + contracts/reporting-obligations.contract.md C-02/C-06`）。FR-002 的两个分支是析取（并发 ≥2 **或** 有一个持续到派发之后的异步委托），「single synchronous step out of scope」的主语是 synchronous step；§ Edge Cases 与 A9 已逐字给出同一裁决，C-06 还把「单个 subordinate 必须被点名」写进主从义务 | — | `requirements.md:189-192,203-207,384-392`；`contracts/reporting-obligations.contract.md:31-42,75-81` |
| CHK027（SC-003 的 stalled 方向） | **成立**，见 F-02 | **HIGH** | `requirements.md:317` vs `:230-232`、`:98-100`；`contracts/supervision-report.contract.md:37-44` |
| CHK052（30 秒三处复述） | **部分成立**，见 A-01。**事实纠正**：SC-006 并未写「30 秒」——它只写「the default cadence value」；真正复述数值的是 FR-003、FR-020 与 5 处叙述（Overview / US1 标题 / US1 正文 / Boundary 表 / A2），另有 3 处 Clarifications。冲突点不是「SC-006 自己复述」，而是 FR-003 的适用范围（无条件 30 s）与 FR-020 的条件档位相左，且 A6 声称「never copied」 | **MEDIUM** | `requirements.md:209,271`（含数字）；`:320`（SC-006 无数字）；`plan.md:206`（EP-008 扫描域）；`contracts/status-report.contract.md:36-43`（C-24 已按条件收窄） |
| CHK056（FR-016 与 A15 争同一可观察事件） | **部分成立**，见 C-06：两者不冲突（A15 给机制、FR-016 给结果），但 FR-016 未限定「whose loop」，C-29 的 `reporter-failure` 行与 A15 的 liveness 判定因此可能被同一事件同时触发/互相推诿 | **LOW** | `requirements.md:253-255,185-188,415-421`；`contracts/status-report.contract.md:91-97`；`contracts/reporting-obligations.contract.md:120-127` |

## 5. 契约条款覆盖裁决（`account-clause-coverage.py --spec`，未 `--freeze`）

**脚本读数据（原文摘录）**：`claimed clauses (this feature): 36`；`baseline: … coverage-baseline.txt (0 names, MISSING)`；`[fr-uncovered] fail (20) — 2 of 22 FRs cited from citation groups`；`[clause-uncovered] fail (589)`；`[clause-unparsable] warn (107)`；`status: baseline-missing`。

**与 tasks 自报的差异**：tasks.md 声明 `37 of the contracts' 52 clauses are claimed … the 15 unclaimed ones are enumerated`（`tasks.md:276`），实测 **36/16**。差异原因：`reporter-seat#C-18` 既未被任何行 claim，也**不在**作者的 15 条清单里。

**16 条未认领条款逐条归类**（判定口径：该条款的 `*Judged by*` 所指的测试/守卫命题是否有行排程、其内容是否有行撰写）：

| # | 条款 | 主体 | 归类 | 依据 |
|---|------|------|------|------|
| 1 | `reporting-obligations#C-02` | 范围谓词 | 有理由（T007 的 owner 断言 + T038 的样本分类） | `tasks.md:83,175` |
| 2 | `reporting-obligations#C-03` | 缺省值单一定义点 | 有理由（T007 断言 cadence anchor；T034 实现 RO-03 扫描） | `tasks.md:83,171` |
| 3 | `reporting-obligations#C-05` | 四要素按锚点 | 有理由（T007 + T008） | `tasks.md:83,87` |
| 4 | `reporting-obligations#C-06` | 主从义务覆盖每个子流程 | 有理由（T008 撰写；T021 断言闭包；RO-06 在 T043） | `tasks.md:87,129,189` |
| 5 | `reporting-obligations#C-07` | 停滞阈值按锚点 | 有理由（T008 撰写；RO-07 在 T043） | `tasks.md:87,189` |
| 6 | `reporting-obligations#C-08` | 越周期触发器（三类） | 有理由（T008 撰写；T017 实现；T053 验；RO-08 在 T043） | `tasks.md:87,111,136,189` |
| 7 | `reporting-obligations#C-09` | 摘要契约 by shape | 有理由，但**主体本身待裁**（D-01/F-01） | `tasks.md:87`；C-09 vs C-46 |
| 8 | `reporting-obligations#C-10` | 单向陈述 | 有理由（T007 的 prohibition 断言；RO-10 在 T043） | `tasks.md:83,189` |
| 9 | `reporting-obligations#C-11` | 失败必须浮出 | 有理由（T008 撰写；RO-11 在 T043） | `tasks.md:87,189` |
| 10 | `reporter-seat#C-14` | Template 路径/镜像/frontmatter key set | **部分有理由**：存在性与镜像由 T039 的 `sync-mirrors --check` 覆盖；**key-set 断言无行排程**（作者声称的「Phase 1 baseline」不读该文件） | `tasks.md:108,185`；T001–T005 的五个基线文件清单 |
| 11 | `reporter-seat#C-18` | 运行期省略条件的两个合取式 | **无排程（真缺口）**，且未列入作者清单 | `contracts/reporter-seat.contract.md:61-69`；`tasks.md:105`（T011 fixture 只覆盖 reason 值域）、`:109`（T015 只撰写文本） |
| 12 | `reporter-seat#C-21` | stdlib-only + 被 create 流程调用 | 有理由（T011 的 stdlib-import audit + T015 的 call site） | `tasks.md:105,109` |
| 13 | `status-report#C-23` | 四要素按锚点引用 | 有理由（RO-05 → T043） | `tasks.md:189` |
| 14 | `status-report#C-30` | 双档 + 切换记录 | 有理由（T053 验 profile 与 recorded switch） | `tasks.md:136` |
| 15 | `supervision-report#C-36` | coaching 单派发被点名 | 有理由（T020 的断言正是该条） | `tasks.md:128` |
| 16 | `ownership-map#C-48` | 关系表单向声明 | 有理由（T032 断言 relation table 与 feature-ref 一致） | `tasks.md:169` |

> 表内 16 行即实测未认领全集（脚本 `claimed clauses: 36` + 本表 16 = 52）。**结论：14 条有理由、1 条部分有理由（C-14）、1 条无排程（C-18）**——「有理由的未认领」未判为错误；只有 C-18 与 C-14 的 key-set 半边进入 E-03。

## 6. 汇总表

### 6.1 Coverage Summary

| 通道 | 全集 | 已覆盖 | 裁决 |
|------|------|--------|------|
| FR → 任务行 `[covers:]` | 22 | 21（95.5%） | FR-021 未认领（E-02） |
| FR → 任务行任意提及 | 22 | 22 | 仅 prose 的 1 条仍是 E-02 |
| FR → 契约 citation group | 22 | 2（9.1%） | `[fr-uncovered] fail (20)`（E-05） |
| 契约条款 → 任务 `[green:]` | 52 | 36（69.2%） | 16 未认领；14 有理由 / 1 部分 / 1 无排程（E-03） |
| SC → 任务行显式 id | 10 | 6（60%） | SC-002…SC-005 由 T042 的区间覆盖（T018/T026/T052/T031 供证）；SC-009 无产出（E-06） |
| Checklist `[Gap]` 处置 | 17 | 17 | 0 undispositioned（§3） |
| 冻结基线差集 | — | — | `status: baseline-missing`（E-04） |

### 6.2 Feature Linkage Summary

| 信号 | 读数 | 置信度 |
|------|------|--------|
| Index 行 087 | 存在；Name/Description/Status=Planned/Details/Spec Path 齐全 | high（ID 与 slug 精确匹配） |
| Detail 文件 | 存在；Status=Planned；FR 叙述与 22 条 FR 一致 | high |
| Requirement ↔ Feature 意图 | 需求主题（并发/异步流程的现状可见性）与 Feature 描述逐句对应 | high |
| 状态合法性 | `Planned` 合法：tasks/checklist 都不拥有状态跃迁，且不得回退 | high |
| 阶段记录 | tasks + checklist 未记录（index 行只到 plan；detail 仍写「下一步 /speckit.tasks」） | — → G-01 |

### 6.3 Constitution Alignment

| 原则 | 判定 | 说明 |
|------|------|------|
| XIV One Source of Truth | **冲突** | D-01（命题清单双定义点 + 单行漂移）；A-01 的 requirements 内复述为次级证据 |
| VII SDD 工作流（Feature Index 每阶段校验/更新） | **部分不符合** | G-01（tasks/checklist 阶段未更新注册表记录） |
| IV Test-First & Contract-Driven | Pass | 新行为测试行先于实现行；red-first 记录有落点（`notes/red-first-evidence.md`）；两处 regression-guard 例外已声明 |
| IX / XVII / XVIII（零新机械 / 目录治理 / 命名） | Pass | `Status Digest` 脚本 + owner 文档 + 模板均落在既有目录；无新顶层目录 |
| 其余 14 条 | Pass（无证据冲突） | plan 的 19 行检查除 XIV 行外与产物一致；`validate-decision-tensions` status=ok |

### 6.4 Unmapped Tasks（无 `[covers:]` 的行）

7 行：T002、T005（基线采集）、T029（撰写命令）、T040（生成拷贝）、T044（复跑守卫）、T045（注册表落状态）、T046（前提漂移清扫）。均为基础设施/证据行，**不欠 FR**，不记为覆盖缺口。
附注：T001 自称「claims no contract clause」却带 `[covers: FR-001]`——FR-001 的实际交付者是 T007/T008/T039，该标记属弱映射（不单列 finding）。

### 6.5 Metrics

| 指标 | 值 |
|------|-----|
| Requirements | 22 FR / 10 SC / 15 A / 12 Edge Cases |
| Tasks | 50 行（T001–T046 + T051–T054；Setup 5 / Foundational 5 / US1 10 / US2 10 / US3 5 / US4 7 / Polish 8） |
| Contracts | 6 文件 / 52 条款（C-01…C-52） |
| Clause claim | 36 / 52（69.2%），重复认领 0，悬空认领 0 |
| Findings | 22（CRITICAL 1 / HIGH 3 / MEDIUM 13 / LOW 5） |
| 分布 | Duplication 1 · Ambiguity 0 · Underspecification 6 · Constitution 1 · Coverage 6 · Inconsistency 6 · Feature-linkage 1 · Checklist 1 · Decision-tension 0 |
| Validation | 应验证 4 条（C/H）；实际第三方验证 0；直接重读 4；降级率 n/a |

## 7. 系统性观察（不抬高任何单行 severity）

1. **映射表被当成证据**（objective-analysis-gate rule 4 的教科书样本）：`validate-tasks` 判 0 dangling、0 duplicate 全绿，`validate-requirements` / `validate-decision-tensions` / `pre-analyze-check` 全绿——所有机器门都只看「id 解析得到」，而 D-01/F-01/F-03 的缺陷恰是「解析得到但指向别的内容」。本特性的 6 份契约 + data-model + tasks 之间有三层此类映射（命题→条款、条款→行、INV→命题）。
2. **复制的枚举必然漂移**：13 条命题清单、52 条款计数、Mirror Obligations 行数、checklist 维度普查——每一处副本都与 owner 偏离 1（或多）个单位。修复应把副本改引用，而不是把数字改对。
3. **「实测」声明未必实测**：plan § Phase 1 Summary 声称「counts taken from the files on disk after they were written」但 50/52、6/8、「three files」均不成立（F-04）；checklist § Notes 声称 measured 的维度计数也不成立（H-01）。这类声明让后续阶段失去重新测量的动机。
4. **决策下沉未回写**：stale bound、多项目 workspace、两席位、锚点、抑制策略等决定都只在 plan/data-model/tasks 层被隐式做出，requirements 没有对应的锚点（C-01/C-02/C-03/C-04/C-05）——guard 的判定因此依赖未记录的约定。
5. **守卫的可执行前提未闭合**：RO-04 依赖 12 个 roster（E-01）、RO-09 待裁（D-01/F-01）、stale bound 无值（C-01）——守卫是全特性唯一「机器裁决面」，其输入契约目前不自洽。

## 8. Rerun delta

无前序 analyze 报告（`test-evidence/` 内无 analyze-report-*，git 历史亦无）。本轮为首轮，故 **Resolved Since Last Run / New Since Last Run 均 N/A**；后续轮次须以本报告的 ID 集为基线（`(carried over)` 标记沿用同一 ID）。

## 9. Next actions

1. **阻断项（按归属阶段）**
   - **plan**：D-01（指定命题清单唯一 owner；C-46 表改引用）、F-01（8 处指针 + T043 措辞）、E-05（条款补非代码引用组）、F-04（重算计数）。
   - **requirements**：F-02（SC-003 方向）、A-01（单值来源 + SC-006 扫描域）、C-01…C-03、C-06、E-02 的 FR-021 口径、F-05（A11/Boundary 行）、E-01 的群体口径。
   - **tasks**：E-03（15→16、补 C-18/C-14 断言行）、F-03（5 处 `[green:]` 改挂）、E-02（covers 修正）、E-04（补 freeze）、E-06（SC-009 记 `not-measured` 或补行）、F-04 的 T039/GATE-1 两处引用。
   - **feature / checklist**：G-01（补 tasks+checklist 阶段记录）、H-01（更正维度计数）。
2. **不阻断**：C-04/C-05（owner 文档补 7 句声明）、F-06（对象名词定义）、E-06（若接受 not-measured）。
3. **可选的具体修复草稿**：本报告只提供定位与建议，不自动改写任何产物；上游修复命令由驱动者/用户手动调用（`/speckit.requirements`、`/speckit.plan`、`/speckit.tasks`）。
4. **修复后复跑**：必须重跑 `/speckit.analyze`（Round 2），并按 SKILL § Rounds 给出 Resolved / New / carried-over 三向 delta；本文的 ID 为稳定基线。

---

**Evidence integrity**: 本报告所有计数与定位均可由 §1 的命令重放；未运行任何写命令（本文件除外）；`git status --porcelain` 的既有脏文件集合未被触碰。
