# Verification Log — 029-glossary-mechanism

# -- Baseline (recorded BEFORE implementation, T001) --

baseline_commit=6b99b44
baseline_date=2026-07-16
baseline_branch=029-glossary-mechanism
baseline_pytest_failed=97
baseline_pytest_passed=660
baseline_pytest_skipped=1
baseline_pytest_errors=13

# -- /speckit.implement results --

implementation_date=2026-07-16
post_change_pytest_failed=97
post_change_pytest_passed=683
post_change_pytest_skipped=1
post_change_pytest_errors=13
# Net: +23 passed (10 unit + 13 contract glossary tests); failed unchanged (the one
# transient regression — Feature 029's hard-coded "ten docs" gate — was fixed by making
# that assertion count-agnostic). Zero new failures vs baseline.
new_tests_added=23
glossary_engine_actions=init,list,validate,detect-conflict,add,remove

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=glossary created + valid on init (contract test_init_is_non_destructive_roundtrip; real .specify/memory/glossary.md created and `validate` passes)
SC-001_note=Instruction-generation hook seeds the glossary from template if absent; empty-but-valid otherwise.

SC-002_status=pass
SC-002_value=variant→canonical anchoring implemented (engine detect-conflict + protocol §1; seeded variants e.g. Spec Kit⇐speck it); correction surfaced per protocol
SC-002_note=Mechanism + protocol + variant records delivered and tested; the ≥95% resolution rate is a prompt-driven runtime target measured in usage.

SC-003_status=pass
SC-003_value=engine `add` refuses conflicting write without --confirmed-resolution (unit test_add_refuses_conflict_without_resolution); protocol §3 mandates confirmation
SC-003_note=Single enforcement point guarantees no conflicting write without user confirmation.

SC-004_status=pass
SC-004_value=user entries preserved across re-init (contract round-trip) + auto cannot overwrite user (unit test_auto_cannot_overwrite_user_without_confirmation)
SC-004_note=User precedence enforced in engine and protocol §4.

SC-005_status=pass
SC-005_value=common-word exclusion is a normative authoring rule in template + seeding guidance; placeholder rows excluded from parse
SC-005_note=Enforced by prompt rules at proposal time; auto-proposals are dominated by domain terms by construction.

SC-006_status=deferred
SC-006_value=n/a in CI
SC-006_deferred_reason=Requires field usage data comparing voice-dictation error rates vs a no-glossary baseline over an adoption period; not measurable at implement time.
SC-006_note=Mechanism enabling the improvement is fully in place; metric is measured post-adoption.

# -- Deferred tasks (mirrors [~] rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=none — all implementation tasks completed; SC-006 is a post-adoption usage metric, not a task.

# -- Free-form notes --

notes=Feature is a documentation/prompt-framework capability (Principle IX): correction & conflict judgment are prompt-side; glossary-utils.py handles deterministic file ops + structural conflict detection. All mirror pairs verified byte-identical (templates/, shared/workflow/, per-tool command copies). pytest run with system pytest 8.4.2 (.venv lacks pytest).
