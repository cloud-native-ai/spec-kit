# Contract: 阶段命令接线（Stage Wiring）

**Feature**: 077-doc-sdd-integration
**Spec**: [requirements.md](../requirements.md)
**Owner 指针**：算子 id、阶段行与阻断级别归 `shared/workflow/expression-gates.md` § 阶段算子表与 § 调用点表；
类别判据归 `shared/definitions/flow-class-definitions.md`。本契约只登记**接线形态与文本卫生**，不复制任何表。

## 接线面

- **C-001** 接线面 MUST 恰为七个命令模板：`templates/commands/requirements.md`、`clarify.md`、`plan.md`、
  `tasks.md`、`checklist.md`、`analyze.md`、`implement.md`。`clarify` MUST 在内——门禁 owner 的阶段算子表为它
  登记了两行算子，排除它会让该阶段成为唯一无类感知的阶段。(FR-008, FR-023)

- **C-002** 每个模板 MUST 新增恰一个子节承载接线，子节标题逐字取 `research.md` R-9 登记的**唯一字面量**
  （该字面量的登记处只有 R-9 一处；模板、本契约、测试与剥离器一律从它取值，MUST NOT 各自复制一份字面量，
  MUST NOT 给它加后缀变体）。子节内 MUST 恰有**一次** lookup 调用，形态为
  `flow-class-check.py --action lookup --unit-id "spec:<spec 目录名>"`。同一次阶段运行 MUST 只读取一次。(FR-008)

- **C-003** 子节 MUST 携带两条 owner 指针（类别判据 owner 路径、门禁算子 owner 路径）、一条分支句、
  一条降级可见句与**一条退出码 1 的停止句**。停止句 MUST 表达：解析报作者输入错误（退出码 1）时本阶段**停下**，
  以阶段协议的异常行形态作最后一行输出并点名文件与行号，MUST NOT 落入「既有门禁集逐字不变」那一支继续执行
  （该支只覆盖退出码 0 的未声明/降级路径）。
  子节 MUST NOT 出现：任何 `G-` 算子 id、任何六面 face id 表、任何 `flow_class=` 或 `flow_class:` 赋值形、
  任何按特性号 / 路径 / 关键词 / 文件类型的允许列表。分支句 MUST 用语义措辞表达（表达类按阶段算子表执行本阶段
  登记的行；其余既有门禁集逐字不变）。(FR-008, FR-012, FR-005)

- **C-004** 分支句只允许两个分支：表达类执行该阶段在算子表中登记的行；其余（含未声明按默认）MUST 保持既有门禁集
  逐字不变。MUST NOT 存在第三个分支，MUST NOT 由模板自行判断「该阶段要不要走文档门禁」。(FR-010, FR-012)

## 时点

- **C-005** 六个阶段（clarify / plan / tasks / checklist / analyze / implement）的读取 MUST 发生在阶段入口，
  即早于该阶段第一件依赖类别的动作（产物生成或门禁判定，取先发生者）。`requirements` 阶段的读取 MUST 发生在
  声明行写入之后、`validate-requirements.py` 之前。(FR-006)

- **C-006** 命令与其委托技能在同一次产物变更上重叠时 MUST 复用调用方结果，技能 MUST NOT 再读一次。
  该复用义务由命令模板的接线子节声明，MUST NOT 通过修改委派技能实现。(FR-008, FR-023)

## execution 零行为变化

- **C-007** 执行类特性线的可观察行为 MUST 不变：零新增阻断检查、零新增必填章节，门禁判定集合与基线提交
  `c1cd4600` 逐项相同。可判定形态：把 C-002 的子节整块剥离后，七个模板 MUST 与基线提交的同名文件**逐字相同**
  （SHA-256 相等）。**剥离算法（钉死，可复算）**：① 起点 = 子节标题行（含）；② 终点 = 该行之后第一个同级或更高级
  标题行（`^#{1,3} `）的**前一行**（含；其后无标题则至文件末尾）——**块内出现任何同级或更高级标题（含 `###`）一律视为块结束**，
  子节正文 MUST NOT 嵌 `###` 小标题（需要分层时用 `####`，不匹配 `^#{1,3} `，不会提前截断）；③ 删除起点至终点，不额外插入或删除空行。
  为使该算法成立，子节块 MUST 以**恰一个空行**收尾（块末与下一个标题之间不得出现两个及以上空行），
  违反即判接线形态违规（由 C-013 的同一守卫断言）。算法与可复算样例的登记处是 `research.md` R-9。(FR-011)

- **C-008** 执行类阶段在引擎缺席时 MUST 照常完成：新增的类别读取对执行类 MUST 非阻断，降级只打印标签，
  MUST NOT 新增失败。(FR-009, FR-011)

## 切换只由类别驱动

- **C-009** 模板与技能 MUST NOT 内嵌按特性号、路径、关键词或文件类型的允许列表来判定是否走文档门禁。
  判定面 MUST 是「两条仅类别不同的夹具线跑同一模板，输出差异完全由声明解释」，且模板全文 grep
  MUST 不出现任何特性号或路径白名单。(FR-012)

- **C-010** 表达类特性线上，本阶段登记的 blocking 算子 MUST 真正阻断：任一面为 `not-evaluated` 时该阶段门禁判未通过。
  表达类 MUST NOT 继承代码型算子（测试执行、覆盖率、编译）；该线同时产出代码或站点时，代码型算子 MUST 按**产物**
  补回，MUST NOT 按类别补回。(FR-010)

## 编辑面与分发

- **C-011** 改动的唯一编辑面 MUST 是框架源。`.specify/` 运行时副本与各工具命令副本 MUST 由 `sync-mirrors.py` /
  `regen-command-copies.py` 产出，MUST NOT 手改。未刷新的项目 MUST 保持改动前行为（旧副本不含接线子节）。(FR-024)

- **C-012** 接线面 MUST 是封闭集：七个命令模板 + `templates/plan-template.md`（表达类 `## Document Structure` 骨架的产出方）+
  `skills/external/sdd-loop-driver/` 及其 `references/` + 两份 owner 文档 + `flow-class-check.py` +
  `doc-consistency-check.py`（仅新增 `--action structure`）。扩面 MUST 走契约修订，MUST NOT 由某个模板或技能就地扩面。(FR-023)

- **C-013** `tests/contract/test_expression_gate_wiring.py` 的闭合集断言 MUST 在同一改动内把七个模板并入已接线名册，
  分母断言（模板与技能清单规模）MUST 保持不变。MUST NOT 删除该断言，MUST NOT 把它放宽成「任一面板可接线」。
  同一守卫 MUST 同时断言：七模板各恰一个子节、子节块以恰一个空行收尾、**剥离后与基线逐字相同**，且**子节在场**——
  否则它在无接线时空转（空绿）。(FR-023)
