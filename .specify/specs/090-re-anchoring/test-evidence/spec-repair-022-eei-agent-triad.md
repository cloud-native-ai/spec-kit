# Spec repair — 022-eei-agent-triad

**Date**: 2026-11-10
**Object**: `.specify/archive/specs/022-eei-agent-triad/` (archived; no live `.specify/specs/022-eei-agent-triad/` exists)
**Tree**: main tree `/storage/project/cloud-native-ai/spec-kit`, `master` @ `9ac56bf10`. Other pre-existing uncommitted changes in the tree (e.g. 046, 052) were not touched.
**Inputs**: prior audit `.specify/specs/090-re-anchoring/test-evidence/spec-audit-022-eei-agent-triad.md` (verdict BROKEN; its line-level broken list) and the deterministic settled scan `.specify/specs/090-re-anchoring/test-evidence/spec-audit-settled.json` (entry `.specify/archive/specs/022-eei-agent-triad`: `refs 57 / alive 28 / moved 28 / dead 29`, `dead_list` 20 tokens).
**Mode**: no commit, no push, no subagents. Files changed: `plan.md`, `tasks.md`, `quickstart.md`, `checklists/requirements.md`, `contracts/agent-authoring-contract.md` (5 files, 37 insertions / 37 deletions). `review.md` and `verification.md` are untouched by design (dated records).

## Counting rule

One count per **path occurrence** = one (artifact, line, concrete repository path token). Two distinct paths on one line count twice. A reference is **dead** when its target does not exist in the current tree.

Scope union: the prior audit's broken list (21 instances / 13 distinct targets under its per-artifact dedupe), the settled scan's `dead_list`, the anchor moves (`memory/` → `.specify/` roots), and the relocation drift measured against the current tree. The settled `dead_list` is truncated at 20 entries (`dead` is 29), so the line-level audit plus a fresh tree resolution were used to complete it.

Excluded from the count (consistent with the prior audit's method): bare filename children inside ASCII tree diagrams (`plan.md:65-68,77,188` — structural diagrams, whose `templates/` root is alive), name-family prose without a directory prefix (`agent-subrole-*`, `agent-triad-orchestration-*`), and relative sibling links that resolve inside the archive (`quickstart.md` → `contracts/agent-authoring-contract.md`, `contracts/agent-authoring-contract.md:3` → `triad-protocol.md`).

This occurrence-level rule yields a larger total (90) than the audit's deduped count (21); the difference is counting granularity plus the anchor-move and relocation entries the audit had classified separately as "alive-with-drift".

## Counts

| Dead total | live-fixed | dated-kept | non-reference |
|---:|---:|---:|---:|
| **90** | **45** | **40** | **5** |

Artifacts with repairs: `plan.md` (11 fixed), `tasks.md` (31 fixed), `quickstart.md` (1), `checklists/requirements.md` (1), `contracts/agent-authoring-contract.md` (1).

## Live-fixed (45)

Path repaired to the object's actual current home. No reading, count, quoted output or result value was altered.

### plan.md (11)

| # | Line | Before | After |
|---:|---:|---|---|
| 1 | 4 | `.specify/specs/022-eei-agent-triad/requirements.md` | `.specify/archive/specs/022-eei-agent-triad/requirements.md` |
| 2 | 15 | `templates/agent-role-*-template.md` | `skills/internal/create-agent/templates/agent-capacity-*-template.md` |
| 3 | 28 | `.specify/memory/constitution.md` | `.specify/constitution.md` |
| 4 | 47 | `.specify/specs/022-eei-agent-triad/` | `.specify/archive/specs/022-eei-agent-triad/` |
| 5 | 158 | `.specify/memory/constitution.md` | `.specify/constitution.md` |
| 6 | 178 | `.specify/agents/*.agent.md` | `.specify/agents/{templates,instances}/*.agent.md` |
| 7 | 197 | `.specify/specs/022-eei-agent-triad/` | `.specify/archive/specs/022-eei-agent-triad/` |
| 8 | 237 | `templates/agent-role-*-template.md` | `skills/internal/create-agent/templates/agent-capacity-*-template.md` |
| 9 | 237 | `.specify/templates/agent-role-*-template.md` | `.specify/skills/internal/create-agent/templates/agent-capacity-*-template.md` |
| 10 | 239 | `templates/agent-subrole-*-template.md` | `skills/internal/create-team/templates/agents/agent-stage-*-template.md` |
| 11 | 239 | `.specify/templates/agent-subrole-*-template.md` | `.specify/skills/internal/create-team/templates/agents/agent-stage-*-template.md` |

Rows 8-11 are the runtime mirror map: the source moved from root `templates/` into the owning skills (`ec458611b`, `bc8eaba53`), and the mirror moved with it.

### tasks.md (31)

| # | Line | Before | After |
|---:|---:|---|---|
| 12 | 5 | `.specify/memory/features.md` | `.specify/features.md` |
| 13 | 6 | `.specify/specs/022-eei-agent-triad/` | `.specify/archive/specs/022-eei-agent-triad/` |
| 14 | 44 | `templates/agent-role-system-designer-template.md` | `skills/internal/create-agent/templates/agent-capacity-system-designer-template.md` |
| 15 | 52 | `templates/agent-subrole-executor-template.md` | `skills/internal/create-team/templates/agents/agent-stage-executor-template.md` |
| 16 | 53 | `templates/agent-subrole-evaluator-template.md` | `skills/internal/create-team/templates/agents/agent-stage-evaluator-template.md` |
| 17 | 54 | `templates/agent-subrole-improver-template.md` | `skills/internal/create-team/templates/agents/agent-stage-optimizer-template.md` |
| 18 | 76 | `templates/agent-subrole-executor-template.md` | `skills/internal/create-team/templates/agents/agent-stage-executor-template.md` |
| 19 | 77 | `templates/agent-subrole-evaluator-template.md` | `skills/internal/create-team/templates/agents/agent-stage-evaluator-template.md` |
| 20 | 78 | `templates/agent-subrole-improver-template.md` | `skills/internal/create-team/templates/agents/agent-stage-optimizer-template.md` |
| 21 | 119 | `.specify/memory/features/019.md` | `.specify/features/019-agents-command.md` |
| 22 | 168 | `templates/agent-role-*-template.md` | `skills/internal/create-agent/templates/agent-capacity-*-template.md` |
| 23 | 184 | `.specify/specs/022-eei-agent-triad/plan.md` | `.specify/archive/specs/022-eei-agent-triad/plan.md` |
| 24 | 184 | `templates/agent-role-*` | `skills/internal/create-agent/templates/agent-capacity-*` |
| 25 | 184 | `.specify/templates/agent-role-*` | `.specify/skills/internal/create-agent/templates/agent-capacity-*` |
| 26 | 184 | `skills/{create,improve}-agent/SKILL.md` | `skills/internal/{create-agent,improve-agent}/SKILL.md` |
| 27 | 197 | `.specify/specs/022-eei-agent-triad/quickstart.md` | `.specify/archive/specs/022-eei-agent-triad/quickstart.md` |
| 28 | 198 | `templates/agent-role-system-designer-template.md` | `skills/internal/create-agent/templates/agent-capacity-system-designer-template.md` |
| 29 | 198 | `.specify/templates/agent-role-system-designer-template.md` | `.specify/skills/internal/create-agent/templates/agent-capacity-system-designer-template.md` |
| 30 | 199 | `templates/agent-role-requirements-analyst-template.md` | `skills/internal/create-agent/templates/agent-capacity-requirements-analyst-template.md` |
| 31 | 200 | `templates/agent-role-module-designer-template.md` | `skills/internal/create-agent/templates/agent-capacity-module-designer-template.md` |
| 32 | 201 | `templates/agent-role-test-engineer-template.md` | `skills/internal/create-agent/templates/agent-capacity-test-engineer-template.md` |
| 33 | 202 | `templates/agent-role-qa-engineer-template.md` | `skills/internal/create-agent/templates/agent-capacity-qa-engineer-template.md` |
| 34 | 203 | `templates/agent-role-knowledge-manager-template.md` | `skills/internal/create-agent/templates/agent-capacity-knowledge-manager-template.md` |
| 35 | 209 | `.specify/specs/022-eei-agent-triad/quickstart.md` | `.specify/archive/specs/022-eei-agent-triad/quickstart.md` |
| 36 | 218 | `.specify/specs/022-eei-agent-triad/quickstart.md` | `.specify/archive/specs/022-eei-agent-triad/quickstart.md` |
| 37 | 219 | `templates/agent-role-*` | `skills/internal/create-agent/templates/agent-capacity-*` |
| 38 | 219 | `.specify/agents/*.agent.md` | `.specify/agents/{templates,instances}/*.agent.md` |
| 39 | 225 | `.specify/specs/022-eei-agent-triad/quickstart.md` | `.specify/archive/specs/022-eei-agent-triad/quickstart.md` |
| 40 | 235 | `.specify/agents/<role>.agent.md` | `.specify/agents/templates/<role>.agent.md` |
| 41 | 236 | `.specify/memory/features/019.md` | `.specify/features/019-agents-command.md` |
| 42 | 236 | `.specify/memory/features.md` | `.specify/features.md` |

Rename note for rows 15-20 and 30-34: the 023 redesign renamed the sub-role stage family (`executor`, `evaluator`, `improver` → `executor`, `evaluator`, `optimizer`) and the role family (`agent-role-*` → `agent-capacity-*`); the after paths name the live objects. Row 40 follows the live layer rule: a role/supervisor definition is a Template, so it is written to `.specify/agents/templates/<name>.agent.md` (create-agent skill § Layer Targeting).

### quickstart.md (1)

| # | Line | Before | After |
|---:|---:|---|---|
| 43 | 145 | `templates/agent-role-*-template.md` | `skills/internal/create-agent/templates/agent-capacity-*-template.md` |

### checklists/requirements.md (1)

| # | Line | Before | After |
|---:|---:|---|---|
| 44 | 5 | `.specify/specs/022-eei-agent-triad/requirements.md` (display text; link target `../requirements.md` already resolved) | `.specify/archive/specs/022-eei-agent-triad/requirements.md` |

### contracts/agent-authoring-contract.md (1)

| # | Line | Before | After |
|---:|---:|---|---|
| 45 | 56 | `.specify/agents/*.agent.md` | `.specify/agents/{templates,instances}/*.agent.md` |

## Dated-kept (40)

Text unchanged. These are dated records or dated design statements, not current navigation pointers.

### plan.md (5)

| Line | Kept path | Why kept |
|---:|---|---|
| 143 | `templates/agent-role-*-template.md` | Evidence table explicitly stamped "current state @ commit 0bf2a9a" — a dated snapshot. |
| 145 | `templates/agent-role-*-template.md` | Inside a quoted historical goal string in the same dated evidence table. |
| 152 | `templates/agent-role-*-template.md` | "Technical Context (delta)" of the dated amendment; the role-template edit was later superseded by the in-document OQ-2 resolution (`plan.md:229`: role templates are NOT edited to contain the section). |
| 174 | `templates/agent-role-*-template.md` | D1 of the dated amendment, likewise superseded by the OQ-2 resolution recorded at `plan.md:229`. |
| 178 | `templates/agent-role-*` | Past-state description ("from *only* `templates/agent-role-*`"); the same line's live-pointer token `.specify/agents/*.agent.md` was fixed (row 6). |

### review.md (31)

`review.md` is a dated process-review report (Review Date 2026-07-02, snapshot commit `0bf2a9a`, Section 7 declares its paths a self-contained snapshot). Its inventory records line counts of that snapshot (e.g. plan.md 120 lines, tasks.md 149 lines — the archived files are 243 / 264 today), so re-pointing the paths would assert the later archived versions were the reviewed ones. Left whole.

| Lines | Kept path(s) | Why kept |
|---:|---|---|
| 29-36 | 8 artifact-inventory paths `.specify/specs/022-eei-agent-triad/...` | Dated review snapshot with dated line-count readings. |
| 47 | `templates/agent-subrole-{executor,evaluator,improver}-template.md`; `docs/eei-triad-pattern.md` | Timeline row recording what the implement run created (dated observation). |
| 49 | `skills/draw-plantuml/SKILL.md` | Dated observation of the feature commit's bundled files. |
| 95 (2), 118, 181, 197 | `.specify/specs/022-eei-agent-triad/{tasks,plan,verification}.md` | Finding "Location" fields of the dated report. |
| 144 (2), 145, 146 | `.specify/templates/agent-subrole-*.md`, `.specify/templates/agent-triad-*.md` | Verbatim quoted `ls` output (evidence for F4) — quoted evidence is never rewritten. |
| 150, 151, 152 | `skills/create-agent/SKILL.md`, `skills/improve-agent/SKILL.md`, `templates/agent-subrole-executor-template.md` | Verbatim quoted `git show --stat` output (evidence for F4). |
| 157, 233, 243 | `scripts/bash/sync-runtime.sh` | Proposal target of a dated recommendation; never created. The capability it asked for landed as `scripts/python/sync-mirrors.py` (`--check`/`--write`), but rewriting a proposal's target would rewrite the proposal. |
| 168, 170 | `.specify/skills/draw-plantuml/SKILL.md`, `skills/draw-plantuml/SKILL.md` | F5 "Location"/quoted evidence of the dated feature commit; the skill has since been removed. |
| 175, 234, 244 | `docs/git-workflow.md` | Recommendation target of the dated report; the live owner is `.specify/workflow/git.md`, but the report records what was recommended then. |

### tasks.md (4)

| Line | Kept path | Why kept |
|---:|---|---|
| 63 | `tests/contract/test_triad_orchestration_template.py` | Completed-task record of a deferred task (`[~] T008`); the file was never created and has no live successor. |
| 68 | `tests/integration/test_eei_triad_loop.py` | Same: `[~] T013`, never created, no live successor. |
| 117 | `docs/eei-triad-pattern.md` | Completed-task record (`T029`); the file was later deleted with no replacement object. The narrative survives at `docs/reference/history/01-agent-system-evolution.md` and `skills/internal/create-team/references/conceptual-model.md`, but those are not the guide the task asked for — naming them would invent a target. |
| 232 | `docs/eei-triad-pattern.md` | Same object on the amendment task `T053`; same reason. |

## Non-reference (5)

Not resolvable repository references; ignored and left unchanged.

| File:line | Token | Reason |
|---|---|---|
| plan.md:222 | `templates/prompts` | Prose fragment ("Markdown templates/prompts"), not a path. |
| quickstart.md:106 | `.specify/agents/system-designer.agent.md` | Illustrative Scenario-4 output that was never committed; the scenario remains an example, not a pointer. |
| quickstart.md:142 | `templates/skills/command` | Prose fragment ("templates/skills/command feature"), not a path. |
| review.md:23 | `templates/commands/scripts` | Prose fragment ("reviewed templates/commands/scripts"), not a path. |
| verification.md:59 | `templates/skills` | Prose fragment, not a path. |

## Target verification

Every repaired target was resolved against the current tree after the edits (glob hits in parentheses):

- `skills/internal/create-agent/templates/agent-capacity-*-template.md` (7) and `.specify/skills/internal/create-agent/templates/agent-capacity-*-template.md` (7)
- the six named capacity templates (system-designer, requirements-analyst, module-designer, test-engineer, qa-engineer, knowledge-manager) — 1 hit each, source and `.specify` mirror
- `skills/internal/create-team/templates/agents/agent-stage-*-template.md` (executor / evaluator / optimizer — 3) and the `.specify` mirror (3)
- `.specify/agents/{templates,instances}/*.agent.md` — `.specify/agents/templates/` holds 17 definitions, `.specify/agents/instances/` holds 3
- `.specify/features/019-agents-command.md` — exists; its body records Spec 022 at lines 51/53
- `.specify/features.md`, `.specify/constitution.md` — exist at the anchor root
- `.specify/archive/specs/022-eei-agent-triad/{requirements,plan,quickstart}.md` — exist

## Validator readings

Commands (from the repo root):

```
python3 scripts/python/validate-requirements.py .specify/archive/specs/022-eei-agent-triad/requirements.md
python3 scripts/python/validate-tasks.py .specify/archive/specs/022-eei-agent-triad/tasks.md
```

**validate-requirements.py — exit 0**:

```
file: .specify/archive/specs/022-eei-agent-triad/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
  [path-marker] pass (0)
scanned: 173 lines, 18 definition rows, 0 shared strings
0 error(s), 0 warning(s)
```

**validate-tasks.py — exit 1; 17 error(s), 10 warning(s)**:

- 17 `story-labels` errors — the amendment phases G1–G4 label rows `[G1]`…`[G4]` instead of `[US<n>]` (lines 197-203, 209-212, 218-219, 225-228). Pre-existing spec-content issue, not a dead reference; out of this repair's scope.
- 10 `parallel-safe` warnings — T038–T042 (lines 199-203) all resolve their mirror write target to the shared `specify/templates/` directory. Pre-existing; unchanged.

Before/after identity check: the HEAD version of `tasks.md` was re-validated from `.specify/.tmp/` and the two reports diffed after normalizing the `file:`/`FAIL:` path lines — **IDENTICAL VERDICT** (same 17 `story-labels` errors and same 10 `parallel-safe` warnings). The repair changed no validator verdict; the pre-existing failure set is the baseline, not a regression. (Temp scratch removed after the reading.)

## Notes

- No target was invented: every after-path names an object that exists now. Objects with no live successor (`tests/contract/test_triad_orchestration_template.py`, `tests/integration/test_eei_triad_loop.py`, `docs/eei-triad-pattern.md`, `scripts/bash/sync-runtime.sh`) were kept, not re-pointed.
- `data-model.md`, `requirements.md` and `contracts/triad-protocol.md` carried no dead path token; `verification.md` carried one prose fragment only.
- No registry row was touched: this spec is archived, and the prior audit established that the consolidation ledger binds it to Feature 019 rather than to a numeric `022` row.
- Pre-existing anomaly carried forward (not introduced here, out of a dead-reference repair): the prior audit records that `tests/contract/test_single_agent_purity.py` now forbids the `triad` capability / "Triad Refinement" surface that DoD-10/DoD-11 describe.
