# Data Model: 双语表述（Bilingual Expression）

**Spec**: `.specify/specs/078-bilingual-expression/` | **Date**: 2026-10-30 | **Source**: `requirements.md` § Key Entities（4 实体）+ plan 期派生（E5…E7）

实体的唯一 owner 以「承载位置」列为准；本文件只做投影，规则正文 MUST NOT 在此复述（One Source of Truth，宪法 XIV）。

## E1 双语表述约定（Bilingual Expression Convention）

- **承载位置**: `shared/guidelines/bilingual-expression.md`（[[STR-001]]，框架源；镜像 `.specify/shared/guidelines/bilingual-expression.md`）
- **属性**: 方向规则（zh→`中文(English)` / en→`English(中文)`）、唯一形态字面量（半角、紧贴）、覆盖定义面封闭集、豁免面封闭集、一致性规则、迁移边界
- **owner 声明**: 文件头部声明「本文件是双语表述约定的唯一 owner」，点名拥有的六组事实
- **状态机**: 成文（implement 落盘）→ 分发（镜像同步 + `specify init`）→ 维护（封闭集增删只能经本文件修订）
- **校验规则**: 头部前 40 非空行内有 `**Readers**` / `**Reading scenario**` 两行（reader-purpose 面）；四组枚举各为 Markdown 列表（供 SC-001 关键词表机械派生）；全文件无双语规则的第二个定义点

## E2 定义处（Definition Site）

- **承载位置**: owner 文档 § 定义处与可判定信号（信号清单的唯一登记处）
- **属性**: 所在文档主语言（zh/en）、可判定信号（S1…S4，封闭集）、所属覆盖定义面（E1 封闭集成员）
- **可判定信号（plan 预设计，owner 文档成文时落字）**:
  - S1 词汇表条目行：`.specify/memory/glossary.md` 中表体行（`| Canonical | …` 表内）
  - S2 覆盖定义面文档的章节标题行（概念/流程名在标题中被定义）
  - S3 加粗引导定义行：prose 中 `**<词条>**` 紧接 `（`/`(`/`—`/`:` 的行
  - S4 文档主语言声明行（owner 文档登记的每文档主语言判定信号；无声明时按正文 CJK/拉丁字母占比的保守缺省）
- **不可机械判定部分**: 「首次定义」的语义判断（A7）——不在检查器范围，由评审面承担
- **校验规则**: 信号清单封闭；新增信号只能经 owner 文档修订（FR-002）

## E3 术语条目（Glossary Entry）

- **承载位置**: `.specify/memory/glossary.md`（本仓运行时词汇表；协议 owner 为 `shared/workflow/glossary.md`）
- **属性**: Canonical（A5 双语形态 `中文(English)`）、Variants（收集中文侧易混写）、Origin/Status（协议字段）
- **与约定的关系**: FR-005 跨文档一致性的唯一判定基准；本特性 MUST NOT 改动词汇表引擎（`glossary-utils.py`）行为，只复用其读取模式
- **校验规则**: 新增/修订条目的 Canonical 采用双语形态（纯英文专名豁免，FR-004）；双语条目数是 dated record（M-7 = 132/161），引用时带 as-of

## E4 检查器（Checker）

- **承载位置**: `scripts/python/bilingual-expression-check.py`（框架源；镜像 `.specify/scripts/python/`；行为契约 `contracts/checker.md`）
- **属性**: 动作集（`scan` / `coverage` / `census`）、输入信号（派生自 E2 清单）、豁免扫描规则（跳过围栏代码块与行内代码）、输出形态（`file:line [code] message`）、退出码（0/1/2）、测量模式（`--scope changed` 与全量）
- **校验规则**: 只做 (a)(b)(c) 三类机械判定（FR-009）；MUST NOT 判语义；LLM MUST NOT 参与匹配计数；finding 码封闭四值（`full-width-parens` / `same-language-bracket` / `missing-bilingual` / `coverage-missing`）
- **边界**: 不绑定阶段门禁算子（FR-010，R-10）；不并入 `doc-consistency-check.py`（R-7）

## E5 ambient 小节（Ambient Section）

- **承载位置**: `templates/instructions-template.md` § `Bilingual Expression (双语表述)`（框架源；镜像 `.specify/templates/`；运行时 `.specify/instructions.md` 经 `generate-instructions.sh` 产出）
- **属性**: 一句话摘要 + owner 路径指针（[[STR-001]]）；形态遵循既有 ambient 小节惯例（对照 `## One Source Of Truth` 小节）
- **校验规则**: MUST NOT 复述方向/形态/覆盖面/豁免的枚举（FR-008）；MUST NOT 出现本仓专属路径或提交号（FR-012）；无阻断式确认句（R-4）

## E6 存量差异清单（Legacy Divergence List）

- **承载位置**: 派生记录——检查器全量扫描输出，按执行日期落 `test-evidence/`（dated record，永不重写）
- **属性**: 扫描日期、违规 `file:line [code]` 全量输出、基线语义（FR-016：清单化但不批量改写）
- **校验规则**: append-only（并发开发安全：一文一件，按日期命名）；只读作迁移输入，不作门禁失败依据

## E7 关键词基线快照（Keyword Baseline Snapshot）

- **承载位置**: `test-evidence/` 交付日快照（SC-001 的基线语义：「交付当日的实测快照」）
- **属性**: 关键词表（机械派生自 E1 四组枚举的列表项字面量）、检索范围（`shared/`、`templates/`、`.specify/` 排除 specs/history）、逐关键词命中位置清单
- **校验规则**: 快照冻结于交付日；SC-001 判定时 owner 文档之外命中数 = 0（contracts/measurement.md 定豁免行形态：含 owner 路径指针的行不计为复制位置）

## 关系汇总

- E1 owns：方向/形态/覆盖面/豁免/一致性/迁移六组事实。
- E2 ∈ E1 覆盖面（封闭集成员的定义行由 E2 信号识别）。
- E3 是 E1 一致性规则（FR-005）的判定基准；E4 的 `census` 动作消费 E3。
- E5 引用 E1（摘要 + 指针）；E6 / E7 是 E4 / E1 的派生记录（dated，不回流改判据）。
