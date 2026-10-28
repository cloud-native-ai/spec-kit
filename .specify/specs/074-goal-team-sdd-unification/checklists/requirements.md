# Specification Quality Checklist: Goal/Team/Agent 与 SDD 开发流程统一

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-10-28
**Feature**: `.specify/specs/074-goal-team-sdd-unification/requirements.md`

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Stability / containment claims name a baseline referent and a derivable allowed-delta set (owner: `.specify/shared/guidelines/closed-set-claims.md`)
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- Checker evidence (re-run after the clarify write-back): `python3 scripts/python/validate-requirements.py .specify/specs/074-goal-team-sdd-unification/requirements.md` → `status: ok`, all five propositions pass (`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id`), scanned 524 lines, 36 definition rows (28 FR + 8 SC), 11 shared strings, `0 error(s), 0 warning(s)`, exit code 0. Every stamp above derives from this run, not from hand-typing.
- Decomposition gate evidence: `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/074-goal-team-sdd-unification/requirements.md` → `{"decision": "proceed", "measured": {"fr_count": 28, "fr_ceiling": 30, "task_ceiling": 40}, "reasons": []}`, exit code 0. No slicing required.
- Requirements-stage in-session clarifications (sanctioned variant): the three load-bearing design questions were settled before the checklist and are recorded under `## Clarifications` > `### Session 2026-10-28` — authorization surface (Agent capability + Team policy), routing basis (composite deterministic verdict), and nested-run end state (review handoff, outer layer owns merge). No active clarification marker remains.
- Clarify run (Mode A, same-author gate): the coverage scan was delegated to one fresh-context read-only subagent (8 material candidates); five were ratified — new Feature 074, `shared/definitions/sdd-routing-definitions.md` as the routing owner, precedence `adjudicate > sdd > direct`, depth-2 nesting with virtual-mode hosting prohibited, and a `team.md` frontmatter `seats` map resolved by (team, seat). Three bounded corrections landed in the same pass: routing unit = one declared duty reused until inputs change; concurrency cap = per member; handoff carries the integration identity and the team supervisor writes the ledger attribution row. All are recorded under the same session block.
- Feature linkage is resolved: `Related Feature` is Feature 074; the index row (Draft) and `features/074.md` detail land in this run.
- Containment claims were repaired before stamping: FR-026, FR-027, SC-005, and SC-008 now name a baseline referent (the pre-change case set / goal fixture captured at the baseline commit in the verification record), a comparison unit (contract-suite case set; parsed Goal field set), an allowed delta (added cases only; identical field set), and no undefined aggregate such as "unaffected" or "其余".
- Reader baseline: this is a framework-maintenance specification, so "non-technical stakeholder" is the framework maintainer who did not take part in the run. Every framework term is either defined in the spec or reached by owner path; named artifacts are existing owners (`sdd-loop-driver`, `team.md`, agent frontmatter, line registry), not a new technology choice.
- Honest boundary recorded as Assumption A4: the routing engine is deterministic over declared inputs; a knowingly misclassified declaration cannot be detected by the engine and is audited by the review surface. The spec does not claim otherwise.
- Scope interpretation recorded as Assumption A6: only `sdd-loop-driver` is the SDD development flow; `sdd-project-setup` and `sdd-house-keeping` are routed bootstrap/maintenance paths in the same routing surface, not nested development runs.
- The anti-nesting obligation is narrowed once, in its existing owner, to the depth-2 chain in FR-005/FR-006 (including the virtual-mode prohibition); the spec references that owner rather than creating a second governance rule.
