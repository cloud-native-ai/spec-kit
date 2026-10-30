# Contract: 确定性检查器（Checker）

**Feature**: 078-bilingual-expression
**Spec**: [requirements.md](../requirements.md)
**Owner 指针**：定义处信号清单归 [[STR-001]] § 定义处与可判定信号；豁免面归其 § 豁免面；
词汇表读取协议归 `scripts/python/glossary-utils.py`。本契约钉检查器的**行为契约**（入口、退出码、
扫描规则、判定边界），不复制 owner 的规则正文。实现载体：`scripts/python/bilingual-expression-check.py`
（框架源，镜像 `.specify/scripts/python/`；MUST NOT 并入 `doc-consistency-check.py`，研究记录 R-7）。

## 入口与退出码

- **C-001** 检查器 MUST 提供三个动作：`scan`（形态判定）、`coverage`（覆盖面核验）、`census`（SC-005 全查）。命令形态：`python3 scripts/python/bilingual-expression-check.py --action scan --path <file|dir> [--scope full|changed] [--json]`；`coverage` 与 `census` 不接受 `--path` 覆盖默认范围（范围归 owner 文档覆盖面清单，见 C-007)。所有动作打印 JSON 摘要到 stdout（人类可读明细行 + `--json` 纯 JSON），finding 明细逐行 `file:line [code] message`。(FR-009, FR-010)

- **C-002** 退出码封闭三段：`0` = 无 findings；`1` = 有 findings；`2` = 用法错误（未知动作、缺失参数、路径不存在）。退出码 MUST NOT 因 findings 数量或文件数量改变语义。(FR-010)

- **C-003** 检查器 MUST NOT 在本特性内绑定任何阶段门禁算子（FR-010）；挂接面 = 本契约的退出码契约 + `contracts/measurement.md` 的采证时机（维护者提交前自跑 + review 阶段采证）。(FR-010)

## 扫描规则（豁免面机械执行）

- **C-004** `scan` MUST NOT 进入围栏代码块（``` / ~~~）与行内代码span（`` ` ``）内部；代码块状态 MUST 按行线性跟踪（围栏可出现在任意列）。被豁免区间内的任何括号形态 MUST NOT 产生 finding。链接目标（`[...](...)` 的括号段）与图片语法同样豁免。(FR-004, FR-009)

- **C-005** `scan` 的输入行 MUST 只取 owner 文档登记的可判定信号命中的行（S1 表体行 / S2 标题行 / S3 加粗定义行）；非信号行的任何形态 MUST NOT 产生 finding（FR-002：每一次提及不要求双语）。S4 只用于主语言判定，不单独产生 finding。(FR-002, FR-009)

## 三类机械判定

- **C-006** 判定 (a)：信号行 MUST 含半角括号双语形态（紧贴、无前置空格），形态常量的逐字形态归 owner 文档 C-005 登记行；缺失即 finding 码 `missing-bilingual`。(FR-009(a))

- **C-007** 判定 (b)：信号行括号内词条的脚本类（CJK/拉丁）MUST 与括号外主词条相反；括号语言与文档主语言同向即 finding 码 `same-language-bracket`。文档主语言取 S4 信号（声明优先，缺省为正文 CJK/拉丁字母占比高者）。(FR-009(b), FR-003)

- **C-008** 判定 (c)：`coverage` 动作 MUST 核验 owner 文档覆盖面清单登记的每个定义面存在且非空（词汇表文件、`shared/definitions/`、`shared/guidelines/` 与 `shared/workflow/` 标题面、宪法原则标题、instructions ambient 标题、`templates/` 章节标题、命令与技能名首次定义处的承载文件）；整面缺失即 finding 码 `coverage-missing` 并输出缺失项清单。(FR-009(c), FR-007)

- **C-009** `scan` 对信号行上的全角括号形态（`（`…`）` 紧贴词条）MUST 报 finding 码 `full-width-parens`。四值码集封闭：`full-width-parens` / `same-language-bracket` / `missing-bilingual` / `coverage-missing`；新增码 MUST 走本契约修订。(FR-009, A4)

- **C-010** `scan --scope changed` MUST 只判定改动路径（调用方以 `git diff --name-only <base>..HEAD` 与 `git status --porcelain` 的并集传入）上的信号行；`--scope full` 判定覆盖面清单全量并产出 E6 存量差异清单（dated record，append-only）。SC-002 的合规率分母只取 `--scope changed` 的信号行（FR-006/FR-016：存量不入分母）。(FR-016, SC-002)

- **C-011** `census` 动作 MUST 读取 `.specify/memory/glossary.md` 全部双语 Canonical 词条（复用 `glossary-utils.py` 的表解析模式），对覆盖面清单全量扫描这些词条的定义行，比对中文侧用词与 Canonical 中文侧逐字一致；不一致逐条输出 `file:line [code] message`。抽样比例 = 100% census（R-11）；执行主体是程序，LLM MUST NOT 参与匹配与计数。(FR-005, FR-009, FR-010, SC-005)

- **C-012** 检查器 MUST NOT 做语义判断（「括号内的英文是否译得准」「这行是否定义处」的信号外部分）；判定只读字符形态与脚本类。LLM MUST NOT 参与匹配、计数或 finding 归因。(FR-009, A7)
