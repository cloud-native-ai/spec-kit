# Decision Tension Record（决策反题与反指标契约）

**本文件是该纪律的唯一真源（single source of truth）**：本文件拥有六字段记录形态（含记录标识
`tension_id`）、可采纳判据、拒绝形态、承重决策门槛、与相邻 owner 的边界、以及记录标识形态。
计划模板、分析检测通道、ADR 模板与契约测试四个消费者 MUST 以路径引用本文件，MUST NOT 复述
其判据表、拒绝清单或门槛表——复述即第二定义点，会各自漂移。

**本纪律防的失效是「没有反题的决策」**：一条承重决策只在工件上留下「我们选了 A」，最强反题、
双方不可让渡的约束、能判定哪一极更对的观测、选择要付出的代价与重开条件都不在工件上，于是
事后无法判断这次取舍是否成立，也无法在指标恶化时找到重开点。

## 记录形态：六字段 + 记录标识（封闭集）

一条记录由封闭的六字段与一个记录标识构成，字段名逐字如下：

| 字段 | 内容 |
|------|------|
| `decision` | 一句话点名被选中的一极 |
| `antithesis` | 可独立采纳的具名反题方案，附「在什么条件下它更优」 |
| `binding_constraints` | 双极约束，含 `pole_a` 与 `pole_b` 两个极点 |
| `discriminating_evidence` | 一位复核者可执行、结果二值的观测或实验 |
| `expected_sacrifice` | 预期代价，绑定一条已声明的测量来源 |
| `revision_trigger` | 重开条件：指标恶化到什么程度 / 出现什么证据 → 重开动作 |

记录标识 `tension_id` 取 `T-NNN` 形态（三位十进制数字），在同一份计划内唯一，并按出现顺序
递增（`T-001`、`T-002` …，不得跳号）。字段集合封闭：新增、改名或删除字段 MUST 走本文件修订，
MUST NOT 在消费点就地扩展。记录以三级子节承载，子节标题以 `T-NNN` 起头，正文不再重复声明
标识——一个标识只有一个定义点。

## 可采纳判据（封闭集，四条全满足）

1. `decision` 用一句话点名被选中的一极，不同时陈述两极为可选；
2. `antithesis` 是一个可被独立采纳的具名方案，不是被选方案的弱化版、也不是「什么都不做」，
   并给出至少一条「在什么条件下它更优」的陈述——只有「但它更差」的陈述判为稻草人；
3. 两个极点约束均非空，且被选方案不同时满足两极——能同时满足时该张力不成立，MUST 改写为
   双赢解或降级为普通取舍，MUST NOT 保留为记录；
4. `discriminating_evidence` 是一位复核者可执行、结果二值的观测或实验。

四条构成封闭集，与关系：任一不满足即不可采纳。

## 拒绝形态（封闭清单，命中即拒）与判定者分工

- `expected_sacrifice: none`——放弃取舍本身即拒；值留空按同一条判；
- 任一极点为空（`pole_a` / `pole_b` 行缺失或留空）；
- `discriminating_evidence` 不可执行，或结果非二值；
- `antithesis` 为稻草人（「什么都不做」、被选方案的弱化版、只有「但它更差」的陈述）；
- 正文以「要平衡」「综合考虑」「视情况而定」一类不可判定措辞代替取舍。

清单条目新增 MUST 走本文件修订。**判定者分工**：机械可判的三项——字面 `none` 或空代价、
空极点、命中不可判定措辞清单——由确定性校验器判定；语义两项——稻草人反题、证据不可执行或
结果非二值——由两位复核者按同一条判据判定，两人 MUST 得到同一 verdict，分歧即判据待修订，
不能两人各自成立。

## 承重门槛（四类触发）与复杂度门控

四类触发任一成立即承重：不可逆（回滚需要迁移或重建）、跨团队（改变他人依赖的契约或接口）、
高爆炸半径（故障影响面超出本特性边界）、与宪法原则相关（触及任一 MUST 条）。不满足任一触发的
决策 MUST NOT 被要求填写记录；缺失记录 MUST NOT 被判为缺陷。

复杂度门控引用 `shared/guidelines/task-complexity-rubric.md` 的分级：Trivial 级任务按定义不含
承重决策，因此 MUST NOT 触发记录。当复杂度分级与承重判据冲突时，MUST 按该 rubric 的 tie-break
规则取较高一级，并以承重判据为准判定是否需要记录。

## 与相邻 owner 的边界

- `shared/definitions/derivation-definitions.md` § Contradiction Handling 管两个来源冲突时不取平均；
- `/speckit.clarify` 与访谈账本管需求阶段的分歧与翻供；
- `shared/guidelines/fast-fail.md` 管执行中的异常纠正与裁定；
- `shared/guidelines/critique-and-self-critique.md` 管改进提案的证伪。

本纪律只承接「方向已选定之后的技术取舍」，MUST NOT 承接需求分歧；四条边界的规则正文归各
owner，本文件不复述。

## 消费者与引用方式

| 消费者 | 引用方式 |
|--------|----------|
| `templates/plan-template.md` | 一条指针加字段名清单，不复述判据表 |
| `skills/internal/analyze-artifacts/references/detection-and-severity.md` | 消费校验器 verdict，按本文件判据分类 |
| `scripts/python/validate-decision-tensions.py` | 实现机械可判的三项拒绝形态与记录形态检查 |
| `docs/decisions/template.md` | 以 `tension_id` 指回记录，不复制字段内容 |
| `tests/contract/test_decision_tension_contract.py` | 断言本文件存在、封闭、且以路径引用相邻 owner |

本文件 MUST NOT 引入持久化载体、台账、调度器、评分器或运行时；记录搭在计划工件上，判定结果
只进既有 analyze 报告与计划文本。
