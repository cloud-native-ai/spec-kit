# Data Model — 081 Stricter Acceptance & Artifact Review

**Owner boundary**: this file defines the **entities, fields and validation rules** the feature introduces; the *schema authority* for the four new tables, the two vocabularies and the closed reason set is `shared/workflow/acceptance-hardening.md` (requirements [[STR-017]]). Where this file and that owner disagree, the owner wins and this file is stale.

**Projection surface (SC-009 ④)**: this file is a declared projection of the owner — its value domains may narrow the owner's, never expand them, and it restates no state-transition row set (see § E-8). The uniqueness guard asserts exactly those two properties instead of counting this file's literals as duplicate hits.

**Census**: 10 entities (E-1 … E-10), 26 validation rules (V-1 … V-26), 2 state machines (SM-1 feature status, SM-2 line state), 1 closed reason set (7 values), 2 closed vocabularies (verification status, runtime-stack form).

Every entity below states its **carrier** (the file that physically holds it) and its **parser** (the code that reads it) — the two must be named together, because an entity whose carrier exists but whose parser does not is exactly the "green check that proves nothing" failure mode (Constitution XVI).

## E-1 — Path-annotated Success Criterion

**Carrier**: `requirements.md`, inside every `- **SC-NNN**: …` definition line.
**Parser**: `scripts/python/validate-requirements.py` (check `path-marker`) and `scripts/python/closure-acceptance-check.py`.

| Field | Domain | Rule |
|---|---|---|
| `id` | `SC-\d{3}` | dense sequence, owned by `validate-requirements.py` check `id-contiguous` |
| `text` | free text | the criterion statement, unchanged by this feature |
| `path` | `final` / `supporting` | literal marker `**Path**: final` or `**Path**: supporting`, written as the **last token** of the definition line, exactly once per line |

- **V-1**: an `execution`-class feature MUST carry at least one `final`-path SC. An `expression`-class feature is exempt and MUST NOT be forced to invent one.
- **V-2**: the marker MUST be the last token of the line and MUST occur exactly once; a second `**Path**` occurrence, a value outside the closed two-value domain, or a missing marker is a **format violation** reported by `validate-requirements.py` with file and line.
- **V-3**: when the marker cannot be parsed, `closure-acceptance-check.py` exits `2` (input error) and MUST NOT report `accept` or a `block` reason.

**Why an inline marker and not a table**: A4 (requirements § Assumptions) — an inline attribute needs no second structure kept in sync with the SC list, and both existing parsers anchor only on the line prefix, so the trailing marker is tolerated without touching them.

## E-2 — Verification status row

**Carrier**: `verification.md` (seeded from `templates/verification-log-template.md`).
**Parser**: `closure-acceptance-check.py`; `gate-implement-evidence-binding` reads the evidence fields.

| Field | Domain | Required for |
|---|---|---|
| `SC-NNN_status` | `pass` / `fail` / `partial` / `blocked` / `deferred` / `unknown` | every SC |
| `SC-NNN_value` | free text / number | optional (raw measurement) |
| `SC-NNN_note` | one line | optional |
| `SC-NNN_blocked_at` | ISO date or a named reason | `blocked`, `deferred`, `partial` |
| `SC-NNN_reduced_measurement` | free text (what *can* be measured instead) | `blocked`, `deferred`, `partial` |
| `SC-NNN_reduced_measurement_run` | `yes` / `no` | `blocked`, `deferred`, `partial` |
| `SC-NNN_why_reduced_insufficient` | free text | `blocked`, `deferred`, `partial` |
| `SC-NNN_unblock` | free text (what would lift it) | `blocked`, `deferred`, `partial` |
| `SC-NNN_deferred_reason` | free text | `deferred` (pre-existing field, kept) |

- **V-4**: the vocabulary is a closed six-value set; the owner of the set is `templates/verification-log-template.md` and no gate may narrow it to a subset.
- **V-5**: a `blocked` / `deferred` / `partial` row missing any of the five ladder fields is **illegal**.
- **V-6**: a row whose `SC-NNN_reduced_measurement` is non-empty while `SC-NNN_reduced_measurement_run=no` is **illegal** — honesty is not an accepted substitute (reason [[STR-010]]). The trigger is mechanical: it reads *non-empty*, never "available".
- **V-7**: `blocked` means *the environment cannot measure this assertion, so the feature is not acceptable*; `deferred` means *not attempted this round and the feature may still be acceptable* — the second is only legal on a `supporting`-path SC.

## E-3 — Smoke test record

**Carrier**: `verification.md` (three keys), mirrored in `tasks.md` as a task row.
**Parser**: `closure-acceptance-check.py`; the implement gate reads it as condition ④.

| Field | Domain | Rule |
|---|---|---|
| `smoke_command` | one shell command, verbatim | exactly one per feature; end-to-end over the feature's main flow, not the full suite |
| `smoke_exit_code` | integer | `0` for a feature claiming `Implemented` |
| `smoke_evidence_path` | repo-relative path | the file MUST exist and be non-empty |

- **V-8**: exactly one smoke record per feature (a second `smoke_command=` line is a defect, not a choice).
- **V-9**: a feature that cannot run its smoke MUST land `Blocked`; a missing or non-zero exit code MUST NOT be read as `Implemented`.
- **V-10**: "needs a real cluster / real network" is NOT an exemption — either the command is made deterministic with a local fixture, or the feature is `Blocked`.

## E-4 — Closure verdict

**Carrier**: stdout JSON of `scripts/python/closure-acceptance-check.py`; consumed by three call sites; the ARC counts are then written into `review.md`.
**Parser**: the three call sites (implement gate, review, driver closure/merge).

| Field | Domain |
|---|---|
| `verdict` | `accept` / `block` (binary; no middle tier) |
| `reasons[]` | `{code, target}` where `code` ∈ the closed 7-value reason set |
| `final_path` | `{pass, blocked, deferred, fail, unknown, total}` — computed **here and only here** |
| `flow_class` | `execution` / `expression` |
| `exit code` | `0` accept · `1` block · `2` input missing/unparsable |

**Closed reason set (7, no growth without an owner revision)**: `zero-final-path-pass`, `final-path-not-pass: SC-NNN`, `blocked-without-measurement-ladder: SC-NNN`, `runtime-dependency-not-owned: RS-NNN`, `falsified-premise-undecided: EP-NNN`, `inherited-blocker-undisposed: <feature>:<row>`, `status-claims-implemented-but-blocked`.

- **V-11**: `zero-final-path-pass` is emitted once when the `final`-path `pass` count is zero; `final-path-not-pass: SC-NNN` is emitted per failing SC when at least one other `final`-path SC passed. Both are in the set, so either satisfies "a named reason". For an `expression`-class feature the `final`-path rule is **vacuous** (V-1 / FR-001 / Edge Case "只有 supporting SC 的表达类特性"): when the `Path` marker parse succeeds and the feature class is `expression`, neither reason may be emitted merely because there is no `final`-path SC — the class is read from `flow_class` in the same payload (E-4), so the exemption is mechanical, not a judgement.
- **V-12**: `status-claims-implemented-but-blocked` fires only when the claimed status is `Implemented` or `Ready for Review` **and** the verdict is `block` — i.e. it is the ARC's deterministic basis, and it can never fire during `Planned → Implemented` (where the claimed status is `Planned`).
- **V-13**: `--audit-existing` is zero-write and exits `0` whenever inputs are valid, regardless of findings; it MUST NOT block anything and MUST NOT rewrite history.
- **V-14**: the checker is read-only and stdlib-only; it MUST NOT consult a model, a network, or `.specify/.tmp`.

## E-5 — Runtime Stack Row

**Carrier**: `requirements.md` § Runtime Stack & Dependency Ownership.
**Parser**: `closure-acceptance-check.py`; `pre-analyze-check.py` reports the same row set as a finding source.

| Field | Domain | Rule |
|---|---|---|
| `ID` | `RS-\d{3}` | dense, unique |
| `Capability` | free text | one runtime capability the feature consumes or delivers |
| `Form` | `in-scope` / `signed-contract` / `user-waived` (+ `not-required` for expression-class, with reason) | closed |
| `Owner` | free text | who provides it |
| `Pin` | version / digest / commit | required for `signed-contract`; MUST be measured, never invented |
| `Joint acceptance` | named owner or command | required for `signed-contract` and `in-scope` |
| `FR` | `FR-NNN` list | required for `in-scope` (the FR that delivers it) |

- **V-15**: `in-scope` means **this feature delivers the capability**; a capability supplied externally and only consumed here MUST be `signed-contract` (or `user-waived`) — recording it `in-scope` merely renames outsourcing.
- **V-16**: a prose-only dependency declaration with no row is a violation ([[STR-011]]). The defect is not "there is an external dependency"; it is "the dependency exists only as prose".
- **V-17**: `user-waived` MUST cite the user ruling and state the residual risk.

## E-6 — Execution Premise

**Carrier**: `plan.md` § Execution Premises.
**Parser**: `closure-acceptance-check.py`; `pre-analyze-check.py` (plan stage).

| Field | Domain | Rule |
|---|---|---|
| `ID` | `EP-\d{3}` | dense, unique |
| `Premise` | free text | one load-bearing assumption the plan rests on |
| `Evidence` | path / command / measurement | citable |
| `Status` | `verified` / `unverified` / `falsified` | closed |
| `Decision` | `resolve-in-scope` / `fallback` / `user-waiver` | required when `Status=falsified` (reason [[STR-012]] `falsified-premise-undecided: EP-NNN`) |

- **V-18**: every FR that consumes a runtime capability MUST cite a premise ID.
- **V-19**: a known negative conclusion MUST NOT be parked as "out-of-scope P2/P3" — it becomes a `falsified` premise with a `Decision`.
- **V-20** (A13 boundary): plan premises are planning-time facts; `tasks.md` § Environment Prerequisites owns task-generation probe verdicts; the same fact MUST live in exactly one of the three carriers and be referenced by pointer from the others.

## E-7 — Inherited Blocker

**Carrier**: `plan.md` § Inherited Blockers.
**Parser**: `closure-acceptance-check.py` (extraction from dependency feature details).

| Field | Domain | Rule |
|---|---|---|
| source | `<feature>:<row>` | a dependency's `## Deferred` row, its `verification.md` status row, or its `deferred_tasks=` list |
| Disposition | `resolved` / `inherited` / `not-applicable` | closed |
| Evidence / note | path + one line | required |

- **V-21**: every extracted row MUST have a disposition; an undisposed row is [[STR-013]] `inherited-blocker-undisposed: <feature>:<row>`.
- **V-22**: the dependency set is derived and stated (with the basis for each exclusion); it is never implied.

## E-8 — Feature status `Blocked` (SM-1)

**Carrier**: `templates/feature-details-template.md` § Canonical Status State Machine; the live value lives in `.specify/memory/features/<ID>.md` `**Status**` and in the `features.md` row.
**Parser**: `/speckit.implement`, `/speckit.review`, `manage-features`, the closure checker (claimed-status input).

**Row set owner**: `shared/workflow/acceptance-hardening.md` § Feature Status ([[STR-017]]) owns the `From | To | Allowed | Condition` rows for `Draft` / `Planned` / `Blocked` / `Implemented` / `Ready for Review` / `Completed`, including the explicitly **illegal** `Blocked → Ready for Review` and the narrow `Implemented → Blocked` audit-correction row; `templates/feature-details-template.md` § Canonical Status State Machine is the carrier those rows must physically land in (FR-002 / FR-003 / FR-018). This section keeps only the entity boundary, its carrier and parser, and the two rules the checker reads below — the transition table MUST NOT be restated here (SC-009 ④ asserts **0** transition rows in this file; a restated row is an unguarded duplicate).

- **V-23**: the never-regress rule gains exactly one narrow exception — `Implemented → Blocked` with cited audit evidence; every other backward move stays illegal.
- **V-24**: `Implemented → Ready for Review`'s fourth condition: no `final`-path SC in `blocked` / `deferred` / `fail`, unless an explicit **user** waiver exists (a driver's or agent's confirmation is never a user ruling).

## E-9 — Line state `blocked` (SM-2)

**Carrier**: `skills/external/sdd-loop-driver/scripts/line-registry.py`.
**Parser**: the engine itself; `integrate-lines.py`; `promote-waiting` / `ownership-check`.

State set grows 7 → 8: `{active, waiting, stalled, completed, orphaned, stale, closed, blocked}`.

| # | Invariant | Effect |
|---|---|---|
| I-1 | `ACTIVE_STATES = {active, waiting}` unchanged | `blocked` never appears in `--active` lists, never holds a concurrency slot |
| I-2 | `HOLDING_STATES = {active, completed}` unchanged, with a declared rule | the `blocked` transfer releases the lease and clears `holder_line_id` / `waiting_reason` / `queued_at` |
| I-3 | `merge_ready=true ⇒ state=completed` unchanged | plus a new assertion: `state=blocked` with `merge_ready=true` is rejected on the same validation point |
| I-4 | `integration-enqueue` / `integration-plan` / `integration-record` require `state=completed` unchanged | a `blocked` line is structurally un-enqueueable and unrecordable |
| I-5 | terminal guard set stays `{closed, stale, orphaned}` | `blocked` is recoverable by design and MUST NOT join it |
| I-6 | `promote-waiting` requires `state=="waiting"` unchanged | a `blocked` line cannot shortcut ownership re-acquisition |
| I-7 | `stale_from_state` may carry `blocked` | no enum expansion; comment + test only |
| I-8 | recovery path = `update --state active` + recorded unblock reason | requires the "entering `active`" guard to admit `blocked` alongside `{waiting, stalled}` (measured interaction, `research.md` § R6) |

- **V-25**: `blocked` and `merge_ready=true` MUST be mutually exclusive at every write point.
- **V-26**: no line-level never-regress rule is introduced — the line state set never had that semantics and this feature does not add one.

## E-10 — Review composition record

**Carrier**: `REQUIREMENTS_DIR/review.md` (slots `### 2.1` … `### 2.4`), plus `REQUIREMENTS_DIR/code-review.md` for the code segment.
**Parser**: `/speckit.review`; the guards in `tests/contract/test_review_*`.

| Entity | Fields | Owner |
|---|---|---|
| Segment run record | `segment` (process / artifact / implementation / code), `judgment object`, `verdict`, `findings[]` | `templates/commands/review.md` (order) + each segment's skill (method) |
| Finding | `severity`, `artifact or diff path`, `line` (optional), `statement` | artifact/implementation: `P0`/`P1`/`P2` family owned by `review-sdd-process`; code: the six-level family owned by `code-review`; no conversion |
| ARC record | `final_pass`, `final_blocked`, `final_deferred`, `claimed_status`, `verdict`, fixed item `F-ACCEPTANCE` (`P0`) | deterministic, from the closure checker output (never re-counted) |
| Unit census | four units: `/speckit.review`, `skill:review-sdd-process`, `skill:review-feature-quality`, `skill:code-review` — same `run_id`, distinct `unit_id` | each unit's own closing record |

Findings are never merged across families, never converted, never scored as one number.

## Fixture set (the declarative inputs the rules are proved on)

**Carrier**: `tests/fixtures/acceptance-hardening/<case>/` — each case is a minimal file set (`requirements.md`, `plan.md`, `tasks.md`, `verification.md`, a feature detail, a registry row); no case references a real feature directory.

| Case | Shape | Proves |
|---|---|---|
| `positive` | `final`-path SCs all `pass`, complete smoke record, runtime rows valid, premises all `verified` | V-1…V-26 do not over-block (`accept`, exit 0) |
| `negative` | zero `[ ]`, every SC has a status row, every `final`-path SC is `blocked`/`deferred` (the 026 shape) | V-23/V-9 block at all three call sites with a named reason |
| `premise-mutation` | one `falsified` premise with `Decision` removed | `falsified-premise-undecided: EP-NNN` |
| `runtime-gap-mutation` | one runtime dependency present as prose only; one `signed-contract` row with empty `Pin` | `runtime-dependency-not-owned: RS-NNN` |
| `ladder-mutation` | a `blocked` row with all five ladder fields; then `SC-NNN_reduced_measurement_run=no` | `blocked-without-measurement-ladder: SC-NNN` |
| `smoke-mutation` | `positive` with the smoke record removed | feature is `Blocked`, never `Implemented` |
| `mixed-path` | an `execution` feature with three SCs: `SC-001` `final` `pass`, `SC-002` `final` `fail`, `SC-003` `supporting` `deferred` (full ladder) | V-11 + Edge Case "final 与 supporting 混合": the reason is `final-path-not-pass: SC-002` (`zero-final-path-pass` is **not** emitted, since one `final` passed), and the lone `supporting` non-`pass` is not a standalone blocking reason |
| `expr-supporting-only` | an `expression` feature whose SCs are all `supporting`, one of them `deferred` with the full ladder | V-11's `expression` exemption: the `final`-path rule is vacuous — no `final`-path reason is emitted and the fixture MUST NOT be forced to invent a `final` SC |
| `execution-without-final` | an `execution` feature whose SCs are all `supporting` (zero `final`-path SC) | V-1 via `validate-requirements.py` check `path-marker` (an `execution` feature with zero `final`-path SC **fails**), and at the checker layer `final_path.total = 0` so V-11's `zero-final-path-pass` applies |
| `audit-history` | an `Implemented` feature that would become `Blocked` under the new rules | `--audit-existing` reports it, writes nothing, exits 0 |
