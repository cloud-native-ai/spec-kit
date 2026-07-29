"""Contract tests for the findings.json evidence contract (spec 034, contracts/findings-contract.md C-F1..C-F14)."""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / ".specify" / "scripts" / "python" / "evidence-utils.py"

TOP_LEVEL_WHITELIST = {
    "schemaVersion", "kind", "target", "runId", "window",
    "platforms", "lanes", "evidence", "findingsDigest",
}
SEVEN_STATES = {
    "Present", "Wired", "Exercised", "Outcome-supported",
    "Missing", "Unobserved", "Not applicable",
}
LANE_NAMES = {"session", "project", "assets", "runs", "feedback"}
LANE_STATUS = {"available", "partial", "unavailable"}
VERDICT_KEY_BLACKLIST = {
    "severity", "score", "scores", "aiFixPrompt", "recommendation",
    "supportTrack", "priority",
}
SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"ghp_[A-Za-z0-9]{36}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"sk-[A-Za-z0-9]{20,}",
]


def collect_fixture(tmp_path: Path, lanes: str = "runs,feedback") -> dict:
    """Run a real collect in an isolated workspace and load its artifacts."""
    workspace = tmp_path / "ws"
    feedback_dir = workspace / ".specify" / "memory" / "feedback"
    feedback_dir.mkdir(parents=True)
    (workspace / ".specify" / "memory" / "evidence").mkdir(parents=True)
    team = workspace / ".specify" / "teams" / "demo-team"
    (team / "runs").mkdir(parents=True)
    (team / "runs" / "20260101T000000Z-report.md").write_text("# report\nok\n", encoding="utf-8")
    (team / "STATE.md").write_text(
        "# Team State — demo-team\nLast cycle: 2026-01-01T00:00:00Z   Maturity: L1   Cadence: 2h\n\n"
        "## High Priority\n\n## Watch List\n\n## Recent Noise\n\n"
        "## Post-Run Critique (每 cycle 追加，用于晋级判据)\n- 2026-01-01T00:00:00Z: ok / 误报=0\n",
        encoding="utf-8",
    )
    (team / "run-log.jsonl").write_text(
        json.dumps({"cycle": "2026-01-01T00:00:00Z", "maturity": "L1", "items_found": 2,
                    "actions_taken": 1, "escalations": 0, "tokens_estimate": 1000,
                    "outcome": "report-only"}) + "\n",
        encoding="utf-8",
    )
    entry = feedback_dir / "20260101T000000Z-skill-demo.md"
    entry.write_text(
        "---\nid: 20260101T000000Z-skill-demo\nunit_id: skill:demo\nunit_type: skill\n"
        "run_id: r1\nscope: local\nfeature: \"\"\npartial: false\ncreated: 2026-01-01T00:00:00Z\n"
        "summary: demo\n---\n\n## Review\nok\n\n## Optimization Points\n- tighten step 3\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--action", "collect", "--target", "project",
         "--lanes", lanes],
        capture_output=True, text=True, cwd=str(workspace), timeout=300,
    )
    assert result.returncode == 0, result.stderr
    out = json.loads(result.stdout)
    run_dir = (workspace / out["path"]) if not Path(out["path"]).is_absolute() else Path(out["path"])
    findings = json.loads((run_dir / "findings.json").read_text(encoding="utf-8"))
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    index = json.loads((workspace / ".specify" / "memory" / "evidence" / "index.json").read_text(encoding="utf-8"))
    return {"findings": findings, "manifest": manifest, "index": index,
            "run_dir": run_dir, "workspace": workspace}


@pytest.fixture(scope="module")
def artifacts(tmp_path_factory):
    return collect_fixture(tmp_path_factory.mktemp("evidence"))


class TestCF1TopLevel:
    def test_exact_field_whitelist(self, artifacts):
        assert set(artifacts["findings"].keys()) == TOP_LEVEL_WHITELIST

    def test_schema_and_kind(self, artifacts):
        assert artifacts["findings"]["schemaVersion"] == 1
        assert artifacts["findings"]["kind"] == "speckit.evidence-findings"


class TestCF2CF3Identifiers:
    def test_target_vocabulary(self, artifacts):
        assert re.match(r"^(skill:[a-z0-9._-]+|/speckit\.[a-z0-9._-]+|project)$",
                        artifacts["findings"]["target"])

    def test_run_id_format_and_consistency(self, artifacts):
        run_id = artifacts["findings"]["runId"]
        assert re.match(r"^ev-\d{8}-\d{6}-[a-z0-9-]+$", run_id)
        assert artifacts["manifest"]["runId"] == run_id
        assert artifacts["run_dir"].name == run_id


class TestCF4CF5Enums:
    def test_evidence_state_enum_closed(self, artifacts):
        for item in artifacts["findings"]["evidence"]:
            assert item["evidenceState"] in SEVEN_STATES, item["evidenceState"]

    def test_lanes_five_keys_and_status(self, artifacts):
        lanes = artifacts["findings"]["lanes"]
        assert set(lanes.keys()) == LANE_NAMES
        for lane, info in lanes.items():
            assert info["status"] in LANE_STATUS, lane


class TestCF6VerdictBan:
    def _walk_keys(self, node):
        if isinstance(node, dict):
            for key, value in node.items():
                yield key
                yield from self._walk_keys(value)
        elif isinstance(node, list):
            for value in node:
                yield from self._walk_keys(value)

    def test_no_verdict_keys_recursively(self, artifacts):
        keys = set(self._walk_keys(artifacts["findings"]))
        assert not (keys & VERDICT_KEY_BLACKLIST), keys & VERDICT_KEY_BLACKLIST


class TestCF7Privacy:
    def test_no_secret_patterns(self, artifacts):
        text = json.dumps(artifacts["findings"], ensure_ascii=False)
        for pattern in SECRET_PATTERNS:
            assert not re.search(pattern, text), pattern

    def test_no_home_absolute_paths_in_evidence(self, artifacts):
        for item in artifacts["findings"]["evidence"]:
            body = json.dumps(
                {"summary": item["summary"], "evidenceRefs": item["evidenceRefs"]},
                ensure_ascii=False)
            assert "/home/" not in body and "/Users/" not in body, body


class TestCF8Digest:
    def test_digest_format_and_cross_consistency(self, artifacts):
        digest = artifacts["findings"]["findingsDigest"]
        assert re.match(r"^sha256:[0-9a-f]{64}$", digest)
        assert artifacts["manifest"]["findingsDigest"] == digest


class TestCF9EvidenceItems:
    def test_item_fields(self, artifacts):
        seen = set()
        for pos, item in enumerate(artifacts["findings"]["evidence"], start=1):
            assert re.match(r"^ev-\d{3}$", item["id"])
            assert item["id"] not in seen
            seen.add(item["id"])
            assert item["id"] == f"ev-{pos:03d}", "ids must be sequential from 001"
            assert item["lane"] in LANE_NAMES
            assert isinstance(item["summary"], str) and item["summary"]
            assert isinstance(item["evidenceRefs"], list)
            assert isinstance(item["signals"], dict)
            for value in item["signals"].values():
                assert isinstance(value, (int, float))


class TestCF10CF11Manifest:
    def test_manifest_required_fields(self, artifacts):
        manifest = artifacts["manifest"]
        for field in ("runId", "target", "created", "lanes", "engine", "findingsDigest"):
            assert field in manifest, field
        assert "engineSubsetPath" in manifest["engine"]
        assert "upstreamCommit" in manifest["engine"]

    def test_unavailable_lanes_have_reason_and_no_lane_file(self, artifacts):
        for lane, info in artifacts["manifest"]["lanes"].items():
            lane_file = artifacts["run_dir"] / "lanes" / f"{lane}.json"
            if info["status"] == "unavailable":
                assert info.get("reason"), f"{lane} missing reason"
                assert not lane_file.exists(), f"{lane} unavailable but lane file exists"
            else:
                assert lane_file.is_file(), f"{lane} executed but lane file missing"


class TestCF12Index:
    def test_index_structure(self, artifacts):
        index = artifacts["index"]
        assert index["store"] == "evidence"
        assert index["entries"], "collect must append an index entry"
        entry = index["entries"][-1]
        for field in ("runId", "target", "created", "lanesSummary", "file"):
            assert field in entry, field


class TestCF13FeedbackPackageExclusion:
    def test_package_zip_contains_no_evidence_paths(self, artifacts):
        workspace = artifacts["workspace"]
        feedback_utils = REPO_ROOT / ".specify" / "scripts" / "python" / "feedback-utils.py"
        subprocess.run(
            [sys.executable, str(feedback_utils), "--action", "reindex",
             "--workspace-root", str(workspace)],
            capture_output=True, text=True, cwd=str(workspace), timeout=120,
        )
        result = subprocess.run(
            [sys.executable, str(feedback_utils), "--action", "package", "--all",
             "--workspace-root", str(workspace)],
            capture_output=True, text=True, cwd=str(workspace), timeout=120,
        )
        assert result.returncode == 0, result.stderr
        packages_dir = workspace / ".specify" / "memory" / "feedback" / "packages"
        zips = sorted(packages_dir.glob("feedback-*.zip"))
        assert zips, "package produced no zip in the isolated workspace"
        import zipfile
        names = zipfile.ZipFile(zips[-1]).namelist()
        assert not [n for n in names if "evidence" in n], names
