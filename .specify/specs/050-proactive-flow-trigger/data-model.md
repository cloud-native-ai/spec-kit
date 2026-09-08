# Data Model — 主动触发机制(Proactive Flow Trigger)

**Requirement**: `050-proactive-flow-trigger` → Feature 050
**Date**: 2026-09-07
**Source**: [requirements.md](./requirements.md) § Key Entities(7 实体)· [plan.md](./plan.md) § D-7 / D-8

本文件定义 7 个实体、2 个状态机、受控情境词表初版、探测升级判据表与校验规则。字段命名一律 **camelCase**(承 `derive-utils.py` 信封范式)。

---

## 存储布局

```text
.specify/memory/trigger/
├── index.json          # git 跟踪 — 配置 + 规则集 + 晋升聚合态 + 调优提议(每会话变数次)
└── telemetry.jsonl     # git 忽略 — 每回合遥测,一行一 JSON 对象(每回合变一次,有保留窗口、可轮转)

templates/proactive-trigger-seed.json   # 出厂种子(随包分发,携带 provenance;+ .specify/templates/ 镜像)
```

跟踪边界按**变动频率**切分(plan.md D-8):`index.json` 承载需跨 clone 存活的用户调优(同 `.specify/git-workflow.md`、`.specify/docs/target-structure.md` 的持久项目契约定位);`telemetry.jsonl` 是高频 ephemeral churn,承 `implement-loop.local.md` 先例入 gitignore。轮转只作用于后者。

---

## E1 情境身份 (Situation Identity)

受控词表中的一个**命名取值**,是"同一情境"的判定单位,因而也是 E5 连续计数良定义的前提(FR-023)。

| Field | Type | 说明 |
|---|---|---|
| `id` | string | 封闭词表键,`^s[0-9]{2}$`(如 `s01`);稳定不复用,退役后不重编号 |
| `name` | string | 人类可读名(如 `requirements-unclear`) |
| `stage` | enum | 特性生命周期阶段,见 §受控词表 |
| `signals` | string[] | 待处理信号集(排序后比较),见 §受控词表 |
| `match` | object | 判定谓词:`{ stage: <enum>, signalsAll: string[], signalsAny: string[] }` — 引擎按此确定性解析 |

**校验规则**
- V1.1 `id` 在全词表内唯一;新增只经用户批准通道(FR-016 / FR-023),引擎 MUST NOT 自行造词。
- V1.2 `stage` 与 `signals` 的每个取值 MUST 属封闭枚举;越界即 `EXIT_INVALID(4)`。
- V1.3 同一 `(stage, signalsAll)` 组合 MUST NOT 被两个 `id` 同时声明(否则身份不唯一,计数歧义)。
- V1.4 **身份 ≠ 快照**:身份是粗粒度可复现标签;某次评估的 `snapshot`(摘要级证据留痕)挂在 E3 上,MUST NOT 参与身份比较——否则退化为制品状态指纹反模式(FR-023 / SC-014)。
- V1.5 **匹配谓词语义**:`match.signalsAll` 的每个信号都 MUST 出现在调用方传入的 `--signal` 集合中;`match.signalsAny` 非空时其**至少一个** MUST 出现,为空(或缺省)时表示无附加要求。`match.stage` MUST 与 `--stage` 相等。三者同时满足才算命中。
- V1.6 **最具体优先(确定性消歧)**:一次评估可能命中多个情境(子集关系,如 `s06.signalsAll = {open-tasks} ⊂ s05.signalsAll = {open-tasks, checklist-absent}`)。解析 MUST 取 `signalsAll` **基数最大**者为唯一 `situationId`;基数相同则取 `id` 字典序最小者。该规则使 C-12 的"唯一身份"在存在子集关系时仍成立,且无需引入枚举外的负信号。命中情境后再由 E2.`priority` 在该情境的多条规则间收敛为一条建议(FR-008)。

---

## E2 建议规则 (Suggestion Rule)

一条(情境身份 → 目标流程)映射,触发逻辑的最小可优化单元(FR-014)。种子规则与学习规则**同构**,仅 `origin` 与可覆盖性有别(FR-022)。

| Field | Type | 说明 |
|---|---|---|
| `ruleId` | string | `^r-[0-9]{3}$`,项目内单调发放,不复用 |
| `situationId` | string | 引用 E1.`id` |
| `flow` | string | 目标流程的调用名(如 `/speckit.clarify`)或技能名 |
| `invocation` | string | **确切可复制的调用形式**(FR-006),含必要参数占位 |
| `rationale` | string | 用途说明(呈现给用户的一行文案素材) |
| `confirmationClass` | enum | `reversible` \| `destructive` — **数据,不由引擎计算**;判据归 `shared/guidelines/confirmation-gates.md`,存疑从严取 `destructive`(FR-011) |
| `origin` | enum | `seed` \| `learned` |
| `provenance` | object? | 仅 `origin=seed`:`{ file, anchorKind, anchor, quote }`。`anchorKind ∈ {handoffs, owning-section}`(FR-022 订正后的两类派生来源);`file` 为相对仓库根路径;`quote` 为逐字引文。`handoffs` 类的 `quote` 必须落在该文件的 `## Handoffs` 段内,`owning-section` 类落在 `anchor` 指名的段落内。漂移检出的依据,见 `contracts/seed-derivation.md` |
| `notes` | string? | 可选,仅用于记**分类判据出处**(如某规则为何归 `destructive`),以路径引用 `shared/guidelines/confirmation-gates.md`,MUST NOT 复述其分类表(`seed-derivation.md` C-9) |
| `state` | enum | `active` \| `suppressed` \| `promoted`,见 §状态机 SM-1 |
| `priority` | int | 多规则同时命中时的收敛序(FR-008:收敛为一条最高优先建议) |
| `promotion` | object | E5 内嵌 |
| `stats` | object | `{ hits, accepted, declined, ignored, lastSeen }` — 调优证据来源(FR-015) |
| `tuning` | object? | `{ suppressedBy, ratifiedAt, evidenceRef }` — 用户调优痕迹;**优先级高于同 `ruleId` 的种子更新**(FR-022) |

**校验规则**
- V2.1 `confirmationClass=destructive` 的规则 MUST 恒 `state ∈ {active, suppressed}`,`promotion.promoted` MUST 恒 `false`(FR-011,零容忍,SC-005)。
- V2.2 `origin=seed` MUST 携带 `provenance`(四键齐备,`anchorKind=handoffs` 时 `quote` 须在该文件的 `## Handoffs` 段内、`owning-section` 时须在 `anchor` 指名段落内);`origin=learned` MUST NOT 携带。
- V2.3 用户调优不可被种子回退:合并种子更新时,凡 `tuning` 非空的 `ruleId`,其 `state` / `priority` / `confirmationClass` 以本地值为准,仅 `rationale` / `invocation` 可从种子刷新(且刷新须在 `notes[]` 留痕)。
- V2.4 同一 `situationId` 下 `flow` MUST 唯一(避免同情境两条指向同一流程的规则重复计数)。
- V2.5 **标识符文法(封闭,机械可断言)**:`ruleId` 匹配 `^r-[0-9]{3}$`;`situationId` 匹配 `^s[0-9]{2}$`;`eventId` 匹配 `^[0-9]{8}T[0-9]{6}Z-[0-9]{2}$`;`turnId` 匹配 `^<sessionId>-[0-9]{2,4}$` 且 `sessionId` 匹配 `^s[0-9A-Za-z-]{1,32}$`;`proposalId` 匹配 `^p-[0-9]{3}$`。越界一律 `EXIT_INVALID(4)`;`quickstart.md` 中出现的每个标识符实参都 MUST 满足对应正则(由 `trigger-engine.md` C-11 钉住)。

---

## E3 建议事件 (Suggestion Event)

一次建议的发生记录,是**计数晋升与规则优化的唯一证据来源**(FR-009①)。

| Field | Type | 说明 |
|---|---|---|
| `eventId` | string | `<UTC-compact>-<seq>`(如 `20260907T142530Z-01`) |
| `ruleId` | string | 命中的规则 |
| `situationId` | string | 解析出的情境身份 |
| `snapshot` | string | **摘要级**证据留痕(≤ 200 字符),MUST NOT 含制品原文(FR-005) |
| `response` | enum | `accepted` \| `declined` \| `ignored` |
| `escalated` | bool | 该次评估是否升级到了确定性探测 |
| `created` | string | ISO-8601 UTC |

**校验规则**
- V3.1 `response=accepted` → 对应规则 `promotion.consecutive += 1`;达 `threshold` 且 `confirmationClass=reversible` → `state=promoted`(FR-010)。
- V3.2 `response ∈ {declined, ignored}` → `promotion.consecutive = 0`(**一次拒绝即重置**,R2-Q3)。`declined` 与 `ignored` 在 `stats` 中分列(调优证据需要区分"明确不要"与"没理会")。
- V3.3 `snapshot` 超 200 字符即 `EXIT_INVALID(4)`——把"摘要级"钉成机械可断言的约束。
- V3.4 **字段来源(关联规则)**:`record` 的 flag 只有 `--rule` 与 `--response`,故 E3 的 `situationId` / `snapshot` / `escalated` / `created` MUST 由引擎从 E6.`lastSuggestion`(同 `--session` 下最近一次 `assess` 的结果)关联填充;若该会话无在先 `assess`,则 `EXIT_INPUT_ERROR(2)` 且 `errors[]` 记 `no-prior-assess`,MUST NOT 写入半截事件。该规则使 `quickstart.md` 场景 4 的"先 assess 后 record"序列成为**必需**而非可选。

---

## E4 回合遥测 (Turn Telemetry)

**每个用户回合**一行,无论该回合是否产出建议(FR-009②)。是 SC-011 / SC-012 的唯一分母来源。落 `telemetry.jsonl`,一行一对象。

| Field | Type | 说明 |
|---|---|---|
| `turnId` | string | 语法见 V2.5(`^<sessionId>-[0-9]{2,4}$`) |
| `assessed` | bool | 该回合是否执行了评估。**结构上恒为 `true`** —— 遥测行只由 `assess` 写入,故本字段无法证明"agent 跳过了某回合的评估";它的作用是显式记录该不变量、并在未来若引入其他写入方时保留判别位(见 V4.5) |
| `escalated` | bool | 是否升级探测(SC-011 分子) |
| `suggested` | bool | 是否产出建议 |
| `complianceDone` | bool | constitution 合规分析是否**先于**建议完成(SC-012 顺序契约)。**由 `--compliance-done` 传入**,引擎 MUST NOT 自行推断(它无法观察 agent 的推理过程);未传时默认 `false`,故 `suggested=true` 而未传该 flag 会如实报 `ordering-violation`——这是有意的:顺序契约需要调用方显式声明,而非被默认满足 |
| `visibleOutput` | bool | 本机制是否产生了用户可见输出(SC-011 静默性判据) |
| `ts` | string | ISO-8601 UTC |

**校验规则**
- V4.1 `suggested=true` MUST 蕴含 `complianceDone=true`;违反即 SC-012 失败,引擎在写入时以 `errors[]` 报出(FR-005b②)。
- V4.2 `assessed=true ∧ suggested=false` MUST 蕴含 `visibleOutput=false`(FR-005a 静默性 / SC-011)。
- V4.3 **有界(恒真不变量)**:`assess` 每次追加后 MUST 立即截断,使 `telemetry.jsonl` 行数 **恒 ≤ `config.telemetryWindow`**(默认 200)。故"超窗"不是需由 `--action rotate` 事后修复的暂态,而是任何一次调用返回后都不成立的状态;`rotate` 保留为显式/手动收缩入口(如用户调小窗口后)(FR-009a / SC-015)。
- V4.4 轮转与截断 MUST NOT 触及 `index.json`:晋升计数是 E2 内嵌的**聚合态**,不由遥测行重算(FR-009a / SC-015 零丢失)。
- V4.5 **度量边界(诚实声明)**:遥测行只由 `assess` 产生,故 SC-011 的分母是**评估调用数**而非原始用户回合数。若 agent 整回合跳过评估,该回合不留任何痕迹 —— FR-005a 的"每回合评估"义务**无法仅凭遥测证明**,须辅以会话侧观察(T050 的 dogfood 走查)。`assessed` 字段因此恒为 `true`,不作为漏评估的证据位。

---

## E5 晋升态 (Promotion State)

E2 的内嵌对象,表达规则的自动执行资格。

| Field | Type | 说明 |
|---|---|---|
| `consecutive` | int | 连续采纳计数(≥ 0) |
| `threshold` | int | 生效阈值(默认 3;解析优先级见 §配置) |
| `promoted` | bool | 是否已晋升为免确认自动执行 |
| `destructiveExempt` | bool | 恒等于 `confirmationClass=destructive`;为 `true` 时 `promoted` MUST 恒 `false`(FR-011) |
| `resetBy` | string? | 最近一次重置的 `eventId`(可回查) |
| `userResetAt` | string? | 用户手动复位痕迹(FR-012) |

**状态转移**:`consecutive` 达 `threshold` ∧ ¬`destructiveExempt` → `promoted=true`;任一 `declined`/`ignored` → `consecutive=0`,`promoted=false`(降级回"只建议");用户 `--action reset` → 同前但记 `userResetAt`。

**校验规则**
- V5.1 `promoted=true` MUST 蕴含 `confirmationClass=reversible`(与 V2.1 互为正反断言:V2.1 从规则视角禁止,V5.1 从晋升态视角禁止)。
- V5.2 `consecutive` MUST ≥ 0;`consecutive < threshold` 时 `promoted` MUST 为 `false`。
- V5.3 `userResetAt` 非空时 `consecutive` MUST 为 0 且 `promoted` MUST 为 `false`(复位痕迹与计数一致,不得留下"已复位却仍晋升"的矛盾态)。
- V5.4 **阈值变更后重判**:`config --threshold` 改写阈值后,每条规则的 `promoted` MUST 按新阈值重新判定;`consecutive < 新阈值` 者回落 `false`。MUST NOT 保留旧阈值下取得的晋升资格(否则调高阈值形同无效)。

---

## E6 触发学习状态 (Trigger Learning State)

`index.json` 整体,项目本地机器维护状态(FR-013 / FR-020)。

| Field | Type | 说明 |
|---|---|---|
| `store` | string | 恒 `.specify/memory/trigger/`(自描述,承 `feedback-utils.py` index 范式) |
| `schemaVersion` | int | 不兼容即降级为"只建议"并从零重学(FR-013),MUST NOT 中断会话 |
| `updated` | string | ISO-8601 UTC |
| `config` | object | `{ enabled: bool, threshold: int, telemetryWindow: int, probeBudgetPct: int, minSample: int }` — 默认依次为 `true / 3 / 200 / 20 / 5` |
| `situations` | E1[] | 受控词表(封闭) |
| `rules` | E2[] | 规则集(种子 + 学习) |
| `events` | E3[] | 建议事件(降序 by `created`) |
| `lastSuggestion` | object? | 按 `sessionId` 键控的最近一次 `assess` 结果:`{ sessionId, turnId, situationId, ruleId, snapshot, escalated, suggested, ts }`。两个用途:① 供 `record` 关联填充 E3 字段(V3.4);② 供**会话级重复建议抑制**——同 `sessionId` 下若 `situationId` 与 `ruleId` 均未变,`assess` MUST 返回 `payload.suppressed=true` 且 `suggestion=null`(FR-008 的"状态未变不重复产出",由 `trigger-engine.md` C-20 钉住) |
| `proposals` | object[] | 调优提议,每项键集恰为 `{ proposalId, kind, ruleId?, situationId?, evidence, state, createdAt, ratifiedAt?, appliedAt?, reason? }`;`kind ∈ {tighten, suppress, add-rule, extend-vocabulary}`;`evidence` 为 `{ metric, value, sampleSize }`;`state ∈ {proposed, ratified, applied, rejected}`(见 §状态机 SM-2)。`proposalId` 语法见 V2.5 |

**校验规则**
- V6.1 `config.enabled=false` → 引擎在 `assess` 上恒返回"无建议"且不写遥测外的任何状态;建议产出数与自动执行数均为 0(FR-018 / SC-009)。用户显式关闭 MUST 优先于框架默认,且 MUST NOT 被指令再生覆盖(状态与指令文件分离,FR-009)。
- V6.2 `config.threshold` 解析优先级:**显式 `--threshold` > 环境变量 `SPECKIT_TRIGGER_THRESHOLD` > `index.json` 存储值 > 默认 3**(与 `feedback-utils.py:resolve_threshold` 同构,FR-021)。非法环境变量值忽略并降级到下一级,不报错中断。
- V6.3 `config.threshold` 下限为 **2**:`0`/`1` 等于"首次即自动执行",破坏性豁免虽仍生效,但可逆流程零观察即自动执行不符合"稳定偏好"语义;显式拒绝并 `EXIT_USAGE(1)`(Edge Case「阈值配置为 0 或 1」的裁定)。
- V6.4 文件缺失 / JSON 不可解析 / `schemaVersion` 不兼容 → 降级为"只建议"、从零重学,退出码 `EXIT_OK(0)` 且 `warnings[]` 记 `state-unreadable`;MUST NOT 非零退出或中断会话(FR-013 / SC-010)。
- V6.5 写入一律原子:`index.json.part` + `os.replace`(承 `derive-utils.py:500–506`、`sanitize-utils.py:138–142`;**不**照 `feedback-utils.py:save_index` 的非原子写)。
- V6.6 `probeBudgetPct` 默认 20,即 SC-011 的比率上限;`--action tune` 在报告中回显实测比率与该上限的对比。
- V6.7 **会话级重复抑制(FR-008 的机制,不只是散文)**:`assess` 在解析出 `situationId` 与命中 `ruleId` 后,与该 `sessionId` 的 `lastSuggestion` 比对;两者均未变 → 返回 `payload.suppressed=true`、`suggestion=null`、遥测记 `suggested=false` / `visibleOutput=false`。`situationId` 或 `ruleId` 任一变化 → 正常产出建议并更新 `lastSuggestion`。故"状态未变不重复产出"由**情境身份的稳定性**定义,而非由回合计数定义。
- V6.9 **遥测忽略条目由引擎自维护**:`init` 与首次 `assess` MUST 确保项目忽略机制(如 `.gitignore`)含 `.specify/memory/trigger/telemetry.jsonl` 条目;`index.json` MUST NOT 被忽略(它承载需跨 clone 存活的用户调优)。该义务由 `tasks.md` T022 交付,此前无任何 V 规则或契约条款钉住(analyze N-22)。
- V6.8 `lastSuggestion` 按 `sessionId` 键控且**只保留每会话最近一条**;会话切换(新 `--session`)即视为状态可能已变,首回合不抑制。`reset --all` 与 `config --enabled false→true` MUST 清空全部 `lastSuggestion`(否则复位后首回合仍被抑制,用户看不到复位效果)。

---

## E7 主动触发点 (Proactive Trigger Point)

不是运行时数据实体,而是**制品面契约对象**——由 `contracts/trigger-section.md` 与 `contracts/discipline-doc.md` 钉住其形态。

| Attribute | 值 / 约束 |
|---|---|
| canonical 源 | `templates/instructions-template.md` 的一个新 `## ` 章节(插入 L23,紧邻 Documentation Map 常驻指令之后) |
| 字节相同镜像 | `.specify/templates/instructions-template.md` |
| 传播路径 | additive reconcile → `.specify/instructions.md` → 既有 symlink → 各 agent 必经路径。**计数口径以 `contracts/trigger-section.md` C-10 为唯一权威**(6 个 map key / 5 个去重后的声明文件 / 生成脚本共创建 8 条 symlink),本行不复述枚举 |
| 内容形态 | **摘要 + 指针**;全文归 `shared/guidelines/proactive-trigger.md`(FR-002 / Principle XIV) |
| 禁用内容 | 命令名/技能名/参数结构枚举(交引擎在运行时供给);项目专属 token(`spec-kit`、`specify-cli`、`specify_cli`、`Feature 0NN`、仓库路径);任何 `BLOCKING_PATTERNS` 字面量 |
| 开关 | 指针指向 `config.enabled`(FR-018);章节本身恒在,关闭靠状态而非删章节 |

---

## 受控词表初版(可修订数据,非契约常量 — plan.md D-10)

**生命周期阶段 `stage`(9 值,封闭)**

`no-spec` · `requirements-unclear` · `requirements-draft` · `planned` · `tasks-ready` · `implementing` · `implemented` · `review-pending` · `non-feature`

**待处理信号 `signal`(12 值,封闭)**

`needs-clarification` · `no-plan` · `no-tasks` · `open-tasks` · `deferred-tasks` · `checklist-absent` · `feedback-threshold` · `introspection-pending` · `docs-drift` · `instructions-stale` · `feature-index-absent` · `constitution-absent`

> 由 9 扩为 12(analyze 2026-09-08):新增 `checklist-absent`(s05 与 s06 的区分位)、`feature-index-absent`(s03)、`constitution-absent`(s13)。扩表理由见 §身份唯一性的三处订正。词表按 FR-023 属**可修订数据**,但扩展只经用户批准通道;本次扩展由 analyze 发现的身份冲突驱动,已记入 requirements.md `## Clarifications` 第四轮 A-Q5。

**命名情境(13 个)与种子规则映射**

**ruleId 发放规则**:种子规则按命名情境顺序发放,`r-00N` 与 `s0N` 一一配对(`r-001`↔`s01` … `r-013`↔`s13`)。该配对使 `quickstart.md` 与契约测试能以稳定 ID 引用具体规则(如场景 4 用 `r-001` 指可逆的 `/speckit.clarify`、用 `r-006` 指破坏性的 `/speckit.implement`)。学习所得规则的 ID 从 `r-014` 起在项目内单调发放,不与种子段重叠、不复用已退役 ID。

**anchorKind**:`handoffs` = 来源在该文件的 `## Handoffs` 段内;`owning-section` = 无任何 Handoffs 段点名该流程,故取拥有其触发条件的段落(FR-022 订正后的第二类来源)。下表 13 条 anchor **全部经实测核验**(对 25 个命令模板的 Handoffs 段做逐流程交叉扫描后重新定位)。

| id | stage | signalsAll | → flow | confirmationClass | anchorKind | provenance(实测核验) |
|---|---|---|---|---|---|---|
| s01 | requirements-unclear | needs-clarification | `/speckit.clarify` | reversible | handoffs | `templates/commands/requirements.md` `## Handoffs`(「If spec has `[NEEDS CLARIFICATION]` or `Related Feature: Need clarification` → `/speckit.clarify`」) |
| s02 | requirements-draft | no-plan | `/speckit.plan` | reversible | handoffs | `templates/commands/requirements.md` `## Handoffs`(「Otherwise → `/speckit.plan`」) |
| s03 | no-spec | feature-index-absent | `/speckit.feature` | reversible | handoffs | `templates/commands/requirements.md` `## Handoffs`(「recommended whenever `.specify/memory/features.md` is absent or still a placeholder」) |
| s04 | planned | no-tasks | `/speckit.tasks` | reversible | handoffs | `templates/commands/clarify.md` `## Handoffs`(「Mode B → `/speckit.tasks`」) |
| s05 | tasks-ready | open-tasks, checklist-absent | `/speckit.checklist` | reversible | handoffs | `templates/commands/tasks.md` `## Handoffs`(**改指**:原引 `checklist.md` 不成立——命令不会 handoff 给自己) |
| s06 | tasks-ready | open-tasks | `/speckit.implement` | **destructive** | handoffs | `templates/commands/checklist.md` `## Handoffs`(「Once satisfied → `/speckit.implement`」) |
| s07 | implementing | open-tasks | `/speckit.analyze` | reversible | handoffs | `templates/commands/implement.md` `## Handoffs`(**改指**:原引 `analyze.md` 不成立) |
| s08 | implemented | deferred-tasks | `/speckit.review` | reversible | handoffs | `templates/commands/implement.md` `## Handoffs`(**改指**:原引 `analyze.md` 不成立) |
| s09 | non-feature | feedback-threshold | `/speckit.feedback`(package 模式) | reversible | **owning-section** | `shared/workflow/feedback-step.md` §`Threshold prompt protocol`(L99–113:`should_prompt` 为真 → 邀请 `/speckit.feedback package`)。**无 Handoffs 来源**:交叉扫描确认 `/speckit.feedback` 不出现在任何命令模板的 Handoffs 段 |
| s10 | non-feature | introspection-pending | `/speckit.feedback`(introspect 模式) | reversible | **owning-section** | `templates/commands/feedback.md` Mode 表(L27 `introspect` → Mode 5)与 L49(「可先运行 Mode 5(`/speckit.feedback introspect`)自省再打包」) |
| s11 | non-feature | docs-drift | `/speckit.docs` | **destructive** | handoffs | `templates/commands/sanitize.md` `## Handoffs`(**改指**:原引 `docs.md:115` 不成立——该行点名的是 `/speckit.instructions`) |
| s12 | non-feature | instructions-stale | `/speckit.instructions` | reversible | handoffs | `templates/commands/docs.md` `## Handoffs`(**改指**:原引 `instructions.md` 不成立——命令不会 handoff 给自己) |
| s13 | no-spec | constitution-absent | `/speckit.constitution` | **destructive** | handoffs | `templates/commands/feature.md` `## Handoffs`(**改指**:原引 `constitution.md:178` 不成立,且 `/speckit.constitution` 在该文件中根本不出现) |

**表中省略的两列(由规则派生,撰写种子时 MUST 补全 —— `seed-derivation.md` C-8 要求 `situations[]` 携带 E1 完整形状)**:`name` = `id` 的 kebab-case 语义标签(如 `s01` → `requirements-unclear-needs-clarification`);`match.signalsAny` = **除 s05 外一律为空集**(s05 的 `signalsAny` 亦为空 —— 其区分位 `checklist-absent` 放在 `signalsAll` 中,因它是必须条件而非择一条件)。故 13 行的 `signalsAny` 全为空,`match` 完全由 `stage` + `signalsAll` 决定,这使 V1.6 的"最具体优先"只需比较 `signalsAll` 基数(analyze N-24)。

**分类说明(存疑从严,FR-011)**:`/speckit.implement` 虽以 git 可回退,但**影响面大**(批量写代码),按"存疑从严"归 `destructive` → 永不晋升;`/speckit.docs` 含搬迁/归档、`/speckit.constitution` 覆盖治理文件,直接命中 `confirmation-gates.md` 破坏性清单。其余为可逆(只读分析或新增制品)。该列是**数据**,判据归 `confirmation-gates.md`,引擎 MUST NOT 自行计算或改写。

**身份唯一性的三处订正(analyze 2026-09-08)**:

1. **删除 s14**(原 `(non-feature, ∅)` → `/speckit.skills`)。两个独立理由:① 其锚点 `skills.md:36,41` 落在 `## Handoffs` 段**之外**(在 "Step 3: Route" 内),违反 C-6;② 该处语义是「若 agent 依赖新技能」的**意图驱动**分流,不存在可由项目状态触发的"该建技能了"情境。保留它还会让 `(non-feature, ∅)` 每回合命中,与 `quickstart.md` 场景 3(20 个无关回合应零建议)直接矛盾。删除后 `(non-feature, ∅)` 不匹配任何情境 → 如实无建议(FR-008),场景 3 自洽。
2. **s03 与 s13 原同为 `(no-spec, ∅)`**,违反 V1.3 且使 C-12 的"唯一身份"不可满足。订正为各带区分信号:`s03` = `feature-index-absent`(特性注册表缺失/占位)、`s13` = `constitution-absent`(宪法缺失/占位)。两者可同时为真,此时按下方"最具体优先"规则并以 `priority` 收敛为一条建议(s13 优先——无宪法时先立宪法)。
3. **s05 与 s06 原同为 `(tasks-ready, open-tasks)`**。订正为 `s05` 多带 `checklist-absent`;二者仍是子集关系(`s06.signalsAll ⊂ s05.signalsAll`),故由 E1 的**最具体优先**解析规则消歧(见 V1.6),不引入枚举外的负信号。

**由此新增的解析规则**:见 §E1 的 V1.6(最具体优先)。

---

## 探测升级判据表(FR-005"升级判据 MUST 显式声明")

默认**不升级**:agent 只传它从环境上下文已知的粗信号,引擎不读任何文件。仅当下列条件成立时 agent 加 `--probe`,由引擎执行确定性状态探测(仍只输出摘要,不注入原文):

| # | 升级条件 | 探测内容(引擎侧,确定性) |
|---|---|---|
| P1 | 环境上下文未出现当前特性目录/分支信息 | `.specify/specs/` 下最高编号目录 + 其 `requirements.md`/`plan.md`/`tasks.md` 存在性 |
| P2 | 无法判断 requirements 是否含未决标记 | 对当前特性 `requirements.md` 做 `NEEDS CLARIFICATION` / `Need clarification` **计数**(不读全文) |
| P3 | 无法判断 tasks 完成度 | 对 `tasks.md` 做 `[ ]` / `[X]` / `[~]` **计数**(不读全文) |
| P4 | 无法判断 feedback 是否达阈值 | 调 `feedback-utils.py --action status` 取 `count_since_submission` / `threshold` / `should_prompt` |
| P5 | 无法判断指令文件是否陈旧 | `.specify/instructions.md` 与 `templates/instructions-template.md` 的 `## ` 标题集合差集 |

**约束**:探测 MUST 是计数/存在性/集合差这类固定规则判定(Program-First),MUST NOT 读入制品全文;每次升级在 E4 记 `escalated=true`;比率上限 `config.probeBudgetPct`(默认 20%,SC-011)。

---

## 状态机 SM-1:规则状态

```
                 ┌──────────────┐
   seed/learned  │    active    │  建议照常产出,需用户采纳
   ────────────► └──────┬───────┘
                        │ consecutive ≥ threshold ∧ confirmationClass=reversible
                        ▼
                 ┌──────────────┐
                 │   promoted   │  免确认自动执行 + 三段式执行报告(FR-012)
                 └──────┬───────┘
                        │ declined / ignored / 用户 reset
                        ▼
                 ┌──────────────┐        用户批准抑制(FR-016)
                 │    active    │ ◄────────────────────┐
                 └──────┬───────┘                      │
                        │ 拒绝率超阈且样本充足 → 提议   │
                        ▼                              │
                 ┌──────────────┐                      │
                 │  suppressed  │ ─────────────────────┘
                 └──────────────┘   (suppressed 不产出建议,仍留档供调优回查)
```

**不变量**:`confirmationClass=destructive` 的规则在任何路径下 MUST NOT 进入 `promoted`(V2.1 / FR-011 / SC-005 零容忍)。

## 状态机 SM-2:调优提议

```
   --action tune(证据聚合,确定性)
        │
        ▼
   ┌───────────┐   呈现给用户(候选形态,非阻塞)
   │ proposed  │ ─────────────────────────────┐
   └─────┬─────┘                              │
         │ 用户批准                            │ 用户否决 / 忽略
         ▼                                    ▼
   ┌───────────┐                        ┌───────────┐
   │ ratified  │ ── --action tune-apply │ rejected  │
   └─────┬─────┘        ► 写入规则集     └───────────┘
         ▼
   ┌───────────┐
   │  applied  │  留 evidenceRef + ratifiedAt(FR-016 可回查)
   └───────────┘
```

**小样本守卫(FR-017)**:`tune` MUST NOT 对 `stats.hits < config.minSample`(默认 5)的规则产出任何提议;该下限在报告中显式回显,防止小样本抖动。

**漏报检测(FR-015)**:`tune` 比对"用户实际手动调用的流程"(由 agent 在 `--action record-manual` 时传入)与"当回合是否产出过建议",差集即漏报情境,作为**新增规则**提议的证据。这是首轮 Q1=A(唯一通道、无确定性触发)的补偿控制。
