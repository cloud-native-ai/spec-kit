---
slug: demo-seat-dispatch
goal_slug: demo-seat-dispatch
pattern: serial
created: 2026-10-08
updated: 2026-10-08
description: "SC-002 demonstration team for spec 054 — proves a stage-frame seat is instantiated, rendered onto the host registration surface, and dispatched by its registered type."
---

## Goal

Demonstrate spec 054's closed chain end-to-end: a team built by the new create flow references a stage-frame seat, the seat is instantiated (placeholders resolved, team-scope set), reaches the host registration surface via `specify render-agents`, and is dispatched by its registered type — so `general-purpose` is no longer the required carrier.

## Static Structure (Role × Stage × Type)

| role | stage | type | agent | lifecycle | responsibility |
|------|-------|------|-------|----------|----------------|
| Executor | executor | Worker | dogfood-executor | temporary | Verify the host registration surface carries this seat's rendered definition with capacity fields; report success/error. |

## Dynamic Structure

**Pattern**: serial — one stage, quality-first handoff (verification task, no parallelism needed).

## Self-Improvement Contract

None — this team exists to demonstrate spec 054's SC-002 and is retired after the demonstration run.
