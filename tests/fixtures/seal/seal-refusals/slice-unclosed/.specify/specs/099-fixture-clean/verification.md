<!-- Fixture case: seal/seal-refusals/slice-unclosed — see requirements.md for the fixture notice.
     Every `final`-path SC passes and the smoke record is complete. -->

# Verification Log — 099-fixture-clean

# -- Smoke test record (exactly one per feature) --

smoke_command=python3 -c "print('seal-fixture-clean')"
smoke_exit_code=0
smoke_evidence_path=.specify/specs/099-fixture-clean/test-evidence/smoke.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-001_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the fixture's main flow completed once, exit 0
SC-002_status=pass
SC-002_value=the hygiene note is recorded in this file
