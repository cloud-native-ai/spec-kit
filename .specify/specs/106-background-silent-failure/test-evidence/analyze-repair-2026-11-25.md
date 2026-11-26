# Analyze-Repair Record — 106-background-silent-failure — 2026-11-25

- **Trigger**: analyze gate FAIL — 10 validation-confirmed HIGH findings (report `test-evidence/analyze-report-2026-11-25.md`; the analyze close-out receipt records the gate).
- **Route**: analyze-gate autonomous upstream repair. Authority: the 10 HIGH findings listed in the dispatch; no user questions (unattended).
- **Unit / run**: `skill:analyze-artifacts` · `r20261125T125827Z-106r` · feature key `106-background-silent-failure`.
- **Scope discipline**: only live spec artifacts and their records were edited. Dated records (`checklists/background-settlement-2026-11-25.md`, `test-evidence/*` from earlier stages, the analyze report and findings files) were **not** rewritten. FR ids, SC ids, STR ids and contract clause ids are unchanged (additive clarification only; no renumbering). Sentinel literals, watcher verdicts/exit codes, the five-element uplink / seven-field downlink, confirmation discipline, the two-slot budget and the closed settlement value set are untouched.
- **Concurrency reading**: requested=1 · effective=not_evaluated · effective_reason=single-unit (A-17: one executor, single leaf, no dispatch).

## 1. Finding → change → evidence map

### W1-02 — exit 0 + final `ANOMALY:` line matched both the incomplete-`failed` and the `anomaly` branch; no precedence

- **Change**: explicit precedence — an exit-0 termination carrying an explicit anomaly signal settles `anomaly`; the incomplete-`failed` branch applies only without an anomaly marker.
  - `requirements.md:171` (FR-003), `:172` (FR-004), `:148` (edge case), `:246` (matrix `failed` row), `:247` (`anomaly` row).
  - `contracts/settlement-contract.contract.md:16` (C-02: failure requires "without an explicit anomaly signal"; anomaly wins on exit 0).
  - `data-model.md:157` (state-transition precedence note; the transition table already ordered anomaly first).
  - `tasks.md:155` (T002 carries the precedence into the owner page).
- **Evidence**: the clause text now states one reading; `validate-requirements` 0/0; pre-analyze requirements/plan/tasks `decision=pass errors=0`.

### W1-03 — A-7 / glossary required disappearance for `silent-end`; FR-006's no-pid deadline branch was excluded

- **Change**: A-7 widened with the no-pid branch as a substitute for the "subject gone" test (same value, not a second value); FR-006 states the same branch explicitly; the proposed glossary entry is aligned before confirmation (A-15 hands semantic reference to it after takeover).
  - `requirements.md:52` (A-7), `:174` (FR-006).
  - `.specify/glossary.md:208` (silent-end meaning extended with the no-pid/declared-wait-deadline branch).
  - Contract mirrors: `settlement-contract.contract.md:16` (C-02), `:20` (C-03).
- **Evidence**: `glossary-utils.py --action validate` → `{"valid": true}` (`test-evidence/analyze-repair-glossary-validate.txt`); C-03 now says "same value's no-pid branch, not a second value".

### W1-04 — `running` vs `silent-end` decided by unnamed "declared threshold" / "declared wait deadline" (no declarer, field, default, domain)

- **Change**: the declaration surface is named and given one owner. C-25 owns the three boundary inputs and their values/domains/precedence; requirements and the data model point there and never restate the numbers.
  - Owner: `contracts/enforcement-and-migration.contract.md:10` (C-25): `--live-window N` (default 120 s), `--wait-deadline N` (default 1800 s), `--start-grace N` (default 30 s), positive-integer seconds; precedence = attempt-record field > option > built-in default.
  - Pointer updates: `requirements.md:173` (FR-005 live window), `:174` (FR-006 wait deadline), `:178` (FR-010 record fields), `:187` (FR-016 start grace), `:189` (FR-018 deadline); `:250` (matrix `silent-end` row); edge case `:150`.
  - Records/inputs: `data-model.md:29-30` (E2 `wait_deadline_s` / `start_grace_s`), `:128` (INV03), `:129` (INV04); `enforcement-and-migration.contract.md:22` (C-28 input list).
  - Task rows: `tasks.md:155` (T002), `:176` (T007).
- **Evidence**: the earlier full-file grep for 阈值|期限|声明 found no number/domain/declarer; after the repair every use points to C-25, and C-25 carries the only numeric values. Advisories from pre-analyze are missing-path only (0 errors).

### W1-05 — FR-002's independent-verification mechanisms were an open "例如" list; FR-029 / SC-002 guard had no decidable evidence set

- **Change**: the mechanism set is closed at four values with a named owner, and the guard predicate becomes decidable.
  - `requirements.md:170` (FR-002: `u4` / `team-verification` / `five-element` / `return-record`, owner = data-model E4 + revised § Termination, out-of-set mechanisms never constitute completion evidence), `:245` (matrix `completed` row).
  - `settlement-contract.contract.md:16` (C-02 mandates the owner page carry the closed set).
- **Evidence**: E4 (`data-model.md:50-58`) already enumerated exactly those four mechanism values, so the closed set is grounded in the existing record shape; `validate-requirements` 0/0.

### W1-06 — FR-010 / FR-018 required persistent attempt/start records while FR-038 / A-6 forbade new storage; no carrier named

- **Change**: the existing carrier is named — the additive `<label>.attempt` file in the existing dispatch log directory (`--logs-dir` root) — and explicitly placed under FR-033's additive allowance, outside FR-038/A-6's storage ban. C1 reuses its four-piece (no duplicate).
  - `requirements.md:178` (FR-010), `:189` (FR-018), `:218` (FR-038 carve-out sentence), `:156` (edge case names the carrier).
  - `settlement-contract.contract.md:32` (C-06 names the directory and the additive file).
- **Evidence**: `data-model.md` E8 (C4 row) already records the `.attempt` file in the existing dispatch log dir; `carrier-conformance.contract.md:54` (C-24) already said attempt records reuse the existing dispatch log directory. The repair aligns the requirements clause with that plan-level decision.

### W1-07 — FR-039 / SC-009 claimed a frozen-total equality stays green while EP-005 measured it red at base (31≠27)

- **Change**: an actual baseline referent and the EP-005 fallback criterion are named; the equality check is stated as a disclosed pre-existing red that is never claimed green; the requirement checklist item is re-scoped to the referent.
  - `requirements.md:57` (A-12), `:219` (FR-039), `:276` (SC-009), `:287` (SC-009 Source).
  - `checklists/requirements.md:18` (tick re-scoped: EP-005 referent, allowed delta = per-file zero new blocking hits, `== 27` disclosed red).
- **Evidence**: `plan.md:185-187` (EP-005 `falsified` → `fallback`, measured total 31 vs pinned 27, "never claims it green"); live scanner re-run after this repair: `total: 31` unchanged, touched-file hits 0 (`test-evidence/analyze-repair-gate-scan.json`).

### W2-01 — C-06 settled a no-start-record attempt as `unknown` while C-04/INV05/C-26 defined `unknown` only for unreadable evidence (exit 2)

- **Change**: `unknown` now has exactly two readable causes, each with a distinct finding label in the closed E6 shape — `unreadable` and `start-record-missing` — and the exit-2 map is aligned. The settlement value set stays closed (no new value); the distinction is a finding label (`unknown_cause`), recorded as a minor PLAN-EDIT below.
  - `requirements.md:175` (FR-007), `:178` (FR-010), `:156` (edge case; the `legacy/` reading is removed — this also closes the wording half of downgraded W1-01), `:251` (matrix `unknown` row).
  - `settlement-contract.contract.md:24` (C-04), `:32` (C-06).
  - `enforcement-and-migration.contract.md:14` (C-26 exit map), `:42` (C-33).
  - `data-model.md:87` (E6 `unknown_cause`), `:98` (E7 note), `:130` (INV05), `:153-154` (state transitions).
  - Tasks: `tasks.md:155` (T002), `:176` (T007).
- **Evidence**: C-04/C-06/C-26/INV05 now state the same two-cause rule; every `unknown` exit still maps to exit 2 (never 0).

### W2-03 — a legacy 5-column team-report row matched `settlement-unrecorded` (exit 1) while INV08 / C-33 forbade legacy records from failing the exit

- **Change**: explicit legacy carve-out — a row parsed under the legacy 5-column header is annotated `legacy` and MUST NOT be judged `settlement-unrecorded`; mirrored across the model, both contracts and the quickstart scenario.
  - `data-model.md:72` (E5 `settlement_version`), `:94` (E7 `settlement-unrecorded`), `:133` (INV08).
  - `carrier-conformance.contract.md:22` (C-16), `enforcement-and-migration.contract.md:42` (C-33).
  - `quickstart.md:80` (S-3 expected output).
  - Tasks: `tasks.md:197` (T012), `:265` (T029).
- **Evidence**: C-16/C-33/INV08/E7 all now carry the same carve-out; quickstart S-4's exit-0 legacy pin no longer conflicts with S-3.

### W2-04 — the pid-less running/silent-end split (and C-15's start grace) depended on an undeclared wait deadline

- **Change**: same single owner as W1-04 (C-25) for both boundary inputs; C-03/C-15/C-17 and INV03/INV04 point to it; E2 and C-28 extended with the record fields and input list.
  - `contracts/settlement-contract.contract.md:20` (C-03), `contracts/carrier-conformance.contract.md:18` (C-15 start grace), `:26` (C-17 deadline).
  - `enforcement-and-migration.contract.md:10` (C-25 options/defaults/domain/precedence), `:22` (C-28 input list).
  - `data-model.md:29-30` (E2), `:128-129` (INV03/INV04).
- **Evidence**: after the repair, a full grep of requirements/contracts/data-model for 声明等待期限 / declared wait deadline / start grace / threshold resolves every occurrence either to C-25 or to a pointer at C-25; no undeclared boundary value remains.

### W3-01 — tasks.md allowed disclosed small edits to plan-owned files while handoff.md / team.md forbade those paths to every crew seat

- **Change**: one permission regime chosen — the crew never writes plan-owned paths; those paths belong to the spec side (driver / analyze-repair), and an implementation-time design defect halts and returns to the spec side. The territory contracts become the stated precedence owner.
  - `tasks.md:66` (plan-owned face: spec-side only; crew forbidden; territory contract wins on conflict), `:360` (no crew PLAN-EDIT allowance; a design-face defect halts and returns to the spec side, which declares under PLAN-EDIT discipline; substantive changes halt).
- **Evidence**: `handoff.md:42` ("MUST stay forbidden to every seat"), `team.md` territory.forbidden list (same six paths) — unchanged and now uncontested; `validate-tasks` PASS 0/0 after the edit.

## 2. PLAN-EDIT declarations (analyze-driven defect fixes, not intent changes)

| Plan-owned file | Declaration | Classification |
|---|---|---|
| `contracts/settlement-contract.contract.md` | `PLAN-EDIT: contracts/settlement-contract.contract.md — analyze findings W1-02/W1-03/W1-05/W1-06/W2-01/W2-04: precedence, no-pid branch, closed mechanism set, named attempt-record carrier, two-cause `unknown`, boundary-input pointers (C-02/C-03/C-04/C-06); clause ids unchanged` | **minor** — additive clarification of existing clauses; closed sets preserved; no preserved surface touched |
| `contracts/carrier-conformance.contract.md` | `PLAN-EDIT: contracts/carrier-conformance.contract.md — analyze findings W2-03/W2-04: legacy 5-column carve-out, named start-grace/deadline inputs (C-15/C-16/C-17); clause ids unchanged` | **minor** — additive clarification; no carrier removed or added |
| `contracts/enforcement-and-migration.contract.md` | `PLAN-EDIT: contracts/enforcement-and-migration.contract.md — analyze findings W1-04/W2-01/W2-04/W2-03: boundary-input option owner (C-25), exit-2 map extended to `start-record-missing` (C-26), input list (C-28), legacy carve-out (C-33)` | **minor** — additive; exit code meanings unchanged (0/1/2); violation kinds stay three |
| `data-model.md` | `PLAN-EDIT: data-model.md — analyze findings W1-04/W2-01/W2-03/W2-04: E2 optional `wait_deadline_s`/`start_grace_s`, E5/E7 legacy exemption, E6 `unknown_cause`, INV03/INV04/INV05/INV08, transition note` | **minor** — additive fields; 9 entities / 12 invariants retained; value set closed |
| `quickstart.md` | `PLAN-EDIT: quickstart.md — analyze finding W2-03: S-3 expected output states the legacy carve-out (exit 0)` | **minor** — scenario expectation aligned with the contract, no new scenario |

**Not touched**: `plan.md`, `research.md`, `feature-ref.md`. The chosen boundary defaults (120 s / 1800 s / 30 s) live only in C-25; requirements, data model and tasks reference C-25 and do not restate them (one owner).

## 3. Verification (commands and results)

| Check | Command | Result | Evidence |
|---|---|---|---|
| Requirements structure | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/106-background-silent-failure/requirements.md` | rc 0 — **0 error / 0 warning**; 312 lines, 50 definition rows (41 FR + 9 SC), 4 shared strings | `test-evidence/analyze-repair-requirements-validator.txt` |
| Tasks structure | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/106-background-silent-failure/tasks.md` | rc 0 — PASS, **0 error / 0 warning** | `test-evidence/analyze-repair-tasks-validator.txt` |
| Cross-artifact (requirements) | `pre-analyze-check.py --spec-dir … --stage requirements --repo .` | rc 0 — `decision=pass`, **errors=0**, advisories=55 (all expected missing-path of the planned new tests/fixtures), fr=41 sc=9 tasks=37 clauses=34 | `test-evidence/analyze-repair-pre-analyze-requirements.txt` |
| Cross-artifact (plan) | same, `--stage plan` | rc 0 — `decision=pass`, errors=0, advisories=55 | `test-evidence/analyze-repair-pre-analyze-plan.txt` |
| Cross-artifact (tasks) | same, `--stage tasks` | rc 0 — `decision=pass`, errors=0, advisories=55 | `test-evidence/analyze-repair-pre-analyze-tasks.txt` |
| Decomposition | `decomposition-check.py --mode tasks --requirements … --tasks …` | rc 0 — `decision=proceed` (fr 41 / tasks 37, ceilings 120/160) | `test-evidence/analyze-repair-decomposition.txt` |
| Clause extract | `clause_extract.py contracts/*.md` | 3 files, `form=md-bold-closed`, **34 clauses** (12/12/10), ids unchanged | `test-evidence/analyze-repair-clause-extract.json` |
| Clause coverage accountant | `scripts/python/account-clause-coverage.py --spec-dir …` | identical to the frozen tasks-stage reading: claimed clauses 34, `clause-uncovered` beyond-baseline **0**, `fr-uncovered` 37/41, `clause-unparsable` 111 (documented structural verdict, not a pass criterion — tasks GATE-3) | `test-evidence/analyze-repair-clause-coverage.txt` |
| Gate scan | `python3 scripts/python/scan-confirmation-gates.py --root . --json` | total **31** (governance_kept 7 / destructive 23 / reversible 1) — unchanged from base; **touched-file hits 0** (EP-005 fallback satisfied) | `test-evidence/analyze-repair-gate-scan.json` |
| Glossary | `python3 .specify/scripts/python/glossary-utils.py --action validate` | `{"valid": true}` | `test-evidence/analyze-repair-glossary-validate.txt` |

**In-passing correction (fast-fail: correction class, disclosed)**: the first tasks.md edit referenced "C-62" (a handoff-contract clause id) inside this spec, and the first `pre-analyze-check` run rejected the file with `dangling-id` at tasks.md:66. The clause-id mention was removed and all three stages re-ran green. No decision was needed; the correction only removed an id that does not exist in this spec's contract set.

## 4. Assumptions (unattended; no user adjudication)

1. **Boundary defaults chosen** — `--wait-deadline` 1800 s is a newly declared design value (no pre-existing native-background deadline in the repo); `--live-window` 120 s and `--start-grace` 30 s align with the existing `watch-target.sh` defaults (`--heartbeat-max-age=120s`, `--start-grace=30s`). All three are declared once in C-25; review may revisit the numbers without touching requirements.
2. **`unknown` stays one settlement value** — the no-start-record case is distinguished by the closed `unknown_cause` finding label (`unreadable` / `start-record-missing`), not by an eighth settlement value; the settlement value set remains the seven-value closed set.
3. **Legacy detection for team rows** — a row parsed under the legacy 5-column header is version-less by construction; no per-row version marker was invented.
4. **W2-02 (LOW) not repaired** — the unqualified `DONE → completed` arrow in C-13 was outside the 10 HIGH set and is left for a later pass; its qualifier sentence already follows in the same clause.

## 5. Residual risk / open items

- The 14 MEDIUM + 7 LOW findings from the analyze report are **not** in this repair's authorized set and remain open (e.g. W1-08 re-ask-rule owner, W1-10 pre-dispatch failure record shape, W2-05 anomaly/cancelled red paths, W2-06 `return-record` definition, W2-07 C1/E2 duplication, W2-08 RUNNING fallback, W2-09 C3 header decision tension, W2-02 arrow wording). W1-09 (EP-005 carriage on the requirement side) is incidentally addressed: FR-039/SC-009 now carry EP-005 by reference.
- The new C-25 option names and defaults are contract-declared but not yet implemented; T007 now instructs the engine implementation to declare exactly these options. Until T007 lands, `role-edge-check.py --help` does not show them — expected for a pre-implement stage.
- `return-record` remains defined only as "declared equivalent" (W2-06); FR-002's closure makes the guard decidable at the mechanism-value level, but the mechanism's admissible evidence is still to be tightened.
- The glossary entry is a hand edit of a `status=proposed` entry (glossary-utils has no update action); `--action validate` passes, and the entry remains `proposed` for the existing user confirmation channel.

## 6. Fast-fail anomaly line

未发现异常 — no decision-class anomaly. One in-passing correction (dangling `C-62` reference, §3) was disclosed.
