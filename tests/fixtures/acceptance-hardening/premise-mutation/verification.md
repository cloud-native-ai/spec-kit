<!-- Fixture case: acceptance-hardening/premise-mutation — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     The verification side is complete on purpose: every criterion measured, the smoke record present, the
     `in-scope` joint-acceptance row present. The only reason in play is the emptied `Decision` cell in plan.md. -->

# Verification Log — 900-acceptance-fixture-premise-mutation

# -- Smoke test record (exactly one per feature) --

smoke_command=python3 -c "print('acceptance-fixture-premise-mutation')"
smoke_exit_code=0
smoke_evidence_path=tests/fixtures/acceptance-hardening/premise-mutation/test-evidence/smoke.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-001_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the fixture's main flow completed once, exit 0
SC-002_status=pass
SC-002_value=the hygiene note is recorded in this file
