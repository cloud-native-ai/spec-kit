# Specification Quality Checklist: 机器可判定的制品命题(Machine-Decidable Artifact Propositions)

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-09-23
**Feature**: [requirements.md](../requirements.md) · Feature 053 · Status `Draft`
**Validation runs**: 1 — 初稿。本清单在 `/speckit.clarify` 回写后 MUST 重新核验一次(依据:`shared/guidelines/requirements-guidelines.md` § Validation Process,以及本规格 FR-013 自己要求的「清单更新置于澄清回写之后」)。

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

### 未完成项(1 项)

- **`No [NEEDS CLARIFICATION] markers remain` → 未完成**:FR-027 保留 **1** 个活动标记(上限 3),问的是覆盖核算对既有 52 个 spec 的适用性——「仅对本特性之后新建的 spec 强制」与「对既有 spec 提供只读不合规清单而不阻断」两种读法都成立,工件无记录,且二者对范围的影响相差 110 份既有契约文件。该标记 MUST 由 `/speckit.clarify` 解决后才进 `/speckit.plan`。
  计数方式:只数**带冒号且未被反引号包裹**的实例(实测 1);被反引号包裹的提及不计入。这正是 FR-010 规定的形态,本清单按该形态自证。

### 三项判为通过但需说明理由的项

- **`No implementation details` / `No implementation details leak`**:本规格的交付物**就是**一组检查器的判定契约,故 action 名(`run-checks`)、退出码分档、机读字段名不可避免地被点名。处置遵循房子自己的机制:这些字面量全部集中在 `## Shared Strings`(模板对该节的用途说明明确包含「exit codes treated as contract」),下游制品以 `[[STR-NNN]]` 引用而不复写,故一次轮换只改一处。对既有制品的指名(`validate-tasks.py`、`scan-confirmation-gates.py`、`clarify-taxonomy.md`)是**引用现状锚点**,不是设计选择。`/speckit.plan` 应把 `STR-005`…`STR-007` 的具体形态下沉到 `contracts/`。
- **`Written for non-technical stakeholders`**:读者基线取**框架维护者/执行代理**,与 `.specify/shared/guidelines/requirements-guidelines.md` 的 reader baseline 一致;本特性的「用户」就是读制品与跑命令的那一方。
- **`Success criteria are technology-agnostic`**:12 条 SC 的**判据**均为可数量(命中数、集合差、退出码档位、前后校验和相等);工具名只出现在 `### Measurement Sources & Collection Methods`,即模板指定的采集方法落点。

### 本轮自证的两个缺陷(由本规格自己要消灭的那类检查发现)

初稿写完后按 FR-006…FR-010 的判据做了一次人工核验(校验器本身尚不存在,故用等价的 grep/awk 手工执行,含 `shared/constants/clarify-taxonomy.md:111` 那段**本规格 FR-014 要求将来移除**的过渡抽取式),查出两处并已就地修正:

1. **一处不可解析的 `[[STR-NNN]]` 引用**。US1 的验收场景 3 为了描述「不可解析引用」而**裸写**了一个示例编号,该示例本身成了本规格里的一个不可解析引用。修法:场景改为描述形态而不实例化它,并把「被反引号包裹者属提及而非引用」这一区分补进 **FR-009**——原先只有 FR-010 对活动标记做了该区分,对 STR 引用漏了同构的一条。这是本规格撰写过程对自己命题的一次实测命中。
2. **缺失一个必备 H2 节**。`## User Scenarios & Testing *(mandatory)*` 被漏写,导致 5 个用户故事与 `### Edge Cases` 挂在 `## Overview` 之下;节序核验查出后已补回,当前 H2 序为 Related Feature → Overview → User Scenarios & Testing → Requirements → Success Criteria → Shared Strings → Clarifications。

两处都属「结构命题为假而散文读起来通顺」——正是本特性要把判定权从目测交给程序的理由。

### 复验数据(2026-09-23 实测)

| 命题 | 实测值 | 判据 |
|---|---|---|
| FR 编号连续且按文档序 | 48 条,FR-001…FR-048,`ORDER BREAK` 0 | FR-007 / FR-008 |
| SC 编号连续且按文档序 | 12 条,SC-001…SC-012,`ORDER BREAK` 0 | FR-007 / FR-008 |
| `[[STR-NNN]]` 引用可解析 | 引用集 = 定义集 = {001…010},不可解析 0,定义而未被引用 0 | FR-009 |
| 活动标记计数 | 1(上限 3) | FR-010 |
| 模板占位符残留 | 0 | — |
| 必备节齐备且有序 | 7 个 H2 全部在场,序与模板一致 | — |
| 用户故事数与优先级分布 | 5(P1×2、P2×2、P3×1),无占位故事 | — |
| Edge Cases | 8 条,含门控预算余量为 0 这一条 | — |

### 交给下一阶段的依赖

- `/speckit.clarify` MUST 解决 FR-027 的活动标记,并按 `.specify/shared/workflow/feature-integration.md` § Feature Binding Rules 完成 `Related Feature` 绑定(本命令按约定保留 `Need clarification`,不自行绑定)。候选核验时注意:本特性**消费** `validate-tasks.py`、`goal-utils.py`、`clarify-taxonomy.md` 三处既有 owner,但为它们各新增能力,与 Feature 028(Feedback Mechanism)、040(Token Efficiency Discipline)的关系需按同胞吸收启发式逐个核验。
- `/speckit.plan` MUST 承接 FR-014 的债务:US1 落地时移除 `shared/constants/clarify-taxonomy.md` 的过渡 awk 抽取式与「Until that validator ships」一句。
- `/speckit.plan` MUST 把 FR-022 的条款语法 owner 归属作为一个显式设计决策处理(实测 110 份契约文件、仅 21 份采用 `**C-N**` 形态、当前无 owner)。
