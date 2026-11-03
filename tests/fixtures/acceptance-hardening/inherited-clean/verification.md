<!-- Fixture case: acceptance-hardening/inherited-clean — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     Nothing on this side is defective, and neither is the plan side: this fixture must be accepted. -->

# Verification Log — 900-acceptance-fixture-inherited-clean

# -- Smoke test record (exactly one per feature) --

smoke_command=python3 -c "print('acceptance-fixture-inherited-clean')"
smoke_exit_code=0
smoke_evidence_path=tests/fixtures/acceptance-hardening/inherited-clean/test-evidence/smoke.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-001_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the fixture's main flow completed once, exit 0
SC-002_status=pass
SC-002_value=the hygiene note is recorded in this file
