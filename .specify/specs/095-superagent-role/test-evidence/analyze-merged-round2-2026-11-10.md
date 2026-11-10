# Analyze Merged Report — Round 2（095-superagent-role，2026-11-10）

- **Stage**: analyze 第二轮（修复后重过门，一轮为限）· **Line**: `095-superagent-role` · 线 run `r20261110T055657Z-b095` · 集成者作用域 run `r20261110T055657Z-b095-r2merge`
- **Contract**: `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md` / `references/validation-and-report.md`；宪法 `.specify/constitution.md`
- **Inputs（本报告的唯一来源，按读域次序）**: `test-evidence/analyze-findings-round2-W1.md`（requirements × requirements-quality checklist）、`-round2-W2.md`（plan / data-model / quickstart / feature-ref / contracts×4）、`-round2-W3.md`（tasks）。跨制品节另读：`requirements.md`、`plan.md`、`tasks.md`、`data-model.md`、`contracts/`×4 全文，以及上轮 `analyze-merged-2026-11-10.md` 与 `analyze-repair-dispositions-2026-11-10.md`。
- **Deterministic engines（本阶段复跑）**: `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/095-superagent-role` → **exit 1，`status: uncovered`**（claimed 9；baseline 640 names；**29 beyond frozen baseline**；FR claimed 20 / uncovered 18；669 uncovered；107 named-unparseable；290 文件 = 183 parsed + 107 unparsable；clause universe 2037；1 parse doubt；47 error / 1 warning）。ID 机械复算：W1 主表 **26** 行、W2 主表 **11** 行、W3 主表 **4** 行；跨文件主表重复 ID = **0**。专项只读核对：`exec-quant.py` 的 `collect-dispatch` 动作存在（data-model §2.1(c) 载体前提成立）；`watch-model.md` 在框架源与运行时两侧均存在；`role-edge-check.py` 两侧均不存在（EP-004 前提成立）；Feature 095 索引行与详情内容已按 plan D-2/D-6 收敛（修复关闭核验，`features.md:102` / `features/095-superagent-role.md:10`）。
- **只读声明**: 本集成未修改任何分析制品（除本报告与 Wrap-up 记账）；未修复任何 finding、未派发新 Worker、未 push。
- **Round-2 口径**: 三个 Worker 均为**全严重度重裁**（round-1 findings 逐条复裁 + residue 登记 + 全集扫描）；MEDIUM/LOW 按技能规则跳过独立验证波。
- **C/H 验证状态**: 本集成简报（读三份 findings → 归并 → 跨制品检查 → 提交 → 记账）**未派发独立验证波**；下列 HIGH 均为**检测者提议值**，集成者逐条重读锚点并做跨制品扩展（标记 `(re-read by integrator)`）；独立验证与门禁裁决归驱动的 U4。**本报告不得被读作「ready to implement」**。

---

## 0. 顶部汇总：CRITICAL / HIGH（计数 + 逐条指针，不修复）

**集成后计数**: CRITICAL **0** · HIGH **4** · MEDIUM **28** · LOW **12** = **44 行**（Worker 41 + 跨制品新增 3）。

- 分源：W1 **26**（0C / 3H / 20M / 3L）· W2 **11**（0C / 1H / 4M / 6L）· W3 **4**（0C / 0H / 2M / 2L）· 跨制品新增 **3**（0C / 0H / 2M / 1L）
- 上轮对照：round-1 为 2C / 12H / 32M / 8L → **CRITICAL 清零**；HIGH 12 → **4**；MEDIUM/LOW 余量以 deferred 字段级 schema 簇为主
- 50 行上限：44 ≤ 50，无裁剪、无溢出

| # | ID | 来源 | 一句话指针 | 锚点 |
|---|----|------|-----------|------|
| 1 | **W1-30** | W1 | 同一字面量 `dual-role` 双语义：集合形态机读标记（STR-002 / Key Entities / SC-001）vs「已授予派发职责」声明值（FR-005，且未用 [[STR-002]]），契约无法仅凭 token 判别 | REQ:125、128、197、210、239 |
| 2 | **W1-31** | W1 | SC-009 要求四类既有治理契约测试「全绿」，FR-036 完成门却是「相对 implement 起点基线零新增失败 + 基线既有红豁免」；基线若含这四类红则两条不可同时满足 | REQ:177、218；plan:195；tasks:31 |
| 3 | **W1-32** | W1 | W1-04 修复未扫全：SC-001 Source 仍写「违例三类」、US1 故事只列三类示例，与 FR-005 / US1 AS3 / SC-001 四类矛盾 | REQ:29、39、128、210、223 |
| 4 | **W2-13** | W2 | `unbacked-role-claim` 要求载体声明值取 `superagent`，但两处具名载体声明域封闭为 `subagent \| dual-role`，C-9 又规定已知表内未知值 = malformed → exit 2：该违例不可达，或同一行同时落入 exit 2 与 exit 1 | data-model:22、37、40、71、82；engine C-5:49、C-9:65 |

**门禁含义（技能 §9，不修复）**: CRITICAL 0；HIGH 4 须经处置或经验证波 / U4 显式裁决后才可放行 implement；MEDIUM/LOW 可带建议推进。X2 新增 3 条不改变本结论。

---

## 1. W1 — requirements × requirements-quality checklist（读域次序 1）

- **Unit**: `/speckit.analyze` round-2 Worker W1 · Worker run `r20261110T055657Z-b095-r2w1`
- **Read domain（文件级互斥）**: `.specify/specs/095-superagent-role/requirements.md`、`.specify/specs/095-superagent-role/checklists/requirements-quality-2026-11-10.md`
- **归并核对**: 26 行，ID `W1-07…W1-35`（字典序，已机械复算）；severity = 0 CRITICAL / 3 HIGH / 20 MEDIUM / 3 LOW

### 1.1 Findings（当前开放集，原文表；节内按 ID 字典序）

| ID | Status | Severity | Propagation surface | Category | Anchor(s) | 一句话事实 | 建议归属（指针） |
|----|--------|----------|---------------------|----------|-----------|------------|------------------|
| W1-07 | carried over | MEDIUM | role-edge contract | Ambiguity（输入边界） | REQ:128、126；CHK:21 | FR-005 未定义输入记录集与执行树边界（单根 / 多根、跨 run 无关记录如何隔离），边与深度在不同仓库上不可确定。 | plan / contract |
| W1-08 | carried over | MEDIUM | role-edge contract + SC 集 | Inconsistency（覆盖） | REQ:126、128、210-219；CHK:22 | FR-003 要求 `conflict` 报错并点名两处路径，但 FR-005 的输出枚举没有它、也没有任何 SC 验证它，该 MUST 既无输出归宿也无红测。 | `/speckit.requirements` / plan |
| W1-09 | carried over | MEDIUM | role-edge contract | Ambiguity（优先级） | REQ:126、283；CHK:23 | FR-003 允许根身份取状态脊 `run_id` 或 line registry `line_id` 而未给优先级，A11 只把实现名交给 plan。 | plan / contract（X-03 指 data-model §3） |
| W1-10 | carried over | MEDIUM | role-edge / return contract + SC-005 | Underspecification（Gap） | REQ:126、139、214；CHK:24 | 边记录要求「派发尝试标识」，FR-013 的重试 / 陈旧判定依赖它，但没有既有字段被指明为该标识。 | plan / contract |
| W1-12 | carried over | MEDIUM | protocol contract | Ambiguity（owner + 可扩展性） | REQ:136、262；CHK:32 | FR-010 声明封闭消息分类集却把 owner 写成未具名的「owner 文档」，同时又说「最少区分四类」，owner 与可扩展规则都未固定。 | `/speckit.requirements` |
| W1-13 | carried over | MEDIUM | protocol contract | Gap（载体） | REQ:136、142；CHK:33 | 四类消息中的 `ack` 与 `attention-escalation` 未映射到任何既有载荷 / 回传通道，行使它们就会造出 FR-016 禁止的第二通道。 | plan / contract |
| W1-14 | carried over | MEDIUM | edge lifecycle contract | Gap（载体） | REQ:141；CHK:34 | FR-015 要求把 `completed / failed / cancelled` 写入既有载体，但没有既有记录被指明承载 `cancelled`。 | plan / contract |
| W1-15 | carried over | MEDIUM | recovery contract + SC-005 | Gap（词表 / 载体） | REQ:162、214；CHK:46 | FR-027 / SC-005 要求把仍被判定在跑的子项标为 `interrupted` / `attention`，但词表 owner 与承载标记的记录都未具名。 | plan / contract |
| W1-16 | carried over | MEDIUM | recovery contract + SC-005 | Gap（可观测性） | REQ:163、140、214；CHK:47 | FR-028 要求 resume 前重验证授权，但只有失败路径有具名记录；没有记录区分「已重验证的恢复」与「未验证的恢复」。 | plan / contract |
| W1-17 | carried over | MEDIUM | state-sync contract | Gap（写目标） | REQ:160；CHK:43 | FR-025 要求在下一个外部动作前持久化「边 + 已收到返回」，却未指明具体 per-entry 载体，而唯一被引用的 run report 是单文件产物。 | plan / contract |
| W1-18 | carried over | MEDIUM | status-read contract | Inconsistency | REQ:161、167；CHK:44 | FR-026 要求从状态层、Assignment 事实层与宿主事件层派生，FR-029 又要求同一次状态读取；该单次读取覆盖哪几层未说明。 | plan / contract（W2-01 共享物化） |
| W1-19 | carried over | MEDIUM | digest contract + SC-006 | Ambiguity（有界性） | REQ:167、169；CHK:51 | 「条目 MUST 有界」未说明 cap 是单条还是整集、`omitted` 在哪个集合上声明，FR-031 的父 + 子形状可能被静默截断。 | plan / contract |
| W1-20 | carried over | MEDIUM | run-report mapping + digest contract | Inconsistency | REQ:167、168；CHK:52 | FR-029 要求每行显示父边身份，FR-030 的映射表 schema（`label → 角色 → 工作区`）没有父列，也未给 join 规则。 | `/speckit.requirements` / plan |
| W1-21 | carried over | MEDIUM | dispatch-face contract + SC-002/003/007 | Coverage | REQ:175、211-216；CHK:59 | FR-034 要求 team 与 driver 阶段载荷携带角色字段，但 SC-002 只验证 run-agent 注入、SC-003 只验证边记录，两个接线点无验证。 | `/speckit.requirements` |
| W1-22 | carried over | MEDIUM | test-plan + SC-009 | Ambiguity / Coverage | REQ:177、178、218；CHK:60 | FR-036 的「全套契约测试」未定义是 `contract` 标记、整个 `tests/` 还是具名模块清单，且没有 SC 验证改写 / 保持 / 移除处置台账。 | `/speckit.requirements` / plan |
| W1-23 | carried over | MEDIUM | appendix contract + SC-010 | Measurability | REQ:182、219；CHK:68 | FR-038 / SC-010 要求「可解析证据路径」却未定义可解析（存在 / 可解析内容 / 命令可复现），也未把切片集钉到测量时点或 commit。 | `/speckit.requirements` |
| W1-25 | carried over | MEDIUM | authorization contract | Ambiguity（形态覆盖） | REQ:140、130、69-70；CHK:37 | FR-014 的封闭授权面（能力键 / 席位策略 / 路由裁决 / team territory）未被证明能为 SSH 形态或通用非 SDD 扇出给出可解析授权依据。 | `/speckit.requirements` / plan |
| W1-26 | carried over | MEDIUM | owner-doc assertions + SC-007 | Measurability | REQ:173、174、216、284；CHK:57 | FR-032 / FR-033 与 SC-007 禁止复制 owner 规则文本并要求转红，但没有客观判据区分合法指针与副本，红腿依赖散文判断。 | plan / contract |
| W1-28 | carried over | LOW | 预算测量记录 | Traceability | REQ:285、174；CHK:58 | A13 记录三个字节数与 946 B 余量，但无可复现命令或证据路径，测量无法仅凭需求重导。 | `/speckit.requirements` |
| W1-29 | carried over | LOW | owner-doc assertions | Ambiguity | REQ:173、269；CHK:56 | FR-032 的 owner 文档内容清单要求「术语边界」，却未点名要消歧的术语，该节的完整性不可断言。 | `/speckit.requirements` |
| W1-30 | new（W2-02 修复残留） | **HIGH** | `role-edge` 契约 + SC-001 角色集输出 | Inconsistency / Ambiguity | REQ:125、128、197、210、239 | 同一机读字面量 `dual-role` 同时被定义为「双角色集合标记」（STR-002 / Key Entities / SC-001）与「已授予派发职责的声明值」（FR-005），且 FR-005 用字面量而非 [[STR-002]]；契约无法仅凭 token 判别语义。 | `/speckit.requirements`：FR-005 / Shared Strings / Key Entities |
| W1-31 | new（X-01 同根残留） | **HIGH** | implement 完成门（SC-009 → verification.log） | Inconsistency / containment claim | REQ:177、218 | SC-009 要求四类既有治理契约测试「全绿」，而 FR-036 把完成门判据定义为相对 implement 起点基线的零新增失败并豁免基线既有红；若基线含这四类测试的既有红，两条判据不可同时满足。 | `/speckit.requirements`：SC-009（对齐 FR-036 或点名基线绿证据） |
| W1-32 | residual of W1-04 | **HIGH** | SC-001 测量源 → test-evidence 夹具 | Inconsistency / Coverage | REQ:29、39、128、210、223 | W1-04 修复未扫到测量源与故事叙述：SC-001 Source 仍写「违例三类」，US1 故事只列三类示例，与 FR-005 / US1 AS3 / SC-001 的四类违例矛盾。 | `/speckit.requirements`：SC-001 Source + US1 叙述 |
| W1-33 | new（CHK016 残留） | MEDIUM | 等待 / 恢复契约（FR-012） | Gap / Traceability | REQ:138；CHK:35 | FR-012 要求按「既有阈值」区分 slow / stalled，但全篇未给出该阈值或分类的 owner 路径（FR-013 的 attribution owner 已在 W1-01 修复中补上）。 | `/speckit.requirements`：FR-012 补 owner 路径（或 plan/contract） |
| W1-34 | new | MEDIUM | SC-002 上行回传断言 | Inconsistency / Coverage | REQ:148、211、224 | SC-002 只断言双重角色上行回传的三个要素，而其测量源写「四项断言」、FR-019 定义四项（含边界与异常停止）；缺项可能在测试中被漏掉或被源清单补回。 | `/speckit.requirements`：SC-002 / SC-002 Source |
| W1-35 | residual of W1-27 | LOW | Shared Strings 引用图（合约 / 测试读取） | Traceability | REQ:38、49、53、103、239-243、245 | Shared Strings 反向引用仍不完整：表未列 US1 AS2 / US2 IT+AS1 的括号引用，US5 AS3 直接复制字面量 `not-observed` 而非 [[STR-006]]，且引用约定未声明 US 文本是否在范围内。 | `/speckit.requirements`：Shared Strings / citation convention |

### 1.2 Round-1 delta / residue 摘要（全文见 Worker 文件 §Residue Registry）

- **上轮 29 条**：8 fixed（W1-01/02/03/05/06/11/24/27）+ 1 partially-fixed（W1-04 → 残留重报 W1-32）+ 20 deferred + 0 rejected。
- **Checklist 问责（pass H）**: 39 unchecked = **25 raised-as-finding + 14 covered-by + 0 unraised/undispositioned**；`[Gap]` 子集（任意位置匹配）= 10 = 6 raised + 4 covered-by + 0（W1 修正上轮「9」的口径：CHK039 的 `Gap` 位于 tag 第二位）。
- **读域内宪法面**: W1-01（XIV）与 W1-02（Feature Documentation Requirements）已核验关闭；无新增 CRITICAL。W1-30 按 F 不一致（HIGH）报告而非 XIV；若验证者把 Shared Strings 行读作该 token 的语义 owner，则按 XIV 升为 CRITICAL（归验证波裁决）。
- **其他检测面**: A 重复 0 条新增；E（task 覆盖）与 I（decision tension）不在读域；G Feature linkage 一致（095 行 / 详情 / 需求绑定）；SO-R2-1…5 见 Worker 文件 §Systemic Observations。

---

## 2. W2 — plan / data-model / quickstart / feature-ref / contracts×4（读域次序 2）

- **Unit**: `/speckit.analyze` round-2 Worker W2 · Worker run `r20261110T055657Z-b095-r2w2`
- **Read domain（文件级互斥，8 文件）**: `plan.md`、`data-model.md`、`quickstart.md`、`feature-ref.md`、`contracts/harness-landing.contract.md`、`contracts/role-edge-engine.contract.md`、`contracts/role-transition-payload.contract.md`、`contracts/status-digest-role-view.contract.md`
- **归并核对**: 11 行，ID `W2-05…W2-20`（字典序，已机械复算）；severity = 0 CRITICAL / 1 HIGH / 4 MEDIUM / 6 LOW

### 2.1 Findings（本轮主表，原文表；节内按 ID 字典序）

| ID | 类别 | propagation_surface | Severity | 锚点 | 一句话事实 | 建议归属（指针） |
|----|------|---------------------|----------|------|------------|------------------|
| W2-05 | underspecification | 引擎边记录填充 + 确定性排序（P2） | MEDIUM | `data-model.md:21`（`attempt`）、`:30-44`（三载体形态）、`contracts/role-edge-engine.contract.md:37`（edges `attempt`）、`:57`（C-7 排序键） | **(carried over)** `attempt` 是边必备键与确定性排序键，但三种可解析载体（team 映射表、driver sidecar 六字段、run-agent `unit_id`/`run_id` 对）均不携带 attempt，取值来源仍未声明（修复轮未处置，显式 deferred） | `/speckit.plan`/`data-model.md` §2.1：逐载体声明 attempt 取得规则（如 report stamp / 产物后缀） |
| W2-07 | underspecification | 恢复/状态推导实现 + digest `state` 渲染（P2/P4） | MEDIUM | `data-model.md:63`（§4 `state` 仅写 "enum"）、`:99`（§8 消息类）、`:113`（§10 恢复标记） | **(carried over)** §10 仍把恢复中仍运行的子项标记 `interrupted` / `attention`，§4 的 `state` 却不再给任何值域，两标记未落入任何声明域，`attention` 与 §8 消息类 `attention-escalation` 的载体区分仍未给出（修复轮未处置，显式 deferred；原闭域冲突已改为值域沉默） | `/speckit.plan`/`data-model.md` §4/§10：声明标记的字段与词表 owner，或删除标记 |
| W2-12 | coverage-gap | Feature 详情 → plan 的覆盖映射（读者/评审） | LOW | `feature-ref.md:14`（第 1 行）、`contracts/harness-landing.contract.md:19-25`（C-2 仅指针行） | **(carried over)** feature-ref 第 1 行仍把「新 owner 页」映射到 harness C-2，而 C-2 只治理三个 sibling 的指针行；owner 页自身内容由 C-5 的 `test_superagent_definitions.py` + P1 守卫，映射不精确（修复轮未处置，显式 deferred） | `/speckit.plan`/`feature-ref.md` 第 1 行：改指 FR-001/P1 + C-5 测试，或 harness 补 owner 页条款 |
| W2-13 | inconsistency（违例不可达） | 引擎实现 + `test_role_edge_engine.py`（P2 变异演练 c） + C-9 输入严格性测试 | **HIGH**（提议值） | `data-model.md:71`（§5 谓词）、`:37`（§2.1(a) 行形 role 值域）、`:22`（§2 表 `role_declaration` 值域）、`:82`（§6 同值域）、`:40`（§2.1(a) 注）；`contracts/role-edge-engine.contract.md:49`（C-5）、`:65`（C-9） | `unbacked-role-claim` 的谓词要求某载体声明值取 `superagent`，但两处具名载体的声明域均封闭为 `subagent \| dual-role`，而 C-9 规定已知表内未知值 = malformed → exit 2——按字面实现，该违例或不可达，或同一行同时落入 exit 2（C-9）与 exit 1（C-5）两个相反判定 | `/speckit.plan` 修订轮：把 `superagent` 纳入载体声明值域（§2/§2.1(a)/§6 三处同步）或改指其他可解析断言载体；C-5/C-9 同步 |
| W2-14 | inconsistency（X-03 修复残留） | 引擎身份解析实现 + 边排序夹具（plan → tasks） | MEDIUM | `plan.md:33`（D-5 内嵌顺序）、`data-model.md:46-52`（§3 唯一 owner 顺序） | plan D-5 在声称「本行不携带第二套顺序」的同时仍内嵌根身份取值顺序（run_id → line_id → literal root），与 data-model §3（line_id 先于 run_id）优先级相反；同一根同时持有 line_id 与 run_id 时两处给出不同首选身份 | `/speckit.plan`：删除 D-5 内嵌片段、仅留 §3 指针（或反向把 §3 顺序回写为与 D-5 一致——须单一 owner） |
| W2-15 | underspecification（契约缝） | digest 实现 + `test_status_digest_roles.py` 的 `nothing-running` 断言（P4） | MEDIUM | `contracts/role-edge-engine.contract.md:30`（C-2 required roots）、`contracts/status-digest-role-view.contract.md:7`（C-1 默认根单次物化）、`:19`（C-3 nothing-running） | 引擎把 `--teams-dir` / `--logs-dir` 列为必需根（缺失→2），digest 却要求经引擎默认根物化并承诺零条目渲染 `nothing-running`；没有任何条款声明 digest 在默认根缺失时如何渲染，而 `.specify/teams` 与 `.specify/agents/execution/logs` 均非 CLI init 创建（实测 `src/specify_cli/__init__.py` 零引用）——空闲下游项目正落在该未定义缝上 | `/speckit.plan`：C-2 与该缝二选一定义（digest 侧降级渲染 vs 把 teams/logs 改 optional-empty），并给 P4 一条可判断言 |
| W2-16 | inconsistency（闭表未同步） | 引擎 exit-code 契约测试（P2） | LOW | `contracts/role-edge-engine.contract.md:28`（C-2 code 2 行）、`:45`（C-4 未知 query 身份） | C-2 自称 exit code 闭集且 code 2 仅定义「unreadable or malformed input」，C-4 却新增第三类触发（query 参数身份无法解析）且同为 2——行为一致、定义未收录 | `/speckit.plan`：C-2 的 code-2 行补该触发条件（或 C-4 改引 C-2 条目） |
| W2-17 | ambiguity（W2-09 修复残留） | `test_status_digest_roles.py` 字段存在断言（P4） | LOW | `contracts/status-digest-role-view.contract.md:11`（C-2 首段）、`:13`（C-2 按来源分 schema） | C-2 首段规定「每个渲染条目携带 `id` … `last_activity`」，第二段却规定 line 来源行保留 `line_id` / `last_activity_at` 且两类字段族不混行——同一契约内 `id` 既必须在每个条目出现、又不出现在 line 行上 | `/speckit.plan`：首段改为「按来源族携带身份/活动字段」，与第二段同义 |
| W2-18 | underspecification | `test_role_edge_engine.py` schema 断言（P2） | LOW | `contracts/role-edge-engine.contract.md:34`（C-3 必需键）、`:30`（C-2 `inputs` 提及） | C-3 把 `inputs` 与 `roots` 列为 report 必需键，但两键的形状与语义在契约与 data-model 中均未定义（C-2 只说 registry 缺失记入 `inputs`） | `/speckit.plan`：C-3 定义两键形状，或删除 `roots` 并入既有键 |
| W2-19 | inconsistency（载体族计数） | none（叙述性；不阻断实现） | LOW | `plan.md:173`（EP-003 实测五类）、`data-model.md:42`（§2.1(b)「four-piece」） | plan 按实测列 `{pid,status,log,heartbeat,raw}-<line>-<stage>` 五类状态文件，data-model 称四件套（pid/status/log/heartbeat）；实测目录另有 `runner-log-`（13 个）——两处计数不一致且均不完整 | `/speckit.plan`：统一载体族表述（按实测六类命名或声明「四件套」为解析子集） |
| W2-20 | ambiguity（谓词方向） | 引擎谓词实现（plan → tasks，经 C-5 兜底） | LOW | `plan.md:34`（D-6）、`data-model.md:71`（§5 谓词） | D-6 把 `unbacked-role-claim` 写成「explicit … superagent role assertion with no parent edge」——字面读作「无入边（即根）」，而 §5/C-5 的谓词是「无一条以其为 parent 的出边」；D-6 自称实现解读，方向相反 | `/speckit.plan`：D-6 改为「no edge where it is the parent」（§5 措辞） |

### 2.2 Resolved 摘要（round-1 本读域，原文 §2）

- **fixed 12**：W2-01（单次物化 + importable 签名）、W2-02（`dual-role` = 授予职责，引出 W2-13）、W2-03（pin 35/36 同提交 +1）、W2-04（`dispatch_duty`/`sources` 对齐）、W2-06（conflicts 顶层行 + 边身份）、W2-08（required/optional 根闭集）、W2-09（按来源分 schema，引出 W2-17）、W2-10（注册表内容收敛；**集成者已跨域复核**：`features.md:102` 与详情 `:10` 现为「独立只读引擎 `role-edge-check.py` + 四类封闭违例」——与 plan D-2/D-6 一致）、W2-11（registry 默认链改指针）、W1-05 本域部分、X-01（plan Inherited #4 与 FR-036/GATE-1 同判据）、X-02（C-4 两种机器行为分离；闭表残留另立 W2-16）。
- **partially fixed 1**：X-03 → 以 W2-14 跟踪（D-5 指针已加、内嵌顺序未删）。
- **跨域残留登记 12 行**：见 Worker 文件 §3（W2-05/07/12、X-03、W1-07/10/13/15/17/18/19/20；其中 W1-20 经 W2 复核 covered-by `data-model.md:35-38` + payload C-11 的 `parent` 列）。

### 2.3 定向读数摘要（W2 §6，未运行 pytest）

- 吻合：pin `TPL_EXPECTED=35` / `LIVE_EXPECTED=36`；budget owner 38,400（`generate-instructions.sh:107`）；尺寸 37,454 / 32,975 B；引擎路径未占用；sidecar 命名；映射表落 `## Execution Detail`；digest 无 CLI override（无 split-brain）。
- 不吻合：状态文件族实为 6 类（raw/runner-log/pid/log/heartbeat/status）→ W2-19。
- 支持 W2-15：`specify init` 不创建 `.specify/teams` / `agents/execution`（`src/specify_cli/__init__.py` 零命中）。
- 宪法读域内：0 CRITICAL；XIV 残留实义冲突按 inconsistency/ambiguity 计（W2-14/W2-20），不计宪法级重复。

---

## 3. W3 — tasks.md（读域次序 3）

- **Unit**: `/speckit.analyze` round-2 Worker W3 · Worker run `r20261110T080102Z-b095-r2w3`
- **Read domain（唯一 spec 文件）**: `.specify/specs/095-superagent-role/tasks.md`（HEAD `1e59f10e2`）
- **归并核对**: 4 行，ID `W3-06…W3-11`（字典序，已机械复算）；severity = 0 CRITICAL / 0 HIGH / 2 MEDIUM / 2 LOW

### 3.1 Findings（round 2 现行项，原文表；节内按 ID 字典序）

| ID | Severity | Category | propagation_surface | Anchor（文件:行） | 一句话事实 | 建议归属（指针） |
|----|----------|----------|---------------------|-------------------|------------|------------------|
| W3-06 | MEDIUM | inconsistency（政策 vs 确定性 lane） | analyze 覆盖率汇总 / 实现 | `.specify/specs/095-superagent-role/tasks.md:52`（并见 `:90` T003） | 「严格子集可接受留白」政策与确定性 lane（集成者本轮复跑：`status: uncovered`、exit 1、claimed 9、29 条 beyond 冻结基线）互斥；本文件无 DoD/GATE 覆盖该 lane | `/speckit.tasks` + 覆盖率契约 owner：裁定该 lane 是否成门，或记录其非门理由 |
| W3-08 | LOW | inconsistency（机器标记 vs 散文） | 并行派发 | `tasks.md:151, :284`（并见 `:280, :292`） | T021 未标 `[P]` 而 `:280`/`:292` 称 T021–T025 可并行；`:284` 称 T049/T050 可与 T046 并行而三者均未标 `[P]`（修复处置 §2 明示维持） | `/speckit.tasks`：对齐 `[P]` 与说明，保持其一为 owner |
| W3-10 | LOW | underspecification（未命名载体） | 任务 → 实现 | `tasks.md:146, :234`（并见 `:54`） | T019 的 "six downlink role fields block" 与 T047 的 "a deterministic check" 仍未命名自身载体/实现归属，与本文件 `:54` 自定规则不一致（修复处置 §2 明示维持） | `/speckit.tasks`：为两处命名载体（夹具文件 / 检查脚本或其复用的 Tool） |
| W3-11 | MEDIUM | ambiguity / inconsistency（验证命令作用域） | T045 验证证据 → SC-008 / SC-009 | `.specify/specs/095-superagent-role/tasks.md:223`（对照 `:157`、`:222`） | T045 把三个测试模块与一个全局 `-k 'i14'` 组进同一反引号选择，而 `run-tests.sh` 把全部参数**单次**转发 pytest（`scripts/bash/run-tests.sh:319`），`-k` 作用于全部被收集项；实测 `test_sdd_invocation_governance.py` 与 `test_nested_run_report.py` 中 "i14" 命中数为 **0**，故字面命令会静默取消这两个模块（对新 zero-mechanism 模块同理），与「三模块全绿」的声称不符 | `/speckit.tasks`：把 T045 拆成独立调用（`fast_fail_discipline.py -k 'i14'` 单独一行；governance 与 nested_run_report 各自全量）或去掉 `-k` 分组 |

### 3.2 Round-1 复裁摘要（W3 §1）

- **resolved 6（含 3 HIGH）**：W3-01（镜像义务 10 行/12 文件，owner = plan 表）、W3-02（FR-011…FR-016 获落点，任务行 FR 引用 38/38）、W3-03（T053 改为实际运行 smoke 并写证据）、W3-04（US1 IT 四类）、W3-05（US2 依赖句按 `blockedBy` 图重写）、W3-07（T038/T044 证据落点具名）。
- **rejected 1**：W3-09（round-1「registry 未标 cross-check」的正文不支持：`:123` 已显式标 "cross-check entries"）。
- **carried 3**：W3-06、W3-08、W3-10（均显式 deferred）。
- **确定性 lane（集成者复跑确认）**: exit 1 / `uncovered`；claimed 9；baseline 640 names；29 beyond baseline；FR claimed 20 / uncovered 18；与 W3-06 的互斥描述一致。
- **全量复核摘要**: `validate-tasks.py` PASS 0/0；54 行；FR 38/38、SC 10/10；`[P]` 22、`blockedBy` 38、green 9 条单调无 collision；宪法读域内 0 CRITICAL。

---

## 4. 归并规则与跨 Worker 等价关系（确定性说明）

- **排序**: 按读域次序 W1 → W2 → W3 分节；节内按 finding ID **字典序**（机械复算 W1 26 / W2 11 / W3 4，与 Worker 自报一致）。
- **跨 Worker 重复 ID**: 三个 Worker 的前缀命名空间（`W1-` / `W2-` / `W3-`）不相交，主表重复 ID = **0**；「先声明先得」破平规则**无适用对象，无被抑制副本**。
- **跨域登记不是重复 finding**: W2 文件 §3 的 8 行 `W1-NN` 是**跨域落点登记**（W2 自述「本 Worker 不跨域改判」），其事实归 W1 主表（先声明）；保留为指针，不重复计数。等价对：**W1-10 ≡ W2-05**（W2 自述「同一事实，requirements 侧锚点」）、**W1-15 ≡ W2-07 家族**（W2 自述）、**W1-20** 经 W2 复核 covered-by（`data-model.md:35-38` + payload C-11 映射表）。两者均保留各自制品锚点，无内容抑制。
- **上轮已关闭 ID**（W1-01…W1-29 / W2-01…W2-12 / W3-01…W3-10 中的 fixed/rejected 行）保留在三个 Worker 文件的 delta / residue 表中，本报告只登记门相关摘要，不重列。

---

## 5. 跨制品一致性（串行集成者；requirements ↔ plan ↔ tasks ↔ contracts）

读域互斥解除后的独立检查：对 coverage、术语、判据与数字声明四类逐对核对。**与既有 Worker finding 同源的条目只进 §5.2 确认表，不重复计 severity**；真正新发现才给 `X2-` ID 并计入顶部计数。

### 5.1 新增跨制品 findings（集成者检测，3 条）

| ID | Severity | 制品对 | 锚点 | 一句话事实 | 建议归属（指针） |
|----|----------|--------|------|------------|------------------|
| X2-01 | MEDIUM | tasks ↔ data-model ↔ engine contract | `tasks.md:129`（T015）；`data-model.md:63`（§4）；`contracts/role-edge-engine.contract.md:36`（C-3 `executors[]` 键集） | T015 要求引擎实现「executor `state` derivation from the existing carriers per data-model §4/§9 (completed / failed / cancelled)」，而 data-model §4 明确 `state` / `last_activity` / `age` / `stale` 是 **digest 视图字段、非引擎输出键**（引擎只输出 `id`/`parent`/`roles`/`depth`/`sources`），C-3 的 `executors[]`/`edges[]` 键集也无 `state`——按 T015 实现会与 C-3 的 schema 断言冲突；按 §4 实现则 T015 的 state 义务无落点（W2-04 修复把 state 移出引擎后，tasks 侧未同步回写）。 | `/speckit.tasks`：T015 收窄为生命周期/既有载体引用；或 `/speckit.plan`：若确需引擎输出 state，则同步 C-3 与 P2/P4 测试 |
| X2-02 | MEDIUM | requirements ↔ tasks | `requirements.md:213`（SC-004）、`:226`（SC-004 Source）、`:218`（SC-009）、`:231`（SC-009 Source）；`tasks.md:158`（T028）、`:223`（T045） | SC-004 Source 要求「交错派发夹具的时序与预留记录…把预留后移的合成变异实测」，SC-009 Source 要求「放宽禁令的合成变异实测」；但任务图没有创建该交错派发夹具或执行这两类变异演练的行——T028 只跑既有三个并发契约模块并核对 owner 页指针形态，T045 只跑绿三个既有模块。SC-004 为 **final** 路径（DoD-6 要求全部 pass 且证据在位），其测量源缺生产者；SC-009 变异半同理。 | `/speckit.tasks`：为 SC-004 增补夹具 + 变异行（或收窄 SC-004 Source）；为 SC-009 变异半补行，或声明由既有测试承担并点名 |
| X2-03 | LOW | requirements ↔ contracts / tasks | `requirements.md:126`（FR-003 record kind [[STR-005]]）、`:242`；`data-model.md:15`；`contracts/role-edge-engine.contract.md:32-39`（C-3）；`tasks.md` 全文件 | STR-005 字面量 `role-edge` 只出现在 requirements 与 data-model 的叙述里；引擎 C-3 输出键集与全部任务/测试断言都没有该 record-kind 判别符——FR-003 的「唯一机读记录形态（record kind role-edge）」下游没有机器消费者。 | `/speckit.requirements` 或 `/speckit.plan`：把 kind 判别符加入 C-3/测试，或把 FR-003 的 kind 措辞改为对 §2 字段集的指称 |

**证据边界**: X2-01 已重读三处文本；未运行测试，`test_role_edge_engine.py` 的 schema 断言是否允许额外键未测量（C-3 写 "Required keys" 而非闭集，故冲突以「义务落点不一致」为主张，不夸大为必然红）。X2-02 已重读 SC Source 与 T028/T045 文本及任务图；未运行任何夹具/变异。X2-03 已用全目录检索确认 `role-edge` 字面量消费点（requirements、data-model、plan XVIII/EP-004 与文件/模块名）；若 kind 仅为命名性措辞则按 do-not-flag 可降为观察，交由验证波/U4 裁决。

### 5.2 跨制品复核确认表（既有 Worker finding 的制品对证据，`(re-read by integrator)`；不重复计数）

| 主题 | 制品对 | 对应 Worker finding | 复核结论 |
|------|--------|---------------------|----------|
| 完成门判据 | REQ:218（SC-009 全绿）↔ REQ:177（FR-036 零新增 + 基线豁免）↔ plan:195（Inherited #4）↔ tasks GATE-1:31 / T051:238 | W1-31（HIGH） | 确认：plan / FR-036 / GATE-1 三处已对齐为「相对 implement 起点基线零新增失败」；只有 SC-009 仍写「全绿」——若基线含四类治理测试既有红则不可同时满足 |
| `dual-role` / `superagent` 载体域 | FR-002/005/Key Entities/SC-001/STR-002 ↔ data-model §1/§2/§2.1(a)/§6 ↔ engine C-5/C-9 ↔ FR-005 声明载体句 | W1-30（HIGH）+ W2-13（HIGH） | 确认并跨制品化：requirements 明确要求「team 映射行 `role` 列或 stage envelope `role_edge` 声明取值为 `superagent`」，data-model 却把同一载体域闭为 `subagent \| dual-role`，C-9 又判未知值 malformed → exit 2；单一侧修复会留下另一侧矛盾，须联合处置 |
| SC-001 测量源 | REQ:223（「违例三类」）/ REQ:29（US1 三类示例）↔ FR-005:128 / US1 AS3:39 / SC-001:210（四类）↔ tasks US1 IT:116（四类） | W1-32（HIGH） | 确认：下游（plan D-6 / tasks）均四类，只有 requirements 两处残留 |
| 根身份顺序 | plan:33（D-5 内嵌 run_id→line_id→root）↔ data-model §2:19（root fallback run_id→line_id）↔ §3:46-52（line_id 先于 run_id）↔ tasks T015:129（exact §3 order） | W2-14（MEDIUM；X-03 残留） | 确认并扩展：除 plan D-5 外，data-model §2 的 root fallback 与 §3 的解析顺序也未收敛——同一文件两套优先级 |
| digest 默认根缺失缝 | engine C-2:30（state/teams/logs required）↔ digest C-1:7 / C-3:19（默认根物化 + nothing-running）↔ FR-029:167 / SC-006:215（空集渲染 `nothing-running`）↔ W2 实测 init 不建 teams/logs | W2-15（MEDIUM） | 确认并扩展：新下游项目空集路径会先撞引擎 exit 2，而非渲染 `nothing-running` |
| SC-002 回传要素 | SC-002:211（三要素）↔ Source:224（「四项断言」）↔ FR-019:148（四项）↔ payload C-5:25（五项）↔ tasks US2 IT:142 / T020:147（五项） | W1-34（MEDIUM） | 确认并扩展：契约与任务侧固定为五项，requirements 侧存在三种计数 |
| T045 命令作用域 | tasks:223 ↔ `run-tests.sh:319`（参数单次转发）↔ SC-008/SC-009 证据 | W3-11（MEDIUM） | 确认：`-k 'i14'` 在单次调用中作用于全部被收集项，两模块将静默取消 |
| 覆盖率政策 | tasks:52（严格子集留白）↔ accountant（本轮复跑 9 claimed / 29 beyond baseline）↔ T003:90（implement 起点 `--freeze`） | W3-06（MEDIUM） | 确认：读数未变；`--freeze` 会把 29 并入新基线，使 delta lane 归零 |
| 载体族计数 | plan EP-003:173（五类）↔ data-model §2.1(b):42（四件套）↔ 实测 6 类 | W2-19（LOW） | 确认 |
| `attempt` 载体 | FR-003:126 / FR-013:139 ↔ data-model §2.1 三载体 ↔ C-7:57 排序键 | W2-05（MEDIUM）+ W1-10（MEDIUM） | 确认：三载体均不携带 attempt，取值来源未声明 |
| 映射表 `parent` 列 | FR-030:168（`label → 角色 → 工作区`）↔ plan D-9:37 ↔ payload C-11:55 ↔ data-model §2.1(a):35 | W1-20（MEDIUM） | 确认：下游已加 `parent` 列，需求文本未回写 |
| C-3 `inputs`/`roots` 形状 | C-3:34（必需键）↔ data-model §4:62-63（只定义 5 个 executor 键） | W2-18（LOW） | 确认：两键形状无 owner |
| C-2 闭表 | C-2:28（code 2 闭集）↔ C-4:45（第三类触发） | W2-16（LOW） | 确认 |
| 注入清单封闭性 | FR-017:146（恰好九项）↔ payload C-2:11（closed）↔ data-model §7:93（九个 slug）↔ T020:147 | W1-11（fixed） | 确认关闭；W1-12（消息类 owner/最少四类）仍开放 |
| 注入逐项判据 | FR-018:147（逐项 item-id 句柄）↔ C-3:16 ↔ T020:147 | W1-06（fixed） | 确认关闭：九项 slug 在 data-model §7 固定 |

### 5.3 已检查且不构成 finding 的项（noise floor / 边界说明）

- **数字声明一致**: 预算 37,454 / 32,975 / 38,400 B 与余量 946 B（tasks 的「可用最后一字节 945 B」是 `size >= budget` 语义的更严格读法，非矛盾）；镜像基线 428 DIFF-class（437 是已记录 trap）；切片 14（092 缺失）；section-count pins `TPL 35→36` / `LIVE 36→37`；`test_i13` 7→8；契约子句 38 = engine 11 + payload 13 + digest 8 + harness 6（accountant 9 claimed + 29 beyond = 38 复算吻合）；green 9；Work Packages 7/13/10/6/6/9（全部 ≤16）；任务 54。
- **术语一致**: `super agent`（正文）/ `superagent`（机读）/ `super-agent`（仅 glossary alias）按 A15 在四制品一致；四个违例 kind、九个注入 slug、四个消息类 token 在 requirements / data-model / contracts / tasks 逐字一致。
- **六字段下行清单一致**: FR-008 / data-model §6 / payload C-1 / tasks T020、T025；FR-034 的三字段是子集表述（六 ⊇ 三，无行为冲突）。
- **深度语义一致**: FR-004 最短距离 / SC-001 的 0-1-2 / fixtures（T012、T032）/ T015。
- **Feature 状态与注册表**: `Planned` 在 index / detail / tasks / feature-ref 一致；W2-10 的内容漂移已由修复提交 `1e59f10e2` 关闭（集成者重读 `features.md:102` 与详情 `:10` 确认「独立只读引擎 + 四类封闭违例」）。
- **前提成立性**: `exec-quant.py` 含 `collect-dispatch` 动作（data-model §2.1(c) 载体前提）；`watch-model.md` 两侧存在（requirements 运行时路径与 plan 源路径都解析）；`role-edge-check.py` 两侧均不存在（EP-004 与新产物前提）。
- **do-not-flag**: requirements `Status: Draft` 元数据、checklist 头部的 dated size 快照（W1 的 SO-R2-4）、格式/措辞偏好、已一致的模板占位。

### 5.4 跨 Worker / 跨制品张力（不裁决，交验证波 / U4）

- **T2-1（W1-30 vs W2-13）**: 同根不同制品——requirements 侧是 token 双语义与声明载体句，data-model 侧是载体值域闭合 + C-9 严格输入。两条均维持；修复须联合（单独修一侧会留下另一侧矛盾）。
- **T2-2（W2「X-01 fixed」vs W1-31）**: 兼容——plan / FR-036 / GATE-1 已对齐，SC-009 未在其证据锚点内，故 W1-31 是**同根残留**而非重复 finding。
- **T2-3（W3-06 vs tasks:52）**: 覆盖率 lane 是否成门属覆盖率契约 owner 裁定；集成者本轮复跑不改变读数。
- **T2-4（W2 对 W2-13 的降级条件）**: W2 提示「若契约已按 `dispatch_duty` 分离字段则 claim 收窄」。实测 data-model §2 已分离 `dispatch_duty`，但 `role` / `role_declaration` 值域仍闭为 `subagent | dual-role`，故 claim 收窄为「显式 `superagent` 断言的载体域未开放」，严重度维持（待验证）。

---

## 6. 汇总读数

### 6.1 Coverage Summary

| 维度 | 读数 | 来源 |
|------|------|------|
| Clause coverage（本特性） | exit 1 / `status: uncovered`；claimed **9/38**；**29 beyond frozen baseline**（9 + 29 = 38 复算吻合） | 集成者复跑 accountant（2026-11-10） |
| FR 契约引用组 lane | claimed **20** / uncovered **18**（of 38） | 同上 |
| 语料级 | 290 文件 = 183 parsed + 107 named-unparseable；clause universe 2037；1 parse doubt；**47 error / 1 warning** | 同上 |
| Baseline | 640 names；640 baseline-internal uncovered 不阻断；delta 29 为阻断项 | 同上 |
| FR 任务行引用 | **38 / 38**（上轮 32/38 已修复） | W3 复算 |
| SC 任务行引用 | **10 / 10** | W3 |
| Checklist 问责（pass H） | 39 = **25 raised + 14 covered-by + 0** unraised/undispositioned；`[Gap]` 子集 10 = 6 + 4 + 0 | W1 + 机械复算 |
| Feature linkage | 1 / 1 consistent（绑定、状态 `Planned`、内容漂移已修复） | W1 / W2 + 集成者重读 |

**零 finding 底线**: 不适用（本波 findings 非零）。

### 6.2 Metrics

| 指标 | 值 |
|------|-----|
| Worker findings | **41**（0C / 4H / 26M / 11L）：W1 26（3H/20M/3L）· W2 11（1H/4M/6L）· W3 4（0H/2M/2L） |
| 跨制品新增 | **3**（0C / 0H / 2M / 1L） |
| 集成后总量 | **44**（0C / **4H** / 28M / 12L）；44 ≤ 50，无裁剪 |
| Round-1 delta | W1：29 = 8 fixed + 1 partial + 20 deferred；W2：12 resolved（1 partial → W2-14）；W3：6 resolved（含 3 HIGH）+ 3 carried + 1 rejected |
| Requirements | validator `status: ok`（0 error / 0 warning；288 行 / 48 定义行 / 6 shared strings，修复轮读数）；55,778 B；38 FR / 10 SC / 6 STR / 5 US / 10 Edge / 16 Q / 15 A |
| Tasks | 54 行 / 8 阶段；22 `[P]`；38 `blockedBy`；9 green；6 个新契约测试模块计划 |
| Contract clauses | 38（engine 11 / payload 13 / digest 8 / harness 6） |
| C/H 验证状态 | **pending**：本简报未派发独立验证波；4 条 HIGH 为检测者提议值，锚点由集成者重读并经跨制品扩展 |
| Downgrade rate | **n/a**（无验证波，不产生 confirm/reject/downgrade 计数） |
| 跨 Worker 重复 ID | **0**（前缀不相交；无被抑制副本） |

### 6.3 Systemic Observations（簇级，不抬升单行 severity）

- **SO-2A（字段所有权跨制品漂移）**: W2-04 修复把 `state` 移出引擎输出键集后，tasks T015 未同步回写（X2-01）——「修复搬迁」必须在 tasks 侧同步登记，否则实现期两边各按一侧执行。
- **SO-2B（SC Source 的合成变异无生产者）**: X2-02——SC Source 承诺的夹具与变异演练需要任务行承接；否则 DoD-6 的 final 证据链在验收时才发现断裂（与 round-1 W3-03 同型）。
- **SO-2C（修复扇出未扫全）**: W1-32（SC-001 Source 残留）、W1-35（US 级引用残留）、W2-14（D-5 内嵌残留）同型——集合/计数/顺序类修复需要机械扫全部出现点。
- **SO-2D（token 过载延续）**: W1-30 / W2-13 是 W2-02 收窄谓词后未分离载体域的残留；`dual-role` 在「集合形态标记」与「授予职责声明值」两个作用面上继续共用同一字面量。
- **Worker 侧 SO-R2-1…5**（修复扇出、token 过载、Shared Strings 反向、dated 快照、deferred 簇）见 W1 文件；W2/W3 的读域观测见各自文件，不在此重复。
- **框架观察**: 本轮无新增 FO；W3-11 的 runner 单次转发是既有设计语义（非缺陷）；FO-095-09/10 已在上轮 merged 报告登记。

---

## 7. Next Actions（技能 §9；不自动修复）

1. **HIGH（4）**: W1-30 / W1-31 / W1-32 归 `/speckit.requirements`（W1-30 可联合 `/speckit.plan` 的载体域）；W2-13 归 `/speckit.plan`（data-model §2/§2.1(a)/§6 与 C-5/C-9 同步）。
2. **MEDIUM（28）**: X2-01 → `/speckit.tasks`（T015）或 plan（C-3）；X2-02 → `/speckit.tasks`；其余按各行归属指针分流（以 requirements 与 plan/contract 侧居多）。
3. **LOW（12）**: X2-03 等可随修订一并处置或显式延后（`/speckit.todo` / 处置台账）。
4. **验证波**: 正式门禁前应补一次独立只读验证波（fresh-context、与检测者不相交）或由 U4 显式裁决；本报告不冒充该结论。
5. 本报告未应用任何修复编辑；后续命令由驱动者/用户自行发起。

## 8. Limitations

- **未运行测试套件**（analyze 只读；全部 finding 为静态文本/结构证据；W3-11 的 pytest 语义结论由 pytest `-k` 语义 + `run-tests.sh:319` 源码读数支撑）。
- 未派发独立验证波；HIGH 为检测者提议值，U4 裁决前不得作为门禁结论。
- Worker 的 residue / delta 全文在三个 Worker 文件中；本报告只登记门相关摘要与跨制品证据。
- 日期化快照（checklist 头部尺寸、上轮报告计数、dated measurements）按 one-source-of-truth 的 dated-record 豁免，不作为当前读数。
