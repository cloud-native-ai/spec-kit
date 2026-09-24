# Specification Quality Checklist: 机器可判定的制品命题(Machine-Decidable Artifact Propositions)

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-09-23
**Feature**: [requirements.md](../requirements.md) · Feature 053 · Status `Draft`
**Validation runs**: 2 — ① 2026-09-23 初稿(15/16,唯一未过项为 FR-027 的活动标记);② 2026-09-24 `/speckit.clarify` Mode A 回写**之后**复验(16/16)。本次复验即 FR-013 自己要求的「清单更新置于澄清回写之后」,依据 `shared/guidelines/requirements-guidelines.md` § Validation Process。

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
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

### 未完成项(0 项 — 初稿的 1 项已于第 2 轮关闭)

- **`No [NEEDS CLARIFICATION] markers remain` → 初稿未完成,现已通过**:FR-027 的活动标记已由 2026-09-24 `/speckit.clarify` Mode A 经用户裁定为「**冻结名字级基线,只对新增未覆盖项阻断**」并改写为该判据;`## Related Feature` 亦由同一轮裁定为**新建 Feature 053(Draft)**。实测活动标记 **0**。
  计数方式:只数**带冒号且未被反引号包裹**的实例——这正是 FR-010 规定的形态,本清单按该形态自证。
  附带处置:模板的 `ACTION REQUIRED`(「Keep the default values as "Need clarification"」)注释在绑定解析后按房子先例移除(050 / 051 / 052 三份规格均在解析后移除;全仓 44 份里仅 9 份仍保留,即绑定尚未解析者)。

### 第 2 轮(clarify 回写后)新查出并订正的规格自身缺陷

同作者检测已按 `.specify/shared/workflow/objective-analysis-gate.md` **委托**给 3 个新鲜上下文只读子代理(规格由同一 agent 在同一会话写成)。三路回传收敛为 4 个用户裁定问题 + **13 项纠正**,其中 **5 项是初稿的事实缺陷**,均经编排者复跑源码确认:

| # | 初稿所印 | 实测 | 证据 |
|---|---|---|---|
| 1 | `validate-tasks.py` 检查面 **5** 项 | **6** 项(漏 `dod-format`) | 该项由 `b4fb16cb`(2026-09-11)落地,**早于初稿自陈的实测日期 12 天** |
| 2 | 该脚本契约钉子 **0 个** | **2 处**(标签集钉 `EXPECTED_CHECKS` `:75-82` 由 `:314` 断言;退出码表钉 `test_c5_exit_code_table` `:346`) | `git merge-base --is-ancestor 46760e37 7c5598c0` 为真 ⇒ 钉子的提交是初稿提交的**祖先**,「零钉子」在写下那一刻就是假的 |
| 3 | FR-027 分母「既有 **52** 个 spec」 | **44** 个 spec 目录(42 个含 `contracts/`) | 52 是 `features.md` 的 `Total Features`,两个计数被混用 |
| 4 | FR-028:10 份 `.yaml` 可「解析其 operations」 | 分属**两种**语法:9 份 OpenAPI(条款全集 = `paths:` 下 HTTP 方法键,共 **39** 个;文件内**无**字面 `operations:` 键)+ 1 份 `assertions[].id`(**6** 条,文件名却是 `.openapi.yaml`) | 逐文件解析实测 |
| 5 | US2 验收场景 2 要求「exit 码为『有 WARN 无 ERROR』对应的那一档」 | **该档不存在**:既有表只有「无 ERROR → 0(警告不单独成档)」「有 ERROR → 1」 | `test_c5_exit_code_table:353,356` |

另 8 项纠正:术语归一(`校验器` 20 处 → 已登记的 Key Entity 名 `检查器`;第 6 行 `**Input**` 逐字记录按「日期化记录不作为当前现实被引用」豁免保留)· 两处对 `fast-fail.md` 的引用**指向不存在的条款名**(「机器绿条款」在 owner 里零命中,真名 `§ 判据同样覆盖机器给出的绿`)· 一处对已登记术语 `盲检 (Blind Check)` 另造 `假绿` · Shared Strings 的 `Consumed by` 列 **7** 处「点名了某 FR/SC 但该处未写出 `[[STR-NNN]]`」,其中 2 处把字面量**重打**了一遍(SC-008 的 `not-evaluated`、SC-007 的 `run-checks`),正是模板引用公约明令禁止的形态 · A-2 暗示 CI 是许可通道,与 FR-048 的封闭两通道集矛盾且实测本仓无任何 CI 配置 · STR-004 标注为**新造字面量**(实测在 `goal-utils.py` 零命中,有效词表是 STR-006 ∪ {STR-004}),STR-006 的 7 个字面量逐个实测命中 · 补 2 条边界情形(检查器从镜像副本被调用时的自定位自匹配、「可解析但抽出零条款」)· FR-022 补落点约束(`SCAN_DIRS` 含 `shared`,故新建在 `shared/definitions/` 下的 owner 文档从第一稿起就在零余量门控预算内)。

**一处编排者自身缺陷已订正**:整合第 4 个裁定时先写成 `FR-003a`,而本规格的边界情形明令「编号带字母后缀 MUST 判为形态违例」——规格违反了自己的规则。已折叠进 FR-003 本体,残留复核为 0。

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
| FR 编号连续且按文档序 | 48 条,FR-001…FR-048,`ORDER BREAK` **0** | FR-007 / FR-008 |
| SC 编号连续且按文档序 | 12 条,SC-001…SC-012,`ORDER BREAK` **0** | FR-007 / FR-008 |
| `[[STR-NNN]]` **正向**可解析 | 引用集 = 定义集 = {001…010},不可解析 **0**,定义而未被引用 **0** | FR-009 |
| `[[STR-NNN]]` **反向**一致(表内点名 → 该处确有引用) | 不符 **0**(初稿为 **7**,已全部改为引用形) | 模板 § Citation convention |
| 活动标记计数 | **0**(上限 3;初稿为 1) | FR-010 |
| 模板占位符残留 | **0** | — |
| 必备节齐备且有序 | **7** 个 H2 全部在场,序与模板一致 | — |
| 用户故事数与优先级分布 | **5**(P1×2、P2×2、P3×1),无占位故事 | — |
| Edge Cases | **10** 条(初稿 8,新增自定位自匹配与「可解析但抽出零条款」),含门控预算余量为 0 这一条 | — |
| `## Related Feature` 绑定 | 已解析为 **Feature 053**(全文件对 `Need clarification` 命中 **0**) | feature-integration.md § Feature Binding Rules |
| `## Clarifications` 回写 | `### Session 2026-09-24` 下 **4** 条 bullet,一条对应一个被接受的裁定 | clarify Mode A 步骤 5 |

**复验时间**:2026-09-24(clarify 回写之后)。以上每行均由程序实跑得出,非目测——初稿正是把这 11 行里的第 1、2 行写错了(检查面 5→6、钉子 0→2),而散文读起来完全通顺。

### 交给下一阶段的依赖

- ~~`/speckit.clarify` MUST 解决 FR-027 的活动标记并完成 `Related Feature` 绑定~~ — **已于 2026-09-24 完成**,4 项裁定的 Q→A 痕迹记在规格 `## Clarifications` > `### Session 2026-09-24`,绑定判定与逐候选排除理由记在规格 `## Related Feature` 与 `.specify/memory/features/053.md`。
- `/speckit.plan` MUST 承接 FR-014 的债务:US1 落地时移除 `shared/constants/clarify-taxonomy.md` 的过渡 awk 抽取式与「Until that validator ships」一句。
- `/speckit.plan` MUST 把 **FR-022 的条款语法 owner 归属**作为一个显式设计决策处理。实测输入已订正为:110 份契约里只有 **31** 份有机器可抽取形态(21 份 `**C-N**` + 9 份 OpenAPI/39 operation + 1 份结构化断言/6 条),**79 份 `.md` 一份都没有**;且 owner 文档若新建在 `shared/definitions/` 下,从第一稿起就落在门控扫描面内(`SCAN_DIRS` 含 `shared`)而预算整数余量为 **0**。
- `/speckit.plan` MUST 把 **FR-028 的 `.yaml` 处置**作为设计选择处理(两种语法各写一个抽取器,或逐个点名跳过并计入 FR-023 的伴生量)——本阶段只订正了其事实前提,未替 plan 做选择。
- `/speckit.plan` MUST 承接 **FR-027 裁定产生的新制品**:一份冻结的未覆盖项**名字级**基线文件,落在本特性目录(与 SC-012 的测试名字级基线同类但不同物),采集时机见 `### Measurement Sources & Collection Methods` 的 `FR-027 基线 Source` 行。
- **范围外但已实测的两笔欠账**(记在 `.specify/memory/features/053.md` § Future Evolution Suggestions,plan MUST NOT 顺手纳入):① `scripts/python/` 下四个脚本各自重复定义同一张 `EXIT_*` 表而 `shared/`、`templates/`、`docs/` 对该表的命中数为 **0**(无 owner),`skills/create-team/scripts/build-summary-input.py` 另有第五套且 3/4 语义相左;② `Consumed by` 列的**反向**检查全仓无守卫,US1 检查器是其最自然的落点。
