"""Integration tests: dispatch injection survives the store-layout move (Feature 105, US3 / T018).

Contract: ``contracts/memory-and-injection.contract.md`` P-3 / P-4 / P-5; requirements
FR-010, FR-011, FR-012. The super↔sub protocol keeps its closed field sets — seven-field
downlink, four existing injections, five-element uplink — and the only change is that every
injected memory reference resolves under ``.specify/session/`` or ``.specify/knowledge/``
instead of the retired container.

The dispatch fixture: a child that declares ``memory-recall`` (the shipped
``agents/reporter.agent.md`` template) plus pre-seeded memory entries; the retrieval the
child performs is the shipped engine call, asserted against the new roots. The reverse
fixture writes a unique token into the feedback and exec-quant runtime stores only, and the
same retrieval MUST NOT return it (the memory boundary is verifiable).

Red-first (Constitution IV): authored before T019's wiring lands; execution readings land in
the feature's ``notes/red-first-evidence.md``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from script_api import load_engine_module, run_engine_in_process

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
MEMORY = ROOT / "scripts" / "python" / "memory-utils.py"
SUPERAGENT_OWNER = ROOT / "shared" / "definitions" / "superagent-definitions.md"
CHILD_TEMPLATE = ROOT / "agents" / "reporter.agent.md"
RECORD_SKILL = ROOT / "skills" / "internal" / "memory-record" / "SKILL.md"
RECALL_SKILL = ROOT / "skills" / "internal" / "memory-recall" / "SKILL.md"

SESSION_ROOT = ".specify/session/"
KNOWLEDGE_ROOT = ".specify/knowledge/"
RETIRED_ROOT = ".specify/memory"

# Closed field sets owned by shared/definitions/superagent-definitions.md § The super↔sub Protocol.
DOWNLINK_FIELDS = {
    "parent_identity",
    "child_label",
    "role_declaration",
    "dispatch_duty",
    "depth_position",
    "authority_ref",
    "return_channel",
}
INJECTION_OWNERS = (
    "shared/guidelines/fast-fail.md",          # fast-fail clause (§ 子代理派发注入)
    "subagent-definitions.md",                 # concurrency obligation (§ The Concurrency Obligation)
    "shared/guidelines/reporting-obligations.md",  # reporting duty
    "shared/definitions/re-anchoring-definitions.md",  # re-anchoring anchor digest
)
UPLINK_ELEMENTS = (
    "deliverable path",
    "evidence pointer",
    "anomaly line",
    "concurrency reading triple",
    "identity",
)


def _run(ws: Path, *args: str):
    return run_engine_in_process(MEMORY, ["--workspace-root", str(ws), *args])


def _record(ws: Path, scope: str, title: str, content: str, **extra: str) -> dict:
    args = ["--action", "record", "--scope", scope,
            "--source", "skill:test-dispatch", "--title", title, "--content", content]
    for key, value in extra.items():
        args += [f"--{key.replace('_', '-')}", value]
    result = _run(ws, *args)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


@pytest.fixture
def ws(tmp_path: Path) -> Path:
    (tmp_path / ".specify").mkdir(parents=True)
    return tmp_path


def _protocol_paragraph() -> str:
    text = SUPERAGENT_OWNER.read_text(encoding="utf-8")
    start = text.index("**Downlink.**")
    end = text.index("**Message classes.**")
    return text[start:end]


def test_downlink_field_set_is_closed_at_seven():
    downlink = _protocol_paragraph()
    assert "seven role fields" in downlink, "the protocol must still declare seven fields"
    extracted = {
        token
        for token in re.findall(r"`([a-z][a-z_]+)`", downlink)
        if "_" in token
    }
    assert extracted == DOWNLINK_FIELDS, (
        "the downlink field set changed; P-3 keeps it closed at seven: "
        f"extra={sorted(extracted - DOWNLINK_FIELDS)} missing={sorted(DOWNLINK_FIELDS - extracted)}"
    )


def test_four_injections_keep_their_owner_pointers():
    downlink = _protocol_paragraph()
    assert "four pre-existing injections" in downlink
    missing = [owner for owner in INJECTION_OWNERS if owner not in downlink]
    assert not missing, f"injection owner pointers disappeared: {missing}"


def test_uplink_carries_its_five_elements():
    paragraph = _protocol_paragraph()
    uplink = paragraph[paragraph.index("**Uplink.**"):]
    missing = [element for element in UPLINK_ELEMENTS if element not in uplink]
    assert not missing, f"uplink elements removed: {missing}"


def test_child_template_declares_memory_recall_and_refs_resolve_under_memory_roots(ws: Path):
    template = CHILD_TEMPLATE.read_text(encoding="utf-8")
    frontmatter = template.split("---", 2)[1]
    skills_line = re.search(r"(?m)^skills:\s*\[(.*?)\]\s*$", frontmatter)
    assert skills_line, "the reporter template must keep an inline skills declaration"
    assert "memory-recall" in [s.strip() for s in skills_line.group(1).split(",")], (
        "the dispatch fixture's child must still declare memory-recall (FR-011)"
    )

    session = _record(ws, "session", "Dispatch context",
                      "inject-token-session: the super agent decided to keep injection intact")
    knowledge = _record(ws, "knowledge", "Durable injection convention",
                        "inject-token-knowledge: recall stays the only retrieval source")

    recalled = _run(ws, "--action", "recall", "--scope", "all",
                    "--query", "inject-token", "--format", "json")
    assert recalled.returncode == 0, recalled.stderr
    matches = json.loads(recalled.stdout)["matches"]
    paths = {m["path"] for m in matches}
    assert {session["path"], knowledge["path"]} <= paths, (
        f"the child's retrieval must surface both seeded memory entries; got {sorted(paths)}"
    )
    for path in paths:
        assert path.startswith((SESSION_ROOT, KNOWLEDGE_ROOT)), (
            f"an injected memory reference resolved outside the memory stores: {path}"
        )
        assert not path.startswith(RETIRED_ROOT), "no injected reference may name the retired root"
        assert (ws / path).is_file(), f"an injected reference must resolve to a real entry: {path}"


def test_memory_skill_text_names_only_the_new_roots():
    for skill in (RECORD_SKILL, RECALL_SKILL):
        body = skill.read_text(encoding="utf-8")
        rel = skill.relative_to(ROOT).as_posix()
        assert f"{RETIRED_ROOT}/" not in body, (
            f"{rel} still injects a reference to the retired root"
        )
        assert SESSION_ROOT in body, f"{rel} must name the session tier's new root"
        assert KNOWLEDGE_ROOT in body, f"{rel} must name the knowledge tier's new root"


def test_runtime_store_token_is_not_recalled_as_memory(ws: Path):
    token = "reverse-token-9f3c1b"
    feedback_entry = ws / ".specify" / "feedback" / "20260101T000000Z-probe.md"
    feedback_entry.parent.mkdir(parents=True)
    feedback_entry.write_text(f"---\ntitle: probe\n---\n\n{token} lives only in feedback\n",
                              encoding="utf-8")
    exec_quant_entry = ws / ".specify" / "exec-quant" / "20260101T000000Z-probe.json"
    exec_quant_entry.parent.mkdir(parents=True)
    exec_quant_entry.write_text(json.dumps({"unit_id": "skill:probe", "note": token}),
                                encoding="utf-8")
    _record(ws, "session", "control entry", "a real memory entry to make recall non-vacuous")

    result = _run(ws, "--action", "recall", "--scope", "all",
                  "--query", token, "--format", "json")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    returned = "\n".join(json.dumps(m, ensure_ascii=False) for m in payload["matches"])
    assert token not in returned, (
        "memory recall returned text that only exists in runtime stores (FR-008 / SC-003)"
    )
    assert payload["matches"] == [], "the unique runtime-store token matches no memory entry"


def test_no_new_retrieval_source_or_payload_field(ws: Path):
    # The scope closed set is the memory tier fact; widening it would be a second source.
    module = load_engine_module(MEMORY)
    assert tuple(module.SCOPES) == ("session", "knowledge"), (
        f"the memory scope set changed: {module.SCOPES}"
    )

    _record(ws, "session", "only memory", "a session entry")
    (ws / ".specify" / "feedback").mkdir(parents=True, exist_ok=True)
    (ws / ".specify" / "feedback" / "noise.md").write_text(
        "---\ntitle: noise\n---\n\nruntime noise\n", encoding="utf-8")
    listed = _run(ws, "--action", "list", "--scope", "all", "--format", "json")
    assert listed.returncode == 0, listed.stderr
    items = json.loads(listed.stdout)["matches"]
    assert items, "the listing must be non-vacuous"
    assert all(i["path"].startswith((SESSION_ROOT, KNOWLEDGE_ROOT)) for i in items), (
        f"a listing source outside the memory stores appeared: "
        f"{[i['path'] for i in items]}"
    )
