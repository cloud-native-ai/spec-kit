# Data Model — 081 Stricter Acceptance & Artifact Review

**Owner boundary**: this file defines the **entities, fields and validation rules** the feature introduces; the *schema authority* for the four new tables, the two vocabularies and the closed reason set is `shared/workflow/acceptance-hardening.md` (requirements [[STR-017]]). Where this file and that owner disagree, the owner wins and this file is stale.

**Projection surface (SC-009 ④)**: this file is a declared projection of the owner — its value domains may narrow the owner's, never expand them, and it restates no state-transition row set (see § E-8). The uniqueness guard asserts exactly those two properties instead of counting this file's literals as duplicate hits.

**Census**: 10 entities (E-1 … E-10), 30 validation rules (V-1 … V-30), 2 state machines (SM-1 feature status, SM-2 line state), 1 closed reason set (7 values), 2 closed vocabularies (verification status, runtime-stack form).

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
| `final_path` | `{pass, blocked, deferred, partial, fail, unknown, total}` — six status buckets plus the total, computed **here and only here**; `unknown` = no status row exists, `partial` = a measured `partial` |
| `flow_class` | `execution` / `expression` |
| `exit code` | `0` accept · `1` block · `2` input missing/unparsable |

**Closed reason set (7, no growth without an owner revision)**: `zero-final-path-pass`, `final-path-not-pass: SC-NNN`, `blocked-without-measurement-ladder: SC-NNN`, `runtime-dependency-not-owned: RS-NNN`, `falsified-premise-undecided: EP-NNN`, `inherited-blocker-undisposed: <feature>:<row>`, `status-claims-implemented-but-blocked`. One argument slot has a **reserved literal** instead of an id: `runtime-dependency-not-owned: runtime-stack` is the instance for the zero-data-row shape (V-27) — that shape has no `RS-NNN` to name, and emitting nothing would be the false green the finding exists to catch. `RS-\d{3}` never equals that literal, so the two forms do not collide; the grammar is owned by `requirements.md` § Shared Strings.

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
| `Contract` | repo-relative path | required for `signed-contract`; MUST resolve to a file in the checkout. Its own cell — reading it out of `Owner` prose is what made the check unreadable |
| `Joint acceptance` | named owner or command | required for `signed-contract` and `in-scope` |
| `FR` | `FR-NNN` list | required for `in-scope` (the FR that delivers it) |
| `Premises` | `EP-NNN` list | the premise ids every FR of this row depends on; each MUST exist in `plan.md` § Execution Premises and obey V-18…V-19 |

- **V-15**: `in-scope` means **this feature delivers the capability**; a capability supplied externally and only consumed here MUST be `signed-contract` (or `user-waived`) — recording it `in-scope` merely renames outsourcing.
- **V-16**: a prose-only dependency declaration with no row is a violation ([[STR-011]]). The defect is not "there is an external dependency"; it is "the dependency exists only as prose". Decidable by rule, not by reading: fenced code blocks and headings are removed, then a `- **Runtime dependency**: <capability> — <owner>` line inside the section is a declaration (with an `RS-NNN` ⇒ the reason; without one ⇒ input error), and a narrative line without that marker is not.
- **V-17**: `user-waived` MUST cite the user ruling and state the residual risk. A missing ruling is `runtime-dependency-not-owned: RS-NNN` ([[STR-011]]); an empty residual-risk field is the same reason; `not-required` on an `execution`-class feature is an input error.
- **V-27**: the runtime-row class has **three shapes and three verdicts, never a silent pass**: section absent ⇒ input error (exit 2); section present with **zero data rows** ⇒ `runtime-dependency-not-owned: runtime-stack` (the reserved argument owned by `requirements.md` § Shared Strings); a data row with a required-but-empty cell ⇒ `runtime-dependency-not-owned: RS-NNN`. Zero data rows is the most complete form of "no table row" and MUST NOT be read as "no runtime dependency".
- **V-28**: cell-shape defects are input errors, existence/acceptability defects are reasons: a `Form` value outside the domain, `not-required` on an `execution` feature, a `Premises` id with no matching `EP` row, and an unresolvable `Contract` path ⇒ exit 2; a missing `RS` obligation or an unsupported waiver ⇒ [[STR-011]]. The split is FR-009's and is not re-decided per caller.

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

- **V-18**: every FR that consumes a runtime capability MUST cite a premise ID, and the carrier is the `Premises` cell of the runtime-stack row naming that FR — not a prose sentence in the plan. Each cited `EP-NNN` MUST exist in this table; a cell naming an absent id is an input error, and a `falsified` premise there without a `Decision` is [[STR-012]].
- **V-19**: a known negative conclusion MUST NOT be parked as "out-of-scope P2/P3" — it becomes a `falsified` premise with a `Decision`.
- **V-20** (A13 boundary): plan premises are planning-time facts; `tasks.md` § Environment Prerequisites owns task-generation probe verdicts; the same fact MUST live in exactly one of the three carriers and be referenced by pointer from the others.

## E-7 — Inherited Blocker

**Carrier**: `plan.md` § Inherited Blockers.
**Parser**: `closure-acceptance-check.py` (extraction from dependency feature details).

| Field | Domain | Rule |
|---|---|---|
| source | `<feature>:<row>` | a dependency's `## Deferred` row, its `blocked`/`deferred`/**`partial`** `verification.md` status row, or its **non-empty** `deferred_tasks=` list. Single grammar, no whitespace: `<feature-id>:<row-locator>` with `<row-locator>` ∈ `SC-\d{3}_status` / `deferred_tasks` / `deferred:<slug>` |
| Disposition | `resolved` / `inherited` / `not-applicable` | closed |
| Carrier | `task:<T-ID>+test:<repo-relative test path>` or `gate:<GATE-ID>` | required when `Disposition=inherited`; the task form is **conjunctive** (task row *and* its test module); MUST resolve and MUST NOT be a deferrable `supporting`-path SC (the three dispositions' obligations are owned by `requirements.md` FR-011) |
| Carrier slice | `this-slice` / a later slice id (`081c`, `081d`, …) | a later slice is legal only while the parent feature is `Blocked` and the slice is in `plan.md` § D10's table; the row then reads **`inherited-later`** — disclosed, neither blocking nor resolved |
| Carrier (later slice) | `test:<repo-relative test path>` alone | allowed only when `Carrier slice` names a later slice: the task id does not exist yet and writing one would be fabricated; the row is re-read at that slice's closure, where the carrier MUST become `task:<T-ID>+test:<path>` and resolve (V-30) |
| Evidence / note | path + one line | required |

- **V-21**: every extracted row MUST have a disposition; an undisposed row is [[STR-013]] `inherited-blocker-undisposed: <feature>:<row>`. The join key is the source row: a locator disposed twice is an input error (two dispositions, one key). An `inherited` row with no `Carrier`, a `Carrier` that does not parse as one of the two forms, a `Carrier` that does not resolve, or a `Carrier` that points at a deferrable `supporting`-path SC is judged **the same** as an undisposed row, under the same reason (the closed set does not grow). A later-slice `Carrier slice` is **not** in that class — V-29.
- **V-22**: the dependency set is derived and stated (with the basis for each exclusion); it is never implied.
- **V-29**: `inherited-later` is a **fourth reading, not a fourth disposition**: the disposition field stays three-valued, and the reading is derived from `Carrier slice` + the parent's claimed status. It MUST be counted separately from resolved carriers and MUST NOT be counted as undisposed — conflating it with either is what made this feature's own `inherited` row look like an unresolved blocker while its carrier was simply scheduled in a later slice. Its carrier is `test:<path>` alone, because the task id belongs to an unwritten `tasks.md`; the row is completed and re-read when its slice closes (V-30).
- **V-30**: an `inherited-later` row MUST be re-read at its carrier slice's closure: the carrier MUST then be completed to `task:<T-ID>+test:<path>` (both parts resolving) or the row is an undisposed row **in that slice**, under the same [[STR-013]] reason. Writing a task id before that slice's `tasks.md` exists is forbidden — an id nobody can resolve is a fabricated premise, not evidence.

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

**Authority for the eight dispositions**: `requirements.md` § Assumptions A6 items 1–8 own the obligations (which invariants change, which must not, and where recovery goes); `skills/external/sdd-loop-driver/scripts/line-registry.py` is the implementation those obligations land in, and `tests/contract/test_line_state_blocked.py` is the single test carrier that pins each one (SV-13). This section keeps only the entity boundary — its carrier, its parser and the closed-set growth above. It MUST NOT restate the eight dispositions: a second copy here would be an unguarded duplicate (the same defect SC-009 ④ guards elsewhere), and the implement-stage landing map is recorded once, in `plan.md` § D6, as a pointer to A6 items 1–8.

- **V-25**: `blocked` and `merge_ready=true` MUST be mutually exclusive at every write point — the obligation is A6 item 4; this rule names the assertion the guard must carry, not a second definition of the disposition.
- **V-26**: no line-level never-regress rule is introduced — the line state set never had that semantics and this feature does not add one (A6 closing sentence).

## E-10 — Review composition record

**Carrier**: `REQUIREMENTS_DIR/review.md` (slots `### 2.1` … `### 2.4`), plus `REQUIREMENTS_DIR/code-review.md` for the code segment.
**Parser**: `/speckit.review`; the guards in `tests/contract/test_review_*`.

| Entity | Fields | Owner |
|---|---|---|
| Segment run record | `segment` (process / artifact / implementation / code), `judgment object`, `verdict`, `findings[]` | `templates/commands/review.md` (order) + each segment's skill (method) |
| Expected artifact set | `expected_artifacts[]` — every artifact the slice's stage rules and `plan.md` § Project Structure require; each member is judged | the artifact segment's coverage **denominator**. A member that is missing is itself a finding, never a silent exclusion from the denominator (obligation owned by `requirements.md` FR-013; derivation rule owned by the owner doc § Review Composition) |
| Finding | `severity`, `artifact or diff path`, `line` (optional), `statement` | artifact/implementation: `P0`/`P1`/`P2` family owned by `review-sdd-process`; code: the six-level family owned by `code-review`; no conversion |
| ARC record | the `final_path` record copied verbatim (`pass`, `blocked`, `deferred`, `partial`, `fail`, `unknown`, `total`), `claimed_status`, `verdict`, fixed item `F-ACCEPTANCE` (`P0`) | deterministic, from the closure checker output (never re-counted; never narrowed to a three-count summary) |
| Unit census | four units: `/speckit.review`, `skill:review-sdd-process`, `skill:review-feature-quality`, `skill:code-review` — same `run_id`, distinct `unit_id` | each unit's own closing record |

Findings are never merged across families, never converted, never scored as one number.

## Fixture set (the declarative inputs the rules are proved on)

**Carrier**: `tests/fixtures/acceptance-hardening/<case>/` — each case is a minimal file set (`requirements.md`, `plan.md`, `tasks.md`, `verification.md`, a feature detail, a registry row); no case references a real feature directory.

**The `Slice` column is what keeps absence readable**: a case whose slice has not landed yet is *not there yet*, not *missing*. 081a's seven cases exist on disk today; 081b adds five (`premise-mutation`, `runtime-gap-mutation`, `runtime-zero-row`, `inherited-mutation`, `inherited-clean`) and 081d adds `audit-history`; all of them are listed here so the table states the intended corpus instead of the current directory listing. A dependency-side case carries, in addition to the `positive` shape, a **dependency feature detail and its `verification.md`** — that is the artifact the extraction reads, and a fixture without it can only prove that a judgement fires, never that extraction discovers rows.

| Case | Slice | Shape | Proves |
|---|---|---|
| `positive` | 081a | `final`-path SCs all `pass`, complete smoke record, runtime rows valid, premises all `verified` | V-1…V-29 do not over-block (`accept`, exit 0); its runtime-stack section also carries **one narrative line that mentions `RS-004` without the declaration marker**, which proves the prose rule's exclusion arm (V-16 / V-27: an id inside narrative prose is not a declaration) |
| `negative` | 081a | zero `[ ]`, every SC has a status row, every `final`-path SC is `blocked`/`deferred` (the 026 shape) | V-23/V-9 block at all three call sites with a named reason |
| `premise-mutation` | 081b | one `falsified` premise with the `Decision` **cell emptied** (the row stays, the value goes) | `falsified-premise-undecided: EP-NNN` — "emptied", not "deleted", so the finding is about a missing decision and not about a missing row |
| `runtime-gap-mutation` | 081b | one capability declared as `- **Runtime dependency**: … — RS-905` with **no** table row (plus one narrative `RS-` mention without the marker, which MUST NOT fire), and one `signed-contract` row with an empty `Pin` and an empty `Contract` cell | `runtime-dependency-not-owned: RS-905`, and the same reason for the row with the empty cells — two shapes, one reason |
| `runtime-zero-row` | 081b | the runtime-stack section present with header + separator and **no data row**, everything else as in `positive` | V-27's middle shape: `runtime-dependency-not-owned: runtime-stack` (block) — not a silent pass, and not an input error |
| `inherited-mutation` | 081b | a dependency detail carrying all three source kinds — a `## Deferred` section with two bullets, a `verification.md` with `blocked`, `deferred` and `partial` rows, and a **non-empty** `deferred_tasks=` list — with exactly one of those rows left undisposed and one `inherited` row whose `Carrier` names a `supporting`-path SC | the extraction set is non-empty and the fourth finding fires (`inherited-blocker-undisposed: <feature>:<row>`), for both the undisposed row and the ineligible carrier |
| `inherited-clean` | 081b | the same dependency-side shape as `inherited-mutation`, every row disposed (two `resolved`, one `not-applicable`, one `inherited` with a `task:…+test:…` carrier, one `inherited-later` with `Carrier slice = 081c` while the fixture's claimed status is `Blocked`) | the extraction branch has a **counterexample**: rows really are discovered, and the `inherited-later` reading neither blocks nor counts as resolved |
| `ladder-mutation` | 081a | a `blocked` row with all five ladder fields; then `SC-NNN_reduced_measurement_run=no` | `blocked-without-measurement-ladder: SC-NNN` |
| `smoke-mutation` | 081a | `positive` with the smoke record removed, claimed `Implemented` | V-9 / V-12: a claimed-`Implemented` feature whose completion condition ④ fails is `block` (exit 1) with the named reason [[STR-014]], never `Implemented` — this is the one fixture that proves [[STR-014]] |
| `mixed-path` | 081a | an `execution` feature with three SCs: `SC-001` `final` `pass`, `SC-002` `final` `fail`, `SC-003` `supporting` `deferred` (full ladder) | V-11 + Edge Case "final 与 supporting 混合": the reason is `final-path-not-pass: SC-002` (`zero-final-path-pass` is **not** emitted, since one `final` passed), and the lone `supporting` non-`pass` is not a standalone blocking reason |
| `expr-supporting-only` | 081a | an `expression` feature whose SCs are all `supporting`, one of them `deferred` with the full ladder | V-11's `expression` exemption: the `final`-path rule is vacuous — no `final`-path reason is emitted and the fixture MUST NOT be forced to invent a `final` SC |
| `execution-without-final` | 081a | an `execution` feature whose SCs are all `supporting` (zero `final`-path SC) | V-1 via `validate-requirements.py` check `path-marker` (an `execution` feature with zero `final`-path SC **fails**), and at the checker layer `final_path.total = 0` so V-11's `zero-final-path-pass` applies |
| `audit-history` | 081d | an `Implemented` feature that would become `Blocked` under the new rules | `--audit-existing` reports it, writes nothing, exits 0 |
