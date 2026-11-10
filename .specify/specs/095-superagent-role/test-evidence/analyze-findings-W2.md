# Analyze Findings — W2（plan / data-model / quickstart / feature-ref / contracts）

- 阶段：analyze（并发波 W2）；run_id `r20261110T055657Z-b095`；线 `095-superagent-role`
- 线类别四元组：`flow_class=execution`；`source=declaration`；`marker=`（空）；`error=-`
- 读域（文件级互斥，8 个文件）：`plan.md`、`data-model.md`、`quickstart.md`、`feature-ref.md`、`contracts/harness-landing.contract.md`、`contracts/role-edge-engine.contract.md`、`contracts/role-transition-payload.contract.md`、`contracts/status-digest-role-view.contract.md`
- 方法：按 `.specify/skills/internal/analyze-artifacts/SKILL.md` 的检测面 A（duplication）/ B（ambiguity）/ C（underspecification）/ D（constitution alignment）/ E（coverage gaps）/ F（inconsistency）/ G（feature/registry）对读域执行只读分析；未修改任何制品；本文件是本 Worker 唯一产物。
- 独立性：读域制品由前序阶段/其他 run 产出，非本 Worker 所著，检测不构成自审。技能 §7 的 C/H 独立验证波由集成分析者运行，本表严重度为**提议值**。
- 范围边界：`requirements.md` 与 `tasks.md` 不在本 Worker 读域；技能 §3 的 clause/FR 覆盖记账器与 §5 的 H（checklist 问责）面由集成分析者负责。

## Findings

| ID | 类别 | Severity | propagation_surface | 锚点 | 一句话事实 | 建议归属（指针） |
|----|------|----------|---------------------|------|------------|------------------|
| W2-01 | underspecification | **HIGH** | digest 角色视图实现 + `test_status_digest_roles.py` 的单读断言（P4） | `plan.md:36`（D-8）、`contracts/status-digest-role-view.contract.md:7`（C-1）、`data-model.md:31-41`（§2.1 三载体）、`plan.md:17`（registry 仅 cross-check） | digest 契约规定角色视图以「导入引擎纯求值函数 + 传入 digest 已读的 registry entries + 单次状态读取」构建，但角色边的主载体是 team 报告、driver 脊/sidecar 与 run-agent 记录三族，digest 现只读 line-registry 条目与三元组——按声明输入得不到目标角色边；且引擎契约（C-1）未声明可导入的纯函数名/签名/输入集 | 归属：`status-digest-role-view` C-1 + `role-edge-engine` C-1 + plan D-8，由 plan 修订轮统一定义输入集与单读断言语义 |
| W2-02 | inconsistency | **HIGH** | 引擎判违例实现 + P2 变异演练（c）「move a role claim off its edge → red」 | `data-model.md:10`（`dual-role` = both-roles 标记）、`:22`（`dual-role` = 授予派发职责）、`:57`（superagent ⇔ 父出 ≥1 条边）、`:69`（`unbacked-role-claim` 谓词） | `dual-role` 被定义为「授予派发职责即标记」的双角色标记，而 superagent 又被定义为「父出 ≥1 条边」；`unbacked-role-claim` 却把映射行 `role=dual-role` 当作 superagent 主张并在无子边时判违例——任何已获授权但尚未/无需派发的 dual-role 子执行体都会被判违规 | 归属：`data-model.md` §1/§2/§4/§5 的定义收敛（或明确违例仅对「显式 superagent 声明且无支撑边」成立） |
| W2-03 | inconsistency | **HIGH** | tasks → implement（P5 的实施与既有套件回归） | `plan.md:209`（Phase 0 #5）、`tests/contract/test_fast_fail_discipline.py:729-763`（`TPL_EXPECTED = 35` / `LIVE_EXPECTED = 36`，`:751-752`） | plan Phase 0 #5 断言「no contract test pins the section count (only set-containment)」，但既有测试精确钉住顶层 section 数并要求「加/删 `##` 段落须在同一提交升降 pin」；新增 `## Super Agent (相对逻辑角色)` 将使其转红，而 P5/D-10 与 Mirror Obligations 均未列该 pin 更新 | 归属：plan D-10/P5 增列 `test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22` 的 pin +1 义务，并更正 Phase 0 #5 实测表述 |
| W2-04 | inconsistency | MEDIUM | 引擎输出 schema + `test_role_edge_engine.py` 断言（P2） | `contracts/role-edge-engine.contract.md:33-34`（C-3 键集）、`data-model.md:22-25`（§2 字段）、`:53-61`（§4 字段） | 引擎契约的 `executors[]`/`edges[]` 键集与 data-model 字段表不一致：新增 `dispatch_duty`（与 `role_declaration=dual-role` 同义，data-model 未定义）与 executor `sources`（data-model 无此字段），同时 data-model §4 声明的 `state`/`last_activity`/`age`/`stale` 不在引擎输出中——而 data-model 自称只固定「引擎消费的字段形状」 | 归属：`role-edge-engine` C-3 与 `data-model.md` §2/§4 二选一为 owner 后对齐（契约或数据模型） |
| W2-05 | underspecification | MEDIUM | 引擎边记录填充 + 确定性排序（P2） | `data-model.md:21`（`attempt` 字段）、`:31-41`（三载体行形态）、`contracts/role-edge-engine.contract.md:34`（edges `attempt`）、`:54`（C-7 排序键） | `attempt` 是 Role Edge 必备字段与确定性排序键，但三种唯一可解析的载体形态（team 映射表、driver sidecar 六字段、run-agent `unit_id`/`run_id` 对）都不携带 attempt——其取值来源未声明 | 归属：`data-model.md` §2.1 逐载体声明 `attempt` 的取得规则（如 report stamp / status 产物后缀） |
| W2-06 | inconsistency | MEDIUM | 引擎冲突输出 + 多边报告可读性（P2） | `plan.md:33`（D-5 写 `conflict`）、`data-model.md:25`（`conflicts` 为边内字段）、`contracts/role-edge-engine.contract.md:36`（顶层 `conflicts[]` 仅 `field`/`paths`）、`:58`（C-8） | 冲突行有三种形状：plan 写 `conflict`（单数）、data-model 把 `conflicts` 嵌在边记录内、契约输出顶层 `conflicts[]` 且无父/子/attempt 标识——多边报告中冲突行无法归属到具体边 | 归属：`role-edge-engine` C-3/C-8（补边身份或改为边内嵌套）并统一标识符；plan D-5 措辞随之对齐 |
| W2-07 | underspecification | MEDIUM | 恢复/状态推导实现 + digest `state` 渲染（P2/P4） | `data-model.md:59`（`state` 闭域）、`:97`（消息类 `attention-escalation`）、`:111`（§10 恢复标记） | data-model §10 说恢复会把仍运行的子项标记为 `interrupted` / `attention`，但 §4 的 `state` 闭域只有 `running/completed/failed/cancelled/unknown`；两个标记未定义载体、未进入任何域，`attention` 又与消息类 `attention-escalation` 混用 | 归属：`data-model.md` §4/§10（为标记定义字段或扩展闭域，并区分消息类词表） |
| W2-08 | ambiguity | MEDIUM | 引擎 CLI 输入校验 + 空集/缺失根行为（P2） | `contracts/role-edge-engine.contract.md:16`（registry = cross-check root）、`:25`（空边集 = clean/exit 0）、`:27`（required input root 缺失 = exit 2）、`plan.md:32`（D-4） | 契约以「required input root 缺失/不可读」判 exit 2，但从未声明四个 root 中哪些是 required；`--registry-dir` 被标为 cross-check-only，其缺失究竟记 exit 2 还是可忽略未定，并与同一契约的「空边集 = clean」并存 | 归属：`role-edge-engine` C-2（枚举 required/optional root 及各自缺失时的退出语义） |
| W2-09 | underspecification | MEDIUM | digest 合并 entry schema + `test_status_digest_roles.py`（P4） | `contracts/status-digest-role-view.contract.md:11`（C-2 字段名）、`:15`（merged entry set）、`:22`（C-4 每 child 一行）、`:30`（C-6 既有键不变） | 契约要求把执行体行并入既有 line 导向的 entry 集，同时要求 JSON 键沿用 C-2 的名字：`id` vs 既有 `line_id`、`last_activity` vs 既有 `last_activity_at` 与 C-6「既有键名不变」冲突；非 line 子行的 `project_dir`/`branch`/`stage` 取值亦未定义 | 归属：`status-digest-role-view` C-2/C-6（声明按来源类型的合并行 schema 与字段映射） |
| W2-10 | registry | MEDIUM | 注册表读取者 / 后续 implement 与 review 的特性认知 | `.specify/features.md:102`（095 行）、`.specify/features/095-superagent-role.md:10`（Key Changes 2）、`plan.md:30`（D-2）、`:34`（D-6） | Feature 注册表两处仍写「只读角色-边判定**引擎动作**」与「**三类**违例」，与 plan D-2 的新独立引擎、D-6 的四类封闭违例集不一致 | 归属：Feature 详情 Key Changes + 索引行描述（按 plan D-2/D-6 收敛；feature-integration 的 key changes/notes 义务） |
| W2-11 | duplication | LOW | 引擎默认值实现（P2） | `plan.md:17`、`contracts/role-edge-engine.contract.md:16`、`skills/external/sdd-loop-driver/scripts/line-registry.py:145-153` | line registry 的默认解析链（`$SPECIFY_LINE_REGISTRY_DIR` → `$XDG_STATE_HOME/spec-kit/lines` → `~/.local/state/spec-kit/lines`）在 plan 与引擎契约各复制一份，其 owner 是 `line-registry.py` | 归属：契约 C-1 改为「同 `line-registry.py` 的解析」，plan 处改为指针（One Source of Truth） |
| W2-12 | coverage-gap | LOW | Feature 详情 → plan 的覆盖映射（读者/评审） | `feature-ref.md:14`（第 1 行）、`contracts/harness-landing.contract.md:17-24`（C-2） | feature-ref 把「新 owner 页」映射到 harness C-2，但 C-2 只治理 agent-definitions/subagent-definitions/framework-map 的指针行；owner 页自身内容没有任何契约条款承载（仅由 P1 的定义测试守卫） | 归属：`feature-ref.md` 第 1 行（改指 FR-001/P1 + `test_superagent_definitions.py`，或在 harness 契约补 owner 页条款） |

## 已核对读数（plan / contracts 的事实断言复测）

> 除注明外均为只读命令；未运行测试套件（按 analyze 阶段只读纪律与 `run-tests.sh` 唯一入口规则）。

| 断言（出处） | 实测 | 结论 |
|--------------|------|------|
| `INSTRUCTIONS_BUDGET_BYTES = 38400`（plan:22、:175；harness C-4） | `scripts/bash/generate-instructions.sh:107` | 吻合 |
| live / template 字节 37,454 / 32,975，余量 946 B（plan:22、:175；quickstart:39） | `wc -c`：37,454 / 32,975；38,400 − 37,454 = 946 | 吻合 |
| 镜像基线 428 DIFF/ORPHAN（plan:146、:210） | `sync-mirrors.py --check`：437 行、428 条 DIFF/ORPHAN、exit 2 | 吻合 |
| `--only` 接受精确路径前缀（plan:148） | `scripts/python/sync-mirrors.py:37-38` | 吻合 |
| status-digest 三动作（plan:176、:206） | `scripts/python/status-digest.py:2279` | 吻合 |
| `NOTHING_RUNNING` 与 exit 3（plan:206；digest C-3） | `status-digest.py:94`、`:79`、`:1187` | 吻合 |
| digest JSON 键（digest C-6） | `:876-886` 与 `:1176-1177`（含 `profile`/`state_summary`） | 吻合 |
| digest 当前六列（digest C-8 前提） | 实跑 `--action digest`：线路/状态/阶段/已静默/标记/最近步骤与消耗 | 吻合 |
| exec-quant 导入先例（plan:176） | `status-digest.py:100`、`read_store` 于 `:864` | 吻合 |
| line-registry 24 actions（plan:205） | `skills/external/sdd-loop-driver/scripts/line-registry.py:2495-2520` 计数 24 | 吻合 |
| registry 默认链与 `parent_line_id`/`line_role` 字段（plan:173、:205；engine C-1） | `line-registry.py:145-153`、`:445-453` | 吻合（重复问题见 W2-11） |
| 派发面载体存在（plan:207；payload C-11） | `skills/internal/run-agent/SKILL.md:114`、`create-team/references/patterns.md:102-112`、`sdd-loop-driver/SKILL.md:20/49`、`stage-prompts.md:324` | 吻合 |
| 模板相邻标题（harness C-1） | `templates/instructions-template.md:266/272`；live `.specify/instructions.md:283/289` | 吻合 |
| 生成器从 mirror 模板生成（harness C-6） | `generate-instructions.sh:42/48` | 吻合 |
| `BUDGET:` 与 `Instructions size:` 日志（harness C-4；quickstart:46） | `generate-instructions.sh:167`、`:225` | 吻合 |
| `*-check.py` 兄弟命名（plan XVIII） | `scripts/python/` 下 9 个 `*-check.py` | 吻合 |
| py3.8 下界 / 实测 3.11.11（plan:15） | `pyproject.toml:5`、`python3 --version` | 吻合 |
| `run-tests.sh:319` exec 行（plan:172） | 实际第 319 行 | 吻合 |
| Feature 095 行 `Planned` / 详情存在（feature-ref；plan II） | `.specify/features.md:102`、`.specify/features/095-superagent-role.md` | 吻合 |
| **反例**：Phase 0 #5「无 section count pin」（plan:209） | `tests/contract/test_fast_fail_discipline.py:751-752`：`TPL_EXPECTED = 35`、`LIVE_EXPECTED = 36` | **不吻合 → W2-03** |

## 覆盖与链接摘要（读域内）

- **plan D-1…D-14 → Work Packages**：D-1→P1；D-2…D-7→P2；D-8→P4；D-9/D-14→P3；D-10→P5；D-11/D-12/D-13→P6。无未覆盖决策；包依赖（P2/P3/P5←P1，P4←P1/P2，P6←P1–P5）无环。
- **契约条款 → 守卫测试**：harness C-1/C-2/C-4/C-5/C-6 与 C-3 均有命名测试；engine C-1…C-11 → `test_role_edge_engine.py`；payload C-1…C-13 → `test_role_transition_payload.py`（C-8 等待/尝试仅引用既有 watch-model 行为，契约自身未列新增断言，记录为观察）；digest C-1…C-8 → `test_status_digest_roles.py`。未发现「契约条款零测试」；字段级缺口见 W2-04/W2-05/W2-06。
- **quickstart 4 场景 ↔ 契约/测试**：S1→engine C-1/C-10；S2→digest C-3/C-8；S3→payload C-2/C-3；S4→harness C-1/C-4/C-6。逐场景前提/执行状态行齐备。
- **feature-ref 6 行 ↔ 详情 Key Changes 6 项**：一一对应；第 1 行契约指针不精确（W2-12）。
- **Feature linkage / registry**：Feature 095 索引行 `Planned`、详情链接与 spec 链接在位、Last Updated 2026-11-10，与 feature-ref「Draft → Planned 由本 plan 拥有」一致；未新建/废弃 Feature。邻域交叉引用 027/085/093 存在于详情文件（feature-ref 声明成立）；详情 Clarify Notes 另提及候选 019，属候选比较语境，不作 finding。漂移见 W2-10。

## Constitution alignment（读域内）

- plan 的 22 行 Constitution Check 逐条自称 Pass；抽查 XXII（re-anchoring 指针）、XXI（引擎 CLI `--help`/`--version`/未声明选项拒绝）、XIV（owner 指针纪律）、XVII（仅新增按惯例的 `tests/fixtures/superagent-role/`）、XVIII（`*-check.py` 兄弟存在）、XX（`run-tests.sh` 唯一入口）均成立。
- 读域内**未发现 CRITICAL 原则冲突**。
- 观察（不 flag）：Feature 详情文件暂无 `## Implementation Notes`；模板与宪法要求该节，但同代先例 093 在 implement 阶段才落该节，按「按阶段落笔」的既有惯例处理，不按缺陷计（noise floor）。

## 度量与验证状态

- Findings 总数 **12**：CRITICAL **0** / HIGH **3** / MEDIUM **7** / LOW **2**。
- 类别计数：duplication 1；ambiguity 1；underspecification 4；constitution-conflict 0；coverage-gap 1；inconsistency 4；registry 1。
- 验证状态：3 条 HIGH 为**待验证提议值**——技能 §7 的独立只读验证波（fresh-context，每 finding 一 verdict + 两个 evidence-boundary 字段）不在本 Worker 派发范围，由集成分析者执行；本 Worker 未自验、未派发验证者。
- 复测命令集：`wc -c`、`sync-mirrors.py --check`、`status-digest.py --action digest`、定向 `Read`/`Grep`（行号、字段、标题、action 计数、pin 值）。未运行 pytest（analyze 只读；W2-03 依据静态断言，不依赖运行）。

## 限制与交由集成者复核的点

- `requirements.md`、`tasks.md` 不在读域：W2-03 的 tasks 覆盖（是否已有 pin 更新任务）、W2-10 的详情↔需求一致性，需集成者跨域复核；若已覆盖，相应行可降级或关闭。
- 本 Worker 的代码取证限于存在性/行号/字段/字节计数等定向只读核对，未整读代码文件；未消费其他 worker 的 findings 文件。

## 异常与披露

ANOMALY: 未发现异常 — 本 Worker 未触发 fast-fail 裁定点，无 in-passing repair，未修改任何制品；唯一写入为本 findings 文件与 wrap-up 三步记账。
