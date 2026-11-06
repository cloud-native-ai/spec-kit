# Contract — Checkpoints

Owners: `skills/internal/improve-team/SKILL.md` (targeted team edits), `skills/internal/manage-goal/SKILL.md` § coordinate (proposal shape), `skills/external/sdd-loop-driver/references/decomposition-model.md` (metrics).

- **C-001**: After every stage U4 and before the next dispatch, the driver MUST run a four-part checkpoint.
- **C-002**: Part 1 MUST consume the U4 verdict and a `loop-state.py` snapshot; it MUST NOT infer completion from self-report.
- **C-003**: Part 2 MUST record `criterion / degree / evidence_ptr` for the temporary goal; goal content changes only through the goal engine.
- **C-004**: Part 3 MUST produce at most one team-configuration proposal, with its evidence and exact delta.
- **C-005**: The proposal MUST be ratified according to `checkpoint_policy.ratification` before it is applied.
- **C-006**: Part 4 MUST record the next stage's requested/effective concurrency and roster decision.
- **C-007**: The checkpoint MUST be written to `.specify/specs/<NNN-slug>/checkpoints/<NN>-<stage>.md`; a final `closure.md` MUST record the terminal goal degree table and the archived team state.
- **C-008**: All four parts MUST be present; an inapplicable part MUST carry `n/a` and a reason, never omission.
- **C-009**: A checkpoint MUST apply at most one configuration, concurrency, or roster change; an explicit human goal edit does not count.
- **C-010**: The proposal evidence MUST come from `wp-report.py`, the team run report, and the ledger; no new metric store.
- **C-011**: Rollback MUST trigger on the next checkpoint when U4 fails, new test failures appear, package retries increase by at least two, or parallelism efficiency drops by at least 30 percent.
- **C-012**: A rolled-back change MUST NOT be re-proposed immediately.
- **C-013**: Territory changes MUST go through an explicit `/speckit.team modify`; `coordinate` remains territory-overlap only. (FR-037, FR-038, FR-039, FR-040, FR-041, FR-042)
