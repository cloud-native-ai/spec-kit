# Spec repair — 023-agent-framework-redesign

**Date**: 2026-11-10
**Object**: `.specify/specs/023-agent-framework-redesign/` (live; no archived copy exists under `.specify/archive/specs/`)
**Tree**: main tree `/storage/project/cloud-native-ai/spec-kit`, `master` @ `9ac56bf10`. Other pre-existing uncommitted changes in the tree (e.g. 046, 052, 053, 081, 087, 092, 093, 094) were not touched.
**Inputs**: prior audit `.specify/specs/090-re-anchoring/test-evidence/spec-audit-live-batch-10.md` § 023 (verdict BROKEN; 8 stale-pointer groups, 2 missing guards, 3 anchor-move refs, 7 non-pointer tokens), cross-checks at `spec-audit-003-speckit-agents-command.md` and `spec-audit-022-eei-agent-triad.md`, and the deterministic settled scan `spec-audit-settled.json` (entry `.specify/specs/023-agent-framework-redesign`: `refs 81 / alive 40 / moved 40 / dead 41`; `dead_list` 20 unique paths — the list is capped at 20 while `dead` counts 41 occurrences).
**Mode**: no commit, no push, no subagents. Files changed: `plan.md`, `requirements.md`, `tasks.md`, `quickstart.md`, `feature-ref.md`, `contracts/template-migration-contract.md` (6 files, 42 insertions / 42 deletions). `verification.md` is untouched by design (dated record).

## Counting rule

One count per **path occurrence** = one (artifact, line, concrete path token). Two distinct paths on one line count twice. A reference is **dead** when its target does not exist in the current tree.

Scope union: the settled scan's `dead_list` (all occurrences; the visible list is capped at 20 unique paths), the prior audit's broken-pointer groups, the anchor moves (`.specify/memory/*` → `.specify/` roots), the persisted-agent layer glob (`.specify/agents/*.agent.md` → `{templates,instances}`), and the relocation drift measured against the current tree.

Excluded from the count (consistent with the prior audit's method and the sibling `spec-repair-022-eei-agent-triad.md`): relative sibling links that resolve from the artifact's own directory (`./requirements.md`, `../contracts/...`), elisions (`tests/scenarios/.../team-loop-scenario.md`), bare filename families without a directory prefix (`agent-subrole-*`, `agent-stage-*`, `meta-coordinator` inside grep patterns), and ASCII-diagram bare children whose directory token carries the count.

This occurrence-level rule yields a larger total (122) than the settled scan's dead count (41); the difference is counting granularity, the anchor-move entries the scan classified as `moved`, the layer-glob and regex-fragment drift, and the full external-research Key-files set (37 tokens, of which the capped `dead_list` shows 8).

## Counts

| Dead total (settled scan) | Repair inventory | live-fixed | dated-kept | non-reference |
|---:|---:|---:|---:|---:|
| **41** occurrences (20 unique visible) | **122** | **44** | **31** | **47** |

Artifacts with repairs: `plan.md` (12), `tasks.md` (14), `requirements.md` (7), `quickstart.md` (6), `feature-ref.md` (3), `contracts/template-migration-contract.md` (2).

## Live-fixed (44)

Path repaired to the object's actual current home. No reading, count, quoted output or result value was altered.

### plan.md (12)

| # | Line | Before | After |
|---:|---:|---|---|
| 1 | 8 | `docs/agents` | `docs/reference/agents` |
| 2 | 26 | `.specify/memory/constitution.md` | `.specify/constitution.md` |
| 3 | 31 | `features/019.md` | `.specify/features/019-agents-command.md` |
| 4 | 71 | `skills/improve-agent/SKILL.md` | `skills/internal/improve-agent/SKILL.md` |
| 5 | 72 | `skills/organize-agents/SKILL.md` | `skills/internal/create-team/SKILL.md` |
| 6 | 73 | `docs/agents/` + `eei-triad-pattern.md` + `multi-agent-orchestration.md` | `docs/reference/agents/` + `quality-loop.md` + orchestration guide at `docs/reference/teams/orchestration.md` |
| 7 | 74 | `docs/commands/agents.md` | `docs/reference/commands/agents.md` |
| 8 | 80 | `.specify/memory/features.md` | `.specify/features.md` |
| 9 | 81 | `.specify/memory/features/019.md` | `.specify/features/019-agents-command.md` |
| 10 | 104 | `features/019.md` | `.specify/features/019-agents-command.md` |
| 11 | 117 | `.specify/memory/features/019.md` | `.specify/features/019-agents-command.md` |
| 12 | 117 | `.specify/memory/features.md` | `.specify/features.md` |

Rows 4-5: the skills moved into the `internal/` layer (`1adfa49ab`); `organize-agents` was renamed to `create-team` (recorded in `.specify/features/027-feedback-mechanism.md`: "`create-team` (renamed from `organize-agents`, retaining orchestration + execution)").

Row 6: `docs/agents/` moved to `docs/reference/agents/` (`141dde0e3`, R100); `eei-triad-pattern.md` was renamed to `quality-loop.md` (`a73180759`, R076) and moved with the directory. `multi-agent-orchestration.md` was deleted in `70f00c93d`; its live replacement is the Team Orchestration Guide `docs/reference/teams/orchestration.md` — the archived copy's own final text ("all three modes are entered through the single `/speckit.team` command and executed by the `create-team` skill") matches the live guide's scope, so this is a content successor, not an invented target.

### requirements.md (7)

| # | Line | Before | After |
|---:|---:|---|---|
| 13-18 | 95, 99, 106, 138, 165, 177 | `docs/agents` | `docs/reference/agents` |
| 19 | 179 | `.specify/agents/*.agent.md` | `.specify/agents/{templates,instances}/*.agent.md` |

Row 19 follows the live agent layer: role/supervisor definitions are Templates, executed agents are Instances (`skills/internal/create-agent/SKILL.md` § Layer Targeting).

### tasks.md (14)

| # | Line | Before | After |
|---:|---:|---|---|
| 20 | 24 | `docs/agents/*` (DoD-6) | `docs/reference/agents/*` |
| 21 | 63 | `.specify/memory/features/019.md` (guard exclusion) | `.specify/features/019-agents-command.md` |
| 22 | 112 | `skills/organize-agents/SKILL.md` (T020) | `skills/internal/create-team/SKILL.md` |
| 23 | 126 | `tests/scenarios/multi-agent-orchestration/team-loop-scenario.md` (T021) | `tests/scenarios/multi-agent-orchestration/iteration-scenario.md` |
| 24 | 162 | `docs/agents` (Phase-7 Goal) | `docs/reference/agents` |
| 25 | 164 | `docs/agents/*` (Independent Test) | `docs/reference/agents/*` |
| 26 | 169 | `.specify/skills/organize-agents/**` (T032) | `.specify/skills/internal/create-team/**` |
| 27 | 170 | `docs/agents/eei-triad-pattern.md` (T033) | `docs/reference/agents/quality-loop.md` |
| 28 | 171 | `docs/agents/multi-agent-orchestration.md` (T034) | `docs/reference/teams/orchestration.md` |
| 29 | 186 | `.specify/memory/features.md` (T040) | `.specify/features.md` |
| 30 | 186 | `.specify/memory/features/019.md` (T040) | `.specify/features/019-agents-command.md` |
| 31 | 200 | `create-agent/SKILL.md` (dependency note) | `skills/internal/create-agent/SKILL.md` |
| 32 | 231 | `improve-agent/SKILL.md` (parallel example) | `skills/internal/improve-agent/SKILL.md` |
| 33 | 268 | `features/019.md` (Notes / Decision D5) | `.specify/features/019-agents-command.md` |

Row 23: `team-loop-scenario.md` was renamed to `iteration-scenario.md` (`70f00c93d`, R096).

### quickstart.md (6)

| # | Line | Before | After |
|---:|---:|---|---|
| 34 | 13 | `\|/features/019\.md` (grep exclusion) | `\|/features/019-agents-command\.md` |
| 35 | 16 | `.specify/agents/*.agent.md` | `.specify/agents/{templates,instances}/*.agent.md` |
| 36 | 21 | `skills/create-agent/templates/agent-stage-*.md` | `skills/internal/create-team/templates/agents/agent-stage-*.md` |
| 37 | 22 | `skills/create-agent/templates/agent-role-team-supervisor-template.md` | `skills/internal/create-team/templates/agents/agent-team-supervisor-template.md` |
| 38 | 35 | `\|/features/019\.md` (grep exclusion) | `\|/features/019-agents-command\.md` |
| 39 | 60 | `docs/agents/{design.md,eei-triad-pattern.md,multi-agent-orchestration.md}` | `docs/reference/agents/{design.md,quality-loop.md}` + `docs/reference/teams/orchestration.md` |

Rows 34/38 are executable-check fragments: `.specify/features/019-agents-command.md` still carries 4 historical term lines, so the old exclusion no longer excluded it; the repaired regex excludes the live file.
Rows 36-37: the stage templates and the merged supervisor template moved to the team domain (`027`; live files verified: 3 `agent-stage-*` templates and `agent-team-supervisor-template.md` under `skills/internal/create-team/templates/agents/`).

### feature-ref.md (3)

| # | Line | Before | After |
|---:|---:|---|---|
| 40 | 11 | `.specify/memory/features/019.md` | `.specify/features/019-agents-command.md` |
| 41 | 22 | `.specify/memory/features/019.md` | `.specify/features/019-agents-command.md` |
| 42 | 23 | `.specify/memory/features.md` | `.specify/features.md` |

### contracts/template-migration-contract.md (2)

| # | Line | Before | After |
|---:|---:|---|---|
| 43 | 27 | `features/019.md` (M4 exclusion) | `.specify/features/019-agents-command.md` |
| 44 | 35 | `.specify/agents/*.agent.md` (M6) | `.specify/agents/{templates,instances}/*.agent.md` |

## Dated-kept (31)

Text unchanged. Dates, readings, rename-source names, deleted objects with no live successor, and self-declared history.

### plan.md (4)

| Line | Kept path | Why kept |
|---:|---|---|
| 20 | `docs/agents` | Scale/Scope reading of the plan date ("3 `docs/agents` files") — a dated measurement, not a navigation pointer. |
| 91 | `docs/agents/*` | Phase 0 pre-change footprint measurement ("`subrole`/`improver` appear in ..."); a dated baseline. |
| 100 | `skills/internal/create-agent/templates/agent-role-ux-analyst-template.md` | Superseded-decision annotation stamped `2026-07-10, commit d87dfca9`, self-declared immutable history. Live successor `agent-capacity-ux-analyst-template.md` not substituted (would rewrite the historical annotation). |
| 100 | `.specify/agents/ux-analyst.agent.md` | Same annotation; the persisted agent has no live file today. |

### tasks.md (9)

| Line | Kept path | Why kept |
|---:|---|---|
| 63 | `tests/unit/test_agent_deprecated_terms.py` | Guard test deleted in `cabc9f1e3` ("delete 47 files that cannot fail or whose subject no longer exists"); no live successor. |
| 64 | `tests/unit/test_agent_reference_integrity.py` | Same deletion; no successor. |
| 103 | `.../agent-subrole-executor-template.md` | Rename "from" name (T011) — historical by construction; rewriting it would falsify the rename record. |
| 104 | `.../agent-subrole-evaluator-template.md` | Same (T012). |
| 105 | `.../agent-subrole-improver-template.md` | Same (T013). |
| 106 | `.../agent-role-meta-coordinator-template.md` | Merge-source name (T014); deleted, no live file. |
| 151 | `.specify/agents/{six role agents}.agent.md` | The six persisted role agents (T027) have no live successor after the later agent-layer changes. |
| 183 | `tests/unit/test_agent_deprecated_terms.py` | Dated guard-run record (T037); deleted, no successor. |
| 183 | `tests/unit/test_agent_reference_integrity.py` | Same. |

### verification.md (13)

`verification.md` is the run's measured record (baseline counters, SC values, test readings, dated findings). Left whole by design.

| Line | Kept path |
|---:|---|
| 26 | `.specify/templates/agent-*` (baseline note, 16 files) |
| 38 | `docs/agents/eei-triad-pattern.md` (dated post-change reading) |
| 52 | `tests/unit/test_agent_deprecated_terms.py` (SC-002 reading) |
| 60 | `tests/unit/test_agent_reference_integrity.py` (SC-004 reading) |
| 72 | `docs/agents/{design.md,eei-triad-pattern.md,multi-agent-orchestration.md}` (SC-007 value) |
| 73 | `docs/agents` (SC-007 note) |
| 80 | `.specify/agents/*.agent.md` (SC-009 value) |
| 94 | `team-loop-scenario.md` (T021 finding) |
| 97 | `agent-parallel/serial-orchestration-template.md` (T024 finding) |
| 104 | `create-agent/SKILL.md` (T029 finding) |
| 107 | `/cws_work/spec-kit/.specify/agents` (recorded link-resolution value) |
| 111 | `tests/unit/test_agent_deprecated_terms.py`, `tests/unit/test_agent_reference_integrity.py` (test_guards reading) |

### data-model.md (5)

Line 113, "Migration targets outside templates" — the migration-map record of where the 2026-07-10 change was applied: `create-agent/SKILL.md`, `improve-agent/SKILL.md`, `organize-agents/SKILL.md`, `docs/agents/*`, `.specify/agents/*.agent.md`. A migration map is historical by construction (the old→new table above it uses the same old names); re-pointing it would misstate where the migration applied.

## Non-reference (47)

Not repository references; ignored and left unchanged.

### research.md — external sibling-project Key files (37)

| Line | Tokens (belong to the cited `/cws_work/*` project, not this repo) |
|---:|---|
| 21, 30, 39, 48, 57, 67, 76 | `cws_work/OpenSpec`, `cws_work/superpowers`, `cws_work/claw-code-agent`, `cws_work/intellegix-code-agent-toolkit`, `cws_work/claude-code-ts`, `cws_work/claude-code-py`, `cws_work/learn-claude-code` |
| 28 | `docs/agent-contract.md`, `docs/concepts.md`, `docs/customization.md`, `src/cli/index.ts` |
| 37 | `hooks/session-start`, `skills/subagent-driven-development/SKILL.md`, `skills/dispatching-parallel-agents/SKILL.md`, `.opencode/plugins/superpowers.js` |
| 42, 52, 102 | `.port_sessions/agent`, `.workflow/state.json` (×2) |
| 46 | `src/main.py`, `src/builtin_agents.py`, `src/agent_registry.py`, `src/session_store.py`, `src/agent_manager.py` |
| 55 | `agents/orchestrator.md`, `commands/orchestrator-multi.md`, `automated-loop/loop_driver.py`, `automated-loop/state_tracker.py`, `hooks/orchestrator-guard.py` |
| 65 | `src/Task.ts`, `src/skills/loadSkillsDir.ts`, `src/coordinator/coordinatorMode.ts`, `src/coordinator/workerAgent.ts`, `src/workflow/persistence.ts`, `docs/agent/coordinator-and-swarm.mdx` |
| 74 | `.claude-plugin/marketplace.json`, `plugins/README.md`, `commands/review-pr.md` |

### Prose fragments / slash-words (4)

| File:line | Token | Reason |
|---|---|---|
| requirements.md:130 | `skills/other` | Prose ("optimize skills/other agents"), not a path. |
| plan.md:12 | `templates/skills/docs/commands` | Prose slash-word sequence naming artifact kinds. |
| quickstart.md:49 | `.md/.prompt.md` | Prose extension list. |
| verification.md:48 | `.md/.prompt.md` | Prose extension list (dated reading line). |

### Intended-absence globs (6)

| File:line | Token | Reason |
|---|---|---|
| plan.md:84, 90, 102 | `.specify/templates/agent-*` | Describes the legacy duplicate set that MUST be removed (D3 / FR-013). Absence is the intended outcome. |
| tasks.md:168 | `.specify/templates/agent-*` | T031 removal target; absence is the completion proof. |
| data-model.md:111 | `.specify/templates/agent-*` | Migration-map row "(removed)". |
| contracts/template-migration-contract.md:9 | `.specify/templates/agent-*` | Normative rule "MUST be removed". |

## Settled `dead_list` coverage (20/20)

| dead_list entry | Disposition |
|---|---|
| `tests/scenarios/multi-agent-orchestration/team-loop-scenario.md` | live-fixed #23; dated-kept verification:94 |
| `src/session_store.py` | non-reference (claw-code-agent, research:46) |
| `skills/internal/create-agent/templates/agent-subrole-evaluator-template.md` | dated-kept tasks:104 (rename source) |
| `docs/agents/` | live-fixed #1, 6, 13-18, 20, 24-25, 27-28, 39; dated-kept plan:20, 91, verification:38, 72, 73, data-model:113 |
| `skills/dispatching-parallel-agents/SKILL.md` | non-reference (superpowers, research:37) |
| `docs/customization.md` | non-reference (OpenSpec, research:28) |
| `docs/agents/multi-agent-orchestration.md` | live-fixed #6, 28, 39 |
| `skills/create-agent/templates/agent-role-team-supervisor-template.md` | live-fixed #37 |
| `src/agent_registry.py` | non-reference (claw-code-agent, research:46) |
| `skills/internal/create-agent/templates/agent-subrole-improver-template.md` | dated-kept tasks:105 (rename source) |
| `skills/create-agent/templates/agent-stage-` | live-fixed #36 |
| `skills/other` | non-reference (prose, requirements:130) |
| `tests/unit/test_agent_reference_integrity.py` | dated-kept tasks:64, 183, verification:60, 111 |
| `docs/agent-contract.md` | non-reference (OpenSpec, research:28) |
| `docs/agent/coordinator-and-swarm.mdx` | non-reference (claude-code-ts, research:65) |
| `.specify/templates/agent-` | non-reference (6 intended-absence globs); dated-kept verification:26 |
| `src/coordinator/workerAgent.ts` | non-reference (claude-code-ts, research:65) |
| `src/skills/loadSkillsDir.ts` | non-reference (claude-code-ts, research:65) |
| `skills/improve-agent/SKILL.md` | live-fixed #4 |
| `src/Task.ts` | non-reference (claude-code-ts, research:65) |

## Target verification

Every repaired target was resolved against the current tree after the edits:

- `.specify/constitution.md`, `.specify/features.md`, `.specify/features/019-agents-command.md` — exist at the anchor root / feature-detail layer.
- `skills/internal/improve-agent/SKILL.md`, `skills/internal/create-team/SKILL.md`, `skills/internal/create-agent/SKILL.md` — exist.
- `skills/internal/create-team/templates/agents/{agent-stage-executor,agent-stage-evaluator,agent-stage-optimizer,agent-team-supervisor}-template.md` — 4 files present; `.specify/skills/internal/create-team/templates/agents/` mirror present.
- `.specify/skills/internal/create-team/**` — installed mirror present.
- `docs/reference/agents/{design.md,quality-loop.md}`, `docs/reference/teams/orchestration.md`, `docs/reference/commands/agents.md` — exist.
- `tests/scenarios/multi-agent-orchestration/iteration-scenario.md` — exists.
- `.specify/agents/{templates,instances}/` — both present (17 templates, 3 instances).

## Validator readings

Commands (from the repo root):

```
python3 .specify/scripts/python/validate-requirements.py .specify/specs/023-agent-framework-redesign/requirements.md
python3 .specify/scripts/python/validate-tasks.py .specify/specs/023-agent-framework-redesign/tasks.md
```

**validate-requirements.py — exit 1**:

```
file: .specify/specs/023-agent-framework-redesign/requirements.md
status: error
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] fail (8)
  [marker-count] pass (0)
  [dup-id] pass (0)
  [path-marker] pass (0)
scanned: 210 lines, 30 definition rows, 8 shared strings
8 error(s), 0 warning(s)
```

The 8 `ref-resolvable` errors are pre-existing Shared-Strings drift (lines 193-198): `Consumed by` cells name FR-014/FR-015/FR-004/FR-007/FR-009/FR-016 while those FR rows re-type the literal instead of citing `[[STR-00x]]`. They are unrelated to path repair.

**validate-tasks.py — exit 0**:

```
PASS (with warnings): .specify/specs/023-agent-framework-redesign/tasks.md — 0 error(s), 6 warning(s)
```

The 6 `parallel-safe` warnings (T010/T017, T011/T012, T011/T015, T012/T015, T023/T024, T026/T027) are pre-existing task-decomposition warnings unrelated to path repair.

Before/after identity check: the HEAD versions of both files were re-validated from `.specify/.tmp/` and the reports diffed after normalizing the `file:` path lines — **IDENTICAL** verdicts and identical message sets (same 8 `ref-resolvable` errors, same 6 `parallel-safe` warnings). The repair changed no validator verdict; the pre-existing failure set is the baseline, not a regression. (Temp scratch removed after the reading.)

## Notes

- No target was invented: every after-path names an object that exists now. Objects with no live successor (guard tests deleted in `cabc9f1e3`, the six persisted role agents, the rename-source template names, the superseded UX-analyst annotation) were kept, not re-pointed.
- `docs/concepts.md` at `research.md:28` and the other external sibling-project paths are third-party references; the subagent-collision check (`research.md:102`) and other script paths inside that report remain as written.
- Registry: spec 023 is **live**, and its own binder row **019 (Agents Command)** resolves — Details `.specify/features/019-agents-command.md` exists, Spec Path `.specify/specs/023-agent-framework-redesign/requirements.md` exists. No registry edit was needed. The prior audit's separate anomaly — row **023 (Prompt Template Quality, Draft)** pointing its Details cell at `.specify/features/023-agent-framework-redesign.md`, whose content title is "Prompt Template Quality" — is a different feature's row, outside this spec's repair scope; left untouched.
- `verification.md` and the dated readings inside `plan.md` / `tasks.md` / `data-model.md` were deliberately not rewritten: dates are records, not navigation.
