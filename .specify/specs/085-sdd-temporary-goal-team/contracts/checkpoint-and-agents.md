# Contract — Checkpoints

Owners: `skills/internal/improve-team/SKILL.md` (targeted team edits), `skills/internal/manage-goal/SKILL.md` § coordinate (proposal shape), `skills/external/sdd-loop-driver/references/decomposition-model.md` (metrics), `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` (the checkpoint's five parts).

- **C-001**: After every stage U4 and before the next dispatch, the driver MUST run the five-part checkpoint defined in `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` — parts 1–4 carried by C-002…C-006 below, plus part 5, the Direction audit, which is mandatory (C-014).
  <!-- superseded by: skills/external/sdd-loop-driver/references/checkpoint-protocol.md (five-part checkpoint; part 5 Direction audit is mandatory) -->
  <!-- prior text, retained (2026-11-09): C-001 "the driver MUST run a four-part checkpoint"; C-008 "All four parts MUST be present" -->
- **C-002**: Part 1 MUST consume the U4 verdict and a `loop-state.py` snapshot; it MUST NOT infer completion from self-report.
- **C-003**: Part 2 MUST record `criterion / degree / evidence_ptr` for the temporary goal; goal content changes only through the goal engine.
- **C-004**: Part 3 MUST produce at most one team-configuration proposal, with its evidence and exact delta.
- **C-005**: The proposal MUST be ratified according to `checkpoint_policy.ratification` before it is applied.
- **C-006**: Part 4 MUST record the next stage's requested/effective concurrency and roster decision.
- **C-007**: The checkpoint MUST be written to `.specify/specs/<NNN-slug>/checkpoints/<NN>-<stage>.md`; a final `closure.md` MUST record the terminal goal degree table and the archived team state.
- **C-008**: All five parts MUST be present; an inapplicable part MUST carry `n/a` and a reason, never omission.
- **C-009**: A checkpoint MUST apply at most one configuration, concurrency, or roster change; an explicit human goal edit does not count.
- **C-010**: The proposal evidence MUST come from `wp-report.py`, the team run report, and the ledger; no new metric store.
- **C-011**: Rollback MUST trigger on the next checkpoint when U4 fails, new test failures appear, package retries increase by at least two, or parallelism efficiency drops by at least 30 percent.
- **C-012**: A rolled-back change MUST NOT be re-proposed immediately.
- **C-013**: Territory changes MUST go through an explicit `/speckit.team modify`; `coordinate` remains territory-overlap only. (FR-037, FR-038, FR-039, FR-040, FR-041, FR-042)
- **C-014**: Part 5 MUST be the Direction audit: the reload tier plus the five binary questions and exactly one verdict of `on-track` / `correction-applied` / `decision-needed`, judged with the RULES before the goal; a checkpoint without it is a defect, and the audit MUST NOT end with a question to the user.
