# Glossary Proposal — plan-stage addendum (proposal-only) — 107-decision-governance

**Date**: 2026-11-25 · **Stage**: plan · **Status**: proposal-only (`origin=auto`, `status=proposed`) — nothing is written to `.specify/glossary.md` before user confirmation (A-11 / FR-005).

The plan stage coined **no new project-specific terms** beyond the nine decision terms already proposed in `glossary-proposal.md` (Decision Item, Decision Class, Human-Interactive Decision, AI-Autonomous Decision, Decision Record, Decision Archive, Decision Producer, Decision Transmission, Implementation Receipt). That earlier file remains the current proposal; it is not rewritten here.

Field-name literals introduced by the plan are **not** glossary entries: `resource_locator`, `same_name_conflict`, `transmission_status`, `implementation_receipt`, `decision_block`, `superseded_by`, `forced` are schema field names whose value domains are owned by `shared/definitions/decision-definitions.md`; adding them to the glossary would create a second meaning surface. At implementation, the nine terms run `glossary-utils.py --action detect-conflict` before any proposed write, as the requirements-stage proposal already instructs.
