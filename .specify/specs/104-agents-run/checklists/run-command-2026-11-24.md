# Requirements-Quality Checklist: /speckit.agents run — 显式 run 子命令与 superagent/subagent 架构自动应用（Agents Run）

**Purpose**: 检验 Feature 104 需求文本（`requirements.md`）的**写作质量**——显式 `run` 语法与路由是否可判定、角色自动性接线是否可按指针取证、多子代身份与可见性是否闭合到既有载体、SDD 探针边界与单代理红线是否一致、文档同源与陈旧字面量封闭集是否可机械判定、行为类条款取证路线与 SC 证据路径是否可复现。每条都是对需求文本（或它点名的 owner 行）的提问，**不是**对实现行为的检验：凡只有跑一遍产品才能回答的条目，本身就是本清单的缺陷。
**Created**: 2026-11-24
**Feature (Requirement Scope)**: `.specify/features/019-agents-command.md`（Feature 019 Agents Command，状态 `Implemented`；本轮 checklist 位于 `/speckit.implement` 之前，按 Feature Integration Protocol 的 conditional initiator 条款不发起 `Implemented → Ready for Review` 迁移，也不得为缺少 code-segment 结论报错或编造一个）
**Requirements (What)**: [../requirements.md](../requirements.md) — 本轮机械读数（2026-11-24，`validate-requirements.py`）：281 行 / 0 error / 0 warning；**24 FR**（FR-001…FR-024）、**7 SC**（SC-001…SC-007；final 1 / supporting 6）、**8 Shared Strings**（STR-001…STR-008）、5 个用户故事、10 条 Edge Cases、A-1…A-14、三段 Clarifications 会话。
**Specifications (How, context only)**: [../plan.md](../plan.md)、[../tasks.md](../tasks.md)（33 任务行）、[../contracts/](../contracts/)（35 条款：command 10 / dispatch 12 / docs 13）——**只**用于暴露需求的缺口、歧义与冲突，**从不**为它们自身打分。
**Readers**: 需要判定「104 的需求是否足以从 checklist 放行进 analyze / implement」的复核者——`/speckit.analyze` 的检测者、`/speckit.implement` 的协调者与后续接手本线的编写者；他们依据本清单、被引用的需求行与 `test-evidence/` 的机读读数取结论。
**Reading scenario**: 复核者打开本文件，决定三件事：(1) 哪几条需求缺陷必须在 analyze / implement 之前修掉；(2) 哪些项可登记为「已裁定、由下游承载」而放行；(3) 哪些项因判据依赖尚未落地的机制而保持 `not_evaluated`。按条末的 `[Req §…]` 锚回到需求正文逐字核对。
**Focus / Depth / Audience**: Focus = 阶段简报的七个聚焦簇（显式语法与路由 / 角色自动性与行为类-制品类取证 / 多子代身份与可见性 / 边界与治理 / 文档同源 / 行为类取证可复现性（变异演练 4/4）/ SC 可判定性与证据路径）；Depth = **Standard**（默认）；Audience = **Reviewer**（默认）。阶段简报（`$ARGUMENTS`）已使意图明确，技能 §2 的三个意图澄清问题按「已预答」跳过，默认值记录于此。
**Detection path**: same-author 条件**不成立**——`requirements.md` 由上一条无人值守 SDD 线内的独立 requirements 阶段执行体撰写，本轮执行体未曾撰写所分析的任何制品；按 `.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires 的「制品先于本会话或作者不同」分支，门不触发，未派发 fresh-context 检测代理。缺口扫描由本执行体直接完成；可机械核对的前提（FR / SC / STR 计数、FR-023 分类覆盖）均以程序读数当场取证，读数见 Notes。

**Note**: 由 `/speckit.checklist` 按 `.specify/skills/internal/create-checklist/SKILL.md` 生成，方法论 owner 为 `.specify/shared/guidelines/checklist-methodology.md`，结构模板为 `.specify/templates/checklist-template.md`。勾选一条的唯一依据是**需求文本本身**（或该条目点名的 owner 行）给出了答案；答「否」产出的是对 `requirements.md` 的 finding，不是一条实现任务。判据落在需求之外（下游文档 / 工具）时登记为**观察**；判据依赖尚未落地的机制时登记为 `not_evaluated`。

## 一、显式语法与路由

- [ ] CHK001 - 显式 `run` 语法是否已完整定义——动词形态、agent 名必填性、task 可选性、任务文本的终止边界（含空格与引号形态），使「一个 run 输入」可被逐字判别？[Clarity, Completeness, Req §FR-001, Req §Edge Cases]
- [ ] CHK002 - 六类输入（显式 run 带任务 / 仅 `run` + agent 名 / 裸 `run` / 空参数 / 歧义非空输入 / 团队多代理意图）是否各自被指派唯一结果，且分支之间无缝隙、无重叠？[Completeness, Req §FR-002, Req §FR-003, Req §FR-004]
- [ ] CHK003 - 「歧义的非空输入」是否给出可判定判据（什么构成歧义、由哪些词面或结构信号触发），而不是留给执行体自由裁量？[Ambiguity, Req §FR-002]
- [ ] CHK004 - 路由优先级是否完备且一致——显式动词优先于上下文推断时，run 对 create / refine / team 三类的失败分支是否逐一具名？[Consistency, Req §FR-002, Req §FR-014]
- [ ] CHK005 - 越界参数的处置是否可判定——以 `--target` 为例的参数类是否被界定为封闭集，「报告属于 `/speckit.team` 并请求澄清」的响应是否有可核对的输出形态？[Gap, Clarity, Req §Edge Cases]
- [ ] CHK006 - 三条停止字符串（[[STR-002]] / [[STR-003]] / [[STR-004]]）是否一一绑定其停止路径，且「派发数 = 0」有可计数的判定面？[Measurability, Req §FR-003, Req §FR-004, Req §FR-005, Req §SC-001]
- [ ] CHK007 - 「有界的可用项提示」是否被量化——上限值、省略计数声明方式与列表排序依据是否已指明，使「有界」可复现？[Clarity, Measurability, Req §FR-005, Req §US5]

## 二、角色自动性与协议接线

- [ ] CHK008 - 「架构自动应用」是否只以可观测义务表述（呈现 / 载荷 / 回传），且「无开关、无角色实体、无第二份定义」的禁止项是否齐备？[Clarity, Req §FR-006, Req §A-5]
- [ ] CHK009 - 派发前呈现的最小内容是否逐项枚举完整、每项可判定（身份三要素、任务简报、角色关系三要素、既有配置披露项）？[Completeness, Req §FR-007]
- [ ] CHK010 - 「披露而非阻断门禁、用户可在派发前叫停」的可用性是否被操作化——叫停作用于哪个时点、以什么输入表达，而不引入批准门？[Ambiguity, Req §FR-007]
- [ ] CHK011 - 七字段下行与五要素上行是否各自归属唯一 owner，且本规格只以指针引用、未复制规则文本？[Traceability, Req §FR-008, Req §FR-010]
- [ ] CHK012 - 载荷自检的缺陷集是否闭合（`role-transition` 标识、九个 item-id slug、七个下行字段逐项在场）且阻断时点（派发前）明确？[Completeness, Req §FR-009]
- [ ] CHK013 - 「incomplete 回传」是否按五要素逐项定义，含「无异常须显式写未发现异常」与「父侧不得代填」两条禁止？[Completeness, Req §FR-010]
- [ ] CHK014 - 行为类 / 制品类的二分是否覆盖全部 24 条 FR——FR-023 的两份清单之外仍有 FR-002 / 005 / 006 / 009 / 012 / 013 / 014 / 015 / 021 / 024 共 10 条未获类别与取证路线（本轮机械读数），其归属由哪条需求裁定？[Gap, Coverage, Req §FR-023]
- [ ] CHK015 - 「MUST NOT 声称契约测试覆盖行为类条款」的禁令是否同时约束测试文本与文档面，且违反时可被结构断言识别？[Measurability, Req §FR-023, Req §A-14]

## 三、多子代身份与可见性

- [ ] CHK016 - child label 的唯一性域是否被量化——「同一 superagent 下互不相同」之外，跨 superagent / 跨会话的碰撞是预防、允许还是明确排除？[Clarity, Req §FR-011]
- [ ] CHK017 - 「重试」是否以可观测输入定义（同一 agent + 同一任务被再次发起的形态），而不是依赖系统内部判定？[Ambiguity, Req §FR-011]
- [ ] CHK018 - 「迟到返回不被消费」是否指向具名归因 owner，并给出可观测结果（哪份记录 / 哪个判定表达该状态）？[Traceability, Req §FR-011, Req §SC-002]
- [ ] CHK019 - 多子代可见性载体是否封闭为恰好三类（artifact triplet、`exec-quant` 记录、`status-digest` 角色视图），且「零新增清单 / registry / 渲染器」与之一致？[Consistency, Req §FR-012]
- [ ] CHK020 - 同 agent 并发 run、一次 run = 一条边 = 一个子代、单单元并发读数三者是否互不矛盾，且与「一次 run 不扇出」的边界同读？[Consistency, Req §FR-013, Req §FR-017, Req §A-13, Req §Edge Cases]
- [ ] CHK021 - 根身份解析是否顺序明确且可判定（状态脊 / line registry 的既有标识优先，否则 owner 根标记），且禁止第二套根身份？[Clarity, Req §Edge Cases]

## 四、边界与治理

- [ ] CHK022 - SDD 授权探针的适用触发是否可判定——「指派 / 点名 SDD 驱动」的词面边界、收窄谓词的 owner 指针、以及「普通 run 不因缺 team / seat 被阻断」的正反例是否齐备？[Clarity, Req §FR-016, Req §A-7]
- [ ] CHK023 - 「run 不承担团队编排」在路由、单代理语义与边缘例三处是否表述一致，冲突时以哪条为准？[Consistency, Req §FR-014, Req §FR-002, Req §Edge Cases]
- [ ] CHK024 - 零第二机制边界是否以封闭清单表述（调度器 / 队列 / 传输 / 通知 / 持久化根 / registry / 渲染器），并给出零新增计数方法？[Completeness, Req §FR-015, Req §SC-005]
- [ ] CHK025 - 「create / refine 语义与写权保持不变」是否以可测方式表述——什么证据能显示它被改变（既有守卫 / 文本契约 / 基线比较）？[Measurability, Req §FR-014]
- [ ] CHK026 - 零新增依赖是否被量化（无新增第三方 import、只用标准库），且可在新增测试中被机械判定？[Measurability, Req §RS-001]

## 五、文档同源

- [ ] CHK027 - 单副本声明是否可判定——计数谓词（`^# /speckit.agents`）、改前基线（3）与目标（1）、命名文件是否齐备？[Measurability, Req §FR-018, Req §SC-004]
- [ ] CHK028 - 陈旧字面量集合是否封闭——四条具名 STR 之外，「同句式变体」由哪份谓词清单界定，还是留给评审裁量？[Ambiguity, Req §FR-020, Req §SC-004]
- [ ] CHK029 - 能力枚举面封闭清单是否完整，且「plan 阶段发现新枚举面」的并入程序（先改清单与 SC-005 允许集、后编辑）是否可执行？[Clarity, Req §FR-020]
- [ ] CHK030 - 三份串接副本合并为单份时，内容保全规则是否已声明——哪些内容允许删除（陈旧陈述）、哪些必须从旧副本保留（若有），使合并不成为静默丢内容？[Gap, Req §FR-018, Req §P-1]
- [ ] CHK031 - live / dated 边界是否一致——`docs/reference/history/` 的 dated record 豁免封写、live 文档面纠正义务，两者是否以同一判据区分？[Consistency, Req §A-8, Req §FR-020]

## 六、证据可复现性与 SC 可判定性

- [ ] CHK032 - 每条 SC 是否给出可复现的测量来源、采集方法与证据落点（命令 / 计数 / 记录路径），使第二位复核者可独立重放？[Measurability, Req §SC-001…SC-007, Req §Measurement Sources]
- [ ] CHK033 - SC-001 的「路由样例集」是否冻结为固定条数与固定样例（「显式 run ≥2 条」的开放表述如何避免样例随实现漂移）？[Clarity, Req §SC-001]
- [ ] CHK034 - 变异演练 4/4 是否定义完整——四个变异目标、各自钉住的检查、复原判据与记录落点是否齐备且可逐项重放？[Completeness, Req §SC-006]
- [ ] CHK035 - 相对绿判据是否在 FR-022 / FR-024 / SC-003 / SC-007 之间一致——名字级失败基线、既有红逐条点名、「不声称全绿」的表述是否同义？[Consistency, Req §SC-003, Req §SC-007]
- [ ] CHK036 - SC-005 的包含性声明是否可判定——基线参照物、按产物类分组的比较单元、允许差异集的扇出闭包导出与补集断言是否齐备？[Measurability, Req §SC-005]
- [ ] CHK037 - 行为类条款的取证路线是否定义且不越权——真源文本（指针面）+ 评审 + 变异演练三路证据，是否明确「契约测试只钉指针、不冒称行为覆盖」？[Consistency, Req §A-14, Req §FR-023]

## 七、假设与依赖

- [ ] CHK038 - 「派发内核与角色模型已交付」的前提是否有可核对的证据指针（而非断言），缺口审计五条与之一一对应？[Assumption, Req §A-2, Req §Overview]
- [ ] CHK039 - 只读引擎依赖是否逐条钉住 owner、契约路径与零修改义务，且消费接口（动作 / 退出码）有 pin？[Dependency, Req §RS-004…RS-007]
- [ ] CHK040 - Feature 019 绑定是否可追溯，且与 no-status-regression（`Implemented` 不回退）及本轮 checklist 不发起状态迁移的判读一致？[Traceability, Req §Related Feature]

## Notes

- **勾选与判读**：`[x]` 表示该问题已依据需求文本（或点名的 owner 行）得到回答；答「否」即对 `requirements.md` 的 finding，不是一条实现任务。本阶段交付的是清单器械，逐条作答属于 analyze / review 的判定职责。
- **计数与追溯**：共 **40 条**，CHK001…CHK040；**40/40** 携带至少一个追溯锚（`[Req §…]` / `[Gap]` / `[Ambiguity]` / `[Assumption]`），满足 ≥80% 下限；soft cap 40 未超出。
- **新增而非覆盖**：本文件为 checklist 阶段**新增**清单；requirements 阶段产出的 `checklists/requirements.md` 保持原样，未被覆盖、未刷新。
- **机械读数**（2026-11-24）：`validate-requirements.py` → `status: ok`，0 error / 0 warning，281 行 / 31 definition rows（24 FR + 7 SC）/ 8 shared strings。FR-023 分类覆盖读数（CHK014 依据）：行为类清单 6 条（FR-007 / 008 / 010 / 011 / 016 / 017），制品类清单 7 条（FR-001 / 003 / 004 / 018 / 019 / 020 / 022），其余 10 条（FR-002 / 005 / 006 / 009 / 012 / 013 / 014 / 015 / 021 / 024）未获类别。
- **same-author 检测门**：不成立（见 Detection path）；未派发 fresh-context 检测代理，检测路径如实记录于此，不以委托路径冒充直接读。
- **Feature 状态**：本轮位于 `/speckit.implement` 之前，按 Feature Integration Protocol，checklist 不发起 `Implemented → Ready for Review` 迁移，仅产出清单。
