---
id: "20260906T021316Z-skill-git-workflow"
unit_id: "skill:git-workflow"
unit_type: "skill"
run_id: "048-derive-command-merge-20260905"
scope: "local"
probe: "skill-git-workflow-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-09-06T02:13:16Z"
summary: "Ran the skill in Execute scope for the 048-derive-command delivery: commit the branch's work, then merge into master. Observed the managed block in .specify/git-workflow.md is still the 'None yet.' pl"
---

## Review
Ran the skill in Execute scope for the 048-derive-command delivery: commit the branch's work, then merge into master. Observed the managed block in .specify/git-workflow.md is still the 'None yet.' placeholder and this repo has no PRE/DEV tier — only master plus short-lived feature branches. Proceeded with the operation anyway (user directed: local merge, no push, leave the block as-is). Split 60 staged files into three concern-separated commits (3b6506e7 git-fleet mirror, 35f48b5c feedback bundles, 9dd29806 the feature), verified worktree clean and branch ahead=3/behind=0 before merging, then merged --no-ff to match repo precedent (1e5d74f2). Confirmed the merged tree is byte-identical to the branch tip and master is ahead=4/behind=0 of gitlab/master with nothing pushed. Outcome matched the user's request exactly; no destructive git command was used and no hook was skipped.

## Optimization Points
- **Pre-merge safety gate passed only because the worktree happened to be clean; the skill does not tell the agent to make it clean.** `.specify/git-workflow.md`'s Execute Step 3.2 gate is `git status --short` must be empty — but in this run the working tree held 60 staged files spanning three unrelated concerns (52 feature paths, 6 `git-fleet` mirror files, 2 inbound `feedback/*.zip` bundles). The skill has no branch for "gate fails because there IS uncommitted work that belongs to this operation". I had to improvise: `git reset -q` (index-only, worktree untouched) then re-stage by group and commit three times. Suggested addition to `references/execute-commands.md` §前置校验: when the gate fails and the pending work is what the user asked to commit, the resolution is *group-and-commit*, not abort — plus an explicit warning that only `git reset` (never `git checkout .` / `git restore` / `git clean`) may be used to unstage, since the latter three discard work.
- **The managed block being `None yet.` did not block Execute, and the skill does not say what that means.** Phase 0 routes on "block filled?" — unfilled routes to Bootstrap. But the user's instruction was an Execute-shaped operation (commit + merge to master) on a repo whose real branch layout (`master` + short-lived feature branches, no PRE/DEV tier at all) does not match the three-tier model. I chose to execute the operation and leave the block as the user directed, which meant running with **no declared MAIN/PRE/DEV and therefore no tier safety net**: Security rule 2 ("禁止跳过 PRE 直接把 DEV 合入 MAIN") was unenforceable because no PRE exists here. Worth recording as an observation, not a fix: for single-tier repos the skill should either say "Bootstrap first, then Execute" or explicitly define a degraded Execute mode that names which Security rules become vacuous.
