# Specification Quality Checklist: Goal 作为项目级一等概念

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-08-04
**Feature**: [requirements.md](../requirements.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain — *0 markers; the one retained at draft time was resolved 2026-08-05, see Validation Log*
- [x] Requirements are testable and unambiguous
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

## Validation Log

**Iteration 1 — 3 issues found and fixed:**

| # | Item | Issue | Fix |
|---|------|-------|-----|
| 1 | All functional requirements have clear acceptance criteria | FR-019 was a bare `[NEEDS CLARIFICATION]` marker occupying an FR slot, so it stated no requirement at all and nothing could satisfy it. | Rewritten as a real requirement — the integration MUST be built against a documentation-verified contract and MUST NOT be built on a guessed format — with the marker attached as its open question. |
| 2 | Requirements are testable and unambiguous | The relationship to requirement 036's freshly-landed `.specify/project/goal/<goal-slug>/` was implicit, leaving "which goal directory?" ambiguous for every downstream reader. | Added FR-024 (documents MUST distinguish the two), an Edge Case, and a dedicated 命名辨析 paragraph in Assumptions naming both paths and their opposite semantics (authored input vs derived output). |
| 3 | Dependencies and assumptions identified | The spec named new identifiers without checking collisions, contrary to the reserved-identifier rule. | Grepped first: `--goal` is **already claimed by two scripts with different meanings** (`build-summary-input.py` = goal identity to aggregate; `match-team-preset.py` = goal text), and `goal_slug` is 036's established identity key. Recorded as FR-003 (reuse `goal_slug`, no second identifier) + FR-025 (avoid the `--goal` collision) + an Assumption proposing `--goal-id`. |

**Iteration 2 — all items pass.** Mechanical re-validation: 25 FRs with contiguous IDs FR-001…FR-025 and no duplicates, 10 SCs each paired with a measurement source, 5 user stories, 1 clarification marker (within the max of 3), both `[[STR-nnn]]` strings defined and referenced (12 and 11 times), zero template placeholders remaining.

**Post-draft revision (2026-08-04, single-goal-directory decision)** — the user resolved the path-naming question with a fourth option not among the three offered: **`.specify/goal/` absorbs `.specify/project/goal/`, and `.specify/project/` no longer holds goal content.** Recorded verbatim under `## Clarifications`.

This surfaced a **direct contradiction in the draft** that had to be fixed rather than layered over: FR-015 said the requirement "MUST NOT change 036's aggregation semantics, identity grammar **or delivery directory layout**" — but the decision relocates exactly that directory. FR-015 was rewritten to preserve aggregation semantics and identity grammar while explicitly relocating the delivery directory per the new FR-026.

Added: FR-024 rewritten (single goal index), FR-026 (migrate 036's delivery directory; zero residual references), FR-027 (authored definition and derived summary structurally separable inside one goal directory, so 036's write-set discipline still holds), FR-028 (migration must not weaken any existing 036 assertion), SC-009 rewritten (one goal index), SC-011 + source (migration completeness). Replaced the now-obsolete "two confusable paths" edge case with two new ones (definition/summary co-location, transitional dual-path). Rewrote the Assumptions naming paragraph as the decision with its measured cost.

**Migration cost measured before committing to it**: `grep -rl 'project/goal'` returns **37 files**, including 5 per-tool command copies, the canonical skill plus its mirror, the generator script plus its mirror, the Tool record, `docs/reference/commands/team.md`, feature memory, and 036's own spec artifacts and 10 test files. Recorded as the SC-011 baseline so the rework is planned rather than discovered.

**Re-validation after the revision**: 28 FRs contiguous FR-001…FR-028 with no duplicates, 11 SCs each paired with a source, 5 user stories, still exactly 1 clarification marker, `[[STR-001]]` referenced 15 times and `[[STR-002]]` 11 times, and a contradiction sweep for residual "must not change the delivery directory" claims returns only FR-015's corrected form (where the `MUST NOT` now scopes to aggregation *behaviour*, not the path). All 16 checklist items still pass.

**Clarify session (2026-08-05, Mode A) — 4 decisions, both open items closed:**

| # | Question | Decision | Spec impact |
|---|----------|----------|-------------|
| 1 | `Related Feature` binding | **New Feature 041 "Goal Registry"** (not 027) | Related Feature resolved with rationale; Feature 041 registered in `features.md` + `features/041.md`; reverse cross-reference added to `features/027.md` |
| 2 | Authoring entry for goal definitions | **New `/speckit.goal` command** | Added FR-026 (single entry) + FR-027 (delivered via the mirror model) + SC-012 & source; new-command-surface cost recorded in Assumptions for the plan's Principle IX check |
| 3 | Host-CLI integration shape | **Out of scope for this requirement** | Removed the host-CLI user story and FR-017/018/019; added `## Out of Scope`; the last `[NEEDS CLARIFICATION]` marker resolved |
| 4 | Definition vs summary layout inside the goal directory | **`goal.md` + `summary/` subtree** | FR-023/FR-024 made concrete; STR-003/STR-004 added; SC-008 and its source narrowed from the archive root to the definition file; two Edge Cases restated |

**The marker was closed by verification, not by judgement.** `docs/reference/cli/` documents no `/goal`, so the contract was fetched from the host CLI's official documentation (`https://docs.qoder.com/cli/goal.md`): the surface is `/goal set <description> [--turns <n>]` plus `status` / `pause` / `resume` / `take` / `clear`, and **`set` accepts inline text only — there is no file-path or identity option**. The user's original phrasing ("specify it via the goal description file") therefore cannot be honored on the CLI side at all; the user chose to defer the whole integration rather than ship a Spec-Kit-side text-rendering substitute inside this requirement. This is the honest outcome: the draft's FR-017 had asserted a capability the host CLI does not have.

**Renumbering was required, not cosmetic**: removing three FRs would have left a gap, so old FR-020…FR-028 shifted down to FR-017…FR-025 and two new FRs were appended. The 2026-08-04 Clarifications entry was left byte-identical (append-only invariant) and a numbering map was added to the new session entry so its stale numbers stay readable.

**Mechanical re-validation after the clarify session**: 27 FRs contiguous FR-001…FR-027 with no duplicates; 12 SCs each paired 1:1 with a measurement source; 4 contiguous user stories; **0** live `[NEEDS CLARIFICATION:` markers; all 4 `[[STR-nnn]]` citations resolve to table rows with no unused rows; Clarifications `- Q:` rows increased 1 → 5 (append-only invariant held); residual sweep for the dropped host-CLI design (`宿主 code CLI`, `引用关系而非同步关系`, `User Story 5`, `FR-028`) returns hits **only** inside the historical Clarifications entry and the numbering map, which is the intended handling. The Shared Strings consumed-by lists were recomputed programmatically rather than by recall, which exposed three pre-existing inaccuracies in the STR-001 row (it named FR-007, FR-026/027/028, SC-008 and SC-011 as consumers when none of them cite the string).

**Clarify session #2 (2026-08-05, Mode A) — conformance against the concept source of truth.** The user supplied `shared/definitions/goal-definitions.md` (authored 2026-08-04, still uncommitted; identical canonical + `.specify/` mirror) and asked whether the spec's understanding of each concept was correct. Checking all **17** concept points it fixes: **8 already aligned** (authored-not-derived, identity reuses `goal_slug`, archive location, N teams : 1 goal one-way reference, team stores identity only, one team ↔ one goal, legacy inline fallback with definition authoritative, terminal goals retained), **3 conflicts**, **6 gaps**.

| Kind | Finding | Resolution |
|---|---|---|
| Conflict | Lifecycle: definitions fix **3** states (`active`/`achieved`/`abandoned`); spec had **4** (extra `superseded`), with FR-013 and an Edge Case depending on it | User chose to **drop `superseded` and its detection**: FR-006 narrowed, FR-013 deleted, Edge Case removed, SC-005 + source narrowed to broken references, US1 narrative / scenario 4 / Key Entities synced |
| Conflict | Composition: definitions say **exactly three parts**; FR-002 said "at least" five items (identity, narrative, criteria, state, timestamps) | FR-002 restated as the three parts, with identity carried by the directory name and timestamps demoted to change-history metadata |
| Conflict | Assumptions called goal and requirement "**不同层次**" (different layers — implies a hierarchy) while the definitions explicitly state parallel planes with **no necessary hierarchy** | Rewritten as "different planes, no necessary hierarchy"; the Overview gained the same boundary |
| Gap ×5 | Outcome-not-tasklist; per-Goal singularity (no composite goal); unrestricted object; disjoint criteria authority; no structural link | Closed **without asking** as FR-027, FR-028, FR-029, FR-031, FR-032 — the definitions leave no optional space on these |
| Gap ×1 | Measured **by degree** (progress / threshold / evaluator score, not per-clause pass/fail) — absent entirely | Asked, because how much this requirement owns was a scope decision. User chose "state the property, defer the representation" → FR-030 |
| Ambiguity | FR-019 (then FR-020) said team-domain guidance must point at "the new single source of truth" — but there are now **two**, at different levels | User chose **read-only input**: `goal-definitions.md` is the *concept* SSoT, `<goal-slug>/goal.md` the *instance* SSoT. FR-019 split accordingly; STR-005 added; new Assumption fixes the direction of conformance (change the spec, never bend the definition) |

**Compatibility explicitly checked, not assumed**: the definitions' storage tree shows only the Goal definition under `<goal-slug>/`, which could read as excluding 036's derived summary from the same directory. It does not — the same section states that "the file layout inside `<goal-slug>/` is owned by the feature that implements Goal management", which is this Feature. The `goal.md` + `summary/` split is therefore delegated, not tolerated; recorded as an Assumption so a later reader does not re-litigate it.

**Second renumbering**: deleting FR-013 shifted old FR-014…FR-027 down to FR-013…FR-026, and FR-027…FR-032 were appended. Both prior Clarifications entries were left byte-identical and a second `旧→新` map was appended — the same discipline as session #1.

**A count I got wrong, caught by scripting rather than re-reading**: my first draft of this entry claimed "13 concept points, 2 conflicts + 4 gaps", and the SC-013 baseline repeated it. Recounting programmatically against the definitions gave **17 / 3 / 6** — the composition conflict was uncounted, and the criteria-authority and no-structural-link gaps were listed in the prose while excluded from the total. Both statements were corrected and SC-013 was widened from six conformance dimensions to **eight** (adding narrative shape and verification mode), since the original six did not cover FR-027, FR-030 or FR-032. This is the same class of drift as the group-count error in 036 — self-reported counts in prose need a script behind them.

**Mechanical re-validation**: 32 FRs contiguous FR-001…FR-032, no duplicates; 14 SCs paired 1:1 with sources; 4 contiguous user stories; **0** live markers; all 5 `[[STR-nnn]]` resolving with no unused rows; Clarifications `- Q:` rows 5 → 8 across 3 session blocks (append-only held); zero residual `superseded`/`被取代` lifecycle references outside the historical entries and numbering maps; every one of the six new FRs present. Feature 041's index row and detail file were corrected too — both still described the four-state lifecycle. All 16 checklist items still pass.

**Clarify session #3 (2026-08-05, Mode A) — multi-team coordination added.** The user directed that the goal level record which teams are advancing it, plus a coordination mechanism that re-delimits overlapping team scopes so teams collaborate rather than compete. This is a **capability addition**, so it was integrated first (per the command's "integrate user-provided decisions before generating the queue" rule) and the queue covered only the residual design forks.

**Investigated before designing, which changed the design.** `skills/create-team/SKILL.md` already solves exactly this problem one level down: **Territory Division** assigns Write Scope / Read Scope / Forbidden per member under a *zero write overlap* invariant, with a Forbidden Write List for shared files and optional `isolation: worktree` for physical separation. But it exists only at **member level in the parallel pattern** — serial / iteration / continuous have no territory, and there is **no team-level scope field at all**. So the right move was to lift the existing vocabulary and invariant one level rather than invent a "coverage area" concept, and a new team-level field is unavoidable (a union of member territories would cover only one of the four patterns).

| # | Question | Decision | Rejected |
|---|----------|----------|----------|
| 1 | How is a team's coverage expressed so overlap is detectable? | **Team-level `territory`** — path-shaped entries (normalize then intersect) plus typed non-path entries, all four patterns → FR-035 | Derive from member territories (three patterns have none); claim goal criteria instead (misses write conflicts); free text + agent judgement (abandons territory's determinism) |
| 2 | How far does the coordination round's authority go? | **Detect + propose only; human ratifies** → FR-039, SC-017 | Agents negotiate and rewrite scopes automatically; report overlap only (then no coordination actually happens) |
| 3 | Where do the roster and the agreed division live? | **Roster derived into `summary/`; division written back into each `team.md`** → FR-033, FR-040 | A new authored `coordination.md` in the goal dir (would turn last session's two-way split into three); roster as a `goal.md` field (would make the binding two-way and force a derived flow to write the definition — straight into FR-007) |
| 4 | When does overlap detection run? | **Rides 036's existing goal summary refresh** → FR-041 | On binding/scope change (needs a new hook); before every cycle (blocks every run); explicit invocation only (overlap could go unnoticed indefinitely) |

**Compatibility with the read-only concept authority re-checked, not assumed.** `goal-definitions.md` fixes the binding as "one-way identity, the team side stores the identity only". A **derived** roster does not violate that — nothing is stored on the goal side as authority and no `goal→team` field appears; the ratified division lands in `team.md`, keeping the team the sole declaring party. The authority's own singularity rule already says the project may hold multiple active goals "each advanced by its own **team(s)**", so N-teams-per-goal was already sanctioned — it simply never addressed coordination. Coordination is therefore an **addition to the team domain**, not a change to the Goal concept, and last session's read-only-input ruling still holds untouched.

**No renumbering this round** — everything was appended (US5 after US4; FR and SC continued), so no third mapping table exists. US5 is P2 while the preceding US4 is P3; document order is deliberately not priority order here, annotated in place, to avoid a third renumbering of the kind flagged as a recurring cost.

**Mechanical re-validation**: 42 FRs contiguous FR-001…FR-042, no duplicates; 18 SCs paired 1:1 with sources; 5 contiguous user stories; **0** live markers; all 5 `[[STR-nnn]]` resolving with no unused rows; Clarifications `- Q:` rows 8 → 12 across 4 session blocks (append-only held); zero dangling FR/SC cross-references; and the four new-group cross-references (FR-033→FR-007, FR-034→FR-015, FR-035→FR-029, FR-040→FR-023) each verified against the *referenced text* rather than by existence alone — the check that caught two semantically wrong references last session.

**Size flag for `/speckit.plan`**: the spec is now 42 FR / 18 SC / 5 stories across seven FR groups (348 lines), above requirement 036's 36 FR. Nothing is redundant, but the coordination group (FR-033…FR-042) is a self-contained capability depending only on US1/US2 — the plan should consider whether it warrants its own phase, or even its own requirement slice, rather than being decomposed inline with the definition archive.

**Plan phase (2026-08-05) — two measurement defects corrected in the spec.** `/speckit.plan`'s exploration pass found that two figures could not survive contact with the repository, so `requirements.md` was amended before the plan was filled (fact correction, no user ruling needed):

| Defect | Reality | Fix |
|---|---|---|
| FR-022 / SC-011 / Assumptions cited "37 files" for the migration surface | 51 text files contain `project/goal`: **24 live source** (4 canonical + 4 mirrors + 5 generated per-tool copies + 9 tests + 1 user doc + 1 Tool record), **18 historical**, 9 `.pyc` build artifacts | Figures replaced with the verified breakdown |
| SC-011 demanded whole-repo residual references of 0 | **Unachievable by construction** — the 2026-08-04 Clarifications entry quotes `.specify/project/goal/` verbatim as the user's directive, and 036's spec archive plus append-only feedback records legitimately contain it. Rewriting them would falsify the record | FR-022 and SC-011 rescoped **by face**: live residual MUST be 0, historical rewrites MUST be 0; SC-011 Source now gives a reproducible classification rule |

Also established: `.specify/project/goal/` was **never materialized** (the generator creates it on demand), so the migration moves no data — it is a code/doc/test change only. The "transitional dual-path" edge case is retained as a guard but is vacuous in this repo.

**Baseline frozen**: 40 failed / 1308 passed / 1 skipped, names in `baseline-failed.txt`. The single new failure versus 036's merge baseline (`test_review_prerequisite_flags_are_supported`) was diagnosed by running it: it asserts `tasks.md` is in `AVAILABLE_DOCS`, which is false on a branch that has no `tasks.md` yet. Branch-state-dependent, not a defect, self-resolving at `/speckit.tasks` — and it incidentally confirmed the `Related Feature` binding is machine-readable (`"FEATURE_ID":"041"`).

**Re-validation after the plan-phase edits**: 42 FRs contiguous FR-001…FR-042; 18 SCs paired 1:1 with sources; 5 user stories; 0 live markers; all 5 shared strings resolving; Clarifications gained a fifth session entry (append-only held, prior four untouched); the only surviving "37 个文件" string is inside the new entry that documents its supersession. All 16 checklist items still pass. Spec status advanced Draft → Planned.

## Notes

- **The `[NEEDS CLARIFICATION]` marker retained at draft time is now resolved** (2026-08-05): the host CLI's `/goal` contract was established from its official documentation, and the finding — inline text only, no file or identity option — is recorded in `## Out of Scope`. The draft's judgement to hold the marker rather than guess a config format was validated: a guess would have specified a non-existent option.
- **`Related Feature` is now bound to 041 (Goal Registry)**, resolved at this clarify checkpoint as the draft anticipated. The binding went to a new Feature rather than 027 because goal has consumers outside the team domain, which is exactly the tension the draft flagged as needing the binding-precedent heuristic.
- **Grounded in measurement, not assertion**: the "goals are scattered" premise was verified before drafting — all 4 existing teams carry the goal in **two** places each (frontmatter `goal:` + `## Goal` body = 8 copies of 4 goals), 12+ team-domain files discuss goal authoring, and **no** team declares `goal_slug` yet. `.specify/goal/` does not exist; `.specify/project/goal/` is referenced by ~12 source files and 10 test files from 036. These figures are the baselines in SC-001…SC-004.
- **Content Quality item 1, scope note**: the spec names framework artifacts (`team.md`, `goal_slug`, `.specify/goal/`, script names). In this project the framework artifacts *are* the product surface, so these are domain nouns rather than implementation leakage — consistent with the convention in `035-token-efficiency` and `036-team-summary`.
- **Deliberate non-goals**: the spec does not merge goal with `requirement` or `Feature` (three different layers), and does not change Feature Index semantics.
