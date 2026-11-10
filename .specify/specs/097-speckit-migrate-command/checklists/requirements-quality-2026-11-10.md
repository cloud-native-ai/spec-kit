# Requirements-Quality Checklist: /speckit.migrate 一次性迁移收尾命令（判定来源 · 干跑与确认门 · sanitize 边界 · 期望态可机判 · 跨版本与回滚 · 夹具复现）

**Purpose**: 检验 Feature 097 需求文本（`requirements.md`）的**写作质量**——混杂态判定清单是否只有确定性来源、`--dry-run` 默认与双键确认门是否闭合、与 sanitize Migration lane 的职责边界是否唯一、期望态判据是否可机判、跨版本直达 / 续跑 / 回滚语义是否可判、夹具旧项目的验收是否可复核。每条都是对需求文本（或它点名的 owner 行）的提问，**不是**对实现行为的检验：凡只有跑一遍产品才能回答的条目，本身就是本清单的缺陷。
**Created**: 2026-11-10
**Feature (Requirement Scope)**: `.specify/features/024-specification-workspace-versioning.md`（Feature 024，Draft）
**Requirements (What)**: [../requirements.md](../requirements.md) — 机械读数（2026-11-10）：236 行 / 35,235 B；**25 FR**（FR-001…FR-025）；**9 SC**（SC-001…SC-009）；**4 Shared Strings**（STR-001…STR-004）；4 个用户故事；10 条 Edge Cases；2 场 Clarifications（6 + 4 问）；11 条 Assumptions（A1–A11）。
**Specifications (How, context only)**: [../plan.md](../plan.md)（202 行 / 23,639 B；T-001 / T-002）、[../tasks.md](../tasks.md)（380 行 / 51,508 B；48 任务行）、[../data-model.md](../data-model.md)、[../contracts/](../contracts/) — **只**用于暴露需求的缺口、歧义与冲突，**从不**为它们自身打分。
**Readers**: 需要判定「097 的需求是否足以放行 analyze / implement」的复核者——`/speckit.analyze` 的检测者、SDD review 的复核者与后续接手本线的编写者；他们按条末的 `[Req §…]` 锚回到需求正文逐字核对。
**Reading scenario**: 复核者打开本文件，要决定三件事：(1) 哪几条需求缺陷必须在 analyze / implement 之前修掉；(2) 哪些项可登记为「已裁定、由下游承载」而放行；(3) 哪些项因判据依赖尚未落地的机制而保持 `not_evaluated`。
**Focus / Depth / Audience**: Focus = 阶段简报的六个聚焦簇（判定来源确定性 / `--dry-run` 默认与确认门 / sanitize 边界唯一性 / 期望态可机判 / 跨版本与回滚 / 夹具验收可复核）+ 跨清单一致性；Depth = **Standard**（默认）；Audience = **Reviewer**（默认）。本轮 `$ARGUMENTS`（阶段简报）已使意图明确，技能 §2 的三个意图澄清问题按「已预答」跳过，默认值记录于此。
**Detection path**: same-author 条件**成立**——`requirements.md` / `plan.md` / `tasks.md` 由本轮无人值守 SDD 线内的前序阶段代理撰写，共享同一模型与同一套约定。缺口发现按 `.specify/shared/workflow/objective-analysis-gate.md` 派发 **3 路 fresh-context 只读检测代理**，作用域不相交：Detector A = US1–US4 / Edge Cases / FR-001…FR-013（附 plan T-001/T-002 与引擎契约做缺口对照）；Detector B = FR-014…FR-019 / FR-024 / SC-001…SC-005（附 data-model E-3/E-5 与 CLI 契约）；Detector C = FR-020…FR-025 / SC-003…SC-009 / Measurement Sources / Shared Strings / Clarifications / Assumptions（附 tasks.md 缺口检测）。三路共输出 **30 行**检测结果；按门禁规则 4（映射表即断言）逐行回原文核对：**1 行被原文反驳**（「平铺残留双 owner」——FR-005 写「刷新与退役处置」、FR-010 写「确定性检查」，检查 / 处置分工自洽，删除该行）、**1 行拆为两条**（中断点枚举与「中断后工作区被改动」）、**2 组双检测器重叠合并**（源版本记录、lane/pointer 可测性）；其余并入 **39 条**追溯条目。同一轮未另设验证波次（本技能只定义一次检测）；**拒绝率 1/30 = 3.3%**；本技能无严重度分级，追溯锚是其局部等价物，故无「降级」计数。程序读数（行数 / 字节 / FR·SC·STR 计数 / 任务行 / 派发与核对记录）见 [../test-evidence/checklist-readings-2026-11-10.txt](../test-evidence/checklist-readings-2026-11-10.txt)。

**Note**: 由 `/speckit.checklist` 按 `.specify/skills/internal/create-checklist/SKILL.md` 生成，方法论 owner 为 `.specify/shared/guidelines/checklist-methodology.md`，结构模板为 `.specify/templates/checklist-template.md`。勾选一条的唯一依据是**需求文本本身**（或该条目点名的 owner 行）给出了答案；答「否」产出的是对 `requirements.md` 的 finding，不是一条实现任务。判据落在需求之外（下游文档 / 工具）时登记为**观察**；判据依赖尚未落地的机制时登记为 `not_evaluated`。

## 一、混杂态判定清单的确定性来源

- [ ] CHK001 - 五个期望态 owner 的消费形态是否逐一钉名（进程内导入还是 CLI 只读动作）——FR-010 只对 sanitize 检查器规定了形态，其余四个 owner 的消费方式是否留给实现自行选择？[Completeness, Req §FR-005, Req §FR-010]
- [ ] CHK002 - 五个 owner 以「已安装副本」还是「工作区 `.specify/scripts/python/` 副本」为权威，以及「当前已安装版本」如何被确定性判定（wheel 包内数据？可编辑安装？仓库检出？），是否已在 FR-005 定义？[Ambiguity, Req §FR-005]
- [ ] CHK003 - 某个钉名 owner 在安装版本中缺席或执行报错时，命令应如何降级（中止、该维度 `refuse`，还是记降级事实），是否已定义？[Gap, Req §FR-005, Req §FR-008]
- [ ] CHK004 - FR-005 的三条禁令（MUST NOT 读 `.specify/version`、MUST NOT 按模板指纹猜测、MUST NOT 内置旧结构清单）是否各有可转红的负向断言，而不只是正文禁令？[Measurability, Req §FR-005, Req §SC-004]
- [ ] CHK005 - 维度①（模板与生成物，含技能与代理镜像）与维度④（镜像一致性）对同一镜像文件是否互斥；同一 target 被两维命中时的归属、去重与处置优先级是否已规定？[Conflict, Consistency, Req §FR-007, Req §FR-014]

## 二、`--dry-run` 默认、确认门与运行结局

- [ ] CHK006 - 显式 `--dry-run` 与裸默认运行是否等价、`--dry-run` 与 `--apply` 并用时按输入错误还是别的结局处理，是否已在 FR-001 规定（而非只在 data-model / 契约中）？[Clarity, Req §FR-001]
- [ ] CHK007 - 「一次单批确认提示」的覆盖范围（整个破坏性桶，还是按维度分批）与拒绝粒度（一次拒绝使全部破坏项 `blocked`，还是允许逐项选择）是否已定义？[Ambiguity, Req §FR-015]
- [ ] CHK008 - 交互终端下用户在确认提示处 EOF／空回车／取消时，应按拒绝（`blocked`、退出 3、可逆项照常）还是输入错误（退出 2、不产回执）处理？[Gap, Edge Cases, Req §FR-015]
- [ ] CHK009 - 破坏性桶的成员分类是否必须从 confirmation-gates owner 派生/导入并由漂移测试钉住，还是允许在命令内复制一份清单（复制后与 owner 分叉是否能通过全部验收）？[Gap, Req §FR-015]
- [ ] CHK010 - `clean` 与 `applied` 共用退出 0 时，需求是否强制输出可机器解析的 outcome token（及承载它的输出格式），否则 FR-019 的「四类结局可脚本判定」如何成立？[Measurability, Req §FR-019]
- [ ] CHK011 - 一次应用已收敛部分差异项、但仍剩 `refuse`/`blocked` 项时，结局按 `applied`（退出 0）还是 `blocked`（退出 3）——FR-019 的两条定义是否互斥且完备？[Conflict, Req §FR-014, Req §FR-019]
- [ ] CHK012 - 应用期 I/O 失败（归档写失败、目标写失败）归入四个既定结局中的哪一个，还是需要新增结局与 token？[Gap, Req §FR-017, Req §FR-019]
- [ ] CHK013 - 「零写入」的测量基准是否已钉名（内容哈希、路径集合、文件模式与 mtime、符号链接目标），空目录创建与权限变更是否计入判红？[Ambiguity, Req §FR-006, Req §SC-001]
- [ ] CHK014 - FR-018 要求「每次运行（干跑与应用）MUST 产出一份回执」，FR-006 又要求干跑零写入——干跑回执是否允许只走输出流不落盘，该优先关系由哪条需求裁定？[Conflict, Req §FR-006, Req §FR-018]

## 三、sanitize Migration lane 的边界唯一性

- [ ] CHK015 - FR-012 的「lane 定位声明在同一变更内收敛」是否有可观察的验收面（被检视的文本 / 结构及其断言），还是只有 FR 义务而没有任何 SC 取证？[Gap, Req §FR-012]
- [ ] CHK016 - 「一次成功 migrate 之后用户 MUST NOT 被要求再运行 sanitize」如何操作化——被检视的是命令输出、help 文本还是文档措辞的反例断言？[Ambiguity, Req §FR-012]
- [ ] CHK017 - SC-007 的「sanitize 的迁移类检查」是否指名具体检查器或动作集合，使「迁移残留发现为零」可机判？[Ambiguity, Req §SC-007]

## 四、期望态判据的可机判性

- [ ] CHK018 - 差异判定的相等关系（字节相等、符号链接目标字符串、路径改写后的投影）是否在 FR-006 / SC-001 中定义，还是只有 plan 参照树比较的隐含语义？[Ambiguity, Req §FR-006, Req §SC-001]
- [ ] CHK019 - 客户端期望态所依赖的 init 复制机制（`copy_local_templates` / `rewrite_paths` / `generate_commands`）是否已列入 FR-005 的钉名 owner 清单，还是 plan T-001 引入的未授权来源？[Gap, Req §FR-005]
- [ ] CHK020 - 需求是否定义 plan 区分的两种工作区形态（框架源 vs 客户端）及其不同的期望态来源；框架源模式以工作区自身脚本与标记块为来源，是否违反 FR-005 的「唯一来源」约束？[Conflict, Gap, Req §FR-005]
- [ ] CHK021 - 某维度不可评估时（无适用工具面、owner 缺失、平台不支持符号链接之外的其他限制）结局如何——`clean`、可见降级还是 `refuse`/`blocked`——FR-008 的「计划为空只允许在真实无差异时出现」是否可判？[Gap, Edge Cases, Req §FR-008]
- [ ] CHK022 - 平台资产变体（sh/ps 脚本生成物、工具命令目录交集）的选择规则是否属于期望态需求，还是只存在于 plan 的探测步骤？[Gap, Req §FR-007]
- [ ] CHK023 - 文件属性（可执行位、文件模式、符号链接目标字符串）是否纳入期望态比较；若排除，排除声明写在哪里？[Gap, Req §FR-007, Req §SC-001]
- [ ] CHK024 - FR-008 的「每个维度具备可转红断言」是否逐维枚举（五维各一条），且与 FR-024 / FR-025 的变异清单及 SC-001…SC-009 各自声称的变异双向一致（如 SC-005「择一胜出」、SC-003/004/007/009 的变异无对应 FR 强制来源）？[Consistency, Measurability, Req §FR-008, Req §FR-024, Req §FR-025, Req §SC-005]

## 五、跨版本直达、续跑与回滚语义

- [ ] CHK025 - 回执中的「源版本」从哪里读取，对无 source stamp 的 043 前项目以什么既定取值记录（如 `unavailable`），是否已定义？[Gap, Req §FR-020, Req §US3 AS1]
- [ ] CHK026 - FR-018 的回执字段清单是否包含 SC-004 要求的「源版本与目标版本」字段，以及 FR-017 / SC-006 续跑所需的运行状态（`running`/`completed`）与续跑来源标识？[Gap, Conflict, Req §FR-017, Req §FR-018, Req §SC-004]
- [ ] CHK027 - 「中断」被操作化为哪些必须可续跑的中断点（归档后未写、写入中、回执未更新），并对每个点声明「不丢数据 + 不二次搬移」？[Clarity, Req §FR-017, Req §SC-006]
- [ ] CHK028 - 中断与续跑之间工作区被用户改动时，按旧回执续做还是重新探测 / `refuse`，结局如何判定？[Gap, Edge Cases, Req §FR-017]
- [ ] CHK029 - 「不提供全局回滚 / undo」是否配套声明用户可用的替代路径（逐项归档找回 + 前向续跑），使回滚期待被封闭而非仅被排除？[Completeness, Req §FR-016, Req §FR-017]
- [ ] CHK030 - SC-004 的「两类以上历史代残留」在禁止版本识别后如何被确定性计数与断言——「类」与「代」是否同一计量单位？[Measurability, Req §SC-004, Req §FR-020]

## 六、夹具旧项目的验收可复核性

- [ ] CHK031 - 「纯旧版夹具」的构成是否按残留类逐一枚举并映射到具名检查器 / 声明条目，使复核者可判定其对 N→N+k 残留的代表性？[Clarity, Req §FR-023, Req §SC-004]
- [ ] CHK032 - FR-023 枚举的四类构成是否足以让纯旧版夹具产生 SC-001 要求的五维差异（尤其模板 / 镜像内容漂移与兼容链接缺失），还是两处清单不一致？[Consistency, Req §FR-023, Req §SC-001]
- [ ] CHK033 - 「已最新夹具」是 init 现场投影树，还是 migrate 收敛后的树——其 `clean` 期望的构造依据写在哪里？[Ambiguity, Req §FR-023, Req §US1]
- [ ] CHK034 - 「夹具与探测共享同一来源」是否要求构建时实时读取注册表 / 检查器，而非抄写一份作者时名单（后者在注册表演进后会静默漂移）？[Ambiguity, Req §FR-023]
- [ ] CHK035 - §Measurement Sources 的每项来源是否钉到可复现命令、记录落点与变异注入方式，而不止于「实测记录」散文？[Measurability, Req §SC-001 Source … §SC-009 Source]
- [ ] CHK036 - 两写者并发回执测试由哪条 FR 承载、哪条 SC 取证，而非只留在 Edge Cases 与 A6 的散文里？[Gap, Req §Edge Cases, Req §A6]

## 七、跨清单一致性与残余歧义

- [ ] CHK037 - FR-002 的「两个入口逐项一致」以何比较基（解析后的 items/summary 结构还是渲染文本）判定，且哪条 SC 覆盖该等价性？[Gap, Req §FR-002, Req §FR-025]
- [ ] CHK038 - FR-022 的 Qoder 副本 frontmatter 契约由哪条 SC 或验收断言覆盖，SC-009 的装配面清单是否包含它？[Gap, Traceability, Req §FR-022, Req §SC-009]
- [ ] CHK039 - FR-013 的「静止指针」是否有可机检的形态（字段 / 固定文本），使 SC-007 的「指针存在」断言可判定？[Ambiguity, Req §FR-013, Req §SC-007]

## Notes

- 勾选一条的唯一依据是**需求文本本身**（或该条点名的 owner 行）给出了答案；答「否」产出的是对 `requirements.md` 的 finding，由 `/speckit.analyze` 或后续 clarify / plan 迭代消化，不是一条实现任务。
- 本清单只读需求，不在此回答；条目按风险 / 影响排序，39 条低于 soft cap 40。
- 追溯率 39/39 = 100%（每条均带 `[Req §…]` 与 / 或 `[Gap]`、`[Ambiguity]`、`[Conflict]` 锚）。
- 检测与核对记录见 `../test-evidence/checklist-readings-2026-11-10.txt`：3 路检测、30 行原始发现、1 行被原文反驳（拒绝率 3.3%）。
