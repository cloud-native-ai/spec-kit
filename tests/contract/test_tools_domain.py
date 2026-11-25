"""Contract tests: the tools domain holds tracked records beside ignored inventories (Feature 105, US4 / T021).

Contract: ``contracts/store-layout.contract.md`` C-4 (tracking/ignore matrix); requirements
FR-020 and US4. ``.specify/tools/`` is the one directory where human-authored records
(``<name>.md``, tracked) and machine-generated discovery inventories
(``{system,shell,project}.json``, ignored) coexist; the ignore rule must be narrow enough
that a record is never silently dropped and an inventory is never committed.

Red-first (Constitution IV): authored before T022/T023 land; the red readings are recorded
in the feature's ``notes/red-first-evidence.md``. Every ignore judgement is measured with
``git check-ignore`` inside a throwaway git fixture, never by reading the rule text alone.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

import specify_cli

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "gitignore-specify-template"
INSTALLED = ROOT / ".specify" / ".gitignore"
CLAUDE_TEMPLATE = ROOT / "templates" / "claudeignore-template"
CODEX_TEMPLATE = ROOT / "templates" / "codexignore-template"


def _git(args, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, check=False,
                          capture_output=True, text=True)


@pytest.fixture
def tools_workspace(tmp_path: Path) -> Path:
    """A git workspace carrying the installed ignore copy and both tools file kinds."""
    tools = tmp_path / ".specify" / "tools"
    tools.mkdir(parents=True)
    (tools / "kubectl-get.md").write_text("# Tool Record: kubectl-get\n", encoding="utf-8")
    (tools / "kubectl-get.json").write_text('{"source": "machine"}\n', encoding="utf-8")
    (tools / "system.json").write_text('{"binaries": []}\n', encoding="utf-8")
    shutil.copyfile(TEMPLATE, tmp_path / ".specify" / ".gitignore")
    init = _git(["init", "-q"], tmp_path)
    assert init.returncode == 0, init.stderr
    return tmp_path


def test_tools_records_are_tracked_and_inventories_ignored(tools_workspace: Path):
    for rel in (".specify/tools/system.json", ".specify/tools/kubectl-get.json"):
        result = _git(["check-ignore", "-v", rel], tools_workspace)
        assert result.returncode == 0, (
            f"{rel} must be ignored by the framework-owned .specify/.gitignore"
        )
        assert "tools/*.json" in result.stdout, (
            f"the narrow inventory rule must be the matching pattern; got {result.stdout!r}"
        )
    for rel in (".specify/tools/kubectl-get.md",):
        result = _git(["check-ignore", "-q", rel], tools_workspace)
        assert result.returncode == 1, (
            f"{rel} must stay tracked: a whole-directory tools rule silently drops records"
        )


def test_same_basename_record_and_inventory_coexist(tools_workspace: Path):
    tools = tools_workspace / ".specify" / "tools"
    before = {p.name: p.read_text(encoding="utf-8") for p in tools.iterdir()}
    added = _git(["add", "-A"], tools_workspace)
    assert added.returncode == 0, added.stderr
    listed = _git(["ls-files", ".specify/tools"], tools_workspace)
    assert listed.stdout.split() == [".specify/tools/kubectl-get.md"], (
        "exactly the record is staged; the same-basename inventory and system.json stay out"
    )
    after = {p.name: p.read_text(encoding="utf-8") for p in tools.iterdir()}
    assert before == after, "neither the record nor the inventory may be overwritten"


def test_template_and_installed_copy_are_byte_identical_with_narrow_rules():
    assert TEMPLATE.is_file() and INSTALLED.is_file()
    template_bytes = TEMPLATE.read_bytes()
    assert template_bytes == INSTALLED.read_bytes(), (
        "templates/gitignore-specify-template and the installed .specify/.gitignore must be "
        "byte-identical and change in the same commit (C-4)"
    )
    body = template_bytes.decode("utf-8")
    assert "tools/*.json" in body
    assert "\ntools/\n" not in body, "the whole-directory tools rule must be narrowed"
    assert "\nsanitize/\n" in body
    assert "memory/sanitize/" not in body
    assert "\ntrigger/telemetry.jsonl\n" in body
    assert "memory/trigger/telemetry.jsonl" not in body
    assert "memory/tools/" not in body, (
        "the comment must name the tools domain's current home, not the retired one"
    )


def test_claude_and_codex_templates_release_every_store_root():
    statement, label = specify_cli.store_layout()
    assert label is None, label
    stores = list(statement["stores"])
    assert len(stores) == 14, f"the declaration must describe 14 stores; got {stores}"
    for template in (CLAUDE_TEMPLATE, CODEX_TEMPLATE):
        body = template.read_text(encoding="utf-8")
        rel = template.relative_to(ROOT).as_posix()
        assert "!.specify/memory/" not in body, (
            f"{rel} still releases the retired container instead of the store roots"
        )
        missing = [store for store in stores if f"!.specify/{store}/" not in body]
        assert not missing, f"{rel} does not release these store roots: {missing}"
