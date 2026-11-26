---
status: active
created: 2026-11-25
updated: 2026-11-25
handoff_ref: .specify/specs/106-background-silent-failure/handoff.md
---

# Anchor: Background Dispatch Settlement

## Objective

Every background dispatch from a superagent to subagents ends in one observable settlement value with positive evidence — completed, failed, anomaly, cancelled, running, silent-end or unknown — so silent success and silent failure are both detected, reported and acted on, never mistaken for running or for success.

## Success Criteria

1. All 41 FRs and 9 SCs of spec 106 are delivered and verified, including red-first carrier silent-end fixtures and a mutation drill proving the checks can go red.
2. Every in-scope carrier (C1 fork, C2 subprocess, C3 team seats, C4 native background, C6 external recipes; C5 virtual excluded) surfaces a closed settlement value with positive evidence; no silent termination is reported completed, failed or running.
3. Preserved surfaces stay byte-stable (watcher verdicts/exit codes/sentinels, five-element uplink, seven-field downlink, confirmation discipline, two-slot budget) with zero NEW blocking gate hits on touched files.

## Boundaries

- No push, no second mechanism/engine/registry, no auto-kill or auto-retry, no evidence deletion, no history rewrite; legacy records are annotated, never rewritten.

## History

- 2026-11-25 — created.
