---
id: "20261106T075313Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "analyze-087-20261106T0752Z"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "087-arch-diagram-docs"
feature_id: "087"
partial: false
created: "2026-11-06T07:53:13Z"
summary: "analyze stage (round 1, read-only): 16 findings (2 HIGH / 8 MEDIUM / 6 LOW). HIGH-01: the plan Test Plan table B clause labels and the tasks [green:] tags do not track contracts/flow-obligations.contr"
---

## Review
analyze stage (round 1, read-only): 16 findings (2 HIGH / 8 MEDIUM / 6 LOW). HIGH-01: the plan Test Plan table B clause labels and the tasks [green:] tags do not track contracts/flow-obligations.contract.md's clause numbering from C-003 onward (e.g. plan C-003 'Reconcile R2' vs contract C-003 trace-record; plan C-010 'Authoring Flow produce point' vs contract C-010 Tiered Confirmation), so the 'all clauses covered / each claimed exactly once' claims are false and 8 real clauses have no mapped assertion. HIGH-02: plan Technical Constraints row 'docs/ zero change' + GATE-6 + T073 S8 contradict FR-001/plan structure/DoD-7/T064, which require editing docs/concepts/documentation-model.md; the completion gate is unachievable as written. MEDIUM: FR-012 and FR-021 have zero task rows; coverage-baseline.txt missing (accountant exit 2); C-004's five-value precedence contradicts C-016 and its own example; the fixture 'pre-deletion green state' invariant contradicts E6's already-deleted compositions; T076 writes tasks-stage-status.jsonl from an implement row; feature-ref row 10 mirror paths do not exist; OI-087-01 still open in register.md though N6 recorded it removed; feature detail stage record stops at plan attempt 2. No artifact edits, no commit; E3 row written (not-run-docs-only, one changed path).

## Optimization Points
- Analyze the plan's Test Plan and tasks' [green:] tags against the contract files by clause subject, not by name only: the coverage accountant counts names, so a shifted numbering still reads as 33 claims. Treat the plan's own constraints/gates as candidate contradictions when the delivery surface includes a docs/ path.
