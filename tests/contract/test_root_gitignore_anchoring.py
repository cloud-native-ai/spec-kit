"""Contract: the root `.gitignore` build-artifact patterns stay anchored to the repo root.

Adapted-from: a4c86b372 ("fix(build): include specify_cli.bundler.lib in built distribution").
Upstream's defect: hatchling reuses `.gitignore` patterns as build-exclusion rules, so the
unanchored `lib/` / `lib64/` lines inherited from the GitHub Python template also matched the
tracked source package `src/specify_cli/bundler/lib/` and silently dropped it from the built
wheel — every command, `specify init` included, then died on `ModuleNotFoundError`. This fork
ships no `bundler/` package today, so the port is preventive: the two patterns are anchored and
the guard measures the *ignore decision* with `git check-ignore`, not the file's wording.

The discriminating pair is the whole subject: a nested directory named `lib/` MUST NOT be
ignored, while a top-level `lib/` build artifact MUST still be. The last case seeds a throwaway
repo with the pre-fix unanchored pattern so the measurement is proven able to go red.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GITIGNORE = REPO_ROOT / ".gitignore"

pytestmark = pytest.mark.contract

#: Upstream's dropped package path — a nested `lib/` inside the shipped source tree.
NESTED_LIB_PATH = "src/specify_cli/bundler/lib/project.py"
#: The build artifact the pattern is actually for (a top-level venv/build `lib`).
TOP_LEVEL_LIB_PATH = "lib/python3.11/site-packages/thing.py"
TOP_LEVEL_LIB64_PATH = "lib64/thing.so"


def _ignore_verdict(path: str, cwd: Path) -> tuple[bool, str]:
    """Whether `path` is ignored in `cwd`, decided by git itself; a git error is not a verdict.

    `--no-index` asks about the pathname rather than the index, so the subject can be a path that
    does not exist on disk. `core.excludesFile` is neutralised so the verdict belongs to the tree's
    own `.gitignore` and not to a machine-global ignore file.
    """
    proc = subprocess.run(
        ["git", "-c", "core.excludesFile=/dev/null",
         "check-ignore", "-v", "--no-index", path],
        cwd=str(cwd), capture_output=True, text=True,
    )
    assert proc.returncode in (0, 1), (
        "git check-ignore could not decide %r (rc=%s): %s%s"
        % (path, proc.returncode, proc.stdout, proc.stderr)
    )
    return proc.returncode == 0, proc.stdout


def _pattern_lines() -> list[str]:
    return [
        line.strip()
        for line in GITIGNORE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def test_the_lib_patterns_are_root_anchored():
    """The two patterns carry the leading slash, and no unanchored twin survives beside them."""
    lines = _pattern_lines()
    assert "/lib/" in lines and "/lib64/" in lines, (
        "the root .gitignore must anchor both build-artifact patterns (/lib/, /lib64/); got %r"
        % ([line for line in lines if "lib" in line],)
    )
    assert "lib/" not in lines and "lib64/" not in lines, (
        "an unanchored lib/ or lib64/ pattern matches a nested source directory at any depth "
        "and hatchling turns it into a build exclusion"
    )


def test_a_nested_lib_directory_is_not_ignored():
    """The defect's own path: a source package directory named lib/ must stay visible to git."""
    ignored, detail = _ignore_verdict(NESTED_LIB_PATH, REPO_ROOT)
    assert not ignored, (
        "%s is ignored, so a tracked package at that path would be excluded from the wheel: %s"
        % (NESTED_LIB_PATH, detail)
    )


def test_a_top_level_lib_build_artifact_is_still_ignored():
    """Anchoring narrows the pattern; it must not abolish it — the intended artifact stays ignored."""
    for path, rule in ((TOP_LEVEL_LIB_PATH, "/lib/"), (TOP_LEVEL_LIB64_PATH, "/lib64/")):
        ignored, detail = _ignore_verdict(path, REPO_ROOT)
        assert ignored, "%s must still be ignored as a top-level build artifact" % path
        assert rule in detail, (
            "the verdict must come from the anchored %s rule, not from some other pattern: %s"
            % (rule, detail)
        )


def test_the_unanchored_pattern_is_the_defect_this_guard_sees(tmp_path):
    """A green check is a claim, not evidence: the same measurement goes red on the pre-fix pattern."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], capture_output=True, text=True, check=True)
    ignore_file = tmp_path / ".gitignore"

    ignore_file.write_text("lib/\nlib64/\n", encoding="utf-8")
    ignored, _ = _ignore_verdict(NESTED_LIB_PATH, tmp_path)
    assert ignored, (
        "the seeded pre-fix pattern must ignore the nested package path — otherwise this guard "
        "measures nothing and its green verdict on the real tree proves nothing"
    )

    ignore_file.write_text("/lib/\n/lib64/\n", encoding="utf-8")
    ignored, _ = _ignore_verdict(NESTED_LIB_PATH, tmp_path)
    assert not ignored, "the anchored pattern must free the nested path in the same seeded tree"
    ignored, _ = _ignore_verdict(TOP_LEVEL_LIB_PATH, tmp_path)
    assert ignored, "the anchored pattern must still ignore the top-level artifact in that tree"