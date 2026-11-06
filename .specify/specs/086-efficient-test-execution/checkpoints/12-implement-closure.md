# Checkpoint 12 — implement closure (C2)

## 1. Artifact verification

- **C2** `93e61050` + `d30bfadf` on `line/086-wp-c2`, ff-merged into `086-efficient-test-execution` at
  `d30bfadf`; worktree removed; child line deregistered. Actual concurrency: **1** (single integration
  slice + verifier reserve).
- **Closure slot (T047)** — clean rerun after the sandbox contamination was removed:
  `19 failed, 7535 passed, 7 skipped in 284.12 s (0:04:44)` + serial exception pass
  `1 passed, 7561 deselected in 35.22 s`, exit 1, exactly 19 names; `comm -13` and `comm -23` both
  empty against the T050 baseline (687.41 s; 0.41× like-for-like, and 284.12 s ≤ SC-001's 412.59 s
  ceiling). The contaminated first attempt (21 names, 271.72 s) is recorded as
  `slot-2-in-slot-rerun-attempt` with its trigger and targeted disproof — not as a second slot.
- **Gates (T049)** — nine rows, nine PASS: GATE-086, GATE-1 (both comms empty), GATE-2 (six mirror
  pairs; runner carriers byte-identical), GATE-3 (0 open / 56 closed), GATE-4 (SC-001…008 pass +
  smoke triple), GATE-5 (only 085 `verification.md`; 6 lines, 0 non-matching), GATE-6 (runtime deps
  identical to merge base), GATE-7 (27 ≤ 27), GATE-8 (`accept`, exit 0).
- **`closure-acceptance-check.py`** — `verdict: accept`, `reasons: []`, `waived: []`, final_path
  pass 8 / total 8. Registry and detail flipped to **Implemented** on that verdict (C-052); no waiver.
- **085 SC-010** — stays `partial`; the named gap is "review stage has no record or checkpoint yet"
  (T041's four-line carve-out; GATE-5 proves nothing else moved). 086's SC-012 passes on that honest
  state, and `parallel-safety-attribution.md`'s M-18 leg shows `pass` would go red on the partial chain.
- **Record surfaces** — `verification.md` (flat `SC-NNN_status=` form), `completion-gate.txt`,
  `full-run-budget.md` (2 slots, 5 out-of-slot exceptions, 1 in-slot rerun attempt, 2 no-run rows),
  `preservation-085.txt`, `mirror-parity.txt`, `no-new-machinery.txt`, `worktree-clean.txt`,
  `tasks.md` 56/56 closed, `CHANGELOG.md` + feature registry/detail.

## 2. Driver rulings on C2's returned decisions

1. **T047 in-slot rerun** — ratified. The defect was the package's own sandbox worktree inside the
   repo root, not the feature tree; the slot record is the clean run, and the contaminated attempt is
   kept in the ledger with its trigger. No extra slot was spent.
2. **T048 flat form** — ratified. `SC-NNN_status=` is the machine-readable shape GATE-4 and
   `closure-acceptance-check.py` read; 081's flat form is the reference. The checker's `accept` is the
   authority for the `Implemented` flip, overriding the package's pre-written `Blocked` premise.
3. **Sandbox accounting** — ratified. The two completed M-16 real-suite-load sandbox reps are
   `out-of-slot-exception` rows; all doctored copies now live outside the repo root
   (`~/tmp/spec-kit/086/mutations-c2/`).

## 3. Disclosed limitations (carried to review)

- **SC-003** is read on the templates a freshly initialised project carries, not on a rendered
  `constitution.md`/`instructions.md`: at init those are a placeholder and absent, so grepping them
  would measure initialisation order, not delivery. The substitution is disclosed in
  `downstream-init.txt`; the review should judge whether to run a full downstream render.
- **DoD-2 backfill** — C2 found the carrier map named evidence files that did not exist and M-2…M-4 /
  M-10…M-15 had no readings; it produced the readings on doctored copies outside the repo (correction,
  disclosed). No tracked carrier was weakened.
- **GATE-6 interpreter** — the row's `python3 -c "import tomllib"` cannot run on this host's 3.9.6
  `python3`; the reading used `/opt/homebrew/bin/python3` (3.14.6) and was cross-checked against the
  merge-base `pyproject.toml`.
- **Runtime residue** — `.specify/memory/trigger/index.json` is a machine-managed trigger index that
  the session updated; it is not part of this feature and must not be committed. Restored after merge.

## 4. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| Full-suite parallel wall-clock ≤ 40% of the 1031.48 s serial baseline. | 100% | closure 284.12 s ≤ 412.59 s ceiling |
| Final parallel run has zero new failure names vs the serial baseline, serial exceptions declared. | 100% | `closure-diff.txt`; one declared serial exception |
| Principle ships in constitution template/live, instructions template/live, one owner guideline. | 100% | `mirror-parity.txt`; six surfaces green |
| 085 temporary Goal/Team, concurrency, worktree/integration queue and checkpoints are used and green. | 100% (pre-review) | `preservation-085.txt`; `dogfood-record.md`; SC-010 partial by design |
| Feature reaches Ready for Review with zero blocking review findings. | not_evaluated | review pending |

## 5. Team configuration review

- evidence: C2's two commits; the `accept` verdict; the nine gates
- symptom: the package's own sandbox polluted the first closure run and a pre-written `Blocked`
  premise contradicted the checker; both were surfaced instead of hidden
- proposal: no configuration change; review runs as one seat + verifier reserve
- ratification: n/a
- applied: no
- observations: mutation sandboxes must live outside the repo root (now a standing rule for later
  waves); the DoD-2 backfill is the second time a package reported a complete-looking carrier map
  without readings — review should check the newly produced readings.

## 6. Next stage concurrency / roster

- stage: review (last chain stage)
- requested: 24; effective: **2** (1 review seat + 1 verifier reserve); team cap 18 not binding
- stage max_parallel: 18; verifier reserve: 1; executor slots: 1
- review must re-read the feature's complete artifact chain, not the code alone; its findings decide
  whether SC-003's disclosed reading and the DoD-2 backfill stand, and it must not rewrite 085 paths.
