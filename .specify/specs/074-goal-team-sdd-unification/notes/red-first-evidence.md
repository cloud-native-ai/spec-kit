<!-- merged from 074a-authorized-routing (source: .specify/specs/074a-authorized-routing/notes/red-first-evidence.md) -->

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

<!-- merged from 074b-nested-governance (source: .specify/specs/074b-nested-governance/notes/red-first-evidence.md) -->

# Red-first evidence — slice 074b-nested-governance

Append-only evidence sink for this slice's red→green cycles. Each entry records the command, the real
output and the exit code. Nothing here is a paraphrase of a run: the blocks are pasted.

## E-1 · `tests/contract/test_nested_run_report.py` — RED (T036)

**Captured**: 2026-10-29T05:58Z, HEAD `241a6082b`, after the suite was written and before any edit of the
report contract.
**Red shape**: the mandatory section does not exist, so the cases fail as a *missing section*, not as a
contradictory assertion.

```text
$ python3 -m pytest -q tests/contract/test_nested_run_report.py
FFFFFFFFFFFFF.FF                                                         [100%]
=================================== FAILURES ===================================
____________ test_heading_literal_is_stated_verbatim_and_line_exact ____________

    def test_heading_literal_is_stated_verbatim_and_line_exact():
        text = _read(CREATE_TEAM)
        exact = [line for line in text.splitlines() if line.strip() == HEADING_LITERAL]
>       assert len(exact) == 1, (
            f"the report contract MUST state {HEADING_LITERAL!r} verbatim on its own line "
            f"exactly once (C-21); found {len(exact)} line-exact occurrences"
        )
E       AssertionError: the report contract MUST state '## Nested SDD Runs' verbatim on its own line exactly once (C-21); found 0 line-exact occurrences
E       assert 0 == 1
E        +  where 0 = len([])

tests/contract/test_nested_run_report.py:249: AssertionError
________ test_the_literal_lands_in_exactly_one_shipped_source_document _________

    def test_the_literal_lands_in_exactly_one_shipped_source_document():
        holders = _documents_carrying(HEADING_LITERAL)
>       assert holders == ["skills/internal/create-team/SKILL.md"], (
            "the heading literal MUST have exactly one definition point, the report contract "
            f"(C-21 / C-30); documents carrying it: {holders}"
        )
E       AssertionError: the heading literal MUST have exactly one definition point, the report contract (C-21 / C-30); documents carrying it: []
E       assert [] == ['skills/inte...eam/SKILL.md']
E         Right contains one more item: 'skills/internal/create-team/SKILL.md'

tests/contract/test_nested_run_report.py:267: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_nested_run_report.py::test_heading_literal_is_stated_verbatim_and_line_exact
FAILED tests/contract/test_nested_run_report.py::test_the_literal_lands_in_exactly_one_shipped_source_document
FAILED tests/contract/test_nested_run_report.py::test_the_section_is_appended_after_an_unchanged_section_list
FAILED tests/contract/test_nested_run_report.py::test_section_is_mandatory_for_every_run_in_both_pattern_families
FAILED tests/contract/test_nested_run_report.py::test_no_invocation_is_stated_explicitly_and_omission_is_a_violation
FAILED tests/contract/test_nested_run_report.py::test_per_invocation_row_carries_five_fields_and_the_closed_outcome_set
FAILED tests/contract/test_nested_run_report.py::test_blocked_and_failed_are_carried_through_never_dressed_as_success
FAILED tests/contract/test_nested_run_report.py::test_paths_are_carried_as_paths_and_bodies_are_never_inlined
FAILED tests/contract/test_nested_run_report.py::test_nested_section_is_a_peer_of_verification_not_a_replacement
FAILED tests/contract/test_nested_run_report.py::test_routing_verdict_is_a_reference_and_a_missing_record_is_never_rederived
FAILED tests/contract/test_nested_run_report.py::test_handoff_fields_are_read_by_reference_and_an_incomplete_handoff_is_not_success
FAILED tests/contract/test_nested_run_report.py::test_supervisor_is_the_sole_writer_and_a_nested_run_writes_no_tracked_artifact
FAILED tests/contract/test_nested_run_report.py::test_attribution_reuses_the_existing_ledger_field_and_adds_no_goal_field
FAILED tests/contract/test_nested_run_report.py::test_attribution_cardinality_is_exactly_one_with_a_target_and_none_without
FAILED tests/contract/test_nested_run_report.py::test_single_owner_audit_across_the_three_skill_documents
======================== 15 failed, 1 passed in 0.18s ========================
rc=1
```

**Reading of the one green case in the red run**: `test_attribution_is_observational_so_the_goal_field_set_is_unchanged`
executes the SC-008 instrument (`goal-utils.parse_goal` over the `074a` fixture Goal, before and after the
supervisor's ledger row). It is green at the pre-change commit because no change has been made to the Goal
yet — that is exactly the invariance it pins, and it stays green after the edit. It is executed rather than
asserted on purpose: a prose-only test of "the Goal field set is unchanged" would prove nothing.

## E-2 · `tests/contract/test_nested_run_report.py` — GREEN (T037–T039 landed)

**Captured**: 2026-10-29T06:05Z, after the report contract gained the mandatory section.

```text
$ python3 -m pytest -q tests/contract/test_nested_run_report.py
................                                                         [100%]
16 passed in 0.08s
rc=0
```

The same 16 cases that were red in E-1 are the ones now green; no case was removed, renamed or relaxed
between the two runs.

## Single-owner audit (T040)

```text
$ grep -n 'Nested SDD Runs' skills/internal/create-team/SKILL.md skills/internal/run-team/SKILL.md skills/internal/run-agent/SKILL.md
skills/internal/create-team/SKILL.md:63:## Nested SDD Runs
skills/internal/create-team/SKILL.md:76:### Nested SDD Runs section（必填段,本节为该段的唯一真源）
skills/internal/create-team/SKILL.md:78:每个 run 报告 MUST 在既有必填段之后**末尾追加**一个嵌套段,标题字面量逐字为 `## Nested SDD Runs`(不得改写、不得改变标题层级、不得并入其它段)。该段对**每次运行**强制 —— 有界 pattern(parallel / serial / iteration)与 continuous 一律适用,与该次运行是否真的发生过嵌套 SDD 调用无关。既有必填段的名称、次序与内容义务逐字不变;MUST NOT 省略该段,省略即判违约。
rc=0

$ for f in <the three skill documents>; do echo "$(grep -c 'Nested SDD Runs' $f) $f"; done
3 skills/internal/create-team/SKILL.md
0 skills/internal/run-team/SKILL.md
0 skills/internal/run-agent/SKILL.md

$ grep -n '报告契约' skills/internal/run-team/SKILL.md
66:执行结束后把带日期的运行报告写入 `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md`(**每次运行强制**,报告契约真源:create-team SKILL.md → Report;含 `## Verification` 节)。…
```

**Reading**: all three occurrences live in the one owner (`create-team/SKILL.md` § Report contract) — the
skeleton literal, the subsection heading that states the obligation, and the sentence naming the literal.
`run-team` keeps delegating at `:66` and gains no second statement; `run-agent` is untouched by this face.
Measured per **document**, which is the unit "one owner" is decidable in.

## E-3 · `tests/contract/test_nested_run_report.py` — GREEN (T041, US1 closed)

**Captured**: 2026-10-29T06:0Z, HEAD `f26eb59ac`, at the start of implement part 2, before any Phase 3 edit.
No case was added, renamed, relaxed or removed relative to E-1/E-2.

```text
$ python3 -m pytest -q tests/contract/test_nested_run_report.py
................                                                         [100%]
16 passed in 0.08s
rc=0
```

**Reading**: US1's acceptance surface is green at the part-2 base commit, so US2's edits can be judged
against a known-green neighbour rather than against a moving one.

## E-4 · `tests/contract/test_sdd_diffusion.py` — RED (T042)

**Captured**: 2026-10-29T06:2Z, HEAD `f26eb59ac`, after the suite was written and before any Phase 3 edit.
**Red shape**: the four diffusion surfaces are not landed yet, so the surface cases fail as *absent
statements/sections*, not as contradictory assertions.

```text
$ python3 -m pytest -q tests/contract/test_sdd_diffusion.py
FF.F.FFFFFF..F.                                                          [100%]
=================================== FAILURES ===================================
____ test_stage_bullet_keeps_the_three_values_and_gains_the_disambiguation _____

    def test_stage_bullet_keeps_the_three_values_and_gains_the_disambiguation():
        bullet = _stage_bullet()
        stated = re.findall(r"`([^`]+)`", bullet.split("(canonical names")[0])
>       assert tuple(stated) == TEAM_STAGE_VALUES, (...)
>       assert "SDD" in bullet and re.search(r"阶段名册|roster", bullet), (
            "the added text MUST state that this dimension is not the SDD stage roster (C-13)"
        )
E       AssertionError: the added text MUST state that this dimension is not the SDD stage roster (C-13)

______________________ test_no_added_surface_enumerates_the_sdd_stage_roster ______________________
E       in _added_texts -> hosting = _hosting_paragraph()
E       AssertionError: the authoring baseline must carry exactly one hosting-responsibility
        paragraph (C-17), found 0

=================== short test summary info ====================
FAILED tests/contract/test_sdd_diffusion.py::test_stage_bullet_keeps_the_three_values_and_gains_the_disambiguation
FAILED tests/contract/test_sdd_diffusion.py::test_no_added_surface_enumerates_the_sdd_stage_roster
FAILED tests/contract/test_sdd_diffusion.py::test_hosting_rule_states_the_three_responsibilities_and_the_together_reading
FAILED tests/contract/test_sdd_diffusion.py::test_hosting_rule_sits_immediately_after_the_existing_key_paragraph
FAILED tests/contract/test_sdd_diffusion.py::test_hosting_rule_points_at_the_key_set_owner_and_restates_no_domain
FAILED tests/contract/test_sdd_diffusion.py::test_instructions_carry_exactly_one_routing_pointer_section
FAILED tests/contract/test_sdd_diffusion.py::test_instructions_pointer_restates_no_owner_fact
FAILED tests/contract/test_sdd_diffusion.py::test_instructions_section_declares_and_respects_its_own_byte_ceiling
FAILED tests/contract/test_sdd_diffusion.py::test_trigger_gains_the_conjunction_sentence_inside_an_existing_section
FAILED tests/contract/test_sdd_diffusion.py::test_generated_instructions_carry_the_section_verbatim_and_follow_the_symlinks
10 failed, 5 passed in 0.38s
rc=1
```

**Reading of the five green cases in the red run** — each is an *invariance* pin, green before the edit
because nothing has moved yet, and red if this slice breaks its subject:

- `test_shipped_stage_executor_preset_declares_no_hosting_capability` — the shipped leaf already carries
  no `sdd-invocation` key; asserted against the artifact, not against a convention (C-15).
- `test_the_hosting_criterion_fails_in_both_directions` — the C-16 criterion is *executed* over
  synthetic definitions (declaration-only fails, statements-only fails); it does not depend on the
  authoring baseline carrying the rule yet.
- `test_trigger_section_set_stays_the_delivered_closed_set` — the trigger document already has exactly
  its delivered 10 sections; the pin exists to go red when a section is added.
- `test_trigger_edit_moves_no_gate` — the scanner already reports the pre-change total (27); the pin
  exists to go red when the sentence adds a gate-scannable declaration.
- `test_every_shared_string_citation_resolves_to_a_registry_row` — all `[[STR-NNN]]` citations in the
  slice already resolve; the pin exists to catch a new dangling citation.

One in-passing test-defect repair, disclosed: the first red run of this suite reported 11 failures
because `_shared_string_ids()` looked the registry section up by *exact* title, while
`requirements.md`'s heading carries a parenthetical suffix (`## Shared Strings *(optional, …)*`). The
lookup was replaced by `_section_starting()` (prefix match, one hit) — a structural read instead of a
spelling test. `notes/red-first-evidence.md` keeps both numbers: 11 failed / 4 passed before the
repair, 10 failed / 5 passed after it. No implementation face was touched to produce the difference.

## E-5 · `tests/contract/test_sdd_diffusion.py` — GREEN (T043–T047 landed, T048)

**Captured**: 2026-10-29T06:3Z, after the five edits and the regeneration. The same 15 cases that ran in
E-4 are the ones that run here; no case was added, renamed or relaxed, and the 10 that were red are
now green.

```text
$ python3 -m pytest -q tests/contract/test_sdd_diffusion.py
...............                                                          [100%]
15 passed in 0.31s
rc=0
```

**E3 · targeted-set-v1 (part 2)** — the 19 baseline files plus the two suites this slice owns, run
**once** (no second full suite in this part; the full-suite slot belongs to implement start / review
closure). Full capture: `test-evidence/implement-targeted-part2-run.txt`.

```text
$ bash scripts/bash/run-tests.sh --names-out test-evidence/implement-targeted-part2-failed.txt \
    <the 19 files of test-evidence/targeted-set-v1-baseline.txt> \
    tests/contract/test_nested_run_report.py tests/contract/test_sdd_diffusion.py
collected 321 items
======================== 1 failed, 320 passed in 32.54s ========================
# failed-name list written: …/implement-targeted-part2-failed.txt (1 entries)
rc=1

$ cat test-evidence/implement-targeted-part2-failed.txt
tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged

$ comm -13 <(sort test-evidence/implement-targeted-part1-failed.txt) \
           <(sort test-evidence/implement-targeted-part2-failed.txt)
                       # empty → zero NEW failing node ids
```

**Reading**: the single failure is the same pre-existing red node id recorded in
`test-evidence/targeted-set-v1-baseline.txt` (gate total 27 vs the frozen 23, four earlier features'
declarations, not this slice's to repair), and the name-level comparison is empty in the
new-failures direction. Collected count moved 290 → 321 exactly by the two suites this slice owns
(16 + 15 cases); no existing case disappeared.

**Two disclosures, both corrections repaired in passing** — neither changed a contract:

1. **Test-side lookup defect (E-4)**: `_shared_string_ids()` matched the registry heading exactly while
   it carries a parenthetical suffix; replaced by a prefix match. Affected only my own new suite and
   only its first red run (11 failed / 4 passed → 10 failed / 5 passed).
2. **Section position (T045)**: the routing section was first placed between `## Proactive Flow
   Trigger` and `## Fact, Correctness & Logic Checks (Input Sanity)`. Two delivered guards pin that
   exact adjacency (`tests/contract/test_proactive_trigger_section.py` C-3 / C-9 and
   `test_ask_record_repeat.py`), so the first placement turned them red. The section moved to the next
   free slot (after Input Sanity, before `## One Source Of Truth`); commit `e1ee11c35`. Both guards are
   green in the E3 run above.





### E-5b · supplementary targeted check — the template-reading suites (part 2)

**Why this run exists**: `templates/instructions-template.md` is read by ~28 contract suites, most of
them outside the 19-file targeted set. Part 1 already ran a supplementary set for the same reason
(`implement.jsonl` seq 3); part 2 does the same rather than trust that no neighbour reads the surface
it edits *on principle*, without verification.

**First supplementary run (before the two repairs below)**: `1189 collected / 1182 passed / 7 failed`.
Set-diff against `baseline-failed.txt` (`comm -13`) named **four** new failures:

```text
tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22
tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[skills/internal/create-team/SKILL.md->.specify/skills/internal/create-team/SKILL.md]
tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[skills/internal/create-team/references/conceptual-model.md->.specify/skills/internal/create-team/references/conceptual-model.md]
tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[skills/internal/run-agent/SKILL.md->.specify/skills/internal/run-agent/SKILL.md]
```

**Repair 1 — the section-count pin (disclosed, cross-feature)**. `test_a7_section_counts_…` pins the
template at exactly 29 top-level `## ` sections and the live file at 30; C-18 requires exactly one
additive `## ` section, so both counts move by one. The pin's own docstring documents the protocol
("Stale-pin update (2026-10-27): the Closed-Set Claims amendment adds one ambient section"), i.e. the
integer is a *counter of ambient sections*, and adding one is its recorded update path. Bumped
29 → 30 and 30 → 31 with a dated docstring line naming slice 074b. This is the only file this part
touches outside the delivery surface `feature-ref.md` § 2 declares, and it changes two integers plus
one comment line — no clause, no proposition, no scope.

**Repair 2 — the three drifted skill mirrors**. `skills/internal/{create-team/SKILL.md,
create-team/references/conceptual-model.md, run-agent/SKILL.md}` had stale `.specify/` projections
(the first is part 1's T037–T039 edit, which left the mirror for T053; the other two are part-2 edits).
Synced with `python3 scripts/python/sync-mirrors.py --write --only skills/internal` — the projection is
mechanical, one reading only (mirror := source). `sync-mirrors.py --check` is now clean on all six
pairs and `regen-command-copies.py --check` still reports `OK`.

**Second supplementary run (after both repairs)**: `1189 collected / 1186 passed / 3 failed`, and the
three remaining failures are all **pre-existing** members of the 21-name `baseline-failed.txt`
(`test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline`,
`test_token_efficiency_discipline.py::test_cd5_headings_only_in_discipline_doc`,
`test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target`). `comm -13` against the
baseline is **empty**. Capture: `test-evidence/implement-targeted-part2-supp-run.txt`, failing names
in `implement-targeted-part2-supp-failed.txt`, row: `implement.jsonl` seq 5.

## E-6 · `tests/contract/test_sdd_invocation_governance.py` — superset edit (T049, no red step by instruction)

**Why no red step**: `tasks.md` T049 places this row under the migration/regression exception — the
file guards behaviour `074a` already delivered (`sdd-route.py --action authorize`, whose absent-key
default is owned by `NEUTRAL_AGENT_METADATA_KEYS`), so there can be no red-first run: the behaviour
exists before the case does. The guard against a sham superset is the *pre-edit* run below plus the
rule that no existing case's proposition changes.

**Pre-edit run** (before any line of this edit, 2026-10-29):

```text
$ python3 -m pytest -q tests/contract/test_sdd_invocation_governance.py
.................                                                        [100%]
17 passed in 0.24s
rc=0
```

**Post-edit run** (same command, after the six new cases landed):

```text
$ python3 -m pytest -q tests/contract/test_sdd_invocation_governance.py
.......................                                                  [100%]
23 passed in 0.59s
rc=0
```

**Reading**: 23 = the 17 preserved cases + 6 new ones; `17 ⊂ 23` and all 17 keep their verdict, so the
edit is a superset in the direction C-1/C-2 require. The six added node ids:

```text
tests/contract/test_sdd_invocation_governance.py::test_c1_an_agent_definition_without_the_key_resolves_forbidden
tests/contract/test_sdd_invocation_governance.py::test_c1_a_seat_without_the_policy_entry_resolves_forbidden[block-seat_absent-absent-entry]
tests/contract/test_sdd_invocation_governance.py::test_c1_a_seat_without_the_policy_entry_resolves_forbidden[no-seats-seat_allowed-absent-map]
tests/contract/test_sdd_invocation_governance.py::test_c1_the_absent_recipient_cannot_receive_a_driver_naming_dispatch
tests/contract/test_sdd_invocation_governance.py::test_c2_an_absent_agent_key_changes_no_other_field_of_the_dispatch
tests/contract/test_sdd_invocation_governance.py::test_c2_an_absent_seat_key_changes_no_other_field_of_the_dispatch
```

**Non-vacuity of the C-2 cases** (measured, not assumed): the declared/absent pair differs by one
line of the same document at the same path, and the two records differ in exactly the declaring
source — `supplying.agent: declared → absent-key`, with `effective`, `failed_half` and `reason`
identical:

```text
diff fields: ['supplying']
supplying: {'agent': 'declared', 'seat': 'declared'} -> {'agent': 'absent-key', 'seat': 'declared'}
reason equal: True | failed_half: agent agent
effective: forbidden forbidden
```

Had any other field moved, the C-2 cases fail — which is the property they are written to hold.

## E-7 · `tests/contract/test_sdd_compat_containment.py` — RED (T051)

**Captured**: 2026-10-29, before the file existed. The red form for a not-yet-written suite is its
absence, so the capture is the failing lookup rather than a failing assertion:

```text
$ test -e tests/contract/test_sdd_compat_containment.py; echo "exists rc=$?"
exists rc=1

$ python3 -m pytest -q tests/contract/test_sdd_compat_containment.py
ERROR: file or directory not found: tests/contract/test_sdd_compat_containment.py
no tests ran in 0.01s
rc=4
```

**Reading**: rc=4 is pytest's "no such path", so no case of this suite could have run before it was
written — the red is the missing file, and the green below is therefore the first execution of every
case in it.

## E-8 · `tests/contract/test_sdd_compat_containment.py` — GREEN (T051 file landed, T052 run)

```text
$ python3 -m pytest -q tests/contract/test_sdd_compat_containment.py
...........                                                              [100%]
11 passed in 0.32s
rc=0
```

**T052's run** — the compatibility suite together with the file T049 extended, because the two files
together are what carry C-1…C-12:

```text
$ python3 -m pytest -q tests/contract/test_sdd_compat_containment.py tests/contract/test_sdd_invocation_governance.py
..................................                                       [100%]
34 passed in 0.85s
rc=0
```

**Non-vacuity of the six negative clauses** (measured, not assumed). Each clause is an *absence*, and
an absence assertion is worthless if its token set could never appear. Two checks, both executed:

1. The section reader is live — `_report_section()` returns `1612` characters of the actual
   `### Nested SDD Runs section` body (and the helper asserts a single heading and a non-empty body
   before any case uses it), so the absence checks are run against text, not against `""`.
2. Injecting the forbidden token into the extracted text flips the corresponding criterion:

```text
clean offenders: []
mutated 集成  : ['集成']
mutated 确认门: ['确认门']
C-8 on clean: []
C-8 mutated : ['Work Package']
C-9 U-token on clean: None
C-9 U-token mutated : <re.Match object; span=(1617, 1619), match='U3'>
C-12 target_ref on clean: True True
```

The tokens are also ordinary vocabulary elsewhere in the framework sources (`集成` in 18 files,
`确认门` in 17, `daemon` in 13, `scheduler` in 4, `自动上送` in 2), so their absence from this one
section is a property of the section rather than of an unreachable string list.

3. The C-10 gate case carries its own positive control: the scanner reports gates in
   `skills/internal/create-team/references/summary-mapping.md` and
   `shared/guidelines/task-complexity-rubric.md`, i.e. it does see these document families, while
   none of the slice's nine delivered paths is a gate source.

### E-9 · targeted-set-v1 (part 3) — one run for the whole part

```text
$ bash scripts/bash/run-tests.sh --names-out …/implement-targeted-part3-failed.txt \
    <the 19 files of test-evidence/targeted-set-v1-baseline.txt> \
    tests/contract/test_nested_run_report.py tests/contract/test_sdd_diffusion.py \
    tests/contract/test_sdd_compat_containment.py
======================== 1 failed, 337 passed in 34.13s ========================
# failed-name list written: …/implement-targeted-part3-failed.txt (1 entries)
rc=1                                       # wall 34.95 s

$ cat …/implement-targeted-part3-failed.txt
tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged

$ comm -13 <(sort …/implement-targeted-part2-failed.txt) <(sort …/implement-targeted-part3-failed.txt)
                                           # empty → zero NEW failing node ids in this part

$ comm -13 <(sort baseline-failed.txt) <(sort …/implement-targeted-part3-failed.txt)
                                           # empty → the one failure is a member of the 21-name
                                           #         full-suite baseline (gate total 27 vs its frozen 23,
                                           #         four gates predating this slice)
```

**Reading**: collected moved 321 → 338, exactly the 17 cases this part added (6 in the governance file,
11 in the new containment suite); nothing existing disappeared. The single failure is the pre-existing
gate-total red, unmoved and not claimed green. Capture: `test-evidence/implement-targeted-part3-run.txt`,
row `implement.jsonl` seq 6.
