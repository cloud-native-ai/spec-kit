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
