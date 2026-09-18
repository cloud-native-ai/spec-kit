# Contract: constitution-export — 宪章双落点导出契约

**Feature**: 051 面向用户可理解性纪律  
**Guards**: `templates/constitution-template.md` 的两条新原则、`templates/commands/constitution.md` 的 `MUST include` 清单、活动宪章、具名双落点观察名单  
**Test file**: `tests/contract/test_constitution_double_landing.py`  
**Date**: 2026-09-17

条款编号 C-1…C-13 由测试函数名 `test_cN_*` 一一对应。落位与顺序裁定见 `research.md` D-9,命名冲突防线见 D-5,全称守卫不可实现的实测推翻见 D-6。

---

## 模板侧结构

**C-1** `templates/constitution-template.md` MUST 含两条新原则,标题逐字为:
- `### XII. One Source of Truth (Authority & Reference Discipline)`(STR-006,回流)
- `### XIII. User-Facing Comprehension (No Jargon, With Context)`(STR-003,新增)

两条 MUST 插在既有 Principle XI(`:132-141`)之后、`## [SECTION_2_NAME]`(`:143`)之前。模板原则总数由 11 变为 **13**。

**C-2** 每条新原则的结构 MUST 合规,逐项断言(形态取自既有最短完整实例 Principle XI `:132-141` 与 `templates/commands/constitution.md:163-168` 的 Formatting & Style):
- (a) 标题形态匹配 `^### [IVXLC]+\. .+$`;
- (b) 标题后紧随**一句以冒号结尾**的主张;
- (c) **3–6 条**要点,每条含 `MUST` 或 `MUST NOT`;
- (d) 每行硬折行 **<100 字符**;
- (e) 要点与 `Rationale:` 之间**恰好一个空行**;
- (f) 含以字面 `Rationale:` 起始的段落,长度 1–4 句;
- (g) 无未解释的方括号占位符残留。

**C-3** 每条新原则 MUST 含一条**锚定要点**,锚定 `.specify/shared/guidelines/` 下对应真源文档(STR-003 → STR-001;STR-006 → `one-source-of-truth.md`)并写明 "reference it, do not restate it" 语义。形态先例:`templates/constitution-template.md:103-106`。

**C-4** 每条新原则 MUST 含一条**范围限制要点**,声明该原则不新增机制(MUST NOT justify new scoring systems / maturity reports / tracking engines 语义)。形态先例:`templates/constitution-template.md:110-111`。

## 命令侧落点

**C-5** `templates/commands/constitution.md` 的 `MUST include` 清单 MUST 新增**两条**对应条目,形态逐字为 `- **MUST include** a principle for "<完整标题>" that mandates:`,插入位置在既有第 5 条(Better-Harness Orientation,`:111-125`)之后、`:126` 的 Governance 收尾要点之前。清单条目数由 5 变为 **7**。

**C-6** 每条新命令侧条目 MUST 含一条子要点,指明该原则锚定 `.specify/shared/guidelines/` 下的真源文档且 "MUST be referenced, not restated"(先例:`:118-119`),并含一条"不新增机制"子要点(先例:`:124-125`)。

## 具名双落点观察名单(FR-035,D-6 订正后的可实现形态)

**C-7** 测试 MUST 持有一份**具名双落点观察名单**常量,初始值为:

```python
DOUBLE_LANDING_WATCHLIST = (
    "User-Facing Comprehension (No Jargon, With Context)",
    "One Source of Truth (Authority & Reference Discipline)",
)
```

对名单中**每个完整标题**,MUST 同时成立:
- (a) 属于模板标题集 —— 由 regex `^### [IVXLC0-9]+\. (.+)$` 逐行捕获 `templates/constitution-template.md`;
- (b) 属于命令名称集 —— 由 regex `\*\*MUST include\*\* a principle for "([^"]+)"` 捕获 `templates/commands/constitution.md`。

判定 MUST 为**集合成员相等**,MUST NOT 为子串包含。

**C-8** 匹配 MUST NOT 钉死罗马数字字面量。模板与活动宪章的原则名册与编号本就不同(模板 13 条、活动宪章 15 条),钉死数字会在任一侧插入新原则时误报。

**C-9** **命名冲突防线**:`Code as the Single Source of Truth`(命令 `:91` 既有条目)与 `One Source of Truth (Authority & Reference Discipline)`(STR-006)MUST **不被判为同一原则**。测试 MUST 含一条显式断言:二者各自独立存在于命令名称集,且名单匹配对二者给出不同结果。依据:活动宪章 XIV 的 Rationale(`:163`)已显式区分二者;二者共享子串 `Source of Truth`,故子串匹配会误合并。

**C-10** **变异式有效性抽查**:人为从模板侧或命令侧删除名单内任一原则后,C-7 MUST 失败。该抽查 MUST 以临时副本或 monkeypatch 方式进行,MUST NOT 修改仓库内真实文件。首个受测样本为 STR-006——它历史上真的只落了活动宪章、从未回流模板(实测 `grep -c "One Source"` 在两个模板文件双双为 **0**),用它做样本可证明守卫拦得住一个**真实发生过**的同型缺口。

## 活动宪章侧

**C-11** `.specify/memory/constitution.md` MUST 含一条标题为 `### XV. User-Facing Comprehension (No Jargon, With Context)` 的原则(它已含 XIV = STR-006,故只新增一条),原则总数由 14 变为 **15**;结构合规判据同 C-2…C-4。

**C-12** `.specify/memory/constitution.md` 的 `**Version**:` 行前两段 MUST ≥ `(1, 12)`(实测改前为 `1.11.0`,MINOR 递增依 `templates/commands/constitution.md:66`),且文件头部 MUST 含本轮的 Sync Impact Report(前置 HTML 注释,依 `:142-148`)。断言形态对齐 `test_one_source_of_truth.py:175-180` 的版本下限先例,但 MUST NOT 复制其钉死罗马数字的做法(该既有测试 `:170` 用 regex `^### XIV\.` 钉死了活动宪章的数字,是本契约 C-8 明确要避免的形态)。

---

## 不由本契约守护的事项(边界)

- **`templates/plan-template.md` MUST 零改动**。其 `## Constitution Check`(`:31-42`)按 `:37` "Do NOT hard-code principle names here" + `:38-39` 动态枚举 `### <roman-or-arabic-numeral>. <name>`,故两条新原则自动进入下游 `plan` 门控。FR-026 要求**实测验证**该自动传导,方式见 `quickstart.md` 场景 5,不靠契约测试断言。
- **下游 bootstrap 拒绝该原则的路径**:`templates/commands/constitution.md:40-41` 授权拒绝不相关的模板原则。拒绝 MUST 记录进 Sync Impact Report(规格 US3 场景 4),该义务由命令文档承载,不由本契约机械断言。
- **模板与活动宪章的编号不一致属正常**:模板 XII/XIII 与活动宪章 XIV/XV 指向同一对原则,编号不同是因两份名册本就不同(模板是通用脚手架,活动宪章含本项目专有原则)。C-8 已禁止钉死数字。

## 门控预算中立(补充条款)

**C-13** 两条新原则块(XII 与 XIII)对 `scan-confirmation-gates.py` 的 `BLOCKING_RE` 命中数 MUST 各为 **0**。测试 MUST 以 `importlib` 内联加载真实扫描器并复用其 `BLOCKING_RE`,MUST NOT 重写模式副本。

> 本条落实 `contracts/gate-neutrality.md` C-1(c),此前该子条**只有撰写约束与扫描器 `total` 的间接探测**,没有直接断言。间接探测不足以定位问题:`constitution-template.md` 的路径命中 `GOVERNANCE_PATH_PATTERNS`,其命中被归类 `governance_kept` 而 **`governance_kept` 仍计入 `total`**,故一旦命中,`total` 只表现为 +1 而不指明是哪一块原则、哪一行。本条把定位粒度收敛到"两块新原则各自零命中"。

---

## 条款 → FR / SC 映射

| 条款 | FR | SC |
|---|---|---|
| C-1, C-2, C-3, C-4 | FR-024 | SC-005 |
| C-5, C-6 | FR-025 | SC-005 |
| C-7, C-8, C-9, C-10 | FR-035, FR-028, FR-029 ⑤ | SC-015 |
| C-11, C-12 | FR-027 | SC-005 |
| C-13 | FR-032 | SC-012 |
