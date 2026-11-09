# Analyze Repair Round 1 — disposition record (2026-11-09)

Input: `analyze-round1-findings.md` (base `1e49534a`; 1 CRITICAL / 4 HIGH / 13 MEDIUM / 4 LOW + 2 feature-linkage).
Scope honoured: edits touched only `.specify/specs/091-auto-git-closeout/**` and `.specify/memory/features*`. No
framework source, skill, template, test or runtime file was modified. No push.

Gate readings for this round: `analyze-repair-gates.txt` (same directory).

## 1. Blocking findings — all five resolved

### C-01 (CRITICAL) — FR-020/021/022/027 had no discharging clause. RESOLVED.

Root cause confirmed mechanically rather than by reading: `account-clause-coverage.py` reads a clause's **last
FR-containing parenthetical** as its citation group; a clause that merely mentions an id in prose cites nothing. The
four FRs therefore reached the accountant's uncovered list, and the four `feature-ref.md` map rows pointed at clauses
whose subject was something else (a lifecycle position, a delivery row) — the map was the sole evidence, so it was
asserting a discharge that did not exist.

| FR | New/changed clause | What the clause now asserts |
|----|--------------------|-----------------------------|
| FR-027 | `closeout-executor.contract.md` C-1 | the five non-goals as an **owned negative assertion table** — each row names the thing whose absence the guard asserts |
| FR-020 | `closeout-lifecycle.contract.md` **C-8** (new) | one step, reached by pointer from a closed named set of mechanisms; no second implementation; and the driver's authority is not widened by the pointer |
| FR-021 | `closeout-lifecycle.contract.md` **C-9** (new) | compiled faces are rendered by the registry, never authored; no order collision |
| FR-022 | `closeout-lifecycle.contract.md` **C-10** (new) + `closeout-verification.contract.md` **C-7** (new) | pointer, not rules; default no-edit decided by measurement |

Measured before → after: `FR claimed 24/28, FR uncovered 4` → **`FR claimed 28/28, FR uncovered 0`**. Clause count
26 → 32. The FR→contract map in `feature-ref.md` was rewritten row by row against the new citation groups (M-08 folded
in), and the `tasks.md` § "FR lane note" that had adjudicated the gap as a "citation-form gap, not missing work" was
**superseded and marked superseded** — analyze round 1 rejected that reading and the rejection stands.

### H-01 (HIGH) — C-2/C-6 guard scope vs T008/T013/T014. RESOLVED.

`closeout-declaration.contract.md` C-2 now states that the prohibition is a proposition about **the managed block's
contents, on both surfaces** (the shipped template asset and this project's instance), and that a guard reading one
file leaves the other free. It also fixes the baseline question the finding implied: pre-existing instance rows are not
retroactively a defect because C-6's companion assertion compares against the pre-change snapshot. T013 was rewritten
to be parameterised over **both** paths; its green tag was corrected to C-2 (it had been mis-paired with C-3, which is
the `ask`-default clause — T057 owns that).

### H-02 (HIGH) — the strongest authorization value was settled by a placeholder edit. RESOLVED.

The strength now lives in a **runnable transition**, `closeout-executor.contract.md` **C-8**: a four-row table mapping
each declared value to its authorized action set and its terminal state, exercised by the guard per value. T021 was
reframed to author only the `ask` presentation duty and to reach C-8 **by pointer**; a new row **T061** authors the
transition. The value→authority mapping now has exactly one carrier (C-8); declaration C-7 keeps "which value is the
strongest" and points at it, so the two do not hold competing wordings. The US1/US3 fixtures that previously bypassed
`format` via `ask` are covered by C-8's `ask` row: `derived → presented`, nothing executed.

### H-03 (HIGH) — a per-record hash demanded against a single `commit` field. RESOLVED.

`data-model.md` E-4's `commit` moved **into `covered[]`** as a per-row field, and the arity was fixed in the owning
clause: `closeout-lifecycle.contract.md` C-2 now states one run produces **exactly one** records commit. The invariant
a guard asserts is therefore **all `commit` values within one receipt are equal** (new rule **V-15**), never the
field's arity. Why per-row rather than one head-level field: it keeps a future "a class settled in a later commit"
expressible without a schema change and makes the receipt self-describing row by row. Recorded as a **refinement of
T-001**, not a new tension — T-001's two poles and its discriminating evidence are untouched; only the field shape was
under-specified.

### H-04 (HIGH) — C-4/C-5 collapsed distinct states. RESOLVED.

The declaration page now separates the axes explicitly. C-4 owns the **remote axis**: an *empty* and an *absent*
`Closeout remotes` are one outcome ("no pushable remote") with the two reasons distinguished in the report. C-5 owns
the **model axis** and says so: a declared model with no pushable remote is **not** "workflow not declared" — it
degrades the push step only, and the merge still runs. `ask` is named as a third independent axis that does not move a
project between rows. `data-model.md` closes the state set accordingly (see M-04).

## 2. Medium findings

| ID | Disposition | Where |
|----|-------------|-------|
| M-01 | **RESOLVED** — the invalid identifier is gone; verification C-1 now cites the form owner by path and its own form name | `contracts/closeout-verification.contract.md` C-1 |
| M-02 | **RESOLVED** — "no subprocess" now scopes only the structural arm; the boundary sentence says a structural predicate may not shell out while a behavioural one must | verification C-1 |
| M-03 | **RESOLVED** — the substitution token is pinned to the literal `<remote>`, and the guard asserts on the token, not on a description of it | executor C-7 |
| M-04 | **RESOLVED** — the terminal-state set is now a declared closed set of **five** with a table naming which edge cases land where; `degraded` is a named state rather than an unowned edge case | `data-model.md` § State transitions |
| M-05 | **RESOLVED** — the contradiction is settled on one outcome with two distinguished reasons (empty vs absent), not two behaviours | declaration C-4 |
| M-06 | **RESOLVED** — the per-value effect table exists as the value→authority transition (one carrier, reached by pointer) | executor C-8 |
| M-07 | **RESOLVED** — the receipt home is now decidable by its **parent** (already owned by `record-retention.py` as a holding root), plus a measured statement that the parent's current population `plans/`-only is a fact about today, not about ownership | `data-model.md` E-4, `tasks.md` A-G1 |
| M-08 | **RESOLVED** — the whole FR→contract map was re-derived against citation groups and is machine-checked (`.specify/scripts/python/account-clause-coverage.py --spec-dir`) instead of read | `feature-ref.md` § FR → contract map |
| M-09 | **RESOLVED** — the fixture roster has one carrier (E-6); the SC→measurement map points at it and no longer repeats it | `data-model.md` header, `feature-ref.md` § SC map |
| M-10 | **RESOLVED** — `## Status Tracking` added with this feature's criteria, pointing at the template as the state-machine owner and restating no transition | `.specify/memory/features/091.md` |
| M-11 | **RESOLVED** — the stage record now carries tasks / checklist / analyze / analyze-repair; the `Last Updated` cell in `features.md` carries the same chain | `features/091.md`, `features.md` |

## 3. Low findings

| ID | Disposition |
|----|-------------|
| L-01 | **RESOLVED** — the "only read-only remote" edge case now states its reachability condition (only when the model is declared) and states why it cannot collide with the undeclared-model degradation: different report text, mutually exclusive preconditions. |
| L-02 / L-03 / L-04 | **RESOLVED IN PASSING** where the containing clause was rewritten (the C-3→T013 pairing was the L-03-class ID nit and is fixed; the receipt-directory naming was settled in M-07). No remaining residual. |

## 4. Checklist fail items folded into the repair (R-9 … R-13)

Dispositions named in the brief: CHK009 / CHK011 / CHK016 / CHK020 / CHK023 / CHK036 / CHK038 / CHK040 / CHK045 / CHK046
still valid; CHK010 / CHK012 / CHK017 / CHK021 / CHK028 partial.

- **R-9 (CHK010, FR-008 machine form)** → **RESOLVED**: two decidable halves (locate the replaced assertion; old
  assertion absent from every written surface), both file reads. Landed as lifecycle C-7.
- **R-10 (CHK012 / CHK017, two readings)** → **RESOLVED**: the "other line's file" criterion is the run's own output
  set, not tree cleanliness nor git-untracked state (A23); the `--force` / `--force-with-lease` reading is fixed to
  reading (b) and the reason the other reading makes FR-012 vacuous is written down (A24).
- **R-11 (CHK036, RS-001 capability set)** → **RESOLVED**: the `Pin` column now carries the four-command capability
  set with an explicit statement that a version-string comparison is not a substitute (A25).
- **R-12 (CHK023, A20 pointer from SC-004)** → **RESOLVED**: SC-004 now carries the prohibition in its own body
  ("MUST NOT re-assert the total constant — see A20"), so an implementer reading only SC-004 cannot write a second
  constant without violating the criterion.
- **R-13 (CHK046, Readers / Reading scenario)** → **RESOLVED**: both header lines added, reader baseline referenced
  rather than re-invented. `doc-consistency-check.py --faces reader --path .../requirements.md` → `reader=pass`,
  0 findings (it was `reader-declaration-missing` before).
- **CHK009** → **RESOLVED** via A26 + lifecycle C-2/C-3: the record membership is owned by the receipt's `covered[]`,
  defined once, referenced elsewhere.
- **CHK011 / CHK016 / CHK020 / CHK021 / CHK023 / CHK028 / CHK038 / CHK040 / CHK045** → their owner-text fixes ride
  the clauses above (declaration C-4/C-5 for CHK020's "shared delivery root", lifecycle C-5 for CHK012's criterion,
  verification C-6 for the closed-set rule, `data-model.md` V-15/V-16/V-17 for the value and axis rules).

**Residual check items, stated rather than dropped.** CHK011, CHK016, CHK038, CHK040 and CHK045 were *checked against*
this repair but their dispositions live in the analyze round-2 pass: they ask whether the requirements-quality
checklist items are now answerable, and that judgement is round 2's, not this slice's. None is silently closed; the
checklist file itself is untouched so its `fail` marks remain as round 2's input.

## 5. Disclosed new residue created by this repair

- **`tasks.md` grew from 60 to 62 rows** (T061, T062) and its green partition from 26 to 32 claims. Two
  `green-cross-phase` warnings are now visible (one predated the round); both are disclosed in § Green Partition with
  the reason the alternative is worse. The `green-path-divergence` count rose 45 → 69 for the same reason (quadratic in
  claims per path), adjudicated in the same section.
- **`pre-analyze-check.py` advisories rose 46 → 47**, entirely because a new row mentions
  `tests/fixtures/git-closeout/` — the same `missing-path` class that fires on every not-yet-created deliverable.
  Zero errors; both stages report `pass`.
- **`account-clause-coverage.py` is still not green** (`status: baseline-missing`, 598 clause-uncovered + 4 → 0
  FR-uncovered): an absent baseline is not an empty exemption list and the freeze belongs to T056. This round improved
  the FR lane (4 → 0 uncovered) and did **not** claim the gate green.
