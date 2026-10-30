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
- **Decomposition gate**: `decomposition-check.py --mode plan --requirements ...` → `decision=proceed`，`fr_count=27 ≤ fr_ceiling=30`；exit 0。输出存于 `test-evidence/decomposition-check.json`。
- **Pre-analyze gate (requirements stage)**: `pre-analyze-check.py --spec-dir ... --stage requirements --repo .` → `decision=pass errors=0 advisories=1 waived=0`；exit 0。输出存于 `test-evidence/pre-analyze-check.txt`。唯一 advisory 是 `skills/external/coaching-skills/SKILL.md` 尚不存在——这正是本次重命名的目标路径，实现前缺席属预期，**接受为已知 advisory**，不视为缺陷。
- **Requirements testable and unambiguous**: 每条 FR 都点名可判定面——解析退出码与候选坐标、产物小节、观测记录的字段与缺口标记、偏差条目的证据引用、升级清理的目录/链接状态、派生检查的退出码——而不是「更清晰」「更友好」这类形容词。
- **Containment claims**: SC-006 / SC-008 的零残留与零漂移判据以 A11 的封闭活接线面为参照（19 个需手改源文件 + 其派生面），允许差异集为空；FR-027 的 gate 计数相等以改动前后两次读数为参照；历史记录经 A9 明确排除在集合外，符合 `.specify/shared/guidelines/closed-set-claims.md`。
- **Non-technical wording**: US1–US4 与 Edge Cases 用操作语言书写；FR/SC 按本仓既有规格惯例点名既有 owner 与交付面（如 `flow-class-check.py`、`probe-utils.py`、`sync-mirrors.py`），未引入语言、框架、运行时或外部 API。
- **Pending**: `Related Feature: Need clarification` 保留至 `/speckit.clarify` 绑定；A4（旧触发词取舍）与 A5（宿主派发降级）是 clarify 可推翻的缺省裁决。
