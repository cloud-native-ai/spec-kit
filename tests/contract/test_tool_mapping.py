"""Contract test: tool metadata mapping (contracts/tool-mapping.md M-1..M-7)."""

import inspect

import pytest

import specify_cli
from specify_cli import AGENT_CONFIG, NEUTRAL_AGENT_METADATA_KEYS

pytestmark = pytest.mark.contract

RENDER_TOOLS = {"qoder", "claude", "copilot", "opencode"}
ANNOTATED_TOOLS = {"codex", "hermes"}

EXPECTED_TARGET_DIRS = {
    "qoder": ".qoder/agents",
    "claude": ".claude/agents",
    "copilot": ".github/agents",
    "opencode": ".opencode/agents",
}


def _mapping():
    return specify_cli._AGENT_METADATA_MAPPING


def test_m1_mapping_covers_every_supported_tool_dynamically():
    assert set(_mapping()) == set(AGENT_CONFIG), (
        "mapping must cover the AGENT_CONFIG key domain exactly"
    )
    for tool, row in _mapping().items():
        assert row["mode"] in ("render", "annotated"), tool


def test_m1_render_annotated_split():
    render = {t for t, r in _mapping().items() if r["mode"] == "render"}
    annotated = {t for t, r in _mapping().items() if r["mode"] == "annotated"}
    assert render == RENDER_TOOLS
    assert annotated == ANNOTATED_TOOLS


def test_m2_every_row_has_provenance_and_none_pending():
    for tool, row in _mapping().items():
        assert row.get("provenance"), f"{tool}: missing provenance"
        assert "待核实" not in str(row), f"{tool}: unverified row at delivery"


def test_m2_annotated_rows_carry_rationale():
    for tool in ANNOTATED_TOOLS:
        assert _mapping()[tool].get("note"), f"{tool}: annotated row needs a note"


def test_m3_target_dir_matrix():
    for tool, expected in EXPECTED_TARGET_DIRS.items():
        assert _mapping()[tool]["target_dir"] == expected, tool


def test_m4_every_render_key_has_an_explicit_rule():
    render_keys = {
        k for k, (_d, _v, renders) in NEUTRAL_AGENT_METADATA_KEYS.items() if renders
    }
    framework_keys = {
        k for k, (_d, _v, renders) in NEUTRAL_AGENT_METADATA_KEYS.items() if not renders
    }
    for tool in RENDER_TOOLS:
        fields = _mapping()[tool]["fields"]
        assert set(fields) == render_keys, (
            f"{tool}: fields must cover every rendering neutral key explicitly "
            f"(None = unmapped, D3 path)"
        )
        assert not (set(fields) & framework_keys), tool


def test_m6_unmapped_rules_are_none_not_guesses():
    for tool in RENDER_TOOLS:
        for key, rule in _mapping()[tool]["fields"].items():
            if rule is None:
                continue
            assert "emit" in rule, f"{tool}.{key}: rule must name the target field"


def test_m7_single_source_no_legacy_link_table():
    assert not hasattr(specify_cli, "_AGENT_LINK_DIRS"), (
        "the legacy symlink table must be retired (R-11)"
    )
    source = inspect.getsource(specify_cli.render_agents_for_tool)
    assert "_AGENT_METADATA_MAPPING" in source


def test_m5_unmapped_policy_is_documented_at_the_source():
    src = open(specify_cli.__file__, encoding="utf-8").read()
    assert "unmapped-field policy" in src
