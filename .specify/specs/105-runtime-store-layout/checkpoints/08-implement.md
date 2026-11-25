# Checkpoint 08 — implement

## 1. Artifact verification

- **stage sentinel**: `IMPLEMENT-DONE` from the integrator (packages P1–P5 + bounded P5R)
- **independent verification**: `IMPLEMENT-VERIFY-DONE`; verdict table all PASS — 43/43 task closure (42 crew writebacks + spec-side T039), SC-001…SC-009 re-checked, regression `comm -13` NEW=0 / repaired=531 against the 748-name entry baseline, mirrors rc 0, guard/mutation restorations real, discipline clean
- **stage readings**: final fast tier 217 failed / 10042 passed / 3 skipped / 0 setup errors (all 217 are named pre-existing reds); `/usr/local/bin/python3 sync-mirrors.py --check` rc 0 / 0 drift members; `regen-command-copies.py --check` rc 0; retired root absent; 12 stores relocated with receipt v2
- **closure**: `closure-acceptance-check.py` → `verdict: accept` (final_path pass=6); `verification.md` SC-001…SC-009 pass with bound evidence hashes; one smoke triple; RS-001…RS-006 pass
- **commits**: P1 `5b445e916`; P2 `5bc8ed901` + `49899a018`; P3 `45d2ffdd9`; P4 `6a62a8c3a` + `10108ab8d`; P5 `6b442ed97`; P5R `1e6dc208c`; spec-side closure `c8e73add7`
- **workspace**: clean tree at the integrator's close; no push
- **anomaly**: one driver-adjudicated correction (P5R resume supersession) closed; package disclosures recorded in the state spine

## 2. Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| FR/SC delivery (anchor criterion 1) | 27 FR / 9 SC implemented and independently verified; closure accept | requirements/tasks/verification/acceptance-105 |
| Migration safety (criterion 2) | relocate/refuse/block/resume all tested; dogfood migrated 12 stores; third-apply idempotence closed | t016-us2-readings, p5r-resume-idempotence, dogfood |
| Memory/injection preservation (criterion 3) | record→recall on new roots; seven/four/five injection fields; reverse-token proof | t020-us3-readings, t018-red-run |

## 3. Team configuration review

- **evidence**: serial crew executed five packages + one repair; writebacks 42/42; one broad-staging attribution defect (feedback entries swept into a package commit) disclosed
- **symptom**: serial-only pattern left two dependency-independent packages sequential (efficiency, not correctness)
- **proposal**: feed the recorded efficiency entries; no in-run team change
- **ratification**: n/a
- **applied**: no

## 4. Next stage concurrency / roster

- **requested**: 1; **effective**: 1; **reason**: `single-unit`
- **next**: `review` — dispatch the `/speckit.review` execution with the four segments + acceptance reality check; driver retains U4.

## 5. Direction audit

- **reload tier**: T0+T1
- **Q1 rules**: in force — unattended/no approval, U4→next, spine-before-action, workspace guard, fast-fail, gates, budget/report; push forbidden.
- **Q2 process**: on-track — TDD red-first rows, mutation drills, independent verification, closure accept.
- **Q3 next action**: on-track — review is the final quality gate before U6.
- **Q4 spine freshness**: on-track — implement verification and integration recorded before this checkpoint.
- **Q5 territory/workspace**: on-track — crew stayed inside the handoff grant; one attribution defect disclosed, no content impact.

## 5b. Published-state check

- **scope**: n/a — no history correction; no push authorized.
