# Contract: Goal Definition File

**Requirement**: 037-goal-registry | **FRs**: FR-001…FR-007, FR-027…FR-032
**Artifact**: `.specify/goal/<goal-slug>/goal.md`
**Authority**: `shared/definitions/goal-definitions.md` (read-only). This contract fixes the file layout, which that document delegates to the implementing feature at its line 80.

## Location and identity

- Path: `.specify/goal/<goal-slug>/goal.md`.
- `<goal-slug>` is the goal's identity and its directory name. Grammar: first character `[A-Za-z0-9]`, remaining characters `[A-Za-z0-9_.-]`. It MUST be a safe path segment — no `/`, and not `.` or `..`.
- The identity MUST NOT be duplicated as a frontmatter field.

## Format

```markdown
---
status: active            # active | achieved | abandoned
created: 2026-08-05
updated: 2026-08-05
---

# Goal: <human-readable title>

## Objective

<One or more paragraphs stating the desired end outcome.>

## Success Criteria

1. <verifiable attainment condition>
2. <verifiable attainment condition>

## History

- 2026-08-05 — created.
```

## Field rules

| Field | Required | Rule |
|-------|----------|------|
| `status` | yes | Exactly one of `active`, `achieved`, `abandoned`. Any other value is invalid |
| `created` | yes | ISO-8601 date; set once at creation and never rewritten |
| `updated` | yes | ISO-8601 date; advanced on every authored modification |
| `## Objective` | yes | Non-empty. States an outcome |
| `## Success Criteria` | section required, content optional | An ordered list, or the explicit text `None provided.` |
| `## History` | yes | Append-only |

The Goal is composed of exactly three parts — objective, criteria, lifecycle state. `created` / `updated` are change-traceability metadata and MUST NOT be presented as a fourth part.

## Normative rules

- **GD-1** `goal.md` is an authored fact source. No derived flow may write it. A refresh that modifies this file is a write-set violation.
- **GD-2** The objective MUST state an outcome. Task lists and implementation plans are invalid objectives and MUST be rejected with a message naming the violation.
- **GD-3** One file carries exactly one objective. A composite objective MUST be split into separate `<goal-slug>` directories.
- **GD-4** The objective's subject matter is unrestricted. A goal targeting the framework itself, codebase-wide convention convergence, or a runtime outcome is valid. Absence of a corresponding functional requirement in this project MUST NOT block archival.
- **GD-5** Criteria are measured by degree. No criterion carries a current-value, percentage, or score field — those are derived and live under `summary/`.
- **GD-6** Criteria MUST NOT be copied to or from any requirements specification's `SC-xxx`. Cross-feature aggregation happens at the summary layer with each side citing its own source.
- **GD-7** `goal.md` MUST NOT enumerate functional requirements.
- **GD-8** An empty criteria set is valid. Consumers MUST then declare "no verifiable criteria provided" and MUST NOT synthesize criteria.
- **GD-9** Criterion modification MUST append a `## History` entry carrying the prior value. Silent replacement is invalid.
- **GD-10** Terminal states (`achieved`, `abandoned`) are retained in the archive. Deletion is not a lifecycle transition.

## Lifecycle transitions

| From | To | Effect |
|------|----|--------|
| *(none)* | `active` | Directory and `goal.md` created |
| `active` | `achieved` | `status` updated; file retained |
| `active` | `abandoned` | `status` updated; file retained |

No other transition is defined. `superseded` is not a state.

## Validation outcomes

| Condition | Result |
|-----------|--------|
| Identity violates the grammar or path-safety rule | Rejected; message names the offending character |
| Identity already exists | Rejected; message points at the modify path. The existing definition is not overwritten |
| `status` outside the three-value set | Rejected; message lists the valid values |
| `## Objective` missing or empty | Rejected |
| `## Success Criteria` section missing | Rejected; an empty criteria set requires the explicit `None provided.` marker |
| Objective reads as a task list | Rejected with the GD-2 violation named |
| Objective bundles more than one objective | Rejected with the GD-3 violation named; message instructs splitting into separate `<goal-slug>` directories |
