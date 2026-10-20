"""Contract tests for contracts/cli-profiles.md (CLP-01…CLP-17)."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
CLI_DIR = SKILL_DIR / "references" / "cli"
MIRROR_CLI_DIR = REPO_ROOT / ".specify" / "skills" / "sdd-loop-driver" / "references" / "cli"
PROFILES = ["qodercli", "claude", "codex", "opencode", "hermes"]
DIMENSIONS = [
    "invocation", "output_mode", "timeouts", "sentinel",
    "buffering", "session_logs", "detach_signals", "defects_versions",
]
DOCS = REPO_ROOT / "docs" / "reference" / "skills" / "sdd-loop-driver.md"
PROBE_DEFS = REPO_ROOT / "shared" / "definitions" / "probe-definitions.md"


def _profile(name: str) -> str:
    return (CLI_DIR / f"{name}.md").read_text(encoding="utf-8")


def _dimension_rows(text: str) -> dict[str, dict[str, str]]:
    rows = {}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        if cells[0] in DIMENSIONS:
            rows[cells[0]] = {
                "status": cells[1], "value": cells[2], "observed_at": cells[3],
                "cli_version": cells[4], "evidence_ptr": cells[5],
            }
    return rows


def test_clp_01_profile_set_and_location():
    assert CLI_DIR.is_dir()
    assert (CLI_DIR / "index.md").exists()
    for name in PROFILES:
        assert (CLI_DIR / f"{name}.md").exists(), f"missing profile: {name}"
    text = (CLI_DIR / "index.md").read_text(encoding="utf-8")
    for name in PROFILES:
        assert name in text


def test_clp_02_eight_dimensions():
    index = (CLI_DIR / "index.md").read_text(encoding="utf-8")
    for dimension in DIMENSIONS:
        assert dimension in index, f"schema index missing dimension: {dimension}"
    for name in PROFILES:
        rows = _dimension_rows(_profile(name))
        assert set(rows) == set(DIMENSIONS), f"{name}: dimensions {sorted(rows)}"


def test_clp_03_known_unknown_provenance():
    for name in PROFILES:
        text = _profile(name)
        assert "## Provenance" in text, f"{name}: provenance section missing"
        assert re.search(r"\|\s*date\s*\|\s*trigger\s*\|\s*observation\s*\|\s*change\s*\|\s*feedback_id\s*\|", text), (
            f"{name}: provenance table header missing"
        )
        rows = _dimension_rows(text)
        for dimension, row in rows.items():
            assert row["status"] in {"known", "unknown"}, f"{name}/{dimension}: bad status"
            if row["status"] == "known":
                for field in ("observed_at", "cli_version", "evidence_ptr"):
                    assert row[field] and row[field] not in {"-", "unknown"}, (
                        f"{name}/{dimension}: known row lacks {field}"
                    )
            else:
                assert row["value"] in {"-", "unknown"}, (
                    f"{name}/{dimension}: unknown row must not carry a guessed value"
                )


def test_clp_04_qodercli_initial_facts():
    text = _profile("qodercli")
    for needle in [
        "BASH_DEFAULT_TIMEOUT_MS", "BASH_MAX_TIMEOUT_MS", "600,000",
        "stream-json", "~/.qoder/logs/", "缓冲", "脱离",
    ]:
        assert needle in text, f"qodercli fact missing: {needle}"
    rows = _dimension_rows(text)
    assert rows["timeouts"]["status"] in {"known", "unknown"}
    # 0/negative semantics are not measured: the row must say unknown or name it.
    assert "0/负值" in text or "0 / 负值" in text or "0/negative" in text


def test_clp_05_skeleton_discipline():
    for name in ["claude", "codex", "opencode", "hermes"]:
        rows = _dimension_rows(_profile(name))
        assert all(row["status"] == "unknown" for row in rows.values()), (
            f"{name}: skeleton must not contain guessed known facts"
        )


def test_clp_06_single_knowledge_point():
    forbidden = ["BASH_MAX_TIMEOUT_MS", "BASH_DEFAULT_TIMEOUT_MS", "600,000"]
    for rel in [
        "references/dispatch-recipes.md",
        "references/stage-prompts.md",
        "references/watch-model.md",
        "SKILL.md",
    ]:
        text = (SKILL_DIR / rel).read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text, f"{rel} duplicates CLI knowledge: {needle}"
    docs = DOCS.read_text(encoding="utf-8")
    for needle in forbidden:
        assert needle not in docs, f"docs page duplicates CLI knowledge: {needle}"


def test_clp_07_skill_section():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "## CLI Capability Profiles" in text
    section = text.split("## CLI Capability Profiles", 1)[1].split("\n## ", 1)[0]
    for needle in ["references/cli/", "index.md", "U2", "U4", "U5", "CAPABILITY_MATRIX", "唯一"]:
        assert needle in section, f"SKILL section missing: {needle}"
    assert text.index("## CLI Capability Profiles") < text.index("\n## Wrap-up\n")


def test_clp_08_u2_consult_record():
    prompts = (SKILL_DIR / "references" / "stage-prompts.md").read_text(encoding="utf-8")
    for field in ["profile_id", "profile_version", "observed_cli_version"]:
        assert field in prompts, f"dispatch record field missing: {field}"
    assert "U2" in prompts and "只读查阅" in prompts
    index = (CLI_DIR / "index.md").read_text(encoding="utf-8")
    assert "063" in index and "stream-json" in index
    assert "不改写" in index or "不得改写" in index


def test_clp_09_u4_u5_comparisons():
    prompts = (SKILL_DIR / "references" / "stage-prompts.md").read_text(encoding="utf-8")
    assert "U4" in prompts and "U5" in prompts
    assert "比对" in prompts
    for needle in ["缓冲", "哨兵", "退出", "日志", "超时", "detach", "孤儿"]:
        assert needle in prompts, f"U4/U5 comparison missing: {needle}"


def test_clp_10_write_order_and_feedback_cardinality():
    prompts = (SKILL_DIR / "references" / "stage-prompts.md").read_text(encoding="utf-8")
    section = prompts.split("## CLI Capability Profiles", 1)[1].split("\n## ", 1)[0].lower()
    order = ["cli_observations", "provenance", "feedback"]
    positions = [section.find(word) for word in order]
    assert all(position != -1 for position in positions)
    assert positions == sorted(positions), "write order must be spine → provenance → feedback"
    assert "恰好一条" in prompts
    assert "无新事实" in prompts and "零反馈" in prompts
    assert "每个事件各一条" in prompts or "每个观测事件" in prompts


def test_clp_11_marker_retrievable(tmp_path):
    index = (CLI_DIR / "index.md").read_text(encoding="utf-8")
    assert "cli-profile:<cli>" in index
    assert "--action record" in index and "feedback-utils.py" in index
    assert "--action list --contains" in index
    workspace = tmp_path / "ws"
    (workspace / ".specify" / "memory" / "feedback").mkdir(parents=True)
    engine = REPO_ROOT / ".specify" / "scripts" / "python" / "feedback-utils.py"
    record = subprocess.run(
        [sys.executable, str(engine), "--action", "record",
         "--workspace-root", str(workspace),
         "--unit-id", "skill:sdd-loop-driver", "--unit-type", "skill",
         "--run-id", "r20261020T120000Z-a1b2",
         "--review", "cli-profile:qodercli -p buffering mismatch observed",
         "--points", "cli-profile:qodercli mismatch"],
        capture_output=True, text=True,
    )
    assert record.returncode == 0, record.stderr
    listed = subprocess.run(
        [sys.executable, str(engine), "--action", "list", "--workspace-root", str(workspace),
         "--contains", "cli-profile:qodercli", "--format", "json"],
        capture_output=True, text=True,
    )
    assert listed.returncode == 0, listed.stderr
    payload = json.loads(listed.stdout)
    entries = payload.get("matches", payload.get("entries", payload if isinstance(payload, list) else []))
    assert len(entries) == 1


def test_clp_12_probe_object_registered():
    text = PROBE_DEFS.read_text(encoding="utf-8")
    rows = [line for line in text.splitlines()
            if line.startswith("| skill-sdd-loop-driver-cli-profile ")]
    assert len(rows) == 1, "exactly one CLI-profile probe object is required"
    assert "| skill-wrapup | skill:sdd-loop-driver | wrap-up |" in rows[0]
    validate = subprocess.run(
        [sys.executable, str(REPO_ROOT / ".specify" / "scripts" / "python" / "probe-utils.py"),
         "--action", "probes", "--validate"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    unit_rows = [line for line in text.splitlines()
                 if "skill:sdd-loop-driver" in line and line.startswith("|")]
    assert len(unit_rows) == 1


def test_clp_13_non_interference():
    text = (CLI_DIR / "index.md").read_text(encoding="utf-8")
    for needle in ["哨兵", "判定", "退出码", "确认门", "deadline", "测试预算"]:
        assert needle in text, f"non-interference boundary missing: {needle}"
    assert "U2" in text and ("不回溯" in text or "不改变" in text)


def test_clp_14_defect_lifecycle():
    text = _profile("qodercli")
    assert "缺陷" in text
    assert "fixed_in" in text
    assert "版本" in text and "证据" in text


def test_clp_15_matrix_authority():
    index = (CLI_DIR / "index.md").read_text(encoding="utf-8")
    assert "CAPABILITY_MATRIX" in index
    assert "scripts/python/execution-config.py" in index
    assert "唯一 owner" in index or "唯一" in index
    matrix = (REPO_ROOT / "scripts" / "python" / "execution-config.py").read_text(encoding="utf-8")
    assert "CAPABILITY_MATRIX" in matrix
    assert "hermes" not in matrix
    hermes = _profile("hermes")
    assert "矩阵" in hermes and ("无条目" in hermes or "缺口" in hermes)


def test_clp_16_delivery_mirror_docs():
    assert MIRROR_CLI_DIR.exists(), "CLI profiles mirror missing — sync-mirrors --write not run"
    for name in ["index", *PROFILES]:
        source = CLI_DIR / f"{name}.md"
        mirror = MIRROR_CLI_DIR / f"{name}.md"
        assert mirror.exists(), f"mirror missing: {name}"
        assert source.read_bytes() == mirror.read_bytes(), f"mirror drift: {name}"
    docs = DOCS.read_text(encoding="utf-8")
    assert "CLI 能力档案" in docs
    assert "references/cli/" in docs
    assert "BASH_MAX_TIMEOUT_MS" not in docs


def test_clp_17_no_063_duplicate_owner():
    spec_contracts = [
        path for path in (REPO_ROOT / ".specify" / "specs").glob("*/contracts/cli-profiles.md")
    ]
    assert spec_contracts == [REPO_ROOT / ".specify" / "specs" / "064-subagent-concurrency" /
                              "contracts" / "cli-profiles.md"], spec_contracts
    assert not list(REPO_ROOT.glob("**/references/cli/README.md"))
    assert not list(REPO_ROOT.glob("**/test_cli_profile_record.py"))
    probe = PROBE_DEFS.read_text(encoding="utf-8")
    unit_rows = [line for line in probe.splitlines()
                 if "skill:sdd-loop-driver" in line and line.startswith("|")]
    assert len(unit_rows) == 1
    assert "skill-sdd-loop-driver-cli-profile" in unit_rows[0]
    assert "skill-sdd-loop-driver-wrapup" not in probe
