<!-- Fixture case: acceptance-hardening/ladder-mutation — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     All five ladder fields are present; the row is still illegal, because the reduced measurement was written
     down and never run (`run=no` with a non-empty `reduced_measurement`). -->

# Verification Log — 900-acceptance-fixture-ladder-mutation

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-001_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=blocked
SC-001_value=not measured: the fixture's main flow needs a target this fixture does not have
SC-001_blocked_at=2026-11-03
SC-001_reduced_measurement=the fixture's task list is fully closed
SC-001_reduced_measurement_run=no
SC-001_why_reduced_insufficient=a closed task list says the bookkeeping finished, not that the journey ran
SC-001_unblock=run the fixture's main flow once end to end
