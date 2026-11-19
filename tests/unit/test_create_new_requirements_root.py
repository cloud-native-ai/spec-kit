"""Repository-root resolution: the ``.specify`` marker outranks git.

Ported fix family (upstream github/spec-kit):
  * b1ba97297 — when spec-kit is initialised in a subdirectory of a larger repository,
    ``git rev-parse --show-toplevel`` answers with the OUTER root, so the scaffold and
    the branch landed in the wrong project. ``.specify`` is spec-kit's own marker and
    is searched first; git stays the second choice and the script-directory marker walk
    remains the last resort for --no-git projects. Git then counts as available only
    when the resolved root is itself a work tree.
  * 6757c90db — a failed branch checkout names the real remedy (existing branch vs git
    misconfiguration) instead of leaving a bare git error.

Adaptation note: this fork's common.sh publishes the host library's git-first
``git_repo_root`` (cws-lib-bash), a different contract owned elsewhere. The resolution
is therefore local to create-new-requirements.sh and that helper is left untouched.
"""
from __future__ import annotations

import json
import os
import stat
import subprocess

from tests.unit.requirements_scaffold import (
    branch_name,
    git_branch,
    make_nested,
    make_plain_git,
    make_project,
    run_script,
    spec_dirs,
    spec_file,
)


def test_nested_member_project_scaffolds_into_the_member_not_the_outer_repo(tmp_path):
    outer, member = make_nested(tmp_path)
    outer_branch_before = git_branch(outer)
    proc = run_script(member, "Add user authentication system")
    assert proc.returncode == 0, proc.stderr

    assert spec_dirs(member) == [branch_name(proc.stdout)]
    assert spec_file(proc.stdout).startswith(str(member))
    # The outer repository is untouched: no specs, no branch switch.
    assert not (outer / ".specify" / "specs").exists()
    assert git_branch(outer) == outer_branch_before


def test_nested_member_without_its_own_git_skips_branch_creation(tmp_path):
    """Git availability is decided at the resolved root, not inherited from a parent."""
    outer, member = make_nested(tmp_path)
    outer_branch_before = git_branch(outer)
    proc = run_script(member, "Add user authentication system")
    assert proc.returncode == 0, proc.stderr
    assert "Git repository not detected" in proc.stderr
    assert not (member / ".git").exists()
    assert git_branch(outer) == outer_branch_before


def test_git_root_is_used_when_there_is_no_specify_marker(tmp_path):
    """A plain git repository keeps the pre-port resolution: git is the second choice."""
    proj = make_plain_git(tmp_path)
    proc = run_script(proj, "--json", "Add user authentication system")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["SPEC_FILE"].startswith(str(proj))
    assert spec_dirs(proj) == ["001-user-authentication-system"]
    assert git_branch(proj) == "001-user-authentication-system"


def test_no_git_project_with_specify_marker_still_scaffolds(tmp_path):
    proj = make_project(tmp_path, git=False)
    proc = run_script(proj, "Add user authentication system")
    assert proc.returncode == 0, proc.stderr
    assert spec_dirs(proj) == ["001-user-authentication-system"]
    assert "Git repository not detected" in proc.stderr


def test_git_project_with_specify_marker_creates_the_branch(tmp_path):
    proj = make_project(tmp_path, git=True)
    proc = run_script(proj, "Add user authentication system")
    assert proc.returncode == 0, proc.stderr
    assert git_branch(proj) == "001-user-authentication-system"
    assert "Git repository not detected" not in proc.stderr


def test_resolution_walks_up_from_a_subdirectory(tmp_path):
    """The marker search starts at the working directory and walks upward."""
    proj = make_project(tmp_path)
    sub = proj / "src" / "deep"
    sub.mkdir(parents=True)
    proc = run_script(proj, "Add user authentication system", cwd=sub)
    assert proc.returncode == 0, proc.stderr
    assert spec_file(proc.stdout).startswith(str(proj))
    assert spec_dirs(proj) == ["001-user-authentication-system"]


def test_numbering_still_reads_the_resolved_roots_spec_dirs(tmp_path):
    """Root resolution must not disturb the existing numbering sources."""
    proj = make_project(tmp_path)
    (proj / ".specify" / "specs" / "007-existing").mkdir(parents=True)
    proc = run_script(proj, "Add user authentication system")
    assert proc.returncode == 0, proc.stderr
    assert branch_name(proc.stdout) == "008-user-authentication-system"


def test_numbering_handles_octal_looking_prefixes(tmp_path):
    """The ERE digit probe must still feed the ``10#`` decimal guard: 008 -> 009."""
    proj = make_project(tmp_path)
    (proj / ".specify" / "specs" / "008-existing").mkdir(parents=True)
    proc = run_script(proj, "Add auth")
    assert proc.returncode == 0, proc.stderr
    assert branch_name(proc.stdout) == "009-auth"


def test_numbering_counts_archived_spec_dirs(tmp_path):
    """Archived specs keep their numbers; the probe change must not lose that source."""
    proj = make_project(tmp_path)
    (proj / ".specify" / "specs" / ".archive" / "012-archived").mkdir(parents=True)
    proc = run_script(proj, "Add auth")
    assert proc.returncode == 0, proc.stderr
    assert branch_name(proc.stdout) == "013-auth"


def _git_shim(tmp_path, *, checkout_fails: bool, branch_exists: bool):
    """A PATH-front git that delegates to the real git except for ``checkout -b``.

    The numbering sources scan spec dirs and branch names, so an existing branch is
    always numbered around and a real collision cannot be staged deterministically.
    The shim exercises the diagnostic logic directly instead of contriving repo state.
    """
    real_git = subprocess.run(["which", "git"], capture_output=True, encoding="utf-8",
                              check=True).stdout.strip()
    shim_dir = tmp_path / "shim"
    shim_dir.mkdir()
    listing = "001-user-authentication-system\n" if branch_exists else ""
    shim = shim_dir / "git"
    shim.write_text(
        "#!/usr/bin/env bash\n"
        f'real="{real_git}"\n'
        'if [ "$1" = "checkout" ] && [ "$2" = "-b" ]; then\n'
        + ('  exit 1\n' if checkout_fails else '  exec "$real" "$@"\n')
        + 'fi\n'
        'if [ "$1" = "branch" ] && [ "$2" = "--list" ]; then\n'
        + f"  printf '%s' '{listing}'\n"
        + '  exit 0\n'
        + 'fi\n'
        'exec "$real" "$@"\n',
        encoding="utf-8",
    )
    shim.chmod(shim.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return {"PATH": f"{shim_dir}{os.pathsep}{os.environ['PATH']}"}


def test_failed_checkout_reports_an_existing_branch(tmp_path):
    proj = make_project(tmp_path)
    env = _git_shim(tmp_path, checkout_fails=True, branch_exists=True)
    proc = run_script(proj, "Add user authentication system", env=env)
    assert proc.returncode == 1
    assert "already exists" in proc.stderr
    assert "different feature name" in proc.stderr


def test_failed_checkout_reports_a_git_problem_when_no_branch_exists(tmp_path):
    proj = make_project(tmp_path)
    env = _git_shim(tmp_path, checkout_fails=True, branch_exists=False)
    proc = run_script(proj, "Add user authentication system", env=env)
    assert proc.returncode == 1
    assert "Failed to create git branch" in proc.stderr
    assert "git configuration" in proc.stderr


def test_json_mode_checkout_failure_stays_nonzero_and_stderr_only(tmp_path):
    """The pre-existing JSON-mode contract: no git chatter on stdout, exit 1."""
    proj = make_project(tmp_path)
    env = _git_shim(tmp_path, checkout_fails=True, branch_exists=True)
    proc = run_script(proj, "--json", "Add user authentication system", env=env)
    assert proc.returncode == 1
    assert proc.stdout.strip() == ""
    assert "Failed to create and switch to branch" in proc.stderr