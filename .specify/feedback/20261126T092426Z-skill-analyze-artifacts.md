---
id: "20261126T092426Z-skill-analyze-artifacts"
unit_id: "skill:analyze-artifacts"
unit_type: "skill"
run_id: "r20261126T092355Z-108ar2"
scope: "local"
probe: "skill-analyze-artifacts-wrapup"
kind: "internal"
slice: "skills"
feature: "108-team-view-degradation"
feature_id: "108"
partial: false
created: "2026-11-26T09:24:26Z"
summary: "Analyze-repair round 2 for 108-team-view-degradation (analyze gate, 2 validator-confirmed HIGH findings R2-108-W1-01 + R2-108-W3-01)."
---

## Review
Analyze-repair round 2 for 108-team-view-degradation (analyze gate, 2 validator-confirmed HIGH findings R2-108-W1-01 + R2-108-W3-01).

(1) R2-108-W1-01 — the timestamp-grammar contradiction. FR-001's closed set of five accepted forms contradicted its own parenthetical decomposition: "date part YYYYMMDD or YYYY-MM-DD x time part hhmmss / hhmm / hh:mm:ss / hh-mm-ss" expands to 8 combinations, three of which the enumerated five reject, and the Clarifications answer restated the same 8-way cross product. The decomposition now pairs compact date `YYYYMMDD` only with compact times (`hhmmss` / `hhmm`), and ISO date `YYYY-MM-DD` with the three time shapes (`hh:mm:ss` / `hh-mm-ss` / `hhmmss`) — exactly the five enumerated forms, with "五种之外无其它组合"; the Clarifications answer carries the same grouping and names FR-001 as owner. contracts/report-recognition.contract.md C-201, data-model.md C2 and research.md R-1 already carried the correct five forms and needed no edit.

(2) R2-108-W3-01 — the verification.md territory contradiction. Tasks T029 / DoD-1 / DoD-8 / GATE-4 required producing verification.md while both territory contracts forbid that path to every crew seat, and T028 read its baseline commit from that file although T029 is blockedBy T028. Per the 106/107 established pattern, T029 now assembles the crew-writable `test-evidence/verification-input.md`; `verification.md` is derived spec-side from that input and stays forbidden. DoD-1, DoD-8, the task-state sigil, the evidence landing points, the checkpoint and the incremental-delivery line were reworded to that boundary; GATE-4 still checks the derived artifact with an explicit derivation annotation. T028 now uses the literal baseline `54c6efa8c` recorded in DoD-6/FR-022, removing the read-before-producer dependency. handoff.md (Task Reference + forbidden-list explanation) and team.md (Dynamic Structure) carry the same split in the 106/107 wording.

Machine evidence: validate-requirements 0 error / 0 warning; pre-analyze-check requirements/plan/tasks all decision=pass errors=0 (70 advisories, finding set identical to round 1 — 40 external-clause / 30 missing-path, all pre-existing); validate-tasks PASS 0/0; decomposition plan+tasks decision=proceed (25 FR / 29 tasks); a 46-check resolution probe reads ALL PASS. Invariants held: FR 25 / SC 8 / STR 3, 35 clause ids, the reason set and exit-code set, task count 29 and every task status are unchanged; no implementation, no tests run, no dispatch, no push; dated records untouched; the other round-2 domain findings (W1-02..W1-06, W2-01..W2-06, W3-02..W3-06) remain open by design.

## Optimization Points
- process: R2-108-W1-01 lived in FR-001's parenthetical decomposition and the Clarifications answer while the contract, data-model and research already carried the correct five forms — the drift was between prose and enumeration inside the same requirement. A requirements-validation check that expands any "A or B × C" phrasing into its cross product and compares it against the adjacent enumerated set would make this contradiction machine-detectable at the requirements stage.
- process: R2-108-W3-01 is a territory-vs-task-list contradiction that had already been repaired once in 106 and 107; 108's tasks were generated after those repairs yet reintroduced the crew-writable verification.md sink. The tasks validator could reject any task row that names a path in the team's forbidden set — the data already exists in handoff.md / team.md.
- token-efficiency: round 2's verdict is reproducible from the committed 46-check probe (test-evidence/analyze-repair2-resolution-probe.txt) plus the three validator records; later rounds can re-run the probe instead of re-deriving readings by re-reading the artifacts.
- process: pre-analyze-check returns the same 70 advisories for the requirements, plan and tasks stages and the set was identical before and after this repair, so stage-level adjudication keeps repeating one explanation three times; a stage-scoped advisory profile or a recorded waiver set would cut the repetition without hiding findings.
- process: round 1's repair record transcribed its advisory split as 38 external-clause / 32 missing-path while its own JSON held 40/30 — a record-writing helper that copies counts from the engine summary instead of retyping them would prevent that drift class.
