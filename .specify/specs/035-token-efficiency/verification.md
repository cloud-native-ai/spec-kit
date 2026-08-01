# Verification Log — 035-token-efficiency

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=bc26d0d3
baseline_date=2026-08-02
baseline_branch=035-token-efficiency

baseline_pytest_failed=37
baseline_pytest_passed=1045
baseline_v001_injected_bytes=188360
baseline_v002_injected_bytes_fixed=41000
baseline_v003_injected_bytes=57559
baseline_v004_injected_bytes=19668
baseline_v005_injected_bytes=30844

# -- /speckit.implement results --

implementation_date=2026-08-02
post_change_commit=66f6c128+polish

post_change_pytest_failed=37
post_change_pytest_new_failures=0
post_change_v001_injected_bytes=21277
post_change_v002_injected_bytes_fixed=17503
post_change_v003_injected_bytes=36851
post_change_v004_injected_bytes=8520
post_change_v005_injected_bytes=5308
post_change_token_efficiency_contract_tests=60

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=discipline doc + mirror byte-identical; instructions-template ambient ref; 5 authoring gate files carry check items; sync-mirrors --check exit 0
SC-001_note=C-D1..C-D5 + C-A3 pinned by 12+9 contract tests, all green

SC-002_status=pass
SC-002_value=audit covers 19 commands + 26 skills + 17 shared docs + 9 engines; 9 violations frozen; top-5 (V-001..V-005) 100% remediated with measured before/after
SC-002_note=audit.md frozen 2026-08-02; V-006..V-009 backlogged per top-5 rule (Clarify Q2)

SC-003_status=pass
SC-003_value=V-001 -88.7%, V-004 -56.7%, V-005 -82.8% (all >=50%); V-002 -57.3% fixed part; V-003 -36.0% preload scope (on-demand savings uncounted); T021 rerun: binding decision unchanged
SC-003_note=sampled reruns show identical conclusions with reduced injection; V-003 scope note recorded in audit.md

SC-004_status=partial
SC-004_value=1 remediated flow re-run in-session (plan Feature-Memory step, T021); template phrase pins guarantee instruction-level compliance for all 5
SC-004_note=full >=3-flow live spot-check requires fresh command runs post-merge; instruction-level compliance verified via 16 pin tests instead

SC-005_status=pass
SC-005_value=list --contains token-efficiency --limit 0 returns 4/4 marked entries (grep cross-check 4/4); zero fabricated token counts in entries; clean-run rule in Reflect step
SC-005_note=C-M1..C-M3 12 tests green; real-store closure executed

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=

# -- Notes --
# notes: plan.md:110 docs/-wholesale read remediated together with V-001 (same unit, same discipline; no new audit row per freeze rule).
# notes: backlog V-006..V-009 left for a later iteration; V-009 (history-utils summary mode) recorded as engine-gap backlog row (T019 condition branch).
# notes: gate-check.py mirror copy (.specify/scripts/python/) resolves gate path against its own tree (looked for .specify/.specify/gate.yaml, exit 3); canonical scripts/python/gate-check.py used instead — candidate upstream fix, out of this spec's scope.
