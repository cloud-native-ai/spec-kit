# Specification Quality Checklist: 外层消费、概念扩散与兼容安全（Feature 074 / Slice 074b）

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-10-29
**Feature**: `.specify/specs/074b-nested-governance/requirements.md`（Feature 074 的切片 074b；父规格 `.specify/specs/074-goal-team-sdd-unification/requirements.md`）

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Stability / containment claims name a baseline referent and a derivable allowed-delta set (owner: `.specify/shared/guidelines/closed-set-claims.md`)
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

### Checker evidence (the authority for every count in this file)

Every count below derives from a checker run captured at execution time, never hand-typed. Full capture (command lines, exit statuses, complete output): `.specify/specs/074b-nested-governance/test-evidence/requirements-checks.txt`.

- `python3 scripts/python/validate-requirements.py .specify/specs/074b-nested-governance/requirements.md` → `status: ok`; all five propositions pass (`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id`, each `pass (0)`); scanned **308 lines**, **10 definition rows** (8 FR + 2 SC), **7 shared strings**; `0 error(s), 0 warning(s)`; exit 0.
- Decomposition gate: `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/074b-nested-governance/requirements.md` → `{"mode": "plan", "decision": "proceed", "measured": {"fr_count": 8, "task_count": null, "fr_ceiling": 30, "task_ceiling": 40}, "reasons": []}`, exit 0. 8 FR sits inside the 8–30 slice band.
- Cross-artifact gate before analyze: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/074b-nested-governance --stage requirements --repo .` → `decision=pass errors=0 advisories=0 waived=0` (`fr: 8`, `sc: 2`, `files: 1`). An earlier run of this same gate reported 5 `dangling-id` errors on the 074a cross-slice ids written as `FR 020` / `FR 018` / `FR 014`; they were rewritten in place to the `074a 本地 FR 020` form (the space form the projection convention already uses for parent ids) and the gate was re-run to `pass`. The re-run, not the first run, is the stamp above.

### Projection fidelity (programmatic, not by eye)

Method and full output are in the evidence file (§ `[4]`): the parent's `- **FR-NNN**:` / `- **SC-NNN**:` blocks and `### User Story N` blocks were extracted alongside the slice's, Shared-Strings ids were canonicalised on **both** sides to semantic tokens (parent `STR-010` ≡ slice `STR-007`; parent `STR-007` ≡ slice `STR-004`; parent `STR-008` ≡ slice `STR-005`; parent `STR-009` ≡ slice `STR-006`; parent/slice `STR-001`–`STR-003` identical), whitespace was collapsed, and block bodies were compared.

- **Identical after canonicalisation**: 7 of 8 FR blocks (`FR-001`←parent `FR 020`, `FR-003`←`FR 022`, `FR-004`←`FR 023`, `FR-005`←`FR 024`, `FR-006`←`FR 026`, `FR-007`←`FR 027`, `FR-008`←`FR 028`) and 2 of 2 SC blocks (`SC-001`←`SC 005`, `SC-002`←`SC 008`).
- **The complete delta set is 3 blocks, all disclosed here**:
  1. `FR-002` (parent `FR 021`): the parent phrase "lists every invocation's outcome, artifact and evidence paths, …" becomes "lists, per invocation, an outcome of `[[STR-004]]`, `[[STR-005]]`, or `[[STR-006]]`, together with its artifact and evidence paths, its routing-verdict reference, and its anomalies". The obligation is unchanged and strictly no weaker; the addition only names the closed outcome domain so the section's value set is citable and testable, which is what makes the slice's `STR-004`–`STR-006` rows consumed rather than defined-but-unused.
  2. `US1` (parent `US4`) and 3. `US2` (parent `US5`): the **"Why this priority"** sentence gains a clause stating the within-slice ordering (US1 is the consumption surface that US2 depends on). Story text, **Independent Test**, and **all six acceptance scenarios** are verbatim.
- No other text drift: no FR / SC obligation, no scenario, no edge case wording, and no assumption wording differs from the parent beyond the canonical id mapping above.

### Numbering and reference hygiene

- Numbering is slice-local and gapless (`FR-001`–`FR-008`, `SC-001`–`SC-002`, `STR-001`–`STR-007`); no parent number is retained as a definition row, and the three `## Parent Mapping` tables carry the per-item parent id plus a one-line meaning.
- Parent ids anywhere in the file are written in the **space form** (`Parent FR 020`, `父 FR 001`) and 074a's own local ids as `074a 本地 FR 020`; neither form can be read by the deterministic checkers as a local definition or a dangling reference. Hyphenated local ids (`FR-001`) refer only to rows defined in this file.
- The `## Parent Mapping` STR table writes its ids **without** code spans on purpose: with backticks the validator would read those rows as a second Shared Strings definition table and report 14 strings instead of the true 7.
- Shared Strings carries only the parent strings this slice actually cites (parent `STR 001`–`003` and `STR 007`–`010`). The validator's bidirectional `ref-resolvable` check passes with zero warnings, so no row is defined-but-uncited and no citation is dangling.

### Scope boundary, both directions

- `## Slice Scope` names the in-slice parent items (parent `US4`, `US5`; parent `FR 020`–`FR 024`, `FR 026`–`FR 028`; parent `SC 005`, `SC 008`) and the out-of-slice 074a items with the reason (already implemented and merged to `master`, read-only reference).
- `## Out of Scope` names 074a's range explicitly — 控制层级、双层授权、深度 2 嵌套谓词（父 `FR 001`–`FR 006`）、三值分流裁决（父 `FR 007`–`FR 014`）、nested invocation 入口与 handoff 核心（父 `FR 015`–`FR 019`）、引导/维护路径分流面（父 `FR 025` = `074a` 本地 FR 020） — with the 074a implemented surfaces it may be read from by path. The slice defines no 074a requirement, implements none, and rewrites none.
- Two-slice arithmetic is consistent with the confirmed split record: 8 (this slice) + 20 (074a) = parent 28, with mutually exclusive FR sets.

### Containment-claim treatment

`FR-006`, `FR-007` and `SC-001` carry containment claims and were inherited verbatim from the parent, where they were already made decidable (parent contract C-62 owns the mechanical procedure): the baseline referent is the case set captured at the pre-change commit named in the verification record; the comparison unit is each named suite's **collected test-node-id set**, not a file list or a count; the allowed-delta source is mechanical (post ⊇ pre); and the complement assertion is "every pre-change case returns the same verdict / passes", so a renamed case cannot net out against an added one. No hand-written byte-site list and no undefined aggregate ("unaffected leaves") carries acceptance semantics.

`SC-002` names its baseline as the goal fixture captured before the scripted nested run, its comparison unit as the parsed Goal field set, and its allowed delta as empty; the prohibition side ("attribution resolves only through the existing ledger reference") is asserted by the same contract test. Nothing in this slice voids either claim.

**One inherited forward reference, stated rather than hidden**: the baseline *commit* in `FR-006` / `FR-007` / `SC-001` is named by the verification record, which does not exist at requirements time. That is the parent's own wording and its own decision (C-62), and it stays decidable at verification time because the procedure — freeze the collected node-id set before any edit, then assert containment — is fixed here; naming a commit now would pre-empt the plan stage's baseline choice. No analysis verdict in this slice depends on it.

### Reader baseline

This is a framework-governance specification, so "non-technical stakeholder" is the framework maintainer who did not take part in this run. Every framework term is either defined in the spec or reached by owner path (`team.md` / team run-report contract, `sdd-loop-driver`, goal and ledger model, `shared/definitions/sdd-routing-definitions.md`, neutral metadata key set). The required output—a report section, an attribution boundary, a disambiguation paragraph, and two containment obligations—introduces no new technology choice.

### Assumptions and story coverage

- Assumption labels retain the parent letters, so the block reads `A1`, `A5`, `A8`, `A10`, `A13` with a stated reason: the other parent assumptions describe the authorization, routing and nesting-predicate faces delivered by `074a` and are not restated here.
- Two user stories (parent `US4` → local `US1`, parent `US5` → local `US2`) each carry an Independent Test and three `Given` scenarios — 6 scenarios total, verbatim from the parent.
- 5 edge cases: 3 verbatim parent cases that land on the outer layer (unresolved review findings, missing integration identity, stall/timeout/budget exhaustion) plus 2 slice-boundary stitches (no-invocation section must be explicit; an unlocatable verdict reference must be recorded as missing rather than re-derived).

### Recorded deviation for downstream stages

The `**Requirement Branch**` field records the live branch `074b-nested-governance`, and `**Parent Feature Branch**` records `074-goal-team-sdd-unification`. The slice branch does not match the `^[0-9]+-<slug>` shape the scaffold script recognises, so `check-prerequisites.sh` cannot derive `REQUIREMENT_ID` from it and would resolve `REQUIREMENTS_DIR` to the parent spec. Downstream stages MUST target `.specify/specs/074b-nested-governance/` explicitly; the parent spec is read-only for this slice. This is a consequence of the confirmed two-slice split, not a defect introduced here.

### Route decision for this stage

Requirements only. No `/speckit.clarify`, `/speckit.plan` or `/speckit.checklist` action was taken in this run; the parent design under `.specify/specs/074-goal-team-sdd-unification/` was read as the projection source and was not modified. Every clarification this slice needed was settled in-session and recorded under `## Clarifications` > `### Session 2026-10-29` before this checklist was stamped (the sanctioned in-session variant), so the first-pass all-green result above is a legitimate outcome rather than a skipped validation step.
