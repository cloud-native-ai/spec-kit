# Requirements-Quality Checklist: Stricter Acceptance & Artifact Review — slice 081a

**Purpose**: 以「需求写作的单元测试」形态检查 Feature 081 当前切片（081a）的 requirements / plan / tasks / contracts 是否定义清楚、可判定、可追溯；本清单**不判定实现行为**，也不改写任何上游产物。
**Created**: 2026-11-03
**Depth / Audience**: Standard / Reviewer（brief §2 的 12 个维度全覆盖）
**Feature (Requirement Scope)**: Feature 081「更严格的验收与产物审查」— `.specify/memory/features/081.md`
**Requirements (What)**: `.specify/specs/081-acceptance-hardening/requirements.md`
**Specifications (How, context only)**: `.specify/specs/081-acceptance-hardening/{plan,tasks,data-model}.md` + `contracts/`（仅用于暴露需求缺项、歧义与追溯断点）

**Note**: 本清单由 `/speckit.checklist` 生成，验证 **Requirements (What)** 的质量。`###` 分节对应 brief §2 的 12 个维度（标 `D1`…`D12`）。勾选约定：`[x]` = 已回答且 PASS；`[ ]` = 已回答但 **FAIL**（质量信号，交 `/speckit.analyze` 裁决，本清单不改上游）。每条 FAIL 附 `Gap`（缺什么）与 `Propagation`（下游哪些产物继承它，按 `objective-analysis-gate.md` § 3 作为首字段）。全部证据为**本次静态/定向检查**所得，命令与退出码见 § Probes 与 `test-evidence/checklist-probes.txt`。

---

## D1 Final-path SCs (final 路径验收判据)

- [x] CHK001 — SC-001 是否给出可判定的分母与可计数结果（拒绝点数、放行上限、原因命中率），使「会不会通过」不依赖读者解读？[Measurability, Req §SC-001]
  - **Verdict**: PASS
  - **Evidence**: `requirements.md:201` — 「3/3 拒绝，0 处放行」「3/3 逐字命中封闭集其一（[[STR-008]] / [[STR-009]] / [[STR-014]] 之一）」；采集方法见 `requirements.md:213`（`SC-001 Source`）。

- [x] CHK002 — SC-002 的两半（正路径不误杀 2/2；删掉 smoke 记录后为 `Blocked` 1/1）是否各自给出可判定的观察量与反例形态？[Measurability, Req §SC-002]
  - **Verdict**: PASS
  - **Evidence**: `requirements.md:202`；反例形态与 `data-model.md:196`（`smoke-mutation` = `positive` 删掉 smoke 记录）一致；`requirements.md:120`（Edge Case「smoke test 需要外部环境…要么做成确定性命令，要么 `Blocked`」）给出同一条边界。

- [x] CHK003 — `Path` 标注的形态（行内、行尾、每行恰好一次、封闭二值）是否足以写出逐字匹配器，且 final 集合的取值与「final SC 被 deferred 就必须 `Blocked`」的后果是否都写在同一处可追溯位置？[Clarity / Consistency, Req §FR-001, §FR-002, §A4]
  - **Verdict**: PASS
  - **Evidence**: `requirements.md:135`（标记形态与「每行恰好一次」）+ `requirements.md:30`（A4 给出两处解析器容差证据）；实测 9/9 条 SC 定义行（`requirements.md:201-209`）`**Path**` 字面出现次数 = 1 且为行尾 token。SC-006 行（`:206`）含 `Path` 一词 2 次但只有 1 次 `**Path**`，`data-model.md:21`（V-2）把违规定义为「第二次 `**Path**` 出现」，判定标准是封闭且可机械执行的。final 集合取值与理由在 `requirements.md:206`（SC-006 的 Path 裁决）+ `requirements.md:264`（Clarifications Q3）。deferral 后果见 `tasks.md:19`（DoD-5）/ `tasks.md:31`（GATE-6）。

## D2 Status semantics (`Blocked` 与「081a 后仍 Blocked」的后果)

- [ ] CHK004 — `Blocked` 的转移集与四条新转移是否只在一处定义、其余产物只以指针引用（FR-002/FR-022 要求「其他产物 MUST 只引用不复制」）？
  - **Verdict**: FAIL
  - **Propagation**: `shared/workflow/acceptance-hardening.md`（T005 的 § Feature Status）、`templates/feature-details-template.md`（T012）、SC-009 ④ 的守卫范围（081d）
  - **Gap**: 同一组转移被**全文复述**至少三处——`requirements.md:137`（FR-003 逐条列出四条转移）、`data-model.md:139-150`（§ E-8 完整 `From | To | Allowed | Condition` 表）、`contracts/state-vocabulary.contract.md:13`（SV-03 指定该表为「the `Blocked` row set」）；而 SC-009 ④ 的唯一性守卫范围只覆盖 `templates/` 与 `shared/` 两类路径（`requirements.md:209`），**`data-model.md` 与 `contracts/` 不在其内**，因此这处复述没有任何机械守卫。
  - **Evidence**: `requirements.md:137`；`data-model.md:133-152`；`contracts/state-vocabulary.contract.md:13`；守卫范围 `requirements.md:209`。

- [ ] CHK005 — 「081a 后本特性仍为 `Blocked`」是否被写成**可判定的状态值**（而不只是「不是 Implemented」），并且在该切片关闭时确实可写出该值？
  - **Verdict**: FAIL
  - **Propagation**: `verification.md` 播种（T020）、`.specify/memory/features.md` 行、FR-018 的第三处词表 owner（081d）
  - **Gap**: DoD-5 要求「it is `Blocked`」（`tasks.md:19`），但唯一的机械检查 GATE-5 只断言 awk 取出的第 5 列**不打印** `Implemented`（`tasks.md:30`）。实测该列现值为 `Planned`（`features.md:89` → `col5=[ Planned ]`），因此 GATE-5 在「状态原封不动」时同样通过，无法区分 `Blocked` 与 `Planned`。同时 081a 不向 `features.md` 写入任何值（`tasks.md:175`「Do not advance the feature status」），而承载该值词表的 `templates/feature-index-template.md` 要到 081d 才落地（`tasks.md:202`）。
  - **Evidence**: `tasks.md:19`、`tasks.md:30`、`tasks.md:175`、`.specify/memory/features.md:89`、`templates/feature-index-template.md:20`（只有 `Status` 列，全文 21 行，**无取值域清单**——FR-018 称其为「词表 owner」与实测不符）。

- [x] CHK006 — 第四条件的「用户豁免」是否被定义为可核验载体（谁写、写在哪两处），且「agent 确认不是用户裁定」是否成文？[Clarity, Req §FR-016, §Edge Cases]
  - **Verdict**: PASS
  - **Evidence**: `requirements.md:156`（豁免须落在该转移 owner 已声明的可核验载体）+ `requirements.md:122`（Edge Case：agent 确认与「无异议」都不是豁免）；载体在 owner 内已存在——`templates/feature-details-template.md:84`（waiver 写入 process report 的 code 子节 + 本特性的 `## Latest Review` 记录）。

## D3 Verification vocabulary & ladder

- [x] CHK007 — `blocked` 与 `deferred` 的区别是否写成**判定规则**（而非形容词），使一条记录只能落其中一边？[Clarity, Req §FR-004]
  - **Verdict**: PASS
  - **Evidence**: `requirements.md:138`（`blocked` = 环境无法测量、特性不可验收；`deferred` = 本轮未尝试但特性仍可验收，仅限 `supporting`）+ `data-model.md:44`（V-7 同义重述并给出「仅 `supporting` 路径合法」的约束）。

- [ ] CHK008 — 五项测量阶梯字段名与「非法行」触发条件是否只有一种字面形态，使解析器与夹具能逐字匹配？
  - **Verdict**: FAIL
  - **Propagation**: `templates/verification-log-template.md`（T013）、checker 的 `C-16` 读取子句（T015）、`ladder-mutation` 夹具（T004/T007）
  - **Gap**: 字段名两种写法并存——`requirements.md:138` 与 `tasks.md:107` 写无前缀形态（`blocked_at`、`reduced_measurement`、`reduced_measurement_run`、`why_reduced_insufficient`、`unblock`），而 `data-model.md:35-39` 与模板既有约定写 `SC-NNN_` 前缀（`templates/verification-log-template.md:77`、`:92`）。触发条件也已分叉：需求写「当**存在可用的** reduced measurement 而 `reduced_measurement_run=no`」（`requirements.md:138`），data-model 写「`reduced_measurement` **非空**」（`data-model.md:42`）——「可用」需语义判断，「非空」是机械判定。
  - **Evidence**: `requirements.md:138`、`tasks.md:107`、`data-model.md:35-39`、`data-model.md:42`、`templates/verification-log-template.md:77`。

- [x] CHK009 — smoke 记录的三件（命令原文 / 退出码 / 证据路径）是否在需求、模板与 fixture 三处使用同一组字段名与同一条「每特性恰好一条」约束？[Consistency, Req §FR-005]
  - **Verdict**: PASS
  - **Evidence**: `data-model.md:48-62`（`smoke_command` / `smoke_exit_code` / `smoke_evidence_path`，V-8「exactly one smoke record」）+ `tasks.md:107`（T013 同名三项 + exactly-one）+ `data-model.md:60`（V-9/V-10 给出 `Blocked` 与「不许以需要真集群为借口」的判定）。

## D4 Runtime stack ownership（运行时栈／依赖所有权）

- [x] CHK010 — `Form` 是否封闭，且 `in-scope` 与 `signed-contract` 之间是否给出**按交付方划分**的判据（不是按便利挑选）？[Clarity, Req §FR-009]
  - **Verdict**: PASS
  - **Evidence**: `requirements.md:146`（`in-scope | signed-contract | user-waived`，并明文「`in-scope` 的判据是本特性交付该能力」）+ `requirements.md:265`（Clarifications Q4 逐行落到 RS-001…RS-004）+ `contracts/artifact-schemas.contract.md:16`（AS-06 给出 `not-required` 仅限表达类）。

- [x] CHK011 — 每行的 pin 是否都是**测量所得**而非凭空书写，且测量出处可复核？[Measurability, Req §FR-009, §FR-023]
  - **Verdict**: PASS
  - **Evidence**: RS-001 的 pin 为仓内已声明值 `pyproject.toml:5`（`requires-python = ">=3.8"`，未新增）；RS-002／RS-003 的 pin 取自同一次采集：`test-evidence/plan-runner-pins.txt`（`pytest 9.2.0` / `Python 3.14.6` / `git version 2.54.0 (Apple Git-157)`），与 `requirements.md:189-190` 的「MUST NOT 凭空写一个版本号」一致；`pyproject.toml:41` 只有 `[tool.pytest.ini_options]`、无版本 pin，实测与需求描述相符。

- [ ] CHK012 — 「pin」的定义是否足以跨机复现：一个只存在于某次运行输出里的版本转录，是否满足 FR-009 对 pin（commit / digest / version）的要求？
  - **Verdict**: FAIL
  - **Propagation**: checker 的输入解析（T015）、SC-009 ② 的基线比较（081d）、RS-002／RS-003 的联合验收
  - **Gap**: RS-002／RS-003 的 Pin 单元格不是一个仓内声明值，而是「由 FR-023 在采集基线同一次记录的 `--version` 原文」（`requirements.md:189-190`），且计划明确「nothing was written into `pyproject.toml`」（`plan.md:305`）。需求没有说明：venv 重建 / 换机后 pin 改变是否构成 pin 失效、该由哪条门禁发现。于是「pin」在语义上等于「某台机器某时刻的观察」，无法判定「pin 是否被遵守」。
  - **Evidence**: `requirements.md:189-190`、`plan.md:305`、`test-evidence/plan-runner-pins.txt`。

- [x] CHK013 — 每行的联合验收是否写成一个可运行命令或一个具名 owner（而非散文承诺）？[Measurability, Req §FR-009]
  - **Verdict**: PASS
  - **Evidence**: `requirements.md:188`（RS-001：静态 import 清单为空，机械可判）、`:189`（RS-002：基线重跑同一 pin 上复现失败集）、`:190`（RS-003：实跑 `base..head` + 两个 `--check` exit 0 + 审计前后 porcelain 增量为空）、`:191`（RS-004：smoke 退出码 0 且夹具被生成）。

## D5 Execution premises / inherited blockers

- [x] CHK014 — 每条 `falsified` premise 是否都带 `Decision` 且附证伪证据（而非结论）？[Completeness, Req §FR-010]
  - **Verdict**: PASS
  - **Evidence**: `plan.md:209`（EP-002 = `falsified` + `resolve-in-scope`，证据为 `.venv/bin/specify init …` → `Error: Local templates not found.`）；`plan.md:204` 声明 `falsified` 必须带三值之一的 Decision。

- [x] CHK015 — 依赖特性中所有 `## Deferred` / blocked 记录是否都被逐条处置，且分母是实测而非估计？[Coverage, Req §FR-011]
  - **Verdict**: PASS
  - **Evidence**: 本次实测 — `071/verification.md:66`、`:86` 与 `077/verification.md:77`、`:89`、`:101` 共 5 条 `_status=partial`；`grep -rln '^## Deferred' .specify/memory/features/` 零命中；`deferred_tasks=` 在 `071:96`、`077:107` 均为空。`plan.md:226-233` 的 IB-001…IB-008 逐条覆盖（`resolved` × 3、`inherited` × 3、`not-applicable` × 2），处置率 5/5。

- [x] CHK016 — 三张「前提／环境」表的不叠位边界（A13）是否只写在一处，并从三个承载处都指向它？[Consistency, Req §A13, §FR-019]
  - **Verdict**: PASS
  - **Evidence**: `requirements.md:48`（A13 定义三者的判定对象互斥）；指针就位——`plan.md:220`（本表只承载 dependency-inherited 记录）、`tasks.md:40`（planning-time premises 不在 tasks 复述）、`contracts/artifact-schemas.contract.md:25`（AS-12：同一事实出现两处即缺陷，第二处必须改为指针）。

- [ ] CHK017 — `resolved | inherited | not-applicable` 三个处置值中，「inherited」对本特性提出的义务是否被定义（它要求继承什么、以什么为证据）？
  - **Verdict**: FAIL
  - **Propagation**: `shared/workflow/acceptance-hardening.md` § Inherited Blockers（081b 的 T 行）、`pre-analyze-check.py` 的第四类发现（081b）、SC-005 的「处置率 100%」
  - **Gap**: FR-011 只要求「处置为 `resolved | inherited | not-applicable` 并附证据」（`requirements.md:148`），三个值的语义未定义；`contracts/artifact-schemas.contract.md:23`（AS-10）同样只给字面取值。而 `plan.md:229-232` 实际把 `inherited` 用成了「该结构证据必须由本特性的 SC 重新采集」，这是一个**未被任何 owner 声明的含义**。081b 的确定性检查若按字面执行，只能检查「值在封闭集内」而无法检查处置是否成立。
  - **Evidence**: `requirements.md:148`、`contracts/artifact-schemas.contract.md:23`、`plan.md:229-232`。

## D6 Review composition（四段 + ARC）

- [x] CHK018 — 四段与 ARC 的判定对象是否互斥成文、且「互不代答」是否逐对给出禁止条款，同时两个严重度家族保持不可转换？[Consistency, Req §A3, §A12, §FR-014]
  - **Verdict**: PASS
  - **Evidence**: 判定对象逐段定义于 `requirements.md:25`（①流程 ②产物 ③实现 ④代码 ⑤ARC）；逐对禁止与「ARC 不得由模型判断代替」同在 `requirements.md:27`；实现段与代码段的互不代答在 `requirements.md:154`（FR-014）与 `contracts/review-composition.contract.md:18`（RC-08）；严重度家族 owner 分别在 `skills/internal/review-sdd-process/SKILL.md:116`（`P0/P1/P2`）与 `templates/feature-details-template.md:82`（六级），「无映射表、无转换、无统一分数」在 `contracts/review-composition.contract.md:11`（RC-04）。

- [x] CHK019 — ARC 的载体槽位与三个计数名是否与 review 模板**现存**编号兼容（不重编号、不撞号）？[Consistency, Req §FR-015]
  - **Verdict**: PASS
  - **Evidence**: 现存槽位 `templates/review-template.md:70`（`### 2.1 Code Segment`）；新增槽位定义在 `contracts/review-composition.contract.md:36`（RC-17：`### 2.2`/`### 2.3`/`### 2.4`，「`### 2.1` MUST NOT be renumbered」）；三计数名 `final_pass` / `final_blocked` / `final_deferred` 在 `contracts/review-composition.contract.md:30`（RC-14）与 `data-model.md:181`（E-10）一致。

- [x] CHK020 — A12 的载体是否是运行时可达的具名 owner，且 census 从 3 变 4 的义务连同其守卫更新一起成文？[Clarity, Req §A12, §FR-013]
  - **Verdict**: PASS
  - **Evidence**: 载体路径 `.specify/skills/internal/review-feature-quality/SKILL.md`（`contracts/review-composition.contract.md:23`，RC-10）在镜像布局内可达——`scripts/python/sync-mirrors.py:85` 的 `("skills/internal", ".specify/skills/internal", …)` 是现存镜像对，`.specify/skills/internal/` 目录实测存在；census 与守卫义务见 `contracts/review-composition.contract.md:37-38`（RC-18/RC-19），被更新的守卫 `tests/contract/test_review_feedback_boundary.py` 实测存在。

- [ ] CHK021 — 当某阶段的产物「按阶段应当存在但实际缺失」时，产物段应报缺口还是静默跳过——需求是否给出了可判定的覆盖分母？
  - **Verdict**: FAIL
  - **Propagation**: `skills/internal/review-feature-quality/SKILL.md`（081c）、SC-006 的「覆盖率 = 实测分母」
  - **Gap**: 产物段的判定对象被定义为「当次**存在的**每个阶段产物」（`requirements.md:25`，同义条款在 `contracts/review-composition.contract.md:16` RC-06 列举七个文件）。分母取「存在的」，因此「`tasks.md` 缺失 / `verification.md` 未生成」不会进入分母，也不会产生 finding；而 SC-006 写「覆盖率 = 实测分母」（`requirements.md:206`），分母本身没有被独立来源钉住，缺件因此可以表现为 100% 覆盖。
  - **Evidence**: `requirements.md:25`、`requirements.md:206`、`contracts/review-composition.contract.md:16`。

## D7 Slice boundary / FR coverage

- [x] CHK022 — 每条 FR 与每条 SC 是否都被分配到恰好一个切片，且任务总数在声明的分解上限内？[Completeness, Req §Decomposition & Ceiling, §FR-025]
  - **Verdict**: PASS
  - **Evidence**: `tasks.md:189-218` 逐行覆盖 FR-001…FR-025（含 `FR-009…FR-012`、`FR-013…FR-016` 两处成组行）与 SC-001…SC-009，无遗漏；deferred 切片在 `tasks.md:232-234` 显式列出 081b/081c/081d 及其 FR；任务行实测 20 条（`tasks.md:66-123` T001–T020）≤ 上限 40（`plan.md:313`）。

- [x] CHK023 — 切片未能满足的那部分（SC-001 只到 1/3）是否被写成可计数的欠账并指明关门者？[Measurability, Req §FR-008, §SC-001]
  - **Verdict**: PASS
  - **Evidence**: `tasks.md:198`（FR-008「partial — 1 of 3」并将其余两处指向 081c/081d）、`tasks.md:210`（SC-001「partial — 1/3 … SC-001 cannot pass until all three are wired」）、`tasks.md:222-226`（status consequence 三条），以及 GATE-6（`tasks.md:31`）把「checker 拒绝本特性」变成可执行判据。

- [ ] CHK024 — 契约中为某条 SC 指派的守卫测试模块，是否在 plan 的测试清单与某个切片里都有归属（否则该 SC 的义务没有载体）？
  - **Verdict**: FAIL
  - **Propagation**: SC-009 ④（schema 唯一性）、`plan.md` § Source Code 的 `tests/` 清单、081c/081d 的 `Deferred Slices` 行
  - **Gap**: 两份契约把 `tests/contract/test_acceptance_schema_ownership.py` 指定为 FR-022/SC-009 ④ 的守卫（`contracts/artifact-schemas.contract.md:43`、`contracts/gate-wiring.contract.md:47`），但该模块既不在 plan 的五个红先行契约测试清单里（`plan.md:175-177`、`plan.md:42`），也不在 `tasks.md` 的任何 T 行或 `Deferred Slices` 行里（实测 grep 三个文件零命中；`tests/contract/` 下亦不存在）。`tasks.md:218` 只在文字上把「schema-uniqueness guard test」推给 081d，没有给模块名，于是这条 SC 义务在任务层面没有落点。
  - **Evidence**: `contracts/artifact-schemas.contract.md:43`、`contracts/gate-wiring.contract.md:47`、`plan.md:175-177`、`tasks.md:218`。

## D8 Deterministic checker（封闭原因集／退出码／夹具）

- [ ] CHK025 — 七个封闭原因的字面形态（是否带尾随 `:`、是否带目标后缀）是否在所有产物中逐字一致，使「原因逐字命中封闭集」可机械判定？
  - **Verdict**: FAIL
  - **Propagation**: checker 的 reason 发射（T015）、`test_closure_acceptance_check.py` 的逐字成员断言（T007）、ARC 的原因呈现（081c）、review 与 driver 两处调用点（081c/081d）、**SC-001（final 路径）本身**
  - **Gap**: 三种写法并存——① Shared Strings 表把五个原因定义为**带尾随冒号**的标签（`requirements.md:242-246`：`final-path-not-pass:`、`blocked-without-measurement-ladder:`、`runtime-dependency-not-owned:`、`falsified-premise-undecided:`、`inherited-blocker-undisposed:`，另两个 `zero-final-path-pass` / `status-claims-implemented-but-blocked` 无冒号）；② 契约 C-09 把七个值一律列成**无冒号**形态（`contracts/closure-acceptance-check.contract.md:23`）；③ 正文与计划又在两种形态间混用（`requirements.md:79` 裸写 `runtime-dependency-not-owned`，`plan.md:265` 写 `runtime-dependency-not-owned: RS-NNN`，`tasks.md:109` 又用带 `SC-NNN` 后缀的形态）。SC-001 要求「命名原因逐字命中封闭集其一」（`requirements.md:201`），因此这条不一致直接落在一个 **final 路径 SC** 上。
  - **Evidence**: `requirements.md:201`、`requirements.md:242-246`、`contracts/closure-acceptance-check.contract.md:23`、`requirements.md:79`、`plan.md:265`、`tasks.md:109`。

- [x] CHK026 — 退出码三态与「输入缺失/不可解析」的分支是否写成互斥判据（尤其：缺文件不得被读作 `block`）？[Clarity, Req §FR-006, §Edge Cases]
  - **Verdict**: PASS
  - **Evidence**: `requirements.md:140`（0 = accept、1 = block、2 = 输入缺失或不可解析）+ `requirements.md:118`（Edge Case：checker 缺文件 MUST 以 2 表示输入错误、MUST NOT 读作 [[STR-006]]）+ `contracts/closure-acceptance-check.contract.md:13`（C-02 逐字重复该禁令）+ `contracts/closure-acceptance-check.contract.md:27`（C-10 审计模式下退出码只反映输入有效性）。

- [ ] CHK027 — 夹具集是否足以区分每条原因与该特性的边界规则（尤其「final 与 supporting 混合」这条）？
  - **Verdict**: FAIL
  - **Propagation**: `tests/contract/test_closure_acceptance_check.py`（T007）、`tests/fixtures/acceptance-hardening/`（T003/T004）、SC-001 与 SC-004 的夹具分母
  - **Gap**: Edge Cases 明确规定「只要有一条 final SC 非 `pass` 即 [[STR-007]]，原因点名该 SC；supporting SC 的非 `pass` 不单独阻断」（`requirements.md:123`），但夹具集（`data-model.md:192-200` 七个用例：positive / negative / premise-mutation / runtime-gap-mutation / ladder-mutation / smoke-mutation / audit-history）**没有**「一条 final 失败 + 其余 final 通过 + 一条 supporting 非 pass」的混合用例。`negative` 让所有 final SC 同时非 pass，`:201` 的逐 SC 原因与「supporting 不阻断」两个断言因此没有反例可证伪。
  - **Evidence**: `requirements.md:123`、`data-model.md:192-200`、`tasks.md:69`（T004 只造 ladder-mutation 与 smoke-mutation）。

- [x] CHK028 — 081a 只接一处调用点这一事实，是否在**读 checker 的人会看到的地方**成文并附理由？[Clarity, Req §FR-008]
  - **Verdict**: PASS
  - **Evidence**: `tasks.md:101`（T010 明确 review/driver 两处「asserted as absent-with-reason here and are 081c / 081d work」）、`tasks.md:198`、`tasks.md:222-226`；`contracts/gate-wiring.contract.md:8-10`（GW-01…GW-03 三处调用点分列，理由可追）。

## D9 Smoke

- [x] CHK029 — 「恰好一条」smoke 命令是否在 plan、tasks、gate 与证据路径四处逐字一致？[Consistency, Req §FR-005]
  - **Verdict**: PASS
  - **Evidence**: 四处同一条命令 —— `plan.md:17`、`plan.md:297`、`tasks.md:29`（GATE-4）、`tasks.md:111`（T017）、`tasks.md:241`（Notes）：`bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q`；证据路径统一为 `<spec-dir>/test-evidence/smoke-081.txt`（`tasks.md:29`、`tasks.md:111`、`plan.md:301`）。该命令形态可执行：`scripts/bash/run-tests.sh:29` 把非 `--names-out` 参数原样传给 pytest。

- [x] CHK030 — FR-005 要求覆盖的三件事是否与 smoke 的三条断言一一对应（不多不少）？[Completeness, Req §FR-005]
  - **Verdict**: PASS
  - **Evidence**: 需求侧 `requirements.md:139`（`specify init` / 正负夹具过 checker / `regen-command-copies.py --check`）；实现侧 `plan.md:299`（(a)(b)(c) 三项逐条对应）与 `tasks.md:111`（T017 的 exactly three sub-checks）。

- [x] CHK031 — 「连跑两次退出码一致」与「证据落点固定」是否都是可判定表述（谁跑、写到哪、比什么）？[Measurability, Req §FR-023, §SC-008]
  - **Verdict**: PASS
  - **Evidence**: `tasks.md:29`（GATE-4：同一命令跑两次、退出码相同、证据在固定路径）+ `tasks.md:122`（T019 把两次退出码记入 `notes/quickstart-run.md`）+ `plan.md:300`（断言里无网络、无 wall-clock，故「字节一致」是更强的可观察事实）。

## D10 Two Hats / mirrors

- [x] CHK032 — 每个被改的框架源文件是否都列了镜像/副本目标与再生成命令，且列法经得起镜像引擎核对？[Completeness, Req §FR-021, §FR-024]
  - **Verdict**: PASS
  - **Evidence**: `plan.md:192-200` 逐行给出 source → mirror → verify；本次与引擎逐条核对一致：`scripts/python/sync-mirrors.py:82-89` 的六对为 `templates`（exclude `commands`）、`skills/external → .specify/skills`（exclude `site`,`internal`）、`skills/internal → .specify/skills/internal`、`agents`、`scripts`（`strict=True`）、`shared`；`templates/commands/` 实测**不存在**（与 `plan.md:194` 的「retired」一致）。

- [x] CHK033 — 「不得手改 `.specify/` 镜像」这条规则是否有**测量得到的**零漂移基线支撑（而不是预先写死的期望值）？[Measurability, Req §FR-024, §SC-009 ①]
  - **Verdict**: PASS
  - **Evidence**: 本次实测（命令与退出码见 § Probes）：`regen-command-copies.py --check` → exit 0；`sync-mirrors.py --check` → exit 0，计数 `templates 22 / skills-external 408 / skills-internal 136 / agents 3 / scripts 118 / shared 61`，与 `plan.md:190` 记录的数字逐个相符；两个基线值由 `plan.md:190` 声明为「measured before any edit」。

## D11 Test plan（基线、红先行、任务注解）

- [x] CHK034 — 基线三数字是否被一致引用且明确「不重跑」，同时任务行的 `[blockedBy]` / `[P]` 是否都真实（每个前驱确实产出后继的输入、并行行确实不写同一文件）？[Consistency, Req §FR-023]
  - **Verdict**: PASS
  - **Evidence**: 基线 —— `baseline-failed.txt` 实测 39 行、`test-evidence/plan-baseline-run.txt` 末行 `39 failed, 6970 passed, 7 skipped`，三处引用一致（`plan.md:216`、`tasks.md:20`、`tasks.md:240`）且写明「Do not re-run the full suite」。`[blockedBy]` 逐边核对为真：T011←T008（先有 `path-marker` 测试，`tasks.md:99`→`:105`）、T012/T013←T009、T014←T013（GATE-4 引用的 smoke 三字段先由 T013 定义）、T015←T006,T007,T011、T016←T007,T010,T015、T017←T002,T003,T015、T018←T012…T016、T019←T017,T018、T020←T013,T019。`[P]` 行写出的路径互不重叠：T001（`notes/`）、T002（`src/specify_cli/__init__.py`）、T003（`fixtures/{positive,negative}`）、T004（`fixtures/{ladder-mutation,smoke-mutation}`）；测试四行为四个不同模块。

- [ ] CHK035 — 「在 implement 调用点接入 checker」这条任务指向的步骤号是否与实现载体里实际存在的步骤一致？
  - **Verdict**: FAIL
  - **Propagation**: `skills/internal/implement-feature/SKILL.md`（T016 的编辑对象）、`shared/workflow/feature-integration.md` § Pre-Status-Flip Gate（`shared/workflow/feature-integration.md:40`）、`test_gate_wiring_081.py`（T010 的断言位置）
  - **Gap**: T016 写「`skills/internal/implement-feature/SKILL.md` **step 8**」，而 plan 写「steps 8–9」（`plan.md:260`）；实测该技能的步骤划分是 `### Step 8 — Completion validation`（`skills/internal/implement-feature/SKILL.md:249`）与 `### Step 9 — Pre-Status-Flip Gate and Verification Log`（`:310`），真正的翻转发生点在 Step 9。因此三处指向不同的步骤，T016 的「run the checker before the flip」若按字面落在 Step 8 就落错位置。
  - **Evidence**: `tasks.md:110`、`plan.md:260`、`skills/internal/implement-feature/SKILL.md:249`、`skills/internal/implement-feature/SKILL.md:310`、`shared/workflow/feature-integration.md:40`。

- [ ] CHK036 — 「零新增失败」这条关闭判据在 DoD 与 SC 之间是否同一口径（同一比较单元、同一范围）？
  - **Verdict**: FAIL
  - **Propagation**: SC-009 ②（`requirements.md:209`）、T020 与 GATE 集、081d 的 id 级差集比较
  - **Gap**: SC-009 ② 的口径是集合级且无范围限制——「`head 失败集 − 基线失败集` MUST 为空（0 个新增失败），而 `基线失败集 − head 失败集` MUST 逐条列为已修复项」（`requirements.md:209`）；切片 DoD-6 则把同一判据**收窄为模块范围**——「No new failing test vs `baseline-failed.txt` … **for the modules this slice touches**」（`tasks.md:20`）。收窄后，一个在未触碰模块里新增的失败既满足 DoD-6 又违反 SC-009 ②，两句都没有说明谁优先，也没有说明收窄是「切片内暂时口径」还是「本特性口径」。
  - **Evidence**: `requirements.md:209`、`tasks.md:20`、`requirements.md:221`（`SC-009 Source`）。

## D12 Evidence honesty

- [x] CHK037 — 每条 `pass` 声明是否都绑定命令 / 退出码 / 证据路径（而不是「看起来绿」）？[Completeness, Req §FR-023, §SC-009]
  - **Verdict**: PASS
  - **Evidence**: `plan.md:208`（EP-001 附 `--collect-only` 输出与版本）、`plan.md:216`（EP-009 附基线命令与汇总行）、`plan.md:211`（EP-004 指向 `research.md` § R5 实测）、`requirements.md:213-221` 为每条 SC 指定采集来源；`tasks.md:15`（DoD-1）要求每条任务声明的产物确实存在于其所写路径。

- [x] CHK038 — 「环境缺失 / 测不了」是否被判为 `blocked` 而不是 `pass`，且该判据有反例夹具？[Coverage, Req §Edge Cases, §FR-005]
  - **Verdict**: PASS
  - **Evidence**: `requirements.md:120`（需要真集群/真网络不是豁免）+ `data-model.md:60`（V-10 同义）+ `requirements.md:121`（有可用测量却 `run=no` 判非法）；反例夹具为 `ladder-mutation`（`data-model.md:198`）与 `smoke-mutation`（`data-model.md:199`）。

- [x] CHK039 — 产物中出现的版本、sha、计数是否全部可复核（无凭空值），且新增义务没有把「机械可得的事实」写成估计？[Measurability, Req §A11, §SC-009]
  - **Verdict**: PASS
  - **Evidence**: 版本 —— `test-evidence/plan-runner-pins.txt` 三行原文可复核（pytest 9.2.0 / CPython 3.14.6 / git 2.54.0），无 `pyproject.toml` 侧新增 pin（`pyproject.toml:5`、`:41` 实测）；计数 —— 镜像六项计数由本次 `--check` 复现（见 CHK033），基线 39/6970/7 复现（见 CHK034）；「不可核验编号」的处置规则在 `requirements.md:46`（A11：026 为外部事故代称，任何产物 MUST NOT 把它当作可核验证据引用）。

---

## Probes（本清单的确定性输入，全部只读）

| # | 命令 | 结果 |
|---|------|------|
| P1 | `python3 scripts/python/regen-command-copies.py --check` | exit 0（`OK: all per-tool command copies match the source templates.`） |
| P2 | `python3 scripts/python/sync-mirrors.py --check` | exit 0（templates 22 / skills-external 408 / skills-internal 136 / agents 3 / scripts 118 / shared 61） |
| P3 | `awk -F'\|' '$2 ~ /^ *081 *$/ {print $5}' .specify/memory/features.md` | ` col5=[ Planned ]`（→ CHK005：GATE-5 在状态未变时同样通过） |
| P4 | 逐行统计 SC 定义行的 `**Path**` 次数与行尾形态 | 9/9 行次数 = 1 且以 `**Path**: final\|supporting` 结尾 |
| P5 | `grep -n "_status=partial" .specify/specs/071*/verification.md .specify/specs/077*/verification.md` | 5 条（071:66,86；077:77,89,101）→ 与 `plan.md` IB 行 1:1 |
| P6 | `grep -rln '^## Deferred' .specify/memory/features/` | 零命中 |
| P7 | `wc -l baseline-failed.txt` + 基线日志末行 | 39 行 / `39 failed, 6970 passed, 7 skipped` |
| P8 | `ls templates/commands`、`grep -n MIRROR_PAIRS -A 8 scripts/python/sync-mirrors.py` | 目录不存在（retired 属实）/ 六对与 `plan.md:192-200` 相符 |
| P9 | `grep -rn test_acceptance_schema_ownership` 于 plan/tasks/quickstart + `ls tests/contract/` | 零命中、文件不存在（→ CHK024） |
| P10 | `sed -n '98p' templates/feature-details-template.md`、`sed -n '121p' skills/internal/manage-features/SKILL.md`、`sed -n '20p' templates/feature-index-template.md` + `wc -l` | 前两处有取值域清单；第三处只有 `Status` 列、全文 21 行（→ CHK005） |
| P11 | `grep -n '^### Step 8\|^### Step 9' skills/internal/implement-feature/SKILL.md` | `249:### Step 8 — Completion validation`、`310:### Step 9 — Pre-Status-Flip Gate …`（→ CHK035） |

逐字输出存档：`test-evidence/checklist-probes.txt`。

## Detection disclosure（objective-analysis-gate）

- 同一作者条件**成立**：本清单审计的 requirements / plan / tasks / contracts 由本线的既有阶段（同一模型、连续会话）产出。
- 检测方式：本次为**直接有限读**，非子代理分派——本执行位没有可用的子代理工具（派发在结构上不可得，等同 `objective-analysis-gate.md` § 7 的 subagent-unavailable 情形）。因此本清单所有行按 § 7 以降级形态产出，读者应把每条 PASS 视为「一次有界直读所得」，而非独立第二读者确认。
- 验证波与降级率：**未评估**（无独立验证波，故不报告降级率，也不声称接近零）。
- 为补偿单读者偏差，本次把可由程序判定的事实全部改为程序读数（P1–P9），使结论不依赖模型复述。

## Summary

- **Items**: 39（CHK001–CHK039 连续编号；`## Probes` 与本节不计入项数）
- **PASS**: 28 · **FAIL**: 11
- **Traceability**: 39/39（100%）带 `[Req §…]` / `[Gap]` / `[Ambiguity]` / `[Consistency]` / `[Measurability]` / `[Coverage]` 之一及 owner 锚点
- **分维度分布**：D1 3 · D2 3 · D3 3 · D4 4 · D5 4 · D6 4 · D7 3 · D8 4 · D9 3 · D10 2 · D11 3 · D12 3
- **FAIL 清单（按传播面从大到小）**：
  1. **CHK025** 七个封闭原因的字面形态三处不一致（含尾随冒号与否）→ 直接落在 **SC-001（final 路径）** 的「逐字命中」上；传播到 checker 发射、逐字成员断言、ARC 呈现与两处后置调用点。
  2. **CHK005** 「081a 后仍为 `Blocked`」不可机械判定（GATE-5 只排除 `Implemented`；`templates/feature-index-template.md:20` 无取值域清单）→ 传播到 T020 播种、`features.md` 行、081d 词表。
  3. **CHK004** 转移集被全文复述三处，而 SC-009 ④ 守卫范围只覆盖 `templates/` 与 `shared/`。
  4. **CHK024** `tests/contract/test_acceptance_schema_ownership.py` 只存在于两份契约，不在 plan 测试清单、不在任何切片行（SC-009 ④ 的义务缺载体）。
  5. **CHK036** DoD-6 把「零新增失败」收窄到「本切片触碰的模块」，与 SC-009 ② 的集合级口径冲突。
  6. **CHK008** 五项阶梯字段名（`SC-NNN_` 前缀）与非法行触发词（「存在可用」vs「非空」）两处形态不一致。
  7. **CHK021** 产物段分母只取「当次存在的产物」，按阶段应存在而缺失的产物既不计入分母也不产生 finding。
  8. **CHK027** 缺少「final 与 supporting 混合」夹具，`requirements.md:123` 的边界规则无反例可证伪。
  9. **CHK017** `inherited` 处置值的义务未定义，`plan.md:229-232` 在实际使用一个未声明的含义。
  10. **CHK012** RS-002／RS-003 的 pin 是一次运行输出的转录，未定义「pin 何时失效」。
  11. **CHK035** implement 调用点的步骤号三处不一致（T016 写 step 8、plan 写 steps 8–9、实际翻转在 Step 9）。
- **本清单不作为门禁**：以上 11 项是 requirements/plan/tasks/contracts 的**写作质量信号**，裁决与处置归 `/speckit.analyze`；本阶段未修改任何上游产物。

## Notes

- 逐项复核只需 `## Probes` 的九条命令加各条 `Evidence` 的 `path:line`；无需运行测试套件（本阶段按要求只做静态/定向检查）。
- SC-001 与 SC-002 是唯一两条 `final` 路径判据（`requirements.md:201-202`、`:264`），因此上表中任何影响这两条判据可判定性的 FAIL（CHK025、CHK005）优先于其余项。
- 本清单与 `checklists/requirements.md`（2026-11-01，规划前质量门）是两份**独立历史文件**：前者判「实现前一版规格是否可开工」，本文件判「081a 切片此刻的规格/计划/任务是否可判定」，互不覆盖。
