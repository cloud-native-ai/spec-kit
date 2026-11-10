# Red-first evidence — wp02-observer-definition

One entry per red-first run: command · real output · exit status. Appended by the rows of
`wp02-observer-definition` (T018, T037); never rewritten.

<!-- entries appended below -->

## T018 — observer agent contract module, red while the template is absent

Command: `bash scripts/bash/run-tests.sh tests/contract/test_sdd_observer_agent.py -q`
Exit status: 1

```text
    def test_template_exists_with_neutral_frontmatter():
        from specify_cli import NEUTRAL_AGENT_METADATA_KEYS

>       fields, body = _frontmatter_fields(_text())
                                           ^^^^^^^

tests/contract/test_sdd_observer_agent.py:66:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

path = PosixPath('/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/agents/sdd-observer.agent.md')

    def _text(path: Path = TEMPLATE) -> str:
>       assert path.is_file(), "missing observer template: %s" % path
E       AssertionError: missing observer template: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/agents/sdd-observer.agent.md
E       assert False
E        +  where False = is_file()

tests/contract/test_sdd_observer_agent.py:31: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_sdd_observer_agent.py::test_role_face_is_observer_not_a_stage_seat
FAILED tests/contract/test_sdd_observer_agent.py::test_read_domain_and_write_surface_are_declared
FAILED tests/contract/test_sdd_observer_agent.py::test_forbidden_capabilities_are_declared
FAILED tests/contract/test_sdd_observer_agent.py::test_objectivity_prohibition_is_verbatim
FAILED tests/contract/test_sdd_observer_agent.py::test_three_layer_binding_uses_the_current_model
FAILED tests/contract/test_sdd_observer_agent.py::test_fast_fail_clause_is_byte_identical
FAILED tests/contract/test_sdd_observer_agent.py::test_template_exists_with_neutral_frontmatter
7 failed in 6.14s
```

## T037 — US5 appended assertions: no red-first leg by construction

Command: `bash scripts/bash/run-tests.sh tests/contract/test_journal_engine.py -q`
Exit status: 0

```text
..................                                                       [100%]
18 passed in 7.35s
```

Disclosure (tasks.md § Tests, line 11 exception): T037 extends an already-authored module and
claims no `[green:]` point. The engine behavior its three assertions observe — single-writer
flock (T011), per-line identity (T009–T011) and projection order (T010) — landed in
`wp01-journal-core`, so there is no earlier red state of this module to append. A fabricated
red run would not describe any real tree state, so the entry is recorded as what it is.

The red capability is held inside the passing tests rather than in a past run:

- `test_first_journal_row_precedes_first_stage_completion` withholds every stage carrier for the
  observer's first append, restores them after a 1.05 s clock boundary, and asserts a strictly
  earlier `observed_at` for the first journal row; an engine that projected stage completions
  before the observer's first entry turns it red.
- `test_same_line_second_writer_exits_three` reruns the held-lock probe against a copied engine
  with the `fcntl.flock` line removed and asserts that engine is NOT refused (exit != `3`, no
  `concurrent-writer-refused`), so the exit-3 assertion cannot pass vacuously.
