# Verification Log — 097-speckit-migrate-command

<!--
  Schema owner: shared/workflow/acceptance-hardening.md — § Verification Vocabulary and
  § Closure Verdict; shape from templates/verification-log-template.md. The key=value block
  below is the record; the human view at the end renders from it. The closure judgement
  (scripts/python/closure-acceptance-check.py) parses `SC-NNN_status=` lines and nothing else.
  Written by the pkg07-polish package (T048), 2026-11-10.
-->

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=4194e0ebb
baseline_date=2026-11-10
baseline_branch=097-speckit-migrate-command
baseline_implement_entry_failed_ids=278
baseline_implement_entry_failed_ids_source=.specify/specs/097-speckit-migrate-command/baseline-failed.txt
baseline_implement_entry_suite_reading=.specify/specs/097-speckit-migrate-command/test-evidence/implement-entry-baseline-suite.txt

# -- /speckit.implement results --

implementation_date=2026-11-10
post_change_commit=1b2d998c6 plus the pkg07 working tree (this file lands in the pkg07 commit on branch 097-speckit-migrate-command)

# -- Smoke test record (exactly one per feature) --

smoke_command=bash scripts/bash/run-tests.sh --names-out .specify/.tmp/review-repair-r1/final-failed.txt tests/contract/test_migrate_cli_surface.py tests/contract/test_migrate_engine_contract.py tests/contract/test_migrate_template.py tests/contract/test_migrate_distribution_assembly.py tests/contract/test_migration_distribution.py tests/unit/test_migrate_planner.py tests/unit/test_migrate_receipts.py tests/integration/test_migrate_us1_converge.py tests/integration/test_migrate_us2_safety.py tests/integration/test_migrate_us3_crossversion.py tests/integration/test_migrate_us4_equivalence.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/097-speckit-migrate-command/test-evidence/final-suite.txt

# -- Closure verdict (implement status step, landed by review-repair r1 2026-11-10) --
# Copied from closure-acceptance-check.py --json-out; the verdict measures the tree being
# claimed (this working tree). The pre-flip run reads the prior `Planned` claim; the
# post-flip run re-reads the landed `Implemented` claim against the same tree.

closure_verdict=accept
closure_reasons=(none emitted)
closure_final_path=pass 4 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 4
closure_conditions=every_final_path_pass=true, no_open_rows=true, smoke_record_pass=true, status_row_per_criterion=true
closure_checker_command=python3 .specify/scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/097-speckit-migrate-command --feature-detail .specify/features/024-specification-workspace-versioning.md --json --json-out .specify/specs/097-speckit-migrate-command/test-evidence/closure-verdict-pre-flip-2026-11-10.json
closure_evidence=.specify/specs/097-speckit-migrate-command/test-evidence/closure-verdict-pre-flip-2026-11-10.json and closure-verdict-implemented-2026-11-10.json

# -- Evidence records (bind every pass claim to archived evidence) --

sample_id=SC-001
evidence_path=.specify/specs/097-speckit-migrate-command/test-evidence/us1-converge.txt
evidence_sha256=61e7426740ec3262a4c376b66d8ca352284b10756c9699da422fd8833e3aa7f1
verdict=pass

sample_id=SC-002
evidence_path=.specify/specs/097-speckit-migrate-command/test-evidence/us2-safety.txt
evidence_sha256=e73f5a239d9d001defd437f654a83682e29b495c73491749e3f14d8a411550f1
verdict=pass

sample_id=SC-003
evidence_path=.specify/specs/097-speckit-migrate-command/test-evidence/final-suite.txt
evidence_sha256=f3a09310389e1b653904a9d6069a6b10259894f14f9ca729bf8d9ee4876f18d8
verdict=pass

sample_id=SC-004
evidence_path=.specify/specs/097-speckit-migrate-command/test-evidence/us3-crossversion.txt
evidence_sha256=b8764bcba5486f886b3657c709f43348657eb2d9ec8821848cd6c935ae2c4f7c
verdict=pass

sample_id=SC-005
evidence_path=.specify/specs/097-speckit-migrate-command/test-evidence/us2-safety.txt
evidence_sha256=e73f5a239d9d001defd437f654a83682e29b495c73491749e3f14d8a411550f1
verdict=pass

sample_id=SC-006
evidence_path=.specify/specs/097-speckit-migrate-command/test-evidence/us3-crossversion.txt
evidence_sha256=b8764bcba5486f886b3657c709f43348657eb2d9ec8821848cd6c935ae2c4f7c
verdict=pass

sample_id=SC-007
evidence_path=.specify/specs/097-speckit-migrate-command/test-evidence/us1-converge.txt
evidence_sha256=61e7426740ec3262a4c376b66d8ca352284b10756c9699da422fd8833e3aa7f1
verdict=pass

sample_id=SC-008
evidence_path=.specify/specs/097-speckit-migrate-command/test-evidence/us2-safety.txt
evidence_sha256=e73f5a239d9d001defd437f654a83682e29b495c73491749e3f14d8a411550f1
verdict=pass

sample_id=SC-009
evidence_path=.specify/specs/097-speckit-migrate-command/test-evidence/us4-equivalence.txt
evidence_sha256=be1ddf7d519ba93009c97a6ec918d4587ca1a1e478d90496eb238ef222c9159a
verdict=pass

# -- Success Criteria evaluation --
# One block per SC from requirements.md. Status values come from the closed six-value set
# declared in the template; every blocked / deferred / partial row carries the five ladder fields.

SC-001_status=pass
SC-001_value=us1-converge.txt: latest fixture dry-run clean exit 0 with unchanged tree hash; legacy fixture dry-run planned exit 1 with unchanged tree hash and items in all five dimensions (3/2/1/1/4); apply applied exit 0, 11/11 items done, 9 archives all present; second run clean exit 0 zero-write; the per-dimension removal mutation zeroes each dimension (control >0)
SC-001_note=own fixture readings, not delegated evidence; suite inside the 105-passed final run (final-suite.txt).

SC-002_status=pass
SC-002_value=us2-safety-v2.txt: non-interactive apply executes every archive-first item (outcome applied exit 0, no prompt, 9/9 destructive items done), every replaced/merged/archived object exists at its receipt-named archive path with matching digests and recover equals archives; the real/real merge fixtures preserve both the current and legacy content; in-suite red-ability: the archive-removal and full-delete mutations turn the archive/user-content assertions red, the pick-one-side drill turns the both-sides check red, and the workspace-writing symlink-probe variant turns the zero-write assertion red; the existence-only weakening stays green while the byte assertion reds (MUT-existence-only)
SC-002_note=both halves measured on one fixture family; the product mutations and the check-power drills prove red-ability (FR-024); re-ran 2026-11-11 for the single-authorization archive-first change (26 passed, us2-safety-v2.txt).

SC-003_status=pass
SC-003_value=final-suite.txt: mixed fixture dry-run planned exit 1 total 3 (templates-generated 1 / compat-links 1 / migration-residue 1) zero-write; one apply applied exit 0 with all items done and 2 archives present; re-run clean exit 0 zero-write; latest fixture clean in dry-run and re-run with zero writes (us1-converge.txt); a corrupted converged target exists while the equivalence reading flags it (test_mixed_fixture_equivalence_assertion_has_power_beyond_existence), so an existence-only weakening turns red; three-class outcomes decidable by outcome token and exit code
SC-003_note=T048 gate discovery: the mixed fixture had no acceptance reading (builder constructed by T007 but unexercised); probe .specify/.tmp/pkg07/mixed-probe.txt measured the capability correct and two tests were added to the T015 suite; suite re-run 103 passed with zero NEW failures (final-suite.txt § Acceptance repair).

SC-004_status=pass
SC-004_value=us3-crossversion.txt: multi-generation fixture dry-run planned 17 items with the second generation 6/6 visible; a single apply converged 17/17 in one run with no intermediate-version step; receipt records source (.specify/source.json) and target (CLI version + framework commit) and the source file is never rewritten; the source-version-routing mutation turns plan identity red
SC-004_note=one-run N to N+k with record-only version fields (FR-020).

SC-005_status=pass
SC-005_value=us2-safety-v2.txt MERGE: a real/real `features.md` pair is unioned by feature ID — the current row wins on a duplicate id, the legacy-only row is appended, and the totals/date are recomputed; a real/real `constitution.md` pair is appended under the fixed merge marker with both principles preserved; an unmergeable structural target (non-empty directory) is refused and both candidates survive. No silent winner.
SC-005_note=the pick-one-side drill turns the both-sides check red; the structural refuse path keeps both candidates (C-3/C-6).

SC-006_status=pass
SC-006_value=us3-crossversion.txt INTERRUPT: interrupted apply (target deleted, receipt status=running, archive kept) resumes with resumedFrom naming the old run, notes reporting the stage, target restored byte-identically, old archive still at its receipt-named path (exactly one carried entry, same archiveTo), old receipt untouched; the re-move mutation turns the resume checks red
SC-006_note=counts and existence assertions on one fixture (SC-006 wording).

SC-007_status=pass
SC-007_value=us1-converge.txt POINTER/POINTER-RECEIPT: every plan and receipt carries the E-9 static goal/team pointer and zero goal/team items; the sanitize Migration wrap-up lane declares `/speckit.migrate` as the one-shot closeout main entry with the lane as periodic recheck fallback and unchanged checkers/dispositions — `skills/internal/sanitize-materials/SKILL.md:167-178`, framework source and mirror byte-identical (mirror-verify.txt Pair 1, diff_exit=0); the reused migration-residue dimension is empty on the post-apply re-run (SECOND-RUN outcome=clean items=0)
SC-007_note=migrate absorbs no goal/team migration and no periodic sanitize duty (FR-012/FR-013).

SC-008_status=pass
SC-008_value=us2-safety.txt: user-built skills, hand-edited framework files and .specify/memory content stay byte-identical after convergence; every replaced object's pre-replacement bytes match its archived copy; the full-delete mutation turns the archive and user-content cells red
SC-008_note=archive-before-write measured per object, not asserted in prose.

SC-009_status=pass
SC-009_value=us4-equivalence.txt: source template plus four per-tool copies (AUTO-GENERATED), Qoder short-description frontmatter, command doc page, COMMAND_BASELINE 30, retired mirror face absent, regen-command-copies --check exit 0; distribution counts 30 templates / 30 per copy tree / 28 docs; mirror-verify.txt carries both obligation checks at exit 0
SC-009_note=every assembly face listed in SC-009 present and counted; missing-face mutation lives in the assembly contract.

# -- Joint acceptance (one row per `in-scope` runtime-stack row in requirements.md) --

RS-004_joint_acceptance=pass

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=

# -- Definition of Done readings (tasks.md § Definition of Done) --

DoD-1=pass — FR lane: 25 distinct FR-0NN tokens cited by task rows (`grep -E '^- \\[[ xX>~]\\] T[0-9]{3} ' tasks.md | grep -oE 'FR-0[0-9]{2}' | sort -u | wc -l` returns 25)
DoD-2=pass — clause lane: `python3 .specify/scripts/python/validate-tasks.py tasks.md` exit 0, 0 error(s), 0 warning(s)
DoD-3=pass — no second engine: test_migrate_engine_contract.py green inside the 105-passed final run (clean assertions plus the five in-test injection mutations in one suite run)
DoD-4=pass — archive-first measured: us2-safety-v2.txt per-object existence readings plus the five red-ability drills (archive removal, full delete, pick-one-side, workspace-writing probe variant, existence-only weakening)
DoD-5=pass — distribution complete: test_migration_distribution.py green, regen-command-copies.py --check exit 0, us4 counts 30/30/28 with COMMAND_BASELINE 30
DoD-6=pass — mirrors no NEW drift: sync-mirrors.py --check exit 0 vs the R-8 baseline (exit 0); both touched pairs diff -q byte-identical (mirror-verify.txt)
DoD-7=pass — final-path criteria SC-001…SC-004 all pass and the smoke record is present (this file)
DoD-8=pass — zero-write and determinism measured: us1-converge.txt tree hashes (dry-run before/after, post-apply re-run) and repeated dry-run byte-identical items+summary; quickstart scenarios 1 and 2 in notes/quickstart-run.md
DoD-9=pass — quickstart scenarios 1–5 executed end to end with real outputs and exit codes (notes/quickstart-run.md; driver all_pass=True)
DoD-10=pass — zero unfinished rows: `grep -cE '^- \\[[ >]\\] T[0-9]{3} ' tasks.md` returns 0

# -- Gates (tasks.md § Completion Gate) --

GATE-1=pass — feature subset exit 0, 105 passed, zero NEW failing names vs the implement-entry baseline (278 names; final-suite.txt)
GATE-2=pass — test_migration_distribution.py green in GATE-1's run; regen-command-copies.py --check exit 0 (mirror-verify.txt)
GATE-3=pass — sync-mirrors.py --check exit 0, no NEW drift vs R-8; regen-command-copies.py --check exit 0 (mirror-verify.txt)
GATE-4=pass — every final-path criterion (SC-001…SC-004) is pass; smoke_command/smoke_exit_code=0/smoke_evidence_path all present
GATE-5=pass — zero `[ ]` / `[>]` rows (grep returns 0)
GATE-6=pass — validate-tasks.py exit 0, 0 error(s), 0 warning(s)

# -- Free-form notes --

notes=Disclosed acceptance repair (2026-11-10, T048 gate re-validation): contract C-8's last bullet and SC-003's mixed-fixture limb had no acceptance reading — build_mixed_project was constructed by T007 but no test exercised it. A zero-write probe (.specify/.tmp/pkg07/mixed-probe.txt) measured the capability correct (planned exit 1 total 3; applied exit 0 with 2 archives; re-run clean zero-write; corrupted converged target flagged while existing), then two tests were added to tests/integration/test_migrate_us1_converge.py — the T015 suite — test-only, no engine change. Targeted run 6 passed; the T046 subset was re-run and re-recorded (101 to 103 passed, zero NEW failures). The worktree's pre-existing unrelated changes (.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt modification; checkpoints/01-requirements.md, checkpoints/02-clarify.md, test-evidence/analyze-validation-round2-2026-11-10.md untracked) were left untouched and are not part of this package. Quickstart substituted the repository source for the installed CLI per tasks.md § Environment Prerequisites (installed CLI is released 0.0.22). Review-repair r1 (2026-11-10): the US2 zero-write probe test was rebuilt into an observable guard plus mutation 5 (red-base drill: test-evidence/red-base-probe-guard-2026-11-10.txt; us2 re-run appended in us2-safety.txt, 12 passed); the smoke record was re-executed and re-recorded verbatim with its --names-out path (103 to 105 passed, final-suite.txt); SC-002/SC-007/DoD-4 wording aligned with the exercised drills; contract C-1, the command docs and the template converged to --help only (no -h registration); the receipt workspace key was implemented (C-4/E-2/E-3); quickstart's status declaration and tasks.md's DoD status were refreshed. Re-verification 2026-11-11 (archive-first single-authorization change): the US2 suite was re-run against the new behavior — non-interactive apply exits 0 with every archive-first item executed, the merge fixtures preserve both sides, and the structural refusal path keeps both candidates; evidence test-evidence/us2-safety-v2.txt (26 passed). The pre-change smoke record and closure verdict above are historical and were not rewritten.

# -- Human-readable view (NOT the record; rendered from the block above) --

| SC | Path | Status | Evidence pointer |
|----|------|--------|------------------|
| SC-001 | final | pass | us1-converge.txt — five-dimension convergence, zero-write hashes, per-dimension removal mutation |
| SC-002 | final | pass | us2-safety-v2.txt — non-interactive archive-first apply, merge preserves both sides, archives recoverable, five red-ability drills (observable probe guard) |
| SC-003 | final | pass | final-suite.txt — mixed planned/applied/clean + existence-only weakening red (repair disclosed) |
| SC-004 | final | pass | us3-crossversion.txt — one-run N→N+k, version fields, routing mutation |
| SC-005 | supporting | pass | us2-safety-v2.txt — real/real anchors merge and preserve both; structural conflict refuses, no winner |
| SC-006 | supporting | pass | us3-crossversion.txt — interruption resume, no second move |
| SC-007 | supporting | pass | us1-converge.txt + SKILL.md:167-178 + mirror-verify.txt — static pointer, zero goal/team items; sanitize lane boundary |
| SC-008 | supporting | pass | us2-safety.txt — user content byte-identical, archive-before-write |
| SC-009 | supporting | pass | us4-equivalence.txt + mirror-verify.txt — assembly faces, regen/mirror checks |
