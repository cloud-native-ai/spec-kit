# Requirements Quality Checklist: Review P1 Governance（评审 P1 治理）

**Purpose**: 作为“需求写作的单元测试”，检验 063 需求文本的清晰性、完整性、可测试性、一致性、边界与术语质量；不验证实现行为。
**Created**: 2026-10-19
**Feature (Requirement Scope)**: 063 Review P1 Governance（评审 P1 治理） — `.specify/memory/features/063.md`
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md)、[tasks.md](../tasks.md)、[data-model.md](../data-model.md)、[contracts/](../contracts/) — 仅用于暴露需求缺口、歧义与冲突，不评价设计或实现。
**Depth**: Standard · **Audience**: Reviewer · **Focus**: 清晰性、完整性、可测试性、一致性、边界、术语
**Assumptions**: 用户输入已明确 checklist 主题与六个质量维度，访谈式问题按缺省值裁决（Depth=Standard、Audience=Reviewer、Focus=上列六维）。本 feature 的 requirements/plan/tasks 由先前阶段派发产出，本会话并非其作者，故 `objective-analysis-gate.md` 的同作者委派条件不触发；`plan.md`/`tasks.md`/`contracts/` 仅作 gap-finding 输入。

**Note**: 本清单由 `/speckit.checklist` 生成，只检验 **Requirements (What)** 的文本质量。清单项即使引用设计决策，也只质问“需求是否定义/是否一致/是否可判定”，不判定实现是否正确。编号 CHK001 起连续；每项均带质量维度与可追溯锚点（`[Req §…]`、`[Gap]`、`[Ambiguity]`、`[Conflict]`、`[Assumption]`）。

## 1. Requirement Completeness（完整性）

- [ ] CHK001 需求是否明确了 `/speckit.implement` 预检应重新捕获的**完整**冻结基线集合，覆盖 `<spec-dir>/notes/baseline-*`、`<spec-dir>/baseline-*` 与 `coverage-baseline.txt`（[[STR-002]]），而不是只列举其中一类？ [Completeness/Gap, Req §FR-022；对照 C-29/E12]
- [ ] CHK002 需求是否定义了“无契约集 feature 显式 skip”的落点与记录形态（写在哪里、由谁检查），使该义务可被观察而非只停留于口头？ [Completeness/Gap, Req §FR-004；对照 C-6]
- [ ] CHK003 需求是否定义了 waiver 的存放位置、生命周期与更新规则（谁能追加、何时视为失效），而不仅是四段字段格式？ [Completeness/Gap, Req §FR-008；对照 E5]
- [ ] CHK004 需求是否定义了 FR-017 所称“运行证据”的载体、路径与最小字段，使“调用者显式补测”的决定可被追溯？ [Completeness/Gap, Req §FR-017]
- [ ] CHK005 需求是否定义了 `.specify/memory/register.md` 不存在、不可写或缺少指针行表头时的行为（失败、创建、还是降级）？ [Completeness/Edge Case, Req §FR-009]
- [ ] CHK006 需求是否定义了已勾选却带 `Gap` 标签的条目、以及没有 `Req §` 引用可指向的 `Gap` 条目的处置语义（FR-006 要求回答引用 requirement 行）？ [Completeness/Gap, Req §FR-005, §FR-006]
- [ ] CHK007 需求是否定义了 backlog 行“附证据”的形态（证据放在行内、邻近文件还是提交说明）与可解析方式？ [Completeness/Gap, Req §FR-016, §US3.4]

## 2. Requirement Clarity（清晰性）

- [ ] CHK008 “逐字执行”与 FR-014 的尖括号占位符之间是否有明确关系——执行者应原样执行、还是先按占位约定代入运行时值？ [Clarity/Ambiguity, Req §US3, §SC-007, §FR-014]
- [ ] CHK009 “缺 2 个以上必填参数”是否明确包含恰好 2 个（≥2），并定义了“必填参数全集”的判定来源？ [Clarity/Boundary, Req §US3, §SC-008, §FR-015]
- [ ] CHK010 “ISO 日期”是否限定了粒度与形态（如 `YYYY-MM-DD` 日期、UTC 时间戳或带时区时间戳），使格式可机械判定？ [Clarity, Req §FR-018, §SC-009]
- [ ] CHK011 “复述环境判据”是否有可操作定义（哪些句式/字段构成复述、哪些属于无关散文），使 SC-009 的 100% 断言可被检查？ [Clarity/Measurability, Req §FR-018, §SC-009]
- [ ] CHK012 “内容哈希”是否明确哈希对象是归档文件的原始字节（含换行与编码），而不是规范化后的文本内容？ [Clarity/Ambiguity, Req §FR-019, §FR-020]
- [ ] CHK013 引用组允许的嵌套深度是否在规范性 FR 中与 Edge Cases 一致（FR-001 只说“同宽度”，Edge Cases 与 owner 说“一层”）？ [Clarity/Consistency, Req §FR-001, §Edge Cases]
- [ ] CHK014 “适用时以 `--reconcile` 收口”是否定义了“适用”的客观判据（哪些单元/哪些漂移状态必须使用），而非留给执行者临场判断？ [Clarity/Ambiguity, Req §FR-016]
- [ ] CHK015 “每个机制变更”与“变异演练”是否定义了计数单位与通过判据（按 FR、按契约条款还是按编辑文件；演练必须怎样转红才算成立）？ [Clarity/Measurability, Req §FR-027]
- [ ] CHK016 `upstream repair`、`inherited`、`attributable to this feature`、`undecidable` 四类是否各有判定标准，使归因者在类别间作选择时不依赖直觉？ [Clarity, Req §FR-022, §Assumptions]
- [ ] CHK017 “每个延期项已解决或豁免”中的“延期项”是否定义了范围与判定（tasks 的 `[~]`、checklist 延后项、waiver 覆盖项分别如何计入）？ [Clarity/Ambiguity, Req §FR-013, §US2.4]

## 3. Requirement Consistency（一致性）

- [ ] CHK018 FR-020 的“GATE-8 旁”与 FR-025 的“implement-feature SKILL 规定 red-first note 形态处”是否与代码中实际存在的锚点一致（设计已披露改为 Step 9 与 create-tasks 技能），需求文本是否应同步或显式引用该订正？ [Consistency/Conflict, Req §FR-020, §FR-025；对照 C-27/C-18]
- [ ] CHK019 FR-026 的“所有修复 MUST 落在框架源侧”与 FR-009/FR-016 要求的 `.specify/memory/register.md` 登记、`backlog.md` 状态翻转之间，是否说明了项目记忆类写入的豁免边界？ [Consistency/Conflict, Req §FR-009, §FR-016, §FR-026；SC-014]
- [ ] CHK020 FR-029 只枚举 062 的四个文件，而 SC-014/C-34 要求整个 062 目录零变更；只读范围是否在需求中统一（是否也覆盖 notes、verification、contracts、checklists）？ [Consistency/Conflict, Req §FR-029, §SC-014]
- [ ] CHK021 FR-014 对源参数的手写枚举（含“等”）是否被明确标注为示例并让位于引擎 parser 的权威集合，从而不与 FR-030 的“MUST NOT 手写固定枚举”冲突？ [Consistency, Req §FR-014, §FR-030]
- [ ] CHK022 当 `/speckit.review` 与“implement 之后运行的 `/speckit.checklist`”都能触发 `Implemented → Ready for Review` 时，需求是否定义了优先级、幂等语义或唯一归属？ [Consistency/Conflict, Req §FR-013, §US2.4]
- [ ] CHK023 US1.3 同时说“尚未冻结 coverage-baseline”与“`/speckit.tasks` 已按既有冻结时机产出该基线”；`baseline-missing` 的触发条件与 remedy 是否在该场景与 FR-003/FR-004 之间保持一致？ [Consistency/Ambiguity, Req §US1.3, §FR-003, §FR-004]

## 4. Acceptance Criteria & Measurability（可测试性）

- [ ] CHK024 每个以 100% 表述的 SC 是否都声明了非空分母（seed/fixture 的最小条数或覆盖域），使断言不会在零样本上空洞通过？ [Measurability, Req §SC-001–§SC-014]
- [ ] CHK025 SC-003 的“不再需要后续三提交修复环”是否被量化为可观察指标（如同一 Gap 的后续修复提交数 = 0），而不是对过程形态的叙述？ [Measurability, Req §SC-003]
- [ ] CHK026 SC-006 的“在同一运行中进入 Ready for Review”是否定义了“同一运行”的时间/调用边界（一次命令运行、一个 feature 生命周期，还是同一提交窗口）？ [Measurability, Req §SC-006]
- [ ] CHK027 SC-014 的“本特性提交窗口”是否由明确的起止 SHA 或基线定义，使 `git diff` 的 0 变更断言可复现？ [Measurability, Req §SC-014]
- [ ] CHK028 SC-005 的“登记行可解析到报告锚点与状态”是否定义了“可解析”的判据（锚点语法、目标文件存在性、状态词表），使检查不依赖人工解读？ [Measurability/Clarity, Req §FR-009, §SC-005]
- [ ] CHK029 SC-001 的“ASCII-only 与双宽度实现的覆盖率总数差异为 0”是否明确了比较对象与语料（同一实现的前后行为，还是两个实现；混合宽度语料在 ASCII-only 下本就不可能同数）？ [Measurability/Ambiguity, Req §SC-001, §US1.2]

## 5. Scenario & Edge Case Coverage（边界与场景覆盖）

- [ ] CHK030 F7 的来源场景包含环境导致的基线差异（如缺失可选依赖造成的失败名集合变化）；FR-022 的四分类是否覆盖这一类差异，还是只能被迫归入 `undecidable`/`inherited`？ [Coverage/Gap, Req §FR-022, §Assumptions]
- [ ] CHK031 当 spec 目录没有任何基线文件（或没有 `notes/` 目录）时，FR-022 的“集合从目录派生”是否定义了空集合的处理（无操作、首次捕获还是阶段可见问题）？ [Coverage/Edge Case, Req §FR-022]
- [ ] CHK032 对于在本特性落地前已运行过 tasks、没有 `coverage-baseline.txt` 的历史 feature，`baseline-missing` 的 remedy 与责任阶段是否仍成立，是否需要显式迁移路径？ [Coverage/Edge Case, Req §US1.3, §FR-003, §FR-004]
- [ ] CHK033 FR-018 要求任何复述环境判据的行携带 `(see § Environment Prerequisites)` 指针；作为唯一权威落点的该章节自身是否被明确豁免自指义务，边界是否写清？ [Coverage/Edge Case, Req §FR-018]

## 6. Non-Functional Requirements（非功能需求）

- [ ] CHK034 需求是否显式声明性能、安全、可访问性等非功能维度对本治理特性为 N/A（并给出理由），而不是仅以“无运行时平台”隐含排除？ [Completeness/Gap, Req §Out of Scope]

## 7. Dependencies & Assumptions（依赖与假设）

- [ ] CHK035 FR-022 依赖 `git log` 可提供足够历史来归因；需求是否记录了该环境假设（如浅克隆/历史重写时如何处理）？ [Assumption/Gap, Req §FR-022]
- [ ] CHK036 FR-014/FR-015 依赖三个引擎暴露由 parser 派生的参数清单；需求是否把该前置条件与版本不一致时的行为（拒绝未知参数、一次列全）写成可验收要求，而不只放在 Edge Cases？ [Dependency/Coverage, Req §FR-014, §FR-015, §Edge Cases]
- [ ] CHK037 FR-027 的“冻结的失败节点名单”是否引用其 artifact 路径与捕获口径，并明确“零新增失败”按名字级集合差（而非计数）判定？ [Dependency/Clarity, Req §FR-027, §SC-013]

## 8. Terminology & Ambiguities（术语与歧义）

- [ ] CHK038 需求引入的术语（`recheck`、`disposition`、`载体`、`畸形组`、`baseline-missing`、`undecidable`、`unverified`）是否各有定义或指向唯一 owner，而不是只在上下文中被使用？ [Terminology/Gap, Req §FR-001–§FR-025]
- [ ] CHK039 FR-011 的“Mode 5 自省”与现行机制名“A3 自省 (Introspection)”之间的关系是否在需求中说明（历史名/现行名），使读者能解析到实际入口？ [Terminology/Consistency, Req §FR-011；对照 C-13/D-5]
- [ ] CHK040 FR-021 的 `unverified` 是否被定义为模板状态词表中的一个取值，并说明它与既有的 `unknown`/`fail`/`deferred` 如何区分？ [Terminology/Consistency, Req §FR-019, §FR-021；对照 E10]

## Notes

- 勾选方式：`[x]`；发现可直接写在该条目下或链接到具体制品/行号。
- 本清单不修改 `requirements.md` / `plan.md` / `tasks.md` 的实质内容；确认的需求缺陷应回到对应阶段修复。
- 统计：40 项，8 个分组；全部条目带可追溯锚点（`Req §…` / `SC-…` / `Gap` / `Ambiguity` / `Conflict` / `Assumption`）。
- 生成依据：`.specify/shared/guidelines/checklist-methodology.md`、`.specify/templates/checklist-template.md`。
