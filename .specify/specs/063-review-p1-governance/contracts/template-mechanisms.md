# Contracts: Template & Mechanism Surface（F1/F2/F3/F5/F8）

**Spec**: `.specify/specs/063-review-p1-governance/requirements.md`
**Convention**: canonical clause form (`**C-N**` md-bold-closed) per `shared/definitions/contract-clause-definitions.md` § 3. Citation groups follow § 4 rule 2 (last parenthesized group carrying FR-/SC- ids in the block): each clause's citation group is the trailing `(FR-…, SC-…)` at the end of its block; FR ids in a clause's label or mid-body are mentions, not citations. Shared strings are cited as [[STR-NNN]] per the requirements' Shared Strings table.

## Template & documentation mechanisms

**C-1**: Owner 声明引用组定界字符集 `shared/definitions/contract-clause-definitions.md` § 4 rule 2 MUST gain a normative sentence declaring that an opening group delimiter is `(` or `（` and its matching closer is `)` or `）`, that nesting MUST match within one width, and that a cross-width pairing or an unpaired delimiter is a 畸形组 (malformed group) that the checker MUST report and MUST NOT silently count as a citation or as a mention. The declaration lives in the owner body — the extractor implementation MUST NOT be its only record. Verification: a contract test asserts the owner text names both widths and the same-width nesting rule (FR-001, SC-001)。

**C-2**: 抽取器实现声明字符集并自带畸形组报告 `scripts/python/clause_extract.py` `parentheticals()` MUST accept both widths with same-width one-level nesting (existing depth semantics preserved) and MUST report a malformed group (cross-width or unpaired) as its own outcome — never as citation, never as mention. Deterministic self-test samples MUST be added to `tests/contract/test_clause_forms.py` (the extractor's existing self-test home), covering at least: one full-width group, one same-width nested group, one cross-width malformed case, and a corpus where adding width support leaves an ASCII-only corpus's total unchanged (FR-002, SC-001)。

**C-3**: analyze 装载 checklist `skills/internal/analyze-artifacts/SKILL.md` § 2 artifact load table MUST gain a `checklists/*.md` row (load: item text, checked state, tags — `[Gap]` in particular); `templates/commands/analyze.md` § Delegation Inputs MUST name the checklist surface so the command face carries the duty (FR-005, SC-003)。

**C-4**: Gap 条目升格或显式处置 the analyze skill's detection passes MUST include one checklist pass: every unchecked item tagged `[Gap]` MUST be raised as a finding or carry an explicit disposition marker in the gate report. The marker form is defined by the skill and MUST be deterministically checkable (e.g. `CHK005 disposition: raised-as-finding H-01` / `CHK005 disposition: covered-by <artifact § anchor>`); free prose MUST NOT satisfy it. The report MUST make "unchecked + unraised + undispositioned" count observable as zero (FR-005, SC-003)。

**C-5**: 覆盖核算接入 analyze the analyze skill's workflow MUST run `scripts/python/account-clause-coverage.py --spec <spec-dir>` as a fixed step (read-only, no `--freeze`) and MUST surface its verdict in the report. `status: baseline-missing` MUST appear as a phase-visible problem with its remedy (run `/speckit.tasks` to freeze the baseline), never silently skipped; the run's `[fr-uncovered]` lane feeds the report's coverage summary. A feature without a contract set MUST record an explicit skip with its reason (FR-003, SC-002)。

**C-6**: tasks 冻结覆盖基线 `skills/internal/create-tasks/SKILL.md` § Runtime-evidence landing points MUST add the coverage baseline: for a feature with a contract set, `/speckit.tasks` freezes `coverage-baseline.txt` ([[STR-002]]) via `account-clause-coverage.py --freeze > <spec-dir>/coverage-baseline.txt` (the engine's own default path and `BASELINE_NAME`), at the same re-freeze timing as the other frozen baselines (first full-tree accounting per feature, not first all-green). A feature without a contract set MUST skip with an explicit stated reason — no empty fabricated baseline (FR-004, SC-002)。

**C-7**: 消费侧指向同一基线文件 the analyze consumption step (C-5) and the tasks freeze step (C-6) MUST name the same file path form (`<spec-dir>/coverage-baseline.txt`, the accountant's `--baseline` default); neither side restate the other's procedure (One Source of Truth: the accountant owns the format, C-5/C-6 own the wiring) (FR-003, FR-004, FR-030, SC-002)。

## Checklist accountability & closure（F2）

**C-8**: append-only recheck 形态 `skills/internal/create-checklist/SKILL.md` § 5 Generate MUST declare the recheck form: answers land in a NEW append-only recheck file per round (`checklists/recheck-<date>-<topic>.md`); every answered entry MUST quote the requirement line it answers; the original checklist MUST NOT be refreshed in place and its unchecked rows are preserved as history. This lands 061 REC-C5 at its named target (FR-006, SC-004)。

**C-9**: implement 豁免门第三分支 `skills/internal/implement-feature/SKILL.md` § Step 2 — Checklist exemption gate MUST gain a third branch: when a later stage resolved an item's subject and recorded the answer per C-8, that item is counted as answered — not incomplete, no waiver needed. The gate fires only for genuinely unresolved items, ending the every-feature-waiver steady state (FR-007, SC-004)。

**C-10**: waiver 四段格式 the same § Step 2 MUST require waivers to carry `Scope` / `Basis` / `Disposition` / `Closed`, listing the upstream artifact edits that closed the item; `Closed` MUST state what solved it. A waiver missing any part is non-compliant and MUST NOT be treated as closed evidence. This lands 061 REC-C6 at its named target (FR-008, SC-004)。

## Review loop persistence（F3）

**C-11**: review Handoffs 具名所有者与同提交登记 `templates/commands/review.md` § Handoffs "After" MUST replace the ownerless "Apply improvements to spec-kit templates/commands/scripts" with a named duty: every `REC-` ([[STR-003]]) id coined in the report is registered in `.specify/memory/register.md` in the same commit, using the register's existing pointer-row form (id → one-line meaning → report anchor → status). The register owns the row form; the command owns the obligation (FR-009, SC-005)。

**C-12**: 常驻指令层枚举 REC- `templates/instructions-template.md` § ID Register enumeration sentence MUST add the recommendation identifier (`REC-…`) alongside `D-…`/`OI-…`/`S…`/`T-…`/`F-…`/`B-…`; the live `.specify/instructions.md` MUST receive the change through the existing content-refresh owner — `/speckit.instructions` (manage-instructions Action 5), never by hand-editing the runtime copy and never by extending the additive-only `scripts/bash/generate-instructions.sh` out of its pinned C-2 contract (user adjudication 2026-10-20, recorded in requirements § Clarifications) (FR-010, SC-005)。

**C-13**: 全局建议的合法入口 `shared/workflow/feedback-step.md` § Scope guard (step 3) MUST keep the `scope: local` rule for wrap-up entries AND name the existing legal intake for a global review recommendation: the introspection step of `/speckit.feedback` (manage-feedback skill, Path A digest § A3 自省(Introspection)) — the path today's codebase provides (the review report's "Mode 5 自省" label is its historical name). No new intake store, tracking engine, or scoring system (宪法 IX/XIII) (FR-011, SC-005)。

**C-14**: REC 目标 repo-relative 优先 `templates/review-template.md` § 5 and Replacement Rule 3 MUST make the repo-relative path the PRIMARY form for a REC target (resolves on any checkout), with the absolute path as a parenthetical supplement; a target with no repo-relative form MUST be marked `external` with its reason. The instruction MUST NOT reintroduce 061's machine-local absolute-only form (FR-012, SC-005)。

**C-15**: /speckit.review 转换行（E2 裁决） `shared/workflow/feature-integration.md` § Status State Machine MUST gain `| /speckit.review | Implemented → Ready for Review | review.md committed AND every deferred item resolved or waived |` after the checklist row, and the checklist row MUST be annotated "applies only when the checklist runs after implement". The command list at the top of the document MUST include `/speckit.review`. "Each command owns exactly one transition" stays true: each command keeps exactly one row (FR-013, SC-006)。

## Environment-premise carriers & gate citations（F5/F8）

**C-16**: 载体清单开放 `skills/internal/create-tasks/SKILL.md` § Environment probe rules item 2 ("Single landing point") MUST replace the closed carrier enumeration "Per-phase prerequisites and `[~]` task notes" with one that also covers any assumption/decision or free-prose row, so the "MUST reference § Environment Prerequisites instead of restating verdicts" duty cannot be escaped by sitting in an unlisted carrier (FR-018, SC-009)。

**C-17**: 复述行带日期与指针 `templates/tasks-template.md` § Environment Prerequisites ACTION REQUIRED comment MUST gain: any row restating an environment verdict — in any carrier — MUST carry an ISO date stamp and a `(see § Environment Prerequisites)` pointer; both together, neither alone (Edge Cases) (FR-018, SC-009)。

**C-18**: red-first note 逐字引用 gate 行 the red-first evidence note's shape rule — owned by `skills/internal/create-tasks/SKILL.md` § Runtime-evidence landing points, where the note's content prescription lives — MUST require that when the note binds a claim to a gate, it quote the gate row verbatim (id + name + check command); a bare gate id alone MUST NOT be used, so a later renumbering produces a visible mismatch. Forward-applicable only; 062's note instance is out of scope (FR-029) (FR-025, SC-012)。*Owner-file note: FR-025 names implement-feature/SKILL.md "where it prescribes the note's shape" — the codebase shows the prescription lives in create-tasks (the landing-point owner); the duty lands there to keep one shape owner (One Source of Truth). Disclosed at plan and wrap-up.*

**C-19**: re-freeze timing 指向消费侧 `skills/internal/create-tasks/SKILL.md` § Re-freeze timing MUST point at the implement-side consumer step (the pre-flight duty contracted in C-29) instead of describing a duty it cannot itself execute; it retains the producer-side re-capture obligation (FR-024, SC-011)。

## Traceability

| Clause | Finding | FR | SC | Primary artifact |
|--------|---------|----|----|------------------|
| C-1 | F1 | FR-001 | SC-001 | shared/definitions/contract-clause-definitions.md |
| C-2 | F1 | FR-002 | SC-001 | scripts/python/clause_extract.py + tests/contract/test_clause_forms.py |
| C-3 | F2 | FR-005 | SC-003 | skills/internal/analyze-artifacts/SKILL.md + templates/commands/analyze.md |
| C-4 | F2 | FR-005 | SC-003 | skills/internal/analyze-artifacts/SKILL.md |
| C-5 | F1 | FR-003 | SC-002 | skills/internal/analyze-artifacts/SKILL.md |
| C-6 | F1 | FR-004 | SC-002 | skills/internal/create-tasks/SKILL.md |
| C-7 | F1 | FR-003/FR-004/FR-030 | SC-002 | both sides' path form |
| C-8 | F2 | FR-006 | SC-004 | skills/internal/create-checklist/SKILL.md |
| C-9 | F2 | FR-007 | SC-004 | skills/internal/implement-feature/SKILL.md |
| C-10 | F2 | FR-008 | SC-004 | skills/internal/implement-feature/SKILL.md |
| C-11 | F3 | FR-009 | SC-005 | templates/commands/review.md |
| C-12 | F3 | FR-010 | SC-005 | templates/instructions-template.md |
| C-13 | F3 | FR-011 | SC-005 | shared/workflow/feedback-step.md |
| C-14 | F3 | FR-012 | SC-005 | templates/review-template.md |
| C-15 | F3/E2 | FR-013 | SC-006 | shared/workflow/feature-integration.md |
| C-16 | F5 | FR-018 | SC-009 | skills/internal/create-tasks/SKILL.md |
| C-17 | F5 | FR-018 | SC-009 | templates/tasks-template.md |
| C-18 | F8 | FR-025 | SC-012 | skills/internal/create-tasks/SKILL.md |
| C-19 | F7 | FR-024 | SC-011 | skills/internal/create-tasks/SKILL.md |
