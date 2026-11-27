# Context Management(上下文管理)

Fixture owner document for the context-management guard family. The `## Forms`
table owns the form-by-layer legality matrix; the `## Layout` table owns the
per-row data. The audit engine reads both tables; the guard tests pin their shapes.

## Forms

| form | legal layers |
|------|--------------|
| `pointer` | system, project, task |
| `read-in-full` | project |
| `bounded-index` | project, task |
| `runtime-discovery` | system |
| `inline-digest` | task |

cap_required_forms: bounded-index

## Layout

| class id | layer | form | source | owner | cap reference |
|----------|-------|------|--------|-------|---------------|
| `runtime-environment` | system | `runtime-discovery` | runtime-discovery:platform | engine probe | — |
| `reality-constraints` | system | `pointer` | docs/constraints.md | fixture owner | — |
| `reality-constraints` | system | `pointer` | docs/constraints.md | fixture owner | — |
| `governance-baseline` | project | `read-in-full` | .specify/constitution.md, .specify/instructions.md | fixture owner | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `project-vocabulary` | project | `pointer` | .specify/glossary.md | fixture owner | — |
| `concept-definitions` | project | `bounded-index` | .specify/shared/definitions/ | fixture owner | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `concept-explanations` | project | `pointer` | .specify/skills.md, .specify/tools.md | fixture owner | — |
| `task-artifacts` | task | `bounded-index` | .specify/specs/ | fixture owner | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `task-memory` | task | `bounded-index` | .specify/session/, .specify/knowledge/ | fixture owner | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `task-statement` | task | `inline-digest` | .specify/shared/workflow/user-input-protocol.md | fixture owner | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
