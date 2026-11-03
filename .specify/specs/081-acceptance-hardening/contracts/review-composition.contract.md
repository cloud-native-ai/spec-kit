# Contract — Review Composition (four segments + one deterministic check)

**Status**: designed (this stage); implemented by `/speckit.implement`
**Owner of the composition, the order and the boundaries**: `templates/commands/review.md` § Composition (the owner text this feature rewrites). **Owner of the two new segments' method**: `skills/internal/review-feature-quality/SKILL.md`. **Owner of the `P0`/`P1`/`P2` family**: `skills/internal/review-sdd-process/SKILL.md`. **Owner of the six-level code family**: `skills/internal/code-review/SKILL.md`. This contract states the obligations; it restates no severity definition.

## Composition and order

- **RC-01**: `/speckit.review` MUST run four segments in one fixed order — process (`review-sdd-process`) → artifact (new) → implementation (new) → code (`code-review`) — followed by one deterministic check (Acceptance Reality Check) that is not a segment.
- **RC-02**: The order MUST be a property of the command template; `$ARGUMENTS` MUST NOT select, reorder or skip any segment, and no execution/expression class exempts the process segment.
- **RC-03**: The composition sentence MUST be rewritten in place — the pre-change wording ("exactly two segments") MUST NOT survive anywhere, and `code-review` MUST remain present (its replacement is forbidden).
- **RC-04**: The four segment conclusions MUST NOT be merged, converted, mapped or scored together; no mapping table between the `P0`/`P1`/`P2` family and the six-level family may exist, and the run MUST store no combined value.

## Segment contracts

- **RC-05**: Each segment MUST be described by the same five fields: `Skill` (runtime path), `Judgment object`, `Severity vocabulary` (family + owner), `Inputs`, `Outputs`.
- **RC-06**: The artifact segment's judgment object MUST be every stage artifact the slice's **stage rules and `plan.md` § Project Structure require** — `requirements.md`, `plan.md`, `tasks.md`, `contracts/`, `data-model.md`, `quickstart.md`, `verification.md` — judged for completeness, internal consistency, traceability (FR → task → SC → evidence), dependency/premise ownership and acceptance honesty; every finding MUST carry a severity and a `path` (+ `line` where the finding is line-anchored). The coverage denominator is the **expected** set, never "the ones that exist this time": a required artifact that is missing MUST produce a finding and MUST count as uncovered, otherwise a missing artifact would render as 100% coverage (`requirements.md` FR-013 owns the obligation; the derivation rule from stage rules lives in the owner doc § Review Composition).
- **RC-07**: The implementation segment's judgment object MUST be this slice's implementation, `base..head`, judged against `requirements.md` and `tasks.md` for correctness, scope and regression, and it MUST run or verify the smoke test and record command, exit code and evidence path.
- **RC-08**: The artifact and implementation segments MUST NOT substitute for each other, and neither MUST be answered by the code segment; `review-sdd-process` MUST NOT be treated as a substitute for either.
- **RC-09**: `base..head` resolution MUST reuse `skills/internal/code-review/scripts/git-delta-review.sh` (its ordered resolution tiers and its closed trunk order); the new segment MUST NOT implement a second base resolution.

## Carrier (A12)

- **RC-10**: The two new segments' methodology MUST live in one runtime-reachable named owner — the internal skill `review-feature-quality`, runtime path `.specify/skills/internal/review-feature-quality/SKILL.md` — with two explicitly named sub-sections (`Segment A — Artifact Review`, `Segment B — Implementation Review`).
- **RC-11**: `templates/commands/review.md` MUST reference that owner by path and section anchor and MUST NOT inline its dimension lists, its severity definitions or its field lists.
- **RC-12**: The process skill's judgment object MUST remain single and unchanged after the carrier lands; a second judgment object appearing in its body is a defect.

## Acceptance Reality Check (ARC)

- **RC-13**: ARC MUST read the closure checker's `final_path` counts and MUST NOT re-count them from `verification.md`.
- **RC-14**: ARC MUST write the three counts (`final_pass`, `final_blocked`, `final_deferred`) into `review.md`, in the carrier slot `### 2.4`, and MUST compare them against the feature's claimed status.
- **RC-15**: When the claimed status is `Implemented` or `Ready for Review` and `final_pass` is zero, ARC MUST emit the fixed item `F-ACCEPTANCE` at `P0` and the transition `Implemented → Ready for Review` MUST be refused; the refusal MUST name the failed condition and leave the status at `Implemented`.
- **RC-16**: ARC MUST NOT be delegated to a model judgement and MUST NOT be described as a fifth segment.

## Report slots and the unit census

- **RC-17**: `templates/review-template.md` MUST gain stable slots `### 2.2 Artifact Review Segment`, `### 2.3 Implementation Review Segment`, `### 2.4 Acceptance Reality Check` after the existing `### 2.1`; subsection numbers are stable slots, not execution order, and `### 2.1` MUST NOT be renumbered.
- **RC-18**: The feedback unit census of one composed run MUST become four units — `/speckit.review`, `skill:review-sdd-process`, `skill:review-feature-quality`, `skill:code-review` — sharing one `run_id`, each completing its own closing record; the command MUST NOT suppress any skill's wrap-up.
- **RC-19**: The existing guard that pins the census (currently "three units") MUST be updated deliberately in the same change, and the commit message MUST state why (a new runtime-reachable segment carrier forces a fourth unit).

## Traceability

| FR | Clauses | Test |
|---|---|---|
| FR-013 | RC-01…RC-06, RC-10, RC-11, RC-17 | `tests/contract/test_acceptance_review_composition.py` (+ updated `test_review_code_composition.py`) |
| FR-014 | RC-07, RC-08, RC-09 | `tests/contract/test_acceptance_review_composition.py` |
| FR-015 | RC-13…RC-16 | `tests/contract/test_acceptance_review_composition.py` (negative fixture: `F-ACCEPTANCE` + refusal) |
| FR-016 | RC-15 | `tests/contract/test_acceptance_state_machine.py` |
| FR-018 (census) | RC-18, RC-19 | `tests/contract/test_review_feedback_boundary.py` (deliberate update) |
| SC-006 | RC-05…RC-07, RC-14, RC-17 | the same two files |
