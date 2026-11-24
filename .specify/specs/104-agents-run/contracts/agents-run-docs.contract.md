# Contract — Documentation Same-Source (`docs/reference/commands/agents.md`, `docs/reference/agents/*`, `docs/tutorials/*`, routing scenario)

**Consumers**: `/speckit.tasks` turns each clause into task rows; `/speckit.implement` checks each one off; the pinning test below enforces the machine-readable clauses.
**Pinning test**: `tests/contract/test_agents_run_docs_contract.py` (artifact-class clauses C-23…C-34; C-35 is the mutation drill, executed once and recorded in `test-evidence/`).
**Clause grammar owner**: `shared/definitions/contract-clause-definitions.md` (canonical `**C-N**` form).
**Shared Strings**: `[[STR-001]]` = `[create|refine|run] [agent-name] [task]`; `[[STR-005]]` = `capabilities (create / refine)`; `[[STR-006]]` = `create and refine one agent`; `[[STR-007]]` = `Generate role-based agents or create custom agents`; `[[STR-008]]` = `generates the seven role-based workflow agents`.

**C-23** One command reference body.

`docs/reference/commands/agents.md` MUST contain exactly one top-level `# /speckit.agents` heading (`^# /speckit.agents` count = 1; measured 3 before this feature). The two older concatenated copies are deleted, not reworded. (FR-018, SC-004)

**C-24** The opening description names three capabilities.

The opening paragraph MUST describe the command as the entry point for create, refine **and run**; `[[STR-006]]` MUST appear 0 times. (FR-018, SC-004)

**C-25** The Syntax block carries the explicit run form.

The `## Syntax` block MUST contain `[[STR-001]]` verbatim (the same argument-hint grammar as C-01 of the command contract) and an explicit `/speckit.agents run <agent-name> [task]` line; it MUST keep a no-argument line describing the list + suggestion behaviour and a natural-language intent line. (FR-018, SC-001)

**C-26** The intent table has a run row and the ambiguity report is three-way.

The intent table MUST list run → `run-agent` beside create → `create-agent` and refine → `improve-agent`; the ambiguity sentence MUST list three capabilities (create / refine / run); `[[STR-005]]` MUST appear 0 times. (FR-018, SC-004)

**C-27** Companion skills list three skills.

`## Companion Skills` MUST list `create-agent`, `improve-agent` **and** `run-agent`, each with its role; the stale two-skill list is gone. (FR-018)

**C-28** The no-argument behaviour matches the template.

The no-argument section MUST describe the current sequence — list existing agents, give grounded suggestions, show the three-mode capability summary — and MUST NOT claim that `/speckit.agents` with no arguments generates role-based agents. `[[STR-008]]` MUST appear 0 times, and the stale-variant predicates of C-34 MUST hold. (FR-018, SC-004)

**C-29** `command-and-skills.md` becomes three-capability.

`docs/reference/agents/command-and-skills.md` MUST: describe the command as create / refine / run; state that the single-agent work is done by **three** skills; carry a run row in its intent-routing table; cover run in its routing flow; and add a `run-agent` section that describes resolve → present → dispatch → external collect → report **by pointer to its output contract**, without copying rule text. `[[STR-006]]`-class two-capability statements and `[[STR-005]]` MUST appear 0 times. (FR-019, SC-004)

**C-30** `overview.md` gains run and the third skill.

`docs/reference/agents/overview.md` MUST: include run in its command capability statement; change the skill-count statement from two to three skills (both the prose sentence and the navigation row); and include `run-agent` in the entry diagram's skill layer. (FR-020, SC-004)

**C-31** `design.md` gains run and the third skill.

`docs/reference/agents/design.md` MUST: include run in the command capability line; add the run step to the single-agent command workflow; and add `run-agent` to the single-agent skill list. (FR-020, SC-004)

**C-32** The tutorials carry run and drop the stale claims.

`docs/tutorials/installation.md` and `docs/tutorials/quickstart.md` MUST: give `/speckit.agents` a command-table row naming create / refine / run; and contain 0 occurrences of `[[STR-007]]` and of the stale no-argument generation predicates of C-34. (FR-020, SC-004)

**C-33** The routing scenario is three-capability.

`tests/scenarios/agents-command/single-entry-routing-scenario.md` MUST state the single-agent scope as create / refine / run, add explicit run routing samples, and report three capabilities on ambiguous input; `[[STR-005]]` MUST appear 0 times. (FR-020, SC-004)

**C-34** The stale-literal set is closed and empty after the change.

Measured baselines (2026-11-24) and the required after-state across the seven named files — this command reference, `docs/reference/agents/command-and-skills.md`, `overview.md`, `design.md`, `docs/tutorials/installation.md`, `docs/tutorials/quickstart.md`, and `tests/scenarios/agents-command/single-entry-routing-scenario.md`:

| Predicate | Before (files) | After |
|-----------|----------------|-------|
| `[[STR-005]]` | 4 (commands ref 2, command-and-skills 1, routing scenario 1) | 0 |
| `[[STR-006]]` | 2 (commands ref 2) | 0 |
| `[[STR-007]]` | 2 (installation 1, quickstart 1) | 0 |
| `[[STR-008]]` | 2 (commands ref 2) | 0 |
| case-insensitive `generate role-based agents` | commands ref, quickstart, installation | 0 |
| case-insensitive `generate project-aware role agents` | quickstart | 0 |
| case-insensitive `generate seven` | installation, quickstart | 0 |
| line containing both `no arguments` and `generate` | installation, quickstart | 0 |

`docs/reference/history/` MUST NOT be edited (dated records). README carries no `/speckit.agents` capability row (measured 0) and is not part of this set. (FR-018, FR-020, SC-004)

**C-35** Mutation drill (4/4) is exercised and recorded.

Each of the four mutations MUST turn its pinned check red, and restoration MUST turn it green: delete `argument-hint` → C-01 of the command contract red; delete the run intent row → C-02 of the command contract red; delete the seven-field downlink pointer → C-12 of the dispatch contract red; duplicate the command reference body → C-23 of this contract red. The red/green readings are recorded in `test-evidence/` (SC-006 source). (SC-006, FR-024)
