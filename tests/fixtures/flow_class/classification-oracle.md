# 分类正确性判定工作表（独立 oracle）— 069a / FR-006 / SC-001

**Readers**: 069a 的维护者与评审者，在改动分类判据、台账或 `test_flow_class_correctness.py` 时需要判断「期望值是否仍按判据得出」。
**Reading scenario**: 审阅正确性测试时先读本表的逐单元判据应用，再看测试是否只按本表断言；判据本身有争议时回到所有者文档，不在本表就地裁定。

## 这份文件是什么 / 不是什么（对象边界）

- **是** 正确性测试的**期望侧**（oracle）：按 `shared/definitions/flow-class-definitions.md` § 判据 的「唯一问题 + 两步判定」逐单元写下判定记录，供测试逐字段比对。
- **不是** 分类数据源：`flow-class-check.py` 不读本文件，本文件也不是 `contracts/flow-class-ledger.md` C-1 所说的「第二份单元 → 类别映射」——C-1 的封闭面是**消费方文档**（模板、技能、契约、门户），`tests/` 是测试夹具区，只承载判定记录。
- **不是** fixture 的副本：测试的**输入侧**（fixture 台账 `FIXTURE_ROWS`）在测试文件里单独维护，本表只写期望。两侧由不同段落、不同维护动作产生，因此「lookup 把台账原样抄回来」这条路径无法让本表变绿（那正是修复前的缺陷：期望值直接内联 fixture 的类别值）。

## 判定记录

**判定者**: fresh-context review pass（2026-10-24），只读所有者 § 判据 / § 两个取值 / § 判定依据 `basis`；判定时**不参考** fixture 台账与真实台账的取值。
**判据问题（唯一）**: 该流程的主交付物，其验收由什么判定？
**判据落点**: `shared/definitions/flow-class-definitions.md` § 判据（唯一问题 / 判定步骤 / 两个取值 / 判定依据 `basis` / 边界例）。

| unit_id | 主交付物（第一步） | 判定面（第二步） | 判据落点 | flow_class | basis | neutral |
|---|---|---|---|---|---|---|
| /speckit.docs | 文档空间：根入口文件与 `docs/` 树 | 读者面——读者读错或与外部事实不符才暴露；结构 / 链接 / 构建通过只是必要条件（边界例「站点构建通过不改变判定」） | § 两个取值 · expression | expression | reader-oracle |  |
| /speckit.humanize | 改写后的文本本身 | 读者面——自然度与保真是否被读者认可；无机器可观测的验收面 | § 两个取值 · expression | expression | reader-oracle |  |
| /speckit.requirements | `requirements.md` | 机器面——validator 的结构检查与下游 plan / tasks / implement 的消费；缺陷以检查失败或下游产物不可用显现 | § 判定步骤 · 机器面 | execution | behavior-oracle |  |
| /speckit.plan | `plan.md` | 机器面——`pre-analyze` 检查与下游 tasks 生成消费该产物 | § 判定步骤 · 机器面 | execution | behavior-oracle |  |
| /speckit.analyze | 跨产物一致性分析结论 | 机器面——结论可重跑复算，并作为门禁裁决被消费 | § 判定步骤 · 机器面 | execution | behavior-oracle |  |
| /speckit.implement | 代码与规格回填 | 两面签字——代码须运行通过（机器面）、规格回填须读者核（读者面）；按边界例「两面都必须签字」取 execution | § 判定步骤 · mixed-oracle | execution | mixed-oracle |  |
| skill:create-docs | 文档空间结构（`/speckit.docs` 的执行体） | 读者面——同 `/speckit.docs`，结构检查仅必要条件 | § 两个取值 · expression | expression | reader-oracle |  |
| skill:humanize | 改写后的文本（`/speckit.humanize` 的执行体） | 读者面——同 `/speckit.humanize` | § 两个取值 · expression | expression | reader-oracle |  |
| skill:git-utils | 平台对象与分支状态 | 机器面——以平台行为与仓库状态判定 | § 判定步骤 · 机器面 | execution | behavior-oracle |  |
| skill:memory-record | 调用方流程的记忆记录 | 机器面——记录被下游流程消费，本身无独立读者验收面；`category = memory` | § 判定依据 · behavior-oracle；类中立不豁免门禁 | execution | behavior-oracle | yes |

## 未登记探针（不属本表的判定记录）

`/speckit.ghost` 与 `skill:ghost` 是**未登记**探针：所有者 § 边界例「未登记单元 → 默认 `execution` 并在消费点标注」直接给出期望（默认类 + `未声明·按默认` 标记 + `source = default`）。它们不是判定结果，故不进上表，由测试内常量 `UNREGISTERED_PROBES` 承载。

## 维护规则

1. 改判据 → 先改所有者 § 判据，再按新判据重判**全部**行（`FR-006`：MUST NOT 就地逐案裁定）。
2. 改本表 → 同步说明判据落点；仅改 `flow_class` 而判据落点不变，视为判据缺陷信号，需在 PR 说明里解释。
3. 本表与 fixture 台账不一致时，测试必须转红——这正是它存在的理由。
