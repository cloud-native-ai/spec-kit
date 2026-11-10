"""Unit tests: the carrier set of `--action obligation` (spec 087, `C-003`).

`plan.md` § Test Plan table A row `C-003` owns the assertion names and their red-when conditions. This file is
separate from `test_docs_utils_obligation.py` because it writes a different path — the two never conflict in a
parallel phase, and the carrier set is the one definition point a whole family of judgements rests on.

The carrier set is: `<root>/docs/{concepts,tutorials,tasks,reference,decisions,contribute}/**/*.md` read
**recursively**, plus `<root>/docs/ARCHITECTURE.md` when it exists. Everything else under `docs/` —
`notes/`, `archive/`, `.speckit/`, site tooling — is invisible: not judged, not counted, never "passing".
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from script_api import run_engine_in_process
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "create-docs" / "scripts" / "docs-utils.py"
TYPED_DIRS = ("concepts", "tutorials", "tasks", "reference", "decisions", "contribute")


def obligation(root: Path) -> dict:
    proc = run_engine_in_process(
        SCRIPT, ["--action", "obligation", "--root", str(root)]
    )
    assert proc.returncode == 0, f"engine exited {proc.returncode}: {proc.stderr}{proc.stdout}"
    return json.loads(proc.stdout)


def judged_paths(payload: dict) -> set[str]:
    return {entry["path"] for entry in payload["documents"]}


def write(path: Path, text: str = "# doc\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_space(root: Path) -> None:
    """A space whose typed directories carry both first-level and deeply nested documents."""
    write(root / "README.md")
    for d in TYPED_DIRS:
        write(root / "docs" / d / "index.md")
    # nesting: the naive one-level glob loses every one of these
    write(root / "docs" / "reference" / "commands" / "deep-a.md")
    write(root / "docs" / "reference" / "commands" / "deeper" / "deep-b.md")
    write(root / "docs" / "concepts" / "sub" / "deep-c.md")
    # a root ARCHITECTURE.md inside docs/ is a carrier
    write(root / "docs" / "ARCHITECTURE.md")


@pytest.mark.integration
def test_carriers_typed_dirs_recursive(tmp_path: Path):
    """The six typed directories are read recursively, so nested reference documents are judged.

    The recorded trap (`notes/pre-change-measurements.md` § T002 (b)): `glob('*.md')` on a directory tree loses
    every nested file. On this space the naive walk yields 6 typed documents and the recursive walk yields the
    nested ones as well — the assertion names both numbers so a silent regression to `glob` is caught by name,
    not by a vague count mismatch.

    red-when: a nested document under any typed directory is missing from `documents[]`.
    """
    build_space(tmp_path)
    payload = obligation(tmp_path)
    judged = judged_paths(payload)

    nested = {
        "docs/reference/commands/deep-a.md",
        "docs/reference/commands/deeper/deep-b.md",
        "docs/concepts/sub/deep-c.md",
    }
    missing = nested - judged
    assert not missing, f"carrier walk is not recursive; these nested carriers were not judged: {sorted(missing)}"

    first_level = {f"docs/{d}/index.md" for d in TYPED_DIRS}
    assert first_level <= judged, f"first-level carriers missing: {sorted(first_level - judged)}"
    assert "docs/ARCHITECTURE.md" in judged, "docs/ARCHITECTURE.md is a carrier and must be judged"

    # 6 first-level + 1 docs/ARCHITECTURE.md + 3 nested
    assert payload["carriers"] == 10, (
        f"carrier count {payload['carriers']} != 10; a naive one-level glob would report 7"
    )
    assert payload["carriers"] == len(payload["documents"]), (
        "every carrier is judged exactly once: carriers and documents[] must agree"
    )


@pytest.mark.integration
def test_c003_non_carrier_not_judged(tmp_path: Path):
    """A document outside the carrier set never appears in `documents[]`.

    `docs/notes/` is temporary by contract, `docs/archive/` is retired content, `docs/.speckit/` is the machine
    area, and a site-tooling directory is not documentation — none of them carries the diagram obligation.

    red-when: any of those paths shows up in `documents[]`, whether as `satisfied` or as `missing` (invisible
    means invisible, never "silently satisfied").
    """
    build_space(tmp_path)
    write(tmp_path / "docs" / "notes" / "scratch.md")
    write(tmp_path / "docs" / "archive" / "retired.md")
    write(tmp_path / "docs" / ".speckit" / "notes" / "machine.md")
    write(tmp_path / "docs" / "site" / "tooling.md")

    payload = obligation(tmp_path)
    judged = judged_paths(payload)

    for outsider in (
        "docs/notes/scratch.md",
        "docs/archive/retired.md",
        "docs/.speckit/notes/machine.md",
        "docs/site/tooling.md",
    ):
        assert outsider not in judged, f"{outsider} is not a carrier but was judged"
    assert payload["carriers"] == 10, (
        "non-carriers must not inflate the carrier count either"
    )
