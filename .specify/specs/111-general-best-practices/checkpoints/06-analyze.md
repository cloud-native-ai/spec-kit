# Checkpoint 06 — analyze (line general-best-practices)

- **U4**: pass after repair + round 2. Round-1 CRITICAL/HIGH all FIXED (AR1-02/01/03); round-2 open set **C 0 / H 0 / M 4 / L 6** (residues deferred with reasons).
- **Repair commit**: `61e3ccfb6`; round-2 report commit `93326d8bc`; evidence `analyze-round2-*`.
- **Gate**: no open CRITICAL/HIGH → proceed to implement. Residues are review-visible.
- **Goal/team**: none; `not_evaluated`.
- **Next (implement)**: split into 2 serial packages T001–T010 / T011–T019 (≤16 each); siblings 110 (analyze-repair) and 112 (clarify) concurrent.
- **Direction audit**: rules in force; the repair was verified by an independent round-2 pass, not self-reported; next per plan; spine fresh; territory = feature + evidence. Verdict `correction-applied` (analyze repair), otherwise on-track.
