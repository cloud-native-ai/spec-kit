# Red-first evidence — slice 074a-authorized-routing, implement stage

Per `tasks.md` line 12: one entry per test group, carrying the command, the real output and the
exit code. Nothing in this file is reconstructed from memory; every block was copied from a run in
this session (2026-10-29) — part 1 of 5 = tasks T001–T008 at `HEAD=71954e31a`, part 2 of 5 =
tasks T009–T016 starting from `HEAD=08258b795`.

The green evidence for each group is appended by the row that turns it green — T016 for
`test_sdd_authorization.py`, T021 for `test_sdd_routing_definitions.py` — so this file always ends
with the last state actually measured, never with an assumed one.

---

## T005 — `tests/contract/test_sdd_routing_definitions.py` (red)

Written after T004 landed the owner document's foundation (ownership declaration,
`## Hierarchy`, `## Direct modification`, `## Invocation kinds`) and **before** the routing body
(five input domains, verdict table, precedence, reason codes, golden table) exists. Red shape is the
one the task predicts: **sections missing**.

```console
$ python3 -m pytest -q tests/contract/test_sdd_routing_definitions.py
..FFFFF.......                                                           [100%]
E       AssertionError: F-1 declares its landing as '## Inputs', which the document does not contain — an ownership claim with no landing point is not decidable (sections present: ['Direct modification', 'Hierarchy', 'Invocation kinds'])
E       AssertionError: owner document has no '## Inputs' section; declared landings must resolve (sections present: ['Direct modification', 'Hierarchy', 'Invocation kinds'])
E       AssertionError: the owner document MUST state, as a rule, that the decision consumes none of: implementation medium, file extension, language, artifact count, author identity (C-18)
=========================== short test summary info ============================
FAILED tests/contract/test_sdd_routing_definitions.py::test_each_fact_has_a_resolvable_landing_section
FAILED tests/contract/test_sdd_routing_definitions.py::test_five_inputs_declare_closed_value_domains
FAILED tests/contract/test_sdd_routing_definitions.py::test_change_nature_domain_carries_definition_class
FAILED tests/contract/test_sdd_routing_definitions.py::test_complexity_tier_domain_cites_the_rubric_owner
FAILED tests/contract/test_sdd_routing_definitions.py::test_forbidden_dimensions_are_stated_as_a_rule
5 failed, 9 passed in 0.09s
# RC=1
```

**Reading of the red**: the nine passing cases are the foundation this part delivers (ownership
declaration, hierarchy chain + boundary, direct-modification definition, the four invocation kinds,
shared-string citation resolution). The five failing cases are exactly the facts whose content is
task T017's (`§ Inputs`, the `definition-class` value, the tier-by-reference rule, the forbidden-input
rule) plus the landing-resolution check that consumes them. No case fails for any other reason
(full log: `red-t005.txt`).

## T007 — `tests/contract/test_sdd_authorization.py` (red)

Written after T006 landed the fixture and **before** `scripts/python/sdd-route.py` exists. The module
carries an autouse guard so no `rc == 2` assertion can pass while the engine is missing —
`python3 <missing file>` also exits 2, which is the classic false green for an exit-alphabet test.

```console
$ python3 -m pytest -q tests/contract/test_sdd_authorization.py
EEEEEEEEEEE                                                              [100%]
E       AssertionError: --action authorize engine is missing: /storage/project/cloud-native-ai/spec-kit/scripts/python/sdd-route.py (delivered by task T011)
E       assert False
E        +  where False = is_file()
E        +    where is_file = PosixPath('/storage/project/cloud-native-ai/spec-kit/scripts/python/sdd-route.py').is_file
=========================== short test summary info ============================
ERROR tests/contract/test_sdd_authorization.py::test_both_halves_allowed_resolves_allowed
ERROR tests/contract/test_sdd_authorization.py::test_seat_forbidden_names_the_seat_half
ERROR tests/contract/test_sdd_authorization.py::test_agent_key_absent_names_the_agent_half
ERROR tests/contract/test_sdd_authorization.py::test_both_halves_failing_names_both
ERROR tests/contract/test_sdd_authorization.py::test_absent_seats_map_defaults_to_forbidden
ERROR tests/contract/test_sdd_authorization.py::test_absent_seat_entry_defaults_to_forbidden
ERROR tests/contract/test_sdd_authorization.py::test_flow_style_seats_map_is_refused_with_the_seat_named
ERROR tests/contract/test_sdd_authorization.py::test_dangling_seat_entry_is_refused_with_the_seat_named
ERROR tests/contract/test_sdd_authorization.py::test_payload_with_only_the_seat_is_refused
ERROR tests/contract/test_sdd_authorization.py::test_refusal_record_carries_two_source_paths_and_the_seat_slug
ERROR tests/contract/test_sdd_authorization.py::test_authorize_writes_no_file
11 errors in 0.09s
# RC=1
```

**Reading of the red**: all eleven cases are blocked by the single missing subject (the engine's
`--action authorize`), which is task T011's deliverable in the next part. The red is *absence*, not
a contradictory assertion: the record shape the cases assert (`agent_capability`, `seat_policy`,
`effective`, `verdict`, `reason`, `failed_half`, `team_slug`, `seat_slug`, `sources`) is the
authorization-probe record contracted by C-8 / C-14, and T011 implements to it
(full log: `red-t007.txt`).

## T006 — fixture smoke check (not a test row)

`tests/fixtures/nested_sdd.py` is a builder, so its verification is a build, not a pytest case. Real
output of a build under a disposable root:

```console
$ PYTHONPATH=tests python3 -c "import tempfile, pathlib; from fixtures.nested_sdd import build; ..."
 file: .specify/agents/execution/20261029T000000Z-routing-verdict-d1.md
 file: .specify/agents/instances/seat-allowed.agent.md
 file: .specify/agents/instances/seat-forbidden.agent.md
 file: .specify/goal/fixture-goal/goal.md
 file: .specify/teams/fixture-team/team.md
```

The five files are the four surfaces the slice reads (seat policy map, two agent definitions, one
Goal with one `open` Target) plus the pre-recorded routing verdict that keeps US1 independent of
US2. Four `seats:` variants are reachable (`block` / `flow` / `dangling` / `no-seats`) because a
malformed-input guard that can only be driven in one direction proves nothing.

## T009 / T010 — authoring-surface checks (not test rows)

Both rows edit prose surfaces (the `run-agent` authoring baseline and the `team.md` schema), so their
verification is a content read, not a pytest case; the executable halves of the same facts are pinned
by `test_sdd_authorization.py` (resolution) and `test_sdd_routing_definitions.py` (single landing
place). Real output (2026-10-29, part 2):

```console
$ grep -c 'sdd-invocation' skills/internal/run-agent/SKILL.md \
      skills/internal/create-team/references/create-mode.md
skills/internal/run-agent/SKILL.md:2
skills/internal/create-team/references/create-mode.md:1

$ grep -n 'sdd-invocation.*\(allowed\|forbidden\)' skills/internal/run-agent/SKILL.md \
      skills/internal/create-team/references/create-mode.md
(no output)
# RC=1 — neither surface restates the closed value set; both point at the key-set owner.

$ sed -n '/^seats:/,/^members:/p' skills/internal/create-team/references/create-mode.md
seats:                         # optional (074a) — per-seat SDD invocation policy; block map ONLY
  <seat-slug>:                 #   keyed by seat slug; the slug MUST resolve to a roster member
    sdd-invocation: <value>    #   the same key the agent definition carries; value set and
                               #   absent-entry default are owned by NEUTRAL_AGENT_METADATA_KEYS
                               #   (src/specify_cli/__init__.py) — cited, never restated here
members:

$ python3 -m pytest -q tests/contract/test_neutral_vocabulary_scan.py \
      tests/contract/test_team_command_routing.py tests/contract/test_neutral_metadata_schema.py
..................................................................       [100%]
66 passed in 0.58s
# RC=0
```

**Reading**: the pointer discipline holds in both directions — the two authoring surfaces name the
new key (so an authored instance can declare it and `validate_agent_metadata` can reject a value
outside its closed set) while quoting none of the owner's values; the three suites that read those
surfaces stay green.


## T012 — `tests/contract/test_nested_sdd_invocation.py` (red)

Written after T011 landed the engine and **before** `sdd-loop-driver/SKILL.md` gains its
invoked-from-team entry and `references/nested-invocation.md` exists. Red shape = sections missing
(the documents the cases read do not exist yet); full log: `red-t012.txt`.

```console
$ python3 -m pytest -q tests/contract/test_nested_sdd_invocation.py
FFFFFFFFFFFFFFFFFFFFFFF                                                  [100%]
E       AssertionError: skills/external/sdd-loop-driver/SKILL.md must carry exactly one 'Invoked-from-Team Entry' section, found []
E       AssertionError: missing document: skills/external/sdd-loop-driver/references/nested-invocation.md
FAILED tests/contract/test_nested_sdd_invocation.py::test_entry_form_section_exists_as_an_additive_subsection
FAILED tests/contract/test_nested_sdd_invocation.py::test_entry_form_accepts_exactly_the_six_facts
FAILED tests/contract/test_nested_sdd_invocation.py::test_entry_validation_table_covers_the_closed_condition_set
FAILED tests/contract/test_nested_sdd_invocation.py::test_no_instruction_issues_a_merge_or_push
FAILED tests/contract/test_nested_sdd_invocation.py::test_nested_run_reaches_review_zero_merge_zero_push
FAILED tests/contract/test_nested_sdd_invocation.py::test_no_second_registry_ledger_spine_or_queue
FAILED tests/contract/test_nested_sdd_invocation.py::test_artifact_and_evidence_paths_are_referenceable
23 failed in 0.38s
# RC=1
```

**Reading of the red**: every one of the 23 cases fails on absence — no case fails for a
contradictory assertion, and none passes vacuously. Two cases needed their own anti-vacuity guard
to get there: the merge/push scan now requires both prohibitions to be **stated** (a scan that can
only be empty would pass on a document that never forbids merging), and the handoff completeness
test derives its required field set from the document's own schema table, so an absent document is
a failure rather than an empty requirement.

## T011 / T016 — `tests/contract/test_sdd_authorization.py` (green) and `test_nested_sdd_invocation.py` (green)

T011 landed the engine action the T007 red was blocked on; T013–T015 landed the two driver
surfaces the T012 red was blocked on. The two modules now run together:

```console
$ python3 -m pytest -q tests/contract/test_sdd_authorization.py tests/contract/test_nested_sdd_invocation.py
..................................                                       [100%]
34 passed in 0.49s
# RC=0
```

Full log: `green-t016.txt`. The green is the *same* case set that was red, not a reduced one: 11
authorization cases (T007) + 23 nested-invocation cases (T012), with the two anti-vacuity guards
T012 added still in place (the merge/push scan requires both prohibitions to be stated, and the
handoff completeness test derives its required field set from the document's own schema table).

A per-seat walk-through of the same engine against the fixture — the allowed seat, the forbidden
seat, and the malformed `seats:` map — is recorded with its real output in `quickstart-run.md`
§ S4 / § S5 (full log: `green-t016-demo.txt`).

---

Part 3 of 5 (tasks T017–T021), 2026-10-29, starting from `HEAD=186d6ce9b`.

## T018 — `tests/contract/test_sdd_routing_engine.py` (red)

Written after T017 landed the routing body in the owner document (five input domains, verdict
table, precedence, conflict set, reason codes) and **before** `scripts/python/sdd-route.py` has the
`route` / `golden` actions. Red shape is the one the task predicts: **the two actions do not exist**.

```console
$ python3 -m pytest -q tests/contract/test_sdd_routing_engine.py
EEEEEEEEEEEEEEEEEEEEE                                                    [100%]
E       AssertionError: --action route / golden missing from
E       /storage/project/cloud-native-ai/spec-kit/scripts/python/sdd-route.py (delivered by task
E       T019); the parser offered: "usage: sdd-route.py [-h] --action {authorize} ...\nsdd-route.py:
E       error: argument --action: invalid choice: '__absent-action__' (choose from 'authorize')"
...
ERROR tests/contract/test_sdd_routing_engine.py::test_route_is_deterministic
ERROR tests/contract/test_sdd_routing_engine.py::test_route_feature_scale_returns_sdd
... (21 errors, one per case)
21 errors in 0.82s
# RC=1
```

**Reading of the red**: all 21 cases fail on absence through an autouse guard that reads the
parser's own invalid-choice diagnostic. That guard is the anti-false-green device for this module:
without it, `python3 <engine> --action route` exits `2` for a *missing action* exactly as it does
for a *malformed input*, so every `rc == 2` assertion would pass while `rc == 0` behaviour was never
exercised. No case fails on a contradictory assertion and none passes vacuously (full log:
`red-t018.txt`).

## T017 / T021 — `tests/contract/test_sdd_routing_definitions.py` (red → green)

The T005 red (5 failed / 9 passed, § T005 above) turns green at T017, which landed § Inputs,
§ Definition-class default, § Verdict table, § Precedence, § Conflict set, § Reason codes,
§ User override, § Per-duty application and § Verdict record in the owner document:

```console
$ python3 -m pytest -q tests/contract/test_sdd_routing_definitions.py
..............                                                           [100%]
14 passed in 0.10s
# RC=0
```

Full log: `green-t017.txt`. The five cases that were red at T005 are the same five that pass here —
the landing-resolution check, the five-input domain table, the `definition-class` value, the
tier-by-reference rule and the forbidden-input rule — so the green is the same case set, not a
reduced one. The US2 close-out run (both modules together) is appended from T021's measurement.

## T019 / T021 — `tests/contract/test_sdd_routing_engine.py` (green) and the US2 close-out

T019 landed `--action route` and `--action golden` in the same engine, reading the four facts out of
the owner document at run time; T020 added the owner's § Golden case table (14 rows, the seven
required faces). The two routing modules now run together:

```console
$ python3 -m pytest -q tests/contract/test_sdd_routing_definitions.py tests/contract/test_sdd_routing_engine.py
...................................                                      [100%]
35 passed in 1.67s
# RC=0
```

Full log: `green-t021.txt`. The green is the same case set that was red, not a reduced one: 14
owner-document cases (T005's 5 red + 9 that were already green) and 21 engine cases (T018's red).
Five of the 21 stayed red between the T019 commit and the T020 commit for the predicted reason — the
golden action had no table to judge yet — and turned green when T020 landed the rows; no case was
weakened, deleted or skipped to get there.

Two anchored properties deserve their own lines, because they are the ones a plausible implementation
would fail:

- **The four facts are read, not copied.** Three probes mutate a temp *copy* of the owner document
  and require the engine to follow: a renamed reason code (`sdd-capability-or-contract-change` →
  `capability-change-renamed`) changes the reported code; a reversed precedence line flips the same
  inputs from `adjudicate` to `sdd`; narrowing the reversibility domain turns the previously direct
  case into `adjudicate / adjudicate-ambiguous-value`. A fourth probe scans the engine source and
  requires that no reason code, no verdict literal, no domain value and no domain/condition sequence
  appears in it.
- **No clock.** `recorded_at` is null unless the caller passes `--recorded-at`, because a timestamp
  read inside the engine would break the byte-identical property C-24 requires. The golden action
  reads no clock at all, so its two runs are byte-identical (`notes/golden-run1.json` /
  `golden-run2.json`, same sha256 `7ad8419e…`).

The golden table's own evidence — two byte-identical `--action golden` runs plus the row-by-row
judgement — is recorded in `quickstart-run.md` § S1 / § S2 / § S3 (the scenario sections T021 asks
for), with the raw payloads at `golden-run1.json`, `golden-run2.json` and `golden-rows.txt`.

## Regression check for this part

The slice's fixed targeted set (13 contract files, the sufficiency statement in
`test-evidence/targeted-set-v1-baseline.txt`) was re-run once for this part:

```console
$ bash scripts/bash/run-tests.sh --names-out notes/targeted-set-v1-failed.txt <the 13 files>
============================= 191 passed in 22.63s =============================
# failed-name list written: notes/targeted-set-v1-failed.txt (0 entries)
# RC=0
```

Name-level identical to the implement-start re-capture (191 passed, 0 failed names), so this part
introduces no new failure in the slice's non-regression set. No second full-suite run was made: the
E2 baseline slot was consumed at implement start (`test-evidence/implement.jsonl` seq 1).

---

# Part 4 of 5 — tasks T022–T025 (US3, started from `HEAD=0dbe8897b`)

## T022 — `tests/contract/test_sdd_invocation_governance.py` (red)

Written after US1/US2 closed and **before** the owner site's amendment (the narrowing, the depth-2
chain, the virtual prohibition, the cap and the refusal record) and before the probe is wired to the
engine. The file decides each clause on the surface that carries it: the owner site
(`shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation), the probe
(`skills/internal/run-agent/SKILL.md`, anti-nesting paragraph), and the executable half
(`scripts/python/sdd-route.py --action authorize`).

```console
$ python3 -m pytest -q tests/contract/test_sdd_invocation_governance.py
F.FFFFFFFFF....F.                                                        [100%]
=========================== short test summary info ============================
FAILED tests/contract/test_sdd_invocation_governance.py::test_c9_the_predicate_narrows_to_exactly_three_conditions
FAILED tests/contract/test_sdd_invocation_governance.py::test_c9_the_exclusivity_sentence_is_replaced_by_the_predicate
FAILED tests/contract/test_sdd_invocation_governance.py::test_c9_no_second_copy_of_the_prohibition_set
FAILED tests/contract/test_sdd_invocation_governance.py::test_c10_the_probe_calls_the_engine_and_fails_closed
FAILED tests/contract/test_sdd_invocation_governance.py::test_c11_the_permitted_chain_is_depth_two_with_its_three_prohibitions
FAILED tests/contract/test_sdd_invocation_governance.py::test_c12_virtual_mode_must_not_host_a_run
FAILED tests/contract/test_sdd_invocation_governance.py::test_c13_the_per_member_cap_is_hard_and_cites_the_existing_line_mechanism
FAILED tests/contract/test_sdd_invocation_governance.py::test_c14_a_refusal_record_names_the_condition_and_the_resolved_values
FAILED tests/contract/test_sdd_invocation_governance.py::test_c15_stage_executors_and_unqualified_prompts_are_blocked_before_dispatch
FAILED tests/contract/test_sdd_invocation_governance.py::test_c16_no_confirmation_gate_no_scheduler_no_second_registry
FAILED tests/contract/test_sdd_invocation_governance.py::test_the_four_dispatch_forms_each_carry_their_rule
11 failed, 6 passed in 0.24s
# RC=1
```

**Reading of the red**: the eleven failures are the eleven *declaration* cases — every one fails as
a **missing statement** on the surface that owns it (`'no confirmation gate' in gov` → the C-16
sentence does not exist yet; `dispatch form 'prompt-names-a-driver' … does not name 'failed
condition'` → the probe still restates the obligation in prose). No case fails as a contradictory
assertion, and no case fails for a reason outside US3's scope. The six passes are the two
behavioural groups (the allowed form, and the three refusal cases naming `seat` / `agent` / `both`)
plus the two containment guards (`test_c9_the_original_prohibition_survives_word_for_word`,
`test_the_pre_existing_probe_terms_still_hold`): they consume surfaces US1/us already landed, and
they are here so that the narrowing cannot pass by disturbing them. Full log: `red-t022.txt`.

## T023 — owner site amended + probe wired to the engine (partial green)

T023 replaced the unqualified "loop depth is always 1" sentence at `subagent-definitions.md`
§ Dispatch-Time Governance Obligation with the three-condition predicate (keeping the three original
prohibition clauses word for word), and rewrote the `run-agent/SKILL.md` anti-nesting paragraph so
the pre-dispatch probe calls `scripts/python/sdd-route.py --action authorize` and fails closed. The
same module re-run at that commit (`8b0c3c672`) — summary lines only, the full log of the end state
is `green-t025.txt`:

```console
$ python3 -m pytest -q tests/contract/test_sdd_invocation_governance.py
FAILED tests/contract/test_sdd_invocation_governance.py::test_c9_no_second_copy_of_the_prohibition_set
FAILED tests/contract/test_sdd_invocation_governance.py::test_c11_the_permitted_chain_is_depth_two_with_its_three_prohibitions
FAILED tests/contract/test_sdd_invocation_governance.py::test_c12_virtual_mode_must_not_host_a_run
FAILED tests/contract/test_sdd_invocation_governance.py::test_c13_the_per_member_cap_is_hard_and_cites_the_existing_line_mechanism
FAILED tests/contract/test_sdd_invocation_governance.py::test_c14_a_refusal_record_names_the_condition_and_the_resolved_values
FAILED tests/contract/test_sdd_invocation_governance.py::test_c15_stage_executors_and_unqualified_prompts_are_blocked_before_dispatch
FAILED tests/contract/test_sdd_invocation_governance.py::test_c16_no_confirmation_gate_no_scheduler_no_second_registry
FAILED tests/contract/test_sdd_invocation_governance.py::test_the_four_dispatch_forms_each_carry_their_rule
8 failed, 9 passed in 0.24s
# RC=1
```

The three cases T023 claims went green here: `test_c9_the_predicate_narrows_to_exactly_three_conditions`,
`test_c9_the_exclusivity_sentence_is_replaced_by_the_predicate`, and
`test_c10_the_probe_calls_the_engine_and_fails_closed` — 9 passed = those three + the 6 that were
already green at T022. The 8 still red are exactly the clauses T024 owns (C-11…C-16), each failing
as a missing statement.

## Correction disclosed — one pre-existing paragraph restored between T023 and T024

Splitting T023 and T024 into two commits over one file cost one paragraph: the pre-existing sentence
"*The obligation binds all three execution modes (native / virtual / external) equally … so the
wrapper stays generic and unchanged*" was cut together with T024's block when the block was staged
out of the T023 commit, so the T023 commit (`8b0c3c672`) is missing it and the T024 commit
(`cfa925c1a`) restores it **verbatim**:

```console
$ git show 8b0c3c672:shared/definitions/subagent-definitions.md | grep -c "binds all three execution modes"
0
$ git show cfa925c1a:shared/definitions/subagent-definitions.md | grep -c "binds all three execution modes"
1
```

Verified byte-identical to the pre-slice text (`git show 0dbe8897b:…` compared by string equality),
so the end state of the part carries no unintended deletion — the defect lived in the intermediate
commit only, and the file's final content is what both the tests and the contract read.

## T024 / T025 — US3 green and its evidence

T024 declared the depth-2 chain and its three prohibitions, the virtual-mode exclusion, the
one-run-per-member hard cap, the refusal record's field set and the no-new-machinery statement on the
same owner site. The module is green over the same 17 cases that were red:

```console
$ python3 -m pytest -q tests/contract/test_sdd_invocation_governance.py
.................                                                        [100%]
17 passed in 0.24s
# RC=0
```

Full log: `green-t025.txt`. No case was weakened, renamed or skipped between the red run and this one:
the 17 node ids are identical in both logs (11 failed → 17 passed through the 8-case intermediate
above).

The pre-existing anti-nesting cases were re-run in the same part at name level — see the regression
check below; the governance record itself (the four forms, the live refusal payloads, the declared
leaf/virtual refusals and the structure face) is in `quickstart-run.md` § Governance.

## Regression check for this part

The slice's fixed targeted set (the 13 contract files owned by
`test-evidence/targeted-set-v1-baseline.txt`) was re-run once for this part:

```console
$ bash scripts/bash/run-tests.sh --names-out notes/targeted-set-v1-failed.txt <the 13 files>
============================= 191 passed in 21.62s =============================
# failed-name list written: notes/targeted-set-v1-failed.txt (0 entries)
# RC=0
```

Name-level identical to the implement-start re-capture (191 passed, 0 failed names; the names-out
file is byte-identical — `git diff` on it is empty), so this part introduces no new failure in the
slice's non-regression set, and the three pre-existing anti-nesting assertions
(`test_agent_dispatch_mechanism.py` C-6 / C-20, `test_sdd_loop_driver_skill.py` C-20) keep their
verdict. Full log: `green-t025-targeted.txt`. No second full-suite run was made: the E2 baseline slot
was consumed at implement start (`test-evidence/implement.jsonl` seq 1).
