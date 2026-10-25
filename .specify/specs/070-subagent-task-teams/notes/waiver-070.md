# User Waiver — SC-001 / SC-002 (Feature 070)

- **Date**: 2026-10-25
- **Decision**: the user explicitly waived **SC-001** (median wall-clock reduction) and **SC-002** (stage executions per canonical stage) for Feature 070.
- **Reason**: the decomposition/coordination mechanism, functional behavior, and all quality gates are verified (39/39 tasks; analyze READY 0 CRITICAL / 0 HIGH; review pending; mirror synced). A comparable real decomposed `plan`/`review` benchmark requires at least three samples and driver dogfooding, which is deferred to a later run. No fabricated metric is claimed; both criteria remain `not_evaluated` in `notes/benchmark-070.md`.
- **Scope**: SC-003…SC-008 remain in force. This waiver satisfies the A-18 closure block for SC-001/SC-002 only.
- **Follow-up**: after the driver adopts the 070 mechanism, run a ≥3-sample comparable benchmark (same interval, host, and topology) and replace the `not_evaluated` record; do not mix sources.
- **Authority**: user decision recorded in the driving session on 2026-10-25; committed by the driver at closure.
