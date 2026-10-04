# Contract: 绿点归属声明面(US2)

**Requirement**: `053-machine-decidable-artifacts` → Feature 053  
**Covers**: FR-015…FR-021  
**Subjects**: `templates/tasks-template.md`(声明面定义)、`scripts/python/validate-tasks.py`(解析与四项新检查)  
**Clause form**: `**C-N**` 行首裸粗体。  
**Class labeling**: 同 `contracts/checker-form.md`([制品类] / [行为类])。

---

## 声明面的形态

**C-1** [制品类] `templates/tasks-template.md` MUST 定义一个行内归属声明面,其字面形态为 STR-001 `[green: <contract>#<clause>]`。判据:对该模板 grep 该形态(或其带占位符的等价式)命中数 ≥ 1。(FR-015)

**C-2** [制品类] 一行任务 MAY 声明**零到多条**归属;声明零条时该行 MUST 与今天的行形态完全一致(即声明面是纯增量)。判据:一份不含任何 `[green:]` 的 tasks.md 在新检查器下 exit 0 且零 WARN。(FR-015)

**C-3** [制品类] 声明 MUST 与行内的其它方括号标签共存于**同一物理行**——既有约定要求整行任务(checkbox、ID、标签、描述、文件路径)MUST 留在单行(owned by `templates/commands/tasks.md:155`,机器强制于 `validate-tasks.py:9-12` 与 `:204-209`)。判据:把归属声明折到续行的副本被既有行形态检查报 ERROR。(FR-015)

**C-4** [制品类] 归属声明面 MUST **项目中立**:MUST NOT 含 `spec-kit` / `specify-cli` / `specify_cli` / `cloud-native-ai` 一类本仓专名;其形态说明 MUST 落在 tasks 模板而非某个 spec 的散文里。判据:对模板新增内容做专名 grep,命中数为 **0**。(FR-021、FR-044)

**C-5** [制品类] 新标签的落点 MUST 与既有 `[blockedBy: …]` 的说明同节:实测 `templates/tasks-template.md:104` 正是 `[blockedBy: T001,T002]` 的定义行(「explicit dependency tag … Machine-checkable alternative to prose」),它是行内方括号标签的**直接先例形态**;`:100-106` 是 `## Format:` 节。判据:新标签的说明落在该节内。(FR-015、D-1 类比)

## 解析

**C-6** [制品类] `validate-tasks.py` MUST 把该形态解析为 `(契约文件, 条款 id, 任务 id, 所处阶段)` 四元组。判据:对一份含一条声明的最小 tasks.md 跑 `--json`,输出的声明数组每项含四个字段。(FR-016)

**C-7** [制品类] 解析式 MUST 容许 `#` 之后含点号与连字符的条款 id(实测条款 id 位宽与形态均不统一:`C-1` / `C-01` / `C-001` / `C-3.4`),即分隔符取**第一个** `#`,其后至 `]` 前全部视为条款 id。判据:`[green: contracts/x.md#C-3.4]` 被解析为 `("contracts/x.md", "C-3.4")`。(FR-016、E-5a)

**C-8** [制品类] 出现在**围栏代码块内**或**行内代码跨度内**的该形态 MUST NOT 被当作真实声明解析:前者是**示例**,后者是**提及**——与 FR-009 对引用所画的是同一条区分,故复用 `clause_extract.strip_code_spans`(CommonMark 的 N 反引号串),MUST NOT 另立一个单反引号奇偶近似。判据**双向**:一份把声明写在 ```` ``` ```` 围栏内的 tasks.md,其解析出的声明数为 **0**;一份只用反引号**提及** `` `[green: <contract>#<clause>]` `` 而行尾另有一条裸声明者,解析出的声明数恰为 **1**;且**未闭合**反引号串之后的裸声明仍 MUST 被解析——否则「排除提及」会退化成「排除一切」,而一个永不触发的排除规则与没有规则不可区分。取证:2026-10-04 US2 实跑发现初版把本特性 `tasks.md` T018 行里那句**用来定义该标记**的字面量当成对文件名为 `<contract>` 的真实认领,报 `green-dangling` 并令该文件退出码变 1,即 GATE-7 被它自己的定义行推翻;先例另有本轮消化的一条反馈「指针落进了围栏示例块内」,靠一次围栏感知扫描才发现。(`requirements.md` § Edge Cases、FR-020 的 2026-10-04 扩写) (FR-020)

## 悬空归属(ERROR)

**C-9** [制品类] 对指向**不存在的契约文件**的声明 MUST 报 `green-dangling`(**ERROR**),而不是 WARN——悬空归属比跨阶段归属更严重。判据:退出码 **1**。(FR-016、SC-004)

**C-10** [制品类] 对指向**不存在的条款 id** 的声明同样 MUST 报 `green-dangling`(ERROR)。判据:契约文件存在但其中无该 id 时 exit 1,且消息点名文件与该 id。(FR-016、SC-004)

**C-11** [制品类] 条款 id 的可解析性 MUST 按 D-1 owner 文档声明的形态判定;对该文件不可解析的形态 MUST 报 `green-dangling`,MUST NOT 静默放行。判据:对一份 `md-none` 形态(无任何机器可辨条款)的契约文件声明归属时报 ERROR。(FR-016、FR-022)

## 跨阶段绿点(WARN)

**C-12** [制品类] `green-cross-phase`(**WARN**)的触发条件 MUST 为:**同一契约内**,相邻两行认领的条款**序数**沿其单调行序 `order` **严格递减**时,对该相邻对报一次,消息点名条款、涉及的两行、以及二者的阶段串与行序。序数取条款 id 里的数字组元组(`C-1` → `(1,)`、`C-3.4` → `(3,4)`,故 `C-01` 与 `C-1` 等值);无数字的 id(`yaml-assertions` 一类的名字)无序,MUST **跳过**而不是猜一个序。**(2026-10-04 落定)** FR-017 的字面「某条款的归属任务集中存在所处阶段晚于声明行的任务」欠定,三种读法里只有本条与本判据的两个半句同时相容:取**逐条款**归属集,则下面那份反向副本里每条条款都只有一个认领行,判据的第二半永不可达;取**逐契约**归属集,则正向副本也会报,第一半不可达。本读法另外使 C-27 要求的四标签逆样本互不遮蔽——同一条款被两行认领是序数**相等**而非递减,故只触发 `green-clause-collision`,不连带触发本检查。判据:对一份归属序与阶段序一致的最小 tasks.md 跑得 **0** WARN;对一份把认领 C-2 的行放在认领 C-1 的行**之前**的阶段的副本跑得 **≥1** WARN——两个方向都实测;另配一份**相位号与行序相反**(`## Phase 9` 在前、`## Phase 2` 在后)的副本仍得同一条 WARN,以钉住 C-13 的「比较 `order` 而非阶段号」。(FR-017、SC-003)

**C-13** [制品类] 跨阶段判定 MUST 用既有的**单调行序** `order`(`validate-tasks.py:123` 初始化、`:171`/`:181` 递增并存入每条任务),MUST NOT 依赖数值阶段索引——该脚本**没有**数值阶段索引(`PHASE_HEADING` `:57` 只捕获标题串,`by_phase` `:236-239` 按标题字符串分组)。判据:直接先例是 `:229-233` 的 `blockedBy` 前向依赖 WARN,它同样比较 `order`。(FR-017、D-8)

**C-14** [制品类] 仅跨阶段 WARN 时退出码 MUST 仍为 **0**——既有退出码表只有「无 ERROR → 0」「有 ERROR → 1」两档,警告不单独成档(被 `test_c5_exit_code_table:353,356` 钉住)。MUST NOT 为此新设第三档。(FR-017、SC-004、clarify 轮订正)

## 两类冲突(WARN,分列)

**C-15** [制品类] 两行任务认领**同一条款的同一区间**时 MUST 报 `green-clause-collision`(WARN)并点名两行。判据:对一份两行都声明 `[green: contracts/x.md#C-1]` 的 tasks.md 跑得 ≥1 WARN 且点名两行。(FR-018(a))

**C-16** [制品类] 同一**测试路径**出现在两个核验行、且两行的绿点**不同**时 MUST 报 `green-path-divergence`(WARN),点名两行与该路径。**(2026-10-04 T045 实跑收窄,并订正 `data-model.md` E-4)**:「测试路径」是本条的**辖域**,不是修辞——E-4 曾把 `test_paths` 字段定义为「同行经路径分类后的**写入目标**集」,与字段名自相矛盾;按那个定义落地后,本特性自己的 `tasks.md` 在 T045 写入 182 条认领的当下即报出 **3** 条假违例,因为 T007/T008/T017 三行都把自己那份取证**追加**进同一个 `notes/red-first-evidence.md`——一个只追加的汇集文件不是任何一行的绿点,没有一行在声称「由我让它转绿」。判定取结构事实而非猜测:`tests` 是房子模板自己声明的位置(`templates/tasks-template.md` § Path Conventions)、`test_*` 是 pytest 的收集前缀。收窄 MUST 配正样本对照(同样两行、同样绿点不同,但共用的是 `tests/` 下的文件 → MUST 仍报),否则「收窄」与「删掉这条检查」不可区分;`parallel-safe` **不受影响**——两个 `[P]` 行写同一文件无论该文件作何用都是真冲突。判据正反两向:绿点不同的副本 ≥1 WARN;「同一路径、两行绿点相同」的副本 **0** WARN——证明该检查认的是**绿点分歧**而不是**路径共用**。(FR-018(b)、US2 验收场景 6)

**C-17** [制品类] `green-clause-collision` 与 `green-path-divergence` MUST **分列**报出,MUST NOT 合并为一个计数;二者的判据不同(条款区间重叠 vs 测试路径共用且绿点不同),同一份 tasks.md 上可以各自独立触发。判据:构造一份只触发其一的制品,另一标签的命中数为 0。(FR-018、D-3、V-8)

**C-18** [制品类] 实现处 MUST 引用 `.specify/memory/glossary.md` 已登记的术语「条款分区 (Clause Partition)」,MUST NOT 另造名词。判据:对脚本源或契约 grep 该术语命中数 ≥ 1。(FR-018)

**C-19** [行为类] C-16 机械化的是一项**已经存在**的散文义务:`templates/commands/tasks.md:197` 原文「Add a self-check that flags any test path appearing in two verification rows with different green points」;而 glossary 的「条款分区」条目本身即写明「生成期 MUST 机械核算分区的并集覆盖全部条款且无幻影记号」。落地后该散文自检 MAY 改为指向本检查,MUST NOT 同时保留两套判据。(FR-018、D-3)

## 与既有检查的正交性(承重)

**C-20** [制品类] 归属声明 MUST 与既有的行形态检查正交:一行只声明归属而不声明文件路径时,既有检查 MUST NOT 误报。判据:对一份「一行只有 `[green:]`、无文件路径」的 tasks.md 跑,`row-format` 命中数为 **0**。(FR-019)

**C-21** [制品类] 归属声明内的契约路径 MUST NOT 被既有路径分类器当作**写入目标**。实测反例(本轮实跑,临时目录已删净):

```text
- [ ] T001 [P] Write the thing in docs/a.md [green: contracts/x.md#C-1]
- [ ] T002 [P] Write another thing in docs/b.md [green: contracts/x.md#C-2]
→ WARN 3: parallel-safe: … both WRITE ['contracts/x.md'] …   ← 假告警
```

`docs/a.md` 与 `docs/b.md` 本不相同,告警点名的却是标签内的契约路径。判据:上述制品在修复后 `parallel-safe` 命中数为 **0**;正样本对照(两行 `[P]` 写**同一**真实路径)MUST 仍报 WARN,以证明该检查未被削弱。(FR-019、D-7)

**C-22** [制品类] 修复形态 MUST 是**先抽取归属声明、再对残余文本做路径分类**,MUST NOT 靠往 `POINTER_GOVERNOR`(`validate-tasks.py:70-75`)里加标签前缀来解决。依据:该表的注释明写它是「a closed list of unambiguous read-only **governors**」即治理**词**,而 `[green:` 是标签前缀不是词,塞进去会使该表语义不再自洽;先抽取再分类使 C-20 的正交性成为**构造性质**而不是一个正则特例,并同时产出 C-6 的四元组。(FR-019、D-7)

**C-23** [行为类] C-21 的机理 MUST 记入实现处的注释:`PATH_TOKEN`(`:63-65`)的尾字符类不含 `#`,故它在标签内匹配出 `contracts/x.md`;`:106-107` 的 `if "[" in tok or "]" in tok: continue` **保护不到它**——被匹配的 token 自身不含方括号,方括号在匹配范围之外。(FR-019、D-7)

**C-24** [行为类] 探「C-21 不再误报」这一命题时 MUST 先证明 `parallel-safe` 在正样本上会报(两行 `[P]` 写同一路径),否则探到的是「检查没被触发」——本特性 plan 期的第一次探针即因 T001 漏掉 `[P]` 而误判为「无告警」。该纪律见 `contracts/checker-form.md` C-21。(FR-019、FR-039)

## 钉子扩充

**C-25** [制品类] US2 落地后,`validate-tasks.py` 的标签集 MUST 为既有 6 项 + 新增 4 项(`green-dangling`、`green-cross-phase`、`green-clause-collision`、`green-path-divergence`)= **10** 项;`EXPECTED_CHECKS`(`test_validate_tasks_parallel_safety.py:75-82`)与脚本 docstring 的枚举段 MUST 在**同一提交内**同步扩充,因为 `:312` 从 docstring 抽取标签、`:314` 断言二者集合相等。(FR-046、D-5)

**C-26** [制品类] 退出码表钉子 `test_c5_exit_code_table`(`:346-370`)MUST 被扩充以覆盖新档:`green-dangling`(ERROR)→ **1**、仅 `green-cross-phase` / 两类 collision(WARN)→ **0**。MUST NOT 改动既有四档断言的语义。(FR-046、C-14)

**C-27** [制品类] 四项新检查 MUST 逐项有逆样本(共 ≥ 4 份),且 `green-path-divergence` 的逆样本 MUST 成对(绿点不同 → 报;绿点相同 → 不报),因为它的命题是**分歧**而非**共用**。(FR-039、SC-011、C-16)
