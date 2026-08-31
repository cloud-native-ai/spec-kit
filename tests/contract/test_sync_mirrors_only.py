"""Contract test: sync-mirrors.py --only path-prefix scoping (review 047 F4).

--only restricts a run to the given repo-relative prefix so feature-scoped
syncs never drag unrelated mirror drift into the change surface.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = "scripts/python/sync-mirrors.py"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, SCRIPT, *args], cwd=REPO_ROOT,
        capture_output=True, text=True)


@pytest.mark.contract
class TestOnlyScoping:
    def test_only_file_scopes_check_to_its_pair(self):
        proc = _run("--only", "scripts/python/feedback-utils.py", "--check")
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "scripts/" in proc.stdout
        # other pairs and the regen delegation stay out of scope
        assert "templates/" not in proc.stdout
        assert "skills/" not in proc.stdout
        assert "agents/" not in proc.stdout

    def test_only_write_syncs_nothing_outside_prefix(self):
        # scratch canonical file inside templates/ (in-scope prefix) — the
        # write run must touch ONLY that file's mirror, nothing else.
        scratch = REPO_ROOT / "templates" / "sync-only-probe.md"
        mirror = REPO_ROOT / ".specify" / "templates" / "sync-only-probe.md"
        scratch.write_text("probe\n", encoding="utf-8")
        try:
            proc = _run("--only", "templates/sync-only-probe.md", "--write")
            assert proc.returncode == 0, proc.stdout + proc.stderr
            assert mirror.read_text(encoding="utf-8") == "probe\n"
            assert "skills/" not in proc.stdout
            assert "agents/" not in proc.stdout
        finally:
            scratch.unlink(missing_ok=True)
            mirror.unlink(missing_ok=True)

    def test_only_unknown_prefix_errors(self):
        proc = _run("--only", "no/such/prefix", "--check")
        assert proc.returncode == 2
        assert "no/such/prefix" in (proc.stdout + proc.stderr)
