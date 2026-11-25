# Requirements-Quality Checklist: Runtime Store Layout — 运行期存储迁出 `.specify/memory/`

**Purpose**: 检验 Feature 105 需求文本（`requirements.md`）的**写作质量**——运行期存储的封闭清点与退役根语义是否可判定、迁移/拒绝契约是否闭合到具名行为、临时记忆与 super agent→sub agent 注入是否被要求行为保持、tools 记录-忽略拆分与源-镜像-安装一致性是否可机械核对、dated record 保全与 live 引用更新边界是否一致、以及用户追加要求（每个向后不兼容变更都由 `/speckit.migrate` 迁移或确定性拒绝）是否可验收。每条都是对需求文本（或它点名的 owner 行）的提问，**不是**对实现行为的检验：凡只有跑一遍产品才能回答的条目，本身就是本清单的缺陷。
**Created**: 2026-11-25
**Feature (Requirement Scope)**: `.specify/features/024-specification-workspace-versioning.md`（Feature 024 Specification Workspace Versioning；本规格为 slice 105，登记行状态 `Planned`；本清单位于 `/speckit.implement` 之前，按 Feature Integration Protocol 不发起 `Implemented → Ready for Review` 迁移，也不为缺少 code-segment 结论报错或编造结论）
**Requirements (What)**: [../requirements.md](../requirements.md) — 本轮机械读数（2026-11-25，`validate-requirements.py`，逐字输出见 `../test-evidence/checklist-requirements-validator.txt`）：**326 行 / 0 error / 0 warning**；**27 FR**（FR-001…FR-027）、**9 SC**（SC-001…SC-009；final 5 / supporting 4）、**6 Shared Strings**（STR-001…STR-006）、16 条假设裁定（A-1…A-16）、6 个用户故事、**17 行封闭 Store Inventory**、3 段 Clarifications 会话（末段为用户追加要求的逐字记录）。
**Specifications (How, context only)**: [../plan.md](../plan.md)（**18 行**向后不兼容变更清点 BC01…BC18；闭集行为类与证据指针）、[../tasks.md](../tasks.md)（**43** 任务行）、[../contracts/](../contracts/)（**32 条款**：C-1…C-8 / M-1…M-10 / P-1…P-6 / L-1…L-8）——**只**用于暴露需求的缺口、歧义与冲突，**从不**为它们自身打分。
**Readers**: 需要判定「105 的需求是否足以从 checklist 放行进 analyze / implement」的复核者——`/speckit.analyze` 的检测者、`/speckit.implement` 的协调者与后续接手本线的编写者；他们依据本清单、被引用的需求行与 `test-evidence/` 的机读读数取结论。
**Reading scenario**: 复核者打开本文件，决定三件事：(1) 哪几条需求缺陷必须在 analyze / implement 之前修掉；(2) 哪些项可登记为「已裁定、由下游承载」而放行；(3) 哪些项因判据依赖尚未落地的机制而保持 `not_evaluated`。按条末的 `[Req §…]` / `plan §…` 锚回到正文逐字核对。
**Focus / Depth / Audience**: Focus = 阶段简报的八组聚焦簇（用户追加的向后不兼容闭包 / 封闭 Store Inventory 与退役根 / 迁移幂等与拒绝 / 记忆与注入保持 / tools 记录-忽略拆分 / 源-镜像-安装一致性 / dated record 保全 / 常规质量维度）；Depth = **Deep**（简报把追加要求与风险簇写成必覆盖集，默认 Standard 不足以承载）；Audience = **Reviewer**。阶段简报已使意图明确，技能 §2 的三个意图澄清问题按「已预答」跳过，默认值与升深理由记录于此。
**Detection path**: same-author 条件**不成立**——`requirements.md` 与 plan/tasks 由上一条无人值守 SDD 线内的独立阶段执行体撰写，本执行体未曾撰写所分析的任何制品；按 `.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires 的「制品先于本会话或作者不同」分支，门不触发，未派发 fresh-context 检测代理（本派发亦明令不得再派发代理）。缺口扫描由本执行体直接完成；可机械核对的前提（FR / SC / STR 计数、清单行数、BC 行数、契约条款数）均以程序读数当场取证，读数见 Notes。

**Note**: 由 `/speckit.checklist` 按 `.specify/skills/internal/create-checklist/SKILL.md` 生成，方法论 owner 为 `.specify/shared/guidelines/checklist-methodology.md`，结构模板为 `.specify/templates/checklist-template.md`。勾选一条的唯一依据是**需求文本本身**（或该条目点名的 owner 行）给出了答案；答「否」产出的是对 `requirements.md` 的 finding，不是一条实现任务。判据落在需求之外（下游文档 / 工具）时登记为**观察**；判据依赖尚未落地的机制时登记为 `not_evaluated`。

## 一、存储清点闭合与退役根

- [ ] CHK001 - Store Inventory 是否声明为**封闭**，给出基线参照物（提交 `23938f22e` 的实测子目录集）与「表外发现 = 表格修订、不得静默保留」的处置规则？[Completeness, Req §FR-001, Req §Store Inventory]
- [ ] CHK002 - 17 行清点是否逐行具备**唯一处置**（具名目标根或退役）与 owner，且不存在「因已存在而保留」的出口？[Completeness, Req §A-3, Req §Store Inventory]
- [ ] CHK003 - 退役容器 [[STR-001]] 的唯一含义是否钉死为框架地图墓碑行，并且允许出现集（墓碑 / 迁移引擎与其测试 / 遗留残留扫描器）与禁止行为（创建 / 读写 / 运行时回退）是否各自枚举？[Completeness, Req §FR-004, Req §A-8]
- [ ] CHK004 - 每个顶层存储是否被要求有**唯一 owning 组件**，且「第二写入者 / 跨存储写入」被明确禁止？[Completeness, Req §FR-005]
- [ ] CHK005 - 记忆系统是否被要求保持两层闭集、作用域名与动作契约不变，同时把「memory」限定为系统伞形名、两个 tier 以新顶层路径命名（[[STR-002]] / [[STR-003]]）？[Completeness, Req §FR-006, Req §FR-009]
- [ ] CHK006 - 必须迁移的活路径面是否给出**下限清单**并把实现期仓内扫描声明为完整性 oracle（而不是把清单当作全集上限）？[Gap, Completeness, Req §FR-018, Req §SC-006]

## 二、判据清晰度与可测量性

- [ ] CHK007 - 冲突判定里的「非空内容」是否被量化到**权威条目**口径，并同时规定可再生忽略生成物与安装器占位「不计冲突、但不得覆盖或删除」？[Clarity, Req §A-7, Req §FR-015]
- [ ] CHK008 - 「迁移完成」是否可由具名现场事实（退役根不存在 / 回执 / 残留报告）判定，而不依赖对话记忆或人工声明？[Measurability, Req §FR-016]
- [ ] CHK009 - 旧路径「零回退」是否写成可判定的出现规则（允许集 + 集合之外为零），且四项 containment 类 SC（SC-001 / SC-006 / SC-007 / SC-008）是否各自点名基线、比较类与可导出的允许差异集？[Measurability, Req §A-8, Req §SC-001, Req §SC-006, Req §SC-007, Req §SC-008]
- [ ] CHK010 - 「条目格式 / 写入协议不变」是否对**每个**被迁移存储成立（每条目一文件、派生索引即读即建、无共享聚合），而不是只对记忆两层成立？[Clarity, Req §FR-002, Req §FR-025]
- [ ] CHK011 - 迁移结局 token 是否构成**封闭枚举**（`migrate:relocate` / `migrate:container-pass` / `migrate:refuse:<token>` / `compatibility-bridge` / `no-workspace-object`）且每类有判定含义，不存在自由文本结局？[Clarity, Req §FR-027]
- [ ] CHK012 - 「archive-first」是否落到具名可恢复证据对象（manifest / 回执中的恢复路径），而不是仅以意图短语出现？[Clarity, Req §FR-014]
- [ ] CHK013 - 「幂等」是否以可观察的 no-op 契约量化（第二次运行无移动、无重复条目、不重建旧根、输出可判定）？[Measurability, Gap, Req §FR-013, Req §SC-004]

## 三、一致性与可追溯性

- [ ] CHK014 - 被测试 / 契约逐字消费的路径字面量是否登记为 Shared Strings 并以 ID 引用，需求正文中是否存在未登记的重复字面量？[Consistency, Req §Shared Strings]
- [ ] CHK015 - 27 条 FR 是否各自可映射到交付单元、9 条 SC 是否各自映射到具名测试 / 覆盖行，且追加要求是否以**新增** FR-027 / SC-009 落位而未重编既有编号？[Traceability, Req §FR-001…FR-027, Req §SC-001…SC-009]
- [ ] CHK016 - Store Inventory 与 BC 清点的逐行对应是否精确可机检（行 1–15、17 ↔ BC01…BC16；行 16 显式无 BC 行）？[Consistency, Req §FR-027, plan §Backward-Incompatible Change Inventory]
- [ ] CHK017 - `specify migrate` 与 `specify init` 的职责分工是否在 A-6、FR-013、FR-017 / FR-019 与用户故事之间一致（只有 migrate 搬数据；init 只播种新布局、跳过旧内容并指向 migrate）？[Consistency, Req §A-6, Req §FR-013, Req §FR-017, Req §FR-019, Req §US2]
- [ ] CHK018 - tools 域「记录受跟踪 / 生成物被忽略 / 目录不被整目录忽略」是否在 FR-003、A-5、FR-020 与 SC-008 四处一致？[Consistency, Req §FR-003, Req §A-5, Req §FR-020, Req §SC-008]
- [ ] CHK019 - Feature 绑定（024 / slice 105 / 父行 `Ready for Review` 不回退）是否在 §Related Feature、§Clarifications 与注册表行之间一致？[Consistency, Req §Related Feature]

## 四、场景与边界覆盖

- [ ] CHK020 - 三种迁移形态（仅旧 / 新旧并存 / 重跑）是否各有一个验收场景，且三者的期望结局互不重叠、可客观观察？[Coverage, Req §US2, Req §SC-004]
- [ ] CHK021 - 状态形态边界（旧空新空 / 旧空新非空 / 未知顶层文件 / 符号链接）与写入交错、同名跨根冲突是否各自给出预期行为或显式消歧？[Coverage, Gap, Req §Edge Cases, Req §US6]
- [ ] CHK022 - 失败形态（中断后续跑或拒绝、权限只读、无部分成功）是否规定了「续做还是再次拒绝」的判定面，且要求零重复条目、零半条目？[Coverage, Req §US6, Req §FR-014]
- [ ] CHK023 - 记忆边界是否要求一个**反向夹具**（只存在于运行期存储的文本不被记忆召回返回）作为其验证形态？[Coverage, Req §FR-008, Req §SC-003]
- [ ] CHK024 - 两层记忆的记录→召回往返、`run-determination` 持久化与 prune / reindex 语义是否各自具备验收承载？[Coverage, Req §FR-007, Req §SC-002]

## 五、记忆系统与注入保持

- [ ] CHK025 - 派发载荷契约是否以**单一 owner 指针**引用（七字段下行 / 四项注入 / 五要素上行），本规格未复制或改写其字段集？[Consistency, Req §FR-010]
- [ ] CHK026 - 注入的记忆引用是否被要求只解析到两个新记忆根，且禁止引用退役根？[Clarity, Req §FR-011]
- [ ] CHK027 - 「不得引入第二注入机制 / 第二记忆源 / 新注入存储」是否以可判定的禁止项表述？[Completeness, Req §FR-012]

## 六、迁移与向后不兼容闭包（用户追加要求）

- [ ] CHK028 - 本特性引入的每个向后不兼容**工作区**变更是否恰好映射到一个闭集行为，且 `no-workspace-object` 被明令禁止用于工作区状态变更、其适用边界（包内资产）与历史变更的排除边界是否同时写明？[Completeness, Req §FR-027, Req §Clarifications]
- [ ] CHK029 - 拒绝 token 集是否封闭枚举，且每个拒绝被规定为终态（数据原地保留、两侧路径点名、run 阻塞）而不是跳过或回退？[Clarity, Req §FR-027]
- [ ] CHK030 - 运行时双路径回退与人工操作说明是否被明确禁止用于满足任何 BC 行，且守卫被要求在违规时转红？[Consistency, Req §FR-027, Req §SC-009]
- [ ] CHK031 - 每个 BC 行是否至少携带一个可解析证据指针，且「删除一行 / 改用禁止词」的变异演练是否被要求使闭包守卫转红？[Measurability, Req §SC-009, plan §Backward-Incompatible Change Inventory]
- [ ] CHK032 - 对每个映射的 store 变更，`/speckit.migrate` 的 dry-run 零写入与 `--apply` 演示是否被要求执行并留证到具名证据文件？[Coverage, Req §SC-009]
- [ ] CHK033 - 维度集扩展是否被表述为受控断点（有序前缀保持、六 token 全集守卫、v1 回执仍可读）？[Consistency, Req §FR-027, plan §BC18]

## 七、依赖、假设与范围边界

- [ ] CHK034 - 关键假设（A-7 / A-8 / A-13 / A-16 等）是否各自非阻塞、与其喂给的 FR 成对，且没有任何验收标准被未确认的词汇表条目录卡住；六行 Runtime Stack（RS-001…RS-006）是否具备 owner / pin / contract / premises 且零新增依赖可被机械判定？[Assumption, Dependency, Req §Assumptions & Decisions, Req §Runtime Stack]
- [ ] CHK035 - 非目标是否显式且可检验（不新建存储引擎 / 注册表 / 调度器 / 第二注入机制，不改条目格式，不改写 dated record，不留第二权威）？[Clarity, Req §Overview, Req §FR-012, Req §FR-023, Req §FR-025]

## 八、非功能与运行面

- [ ] CHK036 - 忽略策略是否要求模板与已装副本**逐字一致**，并覆盖 tools 拆分与各 agent ignore 模板的放行项？[Completeness, Req §FR-020, Req §SC-008]
- [ ] CHK037 - 镜像与命令副本再生成是否要求**同一变更内**完成，并以「相对基线的成员集无新增漂移」这一可测口径表述？[Measurability, Req §FR-022, Req §SC-007]
- [ ] CHK038 - 活引用更新（docs / glossary / instructions / 已分发指南）与 dated record 保全是否成对声明，且受保护树清单与 live / dated 边界显式可判定？[Consistency, Req §FR-021, Req §FR-023, Req §A-11]
- [ ] CHK039 - 并发写安全是否对**每个**新存储成立（每条目一文件、派生索引、每个新存储一个「两写入者产生不同路径」的模拟测试）？[Non-Functional, Req §FR-025]
- [ ] CHK040 - 「行为保持而非仅路径存在」是否以一张可枚举的行为清单承载（记忆往返、feedback 链路、evidence 车道、exec-quant、trigger、retention、run-determination、一次派发注入），并逐项留有证据落点？[Measurability, Req §FR-026]

## Notes

- **勾选与判读**：`[x]` 表示该问题已依据需求文本（或点名的 owner 行）得到回答；答「否」即对 `requirements.md` 的 finding，不是一条实现任务。本阶段交付的是清单器械，逐条作答属于 analyze / review 的判定职责。
- **计数与追溯**：共 **40 条**，CHK001…CHK040；**40/40** 携带至少一个追溯锚（`[Req §…]` / `plan §…` / `[Gap]` / `[Assumption]`），满足 ≥80% 下限；soft cap 40 未超出；无 `Verify` / `Test` / `Confirm` / `Check` 开头的实现检验式条目。
- **新增而非覆盖**：本文件为 checklist 阶段**新增**清单；requirements 阶段产出的 `checklists/requirements.md` 保持原样，未被覆盖、未刷新。
- **机械读数**（2026-11-25）：`validate-requirements.py` → `status: ok`，0 error / 0 warning，326 行 / 36 definition rows（27 FR + 9 SC）/ 6 shared strings（逐字输出：`../test-evidence/checklist-requirements-validator.txt`）；requirements 的 Store Inventory 实测 17 行、假设裁定 16 条（A-1…A-16）、用户故事 6 个；`plan.md` 的 BC 清点实测 18 行（BC01…BC18）；`tasks.md` 实测 43 任务行；`contracts/` 实测 4 份 / 32 条款（C-8 / M-10 / P-6 / L-8）。
- **用户追加要求纳入**：需求原文「需要将所有不向前兼容的修改都在speckit.migrate命令中添加迁移逻辑」由 CHK016 与 CHK028…CHK033 承载（闭包映射、拒绝终态、禁止替代品、证据指针与变异演练、dry-run/apply 演示、维度集受控扩展）；追加要求的落位方式（新增 FR-027 / SC-009、不重编既有编号）由 CHK015 承载。
- **same-author 检测门**：不成立（见 Detection path）；未派发 fresh-context 检测代理，检测路径如实记录于此，不以委托路径冒充直接读。
- **Feature 状态**：本轮位于 `/speckit.implement` 之前，按 Feature Integration Protocol，checklist 不发起 `Implemented → Ready for Review` 迁移，仅产出清单。
