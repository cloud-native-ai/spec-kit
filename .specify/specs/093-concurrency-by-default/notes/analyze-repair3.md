# Analyze-repair — round 3 (093-concurrency-by-default)

**Stage**: analyze-repair round 3 (the stage implied by analyze round 3's FAIL verdicts)
**Branch / worktree**: `093-concurrency-by-default` @ `.specify/.tmp/sdd-loop/worktrees/093-clarify`
**Base commit**: `c7a8ac4f` (the round-3 verdict record; verifier HEAD `8c90088c`; analyze notes at `notes/analyze-round3/`)
**Date**: 2026-11-09
**Inputs**: `notes/analyze-round3/v1b-manifest.md` (3 MEDIUM gaps), `notes/analyze-round3/v3b-consistency.md` (V3B-F1/F2), `notes/analyze-repair2.md`, `plan.md`, `tasks.md`, `quickstart.md`, `notes/analyze-round2/v2-gates-directive.md` § C (the 20-surface list), and the measured framework surfaces they name.
**Execution shape of this stage**: serial, one executor; no subagent dispatched. The feature's own mechanism has not landed, so this stage's record is `mechanism-not-yet-landed` ([[STR-010]]) and SC-006 stays `not_evaluated` — no concurrency is claimed. Framework sources were read, never edited: every surface correction is an implement-stage row.

---

## 0. Repair verdict

**V1B (3 MEDIUM manifest gaps) CLOSED.** Each of the three baseline surfaces whose pre-existing rows named it without carrying the carrier requirement now has a dedicated implement row: **T153** (`decomposition-model.md` § 13.4), **T154** (`stage-team-preset.md` `stage-worker` line), **T155** (`subagent-definitions.md` mode selection). Every new row names the exact surface path and line anchor, requires the fork carrier (same-family `qodercli` child processes through `scripts/stage-runner.sh`) and the subprocess carrier (heterogeneous agents), and states the host-internal in-process ban. The plan manifest rows 4/6/16 now carry the new row ids and the round-3 severity, so the 20-surface table maps surface → row without a silent "already scheduled" cell.

**V3B CLOSED.** V3B-F1 (MEDIUM): T006 now states the **measured 94** clause definitions (18+22+22+18+14, re-measured today with the row's own command) and instructs re-reading the count in the same command. V3B-F2 (LOW): `quickstart.md:8` now points at **S-0 and S-1** — both real scenarios; **S-9 was not added** (the page defines S-0…S-6 and `plan.md:331` declares "7 scenarios (S-0…S-6)", so adding S-9 would have opened an S-7/S-8 gap and contradicted the plan count).

Counts after this pass: tasks **152 → 155** (three document rows, all inside the existing `WP3-owners`); FR **35** unchanged; contract clauses **94** unchanged; packages still **5**. No gate was weakened, no coverage baseline was frozen, and no framework source was edited.

---

## 1. V1B closure (per id)

| id | severity | surface (measured today) | correction | anchor |
|----|----------|--------------------------|------------|--------|
| V1B-F1 | MEDIUM | `skills/external/sdd-loop-driver/references/decomposition-model.md` § 13.4 (~L184): "Local: one native host subagent per package through the existing `run-agent` dispatch path. No external CLI is launched locally; when the host cannot issue parallel native calls, the serial fallback above applies." | **Row T153 added**: names § 13.4 explicitly, quotes the old sentence, rewrites the local carrier to fork (same-family `qodercli` through `scripts/stage-runner.sh`) + subprocess (heterogeneous, independent child of the agent's own CLI), bans the host-internal in-process path as a concurrency carrier, keeps the remote topology and SD-13/SD-15 unchanged, and cites the recorded FR-035 conflict. **T140 keeps its § 20.1 scope** (the analyze `off`→N default) — the two sections no longer share one row. | `tasks.md` T153; `plan.md` manifest row 4 → `T140, T153` |
| V1B-F2 | MEDIUM | `skills/external/sdd-loop-driver/templates/stage-team-preset.md` L74: "`stage-worker` is filled by one execution per Work Package (**a native subagent locally, one detached runner remotely**)." | **Row T154 added**: names the preset and the `stage-worker` fill sentence (~L74), requires fork as the local form and subprocess for heterogeneous agents, bans the in-process path as a carrier, and leaves the seat structure and the slot-cap projection line untouched. T116/T133 keep their obligations (team obligation + slot pointer). | `tasks.md` T154; `plan.md` manifest row 6 → `T116, T133, T154` |
| V1B-F3 | MEDIUM | `shared/definitions/subagent-definitions.md` `## Three Execution Modes` ("**Native** is the default whenever the executing runtime supports it") and `## Mode Selection` ("Parallel fan-out … External (or native parallel calls when the runtime supports them …)", "When in doubt: **native first** …") | **Row T155 added**: names the file and all three old statements, makes the parallel forms the fork and subprocess carriers, and bans the host-internal in-process path as a concurrency carrier; the Visibility Contract and the session-creation-API prohibition stay unchanged. T037/T060/T099/T132 keep their capability/mode content. | `tasks.md` T155; `plan.md` manifest row 16 → `T037, T060, T099, T132, T155` |

Judged against V2's stated rule (a surface is covered only when a row names the exact surface path and its wording requires the fork carrier **and** bans the in-process path): T153, T154 and T155 each satisfy all three clauses. None carries a `[green:]` tag — C-094 is claimed exactly once by T142 and a second claim would trip `green-clause-collision` (the marker reading, DoD-1); each row cites `(FR-035, C-094)` in its text, like T144–T152.

**Manifest-side encoding.** `plan.md` § Complete-correction manifest: rows 4/6/16 now read `T140, T153` / `T116, T133, T154` / `T037, T060, T099, T132, T155` with the correction content named; the severity cell for each moved from "—" to "MEDIUM (round-3 re-measure)"; the appendix sentence now reads "Task rows T144–T155 … appended in Phase 8" and records that T153–T155 close the round-3 re-measure.

---

## 2. V3B closure (per id)

| id | severity | finding | fix (in place — both are live artifacts, not dated records) | anchor |
|----|----------|---------|----------------------------------------------------------|--------|
| V3B-F1 | MEDIUM | T006's expected value "confirm **92** clauses" contradicted the corpus (94 after C-093/C-094), at the very step that freezes the clause-coverage baseline. | Rewritten to "confirm **94** clauses … (measured 2026-11-09: 18 declaration-facts + 22 judgement-engine + 22 executor-obligations + 18 high-order-executors + 14 existing-semantics-disposal = 94 …)", with an instruction to re-read the count in the same command rather than trusting the figure. Re-measured today with the row's own command: **94**, per-file 18/22/22/18/14. | `tasks.md` T006 |
| V3B-F2 | LOW | `quickstart.md:8` cited scenario "S-9", which no revision of the page defines (the page defines S-0…S-6; `plan.md:331` states "7 scenarios (S-0…S-6)"). | Reference fixed to "**S-0 and S-1**". S-0 is the scenario that demonstrates the unregistered-fact red (`--action get --fact concurrency-class` exits 1, C-039); S-1 is the first downstream scenario that assumes the fact exists. **S-9 was not added**: a new S-9 would require S-7/S-8 and would contradict the plan's 7-scenario count. | `quickstart.md:8` |

---

## 3. Verification-local ids and promotion mapping

`V1B-F1…F3` and `V3B-F1…F2` are **verification-local ids** (the round-3 notes declare them findings of the verification workers, not registered F-093 ids). Every one closes inside this repair, so no new `F-093-*` number was coined; one grouped register row (`V1B/V3B@093-analyze-round3`) points here, following the round-2 precedent.

| local id | closure | durable anchor |
|---|---|---|
| V1B-F1 | implement row | `tasks.md` T153; `plan.md` manifest row 4 |
| V1B-F2 | implement row | `tasks.md` T154; `plan.md` manifest row 6 |
| V1B-F3 | implement row | `tasks.md` T155; `plan.md` manifest row 16 |
| V3B-F1 | fixed in place | `tasks.md` T006 |
| V3B-F2 | fixed in place | `quickstart.md:8` |

---

## 4. Gate readings (post-repair, explicit flags)

Full command lines, stdout/stderr and exit codes are retained under `test-evidence/analyze-repair3-*`.

| # | Gate (explicit flags) | Reading | Verdict |
|---|----------------------|---------|---------|
| G1 | `validate-requirements.py .specify/specs/093-concurrency-by-default/requirements.md` | `status: ok` — `[id-contiguous]` `[doc-order]` `[ref-resolvable]` `[marker-count]` `[dup-id]` `[path-marker]` all `pass (0)`; 337 lines / 47 definition rows / 11 shared strings; **0 error / 0 warning**, EXIT 0 | PASS |
| G2 | `account-clause-coverage.py .specify/specs/093-concurrency-by-default --corpus-root <worktree>/.specify/specs` (no `--freeze`) | `status: baseline-missing`; `[fr-uncovered] pass (0) — 35 of 35 FRs cited from citation groups`; `[clause-uncovered] fail (656)`, `[clause-unparsable] fail (116)`, `[coverage-baseline-delta] fail (656)`; 657 errors / 1 warning, EXIT 2 — the clause lane's declared expected state (no baseline exists; T006 owns it) and **no baseline file was created** | PASS on the FR lane; clause lane red-by-baseline-missing, expected |
| G3 | `validate-tasks.py .specify/specs/093-concurrency-by-default/tasks.md` | `PASS — 0 error(s), 0 warning(s)`, EXIT 0 (155 rows) | PASS |
| G4 | `validate-decision-tensions.py --spec .specify/specs/093-concurrency-by-default` | `status: ok` — every rule `pass (0)`; 5 records T-001…T-005; **0 error / 0 warning**, EXIT 0 | PASS |
| G5 | `pre-analyze-check.py --repo <worktree> --spec-dir .specify/specs/093-concurrency-by-default --stage requirements` / `plan` / `tasks` | all three `decision=pass`, **0 errors**, 112 advisories (the same creation-target + dated-history set as round 2), `fr=35 / sc=12 / tasks=155`, EXIT 0 | PASS |
| G6 | `decomposition-check.py --mode tasks --requirements …/requirements.md --tasks …/tasks.md` | `{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 35, "task_count": 155, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": []}`, EXIT 0 | PASS |
| G7 | Structural self-check (row contiguity + package partition) | **155** rows, T001…T155 contiguous, ascending, unique; package map an exact partition: WP1 16 + WP2 26 + WP3 27 + WP4 37 + WP5 49 = **155**, 0 missing, 0 extra; T153–T155 inside `WP3-owners`, whose declared write domain already lists all three files (`decomposition-model.md`, `stage-team-preset.md`, `subagent-definitions.md`) — no new package and no write-domain change | PASS |

Evidence files: `test-evidence/analyze-repair3-validate-requirements.txt`, `…-validate-tasks.txt`, `…-decision-tensions.txt`, `…-pre-analyze-{requirements,plan,tasks}.txt`, `…-decomposition-tasks.txt`, `…-account-clause-coverage.txt`. Every earlier green reading stayed green; task-ceiling headroom is now **5 rows** (155/160) — the closest split trigger.

---

## 5. Fast-fail decisions in this pass

**Repaired in passing, disclosed** (each is one reading of the recorded verdict):
1. The manifest severity cells for rows 4/6/16 moved from "—" to "MEDIUM (round-3 re-measure)": leaving "—" would let the table read as if those surfaces were never found missing, contradicting V1B's grades.
2. The phase-gating prose in `tasks.md` extended from "T144–T152 implement the same FR-035 ruling" to "T144–T155 …", recording the round-2 vs round-3 origin split, so a phase reader sees the three new rows.
3. Both "152 rows" live-count references updated to 155 (`tasks.md` § Work Packages prose and § Package size); the **dated** round-2 run record keeps its "152" and a new round-3 run-record bullet carries "over 155 rows" — dated records are annotated forward, never rewritten.

**Refused (surfaced, not absorbed):**
1. Editing the three framework surfaces in place — outside the spec dir; they are T153–T155's subject (implement stage).
2. Adding a scenario "S-9" to quickstart — it would need S-7/S-8 and would contradict `plan.md:331`'s "7 scenarios (S-0…S-6)".
3. Rewriting the round-2 dated run record's 152 — a dated record, not a live count.

**Anomaly line**: **ANOMALY: none unreported.** The prompt's stated base commit (`8c90088c`) is one commit behind the actual HEAD (`c7a8ac4f`, the round-3 verdict record); this ledger records the actual base. Known residuals are in § 6, not buried.

---

## 6. Residual risks

- **The old rule still ships until implement lands T144–T155.** The three surfaces re-measured in round 3 (`decomposition-model.md` § 13.4, `stage-team-preset.md` L74, `subagent-definitions.md` mode selection) still read the local-native rule on disk, and the four contract tests still pin the pre-ruling text. That is the intended state for a repair pass (analyze may not edit framework source); the rows are named, attributed and packaged (WP3-owners / WP4-tests).
- **Task-ceiling headroom is 5 rows** (155/160). Any further row addition must re-run `decomposition-check.py`; at ≥161 the decision flips to `split-required`.
- **Heterogeneous-agent carrier is form-only** (unchanged from round 2): FR-035 / C-094 state the subprocess carrier's judgment; no engine consumes it yet, and T143's fork contract does not assert the subprocess arm.
- **`DoD-1` totality sentence** (V3B § 9 observation 3) remains an observation, untouched here: "every contract clause C-001…C-094 is owned by at least one row" has no machine owner and "owned" is undefined. Out of this repair's scope; analyze round 4 may re-judge or the implement stage may scope it.
- **Claim-reading drift in dated records** (V3B § 9 observation 1) stays as recorded: `register.md` and the spine findings still carry "92 中的 35"; the live reading is 37 of 94. A future reader must re-measure, not lift the number.
