# Analyze Round 2 — Verification of Round 1 Findings and Residual List (2026-11-09)

Stage: analyze round 2 (read-only; no artifact writes outside this findings report and the gate evidence file).
Base commit: `35248f14` (round 1 ran at `1e49534a`; repair landed as `9d5acb7a`).
Evidence: `analyze-round2-gates.txt` (same directory) — the five required gates re-run at this commit.
Input: `analyze-round1-findings.md` (1 CRITICAL / 4 HIGH / 13 MEDIUM / 4 LOW + 2 feature-linkage = 20 findings).

Verdict: **CRITICAL = 0, HIGH = 0. Implement entry is permitted.** 10 residual items carry forward with an explicit
disposition; none is CRITICAL or HIGH, and the two that touch deliverable text are handed to implement as named
preconditions rather than blockers.

## 1. Five required gates — re-read at `35248f14`

| Gate | Reading | Exit |
|------|---------|------|
| `validate-requirements.py` | `status: ok`; 6 checks pass; 320 lines / 36 definition rows / 6 shared strings; 0 error, 0 warning | 0 |
| `pre-analyze-check.py --stage requirements` | `decision=pass`; errors 0, advisories 47, waived 0; `fr=28 sc=8 tasks=62 clauses=0 files=12` | 0 |
| `pre-analyze-check.py --stage plan` | `decision=pass`; errors 0, advisories 47 (identical set) | 0 |
| `validate-decision-tensions.py` | `status: ok`; 6 checks pass; 322 lines / 5 records; 0 error, 0 warning | 0 |
| `decomposition-check.py --mode plan` | `decision=proceed`; `fr_count=28`, ceiling 120; reasons `[]` | 0 |

Supporting (not among the five):
- `account-clause-coverage.py --spec-dir` -> **FR claimed 28 / FR uncovered 0**; `fr-uncovered` check **pass (0)**.
  Status remains `baseline-missing` (598 clause-uncovered, 0 baseline-internal) — unchanged by design; T056 owns the freeze.
- `validate-tasks.py` -> 0 errors / 69 warnings; `green-dangling` + `green-clause-collision` = 0; `green-cross-phase` = 2.

## 2. Clause coverage — 32 clauses / 28 FR, independently reproduced

Not trusted from the round-1 record: recomputed twice, once through the shipped accountant and once with an ad-hoc
parser that re-implements its documented rule (a clause cites the FR ids in its **last FR-containing parenthetical**).

| Quantity | Round 1 (base `1e49534a`) | Round 2 (base `35248f14`) | How measured |
|----------|---------------------------|---------------------------|--------------|
| Contract clauses | 26 | **32** (declaration 7 + executor 8 + lifecycle 10 + verification 7) | clause markers `**C-n**` per page |
| FR universe | 28 | 28 | `^- **FR-nnn**:` rows |
| FR cited from a citation group | 24 | **28** | accountant + independent re-parse |
| FR uncovered | 4 | **0** | both methods agree |
| Distinct green claims | 26 | 32, each clause claimed exactly once | grep of `contracts/*#C-n` tokens in `tasks.md` |

The four formerly-orphaned FRs were checked at **subject** level, not only at citation level — a citation that points at
an unrelated clause is the failure mode C-01 named:

- **FR-020** -> lifecycle C-8: one step, reached by pointer from a closed named set (driver close / house-keeping /
  feedback digest), no second implementation, and the pointer does not widen the driver's authority. Subject matches.
- **FR-021** -> lifecycle C-9: faces rendered by the registry, never authored; order must not collide and is measured.
  Subject matches.
- **FR-022** -> lifecycle C-10 **and** verification C-7: pointer-not-rules, default no-edit, decided by a measurement.
  Subject matches; the delivery-row-only mapping round 1 rejected is gone.
- **FR-027** -> executor C-1: a five-row **owned negative assertion table**, each row stating what the guard asserts is
  absent, plus a statement of which arm (structural vs behavioural) carries each. Subject matches; FR-027's other four
  non-goals are now owned rather than unowned.

## 3. Round 1 findings — current status (RESOLVED / RESIDUAL)

Counts. **Round-1 findings: 20 total, 20 RESOLVED, 0 left open.** By severity: CRITICAL 1/1 resolved,
HIGH 4/4 resolved, MEDIUM 13/13 resolved, LOW 4/4 resolved, feature-linkage 2/2 resolved.
**New residuals created or left visible by the repair: 10** — CRITICAL 0, HIGH 0, **MEDIUM 5**
(R-14 stale premises, R-15 FR-017/FR-018 text tension, R-16 unmeasured parent-ownership claim, R-17 two disclosed
`green-cross-phase` warnings, R-18 `baseline-missing`), **LOW 5** (R-19 NOT-OURS parser, R-20 CHK011, R-21 CHK020,
R-22 CHK028, R-23 CHK040). All 10 carry a disposition — R-14…R-19 in § 4, R-20…R-23 in § 5; none blocks implement.

| ID | Sev | Status | Evidence at round 2 |
|----|-----|--------|---------------------|
| C-01 | CRITICAL | **RESOLVED** | 32 clauses, FR uncovered 0 by two independent methods; subject-level check passed for all four FRs. |
| H-01 | HIGH | **RESOLVED** | declaration C-2 scopes the guard to the block **on both surfaces** and states the snapshot baseline rule; T013 parameterised over both paths; T013's green tag now C-2. |
| H-02 | HIGH | **RESOLVED** | executor C-8 is a four-row value->authority->transition table exercised per value; declaration C-7 keeps only "which value is strongest" and points at C-8; no second wording. |
| H-03 | HIGH | **RESOLVED** | E-4 `covered[]` carries `commit` per row; lifecycle C-2 fixes **one records commit per run**; invariant V-15 is "all `commit` values in one receipt are equal", not field arity. |
| H-04 | HIGH | **RESOLVED** | declaration C-4 owns the remote axis (empty and absent = one outcome, reasons distinguished), C-5 owns the model axis and says so; `ask` named as a third independent axis; V-17 states the orthogonality. |
| M-01 | MED | RESOLVED | verification C-1 cites the form owner by path; the invalid identifier is absent. |
| M-02 | MED | RESOLVED | "no subprocess" scoped to the structural arm; the behavioural arm must run. |
| M-03 | MED | RESOLVED | executor C-7 pins the literal `<remote>` token and asserts on the token. |
| M-04 | MED | RESOLVED | five terminal states, declared closed, each edge case mapped; `degraded` is a named state. |
| M-05 | MED | RESOLVED | one outcome, two distinguished reasons (empty vs absent). |
| M-06 | MED | RESOLVED | per-value effect table exists as executor C-8 (single carrier). |
| M-07 | MED | **RESOLVED (residual note R-16)** | E-4 states the receipt home is decidable by its **parent**; the parent-ownership claim was not re-measured this round. |
| M-08 | MED | RESOLVED | map re-derived; machine-checked by the accountant (reproduced here). |
| M-09 | MED | RESOLVED | E-6 is the single fixture-roster carrier; the SC map points at it. |
| M-10 | MED | RESOLVED | `features/091.md` § Status Tracking present, criteria only, points at the template as the state-machine owner. |
| M-11 | MED | RESOLVED | stage record chain tasks->checklist->analyze->analyze-repair present. |
| L-01 | LOW | RESOLVED | reachability condition stated for the read-only-only-remote edge case; cannot collide with the undeclared-model degradation. |
| L-02 | LOW | RESOLVED | fixed with the containing clause (C-2->T013 pairing). |
| L-03 | LOW | RESOLVED | receipt naming settled in M-07. |
| L-04 | LOW | RESOLVED | fixed in passing. |
| M-LINK-01/02 | LOW | RESOLVED | `features.md` + `features/091.md` chain consistent. |

## 4. Residual list (R-14…R-19) — severity-ordered, with disposition

Dispositions: **implement 前置** = an implement-phase row must discharge it before the feature can be accepted;
**允许携带** = may ride into implement, already owned by a named implement row; **NOT-OURS** = not this feature's to
fix (framework or other-owner defect, surfaced only). No residual is CRITICAL or HIGH; nothing is undispositioned.

### R-14 (MEDIUM) — `tasks.md` stale premises contradict the measured state — implement 前置 (text repair)

`tasks.md` § "Premises measured at generation time" is stamped "re-derived this stage" but was **not** re-derived after
the repair round. Five cells are false against the tree at `35248f14`:

| Location | Stale claim | Measured now |
|----------|-------------|--------------|
| line 67 (Environment Prerequisites) | "the accountant reports ... `FR uncovered: 4` ... each has a discharging clause but no numeric token" | FR uncovered **0** |
| line 100 (premises table) | "Contract clauses **26**" | **32** |
| line 100 | "Data-model validation rules **14**" | **17** (V-1…V-17) |
| line 100 | "Task rows **60**" | **62** |
| line 100 | "FRs with no numeric citation **4**" | **0** |

The superseded reading sits in the section implement reads first, while `§ FR -> row trace` (line 320) **does** carry the
corrected reading and marks the old wording superseded — so the file contradicts itself across two sections.
Disposition: **implement 前置** — one implement row re-derives the premise table and the prerequisites bullet. A text
correction with zero behavioural risk, but leaving it makes `tasks.md` assert a coverage gap that no longer exists.

### R-15 (MEDIUM) — FR-017 / FR-018 remain in tension inside `requirements.md` (CHK016) — implement 前置 (adjudication note)

CHK016's finding stands as a finding *about the requirements text*: FR-017's parenthetical names three gate classes while
FR-018 forbids copying the gate list into "any surface". The repair (correctly) did not amend either FR; it made the
downstream reading unambiguous (lifecycle C-6 and declaration C-7 reference the owner by path and cite no gate by name;
T046 carries the guard predicate). So the downstream reading is settled; the requirements-text ambiguity is not.
Disposition: **implement 前置** — implement MUST NOT resolve it by editing FR-017 (a re-cut of an accepted requirement
outside an analyze pass); it records the settled reading in `verification.md`. MEDIUM because a reviewer reading only
FR-017/FR-018 still sees two readings.

### R-16 (MEDIUM) — M-07's parent-ownership claim is asserted, not measured — 允许携带

E-4 argues the receipt home is legitimate because `.specify/memory/retention/` is a holding root `record-retention.py`
already owns. That is a claim about a script this feature does not modify, and it was not re-measured this round.
Disposition: **允许携带** — T056/A-G1 own the freeze and the directory decision, and a wrong claim surfaces as a red
guard, not a silent defect. If T056 finds the parent is not owned, the receipt moves and only E-4's prose changes.

### R-17 (MEDIUM) — two `green-cross-phase` warnings are disclosed, not zero — 允许携带

`validate-tasks.py` reports 2: T057->declaration C-2 and T061->executor C-8. Both are accepted on their stated reasons in
`tasks.md` § Green Partition, and the reasons were re-read and re-measured this round: each is a clause whose subject
belongs to an earlier phase than the row that turns it green, and renumbering the page into row order would move the
authorization table after the sequences it authorizes. The count cannot honestly be made zero without a worse reading.
Disposition: **允许携带**; the DoD asserts the count is exactly 2, never zero.

### R-18 (MEDIUM) — `account-clause-coverage.py` is still `baseline-missing` — 允许携带 (owned by T056)

598 clause-uncovered across the whole spec corpus, 0 baseline-internal; the FR lane is green. An absent baseline is not
an empty exemption list, and the freeze belongs to T056. Round 2 does **not** claim this gate green. Disposition:
**允许携带** — T056.

### R-19 (LOW, framework) — `pre-analyze-check.py` flags the documented `[blockedBy: Txxx]` placeholder — NOT-OURS

Of 47 advisories: 46 are `missing-path` on deliverables this feature has not created (by construction) and 1 is
`non-concrete blockedBy token 'Txxx'` on `tasks.md` line 73. That line is the **format legend** — it documents the tag
syntax and is not a dependency claim; the check reads a code span in the legend as a real token. Disposition:
**NOT-OURS** — driver-skill parser behaviour, surfaced in `framework_observations`. Deleting the legend to satisfy the
parser would make the file less readable.

## 5. The 15 checklist `fail` items — re-adjudication (this round's owned judgement)

Round 1 left the checklist file untouched, so its marks are round-1 state. Round 2 asked, per item, whether the **owner
text** now answers it.

| CHK | Round 1 | Round 2 verdict | Why |
|-----|---------|-----------------|-----|
| CHK009 | fail | **RESOLVED** | A26 + lifecycle C-2 own the record membership (`covered[]`), defined once. |
| CHK010 | fail (partial) | **RESOLVED** | lifecycle C-7 gives two decidable halves for FR-008 (locate the replaced assertion; old assertion absent from every written surface), both file reads. |
| CHK011 | fail | **RESIDUAL (R-20)** | the three forks are still not declared closed in FR-007, and "records produced, no artifacts" still has no named home. |
| CHK012 | fail (partial) | **RESOLVED** | the criterion is the run's own output set (A23), not tree cleanliness; lifecycle C-5 encodes it. |
| CHK016 | fail | **RESIDUAL (R-15)** | downstream settled, requirement text not. |
| CHK017 | fail (partial) | **RESOLVED** | reading (b) fixed in A24; executor C-5 + V-10 encode it. The requirement's wording still leans (a) but the adjudication exists and is citable. |
| CHK020 | fail | **RESIDUAL (R-21)** | E-4 makes the location decidable by parent, but FR-028's "共享交付根" has no domain and the decision's transfer to tasks is unregistered in requirements. |
| CHK021 | fail (partial) | **RESOLVED** | the identity key is now single-valued: E-4 and lifecycle C-3 both say one file **per run**; no third reading survives. |
| CHK023 | fail | **RESOLVED** | SC-004's body now carries "MUST NOT re-assert the total constant — see A20". |
| CHK028 | fail | **RESIDUAL (R-22)** | A17 is carried by no FR/SC and FR-027's non-goal list omits "host-platform API read". |
| CHK036 | fail | **RESOLVED** | RS-001's `Pin` carries the four-command capability set and states a version-string comparison is not a substitute; A25 records why. |
| CHK038 | fail | **RESOLVED** | the edge case states its reachability condition and why it cannot collide with the undeclared-model degradation (L-01). |
| CHK040 | fail | **RESIDUAL (R-23)** | the value grammar is still downstream-only and the two sites differ ("empty or absent" in E-1 vs "explicitly empty list" in declaration C-1). |
| CHK045 | fail | **RESOLVED** | the map is machine-checked; reproduced 28/28 uncovered 0 independently; the four subject-level pairings verified. |
| CHK046 | fail | **RESOLVED** | `Readers` + `Reading scenario` present; `doc-consistency-check.py --faces reader` -> `reader=pass`, 0 findings. |

Round-2 tally over the 15: **10 RESOLVED, 5 RESIDUAL**. Checklist file totals unchanged: 25 pass / 15 fail / 7 观察 = 47.

### R-20 (LOW) — CHK011: "records without artifacts" has no named branch

FR-007 lists three forks without declaring them closed, and "a record class landed, no artifact commit this run" matches
none. `data-model.md` § State transitions does not cover it — the `records produced` arrow assumes an artifact commit.
Disposition: **允许携带** — the outcome is expressible in E-5's report vocabulary and lifecycle C-5's forks bracket it;
implement records the reading in `verification.md`. LOW because the gap is in the enumeration, not the behaviour.

### R-21 (LOW) — CHK020: FR-028's location delegating to tasks is unregistered

FR-028 says the receipt shares "一个共享交付根" and is "一文一件" — neither a path nor a resolvable owner name; E-4 settles
it by parent. The requirements->tasks decision transfer is real but unrecorded in requirements. Disposition:
**允许携带** — A-G1/T056 own the decision; only the traceability of the transfer is thin.

### R-22 (LOW) — CHK028: A17 (no host-platform API) is carried by no FR/SC

A17 states the boundary; no FR or SC asserts it and FR-027's non-goal list omits it. It is nonetheless enforced by
construction: executor C-1's fifth row asserts no remote API is contacted. Disposition: **允许携带** — the obligation
exists at clause level; a reader checking FRs alone cannot find it.

### R-23 (LOW) — CHK040: STR-002's value grammar is downstream-only and self-disagreeing

Requirements carry no grammar. Two downstream sites describe it differently: `data-model.md` E-1 "comma-separated; empty
or absent means no pushable remote" versus `closeout-declaration.contract.md` C-1 "a comma-separated list of remote names,
or an explicitly empty list". "Empty or absent" and "explicitly empty" are not the same claim about a blank value.
Disposition: **允许携带, with a demanded tie-break** — implement adopts declaration C-1's wording (the clause owns the
block's shape) and reads "absent" as equivalent to "empty" per C-4's one-outcome rule; one sentence in `verification.md`.

## 6. Implement-entry decision

**CRITICAL = 0 and HIGH = 0 => implement entry is permitted.**

The residuals are **5 MEDIUM and 5 LOW**. Each has an owner and none invalidates an acceptance criterion. The two MEDIUM items that touch deliverable text (R-14, R-15) are text-and-note corrections with no
behavioural risk, handed to implement as named preconditions rather than blockers.

Carried into implement, in brief:
1. **R-14**: re-derive `tasks.md` § Premises (5 stale cells) — do this **before** executing task rows.
2. **R-15**: do not edit FR-017; record the settled reading (C-6 / C-7 / T046) in `verification.md`.
3. **R-16 / R-17 / R-18**: owned by T056 and the DoD; assert `green-cross-phase` is exactly 2.
4. **R-20 / R-21 / R-22 / R-23**: one-sentence adjudications in `verification.md`; R-23 also demands adopting
   declaration C-1's wording over E-1's.
5. **T056** freezes `coverage-baseline.txt`; until then the accountant cannot judge a delta and stays `baseline-missing`.

Not ours: R-19 (driver-skill parser reads a format legend as a dependency token).
