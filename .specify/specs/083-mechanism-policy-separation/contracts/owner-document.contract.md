# Contract — 原则 owner 文档形态（Owner Document Schema）

**Status**: designed（本阶段）；由 `/speckit.implement` 落地
**产物**: `shared/definitions/mechanism-policy-definitions.md`（框架源）→ 镜像 `.specify/shared/definitions/mechanism-policy-definitions.md`
**条款** — 可追溯性表在文末；每条条款只指向 `requirements.md` 的 FR / SC，不复述其正文。

## OD-01 — 头部所有权声明（Owner declaration）

- 文档前 12 行 MUST 含字面 `single source of truth`（本仓既有 owner 文档的统一形态：`shared/definitions/derivation-definitions.md`、`shared/guidelines/one-source-of-truth.md` 同款）。
- 前 12 行 MUST 逐项点名本文拥有的**事实组**，且每组 MUST 在正文有一个落点章节：① 两层的定义与判别口径；② 双层边界测试与两侧成员；③ 误置的两类症状；④ 归档规则；⑤ 消费侧提示形态；⑥ 元层成员表与谓词；⑦ 与相邻 owner 的边界。
- 前 12 行 MUST 含字面 `MUST NOT` 并说明「消费方以路径引用，MUST NOT 复制本文的判据、症状表、提示形态与成员表」（FR-015）。
- 文档 MUST 声明**自己不拥有**什么，并逐条给出 owner 路径：目录能否存在 → `shared/guidelines/directory-governance.md`；「机制 vs 问题」的修复方向 → `shared/definitions/dogfooding-definitions.md` § 1；`${SKILL_HOME}` / `${SKILL_WORKDIR}` 的取值来源 → `skills/external/create-skills/SKILL.md` § 2；运行期根 → `shared/guidelines/directory-governance.md` § 5。这是 C2 的机械形态：**两处共享「机制」一词、事实不同**，本文不重述对方定义。

## OD-02 — § Terminology：两层的定义与双向判据

- 两个 canonical 词 MUST 逐字为 `机制 (Mechanism)` 与 `策略 (Policy)`（双语形态逐字，见 `shared/guidelines/bilingual-expression.md` § 方向规则；本文主语言为中文）。
- 两层的判别口径 MUST 以**一个问题**表达：*换掉运行环境，这段文字要不要改？* 不改 → 机制；要改 → 策略。判据 MUST 写成二值，MUST NOT 引入严重度或「视情况」中间层。
- MUST 给出两个**可观测方向**（requirements § Terminology）：去向改变而读者答不出运行环境 → 机制；答得出运行环境 → 策略。
- 判据 MUST 明写它**不参与判定**的因素：文件名、目录名、内容语言、篇幅、介质（Markdown / 脚本 / 模板）。
- 表格形态固定为 `| 内容示例 | 判别 | 一句话依据 |`，示例行 MUST 至少覆盖 requirements § Key Entities 的四个实体类（机制侧内容、策略侧内容、误置、元层成员表）各至少一行。

## OD-03 — § Boundary Test：双向边界测试与两侧成员

- MUST 给出「两侧成员表」两张（机制侧 / 策略侧），每张表是**派生结果**：每一行 MUST 由一个 OD-02 的判据实例得出，MUST NOT 是手工枚举后无依据的清单（FR-002(a)）。
- 机制侧成员 MUST 至少覆盖：判定规则、算法、步骤顺序、可复用方法、技能定义本体、`references/`、`scripts/` 的逻辑、`assets/` 中随技能分发的模板。
- 策略侧成员 MUST 至少覆盖：用户指定目录、当前工作目录、`.specify/` 下运行期路径、输入来源、输出落点与形态、运行模式绑定；路径取值来源 MUST 以 `${SKILL_HOME}` / `${SKILL_WORKDIR}` **引用** （C3 指针，不复制定义）。
- MUST 给出 A4 的裁决：脚本的**逻辑**属机制、**参数与落点**属策略，并说明「二者不一致时按内容判、不按文件名判」（FR-003）。
- MUST 说明两层**不必在同一文件内分开、但在语义上必须可分开**（FR-003），并给出「同一段落同时含两层」的拆法：逐句过判据，拆不开时两个方向各判一次，冲突记为待澄清（requirements § Edge Cases 第一条的同一条规则——本文件是它的落点，requirements 只写规则）。

## OD-04 — § Misplacement Symptoms：误置的两类症状

- 两张症状表，各 MUST 至少两条可观测表现，形态固定为 `| 症状 | 可观测表现 | 改正方向 |`（FR-002(b)）。
- 机制误置（可复用逻辑住在运行环境侧）MUST 覆盖至少：某用户目录的运行说明里出现判定规则/步骤顺序；`.specify/` 下的笔记文件里出现算法分支。
- 策略误置（运行环境绑定被固化进机制侧）MUST 覆盖至少：技能正文出现绝对路径或用户目录名；`references/` 里出现「默认输出到 `<某个具体目录>`」。
- 每条「改正方向」MUST 指向**另一侧的具体落点类别**（技能资产 / 运行环境），MUST NOT 只写「应该改」。

## OD-05 — § Archival Rules：归档规则与目录治理的关系

- 规则 MUST 以两层各一条陈述：机制 → 技能资产（`SKILL_HOME` 侧，含 `references/`、`scripts/`、`assets/`）；策略 → 运行环境（`SKILL_WORKDIR` 侧 / 用户指定目录 / 当前工作目录 / `.specify/` 侧）。
- 本文 MUST 明写：**目录能否存在、叫什么、在哪登记**归 `shared/guidelines/directory-governance.md`，本文只回答「内容住哪一层」；关系是**引用而非复制**（FR-004）。判据是：本文 MUST NOT 出现目录命名正则、注册义务句或运行期根清单。
- 本文 MUST NOT 新增环境变量、配置键、目录根（A3 / FR-016）。
- MUST 给出 Edge Case 的落地裁决：写状态到 `.specify/state/` —— 动作规则属机制、落根属策略、根由 `directory-governance.md` § 5 拥有；本文 MUST NOT 作为第二个根的声明处。

## OD-06 — § Consumption Contract：策略缺失 / 含糊的统一提示形态

- 提示形态 MUST 是**一个固定形状**，三要件齐全（FR-006）：① 缺的是哪一个策略项（以用户可识别的名字点名，不用内部变量名）；② 为什么此刻需要它（下一步要做什么副作用）；③ 用户可以照做的提供方式（至少一条具体形式）。
- 形态 MUST 给出可复制的骨架（标题行 + 三行字段 + 一个示例），示例 MUST 标出它落在「写入侧」还是「读取侧」。
- MUST 区分两种判定（FR-007），且后续动作可区分：**策略缺失**（没说要哪一份）→ 停下并索取，不产生产物；**环境错误**（给了但取不到）→ 停下并报出取不到的那个值、以及可执行的恢复路径；两者 MUST NOT 合并成一条措辞。
- MUST 声明检查发生在**任何副作用之前**（写文件、建目录、删改），停止后不留半成品（FR-008）。
- MUST 明写两条禁止：不得以「机制默认值」顶替缺失的策略；不得静默挑默认落点（含当前工作目录）（FR-005）。
- MUST 覆盖 standalone 形态（无 `.specify/` 时候选集合收窄，提示形态不变；requirements § Edge Cases 第 4 条）。

## OD-07 — § Meta-layer Membership：谓词与封闭成员表

- 谓词 MUST 逐字为 requirements § Constraints C1 的谓词；本文 MUST 声明它是判定的**唯一依据**（FR-010）。
- 成员表 MUST 是封闭的，三行一组固定形态：`| 流程 | 产出 | 裁定 | 理由/接线位置 |`；裁定值域 MUST 封闭为 `included` / `excluded`（+ 命令面单列，见下）。
- `included` MUST 恰为 `create-skills`、`improve-skills`、`merge-skills`（C1 已裁定，本文不复判）。
- `excluded` MUST 恰为 `coaching-skills`、`run-skills`，每行理由 MUST 命中同一谓词（产出是观察与计划 / 产出是目标技能按其自身流程执行），且 MUST 给出「真实改写仍经 improve-skills 覆盖」的通道说明（FR-014）。
- `/speckit.skills` MUST 单列一行，标为**命令面**：转发给 `included` 成员，只声明接线位置，不新增第二套判定（FR-011 / C1）。
- 本文 MUST 声明谓词变化的后果：谓词一改，全表重算并在计划中记录，MUST NOT 只改一行（C1 末句）。

## OD-08 — § Boundaries：与相邻 owner 的边界

- 一表，形态 `| 相邻 owner | 它拥有的事实 | 本文的回答 |`，行集 MUST 至少为：`dogfooding-definitions.md` § 1（机制 vs 问题）、`directory-governance.md`（§ 2 目录图、§ 5 运行期根）、`create-skills` § 2（`${SKILL_HOME}` / `${SKILL_WORKDIR}` 定义）、`one-source-of-truth.md`（引用纪律本身）、`bilingual-expression.md`（双语形态）、`temp-directory-discipline.md`（临时根）。
- 某行的事实 MUST NOT 在本文被复述：断言是「本文不含该 owner 的规则字面」（具体字面由契约测试 `test_mechanism_policy_ownership.py` 枚举）。

## OD-09 — § Worked Examples：附录样例题（SC-001 / SC-005 的分母）

- MUST 给出一个**封闭**的样例题集：至少 12 条待判定内容，覆盖两类内容、两类误置与边界情形（脚本参数、模板标题、`.specify/` 笔记、双语句子各至少一条）。
- 每条 MUST 含：内容片段（1–3 行）、标准答案（机制 / 策略 / 待澄清）、一句话依据（只能引 OD-02 的判据，MUST NOT 引入新规则）。
- 题集 MUST 足以让两位独立判定者**仅凭本文**作答（SC-001），因此题集不得引用本文之外的任何文件作为答句依据。
- 题集 MUST 标注「SC-001 / SC-005 的唯一分母来源」，其他位置 MUST NOT 再列举一份（FR-016）。

## OD-10 — § Change Log：变更记录

- 一条 `| 日期 | 变更 | 依据 |` 表；首行 MUST 为本特性落地的日期与 `requirements.md` FR 编号。本文的修订 MUST 在此留一行，MUST NOT 只在提交信息里说明。

## 代码式不变量的边界声明

本文是作者态文档，**不**规定任何机器面 schema（无 YAML 键、无 JSON、无脚本参数）；`data-model.md` 对它做的是形态投影，MUST NOT 扩大本契约的值域。

## 可追溯性

| FR | 条款 | 测试载体 |
|---|---|---|
| FR-001 | OD-01, OD-07 | `tests/contract/test_mechanism_policy_owner_doc.py` |
| FR-002 | OD-02, OD-03, OD-04 | 同上 |
| FR-003 | OD-03 | 同上 |
| FR-004 | OD-05 | `tests/contract/test_mechanism_policy_ownership.py` |
| FR-005 | OD-06 | `tests/contract/test_mechanism_policy_owner_doc.py` |
| FR-006 | OD-06 | 同上 |
| FR-007 | OD-06 | 同上 |
| FR-008 | `contracts/skill-wiring.contract.md` SW-04 + OD-06 | `tests/contract/test_mechanism_policy_skill_wiring.py` |
| FR-009 | OD-07 + `skill-wiring.contract.md` | `tests/contract/test_mechanism_policy_skill_wiring.py` |
| FR-010 | OD-07 | `tests/contract/test_mechanism_policy_owner_doc.py` |
| FR-014 | OD-07 | 同上 |
| FR-015 | OD-01, OD-08 | `tests/contract/test_mechanism_policy_ownership.py` |
| FR-016 | OD-05, OD-09 | 同上 |
| FR-018 | OD-02 | `tests/contract/test_mechanism_policy_owner_doc.py` |
| SC-001 | OD-09 | test-evidence 双判定记录 |
| SC-005 | OD-09 | test-evidence 读者作答记录 |
