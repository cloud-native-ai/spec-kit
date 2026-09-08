# Verification Log — 050-proactive-flow-trigger

<!--
  Populated during the /speckit.implement run per .specify/templates/verification-log-template.md.
  Shape is key=value + per-SC three-field rows so /speckit.review, /speckit.analyze and CI can
  derive pass-rates programmatically without grepping prose.
  status ∈ {pass | fail | partial | deferred | unknown}. `unknown` = producing task not yet run.
-->

# -- Baseline (recorded once, BEFORE any /speckit.implement work changed the tree) --

baseline_commit=c3bc955d
baseline_date=2026-09-08
baseline_branch=050-proactive-flow-trigger

# Counters frozen by T002 into baseline-gates.json; restated here so the SC rows
# below have their comparison values in one place.
baseline_confirmation_gates_total=23
baseline_confirmation_gates_violations=0
baseline_gate_budget_cap=23.25
baseline_gate_integer_headroom=0
baseline_probe_internal_objects=73
baseline_probe_external_objects=0
baseline_complex_commands=19
baseline_simple_commands=4
baseline_docs_step_injections=16
baseline_suite_failed=42
baseline_suite_passed=2496
baseline_suite_skipped=1
baseline_instructions_h2_sections=15
baseline_instructions_symlinks_created=6
baseline_declared_agent_paths=5
baseline_hermes_path_generated=no
baseline_opencode_path_generated=no
baseline_check_instructions_passing_keys=4
baseline_seed_anchor_verified=0

# -- /speckit.implement results --

implementation_date=2026-09-08
post_change_commit=PENDING_RUN_END

post_change_confirmation_gates_total=23
post_change_confirmation_gates_violations=0
post_change_probe_internal_objects=73
post_change_complex_commands=19
post_change_simple_commands=4
post_change_docs_step_injections=16
post_change_instructions_h2_sections=16
post_change_instructions_symlinks_created=8
post_change_hermes_path_generated=yes
post_change_opencode_path_generated=yes
post_change_check_instructions_passing_keys=6
post_change_seed_anchor_verified=13

# -- Run notes --

notes=T013 found and corrected a quickstart scenario-1 premise defect: `specify init` never writes .specify/instructions.md nor any symlink (src/specify_cli/__init__.py has no generator call; its line 985 mention is only a _CORE_SPECIFY_ASSETS preservation entry). The real pipeline is two steps (init then /speckit.instructions). Scenario 1 was amended and re-run green; the defect was in the verification premise, not in the implementation.
notes=One regression-suite failure during Phase 2 was attributed to EXTERNAL provenance (a parallel session scaffolding git-ignored .specify/skills/.migration-backups/layout-int-* dirs). Evidence and reasoning recorded in baseline-gates.json `externalAttribution` and in baseline-failed.txt's header. The assertion was NOT loosened and the dirs were NOT deleted.

# -- Success Criteria (all 15, seeded per template instruction) --

SC-001_status=pass
SC-001_value=8/8 agent instruction paths created and resolving to .specify/instructions.md; 6/6 _check_instructions tool keys pass; divergent copies = 0
SC-001_note=Produced by T013 (automated) + T015 (manual walkthrough of quickstart scenario 1). Fresh mktemp root, `specify init --here --ai qoder --force --ignore-agent-tools` then the root's own shipped `.specify/scripts/bash/generate-instructions.sh`. All of CLAUDE.md, AGENTS.md, HERMES.md, .github/copilot-instructions.md, .opencode/instructions.md, QODER.md, .qoder/project_rules.md, .claude/project_rules.md are symlinks whose realpath is the one canonical .specify/instructions.md, so semantic sameness is structural (one file, eight links) rather than a content comparison — divergent copies cannot exist. Each of the 8 read through its link reports heading=1 pointer=1. Regression: before T011 HERMES.md and .opencode/instructions.md were MISS and hermes/opencode returned `fail`; both now pass. The shipped discipline doc is byte-identical to the working-tree source. Pinned by trigger-section.md C-1/C-10/C-12 (tests/contract/test_proactive_trigger_section.py, 16 tests green with the existing propagation guard).

SC-002_status=pass
SC-002_value=0 enumeration copies (0 command names of 25, 0 skill names of 34, 0 `skills/` paths, 0 parameter structures)
SC-002_note=Produced by T015 via cross-text check against the authoritative rosters, and pinned by trigger-section.md C-5. Rosters were derived, not assumed: 25 command names from templates/commands/*.md and 34 skill directory names from skills/. All three surfaces checked (templates/instructions-template.md, its .specify mirror, and the regenerated live .specify/instructions.md) — each reports 0 hits for every command name, 0 for every skill name, 0 for `skills/`, and 0 for the closed parameter-pattern set (`--<long-option>`, `$ARGUMENTS`, `<placeholder>`). Section body is 9 lines (limit 25) with 0 `### ` subheadings, so nothing is hidden in a subsection that additive reconcile would fail to propagate. Invocation forms are supplied by the engine at runtime, never enumerated in the instructions file.

SC-003_status=unknown
SC-003_value=
SC-003_note=Producing task T028 (US2 manual walkthrough) not yet run. Requires >=6 lifecycle state samples with per-state suggestion records and human correctness judgement.

SC-004_status=unknown
SC-004_value=
SC-004_note=Producing tasks T028 (part 1: irrelevant-suggestion count over 20 unrelated turns) and T050 (part 2: repeat-suggestion count within one session) not yet run.

SC-005_status=unknown
SC-005_value=
SC-005_note=Producing task T036 (US3 manual walkthrough) not yet run. Requires the destructive-flow zero-tolerance measurement over 10 consecutive acceptances.

SC-006_status=unknown
SC-006_value=
SC-006_note=Producing task T036 not yet run. Part 2 (zero learning-state loss after instructions regeneration) requires actually running generate-instructions.sh and diffing the trigger index.

SC-007_status=unknown
SC-007_value=
SC-007_note=Producing task T043 (US4 manual walkthrough, quickstart scenario 6) not yet run.

SC-008_status=unknown
SC-008_value=
SC-008_note=Producing task T050 (part 2: blocked-or-deferred event count during dogfooding) not yet run. Part 1 (gate-scan new violations = 0, total within the existing contract cap) is already measured green at every phase boundary — 23 total, 0 violations, cap 23.25 — but the SC row is held open until T050 lands the intrusion half.

SC-009_status=unknown
SC-009_value=
SC-009_note=Producing task T036 not yet run. Requires config --enabled false to yield 0 suggestions and 0 auto-executions, and to survive instructions regeneration.

SC-010_status=unknown
SC-010_value=
SC-010_note=Producing task T036 not yet run. Requires the three-state degradation walkthrough (missing / corrupt JSON / incompatible schemaVersion).

SC-011_status=unknown
SC-011_value=
SC-011_note=Producing tasks T028 (scenario 3 readings) and T050 (>=20 real dogfooding turns) not yet run. Denominator caveat per data-model.md V4.5 must be stated honestly: telemetry only exists when assess is called, so it cannot prove an assessment was skipped.

SC-012_status=unknown
SC-012_value=
SC-012_note=Producing task T050 not yet run. Requires complianceDone/suggested timing evidence (expected zero ordering-violation).

SC-013_status=unknown
SC-013_value=
SC-013_note=Producing tasks T028 (cold-start first-day suggestion) and T043 not yet run. The provenance half is already measured: T003 verified 13/13 seed anchors mechanically before implementation (baseline-gates.json seedAnchorsPrecheck), but the SC row is held open until the seed file exists and the cold-start behaviour is observed.

SC-014_status=unknown
SC-014_value=
SC-014_note=Producing task T028 not yet run. Requires >=5 independent sessions resolving the same constructed state to the same situationId.

SC-015_status=unknown
SC-015_value=
SC-015_note=Producing tasks T030 (automated) and T036 (manual, quickstart scenario 5) not yet run. Requires the append-then-truncate invariant and zero loss of promotion counts across rotation.
