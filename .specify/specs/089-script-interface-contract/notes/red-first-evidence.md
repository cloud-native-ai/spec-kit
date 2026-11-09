# Red-first evidence — Feature 089 (implement stage, package 1 = T001–T011)

**Owner of this file**: the implement stage's red-first rows of this feature. `tasks.md` § Tests says
"MANDATORY. Red-first evidence lands in `notes/red-first-evidence.md`; execution and closure evidence lands in
`test-evidence/`."

**Rule this file records**: every contract assertion lands BEFORE the implementation row that turns it green.
This package (Phase 1 Setup + Phase 2 Foundational) carries ONE implementation subject with a unit-test
surface — `scripts/python/script_interface_cli.py` (T011) — and NO contract-test surface: the owner page's
structure (T006–T009) is guarded by the contract test of a later package (`T012`/`T018`/`T019`), which is why
this package writes no contract test for it.

---

## Package 1's one red-first pair — the version helper (T011)

| Step | Command | Reading | Verdict |
|---|---|---|---|
| subject asserted first | `test_script_interface_cli.py::test_module_exists` | asserts `HELPER.is_file()` before any behaviour | red-first is *artifact missing*, not an import or collection error — the sibling pattern `tests/unit/test_flow_class_check.py` uses |
| **red** | `SPECKIT_PYTHON=/usr/bin/python3 /usr/bin/python3 -m pytest tests/unit/test_script_interface_cli.py -q` at `9add95eb` (before `scripts/python/script_interface_cli.py` existed) | collection succeeds; **24 failed** — every test fails on `AssertionError: artifact missing` | RED |
| first green attempt (after the first draft) | same command | **21 passed, 3 failed** | still RED — three assertions were doing real work |
| the three failures, and what each one proved | `test_module_has_no_third_party_import` | flagged `script_interface_cli` — a *docstring* naming the consumer recipe, not an import | the check was a regex, so it could not tell code from documentation; repaired to an `ast` walk over `Import` / `ImportFrom` nodes, which is the C-14 rule's actual subject |
| | `test_version_action_register_forms` | `TypeError: VersionAction.__call__() got an unexpected keyword argument 'dest'` on the INSTANCE form | a real API defect in the first draft: argparse re-instantiates whatever it receives by *calling it with its own resolved kwargs*, so a pre-built action instance can never be registered. The class is the only correct form; `VersionAction.attach(parser)` was added and the docstring corrected |
| | `test_preparse_guard_stops_at_a_bare_separator` | `SystemExit: 2` — the guard rejected `--something` *before* the `--` | the TEST was wrong, not the guard: C-9 says everything before a bare `--` is judged as an option, so a token that looks like an option before the separator is correctly an unknown option. The test was rewritten to exercise what the clause actually fixes — `["--", "--no-such-flag"]` and `["--", "--version"]` both pass through unchanged |
| **green** | `SPECKIT_PYTHON=/usr/bin/python3 /usr/bin/python3 -m pytest tests/unit/test_script_interface_cli.py -q` | **24 passed in 0.27s** | GREEN |

The three intermediate failures are recorded rather than folded away, because each one changed the artifact or
the assertion: two of them were defects in the delivered module (docstring-shaped import, instance-form action)
and one was a defect in a test that asserted a stricter reading than the clause owns.

## Why the owner page (T006–T009) has no red-first row in this package

`tasks.md` assigns the owner page's structure to contract rows that sit in later phases: T012 (the page declares
itself the single source and lists its five owned items), T018 (the banned-literal list is read OUT of the page),
T019 (the page's exception table agrees with the checker's `exceptions[]` row for row), T082 (the page and
`--emit-rule` agree in both directions). Those rows are red against the page's absence today, which is exactly the
ordering the tests-mode rule asks for. Writing a second, private guard here would be the "two rows cannot each be
the one that turns this file green" defect the tasks file already adjudicates.

The one structural property this package CAN assert without owning the guard is that the page is well-formed
enough for its mirror to be byte-identical, and that is asserted by projection, not by a test:
`sync-mirrors.py --check` exits 0 with `ok shared/ == .specify/shared/ (95 files)` (see
`test-evidence/pkg1-stage-status.md`).

## Assertions deliberately NOT written here

- `find_repo_root` walking into a **foreign checkout**: covered by `test_pyproject_without_git_is_not_a_repository_root`
  (the decoy directory) and `test_search_is_bounded_and_stops_at_the_nearest_root` (the nested root wins).
  Not covered: the literal 12-level ceiling, because a fixture that deep measures the fixture, not the rule.
- `preparse_version_guard`'s `--help` pass-through: deliberately not implemented (FR-018 — a hand-rolled parser keeps
  its own help path), so there is nothing to assert; the decision is recorded in the module docstring.
- Any assertion over `shared/definitions/script-interface-definitions.md`'s *content*: owned by T012/T018/T019/T082.
