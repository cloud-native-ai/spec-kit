---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
short-description: 创建或更新项目宪法，并保持依赖模板同步
handoffs:
   - label: Refresh Feature Registry
      agent: speckit.feature
      prompt: Refresh project feature index and per-feature detail files based on the updated constitution.
      send: true
   - label: Create / Update Requirements
      agent: speckit.requirements
      prompt: Create or update a requirements specification under the updated constitutional rules.
      send: true
---

> **Concurrency obligation（执行义务，按指针抵达）**: this command is an execution body — consider concurrency first, default to it when the class and capability allow, and, when serial, name a reason code and record the `requested` / `effective` / `effective_reason` reading. Authored text: `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; class table: `shared/declarations/facts/concurrency-class.yaml`; reason codes: `shared/declarations/facts/serial-reason.yaml`; reading fields: `shared/declarations/facts/effective-concurrency.yaml`. This template restates none of their rules.

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](shared/workflow/user-input-protocol.md). Treat as governance principles, amendment intentions, or supplemental context.

## Delegation

`/speckit.constitution` creates or updates the project constitution at `/.specify/constitution.md` and keeps every dependent template in sync with the amended principles.

**Load and follow** `.specify/skills/internal/manage-constitution/SKILL.md`:

- **Inputs**: the processed `$ARGUMENTS` substance — governance principles, amendment intentions, or supplemental context; project context for the Pre-flight inference (`README.md`, the manifest file that exists, `docs/`); the template at `/.specify/templates/constitution-template.md` when the constitution file does not exist yet (bootstrap).
- **Outputs**: the updated `.specify/constitution.md` (every bracketed placeholder resolved or explicitly justified, the mandatory-principle set enforced, the `x.y.z.ddd` version bumped per the skill's MAJOR/MINOR/PATCH/DAILY rules) with the Sync Impact Report prepended as an HTML comment; the consistency-propagation checklist applied across the dependent templates (plan / requirements / tasks templates, `README.md`, `docs/tutorials/quickstart.md`) with any un-automatable file flagged; a final summary (new version + bump rationale, flagged files, suggested commit message).

The skill owns the entire workflow: pre-flight project-context inference, bootstrap + Template Cleanup Mandate, placeholder value collection, the version-increment rules, the mandatory-principle payloads, drafting and formatting rules, propagation, validation, write-back, and the edge rules (partial updates, TODO-marked missing info, never create a new template).

## Handoffs

**Before**: Use when governance/principles need introduction or amendment. If constitution exists at version ≥ 1.0.0 with no `$ARGUMENTS`, ask what amendments are desired.

**After**: `/speckit.feature` to refresh feature registry. `/speckit.requirements` for in-progress specs. `/speckit.plan` if "Constitution Check" in plan-template was modified.
