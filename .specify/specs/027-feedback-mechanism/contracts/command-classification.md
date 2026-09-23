# Contract: Command Complexity Classification (FR-006)

**Feature**: 028 Feedback Mechanism | **Type**: Classification contract

Fixes which of the 17 commands are **complex** (carry feedback) vs **simple** (excluded). This is the authoritative source for the convention + conformance tests.

## Classification rule

A command is **complex** — and therefore MUST carry the feedback step — iff it meets ANY of:

- **(a)** it invokes scripts or command-line tools (e.g. `scripts/bash/*.sh`, `scripts/python/*.py`);
- **(b)** it produces an artifact consumed by another flow;
- **(c)** it consumes an artifact produced by another flow.

A command meeting NONE of these is **simple** and MUST NOT carry the feedback step (FR-006, FR-007).

> Note: `create-*` / `improve-*` authoring is delivered as **skills**, which carry feedback under the all-skills rule (FR-002). The thin command wrappers listed as "simple" therefore do not double up on feedback.

## Classification table (17 commands)

| Command | (a) scripts | (b) produces for | (c) consumes from | Class | Rationale |
|---------|:---:|:---:|:---:|-------|-----------|
| `requirements` | ✅ | plan, clarify, tasks, analyze, checklist, review | — | **Complex** | Emits `requirements.md`; runs create-new-requirements script. |
| `clarify` | ✅ | plan | requirements | **Complex** | Consumes + amends `requirements.md`. |
| `plan` | ✅ | tasks | requirements, research, constitution | **Complex** | Emits plan/data-model/contracts; runs create-new-plan script. |
| `tasks` | ✅ | implement | plan | **Complex** | Emits `tasks.md`; runs prereq script. |
| `implement` | ✅ | review | tasks | **Complex** | Consumes `tasks.md`; emits code + verification. |
| `analyze` | ✅ | — | requirements, plan, tasks | **Complex** | Cross-artifact consistency read. |
| `checklist` | ✅ | — | requirements | **Complex** | Consumes spec; runs script. |
| `review` | ✅ | — | requirements, plan, tasks | **Complex** | Global report over multiple artifacts (owns global scope; still self-reviews locally). |
| `research` | ✅ | plan | — | **Complex** | Emits `research.md`; runs research script. |
| `instructions` | ✅ | (compat symlinks) | project state | **Complex** | Runs generate-instructions script; regenerates instructions + symlinks. |
| `tools` | ✅ | — | — | **Complex** | Orchestrates tool scripts / external CLIs. |
| `skills` | ✅ | — | — | **Complex** | Runs skills-utils / create-new-skill scripts. |
| `todo` | ✅ | — | — | **Complex** | Runs detect/scan scripts over files. |
| `agents` | ❌ | — | — | **Simple** | Self-contained `.agent.md` authoring; no script, no per-run flow I/O. |
| `constitution` | ❌ | — | — | **Simple** | Interactive editing of a shared registry doc; not a per-run producer/consumer flow. |
| `feature` | ❌ | — | — | **Simple** | Feature-index registry editing; not a scripted / chained flow. |
| `team` | ✅ | run, goal coordinate, improve-team | goal | **Complex** | Reclassified 2026-09-23 (introspection-20260923T120035Z#F-02, user-adjudicated). Not a thin wrapper: `templates/commands/team.md` invokes 4 distinct scripts directly (`scripts/python/goal-utils.py`, `skills/create-team/scripts/match-team-preset.py`, `skills/create-team/scripts/verify-territory-disjoint.py`, `build-summary-input.py`), emits `.specify/teams/<slug>/team.md` + `runs/` consumed by `/speckit.team run`, `/speckit.goal coordinate` and `improve-team`, and consumes the bound goal's `## Targets`. All three criteria hold, so the delegation rationale below the table does not apply. |

**Result**: 14 complex (feedback-bearing) · 3 simple (excluded).

## Maintenance

- If a command later starts invoking a script or joining the producer/consumer chain, re-run this rule and update both this table and the command template.
- The conformance test in `tests/contract/` MUST read this table (or an equivalent list) so classification drift is caught automatically.
- **Known gap (recorded 2026-09-23, not fixed here)**: this table covers 17 commands, while `templates/commands/` currently holds 25. The 8 unlisted commands (`goal`, `interview`, `feedback`, `sanitize`, `derive`, `session`, `history`, `todo`'s siblings as applicable) were added after Feature 028 and are classified only by the conformance tests' own lists. Re-deriving the full table against the current tree is a separate task; until then the tests' `COMPLEX_COMMANDS` lists — not this table — are the operative enumeration.
