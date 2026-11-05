# Data Model — 082 机制/策略分离与技能引用归一化（Mechanism–Policy Separation & Skill-Reference Normalization）

**Owner boundary**: 本文件定义本特性引入的**实体、字段、校验规则与状态转移**；能力一（机制/策略分离）的**语义权威**是 `shared/definitions/mechanism-policy-definitions.md`（[[STR-003]]），能力二（技能引用归一化）的**语义权威**是 `shared/definitions/skill-reference-definitions.md`（[[STR-004]]）。两者冲突时 owner 胜，本文件为陈旧。

**投影面**：本文件是两份 owner 的**形态投影**——可以收窄 owner 的值域，MUST NOT 扩大；它不复述 owner 的判据表、症状表、提示骨架、接受形式清单或失败语义表，只把它们变成可断言的字段。

**Census**: 10 个实体（E-1 … E-10；E-1…E-7 属能力一，E-8…E-10 属能力二）、34 条校验规则（V-1 … V-34）、1 个封闭谓词（C1）、1 个封闭成员表（3 / 2 / 1）、1 个封闭允许差异集（18 条路径登记，其中属比较单元者 8）、3 条状态转移（SM-1 作者侧判定、SM-2 消费侧检查、SM-3 引用归一化）。

每个实体都同时给出 **carrier**（物理承载它的文件）与 **consumer**（读它的契约/测试）——只有 carrier 而没有 consumer 的实体，正是「绿了但什么都没证明」的失效面（Constitution XVI）。

## E-1 — 原则本体（Principle）

**Carrier**: `shared/definitions/mechanism-policy-definitions.md`（框架源；镜像 `.specify/shared/definitions/`）
**Consumer**: `tests/contract/test_mechanism_policy_owner_doc.py`、`test_mechanism_policy_ownership.py`

| 字段 | 域 | 规则 |
|---|---|---|
| `canonical_name_en` | 字面 `Mechanism–Policy Separation` | [[STR-003]]；标题行逐字使用（V-1） |
| `canonical_name_zh` | 字面 `机制/策略分离` | 双语形态 `机制/策略分离(Mechanism–Policy Separation)` 至少在标题行出现一次（owner § 双语） |
| `owner_path` | `shared/definitions/mechanism-policy-definitions.md` | 单一 owner；消费者只带路径（V-2） |
| `owns[]` | 七个事实组（OD-01 ①–⑦） | 每组在正文有落点章节（V-3） |
| `does_not_own[]` | ≥ 4 条，每条带 owner 路径 | 目录治理 / 机制 vs 问题 / `${SKILL_HOME}` 取值源 / 运行期根（V-4） |

- **V-1**: 英文名与中文名 MUST 逐字；`Mechanism-Policy`（半角连字符）在标题行是缺陷——字面为 en dash `–`。
- **V-2**: owner 路径之外 MUST NOT 出现第二份判据表；断言形态见 E-5 / V-13。
- **V-3**: 声明了却无落点章节 = 悬空所有权声明（判红）。
- **V-4**: `does_not_own[]` 缺任何一条 = C2 / C3 / C4 的边界没有机械落点（判红）。

## E-2 — 两层判别（Layer Judgement）

**Carrier**: owner § Terminology（判据）+ § Boundary Test（两侧成员表）
**Consumer**: `test_mechanism_policy_owner_doc.py`；SC-001 的双判定者

| 字段 | 域 | 规则 |
|---|---|---|
| `question` | 单句，形如「换掉运行环境，这段文字要不要改？」 | 二值判据，无中间档（V-5） |
| `yes_branch` | `策略 (Policy)` | 判据答「要改」 |
| `no_branch` | `机制 (Mechanism)` | 判据答「不改」 |
| `observable_directions[]` | ≥ 2 条 | 「答得出运行环境 → 策略」「答不出 → 机制」 |
| `non_deciding_factors[]` | 文件名 / 目录名 / 语言 / 篇幅 / 介质 | 判据 MUST 明写它们不参与判定（V-6） |
| `mechanism_members[]` | ≥ 7 行，每行有判据依据 | 派生而非枚举（V-7） |
| `policy_members[]` | ≥ 6 行，每行有判据依据 | 派生而非枚举（V-7） |
| `script_split` | 一句裁决 | 脚本逻辑 → 机制；参数与落点 → 策略（A4） |

- **V-5**: 判据 MUST 是二值；出现「视情况 / 综合考虑 / 视严重度」判红。
- **V-6**: 五个不参与判定因素缺一即判红（requirements § Edge Cases 跨语言、元命令模板两条依赖它）。
- **V-7**: 成员表每行 MUST 能被一个判据实例独立复算（US4 独立测试的机械前提）。

## E-3 — 误置症状（Misplacement Symptom）

**Carrier**: owner § Misplacement Symptoms
**Consumer**: `test_mechanism_policy_owner_doc.py`；元技能的判定步骤（SW-01 / SW-02）在运行时点名症状

| 字段 | 域 | 规则 |
|---|---|---|
| `kind` | `mechanism-in-policy` / `policy-in-mechanism` | 两类，封闭（V-8） |
| `observable[]` | ≥ 2 条/类 | 可观测表现（能 grep 到的形态） |
| `signature` | ≥ 1 条可机械识别的形态 | 如绝对路径 / 盘符路径 / 用户目录名（V-9） |
| `correction_side` | `skill-asset` / `runtime-environment` | 改正方向指向另一侧（V-10） |

- **V-8**: 两类 MUST 都在；只有策略侧一类 = US1 场景 2 未覆盖。
- **V-9**: `signature` 是元技能**可定位判定**的最小依据；没有签名，判定无法点名行。
- **V-10**: `correction_side` MUST NOT 等于「本侧」（改正方向指向对侧）。

## E-4 — 归档规则（Archival Rule）

**Carrier**: owner § Archival Rules
**Consumer**: `test_mechanism_policy_ownership.py`

| 字段 | 域 | 规则 |
|---|---|---|
| `mechanism_target` | 技能资产（`SKILL_HOME` 侧：`SKILL.md` / `references/` / `scripts/` / `assets/`） | 机制落地根 |
| `policy_targets[]` | 运行环境（`SKILL_WORKDIR` 侧 / 用户指定目录 / cwd / `.specify/` 侧） | 策略落地根，至少四项（V-11） |
| `directory_governance_ref` | `shared/guidelines/directory-governance.md` | 引用而非复制（V-12；FR-004） |
| `no_new_roots` | 布尔，恒 `true` | 本特性不新增目录根 / 环境变量 / 配置键（A3） |

- **V-11**: 四个策略落点缺一 = 与 requirements FR-004 的枚举不一致（判红）。
- **V-12**: owner MUST NOT 含目录命名正则、注册义务句或运行期根清单字面——那三项归 `directory-governance.md` § 1 / § 3 / § 5；出现即复制（判红）。
- **V-13**: owner MUST NOT 含 `${SKILL_HOME}` / `${SKILL_WORKDIR}` 的**定义**（只允许引用 `skills/external/create-skills/SKILL.md` § 2）。

## E-5 — 消费侧提示形态（Missing-Policy Prompt）

**Carrier**: owner § Consumption Contract
**Consumer**: `test_mechanism_policy_owner_doc.py`、`test_mechanism_policy_missing_policy.py`；SW-04 的接线点

| 字段 | 域 | 规则 |
|---|---|---|
| `required_fields[]` | 恰 3 项 | `missing_item` / `why_now` / `how_to_supply`（V-14） |
| `kind` | `policy-missing` / `environment-error` | 封闭二值，措辞与后续动作可区分（V-15） |
| `check_order` | `read → judge → stop` | 任何副作用之前；检查自身零写入（V-16） |
| `forbidden_substitutes[]` | 「机制默认值顶替」「静默选默认落点（含 cwd）」 | 两条禁止（V-17） |
| `standalone_variant` | 候选集合收窄的说明 | 无 `.specify/` 时形态不变、候选变少 |

- **V-14**: 三要件缺一 = FR-006 未落地；多出第四要件 = 形态不唯一（也会判红，因为「统一形态」的前提是字段数固定）。
- **V-15**: 两类合并成一条措辞 = FR-007 未落地；两类 MUST 各自给出一个示例句。
- **V-16**: `check_order` MUST 写成三步；`judge` 步 MUST NOT 包含写动作（写文件 / 建目录 / 删改）。
- **V-17**: 禁止项 MUST 逐字出现（它们是 FR-005 的可判形态）。

## E-6 — 元层成员资格（Meta-layer Membership）

**Carrier**: owner § Meta-layer Membership（成员表）；`/speckit.skills` 的命令面接线位同一章节声明
**Consumer**: `test_mechanism_policy_owner_doc.py`（表形态）、`test_mechanism_policy_guard.py`（与允许差异集交叉）、`test_mechanism_policy_skill_wiring.py`（included 行各有接线）

| 字段 | 域 | 规则 |
|---|---|---|
| `predicate` | 字面逐字同 requirements § Constraints C1 | 唯一判定依据（V-18） |
| `members[].flow` | 技能或命令名 | 封闭集见下 |
| `members[].output` | 该流程的产出（一句话） | 判定依据 |
| `members[].verdict` | `included` / `excluded` / `command-surface` | 封闭三值 |
| `members[].reason` | 命中谓词的一句理由 | included 也可写理由（为何命中） |

**封闭成员表**（本特性的裁定结果，`included` 恰 3 / `excluded` 恰 2 / `command-surface` 恰 1）：

| 流程 | verdict | 依据 |
|---|---|---|
| `create-skills` | `included` | 产出新技能 |
| `improve-skills` | `included` | 产出变更后的技能 |
| `merge-skills` | `included` | 产出合并后的目标技能并下线源技能 |
| `coaching-skills` | `excluded` | 产出是观察与计划，不改写受训技能 |
| `run-skills` | `excluded` | 产出是目标技能按其自身流程执行，不改变任何技能定义/行为 |
| `/speckit.skills` | `command-surface` | 转发给 included 成员；只声明接线位 |

- **V-18**: `predicate` 与 C1 逐字不一致 = 判定依据漂移（判红）；谓词若改动，全表 MUST 重算（C1 末句），本文件与 owner 同趟更新。
- **V-19**: `included` 集合 MUST NOT 与 GM-03 允许差异集的**流程子集**不一致（`test_mechanism_policy_guard.py` 交叉断言）。
- **V-20**: `excluded` 行 MUST 各写理由，且 `coaching-skills` 的理由 MUST 含「真实改写仍经 `improve-skills`」的通道句（FR-014）。

## E-7 — 判定样本（Decidability Sample）

**Carrier**: owner § Worked Examples（附录）
**Consumer**: `test_mechanism_policy_decidability.py`；SC-001 双判定者协议、SC-005 读者作答

| 字段 | 域 | 规则 |
|---|---|---|
| `sample_id` | `S-01` … | 稳定 id，题集内唯一 |
| `content` | 1–3 行 | 待判定内容 |
| `answer` | `机制` / `策略` / `待澄清` | 封闭三值（V-21） |
| `basis` | 一句话，只能引用 E-2 判据 | 不得引入新规则 |
| `covers` | 实体类标签 | 至少覆盖机制侧 / 策略侧 / 两类误置 / 边界情形 |

- **V-21**: `answer` 出现第四值（如「视情况」）= 判据不可判定，判红；`待澄清` 只用于 requirements § Edge Cases 第一条的「拆不开」情形，且 MUST 附「为什么两个方向都成立」一句。
- **题集规模**: ≥ 12 条；`边界情形` 至少含：脚本 `--out <dir>`（策略）、模板标题（机制）、`.specify/` 笔记里的算法分支（机制）、一句双语表述（不构成机制内容）。

## E-8 — 技能引用（Skill Reference）

**Carrier**: `shared/definitions/skill-reference-definitions.md` § Accepted forms（框架源；镜像 `.specify/shared/definitions/` 由 `sync-mirrors.py` 生成，MUST NOT 手改）
**Consumer**: `tests/contract/test_skill_reference_grammar.py`（字段域与 form 集合的字面断言）、`test_skill_reference_consumers.py`（源路径坐标与接线条数）；五个消费方（SR-01…SR-06）的输入段

| 字段 | 域 | 规则 |
|---|---|---|
| `raw` | 非空字符串（允许首尾空白与一层包裹引号） | 逐字保留，作为**成对报告**的原始半（V-22；FR-025） |
| `form` | 封闭接受形式之一（见下表） | 每个形式一个示例 + 一句含义，形式集合只由 owner 修订增长（V-23；FR-020） |
| `labelled_prefix` | `skill:`（[[STR-005]]），至多一层 | 剥一次，不递归（V-24） |
| `symbol_prefix` | `/` 或 `@`，至多一段 | `@/` 组合也算**一段**（V-24） |
| `suffix` | `SKILL.md` / 尾 `/` | 剥一次；`.md`（非 `SKILL.md`）**不剥**（V-25） |
| `normalized` | 名称 或 路径 | MUST 不含已剥掉的前缀/后缀（V-26；FR-021） |

**封闭接受形式集合**（六项，与 fixture 的 `forms` 对象一一对应）：

| form | 示例 | 含义 |
|---|---|---|
| bare name | `improve-skills` | 技能目录名 / frontmatter `name` |
| slash reference | `/improve-skills` | **斜杠命令面**标记；不是「直接执行它」的指令（FR-023(a)） |
| at reference | `@merge-skills` | At 提及面 |
| labelled reference | `skill:merge-skills` | 带标签（[[STR-005]]）的同义写法 |
| canonical path | `skills/external/merge-skills/SKILL.md` | 以 `SKILL.md` 结尾的路径 |
| directory path | `skills/external/merge-skills`（可带尾 `/`） | 技能目录路径 |

- **V-22**: `raw` MUST 与 `normalized` 成对出现在消费方报告里，缺一即「未报告」（FR-025）；只报 `normalized` 判红。
- **V-23**: 六个形式缺一即判红；新增形式**必须**走一次 owner 修订，MUST NOT 由某个消费方就地扩展（FR-019 唯一 owner + FR-029）。
- **V-24**: 标签与前缀各**至多剥一层**；`skill:skill:x`、`@@x` 属失败面而非「多剥几次」。
- **V-25**: `SKILL.md` 与尾 `/` 剥一次；`.md` 不剥——`my-draft.md` 的分歧（fixture R14）由此单点收敛到一条规则，不再是两个读法（见 § SM-3 与 plan.md § D12 residue 表）。
- **V-26**: `normalized` 里出现被剥掉的前缀/后缀 = 把剥离留给下游再猜（FR-021 反例），判红。

## E-9 — 归一化结果（Normalized Reference）

**Carrier**: owner § Normalization + § Failure semantics
**Consumer**: `tests/contract/skill_reference_matrix.py` + `tests/contract/test_skill_reference_matrix.py`（读 `tests/fixtures/skill-reference/normalization-matrix.json`）；SC-006 的第三方复算

| 字段 | 域 | 规则 |
|---|---|---|
| `outcome` | `command-surface` / `skill` / `failure` | **封闭三值**，无第四值（V-27；FR-030） |
| `payload` | `command-surface` → 命令名；`skill` → 名称 或 路径+层级；`failure` → 失败类 + 必需报告项 | 与 `outcome` 一一对应（V-28） |
| `by_ladder` | `skill` 的名字通道才需要 | 名字落成路径是**位置阶梯**的事（FR-022），不是归一化的第二个结果（V-29） |
| `case_pass` | `exact` / `insensitive` | 先精确、零命中才不分大小写；不分大小写多命中即失败（V-30） |

**确定性管线（NP-1 … NP-8，顺序不可交换）**——这是 clarify 裁决 (1) 的归一化顺序的字段化投影：

| 步 | 动作 | 失败面 |
|---|---|---|
| NP-1 | 形态判定：是不是一次调用（`/speckit.*` 等 cli 形态先分流） | 不进入技能解析 |
| NP-2 | 去首尾空白 + 去一层配对包裹引号 | 未配对引号 → 失败 |
| NP-3 | 剥一段 `skill:` 标签 | — |
| NP-4 | 剥一段 `@` 或 `/` 前缀（含 `@/name`，剥后不得只剩空串） | — |
| NP-5 | 剥 `SKILL.md` 或尾 `/`（`.md` 不剥） | — |
| NP-6 | 通道判定：含 `/` → path 通道，否则 name 通道 | 残留可疑形态（`..` 相对片段）→ 失败 |
| NP-7 | 命中判定（name 通道按 E-8 case 规则；path 通道对位置阶梯） | 零命中 / 越界 / 不可读 / 双层同名 → 失败（E-10） |
| NP-8 | 输出恰三值之一 + 与原始引用成对报告 | 第四值 = 判红 |

- **V-27**: 出现三值之外的任何结果（例如「原样返回，下游再猜」）= FR-030 被破，判红。R10 的读数（`classes=2`、`closed_three_way=False`）是这条规则的**反例证据**：现顺序连失败都表达不出来。
- **V-28**: `command-surface` 的 `payload` 是**命令名**（不是技能路径）；`skill` 的 `payload` 是名称或路径+层级；`failure` 的 `payload` 必须含该失败类的**全部必需报告项**（E-10）。
- **V-29**: 把「这个标识该在哪个目录找」写进归一化结果 = 内联位置阶梯（破 FR-022），判红；`by_ladder` 只允许出现一个**指向**该阶梯的引用。
- **V-30**: `case_pass=insensitive` 且命中 ≥ 2 = 「两个不同层同名」失败，MUST NOT 任选其一（clarify 裁决 (1) 条目 9）。
- **NP 顺序不变量**: NP-3/NP-4 MUST 先于 NP-6。R05（`speckit.skills`）与 R06（`speckit.skills/SKILL.md`）今天分属 NAME/PATH，就是 NP-6 抢在 NP-5 之前的后果；换序后两者**都**归 `command-surface`（SU-03 的闭合方式）。

## E-10 — 失败类（Failure Class）

**Carrier**: owner § Failure semantics（四行表）
**Consumer**: `test_skill_reference_grammar.py`（表形态 + 逐项报告项）、`test_skill_reference_failures.py`（四类互斥与成对报告）、`test_skill_reference_matrix.py`（失败行复算）

| failure class | 条件 | 必需报告项 |
|---|---|---|
| zero-hit | 归一化后无命中 | 原始输入、归一化形、已搜索的全部坐标 |
| out-of-ladder | 路径落在已知位置之外 | 该路径 + 已知位置集 |
| unreadable | 目录无可读 `SKILL.md` 或 frontmatter 无效 | 路径 + 缺陷 |
| dual-layer | 两个**不同层**同名命中 | 两个候选路径（MUST NOT 挑最近的一个） |

- **V-31**: 四类缺一即判红；每类的**必需报告项**必须逐项可核对（不是「报个错」）。
- **V-32**: 失败 MUST 关闭（停住），MUST NOT 降级为「先试一个」；consumer 侧发现「先试」措辞即判红（FR-024 末句）。
- **V-33**: 「同名两处」只在**不同层**时才算两处；dev 规范层与其安装镜像的同名命中算一处（FR-023(c)）。因此 `dual-layer` 断言 MUST 用两个不同层的 fixture 行，不能拿「源 + 镜像」当反例。


## 状态转移

**SM-1 — 作者侧判定（元技能内）**

| From | To | 触发 | 产物 |
|---|---|---|---|
| `pending` | `pass` | 两侧均无 `observable` 命中 | 完成报告不含该条 finding |
| `pending` | `misplaced` | 任一侧 `signature` 命中 | 一条可定位 finding（文件 + 位置 + 改正方向） |
| `misplaced` | `pass` | 改正后复查 | 复查记录（同一判定，不得换判据） |
| `pending` | `undecided` | 内容拆不开（两个方向都成立） | 交回用户裁决；MUST NOT 任选一边 |

不变量：`pass` 必须有判定记录（判定不是默认值）；`undecided` MUST NOT 被当作 `pass`。

**SM-2 — 消费侧检查（执行前）**

| From | To | 触发 | 产物 |
|---|---|---|---|
| `checking` | `ready` | 策略齐备且可取值 | 继续执行 |
| `checking` | `ask` | 策略缺失或含糊 | 统一提示（E-5 三要件），零写入 |
| `checking` | `error` | 策略给了但取不到 | 环境错误措辞 + 恢复路径；零写入 |
| `ask` / `error` | `checking` | 用户补齐策略 | 重新检查，MUST NOT 缓存旧的 `ask` 结论 |

不变量：从 `checking` 出发的两条停止边 MUST NOT 留下任何副作用；`error` MUST NOT 退化成为 `ask`（两者措辞与后续动作不同）。

**SM-3 — 引用归一化（元技能内部，NP-1 … NP-8）**

| From | To | 触发 | 产物 |
|---|---|---|---|
| `received` | `command-surface` | NP-8 判定归一化名落在 `/speckit.*` 命名空间 | 命令面报告（指向该命令），**不进技能解析** |
| `received` | `skill` | NP-7 命中且 NP-8 判定为技能 | 名称（+ 名称通道时交给位置阶梯）+ 成对报告 |
| `received` | `failure` | NP-6/NP-7 命中任一失败类 | 失败类 + 该类的全部必需报告项；**停住** |
| `failure` | `received` | 用户改写成另一个可解析的引用 | 重新归一化，MUST NOT 复用上一次的失败结论 |

不变量：从 `received` 出发恰有**三条**出边，没有第四条（FR-030）；`skill` MUST NOT 携带「该去哪个目录找」的结论（那是位置阶梯的产物，FR-022）；`failure` MUST NOT 有「先试一个」的恢复边（V-32）。

## GM-03 — 允许差异集（SC-003 封闭集声明，供给 `contracts/guard-and-measurement.contract.md` 要件 3）

| # | 路径 | 类别 | 属比较单元 |
|---|---|---|---|
| 1 | `skills/external/create-skills/SKILL.md` | 改写（SW-01；能力二为接线 SR-02） | 是 |
| 2 | `skills/external/create-skills/references/mechanism-policy-check.md` | 新增（SW-01） | 是 |
| 3 | `skills/external/improve-skills/SKILL.md` | 改写（SW-02；能力二为接线 SR-03） | 是 |
| 4 | `skills/external/improve-skills/references/loop-playbook.md` | 改写（SW-02 批量说明） | 是 |
| 5 | `skills/external/merge-skills/SKILL.md` | 改写（SW-03；能力二为接线 SR-04） | 是 |
| 6 | `skills/external/merge-skills/references/provenance-record.md` | 改写（SW-03） | 是 |
| 7 | `skills/external/coaching-skills/SKILL.md` | 改写（SR-06，仅引用接线） | 是 |
| 8 | `skills/internal/run-skills/SKILL.md` | 改写（SR-01，仅引用接线） | 是 |
| 9 | `tests/fixtures/skill-reference/normalization-matrix.json` | 新增（SC-006 矩阵，D13） | 否（`tests/` 不在单元内） |
| 10 | `tests/contract/test_mechanism_policy_owner_doc.py` | 新增 | 否 |
| 11 | `tests/contract/test_mechanism_policy_ownership.py` | 新增 | 否 |
| 12 | `tests/contract/test_mechanism_policy_skill_wiring.py` | 新增 | 否 |
| 13 | `tests/contract/test_mechanism_policy_guard.py` | 新增 | 否 |
| 14 | `tests/contract/test_mechanism_policy_missing_policy.py` | 新增 | 否 |
| 15 | `tests/contract/test_mechanism_policy_decidability.py` | 新增 | 否 |
| 16 | `tests/contract/skill_reference_matrix.py` | 新增（测试辅助，非门禁脚本） | 否 |
| 17 | `tests/contract/test_skill_reference_matrix.py` | 新增（SC-006） | 否 |
| 18 | `tests/contract/{test_skill_reference_grammar,test_skill_reference_consumers,test_skill_reference_command_surface,test_skill_reference_failures}.py` | 新增（GR 形态、SC-007、SC-008、SC-009） | 否 |

登记表在**比较单元内**的条目恰为第 1–8 行（**1 条新增 + 7 条改写**：新增只有第 2 行的 `references/mechanism-policy-check.md`，其余七行都是改写），第 9–18 行是落在比较单元之外（`tests/`）的新增路径，列出是为了让「新增路径」一侧也可逐条核对，它们不参与字节相等断言。**本条与第 9–18 行的条数以本表行为准**：任何引用本节的地方 MUST NOT 手抄一个与表不符的总数（M3 repair 2026-11-05 改，原正文「2 新增 + 6 改写」与行不符）。第 18 行登记的是**一组**文件（五个引用侧模块中的四个 pytest 模块；第五个 `test_skill_reference_matrix.py` 已在第 17 行单列），契约侧只陈述「技能引用测试组」这一数，路径细节以本表与 plan.md § Project Structure 为准。

**结构不变量**（三条）：
1. `included` 成员的技能目录 = 允许差异集中 `skills/external/<member>/` 前缀的路径集合的父目录集合（V-19）。
2. `excluded` 成员（`coaching-skills`、`run-skills`）的**行为**零变化，但**引用坐标**被改写（第 7、8 行）：它们仍在允许集里，因此逐字节相等断言对它们**失效**——补偿判据是 SW-05 的「机制/策略判定字面零命中」（且 SW-05 本身按 SU-01 收紧为可判形态）+ 接线行只声明参数（V-34）。
3. 能力一的允许集与能力二的允许集**共用同一张表**：一张表、一个分母，MUST NOT 出现「按能力各开一张允许集」的第二份（SC-003 的分母唯一）。

- **V-34**: `coaching-skills` / `run-skills` 的改写 MUST 限于引用串改写与「按 owner 归一化并披露」的接线句；出现判据表 / 症状表 / 失败表的任何一行即判红（C9：两个能力的 owner 互不复制）。

## 实体关系

```
E-1 Principle ──owns──▶ E-2 Layer Judgement ──derives──▶ E-4 Archival Rule
     │                        │
     │                        └──fails-as──▶ E-3 Misplacement Symptom ──checked-by──▶ (元技能 SW-01/02/03)
     ├──owns──▶ E-5 Missing-Policy Prompt ──consumed-by──▶ (元技能/元命令 SW-04)
     ├──owns──▶ E-6 Membership ──cross-checked-with──▶ GM-03 允许差异集 (SC-003)
     └──owns──▶ E-7 Decidability Sample ──measures──▶ SC-001 / SC-005

E-8 Skill Reference ──normalized-by──▶ E-9 Normalized Reference ──three-way──┬─▶ command-surface
     │                          │                                             ├─▶ skill ──(position ladder, FR-022)──▶ 路径
     │                          └─────────fails-as──▶ E-10 Failure Class ─────┴─▶ failure（关闭，无降级边）
     └──cited-by──▶ (五个消费方 SR-01…SR-06，各自只声明自己的参数)

E-7 (能力一) ──与── E-9 (能力二) 共享 C1 的范围判据，但两份 owner MUST NOT 互相复制（C9）
```
