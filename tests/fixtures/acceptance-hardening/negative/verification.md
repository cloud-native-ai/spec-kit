<!-- Fixture case: acceptance-hardening/negative — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     Every SC has a status row; both `final`-path SCs are non-`pass`, each with the full measurement ladder.
     No smoke record exists — as in 026 — and a missing smoke record is never an input error, only a
     completeness fact about the feature. -->

# Verification Log — 900-acceptance-fixture-negative

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-001_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=blocked
SC-001_value=not measured: the fixture's main flow needs a target this fixture does not have
SC-001_blocked_at=2026-11-03
SC-001_reduced_measurement=the fixture's task list is fully closed
SC-001_reduced_measurement_run=yes
SC-001_why_reduced_insufficient=a closed task list says the bookkeeping finished, not that the journey ran
SC-001_unblock=run the fixture's main flow once end to end

SC-002_status=deferred
SC-002_value=not attempted this round
SC-002_deferred_reason=the error path is only reachable after the main flow runs
SC-002_blocked_at=2026-11-03
SC-002_reduced_measurement=the error-path task is closed
SC-002_reduced_measurement_run=yes
SC-002_why_reduced_insufficient=a closed task is a claim about work, not a measurement of the path
SC-002_unblock=run the fixture's error path once, after the main flow
