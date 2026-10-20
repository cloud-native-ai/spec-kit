# Contracts: Cross-cutting Constraints（FR-026..FR-029）

**Spec**: `.specify/specs/063-review-p1-governance/requirements.md`
**Convention**: canonical clause form (`**C-N**` md-bold-closed) per `shared/definitions/contract-clause-definitions.md` § 3. Each clause's citation group is the trailing `(FR-…, SC-…)` at the end of its block (§ 4 rule 2); FR ids in a label or mid-body are mentions, not citations.

These clauses carry the feature-wide obligations no single mechanism contract owns. They bind every change this feature lands, including the changes contracted in `template-mechanisms.md`, `engine-face-contract.md`, and `evidence-baseline-contract.md`.

## Feature-wide obligations

**C-31**: 两顶帽子同步义务 — every mechanism edit in this feature MUST land framework-source side (`shared/`, `templates/`, `skills/`, `scripts/`, `tests/`, `docs/`), and each `.specify/` runtime projection MUST be produced by the existing generator flow in the same change (`sync-mirrors.py` mirror pairs, `regen-command-copies.py` per-tool command copies, `generate-instructions.sh` instructions, `probe-utils.py --action compile-embeds` compiled wrap-up faces); a hand-edited runtime copy MUST NOT be the primary delivery. The pre-change drift baselines fixed in `plan.md` § Mirror Obligations (202 sync-mirrors DIFF entries; clean regen copies; 74-unit zero compile drift) set the acceptance criterion as no-NEW drift, and a mirror pair this feature touches MUST clear its own pre-existing entry via the mandated sync (FR-026, SC-013, SC-014)。

**C-32**: 逐机制确定性测试与变异演练 — every mechanism clause in this feature's contract set MUST land with a deterministic contract test pinning it, and every clause guarding a negative proposition ("X MUST NOT happen") MUST additionally carry a mutation drill proving the guard turns red when its object is broken. Test outcomes MUST be compared against the frozen name-level baseline at `.specify/specs/063-review-p1-governance/notes/baseline-failed-tests.txt` by sorted-name `comm -13`, and the gate is zero NEW failures — existing failures are never counted as regressions, and the baseline MUST be frozen before any change (FR-027, SC-013)。

**C-33**: 零新增依赖与常驻 — no mechanism in this feature MAY introduce an external service, a network call, a model API call, a third-party dependency, or a background daemon; the S10 verification's dependency-manifest diff and network-call sweep measure each count as zero (FR-028, SC-013)。

**C-34**: 062 制品只读 — the files under `.specify/specs/062-humanize-command/` (`requirements.md`, `plan.md`, `tasks.md`, `review.md`, and the notes instances) are evidence for this feature and MUST NOT be edited to clear a finding; any 062 notes-instance repair is separate work outside this feature. `git diff` over that directory within this feature's commit window MUST be empty (FR-029, SC-014)。

## Traceability

| Clause | FR | SC | Scope |
|--------|----|----|-------|
| C-31 | FR-026 | SC-013, SC-014 | all framework-source edits + their projections |
| C-32 | FR-027 | SC-013 | per-mechanism test pins + mutation drills |
| C-33 | FR-028 | SC-013 | dependency/network/daemon surface |
| C-34 | FR-029 | SC-014 | 062 artifact immutability |
