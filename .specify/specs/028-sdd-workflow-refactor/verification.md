# Verification Log — 028-sdd-workflow-refactor

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=ed4fc0a015
baseline_date=2026-07-14
baseline_branch=028-sdd-workflow-refactor

# Free-form baseline counters used to evaluate SCs. One per line.
baseline_sdd_workflow_live_matches=290
baseline_source_ref_files_templates=18
baseline_source_ref_files_skills=20
baseline_source_ref_files_docs=8
baseline_skill_count=20
baseline_pytest=104 failed, 622 passed, 1 skipped, 13 errors
# Note: the 104 failures + 13 errors are PRE-EXISTING and unrelated to this feature
# (same class of pre-existing failures documented for Feature 028).

# -- /speckit.implement results --

implementation_date=2026-07-14
post_change_commit=[PENDING commit]

post_change_sdd_workflow_live_matches=0
post_change_skill_count=19
post_change_pytest=104 failed, 643 passed, 1 skipped, 13 errors
# Delta vs baseline: failures unchanged (104), passing +21 (the new Feature 029 tests).
# The clean baseline worktree lacked 3 git-ignored docs/history failures that are
# pre-existing in the real working tree; no genuine regression introduced.
# The one true regression (test_core_assets_detectable_in_multi_assistant_project,
# caused by adding .specify/shared to _CORE_SPECIFY_ASSETS) was fixed by extending
# the make_resource_with_skills fixture with a shared/workflow/ directory.

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=0 live matches outside excluded set (repo-wide gate)
SC-001_note=grep sdd-workflow must be zero outside excluded set

SC-002_status=pass
SC-002_value=skill count 20→19; sdd-workflow absent from skills/, .specify/skills/, all symlinks, registry
SC-002_note=skill registry lists one fewer; sdd-workflow absent from all skills surfaces

SC-003_status=pass
SC-003_value=10 docs relocated via git mv to shared/workflow/ (history preserved, content parity)
SC-003_note=10 docs relocated with content parity

SC-004_status=pass
SC-004_value=copy_local_templates installs .specify/shared/workflow/; contract+integration tests green
SC-004_note=fresh init installs .specify/shared/workflow; links resolve

SC-005_status=pass
SC-005_value=.specify/shared listed in _CORE_SPECIFY_ASSETS (retained on re-init); test_shared_dir_install green
SC-005_note=re-init retains .specify/shared/workflow

SC-006_status=pass
SC-006_value=104 failed (== baseline 104); passing 622→643 (+21 new tests); 0 new failures
SC-006_note=no new pytest failures vs baseline

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=

# -- Free-form notes --

notes=Baseline pytest failures (104F/13E) are pre-existing and outside this feature's scope; SC-006 is evaluated as "no NEW failures vs baseline".
