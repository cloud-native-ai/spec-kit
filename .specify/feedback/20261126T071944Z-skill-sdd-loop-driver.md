---
id: "20261126T071944Z-skill-sdd-loop-driver"
unit_id: "skill:sdd-loop-driver"
unit_type: "skill"
run_id: "r20261126T071500Z-fb"
scope: "local"
probe: "skill-sdd-loop-driver-cli-profile"
kind: "internal"
slice: "skills"
disposition: "processed"
partial: false
created: "2026-11-26T07:19:44Z"
summary: "Worktree dispatch dies at startup because the runner resolves its prompt after changing directory: skills/external/sdd-loop-driver/scripts/stage-runner.sh chdirs to --project-dir and only then reads -"
introspection_ref: "introspection-20261127T162331Z#F-07"
disposition_reason: "introspection:introspection-20261127T162331Z#F-07"
---

## Review
Worktree dispatch dies at startup because the runner resolves its prompt after changing directory: skills/external/sdd-loop-driver/scripts/stage-runner.sh chdirs to --project-dir and only then reads --prompt-file, so the documented relative prompt path (.specify/state/prompt-<line>-<stage>.md) resolves inside the worktree and the first stage of line 107 failed about 7 s in (rc 1, "No such file or directory"; review F2, spine F-OBS-107-1 and "U5 — requirements attempt 1 FAILED"). Absolute --prompt-file/--state-dir paths are the only workaround and no recipe states it, so every worktree line pays one failed dispatch before its first useful stage, and the failure reads as a missing prompt rather than a path-resolution defect.

## Optimization Points
- 1. Resolve --prompt-file and --state-dir against the invocation directory before the chdir to --project-dir, then use the resolved absolute paths for the rest of the run.
- 2. If resolution cannot change, make a relative prompt path that resolves outside the project dir a startup error that names both candidate resolutions, instead of a late "No such file or directory".
- 3. Document the absolute-path requirement in the dispatch recipe and add the check to dispatch preflight so a worktree line cannot launch on a doomed path.
