<!-- Fixture case: seal/merged-clean — see requirements.md for the fixture notice.
     Every `final`-path SC passes and the smoke record is complete. -->

# Verification Log — 099-fixture-merged

# -- Smoke test record (exactly one per feature) --

smoke_command=python3 -c "print('seal-fixture-merged')"
smoke_exit_code=0
smoke_evidence_path=.specify/specs/099-fixture-merged/test-evidence/smoke.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-001_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the fixture's main flow completed once, exit 0
SC-002_status=pass
SC-002_value=the hygiene note is recorded in this file

<!-- begin: merge-apply aggregated pointer view (generated) -->
SC-001_status=pass
SC-001_note=.specify/specs/099a-fixture-slice/verification.md (099a-fixture-slice local row SC-001)
<!-- end: merge-apply aggregated pointer view -->
