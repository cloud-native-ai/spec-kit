# Acceptance Hardening — Feature Status, Verification Vocabulary, Gates and Closure Verdict

**Owner (single definition point)**: this file, `shared/workflow/acceptance-hardening.md`, owns the schemas that
make "may this feature be called `Implemented`?" a deterministic question: the feature-status value `Blocked`
and its four transitions, the verification vocabulary and its measurement ladder, the gate conditions that read
them, the closure verdict with its closed reason set, exit codes and `final_path` counts, and the three artifact
schemas that say **what a feature must own and what it must have inherited** — the runtime-stack table, the
execution-premises table and the inherited-blockers table. Every other surface — template, command, skill, driver
doc — reaches these by path plus `§ section anchor`, and **none restates** a table, a value domain, a threshold or
a reason literal.

**Declared carriers (projections, never second owners)**: `templates/feature-details-template.md` § Canonical
Status State Machine, `templates/verification-log-template.md`, `templates/tasks-template.md` (§ GATE-4) and
`templates/plan-template.md` (the two plan-table skeletons, which carry **column names only**) physically hold what
this file defines, because a consumer that is editing a template must find the rules where it is editing. A carrier
is a **declared projection**: it may not widen a value domain, and where a carrier and this file disagree, this file
wins and the carrier is stale. The four carriers are also the exemption list of the schema-uniqueness guard
(`requirements.md` SC-009 ④), and each carries its own narrowing assertion — the plan skeleton, in particular, may
repeat a column set and **zero** domain literals.

**Scope of this revision**: § Feature Status · § Verification Vocabulary · § Gates · § Closure Verdict ·
§ Runtime Stack & Dependency Ownership · § Execution Premises · § Inherited Blockers. Sections belonging to later
slices are listed in § Extension Points, together with the owner their obligations currently have. Nothing here is
inferred from a slice that has not landed.

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

`final_path = {pass, blocked, deferred, partial, fail, unknown, total}` over the `final`-path
criteria — six status buckets plus the total, and the record is **closed**: a seventh bucket requires
revising this section, never a local addition. Two of the six are easy to confuse and are therefore
distinguished here once:

| Bucket | Meaning |
|--------|---------|
| `unknown` | **no status row exists** for the criterion. A missing measurement is not evidence of anything, least of all of a pass. |
| `partial` | the row **exists and was measured** as `partial`. It is a measurement, not a gap — the same status the verification vocabulary admits, counted rather than reinterpreted. |

The checker computes these counts; no caller, template or report recomputes them — a report copies
them. A second count is a second source of truth, and the two drift.

### The seven reason templates

`block` MUST carry at least one reason drawn from this closed set. Five take an argument, two take none:

| Template | Argument |
|----------|----------|
| `zero-final-path-pass` | — |
| `final-path-not-pass: SC-NNN` | `SC-\d{3}` |
| `blocked-without-measurement-ladder: SC-NNN` | `SC-\d{3}` |
| `runtime-dependency-not-owned: RS-NNN` | `RS-\d{3}`, or the reserved literal `runtime-stack` for a section with zero data rows |
| `falsified-premise-undecided: EP-NNN` | `EP-\d{3}` |
| `inherited-blocker-undisposed: <feature>:<row>` | `<feature>` = the dependency's feature id; `<row>` = that source row's locator as the dependency artifact writes it |
| `status-claims-implemented-but-blocked` | — |

**Template versus instance, and membership**: these seven are **templates**. An emitted reason is an
**instance** — `prefix + ": " + argument`, where the prefix is the template with its `: <placeholder>` suffix
removed, joined by exactly one `": "`, and the argument satisfies the grammar above. Membership is therefore a
mechanical **two-part test**: template match (byte-identical prefix) **and** a well-formed argument. A bare
prefix of an argument-taking template is not a member; no third spelling, trailing colon or re-spelled
placeholder is admitted. One argument slot is a **reserved literal** rather than an id: the runtime-row class has a
shape with no `RS-NNN` to name — the section exists but carries **zero data rows** — and that shape's instance is
`runtime-dependency-not-owned: runtime-stack`. Emitting nothing there is the false green the finding exists to
catch, and a fabricated `RS-NNN` would be worse than silence: it points at a row nobody wrote. A reason outside the set, or an instance with a malformed argument, is a defect of the
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

## Runtime Stack & Dependency Ownership

The requirements-side table that answers "is the runtime this feature stands on inside the feature's own
acceptance boundary?" Mandatory in `requirements.md` of an `execution`-class feature. The columns are fixed and are
read **by column name** — never recovered from another cell's prose:

| Column | Content |
|--------|---------|
| `ID` | `RS-\d{3}`, dense and unique |
| `Capability` | one runtime capability the feature consumes or delivers |
| `Form` | the closed domain below |
| `Owner` | who provides it |
| `Pin` | version / digest / commit — measured, never invented; required for `signed-contract` |
| `Contract` | repo-relative path of the file the contract actually lives in; required for `signed-contract`, and it MUST resolve in the checkout |
| `Joint acceptance` | a named owner or a command; required for `signed-contract` and for `in-scope` |
| `FR` | the `FR-NNN` list that delivers the capability; required for `in-scope` |
| `Premises` | the `EP-NNN` ids the row's FRs depend on, `, `-separated; each MUST exist in `plan.md` § Execution Premises and obey § Execution Premises below |

`Contract` and `Premises` are **their own cells**, and that is load-bearing rather than cosmetic: a contract path
living inside `Owner` prose gave the contract-path check nothing to read, and a premise id with no cell of its own
made "every runtime-dependent FR cites a premise" uncheckable.

### The `Form` domain

`in-scope` · `signed-contract` · `user-waived` — closed. An `expression`-class feature MAY record `not-required`
with a stated reason; on an `execution`-class feature `not-required` is a defective cell.

`in-scope` means **this feature delivers the capability**. A capability supplied externally and merely consumed
here MUST be `signed-contract` (or `user-waived`) — recording it `in-scope` only renames the outsourcing.

`signed-contract` MUST carry a `Contract` cell that resolves, a measured `Pin`, an external `Owner` and a named
joint-acceptance owner or command. `user-waived` MUST cite the user ruling and state the residual risk.

### The three `in-scope` duties, each judged where its carrier is readable

| Duty | Obligation | Judged at | Failure class |
|------|-----------|-----------|---------------|
| ① | the `FR` cell is non-empty and resolves to an FR defined in **this** spec | requirements | **input error** (exit `2`) — a defective cell is a fact about the artifact, never a `block` about the feature |
| ② | at least one `tasks.md` row quotes that FR, by a **line-level** match `^- \[.\] T\d{3}.*\bFR-0NN\b` — an FR named in a table cell or in prose is not a task row | tasks | `runtime-dependency-not-owned: RS-NNN` |
| ③ | `verification.md` carries a joint-acceptance row naming that `RS-NNN` | closure | `runtime-dependency-not-owned: RS-NNN` |

A stage that cannot see the carrier artifact MUST NOT report the duty as satisfied. Duties ② and ③ share their
reason with the prose-only case below, because they are the same conclusion about the same artifact — the
capability is claimed and nothing owns it. No reason is coined for them.

### Three shapes, three verdicts — silence is not one of them

| Shape | Verdict |
|-------|---------|
| the section is absent | **input error** (exit `2`) — the artifact is incomplete |
| the section is present with **zero data rows** | `runtime-dependency-not-owned: runtime-stack` — the reserved argument (§ Closure Verdict), because this shape has no `RS-NNN` to name |
| a data row with a required-but-empty cell | `runtime-dependency-not-owned: RS-NNN` |

Zero data rows is the most complete form of "no table row" and MUST NOT be read as "this feature has no runtime
dependency". Emitting nothing there is the false green this class exists to remove, and a fabricated `RS-NNN` would
be worse than silence: it points at a row nobody wrote.

**Cell-shape defects are input errors, existence and acceptability defects are reasons.** A `Form` value outside
the domain, `not-required` on an `execution` feature, a `Premises` id with no matching premise row, and a
`Contract` path that does not resolve all exit `2`; a missing `RS` obligation, an unsupported waiver, and a
`user-waived` row whose residual-risk cell is empty are `runtime-dependency-not-owned: RS-NNN`. The split is not
re-decided per caller.

### The prose-declaration rule — mechanical, code blocks excluded

"Prose only" is decidable rather than a reading. Inside the section, fenced code blocks (backtick and tilde
fences) and heading lines are removed first; a remaining line shaped

```text
- **Runtime dependency**: <capability> — <owner>
```

is a **prose declaration**: carrying an `RS-NNN` it yields `runtime-dependency-not-owned: RS-NNN`, carrying none it
is an input error naming that line. A narrative line **without** the marker — for example an explanatory paragraph
that mentions `RS-004` — is not a declaration and MUST NOT fire. The marker is the rule; without it "prose" would
be a judgement, and the obligation would only bite on examples written to be caught.

## Execution Premises

The plan-side table that records what the plan **assumes at planning time** and whether evidence supports it.
Mandatory in `plan.md` of an `execution`-class feature.

| Column | Content |
|--------|---------|
| `ID` | `EP-\d{3}`, dense and unique |
| `Premise` | one load-bearing assumption the plan rests on |
| `Evidence` | a path, a command, or a measurement — citable |
| `Status` | the closed domain below |
| `Decision` | the closed domain below |

### `Status` — closed over three values

`verified` · `unverified` · `falsified`.

### `Decision` — required whenever `Status` is `falsified`

`resolve-in-scope` · `fallback` · `user-waiver`, closed. A `falsified` premise whose `Decision` cell is empty or
absent is `falsified-premise-undecided: EP-NNN` (§ Closure Verdict): the premise is a known-bad fact and nobody has
said what happens about it. A `Decision` value outside the domain is a defective cell.

### Two duties

1. **Every FR that consumes a runtime capability cites a premise id**, and the carrier is the `Premises` cell of
   the runtime-stack row naming that FR (§ Runtime Stack & Dependency Ownership) — not a prose sentence in the
   plan. A cell naming an absent id is a defective cell (exit `2`); a cited premise that is `falsified` with no
   `Decision` is `falsified-premise-undecided: EP-NNN`. When one FR appears in several rows, every one of those
   rows carries the id.
2. **A known negative conclusion is a `falsified` premise with a `Decision`**, never an "out-of-scope P2/P3" line.
   Parking it is the same defect as not recording it: the fact stays known, and the feature keeps standing on it
   while the document says it does not.

Boundary (A13): planning-time premises only. § Gates § The A13 boundary owns the split between this table, the
inherited-blockers table and `tasks.md` § Environment Prerequisites; this section does not restate it.

## Inherited Blockers

The plan-side table that records what a **dependency** feature already measured, and this feature's disposition of
each record. Mandatory in `plan.md` of an `execution`-class feature. Columns, read by name:

| Column | Content |
|--------|---------|
| `#` | the row's ordinal in this table — bookkeeping only, never a join key |
| `Source row` | the extracted dependency record's locator — the join key, spelled below |
| `Disposition` | the closed domain below |
| `Carrier` | required when `Disposition` is `inherited`; one of the two forms below |
| `Carrier slice` | `this-slice` or a later slice id — see below |
| `Evidence / note` | a path plus one line, or the one-line reason the disposition holds |

### The dependency set is declared, never implied

The plan states which dependencies it read, and for each one the basis on which it is included or excluded. An
implied set is unreadable: nobody can tell whether a row is missing or a dependency was never opened.

**The declaration's marker is fixed, because both the gate and the closure checker read it mechanically.** A plan
with dependencies carries a paragraph whose first token is the literal
`**Dependency artifacts (declared, never implied)**`, followed by one bullet per dependency; each bullet names that
dependency's artifacts in backticks (its feature detail and its `verification.md`), as repo-relative paths or paths
relative to the spec directory:

```text
**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:
- `071`: `.specify/memory/features/071.md`, `.specify/specs/071-review-code-integration/verification.md`
```

Only backticked `.md` paths **inside this block** are read; a backticked `.md` token elsewhere in the section (this
spec's own `verification.md`, a research note) is never a dependency. A plan with no dependencies writes the exact
sentence `Dependency set: none`. Any other dependency-set sentence without the block is an **input error**: an
absent declaration MUST NOT silently disable the fourth finding.

### The extraction set — closed at three sources

Each dependency yields rows from exactly three places and from nowhere else:

| Source | Row |
|--------|-----|
| the dependency's detail, its `## Deferred` section | one row per non-empty list item |
| the dependency's `verification.md` | one row per status row in `blocked` · `deferred` · **`partial`** |
| the dependency's `verification.md` | one row for a **non-empty** `deferred_tasks=` list — an empty value yields no row |

`partial` is inside the set: a dependency may carry `partial` rows and nothing else, and an extraction set that
excludes it is disjoint from the disposition set, which makes the finding unreachable.

### The row locator, and the join key

`Source row` = `<feature-id>:<row-locator>`, no whitespace. `<feature-id>` is the dependency's feature id
(`\d{3}`); `<row-locator>` is exactly one of:

| Form | Written for |
|------|-------------|
| `SC-\d{3}_status` | a `verification.md` status row — e.g. `071:SC-006_status` |
| `deferred_tasks` | a non-empty `deferred_tasks=` list — e.g. `077:deferred_tasks` |
| `deferred:<slug>` | a `## Deferred` list item; `<slug>` = `[a-z0-9][a-z0-9-]*`, the item's label lowercased with whitespace collapsed to `-`, else `row-<n>` by 1-based position inside the section |

`Source row` **is the join key**: every disposition row reproduces the extracted locator verbatim, and a locator
disposed twice is a defective cell (two dispositions for one key). An extracted row with no disposition row of its
own is an undisposed row.

A disposition row that disposes **nothing** — normally `not-applicable` with no extracted record behind it — writes
`—` (or the legacy `(none)`) in `Source row`. That sentinel is not a locator and is never joined; any other value
MUST satisfy the grammar above.

### `Disposition` — closed over three values, and what each one owes

| Disposition | Obligation |
|-------------|-----------|
| `resolved` | the blocker is gone, with re-checkable evidence — a command and its output, or the row's measured value |
| `inherited` | this feature takes the measurement over, and MUST name a runtime-reachable **carrier** (below) |
| `not-applicable` | the thing measured does not apply to this feature, with the reason |

### The `inherited` carrier

`Carrier` is exactly one of two forms, no whitespace:

| Form | Parts |
|------|-------|
| `task:<T-ID>+test:<repo-relative test path>` | **conjunctive**: `<T-ID>` = `T\d{3}` and MUST be a mandatory row of this slice's `tasks.md`, and the test path MUST appear verbatim in that row's description. One part alone is not this form |
| `gate:<GATE-ID>` | `<GATE-ID>` = `GATE-[0-9]+` and MUST be one of this slice's completion gates |

**Eligibility**: a carrier MUST be a `final`-path criterion, a mandatory task row of the same slice, or a mandatory
gate. It MUST NOT be a deferrable `supporting`-path criterion — a thing that may be `deferred` cannot carry an
inherited measurement.

**`Carrier slice`** is `this-slice` or a later slice id (`081c`, `081d`, …). `this-slice` requires both limbs
above to hold in this judgement. A later slice id is legal **only** while the parent feature's claimed status is
`Blocked` and that slice is listed in the plan's § D10 slice table; the row then reads **`inherited-later`**. Any
other value is a defective cell.

### `inherited-later` — a fourth *reading*, never a fourth disposition

The disposition cell stays three-valued. `inherited-later` is derived from `Carrier slice` plus the parent's
claimed status, and it means **disclosed, neither blocking nor resolved**: it is counted separately from resolved
carriers and MUST NOT be counted as undisposed. In such a row `Carrier` is `test:<repo-relative test path>`
**alone** — the task id belongs to a `tasks.md` that does not exist yet, and writing one would be a fabricated id.
`Carrier slice` supplies the slice. The row is re-read at that slice's closure, where the carrier MUST be completed
to `task:<T-ID>+test:<path>` and resolve; an incomplete carrier there is an undisposed row **in that slice**, under
the same reason.

### One reason for five ways to fail

An undisposed row, an `inherited` row with no `Carrier`, a `Carrier` that does not parse as one of the two forms, a
`Carrier` that does not resolve, and a `Carrier` pointing at a deferrable `supporting`-path criterion are judged
**the same**, under `inherited-blocker-undisposed: <feature>:<row>`. The closed reason set does not grow for any of
them. A later-slice `Carrier slice` is not in that class — that is `inherited-later`, above.

Boundary (A13): dependency-inherited records only. § Gates § The A13 boundary owns the split between this table,
the plan's premises and `tasks.md` § Environment Prerequisites; this section does not restate it.

## Extension Points

Sections later slices add to **this** file. Each line names the owner its obligations have **today**, so that
nothing is undefined while the section is absent.

- `## Review Composition` (**081c**) — the process → artifact → implementation → code segments plus the
  Acceptance Reality Check, the expected-artifact denominator, and their boundaries.
- Additions to § Verification Vocabulary (**081d**) — the reconciliation of the four `blocked` literals (owner:
  the declaring specification's **FR-019**) and the closed status vocabulary of
  `templates/feature-index-template.md`, which today carries only a `Status` column header, so its obligation is
  to **add** a value domain rather than to insert one value into an existing list.
