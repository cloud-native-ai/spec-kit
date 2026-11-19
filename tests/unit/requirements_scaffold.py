"""Shared sandbox helpers for the create-new-requirements.sh regressions.

Not a test module (no ``test_`` prefix), so pytest does not collect it. Every helper
builds an isolated client project under the caller's ``tmp_path``: the framework repo
itself is never written to, which matters because this script scaffolds into
``.specify/specs`` of whatever root it resolves.

stdin is always an explicit empty string unless a test supplies content. The script
reads stdin whenever it is not a tty, so an inherited pipe would otherwise be consumed
as feature description (and would eat a surrounding loop's input).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_REL = "scripts/bash/create-new-requirements.sh"
SCRIPT_PATH = ROOT / SCRIPT_REL


def _git_init(path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.invalid"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=path, check=True)
    subprocess.run(["git", "commit", "--allow-empty", "-q", "-m", "init"], cwd=path, check=True)


def _install_scripts(proj: Path) -> None:
    (proj / "scripts").mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "scripts" / "bash", proj / "scripts" / "bash")


def make_project(base: Path, *, git: bool = True) -> Path:
    """A client project: ``.specify/specs`` plus a copy of ``scripts/bash``."""
    proj = base / "tree"
    (proj / ".specify" / "specs").mkdir(parents=True)
    _install_scripts(proj)
    (proj / "pyproject.toml").write_text(
        '[project]\nname = "s"\nversion = "1.0.0"\n', encoding="utf-8"
    )
    if git:
        _git_init(proj)
    return proj


def make_nested(base: Path) -> tuple[Path, Path]:
    """An outer git repo holding a member spec-kit project with no ``.git`` of its own.

    This is the shape upstream b1ba97297 fixes: ``git rev-parse --show-toplevel`` from
    the member answers with the OUTER root, so a git-first resolution scaffolds into
    the wrong project.
    """
    outer = base / "outer"
    outer.mkdir(parents=True)
    _git_init(outer)
    member = outer / "member"
    (member / ".specify" / "specs").mkdir(parents=True)
    _install_scripts(member)
    return outer, member


def make_plain_git(base: Path) -> Path:
    """A git repository with no ``.specify`` marker, but with the script installed."""
    proj = base / "plaingit"
    proj.mkdir(parents=True)
    _git_init(proj)
    _install_scripts(proj)
    return proj


def run_script(
    proj: Path,
    *args: str,
    stdin: str = "",
    env: dict[str, str] | None = None,
    bash: str = "bash",
    cwd: Path | None = None,
) -> subprocess.CompletedProcess:
    """Run the script with cwd=proj (or an explicit subdirectory). ``encoding='utf-8'``
    keeps decoding independent of the child's locale, so a LC_ALL=C run still yields
    readable Unicode output."""
    child_env = dict(os.environ)
    if env is not None:
        child_env.update(env)
    # Absolute script path: a test may run from a subdirectory of the project, where a
    # relative SCRIPT_REL would not resolve.
    return subprocess.run(
        [bash, str(proj / SCRIPT_REL), *args],
        cwd=cwd if cwd is not None else proj,
        capture_output=True,
        encoding="utf-8",
        timeout=120,
        input=stdin,
        env=child_env,
    )


def git_branch(repo: Path) -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo, capture_output=True, encoding="utf-8", timeout=60,
    )
    return proc.stdout.strip()


def minimal_env(**extra: str) -> dict[str, str]:
    """An ``env -i``-style environment: only what the script genuinely needs."""
    keep = ("PATH", "HOME", "CWS_LIB_BASH_HOME")
    base = {k: os.environ[k] for k in keep if k in os.environ}
    base.update(extra)
    return base


def field(stdout: str, key: str) -> str:
    prefix = f"{key}: "
    for line in stdout.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):]
    return ""


def branch_name(stdout: str) -> str:
    return field(stdout, "BRANCH_NAME")


def suffix(stdout: str) -> str:
    name = branch_name(stdout)
    return name.split("-", 1)[1] if "-" in name else ""


def spec_file(stdout: str) -> str:
    return field(stdout, "SPEC_FILE")


def json_out(stdout: str) -> dict:
    return json.loads(stdout)


def byte_len(text: str) -> int:
    return len(text.encode("utf-8"))


def spec_dirs(proj: Path) -> list[str]:
    specs = proj / ".specify" / "specs"
    return sorted(p.name for p in specs.iterdir()) if specs.is_dir() else []