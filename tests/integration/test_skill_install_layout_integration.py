import json
import os
import subprocess
import uuid
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture()
def root(tmp_path: Path) -> Path:
    """A throwaway repo root that create-new-skill.sh accepts.

    The script resolves its root with `git rev-parse --show-toplevel`, so a git-init'd
    tmp_path is enough; everything else it touches under that root is listed here. These
    tests used to run against the real repository, which left a `layout-int-<uuid>` skill
    behind under `.specify/skills/.migration-backups/` on every run — 22 had accumulated,
    each one registering as an installed skill and each one keeping
    test_no_nested_skills.py permanently red.
    """
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".specify").mkdir()
    (tmp_path / ".specify" / "scripts").symlink_to(
        REPO_ROOT / ".specify" / "scripts", target_is_directory=True
    )
    (tmp_path / ".specify" / "templates").mkdir()
    (tmp_path / ".specify" / "templates" / "skills-template.md").write_bytes(
        (REPO_ROOT / "templates" / "skills-template.md").read_bytes()
    )
    (tmp_path / ".specify" / "skills").mkdir()
    (tmp_path / ".github").mkdir()
    return tmp_path


def _github_skills_is_global_symlink(root: Path) -> bool:
    github_skills = root / ".github" / "skills"
    primary_skills = root / ".specify" / "skills"
    return (
        github_skills.is_symlink()
        and github_skills.resolve() == primary_skills.resolve()
    )


def _run_create_skill(
    root: Path, skill_name: str, check: bool = True, env: dict | None = None
):
    script = root / ".specify" / "scripts" / "bash" / "create-new-skill.sh"
    merged_env = None
    if env:
        merged_env = dict(os.environ)
        merged_env.update(env)
    return subprocess.run(
        [str(script), "--json", f"{skill_name} - integration scenario"],
        cwd=root,
        env=merged_env,
        stdin=subprocess.DEVNULL,
        check=check,
        capture_output=True,
        text=True,
    )


def test_default_install_creates_primary_copy_and_compat_entrypoint(root: Path):
    skill_name = f"layout-int-{uuid.uuid4().hex[:8]}"
    primary_dir = root / ".specify" / "skills" / skill_name
    github_entry = root / ".github" / "skills" / skill_name

    payload = json.loads(_run_create_skill(root, skill_name).stdout)
    assert payload["status"] == "created"
    assert payload["primary_copy_status"] == "created"
    assert (primary_dir / "SKILL.md").exists()
    assert github_entry.exists()
    assert payload["entrypoint_github_mode"] in {"symlink", "placeholder"}

    payload_second = json.loads(_run_create_skill(root, skill_name).stdout)
    assert payload_second["status"] == "refreshed"
    assert payload_second["primary_copy_status"] == "reused"


def test_conflict_entrypoint_blocks_overwrite(root: Path):
    skill_name = f"layout-conflict-{uuid.uuid4().hex[:8]}"
    github_entry = root / ".github" / "skills" / skill_name
    github_entry.parent.mkdir(parents=True, exist_ok=True)
    github_entry.write_text("conflict", encoding="utf-8")

    result = _run_create_skill(root, skill_name, check=False)
    assert result.returncode != 0
    assert "conflict" in (result.stdout + result.stderr).lower()
    if result.stdout.strip():
        assert json.loads(result.stdout).get("code") == "conflict-entry-path"


def test_placeholder_fallback_mode_can_be_forced(root: Path):
    skill_name = f"layout-placeholder-{uuid.uuid4().hex[:8]}"
    github_entry = root / ".github" / "skills" / skill_name

    payload = json.loads(
        _run_create_skill(
            root, skill_name, env={"SPECIFY_FORCE_PLACEHOLDER": "1"}
        ).stdout
    )
    if _github_skills_is_global_symlink(root):
        assert payload["entrypoint_github_mode"] == "symlink"
        assert payload["entrypoint_github_reason"] == "parent-already-linked"
    else:
        assert payload["entrypoint_github_mode"] == "placeholder"
        assert (github_entry / "README.md").exists()


def test_legacy_directory_migrates_to_primary_copy(root: Path):
    skill_name = f"layout-migrate-{uuid.uuid4().hex[:8]}"
    legacy_dir = root / ".github" / "skills" / skill_name
    primary_dir = root / ".specify" / "skills" / skill_name

    if _github_skills_is_global_symlink(root):
        pytest.skip(
            "legacy per-skill migration is not applicable when .github/skills is a global symlink"
        )

    primary_dir.mkdir(parents=True)
    (primary_dir / "legacy-overwrite.txt").write_text("from-primary", encoding="utf-8")
    legacy_dir.mkdir(parents=True)
    (legacy_dir / "SKILL.md").write_text(
        "---\nname: demo\ndescription: demo\n---\n", encoding="utf-8"
    )
    (legacy_dir / "legacy-overwrite.txt").write_text("from-legacy", encoding="utf-8")
    (legacy_dir / "legacy-only.txt").write_text("moved", encoding="utf-8")

    payload = json.loads(_run_create_skill(root, skill_name).stdout)
    assert payload["migration_state"] == "completed"
    assert (primary_dir / "SKILL.md").exists()
    assert (
        primary_dir / "legacy-overwrite.txt"
    ).read_text(encoding="utf-8") == "from-legacy"
    assert (primary_dir / "legacy-only.txt").exists()
    assert legacy_dir.is_symlink() or (
        legacy_dir / ".specify-skill-placeholder"
    ).exists()


def test_legacy_backup_failure_marks_manual_required(root: Path):
    skill_name = f"layout-backup-fail-{uuid.uuid4().hex[:8]}"
    legacy_dir = root / ".github" / "skills" / skill_name

    legacy_dir.mkdir(parents=True)
    (legacy_dir / "SKILL.md").write_text(
        "---\nname: demo\ndescription: demo\n---\n", encoding="utf-8"
    )

    payload = json.loads(
        _run_create_skill(
            root, skill_name, env={"SPECIFY_FORCE_BACKUP_FAIL": "1"}
        ).stdout
    )
    assert payload["overall_status"] == "partial-success"
    assert payload["migration_state"] == "manual-required"
    assert legacy_dir.exists()
