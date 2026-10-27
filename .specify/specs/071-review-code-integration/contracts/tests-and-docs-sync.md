# Contracts: Deterministic tests, documentation sync, delivery surface (C-65…C-73)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Owner**: this file owns the test obligations, the documentation-sync surface, the framework-source-only rule, the mirror obligations' acceptance criterion, and the frozen-roster constraint. The mirror table itself is owned by `plan.md` § Mirror Obligations; this file states the criterion and points there.
**Pinned by**: `tests/contract/test_review_docs_isomorphism.py`
**Measures**: SC-006

**C-65**: New behavior lands with deterministic contract coverage of six things, one test group each: (a) the command template's two segments and their fixed order; (b) the three applicability values; (c) the state-machine gate conditions; (d) the receipt's non-zero exit on a gap; (e) the base-resolution rule; (f) documentation/template isomorphism. A group that would stay green when its subject breaks is not coverage (FR-028, SC-006).

**C-66**: Each new test is run before the mechanism it pins exists and is recorded as failing, with the command, the exit code, and the failing count. A green check is a claim, not evidence: a test that cannot go red is reported as a fast-fail finding rather than cited as proof (FR-028, SC-006).

**C-67**: The one changed pin keeps its subject and grows: the `/speckit.review` row assertion in `tests/contract/test_review_p1_review_loop.py` still requires the row to exist and still requires the command to own that transition, stops requiring the duplicated criteria wording, and adds (i) an assertion that the row cites `templates/feature-details-template.md` § Canonical Status State Machine and (ii) a negative assertion that the duplicated wording is gone. The net assertion count rises; nothing is dropped without a replacement assertion naming the same obligation (FR-027, FR-028).

**C-68**: The documentation-sync surface covers three places in the same change: the command reference page `docs/reference/commands/review.md`, the boundary wording of both review skills, and the state-machine owner's gate row. A page that still describes a process-only review is a defect, not a stale nicety (FR-028).

**C-69**: Framework sources are the only edit surface — `templates/`, `skills/`, `shared/`, `scripts/` where a shared asset is touched, `docs/`, `tests/`. Every runtime projection is produced by the existing generators and MUST NOT be hand-edited: the per-tool command copies by the command-copy regenerator, the `.specify/` template/skill/shared copies by the mirror synchronizer (FR-028).

**C-70**: Each edited source lands its projected copies and the acceptance criterion is "no NEW drift" against the baselines measured before this plan: templates 22 files, skills/internal 136 files, shared 55 files, and per-tool command copies matching their templates. An absolute "all green" criterion is unpassable whenever unrelated drift predates the change, so the criterion is stated relative to that measurement. The per-pair table is owned by `plan.md` § Mirror Obligations (FR-028, SC-006).

**C-71**: The command reference page describes the same surface as the template: two segments, two artifacts, two severity vocabularies not mapped to each other, and the three applicability values. The isomorphism test compares the declared surface — the named segments, artifacts, and values — rather than prose, so a cosmetic reword does not red it and a deleted segment does (FR-028, SC-006).

**C-72**: This feature adds no new `/speckit.*` command, no new skill, no new agent, no new package dependency, no network call, no external service, and no resident process (FR-026).

**C-73**: The command and skill rosters stay frozen exactly as the existing suite pins them — the command baseline and the skill baseline measured by `tests/contract/test_migration_distribution.py` do not change, because this feature adds neither a command template nor a skill directory. A roster change would be a scope violation, not an implementation detail (FR-026).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-65 | FR-028 | SC-006 | six new test groups |
| C-66 | FR-028 | SC-006 | test evidence |
| C-67 | FR-027, FR-028 | SC-006 | one pin update |
| C-68 | FR-028 | — | docs page + two skills + owner |
| C-69 | FR-028 | — | generators |
| C-70 | FR-028 | SC-006 | mirror check |
| C-71 | FR-028 | SC-006 | docs ↔ template |
| C-72 | FR-026 | — | dependency/command sweep |
| C-73 | FR-026 | — | roster pins |
