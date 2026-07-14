# Contract: Feedback Entry & Store File Schema

**Feature**: 028 Feedback Mechanism | **Type**: File-format contract

Defines the on-disk representation of the feedback store under `.specify/memory/feedback/`. Format mirrors the memory-as-files store (`memory-utils.py`): Markdown files with frontmatter plus one `index.json`.

## Layout

```
.specify/memory/feedback/
  <created-ts>-<unit-slug>.md    # one file per recorded run
  index.json                     # store metadata + entry mirror
  .gitkeep                       # already present
```

- `<created-ts>` MUST be `YYYYMMDDTHHMMSSZ` (UTC).
- `<unit-slug>` is derived from `unit_id` (e.g. `/speckit.plan` → `speckit-plan`, `skill:analysis-project` → `skill-analysis-project`).

## Entry file schema

Frontmatter (delimited by `---`), then a Markdown body.

```markdown
---
id: "20260713T170000Z-speckit-plan"
unit_id: "/speckit.plan"
unit_type: "command"
run_id: "027-feedback-mechanism-20260713T1700"
scope: "local"
feature: "027-feedback-mechanism"
partial: false
created: "2026-07-13T17:00:00Z"
summary: "Plan run was smooth; classification table required manual command triage."
---

## Review
<prose review of the just-completed run, judged against the unit's declared purpose>

## Optimization Points
- <actionable, unit-specific point 1>
- <point 2>
```

**Normative rules**
- `scope` MUST be the literal `local`. A global/whole-project assessment MUST NOT appear here (FR-005).
- The body MUST contain a `## Review` section and a `## Optimization Points` section.
- `## Optimization Points` MUST contain at least one bullet. A clean run uses exactly: `- No significant optimization points identified this run.` (Edge "No optimization points found").
- When `partial: true`, the `## Review` MUST begin with a partial-run label, e.g. `**Partial run** — ` (FR-009).
- Entry files are immutable once written; corrections create a new entry, they never overwrite an existing `id`.

## `index.json` schema

```json
{
  "store": "feedback",
  "updated": "2026-07-13T17:00:00Z",
  "threshold": 10,
  "count_since_submission": 3,
  "submitted_at": null,
  "entries": [
    {
      "id": "20260713T170000Z-speckit-plan",
      "file": "20260713T170000Z-speckit-plan.md",
      "unit_id": "/speckit.plan",
      "unit_type": "command",
      "run_id": "027-feedback-mechanism-20260713T1700",
      "feature": "027-feedback-mechanism",
      "partial": false,
      "created": "2026-07-13T17:00:00Z",
      "summary": "Plan run was smooth; classification table required manual command triage."
    }
  ]
}
```

**Normative rules**
- `entries` MUST be sorted by `created` descending.
- `count_since_submission` MUST equal the number of new entries recorded since the last `mark-submitted` (or since store creation).
- `threshold` default is `10`; a value supplied via `--threshold` or `SPECKIT_FEEDBACK_THRESHOLD` persists into the index.
- The index MUST be reconstructable from entry files via `reindex` (except `submitted_at`, which is preserved).
