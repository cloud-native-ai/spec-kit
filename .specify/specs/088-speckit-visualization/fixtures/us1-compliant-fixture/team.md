---
name: US1 Cadence Fixture Team
slug: us1-compliant-fixture
description: The compliant roster fixture T018 renders the seat and the status line against.
goal: >
  Prove the reporter seat is a roster row and that a run over it emits attributed
  status lines on cadence for longer than two intervals.
pattern: parallel
created: 2026-11-06
updated: 2026-11-06
members:
  - agent: skill-verifier
    role: verifier
    lifecycle: temporary
  - agent: reporter
    role: reporter
    lifecycle: persistent
    reporting-territory:
      read: [".specify/teams/us1-compliant-fixture/**"]
      write: [".specify/teams/us1-compliant-fixture/runs/status.live.log"]
    reporting-cadence: default
config:
  parallelism: 1
---

## Goal

Prove the reporter seat is a `members[]` row and that a run over it emits attributed status lines on cadence.

## Static Structure

| Role | Stage | Type | Agent |
| --- | --- | --- | --- |
| verifier | evaluator | Worker | skill-verifier |
| reporter | (lifecycle-wide) | Meta | reporter |

## Dynamic Structure

Parallel; one lane, one lifecycle-wide reporter seat.

## Self-Improvement Contract

- Subject: this fixture roster; the guard run is the evidence.
- Observe: the guard's exit code and its named defects.
- Improve: n/a — a fixture, not a team under improvement.
- Boundary: preserves the seat's cardinality (at most one).
- Verify: `validate-roster.py` exits 0.
