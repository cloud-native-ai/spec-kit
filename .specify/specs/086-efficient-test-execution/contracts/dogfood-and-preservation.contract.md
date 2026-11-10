# Contract: 085 Preservation, Parallel Safety and Dogfood Evidence (C-041…C-052)

Owner of the propositions below: this contract. Implementation surfaces: the marked test file, the newly
added preservation guard, the registry and CHANGELOG rows, and this spec's evidence directory.

**Inherited, not restated**: the temporary Goal/Team, stage-agent, concurrency, worktree-isolation,
integration-queue and checkpoint mechanisms are owned by
`.specify/specs/085-sdd-temporary-goal-team/{requirements.md,plan.md,contracts/}`. The feature-status and
verification vocabulary are owned by `shared/workflow/acceptance-hardening.md`. This contract adds only the
preservation assertion, the parallel-safety disposition and the evidence shape for SC-010.

## A. Preservation of the 085 surface

- **C-041**: No commit of this feature MAY modify, delete or rewrite any file under
  `.specify/specs/085-sdd-temporary-goal-team/` or `.specify/anchoring/` or `.specify/teams/`, with exactly one
  narrow carve-out: the SC-010 status / value / note / blocked_at lines of
  `.specify/specs/085-sdd-temporary-goal-team/verification.md` MAY be updated, and only those lines — every
  other line of that file and every other 085 path MUST stay byte-identical (FR-027, FR-030). The carve-out
  is authorized by FR-030 and is the only 085 write this feature makes; `requirements.md` FR-027 states it,
  and `plan.md` R-8 / WP-C2 / the temporary Team's `forbidden` territory carry the same narrow wording. The
  check is mechanical and two-part: (a) `git diff -U0 --name-only <stage-base>..<closure-commit> --
  .specify/specs/085-sdd-temporary-goal-team .specify/anchoring .specify/teams` MUST name at most
  `verification.md`; (b) `git diff -U0 <stage-base>..<closure-commit> --
  .specify/specs/085-sdd-temporary-goal-team/verification.md` MUST contain only hunks whose added and removed
  lines each match `^SC-010_(status|value|note|blocked_at)=`. Any other 085 path in (a), or any hunk in (b)
  that adds or removes a non-`SC-010_*` line, fails the clause. `verification.md` is named by 085's own
  `plan.md` as the `/speckit.implement` output artifact (085 `plan.md` line 117), which is what makes the
  status line a live reference rather than a rewrite of a frozen record (A12, A17).
- **C-042**: Additive use is required, not merely permitted: this feature's own run MUST create a spec-local
  temporary Goal (already present) and a spec-local temporary Team, and MUST leave per-stage checkpoints. A
  run that bypasses the 085 mechanisms fails the clause even though no file was changed (FR-028).
- **C-043**: 085's contract and integration tests MUST be re-run after this feature's changes and MUST show
  zero new failure names against the same-tree serial baseline. `/speckit.tasks` MUST name the concrete test
  files it will run; this contract names the obligation, not a canonical list (FR-029).

## B. Parallel safety

- **C-044**: The watch-target self-test (`tests/contract/test_sdd_loop_driver_skill.py::test_c22_watch_target_hook_selftest`)
  MUST be declared a serial exception via the `serial` marker (C-010…C-012 of
  `contracts/runner-contract-086.contract.md`). It MUST NOT be skipped, xfailed, deleted, or given a raised
  timeout unless the marker form is demonstrated unable to preserve the name list and the exit code
  (FR-010, FR-012).
- **C-045**: Any **other** test that becomes parallel-unsafe as measured by the post-change name diff MUST be
  resolved by the same three-way disposition (root-cause fix / named serial exception / pre-existing baseline
  failure). A root-cause fix MUST be the choice when the cause is shared mutable state (a fixed path, a
  fixed port, a fixed repo root): isolation via `tmp_path` or a per-worker path, never "run this test only on
  one worker" (FR-010, FR-013).
- **C-046**: Tests that pass in parallel today (including the mirror probe, the smoke evidence and the
  whole-worktree `git status` assertions) MUST NOT be rewritten pre-emptively. If the post-change run makes
  one of them fail, the fix MUST preserve the proposition the assertion makes: scope the assertion to the
  paths it actually claims, or move the probe into a temp sandbox — never weaken it (FR-010).
- **C-047**: The final closure comparison MUST be a name-level diff in both directions against the
  implementation-start baseline slot: added names MUST be `0` after attribution; dropped names MUST be
  recorded and MUST NOT be claimed as this feature's fix (FR-014).

## C. Dogfood evidence (085 SC-010)

- **C-048**: The evidence directory `test-evidence/` MUST contain a dogfood record naming, per stage: the
  carrier identity (host-native agent), `agent_concurrency_requested`, `agent_concurrency_effective` with the
  named reason when lower, the checkpoint path, and the stage's completion state (FR-028).
- **C-049**: At least one stage MUST show an actual maximum concurrency greater than one, taken from dispatch
  records rather than from the declared value (FR-028).
- **C-050**: 085 SC-010's status MUST be updated from `partial` only when the full chain of C-048 evidence
  exists — every stage, a checkpoint each, and C-049 satisfied. Otherwise the status MUST stay `partial` and
  the remaining gap MUST be named in one line. "The feature ran once" is not sufficient evidence (FR-030).
- **C-051**: The carrier downgrade (host-native agent identities standing in for 085's stage-agent types,
  `plan.md` § 085 Carrier Observation) MUST be recorded in the evidence as an observation. It MUST NOT be
  recorded as a 085 failure and MUST NOT be repaired in this feature (FR-027, FR-028).

## D. Records

- **C-052**: `.specify/features/086-efficient-test-execution.md` and the `086` row of `.specify/features.md` MUST reach
  `Planned` in the plan stage and subsequently reflect `Implemented`/`Blocked` per
  `shared/workflow/acceptance-hardening.md`; `CHANGELOG.md` MUST carry one entry describing the runner
  default change, the new principle and the dev-side dependency in user-visible terms, pointing at the owner
  guideline rather than restating it (FR-031, FR-033).

## Mutation Legs

The legs across all four contracts number **19** (M-1…M-7 in `runner-contract-086.contract.md`, M-8…M-9 in
`budget-ledger-parser.contract.md`, M-10…M-15 in `principle-landing.contract.md`, M-16…M-19 here). Each leg is
carried by exactly one task row; the leg → task → expected-fail map lives in `tasks.md` § Mutation Leg
Carriers, which is the single place a reviewer reads it.

| Leg | Mutation | Must fail |
|-----|----------|-----------|
| M-16 | Touch one byte in `.specify/specs/085-sdd-temporary-goal-team/verification.md` **outside** the `SC-010_status` / `SC-010_value` / `SC-010_note` / `SC-010_blocked_at` lines (the carve-out lines themselves are admissible under C-041) | C-041 |
| M-17 | Skip (rather than mark) the watch-target self-test in a parallel run | C-044 |
| M-18 | Claim 085 SC-010 `pass` with only requirements/clarify/plan checkpoints present | C-050 |
| M-19 | Report `agent_concurrency_effective` from the declared 24 while the stage actually dispatched one agent | C-049 |
