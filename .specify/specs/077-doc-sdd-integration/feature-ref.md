# Feature Reference: 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）

**Feature ID**: 077 | **Feature Name**: 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）
**Requirement**: `.specify/specs/077-doc-sdd-integration/requirements.md`（2026-10-30 立项并绑定；本次为首次实现规划）
**Status at plan time**: 077 = `Draft` → 本 plan 推进到 `Planned`（`Implemented` 由 `/speckit.implement` 拥有，本阶段 MUST NOT 落该状态）

## 绑定关系

- 绑定结论与 reuse-first 复核见 `requirements.md` § Related Feature；本 plan 不新建、不合并、不废弃任何 Feature。
- 077 是**新建 Feature 的承接边**，不是 069 的新切片：一条 spec 目录只绑一个 Feature，Feature 可拥有多条线
  （069 拥有 `069-` / `069a-` / `069b-` 三条）。承接关系记在本文件与 `features/077.md`，**不**回写 069 的详情文件。
- 069 与 069a / 069b 均保持 `Implemented`，其正文与切片规格零改动；本特性只在两份 owner 文档
  （`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`）做**类条件追加**。
- Feature 集成动作两条：索引行状态推进（`Draft` → `Planned`）+ 详情文件记录本 plan 的关键变更。
- **对既有契约测试的连带义务**：`tests/contract/test_expression_gate_wiring.py` 的闭合集断言把「除 docs/humanize
  外的模板与技能都零命中」钉死，七模板接线必然使其转红（mutation 实证见 `test-evidence/plan-a6-mutation-probe.txt`）。
  修订方式是把七模板并入已接线名册，分母断言不变（`contracts/stage-wiring.md` C-013）。

## FR → 设计映射

| FR | 设计落点 | 契约 |
|----|----------|------|
| FR-001 声明行文法、位置与两个形态码（MUST 只约束新增声明线） | `templates/requirements-template.md` 头部字段；`flow-class-check.py` 的 `spec:` 键解析与四码 | C-001…C-006（decl） |
| FR-002 声明单一、索引与详情不存取值 | requirements 模板注释与契约禁令；`flow_class` 不加索引列 | C-007（decl） |
| FR-003 `spec:` 键族、九字段同形记录、三段退出码、owner 先于键文法 | `scripts/python/flow-class-check.py` 的键族与 `action_lookup` 分支 | C-001…C-010（res） |
| FR-004 未声明按默认 + 默认标记（存量缺省 vs 机制降级可区分） | 记录 `source: default` + `marker` + `error.label`；互斥约束 | C-004 / C-005（res）、C-008（decl） |
| FR-005 取值越界阻断、点名文件行号取值 | 退出码 1 + stderr 形态 + `flow_class: null` | C-007 / C-008（res）、C-009 / C-010（decl） |
| FR-006 读取时点（含 requirements 特例、re-baseline） | 七模板子节的时点句；re-baseline 记阶段记录 | C-005（wire）、C-011 / C-012（decl） |
| FR-007 声明单位 = 特性线、不跨线复用 | `spec:` 键的 basename 语义；禁 `feature:<ID>` | C-002（res）、C-011（res）、C-013（decl） |
| FR-008 七模板各一次读取、零副本 | `templates/commands/*.md` 的接线子节 | C-001…C-006（wire） |
| FR-009 `owner-unavailable` 与保持既有门禁集 | 退出码 2 的三类输入（含调用方可观察的「无法执行引擎」）、降级句与载荷 `error` 位 | C-012（res）、C-008（wire）、C-001（drv） |
| FR-010 表达类 blocking 真阻断、代码型算子按产物补回 | 子节分支句 + 门禁 owner 的阶段行 | C-004 / C-010（wire） |
| FR-011 执行类零行为变化（含两处登记豁免） | 剥离守卫（与基线提交逐字相同）+ 引擎缺席不新增失败 | C-007 / C-008（wire） |
| FR-012 切换只由类别驱动、无白名单 | 子节文本卫生（禁赋值形、禁 `G-` id、禁特性号/路径） | C-003 / C-009（wire） |
| FR-013 `## Document Structure` 四子节 + `--action structure` + plan 模板骨架产出 | `doc-consistency-check.py` 新动作 + 列名常量 + `templates/plan-template.md` | C-001…C-010（doc） |
| FR-014 章节两向比对两个码 + 四个语法码 + 落文输入（既有 `--path`） | 结构动作的章节族判定 | C-011…C-013（doc） |
| FR-015 证据清单覆盖与四码复用 | 证据面复用既有语法与码 | C-004 / C-014（doc） |
| FR-016 事实唯一 owner 三码 + 副本下限 | owner 面 + 既有 `duplicate` 下限 | C-015 / C-016（doc） |
| FR-017 implement 四面（CLI 输出面）+ 结构子步 + `verification.md` | 四面输出文件即 SC 证据源；结构绿而内容红的实例 | C-017…C-019（doc） |
| FR-018 派发载荷四元组、每次派发前解析 | `references/stage-prompts.md` 第①段 + 驱动流程 | C-001…C-003（drv） |
| FR-019 U4 四项增补（全 blocking；(a) 取算子表分母、(b) 存在非空、(c) `error` 分支） | `references/stage-prompts.md` § Independent Verification | C-004 / C-005（drv） |
| FR-020 两槽位换内容、`rc` 聚合、`not-applicable` 单列、审计不变 | `references/efficiency-model.md` §2 的类别分支 + 状态脊行字段 | C-006…C-008（drv）、`data-model.md` E8 |
| FR-021 驱动其他行为不变、analyze/review 100% | 边界声明（C-009 / C-010） | C-009 / C-010（drv） |
| FR-022 零新增命令 / 运行时 / 依赖 / 阻断式确认门（计数可判定） | `contracts/invariants-and-distribution.md` + T021 的扫描器运行 | C-001…C-003（inv） |
| FR-023 接线面封闭（含 `templates/plan-template.md`）+ 两份 owner 只做类条件追加 | 接线面清单 + 闭合集名册修订 | C-012 / C-013（wire）、C-003 / C-009（inv） |
| FR-024 编辑面 = 框架源、副本再生成、未刷新项目不变 | 镜像与命令副本判据 | C-011（wire）、C-004…C-006（inv） |
| FR-025 不削弱 069、不回退其状态、承接边 | 边界声明 | C-007 / C-008（inv）、C-010 / C-011（drv） |

**覆盖核对**：25 条 FR 全部被至少一条契约条款引用；`account-clause-coverage.py` 的 FR 车道实测
`FR uncovered: 0`（原始输出见 `test-evidence/plan-account-clause-coverage.txt`）。

## SC → 验收来源映射

| SC | 验收来源 | 证据落点 |
|----|----------|----------|
| SC-001 声明解析三例 | S2 三夹具的退出码与记录字段 | `test-evidence/`（实现期全量捕获） |
| SC-002 执行类零回归 | 七个模板剥离守卫 + 引擎移走后重跑 | `test-evidence/` |
| SC-003 表达类算子覆盖 | 七阶段算子结果记录 + 两个负向用例 | `test-evidence/` |
| SC-004 结构门禁 | 五个结构夹具 + 两个落文夹具（含结构绿而内容红） | `test-evidence/` |
| SC-005 驱动门禁 | U4 判定记录 + 状态脊槽位 | 状态脊 + `test-evidence/` |
| SC-006 零新增机制 | 命令清单 / 依赖 / 进程两次采集差异 | `test-evidence/` |
| SC-007 分发等价 | `sync-mirrors` / `regen` 漂移检查 + 两态渲染 | `test-evidence/` |
| SC-008 阶段完整性 | 试点线的八阶段记录与 analyze/review 判定 | 状态脊 |

本表只登记「哪个 SC 由哪类证据判定」，不复述 SC 的判定阈值（阈值归 `requirements.md` § Measurable Outcomes）。
