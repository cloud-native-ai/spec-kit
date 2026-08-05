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
- **Shared flags** (`--repo-root`, `--json`) are accepted **both before and after** the subcommand.

## Parameters

| Name | Required | Description |
|------|----------|-------------|
| subcommand | yes | One of `create`, `validate`, `list`, `status`, `criteria`, `migrate` |
| `create <slug> --objective T [--criterion C ...]` | — | Archive a new definition at `.specify/goal/<slug>/goal.md` |
| `validate <slug\|path>` | — | Validate one definition against the contract |
| `list` | — | Enumerate the archive (slug, status, criteria count) |
| `status <slug> --set STATE` | — | Change lifecycle state (`active`/`achieved`/`abandoned`) |
| `criteria <slug> --criterion C ...` | — | Replace criteria, appending the prior value to History |
| `migrate <team-slug> [--drop-inline]` | — | Derive a definition from a team's inline goal and set its `goal_slug`; inline kept unless `--drop-inline` |
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

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | ok |
| `2` | input error — invalid identity, duplicate, rejected objective, or missing team/inline goal |
| `3` | goal not found (for `status` / `criteria` on a missing slug) |
| `4` | validation failed (`validate`) |

## Environment Applicability

- **Verified against**: Python 3.11.11 in this repository (2026-08-05). No third-party dependencies — standard library only.
- **Unverified**: other Python versions and platforms. Status stays **Draft** until exercised on the project's declared floor (`>=3.8`) in CI; the promotion to Verified is the outstanding step.

## Mirror

Canonical `scripts/python/goal-utils.py` is mirrored byte-identical to `.specify/scripts/python/goal-utils.py` by `sync-mirrors.py`. Never hand-edit the mirror.
