---
id: "20261126T071947Z-skill-sdd-loop-driver"
unit_id: "skill:sdd-loop-driver"
unit_type: "skill"
run_id: "r20261126T071500Z-fb-2"
scope: "local"
probe: "skill-sdd-loop-driver-cli-profile"
kind: "internal"
slice: "skills"
disposition: "processed"
partial: false
created: "2026-11-26T07:19:47Z"
summary: "The driver's sanctioned worktree root is rejected by the registry that is supposed to record it: `line-registry.py register --write-line --worktree-path <repo>/.specify/.tmp/sdd-loop/worktrees/<line>`"
introspection_ref: "introspection-20261127T162331Z#F-07"
disposition_reason: "introspection:introspection-20261127T162331Z#F-07"
---

## Review
The driver's sanctioned worktree root is rejected by the registry that is supposed to record it: `line-registry.py register --write-line --worktree-path <repo>/.specify/.tmp/sdd-loop/worktrees/<line>` exits 2 with "worktree_path must be outside repo_root", while that exact path is the driver's sanctioned location (line 107, review F3, spine F-OBS-107-2). Line 107 was registered without write-line fields and the worktree was recorded only in the spine prose, so registry-driven status and recovery cannot see worktree lines and the two owners disagree about the same path.

## Optimization Points
- 1. Exempt the sanctioned .specify/.tmp/sdd-loop/worktrees/ prefix from the outside-repo rule while still rejecting arbitrary in-repo paths.
- 2. Or move the sanctioned worktree root outside the repository and update the dispatch recipes, guards and tests in the same change.
- 3. Add a contract test with the sanctioned path accepted and a random in-repo path rejected, so the registry and the driver cannot drift apart again.
