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
post_change_commit=[PENDING]

post_change_sdd_workflow_live_matches=[PENDING]
post_change_skill_count=[PENDING]
post_change_pytest=[PENDING]

# -- Success Criteria evaluation --

SC-001_status=unknown
SC-001_value=[PENDING zero-reference gate]
SC-001_note=grep sdd-workflow must be zero outside excluded set

SC-002_status=unknown
SC-002_value=[PENDING]
SC-002_note=skill registry lists one fewer; sdd-workflow absent from all skills surfaces

SC-003_status=unknown
SC-003_value=[PENDING]
SC-003_note=10 docs relocated with content parity

SC-004_status=unknown
SC-004_value=[PENDING]
SC-004_note=fresh init installs .specify/shared/workflow; links resolve

SC-005_status=unknown
SC-005_value=[PENDING]
SC-005_note=re-init retains .specify/shared/workflow

SC-006_status=unknown
SC-006_value=[PENDING]
SC-006_note=no new pytest failures vs baseline

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=

# -- Free-form notes --

notes=Baseline pytest failures (104F/13E) are pre-existing and outside this feature's scope; SC-006 is evaluated as "no NEW failures vs baseline".
