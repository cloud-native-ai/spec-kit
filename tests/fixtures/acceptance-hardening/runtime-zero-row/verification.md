<!-- Fixture case: acceptance-hardening/runtime-zero-row — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     Carried over unchanged from `positive` — including the `RS-001_joint_acceptance` row — because this fixture
     mutates exactly one thing: the data rows of the runtime-stack table. A single-variable mutation is what
     makes the emitted reason attributable. -->

# Verification Log — 900-acceptance-fixture-runtime-zero-row

# -- Smoke test record (exactly one per feature) --

smoke_command=python3 -c "print('acceptance-fixture-runtime-zero-row')"
smoke_exit_code=0
smoke_evidence_path=tests/fixtures/acceptance-hardening/runtime-zero-row/test-evidence/smoke.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-001_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the fixture's main flow completed once, exit 0
SC-002_status=pass
SC-002_value=the hygiene note is recorded in this file
