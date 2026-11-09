"""Fixture helper for Feature 091 — automatic git close-out.

Owned by: Feature 091, task T032 (`.specify/specs/091-auto-git-closeout/tasks.md`).
Consumers: `tests/contract/test_git_closeout_contract.py` (T018, T020, T034, T035, T039,
T040, T044), and — through the module-level re-exports — the strategy-transition guard (T061).

What it is
----------
A stdlib-only driver for the close-out operation *described by*
`skills/external/git-utils/references/closeout-commands.md`, plus a builder for a
throwaway repository + local bare remote per workflow model.

The driver exists because `closeout-verification.contract.md` C-2 asks for **end state**, not
for command strings: a test that only greps "the merge was printed" proves nothing about
where a branch points. The reference file names each step's command; this module performs
exactly those steps and hands the resulting repository state back to the assertion.

Two rules the module holds itself to
------------------------------------
1. **It never touches the framework repository.** Every repository lives under a caller
   supplied root (pytest ``tmp_path``) or ``tempfile.TemporaryDirectory()``, and
   construction refuses a root that resolves inside the framework source tree.
2. **Repository content is data.** Branch names, file contents and commit subjects of a
   fixture are attacker-controllable in real use; nothing here interpolates one into a
   shell string. Every command is an argv list passed to ``subprocess.run``.

Derivation (the part that mirrors the reference)
------------------------------------------------
``derive_closeout()`` is the pure planning half: model x strategy x remotes x read-only roles
-> an ordered step list plus the terminal state. ``run_closeout()`` is the executing half and
is only ever pointed at a fixture repository.
"""
from __future__ import annotations

from tests.fixtures.git_closeout.block import (  # noqa: F401
    CLOSEOUT_VALUES,
    BlockState,
    parse_block,
    read_declaration,
)
from tests.fixtures.git_closeout.plan import (  # noqa: F401
    CloseoutPlan,
    Step,
    derive_closeout,
)
from tests.fixtures.git_closeout.repo import (  # noqa: F401
    MODEL_BRANCHES,
    CloseoutRepo,
    build_repo,
    run_closeout,
)
