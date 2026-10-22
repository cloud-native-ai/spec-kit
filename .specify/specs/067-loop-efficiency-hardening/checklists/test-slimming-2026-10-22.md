# 需求质量检查清单：067 框架测试套件瘦身（User Story 5 · FR-011…FR-021 · SC-006…SC-010）

**Purpose**: 验证 2026-10-22 范围扩展（框架测试套件瘦身）的需求质量——完整性、清晰性与跨产物一致性、验收可判定性、边界反例判据、回归防护充分性、依赖与范围自洽、流程合规。这是**需求写作的"单元测试"**，不是测试用例表、不是 tasks.md 复述、不是实现行为验证。
**Created**: 2026-10-22
**Feature (Requirement Scope)**: 067-loop-efficiency-hardening → Feature 058 无人值守 SDD 循环驱动机制（演化规格，状态保持 Implemented）
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md)、[tasks.md](../tasks.md)、[contracts/](../contracts/)、[data-model.md](../data-model.md)、[quickstart.md](../quickstart.md)、[test-evidence/](../test-evidence/) dated records
**Checklist Domain**: completeness / clarity-consistency / acceptance-decidability / boundary-counterexamples / regression-protection / dependency-scope / process-compliance
**Depth / Audience / Focus**: Standard / Reviewer（框架维护者与无人值守循环操作者）/ ① US5 范围 FR/SC 的完整性与三产物一致性；② SC-006…SC-010 的证据链与可判定性；③「提速但不降质」的防护闭环与两槽位、E2 围栏合规

## 判定口径与证据方法

- **判定对象是 Requirements (What)**：`plan.md` / `tasks.md` / `contracts/` / `data-model.md` / dated records 仅用于发现需求缺口、歧义、冲突与溯源问题，不作被评分对象；结论必须能落回需求文本或其记录的裁决。
- **复选框语义（沿 063 清单惯例）**：`[x]` = 生成时已裁决 **PASS**（证据随行）；`[ ]` = **FAIL / [Gap]**（缺口、补正落点与残留风险随行，留待被指名产物的所属阶段补正后在新 dated 清单复核）。本清单生成后原位不刷新。
- **判定值域**：PASS（判据成立且证据唯一可指）/ FAIL（发现矛盾、歧义或不可测项）/ [Gap]（现有产物不足以裁决，须他阶段补正）。
- **同作者门**：本阶段为派发的 fresh-context 执行者；requirements/plan/tasks 由前序阶段子代理撰写，本执行者未参与其写作，未触发 `.specify/shared/workflow/objective-analysis-gate.md` 的同作者委派条件。
- **本阶段测试证据（E3）**：`status=not-run-docs-only`——本阶段只新增本清单，未跑任何测试、未改任何可执行面；文中所有数字均转引自 committed dated record，未运行测试复测，不声称任何测试通过。
- **机械核对已执行（本阶段实际运行的唯一命令类）**：基线失败清单层分布统计（83 名 = 80 contract + 3 unit）、运行器参数透传与 `--names-out` 语义核对、pre-analyze-check 支持面核查（无 checklist stage，故结构校验以本清单自校验节为准）。

## 1. 完整性（Completeness：US5 / FR-011…FR-021 / SC-006…SC-010 无遗漏、无不可测项、无未定义术语）

- [x] CHK001 - US5 的四条验收场景是否每条都有 FR 条款承载，且 FR-011…FR-021 每条都能回指至少一个验收场景或 SC（双向可溯）？ [Completeness, Traceability, Req §US5 A1-A4, §FR-011…FR-021]
  - 判定依据：PASS — 场景 1（墙钟+证据）→ FR-012/FR-011；场景 2（构成审计+台账指向）→ FR-011/FR-015；场景 3（注入定位+定向重跑）→ FR-014/FR-020；场景 4（钉住保留+相对绿）→ FR-018（requirements.md:120-123 ↔ :158-168）。FR-013/016/017/019/021 分别由场景 1 的测量合法性、场景 2 的隔离语义、FR-017 等价加速分支、SC-010、交付面承载；plan §Requirements Coverage 与 tasks §Requirements Coverage 两处映射逐条点名（plan.md:128-133；tasks.md:21-24），无悬空条款。
- [x] CHK002 - tasks §Requirements Coverage 引用的任务 ID 是否全部真实存在（无悬空引用），且 FR-011…FR-021 每条至少一个任务行承载？ [Completeness, Traceability, Req §FR-011…FR-021; Tasks §Requirements Coverage]
  - 判定依据：PASS — tasks.md:21-24 引用的全部 T-id（T001–T038 子集）逐一存在于 Phase 1–9 任务行（tasks.md:91-200）；FR-011→T007/T034+Notes、FR-012→T007/T034、FR-013→Notes+T030、FR-014→T005/T016/T017/T019-T022、FR-015→T002/T004/T020-T022/T035、FR-016→T004/T005/T008/T010/T011/T013/T015、FR-017→Notes（R-7 等价加速=W2 各任务）、FR-018→T002/T019-T020/T023/T025/T036、FR-019→T037、FR-020→T019/T022/T028、FR-021→Path Conventions+T030。
- [x] CHK003 - SC-006…SC-010 每条是否都定义了 Measurement Source，且该 source 的生成义务落到具体任务与执行时点（而非留给实现自行选择）？ [Completeness, Measurability, Req §Measurement Sources :211-215]
  - 判定依据：PASS — SC-006→E1 dated 记录（T034）；SC-007→基线/post id 清单+台账三方核对（T001/T033/T035）；SC-008→钉住名册核对+注入演练差集（T002/T036/T028）；SC-009→注入演练 dated 记录（T028）；SC-010→pyproject diff+检索记录（T037）（requirements.md:211-215；plan §W5 表 plan.md:118-127）。基线 id 清单的生成时点已裁决为 implement 义务并显式声明「不是本阶段遗留缺口」（requirements.md:236；protocol §3 measurement-protocol-2026-10-22.md:44-51）。
- [x] CHK004 - SC-007 基线 id 清单的「基线全量运行 → 清单生成 → 首个合并任务」顺序依赖是否已定义为唯一时点规则，并配机械校验？ [Completeness, Measurability, Req §SC-007; Contract §LED-01; Data §E4]
  - 判定依据：PASS — 时点 = implement 首个涉及合并的任务开工前、且在基线全量运行完成后（requirements.md:212；data-model.md:66-69）；同法再生（V-E4-1）与计数交叉核对（V-E4-2，对照 4553，实质偏差即停并 `ANOMALY:` 上报）由 E4 校验规则与 T001 验收双载体（data-model.md:72-74；tasks.md:91）；T019–T022 全部 blockedBy T001/T002/T007（tasks.md:154-157），顺序约束在依赖图上成立。
- [x] CHK005 - FR-018「钉住类契约测试」的类别词表是否封闭可盘点，盘点范围与类别措辞一致（不会因层分布漏盘）？ [Completeness, Coverage, Req §FR-018; Contract §FB-03; Tasks T002]
  - 判定依据：PASS — 类别封闭列举五类（技能文档节集合钉住、镜像同步检查、宪法双落地 watchlist、确认门准则 SHA 钉住、fast-fail 契约）且措辞限定「契约测试」（requirements.md:165；FB-03 同义 failure-baseline.md:11-14）；盘点程序 = T002(c) 按 FR-018/FB-03 类目从 `tests/contract/` 生成名册（tasks.md:92）。本阶段机械核对：83 名基线失败分布 = 80 条在 tests/contract/ + 3 条 unit（loop-state，非钉住类、归 T027 triage），钉住类（fast-fail 8 名、constitution_double_landing 1 名等）全部位于 contract 层——盘点范围与实际层分布一致（test-evidence/baseline-failures-2026-10-22.txt）。残余注记：未来若在非 contract 层新增钉住类测试，需先扩 FR-018 类目措辞再扩名册扫描面；属范围演化路径，非本需求缺陷。
- [x] CHK006 - 本范围的核心术语（完整运行、冷缓存、开发主机口径、留证台账、名称级失败、等价覆盖）是否各有唯一权威定义点、其余位置以引用到达？ [Completeness, Clarity, Req §FR-011/012/015; One Source of Truth]
  - 判定依据：PASS — 完整运行 owner = FR-011（requirements.md:158）+ clarify 确认裁决（:239）；冷缓存/墙钟/主机 = FR-012（:159）→ 契约 MP-02…MP-07（contracts/measurement.md:10-33）→ 协议 dated record（measurement-protocol-2026-10-22.md:9-32, 76-80），chain 单向；台账 = FR-015（:162）→ E2 字段表（data-model.md:33-50）→ LED-01…08（contracts/consolidation-ledger.md）；名称级失败 = FB-01/FB-04（contracts/failure-baseline.md:6-17）；等价覆盖 = LED-04（:14-17）。未发现同一事实两处独立定义。

## 2. 清晰性与一致性（≤600s 口径、完整运行构成、冷/热缓存、基线失败集相对语义、xdist、台账、失败定位、依赖边界在 requirements/plan/tasks 三处是否一致）

- [x] CHK007 - ≤600 秒预算的测量口径（冷缓存清理范围、墙钟采集方式、warm-up 规则、达标主机）在 requirements FR-012、clarify 裁决、契约 MP、plan W4 四处是否逐项同义？ [Clarity, Consistency, Req §FR-012; Contract §MP-02…MP-07]
  - 判定依据：PASS — 四处一致：冷缓存 = 清理 `.pytest_cache` 与 `tests/`、`src/` 下 `__pycache__` 后首测，清理至运行结束无其他运行，至多一次先于清理的 warm-up 不计证据（requirements.md:159 与 :234；contracts/measurement.md:20-22；plan.md:113）；墙钟 = 包装 epoch 差、pytest 自报仅交叉核对（MP-04 :23-24）；主机 = 2026-10-22 基线开发主机唯一达标口径（MP-07 :31-33；protocol §6 :76-80）。固定命令逐字钉于 MP-02（:10-19），plan/tasks 只引用不复制（plan.md:113；tasks.md:106/196）。
- [x] CHK008 - 「完整运行」构成要素（单次调用、无路径/`-k`/`-m` 过滤、三层全执行、含收集与夹具时间、deselected=0）在 FR-011、clarify 确认裁决、MP-05、US5 场景 2 之间是否闭合无缺漏？ [Clarity, Consistency, Req §FR-011, §US5 A2; Contract §MP-05]
  - 判定依据：PASS — 五要素在四处逐一对应（requirements.md:158、:121、:239；contracts/measurement.md:25-28）；MP-05 把违反任一要素定义为「无论墙钟数字如何一律无效证据」，与 Edge Case「以任何形式少跑一律判不达标」（requirements.md:134）同一语义；T007/T034 把 MP-05 列为有效性判据（tasks.md:106/196）。
- [x] CHK009 - 基线失败集的权威定义（83 名全量 FAILED 清单 vs 109 条 lastfailed provisional）是否在所有产物中一致采用「全量清单权威、cache 记录退役」的分层时序语义？ [Consistency, Measurability, Req §SC-008; Contract §FB-01; Data §E3]
  - 判定依据：PASS — 权威 = 2026-10-22 全量 FAILED 清单（requirements.md:237；FB-01 contracts/failure-baseline.md:6-8；E3 data-model.md:52-61；baseline-full-2026-10-22.md:33-35）；109 条 lastfailed 显式标注 provisional 且被 FB-01 声明退役、不再用于判定（requirements.md:32 保留为 dated 背景 + :237 裁决覆盖；failure-baseline.md:7-8）；SC-008 的相对绿语义（不新增名称级失败）三处同文（requirements.md:201；FB-02 :9-10；baseline-full:35）。
- [x] CHK010 - xdist 的「准入」（requirements/clarify）与「本 spec 不采用」（research/契约/plan/tasks）是否为无冲突的两级表述，且 FR-017 的等价加速分支有明确承载？ [Consistency, Req §FR-017; Contract §RC-03; Research R-7]
  - 判定依据：PASS — 准入是依赖政策（允许 dev-only 并行依赖、三条件约束，requirements.md:45、:164、clarify :233）；不采用是本 spec 的采用决定（R-7 research.md:86-94；RC-03 contracts/runner-contract.md:11-15；plan.md:116；tasks.md:79），两层不矛盾；未采用时的达标路径 = FR-017 末句等价加速分支，由 W2 各任务合计承载（plan.md:87-99；tasks.md:22），串行默认路径经 RC-03/MP-02 保持为唯一测量口径；FR-017(c) 串行可用性因「默认即串行」而天然满足。
- [x] CHK011 - 台账处置词表与行粒度：FR-015 的三值（删除/合并/保留）、LED-02/E2 的四值（deleted/case-merge/file-merge/retained）、clarify 的粒度对应规则是否一致？ [Consistency, Clarity, Req §FR-015; Contract §LED-02; Data §E2]
  - 判定依据：PASS — 需求使用粗粒度词表，契约按 clarify「文件级与用例级合并均允许、台账行粒度与合并粒度对应」（requirements.md:238、:47）把「合并」细分为 case-merge/file-merge，属精化而非冲突；`deleted` 行必须携带 retained_equivalent_id 否则无效（LED-02 contracts/consolidation-ledger.md:10-11；V-E2-3 data-model.md:49-50）与 SC-007 零静默删除、FB-07 禁止以删除处置失败同向（failure-baseline.md:30-31）；追加式与 date/commit 归因三处一致（FR-015 requirements.md:162；LED-03 :12-13；clarify :238）。
- [ ] CHK012 - 符号「E2」在 067 工件集内的指涉是否唯一？ [Consistency, Clarity, Tasks T002/T007/T034/GATE-6; Data §E2; 063 Efficiency-Model §E2]
  - 判定依据：FAIL — 同一符号在 tasks.md 内并存两个指涉：T002 的「E2 行字段」（original_id/disposition/…）= data-model.md §E2 ConsolidationLedger 台账行（tasks.md:92；data-model.md:33-50），而 GATE-6/T007/T034 的「E2 行/E2 台账」= 状态脊 `<!-- test-budget -->` 围栏槽位行（063 efficiency-model.md:98 语义；tasks.md:46、:106、:196）。两个「E2 行」都是 implement 期由执行侧写入的行式记录，implement 子代理可能把台账行写进脊围栏或把槽位行写进台账文件。既有机械护栏能兜底：GATE-6 审计脊围栏形态（tasks.md:46）、LED-05 join 只对账台账文件（contracts/consolidation-ledger.md:18-28）——错写会在收口被拦，但将造成 implement 期返工。
  - 缺口：跨产物符号冲突，属 tasks/plan 阶段产物缺陷，非 requirements.md 文本缺陷（requirements.md 未使用 E2 指涉任一实体）。
  - 建议处置（落点 = tasks.md Notes 红线节或 data-model.md §E2 标题，本阶段不改他阶段产物）：在 tasks.md Notes 加一行指涉注记——「GATE-6/T007/T034 的 E2 = 063 状态脊 test-budget 槽位台账（efficiency-model §E2）；T002 的 E2 = data-model §E2 ConsolidationLedger」，或将 T002(a) 措辞改为「data-model §E2 行字段」以消歧。残留风险见 § 裁决汇总。
- [x] CHK013 - 计数口径披露（4553 用例、234/25/9 vs 110/12/6 slow-pattern 两口径）是否诚实分离「驱动者盘点口径」与「可复算口径」，且不进入任何判据分母？ [Consistency, Clarity, Req §现状锚点; Notes test-slimming-scope]
  - 判定依据：PASS — 两口径差异显式披露并给出 dated 记录指针（requirements.md:29、:48；notes/test-slimming-scope-2026-10-22.md）；进入判据的唯一计数 = 基线全量 collected 4553（SC-007 分母经 V-E4-2 与 E1 layer_counts 交叉核对，data-model.md:72-74；baseline-full-2026-10-22.md:14），slow-pattern 计数只作设计动机、不充当达标或否定判据。
- [x] CHK014 - 交付面范围在 FR-021、RC-06、plan Project Structure、tasks Path Conventions 四处是否规范一致（范围估计的内部张力是否不影响规范面）？ [Consistency, Scope, Req §FR-021; Contract §RC-06; Tasks §Path Conventions]
  - 判定依据：PASS — 规范面四处同文：tests/（用例、夹具、conftest）+ 运行器（如需）+ pyproject 开发依赖组 + 本 spec 留证；MUST NOT 改 src 运行时行为；驱动面仅引用性更新（requirements.md:168；contracts/runner-contract.md:23-26；plan.md:44、:156-162；tasks.md:71-72）。披露一处非规范性张力：plan Scale/Scope 估「8–15 个文件」而 W3 折叠面按 P-5 盘点约 40 文件函数级删除（plan.md:45 vs :108）——估计值自相矛盾，但估计不进入任何门判据，tasks 以机械分批（T020–T022 字典序三分，tasks.md:155-157）替代估计，真实边界由 SC-007/LED-05 把守。
- [x] CHK015 - FR-013「运行器契约不变」与 T001/T033 依赖的 `--collect-only` 透传、`--names-out` 语义、`# test runner:` 头行剥离是否机制可行且互不冲突？ [Consistency, Measurability, Req §FR-013; Contract §RC-01/RC-02; Tasks T001/T033]
  - 判定依据：PASS — 本阶段实读运行器：参数循环对未知参数（含 `--collect-only -q`）原样直通 pytest（scripts/bash/run-tests.sh:27-32、:45），`--names-out` 语义与 RC-02 逐条吻合（排序 FAILED 名单、剥后缀、退出码 = pytest 结果，:22-24、:35-43），`# test runner:` 头行存在且 T001 已把剥离列入步骤（:34；tasks.md:91）；RC-01 要求入口/透传/解释器解析不变，T001/T033 只消费透传不触碰契约（tasks.md:91/195）。

## 3. 验收可判定性（每条 SC 的证据是否存在、由哪个任务产生、是否堵死伪造与外推通道）

- [x] CHK016 - SC-006 的达标主张是否堵死估算、外推、子集运行、重试包装四条伪造通道，且证据字段齐备可审计？ [Measurability, Req §SC-006; Contract §MP-04/05/08/09; Data §E1]
  - 判定依据：PASS — 达标主张 MUST 引用已提交的 E1 记录、估算/外推/子集运行不构成主张（MP-08 contracts/measurement.md:34-36）；有效性五判据含 deselected=0（MP-05 :25-28）；测量禁入重试/循环包装（MP-09 :37）；墙钟只认包装 epoch 差、自报仅交叉核对（MP-04 :23-24；V-E1-3 data-model.md:31）；E1 全字段 + V-E1-1 缺字段即无效证据（data-model.md:14-29）；>600 s 唯一出口 = RC-04 显式升级（contracts/runner-contract.md:16-20；GATE-4 tasks.md:44）；驱动者 U4 独立复核字段完整性（plan §W5 plan.md:123）。
- [x] CHK017 - SC-007 的集合核对是否机械可执行、方向唯一、两侧同法（无「谁算消失」的裁量空间）？ [Measurability, Req §SC-007; Contract §LED-05/06/08; Data §V-E4-1]
  - 判定依据：PASS — 差集方向钉死 `comm -23 baseline-ids post-ids`（LED-05 contracts/consolidation-ledger.md:18-28）；两侧必须同一收集方法（V-E4-1 data-model.md:72；T033 与 T001 同法，tasks.md:195）；case 行按全 id、file 行按声明前缀机械展开 join（LED-05；clarify requirements.md:238），unmatched=0 为唯一过线（LED-06 :29-30；GATE-2 tasks.md:42）；post-only 新增 id 仅报告性列出（LED-08 :35-36），避免新增面误判为删失。
- [x] CHK018 - SC-008 的三项判据（名册 ⊆ post 100%、名称级差集为空、基线钉住负债闭环）是否各自有唯一命令级判据与指名产出任务？ [Measurability, Req §SC-008; Contract §FB-04/05/06; Tasks T002/T025-T027/T029/T036]
  - 判定依据：PASS — ①名册核对：T002 生成名册（tasks.md:92）→ T036 名册 ⊆ post id 清单 100%（:198；FB-03）；②差集：closure 日志提取 FAILED 名（FB-04 认可的等价形态，与基线侧同法同为日志提取，tasks.md:198；failure-baseline.md:15-17）→ `comm -13` 为空（FB-02；GATE-1 tasks.md:41）；③负债：T025–T027 逐名三选一（tasks.md:169-171）→ T029 按 V-E5-1…3 机械闭环（:173；data-model.md:82-86），debt 行必须指向「非本范围引入」的 dated 负债记录（FB-06 failure-baseline.md:26-29）。
- [x] CHK019 - SC-009 的「100%」判据分母是否已由需求文本自身定义，样本量（注入演练单点）是否足以支撑该判据？ [Measurability, Req §SC-009, §US5 Independent Test; Contract §FB-08/09]
  - 判定依据：PASS — 分母 = 注入演练中的注入失败集，由 SC-009 判据句「（判据 = 注入演练 dated 记录）」与 Measurement Sources 显式钉死（requirements.md:202、:214）；US5 Independent Test 同义使用单数「注入单行失败」（:116）；演练验证的是机制（parametrize id 携带行标识 → node id 唯一可定位 + 定向重跑复现，FB-08/09 failure-baseline.md:32-38），折叠面的批量核对由 T022 承担（「失败形态全部可定位到参数行」，tasks.md:157）——机制证明 + 面上核对两层合起来覆盖「定位不退化」，单点注入对本判据充分。
- [x] CHK020 - SC-010 的三项检索是否全部有命令级判据，且「新增面为 0」以 diff 基点操作化（不误报既有匹配）？ [Measurability, Req §SC-010; Contract §RC-08; Tasks T037]
  - 判定依据：PASS — T037 三项：`git diff <实施基点>..HEAD -- pyproject.toml` 运行时段 diff 为空；测试侧新增依赖（预期零）全在开发组；`grep -rnE "urllib|requests|httpx|socket" tests/` 仅既有匹配、新增面为 0（tasks.md:199）——「新增面」以实施基点 diff 划定，避免把仓库既有匹配误判为违规；RC-08 的收口验证三要件与之一一对应（contracts/runner-contract.md:32-36）；quickstart S7 提供操作手册（quickstart.md:72）。
- [x] CHK021 - GATE-1…GATE-7 是否与 DoD-1…7 及 SC-006…SC-010 形成完整映射，且每个 check 都是机械命令（无主观判定入口）？ [Measurability, Tasks §DoD/GATE]
  - 判定依据：PASS — 七门全部命令化：comm -13 空（GATE-1）、LED-05 join unmatched=0（GATE-2）、任务行 grep=0（GATE-3）、E1 文件存在 + wall ≤600 或含 RC-04 段（GATE-4）、validate-tasks/pre-analyze/decomposition 退出 0（GATE-5）、audit-test-budget `baseline:1 closure:1`（GATE-6）、镜像 `--check` 本对零 drift + 全仓零 NEW drift（GATE-7）（tasks.md:41-47）；DoD-1…7 逐条对应证据落点（:29-35）；SC-006→GATE-4、SC-007→GATE-2、SC-008→GATE-1、SC-010→T037 判据、槽位纪律→GATE-6，映射完整。

## 4. 边界与反例（删层/默认过滤/伪绿/长期 `-k`/静默删测/并行污染/夹具污染是否有明确判据）

- [x] CHK022 - 「删层 / 把整层移出完整运行」是否有需求级禁令与机械拦截点双重覆盖？ [Edge Cases, Req §FR-011, §Out of Scope, §Edge Cases; Contract §MP-05]
  - 判定依据：PASS — 需求级：FR-011 禁止把某层移出完整运行（requirements.md:158）、Out of Scope 排除「重定义为跳过任一层/删除整层测试」（:184）、Edge Case「整层移除…一律判不达标」（:134）；机械级：E1 layer_counts 三层计数 + MP-05 三层全执行有效性判据（contracts/measurement.md:25-28；data-model.md:24），US5 场景 2 与 T035 层计数交叉核对（requirements.md:121；tasks.md:197）。
- [x] CHK023 - 「默认过滤器」「长期 `-k` 子集达标」「诊断性标记改变构成」三个变体是否各有判据？ [Edge Cases, Req §FR-011, §Edge Cases; Contract §MP-02/05/10, §RC-05]
  - 判定依据：PASS — 默认追加 `-k`/`-m` 被 FR-011 点名禁止（requirements.md:158）；「长期默认 `-k` 子集达标」在 Edge Case 单列（:133）并进 Out of Scope（:184）；deselected>0 直接使测量记录无效（MP-05 contracts/measurement.md:25-28），且 MP-02 固定命令逐字不含过滤参数——合法记录在构造上不可能携带过滤；诊断性标记（如 slow）必须构成中立（MP-10 :38-39；RC-05 contracts/runner-contract.md:21-22），构成改变的标记即违约。
- [x] CHK024 - 伪绿（把未跑/waived 写成 pass、债务记录声称 green）是否有封闭判据并落到本范围的收口产物？ [Edge Cases, Req §FR-006/FR-018, §Edge Cases; Contract §FB-06; Tasks Notes]
  - 判定依据：PASS — FR-006 禁止任何产物把未跑测试写成 pass/green（requirements.md:150）；Edge Case 豁免必须留原文、review 必须看到（:129）；FB-06 债务记录永不声称 green（contracts/failure-baseline.md:26-29）；tasks Notes 把「不声称任何测试通过、green 均为须实际达成并留证的预期」立为本文件红线（tasks.md:82），T032/T038 verification 强制记录跑了/没跑/waiver 原文（tasks.md:185/200）。
- [x] CHK025 - 「静默删测」（无台账条目而从完整运行消失）是否有机械判据且失败后果落在收口审计？ [Edge Cases, Req §FR-015, §SC-007; Contract §LED-06]
  - 判定依据：PASS — FR-015 把该形态直接定义为「一律视为静默删除，收口审计判不通过」（requirements.md:162）；LED-06 把 unmatched>0 定为审计失败（contracts/consolidation-ledger.md:29-30）；GATE-2/T035 双载体执行（tasks.md:42/197）；「无台账即静默删除」的核对方法在 clarify 已定案为确定性脚本对账（requirements.md:238）。
- [x] CHK026 - 并行污染与夹具污染（共享临时目录/端口/顺序依赖、跨用例 fixture 泄漏）是否有判据、修复路径与「不得以关闭并行冒充达标」条款？ [Edge Cases, Req §FR-016/FR-017, §Edge Cases; Plan §W2 行 4; Tasks T015/T018]
  - 判定依据：PASS — Edge Case 并行相互污染必须修复隔离后重测、不得关并行仍主张并行达标（requirements.md:135）；FR-017(b) 受影响用例可并行隔离为采用前提（:164）；FR-016 复用不得改变隔离语义、相互影响必须显式隔离修复并记录（:163）；夹具污染在 plan W2 行 4 风险列点名（c9 裸起点语义，plan.md:95），T015 每用例独立克隆、T018 跨用例无污染核对落地（tasks.md:141/144）；xdist 本 spec 不采用，该分支处于休眠但判据完备。
- [x] CHK027 - 测量包装反例（重试/循环包装、降级串行运行冒充达标）是否有判据？ [Edge Cases, Req §Edge Cases; Contract §MP-09, §RC-03; Protocol §7]
  - 判定依据：PASS — MP-09 禁止测量运行包在重试或循环包装里（contracts/measurement.md:37），clarify 确认裁决同句重申（requirements.md:239）；降级串行运行永不作为达标证据（requirements.md:137；RC-03 contracts/runner-contract.md:11-15；protocol §7 measurement-protocol-2026-10-22.md:82-89）；新增依赖缺失时的显式降级 + 记录义务同条覆盖（:137）。
- [x] CHK028 - 「为提速引入运行时/联网依赖」是否有「检出即判不达标并回退」的需求级判据？ [Edge Cases, Req §FR-019, §Edge Cases, §Out of Scope; Contract §RC-08]
  - 判定依据：PASS — Edge Case 直接规定检出即判不达标并回退该改动（requirements.md:139）；FR-019 三禁（运行时依赖、联网步骤、常驻服务）+ 无网可跑（:166）；Out of Scope 双列（:185）；SC-010 给出检索判据（:203），T037 执行（tasks.md:199）。

## 5. 回归保护（钉住强度/完整运行计数/名称级差集/注入演练是否足以防止「提速但降质」）

- [x] CHK029 - 合并与折叠路径上的钉住强度（字面量保留、断言强度不降、额外断言不丢失）是否逐点有守卫？ [Regression, Req §FR-018; Contract §LED-07, §FB-03; Plan §W3; Tasks T020/T025]
  - 判定依据：PASS — LED-07 逐点规定：合并钉住保留字面主体、被合并钉住的额外断言随幸存用例保留、强度不降（contracts/consolidation-ledger.md:31-34）；FB-03 同义 + 有意更新须记录理由（failure-baseline.md:11-14）；T020 每批折叠执行 LED-07 核对（tasks.md:155）；T025 陈旧钉住更新必须按 owner 事实并记录理由（:169）；W3 论证钉住强度只增不减——共享套件覆盖引擎清单全部文件对、引擎新增对自动入列（plan.md:106-107）。
- [x] CHK030 - 名称级差集防护的两侧提取方法是否同构，检出能力是否经注入演练证明而非仅声明？ [Regression, Req §SC-008; Contract §FB-04/08; Tasks T028/T036]
  - 判定依据：PASS — 基线侧与 post 侧同为「运行日志提取 FAILED 名、剥离前缀排序一行一条」（baseline-failures-2026-10-22.txt 的来源即基线日志；T036 closure 日志同法，tasks.md:198；FB-04 认可等价形态 failure-baseline.md:15-17）；差集方向 `comm -13` 唯一（GATE-1 tasks.md:41）；检出能力由 FB-08 注入演练实证「差集 100% 命中且仅命中注入名」而非声明（failure-baseline.md:32-35；T028 验收三项全中，tasks.md:172）。
- [x] CHK031 - 完整运行计数的回归核对（三层计数交叉核对）与 id 级集合审计是否互补，计数变化是否必须可由台账解释？ [Regression, Req §SC-007; Tasks T033/T035]
  - 判定依据：PASS — id 级 LED-05 join 是主判据（每条消失 id 必须对上台账行），层计数交叉核对（contract 3428 / unit 734 / integration 391）是辅证（T035 tasks.md:197）；行数偏差的预期形态在 T033 验收预声明「= 基线 − 折叠数 + 新增数」并须在审计中解释（tasks.md:195）——计数对不上而台账解释不了时，审计两道判据（LED-06 join + 计数解释）都不会放行。
- [x] CHK032 - 「提速但降质」的防护空间是否被四个独立守卫 + 依赖边界闭合（构成/覆盖/漂移/定位）？ [Regression, Req §FR-011/FR-015/FR-018/FR-020, §SC-006…SC-010]
  - 判定依据：PASS — 构成守卫：FR-011 + MP-05（什么算一次完整运行不可谈判）；覆盖守卫：FR-015 + SC-007 + LED-05/06（消失必留证）；漂移守卫：FR-018 + SC-008 + FB-03/04（钉住保留 + 零新增名称级失败 + 演练证明检出）；定位守卫：FR-020 + SC-009 + FB-09（行级可定位 + 定向重跑复现）；外加 SC-010 依赖边界（不靠引入重型依赖换速度）。四守卫分别堵住「重定义完整运行」「悄悄少测」「漂移防护退化」「失败不可定位」四条降质路径，彼此正交、各有独立判据与任务载体（tasks §Requirements Coverage :21-25）。
- [x] CHK033 - 镜像套件「只增不减」的论证是否锚定 owner 事实（表源取同步引擎 pair 清单）而非复述清单？ [Regression, Req §FR-018; Plan §W3; Tasks T019; Constitution VIII/XII]
  - 判定依据：PASS — 参数表源 = importlib 载入 `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS` 与枚举 helper、不复制清单（T019 tasks.md:154；plan.md:105；R-5）——引擎为唯一 pair owner（Constitution VIII 代码事实优先、XII Tool Reuse），新增对自动入列使强度单调不减；例外对保持引擎语义、不额外放宽（plan.md:106）；断言语义 = 引擎 `--check` 同一比对（plan.md:105），漂移对继续失败正是 SC-008 相对语义的输入（plan.md:109）。

## 6. 依赖与范围（Feature 058 绑定、交付面、禁改面、运行时依赖零扩大是否自洽）

- [x] CHK034 - Feature 058 绑定与「演化规格、状态不回退、不改注册表计数」是否在 requirements/plan/tasks 三处一致？ [Dependencies, Scope, Req §Related Feature; Plan §Constitution Check II; Tasks header]
  - 判定依据：PASS — 三处同文：绑定 Feature 058、不新建 Feature、058 状态保持 Implemented、不改注册表计数（requirements.md:10-14；plan.md:56；tasks.md:5）；范围扩展注记显式论证测试瘦身仍属同一循环效率演化、不新增 Feature（requirements.md:14）。
- [x] CHK035 - 交付面与禁改面是否在 tasks Path Conventions 穷尽一致，且各任务对引擎/宿主配置的实际触碰方式不越界？ [Scope, Req §FR-021; Contract §RC-06/RC-07; Tasks §Path Conventions, T003/T004/T013/T019/T023]
  - 判定依据：PASS — 禁改面列举 src 运行时行为、`scripts/python/` 引擎语义、宿主 git 配置、`templates/`、注册表、requirements/plan（tasks.md:72），与 FR-021/RC-06 同向（requirements.md:168；contracts/runner-contract.md:23-26）；实际触碰方式核对：引擎一律只读消费（T004/T013/T019 importlib 载入直调、T023 经引擎调用修复、均不改引擎，tasks.md:103/130/154/158），RC-07 中和只作用测试进程树、宿主 git 配置零改动且可回退 = 删 fixture（contracts/runner-contract.md:27-31；tasks.md:102）。
- [x] CHK036 - 「运行时依赖零扩大」与「开发依赖组预期零新增」在 xdist 不采用的前提下是否自洽（准入 vs 采用 vs 实际依赖面三层无矛盾）？ [Dependencies, Req §FR-017/FR-019, §SC-010; Plan §Technical Context; Research R-7]
  - 判定依据：PASS — 准入（允许 dev-only 并行依赖）不蕴含新增：本 spec 采用决定 = 不采用（R-7 research.md:86-94），故开发依赖组预期零新增（plan.md:38）、环境前置声明 not required（tasks.md:54）、T037 检索预期零（tasks.md:199）；若 closure 超 600 s 需要并行，出口是 RC-04 显式升级而非静默加依赖（contracts/runner-contract.md:16-20），SC-010 diff 判据保持把守。
- [x] CHK037 - 镜像义务（条件性触碰运行器/驱动面）与「预期零改动」之间是否存在未声明的同步义务缺口？ [Dependencies, Scope, Plan §Mirror Obligations; Tasks T030/GATE-7]
  - 判定依据：PASS — 义务矩阵覆盖条件分支：运行器若被改 → strict 对同步 + `--check` 零 drift；驱动面引用性更新 → 同引擎同步 + 相对实施前零 NEW drift；tests/pyproject 不在镜像对内已显式声明；本 spec 目录产物无镜像（plan.md:170-177）；T030 执行 + 「未触碰则显式记录」分支（tasks.md:183），GATE-7 机械审计（:47）；既有漂移以「相对基线零 NEW drift」为判据而非绝对全绿，与 W1 triage 分工明确（plan.md:177）。

## 7. 流程合规（宪法 IV 特化、两槽位纪律、状态脊 E2 围栏）

- [x] CHK038 - 宪法 IV（Test-First & Contract-Driven）在本特性下的特化是否成立，且 plan Complexity Tracking 与 tasks Tests Mode 两处一致（引用而非复制）？ [Process, Constitution IV; Plan §Complexity Tracking; Tasks §Tests Mode]
  - 判定依据：PASS — plan 判 IV ⚠ Partial 并给出辩护：本 spec 交付物 = 测试面重组与测量证据，「先写测试再实现」的对象不存在，red→green 意图由等价证据承载——每个合并/夹具动作以 FB-08 注入 + FB-09 定位演练验证防护、每个测量主张以 E1 dated 记录承载、失败处置以名称级差集承载，063 先例同判（plan.md:58、:179-183；constitution.md:73-81 的意图 = 防回归、可验证）；tasks Tests Mode ON 以「只引用不复制」方式原样适用同一辩护，并把性能类 red = 基线家族墙钟（dated）、green = 同法定向复测落带显式定义（tasks.md:9），超带如实归因不虚报（:82）。特化自洽且两处无分歧。
- [x] CHK039 - 两槽位纪律（全量仅 implement 起点 T007 与 closure T034）是否与 063 TB-03/TB-04 语义一致且机械可审计？ [Process, Req §FR-005; Tasks T007/T034/GATE-6; 063 TB-03/04]
  - 判定依据：PASS — 槽位定义同构：implement 起点全量（T007，兼 RC-07 全局验证点）+ closure 全量（T034，review 后、合并前），implement 内不得第二次全量、closure 修复重入不重耗 baseline 槽位（tasks.md:11、:81、:106、:196；063 contracts/test-budget.md:9-10 TB-03/TB-04 同语义）；审计 = GATE-6 `audit-test-budget.py --stage-check closure` 期望 `baseline:1 closure:1`（tasks.md:46）；槽外全量须显式例外（FR-005 requirements.md:149），本 spec 未计划任何例外。
- [x] CHK040 - 状态脊 E2 槽位围栏的写入者、时点、写入模式与审计来源是否明确（direct 写入、U0 声明路径、围栏唯一台账来源）？ [Process, Tasks T007/T034/GATE-6; 063 Efficiency-Model §E2]
  - 判定依据：PASS — T007/T034 各自把槽位写入状态脊 `<!-- test-budget -->` 围栏（slot=baseline / slot=closure，含名称级差集字段），写入模式 SPINE_WRITE_MODE=direct、`$STATE_SPINE` = 驱动 U0 入口声明路径（tasks.md:106/196；state-spine.md:20）；台账唯一来源 = 脊围栏、传输副本不作为审计来源（063 efficiency-model.md:98 语义，经 tasks.md:46 引用）；GATE-6 审计闭环。注记：CHK012 已裁决「E2」符号双指涉风险，本条判据不受其影响（围栏本身的写入纪律各处一致）。
- [x] CHK041 - closure 槽位时点（review 后、合并前）与收口阶段拆分（Phase 8 review 前置 / Phase 9 closure）是否与 063 槽位语义及本 spec 的 review 流程自洽？ [Process, Tasks Phase 8/9; Plan §W5; 063 TB-04]
  - 判定依据：PASS — Phase 8 = implement 期收尾（镜像核销、review 前置核对、verification 建档），Phase 9 = closure 槽位验收、显式标注「review 后、合并前执行」（tasks.md:179-202），与 063 TB-04 closure 槽位语义一致（.specify/specs/063-sdd-loop-efficiency/contracts/test-budget.md:10）；plan §W5 的 SC-006 验证时点同为「closure 槽位（review 后、合并前）」（plan.md:122）；T032 把 SC-006…SC-010 标 pending-closure 待回填（tasks.md:185），时序无冲突。

## 裁决汇总

- **总计 41 项：PASS 40 · FAIL 1 · [Gap] 0**（ID 连续 CHK001–CHK041；每项带判定依据与证据指针；无未答项）。
- **FAIL 清单（1 项）**：CHK012 —— 符号「E2」跨产物双指涉（data-model §E2 ConsolidationLedger vs 063 状态脊 test-budget 槽位台账）。补正落点 = tasks.md Notes（加指涉注记）或 data-model.md §E2 标题；属他阶段产物，本阶段不改。机械护栏（GATE-6 围栏审计、LED-05 join）保证错写不会漏到收口，最坏后果是 implement 期返工一轮。
- **残留风险**：① CHK012 未补正前，implement 子代理首次写「E2 行」时须依上文指涉注记自行消歧——建议驱动者在 implement part brief 中点名该注记；② plan Scale/Scope 文件数估计内部张力（CHK014 已披露）为非规范估计，若 implement 期实际触碰面显著偏离，以 SC-007/LED-05 判据为准、不回改估计；③ FR-018 名册扫描面 = contract 层（CHK005），未来非 contract 层新增钉住类测试须先扩需求类别措辞。
- **本阶段边界声明**：未修改 requirements.md / plan.md / tasks.md / tests / scripts / pyproject.toml / 源码 / 镜像 / 注册表；未运行任何测试；新增文件仅本清单。
- **结构自校验**：ID 连续性、判定依据覆盖、复选框/判定值一致性与裁决汇总计数核对——机械核对结果：items=41（`grep -c '^- \['`）、checked=40 / unchecked=1（即 FAIL 项 CHK012）、ID 序列 CHK001…CHK041 无跳号无重复、41 项全部带判定依据（PASS 40 / FAIL 1 / [Gap] 0）。validator 见证：项目无 checklist 专用校验器（pre-analyze-check 仅支持 requirements/plan/tasks），以 `pre-analyze-check --stage tasks` 作无回归见证 → decision=pass、errors=0、advisories=8（7 条为本清单引用 063 外部命名空间条款 TB-03/TB-04 的提示、1 条为 tasks 阶段既有的预期缺失新测试路径提示，均非阻断）。

