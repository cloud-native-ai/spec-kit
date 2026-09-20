"""Contract tests for the archive-session export skill (039-session-export).

Contracts: ``.specify/specs/039-session-export/contracts/export-skill-rework.contract.md``
(T002 rework + T009 genericity — the two were split across
``test_export_skill_rework.py`` and ``test_export_skill_genericity.py`` and are
merged here, since both read the same two files against the same contract).

Pins: the six-tool PARSERS convergence (STR-002), zero residue of the six removed
products and of the platform-specific (aone-open) dependency lineage in **both**
skill files, the network-free guarantee, the zip→directory product shape, --name
grammar and conflict handling, probe-style adapters for copilot/hermes (exit 4 +
honest declaration), the five-value exit-code semantics, and the read-only
discipline on host session storage. The CLI is exercised black-box via subprocess
with a synthetic HOME so no real session store is touched.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "skills/archive-session/scripts/export.py"
SKILL = REPO_ROOT / "skills/archive-session/SKILL.md"

pytestmark = pytest.mark.contract

#: STR-002 — exactly six, normative tool names.
SIX_TOOLS = {"claude-code", "codex-cli", "qoder-cli", "copilot", "opencode", "hermes"}

#: Identifier-level residue markers of the six removed products — zero residue in
#: BOTH the engine and the skill document (one list, one owner).
REMOVED_MARKERS = [
    "qwen-code", "qwen_", "_qwen_", "qoderwork", "oh-my-pi", "_omp_root",
    "kimi-code", "kimi_", "_kimi_", "codex-app", "codexapp",
]

#: Platform-specific dependency markers (aone-open lineage).
PLATFORM_MARKERS = ["a1 skill report", "x-source", "aone-open", "aone_open"]

#: The two generalized surfaces every residue/genericity claim is read from.
GENERICITY_SURFACES = (ENGINE, SKILL)


def _engine():
    spec = importlib.util.spec_from_file_location("export_session_rework", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["export_session_rework"] = module
    spec.loader.exec_module(module)
    return module


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture()
def fake_home(tmp_path):
    """Synthetic HOME with one claude-code session for a fake project."""
    home = tmp_path / "home"
    project = tmp_path / "proj"
    project.mkdir()
    sid = "abc12345-0000-4000-8000-deadbeef0000"
    proj_dir = home / ".claude" / "projects" / "-fake-proj"
    proj_dir.mkdir(parents=True)
    lines = [
        json.dumps({"cwd": str(project), "type": "user",
                    "message": {"role": "user", "content": "唯一探针文本 xylophone-42"}}),
        json.dumps({"cwd": str(project), "type": "assistant",
                    "message": {"role": "assistant", "model": "test-model",
                                "content": "ok"}}),
    ]
    (proj_dir / f"{sid}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return home, project, sid


def run_cli(home: Path, project: Path, *args: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "HOME": str(home)}
    return subprocess.run(
        [sys.executable, str(ENGINE), "--project", str(project), *args],
        capture_output=True, text=True, env=env, cwd=str(project),
    )


# --------------------------------------------------------------------------
# §1 support matrix convergence
# --------------------------------------------------------------------------

def test_parsers_converge_to_exactly_six_tools():
    module = _engine()
    assert set(module.PARSERS.keys()) == SIX_TOOLS


def test_support_matrix_is_exactly_the_six_tools():
    """The agent-facing matrix in SKILL.md must name the same six the engine parses.

    ``PARSERS`` is the machine-checkable owner (equality-pinned above); this is the
    doc side, plus the broader legacy-name negative — bare ``qwen``/``kimi`` are not
    covered by REMOVED_MARKERS, whose entries are all identifier-shaped.
    """
    text = SKILL.read_text(encoding="utf-8")
    for tool in SIX_TOOLS:
        assert f"`{tool}`" in text, f"matrix row missing for {tool}"
    # removed tool names must not appear even as prose
    for legacy in ("qwen", "kimi", "oh-my-pi", "qoderwork"):
        assert legacy not in text.lower(), f"legacy tool {legacy!r} mentioned in SKILL.md"


@pytest.mark.parametrize("marker", REMOVED_MARKERS)
def test_removed_products_leave_zero_residue(marker):
    """The six removed products must be gone from the engine *and* the skill doc.

    Both halves were pinned once each with byte-identical marker lists; one list
    read over both files is the same proposition with one owner.
    """
    for path in GENERICITY_SURFACES:
        text = path.read_text(encoding="utf-8")
        assert marker not in text, f"{marker!r} residue in {path.name}"


# --------------------------------------------------------------------------
# §1b genericity: no platform-specific lineage, network-free (was T009)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("marker", PLATFORM_MARKERS)
def test_no_platform_specific_dependency_residue(marker):
    for path in GENERICITY_SURFACES:
        text = path.read_text(encoding="utf-8")
        assert marker not in text, f"platform dependency {marker!r} in {path.name}"


def test_no_outbound_network_calls():
    for path in GENERICITY_SURFACES:
        text = path.read_text(encoding="utf-8")
        assert "http://" not in text and "https://" not in text, (
            f"outbound URL in {path.name} — the skill must be network-free"
        )


# --------------------------------------------------------------------------
# §2 directory product shape
# --------------------------------------------------------------------------

def test_export_produces_the_contracted_directory(fake_home, tmp_path):
    home, project, sid = fake_home
    result = run_cli(home, project, "--name", "dir-shape", "--tool", "claude-code")
    assert result.returncode == 0, result.stderr
    bundle = project / ".session-export" / "dir-shape"
    assert result.stdout.strip().splitlines()[-1] == str(bundle)
    assert bundle.is_dir(), "product shape is a user-named directory, not a zip"
    assert (bundle / "session-meta.json").is_file()
    assert (bundle / "SESSION.md").is_file()
    mains = [p for p in bundle.glob("main.*")]
    assert mains, "the main session record must land as main.<ext>"
    content = mains[0].read_text(encoding="utf-8")
    assert "xylophone-42" in content, "raw record content must not be weakened"
    # no zip artifact in the new shape
    assert not list(bundle.glob("*.zip"))


# --------------------------------------------------------------------------
# §3 --name grammar and conflicts
# --------------------------------------------------------------------------

def test_missing_name_is_exit_2(fake_home):
    home, project, _ = fake_home
    result = run_cli(home, project, "--tool", "claude-code")
    assert result.returncode == 2, result.stderr


@pytest.mark.parametrize("bad_name", ["has/slash", "-leading-dash", "spa ce", ".."])
def test_bad_name_grammar_is_exit_2(fake_home, bad_name):
    home, project, _ = fake_home
    result = run_cli(home, project, "--name", bad_name, "--tool", "claude-code")
    assert result.returncode == 2, result.stderr


def test_same_name_conflict_refuses_without_interactive_override(fake_home):
    home, project, _ = fake_home
    first = run_cli(home, project, "--name", "dup", "--tool", "claude-code")
    assert first.returncode == 0, first.stderr
    second = run_cli(home, project, "--name", "dup", "--tool", "claude-code")
    assert second.returncode != 0, "same-name re-export must not silently overwrite"
    assert "dup" in second.stderr


# --------------------------------------------------------------------------
# §1 probe-style adapters: copilot / hermes
# --------------------------------------------------------------------------

@pytest.mark.parametrize("tool", ["copilot", "hermes"])
def test_probe_tools_declare_no_source_honestly(fake_home, tool):
    home, project, _ = fake_home
    result = run_cli(home, project, "--name", "probe-x", "--tool", tool)
    assert result.returncode == 4, result.stderr
    assert "未探测到" in result.stderr or "not detected" in result.stderr.lower()


# --------------------------------------------------------------------------
# §6 exit-code semantics
# --------------------------------------------------------------------------

def test_no_session_found_is_exit_3(fake_home):
    home, project, _ = fake_home
    empty = fake_home[1].parent / "empty-proj"
    empty.mkdir()
    result = run_cli(home, project, "--name", "nf", "--tool", "claude-code",
                     "--project", str(empty))
    # explicit tool + no session for that project → not found
    assert result.returncode == 3, result.stderr


# --------------------------------------------------------------------------
# §5 read-only discipline
# --------------------------------------------------------------------------

def test_export_does_not_touch_the_host_store(fake_home):
    home, project, sid = fake_home
    src = home / ".claude" / "projects" / "-fake-proj" / f"{sid}.jsonl"
    before = _sha(src)
    result = run_cli(home, project, "--name", "ro-check", "--tool", "claude-code")
    assert result.returncode == 0, result.stderr
    assert _sha(src) == before, "host session storage must stay byte-identical"


# --------------------------------------------------------------------------
# §7 SKILL.md documents what the CLI above actually does
# --------------------------------------------------------------------------

def test_skill_describes_the_directory_product_shape():
    text = SKILL.read_text(encoding="utf-8")
    assert "SESSION.md" in text, "description doc flow must be documented"
    assert "session-meta.json" in text, "meta output must be documented"
    assert ".session-export" in text, "export root must be documented"


def test_skill_documents_the_name_argument_and_exit_codes():
    """Exit codes 0 and 5 are documented-only — no CLI case above exercises them."""
    text = SKILL.read_text(encoding="utf-8")
    assert "--name" in text
    for code in ("0", "2", "3", "4", "5"):
        assert f"| {code} |" in text, f"exit-code row missing: {code}"
