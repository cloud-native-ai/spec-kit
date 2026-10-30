# Contract: Coaching Run

**Scope**: the run as a whole — inputs, Trainee resolution, run identity, artifact set and order, execution-first priority, dispatch cardinality, evaluation, optimization, run status, governance.

**Literal authority**: the 17 Shared Strings (`STR-001`…`STR-017`) and the closed status vocabularies are owned by [`../requirements.md`](../requirements.md) § Shared Strings. This contract refines field-level shape only; on any disagreement the requirements file wins.

## C-1 Inputs

- The skill accepts **exactly two positional parameters**: `<trainee-name|trainee-path>` and `<work>`.
- `<work>` MUST be non-empty. A missing or empty parameter fails closed and names the missing parameter.
- `<work>` enters the run directory and the dispatch payload **verbatim**; the skill MUST NOT rewrite, summarize, or re-scope it.
- The skill MUST NOT substitute one parameter for the other, and MUST NOT pick a topic on the user's behalf when `<work>` is absent.
- Missing-argument handling is a plain one-sentence clarification, not a confirmation step.

## C-2 Trainee Resolution

- Resolution reuses the `run-skills` position ladder (canonical internal → canonical external → installed internal → installed external). No second resolution rule exists.
- A source hit and its installed mirror hit are **one** hit for the same skill (they are the same entity); only two distinct layers carrying the same name are two hits.
- Two hits → fail closed, naming both candidate paths.
- Zero hits → fail closed, naming the resolved identifier and the searched coordinates.
- A directory without a readable `SKILL.md`, or with invalid frontmatter, is rejected before the expectation phase.
- A target resolving to `coaching-skills` itself is rejected (recursion depth 1); no dispatch happens.
- When the host can only load by explicit path, the run uses the `run-skills` explicit-path mode and records it in the DispatchRecord `mode`.

## C-3 Run Identity and Directory

- `run-id` is `YYYYMMDDTHHMMSSZ-<trainee-slug>` (UTC timestamp, lowercase kebab slug of the resolved Trainee name).
- The run directory is `.specify/memory/coaching/<run-id>/` (STR-013). The skill creates it before writing the expectation.
- If that directory already exists, the run fails closed naming the existing path. The skill MUST NOT append a suffix or reuse the directory.
- All four artifacts are written inside the run directory; no artifact path escapes it.

## C-4 Artifact Set and Ordering

- The run produces exactly the four files named by STR-014…STR-017.
- `expectation.md` MUST land on disk before the first action of the dispatched subagent. The DispatchRecord's `dispatched-at` is the ordering evidence.
- `observation.md`, `deviations.md`, `improvement-plan.md` follow in that order; a missing file fails the run regardless of how good the others are.
- The run's two closed status values are recorded once, in `improvement-plan.md` § Run Status (see C-10).

## C-5 Execution-First Priority

- The primary success condition of a run is: the Trainee's real work completed and its primary artifact exists.
- Optimization MUST NOT be a precondition of execution and MUST NOT shorten, redirect, or simplify the execution to collect optimization material.
- The coach MUST NOT run any Trainee step in parallel with the subagent.

## C-6 Single Dispatch, No Re-Run

- A run dispatches **exactly one** subagent. A failed, timed-out, or refused dispatch is recorded as such and is never retried inside the same run.
- After a failed dispatch the run continues into `deviations.md` and `improvement-plan.md`; “continue” means exactly that and nothing more.
- The coach never executes Trainee steps itself and never injects side effects into the subagent's work.

## C-7 Deviations

- `deviations.md` compares expectation against observation on both dimensions (STR-008, STR-009).
- Every finding cites concrete evidence from `observation.md` (step id and/or artifact path).
- Every finding is classified `result-deviation` or `process-deviation`; a partially completed Trainee flow MUST separate the two classes.
- The report MUST state where the coach's reading of `<work>` and the Trainee's actual reading/execution materially diverged (beyond normal execution noise).

## C-8 Improvement Plan

- `improvement-plan.md` entries name a concrete Trainee file and section plus one concrete tweak.
- Generic advice (“improve clarity”, “be more careful”) is invalid as an entry.
- Each entry cites `D-*` findings, or is explicitly marked `evidence: none` when no execution evidence exists.
- When observation is empty, the plan is still produced; it MUST NOT be dropped for lack of evidence.

## C-9 Optimization Application

- **Protocol owner**: [`../data-model.md`](../data-model.md) § Optimization claim owns the claim protocol — its path, its timing (one atomic step inside `plan-written → optimization-*`, after the execution loop is complete and the improvement plan is written, before `improve-skills` is invoked), its atomic creation, its conflict rule, its release and its leftover semantics. This clause references that owner and states no second version of it.
- The plan is applied through the existing `improve-skills` entry, passing the Trainee target and the deviation evidence.
- The skill MUST NOT rewrite Trainee files directly during this run, and MUST NOT change `improve-skills`' contract.
- A claim is taken only by the owner's single exclusive-create primitive on the owner's shared path. Deciding by scanning sibling run directories — or by any other read-then-write sequence — is a non-conforming implementation of this clause, and so is creating a claim at an earlier transition than the owner's timing permits.
- A claim conflict fails this step closed: the recorded outcome is `optimization: failed` — one value of STR-010's closed domain, no new value and no extra branch — with the conflicting run-id named as the owner's conflict rule prescribes.
- A rejection by `improve-skills` is recorded as `optimization: failed` (or `unavailable` when the entry could not be resolved) and is not retried in a loop.

## C-10 Run Status

| Field | Closed domain | Recorded in |
|-------|---------------|-------------|
| `run` | `success` \| `partial` \| `failed` | `improvement-plan.md` § Run Status |
| `optimization` | applied \| skipped \| unavailable \| failed (STR-010) | same section |

- **Semantics owner**: [`../data-model.md`](../data-model.md) § RunStatus owns the verdict ladder — how an execution outcome plus an optimization outcome combine into these two values. This clause owns the field shape and the recording location; the skill body (`SKILL.md`) and the run report reference the owner instead of restating the ladder. The one boundary rule this clause does fix is the FR-017 exception below, because it is the misreading the shape must prevent.
- **FR-017 exception, stated at the contract boundary because it is the misreading this shape must prevent**: optimization status is reported beside the execution verdict, never inside it. An unavailable, skipped, or failed optimization never turns a completed Trainee execution into `failed`. When the primary artifact is complete per its `OC-1` criterion the optimization cap does not apply and the run closes `run: success` — unless the owner's separate partial trigger fires (zero observation evidence, `data-model.md` § RunStatus rule 2); otherwise the run stays at or below `partial`. Optimization status is never an input to this decision.
- The user-facing run report restates both values and names the four artifact paths.

## C-11 Degradation Ladder

- Host events available → steps are `host-event`.
- Host events unavailable, subagent self-report available → steps are `self-report`.
- Neither → the step is a row marked `observation-gap`, counted in the gap list, never invented.
- No observation at all → the plan still exists and every entry is `evidence: none`; the verdict follows [`../data-model.md`](../data-model.md) § RunStatus (zero observation evidence is not `success`).

## C-12 Dispatch Mechanism Boundary

- Subagent dispatch reuses host-native capability first; `run-agent` is the fallback; `run-skills` only resolves and executes the Trainee and carries no dispatch duty.
- No second dispatch mechanism is introduced.
- The mode used is recorded in the DispatchRecord.

## C-13 Governance Budget

- The skill remains `classification: external`; it MUST NOT move into the internal layer.
- New wording introduced by this feature MUST NOT add blocking confirmation phrasing: the judged unit is the added line in `git diff`, and those lines must contain zero hits against `scan-confirmation-gates.py`'s blocking patterns. The executable judgment (pathspec, pattern source, baseline reading) is owned by `identity-and-wiring.contract.md` C-8 § New-line gate; this clause states the rule, not the command.
- Relaying a destructive step that belongs to the Trainee's own flow is a governance-kept relay, not a new gate: the skill states the step, gets the answer, then dispatches; the subagent never self-approves.

## C-14 Dual Independent Context

- The coach forms its expectation from its own reading of `<work>`; the subagent receives `<work>` verbatim plus the Trainee target plus “execute per the Trainee's own SKILL.md”.
- The dispatch payload MUST NOT contain the expectation, deviation guesses, or the coach's conclusions.
- The coach MUST NOT pre-digest `<work>` to remove the independence of the two readings; divergence is a reportable finding, not something to eliminate.
