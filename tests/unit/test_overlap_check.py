"""Unit tests for overlap-check.py (cross-feature delivery overlap gate)."""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "overlap-check.py"


def _spec(root, name, *declarations):
    spec = root / name
    spec.mkdir(parents=True)
    lines = ["# Feature Reference", "", "## Delivered paths", ""]
    lines += ["- `%s`" % item for item in declarations]
    (spec / "feature-ref.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (spec / "requirements.md").write_text("# Requirements\n", encoding="utf-8")
    return spec


def _run(spec, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--spec-dir", str(spec), *args],
        capture_output=True, text=True)


def _record(proc):
    return json.loads(proc.stdout)


def test_no_overlap_passes(tmp_path):
    alpha = _spec(tmp_path, "001-alpha", "skills/external/shared/references/a.md")
    _spec(tmp_path, "002-beta", "docs/reference/other.md")
    proc = _run(alpha)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    record = _record(proc)
    assert record["decision"] == "clear"
    assert record["overlaps"] == []


def test_same_path_overlap_fails(tmp_path):
    alpha = _spec(tmp_path, "001-alpha", "skills/external/demo/references/cli/qodercli.md")
    _spec(tmp_path, "002-beta", "skills/external/demo/references/cli/qodercli.md")
    proc = _run(alpha)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    record = _record(proc)
    assert record["decision"] == "overlap"
    assert len(record["overlaps"]) == 1
    overlap = record["overlaps"][0]
    assert overlap["other_spec"] == "002-beta"
    assert overlap["relation"] == "same-path"


def test_nested_path_overlap_fails(tmp_path):
    alpha = _spec(tmp_path, "001-alpha", "skills/external/demo/references/cli/")
    _spec(tmp_path, "002-beta", "skills/external/demo/references/cli/qodercli.md")
    proc = _run(alpha)
    assert proc.returncode == 1
    assert _record(proc)["overlaps"][0]["relation"] == "nested-path"


def test_spec_internal_paths_are_ignored(tmp_path):
    alpha = _spec(tmp_path, "001-alpha",
                  ".specify/specs/001-alpha/notes/a.md",
                  "skills/external/alpha-only/a.md")
    _spec(tmp_path, "002-beta", ".specify/specs/001-alpha/notes/a.md")
    proc = _run(alpha)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_empty_declaration_is_clear(tmp_path):
    alpha = _spec(tmp_path, "001-alpha")
    _spec(tmp_path, "002-beta", "skills/external/demo/a.md")
    proc = _run(alpha)
    assert proc.returncode == 0
    record = _record(proc)
    assert record["decision"] == "clear"
    assert "no shared delivery paths" in record["note"]


def test_missing_spec_dir_is_input_error(tmp_path):
    proc = _run(tmp_path / "absent")
    assert proc.returncode == 2
    assert "spec dir not found" in proc.stderr


def test_repo_relativization_skips_own_spec(tmp_path):
    specs = tmp_path / ".specify" / "specs"
    alpha = _spec(specs, "001-alpha", "skills/external/demo/a.md")
    _spec(specs, "002-beta", "skills/external/demo/a.md")
    proc = _run(alpha, "--repo", str(tmp_path))
    assert proc.returncode == 1
    assert _record(proc)["current_paths"] == ["skills/external/demo/a.md"]


def test_checked_specs_excludes_current(tmp_path):
    alpha = _spec(tmp_path, "001-alpha", "skills/external/alpha/a.md")
    _spec(tmp_path, "002-beta", "docs/other.md")
    proc = _run(alpha)
    record = _record(proc)
    assert record["checked_specs"] == ["001-alpha", "002-beta"]
    assert all(o["other_spec"] != "001-alpha" for o in record["overlaps"])


def test_delivered_surface_uses_commit_messages(tmp_path):
    """A finished feature's delivery surface comes from commits that name the
    spec, so a cited input is not mistaken for a deliverable."""
    import subprocess as sp
    repo = tmp_path
    sp.run(["git", "-C", str(repo), "init", "-q"], check=True)
    sp.run(["git", "-C", str(repo), "-c", "user.name=t",
            "-c", "user.email=t@example.com", "commit", "--allow-empty",
            "-q", "-m", "init"], check=True)
    alpha = _spec(repo / ".specify" / "specs", "001-alpha",
                  "skills/external/demo/shared.md")
    beta = _spec(repo / ".specify" / "specs", "002-beta", "docs/other.md")
    delivered = repo / "skills" / "external" / "demo" / "shared.md"
    delivered.parent.mkdir(parents=True)
    delivered.write_text("delivered by 002\n", encoding="utf-8")
    sp.run(["git", "-C", str(repo), "add", "-A"], check=True)
    sp.run(["git", "-C", str(repo), "-c", "user.name=t",
            "-c", "user.email=t@example.com", "commit", "-q",
            "-m", "feat(002-beta): deliver the shared file"], check=True)
    proc = _run(alpha, "--repo", str(repo))
    assert proc.returncode == 1, proc.stdout + proc.stderr
    overlap = _record(proc)["overlaps"][0]
    assert overlap["other_spec"] == "002-beta"
    assert overlap["other_path"] == "skills/external/demo/shared.md"
