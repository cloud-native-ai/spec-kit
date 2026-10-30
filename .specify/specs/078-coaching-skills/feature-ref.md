# Feature Reference: 078-coaching-skills

**Requirement → Feature**: `078-coaching-skills` → Feature 078 Coaching Skills（教练技能）

## Binding

| Field | Value |
|-------|-------|
| Feature ID | 078 |
| Feature name | Coaching Skills（教练技能） |
| Feature index row | `.specify/memory/features.md` |
| Feature detail | `.specify/memory/features/078.md` |
| Spec | `.specify/specs/078-coaching-skills/requirements.md` |
| Status before this plan | Draft |
| Status after this plan | Planned |
| New feature created? | No — the row was registered at `/speckit.clarify` and this plan advances it |

## How This Plan Maps to the Feature

| Plan artifact | Feature-level meaning |
|---------------|----------------------|
| `plan.md` § Summary / Technical Context | What the coach loop is and the zero-new-runtime route that delivers it |
| `plan.md` § Mirror Obligations | The rename half of the feature: source edit → derived regeneration |
| `data-model.md` | The run record vocabulary: CoachRun, TraineeTarget, ExpectationCriteria, ObservationStep, DeviationFinding, ImprovementEntry, RunStatus |
| `contracts/coaching-run.contract.md` | Feature Key Change 1 (rename) + 2 (loop) + 5 (run directory, one file per record) |
| `contracts/expectation.contract.md` | Feature Key Change 2: the two-dimension expectation produced by the former simulation procedure |
| `contracts/observation.contract.md` | Feature Key Change 4: per-step observation, source tagging, gap marking |
| `contracts/dispatch-payload.contract.md` | Feature Key Change 3: dual independent contexts, verbatim `<work>` |
| `contracts/identity-and-wiring.contract.md` | Feature Key Change 1 and Implementation Notes: the closed wiring surface by reference to requirements A10 (with the guard-copy derivation for the residual audit), derived faces, frozen tests, history boundary |
| `quickstart.md` | Acceptance path for SC-001…SC-009, plus the FR-traceability verification boundary owned by plan § Phase 1 |

## Feature-List Review

- **New features introduced by this plan**: none. The plan does not split 078 into slices; the requirements budget (29 FR) stays a single feature.
- **Deprecated or merged features**: none. Feature 057's modify-family boundary gains a renamed member; the boundary itself is unchanged.
- **Non-functional classification**: unchanged — the feature remains a functional capability (skill behavior + wiring), not an infrastructure change.
- **Cross-feature notes recorded in the detail file**: the rename chain `thought-experiment-verifier → think-skills → coaching-skills` stays recorded in `_OBSOLETE_SKILLS`' comment area (without repeating the old literal; see plan Phase 0 finding 2).

## Status Advance Evidence

`Draft → Planned` per `.specify/templates/feature-details-template.md` § Canonical Status State Machine: `plan.md`, `data-model.md`, `contracts/`, `quickstart.md` exist for the bound requirement, and the Constitution Check has no unjustified Fail or Partial row. Status `Implemented` is NOT claimed here; that transition belongs to `/speckit.implement`.
