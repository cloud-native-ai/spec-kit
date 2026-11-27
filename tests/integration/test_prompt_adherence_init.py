"""Downstream-init distribution guard for prompt adherence (109).

A declared regression guard with its mirror-independent initial form: a temp project
initialized from THIS repository's framework sources (the ``copy_local_templates`` +
``get_resource_path`` monkeypatch pattern) carries the mechanism without any additional
setup:

* the owner document lands under the project's ``.specify/shared/definitions/``;
* the five declaration facts land under the project's ``.specify/shared/declarations/facts/``;
* the engine lands under the project's ``.specify/scripts/python/`` and answers ``--version``;
* the bare invocation on the recordless project emits explicit ``not_evaluated`` /
  ``Unobserved`` lines with exit 0 under a socket-blocked interpreter;
* no ambient instructions section and no ``/speckit.*`` command or skill surface ships for
  this feature; the C-037 inventory-only scope is asserted (the fresh project's
  prompt-adherence-named files are exactly the mechanism surfaces).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]

INSTALLED_OWNER = Path(".specify/shared/definitions/prompt-adherence-definitions.md")
INSTALLED_ENGINE = Path(".specify/scripts/python/prompt-adherence.py")
INSTALLED_FACTS = Path(".specify/shared/declarations/facts")
FACT_SLUGS = (
    "prompt-adherence-layers",
    "prompt-adherence-strengths",
    "prompt-adherence-signals",
    "prompt-adherence-deviation-classes",
    "prompt-adherence-reading-status",
)
CATALOG_ORDER = (
    "run-determination-record",
    "exec-quant-record",
    "feedback-entry",
    "gate-observation-record",
    "evidence-finding",
    "probe-registry-declaration",
)
BLIND_SPOTS = (
    "host-prompt-content",
    "host-rule-surfacing",
    "in-turn-rule-behavior",
    "anomaly-line-persistence",
    "gate-breach-and-silent-skip",
    "instruction-drift-between-reconciles",
)


def _initialize_from_repo_sources(project: Path, monkeypatch) -> None:
    """Run the real init distribution with this repository as the resource root."""
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: REPO_ROOT)
    from specify_cli import copy_local_templates

    copy_local_templates(project, "qoder", "sh")


def _blocked_env(tmp_path: Path) -> dict:
    """An environment whose interpreter blocks every socket entry point at startup."""
    blocker = tmp_path / "netblock"
    blocker.mkdir(exist_ok=True)
    (blocker / "sitecustomize.py").write_text(
        "import socket\n"
        "\n"
        "def _blocked(*args, **kwargs):\n"
        "    raise RuntimeError('network access is blocked in this interpreter')\n"
        "\n"
        "socket.socket = _blocked\n"
        "socket.create_connection = _blocked\n"
        "socket.getaddrinfo = _blocked\n"
        "socket.gethostbyname = _blocked\n",
        encoding="utf-8",
    )
    env = {**os.environ}
    env["PYTHONPATH"] = str(blocker)
    return env


def _run_installed(project: Path, *args, env=None):
    return subprocess.run(
        [sys.executable, str(project / INSTALLED_ENGINE)] + [str(arg) for arg in args],
        cwd=str(project),
        capture_output=True,
        text=True,
        env=env,
    )


# --------------------------------------------------------------------------- #
# FR-020 / SC-005 — a fresh init contains the mechanism
# --------------------------------------------------------------------------- #
def test_fresh_init_contains_the_owner_document_facts_and_engine(tmp_path, monkeypatch):
    project = tmp_path / "fresh"
    _initialize_from_repo_sources(project, monkeypatch)

    owner = project / INSTALLED_OWNER
    assert owner.is_file(), (
        "a fresh init lacks the owner document at %r — the shared/ tree did not ride "
        "publish -> install -> init (FR-020)" % INSTALLED_OWNER.as_posix()
    )
    owner_text = owner.read_text(encoding="utf-8").lower()
    assert "coverage map" in owner_text, (
        "the installed owner document carries no coverage map"
    )
    assert "blind-spot register" in owner_text, (
        "the installed owner document carries no blind-spot register"
    )

    for slug in FACT_SLUGS:
        fact = project / INSTALLED_FACTS / (slug + ".yaml")
        assert fact.is_file(), (
            "a fresh init lacks the declaration fact %r (FR-020)" % fact.relative_to(project)
        )

    engine = project / INSTALLED_ENGINE
    assert engine.is_file(), (
        "a fresh init lacks the engine at %r (FR-020)" % INSTALLED_ENGINE.as_posix()
    )


# --------------------------------------------------------------------------- #
# FR-022 / FR-023 — the installed entry answers --version
# --------------------------------------------------------------------------- #
def test_installed_entry_answers_version(tmp_path, monkeypatch):
    project = tmp_path / "fresh"
    _initialize_from_repo_sources(project, monkeypatch)
    proc = _run_installed(project, "--version")
    assert proc.returncode == 0, (
        "the installed copy's --version exited %d; stderr=%r" % (proc.returncode, proc.stderr)
    )
    line = proc.stdout.strip()
    assert line.startswith("prompt-adherence.py "), (
        "the installed copy's --version is not one '<script-name> <version>' line: %r" % line
    )
    assert len(line.split()) == 2, "--version must print exactly one identity line: %r" % line


# --------------------------------------------------------------------------- #
# FR-021 / SC-005 — offline, explicit absence, exit 0
# --------------------------------------------------------------------------- #
def test_socket_blocking_actually_blocks_the_interpreter(tmp_path):
    env = _blocked_env(tmp_path)
    proc = subprocess.run(
        [sys.executable, "-c", "import socket; socket.socket()"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode != 0 and "blocked" in proc.stderr, (
        "the socket-blocked interpreter did not reject a socket dial, so the isolation leg "
        "below would prove nothing: rc=%d stderr=%r" % (proc.returncode, proc.stderr)
    )


def test_bare_invocation_offline_emits_explicit_absence_lines(tmp_path, monkeypatch):
    project = tmp_path / "fresh"
    _initialize_from_repo_sources(project, monkeypatch)
    proc = _run_installed(project, env=_blocked_env(tmp_path))
    assert proc.returncode == 0, (
        "the bare invocation on a fresh project must complete with exit 0 under a "
        "socket-blocked interpreter (FR-021/SC-005); rc=%d stdout=%r stderr=%r"
        % (proc.returncode, proc.stdout, proc.stderr)
    )
    assert "Traceback" not in proc.stderr, (
        "the offline bare invocation crashed: %r" % proc.stderr
    )
    assert "status: no-data" in proc.stdout, (
        "a recordless project must read status no-data; got: %r" % proc.stdout
    )
    assert "state=not_evaluated" in proc.stdout, (
        "the recordless reading carries no explicit not_evaluated line (FR-011)"
    )
    assert "state=Unobserved" in proc.stdout, (
        "the recordless reading carries no explicit Unobserved line (FR-011)"
    )
    assert "reason=source-unavailable" in proc.stdout, (
        "an absent store must surface its reason, never a clean default (FR-022)"
    )
    assert "coverage-blind-spots: " + ", ".join(BLIND_SPOTS) in proc.stdout, (
        "the fresh-project reading does not carry all six blind spots as not observable "
        "(FR-013)"
    )


def test_bare_invocation_json_form_is_the_same_reading(tmp_path, monkeypatch):
    project = tmp_path / "fresh"
    _initialize_from_repo_sources(project, monkeypatch)
    proc = _run_installed(project, "--json", env=_blocked_env(tmp_path))
    assert proc.returncode == 0, proc.stderr
    reading = json.loads(proc.stdout)
    assert reading["status"] == "no-data"
    assert reading["coverage"]["blind_spots"] == list(BLIND_SPOTS)
    assert [obs["row"] for obs in reading["observations"]] == list(CATALOG_ORDER)
    for observation in reading["observations"]:
        assert observation["state"] in {"not_evaluated", "Unobserved", "Wired"}, (
            "a recordless project reads %r for %r; absence must never read as a positive "
            "state (FR-011)" % (observation["state"], observation["row"])
        )


# --------------------------------------------------------------------------- #
# C-037 — no ambient instructions section, no command or skill surface
# --------------------------------------------------------------------------- #
def test_no_instructions_section_and_no_command_or_skill_surface(tmp_path, monkeypatch):
    for path in (
        REPO_ROOT / "templates" / "instructions-template.md",
        REPO_ROOT / ".specify" / "instructions.md",
    ):
        assert path.is_file(), "expected instructions surface missing: %s" % path
        lowered = path.read_text(encoding="utf-8").lower()
        assert "prompt-adherence" not in lowered and "prompt adherence" not in lowered, (
            "%s carries a prompt-adherence section; this feature ships no ambient "
            "instructions section (C-037)" % path.relative_to(REPO_ROOT)
        )

    hits = []
    for pattern in (
        "templates/commands/**/*prompt-adherence*",
        "skills/**/*prompt-adherence*",
        ".specify/skills/**/*prompt-adherence*",
        ".specify/templates/commands/**/*prompt-adherence*",
    ):
        hits.extend(str(path.relative_to(REPO_ROOT)) for path in REPO_ROOT.glob(pattern))
    assert not hits, (
        "a /speckit.* command or skill surface ships for this feature; none may (C-037): %r"
        % hits
    )

    project = tmp_path / "fresh"
    _initialize_from_repo_sources(project, monkeypatch)
    generated = [
        str(path.relative_to(project))
        for pattern in (".qoder/commands/*prompt-adherence*", ".specify/skills/**/*prompt-adherence*")
        for path in project.glob(pattern)
    ]
    assert not generated, (
        "the fresh init generated a prompt-adherence command or skill surface: %r" % generated
    )


def test_fresh_project_prompt_adherence_inventory_is_the_mechanism_only(tmp_path, monkeypatch):
    """C-037's inventory-only scope: no file named for the feature beyond the mechanism."""
    project = tmp_path / "fresh"
    _initialize_from_repo_sources(project, monkeypatch)
    hits = {
        path.relative_to(project).as_posix()
        for path in project.rglob("*prompt-adherence*")
        if path.is_file()
    }
    expected = {INSTALLED_OWNER.as_posix(), INSTALLED_ENGINE.as_posix()} | {
        (INSTALLED_FACTS / (slug + ".yaml")).as_posix() for slug in FACT_SLUGS
    }
    assert hits == expected, (
        "the fresh project's prompt-adherence inventory is %r; expected exactly the mechanism "
        "surfaces %r (C-037 inventory-only scope)" % (sorted(hits), sorted(expected))
    )