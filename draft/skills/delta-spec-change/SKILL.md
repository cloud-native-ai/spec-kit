---
name: delta-spec-change
description: |
  Brownfield spec change-management workflow that captures a change as a self-contained proposal — a change proposal directory holding proposal, design, delta specs, and a task checklist — then applies deltas (ADDED / MODIFIED / REMOVED / RENAMED requirements) into living capability specs and archives the completed change to a dated directory. Deltas express intent against existing specs so brownfield changes stay reviewable and testable. Use this when the user mentions ["delta spec", "change proposal", "brownfield change", "spec change", "change management", "ADDED requirements", "MODIFIED requirements", "REMOVED requirements", "RENAMED requirements", "sync specs", "archive change", "living spec", "capability spec", "OpenSpec", "opsx", "增量规范", "变更提案", "规范变更", "归档变更", "变更管理", "棕地变更", "增量变更", "同步规范", "现存规范", "能力规范", "新增需求", "修改需求", "移除需求", "重命名需求"]
skill_id: "<SKILL:draft/skills/delta-spec-change/SKILL.md>"
---

# delta-spec-change

> **Status: draft** — adapted from OpenSpec (@fission-ai/openspec) Delta Spec workflow. Incubating in draft/; not wired into the main /speckit.* flow.

## Overview

This skill manages **changes to an existing, spec-driven codebase** (brownfield work).
Instead of editing a capability's specification in place, you author a **change
proposal** that records *why* the change is needed and a set of **delta specs** that
describe the *difference* you intend to introduce — new requirements (ADDED), changed
behavior (MODIFIED), deprecations (REMOVED), and pure renames (RENAMED).

The change lives as a self-contained directory while you implement it. When
implementation is complete, you **sync** the deltas into the permanent **living
specs**, then **archive** the change to a dated directory. This keeps a coherent,
reviewable history of how the system's specs evolved.

There are two kinds of spec files:

- **Living spec** — `draft/specs/<capability>/spec.md`. The current, agreed truth for
  a capability. Sections: `## Purpose`, `## Requirements`.
- **Delta spec** — `draft/changes/<change>/specs/<capability>/spec.md`. The intended
  difference for one change. Sections: `## ADDED / MODIFIED / REMOVED / RENAMED
  Requirements`.

> Because this is a draft skill, it works under `draft/changes/` and `draft/specs/` so
> it does **not** collide with the master project's existing `/speckit.*` spec flow
> (`.specify/specs/`). Treat `draft/` as the sandbox root for this workflow.

### Directory layout

```
draft/
├── specs/                                  # living specs (permanent truth)
│   └── <capability>/
│       └── spec.md                         # ## Purpose + ## Requirements
└── changes/
    ├── <kebab-change-name>/                # one active change
    │   ├── proposal.md                     # WHY + What Changes + Capabilities + Impact
    │   ├── design.md                       # HOW (optional — only for complex changes)
    │   ├── tasks.md                        # implementation checklist (- [ ] / - [x])
    │   └── specs/
    │       └── <capability>/
    │           └── spec.md                 # delta spec (ADDED/MODIFIED/REMOVED/RENAMED)
    └── archive/
        └── YYYY-MM-DD-<kebab-change-name>/ # completed change (moved here on archive)
```

### Lifecycle

```
propose ──► apply ──► sync ──► archive
(author)   (implement) (merge deltas) (move to dated dir)
```

Modeled on OpenSpec's OPSX command set (`propose → apply → sync → archive`). The
stages are actions, not rigid phases — during `apply` you may revisit the proposal or
delta specs as you learn, then continue.

## When to Use

Use this skill when:

- The user wants to make a **requirement-level change** to an existing capability and
  wants it captured as a reviewable proposal before implementation.
- The user mentions delta specs, change proposals, ADDED/MODIFIED/REMOVED
  requirements, brownfield/spec change management, or syncing/archiving changes
  (增量规范、变更提案、规范变更、归档变更).
- You need a paper trail of *why* and *how* a spec evolved, not just an in-place edit.

Do **not** use this skill for pure implementation with no spec-level behavior change,
or for the master project's greenfield `/speckit.*` spec flow.

## Workflow

### Stage 1 — Propose (author the change)

1. **Pick a change name** in kebab-case (e.g. `add-user-auth`, `simplify-export`).
   Validate it: lowercase letters, digits, and single hyphens only; no leading/
   trailing/consecutive hyphens, spaces, underscores, or uppercase.

2. **Create the change directory:**
   ```bash
   mkdir -p draft/changes/<change-name>/specs
   ```

3. **Fill `proposal.md`** from `./assets/proposal-template.md`. Sections:
   - **Why** — 1-2 sentences on the problem/opportunity. Why now?
   - **What Changes** — bullet list of concrete changes. Mark breaking changes with
     **BREAKING**.
   - **Capabilities** — the contract between proposal and specs:
     - *New Capabilities*: each becomes a new `draft/specs/<name>/spec.md`
       (kebab-case).
     - *Modified Capabilities*: existing capabilities whose **requirements** change.
       Reuse existing folder names under `draft/specs/`. Leave empty if no
       requirement-level change. Research `draft/specs/` before filling this in.
   - **Impact** — affected code, APIs, dependencies, systems.

   Keep it concise (1-2 pages). Focus on *why*, not *how*.

4. **Write delta specs.** For each capability listed under Capabilities, create
   `draft/changes/<change-name>/specs/<capability>/spec.md` from
   `./assets/delta-spec-template.md`. Use the delta operations:
   - `## ADDED Requirements` — new requirements.
   - `## MODIFIED Requirements` — changed behavior; **include the full updated
     requirement** (copy the whole block from the living spec, then edit).
   - `## REMOVED Requirements` — deprecations; **include `**Reason**` and
     `**Migration**`**.
   - `## RENAMED Requirements` — name-only changes; use `FROM:` / `TO:` format.

   Follow the critical rules (see "Delta Spec format" below). Full authoring rules,
   verbatim examples, and a real example are in `./references/delta-format.md`.

5. **Write `design.md`** (optional) from `./assets/design-template.md` — only for
   cross-cutting changes, new dependencies/patterns, significant data-model changes,
   or notable security/performance/migration complexity. Sections: Context, Goals /
   Non-Goals, Decisions (with alternatives), Risks / Trade-offs, and optionally
   Migration Plan and Open Questions. Focus on architecture, not line-by-line code.

6. **Write `tasks.md`** from `./assets/change-tasks-template.md`. Group tasks under
   `## N. <Group>` headings; every task MUST be a checkbox `- [ ] N.M description`.
   Order by dependency; keep each task small and verifiable. The apply stage parses
   the checkbox format — tasks not using `- [ ]` will not be tracked.

### Stage 2 — Apply (implement)

7. **Work through `tasks.md`**, implementing each task. As you complete a task, mark
   it `- [x]`. Pause on blockers or when you need clarification.

8. **Iterate freely.** If implementation reveals the design or a delta spec was wrong,
   edit the artifact and continue — do not force a wrong plan through.

### Stage 3 — Sync (merge deltas into living specs)

9. **Apply each delta into its living spec** at `draft/specs/<capability>/spec.md`.
   This is an agent-driven intelligent merge:
   - **ADDED** → add the requirement (or update it if it already exists).
   - **MODIFIED** → find the requirement by header and apply the change; **preserve
     scenarios/content not mentioned in the delta**.
   - **REMOVED** → delete the entire requirement block.
   - **RENAMED** → rename the FROM requirement to TO, preserving content.
   - If a capability has no living spec yet, create it with `## Purpose` and
     `## Requirements`.

   The merge MUST be **idempotent** — running it twice gives the same result. Full
   rules and output shape are in `./references/sync-and-archive.md`. Sync may be run
   before archive, or deferred to the archive prompt.

### Stage 4 — Archive (finalize)

10. **Confirm completion.** Check that artifacts exist and count `- [ ]` vs `- [x]` in
    `tasks.md`. Warn on incomplete artifacts/tasks and confirm before proceeding — do
    not hard-block.

11. **Assess sync state.** If delta specs exist and have not been synced, prompt to
    "Sync now (recommended)" vs "Archive without syncing", and sync first if chosen.

12. **Move the change to the dated archive:**
    ```bash
    mkdir -p draft/changes/archive
    mv "draft/changes/<change-name>" "draft/changes/archive/YYYY-MM-DD-<change-name>"
    ```
    If the target already exists, fail and suggest renaming or a different date. Then
    print a summary (change name, archive location, sync status, warnings).

## Delta Spec format

A delta spec expresses the *difference* against a living spec using `##` operation
headers. Summary of the format and the non-negotiable rules:

```markdown
## ADDED Requirements

### Requirement: <name>
The system SHALL <normative behavior>.

#### Scenario: <name>
- **WHEN** <condition>
- **THEN** <expected outcome>

## MODIFIED Requirements

### Requirement: <existing name — must match living spec>
<full updated requirement text + all scenarios>

## REMOVED Requirements

### Requirement: <name>
**Reason**: <why it is being removed>
**Migration**: <what to use instead>

## RENAMED Requirements

- FROM: `### Requirement: Old Name`
- TO: `### Requirement: New Name`
```

**Critical rules:**

- Scenarios MUST use **exactly four hashtags** (`####`). Three hashtags or bullets
  fail silently.
- **Every requirement MUST have at least one scenario.**
- MODIFIED MUST include the **full updated requirement**, with a header that matches
  the existing requirement exactly (whitespace-insensitive).
- REMOVED MUST include **`**Reason**`** and **`**Migration**`**.
- Use **SHALL / MUST** for normative requirements (avoid should/may).
- Scenarios use **WHEN / THEN** format; treat each as a potential test case.

See `./references/delta-format.md` for the complete reference (living-vs-delta
distinction, per-operation rules, and a concrete real example).

## Resources

### References (`./references/`)
- `delta-format.md` — full ADDED/MODIFIED/REMOVED/RENAMED reference with verbatim
  examples, authoring rules, the living-spec vs delta-spec distinction, and a real
  example.
- `sync-and-archive.md` — intelligent-merge rules for syncing deltas into living
  specs (idempotent, preserve unmentioned content) and the sync-then-move archive
  mechanics.

### Assets (`./assets/`)
- `proposal-template.md` — `proposal.md` scaffold (Why / What Changes / Capabilities
  / Impact).
- `delta-spec-template.md` — delta spec scaffold (ADDED requirement + scenario).
- `change-tasks-template.md` — `tasks.md` checkbox scaffold.
- `design-template.md` — optional `design.md` scaffold (Context / Goals / Decisions /
  Risks).
