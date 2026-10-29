# Data Model: sdd-loop-driver 运行效率优化（SDD Loop Efficiency）

**Feature**: 074-sdd-loop-efficiency → Feature 058（演化特性）
**Spec**: [requirements.md](requirements.md)
**说明**: 本特性不新增数据库或常驻存储。实体全部落在文件上：每线**状态脊**（Markdown，承载记录与台账）、特性目录下的**测试证据文件**（JSONL）、阶段运行产物（raw stream / live log / pid / status / heartbeat / runner-log）。本文件登记字段面与校验规则，是契约测试与审计脚本的判定对象；字段值域以本节为 plan 期权威，实现后由脚本常量与契约测试共同钉住。除 E1–E8 实体外，本文件还登记一个**非实体证据制品**：Stall Behavior Baseline（SC-010）。CLI Capability Profile 与 CLI 观测字段由 Feature 064 的 `data-model.md` E9/E10 拥有，不在本文件定义。

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

**`lines.manifest` 行语法（owner）**：本小节是 `lines.manifest` 行语法的唯一 owner；FL-03(e)、quickstart 与夹具只引用本节，不复述语法。

- 文件为 UTF-8 文本；空行忽略；以 `#` 开头的行是注释，不构成记录。
- 每条记录行 = `<line-label>|<branch>`：恰一个 ASCII `|` 分隔符、两个非空字段，字段前后无空白。
- `line-label` 匹配 `[A-Za-z0-9._-]+`；`branch` 是 git 分支引用名，不得含空白或 `|`。
- 快车道准入要求文件恰有一条记录，且其 `branch` 等于 `--expected-branch`；零条、多条或分支不匹配 → 判据 (e) fail（fail-closed）。

**校验规则**：
- V-E1-1：`decision=fast-lane` 时七个判据全部为 `pass`，且每项 `evidence` 非空与可复算（SC-001）。
- V-E1-2：`entry_evidence` 缺失 [[STR-006]] → MUST NOT 产生 `fast-lane`；自然语言声明不构成启用。
- V-E1-3：`tasks.md` 缺失/不可解析、任一计数无法复算、`lines_manifest` 缺失、记录不符合本节「行语法」或非单线 → `full-chain`（fail-closed），记录原因。
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
| `merge_source` | 路径 + 内容哈希或 `na` | 行由执行侧（远端拓扑/E3 传输副本）合并进状态脊时必填；记录来源路径、哈希与合并时间；`na` 表示本行由状态脊一侧直接写入 |
| `merged_at` | epoch 或 ISO-8601 或 `na` | 合并时间；`merge_source=na` 时为 `na` |

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
- V-E2-7：`merge_source` 非 `na` 时，驱动 MUST 把执行侧传输行合并进状态脊并记录来源路径/哈希/时间；合并后的槽位语义 MUST 与直接写入一致；`test-evidence/implement.jsonl` 只是传输载体，合并前 MUST NOT 作为台账或审计来源；closure 审计在状态脊看不到 baseline 时 MUST 失败（FR-017/TB-03）。

## E3 — Targeted Test Evidence

**定位**：每个中间阶段与 review 的测试证据；一行一条测试运行或一次 `not-run` 判定。

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `stage` | 阶段名 | 一条记录只属一个阶段 |
| `row_type` | `stage-status` \| `run` | 每个适用阶段恰有一条 `stage-status`（阶段状态行）；`run` 为可选的补充运行行 |
| `status` | `ran` \| `not-run-docs-only` \| `empty-selection-escalated` \| `not-applicable-skipped-stage` \| `unknown` | 不允许静默空证据；`not-applicable-skipped-stage` 即 [[STR-008]] |
| `command` | 命令行 | `ran` 必填 |
| `selection_basis` | 规则编号 + 命令输出摘要 | 算法 owner = `contracts/test-budget.md` TB-05 `targeted-set-v1`；取 (a) 改动路径覆盖、(b) 交付物契约测试、(c) 夹具改动测试的并集 |
| `selected_paths[]` | 测试路径列表 | 空集时按 FR-013 边界处置 |
| `sufficiency` | 字符串 | 为何足以发现本阶段引入的回归 |
| `rc` / `passed` / `failed` | 整数 | `ran` 必填；缺失 → `unknown` |
| `new_failures[]` | 测试 ID 列表 | 相对所选基线 |
| `baseline` | 路径/命令或 `na` | 比较基线 |
| `changed_paths[]` | 仓库相对路径列表 | `not-run-docs-only` 必填；证明改动集不含可执行/测试面 |
| `evidence_ptr` | 路径 | 阶段日志/证据文件 |

**校验规则**：
- V-E3-1：`selected_paths` 为空且本阶段改动了可执行面 → `status=empty-selection-escalated`，必须扩大同族或按显式例外升级为全量（FR-013 边界）。
- V-E3-2：`not-run-docs-only` 仅当改动集不含可执行/测试面时合法；必须附 `changed_paths[]` 证据。
- V-E3-3：`ran` 行缺命令、选择依据、rc、计数、新增失败、基线任一字段 → 收口审计报告 `unknown`（SC-005）。
- V-E3-4：`status=not-applicable-skipped-stage`（[[STR-008]]）仅当 `stage=checklist`、E1 准入记录 `decision=fast-lane` 且状态脊含 [[STR-003]] 跳过标记时合法；该记录 MUST NOT 记为 `unknown`，MUST NOT 计入 SC-005 完整性分母；缺少上述联结证据的跳过 → `unknown` 并由收口审计报告。
- V-E3-5：`status=not-run-docs-only` 按缩减字段集判定完整——`stage`、`row_type=stage-status`、`status`、`selection_basis`、`changed_paths[]`、`evidence_ptr` 六项齐全；运行字段（`command`、`rc`、`passed`、`failed`、`new_failures`、`baseline`）不适用，MUST NOT 报 `unknown`。缺任一缩减字段 → 判未完整。
- V-E3-6：每个适用阶段 MUST 恰有一条 `row_type=stage-status` 行；整阶段缺失该行 → 计入完整性分母并判未完整（MUST NOT 静默缩小分母）；授权跳过阶段（[[STR-008]]）不计入分母；收口审计 MUST 输出 `stages=N complete=N`（N = 适用阶段总数）。

## E4 — Plan Constraint State

**定位**：plan 完成后的只小修约束状态。

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `plan_constraint` | `absent` \| `active` | plan U4 通过时置 `active` |
| `activated_at` | epoch/ISO-8601 | 生效点 = plan 完成时 |
| `plan_commit` | 提交号 | 约束基线；同时是「已批准需求基线」的**初始**锚点（FR-022） |
| `approved_baseline_commit` | 提交号 | 初始 MUST 等于 `plan_commit`；任何 re-baseline 后更新为最新基线提交；E5 分类 MUST 以它为准 |
| `rebaseline_events[]` | 每次 `{trigger, at, previous_baseline_commit, new_baseline_commit, requirements_diff_summary}` | requirements.md 在 plan U4 后被合法修改时记录的重新锚定事件；不构成 plan 重审，不移动约束生效点 |
| `plan_owned_paths[]` | 路径列表 | `plan.md`、`data-model.md`、`contracts/`、`quickstart.md`、`research.md`、`feature-ref.md` |
| `re_reviews[]` | 每次 `{trigger, at, plan_commit}` | 每次完整 plan 重审都必须记录；不设人工次数上限，重复回环由既有 stall/retry 纪律（90 分钟 / 2 次）兜底 |

**校验规则**：
- V-E4-1：`active` 后下游提示词必须携带只小修块与 `PLAN-EDIT:` 声明要求（FR-020/FR-021）。
- V-E4-2：驱动重入后必须从状态脊恢复 `active` 与 `activated_at`（edge case）。
- V-E4-3：收尾汇总必须报告是否发生 plan 制品改动及其分类（FR-024）。
- V-E4-4（re-anchoring）：plan 约束激活后，任何在门内完成的 `requirements.md` 变更（含 analyze 路由修复、clarify 写回与显式范围修订）MUST 在下一个依赖该基线的 U4 分类之前触发 re-baseline——状态脊记录 `rebaseline_events[]` 一条（触发、时间、前一基线提交、新基线提交 = 包含该变更的提交、FR/SC 定义集合与语义差异摘要），并把 `approved_baseline_commit` 更新为新基线提交。变更未提交或无法定位其提交时 MUST NOT re-anchor，受影响 plan 改动一律按 FR-022(b) 上送。re-anchoring 本身不构成 plan 重审，也不移动约束生效点；此后的 (a)/(b) 判定 MUST 以最新锚定基线为比较对象。
- V-E4-5：`approved_baseline_commit` MUST 指向一个包含当前 `requirements.md` FR/SC 定义集合与语义的提交；驱动 MUST 用 `git show <commit>:requirements.md` 复核该文件存在且定义集合与记录一致；缺失或不一致 → 分类不可信、门失败。

## E5 — Plan Change Classification

**定位**：U4 对下游阶段提交的 plan 制品改动分类与处置。

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `stage` / `base` / `head` | 阶段名 + 提交区间 | `base..head` 覆盖本阶段提交 |
| `approved_baseline_commit` | 提交号 | MUST 等于 E4 最新的 `approved_baseline_commit`（初始为 `plan_commit`，re-baseline 后为最新基线提交）；分支 (a)/(b) 判定以该提交的 `requirements.md` FR/SC 定义集合与语义为比较对象；缺失或不一致 → 分类不可信、门失败 |
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
- V-E5-5：分类记录 MUST 含 `approved_baseline_commit`，其值 MUST 等于 E4 最新的 `approved_baseline_commit`（初始 = `plan_commit`，re-baseline 后 = 最新基线）；分支 (a) 的「不改变已批准需求」判定 MUST 以该提交的 `requirements.md` 为比较对象，MUST NOT 以工作树当前文本或其它提交替代（FR-022/SC-006）。
- V-E5-6：若 `requirements.md` 在 plan U4 后发生变更但尚未提交、或无法定位其提交，则 MUST NOT re-anchor；受影响 plan 改动一律按 FR-022(b) 上送。若已 re-anchor，分类 MUST 使用最新 `approved_baseline_commit`，且为本特性新口径所需的 plan 改动 MUST 按两分支正常分类，不得因旧基线缺少该需求而误判越界。

## E6 — Stage Dispatch Record

**定位**：每次阶段派发的运行要素；U2 写状态脊，U3/U4 更新。

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `stage` / `line` | 阶段与线标签 | 一线一状态脊 |
| `state_spine_path` | 绝对或仓库相对路径 | MUST 等于 E8 U0 入口声明记录的路径；阶段提示词骨架中的 `STATE_SPINE_PATH` 与它同源；缺失 → 派发前快速失败（`ANOMALY:`），MUST NOT 另建第二份状态脊 |
| `spine_write_mode` | `direct` \| `transport` | `direct` = 执行侧可直接写状态脊（本地）；`transport` = 远端拓扑，执行侧写 `<spec-dir>/test-evidence/<stage>.jsonl` 传输行，由驱动合并进状态脊并记 `merge_source` |
| `prompt_path` / `sentinel` | 路径 + 字面量 | 哨兵不变（大写阶段名 + [[STR-002]]） |
| `detached` | `yes` \| `no` | 本地/远端都编码 nohup 形态；`no` 必须标记「未脱离」风险 |
| `dispatch_form` | 命令行形态摘要 | 必含 `nohup` 与 stdin `/dev/null` 与 stdout/stderr 重定向（FR-031） |
| `mode` | `stream` \| `buffered-degraded` | 降级必须带原因 |
| `raw_path` / `live_log_path` | 路径 | stream 模式 raw 必填；buffered 记 `na` |
| `pid/status/heartbeat` | 路径 | 四件套保持 |
| `stage_started_at` / `stage_deadline_epoch` | epoch | TIMEOUT 唯一判据 |
| `fast_lane_marker` | `none` \| [[STR-003]] | 与准入记录一致 |
| `plan_constraint_marker` | `none` \| `active` | 与 E4 一致 |

CLI 查档字段（`profile_id` / `profile_version` / `observed_cli_version`）由 Feature 064 的 `data-model.md` E10 追加到派发记录；本文件不重复定义，MUST NOT 在 063 另立字段。

**校验规则**：
- V-E6-1：`detached=no` 的运行不得计入受保护运行，状态脊记录风险（edge case）。
- V-E6-2：`mode=buffered-degraded` 必须附 [[STR-004]] 与原因（SC-011）。
- V-E6-3：哨兵、判定状态机、退出码、四件套路径语义不得因本实体扩格而变化（FR-029/FR-032）。
- V-E6-4：`state_spine_path` MUST 非空并与 E8 U0 入口声明一致；缺失或与 U0 不一致 → 派发前以 `ANOMALY:` 快速失败，MUST NOT 猜测路径或另建台账。
- V-E6-6：`spine_write_mode=transport` 时，阶段 MUST 只写 E3 传输行与名称名单；驱动 MUST 在 U4 后把对应 E2 行合并进状态脊并记 `merge_source`；执行侧 MUST NOT 创建第二份台账，closure 审计在状态脊看不到 baseline 时 MUST 失败。

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
- V-E7-2：`derivation` 降级时 MUST 先尝试 `raw-finish` 从终止 result 事件恢复；恢复成功写入 live log 并记 `degraded:derivation-recovered`；只有 raw 无 result 且 raw 最后非空行恰为哨兵时才走 `buffered-fallback`；两者皆无 → `sentinel=0`，判 INCOMPLETE（缺失完成证据，不是降级导致阶段失败）。不得伪造进度行（SC-007/SC-009）；每条派生行 MUST 可追溯到一条 raw 事件，事件从 runner 接收并写入 raw stream 到对应派生行写入 live log 的延迟 MUST ≤120 秒，无事件区间不适用该阈值。
- V-E7-3：raw 与 live 均须保留到 U4/U5 与收尾审计（FR-035）。

## E8 — Line State Spine

**定位**：每线唯一持久状态；续环与重入只读它。

| 区块 | 内容 | 写入时机 |
|------|------|----------|
| U0 entry | 目标/拓扑/权威/切片/断点 + `state_spine_path` + `spine_write_mode`（`direct`/`transport`） + [[STR-006]]（如有） | U0 |
| preflight | 五族结论摘要 | U0/U1 之间 |
| dispatch | E6 字段（含 `state_spine_path`、`spine_write_mode`；CLI 查档字段由 064 E10 追加） | U2 派发前 |
| watch | `last_verdict` / 证据快照 | U3 终止判定时 |
| admission | E1 | checklist 派发前 |
| test budget | E2 围栏 | 每次测试证据入账时 |
| plan constraint | E4（含 `approved_baseline_commit`、`rebaseline_events[]`） | plan U4 后 |
| stall baseline | [[STR-007]] 路径 + `base_commit` + `initial_retries=0` + 录制时间 | 实现首个行为面提交前 |
| plan changes | E5 | 每个下游阶段 U4 后 |
| verify/stall | U4 结论 / U5 上送四要素 | U4/U5 |

CLI 观测段（`cli_observations`）由 Feature 064 的 `data-model.md` E10 定义并追加到状态脊；本文件不重复该段及其写序规则。

**校验规则**：
- V-E8-1：所有状态转移先写状态脊后执行动作；续环不依赖会话记忆。
- V-E8-2：多线并行时每线独立 E1/E2/E4/E6/E7，路径与槽位不得共享或互相覆盖（FR-011）。
- V-E8-3：新会话接手先 `--once` 快照；已完成阶段只核验不重派（FR-032）。
- V-E8-4：U0 入口 MUST 记录 `state_spine_path` 与 `spine_write_mode`；所有阶段的 E6 与阶段提示词骨架 MUST 引用同一路径。远端拓扑（`transport`）下，执行侧只写 spec-dir 证据与传输行，驱动在 U4 后合并进状态脊并记录 `merge_source`；本地拓扑（`direct`）可直接追加，但状态脊 MUST 仍是唯一台账来源（FR-017/TB-03）。

## Stall Behavior Baseline（卡死行为基线证据制品，非 E1–E8 实体）

**定位**：SC-010 的行为比较对象。路径固定为 spec-dir 下的 [[STR-007]]，在实现首个行为面提交之前录制；它不是状态脊实体，不改变 E1–E8 实体计数，也不消耗全量测试预算槽位。

**录制对象**：实际行为基线提交 `a1aac7e5`（规格冻结读数 `ba2a18db` 不适用：其后的首个行为面提交为 `9e69f3de`，按 FR-038 取首个行为面改动前的父提交；差异记录于状态脊与 plan.md § Plan Repair Record 第 5 轮）上的三类卡死场景，外加一个成功完成的正控场景：

| 场景 | 处置结果 |
|------|----------|
| 超时（TIMEOUT） | watcher 判 TIMEOUT |
| 重试上限（stalled） | 状态脊卡死状态 + 四要素上送件齐备 |
| 伪完成（退出 rc=0 且哨兵缺失） | 判 INCOMPLETE，不派发下一阶段 |
| 成功（DONE） | 写 `next_stage=<stage>` 到 `dispatch.log` 并派发，`next_stage_dispatched=yes` |

**每个元组字段**：`watcher_verdict`、`exit_code`（对象：`{"watcher": <int>, "runner": <int>}`，分别记录 watcher 判定退出码与 runner/CLI rc；MUST NOT 合并为一个值）、`spine_stall_state`、`retries_consumed`、`escalation_package_complete`（或 `not-applicable`）、`next_stage_dispatched`（`yes|no`）、`spine_write_before_action`（`yes|no`）、`evidence_ptr`。文件根字段：`base_commit`、`recorded_at`、`initial_retries`（固定为 `0`）、`scenarios[]`。

**录制与比较约束**：
- SB-1：基线 MUST 在实现首个行为面提交之前录制；录制时点、`base_commit` 与 `initial_retries=0` MUST 写入状态脊（E8 stall baseline 行）。
- SB-2：三类卡死场景（超时 / 重试上限 / 伪完成）MUST 统一由**驱动侧可执行夹具**（`tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py`）驱动并观测：stub runner 产生受控 pid/status/heartbeat/runner-log 与 rc，真实 `watch-target.sh` 提供 U3 判定，夹具执行文档化的 U4/U5 驱动侧程序（状态脊先写后动、重试消耗、四要素上送件、下一阶段派发决策）并从状态脊/status/退出记录读取七个字段。另以一个成功完成场景作为正控，使 `next_stage_dispatched` 在 `yes` 与 `no` 两个方向都可观测；正控不替代三类卡死场景。watcher 自动夹具只提供 U3 判定，不得被当作驱动侧字段来源；录制 trace 仅可作为端到端补充证据，MUST NOT 替代夹具观测。
- SB-3：收口 MUST 用同一可执行夹具与同一 `initial_retries=0` 在当前树上重放并生成 final 记录；比较前归一化剔除时间戳、PID、绝对路径与耗时，证据指针按「场景目录/文件名」比较。
- SB-4：逐字段比较；任何字段差异 MUST 判回归并修复，MUST NOT 以归因豁免。名称级测试失败基线只服务 SC-012，MUST NOT 用于 SC-010。
- SB-5（反转录）：夹具 MUST NOT 从判定表/场景→期望值映射填充字段，MUST NOT 从基线文件回填；字段值 MUST 由受控场景中的实际观测产生。夹具 MAY 断言内部一致性（如 `runner` 子字段等于 status 文件的 `exit`、`watcher` 子字段等于 watcher 进程退出码），但 MUST NOT 断言或写入硬编码的期望元组。`retries_consumed` MUST 从 `initial_retries=0` 起按实际重试逐步累加；`spine_write_before_action` MUST 由状态脊写入与动作执行的可复核顺序产生。
- SB-6（证据持久化）：每场景的 spine/status/watcher/dispatch/escalation 等证据 MUST 在临时运行根删除前复制到 spec-dir notes 下的持久目录；`evidence_ptr` MUST 指向该持久位置的相对路径，MUST NOT 指向已删除的临时目录。

## CLI Capability Profile / CLI Observation（归属 064，仅指针）

这两个证据制品不在本特性数据模型内。唯一 owner = `.specify/specs/064-subagent-concurrency/data-model.md` E9（CLI Capability Profile）与 E10（State Spine Extension：`cli_observations` 与派发记录 `profile_id` / `profile_version` / `observed_cli_version`），契约 = 064 `contracts/cli-profiles.md` CLP-01…CLP-17。063 的 E6/E8 只保留基础派发/状态脊字段；CLI 追加字段由 064 E10 定义，MUST NOT 在 063 复制字段表、观测记录或校验规则。

## 实体关系

```text
E8 State Spine (per line)
 ├─ E6 Dispatch Record ×N ──▶ E7 Raw/Live Pair (per stage)
 ├─ E1 Admission Record (0..1 per feature run)
 ├─ E2 Test Budget Ledger (2 slots + reruns/exceptions)
 │    └─ evidence_ptr ──▶ E3 Targeted Evidence ×N (per stage)
 ├─ E4 Plan Constraint State (activated at plan completion)
 │    └─ approved_baseline_commit / rebaseline_events[]
 ├─ E5 Plan Change Classification ×N (per downstream stage U4)
 └─ Stall Behavior Baseline ──▶ [[STR-007]] (recorded before first behavior commit)
```

CLI 观测段与 CLI 档案（064 E9/E10）不在此关系图内；它们引用 E6/E8 的基础字段，由 064 定义。
