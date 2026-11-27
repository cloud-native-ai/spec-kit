"""Integration guard: fresh init distribution, offline audit, ambient section (Feature 110).

Two separately named legs (C-036, FR-023/FR-024/FR-025, SC-005/SC-009):

* ``test_fresh_init_distributes_and_audits_offline`` — initializes a fresh project through
  the repository's own in-process init path (``specify_cli`` with its resource root pointed
  at the repository root, sockets blocked in process), asserts the owner document, the four
  facts and the engine land under ``.specify/``, and runs ``check`` (exit 0) plus
  ``manifest --layer project`` (explicit absence lines, exit 0) with zero socket attempts
  and nothing transmitted.
* ``test_fresh_init_instructions_carry_the_ambient_section`` — regenerates the fresh tree's
  instructions through the house generator and asserts the ambient section is present in
  summary-plus-pointer shape. This leg stays red until the ambient section lands (T029).

The installed 0.0.22 build predates this feature, so both legs initialize through the
repository's own sources, never through the installed CLI.

Authored red-first (C-040): neither the engine nor the ambient section exists yet at this
point of the run, so both legs are expected to fail before the implementation rows land.
"""
from __future__ import annotations

import json
import socket

import pytest

from fixtures.context_management_support import ENGINE, REPO_ROOT
from tests.script_api import run_engine_in_process, run_generate_instructions

pytestmark = pytest.mark.integration

AMBIENT_HEADING = "## Context Management(上下文管理)"
AMBIENT_OWNER_POINTER = ".specify/shared/definitions/context-management-definitions.md"
AMBIENT_AUDIT_ENTRY = ".specify/scripts/python/context-audit.py"

INSTALLED_PATHS = (
    ".specify/shared/definitions/context-management-definitions.md",
    ".specify/shared/declarations/facts/context-categories.yaml",
    ".specify/shared/declarations/facts/context-layers.yaml",
    ".specify/shared/declarations/facts/context-forms.yaml",
    ".specify/shared/declarations/facts/context-classes.yaml",
    ".specify/scripts/python/context-audit.py",
)


def _block_sockets(monkeypatch) -> list:
    attempts = []

    def blocked(*args, **kwargs):
        attempts.append((args, kwargs))
        raise AssertionError("a socket entry point was reached during init or audit")

    monkeypatch.setattr(socket, "socket", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(socket, "getaddrinfo", blocked)
    return attempts


def _fresh_project(tmp_path, monkeypatch):
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: REPO_ROOT)
    from specify_cli import copy_local_templates

    project = tmp_path / "fresh"
    copy_local_templates(project, "qoder", "sh")
    return project


def _active_house_engine():
    assert ENGINE.is_file(), f"audit engine missing: {ENGINE}"
    return ENGINE


def test_fresh_init_distributes_and_audits_offline(tmp_path, monkeypatch):
    attempts = _block_sockets(monkeypatch)
    fresh = _fresh_project(tmp_path, monkeypatch)
    engine = _active_house_engine()

    for relative in INSTALLED_PATHS:
        installed = fresh / relative
        assert installed.is_file(), f"fresh init did not distribute {relative}"

    check = run_engine_in_process(
        engine, ("--action", "check", "--workspace-root", str(fresh)))
    assert check.returncode == 0, (
        f"a fresh project's check must exit 0, got {check.returncode}\n"
        f"stdout={check.stdout}\nstderr={check.stderr}")

    manifest = run_engine_in_process(
        engine, ("--action", "manifest", "--layer", "project", "--json",
                 "--workspace-root", str(fresh)))
    assert manifest.returncode == 0, (
        f"a fresh project's manifest must exit 0, got {manifest.returncode}\n"
        f"stdout={manifest.stdout}\nstderr={manifest.stderr}")
    payload = json.loads(manifest.stdout)
    assert payload["layer"] == "project"
    assert payload["rows"], "the manifest must print the project-layer rows"
    absences = [row for row in payload["rows"] if row["token"] != "present"]
    assert absences, "a fresh project must print explicit absence lines, never an empty silence"
    for row in absences:
        assert row["reason"], f"an absence row must carry its reason: {row}"
    assert attempts == [], f"a socket entry point was reached: {attempts}"


def _ambient_body(text: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == AMBIENT_HEADING:
            start = index + 1
            break
    if start is None:
        return ""
    out = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out)


def test_fresh_init_instructions_carry_the_ambient_section(tmp_path, monkeypatch):
    fresh = _fresh_project(tmp_path, monkeypatch)
    import subprocess

    subprocess.run(["git", "init", "-q"], cwd=fresh, check=True)
    result = run_generate_instructions(fresh)
    assert result.returncode == 0, (
        f"the instructions generator must succeed in the fresh tree:\n"
        f"stdout={result.stdout}\nstderr={result.stderr}")
    live = (fresh / ".specify" / "instructions.md")
    assert live.is_file(), "the generator did not produce .specify/instructions.md"
    text = live.read_text(encoding="utf-8")
    assert AMBIENT_HEADING in text.splitlines(), (
        "the ambient section heading must appear verbatim in the fresh tree's instructions")
    body = _ambient_body(text)
    assert body, "the ambient section carries no body"
    assert AMBIENT_OWNER_POINTER in body, "the section must point at the installed owner document"
    assert AMBIENT_AUDIT_ENTRY in body, "the section must point at the installed audit entry"
    for line in body.splitlines():
        assert not line.strip().startswith("|"), (
            f"the ambient section must stay summary-plus-pointer, no table: {line!r}")