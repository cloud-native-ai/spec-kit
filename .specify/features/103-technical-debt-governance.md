# Feature Detail: Technical Debt Governance

**Feature ID**: 103  
**Name**: Technical Debt Governance  
**Description**: Read-only technical-debt inventory and phased governance planning through a dedicated skill and agent roles, with authorized cleanup routed to the existing sanitize and SDD flows.  
**Status**: Implemented  
**Created**: 2026-11-11  
**Last Updated**: 2026-11-22

## Overview

The `debt-audit` skill partitions a project into disjoint read domains, dispatches one SDD Debt Governor execution per domain, verifies each returned report, and synthesizes a debt register plus a phased governance plan. The audit is read-only across project files: data reclamation belongs to `/speckit.sanitize`, mechanism repairs belong to an SDD run, and authorized bounded cleanup batches use the SDD Debt Fixer role. The capability is currently skill-level and deliberately has no slash-command wrapper.

## Latest Review

2026-11-22 implementation audit: the framework source contains `skills/internal/debt-audit/SKILL.md`, `agents/sdd-debt-governor.agent.md`, and `agents/sdd-debt-fixer.agent.md`, with installed projections and distribution/roster guards. The three source files were introduced on 2026-11-11 but had no feature-registry row; this record registers the delivered capability rather than proposing new work.

## Key Changes

1. Add a `debt-audit` orchestration skill for context loading, disjoint domain partitioning, governed dispatch, return verification, synthesis, adjudication, and handoff.
2. Add the SDD Debt Governor template for reproducible technical-debt findings, severity and disposition classification, baseline re-verification, and phased governance planning.
3. Add the SDD Debt Fixer template for explicitly authorized, bounded cleanup territories with pre-action manifests and post-action evidence.
4. Keep cleanup outside the audit skill: `/speckit.sanitize` owns reclamation and the SDD flow owns mechanism repairs.
5. Wire the capability into skill distribution, flow-class, probe, run-skills, and installed-mirror surfaces.

## Implementation Notes

- Framework sources: `skills/internal/debt-audit/SKILL.md`, `agents/sdd-debt-governor.agent.md`, and `agents/sdd-debt-fixer.agent.md`.
- The Governor may write only assigned reports and execution logs; the Fixer may write only an authorized item set, territory, and evidence path.
- Existing coverage includes `tests/contract/test_expression_compatibility.py`, `test_flow_class_ledger.py`, `test_migration_distribution.py`, `test_run_skills_wiring.py`, and `test_skill_layer_visibility_guards.py`.
- No standalone audit engine or second durable debt registry is introduced; reports use `.specify/studies/` by default.

## Future Evolution Suggestions

- Accumulate real audit-run evidence for partition quality, report verification, and synthesis fidelity.
- Add a slash-command wrapper only through a separate specification and governance decision.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/103-technical-debt-governance.md`
- Implementation: `skills/internal/debt-audit/SKILL.md`
- Agent Roles: `agents/sdd-debt-governor.agent.md`, `agents/sdd-debt-fixer.agent.md`
- Specification: none; this row registers existing implementation evidence.

## Status Tracking

- **Draft**: Capability gap or wrapper proposal registered without implementation.
- **Planned**: Requirements and design artifacts approved for a subsequent extension.
- **Implemented**: The audit skill and both agent roles exist in framework source and are wired into distribution and invocation surfaces. (current)
- **Blocked**: A declared final-path acceptance criterion for a subsequent extension fails.
- **Ready for Review**: Review evidence for a subsequent extension is complete and its current code-review record has no blocking entry.
- **Sealed**: A reviewed extension meets the canonical seal and archive-admission criteria.
- **Completed** (legacy): Historical terminal record only; not used for this feature.
