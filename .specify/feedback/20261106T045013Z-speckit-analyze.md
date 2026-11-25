---
id: "20261106T045013Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261106T040353Z-087a"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "087-speckit-visualization"
disposition: "processed"
partial: false
created: "2026-11-06T04:50:13Z"
summary: "analyze round 1 produced 22 findings (1 critical / 3 high / 13 medium / 5 low); the four checklist-named items were adjudicated (CHK027 high, CHK052 medium with a corrected premise, CHK056 low, CHK012"
introspection_ref: "introspection-20261108T192504Z#F-11"
disposition_reason: "introspection:introspection-20261108T192504Z#F-11"
---

## Review
analyze round 1 produced 22 findings (1 critical / 3 high / 13 medium / 5 low); the four checklist-named items were adjudicated (CHK027 high, CHK052 medium with a corrected premise, CHK056 low, CHK012 no finding); 16 unclaimed contract clauses classified (14 justified, 1 partial, 1 with no scheduled proof); both deterministic coverage problems (baseline-missing, fr-uncovered 20/22) surfaced with remedies. CRITICAL/HIGH validation degraded to a direct re-read because this worker cannot dispatch subagents, and that degradation is stated per row.

## Optimization Points
- Works: the deterministic validators (requirements/tasks/decision-tensions/pre-analyze) all passed while the artifact set still carried cross-layer mapping drift, so the semantic mapping check this skill adds earned its keep. Friction: (1) account-clause-coverage's fr-uncovered lane reads backticked FR ids as mentions, so a contract set that cites FRs in code spans reports 20/22 uncovered even though the file headers map every FR; (2) the analyze worker has no sanctioned way to freeze a missing coverage baseline (correctly), so the coverage lane stays red until the tasks stage is re-entered; (3) the checklist-named premise for CHK052 (SC-006 carries the 30-second literal) was factually wrong and had to be corrected in the report rather than fixed upstream.
- token-efficiency: the six contract bodies were consumed in full (~40 KB) although the mapping checks (16 unclaimed clauses, 8 proposition pointers) needed only clause headings plus the `*Judged by*` lines; a heading-first index (~6 KB) followed by targeted bodies for the unclaimed clauses would have roughly halved the read volume. Counts were program-derived (Python/shell), no machine-managed store was injected whole, and the 93 KB accountant output was consumed via its head/tail preview plus targeted grep rather than in full. Proxy metric = bytes read, not a token count.
