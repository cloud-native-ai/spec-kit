---
id: "20261110T104158Z-skill-sdd-loop-driver"
unit_id: "skill:sdd-loop-driver"
unit_type: "skill"
run_id: "20261110T092500Z-sdd-loop-driver"
scope: "local"
probe: "skill-sdd-loop-driver-cli-profile"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-10T10:41:58Z"
summary: "4-line unattended run (095-098): analyze gate stopped all four lines; fork carriers, read-domain waves, validation waves and per-stage gates otherwise worked."
---

## Review
4-line unattended run (095-098): analyze gate stopped all four lines; fork carriers, read-domain waves, validation waves and per-stage gates otherwise worked.

## Optimization Points
- FO-01 watcher pid file lacks run= → --run-id attribution always unattributed NO_SIGNAL; FO-02 window does not return RUNNING at expiry when pid alive; FO-03 re-dispatch reuses stale status-* → false DONE at elapsed=0; FO-04 gate literal grammar vs template wording (Source row cell / count-claim N tasks per package / RS-001 Contract cell); FO-05 manifest watcher exits at first terminal instead of waiting for all; FO-09 analyze gate one-repair-round bound stops 4/4 runs — propose an explicit disposition path or bound relaxation
