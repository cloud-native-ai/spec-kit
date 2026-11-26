# Analyze Report (r5, final) — 106 Background Silent Failure

- **Spec**: `.specify/specs/106-background-silent-failure`
- **Stage**: `analyze` — final gate reading after incremental round 5
- **Date**: 2026-11-26 · **Owner of this merge**: SDD Analyze Final Integrator (this bounded assignment)
- **Scope of this pass**: synthesis only — **no detection re-run, no MEDIUM validation, no spec-artifact edit**. Structural-check results quoted below are the repairs' own recorded runs, not new executions.
- **Inputs**: round-1 report `analyze-report-2026-11-25.md` · round-2/3 findings `analyze-domain-*-r2.jsonl` / `analyze-domain-*-r3.jsonl` · round-4/5 findings `analyze-incremental-r4.jsonl` / `analyze-incremental-r5.jsonl` · validation waves `.specify/state/validate-wave{1,2,3}.verdicts.json` + the round-4 validator record (`validate-r4-01`) · repair records `analyze-repair-2026-11-25.md`, `analyze-repair2-2026-11-25.md`, `analyze-repair3-2026-11-25.md`, `analyze-repair4-2026-11-26.md` · reused-domain hashes `.specify/state/analyze-r4-reused-domain-hashes.txt`.

## 1. Gate verdict

**gate: PASS — 0 CRITICAL, 0 HIGH, 6 MEDIUM residual**

Every CRITICAL/HIGH raised across five detection rounds was validator-confirmed and repaired (20), validator-downgraded (2) or validator-rejected (2); the final incremental round (r5) re-detected the repaired loci and returned 0 CRITICAL / 0 HIGH / 6 MEDIUM. The 6 MEDIUM residuals are carried openly in §5 and do not block. `/speckit.implement` may start.

## 2. Verification chain

### 2.1 Round table

| Round | Kind | Workers / read domains | Findings detected | C/H sent | Verdicts (confirm / downgrade / reject) | Gate C/H after validation | Repair | Next-round adjudication |
|---|---|---|---|---|---|---|---|---|
| R1 | full wave | W1 · W2 · W3 + integration | 31 (0C/12H/13M/6L pre-validation) | 12 | 10 / 2 / 0 | **10 HIGH** — FAIL | repair1 fixed 10 HIGH | R2 re-read: all 10 fixed |
| R2 | full re-run | w1 · w2a · w2b · w2c · w3 | 38 (0C/6H/24M/8L) | 6 | 5 / 0 / 1 | **5 HIGH** | repair2 fixed 5 HIGH (w2c-03 rejected, not repaired) | R3 re-read: all 5 fixed |
| R3 | full re-run | w1 · w2a · w2b · w2c · w3 | 29 (0C/5H/17M/7L) | 5 | 4 / 0 / 1 | **4 HIGH** | repair3 fixed 4 HIGH (R3-W2B-03 rejected, not repaired) | R4 re-read: all 4 fixed; a related residual filed anew as R4-02 |
| R4 | incremental | 1 worker · plan.md, data-model.md, enforcement-&-migration contract (+ one-hop) | 5 (1H/4M) | 1 | 1 / 0 / 0 | **1 HIGH** | repair4 fixed R4-01 | R5 re-read: fixed (MEDIUM residue R5-01) |
| R5 | incremental | 1 worker · data-model.md, carrier-conformance contract, enforcement-&-migration contract (+ one-hop) | 6 (0C/0H/6M/0L) | 0 | — | **0** — PASS | none needed | — |

Round-1 detail: 12 HIGH were sent; 2 were downgraded (W1-01 → MEDIUM, W2-02 → LOW), leaving 10 HIGH at the gate. The two rejected findings (w2c-03 in R2, R3-W2B-03 in R3) are outside the residual set; the R4/R5 briefs barred re-raising R3-W2B-03 without new evidence, and it was not re-raised.

### 2.2 Open-HIGH trajectory

10 (R1) → 5 (R2) → 4 (R3) → 1 (R4) → **0 (R5)**.

### 2.3 HIGH-by-HIGH disposition

- **R1 (10, repaired by repair1; each re-read fixed in R2)**: W1-02 · W1-03 · W1-04 · W1-05 · W1-06 · W1-07 · W2-01 · W2-03 · W2-04 · W3-01.
- **R2 (5, repaired by repair2; each re-read fixed in R3)**: R2-W1-01 · R2-W1-02 · R2-W3-01 · w2a-01 · w2b-01. Rejected: w2c-03.
- **R3 (4, repaired by repair3; each re-read fixed in R4)**: R3-W2A-01 · R3-W2A-02 · R3-W2B-01 · R3-W2B-02. Rejected: R3-W2B-03.
- **R4 (1, repaired by repair4; re-read fixed in R5)**: R4-01; its MEDIUM residue is R5-01 (definition of "malformed 7-column row"), not a re-opening of the HIGH.
- **R5**: none detected.

### 2.4 Closing readings of the repaired HIGHs (from the next round's adjudication)

| Finding | Closing reading (next-round verified) |
|---|---|
| W1-02 | Exit 0 + explicit `ANOMALY:` signal settles `anomaly`; incomplete-`failed` applies only without the marker (FR-003/FR-004, C-02). |
| W1-03 | A-7 / FR-006 no-pid deadline branch aligned; the proposed glossary entry widened before A-15 takeover. |
| W1-04 | Boundary inputs declared once on C-25 (`--live-window` / `--wait-deadline` / `--start-grace`: defaults, domains, precedence); requirements carry pointers only. |
| W1-05 | FR-002 closed mechanism set {u4, team-verification, five-element, return-record}; expansion only by spec revision. |
| W1-06 | Attempt-record carrier named: additive `<label>.attempt` under the existing dispatch-log root; FR-038 declares it allowed-additive, not a new store. |
| W1-07 | FR-039 / SC-009 re-scoped to plan EP-005 per-file counts; `total == 27` red at base disclosed; never claimed green. |
| W2-01 | C-06 reconciled to a two-cause `unknown` (missing start record vs unreadable evidence); exit semantics aligned. |
| W2-03 | Legacy 5-column row carved out of `settlement-unrecorded` (legacy annotated, not judged, no exit 1). |
| W2-04 | Pid-less running/silent-end boundary bound to C-25's declared inputs; no undeclared value remains. |
| W3-01 | tasks.md plan-owned faces are spec-side only and explicitly crew-forbidden; the territory contract wins on conflict. |
| R2-W1-01 | The wait deadline triggers the settlement-time observation; no second grace parameter; later returns are late returns under FR-009. |
| R2-W1-02 | SC-006 asserts a relative criterion (zero new drift on the feature's touched surface). |
| R2-W3-01 | Crew writes `test-evidence/verification-input.md`; `verification.md` is spec-side derived and forbidden to every crew seat. |
| w2a-01 | C3 seat start record (E2 `c3-team-seat` or same-label C1/C2 start evidence); the report row stays the E5 claim surface only. |
| w2b-01 | C-02/C-03 consume C-25's `--live-window` / `--wait-deadline` / `--start-grace` by name; numbers stay on C-25. |
| R3-W2A-01 | Legacy = annotated, not judged; all three E7 predicates scoped to version-bearing records; the exit-2 `unknown` refusal stays version-independent. |
| R3-W2A-02 | C2's E4 mechanism is `return-record`; the parent-written `<label>.settlement` claim has a declared writer and lives in the existing evidence directory. |
| R3-W2B-01 | C-33 qualified: legacy exempt from the three predicates; exit 1 kept for version-bearing violations; exit-2 boundary unchanged. |
| R3-W2B-02 | C-34 closed behavior-class set gains FR-010 and FR-024 (ten duty items). |
| R4-01 | Version-bearing is a per-shape test — claim file by `settlement_version`, team-report row by its 7-column header (5-column = legacy); malformed 7-column row is `settlement-unrecorded` (exit 1). |

### 2.5 Structural verification carried with every repair

Each repair re-ran and recorded: `validate-requirements` (rc 0, 0 error / 0 warning; 312 lines, 41 FR + 9 SC + 4 shared strings) · `validate-tasks` (rc 0, 0/0) · `pre-analyze-check` at requirements / plan / tasks (`decision=pass`, errors=0, advisories=55 — all expected missing-path of planned new tests/fixtures) · `decomposition-check` (`proceed`; fr 41 / tasks 37; ceilings 120/160) · clause extract (3 files, 34 clauses, ids unchanged) · clause coverage (identical reading: `clause-uncovered` beyond-baseline 0; `fr-uncovered` 37/41 — FR-036/037/039/040; `clause-unparsable` 111 = documented corpus-wide structural verdict, not a pass criterion) · gate scan (total 31; 0 violations) · glossary validate (`{"valid": true}`). At repair4 the clause-extract, clause-coverage and gate-scan outputs were **byte-identical** (`cmp`) to the repair3 readings. No FR/SC/STR/clause id, closed set, sentinel literal, exit-code meaning or preserved surface changed across the four repairs.

## 3. Incremental rounds — declaration and reused-domain hashes

**Declaration (R4 and R5 dispatch briefs, verbatim intent)**: incremental touched-loci re-check; read only the repair-touched files plus one-hop neighbors; **W1/W3 reused with hashes by the driver**; one worker, single unit (`effective_reason=single-unit`).

- **R4 read domain**: `plan.md`, `data-model.md`, `contracts/enforcement-and-migration.contract.md`.
- **R5 read domain**: `data-model.md`, `contracts/carrier-conformance.contract.md`, `contracts/enforcement-and-migration.contract.md`.
- **Not read in R5 by declaration**: the W1 set (requirements / checklists / constitution / glossary), the W3 set (tasks / feature-ref / handoff / coverage-baseline / team / anchor), and quickstart/research (so R4-04 was explicitly not re-checked).

**Hash record** — `.specify/state/analyze-r4-reused-domain-hashes.txt` (copy committed as `test-evidence/analyze-r4-reused-domain-hashes.txt`), re-verified by this pass on 2026-11-26 with `sha256sum` — all four current files match byte-for-byte:

| File | sha256 (recorded = current) |
|---|---|
| `requirements.md` | `d2f8d5056366b81b2716edcf07ede2903a909a2146a5c0c0caae7e4b9ad56e78` |
| `checklists/requirements.md` | `06260b155926088c46213c30526e9e2befd4af0e3538e9c91024ad3317bb5dd7` |
| `checklists/background-settlement-2026-11-25.md` | `71d7d2ac2e325abaf00a5e6a6e21a77ad0beab0c5f42f20389364b9001ceeec8` |
| `.specify/constitution.md` | `dbabe7e4572716a70ad2d501200082d9773b0cdf7cb99bd9f99070deb0ece383` |

**Evidence boundary (disclosed, not silently widened)**: the persisted hash record covers the four W1-domain files listed. It records no digest for `.specify/glossary.md` (also inside W1's read set) and none for any W3-domain file (`tasks.md`, `feature-ref.md`, `handoff.md`, `coverage-baseline.txt`, `team.md`, `anchor.md`); no separate W3 hash artifact was located under `.specify/state/`. The W3 half of the reuse declaration therefore rests on the dispatch brief, not on a persisted digest. Consequently this report's gate reading rests on (a) the R5 detection over its three declared files and (b) the W1 digest-verified non-change; it does **not** claim a fresh R5 pass over the W3 artifact set. This bound changes no finding severity and does not affect the 0 C/H reading. Note the repair3 and repair4 edits to `tasks.md` (2 and 4 lines respectively: T035 verification split; T003/T029 per-shape version test) sit inside the W3 read set but outside any persisted hash record.

## 4. Round-5 detection — what the final round actually returned

- **Worker**: one read-only SDD Analysis Worker; output `test-evidence/analyze-incremental-r5.jsonl`; passes A duplication · B ambiguity · C underspecification · E coverage gaps · F cross-clause contradictions · G relevance · I decision-tension; budget ≤6 findings; no self-validation, no repair.
- **Result**: 6 findings — **0 CRITICAL · 0 HIGH · 6 MEDIUM · 0 LOW**. Worker final line `WP-R5-DONE`; anomaly line `未发现异常`.
- **Adjudication lines (worker, verbatim intent)**: R4-01 **fixed** — the per-shape version test (claim file: `settlement_version`; team-report row: 7-column header; 5-column = legacy) is present and consistent across E5/E6/E7/INV08 + C-16/C-33; the residual "malformed 7-column row" ambiguity is recorded as R5-01. R4-02 / R4-03 / R4-05 **still open** — re-emitted as R5-04 / R5-05 / R5-06. R4-04 **not re-checked** (quickstart outside the read domain).

## 5. Residual findings

### 5.1 Final residual set — R5, 6 MEDIUM (not validated: MEDIUM/LOW skip the C/H wave by rule; severity is the worker-declared one)

| ID | Category | Subject | Provenance |
|---|---|---|---|
| R5-01 | ambiguity | "Malformed 7-column row" is undefined: one input is simultaneously `settlement-unrecorded` (exit 1) and unparseable evidence → `unknown` (exit 2); the readable-empty-cells reading exists only as Assumption 3 of the repair record. | **New** — residue of the R4-01 repair |
| R5-02 | cross-clause contradiction | C-16/E7 classify an empty `evidence` cell on a 7-column row as `settlement-unrecorded`, while E5 requires evidence only for `completed`/`silent-end`; a `completed` row with empty evidence matches both `settlement-unrecorded` and `settlement-unbacked` with no precedence. | Persists from R3-W2C-04 |
| R5-03 | coverage gap | C-15/C-17 are closed settlement-rule lists with **no live branch**; a still-live C2/C4 attempt at settlement is unassigned or forced to `unknown`/`silent-end` by elimination. | Persists from R3-W2C-02 |
| R5-04 | cross-clause contradiction | C-34's closed behavior-class set does not equal the behavior-class tags carried by C-13, C-15, C-17, C-20 and C-33; which duties are exempt from machine coverage is not reproducible. | Persists from R4-02 (C-17 added beyond R4-02's four) |
| R5-05 | ambiguity | C-27 requires emission of the four edge kinds "where they apply" in settle output, but E6's `violations` field is typed `list of E7` (three settlement kinds); no clause states which edge kinds apply, where they enter the row, or their exit. | Persists from R4-03 |
| R5-06 | underspecification | E9's Reaction Record declares fields but no storage surface, writer or reader; no clause references it and E6 carries no reaction field, while C-31 requires fixtures to assert "the reaction". | Persists from R4-05 |

### 5.2 Carried earlier findings without a disposition

**Explicitly carried (named in the last round, not re-checked in R5)**:

| ID | Severity | Subject | Round |
|---|---|---|---|
| R4-04 | MEDIUM | C-34 requires behavior-class clauses to be "named as such in the contracts and quickstart", but quickstart.md names none; not re-checked in R5 (quickstart outside the read domain). | R4 |

**Earlier non-HIGH inventory — recorded, no disposition, last-declared severity.** The four repairs were bounded to validator-confirmed HIGH sets and adjudicated no non-HIGH finding; some of those loci were touched by HIGH repairs, so incidental closure cannot be excluded and is **not claimed**. Items below are carried as recorded (not re-validated, not re-detected in this pass):

| Round | Count | IDs (severity) |
|---|---|---|
| R1 (post-validation) | 21 = 14 M + 7 L | W1-01·M · W1-08·M · W1-09·M · W1-10·M · W1-11·L · W2-02·L · W2-05·M · W2-06·M · W2-07·M · W2-08·M · W2-09·M · W2-10·L · W3-02·M · W3-03·M · W3-04·M · W3-05·M · W3-06·M · W3-07·L · W3-08·L · W3-09·L · W3-10·L |
| R2 | 32 = 24 M + 8 L | R2-W1-03…08·M (6) · R2-W1-09,10·L (2) · w2a-02…05·M (4) · w2a-06·L · w2b-02…05·M (4) · w2b-06·L · w2c-01,02,04,05,06·M (5) · R2-W3-02…06·M (5) · R2-W3-07…10·L (4) |
| R3 | 24 = 17 M + 7 L | R3-W1-01…03·M (3) · R3-W1-04…06·L (3) · R3-W2A-03,04·M (2) · R3-W2A-05,06·L (2) · R3-W2B-04…06·M (3) · R3-W2C-01…05·M (5) · R3-W2C-06·L · R3-W3-01…04·M (4) · R3-W3-05·L |
| R4 | 4 M | R4-02·M (→R5-04) · R4-03·M (→R5-05) · R4-04·M (carried above) · R4-05·M (→R5-06) |
| R5 | 6 M | R5-01…R5-06 (table 5.1) |

Re-emission bookkeeping (to avoid double counting): R3-W2C-02 → R5-03 and R3-W2C-04 → R5-02 are subsumed by their R5 rows; R4-02 / R4-03 / R4-05 are subsumed by R5-04 / R5-05 / R5-06. Excluded from the carried set: w2c-03 (HIGH, rejected in R2) and R3-W2B-03 (HIGH, rejected in R3). The RECORDED non-HIGH total across rounds is 87; after the 5 subsumed re-emissions the unsubsumed recorded inventory is 82 — **no disposition is claimed for any of them**, and this bookkeeping does not affect the gate, which counts CRITICAL/HIGH only.

## 6. Metrics

### 6.1 Detection output and gate state per round

| Round | Detection findings (C/H/M/L) | Post-validation C/H at gate | New HIGH entering repair | Cumulative repaired HIGH |
|---|---|---|---|---|
| R1 | 0 / 12 / 13 / 6 (pre-validation) | 10 HIGH | 10 | 10 |
| R2 | 0 / 6 / 24 / 8 | 5 HIGH | 5 | 15 |
| R3 | 0 / 5 / 17 / 7 | 4 HIGH | 4 | 19 |
| R4 | 0 / 1 / 4 / 0 | 1 HIGH | 1 | 20 |
| R5 | 0 / 0 / 6 / 0 | **0** | 0 | 20 |

New-detection yield in the final round: **1 new MEDIUM (R5-01); 0 new HIGH/CRITICAL**; the other 5 MEDIUMs are persisting/re-emitted items.

### 6.2 Validation waves and downgrade rates

| Wave | Round | Sent (C/H) | Confirm | Downgrade | Reject | Downgrade rate | Reject rate |
|---|---|---|---|---|---|---|---|
| W1 | R1 | 12 | 10 | 2 | 0 | 16.7% | 0% |
| W2 | R2 | 6 | 5 | 0 | 1 | 0% | 16.7% |
| W3 | R3 | 5 | 4 | 0 | 1 | 0% | 20.0% |
| W4 | R4 | 1 | 1 | 0 | 0 | 0% | 0% |
| **Total** | — | **24** | **21** | **2** | **2** | **8.3%** | **8.3%** |

Evidence-boundary completeness: **24/24** verdicts carry both `evidence_supported` and `evidence_not_supported` (waves 1–3 measured in the verdict files; W4 in the validator record). No R5 validation wave exists: 0 C/H → nothing to send by rule. Downgrades: W1-01 HIGH→MEDIUM, W2-02 HIGH→LOW (both wave 1); both remain in the carried inventory at their downgraded severities.

### 6.3 Detection passes that ran

| Round | Passes |
|---|---|
| R1 | W1: A–I incl. **D** constitution alignment and **H** checklist accountability · W2: A·B·C·E·F·G·I · W3: A·B·C·E·F·G·I · integration: **H** over both checklists + deterministic merge + read-only clause-coverage accounting |
| R2 | w1: A·B·C·E·F·G·I + **D** · w2a/w2b/w2c: A·B·C·E·F·G·I · w3: A·B·C·E·F·G·I · every worker also re-read the prior round's confirmed HIGH loci for adjudication |
| R3 | w1/w2a/w2b/w2c/w3: A·B·C·E·F·G·I + prior-HIGH adjudication |
| R4 | one worker, three files + one-hop: A·B·C·E·F·G·I + R3-HIGH adjudication |
| R5 | one worker, three files + one-hop: A·B·C·E·F·G·I + R4-01 adjudication |

Round-2/3 domain split (file-disjoint): **w1** requirements + both checklists + constitution + glossary · **w2a** plan + data-model · **w2b** settlement-contract + enforcement-and-migration contract · **w2c** carrier-conformance contract + quickstart + research · **w3** tasks + feature-ref + handoff + coverage-baseline + team + anchor. Zero-finding floor never applied — every round produced findings.

### 6.4 Scale and invariants across the whole chain

41 FR · 9 SC · 4 STR · 34 contract clauses (12 + 10 + 12 by file: settlement 12, carrier-conformance 10, enforcement-and-migration 12) · 37 tasks · 9 entities · 12 invariants — all unchanged across the four repairs. FR claim rate 37/41 (FR-036/037/039/040 uncited) is unchanged from the tasks-stage freeze; its one 106-specific component remains finding W3-08.

## 7. Gate disposition and next actions

1. **Analyze gate PASS** → `/speckit.implement` may start.
2. **Residual MEDIUMs (6)** sit on the settlement-engine contract surfaces: malformed-row definition (R5-01), evidence-vs-violation predicate (R5-02), live C2/C4 branch (R5-03), behavior-class set vs tags (R5-04), edge kinds in settle output (R5-05), E9 reaction-record surface (R5-06). None blocks; their disposition belongs to a downstream clarify/plan touch or the implement-stage contract tests, not to this pass.
3. **No further analyze repair is authorized by this pass.** The earlier MEDIUM/LOW inventory in §5.2 remains recorded without disposition.
4. **Records commit**: this report, the round-4/5 finding files, the round-2/3/4 verdict copies, and the reused-domain hash copy land together as a records-only commit — no spec artifact is edited.

## 8. Run notes

- **Anomaly**: `未发现异常` — no decision-class anomaly in this integration pass.
- **In-passing disclosures (corrections, not decisions)**:
  1. **Hash-scope correction**: the persisted reused-domain hash record is W1-domain-only (four files), while the dispatch briefs describe "W1/W3 reused with hashes". This report records the file's actual scope and the W3 evidence bound (§3) instead of repeating the broader claim. No file was edited.
  2. **Round-2 W2 execution**: a single W2 worker attempt hit its output-token limit and produced no findings file; the round-2 W2 reading is the three file-disjoint sub-domains w2a/w2b/w2c. The abandoned log remains in git-ignored `.specify/state/`.
  3. **Round-4 verdict extraction**: the W4 validator output existed only inside the git-ignored raw log; its verbatim verdict object is extracted to `test-evidence/validate-r4-01.verdicts.json` so the verdict is committable without bypassing `.specify/state/`'s ignore rule (same precedent as the wave-1 copy).
  4. **No re-execution**: every structural-check reading in §2.5 is quoted from the repair records; this pass did not re-run detection, validators or coverage, by instruction. The only verification newly executed here is the `sha256sum` comparison in §3.
- **Read-only proof for the report itself**: no spec artifact was edited; the only writes are this report and the evidence copies committed with it.

## 9. Evidence index

| Evidence | Path |
|---|---|
| Round-1 report (gate FAIL, 10 HIGH) | `test-evidence/analyze-report-2026-11-25.md` |
| Round-1 domain findings | `test-evidence/analyze-domain-w1.jsonl`, `-w2.jsonl`, `-w3.jsonl` |
| Round-2 domain findings | `test-evidence/analyze-domain-{w1,w2a,w2b,w2c,w3}-r2.jsonl` |
| Round-3 domain findings | `test-evidence/analyze-domain-{w1,w2a,w2b,w2c,w3}-r3.jsonl` |
| Round-4 findings | `test-evidence/analyze-incremental-r4.jsonl` |
| Round-5 findings (final) | `test-evidence/analyze-incremental-r5.jsonl` |
| Validation wave 1 (12 verdicts) | `test-evidence/validate-wave1.verdicts.json` |
| Validation wave 2 (6 verdicts) | `test-evidence/validate-wave2.verdicts.json` (copy of `.specify/state/validate-wave2.verdicts.json`) |
| Validation wave 3 (5 verdicts) | `test-evidence/validate-wave3.verdicts.json` (copy of `.specify/state/validate-wave3.verdicts.json`) |
| Validation wave 4 (R4-01) | `test-evidence/validate-r4-01.verdicts.json` (extracted from the validator's final message) |
| Repair 1–4 records | `test-evidence/analyze-repair-2026-11-25.md`, `analyze-repair2-2026-11-25.md`, `analyze-repair3-2026-11-25.md`, `analyze-repair4-2026-11-26.md` |
| Reused-domain hashes | `test-evidence/analyze-r4-reused-domain-hashes.txt` (copy of `.specify/state/analyze-r4-reused-domain-hashes.txt`) |
| Repair structural checks | `test-evidence/analyze-repair{2,3,4}-{requirements-validator,tasks-validator,pre-analyze-*,clause-extract,clause-coverage,gate-scan,glossary-validate}*` |
| Round-4/5 dispatch briefs and worker logs (git-ignored) | `.specify/state/prompt-background-silent-failure-analyze-r{4,5}.md`; `log-background-silent-failure-analyze-r{4,5}.log`; `log-background-silent-failure-validate-r4-01.log` |
