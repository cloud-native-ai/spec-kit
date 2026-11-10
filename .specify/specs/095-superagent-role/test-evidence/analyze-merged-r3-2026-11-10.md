# Analyze Merged Report — Round 3（095-superagent-role，2026-11-10）

- **Stage**: analyze 第三轮（r3 修复后重过门）· **Line**: `095-superagent-role` · 线 run `r20261110T055657Z-b095` · 本轮单元 run `r20261110T055657Z-b095-r3`
- **Contract**: `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md` / `references/validation-and-report.md`；宪法 `.specify/constitution.md`
- **Inputs**: `test-evidence/analyze-merged-round2-2026-11-10.md`（round-2 基线，44 行 = 0C/4H/28M/12L）+ `analyze-findings-round2-W{1,2,3}.md`（ID / residue 来源）+ `analyze-repair-dispositions-r3-2026-11-10.md` + `analyze-repair-gates-r3-2026-11-10.txt`（r3 修复面）；现行制品全文：`requirements.md`、`plan.md`、`tasks.md`、`data-model.md`、`contracts/`×4、`quickstart.md`、`feature-ref.md`、`checklists/`×2、`.specify/features.md` 095 行与 `.specify/features/095-superagent-role.md`
- **Round-3 口径**: 全严重度重裁——round-2 的 44 行逐条复裁（4 HIGH + 2 M/L 已在 r3 修复；其余 38 行维持并标注 `carried over`）+ r3 修复面复裁（`dual-role` 单语义、`dispatch_duty` 分离、四类违例扇出、SC-009 完成门）+ 全制品重新检测（A/B/C/D/E/F/G/I + H）
- **并发读数**: `requested=24`；`effective=1`；`effective_reason=budget-reserve`（可用槽位 < 2）——单 Worker 串行；**未派发独立验证波**
- **C/H 验证状态**: 无独立验证波。按技能 §5.5 的 subagent-unavailable fallback，C/H 行由本轮直接重读锚点替代，标记 `(validated: direct re-read, subagent unavailable)`；**severity 仍是检测者提议值，门禁裁决归 U4**
- **只读声明**: 本轮未修改任何 spec 制品、未修复任何 finding、未 push；除本报告与 Wrap-up 记账外无写点（临时捕获在 `.specify/.tmp/`，已被忽略）
- **锚点图例**: `REQ:` = `requirements.md`；`PLAN:` = `plan.md`；`TASK:` = `tasks.md`；`DATA:` = `data-model.md`；`ENG:` / `PAY:` / `DIG:` / `HAR:` = `contracts/role-edge-engine` / `role-transition-payload` / `status-digest-role-view` / `harness-landing`；`CHK:` = `checklists/requirements-quality-2026-11-10.md`；`FEAT:` = `.specify/features/095-superagent-role.md`（行号均为本轮实读）

---

## 0. 顶部汇总：CRITICAL / HIGH（计数 + 逐条指针，不修复）

**集成后计数**: CRITICAL **0** · HIGH **1** · MEDIUM **28** · LOW **12** = **41 行**（round-2 开放 38 + 本轮新增 3；round-2 已修复 6 行转入 §4.1）。

- **round-2 遗留清理**: 4 条 HIGH（W1-30 / W1-31 / W1-32 / W2-13）**全部关闭并有锚点证据**（§4.1）；另 2 条 M/L（W1-20 / W2-20）随同轮修复关闭。
- **HEADLINE（两种主张分开读）**: round-2 的 C/H 遗留**已清**（0C / 0 carried H）；但本次 rerun **不干净**——新增 HIGH 1（R3-01）。「遗留已清」≠「门禁干净」。
- 50 行上限：41 ≤ 50，无裁剪、无溢出。

| # | ID | 来源 | Validation | 一句话指针 | 锚点 |
|---|----|------|-----------|-----------|------|
| 1 | **R3-01** | round-3 新检出（W1-30 修复残留） | validated（direct re-read；subagent unavailable） | `dual-role` 被 r3 收敛为「只出现在角色集输出」的机读标记（SC-001 要求以 [[STR-002]] 标记集合形态），但引擎契约 C-3 只定义 `roles` 为 `{superagent,subagent}` 集合数组、C-10 把 A 的 `roles` 钉为恰好两项，**没有输出键承载该标记**；按字面实现，「标记在输出中」与 C-3/C-10 的集合语义二选一 | REQ:125、128、210；DATA:10、63；ENG:36、77；DIG:11；PLAN:36、222；TASK:122、123、198 |

**门禁含义（技能 §9，不修复）**: CRITICAL 0；HIGH 1（提议值）须经 U4 显式裁决或独立验证波后方可放行 implement；MEDIUM/LOW 可按归属指针带建议推进。**本报告不得被读作「ready to implement」。**

---

## 1. HIGH（1 行；节内 ID 字典序）

| ID | Status | Validation | propagation_surface | Category | Anchors | 一句话事实 | 建议归属（指针） |
|----|--------|-----------|---------------------|----------|---------|------------|------------------|
| R3-01 | new（W1-30 修复残留） | validated（direct re-read, subagent unavailable） | 引擎契约 C-3/C-10 + `test_role_edge_engine.py`（P2）+ digest C-2 渲染 | Inconsistency / Underspecification（输出槽位） | REQ:210（SC-001 要求 STR-002 标记集合形态）、125（FR-002）、128（FR-005）；DATA:10（role set = `{superagent,subagent}` 子集 + marker 声明）、63（§4 roles 为派生集合）；ENG:36（C-3 `executors[].roles` = array, set semantics）、77（C-10 钉 `A roles: ["subagent","superagent"]`）；DIG:11（both-roles rendered via the marker）；PLAN:36（D-8）、222（P2「role sets incl. dual-role」）；TASK:122（T011 schema 断言）、123（T012「A's role set carries the dual-role output marker」）、198（T036） | r3 把 `dual-role` 收窄为**只在角色集输出出现**的机读标记后，输出 schema 没有给它任何槽位：`roles` 若含第三 token 则违反 DATA:10 的集合域并打破 ENG:77 钉死的两项数组；若为独立键则 C-3/C-10/T011 均未声明与断言。两种读法各有一处必红，「以 STR-002 标记该集合形态」这一 final 路径验收当前不可判定。 | `/speckit.plan`：在 C-3 声明标记的键/值位置（如独立 `role_set_marker`）并同步 C-10/T011/T012/T036/D-8/P2；或 `/speckit.requirements`：收窄 SC-001 的标记断言到已契约化的观察点（须单一 owner） |

**检测侧证据边界（不得作为验证者 verdict 传入）**: 已逐字重读全部锚点；未运行测试，未实现引擎，因此「必红」是从文本推出的，不是实测读数。未测量是否存在额外 JSON 键的容忍度（C-3 写 "Required keys"，非闭集——若标记以额外键承载，C-3 不禁止，但 T011 也未钉它）。

---

## 2. MEDIUM（28 行；节内 ID 字典序）

| ID | Status | propagation_surface | Category | Anchors | 一句话事实 | 建议归属（指针） |
|----|--------|---------------------|----------|---------|------------|------------------|
| R3-02 | new（W2-13/W1-30 修复残留） | 引擎实现 + `test_role_edge_engine.py` schema 断言（P2） | Underspecification（字段来源） | DATA:23（§2 `dispatch_duty` 必备 + 语义）、44（§2.1(c) run-agent 载体仅 `unit_id`/`run_id`）、83（§6）；ENG:37（C-3 `edges[]` 必备 `dispatch_duty`） | `dispatch_duty` 是边记录必备字段与 C-3 必备输出键，但三载体中只有 (a) 映射行与 (b) sidecar 明确携带它；(c) `run-agent`/exec-quant 记录不含该字段。仅经 (c) 出现的边，该键取值无来源声明（`role_declaration` 尚有「本边即 subagent」的默认语义，`dispatch_duty` 没有），引擎只能在「省略（违反 C-3）」与「自行默认（未声明）」之间选择。 | `/speckit.plan`：在 §2.1(c) 声明取得规则（如按边默认 `not-granted`），或让 C-3 该键在 (c) 来源上可为 `null` |
| W1-07 | carried over | role-edge contract | Ambiguity（输入边界） | REQ:128、126；CHK:21 | FR-005 未定义输入记录集与执行树边界（单根 / 多根、跨 run 无关记录如何隔离），边与深度在不同仓库上不可确定。 | plan / contract |
| W1-08 | carried over | role-edge contract + SC 集 | Inconsistency（覆盖） | REQ:126、128、210-219；CHK:22 | FR-003 要求 `conflict` 报错并点名两处路径，但 FR-005 的输出枚举没有它、也没有任何 SC 验证它，该 MUST 既无输出归宿也无红测。 | `/speckit.requirements` / plan |
| W1-09 | carried over | role-edge contract | Ambiguity（优先级） | REQ:126、283；CHK:23 | FR-003 允许根身份取状态脊 `run_id` 或 line registry `line_id` 而未给优先级，A11 只把实现名交给 plan。 | plan / contract（见 W2-14） |
| W1-10 | carried over | role-edge / return contract + SC-005 | Underspecification（Gap） | REQ:126、139、214；CHK:24 | 边记录要求「派发尝试标识」，FR-013 的重试 / 陈旧判定依赖它，但没有既有字段被指明为该标识。 | plan / contract（≡ W2-05） |
| W1-12 | carried over | protocol contract | Ambiguity（owner + 可扩展性） | REQ:136、262；CHK:32 | FR-010 声明封闭消息分类集却把 owner 写成未具名的「owner 文档」，同时又说「最少区分四类」，owner 与可扩展规则都未固定。 | `/speckit.requirements` |
| W1-13 | carried over | protocol contract | Gap（载体） | REQ:136、142；CHK:33 | 四类消息中的 `ack` 与 `attention-escalation` 未映射到任何既有载荷 / 回传通道，行使它们就会造出 FR-016 禁止的第二通道。 | plan / contract |
| W1-14 | carried over | edge lifecycle contract | Gap（载体） | REQ:141；CHK:34 | FR-015 要求把 `completed / failed / cancelled` 写入既有载体，但没有既有记录被指明承载 `cancelled`。 | plan / contract |
| W1-15 | carried over | recovery contract + SC-005 | Gap（词表 / 载体） | REQ:162、214；CHK:46 | FR-027 / SC-005 要求把仍被判定在跑的子项标为 `interrupted` / `attention`，但词表 owner 与承载标记的记录都未具名。 | plan / contract（≡ W2-07） |
| W1-16 | carried over | recovery contract + SC-005 | Gap（可观测性） | REQ:163、140、214；CHK:47 | FR-028 要求 resume 前重验证授权，但只有失败路径有具名记录；没有记录区分「已重验证的恢复」与「未验证的恢复」。 | plan / contract |
| W1-17 | carried over | state-sync contract | Gap（写目标） | REQ:160；CHK:43 | FR-025 要求在下一个外部动作前持久化「边 + 已收到返回」，却未指明具体 per-entry 载体，而唯一被引用的 run report 是单文件产物。 | plan / contract |
| W1-18 | carried over | status-read contract | Inconsistency | REQ:161、167；CHK:44 | FR-026 要求从状态层、Assignment 事实层与宿主事件层派生，FR-029 又要求同一次状态读取；该单次读取覆盖哪几层未说明。 | plan / contract |
| W1-19 | carried over | digest contract + SC-006 | Ambiguity（有界性） | REQ:167、169；CHK:51 | 「条目 MUST 有界」未说明 cap 是单条还是整集、`omitted` 在哪个集合上声明，FR-031 的父 + 子形状可能被静默截断。 | plan / contract |
| W1-21 | carried over | dispatch-face contract + SC-002/003/007 | Coverage | REQ:175、211-216；CHK:59 | FR-034 要求 team 与 driver 阶段载荷携带角色字段，但 SC-002 只验证 run-agent 注入、SC-003 只验证边记录，两个接线点无验证。 | `/speckit.requirements` |
| W1-22 | carried over | test-plan + SC-009 | Ambiguity / Coverage | REQ:177、178、218；CHK:60 | FR-036 的「全套契约测试」未定义是 `contract` 标记、整个 `tests/` 还是具名模块清单，且没有 SC 验证改写 / 保持 / 移除处置台账。 | `/speckit.requirements` / plan |
| W1-23 | carried over | appendix contract + SC-010 | Measurability | REQ:182、219；CHK:68 | FR-038 / SC-010 要求「可解析证据路径」却未定义可解析（存在 / 可解析内容 / 命令可复现），也未把切片集钉到测量时点或 commit。 | `/speckit.requirements` |
| W1-25 | carried over | authorization contract | Ambiguity（形态覆盖） | REQ:140、130、269；CHK:37 | FR-014 的封闭授权面（能力键 / 席位策略 / 路由裁决 / team territory）未被证明能为 SSH 形态或通用非 SDD 扇出给出可解析授权依据。 | `/speckit.requirements` / plan |
| W1-26 | carried over | owner-doc assertions + SC-007 | Measurability | REQ:173、174、216、284；CHK:57 | FR-032 / FR-033 与 SC-007 禁止复制 owner 规则文本并要求转红，但没有客观判据区分合法指针与副本，红腿依赖散文判断。 | plan / contract |
| W1-33 | carried over | 等待 / 恢复契约（FR-012） | Gap / Traceability | REQ:138；CHK:35 | FR-012 要求按「既有阈值」区分 slow / stalled；锚点复读：watch-model 文档路径在句内，残留是**节级**阈值 / 分类 owner 未点名（原「全篇未给出 owner 路径」按字面过宽，claim 已收窄，severity 不变）。 | `/speckit.requirements`：FR-012 补节级 owner 路径 |
| W1-34 | carried over | SC-002 上行回传断言 | Inconsistency / Coverage | REQ:148、211、224 | SC-002 只断言双重角色上行回传的三个要素，而其测量源写「四项断言」、FR-019 定义四项（含边界与异常停止）；缺项可能在测试中被漏掉或被源清单补回。 | `/speckit.requirements`：SC-002 / SC-002 Source |
| W2-05 | carried over | 引擎边记录填充 + 确定性排序（P2） | Underspecification | DATA:21（`attempt`）、30-44（三载体形态）、ENG:37（edges `attempt`）、57（C-7 排序键） | `attempt` 是边必备键与确定性排序键，但三种可解析载体（team 映射表、driver sidecar、run-agent `unit_id`/`run_id` 对）均不携带 attempt，取值来源仍未声明。 | `/speckit.plan`/`data-model.md` §2.1：逐载体声明 attempt 取得规则 |
| W2-07 | carried over | 恢复 / 状态推导实现 + digest `state` 渲染（P2/P4） | Underspecification | DATA:63（§4 `state` 仅写 "enum"）、99（§8 消息类）、113（§10 恢复标记） | §10 仍把恢复中仍运行的子项标记 `interrupted` / `attention`，§4 的 `state` 却不再给任何值域，两标记未落入任何声明域；`attention` 与 §8 消息类 `attention-escalation` 的载体区分仍未给出。 | `/speckit.plan`/`data-model.md` §4/§10：声明标记字段与词表 owner，或删除标记 |
| W2-14 | carried over | 引擎身份解析实现 + 边排序夹具（plan → tasks） | Inconsistency（X-03 修复残留） | PLAN:33（D-5 内嵌顺序）、DATA:19（§2 root fallback）、46-52（§3 唯一 owner 顺序） | D-5 在声称「本行不携带第二套顺序」的同时仍内嵌根身份取值顺序（run_id → line_id → root）；DATA:19 的 root fallback 同为 run_id 先于 line_id，而 §3 的解析顺序把 line id 排在 run_id 之前——同一根同时持有两者时出现不同首选身份。 | `/speckit.plan`：删除 D-5 内嵌片段、仅留 §3 指针；DATA:19 与 §3 收敛为一套 |
| W2-15 | carried over | digest 实现 + `test_status_digest_roles.py` 的 `nothing-running` 断言（P4） | Underspecification（契约缝） | ENG:30（C-2 required roots）、DIG:7（C-1 默认根单次物化）、19（C-3 nothing-running） | 引擎把 `--teams-dir` / `--logs-dir` 列为必需根（缺失→2），digest 却要求经引擎默认根物化并承诺零条目渲染 `nothing-running`；没有条款声明默认根缺失时如何渲染，而 `.specify/teams` 与 `.specify/agents/execution/logs` 均非 CLI init 创建——空闲下游项目正落在该未定义缝上。 | `/speckit.plan`：digest 侧降级渲染 vs teams/logs 改 optional-empty 二选一定义，并给 P4 可判断言 |
| W3-06 | carried over | analyze 覆盖率汇总 / 实现 | Inconsistency（政策 vs 确定性 lane） | TASK:52（严格子集可接受留白）、90（T003） | 「严格子集可接受留白」政策与确定性 lane（本轮复跑 `status: uncovered`、exit 1、claimed 9、29 条 beyond 冻结基线）互斥；本文件无 DoD/GATE 覆盖该 lane。 | `/speckit.tasks` + 覆盖率契约 owner：裁定该 lane 是否成门，或记录其非门理由 |
| W3-11 | carried over | T045 验证证据 → SC-008 / SC-009 | Ambiguity / Inconsistency（验证命令作用域） | TASK:223（对照 `:157`、`:222`）；`scripts/bash/run-tests.sh:319` | T045 把三个模块与一个 `-k 'i14'` 组进同一反引号选择，而 runner 把全部参数**单次**转发 pytest，`-k` 作用于全部被收集项；`test_sdd_invocation_governance.py` 与 `test_nested_run_report.py` 中 "i14" 命中为 0，字面命令会静默取消这两个模块。 | `/speckit.tasks`：拆成独立调用或去掉 `-k` 分组 |
| X2-01 | carried over | tasks ↔ data-model ↔ engine contract | Inconsistency（义务落点） | TASK:129（T015 要求引擎实现 `state` derivation）、DATA:63（§4 state 为 digest 视图字段）、ENG:36（C-3 `executors[]` 键集无 `state`） | T015 要求引擎实现「executor `state` derivation per §4/§9」，而 §4 明确 `state`/`last_activity`/`age`/`stale` 是 digest 视图字段、非引擎输出键，C-3 键集也无 `state`——按 T015 实现与 C-3 schema 断言冲突，按 §4 实现则 T015 的 state 义务无落点。 | `/speckit.tasks`：T015 收窄为生命周期/既有载体引用；或 plan 同步 C-3 与测试 |
| X2-02 | carried over | requirements ↔ tasks | Coverage（测量源无生产者） | REQ:213、226（SC-004 / Source）、218、231（SC-009 / Source）；TASK:158（T028）、223（T045） | SC-004 Source 要求交错派发夹具与「预留后移」合成变异实测；SC-009 Source 要求「放宽禁令」合成变异实测；任务图没有创建该夹具或执行这两类变异演练的行（T028 只跑既有并发模块，T045 只跑绿+基线比对）。 | `/speckit.tasks`：为 SC-004 增补夹具 + 变异行；为 SC-009 变异半补行或声明由既有测试承担并点名 |

---

## 3. LOW（12 行；节内 ID 字典序）

| ID | Status | propagation_surface | Category | Anchors | 一句话事实 | 建议归属（指针） |
|----|--------|---------------------|----------|---------|------------|------------------|
| R3-03 | new（round-2 漏检） | 包级验证列（plan P2 → tasks T011） | Inconsistency（第三变异演练） | PLAN:222（P2 verification 写 `self-dispatch red`）、ENG:81（C-11 (c)「move a role claim off its edge」）、TASK:122（T011 第三演练 = 无父边的显式 `superagent` 断言） | 同一「三个变异演练」的第三项不同名：P2 列 `self-dispatch red`，C-11/T011 钉的是 unbacked-role-claim 演练。实现者若按 P2 列执行，第三项会被换成自派发而漏掉无背书声明。契约与测试 owner 一致，仅包级摘要行漂移。 | `/speckit.plan`：P2 第三项改为与 C-11/T011 同名 |
| W1-28 | carried over | 预算测量记录 | Traceability | REQ:285、174；CHK:58 | A13 记录三个字节数与 946 B 余量，但无可复现命令或证据路径，测量无法仅凭需求重导。 | `/speckit.requirements` |
| W1-29 | carried over | owner-doc assertions | Ambiguity | REQ:173、269；CHK:56 | FR-032 的 owner 文档内容清单要求「术语边界」，却未点名要消歧的术语，该节的完整性不可断言。 | `/speckit.requirements` |
| W1-35 | carried over | Shared Strings 引用图（合约 / 测试读取） | Traceability | REQ:38、49、53、103、239-243、245 | Shared Strings 反向引用仍不完整：表未列 US1 AS2 / US2 IT+AS1 的括号引用，US5 AS3 直接复制字面量 `not-observed` 而非 [[STR-006]]，且引用约定未声明 US 文本是否在范围内。 | `/speckit.requirements`：Shared Strings / citation convention |
| W2-12 | carried over | Feature 详情 → plan 的覆盖映射（读者/评审） | Coverage-gap | `feature-ref.md:14`（第 1 行）、`contracts/harness-landing.contract.md:19-25`（C-2 仅指针行） | feature-ref 第 1 行把「新 owner 页」映射到 harness C-2，而 C-2 只治理三个 sibling 的指针行；owner 页自身内容由 C-5 的 `test_superagent_definitions.py` + P1 守卫，映射不精确。 | `/speckit.plan`/`feature-ref.md`：改指 FR-001/P1 + C-5 测试，或 harness 补 owner 页条款 |
| W2-16 | carried over | 引擎 exit-code 契约测试（P2） | Inconsistency（闭表未同步） | ENG:28（C-2 code 2 行）、45（C-4 未知 query 身份） | C-2 自称 exit code 闭集且 code 2 仅定义「unreadable or malformed input」，C-4 却新增第三类触发（query 参数身份无法解析）且同为 2——行为一致、定义未收录。 | `/speckit.plan`：C-2 的 code-2 行补该触发条件（或 C-4 改引 C-2 条目） |
| W2-17 | carried over | `test_status_digest_roles.py` 字段存在断言（P4） | Ambiguity | DIG:11（C-2 首段）、13（C-2 按来源分 schema） | C-2 首段规定「每个渲染条目携带 `id` … `last_activity`」，第二段却规定 line 来源行保留 `line_id` / `last_activity_at` 且两类字段族不混行——同一契约内 `id` 既必须在每个条目出现、又不出现在 line 行上。 | `/speckit.plan`：首段改为「按来源族携带身份/活动字段」，与第二段同义 |
| W2-18 | carried over | `test_role_edge_engine.py` schema 断言（P2） | Underspecification | ENG:34（C-3 必需键）、30（C-2 `inputs` 提及） | C-3 把 `inputs` 与 `roots` 列为 report 必需键，但两键的形状与语义在契约与 data-model 中均未定义（C-2 只说 registry 缺失记入 `inputs`）。 | `/speckit.plan`：C-3 定义两键形状，或删除 `roots` 并入既有键 |
| W2-19 | carried over | none（叙述性；不阻断实现） | Inconsistency（载体族计数） | PLAN:173（EP-003「four-piece」但证据列举 `raw-` 第五类）、DATA:42（§2.1(b)「four-piece」）、实测另有 `runner-log-` | 状态文件族计数不一致且均不完整：plan EP-003 称四件套而证据列出五类名；data-model 称四件套；实测目录另有 `runner-log-`。 | `/speckit.plan`：统一载体族表述（按实测命名或声明「四件套」为解析子集） |
| W3-08 | carried over | 并行派发 | Inconsistency（机器标记 vs 散文） | TASK:151、284（并见 280、292） | T021 未标 `[P]` 而 `:280`/`:292` 称 T021–T025 可并行；`:284` 称 T049/T050 可与 T046 并行而三者均未标 `[P]`。 | `/speckit.tasks`：对齐 `[P]` 与说明，保持其一为 owner |
| W3-10 | carried over | 任务 → 实现 | Underspecification（未命名载体） | TASK:146、234（并见 54） | T019 的 "seven downlink role fields block" 与 T047 的 "a deterministic check" 仍未命名自身载体/实现归属，与本文件 `:54` 自定规则不一致。 | `/speckit.tasks`：为两处命名载体（夹具文件 / 检查脚本或其复用的 Tool） |
| X2-03 | carried over | requirements ↔ contracts / tasks（叙述性） | Traceability | REQ:126、242；DATA:15；ENG:32-39（C-3）；TASK 全文件 | STR-005 字面量 `role-edge` 只出现在 requirements 与 data-model 的叙述里；引擎 C-3 输出键集与全部任务/测试断言都没有该 record-kind 判别符——FR-003 的「唯一机读记录形态（record kind role-edge）」下游没有机器消费者。 | `/speckit.requirements` 或 `/speckit.plan`：把 kind 判别符加入 C-3/测试，或把 FR-003 的 kind 措辞改为对 §2 字段集的指称 |

---

## 4. Rerun Delta（相对 round-2）

### 4.1 Resolved Since Last Run（6 行；锚点证据）

| 上轮 ID | 原 severity | 关闭证据（本轮实读） |
|---------|-------------|----------------------|
| W1-30 | HIGH | `dual-role` 收敛为单一输出语义：FR-005（REQ:128）改由独立 `dispatch_duty` 承载授予事实，并声明 STR-002「只是角色集输出中的标记、MUST NOT 作为任何载体声明字段的取值」；Key Entities（REQ:197）与 SC-001（REQ:210）同步；DATA:13/22-23/37-40/71/76-83 值域改为 `subagent \| superagent` + 独立 `dispatch_duty`；PAY:7（C-1）声明 role claim 与 grant 分离且 role 永取不到 `dual-role`，PAY:54-57（C-11）与 PAY:67（C-13）同步；PLAN:34（D-6）/37（D-9）同步；TASK:101（T005）、122（T011）、123（T012）、129（T015）、147（T020）、152（T022）、153（T023）、155（T025）、178（T032）、296 同步；FEAT:20/49 同步。全篇 `dual-role` 复扫仅剩输出标记 / 「双重角色执行体」概念用法。**残留另立 R3-01**（标记的输出槽位）。 |
| W1-31 | HIGH | SC-009（REQ:218）改为**相对 implement 起点全量失败名单基线零新增失败**（与 FR-036 同一判据），点名基线既有红并禁止「全绿」声称；SC-009 Source（REQ:231）补基线逐条比对；T045（TASK:223）与 US5 checkpoint（TASK:225）同步。FR-036（REQ:177）、plan Inherited #4（PLAN:195）、GATE-1（TASK:31）复读确认为同一判据，无改动。 |
| W1-32 | HIGH | US1 故事叙述（REQ:29）补入「深度不一致」第四类；SC-001 Source（REQ:223）改为四类逐项枚举（`self-dispatch` / `dangling-parent` / `unbacked-role-claim` / `depth-inconsistent`）。全制品 `三类` 复扫 = 0（仅 dated checklist CHK003 保留其写作时提问，不作为现行读数）。 |
| W2-13 | HIGH | 载体声明域改为 `subagent \| superagent`：DATA:22（§2）、37-40（§2.1(a) 表+注）、71（§5）、82（§6）四处一致；ENG:65（C-9）显式声明 `superagent` 为已知值、由 C-5 判红（exit 1）、永不落 malformed（exit 2）；TASK:122（T011）严格输入子句同步。`unbacked-role-claim` 由此可达且单分类；「已授权未派发」由 `dispatch_duty: granted` 保持合法。 |
| W1-20 | MEDIUM | FR-030（REQ:168）映射表回写为 `label → 角色 → 派发职责 → 工作区 → 父身份`；DATA:35-37（§2.1(a) 五列）、PAY:55（C-11）、PLAN:37（D-9）、TASK:153（T023）、FEAT:49 一致。 |
| W2-20 | LOW | PLAN:34（D-6）改为 "no edge where it is the parent"；TASK:122（T011）与 TASK:129（T015）同向；与 DATA:71（§5）谓词一致。 |

### 4.2 New Since Last Run（3 行，含修复本身引入的）

- **R3-01（HIGH）**：W1-30 修复把 `dual-role` 变为输出专用标记，但输出 schema 未获标记槽位（§1）。
- **R3-02（MEDIUM）**：W2-13/W1-30 修复新增必备输出键 `dispatch_duty`，但三载体中的 (c) 不携带它（§2）。
- **R3-03（LOW）**：round-2 未检出的包级摘要漂移——plan P2 的第三变异演练与 C-11/T011 不同名（§3）。

### 4.3 Carried Over（38 行）

- **MEDIUM 27**：W1-07/08/09/10/12/13/14/15/16/17/18/19/21/22/23/25/26/33/34、W2-05/07/14/15、W3-06/11、X2-01/02（均在 §2 表内标注 `carried over`）。
- **LOW 11**：W1-28/29/35、W2-12/16/17/18/19、W3-08/10、X2-03（均在 §3 表内标注 `carried over`）。
- 维持理由：r3 修复轮授权仅覆盖 4 HIGH（+ 同句扇出的 W1-20/W2-20），其余 finding 的锚点在现行树上逐条复读仍成立；未修复、未拒绝、无静默丢条。

---

## 5. Coverage Summary

| 维度 | 读数 | 来源 |
|------|------|------|
| Clause coverage（本特性） | exit 1 / `status: uncovered`；claimed **9/38**；**29 beyond frozen baseline**（9 + 29 = 38 复算吻合） | 本轮复跑 `account-clause-coverage.py --spec-dir …`（2026-11-10T12:25Z） |
| FR 契约引用组 lane | claimed **20** / uncovered **18**（of 38） | 同上 |
| 语料级 | 290 文件 = 183 parsed + 107 named-unparseable；clause universe 2037（2056 ids，19 collapsed）；1 parse doubt；**47 error / 1 warning** | 同上 |
| Baseline | 640 names；640 baseline-internal uncovered 不阻断；delta 29 为阻断项 | 同上 |
| FR 任务行引用 | **38 / 38**（机械复扫无缺） | 本轮 grep 复算 |
| SC 任务行引用 | **10 / 10**（机械复扫无缺） | 本轮 grep 复算 |
| Checklist 问责（pass H） | 39 = **21 raised + 18 covered-by + 0** unraised/undispositioned；`[Gap]` 子集 10 = 6 + 4 + 0 | §9 |
| Feature linkage | 1 / 1 consistent | §6 |

**零 finding 底线**: 不适用（本轮 findings 非零；零 finding 主张的证据要求未触发）。

---

## 6. Feature Linkage Summary

| 检查 | 读数 |
|------|------|
| Feature 绑定 | `requirements.md` Related Feature 095（REQ:14-15）↔ `.specify/features.md:102` 行 ↔ `.specify/features/095-superagent-role.md`（ID / Name / Spec Path 一致） |
| 状态 | 索引行与详情文件均 `Planned`；analyze 不在 `feature-integration.md` § Status State Machine 的生命周期命令表内，无状态迁移义务，保持 `Planned` 合法 |
| 阶段记账 | 详情文件含 Overview / Key Changes / Implementation Notes / Clarify Notes / Plan Notes / Related Specifications / Related Files / Status Criteria；`Last Updated: 2026-11-10`；r3 修复已把 `dispatch_duty` 分离与七字段写回 Implementation Notes 与 Plan Notes（FEAT:20/49） |
| 邻域 | Related Features（027 / 085 / 093）只在详情文件记录，未改对方产物；无失效 / 新引入 Feature |
| 结论 | **无 finding**（W2-10 的注册表漂移在 round-2 已关闭，本轮复读保持） |

---

## 7. Constitution Alignment Issues

- **CRITICAL: 0**。宪法 22 条原则（live roster：I…XXII，本轮机械核对 22 个标题；plan 的 Constitution Check 恰为 22 行且全 pass）。
- r3 修复只改字段语义 / 值域 / 指针，未新增持久化根、registry、renderer、dispatcher 或第二通道；未改动 owner 规则文本；无宪法 MUST 冲突。
- **XIV（One Source of Truth）边界说明**: `superagent` / `dispatch_duty` 值域与七字段清单在 FR / data-model / contracts 多处出现，但截至本轮**各处一致**（不存在会漂移的副本冲突）；`dual-role` 的语义已单点收敛。若修复 R3-01 时以第二套词汇另立标记槽位，将立即构成 XIV 问题——那是修复轮的义务，不是本轮 finding。
- **R3 新发现均非宪法级**：R3-01 是输出契约缺口（不是 owner 冲突）；R3-02 是载体来源缺口；R3-03 是摘要行漂移。按技能规则，宪法冲突才自动 CRITICAL——本三项不适用。

---

## 8. Unmapped Tasks

- 54 条任务行全部带 FR/SC 括号引用；FR-001…FR-038 与 SC-001…SC-010 在 `tasks.md` 中均可解析（38/38、10/10）。
- 无「任务无需求」或「需求无任务」的新增断点；round-2 的 X2-02（SC Source 无生产者）仍是**测量源**问题，不是任务-需求映射缺失，已在 §2 保留。

---

## 9. Checklist Accountability（pass H）

**等式**：39 unchecked = **21 raised-as-finding + 18 covered-by + 0 unraised/undispositioned**（round-2 的 25+14 中，CHK002 / CHK003 / CHK027 / CHK038 因对应 finding 在 r3 关闭而转为 covered-by）。

- CHK001 disposition: covered-by requirements.md §FR-001 / §FR-002
- CHK002 disposition: covered-by requirements.md §FR-002 / §FR-005 / §Key Entities / §SC-001（W1-30 已修复；标记的输出槽位由 R3-01 跟踪）
- CHK003 disposition: covered-by requirements.md §FR-005 / §US1 / §SC-001 / §SC-001 Source（W1-32 已修复，四类逐处一致）
- CHK004 disposition: covered-by requirements.md §FR-005
- CHK005 disposition: raised-as-finding W1-07
- CHK006 disposition: raised-as-finding W1-08
- CHK007 disposition: raised-as-finding W1-09
- CHK008 disposition: raised-as-finding W1-10
- CHK009 disposition: covered-by requirements.md §FR-008 / §FR-001 / §FR-005（dated 快照：六字段枚举不因 r3 七字段回写）
- CHK010 disposition: covered-by requirements.md §FR-022 (d) / §FR-011 (e) / §FR-010 + Clarifications Q3 (g)
- CHK011 disposition: covered-by requirements.md §FR-017（恰好九项、不得增项）
- CHK012 disposition: covered-by requirements.md §FR-018（逐项句柄；字面量 owner 指向 data-model.md §7）
- CHK013 disposition: raised-as-finding W1-12
- CHK014 disposition: raised-as-finding W1-13
- CHK015 disposition: raised-as-finding W1-14
- CHK016 disposition: raised-as-finding W1-33（FR-013 半边 covered-by requirements.md §FR-013）
- CHK017 disposition: covered-by requirements.md §FR-009 / §FR-019 / §FR-020
- CHK018 disposition: raised-as-finding W1-25
- CHK019 disposition: covered-by requirements.md §FR-022 / §FR-024
- CHK020 disposition: covered-by requirements.md §FR-022 / §FR-023
- CHK021 disposition: raised-as-finding W1-17
- CHK022 disposition: raised-as-finding W1-18
- CHK023 disposition: covered-by requirements.md §FR-026 / §SC-005
- CHK024 disposition: raised-as-finding W1-15
- CHK025 disposition: raised-as-finding W1-16
- CHK026 disposition: raised-as-finding W1-19
- CHK027 disposition: covered-by requirements.md §FR-030 / §FR-029（W1-20 已修复：五列含派发职责与父身份）
- CHK028 disposition: raised-as-finding W1-29
- CHK029 disposition: raised-as-finding W1-26
- CHK030 disposition: raised-as-finding W1-28（触发条件半边 covered-by requirements.md §FR-033 / §A7）
- CHK031 disposition: raised-as-finding W1-21
- CHK032 disposition: raised-as-finding W1-22
- CHK033 disposition: covered-by requirements.md §FR-035 / §SC-008 / Measurement Sources SC-008
- CHK034 disposition: covered-by requirements.md §SC-003 / §US3 Independent Test / §A3
- CHK035 disposition: covered-by requirements.md §FR-038 + Clarifications Q5（FR-033 段位置）
- CHK036 disposition: raised-as-finding W1-35
- CHK037 disposition: raised-as-finding W1-23
- CHK038 disposition: covered-by requirements.md §A15 / §FR-002 / §FR-005 / §Key Entities（W1-30 已修复；`dual-role` 只作输出标记）
- CHK039 disposition: covered-by checklists/requirements-quality-2026-11-10.md §七（39/39 均可由需求正文或点名 owner 行回答）

**`[Gap]` 子集**：按 tag 列表任意位置匹配 **10** = 6 raised（CHK008 / 015 / 016 / 021 / 024 / 025）+ 4 covered-by（CHK004 / 010 / 019 / 039）+ 0 undispositioned。

---

## 10. Systemic Observations（簇级，不抬升单行 severity）

- **SO-3A（语义收窄后输出槽位未补）**: W1-30 把 `dual-role` 收窄为输出标记后，未给标记落点（R3-01）；同型：`dispatch_duty` 作为新增必备输出键却有一个载体无来源（R3-02）。教训：字段级修复必须同时检查「必备键 × 每个载体」的笛卡尔面与「声明出的输出事实 × 每个输出 schema」。
- **SO-3B（包级摘要行漂移）**: R3-03——修复扇出扫的是 FR / 契约正文，plan 的 Work Package 验证列未被任何守卫钉住，第三变异演练保留旧名。
- **SO-3C（dated 快照，非 finding）**: checklist 头部尺寸快照（287 行 / 53,696 B）、CHK003 的「只判三类」、CHK009 的六字段枚举、Clarifications Q2 的六字段枚举——均为写作时点的 dated record；按 One Source of Truth 的 dated-record 豁免不作为 finding，且 checklist 自身协议禁止就地刷新（复核须新建 recheck 文件）。下游读者不得把它们当现行读数。
- **SO-3D（deferred 簇未动）**: 27 条 carried MEDIUM 与 11 条 carried LOW 集中在字段级 schema / 载体命名（输入树、conflict 输出、attempt id、消息与终止载体、恢复标记、digest cap、state 义务落点）——r3 修复范围不含它们，维持原归属；清门前应由各 owner 逐簇闭合或显式延后。
- **SO-3E（并发读数与验证形态）**: 本轮 `requested=24 / effective=1 / reason=budget-reserve`，无法派发独立验证波；C/H 采用 direct re-read fallback。多轮 analyze 在同一弱面上反复出现「修复残留」，提示修复轮应把**被修复事实的所有输出/载体落点**列为同轮机械扫全面。

---

## 11. Metrics

| 指标 | 值 |
|------|-----|
| 本轮 findings | **41**（0C / 1H / 28M / 12L）：新增 3（1H / 1M / 1L）+ carried 38（27M / 11L） |
| Round-2 基线 | 44（0C / 4H / 28M / 12L）→ 关闭 6（4H + 1M + 1L）→ 新增 3 → 开放 41 |
| C/H 验证 | 无独立验证波（`effective=1`）；R3-01 = `validated (direct re-read, subagent unavailable)`；downgrade rate **n/a** |
| 跨文件重复 ID（本轮主表） | **0**（carried ID 唯一 + R3-01/02/03 新命名空间；机械复算见下） |
| Requirements | validator `status: ok`；6 标签全 pass；288 行 / 48 定义行 / 6 shared strings；0 error / 0 warning，exit 0；38 FR / 10 SC（final 7 / supporting 3）/ 6 STR / 5 US / 10 Edge / 16 Q / 15 A |
| Tasks | `validate-tasks.py` PASS 0 error / 0 warning，exit 0；54 行 / 8 阶段；22 `[P]`；38 `blockedBy`；9 green |
| Decision tensions | `validate-decision-tensions.py` `status: ok`；6 检查全 pass；247 行 / 2 records（T-001 / T-002） |
| Contract clauses | 38（engine 11 + payload 13 + digest 8 + harness 6）；claimed 9 + beyond 29 = 38 复算吻合 |
| 50 行上限 | 41 ≤ 50，无裁剪 |

---

## 12. Next Actions（技能 §9；不自动修复）

1. **HIGH（1）**: R3-01 → `/speckit.plan` 修订 C-3/C-10 + D-8/P2/T011/T012/T036 的标记槽位（或由 `/speckit.requirements` 收窄 SC-001 断言——须单一 owner，不得两处各改一半）。
2. **MEDIUM（28）**: R3-02 → `/speckit.plan`（§2.1(c) 或 C-3）；其余按 §2 各行归属指针分流（requirements 与 plan/contract 侧居多）。
3. **LOW（12）**: R3-03 → `/speckit.plan` P2 行；其余可随修订一并处置或显式延后（`/speckit.todo` / 处置台账）。
4. **验证波 / 门禁**: 正式门禁前应补一次独立只读验证波（fresh-context、与检测者不相交），或由 U4 显式裁决 R3-01；本报告不冒充该结论。
5. 本报告未应用任何修复编辑；后续命令由驱动者/用户自行发起。

## 13. Limitations

- **未运行测试套件**（analyze 只读）；R3-01/R3-02 的「必红 / 无来源」结论来自契约与测试文本的逐字比对，不是实测读数。
- **未派发独立验证波**（并发读数 `effective=1`，`budget-reserve`）；R3-01 的 severity 与证据边界是检测者提议值，U4 裁决前不得作为门禁结论。其余 MEDIUM/LOW 跳过验证（技能规则）。
- carried-over 行的锚点在现行树上逐条复读仍成立，但未逐条重新做跨制品扩展；W1-33 的 claim 已按实读收窄（见 §2 行内注）。
- dated 快照（checklist 头部尺寸、CHK003/CHK009、Clarifications Q2 的字段枚举）按 One Source of Truth 豁免，不刷新、不计 finding。
- 本轮复裁以提交 `e3fd9cb51` 的修复面为对象；该提交之后的树未再变动（只读证明：提交前 `git status --porcelain` 与阶段开始时一致，仅新增本报告与 `.specify/.tmp/` 临时捕获）。
