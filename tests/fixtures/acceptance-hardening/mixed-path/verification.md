<!-- Fixture case: acceptance-hardening/mixed-path — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     `SC-001` (final) passes, `SC-002` (final) fails, `SC-003` (supporting) is deferred with the full ladder.
     The smoke record is complete, so the only reasons in play are the final-path ones. -->

# Verification Log — 900-acceptance-fixture-mixed-path

# -- Smoke test record (exactly one per feature) --

smoke_command=python3 -c "print('acceptance-fixture-mixed-path')"
smoke_exit_code=0
smoke_evidence_path=tests/fixtures/acceptance-hardening/mixed-path/test-evidence/smoke.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-001_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the fixture's main flow completed once, exit 0

SC-002_status=fail
SC-002_value=the error path returned exit 0 instead of the documented failure code

SC-003_status=deferred
SC-003_value=not attempted this round
SC-003_deferred_reason=the hygiene note is written only after a clean error-path run
SC-003_blocked_at=2026-11-03
SC-003_reduced_measurement=the hygiene section header exists in this file
SC-003_reduced_measurement_run=yes
SC-003_why_reduced_insufficient=a header records the intent to write a note, not the note
SC-003_unblock=run the error path cleanly once, then record the hygiene note
