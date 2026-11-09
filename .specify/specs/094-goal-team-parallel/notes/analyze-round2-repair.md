# Analyze round 2 — repair closure ledger (1 CRITICAL + 4 HIGH + 1 MEDIUM)

**Authority for this repair**: `notes/analyze-round2-findings.md` § 6 (repair brief). Every closure below is
either the brief's prescribed edit or a recorded decision where the brief itself offered two readings
(`fast-fail`: a choice between recorded readings is a decision with a rationale, never a silent invention).
**Measured-before-edited discipline**: no clause was rewritten from memory — C‑71/C‑72/C‑74 and the resident
denominator were re-measured on 2026-11-09 first
(`test-evidence/analyze-repair2-engine-measurements.txt`, `test-evidence/analyze-repair2-resident-measurement.txt`).

## 1. Closure ledger (one row per finding)

| id | severity | state | what closed it | evidence |
|---|---|---|---|---|
| **C-2** | CRITICAL | **closed** | C‑71's predicate replaced: the family criterion is now `source: ledger` / `source: default` read from the lookup record, and the clause states in the same breath that neither `flow_class` nor the exit code decides it (with the measured counter-example `/speckit.nonexistentcommand` → `flow_class: execution`, `source: default`, exit 0). C‑72 aligned to the same discriminator and extends its input set to `source`, `marker`, `error` + exit code. C‑74 now names the field both consumers read. The word `ledger` appears in the conformance layer for the first time (`grep -c ledger contracts/` = 0 before this repair). | `contracts/command-family-and-declarations.md` C‑71/C‑72/C‑74; `test-evidence/analyze-repair2-engine-measurements.txt` § 1–3 |
| **H-2** | HIGH | **closed** | `feature-ref.md`'s FR→clause map is **regenerated from the contracts**, not edited: 43 rows / 43 distinct FR ids, produced by `clause_extract.clause_citations()` over the five contract pages; the generating snippet is embedded in the page so the next reader re-derives instead of hand-patching. `plan.md`'s two certifications ("42/42", now 43/43) and the measurement map (12/12, SC‑012 added) were corrected in the same pass. | `feature-ref.md` § Delivery map (includes the command); `plan.md` L63/L88/L372–L374 |
| **H-3** | HIGH | **closed (option (a) — decided, not assumed)** | A named owner exists at three layers: **FR‑043** (requirements, group B) + **C‑53/C‑54** (contract) + **SC‑012** (criterion) + **T082/T081/T083** (implementation, contract test, real-tree run). The ruling `owner: human` / `owner_id: human` / `origin: null` is recorded in Clarifications as a **decision** (Q14) with its rejected alternative. Denominator is measured, never restated: 6 goal + 12 team = 18 residents, 0 bound. | `requirements.md` FR‑043 + SC‑012 + Q14; `contracts/unified-archive-and-migration.md` C‑53/C‑54; `tasks.md` T082/T081/T083; `test-evidence/analyze-repair2-resident-measurement.txt` |
| **H-4** | HIGH | **closed** | Re-measured the accepted grammar in both engines: `flow-class-check.py` accepts `/speckit.<stem>` or `skill:<dir>`; `run-determination.py` adds only `custom:<owner>/<name>`; **neither accepts `command:<name>`** (exit 2, `invalid-unit-id`). C‑71/C‑72/C‑74 and T020/T021 were rewritten to the `/speckit.<stem>` form and to a verdict read from `source`; the grammar itself is referenced by owner-literal (the two modules) rather than restated, so it cannot drift. | `test-evidence/analyze-repair2-engine-measurements.txt` § 1–2; `contracts/command-family-and-declarations.md` C‑71; `tasks.md` T020/T021 |
| **H-5** | HIGH | **closed (single reading, recorded)** | Two halves, both decided. (a) **plan T‑004 rewritten** to the one current reading `{goal, teams, auto}` — title, `decision`, `discriminating_evidence` (three retired values fail identically, two current values exit 0) and `expected_sacrifice` re-authored against the new member set; the rejected antithesis is kept as the rejected proposal with its scope narrowed. (b) **A11 / § Notes point at C‑36**, and FR‑009 gets **no** new sentence — the prohibition's normative face already lives in C‑36 and a second statement is a second definition point (Constitution XIV). The Clarifications Q(H‑5) answer now records this as **fact**, not as a pending to-do. | `plan.md` T‑004; `requirements.md` § Notes (A11 bullets), Clarifications Q(H‑5) |
| **M-3** | MEDIUM | **closed** | The three previously unowned code items are now explicit task text: the runtime default `… else "global"` (`goal-utils.py:1416`) plus the two user-facing guidance strings (`:166`, `:1418`) land in **T014**; T013 now demands the full literal sweep (default parameter, membership tuple, `Scope("global", …)` constructions, argparse `choices` — "seven `"global"` literals" measured). FR‑025's trace row now cites T013 **and** T014. | `tasks.md` T013/T014, FR lane row `FR-025` |

Nothing else in the round-2 report was touched: M‑2, M‑4, M‑5, L‑4, L‑5, L‑6 and the § 3 "does not hold" items
stay open for round 3 by the dispatch brief's "do not touch the other MEDIUM/LOW items".

## 2. Decisions taken (the brief offered a choice; the reading is recorded here)

**D‑R2‑1 — H‑3 goes to option (a), backfill, not option (b), narrow C‑1.**
Rationale: (i) option (b) makes the feature land on an engine that cannot *read* 18 of its own definitions —
C‑1's rejection is what makes them unreadable, so narrowing the rejection leaves the archive half-legible;
(ii) option (b) also silently contradicts FR‑023's "every definition carries the binding record"; (iii) the
backfill is byte-preserving and idempotent, so its blast radius is one inserted block per file and it is
reversible. Anti-metric to watch: if the backfill needs a judgement call per resident (i.e. `owner: human`
stops being uniform), the ruling was wrong and H‑3 reopens. Recorded in `requirements.md` Clarifications Q14.

**D‑R2‑2 — H‑5's plan-side half is an edit to T‑004, not a "keeps the pre-H‑02 wording" note.**
Rationale: a decision record that carries a member set already ruled out by Q13 cannot be distinguished by a
later reader from one that is current; `validate-decision-tensions.py` validates the *shape*, not the
*agreement with the FR it names*, so no gate would catch it. Anti-metric: if editing T‑004 turned out to
invalidate its own antithesis, the record was never a record of one tension. The antithesis survived (it is
the same rejected proposal, re-scoped).

**D‑R2‑3 — the resident-backfill rows sit at the end of Phase 8, not inside the US2 block.**
This decision cost one iteration: `validate-tasks.py`'s `green-cross-phase` rule compares clause ordinals
against **row** order *within one contract*, and the archive contract is attributed in clause order
(C‑31…C‑50 → T028, C‑51 → T079, C‑52 → T080, C‑53/C‑54 → T082). Placing T082 inside US2 (before T079/T080)
makes the clause order run backwards and the checker says so. The repair is a re-cut of the *row* placement,
never a weakening of the gate or a dropped claim: T082 keeps both claims, sits after T079/T080, and the
reason is written into `tasks.md` § Phase 8 as a note. Anti-metric: if a future edit re-inserts a backfill
row above T079, the same warning returns — that is the rule working, not noise.

**D‑R2‑4 — C‑53/C‑54 instead of C‑53/C‑54/C‑55 (the archive contract stays at 24 clauses).**
An earlier draft split the dry-run obligation out as C‑55; that duplicated what C‑51 (the real-data dry run)
already owns. Clauses per contract are now binding 30 · archive 24 · handoff 18 · command-family 20 ·
owner-rewrites 21 = **113**, and claims = 113, unique = 113.

## 3. Gate readings (all re-run after the edits; evidence files retained)

| gate | command | reading |
|---|---|---|
| requirements | `validate-requirements.py <S92>/requirements.md` | `status: ok`, **0 error / 0 warning**, 316 lines, 55 definition rows |
| coverage | `account-clause-coverage.py <S92> --corpus-root /storage/project/cloud-native-ai/spec-kit/.specify/specs` | `status: ok`, FR universe **43**, FR claimed **43**, FR uncovered **0**; uncovered beyond baseline **0** (598 baseline-internal); claimed clauses 113, scanned 297 |
| tasks | `validate-tasks.py <S92>/tasks.md` | `0 error(s), 1 warning(s)` — the disclosed `T043 → T054` forward dependency only |
| decision tensions | `validate-decision-tensions.py --spec <S92>` | `status: ok`, 7 records (T‑001…T‑007), **0 error / 0 warning** |
| pre-analyze × 3 | `pre-analyze-check.py --repo . --spec-dir <S92> --stage requirements\|plan\|tasks` | **pass** on all three stages, exit 0, 88 findings each, **0 non-advisory** |
| decomposition | `decomposition-check.py --mode tasks --tasks <S92>/tasks.md --requirements <S92>/requirements.md` | **proceed** — 43 FR / 83 tasks against ceilings 120 / 160 |
| decomposition (plan) | `decomposition-check.py --mode plan --requirements <S92>/requirements.md` | **proceed** — 43 FR, ceiling 120 |

Readings: `test-evidence/analyze-repair2-gates-requirements.txt`, `…-gates-tasks.txt`, `…-gates-precheck.txt`,
plus the pre-edit baselines `test-evidence/analyze-repair2-baseline-*.txt`.

## 4. Residual risks handed to round 3

- **R‑1 — H‑2 can recur.** The map is generated *once*, by a snippet embedded in the page; nothing re-runs it.
  Fixing that is § 6 item 8 ("close the structural blind spot"), explicitly out of this round's scope. Proposal
  for a later round: a contract test that re-derives the table and diffs it, or a `feature-ref.md` generator.
- **R‑2 — H‑5 can recur for the same reason.** No gate compares a decision record's `decision` against the FR it
  cites; `discriminating_evidence` is prose to the validator. T‑004 is now consistent by authoring, not by
  construction.
- **R‑3 — the backfill ruling (`owner: human`) is a judgement, not a measurement.** It is uniform across the 18
  residents today; T082's `binding-incomplete` refusal is the surface that will expose the first resident that
  disagrees.
- **R‑4 — SC‑012 is unmeasured on the apply side.** Only the baseline half exists
  (`analyze-repair2-resident-measurement.txt`); the post-backfill half is T083's obligation at implement time.
- **R‑5 — the one remaining warning is disclosed, not cleared.** `T043 → T054` is a genuine forward dependency
  inherited from the tasks stage; clearing it means re-cutting that dependency, not silencing the check.
- **R‑6 — duplicate session headings.** `requirements.md` carries three `### Session 2026-11-09` clarification
  headings (pre-existing). The repair added no fourth by appending to the last one; merging them is a separate,
  structural edit.
