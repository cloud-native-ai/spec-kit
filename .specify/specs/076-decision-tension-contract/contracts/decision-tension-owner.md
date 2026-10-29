# Contract: 规范 owner 与判据（decision-tension-owner）

**Feature**: 076-decision-tension-contract → Feature 076 决策反题与反指标契约（Decision Tension Record）
**FR 覆盖**: FR-001…FR-007
**载体**: `shared/guidelines/decision-tension.md`（新建）、`.specify/shared/guidelines/decision-tension.md`（镜像）

本契约规定新建 owner 文件必须承载什么、不得承载什么。它是该文件的验收面，不是该文件的替代物：
判据正文只在 owner 内定义一次，本文件只断言「存在、封闭、以路径引用相邻 owner」。

## 条款

- **C-1** (owner declaration): the file opens by declaring what it owns — the six-field record shape, the admissibility criteria, the rejection forms, the load-bearing threshold, the boundary to adjacent owners, and the record identifier form — and MUST state that every consumer references this file by path instead of restating its criteria table, rejection list, or threshold table. (FR-001)
- **C-2** (closed six fields): the record MUST be the six fields `decision`, `antithesis`, `binding_constraints` (with both `pole_a` and `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`, plus the record identifier `tension_id` of form `T-NNN` (three digits, unique inside one plan, increasing in document order); the field set is closed and extending, renaming or removing a field is an owner revision, never a per-consumer extension. (FR-002)
- **C-3** (admissibility, closed four): the owner MUST define admissibility as a closed set of four jointly-required criteria — `decision` names one chosen pole in a single sentence; `antithesis` is an independently adoptable named proposal with at least one «under which condition it is better» statement; both pole constraints are non-empty and the chosen option does not satisfy both; `discriminating_evidence` is an executable, two-valued observation available to one reviewer. (FR-003)
- **C-4** (rejection forms, closed): the owner MUST define a closed rejection list whose first entry is the literal `expected_sacrifice: none`, and which also covers an empty pole, a non-executable or non-binary discriminating evidence, a straw-man antithesis, and undecidable wording that substitutes for a trade-off; adding an entry is an owner revision; the owner MUST also name the judge of each entry — the machine-decidable three (the literal `none`, an empty pole, a hit on the undecidable-wording list) belong to the validator, while the two semantic ones (straw-man antithesis, non-executable or non-binary evidence) belong to two reviewers applying one criterion who MUST reach the same verdict. (FR-004)
- **C-5** (load-bearing threshold): the owner MUST define the threshold as four triggers — irreversible (rollback needs migration or rebuild), cross-team (changes a contract or interface others depend on), high blast radius (failure spreads beyond this feature's boundary), and constitution-related (touches any MUST clause) — any one of which makes the decision load-bearing, and MUST state that a decision meeting none MUST NOT be asked for a record and a missing record MUST NOT be judged a defect. (FR-005)
- **C-6** (complexity gating): the owner MUST gate the requirement on the grades owned by `shared/guidelines/task-complexity-rubric.md`, MUST state that a Trivial task contains no load-bearing decision by definition and therefore never triggers a record, and MUST resolve a conflict between grade and threshold by that rubric's tie-break, with the threshold deciding whether a record is required. (FR-006)
- **C-7** (adjacent owners): the owner MUST declare its division of labour with the four adjacent mechanisms — `shared/definitions/derivation-definitions.md` § Contradiction Handling, `/speckit.clarify` and the interview ledger, `shared/guidelines/fast-fail.md`, and `shared/guidelines/critique-and-self-critique.md` — each by path reference only, and MUST bound itself to technical trade-offs made after a direction is chosen, excluding requirement-stage disagreement. (FR-007)
- **C-8** (no second definition): the owner MUST NOT restate any adjacent owner's rule, table or enumeration, and MUST NOT introduce a persistence carrier, a scheduler, a scorer or a runtime; its consumer list is pointer-shaped (consumer path + how it references), not a copy of any field list. (FR-001, FR-007)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-1 | FR-001 | test_owner_declares_ownership_and_pointer_duty |
| C-2 | FR-002 | test_record_field_set_is_closed_six_plus_id |
| C-3 | FR-003 | test_admissibility_is_closed_four |
| C-4 | FR-004 | test_rejection_forms_closed_and_named |
| C-5 | FR-005 | test_load_bearing_threshold_four_triggers |
| C-6 | FR-006 | test_complexity_gating_points_at_rubric |
| C-7 | FR-007 | test_adjacent_owner_boundaries_by_path |
| C-8 | FR-001, FR-007 | test_owner_has_no_second_definition_or_carrier |

## FR 覆盖核对

- FR-001…FR-007 全部由本文件 C-1…C-8 承接；其余 FR 见 `plan-template-anchor.md`、
  `measurement-binding.md`、`analyze-channel.md`、`adr-reference.md`、`validator.md`、
  `falsification-quartet.md`、`mirrors-and-scope.md`。
