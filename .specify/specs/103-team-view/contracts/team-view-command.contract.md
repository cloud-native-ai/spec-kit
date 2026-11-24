# Contract — View Command Wiring (`templates/commands/team.md` + `docs/reference/commands/team.md`)

**Consumers**: `/speckit.tasks` turns each clause into task rows; `/speckit.implement` checks each one off; the pinning test below enforces the machine-readable clauses.
**Pinning test**: `tests/contract/test_team_view_command.py` (all clauses).
**Clause grammar owner**: `shared/definitions/contract-clause-definitions.md` (canonical `**C-N**` form).
**Shared Strings**: `[[STR-001]]` = `team not found`; `[[STR-002]]` = `No teams found`; `[[STR-003]]` = `[create|modify|run|view] [team-slug] [--target <T-<nnn>>]`; `[[STR-004]]` = `exactly three modes`.

**C-01** Frontmatter declares the fourth mode.

`templates/commands/team.md` frontmatter MUST carry:
- a `description` that names four team operations including `view`;
- a `short-description` that names four modes;
- `argument-hint` whose value is exactly `[[STR-003]]` (the key is new to this file; `templates/commands/anchor.md` and `goal.md` are the sibling form). The hint is the **command-level** argument grammar shared by all four modes — it is not a per-mode permission: `--target` remains run-only (C-04).

**C-02** Mode table has exactly four rows.

The `### Modes → Capability Routing` table MUST list, in order, `create`, `modify`, `run`, `view`; the `view` row's recognized intents MUST be the view-intent group (查看 / 展示 / 呈现 / 结构 / 状态 / 详情 / 概览 / overview / status / inspect / show) and its delegate MUST be `view-team`. The other three rows keep their routing target.

**C-03** The stale "three modes" claim is gone.

The literal `[[STR-004]]` MUST appear 0 times in `templates/commands/team.md`, in `docs/reference/commands/team.md`, and in every per-tool copy of `speckit.team` that this repository ships. Per-tool copies are produced by `regen-command-copies.py`; a hand edit of a copy is a defect.

**C-04** Routing flow includes view and preserves no-guess.

The routing flow MUST classify `view` as a mode, route it to the `view-team` skill, and keep these invariants:
- create / modify / run intent MUST NOT route to view;
- a non-empty ambiguous input MUST report all four capabilities and request the missing intent, and MUST NOT execute any mode (including view);
- `--target` is a run-only parameter: `view` carrying `--target` MUST be reported as a mode/parameter conflict and MUST NOT be silently dropped or rerouted to run (pinned by `tests/contract/test_team_view_command.py::test_view_target_conflict_declared`).

**C-05** Default behavior names all four modes.

The no-argument default behavior's capability summary MUST list the four modes. The default behavior itself stays the existing informational sequence (list teams, ground suggestions, show capabilities); it MUST NOT become an implicit view execution.

**C-06** View delegates; the template does not render.

A `### View Mode` section MUST delegate to the read-only skill at the runtime path `.specify/skills/internal/view-team/SKILL.md` and state, in substance:
- view is read-only: no definition/run/ledger/summary/anchor/registry/state write, no seat dispatch, no run-line registration;
- no-slug = overview; slug = exact match; unknown slug = `[[STR-001]]` + create suggestion; corrupt definition = a named-path "定义损坏" report, not "not found";
- `--target` carried by view is a mode/parameter conflict (C-04), never a silent drop;
- the five-check preview and `blocked` verdict belong to `run-team`, not to view;
- fixed extraction runs in `scripts/python/team-view.py`.

The template MUST NOT enumerate the six groups' fields and MUST NOT carry rendering logic.

**C-07** Docs page carries four modes.

`docs/reference/commands/team.md` MUST:
- describe the command as four modes in its opening paragraph and `When to Use`;
- list `view` in `Syntax` and in the modes table (four rows);
- contain a `## View Mode` section covering: read-only, no-slug overview, exact slug match, `team not found` + create suggestion, corrupt-definition named path, and the not-a-run-preview boundary;
- list `view-team` under `Companion Skills`.

**C-08** The two run-mode drift corrections land in the same change.

In `docs/reference/commands/team.md`:
- the run delegation cell/statement MUST name `run-team` (never `create-team (execution path)`);
- the run preview MUST be described as disclosure, not a blocking gate: the text MUST NOT claim that execution waits for an explicit confirmation or that declining prevents execution. The false-claim literals `never executes before you confirm`, `Only then does orchestration run`, and `Declining stops without executing` MUST each appear 0 times.

The template and `skills/internal/run-team/SKILL.md` are the sole record of intent; the docs page follows them.

**C-09** Routing sample set.

The contract carries a routing sample set of at least one intent per class:

| # | Sample input | Expected mode |
|---|--------------|---------------|
| 1 | `查看 cws-workspace-cluster 的结构和状态` | view |
| 2 | `show me the team structure` | view |
| 3 | `overview of all teams` | view |
| 4 | `创建一个团队来跑回归` | create |
| 5 | `调整团队的人员配置` | modify |
| 6 | `运行团队 --target T-001` | run |
| 7 | `team`（无进一步语义） | ambiguous → capabilities only |

The pinning test asserts the deterministic proxy: every sample's distinctive token appears in the row of its expected mode, and every view-distinctive token appears in no create/modify/run row. The test does not execute an LLM.

**C-10** SC-005 named files.

The two named files — `templates/commands/team.md` and `docs/reference/commands/team.md` — MUST each contain four mode identifiers in their mode table (`create`, `modify`, `run`, `view`), and `[[STR-004]]` MUST be 0 in both. This is a fixed-pattern count with an empty allowed increment.

**C-11** Read-only at the command level.

The view path MUST NOT register a run line and MUST NOT dispatch a seat. The command template states this; the skill and program contracts enforce it mechanically.

**C-12** Mirrors and copies.

- `templates/commands/team.md` is the source; its four per-tool copies MUST be regenerated by `python3 scripts/python/regen-command-copies.py` and pass `--check`.
- `docs/reference/commands/team.md` has no mirror.
- No `.specify/templates/commands/` mirror exists (retired); a change that creates one is a defect.
