# Contract: 纪律文档与 ambient 引用(discipline-doc)

**Consumers**: contract tests(tests/contract/)、/speckit.implement、创作/改进技能

## C-D1 文件存在性与镜像

- `shared/guidelines/token-efficiency.md` MUST 存在(canonical)。
- `.specify/shared/guidelines/token-efficiency.md` MUST 与 canonical 字节一致(经 `sync-mirrors.py`)。

## C-D2 必备节

文档 MUST 含以下六个节(标题字面量,层级 `##`):

1. `## 程序优先(Program-First)`
2. `## 摘要优先(Summary-First)`
3. `## 升级阶梯(Escalation Ladder)`
4. `## 小文件阈值`
5. `## 判定边界`
6. `## 消耗观察(Consumption Observation)`

## C-D3 规范性内容钉扎

- 程序优先节 MUST 含固定规则判断类型清单(模式匹配、结构校验、计数、去重、排序、比对)与 MUST/MUST NOT 措辞。
- 摘要优先节 MUST 逐字对齐 FR-003 的三个例外情形 (a)(b)(c)。
- 小文件阈值节 MUST 含默认值 `≤ 100 行` 且 `≤ 10 KB`(双条件),并声明"唯一定义点,他处仅引用"。
- 消耗观察节 MUST 含字面量 `token-efficiency`([[STR-001]])的标记约定与"不编造 Token 数值"规则。
- 文档 MUST NOT 复制 Tool 复用门 / feedback-step 的定义,只互引路径。

## C-D4 Ambient 引用

- `templates/instructions-template.md` MUST 含指向 `token-efficiency.md` 的引用(新增节或既有节内条目),且与 `.specify/templates/instructions-template.md` 字节一致。
- 引用处 MUST NOT 内联复制纪律规则全文(单一事实源约束)。

## C-D5 引用不复制(全局)

任何命令模板/技能/共享工作流引用纪律时 MUST 以路径引用;grep `shared/` 与 `templates/` 面,纪律六节标题在 token-efficiency.md 之外的出现次数 MUST 为 0(允许引用路径字符串本身)。
