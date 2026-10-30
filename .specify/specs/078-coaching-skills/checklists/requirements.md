# Specification Quality Checklist: Coaching Skills（教练技能）

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-10-30
**Feature**: `.specify/specs/078-coaching-skills/requirements.md`

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
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- **Deterministic checker (authority for every count)**: `python3 scripts/python/validate-requirements.py .specify/specs/078-coaching-skills/requirements.md` → `status: ok`；`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id` 全 pass；`0 error(s), 0 warning(s)`；exit 0。逐字输出存于 `test-evidence/validate-requirements.txt`。本清单不手抄计数，计数以该文件为准。
- **Decomposition gate**: `decomposition-check.py --mode plan --requirements ...` → `decision=proceed`，`fr_count=29 ≤ fr_ceiling=30`；exit 0。输出存于 `test-evidence/decomposition-check.json`。
- **Pre-analyze gate (requirements stage, 2026-10-30 analyze 回环重跑)**: `pre-analyze-check.py --spec-dir ... --stage requirements --repo .` → `decision=pass errors=0 advisories=50 waived=0`；exit 0。输出存于 `test-evidence/pre-analyze-check.txt`。50 条 advisory 全部是同一类 `missing-path`：plan/tasks/contracts 指向的交付路径（`skills/external/coaching-skills/**`、`.specify/memory/coaching/`、`tests/contract/test_coaching_*`、`tests/fixtures/coaching/**` 等）尚未创建——实现前缺席属预期，**整体接受为已知 advisory**，不视为缺陷。（requirements 阶段早期只有 requirements.md 时该读数为 2，plan/tasks 落盘后审计面扩大至 13 个文件，读数随之变化。）
- **Requirements testable and unambiguous**: 每条 FR 都点名可判定面——解析退出码与候选坐标、产物小节、观测记录的字段与缺口标记、偏差条目的证据引用、升级清理的目录/链接状态、派生检查的退出码——而不是「更清晰」「更友好」这类形容词。
- **Containment claims**: SC-006 / SC-008 的零残留与零漂移判据以 **A10** 的封闭活接线面为参照（19 个需手改源文件 + 其派生面），允许差异集**恰为 `_OBSOLETE_SKILLS` 中保留旧名的那一行**（FR-020 要求其必须存在；除此之外空集）；SC-008 的门控判据与 **FR-027/A11** 同单位——`git diff <base> -- <A10 封闭面> | grep '^+'` 的新增行 0 命中 `scan-confirmation-gates.py` 的 `BLOCKING_PATTERNS`，改动前基线读数须入证据，不以改动前后总量相等作判据；历史记录经 **A9** 明确排除在集合外（A9 的边界是「本特性 `078-coaching-skills` 目录之外的既有记录」，本特性自身产物可正常改写），符合 `.specify/shared/guidelines/closed-set-claims.md`。
- **SC-006 计数集 (2026-10-30 analyze 回环)**: 计数集是 FR-018 的八个身份坐标、合计 8/8，坐标清单与「按坐标计数、[[STR-001]] 被 [[STR-003]] 包含不重复计」的规则均以 SC-006 为唯一出处，本清单不复述。
- **Non-technical wording**: US1–US4 与 Edge Cases 用操作语言书写；FR/SC 按本仓既有规格惯例点名既有 owner 与交付面（如 `flow-class-check.py`、`probe-utils.py`、`sync-mirrors.py`），未引入语言、框架、运行时或外部 API。
- **Clarify write-back (2026-10-30)**: 4 个问题已回答并写回（Feature 绑定 078 / `<work>` 第二位置参数与双上下文独立性 / 观测通道 / 运行目录与四文件）；覆盖率扫描由 2 个 fresh-context 只读子代理分域执行，24 条发现中 20 条经既有 owner 事实裁决就地修正。写回后三条确定性检查已重跑：checker `status: ok` 0 error，decomposition `fr_count=29`，pre-analyze `decision=pass errors=0`；本清单上方每条戳记均派生自该次重跑。
- **Analyze 回环修复 (2026-10-30, loop 1/1，requirements 侧)**: M-01 → FR-024/A9 的不改写边界改为「本特性 `078-coaching-skills` 目录之外的既有记录」，并声明本特性自身产物可正常改写；M-02 → SC-006 计数集扩为 FR-018 的八个身份坐标（8/8）；H-02 → SC-008 第三条改为 `git diff` 新增行 0 命中 `BLOCKING_PATTERNS`（与 FR-027/A11 同单位），基线读数存于 `test-evidence/gate-newline-baseline.txt`；C-01（requirements 侧）→ 本清单 Containment claims 的封闭面锚点由 A11 改为 A10、允许差异集改为恰为 `_OBSOLETE_SKILLS` 一行。修复未新增任何 FR/SC 编号；plan / contracts / tasks 侧的同源修复留给后续阶段。修复后三门已重跑：checker `status: ok` 0 error、decomposition `fr_count=29 ≤ 30`、pre-analyze `decision=pass errors=0`。测试预算：docs-only，`status=not-run-docs-only`。
- **Pending**: 无未决澄清；A10（封闭清单）与 A11（零新增门禁）是已裁定的缺省，后续阶段若发现不适配按 re-baseline 处置。
