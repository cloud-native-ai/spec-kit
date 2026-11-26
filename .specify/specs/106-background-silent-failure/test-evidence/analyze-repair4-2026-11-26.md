# Analyze-Repair4 Record — 106-background-silent-failure — 2026-11-26

- **Trigger**: analyze round 4 (incremental) produced five findings in `test-evidence/analyze-incremental-r4.jsonl`; **1 is validator-confirmed HIGH and is this repair's authorized set** — R4-01. Every other round-4 finding (R4-02…R4-05, all MEDIUM) is **outside this dispatch** and was not repaired.
- **Route**: analyze-gate autonomous upstream repair (round 4). Authority: the dispatch's 1-finding set; no user questions (unattended).
- **Unit / run**: `skill:analyze-artifacts` · `r20261125T173750Z-106r4` · feature key `106-background-silent-failure`.
- **Scope discipline**: only live spec artifacts and their records were edited. Dated records (`checklists/background-settlement-2026-11-25.md`, earlier `test-evidence/*`) were **not** rewritten; the untracked round-4 findings JSONL file was left untouched and is not part of this repair's commit. FR ids (41), SC ids (9), STR ids (4) and all 34 contract clause ids are unchanged; the closed settlement value set, violation kinds, sentinel literals, watcher verdicts/exit codes, five-element uplink, seven-field downlink, confirmation discipline and the two-slot budget are untouched. No code, test, carrier script or requirement was edited.
- **Concurrency reading**: requested=1 · effective=not_evaluated · effective_reason=single-unit (A-17: one executor, single leaf, no dispatch).

## 1. Finding → change → evidence map

### R4-01 — `E7`'s Legacy-scope sentence defines a version-bearing record as one "carrying `settlement_version`", but the E5 `team-report-row` shape has no such slot (C-16 makes a row version-bearing by its 7-column header versus the legacy 5-column header)

- **Reconciliation chosen**: the version-bearing test is **per claim shape** — a claim file (E5 `attempt-file`) is version-bearing iff it carries `settlement_version`; a team-report row (E5 `team-report-row`) carries no version slot and is version-bearing iff it is parsed under the **7-column header** (a 5-column row is legacy by schema). Consequences made explicit: a malformed 7-column row (empty `end_state`/`evidence`) is **`settlement-unrecorded` → exit 1**; a 5-column row is legacy → no exit-1 contribution. Ground: C-16 fixes the new report header at exactly 7 columns (`label | role | dispatch_duty | workspace | parent | end_state | evidence`), so the header arity *is* the row's additive version declaration, and FR-034 scopes the legacy annotation to "旧尝试/旧报告" (old attempts/old reports) — a new 7-column report is not one; the same clause's "MUST NOT 改动既有行格式" is what keeps rows out of a version-cell design.
- **Change**:
  - `data-model.md:74` (E5 `settlement_version`) — slot declared `attempt-file` shape only; the `team-report-row` shape's version-bearing test is the 7-column header (E7 Legacy scope; C-16).
  - `data-model.md:88` (E6 `legacy`) — boolean defined by the shape's test: claim file carrying no `settlement_version`; team-report row under the legacy 5-column header.
  - `data-model.md:96` (E7 `settlement-unrecorded`) — "versioned" → "version-bearing", with the 7-column row named as version-bearing by its header; the claim-file case now names "carrying `settlement_version`"; the 5-column exemption stands.
  - `data-model.md:100` (E7 Legacy scope) — the per-shape version test replaces "(a claim or record carrying `settlement_version`)"; a malformed 7-column row stays version-bearing (`settlement-unrecorded`, exit 1) while a 5-column row contributes none.
  - `data-model.md:137` (INV08) — the invariant states the per-shape test, the legacy set (claim file without `settlement_version`; 5-column-header row) and the malformed-7-column exit-1 consequence.
  - `contracts/carrier-conformance.contract.md:22` (C-16) — "Version-bearing for this claim shape is the header: a 7-column row has no `settlement_version` cell and its header arity is its version declaration, while a 5-column row is version-less by schema. A 7-column row with an empty `end_state`/`evidence` is `settlement-unrecorded` (exit 1)"; the legacy carve-out is unchanged.
  - `contracts/enforcement-and-migration.contract.md:42` (C-33) — opening now decides version-bearing per claim shape (C-16), names the malformed 7-column row as judged `settlement-unrecorded`, and exempts "records without a version declaration in their shape's form"; the three-predicate exemption, the exit-1-kept sentence (C-26) and the version-independent exit-2 refusal are unchanged.
  - `tasks.md:156` (T003, owner amendment) — the `settlement_version`/legacy scope now carries the per-shape version test, so the owner page cannot re-derive the generic rule.
  - `tasks.md:265` (T029, engine implementation) — the settle version/legacy row now reads version-bearing per shape (claim file by field, report row by 7-column header) and pins the malformed-7-column → `settlement-unrecorded` (exit 1) branch; task count/order/claims unchanged.
- **Evidence**: the six design surfaces (E5/E6/E7/INV08 + C-16/C-33) state one reading and cross-reference each other (C-16 → INV08/C-33; C-33 → C-16; E7 → C-16; INV08 → C-16); the two task rows that restate the rule downstream now carry it. `quickstart.md:80-82` (versioned row missing `end_state`/`evidence` → `settlement-unrecorded` exit 1; 5-column legacy → exit 0) and S-4 (attempt-file fixtures carry `settlement_version: 1`) are already consistent and needed no edit. Clause extraction still finds 34 clauses with unchanged ids; all validators/pre-analyze/decomposition gates pass (Section 3).

## 2. PLAN-EDIT declarations (analyze-driven defect fixes, not intent changes)

| Plan-owned file | Declaration | Classification |
|---|---|---|
| `data-model.md` | `PLAN-EDIT: data-model.md — R4-01: version-bearing made a per-shape test (claim file by settlement_version; team-report row by its 7-column header, 5-column = legacy); E5 slot scoped to attempt-file, E6 legacy defined per shape, E7 settlement-unrecorded + Legacy scope and INV08 aligned; malformed 7-column row = settlement-unrecorded exit 1; no other predicate/evidence semantics changed` | **minor** — scoping of an existing predicate definition; 9 entities / 12 invariants retained |
| `contracts/carrier-conformance.contract.md` | `PLAN-EDIT: contracts/carrier-conformance.contract.md — R4-01: C-16 states the 7-column header as the row's version declaration and the malformed-7-column exit-1 outcome; clause id, column set and legacy carve-out unchanged` | **minor** — adds the version test already implied by the header arity |
| `contracts/enforcement-and-migration.contract.md` | `PLAN-EDIT: contracts/enforcement-and-migration.contract.md — R4-01: C-33 decides version-bearing per claim shape (C-16), exempts "records without a version declaration in their shape's form", and names the malformed 7-column row as judged; clause id, three-predicate exemption and exit-2 boundary unchanged` | **minor** — qualifier text only; the exempt set and exit semantics are unchanged |
| `tasks.md` | `PLAN-EDIT: tasks.md — R4-01 follow-through: T003 (owner amendment) and T029 (engine version/legacy) carry the per-shape version test and the malformed-7-column exit-1 branch; task count/order/claims unchanged` | **minor** — precision only in the two rows that restate the rule |

**Registry (not plan-owned)**: `.specify/features.md` row 106 gained the analyze-repair4 event line; status stays `Planned`; parent 095 stays `Ready for Review`. **Not touched**: `requirements.md`, `research.md`, `feature-ref.md`, `plan.md`, `quickstart.md`, `handoff.md`, `contracts/settlement-contract.contract.md`; the dated checklist was not rewritten.

## 3. Verification (commands and results)

| Check | Command | Result | Evidence |
|---|---|---|---|
| Requirements structure | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/106-background-silent-failure/requirements.md` | rc 0 — **0 error / 0 warning**; 312 lines, 50 definition rows, 4 shared strings | `test-evidence/analyze-repair4-requirements-validator.txt` |
| Tasks structure | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/106-background-silent-failure/tasks.md` | rc 0 — PASS, **0 error / 0 warning** | `test-evidence/analyze-repair4-tasks-validator.txt` |
| Cross-artifact (requirements) | `pre-analyze-check.py --spec-dir … --stage requirements --repo .` | rc 0 — `decision=pass`, **errors=0**, advisories=55 (all expected missing-path of the planned new tests/fixtures), waived=0; fr=41 sc=9 tasks=37 clauses=34 files=12 | `test-evidence/analyze-repair4-pre-analyze-requirements.txt` |
| Cross-artifact (plan) | same, `--stage plan` | rc 0 — `decision=pass`, errors=0, advisories=55, waived=0 | `test-evidence/analyze-repair4-pre-analyze-plan.txt` |
| Cross-artifact (tasks) | same, `--stage tasks` | rc 0 — `decision=pass`, errors=0, advisories=55, waived=0 | `test-evidence/analyze-repair4-pre-analyze-tasks.txt` |
| Decomposition | `decomposition-check.py --mode tasks --requirements … --tasks …` | rc 0 — `decision=proceed` (fr 41 / tasks 37; ceilings 120/160) | `test-evidence/analyze-repair4-decomposition.txt` |
| Clause extract | `clause_extract.py contracts/*.md` | 3 files, `form=md-bold-closed`, **34 clauses** (12/10/12), ids unchanged; output **byte-identical** to the r3 reading (`cmp` equal) | `test-evidence/analyze-repair4-clause-extract.json` |
| Clause coverage accountant | `scripts/python/account-clause-coverage.py --spec-dir …` | rc 1 with output **byte-identical** to the r3 reading (`cmp` equal): claimed clauses 34, `clause-uncovered` beyond-baseline **0**, `fr-uncovered` 37/41 (FR-036/037/039/040), `clause-unparsable` 111 (documented structural verdict, not a pass criterion — tasks GATE-3) | `test-evidence/analyze-repair4-clause-coverage.txt` |
| Gate scan | `python3 scripts/python/scan-confirmation-gates.py --root . --json` | rc 0, **byte-identical** to the r3 reading: total **31** (governance_kept 7 / destructive 23 / reversible 1; keep_gate 30 / auto_execute 1); **0 hits in the four touched files**; violations 0 | `test-evidence/analyze-repair4-gate-scan.json` |
| Glossary | `python3 .specify/scripts/python/glossary-utils.py --action validate` | `{"valid": true}` | `test-evidence/analyze-repair4-glossary-validate.txt` |
| Workspace guard (before) | `workspace-guard.py --snapshot …-analyze-repair4-before.json --repo .` then `--check` | snapshot recorded; `--check` → `clean` (rc 0) | `test-evidence/workspace-snapshot-analyze-repair4-before.json`, `workspace-check-analyze-repair4-before-commit.txt` |
| Run determination | `run-determination.py --action determine --unit-id skill:analyze-artifacts --run-id r20261125T173750Z-106r4 --complexity complex --qualification qualified --declared-check ×10` | recorded; four axes `not_evaluated` with named reasons; `trigger_feedback: false`; change point `cp-r20261125T173750Z-106r4` (clean=false findings=4); previous run r3 settled `not_evaluated` (`no_user_input`) in a follow-up `--action settle` | `test-evidence/run-determination-analyze-repair4.txt`; `.specify/session/20261125T173937Z-run-determination-skill-analyze-artifacts-r20261125t173750z.md` |
| Exec quant | `exec-quant.py --action collect --unit-id skill:analyze-artifacts --run-id …` | recorded → `.specify/exec-quant/records/20261125T173956791454Z-2e94960a.json` | `test-evidence/exec-quant-analyze-repair4.txt` |
| Feedback record | `feedback-utils.py --action record …` | entry `20261125T174002Z-skill-analyze-artifacts` (`should_prompt: true`, count 565 vs threshold 10; no packaging/transmission — `trigger_feedback: false`) | `test-evidence/feedback-record-analyze-repair4.txt`; `.specify/feedback/20261125T174002Z-skill-analyze-artifacts.md` |

## 4. Preserved surfaces

- Closed settlement set `completed` / `failed` / `anomaly` / `cancelled` / `running` / `silent-end` / `unknown`, the three violation kinds, the three predicates' count and the four E4 mechanism values: unchanged.
- Exit-code meanings (C-26: 0 judged / 1 violations / 2 `unknown`) unchanged; the fix only makes the 7-column-row path decidable within them.
- Sentinel literals, watcher verdict tokens/exit codes/`--self-test`, five-element uplink, seven-field downlink, destructive-action discipline, confirmation-gate budget, two-slot test budget: unchanged; `watch-target.sh` not edited; zero tests collected or run.
- FR/SC/STR ids and all 34 clause ids unchanged; no task added/removed/renumbered; no new carrier, store, root, column or engine.

## 5. Assumptions (unattended; no user adjudication)

1. **A team-report row's version declaration is its 7-column header** — C-16 fixes the new header at exactly 7 columns, so a `settlement_version` cell is unavailable by design; FR-034's "MUST NOT 改动既有行格式" supports declaring the version through the additive header rather than a column.
2. **C-10's "settlement-bearing record" is read as the file-shaped records** (E2/E3/E5 `attempt-file`); the row shape's additive declaration is C-16's header. C-10 was outside the named fix surface (E5/E6/E7/INV08 + C-16/C-33) and its wording stays true under this reading; FR-034 scopes legacy to old attempts/old reports, which a new 7-column report is not.
3. **A malformed 7-column row exits 1, not 2** — the row is readable and version-bearing; its empty cells are an unrecorded claim (C-26's "settlement violations found"), never an unreadable-evidence refusal (INV05).
4. **T003/T029 were aligned inside this repair** — they are the owner-amendment and engine-implementation rows that restate the version test; leaving them generic would re-create R4-01 in the owner text and the engine. Counts, order and clause claims are unchanged.

## 6. Residual risk / open items

- Round-4 MEDIUM findings **R4-02…R4-05 remain open by design** (outside the 1-HIGH dispatch): C-34's closed behavior-class set vs four tagged clauses; C-27's settle edge-kind emission shape; quickstart behavior-class naming; E9's reaction-record storage surface.
- C-10's wording ("every new settlement-bearing record" / "records without it are legacy") uses the file-record reading recorded in Assumption 2; if a later round reads it to cover report rows, that is a new finding against C-10 rather than a silent repair here.
- All earlier unresolved MEDIUM/LOW findings (rounds 1–3) remain open as recorded.
- The coverage accountant's rc 1 (`fr-uncovered` 37/41, `clause-unparsable` 111) is the documented structural verdict, byte-identical to the frozen reading; reported honestly, never used as a pass criterion.
- The R4-01 fix is design-level; the engine behavior (T007/T009/T028/T029) and its exit-1/exit-0 fixtures are future implementation evidence.

## 7. Fast-fail anomaly line

未发现异常 — no decision-class anomaly and no in-passing correction was needed; every edit is the authorized repair of R4-01, with the four task-row alignments disclosed in Section 2.
