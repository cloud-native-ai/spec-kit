# Red-first evidence — 082-self-explanatory-integration

**Stage**: implement, `part_scope=T001-T006` | **Captured**: 2026-11-05 | **Base commit**: `94e8c30d`
**Working dir**: repository root (`/storage/project/cloud-native-ai/spec-kit`)

Each entry pairs a **RED** capture (the guard going red because the artifact is absent) with the
**GREEN** capture that later closes it. A guard whose red is missing is not proven effective, and a
green without a paired red is reported as such rather than counted.

## R-1 — T006 red: `test_self_explanatory_constitution.py::test_c1_template_carries_the_principle`

### RED (executed 2026-11-05, before the principle exists)

```console
$ python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q
F                                                                        [100%]
=================================== FAILURES ===================================
____________________ test_c1_template_carries_the_principle ____________________

    def test_c1_template_carries_the_principle() -> None:
        """C-1: the title is a MEMBER of the template's title set (set membership, never substring)."""
        titles = _template_titles(TEMPLATE.read_text(encoding="utf-8"))
>       assert PRINCIPLE_TITLE in titles, (
            f"templates/constitution-template.md is missing the principle titled {PRINCIPLE_TITLE!r}; "
            f"present titles: {sorted(titles)}"
        )
E       AssertionError: templates/constitution-template.md is missing the principle titled 'Self-Explanatory Structure (不言自明)'; present titles: ['Better-Harness Orientation', 'CLI & Text I/O Interface', 'Complete & Correct Options, or None', 'Continuous Integration & Quality Gates', 'Directory Governance (Named, Documented, Ignored When Temporary)', 'Documentation-First', 'Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest)', 'Feature-Centric Development', 'Grounded Naming', 'Integration & Contract Testing', 'Library-First Design', 'Non-Destructive Remediation', 'Observability, Versioning & Simplicity', 'One Source of Truth (Authority & Reference Discipline)', 'Single-Run Evidence (Capture Once, Consume Many)', 'Test-First Development', 'User-Facing Comprehension (No Jargon, With Context)']
E       assert 'Self-Explanatory Structure (不言自明)' in {'Better-Harness Orientation', ...}

tests/contract/test_self_explanatory_constitution.py:49: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_self_explanatory_constitution.py::test_c1_template_carries_the_principle
1 failed in 0.05s
EXIT=1
```

**Failure attribution** (the side that is wrong is decided before anything is changed): the
**subject** is missing — `templates/constitution-template.md` genuinely has 17 principles and none
of them is the new one. The assertion is not fragile: it extracts `### <numeral>. <title>` title
lines and asserts set membership, the shape the carrier file already uses, and it names the present
titles so the failure is self-diagnosing. T011 (US1) lands the artifact that closes this red; the
pair is closed in R-1-GREEN at T015.

### Not-the-red control (executed 2026-11-05)

The two suites `tasks.md` originally named for this capture are measured here so the record carries
the control beside the red — they are **green**, which is exactly why they cannot serve as this
feature's red signal:

```console
$ python3 -m pytest tests/contract/test_constitution_double_landing.py tests/contract/test_instructions_section_propagation.py -q
.....................                                                    [100%]
21 passed in 1.68s
EXIT=0
```

Neither file references `[[STR-001]]`, so no change this feature makes can turn them red-then-green
on the new principle's account. This is the analyze-stage finding U1-a, repaired in `tasks.md` at
`94e8c30d`; the repaired row (T006) creates this module instead, and the capture above is the
replacement red.

## Pending pairs (closed by later parts — recorded as NOT YET PROVEN)

| Pair | Red captured | Green expected at | Status in part 1 |
|------|--------------|-------------------|------------------|
| R-1 C-1 template carries the principle | yes (above) | T015 (US1) | **CLOSED** — see R-1-GREEN below |
| R-2 C-24 mirror byte parity | — | T031/T032 (US3) | NOT STARTED |
| R-3 C-31 glossary entry | — | T043 (US4) | NOT STARTED |

The closing pass is `tasks.md` T051, which owns the pairing cleanup. This file is the fixed landing
point that row consolidates; part 1 writes only the red it produced and never marks an unproven pair
as closed.

---

# Part 3 (T013-T018) — R-1 green captured, and the two mutation legs

**Captured**: 2026-11-05 | **Base commit**: `8daf6b65` | **part_scope**: `T013-T018`

## R-1-GREEN — the pair's green half (T015)

The red captured in part 1 (`test_c1_template_carries_the_principle`, EXIT=1, "principle not found")
is now paired with a green produced by the artifact that closed it. The command is the US1 subset
`tasks.md` T015 specifies — `-k 'not c21'` because C-21's subject (the instructions section) is a
US2 artifact and its red/green pairing belongs to T024/T051:

```console
$ python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q -k 'not c21'
............                                                             [100%]
12 passed, 1 deselected in 0.06s
EXIT=0
```

The twelve selected tests, by name (the pair's subject is the first):

```console
tests/contract/test_self_explanatory_constitution.py::test_c1_template_carries_the_principle
tests/contract/test_self_explanatory_constitution.py::test_c3_matcher_resolves_the_principle_under_an_unused_numeral
tests/contract/test_self_explanatory_constitution.py::test_c4_no_pinned_numeral_where_this_principle_lands
tests/contract/test_self_explanatory_constitution.py::test_c2_the_principle_block_satisfies_the_house_shape
tests/contract/test_self_explanatory_constitution.py::test_c6_all_five_content_obligations_are_each_carried_by_their_own_bullet
tests/contract/test_self_explanatory_constitution.py::test_c6_points_at_the_runtime_owner_and_states_reference_not_restate
tests/contract/test_self_explanatory_constitution.py::test_c6_framework_owner_path_appears_only_as_the_framework_owner
tests/contract/test_self_explanatory_constitution.py::test_c7_template_side_membership_of_every_watchlist_title
tests/contract/test_self_explanatory_constitution.py::test_c7_mutation_leg_m1_removing_the_block_breaks_membership
tests/contract/test_self_explanatory_constitution.py::test_c8_principle_block_has_zero_blocking_pattern_hits
tests/contract/test_self_explanatory_constitution.py::test_c20_no_owner_heading_is_copied_onto_a_projected_surface[constitution-template]
tests/contract/test_self_explanatory_constitution.py::test_c20_no_owner_heading_is_copied_onto_a_projected_surface[instructions-template]
```

Honest reading of the pair: the red and the green are **different populations**, not one assertion
flipping. The part-1 red was C-1 alone (the module was run before T011 landed the principle); the
green covers the twelve US1 assertions that the same artifact set now supports. That is what a
red-first capture across a multi-part phase looks like — the artifact that closes the red also
brings every sibling assertion green at once. It is recorded this way rather than as "the same test
went red then green", which would overstate what was measured.

## The mandate-side half of C-7 also closed (T013)

Before T013 the carrier's C-5/C-7 were red on the **count pin** (10 vs 11 entries) — measured and
recorded in part 2. After T013 the entry exists and after T016 the count matches:

```console
$ python3 -m pytest tests/contract/test_constitution_double_landing.py -q -k 'c6 or c7'
.....                                                                    [100%]
5 passed, 14 deselected in 0.05s
EXIT=0
```

The mandate entry carries, verified mechanically on the flattened entry body: the truth anchor
`.specify/shared/definitions/self-explanatory-definitions.md` → present; the
"referenced, not restated" clause → present; the "MUST NOT justify" no-machinery limit → present.

## T018 — mutation legs M-1 / M-2

Executed on copies in `mktemp -d` (`/tmp/p082-m12-*`, removed afterwards). The judgement functions are
the carriers' own, so the legs exercise the real matchers rather than a paraphrase of them.

```console
MUTATION LEGS M-1 / M-2
==============================================================================
[PASS] M-1 mutation took effect (copy differs from real file)
        21467 -> 19883 bytes
[PASS] M-1 C-7 template-side membership turns False
        title in carrier title set: False; in new module title set: False
[PASS] M-1 C-1 membership turns False
        title present: False
[PASS] M-1 anti-vacuity: real template carries the subject
        real file membership True
[PASS] M-2 mutation took effect (copy differs from real file)
        22197 -> 21096 bytes
[PASS] M-2 C-7 mandate-side membership turns False
        title in mandate name set: False
[PASS] M-2 C-5 count turns red (copy count != COMMAND_COUNT)
        copy=10 real=11 COMMAND_COUNT=11
[PASS] M-2 anti-vacuity: real skill carries the subject
        real mandate membership True; real count 11
[PASS] Both repository files are byte-identical after the legs
        constitution-template.md:0718cc7c5fde; SKILL.md:dec567fcddc9
==============================================================================
VERDICT: PASS — both legs make their clause go false and the repository is untouched
EXIT=0
```

Both legs therefore satisfy the contract's three requirements: the clause goes **false** under the
mutation, the anti-vacuity companion proves the real file carries the subject, and the repository
files are byte-identical afterwards (sha256 before and after).

## Pairs still open after this part

| Pair | Red captured | Green expected at | Status |
|------|--------------|-------------------|--------|
| R-2 C-24 mirror byte parity | — | T031/T032 (US3) | NOT STARTED |
| R-3 C-31 glossary entry | — | T043 (US4) | NOT STARTED |
| C-21 instructions summary | declared red (part 2) | T024 (US2) | OPEN — green belongs to T024 |
