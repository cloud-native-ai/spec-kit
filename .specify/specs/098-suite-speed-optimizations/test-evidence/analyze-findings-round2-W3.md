# Analyze Findings — Round 2, Wave W3 (098-suite-speed-optimizations)

- Feature: 098-suite-speed-optimizations
- Round: 2 (post-repair re-gate; one-round limit)
- Read domain: `.specify/specs/098-suite-speed-optimizations/tasks.md` (sole file read for detection)
- Contract: `.specify/skills/internal/analyze-artifacts/SKILL.md`
- Scope: detection passes A (duplication) / B (ambiguity) / C (underspecification) / E (coverage) / F (inconsistency) / G (relevance) / I (decision tension) applied at tasks.md scope. Cross-artifact passes (requirements.md, plan.md, feature registry, checklists, constitution), the clause-coverage accountant, and round-1 residue enumeration are outside this wave's read domain; they are owned by the merged round-2 report.
- Read-only: no artifact was modified; this file is the only write.

## Mechanical verification (2026-11-10)

- 61 task rows, T001–T061 contiguous; 60 `[ ]` + 1 `[~]` (T061, carrying the deferred comment).
- 68 `[green:]` claims over six contracts (16/9/12/11/10/10); every clause claimed exactly once, no duplicate, no non-canonical clause id, every task row on one physical line.
- All `[blockedBy:]` targets resolve; no dependency cycle.
- Phase sizes 3/10/10/7/12/12/7 (all ≤ 16); WP-1…WP-9 plus "Setup / closure handoff" cover all 61 rows exactly once.
- FR-001…FR-027 and SC-001…SC-011 tables are complete; every task id referenced there resolves.
- The only table-vs-row divergence found is § Clause Attribution (W3-01).

## Findings

| ID | Severity | Anchor | Fact (one line) | Suggested attribution |
|----|----------|--------|-----------------|-----------------------|
| W3-01 | MEDIUM | tasks.md:395–396 vs :89, :91, :108, :112–114 | The § Clause Attribution "Claiming rows" column contradicts the actual `[green:]` tags on 14 clause rows — slow-membership C-005…C-009 are attributed to T010 but tagged on T012; parallel-consistency C-001…C-006 and C-009…C-011 are attributed to T014/T015/T016 but all nine carry T017 (C-007/C-008 match at T061) — while the tag partition itself is exactly-once 68/68, so the stale side is the table. | tasks repair: reconcile § Clause Attribution with the row tags (row tags are the machine-checked partition) |
| W3-02 | MEDIUM | tasks.md:91 (T012), :118 (T021), :287–289 | T012 declares it runs `test_suite_tier_contract.py` "(obligations 1–11)" with blockers T010/T011 only, but obligation 11's two cases are appended only at T021 (US2) and the Implementation Strategy completes US1 (T004–T013) before US2 — T012's declared run scope includes cases that cannot yet exist. | tasks repair: narrow T012's stated scope to obligations 1–10, or move/couple T021's authoring ahead of T012 |
| W3-03 | MEDIUM | tasks.md:373, :92 (T013), :118 (T021) | The TS-M1…TS-M8 carrier names T021 as a guard row, but the only drill row T013 is blocked by T012 only and sits in US1 before T021 (US2); any TS leg carried by T021's cases is unexecutable at its declared drill row, and no per-leg split across T004/T010/T021 is stated. | tasks repair: state the per-leg guard mapping and either drop T021 from the TS carrier or add a drill row after T021 |
| W3-04 | MEDIUM | tasks.md:170 (T037), :161 (T031), :247 | T037 changes the `wait_until` defaults (the change that makes event-wait C-006/C-007 green) but declares no `[blockedBy: T031]`, the row that authors the red default assertions; the file's test-first chain list (T031→T032) does not cover this change, so the graph permits the change to land before its red case. | tasks repair: add `[blockedBy: T031]` to T037 and list the chain in § Within Each User Story |
| W3-05 | LOW | tasks.md:215–216 (T055/T056), :257 | T055 is `[P]` with no blocker, yet it records from T003's slot-1 reading and writes `test-evidence/tier-measurements.txt`, the same evidence file T056 writes; the `[P]` premise (different files, no incomplete dependency) and the input dependency are undeclared as written. | tasks repair: add `[blockedBy: T003]`, drop `[P]`, or split the evidence target from T056 |
| W3-06 | LOW | tasks.md:218 (T058), :220 (T060), :237 | T058 (`[P]`, interface evidence must show `--full` in `--help` and the undeclared-option exit) and T060 (quickstart S-1…S-13 across all five mechanisms) declare no `[blockedBy:]`; their prerequisites (T005/T012; the story completion rows) are enforced by phase narrative only. | tasks repair: declare the missing blockers |
| W3-07 | LOW | tasks.md:9 vs :16 (DoD-2) and :31 (GATE-5) | The Tests Mode layer statement says "5 new guard files + the tier contract file", while DoD-2 and GATE-5 enumerate five files total including `test_suite_tier_contract.py`; the statement either overcounts by one or uses "+ the tier contract file" for a contract document without saying so. | tasks repair: align the layer statement with the five-file enumeration |
| W3-08 | LOW | tasks.md:11 vs :300–311 (Work Package Mapping) | The Organization line maps "WP-9 → Polish and the closure-stage row", but the package table places T061 in the separate "Setup / closure handoff" package and places T003/T022 inside WP-9. | tasks repair: align the Organization line with the package table |
| W3-09 | LOW | tasks.md:29 (GATE-3 check) | GATE-3's check is phrased "`grep -cE …` returns 0"; `grep -c` prints `0` but exits 1 when no line matches, so a literal exit-status reading inverts the gate verdict. | tasks repair: phrase the check as printed-count 0, or use `! grep -qE …` |

## Severity floor and validation

- CRITICAL: 0. HIGH: 0. MEDIUM: 4 (W3-01…W3-04). LOW: 5 (W3-05…W3-09).
- No CRITICAL/HIGH finding exists in this wave, so the independent C/H validation wave is not triggered by W3; the merged round-2 report owns the residue enumeration for round-1 MEDIUM/LOW findings.
