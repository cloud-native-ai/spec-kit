# Red-first evidence — 087 arch-diagram-docs (implement stage)

## Evidence landing points (T001)

- notes: `/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs/.specify/specs/087-arch-diagram-docs/notes`
- test-evidence: `/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs/.specify/specs/087-arch-diagram-docs/test-evidence`

Both are repository paths under `.specify/specs/087-arch-diagram-docs/`; the absolute forms above are the
resolved reading of the same two directories in this worktree. Every row below quotes the command it ran and
the real output it got — nothing here is copied from a planning-phase projection.

Interpreter used for every reading in this file (the one that can `import typer`):

```text
$ /usr/bin/python3 -c "import sys, typer, pytest; print(sys.version); print('typer', typer.__version__); print('pytest', pytest.__version__)"
3.11.13 (main, May 13 2026, 09:30:18) [GCC 10.2.1 20200825 (Alibaba 10.2.1-3.9 2.32)]
typer 0.27.3
pytest 9.2.0
```

(A bare `python3` that cannot `import typer` reports a false red on the mirror checks; see
`notes/pre-change-measurements.md` § T003 for that trap's measured output. It is an environment gap, never
drift.)

## T008–T012 — the red-first reading (before `--action obligation` existed)

Command, run in the worktree with the typer-capable interpreter:

```text
$ /usr/bin/python3 -m pytest tests/unit/test_docs_utils_obligation.py \
    tests/unit/test_docs_utils_carriers.py tests/integration/test_docs_obligation_scenarios.py \
    -q --no-header -p no:cacheprovider
=========================== short test summary info ============================
FAILED tests/unit/test_docs_utils_obligation.py::test_c001_action_registered
FAILED tests/unit/test_docs_utils_obligation.py::test_c001_option_set_closed
FAILED tests/unit/test_docs_utils_obligation.py::test_c001_before_implementation_exit2
FAILED tests/unit/test_docs_utils_obligation.py::test_c016_precedence_order
FAILED tests/unit/test_docs_utils_obligation.py::test_c016_no_backtracking
FAILED tests/unit/test_docs_utils_obligation.py::test_c016_no_second_precedence_owner
FAILED tests/unit/test_docs_utils_obligation.py::test_c006_payload_schema
FAILED tests/unit/test_docs_utils_obligation.py::test_c006_field_order_stable
FAILED tests/unit/test_docs_utils_obligation.py::test_c006_field_set_and_order
FAILED tests/unit/test_docs_utils_carriers.py::test_carriers_typed_dirs_recursive
FAILED tests/unit/test_docs_utils_carriers.py::test_c003_non_carrier_not_judged
FAILED tests/integration/test_docs_obligation_scenarios.py::test_c002_two_runs_identical_json
FAILED tests/integration/test_docs_obligation_scenarios.py::test_c002_no_writes_on_dirty_fixture
13 failed, 1 warning in 0.18s
exit status = 1
```

The cause is the one every one of these assertions is supposed to catch — the action does not exist:

```text
$ /usr/bin/python3 -m pytest tests/unit/test_docs_utils_obligation.py::test_c001_action_registered \
    tests/unit/test_docs_utils_carriers.py::test_carriers_typed_dirs_recursive -q
E       AssertionError: `--action obligation` is not a registered choice: usage: docs-utils.py [-h] --action
E                              {scan,expire,clean,archive-check,stats,validate,fix-links,audit}
E                              …
E         docs-utils.py: error: argument --action: invalid choice: 'obligation' (choose from 'scan', 'expire', 'clean', 'archive-check', 'stats', 'validate', 'fix-links', 'audit')
E       assert 2 == 0
```

Thirteen assertions, thirteen reds — no test was written against a behaviour that already worked. The one test
count that does not move is `test_c016_precedence_order`'s per-fixture loop: it fails on its first fixture
(`deleted-rendered`), which is the fixture the contract names as the ordering's sharpest case, so the red names
the intended subject.

### Per-task attribution

| Task | Assertions authored (all red at this point) |
|------|---------------------------------------------|
| T008 | `test_c001_action_registered`, `test_c001_option_set_closed`, `test_c001_before_implementation_exit2` |
| T009 | `test_carriers_typed_dirs_recursive`, `test_c003_non_carrier_not_judged` |
| T010 | `test_c002_two_runs_identical_json`, `test_c002_no_writes_on_dirty_fixture` |
| T011 | `test_c016_precedence_order`, `test_c016_no_backtracking`, `test_c016_no_second_precedence_owner` |
| T012 | `test_c006_payload_schema`, `test_c006_field_order_stable`, `test_c006_field_set_and_order` |

### Fixture build readings (T005–T007)

```text
$ /usr/bin/python3 tests/fixtures/docs-obligation/build_fixtures.py
built 11 fixture spaces: clean, no-diagram, deleted-rendered, orphan-rendered, orphan-source, stale-source, no-trace, trace-incomplete, exempt-ok, exempt-bad, exempt-superseded
OK: 11 docs-obligation fixture spaces match their registered composition
rc=0
```

`copy_fixture` + the `os.utime` step, applied to every space (the mtime fact lands only where a space registers
one):

```text
copy_fixture over all 11 spaces: ok
clean             source=1793954841.1 rendered=1793954841.1 newer=False
stale-source      source=1793954901.1 rendered=1793954841.1 newer=True   (rendered + 60s)
others            (no both-faces pair, or intentionally equal — never stale by accident)
```

The +60s gap on the copy and the post-`utime` assertion are the T007 build step; a filesystem that silently
refused `os.utime` would fail that assertion instead of turning `stale-source/` green on one machine and red on
the next.

