# Acceptance Hardening — Feature Status, Verification Vocabulary, Gates and Closure Verdict

**Owner (single definition point)**: this file, `shared/workflow/acceptance-hardening.md`, owns the schemas that
make "may this feature be called `Implemented`?" a deterministic question: the feature-status value `Blocked`
and its four transitions, the verification vocabulary and its measurement ladder, the gate conditions that read
them, and the closure verdict with its closed reason set, exit codes and `final_path` counts. Every other
surface — template, command, skill, driver doc — reaches these by path plus `§ section anchor`, and **none
restates** a table, a value domain, a threshold or a reason literal.

**Declared carriers (projections, never second owners)**: `templates/feature-details-template.md` § Canonical
Status State Machine, `templates/verification-log-template.md` and `templates/tasks-template.md` (§ GATE-4)
physically hold what this file defines, because a consumer that is editing a template must find the rules where
it is editing. A carrier is a **declared projection**: it may not widen a value domain, and where a carrier and
this file disagree, this file wins and the carrier is stale.

**Scope of this revision**: § Feature Status · § Verification Vocabulary · § Gates · § Closure Verdict. Sections
belonging to later slices are listed in § Extension Points, together with the owner their obligations currently
have. Nothing here is inferred from a slice that has not landed.

**Machine-readable form**: `scripts/python/closure-acceptance-check.py` is the only program that turns these
schemas into a verdict. Its calling surface is fixed by a contract; its verdict is **not** re-derivable by a
model, by an ad-hoc grep, or by a second script.

## Feature Status

`Blocked` is a **first-class feature status**, not "`Implemented` with a note attached". It says: the work that
could be done is done, and the feature is still not acceptable. It exists because the pre-change bar —
every task closed, a status row per criterion — is satisfied by a feature whose main journey never ran.

### `Planned → Implemented` is four conjunctive conditions

All four MUST hold. Three of four is `Blocked`.

1. `tasks.md` has zero open rows — no `[ ]` and no `[>]`.
2. Every success criterion has a status row in `verification.md` (see § Verification Vocabulary).
3. **Every `final`-path criterion's status is `pass`.**
4. The feature's smoke record is `pass` (command, exit code `0`, evidence path present — see § Verification
   Vocabulary).

### The four `Blocked` transitions

| From | To | Allowed | Condition |
|------|----|---------|-----------|
| `Planned` | `Blocked` | yes | tasks are closed but at least one `final`-path criterion is not `pass` |
| `Blocked` | `Implemented` | yes | the blocker is lifted **and** every `final`-path criterion is `pass` |
| `Blocked` | `Ready for Review` | **no — illegal** | a blocked feature has not earned review; it must re-enter through `Implemented` |
| `Implemented` | `Blocked` | yes, narrow | **audit correction only**, and it MUST cite the evidence that makes the claim false |

### Never regress — one narrow exception

Every backward transition stays illegal, with exactly one exception: `Implemented → Blocked` as an audit
correction, and only while citing evidence. "The user did not object", an agent's own confirmation, or a later
discovery that nobody wrote down is not evidence.

## Verification Vocabulary

### The closed six-value status set

`pass` · `fail` · `partial` · `blocked` · `deferred` · `unknown`

Closed: no gate, Definition-of-Done row or task row may narrow it to a subset, because a narrower set silently
forbids an honest value and forces a reclassification judgement. **`blocked` vs `deferred`, in one sentence
each** — `blocked` means the environment cannot measure this assertion, so the feature is **not** acceptable;
`deferred` means the assertion was not attempted this round and the feature **may still** be acceptable, which
is legal only on a `supporting`-path criterion.

### The five measurement-ladder fields

A `blocked`, `deferred` or `partial` row MUST carry all five, named with the criterion id as prefix and spelled
exactly:

| Field | Content |
|-------|---------|
| `SC-NNN_blocked_at` | ISO date, or the name of the reason it is blocked |
| `SC-NNN_reduced_measurement` | what **can** be measured instead |
| `SC-NNN_reduced_measurement_run` | `yes` / `no` |
| `SC-NNN_why_reduced_insufficient` | why the reduced measurement does not stand in for the assertion |
| `SC-NNN_unblock` | what would lift it |

**Illegal row (mechanical trigger, no semantic judgement)**: `SC-NNN_reduced_measurement` is **non-empty** AND
`SC-NNN_reduced_measurement_run=no`. A missing ladder field is illegal in the same way. The trigger reads
*non-empty*, never "available" — a measurement written down and not run is not an honest substitute for running
it, it is the same shape as the defect the ladder was introduced to stop.

### The smoke record — three fields, exactly one per feature

| Field | Content |
|-------|---------|
| `smoke_command` | one shell command, verbatim; end-to-end over the feature's main flow, not the whole suite |
| `smoke_exit_code` | `0` for a feature claiming `Implemented` |
| `smoke_evidence_path` | repo-relative path to a file that exists and is non-empty |

A second `smoke_command=` line is a defect, not a choice. A feature that cannot run its smoke lands `Blocked` —
"needs a real cluster" or "needs real network" is **not** an exemption: either the command is made
deterministic on a local fixture, or the feature is `Blocked`. A **missing** smoke record is never an input
error; it is a completeness fact about the feature, and it blocks completion condition ④.

## Gates

### The fourth `Implemented → Ready for Review` condition

`Implemented → Ready for Review` is conjunctive like the transition that precedes it, and its fourth condition
is: **no `final`-path criterion sits in `blocked` / `deferred` / `fail`, unless an explicit user waiver names
it.** A waiver is a user-authored artifact or the user's own ruling; a driver's or an agent's confirmation, and
the absence of objection, are never waivers. The reachable block consumers cite is § Canonical Status State
Machine of `templates/feature-details-template.md`; `/speckit.review`, `/speckit.checklist` and
`shared/workflow/feature-integration.md` § Pre-Status-Flip Gate reference that block and do not restate it.

### GATE-4 (tasks stage)

For every `final`-path criterion, GATE-4 requires a `pass` status **and** a present smoke record — or an
explicit user waiver naming the criterion. The carrier is `templates/tasks-template.md`; the condition set is
this section's.

### The A13 boundary — three carriers, one fact each

Three tables look alike and judge different things. The same fact MUST live in exactly one of them, and the
others reference it (`see § …`), never copy it:

| Carrier | Judges |
|---------|--------|
| `plan.md` § Execution Premises | planning-time load-bearing premises and whether evidence supports them |
| `plan.md` § Inherited Blockers | records inherited from a dependency feature, and this feature's disposition of each |
| `tasks.md` § Environment Prerequisites | task-generation probe verdicts, each with its probe command and an ISO date |

A fact written in two of the three is a defect; the second occurrence MUST be converted into a pointer.

## Closure Verdict

### Binary, and only binary

`accept` or `block`. There is no third value, no severity scale and no advisory tier. The payload carries the
verdict, the reasons, the `final_path` counts and the feature class (`execution` / `expression`) — and nothing
else is a verdict.

### The three exit codes

| Exit | Meaning |
|------|---------|
| `0` | `accept` |
| `1` | `block` |
| `2` | an input is missing or unparsable |

A missing input is **never** reported as `block`: it is a defect of the artifact or of the invocation, not a
finding about the feature. In audit mode the exit code reflects input validity only — `0` whenever the inputs
parse, however many features the audit reports.

### `final_path` counts, computed once

`final_path = {pass, blocked, deferred, fail, unknown, total}` over the `final`-path criteria. The checker
computes these counts; no caller, template or report recomputes them — a report copies them. A second count is a
second source of truth, and the two drift.

### The seven reason templates

`block` MUST carry at least one reason drawn from this closed set. Five take an argument, two take none:

| Template | Argument |
|----------|----------|
| `zero-final-path-pass` | — |
| `final-path-not-pass: SC-NNN` | `SC-\d{3}` |
| `blocked-without-measurement-ladder: SC-NNN` | `SC-\d{3}` |
| `runtime-dependency-not-owned: RS-NNN` | `RS-\d{3}` |
| `falsified-premise-undecided: EP-NNN` | `EP-\d{3}` |
| `inherited-blocker-undisposed: <feature>:<row>` | `<feature>` = the dependency's feature id; `<row>` = that source row's locator as the dependency artifact writes it |
| `status-claims-implemented-but-blocked` | — |

**Template versus instance, and membership**: these seven are **templates**. An emitted reason is an
**instance** — `prefix + ": " + argument`, where the prefix is the template with its `: <placeholder>` suffix
removed, joined by exactly one `": "`, and the argument satisfies the grammar above. Membership is therefore a
mechanical **two-part test**: template match (byte-identical prefix) **and** a well-formed argument. A bare
prefix of an argument-taking template is not a member; no third spelling, trailing colon or re-spelled
placeholder is admitted. A reason outside the set, or an instance with a malformed argument, is a defect of the
checker — not a finding about the feature.

The set is **closed**: an eighth reason requires revising this file, never a local addition. A non-`pass`
`supporting`-path criterion produces no reason of its own; only `final`-path criteria can refuse a verdict. For
an `expression`-class feature the `final`-path rule is **vacuous** — the class is read from the declared flow
class, so the exemption is mechanical, and such a feature is never forced to invent a `final` criterion.

A declaring specification records the same seven templates in its own `## Shared Strings` so its tests can pin
them verbatim. That is a per-spec declaration for matching, not a second schema: this file is authoritative for
what a consumer emits.

### Input contract — the `Path` marker

Every success-criterion definition line carries `**Path**: final` or `**Path**: supporting`, written as the
**last token of the line, exactly once**. `final` = the criterion proves the feature's main user journey /
product flow works; `supporting` = auxiliary quality, hygiene, documentation or non-blocking evidence. An
`execution`-class feature MUST carry at least one `final`-path criterion; an `expression`-class feature is
exempt and MUST NOT be forced to invent one. A missing marker, a second `**Path**` on the same line, or a value
outside the two-value domain is a format violation reported with file and line — and a marker that cannot be
parsed makes the closure check an **input error** (exit `2`), never a `block`.

### When the judgement runs

At the **feature line's closure**. One line carries a feature's whole slice set, so the verdict runs once, when
that line closes — a `final`-path criterion is legitimately not `pass` in an early slice, and reading the
judgement as "every slice merge must pass it" would block the first merge by construction. Slice merges are
judged by the review gate. The three call sites — implement (before `Planned → Implemented`), review (before
`Implemented → Ready for Review`) and the driver's closure/merge step — share this one verdict, and no call site
may substitute a model judgement, a different script or an ad-hoc grep for it.

## Extension Points

Sections later slices add to **this** file. Each line names the owner its obligations have **today**, so that
nothing is undefined while the section is absent.

- `## Execution Premises` + `## Inherited Blockers` (**081b**) — the two tables' column sets, value domains and
  invalid-row rules. The carriers themselves are already named in § Gates above (the A13 boundary), so this
  extension adds the schema, not the boundary. Obligations these sections will carry are owned today by the
  declaring specification's functional requirements **FR-010** (execution premises) and **FR-011** (inherited
  blockers). In particular the `inherited` disposition's **carrier obligation** — an `inherited` row MUST name a
  runtime-reachable carrier, and that carrier MUST NOT be a deferrable `supporting`-path criterion — is owned by
  **FR-011** and is *not* left undefined by the absence of this section. The matching plan skeleton belongs to
  `templates/plan-template.md` and lands with the same slice; it carries the column sets only, never a value
  domain and never an invalid-row rule.
- `## Review Composition` (**081c**) — the process → artifact → implementation → code segments plus the
  Acceptance Reality Check, the expected-artifact denominator, and their boundaries.
- Additions to § Verification Vocabulary (**081d**) — the reconciliation of the four `blocked` literals (owner:
  the declaring specification's **FR-019**) and the closed status vocabulary of
  `templates/feature-index-template.md`, which today carries only a `Status` column header, so its obligation is
  to **add** a value domain rather than to insert one value into an existing list.
