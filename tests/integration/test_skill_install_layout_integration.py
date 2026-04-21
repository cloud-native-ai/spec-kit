import json
import shutil
import subprocess
import uuid
from pathlib import Path


def _run_create_skill(
    root: Path, skill_name: str, check: bool = True, env: dict | None = None
):
    script = root / ".specify" / "scripts" / "bash" / "create-new-skill.sh"
    merged_env = None
    if env:
        merged_env = dict(**__import__("os").environ)
        merged_env.update(env)
    return subprocess.run(
        [
            str(script),
            "--json",
            f"{skill_name} - integration scenario",
        ],
        cwd=root,
        env=merged_env,
        stdin=subprocess.DEVNULL,
        check=check,
        capture_output=True,
        text=True,
    )


def test_default_install_creates_primary_copy_and_compat_entrypoint():
    root = Path(__file__).resolve().parents[2]
    skill_name = f"layout-int-{uuid.uuid4().hex[:8]}"
    primary_dir = root / ".specify" / "skills" / skill_name
    github_entry = root / ".github" / "skills" / skill_name

    try:
        result = _run_create_skill(root, skill_name, check=True)
        payload = json.loads(result.stdout)

        assert payload["status"] == "created"
        assert payload["primary_copy_status"] == "created"
        assert primary_dir.exists()
        assert (primary_dir / "SKILL.md").exists()
        assert github_entry.exists()
        assert payload["entrypoint_github_mode"] in {"symlink", "placeholder"}

        result_second = _run_create_skill(root, skill_name, check=True)
        payload_second = json.loads(result_second.stdout)
        assert payload_second["status"] == "refreshed"
        assert payload_second["primary_copy_status"] == "reused"
    finally:
        shutil.rmtree(primary_dir, ignore_errors=True)
        if github_entry.is_symlink() or github_entry.is_file():
            github_entry.unlink(missing_ok=True)
        else:
            shutil.rmtree(github_entry, ignore_errors=True)


def test_conflict_entrypoint_blocks_overwrite():
    root = Path(__file__).resolve().parents[2]
    skill_name = f"layout-conflict-{uuid.uuid4().hex[:8]}"
    github_entry = root / ".github" / "skills" / skill_name

    try:
        github_entry.parent.mkdir(parents=True, exist_ok=True)
        github_entry.write_text("conflict", encoding="utf-8")

        result = _run_create_skill(root, skill_name, check=False)
        assert result.returncode != 0
        assert "conflict" in (result.stdout + result.stderr).lower()
        if result.stdout.strip():
            payload = json.loads(result.stdout)
            assert payload.get("code") == "conflict-entry-path"
    finally:
        if github_entry.exists() or github_entry.is_symlink():
            github_entry.unlink(missing_ok=True)
        primary_dir = root / ".specify" / "skills" / skill_name
        shutil.rmtree(primary_dir, ignore_errors=True)


def test_placeholder_fallback_mode_can_be_forced():
    root = Path(__file__).resolve().parents[2]
    skill_name = f"layout-placeholder-{uuid.uuid4().hex[:8]}"
    primary_dir = root / ".specify" / "skills" / skill_name
    github_entry = root / ".github" / "skills" / skill_name

    try:
        result = _run_create_skill(
            root, skill_name, check=True, env={"SPECIFY_FORCE_PLACEHOLDER": "1"}
        )
        payload = json.loads(result.stdout)

        assert payload["entrypoint_github_mode"] == "placeholder"
        assert (github_entry / "README.md").exists()
    finally:
        shutil.rmtree(primary_dir, ignore_errors=True)
        if github_entry.is_symlink() or github_entry.is_file():
            github_entry.unlink(missing_ok=True)
        else:
            shutil.rmtree(github_entry, ignore_errors=True)


def test_legacy_directory_migrates_to_primary_copy():
    root = Path(__file__).resolve().parents[2]
    skill_name = f"layout-migrate-{uuid.uuid4().hex[:8]}"
    legacy_dir = root / ".github" / "skills" / skill_name
    primary_dir = root / ".specify" / "skills" / skill_name

    try:
        primary_dir.mkdir(parents=True, exist_ok=False)
        (primary_dir / "legacy-overwrite.txt").write_text(
            "from-primary", encoding="utf-8"
        )

        legacy_dir.mkdir(parents=True, exist_ok=False)
        (legacy_dir / "SKILL.md").write_text(
            "---\nname: demo\ndescription: demo\n---\n", encoding="utf-8"
        )
        (legacy_dir / "legacy-overwrite.txt").write_text(
            "from-legacy", encoding="utf-8"
        )
        (legacy_dir / "legacy-only.txt").write_text("moved", encoding="utf-8")

        result = _run_create_skill(root, skill_name, check=True)
        payload = json.loads(result.stdout)

        assert payload["migration_state"] == "completed"
        assert primary_dir.exists()
        assert (primary_dir / "SKILL.md").exists()
        assert (primary_dir / "legacy-overwrite.txt").read_text(
            encoding="utf-8"
        ) == "from-legacy"
        assert (primary_dir / "legacy-only.txt").exists()
        assert (
            legacy_dir.is_symlink()
            or (legacy_dir / ".specify-skill-placeholder").exists()
        )
    finally:
        shutil.rmtree(primary_dir, ignore_errors=True)
        if legacy_dir.is_symlink() or legacy_dir.is_file():
            legacy_dir.unlink(missing_ok=True)
        else:
            shutil.rmtree(legacy_dir, ignore_errors=True)


def test_legacy_backup_failure_marks_manual_required():
    root = Path(__file__).resolve().parents[2]
    skill_name = f"layout-backup-fail-{uuid.uuid4().hex[:8]}"
    legacy_dir = root / ".github" / "skills" / skill_name
    primary_dir = root / ".specify" / "skills" / skill_name

    try:
        legacy_dir.mkdir(parents=True, exist_ok=False)
        (legacy_dir / "SKILL.md").write_text(
            "---\nname: demo\ndescription: demo\n---\n", encoding="utf-8"
        )

        result = _run_create_skill(
            root, skill_name, check=True, env={"SPECIFY_FORCE_BACKUP_FAIL": "1"}
        )
        payload = json.loads(result.stdout)

        assert payload["overall_status"] == "partial-success"
        assert payload["migration_state"] == "manual-required"
        assert legacy_dir.exists()
    finally:
        shutil.rmtree(primary_dir, ignore_errors=True)
        if legacy_dir.is_symlink() or legacy_dir.is_file():
            legacy_dir.unlink(missing_ok=True)
        else:
            shutil.rmtree(legacy_dir, ignore_errors=True)
