"""Integration: US4 entry equivalence — the template and the CLI agree (097 T034).

Claims: contracts/migrate-template.md T-3. The agent-session entry is the
commands the template declares; the CLI entry is the same subcommand invoked
directly. On one fixture the two entries must produce (a) the identical
deterministic plan part (``items`` + ``summary``, cli C-4), (b) the identical
apply outcome and per-item ``disposition`` / ``status``, and (c) no extra files
in either direction — a second plan or an inlined inspection step would show up
as a write or as a differing tree.

Red-first discipline (Constitution IV): authored before the template exists, so
the extraction finds no declared command and the tests fail on that fact; the
in-suite mutation is green-by-construction only after T035 and exists to prove
the no-extra-files assertion has discriminative power (FR-002 / FR-025).

Execution model: the template's ``specify migrate ...`` lines are run in-process
through ``specify_cli.app`` exactly as the CLI entry (so the interactive-seam
monkeypatches apply); any non-``specify`` declared line is executed as a real
subprocess in the workspace — that is how an agent session would run it, and it
is what makes an inlined inspection step observable.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shlex
import subprocess
from pathlib import Path

import pytest

import specify_cli

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "commands" / "migrate.md"
BUILDERS_PATH = ROOT / "tests" / "fixtures" / "migrate-097" / "builders.py"

RUN_ID_RE = re.compile(r"\d{8}T\d{6}Z-[0-9a-f]{8}")
FENCE_RE = re.compile(r"^```(bash|sh)\s*$\n(.*?)^```\s*$", re.M | re.S)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _builders():
    spec = importlib.util.spec_from_file_location(
        "_migrate_us4_builders", BUILDERS_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _invoke(args, input_text=None):
    from typer.testing import CliRunner

    return CliRunner().invoke(specify_cli.app, args, input=input_text)


def _json_payload(result, expected_code):
    assert result.exit_code == expected_code, (
        f"exit {result.exit_code}, expected {expected_code}\n{result.output}"
    )
    return json.loads(result.stdout)


def _allow_apply(monkeypatch):
    monkeypatch.setattr(specify_cli, "migrate_symlink_supported", lambda: True)


def _template_text() -> str:
    assert TEMPLATE.is_file(), (
        "templates/commands/migrate.md is missing — the template entry has no "
        "declared commands to run (T035 authors it)"
    )
    return TEMPLATE.read_text(encoding="utf-8")


def _declared_commands(text: str) -> list[str]:
    """Every executable line the template declares in a bash/sh fence."""
    commands: list[str] = []
    for match in FENCE_RE.finditer(text):
        for line in match.group(2).splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                commands.append(stripped)
    return commands


def _dry_run_commands(text: str) -> list[str]:
    return [line for line in _declared_commands(text) if "--apply" not in line]


def _apply_commands(text: str) -> list[str]:
    return [line for line in _declared_commands(text) if "--apply" in line]


def _execute(commands: list[str], workspace: Path, monkeypatch):
    """Run the declared commands the way the agent session would."""
    monkeypatch.chdir(workspace)
    results = []
    for line in commands:
        argv = shlex.split(line)
        if argv[:1] == ["specify"]:
            results.append(_invoke(argv[1:]))
        else:
            results.append(
                subprocess.run(argv, cwd=workspace, capture_output=True, text=True)
            )
    return results


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            digest.update(f"L {rel} -> {os.readlink(path)}\n".encode("utf-8"))
        elif path.is_dir():
            digest.update(f"D {rel}\n".encode("utf-8"))
        else:
            content = hashlib.sha256(path.read_bytes()).hexdigest()
            digest.update(f"F {rel} {content}\n".encode("utf-8"))
    return digest.hexdigest()


def _assert_zero_write(before: str, after: str, label: str) -> None:
    assert before == after, (
        f"{label} wrote to the workspace — the dry-run entry must be output-only "
        "(no extra files, cli C-7.1)"
    )


def _normalized_paths(root: Path) -> set[str]:
    """Relative path set with per-run ids normalized (receipt name and archive root)."""
    return {
        RUN_ID_RE.sub("<run-id>", path.relative_to(root).as_posix())
        for path in root.rglob("*")
    }


def _receipt(workspace: Path) -> dict:
    files = sorted((workspace / ".specify" / "memory" / "migrate" / "receipts").glob("*.json"))
    assert len(files) == 1, f"expected exactly one receipt, found {[p.name for p in files]}"
    return json.loads(files[0].read_text(encoding="utf-8"))


def _item_tuples(record: dict) -> list[tuple[str, str, str, str]]:
    return sorted(
        (item["dimension"], item["target"], item["disposition"], item["status"])
        for item in record["items"]
    )


# ---------------------------------------------------------------------------
# T-3 — dry-run: same deterministic plan, zero writes on both entries
# ---------------------------------------------------------------------------


def test_template_dry_run_matches_the_direct_cli_plan(tmp_path, monkeypatch):
    workspace = _builders().build_legacy_project(tmp_path / "equiv-dry")

    dry_commands = _dry_run_commands(_template_text())
    assert len(dry_commands) == 1, (
        "the template must declare exactly one dry-run command; "
        f"found {dry_commands!r}"
    )
    assert "--format" in dry_commands[0] and "json" in dry_commands[0], (
        "the declared dry-run command must ask for the machine-readable envelope "
        f"(T-2.1); got {dry_commands[0]!r}"
    )

    before = _tree_digest(workspace)
    template_results = _execute(dry_commands, workspace, monkeypatch)
    template_payload = _json_payload(template_results[0], 1)

    direct_payload = _json_payload(
        _invoke(["migrate", "--workspace", str(workspace), "--format", "json"]), 1
    )

    assert template_payload["items"] == direct_payload["items"], (
        "the template entry and the CLI entry produced different plan items"
    )
    assert template_payload["summary"] == direct_payload["summary"], (
        "the template entry and the CLI entry produced different summaries"
    )
    assert template_payload["outcome"] == direct_payload["outcome"] == "planned"

    _assert_zero_write(before, _tree_digest(workspace), "the two dry-run entries")


# ---------------------------------------------------------------------------
# T-3 — apply: same outcome and per-item dispositions/statuses, no extra files
# ---------------------------------------------------------------------------


def test_template_apply_matches_the_direct_cli_result(tmp_path, monkeypatch):
    template_ws = _builders().build_legacy_project(tmp_path / "entry-template")
    direct_ws = _builders().build_legacy_project(tmp_path / "entry-direct")
    _allow_apply(monkeypatch)

    apply_commands = _apply_commands(_template_text())
    assert len(apply_commands) == 1, (
        "the template must declare exactly one apply command; "
        f"found {apply_commands!r}"
    )

    _execute(apply_commands, template_ws, monkeypatch)
    template_receipt = _receipt(template_ws)

    direct_payload = _json_payload(
        _invoke(
            ["migrate", "--workspace", str(direct_ws), "--apply", "--format", "json"]
        ),
        0,
    )
    direct_receipt = direct_payload["receipt"]

    assert template_receipt["outcome"] == direct_receipt["outcome"] == "applied"
    assert template_receipt["status"] == direct_receipt["status"] == "completed"
    assert _item_tuples(template_receipt) == _item_tuples(direct_receipt), (
        "the two entries disagreed on a per-item disposition/status"
    )

    assert _normalized_paths(template_ws) == _normalized_paths(direct_ws), (
        "one entry left extra files the other did not — the template entry must "
        "produce the same workspace as the CLI entry"
    )
    assert (template_ws / ".specify" / "archive" / "migrate").is_dir()
    assert (direct_ws / ".specify" / "archive" / "migrate").is_dir()


# ---------------------------------------------------------------------------
# FR-002 / FR-025 — an inlined inspection command turns the equivalence red
# ---------------------------------------------------------------------------


def test_mutation_template_inlining_an_inspection_command_turns_equivalence_red(
    tmp_path, monkeypatch
):
    """A template that inlines an inspection step is caught as a workspace write.

    The mutation is a declared shell line an agent session would execute; the
    structural guard in test_migrate_template.py forbids such a line outright,
    and this runtime drill proves the no-extra-files assertion would also catch
    it — a green guard must be able to go red.
    """
    workspace = _builders().build_legacy_project(tmp_path / "mutation")
    mutated = (
        _template_text()
        + "\n```bash\n"
        + "python3 -c \"from pathlib import Path; "
        + "Path('inline-check.txt').write_text('inline')\"\n"
        + "```\n"
    )

    dry_commands = _dry_run_commands(mutated)
    assert any("inline-check" in command for command in dry_commands), (
        "the mutation was not extracted as a declared command"
    )

    before = _tree_digest(workspace)
    _execute(dry_commands, workspace, monkeypatch)
    after = _tree_digest(workspace)

    assert (workspace / "inline-check.txt").is_file(), (
        "the mutation did not take effect — the drill would be vacuous"
    )
    with pytest.raises(AssertionError):
        _assert_zero_write(before, after, "the mutated template")
