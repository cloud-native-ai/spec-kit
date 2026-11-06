"""T006/T007 — the fixture build steps for the `docs-obligation` spaces.

Two duties live here, both about the *state* of a fixture copy rather than about judging anything:

* **T006 `copy_fixture(name, tmp_path)`** — every writing or deleting case operates on a `tmp_path` copy, so
  the repository copy stays byte-identical to its registered composition (`data-model.md` E6). Same shape as
  `tests/integration/test_docs_command_scenarios.py::make_skeleton(tmp_path)`: the case asks for a space, the
  helper materialises it somewhere disposable.
* **T007 `apply_mtime_step(root)`** — `stale-source/`'s mtime inequality is an **explicit fixture fact**, never
  a `git checkout` ordering artifact. The build step sets the source's mtime to `rendered mtime + 60s` and then
  asserts the inequality, so a filesystem that silently refuses `os.utime` fails here — loudly, once — instead
  of making that fixture change colour per machine.

Why the inequality is applied to the copy and not to the repository copy: git stores no mtime, so a value
written into the repository tree would be discarded on the next clone and the fixture would quietly revert to
checkout order. Applying it at copy time keeps the repository copy honest (`git status` clean after a run) and
makes the fact reproducible on every machine.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

FIXTURES_ROOT = Path(__file__).resolve().parent

FIXTURE_NAMES = (
    "clean",
    "no-diagram",
    "deleted-rendered",
    "orphan-rendered",
    "orphan-source",
    "stale-source",
    "no-trace",
    "trace-incomplete",
    "exempt-ok",
    "exempt-bad",
    "exempt-superseded",
)

# Spaces whose registered state is an mtime inequality rather than a file's presence.
MTIME_SPACES = ("stale-source",)

SOURCE_REL = "docs/assets/widget.mmd"
RENDERED_REL = "docs/assets/widget.svg"

MTIME_GAP_SECONDS = 60


def fixture_path(name: str) -> Path:
    if name not in FIXTURE_NAMES:
        raise KeyError(f"unknown docs-obligation fixture: {name!r}")
    return FIXTURES_ROOT / name


def copy_fixture(name: str, tmp_path: Path) -> Path:
    """Copy the named fixture space into `tmp_path` and return the copy's root.

    The copy is the ONLY place a case may write, delete or `os.utime` — the repository copy is the pre-state
    the E6 table registers.
    """
    src = fixture_path(name)
    if not src.is_dir():
        raise AssertionError(f"fixture space {name!r} is absent at {src} — run build_fixtures.py")
    dst = Path(tmp_path) / f"space-{name}"
    shutil.copytree(src, dst, symlinks=True)
    apply_mtime_step(dst)
    return dst


def apply_mtime_step(root: Path) -> None:
    """Make `stale-source/`'s source strictly newer than its earliest rendered face (T007).

    A no-op for every space that does not register an mtime fact, so callers can apply it unconditionally.
    """
    source = Path(root) / SOURCE_REL
    rendered = Path(root) / RENDERED_REL
    if not (source.is_file() and rendered.is_file()):
        return
    if (Path(root).name.removeprefix("space-")) not in MTIME_SPACES:
        return
    rendered_mtime = rendered.stat().st_mtime
    target = rendered_mtime + MTIME_GAP_SECONDS
    os.utime(source, (target, target))
    # Assert immediately: a filesystem that refuses utime must fail HERE, not make the
    # fixture change colour per machine.
    source_mtime = source.stat().st_mtime
    assert source_mtime > rendered.stat().st_mtime, (
        f"os.utime did not take effect on {source}: source={source_mtime} "
        f"rendered={rendered.stat().st_mtime} — the stale-source fixture would change colour per machine"
    )
    assert abs(source_mtime - (rendered_mtime + MTIME_GAP_SECONDS)) < 1.0, (
        f"mtime drift after utime on {source}: expected {rendered_mtime + MTIME_GAP_SECONDS}, "
        f"got {source_mtime}"
    )
