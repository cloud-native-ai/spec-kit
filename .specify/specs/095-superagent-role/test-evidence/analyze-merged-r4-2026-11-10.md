# Analyze Merged Report — Round 4（095-superagent-role，2026-11-10）

- **Stage**: analyze 第四轮（r4 修复后重过门）· **Line**: `095-superagent-role` · 线 run `r20261110T055657Z-b095` · 本轮单元 run `r20261110T055657Z-b095-r4`
- **Contract**: `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md` / `references/validation-and-report.md`；宪法 `.specify/constitution.md`
- **Inputs**: `test-evidence/analyze-merged-r3-2026-11-10.md`（round-3 基线，41 行 = 0C/1H/28M/12L）+ `analyze-repair-dispositions-r4-2026-11-10.md` + `analyze-repair-gates-r4-2026-11-10.txt`（r4 修复面）；现行制品全文：`requirements.md`、`plan.md`、`tasks.md`、`data-model.md`、`contracts/`×4、`quickstart.md`、`feature-ref.md`、`checklists/`×2、`.specify/features.md` 095 行与 `.specify/features/095-superagent-role.md`
- **Round-4 口径**: 全严重度重裁——① r4 修复面复裁（R3-01 的 `role_set_marker` 单槽位）；② round-3 的 40 行开放项逐条复裁（锚点在现行树重读）；③ 全制品重新检测（A/B/C/D/E/F/G/I + H）。修复轮 r4 只改 R3-01 表面（提交 `f95454f54`），未改 carried 行的事实。
- **并发读数**: `requested=24`；`effective=1`；`effective_reason=budget-reserve`（可用槽位 < 2）——单 Worker 串行；**未派发独立验证波**
- **C/H 复核标记**: 本轮开放 CRITICAL/HIGH = **0**；唯一 C/H 动作为 R3-01 的关闭复核，标记 **validated（direct re-read；subagent unavailable）**；本轮**无 proposed 行**（没有新检出 C/H）。severity 归属仍以 U4/独立验证波为最终裁决。
- **只读声明**: 本轮未修改任何 spec 制品、未修复任何 finding、未 push；除本报告与 Wrap-up 记账外无写点（临时捕获在 `.specify/.tmp/`，已被忽略）
- **锚点图例**: `REQ:` = `requirements.md`；`PLAN:` = `plan.md`；`TASK:` = `tasks.md`；`DATA:` = `data-model.md`；`ENG:` / `PAY:` / `DIG:` / `HAR:` = `contracts/role-edge-engine` / `role-transition-payload` / `status-digest-role-view` / `harness-landing`；`CHK:` = `checklists/requirements-quality-2026-11-10.md`；`FEAT:` = `.specify/features/095-superagent-role.md`（行号均为本轮实读，含 r4 插入造成的行号漂移后的现行值）

---

## 0. 顶部汇总：CRITICAL / HIGH（计数 + 逐条指针，不修复）

**集成后计数**: CRITICAL **0** · HIGH **0** · MEDIUM **28** · LOW **13** = **41 行**（round-3 开放 40 行 + 本轮新增 1 行 LOW；round-3 的 1 条 HIGH 经复核关闭，转入 §4.1）。

- **C/H 关闭复核**: **R3-01（HIGH）→ fixed，validated（direct re-read, subagent unavailable）**；逐层锚点证据见 §4.1。
- **HEADLINE（两种主张分开读）**: r3 的 C/H 遗留**已清**（0C / 0H）；但本次 rerun **不是零 finding**——新增 LOW 1（R4-01：两处摘要仍以「角色集（含 …）」措辞复述 r4 已消除的成员读法），且 **40 条 carried MEDIUM/LOW 全部维持**。「C/H 已清」≠「门禁干净」，更 ≠「MEDIUM/LOW 已处置」。
- 50 行上限：41 ≤ 50，无裁剪、无溢出。

**C/H 指针表（本轮）**

| ID | 上轮 severity | 本轮复核 | Validation | 指针 |
|----|---------------|-----------|-----------|------|
| R3-01 | HIGH | **fixed（关闭）** | validated（direct re-read, subagent unavailable） | §4.1（逐层锚点：REQ:210 / DATA:10,13,61,64 / ENG:36-37,46,78 / DIG:11,13,28,32 / PLAN:36,222,224 / TASK:122,123,178,179,193,198 / FEAT:20） |

**门禁含义（技能 §9，不修复）**: CRITICAL 0；HIGH 0。C/H 面已无开放项，但 U4 仍需对「40 条 carried MEDIUM/LOW + 1 条新 LOW 维持开放」作显式放行裁决；**本报告不得被读作「ready to implement」**。

---

## 1. HIGH（0 行）

本轮无开放 HIGH。round-3 的唯一 HIGH（R3-01）经 r4 修复后按锚点逐层复读确认关闭（§4.1），不计入主表。

---

## 2. MEDIUM（28 行；节内 ID 字典序）

| ID | Status | propagation_surface | Category | Anchors | 一句话事实 | 建议归属（指针） |
|----|--------|---------------------|----------|---------|------------|------------------|
| R3-02 | carried over | 引擎实现 + `test_role_edge_engine.py` schema 断言（P2） | Underspecification（字段来源） | DATA:23（§2 `dispatch_duty` 必备 + 语义）、44（§2.1(c) run-agent 载体仅 `unit_id`/`run_id`）、84（§6）；ENG:38（C-3 `edges[]` 必备 `dispatch_duty`） | `dispatch_duty` 是边记录必备字段与 C-3 必备输出键，但三载体中只有 (a) 映射行与 (b) sidecar 明确携带它；(c) `run-agent`/exec-quant 记录不含该字段。仅经 (c) 出现的边，该键取值无来源声明（`role_declaration` 尚有「本边即 subagent」的默认语义，`dispatch_duty` 没有），引擎只能在「省略（违反 C-3）」与「自行默认（未声明）」之间选择。 | `/speckit.plan`：在 §2.1(c) 声明取得规则（如按边默认 `not-granted`），或让 C-3 该键在 (c) 来源上可为 `null` |
| W1-07 | carried over | role-edge contract | Ambiguity（输入边界） | REQ:128、126；CHK:21 | FR-005 未定义输入记录集与执行树边界（单根 / 多根、跨 run 无关记录如何隔离），边与深度在不同仓库上不可确定。 | plan / contract |
| W1-08 | carried over | role-edge contract + SC 集 | Inconsistency（覆盖） | REQ:126、128、210-219；CHK:22 | FR-003 要求 `conflict` 报错并点名两处路径，但 FR-005 的输出枚举没有它、也没有任何 SC 验证它，该 MUST 既无输出归宿也无红测（引擎 C-8 已给出 `conflicts` 行，但需求层枚举未同步）。 | `/speckit.requirements` / plan |
| W1-09 | carried over | role-edge contract | Ambiguity（优先级） | REQ:126、283；CHK:23 | FR-003 允许根身份取状态脊 `run_id` 或 line registry `line_id` 而未给优先级，A11 只把实现名交给 plan。 | plan / contract（见 W2-14） |
| W1-10 | carried over | role-edge / return contract + SC-005 | Underspecification（Gap） | REQ:126、139、214；CHK:24 | 边记录要求「派发尝试标识」，FR-013 的重试 / 陈旧判定依赖它，但没有既有字段被指明为该标识。 | plan / contract（≡ W2-05） |
| W1-12 | carried over | protocol contract | Ambiguity（owner + 可扩展性） | REQ:136、262；CHK:32 | FR-010 声明封闭消息分类集却把 owner 写成未具名的「owner 文档」，同时又说「最少区分四类」，owner 与可扩展规则都未固定。 | `/speckit.requirements` |
| W1-13 | carried over | protocol contract | Gap（载体） | REQ:136、142；CHK:33 | 四类消息中的 `ack` 与 `attention-escalation` 未映射到任何既有载荷 / 回传通道，行使它们就会造出 FR-016 禁止的第二通道。 | plan / contract |
| W1-14 | carried over | edge lifecycle contract | Gap（载体） | REQ:141；CHK:34 | FR-015 要求把 `completed / failed / cancelled` 写入既有载体，但没有既有记录被指明承载 `cancelled`。 | plan / contract |
| W1-15 | carried over | recovery contract + SC-005 | Gap（词表 / 载体） | REQ:162、214；CHK:46 | FR-027 / SC-005 要求把仍被判定在跑的子项标为 `interrupted` / `attention`，但词表 owner 与承载标记的记录都未具名。 | plan / contract（≡ W2-07） |
| W1-16 | carried over | recovery contract + SC-005 | Gap（可观测性） | REQ:163、140、214；CHK:47 | FR-028 要求 resume 前重验证授权，但只有失败路径有具名记录；没有记录区分「已重验证的恢复」与「未验证的恢复」。 | plan / contract |
| W1-17 | carried over | state-sync contract | Gap（写目标） | REQ:160；CHK:43 | FR-025 要求在下一个外部动作前持久化「边 + 已收到返回」，却未指明具体 per-entry 载体，而唯一被引用的 run report 是单文件产物。 | plan / contract |
| W1-18 | carried over | status-read contract | Inconsistency | REQ:161、167；CHK:44 | FR-026 要求从状态层、Assignment 事实层与宿主事件层派生，FR-029 又要求同一次状态读取；该单次读取覆盖哪几层未说明。 | plan / contract |
| W1-19 | carried over | digest contract + SC-006 | Ambiguity（有界性） | REQ:167、169；CHK:51 | 「条目 MUST 有界」未说明 cap 是单条还是整集、`omitted` 在哪个集合上声明，FR-031 的父 + 子形状可能被静默截断（DIG C-3 只部分回答：cap 作用于合并集）。 | plan / contract |
| W1-21 | carried over | dispatch-face contract + SC-002/003/007 | Coverage | REQ:175、211-216；CHK:59 | FR-034 要求 team 与 driver 阶段载荷携带角色字段，但 SC-002 只验证 run-agent 注入、SC-003 只验证边记录，两个接线点无验证。 | `/speckit.requirements` |
| W1-22 | carried over | test-plan + SC-009 | Ambiguity / Coverage | REQ:177、178、218；CHK:60 | FR-036 的「全套契约测试」未定义是 `contract` 标记、整个 `tests/` 还是具名模块清单，且没有 SC 验证改写 / 保持 / 移除处置台账。 | `/speckit.requirements` / plan |
| W1-23 | carried over | appendix contract + SC-010 | Measurability | REQ:182、219；CHK:68 | FR-038 / SC-010 要求「可解析证据路径」却未定义可解析（存在 / 可解析内容 / 命令可复现），也未把切片集钉到测量时点或 commit。 | `/speckit.requirements` |
| W1-25 | carried over | authorization contract | Ambiguity（形态覆盖） | REQ:140、130、269；CHK:37 | FR-014 的封闭授权面（能力键 / 席位策略 / 路由裁决 / team territory）未被证明能为 SSH 形态或通用非 SDD 扇出给出可解析授权依据。 | `/speckit.requirements` / plan |
| W1-26 | carried over | owner-doc assertions + SC-007 | Measurability | REQ:173、174、216、284；CHK:57 | FR-032 / FR-033 与 SC-007 禁止复制 owner 规则文本并要求转红，但没有客观判据区分合法指针与副本，红腿依赖散文判断。 | plan / contract |
| W1-33 | carried over | 等待 / 恢复契约（FR-012） | Gap / Traceability | REQ:138；CHK:35 | FR-012 要求按「既有阈值」区分 slow / stalled；锚点复读：watch-model 文档路径在句内，残留是**节级**阈值 / 分类 owner 未点名。 | `/speckit.requirements`：FR-012 补节级 owner 路径 |
| W1-34 | carried over | SC-002 上行回传断言 | Inconsistency / Coverage | REQ:148、211、224 | SC-002 只断言双重角色上行回传的三个要素，而其测量源写「四项断言」、FR-019 定义四项（含边界与异常停止）；缺项可能在测试中被漏掉或被源清单补回。 | `/speckit.requirements`：SC-002 / SC-002 Source |
| W2-05 | carried over | 引擎边记录填充 + 确定性排序（P2） | Underspecification | DATA:21（`attempt`）、30-44（三载体形态）、ENG:38（edges `attempt`）、58（C-7 排序键） | `attempt` 是边必备键与确定性排序键，但三种可解析载体（team 映射表、driver sidecar、run-agent `unit_id`/`run_id` 对）均不携带 attempt，取值来源仍未声明。 | `/speckit.plan`/`data-model.md` §2.1：逐载体声明 attempt 取得规则 |
| W2-07 | carried over | 恢复 / 状态推导实现 + digest `state` 渲染（P2/P4） | Underspecification | DATA:64（§4 `state` 仅写 "enum"）、99（§8 消息类）、107/115（§10 恢复标记） | §10 仍把恢复中仍运行的子项标记 `interrupted` / `attention`，§4 的 `state` 却不再给任何值域，两标记未落入任何声明域；`attention` 与 §8 消息类 `attention-escalation` 的载体区分仍未给出。 | `/speckit.plan`/`data-model.md` §4/§10：声明标记字段与词表 owner，或删除标记 |
| W2-14 | carried over | 引擎身份解析实现 + 边排序夹具（plan → tasks） | Inconsistency（X-03 修复残留） | PLAN:33（D-5 指向 §3 后仍残留旧文）、DATA:19（§2 root fallback `run_id` 先于 `line_id`）、46-52（§3 顺序 `line id` 先于 `run_id`） | D-5 已改为「本行不携带第二套顺序」，但 DATA:19 的 root fallback 仍为 run_id 先于 line_id，而 §3 的解析顺序把 line id 排在 run_id 之前——同一根同时持有两者时出现不同首选身份。 | `/speckit.plan`：DATA:19 与 §3 收敛为一套 |
| W2-15 | carried over | digest 实现 + `test_status_digest_roles.py` 的 `nothing-running` 断言（P4） | Underspecification（契约缝） | ENG:30（C-2 required roots）、DIG:7（C-1 默认根单次物化）、19（C-3 nothing-running） | 引擎把 `--teams-dir` / `--logs-dir` 列为必需根（缺失→2），digest 却要求经引擎默认根物化并承诺零条目渲染 `nothing-running`；没有条款声明默认根缺失时如何渲染，而 `.specify/teams` 与 `.specify/agents/execution/logs` 均非 CLI init 创建——空闲下游项目正落在该未定义缝上。 | `/speckit.plan`：digest 侧降级渲染 vs teams/logs 改 optional-empty 二选一定义，并给 P4 可判断言 |
| W3-06 | carried over | analyze 覆盖率汇总 / 实现 | Inconsistency（政策 vs 确定性 lane） | TASK:52（严格子集可接受留白）、90（T003） | 「严格子集可接受留白」政策与确定性 lane（本轮复跑 `status: uncovered`、exit 1、claimed 9、29 条 beyond 冻结基线）互斥；本文件无 DoD/GATE 覆盖该 lane。 | `/speckit.tasks` + 覆盖率契约 owner：裁定该 lane 是否成门，或记录其非门理由 |
| W3-11 | carried over | T045 验证证据 → SC-008 / SC-009 | Ambiguity / Inconsistency（验证命令作用域） | TASK:223（对照 `:157`、`:222`）；`scripts/bash/run-tests.sh:319` | T045 把三个模块与一个 `-k 'i14'` 组进同一反引号选择，而 runner 把全部参数**单次**转发 pytest，`-k` 作用于全部被收集项；`test_sdd_invocation_governance.py` 与 `test_nested_run_report.py` 中 "i14" 命中为 0，字面命令会静默取消这两个模块。 | `/speckit.tasks`：拆成独立调用或去掉 `-k` 分组 |
| X2-01 | carried over | tasks ↔ data-model ↔ engine contract | Inconsistency（义务落点） | TASK:129（T015 要求引擎实现 `state` derivation）、DATA:64（§4 state 为 digest 视图字段、非引擎输出键）、ENG:36（C-3 `executors[]` 键集无 `state`） | T015 要求引擎实现「executor `state` derivation per §4/§9」，而 §4 明确 `state`/`last_activity`/`age`/`stale` 是 digest 视图字段、非引擎输出键，C-3 键集也无 `state`——按 T015 实现与 C-3 schema 断言冲突，按 §4 实现则 T015 的 state 义务无落点。 | `/speckit.tasks`：T015 收窄为生命周期/既有载体引用；或 plan 同步 C-3 与测试 |
| X2-02 | carried over | requirements ↔ tasks | Coverage（测量源无生产者） | REQ:213、226（SC-004 / Source）、218、231（SC-009 / Source）；TASK:158（T028）、223（T045） | SC-004 Source 要求交错派发夹具与「预留后移」合成变异实测；SC-009 Source 要求「放宽禁令」合成变异实测；任务图没有创建该夹具或执行这两类变异演练的行（T028 只跑既有并发模块，T045 只跑绿+基线比对）。 | `/speckit.tasks`：为 SC-004 增补夹具 + 变异行；为 SC-009 变异半补行或声明由既有测试承担并点名 |

---

## 3. LOW（13 行；节内 ID 字典序）

| ID | Status | propagation_surface | Category | Anchors | 一句话事实 | 建议归属（指针） |
|----|--------|---------------------|----------|---------|------------|------------------|
| R3-03 | carried over | 包级验证列（plan P2 → tasks T011） | Inconsistency（第三变异演练） | PLAN:222（P2 verification 写 `self-dispatch red`）、ENG:82（C-11 (c)「move a role claim off its edge」）、TASK:122（T011 第三演练 = 无父边的显式 `superagent` 断言） | 同一「三个变异演练」的第三项不同名：P2 列 `self-dispatch red`，C-11/T011 钉的是 unbacked-role-claim 演练。实现者若按 P2 列执行，第三项会被换成自派发而漏掉无背书声明。契约与测试 owner 一致，仅包级摘要行漂移。 | `/speckit.plan`：P2 第三项改为与 C-11/T011 同名 |
| R4-01 | **new（r4 修复残留）** | none（摘要 / 叙述层；权威契约与任务行已单一化） | Inconsistency（摘要措辞残留） | FEAT:10（Key Changes 2「判定边、角色集（含 [[STR-002]]）、深度…」）、TASK:134（US1 checkpoint「角色集（含 `dual-role`）」）；对照 DATA:10、13、61（标记永不作集合成员） | r4 把 `dual-role` 收敛为独立输出键 `role_set_marker` 后，两处摘要仍以「角色集（含 …）」措辞书写，字面可读作标记是集合成员——正是 W1-30 / R3-01 消除的读法。权威层（SC-001 / data-model / 契约 / T011）已无该歧义，故属叙述残留；r4 的机械扫只匹配字面 `dual-role`，未覆盖 `[[STR-002]]` 与「含」组合的变体。 | Feature 详情与 `/speckit.tasks` 后续修订同批改指 `role_set_marker`（或「含双重角色情形」），无需单开修复轮 |
| W1-28 | carried over | 预算测量记录 | Traceability | REQ:285、174；CHK:58 | A13 记录三个字节数与 946 B 余量，但无可复现命令或证据路径，测量无法仅凭需求重导。 | `/speckit.requirements` |
| W1-29 | carried over | owner-doc assertions | Ambiguity | REQ:173、269；CHK:56 | FR-032 的 owner 文档内容清单要求「术语边界」，却未点名要消歧的术语，该节的完整性不可断言。 | `/speckit.requirements` |
| W1-35 | carried over | Shared Strings 引用图（合约 / 测试读取） | Traceability | REQ:38、49、53、103、239-243、245 | Shared Strings 反向引用仍不完整：表未列 US1 AS2 / US2 IT+AS1 的括号引用，US5 AS3 直接复制字面量 `not-observed` 而非 [[STR-006]]，且引用约定未声明 US 文本是否在范围内。 | `/speckit.requirements`：Shared Strings / citation convention |
| W2-12 | carried over | Feature 详情 → plan 的覆盖映射（读者/评审） | Coverage-gap | `feature-ref.md:14`（第 1 行）、`contracts/harness-landing.contract.md:19-25`（C-2 仅指针行） | feature-ref 第 1 行把「新 owner 页」映射到 harness C-2，而 C-2 只治理三个 sibling 的指针行；owner 页自身内容由 C-5 的 `test_superagent_definitions.py` + P1 守卫，映射不精确。 | `/speckit.plan`/`feature-ref.md`：改指 FR-001/P1 + C-5 测试，或 harness 补 owner 页条款 |
| W2-16 | carried over | 引擎 exit-code 契约测试（P2） | Inconsistency（闭表未同步） | ENG:28（C-2 code 2 行）、46（C-4 未知 query 身份） | C-2 自称 exit code 闭集且 code 2 仅定义「unreadable or malformed input」，C-4 却新增第三类触发（query 参数身份无法解析）且同为 2——行为一致、定义未收录。 | `/speckit.plan`：C-2 的 code-2 行补该触发条件（或 C-4 改引 C-2 条目） |
| W2-17 | carried over | `test_status_digest_roles.py` 字段存在断言（P4） | Ambiguity | DIG:11（C-2 首段）、13（C-2 按来源分 schema） | C-2 首段规定「每个渲染条目携带 `id` … `last_activity`」，第二段却规定 line 来源行保留 `line_id` / `last_activity_at` 且两类字段族不混行——同一契约内 `id` 既必须在每个条目出现、又不出现在 line 行上。 | `/speckit.plan`：首段改为「按来源族携带身份/活动字段」，与第二段同义 |
| W2-18 | carried over | `test_role_edge_engine.py` schema 断言（P2） | Underspecification | ENG:34（C-3 必需键）、30（C-2 `inputs` 提及） | C-3 把 `inputs` 与 `roots` 列为 report 必需键，但两键的形状与语义在契约与 data-model 中均未定义（C-2 只说 registry 缺失记入 `inputs`）。 | `/speckit.plan`：C-3 定义两键形状，或删除 `roots` 并入既有键 |
| W2-19 | carried over | none（叙述性；不阻断实现） | Inconsistency（载体族计数） | PLAN:173（EP-003「four-piece」但证据列举 `raw-` 第五类）、DATA:42（§2.1(b)「four-piece」）、实测另有 `runner-log-` | 状态文件族计数不一致且均不完整：plan EP-003 称四件套而证据列出五类名；data-model 称四件套；实测目录另有 `runner-log-`。 | `/speckit.plan`：统一载体族表述（按实测命名或声明「四件套」为解析子集） |
| W3-08 | carried over | 并行派发 | Inconsistency（机器标记 vs 散文） | TASK:151、280、284（并见 292） | T021 未标 `[P]` 而 `:280`/`:292` 称 T021–T025 可并行；`:284` 称 T049/T050 可与 T046 并行而三者均未标 `[P]`。 | `/speckit.tasks`：对齐 `[P]` 与说明，保持其一为 owner |
| W3-10 | carried over | 任务 → 实现 | Underspecification（未命名载体） | TASK:146、234（并见 54） | T019 的 "seven downlink role fields block" 与 T047 的 "a deterministic check" 仍未命名自身载体/实现归属，与本文件 `:54` 自定规则不一致。 | `/speckit.tasks`：为两处命名载体（夹具文件 / 检查脚本或其复用的 Tool） |
| X2-03 | carried over | requirements ↔ contracts / tasks（叙述性） | Traceability | REQ:126、242；DATA:15；ENG:32-39（C-3）；TASK 全文件 | STR-005 字面量 `role-edge` 只出现在 requirements 与 data-model 的叙述里；引擎 C-3 输出键集与全部任务/测试断言都没有该 record-kind 判别符——FR-003 的「唯一机读记录形态（record kind role-edge）」下游没有机器消费者。 | `/speckit.requirements` 或 `/speckit.plan`：把 kind 判别符加入 C-3/测试，或把 FR-003 的 kind 措辞改为对 §2 字段集的指称 |

---

## 4. Rerun Delta（相对 round-3）

### 4.1 Resolved Since Last Run（1 行；锚点证据）

| 上轮 ID | 原 severity | 关闭证据（本轮实读；提交 `f95454f54`） | 复核标记 |
|---------|-------------|--------------------------------------|-----------|
| R3-01 | HIGH | **单槽位已契约化并全链同步**：SC-001（REQ:210）改述「标记由角色集输出的独立机读键承载，键名在 plan 阶段固定于 `data-model.md`；只出现于角色集输出、MUST NOT 作集合成员、不作载体声明取值」；DATA:10/13 声明标记经独立输出键 `role_set_marker` 承载、永不入 `roles` 数组；DATA:61 固定键名/值域（`"dual-role"` \| null）/「`roles` 的确定性投影」，DATA:64 把该键列入引擎输出键清单；ENG:36-37 把 `role_set_marker` 列入 `executors[]` 必备键并定义投影语义与三条禁止，ENG:46 query 的 `parent`/`child` 对象同构携带该键，ENG:78（C-10）钉 A=`"dual-role"`、B/root=`null` 与 query 一致性；DIG:11/13/28/32 声明条目必备该键、由引擎模型透传（never re-derived）、来源族与 JSON 形状同步；PLAN:36（D-8）、222（P2）、224（P4）同步键名与断言点；TASK:122（T011 断言 `executors[].role_set_marker`）、123（T012 fixture 驱动）、178（T032）、179（T033 读数）、193（T034）、198（T036 透传）同步；FEAT:20 记录该键与 data-model 指针。**两种原读法均被排除**：A「`dual-role` 作为第三个 `roles` token」被 DATA:10/ENG:37/C-10 的两项数组钉死排除；B「无任何键承载」被 C-3 必备键 + C-10 期望值排除。 | validated（direct re-read, subagent unavailable） |

### 4.2 New Since Last Run（1 行，含修复本身引入的）

- **R4-01（LOW）**：r4 修复把 `dual-role` 收敛为独立输出键后，Feature 详情 `:10` 与 tasks US1 checkpoint `:134` 仍以「角色集（含 …）」措辞复述成员读法；权威层无此歧义，属摘要残留（§3）。

### 4.3 Carried Over（40 行）

- **MEDIUM 28**：R3-02、W1-07/08/09/10/12/13/14/15/16/17/18/19/21/22/23/25/26/33/34、W2-05/07/14/15、W3-06/11、X2-01/02（均在 §2 表内标注 `carried over`）。
- **LOW 12**：W1-28/29/35、W2-12/16/17/18/19、W3-08/10、X2-03、R3-03（均在 §3 表内标注 `carried over`）。
- 维持理由：r4 修复轮只改 R3-01 表面；carried 行的锚点在本轮现行树上逐条复读仍成立（r4 插入造成的行号漂移已按现行行号重写），未修复、未拒绝、无静默丢条。

---

## 5. Coverage Summary

| 维度 | 读数 | 来源 |
|------|------|------|
| Clause coverage（本特性） | exit 1 / `status: uncovered`；claimed **9/38**；**29 beyond frozen baseline**（9 + 29 = 38 复算吻合） | 本轮复跑 `account-clause-coverage.py --spec-dir …`（2026-11-10T12:40Z） |
| FR 契约引用组 lane | claimed **20** / uncovered **18**（of 38） | 同上 |
| 语料级 | 290 文件 = 183 parsed + 107 named-unparseable；clause universe 2037；1 parse doubt；**47 error / 1 warning** | 同上 |
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
| 阶段记账 | 详情文件含 Overview / Key Changes / Implementation Notes / Clarify Notes / Plan Notes / Related Specifications / Related Files / Status Criteria；`Last Updated: 2026-11-10`；r4 修复已把 `role_set_marker` 写回 Implementation Notes（FEAT:20），Key Changes（FEAT:10）的「角色集（含 …）」措辞属 R4-01 |
| 邻域 | Related Features（027 / 085 / 093）只在详情文件记录，未改对方产物；无失效 / 新引入 Feature |
| 结论 | 无 Feature 级 finding（R4-01 是同一文件内的摘要措辞残留，不是绑定漂移） |

---

## 7. Constitution Alignment Issues

- **CRITICAL: 0**。宪法 22 条原则（live roster：`### I`…`### XXII`，本轮机械核对 22 个标题；plan 的 Constitution Check 恰为 22 行且全 pass）。
- r4 修复只改字段语义 / 值域 / 指针，未新增持久化根、registry、renderer、dispatcher 或第二通道；未改动 owner 规则文本；无宪法 MUST 冲突。
- **XIV（One Source of Truth）边界说明**: `superagent` / `dispatch_duty` 值域与七字段清单在 FR / data-model / contracts 多处出现，但截至本轮**各处一致**；`dual-role` 的语义与键名已单点收敛（键名 owner = `data-model.md` §4，SC-001 只声明「键名归 plan」，不复制名字）。
- R3-01 的关闭**未引入第二套词汇**：`role_set_marker` 只在 data-model 首次命名，plan / tasks / digest 契约均为引用与断言，不构成 XIV 副本冲突。

---

## 8. Unmapped Tasks

- 54 条任务行全部带 FR/SC 括号引用；FR-001…FR-038 与 SC-001…SC-010 在 `tasks.md` 中均可解析（38/38、10/10）。
- 无「任务无需求」或「需求无任务」的新增断点；round-2 的 X2-02（SC Source 无生产者）仍是**测量源**问题，不是任务-需求映射缺失，已在 §2 保留。

---

## 9. Checklist Accountability（pass H）

**等式**：39 unchecked = **21 raised-as-finding + 18 covered-by + 0 unraised/undispositioned**（与 r3 相同；R3-01 的关闭不改变任何 CHK 归属——CHK002 / CHK038 自 r3 起即为 covered-by）。

- CHK001 disposition: covered-by requirements.md §FR-001 / §FR-002
- CHK002 disposition: covered-by requirements.md §FR-002 / §FR-005 / §Key Entities / §SC-001（标记槽位已由 r4 修复关闭）
- CHK003 disposition: covered-by requirements.md §FR-005 / §US1 / §SC-001 / §SC-001 Source
- CHK004 disposition: covered-by requirements.md §FR-005
- CHK005 disposition: raised-as-finding W1-07
- CHK006 disposition: raised-as-finding W1-08
- CHK007 disposition: raised-as-finding W1-09
- CHK008 disposition: raised-as-finding W1-10
- CHK009 disposition: covered-by requirements.md §FR-008 / §FR-001 / §FR-005（dated 快照：六字段枚举不因七字段回写）
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
- CHK038 disposition: covered-by requirements.md §A15 / §FR-002 / §FR-005 / §Key Entities（标记槽位已由 r4 修复关闭；dated 快照不刷新）
- CHK039 disposition: covered-by checklists/requirements-quality-2026-11-10.md §七（39/39 均可由需求正文或点名 owner 行回答）

**`[Gap]` 子集**：按 tag 列表任意位置匹配 **10** = 6 raised（CHK008 / 015 / 016 / 021 / 024 / 025）+ 4 covered-by（CHK004 / 010 / 019 / 039）+ 0 undispositioned。

---

## 10. Systemic Observations（簇级，不抬升单行 severity）

- **SO-4A（修复扫的变体盲区）**: r4 修复把「标记 × 输出槽位」的笛卡尔面收干净了（R3-01 关闭），但其机械扫只匹配字面 `dual-role`；仍有两处用 `[[STR-002]]` / 「含」组合措辞的摘要未被覆盖（R4-01）。教训：修复轮的复扫模式应同时覆盖「字面量」「Shared String 引用」「语义组合词（含/并/加）」三种形态。
- **SO-4B（C/H 清零不等于可放行）**: 本轮 0C/0H，但 40 条 carried MEDIUM/LOW 全部维持，其中 X2-01 / W2-14 / W3-11 / R3-02 会在实现时直接变成错误代码或错误测试命令。门禁裁决必须把「C/H 面」与「M/L 处置面」分开陈述。
- **SO-4C（dated 快照，非 finding）**: checklist 头部尺寸快照（287 行 / 53,696 B）、CHK003 的「只判三类」、CHK009 的六字段枚举、Clarifications Q2 的六字段枚举——均为写作时点的 dated record；按 One Source of Truth 的 dated-record 豁免不作为 finding，且 checklist 自身协议禁止就地刷新（复核须新建 recheck 文件）。
- **SO-4D（反复残留的修复面）**: 连续四轮出现「修复引入新 finding」（R3-01/R3-02/R3-03 → R4-01），且两条落在同型摘要面。建议后续修复轮把「被修复事实的所有落点」按 `grep` 三形态（字面量 / `[[STR-]]` / 组合词）写成固定清单，而不是逐点人工回读。

---

## 11. Metrics

| 指标 | 值 |
|------|-----|
| 本轮 findings | **41**（0C / 0H / 28M / 13L）：新增 1（R4-01 LOW）+ carried 40（28M / 12L） |
| Round-3 基线 | 41（0C / 1H / 28M / 12L）→ 关闭 1（R3-01 HIGH）→ 新增 1 → 开放 41 |
| C/H 验证 | 无独立验证波（`effective=1`）；R3-01 关闭复核 = `validated (direct re-read, subagent unavailable)`；本轮新增 C/H 0；downgrade rate **n/a** |
| 跨文件重复 ID（本轮主表） | **0**（carried ID 唯一 + R4-01 新命名空间；机械复算见下） |
| Requirements | validator `status: ok`；6 标签全 pass；288 行 / 48 定义行 / 6 shared strings；0 error / 0 warning，exit 0；38 FR / 10 SC（final 7 / supporting 3）/ 6 STR / 5 US / 10 Edge / 16 Q / 15 A |
| Tasks | `validate-tasks.py` PASS 0 error / 0 warning，exit 0；54 行 / 8 阶段；22 个 `[P]` 行；37 个 `[blockedBy:]` 行；9 个 `[green:]` 声明（5 行） |
| Decision tensions | `validate-decision-tensions.py` `status: ok`；6 检查全 pass；247 行 / 2 records（T-001 / T-002） |
| Contract clauses | 38（engine 11 + payload 13 + digest 8 + harness 6）；claimed 9 + beyond 29 = 38 复算吻合 |
| 50 行上限 | 41 ≤ 50，无裁剪 |

---

## 12. Next Actions（技能 §9；不自动修复）

1. **CRITICAL / HIGH（0）**: 无开放项；R3-01 已关闭并有锚点证据。门禁放行仍须 U4 对 §2/§3 的 41 行开放集作显式裁决。
2. **MEDIUM（28）**: R3-02 → `/speckit.plan`（§2.1(c) 或 C-3）；其余按 §2 各行归属指针分流（requirements 与 plan/contract 侧居多）；建议优先处置 X2-01 / W2-14 / W3-11 / W2-15 / W3-06——它们会在实现阶段直接转化为错误代码或错误测试命令。
3. **LOW（13）**: R4-01 随 Feature 详情 / `tasks.md` 的任一后续修订同批改指 `role_set_marker`（无需单开修复轮）；R3-03 → `/speckit.plan` P2 行；其余可随修订一并处置或显式延后（`/speckit.todo` / 处置台账）。
4. **验证波 / 门禁**: 正式门禁前应补一次独立只读验证波（fresh-context、与检测者不相交），或由 U4 显式裁决；本报告不冒充该结论。
5. 本报告未应用任何修复编辑；后续命令由驱动者/用户自行发起。

## 13. Limitations

- **未运行测试套件**（analyze 只读）；R4-01 的「字面可读作集合成员」结论来自文本比对，不是可执行读数。
- **未派发独立验证波**（并发读数 `effective=1`，`budget-reserve`）；R3-01 的关闭复核与 severity 边界是 direct re-read 提议值，U4 裁决前不得作为门禁结论。
- carried-over 行的锚点在现行树上逐条复读仍成立，但未逐条重新做跨制品扩展；行号已按 r4 插入后的现行树重读（如 ENG C-4 `45→46`、C-7 `57→58`、C-11 `81→82`、DATA §4 `state 63→64`、§6 `dispatch_duty 83→84`）。
- dated 快照（checklist 头部尺寸、CHK003/CHK009、Clarifications Q2 的字段枚举、A15 的术语记录）按 One Source of Truth 豁免，不刷新、不计 finding。
- 本轮复裁以提交 `f95454f54` 的修复面为对象；该提交之后的树未再变动（只读证明：提交前 `git status --porcelain` 与阶段开始时一致，仅新增本报告与 `.specify/.tmp/` 临时捕获）。