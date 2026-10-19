# Contract: 中型特性快车道（fast-lane）

**Feature**: 063 → Feature 058（演化）
**FR 覆盖**: FR-001…FR-010
**载体**: `skills/external/sdd-loop-driver/SKILL.md`、`references/efficiency-model.md`、`references/dispatch-recipes.md`、`references/stage-prompts.md`、`scripts/admission-check.py`、`docs/reference/skills/sdd-loop-driver.md`

- **FL-01（显式启用）**: 快车道 MUST 仅在 U0 入口声明携带字面量 [[STR-006]] 时启用；该字面量 MUST 原文写入该线状态脊。无人值守运行 MUST NOT 接受任何其他启用形式；交互式用户在场时，驱动 MAY 在准入判据实测后提议一次并记录原文采纳，MUST NOT 因等待回答而阻塞运行。缺失字面量 → 完整链；自然语言声明本身不构成启用（FR-002）。
- **FL-02（裁决时点）**: 准入裁决 MUST 在 `tasks.md` 已产出、`checklist` 派发之前执行，MUST 以制品实测值判定，MUST NOT 以规模印象或历史运行推断（FR-003）。
- **FL-03（七项判据，全部机械判定）**: 准入 MUST 全部满足下列判据；任一项无法判定 MUST 判 `full-chain` 并记录原因。判据 MUST 由 `admission-check.py` 以可复算的制品证据判定，MUST NOT 使用主观自证或规模印象：
  - (a) `requirements.md` 的 **FR 定义行数**与 `tasks.md` 的任务行数落在 FR-003 冻结的中型区间内；端点含入。计数语法 owner 是 `requirements.md` FR-003(a)（FR 定义行 `^- **FR-[0-9]{3}**:`；任务行 `^- \[[ xX]\] T[0-9]{3}`；SC 行、说明行与分组标题不计入），本条款只引用、不改写；区间数值的 owner 同为 FR-003，脚本常量是运行时 owner，二者由契约测试钉住。
  - (b) 特性未修改 `.specify/memory/constitution.md`（`git diff --name-only <base>..HEAD` 为零）。
  - (c) 不新增可执行引擎、CLI 命令/模板、技能、外部依赖、网络服务或模型 API：机械扫描改动路径（引擎类前缀、依赖清单）与改动内容（网络/模型 API 调用痕迹）；采用保守超集，改动既有引擎类路径同样拒绝。
  - (d) 不涉及安全/隐私敏感面：认证授权、凭据/密钥、数据删除/迁移、发布/外传、确认门判据；路径或内容扫描命中即拒绝。
  - (e) 单线单分支且无并发线触碰同一交付路径：`--lines-manifest` 必须恰有一行本线记录，其分支等于当前特性分支；多线或缺失清单 → 拒绝。清单是 U0 拓扑声明的导出视图，属可复核制品证据。行语法的唯一 owner 是 `data-model.md` E1 §「lines.manifest 行语法」；本条款只要求单线记录与分支匹配，不复述语法。
  - (f) `clarify` 已完成、活动 `[NEEDS CLARIFICATION:` 标记为零、Related Feature 绑定已解析（注册表行与详情文件存在）；`clarify` 完成状态由 `## Clarifications` 的 Session 记录或状态脊的 clarify 证据提供。
  - (g) 需求阶段自产质量清单 `checklists/requirements.md` 存在且全部勾选通过（至少一项、零未勾选）。
  - FR-003(a) 的区间调整 MUST 走显式范围修订并同步 SC-002 夹具。
- **FL-04（准入记录）**: 准入记录 MUST 在 `checklist` 派发前写入状态脊，字段至少包含：`decision`、`entry_evidence`、七项判据逐条 `{id, verdict: pass|fail, evidence}`、实测 `fr_count`/`task_count`、`decided_at`；跳过 MUST 使用 [[STR-003]] 标记（FR-004）。记录 schema 的字段面以 `data-model.md` E1 为准。
- **FL-05（下游发布与收口）**: 快车道裁决 MUST 随下游阶段提示词发布（至少 `implement` 与 `review`），使阶段不把缺失的 `checklist` 产物当作缺失的必需门；收尾汇总 MUST 携带 `checklist=skipped(fast-lane)` 或等价可见标记（FR-005，[[STR-003]]）。
- **FL-06（失败回退）**: 录取后任一判据失效，或后续阶段发现新事实使判据不再成立（新增引擎/模式/安全面、任务数越界等）时，驱动 MUST 回退完整链、在适用位置补派 `checklist`、记录回退触发与证据；回退 MUST NOT 静默（FR-006）。若回退发生在 `analyze` 已通过之后，补派 `checklist` 后 MUST 重过 `analyze` 一次再继续（保持完整链顺序与有界回环语义）。
- **FL-07（analyze/review 不削弱）**: 快车道 MUST NOT 改变 `analyze` 的 CRITICAL/HIGH 归零或已处置判据、至多一轮有界回环，也 MUST NOT 改变 `review` 的行为、证据义务与发现分级（FR-007/FR-008）。
- **FL-08（确定性准入脚本）**: `scripts/admission-check.py` MUST 以退出码表达裁决（0=可录取 / 1=拒绝 / 2=输入或解析错误），并输出逐条判据的 JSON 记录供状态脊引用。输入 MUST 至少包含 `--project --base-ref --requirements --tasks --checklists --entry-evidence --lines-manifest --expected-branch`；脚本 MUST 自包含（仅 Python 标准库），MUST NOT 读取框架 `.specify/scripts/` 运行时；阈值常量 MUST 由契约测试钉住（FR-009）。
- **FL-09（定义落点与契约钉住）**: 快车道的判据、记录形态与回退规则 MUST 落在 `references/efficiency-model.md`（技能面单一 owner），并由 `tests/contract/test_sdd_loop_driver_efficiency.py` 钉住；任何运行 MUST NOT 在缺少准入记录时声称自己走了快车道（FR-009）。
- **FL-10（自应用排除）**: 063 自身的运行 MUST 使用完整阶段链，`checklist`/`analyze`/`review` 均必经，MUST NOT 产生本特性自身的快车道记录；该例外 MUST 在规格、plan 与收尾证据中可见（FR-010）。

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| FL-01 | FR-002 | `test_fl_01_opt_in_literal_pinned` |
| FL-02 | FR-003 | `test_fl_02_admission_point_and_sequence_policy`（解析配方决策表：快车道跳过 checklist、保留 analyze/review；完整链含 checklist） |
| FL-03 | FR-003, SC-002 | `test_fl_03_criteria_table_pinned`；单测 `test_admission_check.py`（FR-only 计数、边界、缺件、引擎/敏感路径、lines manifest） |
| FL-04 | FR-004 | `test_fl_04_admission_record_fields` |
| FL-05 | FR-005, SC-001 | `test_fl_05_downstream_publication` |
| FL-06 | FR-006 | `test_fl_06_reversion_procedure` |
| FL-07 | FR-007, FR-008 | `test_fl_07_analyze_review_unchanged` |
| FL-08 | FR-009 | `test_fl_08_admission_script_interface` |
| FL-09 | FR-009, SC-001 | `test_fl_09_definition_owned_and_pinned` |
| FL-10 | FR-010, SC-013 | `test_fl_10_self_application_exclusion` |
