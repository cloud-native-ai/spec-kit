# /speckit.constitution

Create or update the project constitution — the non-negotiable principles and governance rules that guide all development work.

## When to Use

- During project setup to establish core principles and governance
- When governance rules need to be amended
- After significant architectural or policy changes that affect project principles
- To ensure all dependent templates stay in sync with constitutional updates

## Syntax

```text
/speckit.constitution [constitutional update or query]
```

`[constitutional update or query]` is optional — specify principle changes, additions, or amendments.

## Execution Flow

1. **Pre-flight: project context inference** — Scans the project to understand its actual context:
   - Reads README, build configuration (`pyproject.toml`, `package.json`, etc.)
   - Determines language(s), framework(s), project type, and domain context
   - Uses inferred context to reject irrelevant template principles and replace with domain-appropriate ones

2. **Ensure constitution exists** — If `.specify/memory/constitution.md` doesn't exist, generates it from `constitution-template.md`, immediately adapting to the project's actual context:
   - Resolves ALL bracketed placeholders
   - Replaces generic principles with project-relevant ones
   - Removes unused template sections
   - Deletes instructional comments

3. **Collect/derive values** — For each placeholder token:
   - Uses user-supplied values from conversation
   - Infers from repo context (README, docs, prior constitution)
   - Governance dates: `RATIFICATION_DATE` (original adoption), `LAST_AMENDED_DATE` (today if changed)
   - Version follows `x.y.z.ddd` format with semantic increment rules

4. **Draft updated constitution**:
   - Replaces every placeholder with concrete text
   - Ensures each principle has: name, non-negotiable rules, and explicit rationale
   - **Must include** a "Feature-centric development" principle
   - Ensures Governance section lists amendment procedure, versioning policy, and compliance review

5. **Consistency propagation** — Verifies ALL principle references match in dependent files:
   - `plan-template.md` → Constitution Check principle list
   - `requirements-template.md` → Feature binding section
   - `tasks-template.md` → Constitution principle references
   - `README.md` and `quickstart.md` → Principle references
   - Flags files that cannot be updated automatically

6. **Sync Impact Report** — Documents:
   - Version change (old → new) with bump type
   - Modified, added, and removed principles
   - Templates requiring updates (✅ updated / ⚠ pending)

7. **Validation** — No unexplained bracket tokens, version matches `x.y.z.ddd`, dates ISO format, principles are declarative and testable.

8. **Write and report** — Overwrites `.specify/memory/constitution.md` and outputs version, bump rationale, files needing follow-up, and suggested commit message.

## Version Scheme

| Bump | When | Example |
|------|------|---------|
| MAJOR (x) | Complete restructuring, backward-incompatible removals | `1.0.0.0` → `2.0.0.1` |
| MINOR (y) | Adding/removing/renaming principles | `1.2.0.0` → `1.3.0.1` |
| PATCH (z) | Clarifications, wording improvements, typo fixes | `1.2.3.0` → `1.2.4.1` |
| DAILY (ddd) | Every update (always increments) | `1.2.3.15` → `1.2.3.16` |

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Constitution | `.specify/memory/constitution.md` |
| Updated templates | `.specify/templates/plan-template.md`, etc. |

## Prerequisites

- Use when governance/principles need to be introduced or amended

## Next Steps

- Run [`/speckit.feature`](feature.md) to refresh the feature index under updated rules
- Run [`/speckit.requirements`](requirements.md) for in-progress specs to ensure alignment
- If the Constitution Check in `plan-template.md` was modified, run [`/speckit.plan`](plan.md) on open specs
