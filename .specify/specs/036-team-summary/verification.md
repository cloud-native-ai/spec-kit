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
tasks_closed=15
tasks_open=105
regression_failed_count=39
regression_new_failures=0
regression_evidence=comm -13 baseline-failed.txt current-failed.txt returned EMPTY; passes rose 1108 -> 1177 (+69, exactly the new contract tests)
new_contract_tests=69 passing (test_team_item_ledger.py 21, test_summary_writeset.py 23, test_goal_identity.py 25)
mirror_parity=sync-mirrors.py --check exit 0; summary-mapping.md + create-team/SKILL.md + templates/commands/team.md all byte-identical to mirrors; 5 per-tool speckit.team copies regenerated and each carries the goal-directory edit

# -- Success Criteria evaluation --

SC-001_status=unknown
SC-001_value=[PENDING]
SC-001_note=Four patterns each produce a summary from tracked artifacts alone; requires T032 (US1) + serial/parallel fixtures (T030)

SC-002_status=partial
SC-002_value=Phase 0 proof: validate-project-input.py returned status=ready, missing_required=[] on a hand-built form derived solely from cws-workspace-cluster tracked artifacts
SC-002_note=R-tier satisfiability proven feasible by execution; full criterion needs the generator (T020-T029) producing the form automatically

SC-003_status=unknown
SC-003_value=[PENDING]
SC-003_note=Five byte-invariance groups (team tree / monitored targets / invoked skill / agent layers / pre-existing .specify/project artifacts); requires T060 + T072

SC-004_status=unknown
SC-004_value=[PENDING]
SC-004_note=Provenance non-empty rate and path reachability; requires T061

SC-005_status=unknown
SC-005_value=[PENDING]
SC-005_note=Intake must not double between run-count K and 2K; requires T064

SC-006_status=unknown
SC-006_value=[PENDING]
SC-006_note=Budget-tier skip behaviour; requires T049

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
