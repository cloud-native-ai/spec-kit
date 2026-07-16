# Data Model: Project Glossary Mechanism

**Feature**: 031 Glossary Mechanism | **Spec**: [requirements.md](./requirements.md) | **Plan**: [plan.md](./plan.md)

The glossary is a **document artifact**, so the "data model" is the logical schema of `.specify/memory/glossary.md` (a Markdown file) plus the transient in-prompt concepts used during correction and conflict handling. No database, no runtime objects.

## Entity: Glossary (词汇表)

The single project-wide collection of domain/project terms. Exactly one per project (FR-014).

| Attribute | Type | Rule |
|-----------|------|------|
| location | path | Always `.specify/memory/glossary.md` (canonical, one per project). |
| entries | list of Glossary Entry | Zero or more; empty-but-valid on a brand-new project (edge case). |
| header/preamble | Markdown | Carries authoring rules (common words excluded; user-authoritative; conflict protocol) seeded from `glossary-template.md`. |

Grounding: FR-001 (initialized at instruction generation), FR-012 (durable, human-readable), FR-014 (single project-wide).

## Entity: Glossary Entry (词条)

One row = one canonical term and everything needed to anchor input to it.

| Field | Type | Required | Rule |
|-------|------|----------|------|
| `canonical` | string | yes | The agreed project term. Unique key within the glossary (case-insensitive). Excludes common everyday words (FR-002). |
| `variants` | list<string> | no | Known homophones / easily-confused / dictation-error forms that MUST anchor back to `canonical` (FR-003, FR-005). May be empty. |
| `meaning` | string | yes | Brief domain definition — the lightweight domain-knowledge payload (FR-003). |
| `origin` | enum(`auto`, `user`) | yes | `auto` = framework-proposed; `user` = manually authored/confirmed. Governs precedence (FR-011). |
| `status` | enum(`proposed`, `confirmed`) | yes | `proposed` = awaiting user confirmation; `confirmed` = accepted. User edits are `user`+`confirmed`. |

**Identity & uniqueness**: `canonical` is the key. A second entry whose `canonical` (or a `variant`) collides with an existing entry under a *different meaning* is not stored directly — it raises a **Conflict** (below).

**Precedence rule (FR-011)**: When an `auto` proposal targets a term that already has a `user` entry, the `user` entry wins; the proposal is discarded unless the user explicitly confirms a change.

**Lifecycle / state transitions**:

```
(none) --auto-propose--> proposed(auto) --user confirms--> confirmed(auto→treated as accepted)
(none) --user adds------> confirmed(user)
proposed(auto) --user edits value--> confirmed(user)   # manual edit is authoritative
confirmed(*) --user removes--> (none)                  # removal never fails downstream (edge case)
any add/edit that collides --> raises Conflict (must resolve before write)
```

Grounding: FR-002, FR-003, FR-005, FR-010, FR-011.

### Representation in `glossary.md` (illustrative)

A Markdown table (exact columns fixed by `contracts/glossary-file-format.md`):

| Canonical | Variants | Meaning | Origin | Status |
|-----------|----------|---------|--------|--------|
| Spec Kit | speckit, spec-kit, 词条工具 | The SDD CLI toolkit that generates `.specify/` structure | user | confirmed |
| constitution | constitution，宪法, constetution | Project governance principles file | auto | confirmed |

## Entity: Conflict

A transient relationship surfaced when a candidate term (auto-proposed or manually entered) clashes with existing entries. Not persisted as a row; it is a decision point that MUST be resolved before any conflicting write (FR-008/FR-009).

| Field | Type | Rule |
|-------|------|------|
| `candidate` | Glossary Entry (partial) | The term being added/changed. |
| `collidesWith` | list<Glossary Entry> | Existing entry/entries it clashes with. |
| `kind` | enum(`same-term-diff-meaning`, `homophone/near-duplicate`, `ambiguous-variant`) | Classifies the clash (maps to spec edge cases). |
| `resolution` | enum(`keep-existing`, `replace`, `merge-variant`, `add-distinct`, `defer`) | Chosen by the **user**; framework MUST NOT auto-resolve (FR-007/FR-009). |

**Rule**: No conflicting change is written to `glossary.md` without an explicit user `resolution` (FR-009). Ambiguous variants (map to >1 canonical) always `defer` to the user (FR-007).

Grounding: FR-007, FR-008, FR-009; edge cases "same spelling/different meaning", "homophone with distinct spelling", "ambiguous variant", "conflicting manual entries".

## Non-persisted concept: Correction

When a workflow command interprets input, a variant→canonical substitution is a **correction**. It is applied for interpretation only (never a destructive rewrite of the user's literal text) and MUST be surfaced so the user can override it (FR-005/FR-006). Corrections are prompt-time behavior, not stored data.
