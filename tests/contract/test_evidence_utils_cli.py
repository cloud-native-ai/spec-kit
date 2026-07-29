"""Contract tests for evidence-utils.py CLI surface (spec 034, contracts/evidence-utils-cli.md C-E1..C-E11)."""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / ".specify" / "scripts" / "python" / "evidence-utils.py"
MIRROR = REPO_ROOT / "scripts" / "python" / "evidence-utils.py"

ACTIONS = ["doctor", "collect", "list", "latest", "compare"]


def run_cli(*args, cwd=None):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd or REPO_ROOT),
        timeout=300,
    )


# --- C-E1: invocation shape -------------------------------------------------

class TestCE1InvocationShape:
    def test_script_exists(self):
        assert SCRIPT.is_file(), f"missing {SCRIPT}"

    def test_action_required(self):
        result = run_cli()
        assert result.returncode == 2

    def test_unknown_action_rejected(self):
        result = run_cli("--action", "nonsense")
        assert result.returncode == 2

    def test_doctor_outputs_json_with_trailing_newline(self):
        result = run_cli("--action", "doctor")
        assert result.returncode == 0, result.stderr
        assert result.stdout.endswith("\n")
        json.loads(result.stdout)


# --- C-E2: stdlib-only, no shell, no network --------------------------------

class TestCE2StaticSafety:
    def read_source(self):
        return SCRIPT.read_text(encoding="utf-8")

    def test_no_shell_true(self):
        assert "shell=True" not in self.read_source()

    def test_no_network_calls(self):
        source = self.read_source()
        for marker in ("urllib.request", "urlopen(", "http.client", "requests.", "socket.create_connection"):
            assert marker not in source, f"network marker found: {marker}"

    def test_stdlib_only_imports(self):
        source = self.read_source()
        stdlib_allow = {
            "argparse", "json", "hashlib", "os", "re", "subprocess", "sys",
            "datetime", "pathlib", "shutil", "typing", "collections", "textwrap",
        }
        for match in re.finditer(r"^(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_]*)", source, re.M):
            assert match.group(1) in stdlib_allow, f"unexpected import: {match.group(1)}"


# --- C-E3: doctor ------------------------------------------------------------

class TestCE3Doctor:
    @pytest.fixture(scope="class")
    def doctor(self):
        result = run_cli("--action", "doctor")
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)

    def test_node_block(self, doctor):
        assert "node" in doctor
        assert isinstance(doctor["node"]["available"], bool)
        assert isinstance(doctor["node"]["satisfies"], bool)

    def test_engine_subset_block(self, doctor):
        assert doctor["engineSubset"]["present"] is True
        assert "better-harness" in doctor["engineSubset"]["path"]
        assert doctor["engineSubset"]["upstreamCommit"] == "b2e621d"

    def test_platforms_block_covers_eight_tools(self, doctor):
        expected = {"qoder", "codex", "claude", "copilot", "opencode", "qwen", "hermes", "iflow"}
        assert expected.issubset(set(doctor["platforms"].keys()))
        for name, info in doctor["platforms"].items():
            assert info["sessionStore"] in ("detected", "not-detected"), name

    def test_lanes_block(self, doctor):
        assert set(doctor["lanes"].keys()) == {"session", "project", "assets", "runs", "feedback"}

    def test_doctor_is_side_effect_free(self, tmp_path):
        before = sorted((REPO_ROOT / ".specify" / "memory" / "evidence").glob("*"))
        run_cli("--action", "doctor")
        after = sorted((REPO_ROOT / ".specify" / "memory" / "evidence").glob("*"))
        assert before == after


# --- C-E4: collect (behavioural surface tested via tmp workspace) ------------

class TestCE4Collect:
    def test_target_required(self):
        result = run_cli("--action", "collect")
        assert result.returncode != 0

    def test_collect_produces_run_dir(self, tmp_path):
        workspace = make_min_workspace(tmp_path)
        result = run_cli("--action", "collect", "--target", "project",
                         "--lanes", "runs,feedback", cwd=workspace)
        assert result.returncode == 0, result.stderr
        out = json.loads(result.stdout)
        assert re.match(r"^ev-\d{8}-\d{6}-[a-z0-9-]+$", out["runId"])
        run_dir = workspace / out["path"] if not Path(out["path"]).is_absolute() else Path(out["path"])
        assert (run_dir / "findings.json").is_file()
        assert (run_dir / "manifest.json").is_file()
        assert out["findingsDigest"].startswith("sha256:")


# --- C-E5 / C-E6: list & latest ----------------------------------------------

class TestCE5CE6ListLatest:
    def test_list_empty_store(self, tmp_path):
        workspace = make_min_workspace(tmp_path)
        result = run_cli("--action", "list", cwd=workspace)
        assert result.returncode == 0
        assert json.loads(result.stdout)["entries"] == []

    def test_latest_not_found(self, tmp_path):
        workspace = make_min_workspace(tmp_path)
        result = run_cli("--action", "latest", "--target", "project", cwd=workspace)
        assert result.returncode == 0
        assert json.loads(result.stdout)["found"] is False

    def test_latest_after_collect(self, tmp_path):
        workspace = make_min_workspace(tmp_path)
        run_cli("--action", "collect", "--target", "project", "--lanes", "feedback", cwd=workspace)
        result = run_cli("--action", "latest", "--target", "project", cwd=workspace)
        payload = json.loads(result.stdout)
        assert payload["found"] is True
        assert payload["stale"] is False


# --- C-E7: compare error path -------------------------------------------------

class TestCE7CompareErrors:
    def test_compare_missing_runs_exits_1(self, tmp_path):
        workspace = make_min_workspace(tmp_path)
        result = run_cli("--action", "compare", "--target", "project",
                         "--baseline", "ev-20200101-000000-x", cwd=workspace)
        assert result.returncode == 1
        assert "error" in json.loads(result.stdout)


# --- C-E11 / mirror -----------------------------------------------------------

class TestMirror:
    def test_mirror_identical(self):
        assert MIRROR.is_file(), "scripts/python mirror missing"
        assert MIRROR.read_bytes() == SCRIPT.read_bytes()


def make_min_workspace(tmp_path: Path) -> Path:
    """Minimal .specify workspace so lanes can run without the real repo."""
    workspace = tmp_path / "ws"
    (workspace / ".specify" / "memory" / "feedback").mkdir(parents=True)
    (workspace / ".specify" / "memory" / "evidence").mkdir(parents=True)
    (workspace / ".specify" / "teams").mkdir(parents=True)
    return workspace
