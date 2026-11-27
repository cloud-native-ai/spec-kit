# Specification Quality Checklist: Context Management — 上下文的声明、组合与只读审计

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-11-27
**Feature**: [requirements.md](../requirements.md)
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: 本阶段尚无 plan/tasks；源能力设计集（ai-harness `.ah/specs/093-context-management/` 的 plan / data-model / contracts / quickstart / feature-ref）仅作移植上下文读取，不进入本仓产物。

**Note**: 本清单的记录项全部来自确定性 checker 与 gate 的真实运行输出，计数不手写。

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Stability / containment claims name a baseline referent and a derivable allowed-delta set (owner: `.specify/shared/guidelines/closed-set-claims.md`)
- [x] Every required outcome from the brief has at least one functional requirement (声明模型 FR-001…FR-004；单 owner 文档 FR-001/FR-005；只读审计引擎与确定性读数 FR-021/FR-022；矩阵与触发 FR-009/FR-014/FR-029；分发/init 接线 FR-023/FR-025；缺席诚实 FR-020；无第二存储 FR-011/FR-024)
- [x] Backward-incompatible changes are closed over migration/refusal behaviors (本特性纯加性：不改既有引擎语义、不迁移存储；声明层缺失或未知成员按 FR-018 退 `2` 拒绝，而非降级通过)
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- **Checker run（结构命题的权威读取；计数由该次运行派生）**: `python3 scripts/python/validate-requirements.py .specify/specs/110-context-management/requirements.md` → `status: ok`，`0 error(s), 0 warning(s)`，scanned **283 lines, 40 definition rows, 6 shared strings**；逐字输出在 `test-evidence/requirements-validator.txt`（一次通过，零修复迭代）。
- **Driver gate self-check**: `pre-analyze-check.py --spec-dir .specify/specs/110-context-management --stage requirements --repo .` → `decision=pass errors=0 advisories=14 waived=0`，summary `fr=29 sc=11`；逐字输出在 `test-evidence/pre-analyze-requirements.txt`（JSON 同目录）。
- **Decomposition gate**: `decomposition-check.py --mode plan --requirements .specify/specs/110-context-management/requirements.md` → `decision=proceed`，`fr_count=29`，`fr_ceiling=120`；逐字输出在 `test-evidence/decomposition-requirements.txt`（JSON 同目录）。
- **14 条 advisory 的性质（全部为 `missing-path`：尚未存在的交付物路径或产出树才有的常驻见证路径，非缺陷；requirements.md 9 条 + 本清单 5 条）**: `shared/definitions/context-management-definitions.md`（FR-001 的交付物）、`.specify/shared/definitions/context-management-definitions.md`（镜像交付物）、`.specify/scripts/python/context-audit.py`（安装形态交付物）、`tests/fixtures/context-management/`（fixture 交付物 ×2）、`.specify/state/`（`task-delta` 的常驻见证；本 worktree 未携带运行期 state，生产树由驱动写入——本特性要求其缺席读 `absent` 并带原因，见 FR-020）。交付物在 implement 后消失，见证路径按在场诚实读数。
- **Reader baseline**: 本特性是框架治理特性，声明读者为框架维护者与客户项目维护者；每个域术语要么在其 owner 按指针抵达（声明层、token 效率纪律、重锚定、记忆召回、super↔sub 协议、agent 渲染），要么在本规格委托的 owner 文档带双语定义位（[[STR-001]]…[[STR-006]]），见规格头部的 Readers / Reading scenario。
- **Containment claims**: SC-002 的 referent = 每个审计动作**前**对同一 fixture 树（含仓库树读数）计算的 SHA-256 内容哈希清单，允许增量集合为**空**（字节码缓存按名排除）；SC-008 的 referent = implement 入口提交上的全量失败名清单与同 fixture 的协议/召回/渲染输出，允许增量 = 本特性声明的文件扇出。两处均未以「其余不变」等未定义聚合承载验收。
- **Source-port adjudications（载于 Assumptions）**: 类别由层派生（A-4，承重，含反面度量与重开条件）；五形态 + 合法性矩阵（A-5，承重，含重开条件）；布局表/花名册唯一配对与四事实注册形态（A-6）；cap 只引用（A-7，cap owner = token 效率纪律 § 摘要优先）；在场词表一次定义（A-8，适配：源的缺席词 owner 在本仓不存在）；派发边映射（FR-017/A-15，适配：源的七组件包在本仓不存在）；ambient 段预算（A-10，实测余量约 790 B，`BUDGET:` MUST `within`，不提额不裁旧段）；存储登记 = 无（A-11）。
- **Scaffold deviation（披露）**: `create-new-requirements.sh` 会把当前本地分支 `110-context-management` 当作已用编号而派生 111 并新建分支；按 107/108 先例手工从 `.specify/templates/requirements-template.md` 脚手架到本目录，仅跳过其建分支步骤（A-16）。命令与偏差记录见 `test-evidence/requirements-stage-2026-11-27.md`。
- **Measured baselines（2026-11-27，本工作树；供 plan 阶段引用）**: `.specify/instructions.md` = 40,170 B；生成器预算常量 `INSTRUCTIONS_BUDGET_BYTES` = 40,960 B；余量约 790 B。镜像对六组（含 `shared → .specify/shared`、`scripts → .specify/scripts`、`templates → .specify/templates`）。仓内检索 `Tier G` / `Tier T` / `7-component` 零命中、`project-context-render.py` / `project_facts.py` 不存在、四撤销词无框架 owner —— 均作为缺失传感器记入 A-3/A-8/A-15，不伪造路径。
- **Workspace guard**: 快照 `test-evidence/workspace-requirements.json` 于撰写前记录并自检 `clean`；阶段收尾复核见 `test-evidence/workspace-requirements-check.txt`。
- **No failing items; zero validator repair iterations consumed.**