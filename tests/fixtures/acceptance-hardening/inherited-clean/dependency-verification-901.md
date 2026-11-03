<!-- Fixture case: acceptance-hardening/inherited-clean — dependency side.
     This is the verification log of fixture Feature 901, the only dependency of fixture Feature 900. Declarative
     input, not a real log.
     The same dependency side as `inherited-mutation`: the pair differs only in the plan's dispositions. -->

# Verification Log — 901-acceptance-fixture-dependency

deferred_tasks=T007,T008

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the dependency's own main flow completed once, exit 0

SC-002_status=blocked
SC-002_value=not measured: the dependency's journey needs a target this fixture does not have
SC-002_blocked_at=2026-11-03
SC-002_reduced_measurement=the dependency's task list is fully closed
SC-002_reduced_measurement_run=yes
SC-002_why_reduced_insufficient=a closed task list says the bookkeeping finished, not that the journey ran
SC-002_unblock=run the dependency's journey once end to end

SC-003_status=deferred
SC-003_value=not attempted this round
SC-003_deferred_reason=the dependency's error path is only reachable after its main flow runs
SC-003_blocked_at=2026-11-03
SC-003_reduced_measurement=the dependency's error-path task is closed
SC-003_reduced_measurement_run=yes
SC-003_why_reduced_insufficient=a closed task is a claim about work, not a measurement of the path
SC-003_unblock=run the dependency's error path once

SC-004_status=partial
SC-004_value=half of the dependency's matrix rows were measured
SC-004_blocked_at=2026-11-03
SC-004_reduced_measurement=the measured half of the dependency's matrix
SC-004_reduced_measurement_run=yes
SC-004_why_reduced_insufficient=a half matrix cannot stand in for the full matrix
SC-004_unblock=measure the dependency's remaining matrix rows
