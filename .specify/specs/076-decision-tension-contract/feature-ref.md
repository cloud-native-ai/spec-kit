# Feature Reference: 决策反题与反指标契约（Decision Tension Record）

**Feature ID**: 076 | **Feature Name**: 决策反题与反指标契约（Decision Tension Record）
**Requirement**: `.specify/specs/076-decision-tension-contract/requirements.md`（2026-10-29 立项并绑定；本次为首次实现规划）
**Status at plan time**: 076 = Draft → 本 plan 推进到 `Planned`（`Implemented` 由 `/speckit.implement` 拥有，本阶段 MUST NOT 落该状态）

## 绑定关系

- 绑定结论与候选核验见 `requirements.md` § Related Feature；本 plan 不新建、不合并、不废弃任何 Feature。
- 本特性**不**扩展任何既有 Feature 的能力面：A（DTR）是新 owner 与新通道，B（四元组）的 owner 文件
  此前未被任何 Feature 收编（requirements § Related Feature 已逐条核验六个候选）。
- 因此 Feature 集成动作只有两条：索引行状态推进 + 详情文件记录本 plan 的关键变更（见 `plan.md` § Feature Integration）。

## FR → 设计映射

| FR | 设计落点 | 契约 |
|----|----------|------|
| FR-001 规范 owner 与路径引用 | `shared/guidelines/decision-tension.md`（新建）；`data-model.md` E1 | C-1、C-8（owner） |
| FR-002 封闭六字段 + `tension_id` | owner § 记录形态；`data-model.md` E1 | C-2（owner） |
| FR-003 可采纳判据（封闭四条） | owner § 可采纳判据 | C-3（owner） |
| FR-004 拒绝形态（封闭清单） | owner § 拒绝形态；`data-model.md` E1 R5 | C-4（owner） |
| FR-005 承重门槛（四类触发） | owner § 承重门槛；`data-model.md` E4 | C-5（owner） |
| FR-006 复杂度门控 | owner § 门控；引用 `shared/guidelines/task-complexity-rubric.md` | C-6（owner） |
| FR-007 相邻 owner 边界 | owner § 边界（四个相邻机制，路径引用） | C-7（owner） |
| FR-008 模板章节与位置 | `templates/plan-template.md` 新增 `## Decision Tensions`（Constitution Check 直接后继） | C-1、C-2（anchor） |
| FR-009 只引用不复述 | 同上；契约测试四断言 | C-3（anchor） |
| FR-010 代价映射封闭形态 | owner § 代价映射；`scripts/python/validate-decision-tensions.py` 解析 | C-1…C-3（binding） |
| FR-011 analyze 三类缺陷 fail-closed | `detection-and-severity.md` § I 通道 | C-1、C-2（channel） |
| FR-012 严重度取既有传播面判据 | 同上；引用 `objective-analysis-gate.md` | C-3（channel） |
| FR-013 结构判定交程序 | 校验器 + 通道只消费 verdict | C-4（channel） |
| FR-014 通道落点 + 只增不改 | `detection-and-severity.md` + `SKILL.md` 计数行 | C-5（channel） |
| FR-015 ADR `tension_id` 引用位 | `docs/decisions/template.md` § Alternatives | C-1、C-2（adr） |
| FR-016 校验器契约与封闭六标签 | `scripts/python/validate-decision-tensions.py` | C-1…C-3（validator） |
| FR-017 逆样本在测试里 | `tests/contract/test_decision_tension_validator.py` | C-4（validator） |
| FR-018 零新增机制 | 全程；前后集合差判定 | C-1（scope） |
| FR-019 四元组取代一句话形态 | `shared/guidelines/critique-and-self-critique.md` 新增小节 | C-1（quartet） |
| FR-020 字段可判定语义 | 同上；`data-model.md` E5 | C-2（quartet） |
| FR-021 拒收规则与判定者 | `scripts/python/validate-falsification-quartet.py`；封闭六原因 | C-3（quartet） |
| FR-022 载体不变 | SI-4 载荷、SI-7 记录 | C-4（quartet） |
| FR-023 SI-3C 指针化 | `shared/workflow/self-improvement-workflow.md` § SI-3C | C-5（quartet） |
| FR-024 术语合规 | 三棵分发面；`requirements.md` A3 为别名清单 owner | C-2（scope） |
| FR-025 两顶帽子与镜像 | `plan.md` § Mirror Obligations（复用 FR-025 owner 表） | C-3（scope） |
| FR-026 既有闭合面不回退 | 两个 owner 文件的只增不改 + 条目计数 | C-4（scope） |

## SC → 观测方式

| SC | 观测 | 证据落点 |
|----|------|----------|
| SC-001 | 合规夹具一次 + 五个反向输入各一次的退出码与报告条目 | `test-evidence/` 的六次运行记录（实现期） |
| SC-002 | 四个夹具的 analyze 报告严重度列与计数 | 报告快照（实现期） |
| SC-003 | 同一 trivial 夹具前后两次 HIGH 计数与记录条数 | 两份报告快照（实现期） |
| SC-004 | 一个合规 + 六个不合格载荷的接收/拒收判决 | 校验器输出（实现期） |
| SC-005 | 命令清单 / 依赖清单 / 进程清单的前后集合差 | plan 期基线与实现后采集 |
| SC-006 | ADR 模板文本断言 + 记录到测量来源的解析结果 | 契约测试输出 |
| SC-007 | 三棵分发面的别名计数（改动前后各一次） | plan 期计数与实现后计数 |
| SC-008 | 两个 owner 文件与基线提交的逐字 diff + 契约测试断言计数 | 差异行枚举（实现期） |

## Plan 期已完成的证据（本轮）

| 项 | 结果 |
|----|------|
| 子句形态 | 8 份契约 / 34 条条款，全部 `md-bold-closed`（`test-evidence/clause-extract.txt`） |
| FR 车道 | 26 / 26 由条款引用组认领，uncovered 0（`test-evidence/account-clause-coverage.txt`） |
| 镜像基线 | 六对镜像全 `ok`，命令副本 `--check` 退出码 0（`test-evidence/sync-mirrors-check.txt`） |
| 术语基线 | 三棵分发面内部别名命中 0（plan 期测量，实现后复测） |
