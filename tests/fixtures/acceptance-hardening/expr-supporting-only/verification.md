<!-- Fixture case: acceptance-hardening/expr-supporting-only — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     No smoke record: the smoke obligation attaches to `execution`-class features. `SC-002` is deferred with
     the full ladder, which is legal on a `supporting` path. -->

# Verification Log — 900-acceptance-fixture-expr-supporting-only

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

# none: the single runtime-stack row is `not-required`

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the note states the boundary rule it illustrates

SC-002_status=deferred
SC-002_value=not attempted this round
SC-002_deferred_reason=the cross-check needs a second example set the fixture does not carry
SC-002_blocked_at=2026-11-03
SC-002_reduced_measurement=the example count is recorded in the note
SC-002_reduced_measurement_run=yes
SC-002_why_reduced_insufficient=a count is not a cross-check
SC-002_unblock=add the second example set and re-read the note against both
