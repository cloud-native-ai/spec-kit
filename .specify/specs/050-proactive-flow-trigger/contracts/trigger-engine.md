# Contract: 触发引擎 trigger-utils.py (trigger-engine)

**Requirement**: `050-proactive-flow-trigger` → Feature 050
**Surface under contract**: `scripts/python/trigger-utils.py` + `.specify/scripts/python/trigger-utils.py`(**STRICT** 镜像对)
**Test file**: `tests/contract/test_trigger_engine.py`
**Clauses**: C-1 … C-23(C-19…C-23 由 analyze 2026-09-08 补,覆盖此前无机械钉桩的 FR-019 / FR-020 / FR-008 与两处可断言性缺口)
**范式来源**: `scripts/python/derive-utils.py`(最新引擎:camelCase 信封 + 原子写 + 分级退出码);阈值语义形状复用 `feedback-utils.py:101–116`(**复用范式,不复用代码** — plan.md D-6)

---

## 全局约束

| ID | Clause | Assertion |
|----|--------|-----------|
| **C-1** | stdlib only | 模块的全部 `import` 属 Python 标准库;无第三方依赖;Python ≥ 3.8 可运行 |
| **C-2** | 镜像字节相同 | `scripts/python/trigger-utils.py` 与 `.specify/scripts/python/trigger-utils.py` 字节相同;`sync-mirrors.py --check` exit 0(scripts 对为 STRICT,mirror-only 文件报 ORPHAN 并 exit 2) |
| **C-3** | 固定 JSON 信封 | 每次调用向 stdout 输出**恰好一个** JSON 对象,键集恒为:`ok`(bool)、`action`(string)、`workspaceRoot`(string)、`generatedAt`(ISO-8601 UTC)、`errors`(array)、`warnings`(array)、`semanticJudgmentPending`(array)、`notes`(array)、`payload`(object)。键名 **camelCase**;缺失或多余顶层键即违约。**注意一处有意改名**:范式来源 `derive-utils.py:349–361` 的对应键名是 `semanticChecksPending`,本契约改为 `semanticJudgmentPending` —— 因为本引擎交回 agent 的是**判断**(该不该采纳某调优、漏报情境配哪条流程),而非**待补的语义检查项**。实现时照本契约,不要照抄范式源的键名 |
| **C-4** | `--format` | `--format {text,json}`,默认 `json`;`text` 仅改变人类可读渲染,不改变退出码与错误语义 |
| **C-5** | 分级退出码 | `EXIT_OK=0`、`EXIT_USAGE=1`、`EXIT_INPUT_ERROR=2`、`EXIT_NOT_FOUND=3`、`EXIT_INVALID=4`;常量以该名称存在于模块顶层 |
| **C-6** | 原子写 | 对 `index.json` 的写入一律经 `<path>.part` + `os.replace`;进程在写入中途被终止时不留下半截 `index.json`(**不**照 `feedback-utils.py:save_index` 的非原子 `write_text`) |
| **C-7** | workspace-root 解析优先级 | 显式 `--workspace` > 引擎自定位(`*/.specify/scripts/` 上溯)> 最近的含 `.specify/` 的 CWD 祖先 > CWD |
| **C-8** | 状态不可读时降级而非失败 | `index.json` 缺失 / JSON 不可解析 / `schemaVersion` 不兼容 → `ok=true`、退出码 0、`warnings[]` 含 `state-unreadable`、`payload.degraded="suggest-only"`,并以种子重建规则集(计数归零)。MUST NOT 非零退出、MUST NOT 抛栈(FR-013 / SC-010) |

## CLI Grammar(封闭集 — `quickstart.md` 与纪律文档的每条示例都 MUST 落在此集内)

| ID | Clause | Assertion |
|----|--------|-----------|
| **C-9** | action 封闭枚举 | `--action` 必填,`choices` 恰为 11 项:`init`、`assess`、`record`、`record-manual`、`status`、`rules`、`reset`、`config`、`tune`、`tune-apply`、`rotate`。集合外的值 → `EXIT_USAGE(1)` |
| **C-10** | flag 封闭集 | 全部长选项恰为 **20 个**:`--action`、`--format`、`--workspace`、`--session`、`--turn-id`、`--stage`、`--signal`(可重复)、`--probe`、`--compliance-done`、`--rule`、`--response`、`--flow`、`--threshold`、`--enabled`、`--window`、`--probe-budget`、`--proposal`、`--reason`、`--all`、`--min-sample`。未声明选项 → argparse 报错 → `EXIT_USAGE(1)`。`--compliance-done` 是布尔标志,**缺省为 false**:调用方(agent)必须显式声明 constitution 合规分析已先于本回合的流程选取完成;缺省即 false 是有意设计——顺序契约(FR-005b②)要求显式声明,不得被默认满足(见 C-14) |
| **C-11** | 标识符格式 | `--rule` 匹配 `^r-[0-9]{3}$`;`--proposal` 匹配 `^p-[0-9]{3}$`;`--response` ∈ `{accepted, declined, ignored}`;`--stage` 与 `--signal` 取值 MUST 属 `data-model.md` §受控词表的封闭枚举,越界 → `EXIT_INVALID(4)`。情境身份**不由 flag 传入** —— 它由引擎按 `--stage` + `--signal` 依 E1.`match` 谓词解析,只以 `payload.situationId`(匹配 `^s[0-9]{2}$`)出现在输出中(C-12) |

## 每回合语义(FR-005 / FR-005a / FR-009)

| ID | Clause | Assertion |
|----|--------|-----------|
| **C-12** | `assess` 的确定性解析 | `assess` 依 `--stage` + `--signal` 集合按 E1.`match` 谓词解析出**唯一** `situationId`;解析不到即 `payload.suggestion=null` 且 `payload.reason="no-situation-match"`。匹配、计数、阈值判定全在程序内完成,引擎 MUST NOT 要求 agent 提供流程名(FR-002 / Program-First) |
| **C-13** | `assess` 默认不读制品 | 未传 `--probe` 时,`assess` MUST NOT 打开 `.specify/specs/**`、`docs/**`、`README.md` 或任何制品文件(以 monkeypatch 的文件打开计数断言);传 `--probe` 时只允许 `data-model.md` §探测升级判据表 P1–P5 列举的存在性/计数/集合差探测,且返回值 MUST 为摘要(单条 ≤ 200 字符),MUST NOT 回传制品正文(FR-005) |
| **C-14** | `assess` 恒写一行遥测 | 每次 `assess` 向 `telemetry.jsonl` 追加**恰好一行**,字段恰为 E4 的 7 键;`suggested=true` 而 `complianceDone=false` 时,该行照写且 `errors[]` 记 `ordering-violation`(FR-005b② / SC-012);`suggested=false` 时 `visibleOutput` MUST 为 `false`(FR-005a 静默性 / SC-011) |
| **C-15** | 输出摘要有界 | `assess` 的 `payload` 序列化后 ≤ 60 行 / ≤ 2000 字符;`payload.suggestion` 含且仅含 `ruleId`、`flow`、`invocation`、`rationale`、`autoExecute`(bool)(FR-006:确切可复制调用形式由引擎供给) |

## 晋升与安全边界(FR-010 / FR-011 / FR-012)

| ID | Clause | Assertion |
|----|--------|-----------|
| **C-16** | 连续计数与重置 | `record --response accepted` 使该规则 `promotion.consecutive += 1`;`consecutive >= threshold` 且 `confirmationClass == "reversible"` → `state="promoted"`。`record --response declined` 或 `ignored` → `consecutive = 0` 且 `state` 由 `promoted` 回落 `active`,并记 `promotion.resetBy=<eventId>`(R2-Q3:一次拒绝即重置) |
| **C-17** | **破坏性永不晋升**(零容忍) | 对 `confirmationClass == "destructive"` 的规则,无论 `record --response accepted` 调用多少次(测试取 10 次),`promotion.promoted` 恒 `false`、`state` 恒 ≠ `promoted`、`assess` 返回的 `autoExecute` 恒 `false`;`confirmationClass` 是**数据**,引擎 MUST NOT 自行计算、推断或改写它(FR-011 / SC-005) |
| **C-18** | 阈值解析优先级与下限 | `threshold` 解析优先级恒为:显式 `--threshold` > 环境变量 `SPECKIT_TRIGGER_THRESHOLD` > `index.json` 的 `config.threshold` > 默认 `3`;非法环境变量值被忽略并降到下一级(不报错)。解析结果 < 2 → `EXIT_USAGE(1)` 且 `errors[]` 记 `threshold-below-floor`(与 `feedback-utils.py:resolve_threshold` 同构,FR-021;V6.3 下限裁定) |

## 项目本地性、非抢占与可断言性补强(analyze 2026-09-08 新增)

| ID | Clause | Assertion |
|----|--------|-----------|
| **C-19** | **项目本地 + 禁外传**(FR-020) | 模块的 `import` 集 MUST NOT 含任何网络能力模块:`urllib`、`urllib.request`、`http.client`、`socket`、`ssl`、`ftplib`、`smtplib`、`telnetlib`、`xmlrpc`(以 AST 或源码扫描机械断言;注意 C-1 的"stdlib only"**不足以**保证本条,因上述模块都属标准库)。全部写操作的目标路径 MUST 位于 `workspaceRoot` 之下;MUST NOT 存在任何跨项目/全局路径(如 `~/.specify`、`/tmp` 之外的用户级配置)的写入。学习状态 MUST NOT 出现在任何上行/打包通道的输入里 |
| **C-20** | **会话级重复抑制**(FR-008「状态未变不重复产出」的机制) | 同一 `--session` 下,若本次解析出的 `situationId` 与命中 `ruleId` 均与 E6.`lastSuggestion` 相同,`assess` MUST 返回 `payload.suppressed=true` 且 `payload.suggestion=null`,遥测记 `suggested=false` / `visibleOutput=false`;任一变化则正常产出并更新 `lastSuggestion`。`--session` 切换、`reset --all`、`config --enabled false→true` 三者 MUST 清空全部 `lastSuggestion`(V6.8)。**该条使 SC-004 的"重复建议数为 0"从散文变为可测** |
| **C-21** | **不抢占 = 引擎从不自行执行流程**(FR-019) | 引擎 MUST NOT 调用任何 `/speckit.*` 命令或技能:`payload.suggestion.autoExecute` 只是**给 agent 的建议标志**,执行与否、何时执行由 agent 依纪律文档决定。机械断言:模块内 `subprocess`(若使用)的目标 MUST 仅可能是 `feedback-utils.py --action status`(探测 P4 所需),MUST NOT 出现任何 `speckit`、`skill` 或流程名字面量。故"抢占用户当前请求"在引擎侧**结构上不可能**,该义务的剩余部分(agent 让位/延后)由 `discipline-doc.md` C-12 承载 |
| **C-22** | 错误码与警告码**封闭集** | `errors[]` / `warnings[]` 的元素 MUST 属下列封闭集,集合外即违约:`ordering-violation`、`state-unreadable`、`threshold-below-floor`、`vocabulary-out-of-range`、`no-prior-assess`、`rule-not-found`、`proposal-not-found`、`identifier-malformed`、`seed-unreadable`、`telemetry-unwritable`。新增码 MUST 同批修订本条款(纪律文档 `Maintenance Duties` ③) |
| **C-23** | `status` 的 payload schema | `--action status` 的 `payload` 键集恰为:`config`(E6.`config` 全 5 键)、`ruleCountByState`(`{active, suppressed, promoted}`)、`promotedRules`(ruleId 数组)、`pendingProposals`(int)、`telemetry`(`{rows, window, turns, escalated, suggested, visibleOutputCount, escalationPct}`);**`rows` 与 `turns` 的区别 MUST 显式定义**:`rows` = `telemetry.jsonl` 当前行数(受 `window` 截断,故 ≤ window);`turns` = **本 `--session` 内**的遥测行数(按 `turnId` 前缀过滤,不受窗口截断影响)。`escalationPct` 的分母是 `turns`(analyze N-19:此前两者未区分,使 quickstart 场景 3 的 `turns == 20` 依赖走查顺序)、`probeBudgetPct`(int)、`budgetOver`(bool)。`escalationPct` = `escalated / turns × 100`(分母口径见 `data-model.md` V4.5);`budgetOver` = `escalationPct > probeBudgetPct`。`quickstart.md` 场景 3 断言的每个字段名都由本条款钉住 |

---

## 其余 action 的行为契约(由 C-9…C-11 的语法约束 + C-19…C-23 的补强约束 + 下列语义约束共同钉住)

| Action | 语义 | 关键约束 |
|---|---|---|
| `init` | 由种子建状态 | **幂等**;已存在的 `ruleId` 只刷新 `rationale`/`invocation`,凡 `tuning` 非空者其 `state`/`priority`/`confirmationClass` 以本地为准(V2.3:用户调优不被种子回退) |
| `record` | 记建议事件 | 见 C-16;写 E3 并更新 E2.`stats` 与 E5。**字段来源**:`--rule` 与 `--response` 之外的 E3 字段(`situationId`/`snapshot`/`escalated`/`created`)由引擎从同 `--session` 的 E6.`lastSuggestion` 关联填充;该会话无在先 `assess` → `EXIT_INPUT_ERROR(2)` + `errors:["no-prior-assess"]`,MUST NOT 写半截事件(V3.4) |
| `record-manual` | 记用户手动调用的流程 | 需 `--flow`;若当回合遥测中 `suggested=false`,则该条成为**漏报证据**,供 `tune` 消费(FR-015;首轮 Q1=A 的补偿控制) |
| `status` | 紧凑摘要 | `payload` 键集**恰为 C-23 所列**(不再以散文描述);`--format text` 渲染 ≤ 30 行 |
| `rules` | 规则清单 | 每行 `ruleId / situationId / flow / class / origin / state / consecutive / hits / declined`;`--format json` 给全字段 |
| `reset` | 复位晋升态 | `--rule <id>` 或 `--all`;置 `consecutive=0`、`promoted=false`、记 `userResetAt`(FR-012);`--all` 另 MUST 清空全部 `lastSuggestion`(V6.8,否则复位后首回合仍被抑制) |
| `config` | 读写配置 | `--enabled true|false`(FR-018 全局开关;`false` 时 `assess` 恒返回无建议且不产出自动执行)、`--threshold`(改写后 MUST 按 V5.4 对每条规则重判 `promoted`)、`--window`、`--probe-budget`、`--min-sample`;`--enabled` 由 false 转 true 时 MUST 清空全部 `lastSuggestion`(V6.8) |
| `tune` | 证据聚合 → 提议 | **提议发射判据(封闭常量,analyze N-08 补 —— 此前只有小样本守卫而无发射阈值,致 SC-007 的"100% 识别"不可测)**:`suppress` 当 `declined/hits ≥ 0.50`;`tighten` 当 `ignored/hits ≥ 0.50`;`add-rule` 当某 `flow` 的漏报计数(`record-manual` 且当回合 `suggested=false`)**≥ 2**;`extend-vocabulary` 当出现无法被现有词表表达的漏报情境 ≥ 1。四者都另需 `hits ≥ minSample`(小样本守卫)。这些常量是**契约常量**而非 `config` 键(E6.`config` 保持封闭 5 键、C-10 保持封闭 20 flag,不为 v1 引入可调阈值);若未来需要可配,须同批扩 E6/C-10/本行。确定性计算**命中率 / 拒绝率 / 误报 / 漏报**四类指标(漏报 = `record-manual` 集 − 已建议集的差集;误报 = 建议后当回合被 `declined` 的比率);**小样本守卫**:`stats.hits < minSample`(默认 5)的规则 MUST NOT 产出提议(FR-017),被跳过的规则在 `notes[]` 具名回显。提议对象键集见 `data-model.md` E6.`proposals`(含 `kind ∈ {tighten, suppress, add-rule, extend-vocabulary}` 与 `evidence{metric,value,sampleSize}`)。语义判断(该不该采纳、新规则怎么措辞)留在 agent,经 `semanticJudgmentPending[]` 交回 |
| `tune-apply` | 写回已批准提议 | 需 `--proposal <p-nnn>` 与 `--reason`;执行 SM-2 的**两段转移** `proposed → ratified → applied`,并同时写 `ratifiedAt` 与 `appliedAt`(使"批准"成为可回查的独立事件,而非与"生效"混为一谈);写 E2.`tuning.{suppressedBy, ratifiedAt, evidenceRef}`。未经该 action 规则集 MUST NOT 变更(FR-016) |
| `rotate` | 遥测显式收缩 | 截断 `telemetry.jsonl` 保留最近 `config.telemetryWindow` 行。**注意 V4.3 已把有界性改为追加即截断的恒真不变量**,故本 action 只在用户调小窗口或需要立即收缩时才有实际效果;MUST NOT 触及 `index.json`——轮转/截断后 `promotion.consecutive` 与 `state` 逐规则**逐一相等**(FR-009a / SC-015 零丢失) |

## 信封字段的语义约束

- `errors[]` / `warnings[]` 的元素为**短码字符串**,非自由散文;码集**封闭且已在 C-22 完整枚举**(10 个码),故"封闭"是可机械断言的:出现集合外的码即违约。新增码 MUST 同批修订 C-22。
- `semanticJudgmentPending[]` 承载"程序已给出证据、判断归 agent"的项(如调优提议是否成立、漏报情境该配哪条流程),承 `derive-utils.py` 中 `semanticChecksPending` 字段的**分工原则**(键名按 C-3 有意改写):**确定性部分交引擎,语义判断留 agent**。
- `notes[]` 承载非阻塞提示(如被小样本守卫跳过的规则清单、种子刷新的留痕)。

## 本契约对 quickstart 示例的约束

`quickstart.md` 中出现的每条 `trigger-utils.py` 调用,其 `--action` 值 MUST ∈ C-9 的 11 项、其每个长选项 MUST ∈ C-10 的封闭集、其标识符实参 MUST 满足 C-11 的格式。该约束由 `tests/contract/test_trigger_engine.py` 以"解析 quickstart 代码块 → 逐条校验 action/flag/标识符"的方式机械断言,故本契约即 quickstart 示例的**有效性钉桩**(引擎尚未实现,示例无法在本阶段执行)。
