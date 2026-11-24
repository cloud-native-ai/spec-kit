# Feature Detail: Agents Command

**Feature ID**: 019  
**Name**: Agents Command  
**Description**: Create, refine, and run layered agents with rendered host registrations.
**Status**: Ready for Review  
**Created**: 2026-02-27  
**Last Updated**: 2026-11-24

## Overview

`/speckit.agents` routes create, refine, and run intents across Agent Template and Agent Instance storage under `.specify/agents/`. `run-agent` resolves execution configuration and topology before dispatch, while `specify render-agents` projects neutral metadata into real Qoder, Claude, Copilot, and opencode registration files.

## Latest Review

2026-11-24 review (`104-agents-run`): four-segment review completed — P0 = 0; process / artifact / implementation / code segments all `pass`; code gate `allow`; acceptance reality check `final_path` 2/2 `pass` (SC-001, SC-002 with smoke evidence); the transition `Implemented → Ready for Review` was judged allowed (four conjunctive conditions) and **landed by the driver** (this row + this entry + index row). Carried as framework-improvement P1s: F1 `targeted-set-v1` stem matching, F2 plan-change audit scope (basename collision), F3 one-shot clause in the stage-prompt skeleton, F4 implement evidence-capture rules. Closure (full suite + merge) follows on the line.

2026-11-24 checklist: `checklists/run-command-2026-11-24.md` landed for `104-agents-run` — 40 requirement-quality items across seven dimensions (traceability 40/40, soft cap 40), with the requirements-phase `checklists/requirements.md` left untouched; `validate-requirements.py` reported 0 error / 0 warning (281 lines, 24 FR / 7 SC / 8 shared strings); E3 `test-evidence/checklist.jsonl` carries exactly one `stage-status` row (`status=not-run-docs-only`). Feature status stays `Implemented` — the checklist phase precedes `/speckit.implement` and holds no status-transition authority.

2026-11-24 tasks: `tasks.md` landed for `104-agents-run` — 33 dependency-ordered rows (Setup 1 / US1 8 / US2 3 / US3 3 / US4 8 / US5 3 / Polish 7) with 35 `[green:]` claims partitioning C-01…C-35 exactly once; the single `green-cross-phase` WARN is C-06, whose third face (the command-reference Syntax block) lands in US4 and is adjudicated in the tasks report. `validate-tasks.py` 0 error / 1 warning; `pre-analyze-check.py --stage tasks` pass (errors=0, advisories=57, all naming the five test files this stage plans or the data-model INV ids); `account-clause-coverage.py` status=ok (claimed clauses 35, FR 24/24, uncovered beyond baseline 0) after a citation-level `PLAN-EDIT` added FR-013 / FR-021 / FR-024 to existing clause citation groups; `coverage-baseline.txt` frozen at `a02705a3c`. Feature-list re-validation found no new, merged, or invalidated Feature — status stays `Implemented` (the tasks phase has no status-transition authority).

2026-11-24 plan artifacts landed for `104-agents-run`: `plan.md` / `research.md` / `data-model.md` / three contracts (`agents-run-command` / `agents-run-dispatch` / `agents-run-docs`) / `quickstart.md` / `feature-ref.md`. The plan fixes the explicit `run <agent-name> [task]` grammar across three surfaces, wires the 095 role protocol into `run-agent` dispatch (presentation disclosure, seven-field downlink, five-element uplink, child-label convention, narrowed SDD probe condition), and merges the three concatenated command-reference copies into one body. No new skill, store or registry; Feature status stays `Implemented` under the no-status-regression gate.

2026-11-24 clarify binding: requirement `104-agents-run` was bound directly to Feature 019. It adds the explicit `run` subcommand to the same `/speckit.agents` command surface and wires the 095 superagent/subagent role model into dispatch-time presentation, payload, and return contract — the same relation its predecessors (003 / 014 / 022 / 023) already have to this Feature. Feature status stays `Implemented` under the no-status-regression gate; the new spec advances its own lifecycle independently. Binding record and rationale: `.specify/specs/104-agents-run/requirements.md` § Related Feature / § Clarifications.

2026-11-22 implementation audit: `/speckit.agents` now unifies create, refine, and run. Templates and instances live under `.specify/agents/`; `run-agent` owns configuration resolution, topology selection, dispatch, and fast-fail injection. `specify render-agents` writes actual host registration files with deterministic instance-over-template precedence. Older `.github/agents/` primary-storage, directory-symlink, and workspace-file claims below are historical, not the current contract.

## Key Changes

1. Implement agent file creation in `.github/agents/` directory with proper naming conventions (kebab-case)
2. Support both explicit agent specifications and context-inferred agent generation with confidence-based handling
3. Include comprehensive validation for YAML frontmatter correctness, provider whitelist compliance, and tool-workflow consistency
4. Provide example prompts for agent invocation and usage guidance
5. Enable agent updates and refinements with same-name overwrite semantics
6. Added plan artifacts for spec `003-speckit-agents-command` (`plan.md`, `data-model.md`, `contracts/agents-command.openapi.yaml`, `quickstart.md`)
7. Locked clarified defaults: same-name overwrite, low-confidence intent halt, auto-create `.github/agents/`, contradiction blocking, least-privilege tools
8. Added executable task breakdown for Setup/Foundational/US1/US2/US3/Polish phases with explicit dependencies and parallel markers
9. Implemented three-tier validation system: YAML syntax, approved providers only (GitHub Copilot/Qwen Code/opencode), and tools-workflow alignment
10. Added comprehensive quickstart validation steps covering all user stories and edge cases
11. Spec 014: Refactored canonical directory from `.github/agents/` to `.specify/agents/` with directory-level symlink bridging to tool-specific paths
12. Spec 014: Added shared `references/` directory for cross-agent reference materials
13. Spec 014: Added `specify init` bundled agent installation mirroring the skills installation flow
14. Spec 014: Generalized symlink helper to support both skills and agents

## Implementation Notes

- Canonical template and instance stores are `.specify/agents/templates/` and `.specify/agents/instances/`; host-specific files are rendered outputs, not symlinked primary storage.
- `templates/commands/agents.md` routes to `create-agent`, `improve-agent`, and `run-agent` rather than implementing each operation inline.
- `src/specify_cli/__init__.py` owns `render-agents` projection, manifest, backup, and stale-prune behavior; Qoder, Claude, Copilot, and opencode have real renderers.
- `run-agent` injects the fast-fail clause at dispatch and resolves local or remote execution topology from the declared configuration layers.
- Workspace files such as `AGENTS.md`, `MEMORY.md`, `SOUL.md`, and `USER.md` are not created by the current `/speckit.agents` flow.

## Latest Evolution

Spec 022 (eei-agent-triad): Adds the Executor-Evaluator-Improver (EEI) triad dimension to the role-based agent architecture. Within any role, work is decomposed into three independent subagents: Executor (performs tasks), Evaluator (scores output with configurable dimensions), and Improver (modifies executor's environment and prompt). Proven in a K8s diagram optimization session (score 49→91 over 17 rounds). Key innovations: context isolation between triad members, dual-target improvement (environment + executor prompt), dotted/solid line visual distinction for control/data signals.

**Spec 022 implementation (2026-07-02)**: Delivered 4 new templates — `agent-subrole-executor-template.md`, `agent-subrole-evaluator-template.md`, `agent-subrole-improver-template.md` (role-agnostic via `{{AGENT_NAME}}` placeholders), and `agent-triad-orchestration-template.md` (loop scaffold with threshold/regression stopping conditions and iteration-history table). Updated create-agent (Triad Mode) and improve-agent (Triad Refinement) skills. Added `docs/eei-triad-pattern.md` reference guide. Contract/integration test tasks (T008, T013) deferred — no runtime code to pytest; validation is structural + reference-session-based. All 6 SCs pass or partial (SC-001 convergence-rate pending live usage data).

**Spec 022 amendment (2026-07-02, IMPLEMENTED)**: Refactor unifying the role-based and EEI dimensions (tasks T032–T057). Delivered: (1) role agents are role-scoped **supervisors** by default (`supervisor: true` + `role-scope:` in all 6 `agent-role-*` templates; OQ-1 default-on); (2) a single-source snippet `skills/internal/create-agent/templates/agent-supervision-delegation.md` inlined by create-agent at generation (OQ-2 compose-in-skill, no copy/drift); (3) `create-agent`/`improve-agent` generalized to a **capability matrix** (role · supervisor · triad · custom) with `AgentAuthoringRequest` intake and target classify/route; (4) `/speckit.agents` Mode A/B **delegate** to the skills (Delegation Model; contract R1). New artifacts: `contracts/agent-authoring-contract.md`; `RoleSupervisor`/`AgentAuthoringRequest` entities in `data-model.md`; supervisor scenario + Amendment Validation Checklist in `quickstart.md`; `skills/internal/create-agent/templates/agent-supervision-delegation.md`. Also mirrored the previously-missing `agent-subrole-*`/`agent-triad-orchestration` templates to `.specify/templates/` (review F4). OQ-1/OQ-2 resolved via `/speckit.clarify`. Follow-up: update `contracts/agent-authoring-contract.md` R2 (superseded dormant-default) and `plan.md` Open Questions on the next `/speckit.plan` regen.

Previous: Spec 015 (role-based-agents): Refactors the agent template approach from capability-based to role-based (Requirements Analyst, System Designer, etc.).

Spec 023 (agent-framework-redesign, Implemented 2026-07-10): Redesigns the Agent framework around a single conceptual model — **Role × Stage × Type** with **Team** (static Role×Stage matrix) and **Loop** (dynamic iteration) structures — keeping `/speckit.agents` as the sole entry (create-agent/organize-agents delegation). Unifies terminology (**SubRole→Stage**, **improver→optimizer**), merges Meta-Coordinator + Team Supervisor into a single **Team Supervisor** (Meta role), canonicalizes templates under `skills/create-agent/templates/` (removing stale `.specify/templates/agent-*` duplicates), migrates persisted agents under `.specify/agents/`, extends persistent-agent tool config to all supported tools, and regenerates `docs/agents`. Also folds in a cross-project research deliverable mining `/cws_work/*` siblings (FR-021). Plan artifacts: `plan.md`, `data-model.md`, `contracts/{conceptual-model,agents-command,template-migration}-contract.md`, `quickstart.md`, `feature-ref.md`.

## Future Evolution Suggestions

- Add support for agent versioning and dependency management
- Implement agent testing framework for validation
- Add agent discovery and recommendation features
- Support agent composition and orchestration patterns

## Related Files

- Feature Index: .specify/features.md
- Feature Detail: .specify/features/019-agents-command.md
- Cross-reference: Feature 057（命令技能化分解补全，`.specify/features/057-decompose-command-skills.md`）——其 US3 对 /speckit.agents 路由表做接线核查（run/create/refine 三行到既有 agent 技能），不新建 agent 系技能。

## Status Tracking

- **Draft**: Initial specification created and validated
- **Planned**: Feature detailed in index and ready for implementation planning
- **Implemented**: Core functionality working with basic agent creation and validation
- **Ready for Review**: Full implementation complete with comprehensive testing
- **Completed**: Feature fully integrated, documented, and stable in production

## Related Specifications/Requirements

- Agents Run Specification: `.specify/specs/104-agents-run/requirements.md`（2026-11-24 `/speckit.clarify` 直接绑定：显式 run 子命令与 superagent/subagent 架构自动接线；019 状态不回退）
- Current Framework Specification: `.specify/specs/023-agent-framework-redesign/requirements.md`
- Historical Specification: `.specify/archive/specs/003-speckit-agents-command/requirements.md`
- Historical EEI Specification: `.specify/archive/specs/022-eei-agent-triad/requirements.md`
- Implementation: `templates/commands/agents.md`, `skills/internal/run-agent/SKILL.md`, `src/specify_cli/__init__.py`
- Consolidation ledger: `.specify/archive/specs/CONSOLIDATION-LEDGER.md`
