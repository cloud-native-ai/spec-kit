# Data Model: sdd-loop-driver 运行效率优化（SDD Loop Efficiency）

**Feature**: 063-sdd-loop-efficiency → Feature 058（演化特性）
**Spec**: [requirements.md](requirements.md)
**说明**: 本特性不新增数据库或常驻存储。实体全部落在文件上：每线**状态脊**（Markdown，承载记录与台账）、特性目录下的**测试证据文件**（JSONL）、阶段运行产物（raw stream / live log / pid / status / heartbeat / runner-log）。本文件登记字段面与校验规则，是契约测试与审计脚本的判定对象；字段值域以本节为 plan 期权威，实现后由脚本常量与契约测试共同钉住。

## 实体一览

| # | 实体 | 承载 | 本特性变更 |
|---|------|------|------------|
| E1 | Fast-Lane Admission Record（快车道准入记录） | 状态脊 Markdown 块 | 新增 |
| E2 | Test Budget Ledger（全量测试预算台账） | 状态脊 JSONL 围栏 | 新增 |
| E3 | Targeted Test Evidence（定向测试证据） | `<spec-dir>/test-evidence/<stage>.jsonl` | 新增 |
| E4 | Plan Constraint State（plan 约束状态） | 状态脊字段 + 下游提示词块 | 新增 |
| E5 | Plan Change Classification（plan 改动分类） | U4 校验记录（状态脊） | 新增 |
| E6 | Stage Dispatch Record（派发记录） | 状态脊 + 派发产物命名 | 扩格 |
| E7 | Raw/Live Evidence Pair（原始流/实时日志对） | `<state-dir>/raw-*.jsonl` + `log-*.log` | 新增 |
| E8 | Line State Spine（线状态脊） | 驱动侧每线一份 Markdown | 扩格（承载 E1/E2/E4/E6/E7 指针） |

## E1 — Fast-Lane Admission Record

**定位**：一次准入裁决的完整证据包；写入状态脊后才可跳过 `checklist`。

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `decision` | `fast-lane` \| `full-chain` | 只有全部判据通过且入口启用证据有效时为 `fast-lane` |
| `entry_evidence` | 原文片段 | MUST 含字面量 [[STR-006]]，或交互式采纳原文；无人值守运行只认前者 |
| `criteria[]` | 每项 `{id: a…g, verdict: pass\|fail, evidence: string}` | 七项齐全；全部由 `admission-check.py` 机械判定，每项 `evidence` 非空且可复算（无自证项） |
| `lines_manifest_ptr` | 路径 | U0 拓扑声明导出视图；脚本要求恰一行本线记录且分支匹配 |
| `measured.fr_count` / `measured.task_count` | 整数 | 由制品实测派生，不手抄；FR 只数定义行、任务只数任务行；区间 owner 为 requirements.md FR-003 |
| `decided_at` | epoch 或 ISO-8601 | 裁决时间 |
| `reversion`（可选） | `{trigger, evidence, at}` | 录取后判据失效/新事实时的回退触发；发生即必须记录 |

**校验规则**：
- V-E1-1：`decision=fast-lane` 时七个判据全部为 `pass`，且每项 `evidence` 非空与可复算（SC-001）。
- V-E1-2：`entry_evidence` 缺失 [[STR-006]] → MUST NOT 产生 `fast-lane`；自然语言声明不构成启用。
- V-E1-3：`tasks.md` 缺失/不可解析、任一计数无法复算、`lines_manifest` 缺失或非单线 → `full-chain`（fail-closed），记录原因。
- V-E1-4：记录 MUST 在 `checklist` 派发前写入状态脊，并携带 [[STR-003]] 跳过标记（FR-004）。
- V-E1-5：收尾汇总必须能由记录复现：裁决、逐条证据、实测计数、checklist 状态（跳过/执行）。

## E2 — Test Budget Ledger

**定位**：每线独立的全量测试台账；以状态脊内围栏 JSONL 承载，一行一条执行记录。

```text
<!-- test-budget:begin -->
{"seq":1,"slot":"baseline",...}
{"seq":2,"slot":"closure",...}
<!-- test-budget:end -->
```

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `seq` | 正整数，线内单调 | 执行序号 |
| `slot` | `baseline` \| `closure` \| `in-slot-rerun` \| `out-of-slot-exception` \| `environment-failure` | 预算语义见下 |
| `stage` | 阶段名 | 槽外例外必须写明请求阶段 |
| `purpose` | 字符串 | 本次执行目的 |
| `trigger` | 字符串 | 重跑/例外的触发；baseline/closure 首次可为 `scheduled` |
| `at` | epoch 或 ISO-8601 | 时间 |
| `command` | 完整命令行 | 全量 = 项目规范 runner 且无路径/测试过滤器 |
| `selection_basis` | 字符串（定向） | 全量记录为 `full-suite` |
| `rc` | 整数 | 退出码 |
| `passed` / `failed` | 整数或 `unknown` | 证据缺失不得写 0 |
| `failed_names_path` | 路径或 `na` | baseline/closure 必须给出名称清单文件 |
| `baseline_compare` | `na` \| `comm -13` 结果（新增失败名列表/计数） | 最终全量必须是名称级差集 |
| `exception_reason` | 字符串 | `out-of-slot-exception` 必填，含证据指针 |
| `environment_evidence` | 字符串 | `environment-failure` 必填（解释器/依赖缺失、收集前失败证据） |
| `evidence_ptr` | 路径 | 阶段日志或证据文件指针 |

**槽位语义**：
- `baseline`：implement 起点，每线至多 1 条；记录名称级失败基线。
- `closure`：review 通过后、合并前，每线至多 1 条；由驱动或独立校验单元执行。
- `in-slot-rerun`：最终收口槽内因修复新失败而重跑同一全量套件；不另开槽，必须带 `trigger` 与证据。
- `out-of-slot-exception`：槽外全量；必须带原因与证据，收尾汇总列出。
- `environment-failure`：收集/执行任何测试前失败；不消耗槽位。

**校验规则**：
- V-E2-1：正常收口时 `baseline` 恰 1 条、`closure` 恰 1 条；`in-slot-rerun` 只能出现在 `closure` 之后。
- V-E2-2：任何 `slot=out-of-slot-exception` 无 `exception_reason`/`evidence_ptr` → 审计失败（SC-003）。
- V-E2-3：`failed_names_path` 缺失或清单为空而 `failed>0` → 证据不足；`passed/failed` 缺失 → `unknown`，不得补造（FR-017）。
- V-E2-4：`environment-failure` 必须给出收集前失败证据；实际执行了测试的调用（含 0 tests collected 的选择失败）不得记为该槽位。
- V-E2-5：`closure` 的 `baseline_compare` 必须是名称级差集；仅计数比较 → 审计失败（SC-004）。
- V-E2-6：收口审计 MUST 可选扫描阶段日志（`--logs-dir`）中的全量 runner 命令；日志中出现但台账未入账的全量命中 → 审计失败；日志缺失 → `unknown`，MUST NOT 当零。

## E3 — Targeted Test Evidence

**定位**：每个中间阶段与 review 的测试证据；一行一条测试运行或一次 `not-run` 判定。

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `stage` | 阶段名 | 一条记录只属一个阶段 |
| `status` | `ran` \| `not-run-docs-only` \| `empty-selection-escalated` \| `unknown` | 不允许静默空证据 |
| `command` | 命令行 | `ran` 必填 |
| `selection_basis` | 规则编号 + 命令输出摘要 | 取 (a) 改动路径覆盖、(b) 交付物契约测试、(c) 夹具改动测试的并集 |
| `selected_paths[]` | 测试路径列表 | 空集时按 FR-013 边界处置 |
| `sufficiency` | 字符串 | 为何足以发现本阶段引入的回归 |
| `rc` / `passed` / `failed` | 整数 | `ran` 必填；缺失 → `unknown` |
| `new_failures[]` | 测试 ID 列表 | 相对所选基线 |
| `baseline` | 路径/命令或 `na` | 比较基线 |
| `evidence_ptr` | 路径 | 阶段日志/证据文件 |

**校验规则**：
- V-E3-1：`selected_paths` 为空且本阶段改动了可执行面 → `status=empty-selection-escalated`，必须扩大同族或按显式例外升级为全量（FR-013 边界）。
- V-E3-2：`not-run-docs-only` 仅当改动集不含可执行/测试面时合法；必须附改动路径证据。
- V-E3-3：缺命令、选择依据、rc、计数、新增失败、基线任一字段 → 收口审计报告 `unknown`（SC-005）。

## E4 — Plan Constraint State

**定位**：plan 完成后的只小修约束状态。

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `plan_constraint` | `absent` \| `active` | plan U4 通过时置 `active` |
| `activated_at` | epoch/ISO-8601 | 生效点 = plan 完成时 |
| `plan_commit` | 提交号 | 约束基线 |
| `plan_owned_paths[]` | 路径列表 | `plan.md`、`data-model.md`、`contracts/`、`quickstart.md`、`research.md`、`feature-ref.md` |
| `re_reviews[]` | 每次 `{trigger, at, plan_commit}` | 每次完整 plan 重审都必须记录；不设人工次数上限，重复回环由既有 stall/retry 纪律（90 分钟 / 2 次）兜底 |

**校验规则**：
- V-E4-1：`active` 后下游提示词必须携带只小修块与 `PLAN-EDIT:` 声明要求（FR-020/FR-021）。
- V-E4-2：驱动重入后必须从状态脊恢复 `active` 与 `activated_at`（edge case）。
- V-E4-3：收尾汇总必须报告是否发生 plan 制品改动及其分类（FR-024）。

## E5 — Plan Change Classification

**定位**：U4 对下游阶段提交的 plan 制品改动分类与处置。

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `stage` / `base` / `head` | 阶段名 + 提交区间 | `base..head` 覆盖本阶段提交 |
| `touched_paths[]` | plan 拥有路径 | 由 `git diff --name-only <base>..HEAD` **加** `git status --porcelain -- <plan paths>`（未提交改动）机械派生 |
| `declaration_lines[]` | 阶段回传中的 `PLAN-EDIT:` 行 | 缺失即未声明 |
| `classification` | `none` \| `minor` \| `substantive` \| `undeclared` | 按**最终 diff** 判定，不按单次编辑措辞 |
| `rationale` | 字符串 | minor/substantive 必须给出可复核理由 |
| `disposition` | `pass` \| `gate-fail-rereview` \| `gate-fail-escalate` | 见 FR-022 两分支 |

**校验规则**：
- V-E5-1：`touched_paths` 非空且 `declaration_lines` 为空 → `undeclared` → `gate-fail-*`（SC-006）。
- V-E5-2：`substantive` 定义：改变范围、架构方向、数据模型语义、契约语义、FR/SC 内容或任务分解范围，或引入新能力/安全面。
- V-E5-3：`minor` 仅限错别字/措辞、断链/引用修复、格式、行级一致性；多处小修合并后改变语义 → 按最终 diff 判 `substantive`。
- V-E5-4：分流 `(a)` 仅在「修复既有缺陷且不变更上述任一项」时合法；无法判定或引入新面 → `(b)` 四要素上送（FR-022）。

## E6 — Stage Dispatch Record

**定位**：每次阶段派发的运行要素；U2 写状态脊，U3/U4 更新。

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `stage` / `line` | 阶段与线标签 | 一线一状态脊 |
| `prompt_path` / `sentinel` | 路径 + 字面量 | 哨兵不变（大写阶段名 + [[STR-002]]） |
| `detached` | `yes` \| `no` | 本地/远端都编码 nohup 形态；`no` 必须标记「未脱离」风险 |
| `dispatch_form` | 命令行形态摘要 | 必含 `nohup` 与 stdin `/dev/null` 与 stdout/stderr 重定向（FR-031） |
| `mode` | `stream` \| `buffered-degraded` | 降级必须带原因 |
| `raw_path` / `live_log_path` | 路径 | stream 模式 raw 必填；buffered 记 `na` |
| `pid/status/heartbeat` | 路径 | 四件套保持 |
| `stage_started_at` / `stage_deadline_epoch` | epoch | TIMEOUT 唯一判据 |
| `fast_lane_marker` | `none` \| [[STR-003]] | 与准入记录一致 |
| `plan_constraint_marker` | `none` \| `active` | 与 E4 一致 |

**校验规则**：
- V-E6-1：`detached=no` 的运行不得计入受保护运行，状态脊记录风险（edge case）。
- V-E6-2：`mode=buffered-degraded` 必须附 [[STR-004]] 与原因（SC-011）。
- V-E6-3：哨兵、判定状态机、退出码、四件套路径语义不得因本实体扩格而变化（FR-029/FR-032）。

## E7 — Raw/Live Evidence Pair

**定位**：stream-json 原始事件流与派生实时日志；U4/U5 与事后审计证据。

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `raw` | `<state-dir>/raw-<line>-<stage>.jsonl` | 完整 NDJSON 原始事件流（FR-026） |
| `live` | `<state-dir>/log-<line>-<stage>.log` | 运行期增量增长；最后非空行 = 哨兵时为正常完成（FR-027/FR-028） |
| `derivation` | `stream` \| `degraded:<reason>` | 降级原因必填 |
| `result_found` | `yes` \| `no` | 是否从终止 `result` 事件提取到文本 |
| `sentinel_source` | `result-text` \| `raw-finish` \| `buffered-fallback` \| `none` | 非终止事件永不作为来源；stream 模式派生失败时 MUST 先跑一次性 `--finish` 恢复，再考虑 buffered fallback |

**校验规则**：
- V-E7-1：live log 的最后非空行必须等于 `<STAGE>-DONE` 才能作为完成正证据；中间事件中的哨兵字样不得成为裸最后一行。
- V-E7-2：`derivation` 降级时 MUST 先尝试 `raw-finish` 从终止 result 事件恢复；恢复成功写入 live log 并记 `degraded:derivation-recovered`；只有 raw 无 result 且 raw 最后非空行恰为哨兵时才走 `buffered-fallback`；两者皆无 → `sentinel=0`，判 INCOMPLETE（缺失完成证据，不是降级导致阶段失败）。不得伪造进度行（SC-007/SC-009）。
- V-E7-3：raw 与 live 均须保留到 U4/U5 与收尾审计（FR-035）。

## E8 — Line State Spine

**定位**：每线唯一持久状态；续环与重入只读它。

| 区块 | 内容 | 写入时机 |
|------|------|----------|
| U0 entry | 目标/拓扑/权威/切片/断点 + [[STR-006]]（如有） | U0 |
| preflight | 五族结论摘要 | U0/U1 之间 |
| dispatch | E6 字段 | U2 派发前 |
| watch | `last_verdict` / 证据快照 | U3 终止判定时 |
| admission | E1 | checklist 派发前 |
| test budget | E2 围栏 | 每次测试证据入账时 |
| plan constraint | E4 | plan U4 后 |
| plan changes | E5 | 每个下游阶段 U4 后 |
| verify/stall | U4 结论 / U5 上送四要素 | U4/U5 |

**校验规则**：
- V-E8-1：所有状态转移先写状态脊后执行动作；续环不依赖会话记忆。
- V-E8-2：多线并行时每线独立 E1/E2/E4/E6/E7，路径与槽位不得共享或互相覆盖（FR-011）。
- V-E8-3：新会话接手先 `--once` 快照；已完成阶段只核验不重派（FR-032）。

## 实体关系

```text
E8 State Spine (per line)
 ├─ E6 Dispatch Record ×N ──▶ E7 Raw/Live Pair (per stage)
 ├─ E1 Admission Record (0..1 per feature run)
 ├─ E2 Test Budget Ledger (2 slots + reruns/exceptions)
 │    └─ evidence_ptr ──▶ E3 Targeted Evidence ×N (per stage)
 ├─ E4 Plan Constraint State (activated at plan completion)
 └─ E5 Plan Change Classification ×N (per downstream stage U4)
```
