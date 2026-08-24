"""Contract tests: framework distribution exclusions for browser-utils site memory.

Contract: .specify/specs/046-browser-site-memory/contracts/framework-exclusions.md
Requirement 046 / Feature 048 — site/ runtime data must never be committed to
git (X-1/X-2), mirrored by sync-mirrors (X-3/X-4), or shipped in the wheel
(X-5/X-6/X-7; sdist covered by gitignore per X-8).
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

GITIGNORE_LINES = (
    "skills/browser-utils/site/",
    ".specify/skills/browser-utils/site/",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------- X-1 / X-2


class TestGitignoreExclusion:
    def test_gitignore_carries_both_site_lines(self):
        text = _read(REPO_ROOT / ".gitignore")
        for line in GITIGNORE_LINES:
            assert line in text.splitlines(), f".gitignore missing: {line}"

    @pytest.mark.parametrize(
        "probe",
        [
            "skills/browser-utils/site/probe.json",
            ".specify/skills/browser-utils/site/probe.json",
        ],
    )
    def test_git_check_ignore_hits_probe(self, probe):
        proc = subprocess.run(
            ["git", "check-ignore", "-v", probe],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, (
            f"git check-ignore did not match {probe}: {proc.stdout}{proc.stderr}"
        )


# ---------------------------------------------------------------- X-3 / X-4


class TestMirrorSyncExclusion:
    @pytest.mark.parametrize(
        "path",
        [
            "scripts/python/sync-mirrors.py",
            ".specify/scripts/python/sync-mirrors.py",
        ],
    )
    def test_skills_pair_excludes_site_component(self, path):
        text = _read(REPO_ROOT / path)
        match = re.search(
            r'\("skills",\s*"\.specify/skills",\s*\w+,\s*\{([^}]*)\}\)', text
        )
        assert match, f"skills mirror pair not found in {path}"
        excluded = {p.strip().strip('"').strip("'") for p in match.group(1).split(",") if p.strip()}
        assert "site" in excluded, f"skills pair exclude_parts lacks 'site': {excluded}"

    def test_mirror_check_ignores_site_probe(self, tmp_path):
        probe = REPO_ROOT / "skills" / "browser-utils" / "site" / "probe.json"
        probe.parent.mkdir(parents=True, exist_ok=True)
        probe.write_text('{"probe": true}\n', encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, "scripts/python/sync-mirrors.py", "--check"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            # X-4: with the probe present, the skills pair stays clean — the
            # checker must not report any site/ entry on either side.
            combined = proc.stdout + proc.stderr
            offenders = [
                line for line in combined.splitlines()
                if "browser-utils/site" in line or "skills/site" in line
            ]
            assert not offenders, f"sync-mirrors reported site/ entries: {offenders}"
            assert "ok    skills/" in proc.stdout, (
                f"skills pair not reported clean:\n{proc.stdout}\n{proc.stderr}"
            )
        finally:
            probe.unlink(missing_ok=True)
            try:
                probe.parent.rmdir()
            except OSError:
                pass


# ---------------------------------------------------------------- X-5 / X-7


class TestWheelExclusion:
    def test_pyproject_has_no_static_skills_force_include(self):
        text = _read(REPO_ROOT / "pyproject.toml")
        section = re.search(
            r"\[tool\.hatch\.build\.targets\.wheel\.force-include\](.*?)(?=\n\[|\Z)",
            text,
            re.DOTALL,
        )
        body = section.group(1) if section else ""
        assert not re.search(r'^\s*"skills"\s*=', body, re.MULTILINE), (
            'pyproject still force-includes the whole "skills" dir statically'
        )

    def test_hatch_build_stages_skills_without_site(self):
        text = _read(REPO_ROOT / "src" / "hatch_build.py")
        assert "force_include" in text, "hatch_build.py must register force_include"
        assert "site" in text, "hatch_build.py must filter the 'site' path component"

    @pytest.mark.skipif(shutil.which("python3") is None, reason="no python3")
    def test_wheel_build_excludes_site_probe(self):
        probe = REPO_ROOT / "skills" / "browser-utils" / "site" / "probe.json"
        probe.parent.mkdir(parents=True, exist_ok=True)
        probe.write_text('{"probe": true}\n', encoding="utf-8")
        try:
            build = subprocess.run(
                [sys.executable, "-m", "hatchling", "build", "-t", "wheel"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=300,
            )
            assert build.returncode == 0, f"wheel build failed:\n{build.stderr[-2000:]}"
            wheels = sorted((REPO_ROOT / "dist").glob("specify_cli-*.whl"))
            assert wheels, "no wheel produced"
            names = zipfile.ZipFile(wheels[-1]).namelist()
            leaked = [n for n in names if "/skills/browser-utils/site/" in n]
            assert not leaked, f"wheel leaked site/ entries: {leaked}"
            assert "specify_cli/skills/browser-utils/SKILL.md" in names, (
                "wheel lost browser-utils SKILL.md — staging copy dropped real content"
            )
        finally:
            probe.unlink(missing_ok=True)
            try:
                probe.parent.rmdir()
            except OSError:
                pass
            for whl in (REPO_ROOT / "dist").glob("specify_cli-*.whl"):
                whl.unlink(missing_ok=True)
