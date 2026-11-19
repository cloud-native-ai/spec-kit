"""Shared sandbox for the bash hardening regressions (P1 Agent B territory).

Not a test module (no ``test_`` prefix), so pytest does not collect it. Every helper
builds an isolated client project under the caller's ``tmp_path``; the framework repo
itself is never written to. That matters twice over here: the scripts under test
scaffold into ``.specify/specs`` of whatever root they resolve, and one of them is
tested with a branch name that is an injection payload.

The sandbox directory name carries a SPACE on purpose. ``get_feature_paths`` used to
emit ``KEY='value'`` lines that callers fed to an unquoted ``eval $(...)``; a space is
the mildest form of the value that re-parsing mishandles, and a single quote is the
form that turns data into code.

Shell matrix: every bash change is verified under a UTF-8 locale and under C, each
with and without ``shopt -s compat32``. Only bash 4.x is installed here, so bash 3.2
semantics are simulated with bash's own compatibility level rather than claimed:
``compat32`` is injected through ``BASH_ENV``, which a non-interactive bash sources
before it runs the script, so ``$0`` / ``BASH_SOURCE`` stay exactly what a direct
invocation gives them (``bash -c 'shopt ...; source script'`` would not).
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BASH_SRC = ROOT / "scripts" / "bash"

#: (locale, compat32) — the four readings the port discipline asks for. Each param
#: carries ONE value (a tuple), so the fixture hands the pair to the test as one arg.
SHELL_MATRIX = [
    pytest.param(("C.UTF-8", False), id="utf8"),
    pytest.param(("C", False), id="c-locale"),
    pytest.param(("C.UTF-8", True), id="utf8-compat32"),
    pytest.param(("C", True), id="c-locale-compat32"),
]

#: common.sh publishes its helpers only after the host shell library loads; without
#: it the library-link captures nothing at all (git_repo_root included), so these
#: cases cannot measure anything. The reason is stated, never silently skipped.
HOST_LIB = os.environ.get("CWS_LIB_BASH_HOME", "")
needs_host_lib = pytest.mark.skipif(
    not HOST_LIB or not (Path(HOST_LIB) / "bin" / "cws_bash_env").is_file(),
    reason="CWS_LIB_BASH_HOME host shell library absent: common.sh publishes no helpers",
)


@pytest.fixture(params=SHELL_MATRIX)
def shell(request, tmp_path):
    """The (locale, compat32) reading under test, as a runnable env overlay."""
    locale, compat32 = request.param
    overlay = {"LC_ALL": locale, "LANG": locale}
    if compat32:
        env_file = tmp_path / "compat32.env"
        env_file.write_text("shopt -s compat32\n", encoding="utf-8")
        overlay["BASH_ENV"] = str(env_file)
    else:
        overlay.pop("BASH_ENV", None)
    return overlay


def _git_init(path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.invalid"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=path, check=True)
    subprocess.run(["git", "commit", "--allow-empty", "-q", "-m", "init"], cwd=path, check=True)


def make_repo(base: Path, *, dirname: str = "repo space", branch: str = "001-demo") -> Path:
    """A client git project whose root path contains a space, with scripts installed."""
    proj = base / dirname
    (proj / ".specify" / "specs").mkdir(parents=True)
    (proj / ".specify" / "templates").mkdir(parents=True)
    shutil.copytree(BASH_SRC, proj / "scripts" / "bash")
    (proj / "pyproject.toml").write_text(
        '[project]\nname = "s"\nversion = "1.0.0"\n', encoding="utf-8"
    )
    _git_init(proj)
    subprocess.run(["git", "checkout", "-q", "-b", branch], cwd=proj, check=True)
    return proj


def spec_dir(proj: Path, name: str) -> Path:
    d = proj / ".specify" / "specs" / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def plan_template(proj: Path, text: str | None) -> Path:
    """Write the plan template; ``None`` removes it, ``""`` leaves it empty."""
    tpl = proj / ".specify" / "templates" / "plan-template.md"
    if text is None:
        tpl.unlink(missing_ok=True)
    else:
        tpl.write_text(text, encoding="utf-8")
    return tpl


def child_env(proj: Path, overlay: dict | None = None, **extra: str) -> dict:
    """An ``env -i``-style environment: only what the scripts genuinely need.

    Keeping the inherited environment out is the point: a stray SPECIFY_FEATURE or
    LC_ALL in the parent would otherwise decide what the child resolves.
    """
    keep = ("PATH", "HOME", "CWS_LIB_BASH_HOME")
    env = {k: os.environ[k] for k in keep if k in os.environ}
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_SYSTEM"] = os.devnull
    if overlay:
        env.update(overlay)
    env.update(extra)
    return env


def run_script(
    proj: Path,
    script: str,
    *args: str,
    overlay: dict | None = None,
    **extra: str,
) -> subprocess.CompletedProcess:
    """Run one installed bash script with cwd=proj.

    ``encoding='utf-8'`` keeps decoding independent of the child's locale, so a
    LC_ALL=C run still yields readable Unicode. stdin is always empty: none of these
    scripts should read it, and an inherited pipe would be consumed as input.
    """
    return subprocess.run(
        ["bash", f"scripts/bash/{script}", *args],
        cwd=proj,
        capture_output=True,
        encoding="utf-8",
        timeout=120,
        input="",
        env=child_env(proj, overlay, **extra),
    )


def run_snippet(
    proj: Path,
    snippet: str,
    *args: str,
    overlay: dict | None = None,
    **extra: str,
) -> subprocess.CompletedProcess:
    """Run a bash snippet that sources the installed common.sh, with cwd=proj."""
    return subprocess.run(
        ["bash", "-c", snippet, "--", *args],
        cwd=proj,
        capture_output=True,
        encoding="utf-8",
        timeout=120,
        input="",
        env=child_env(proj, overlay, **extra),
    )


#: Source the installed library the way every caller does, then expose the helpers.
SOURCE_COMMON = 'source "$PWD/scripts/bash/common.sh" >/dev/null 2>&1; '

#: The consumer shape the port installs: capture, check status, eval the QUOTED text.
SAFE_EVAL = (
    "_out=$(get_feature_paths) || { echo RESOLVE_FAILED; exit 1; }; "
    'eval "$_out"; unset _out; '
)