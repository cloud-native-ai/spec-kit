# Contract: goal 判据主体的指代形(US5)

**Requirement**: `053-machine-decidable-artifacts` → Feature 053  
**Covers**: FR-035…FR-038  
**Subjects**: `shared/definitions/goal-definitions.md`(概念 owner,新增一节)、`scripts/python/goal-utils.py`(解析)  
**Clause form**: `**C-N**` 行首裸粗体。  
**Class labeling**: 同 `contracts/checker-form.md`([制品类] / [行为类])。

---

## 指代形的定义

**C-1** [制品类] `shared/definitions/goal-definitions.md` MUST 新增一节定义一个可由程序解析的**判据主体指代形**,使主体集合在**解析那一刻**被导出,而不是取自判据文本里的成员枚举。判据:该文件(实测 137 行,镜像 `diff -q` 相同)新增一个 H2/H3 节,节名含「判据主体 / Criterion Subject」。(FR-035)

**C-2** [制品类] 指代形的字面 MUST 为 `[subjects: <glob>]`,glob 相对仓根。判据:该字面在 owner 文档内定义恰好一次,并被解析器的正则单点引用。选方括号标签族的依据是房子既有惯例:`[P]`、`[US<n>]`、`[blockedBy: …]`(`validate-tasks.py:54-61`)、US2 的 `[green: …]`、`templates/requirements-template.md:173-176` 的 `[[STR-NNN]]`。(FR-035、D-14)

**C-3** [制品类] 该形式在改前**无任何既有形态可沿用**:`grep -n "glob\|\*/\|directory-reference\|<dir>\|rglob\|iterdir" shared/definitions/goal-definitions.md` 无命中;该文件唯一的路径形态是存储位置(`:109-111`、`:46`、`:135`),从不作判据主体;`goal-utils.py` 里唯一的 `iterdir` 是归档枚举(`:765`)。故本节是**新增**而非改写。(FR-035、D-14)

**C-4** [制品类] 该文件是**概念 owner 而非被解析对象**——它不被任何程序解析,只被链接(程序化触点仅 `goal-utils.py:13` 的 docstring 引用、`test_goal_targets_engine.py:296` 的 `AUTHORITY` 常量 + `:357` 断言、`test_confirmation_gates_sweep.py:169`、`test_goal_reference.py:150`;散文消费者 20 处)。故 US5 在该文件里**增一节**而不改既有语义,MUST NOT 重写其既有节。(FR-035、D-14)

## 导出与两种失败

**C-5** [制品类] 指代形指向**不存在的路径**时 MUST 报可区分错误,MUST NOT 退化为空集合。判据:对一份指向不存在目录的判据跑解析,退出码/verdict 与「路径存在但无成员」的那一档**互相可区分**。(FR-036)

**C-6** [制品类] 导出集合为**空**(路径存在但无成员)时同样 MUST 报错,前缀为 STR-010 `SUBJECT EMPTY:`——空集合会让「零个主体全部满足」空真。判据:对一个存在但为空的目录跑,输出以该字面量起首并 exit 非 0。(FR-036、边界情形)

**C-7** [制品类] C-5 与 C-6 的两档 MUST 各有一个逆样本,且 MUST 各配反空真哨兵:证明「报错不是因为解析器根本没跑」——即同一份输入下解析器确实产出了一个成员集(可为空)与一个错误。(FR-036、FR-040)

## 冲突判定与其诚实边界

**C-8** [制品类] 一条判据同时使用指代形与成员枚举时 MUST 报冲突,MUST NOT 静默择一。冲突判据取:同一判据行内 `[subjects:]` 与**花括号展开记号** `\{[^}]*,[^}]*\}` 同现。(FR-037、D-14)

**C-9** [行为类] C-8 的判据依据是**实测到的**枚举形态,不是猜测:本仓唯一真实的枚举型判据是 `.specify/goal/draw-two-layer-structure/goal.md:15`「七个绘图技能(draw-diagram 与 draw-{d3js,drawio,echarts,excalidraw,mermaid,plantuml})…」,其 `## History` 直接证明了 US5 要消灭的脆弱性——同一条判据随成员集变化被反复改写(`:36` 前值「六个绘图技能(draw-diagram 与 draw-{d3js,echarts,excalidraw,mermaid,plantuml})」、`:37` 前值「七个绘图技能(… drawio …)」)。(FR-037、D-14)

**C-10** [行为类] **诚实边界**:不带花括号的散文枚举(如「所有绘图技能」)与指代形同现时**检不出**——自由散文里的枚举不可机械判定。该边界 MUST 记入 owner 文档与本契约,MUST NOT 声称覆盖了它;声称覆盖了实际覆盖不到的东西正是 `.specify/memory/glossary.md`「制品类/行为类条款」条目所禁止的形态。(FR-037、D-14、V-32)

## 向后兼容

**C-11** [制品类] 既有的**纯枚举**判据 MUST 保持完全一致的解析行为;本特性 MUST NOT 使任何既有 goal 失效或需要迁移才能继续解析。判据:SC-010 的名字级比对——落地前后对仓内**全部**既有 goal 定义跑一次解析,失败集合按**名字**比对为空(`comm -13` 形态),MUST NOT 按计数。(FR-038、SC-010)

**C-12** [制品类] SC-010 的当前全集**只有 1 份** goal 定义(实测 `.specify/goal/` 下仅 `draw-two-layer-structure/goal.md`,4337 B),该数太小以致「比对为空」近乎空真,故 MUST 配反空真哨兵:至少断言被扫描的 goal 定义数 **≥ 1** 且解析器确实产出了成员集。(FR-038、FR-040、D-14)

**C-13** [行为类] SC-009 的取证 MUST 使指代形的价值**直接可见**:对同一主体集合分别用指代形与成员枚举写两条判据,在目录里增删一个成员后,指代形导出的集合随之变化而枚举形不变,该差异在输出里可见。增删 MUST 在临时副本里做,MUST NOT 改动真实 skills 目录。(SC-009、SC-009 Source)

## 第二个解析器

**C-14** [制品类] US5 MUST 显式处置 `skills/create-team/scripts/build-summary-input.py:354-391` 的**本地** goal 判据解析器:要么让它同样理解指代形,要么显式声明它不理解并记录后果。MUST NOT 沉默。判据:owner 文档或本契约内有一行点名该文件及其处置。(FR-035、D-15)

**C-15** [行为类] 该本地解析器是**刻意**不 import 的——`:356-360` 明写 "This parses locally rather than importing `scripts/python/goal-utils.py` … cross-tree import breaks once installed"(它是 `skills/` 树内脚本,安装后与 `scripts/python/` 不同树)。故「让它理解指代形」的代价是**两处解析器同步**,MUST NOT 靠加一个 import 解决。(D-15)

**C-16** [制品类] 该文件另有自己的退出码表(`:41` `EXIT_OK, EXIT_INPUT_ERROR, EXIT_NO_MATERIAL = 0, 2, 3`、`:44` `EXIT_SERIALIZED = 4`),其 `3`/`4` 与 `goal-utils.py:44-47` 的 `EXIT_NOT_FOUND`/`EXIT_INVALID` **语义相左**——即仓内已有第五套退出码约定。本特性 MUST NOT 顺手统一它(超出声明范围),但 MUST 在 owner 文档里记录该分歧以免后来者误以为一张表通吃。(D-15、A-3)

## 钉子

**C-17** [制品类] 指代形的解析 MUST 有契约测试钉住其**正则形态**与**两档失败**,形态抄 `tests/contract/test_trigger_engine.py:48` 的常量表 + 逐项循环;MUST NOT 只以散文断言。(FR-046)

**C-18** [制品类] `test_goal_targets_engine.py:296` 的 `AUTHORITY = ".specify/shared/definitions/goal-definitions.md"` + `:357` 断言 MUST 在新增一节后仍成立——即新节 MUST 落在该文件内且不破坏既有断言所指的文本。判据:落地后该测试仍绿。(FR-035、C-4)

**C-19** [行为类] 该文件在门控扫描面内(`scan-confirmation-gates.py:35` 的 `SCAN_DIRS` 含 `shared`,且 `test_confirmation_gates_sweep.py:169` 把它列入扫描文件集),而 total 为 **23**、整数余量 **0**,故新节措辞 MUST 对 `BLOCKING_PATTERNS`(**17** 条)零命中。判据:落盘后实跑扫描器 total 仍为 23、violations 为 0。(FR-045)
