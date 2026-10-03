# Contract: 条款语法 owner 与覆盖核算(US3)

**Requirement**: `053-machine-decidable-artifacts` → Feature 053  
**Covers**: FR-022…FR-028  
**Subjects**: `shared/definitions/contract-clause-definitions.md`(新建 owner,D-1)、`scripts/python/account-clause-coverage.py`(新建,D-10)  
**Clause form**: `**C-N**` 行首裸粗体。  
**Class labeling**: 同 `contracts/checker-form.md`([制品类] / [行为类])。

---

## 条款语法的唯一 owner

**C-1** [制品类] `shared/definitions/contract-clause-definitions.md` MUST 存在,且 MUST 在开篇数行内声明自己是条款语法的**唯一 owner** 并点名它拥有什么(房子对 owner 文档的要求:「an owning document says so in its opening lines and names what it owns」)。判据:文件存在;对其开篇 grep「owner / 唯一真源」一类自我声明命中数 ≥ 1。该文档另 MUST 携一行指向 `.specify/shared/guidelines/user-facing-comprehension.md` 的 canonical 指针(Constitution Principle XV 对新增 `shared/` 文档的要求;它是**指针形**而不是复写其规则表——指针形合法、内容形即第二真源)。判据:对该文件 grep 该路径命中数 ≥ 1,且**不**含其界面类表的复写。(FR-022、D-1、Principle XV)

**C-2** [制品类] 该文档 MUST 声明它覆盖的**形态集**,逐形态给出判据正则。形态集为六种,判据如下(**计数不在本条复写**,其唯一拥有者是 `notes/clause-form-census.md`,引用它):

| 形态 | 判据 |
|---|---|
| `md-bold-closed` | `\*\*C-\d+(?:\.\d+)*\*\*` |
| `md-bold-paren` | `\*\*C-\d+` 命中而闭合形不命中 |
| `md-heading` | `^#{1,6}\s+C-\d+` |
| `yaml-openapi` | `openapi:` 且 `paths:`;条款 = `paths:` 下的 HTTP 方法键 |
| `yaml-assertions` | `^\s+- id:` |
| `md-none` | 以上 `.md` 判据全不命中 |

判据:该文档对六种形态逐一在场;四种 `.md` 形态互斥(实测同现文件数为 **0**),故一个文件恰属一类。**该文档还 MUST 声明一条条款块的边界**:自 `**C-n**` 标记行起,至下一个标记行**或下一个章节标题**先到者为止;围栏块与行内代码跨度内的文本不计(2026-10-03 增,来源 `/speckit.analyze` F-20——不声明边界就有三种都自洽的总数,本特性 182 条里恰有 2 条的 `(FR-nnn)` 在标记行之后的行上)。实测:**块边界**的三种读法(在旧的「整块正文计数」抽取下)给出 **190 / 192 / 193** 三个总数,相差 3 条,而三者都自称是同一份语料的实测——这就是「规则没写下来」的代价。**本条把规则定全**(三件,缺一不可):① 块边界取「标记或标题先到」(标题不属于任何条款块);② 引用只认**引用组** = 块内最后一个含 FR/SC id 的括号,容忍一层嵌套(`(FR-018(a))`)、`FR-a…FR-b` 区间展开;③ 组外的同形字样按「提及」处理(FR-009)。按此规则实测三元组 = **188 含重复 / 165 唯一对 / 17 条不引用 FR**(三元组 = 含重复 / 唯一对 / 不引用 FR 的条款数),`feature-ref.md` 的两张映射表已于 2026-10-03 按此整表重导;重导前印的 192 / 166 / 16 出自整块正文计数 + 未记录的边界,把散文里的权限引用也算成了覆盖。据此该表里引用 `requirements-checker` C-21 的那一行(US1 的过渡 awk 债务)MUST NOT 再列该条款——那个 `FR-…` 只出现在中间的章节标题里。判据:`clause_extract.py`(T005)按这三条重导本目录契约,三个数与 `feature-ref.md` § 覆盖统计 逐值相符。(FR-022)

**C-3** [制品类] 该文档 MUST 指定**新契约的规范形态**(一种),并把其余形态声明为**只读识别的遗留形态**。判据:文档内「规范 / canonical」与「遗留 / legacy」两个词各自命中 ≥ 1,且规范形态恰一种。(FR-022)

**C-4** [制品类] 该文档 MUST NOT 复制 `contracts/*` 里任何一份既有契约的条款内容——它是**语法**的 owner,不是条款的副本。判据:对该文档与全仓契约(总数由 `notes/clause-form-census.md` 拥有)做条款 id 交集,交集内任何 id 若在该文档中以条款正文形式出现即违例(引用形态举例除外)。(FR-022、唯一真源纪律)

**C-5** [制品类] 该文档落在 `shared/` 下,故从**第一稿起**就在门控扫描面内(`scan-confirmation-gates.py:35` 的 `SCAN_DIRS` 含 `shared`),而 total 为 **23**、整数余量 **0**。其措辞 MUST 对 `BLOCKING_PATTERNS`(**17** 条,`:46-64`)零命中。判据:落盘后实跑扫描器,total 仍为 **23**、violations 为 **0**。(FR-045、FR-022 落点约束)

**C-6** [行为类] 该文档 MUST NOT 靠放宽被扫描文档集、调高上限或修改任何基线数据来满足 C-5——上限由**三种形态**的断言钉住(硬编码字面量 / 与冻结基线相等 / 派生上限 `baseline * 0.25`),合计 **9** 个断言站点另有 **4** 个元钉子正则匹配前三个站点的**源码文本**,故改动任一钉子的措辞即打红一个元钉子。唯一合法路径是措辞设计。(FR-045、D-16)

## 核算脚本的抽取

**C-7** [制品类] `scripts/python/account-clause-coverage.py` MUST 按 owner 声明的形态抽出条款全集;反空真哨兵 MUST 是**关系式**而不是字面量:「可按 owner 语法解析的文件数 + 逐个点名跳过的文件数 == **本次实扫的文件总数**」,其中总数由脚本在运行时导出并印出。MUST NOT 把该总数写成字面 `110`——本特性自己的 7 份契约就在被扫描面内,落盘后同一命令的总数已变为 **117**(实测,见 `notes/clause-form-census.md` § 自指修正),写成字面量会在本特性自己的制品落盘那一刻自我证伪,而这正是本特性要消灭的缺陷形态。(FR-023、SC-006)

**C-8** [制品类] 对无法按该形态解析的文件 MUST **逐个点名**,并把点名数计入一个**非零伴生量**,MUST NOT 静默跳过。判据:被点名文件数**随 owner 声明的覆盖面而变**(只认 `md-bold-closed` 与六形态全认给出不同的数,二者的当前实测值见 `notes/clause-form-census.md`);两种取值都 MUST 被印出而不是被吞掉,且 MUST 与其所用的形态集声明同时印出,否则该数不可比。(FR-023、D-2)

**C-9** [制品类] 点名清单 MUST 可被折叠为**计数 + 可选展开**,MUST NOT 强制逐行铺满每次输出。判据:默认输出含计数行;展开需一个显式旗标。(FR-023)

**C-10** [制品类] OpenAPI 抽取 MUST 以 `paths:` 下的 HTTP 方法键为条款全集,MUST NOT 以字面 `operations:` 键作探测条件——实测 9 份文件内**无**该键。判据:对全部 OpenAPI 契约抽出的 operation 总数与 `notes/clause-form-census.md` 记录的该形态 id 数相等(改前实测 **39**,as-of 该普查)。(FR-028、V-20)

**C-11** [制品类] 结构化断言形抽取 MUST 以 `^\s+- id:` 的取值为条款全集。判据:对 `.specify/specs/013-portable-skill-creation/contracts/portable-skill-creation.openapi.yaml` 抽出的 id 集恰为 `no-tool-discovery-step`、`no-tool-template-boilerplate`、`no-mandatory-tool-manifests`、`no-refresh-tools-in-script`、`mirror-parity`、`no-tool-manifest-in-checklist`(按**名字**集合比对,不按计数)。该文件名为 `.openapi.yaml` 却**既非** OpenAPI,故 MUST NOT 以扩展名或文件名判定形态。(FR-028)

**C-12** [制品类] 两种 `.yaml` 抽取器 MUST 是**手写行级解析**,MUST NOT 引入 PyYAML 依赖。依据(实测):`pyproject.toml` 的 `dependencies` 六项无一为 YAML,全部 `scripts/python/*.py` 零 `import yaml`;房子先例是 `gate-check.py:48` 的 `parse_gate(text)` 逐行解析 `.specify/gate.yaml`。(FR-028、D-2)

**C-13** [行为类] 任何**解析存疑**的 `.yaml`(流式语法、锚点、多文档、非预期缩进)MUST 回退到 C-8 的点名跳过,MUST NOT 猜测条款集。判据:对一份人为写成流式语法的 OpenAPI 副本跑,该文件被点名而**非**被算作 0 条款已覆盖。(FR-028、FR-023)

**C-14** [制品类] 抽取器 MUST NOT 只写闭合粗体正则:实测 `.specify/specs/031-task-complexity-rubric/contracts/rubric-section.md` 用 `- **C-1 (heading)**`(闭合 `**` 在括注之后),`\*\*C-\d+(?:\.\d+)*\*\*` 不命中而 `\*\*C-\d+` 命中,其 10 条条款会被静默漏掉。判据:该文件被归入 `md-bold-paren` 且贡献 **10** 条条款。(FR-023、V-21)

**C-15** [制品类] 一份**可被解析但抽出零条款**的文件 MUST 报「该文件贡献 0 条款」并计入一个非零伴生量,MUST NOT 静默算作已覆盖。判据:对一份只有标题与散文、无任何条款形态的 `.md` 契约跑,它出现在点名集里而不是消失在分母里。(边界情形、V-22)

## 核算结果的表达

**C-16** [制品类] 核算 MUST 以**集合差**表达结果:全集减去被认领子集,印出未覆盖集,每行以 STR-009 `UNCOVERED:` 起首;未覆盖集为空时 exit **0**,否则 exit **非 0**。判据:对一份 3 条款契约、2 条被认领的最小 spec,印出的未覆盖集**恰为那 1 条**且以该前缀起首;补上认领后为空且 exit 0。(FR-024、SC-005)

**C-17** [制品类] 未覆盖集为空时 MUST 同时印出至少一个**必须非空**的伴生量(已认领条款数、被扫描契约文件数),使「空因为对」与「空因为盲」可区分。判据:契约测试同时断言空集与伴生量 > 0;把分母人为置 0 时该哨兵变红。(FR-025、FR-040)

**C-18** [制品类] 条款未覆盖与 FR 未覆盖 MUST **分列**,二者的全集来源不同(条款来自契约文件、FR 来自 `requirements.md`),MUST NOT 合并为一个计数。**两侧的「被认领子集」来源亦不同**(2026-10-03 增,来源 `/speckit.analyze` F-19,此前这条只分列了全集、没分子集,于是「FR 侧被认领子集 = 条款块尾 `(FR-nnn)` 反向引用」只存在于 `tasks.md` 的散文里——正是 FR-021 禁止的形态):条款侧子集 = `tasks.md` 行上的 `[green:]` 归属声明;FR 侧子集 = 按 C-2 边界切出的条款块里、其**引用组**(块内最后一个含 FR/SC id 的括号,容忍一层嵌套、`FR-a…FR-b` 区间展开;组外的同形字样一律按「提及」处理,FR-009)中的 `(FR-nnn)`。FR MUST NOT 是 `[green:]` 的目标(目标面见 C-9…C-11),故 FR 侧的 verdict 与任务行无关,只随契约条款的**引用组**变化。判据:输出含两个独立小节与两个独立计数;删掉某条款块引用组里的一条 `(FR-nnn)` 后重跑,该 FR MUST 出现在 FR-未覆盖名单里且退出码非零(这条逆样本同时补上 `fr-uncovered` 标签此前无逆样本的空洞)。(FR-026)

**C-19** [制品类] 两次运行 MUST 按**名字**比对而非按计数。判据:输出为有序名字集,形态与 `run-tests.sh --names-out` 同构(每行一个名字、已排序),使 `comm -13` 可直接消费。(SC-005、D-10)

## 既有 spec 的适用性:冻结名字级基线

**C-20** [制品类] 覆盖核算 MUST NOT 要求改造既有 spec 的契约文件。判据:核算脚本对仓内任何文件**零写入**(写入点扫描命中数为 0),且实跑前后 `.specify/specs/` 的字节校验和不变。(FR-027)

**C-21** [制品类] 对既有 **44** 个 spec 目录(其中 **43** 个含 `contracts/`;两个数同基,都**含**本特性自己的目录——初版把含 053 的 44 与不含 053 的 42 混在一句里)的适用性 MUST 取**冻结名字级基线**判据:开工时把当时的未覆盖项**名字集**冻结成 `.specify/specs/<key>/coverage-baseline.txt`,此后只对相对该基线**新增**的未覆盖项阻断。判据:`comm -13 <baseline> <current>` 为空即通过;基线文件落在本特性目录。**冻结面 MUST 排除本特性自己的 spec 目录**(FR-027 § 基线面,2026-10-03 增):本特性自己的条款与 FR 因此恒在基线之外,只能被认领、不能被豁免。**判据 MUST 成对**,光有「基线外未覆盖集为空」不构成本条的通过——同一轮输出里 MUST 另有「本特性已认领条款数」一行且该数 MUST 非空;否则认领从未发生时本条同样报绿(永不变红的检查),与 FR-025 要区分的「空因为盲」同形。**触发 MUST NOT 循环定义**(2026-10-03 增,来源 `/speckit.analyze` F-18):「首次全树运行**变绿**时冻结」是循环——变绿需要基线、基线需要先跑;唯一时机 = 实现开工时的首次全树核算运行(与 `data-model.md` E-3c 的 `frozen_at`、FR-027 § 基线面、`requirements.md` 的 FR-027 Source 行同时机,四处 MUST 说同一件事);**基线文件缺失时 MUST 以非零码退出并点名缺失路径**,MUST NOT 把「无基线」读成「无豁免项」而使差集平凡为空。(FR-027、FR-025、clarify 裁定 3、`/speckit.analyze` F-07/F-18)

**C-22** [制品类] 基线内的既有未覆盖项 MUST NOT 阻断,但每轮 MUST 仍印出其**计数**,使欠账可见而非消失。判据:输出含「基线内既有 N 项」一行,N 与基线文件行数一致。(FR-027)

**C-23** [制品类] 基线 MUST 连同**当轮 owner 声明覆盖哪些形态**一起记录,否则「可解析文件数」在两个 owner 定义之间不可比。判据:基线文件头部含形态集声明或其指纹。(FR-027、V-12、D-2)

**C-24** [行为类] 该判据与本规格 SC-010 / SC-012 已采用的「冻结名字级基线 + `comm -13` 差集为空」**同形**,故不产生永久豁免清单、也不留下「同一检查器对两类 spec 给不同判定」的双标准。落地 MUST 复用同一习语,MUST NOT 另造第二种基线形态。(FR-027、D-10)

**C-25** [行为类] 核算脚本 MUST NOT 复制 `scan-confirmation-gates.py --baseline` 的比较形态——它读基线的**顶层** `total` 而冻结值嵌在 `confirmationGates` 下,且退出码只反映 `violations`,故作为相等门不可用;该缺陷已记录两次(`.specify/memory/constitution.md:14` 后续 TODO (a);052 的 `contracts/gate-neutrality.md` + `verification.md:209`)而上游仍未修。(D-10、A-3)

## `.yaml` 的显式处置

**C-26** [制品类] `.yaml` 契约 MUST 被显式处置,MUST NOT 静默忽略。处置形态:两种语法各一个抽取器(OpenAPI 取 `paths:` 下的方法键、结构化形取 `- id:`)。判据:扫描输出里 `.yaml` 的**已解析文件数 == 被扫描的 `.yaml` 文件总数**,且被点名跳过的 `.yaml` 数为 **0**(除非触发 C-13 的回退);`.yaml` 的文件总数与条款 id 数由 `notes/clause-form-census.md` 拥有,本条不复写。核算面的「可解析 / 总数」两个数同样以关系式表达,理由见 C-7。(FR-028、D-2)

**C-27** [制品类] SC-006 的取证 MUST 是一次对全仓 `.specify/specs/*/contracts/` 的只读扫描,输出「可按 owner 语法解析的文件数 / 逐个点名跳过的文件数 / **本次实扫总数**」三个数,并断言前两者之和等于第三者(关系式哨兵,见 C-7);采集时机为 owner 文档落地后一次、核算脚本落地后一次。逐形态计数由 `notes/clause-form-census.md` 唯一拥有,本条不复写任何数字——其中**只有改前基线是可安全引用的字面量**,含本特性自己契约的值随每次编辑变动,MUST 现场跑该文件内的命令(从仓根)。(SC-006、SC-006 Source)
