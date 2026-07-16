# Test Scenario: Role/Stage/Type Conformance — Agent Templates

Layer-2 structural scenario for the redesigned conceptual model.
Contract: [conceptual-model-contract.md](../../../.specify/specs/.archive/023-agent-framework-redesign/contracts/conceptual-model-contract.md) C1–C6; data-model.md; SC-005.

## Scenario Description

Every agent template under `skills/create-agent/templates/` is inspected to confirm it
expresses the **Role × Stage × Type** model with unified terminology, and that
Type-follows-Stage coupling holds. No template may use the deprecated dimension name
"SubRole" or the deprecated stage name "improver".

## Setup

### Canonical Model (C1–C3)

```yaml
dimensions:
  role:   maps-to "agent-role-<role>-template.md"
  stage:  [executor, evaluator, optimizer]     # canonical names; "improver" was renamed to optimizer
  type:   [Worker, Meta]                        # derived from stage
type_follows_stage:
  executor:  Worker
  evaluator: Meta
  optimizer: Meta
meta_role:
  team-supervisor: Meta at all stages          # never performs real project tasks
deprecated_terms_removed: [SubRole, Subrole, improver, "Meta-Coordinator (as a role)"]  # renamed/merged
```

### Template Inventory (post-migration)

```yaml
role_templates:
  - agent-role-requirements-analyst-template.md
  - agent-role-ux-analyst-template.md
  - agent-role-system-designer-template.md
  - agent-role-module-designer-template.md
  - agent-role-test-engineer-template.md
  - agent-role-qa-engineer-template.md
  - agent-role-knowledge-manager-template.md
  - agent-role-team-supervisor-template.md      # merged Meta role
stage_templates:
  - agent-stage-executor-template.md
  - agent-stage-evaluator-template.md
  - agent-stage-optimizer-template.md           # renamed from improver
orchestration_templates:
  - agent-parallel-orchestration-template.md
  - agent-serial-orchestration-template.md
  - agent-triad-orchestration-template.md
```

## Expected Behavior

### E1: Role templates declare all three dimensions
1. Each `agent-role-*-template.md` declares its Role, the applicable Stage(s), and the resulting Type.
2. Worker roles show Worker at the executor stage; the Team Supervisor shows Meta at all stages.

### E2: Stage templates use canonical names
1. Stage templates are named `agent-stage-{executor,evaluator,optimizer}-template.md`.
2. No file is named `agent-subrole-*` (renamed to `agent-stage-*`); the deprecated "improver" name no longer appears (renamed to optimizer).

### E3: Merged Team Supervisor
1. Exactly one merged `agent-role-team-supervisor-template.md` exists.
2. `agent-role-meta-coordinator-template.md` and `agent-team-supervisor-template.md` no longer exist.

## Verification Points

### V1: Three Dimensions (C1, SC-005)
- [ ] Every `agent-role-*-template.md` declares Role, applicable Stage(s), and Type
- [ ] Stage values are drawn only from {executor, evaluator, optimizer}
- [ ] Type values are drawn only from {Worker, Meta}

### V2: Type-follows-Stage (C3)
- [ ] executor → Worker, evaluator → Meta, optimizer → Meta is honored
- [ ] The Team Supervisor (Meta role) is Meta at all stages

### V3: Unified Terminology (C1, SC-002)
- [ ] No template uses the deprecated "SubRole"/"Subrole" (renamed to Stage)
- [ ] The deprecated "improver" stage name no longer appears (renamed to optimizer)
- [ ] No template references the deprecated "Meta-Coordinator" role (merged into Team Supervisor)

### V4: Merged Supervisor (C4)
- [ ] Exactly one `agent-role-team-supervisor-template.md`
- [ ] The deprecated `agent-role-meta-coordinator-template.md` and legacy `agent-team-supervisor-template.md` no longer exist (merged/renamed)

### V5: Naming Scheme (data-model AgentTemplate)
- [ ] Role templates: `agent-role-<role>-template.md`
- [ ] Stage templates: `agent-stage-<stage>-template.md`

## Success Criteria

- All templates express Role/Stage/Type consistently (SC-005).
- Zero live occurrences of the deprecated "SubRole"/"improver"/"Meta-Coordinator (role)" vocabulary — renamed/merged (SC-002).
- Type-follows-Stage coupling holds across every template (C3/C6).
