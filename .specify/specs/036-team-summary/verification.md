# Verification Log — 036-team-summary

<!--
  Populated by /speckit.implement. Structured key=value + per-SC rows so that
  /speckit.review, /speckit.analyze and CI can derive pass-rates programmatically.
  status ∈ {pass | fail | partial | deferred | unknown}.
-->

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=be984a2774e6913f61acce28d32e9e2045003e81
baseline_date=2026-08-04
baseline_branch=036-team-summary

# Full-suite baseline via the canonical runner:
#   bash .specify/scripts/bash/run-tests.sh --names-out .specify/specs/036-team-summary/baseline-failed.txt
# Failing test IDs are recorded by NAME in baseline-failed.txt (39 entries), not by count alone,
# so zero-new-failures is proven by `comm -13 baseline current` rather than count archaeology.
# These 39 failures are long-standing and unrelated to this requirement (see AGENTS.md
# "Test baseline discipline"): assistant-count/tier assertions, claude/qoder support matrices,
# agent-reference integrity, handoff-chain, skill-home-workdir, agent-env-config.
baseline_failed_count=39
baseline_passed_count=1108
baseline_skipped_count=1
baseline_failed_names_file=.specify/specs/036-team-summary/baseline-failed.txt

# Team-side starting state (measured, informs SC-001 / SC-013 / SC-014)
baseline_team_count=4
baseline_team_patterns=continuous:2 (cws-workspace-cluster, requirement-implement-monitor); iteration:2 (draw-plantuml-optimizer, summarize-project-optimizer)
baseline_teams_declaring_goal_slug=0
baseline_teams_with_items_ledger=0
baseline_teams_able_to_produce_summary=0
baseline_goal_directories=0

# -- Environment prerequisites (probed at task-generation time, re-probed at run start; T003) --

env_python_pytest=pytest 8.4.2; markers contract + integration present
env_summarize_project_chain=validate-project-input.py / project-db.py --load|--check / progress-engine.py all exit 0 against a real team-derived form
env_sync_mirrors=scripts/python/sync-mirrors.py --check exits 0 (no pre-existing drift)
env_plantuml=render verified live via server http://xuanji-plantuml.aliyun-inc.com:9696/plantuml (SVG 1987x1687 + PNG produced); java 21 present but NO local plantuml.jar, so no offline fallback — T095 is [~]-eligible if the server is unreachable
env_plantuml_invocation_caveat=render-plantuml.sh <input.puml> <output_dir> <prefix> — omitting output_dir writes diagram.{puml,svg,png} into the CWD (measured); never invoke from the repo root
env_writability=all 24 target directories from plan.md Source Code tree + Mirror Obligations probed writable at run start
env_ignore_admission=goal delivery dir, per-team items.jsonl, fixtures and verification.md all ADMITTED by .gitignore; teams/.work/ and agents/execution/logs/ correctly ignored
env_gate_check=.specify/gate.yaml present; all Phase 1-2 planned write paths return `allow` (exit 0) via scripts/python/gate-check.py

# -- /speckit.implement results --

implementation_date=2026-08-04
post_change_commit=[PENDING — Phases 1-2 only; run not yet complete]

# -- Progress after Phases 1-2 (Setup + Foundational), measured 2026-08-04 --

phase1_status=complete (T001-T003)
phase2_status=complete (T004-T013, T102-T103)
phase3_status=near-complete (T014-T028, T030-T032 closed; T029 left OPEN — its documented half landed in summary-mapping.md section 9, but the actual non-interactive invocation belongs to the US2 SUMMARIZE step, so it is not closed on partial evidence)
phase4_status=near-complete (T029, T033-T048 closed; T049 left OPEN — it requires a live `/speckit.team run` on a continuous team, which is user-gated by the preview→confirm gate by design)
tasks_closed=50
tasks_open=70
regression_failed_count=39
regression_new_failures=0
regression_evidence=comm -13 baseline-failed.txt current-failed.txt returned EMPTY after every phase; passes rose 1108 -> 1249 (+141, exactly the new tests)
us2_propagation=3/3 shipped presets declare config.summary (artifact-optimizer every=1; process-monitor + workspace-cluster every=5); 5/5 per-tool speckit.team copies carry the confirmation-gate summary disclosure
new_contract_tests=141 passing (added test_summary_trigger.py 48) (test_team_item_ledger.py 21, test_summary_writeset.py 23, test_goal_identity.py 25, test_summary_form_generator.py 15, test_summary_four_patterns.py 9)
generator=skills/create-team/scripts/build-summary-input.py + mirror; --goal/--team selector, exit 0/2/3, mirror --help verified

# -- SC-001 / SC-002 real-data evidence (T032), all four REAL teams, 2026-08-04 --
# command per team: build-summary-input.py --team <slug> --out /tmp/... --json
#   then validate-project-input.py --json, project-db.py --load, project-db.py --check
sc001_cws_workspace_cluster=gen=0 validate=0 load=0 check=0 status=ready missing_required=0 work_items=2 milestones=3 goal_identity=inferred
sc001_requirement_implement_monitor=gen=0 validate=0 load=0 check=0 status=ready missing_required=0 work_items=13 milestones=3 goal_identity=inferred
sc001_draw_plantuml_optimizer=gen=0 validate=0 load=0 check=0 status=ready missing_required=0 work_items=5 milestones=0 goal_identity=inferred
sc001_summarize_project_optimizer=gen=0 validate=0 load=0 check=0 status=ready missing_required=0 work_items=14 milestones=0 goal_identity=inferred
sc001_serial_and_parallel=covered by tests/fixtures/teams/{serial,parallel}-fixture via tests/integration/test_summary_four_patterns.py (all four patterns exit 0 end-to-end)
sc002_manual_form_edits=0 across all four real teams and both fixtures
mirror_parity=sync-mirrors.py --check exit 0; summary-mapping.md + create-team/SKILL.md + templates/commands/team.md all byte-identical to mirrors; 5 per-tool speckit.team copies regenerated and each carries the goal-directory edit

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=4/4 real teams and 4/4 patterns: generator+validate+load+check all exit 0; status=ready; missing_required=0 (baseline was 0/4 able to produce a summary)
SC-001_note=continuous+iteration from real teams, serial+parallel from fixtures (no real team of those patterns exists); proven by T032 evidence rows above plus test_summary_four_patterns.py

SC-002_status=pass
SC-002_value=R-tier missing_required=0 on all four real teams with zero manual form editing; forms produced automatically by build-summary-input.py
SC-002_note=Upgraded from the Phase 0 hand-built proof to the automated generator path

SC-003_status=unknown
SC-003_value=[PENDING]
SC-003_note=Five byte-invariance groups (team tree / monitored targets / invoked skill / agent layers / pre-existing .specify/project artifacts); requires T060 + T072

SC-004_status=unknown
SC-004_value=[PENDING]
SC-004_note=Provenance non-empty rate and path reachability; requires T061

SC-005_status=unknown
SC-005_value=[PENDING]
SC-005_note=Intake must not double between run-count K and 2K; requires T064

SC-006_status=partial
SC-006_value=Gate order, skip vocabulary and the first-drop rule are landed and pinned by 48 passing trigger contract assertions; the live report-only-tier run is not yet executed
SC-006_note=Remaining evidence needs T049, a real /speckit.team run on requirement-implement-monitor at the report-only tier — user-gated by the preview→confirm gate by design

SC-007_status=unknown
SC-007_value=[PENDING]
SC-007_note=One current summary per goal + annotation preservation; requires T050/T059

SC-008_status=unknown
SC-008_value=[PENDING]
SC-008_note=7 entities x 4 patterns mapping coverage matrix; T007/T008 landed the mapping single source of truth (skills/create-team/references/summary-mapping.md) covering all 7 entities and all 4 patterns; dedicated verification task still open (analyze finding C3)

SC-009_status=unknown
SC-009_value=[PENDING]
SC-009_note=Zero fabricated dates/durations/percentages under thin material; requires T075/T086. Engine already returns progress_pct=null and suppresses the Gantt when material is absent (measured)

SC-010_status=unknown
SC-010_value=[PENDING]
SC-010_note=External-reader comprehension + zero internal identifiers in reader sections; requires T062

SC-011_status=unknown
SC-011_value=[PENDING]
SC-011_note=Cross-refresh identity stability; requires T052

SC-012_status=unknown
SC-012_value=[PENDING]
SC-012_note=Breakdown-diagram node count within the upstream CG-6 threshold of 15 at depth >=2; requires T053

SC-013_status=unknown
SC-013_value=[PENDING]
SC-013_note=Goal identity and directory correctness (added by the 2026-08-04 dual-index revision); T102/T103 landed and green (25 assertions incl. explicit-wins, inference fallback, prose-edit stability, DDL+path-safety grammar, and all 4 real teams resolving without migration); full criterion still requires T108/T120

SC-014_status=unknown
SC-014_value=[PENDING]
SC-014_note=Cross-team aggregation completeness + machine-decidable attribution (dual-index revision); requires T104/T106/T107

SC-015_status=unknown
SC-015_value=[PENDING]
SC-015_note=Concurrent-refresh serialization safety (dual-index revision); requires T109/T115

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=

# -- Free-form notes --

notes=Run start 2026-08-04. Requirement was scope-revised mid-flight (before implement) to a dual index: .specify/teams/<team-slug>/ keeps run info, .specify/project/goal/<goal-slug>/ holds the sole complete summary aggregating all teams sharing a goal_slug; recorded verbatim in requirements.md ## Clarifications. /speckit.analyze then found 9 issues; four were remediated with user approval (five phantom `templates/teams/` references, T100 stale SC range, byte-invariance group-count drift which had concealed a missing `.specify/agents/**` group in SC-003, and two phase-number drifts). Open analyze findings carried into this run: I2 (FR-020 carve-out should name the run-report status-line write), C2 (FR-008 has no citing task), C3 (SC-008 has no verification task), I5 (T091 blocked by later T093), A1 (title says "Team Summary" while the deliverable is goal-indexed). FRAMEWORK BUG found at run start: the mechanical write gate invocation documented in /speckit.implement (`python3 .specify/scripts/python/gate-check.py`) always fails with exit 3, because gate-check.py computes REPO_ROOT as Path(__file__).parents[2], which resolves to `.specify/` for the mirrored copy and therefore looks for `.specify/.specify/gate.yaml`; the canonical copy `scripts/python/gate-check.py` resolves correctly and was used instead.
