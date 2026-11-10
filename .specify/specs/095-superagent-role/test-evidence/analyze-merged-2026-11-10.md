# Analyze Merged Report — 095-superagent-role（2026-11-10）

- **Stage**: analyze（并发波归并 + 串行跨制品一致性）· **Line**: `095-superagent-role` · **Run**: `r20261110T055657Z-b095`
- **Contract**: `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md` / `references/validation-and-report.md`
- **Inputs（本报告的唯一来源，按读域次序）**: `test-evidence/analyze-findings-W1.md`（requirements × requirements-quality checklist）、`-W2.md`（plan / data-model / quickstart / feature-ref / contracts×4）、`-W3.md`（tasks）；`.specify/constitution.md`；`.specify/features.md` 与 `.specify/features/095-superagent-role.md`；`.specify/specs/095-superagent-role/` 的 requirements / plan / tasks / data-model / contracts / quickstart / feature-ref 全文（跨制品节）。
- **Deterministic engines（本阶段复跑）**: `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/095-superagent-role` → **exit 1，`status: uncovered`**；ID/severity 机械复算（grep/awk：W1 29、W2 12、W3 10，跨文件重复 ID = 0）；Feature 索引计数（header `Total Features: 90` = 数据行 90）。W2/W3 引用的 `sync-mirrors.py --check`、`validate-tasks.py` 读数取自其原文证据。
- **只读声明**: 本集成未修改任何分析制品（除本报告与 Wrap-up 记账）；未修复任何 finding、未派发新 Worker、未 push。
- **C/H 验证状态**: 本集成简报（任务 1–5）**未派发独立验证波**；下列 CRITICAL/HIGH 均为**检测者提议值**，集成者在跨制品复核中对其中锚点逐条直接重读（标记 `(re-read by integrator)`）；独立验证与门禁裁决归驱动的 U4。**本报告不得被读作「ready to implement」**。

---

## 0. 顶部汇总：CRITICAL / HIGH（计数 + 逐条指针）

**集成后计数**: CRITICAL **2** · HIGH **12** · MEDIUM **32** · LOW **8** = **54 行**（Worker 51 + 跨制品新增 3）。

- Worker 分源：W1 **29**（2C / 4H / 20M / 3L）· W2 **12**（0C / 3H / 7M / 2L）· W3 **10**（0C / 3H / 4M / 3L）
- 跨制品新增：X-01 **HIGH** · X-02 **HIGH** · X-03 MEDIUM
- 超限披露：单报告 50 行上限被波次总量超出（54 > 50）；本报告按证据保全不裁剪、不抑制，仅以本节与 severity 排序控制阅读。

| # | ID | 来源 | 一句话指针 | 锚点 |
|---|----|------|-----------|------|
| 1 | **W1-01** | W1 | FR-013 内联复述 attribution 五个取值且无 owner 路径（宪法 XIV 枚举副本） | REQ:139；CONST:285-293；CHK:35 |
| 2 | **W1-02** | W1 | Feature 详情缺 `## Implementation Notes` / `## Related Files`，宪法要求四节 MUST | FEAT:3-54；CONST:546-550；TMPL:33-52 |
| 3 | **W1-03** | W1 | 双角色机读形态三种互斥写法（集合+marker / 三并列值 / subagent+dual-role） | REQ:125、197、38、210 |
| 4 | **W1-04** | W1 | FR-005 第四类违例「深度越界」无验收场景，且角色深度无上限使其无定义 | REQ:128、39、210、127 |
| 5 | **W1-05** | W1 | 「角色声明」无具名持久化载体，「无对应边的角色声明」不可机判 | REQ:128、109、134 |
| 6 | **W1-06** | W1 | 九项注入只按 `[[STR-003]]` 子串判定，删任一项仍通过，与 SC-002 矛盾 | REQ:147、211、146 |
| 7 | **W2-01** | W2 | digest 角色视图按声明输入（已读 registry entries）拿不到三族角色边；引擎纯函数签名未定 | plan:36（D-8）；digest C-1；data-model §2.1 |
| 8 | **W2-02** | W2 | `unbacked-role-claim` 把「授予派发职责」误当「superagent 主张」，已授权未派发者被误判违例 | data-model §1/§2/§4/§5 |
| 9 | **W2-03** | W2 | plan Phase 0 #5 断言「无 section-count pin」，实测 pin 为 35/36 且要求同提交升降；任务无该 pin 更新行 | plan:209；`tests/contract/test_fast_fail_discipline.py:751-752` |
| 10 | **W3-01** | W3 | 镜像义务声称「11 行」，与 plan 表 **10 行** / T050 枚举 **12 文件** 均不符，单位未定义 | tasks:19、237；plan:150-161 |
| 11 | **W3-02** | W3 | FR-011…FR-016 六个连续 FR 在任务图中零引用（任务行从 FR-009 跳到 FR-017） | tasks:147；全文件普查 |
| 12 | **W3-03** | W3 | GATE-4/DoD-6 要求的 smoke 证据文件无任何任务运行或生成，T053 只记录结果 | tasks:240、22、34 |
| 13 | **X-01** | 集成者（新） | FR-036 字面「全套契约测试全绿」与 plan/GATE-1「零新增失败 vs 基线」的完成门判据不一致 | REQ:177；plan:195；tasks:31、238 |
| 14 | **X-02** | 集成者（新） | FR-006「任一侧无法解析 MUST 报悬空」与引擎 C-4「未知身份 = exit 2 具名错误」机器行为相反 | REQ:129；role-edge-engine C-2/C-4 |

**门禁含义（技能 §9，不修复）**: CRITICAL 必须在 `/speckit.implement` 前解决；HIGH 组须经处理或经验证波/U4 显式裁决后才可放行；MEDIUM/LOW 可带建议推进。本报告不提供或应用任何修复编辑。

---

## 1. W1 — requirements × requirements-quality checklist（读域次序 1）

- **Unit**: `/speckit.analyze` 并发波 Worker W1 · Worker run `r20261110T055657Z-b095-w1`
- **Read domain（文件级互斥）**: `.specify/specs/095-superagent-role/requirements.md`、`checklists/requirements-quality-2026-11-10.md`
- **归并核对**: 29 行，ID `W1-01…W1-29` 字典序（机械复算通过）；severity = 2 CRITICAL / 4 HIGH / 20 MEDIUM / 3 LOW。

### 1.1 Findings（原文表）

| ID | Severity | Propagation surface | Category | Anchor(s) | 一句话事实 | 建议归属（指针） |
|----|----------|---------------------|----------|-----------|------------|------------------|
| W1-01 | CRITICAL | plan → contracts / tasks（枚举可能被复制） | Constitution — One Source of Truth | REQ:139；CONST:285-293；CHK:35（CHK016） | FR-013 内联复述既有 attribution 的五个取值（`own / foreign / stale-run / unattributed / legacy`）且未给出 owner 路径，正是宪法 XIV 禁止的枚举副本。 | `/speckit.requirements`：改为 owner 路径 + 摘要指针。 |
| W1-02 | CRITICAL | Feature governance（`FEAT` 记录） | Constitution — Feature Documentation Requirements | FEAT:3-54；CONST:546-550；TMPL:33-52；FIDX:102 | 绑定 Feature 的详情文件没有 `## Implementation Notes` 与 `## Related Files` 节，而宪法 Feature Documentation Requirements 将四节列为 MUST。 | `/speckit.features`（或所属命令）：恢复强制节；实现内容可后补。 |
| W1-03 | HIGH | role-edge contract + SC-001 测试 | Inconsistency / Ambiguity | REQ:125、REQ:197、REQ:38、REQ:210；CHK:18（CHK002）、CHK:72（CHK038） | 双重角色的机读形态有三种互不相容的写法——FR-002 的 `{subagent, superagent}` 集合加 `dual-role` 标记、Key Entities 的 `superagent / subagent / dual-role` 三个并列值、SC-001 的 `subagent` + `dual-role`（无 `superagent`）——契约测试无法同时满足。 | `/speckit.requirements`：钉住一种形态，US1 AS2 / SC-001 / Key Entities 改为引用它。 |
| W1-04 | HIGH | role-edge contract + SC-001 | Inconsistency / Coverage | REQ:128、REQ:39、REQ:210、REQ:127；CHK:19（CHK003） | FR-005 列出第四类违例「深度越界」，但没有任何验收场景测试它，且 FR-004 规定角色深度无上限，使该类无定义。 | `/speckit.requirements`：用正交的 SDD 许可链限制定义它并给 owner，或删除并对齐 US1 AS3 / SC-001。 |
| W1-05 | HIGH | role-edge contract + SC-001 | Underspecification（Gap） | REQ:128、REQ:109、REQ:134；CHK:20（CHK004） | FR-005 要求判定「无对应边的角色声明」，但没有任何既有记录被指明承载「角色声明」，违例不可机判。 | `/speckit.requirements` / plan：指明持久化的声明载体（如派发记录字段），或删除该类。 |
| W1-06 | HIGH | role-transition payload contract + SC-002 | Inconsistency / Measurability | REQ:147、REQ:211、REQ:146；CHK:31（CHK012） | 声明的派发前自检只按 `[[STR-003]]` 子串判定，删去九项中任意一项仍会通过，与 SC-002 的逐项阻断要求矛盾。 | `/speckit.requirements` / contract：为九项定义机读句柄，或把 SC-002 改为标记级阻断。 |
| W1-07 | MEDIUM | role-edge contract | Ambiguity（输入边界） | REQ:128、REQ:126；CHK:21（CHK005） | FR-005 未定义输入记录集与执行树边界（单根/多根、跨 run 无关记录如何隔离），边与深度结果在不同仓库上不可确定。 | plan / contract：钉住记录选择与根集合规则。 |
| W1-08 | MEDIUM | role-edge contract + SC 集 | Inconsistency（覆盖） | REQ:126、REQ:128、REQ:210-219；CHK:22（CHK006） | FR-003 要求 `conflict` 报错并点名两处路径，但 FR-005 的输出枚举没有它、也没有任何 SC 验证它，该 MUST 既无输出归宿也无红测。 | `/speckit.requirements`：把 conflict 纳入引擎输出契约并由 SC 覆盖（或显式路由到既有门禁）。 |
| W1-09 | MEDIUM | role-edge contract | Ambiguity（优先级） | REQ:126、REQ:283；CHK:23（CHK007） | FR-003 允许根身份取状态脊 `run_id` 或 line registry `line_id` 而未给优先级，A11 只把实现名交给 plan。 | plan / contract：钉住优先级与回退根标记。 |
| W1-10 | MEDIUM | role-edge / return contract + SC-005 | Underspecification（Gap） | REQ:126、REQ:139、REQ:214；CHK:24（CHK008） | 边记录要求「派发尝试标识」，FR-013 的重试/陈旧判定依赖它，但没有既有字段被指明为该标识。 | plan / contract：把尝试标识解析到具体字段并加入边记录。 |
| W1-11 | MEDIUM | role-transition payload contract | Inconsistency（措辞） | REQ:146、REQ:262；CHK:30（CHK011） | FR-017 同时允许超集（「MUST 至少包含」）与禁止增项（「九项即封闭清单」），第十分项的合法性未定义。 | `/speckit.requirements`：改为「恰好九项」（Clarifications Q3 已按封闭读）。 |
| W1-12 | MEDIUM | protocol contract | Ambiguity（owner + 可扩展性） | REQ:136、REQ:262；CHK:32（CHK013） | FR-010 声明封闭消息分类集却把 owner 写成未具名的「owner 文档」，同时又说「最少区分四类」，owner 与可扩展规则都未固定。 | `/speckit.requirements`：点名 owner（新定义页）并只保留一种封闭语义。 |
| W1-13 | MEDIUM | protocol contract | Gap（载体） | REQ:136、REQ:142；CHK:33（CHK014） | 四类消息中的 `ack` 与 `attention-escalation` 未映射到任何既有载荷/回传通道，行使它们就会造出 FR-016 禁止的第二通道。 | plan / contract：逐类映射到既有载体，或删类。 |
| W1-14 | MEDIUM | edge lifecycle contract | Gap（载体） | REQ:141；CHK:34（CHK015） | FR-015 要求把 `completed / failed / cancelled` 写入既有载体，但没有既有记录被指明承载 `cancelled`。 | plan / contract：指明载体/取值，或收窄到既有词表。 |
| W1-15 | MEDIUM | recovery contract + SC-005 | Gap（词表/载体） | REQ:162、REQ:214；CHK:46（CHK024） | FR-027/SC-005 要求把仍被判定在跑的子项标为 `interrupted` / `attention`，但词表 owner 与承载标记的记录都未具名。 | plan / contract：点名词表 owner 与状态载体。 |
| W1-16 | MEDIUM | recovery contract + SC-005 | Gap（可观测性） | REQ:163、REQ:140、REQ:214；CHK:47（CHK025） | FR-028 要求 resume 前重验证授权，但只有失败路径有具名记录；没有记录区分「已重验证的恢复」与「未验证的恢复」。 | plan / contract：指明重验证证据（与派发拒绝记录同形）。 |
| W1-17 | MEDIUM | state-sync contract | Gap（写目标） | REQ:160；CHK:43（CHK021） | FR-025 要求在下一个外部动作前持久化「边 + 已收到返回」，却未指明具体 per-entry 载体，而唯一被引用的 run report 是单文件产物。 | plan / contract：点名 per-entry 文件，并把外部动作集声明为封闭。 |
| W1-18 | MEDIUM | status-read contract | Inconsistency | REQ:161、REQ:167；CHK:44（CHK022） | FR-026 要求从状态层、Assignment 事实层与宿主事件层派生，FR-029 又要求同一次状态读取；该单次读取覆盖哪几层未说明。 | plan / contract：说明读取的层覆盖与 liveness 进入方式。 |
| W1-19 | MEDIUM | digest contract + SC-006 | Ambiguity（有界性） | REQ:167、REQ:169；CHK:51（CHK026） | 「条目 MUST 有界」未说明 cap 是单条还是整集、`omitted` 在哪个集合上声明，FR-031 的父+子形状可能被静默截断。 | plan / contract：定义 cap 单位、`omitted` 范围与扇出原子性。 |
| W1-20 | MEDIUM | run-report mapping + digest contract | Inconsistency | REQ:167、REQ:168；CHK:52（CHK027） | FR-029 要求每行显示父边身份，FR-030 的映射表 schema（`label → 角色 → 工作区`）没有父列，也未给 join 规则。 | `/speckit.requirements` / plan：声明父身份来源（FR-003 父侧记录）或加列。 |
| W1-21 | MEDIUM | dispatch-face contract + SC-002/003/007 | Coverage | REQ:175、REQ:211-216；CHK:59（CHK031） | FR-034 要求 team 与 driver 阶段载荷携带角色字段，但 SC-002 只验证 run-agent 注入、SC-003 只验证边记录，两个接线点无验证。 | `/speckit.requirements`：为两个载荷点增加 SC 断言。 |
| W1-22 | MEDIUM | test-plan + SC-009 | Ambiguity / Coverage | REQ:177、REQ:178、REQ:218；CHK:60（CHK032） | FR-036 的「全套契约测试」未定义是 `contract` 标记、整个 `tests/` 还是具名模块清单，且没有 SC 验证改写/保持/移除处置台账。 | `/speckit.requirements` / plan：钉住套件范围、解释器矩阵与台账判据。 |
| W1-23 | MEDIUM | appendix contract + SC-010 | Measurability | REQ:182、REQ:219；CHK:68（CHK037） | FR-038/SC-010 要求「可解析证据路径」却未定义可解析（存在/可解析内容/命令可复现），也未把切片集钉到测量时点或 commit，附录检查不可复现。 | `/speckit.requirements`：定义可解析判据与切片集测量点。 |
| W1-24 | MEDIUM | requirements → plan（规范内容） | Traceability / Inconsistency | REQ:266、REQ:182、REQ:264、REQ:174；CHK:66（CHK035） | Clarifications 声称 FR-038「已按本裁定补句」，但 FR-038 正文既无「切片机制主张」也无「not-observed 理由」要求；FR-033 的段标题/位置也只存在于 Clarifications。 | `/speckit.requirements`：把声称的补句落入 FR-038/FR-033，或更正声明。 |
| W1-25 | MEDIUM | authorization contract | Ambiguity（形态覆盖） | REQ:140、REQ:130、REQ:69-70；CHK:37（CHK018） | FR-014 的封闭授权面（能力键/席位策略/路由裁决/team territory）未被证明能为 SSH 形态或通用非 SDD 扇出给出可解析授权依据。 | `/speckit.requirements` / plan：为跨主机与通用扇出声明授权依据。 |
| W1-26 | MEDIUM | owner-doc assertions + SC-007 | Measurability | REQ:173、REQ:174、REQ:216、REQ:284；CHK:57（CHK029） | FR-032/FR-033 与 SC-007 禁止复制 owner 规则文本并要求转红，但没有客观判据区分合法指针与副本，红腿依赖散文判断。 | plan / contract：定义结构化的指针判据（路径存在性、规则正文标记缺失）。 |
| W1-27 | LOW | Shared Strings 表 | Traceability | REQ:239-241、REQ:128、REQ:175、REQ:127；CHK:67（CHK036） | `Consumed by` 单元格漏记三处实际引用（STR-002←FR-005、STR-003←FR-034、STR-004←FR-004/FR-034），表不自述其引用图。 | `/speckit.requirements`：补三格；可选把反向核对加入引用约定。 |
| W1-28 | LOW | 预算测量记录 | Traceability | REQ:285、REQ:174；CHK:58（CHK030） | A13 记录三个字节数与 946 B 余量，但无可复现命令或证据路径，测量无法仅凭需求重导。 | `/speckit.requirements`：补日期化命令/证据路径；触发条件本身归生成器 `over` 状态。 |
| W1-29 | LOW | owner-doc assertions | Ambiguity | REQ:173、REQ:269；CHK:56（CHK028） | FR-032 的 owner 文档内容清单要求「术语边界」，却未点名要消歧的术语，该节的完整性不可断言。 | `/speckit.requirements`：点名术语（如 execution/driver/orchestrator/supervisor）或指向 glossary 协议。 |

### 1.2 C/H 行的证据边界（原文，待验证波/U4 确认）

- **W1-01**：FR-013 自身称这些取值是「既有」（REQ:139）；制品内无 owner 路径。若验证者认定外部不存在该枚举 owner，则「副本」claim 收窄，但「缺 owner 路径」仍成立。
- **W1-02**：详情文件存在可被读作等价物的节（`Plan Notes`、`Related Specifications`）；其是否满足宪法四节是验证者的判断。缺失的是宪法点名的节标题本身。
- **W1-03**：SC-001 与 Key Entities 原文已引；`[[STR-002]]` 是否意在代替集合第二个成员是读法问题，但三处形态不一致是事实。
- **W1-04**：若「深度越界」实指 SDD 许可链限制，则缺的是定义与 owner，而不是违例类本身。
- **W1-05**：FR-008 的载荷角色声明存在，但其持久化未声明；「声明载体 = 派发记录」是可修复的假设。
- **W1-06**：若九项各自拥有可匹配句柄，FR-018 的子串机制可逐项扩展；需求文本目前只点名 `[[STR-003]]` 子串。

### 1.3 Checklist 问责（pass H）

**等式**：39 unchecked = 29 raised-as-finding + 10 covered-by + **0 unraised/undispositioned**。
**`[Gap]` 子集**：9 = 7 raised（CHK004/008/015/016/021/024/025）+ 2 covered-by（CHK010/019）+ 0。
逐条 disposition（CHK001–CHK039）见 `analyze-findings-W1.md` § Checklist 问责；旧 `checklists/requirements.md` 经复算为全勾选、0 `[Gap]`，不产生未处置项。

### 1.4 其他检测面（A / B / C / D / F / G）

- **A 重复**：stale-copy decision test 后 0 条合格 finding（逐面约束与验收映射不构成事实副本）。
- **B/C/F**：已逐条落为 W1-03…W1-29。
- **D 宪法对齐**：W1-01（XIV）、W1-02（Feature Documentation Requirements）为两处 MUST 面；其余原则未发现冲突。
- **G 注册表 / Feature linkage**：`Related Feature` 095 与索引行 / 详情文件 ID/Name/Spec Path 一致；`Planned` 在 analyze 阶段合法。唯一 registry finding 为 W1-02 的详情结构。
- **E / I**：不在 W1 读域（E 由 W3 与集成者裁决；I 由 W2 读域与集成者裁决——本报告 §4/§5 记录）。

### 1.5 Metrics / Systemic / Limits（原文摘要）

- Requirements：287 行 / 53,696 B；38 FR（连续）；10 SC（final 7 / supporting 3）；6 Shared Strings；5 用户故事；10 Edge Cases；16 Clarification Q；15 Assumptions；清单头部机械声明经 W1 全数实测为真。
- Findings：29 条 = 2C / 4H / 20M / 3L；C/H 验证状态 = pending。
- **SO-1**：W1-07…W1-10、W1-17…W1-20 同指「规格命名概念、字段级 schema 下推 plan/contracts」的弱面（簇级信号）。
- **SO-2**：W1-04、W1-06、W1-21…W1-23 的 SC 断言其结果，而支撑机制未定义或弱于结果要求。
- **SO-3**：W1-01 是明确 SoT 违规；FR-030 的「结构 slug + 运行戳」为较弱同型实例。
- Limits：读域隔离使 pass E/I、clause coverage、plan/tasks 映射不在 W1；验证波前 C/H 不是门禁结论；`downgrade` 对宪法 finding 不适用。

---

## 2. W2 — plan / data-model / quickstart / feature-ref / contracts（读域次序 2）

- **Read domain（8 文件，互斥）**: `plan.md`、`data-model.md`、`quickstart.md`、`feature-ref.md`、`contracts/harness-landing.contract.md`、`contracts/role-edge-engine.contract.md`、`contracts/role-transition-payload.contract.md`、`contracts/status-digest-role-view.contract.md`
- **归并核对**: 12 行，ID `W2-01…W2-12` 字典序；severity = 0 CRITICAL / 3 HIGH / 7 MEDIUM / 2 LOW。

### 2.1 Findings（原文表；`**HIGH**` 为原文强调）

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

### 2.2 已核对读数（W2 复测摘要）

- 20 项事实断言复测：**19 项吻合 + 1 项反例**。反例 = plan Phase 0 #5「无 section count pin」（实测 `tests/contract/test_fast_fail_discipline.py:751-752` 的 `TPL_EXPECTED = 35` / `LIVE_EXPECTED = 36`）→ W2-03。
- 吻合项覆盖：预算 38,400 / 37,454 / 32,975 B、镜像基线 428 DIFF/ORPHAN、`--only` 精确前缀、digest 三动作与 JSON 键、`NOTHING_RUNNING` + exit 3、exec-quant 导入先例、line-registry 24 actions 与默认链、派发面载体、模板相邻标题 266/272 ↔ live 283/289、生成器来源、`BUDGET:` 日志行、`*-check.py` 兄弟命名、py3.8 下界与实测 3.11.11、`run-tests.sh:319`、Feature 095 行 `Planned`。完整表见 W2 原文。

### 2.3 覆盖 / 链接 / 宪法 / Metrics / Limits（原文摘要）

- **D-1…D-14 → Work Packages**：无未覆盖决策；包依赖无环。
- **契约条款 → 守卫测试**：未发现「契约条款零测试」；字段级缺口见 W2-04/05/06。
- **quickstart 4 场景 ↔ 契约/测试**：逐场景前提/状态行齐备。
- **feature-ref 6 行 ↔ 详情 Key Changes 6 项**：一一对应；第 1 行指针不精确（W2-12）。
- **Feature linkage**：索引 `Planned`、详情链接、Last Updated 2026-11-10 一致；漂移见 W2-10。
- **Constitution alignment（读域内）**：未发现 CRITICAL 原则冲突；观察（不 flag）：详情暂无 `## Implementation Notes`，按 093 先例与「按阶段落笔」惯例未计缺陷——**与 W1-02 构成跨 Worker 张力，见 §4.4 T-1**。
- **Metrics**：12 条 = 0C / 3H / 7M / 2L；类别 duplication 1 / ambiguity 1 / underspecification 4 / constitution 0 / coverage-gap 1 / inconsistency 4 / registry 1；HIGH 为待验证提议值。
- **Limits**：requirements/tasks 不在读域；W2-03 的 tasks 覆盖、W2-10 的需求一致性交集成者复核（本报告 §4.2 已复核）。

---

## 3. W3 — tasks.md（读域次序 3）

- **Read domain（唯一 spec 文件）**: `.specify/specs/095-superagent-role/tasks.md`；W3 run `r20261110T073257Z-b095`
- **归并核对**: 10 行，ID `W3-01…W3-10` 字典序；severity = 0 CRITICAL / 3 HIGH / 4 MEDIUM / 3 LOW。

### 3.1 Findings（原文表）

| ID | Severity | Category | propagation_surface | Anchor（文件:行） | 一句话事实 | 建议归属（指针） |
|---|---|---|---|---|---|---|
| W3-01 | HIGH | inconsistency（计数/包含性声明） | DoD-3 / T050 的镜像义务验证门 | `.specify/specs/095-superagent-role/tasks.md:237`（并见 :19） | T050/DoD-3 声称镜像义务共 **11 行**，但 T050 括号内枚举 `definitions ×4 + template ×1 + engine ×1 + digest ×1 + skills ×5` 合计 **12** 项，且未声明“行数 vs 文件数”的单位，故“11 行每行都有 write+verify”无法从本文件机械判定。 | `/speckit.tasks`：对齐 `plan.md` § Mirror Obligations（行数 owner）并给出逐行映射；若 plan 本身为 12 行，先改 plan 再回写本文件。 |
| W3-02 | HIGH | coverage-gap | 任务 → 实现（六个 FR 无任何任务落点） | `.specify/specs/095-superagent-role/tasks.md:147`（全文件普查；可追溯规则见 :55） | 全文件普查显示 **FR-011…FR-016** 六个连续 FR 在任何任务行中都未被引用（引用从 FR-009 直接跳到 FR-017），这六个需求在任务图中没有落点。 | `/speckit.tasks`：对照 `requirements.md` 补齐任务或记录显式处置；FR-011 / FR-016 在覆盖率会计的契约引用组 lane 中同样未覆盖。 |
| W3-03 | HIGH | underspecification（证据生产者缺失） | GATE-4 / DoD-6 的完成门证据 | `.specify/specs/095-superagent-role/tasks.md:240`（DoD-6 :22；GATE-4 :34） | T053 只“记录” `smoke_command` / `smoke_exit_code=0` / `smoke_evidence_path=test-evidence/smoke-six-modules.txt`，但没有任何任务运行该 smoke 命令或生成该证据文件，GATE-4 要求的“存在且非空”文件没有生产者。 | `/speckit.tasks`：新增 smoke 运行行，或把显式运行并入 T053 并记录真实退出码。 |
| W3-04 | MEDIUM | inconsistency（验收口径） | US1 独立测试 / 验收 | `.specify/specs/095-superagent-role/tasks.md:116`（并见 :114, :124, :129） | US1 独立测试写“**三类**违例夹具各自非零”，而同故事目标、T013 夹具清单与 T015 的闭合违例集都是**四类**（self-dispatch / dangling-parent / unbacked-role-claim / depth-inconsistent）。 | `/speckit.tasks`：改为四类，与 T011/T013/T015 对齐。 |
| W3-05 | MEDIUM | inconsistency（依赖叙述漂移） | 任务派发顺序 | `.specify/specs/095-superagent-role/tasks.md:263`（并见 :254, :158） | “User Story Dependencies”称 US2 与 US1 的唯一交叉点是“T028 引用 T005 / T041 的产物”，但 T028 的阻塞集是 T005,T027，T041 是更晚的 US5 行，且 :254 已声明 US2 与 US1 无硬依赖——依赖叙述与 `blockedBy` 图不一致（该小节与 Phase Dependencies 近乎重复，漂移埋在其中）。 | `/speckit.tasks`：按 `blockedBy` 图重写该句，或删除重复小节只留一处 owner。 |
| W3-06 | MEDIUM | inconsistency / coverage-gap（声明 vs 确定性 lane） | analyze 覆盖率汇总 / 实现 | `.specify/specs/095-superagent-role/tasks.md:52`（并见 :90 T003） | 格式节声明“未声明的契约子句是可接受的留白”（严格子集），但 `account-clause-coverage.py --spec-dir .specify/specs/095-superagent-role` 返回 `status: uncovered`、exit 1、**29 条本特性契约子句超出冻结基线**（已声明仅 9/38），且本文件没有任何 DoD/GATE 行覆盖该 lane，两种口径互斥。 | `/speckit.tasks` + 覆盖率契约 owner：裁定该 lane 是否为门——是则补 green 声明与门项，否则在任务文件记录为何 `uncovered` 可接受。 |
| W3-07 | MEDIUM | underspecification（证据落点缺失） | SC 验证证据（US4 / US5） | `.specify/specs/095-superagent-role/tasks.md:200, :222` | T038 与 T044 只说 “record readings” 而未命名落盘文件，与同文件其它转绿行（均给出 `test-evidence/...` 路径）不一致，而 DoD-6 要求每条 SC 有来源指针。 | `/speckit.tasks`：为两行分别指定 `test-evidence/` 证据文件。 |
| W3-08 | LOW | inconsistency（机器标记 vs 散文） | 并行派发 | `.specify/specs/095-superagent-role/tasks.md:151, :284`（并见 :280, :292） | T021 未标 `[P]` 而 Parallel Opportunities 与 Parallel Example 都说 T021–T025 可同批并行；Polish 的 T046/T049/T050 也未标 `[P]` 而 :284 说 T049/T050 可与 T046 并行——`[P]` 标记与并行说明漂移。 | `/speckit.tasks`：对齐 `[P]` 标记与并行说明，保持其一为 owner。 |
| W3-09 | LOW | ambiguity | 任务输入构造 | `.specify/specs/095-superagent-role/tasks.md:123` | T012 说取 `data-model.md § 2.1` 的 “three carrier forms”，括号内却列出四个载体组（teams/、state/、logs/、registry/），且未说明 registry/ 是 cross-check 而非 carrier。 | `/speckit.tasks`：按 `data-model.md § 2.1` 对齐“三载体 + cross-check”的表述。 |
| W3-10 | LOW | underspecification（未命名载体） | 任务 → 实现 | `.specify/specs/095-superagent-role/tasks.md:146, :234` | T019 的“six downlink role fields block”与 T047 的“a deterministic check”都没有给出自身载体路径 / 实现归属（只给了产物或变异副本路径），与本文件 :54“每行含精确文件路径”的自定规则不一致。 | `/speckit.tasks`：为两处命名载体（夹具文件 / 检查脚本或其复用的 Tool）。 |

### 3.2 Coverage verdict（确定性 lane，W3 原文读数）

- `account-clause-coverage.py --spec-dir .specify/specs/095-superagent-role` → **exit 1，status: uncovered**（未用 `--freeze`）。
- `[clause-uncovered]` fail：669 uncovered，其中 **29 beyond the frozen baseline**；本特性已声明（green）9 条，四契约合计 38 条。29 条分布：`harness-landing` C-2/C-4/C-6（3）、`role-edge-engine` C-2…C-10（9）、`role-transition-payload` C-1/C-3…C-12（11）、`status-digest-role-view` C-2…C-6/C-8（6）→ 与 tasks.md:52 严格子集政策冲突（W3-06）。
- `[fr-uncovered]` fail：19/38（契约引用组 lane，名单：FR-001/002/003/004/006/007/011/016/017/022/023/024/025/026/027/030/036/037/038；FR-011、FR-016 同时命中 W3-02）。
- `[clause-unparsable]` fail：107（语料级，1 个 positive-form parse doubt；基线内）；`coverage-baseline-delta` fail(29)：基线 640 names vs tasks.md:79 记 642 行（差值与文件头行一致，不单列 finding）。
- **Method note（非 W3 finding）**：技能 §3 示例命令写 `--spec <spec-dir>`，引擎声明的是 positional 或 `--spec-dir`（`--spec` 被拒，exit 2）——归 analyze-artifacts 技能源文件；见 §5.5 FO-095-09。

### 3.3 其余读数（W3 原文摘要）

- **Feature / registry**：tasks.md:5 绑定 Feature 095，`Planned`；T054 在翻转前记录 review，时序自洽；索引行实际内容不在 W3 读域（由集成者复核，见 §4.2）。
- **Constitution（pass D）**：读域内未发现 CRITICAL；IV / VII / IX / XII / XIV / XVII / XX / XXI 抽查通过。
- **Premise checks**：`validate-tasks.py` PASS 0 error / 0 warning；任务引用文件全部存在、声明应不存在的 9 个新产物全部不存在；预算 / 模板锚点 / digest 动作 / `test_i13` 存在性核对通过。
- **Metrics**：54 任务行（T001–T054 无缺口）；6 新契约测试模块；包计数 7/13/10/6/6/9；FR 引用 32/38、SC 10/10；green 9/38。
- **Limits**：pass H 与 pass I 不在 W3 读域（H 由 W1 完成、I 由集成者在本报告 §4/§5 裁决）；未整读 requirements/plan/contracts。

---

## 4. 跨制品一致性（串行集成者；requirements ↔ plan ↔ tasks ↔ contracts）

读域互斥解除后的独立检查：对 coverage、术语、判据与数字声明四类逐对核对。**与既有 Worker finding 完全同源的条目只进 §4.2 确认表，不重复计 severity**；真正新发现才给 X-ID 并计入顶部计数。

### 4.1 新增跨制品不一致（本集成者检测）

| ID | Severity | 制品对 | 锚点 | 一句话事实 | 建议归属（指针） |
|----|----------|--------|------|------------|------------------|
| X-01 | **HIGH** | requirements ↔ plan ↔ tasks | REQ:177（FR-036）；plan:193-195（Inherited Blockers #4）；tasks:31（GATE-1）、:238（T051） | FR-036 字面要求「处置后的**全套契约测试** MUST 在 `>=3.8` 上**全绿**」；plan Inherited Blocker #4 把 093 的 frozen-baseline reds 判为 095 写域之外、按「FR-036: no NEW red caused by this feature」读；GATE-1/T051 以 `comm -13` 的**零新增失败**为门——完成门判据在两处不一致；若基线含既有红，字面「全绿」不可达。 | `/speckit.requirements` 或 plan：钉住唯一判据（全绿 vs 零新增）并回写另一处。 |
| X-02 | **HIGH** | requirements ↔ contracts | REQ:129（FR-006）；`contracts/role-edge-engine.contract.md:21-42`（C-2/C-4） | FR-006 要求「任一侧无法解析 MUST **报悬空**并点名两侧路径」；引擎 C-4 却把**未知身份的 query** 定为 **exit 2**（具名输入错误），不是 `dangling-parent` 违例（exit 1）——同一输入在规格与契约下的机器可观察行为相反。 | requirements 或 engine contract：统一 query 未知身份的语义（violation vs input error）。 |
| X-03 | MEDIUM | plan ↔ data-model / tasks | plan:33（D-5）；`data-model.md:43-49`（§3）；tasks:129（T015） | 根/父身份解析顺序两版：plan D-5 为 `run_id → line_id → literal root`；data-model §3（及 T015 的「exact order」）为 `label → line_id → run_id → literal root → dangling`。同一 token 同时命中 line_id 与 run_id 时解析结果不同（W1-09 的「缺优先级」修复落了两处且彼此不一致）。 | plan 或 data-model：二选一为 owner 并回写另一处（契约 C-1 亦应引用该 owner）。 |

**X 行证据边界**：X-01 已证实两处判据文本与命令形式；未运行套件，因此「当前树是否实际含基线红」未由本报告测量（plan 文本自述存在 frozen-baseline reds）。X-02 已证实两处文本；尚无测试同时钉住两种行为。X-03 已证实两处顺序；是否发生真实 token 跨空间碰撞未测量（边界情形）。

### 4.2 跨制品复核确认表（既有 Worker finding 的制品对证据）

| 主题 | 制品对 | 对应 Worker finding | 复核结论（`(re-read by integrator)`） |
|------|--------|---------------------|----------------------------------------|
| 违例类别基数 三 vs 四 | FR-005 四类 ↔ SC-001 三类 ↔ plan D-6 四类 ↔ engine C-5 四类 ↔ tasks US1 IT 三类 | W1-04、W3-04 | 确认：SC-001 欠覆盖第四类；tasks IT 文案漂移。 |
| 双角色机读形态 | FR-002 集合+marker ↔ Key Entities 三并列值 ↔ SC-001 `subagent`+`dual-role` ↔ data-model §1/§2 ↔ engine C-3 `role_declaration`+`dispatch_duty` ↔ digest C-2 集合 | W1-03、W2-04 | 确认：契约层采用集合语义，需求层存在三种写法。 |
| `unbacked-role-claim` 谓词 | FR-005「无对应边的角色声明」↔ data-model §2（`dual-role` = 授予职责）/§4（superagent ⇔ 出边 ≥1）/§5（谓词）↔ engine C-5 | W2-02 | 确认：授予职责 ≠ 主张已有边，谓词会误伤已授权未派发者。 |
| digest 角色视图输入 | plan D-8 ↔ digest C-1 ↔ data-model §2.1 ↔ plan:17（registry 仅 cross-check） | W2-01 | 确认：按「已读 registry entries」单读输入建构不出三族角色边；引擎纯函数签名未声明。 |
| section-count pin | plan Phase 0 #5 ↔ `test_fast_fail_discipline.py:751-752` ↔ tasks（无 pin 更新行） | W2-03 | 确认（集成者 grep：tasks 无 `TPL_EXPECTED`/`LIVE_EXPECTED`/section-count 字样；T048 台账未列该 pin）→ W2 提出的降级条件不成立。 |
| FR-011…FR-016 任务覆盖 | requirements ↔ tasks | W3-02 | 确认（集成者 grep 复算：六者引用数均为 0）。 |
| 镜像义务 11/12/10 | tasks DoD-3:19、T050:237 ↔ plan:150-161 表 | W3-01 | 确认（plan 表体 **10 行**，T050 枚举 **12 文件**；「11」与两者均不符，且「行 vs 文件」单位未定义）。 |
| conflict 行形状与身份 | FR-003 ↔ data-model §2 边内 `conflicts` ↔ engine C-3 顶层 `conflicts[]` ↔ plan D-5 单数 | W2-06 | 确认：顶层行无父/子/attempt 身份，多边报告不可归属。 |
| `attempt` 载体 | FR-003/FR-013 ↔ data-model §2.1 三载体 ↔ engine C-3/C-7（排序键） | W2-05 | 确认：三种载体均不携带 attempt，取值来源未声明。 |
| digest JSON 键名 | digest C-2（`id`/`last_activity`）↔ C-6（既有键名不变：`line_id`/`last_activity_at`）↔ 既有 digest JSON | W2-09 | 确认：合并行 schema 与既有键名冲突，非 line 子行字段未定义。 |
| 映射表 parent 列 | FR-030（`label → 角色 → 工作区`）↔ FR-029（每行父边身份）↔ plan D-9 / contract C-11（四列含 `parent`） | W1-20 | 确认：契约/计划已加 parent 列，需求 FR-030 文本未回写。 |
| `interrupted`/`attention` 词表 | FR-027/SC-005 ↔ data-model §4 `state` 闭域 vs §10 恢复标记 | W1-15、W2-07 | 确认：两标记不在闭域、无载体，且与消息类 `attention-escalation` 混用。 |
| 覆盖率政策 | tasks §Format:52「严格子集可接受」↔ accountant `[coverage-baseline-delta]` 29 ↔ T003 implement 起点再冻结 | W3-06 | 确认并**扩大**：T003 的 `--freeze` 会把 29 条并入新基线、令 delta lane 归零，「严格子集」政策将实质自我确认。 |
| 注册表内容漂移 | Feature detail:10（「三类违例」「引擎动作」）/ index:102 ↔ plan D-2/D-6 | W2-10 | 确认：状态 `Planned` 合法，但两处描述与 plan 的新独立引擎/四类封闭集不一致。 |
| FR-017 超集 vs 封闭 | FR-017「MUST 至少包含」+「九项即封闭清单」↔ payload contract C-2（closed） | W1-11 | 确认：同段两种语义；契约取封闭。 |
| FR-010 封闭 vs 最少四类 | FR-010 ↔ data-model §8 / payload C-7（四 token） | W1-12 | 确认：owner 具名（新 owner 页）但「最少」与「封闭」并存。 |
| team/driver 字段判据 | FR-034（父身份/子 label/角色声明 三字段）↔ engine C-1 与 payload C-11（六字段）↔ T020（每个接线面六字段） | W1-21 | 确认并补充：契约严于需求（六 ⊇ 三，无行为冲突），但 SC-002/SC-003 未验证 team/driver 两个接线点。 |
| FR-038 判据承载 | FR-038 ↔ plan D-12 / T046 ↔ Clarifications Q8（「已按本裁定补句」） | W1-24 | 确认并跨制品化：plan D-12 与 T046 均要求「机制主张」与 `not-observed` **理由**，FR-038 正文未承载。 |
| 根身份优先级 | plan D-5 ↔ data-model §3 / T015 | W1-09 | 演化为 **X-03**：两处修复互不一致。 |
| 其余 MEDIUM/LOW | — | W1-07/08/10/13/14/16/17/18/19/22/23/25/26/28/29；W2-05…W2-12 未列者；W3-05/07/08/09/10 | 维持 Worker 原文与归属指针；本次串行复核未新增跨制品证据，也未发现需要升降级的证据。 |

### 4.3 已检查且不构成 finding 的项（noise floor / 边界说明）

- **数字声明一致**：预算 37,454 / 32,975 / 38,400 B 与 946 B 余量在 A13、plan:22/:175、quickstart:39、tasks:71 间一致；tasks 额外记录的「可用最后一字节 945 B」来自 `size >= budget` 触发语义，是对同一事实的更严格读法，不是矛盾。
- **切片计数一致**：14 切片（080–091、093、094；092 缺失）在 plan D-12、tasks DoD-7、T046 间一致。
- **镜像基线一致**：428 DIFF-class（含 422 DIFF + 6 DIFF[projected]）与 plan:146/:210、tasks:72 一致；`wc -l = 437` 是已记录的 trap。
- **六字段下行清单**：FR-008、data-model §6、payload C-1、T020 一致（FR-034 只点名三字段，属子集表述，已在 §4.2 记录）。
- **六个新契约测试模块**：plan Scope、DoD-1、T004/T011/T020/T034/T040/T041 一致。
- **契约子句计数**：engine 11 + payload 13 + digest 8 + harness 6 = 38，与 green 声明 9 条相容复算。
- **Feature 状态**：`Planned` 在 index/detail/tasks/feature-ref 一致（W1 pass G、W2、W3 三读同意）；内容漂移单列 W2-10。
- **格式/风格项**：按 do-not-flag 清单不报（措辞偏好、已一致的模板占位、既有脏文件等）。

### 4.4 跨 Worker 张力（不裁决，交验证波 / U4）

- **T-1（W1-02 vs W2 噪声底线）**：W1 依宪法 CONST:546-550 判 Feature 详情缺 `## Implementation Notes` / `## Related Files` 为 CRITICAL；W2 依「093 在 implement 阶段才落该节」的同代先例判为噪声底线、不计缺陷。事实层面两读都成立：095 详情确有 `Plan Notes`/`Related Specifications` 而无上述两个字面节；093 详情有 `## Implementation Notes`（:43）但同样用 `## Related Specifications` 而非模板的 `## Related Files`（模板 :49）。宪法权威优先时 W1-02 维持 CRITICAL；最终由验证波/U4 裁决。
- **T-2（W2「无 CRITICAL」）**：W2 的宪法结论限于其读域（plan/contracts/data-model/quickstart/feature-ref），与 W1 在读域内发现两处宪法 CRITICAL 不冲突。
- **T-3（W2-03 的降级条件）**：W2 提出「若 tasks 已覆盖该 pin 可降级」；集成者实测 tasks 无任何 section-count pin 更新行 → 条件不成立，维持 HIGH。
- **T-4（W3-06 与 T003 的相互作用）**：见 §4.2 覆盖率政策行；建议由覆盖率契约 owner 裁定该 lane 是否为门，再决定是否允许 implement 起点 `--freeze`。
- **T-5（W1-09 → X-03）**：W1 要求钉住优先级；plan 与 data-model 各钉了一版且顺序不同 → 新发现 X-03。

---

## 5. 汇总读数

### 5.1 Coverage Summary

| 维度 | 读数 | 来源 |
|------|------|------|
| Clause coverage（本特性） | `status: uncovered`，exit 1；claimed 9 / 38 子句；**29 beyond frozen baseline**（分布见 §3.2） | 集成者复跑 accountant（2026-11-10） |
| 语料级 | 290 文件 = 183 parsed + 107 named-unparseable；clause universe 2037 names / 2056 ids；1 parse doubt；48 errors / 1 warning | 同上 |
| Baseline | 640 names；640 baseline-internal uncovered 不阻断本特性；delta 29 为阻断项 | 同上 |
| FR 任务行引用 | **32 / 38**（缺 FR-011…FR-016，W3-02）；SC **10 / 10** | 集成者 grep 复算 |
| FR 契约引用组 lane | **19 / 38 uncovered**（名单见 §3.2） | accountant |
| Checklist 问责（pass H） | 39 unchecked = 29 raised + 10 covered-by + **0** unraised/undispositioned；`[Gap]` 子集 9 = 7 + 2 + 0；旧 checklist 全勾选 | W1 + 集成者复算 |

**零 finding 底线**：不适用（本波 findings 非零）；无 CRITICAL/HIGH 时的重读采样要求因此不触发。

### 5.2 Feature Linkage Summary

| 项 | 读数 |
|----|------|
| 绑定 Feature | 095 Super Agent Role（索引行 `.specify/features.md:102`，状态 `Planned`，Last Updated 2026-11-10） |
| 详情文件 | `.specify/features/095-superagent-role.md`（ID/Name/Spec Path 一致；结构缺口见 W1-02；内容漂移见 W2-10） |
| 索引计数 | header `Total Features: 90` = 数据行 90（机械复算） |
| 生命周期 | `Planned` 在 analyze 阶段合法（`feature-integration.md`：checklist 后仍由 implement 翻转）；三份 Worker 读法一致 |
| Linkage 置信度 | 高（显式绑定 + 同号惯例 + 详情链接在位） |

### 5.3 Constitution Alignment

- **CRITICAL 2**：W1-01（XIV One Source of Truth——FR-013 枚举副本）；W1-02（Feature Documentation Requirements——详情缺两个 MUST 节）。均为检测者提议值，宪法 finding 不适用 `downgrade`。
- 其余原则：W2 读域与 W3 读域均未发现 CRITICAL 冲突；W1 其余原则未见冲突。
- 跨制品新增 X-01/X-02/X-03 为判据冲突而非原则冲突（其修复归属 requirements/plan/contracts 修订）。

### 5.4 Metrics

| 指标 | 值 |
|------|-----|
| Worker findings | 51（2C / 10H / 31M / 8L） |
| 跨制品新增 | 3（0C / 2H / 1M / 0L） |
| 集成后总量 | **54**（2C / 12H / 32M / 8L）；超 50 行上限 4 行（已披露，未裁剪） |
| Requirements | 38 FR / 10 SC / 6 STR / 5 US / 10 Edge / 16 Q / 15 A |
| Tasks | 54 行（8 阶段）；22 个 `[P]`（机械计数 24 含说明文字命中）；6 个新契约测试模块计划 |
| Contract clauses | 38（engine 11 / payload 13 / digest 8 / harness 6） |
| C/H 验证状态 | **pending**：独立验证波未派发（简报任务 1–5 未含）；锚点由集成者直接重读 |
| Downgrade rate | **n/a**（无验证波，不产生 confirm/reject/downgrade 计数） |
| 跨 Worker 重复 ID | **0**（前缀不相交）；「先声明先得」破平规则无适用对象 |
| Rerun delta | **n/a**（本特性首次 analyze；`test-evidence/` 无更早的 analyze 报告） |

### 5.5 Systemic Observations（簇级，不抬升单行 severity）

- **SO-A（schema 簇收敛失败）**：W1-07…W1-10、W1-17…W1-20 的「字段级 schema 下推 plan/contracts」在 W2 读域内并未收敛——data-model 与引擎/digest 契约在 `role_declaration`/`dispatch_duty`/`sources`/`conflicts`/`attempt`/键名上互相不一致（W2-04/05/06/09）。这是簇级信号：下推不是放弃，接收方必须显式收敛。
- **SO-B（机制 vs 验证簇）**：W1-04/06/21…23 与 W3-03 同型——SC/DoD/GATE 断言的结果强于已定义机制或证据生产者；修复方向是补机制/生产者或收窄断言，而非在验收时解释。
- **SO-C（SoT 模式）**：W1-01 与 W2-11 是同一模式的两个实例（枚举/默认链被复制而非引用）——修复方向统一为「指向 owner 路径」。
- **SO-D（门禁内的数字声明）**：W3-01（11 行）、W2-03（section-count pin 不存在）、tasks:79（642 行 vs 基线 640 names）显示 DoD/GATE 文本中的手写数字会漂移；建议门禁数字由 owner 文件派生或改为命令引用。
- **框架观察（供 080–094 观测面）**：
  - **FO-095-09**：analyze 技能 §3 示例与命令模板写 `account-clause-coverage.py --spec <spec-dir>`，引擎实际接受 positional 或 `--spec-dir`（`--spec` 被拒，exit 2）——owner：`.specify/skills/internal/analyze-artifacts/SKILL.md` §3 与 `.qoder/commands/speckit.analyze.md`（生成源 `templates/commands/analyze.md`）。
  - **FO-095-10**：命令模板称「the seven detection passes」，技能 §5 的 owner 表述为「Eight passes（A–G + I）plus one checklist pass（H）」——两处计数不一致，owner 在技能源文件。

## 6. Next Actions（技能 §9；不自动修复）

1. **CRITICAL（2）**：先由 `/speckit.requirements` / `/speckit.features` 处置 W1-01、W1-02；宪法节修改不在本技能范围。
2. **HIGH（12）**：按归属分流——requirements（W1-03…W1-06、X-02 的语义裁定）、plan（W2-01…W2-03、X-01、X-03）、tasks（W3-01…W3-03）；处理后可重跑 `/speckit.analyze` 生成 rerun delta。
3. **MEDIUM/LOW（40）**：可随上述修订一并处置或显式延后（`/speckit.todo` / 台账）。
4. **验证波**：正式门禁前应补一次独立只读验证波（fresh-context、与检测者不相交）或由 U4 显式裁决；本报告不冒充该结论。
5. 本报告未应用任何修复编辑；后续命令由用户/驱动者自行发起。
