# Analyze Report — 088-speckit-visualization（/speckit.analyze，2026-11-06，Round 2）

**Unit**: `/speckit.analyze` · **Run ID**: `r20261106T040353Z-087a` · **Stage**: analyze（Round 2，全严重度复核）
**Spec dir**: `.specify/specs/088-speckit-visualization`（`REQUIREMENT_ID=087`，`FEATURE_ID=087`，`MODE=C`）
**Flow class**: `execution` / `source=declaration`（`flow-class-check.py --action lookup --unit-id "spec:088-speckit-visualization"` → exit 0；非表达类，既有门禁集不变）
**Prior report**: `test-evidence/analyze-report-2026-11-06.md`（Round 1，22 条 findings）
**Baselines under analysis**: requirements `142ecc4d` / plan `644ebf35` / tasks `852e0843` / checklist `123e5949`
**性质**: 严格只读。本报告是本阶段唯一写入产物；requirements / plan / tasks / contracts / data-model / quickstart / checklists / 注册表零修改。

## 0. 门禁结论（Gate Verdict）

**未通过（NOT GREEN）**：1 条 CRITICAL + 1 条 HIGH 未处置。

| 严重度 | 条数 | 归属与处置要求 |
|--------|------|----------------|
| CRITICAL | 1 | **F-07（新）**：owner 声明事实集的封闭枚举有两个定义点（requirements 五个 / contract 八个）——违反宪法 XIV，须在 `/speckit.implement` 前修复；归属 **requirements + tasks**（FR-001、T007/T008、feature-ref owners 行） |
| HIGH | 1 | **F-01（carried over，部分关闭）**：round-1 列出的 10 个 `*Judged by*` / INV 指针中 5 处已改对（C-25/C-33/INV-01/INV-07/INV-12），剩余 5 处（C-22/C-24/C-30/INV-02/INV-10）+ 同类新识别 1 处（INV-04）+ C-46 两行 + §116-119 仍把「与 owner 主体不同」的命题挂到同一 RO id；归属 **plan**（contracts / data-model） |
| MEDIUM | 4 | E-03 / F-03 / F-04（carried over，均已收窄）+ F-08（新）；不阻断实施，但会影响 analyze/implement 的覆盖台账与一致性判读 |
| LOW | 4 | C-04 / C-05 / H-01（carried over）+ F-09（新）；建议性 |

**上一轮 1 CRITICAL + 3 HIGH 的复核结果**：

| ID | Round-1 严重度 | Round-2 结论 | 关闭证据（摘要） |
|----|----------------|--------------|------------------|
| D-01 | CRITICAL | **已关闭** | 命题清单已指定唯一 owner：`contracts/reporting-obligations.contract.md:11-17` 声明 C-01…C-13 为 propositions 的唯一定义处；`contracts/status-digest.contract.md:94-98` 把 C-46 表降级为 consumer（只写 "what this guard reads"）；`quickstart.md:204-208` 的 F 前提 1 同步改写。Round-1 建议的三步全部落地。RO-09 主体残差改由 F-01 承载（见 §2.2） |
| F-01 | HIGH | **未关闭（carried over，5 处指针 + T043 措辞已改）** | 已改对：C-25→RO-08（`status-report.contract.md:62`）、C-33→RO-06（`supervision-report.contract.md:30`）、INV-01→RO-05（`data-model.md:184`）、INV-07→RO-06（`:190`）、INV-12→RO-13（`:195`）、T043 措辞（`tasks.md:189`）；仍错：C-22/C-24/C-30/INV-02/INV-10 + 同类新识别 INV-04 + C-46 RO-09/RO-04 两行 + §116-119（§2.2 逐条） |
| F-02 | HIGH | **已关闭** | `requirements.md:335` SC-003 改为「one quiet **beyond** the declared stall threshold … marks the beyond-threshold one `stalled` and the just-under one `slow`」；与 FR-009（`:223-226`）、C-35（`supervision-report.contract.md:43-53`）、US2 AS2（`:98-100`）方向一致；`checklists/framework-visualization-2026-11-06.md:66` CHK027 已标注 resolved |
| E-01 | HIGH | **已关闭** | `requirements.md:222-235`（FR-006 定义恰两个集合、既有 roster 不回溯）、`:334`（SC-002）、`:396-404`（A7）、`:423-429`（A11）同步；`contracts/reporting-obligations.contract.md:71-88` C-04 定义 population；`data-model.md:34-39` E1 明确 not-evaluated；`quickstart.md:214-218` F 前提 5；`feature-ref.md:83-88` roster 说明；`tasks.md:66` T003 name-list 基线 + `:172` T035 按名单读。C-46 的 RO-04 行仍留 `.specify/teams/*/team.md` 括注——作为 F-01 的剩余点位处理（不重新抬高 E-01） |

### 0.1 验证波状态（显式降级，非静默）

- **同一作者门（objective-analysis-gate）**: **未触发**——本轮分析的 requirements/plan/tasks/checklist 由本无人值守链的**其它阶段运行**产出，本 worker 未在本次会话撰写它们（gate owner: `.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires 第 2 条；Round 1 同判）。
- **CRITICAL/HIGH 独立验证子代理**: **不可派发**（本层为 bounded assignment，brief 明确禁止派发子代理）。按 SKILL `references/validation-and-report.md` § Subagent-unavailable fallback 执行**直接受限重读**：F-07、F-01 各给 `(validated: direct re-read, subagent unavailable)` 与 evidence_supported / evidence_not_supported 边界（§2.1/§2.2）。
- **降级率**: n/a（无第三方 validator）；应验证 2 条 C/H，第三方验证 0，直接重读 2。**读侧一致性**：每条 C/H 断言均由 §2 引用的原文逐字支撑。
- **零发现下限**: 本轮非零发现，不适用；但 coverage 通道已逐项复算（§5）。

## 1. 方法与执行轨迹

| 步骤 | 命令 / 动作 | 结果 |
|------|-------------|------|
| 前置脚本 | `bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` | exit 0；`AVAILABLE_DOCS` 含 research/data-model/contracts/quickstart/checklists/feature-ref/tasks |
| 类别读取 | `flow-class-check.py --action lookup --unit-id "spec:088-speckit-visualization"` | `flow_class: execution`，`source: declaration` |
| 覆盖核算（固定步骤，只读） | `python3 .specify/scripts/python/account-clause-coverage.py --spec .specify/specs/088-speckit-visualization`（**未** `--freeze`） | exit 1；`claimed clauses (this feature): 33`；`baseline: coverage-baseline.txt (573 names)`；`[fr-uncovered] pass (0) — 22 of 22`；`[clause-uncovered] fail (592)`（573 baseline-internal + **19 beyond baseline**）；`[coverage-baseline-delta] fail (19)`；`status: uncovered` → §5、E-03 |
| 确定性校验 | `validate-requirements.py requirements.md` | `status: ok`，六标签全 pass，0 error 0 warning（518 行 / 32 定义行） |
| 确定性校验 | `validate-tasks.py tasks.md` | `PASS (with warnings)`：0 error / **11 warning**（7 green-cross-phase + 4 green-path-divergence；作者已在 § WARNING ADJUDICATION 裁决） |
| 确定性校验 | `validate-decision-tensions.py --spec …` | `status: ok`，六标签 0 命中，2 records（scanned 321 lines） |
| 确定性校验 | `pre-analyze-check.py --spec-dir … --stage plan --repo .` | `decision=pass errors=0 advisories=126`（全 `missing-path`，交付前路径；`fr=22 sc=10 tasks=50 files=15`）。不带 `--repo` 时 `advisories=0`（跳过路径存在性检查）——两种读法同判 pass |
| 确定性校验 | `pre-analyze-check.py --spec-dir … --stage tasks --repo .` | `decision=pass errors=0 advisories=126`；同 summary。不带 `--repo` 时 `advisories=0` |
| 检测通道 A–I | 逐产物交叉读（§2） | 25 条 total（15 resolved + 10 open） |
| 检查清单 H 通道 | 60 条逐条分诊（§3） | 17 条 unchecked `[Gap]`：10 covered-by + 7 raised，`undispositioned=0` |

**读入的权威面**：requirements.md（22 FR / 10 SC / 15 假设 / 12 边界情形 / 5 条澄清裁决）、plan.md（19 行宪法检查 / T-001–T-002 / EP-001–EP-010 / D1–D12 / 9 行 Mirror Obligations）、tasks.md（50 行，T001–T046 + T051–T054 / § Clause Coverage Ledger）、contracts ×6（52 条款 C-01…C-52）、data-model.md（E1–E7 + INV-01…INV-12）、quickstart.md（A–H）、checklists ×1 现行文件、feature-ref.md、`features.md` 087 行、`features/088.md`、`constitution.md` v1.16.0（19 原则）。

## 2. Findings（open，10 条）

`propagation_surface` 是每条的第一个字段；severity 由它派生（owner: `objective-analysis-gate.md` rule 3）。

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| F-07 | F 不一致 / D 宪法 | 实现（T007 red-first test → T008 owner 文档 → RO-01 守卫） | **CRITICAL**（新，`(validated: direct re-read, subagent unavailable)`） | `requirements.md:198-202`（FR-001 五条）；`contracts/reporting-obligations.contract.md:21-32`（C-01 恰八条）；`tasks.md:83`（T007 "exactly the five owned facts"）、`:87`（T008 "five owned facts"）；`feature-ref.md:123`（owns 行列五条）；`quickstart.md:26`（eight）；`checklists/…:32,105`（CHK002/CHK054 五条） | owner 文档的「owned-fact 集合」有两个互相冲突的封闭枚举：FR-001/T007/T008/feature-ref 写 **五**（scope、默认周期、reporter 席位、主从汇报、摘要契约），C-01/quickstart A 写 **恰八**（另加 stall 判定引用、越周期触发器、零新机械禁令）。T007 是一条 red-first test 行，按契约作者八条会使其断言失败；按测试作者五条则 C-01/RO-01 失败。宪法 XIV 的「enumerated list MUST have exactly one definition point」被违反；该冲突由 plan 阶段把 C-01 从五改八、而 requirements/tasks 仍停五所引入（remediation-introduced） | 二选一：**(A)** requirements 侧把 FR-001 改为八条（与 C-01 八条逐项对齐），tasks 侧把 T007/T008 的 "five" 改八，feature-ref `owns` 行补三条；checklist 的 CHK002/CHK054 为 dated artifact，可在下一轮 checklist 注记而不回写。**(B)** 若坚持五条，则把 C-01 恢复为五条，并把 stall 引用/触发器/零新机械作为其它条款（C-07/C-08/C-13）单列而非 owned facts。推荐 (A)：C-01 的八条与 C-13/C-07/C-08 的实际要求一致 |
| F-01 | F 不一致 | 守卫实现（T033/T043）与 contract tests | **HIGH**（carried over；`(validated: direct re-read, subagent unavailable)`） | `contracts/status-report.contract.md:22`（C-22→RO-05）、`:47-48`（C-24→RO-03+RO-09）、`:123`（C-30→RO-09）；`contracts/status-digest.contract.md:105`（RO-04 行仍留 `.specify/teams/*/team.md`）、`:110`（RO-09=profile）、`:116-119`（"FR-020's profile fields (RO-09)" / "FR-012's cap (RO-13)"）、`:129-131`（同义复述）；`data-model.md:185`（INV-02→RO-05）、`:187`（INV-04→RO-09）、`:193`（INV-10→RO-13）；旁证 `plan.md:85`（XIV Pass 声称 "every other surface reaches them by id without restating a subject"） | 上一轮 8 处指针错误中 5 处已改对（C-25/C-33/INV-01/INV-07/INV-12），但仍有 6 个消费点与 2 个 C-46 行把「主体不同」的命题挂到同一 id：①**归因**（C-22/INV-02）判给 RO-05，而 RO-05 主体是四要素（position/delta/remainder/blocker），归因是另一事实；②**cadence profile / 切换记录**（C-24 后半、C-30、INV-04）判给 RO-09，而 C-09 的主体是 "the digest contract, by shape"；C-46 的 RO-09 行与 §116-119 仍把 profile 绑到 RO-09（round-1 的相反主体未实质改变，只是被 "what this guard reads" 的抬头包了一层）；③**cap**（INV-10）判给 RO-13，而 RO-13 主体是零新机械，cap 的 owner 是 C-43；④C-46 的 RO-04 行仍以 `.specify/teams/*/team.md` 为默认群体（E-01 的残余），与同行的 "population only" 及 "zero paths ⇒ not-evaluated" 自相矛盾。映射表被当证据（gate rule 4）再次命中 | 按唯一 owner 逐条改：①C-22/INV-02 改判 `tests/contract/test_reporting_obligations.py`（与 C-31 同型），或在 C-05/RO-05 的 reading surface 中显式加入归因字段（二选一，须同一处声明）；②决定 RO-09 主体：推荐保留 C-09 = 摘要契约，把 C-46 的 RO-09 行改为「the owner document 的 digest 段 + 一次 digest 渲染的 bounded/omitted/stale/nothing-running 面」，把 C-24 后半/C-30/INV-04 改判 C-30 的 contract test（T053/IPV-04 不再挂 RO-09），并删除 §116-119 的 "FR-020's profile fields (RO-09)"；③INV-10 改判 C-43，删除 "RO-13" 括注；④C-46 的 RO-04 行删去 `.specify/teams/*/team.md` 括注，改为「T003 name-list 中 recorded membership = in-population 的路径 + `--roster` 提供的路径」。同步修 `plan.md:85` 的 Pass 断言 |
| E-03 | E 覆盖 | tasks 覆盖台账 → analyze/implement 覆盖门 | MEDIUM（carried over） | `tasks.md:227`（"this table is that 19-row list"）、`:229-251`（19 行表）、`:253`（basename 掩蔽说）、`:306`；对照 `test-evidence/tasks-repair-analyze-loop1.txt:53,71`（C-48/C-38 在 beyond-baseline 名单中） | 台账计数已与脚本一致（33 claimed / 19 unclaimed），但**成员错位**：表内把 C-01、C-04 列为 unclaimed，而 `[green:]` 明确由 T008、T038 认领（`tasks.md:87,175`）；同时漏列真正 unclaimed 的 `ownership-map#C-48` 与 `supervision-report#C-38`（脚本 beyond-baseline 名单第 1/19 行）。另，`:253` 的「accountant 按 basename 解析、C-12/C-13 被别家条款掩蔽」说法不成立：`_claims_for` 以 `spec_dir / claim["contract_file"]` 的**完整路径**解析（`scripts/python/account-clause-coverage.py:209-240`）；round-1 的 36 vs 37 差异来自作者把格式图例行 `[green: <contract>#<clause>]`（`tasks.md:48`）计为一条 claim，本轮实测 parse = 33（当前）/ 36（round-1，`validate_tasks.validate(..., claims_out=…)` 复算）。C-18/C-14 的排程（round-1 的真缺口）已关闭 | 修 4 个成员点：C-01/C-04 移出台账（它们已有 green），C-48/C-38 补入（照 T032/T020 的 asserting row 写理由）；删掉或改正 basename 掩蔽段（说明 34 = 33 claims + 1 格式图例）。计数核对命令与 §5 同一读数 |
| F-03 | F 不一致 | tasks → implement 的 red-first 锚点 | MEDIUM（carried over） | `tasks.md:152`（T028 claim C-42）、`:189`（T043 claim C-40）；`test-evidence/tasks-repair-analyze-loop1.txt:14`（声称 "T028 re-pointed C-42 -> C-41"）；`test-evidence/validator-tasks.txt` 尾部（13 warning）vs 现行 11 | 5 处错挂中 3 处已删除（T010/C-12、T025/C-38、T039/C-13），但 T028 仍 claim C-42——其行内容是 C-41 的「命令半边/无渲染逻辑」，而 T009 已 claim C-41；repair evidence 的 "C-42 → C-41" 与树上的 tag 不符（记录失真）。T043 保留 C-40 是作者在 repair evidence §4 的显式裁决（可接受，本报告不再重开）。另 tasks.md § WARNING ADJUDICATION 指向 `validator-tasks.txt`（13 warning），现行读数为 11（`tasks-repair-analyze-loop1.txt`） | 二选一：把 T028 的 tag 改 C-41 并让 T009 的 green 改为「script/CLI 半边」（同一 clause 只能一 tag，需重新分区），或把 T028 改为无 green 的 test row、在台账登记 C-42 的 asserting row；同时把 § WARNING ADJUDICATION 的证据指针改到 `tasks-repair-analyze-loop1.txt`。T043/C-40 维持作者裁决 |
| F-04 | F 不一致 | 实现 GATE-1（测试门） | MEDIUM（carried over） | `tasks.md:28`（GATE-1）；`plan.md:216`（EP-010）；`tasks.md:65`（T002） | Round-1 的计数/引用漂移已修（52 条款、8 场景、四新六改、Mirror 9 行、28 路径均对齐），但 GATE-1 仍写 `--deselect <docker/hugo suites recorded in notes/pre-change-measurements.md>`，而 EP-010 实测「there is no docker or hugo suite in this repository to deselect」，T002 只采 progress-reporting 套件；占位符指向的名单不存在 | 把 GATE-1 的 deselect 占位改为「无 deselect；基线名单即 T002 的 progress-reporting node-id 集」，或直接引用 EP-010 |
| F-08 | F 不一致 | 契约测试（T032）与 feature-ref 关系表 | MEDIUM（新） | `contracts/ownership-map.contract.md:37`（"exactly one of four forms: owns/consumes/amends/preserves"）、`:41-50`（表内使用 `extends`）、`:52-53`（judged-by "no relation appears in one and not the other"）；`feature-ref.md:123-132`（10 行，含 `owns` 与 `consumes` line-registry）；`tasks.md:169`（T032） | C-48 的封闭形式集写「四种」却在表里使用第五种 `extends`（`create-team` 行），且 C-48 的 8 行表缺少 feature-ref 的 `consumes — line-registry` 行与 `owns — 新 owner` 行；按其 judged-by，T032 的「两边无单侧关系」断言无法通过。该不一致在 round 1 已存在但未被识别，本轮全量复核时列入（New Since Last Run） | 把 C-48 的形式集改为五种（owns/consumes/amends/preserves/extends），并把 relation 表补齐为 feature-ref 的 10 行（或明确「本表只列 pre-existing owner，line-registry 的关系归 C-42 的 read 面」并让 T032 按该子集断言） |
| F-09 | F 不一致 | quickstart B 的验证路线（人工复核期望） | LOW（新） | `quickstart.md:71-72`（"three fixtures (compliant / missing-seat / unresolvable-agent) plus one out-of-domain"）；`contracts/reporter-seat.contract.md:61-63`（four fixtures, 含 two-seats）；`tasks.md:105`（T011 four defect fixtures） | C-03 的修复把「两席位」写进 C-16/T011，但 quickstart B 的 verification route 仍写三个 fixture，漏掉 two-seats；C-16 现在要求 four fixtures + C-17 的 out-of-domain，共五个 | quickstart B 的 route (b) 改为「four defect fixtures (compliant / missing-seat / unresolvable-agent / two-seats) 加 C-17 的 reason 值域 fixture」 |
| C-04 | C 欠指定 | owner 文档（T008）声明面 | LOW（carried over） | `requirements.md:208-212,269-273,165-168`；`tasks.md:87`（T008 清单） | 四个 owner 级口径仍无声明：① idle tick 是否可抑制；② long-run 档的计时锚点；③ 阈值与周期的数量关系（阈值 < 周期时首 tick 即 stalled）；④ 宿主时钟跳变/挂起时「tick 序列缺口」与「reporter 停滞」如何区分。T008 的清单未新增这四项 | 在 owner 文档把这四条各写一句声明（T008 的作者清单相应加 4 项），不必改 FR |
| C-05 | C 欠指定 | 行级策略（owner + 渲染器） | LOW（carried over） | `requirements.md:174-175`（预算耗尽）、`contracts/status-report.contract.md:106-114`（C-29）、`contracts/supervision-report.contract.md:110-121`（C-40） | 三条行级策略仍缺：① `reporter-failure` 行是否也须携带四要素（INV-01 说 "every Status Report"，C-29 未点名）；② 派发载荷缺 reporting 字段时的失败模式（C-40 只说 "carries by injecting"）；③ 预算耗尽「仍然报告」只有 Edge Case，无 FR/契约条款 | 在 C-29 明确 failure 行的最小内容；在 C-40 增加一个具名失败条件；把预算规则升为一句契约条款 |
| H-01 | H 清单问责 | checklist 证据（`checklist-selfcheck.json` / § Notes） | LOW（carried over） | `checklists/framework-visualization-2026-11-06.md:142-145`；`:152`（"Gaps worth triaging first" 仍列 CHK027）；`test-evidence/checklist-selfcheck.json` `dimension_hits` | 清单自称 "measured" 的维度计数仍与文件不符：`Gap` 声称 19、实测 17；`Ambiguity` 13→11；`Conflict` 6→4；`Assumption` 3→2（另有 1 条 `Assume:`）。60 items、100% 可追溯、0 非问句三项成立；CHK027 已 `[x]`，但 Notes 仍把它列在待分诊 gaps | 重算四个数字并就地加一行更正；或修 selfcheck 的统计口径（排除 legend/正文命中）；把 Notes 的 CHK027 行标注为 resolved |

### 2.1 F-07（CRITICAL）证据

**evidence_supported**：
- `requirements.md:198-202` —— FR-001 原文「…which owns: the obligation's scope …, the default cadence value, the reporter-seat obligation, the master-reporting duty and the digest's contract」——五条。
- `contracts/reporting-obligations.contract.md:21-32` —— 「The document declares itself the single owner of exactly **eight** facts … naming the eight facts it owns and no others」，逐项列 8 条（含 stall judgement reference / out-of-cadence transition triggers / zero-new-machinery prohibition）。
- `tasks.md:83` —— T007 的 red-first 断言原文是「naming **exactly the five owned facts** and the four pointed-at owners」；`tasks.md:87` —— T008 的作者指令写「(**five** owned facts + four named non-owned owners by path)」。
- `feature-ref.md:123` —— `owns` 行把新 owner 的内容列成五类（scope predicate / long-run cadence default / reporter-seat obligation / master-reporting duty + stall reference / digest contract）。
- `quickstart.md:26` —— Scenario A 的 expected 已改为「eight owned facts (the list contract C-01 fixes)」。
- 两处计数均有封闭措辞（C-01 "exactly … and no others"；T007 "exactly the five"），不是「至多/至少」。
- 宪法 `constitution.md:230-236` § XIV：「an enumerated list … MUST have exactly one authoritative definition point」；重复仅限镜像/测试钉值/日期化记录；T007 的测试钉值钉的是**错误的五条**，不属合法重复。

**evidence_not_supported**：无法判定作者意图是五还是八（两处都无 reconciliation 说明）；不声称该冲突会让 guard RO-01 在实现后必然红（实现者可自行选一边），只声称两条机器可读的封闭断言互斥，且 red-first test 与 contract 不能同时满足。**修复后须以同一 commit 更新 requirements 与 tasks 两侧，否则 F-07 会随任一侧单独修复而再次出现。**

**宪法裁定**：按 Constitution Authority，XIV 的 MUST 冲突记 CRITICAL，不接受 downgrade。

### 2.2 F-01（HIGH）证据

**evidence_supported**：
- `contracts/status-digest.contract.md:110` —— C-46 的 RO-09 行仍为「a captured line set: the profile value recorded per line and the recorded profile switch」；`:116-119` 明写「`FR-020`'s profile fields (RO-09)」——而 owner 侧的 C-09（`reporting-obligations.contract.md:135-146`）主体是「The digest contract, by shape」（bounded summary / stale / nothing-running / cap），两者不是同一命题。
- `contracts/status-report.contract.md:123` —— C-30（two profiles, one selected per run）的 *Judged by* 是 RO-09；`:47-48` —— C-24 的 *Judged by* 含 RO-09 且括注「the override is recorded next to the line's profile」；`data-model.md:187` —— INV-04 判给 RO-09。
- `contracts/status-report.contract.md:22` —— C-22（attribution is mandatory）的 *Judged by* 是 RO-05；`data-model.md:185` —— INV-02（attribution never empty）判给 RO-05。RO-05 的 owner 主体（`reporting-obligations.contract.md:90-100`）是四要素（position/delta/remainder/blocker），C-23（`status-report.contract.md:27-38`）逐字列出四要素，归因不在其中（`shared/guidelines/progress-reporting.md:30-37` 的「汇报内容下限（四要素）」同）。
- `data-model.md:193` —— INV-10（cap/omitted）判给 RO-13；RO-13 的 owner 主体（`reporting-obligations.contract.md:180-188`）是零新机械禁令，cap 的 owner 是 C-43（`status-digest.contract.md:47-57`）。
- `contracts/status-digest.contract.md:105` —— RO-04 行写「the roster paths in `FR-006`'s population only (`.specify/teams/*/team.md` plus every path supplied with `--roster`)」；`.specify/teams/*/team.md` 正是 FR-006 排除的既有 12 个 roster（`requirements.md:222-235` 与 A7），同行又以「zero paths supplied ⇒ not-evaluated」自证 glob 不应是默认群体。
- 已改对的对照：C-25→RO-08（`status-report.contract.md:62`）、C-33→RO-06（`supervision-report.contract.md:30`）、INV-01→RO-05（`data-model.md:184`）、INV-07→RO-06（`:190`）、INV-12→RO-13（`:195`）——证明修复方法本身有效，剩余点位是漏改而非方向错误。

**evidence_not_supported**：13 个 RO id 仍全部存在（C-01…C-13 未被删除或改名），因此不声称守卫的命题集合消失；也不声称某条 SC 必然失败——影响的是「哪个命题判哪条条款」的可执行性与测试锚点。对 RO-09 的两种可能读法（摘要契约 / profile 规则）不替作者择一，只指出 C-09 与消费面目前相反。

### 2.3 MEDIUM 证据（摘要）

- **E-03**：`tasks.md:229-251` 的 19 行表包含 C-01、C-04（实际由 T008/T038 认领），漏 C-48、C-38（脚本 beyond-baseline 名单 `tasks-repair-analyze-loop1.txt:53,71` 在列）；`tasks.md:253` 的 basename 掩蔽说与 `account-clause-coverage.py:209-240` 的全路径解析相悖，round-1 的 36/37 差异可由格式图例 `tasks.md:48` 解释（复算：round-1 tasks parse 36 claims；current 33）。
- **F-03**：`tasks.md:152` T028 的 tag 仍是 C-42（repair evidence `:14` 声称已改 C-41，与树不符）；T043 的 C-40 保留是作者显式裁决（`tasks-repair-analyze-loop1.txt:86-91`），本报告接受；§ WARNING ADJUDICATION 的证据指针仍指向 13-warning 的旧档案。
- **F-04**：`tasks.md:28` 的 GATE-1 deselect 占位与 `plan.md:216` EP-010 直接冲突。
- **F-08**：`ownership-map.contract.md:37` 的「four forms」与 `:49` 的 `extends` 冲突；`feature-ref.md:123-132` 的 10 行关系表 vs C-48 的 8 行表，缺 `line-registry` 的 `consumes` 关系；T032 的「无单侧关系」断言不可满足。

## 3. 检查清单问责（§ H pass）

`unchecked [Gap] 17 + unraised 0 + undispositioned 0`；60 条中 59 条未勾选、CHK027 已 `[x]`（Conflict 类，不影响 Gap 集）。17 条 `[Gap]` 全部给出口径：

| CHK | 标签 | disposition |
|-----|------|-------------|
| CHK003 | Gap | `CHK003 disposition: covered-by requirements.md § FR-021 + § Clarifications (Session 2026-11-06) 第 4 问` |
| CHK005 | Gap | `CHK005 disposition: covered-by requirements.md § FR-011 工作区规则 + data-model.md § E5` |
| CHK006 | Gap | `CHK006 disposition: covered-by plan.md D2 + contracts/reporter-seat.contract.md C-14/C-19` |
| CHK007 | Gap | `CHK007 disposition: covered-by requirements.md § Edge Cases "Two cadence profiles in one session" + contracts/status-report.contract.md C-30 + data-model.md E6 selection_record` |
| CHK009 | Gap | `CHK009 disposition: covered-by contracts/status-digest.contract.md C-44 + contracts/ownership-map.contract.md C-47 stale-bound 行 + data-model.md E5` |
| CHK017 | Gap | `CHK017 disposition: raised-as-finding C-04` |
| CHK018 | Gap | `CHK018 disposition: raised-as-finding C-04` |
| CHK021 | Gap | `CHK021 disposition: covered-by contracts/reporter-seat.contract.md C-16（三缺陷闭集含 two-seats）+ tasks.md T011/T013 + data-model.md E1` |
| CHK023 | Gap | `CHK023 disposition: covered-by contracts/reporter-seat.contract.md C-15 + data-model.md E1` |
| CHK032 | Gap | `CHK032 disposition: raised-as-finding C-04` |
| CHK034 | Gap | `CHK034 disposition: raised-as-finding C-05` |
| CHK036 | Gap | `CHK036 disposition: raised-as-finding C-04` |
| CHK039 | Gap | `CHK039 disposition: covered-by contracts/status-digest.contract.md C-45 + C-42 + tasks.md T027` |
| CHK040 | Gap | `CHK040 disposition: covered-by data-model.md E5 profile_summary + contracts/status-digest.contract.md C-41` |
| CHK044 | Gap | `CHK044 disposition: covered-by requirements.md § FR-006 population + contracts/reporting-obligations.contract.md C-04 + tasks.md T003/T035` |
| CHK046 | Gap | `CHK046 disposition: raised-as-finding C-05` |
| CHK058 | Gap | `CHK058 disposition: raised-as-finding C-05` |

**落点统计**：covered-by 10 条（CHK003/005/006/007/009/021/023/039/040/044），raised-as-finding 7 条（C-04×4、C-05×3）。Round-1 的 four adjudicated items 不变：CHK012 不构成 finding；CHK027 已按修复后的 SC-003 关闭；CHK052 的 normative 半边已由 FR-003/SC-006 修复（剩余叙述性复述见 §4.4）；CHK056 由 FR-016 的 "emitting flow's own" 限定关闭。

## 4. Rerun delta

### 4.1 Resolved Since Last Run（15 条，各附关闭证据）

| ID | 关闭证据 |
|----|----------|
| D-01 | `reporting-obligations.contract.md:11-17`（唯一 owner 声明）+ `status-digest.contract.md:94-98`（C-46 降为 consumer）+ `quickstart.md:204-208`；Round-1 建议的三步全部落地 |
| F-02 | `requirements.md:335` SC-003 方向 + `checklist:66` CHK027 resolved |
| E-01 | FR-006 population（`requirements.md:222-235`）、SC-002（`:334`）、A7（`:396-404`）、C-04（`reporting-obligations.contract.md:71-88`）、E1（`data-model.md:34-39`）、quickstart F premise 5（`:214-218`）、feature-ref（`:83-88`）、T003/T035（`tasks.md:66,172`） |
| A-01 | FR-003 改为「by the profile FR-020 selects」（`requirements.md:208-212`）；SC-006 补扫描域（`:338`）。叙述性复述保留（见 §4.4 的 deferred 残差） |
| C-01 | C-44 指向脚本常量（`status-digest.contract.md:59-69`）+ C-47 stale-bound 行（`ownership-map.contract.md:27`）+ E5（`data-model.md:124`） |
| C-02 | FR-011 工作区规则（`requirements.md:248-256`）+ E5（`data-model.md:113-116`） |
| C-03 | C-16 三缺陷闭集（`reporter-seat.contract.md:45-63`）+ T011/T013（`tasks.md:105,107`）+ E1（`data-model.md:30-32`） |
| E-02 | FR-021 → T015（`tasks.md:109`）、FR-016 → T017（`:111`）；22/22 FR 有 `[covers:]`（§6.1） |
| E-04 | `coverage-baseline.txt` 已冻结（573 names，base-sha `644ebf35`）；status `baseline-missing → uncovered` |
| E-05 | FR citation groups 22/22（`[fr-uncovered] pass (0)`） |
| F-05 | A11/Boundary 行改 registry 为机器可读来源（`requirements.md:423-429,361`）；`features/088.md` 同步 |
| F-06 | E2 定义四名词（`data-model.md:44-51`） |
| G-01 | `features.md:94` 与 `features/088.md:8,22,24,26` 已补 tasks/checklist/analyze 记录；Status 维持 `Planned` |
| C-06 | FR-016 限定 "the emitting flow's own" 并指向 A15（`requirements.md:269-273`） |
| E-06 | T042 显式写 SC-009 的 `not-measured` 条件（`tasks.md:188`） |

### 4.2 New Since Last Run（3 条）

| ID | 严重度 | 为何是新的 |
|----|--------|------------|
| F-07 | CRITICAL | plan 阶段把 C-01 从「五条 owned facts」改为「八条」，requirements/tasks/feature-ref 仍停五条——由 remediation 自身引入 |
| F-08 | MEDIUM | C-48 的 four-forms 文本与 `extends` 用法、以及与 feature-ref 10 行表的差集，在 round 1 已存在但未被识别；本轮全量复核列入 |
| F-09 | LOW | C-03 的修复给 C-16/T011 加了 two-seats fixture，quickstart B 的 verification route 未同步 |

### 4.3 Carried Over（7 条）

F-01（HIGH，部分关闭）、E-03 / F-03 / F-04（MEDIUM，均收窄）、C-04 / C-05 / H-01（LOW）。

### 4.4 Deferred residual（不计入 open findings）

- **A-01 residue**：`requirements.md` 的叙述层仍复述 30 秒（`:30`、`:47`、`:50`、`:289`、`:361`、`:379`，另澄清区 `:492-496`），`contracts/ownership-map.contract.md:19` 的 "Long-run cadence default (30 s)" 也带数值。Round-1 的建议只要求 FR-003/SC-006 的 normative 修复，故本轮记 `deferred`，不重开 A-01；若后续按 XIV 收紧，可把这些叙述改为对 FR-020 的引用。
- **round-1 §6.4 的 unmapped 计数修正**：round 1 写「7 行无 `[covers:]`」；实测 15 行无 `[covers:]`，其中 8 行以 `[green:]` 映射到契约（T012/T019/T026/T032/T033/T041/T042/T043），7 行两皆无（T002/T005/T025/T040/T044/T045/T046，均为基础设施/证据/test-pin 行）。不构成 FR 覆盖缺口。
- **pre-analyze 读数的调用形态**：`--repo .` → advisories 126（全 `missing-path`）；不带 `--repo` → advisories 0（跳过路径检查）。Round-1 报告与注册表记录引用的 0 属后者；本报告以两者并列陈述，不作新 finding。

## 5. 契约条款覆盖裁决（`account-clause-coverage.py --spec`，未 `--freeze`）

**脚本读数据（原文摘录）**：`claimed clauses (this feature): 33`；`baseline: … coverage-baseline.txt (573 names)`；`baseline-internal existing uncovered: 573`；`uncovered beyond baseline: 19`；`[fr-uncovered] pass (0) — 22 of 22 FRs cited`；`[clause-uncovered] fail (592)`；`[coverage-baseline-delta] fail (19)`；`status: uncovered`；exit 1。

**19 条 beyond-baseline 未认领条款**（脚本名单）：`ownership-map#C-48`；`reporter-seat#C-14/C-18/C-21`；`reporting-obligations#C-02/C-03/C-05/C-06/C-07/C-08/C-09/C-10/C-11/C-12/C-13`；`status-report#C-23/C-30`；`supervision-report#C-36/C-38`。

**裁决**：17 条在 tasks.md § Clause Coverage Ledger 有理由 + asserting row（C-12/C-13 的「owner 文本 + 守卫读」理由与 T010/T043、T036/T041 的落点可核）；C-48/C-38 无台账行但实际有 asserting row（T032 的关系表断言、T020 的 forbidden/return 断言）——这是 E-03 的成员错位，而非覆盖不存在。C-18/C-14 的排程（round-1 的真缺口）已由 T011/T012 关闭。**结论：无「无理由、无排程」的真缺口；剩余问题是台账记录准确性（E-03）。**

## 6. 汇总表

### 6.1 Coverage Summary

| 通道 | 全集 | 已覆盖 | 裁决 |
|------|------|--------|------|
| FR → 任务行 `[covers:]` | 22 | 22（100%） | E-02 已关闭 |
| FR → 契约 citation group | 22 | 22（100%） | `[fr-uncovered] pass (0)`；E-05 已关闭 |
| 契约条款 → 任务 `[green:]` | 52 | 33（63.5%） | 19 未认领：17 有台账行 / 2 有 asserting row 但漏台账（E-03） |
| SC → 任务行显式 id | 10 | 6（60%） | SC-002…SC-005 由 T042 区间覆盖；SC-009 显式 `not-measured`（E-06 关闭） |
| Checklist `[Gap]` 处置 | 17 | 17 | 0 undispositioned（§3） |
| 冻结基线差集 | — | — | `status: uncovered`；19 beyond-baseline 全是本特性自身的未认领条款，非语料债 |

### 6.2 Feature Linkage Summary

| 信号 | 读数 | 置信度 |
|------|------|--------|
| Index 行 087 | 存在；Name/Description/Status=Planned/Details/Spec Path 齐全；Last Updated 已含 tasks+checklist+analyze | high |
| Detail 文件 | 存在；Latest Review 已补 tasks/checklist/analyze 三段；Status Tracking 写 next step `/speckit.implement` | high |
| Requirement ↔ Feature 意图 | 需求主题与 Feature 描述逐句对应 | high |
| 状态合法性 | `Planned` 合法：tasks/checklist/analyze 都不拥有状态跃迁，且不得回退 | high |
| 阶段记录 | tasks + checklist + analyze 已记录 | G-01 关闭 |

### 6.3 Constitution Alignment

| 原则 | 判定 | 说明 |
|------|------|------|
| XIV One Source of Truth | **冲突（F-07）** / **部分不符合（F-01）** | F-07：owned-fact 封闭枚举五 vs 八；F-01：消费者把不同主体的命题挂到同一 RO id，plan `:85` 的 Pass 断言不完全成立 |
| VII SDD 工作流（Feature Index 每阶段校验/更新） | Pass | G-01 已关闭 |
| IV Test-First & Contract-Driven | **部分不符合** | F-07 使 T007 的 red-first 断言与 C-01 互斥；其余 red-first 结构完整 |
| IX / XVII / XVIII（零新机械 / 目录治理 / 命名） | Pass | 无新顶层目录；registry 命名按既有兄弟 |
| 其余 13 条 | Pass（无证据冲突） | `validate-decision-tensions` status=ok；plan 19 行检查除 XIV 外与产物一致 |

### 6.4 Unmapped Tasks

15 行无 `[covers:]`：其中 8 行以 `[green:]` 映射契约（T012/T019/T026/T032/T033/T041/T042/T043），7 行两皆无（T002/T005/T025/T040/T044/T045/T046）——均为基线采集、证据、test-pin 或基础设施行，**不欠 FR**。

### 6.5 Metrics

| 指标 | 值 |
|------|-----|
| Requirements | 22 FR / 10 SC / 15 A / 12 Edge Cases |
| Tasks | 50 行（T001–T046 + T051–T054；Setup 5 / Foundational 5 / US1 11 / US2 10 / US3 5 / US4 7 / Polish 8） |
| Contracts | 6 文件 / 52 条款（C-01…C-52） |
| Clause claim | 33 / 52（63.5%），重复认领 0，悬空认领 0（`validate-tasks` 0 error） |
| Findings | Round-2 open 10（CRITICAL 1 / HIGH 1 / MEDIUM 4 / LOW 4）；resolved 15；total 25 |
| 分布（open） | Inconsistency 6（F-01/F-03/F-04/F-07/F-08/F-09）· Coverage 1（E-03）· Underspecification 2（C-04/C-05）· Checklist 1（H-01） |
| Validation | 应验证 2（C/H）；第三方 0；直接重读 2；降级率 n/a |
| Gate readings | `validate-requirements` 0/0；`validate-tasks` 0 error / 11 warning；`validate-decision-tensions` 0/0；`pre-analyze --stage plan|tasks` pass / 0 error / 126 advisory（`--repo .`）；coverage exit 1 / status `uncovered` |

## 7. 系统性观察（不抬高任何单行 severity）

1. **修复引入的新漂移集中在「计数/枚举的复制面」**：C-01 五→八 未同步 requirements/tasks/feature-ref（F-07）；C-16 三→四 fixture 未同步 quickstart（F-09）；C-46 的 reading-surface 改写未触及 RO-09 的实体行（F-01）。三处都是「改了一处、没改它的副本」，正是 objective-analysis-gate 描述的自评盲区。
2. **「what this guard reads」的抬头没有治好主体冲突**：把 C-46 表从「proposition 定义」改名为「读取面」是形式上的单 owner 化，但 RO-09 的读取面仍描述 profile 而不是 digest 契约；形式合规不能替代主体一致（gate rule 4）。
3. **台账的计数一致掩盖了成员不一致**：E-03 的 33/19 计数正确，但 19 行表里 2 行错、2 行漏；「计数对」不等于「集合对」，这正是 `coverage-baseline-delta` 按 name set 而非 count 比较的理由。
4. **记录的真实性仍需按调用形态读**：pre-analyze 的 0 vs 126 advisory 是同一命令两种调用形态，注册表记录只留了一个数字；analyze 侧应把调用形态一并记录（本报告 §1 已双读）。
5. **守卫的可执行面仍有一处群体口径不闭合**：C-46 的 RO-04 行保留 `.specify/teams/*/team.md` 默认 glob，而 FR-006/A7/T003/T035 已把既有 12 个 roster 排除；若实现者照 C-46 实现，E-01 的缺陷会以代码形式回来（F-01 点位 ④）。

## 8. Next actions

1. **阻断项（按归属阶段）**
   - **requirements**：F-07（FR-001 五→八，推荐方案 A）；A-01 的叙事复述可选择一并收为引用。
   - **plan**：F-01（6 个消费点 + C-46 RO-09/RO-04 两行 + `plan.md:85` Pass 断言）；F-08（C-48 五形式 + relation 表补齐/子集化）。
   - **tasks**：F-07 的 T007/T008 "five"→"eight"；F-03（T028/C-42 与 § WARNING ADJUDICATION 证据指针）；E-03（台账 4 个成员点 + 删除 basename 掩蔽段）；F-04（GATE-1 deselect 占位）。
   - **quickstart（plan 面）**：F-09（Scenario B 的 fixture 计数）。
2. **不阻断**：C-04/C-05（owner 文档补声明）、H-01（checklist 维度计数更正）。
3. **修复后复跑**：必须重跑 `/speckit.analyze`（Round 3），按本文 ID 集给出 Resolved / New / carried-over 三向 delta；本次新增的 F-07/F-08/F-09 成为下一轮基线。
4. **重复出现的判据**：若下一轮再出现「改了 owner、未改副本」的 F-class，按 systemic observation #1 把它作为同一模式的上送项，而不是逐条重开。

---

**Evidence integrity**: 本报告所有计数与定位均可由 §1 的命令重放；未运行任何写命令（本文件除外）；`git status --porcelain` 的既有脏文件集合未被触碰（本文件是新文件）；未 `--freeze`、未改状态脊、未提交任何运行记录。
