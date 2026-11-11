"""Contract test: a projected verdict is a comparison, not a computability claim.

Debt D6-68 (audit report ``.specify/studies/debt-audit-2026-11-11``, finding D5-03):
``sync-mirrors.py`` used to print ``projected[...] ...: ok`` whenever
``project_for()`` could compute the expected bytes — even when the mirror on disk
was stale, which printed ``DIFF[projected]`` and ``: ok`` on the same screen.
Contract C-35 requires ``--check`` to assert ``mirror == project(source)``, so
``ok`` is truthful only when the mirror's bytes equal the projection.

The test is a mutation leg: it builds a scratch repository whose projected
mirror is stale by construction (the source without the declared bridge), then
asserts that the projected line itself reports ``DIFF[projected]`` and the run
exits non-zero; ``--write`` heals the mirror and the same line reports ``ok``
with ``--check`` at exit 0. Prefix scoping (``--only``) keeps the scratch run on
this one pair and skips the command-copy delegation.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "sync-mirrors.py"

SOURCE_REL = "scripts/python/script_interface_cli.py"
MIRROR_REL = ".specify/scripts/python/script_interface_cli.py"
PROJECTED_PREFIX = (
    f"projected[python-version-bridge] {MIRROR_REL} <- {SOURCE_REL}: "
)


def _make_stale_tree(tmp_path: Path) -> Path:
    """A minimal repo where MIRROR_REL is the source without its projection."""
    engine_copy = tmp_path / "scripts" / "python" / "sync-mirrors.py"
    engine_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ENGINE, engine_copy)

    source = tmp_path / SOURCE_REL
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(
        "def main():\n"
        "    return 0\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    raise SystemExit(main())\n",
        encoding="utf-8",
    )

    mirror = tmp_path / MIRROR_REL
    mirror.parent.mkdir(parents=True, exist_ok=True)
    # Stale by construction: source bytes, bridge block not projected yet.
    mirror.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path


def _run(tree: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(tree / "scripts" / "python" / "sync-mirrors.py"), *args],
        cwd=str(tree),
        capture_output=True,
        text=True,
        timeout=120,
    )


def _projected_line(stdout: str) -> str:
    return next(
        (line for line in stdout.splitlines() if line.startswith(PROJECTED_PREFIX)),
        "",
    )


def test_stale_projection_prints_diff_and_fails(tmp_path):
    tree = _make_stale_tree(tmp_path)
    proc = _run(tree, "--check", "--only", SOURCE_REL)
    assert proc.returncode != 0, (
        "a stale projected mirror MUST fail --check; got exit "
        f"{proc.returncode}\n{proc.stdout}"
    )
    line = _projected_line(proc.stdout)
    assert line, f"no projected verdict line in:\n{proc.stdout}"
    assert line.endswith("DIFF[projected]"), (
        "the projected line MUST judge the mirror's bytes against the projection; "
        f"a computable-but-stale pair may not print ok. Got: {line!r}"
    )


def test_healed_projection_prints_ok_and_passes(tmp_path):
    tree = _make_stale_tree(tmp_path)
    written = _run(tree, "--write", "--only", SOURCE_REL)
    assert written.returncode == 0, (
        f"--write MUST sync the stale projection; got {written.returncode}\n"
        f"{written.stdout}"
    )
    proc = _run(tree, "--check", "--only", SOURCE_REL)
    assert proc.returncode == 0, (
        f"the healed mirror MUST pass --check; got {proc.returncode}\n{proc.stdout}"
    )
    line = _projected_line(proc.stdout)
    assert line.endswith(": ok"), (
        f"an in-sync projection is the only case that may say ok; got {line!r}"
    )
