# Specification Quality Checklist: Goal/Team/Agent 与 SDD 开发流程统一

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-10-28
**Feature**: `.specify/specs/074-goal-team-sdd-unification/requirements.md`

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

- Checker evidence (re-run after the clarify write-back): `python3 scripts/python/validate-requirements.py .specify/specs/074-goal-team-sdd-unification/requirements.md` → `status: ok`, all five propositions pass (`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id`), scanned 524 lines, 36 definition rows (28 FR + 8 SC), 11 shared strings, `0 error(s), 0 warning(s)`, exit code 0. Every stamp above derives from this run, not from hand-typing.
- Decomposition gate evidence: `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/074-goal-team-sdd-unification/requirements.md` → `{"decision": "proceed", "measured": {"fr_count": 28, "fr_ceiling": 30, "task_ceiling": 40}, "reasons": []}`, exit code 0. No slicing required.
- Requirements-stage in-session clarifications (sanctioned variant): the three load-bearing design questions were settled before the checklist and are recorded under `## Clarifications` > `### Session 2026-10-28` — authorization surface (Agent capability + Team policy), routing basis (composite deterministic verdict), and nested-run end state (review handoff, outer layer owns merge). No active clarification marker remains.
- Clarify run (Mode A, same-author gate): the coverage scan was delegated to one fresh-context read-only subagent (8 material candidates); five were ratified — new Feature 074, `shared/definitions/sdd-routing-definitions.md` as the routing owner, precedence `adjudicate > sdd > direct`, depth-2 nesting with virtual-mode hosting prohibited, and a `team.md` frontmatter `seats` map resolved by (team, seat). Three bounded corrections landed in the same pass: routing unit = one declared duty reused until inputs change; concurrency cap = per member; handoff carries the integration identity and the team supervisor writes the ledger attribution row. All are recorded under the same session block.
- Feature linkage is resolved: `Related Feature` is Feature 074; the index row (Draft) and `features/074.md` detail land in this run.
- Containment claims were repaired before stamping: FR-026, FR-027, SC-005, and SC-008 now name a baseline referent (the pre-change case set / goal fixture captured at the baseline commit in the verification record), a comparison unit (contract-suite case set; parsed Goal field set), an allowed delta (added cases only; identical field set), and no undefined aggregate such as "unaffected" or "其余".
- Reader baseline: this is a framework-maintenance specification, so "non-technical stakeholder" is the framework maintainer who did not take part in the run. Every framework term is either defined in the spec or reached by owner path; named artifacts are existing owners (`sdd-loop-driver`, `team.md`, agent frontmatter, line registry), not a new technology choice.
- Honest boundary recorded as Assumption A4: the routing engine is deterministic over declared inputs; a knowingly misclassified declaration cannot be detected by the engine and is audited by the review surface. The spec does not claim otherwise.
- Scope interpretation recorded as Assumption A6: only `sdd-loop-driver` is the SDD development flow; `sdd-project-setup` and `sdd-house-keeping` are routed bootstrap/maintenance paths in the same routing surface, not nested development runs.
- The anti-nesting obligation is narrowed once, in its existing owner, to the depth-2 chain in FR-005/FR-006 (including the virtual-mode prohibition); the spec references that owner rather than creating a second governance rule.

<!-- merged from 074a-authorized-routing (source: .specify/specs/074a-authorized-routing/checklists/requirements.md) -->

# Specification Quality Checklist: 授权席位的有界嵌套 SDD 调用与确定性分流（Feature 074 / Slice 074a）

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-10-28
**Feature**: `.specify/specs/074a-authorized-routing/requirements.md`（Feature 074 的切片 074a；父规格 `.specify/specs/074-goal-team-sdd-unification/requirements.md`）

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

- Checker evidence (the authority for every count below): `python3 scripts/python/validate-requirements.py .specify/specs/074a-authorized-routing/requirements.md` → `status: ok`, all five propositions pass (`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id`), scanned 511 lines, 26 definition rows (20 FR + 6 SC), 10 shared strings, `0 error(s), 0 warning(s)`, exit code 0. Every count above derives from this run, not from hand-typing.
- Decomposition gate evidence: `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/074a-authorized-routing/requirements.md` → `{"mode": "plan", "decision": "proceed", "measured": {"fr_count": 20, "task_count": null, "fr_ceiling": 30, "task_ceiling": 40}, "reasons": [], "checked_at": "2026-10-28T16:01:37Z"}`, exit code 0. 20 FR sits inside the 8–30 slice band; no further slicing needed.
- Projection fidelity (programmatic, not by eye): each local FR / SC block was compared against its parent block after the documented STR remap (`[[STR-011]]` → parent `[[STR-011]]`) with whitespace normalized — 20 FR blocks and 6 SC blocks, zero text drift; the three user-story sections, all 13 Edge Cases, all 9 Key Entities and all 11 retained Assumptions are likewise verbatim-in-parent; parent and slice Shared Strings rows match on both the value cell and the `Consumed by` cell for all 10 rows. Only two junctions were adjusted: the local group label above local `FR-025` is `Bootstrap and maintenance classification` (parent `FR 025` sat under the parent's `Diffusion into the Goal/Team/Agent system` label, whose other members are 074b), and the slice-local numbering itself.
- Numbering is slice-local and gapless (FR-001–FR-025, SC-001–SC-007, STR-001–STR-011); no parent number is retained as a definition row, and the three `## Parent Mapping` tables carry the per-item parent id plus a one-line meaning. Parent ids mentioned outside those tables are written as code spans deliberately, so the checker cannot read them as local definitions or dangling references.
- The `## Parent Mapping` STR table writes its ids without code spans on purpose: with backticks the checker would read those rows as a second definition table and report 20 shared strings instead of the true 10.
- Shared Strings: the table keeps only the parent strings this slice cites; every `[[STR-nnn]]` reference in this file resolves to a local row (checker `ref-resolvable` bidirectional check passes with zero warnings, so no row is defined-but-uncited).
- Clarifications record no new requirement adjudication: this slice is the two-slice projection of parent Feature 074 confirmed by the user on 2026-10-28 (`confirmed-user`, `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（tasks U4，2026-10-28）), and the parent's 2026-10-28 clarifications apply to the projected rows unchanged. The session block states both facts and re-opens nothing.
- Scope boundary is explicit both ways: `## Slice Scope` names the in-slice parent items and `## Out of Scope` names the 074b set (parent `US4`, `US5`, `FR-025`–`FR 024`, `FR 026`–`FR 028`, parent `STR-011`, parent `SC-006`, `SC 008`). The slice defines no 074b requirement and implements none.
- Containment-claim treatment: the slice introduces no new containment claim over a machine-produced surface. The parent's ratified containment claims (parent `FR 026`, `FR 027`, parent `SC-006`, `SC 008`) all sit in 074b and are not carried here. Local `SC-004`'s regression clause names its comparison unit as the repository's pre-existing anti-nesting contract-test case set with an empty allowed-delta set; making that baseline explicit at a named commit is 074b's `SC-006` machinery, and no analysis-stage verdict in this slice depends on a hand-written byte list.
- Reader baseline: this is a framework-maintenance specification, so "non-technical stakeholder" is the framework maintainer who did not take part in this run. Every framework term is either defined in the spec or reached by owner path (`sdd-loop-driver`, `team.md`, agent frontmatter, line registry, `shared/definitions/sdd-routing-definitions.md`); no new technology choice is introduced.
- Assumption labels retain the parent letters, so the block reads `A1`–`A7`, `A9`–`A12` with a stated reason: parent `A8` and `A13` describe the outer-layer attribution surface and travel with 074b.
- Route decision for this stage: requirements only. No `/speckit.clarify` or `/speckit.plan` action was taken in this run; the parent design at `.specify/specs/074-goal-team-sdd-unification/` remains the projection source and was not modified.

## Clarify Round (2026-10-29, `/speckit.clarify` Mode A, target = this slice's `requirements.md`)

- Target override was explicit: the branch is the parent feature branch, so `check-prerequisites.sh --json --paths-only` resolves `REQUIREMENTS_DIR` to `074-goal-team-sdd-unification`; the clarification target declared for this run is `.specify/specs/074a-authorized-routing/requirements.md`, and the parent artifact was read only, never edited.
- Three questions were self-adjudicated (unattended run) and recorded in `requirements.md` § `## Clarifications` > `### Session 2026-10-29`; each carries its rationale. All three live on the slice boundary the parent spec never had — the parent design's contract files are organized by theme, not by slice, so the split boundary is not a file boundary: `diffusion-and-compat.md` carries the clauses for 074a-local `FR-025` (parent `FR 025`), `FR-018` and `FR-014` alongside 074b's own items.
- The three answers are integrated as binding clauses `D-1` / `D-2` / `D-3` in the new `requirements.md` § `## Cross-Slice Design Attribution（跨切片交付归属）`, not left as recorded answers only: D-1 fixes attribution by requirement item (not by parent file), D-2 fixes the routing-verdict record surface inside this slice as the Agent execution evidence, D-3 fixes `SC-003`'s in-slice delivery as its content face while the parent `STR 010` heading and section semantics stay with 074b.
- No FR / SC / STR was added, removed, or renumbered, so every count above still holds after the round (re-measured: 492 lines, 26 definition rows = 20 FR + 6 SC, 10 shared strings, `0 error(s), 0 warning(s)`, exit 0); the only superseded literal in this file was the scan line count `475`, refreshed to `492`.
- Append-only invariant held: the `## Clarifications` section grew from 2 rows to 5 rows (2 in `### Session 2026-10-28`, 3 in `### Session 2026-10-29`); no existing row was rewritten.
- Not discharged here, recorded instead: Feature 074's detail file (`Related Specifications/Requirements`) still lists only the parent spec. Registering the 074a slice there is a Feature-integration duty this dispatch's brief explicitly kept out of scope ("do not touch the registry"), so it is handed back rather than silently skipped.

## Close-out Verification (2026-10-28, second dispatch of stage run `r20261028T132000Z-074d`)

- Both gates were re-run in the close-out pass and reproduced their verdicts: `validate-requirements.py` → `status: ok`, all five propositions pass, scanned 475 lines / 26 definition rows (20 FR + 6 SC) / 10 shared strings, `0 error(s), 0 warning(s)`, exit 0; `decomposition-check.py --mode plan` → `proceed` (`fr_count: 20`, ceiling 30, `reasons: []`, exit 0). That line count is a 2026-10-28 snapshot, superseded by the 2026-10-29 clarify round (492 lines, same 26 definition rows and 10 strings — see § Clarify Round); the two verdicts above still hold.
- Every stamp above was re-checked against the artifact rather than re-typed: 3 user stories carrying 11 `Given` scenarios, 13 Edge Cases, 9 Key Entities, 11 labelled assumptions (`A1`–`A7`, `A9`–`A12`), `## Parent Mapping` rows 20 FR + 6 SC + 10 STR, and zero active clarification markers.
- Close-out scope was verification and bookkeeping only: `requirements.md` was not edited in this pass — no FR / SC / STR text, id, numbering, or parent-mapping cell changed — so the state that was validated is exactly the state on disk, and the stage commit stages these two files by explicit path and nothing else.
- Accounting for this stage run: `session/20261028T160359Z-run-determination-speckit-requirements-r20261028t132000z-074.md` and `exec-quant/records/20261028T160403218399Z-7663625e.json` were written by the first dispatch, and both engines answer `duplicate` on re-invocation, so they stand as recorded with `qualification: partial`. The previously missing feedback entry `feedback/20261028T160637Z-speckit-requirements.md` is now written under the same run id with `partial: true`. That `partial` label records a two-dispatch execution (the authoring dispatch hit its turn limit), not a quality verdict: every gate is green and the artifacts are complete.
- No `test-evidence/` directory is produced at this stage: the evidence is the two checker runs quoted above plus this item-by-item pass, and `/speckit.requirements` declares no execution artifact beyond `requirements.md` and this checklist.

## Analyze-fix Round (2026-10-29, remediation of `/speckit.analyze` round 1)

- **Scope of the requirement edits** (each project of a driver-adjudicated analyze finding; no FR / SC / STR was added, removed, or renumbered): `FR-005` now defines **SDD assignment** as a member duty whose routing decision is recorded as `[[STR-004]]` (HIGH-2); `FR-006` and `A9` drop the per-member cap escape in favour of a hard cap of one run per member (B-04); `FR-007` defines **write-bearing change** as any change that writes a tracked file, excluding read-only analysis (C-03); `FR-008` closes the **definition-class** face by making `definition-class` a value of `change_nature` — the five inputs stay five — with membership derived from a target-path predicate, cross-cutting by default (HIGH-1); `FR-010` keys the bounded-correction escape off that value; `FR-012` makes the FR-011 reason code mandatory on an override record (B-03); `SC-001` names its two carriers — the authorization probe record and the team run report — (B-01); `A4` and the dishonest-classification edge case bind the audit duty to `/speckit.review`, with the driver's U4 verification as an independent check inside a nested run (B-02).
- **Re-measured after the round** (the authority for the counts above): `python3 .specify/scripts/python/validate-requirements.py .specify/specs/074a-authorized-routing/requirements.md` → `status: ok`; `id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id` all `pass (0)`; scanned **511 lines**, **26 definition rows** (20 FR + 6 SC), **10 shared strings**; `0 error(s), 0 warning(s)`; exit 0.
- **Superseded literals, stated rather than silently rewritten**: the `492`-line snapshot in § Clarify Round and the `475`-line snapshot in § Close-out Verification are dated measurements of earlier rounds; the current count is the 511 above. The structural stamps they carry (3 user stories / 11 `Given` scenarios / 13 Edge Cases / 9 Key Entities / 11 assumptions / Parent Mapping 20 FR + 6 SC + 10 STR) are unchanged by this round.
- **Not done here**: no `/speckit.plan`, `/speckit.tasks` or `/speckit.checklist` action was taken in this round, and the plan-owned artifacts were edited under the driver's separate authorization, not from this checklist.

<!-- merged from 074b-nested-governance (source: .specify/specs/074b-nested-governance/checklists/requirements.md) -->

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

Method and full output are in the evidence file (§ `[4]`): the parent's `- **FR-NNN**:` / `- **SC-NNN**:` blocks and `### User Story N` blocks were extracted alongside the slice's, Shared-Strings ids were canonicalised on **both** sides to semantic tokens (parent `STR-010` ≡ slice `STR-010`; parent `STR-010` ≡ slice `STR-007`; parent `STR-008` ≡ slice `STR-008`; parent `STR-009` ≡ slice `STR-009`; parent/slice `STR-001`–`STR-003` identical), whitespace was collapsed, and block bodies were compared.

- **Identical after canonicalisation**: 7 of 8 FR blocks (`FR-020`←parent `FR 020`, `FR-022`←`FR 022`, `FR-023`←`FR 023`, `FR-024`←`FR 024`, `FR-026`←`FR 026`, `FR-027`←`FR 027`, `FR-028`←`FR 028`) and 2 of 2 SC blocks (`SC-005`←`SC 005`, `SC-008`←`SC 008`).
- **The complete delta set is 3 blocks, all disclosed here**:
  1. `FR-021` (parent `FR 021`): the parent phrase "lists every invocation's outcome, artifact and evidence paths, …" becomes "lists, per invocation, an outcome of `[[STR-007]]`, `[[STR-008]]`, or `[[STR-009]]`, together with its artifact and evidence paths, its routing-verdict reference, and its anomalies". The obligation is unchanged and strictly no weaker; the addition only names the closed outcome domain so the section's value set is citable and testable, which is what makes the slice's `STR-007`–`STR-009` rows consumed rather than defined-but-unused.
  2. `US1` (parent `US4`) and 3. `US2` (parent `US5`): the **"Why this priority"** sentence gains a clause stating the within-slice ordering (US1 is the consumption surface that US2 depends on). Story text, **Independent Test**, and **all six acceptance scenarios** are verbatim.
- No other text drift: no FR / SC obligation, no scenario, no edge case wording, and no assumption wording differs from the parent beyond the canonical id mapping above.

### Numbering and reference hygiene

- Numbering is slice-local and gapless (`FR-020`–`FR-028`, `SC-005`–`SC-008`, `STR-001`–`STR-010`); no parent number is retained as a definition row, and the three `## Parent Mapping` tables carry the per-item parent id plus a one-line meaning.
- Parent ids anywhere in the file are written in the **space form** (`Parent FR 020`, `父 FR 001`) and 074a's own local ids as `074a 本地 FR 020`; neither form can be read by the deterministic checkers as a local definition or a dangling reference. Hyphenated local ids (`FR-020`) refer only to rows defined in this file.
- The `## Parent Mapping` STR table writes its ids **without** code spans on purpose: with backticks the validator would read those rows as a second Shared Strings definition table and report 14 strings instead of the true 7.
- Shared Strings carries only the parent strings this slice actually cites (parent `STR 001`–`003` and `STR 007`–`010`). The validator's bidirectional `ref-resolvable` check passes with zero warnings, so no row is defined-but-uncited and no citation is dangling.

### Scope boundary, both directions

- `## Slice Scope` names the in-slice parent items (parent `US4`, `US5`; parent `FR 020`–`FR 024`, `FR 026`–`FR 028`; parent `SC 005`, `SC 008`) and the out-of-slice 074a items with the reason (already implemented and merged to `master`, read-only reference).
- `## Out of Scope` names 074a's range explicitly — 控制层级、双层授权、深度 2 嵌套谓词（父 `FR 001`–`FR 006`）、三值分流裁决（父 `FR 007`–`FR 014`）、nested invocation 入口与 handoff 核心（父 `FR 015`–`FR 019`）、引导/维护路径分流面（父 `FR 025` = `074a` 本地 FR 020） — with the 074a implemented surfaces it may be read from by path. The slice defines no 074a requirement, implements none, and rewrites none.
- Two-slice arithmetic is consistent with the confirmed split record: 8 (this slice) + 20 (074a) = parent 28, with mutually exclusive FR sets.

### Containment-claim treatment

`FR-026`, `FR-027` and `SC-005` carry containment claims and were inherited verbatim from the parent, where they were already made decidable (parent contract C-62 owns the mechanical procedure): the baseline referent is the case set captured at the pre-change commit named in the verification record; the comparison unit is each named suite's **collected test-node-id set**, not a file list or a count; the allowed-delta source is mechanical (post ⊇ pre); and the complement assertion is "every pre-change case returns the same verdict / passes", so a renamed case cannot net out against an added one. No hand-written byte-site list and no undefined aggregate ("unaffected leaves") carries acceptance semantics.

`SC-008` names its baseline as the goal fixture captured before the scripted nested run, its comparison unit as the parsed Goal field set, and its allowed delta as empty; the prohibition side ("attribution resolves only through the existing ledger reference") is asserted by the same contract test. Nothing in this slice voids either claim.

**One inherited forward reference, stated rather than hidden**: the baseline *commit* in `FR-026` / `FR-027` / `SC-005` is named by the verification record, which does not exist at requirements time. That is the parent's own wording and its own decision (C-62), and it stays decidable at verification time because the procedure — freeze the collected node-id set before any edit, then assert containment — is fixed here; naming a commit now would pre-empt the plan stage's baseline choice. No analysis verdict in this slice depends on it.

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
