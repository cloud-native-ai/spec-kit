# Contract: 宪章双落点导出 (constitution-export)

**Feature**: 052 快速失败纪律(Fast Fail)  
**Guards**: `requirements.md` FR-031…FR-034, FR-024  
**Test files**: `tests/contract/test_constitution_double_landing.py`(**既有**,上调四钉)、`tests/contract/test_user_facing_comprehension_doc.py`(**既有**,上调 C-14 一钉)、`tests/contract/test_fast_fail_discipline.py`(函数名 `test_xN_*`)  
**Date**: 2026-09-23

条款号在本文件内独立编号;跨文件引用 MUST 写作 `constitution-export.md C-N`。

---

## 双落点:模板原则 + 命令条目

**C-1** `templates/constitution-template.md` MUST 新增一条原则,标题为 [[STR-004]] = `Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest)`,编号为 **XIV**(接在既有 XIII 之后)。〔改前实测:模板原则 I–XIII 共 **13** 条,`### XIII.` 在 `:169`〕

**C-2** `templates/commands/constitution.md` 的 `MUST include` 清单 MUST 新增一条对应条目,其引号内标题 MUST 与 C-1 的标题**逐字一致**。〔改前实测:该清单 **7** 条,位于 `:77,87,91,100,111,126,137`;新条目插在 `:137` 那条之后、`:149` 的 Governance 收尾项之前〕

**C-3** **双落点缺一即未完成**:模板有原则而命令无条目、或命令有条目而模板无原则,MUST 各自转红。守卫形态为两侧各一次具名标题断言 + 一个观察名单(watchlist)按集合成员双向断言,并配一次**变异演练**(从任一侧删去该标题都能红)。

## 活动宪章

**C-4** `.specify/memory/constitution.md` MUST 新增对应原则,编号为 **XVI**(接在既有 XV 之后)。〔改前实测:活动宪章原则 I–XV 共 **15** 条,`### XV.` 在 `:168`〕

**C-5** 活动宪章版本 MUST 由 `1.12.0` 按 **MINOR** 递增至 **`1.13.0`**,`**Last Amended**` MUST 更新。〔改前实测:`:254` `**Version**: 1.12.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-09-18`〕

**C-6** 活动宪章 MUST 前置一份 Sync Impact Report(HTML 注释块),其形态对齐既有块(实测 `:1-21`):含 `Version change:` 行(注明 bump 类型与新增原则)、Added / Modified / Removed、`Templates requiring updates:`(逐项 ✅ / ⚠)、`Follow-up TODOs:`、`Preserved by design:`。

**C-7** **版本号形态取 3 段**(D-7)。上游分歧如实记录:`templates/commands/constitution.md:64-70` 要求 4 段 `x.y.z.ddd`,而活动宪章与 051 的修订均为 3 段,且守卫 `test_constitution_double_landing.py:420` 只解析 `(\d+)\.(\d+)` 两段。取 3 段是唯一与仓库实况及守卫解析口径一致的读法;该分歧属上游缺陷,MUST NOT 由本特性顺手改写命令模板。

## 原则块结构

**C-8** 新增原则块(模板 XIV 与活动 XVI 各一份)MUST 符合既有结构:`### <罗马数字>. <Title>` → 以冒号结尾的主张句 → 携 `MUST` / `MUST NOT` 的 `- ` 要点 → **恰好一个空行** → `Rationale:` 段。

**C-9** 每份新增原则块 MUST 含:(a) 一条以路径援引 [[STR-002]] 的**指针要点**,并写明消费者 MUST 引用而 MUST NOT 复述;(b) 一条**不新增机制**要点,点名拒绝的机制形态(异常检测引擎 / 分流评分器 / 成熟度报告 / 台账或注册表)。

**C-10** 新增原则块的每一行 MUST 硬折行至 **< 100 字符**(既有守卫 `test_constitution_double_landing.py:165-167` 断言此宽度)。

**C-11** 新增原则块 MUST NOT 复述分流判据、两份清单的条目、或注入子句的正文(FR-034)——只以路径援引真源文档。

**C-12** 新增原则块 MUST 项目中立:MUST NOT 含 `spec-kit` / `specify-cli` / `specify_cli` / `cloud-native-ai`。

## 既有钉子同批上调

**C-13** `tests/contract/test_constitution_double_landing.py` 的四个常量 MUST 在**同一批**变更中上调:

| 常量 | 改前(实测) | 改后 | 断言形态 |
|---|---|---|---|
| `TEMPLATE_COUNT` (`:65`) | 13 | **14** | 相等(`:202`) |
| `LIVE_COUNT` (`:66`) | 15 | **16** | 相等(`:408`) |
| `COMMAND_COUNT` (`:67`) | 7 | **8** | 相等(`:255`) |
| `MIN_VERSION` (`:68`) | `(1, 12)` | **`(1, 13)`** | 下限(`>=`,`:423`) |

**C-14** `MIN_VERSION` 是**下限语义**,故 `1.13.0` 本就通过;上调至 `(1,13)` 不是为了让测试通过,而是为了把下限推到本特性之后——否则后续特性可以在不新增原则的情况下退回 1.12 而不被发现。该理由 MUST 记入实现期提交说明。

**C-15** `DOUBLE_LANDING_WATCHLIST`(`:47-50`,改前含 2 个标题)MUST 增入 [[STR-004]],使新原则与既有两条同样受"两侧按集合成员双向断言"保护。

## plan 模板零改动

**C-16** `templates/plan-template.md` MUST **零改动**。其 `## Constitution Check`(`:31`)明写 `Do NOT hard-code principle names here`(`:37`),按 `### <numeral>. <name>` 动态枚举并每条渲染一行(`:40`)⇒ 新原则一旦进入宪章即自动抵达下游每次 `/speckit.plan` 门控。

**C-17** 反空真哨兵:C-16 断言"该文件零改动"时,MUST 同时断言"该文件的动态枚举指令文本仍在场"(即 `:37` 与 `:40` 的关键短语命中),使"零改动因为无需改"与"零改动因为枚举机制被删掉了"可区分。

**C-18** 下游传导 MUST 可实测:对一个样例宪章渲染 plan 模板的枚举逻辑,其门控行数 MUST 由 **15** 增至 **16**(SC-006)。

## 跨纪律改动:类 ⑪ 登记(D-4)

**C-19** `shared/guidelines/user-facing-comprehension.md` 的界面类映射表中,类 **⑪ 失败如实报告** 的「规则真源文件」列 MUST 增入 `shared/guidelines/fast-fail.md`(该列已支持多文件——类 ⑤ 就列了两个)。〔改前实测:类 ⑪ 行现为 `| ⑪ | 失败如实报告 | shared/guidelines/confirmation-gates.md | — |`〕

**C-20** `tests/contract/test_user_facing_comprehension_doc.py` 的 C-14 断言(`:400-402`,`len(deduped) == 8`)MUST 在**同一批**变更中上调为 **9**。〔改前实测:去重后的 8 个规则真源路径为 `confirmation-gates.md` / `feedback-step.md` / `interview-pattern.md` / `clarify.md` / `requirements-guidelines.md` / `proactive-trigger.md` / `reporting-playbook.md` / `glossary.md`;加入 `fast-fail.md` 后为 9〕

**C-21** 该表的 `reader_baseline_override` 列 MUST **不变**(类 ⑪ 该列为 `—`),故 `test_c18a_override_registry_has_at_most_two_entries`(`:489`,上限 2)不受影响。本条 MUST 被显式核验而非假定。

**C-22** **这是本特性对 Feature 051 拥有制品的唯一改动**,MUST 作为一次**显式列出的跨纪律改动**处理(FR-024):在 `plan.md` › Feature List Review、`feature-ref.md`、以及 `features/051.md` 与 `features/052.md` 双方的交叉引用中各留痕一次;MUST NOT 默默发生。

**C-23** 分工边界 MUST 在真源文档中载明:上送件的**四要素内容下限**归本纪律,类 ⑪ 的**措辞与上下文规则**仍归其既有拥有者;本纪律的真源文档 MUST NOT 成为类 ⑪ 的第二规则真源(FR-024)。

---

## 条款 → FR / SC 映射

| 条款 | FR | SC | 备注 |
|---|---|---|---|
| C-1, C-2, C-3 | FR-031 | SC-006 | 双落点缺一即红 + 变异演练 |
| C-4, C-5, C-6, C-7 | FR-032 | SC-006 | 版本 3 段形态,上游分歧已记录 |
| C-8…C-12 | FR-031, FR-034 | SC-006 | 块结构 + 折行 + 中立 |
| C-13, C-14, C-15 | FR-032 | SC-006 | 四钉同批上调 |
| C-16, C-17, C-18 | FR-033 | SC-006 | 零改动 + 反空真哨兵 + 下游可实测 |
| C-19…C-23 | FR-024, FR-074 | SC-003 | 跨纪律,显式留痕 |
