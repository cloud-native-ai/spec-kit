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
| R-1 C-1 template carries the principle | yes (above) | T015 (US1) | OPEN — red only |
| R-2 C-24 mirror byte parity | — | T031/T032 (US3) | NOT STARTED |
| R-3 C-31 glossary entry | — | T043 (US4) | NOT STARTED |

The closing pass is `tasks.md` T051, which owns the pairing cleanup. This file is the fixed landing
point that row consolidates; part 1 writes only the red it produced and never marks an unproven pair
as closed.
