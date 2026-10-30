# Verification Log — 078-coaching-skills

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=d0f50759
baseline_date=2026-10-30
baseline_branch=078-coaching-skills
baseline_commit_derivation=the requirements-fix commit the analyze-loop rebaseline event names in `.specify/state/078-coaching-skills.md` (`<!-- rebaseline-events -->`), and the `BASE` the plan/quickstart pin for the SC-008 new-line gate; it is the last commit before the first implementation edit and an ancestor of HEAD (`git merge-base --is-ancestor d0f50759 HEAD` exit 0)
baseline_full_suite_passed=6810
baseline_full_suite_failed=16
baseline_full_suite_note=the single implement-start full-suite slot (E2); the 16 names are frozen in `baseline-failed.txt` and are pre-existing reds unrelated to this feature — the seven frozen-roster reds this feature owns are the ones counted next
baseline_frozen_roster_reds=7
baseline_gate_blocking_total=27

# -- /speckit.implement results --

implementation_date=2026-10-30
post_change_commit=this file rides the part-4 commit; resolve it with `git log --oneline -- .specify/specs/078-coaching-skills/verification.md`
post_change_frozen_roster_reds=0
post_change_targeted_passed=162
post_change_targeted_failed=0
post_change_new_failures=0
post_change_gate_blocking_total=27
post_change_gate_violations=0
post_change_new_line_added_lines=475
post_change_new_line_blocking_hits=0
post_change_skill_shape_tokens=3278

# -- Evidence records (bind every `pass` claim to archived evidence) --

sample_id=SC-001
evidence_path=.specify/specs/078-coaching-skills/test-evidence/sc001-run-artifacts.txt
evidence_sha256=c041ccee01f7980d74130352e0c82d7b90f9e7adad9e94208f785a5385b75ca1
verdict=pass

sample_id=SC-002
evidence_path=.specify/specs/078-coaching-skills/test-evidence/sc002-ordering.txt
evidence_sha256=6cfe2e654aa8722b887dde45b0d0b934432da50dc066897aedfbc94dc1049ab2
verdict=pass

sample_id=SC-003
evidence_path=.specify/specs/078-coaching-skills/test-evidence/sc003-deviations.txt
evidence_sha256=396a02d2d88ff571e858d94e6f4a39d6e8d28530cde879b0475e65235452681d
verdict=pass

sample_id=SC-004
evidence_path=.specify/specs/078-coaching-skills/test-evidence/sc004-observation.txt
evidence_sha256=857a65af67a431316688e67b20b61ea5f9a68e66a3559de8874ca148fc7a1351
verdict=pass

sample_id=SC-005
evidence_path=.specify/specs/078-coaching-skills/test-evidence/sc005-degraded.txt
evidence_sha256=d80c9cd59e1b535d90d07bb8ebe1afb1f5fbc523fe0b2795c318fe69818f490c
verdict=pass

sample_id=SC-006
evidence_path=.specify/specs/078-coaching-skills/test-evidence/sc006-identity-and-residual.txt
evidence_sha256=2adb8ee8c6f05df8ffa282de5616f2378cfd3f8229e22c9f2f96a044bf47d64d
verdict=pass

sample_id=SC-007
evidence_path=.specify/specs/078-coaching-skills/test-evidence/sc007-upgrade-fixture.txt
evidence_sha256=5c5b38e73d442da92aa499339bd1f2b531ae508016ec79725d96d2211fbedb70
verdict=pass

sample_id=SC-008
evidence_path=.specify/specs/078-coaching-skills/test-evidence/sc008-drift-and-newline-gate.txt
evidence_sha256=f30ed1d7065c1446cc9272bb3cbfe1e8a51eb63caf837d4c2ef8caa0d5ea3b03
verdict=pass

sample_id=SC-009
evidence_path=.specify/specs/078-coaching-skills/test-evidence/sc009-frozen-baselines.txt
evidence_sha256=9d6c5d4ed7814e36ba6b8e40d2e899aa927dc8e256458ecffde048c9f68e9968
verdict=pass

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=4/4 artifacts + 1/1 primary artifact
SC-001_note=the real fixture run produced `expectation.md`, `observation.md`, `deviations.md`, `improvement-plan.md` under `.specify/memory/coaching/20261030T083250Z-fixture-trainee/` and its Trainee artifact `checklist.md`; the run-shape validator returned no error; see notes/quickstart-run.md § Scenario 2 and test-evidence/sc001-run-artifacts.txt

SC-002_status=pass
SC-002_value=ordering holds 1/1; negative control 1/1
SC-002_note=`expectation.md` mtime 1793349175.2307684 (= 08:32:55.230768Z) is strictly earlier than `dispatched-at` 08:32:58.017522Z; the validator's ordering leg reported no error, and `test_c4_validator_rejects_missing_expectation_and_second_dispatch` (missing expectation / two dispatches) passes as the negative control

SC-003_status=pass
SC-003_value=2/2 dimensions
SC-003_note=`D-1` result-deviation (4 of 5 rows; evidence S6 + checklist.md; high) and `D-2` process-deviation (5 brief reads; evidence S1-S5; medium); both dimension sections present and each finding cites a step id or artifact path

SC-004_status=pass
SC-004_value=gap marker 1/1; invented steps 0
SC-004_note=the contract guard pins the marker to step rows only, counts it once and rejects a repeated marker or a stale count; the real run recorded `gap-count: 0` with seven rows all `source: self-report` and added no step the runner's event log does not contain

SC-005_status=pass
SC-005_value=primary artifact 1/1; `optimization: unavailable` 1/1
SC-005_note=with `improve-skills` removed from both layers (`skills/external`, `skills/internal` and the `.specify/skills` mirror), the degraded run still delivered the Trainee artifact and closed `run: partial` + `optimization: unavailable` — never `failed`

SC-006_status=pass
SC-006_value=8/8 coordinates; 1 surviving occurrence
SC-006_note=the guard copy passes all eight coordinate judgements and derives its candidate faces at run time (22 faces / 1608 files, 0 live occurrences); the diagnostic repo grep over A10's 19 hand-edited sources finds exactly one hit, `src/specify_cli/__init__.py:892` — the `_OBSOLETE_SKILLS` tuple entry (`notes/residual-audit.md`)

SC-007_status=pass
SC-007_value=2/2
SC-007_note=on a disposable fixture, `cleanup_obsolete_framework_assets` removed the entity directory and left a user-authored symlink of the same name (and its target) untouched; the two contract guards under `-k cleanup` pass in the same run

SC-008_status=pass
SC-008_value=3/3
SC-008_note=`sync-mirrors.py --check` and `regen-command-copies.py --check` both exit 0 (zero drift); the new-line gate over `BASE=d0f50759` reads `added_lines=475 blocking_hits=0` (exit 0) against the pre-change baseline `added_lines=0 blocking_hits=0` and the same `BLOCKING_PATTERNS`; the tool's own total stays `blocking=27` (destructive 20 + governance_kept 7), `violations=0` — the total is context, never the criterion

SC-009_status=pass
SC-009_value=4/4
SC-009_note=each of the four frozen rosters carries the new name plus a 2026-10-30 / Feature 078 note (counts unchanged: 27 commands, 52 skills = 15 external + 37 internal, 49 hash-manifest skills) and the four files pass together (48 passed); no silent count edit — the manifest itself stays untouched and the retired path is resolved by the register instead

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=none — T025-T031 all executed in this segment

# -- Free-form notes --

notes=Gates (verbatim; the full raw capture, including the 495 baseline-internal uncovered
clause names, is archived at test-evidence/implement-part4-gates-raw.txt — summary-first per
the token-efficiency discipline, with this file carrying the digest):

```text
### validate-tasks
PASS: .specify/specs/078-coaching-skills/tasks.md — 0 error(s), 0 warning(s)
rc=0

### pre-analyze-check --stage tasks
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=5 waived=0
  advisories: plan.md:137 .specify/templates/commands/ (absent), plan.md:154 + tasks.md:22 + tasks.md:259
  .specify/skills/think-skills/ (the retired mirror, correctly absent), data-model.md:196
  .specify/memory/coaching/.optimization-claims/ (created only when a claim is taken)
rc=0

### decomposition-check --mode tasks
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 29, "task_count": 31,
 "fr_ceiling": 30, "task_ceiling": 40}, "reasons": [], "checked_at": "2026-10-30T08:34:55Z"}
rc=0

### account-clause-coverage
scanned 234 files: parsed 140 + named-unparseable 94 == 234  [relational sentinel OK]
clause universe: 1464 distinct names over 140 parsed files (1488 ids extracted)
claimed clauses (this feature): 38
baseline: .specify/specs/078-coaching-skills/coverage-baseline.txt (495 names)
  [clause-uncovered] pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [fr-uncovered] fail (29) — 0 of 29 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms
  [coverage-baseline-delta] pass (0) — baseline holds 495 names
29 error(s), 0 warning(s)
status: uncovered
rc=1
```

The `fr-uncovered` lane is the **declared not-applicable** lane: quickstart § "Verification
boundary" and plan § Phase 1 own the statement (these contracts use condition-shaped clauses
without citation groups, so the FR lane reports zero by construction, and the FR→clause mapping
lives in plan § Phase 1). The clause lane is green — 38 claimed, 0 beyond the frozen baseline —
which is the lane that can actually regress here; the exit code is 1 for the exempted lane only.

```text
### C-8 verification surface (final reading)
$ flow-class-check.py --action lookup --unit-id skill:coaching-skills
  source: ledger / flow_class: execution / basis: behavior-oracle           rc=0
$ flow-class-check.py --action check
  flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]  rc=0
$ probe-utils.py --action probes --validate
  Probe registry valid: 10 classes, 117 internal + 0 external objects       rc=0
$ probe-utils.py --action compile-embeds --check
  compile-embeds --check: 75 units, zero drift                             rc=0
$ sync-mirrors.py --check
  OK: six pairs byte-identical (templates 22, skills 406, internal 136, agents 3, scripts 117, shared 60)  rc=0
$ regen-command-copies.py --check
  OK: all per-tool command copies match the source templates.              rc=0
$ scan-confirmation-gates.py --summary
  blocking confirmation gates: 27 (destructive 20, governance_kept 7); violations 0  rc=0
```

```text
### new-line gate — BASE=d0f50759
added_lines=475 blocking_hits=0
rc=0
```

```text
### targeted test set (E3) — 162 passed, 0 failed
four frozen baselines + all five coaching contract files + compile_* + directory_governance
+ scan_confirmation_gates
```

```text
### skill-shape (T030)
skills/external/coaching-skills/SKILL.md --budget-tokens 5000 -> pass, ≈3278 tokens / 5000 (253 lines)
findings: 1 warning (flags-outside-contract, the compiled ## Wrap-up face) — notes/skill-shape-after.md
```

**Assumptions recorded in this segment**

1. Scenario 2's single dispatch was executed by a one-shot runner that loads the fixture
   Trainee by explicit path and follows its Workflow literally; no host-native subagent was
   offered to this stage, so the run records `mode: run-skills-explicit-path`, `self-report`
   rows and states the substitution in the DispatchRecord `anomaly-line`. Every artifact
   discloses this; nothing claims `host-event`.
2. `BASE=d0f50759` is read as the feature baseline (the rebaseline event in the state spine);
   § SC-008 records the SHA and the derivation.
3. The four frozen rosters omit the retired literal on purpose: they sit inside A10's closed
   surface, where SC-006 allows exactly one occurrence, so the hash-manifest handoff derives
   the retired path instead of spelling it.
