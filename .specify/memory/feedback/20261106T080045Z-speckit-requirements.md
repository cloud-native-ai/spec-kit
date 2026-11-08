---
id: "20261106T080045Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "r20261106T090000Z-086a"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "086-script-interface-contract"
partial: false
created: "2026-11-06T08:00:45Z"
summary: "086 requirements: the user's incident (generate-instructions.sh ignored --help and ran a reconcile) distilled into a framework-level script interface contract — every directly executable *.sh/*.py MUS"
---

## Review
086 requirements: the user's incident (generate-instructions.sh ignored --help and ran a reconcile) distilled into a framework-level script interface contract — every directly executable *.sh/*.py MUST support -h/--help and --version with zero side effects, unknown options MUST fail non-zero with usage, sourced/imported libraries exempt by a mechanical criterion. 23 FR / 8 SC / 7 user stories / 9 assumptions; 5 governance landing points named. Validator ok (303 lines, 0 error/0 warning); pre-analyze pass (0 advisories); decomposition proceed (23/60); flow-class execution (declaration).

## Optimization Points
- 1) The dispatch brief's baseline count for refresh-tools.sh was wrong — it already has --help; the executor re-measured and corrected A2, which is the right behavior but shows the brief should carry measured evidence, not recalled counts. 2) The incident premise cannot be verified from git history: no commit ever produced '+70/-0' in .specify/instructions.md, so SC-002 had to be rewritten as a self-contained sha256 before/after experiment. 3) The requirements executor completed the stage without running Wrap-up accounting and without emitting WRAPUP-DEFERRED; the driver had to backfill run-determination/exec-quant/feedback. 4) run-determination.py rejects an unknown flag with argparse usage but the surrounding shell pipeline still looked successful until exit codes were checked one by one — exactly the failure class this feature targets.
