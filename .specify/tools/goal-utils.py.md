# Tool Record: goal-utils.py

**Tool Name**: goal-utils.py  
**Tool Type**: `project-script`  
**Source Identifier**: scripts/python/goal-utils.py  
**Tool ID**: <TOOL:.specify/memory/tools/goal-utils.py.md>  
**Aliases**: goal-utils  
**Status**: Draft  
**Discovery Origin**: manual-entry  
**Last Updated**: 2026-08-05

## Scope

**Availability**: Project-level — available only within the current project workspace.  
**Typical Sources**: Scripts bundled with the project (`scripts/python/*.py`, mirrored to `.specify/scripts/python/`).  
**Portability**: Tied to the project repository; not available outside the project root.  
**Source Identifier Convention**: Path relative to the project root.

## Description

The goal definition engine behind `/speckit.goal` (Feature 041). It owns the deterministic half of goal management — identity grammar, the exactly-three-part structure, the three-state lifecycle and its transition table, change history, archive enumeration, and migrating a team's inline goal into an archived definition. The command owns interaction and the preview→confirm gate; this engine owns the fixed rules, so the same judgement is reproducible across runs (Program-First / Principle XII).

## Resource ID

- Canonical ID: `<TOOL:.specify/memory/tools/goal-utils.py.md>`
- Canonical Path: `.specify/memory/tools/goal-utils.py.md`

## Invocation & I/O Contract

- **Input Channel**: command-line subcommands + flags
- **Invocation Mode**: non-interactive
- **Output Mode**: human text by default; `--json` for a machine-readable payload
- **Shared flags** (`--repo-root`, `--json`) are declared on a parser shared by the top level and every subparser, but **pass them AFTER the subcommand**. Measured 2026-10-04: argparse lets a subparser's own default overwrite a value the top-level parser already set, so `--json <subcommand>` silently emits the human form and `--repo-root X <subcommand>` silently resolves to the cwd. The source comment claiming both orders work is wrong and is recorded as `053-machine-decidable-artifacts/research.md` A-9; it is not fixed here because that would change flag precedence for every existing subcommand.

## Parameters

| Name | Required | Description |
|------|----------|-------------|
| subcommand | yes | One of the ten actions `create`, `validate`, `check-statement`, `list`, `status`, `objective`, `criteria`, `migrate`, `targets`, `run-checks` (the closed roster; `--help` lists each with a `read:`/`write:` label) |
| `create <slug> --objective T [--criterion C ...]` | — | Archive a new definition at `.specify/goal/<slug>/goal.md` |
| `validate <slug\|path>` | — | Validate one definition against the contract |
| `list` | — | Enumerate the archive (slug, status, criteria count) |
| `status <slug> --set STATE` | — | Change lifecycle state (`active`/`achieved`/`abandoned`) |
| `criteria <slug> --criterion C ...` | — | Replace criteria, appending the prior value to History |
| `migrate <team-slug> [--drop-inline]` | — | Derive a definition from a team's inline goal and set its `goal_slug`; inline kept unless `--drop-inline` |
| `check-statement <statement>` | — | Standalone dry-run shape validation of one Target statement (GD-2/GD-3); needs NO goal, so it is usable before `create` |
| `objective <slug> --set TEXT` | — | Replace the objective, recording the prior value in `## History` |
| `targets <slug> --list \| --check S \| --add S \| --set STATE --id T-nnn` | — | The Targets of one goal; `--list`/`--check` are reads, `--add`/`--set` are writes |
| `run-checks <team-slug> [--target T-nnn]` | — | **Read.** The five run-precondition checks (goal-binding / dangling / target-terminal / cross-goal / goal-terminal) in one call, zero writes; see RULE-10 |
| `--repo-root` | no | Repository root (default: cwd) |
| `--json` | no | Emit a machine-readable payload |

## Behavioral Rules

- **RULE-1**: Identity grammar is `^[A-Za-z0-9][A-Za-z0-9_.-]*$` **and** a safe path segment (no `/`, not `.`/`..`). This reuses requirement 036's `goal_slug` grammar — there is exactly one identity mechanism, not two.
- **RULE-2**: Lifecycle is exactly three states. `active → achieved` and `active → abandoned` are the only non-identity transitions; reopening a terminal goal is refused. `superseded` is not a state.
- **RULE-3**: A goal is composed of exactly three parts (objective, criteria, lifecycle). Timestamps are change-history metadata, never a fourth part; identity is the directory name, never a frontmatter field.
- **RULE-4**: `create` refuses a duplicate identity and points at the modify path — it never overwrites an existing definition.
- **RULE-5**: An objective that reads as a task list is refused as **GD-2**; one bundling several objectives is refused as **GD-3** with a split instruction.
- **RULE-6**: Empty criteria are legal and recorded as the literal `None provided.` — consumers declare the absence rather than inventing criteria.
- **RULE-7**: A criteria change appends the prior value to `## History`; it never silently replaces.
- **RULE-8**: `migrate` keeps the team's inline goal unless `--drop-inline`; it refuses to migrate onto an already-archived identity.
- **RULE-9**: This engine is the **only** writer of `.specify/goal/<slug>/goal.md`. The summary refresh (`build-summary-input.py`) writes only the `summary/` subtree and never the definition.
- **RULE-10**: `run-checks` is **read-only** and reuses the engine's own parse — it defines no second grammar. Its top-level `verdict` is `preview_target_check`'s, verbatim, whenever a Target reference is in play, so the gate run mode already trusts is the gate this action reports. A check whose precondition does not hold reports `not-evaluated`, **never** `ok`: a check that did not run must not report green. `blocked` is the field that means "this run must stop"; `verdict` only states the binding's condition, so a team with no goal definition and no `--target` reports `no-goal-definition` with `blocked=false` (that is the recorded rule — a missing binding stops a run only when a Target was named), while a terminal goal sets `blocked=true` either way. Exit tiers are mutually distinguishable: blocked `5`, bad argument `2`, definition unusable `4`, team missing `3`.

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | ok |
| `2` | input error — invalid identity, duplicate, rejected objective, or missing team/inline goal |
| `3` | goal not found (for `status` / `criteria` on a missing slug) |
| `4` | validation failed (`validate`), or a definition `run-checks` cannot interpret (a status outside the lifecycle set) |
| `5` | **blocked** — `run-checks` judged the run blocked by one of the five checks. New with 053; the four codes above keep their existing meanings byte for byte, so one code never carries two meanings across actions |

## Environment Applicability

- **Verified against**: Python 3.11.11 in this repository (2026-08-05). No third-party dependencies — standard library only.
- **Unverified**: other Python versions and platforms. Status stays **Draft** until exercised on the project's declared floor (`>=3.8`) in CI; the promotion to Verified is the outstanding step.

## Mirror

Canonical `scripts/python/goal-utils.py` is mirrored byte-identical to `.specify/scripts/python/goal-utils.py` by `sync-mirrors.py`. Never hand-edit the mirror.
