---
id: "20261105T071236Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "ir-20261105T071228Z-improve-skills-ssh-utils"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
disposition: "ignored"
partial: false
created: "2026-11-05T07:12:36Z"
summary: "Extracted SSH transport from sdd-project-setup into the new external ssh-utils skill. ssh-exec.py fixes RemoteCommand=none, POSIX quoting, stdin script push, su wrapping and exit-code propagation; set"
disposition_reason: "introspection:introspection-20261106T084116Z#Excluded"
---

## Review
Extracted SSH transport from sdd-project-setup into the new external ssh-utils skill. ssh-exec.py fixes RemoteCommand=none, POSIX quoting, stdin script push, su wrapping and exit-code propagation; setup now delegates remote execution and keeps only the carrier shape; shared dispatch recipes normalized. Frozen rosters/count pins moved; 19 residual test failures reproduced identically on a clean HEAD worktree (zero regression).

## Optimization Points
- 1) ssh-utils/scripts/ssh-exec.py owns SSH options, quoting, stdin, su and exit codes (RemoteCommand=none is unconditional). 2) sdd-project-setup delegates remote execution and keeps only topology shape. 3) external-dispatch-recipes.md now carries RemoteCommand=none in every direct ssh recipe. 4) tests/contract/test_ssh_utils_skill.py pins the invariant; 11 tests pass.
