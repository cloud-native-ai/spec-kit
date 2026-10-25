# Requirements Quality Checklist: Task Decomposition & Team Coordination for Subagent-Driven SDD

**Purpose**: Pre-analyze requirements-quality gate for Feature 070 — a "unit test for requirements writing" covering FR testability, SC measurability, ownership/non-duplication, decomposition-gate failure modes, scheduler/concurrency safety, verifier independence, retry/escalation, integration/single-commit semantics, observability/`not_evaluated`, opt-out/fallback, and tests/red-first evidence. It validates the *requirement text*, not implementation behaviour.
**Created**: 2026-10-25
**Feature (Requirement Scope)**: Feature 070 — 驱动子代理的任务拆解与配合机制（Task Decomposition & Team Coordination for Subagent-Driven SDD）
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md) · [tasks.md](../tasks.md) · [data-model.md](../data-model.md) · [contracts/](../contracts/) · [notes/clarify-decisions.md](../notes/clarify-decisions.md)
**Distinct from**: `checklists/requirements.md` (the pre-plan 16-item completeness gate). This file is the post-tasks requirements-quality gate; it neither replaces nor re-checks that file's generic items.

**Note**: Plan, tasks, contracts, data model, and clarify notes are cited only to expose requirement gaps, ambiguities, conflicts, and traceability breaks. No item is answered by running the product.

## Verdict Semantics

- `[x]` = **PASS** — the requirement text (including its Assumptions, Clarifications, Edge Cases, and explicit owner references) fixes the decision or names an owner so two readers reach the same verdict; an evidence pointer is given.
- `[ ]` = **FAIL** — a gap, ambiguity, conflict, or untraceable delegation remains; an evidence pointer and an analyze disposition are given.
- Every item is a question with a quality dimension and a requirement/SC reference. `[Gap]`, `[Ambiguity]`, `[Conflict]`, and `[Assumption]` mark items whose traceability is a missing or conflicting requirement.
- This is a judged checklist: **40 items — 7 PASS / 33 FAIL**. A FAIL is a requirements-quality finding for `analyze`, not a stage-run anomaly, and not an instruction to edit upstream artifacts in this stage.
- Depth: Standard · Audience: Reviewer · Focus: decomposition-gate/concurrency safety and verification/integration/metrics. The stage brief fixes scope, risk, and depth, so the skill's intent-clarification round is not run in unattended mode.

**Same-author detection**: The requirements → clarify → plan → tasks set was produced by the same agent lineage across prior stage sessions. The literal same-session trigger in `.specify/shared/workflow/objective-analysis-gate.md` does not fire because the artifacts predate this execution; the gate's staffing rule was applied anyway. Detection was split across two fresh-context read-only subagents with disjoint scopes: (A) `requirements.md` only; (B) `plan.md`, `data-model.md`, `contracts/`, `tasks.md`, `quickstart.md`, and `notes/clarify-decisions.md`, used only to expose requirement gaps. Validation re-opened every cited line. Detector B's 16 findings were accepted/merged (3 became new items, 1 split across 2 items, 12 merged into existing items; 2 severity downgrades; 0 rejected). Detector A's 16 findings yielded 14 accepted/merged, 1 downgraded to a terminology note, and 1 rejected as design-owned (the replay algorithm is fixed by WP-04/WP-06/WP-15, so the requirement's replay property is not defective). No detector validated a finding it produced.

---

## A. Ownership, Scope & Non-Duplication (FR-001…FR-005, FR-025…FR-027; 058/060/061/063/064/067/068)

- [ ] CHK001 — Is the run-specific "required stage output" inventory that FR-003(b) and SC-004 measure against fixed in the requirements (or in a named clarify owner), or must the design invent the per-stage inventory? [Completeness, Req §FR-003(b), SC-004]
  - **Verdict**: FAIL — FR-003(b) requires exactly-once output coverage but never defines the inventory; the design fixes four per-stage inventories in data-model E13 and makes them the WG-08 orphan test, so a plan is judged against a list the requirements do not own. The integrator also assembles the stage deliverable, but FR-003(b)/SC-004 assign every required output to a package and never say whether the integrator's assembled output is owned by a package.
  - **Evidence**: `requirements.md:195`; `requirements.md:272` (SC-004); `data-model.md:366-377`; `contracts/wp-gate.md:14`; `contracts/verification-and-integration.md:16,18`; `data-model.md:302`.
  - **Disposition**: Decision — analyze must ratify the per-stage inventories into the requirements or an explicitly referenced clarify owner; otherwise SC-004's "required stage outputs" has no requirement-level referent.

- [ ] CHK002 — Does FR-025/A12 enumerate every preserved owner (including 060 `run-agent` and 061 `CAPABILITY_MATRIX`) and state that the new U0 declaration fields are additive to 058's U0 contract? [Completeness, Req §FR-025, A12; 060/061]
  - **Verdict**: FAIL — FR-025 preserves 058/063/064/067/068 but omits 060 and 061; A12 names the new U0 fields but never says whether adding them changes 058's U0 semantics. The design treats both as additive (FN-01, SD-15) without requirement authorization.
  - **Evidence**: `requirements.md:232`; `requirements.md:77`; `requirements.md:18-19`; `contracts/fallback-and-nonregression.md:6`; `contracts/scheduler-and-dispatch.md:20`.
  - **Disposition**: Correction — add 060/061 to the preservation clause and state that the U0 fields are additive spine keys owned by 058.

- [x] CHK003 — Is the boundary between the 070 Work Package and the 067 part brief stated as "additive extension, one brief format, one dispatch log," rather than as a change to Feature 067's part-brief rules? [Consistency, Req §FR-025, A11]
  - **Verdict**: PASS — A11 explicitly authorizes the extension and keeps the 067 fields and dispatch log authoritative; WP-12 repeats "one brief format and one dispatch log" and supplies the field-by-field merge (`part_id`, `task_ids`, `turns`, `test_delta`, `commit`, `outcome`, `duration_seconds`, `token_cost`); FR-020's list is a minimum, not an exhaustive schema.
  - **Evidence**: `requirements.md:232`; `requirements.md:76`; `requirements.md:224`; `contracts/work-package-model.md:18`; `research.md:19-27`.

- [x] CHK004 — Is the stage-team preset's compatibility target and seat vocabulary traceable to the `create-team` preset contract, with no catalog registration and no `create-team`/`run-team` modification? [Completeness, Req §FR-008, FR-006]
  - **Verdict**: PASS — FR-008 enumerates the preset fields, forbids a persisted team, and forbids modifying the two skills; the design pins the owner document and the four seats. The Worker/Meta choice is permissive (all four seats are Worker).
  - **Evidence**: `requirements.md:201-203`; `notes/clarify-decisions.md:13-16`; `contracts/stage-team-adapter.md:7-10`; `data-model.md:286-295`.

- [x] CHK005 — Does FR-027 confine delivery and forbid a second registry, ownership model, integration queue, ledger, brief format, service, daemon, external dependency, or model API, with the WP ledger explicitly placed inside the 058 spine? [Completeness, Req §FR-027, FR-020]
  - **Verdict**: PASS — FR-027 states the closed delivery surface and the non-duplication list; FR-020 places the package ledger in the line state spine; the ownership table and D9.3 confirm 064/067/068 primitives are reused, not replaced.
  - **Evidence**: `requirements.md:224`; `requirements.md:234`; `requirements.md:51-62`; `notes/clarify-decisions.md:516-523`.

## B. Functional Requirement Clarity & Non-Ambiguity (FR-001…FR-014, FR-024; A1/A3)

- [ ] CHK006 — Does FR-009 quantify whether a concurrently dispatched package must declare **all** of isolated ports, temporary directories, and caches, or **any one** isolation resource plus a shared read-only resource? [Clarity, Req §FR-009]
  - **Verdict**: FAIL — the sentence reads "isolated ports, temporary directories, and caches, or a read-only shared resource"; the design resolves it as any one of port/temp/cache/shared_readonly (WG-16, V-DEC.6). Two readers can implement different admission rules.
  - **Evidence**: `requirements.md:204`; `contracts/wp-gate.md:22`; `data-model.md:258`.
  - **Disposition**: Correction — replace "and" with a closed "any one of" rule (or require all three) and align WG-16.

- [ ] CHK007 — Is `parallel_safe` given an observable obligation (true only for read-only; false excludes concurrent dispatch), or is it only listed as a required field? [Clarity, Req §FR-001, FR-003(c)]
  - **Verdict**: FAIL — FR-001 requires the field but no FR says what true/false changes; the design makes it a concurrency predicate (WP-02, WG-11, V-WP.3). A package could set false and still be dispatched concurrently under the literal FR-003(c).
  - **Evidence**: `requirements.md:193`; `requirements.md:195`; `contracts/work-package-model.md:8`; `contracts/wp-gate.md:17`; `data-model.md:59`.
  - **Disposition**: Correction — define the field's effect in FR-001/FR-003(c).

- [ ] CHK008 — Are "bounded" and "not beneficial" fixed by mechanical rules, including a guard against relabeling an oversized package as `bounded_by.unit=acceptance` or `artifacts` with count 1? [Measurability, Req §FR-003(d), FR-005, A12]
  - **Verdict**: FAIL — FR-003(d) allows "an equivalent declared acceptance scope" with no size ceiling; the design lets `artifacts`/`acceptance` take any positive count (V-WP.7) and only WG-09 checks tasks/clauses. FR-005's "not beneficial" is made mechanical only by the design's WG-13 benefit test. Both rules are invention points.
  - **Evidence**: `requirements.md:195`; `requirements.md:197`; `requirements.md:77`; `contracts/wp-gate.md:15,19`; `data-model.md:63`; `research.md:175`.
  - **Disposition**: Decision — ratify the WG-13 benefit rule and add a stage-specific size ceiling (or explicitly authorize the acceptance-unit bound).

- [ ] CHK009 — Does FR-002's `tasks` → phase/task-group decomposition rule conflict with FR-024/A1, which keep `requirements`, `tasks`, and `checklist` single-subagent in the first slice? [Conflict, Req §FR-002, FR-024, A1]
  - **Verdict**: FAIL — FR-002 lists a `tasks` rule; FR-024 and A1 say `tasks` remains single-subagent; the design's stage enum and R18 rule table drop `tasks` entirely. A reader cannot tell whether the rule is dead, deferred, or forbidden.
  - **Evidence**: `requirements.md:194`; `requirements.md:231`; `requirements.md:66`; `data-model.md:34`; `research.md:195`.
  - **Disposition**: Decision — delete the `tasks` rule from FR-002 or define `tasks` as a first-slice stage; align A1/FR-024 and E13.

- [ ] CHK010 — Is "contradictory outputs" in FR-014 defined well enough for two verifiers/integrators to agree, or is detection left entirely to implementation judgment? [Ambiguity, Req §FR-014]
  - **Verdict**: FAIL — FR-014 requires detecting "contradictory outputs" but gives no rule (same artifact claimed by two packages, differing content, incompatible values); VI-06 repeats the term without a definition.
  - **Evidence**: `requirements.md:212`; `contracts/verification-and-integration.md:11`; `plan.md:216`.
  - **Disposition**: Correction — define the contradiction classes or delegate to a named verification owner with a fixed check.

- [ ] CHK011 — Does FR-010 authorize both dispatch forms — `run-agent` native and the detached `stage-runner.sh` remote path — or does its "through the `run-agent` mechanism" wording exclude the design's remote runner? [Consistency, Req §FR-010, FR-027]
  - **Verdict**: FAIL — FR-010 says every package is dispatched "through the `run-agent` mechanism"; the design's remote topology uses one detached `stage-runner.sh` per package (SD-08) and treats both as existing paths (SD-15). The requirement does not name the runner or a topology-selection rule.
  - **Evidence**: `requirements.md:208`; `contracts/scheduler-and-dispatch.md:13,20`; `notes/clarify-decisions.md:300`.
  - **Disposition**: Decision — ratify both dispatch forms and the local/remote selection rule in FR-010 (or define the runner as a `run-agent` transport).

- [ ] CHK012 — Is "read-only package" defined precisely enough to decide whether writing its own result/verdict evidence under the state directory is permitted, without contradicting FR-011's "no package may write outside its `owned_paths`"? [Clarity, Req §A1, A3, FR-011]
  - **Verdict**: FAIL — FR-011 forbids writes outside `owned_paths`; a read-only package has an empty write territory by design, yet D2.4/WP-11 permit it to write its evidence file and V-RES.3 carves that path out. The requirements never state the state-directory exception, so the literal invariant is violated by every read-only package.
  - **Evidence**: `requirements.md:68`; `requirements.md:209`; `notes/clarify-decisions.md:196`; `contracts/work-package-model.md:17`; `data-model.md:191`.
  - **Disposition**: Correction — define "read-only" as repository-content read-only and add the state-directory evidence exception to FR-011.

## C. Consistency & Acceptance-Criteria Measurability (SC-001…SC-007)

- [ ] CHK013 — Is the decomposition-decision vocabulary closed at two values (`decomposed` or `single-package`), as SC-005 says, or at four values including `disabled` and `fallback`, and is one canonical record fixed among the stage-attempt declaration, plan fence, and ledger `plan` event? [Conflict, Req §SC-005, FR-005, FR-026]
  - **Verdict**: FAIL — SC-005 enumerates two values; FN-08/E8/D8.1 use four; the design records the decision in three places with no precedence. SC-005 also requires a gate verdict, but `disabled` and `fallback` can occur without a decomposition gate verdict (explicit off, exit 2). The acceptance check cannot be written without choosing one.
  - **Evidence**: `requirements.md:273`; `requirements.md:197`; `requirements.md:233`; `contracts/fallback-and-nonregression.md:13`; `data-model.md:248`; `notes/clarify-decisions.md:474`.
  - **Disposition**: Decision — fix the four-value vocabulary and name one canonical decision record (plan fence or ledger event), with the others referencing it.

- [ ] CHK014 — Is SC-001's baseline basis fixed — median vs range vs upper-bound anchor, minimum comparable samples, "same stage scale," and host/topology comparability — rather than split between the SC text and A5/D7? [Measurability, Req §SC-001, A5]
  - **Verdict**: FAIL — SC-001 says "versus their baseline medians (plan 65–70 min; review 17–37 min)", but the dated record is a range, not a median; A5/D7 switch to the upper-bound anchor (70/37 min), require at least three comparable samples, and define stage scale only in design OR-13. The baseline's 65–70/17–37 min are whole-stage durations, while FR-022 defines wall-clock as first package dispatch to U4 completion; the two are not the same interval. The SC text and the owner disagree on the comparison basis.
  - **Evidence**: `requirements.md:269`; `requirements.md:39`; `requirements.md:70`; `requirements.md:226`; `contracts/observability-and-retry.md:19`; `notes/clarify-decisions.md:452-453`.
  - **Disposition**: Correction — align SC-001's wording to the anchor/sample rule and state that a re-measured baseline replaces it.

- [ ] CHK015 — Does SC-002 define its "1.5" cap (absolute executions per canonical stage or a ratio to a baseline), and does the metric count one stage dispatch per stage attempt rather than one `plan` event, and does excluding package retries leave the rework target blind to package thrash? [Measurability, Req §SC-002, FR-022, A4]
  - **Verdict**: FAIL — "at most 1.5×" has no reference, while "no worse than 1.5 absolute" implies the absolute metric; SC-002 compares to the 2.6× worst measured baseline (063), while FR-023 requires a comparable measured baseline (064's 1.4× is the comparable record); OR-07 defines `stage_attempts` as the count of `plan` events, and WP-10 appends a second `plan` event after a repair, so a repaired stage attempt counts twice; package retries are excluded from SC-002 (OR-08) even though they consume wall-clock and evidence.
  - **Evidence**: `requirements.md:270`; `requirements.md:42`; `requirements.md:227`; `contracts/observability-and-retry.md:13-14`; `contracts/work-package-model.md:16`; `data-model.md:343`.
  - **Disposition**: Decision — define the numerator as stage dispatch attempts (not plan events) and state whether package retries are a separate reported metric or folded into rework.

- [ ] CHK016 — Is SC-006's denominator fixed — per completed benchmark feature, per run, or per session — and does the record carry both numerator and denominator needed for "normalized per session"? [Ambiguity, Req §SC-006, FR-022]
  - **Verdict**: FAIL — SC-006 mixes "per completed benchmark feature" with "30 interventions across 29 sessions, normalized per session"; FR-022 defines interventions per run; OR-09/OR-11 accept only one integer and no session denominator. No requirement names the artifact that records interventions: the ledger has no intervention field and the report's `--manual-interventions` is an optional input. The SC cannot be computed as written.
  - **Evidence**: `requirements.md:274`; `requirements.md:226`; `contracts/observability-and-retry.md:15,17`; `data-model.md:321`; `tasks.md:327`.
  - **Disposition**: Correction — fix one denominator (per session or per run) and add the session count to the report input/record.

- [ ] CHK017 — Does SC-007 define the trigger "at least two ready packages" at a specific point in time and separate package retries from stage retries in the report? [Clarity, Req §SC-007]
  - **Verdict**: FAIL — "ready" is a per-dispatch state; a serial decomposed stage may never have two ready at once, so the SC's population is undefined; "retries" is unqualified although FR-022 and OR-08 count package and stage retries separately.
  - **Evidence**: `requirements.md:275`; `requirements.md:226`; `contracts/observability-and-retry.md:14`; `data-model.md:319`.
  - **Disposition**: Correction — define "ready" as a scheduling state and require the two retry counts explicitly.

## D. Decomposition Gate Failure Modes (FR-003, FR-026; Edge Cases)

- [ ] CHK018 — Does FR-003 fix the gate-repair budget and the second-reject outcome, or does the design's "one repair, then fallback" introduce that decision? [Completeness, Req §FR-003]
  - **Verdict**: FAIL — FR-003 says a gate failure "MUST be resolved by splitting, serializing, or falling back to one package" but never says how many repairs are allowed or that a second reject triggers fallback; the design fixes one repair (WG-18/D3.4).
  - **Evidence**: `requirements.md:195`; `contracts/wp-gate.md:24`; `notes/clarify-decisions.md:275-276`.
  - **Disposition**: Correction — add the one-repair limit and the second-reject fallback to FR-003 or A3/A12.

- [ ] CHK019 — Are all fallback causes — exit-2/unavailable, unrepresentable stage contract, and "loses its evidence" — mapped to one named reason, and is "loses its evidence" reconciled with the missing-verdict edge case (package failure + retry) rather than a stage fallback? [Completeness, Req §FR-026, Edge Case]
  - **Verdict**: FAIL — FR-026 lists "unavailable, fails its own gate, or loses its evidence"; FN-06 names only `gate-reject`, `decomposition-unavailable`, `not-beneficial` and adds the unrepresentable contract without a distinct reason; a missing verdict is a package failure under VI-04, not a fallback. The evidence-loss trigger has no decision rule.
  - **Evidence**: `requirements.md:233`; `requirements.md:184`; `contracts/fallback-and-nonregression.md:11-12`; `contracts/verification-and-integration.md:9`.
  - **Disposition**: Decision — define which evidence losses trigger fallback vs package failure, and add a cause value for the unrepresentable contract.

- [x] CHK020 — Is the decomposition rule and its package list replay-deterministic, with the rule, source artifacts, IDs, edges, and hash recorded before dispatch? [Measurability, Req §FR-002, FR-004]
  - **Verdict**: PASS — FR-002 requires a declared replayable rule and a recorded rule/package list; FR-004 requires the record before dispatch; WP-04/WP-06 fix ID assignment and the canonical hash. The exact source-artifact/ID/hash procedure and the WP execution contract are design-owned (WP-04/WP-06/WP-15); the requirement fixes the replay property, not the algorithm.
  - **Evidence**: `requirements.md:194`; `requirements.md:196`; `contracts/work-package-model.md:10,12,21`; `data-model.md:104`.

## E. Scheduler & Concurrency Safety (FR-007, FR-009, FR-011, FR-012, FR-015)

- [ ] CHK021 — Is the slot-cap default and ceiling fixed in the requirements, and is the interaction between a `serial` pattern and concurrent read-only packages stated? [Completeness, Req §FR-007, FR-009, FR-011, A12]
  - **Verdict**: FAIL — FR-011 says "within the declared slot cap" and A12 declares `decomposition_slot_cap` without a default; the default 2, the ceiling `min(4, allowance)`, and the rule that a serial stage may still run independent ready read-only packages concurrently are design-only (SD-04, D4.1).
  - **Evidence**: `requirements.md:209`; `requirements.md:204`; `requirements.md:77`; `contracts/scheduler-and-dispatch.md:9`; `notes/clarify-decisions.md:286`.
  - **Disposition**: Correction — fix the default/ceiling and the serial-pattern concurrency rule in FR-011 or A12.

- [ ] CHK022 — Does the requirements text require the scheduler to stop launching new read-only packages when a write becomes ready (no starvation), or only to wait for currently running packages, and does it state what happens when the host cannot issue parallel native calls? [Coverage, Req §FR-011, Edge Case]
  - **Verdict**: FAIL — the Edge Case says a write waits for running read-only packages to settle; SD-06 adds "stops launching new" and "never indefinitely deferred"; SD-07 adds the `host-no-parallel-native` fallback. Neither liveness nor host-capability behaviour is requirements-level.
  - **Evidence**: `requirements.md:185`; `requirements.md:209`; `contracts/scheduler-and-dispatch.md:11-12`; `notes/clarify-decisions.md:287`.
  - **Disposition**: Correction — add the no-starvation and host-capability rules to FR-011/Edge Cases.

- [ ] CHK023 — Is the concurrency rule single-valued across FR-007's `serial` pattern, FR-011's read-only concurrency, A3's gate rejection of unordered read/write or write/write pairs, US1.3's reject-then-serialize, and US2's independent test, and does it make package paths a subset of manifest `owned_paths` disjoint from `read_only_paths`/`forbidden_paths`? [Consistency, Req §FR-003(c), FR-007, FR-011, FR-012, FR-015, A3]
  - **Verdict**: FAIL — FR-007 selects `serial` for any graph containing a write package, but FR-011 permits independent read-only overlap and US2's Independent Test expects it; A3 says the gate rejects unordered read/write or write/write pairs, while US1.3 says a rejected plan is then serialized or split. The requirement never says whether `serial` constrains actual concurrency or only names the dominant pattern, nor whether the gate rejects or the scheduler serializes an unordered read/write pair. The WP schema also omits 064's `forbidden_paths`, so a package path can pass FR-003(c)/FR-009 without a forbidden-path check.
  - **Evidence**: `requirements.md:68`; `requirements.md:93`; `requirements.md:105`; `requirements.md:202`; `requirements.md:209`; `requirements.md:213`; `contracts/scheduler-and-dispatch.md:9`; `contracts/wp-gate.md:20-21`; `plan.md:192`.
  - **Disposition**: Decision — define `serial` as a pattern label that still permits read-only concurrency (or forbid it), assign the unordered-pair resolution to exactly one of gate rejection or scheduler serialization, and add the forbidden-path preflight to FR-003(c)/FR-009.

## F. Verifier Independence & Retry/Escalation (FR-013, FR-016)

- [ ] CHK024 — Does "not the package's executing subagent" permit the coordinator (`driver-u4`) to verify when no fresh subagent is available, or does independence require a fresh context in every case, and does the `driver-u4` label conflate package verification with 058's stage U4? [Ambiguity, Req §FR-016, FR-017]
  - **Verdict**: FAIL — FR-016 forbids only the executing subagent; the literal text would also permit the driver, the integrator, or another package's executor to verify; the design adds a fresh-context requirement and then a `driver-u4` fallback with `fresh_context=false`, reusing 058's U4 name. The requirement defines no unavailable-verifier path and does not bind verifier checks to 063's two-slot budget.
  - **Evidence**: `requirements.md:217-218`; `requirements.md:232`; `contracts/verification-and-integration.md:6-7`; `contracts/fallback-and-nonregression.md:15`; `data-model.md:226-234`; `research.md:179`.
  - **Disposition**: Decision — ratify `driver-u4` (with a distinct name and a recorded independence rationale) or remove it and require a fresh verifier.

- [ ] CHK025 — Does FR-016 define when contract vs adversarial checks are required ("where the package's acceptance admits them") and that a verifier may run only the package's declared targeted tests, never a full suite? [Ambiguity, Req §FR-016, FR-025]
  - **Verdict**: FAIL — the trigger for adversarial checks is undefined; the targeted-tests-only rule is design-level (VI-02/FN-10), inferred from the preserved two-slot budget rather than stated for verifiers.
  - **Evidence**: `requirements.md:217`; `requirements.md:232`; `contracts/verification-and-integration.md:7`; `contracts/fallback-and-nonregression.md:15`.
  - **Disposition**: Correction — define the check-kind trigger and state the verifier's test scope in FR-016.

- [ ] CHK026 — Is "changes the dispatch topology" in FR-013 quantified with a closed set of material changes, or is the design's OR-15 set the only definition? [Clarity, Req §FR-013]
  - **Verdict**: FAIL — FR-013 requires a topology change but gives no materiality rule; OR-15 fixes four forms and "materially different," while WG-17 rejects a "fake topology change" without a requirement-level definition.
  - **Evidence**: `requirements.md:211`; `contracts/observability-and-retry.md:21`; `contracts/wp-gate.md:23`.
  - **Disposition**: Correction — adopt the closed topology set and materiality rule in FR-013.

- [ ] CHK027 — Does the one-retry budget survive a split retry — do children inherit the parent's attempt count, is split depth or total attempts per stage capped — and does FR-013's "change the budget" mean strictly greater, as A4/D6 require? [Completeness, Req §FR-013, A4, Edge Case]
  - **Verdict**: FAIL — FR-013 and the Edge Case allow a split into `<parent>-a`/`<parent>-b` with fresh child packages; each child gets a fresh attempt counter, so recursive splits can exceed the one-retry budget. FR-013 says the budget may "change", while A4/D6 require strictly greater. "Fails twice" has no single counter when a parent is superseded.
  - **Evidence**: `requirements.md:211`; `requirements.md:182`; `requirements.md:69`; `contracts/observability-and-retry.md:21`; `contracts/work-package-model.md:14`; `contracts/wp-gate.md:23`.
  - **Disposition**: Decision — state whether children inherit the parent's attempt count, cap split depth/total attempts per stage, and make the budget delta strictly greater in FR-013.

## G. Integration & Single-Commit Semantics (FR-017…FR-019)

- [ ] CHK028 — Is the disposition of the single stage-closing commit defined when stage U4 fails after integration, and is the implement closing commit's content defined when 067 part commits already cover the deliverable? [Gap, Req §FR-017, FR-018]
  - **Verdict**: FAIL — FR-018 requires one stage commit after integration and forbids rewriting 067 part commits; it does not say whether the commit is rolled back, amended, or left when U4 then fails, nor whether the implement closing commit may be empty.
  - **Evidence**: `requirements.md:218-219`; `contracts/verification-and-integration.md:15-18`.
  - **Disposition**: Decision — define the commit/U4 ordering and the failed-U4 disposition, and whether an empty closing commit is permitted.

- [ ] CHK029 — Does the requirements text authorize the decomposed-stage integrator (a new subagent) to emit the stage sentinel `<STAGE>-DONE`, or does 058 reserve sentinel emission to the stage executor? [Ownership, Req §FR-017, FR-018; 058]
  - **Verdict**: FAIL — FR-017 says U4 is unchanged and FR-018 says the commit is by the driver or integrator; the design's VI-11 makes a new integrator execution emit `<STAGE>-DONE`. The requirement never says a package-era integrator may replace 058's sentinel emitter, and FR-010's "stage sentinel context" in the WP brief is not distinguished from the package's own sentinel.
  - **Evidence**: `requirements.md:218-219`; `contracts/verification-and-integration.md:16-17`; `notes/clarify-decisions.md:313-315`.
  - **Disposition**: Decision — confirm 058's emitter rule and either authorize the integrator explicitly or keep the stage executor as the sentinel emitter.

- [ ] CHK030 — Are the boundaries complete: package sentinels never satisfy the stage sentinel, partial integration is never reported/committed as complete, closure/merge stays driver-owned, and "no auto-merge" is defined so it does not forbid 058's driver-owned closing merge? [Completeness, Req §FR-018, FR-019, Edge Case; 058/064]
  - **Verdict**: FAIL — FR-019 forbids "auto-merge" without defining it; 058 requires each line to close by merging back to main and 064 owns the integration queue. The requirement does not say whether the line closing merge is the forbidden auto-merge or a permitted driver-owned merge after confirmation. The sentinel and partial-integration boundaries themselves are clear.
  - **Evidence**: `requirements.md:177`; `requirements.md:219-220`; `contracts/verification-and-integration.md:13,17,19`; `../../058-sdd-loop-driver/requirements.md:200`; `../../064-subagent-concurrency/requirements.md:220`.
  - **Disposition**: Decision — define "auto-merge" (package-level only?) and state that 058's line closing merge remains driver-owned under the existing confirmation gate.

- [x] CHK031 — Is the integration order deterministic with a declared tie-break, and is it distinguished from dispatch order? [Clarity, Req §FR-018]
  - **Verdict**: PASS — FR-018 requires a deterministic order derived from the graph with a declared tie-break; the design fixes `wp_id-lexicographic` and records integration order separately from dispatch order (SD-05, VI-07).
  - **Evidence**: `requirements.md:219`; `contracts/scheduler-and-dispatch.md:10`; `contracts/verification-and-integration.md:12`.

## H. Observability & `not_evaluated` (FR-020…FR-023)

- [ ] CHK032 — Are the metric formulas and interval/exclusion rules fixed: the parallelism-efficiency denominator, canonical-stage count, failed-attempt treatment, and exclusion of verifier/integrator durations? [Ambiguity, Req §FR-022]
  - **Verdict**: FAIL — FR-022's "summed package durations divided by wall-clock times the maximum concurrent package count" is parenthesization-ambiguous; it does not state how failed attempts enter wall-clock/critical path, nor that verifier/integrator executions are excluded. The design fixes all four (OR-04…OR-07, V-EXE.4).
  - **Evidence**: `requirements.md:226`; `contracts/observability-and-retry.md:10-12`; `data-model.md:237`; `notes/clarify-decisions.md:426`.
  - **Disposition**: Correction — parenthesize the formula and state the failed-attempt/verifier-exclusion rules in FR-022.

- [ ] CHK033 — Does FR-020's per-package field list uniquely address every dispatch attempt (stage attempt, WP attempt, attempt id) and include the stage-U4 completion timestamp needed for FR-022's wall-clock? [Completeness, Req §FR-020, FR-013, FR-022]
  - **Verdict**: FAIL — FR-020 lists "attempts" but no stage-attempt/WP-attempt key; the design adds `attempt_id = <wp_id>-a<N>-w<M>` and attempt-scoped evidence paths. It also has no `stage_u4_at` field, so FR-022's wall-clock is not derivable from the mandated spine fields; the design adds an optional `--stage-u4-at` report input. The requirement's own retry/evidence-attribution and metric-derivation goals need both fields.
  - **Evidence**: `requirements.md:224`; `requirements.md:196`; `requirements.md:226`; `contracts/observability-and-retry.md:8,10,17`; `contracts/work-package-model.md:17`; `data-model.md:152`.
  - **Disposition**: Correction — add the attempt identity and stage-U4 timestamp to FR-020's field list, or state that wall-clock is `not_evaluated` when absent.

- [ ] CHK034 — Is `not_evaluated` mandatory for every metric whose source is missing, and does the spec define the acceptance consequence when an efficiency criterion is `not_evaluated` — can the feature ship with every efficiency SC unevaluated? [Completeness, Req §FR-020, FR-023, SC-001]
  - **Verdict**: FAIL — the literal is mandatory and OR-10 forbids zero/estimate, but SC-001 only says a `not_evaluated` criterion is not "met"; no requirement says whether an all-`not_evaluated` result blocks acceptance, requires a waiver, or permits shipping without demonstrating the core value. T038 accepts `not_evaluated` as completion.
  - **Evidence**: `requirements.md:224`; `requirements.md:227`; `requirements.md:269`; `contracts/observability-and-retry.md:16`; `tasks.md:327`.
  - **Disposition**: Decision — define the acceptance consequence (blocking benchmark gate, explicit waiver, or fail) and align T038.

- [x] CHK035 — Does FR-021 fix the report's required fields and the "evidence by path, never raw transcripts" boundary precisely enough to check? [Completeness, Req §FR-021]
  - **Verdict**: PASS — FR-021 enumerates decomposition, pattern, slot cap, dispatch order, critical path, wall-clock, parallelism efficiency, retries, and verdicts; it requires evidence paths and forbids raw transcript dumps; OR-12/V-REP.3 repeat the boundary.
  - **Evidence**: `requirements.md:225`; `contracts/observability-and-retry.md:18`; `data-model.md:330`.

## I. Opt-Out & Fallback (FR-005, FR-024, FR-026; A12)

- [x] CHK036 — Is the opt-out precedence fixed — feature-level `off` as a hard opt-out, stage-attempt override over stage map over built-in defaults — and does the single-subagent path require no new field/argument? [Completeness, Req §A12, FR-005, FR-024]
  - **Verdict**: PASS — A12 fixes the fields, hard opt-out, precedence, and the no-new-argument single-package path; FN-02/FN-05 and D8.2 implement the same.
  - **Evidence**: `requirements.md:77`; `requirements.md:197`; `requirements.md:231`; `contracts/fallback-and-nonregression.md:7,10`.

- [ ] CHK037 — Is the meaning of `on` (as distinct from `auto` and `off`) defined for all gate outcomes — admit, reject, exit 2, and not-beneficial — including whether it can force decomposition for `analyze`/`clarify`? [Ambiguity, Req §A12, FR-005, FR-024]
  - **Verdict**: FAIL — FN-01 allows `auto|on|off`; only `auto` and `off` have resolution rules (FN-04/FN-05, D8.2). `on` has no defined outcome, and A1 says analyze/clarify require an explicit `on`, so the enabling value itself is underspecified.
  - **Evidence**: `requirements.md:77`; `contracts/fallback-and-nonregression.md:6,9-10`; `notes/clarify-decisions.md:483-484`; `data-model.md:256-257`.
  - **Disposition**: Decision — define `on` as "gate-admitted decomposition with the benefit test bypassed" or another closed rule, and align FN-04/V-DEC.4.

## J. Tests & Red-First Evidence (FR-028…FR-030)

- [ ] CHK038 — Does FR-028's contract-pin list cover the ledger event schema, metric definitions, `not_evaluated`, and opt-out precedence, and is the 110-clause coverage check more than an id-presence grep? [Completeness, Req §FR-028, FR-030]
  - **Verdict**: FAIL — FR-028 lists schema/gate/pattern/preset/preflight/retry/single-package but omits ledger/metrics/`not_evaluated` (FN-14 adds opt-out only). T039's `grep -q` passes if an id appears in a comment, so the 110-clause partition is not behaviour-pinned; this is exactly the FR-030 "would not turn red" class.
  - **Evidence**: `requirements.md:238,240`; `contracts/fallback-and-nonregression.md:19`; `tasks.md:328`; `tasks.md:46`.
  - **Disposition**: Decision — extend FR-028's pin set and replace the id-presence check with a behaviour-level assertion (or a red-driven mutation check).

- [ ] CHK039 — Does FR-029's "fixture-based dry runs MUST prove" the scenarios accept a simulator that models the prompt algorithm, or does it require the shipped driver path, and does the enumerated scenario set cover the edge cases (failure isolation, no nested driver, no persisted team, missing verdict)? [Ambiguity, Req §FR-029, SC-008]
  - **Verdict**: FAIL — the design's dry runs use `wp_driver_sim.py`, a test-only model of the algorithm; the plan discloses it does not prove an LLM's adherence. The FR-029 list also omits failure isolation, no nested driver, no team directory, and missing-verdict cases that SC-008 and the Edge Cases require.
  - **Evidence**: `requirements.md:239`; `requirements.md:276`; `plan.md:255,260`; `tasks.md:238,244`; `contracts/scheduler-and-dispatch.md:18`; `contracts/stage-team-adapter.md:15`.
  - **Disposition**: Decision — define what "dry run" proves (algorithm vs shipped path) and close the scenario list against the Edge Cases.

- [ ] CHK040 — Does FR-030 require evidence that a green check would turn red when its subject breaks (mutation/falsifiability), or only prohibit citing a non-falsifiable green? [Measurability, Req §FR-030]
  - **Verdict**: FAIL — FR-030 states the prohibition but imposes no positive obligation to demonstrate falsifiability; the design's mutation drills (T036) and non-regression net (T033) are additions. A green check can therefore satisfy FR-030 without ever being red.
  - **Evidence**: `requirements.md:240`; `contracts/fallback-and-nonregression.md:20`; `tasks.md:325`; `plan.md:257`.
  - **Disposition**: Decision — add a red-when-broken demonstration (mutation drill) to FR-030 or make it an explicit acceptance obligation.

---

## Traceability Matrix

All 30 FR and all 8 SC appear in at least one item; the mapping is collective, not one-item-per-requirement.

| Requirement | Items | Aspect |
|-------------|-------|--------|
| FR-001 | CHK001, CHK007, CHK012, CHK033 | WP fields, `parallel_safe`, read-only definition, attempt key |
| FR-002 | CHK001, CHK009, CHK020 | rule inventory, `tasks` conflict, replay |
| FR-003 | CHK001, CHK007, CHK008, CHK018, CHK023 | coverage, `parallel_safe`, boundedness, gate repair, concurrency invariant |
| FR-004 | CHK001, CHK020, CHK033 | pre-dispatch record, replay, attempt identity |
| FR-005 | CHK008, CHK013, CHK036, CHK037 | benefit, decision vocabulary, precedence, `on` |
| FR-006 | CHK004 | seat vocabulary / Worker–Meta |
| FR-007 | CHK021, CHK023 | pattern / slot cap / serial concurrency |
| FR-008 | CHK004 | preset contract / no persisted team |
| FR-009 | CHK006, CHK021 | resource isolation, slot cap |
| FR-010 | CHK011, CHK023 | dispatch form, sole coordinator |
| FR-011 | CHK012, CHK021, CHK022, CHK023 | read-only definition, slot cap, liveness/host, write-alone |
| FR-012 | CHK022, CHK023 | failure isolation |
| FR-013 | CHK026, CHK027, CHK033 | retry delta, counter, attempt identity |
| FR-014 | CHK010 | aggregation / contradictions |
| FR-015 | CHK023 | sole coordinator |
| FR-016 | CHK024, CHK025 | verifier independence, check scope |
| FR-017 | CHK028, CHK029, CHK030 | U4 ordering, sentinel emitter, boundaries |
| FR-018 | CHK028, CHK029, CHK030, CHK031 | commit/U4, integrator, sentinel, order |
| FR-019 | CHK030 | closure / no push |
| FR-020 | CHK005, CHK033, CHK034 | spine placement, attempt key, `not_evaluated` |
| FR-021 | CHK035 | report fields / no transcripts |
| FR-022 | CHK015, CHK016, CHK017, CHK032, CHK033 | metrics, denominators, stage-U4 timestamp |
| FR-023 | CHK034 | `not_evaluated` discipline |
| FR-024 | CHK009, CHK036, CHK037 | stage slice, precedence, `on` |
| FR-025 | CHK002, CHK003 | preserved owners, 067 boundary |
| FR-026 | CHK013, CHK019, CHK036 | fallback, causes, disabled path |
| FR-027 | CHK005, CHK011 | delivery surface, dispatch form |
| FR-028 | CHK038 | contract pin set |
| FR-029 | CHK039 | dry-run proof |
| FR-030 | CHK038, CHK040 | red-first evidence, falsifiability |
| SC-001 | CHK014, CHK034 | baseline/anchor, `not_evaluated` |
| SC-002 | CHK015 | stage-execution metric |
| SC-003 | CHK030, CHK039 | gate regression / sentinel |
| SC-004 | CHK001 | required-output coverage |
| SC-005 | CHK013 | decision vocabulary |
| SC-006 | CHK016 | manual interventions |
| SC-007 | CHK017 | report trigger / overlap |
| SC-008 | CHK039 | dry-run scenario set |

**Ownership coverage**: 058 → CHK002, CHK023, CHK029, CHK030; 060 → CHK002, CHK004, CHK005, CHK011; 061 → CHK002, CHK005; 063 → CHK002, CHK024, CHK025; 064 → CHK002, CHK005, CHK023; 067 → CHK003, CHK005, CHK028; 068 → CHK002, CHK005, CHK034; `create-team`/`run-team` → CHK004.

## Failing Items — Gate Hand-off

33 failing items are recorded for `analyze` disposition. None was repaired in this stage; requirements, plan, tasks, contracts, data model, clarify notes, feature-ref, and quickstart were read-only.

**Decision-class (analyze/requirements adjudication required)**

- CHK001 — required-output inventories (including the integrator's assembled deliverable) must become requirement-level or an explicitly referenced clarify owner.
- CHK008 — ratify the WG-13 benefit rule and close the acceptance-unit size loophole.
- CHK009 — `tasks` decomposition rule vs FR-024/A1 single-subagent stance.
- CHK011 — FR-010's `run-agent` wording vs the remote `stage-runner.sh` path.
- CHK013 — SC-005's two-value decision vocabulary vs the design's four values and three records; `disabled`/`fallback` have no gate verdict.
- CHK015 — SC-002's 1.5 cap/reference, comparator (2.6× worst vs comparable 1.4×), numerator (plan events vs stage dispatches), and package-retry blindness.
- CHK019 — evidence-loss trigger vs missing-verdict package failure; unrepresentable-contract cause.
- CHK023 — `serial` vs read-only concurrency, gate rejection vs scheduler serialization, and the missing 064 forbidden-path check.
- CHK024 — `driver-u4` self-verification vs fresh-context independence; other-executor verifiers; U4 name reuse.
- CHK027 — split-retry recursion vs the one-retry budget; children's attempt count; strict budget delta.
- CHK028 — closing-commit disposition when U4 fails; empty implement closing commit.
- CHK029 — authority for a new integrator subagent to emit the stage sentinel.
- CHK030 — "auto-merge" vs 058's driver-owned closing merge.
- CHK034 — acceptance consequence when every efficiency criterion is `not_evaluated`.
- CHK037 — `on` semantics for admit/reject/exit-2/not-beneficial.
- CHK038 — FR-028 pin set and the id-presence-only clause check.
- CHK039 — simulator-based dry runs vs FR-029's "MUST prove"; scenario-list closure.
- CHK040 — positive falsifiability obligation for red-first checks.

**Correction-class (one consistent reading; fix locally and disclose)**

- CHK002 — add 060/061 to FR-025 and state the U0 fields are additive to 058.
- CHK006 — replace the FR-009 "and/or" with a closed resource-isolation rule.
- CHK007 — define `parallel_safe`'s effect in FR-001/FR-003(c).
- CHK010 — define "contradictory outputs" or delegate to a named verification rule.
- CHK012 — define "read-only" as repository-content read-only and add the evidence-path exception to FR-011.
- CHK014 — align SC-001's "baseline medians" wording with A5/D7's anchor and ≥3-sample rule, and reconcile the whole-stage baseline with FR-022's dispatch-to-U4 wall-clock.
- CHK016 — fix SC-006's denominator and carry the session count and intervention source.
- CHK017 — define SC-007's "ready" trigger and name both retry counts.
- CHK018 — add the one-repair limit and second-reject fallback to FR-003.
- CHK021 — fix the slot-cap default/ceiling and the serial-pattern concurrency rule.
- CHK022 — add no-starvation and host-capability behaviour to FR-011/Edge Cases.
- CHK025 — define the adversarial-check trigger and the verifier's targeted-test scope.
- CHK026 — adopt the closed retry-topology set in FR-013.
- CHK032 — parenthesize the parallelism-efficiency formula and state exclusion rules.
- CHK033 — add the attempt identity and stage-U4 timestamp to FR-020.

## Validation Record

- **Checklist result**: 40 items — 7 PASS / 33 FAIL. FAILs are requirement-quality findings, not run anomalies.
- **Traceability**: 40/40 items carry a requirement/SC reference plus a quality dimension (100%, above the 80% floor); all 30 FR and all 8 SC appear in the matrix.
- **Detection/validation**: two fresh-context read-only detectors with disjoint scopes; every cited line re-opened by the orchestrator. Detector B's 16 findings were accepted/merged (3 new items, 1 split, 12 merged; 2 severity downgrades; 0 rejected). Detector A's 16 findings yielded 14 accepted/merged, 1 downgraded to a terminology note, and 1 rejected as design-owned (the replay algorithm is WP-04/WP-06/WP-15). No detector validated its own finding; the downgrade/rejection rate is 4/32.
- **Terminology observations**: detector A flagged inconsistent terms; `decomposed` vs `admit`, `single-package` vs `disabled`/`fallback`, and `per run` vs `per session` are adjudicated in CHK013/CHK016; `ready`/`dispatchable`/`settled`/`verified` in CHK017/CHK023; `stage wall-clock` vs the baseline's whole-stage duration in CHK014; `package ledger` vs `dispatch log` in CHK003. `max_turns` vs 067's run-turn budget is recorded for analyze; WP-12 maps `max_turns` as the budget and `turns` as the actual count.
- **Checklist structural check**: CHK001–CHK040 contiguous; 40/40 items carry a quality dimension plus a requirement/SC reference; 30/30 FR and 8/8 SC appear in the matrix; 7 PASS / 33 FAIL; 33 dispositions for 33 FAILs; rc 0. Evidence: `test-evidence/validate-checklist.txt`.
- **Upstream validators (post-write, read-only)**: `python3 scripts/python/validate-requirements.py .specify/specs/070-subagent-task-teams/requirements.md` → `status: ok`, 0 errors / 0 warnings, 320 lines / 38 definition rows, rc 0; `python3 scripts/python/validate-tasks.py .specify/specs/070-subagent-task-teams/tasks.md` → `PASS`, 0 errors / 0 warnings, rc 0.
- **Upstream files untouched**: `git diff --quiet` over requirements.md, plan.md, tasks.md, data-model.md, contracts/, notes/, quickstart.md, and feature-ref.md → rc 0. This file is new; `checklists/requirements.md` is unchanged.
- **Test budget**: docs-only; no full suite run; the two full-suite slots remain the implement baseline and closure. The E3 row is recorded at `test-evidence/checklist.jsonl` with `status=not-run-docs-only`.
- **No implementation testing**: no product behaviour was run; all verdicts are textual/traceability judgments against file:line evidence.
