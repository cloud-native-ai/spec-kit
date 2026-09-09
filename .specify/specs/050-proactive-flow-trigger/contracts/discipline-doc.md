# Contract: 触发纪律文档 (discipline-doc)

**Requirement**: `050-proactive-flow-trigger` → Feature 050
**Surfaces under contract**: `shared/guidelines/proactive-trigger.md` · `.specify/shared/guidelines/proactive-trigger.md`(镜像)
**Test file**: `tests/contract/test_proactive_trigger_discipline_doc.py`(**一份契约一个测试文件** — 与 `trigger-section.md` 分文件,以免两个特性的任务在同一文件上串行化、失去 `[P]` 并行资格)
**Clauses**: C-1 … C-16(C-1…C-7 为结构属性;C-8…C-16 由 analyze 2026-09-08 从原无编号的「各章节必须承载的规范内容」表提升而来,使 FR-005…FR-019 的义务在本契约内可被机械断言)
**定位**: 本文件是主动触发纪律的**单一真源**;指令模板章节只承载摘要 + 指针(房式先例:`shared/guidelines/task-complexity-rubric.md` ↔ 模板 `## Task Complexity Rubric`;`shared/guidelines/token-efficiency.md` ↔ 模板 `## Token Efficiency Discipline`)

---

| ID | Clause | Assertion |
|----|--------|-----------|
| **C-1** | 双表面 + 字节相同 | `shared/guidelines/proactive-trigger.md` 存在;`.specify/shared/guidelines/proactive-trigger.md` 与其**字节相同**(sync-mirrors shared 对,lenient) |
| **C-2** | 章节集封闭且齐备 | 文档的 `## ` 标题集**恰为**以下 10 项(顺序如列):`Ownership`、`Evaluation Cadence`、`Evidence Budget & Escalation`、`Suggestion Shape`、`Ordering Contract`、`Promotion & Safety Boundary`、`Telemetry & Retention`、`Tuning Protocol`、`Global Switch`、`Maintenance Duties`。缺项或多项即违约 |
| **C-3** | **零 BLOCKING_PATTERNS 命中** | 对文档全文运行 `scan-confirmation-gates.py` 的 `BLOCKING_RE`,命中数 == 0。`shared/` 在 `SCAN_DIRS` 内,且本文件路径**不匹配**任何 `GOVERNANCE_PATH_PATTERNS`,故不享受 governance_kept 豁免 —— 任一命中都会把扫描 total 推过 23.25 的上限(plan.md D-4) |
| **C-4** | 引用不复述 | 文档 MUST NOT 复述 `shared/guidelines/confirmation-gates.md` 的两级分类表或破坏性清单(只以路径引用);MUST NOT 复述 `templates/proactive-trigger-seed.json` 的规则表或命名情境表的完整映射(情境数以 `data-model.md` §受控词表为权威,本条款不复述数字)(只以路径引用,并说明词表与种子文件的归属);MUST NOT 复述 `trigger-utils.py` 的信封键集(只列 action 名与用途一行,细节指向引擎 `--help` 与 `contracts/trigger-engine.md`) |
| **C-5** | 拥有升级判据并声明归属 | `## Evidence Budget & Escalation` 章节 MUST 完整给出 P1–P5 升级判据表(条件 → 探测内容),并在 `## Ownership` 章节声明本文件为"评估节奏 / 证据预算与升级判据 / 建议形态 / 顺序契约 / 遥测与保留 / 调优协议 / 全局开关"的**owner**。`.specify/specs/050-*/data-model.md` 中的同表是**设计期记录**(dated record,不随包分发、不作为当前现实被引用),属 `one-source-of-truth.md` 许可的第三类合法副本,不构成漂移 |
| **C-6** | 项目中性 | 文档 MUST NOT 出现任一禁用 token:`spec-kit`、`specify-cli`、`specify_cli`、`Feature 0`、`cloud-native-ai`、`.specify/specs/0`、`requirement 0`。`shared/` 随 init 整体拷贝到每个下游项目,故 shipped surface 必须中性(承 Feature 049 的 shipped-surface 中性纪律) |
| **C-7** | 发现路径不依赖既有章节内部改动 | 文档的可达性 MUST 由**新 `## ` 章节内的指针**提供,MUST NOT 依赖在 Documentation Map 表格内新增一行 —— additive reconcile 只按 `## ` 整行集合差传播,**既有章节内部的改动不会抵达已初始化项目**(plan.md D-1 推论)。允许同时为全新 init 增加 Documentation Map 行,但该行 MUST NOT 是唯一发现路径 |

---

## 各章节必须承载的规范内容(编号条款 —— analyze 2026-09-08 由无编号表提升,使 FR 义务可被机械断言)

> 提升理由:此前这些内容以无编号表承载,而 `feature-ref.md` 把 FR-005a/005b/006/007/008/009/009a/010–012/015–018 全部映射到本契约的 C-1…C-7 —— 而那七条断言的是**结构属性**(双表面、章节集、文案安全、引用不复述、归属声明、中性、发现路径),不是这些义务本身;T004 也只断言章节集与顺序。结果是十余条 FR 名义上有覆盖、实际无钉桩。以下 C-8…C-16 逐节把义务变成条款,断言方式为"该 `## ` 章节正文 MUST 含下列规范陈述(以关键短语存在性 + 规范化语义双判据)"。

| ID | 章节 | Clause(必须规定,且可机械断言) | 覆盖的 FR |
|----|---|---|---|
| **C-8** | `Evaluation Cadence` | 章节 MUST 同时含:① 每个用户回合都评估的陈述;② 评估**静默**——无适用流程或状态未变时零用户可见输出;③ 明示"**评估节奏 ≠ 建议节奏**"(每回合评估不等于每回合建议)。三者缺一即违约 | FR-005a |
| **C-9** | `Evidence Budget & Escalation` | 章节 MUST 含:① 默认只用已在上下文中的信息;② **完整的 P1–P5 升级判据表**(五行齐备,每行含条件与探测内容);③ 探测只做存在性/计数/集合差、MUST NOT 读制品全文;④ 升级率上限(默认 20%)与其口径(分母为 `assess` 调用数,见 `data-model.md` V4.5) | FR-005 |
| **C-10** | `Suggestion Shape` | 章节 MUST 含:① 一行非阻塞提示 = 用途说明 + 引擎给出的确切调用形式;② 建议输出频次有界,且**边界由会话级重复抑制机制定义**(同会话同情境同规则不重复产出,见 `trigger-engine.md` C-20),不只是"不要刷屏"的劝告;③ 多规则命中收敛为一条最高优先;④ 无适用流程时如实不建议、MUST NOT 凑数 | FR-006 / FR-007 / FR-008 |
| **C-11** | `Ordering Contract` | 章节 MUST 含:① 合规检查先行、流程选取在**同一趟**接续;② 建议 MUST NOT 早于合规检查产出;③ MUST NOT 把 plan 期的逐原则枚举门控搬到每回合(并点名 `plan-template.md` 的 Constitution Check 属 plan 期);④ **调用引擎评估时 MUST 显式声明合规检查已完成**(即传 `--compliance-done`;该 flag 缺省为 false,缺省即如实报 `ordering-violation`)—— ④ 是 ①② 可被度量的前提,缺它则 SC-012 只能读到常量(补 analyze N-15:此前无任何条款要求 agent 传该 flag,而 `trigger-section.md` C-5 禁止指令章节出现 `--<flag>` 字面量,故该义务**只能**由本纪律文档承载) | FR-005b |
| **C-12** | `Promotion & Safety Boundary` | 章节 MUST 含:① 连续采纳达阈值(默认 3)晋升、一次拒绝即重置;② **破坏性/不可逆流程永不晋升**,判据以路径引用 `shared/guidelines/confirmation-gates.md`(MUST NOT 复述其分类表,见 C-4)、存疑从严;③ **自动执行仍出三段式执行报告**(以路径引用该判据文档,不复述三要素);④ **自动执行 MUST NOT 抢占用户当前请求**——情境命中但用户正在执行其他任务时 MUST 让位或延后(引擎侧的结构保证见 `trigger-engine.md` C-21:引擎从不自行执行流程,本项约束的是 agent 的执行时机);⑤ 用户可复位单条或全局降级 | FR-010 / FR-011 / FR-012 / **FR-019** |
| **C-13** | `Telemetry & Retention` | 章节 MUST 含:① 每回合遥测行的字段与用途(SC-011 / SC-012 的分母);② 保留窗口默认值与**追加即截断**的恒真不变量(见 `data-model.md` V4.3);③ 晋升计数是规则上的聚合态、轮转或截断不清空学习结果;④ **诚实声明度量边界**:遥测无法证明"agent 跳过了某回合的评估"(V4.5) | FR-009 / FR-009a |
| **C-14** | `Tuning Protocol` | 章节 MUST 含:① 四类证据口径(命中率 / 拒绝率 / **误报** / 漏报);② 小样本守卫(默认 `hits < 5` 不提议)且被跳过者具名回显;③ 提议以候选形态呈现、**用户批准后才写入**(措辞须避开 C-3 的禁用字面量);④ 批准与证据、痕迹的可回查关联(SM-2 的 `proposed → ratified → applied` 两段转移与双时间戳) | FR-015 / FR-016 / FR-017 |
| **C-15** | `Global Switch` | 章节 MUST 含:① `config.enabled=false` 的语义(不产出建议、不自动执行);② 用户显式关闭优先于框架默认;③ 关闭状态 MUST NOT 被指令再生覆盖(状态与指令文件分离);④ 由 false 转 true 时清空会话抑制态(见 `trigger-engine.md` C-20 / `data-model.md` V6.8) | FR-018 |
| **C-16** | `Maintenance Duties` | 章节 MUST 含三项义务:① 改写任一命令模板的 `## Handoffs`(或 `owning-section` 类来源段落)后 MUST 同步种子文件,否则漂移检出契约失败,且**修复方式是同步而非放宽测试**;② 情境词表扩展只经用户批准通道,MUST NOT 临场造词;③ 新增 action、flag 或错误码 MUST 同批修订 `contracts/trigger-engine.md` 的 C-9 / C-10 / C-22 封闭集 | 跨 FR 的维护义务 |

## 文案安全清单(实现期硬性,由 C-3 机械断言)

禁用的字面量全集见 `scripts/python/scan-confirmation-gates.py` 的 `BLOCKING_PATTERNS`(L46–64)。本特性最易误犯的五处及其替代表述:

| 想表达 | 禁用写法 | 合规写法 |
|---|---|---|
| 调优需用户批准 | `等待用户确认` / `显式用户确认` / `confirm before` / `after confirmation` | 「以候选形态呈现,用户批准后写入规则集」/「未经用户批准 MUST NOT 变更规则集」 |
| 破坏性流程需前置确认 | `确认后才执行` / `stop and confirm` | 以路径引用 `shared/guidelines/confirmation-gates.md`,不复述其措辞 |
| 提到治理域名 | `confirmation gate` / `确认门禁` / `确认门控` | 用路径形式 `confirmation-gates.md`(连字符不匹配空格形态) |
| 建议的交互形态 | `Proceed … yes/no` / `interactive confirmation` | 「用户可采纳,也可忽略;忽略不影响其当前请求」 |
| 晋升后的执行 | `Execute on Confirmation` / `确认并落盘` | 「晋升后的规则在情境命中时直接执行,并出具执行报告」 |

## 交付顺序约束

C-1 的镜像由 `sync-mirrors.py --write` 落地,故顺序 MUST 为:写 `shared/guidelines/proactive-trigger.md` → `sync-mirrors.py --write` → 跑 C-1…C-7 → 再写模板章节(其指针指向本文件,`trigger-section.md` C-1 断言该指针存在)。验证步骤 MUST 跑 **C-1…C-16 全部条款**(C-8…C-16 是 analyze 2026-09-08 由无编号内容表提升而来的义务条款,`tasks.md` T004 已同步扩到该范围)。
