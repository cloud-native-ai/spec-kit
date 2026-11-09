# verification — 091-auto-git-closeout, implement stage — 2026-11-09

**Stage**: implement (completion slice 2) · **Run**: `r20261109T023000Z-auto-closeout` · **Branch**: `master`
**Authority**: `requirements.md` (FR-001…FR-028 / SC-001…SC-008) · `plan.md` · `contracts/` (**32** clauses:
declaration C-1…C-7, lifecycle C-1…C-10, executor C-1…C-8, verification C-1…C-7) · `tasks.md` (**62** rows, all closed)
**Implement-entry baseline**: `test-evidence/baseline-failed.txt` (36 failed node ids, captured by T002 at the
implement entry of slice 1).

## Success criteria

| Criterion | Path | Status | Evidence | Reading |
|---|---|---|---|---|
| SC-001 | final | **pass** | `test-evidence/T030-forks.txt`, `tests/contract/test_git_closeout_contract.py::test_single_and_dual_branch_models_reach_the_expected_end_state` / `::test_three_tier_model_advances_through_the_intermediate_branch` / `::test_the_reference_carries_all_four_derived_sequences` | four models, four fixture repositories, each end state asserted on branch existence, HEAD and what the bare remote actually holds |
| SC-002 | final | **pass** | `::test_the_two_declaration_rows_exist_with_the_closed_value_set` (parameterised over the shipped asset and this project's instance), `::test_mutation_*` arms | the two rows, the four-value closed set and the `ask` default are pinned on both surfaces; the mutation arms red on an illegal value and on a deleted row |
| SC-003 | final | **pass** | `test-evidence/mutations.txt` § R-21b, `test-evidence/T041-mutation-probe.py`, `::test_a_rejected_push_stops_before_the_remote_changes` / `::test_a_merge_conflict_stops_before_any_push` | both failure fixtures green; the injected retry now reds through the `retries` axis that this slice added (see § Rulings R-21b) |
| SC-004 | final | **pass** | `::test_the_destructive_boundary_did_not_shrink_by_gate_name`, `test-evidence/T056-mirrors.txt` | gate set compared **by name** against the same-run scan; pre-change `27` (`destructive 20` / `governance_kept 7`, `violations 0`) reproduced after the change; no surface carries the list's plain text |
| SC-005 | final | **pass** | `::test_every_unattended_mechanism_reaches_the_one_owner`, `::test_mutation_a_second_closeout_owner_reds_the_single_owner_search` | three unattended mechanisms reach the one owner by pointer; the negative search finds no second close-out owner or engine |
| SC-006 | supporting | **pass** | `test-evidence/dry-run-closeout.txt`, `test-evidence/dry-run-closeout.py`, `test-evidence/dry-run-closeout-rerun.txt` | derived sequence printed for this repository's declared model and strategy; remote reference listing byte-identical before and after; no branch created |
| SC-007 | supporting | **pass** | `test-evidence/T030-forks.txt`, `::test_three_forks_are_three_distinct_behaviours`, `::test_report_field_set_is_enumerated_and_omission_is_a_defect` | read-only fork skips with one line and no commit step; artifacts-without-records fork still merges and pushes and says so |
| SC-008 | final | **pass** | `::test_the_destructive_boundary_did_not_shrink_by_gate_name`, `::test_mutation_a_dropped_gate_id_reds_the_closed_set_comparison`, `::test_the_hand_off_points_at_the_gate_owner_instead_of_restating_it` | baseline object, comparison unit and `shared/guidelines/closed-set-claims.md` are all named inside the test; dropping one gate reds it, copying the list into a surface reds the pointer guard |

`[final]`-path criteria in `blocked` / `deferred` / `fail`: **none**. `deferred_tasks=` (empty) — no row was deferred.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| GATE-1 no NEW failure | **pass** — NEW `0` once R-36a's four `test_compile_embeds.py` ids are read at their measured standing (`git stash -u` A/B: red at `HEAD` too); cleared `6`. The one failure this slice really introduced was repaired at the root, not waived | `test-evidence/final-full.txt`, `test-evidence/final-failed.txt`, `test-evidence/baseline-failed.txt` |
| GATE-2 guard module green and mutation arms red | **pass** — `42 passed`; six mutation arms, each with a landed-green / mutated-red pair | `test-evidence/T062-smoke.txt`, `test-evidence/mutations.txt` |
| GATE-3 mirror obligations | **pass** — `sync-mirrors.py --check` exit 0 and `compile-embeds --check` exit 0 (`79 units, zero drift`), both re-run at the end of this slice | `test-evidence/implement-gates.txt` § 1–2, `test-evidence/T056-mirrors.txt` |
| GATE-4 no open task rows | **pass** — `grep -cE '^- \[[ >~]\]' tasks.md` → `0`; `62` rows, all `[X]` | `tasks.md` |
| GATE-5 final-path criteria pass + smoke record | **pass** — six `final`-path criteria all `pass`; the smoke record below | `test-evidence/T062-smoke.txt` |
| GATE-6 structure, clause attribution, coverage lanes | **pass** — `validate-tasks.py` `0 error(s)`; `account-clause-coverage.py` exit 0, `FR claimed 28 / uncovered 0`, `claimed clauses 32`, `uncovered beyond baseline 0`, `status: ok` | `test-evidence/implement-gates.txt` |

## Definition of Done

| Item | Result |
|---|---|
| DoD-1 FR lane | **pass** — `fr.uncovered` 0 of 28, reproduced this slice |
| DoD-2 clause lane | **pass** — 32 clauses, 32 claims, 0 duplicates; `green-dangling` 0, `green-clause-collision` 0, `green-cross-phase` **2** (both disclosed in `tasks.md` § Green Partition: T057→declaration C-2, T061→executor C-8) |
| DoD-3 no second constant on the destructive boundary | **pass** — the guard compares gate ids by name; `test_wrap_up_wording_gate_safe.py::test_confirmation_gate_budget_unchanged` untouched and passing |
| DoD-4 no NEW failure | **pass** — `0` new ids once R-36a is applied; see § Full-suite baseline comparison |
| DoD-5 mirrors and compiled faces generated | **pass** — `sync-mirrors.py --check` 0, `compile-embeds --check` 0 |
| DoD-6 evidence for every `final`-path criterion | **pass** — every row of § Success criteria names a file produced in this feature's run |
| DoD-7 every ruling disclosed in § Notes | **pass** — A-G1…A-G4 at generation; R-14…R-23 and R-21b in this file's § Rulings |

## Smoke record

```
smoke_command=SPECKIT_PYTHON=/usr/bin/python3 /usr/bin/python3 -m pytest tests/contract/test_git_closeout_contract.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/091-auto-git-closeout/test-evidence/T062-smoke.txt
```

End-to-end over the feature's main flow: the module derives a sequence from a declaration, executes it
against a throwaway repository with a local bare remote, and asserts the end state — the close-out itself,
not a unit of it.

## Full-suite baseline comparison

| Quantity | Implement-entry baseline (`baseline-failed.txt`) | Final (`final-full.txt` → `final-failed.txt`) |
|---|---|---|
| failed node ids | 36 | **34** |
| passed / skipped | `8026 passed, 2 skipped` | **`8045 passed, 2 skipped`** |
| run wall clock | not recorded at entry | `566.07s` |

**Selection, disclosed rather than implied.** `final-full.txt` is `tests/` as a whole plus *re-inclusion* of the three
modules the first restart had skipped — `test_compile_embeds.py` (4 ids), `test_engine_face_contract.py`,
`test_compile_reconcile_guards.py`. Those three are R-36a. In this run the environment killed them at ~0.2 s each with
`failed` (not `error`), so their four ids appear in `final-failed.txt` and **must be read through R-36a, not as
regressions**: the same four are red at `HEAD` with this feature's changes stashed (`git stash -u`, re-run this slice)
— the exact A/B that earns the exclusion. Every other id in the list is an entry-baseline id.

Comparison command (GATE-1's own form):

    LC_ALL=C comm -13 .../test-evidence/baseline-failed.txt .../test-evidence/final-failed.txt   # NEW
    LC_ALL=C comm -23 .../test-evidence/baseline-failed.txt .../test-evidence/final-failed.txt   # cleared

**Reading (measured, not asserted)** — re-measured after the last repair, on the final run:

- **NEW: 4 ids, all of them R-36a's (`test_compile_embeds.py`).** Excluding R-36a's three modules, **NEW = 0**. The
  one *real* new failure this slice produced was found and repaired at the root, not waived:
  `test_decision_tension_contract.py::TestScenarioBAnalyzeStructuralChannel::test_channel_only_add_allowed_delta_enumeration`.
  That clause pins the allowed delta on `skills/analyze/SKILL.md` (enumeration paragraph ∪ `## Rounds` ∪ compiled
  banner), and 091's registry row makes every compiled face gain a close-out step line. The guard now reads that line
  **out of git** in the same shape as the banner (`closeout_step_delta`), so the claim stays decidable — a close-out
  line outside `## Wrap-up`, a second such line, or any fifth delta still reds it. The C-5 comment names the
  allowance.
- **Cleared: 6 ids** — `test_mirror_parity_suite.py::…git-workflow-block.md…`,
  `test_script_interface_contract.py::test_c33…` / `::test_c35…`,
  `test_scripts_distribution_parity.py::…`, `test_shipped_surface_client_neutrality.py::…`,
  `test_trigger_engine.py::test_c2_sync_mirrors_check_clean`. All six are mirror/byte-state readings that the entry
  baseline captured while the tree was dirty between slices; they are green now that the tree is synced. Recorded as
  cleared, **not** claimed as an improvement.
- **Repaired in this slice (never appear in the final list)**: the three compiled-face closing-step pins
  (`test_client_guard_sweep.py::test_c53…`, `test_review_code_composition.py::test_c16…`,
  `test_review_feedback_boundary.py::test_c55…` ×2) and
  `test_humanize_command_surface.py::test_wc07_skill_body_budget`, which the extra compiled step pushed from `4999` to
  `5023` tokens against a `5000` ceiling. The body was slimmed back to `4998` by deleting one line that restated the
  option set its own contract owner (`references/run-mode.md` § Parse) already carries — one-source-of-truth, no rule
  text dropped.
- **Two readings exist for this stage and only one is the verdict.** A first final run (`42 failed, 8037 passed`) was
  taken while `sync-mirrors.py` and the humanize edit were still in flight; it caught the tree mid-edit and is kept
  as `test-evidence/run-note-sandbox.txt`, never as acceptance. The numbers above are the post-repair run.

## Rulings made this stage (DoD-7 discharge)

- **R-14 (tasks.md stale premises) — discharged.** Five cells were re-derived: clause count 26 → **32**,
  data-model rules 14 → **17**, task rows 60 → **62**, FRs with no numeric citation 4 → **0**, and the
  Environment-Prerequisites `coverage-baseline.txt` bullet now reads "present, frozen by T005". The three-module
  cell gained the implement-entry re-measurement (`836 passed`, up one from `835` because this feature's own
  fixtures add a test to `test_mirror_parity_suite.py`'s parameterisation) — the criterion stays "no NEW failure",
  never a frozen number. Evidence: `tasks.md` § Premises.
- **R-15 (CHK016, FR-017 / FR-018 in tension) — recorded, FR text untouched.** FR-017 states that
  `commit+merge+push` is a project-level standing authorization for the routine actions **inside** the derived
  sequence and "MUST NOT be read as a global exemption for actions on the confirmation-gate list
  (force-push, push to a read-only upstream, destruction of a cross-project shared branch)". FR-018 forbids any
  surface of this feature from copying the gate list's plain text and requires pointer-only reference. **The
  settled reading, adopted and now measured**: FR-017's parenthetical enumerates the three classes *in order to
  exclude them*, i.e. it is the same proposition FR-018 makes from the other side — "these three keep their own
  gate". Evidence for the operative half: declaration C-7's own text carries the three class **names** (as
  exclusions, not as a copied procedure), while **every surface this feature writes** — `closeout-commands.md`,
  `artifact-commit-step.md` § Close-out, `git-utils/SKILL.md` — reaches the list only by the path
  `shared/guidelines/confirmation-gates.md`. `::test_the_hand_off_points_at_the_gate_owner_instead_of_restating_it`
  is the guard and it is green; `::test_mutation_a_gate_list_copied_into_a_surface_reds_the_pointer_guard` is the
  control. The requirements text is not edited here: a re-cut of an accepted FR belongs to an analyze pass, and
  doing it inside implement would be exactly the silent normalisation `fast-fail.md` forbids.
  **Measured, and disclosed rather than smoothed**: the four-value probe
  (`test-evidence/T041-mutation-probe.py --r15`) reads
  `commit+merge+push → terminal=executed, pushed=('mirror',)`; `ask → terminal=presented, nothing executed`;
  but `commit+merge` and `commit-only` both **stop at stage `commit` with exit 1** on the single-branch fixture,
  because that sequence has no `merge` step to run and the fixture driver treats the merge cursor as unset. The
  *transition* (which steps each value authorizes) and the terminal state are correct and guarded
  (`::test_strategy_value_transition_is_per_value_and_behavioural`); the residual is the fixture **executor**'s
  handling of a value whose sequence contains no merge, i.e. a test-harness limit, not a behaviour of the shipped
  reference. It does not touch any `final`-path criterion (SC-001's four models are all proven under
  `commit+merge+push`), and it is recorded here so the next reader does not discover it by running the probe.
- **R-16 (parent ownership of the receipt home) — measured this slice.** `scripts/python/record-retention.py:32`
  reads `RETENTION_REL = ".specify/memory/retention"`, so the parent is owned by the retention engine and the
  receipt directory `closeout/` is a sibling of its existing `receipts/` and `plans/`, creating no new top-level
  store (A-G1 unchanged). Evidence: `tasks.md` § Premises row "Receipt holding root".
- **R-17 (two `green-cross-phase`) — asserted, not zero.** See DoD-2; both are disclosed with their reasons in
  `tasks.md` § Green Partition.
- **R-18 (`baseline-missing`) — cleared.** T005 froze `coverage-baseline.txt` in slice 1 and the accountant now
  reports `status: ok`, `uncovered beyond baseline 0`.
- **R-19 (`blockedBy: Txxx` legend read as a dependency) — NOT-OURS, surfaced.** The format legend is not a
  dependency claim; the parser reads the code span as one.
- **R-20 (CHK011, "records without artifacts") — recorded reading.** A run that produces records but no artifact
  matches lifecycle C-5 fork 2's shape (merge and push still happen, the report says this close-out carried no
  records commit) and no separate branch is invented for it: FR-007's three forks stay three, and the
  records-only run reports under the fork it actually is. LOW because the gap is in the enumeration, not in
  the behaviour.
- **R-21 (CHK020, FR-028's location) — recorded reading.** The receipt home is settled by parent
  (R-16 above) rather than by a path written into FR-028; the requirements→tasks transfer stays as thin as it was
  and is not back-filled here.
- **R-22 (CHK028, A17 "no host-platform API") — recorded reading.** Enforced by construction:
  `closeout-executor.contract.md` C-1's fifth row asserts that no remote API is contacted. A reader checking FRs
  alone cannot find it; that is stated rather than repaired.
- **R-23 (CHK040, the STR-002 value grammar) — adopted declaration C-1's wording.** The close-out reads the
  `Closeout remotes` cell as "a comma-separated list of remote names, or an explicitly empty list", and reads a
  blank/absent cell as equivalent to an empty one per declaration C-4's one-outcome rule. `data-model.md` E-1's
  "empty or absent" is therefore the same claim, not a second one.
- **R-21b (the behavioural retry arm) — added this slice, limit recorded.** T041 asks that the T039/T040
  assertions go red when an automatic retry is injected. Measured with the driver's `attempt_retry` hook: both
  arms stayed **green** under the mutation, because a retry changes neither the remote's ref listing nor the
  failing stage — the assertion had no axis on which a mutation could show. The fix is an axis, not a weakened
  rule: `CloseoutOutcome.retries` is a reported field, and
  `::test_mutation_a_behavioural_retry_loop_reds_the_no_retry_assertions` asserts `retries == 0` on the landed
  driver and the mutated driver's non-zero reading. Second limit, also recorded: the hook sits on the push step, so
  the merge arm is unchanged by it (`retries == 0` under both runs) and its guarantee stays "stops at the merge,
  no push after it"; the test asserts that too, so a later change that makes the merge retryable reds it.
  Evidence: `test-evidence/mutations.txt` § R-21b and `test-evidence/T041-mutation-probe.py`.
- **R-38 (five compiled-face pins and one skill budget re-pinned) — discharged, with the containment kept.**
  The registry row 091 appends makes every compiled face carry one more wrapped step, which breaks any test that pins
  a face's step set or the token budget measured over that face. Five pins were re-derived from the same registry
  (`test_client_guard_sweep.py::test_c53…`, `test_review_code_composition.py::test_c16…`,
  `test_review_feedback_boundary.py::test_c55…` ×2, `test_decision_tension_contract.py::test_channel_only_add_allowed_delta_enumeration`)
  and one body was slimmed (`skills/external/humanize/SKILL.md`, `5023` → `4998` tokens against a `5000` ceiling) by
  deleting a line that restated the option set its own contract owner already carries. Every re-pin keeps the claim
  decidable: the step sets are still derived from the registry (never a hand-written list), and the analyze delta
  still reads its allowed close-out line **out of git** so a line moved outside `## Wrap-up`, a duplicate, or any
  fifth delta reds it. NONE of the pins was relaxed, skipped or emptied; each diff is a one-line expectation move
  with its reason written next to it.
- **R-36a/R-36b (pre-existing reds) — carried, measured, disclosed.** The sandbox-ordering trio is excluded from
  both sides of the comparison and its cause is named (R-36a below); the neighbourhood failures the entry baseline
  captured are recorded as baseline, never as this feature's regressions. Neither is repaired here: the first needs a
  probe-layer change, the second is a byte-state reading the sync already clears.

## Residuals

| ID | Severity | Fact | Disposition |
|---|---|---|---|
| R-36a | MEDIUM | **Three modules cannot pass in this sandbox, and this feature did not make them so**: `tests/unit/test_compile_embeds.py`, `tests/contract/test_engine_face_contract.py`, `tests/contract/test_compile_reconcile_guards.py`. Measured cause: their `_build_workspace` copies the live probe registry plus a fixed `_OWNER_COPIES` list (`feedback-step.md`, `docs-step.md`, the `create-team` SKILL, `confirmation-gates.md`) — **not** the behaviour owner `shared/workflow/artifact-commit-step.md` — so once any registry row names an unreachable owner the compile inside the sandbox exits 2 and the module reads an empty stdout (`JSONDecodeError` / empty stderr). Proven pre-existing by an A/B run at `HEAD` with and without this feature's changes (`git stash -u`, both 17 failing), i.e. the defect is order-dependent on registry content, not on 091's rows | **carried, disclosed** — excluded from both sides of the GATE-1 comparison so the comparison measures like for like; a framework-level repair (the sandbox should derive its owner copies from the registry) belongs to the probe layer, not to this feature. The production paths of all three checks pass on the same tree: `probe-utils.py --action compile-embeds --check` → `79 units, zero drift`, exit 0 |
| R-36b | MEDIUM | Four node ids in this feature's neighbourhood were **already red at implement entry** (present in `baseline-failed.txt`): `test_mirror_parity_suite.py::…git-workflow-block.md…`, `test_shipped_surface_client_neutrality.py::…`, `test_trigger_engine.py::test_c2_sync_mirrors_check_clean`, and one `test_fast_fail_discipline.py::test_i11…` | **cleared this run, not claimed** — three of the four are green in the final list purely because the tree is synced now (they are byte-state readings). `test_fast_fail_discipline.py::test_i11…` is still red on both sides. `test-evidence/final-failed.txt` is the reading; nothing here was repaired by hand |
| R-19 | LOW | driver-skill parser reads the format legend as a dependency token | NOT-OURS, surfaced in `framework_observations` |
| R-20 / R-21 / R-22 | LOW | requirements-text thinness (see § Rulings) | recorded readings, no text edit |
| R-37 | MEDIUM | the fixture **executor** stops at stage `commit` (exit 1) for a strategy value whose derived sequence contains no merge step (`commit+merge` / `commit-only` on a single-branch fixture), so a behavioural read of those two values is not available — only their transition and terminal state are | **carried, surfaced** — the transition is guarded per value and the shipped reference is unaffected; whoever next extends the fixture driver should either make the merge cursor a no-op when the sequence has no merge or narrow the probe's claim. Recorded, not silently absorbed |

## Not verified here (belongs to the review stage)

`/speckit.review` owns the quality verdict. This record states what was **measured**; it does not claim the
feature is ready for review, and it does not touch `code-review.md`.
