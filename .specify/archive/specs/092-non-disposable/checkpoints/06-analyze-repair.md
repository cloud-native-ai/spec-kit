# Checkpoint 06 — analyze repair

## 1. Artifact verification

- scope: the bounded analyze repair for `test-evidence/analyze-findings.md` F-1…F-25, editing only this feature's artifacts
- required closures: F-3 (CRITICAL) closed; F-1, F-2, F-4, F-5, F-7, F-8, F-10, F-13, F-19 (HIGH) closed; F-6, F-9, F-11, F-12, F-14…F-18, F-20…F-25 closed in the same pass
- four gate readings: `test-evidence/analyze-repair-gates.txt` — coverage `status: ok` (62/62 clauses claimed, FR lane `uncovered: 0`), tasks `PASS 0 error(s), 0 warning(s)`, decision-tensions `0 error(s)`, pre-analyze `decision=pass errors=0 advisories=0`

### The four owner-arbitrated rulings, and where each landed

| Ruling | Landed in |
|---|---|
| F-3 — extend the closed status domain so `Planned × accept` (A3) is detectable | `status-and-verification` C-202 now fixes the closed registry domain (six live values + `Relocated`), the total status × verdict table, and the reason-code assignment; `acceptance-readability` C-802 owns the table and its corpus/fixture legs; C-803 requires A3 to land **red** |
| F-7 — widen C-203's object to the three readable objects | `acceptance-readability` C-801 names O1 registry row / O2 verification machine-block / O3 tasks + decision-tension structure; `status-and-verification` C-201…C-206 says why the rest lives there; A6 is C-804, judged by `validate-requirements.py path-marker` and explicitly **not** by `status-unreadable` |
| F-13 — named shard formula, and "shards act on the file set" | `detection-engine-cli` C-606: `s{index:03d}-of-{n:03d}`, assignment by sorted path index mod `n`, and the sentence that classes do not participate (this is what removes the C-102 conflict); C-604 points at it |
| F-10 — the 档 II marker clause, and the 12/15/19 reconciliation | `acceptance-readability` C-805 (form, guard carrier, counting); `plan.md` § Shift List carries the count table; `tasks.md` DoD-4 reads both numbers; `team.md` gained a `write_carve_outs` block naming which surface lands the marker |
| F-5 — FR-050/051/057 have no clause | C-806 declares FR-046/050/051 **process-grade**; FR-057 was *not* put in that set — it has a readable object, so C-805 carries it. The FR lane closes by citation or by a named declaration, never by absence (GATE-5 now says so) |
| F-8 — references to nonexistent clauses | quickstart §1/§3 now point at `harness-triple-check.resolve_repo` and 086's real last clause C-016 + 089 C-35; `tasks.md` T127 now names 085 C-007/C-008 and C-001 |

### Judgment calls made without a further round-trip

- `Relocated` is a real live value (one row in `features.md`), so it is excluded from the contradiction table **by name** with its reason, not by silence.
- C-206 and C-207 were **swapped** so that the newly claimed clause sits after the previously claimed one (the `green-cross-phase` check reads clause order against row order); citations were re-seated accordingly, and FR-062 moved off this file entirely (F-1).
- The new contract file is `contracts/acceptance-readability.contract.md` (C-801…C-807) rather than an eighth section inside `status-and-verification`, because the contradiction table has an owner the consumption clauses do not.
- Two new tasks rows were needed (T156 seam-bypass; five owner-page rows), all on plain ids after the id-normalization described below.

### Id normalization (worth reading before the tasks stage)

`tasks.md` row ids are read by two tools with different regexes: `validate-tasks.py` wants `T<NNN>`, and `pre-analyze-check.py`'s duplicate-id check truncates to the first three digits, so `T001a…T001e` all read as duplicates of `T001`. The six new rows therefore use plain sequential ids (`T001`–`T005` for the owner-page rows, `T156` for the guard row), not lettered variants. Never re-introduce `Tnnna`/`T-na`.

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| A–H classes covered | 100% | `plan.md` § A–H Corpus Mapping; A3 now has an engine-visible cell (C-802) |
| Mechanism reproduces A–H | not_evaluated (implement) | — |
| Repair lane after confirmation | not_evaluated | — |

## 3. Team configuration review

- evidence: no team run in this stage; the roster's territory changed (`write_carve_outs` added under `territory`)
- symptom: the previous `forbidden` list forbade every 档 I/档 II body the feature must repair — the territory contradicted P6/P7
- proposal: narrow the list to the two named write faces (C-805 requires this decision to be recorded)
- applied: yes — `team/092-non-disposable/team.md` § territory (`write_carve_outs`, P6 record-completion, P7 one marker per receiving body); YAML front matter re-parsed

## 4. Next stage concurrency / roster

- requested: 24; effective: 24; stage max_parallel: 1 (the repair was serial, one artifact at a time); verifier reserve 1

## 5. Direction audit

- reload tier: T0+T1
- Q1 rules: in force — the CRITICAL was repaired at its owner page rather than deferred to implement; every count conflict is now stated once with its source
- Q2 process: no implementation file, no other feature's body, no constitution, no push
- Q3 next action: implement (the repair closed the analyze findings; the gates are green)
- Q4 spine freshness: this checkpoint records the repair; the driver owns the spine write
- Q5 territory/workspace: this feature's artifacts only; the pre-existing dirty file left untouched
- verdict: on-track

## 6. Anomalies and residual notes

- The corpus reading for A3 was not re-derived on this tree during the repair: C-802's clause states what A3 must read (closure `accept` 4/4, registry `Planned`) and C-803 requires the guard to land it red. If the tree moved, the number in the clause is the recorded reading at analyze time, not a live one.
- `coverage-baseline.txt` was not re-frozen: `--freeze` excludes the spec being accounted, so the 62 clauses are claimable without touching the baseline. Re-freezing before the first implement run is still T042's job.
- The 107 `clause-unparsable` warning is pre-existing and baseline-internal (no file declares a positive form), unchanged by this repair.
