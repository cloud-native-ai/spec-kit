# Read-only spec audit — 022-eei-agent-triad (batch 5)

**Audit date**: 2026-11-10
**Audited object**: `.specify/archive/specs/022-eei-agent-triad/` (10 artifacts: requirements, plan, tasks, data-model, verification, quickstart, checklists/requirements, contracts/triad-protocol, contracts/agent-authoring-contract, review)
**Tree audited**: working tree at `HEAD 564a5f5a6` (branch `master`) — pre-existing uncommitted changes were present and were not touched
**Mode**: read-only; no spec/source edits, no subagents, no commits. This file is the only write.

## Scope & method

Every repository path token in the 10 artifacts was extracted (prefixes `.specify/`, `templates/`, `skills/`, `scripts/`, `shared/`, `tests/`, `docs/`, `agents/`, `.claude/`), deduplicated per artifact, then resolved against the current tree with filesystem checks, `find`, and git history.

Counting rule: one count per `(artifact, canonical path token)`; brace-expansion groups count once; directory-relative links count once; directory-only references count once. Excluded as prose, not paths: `templates/prompts` (plan.md:222), `templates/skills` (verification.md:59), `templates/skills/command` (quickstart.md:142), `templates/commands/scripts` (review.md:23), and placeholder-only tokens.

Classification: **alive** = the target exists now (including renamed/relocated objects), **archived-elsewhere** = target resolves only inside an archive, **dead** = no target (per instruction, a stale pre-archive `.specify/specs/022-eei-agent-triad/...` path counts as dead).

## Counts

| Artifact | Refs | Alive | Archived-elsewhere | Dead |
|---|---:|---:|---:|---:|
| requirements.md | 0 | 0 | 0 | 0 |
| plan.md | 24 | 22 | 0 | 2 |
| tasks.md | 35 | 29 | 0 | 6 |
| data-model.md | 1 | 1 | 0 | 0 |
| verification.md | 1 | 1 | 0 | 0 |
| quickstart.md | 9 | 7 | 1 | 1 |
| checklists/requirements.md | 2 | 0 | 1 | 1 |
| contracts/triad-protocol.md | 0 | 0 | 0 | 0 |
| contracts/agent-authoring-contract.md | 5 | 4 | 1 | 0 |
| review.md | 31 | 20 | 0 | 11 |
| **Total** | **108** | **84** | **3** | **21** |

## Alive-with-drift (object survived under a renamed/relocated path)

The implementation was re-laid-out by `ec458611b` (2026-07-09, "add agent skills") and `bc8eaba53` (2026-07-10, 023-agent-framework-redesign). These targets are alive but no longer at the cited path:

| Cited path | Current home |
|---|---|
| `templates/agent-role-*-template.md` (6 named files, tasks.md:44,198-203) | `skills/internal/create-agent/templates/agent-capacity-<slug>-template.md` (now 7 files — `ux-analyst` added), mirrored under `.specify/skills/internal/create-agent/templates/` |
| `templates/agent-subrole-{executor,evaluator,improver}-template.md` (tasks.md:52-54,76-78) | `skills/internal/create-team/templates/agents/agent-stage-{executor,evaluator,optimizer}-template.md`; "Improver" → "Optimizer" (023 FR-014) |
| `templates/agent-triad-orchestration-template.md` (plan.md:68,189) | `skills/internal/create-team/templates/agents/agent-triad-orchestration-template.md` |
| `.specify/templates/agent-role-*`, `.specify/templates/agent-subrole-*`, `.specify/templates/agent-triad-*` (plan.md:237-239, tasks.md:184, review.md:144) | No agent templates remain under `.specify/templates/`; runtime mirrors live beside the skills (`.specify/skills/internal/create-agent/templates/`, `.specify/skills/internal/create-team/templates/agents/`) |
| `skills/create-agent/SKILL.md`, `skills/improve-agent/SKILL.md` (review.md:150-151) | `skills/internal/create-agent/SKILL.md`, `skills/internal/improve-agent/SKILL.md` |
| `docs/git-workflow.md` (review.md:175,234,244) | `.specify/workflow/git.md` |
| `scripts/bash/sync-runtime.sh` (review.md:157,233,243 — a proposal, never created) | Capability exists as `scripts/python/sync-mirrors.py` (`--check`/`--write`) |
| `.specify/agents/*.agent.md` (plan.md:178, contract:56, tasks.md:219) | `.specify/agents/{templates,instances}/<name>.agent.md` |
| `templates/commands/agents.md` "Mode A / Mode B" (plan.md:180, tasks.md:226-228, quickstart.md:160-161) | Single intent-routing table (create / refine / run / empty) at `templates/commands/agents.md:25-33`; no Mode A/B structure remains |
| `.gitignore#L40` (review.md:75) | `.gitignore` alive; the `*.log` rule is now at line 37 |

Metadata-key drift: the spec's `role-scope:` frontmatter key is now `capacity-scope:` (verified on all 7 `agent-capacity-*` templates); `{{ROLE_SCOPE}}` survives inside the orchestration template.

## Broken list

21 dead reference instances (13 distinct targets):

- `plan.md:4` `.specify/specs/022-eei-agent-triad/requirements.md` → dead; the spec now lives at `.specify/archive/specs/022-eei-agent-triad/requirements.md`
- `plan.md:47,197` `.specify/specs/022-eei-agent-triad/` → dead (stale pre-archive dir)
- `tasks.md:6` `.specify/specs/022-eei-agent-triad/` → dead
- `tasks.md:184` `.specify/specs/022-eei-agent-triad/plan.md` → dead
- `tasks.md:197,209,218,225` `.specify/specs/022-eei-agent-triad/quickstart.md` → dead
- `checklists/requirements.md:5` `.specify/specs/022-eei-agent-triad/requirements.md` → dead (the sibling `../requirements.md` still resolves in the archive)
- `review.md:29-36` artifact inventory (8 paths: requirements, plan, tasks, data-model, contracts/triad-protocol, quickstart, checklists/requirements, verification) → all dead as `.specify/specs/...`; each file exists in the archive
- `tasks.md:63` `tests/contract/test_triad_orchestration_template.py` → missing; never created (T008 left `[~]`)
- `tasks.md:68` `tests/integration/test_eei_triad_loop.py` → missing; never created (T013 left `[~]`)
- `tasks.md:117` + `review.md:47` `docs/eei-triad-pattern.md` → missing; deleted by `bc8eaba5` with no replacement file (the narrative survives at `docs/reference/history/01-agent-system-evolution.md:62` and `skills/internal/create-team/references/conceptual-model.md`, but DoD-6/T029's "reference guide" object has no target)
- `quickstart.md:106` `.specify/agents/system-designer.agent.md` → missing; illustrative Scenario-4 output, never committed (no `system-designer.agent.md` exists anywhere in the tree)
- `review.md:49,170` `skills/draw-plantuml/SKILL.md` → missing; the draw-plantuml skill was removed
- `review.md:168` `.specify/skills/draw-plantuml/SKILL.md` → missing

Archived-elsewhere (3): `quickstart.md:153` `contracts/agent-authoring-contract.md`, `checklists/requirements.md:5` `../requirements.md`, `contracts/agent-authoring-contract.md:3` `triad-protocol.md` — all resolve inside `.specify/archive/specs/022-eei-agent-triad/`.

## Ledger-target check

Ledger row: `.specify/archive/specs/CONSOLIDATION-LEDGER.md:14` — `022-eei-agent-triad | archive | Feature 019 child (retired EEI vocabulary) | review-G2`.

- **Archive target resolves**: `.specify/archive/specs/022-eei-agent-triad/` exists with all 10 artifacts.
- **Feature/spec target resolves**: `.specify/memory/features.md:28` row `019 | Agents Command | … | Implemented` exists; detail file `.specify/memory/features/019.md` exists and records spec 022 at lines 51/53/55 plus the 2026-11-09 consolidation at line 97. `.specify/archive/specs/022-eei-agent-triad/requirements.md:10-11` confirms the binding (Feature ID 019).
- **Registry row**: no `022-eei-agent-triad` entry exists in `.specify/memory/register.md`; the ledger does not claim one, so this is not a defect. The numeric row `022` in `features.md` is a different feature ("AI Tools Support"); the ledger's by-reference binding to Feature 019 is what keeps the entry unambiguous (same pattern as the 003 row).
- **Accuracy caveat (non-blocking)**: the note "retired EEI vocabulary" is inexact. 023 renamed *Improver* → *Optimizer* and expanded the acronym (`.specify/specs/023-agent-framework-redesign/verification.md:102-103`), but "EEI" remains in live surfaces (`create-agent` SKILL.md:12,160-176; `create-team` SKILL.md:206; all three stage templates; the supervision snippet's "Executor-Evaluator-Optimizer (EEI)"). Suggested wording: "renamed Improver→Optimizer; EEI retained as Executor-Evaluator-Optimizer". The ledger row itself (verdict `archive`, reference target `Feature 019 child`) is otherwise accurate.

## Missing guards

Named by the spec, absent from the tree:

- `tests/contract/test_triad_orchestration_template.py` (T008) — missing.
- `tests/integration/test_eei_triad_loop.py` (T013) — missing.

Both were explicitly deferred (`[~]`) in `tasks.md` and `verification.md:50`, so the absence is recorded, not silent. Successor coverage that does exist:

- `tests/contract/test_role_templates.py` — structural validation of the 7 capacity templates (required sections + approved placeholders).
- `tests/scenarios/conceptual-model/role-stage-type-conformance-scenario.md` — records the `agent-subrole-*` → `agent-stage-*` / improver → optimizer rename.
- `tests/contract/test_single_agent_purity.py` — **contradicts** the spec: it asserts create-agent must not list a `triad` mode and improve-agent must not contain "Triad Refinement" (see anomaly).
- No guard asserts the supervision single-source or the `supervisor: true` / `capacity-scope:` frontmatter, so DoD-8's structural validation is currently unguarded.

## Three spot-checks

1. **File** — `skills/internal/create-agent/templates/agent-supervision-delegation.md` (claimed by tasks.md:190/DoD-8, T045). Present; headings include `## Supervision & EEI Delegation`; the `.specify/skills/...` twin is byte-identical; `skills/internal/create-agent/SKILL.md:176` names it as the only editable source of the delegation text. **PASS.**
2. **Symbol** — `{{ROLE_SCOPE}}` binding in `skills/internal/create-team/templates/agents/agent-triad-orchestration-template.md` (claimed by tasks.md:191/DoD-9). Present at lines 10 and 21; companions `{{SCORING_DIMENSIONS}}` (19), `{{THRESHOLD}}` (12), `{{MAX_ITERATIONS}}` (13), `{{MAX_REGRESSIONS}}` (14) all present. **PASS**, with vocabulary drift (workspace paths now `{{OPTIMIZER_WORKSPACE_PATHS}}` / `.specify/teams/.work/{{TEAM_SLUG}}/`).
3. **Behaviour surface** — `/speckit.agents` delegates to `create-agent`/`improve-agent` with no inline template rendering (contract R1, T050-T052). Confirmed: `templates/commands/agents.md:25` ("does not render any operation inline"), `:32` routes create to `.specify/skills/internal/create-agent/SKILL.md`, `:33` routes refine to `improve-agent`; `.claude/commands/speckit.agents.md` differs only by the auto-generated header and `shared/` → `.specify/shared/` prefixes (`scripts/python/regen-command-copies.py`). **PASS**, but Mode A/B is gone and the `triad` kind/Triad Refinement are now forbidden (see anomaly).

## References that will move under the pending anchor-layout rename

The `rename-anchors` worktree (`.specify/.tmp/sdd-loop/worktrees/rename-anchors/`) promotes `memory/` anchors to the `.specify/` root. These live references will move:

- `.specify/memory/constitution.md` (plan.md:28,158) → `.specify/constitution.md`
- `.specify/memory/features.md` (tasks.md:5,236) → `.specify/features.md`
- `.specify/memory/features/019.md` (tasks.md:119,236) → `.specify/features/019.md`

The record stores (`.specify/memory/{session,knowledge,feedback,…}`) stay under `memory/` in that layout.

## Verdict

**BROKEN.**

The archived spec set itself is complete, and 84/108 references still resolve (most after a rename/relocation). But 21 references are dead against the current tree — the stale pre-archive spec paths, the deleted `docs/eei-triad-pattern.md`, two named test guards that were never created, an illustrative agent output that was never committed, and the removed draw-plantuml skill — and one implementation claim (DoD-10's `triad` capability / DoD-11's Triad Refinement) is now actively contradicted by a live guard rather than merely relocated.

Anomaly: DoD-10/DoD-11's `triad` capability and "Triad Refinement" are not just renamed — `tests/contract/test_single_agent_purity.py:48-62` asserts both are absent from `skills/internal/create-agent|improve-agent/SKILL.md`, so the spec's stated implementation is now forbidden by a live guard.

SPEC-AUDIT-5-DONE
