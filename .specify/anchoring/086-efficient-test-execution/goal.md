---
status: active
created: 2026-11-06
updated: 2026-11-06
binding:
  owner: human
  owner_id: human
  origin: 086-efficient-test-execution
---

# Goal: 086-efficient-test-execution

## Objective

The spec-kit framework ships efficient test execution as a first-class quality attribute: its own suite runs concurrently by default with a serial fallback and name-level failure parity, the principle is distributed through the constitution and instructions, and 085's temporary Goal/Team and concurrency mechanisms are exercised without regression.

## Success Criteria

1. Full-suite parallel wall-clock is at most 40% of the recorded 1031.48 s serial baseline, measured by the canonical runner.
2. The final parallel run has zero new failure names versus the serial baseline, with every serial exception explicitly declared.
3. The efficient-test-execution principle ships in the constitution template and live file, the instructions template and live file, and a single owner guideline.
4. 085's temporary Goal/Team, stage concurrency, worktree/integration queue and checkpoints are used in this run and their test suites remain green.
5. The feature reaches Ready for Review with zero blocking review findings and honest evidence.

## History

- 2026-11-06 — created.
