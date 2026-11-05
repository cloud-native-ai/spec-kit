# Verification Log — 084-harness-triple-structure

<!--
  USER TEST WAIVER — 2026-11-05. The user directed this run to skip every test: no pytest (full or
  targeted), no smoke, no scratch-tree proofs, no test-typed readings. Test-typed evidence below is
  therefore recorded `waived-by-user`, `deferred` or `blocked` — NEVER `pass`. Seconds-level
  deterministic commands were executed where a task row asked for one and their output is archived;
  those rows say "read" and cite the file.

  Consequence: the feature is **`Implemented`**. After the T032 classification slice and the
  user-authorized 2026-11-05 final test budget, both `final`-path criteria pass: SC-001 on the
  seconds-level coverage/verify readings (`unclassified 0`, determinism, no orphan declarations,
  consumer consistency), SC-002 on the contract module (68 passed) and the residual `duplicate`
  face (pass / 0 findings). The smoke record is complete (two byte-identical coverage runs, exit
  0). Supporting criteria SC-003/SC-005/SC-006 remain deferred/partial; the state machine's
  `Implemented` condition is satisfied (`templates/feature-details-template.md`).
-->

# -- Baseline (recorded at implement start, before any work changed the tree) --

baseline_commit=9657885f
baseline_date=2026-11-05
baseline_branch=084-harness-triple-structure
baseline_note=taken from `.specify/specs/084-harness-triple-structure/notes/pre-change-measurements.md` (T001) and the E2 baseline slot in the state spine; this file cites them, it does not re-derive them
baseline_mirror_check_exit=0
baseline_mirror_scripts_files=119
baseline_mirror_shared_files=62
baseline_command_templates=27
baseline_skill_md_carriers=53
baseline_workflow_documents=19
baseline_definition_documents=12
baseline_pyproject_diff_vs_4b65517c=empty
baseline_081_acceptance_files_diff_vs_4b65517c=empty
baseline_081_collect_counts=40/37 (not re-read this round — user test waiver)

# -- /speckit.implement results --

implementation_date=2026-11-05
post_change_commit=98288d45 (this segment's commit is the one carrying these files; recorded here as the parent-inclusive working tree)
post_change_mirror_check_exit=0
post_change_mirror_scripts_files=121
post_change_mirror_shared_files=89
post_change_command_templates=27
post_change_skill_md_carriers=53
post_change_workflow_documents=19
post_change_definition_documents=13
post_change_pyproject_diff_vs_4b65517c=empty
post_change_081_acceptance_files_diff_vs_4b65517c=empty

# -- Smoke test record (exactly one per feature) --
# Run under the user's 2026-11-05 final test budget. The command is the feature's minimal
# deterministic smoke: the coverage action twice, compared byte for byte.

smoke_command=python3 scripts/python/harness-triple-check.py --action coverage
smoke_exit_code=0
smoke_evidence_path=.specify/specs/084-harness-triple-structure/test-evidence/smoke-run1-2026-11-05.txt
smoke_comparison=byte-identical with .specify/specs/084-harness-triple-structure/test-evidence/smoke-run2-2026-11-05.txt (cmp exit 0)
smoke_not_run_reason=n/a — executed under the user-authorized final test budget

# -- Evidence records (bind every `pass` claim to archived evidence) --

sample_id=SC-004
evidence_path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part5-readings-2026-11-05.txt
evidence_sha256=0068252057d9732b923924b9708b38de4ec2a55a31dc277f5fd1a734c6a69c83
verdict=pass

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=candidates 83 / in-scope 13 / excluded 70 / unclassified 0; coverage exit 0; verify exit 0 with 0 findings; two consecutive coverage runs byte-identical (sha256 f9cd934a…3473, 47 ms / 44 ms); no declaration outside the candidate set; consumer consistency declarations→carriers 31/31 and carriers→declarations 16/16
SC-001_note=all four limbs read on the final tree after T032: (i) determinism holds; (ii) zero `unclassified-candidate:`; (iii) zero orphan declaration; (iv) bidirectional consumer consistency. Fast deterministic readings, not test suites; evidence in test-evidence/t032-classification-readings-2026-11-05.txt
SC-001_evidence=.specify/specs/084-harness-triple-structure/test-evidence/t032-classification-readings-2026-11-05.txt
SC-001_verified_at=2026-11-05 (T032 classification slice, commit 94d9db33)

SC-002_status=pass
SC-002_value=declarations 23; consistency declarations→carriers 31/31, carriers→declarations 16/16; pending 0; `third-layer-missing` 0; `duplicated-fact-literal` 0; 70 exclusion rows (13 in-scope / 70 excluded / 0 unclassified); residual `duplicate` face pass / 0 findings; contract module 68 passed
SC-002_note=all three segments read on the final tree: declaration side, state side (coverage/verify) and the residual `duplicate` face; the contract module (`tests/contract/test_harness_triple_structure.py`) passed 68/68 under the user-authorized final test budget
SC-002_evidence=.specify/specs/084-harness-triple-structure/test-evidence/final-contract-module.txt; .specify/specs/084-harness-triple-structure/test-evidence/final-duplicate-face.txt; .specify/specs/084-harness-triple-structure/test-evidence/t032-classification-readings-2026-11-05.txt
SC-002_verified_at=2026-11-05 (final test budget)

SC-003_status=deferred
SC-003_value=engine exit codes read incidentally (0 none observed / 1 findings / 2 not exercised); the 6/6 negative fixtures + 1/1 positive were not run
SC-003_note=the six-reason proof is a pytest leg (`tests/contract/test_harness_triple_structure.py` + `tests/fixtures/harness-triple-structure/`); supporting path, so a not-attempted reading is `deferred`, not `blocked`
SC-003_deferred_reason=test-waiver: waived-by-user (2026-11-05) — no pytest, so no reason fixture was executed
SC-003_blocked_at=test-waiver: waived-by-user (2026-11-05)
SC-003_reduced_measurement=the engine was executed five times this segment (two coverage, one verify, two delegated from the gate host) and its exit codes and finding text were captured verbatim
SC-003_reduced_measurement_run=yes
SC-003_why_reduced_insufficient=fixture-backed 6/6 with verbatim instances is the criterion, and no fixture ran; the observed runs emit one reason class only (`unclassified-candidate`), so 1 of 6 is witnessed
SC-003_unblock=run the contract module under an unwaived budget; nothing else is missing

SC-004_status=pass
SC-004_value=70 exclusion rows in 2 reason files (`no-machine-fact` 38 rows, `no-harness-asset` 32 rows); `by-owner-decree` 0 rows and consequently no third file created; `exclusion-anchor-unresolvable` 0; unit named twice 0; `coverage` exit 0 with `unclassified 0`
SC-004_note=both limbs measured mechanically on the final tree: every reason value is a filename equal to a member of `contract.yaml#/exclusion_reasons` (the engine rejects any other, an input error that did not occur) and every anchor resolves (0 `STR-012`). Whether each reason is *sufficient* remains a review judgement, which the criterion itself says it does not claim
SC-004_evidence_path=.specify/specs/084-harness-triple-structure/test-evidence/t032-classification-readings-2026-11-05.txt

SC-005_status=partial
SC-005_value=mirror limb READ: `sync-mirrors.py --check` exit 0, six pairs `ok` (templates 22, skills/external 409, skills/internal 138, agents 3, scripts 121, shared 89); second `--write` changed nothing in the tree
SC-005_note=the distribution limb (`specify init` on a sanctioned scratch root, roster assertion, copied checker exit) and the legacy-project degradation reading are scratch-tree proofs — waived, so `partial`, not `pass`
SC-005_blocked_at=test-waiver: waived-by-user (2026-11-05) — no scratch-tree proofs
SC-005_reduced_measurement=mirror projection performed twice (write → check → write) with drift compared against the T001(a) baseline: 0 new drift, and the count delta (scripts 119→121, shared 62→89) is exactly the files this feature adds
SC-005_reduced_measurement_run=yes
SC-005_why_reduced_insufficient=mirrors prove the framework source and this repo's `.specify/` copy agree; they say nothing about what a *client project* receives from `specify init`, which is the limb the criterion names
SC-005_unblock=run T030's source-route init in `.specify/.tmp/084-init/` under an unwaived budget, record the copied checker's exit, and tear the root down

SC-006_status=partial
SC-006_value=`git diff 4b65517c -- pyproject.toml` empty; `git diff --stat 4b65517c -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` empty; command templates 27 (baseline 27), `SKILL.md` 53 (53), workflow documents 19 (19), definition documents 13 (baseline 12)
SC-006_note=the zero-new-failure leg (id-level `comm -13` against the implement-start baseline), the two pytest collect counts and the feature-status value count were not read; `shared/definitions/*.md` moved 12→13 and is reported as a moved count — it is the new owner document, and that directory is not one of the screen's three carrier surfaces
SC-006_blocked_at=test-waiver: waived-by-user (2026-11-05) — no pytest, so no id-level set difference
SC-006_reduced_measurement=the two `git diff` legs against the approved baseline commit plus the four recorded surface counts
SC-006_reduced_measurement_run=yes
SC-006_why_reduced_insufficient="zero new failures on the five frozen gate scripts" is a test-run quantity; an empty file diff shows the assertions were not edited, not that they still pass. The feature-status value count has no baseline at all in T001(c), so that leg is unmeasurable as written rather than unchanged
SC-006_unblock=run the targeted set with `--names-out` and take `comm -13` against `baseline-failed.txt`, then record a baseline for the feature-status value count before comparing it

# -- Joint acceptance (one row per `in-scope` runtime-stack row in requirements.md) --

RS-001_joint_acceptance=partial
RS-001_note=the read entry and the checker ran on CPython 3.11.13 (this host) and both are stdlib-only by import list; the `>=3.8` floor itself was not exercised — no older interpreter was run and the fixture legs were waived

RS-002_joint_acceptance=deferred
RS-002_note=pytest was not run at all under the 2026-11-05 waiver, so the pin's acceptance ("contract module green on the baseline pin, zero new failures") is not attempted. The pin itself (`pytest 9.2.0`) is a recorded premise (EP-001), not re-read here

RS-003_joint_acceptance=deferred
RS-003_note=the distribution reading is T030's scratch-root `specify init` + copied-checker exit; waived with T030. No `src/` change was made, which is what D11 expects, but that is a design reading rather than the criterion's fixture reading

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=no row is `[~]`. T021–T023 and T027–T031 are closed `[X]` under the user's 2026-11-05 test waiver and their readings are recorded `waived-by-user` in `tasks.md` § Notes — a waiver is not a deferral, and the distinction is stated here so that nothing downstream reads these as measured

# -- Free-form notes --

notes=Readings, verbatim: `.specify/specs/084-harness-triple-structure/test-evidence/implement-part5-readings-2026-11-05.txt` (§1 coverage determinism, §2 verify, §3 batch-1 inline constants, §4 SC-006 seconds-level legs, §5 the gate host with and without `--triple-structure`, §6 post-tick validators and the zero-write leg), `t026-mirror-projection-run1-2026-11-05.txt` and `…run2-…txt` (the two projections).
notes_feature_status=Ready for Review (was Implemented until 2026-11-06) — `Implemented` rested on the user-authorized 2026-11-05 final test budget (SC-001 and SC-002 `pass`, machine-readable passing smoke). The `Implemented → Ready for Review` transition was executed by `/speckit.review` round 4 once its four conjunctive conditions held: deferred tasks 0, review evidence on disk (`review.md` + `code-review.md`), zero `blocking` entries in the current code-segment record (`report --summary --file` exits 0, `gate=allow`), and no `final`-path criterion in `blocked` / `deferred` / `fail` (`final_path`: pass 2). ARC at `2d8576b5` reads `verdict: accept` with comparison `agree`.
notes_no_new_mechanism=this segment added no judgement: one exclusion file plus two appended rows, one opt-in flag on an existing gate host, one docs pointer page, one changelog entry, and the mirror projection. Every other row is a reading or a waived reading.
