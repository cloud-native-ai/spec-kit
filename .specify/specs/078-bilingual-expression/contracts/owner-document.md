# Contract: 约定本体 owner 文档（Owner Document）

**Feature**: 078-bilingual-expression
**Spec**: [requirements.md](../requirements.md)
**Owner 指针**：双语规则的六组事实（方向、形态、覆盖面、豁免、一致性、迁移）唯一 owner 是
`shared/guidelines/bilingual-expression.md`（[[STR-001]]）；读者基准归
`shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议；词汇表协议归
`shared/workflow/glossary.md`。本契约只钉 owner 文档的**结构与可判定性**，不复制规则正文。

## Owner 声明与读者面

- **C-001** owner 文档 MUST 在其头部（前 40 非空行内）声明：本文件是双语表述约定的唯一 owner，并逐字点名拥有的六组事实（方向规则、唯一形态、覆盖定义面封闭集、豁免面封闭集、一致性规则、迁移边界）。同一头部 MUST 含 `**Readers**` 与 `**Reading scenario**` 两行且值非空；两行任一缺失或为空即 `reader-declaration-missing`（blocking，判定器 `doc-consistency-check.py --faces reader`）。(FR-001, FR-002)

- **C-002** owner 文档的四组枚举（方向规则、覆盖定义面、豁免面，及唯一形态的字面量条款）MUST 各以 Markdown 列表形态成文（`- ` 引导的列表项），使 SC-001 关键词表可由程序机械派生（逐列表项取字面量）。枚举 MUST NOT 以散文段落形态书写（散文不可派生）。(FR-001, SC-001)

## 定义处与信号

- **C-003** owner 文档 MUST 给出「定义处」的可判定信号清单，信号 id 封闭为 `S1…S4`：S1 词汇表表体行；S2 覆盖定义面文档的章节标题行；S3 prose 中加粗引导定义行（`**<词条>**` 紧接括号/破折号/冒号）；S4 文档主语言声明行与无声明时的保守缺省（正文 CJK/拉丁字母占比）。信号清单之外的新形态不在检查器判定范围，由评审面承担，owner 文档下次修订时补信号。(FR-002, FR-010)

- **C-004** owner 文档 MUST 明确「首次定义」的语义判断不属于任何可判定信号——检查器 MUST NOT 尝试判定它（A7），该面由评审承担。(FR-002)

## 形态与方向（结构面，非内容复述）

- **C-005** owner 文档 MUST 以逐字字面量给出唯一形态（[[STR-002]] 与 [[STR-003]]，半角括号、紧贴），并给出检查器使用的形态判定正则的唯一登记行。大小写维度随词条逐字匹配（FR-005 的精确一致性自然覆盖大小写）。(FR-003, A4)

- **C-006** owner 文档 MUST 规定主语言混合文档的判定信号（文档头/frontmatter/首段声明优先）与无法判定时的保守缺省（按段落各自语言执行方向规则，不强制统一）。(FR-003)

## 覆盖面与豁免（封闭集纪律）

- **C-007** 覆盖定义面封闭集与豁免面封闭集 MUST 各自成列表，增删只能经本文件修订（FR-007 封闭集纪律）；任何消费方（命令模板、技能、契约、测试、instructions、词汇表）MUST 以「路径 + 章节锚」引用本文件，MUST NOT 复述两组清单的条目枚举。(FR-001, FR-004, FR-007)

- **C-008** owner 文档 MUST 声明与 `shared/guidelines/user-facing-comprehension.md` jargon 白名单的交界处理：白名单术语的提及处维持可白名单状态，定义处仍须双语（FR-013）。交界句只在本文件与本契约出现，白名单本身归其 owner。(FR-013)

- **C-009** owner 文档 MUST 声明迁移边界：约定只约束新写内容与 owner 文档维护；既有 dated records、已完成规格、历史记录不追溯重写；存量不合规形态记为已知差异随自然修订收敛（FR-006）。本句的清单化载体是 E6（检查器全量扫描输出），owner 文档只指针不承载清单。(FR-006, FR-016)
