# Specification Quality Checklist: 元技能治理：机制/策略分离与技能引用归一化（Meta-Skill Governance: Mechanism–Policy Separation & Skill Reference Grammar）

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-11-05
**Updated**: 2026-11-05（scope update：并入「技能引用语法与归一化」第二能力；新增判定项见 § Scope Update 2026-11-05。同日 clarify 复评：两条已知缺口在本轮裁决中落定，一条收窄为残留面）
**Feature**: `.specify/specs/083-mechanism-policy-separation/requirements.md`

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Stability / containment claims name a baseline referent and a derivable allowed-delta set (owner: `.specify/shared/guidelines/closed-set-claims.md`)
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria (with the gap recorded under Notes — SC-003)
- [x] No implementation details leak into specification

## Scope Update 2026-11-05 — 第二能力（技能引用语法与归一化）

> 判定对象是本轮 scope update 的增量部分（US5 / FR-019…FR-030 / SC-006…SC-009 / A11 / C9 / C10 / STR-004 / STR-005）。上一节的既有判定项对 083a 仍然成立，本节不重复。

### 新增可测性

- [x] US5 至少 3 个 Given/When/Then，且分别覆盖 bare name、引用形式归一化、`/speckit.*` 命令面消歧、失败语义四类（实测：4 个场景，四类各覆盖一次）
- [x] 每条新增 FR 可判定（判据不落在「看得出来」上）：FR-019…FR-030 每条都指向一个可读的产物位置或一条可跑的断言
- [x] 每条新增 SC 带 `**Path**:` 标注且已给 Measurement Source（SC-006 final / SC-007 final / SC-008 final / SC-009 final，四条均有 Source 行）
- [x] 新增 SC 的分母可机械取得（SC-006 ≥ 12 行 fixture；SC-007 五份接线 + 全仓扫描；SC-008 ≥ 1 正例 + ≥ 1 负例；SC-009 四类各一条），不存在「基数待定」的缺口

### 一源与封闭清单

- [x] 新 owner 文档唯一，且本规格**不复制**其文法（§ Functional Requirements F 组的引导段明写「只要求它拥有什么，不复述其表行」）
- [x] 五个消费方的接线义务写成「只声明自己的参数 + 路径引用」，MUST NOT 复制清单/顺序/失败表（FR-026）
- [x] SC-007 是包含性声明（「除 owner 以外零份」），已按 `closed-set-claims` 五要件在 Source 行写出：基线参照物、比较单元、允许差异集来源（owner / 生成镜像 / 既有测试字面量三类）、补集断言与结构不变量、未定义聚合词清零
- [x] Shared Strings 只登记被逐字消费的字面量；`/`、`@`、`SKILL.md`、`/speckit.*` 不登记（C10 给出理由）

### 边界与不自相矛盾

- [x] 两个能力的 owner 不互复制（C9），且与既有 owner 的边界写明（机制/策略 vs 引用文法 vs 位置阶梯三方各有所属）
- [x] 位置阶梯的唯一 owner 仍是 `skills/internal/run-skills/SKILL.md` § 1（FR-022 明写路径引用、禁止内联/新增位置）
- [x] 「零新增」与既有边界一致：零新命令、零新门禁脚本、零新目录根、零新环境变量（FR-029 对 C4 / C8 / FR-016 的引用而非重述）
- [x] 对并发实现的处置写清「起点 + 核验补齐 + 不推倒重写」（A11 / FR-027），且 `.specify/` 镜像的生成物身份写清（FR-028）
- [x] `Related Feature` 的 Feature ID 未变，名称的**落地改名**明确标为 clarify 的义务，本阶段不改注册表（避免「已完成」的假象）

### 已知缺口（如实记录，不掩盖）

- [x] **（2026-11-05 clarify：本阶段只落了 fixture，未落测试；缺口仍在）SC-006…SC-009 的复算载体此刻不存在**：全仓 `tests/` 对 `skill-reference` 的检索零命中，即该能力目前没有任何机器断言。四条的 `**Path**: final` 是**要求**（该状态须在实现完成后成立），不是当前读数。这与 083a 的 SC-001/SC-002/SC-005 属同一类"可测但载体待落"，已在 § Notes 记为本阶段的真实缺口。
- [x] **（2026-11-05 clarify 已裁决，修正归 plan/implement）owner 文档（起点实现）自身的归一化顺序与其接受形式表互相矛盾**：步骤 2 把任何含 `/` 的值判为路径，于是以 `/` 开头的斜杠引用永远走不到步骤 3 的剥前缀，`@/name` 无规则可归一，且步骤 5 的产物不是 FR-030 要求的三值封闭判定。逐条证据见 `test-evidence/requirements-scope-update-concurrent-impl-readout.txt` § 3。本规格以 FR-021 / FR-030 / SC-006 把这一矛盾变成可选性要求；**它没有被本阶段修复**（改造未提交的用户工作 + 在多种读法间选择，越出本阶段范围），故本条判为**未闭合**，随回传的 ANOMALY 行上送。**2026-11-05 clarify 落定**：目标顺序与输出语义已写入 `requirements.md` § Clarifications § Session 2026-11-05 的 ① 条（先剥标签与前缀、再判通道，输出恰为命令面／技能标识／失败三值），确定性复算载体为 `test-evidence/clarify-scope-update-fixture.json` + `…-fixture-probe.txt`；**owner 文件本身的修正仍属 plan/implement**，本轮未改任何未提交的 `skills/` 或 `shared/` 文件。
- [x] **（2026-11-05 clarify 已裁决，改写归 plan/implement）五处消费者引用的是镜像路径、本规格引用的是源路径**：两者内容今日逐字节相同（`cmp` 一致、`sync-mirrors.py --check` rc=0），但「消费者该写哪一种」没有 owner 裁决。本阶段不改任何一侧，作为 clarify 的裁决点登记（readout § 5）。**2026-11-05 clarify 落定**：以源路径 `shared/definitions/skill-reference-definitions.md` 为准，`.specify/` 镜像只作生成物（standalone 以相对框架根解析、不改写拼写）；五份 `SKILL.md` 的 8 处引用串随 plan/implement 改写，SC-007 的扫描项复核。

### 2026-11-05 clarify 复评（残留面，如实记录，不掩盖）

- [ ] **name 通道与 path 通道的判定集合尚未闭合**：`speckit.skills` 归 NAME、`speckit.skills/SKILL.md` 归 PATH —— 同一命令名的两种写法落在两个判定类，「命令面」判定是否覆盖带路径后缀的写法因而悬空。已落 `requirements.md` § Edge Cases 的「命令名带上像路径的后缀」一条（归一化必须先剥前缀再判路径；「保留原值」不得成为第四种结果），但**具体归属（name 通道输出形态 / 路径内外分类 / 接受形式增减）**是 ① 裁决的残留面，交 plan 与再一轮 clarify。
- [ ] **「名字可省扩展名」与「名字通道不剥 `.md`」的冲突**：`run-skills` § 1 输入契约说名称可省扩展名，而 `my-draft.md` 按归一化落 name 通道、名字里带 `.md`，与 `skills/external/foo`（无 `.md`、有 `/`）落 path 通道构成两个语义不同却共享输入族的失败。已并入 ① 的第 4、11 条要求 owner 消歧；`run-skills` 正文的改写属 plan/implement（它同时是 ② 的消费方之一）。
- [ ] **`@name` 的 CLI 可达性**：已裁决为 § Constraints C11（形态判定 MUST 是归一化的显式确定性步骤；CLI 形态下 `@name` 走零命中失败类并增记「该形式不可达」）；**形态判定步骤落在 owner、确定性程序，还是两者兼有** 属 plan 的设计选择，本阶段不预设。

## Notes

- **本次 scope update 的实测读数（2026-11-05，取自实跑而非手写）**：`validate-requirements.py` → `status: ok`、`scanned: 292 lines, 39 definition rows, 5 shared strings`、`0 error(s), 0 warning(s)`、rc=0（逐字存于 `test-evidence/validate-requirements-scope-update.txt`）；`pre-analyze-check.py --stage requirements` → `decision=pass`、`errors=0`、`advisories=52`、`fr=30`、`sc=9`；`decomposition-check.py --mode plan` → `decision=proceed`、`fr_count=30`、`fr_ceiling=30`（**零余量**）。四处逐字输出同存于 `test-evidence/requirements-scope-update-gates.txt`。本清单**不手抄 FR / SC 计数**：以该次运行的 `fr` / `sc` 字段为准。
- **零余量触发的结构变化（已落地，非计划）**：30 = 30，故不再新增第二个不切片的计划；`plan.md` 追加了 § Scope Snapshot 与 § Slice 083b 两节把第二个能力登记为切片 `083b-skill-reference-grammar`，`feature-ref.md` 追加了 § Slices 表。**083a 的既有计划内容（D1–D10、T-001–T-003、EP-001…EP-006、Measurement Plan）未被改动**。
- **本次修掉的两处计数漂移（disclosed，纠正而非改判据）**：FR/SC 总数变化后，`pre-analyze-check` 以 exit 2 报 `count-claim`（`plan.md` 第 16 行与 `feature-ref.md` 第 16 行把旧总数写成了当前事实）。两处改成指向 validator / decomposition 的实测输出，而不是写入一个新数字——按 `token-efficiency` 与 one-source-of-truth 的口径，规格产物的计数不应有第二个手写所有者。
- **上一轮（083a 建立时）的确定性 checker 记录（历史，未改）**：

- **Deterministic checker（所有计数的唯一权威）**：`python3 scripts/python/validate-requirements.py .specify/specs/083-mechanism-policy-separation/requirements.md` → `status: ok`；`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id` / `path-marker` 全 pass；`scanned: 211 lines, 23 definition rows, 3 shared strings`；`0 error(s), 0 warning(s)`；exit 0。逐字输出存于 `test-evidence/validate-requirements.txt`，本清单**不手抄任何计数**：23 个定义行 = 18 条 FR + 10 条 SC 中的定义行，拆分口径以该次运行的分项 pass 计数为准。
- **本 pass 修掉的两类问题（disclosed，非掩盖）**：① validator 的 4 条 `ref-resolvable`（2 条 error + 2 条 warning）——FR-001 / FR-017 的 `[[STR-001]]` / `[[STR-003]]` 被反引号包裹，落在代码 span 内故未被识别为引用；去掉外侧反引号后双向检查归零。② **同一判据的两处同文本枚举**：FR-001 原句把「机制侧=逻辑/算法/步骤/判定规则/可复用方法、策略侧=配置/输入/输出/运行环境绑定/目标目录/交付物落点」写进正文，而 § Terminology 有逐字相同的表；§ Assumptions A2 与 § Constraints C6 已明写后者是 dated record、owner 定稿后本规格不再更新，两处同步即为 FR-015 所禁的「复制 owner 内容」。已把枚举从 FR-001 移出、改由其判据段（§ Terminology 的「换掉运行环境要不要改」）与 FR-002(a) 派生，记录于 § Assumptions A10。此为纠正而非改判据：判据字句、Shared Strings 三行的值与 `Consumed by` 单元格、`Related Feature` 均未改动。
- **U4 驱动侧纠正（disclosed，非掩盖）**：完成收尾 pass 之后，U4 确定性门发现两处缺陷并已就地更正——① `pre-analyze-check.py --stage requirements` 以 exit 2 报「requirements.md carries no § Runtime Stack & Dependency Ownership」：已补该强制表（5 行，RS-001…RS-005，列与 081 同一 schema：`ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises`）；② SC 定义行使用全角冒号，checker 只识别 ASCII `:`，导致识别 0 条 SC 并产生 31 条 dangling-id：已将 `**SC-001**：`…`**SC-005**：` 改为 `**SC-001**:`…`**SC-005**:`。纠正后的四条门输出（validator / pre-analyze / decomposition / flow-class）逐字存于 `test-evidence/requirements-u4-gates.txt`。
- **预期 advisory（3 条，已登记，非缺陷）**：`shared/definitions/mechanism-policy-definitions.md` 尚不存在（由 plan/implement 创建）；本清单第 40 行的 `skills/external/...` 与 `shared/guidelines/...` 是类路径占位而非真实路径。
- **Flow class（类别声明的机器读数）**：`python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:083-mechanism-policy-separation"` → `flow_class: execution`、`source: declaration`、`marker: null`、exit 0；输出存于 `test-evidence/flow-class-lookup.txt`。故 `source` 由声明（[[STR-001]] 行）解析而非按默认兜底，`path-marker` 的「`execution` 类须至少一条 `final` path」这一条据此适用并通过。
- **`Stability / containment claims` 的判定依据（判通过，理由同处可见）**：本规格只有 **SC-003** 一条包含性声明，它按 owner 五要件写足——① 基线参照物：`[[STR-002]]` 指名的实现起点提交；② 比较单元：按产物类声明（技能与命令模板两类路径），不用「其余 / 叶子 / 未受影响」等聚合词；③ 允许差异集来源：按产物类声明并**配漂移守卫**（与 owner 要件 3 的手写形态一致，非字节点清单）；④ 补集断言 + 结构不变量两侧齐全；⑤ 未定义聚合词清零。SC-001 / SC-002 / SC-004 / SC-005 是确定性或检出率断言，不与包含性混用（owner § 两类断言必须分开）。
- **`Written for non-technical stakeholders` 的判定依据**：本工件属 `.specify/shared/guidelines/user-facing-comprehension.md` 面向用户界面类的第 ⑦ 类，基准读者为「未在本会话打开过本仓、但具备本领域知识的人」。工件中的 `FR-NNN` / `SC-NNN` / `A-nn` / `C-nn` 与路径属该 owner 白名单的标识符与短形式；owner 与判据一律以路径引用而非复述。据此判通过。
- **三处「实现细节」判项（判通过，理由非循环）**：本特性的**主体就是框架自己的归档纪律与元技能流程**，因此 `skills/external/...` 路径、`shared/guidelines/...` owner 路径、`${SKILL_HOME}` / `${SKILL_WORKDIR}` 是用户指令逐字给定的**验收对象**，不是作者擅自选定的 HOW；规格未固定数据结构、算法或第三方依赖，且 § Assumptions A5 / A6 / § Constraints C8 明令本阶段不预设脚本、不新增门禁。据此 `No implementation details` 与 `No implementation details leak` 判通过。
- **已记录的缺口（判「Feature meets measurable outcomes」时如实记入，未掩盖）**：SC-001 / SC-002 / SC-005 的**分母尚未定量**——SC-002 的「成员表全量」要等 C1 谓词在 plan 定稿后才有确定集合，SC-001 的样本集与 SC-005 的样例题集同样由 owner 文档附录给出、此刻尚不存在。按 requirements-guidelines § Success Criteria Guidelines 的可测性要求，三条都是**可测但基数待定**，故本条判为带有已记录缺口的 pass：plan 阶段 MUST 把三个分母落成机械可得的集合，否则升级为缺口。闭环口径已写在各自 `**Path**:` 标注——SC-001～SC-004 为 `final`、SC-005 为 `supporting`，`path-marker` 判项据此通过。
- **待 clarify 落定的一项**：`Related Feature` 保持 `Need clarification`（§ Assumptions A8 / § Constraints C7）——`create-requirements` 不自行绑定。这不是规格缺陷；`/speckit.clarify` MUST 在 plan 之前完成绑定，并复核 C7 提到的既有 Feature 候选。
- **零澄清标记**：`marker-count` pass（0）。缺省裁决记在 § Assumptions（A1–A10）与 § Constraints（C1–C8），其中 A3（不新增第三个环境变量）、A6（探针不抽成脚本）、C1（元层谓词把 `coaching-skills` 判为不纳入强制检查）是三个真正做了选择的点，clarify 阶段可推翻，推翻须给出证据。
