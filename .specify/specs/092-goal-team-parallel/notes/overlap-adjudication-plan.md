# Overlap adjudication — plan stage

`overlap-check.py --repo . --spec-dir .specify/specs/092-goal-team-parallel` → `decision=overlap`,
`checked=83`, `overlaps=9`. The one current surface in the reading is `scripts/python/goal-utils.py`; the declared
delivery surface for this feature is much larger (eleven planned tests, five contracts, two declaration facts, four
owner documents), and the tool sees only paths that already exist. So the reading is a lower bound.

The nine relations are adjudicated one group at a time. The question each answer turns on: does another feature own the
path now, or does it own vocabulary that this feature rewrites? An owner that is closed and wants no further change is a
landing-point, not a conflict.

| Other spec | Relation | Ruling |
|---|---|---|
| 037-goal-registry | same-path | Landing point. 037 created `goal-utils.py`; its scope closed at the `global`/`spec`/`auto` value set this feature replaces. The replacement is the subject of FR-005/T-004; no live writer remains. |
| 053-machine-decidable-artifacts | same-path | Landing point. 053 owns the machine-decidable shape of artifacts, not the goal/team engine body. No write collision: 053 is Completed and its contract tests keep passing. |
| 085-sdd-temporary-goal-team | same-path | Deliberate supersession. 085's engine body, its tests and its routing carve-out are rewritten in place per C-91…C-105; this is the one relation that is a real ownership transfer, and it is recorded as such in plan.md T-001. |
| 027-feedback-mechanism, 033-docs-command, 056-probe-handler-system, 067-loop-efficiency-hardening, 088-speckit-visualization, 089-script-interface-contract | nested-path | Directory-level only: the relation is `scripts/python/` containing this file. No feature in the nested set writes `goal-utils.py`. 089 does constrain its CLI surface (script-interface contract), and C-84 of `command-family-and-declarations.md` keeps the new read action inside that contract rather than beside it. |

**Verdict**: no uncovered live writer. One transfer (085). One vocabulary rewrite (037's scope value set, executed as
085's successor). Six nested-path relations that resolve to "a sibling file lives in the same directory".

Two instrument limits measured while producing this record, kept because they will bite the next reader:

1. The current surface is derived from every backticked path in `feature-ref.md`, so a **planned but not yet created**
   path never appears; today the reading sees one path out of the dozens the feature will deliver.
2. The tool treats a backticked *input* path as a delivery claim (recorded in the 092 clarify feedback entry). This
   feature's `feature-ref.md` therefore names only delivered paths in backticks; inputs are cited by name.
