# Feature Reference: 需求 048 → Feature 049(推导式架构生成 / Derivation Command)

**Requirement → Feature**: `048-derive-command` → Feature 049 Derivation Command(推导式架构生成)
**Concept authority**: `shared/definitions/derivation-definitions.md`(FR-036:推导模型的唯一真源;本文件只引用,不复述其 schema / 等级 / C1–C7 / A1–A14 / 禁用集)
**Identity note**: requirement key `048` ↔ Feature ID `049`(本仓偏移恒为 −2,同 045→047、046→048)

## 绑定裁定(2026-09-05,/speckit.clarify + 用户裁定)

判定为**新建 Feature 049** 而非绑定既有特性:「从权威源重放推理方法以推导架构」是一个新能力面 —— 它的对象是**主题**(跨特性、比任何单个特性长寿),它的产物是**推理形状**(带命名槽位、可跨领域重放),这两点都不落在任何既有 Feature 的权威范围内。逐一考虑并拒绝的候选:

| 候选 | 其能力面 | 拒绝理由 |
|------|----------|----------|
| 013 Skills Command | 技能生命周期管理编排(创建 / 优化 / 路由) | 只管技能这一制品的编排,不含任何技能的能力内容;与 046→048 的裁定同理 |
| 037 Docs Command | `docs/` 文档空间的结构收敛与生命周期治理 | 域限定在文档空间;推导档案落 `.specify/derive/`(新顶层根),既非 docs 内容也非其分类学对象 |
| 031 Glossary Mechanism / 040 Token Efficiency | 横向纪律(词汇锚定 / token 效率) | 纪律型 Feature,约束所有命令的做法,不拥有任何命令的能力;本特性**消费**它们(见交叉引用义务) |
| 041 Goal Registry | 项目级 Goal 一等概念归档 `.specify/goal/<goal-slug>/` | 提供的是**结构先例**(项目级一等概念 = 独立顶层根 + slug 目录 + 单份定义文件 + 引擎独写),不是能力归属;Goal 是「被度量的期望终态」,Derivation 是「被重放的推理」,两者互不引用 |
| 047 Framework Material Hygiene | `/speckit.sanitize` + 自带 stdlib 引擎 + 累积台账 | 提供的是**引擎先例**(命令自带 stdlib-only 多动作引擎、累积存储、稳定身份与合并语义),不是能力归属;卫生治理面向资料正确性,与推导无关 |
| `/speckit.research`(能力归属问题) | 特性级证据采集与决策理由 | 边界由概念锚 §Derivation vs Research vs Plan 一次性划清:research 产出结论层(决策 + 理由)、绑定单个特性;本命令产出方法层(推理模式)、绑定主题。依赖方向单向:Plan MAY 按身份引用 `A-<k>`,Derivation MUST NOT 引用 Plan |

结论:无既有 Feature 拥有该能力面 → 新 Feature;041 与 047 的角色是**先例供给方**,记录在交叉引用义务里而非归属裁定里。

## 同轮裁定(全部落入 requirements.md §Clarifications)

四项设计形态裁定 + 一项能力裁定 + 一项分发裁定,均可追溯到 FR:必须联网核实(FR-001..003/006/007/033)、走完整 SDD 特性流程(过程性,由本 spec 产物集与 `features/049.md` Status Tracking 承载)、产物落项目级推导档案([[STR-006]] / FR-038)、算子跨运行累积为项目级库(FR-012..016 / SC-003)、真实语料不随框架分发(FR-037)。逐项映射见 `checklists/requirements.md` §用户裁定可追溯性。

## US → FR → 设计工件映射

| 用户故事 | FR | 设计工件落点 |
|----------|----|--------------|
| US1 把 handed-in 清单落地为可核实的分级来源表 | FR-001..FR-008 | data-model §1(Source Record)+ §状态机 `access`(含付费墙分支与「协议未跑完 → `unknown`」分支);契约 derivation-model(来源表列序 / 等级门控 / `unknown` → `unverified` 耦合 / 降级分支)、derive-engine(`probe-links` 离线容错、`init` no-clobber);概念锚 §Source Grounding(等级、死链协议、双标题协议) |
| US2 提取思维算子并累积进项目级算子库 | FR-009..FR-016 | data-model §2(Reasoning Move:持久二值 `status` + 运行相对处置)+ §6(Move Library);契约 move-library(`moves-add` 独写 / 槽位同构去重拒绝 / 限定 `anchor` 形式 / `moves-list` 投影 / git 跟踪)、derive-engine(`moves-list`、`moves-add` 的 `intent` 与处置输出);概念锚 §Reasoning Move、§Projection, Not Copy |
| US3 在完整性规则下建链并组装可溯源架构 | FR-017..FR-028 | data-model §3(Derivation Step)/ §4(Architecture Element)/ §5(Open Question)+ §状态机 `confidence`(最小值传播);契约 derivation-model(C1–C7 / A4–A10 引用式钉死、`contested` 双向链、终止条件声明)、derive-engine(`validate` 退出码 4 与规则编号定位、`--max-steps` 预算);概念锚 §Derivation Chain、§Derived Architecture |
| US4 自审、执行报告与命令面接线 | FR-029..FR-035 | data-model §7(Derivation Archive:八节节序,含 `## Termination` [[STR-008]] + `## Self-Audit` 固定表 [[STR-002]]);契约 derive-engine(`validate` 的 `semanticChecksPending`、`stats`、退出码 [[STR-004]])、derivation-model(A11/A14 由 agent 背书;A12 计数归引擎、(a)/(b) 声明归 agent;A13 = 新发放算子必解析到库行);命令模板 `templates/commands/derive.md`(复杂命令节序 Feedback → Documentation → Handoffs)+ probe Object [[STR-005]] 登记进 `shared/definitions/probe-definitions.md` |
| 横向纪律(不属任何单个 US) | FR-036..FR-038 | 概念锚为唯一真源(FR-036,由 shipped-surface 守卫测试承接);`templates/` 与 `shared/` 客户中性 + 示例槽位化(FR-037);`.specify/derive/` 登记进 `shared/definitions/framework-map.md`(FR-038) |

## 对 Feature 049 的 key changes(登记进 `.specify/memory/features/049.md`)

1. **概念面**:新概念锚 `shared/definitions/derivation-definitions.md` ×2 镜像(`shared/` ↔ `.specify/shared/`),拥有四套记录 schema、四级溯源等级、C1–C7、A1–A14、封闭禁用论证集、能力降级规则与 Script/Prompt 边界;其余文档一律引用。
2. **命令面**:`templates/commands/derive.md`(复杂命令,携 `## Feedback` + `## Documentation`,节序固定)+ 四份工具副本经 `regen-command-copies.py` 再生成并携 AUTO-GENERATED 标记 + `docs/reference/commands/derive.md`。
3. **引擎面**:`scripts/python/derive-utils.py`(stdlib-only,六动作 [[STR-003]],退出码 [[STR-004]])×2 镜像(`scripts/python/` ↔ `.specify/scripts/python/`)+ Tool 记录 `.specify/memory/tools/derive-utils.md`。
4. **存储面**:新顶层根 `.specify/derive/` —— `moves.md`(项目级累积算子库,引擎独写,git 跟踪)+ `<topic-slug>/derive.md`(每主题一份推导档案);`shared/definitions/framework-map.md` 新增一行使其对布局真源可见。
5. **接线面**:probe Object `speckit-derive-wrapup`(internal 72→73,`--validate` 退出码 0,`--reconcile` 错误集仍为既有 2 条);复杂命令分类 18→19、docs-step 分类 15→16;门控扫描 total 保持 23(零新增阻塞门控,上限 23.25 无余量);glossary 新词条(词条名以概念锚 §Terminology Boundaries 的推导域行为准,不在本文件复列);全套件名字级新增失败 0(基线 50F)。

## 交叉引用义务

- **040 Token Efficiency Discipline(Program-First / Summary-First)**:确定性判定(身份发放、结构校验、去重、计数、字面量扫描、链接探活)全部下沉引擎;算子库经 `moves-list` **投影**消费而非整文件注入,小文件阈值的唯一定义点是 `shared/guidelines/token-efficiency.md`(概念锚 §Projection, Not Copy 已按引用挂载)。049.md 应指向 040,040 侧无需改动。
- **041 Goal Registry(项目级一等概念归档先例)**:结构同构 —— 独立顶层根 + slug 目录 + 单份定义文件 + 引擎独写 + git 跟踪;差异是 041 的定义文件为 authored、本特性的档案为 derived-from-sources 且携强制溯源链。`features/041.md` 可加一条指向 049 的先例复用注记(非阻塞)。
- **046 Confirmation Gate Governance(可逆动作自动执行 + 执行报告)**:本命令产物均为可逆写入(新文件 + 追加),按两级判据归**自动执行**桶 → 全程零阻塞门控 + 三要素执行报告(执行内容 / 变更工件 / 修改途径),FR-035 与 SC-006 的门控 total 不超基线由此而来。049.md 已指向 046。
- **047 Framework Material Hygiene(命令自带 stdlib 引擎先例)**:`sanitize-utils.py`(4 动作 + 累积台账 + 稳定身份合并)是 `derive-utils.py`(6 动作 + 累积算子库 + 单调身份发放)的直接先例;两者共享「引擎独写存储、语义判断留 agent」的边界。`.specify/derive/` 是否纳入 047 的资料根白名单**不在本特性范围内**,由 047 侧自行裁定。
- **037 Docs Command(docs-step 约定)**:复杂命令收尾的 docs-sync 评估步骤由 `shared/workflow/docs-step.md` 提供,本命令按既有约定接入(分类 15→16),不新建机制。
- **产物侧义务**:`features/049.md` 在 plan 落地时由 Draft → Planned 并补记本文件要点;`features.md` 索引行注记追加 plan 摘要(索引与表头计数**手工编辑**,`update-feature-index.sh` 为破坏性脚本,见 049.md Implementation Notes)。
