# Contracts: Feedback channel, expression boundary, non-regression (C-55…C-64)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Owner**: this file owns what the composed run may and may not post to the feedback store, how the nested units record themselves, which predecessor invariants stay in force, and how the expression-class review face is protected. The feedback mechanism itself — red lines, store, engine, threshold protocol — is owned by `shared/workflow/feedback-step.md` and is cited here, never redefined.
**Pinned by**: `tests/contract/test_review_feedback_boundary.py`
**Measures**: SC-005, SC-007

**C-55**: The review command's closing step set stays exactly as it is — run determination, execution quantification, feedback record, threshold notice, token reflection, docs-sync evaluation. This feature adds no closing step, no side channel, and no second record type; the compiled closing face is not edited (FR-016).

**C-56**: A feedback entry records friction of the framework itself — a missing renderer, an ambiguous base, a receipt gap, an insufficient non-interactive path — and a code defect found by the code segment MUST NOT be posted as a feedback entry. The defect stays in [[STR-004]], where its severity, file, and line are meaningful (FR-017, SC-007).

**C-57**: The classification duty is written into two surfaces — the command template and the code-review skill text — so that posting a code defect as feedback is a detectable violation of a stated rule rather than a matter of taste. A sample built to make that mistake must be judged a violation by the contract test (FR-017, SC-007).

**C-58**: In the nested run the command unit and the skill unit each complete their own closing record. The command MUST NOT suppress the skill's wrap-up, and MUST NOT write the skill's run determination on its behalf (FR-018).

**C-59**: The two records coexist because the entry key is `(unit_id, run_id)`: within one run the two units differ in `unit_id`, so neither dedups the other and neither has to be merged or dropped. This reuses the key the feedback engine already documents; no new key shape is introduced (FR-018).

**C-60**: The predecessor invariants stay in force unchanged: a recommendation identifier is registered in the project register in the same commit that lands it, the introspection step remains the legal entry for a framework-wide recommendation, every entry stays `scope: local`, transmission stays zero-automatic, and the feedback target stays the framework rather than the feature (FR-020).

**C-61**: This feature adds no intake store, no second aggregation directory, no second id family for feedback, and no upload path. The existing local-scope store is the only destination (FR-020).

**C-62**: The expression-class review face still judges against the declared reader baseline and MUST NOT reuse the code-review object — compile results, test results, or coverage numbers. The code segment is an additional segment: for a feature with no code delta it is recorded as [[STR-001]] and the reader-baseline judgement is neither replaced nor short-circuited (FR-027, SC-005).

**C-63**: The receipt's coverage counts reviewed files, not test or compile coverage, and MUST NOT be cited as evidence for the reader-baseline judgement. Two different questions carry the same word; this clause keeps them apart so a later reader cannot mistake one green for the other (FR-027).

**C-64**: No existing contract assertion is deleted, weakened, or semantically drifted. One pin is intentionally changed — the `/speckit.review` row assertion in `tests/contract/test_review_p1_review_loop.py` — because C-47 removes the duplicated wording that pin quotes; the changed pin keeps its subject, adds an assertion of the owner's path, and adds a negative assertion that the duplicated wording is gone, and the change is disclosed in `research.md` § R5 and `feature-ref.md` (FR-027, FR-028).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-55 | FR-016 | — | command template |
| C-56 | FR-017 | SC-007 | command + skill |
| C-57 | FR-017 | SC-007 | command + skill + test |
| C-58 | FR-018 | — | command + skill |
| C-59 | FR-018 | — | feedback engine contract |
| C-60 | FR-020 | — | command + registration duty |
| C-61 | FR-020 | — | scope sweep |
| C-62 | FR-027 | SC-005 | expression gate owner + test |
| C-63 | FR-027 | — | receipt clause |
| C-64 | FR-027, FR-028 | — | test suite |
