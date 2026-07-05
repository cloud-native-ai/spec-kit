# Sync and Archive Reference

This reference captures the intelligent-merge (sync) rules and the archive mechanics,
adapted from OpenSpec's `sync-specs` and `archive-change` workflow templates.

Both operations are **agent-driven**: you read files and edit them directly. There is
no programmatic merge engine — the leverage comes from your judgment applying delta
*intent* to living specs.

---

## Part 1 — Sync: apply deltas into living specs

Sync reads a change's delta specs and edits the living specs at
`draft/specs/<capability>/spec.md` to apply the intended changes. This allows
intelligent merging (e.g. adding a single scenario without recopying an entire
requirement).

### Steps

1. **Resolve the change.** Determine which change to sync
   (`draft/changes/<change>/`). If ambiguous, prompt the user — do not guess or
   auto-select.

2. **Find delta specs.** Enumerate
   `draft/changes/<change>/specs/<capability>/spec.md`. If none exist, inform the
   user and stop.

3. **For each delta spec, apply changes to the living spec:**
   a. Read the delta spec to understand the intended changes.
   b. Read the living spec at `draft/specs/<capability>/spec.md` (may not exist yet).
   c. Apply changes intelligently (see rules below).
   d. If the capability has no living spec yet, create it.

4. **Show a summary** of which capabilities were updated and what changed
   (requirements added / modified / removed / renamed).

### Merge rules per operation

**ADDED Requirements**
- If the requirement does not exist in the living spec → add it.
- If the requirement already exists → update it to match (treat as an implicit
  MODIFIED).

**MODIFIED Requirements**
- Find the requirement in the living spec by matching header text.
- Apply the change, which may be any of:
  - Adding new scenarios (you do not need to copy existing ones).
  - Modifying existing scenarios.
  - Changing the requirement description.
- **Preserve scenarios/content not mentioned in the delta.**

**REMOVED Requirements**
- Remove the entire requirement block from the living spec.

**RENAMED Requirements**
- Find the FROM requirement and rename it to TO. Preserve its content.

### Creating a new living spec

If the capability does not exist yet:
- Create `draft/specs/<capability>/spec.md`.
- Add a `## Purpose` section (may be brief; use the delta's `## Purpose` if present,
  otherwise mark TBD).
- Add a `## Requirements` section containing the ADDED requirements.

### Key principle: intelligent merging

Unlike programmatic merging, you apply **partial updates**:
- To add a scenario, include just that scenario under MODIFIED — do not copy existing
  scenarios.
- The delta represents *intent*, not a wholesale replacement.
- Use your judgment to merge changes sensibly.

### Guardrails

- Read both the delta and the living spec before making changes.
- Preserve existing content not mentioned in the delta.
- If something is unclear, ask for clarification.
- Show what you are changing as you go.
- **The operation MUST be idempotent** — running it twice gives the same result.

### Sync success output (shape)

```
## Specs Synced: <change-name>

Updated living specs:

**<capability-1>**:
- Added requirement: "New Feature"
- Modified requirement: "Existing Feature" (added 1 scenario)

**<capability-2>**:
- Created new spec file
- Added requirement: "Another Feature"

Living specs are now updated. The change remains active — archive when
implementation is complete.
```

---

## Part 2 — Archive: finalize a completed change

Archiving moves a completed change out of the active set and into a dated archive
directory. The canonical pattern is **sync-then-move**: ensure delta intent has been
merged into living specs, then relocate the change directory.

### Steps

1. **Resolve the change.** If not provided, prompt for selection among active
   (non-archived) changes. Do not guess.

2. **Check artifact completion.** Verify `proposal.md`, delta specs, `design.md`
   (if present), and `tasks.md` exist as expected. If artifacts are missing/
   incomplete, warn and confirm with the user before proceeding.

3. **Check task completion.** Read `tasks.md` and count `- [ ]` (incomplete) vs
   `- [x]` (complete). If incomplete tasks remain, warn and confirm. If there is no
   tasks file, proceed without a task warning.

4. **Assess delta sync state.** Check for delta specs under
   `draft/changes/<change>/specs/`. If none exist, proceed without a sync prompt.
   If delta specs exist:
   - Compare each with its living spec at `draft/specs/<capability>/spec.md`.
   - Determine what would be applied (adds/modifications/removals/renames).
   - Show a combined summary, then prompt:
     - If changes are needed: "Sync now (recommended)" / "Archive without syncing".
     - If already synced: "Archive now" / "Sync anyway" / "Cancel".
   - If the user chooses to sync, run the sync procedure (Part 1) first. Proceed to
     archive regardless of the choice.

5. **Perform the archive.**
   - Ensure the archive directory exists: `draft/changes/archive/`.
   - Compute the target name using the current date: `YYYY-MM-DD-<change-name>`.
   - If the target already exists → fail with an error (suggest renaming the
     existing archive or using a different date).
   - Otherwise move the change directory into the archive:

   ```bash
   mkdir -p draft/changes/archive
   mv "draft/changes/<change-name>" "draft/changes/archive/YYYY-MM-DD-<change-name>"
   ```

6. **Display a summary** including the change name, archive location, whether specs
   were synced, and any warnings (incomplete artifacts/tasks).

### Archive success output (shape)

```
## Archive Complete

**Change:** <change-name>
**Archived to:** draft/changes/archive/YYYY-MM-DD-<name>/
**Specs:** ✓ Synced to living specs   (or "No delta specs" or "Sync skipped")

All artifacts complete. All tasks complete.
```

### Archive error output (target exists)

```
## Archive Failed

**Change:** <change-name>
**Target:** draft/changes/archive/YYYY-MM-DD-<name>/

Target archive directory already exists.

Options:
1. Rename the existing archive
2. Delete the existing archive if it is a duplicate
3. Wait until a different date to archive
```

### Guardrails

- Always prompt for change selection if not provided.
- Do not block the archive on warnings — inform and confirm instead.
- The whole change directory (including any metadata files) moves together.
- If delta specs exist, always run the sync assessment and show the combined summary
  before prompting.
- Show a clear summary of what happened.
