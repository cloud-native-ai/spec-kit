---
id: "20261109T032455Z-skill-sdd-loop-driver"
unit_id: "skill:sdd-loop-driver"
unit_type: "skill"
run_id: "r20261109T023000Z-auto-closeout-repair1"
scope: "local"
probe: "skill-sdd-loop-driver-cli-profile"
kind: "internal"
slice: "skills"
feature: "091-auto-git-closeout"
feature_id: "091"
partial: false
created: "2026-11-09T03:24:55Z"
summary: "Analyze-repair slice for 091: resolved the CRITICAL and all four HIGH findings, re-cut the contract clause set 26 -> 32, and brought FR coverage 24/28 -> 28/28. Five required gates green before and af"
---

## Review
Analyze-repair slice for 091: resolved the CRITICAL and all four HIGH findings, re-cut the contract clause set 26 -> 32, and brought FR coverage 24/28 -> 28/28. Five required gates green before and after.

## Optimization Points
- 1. account-clause-coverage.py counts a clause's LAST FR-containing parenthetical as its citation group, so a clause that mentions an id in prose cites nothing and the gap looks like a citation-form nit. Four FRs sat uncovered while feature-ref.md asserted they were discharged; reading the extractor (clause_extract.py clause_citations) first would have made C-01 a five-minute finding instead of an inference. The gate's own docstring states the rule; the artifact's map contradicted it. -- 2. validate-tasks.py green-cross-phase compares clause order against ROW order within one contract page, so a clause whose subject belongs to an earlier user story than the row which turns it green always warns. There is no way to satisfy it without renumbering the page into a worse reading; the check has no 'disclosed exception' channel, so the only honest form is a recorded adjudication plus a non-zero count in the DoD. -- 3. run-determination.py --names-current/--names-baseline are FAILED-test-nodeid lists, not 'what passed' notes; the flag names read like free-text summaries and the args-manifest does not say otherwise. Two rejected invocations before the semantics were found. -- 4. run-determination.py admits custom:<owner>/<name> in its own record schema but the memory engine's --source contract rejects it, so a custom unit's record is emitted and NOT landed, with a message on stdout only. A subagent slice that identifies itself honestly loses its run record; identifying as skill:sdd-loop-driver lands it but misattributes the unit. -- 5. pre-analyze-check.py missing-path advisories fire on every deliverable a plan has not created yet, so this feature's advisory count (46 -> 47) can only move when a task row stops naming its own deliverables. An advisory class that punishes declaring work is hard to distinguish from a real defect count. -- 6. The repair brief lists R-1..R-13 but the analyzer's full findings text for M/L items was compressed into a single paragraph, so several MEDIUM dispositions (M-01, M-03, M-08) had to be re-derived from the artifacts rather than read from the report; the brief's own pointers were the only source.
