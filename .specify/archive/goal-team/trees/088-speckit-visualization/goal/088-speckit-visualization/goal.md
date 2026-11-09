---
status: active
created: 2026-11-06
updated: 2026-11-06
---

# Goal: Speckit Framework Visualization — 随时掌握并发/异步流程现状

## Objective

While a Speckit run is executing, the user can tell at any moment what is currently running, what has completed, and what is blocked, without interrupting the run or inspecting internal records.

## Success Criteria

1. A user without access to internal logs can state, from console output alone, which stage and which agents are currently active in a live run.
2. No long-running asynchronous flow reaches completion or stall without the user having received at least one visible state update while it ran.
3. Every reported progress line corresponds to an observed event; the reporting layer never fabricates progress and never buffers all output until process exit.

## Boundaries

- Not a replacement for on-disk evidence (state spine, stage logs, exit records); not a new persistent service or daemon; not a change to the stage sequence, sentinels, or gate semantics.

## Targets

| ID | Target | Status |
|----|--------|--------|
| T-001 | Each team run reports its overall progress and current state to the console at a fixed 30-second cadence. | open |
| T-002 | A supervising master-slave flow (such as the coaching-skills skill) reports the state and progress of its child flows while they run. | open |

## History

- 2026-11-06 — created.
- 2026-11-06 target T-001 added: Each team run reports its overall progress and current state to the console at a fixed 30-second cadence.
- 2026-11-06 target T-002 added: A supervising master-slave flow (such as the coaching-skills skill) reports the state and progress of its child flows while they run.
