# Exec-Quant Feedback Channel Checklist: 执行量化数据反馈回传与汇总（Feature 068）

**Purpose**: 检验 068 规格集（requirements / data-model / contracts / quickstart）在执行量化回传通道三个腿上的需求写作质量——每条都是关于「是否已定义/已量化/已圈界」的问题，可仅凭阅读规格/设计产物回答
**Created**: 2026-10-22
**Feature (Requirement Scope)**: `.specify/specs/068-exec-quant-feedback-channel/requirements.md`（19 FR / 6 SC）
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md) · [tasks.md](../tasks.md) · [data-model.md](../data-model.md) · [contracts/](../contracts/) · [research.md](../research.md) · [quickstart.md](../quickstart.md)

**Note**: 本清单由 `/speckit.checklist` 生成，是**需求写作的单元测试**，不是实现测试——任何条目都不得以运行产品来回答。引用 plan/tasks/contracts 仅用于暴露需求缺口、歧义、冲突与可追溯性问题，不评审设计与分解本身。与既有 [requirements.md](requirements.md)（通用规格质量门）互补，零覆盖重复。

**Run meta（无人值守裁决记录）**:

- 意图澄清按派发缺省自裁：**Depth = Standard · Audience = Reviewer · Focus = top 2 相关簇（打包腿、接收腿）为主，另按派发指令强制覆盖汇总腿 / 安全与兼容 / 测试与交付三个关键风险簇**。未向用户提问。
- 同作者缺口发现降级：本运行无子代理派发工具，按 objective-analysis-gate §7 以直接有界读取执行，缺口条目标注 `(detected: direct read, subagent unavailable)`——弱证据路径对读者可见。
- 条目 40 条（soft cap 40 内），编号 CHK001 起；40/40 携带可追溯引用（≥80% 达标）。`[Gap]` 条目 = 规格缺口发现，仅记录于本清单，不回改 requirements/plan/tasks（由 analyze 阶段处置）。

## 打包腿——载荷完整性、只读与降级（Focus Cluster 1 · P1）

- [ ] CHK001 载荷纳入规则是否对两类存储形态（逐条 `records/` 目录 + 遗留 `records.jsonl` 流）都完整定义，并明确「两类并存时全量纳入、不引入增量水位」？ [Completeness, Req §FR-001 / Contract C-1]
- [ ] CHK002 载荷条目的合格判据是否精确定义（可 `json.loads` 为 object 且 `kind == [[STR-001]]`），不合格条目的计数归属（`skipped_unreadable`）是否随之明确？ [Completeness, Contract C-1 / Req §FR-005]
- [ ] CHK003 「只读源存储」是否落为可验证判据（打包前后 exec-quant 存储与 feedback store 逐文件清点零差异），而非仅陈述性意图？ [Measurability, Req §FR-002 / Req §SC-001 / Contract C-1]
- [ ] CHK004 封顶阈值是否量化为确切数值（条数与字节双上限）且要求写入 payload-manifest 的取证字段（`cap_records` / `cap_bytes`）？ [Clarity, Contract C-2 / Data §E4]
- [ ] CHK005 截断粒度（整条记录、无半条字节）与「单条记录自身超过字节上限」的处置是否被定义？ [Edge Case, Gap, Contract C-2] `(detected: direct read, subagent unavailable)`
- [ ] CHK006 确定性排序键是否覆盖字段缺失情形——记录缺 `collected_at` 时的排序位置是否被规定？ [Edge Case, Gap, Contract C-2 / Data §E1] `(detected: direct read, subagent unavailable)`
- [ ] CHK007 data-model 的对账恒等式（`skipped_unreadable + truncated_count + record_count == 探测总数`）能否仅凭 payload-manifest 已记录字段复核——「探测总数」本身是否在任何产物中留痕？ [Ambiguity, Data §E4] `(detected: direct read, subagent unavailable)`
- [ ] CHK008 降级阶梯（空存储/目录缺失、部分不可解析、触顶截断、身份缺失）是否逐级给出显式且非阻塞的结果定义？ [Coverage, Req §FR-005 / Contract C-9]
- [ ] CHK009 FR-019 双空不产包情形的退出语义是否有别于失败退出——C-8 中「既有非零包为成功语义不变」的措辞对照 D10 的 exit 0 / exit 2 阶梯是否无歧义？ [Ambiguity, Req §FR-019 / Contract C-8 / research D10] `(detected: direct read, subagent unavailable)`
- [ ] CHK010 MANIFEST 人读段与 payload-manifest.json 的「同源渲染」（同一函数产出）是否作为绑定需求定义，空载荷段的强制存在是否被覆盖？ [Completeness, Contract C-4 / C-6 / Data §E5]
- [ ] CHK011 投递前知情义务是否对 text 与 `--format json` 双输出面都定义了可见的载荷条数与降级计数？ [Completeness, Req §FR-004 / Contract C-7]

## 接收腿——Path A 承接、识别、归因与幂等（Focus Cluster 2 · P1）

- [ ] CHK012 接收承接面是否无歧义（既有 feedback-utils 引擎动作承接 Path A、零新增命令），调用点（Path A A2 每包一次）是否被点名？ [Completeness, Req §FR-006 / Contract C-10]
- [ ] CHK013 载荷识别是否锚定单一机制（zip 成员路径前缀 `exec-quant/`），无载荷包的行为是否全钉死（零计数、exit 0、零写入、零目录创建）？ [Completeness, Req §FR-009 / Contract C-11 / C-27]
- [ ] CHK014 身份缺失路径是否完整定义（unknown-project 字面分组、MUST NOT 从路径或内容猜测、manifest 不可读降级仍逐条尝试）？ [Coverage, Req §FR-006 / Contract C-11 / C-12]
- [ ] CHK015 幂等身份定义在需求层（源项目 + unit_id + run_id + 采集时间戳）与契约层（五元组另含 unit_type + content_hash）之间是否一致——unit_type 的加入是否被说明为意图内细化而非口径漂移？ [Consistency, Req §FR-008 vs Contract C-13] `(detected: direct read, subagent unavailable)`
- [ ] CHK016 同 key 异 content_hash 的处置是否被显式裁定（keep-first + `identity_conflicts` 计数），而非留白？ [Completeness, Contract C-13]
- [ ] CHK017 去重检查与写入的并发形态是否被规定（单一 flock 临界区、锁文件 `aggregated/.write.lock`、tmp+rename 原子写）？ [Completeness, Req §FR-012 / Contract C-13 / C-14]
- [ ] CHK018 zip 成员级损坏（区别于单条记录不可解析）的显式计数是否有自己的输出键定义？ [Gap, Req §Edge Cases / Contract C-16] `(detected: direct read, subagent unavailable)`
- [ ] CHK019 payload-manifest 可读但其声明计数与 zip 实际成员不一致（`record_count != len(records/)`）时接收行为是否被定义？ [Gap, Data §E4 / Contract C-11] `(detected: direct read, subagent unavailable)`
- [ ] CHK020 存储分界（exec-quant 记录零条混入 feedback store、两 store 清点口径互不引用）是否落为可验证判据而非陈述？ [Measurability, Req §FR-006 / Req §SC-003 / Contract C-30]
- [ ] CHK021 「接收不自动汇总」是否表述为可测义务（ingest MUST NOT 触发 aggregate、`aggregated/summaries/` 零新增）？ [Consistency, Req §FR-011 / Contract C-17]

## 汇总腿——显式汇总、可对账与本地边界（Focus Cluster 3 · P2）

- [ ] CHK022 汇总触发语义是否显式（用户发起的引擎动作、绝不随接收自动执行）且调用入口被点名（`exec-quant.py --action aggregate`）？ [Completeness, Req §FR-011 / Contract C-23]
- [ ] CHK023 消费面是否精确圈定（只读 `aggregated/**/records/*.json` 信封、本地 `records/` 与 `scores/` 被排除且给了负例）？ [Clarity, Contract C-19]
- [ ] CHK024 「每个聚合数字可对账」是否同时定义为能力（`sources[].record_files[]` 名单）与验收判据（名单重放核对）？ [Measurability, Req §FR-011 / Req §SC-004 / Contract C-20]
- [ ] CHK025 质量分布的字段全集（哪些记录字段进入 `quality{field: {evaluated, not_evaluated}}` 枚举、未知新字段是否入列）是否被显式定义？ [Gap, Contract C-20 / Data §E7] `(detected: direct read, subagent unavailable)`
- [ ] CHK026 零臆造是否操作化（未测/缺失以 [[STR-002]] 显式计数呈现、禁止填补/外推/杜撰基线、不评估不打分不判阈值）？ [Completeness, Req §FR-013 / Contract C-21]
- [ ] CHK027 空聚合层执行汇总的行为（零 `sources[]`、`totals` 未测占比的分母为零）是否被定义？ [Edge Case, Gap, Contract C-20] `(detected: direct read, subagent unavailable)`
- [ ] CHK028 产物按条落盘的并发安全形态是否被规定（一次汇总一个新文件、旧文件零改写、`store_digest` 支撑重跑重建核对）？ [Completeness, Req §FR-012 / Contract C-22]
- [ ] CHK029 汇总产物仅本地/零外发是否同时覆盖执行面与产物面（零网络操作、产物只落本仓 `aggregated/`）？ [Non-Functional, Req §FR-014 / Contract C-23]

## 安全与兼容边界（Focus Cluster 4 · P2）

- [ ] CHK030 凭据零出现的扫描判据是否可复现（何谓「凭据型变量名/形态」、对产物 zip、`aggregated/` 目录、汇总产物三个面分别执行、命中计数 = 0）？ [Measurability, Req §FR-015 / Req §SC-005 / Contract C-25]
- [ ] CHK031 对 059 FR-011 的修订是否按子句拆分留痕（仅「结构性排除于反馈打包」子句修订为手动触发打包腿，「排除于一切上送路径」子句原样保留），整条放宽的误读是否被显式封堵？ [Consistency, Req §FR-016 / Contract C-24]
- [ ] CHK032 三条容忍轴（目录布局 records/ vs 遗留 jsonl、schema v1/v2、`{value, provenance}` vs 裸 `[[STR-002]]`）是否逐轴命名并指定归一处（仅读取与派生视图侧、源数据零改写、遗留单体流只读回退）？ [Coverage, Req §FR-007 / Contract C-15 / C-28]
- [ ] CHK033 未知字段原样保留（零丢弃进聚合层）与未知形态按未测处理是否覆盖三条腿的全部读取面，且零版本号硬编码？ [Coverage, Req §FR-007 / Contract C-15 / C-28]
- [ ] CHK034 既有引擎零回归判据是否为名字级（排序失败 nodeid 与冻结基线逐名比对、非计数级），且基线路径与冻结日期明确？ [Measurability, Req §FR-018 / Req §SC-006 / Plan §Test Strategy]

## 测试与交付（Focus Cluster 5 · 派发强制覆盖）

- [ ] CHK035 Tests Mode 是否显式判定为 ON 并给出宪法依据（Principle IV），红先取证义务是否逐条挂到新增行为测试行、US4 回归网例外是否显式声明？ [Completeness, Tasks §Tests / Plan §Test Strategy]
- [ ] CHK036 E2 / E3 / closure 测试预算的槽位归属是否被声明（baseline 恰一次于 implement 起点、阶段定向行落 stage-status、closure 槽留待 review 后、plan 冻结定向基线 ≠ E2）？ [Completeness, Tasks §Test Budget]
- [ ] CHK037 镜像同步顺序（先框架源后镜像、禁手改镜像/逐工具副本）与判据（相对既有基线零 NEW drift，绝无绝对「全绿」判据）是否逐镜像对规定？ [Consistency, Contract C-31 / Plan §Mirror Obligations / Tasks §Mirror Obligations]
- [ ] CHK038 文档同步义务是否落到文件级（技能 SKILL + 两份 references、命令模板、shared step、两份 docs）且声明「引擎动作名以代码 `_ACTIONS`/`ACTIONS` 为准」的取值权威？ [Completeness, Tasks T025 / T026 / Contract C-31]
- [ ] CHK039 本清单不推进生命周期、Feature 068 保持 Planned（`Planned → Implemented` 属 implement 阶段）的边界是否被显式记录于规格面？ [Dependencies, feature-ref.md / Tasks §Notes]
- [ ] CHK040 `aggregated/` 派生存储的 git 跟踪姿态在 plan（「按 records/ 惯例随 git 跟踪」）与 Artifact Commit 约定（运行时记录不入特性提交）之间的执行口径是否一致？ [Ambiguity, Plan §Source Code / Tasks §Notes] `(detected: direct read, subagent unavailable)`

## Notes

- 应答方式：逐条以 `[x]` 勾选并在行内附结论/引用；后续轮次的解答写入新的 `recheck-<date>-<topic>.md`，本文件不就地刷新（append-only 历史）。
- **缺口发现汇总（仅记录，不回改上游；analyze 阶段处置）**——共 10 条：[Gap] 6 条（CHK005/006/018/019/025/027）+ [Ambiguity] 3 条（CHK007/009/040）+ [Consistency] 发现 1 条（CHK015）：
  1. CHK005 截断粒度与单条超字节上限记录的处置未定义 [Contract C-2]
  2. CHK006 缺 `collected_at` 记录的排序位置未定义 [Contract C-2 / Data §E1]
  3. CHK007 E4 对账恒等式的「探测总数」无留痕字段，接收侧不可独立复核 [Data §E4]
  4. CHK009 C-8「既有非零包为成功语义不变」措辞歧义（双空退出语义 vs D10 阶梯）[Contract C-8]
  5. CHK015 FR-008 四元组身份 vs C-13 五元组（+unit_type）差异未被说明为意图内细化 [Req §FR-008 / Contract C-13]
  6. CHK018 zip 成员级损坏计数无独立输出键 [Req §Edge Cases / Contract C-16]
  7. CHK019 payload-manifest 计数与实际成员不一致时的接收行为未定义 [Data §E4 / Contract C-11]
  8. CHK025 汇总视图质量分布的字段全集未定义 [Contract C-20 / Data §E7]
  9. CHK027 空聚合层汇总（未测占比 0/0）行为未定义 [Contract C-20]
  10. CHK040 `aggregated/` git 跟踪姿态在 plan 与 tasks 换算为提交纪律时的口径张力 [Plan §Source Code / Tasks §Notes]
- 缺口发现证据路径降级声明：`(detected: direct read, subagent unavailable)`（objective-analysis-gate §7；本运行无子代理派发工具）。
- 引用缩写：`Req §` = requirements.md；`Contract C-n` = contracts/ 四文件条款；`Data §E*` = data-model.md 实体；`Plan §` / `Tasks §` = plan.md / tasks.md 章节；`research D*` = research.md 决策。
