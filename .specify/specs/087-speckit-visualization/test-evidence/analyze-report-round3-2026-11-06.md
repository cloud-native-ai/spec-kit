# Analyze Report — 087-speckit-visualization（/speckit.analyze，2026-11-06，Round 3）

**Unit**: `/speckit.analyze` · **Run ID**: `r20261106T040353Z-087a` · **Stage**: analyze（Round 3，全严重度复核 + rerun delta）
**Spec dir**: `.specify/specs/087-speckit-visualization`（`REQUIREMENT_ID=087`，`FEATURE_ID=087`，`MODE=C`）
**Flow class**: `execution` / `source=declaration`（`flow-class-check.py --action lookup --unit-id "spec:087-speckit-visualization"` → exit 0；非表达类，既有门禁集不变）
**Prior report**: `test-evidence/analyze-report-round2-2026-11-06.md`（Round 2，10 条 open findings）
**Baselines under analysis**: requirements `b2c044e0` / plan `3ec54975` / tasks `799083f2` / checklist `d3946058`
**性质**: 严格只读。本报告是本阶段唯一交付产物；requirements / plan / tasks / contracts / data-model / quickstart / checklists / 注册表零修改。§1 的三份 validator 原始读数写入 `test-evidence/round3-*.txt`（证据，不是产物）。

## 0. 门禁结论（Gate Verdict）

**未通过（NOT GREEN）**：round 2 的 1 CRITICAL（F-07）+ 1 HIGH（F-01）**均已关闭**，但本轮全量复核新识别 **2 条 HIGH**（F-10 / F-11，均为树内既有、此前两轮未识别的封闭集合冲突），按「CRITICAL/HIGH 为零或已处置」判据不得判绿。

| 严重度 | 条数 | 归属与处置要求 |
|--------|------|----------------|
| CRITICAL | 0 | — |
| HIGH | 2 | **F-10（新）**：plan `D10` 的 exit-status 定义与合同 `C-45` 逐字相反（nothing-running = 0 vs 3），使 SC-005 的「declared exit status」有两个声明值；归属 **plan**（plan.md:291-292）。**F-11（新）**：`C-41`/plan `D8`/T009/T029 写「exactly two actions」，T016 要求第三个 `--action report`；归属 **plan + tasks**（选择二动作或三动作后单向对齐） |
| MEDIUM | 1 | **F-12（新）**：tasks.md 的 US1 Independent Test（:99）与 Parallel Example（:273）仍写「three roster fixtures」，而 C-16/T011 已固定四个 fixture（三个具名缺陷 + compliant）；归属 **tasks**。不阻断，但会使 US1 测试漏掉 two-seats 缺陷类 |
| LOW | 5 | C-04、C-05、H-01（carried over）+ F-13、G-02（新）；不阻断 |

**round-2 C/H 复核（逐条）**：

| ID | Round-2 严重度 | Round-3 结论 | 关闭证据（摘要） |
|----|----------------|--------------|------------------|
| F-07 | CRITICAL | **已关闭** | `requirements.md:198-205` FR-001 改为「exactly eight facts and no others」并逐项与 C-01 八条同序；`contracts/reporting-obligations.contract.md:21-32` 八条；`tasks.md:83` T007「exactly eight … asserts it by clause id and count rather than re-listing the eight」；`tasks.md:87` T008「the eight … the same eight requirements.md FR-001 enumerates」；`feature-ref.md:123` owns 行改为「enumerated once, in C-01 (mirroring FR-001), not re-enumerated here」；`quickstart.md:26` eight；`requirements.md:419-423` A10 eight；checklist `d3946058` 把 CHK002/CHK054 标为 resolved。全 spec 目录 grep 无 `five owned / five facts / exactly five` 残留 |
| F-01 | HIGH | **已关闭** | 六份合同的全部 `*Judged by*` 与 INV 映射逐个复核：C-22→test file（并明写 attribution 不是 RO-05 的四要素，`status-report.contract.md:22-24`）、C-24→RO-03+test 且「override 由 C-30 钉住，不是 RO-09」（`:48-50`）、C-30→test file（`:125-127`）、INV-02→test file（`data-model.md:185`）、INV-04→C-30/test（`:187`）、INV-10→C-43/unit test（`:193`）；C-46 的 RO-04 行改为 T003 name-list + `--roster` 且「no glob is a default population」（`status-digest.contract.md:105`）；RO-09 行改为 owner digest section + 四个 digest face（`:110`）；§116-119 改为「profile selection (C-30)」且删除「FR-020's profile fields (RO-09)」；`plan.md:85,107-113` 的 XIV Pass 断言同步。13 个 RO id 全部仍存在且主体一致 |

**round-2 MEDIUM/LOW 复核**：E-03、F-03、F-04、F-08、F-09 **全部关闭**（证据见 §4.1）；C-04、C-05、H-01 仍 open（等级不变，理由见 §2.4 与 §4.3）。

### 0.1 验证波状态（显式降级，非静默）

- **同一作者门（objective-analysis-gate）**: **未触发**——requirements/plan/tasks/checklist 由本无人值守链的**其它阶段运行**产出，本 worker 未在本次会话撰写它们（gate owner: `.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires 第 2 条；round 1/2 同判）。
- **CRITICAL/HIGH 独立验证子代理**: **不可派发**（本层为 bounded assignment，brief 明确禁止派发子代理）。按 SKILL `references/validation-and-report.md` § Subagent-unavailable fallback 执行**直接受限重读**：F-10、F-11 各给 `(validated: direct re-read, subagent unavailable)` 与 evidence_supported / evidence_not_supported 边界（§2.1/§2.2）。
- **降级率**: n/a（无第三方 validator）；应验证 2 条 C/H，第三方验证 0，直接重读 2。**读侧一致性**：每条 C/H 断言均由 §2 引用的原文逐字支撑（两条均为「两处规范文本互相矛盾」的文本事实，不依赖推断）。
- **零发现下限**: 本轮非零发现，不适用；coverage 通道已逐项复算（§5）。

## 1. 方法与执行轨迹

| 步骤 | 命令 / 动作 | 结果 |
|------|-------------|------|
| 前置脚本 | `bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` | exit 0；`MODE=C`；`AVAILABLE_DOCS` 含 research/data-model/contracts/quickstart/checklists/feature-ref/tasks |
| 类别读取 | `flow-class-check.py --action lookup --unit-id "spec:087-speckit-visualization"` | `flow_class: execution`，`source: declaration`，exit 0 |
| 覆盖核算（固定步骤，只读） | `python3 .specify/scripts/python/account-clause-coverage.py --spec .specify/specs/087-speckit-visualization`（**未** `--freeze`；原始读数 `test-evidence/round3-coverage.txt`） | exit 1；`claimed clauses (this feature): 33`；`baseline: coverage-baseline.txt (573 names)`；`[fr-uncovered] pass (0) — 22 of 22`；`[clause-uncovered] fail (592)`；`[coverage-baseline-delta] fail (19)`；`[clause-unparsable] warn (107)`；`status: uncovered` → §5 |
| 确定性校验 | `validate-requirements.py requirements.md` | `status: ok`，六标签全 pass（0），`scanned: 522 lines, 32 definition rows, 0 shared strings`，0 error 0 warning |
| 确定性校验 | `validate-tasks.py tasks.md` | `PASS (with warnings)`：0 error / **11 warning**（7 `green-cross-phase` + 4 `green-path-divergence`；全部在 tasks.md § WARNING ADJUDICATION 有作者裁决） |
| 确定性校验 | `validate-decision-tensions.py --spec …` | `status: ok`，六标签 0 命中，`scanned: 330 lines, 2 record(s)`，`channel: value_domain=HIGH-or-0, high=0` |
| 确定性校验 | `pre-analyze-check.py --spec-dir … --stage plan --repo .`（原始读数 `round3-pre-analyze-plan.txt`） | `decision=pass errors=0 advisories=134 waived=0`；`fr=22 sc=10 tasks=50 files=15`；134 条全为 `missing-path`，覆盖 13 个交付期路径名（`shared/guidelines/reporting-obligations.md`、`agents/reporter.agent.md`、`templates/commands/status.md`、`scripts/python/status-digest.py`、`skills/internal/create-team/scripts/validate-roster.py`、5 个 `tests/` 文件及其镜像），无第 14 个非交付路径名 |
| 确定性校验 | `pre-analyze-check.py --spec-dir … --stage tasks --repo .`（原始读数 `round3-pre-analyze-tasks.txt`） | 同读：`decision=pass errors=0 advisories=134 waived=0` |
| 检测通道 A–I | 逐产物交叉读（§2） | 8 条 open（2 HIGH / 1 MEDIUM / 5 LOW）+ 7 条本轮关闭 |
| 检查清单 H 通道 | 60 条逐条分诊（§3） | 17 条 unchecked `[Gap]`：10 covered-by + 7 raised，`undispositioned=0`；3 条已 `[x]` |

**round-2 → round-3 读数对照（同一命令）**：`pre-analyze --repo .` 的 advisories 124（round-2 归档文件 `pre-analyze-tasks.txt`）→ 134；路径名集合不变（13 个），增量来自修复后文本对同一批交付期路径的引用次数增加；`files` 14 → 15。round-2 报告正文写 126，其归档文件写 124——正文与证据相差 2，属 prior report 的记账笔误，不影响结论（§4.4）。

**读入的权威面**：requirements.md（22 FR / 10 SC / 15 A / 12 Edge Cases / 522 行）、plan.md（19 行宪法检查 / T-001–T-002 / EP-001–EP-010 / D1–D12 / 9 行 Mirror Obligations）、tasks.md（50 行，T001–T046 + T051–T054 / § Clause Coverage Ledger）、contracts ×6（52 条款 C-01…C-52）、data-model.md（E1–E7 + INV-01…INV-12）、quickstart.md（A–H）、checklists ×2、feature-ref.md、`features.md` 087 行、`features/087.md`、`constitution.md` v1.16.0（19 原则）。

## 2. Findings（open，8 条）

`propagation_surface` 是每条的第一个字段；severity 由它派生（owner: `objective-analysis-gate.md` rule 3）。

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| F-10 | F 不一致 | 摘要实现 → SC-005 的验收读数 + quickstart D | **HIGH**（新识别，既有 `(validated: direct re-read, subagent unavailable)`） | `plan.md:291-292`（D10）；`contracts/status-digest.contract.md:77,78,84-85`（C-45）；`quickstart.md:123,132`；`data-model.md:125`；`research.md:228`（U-4） | 同一个 exit-status 事实有两个互相矛盾的规范定义：plan D10 写「`0` = a digest was rendered (**including** the explicit "nothing running" rendering)」且同时写「`3` = nothing active」——同一 case 被判给 0 又判给 3，集合不互斥；C-45 的同一行写「(an explicit "nothing running" rendering is **not** this status)」并在 :84 加 MUST NOT「render an empty digest with status `0`」。quickstart D / data-model E5 / research U-4 与 C-45 一致，D10 是孤例。SC-005 只写「the declared exit status」，该表述因此有两个声明值 → 验收判据不可判定 | 改 plan D10 的一行：`0` 行删去「including … 'nothing running' rendering」，改为「`0` = a digest was rendered with at least one entry; an explicit 'nothing running' rendering is status `3`」，与 C-45 逐字一致。C-45 是测试判据（T027/T031/quickstart D 都读 3），plan 是 stale 侧 |
| F-11 | F 不一致 | 脚本 CLI 接口 → C-41 的 contract test + US1/US2 的任务链（T016/T017/T018/T052） | **HIGH**（新识别，既有 `(validated: direct re-read, subagent unavailable)`） | `contracts/status-digest.contract.md:5,12,15-18`（C-41「exactly two actions」）；`plan.md:282-283`（D8「One script, two actions」）；`tasks.md:88`（T009「two actions」）、`:153`（T029「the two actions」）、`:91`（checkpoint「both script actions」）；反例 `tasks.md:110`（T016「as a **third action** (`--action report`)」） | 脚本 action 集合有两个定义点：C-41 的标题与正文（`one command, one script, two actions` / `MUST implement exactly two actions`: digest、guard）与 plan D8/T009/T029 一致；T016 却要求 `--action report` 作为第三个 action，且 T017/T018/T052 都依赖它。T009 以自己的 green point 认领 C-41，T016 落地后会把 C-41 重新变红。四个文本对两个文本，任何实现者都必须先择一 | 二选一后单向对齐（同一提交）：**(A) 三动作**——把 C-41 标题/正文/judged-by 改为「three actions（digest / guard / report）」，同步 plan D8、T009、T029（并把 C-41 的 judged-by 从「exposes both actions」改为「exposes exactly these three」）；**(B) 两动作**——把 T016 改为「the report renderer is an internal helper shared by the two actions（no third `--action`）」并同步 T017/T018/T052 的调用形态。推荐 (A)：T016/T017/T018/T052 的链条更长，(B) 要改四行 |
| F-12 | F 不一致 | US1 的 red-first 测试范围（T011 的执行文本） | MEDIUM（新识别，既有；与 F-09 同类残差） | `tasks.md:99`（US1 **Independent Test**「over the three roster fixtures (compliant / missing-seat / unresolvable-agent)」）、`:273`（Parallel Example「three roster fixtures + reason set」）；对照 `tasks.md:105`（T011 四个 fixture，含 **two `role: reporter` seats**）与 `contracts/reporter-seat.contract.md:62-63`（C-16「four fixtures (compliant, missing-seat, unresolvable-agent, two-seats)」） | C-03 的修复把 two-seats 缺陷类写进 C-16/T011，但 tasks.md 的两处指导文本仍停在三个 fixture，且恰好漏掉的 two-seats 是 C-16 封闭缺陷集的第三个成员。测试作者按 Independent Test 写会少测一个具名缺陷类；按 T011 写则与指导文本不一致 | 把 `tasks.md:99` 与 `:273` 的「three roster fixtures …」改为「four fixtures (compliant / missing-seat / unresolvable-agent / two-seats)」。注意 `tasks.md:105` 与 `quickstart.md:72` 的「four **defect** fixtures」措辞把 compliant 也称作 defect，与「closed at three named defects」不符——属同一处的命名小疵，可一并改为「four fixtures (three named defects + compliant)」 |
| C-04 | C 欠指定 | owner 文档（T008）声明面 | LOW（carried over） | `requirements.md:206-212,245-250,160-170`；`tasks.md:87`（T008 清单） | 四个 owner 级口径仍无声明：① idle tick 是否可抑制；② long-run 档的计时锚点；③ 阈值与周期的数量关系；④ 宿主时钟跳变/挂起时「tick 序列缺口」与「reporter 停滞」如何区分。T008 的清单未新增这四项 | 在 owner 文档把这四条各写一句声明（T008 的作者清单相应加 4 项），不必改 FR（与 round 2 建议同） |
| C-05 | C 欠指定 | 行级策略（owner + 渲染器） | LOW（carried over） | `requirements.md:174-175`（预算耗尽）、`contracts/status-report.contract.md:108-116`（C-29）、`contracts/supervision-report.contract.md:110-121`（C-40） | 三条行级策略仍缺：① `reporter-failure` 行是否也须携带四要素（INV-01 说 "every Status Report"，C-29 未点名）；② 派发载荷缺 reporting 字段时的失败模式（C-40 只说 "carries by injecting"）；③ 预算耗尽「仍然报告」只有 Edge Case，无 FR/契约条款 | 同 round 2：C-29 明确 failure 行的最小内容；C-40 增加一个具名失败条件；把预算规则升为一句契约条款 |
| H-01 | H 清单问责 | checklist 证据（`checklist-selfcheck.json` / § Notes） | LOW（carried over） | `checklists/framework-visualization-2026-11-06.md:141-145`；`:152`（"Gaps worth triaging first" 仍列 CHK027） | 清单 Notes 自称 "measured" 的维度计数仍与文件不符：实测 `Gap` 17（声称 19）、`Ambiguity` 11（13）、`Conflict` 4（6）、`Assumption` 2（3）；60 items、100% 可追溯、0 非问句三项成立；CHK027 已 `[x]`，Notes 仍把它列在待分诊 gaps | 重算四个数字并就地加一行更正；把 Notes 的 CHK027 行标注为 resolved |
| F-13 | F 不一致 | 读者/实现者按路径打开 owner | LOW（新识别，既有） | `data-model.md:108`（`` `storage/guidelines/one-source-of-truth.md` is the discipline ``） | 该路径不存在（本仓只有 `shared/guidelines/one-source-of-truth.md` 与其镜像 `.specify/shared/guidelines/one-source-of-truth.md`）；它在 E4 的「number keeps its single definition point」句中充当纪律指针，是一处断链的 owner 引用 | 改为 `.specify/shared/guidelines/one-source-of-truth.md`（或框架源路径 `shared/guidelines/one-source-of-truth.md`，按读者面择一） |
| G-02 | G 特性联动 | feature registry 记录 → 后续阶段读法 | LOW（新识别，既有） | `features.md:94`（087 行 plan 记录「Execution Premises EP-001…EP-009（全 `verified`）」）；`features/087.md:20`（同句）；对照 `plan.md:216-225`（EP-001…**EP-010**，10 行全 verified） | 特性注册表把 plan 的 premise 数量记成 9，而 plan 实际有 10 条（EP-010 是 round-1 修复为消解 GATE-1 占位而新增的）；index 与 detail 同句同错。状态 `Planned` 本身合法，阶段记录齐备（G-01 不回退） | 把两处的 `EP-001…EP-009` 改为 `EP-001…EP-010`（dated 记录内的一处数字更正），或在该记录尾部加一句 `EP-010 added 2026-11-06` |

### 2.1 F-10（HIGH）证据

**evidence_supported**：
- `plan.md:291-292` —— 「**D10 — Exit statuses are a closed three-value set.** `0` = a digest was rendered (including the explicit "nothing running" rendering, which is an answer), `3` = nothing active (the declared "nothing active" status `FR-011`/SC-005 name), `2` = usage or input error.」
- `contracts/status-digest.contract.md:77` —— C-45 表：`| `0` | a digest was rendered (an explicit "nothing running" rendering is **not** this status) |`；`:78` —— `| `3` | nothing active — … with the explicit `nothing-running` rendering |`；`:84-85` —— 「An empty entry set MUST render `nothing-running` with status `3`; it MUST NOT render an empty digest with status `0` (`SC-005`).」
- `quickstart.md:123` —— Scenario D「status `3`」；`:132` —— premise 4「the exit status is `3` — … distinct from `0` (a rendered digest)」；`data-model.md:125` —— E5「`nothing-running` … with exit status `3`, never an empty result」；`research.md:228` —— U-4「statuses `0` rendered / `3` nothing active / `2` input error」。
- `requirements.md:340` —— SC-005 写「renders an explicit "nothing running" state with the **declared** exit status」，把该值的可判定性交给「声明」；两处声明不一致即不可判定。

**evidence_not_supported**：不声称某条测试必然失败——T027 的测试行只写「an empty registry renders `nothing-running`」而未在行内点名 exit code；T031 只要求「with exits codes」；C-45 的 judged-by 说「three fixtures … assert the three statuses」，若测试作者按 C-45 写则会与 D10 派生的实现冲突。也不自称知道作者意图（0 还是 3）；只声称 D10 自身两句互斥、且与 C-45 的 MUST NOT 逐字相反。

**stale-copy decision test**：D10 的 exit-status 重述不属于 XIV 允许的三类合法重复（不是镜像/逐工具副本、不是测试里钉住的字面量、不是 dated record），因此它是会漂移的副本，按 `.specify/shared/guidelines/one-source-of-truth.md` 必须转为引用（或删去 D10 的集合，改为「see C-45」）。

### 2.2 F-11（HIGH）证据

**evidence_supported**：
- `contracts/status-digest.contract.md:12` —— 标题「## C-41 · DG-01 — One command, one script, **two actions**, one reading」；`:15-18` ——「The script MUST implement **exactly two actions**: - `--action digest` … - `--action guard` …」；`:5` —— 文件头「the deterministic script `scripts/python/status-digest.py` with two actions」。
- `plan.md:282-283` —— 「**D8 — One script, two actions.** `status-digest.py --action digest` …; `--action guard` …」。
- `tasks.md:88` —— T009「as one stdlib-only file with **two actions** over one shared reader: `--action digest` … and `--action guard` …」，且该行的 `[green: …#C-41]` 正是把 C-41 判绿的行；`tasks.md:153` —— T029「a body that only names the script path, **the two actions** and the exit-status set」；`tasks.md:91` —— Foundational checkpoint「the shared reader exists behind **both script actions**」。
- 反例 `tasks.md:110` —— T016「Author the status-line renderer into `scripts/python/status-digest.py` as a **third action (`--action report`)** …」；T017（`:111`）「the same renderer」、T018（`:113`）「emit ≥3 attributed status lines」、T052（`:135`）均以该 action 为前提。
- 后果链：T009 以 C-41 为 green point；T016 落地后脚本有第三个 action，C-41 的「exactly two」不再成立——同一文件的 § WARNING ADJUDICATION 声称 green point 与行内容一致，此处是它未覆盖的一条。

**evidence_not_supported**：不声称 C-41 的 judged-by 会失败——其断言是「the script exposes **both** actions」，三个 action 仍满足「exposes both」；因此这不是 F-07 式「两条机器断言互斥」的死锁，而是规范文本（C-41/D8/T009/T029）与执行行（T016）对同一接口的两套定义。也不替作者选择「二动作」还是「三动作」；两种读法都只需单向、有界的对齐。

**stale-copy decision test**：action 集合在 D8/T009/T029 中的重述都不属于三类合法重复，且 T016 给出了第三值——按 one-source-of-truth 的 disagreement procedure，C-41 是 owner，其他位置应转为引用，或（若设计确为三动作）先改 owner 再让副本引用它。

### 2.3 MEDIUM 证据（F-12）

- `tasks.md:99`（US1 Independent Test）：「run `…/validate-roster.py` over the **three roster fixtures** (compliant / missing-seat / unresolvable-agent)」——缺 two-seats。
- `tasks.md:273`（Parallel Example）：「Author tests/contract/test_roster_reporter_seat.py (**three roster fixtures** + reason set)」。
- 权威侧：`tasks.md:105`（T011）「**four defect fixtures** (compliant, missing seat, … **two `role: reporter` seats** — the closed defect set's third member)」；`contracts/reporter-seat.contract.md:62-63`（C-16 judged-by「**four fixtures** (compliant, missing-seat, unresolvable-agent, two-seats)」）；`quickstart.md:72-75`（round-2 F-09 已修：four + value-domain = five）。
- 该两处自 852e0843（round-1 修复落盘后）起就未同步，round 2 未识别；与 F-09 同类（「改 owner、未改副本」），但落在执行面的 Independent Test 上，故记 MEDIUM 而非 F-09 的 LOW。

### 2.4 LOW 证据（摘要）

- **C-04**：`requirements.md:160-170`（Cadence versus atomic steps / Stall versus slow 只覆盖相邻概念）、`:206-212`（FR-003 无 idle/tick-up 抑制语）、`:245-250`（FR-009 无阈值与周期关系语）；`tasks.md:87` T008 的作者清单没有这四项。与 round 2 同点位、同等级。
- **C-05**：`contracts/status-report.contract.md:108-116`（C-29 不点名 failure 行的四要素）、`contracts/supervision-report.contract.md:110-121`（C-40 无缺字段的失败条件）；`requirements.md:174-175` 的预算规则仍只在 Edge Case。与 round 2 同点位、同等级。
- **H-01**：实测维度命中 `Gap 17 / Ambiguity 11 / Conflict 4 / Clarity 6 / Measurability 6 / Consistency 5 / Completeness 4 / Assumption 2 / Dependency 3 / Coverage 2`；Notes 声称 `19 / 13 / 6 / … / 3`；`:152` 的 triage 列表仍含 CHK027（已在 `123e5949` 标为 `[x]`）。
- **F-13**：`data-model.md:108` 的 `storage/guidelines/one-source-of-truth.md` 在树中不存在；`shared/guidelines/one-source-of-truth.md` 与 `.specify/shared/guidelines/one-source-of-truth.md` 均存在。`pre-analyze` 的路径检查未报它（其路径识别只覆盖框架源前缀 + 交付路径形态），故此前两轮均未浮出。
- **G-02**：`features.md:94` 与 `features/087.md:20` 写 `EP-001…EP-009`；plan 的 Execution Premises 表有 10 行（EP-001…EP-010，`:216-225`），全 `verified`。阶段记录本身齐备（tasks/checklist/analyze 均已记录，G-01 不回退）；`pre-analyze --advisories=0` 的调用形态问题仍作 §4.4 的 deferred 记录，不并入本条。

## 3. 检查清单问责（§ H pass）

`unchecked [Gap] 17 + unraised 0 + undispositioned 0`；60 条中 57 条未勾选、3 条已 `[x]`（CHK002/CHK027/CHK054，均为 analyze 前两轮的 resolved 标注，不影响 Gap 集）。17 条 `[Gap]` 全部给出口径（逐条复验锚点仍在位）：

| CHK | 标签 | disposition |
|-----|------|-------------|
| CHK003 | Gap | `CHK003 disposition: covered-by requirements.md § FR-021 + § Clarifications (Session 2026-11-06) 第 4 问` |
| CHK005 | Gap | `CHK005 disposition: covered-by requirements.md § FR-011 workspace rule + data-model.md § E5` |
| CHK006 | Gap | `CHK006 disposition: covered-by plan.md D2 + contracts/reporter-seat.contract.md C-14/C-19` |
| CHK007 | Gap | `CHK007 disposition: covered-by requirements.md § Edge Cases "Two cadence profiles in one session" + contracts/status-report.contract.md C-30 + data-model.md E6 selection_record` |
| CHK009 | Gap | `CHK009 disposition: covered-by contracts/status-digest.contract.md C-44 + contracts/ownership-map.contract.md C-47 stale-bound 行 + data-model.md E5` |
| CHK017 | Gap | `CHK017 disposition: raised-as-finding C-04` |
| CHK018 | Gap | `CHK018 disposition: raised-as-finding C-04` |
| CHK021 | Gap | `CHK021 disposition: covered-by contracts/reporter-seat.contract.md C-16（four fixtures / 三个具名缺陷含 two-seats）+ tasks.md T011/T013 + data-model.md E1` |
| CHK023 | Gap | `CHK023 disposition: covered-by contracts/reporter-seat.contract.md C-15 + data-model.md E1` |
| CHK032 | Gap | `CHK032 disposition: raised-as-finding C-04` |
| CHK034 | Gap | `CHK034 disposition: raised-as-finding C-05` |
| CHK036 | Gap | `CHK036 disposition: raised-as-finding C-04` |
| CHK039 | Gap | `CHK039 disposition: covered-by contracts/status-digest.contract.md C-45 + C-42 + tasks.md T027` |
| CHK040 | Gap | `CHK040 disposition: covered-by data-model.md E5 profile_summary + contracts/status-digest.contract.md C-41`（沿用 round-2 裁定，不重开） |
| CHK044 | Gap | `CHK044 disposition: covered-by requirements.md § FR-006 population + contracts/reporting-obligations.contract.md C-04 + tasks.md T003/T035` |
| CHK046 | Gap | `CHK046 disposition: raised-as-finding C-05` |
| CHK058 | Gap | `CHK058 disposition: raised-as-finding C-05` |

**落点统计**：covered-by 10 条（CHK003/005/006/007/009/021/023/039/040/044），raised-as-finding 7 条（C-04×4、C-05×3）。上一轮的 four adjudicated items 不变：CHK012 不构成 finding；CHK027 已按修复后的 SC-003 关闭；CHK052 的 normative 半边已由 FR-003/SC-006 修复（叙述性复述见 §4.4）；CHK056 由 FR-016 的 "emitting flow's own" 限定关闭。

## 4. Rerun delta

### 4.1 Resolved Since Last Run（7 条，各附关闭证据）

| ID | Round-2 严重度 | 关闭证据 |
|----|----------------|----------|
| F-07 | CRITICAL | `requirements.md:198-205`（eight，逐项与 C-01 同序）+ `contracts/reporting-obligations.contract.md:21-32` + `tasks.md:83,87`（eight，按 clause id + count 断言，不重列）+ `feature-ref.md:123`（不重列，只引 C-01/FR-001）+ `quickstart.md:26` + `requirements.md:419-423` A10 + checklist `d3946058`（CHK002/CHK054 resolved） |
| F-01 | HIGH | 六合同的 `*Judged by*`/INV 映射逐个复核无错位：`status-report.contract.md:22-24,48-50,125-127`；`data-model.md:185,187,193`；`status-digest.contract.md:105,110,116-119`；`plan.md:85,107-113`。13 个 RO id 全部在 C-01…C-13 中有定义 |
| E-03 | MEDIUM | `tasks.md:227-251` 的 19 行表与脚本 beyond-baseline 名单逐名相等（C-48/C-38 在列，C-01/C-04 移出）；`:253` basename 说法已撤回并改为全路径解析 + 名称碰撞披露；`:255` 的 33/34 口径已给出（见 §4.4 的 greps 说明） |
| F-03 | MEDIUM | `tasks.md:152` T028 的 green point 改为 C-42，行内容与 C-42 的「projection / no write」主题一致；C-41 的 entry 半边以「without a second tag」显式不认领；T009（`:88`）保留 C-41。§ WARNING ADJUDICATION（`:215`）的证据指针改为 `tasks-repair-analyze-loop1.txt` + `tasks-repair-round3.txt` |
| F-04 | MEDIUM | `tasks.md:28` GATE-1 改为「no `--deselect`: the baseline name-list is exactly the node-id set T002 captures … there is no docker or hugo suite in this repository（plan.md EP-010 states the premise）」 |
| F-08 | MEDIUM | `contracts/ownership-map.contract.md:37` 改为「exactly one of **five** forms」并列出 `extends`；relation 表 10 行与 `feature-ref.md:119-133` 的 10 行同序同词；T032 的「no relation in one and not the other」可满足 |
| F-09 | LOW | `quickstart.md:72-75` 改为 four fixtures（含 two-seats）+ C-17 的 reason 值域 fixture，「That is five fixture cases in total, not three」 |

### 4.2 New Since Last Run（5 条）

| ID | 严重度 | 为何是新的 |
|----|--------|------------|
| F-10 | HIGH | plan D10 与 C-45 的 exit-status 冲突自 plan 首版（2b24d24e）即存在，round 1/2 均未把 plan 的 D1–D12 块与合同逐条对读，故未识别。`(validated: direct re-read, subagent unavailable)` |
| F-11 | HIGH | C-41/D8/T009/T029 的「two actions」与 T016 的「third action」冲突自 tasks 首版即存在，round 1 的 F-03 只检查了 T028/T010/T025/T039/T043 的 green 归属，未检查 action 集合；round 2 未重查。`(validated: direct re-read, subagent unavailable)` |
| F-12 | MEDIUM | C-03 的 round-1 修复引入 `tasks.md:99,273` 的两处 stale 「three roster fixtures」；round 2 的 F-09 只治了 quickstart 的同一副本 |
| F-13 | LOW | `data-model.md:108` 的 `storage/guidelines/…` 断链自 plan 首版存在；`pre-analyze` 的路径识别不覆盖该形态，前两轮未浮出 |
| G-02 | LOW | EP-010 是 round-1 为修 F-04 而新增的 premise；registry 的 plan 记录仍写 EP-001…EP-009。round 2 的 G-01 只验了「阶段记录齐备」，未复算记录内的计数 |

### 4.3 Carried Over（3 条）

C-04、C-05（LOW，欠指定，均收窄到 owner 文档的声明面）、H-01（LOW，checklist 计数与 Notes 更正）。

### 4.4 Deferred residual（不计入 open findings）

- **A-01 residue**：`requirements.md` 的叙述层仍复述 30 秒（`:30`、`:47`、`:50`、`:292`、`:383`、`:496-498`，另澄清区），`contracts/ownership-map.contract.md:19` 的 "Long-run cadence default (30 s)" 也带数值。SC-006 的扫描域是 `shared/ templates/ skills/ agents/`，requirements/plan 不在域内；round 1/2 已裁为 deferred，本轮不重开。
- **pre-analyze 读数的调用形态**：`--repo .` → advisories 134（全 `missing-path`，13 个交付期路径名）；不带 `--repo` → advisories 0（跳过路径存在性检查）。registry 记录引用的是后者（`advisories=0`），round 2 已记为 deferred；本轮沿用。
- **green-tag 的原文计数**：`tasks.md:255` 写「33 tags + 1 format legend = 34 raw textual occurrences」；实际 `grep -o '\[green: [^]]*\]'` 得 35，因为该说明句自身也含模板字符串 `[green: <contract>#<clause>]`。这是 round-2 建议（「34 = 33 + 1 图例」）的直接落地产物，属自指计数，不重开 E-03。
- **fixture 命名小疵**：`tasks.md:105` 与 `quickstart.md:72` 的「four defect fixtures」把 compliant 也算作 defect；count 与 C-16 一致（四个 fixture、三个具名缺陷），仅命名不精确。并入 F-12 的建议句，不单列。
- **round-2 报告的 advisory 记账**：round-2 正文写 126、归档文件写 124；本轮实测 134。属 prior report 的记账笔误，不影响结论。
- **registry 的 analyze 记录**：`features.md:94` 只写到「analyze 首轮报告 … 已回写」；round 2/3 的复验记录在本报告与 test-evidence 中，registry 的 analyze 阶段记录仍成立（阶段记录义务是「记录该阶段」，不是「记录每次复验」）。

## 5. 契约条款覆盖裁决（`account-clause-coverage.py --spec`，未 `--freeze`）

**脚本读数据（原文摘录）**：`claimed clauses (this feature): 33`；`baseline: … coverage-baseline.txt (573 names)`；`baseline-internal existing uncovered: 573`；`uncovered beyond baseline: 19`；`[fr-uncovered] pass (0) — 22 of 22 FRs cited from citation groups`；`[clause-uncovered] fail (592) — 592 uncovered, 19 beyond the frozen baseline`；`[clause-unparsable] warn (107) — 107 files yield no clause id … 0 of them declare a positive form`；`[coverage-baseline-delta] fail (19) — baseline holds 573 names; 573 uncovered items are baseline-internal and do not block`；`status: uncovered`；exit 1。

**19 条 beyond-baseline 未认领条款（脚本名单）**：`ownership-map#C-48`；`reporter-seat#C-14/C-18/C-21`；`reporting-obligations#C-02/C-03/C-05/C-06/C-07/C-08/C-09/C-10/C-11/C-12/C-13`；`status-report#C-23/C-30`；`supervision-report#C-36/C-38`。

**裁决**：19 个名字与 tasks.md § Clause Coverage Ledger 的 19 行逐名相等，每行都有理由 + 具名 asserting row（本轮复核 T032/T008/T039、T011/T012/T039、T011/T015、T011/T015/T041、T007/T038、T007/T034、T007/T008、T008/T021、T008/T043、T008/T017/T053、T008/T043、T007/T054、T008/T043、T010/T043、T036/T041、T012、T053、T020、T020/T023 均存在于行集）。**结论：无「无理由、无排程」的真缺口；`status: uncovered` 的 19 条是本特性自身的未认领条款（由台账持有），573 条 baseline-internal 不阻断。**

## 6. 汇总表

### 6.1 Coverage Summary

| 通道 | 全集 | 已覆盖 | 裁决 |
|------|------|--------|------|
| FR → 任务行 `[covers:]` | 22 | 22（100%） | E-02 保持关闭（35 行带 covers 标签，共 36 个出现，含 § Format 的 1 个图例） |
| FR → 契约 citation group | 22 | 22（100%） | `[fr-uncovered] pass (0)`；E-05 保持关闭 |
| 契约条款 → 任务 `[green:]` | 52 | 33（63.5%） | 19 未认领全部有台账行（E-03 关闭） |
| SC → 任务行显式 id | 10 | 6（60%） | SC-002…SC-005 由 T042 区间覆盖；SC-009 显式 `not-measured`（E-06 保持关闭） |
| Checklist `[Gap]` 处置 | 17 | 17 | 0 undispositioned（§3） |
| 冻结基线差集 | — | — | `status: uncovered`；19 beyond-baseline 全是本特性自身的未认领条款，非语料债 |

### 6.2 Feature Linkage Summary

| 信号 | 读数 | 置信度 |
|------|------|--------|
| Index 行 087 | 存在；Name/Description/Status=Planned/Details/Spec Path 齐全；Last Updated 含 requirements+clarify+plan+tasks+checklist+analyze(首轮) | high |
| Detail 文件 | 存在；Latest Review 与 Status Tracking 与 index 一致；Status 维持 `Planned` | high |
| Requirement ↔ Feature 意图 | 需求主题与 Feature 描述逐句对应 | high |
| 状态合法性 | `Planned` 合法：tasks/checklist/analyze 都不拥有状态跃迁，且不得回退 | high |
| 阶段记录 | tasks + checklist + analyze 已记录（G-01 不回退）；plan 记录内的 EP 计数 stale → G-02 | high |

### 6.3 Constitution Alignment

| 原则 | 判定 | 说明 |
|------|------|------|
| XIV One Source of Truth | **部分不符合（F-10 / F-11）** | exit-status 与 action 两个封闭集合各有两个定义点（plan vs contract / plan+tasks），其中 F-10 使 SC-005 的声明值不唯一；F-07/F-01 的 XIV 冲突已关闭，`plan.md:85,107-113` 的 Pass 断言在 RO 映射层面成立，在 D8/D10 层面不成立 |
| VII SDD 工作流（Feature Index 每阶段校验/更新） | Pass（附带 G-02） | 阶段记录齐备；plan 记录内 EP 计数 stale 记 G-02（LOW） |
| IV Test-First & Contract-Driven | **部分不符合（F-11）** | T009 以 C-41 判绿，T016 引入第三个 action 会使其失效；其余 red-first 结构完整（T007 已改为 clause id + count 断言） |
| IX / XVII / XVIII（零新机械 / 目录治理 / 命名） | Pass | 无新顶层目录；registry 命名按既有兄弟 |
| 其余 15 条 | Pass（无证据冲突） | `validate-decision-tensions` status=ok；plan 19 行检查除 XIV 外与产物一致 |

### 6.4 Unmapped Tasks

50 行中 15 行无 `[covers:]`：其中 8 行以 `[green:]` 映射契约（T012/T019/T026/T032/T033/T041/T042/T043），7 行两皆无（T002/T005/T025/T040/T044/T045/T046）——均为基线采集、证据、test-pin 或基础设施行，**不欠 FR**；与 round 2 的 15 行一致。

### 6.5 Metrics

| 指标 | 值 |
|------|-----|
| Requirements | 22 FR / 10 SC / 15 A / 12 Edge Cases；522 行 / 32 定义行 |
| Tasks | 50 行（T001–T046 + T051–T054；Setup 5 / Foundational 5 / US1 11 / US2 10 / US3 5 / US4 7 / Polish 8） |
| Contracts | 6 文件 / 52 条款（C-01…C-52） |
| Clause claim | 33 / 52（63.5%），重复认领 0，悬空认领 0（`validate-tasks` 0 error） |
| Findings | Round-3 open 8（0 / 2 / 1 / 5）；本轮关闭 7；新增 5；carried 3；跨轮 distinct 30 |
| 分布（open） | Inconsistency 4（F-10/F-11/F-12/F-13）· Underspecification 2（C-04/C-05）· Checklist 1（H-01）· Feature linkage 1（G-02） |
| Validation | 应验证 2（C/H）；第三方 0；直接重读 2；降级率 n/a |
| Gate readings | `validate-requirements` 0/0；`validate-tasks` 0 error / 11 warning；`validate-decision-tensions` 0/0（2 records）；`pre-analyze --stage plan|tasks` pass / 0 error / 134 advisory（`--repo .`）；coverage exit 1 / status `uncovered` |

## 7. 系统性观察（不抬高任何单行 severity）

1. **round-3 修复确实关闭了两个阻断项**：F-07 的两侧（requirements 八条 + tasks 按 clause id/count 断言）与 F-01 的 20 处消费点全部对齐，且清单/feature-ref/quickstart 的副本同步；这是前两轮少见的「改 owner 同时改全部副本」闭环。
2. **剩余的缺陷全部落在「plan 的 D1–D12 块」与「tasks 的指导文本」这两个此前未被逐条对读的面**：D10 vs C-45、D8 vs C-41/T016、tasks:99/273 vs C-16、registry 的 EP 计数。它们不是新引入的漂移，而是 analyze 的检测面一直只覆盖合同/数据模型/行级 tag，没有把 plan 的设计决策块与合同逐条对照。建议把「plan D1–D12 × 合同条款」的对照加入 analyze 的固定步骤（或在 plan 模板加一个自检表），否则下一轮仍会有同类漏检。
3. **「exactly N」的措辞是这台分析器最可靠的信号**：F-07（exactly five/eight）、F-08（exactly one of four/five）、F-11（exactly two actions）都是封闭措辞的两处定义；F-10 是封闭表（0/3/2）的两处定义。对这类词做一次全 spec grep（`exactly \w+|closed (set|at|three|…)`）并逐条找第二定义点，比逐文件通读更省 token（本轮已实测：两条 HIGH 均由此法定位）。
4. **副本修复的检查清单需要覆盖「指导文本」而不只是「规范文本」**：F-12 的两处 `three roster fixtures` 是 Independent Test 与 Parallel Example——它们不参与机器校验，却是测试作者最先读到的文本；F-09 治好了 quickstart 的同类副本，tasks 的两处仍在。
5. **注册表记录的 stale 计数与 analyze 复验记录是两种不同的义务**：G-02 是「记录内的数字与产物不符」，registry 不记录每轮复验则是设计如此；两者不应混为一谈（本报告分开处理）。

## 8. Next actions

1. **阻断项（按归属阶段，均为一行到数行的有界修复）**
   - **plan**：F-10（改 D10 的一行，使 `0` 行不再包含 nothing-running，与 C-45 逐字一致）；F-11（选择二/三动作后，单向对齐 C-41 标题/正文/judged-by 与 D8——推荐三动作，因 T016/T017/T018/T052 都依赖它）；F-13（`data-model.md:108` 的 owner 路径改为实际存在的 `shared/guidelines/one-source-of-truth.md` 或镜像路径）。
   - **tasks**：F-11 的 T009/T029（若 plan 选三动作）；F-12（`:99`、`:273` 改为 four fixtures，并把「four defect fixtures」措辞改为「four fixtures（三个具名缺陷 + compliant）」，同步 `:105` 与 `quickstart.md:72` 的措辞）。
   - **feature（registry）**：G-02（`features.md:94` 与 `features/087.md:20` 的 EP-001…EP-009 → EP-001…EP-010，或在记录尾补 `EP-010 added 2026-11-06`）。
2. **不阻断**：C-04/C-05（owner 文档补声明）、H-01（checklist 计数与 Notes 更正）。
3. **修复后复跑**：必须重跑 `/speckit.analyze`（Round 4），按本文 ID 集给出 Resolved / New / carried-over 三向 delta；本轮新增的 F-10/F-11/F-12/F-13/G-02 成为下一轮基线。
4. **判据保持**：若下一轮再出现「封闭集合的第二定义点」，直接按 F-10/F-11/F-07 同一模式归并上送，而不是逐条重开等级讨论。

## 9. Wrap-up 记录（Run Determination / Exec Quant / Feedback / Threshold / Token / Docs）

| 步骤 | 执行 | 结果 |
|------|------|------|
| Run Determination | `run-determination.py --action determine --unit-id "/speckit.analyze" --unit-type command --run-id r20261106T040353Z-087a --complexity complex --feature 087-speckit-visualization …` | **duplicate**：该 `(unit, run_id)` 的确定记录已由 round 1 落盘（`20261106T044954Z-…-087a.md`），引擎按「一轮一条」拒绝第二行；未伪造新记录 |
| Exec Quant | `exec-quant.py --action collect --unit-id "/speckit.analyze" --run-id r20261106T040353Z-087a` | **duplicate**：round 1 已采集（`20261106T044957654772Z-98988b68.json`），未写第二行 |
| Feedback Record | `feedback-utils.py --action record --unit-id "/speckit.analyze" --run-id r20261106T040353Z-087a --feature 087-speckit-visualization --feature-id 087 --review … --points …` | **duplicate: true**（`20261106T045013Z-speckit-analyze.md`）：dedup guard 按同一 `(unit_id, run_id)` 不强制重复；本轮 review/points 因而不入库，要点已落在本报告 §0/§7/§9 |
| Threshold Notice | `feedback-utils.py --action status` | `should_prompt: true`（287 条未提交，阈值 10）→ §9.1 的单条非阻塞通知（不暂停、不自动传输） |
| Token Reflection | 三问自评（原文转储 / LLM 代做确定性工作 / 重复读取） | ① 无机器管理数据文件整体注入（`features.md` 只读 087 行、exec-quant/feedback 只读单条；checklist 走定向摘录）；② 所有计数由程序得出（grep/awk/python + 五个 validator），无固定规则代做；③ 一处**重复执行**：首次 coverage 采集经 `tee | head` 被 SIGPIPE 截断（640 行只存 326 行），按 single-run-evidence 纪律重跑并全量落盘——记为 `token-efficiency` 教训「捕获管线不得带提前退出的消费者」。另：六份合同正文（约 40 KB）全量读入，若先取标题 + `*Judged by*` 索引再定向读正文可约减半；该观察属读数效率，不影响本轮结论 |
| Docs Sync Eval | 对照 `docs/concepts/documentation-model.md` 的所有权边界 | **无 docs 同步义务**：本阶段只读 spec 链，未改变 `docs/` 或根入口；本轮 findings 的落点均在 spec 产物与注册表记录内 |

### 9.1 Threshold Notice（非阻塞，单条）

反馈库累积已超过提交阈值。可以运行 `/speckit.feedback`（无参数）让命令自行判断去向；也可以显式要求 `package` 打包后手动发送；或选择本次跳过——不回复即视为跳过，本轮不暂停等待，也不会自动传输。

---

**Evidence integrity**: 本报告所有计数与定位均可由 §1 的命令重放；未运行任何写命令（本文件与三份 `round3-*` 原始读数除外）；`git status --porcelain` 的既有脏文件集合（session / exec-quant / feedback / `.specify/state/`）未被触碰；未 `--freeze`、未改状态脊、未提交任何运行记录。
