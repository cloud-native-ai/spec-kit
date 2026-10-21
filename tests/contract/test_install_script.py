"""Contract tests for the repo-root bootstrap installer (install.sh).

Contract: install.sh is the single owner of cold-start install logic —
python resolution ladder, pip index pairing, intranet-first source fallback,
and the opt-in uv path. These tests pin the externally observable contract
with offline dry-runs only (--dry-run --no-probe; no network, no mutation):
help surface, intranet-first source ordering, index override precedence,
interpreter pinning, local/editable modes, and the uv-missing fast-fail.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTALL_SH = REPO_ROOT / "install.sh"

pytestmark = pytest.mark.contract

GITLAB = "gitlab.alibaba-inc.com"
GITEE = "gitee.com"
GITHUB = "github.com"


def _run(args, *, env_extra=None, cwd=None):
    """Run install.sh in a hermetic-ish environment, offline dry-run style."""
    env = os.environ.copy()
    # Strip installer-relevant env so tests are deterministic regardless of
    # the machine the suite runs on.
    for var in ("PIP_INDEX_URL", "SPECIFY_PYTHON", "SPECIFY_INSTALLER"):
        env.pop(var, None)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        ["bash", str(INSTALL_SH), *args],
        capture_output=True,
        text=True,
        timeout=120,
        env=env,
        cwd=str(cwd) if cwd else None,
        check=False,
    )


def test_script_exists_and_parses():
    assert INSTALL_SH.is_file(), "repo-root install.sh must exist"
    result = subprocess.run(
        ["bash", "-n", str(INSTALL_SH)], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr


def test_help_documents_contract_surface():
    result = _run(["--help"])
    assert result.returncode == 0
    for flag in (
        "--python",
        "--index-url",
        "--source-url",
        "--local",
        "--uv",
        "--intranet-only",
        "--no-probe",
        "--dry-run",
    ):
        assert flag in result.stdout, f"--help must document {flag}"
    # Exit-code contract is part of the surface.
    assert "0 ok" in result.stdout and "2" in result.stdout


def test_dry_run_plan_lists_sources_intranet_first(tmp_path):
    result = _run(["--dry-run", "--no-probe"], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    out = result.stdout
    assert "==== install.sh plan (dry-run) ====" in out
    assert "would run:" in out
    # Intranet-first ordering: internal GitLab before both public mirrors.
    assert out.index(GITLAB) < out.index(GITEE) < out.index(GITHUB)
    # The pip install line always pins the probed index explicitly.
    assert "pip install" in out and "--index-url" in out
    # Post-install verification is part of the plan.
    assert "specify check" in out


def test_dry_run_intranet_only_drops_public_mirrors(tmp_path):
    result = _run(["--dry-run", "--no-probe", "--intranet-only"], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert GITLAB in result.stdout
    assert GITEE not in result.stdout
    assert GITHUB not in result.stdout


def test_index_url_flag_beats_env(tmp_path):
    result = _run(
        ["--dry-run", "--no-probe", "--index-url=http://flag.invalid/simple/"],
        env_extra={"PIP_INDEX_URL": "http://env.invalid/simple/"},
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    assert "http://flag.invalid/simple/" in result.stdout
    assert "http://env.invalid/simple/" not in result.stdout
    assert "flag --index-url" in result.stdout


def test_pip_index_url_env_is_respected(tmp_path):
    result = _run(
        ["--dry-run", "--no-probe"],
        env_extra={"PIP_INDEX_URL": "http://env.invalid/simple/"},
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    assert "http://env.invalid/simple/" in result.stdout
    assert "env PIP_INDEX_URL" in result.stdout


def test_python_flag_pins_interpreter(tmp_path):
    result = _run(["--dry-run", "--no-probe", "--python",
                  sys.executable], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert sys.executable in result.stdout


def test_python_flag_rejects_missing_interpreter():
    result = _run(["--python", "/nonexistent/python-xyz"])
    assert result.returncode == 2
    assert "not executable" in result.stderr


def test_local_mode_is_editable_install_of_repo_root(tmp_path):
    result = _run(["--dry-run", "--no-probe", "--local"], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert "pip install -e" in result.stdout
    assert str(REPO_ROOT) in result.stdout


def test_source_url_local_directory_installs_from_dir(tmp_path):
    checkout = tmp_path / "spec-kit-checkout"
    checkout.mkdir()
    (checkout /
     "pyproject.toml").write_text("[project]\nname = 'stub'\n", encoding="utf-8")
    result = _run(["--dry-run", "--no-probe", "--source-url",
                  str(checkout)], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert str(checkout) in result.stdout
    assert "pip install -e" not in result.stdout  # non-editable from a dir


def test_source_url_rejects_non_checkout_directory(tmp_path):
    empty = tmp_path / "not-a-checkout"
    empty.mkdir()
    result = _run(["--source-url", str(empty)])
    assert result.returncode == 2
    assert "pyproject.toml" in result.stderr


@pytest.mark.skipif(shutil.which("uv") is not None, reason="uv present on this machine")
def test_uv_optin_fails_fast_when_uv_missing(tmp_path):
    """uv is an accelerator, never a bootstrap dependency: a machine without
    uv gets a hard exit 2 with guidance, even in dry-run."""
    result = _run(["--uv", "--dry-run", "--no-probe"], cwd=tmp_path)
    assert result.returncode == 2
    assert "uv" in result.stderr
    assert "never installs uv" in result.stderr


def test_local_and_source_url_are_mutually_exclusive(tmp_path):
    result = _run(["--local", "--source-url",
                  "git+https://example.invalid/x.git"])
    assert result.returncode == 2
    assert "mutually exclusive" in result.stderr


# ------------------------------------------------- upgrade-in-place ladder --
# specify has no self-update subcommand, so this installer doubles as the
# UPGRADE path (clean reinstall). The ladder must prefer the python of an
# existing specify over unrelated PATH pythons, else an upgrade from a random
# directory installs a duplicate into the wrong env.


def _fake_existing_install(base):
    """Create a fake venv-layout tool dir: <base>/bin/{specify,python}."""
    bin_dir = base / "bin"
    bin_dir.mkdir(parents=True)
    (bin_dir / "specify").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    (bin_dir / "specify").chmod(0o755)
    (bin_dir / "python").symlink_to(sys.executable)
    return bin_dir


def test_upgrade_in_place_prefers_existing_specify_python(tmp_path):
    bin_dir = _fake_existing_install(tmp_path / "fakevenv")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    result = _run(
        ["--dry-run", "--no-probe"],
        env_extra={"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"},
        cwd=elsewhere,
    )
    assert result.returncode == 0, result.stderr
    assert str(bin_dir / "python") in result.stdout
    assert "upgrade-in-place" in result.stdout


def test_cwd_venv_beats_existing_specify(tmp_path):
    """Caller's cwd context wins over the existing installation: the fleet
    upgrade workflow cds into a project venv and expects THAT env."""
    bin_dir = _fake_existing_install(tmp_path / "fakevenv")
    project = tmp_path / "project"
    (project / ".venv" / "bin").mkdir(parents=True)
    (project / ".venv" / "bin" / "python").symlink_to(sys.executable)
    result = _run(
        ["--dry-run", "--no-probe"],
        env_extra={"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"},
        cwd=project,
    )
    assert result.returncode == 0, result.stderr
    assert str(project / ".venv" / "bin" / "python") in result.stdout
    assert "cwd .venv" in result.stdout


def test_pinned_python_beats_existing_specify(tmp_path):
    bin_dir = _fake_existing_install(tmp_path / "fakevenv")
    result = _run(
        ["--dry-run", "--no-probe", "--python", sys.executable],
        env_extra={"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"},
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    assert sys.executable in result.stdout
    assert "flag --python" in result.stdout


def test_help_documents_upgrade_semantics():
    result = _run(["--help"])
    assert result.returncode == 0
    assert "Upgrade semantics" in result.stdout
    assert "upgrade-in-place" in result.stdout
