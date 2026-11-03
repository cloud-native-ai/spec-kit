---
id: "20261103T001400Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261102T225758Z-081a"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-11-03T00:14:00Z"
summary: "analyze 081a: 3 checklist semantic FAILs adjudicated (CHK012/017/021 sustained), 8 fixes re-verified with 3 reopenings, 3 HIGH confirmed by external qodercli validators (after SDK-env defect on first "
---

## Review
analyze 081a: 3 checklist semantic FAILs adjudicated (CHK012/017/021 sustained), 8 fixes re-verified with 3 reopenings, 3 HIGH confirmed by external qodercli validators (after SDK-env defect on first dispatch), 8 MEDIUM/6 LOW; deterministic gates rerun (validate-requirements ok, pre-analyze pass 98 advisories, decision-tensions ok, validate-tasks 1 warning on T003/T021 [P], coverage baseline missing).

## Optimization Points
- fast-fail on the validator dispatch: recipe 7's DISPATCH_CLI_FLAGS default fails on this host (sdk_worker_removed, exit 42) and claude is not resolvable from the wrapper (exit 127); the recipe should document unsetting QODER_AGENT_SDK_* / QODER_SESSION_TYPE before dispatch, as its own note already hints. Also: validate-tasks treats any path *cited* in a row description as a write target, so an [P] row that references data-model.md is flagged — the template should distinguish cited-reference paths from write targets. And account-clause-coverage's [fr-uncovered] lane reports 0/N on every spec tried (080 and 081 identically), so the lane cannot discriminate; consumers waste a run discovering it.
