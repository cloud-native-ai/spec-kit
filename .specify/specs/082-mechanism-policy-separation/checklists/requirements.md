# Specification Quality Checklist: 机制/策略分离（Mechanism–Policy Separation）

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-11-05
**Feature**: `.specify/specs/082-mechanism-policy-separation/requirements.md`

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Stability / containment claims name a baseline referent and a derivable allowed-delta set (owner: `.specify/shared/guidelines/closed-set-claims.md`)
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria (with the gap recorded under Notes — SC-003)
- [x] No implementation details leak into specification

## Notes

- **Deterministic checker（所有计数的唯一权威）**：`python3 scripts/python/validate-requirements.py .specify/specs/082-mechanism-policy-separation/requirements.md` → `status: ok`；`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id` / `path-marker` 全 pass；`scanned: 199 lines, 23 definition rows, 3 shared strings`；`0 error(s), 0 warning(s)`；exit 0。逐字输出存于 `test-evidence/validate-requirements.txt`，本清单**不手抄任何计数**：23 个定义行 = 18 条 FR + 10 条 SC 中的定义行，拆分口径以该次运行的分项 pass 计数为准。
- **本 pass 修掉的两类问题（disclosed，非掩盖）**：① validator 的 4 条 `ref-resolvable`（2 条 error + 2 条 warning）——FR-001 / FR-017 的 `[[STR-001]]` / `[[STR-003]]` 被反引号包裹，落在代码 span 内故未被识别为引用；去掉外侧反引号后双向检查归零。② **同一判据的两处同文本枚举**：FR-001 原句把「机制侧=逻辑/算法/步骤/判定规则/可复用方法、策略侧=配置/输入/输出/运行环境绑定/目标目录/交付物落点」写进正文，而 § Terminology 有逐字相同的表；§ Assumptions A2 与 § Constraints C6 已明写后者是 dated record、owner 定稿后本规格不再更新，两处同步即为 FR-015 所禁的「复制 owner 内容」。已把枚举从 FR-001 移出、改由其判据段（§ Terminology 的「换掉运行环境要不要改」）与 FR-002(a) 派生，记录于 § Assumptions A10。此为纠正而非改判据：判据字句、Shared Strings 三行的值与 `Consumed by` 单元格、`Related Feature` 均未改动。
- **Flow class（类别声明的机器读数）**：`python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:082-mechanism-policy-separation"` → `flow_class: execution`、`source: declaration`、`marker: null`、exit 0；输出存于 `test-evidence/flow-class-lookup.txt`。故 `source` 由声明（[[STR-001]] 行）解析而非按默认兜底，`path-marker` 的「`execution` 类须至少一条 `final` path」这一条据此适用并通过。
- **`Stability / containment claims` 的判定依据（判通过，理由同处可见）**：本规格只有 **SC-003** 一条包含性声明，它按 owner 五要件写足——① 基线参照物：`[[STR-002]]` 指名的实现起点提交；② 比较单元：按产物类声明（技能与命令模板两类路径），不用「其余 / 叶子 / 未受影响」等聚合词；③ 允许差异集来源：按产物类声明并**配漂移守卫**（与 owner 要件 3 的手写形态一致，非字节点清单）；④ 补集断言 + 结构不变量两侧齐全；⑤ 未定义聚合词清零。SC-001 / SC-002 / SC-004 / SC-005 是确定性或检出率断言，不与包含性混用（owner § 两类断言必须分开）。
- **`Written for non-technical stakeholders` 的判定依据**：本工件属 `.specify/shared/guidelines/user-facing-comprehension.md` 面向用户界面类的第 ⑦ 类，基准读者为「未在本会话打开过本仓、但具备本领域知识的人」。工件中的 `FR-NNN` / `SC-NNN` / `A-nn` / `C-nn` 与路径属该 owner 白名单的标识符与短形式；owner 与判据一律以路径引用而非复述。据此判通过。
- **三处「实现细节」判项（判通过，理由非循环）**：本特性的**主体就是框架自己的归档纪律与元技能流程**，因此 `skills/external/...` 路径、`shared/guidelines/...` owner 路径、`${SKILL_HOME}` / `${SKILL_WORKDIR}` 是用户指令逐字给定的**验收对象**，不是作者擅自选定的 HOW；规格未固定数据结构、算法或第三方依赖，且 § Assumptions A5 / A6 / § Constraints C8 明令本阶段不预设脚本、不新增门禁。据此 `No implementation details` 与 `No implementation details leak` 判通过。
- **已记录的缺口（判「Feature meets measurable outcomes」时如实记入，未掩盖）**：SC-001 / SC-002 / SC-005 的**分母尚未定量**——SC-002 的「成员表全量」要等 C1 谓词在 plan 定稿后才有确定集合，SC-001 的样本集与 SC-005 的样例题集同样由 owner 文档附录给出、此刻尚不存在。按 requirements-guidelines § Success Criteria Guidelines 的可测性要求，三条都是**可测但基数待定**，故本条判为带有已记录缺口的 pass：plan 阶段 MUST 把三个分母落成机械可得的集合，否则升级为缺口。闭环口径已写在各自 `**Path**:` 标注——SC-001～SC-004 为 `final`、SC-005 为 `supporting`，`path-marker` 判项据此通过。
- **待 clarify 落定的一项**：`Related Feature` 保持 `Need clarification`（§ Assumptions A8 / § Constraints C7）——`create-requirements` 不自行绑定。这不是规格缺陷；`/speckit.clarify` MUST 在 plan 之前完成绑定，并复核 C7 提到的既有 Feature 候选。
- **零澄清标记**：`marker-count` pass（0）。缺省裁决记在 § Assumptions（A1–A10）与 § Constraints（C1–C8），其中 A3（不新增第三个环境变量）、A6（探针不抽成脚本）、C1（元层谓词把 `coaching-skills` 判为不纳入强制检查）是三个真正做了选择的点，clarify 阶段可推翻，推翻须给出证据。
