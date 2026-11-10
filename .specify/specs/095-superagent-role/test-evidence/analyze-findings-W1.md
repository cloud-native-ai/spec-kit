# Analyze Findings — W1（requirements × requirements-quality checklist）

- **Unit**: `/speckit.analyze`（并发波 Worker W1）· **Run**: `r20261110T055657Z-b095-w1`（线 run `r20261110T055657Z-b095`）· **Stage**: analyze · **Date**: 2026-11-10
- **Read domain（文件级、互斥）**: `.specify/specs/095-superagent-role/requirements.md`、`.specify/specs/095-superagent-role/checklists/requirements-quality-2026-11-10.md`
- **Governance inputs read（非 spec 制品）**: `.specify/constitution.md`；`analyze-artifacts` SKILL 及其 `references/`；`.specify/features.md` 与 `.specify/features/095-superagent-role.md`（registry pass）；`feature-integration.md`、`one-source-of-truth.md`、`objective-analysis-gate.md`、`feature-details-template.md`；`.specify/state/095-superagent-role.md`（run 标识）
- **Not read（按读域隔离，属其他 Worker / 集成者）**: `plan.md`、`tasks.md`、`data-model.md`、`contracts/`、`quickstart.md`、其他 `test-evidence/` 文件。因此 **pass E（task 覆盖）与 pass I（decision tension）不由 W1 裁决**；clause/FR coverage accountant 未由 W1 运行（属集成者第 3 步）。
- **只读声明**: 未修改任何制品；本文件是唯一产物。C/H 行等待集成者的独立验证波；MEDIUM/LOW 按技能跳过验证。
- **same-author**: 制品由本线前序阶段代理撰写；W1 是 analyze 波派发的 fresh-context 只读检测者（即 same-author gate 的委派载体），未参与撰写。
- **锚点前缀**: `REQ:` = `requirements.md`；`CHK:` = `checklists/requirements-quality-2026-11-10.md`；`CONST:` = `.specify/constitution.md`；`FEAT:` = `.specify/features/095-superagent-role.md`；`FIDX:` = `.specify/features.md`；`TMPL:` = `.specify/templates/feature-details-template.md`。

## 裁决摘要

29 条 findings：**2 CRITICAL / 4 HIGH / 20 MEDIUM / 3 LOW**。其中 6 条 C/H（W1-01…W1-06）**尚待独立验证波确认**；在确认并处置前，本证据不支持「ready to implement」的 analyze 门禁通过。23 条 MEDIUM/LOW 为建议级。

## Findings

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

### C/H 行的证据边界（待集成者验证波确认）

- **W1-01**：FR-013 自身称这些取值是「既有」（REQ:139）；制品内无 owner 路径。若验证者认定外部不存在该枚举 owner，则「副本」claim 收窄，但「缺 owner 路径」仍成立。
- **W1-02**：详情文件存在可被读作等价物的节（`Plan Notes`、`Related Specifications`）；其是否满足宪法四节是验证者的判断。缺失的是宪法点名的节标题本身。
- **W1-03**：SC-001 与 Key Entities 原文已引；`[[STR-002]]` 是否意在代替集合第二个成员是读法问题，但三处形态不一致是事实。
- **W1-04**：若「深度越界」实指 SDD 许可链限制，则缺的是定义与 owner，而不是违例类本身。
- **W1-05**：FR-008 的载荷角色声明存在，但其持久化未声明；「声明载体 = 派发记录」是可修复的假设。
- **W1-06**：若九项各自拥有可匹配句柄，FR-018 的子串机制可逐项扩展；需求文本目前只点名 `[[STR-003]]` 子串。

## Checklist 问责（pass H）

**等式**：39 unchecked = 29 raised-as-finding + 10 covered-by + **0 unraised/undispositioned**。
**`[Gap]` 子集**：9 = 7 raised（CHK004/008/015/016/021/024/025）+ 2 covered-by（CHK010/019）+ 0。

- CHK001 disposition: covered-by requirements.md §FR-001 / §FR-002 / §FR-005
- CHK002 disposition: raised-as-finding W1-03
- CHK003 disposition: raised-as-finding W1-04
- CHK004 disposition: raised-as-finding W1-05
- CHK005 disposition: raised-as-finding W1-07
- CHK006 disposition: raised-as-finding W1-08
- CHK007 disposition: raised-as-finding W1-09
- CHK008 disposition: raised-as-finding W1-10
- CHK009 disposition: covered-by requirements.md §FR-008 / §FR-005
- CHK010 disposition: covered-by requirements.md §FR-022 (d) / §FR-011 (e) / §FR-010 + Clarifications Q3 (g)
- CHK011 disposition: raised-as-finding W1-11
- CHK012 disposition: raised-as-finding W1-06
- CHK013 disposition: raised-as-finding W1-12
- CHK014 disposition: raised-as-finding W1-13
- CHK015 disposition: raised-as-finding W1-14
- CHK016 disposition: raised-as-finding W1-01（FR-012 半边 covered-by requirements.md §FR-012）
- CHK017 disposition: covered-by requirements.md §FR-009 / §FR-019 / §FR-020
- CHK018 disposition: raised-as-finding W1-25
- CHK019 disposition: covered-by requirements.md §FR-022 / §FR-024（owner 文件存在性核对不在 W1 读域）
- CHK020 disposition: covered-by requirements.md §FR-022 / §FR-023（grain 与读数三元组归既有 owner）
- CHK021 disposition: raised-as-finding W1-17
- CHK022 disposition: raised-as-finding W1-18
- CHK023 disposition: covered-by requirements.md §FR-026 / §SC-005
- CHK024 disposition: raised-as-finding W1-15
- CHK025 disposition: raised-as-finding W1-16
- CHK026 disposition: raised-as-finding W1-19
- CHK027 disposition: raised-as-finding W1-20
- CHK028 disposition: raised-as-finding W1-29
- CHK029 disposition: raised-as-finding W1-26
- CHK030 disposition: raised-as-finding W1-28（触发条件半边 covered-by requirements.md §FR-033 / §A7）
- CHK031 disposition: raised-as-finding W1-21
- CHK032 disposition: raised-as-finding W1-22
- CHK033 disposition: covered-by requirements.md §FR-035 / §SC-008 / §Measurement Sources SC-008
- CHK034 disposition: covered-by requirements.md §US3 Independent Test / §A3
- CHK035 disposition: raised-as-finding W1-24
- CHK036 disposition: raised-as-finding W1-27
- CHK037 disposition: raised-as-finding W1-23
- CHK038 disposition: raised-as-finding W1-03
- CHK039 disposition: covered-by checklists/requirements-quality-2026-11-10.md §七（39/39 均可由需求正文或点名 owner 行回答，无一条要求运行产品）

## 其他检测面（pass A / B / C / D / F / G）

- **A 重复**：stale-copy decision test 后 0 条合格 finding。`MUST NOT 新建第二 renderer/parser` 在 FR-029/030/031/035 的重复属于逐面约束（作用面不同），不是漂移副本；US2 AS1 复述九项属验收场景映射，不构成事实副本。
- **B 歧义 / C 欠指定 / F 不一致**：已在上表逐条落为 W1-03…W1-29。
- **D 宪法对齐**：W1-01（XIV One Source of Truth）、W1-02（Feature Documentation Requirements）为两处 MUST 面；其余原则（IV/VII/IX/XXI 等）在需求文本中未发现冲突。
- **G 注册表 / Feature linkage**：requirements 的 `Related Feature` 095（REQ:14-15）与 `FIDX:102` 行、`FEAT` 详情文件的 ID/Name/Spec Path 一致；`FIDX` 行数 90 与 header `Total Features: 90` 一致（机械核对）；`Planned` 在 analyze 阶段是合法状态（`feature-integration.md:29-38`：checklist 只在 implement 之后发起迁移，plan 落 Planned，tasks 维持）。唯一 registry finding 为 W1-02 的详情结构。
- **E / I**：不在 W1 读域，未裁决（见文件头）。

## Metrics

- **Requirements**：287 行 / 53,696 B；38 FR（FR-001…FR-038，连续）；10 SC（final 7 / supporting 3）；6 Shared Strings；5 用户故事；10 Edge Cases；16 Clarification Q（6 + 10）；15 Assumptions（A1–A15）。
- **Checklist**：39 条（`grep -c '^- \[ \] CHK'` 复算）；9 条含 `[Gap]`；29 raised + 10 covered-by + 0 unraised/undispositioned。
- **Findings**：29 条 = 2 CRITICAL / 4 HIGH / 20 MEDIUM / 3 LOW；C/H 验证状态 = pending（集成者验证波）。
- **清单头部机械声明核对**：287/53,696、38 FR、10 SC、6 STR、5 US、10 edge cases、16 Q、15 A、39 CHK 全部实测为真。

## Systemic Observations

- **SO-1（记录 schema 簇）**：W1-07…W1-10、W1-17…W1-20 同指一个弱面——规格命名了概念，但字段级 schema 交给 plan/contracts；这是簇级信号，不据此提高任何单条 severity。
- **SO-2（机制 vs 验证簇）**：W1-04、W1-06、W1-21…W1-23 的 SC 断言其结果，而支撑机制未定义或弱于结果要求；W2 可核对 plan/contracts 是否已闭合。
- **SO-3（SoT 模式）**：W1-01 是明确违规；FR-030 的「结构 slug + 运行戳」（REQ:168）是同一模式的较弱实例，为避免重复行未单列，修复方向相同（改为 owner 路径）。

## Limitations

- 读域隔离使 pass E/I、clause coverage accountant、plan/tasks 侧映射无法在本文件裁决；这些属集成者与 W2/W3。
- C/H 行的严重度在验证波前不是门禁结论；`downgrade` 对宪法 finding（W1-01/W1-02）不适用（技能 carve-out）。
- 本清单的检测流程读数（35 行、1 行实测反驳、29 追溯条目）是 checklist 阶段自报，W1 读域内无法独立复算；W1 只复算了其计数与引用类声明。
- W1-02 的等价节判断、W1-03 的 marker 语义属验证者裁量，已在证据边界中披露。

## Integrator handoff

- **验证波输入**：W1-01…W1-06（2 CRITICAL + 4 HIGH），每条附 id/category/claim/severity/evidence location；检测者与验证者需为 disjoint set。
- **W2 可核对**：W1-07/08/09/10/17/18/19/20/21/26 是否已被 plan/contracts 闭合。
- **W3 可核对**：W1-21/22 的任务覆盖；以及 tasks 是否已把上述 schema 落点钉住。
