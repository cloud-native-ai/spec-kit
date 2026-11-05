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
| R-2 C-24 mirror byte parity | — | T031/T032 (US3) | CLOSED in part 6 — see § R-2 (row kept as the historical snapshot of this part) |
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

## R-4 — US2 template-side section (T019/T020), red captured 2026-11-05

Commands run **before** T022/T023 touched any artifact, from the repository root:

```text
$ python3 -m pytest tests/contract/test_instructions_section_propagation.py -q
FAILED tests/contract/test_instructions_section_propagation.py::test_c10_template_carries_the_section_and_its_runtime_pointer
FAILED tests/contract/test_instructions_section_propagation.py::test_c11_section_is_summary_plus_pointer_not_a_copy
FAILED tests/contract/test_instructions_section_propagation.py::test_c14_template_side_presence_survives_rendering
3 failed, 3 passed in 1.67s
EXIT=1

$ python3 -m pytest tests/contract/test_instructions_size_budget.py -q
13 passed in 6.46s
EXIT=0
```

Where each red comes from, and why it is the right one:

- C-10 / C-11 fail at `_section_body` → `AssertionError: no '## Self-Explanatory Structure
  (不言自明)' section on the surface under test` — the artifact is absent, not the assertion
  mis-written. The owner files themselves exist and are byte-identical, so C-11's precondition
  holds and the failure is attributable to the missing section alone.
- C-14 fails at its first line with the message it exists to produce: the template lost the
  heading. That is the template-side assertion firing, which is what the contract's mutation leg
  (M-3) must be able to do; it is not a live-file red.
- The C-14 anti-drift companion (`..._rendered_template_matches_the_generator_substitution_set`)
  and C-17 pass at red time **by design** — both guard inherited surfaces that this feature does
  not move. Their being green here is the control: the red is confined to the three assertions
  whose subject is the missing artifact.

Note on clause ordering (disclosed, not an anomaly): C-17's assertion is a real-tree measurement,
so it is green before and after T022/T023 — the new section adds bytes to the live file only at
T024. Its discriminating evidence is therefore the derived-value rule, not a red/green pair at
this part. A budget literal in the test would not have made it red either; it would have made it
green for the wrong reason.

## Pairs still open after part 4

| Pair | Red captured | Green expected at | Status |
|------|--------------|-------------------|--------|
| R-2 C-24 mirror byte parity | — | T031/T032 (US3) | CLOSED in part 6 — see § R-2 (row kept as the historical snapshot of this part) |
| R-3 C-31 glossary entry | — | T043 (US4) | NOT STARTED |
| C-21 instructions summary | declared red (part 2) | T024 (US2) | OPEN — green belongs to T024 |
| R-4 C-10/C-11/C-14 | this section | T024's reconcile / T027's M-3 | RED CAPTURED |

## Part 4 shape finding — the section's summary must be ONE sentence (disclosed repair)

The C-21 carrier (`test_self_explanatory_constitution.py`) removes **every line containing the
pointer path** before counting sentences. My first draft put summary sentences and the pointer on
the same physical line, so the whole paragraph was removed and C-21 failed with "the section
carries no summary at all". Measured, not guessed:

```text
body   = "\nCorrectness makes …. Full definitions …: `.specify/…-definitions.md` (do NOT restate …).\n"
pointer_lines = [that entire line]        # → summary became empty → C-21 red on a REAL defect
```

Repaired by giving the section the shape C-21 exists to enforce: **one summary sentence**, a blank
line, then the pointer on its own line. Two summary sentences on separate lines would also satisfy
C-21, but the earlier draft's *second* sentence was not a summary — it restated rules the owner
already owns, which is the very duplication C-20/C-21 exist to prevent. So the short body is the
correct shape, not a budget concession. Final section body is 1 summary sentence + 1 pointer line,
618 B.

This is an in-passing correction (one reading consistent with the contract's intent, local,
reversible), not a decision: disclosed here and in the part-4 checkpoint.

---

# Part 5 (T024-T028) — M-3 / M-4, and the C-21 pair

**Captured**: 2026-11-05 | **Base commit**: `5f267f22` | **part_scope**: `T024-T028`
**Scratch root**: `.specify/.tmp/082-part5/` (git-ignored, checked with `git check-ignore` before the
first write; removed after the run)

Both legs call the carrier's **own** functions (`carrier._section_body`, `carrier._render`,
`carrier._generator_substitutions`) and the **real** mirrored generator — neither is a paraphrase of the
assertion it is meant to break.

## M-3 — deleting the section from a COPY of the template

```console
$ python3 .specify/.tmp/082-part5/m34.py
MUTATION LEGS M-3 / M-4 — part 5 (T027)
==============================================================================

[M-3] delete the section from a COPY of the template
[PASS] M-3 mutation took effect (copy differs, heading gone)
        28930 -> 28311 bytes
[PASS] M-3 C-14 template-side presence turns False
        present=False
[PASS] M-3 C-10 section lookup turns red
        AssertionError: no '## Self-Explanatory Structure (不言自明)' section on the surface under test; t...
[PASS] M-3 rendered reconcile input lacks the heading
```

The C-10 leg re-uses `carrier._section_body` against the mutated text, so the leg exercises the actual
matcher rather than a re-typed assertion. The rendered-reconcile leg uses `carrier._render`, whose
placeholder set is itself pinned to the generator by `test_c14_rendered_template_matches_the_generator_substitution_set`.

## M-4 — the generator on a fixture with no template section

```console
[M-4] generator on a fixture whose template has NO section injects nothing
[PASS] M-4 generator exits 0
[PASS] M-4 zero injection of the absent section
        INJECTED list has 33 sections, none of them the subject
[PASS] M-4 live fixture did not gain the section
        live=28188 B
[PASS] M-4 counter-check: the reconcile DID run and DID inject other sections
        the same run injected the other template sections
[PASS] M-4 pre-existing content preserved
        custom section and overview both intact
[PASS] M-4 anti-vacuity: the same generator DOES inject it once the template carries it
        Injected missing template section(s): Documentation Map, Proacti...
[PASS] M-4 anti-vacuity: pre-existing content preserved when injecting

[anti-vacuity] the repository was never the subject
[PASS] real template still carries the heading
        present=True; 28930 bytes
[PASS] all four repository files byte-identical after the legs
        template=44ea5381d660 generator=e8c46c498a75
==============================================================================
VERDICT: PASS — M-3 turns C-14 and C-10 red on a copy; M-4 shows zero injection, with its
         anti-vacuity companion injecting on the same fixture; the repository is untouched
EXIT=0
```

### What the first two attempts measured, and why they were wrong

Disclosed rather than quietly fixed, because a mutation leg that passes for the wrong reason is the
defect this whole section exists to prevent. Two distinct mistakes were made and are recorded here:

1. **Attempt 1 — assertion wider than its subject.** The leg asserted "no `INJECTED` line at all". The
   fixture's live file carried none of the template's sections, so the generator legitimately injected
   the other 33 and the leg failed. The subject is **the section**, so the assertion was narrowed to
   "the absent section never appears in the INJECTED list", with a counter-check that the reconcile did
   run and did inject the others (otherwise the silence would prove nothing).
2. **Attempt 2 — a vacuous anti-vacuity.** The positive-control half reused the same live file after the
   first half had filled it in, so every template heading was already present and the generator became a
   byte-for-byte no-op: the second half "passed" without ever exercising an injection. Repaired by
   re-seeding the live file before **each** half, so the two halves differ in exactly one variable —
   whether the template carries the section. (The US2 carrier avoids the same trap the same way: its C-2
   fixture writes a live file that differs from its template.)

Both mistakes were found by the legs failing, not by review — the transcript order above is the order
they ran.

## The C-21 pair, closed

| half | where | verdict |
|------|-------|---------|
| RED | part 4, before the section had its final shape | "the section carries no summary at all" — a real defect: the pointer shared a line with the summary and the carrier strips pointer lines before counting |
| GREEN | this part, `-k c21` | `1 passed, 12 deselected` — `EXIT=0` |

Recorded honestly: C-21's subject is the **template** section, so the green arrived at T022 (after the
shape repair), not at T024's live reconcile. T024's contribution to the pair is that the section now
exists on the live surface as well — the pair is closed as "red then green on the same assertion across
parts", not as "the reconcile turned it green". The command and output are in
`notes/quickstart-run.md` § "T024 — the C-21 pairing".

## Pairs after part 5

| Pair | Red captured | Green expected at | Status |
|------|--------------|-------------------|--------|
| R-1 C-1 template carries the principle | yes (part 1) | T015 (US1) | CLOSED |
| C-21 instructions summary | yes (part 4) | T024 (US2) | **CLOSED** (this part) |
| R-4 C-10/C-11/C-14 | yes (part 4) | T024's reconcile / T027's M-3 | **CLOSED** — C-10/C-11/C-14 green at part 4 after T022, M-3 now proves the template side can go red |
| R-2 C-24 mirror byte parity | — | T031/T032 (US3) | CLOSED in part 6 — see § R-2 (row kept as the historical snapshot of this part) |
| R-3 C-31 glossary entry | — | T043 (US4) | NOT STARTED |

T051 owns the final consolidation. Nothing above is marked closed without the command that produced it.


## R-2 — the distribution chain, red then green (part 6, T029-T031)

R-2 was carried as `NOT STARTED` through five parts because its subject (the documents reaching a
client project) only became testable once T030 tracked the sources. It splits into three assertions
that each need their own red and green — a presence check that was never red proves as little as a
mirror `cmp` that was never run.

### R-2a — the mirror pair: RED was measured by the plan stage, GREEN by this part

The RED half is not this run's own transcript, and is not presented as such. research.md B-1 records
the stage-start reading of the same command:

```console
$ python3 scripts/python/sync-mirrors.py --check          # plan-stage B-1, before the mirrors existed
MISS  .specify/shared/definitions/self-explanatory-definitions.md
MISS  .specify/shared/guidelines/self-explanatory.md
MISS  .specify/shared/workflow/best-practice-optimization.md
EXIT=2
```

The GREEN half, this part:

```console
$ python3 scripts/python/sync-mirrors.py --check
ok    shared/ == .specify/shared/ (65 files)
EXIT=0
```

The pair is closed on the same three subjects: the three `MISS` lines B-1 recorded are exactly the
three `cmp rc=0` pairs of T032. The engine-level red was additionally re-created by this part (`printf
'x' >>` one mirror → `DIFF` + `EXIT=2` → `--write` → `sync … (1 files)` → `cmp rc=0`); that transcript
is in `notes/pre-change-measurements.md` § "T031 — mutation off the dispatcher's checklist".

### R-2b — C-26's distribution assertion: red proven by removal, green by construction

`test_self_explanatory_distribution.py` judges C-26 in two layers (the entry point's resource root;
`specify init` into a temp project). Both were made to go red on their own subject:

```console
$ mv shared/workflow/best-practice-optimization.md /tmp/<scratch>/hidden.md   # one document removed
$ python3 -m pytest tests/contract/test_self_explanatory_distribution.py -q
FAILED …::test_c26_specify_init_distributes_the_three_documents
FAILED …::test_c26_entry_point_resource_root_carries_the_three_documents
2 failed, 2 passed
EXIT=1

  AssertionError: the entry point's resource root does not carry:
    .specify/shared/workflow/best-practice-optimization.md
    layout: editable install (resource root == MODULE_DIR.parent.parent, the repo root)

$ mv /tmp/<scratch>/hidden.md shared/workflow/best-practice-optimization.md
$ sha256sum -c before.sha256 && diff -r shared /tmp/<scratch>/shared-copy
3 OK / diff empty → TREE-RESTORED-IDENTICAL
$ python3 -m pytest tests/contract/test_self_explanatory_distribution.py -q
4 passed
EXIT=0
```

The red names the one document that was removed, and the third assertion
(`test_c26_an_absent_document_fails_this_clause`) is an anti-vacuity companion: it asserts the
presence check reports exactly the missing entry, so a typo in the subject list or an always-true
file test cannot keep C-26 green on a broken tree.

Two things the red exposed, both repaired in passing and disclosed:

1. **A wrong premise in this part's own first attempt.** Layer 3 initially skipped (reporting
   `ANOMALY:`) when the editable install's resource root differed from `MODULE_DIR`. The measured
   layout is that an editable install leaves `specify_cli.__file__` under `<repo>/src/` while the
   build materialises `<repo>/src/specify_cli/{templates,shared,…}` as a sibling, so
   `get_resource_path()` returns `MODULE_DIR.parent.parent`. Skipping made the strongest layer
   unjudged on the very host that runs the suite; the two-layout branch replaces it, and a third
   value still fails rather than skips.
2. **`importlib` by-path loading does not work for this module.** `src/specify_cli/__init__.py`
   carries package-relative imports (`from . import _provenance`), so the by-path idiom used by the
   mirror-parity suite raises `ModuleNotFoundError` here. The module uses the `sys.path` + plain
   `import specify_cli` idiom that `test_upgrade_end_state.py` already established, and asserts the
   import really came from this working tree.

### R-2 status

| half | subject | RED | GREEN | verdict |
|------|---------|-----|-------|---------|
| R-2a | the three mirror pairs exist and are byte-identical | B-1's three `MISS` lines (`EXIT=2`) + this part's `DIFF` reconstruction | T031/T032 (`EXIT=0`, `cmp rc=0` ×3) | CLOSED |
| R-2b | C-26 — `specify init` distributes the three documents | removal transcript above (2 failed) | `4 passed` | CLOSED |

## Pairs after part 6

| Pair | Red captured | Green expected at | Status |
|------|--------------|-------------------|--------|
| R-1 C-1 template carries the principle | yes (part 1) | T015 (US1) | CLOSED |
| C-21 instructions summary | yes (part 4) | T024 (US2) | CLOSED |
| R-4 C-10/C-11/C-14 | yes (part 4) | T024 / T027 | CLOSED |
| R-2 C-24 mirror byte parity | B-1 (plan stage) + this part's DIFF | T031/T032 | **CLOSED** (this part) |
| R-2b C-26 distribution | this part's removal leg | T029 | **CLOSED** (this part) |
| R-3 C-31 glossary entry | — | T043 (US4) | NOT STARTED |

T051 owns the final consolidation. Nothing above is marked closed without the command that produced it.

---

# Part 7 (T034-T038) — M-5 / M-6, and the C-27 pair

**Captured**: 2026-11-05 | **Base commit**: `e5d0ae87` | **part_scope**: `T034-T038`
**Scratch root**: `.specify/.tmp/082-part7/` (git-ignored, `git check-ignore -q .specify/.tmp` checked
before the first write; removed after the run)

Both legs call the carriers' **own** functions — the mirror engine's `compare_pair` for M-5, the
distribution module's `docs_page_paths` / `unresolved_docs_page_paths` for M-6 — so neither is a
paraphrase of the assertion it is meant to break. Neither leg's subject is a repository file: both
mutate copies, and both assert the real file's digest afterwards.

## Verbatim transcript

```console
$ python3 .specify/.tmp/082-part7/m56.py
MUTATION LEGS M-5 / M-6 — part 7 (T037 / T038)
==============================================================================

[M-5] one byte flipped in a COPY of a mirror file, compared with the engine's compare_pair
      subject pair: shared/definitions/self-explanatory-definitions.md
[PASS] M-5 precondition: the copied pair is clean before mutation
        missing=[] differing=[] extra=[]
[PASS] M-5 mutation took effect (copy differs by exactly one byte)
        4508 bytes, byte 53: b'\n' -> b'\x0b'
[PASS] M-5 compare_pair reports DIFF for exactly that pair
        missing=[] differing=[PosixPath('definitions/self-explanatory-definitions.md')] extra=[]
[PASS] M-5 C-22's byte-identity assertion turns red, and the message names source->mirror
        AssertionError: mirror drift: .specify/shared/definitions/self-explanatory-definitions.md (engine compare_pair DIFF)
[PASS] M-5 the real mirror pair is byte-identical to its pre-leg digest
        sha256 source=1b12a9c5e098 mirror=1b12a9c5e098

[M-6] the STR-002 inline pointer deleted from a COPY of the docs page
      subject: docs/concepts/self-explanatory.md
[PASS] M-6 precondition: the page carries the STR-002 pointer
        shared/definitions/self-explanatory-definitions.md
[PASS] M-6 mutation took effect (the pointer is gone from the copy)
        1969 -> 1954 bytes
[PASS] M-6 extraction no longer yields the deleted path (extraction itself is unchanged)
        ['shared/definitions/removed-by-m6.md', 'shared/guidelines/self-explanatory.md', 'shared/workflow/best-practice-optimization.md']
[PASS] M-6 C-27's `assert not problems` turns red on the copy
        ['shared/definitions/removed-by-m6.md: MISSING in the source tree']
[PASS] M-6 the red names the path the mutation introduced
[PASS] M-6 anti-vacuity: the same carrier is green on the unmutated page
[PASS] M-6 the real docs page is byte-identical to its pre-leg digest
        sha256=04bb8c345c4e
[PASS] M-6 nothing under docs/concepts/ changed
        11 files

==============================================================================
VERDICT: PASS — M-5 turns C-22's byte-identity assertion red on a copy; M-6 turns C-27's
         resolution assertion red on a copy; both real subjects are byte-identical after
         the legs. scratch root: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/082-part7
EXIT=0
```

The M-6 leg ran against the **pre-T035** page text (1969 B; the page gained a two-line note during
T035), which is immaterial to the leg — it deletes a pointer and checks that resolution goes red — but
is recorded so the byte counts are reproducible rather than mysterious.

## M-5 (C-24) — what the leg establishes

| step | measurement |
|------|-------------|
| precondition | the copied pair is clean under `compare_pair` (no `MISS`, no `DIFF`, no extra) |
| mutation | exactly one byte changed (offset 53, `0x0a` → `0x0b`) in the *mirror* copy |
| detection | `compare_pair` returns `differing=[definitions/self-explanatory-definitions.md]` — the pair, not the file |
| red | the parity suite's own `assert src.read_bytes() == mirror.read_bytes()` raises, with a message naming `.specify/shared/definitions/self-explanatory-definitions.md`, i.e. the node id is directly re-runnable (C-24) |
| isolation | the real pair's sha256 is identical before and after the leg |

## M-6 (C-27) — what the leg establishes

| step | measurement |
|------|-------------|
| precondition | the page carries the `STR-002` inline path |
| mutation | `` `shared/definitions/self-explanatory-definitions.md` `` → `` `shared/definitions/removed-by-m6.md` `` in the *copy* |
| extraction unchanged | the copy still yields three paths; the deleted one is absent, so the leg breaks resolution, not extraction |
| red | `unresolved_docs_page_paths` returns `['shared/definitions/removed-by-m6.md: MISSING in the source tree']` — the guard's own `assert not problems` line fails, naming the mutation |
| anti-vacuity | the same carrier returns `[]` on the unmutated text |
| isolation | the real page's sha256 is unchanged, and all 11 files under `docs/concepts/` keep their digests |

## Pairs after part 7

| Pair | Red captured | Green expected at | Status |
|------|--------------|-------------------|--------|
| R-1 C-1 template carries the principle | yes (part 1) | T015 (US1) | CLOSED |
| C-21 instructions summary | yes (part 4) | T024 (US2) | CLOSED |
| R-4 C-10/C-11/C-14 | yes (part 4) | T024 / T027 | CLOSED |
| R-2 C-24 mirror byte parity | B-1 (plan stage) + part 6's DIFF | T031/T032 | CLOSED (part 6) |
| R-2b C-26 distribution | part 6's removal leg | T029 | CLOSED (part 6) |
| **R-5 C-27 docs links** | **M-6 (this part)** | **T034 (this part)** | **CLOSED (this part)** |
| R-3 C-31 glossary entry | **M-1 / M-2 (part 8)** | **T039/T040 (part 8)** | **CLOSED (part 8)** |
| R-6 C-22/C-24 mirror-enumeration | **M-4 / M-5 (part 8)** | **T042 (part 8)** | **CLOSED (part 8)** |

R-5 is new in this part: C-27 had no carrier before T034, so its red had to be produced by the mutation
leg rather than inherited from an earlier part. M-6 is that red, and the guard's green on the real page
is the same assertion run on the unmutated subject (also asserted inside the leg as its anti-vacuity
half).

T051 owns the final consolidation. Nothing above is marked closed without the command that produced it.

## Part 8 — R-3 (glossary entry) and R-6 (mirror enumeration), T039-T043

**Part scope**: `T039-T043` (implement part 8 of 10) | **Stage base**: `35a2948b` | **Runner**:
`.specify/.tmp/082-part8/red_legs.py` (git-ignored scratch; the transcript below is the durable copy)

The glossary entry already existed when this part opened (written by the engine during the plan
stage), so no assertion here could capture a "subject is absent" red the way R-1 did. The red is
therefore produced the way R-5's was: each assertion is run against a **mutated copy** of its subject
and must raise, while the same assertion run on the unmutated subject must pass. Copies only — the
real store's sha256 is compared before and after the whole run.

### Verbatim transcript

```console
$ python3 .specify/.tmp/082-part8/red_legs.py
[PASS] control: test_c29_entry_exists_with_origin_auto_and_status_proposed is green on the control
[PASS] control: test_c30_no_second_row_carries_the_retired_name_or_canonical_as_canonical is green on the control
[PASS] control: test_c32_meaning_cell_names_an_existing_repository_relative_path is green on the control
[PASS] M-1: test_c30_no_second_row_carries_the_retired_name_or_canonical_as_canonical is RED — a second row puts the retired name or the canonical string in the canonical column: [(161, '望文生义')] (the canonical row is entry index 160)
[PASS] M-2: test_c29_entry_exists_with_origin_auto_and_status_proposed is RED — expected exactly one entry whose canonical cell is '不言自明 (Self-explanatory)', found 2: [(160, '不言自明 (Self-explanatory)'), (161, '不言自明 (Self-explanatory)')]
[PASS] M-2: test_c30_no_second_row_carries_the_retired_name_or_canonical_as_canonical is RED — expected exactly one entry whose canonical cell is '不言自明 (Self-explanatory)', found 2: [(160, '不言自明 (Self-explanatory)'), (161, '不言自明 (Self-explanatory)')]
[PASS] M-3: test_c32_meaning_cell_names_an_existing_repository_relative_path is RED — the meaning cell does not name the concept owner 'shared/definitions/self-explanatory-definitions.md'; a reader landing on the glossary row would not reach the
[PASS] M-4: C-22 parameter-presence is RED with the engine enumeration emptied — the engine must own shared/definitions/self-explanatory-definitions.md->.specify/shared/definitions/self-explanatory-definitions.md through exactly one MIRROR_P
[PASS] M-5: C-22 byte-identity is RED when the mirrored copy differs — mirror drift: shared/workflow/best-practice-optimization.md->.specify/shared/workflow/best-practice-optimization.md (C-22 requires byte identity; C-24 requires
[PASS] isolation: real store sha256 unchanged (21482f6444ed815fdcbfb17ffaed417728225563c3d6f85173baea4c673c826a -> 21482f6444ed815fdcbfb17ffaed417728225563c3d6f85173baea4c673c826a)
VERDICT: PASS — 10 PASS / 0 FAIL
EXIT=0
```

### What each leg establishes

| Leg | Mutation (on a copy) | Red it produces |
|-----|----------------------|-----------------|
| M-1 | a new row with `望文生义` in the **canonical** column, inserted right after the canonical row | `test_c30_...` names the offending entry index and value — the row parse distinguishes the defect from the legitimate occurrence of the same string in the variants cell, which a substring search could not |
| M-2 | a new row duplicating the **canonical string** in the canonical column | `test_c29_...` reports "found 2" with both indices; `test_c30_...` reports the second row. Two assertions, one mutation, as C-29 and C-30 require |
| M-3 | the canonical row's owner path replaced with `shared/definitions/absent-by-construction.md` | `test_c32_...` fails on the named-path arm (the owner is unreachable), not on the "no path found" arm |
| M-4 | `MIRROR_PAIRS` emptied on the loaded engine module | the C-22 parameter-presence assertion fails with "found 0" owning pairs — i.e. with no enumeration a document has no mirror parameter at all |
| M-5 | both sides copied under one root, then the **mirror** copy's first byte changed | the byte-identity assertion fails naming `source->mirror`, which is the node-id form C-24 requires; the copy root carries exactly one document so the leg reaches the byte arm rather than the enumeration arm |
| isolation | — | the real store digest is unchanged after all legs |

### The engine's idempotent write (T043)

`--action detect-conflict` reported `{"conflict": true, "kind": "same-term-diff-meaning", "collidesWith": ["不言自明 (Self-explanatory)"]}`
— a collision **with itself**, because the term is already present. The engine's `action_add`
excludes the existing entry from its own conflict sweep (`[e for e in entries if e is not existing]`)
and replaces it in place, so the write is idempotent rather than refused:

```console
$ sha256sum .specify/memory/glossary.md          # before
21482f6444ed815fdcbfb17ffaed417728225563c3d6f85173baea4c673c826a  .specify/memory/glossary.md
$ python3 scripts/python/glossary-utils.py --action add --canonical "不言自明 (Self-explanatory)" \
      --variants "望文生义" --meaning "<summary; 真源 shared/definitions/self-explanatory-definitions.md>" \
      --origin auto --status proposed
{"written": true, "canonical": "不言自明 (Self-explanatory)", "count": 161}
EXIT=0
$ sha256sum .specify/memory/glossary.md          # after
21482f6444ed815fdcbfb17ffaed417728225563c3d6f85173baea4c673c826a  .specify/memory/glossary.md
$ git diff --stat .specify/memory/glossary.md    # empty
```

No hand edit, no second row: the file is byte-identical before and after, and the store still reports
161 entries.

### Pairs after part 8

| Pair | Red captured | Green expected at | Status |
|------|--------------|-------------------|--------|
| R-3 C-29/C-30/C-32 glossary entry | M-1 / M-2 / M-3 (this part) | T039 / T040 / T041 (this part) | CLOSED (this part) |
| R-6 C-22/C-24 mirror enumeration + byte identity | M-4 / M-5 (this part) | T042 (this part) | CLOSED (this part) |

