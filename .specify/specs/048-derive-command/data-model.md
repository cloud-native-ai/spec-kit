# Data Model: Derivation Command(需求 048 / Feature 049)

**Requirement → Feature**: `048-derive-command` → Feature 049 Derivation Command
**Concept authority**: `shared/definitions/derivation-definitions.md` — 对本文件**只读**。四套记录 schema(§Source Record / §Move Record / §Step Record / §Element Record / §Open Questions)、四级溯源等级(§Provenance Grades)、链完整性规则(§Chain Integrity Rules)、自审集(§Self-Audit)、封闭禁用集(§Banned Justifications)、降级规则(§Capability Degradation)、机械/语义边界(§Script / Prompt Boundary)全部由锚拥有。**本文件不复列任何字段语义表或规则表**;冲突时锚赢,本文件是缺陷。
**本文件拥有的部分**:持久化形态与列序(引擎解析契约)、生命周期(含算子持久 `status` 的二值机)与两个专节状态机(`access` / `confidence`)、身份发放作用域与比较语义、`init` 的 no-clobber / `--force` 语义、实体关系。
**Shared strings**:存储路径 [[STR-006]] · 引擎动作 [[STR-003]] · 退出码 [[STR-004]] · 降级理由 [[STR-007]] · 自审表头与检查项 ID 集 [[STR-002]] · 禁用字面量集 [[STR-001]] · 终止声明节 [[STR-008]]。

## 实体总览

| 实体 | 种类 | 身份与作用域 | 持久化位置 | 唯一写入者 |
|------|------|--------------|------------|------------|
| Source Record | 落地记录 | `S-<nnn>`,**每主题**发放 | `derive.md` §`## Sources` 一行 | 命令运行(落地阶段) |
| Reasoning Move | 累积记录 | `M-<nnn>`,**项目级**发放 | `moves.md` 一行(权威副本) | 引擎 `moves-add`(FR-012) |
| Derivation Step | 推导记录 | `D-<k>`,每文档 | `derive.md` §`## Derivation Chain` 一个块 | 命令运行(建链阶段) |
| Architecture Element | 交付记录 | `A-<k>`,每文档 | `derive.md` §`## Derived Architecture` 一个块 | 命令运行(组装阶段) |
| Open Question | 缺口记录 | `Q-<k>`,每文档 | `derive.md` §`## Open Questions` 一个块 | 命令运行(建链/组装阶段) |
| Move Library | 累积存储(聚合) | 单文件,项目级 | [[STR-006]] 的 `moves.md` | 引擎(独写) |
| Derivation Archive | 主题存储(聚合) | `<topic-slug>` 目录名即身份 | [[STR-006]] 的 `<topic-slug>/derive.md` | 命令运行 + 引擎 `init` 脚手架 |

五类记录(S / M / D / A / Q)的**字段含义**见锚对应节;以下每节只写持久化、生命周期、不变量与约束 FR。

## 持久化形态(引擎解析契约)

### `derive.md` 节序(冻结)

```text
# Derivation: <topic>          ← H1,含 topic 与运行元信息(日期、运行标识)
## Sources                     ← 表,列序见下
## Unverifiable Sources        ← 表:id | reason(每条 unverified 行必须在此出现,FR-005)
## Reasoning Moves Applied     ← 表:move_id | 本次处置(运行相对,非库的 `status` 列)| 投影注释(可选)
## Derivation Chain            ← `### D-<k>` 块序列,k 严格递增
## Derived Architecture        ← `### A-<k> <element name>` 块序列
## Open Questions              ← `### Q-<k>` 块序列
## Termination                 ← 机器可读终止声明,两行字面量见 [[STR-008]](FR-023,A12 的可校验形态)
## Self-Audit                  ← 固定表 [[STR-002]],检查项 A1…A14 全列
```

- **DM-1** 节序(八节)由 `init` 脚手架一次性生成,引擎按**标题字面量 + 出现次序**解析;新增节 MUST 追加在 `## Self-Audit` 之后,插入中间即破坏解析(本文件的裁定,锚未规定节序)。
- **DM-2** 表列序冻结:引擎按**位置**取值,不按列名匹配。列的**含义**归锚;此处的可测事实是「列数与位置不得增删换序」。`## Sources` 为 9 列(锚 §Source Record 表头原序),`moves.md` 为 7 列(锚 §Move Record 表头原序),`## Self-Audit` 为 4 列 [[STR-002]];`## Termination` 为两行 `- <label>: <value>` 形态,字面量归 [[STR-008]]。
- **DM-3** `### D-<k>` / `### A-<k>` / `### Q-<k>` 块内为 `- <label>: <value>` 行,label 拼写与次序按锚的 fenced shape 原样;id 列表以 `, ` 分隔;`contested-with` 仅在 `confidence: contested` 时出现(锚 §Step Record)。
- **DM-4** 只引用不复制(FR-015):`## Reasoning Moves Applied` MUST 以 `M-<nnn>` 引用算子;为可读性拼出形状时 MUST 带投影标记(锚 §Projection, Not Copy 的注释形式),且其 `inference_form` 与库中同 id 行不一致即校验失败(A9)。

## 1. Source Record(`S-<nnn>`)

- **身份与发放**:引擎在落地阶段按主题内出现序发放,主题内单调、永不复用(锚 §Source Record)。跨主题会重号,故**跨主题引用 MUST 用限定形式** `<topic-slug>.S-<nnn>`(锚 §Source Record / §Move Record;比较语义见 §身份语法 ID-3)。
- **存储**:`## Sources` 一行;`grade: unverified` 的行**同时**在 `## Unverifiable Sources` 出现一次(id + 理由),不是第二份记录而是同一身份的第二处列示(FR-005)。
- **生命周期**:即 `access` 状态机(§状态机 A);`grade` 与 `access` 正交 —— 存档救回只改善 `access`,**永不**上调 `grade`(FR-006)。
- **不变量**:
  - **SR-1** 每条来源 MUST 走完 FR-001 的固定三级次序,每级结果落 `access` + `resolved_via`;禁止跳级或凭记忆断言(FR-001/FR-002)。
  - **SR-2** `verification` MUST 是具体证据引用,受最小长度 + 禁字面量双重引擎检查;裸断言被拒(FR-002,锚 §Source Record)。
  - **SR-3** `title_mismatch` MUST 由引擎按归一化字符串比较算出,agent 断言无效;为真时双标题都留痕,引用该源的步骤 MUST 引用 `resolved_title`(FR-003,A3)。
  - **SR-4** 同一 URL 的重复条目按来源身份去重为一行,**全部** `claimed_title` 变体留在该行的 `claimed_title` 单元格内、以转义分隔符 `\|` 连接(切分正则与「任一变体不一致即为真」的判定归 `contracts/derivation-model.md` C-30;Edge Cases 第 1 条、FR-008)。
  - **SR-5** 只有 `primary` / `authoritative-secondary` 可出现在 `premises`;`community` / `unverified` 只能出现在 `leads`(FR-004,C1)。
  - **SR-6** 宿主无线上能力时:全部行 `grade: unverified` + 理由 [[STR-007]],可锚定步骤数 0,运行在建链前停止且不产出架构(FR-007,SC-005,锚 §Capability Degradation)。
  - **SR-7** `access` 与 `grade` 的两处强制耦合(FR-001/FR-004,锚 §Dead-Link Protocol 第 1、4 步):`unknown`(探活未能运行)MUST 落 `grade: unverified` —— 未探到的 URL 不是死亡证据,把它记成 `dead` 或记成任何可锚定等级都是编造;`paywalled` 的等级按**公开摘要**判定(摘要足以支撑归属判断),但摘要 MUST NOT 支撑任何需要完整论证的算子抽取(该判断是语义的,归 agent,见 `contracts/derivation-model.md` C-50)。
- **约束 FR**:FR-001..FR-008;度量 SC-001 / SC-002 / SC-005。

## 2. Reasoning Move(`M-<nnn>`)

- **身份与发放**:引擎 `moves-add` 项目级发放,`next = max(既有 id) + 1`,永不复用、永不重编号,且 `M-` 是**唯一由引擎发放**的身份族(FR-014,`contracts/derive-engine.md` C-26/C-27)。US2 AS3 即按 `max+1` 表述,不依赖「行数 == 最大编号」这一只在纯追加下成立的等式。
- **存储**:权威副本 = `moves.md` 一行。档案内**只有引用**(`## Reasoning Moves Applied`)与可选投影标记(DM-4)。
- **生命周期(持久 `status`,二值)**:

```text
(不存在) --moves-add 接受(处置 new)--> active
active   --后续运行命中同一归一化 inference_form--> active(处置 reused:不写库)
active   --后续运行命中并带来新锚点----> active(处置 reinforced:就地只增 anchor 列)
active   --后续运行判定该算子错了------> superseded(终态:永久保留、不得删行、不得再被引用,FR-016)
superseded --任何迁移动作--------------> 非法(需要该形状时由 moves-add 落新行)
```

  **持久状态 vs 运行相对处置(锚 §Move Record 已裁定)**:`status` 是库行的**持久**状态,只有 `active` / `superseded` 两值;`new` / `reused` / `reinforced` 描述的是**某次运行与算子的关系**,由 `moves-add` 与 `stats` 的输出报告(档案侧落在 `## Reasoning Moves Applied` 的处置列),MUST NOT 成为库列。把运行相对值写进持久行,库就会在第二次运行时自相矛盾(同一行既 `new` 又 `reused`);SC-003 的度量取自引擎输出的处置计数,与该列无关。
- **不变量**:
  - **MR-1** `inference_form` MUST 带命名槽位、换掉领域名词后仍成立(FR-010,锚 §Reasoning Move 的 slot test)。
  - **MR-2** `applies_when` MUST 同时含适用条件与过度使用护栏;缺护栏即判不完整(FR-011)。
  - **MR-3** `moves-add` 按归一化 `inference_form` 去重(近重复 = 槽位同构,判据归 `contracts/move-library.md` C-13/C-14);命中即 MUST 拒写并返回既有 `move_id`,使本次运行的**处置**转为 `reinforced`(FR-013)。
  - **MR-4** 库 MUST 只由引擎写入;手工编辑由 `validate` 检出行形 / id 单调性 / 重复 id / 锚点形式异常并报告,不静默接受(Edge Cases 第 6 条;A13 的判据见 FR-029 与 `contracts/derivation-model.md` C-40/C-41)。
  - **MR-5** 库 MUST 被 git 跟踪(算子不可重新推导);MUST NOT 进 `.gitignore`(FR-016,锚 §Move Library)。
  - **MR-6** 消费 MUST 经 `moves-list` 投影;整文件读入只在锚引用的小文件阈值内合法(阈值的唯一定义点是 `shared/guidelines/token-efficiency.md`)。
  - **MR-7** `anchor` MUST 以限定形式 `<topic-slug>.S-<nnn>` 存储(FR-014,锚 §Move Record),使项目级库里的锚点在任何后续主题中仍可解析;锚点 MUST **只增不减**,`reinforced` MUST 带来一个不在该行现有锚点中的新锚点(判据与退出码归 `contracts/move-library.md` C-19/C-20)。
- **约束 FR**:FR-009..FR-016;度量 SC-003。

## 3. Derivation Step(`D-<k>`)

- **身份与发放**:每文档发放,`k` 从 1 单调递增且**必须等于块在 `## Derivation Chain` 中的出现序**(FR-018 的 `j < k` 只在 id 与文序一致时可判定)。
- **存储**:`### D-<k>` 块,字段按 DM-3。
- **生命周期**:即 `confidence` 状态机(§状态机 B);步骤本身无独立状态字段,其存续由档案的一次运行整体决定。
- **不变量**:
  - **DS-1** 恰好一个 `move`(FR-017,C2):零个 = 无论证断言,两个 = 应拆两步。
  - **DS-2** `premises` 全部可解析:每个 `S-<k>` 存在且等级达标,每个 `D-<j>` 满足 `j < k`;前向引用与环被拒(FR-018,C1)。
  - **DS-3** `derivation` 与 `conclusion` MUST NOT 含 [[STR-001]] 任一字面量(FR-019,C3);封闭集扩充须同改锚与引擎。
  - **DS-4** `falsification` 非空洞:不为 `none` / `n/a` / `-`,且非 `conclusion` 的复述(引擎捕获同一与近似同一)(FR-020,C4)。
  - **DS-5** 冲突不静默择一:标 `contested` + 双向 `contested-with` + 判别性问题 + 残余入 `## Open Questions`(FR-021,C5)。
  - **DS-6** 结论洗白的退化形态被拒:`derivation` 为空或过短、`conclusion` 与来源标题相同(FR-025,C7)。
  - **DS-7** 步数受 `--max-steps` 约束(解析次序:显式 flag → 引擎默认常量,FR-024);触顶如实报告,不静默截断或继续(C6)。终止条件 (a)|(b) 与步数/预算 MUST 在 [[STR-008]] 节中机器可读地声明(FR-023);A12 据此分半 —— 计数对预算由引擎判定,(a) 与 (b) 之别由 agent 声明并背书,引擎只校验声明存在且取值合法。
- **约束 FR**:FR-017..FR-025;度量 SC-002 / SC-004。

## 4. Architecture Element(`A-<k>`)

- **身份与发放**:每文档发放,`k` 单调递增;身份只在本文档内有效(Plan 按 `A-<k>` 引用时需带主题限定,方向见锚 §Derivation vs Research vs Plan)。
- **存储**:`### A-<k> <element name>` 块,字段按 DM-3。
- **生命周期**:

```text
(不存在) --链走到头且该元素的全部 derived-from 均已建立--> 进入 ## Derived Architecture
预算触顶仍未溯源 ────────────────────────────────────────▶ 不得进入本节,留在 ## Open Questions(Edge Cases 第 9 条)
上游步骤事后降级 ──▶ confidence 按最小值重算(可下调,不得保留旧 derived)
任一引擎检查为红 ──▶ 整个文件被拒(FR-026 硬失败 / FR-031),本节不得作为已推导结果呈现
```

- **不变量**:
  - **AE-1** `derived-from` 非空且全部可解析;缺失 = **硬校验失败**,引擎拒绝整个文件而非仅告警(FR-026,A7)。
  - **AE-2** `confidence` = 其 `derived-from` 各步骤置信度的 **MIN**(FR-027,详见 §状态机 B);`derived` 元素建立在 `contested` 步骤上即被拒(A8)。
  - **AE-3** 被未决问题阻塞的元素 MUST 为 `provisional` 或 `contested`,且 `open-questions` 与对应 `Q-<k>` 的 `would-resolve` 双向可解析(FR-028,A10)。
- **约束 FR**:FR-026..FR-028、FR-031;度量 SC-002。

## 5. Open Question(`Q-<k>`)

- **身份与发放**:每文档发放,`k` 单调递增。
- **存储**:`### Q-<k>` 块,四字段按锚 §Open Questions 与 DM-3。
- **生命周期**:两个产生入口 —— 终止条件 (b)(下一步所需前提无已核实来源可提供,FR-023)与 `contested` 残余(FR-021)。**需求未定义消解状态**:一个 `Q-<k>` 被后续证据定案后,是删除、还是保留并标注定案步骤,无 FR 承载;本文件按「档案整体重跑时重写,不单独销账」建模(见 §未决建模项)。
- **不变量**:
  - **OQ-1** MUST 携 `why-undetermined` 与 `discriminator`;缺口 MUST NOT 被编造前提填补(FR-023,C6)。
  - **OQ-2** `would-resolve` 与被指元素的 `open-questions` MUST 双向解析(A10,FR-028)。
- **约束 FR**:FR-021、FR-023、FR-028;度量 SC-002(经 A10)。

## 6. Move Library(累积存储)

- **身份**:单文件即身份,无内部 id;位置 [[STR-006]] 的 `moves.md`,在 `.specify/derive/` **根**而非 `<topic-slug>/` 内(跨主题设计,理由归锚 §Move Library)。
- **生命周期**:`init` 缺失则创建骨架(表头 + 空表);存在则**永不重写**;此后只经 `moves-add` 追加行,或就地更新既有行的 `anchor`(只增不减)与 `status`(唯一合法迁移 `active → superseded`)。行永不删除(FR-016)。
- **不变量**:ML-1 = MR-3(去重拒写)· ML-2 = MR-4(引擎独写 + 手编检测)· ML-3 = MR-5(git 跟踪)· ML-4 = MR-6(投影消费)· **ML-5** 库文件 MUST NOT 出现在任何 `.gitignore` 分量中,且 `.specify/derive/` MUST NOT 被登记为镜像对(它是项目运行期数据、不随 wheel 分发;判据与理由归 `contracts/move-library.md` C-32/C-33/C-36)。
- **约束 FR**:FR-012..FR-016、FR-038;度量 SC-003。

## 7. Derivation Archive(主题存储)

- **身份**:`<topic-slug>` 目录名即身份(类比 `.specify/goal/<goal-slug>/`,Clarifications 裁定 4);slug 语法按 `shared/definitions/goal-definitions.md` 的 goal-slug 语法同构(首字符字母数字、其余 `[A-Za-z0-9_.-]`、MUST 是安全路径段)—— 这是**类比裁定**,锚未规定 slug 语法。
- **存储**:`<topic-slug>/derive.md`,一主题一份;git 跟踪;八节按 §持久化形态的冻结节序。
- **生命周期**:

```text
(不存在) --init--> scaffolded(八节空骨架,退出码 0)
scaffolded --落地--> grounded(## Sources / ## Unverifiable Sources 填齐)
grounded   --抽取--> moves-applied(## Reasoning Moves Applied 引用 M-nnn)
moves-applied --建链--> chained(## Derivation Chain + ## Open Questions)
chained    --组装--> assembled(## Derived Architecture)
assembled  --声明终止--> declared(## Termination:[[STR-008]] 两行,condition + steps/budget)
declared   --自审--> audited(## Self-Audit:A1–A10/A12/A13 引擎结果 + A11/A14 待背书)
audited --validate--> accepted(退出码 0)| rejected(退出码 4,errors[] 定位规则编号)
rejected --修复后重跑--> audited            accepted --同主题再运行--> grounded(增补式,见下)
```

  同主题第二次运行:算子库侧行为由 FR-013/FR-015/FR-016 明确(处置为增锚点或复用,仅 genuinely new 追加新行,库列 `status` 只可能由 `active` 迁向 `superseded`);**档案侧**是覆写还是就地增补,requirements 未规定(US2 的两次运行只约束算子库)。本文件按「重跑重写落地与链、算子库只追加」建模并列入 §未决建模项。`--force` 重脚手架对既有档案内容的处置**已裁定**:同目录备份为 `.bak` 后再脚手架(判据归 `contracts/derive-engine.md` C-12)。
- **不变量**:
  - **DA-1** 任一引擎检查为红的档案 MUST NOT 把 `## Derived Architecture` 作为已推导结果呈现(FR-031)。
  - **DA-2** `validate` MUST 在输出中返回 `semanticChecksPending`,其值恰为 A11 与 A14 [[STR-002]];二者 MUST 由 agent 显式背书,不得继承为通过(FR-029/FR-030)。
  - **DA-3** 降级运行时 `## Derived Architecture` 为空或不存在,且输出含降级说明(FR-007,SC-005)。
  - **DA-4** 档案 MUST NOT 引用 Plan;依赖方向单向(锚 §Derivation vs Research vs Plan)。
- **约束 FR**:FR-023/FR-024、FR-029..FR-031、FR-035..FR-038;度量 SC-002 / SC-005 / SC-006。

## 状态机 A:`access`(取值集归锚 §Source Record)

由 FR-001 的固定三级次序、其付费墙分支、以及「协议未能跑完」的容错分支(FR-033)产生;`resolved_via` 记录**是哪一级产生的**(取值集归锚,本文件不复列)。

```text
(未探测)
   │ ① 直连抓取
   ├── 可解析且正文可读 ────────────▶ live                 [resolved_via: direct]
   ├── 可解析但正文在付费墙后、仅摘要公开 ─▶ paywalled      [resolved_via: direct;grade 按公开摘要判定,SR-7]
   ├── 否定应答(404/410 等)
   │      │ ② 存档可用性查询
   │      ├── 有快照 ───────────────▶ wayback:<ts>          [resolved_via: wayback;grade 按快照内容判定,FR-006]
   │      └── 无快照
   │             │ ③ 归属搜索(标题 + 作者,一次)
   │             ├── 命中权威活副本 ─▶ 以新 URL 重入 ① ────▶ live | paywalled | wayback:<ts>   [resolved_via: websearch]
   │             └── 未命中 ────────▶ dead                  [三级**全部跑完且全部否定**;grade: unverified → ## Unverifiable Sources,FR-005]
   └── 协议**未能跑完**(无连通性 / 主机不可达 / 超时 / DNS 失败 / 传输缝异常)
          └────────────────────────▶ unknown               [grade MUST 为 unverified,SR-7;FR-033:probe-links 退出码 0,绝不阻塞,不编造;MUST NOT 记 dead]

任意态 ──(后续运行重探活,链接已腐烂)──▶ wayback:<ts> | dead | unknown   → 触发 §状态机 B 的降级级联
宿主完全无线上能力 ──▶ 全部行 unknown/未探测 → grade 一律 unverified + 理由 [[STR-007]](FR-007)
```

- **AC-1** 枚举的每个取值都有产生路径(锚 §Source Record 明言该性质):`live` / `wayback:<ts>` / `dead` 来自三级次序,`paywalled` 来自 ① 的付费墙分支,`unknown` 来自「协议未能跑完」。曾并列的 `not-found` 无产生路径(三级次序把「无快照 + 归属未命中」判为 `dead`),已从锚删除,本文件不再建模;`dead` 与 `unknown` 的界线即「协议跑完了没有」。
- **AC-2** `access` 只表达可达性,`grade` 只由**实际内容**判定;二者仅有的两处强制耦合见 SR-7(`unknown` MUST 落 `unverified`;`paywalled` 的等级按公开摘要判定,而摘要不足以支撑需要完整论证的算子抽取)。存档救回只改善 `access`,**永不**上调 `grade`(FR-006)。
- **AC-3** `unknown` MUST NOT 被当作 `live` 或 `dead` 的替身:它是「本次没测出来」,与「测出来是死的」在证据上不同。因此它强制 `grade: unverified`(FR-004),该来源进 `## Unverifiable Sources` 并附理由(FR-005),且不得出现在任何步骤的 `premises`(SR-5)。
- **AC-4** 存档快照不完整(截断/缺章节)时 `verification` MUST 写明不完整,不足以支撑的推理形状 MUST NOT 抽取(Edge Cases 第 3 条)。

## 状态机 B:`confidence`(三值 + 最小值传播)

偏序:`derived` > `provisional` > `contested`(MIN 取偏序下界)。适用于 `D-<k>` 与 `A-<k>` 两处,规则同源。

```text
【步骤级】
(建链) ── 前提全部为 primary/authoritative-secondary 且不消费 contested 步骤 ──▶ derived
(建链) ── 消费了任一 contested 步骤 ─────────────────────────────────────────▶ 至多 provisional(FR-022;标 derived 即被拒)
(建链) ── 两源算子推出冲突结论 ───────────────────────────────────────────────▶ contested(+ 双向 contested-with + 判别性问题 + 残余入 Open Questions,FR-021)
contested ── 判别性证据到位、冲突消解(需新一次运行的落地证据)──▶ provisional | derived
derived | provisional ── 上游来源事后降级 / 上游步骤转 contested ──▶ 按 MIN 重算(只可下调)

【元素级】
A.confidence = MIN{ D.confidence | D ∈ A.derived-from }        (FR-027,引擎每次 validate 重算)
A 携 open-questions ──▶ A.confidence ∈ {provisional, contested}  (FR-028)
A 的 MIN 为 contested 而 A 标 derived ──▶ A8 硬失败,拒绝整个文件
```

- **CF-1 最小值传播规则(完整陈述)**:元素的置信度是其全部 `derived-from` 步骤置信度的**最小值**,不是平均值、不是多数值、不是首项。因此一个 `contested` 步骤足以把任何含它的元素压到 `contested`,一个 `provisional` 步骤足以把 `derived` 元素压到 `provisional`。
- **CF-2 传递性**:下调沿链传递。某来源事后降级导致 `D-3` 由 `derived` 变 `provisional`,则所有把 `D-3` 列入 `premises` 的步骤与所有把该步骤列入 `derived-from` 的元素 MUST 一并重算下调,不得保留旧 `derived`(Edge Cases 第 8 条)。重算范围 = 该步骤的传递后继集(链是 DAG,FR-018 保证无环,故重算可终止)。
- **CF-3 只降不升(引擎侧)**:引擎只**重算**(结果可能下调),从不自行上调;上调只能来自一次带新落地证据的运行,且仍须满足 CF-1。
- **CF-4 不可洗白**:`contested` MUST NOT 作为 `derived` 置信度步骤的前提(FR-022);矛盾 MUST NOT 被折中或平均(FR-021,C5,锚 §Contradiction Handling)。
- **CF-5 `provisional` 的产生者**:需求强制的入口只有两个(FR-022 消费 contested、FR-028 被未决问题阻塞);agent 出于其他理由给 `provisional` 不受禁止,但也无 FR 约束 —— 记录为观察,不建模为状态转换。

## 身份语法与发放作用域

| 身份 | 语法 | 发放作用域 | 发放者 | 比较语义 |
|------|------|------------|--------|----------|
| `S-<nnn>` | 3 位零填充;跨主题引用用限定形式 `<topic-slug>.S-<nnn>` | **每主题**(单份 `derive.md` 内唯一) | agent 于落地阶段书写,引擎校验语法与单调 | 数值;限定形式先按 slug 分组再按数值比较 |
| `M-<nnn>` | 3 位零填充 | **项目级**(`moves.md` 内唯一) | **引擎 `moves-add`**(`next = max+1`)—— 唯一由引擎发放的身份族 | 数值 |
| `D-<k>` | 不填充 | 每文档 | agent 于建链阶段书写,引擎校验 | **数值**,`j < k`(FR-018);MUST NOT 字典序比较(`D-10` > `D-9`) |
| `A-<k>` | 不填充 | 每文档 | agent 于组装阶段书写,引擎校验 | 数值 |
| `Q-<k>` | 不填充 | 每文档 | agent 于建链/组装阶段书写,引擎校验 | 数值 |

  发放者一列的执行面收窄(锚 §Script / Prompt Boundary 把「identity grammar and monotonic ID issuance」列为引擎所有,而发放只在引擎独写的文件上有意义)归 `contracts/derive-engine.md` C-27,本文件不复述其理由。

- **ID-1** 永不复用、永不重编号:`M-` 由 FR-014 显式规定,`S-` 由锚 §Source Record 规定;`D-`/`A-`/`Q-` 在一次运行内单调,重跑重写时从头发放(档案是单份文档,不是累积台账)。
- **ID-2** 位数溢出:超过 999 时按自然位数扩展(`S-1000`),解析 MUST 用 `^([SMDAQ])-(\d+)$` 而非定长切片;限定形式在左侧多一个 slug 段,解析 MUST 先剥离 slug 再套用该式。
- **ID-3** 跨作用域引用**已闭合**(锚 §Source Record / §Move Record 裁定):`M-<nnn>` 项目级、`S-<nnn>` 每主题,故库中 `anchor` MUST 写限定形式 `<topic-slug>.S-<nnn>` —— 点号命名,沿用 `shared/definitions/goal-definitions.md` §Target Decomposition 的 `<goal-slug>.T-<nnn>` 先例,其共享身份语法容 `.` 不容 `#` / `/`。裸 `S-<nnn>` 入库不可解析,MUST 被拒(判据归 `contracts/move-library.md` C-6/C-20)。

## `init` 的 no-clobber 与 `--force` 语义

`init`([[STR-003]])的写入集只有两项,退出码按 [[STR-004]]:

| 目标 | 缺失时 | 已存在时 | `--force` 时 |
|------|--------|----------|--------------|
| `.specify/derive/moves.md` | 创建骨架(表头 + 空表) | **永不重写**(累积库,只由 `moves-add` 追加) | 同「已存在」—— `--force` MUST NOT 触及算子库(FR-016) |
| `.specify/derive/<topic-slug>/derive.md` | 按冻结节序脚手架空档案 | **拒绝覆盖**(no-clobber,Edge Cases 第 7 条),报告已存在路径并指向修改路径 | 重新脚手架 |

- **IN-1** 退出码:成功 0;缺 `--slug` / slug 非法(不合 `contracts/derive-engine.md` C-6 的身份语法,故非安全路径段)→ 2;slug 重名且未给 `--force` → 2([[STR-004]] 无「已存在」专用码,归入 input error;由引擎契约 C-12 钉死);给 `--force` → 0,`payload.clobbered` 为 `true` 且 `payload.backupPath` 记录同目录 `.bak`(处置见 IN-2);`--force` 与不存在的主题同给 → 0(等价于普通创建,`clobbered` 为 `false`)。
- **IN-2** `--force` 对既有档案内容的处置**已裁定**:同目录备份为 `derive.md.bak` 后再脚手架(可逆 → 自动执行 + 执行报告,FR-035;判据与 payload 字段归 `contracts/derive-engine.md` C-12)。备份保住既有链与 `## Open Questions`;`--force` MUST NOT 触及算子库。
- **IN-3** `init` MUST NOT 联网、MUST NOT 发放 `M-`(身份发放属 `moves-add`)、MUST NOT 写 `## Self-Audit` 的任何结果(脚手架阶段全为待判)。

## 关系

```text
Derivation Archive 1 ── * Source Record          (## Sources;unverified 子集另列于 ## Unverifiable Sources)
Source Record 1 ── * Reasoning Move              (anchor,限定形式 `<topic-slug>.S-<nnn>`,跨主题可解析,ID-3)
Move Library 1 ── * Reasoning Move               (权威副本;档案只持引用)
Derivation Archive 1 ── * Derivation Step        (## Derivation Chain;步骤序 = DAG 拓扑序)
Source Record 1 ── * Derivation Step             (premises,仅 primary/authoritative-secondary;leads 另计)
Derivation Step 1 ── 1 Reasoning Move            (恰好一个,FR-017)
Derivation Step * ── * Derivation Step           (premises 引更早的 D;contested-with 双向)
Derivation Step 1 ── * Architecture Element      (derived-from,≥1 且全解析,FR-026)
Architecture Element * ── * Open Question        (open-questions ↔ would-resolve,双向,FR-028)
Derivation Archive 1 ── 1 Self-Audit 表          ([[STR-002]];A11/A14 待 agent 背书)
Plan ──▶ Architecture Element                    (单向:Plan MAY 按身份引用 A-k;档案 MUST NOT 引 Plan)
```

## 本文件记录的未决建模项(报告,不自行裁定)

1. **`Q-<k>` 无消解状态**(§5):一个未决问题被后续证据定案后,是删除、还是保留并标注定案步骤,无 FR 承载;本文件按「档案整体重跑时重写,不单独销账」建模,须由 requirements 侧裁定。
2. **同主题重跑对 `derive.md` 是覆写还是就地增补**(§7):US2 的两次运行只约束算子库侧,档案侧语义无 FR 承载;本文件按「重跑重写落地与链、算子库只追加」建模。

**本轮已闭合**(锚修正 + 设计裁定后不再未决,列出以免被当作遗留):枚举可达性与 `paywalled` / `unknown` 的判定入口(§状态机 A、SR-7)· `unknown` → `grade: unverified` 的强制耦合(FR-004/SR-7)· `anchor` 的跨作用域限定形式(ID-3)· A13 的可判定证据面(FR-029 与 `contracts/derivation-model.md` C-40/C-41)· 算子库 `status` 的持久/运行相对双语义(§2)· `--force` 的内容处置(IN-2)。
