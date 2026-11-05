# Data Model — 082 机制/策略分离（Mechanism–Policy Separation）

**Owner boundary**: 本文件定义本特性引入的**实体、字段、校验规则与状态转移**；「两层是什么、怎么判」的**语义权威**是 `shared/definitions/mechanism-policy-definitions.md`（下称 owner，[[STR-003]]）。两者冲突时 owner 胜，本文件为陈旧。

**投影面**：本文件是 owner 的**形态投影**——可以收窄 owner 的值域，MUST NOT 扩大；它不复述 owner 的判据表、症状表或提示骨架，只把它们变成可断言的字段。

**Census**: 7 个实体（E-1 … E-7）、21 条校验规则（V-1 … V-21）、1 个封闭谓词（C1）、1 个封闭成员表（3 / 2 / 1）、1 个封闭允许差异集（9 条路径登记，其中属比较单元者 6）、2 条状态转移（SM-1 作者侧判定、SM-2 消费侧检查）。

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

## GM-03 — 允许差异集（SC-003 封闭集声明，供给 `contracts/guard-and-measurement.contract.md` 要件 3）

| # | 路径 | 类别 | 属比较单元 |
|---|---|---|---|
| 1 | `skills/external/create-skills/SKILL.md` | 改写（SW-01） | 是 |
| 2 | `skills/external/create-skills/references/mechanism-policy-check.md` | 新增（SW-01） | 是 |
| 3 | `skills/external/improve-skills/SKILL.md` | 改写（SW-02） | 是 |
| 4 | `skills/external/improve-skills/references/loop-playbook.md` | 改写（SW-02 批量说明） | 是 |
| 5 | `skills/external/merge-skills/SKILL.md` | 改写（SW-03） | 是 |
| 6 | `skills/external/merge-skills/references/provenance-record.md` | 改写（SW-03） | 是 |
| 7 | `tests/contract/test_mechanism_policy_owner_doc.py` | 新增 | 否（`tests/` 不在单元内） |
| 8 | `tests/contract/test_mechanism_policy_ownership.py` | 新增 | 否 |
| 9 | `tests/contract/test_mechanism_policy_skill_wiring.py` | 新增 | 否 |
| 10 | `tests/contract/test_mechanism_policy_guard.py` | 新增 | 否 |
| 11 | `tests/contract/test_mechanism_policy_missing_policy.py` | 新增 | 否 |
| 12 | `tests/contract/test_mechanism_policy_decidability.py` | 新增 | 否 |

登记表在**比较单元内**的条目恰为第 1–6 行（6 条：2 条新增 + 4 条改写），`contracts/guard-and-measurement.contract.md` GM-03 只陈述这个数，MUST NOT 再逐条列举路径——本表是允许差异集路径的唯一落点。第 7–12 行是同一实现期落在比较单元之外的新增路径，列出是为了让「新增路径」一侧也可逐条核对，它们不参与字节相等断言。

**结构不变量**（两条）：
1. `included` 成员的技能目录 = 允许差异集中 `skills/external/<member>/` 前缀的路径集合的父目录集合（V-19）。
2. `excluded` 成员（`coaching-skills`、`run-skills`）在允许集里 MUST 零命中——它们的每一条路径都落在补集，因此逐字节断言覆盖它们。

## 实体关系

```
E-1 Principle ──owns──▶ E-2 Layer Judgement ──derives──▶ E-4 Archival Rule
     │                        │
     │                        └──fails-as──▶ E-3 Misplacement Symptom ──checked-by──▶ (元技能 SW-01/02/03)
     ├──owns──▶ E-5 Missing-Policy Prompt ──consumed-by──▶ (元技能/元命令 SW-04)
     ├──owns──▶ E-6 Membership ──cross-checked-with──▶ GM-03 允许差异集 (SC-003)
     └──owns──▶ E-7 Decidability Sample ──measures──▶ SC-001 / SC-005
```
