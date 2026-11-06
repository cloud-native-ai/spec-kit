# Checkpoint 11 — implement wave 4 (C1)

## 1. Artifact verification

- **C1 first commit** `05ae56ca` — watch-target self-test carries the registered `serial` marker
  (body/timeout unchanged), nested-runner integration case added, `dogfood-record.md` (085 temporary
  Goal/Team per stage, concurrency from dispatch records, carrier downgrade as an observation),
  `parallel-safety.txt` (T014: 19/19 names, `comm -13`/`comm -23` both empty, 206.12 s vs the 687.41 s
  T050 baseline = 0.30×).
- **C1 repair commit** `bf455401` — driver-authorised root-cause fix for the executor's load-bearing
  anomaly: the runner appended `--dist load` on top of a caller-supplied `--dist loadfile`, so T016
  could not measure the arm it named. C-009 now guards `--dist`/`--dist=<value>`, forwards the caller's
  scheduler verbatim and names it in the mode line; two new contract cases (40/40 pass), plus
  `parallel-safety-attribution.md` (0 new names, 0 unattributed) and `scheduling-experiment.txt`.
- **T016 result** — two representative arms on one selection: `-n auto --dist load` (parallel pass
  201.34 s) vs `-n 8 --dist loadfile` (204.99 s); identical 19 names, `comm -3` empty, new names vs T050
  baseline 0 for both. Decision: default stays `-n auto` + `--dist load`; no cap, no scheduler switch.
- **085 re-run (T040)** — five named files, 20 passed, 0 failures, 0 new names vs baseline.
- **Serial exception** — `pytest -m serial --collect-only -q` enumerates exactly one node id
  (`1/7562 collected`); C1-owned tests 27/27 pass; runner-contract suite 40/40 pass.
- **Integration**: C1 ff-merged into `086-efficient-test-execution` at `bf455401`; worktree removed;
  child line `086-wp-c1` deregistered. Actual concurrency in this wave: **1** (C1 alone).

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| Full-suite parallel wall-clock ≤ 40% of the 1031.48 s serial baseline. | 100% | T050 687.41 s; T014 206.12 s = 0.30× |
| Final parallel run has zero new failure names vs the serial baseline, serial exceptions declared. | 100% (pending closure re-read) | `parallel-safety.txt`, `scheduling-experiment.txt`, `parallel-safety-attribution.md`; T047 re-reads |
| Principle ships in constitution template/live, instructions template/live, one owner guideline. | 100% | B1+B2+B3 integrated; 191/1 clean |
| 085 temporary Goal/Team, concurrency, worktree/integration queue and checkpoints are used and green. | 90% | waves 1–3 (2/3/2-way); checkpoints 01–11; `dogfood-record.md`; T041/T043 evidence pending in C2 |
| Feature reaches Ready for Review with zero blocking review findings. | not_evaluated | C2 then review |

## 3. Team configuration review

- evidence: C1 child line/worktree/integration; the driver's guard repair on an executor-reported anomaly
- symptom: the WP-C1 executor correctly stopped at a cross-package contract decision instead of
  patching around it (Fast Fail honoured)
- proposal: no configuration change; C2 remains one integration slice + verifier reserve
- ratification: n/a
- applied: no
- observations: the C-009 guard set was under-specified for `--dist`; the contract is now the owner of
  the scheduler guard. The previous caller pitfall (relative `SPECKIT_PYTHON`) still applies — C2 must
  pass an absolute path or unset it.

## 4. Next stage concurrency / roster

- stage: implement (C2, last package)
- requested: 24; effective: **2** (1 executor + 1 verifier reserve); team cap 18 not binding
- stage max_parallel: 18; verifier reserve: 1; executor slots: 1
- C2 scope: T038/T041/T042/T043/T044/T045/T047/T048/T049/T054/T055, registry/features/CHANGELOG,
  closure full run (slot 2), 085 SC-010 carve-out edit only.
