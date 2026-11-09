---
id: "20261109T085247Z-skill-analyze-artifacts"
unit_id: "skill:analyze-artifacts"
unit_type: "skill"
run_id: "093-analyze-skill-a1"
scope: "local"
probe: "skill-analyze-artifacts-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-09T08:52:47Z"
summary: "The skill's seven detection passes covered duplication, ambiguity, underspecification, inconsistency and constitution conflict well; the gap was coverage: the skill's coverage step consumes account-cl"
---

## Review
The skill's seven detection passes covered duplication, ambiguity, underspecification, inconsistency and constitution conflict well; the gap was coverage: the skill's coverage step consumes account-clause-coverage.py but the skill text does not say that a red FR lane blocks, so an executor must decide severity for it unprompted.

## Optimization Points
- Spell out which gate verdicts are blocking (FR lane, clause lane) and which are informational, so the verdict rule is reproducible across executors.
