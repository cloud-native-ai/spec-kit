# Goal Definitions Reference

Canonical definition of the **action-level Goal** (行动级目标) in Spec Kit: short-horizon, executable practical guidance that steers concrete work being done now. This file is the **sole owner** of three facts:

1. **the Goal concept and its composition** — executable guidance, at least one verifiable completion condition, and a lifecycle state;
2. **its store and identity** — `.specify/goals/<goal-slug>/goal.md` ([[STR-002]]), the directory slug as the only identity, and the identity grammar;
3. **its schema** — the closed frontmatter key set and the closed section set, including what a Goal definition does **not** declare.

Two facts are **cited, never restated**: the shared three-key **binding record** and the shared **lifecycle** are owned by `shared/definitions/anchor-definitions.md` (its § The Binding Record and § Lifecycle). The project-level, long-horizon end state is a different concept with its own owner, that same file; a Goal is not that concept and carries none of its mechanics. The engine's action signatures and exit codes are owned by `scripts/python/goal-utils.py` and are cited, never restated here.

## What an Action-Level Goal Is

An **action-level Goal** is **authored practical guidance for work in front of the reader**: what to do next, and how the reader will know it is done. Its horizon is short, its object is a concrete course of action, and its reader is an executing subject — a person or an agent — not an evaluator measuring a project-wide end state.

Composition is exactly three parts:

1. **Guidance narrative** — the practical direction. Unlike an Anchor's objective, **guidance MAY be step-shaped**: a numbered sequence, a checklist, or a phase-ordered approach is a legitimate body. No outcome-only shape rule applies here.
2. **Verifiable completion conditions** — at least one condition that tells the reader the guidance has been carried out. "Verifiable" means a reader can decide it from the artifact state; a condition nobody can check is not one. A definition with zero completion conditions is not a Goal.
3. **Lifecycle state** — inherited from § Lifecycle of `shared/definitions/anchor-definitions.md`.

A Goal MAY carry a **readable title** — a presentation-layer heading. **Identity stays the directory slug**: a title is never a second identifier and never takes part in resolution, binding, or reference. A Goal MAY also carry `created` / `updated` timestamps. Nothing else is part of the concept.

Two operating properties follow:

- **Consumed while the work is live**: a Goal is written to be acted on now. It is not a long-horizon pursuit, and nothing about it is measured by degree over time.
- **Modified deliberately**: changing a Goal is recorded in its `## History`; silent drift is prohibited.

## Store and Identity

| Aspect | Value |
|--------|-------|
| Store | `.specify/goals/<goal-slug>/goal.md` ([[STR-002]]) |
| Identity | the directory slug `goal-slug`; one directory per Goal |
| Definition file | `goal.md` — the layer's filename, resolved by the engine per layer |
| Derived neighbour | a `summary/` subtree MAY sit beside the definition; it is derived, never hand-edited, and never a definition |

**Identity grammar.** A slug is admitted only when it passes the engine's `is_valid_identity`: a non-empty token starting with an ASCII letter or digit and continuing with letters, digits, `_`, `.` or `-` (`^[A-Za-z0-9][A-Za-z0-9_.\-]*$`), and never `.`, `..`, or a token containing `/` or `\`. The engine's function is the executable owner of this grammar; this table is its authored statement.

**Layer separation is absolute.** A Goal identity resolves only in `.specify/goals/`. A slug that exists under `.specify/anchoring/` is an Anchor identity and MUST NOT resolve as a Goal; a team's `anchor_slug` MUST NOT resolve to a Goal. The engine refuses a write that would store the same slug in both stores, naming both candidates — there is no dual storage and no silent precedence.

## Schema

**Frontmatter** — exactly these keys:

| Key | Meaning |
|-----|---------|
| `status` | a value from the shared lifecycle (owner cited above) |
| `created` / `updated` | ISO-8601 timestamps |
| `binding` | the shared three-key binding record (owner cited above) |

The key set is **closed**. In particular the schema declares **no `anchor_ref`** and **no key named after an Anchor**, because a Goal is not organised around one. An undeclared key is refused through the interface contract's undeclared-option rule (exit 2): the engine rejects it instead of ignoring it. The **only** cross-reference a Goal may carry is the binding record's `origin` (the spec directory it directly came from).

**Sections** — exactly these headings:

| Section | Status |
|---------|--------|
| `## Guidance` | required — the practical narrative (steps allowed) |
| `## Completion Conditions` | required — at least one verifiable condition |
| `## History` | required — append-only change record |
| `## Migrated Targets` | optional carry-over — a preserved record from a definition migrated by feature 101; it is history, not a live mechanism |
| `## Boundaries` | optional carry-over — exclusions preserved from a migrated definition |

A Goal definition does **not** declare `## Objective`, `## Success Criteria`, or a live `## Targets` section. Target decomposition, Target identity and Target lifecycle are mechanics of the Anchor, owned by `shared/definitions/anchor-definitions.md`; a Goal neither issues, transitions nor resolves Targets, and the rows under `## Migrated Targets` are inert text preserved from the migration. The same holds for team binding and for `coordinate`: both are Anchor-side and team-side mechanics and have no Goal-side form.

## Lifecycle (by reference)

The value set and transition discipline are owned by `shared/definitions/anchor-definitions.md` § Lifecycle. In Goal terms:

- `active` → `achieved` | `abandoned`; both terminal states are absorbing for ordinary actions and **retained on disk** — a terminal Goal is never deleted.
- Re-opening a terminal Goal requires the explicit `reopen` action, is permitted only for `owner: human`, and appends a `## History` line. It is never a side effect of another action.
- The engine's Goal status action both **reports** the current state and performs a transition when one is requested; with no requested transition it only reports and writes nothing.

## Relationship to Its Neighbours

**Versus the Anchor.** The Anchor is the project-level, long-horizon end state; a Goal is short-horizon executable guidance. They are separate concepts in separate stores with separate command surfaces, and neither derives from the other. A Goal never references an Anchor by identity (see Schema), and an Anchor never contains Goals.

**Versus SDD (spec / plan / tasks).** They are **parallel, not subordinate**. A spec directory carries the design of a deliverable — requirements, plan, tasks — and a Goal carries action-level guidance. Neither resolves the other's identity: a Goal has no spec field, and a spec carries no goal-slug field. A Goal is not a replacement for a requirements spec, and a spec is not a substitute for a Goal.

**Versus the Team and the control hierarchy.** The control hierarchy is Anchor → Team → Agent → SDD run. A Goal has **no position in it**: it is not a level, not a parent, and not a subordinate, and no team binds it. Team binding and slice coordination are carried by Anchor and Team only.

**Versus the Requirement.** A Requirement is a binding clause on a deliverable, verified pass/fail against tests; a Goal's completion conditions describe the state after the guidance has been carried out. Neither audits the other, and a completion condition MUST NOT be presented as a per-feature success criterion.

## Terminology

| Term | Meaning |
|------|---------|
| **action-level Goal** (行动级目标) | The concept defined here: short-horizon executable guidance in `.specify/goals/<goal-slug>/goal.md` |
| **Goal archive** | The `.specify/goals/` directory tree holding Goal definitions; one of the three archive layers |
| **Guidance** | The Goal's practical narrative — steps allowed, and not an outcome-only objective |
| **Completion condition** | A checkable statement that the guidance has been carried out; at least one per Goal |

**Retired wording (mapped forward, never reused):** the phrases "project-level Goal", "Global Goal" and "temporary Goal" described the concept that is now the **Anchor**; they are historical spellings and MUST NOT be used for a Goal in any live surface. The project-level end state is the Anchor — its owner is `shared/definitions/anchor-definitions.md`. Likewise the retired team binding key `goal_slug` refers to an Anchor binding and is now `anchor_slug`.

**Action signatures are not here.** The engine (`scripts/python/goal-utils.py`) owns the Goal action group's names, flags and exit codes; this document defines what the words mean and cites the engine for how to call it.
