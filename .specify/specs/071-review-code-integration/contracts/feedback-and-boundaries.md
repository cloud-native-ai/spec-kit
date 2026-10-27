# Contracts: Feedback channel, expression boundary, non-regression (C-55…C-64)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Owner**: this file owns what the composed run may and may not post to the feedback store, how the nested units record themselves, which predecessor invariants stay in force, and how the expression-class review face is protected. The feedback mechanism itself — red lines, store, engine, threshold protocol — is owned by `shared/workflow/feedback-step.md` and is cited here, never redefined.
**Pinned by**: `tests/contract/test_review_feedback_boundary.py`
**Measures**: SC-005, SC-007

**C-55**: The review command's closing step set stays exactly as it is — run determination, execution quantification, feedback record, threshold notice, token reflection, docs-sync evaluation. This feature adds no closing step, no side channel, and no second record type; the compiled closing face is not edited (FR-016).

**C-56**: A feedback entry records friction of the framework itself — a missing renderer, an ambiguous base, a receipt gap, an insufficient non-interactive path — and a code defect found by the code segment MUST NOT be posted as a feedback entry. The defect stays in [[STR-004]], where its severity, file, and line are meaningful (FR-017, SC-007).

**C-57**: The classification duty is written into two surfaces — the command template and the code-review skill text — so that posting a code defect as feedback is a detectable violation of a stated rule rather than a matter of taste. A sample built to make that mistake must be judged a violation by the contract test (FR-017, SC-007).

**C-58**: In the nested run the unit census is **three**, not two: the command unit `/speckit.review`, the delegated process-skill unit `skill:review-sdd-process`, and the delegated code-skill unit `skill:code-review`. Each unit completes its own closing record. The command MUST NOT suppress either skill's wrap-up, MUST NOT write a skill's run determination on its behalf, and MUST NOT back-fill one after the fact (FR-018).

**C-59**: The three records coexist because the entry key is `(unit_id, run_id)`: within one run the units differ in `unit_id`, so none dedups another and none has to be merged or dropped. This reuses the key the feedback engine already documents; no new key shape is introduced. The clause MUST NOT be read as "a nested run produces only two entries" — the command side adds its own entry and leaves both skills' entries intact (FR-018).

**C-60**: The predecessor invariants stay in force unchanged: a recommendation identifier is registered in the project register in the same commit that lands it, the introspection step remains the legal entry for a framework-wide recommendation, every entry stays `scope: local`, transmission stays zero-automatic, and the feedback target stays the framework rather than the feature (FR-020).

**C-61**: This feature adds no intake store, no second aggregation directory, no second id family for feedback, and no upload path. The existing local-scope store is the only destination (FR-020).

**C-62**: The expression-class review face still judges against the declared reader baseline and MUST NOT reuse the code-review object — compile results, test results, or coverage numbers. The code segment is an additional segment: for a feature with no code delta it is recorded as [[STR-001]] and the reader-baseline judgement is neither replaced nor short-circuited (FR-027, SC-005).

**C-63**: The receipt's coverage counts reviewed files — the share of the changed-file set that carries a verdict — never test coverage and never compile coverage. FR-027's prohibition targets the latter, which is the object the expression-class review face may not reuse; the receipt is required by FR-014 and is not the object that prohibition forbids. Two different questions carry the same word, so this clause keeps them apart: the receipt may not be cited as evidence for the reader-baseline judgement, and FR-027 may not be cited to forbid the receipt (FR-014, FR-027).

**C-64**: No existing contract assertion is deleted, weakened, or semantically drifted. Exactly one assertion change is authorized, and it is the only one: `tests/contract/test_review_p1_review_loop.py::test_c15_review_owns_the_ready_for_review_transition` is rewritten because C-47 removes the duplicated wording that pin quotes. The rewrite keeps its subject — the `/speckit.review` row exists and the command owns that transition — stops requiring the duplicated wording, adds an assertion that the row cites `templates/feature-details-template.md` § Canonical Status State Machine, and adds a negative assertion that the duplicated wording is gone; the net assertion count rises. Its rationale MUST be declared in the feature detail's `## Latest Review` review-record entry, so the exception is readable where the feature's reviews are recorded. The authorization is **non-precedential**: no other existing assertion may be deleted or weakened, and this clause MUST NOT be cited as a basis for one (FR-027).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-55 | FR-016 | — | command template |
| C-56 | FR-017 | SC-007 | command + skill |
| C-57 | FR-017 | SC-007 | command + skill + test |
| C-58 | FR-018 | — | command + two skills |
| C-59 | FR-018 | — | feedback engine contract |
| C-60 | FR-020 | — | command + registration duty |
| C-61 | FR-020 | — | scope sweep |
| C-62 | FR-027 | SC-005 | expression gate owner + test |
| C-63 | FR-014, FR-027 | — | receipt clause |
| C-64 | FR-027 | — | test suite + feature detail |

## Amendment log — remediation round 1 (2026-10-27)

Trigger: `test-evidence/analyze-report.md` (`GATE: CRITICAL=0 HIGH=6`) and `notes/remediation-round-1.md`. Clause ids are unchanged; no obligation was dropped.

| Clause | Change | Why (finding) |
|--------|--------|---------------|
| C-58 | the per-run unit census becomes three, with both delegated skills named | A-20 |
| C-59 | the coexistence argument covers three records, not two | A-20 |
| C-63 | the "coverage" disambiguation now runs both ways: FR-014 requires the receipt, FR-027 forbids the other object | A-17 |
| C-64 | the single authorized assertion change is named as non-precedential and carries a declaration duty in the feature detail | A-06 |
