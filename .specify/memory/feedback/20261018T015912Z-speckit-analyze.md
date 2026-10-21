---
id: "20261018T015912Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "speckit-analyze-20261018T015833Z"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "061-subagent-cli-config"
feature_id: "061"
disposition: "ignored"
partial: false
created: "2026-10-18T01:59:12Z"
summary: "061 analyze: 4 HIGH (auto vs matrix; SC-006 claude+declared; defaults mode precedence; runtime defaults missing), 18 MEDIUM, 3 LOW; read-only report; no commit."
disposition_reason: "introspection-20261021T133447Z: excluded (no actionable framework finding)"
---

## Review
061 analyze: 4 HIGH (auto vs matrix; SC-006 claude+declared; defaults mode precedence; runtime defaults missing), 18 MEDIUM, 3 LOW; read-only report; no commit.

## Optimization Points
- Analyze wrap-up surface is under-specified: run-determination requires --run-id/--complexity and feedback-utils requires --points, but the generated Wrap-up lists only --unit-id/--unit-type.
