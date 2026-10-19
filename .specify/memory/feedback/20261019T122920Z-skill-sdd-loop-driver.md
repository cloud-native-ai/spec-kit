---
id: "20261019T122920Z-skill-sdd-loop-driver"
unit_id: "skill:sdd-loop-driver"
unit_type: "skill"
run_id: "sdd-loop-driver-062-humanize-20261019"
scope: "local"
probe: "skill-sdd-loop-driver-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-10-19T12:29:20Z"
summary: "062 humanize SDD loop complete; monitoring hook/SSH improvements landed; probe object registered to close the feedback landing gap."
---

## Review
062 humanize SDD loop complete; monitoring hook/SSH improvements landed; probe object registered to close the feedback landing gap.

## Optimization Points
- Qoder CLI provides Claude-Code-compatible Stop/SubagentStop hooks; a Stop hook + FIFO/status file is a viable event-driven completion backstop for subagent monitoring, including remote SSH (hook on the run-user side, remote FIFO read over ssh, done.json check-before-wait).
- The existing watch-target.sh correctly uses PID file + start ticks + status/sentinel/heartbeat instead of pgrep counting; the ad-hoc failure matrix (pgrep zero-match, scope, login-shell noise, cws deletion) should be folded into the driver references.
- /speckit.plan and /speckit.implement Wrap-up engine calls in the templates lack required args (run-determination --run-id/--complexity, feedback-utils --run-id/--review/--points); agents must supplement them manually.
- The implement run was interrupted by UnsupportedFinishReasonError (transient model/CLI failure) and resumed from the tasks breakpoint; the exit-record/status path correctly returned FAILED while the Stop hook (normal-stop only) did not fire.
- An unplanned probe-utils.py path normalization was required for the compile pipeline (rollback experiment: compile-embeds --check exit 2); it was documented as a deviation rather than silently included.
- Review findings point to framework-level gaps: clause bracket-charset owner, checklist disposition ownership, review→improvement dead letter, compiled Wrap-up args, claimed-sample/evidence binding, baseline re-freeze on implement side.
- Remote SSH monitoring should run the watcher under bash --noprofile --norc with scoped repo matching, numeric-only parsing, empty=UNKNOWN, and dual-signal completion (exit record + sentinel); never kill remote processes on SSH failure.
