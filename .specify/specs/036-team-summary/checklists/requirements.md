# Specification Quality Checklist: Team Summary 信息管理机制

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-08-04
**Feature**: [requirements.md](../requirements.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
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

## Validation Log

**Iteration 1 — 4 issues found and fixed:**

| # | Item | Issue | Fix |
|---|------|-------|-----|
| 1 | Requirements are testable and unambiguous | FR-012 said "四种模式各自声明的阶段边界" — circular; a tester could not determine the boundaries from the requirement itself. | FR-012 now enumerates all four boundaries explicitly (serial stage 交接 / parallel 交叉校验汇总 / iteration DECIDE 相 / continuous 第 N 个 cycle). |
| 2 | Requirements are testable and unambiguous | FR-013 required "为每种模式提供默认值" without any verifiable property of those defaults — the highest-cost failure mode (continuous defaulting to per-cycle charting) was unguarded. | FR-013 now requires documented per-pattern defaults **and** forbids a per-cycle default for continuous. |
| 3 | Success criteria are technology-agnostic | SC-001 embedded exit codes ("退出 0(非 3)") — a measurement mechanism, not an outcome. | SC-001 restated as outcome ("校验通过而非阻断补填"); exit-code semantics moved to SC-001 Source. |
| 4 | All functional requirements have clear acceptance criteria | FR-024 (`summarize-project` must remain unchanged) had no measurable outcome backing it. | SC-003 widened to a three-group byte-invariance check (事实源工件 / 被监控目标 / 技能自身文件); SC-003 Source updated accordingly. |

**Iteration 2 — all items pass.** No further issues found.

**Post-clarify re-validation (2026-08-04, after `/speckit.clarify` Session 2026-08-04)** — re-ran every item against the amended spec (Feature binding resolved to 027; FR-012/FR-013/FR-018/FR-020/FR-025 amended; FR-026…FR-029 added; SC-011 + SC-012 added; `Work Item Identity` added to Key Entities). All 16 items still pass. Checks: 29 FRs with contiguous IDs FR-001…FR-029, 12 SCs each with a Measurement Source, all 5 `[[STR-nnn]]` references resolving, no lingering placeholders. One cross-FR contradiction was caught and fixed during integration (FR-020's byte-invariance vs FR-026's requirement that `STATE.md` carry item IDs — FR-020 is now scoped to the summary step, with the Supervisor's normal cycle writes explicitly carved out).

**Scope-revision re-validation (2026-08-04, dual-index directive)** — the user re-scoped the feature after plan.md and tasks.md existed: summary output must also be emitted to `.specify/project/goal/<goal-slug>/`, with `.specify/teams/` indexed by team and `.specify/project/goal/` indexed by goal. Handled per the Scope Revision Protocol (amend upstream in place, regenerate downstream by hand, residual sweep, re-validate) rather than as a clarification. Three decisions resolved it: 1 goal : N teams (aggregation); explicit `goal_slug` in `team.md` frontmatter; goal side holds the sole complete summary while the team side keeps run info only.

Added: User Story 6, FR-030…FR-036, SC-013…SC-015 (+ sources), `[[STR-006]]`, four Key Entities (Goal Summary / Goal Identity / Team Attribution / Team Run Info), five edge cases, three assumptions. Amended for staleness: `[[STR-001]]` repointed from `.specify/teams/<slug>/summary/` to the goal directory; FR-017 / FR-019 / FR-020 / FR-025; SC-003 / SC-007 and their sources; the Overview boundary paragraph; and the team-rename edge case, which previously said the delivery directory moves with the team — no longer true now that the directory is keyed on goal.

All 16 items still pass. Checks: 36 FRs with contiguous IDs FR-001…FR-036, 15 SCs each with a measurement source, all 6 `[[STR-nnn]]` references resolving, zero residual references to the dropped `.specify/teams/<slug>/summary/` path.

## Notes

- **Feature binding resolved (was `Need clarification`)** — `/speckit.clarify` (Session 2026-08-04) bound this spec to **Feature 027 — Team Management**. Evidence: 027 owns the team domain (`/speckit.team`, `create-team` + `improve-team`, `.specify/teams/` persistence) and its own `## Future Evolution Suggestions` already predicted this item («Team run history/observability under `.specify/teams/`»). Not bound to 013 (Skills Command) because FR-024 forbids changing `summarize-project`. Registered in `.specify/memory/features.md` and `.specify/memory/features/027.md`.
- **Content Quality item 1, scope note**: the spec names framework artifacts (`team.md`, `STATE.md`, `run-log.jsonl`, `runs/`, delivery-directory paths). In this project the framework artifacts *are* the product surface, so these are domain nouns rather than implementation leakage — consistent with the convention in `035-token-efficiency`. No language, framework, or API choices appear.
- **Zero `[NEEDS CLARIFICATION]` markers by design**: the three genuinely ambiguous readings (「拓扑结构」vocabulary alignment; whether "项目" means the team itself or a monitored external target; per-run snapshot vs cumulative product) each had a defensible default and are recorded as first-class entries in `## Assumptions` instead of consuming clarification budget. `/speckit.clarify` can still overturn any of them.
- **Reserved-identifier disclosure**: team preset files already carry a top-level one-line `summary:` field. The spec therefore nests the new configuration under `config.summary` ([[STR-002]]) rather than introducing a colliding top-level `summary:` key; the collision and the alternate name are stated in `## Assumptions` for user override.
