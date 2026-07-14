# Data Model: Framework Feedback Mechanism

**Feature**: 028 Feedback Mechanism | **Spec**: [requirements.md](./requirements.md) | **Plan**: [plan.md](./plan.md)

This model is derived from the Key Entities in `requirements.md`. The feedback store is a **file-based** store (Markdown entries + a JSON index), mirroring the existing memory-as-files engine — there is no database and no service API.

## Entity: Feedback Entry

A record produced at the wrap-up of one qualifying run. Persisted as one Markdown file under `.specify/memory/feedback/<created-ts>-<unit-slug>.md` with frontmatter + body.

| Field | Type | Required | Constraints / Notes |
|-------|------|----------|---------------------|
| `id` | string | Yes | `<created-ts>-<unit-slug>` (unique per run); doubles as the filename stem. |
| `unit_id` | string | Yes | Canonical identifier of the evaluated unit. Skill: `skill:<name>`. Command: `/speckit.<command>`. Matches the memory `--source` grammar. |
| `unit_type` | enum | Yes | `skill` \| `command`. |
| `run_id` | string | Yes | Opaque per-run identifier used for dedup keying `(unit_id, run_id)`. |
| `scope` | const | Yes | Always `local` — distinguishes from the global `/speckit.review` report (FR-005). |
| `review` | string | Yes | Short prose review of the just-completed execution, written against the unit's declared purpose (FR-003). |
| `points` | list<string> | Yes | ≥1 actionable, unit-specific optimization point, OR exactly one explicit "no significant optimization points identified this run" (FR-003, SC-003). |
| `partial` | bool | No (default `false`) | `true` when the run aborted/failed before wrap-up; the `review` MUST be labeled as covering a partial run (FR-009). |
| `feature` | string | No | Feature key/ID if the run was feature-scoped (informational). |
| `created` | ISO-8601 UTC | Yes | Timestamp, `YYYY-MM-DDTHH:MM:SSZ`. |
| `summary` | string | Yes (derived) | First non-empty line of `review`, ≤200 chars (index preview). |

**Validation rules**
- `unit_id` MUST match `^(?:/speckit\.[a-z0-9._-]+|skill:[a-z0-9._-]+)$` (rejects arbitrary sources — same boundary as `memory-utils.py`).
- `scope` MUST equal `local`; any global/project-wide assessment is out of scope (FR-005, Edge "Overlap with global review").
- `points` MUST be non-empty. A clean run uses the explicit no-op sentence rather than an empty list (Edge "No optimization points found").
- A `record` for an existing `(unit_id, run_id)` pair is a no-op (FR-008 / SC-005).

## Entity: Feedback Store

The accumulating collection under `.specify/memory/feedback/`, indexed by `index.json`.

`index.json` schema:

| Field | Type | Notes |
|-------|------|-------|
| `store` | const `feedback` | Store discriminator. |
| `updated` | ISO-8601 UTC | Last mutation time. |
| `threshold` | int | Consolidated-prompt threshold. Default **10**; overridable via `--threshold` / `SPECKIT_FEEDBACK_THRESHOLD`. |
| `count_since_submission` | int | Entries recorded since the last submission; reset to 0 by `mark-submitted`. |
| `submitted_at` | ISO-8601 UTC \| null | Timestamp of the most recent submission acknowledgement. |
| `entries` | list<EntryMeta> | Mirror of each entry's `id, file, unit_id, unit_type, run_id, feature, created, summary, partial`; sorted by `created` desc. |

**Invariants**
- `count_since_submission` increments by 1 only on a *new* (non-duplicate) `record`.
- `should_prompt` (computed) = `count_since_submission >= threshold` (SC-007).
- Concurrent writers MUST NOT corrupt the store: writes are last-write-wins on the index with per-entry files never overwritten across distinct `id`s (Edge "Concurrent writes").

## Entity: Feedback Trigger Policy (rules, not stored)

The decision rule for which flows emit feedback. Not persisted; encoded in the convention + command classification contract.

- **All skills** qualify by default (FR-002).
- **Complex commands only** qualify (FR-006): a command qualifies iff it (a) invokes scripts/CLI tools, (b) produces an artifact consumed by another flow, or (c) consumes another flow's artifact.
- **Trivial/short flows** never qualify (FR-007).
- Simple commands (`agents`, `constitution`, `feature`, `team`) are explicitly excluded (see `contracts/command-classification.md`).

## Entity: Target Unit (reference)

The skill or command under evaluation. The entry binds to its declared purpose so `points` are specific to it. Resolved from:
- Skill: the `name` + `description`/`## Overview` of its `SKILL.md`.
- Command: the `description` frontmatter + goal of its `templates/commands/<name>.md`.

## Entity: Submission Prompt (transient)

A consolidated, one-time notification raised when `should_prompt` becomes true. Not persisted as data; it is an agent-surfaced message inviting the user to submit collected feedback to the Spec Kit developers. Acknowledging submission triggers `mark-submitted` (resets `count_since_submission`, stamps `submitted_at`).

## Entity: Global Review Report (external reference)

The existing `/speckit.review` artifact — whole-project, maintainer-facing. Referenced only to delineate scope: local Feedback Entries complement it and MUST NOT duplicate its global perspective (FR-005, SC-006).

## State Transitions

**Feedback Store accumulation**

```
[empty] --record--> [accumulating] --record(xN)--> [at/over threshold: should_prompt=true]
   ^                                                        |
   |------------------- mark-submitted ---------------------|
                (count_since_submission := 0, submitted_at := now)
```

**Single run**

```
run start -> ... work ... -> wrap-up gate
   ├─ qualifying + completed -> record(partial=false)   (idempotent per run_id)
   ├─ qualifying + aborted   -> record(partial=true) OR skip   (FR-009)
   └─ non-qualifying (trivial/simple command) -> no record     (FR-007)
```
