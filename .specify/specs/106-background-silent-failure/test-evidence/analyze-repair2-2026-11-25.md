# Analyze-Repair2 Record — 106-background-silent-failure — 2026-11-25

- **Trigger**: analyze round 2 produced 6 HIGH findings; validators confirmed 5 (R2-W1-01, R2-W1-02, R2-W3-01, w2a-01, w2b-01) and rejected 1 (w2c-03). This repair is bounded to the 5 confirmed findings; **w2c-03 was NOT repaired** per the dispatch.
- **Route**: analyze-gate autonomous upstream repair (round 2). Authority: the dispatch's 5-finding set; no user questions (unattended).
- **Unit / run**: `skill:analyze-artifacts` · `r20261125T132316Z-106r2` · feature key `106-background-silent-failure`.
- **Scope discipline**: only live spec artifacts and their records were edited. Dated records (`checklists/background-settlement-2026-11-25.md`, earlier `test-evidence/*`, the round-2 finding files `analyze-domain-*-r2.jsonl`) were **not** rewritten; the 5 untracked round-2 domain files were left untouched and are not part of this repair's commit. FR ids (41), SC ids (9), STR ids (4) and all 34 contract clause ids are unchanged; the closed settlement value set, sentinel literals, watcher verdicts/exit codes, five-element uplink / seven-field downlink, confirmation discipline and the two-slot budget are untouched. No code, test or carrier script was implemented.
- **Concurrency reading**: requested=1 · effective=not_evaluated · effective_reason=single-unit (A-17: one executor, single leaf, no dispatch).

## 1. Finding → change → evidence map

### R2-W1-01 — FR-006/A-7 (no-pid `silent-end` at the wait deadline) vs Edge Case 「期限之后的晚完成」 (waits out an unnamed "deadline grace")

- **Reconciliation chosen**: the declared wait deadline **triggers the settlement-time observation**; the only reclassification window is the existing one — evidence already present at that observation settles the attempt, and for C1 the watcher's existing `--deadline-grace` (default 120 s, `watch-target.sh --help`) keeps its reclassification semantics unchanged. The settlement layer adds **no second grace parameter**; once `silent-end` is settled, a later return is a late return under FR-009 and never rewrites the settled value.
- **Change** (stated once in FR-006; duplicates reduced to pointers):
  - `requirements.md:174` (FR-006) — adds the observation-trigger sentence, the C1 `--deadline-grace` pointer, "MUST NOT 在期限之前宣布消失", and the late-return rule.
  - `requirements.md:52` (A-7) — no-pid substitute now says the deadline only triggers the observation and points to FR-006.
  - `requirements.md:153` (Edge Case) — rewritten as a pointer to FR-006's single reading; keeps "not before the deadline" and the FR-009 late-return rule.
  - `contracts/settlement-contract.contract.md:20` (C-03) — owner-page clause now carries the same observation-trigger semantics and the "adds no settlement-side parameter" boundary.
- **Evidence**: the "existing deadline grace" is a real, pre-existing watcher option (`test-evidence/watch-help-baseline.txt`: `--deadline-grace N` … default 120s; "a late status/sentinel reclassifies to DONE/FAILED before TIMEOUT"), so the repair names it instead of inventing a fourth boundary value; `validate-requirements` 0/0; pre-analyze 3 stages pass.

### R2-W1-02 — SC-006 asserted absolute source/template/installed identity while its own Source and the glossary's relative-criterion rule re-scope it

- **Change**: `requirements.md:273` (SC-006) — "源/模板/已安装副本一致" → "源/模板/已安装副本在**本特性触及面**上零新增漂移（基线漂移如实报告、不声称全树一致——相对判据形态同 SC-009）".
- **Duplicates checked**: the absolute claim existed only at SC-006 (repo grep over requirements / tasks / quickstart / checklists). SC-006's own Source (`:285`), `tasks.md` DoD-5 and plan § Mirror Obligations were already baseline-relative and needed no edit.
- **Evidence**: glossary entry 「相对判据 (Relative Criterion)」 (`.specify/glossary.md:138`) records the pre-existing full-tree mirror red and mandates the relative form; SC-009 already uses it.

### R2-W3-01 — T035 wrote `verification.md`, which handoff.md / team.md forbid to every crew seat

- **Reconciliation chosen**: crew-writable input + spec-side writeback (the spec-105 precedent — its T039 writeback records `spec-side write because verification.md stays forbidden to the crew per handoff C-62`).
  - `tasks.md:283` (T035) — crew now writes `test-evidence/verification-input.md` (SC status rows, smoke triple, `deferred_tasks=`); `verification.md` is materialized **spec-side** (driver) from that input after it lands. DoD-8 and GATE-4 still read `verification.md` and stay satisfiable.
  - `tasks.md:24` (DoD-8) — states the same split.
  - `tasks.md:64` (Path Conventions · 证据落点) — `verification-input.md` (crew) added; `verification.md` marked spec-side derived, forbidden to crew.
  - `handoff.md:26` (Task Reference) — the wholesale T001–T037 hand adds the one ownership split, keeping `verification.md` forbidden (C-62) and the input crew-writable.
- **Evidence**: `handoff.md:42` and `.specify/teams/106-background-silent-failure/team.md` forbidden lists unchanged; `test-evidence/**` is in both write grants (handoff.md:34; team.md:21), so the input path is legal for the crew.

### w2a-01 — C3 had no start-side record, so a seat dying before its report row could never settle `silent-end`

- **Reconciliation chosen**: give C3 an E2 start record consistent with E2's existing `c3-team-seat` carrier value — `run-team` writes `<label>.attempt` (`started_at`) before seat hand-off; when the seat is dispatched through C1/C2, the same label's existing carrier start evidence **is** the start record (no duplicate write, mirroring C1's no-duplicate rule). The report row remains the E5 **claim** surface, not the start record.
- **Change**:
  - `requirements.md:178` (FR-010) — attempt-record writers now "C2 / C3 / C4 直接写入；C1 复用四件套、经 C1/C2 派发的 C3 席位复用同 label 的载体起点证据，均不重复写".
  - `requirements.md:188` (FR-017) — adds the per-seat start-record obligation and the "missing rows/start record/settlement ⇒ report incomplete" reading.
  - `requirements.md:227` (Evidence Bundle C3) and `:236` (Carrier Inventory C3 row: 现有证据 "无席位起点记录", 处置 adds the start record); `:31` (Overview C3 baseline narrative notes the missing start record).
  - `contracts/carrier-conformance.contract.md:22` (C-16) — start-side record requirement + the silent-seat settlement consequence; `:54` (C-24) — team settlement rides the report **and** the additive seat start record in the existing dispatch log dir (no new root).
  - `contracts/enforcement-and-migration.contract.md:22` (C-28) — settle input list now names "the C3 seat start records (E2, carrier `c3-team-seat`) + team report mapping rows".
  - `data-model.md:26` (E2 `started_at` rule includes C3), `:106` (E8 C3 row: attempt record written by `run-team` seat dispatch / same-label C1/C2 evidence; report row stays E5), `:129` (INV04 start-record leg names the C3 substitute).
  - `tasks.md` — T005 (C3 start-record / missing-start fixtures), T007 (engine reads C3 seat start records), T009 (C3 silent death → `silent-end`; no start record → `unknown` `start-record-missing`), T017 (run-team entry line carries the start-record obligation); Requirement Coverage Map FR-010 adds T017 and FR-017 adds T007/T017.
  - PLAN-EDIT: `plan.md:15` (summary item 3) and `:23` (Storage) name the seat start record; `quickstart.md` S-3 Premises add the start-record premise and the two settlement outcomes.
- **Evidence**: `data-model.md:18-33` already defines E2 with `carrier: … c3-team-seat …` and `started_at`, so the repair grounds C3 in the existing record shape rather than inventing one; INV04/C-02's silent-end rule ("E2 start record present") becomes satisfiable for C3; `validate-requirements` 0/0; `validate-tasks` PASS.

### w2b-01 — C-25 declared `--live-window` / `--wait-deadline` / `--start-grace` but the settlement contract's `running` / pid-less `silent-end` rows did not consume them

- **Change** (numbers stay only in C-25; the settlement contract cites option/field names):
  - `contracts/settlement-contract.contract.md:16` (C-02) — `running` row: live-log-growth leg measured over C-25's `--live-window`; `silent-end` row: "no live signal" is defined as the same settlement-time live check failing on every leg (live-log leg over `--live-window`), and process-carrier subject-gone includes a pid that never appeared within C-25's `--start-grace` / the attempt's `start_grace_s`.
  - `contracts/settlement-contract.contract.md:20` (C-03) — points "no live signal" at C-02's `running` row (one definition) and restates the observation-trigger/late-return boundary from R2-W1-01.
  - `data-model.md:129` (INV04) — consumes all three inputs: process-carrier `--start-grace` / `start_grace_s`, pid-less `--wait-deadline` / `wait_deadline_s` + settlement-time live check; INV03 already cites `--live-window`.
- **Evidence**: repo grep shows the three options' numeric defaults/domains appear only at `enforcement-and-migration.contract.md:10` (C-25) and the two record fields' semantics at E2; every settlement-contract use is a named pointer. `pre-analyze` 3 stages `decision=pass errors=0`.

## 2. PLAN-EDIT declarations (analyze-driven defect fixes, not intent changes)

| Plan-owned file | Declaration | Classification |
|---|---|---|
| `contracts/settlement-contract.contract.md` | `PLAN-EDIT: contracts/settlement-contract.contract.md — R2-W1-01/w2b-01: observation-trigger + late-return semantics (C-03); running/silent-end consume C-25's --live-window/--wait-deadline/--start-grace by name, numbers stay in C-25 (C-02); clause ids unchanged` | **minor** — additive clarification; seven-value set and evidence matrix unchanged |
| `contracts/carrier-conformance.contract.md` | `PLAN-EDIT: contracts/carrier-conformance.contract.md — w2a-01: C3 seat start record (E2 carrier c3-team-seat or same-label C1/C2 evidence; C-16) and team settlement rides the additive seat start record (C-24); clause ids unchanged` | **minor** — additive; no carrier added/removed |
| `contracts/enforcement-and-migration.contract.md` | `PLAN-EDIT: contracts/enforcement-and-migration.contract.md — w2a-01: settle input list names C3 seat start records (C-28); clause ids unchanged` | **minor** — additive input list; exit codes and violation kinds unchanged |
| `data-model.md` | `PLAN-EDIT: data-model.md — w2a-01/w2b-01: E2 started_at covers C3, E8 C3 row gains the start-record writer, INV04 consumes start-grace + wait-deadline + settlement-time live check` | **minor** — additive rules on existing entities; 9 entities / 12 invariants retained |
| `plan.md` | `PLAN-EDIT: plan.md — w2a-01 pointer: summary item 3 and the Storage line name the C3 seat start record; no scope/count change` | **minor** — pointer alignment only |
| `quickstart.md` | `PLAN-EDIT: quickstart.md — w2a-01 premise: S-3 states the seat start-record premise and the silent-end / start-record-missing outcomes` | **minor** — premise alignment; no new scenario |

**Not touched**: `research.md`, `feature-ref.md`; `checklists/background-settlement-2026-11-25.md` is a dated record and was not rewritten; rejected finding `w2c-03` (C-15 "completion declaration" vs research R-03's optional `.settlement`) was left unrepaired per the dispatch.

## 3. Verification (commands and results)

| Check | Command | Result | Evidence |
|---|---|---|---|
| Requirements structure | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/106-background-silent-failure/requirements.md` | rc 0 — **0 error / 0 warning**; 312 lines, 50 definition rows (41 FR + 9 SC), 4 shared strings | `test-evidence/analyze-repair2-requirements-validator.txt` |
| Tasks structure | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/106-background-silent-failure/tasks.md` | rc 0 — PASS, **0 error / 0 warning** | `test-evidence/analyze-repair2-tasks-validator.txt` |
| Cross-artifact (requirements) | `pre-analyze-check.py --spec-dir … --stage requirements --repo .` | rc 0 — `decision=pass`, **errors=0**, advisories=55 (all expected missing-path of the planned new tests/fixtures), waived=0; fr=41 sc=9 tasks=37 clauses=34 | `test-evidence/analyze-repair2-pre-analyze-requirements.txt` |
| Cross-artifact (plan) | same, `--stage plan` | rc 0 — `decision=pass`, errors=0, advisories=55, waived=0 | `test-evidence/analyze-repair2-pre-analyze-plan.txt` |
| Cross-artifact (tasks) | same, `--stage tasks` | rc 0 — `decision=pass`, errors=0, advisories=55, waived=0 | `test-evidence/analyze-repair2-pre-analyze-tasks.txt` |
| Decomposition | `decomposition-check.py --mode tasks --requirements … --tasks …` | rc 0 — `decision=proceed` (fr 41 / tasks 37; ceilings 120/160) | `test-evidence/analyze-repair2-decomposition.txt` |
| Clause extract | `clause_extract.py contracts/*.md` | 3 files, `form=md-bold-closed`, **34 clauses** (12/12/10), ids unchanged | `test-evidence/analyze-repair2-clause-extract.json` |
| Clause coverage accountant | `scripts/python/account-clause-coverage.py --spec-dir …` | rc 1 with output **byte-identical** to the frozen tasks-stage reading: claimed clauses 34, `clause-uncovered` beyond-baseline **0**, `fr-uncovered` 37/41, `clause-unparsable` 111 (documented structural verdict, not a pass criterion — tasks GATE-3) | `test-evidence/analyze-repair2-clause-coverage.txt` |
| Gate scan | `python3 scripts/python/scan-confirmation-gates.py --root . --json` | total **31** (governance_kept 7 / destructive 23 / reversible 1) — unchanged from base; **touched-file hits 0** (EP-005 fallback satisfied); violations 0 | `test-evidence/analyze-repair2-gate-scan.json` |
| Glossary | `python3 .specify/scripts/python/glossary-utils.py --action validate` | `{"valid": true}` | `test-evidence/analyze-repair2-glossary-validate.txt` |
| Workspace guard (before) | `workspace-guard.py --snapshot …-analyze-repair2-before.json --repo .` | recorded | `test-evidence/workspace-snapshot-analyze-repair2-before.json` |

## 4. Preserved surfaces

- Closed settlement set `completed` / `failed` / `anomaly` / `cancelled` / `running` / `silent-end` / `unknown` and the per-value evidence matrix: unchanged.
- Sentinel literals, watcher verdict tokens/exit codes/`--self-test`, five-element uplink, seven-field downlink, destructive-action discipline, confirmation-gate budget, two-slot test budget: unchanged; `watch-target.sh` not edited.
- FR/SC/STR ids and all 34 clause ids unchanged; no task added/removed/renumbered (still 37 rows, 5 stories, 34 green claims); no new carrier, store, root or engine.
- `w2c-03` (rejected) left unrepaired by design.

## 5. Assumptions (unattended; no user adjudication)

1. **"既有 deadline grace" = the watcher's `--deadline-grace`** (default 120 s, pre-existing and preserved by FR-014/C-13). The repair names it in requirements/contract text as C1's reclassification window; it is not a settle-action option, because the settle action is a one-shot read-only judgment and does not wait.
2. **C3 start record is the seat's E2 record or the same label's existing C1/C2 start evidence** — E2 already enumerates carrier `c3-team-seat`, and the requirements state C3 seats are dispatched through C1/C2; writing a second record for the same attempt would violate the one-attempt-one-record shape, so reuse is the consistent reading.
3. **verification-input.md naming follows the spec-105 precedent** (crew input `test-evidence/verification-input.md`, spec-side `verification.md` materialization), keeping DoD-8/GATE-4 satisfied without granting the crew a forbidden path.

## 6. Residual risk / open items

- `w2c-03` (rejected HIGH) remains open: C-15's "completion declaration" is still undefined against research R-03's optional `<label>.settlement`; repairing it was explicitly out of scope.
- Round-2 MEDIUM/LOW findings outside the authorized 5 remain open.
- The C3 start record is a **behavior obligation on `run-team` text** discharged at T017; until implementation, the engine cannot settle a C3 seat that dies before its report row (pre-implement stage — expected).
- The no-pid observation window for non-C1 carriers is bounded by the parent's settlement obligation (FR-011), not by a declared duration. If review wants a settle-side reclassification duration, that is a new C-25 option and a spec revision, deliberately not invented here.
- The coverage accountant's rc 1 (`fr-uncovered` 37/41, `clause-unparsable` 111) is the documented structural verdict, identical to the frozen tasks-stage reading; it is reported honestly and not used as a pass criterion.

## 7. Fast-fail anomaly line

未发现异常 — no decision-class anomaly and no in-passing correction was needed; all edits are the authorized repair of the 5 confined findings.
