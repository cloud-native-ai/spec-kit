---
id: "20260730T063643Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "type-criterion-fix-20260730"
scope: "local"
partial: false
created: "2026-07-30T06:36:43Z"
summary: "Fixed the Type-follows-Stage modeling error per docs/notes/type-follows-stage-misclassification.md (Option A). Replaced the stage->type derivation with a judge-by-operating-object criterion, retaining"
---

## Review
Fixed the Type-follows-Stage modeling error per docs/notes/type-follows-stage-misclassification.md (Option A). Replaced the stage->type derivation with a judge-by-operating-object criterion, retaining the correct half (Team Supervisor always Meta). Corrected the full diffusion path: conceptual-model.md, 4 stage/triad templates, 7 role templates + 7 agent files, 3 presets, 2 instance teams, design.md including its Role x Stage matrix, and the conformance scenario. Also closed the root cause: create-team/SKILL.md step 4 never told the agent how to judge Type, so it inherited the derivation from templates. Validation: failure set identical to baseline (74), zero new failures; all skills/ and agents/ mirrors byte-identical.

## Optimization Points
- The defect was a modeling error that no test could catch: two orthogonal dimensions (Stage = horizontal process position, Type = vertical abstraction level) were bound into a one-way derivation. The conformance scenario actively *asserted* the wrong coupling, so the test suite defended the bug. When a rule is expressed as a derivation ("X follows Y"), verify the two axes are genuinely dependent before encoding it as a contract.
- The true root cause was an instruction gap, not just bad templates: `create-team/SKILL.md` step 4 told the agent to build a "Role × Stage × Type matrix" but never said how to decide Worker vs Meta. With no criterion in the workflow, the agent silently inherited the stage derivation baked into the stage templates. A schema field that a workflow never explains how to fill will be filled by whatever the templates imply.
- Error propagation followed a predictable path — spec contract → conceptual model → templates → presets → instances → docs → tests. Fixing only the reported instance (Option B) would have left presets regenerating the error on every instantiation. When a defect originates in a shared conceptual model, the fix must walk the whole diffusion path, and the note's own impact table was the right unit of work.
- Archived specs were deliberately left unmodified; supersession was recorded in the live conceptual model instead. This keeps history honest while making the current rule unambiguous — worth codifying as the standard way to retire a normative contract.
