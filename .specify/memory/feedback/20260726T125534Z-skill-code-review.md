---
id: "20260726T125534Z-skill-code-review"
unit_id: "skill:code-review"
unit_type: "skill"
run_id: "code-review-dogfood-20260726"
scope: "local"
feature: "code-review"
partial: false
created: "2026-07-26T12:55:34Z"
summary: "First dogfood run of code-review (presenting the instructions+memory change set) exposed two real defects in git-delta-review.sh: no support for uncommitted changes (ref..ref only) and silent invisibi"
---

## Review
First dogfood run of code-review (presenting the instructions+memory change set) exposed two real defects in git-delta-review.sh: no support for uncommitted changes (ref..ref only) and silent invisibility of untracked files. Both were fixed and runtime-validated in the same loop (--worktree mode + warn_untracked). Merge-gate summary correctly reported 0 blocking/0 important for a change set with only praise/suggestion notes.

## Optimization Points
- [FIXED this run] First dogfood use failed immediately: script only supported ref..ref diffs, but the primary dogfooding scenario is reviewing uncommitted changes. Added --worktree mode (git diff HEAD, staged+unstaged) to diff/review.
- [FIXED this run] git diff HEAD silently hides untracked files — an entire new skill was invisible to review. Added warn_untracked surfacing untracked files with git add -N guidance (excludes .review/ itself).
- Environment note: delta not installed in this container, so side-by-side rendering was exercised via a cat-stub; a real-delta run should be validated on a machine with delta installed (install: https://github.com/dandavison/delta).
