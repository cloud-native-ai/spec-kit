# Delta Spec Format Reference

This reference captures the full authoring rules for delta specs, adapted verbatim
from OpenSpec's `spec-driven` schema (`schemas/spec-driven/schema.yaml`, artifact
`specs`) and the sync workflow templates.

---

## Living specs vs. delta specs

There are two kinds of spec files, and keeping them distinct is the central idea of
this workflow.

| | Living spec | Delta spec |
|---|---|---|
| **Location** | `draft/specs/<capability>/spec.md` | `draft/changes/<change>/specs/<capability>/spec.md` |
| **Represents** | The current, agreed-upon truth for a capability | The *intent* to change that truth |
| **Lifetime** | Permanent (evolves over time) | Temporary (lives for the duration of one change, then archived) |
| **Section headers** | `## Purpose`, `## Requirements` | `## ADDED / MODIFIED / REMOVED / RENAMED Requirements` |
| **Author** | Produced by *syncing* deltas | Hand-authored during a change |

A **living spec** describes what the system does today. A **delta spec** describes
the difference you intend to introduce. The `sync` step (see
`./sync-and-archive.md`) is what turns delta intent into living-spec truth.

### Living spec shape

```markdown
# <capability> Specification

## Purpose
<one or two sentences describing what this capability covers>

## Requirements

### Requirement: <name>
The system SHALL ...

#### Scenario: <name>
- **WHEN** <condition>
- **THEN** <expected outcome>
```

### Delta spec shape

A delta spec contains only the operation sections that apply. Optionally it may lead
with a `## Purpose` block when introducing a brand-new capability (this seeds the
living spec's Purpose at sync time).

```markdown
## ADDED Requirements
...

## MODIFIED Requirements
...

## REMOVED Requirements
...

## RENAMED Requirements
...
```

---

## Delta operations

Use `##` headers for operation groups. Under each group, list requirements with
`### Requirement: <name>` and scenarios with `#### Scenario: <name>`.

### ADDED Requirements

New requirements being introduced by this change.

- Each requirement gets a full `### Requirement: <name>` block with description and
  at least one scenario.
- At sync time: if the requirement does not exist in the living spec, it is added.
  If it already exists, it is updated to match (treated as an implicit MODIFIED).

```markdown
## ADDED Requirements

### Requirement: User can export data
The system SHALL allow users to export their data in CSV format.

#### Scenario: Successful export
- **WHEN** user clicks "Export" button
- **THEN** system downloads a CSV file with all user data
```

### MODIFIED Requirements

Changed behavior on an existing requirement.

- **MUST include the full updated requirement content.** The header text must match
  the existing requirement's header exactly (whitespace-insensitive) so the sync
  step can locate it.
- Copy the ENTIRE requirement block from the living spec, then edit it to reflect
  the new behavior.

**MODIFIED requirements workflow:**
1. Locate the existing requirement in `draft/specs/<capability>/spec.md`.
2. Copy the entire requirement block (from `### Requirement:` through all scenarios).
3. Paste under `## MODIFIED Requirements` and edit to reflect the new behavior.
4. Ensure the header text matches exactly (whitespace-insensitive).

**Common pitfall:** Using MODIFIED with partial content loses detail at archive
time. If you are adding new concerns without changing existing behavior, use ADDED
instead.

> Note: at *sync* time the agent can apply partial MODIFIED intent intelligently
> (e.g. add a single scenario without recopying the others). But when authoring a
> delta that is intended to fully replace a requirement, include the complete block
> so no detail is lost. When in doubt, include the full block.

```markdown
## MODIFIED Requirements

### Requirement: User can export data
The system SHALL allow users to export their data in CSV and JSON formats.

#### Scenario: Successful CSV export
- **WHEN** user clicks "Export" and selects CSV
- **THEN** system downloads a CSV file with all user data

#### Scenario: Successful JSON export
- **WHEN** user clicks "Export" and selects JSON
- **THEN** system downloads a JSON file with all user data
```

### REMOVED Requirements

Requirements being deprecated/removed.

- **MUST include `**Reason**` and `**Migration**`** so future readers understand why
  it was removed and what to use instead.
- At sync time: the entire requirement block is removed from the living spec.

```markdown
## REMOVED Requirements

### Requirement: Legacy export
**Reason**: Replaced by new export system
**Migration**: Use new export endpoint at /api/v2/export
```

### RENAMED Requirements

Name-only changes (no behavior change). Use the FROM/TO format.

- At sync time: the FROM requirement is located and its header renamed to TO;
  content is preserved.

```markdown
## RENAMED Requirements

- FROM: `### Requirement: Old Name`
- TO: `### Requirement: New Name`
```

---

## Critical authoring rules

These rules come straight from the schema instruction and cause silent failures if
ignored.

1. **Scenarios MUST use exactly four hashtags (`####`).** Using three hashtags or
   bullets will fail silently — the scenario will not be recognized.
2. **Every requirement MUST have at least one scenario.** A requirement with no
   scenario is incomplete.
3. **Use SHALL / MUST for normative requirements.** Avoid should / may — specs
   should be testable and unambiguous.
4. **MODIFIED must include the full updated requirement content** and a header that
   matches the existing requirement exactly.
5. **REMOVED must include `**Reason**` and `**Migration**`.**
6. **Each scenario uses WHEN / THEN format** (`- **WHEN** ...` / `- **THEN** ...`).
   Additional `- **THEN**` lines may be chained for multiple outcomes.
7. **Specs should be testable** — treat each scenario as a potential test case.
8. Use the exact kebab-case capability name from the proposal for new capabilities;
   for modified capabilities reuse the existing folder name under `draft/specs/`.

---

## Concrete real example

The following is drawn from a real OpenSpec change (`simplify-skill-installation`),
which introduced a new `propose-workflow` capability. The delta spec led with a
`## Purpose` block (seeding the living spec) followed by `## ADDED Requirements`.

```markdown
## Purpose

The propose workflow SHALL combine change creation and artifact generation into a
single command, reducing friction for new users while teaching them the workflow
through embedded guidance.

## ADDED Requirements

### Requirement: Propose workflow creation
The system SHALL provide a `propose` workflow that creates a change and generates
all artifacts in one step.

#### Scenario: Basic propose invocation
- **WHEN** user invokes `/opsx:propose "add user authentication"`
- **THEN** the system SHALL create a change directory with kebab-case name
- **THEN** the system SHALL generate all artifacts needed for implementation:
  proposal.md, design.md, specs/, tasks.md

#### Scenario: Propose with existing change name
- **WHEN** user invokes `/opsx:propose` with a name that already exists
- **THEN** the system SHALL ask if user wants to continue existing change or create new
- **THEN** in non-interactive mode: the system SHALL fail with error suggesting a
  different name

### Requirement: Propose workflow onboarding UX
The `propose` workflow SHALL include explanatory output to help new users understand
the process.

#### Scenario: First-time user guidance
- **WHEN** user invokes `/opsx:propose`
- **THEN** the system SHALL explain what artifacts will be created
- **THEN** the system SHALL indicate the next step to implement
```

After this change is synced, `draft/specs/propose-workflow/spec.md` (a living spec)
would contain a `## Purpose` section and a `## Requirements` section holding those
two requirements with their scenarios.
