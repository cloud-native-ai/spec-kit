# Test Scenario: Role/Stage/Type Conformance — Agent Templates

Layer-2 structural scenario for the redesigned conceptual model.
Contract: [conceptual-model-contract.md](../../../.specify/specs/.archive/023-agent-framework-redesign/contracts/conceptual-model-contract.md) C1–C6; data-model.md; SC-005.

## Scenario Description

Every agent template under `skills/create-agent/templates/` is inspected to confirm it
expresses the **Role × Stage × Type** model with unified terminology, and that the
**Type-by-operating-object criterion** holds (superseding the former Type-follows-Stage
coupling from contract C3). No template may use the deprecated dimension name
"SubRole" or the deprecated stage name "improver".

## Setup

### Canonical Model (C1–C3)

```yaml
dimensions:
  role:   filled-by "agent-capacity-<X>-template.md" (worker capacities) or "agent-team-supervisor-template.md" (the Meta role)
  stage:  [executor, evaluator, optimizer]     # canonical names; "improver" was renamed to optimizer
  type:   [Worker, Meta]                        # judged by operating object, NOT derived from stage
type_criterion:                                 # supersedes the former type_follows_stage coupling
  meta:   "operates on other agents / skills / agent-defining configuration"
  worker: "operates on business artifacts and business information"
  stage_defaults:
    executor:  Worker                           # default; acts on business artifacts
    evaluator: judge-by-evaluated-object        # business artifact -> Worker; agent performance -> Meta
    optimizer: judge-by-optimized-object        # agent/skill/config -> Meta; business artifact -> Worker
meta_role:
  team-supervisor: Meta at all stages          # operating objects are inherently the agent system
deprecated_terms_removed: [SubRole, Subrole, improver, "Meta-Coordinator (as a role)"]  # renamed/merged
```

### Template Inventory (post-migration)

```yaml
role_templates:
  - agent-capacity-requirements-analyst-template.md
  - agent-capacity-ux-analyst-template.md
  - agent-capacity-system-designer-template.md
  - agent-capacity-module-designer-template.md
  - agent-capacity-test-engineer-template.md
  - agent-capacity-qa-engineer-template.md
  - agent-capacity-knowledge-manager-template.md
  - agent-team-supervisor-template.md      # merged Meta role
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
1. Each `agent-capacity-*-template.md` declares its Role seat, the applicable Stage(s), and how Type is judged.
2. Worker roles show Worker when operating on business artifacts (their normal case, at any stage); the Team Supervisor shows Meta at all stages.

### E2: Stage templates use canonical names
1. Stage templates are named `agent-stage-{executor,evaluator,optimizer}-template.md`.
2. No file is named `agent-subrole-*` (renamed to `agent-stage-*`); the deprecated "improver" name no longer appears (renamed to optimizer).

### E3: Merged Team Supervisor
1. Exactly one merged `agent-team-supervisor-template.md` exists.
2. `agent-role-meta-coordinator-template.md` and the pre-rename `agent-role-team-supervisor-template.md` no longer exist.

## Verification Points

### V1: Three Dimensions (C1, SC-005)
- [ ] Every `agent-capacity-*-template.md` declares Role seat, applicable Stage(s), and Type
- [ ] Stage values are drawn only from {executor, evaluator, optimizer}
- [ ] Type values are drawn only from {Worker, Meta}

### V2: Type judged by operating object (supersedes C3)
- [ ] No template states or implies the retired `evaluator → Meta` / `optimizer → Meta` derivation
- [ ] Each template states that Type is judged by **operating object**, with Stage as a default only
- [ ] A business-layer evaluator (e.g. one scoring repo state or a rendered artifact) is **Worker**, not Meta
- [ ] The Team Supervisor (Meta role) is Meta at all stages — its objects are the agent system

### V3: Unified Terminology (C1, SC-002)
- [ ] No template uses the deprecated "SubRole"/"Subrole" (renamed to Stage)
- [ ] The deprecated "improver" stage name no longer appears (renamed to optimizer)
- [ ] No template references the deprecated "Meta-Coordinator" role (merged into Team Supervisor)

### V4: Merged Supervisor (C4)
- [ ] Exactly one `agent-team-supervisor-template.md`
- [ ] The deprecated `agent-role-meta-coordinator-template.md` and the pre-rename `agent-role-team-supervisor-template.md` no longer exist (merged/renamed)

### V5: Naming Scheme (data-model AgentTemplate)
- [ ] Capacity templates: `agent-capacity-<X>-template.md`; the sole Meta role: `agent-team-supervisor-template.md`
- [ ] Stage templates: `agent-stage-<stage>-template.md`

## Success Criteria

- All templates express Role/Stage/Type consistently (SC-005).
- Zero live occurrences of the deprecated "SubRole"/"improver"/"Meta-Coordinator (role)" vocabulary — renamed/merged (SC-002).
- The Type-by-operating-object criterion holds across every template; the retired Type-follows-Stage derivation appears nowhere as a live rule (supersedes C3/C6).
