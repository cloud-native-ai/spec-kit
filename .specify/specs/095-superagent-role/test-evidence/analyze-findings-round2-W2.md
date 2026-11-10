# Analyze Findings — Round 2 · W2（plan / data-model / quickstart / feature-ref / contracts）

- 阶段：analyze 第二轮（并发波 W2；修复轮后重过门，一轮为限）；run_id `r20261110T055657Z-b095-r2w2`（worker 作用域后缀，见 §7 记账）
- 线：`095-superagent-role`；线类别四元组：`flow_class=execution`；`source=declaration`；`marker=`（空）；`error=-`
- 读域（文件级互斥，8 个文件）：`plan.md`、`data-model.md`、`quickstart.md`、`feature-ref.md`、`contracts/harness-landing.contract.md`、`contracts/role-edge-engine.contract.md`、`contracts/role-transition-payload.contract.md`、`contracts/status-digest-role-view.contract.md`
- 方法：按 `.specify/skills/internal/analyze-artifacts/SKILL.md` 检测面 A/B/C/D/E/F/G/I 对读域执行只读分析；本轮为**全严重度重审**（非 C/H-only）：round-1 findings 逐条重裁 + 全集扫描。未修改任何制品；本文件是本 Worker 唯一产物（round-1 `analyze-findings-W2.md` 原样保留）。brief 内两处输出文件名不一致（`analyze-findings-round2-W2.md` vs `analyze-findings-W2.md`），按不覆盖 round-1 证据的唯一解读落到 round2 文件名（in-passing correction，已披露）。
- 输入：本读域 8 文件（当前态）+ `test-evidence/analyze-merged-2026-11-10.md` + `test-evidence/analyze-repair-dispositions-2026-11-10.md` + `.specify/constitution.md`（v1.19.0）+ 技能 references。未读 requirements.md / tasks.md / 其他 spec 制品。
- 独立性：读域制品由前序阶段/其他 run 产出，非本 Worker 所著。技能 §7 的 C/H 独立验证波**不在 Worker 派发范围**；本表 CRITICAL/HIGH 为**待验证提议值**，由集成分析者/验证波裁决。

## 1. 主表 — 本轮 findings（新建 8 条 + carried-over 3 条）

| ID | 类别 | propagation_surface | Severity | 锚点 | 一句话事实 | 建议归属（指针） |
|----|------|---------------------|----------|------|------------|------------------|
| W2-13 | inconsistency（违例不可达） | 引擎实现 + `test_role_edge_engine.py`（P2 变异演练 c） + C-9 输入严格性测试 | **HIGH**（提议值） | `data-model.md:71`（§5 谓词）、`:37`（§2.1(a) 行形 role 值域）、`:22`（§2 表 `role_declaration` 值域）、`:82`（§6 同值域）、`:40`（§2.1(a) 注）；`contracts/role-edge-engine.contract.md:49`（C-5）、`:65`（C-9） | `unbacked-role-claim` 的谓词要求某载体声明值取 `superagent`，但两处具名载体的声明域均封闭为 `subagent \| dual-role`，而 C-9 规定已知表内未知值 = malformed → exit 2——按字面实现，该违例或不可达，或同一行同时落入 exit 2（C-9）与 exit 1（C-5）两个相反判定 | `/speckit.plan` 修订轮：把 `superagent` 纳入载体声明值域（§2/§2.1(a)/§6 三处同步）或改指其他可解析断言载体；C-5/C-9 同步 |
| W2-14 | inconsistency（X-03 修复残留） | 引擎身份解析实现 + 边排序夹具（plan → tasks） | MEDIUM | `plan.md:33`（D-5 内嵌顺序）、`data-model.md:46-52`（§3 唯一 owner 顺序） | plan D-5 在声称「本行不携带第二套顺序」的同时仍内嵌根身份取值顺序（run_id → line_id → literal root），与 data-model §3（line_id 先于 run_id）优先级相反；同一根同时持有 line_id 与 run_id 时两处给出不同首选身份 | `/speckit.plan`：删除 D-5 内嵌片段、仅留 §3 指针（或反向把 §3 顺序回写为与 D-5 一致——须单一 owner） |
| W2-15 | underspecification（契约缝） | digest 实现 + `test_status_digest_roles.py` 的 `nothing-running` 断言（P4） | MEDIUM | `contracts/role-edge-engine.contract.md:30`（C-2 required roots）、`contracts/status-digest-role-view.contract.md:7`（C-1 默认根单次物化）、`:19`（C-3 nothing-running） | 引擎把 `--teams-dir` / `--logs-dir` 列为必需根（缺失→2），digest 却要求经引擎默认根物化并承诺零条目渲染 `nothing-running`；没有任何条款声明 digest 在默认根缺失时如何渲染，而 `.specify/teams` 与 `.specify/agents/execution/logs` 均非 CLI init 创建（实测 `src/specify_cli/__init__.py` 零引用）——空闲下游项目正落在该未定义缝上 | `/speckit.plan`：C-2 与该缝二选一定义（digest 侧降级渲染 vs 把 teams/logs 改 optional-empty），并给 P4 一条可判断言 |
| W2-16 | inconsistency（闭表未同步） | 引擎 exit-code 契约测试（P2） | LOW | `contracts/role-edge-engine.contract.md:28`（C-2 code 2 行）、`:45`（C-4 未知 query 身份） | C-2 自称 exit code 闭集且 code 2 仅定义「unreadable or malformed input」，C-4 却新增第三类触发（query 参数身份无法解析）且同为 2——行为一致、定义未收录 | `/speckit.plan`：C-2 的 code-2 行补该触发条件（或 C-4 改引 C-2 条目） |
| W2-17 | ambiguity（W2-09 修复残留） | `test_status_digest_roles.py` 字段存在断言（P4） | LOW | `contracts/status-digest-role-view.contract.md:11`（C-2 首段）、`:13`（C-2 按来源分 schema） | C-2 首段规定「每个渲染条目携带 `id` … `last_activity`」，第二段却规定 line 来源行保留 `line_id` / `last_activity_at` 且两类字段族不混行——同一契约内 `id` 既必须在每个条目出现、又不出现在 line 行上 | `/speckit.plan`：首段改为「按来源族携带身份/活动字段」，与第二段同义 |
| W2-18 | underspecification | `test_role_edge_engine.py` schema 断言（P2） | LOW | `contracts/role-edge-engine.contract.md:34`（C-3 必需键）、`:30`（C-2 `inputs` 提及） | C-3 把 `inputs` 与 `roots` 列为 report 必需键，但两键的形状与语义在契约与 data-model 中均未定义（C-2 只说 registry 缺失记入 `inputs`） | `/speckit.plan`：C-3 定义两键形状，或删除 `roots` 并入既有键 |
| W2-19 | inconsistency（载体族计数） | none（叙述性；不阻断实现） | LOW | `plan.md:173`（EP-003 实测五类）、`data-model.md:42`（§2.1(b)「four-piece」） | plan 按实测列 `{pid,status,log,heartbeat,raw}-<line>-<stage>` 五类状态文件，data-model 称四件套（pid/status/log/heartbeat）；实测目录另有 `runner-log-`（13 个）——两处计数不一致且均不完整 | `/speckit.plan`：统一载体族表述（按实测六类命名或声明「四件套」为解析子集） |
| W2-20 | ambiguity（谓词方向） | 引擎谓词实现（plan → tasks，经 C-5 兜底） | LOW | `plan.md:34`（D-6）、`data-model.md:71`（§5 谓词） | D-6 把 `unbacked-role-claim` 写成「explicit … superagent role assertion with no parent edge」——字面读作「无入边（即根）」，而 §5/C-5 的谓词是「无一条以其为 parent 的出边」；D-6 自称实现解读，方向相反 | `/speckit.plan`：D-6 改为「no edge where it is the parent」（§5 措辞） |
| W2-05 | underspecification | 引擎边记录填充 + 确定性排序（P2） | MEDIUM | `data-model.md:21`（`attempt`）、`:30-44`（三载体形态）、`contracts/role-edge-engine.contract.md:37`（edges `attempt`）、`:57`（C-7 排序键） | **(carried over)** `attempt` 是边必备键与确定性排序键，但三种可解析载体（team 映射表、driver sidecar 六字段、run-agent `unit_id`/`run_id` 对）均不携带 attempt，取值来源仍未声明（修复轮未处置，显式 deferred） | `/speckit.plan`/`data-model.md` §2.1：逐载体声明 attempt 取得规则（如 report stamp / 产物后缀） |
| W2-07 | underspecification | 恢复/状态推导实现 + digest `state` 渲染（P2/P4） | MEDIUM | `data-model.md:63`（§4 `state` 仅写 "enum"）、`:99`（§8 消息类）、`:113`（§10 恢复标记） | **(carried over)** §10 仍把恢复中仍运行的子项标记 `interrupted` / `attention`，§4 的 `state` 却不再给任何值域，两标记未落入任何声明域，`attention` 与 §8 消息类 `attention-escalation` 的载体区分仍未给出（修复轮未处置，显式 deferred；原闭域冲突已改为值域沉默） | `/speckit.plan`/`data-model.md` §4/§10：声明标记的字段与词表 owner，或删除标记 |
| W2-12 | coverage-gap | Feature 详情 → plan 的覆盖映射（读者/评审） | LOW | `feature-ref.md:14`（第 1 行）、`contracts/harness-landing.contract.md:19-25`（C-2 仅指针行） | **(carried over)** feature-ref 第 1 行仍把「新 owner 页」映射到 harness C-2，而 C-2 只治理三个 sibling 的指针行；owner 页自身内容由 C-5 的 `test_superagent_definitions.py` + P1 守卫，映射不精确（修复轮未处置，显式 deferred） | `/speckit.plan`/`feature-ref.md` 第 1 行：改指 FR-001/P1 + C-5 测试，或 harness 补 owner 页条款 |

> 严重度依 propagation-surface 规则派生（MEDIUM/LOW 跳过验证波；W2-19 surface=`none`，按规则封顶 MEDIUM，实为 LOW）。CRITICAL：**0**。

## 2. Resolved Since Last Run（round-1 在本读域的 findings，附关闭证据）

| Round-1 ID | 结论 | 关闭证据（当前态锚点） |
|------------|------|------------------------|
| W2-01 (H) | fixed | `plan.md:36`（D-8：一次 `read_carrier_inputs` + 一次 `evaluate_role_model`，共享单次载体物化）；`contracts/role-edge-engine.contract.md:18`（C-1 可导入签名）；`contracts/status-digest-role-view.contract.md:7`（C-1 单次调用） |
| W2-02 (H) | fixed | `data-model.md:13`（`dual-role` = 集合形态标记 / 声明 = 已授予职责，非 superagent 主张）、`:23`（`dispatch_duty`）、`:71`（谓词收窄为显式 `superagent` 断言）；`plan.md:34`（D-6 同步）——但该修复引出新 finding W2-13 |
| W2-03 (H) | fixed | `plan.md:38`（D-10）、`:156`（Mirror 行）、`:209`（Phase 0 #5 已改为实测表述）、`:225`（P5）；`contracts/harness-landing.contract.md:17`（pin +1 义务）；实测 pin `TPL_EXPECTED = 35` / `LIVE_EXPECTED = 36`（`tests/contract/test_fast_fail_discipline.py:751-752`）吻合 |
| W2-04 (M) | fixed | `data-model.md:23`（`dispatch_duty`）、`:62-63`（`sources`；`state/last_activity/age/stale` 明示为 digest 视图字段）；`contracts/role-edge-engine.contract.md:36-37`（C-3 键集）对齐 |
| W2-06 (M) | fixed | `data-model.md:26`（顶层 `conflicts` 行携带边身份）；`contracts/role-edge-engine.contract.md:39`（C-3 `edge` 对象）、`:61`（C-8）；`plan.md:33`（D-5）措辞对齐 |
| W2-08 (M) | fixed | `contracts/role-edge-engine.contract.md:30`（C-2 required/optional 根闭集）；`plan.md:32`（D-4 指针） |
| W2-09 (M) | fixed | `contracts/status-digest-role-view.contract.md:13`（C-2 按来源分 schema）、`:32`（C-6）——但首段措辞引出新 finding W2-17 |
| W2-10 (M) | fixed（按 repair 记录；锚点在注册表，不在本读域，未复核） | `analyze-repair-dispositions-2026-11-10.md` §2 行 W2-10；需集成者跨域复核 |
| W2-11 (L) | fixed | `contracts/role-edge-engine.contract.md:16`（C-1 改指 `line-registry.py` owner）；`plan.md:31`（D-3 指针） |
| W1-05 (H, 本域部分) | fixed | `data-model.md:40`（显式断言载体注）、`:71`（§5 谓词可机判）；载体值域缺口另见 W2-13 |
| X-01 (H) | fixed | `plan.md:195`（Inherited #4 完成门 = 相对 implement 起点零新增失败，与 FR-036/GATE-1 同一判据） |
| X-02 (H) | fixed | `contracts/role-edge-engine.contract.md:45`（C-4：记录侧悬空 = exit 1；query 参数未知 = exit 2）——C-2 闭表未同步，另立 W2-16 |
| X-03 (M) | partially fixed | `plan.md:33` 已加「唯一 owner = data-model §3」指针，但内嵌顺序片段仍在 → 以 W2-14 跟踪 |

## 3. 残留登记（round-2 门的 C/H 判定输入；open MEDIUM/LOW 逐条列明）

| Round-1 ID | 当前状态 | Disposition | 理由 |
|------------|----------|-------------|------|
| W2-05 | open | deferred | `attempt` 取得规则仍未声明；P2 的确定性排序与边输出依赖它 |
| W2-07 | open（形态变化） | deferred | §4 值域改为沉默、§10 标记仍无字段/词表 owner |
| W2-12 | open | deferred | feature-ref 行 1 映射未改 |
| X-03 | open（部分修复） | fixed-partial → tracked as W2-14 | D-5 指针已加，内嵌顺序未删 |
| W1-07（跨域；本域落点） | open | deferred | 引擎输入记录集/多根与跨 run 隔离规则仍未声明（engine C-1/C-9、data-model §3 未新增约束）；锚点在 requirements，由集成者登记 |
| W1-10 | open | deferred | = W2-05（同一事实，requirements 侧锚点） |
| W1-13（本域落点 payload C-7） | open | deferred | `ack` / `attention-escalation` 仍未逐类映射既有载体 |
| W1-15 | open | deferred | = W2-07 家族（`interrupted` / `attention` 词表 owner） |
| W1-17（本域落点 data-model §10） | open | deferred | 「边 + 已收到返回」的 per-entry 写目标仍未点名 |
| W1-18 | partially addressed | deferred | digest C-1 现在声明四根单次物化；三层事实与四根的映射仍隐含 |
| W1-19（本域落点 digest C-3/C-4） | open | deferred | cap 单位与 `omitted` 范围已隐含于「merged entry set」，扇出原子性（父+子不被截断拆散）仍未声明 |
| W1-20 | addressed in-domain | covered-by `data-model.md:35-38` + `contracts/role-transition-payload.contract.md:55` | 映射表已含 `parent` 列并有 §3 解析规则 |

> 其余 round-1 M/L（W1-11/24/27、W3-04/05/07 等改为 fixed；W1-01/02/03/04/06/12/14/16/21–23/25/26/28/29、W2-05/07/12、W3-06/08/09/10）不在本读域的裁决范围；其残留清单以 merged 报告与 repair dispositions 为 owner，由集成者的门报告统一登记。本 Worker 不跨域改判。

## 4. 覆盖与链接摘要（读域内）

- **plan D-1…D-14 → Work Packages**：D-1→P1；D-2…D-7→P2；D-8→P4；D-9/D-14→P3；D-10→P5；D-11…D-13→P6。无未覆盖决策；依赖（P2/P3/P5←P1，P4←P1/P2，P6←P1–P5）无环。新 finding 落点：W2-13→P2；W2-14→P2；W2-15→P4；W2-16/17/18→P2/P4 测试；W2-19/20→P5/P2 文本。
- **契约条款 → 守卫测试**：engine C-1…C-11 → `test_role_edge_engine.py`；payload C-1…C-13 → `test_role_transition_payload.py`；digest C-1…C-8 → `test_status_digest_roles.py`；harness C-1…C-6 → `test_instructions_budget_superagent_section.py` / `test_superagent_zero_mechanism.py` / `test_superagent_definitions.py`。未发现「契约条款零测试」；同源缺口见 W2-13/W2-15/W2-16/W2-18。
- **quickstart 4 场景 ↔ 契约/测试**：S1→engine C-1/C-10；S2→digest C-1/C-3/C-8；S3→payload C-2/C-3/C-11；S4→harness C-1/C-4/C-6。逐场景前提/执行状态行齐备；S2 的 `nothing-running` 断言落在 W2-15 的未定义缝上。
- **feature-ref 6 行 ↔ 详情 Key Changes 6 项**：一一对应；第 1 行契约指针不精确（W2-12 carried）。
- **Feature linkage**：`plan.md:4`/`feature-ref.md:3-8` 声明 Feature 095、`Draft → Planned` 归本 plan；本读域未发现索引/详情漂移证据（注册表不在读域，漂移监测归 W2-10 关闭记录与集成者）。

## 5. Constitution alignment（读域内）

对 `.specify/constitution.md`（v1.19.0，22 原则）逐条对照读域文本：**未发现 CRITICAL 原则冲突，本轮不提出宪法级 finding**。相关抽查：

- XIV（One Source of Truth）：`plan.md:33/36`、`role-edge-engine.contract.md:16`、`harness-landing.contract.md:11` 均已改为指针；残留的实义冲突（D-5 内嵌顺序、D-6 谓词方向）已按 inconsistency/ambiguity 计（W2-14/W2-20），不计为宪法级重复。
- XXI（Script Interface）：`role-edge-engine.contract.md:19-20`（`--help`/`--version`/未声明选项）与 D-3 一致；读域声明引擎虽属只读豁免面但仍自钉，合规。
- XVII（Directory Governance）：新增目录仅 `tests/fixtures/superagent-role/`（按 feature fixture 惯例），`plan.md:142` 已声明；无未注册目录。
- VII/IV（工作流与 Test-First）：P1–P6 每个行为面均配命名契约测试；无 `[ ]`-task 声明越界。
- II（Feature-Centric）：`feature-ref.md:8` 状态迁移归 plan、`Implemented` 归 implement，无回归语义。

## 6. 确定性读数与度量

**本轮定向复测（只读命令/静态断言；未运行 pytest——测试入口纪律保持 `scripts/bash/run-tests.sh`）**

| 断言（出处） | 实测 | 结论 |
|--------------|------|------|
| pin 值 35/36（`plan.md:209`、`:156`；harness C-1:17） | `tests/contract/test_fast_fail_discipline.py:751-752` `TPL_EXPECTED = 35` / `LIVE_EXPECTED = 36` | 吻合 |
| 被引测试文件存在（harness C-5:46；plan:148） | `tests/contract/test_instructions_size_budget.py`、`tests/contract/test_mirror_parity_suite.py` 存在 | 吻合 |
| budget owner 38,400（`plan.md:22/175`；harness C-4:42） | `scripts/bash/generate-instructions.sh:107` `INSTRUCTIONS_BUDGET_BYTES=38400` | 吻合 |
| 尺寸 37,454 / 32,975 B（`plan.md:175`；`quickstart.md:39`） | `wc -c` = 37,454 / 32,975 | 吻合 |
| 引擎路径未被占用（EP-004:174） | `ls scripts/python/role-edge-check.py` → No such file | 吻合 |
| sidecar 命名 `prompt-<line>-<stage>.md.meta.json`（`data-model.md:42`） | `skills/external/sdd-loop-driver/references/stage-prompts.md:324` 同名形式 | 吻合 |
| 映射表落 `## Execution Detail`（`plan.md:207`；payload C-11:55） | `skills/internal/create-team/SKILL.md:79` 报告契约含该节 | 吻合 |
| 状态文件族（EP-003:173；`data-model.md:42`） | `ls .specify/state/`：raw 26 / runner-log 13 / pid 13 / log 13 / heartbeat 13 / status 12 | **不吻合（计数与构成）→ W2-19** |
| digest 载体根是否有 CLI override（digest C-1:7 前提） | `status-digest.py` 无 `--registry-dir/--teams-dir/...`；registry 由内建 `resolve_registry_dir()`（`:212`）解析，与引擎默认链一致 | 吻合（无 split-brain） |
| `specify init` 是否创建 teams/logs 根（W2-15 证据） | `grep` `src/specify_cli/__init__.py` 零命中 `.specify/teams` / `agents/execution` | 支持 W2-15 |

**度量**：本轮主表 11 条 = 新建 8（HIGH 1 / MEDIUM 2 / LOW 5）+ carried-over 3（M 2 / L 1）；CRITICAL 0。类别计数（新建）：inconsistency 4；underspecification 2；ambiguity 2。Resolved 12 条（其中 1 条按记录未跨域复核、1 条 partial 转 W2-14）。残留登记 12 行。无溢出（≪50 上限）。

**验证状态**：W2-13（唯一 HIGH）为**待验证提议值**——独立只读验证波（fresh-context、每 finding 一 verdict + 两个 evidence-boundary 字段）不在本 Worker 派发范围，由集成分析者执行；本 Worker 未自验、未派发验证者。

## 7. 限制与披露

- `requirements.md` / `tasks.md` / 注册表不在读域：W2-13 的 FR-005 侧一致性、W2-10 的跨域复核、残留表中 W1 行的 requirements 锚点均需集成者裁决；若已覆盖，相应行可降级或关闭。
- 取证限于存在性/行号/字段/字节/文件名计数的定向只读核对；未整读产品代码。
- 假设（自行裁决并记录）：① brief 两处产物文件名不一致，按不破坏 round-1 证据的读法写 `analyze-findings-round2-W2.md`；② wrap-up 引擎使用 worker 作用域 run-id `r20261110T055657Z-b095-r2w2`——round-1 教训（worker 占用命令级 run-id 致集成者被判 duplicate，见 `feedback/20261110T074703Z-speckit-analyze.md` 优化点 3）与 round-1 集成者 `-merge` 后缀先例均支持该做法。
- 未运行测试套件（analyze 只读；所有 finding 均为静态文本/结构证据，不依赖运行）。

## 8. Wrap-up 记账（Run Determination / Exec Quant / Feedback Record）

unit-id `/speckit.analyze`；run-id `r20261110T055657Z-b095-r2w2`；三步均执行成功，无 settle 副作用（determine 输出无 "settled previous run" 行）：

```text
[1] run-determination.py --action determine
unit: /speckit.analyze   run: r20261110T055657Z-b095-r2w2
  token_consumption    not_evaluated (source_unavailable)
  elapsed              not_evaluated (source_unavailable)
  artifact_correctness not_evaluated (no_declared_checks)
  satisfaction         not_evaluated (pending_next_turn)
trigger_feedback: false
change_point: cp-r20261110T055657Z-b095-r2w2 clean=false findings=4
persisted: .specify/memory/session/20261110T080529Z-run-determination-speckit-analyze-r20261110t055657z-b095-r2w.md

[2] exec-quant.py --action collect
exec-quant: recorded /speckit.analyze run=r20261110T055657Z-b095-r2w2 resolution=explicit -> .specify/memory/exec-quant/records/20261110T080536949332Z-a3e82c5a.json

[3] feedback-utils.py --action record
id=20261110T080543Z-speckit-analyze duplicate=false count_since_submission=409 should_prompt=true migrated=false
path=.specify/memory/feedback/20261110T080543Z-speckit-analyze.md
```

- Threshold notice：`should_prompt=true` × `trigger_feedback=false` → 不弹出提示（两真才弹）。
- Token reflection：见 feedback 条目 `## Optimization Points`（`token-efficiency` 标记 1 条；process 2 条）。

## 异常与披露

ANOMALY: 未发现需上报的 fast-fail 异常 — 无阻断性发现；in-passing correction 1 项（产物文件名按不覆盖 round-1 证据的唯一解读落地，见 §7 假设①）；无制品修改；唯一写入为本 findings 文件与 wrap-up 三步记账。
