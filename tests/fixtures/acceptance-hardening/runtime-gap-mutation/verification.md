<!-- Fixture case: acceptance-hardening/runtime-gap-mutation — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     The verification side is complete on purpose: every criterion measured, the smoke record present, the
     joint-acceptance row naming `RS-001` present. The reasons in play come from the runtime-stack section only. -->

# Verification Log — 900-acceptance-fixture-runtime-gap-mutation

# -- Smoke test record (exactly one per feature) --

smoke_command=python3 -c "print('acceptance-fixture-runtime-gap-mutation')"
smoke_exit_code=0
smoke_evidence_path=tests/fixtures/acceptance-hardening/runtime-gap-mutation/test-evidence/smoke.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-001_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the fixture's main flow completed once, exit 0
SC-002_status=pass
SC-002_value=the hygiene note is recorded in this file
