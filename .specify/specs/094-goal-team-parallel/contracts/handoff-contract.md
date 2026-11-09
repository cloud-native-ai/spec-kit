# Contract — Handoff Contract (`handoff.md`) and Construction Crew

Owner of the artifact shape: this contract. Owner of the territory mechanism it consumes:
`skills/internal/create-team/references/create-mode.md` § territory (the existing closed allow/forbid list).
Owner of the task table: `<spec-dir>/tasks.md` (this contract references task ids, never copies task rows).

## 1. Shape and location

- **C-53**: A handoff contract MUST live at `<spec-dir>/` + [[STR-004]] (`handoff.md`) — one per spec, a fixed
  relative path, no variant names and no second location .

(FR-016, FR-035)
- **C-54**: `handoff.md` MUST carry exactly these top-level sections, in this order: `## Status`, `## Goal`,
  `## Targets`, `## Task Reference`, `## Territory`, `## Acceptance Criteria`, `## Writeback`, `## Crew`. Each
  section is mandatory; an empty section MUST be written as the single line `None.` rather than omitted.

(FR-016, FR-035)
- **C-55**: `## Status` MUST carry a YAML frontmatter block with `contract: handoff/v1`, `state: active |
  fulfilled | abandoned`, `goal_slug`, `team_slug`, `created`, `updated`, and `supersedes: null | <path>`.
  `state` is a two-terminal-state machine: `active → fulfilled` or `active → abandoned`; a terminal handoff is
  retained, never deleted.

(FR-016, FR-035)
- **C-56**: `## Goal` MUST cite the goal definition by `goal_slug` only and MUST NOT restate its objective or
  criteria (the N teams : 1 goal identity rule). `## Targets` MUST cite the goal's `T-NNN` ids the crew may
  advance, and MUST NOT restate their statements.

(FR-016, FR-035)
- **C-57**: `## Task Reference` MUST reference the task table by **id ranges or explicit id list** and MUST NOT
  copy task rows. A handoff that contains a line beginning with `- [ ] T` is a defect
  (`task-copy-in-handoff`, refused).

(FR-016, FR-035)
## 2. The three-way key pair (FR-034)

- **C-58**: `handoff.md` frontmatter `goal_slug` MUST resolve to `.specify/anchoring/<goal_slug>/goal.md`, and
  `team_slug` ([[STR-005]]) MUST resolve to `.specify/teams/<team_slug>/team.md`. Both MUST be refused at
  creation when they do not resolve (`handoff-dangling-key`, exit 2): a contract never names a team that does not
  exist.

(FR-016, FR-034)
- **C-59**: The reverse keys MUST exist on the two other sides: `.specify/anchoring/<goal_slug>/goal.md` and
  `.specify/teams/<team_slug>/team.md` each MUST carry `handoff_ref: <spec-dir-relative path>` pointing back at
  the same `handoff.md`, written by the engine's binding action (C-5/C-6's discipline), never by the contract
  file alone.

(FR-003, FR-016, FR-034)
- **C-60**: The three-way resolution MUST be decidable without reading prose: a contract test loads the three
  files and asserts each key resolves and that the two `handoff_ref` values point at the same file (SC-006).

(FR-016, FR-034)
## 3. Territory: design authority vs construction (FR-036)

- **C-61**: On activation the contract's `## Territory` entry set MUST be expanded into the `territory.write`
  list of **every** team bound to that `goal_slug`, before the crew runs. The expansion is an `improve-team`
  applied modification (explicit, disclosed, one record per team), never an optimizer guess.

(FR-016, FR-036)
- **C-62**: `requirements.md`, `tasks.md`, `verification.md` and `handoff.md` itself MUST land in
  `territory.forbidden` of every seat that carries the expansion. A crew write attempt against any of them MUST be
  refused by the existing `create-team` territory check, with a non-zero exit and a refusal text naming the path
  and the seat (SC-007). The refusal MUST NOT depend on the crew's cooperation.

(FR-019, FR-036)
- **C-63**: `territory.write` entries granted by C-61 MUST stay inside the spec directory of the contract and
  MUST NOT include `.specify/anchoring/**` or `.specify/teams/**` (C-15 of `binding-and-lifecycle.md`).

(FR-036)
- **C-64**: The design face of `handoff.md` is owned by the spec side: a crew seat MUST NOT hold `write` on it.
  Amendments to the contract are a spec-side edit plus an engine re-expansion; an `active → fulfilled` transition
  is recorded by the spec side after the writeback is verified.

(FR-017, FR-036)
## 4. Writeback (FR-020, FR-019)

- **C-65**: `## Writeback` MUST name the writeback form: one record per completed task under
  `<spec-dir>/writeback/<T-NNN>.yaml` carrying `task`, `outcome` (`done` | `blocked` | `deferred`), `run_id`,
  `evidence` (path or command plus exit code), and `at`. One file per entry — never a shared stream.

(FR-020)
- **C-66**: The spec side MUST be able to judge each task's state from those files alone; a missing record is
  `not-written-back`, never inferred from a commit message or a summary.

(FR-020)
- **C-67**: `tasks.md` and `verification.md` remain spec-side writes (C-62). The crew's delivery is the writeback
  set plus patches under its territory; it MUST NOT mark a task complete in the task table.

(FR-019, FR-020)
## 5. Production and consumption timing (FR-035, FR-039)

- **C-68**: `handoff.md` MUST be produced by the `tasks` stage, after the complexity decision returns `handoff`,
  and consumed by `implement`. The `plan` stage MUST NOT produce one — the task table does not exist yet
  (Clarifications Q4).

(FR-035, FR-039)
- **C-69**: A spec whose complexity decision returns `direct` MUST NOT carry a `handoff.md`; an unexpected one is
  reported (`handoff-without-handoff-decision`) and MUST NOT be consumed as authority.

(FR-035, FR-039)
- **C-70**: `implement` MUST refuse to start a handoff-mode run when the contract is `abandoned` or when any of
  C-58's keys no longer resolve; it MUST NOT repair the contract itself.

(FR-035, FR-039)
## Requirement coverage

FR-016, FR-017, FR-018, FR-019, FR-020, FR-034, FR-035, FR-036; SC-006, SC-007.
