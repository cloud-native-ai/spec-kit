# Plan Re-review Stage Record — 107-decision-governance

- **Stage**: plan · re-review (route 3.5(a), after the analyze-gate substantive PLAN-EDITs) · attempt 2 · 2026-11-26
- **Line / run**: `decision-governance` / `r20261125T173500Z-107c`
- **Baseline commit**: `62815af79` (branch `107-decision-governance`; worktree `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-governance`)
- **Assignment**: consistency re-review of the plan-owned set against the repaired requirements/contracts — layered record grammar (10 base fields + same-name / supersession / transmission families), conditional timepoints by phase, M-01/M-02 conditions, C-202/C-401; update stale pointers/counts; re-run the 23-row Constitution Check, Decision Tensions and Execution Premises; deterministic gates, targeted-set E3 row, wrap-up accounting.
- **Execution class**: direct; no subagents dispatched; no user questions; no state-spine writes; no push.
- **Concurrency reading**: `requested=1`, `effective=not_evaluated`, `effective_reason=single-unit` (a single bounded unit has no dispatch/settle interval pair; `single-unit` is a member of `shared/declarations/facts/serial-reason.yaml`).

## 1. Authority and reviewed surface

- **Repaired authority (non-plan-owned, read-only to this dispatch)**: `requirements.md` FR-014 (a: 10-field base layer; b: three conditional families by trigger), Field Ownership table (19 rows = 10 base + 8 conditional + 1 dimension row), M-01/M-02 rows, SC-005, Clarifications 2026-11-26 round 2; `tasks.md` T023/T026/T029, DoD-4, US3 (already repaired at `d33319fa7`).
- **Plan-owned set reviewed**: `plan.md`, `data-model.md`, all 5 contracts, `quickstart.md`, `research.md`, `feature-ref.md`.
- **Prior substantive PLAN-EDITs verified present** (declared at `d33319fa7`; no re-edit needed):
  - `data-model.md` E2 is a layered table — base=10, condition=6, total=16 rows; the field-closure paragraph is authoritative and delegates value domains to the owner page; I-03 reads "base present on every record; each conditional field exactly when its trigger holds; timepoints follow the phase".
  - `contracts/archive-and-audit.contract.md` C-202 states the layered closure and phase-driven timepoints; acknowledgement/`implementation_receipt` are return items, not record fields.
  - `contracts/enforcement-boundary.contract.md` C-401 M-01 red condition = missing base-layer field / conditional field missing while its trigger holds / class outside the set / `transmission_status` outside its domain / malformed or phase-contradicting timepoint; M-02 scoped to the same-name conditional family.
  - `contracts/transmission-and-implementation.contract.md` C-303/C-304 drive `acknowledged_at` / `implemented_at` and the status phase per C-202.

## 2. Findings → Changes (5/5, all minor)

| # | Finding | Change (file:location) | Evidence | Classification |
|---|---------|------------------------|----------|----------------|
| 1 | `plan.md` Constitution row IV cited a non-existent section ("§ Enforcement below") | Pointer corrected to "§ Project Structure test map; `contracts/enforcement-boundary.contract.md` C-401/C-403" | `grep '§ Enforcement below' → 0`; plan.md heading inventory has no Enforcement section | minor |
| 2 | `plan.md` § Project Structure test map listed guards as "M-02/M-05/M-06/M-07/M-08" — omits M-09, whose traceability test (`test_broken_pointer_red`) lives in the guards file | Added `/M-09` to the guards line | `contracts/archive-and-audit.contract.md` traceability C-204 → guards::`test_broken_pointer_red`; `tasks.md` T024 bundles the M-09 fixture | minor |
| 3 | `data-model.md` I-08 rule source read "FR-013, M-… replay" — a placeholder, and no M rule owns replay | Rule source corrected to "FR-013, C-107" | FR-013 owns replayability; C-107 owns the replay obligation and maps to `test_ai_replay_deterministic`; no M row judges replay | minor |
| 4 | `research.md` R-3 said "three actions" while naming four (records / payload / chain / inventory) and plan T-003 says four | Count corrected to "four actions" | plan.md T-003 "四个 action"; C-401 judge column uses all four | minor |
| 5 | `quickstart.md` Scenario 5 said "delete one field → M-01 red" — under the layered grammar a non-applicable field is not a defect | Rewritten to "delete one applicable-layer mandatory field", plus the four-carrier non-transmission note | SC-005 reading ("适用层全部字段；四类载体均非传输生产者，只判基础层与到场条件族") | minor |

No substantive PLAN-EDIT was required; the analyze-gate repairs already hold across the plan set.

## 3. Consistency matrix (plan-owned vs repaired authority)

| Artifact | Reading | Verdict |
|----------|---------|---------|
| `plan.md` Summary / Scale/Scope | "red-first guard fixtures for M-01…M-09"; 9 machine rules, 6 behavior rules, 12 producers, 6 BC rows, 21 landing files (+6 test suites), 5 contracts | consistent |
| `plan.md` Constitution Check | 23 rows for constitution v1.20.0's 23 principles; row IV pointer repaired; no status change | consistent |
| `plan.md` Decision Tensions | 3 records (`T-001…T-003`), registered `T-019…T-021`; T-002 governs serialization form, unaffected by the layered-closure repair | consistent |
| `plan.md` Execution Premises | 7 rows; EP-005 falsified + `resolve-in-scope` retained; EP-006 substance re-verified (§ 6) | consistent |
| `plan.md` BC inventory | BC-01…BC-06 closed; BC-01/BC-03 use the C-201 + C-206 discriminator; BC-02 refusal = M-06 | consistent |
| `data-model.md` | 9 entities; E2 16 rows (10 base + 6 conditional); 14 invariants (I-03 layered, I-08 fixed, I-12 `superseded_by`, I-13 legacy); 1 state domain (E9, 6 values) | consistent |
| `contracts/` (5 files) | 38 clauses: C-101…C-109 (9), C-201…C-208 (8), C-301…C-308 (8), C-401…C-407 (7), C-501…C-506 (6); C-401 has exactly 9 M rows, each with one judge action, one red condition and one reverse sample | consistent |
| `quickstart.md` | 6 scenarios; S1 layered authoring; S5 applicable-layer reconstruction (fixed) | consistent |
| `research.md` | 16 baseline measurements (M-1…M-16) + 8 resolved design points (R-1…R-8); R-2 layered closure, phase timepoints, no `not-yet` placeholder; R-3 four actions (fixed) | consistent |
| `feature-ref.md` | 21 delivery files match plan § Project Structure (non-test) exactly; § 5 BC inventory matches; § 6 handoff keeps its stage-time phrasing (live handoff is `handoff.md`) | consistent |

## 4. Constitution Check re-run (all 23 rows)

Rendered from `.specify/constitution.md` v1.20.0 (live roster: 23 principles, I…XXIII; plan table rows: 23). **All 23 rows remain ✅ Pass; no row changed status.** Rows whose evidence touches the repaired grammar were re-verified in detail:

| Row | Re-check |
|-----|----------|
| IV | C-401 now has 9 judge/red/reverse rows; C-403 pins reverse samples; row evidence pointer corrected (finding 1). Pass |
| VI | Machine/behavior split intact; legacy reported, never skipped; no `.bak` practice. Pass |
| XIV | Single owner page; Field Ownership 19 rows layered (10+8+1); adjacent owners pointer-only. Pass |
| XVI | Silent re-decision = explicit anomaly; invalidation stops at the anomaly point (C-305/C-308). Pass |
| XXI | Checker interface obligations unchanged (C-404); read-only. Pass |

Other rows re-verified against the unchanged design (no drift introduced by the analyze repairs). **Gates status: all 23 pass; Complexity Tracking N/A.**

## 5. Decision Tensions re-validation

`python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/107-decision-governance` → `status: ok`; 6/6 checks pass (anchor, section, record completeness, tension id, rejected form, expected-sacrifice mapping); `scanned: 217 lines, 3 record(s)`; `0 error(s), 0 warning(s)`; exit 0 — `test-evidence/plan-rereview-validate-decision-tensions.txt`.

- T-001 (whole-section landing + budget ruling 38,912 → 40,960) unchanged; reopen condition intact.
- T-002 (heading + single-line field grammar, not fenced blocks) unchanged — the layered-closure repair changes membership/requiredness, not serialization form.
- T-003 (independent read-only checker with four actions) unchanged; register rows `T-019…T-021` still map to these records.

## 6. Execution Premises re-check

| ID | Status after re-review | Re-measured evidence (2026-11-26) |
|----|------------------------|----------------------------------|
| EP-001 | verified | `pyproject.toml: requires-python = ">=3.8"`; `scripts/bash/run-tests.sh` `resolve_python()` ladder (SPECKIT_PYTHON → .venv → python3 → python) present |
| EP-002 | verified | `shared/definitions/superagent-definitions.md` § Downlink: seven role fields + four injections unchanged |
| EP-003 | verified | `scan-confirmation-gates.py`: 31 blocking gates (23 destructive / 7 governance-kept / 1 reversible), 0 violations; `SCAN_DIRS = ("templates/commands", "skills", "shared")` covers the new owner page |
| EP-004 | verified | `sync-mirrors.py --check` rc 0 (6 pairs; `shared/` 116 files byte-identical); `regen-command-copies.py --check` rc 0 |
| EP-005 | **falsified — retained** | Premise "bullets inside an existing section would reach initialized projects" stays falsified; decision `resolve-in-scope` = land a whole new section (T-001) |
| EP-006 | verified (substance); one numeral caveat | 101 `T-NNN` headings at base, 127 checkpoint files at base, 39 pre-existing `### D-…` headings live (one/two-digit forms), **0** three-digit record-form headings, 0 deleted corpus lines / 0 deleted files vs `08b59695c`. Caveat: the descriptive count "43 run reports" does not reproduce from a single stated basis (candidates: 41 `.specify/teams/**/runs/*-report.md` + 2 `.specify/specs/**/analyze-rerun-report.md` = 43; `.specify/specs/**/*-report.md` = 14; whole repo = 77). Non-load-bearing; not edited in this dispatch (choosing a counting basis would be an adjudication). Disclosed for the analyze/review flow |
| EP-007 | verified | Live `.specify/instructions.md` = 38,894 B; `INSTRUCTIONS_BUDGET_BYTES=38912`; generator reports `over` at `size >= budget` |

## 7. Deterministic gates (all captured under `test-evidence/plan-rereview-*`)

| Gate | Command | Reading |
|------|---------|---------|
| Pre-analyze (plan) | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/107-decision-governance --stage plan --repo .` | `decision=pass errors=0 advisories=127 waived=0`, exit 0; summary fr=30 / sc=10 / tasks=56 / clauses=38 / files=14; advisory split 48 `external-clause` (BC-NN external namespace) + 79 `missing-path` (deliverables land at implement) — identical composition to the analyze-repair2 baseline — `plan-rereview-pre-analyze-plan.txt` |
| Decision-tension validator | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/107-decision-governance` | `status: ok`; 0 error / 0 warning; 3 records, 217 lines — `plan-rereview-validate-decision-tensions.txt` |
| Plan integrity + consistency counts | template-integrity tokens; closed-set counts; stale sweep; containment | placeholders 0 / H1 1 / stamp 1 / template note 0; constitution 23=23; M 9=9 (C-401); B 6; P 12; FR 30; SC 10; STR 9; clauses 38; E2 16 (10+6); invariants 14; Field Ownership 19 (10+8+1); delivery 21 = landing 21 (+6 test suites); stale sweep all 0 (`not-yet` only as the prohibition sentence); containment 0 deleted lines / 0 deleted files — `plan-rereview-integrity.txt` |
| Gate scan | `python3 scripts/python/scan-confirmation-gates.py` | 31 blocking gates / 0 violations (same as baseline) |
| Workspace signature | `workspace-guard.py --snapshot` … `--check` | before `recorded`; after `status: clean`, `changed: []`, rc 0 — `workspace-plan-rereview-before.json` / `workspace-plan-rereview-after.json` |

## 8. Test budget (E3)

- **Program**: `targeted-set-v1` (TB-05) with `stage_base=62815af79`.
- **Input**: 9 changed paths — the four repaired plan-owned files and five test-evidence files, all documentation under `.specify/specs/107-decision-governance/`; **0 executable or test paths changed**.
- **Selection output**: 586 candidates; (a) 239 stem/path matches; (b) 31 delivery-surface contract/integration matches; 256 deduped (dominated by the generic `plan`/`research` stems) — informational only because no executable surface changed — `plan-rereview-targeted-set.txt`.
- **Status**: `not-run-docs-only` (TB-06 docs-only clause), six reduced fields recorded in `test-evidence/plan-rereview.jsonl`. No full suite, no slot consumed.

## 9. Disclosures (recorded, not silently repaired)

1. **Base duality** — requirements FR-028/SC-009 cite the requirements-stage base `fbab7a45c`; plan EP-006 and C-502 cite the plan-stage base `08b59695c`. Both are stage-time readings; this was disclosed in `analyze-repair-2026-11-26.md` § 5(3) and the implementation zero-rewrite test follows C-502's `08b59695c`. Unchanged by this re-review (unifying the bases would be an adjudication).
2. **EP-006 "43 run reports"** — measurement-basis gap as described in § 6; the premise's substantive claims and the containment reading hold.
3. **`feature-ref.md` § 6** retains its plan-stage "Next stage: `/speckit.tasks`" phrasing; tasks.md has since landed and was reconciled at `d33319fa7`. The live handoff contract is `handoff.md`; § 2/§ 3 delivery surfaces were re-verified against plan § Project Structure (21 = 21).
4. **Dated records are immutable** — the plan-stage record's "8 machine rules" line and the analyze reports' prior wording are dated history, not rewritten here (only live artifacts were repaired).

## 10. Anomaly line

未发现异常。Five minor PLAN-EDITs were made and are disclosed above; the EP-006 numeral gap and the base duality are recorded disclosures, not decision-requiring anomalies (neither is load-bearing for any premise, contract or test). No destructive action, no dirty-file touch, no state-spine write, no push.

## 11. Re-anchoring record

- After brief + role template + authority artifacts: `on-track`.
- After the plan-set consistency sweep and the repaired-grammar cross-read: `on-track`.
- After the five PLAN-EDITs and gate re-runs: `on-track`.
- After the premises re-check (EP-006 numeral exploration) and the decisions to record-not-edit: `correction-applied` (two candidate bases investigated; two disclosures recorded; no invented measurement basis).
- After wrap-up accounting: `on-track`.

## 12. Wrap-up accounting

- **Run Determination**: `run-determination.py --action determine --unit-id skill:create-plan --unit-type skill --run-id r20261125T173500Z-107c --complexity complex --feature 107-decision-governance --feature-id 107 --prev-user-turn-class no_user_input` → record under `.specify/session/`; axes recorded in the close-out receipt.
- **Exec Quant**: `exec-quant.py --action collect --unit-id skill:create-plan --unit-type skill --run-id r20261125T173500Z-107c`.
- **Feedback Record**: `feedback-utils.py --action record --unit-id skill:create-plan --unit-type skill --run-id r20261125T173500Z-107c --feature 107-decision-governance --feature-id 107` (review + points below).
- **Points**: (1) `token-efficiency` — TB-05's stem rule stays noisy on docs-only stages (256 candidates for zero executable changes); a docs-only short-circuit remains the optimization candidate. (2) `token-efficiency` — a plan re-review can start from the analyze-repair's file list and targeted greps instead of re-reading all five contracts in full.
- **Close-out receipt**: `.specify/retention/closeout/` (records commit reference inside).

## 13. Evidence pointers

- Plan set: `plan.md`, `data-model.md`, `contracts/` (5), `quickstart.md`, `research.md`, `feature-ref.md`
- Gates/e3: `test-evidence/plan-rereview-{pre-analyze-plan.txt, validate-decision-tensions.txt, integrity.txt, targeted-set.txt, .jsonl}`
- Workspace: `test-evidence/workspace-plan-rereview-{before,after}.json`
