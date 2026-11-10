"""Contract tests for the sdd-observer agent template (Feature 096).

Contracts: `contracts/observer-role.contract.md` C-02…C-08 authored in T018 and the C-09
instance-identity face extended in T038. The template is a framework source under `agents/`;
its installed mirror and per-tool copies are later packages' subjects. Journal spellings stay
with their declaration owners; this module pins only the template's own face.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "agents" / "sdd-observer.agent.md"
FAST_FAIL_DOC = REPO_ROOT / "shared" / "guidelines" / "fast-fail.md"
AGENT_DEFINITIONS = REPO_ROOT / "shared" / "definitions" / "agent-definitions.md"

CLAUSE_BEGIN = "<!-- fast-fail-clause:begin -->"
CLAUSE_END = "<!-- fast-fail-clause:end -->"

#: Read/search/shell tools are the only capability classes an observer may hold.
READ_TOOLS = {"Read", "Grep", "Glob", "Bash"}
DISPATCH_TOOLS = {"Agent", "Task", "Dispatch", "Spawn", "Delegate"}


def _text(path: Path = TEMPLATE) -> str:
    assert path.is_file(), "missing observer template: %s" % path
    return path.read_text(encoding="utf-8")


def _frontmatter_fields(text: str):
    assert text.startswith("---"), "the template must open with a YAML frontmatter block"
    end = text.find("\n---", 3)
    assert end != -1, "the frontmatter block is not closed"
    block, body = text[4:end], text[end + 4:]
    fields = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        assert sep, "frontmatter line without a key/value split: %r" % line
        fields[key.strip()] = value.strip()
    return fields, body


def _clause_interval(text: str) -> str:
    assert text.count(CLAUSE_BEGIN) == 1, "exactly one fast-fail begin delimiter is required"
    assert text.count(CLAUSE_END) == 1, "exactly one fast-fail end delimiter is required"
    begin = text.index(CLAUSE_BEGIN) + len(CLAUSE_BEGIN)
    end = text.index(CLAUSE_END)
    assert begin < end, "the fast-fail delimiter pair is inverted"
    return text[begin:end]


# --------------------------------------------------------------------------- #
# C-02 — neutral frontmatter
# --------------------------------------------------------------------------- #

def test_template_exists_with_neutral_frontmatter():
    from specify_cli import NEUTRAL_AGENT_METADATA_KEYS

    fields, body = _frontmatter_fields(_text())
    assert body.strip(), "the template body is empty"
    for key in ("name", "description", "user-invocable", "disable-model-invocation",
                "supervisor", "model-tier", "capability-tools", "skills", "run-turn-budget"):
        assert key in fields, "the frontmatter lacks the neutral key %r" % key
    assert fields["user-invocable"] == "false"
    assert fields["disable-model-invocation"] == "false"
    assert fields["supervisor"] == "false"
    assert fields["model-tier"] == "auto"
    assert fields["run-turn-budget"] == "500"
    assert fields["skills"].replace(" ", "") == "[]", "skills must be the empty list"
    unknown = sorted(set(fields) - set(NEUTRAL_AGENT_METADATA_KEYS))
    assert unknown == [], "non-neutral frontmatter keys: %r" % unknown

    tools_match = re.fullmatch(r"\[(.*?)\]", fields["capability-tools"])
    assert tools_match, "capability-tools must be declared as a bracketed list"
    tools = {item.strip() for item in tools_match.group(1).split(",") if item.strip()}
    assert tools, "the observer needs at least one read-class tool"
    assert tools <= READ_TOOLS, "read/search/shell-only: unexpected tools %r" % sorted(tools - READ_TOOLS)
    denied = tools & DISPATCH_TOOLS
    assert not denied, "dispatch-class tools are forbidden on the observer: %r" % sorted(denied)


# --------------------------------------------------------------------------- #
# C-03 — the role face is declared, not implied
# --------------------------------------------------------------------------- #

def test_role_face_is_observer_not_a_stage_seat():
    _, body = _frontmatter_fields(_text())
    assert re.search(r"\*\*Role\*\*:\s*`?observer`?", body), "the body does not declare the `observer` role"
    assert "exactly one SDD line" in body, "the role face does not scope the observer to one line"
    assert "no execution, evaluation, review or decision" in body, (
        "the role face does not exclude execution, evaluation, review and decision"
    )
    assert "not a stage executor, reviewer or reporter seat" in body, (
        "the seat boundary is not declared"
    )
    assert "no write authority over the development line" in body, (
        "the role face does not deny write authority over the line"
    )


# --------------------------------------------------------------------------- #
# C-04 — objectivity prohibition, verbatim
# --------------------------------------------------------------------------- #

def test_objectivity_prohibition_is_verbatim():
    text = _text()
    _, body = _frontmatter_fields(text)
    assert "不评价、不建议、不推断" in text, "the verbatim prohibition is absent"
    assert "deterministic projection" in body, (
        "entries are not declared deterministic projections of carrier facts"
    )
    for prohibited in ("evaluation", "suggestion", "causal inference", "severity", "recommendation"):
        assert prohibited in body, "the no-field rule does not name %r" % prohibited


# --------------------------------------------------------------------------- #
# C-05 — read domain and write surface are explicit
# --------------------------------------------------------------------------- #

def test_read_domain_and_write_surface_are_declared():
    _, body = _frontmatter_fields(_text())
    for token in ("state spine", "stage logs", "sentinels", "checkpoints", "git history",
                  "positive-evidence quartet", "execution records"):
        assert token in body, "the read domain does not name %r" % token
    assert "Driver conversation and stage prompt bodies are excluded from the read domain." in body, (
        "the read domain does not exclude the driver conversation and stage prompts"
    )
    assert "journal through `scripts/python/journal-utils.py`" in body, (
        "the journal surface does not go through the engine"
    )
    assert "own execution artifacts" in body, "the second write surface is not declared"
    assert "Writing the state spine, stage artifacts, feature registry or glossary is a defect" in body, (
        "the out-of-surface writes are not declared defects"
    )


# --------------------------------------------------------------------------- #
# C-06 — layer binding uses the current three-layer model
# --------------------------------------------------------------------------- #

def test_three_layer_binding_uses_the_current_model():
    _, body = _frontmatter_fields(_text())
    assert "Template → Instance → Execution" in body, "the three-layer chain is not named"
    assert "shared/definitions/agent-definitions.md" in body, (
        "the binding does not cite the three-layer owner"
    )
    assert AGENT_DEFINITIONS.is_file(), "the cited three-layer owner must exist"
    lowered = body.lower()
    assert "superagent" not in lowered, "the template references an unmerged-feature role model"
    assert "095" not in body, "the template references an unmerged-feature artifact"


# --------------------------------------------------------------------------- #
# C-08 — forbidden capabilities and the byte-identical fast-fail clause
# --------------------------------------------------------------------------- #

def test_forbidden_capabilities_are_declared():
    _, body = _frontmatter_fields(_text())
    assert "MUST NOT reference or load the driver skill or the SDD loop skill" in body, (
        "loading the driver/loop skill is not forbidden"
    )
    assert "MUST NOT host or start an SDD run" in body, "SDD run hosting is not forbidden"
    assert "user-visible reports, questions or approval requests" in body, (
        "user-visible reporting is not forbidden"
    )


def test_fast_fail_clause_is_byte_identical():
    owner = _clause_interval(FAST_FAIL_DOC.read_text(encoding="utf-8"))
    assert _clause_interval(_text()) == owner, (
        "the template's fast-fail clause is not byte-identical to its owner literal"
    )


# --------------------------------------------------------------------------- #
# C-09 — instance identity, creation duty and the subagent capability audit
# --------------------------------------------------------------------------- #

def test_instance_identity_derives_from_line_id():
    _, body = _frontmatter_fields(_text())
    assert "one Observer Instance per line" in body, "the one-instance-per-line duty is absent"
    assert "sdd-observer-<line_id>" in body, "the instance slug is not derived from line_id"
    assert "driver's startup step" in body, (
        "instance creation is not bound to the driver's startup step"
    )
    assert "create-agent" in body, "instance creation does not go through create-agent"
    assert "no stage command creates an observer instance" in body, (
        "stage commands are not barred from creating observer instances"
    )


def test_internal_subagents_are_serial_and_host_in_process_is_banned():
    _, body = _frontmatter_fields(_text())
    lowered = body.lower()
    assert "internal subagents are permitted" in lowered, "internal subagents are not permitted"
    assert "serial execution only" in lowered, "the serial-only rule is absent"
    assert "never a concurrency carrier" in lowered, "the no-concurrency-carrier rule is absent"
    assert "in-process" in lowered and "banned" in lowered, (
        "the host-internal in-process path is not banned"
    )
    assert "inherits this observer's read domain, write surface and objectivity structure" in lowered, (
        "subagents are not declared to inherit the observer's bounds"
    )
    assert "MUST NOT reference or load the driver skill" in body, (
        "no driver/loop load is permitted, but the ban is absent"
    )
    assert "MUST NOT host or start an SDD run" in body, (
        "no SDD run hosting is permitted, but the ban is absent"
    )
