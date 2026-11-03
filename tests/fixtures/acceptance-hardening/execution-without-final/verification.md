<!-- Fixture case: acceptance-hardening/execution-without-final — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     Both criteria pass and the smoke record is complete — every bookkeeping box is ticked, and the feature is
     still not acceptable, because an `execution` feature with no `final`-path criterion has nothing that
     could make it acceptable. -->

# Verification Log — 900-acceptance-fixture-execution-without-final

# -- Smoke test record (exactly one per feature) --

smoke_command=python3 -c "print('acceptance-fixture-execution-without-final')"
smoke_exit_code=0
smoke_evidence_path=tests/fixtures/acceptance-hardening/execution-without-final/test-evidence/smoke.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-001_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the helper script parses its own arguments, exit 0
SC-002_status=pass
SC-002_value=the helper script's unit test passes
