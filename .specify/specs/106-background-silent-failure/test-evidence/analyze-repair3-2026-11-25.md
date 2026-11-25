# Analyze-Repair3 Record — 106-background-silent-failure — 2026-11-25

- **Trigger**: analyze round 3 produced validator-confirmed HIGH findings in domains w2a/w2b; **4 are in this repair's authorized set** — R3-W2A-01, R3-W2A-02, R3-W2B-01, R3-W2B-02. Every other round-3 finding (MEDIUM/LOW, including R3-W2A-03…06, R3-W2B-03…06, R3-W2C-01…06, R3-W1-01…06, R3-W3-01…05) is **outside this dispatch** and was not repaired.
- **Route**: analyze-gate autonomous upstream repair (round 3). Authority: the dispatch's 4-finding set; no user questions (unattended).
- **Unit / run**: `skill:analyze-artifacts` · `r20261125T134017Z-106r3` · feature key `106-background-silent-failure`.
- **Scope discipline**: only live spec artifacts and their records were edited. Dated records (`checklists/background-settlement-2026-11-25.md`, earlier `test-evidence/*`) were **not** rewritten; the untracked round-2/round-3 findings JSONL files were left untouched and are not part of this repair's commit. FR ids (41), SC ids (9), STR ids (4) and all 34 contract clause ids are unchanged; the closed settlement value set, sentinel literals, watcher verdicts/exit codes, five-element uplink, seven-field downlink, confirmation discipline and the two-slot budget are untouched. No code, test, carrier script or requirement was edited.
- **Concurrency reading**: requested=1 · effective=not_evaluated · effective_reason=single-unit (A-17: one executor, single leaf, no dispatch).

## 1. Finding → change → evidence map

### R3-W2A-01 — `INV08` (legacy never causes a failing exit) vs `E7`'s `settlement-unbacked` / `settlement-out-of-set` applying to any recorded value

- **Reconciliation chosen**: legacy = **annotated, not judged**. All three E7 violation predicates are scoped to **version-bearing** records (a claim/record carrying `settlement_version`); a versionless record is annotated `legacy`, exempt from all three, and therefore contributes no exit 1. The exit-2 `unknown` refusal stays a **detection defect, not a judgment**, so it keeps applying regardless of version (matching quickstart S-4's "unreadable evidence in either fixture exits 2").
- **Change**:
  - `data-model.md:97-98` (E7) — `settlement-out-of-set` and `settlement-unbacked` predicates now read "on a version-bearing record".
  - `data-model.md:100` (E7) — new **Legacy scope** paragraph: all three predicates apply only to version-bearing records; the 5-column exemption in `settlement-unrecorded` is this scope's table-level instance.
  - `data-model.md:102` (E7) — the `unknown` paragraph states the legacy annotation never suppresses the exit-2 refusal.
  - `data-model.md:74` (E5 `settlement_version`) — "annotated `legacy`, never counted as compliant, never rewritten, and not judged by any E7 predicate (so it contributes no exit 1)".
  - `data-model.md:137` (INV08) — rewritten to the same three-predicate exemption + the exit-2 boundary.
- **Evidence**: the three surfaces (E5 row, E7 table + scope, INV08) now state one reading; the contract twin C-33 was qualified in the same round (R3-W2B-01) so exit 0/1/2 is decidable for a legacy fixture. `validate-requirements` 0/0, pre-analyze 3 stages pass.

### R3-W2A-02 — C2 has no E4 completion-verification slot and `<label>.settlement` has no declared writer

- **Reconciliation chosen**: C2's E4 mechanism is the existing closed-set value **`return-record`** — the parent verifies the child's declared-equivalent return and records the resolvable evidence pointers in its `<label>.settlement` claim. The claim writer is the **parent** (`dispatch.sh` writes only `.attempt`/`.end`; the engine is read-only), and the file lives beside `.attempt`/`.end` in the carrier's existing evidence directory — **no new storage root**. A missing claim blocks `completed` (INV02) but not verdict derivation.
- **Change**:
  - `data-model.md:56` (E4 `mechanism`) — each mechanism now names its carrier; `return-record` names C2's read slot (parent-written `<label>.settlement` claim, child's returned artifact pointers).
  - `data-model.md:60` (E4) — closed mechanism↔carrier mapping (`u4`→C1, `return-record`→C2, `team-verification`→C3, `five-element`→C4; C6 only through a compliant C1/C2 runner) + writer sentence.
  - `data-model.md:70` (E5 `surface`) — `attempt-file` writer declared: only the parent, after its independent verification; same existing evidence directory as E2/E3; `team-report-row` writer is the team run.
  - `data-model.md:109` (E8 C2 row) — "optional parent-written `.settlement` claim"; the written-by cell scopes `dispatch.sh` to attempt/end only.
- **Evidence**: research `R-03` already records "A parent may add `<label>.settlement` (a claim with verdict + evidence pointers + version) after independent verification" — the repair grounds the data model in that recorded decision rather than inventing a mechanism; the E4 mechanism set stays the closed four values of FR-002/C-02 (no new value, no requirements edit); C-15's "verified return" now has a named mechanism and read slot; B-13 keeps the location inside the already-ignored dispatch log directory.

### R3-W2B-01 — `C-33`'s unqualified "MUST NOT cause a failing exit code" vs `C-26`'s exit-1 duty

- **Reconciliation chosen**: qualify C-33 exactly as the design implies — legacy records are annotated, **not judged**; settlement violations on **version-bearing** records keep exit 1 (C-26); the `unknown` exit-2 refusal is a detection defect and applies regardless of `settlement_version`.
- **Change**: `contracts/enforcement-and-migration.contract.md:42` (C-33) — the sentence now names the three-predicate exemption, keeps C-26's exit-1 duty for version-bearing records, restates the 5-column row as the table-level case ("contributes no failing exit code" instead of the locally-true-but-ambiguous "exits 0"), and scopes the exit-2 refusal.
- **Evidence**: C-26 unchanged (exit 0/1/2 semantics preserved); C-10's "annotation alone does not produce a failing exit code" remains true and narrower than the new C-33 text, so no second qualifier is needed; quickstart S-4's exit-2-on-either-fixture statement and S-3's legacy exit-0 statement remain consistent; T029's "legacy 标注不影响退出码" remains consistent.

### R3-W2B-02 — `C-34`'s closed behavior-class set omits FR-024 (C-08) and FR-010 (C-06)

- **Reconciliation chosen**: **fix the set**, not the tags — C-06 and C-08 are genuinely behavior-class in these duties, so removing the tags would soften the honesty boundary. The closed set gains FR-010 (parent's attempt-record writing and the return-channel-silence reading) and FR-024 (named-diagnosis-or-user-ruling precondition on `silent-end`/`unknown` retries); it stays an explicit closed enumeration (now ten items).
- **Change**:
  - `contracts/enforcement-and-migration.contract.md:46` (C-34) — set updated with the two entries.
  - `tasks.md:271` (T032) — "（C-34 列出的八项）" → "（项数以 C-34 的封闭集合为准，不在此复述）": pointer-only, so the task no longer restates a count that the set now changes (One Source Of Truth).
- **Evidence**: every clause tagged *behavior-class … discharge* whose FR was missing from the set is now enumerated; `grep -rn "八项"` over the live spec artifacts shows no remaining C-34 count (the one hit in the dated checklist refers to the checklist's own eight dimension clusters and is not rewritten); DoD-3/DoD-7/§ Gate rows already use pointer form ("C-34 列举的集合").

## 2. PLAN-EDIT declarations (analyze-driven defect fixes, not intent changes)

| Plan-owned file | Declaration | Classification |
|---|---|---|
| `data-model.md` | `PLAN-EDIT: data-model.md — R3-W2A-01/R3-W2A-02: E7's three predicates scoped to version-bearing records with a Legacy-scope paragraph, E5/INV08 aligned (no exit-1 contribution; exit-2 detection refusal kept version-independent); E4 names its mechanism↔carrier mapping with `return-record` as C2's read slot; E5 declares the parent as the sole writer of `<label>.settlement` (existing evidence directory, no new root); E8 C2 row aligned` | **minor** — additive scoping/declarations on existing entities; 9 entities / 12 invariants retained |
| `contracts/enforcement-and-migration.contract.md` | `PLAN-EDIT: contracts/enforcement-and-migration.contract.md — R3-W2B-01/R3-W2B-02: C-33 qualified (legacy annotated not judged; version-bearing violations keep exit 1 per C-26; exit-2 detection refusal version-independent); C-34's closed behavior-class set gains FR-010 and FR-024; clause ids unchanged` | **minor** — the exit-code semantics and the closed-set mechanism are unchanged; the set gains two already-tagged duties |
| `tasks.md` | `PLAN-EDIT: tasks.md — R3-W2B-02 follow-through: T032's "C-34 列出的八项" becomes a pointer to C-34's closed set (no count restated); task count/order/claims unchanged` | **minor** — pointer-only |

**Registry (not plan-owned)**: `.specify/features.md` row 106 gained the analyze-repair3 event line; status stays `Planned`; parent 095 stays `Ready for Review`. **Not touched**: `requirements.md`, `research.md`, `feature-ref.md`, `plan.md`, `quickstart.md`, `handoff.md`, `contracts/settlement-contract.contract.md`, `contracts/carrier-conformance.contract.md`; the dated checklist was not rewritten.

## 3. Verification (commands and results)

| Check | Command | Result | Evidence |
|---|---|---|---|
| Requirements structure | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/106-background-silent-failure/requirements.md` | rc 0 — **0 error / 0 warning**; 312 lines, 50 definition rows, 4 shared strings | `test-evidence/analyze-repair3-requirements-validator.txt` |
| Tasks structure | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/106-background-silent-failure/tasks.md` | rc 0 — PASS, **0 error / 0 warning** | `test-evidence/analyze-repair3-tasks-validator.txt` |
| Cross-artifact (requirements) | `pre-analyze-check.py --spec-dir … --stage requirements --repo .` | rc 0 — `decision=pass`, **errors=0**, advisories=55 (all expected missing-path of the planned new tests/fixtures), waived=0; fr=41 sc=9 tasks=37 clauses=34 | `test-evidence/analyze-repair3-pre-analyze-requirements.txt` |
| Cross-artifact (plan) | same, `--stage plan` | rc 0 — `decision=pass`, errors=0, advisories=55, waived=0 | `test-evidence/analyze-repair3-pre-analyze-plan.txt` |
| Cross-artifact (tasks) | same, `--stage tasks` | rc 0 — `decision=pass`, errors=0, advisories=55, waived=0 | `test-evidence/analyze-repair3-pre-analyze-tasks.txt` |
| Decomposition | `decomposition-check.py --mode tasks --requirements … --tasks …` | rc 0 — `decision=proceed` (fr 41 / tasks 37; ceilings 120/160) | `test-evidence/analyze-repair3-decomposition.txt` |
| Clause extract | `clause_extract.py contracts/*.md` | 3 files, `form=md-bold-closed`, **34 clauses** (12/12/10), ids unchanged | `test-evidence/analyze-repair3-clause-extract.json` |
| Clause coverage accountant | `scripts/python/account-clause-coverage.py --spec-dir …` | rc 1 with output **byte-identical** to the frozen r2 reading (`cmp` equal): claimed clauses 34, `clause-uncovered` beyond-baseline **0**, `fr-uncovered` 37/41, `clause-unparsable` 111 (documented structural verdict, not a pass criterion — tasks GATE-3) | `test-evidence/analyze-repair3-clause-coverage.txt` |
| Gate scan | `python3 scripts/python/scan-confirmation-gates.py --root . --json` | byte-identical to the r2 reading: total **31** (governance_kept 7 / destructive 23 / reversible 1); **0 touched-file hits**; violations 0 | `test-evidence/analyze-repair3-gate-scan.json` |
| Glossary | `python3 .specify/scripts/python/glossary-utils.py --action validate` | `{"valid": true}` | `test-evidence/analyze-repair3-glossary-validate.txt` |
| Workspace guard (before) | `workspace-guard.py --snapshot …-analyze-repair3-before.json --repo .` then `--check` | snapshot recorded; `--check` → `clean` (rc 0) | `test-evidence/workspace-snapshot-analyze-repair3-before.json`, `workspace-check-analyze-repair3-before-commit.txt` |
| Run determination | `run-determination.py --action determine --unit-id skill:analyze-artifacts --run-id r20261125T134017Z-106r3 …` | recorded; four axes `not_evaluated` with named reasons; `trigger_feedback: false`; change point `cp-r20261125T134017Z-106r3`; previous run settled `not_evaluated` | `test-evidence/run-determination-analyze-repair3.txt`; `.specify/session/20261125T134017Z-run-determination-skill-analyze-artifacts-r20261125t134017z.md` |
| Exec quant | `exec-quant.py --action collect --unit-id skill:analyze-artifacts --run-id …` | recorded → `.specify/exec-quant/records/20261125T134020382137Z-dc4a1b7c.json` | `test-evidence/exec-quant-analyze-repair3.txt` |
| Feedback record | `feedback-utils.py --action record …` | entry `20261125T134023Z-skill-analyze-artifacts` (`should_prompt: true`, count 564 vs threshold 10; no packaging/transmission — `trigger_feedback: false`) | `test-evidence/feedback-record-analyze-repair3.txt`; `.specify/feedback/20261125T134023Z-skill-analyze-artifacts.md` |

## 4. Preserved surfaces

- Closed settlement set `completed` / `failed` / `anomaly` / `cancelled` / `running` / `silent-end` / `unknown`, the three violation kinds and the four E4 mechanism values: unchanged (the E4 fix maps an existing value to C2; it adds none).
- Sentinel literals, watcher verdict tokens/exit codes/`--self-test`, five-element uplink, seven-field downlink, destructive-action discipline, confirmation-gate budget, two-slot test budget: unchanged; `watch-target.sh` not edited; zero tests collected or run.
- FR/SC/STR ids and all 34 clause ids unchanged; no task added/removed/renumbered; no new carrier, store, root or engine.

## 5. Assumptions (unattended; no user adjudication)

1. **C2's E4 mechanism is `return-record`** — FR-002's closed four-value set has no carrier-specific name for C2's "已核验返回", and `return-record` ("申报等价返回") is the value whose recorded meaning (a parent-verified declared return) matches C-15's C2 rule; assigning it in E4 (the set's co-owner per FR-002) keeps the requirements' closed set untouched.
2. **The `.settlement` claim is the parent's** — research R-03 already places its writing "after independent verification" on the parent; `dispatch.sh` writing it would contradict C-14 (`.attempt`/`.end` only) and the parent-side settlement model.
3. **The behavior-class set fix was preferred to tag removal** — C-06's recording/silence-reading duty and C-08's retry-diagnosis duty are not machine-assertable, so removing their tags would misstate the honesty boundary (FR-041).

## 6. Residual risk / open items

- **Quickstart behavior-class naming**: C-34 requires behavior-class clauses to be "named as such in the contracts and quickstart", but quickstart currently names none. This is outside the authorized 4-finding fix surface (a quickstart edit was not required to fix the set) and is recorded here for the next analyze round rather than repaired silently.
- R3-W2A-02 defines `return-record` only at C2's read-slot level; the pre-existing round-1 MEDIUM W2-06 (`return-record`'s general admissibility beyond C2) remains broader than this repair.
- Rejected round-2 finding `w2c-03` (C-15's "completion declaration" vs R-03's optional `.settlement`) remains open; the new E4 sentence ("a missing claim blocks `completed`, not verdict derivation") narrows the ambiguity without rewriting C-15.
- The other clauses tagged *behavior-class …* (C-13/C-15/C-17/C-20) map their behavioral components onto the nearest closed-set entries (FR-005/FR-010/FR-011/FR-027); if a later round reads them as separate duties, that is a new finding against C-34.
- All other round-3 findings (MEDIUM/LOW) and earlier unresolved MEDIUM/LOW findings remain open by design.
- The coverage accountant's rc 1 (`fr-uncovered` 37/41, `clause-unparsable` 111) is the documented structural verdict, byte-identical to the frozen reading; it is reported honestly and not used as a pass criterion.

## 7. Fast-fail anomaly line

未发现异常 — no decision-class anomaly and no in-passing correction was needed; every edit is the authorized repair of the 4 confined findings.
