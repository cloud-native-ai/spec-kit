Contract: Acceptance Readability — Status, Records and Tier Handoff

**Feature**: 092-non-disposable | **Contract file**: `contracts/acceptance-readability.contract.md`
**Guard carrier**: `tests/contract/test_non_disposable_contract.py` (one test per object named in C-801, each with a
mutation leg that breaks the object and asserts red)
**Owner**: the **registry status domain** (the values a feature row may take) is owned by
`shared/workflow/feature-integration.md` § Status State Machine; the **closure verdict and its reason codes** are
owned by `shared/workflow/acceptance-hardening.md` § Closure Verdict and realised by
`scripts/python/closure-acceptance-check.py` (`ARC_VERDICTS`, `REASON_CODES`); the **verification vocabulary and the
smoke fields** are owned by `shared/workflow/acceptance-hardening.md` § Verification Vocabulary; the **decision-tension
record shape** is owned by `shared/guidelines/decision-tension.md` and checked by
`scripts/python/validate-decision-tensions.py`; the **`**Path**:` marker** is owned by
`shared/workflow/acceptance-hardening.md` § Measurement Sources; the **handoff marker form and the Shift List** are
owned by `plan.md` § Shift List and § A–H Corpus Mapping. This file owns **one** thing the owners above do not: the
**contradiction table** between a registry status and a closure verdict, plus the obligation that the four objects
below are *read* rather than trusted. It restates no owner's value domain — it cites it.
**FR coverage**: each clause carries its own trailing citation group.

**Why a separate file.** `contracts/status-and-verification.contract.md` fixes how the engine **consumes** the
closure verdict. This file fixes what else a status claim is allowed to rest on, and it exists because a machine can
read four different objects on the "is this feature closed?" path — the registry row, the `verification.md`
machine-block, the `tasks.md` structure and the `plan.md` decision-tension records — and a defect in **any one** of
them shows up as `status-unreadable`. Before this file the check read one object, so three of the corpus rows
(A3, A4, A5) could not be judged at all.

- **C-801** — Three objects, then a fourth with its own clause

`status-unreadable` judges **three readable objects**, each with its own finding shape:

| # | Object | Read from | What makes it red |
|---|--------|-----------|-------------------|
| O1 | the registry row | `.specify/features.md` | the row's status contradicts the closure verdict per **C-802** |
| O2 | the verification machine-block | `<spec-dir>/verification.md` | a per-criterion machine-readable block or a smoke field is absent (**C-203**) |
| O3 | the tasks structure **and** the decision-tension structure | `<spec-dir>/tasks.md`, `<spec-dir>/plan.md` | a user-story label sits in a phase that is not a story phase, or a decision-tension record does not carry the owner's six-field form |

O3 is one object with two surfaces because both answer the same question — "does this feature's own record shape
match the shape its owner requires" — and both are read from the spec's own files. A red on either surface yields a
`status-unreadable` entry naming the file, the line and the **missing or malformed structure element**.

`requirements.md` is **not** a fourth object of this class. Its `**Path**:` markers are a requirements-side
measurement obligation, and C-804 gives that one its own clause instead of folding it in here — a single clause whose
predicate silently spanned every spec file would be the "semantic hit dressed as deterministic" failure
`requirements.md` § Edge Cases names.

(FR-025, FR-026, FR-027, FR-030)

- **C-802** — The status × verdict contradiction table (closed)

The engine MUST read the registry status domain from its owner (`templates/feature-details-template.md` § Canonical
Status State Machine, which declares the carrier and names `shared/workflow/acceptance-hardening.md` § Feature Status
as the schema owner) and the closure verdict domain from `closure-acceptance-check.py` (`ARC_VERDICTS`), and MUST
report a **contradiction** exactly for the cells marked ✗ below. The table is closed: a pair not listed is **not** a
contradiction, and the engine MUST NOT invent a further reading (for example "status looks stale").

| Registry status ↓ / closure verdict → | `accept` | `block` |
|---|---|---|
| `Draft` | **✗ contradiction** — a feature still in draft is not closed | agree |
| `Planned` | **✗ contradiction** (corpus A3: `090` reads `Planned`, closure is `accept`) | agree — a planned feature may legitimately be blocked |
| `Implemented` | agree | **✗ contradiction** — reason code `status-claims-implemented-but-blocked` |
| `Ready for Review` | agree | **✗ contradiction** — reason code `status-claims-implemented-but-blocked` |
| `Blocked` | **✗ contradiction** — the registry records a blocker the checker does not see | agree, and green |
| `Completed` | agree | **✗ contradiction** — a completed feature whose closure is `block` |
| `Relocated` | **not a live row** — excluded by name, `count: 0` with its reason recorded | same |

`Relocated` is the one excluded row and it is excluded by a **named** rule rather than by silence: a relocated row
carries no live spec directory of its own, so there is no closure verdict to compare it against, and the engine MUST
report `count: 0` for that status **with** the reason — never fold it into the agree column. `Relocated` is real, not
hypothetical: **one** row in `.specify/features.md` carries it today, which is why the exclusion needs a rule
rather than a passing mention.

**Reason-code assignment.** The closure engine owns exactly one status-related code,
`status-claims-implemented-but-blocked`, and it is emitted **only** for the two cells whose status is a *completion
claim* (`Implemented`, `Ready for Review`). The other ✗ cells (`Draft`, `Planned`, `Blocked`, `Completed`) have no code
in the closure set and MUST NOT be given an invented one: the engine emits them with an **empty** `reasons` list and
carries the two readings (registry row, checker call identity) in the entry's own `evidence_refs`. Minting a second
code for them is forbidden by C-205 — a status reading that needs a new vocabulary word has found an owner-page
question, not an engine string.

**Three prohibitions.**

- The engine MUST NOT compare a status whose spelling is absent from the owner's domain. An unknown spelling is an
  **input error** (exit `2`, naming the row), never a silent "agree" — a value that agrees because nobody recognises
  it is the failure corpus A1 was.
- The engine MUST NOT treat `Completed` or `Relocated` as "out of scope" beyond the one named exclusion above; a
  completed row with a `block` verdict is exactly the "closed twice" contradiction this class exists to report.
- The engine MUST NOT read a third verdict value. If the checker's `ARC_VERDICTS` grows, this table stops being
  decidable and the guard MUST fail rather than guess, until this clause is revised against the owner.

(FR-026, FR-028, SC-008)

- **C-803** — Every cell of the table has a corpus row or a named construction leg

The guard MUST prove C-802's table cell by cell. Existing corpus rows cover `Planned × accept` (A3),
`Implemented × block` (A1) and `Ready for Review × block` (the same A1 family); the remaining cells
(`Draft × accept`, `Blocked × accept`, `Completed × block`, and the `agree` cells) are proven on a **fixture tree** stated in the
guard's own data, so the missing corpus coverage stays visible to the next reader rather than being read as complete.

**Which side of the table the corpus sits on matters.** A cell is proven by a clash only when the artifact disagrees
with the *truth*; a corpus row that is genuinely consistent must land **green**, and forcing it red is a false
positive, not coverage. So the guard carries two fixture families and keeps them apart:

- a **clash fixture** — the artifact says `Planned` while the truth is closed — MUST land red on that cell;
- a **consistent fixture** — the artifact says `Planned` and the truth is also open, or says `Implemented` and the
  truth is closed — MUST land green, and a guard that reports it is the defect.

A3's corpus row is the load-bearing one: `090-re-anchoring`'s registry row reads `Planned` while
`closure-acceptance-check.py --json` returns `accept` with 4/4 `final`-path criteria passing. Before C-802 the engine
had no reading for that pair and A3 could only be described, never judged. The guard MUST include the reading that
A3 lands **red**, not merely the reading that it is "status-inconsistent".

(FR-026, SC-008)

- **C-804** — `requirements.md`'s `**Path**:` markers are a requirements-side mark, judged by their own reading

A `requirements.md` success-criterion row that carries no `**Path**:` marker (corpus A6,
`080-humanize-run-output`, the 080 requirements face) MUST be reported by the requirements-side reading the repository already owns —
`scripts/python/validate-requirements.py`'s `path-marker` check — and **not** by `status-unreadable`.

Two consequences, both obligations:

- The engine's report MUST carry the requirements-side reading as an **evidence ref** on any entry that would
  otherwise be read as "the spec's status is unreadable because its requirements file is malformed". One defect, one
  class.
- The guard MUST NOT assert A6 against `status-unreadable`. A6's expected reading is `validate-requirements.py`
  red on `path-marker`; asserting it against the status class would make the status class a catch-all and destroy
  the discrimination C-801 was written to create.

(FR-025, FR-030)

- **C-805** — The 档 II handoff marker: form, guard carrier, and the count it is counted under

The 档 II handoff is a **deliverable, not a deferral** (FR-056). It is a marker line, placed in the receiving body at
the defect's location:

```text
<!-- 092 handoff: <corpus id> → <receiving feature> -->
```

Obligations, each decidable:

- **Form.** Exactly one such line per receiving body; the corpus id MUST be one of the 档 II ids, and the receiving
  feature MUST be the one `plan.md` § Shift List names. Zero markers, two markers on one body, an id outside the 档 II
  set, or a receiving feature that disagrees with the Shift List are findings.
- **Guard carrier.** The form's single owner is `plan.md` § Shift List (C-805 names the obligations; the marker's
  literal shape is stated there). The guard asserts the form by reading that owner's statement, never by carrying a
  second literal copy of it.
- **Counting.** The marker count equals the **distinct receiving-body count**, which equals the Shift List's row
  count. Those three numbers travel together and must be equal: the **12** Shift List rows, the **12** receiving
  bodies they resolve to, and the **12** markers. The **15** 档 II corpus entries and the **19** 档 I entries count a
  *different* object — corpus entries, not receiving bodies. All three are fixed once, in `plan.md` § Shift List's
  own count table, so that a later reader does not "fix" one of them to match another.

  The three are neither the same pool nor a partition of one another: the **19** 档 I entries are closed in place by
  this feature and land **no marker at all** (DoD-4 names them), while the **15** 档 II entries reach only **12**
  bodies because the mapping is many-to-one at the row: `081` carries D1 + D2, `084` carries D3 + E5, `090` carries
  D5 + F2, `083` carries E1 + E2 + E3 + F5, and the dated-bodies row carries F1 + F3 — five rows holding twelve
  entries between them, the other seven rows holding one apiece. The marker count is the **row** count, so the
  arithmetic to refuse is "15 entries, therefore 15 markers": that lands three duplicate markers on three bodies.
  A count that moves without its own reason is a finding, not a tidy-up.
- **Which surface lands the marker.** Each 档 II receiving body is a file **outside** this feature's directory. The
  driver MUST decide, at the moment the Shift List is authored, between two readings — either the marker is landed in
  the receiving body by this feature's P7 (a cross-line write, whose permission is then recorded by narrowing the
  team's `forbidden` list to the marker lines), or the marker's landing is recorded in that body's **own** line. That
  choice is a decision, not a correction; this clause records that it MUST be taken and where it is recorded
  (`team/092-non-disposable/team.md` § Handoff boundary), so the obligation is not left to implement time.

(FR-056, FR-057, FR-063, SC-020)

- **C-806** — FRs whose obligations are process-grade say so

The three FRs whose obligations are carried by the **process** rather than by a machine-readable object — FR-046 (the
semantic face on the 085 team), and FR-050 / FR-051 (the concurrency ceiling and the team-creation timing) — are
declared **process-grade** here: no engine class judges them, and their reading is the plan's own record (execution
premise EP-005) plus SC-020's measurement source.

FR-057 is **not** in this set: the per-entry tier assignment is checkable against a structure, the marker form C-805
fixes, so its carrier is C-805 and not a process declaration. The distinction is the point of this clause — a
process-grade declaration is for an obligation with no readable object, and using it for one that has a readable
object would hide a machine check behind a prose note.

This clause exists so that "no clause cites FR-046/050/051" becomes a **recorded disposition** instead of an
unreachable lane. The FR lane of `account-clause-coverage.py` is closed for these three by this declaration, never by
a silent absence.

(FR-046, FR-050, FR-051)

- **C-807** — The owner-page landing obligations are cited where they land

FR-063 (the seven-face landing), FR-064 (its four connected obligations) and FR-065 (a future constitution revision)
are landed by **C-101** (the owner page is the one rule owner and declares what it owns) and by this clause: the seven
faces and the four connected obligations are `plan.md` § Landing Checklist's subject, and FR-065 is `T-002`'s deferred
question. The clause states the pointer so the three FRs have a citation group naming them; it does **not** restate
the seven faces.

(FR-063, FR-064, FR-065)
