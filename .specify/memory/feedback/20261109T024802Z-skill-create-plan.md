---
id: "20261109T024802Z-skill-create-plan"
unit_id: "skill:create-plan"
unit_type: "skill"
run_id: "r20261109T023000Z-auto-git-closeout"
scope: "local"
probe: "skill-create-plan-wrapup"
kind: "internal"
slice: "skills"
feature: "091-auto-git-closeout"
feature_id: "091"
partial: false
created: "2026-11-09T02:48:02Z"
summary: "Plan stage on the 28-FR / 8-SC 091 spec produced plan.md plus the full Phase 1 set (research R1-R12, data model 6 entities / 14 rules, 4 contract pages / 26 clauses, quickstart 8 scenarios) and refine"
---

## Review
Plan stage on the 28-FR / 8-SC 091 spec produced plan.md plus the full Phase 1 set (research R1-R12, data model 6 entities / 14 rules, 4 contract pages / 26 clauses, quickstart 8 scenarios) and refined the delivery surface in three measured places. Driven to `pre-analyze-check --stage plan decision=pass errors=0 advisories=0`, 5 decision-tension records clean, decomposition `proceed`, overlap unchanged at 36 adjudicated collisions (all on completed lines, zero active).

## Optimization Points
- pre-analyze-check.py `§ Execution Premises` row parsing counted a bare `| 090 |` inside an Evidence cell as the EP's Status value (`plan.md:229 EP-006 declares Status: 090`). The cell grammar is unescaped markdown, so any pipe-delimited content in a free-text cell silently becomes a field. A reader of the FAIL message cannot tell it parsed the wrong cell.
- The `missing-path` advisory class fires on every backticked token that does not exist yet, i.e. exactly the deliverables a plan is supposed to declare (5 fired, all on files the plan promises to create). The only remedy is to stop naming them as paths, which degrades precision. A path declaration and a path existence claim are different propositions; one advisory class serves both.
- `inherited-blocker-undisposed` rejects the conventional `—` empty-cell marker with an opaque key `091-auto-git-closeout:—`; the closed set (`resolved` / `inherited` / `not-applicable`) is not discoverable from the message.
- validate-decision-tensions.py enforces dense ID order across the whole document (`expected T-005, found T-014`), so inserting a record mid-document forces renumbering of every later record — the T-NNN identity is positional rather than stable. Cheap to hit, and the renumbering is invisible to anything that cited the old number.
- Gate invocation surfaces differ per script for the same concept: `pre-analyze-check`/`overlap-check` take `--spec-dir`, `decomposition-check` takes `--requirements`, `validate-requirements`/`validate-decision-tensions` take a positional path / `--spec`. Three rejected invocations in this stage before the right form was found for each.
