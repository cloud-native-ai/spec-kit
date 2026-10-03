# Data Model: 机器可判定的制品命题(Machine-Decidable Artifact Propositions)

**Requirement**: `053-machine-decidable-artifacts` → Feature 053  
**Date**: 2026-10-02  
**Source**: 实体集取自 `requirements.md` § Key Entities(8 个),按 US1…US5 的判定面补齐字段与校验规则。派生实体(检查项标签、verdict、基线)在 § 派生实体 单列,因为它们在规格里以属性形式出现、在实现里各自是独立的机器可判对象。

**持久化边界**:本特性**不引入任何新的持久化存据**。全部实体都是对既有制品(Markdown / YAML 文本)的一次只读解析结果,生命周期止于一次调用的 stdout 与退出码(A-3 零写入)。唯一的**新增落盘物**是 FR-027 裁定产生的冻结基线文件(§ 派生实体 E-3),它是文本、由 `--names-out` 同形态的有序名字集构成,不是数据库。

---

## E-1 检查器 (Checker)

一个单一入口的可执行判定者。

| 字段 | 类型 | 约束 | 来源 |
|---|---|---|---|
| `entry` | 路径 | 单一入口可执行脚本,以被校验制品路径为参数 | FR-001 |
| `artifact_class` | 枚举 | 被校验制品类别(`requirements.md` / `tasks.md` / `contracts/*` / goal 定义) | Key Entities |
| `check_labels` | 字符串集 | 逐项检查的标签集;**唯一真源是模块 docstring 的枚举段**,不是运行输出 | D-5、FR-042 |
| `exit_table` | 映射 | 退出码 → 含义;新检查器沿用 `0/1/2` 三档 | D-6、FR-033 |
| `readonly` | 布尔 | 恒为 `true`;判定只经 stdout 与退出码表达 | FR-005、A-3 |
| `attribution` | 字符串 | docstring 首句按 STR-008 形态点名 Program-First 规则 owner | FR-002 |
| `json_keys` | 字符串集 | 机读输出键集;新增检查器 MUST 含逐项 verdict 数组 | FR-003 |
| `pinned_by` | 路径集 | 钉住其标签集与退出码表的契约测试 | FR-046 |
| `mirror_pair` | 路径对 | 源 ↔ `.specify/` 运行时镜像 | FR-047、D-17 |

**校验规则**

- **V-1**:`check_labels` MUST 由 docstring 的枚举段机械抽取,抽取式为 `^  ([A-Za-z][A-Za-z-]*)\s{2,}`(两空格缩进 + 标签 + ≥2 空格)。偏离该缩进/间隔会让抽取漏项,而漏项表现为「集合变小」——故钉子 MUST 同时钉住 docstring 体例(见 `contracts/checker-form.md`)。
- **V-2**:`readonly` 的取证 MUST 是一次写入点扫描(对脚本源 grep `write_text|mkdir|open(` 并逐点归属到某个写动作),MUST NOT 只凭 docstring 自陈。
- **V-3**:`exit_table` 的档位 MUST 与 `artifact_class` 相同的既有检查器一致;不一致即需在契约里显式声明理由。
- **V-4**:`json_keys` 的「逐项 verdict 数组」义务**只辖新增检查器**;既有 `validate-tasks.py` 的四键形态(`file`/`errors`/`warnings`/`status`)MUST NOT 因本特性被要求迁移(clarify 裁定 4)。

**关系**:被一个 `/speckit.*` 命令在其既有步骤调用(FR-048 的封闭两通道之一);被契约测试钉住;判定多个命题(E-2)。

---

## E-2 命题 (Proposition)

制品对自己或兄弟制品做出的一个结构性断言。

| 字段 | 类型 | 约束 |
|---|---|---|
| `text` | 字符串 | 命题文本(通常是一条 FR/SC 的可判定部分) |
| `judge` | (E-1, 标签) | 判定者 = 检查器 + 一个检查项标签 |
| `verdict` | 枚举 | 当前判定结果 |
| `evidence` | 路径/输出 | 逆样本或实跑输出 |

**校验规则**

- **V-5**:一个命题**恰有**一个判定者。两个判定者对同一命题给出不同 verdict 时,MUST 报冲突而不是静默择一——该唯一性在规格里只作为 Key Entity 的关系声明存在、无 FR 强制,故本模型把它升为校验规则并记入 `features/053.md` § Future Evolution(范围外的欠账 4)。
- **V-6**:一个检查器 MAY 判定多个命题;反之不成立。
- **V-7**:每个命题 MUST 有至少一个逆样本(E-6);缺逆样本的命题视为**未取证**,MUST NOT 报为已覆盖(FR-039、SC-011)。

---

## E-3 派生实体:检查项标签 / verdict / 冻结基线

### E-3a 检查项标签 (Check Label)

| 字段 | 约束 |
|---|---|
| `name` | 小写字母 + 连字符,匹配 `^[A-Za-z][A-Za-z-]*$` |
| `severity` | `ERROR` 或 `WARN`;WARN 永不影响退出码 |
| `owner_checker` | 恰一个 E-1 |

**本特性新增的标签集**(D-5):

- `validate-requirements.py`(新建,5 项):`id-contiguous`(FR-007)、`doc-order`(FR-008)、`ref-resolvable`(FR-009)、`marker-count`(FR-010)、`dup-id`(FR-011)
- `validate-tasks.py`(既有 6 项 + 新 4 项 = 10 项):新增 `green-dangling`(FR-016,**ERROR**)、`green-cross-phase`(FR-017,WARN)、`green-clause-collision`(FR-018(a),WARN)、`green-path-divergence`(FR-018(b),WARN)
- `account-clause-coverage.py`(新建):`clause-uncovered`(FR-024)、`fr-uncovered`(FR-026)、`clause-unparsable`(FR-023 的点名)、`coverage-baseline-delta`(FR-027)

**V-8**:`green-clause-collision` 与 `green-path-divergence` MUST **分列**,MUST NOT 合并为一个计数(FR-018、D-3)。二者的判据不同:前者是条款区间重叠,后者是测试路径共用且绿点不同;同一份 `tasks.md` 上可以各自独立触发。

### E-3b verdict

| 词表 | 取值 | 适用 |
|---|---|---|
| 检查器级 | `PASS` / `PASS (with warnings)` / `FAIL` / **新增第四值**(空或仅模板骨架) | E-1 的 `--json` `status` |
| `run-checks` 单项 | STR-006 的 7 个字面量 ∪ {STR-004 `not-evaluated`} | FR-032 |

**V-9**:`run-checks` 的 check `name`(五个:goal-binding / dangling / target-terminal / cross-goal / goal-terminal)与其 `verdict` 字面量是**两个词表**,MUST NOT 混用——实测无字面量名为 `goal-binding`,第①项的 verdict 是 `no-goal-definition`(D-11)。

**V-10**:`goal-utils.py` 另发第 8 个字面量 `rejected`(`:935`、`:968`),与五项检查无关,MUST NOT 因本特性删改(D-11、A-6)。

### E-3c 冻结基线 (Frozen Baseline)

| 字段 | 约束 |
|---|---|
| `kind` | 三组之一:测试失败名字集(SC-012)/ 门控 total(FR-045)/ 未覆盖项名字集(FR-027) |
| `path` | 落在本特性目录 |
| `form` | 每行一个名字、已排序(与 `run-tests.sh --names-out` 同构) |
| `frozen_at` | 实现开工时刻(唯一时机声明;MUST NOT 写成「首次全树**变绿**时」——变绿需要基线、基线需要先跑,循环定义,C-21) |
| `corpus` | 基线文件头部 MUST 记采集面选择器:排除本特性自己 spec 目录的 excl-`<ID>` 语料(声明处 = FR-027 § 基线面;此处只是把它写进产物头部,使两轮比对可核对同一基底) |
| `universe` | 冻结的名字集承载**哪几个全集**:基线按 `contracts/*` 条款名建键,故它天然只覆盖条款侧;FR 侧是否也要一份基线属**未裁定**项,已记为 `research.md` A-7(不是本实体的字段缺漏,而是需求侧尚未记录的决定) |

**V-11**:比对 MUST 按**名字集合**(`comm -13` 形态),MUST NOT 按计数(SC-010、SC-012、FR-027)。

**V-12**:覆盖基线 MUST 连同**当轮 owner 声明覆盖哪些形态**一起记录,否则「可解析文件数」在两个 owner 定义之间不可比(D-2、`notes/clause-form-census.md`)。

**V-13**:基线文件 MUST NOT 只存在于会话上下文;MUST 落盘本特性目录并可被 `comm` 直接消费。

---

## E-4 归属声明 (Green-Point Claim)

一行任务对「我负责让某条款转绿」的机器可解析陈述。目标是**契约文件 + 条款 id** 这一对;FR **不在**本实体的目标范围之内(FR-015、FR-016、FR-026)——FR 侧的「被认领子集」由 `clause_extract` 从条款块尾的 `(FR-nnn)` 反向引用得出,与任务行无关(E-5b、V-24)。

| 字段 | 类型 | 约束 |
|---|---|---|
| `contract_file` | 路径 | 相对仓根;MUST 存在,否则 `green-dangling`(ERROR) |
| `clause_id` | 字符串 | MUST 在该契约文件内可解析,否则 `green-dangling`(ERROR) |
| `task_id` | `T<NNN>[letter]` | 取自所在行 |
| `phase` | 字符串 | 取自最近的 `## Phase` 标题(`PHASE_HEADING`) |
| `order` | 整数 | 单调行序;跨阶段判定的比较量(D-8) |
| `test_paths` | 路径集 | 同行经路径分类后的**写入目标**集;`green-path-divergence` 的判据之一 |

**字面形态**:`[green: <contract>#<clause>]`(STR-001)。一行 MAY 声明零到多条(FR-015)。

**校验规则**

- **V-14**:归属声明 MUST 与既有行形态检查**正交**——一行只声明归属而不声明文件路径时,既有检查 MUST NOT 误报(FR-019)。
- **V-15**(承重,实证):归属声明内的契约路径 MUST NOT 被既有路径分类器当作**写入目标**。实测反例:两行 `[P]` 各写不同文件、但 `[green:]` 指向同一契约时,`parallel-safe` 报 `both WRITE ['contracts/x.md']`——假告警。故实现 MUST **先抽取归属声明、再对残余文本做路径分类**;MUST NOT 靠往 `POINTER_GOVERNOR`(一个刻意封闭的只读治理**词**表)里加标签前缀来解决(D-7)。
- **V-16**:出现在**围栏代码块内**的该形态 MUST NOT 被当作真实声明解析(FR-020)。
- **V-17**:`clause_id` 的解析 MUST 按 D-1 owner 文档声明的形态;对该文件不可解析的形态,报 `green-dangling` 而不是静默放行。
- **V-18**:归属声明面 MUST 项目中立,MUST NOT 含本仓专名(FR-021、FR-044)。

---

## E-5 条款 (Clause) 与 未覆盖集 (Uncovered Set)

### E-5a 条款

| 字段 | 约束 |
|---|---|
| `contract_file` | 所属契约文件 |
| `clause_id` | 条款 id;**位宽与形态均不统一**(实测 `C-1` / `C-01` / `C-001` / `C-3.4`) |
| `form` | 抽取形态,取值见下表 |
| `parsable` | 是否可被 owner 定义的语法解析 |
| `block_extent` | 条款正文边界:自标记行至**下一个标记行或下一个章节标题**先到者止,围栏块与行内代码跨度不计(FR-022、C-2;2026-10-03 由 `/speckit.analyze` F-20 定,实测三种读法给出 190 / 192 / 193 三个总数,唯此读法复现 `feature-ref.md` 已印的 192/166/16) |
| `cites_frs` | 该块**引用组**里的 FR id 集合(C-2 的三条规则:块边界 = 标记或标题先到;引用组 = 块内最后一个含 FR/SC id 的括号,容忍一层嵌套、`FR-a…FR-b` 区间展开;组外同形字样按「提及」处理,FR-009)—— **FR 侧被认领子集的唯一来源**,与 E-4 无关(FR-026、C-18) |

**形态集与其判据**(逐形态的**计数**由 `notes/clause-form-census.md` 唯一拥有,本表不复写——该量随本特性自己的契约落盘而变):

| `form` | 判据 |
|---|---|
| `md-bold-closed` | `\*\*C-\d+(?:\.\d+)*\*\*` |
| `md-bold-paren` | `\*\*C-\d+` 命中而闭合形不命中 |
| `md-heading` | `^#{1,6}\s+C-\d+` |
| `yaml-openapi` | `openapi:` 且 `paths:`;条款 = `paths:` 下的 HTTP 方法键 |
| `yaml-assertions` | `^\s+- id:` |
| `md-none` | 以上 `.md` 判据全不命中 |

**V-19**:四种 `.md` 形态互斥(实测同现文件数为 **0**),故一个文件恰属一类。

**V-20**:抽取器 MUST NOT 以字面 `operations:` 键探测 OpenAPI——实测 9 份文件内**无**该键,其 operation 是 `paths:` 下的方法键(FR-028 订正后的结论)。

**V-21**:只写闭合粗体正则会静默漏掉整个 `md-bold-paren` 形态(`.specify/specs/031-task-complexity-rubric/contracts/rubric-section.md` 用 `- **C-1 (heading)**`,闭合 `**` 在括注之后;该形态当前的文件数与条款数见 `notes/clause-form-census.md`)。故「可解析文件数」MUST 按 owner 声明的形态集分别计数,MUST NOT 报一个不含形态声明的单一数字。

**V-22**:一份**可被解析但抽出零条款**的文件 MUST 报「该文件贡献 0 条款」并计入一个非零伴生量,MUST NOT 静默算作已覆盖(边界情形)。

### E-5b 未覆盖集

| 字段 | 约束 |
|---|---|
| `members` | **两侧各一套**,不是同一个变量:条款侧 = 条款全集 − `[green:]` 认领子集;FR 侧 = FR 全集 − **条款块尾 `(FR-nnn)` 反向引用**子集(FR-026;FR 不是 `[green:]` 的目标,故 FR 侧与任务行无关) |
| `companion` | 伴生的**必须非空**量;两侧各给自己的伴生量(FR-025) |
| `prefix` | 每行以 STR-009 `UNCOVERED:` 起首 |
| `baseline_present` | 基线文件缺失时本实体不成立:核算 MUST 以非零码退出并点名缺失路径,MUST NOT 让差集平凡为空(FR-027 § 基线面) |

**V-23**:未覆盖集为空**只在伴生量非空时**才有意义(FR-025、FR-040)。

**V-24**:条款未覆盖与 FR 未覆盖 MUST 分列,二者**全集来源不同、被认领子集来源也不同**(条款侧子集 = `tasks.md` 的 `[green:]`;FR 侧子集 = 按 FR-022 块边界切出的条款块里的 `(FR-nnn)` 引用),MUST NOT 合并为一个计数,也 MUST NOT 各写一套解析——两侧抽取共用 owner 声明的形态集与块边界(FR-026、C-2、C-18)。

**V-25**:输出 MUST 可折叠为计数 + 可选展开;被点名文件数**随 owner 声明的覆盖面而变**(两个端值的当前实测由 `notes/clause-form-census.md` 拥有),且两种取值都远超可逐行铺满的量(FR-023、D-2)。

---

## E-6 逆样本 (Counter-Sample)

一份人为破坏了被守命题的最小制品。

| 字段 | 约束 |
|---|---|
| `breaks` | 破坏了哪个**检查单位**(恰一个,键到具体主语)。单位有三种同格形态(SC-011,2026-10-03 增):一个检查标签(E-3a)、一个**退出档**、或一个 verdict 词汇项——后两种覆盖没有标签集的主语(既有脚本里新增的 action 以「action + 期望档」为键);此前本字段写「恰一个 E-3a 标签」,于是 `run-checks` 与 US5 的逆样本无处可归 |
| `subject` | 该单位属于哪个检查器/哪个 action(必填;门的分母按它聚合,SC-011、GATE-9) |
| `expected_verdict` | 期望的 verdict |
| `expected_exit` | 期望的退出码 |
| `location` | MUST 建在临时目录,MUST NOT 落在 `.specify/specs/` 下(SC-001 Source) |

**V-26**:每个检查单位**恰有**至少一个逆样本;缺逆样本的单位视为未取证(FR-039、SC-011)。**分母 = 本特性新增的单位数**,不是该检查器现有的单位总数(一个既有脚本被扩 4 项,分母就是 4;全量标签集由其模块 docstring 拥有,D-5)——这一区分是 GATE-9 能由命令计算的前提。

**V-27**:守卫**负面命题**的检查项(某物不存在 / 未变化 / 未泄漏)MUST 另有一次变异演练记录:弄坏被守物 → 确认变红 → 精确反向替换复原 → 确认恢复绿,并复核复原后差异回到预期形态;演练临时产物的残留计数 MUST 为 0(FR-041、SC-011)。

**V-28**:SC-001 的命中率判据是 **4/4 且零交叉遮蔽**——四份各只破坏一类命题的副本,各自只报出对应那一类。

---

## E-7 判据主体 (Criterion Subject)

一条 goal 判据所约束的对象集合。

| 字段 | 约束 |
|---|---|
| `form` | `reference`(指代形)或 `enumeration`(成员枚举) |
| `glob` | 指代形的模式,相对仓根 |
| `members` | **解析那一刻**导出的成员集 |

**指代形字面**:`[subjects: <glob>]`(D-14)。选方括号标签族的依据是房子既有惯例:`[P]`、`[US<n>]`、`[blockedBy: …]`、`[green: …]`、`[[STR-NNN]]`。

**校验规则**

- **V-29**:指代形指向不存在的路径时 MUST 报可区分错误,MUST NOT 退化为空集合(FR-036)。
- **V-30**:导出集合为空(路径存在但无成员)时同样 MUST 报错,前缀为 STR-010 `SUBJECT EMPTY:`——空集合会让「零个主体全部满足」空真(FR-036)。
- **V-31**:同一判据行内指代形与**花括号展开记号** `\{[^}]*,[^}]*\}` 同现即报冲突,MUST NOT 静默择一(FR-037、D-14)。
- **V-32**(诚实边界):不带花括号的散文枚举(如「所有绘图技能」)与指代形同现时**检不出**。该边界 MUST 记入契约,MUST NOT 声称覆盖了它(D-14)。
- **V-33**:既有的纯枚举判据 MUST 保持完全一致的解析行为;本特性 MUST NOT 使任何既有 goal 失效或需要迁移才能继续解析(FR-038)。
- **V-34**:SC-010 的名字级比对当前全集只有 **1** 份 goal 定义(实测 `.specify/goal/` 下仅 `draw-two-layer-structure`),该数太小以致「比对为空」近乎空真,故 MUST 配反空真哨兵:至少断言被扫描的 goal 定义数 ≥ 1 且解析器确实产出了成员集(D-14、FR-040)。

**V-31 的实测依据**:`.specify/goal/draw-two-layer-structure/goal.md:15` 是本仓唯一真实的枚举型判据(「七个绘图技能(draw-diagram 与 draw-{d3js,drawio,echarts,excalidraw,mermaid,plantuml})…」),其 `## History` `:36`/`:37` 记录了同一条判据随成员集变化被反复改写(「六个绘图技能…」→「七个绘图技能…」)——这正是 US5 要消灭的脆弱性的**实证**。

---

## E-8 run 前置 verdict

团队 run 前五项检查的一次性机读结论。

| 字段 | 约束 |
|---|---|
| `team_slug` | 顶层 |
| `goal_slug` | 顶层 |
| `identity_kind` | 顶层,来自 `resolve_team_goal_identity` |
| `resolution` | 顶层,来自 `resolve_effective_target` 的 `{effective, source, declared_focus}` |
| `checks` | 5 条,每条含 `id`(1..5)、`name`(五个名字之一)、`verdict`、`message` |
| `verdict` | 顶层,由 5 条派生 |
| `blocked` | 顶层布尔 |

**校验规则**

- **V-35**:因前置条件不成立而被短路的检查 MUST 记 STR-004 `not-evaluated`,MUST NOT 记 `ok`(FR-032)。
- **V-36**:五项里有一项自身抛异常时,MUST 把该条记为 `not-evaluated` 并**继续评估其余四项**,MUST NOT 让一项异常吞掉整份 verdict(边界情形)。
- **V-37**:无 `--target` 时 MUST 先经 `resolve_effective_target` 解析有效 target;解析不出时 ②③④ 记 `not-evaluated`(无判定主体),①⑤ **仍 MUST 被评估**(只依赖团队与 goal 的绑定关系)(D-11)。
- **V-38**:退出码 MUST 按 STR-007 `0=ok / 2=input-error / 3=not-found / 4=invalid / 5=blocked` 分档,即**沿用 `goal-utils.py:44-47` 既有四码原义**、`blocked` 取实测空闲的 5;MUST NOT 让同一个码在同一脚本里按 action 而有两种含义(FR-033、D-13)。
- **V-39**:该 action MUST 零写入——任何一次调用都 MUST NOT 修改 `.specify/goal/` 或 `.specify/teams/` 下的任何文件(FR-034)。取证形态为调用前后的**字节校验和**对比(SC-007 Source)。
- **V-40**:MUST 复用既有内部解析函数而不重写第二套文法(FR-030);`run-checks` 的 help 行 MUST 以 `read:` 起首(D-12)。

---

## 状态迁移

本特性**不引入任何状态机**(FR-048:MUST NOT 改变 `/speckit.*` 的阶段划分或状态机)。唯一涉及状态的是既有物的读取:

- **goal 状态**:`TERMINAL_STATES`(`goal-utils.py:55`)决定第⑤项检查是否报 `goal-terminal`;本特性只读该状态,MUST NOT 迁移它。
- **target 状态**:`done` / `dropped` 决定第③项是否报 `target-terminal`;同样只读。
- **Feature 状态**:053 自身沿既有状态机 `Draft → Planned → Implemented`,由 `/speckit.plan` 与 `/speckit.implement` 各自拥有,本特性不改动该机器。
