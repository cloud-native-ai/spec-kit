---
status: active
created: 2026-11-26
updated: 2026-11-26
handoff_ref: .specify/specs/108-team-view-degradation/handoff.md
---

# Anchor: Team View Degradation

## Objective

The /speckit.team view command presents real-world team workspaces honestly: run reports are recognized by parseable timestamps (including hex suffixes), the latest report is chosen by parsed time, residue is named, missing artifacts and incomplete binding/goal are explicit degradation states with sanctioned repair pointers, and healthy teams keep byte-identical output from the single existing engine.

## Success Criteria

1. All 25 FR and 8 SC of spec 108 are delivered and verified, with red-first recognition/degradation tests and golden-output preservation for conforming teams.
2. Report recognition, latest selection, residue and missing-artifact states are honest and testable; binding/goal guidance never mutates; roster-matrix anomalies are explicit; degradation reasons and exit codes form a closed, documented set.
3. One engine (scripts/python/team-view.py); existing healthy output byte-preserved; compatibility/migration for any shape change; no second reader.

## Boundaries

- No push at implement; no view-side mutation of team definitions; no second reader or parallel state table.

## History

- 2026-11-26 — created.
