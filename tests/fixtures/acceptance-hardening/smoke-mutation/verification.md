<!-- Fixture case: acceptance-hardening/smoke-mutation — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     Every `final`-path SC passes; the smoke record (command / exit code / evidence path) is absent, and the
     claimed status is `Implemented`. A missing smoke record is not an input error — it is the feature failing
     completion condition ④ while claiming otherwise. -->

# Verification Log — 900-acceptance-fixture-smoke-mutation

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-001_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the fixture's main flow completed once, exit 0
SC-002_status=pass
SC-002_value=the hygiene note is recorded in this file
