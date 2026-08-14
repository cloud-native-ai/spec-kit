"""Contract test: neutral agent metadata schema (contracts/neutral-metadata-schema.md).

Covers C-1 (key-set closure), C-2 (required/defaults), C-3 (kebab-case),
C-5 (body carries no distribution parameters), C-7 (placeholder rejection),
C-8 (discovery without reading the body). Uses synthetic fixtures so the
suite stays green independently of the repo's migration timeline (US2/US5).
"""

import re

import pytest

from specify_cli import (
    AgentMetadataError,
    FORBIDDEN_AGENT_METADATA_KEYS,
    NEUTRAL_AGENT_METADATA_KEYS,
    NEUTRAL_AGENT_FRAMEWORK_KEYS,
    split_agent_frontmatter,
    validate_agent_metadata,
)

pytestmark = pytest.mark.contract

NEUTRAL_SAMPLE = """---
name: "Sample Agent"
description: "A synthetic agent for contract tests."
user-invocable: true
disable-model-invocation: false
model-tier: auto
capability-tools: [Read, Grep, Glob]
skills: [memory-recall]
run-turn-budget: 12
display-color: blue
supervisor: true
capacity-scope: sample-agent
---
You are a **Sample Agent**.

## Identity & Responsibilities

You operate on business artifacts.
"""


def test_full_neutral_definition_parses():
    metadata, body = validate_agent_metadata("sample.agent.md", NEUTRAL_SAMPLE)
    assert metadata["name"] == "Sample Agent"
    assert metadata["capability-tools"] == ["Read", "Grep", "Glob"]
    assert metadata["run-turn-budget"] == 12
    assert body.startswith("You are a **Sample Agent**.")


def test_c1_unknown_key_fails_and_names_file_and_key(tmp_path):
    text = NEUTRAL_SAMPLE.replace("run-turn-budget", "totally-unknown-key")
    target = tmp_path / "rogue.agent.md"
    target.write_text(text)
    with pytest.raises(AgentMetadataError) as exc:
        validate_agent_metadata(target, text)
    assert str(target) in str(exc.value)
    assert "totally-unknown-key" in str(exc.value)
    assert exc.value.keys == ("totally-unknown-key",)


@pytest.mark.parametrize("key", sorted(FORBIDDEN_AGENT_METADATA_KEYS))
def test_c4_every_forbidden_dialect_key_is_rejected(key):
    text = f"---\nname: X\ndescription: d\n{key}: whatever\n---\nbody"
    with pytest.raises(AgentMetadataError) as exc:
        validate_agent_metadata("t.agent.md", text)
    assert key in str(exc.value)


def test_c2_missing_required_key_fails():
    text = "---\ndescription: d\n---\nbody"
    with pytest.raises(AgentMetadataError) as exc:
        validate_agent_metadata("t.agent.md", text)
    assert "name" in str(exc.value)


@pytest.mark.parametrize(
    "line, fragment",
    [
        ("model-tier: turbo", "expects one of"),
        ("run-turn-budget: 0", "positive integer"),
        ("user-invocable: yes", "expects a boolean"),
        ("capability-tools: Read", "list of non-empty strings"),
        ("name: \"\"", "non-empty string"),
    ],
)
def test_c2_domain_violations_fail(line, fragment):
    text = f"---\nname: X\ndescription: d\n{line}\n---\nbody"
    with pytest.raises(AgentMetadataError) as exc:
        validate_agent_metadata("t.agent.md", text)
    assert fragment in str(exc.value)


def test_c3_camelcase_key_fails():
    text = "---\nname: X\ndescription: d\nmaxTurns: 5\n---\nbody"
    with pytest.raises(AgentMetadataError):
        validate_agent_metadata("t.agent.md", text)


def test_c5_metadata_extraction_needs_no_body_semantics():
    metadata, _body = validate_agent_metadata("sample.agent.md", NEUTRAL_SAMPLE)
    # Every metadata value is obtained from the frontmatter alone.
    fm_lines, _ = split_agent_frontmatter(NEUTRAL_SAMPLE)
    assert len(fm_lines) == len(NEUTRAL_AGENT_METADATA_KEYS)
    assert set(metadata) == set(NEUTRAL_AGENT_METADATA_KEYS)


def test_c5_body_carries_no_distribution_parameters():
    _metadata, body = validate_agent_metadata("sample.agent.md", NEUTRAL_SAMPLE)
    for pattern in (
        r"maxTurns\s*:",
        r"run-turn-budget\s*:",
        r"display-color\s*:",
        r"capability-tools\s*:",
    ):
        assert re.search(pattern, body) is None


def test_c7_placeholders_in_metadata_rejected():
    text = '---\nname: "{{AGENT_NAME}}"\ndescription: d\n---\nbody'
    with pytest.raises(AgentMetadataError) as exc:
        validate_agent_metadata("t.agent.md", text)
    assert "placeholder" in str(exc.value)


def test_c6_framework_keys_are_marked_non_rendering():
    assert NEUTRAL_AGENT_FRAMEWORK_KEYS == {"supervisor", "capacity-scope"}
    for key in NEUTRAL_AGENT_FRAMEWORK_KEYS:
        _domain, _default, renders = NEUTRAL_AGENT_METADATA_KEYS[key]
        assert renders is False, key


def test_c8_discovery_enumerates_without_body():
    metadata, _ = validate_agent_metadata("sample.agent.md", NEUTRAL_SAMPLE)
    # Discovery needs only name/description from the metadata block.
    assert metadata["name"] and metadata["description"]


def test_missing_frontmatter_fails():
    with pytest.raises(AgentMetadataError) as exc:
        validate_agent_metadata("t.agent.md", "just a body")
    assert "missing frontmatter" in str(exc.value)


# --- Shared read-path entry point (T005) ---------------------------------


def _write_def(directory, slug, name):
    directory.mkdir(parents=True, exist_ok=True)
    text = (
        "---\n"
        f'name: "{name}"\n'
        f'description: "Definition of {slug}."\n'
        "model-tier: auto\n"
        "---\n"
        f"Body of {slug}.\n"
    )
    (directory / f"{slug}.agent.md").write_text(text)


def test_collect_reads_templates_and_instances(tmp_path):
    from specify_cli import load_project_agent_definitions

    specify = tmp_path / ".specify" / "agents"
    _write_def(specify / "templates", "alpha", "Alpha")
    _write_def(specify / "instances", "beta", "Beta")
    defs = load_project_agent_definitions(tmp_path)
    assert {d["slug"] for d in defs} == {"alpha", "beta"}
    assert all(d["metadata"]["name"] for d in defs)


def test_collect_instance_wins_on_name_collision(tmp_path):
    from specify_cli import load_project_agent_definitions

    specify = tmp_path / ".specify" / "agents"
    _write_def(specify / "templates", "alpha", "Alpha Template")
    _write_def(specify / "instances", "alpha", "Alpha Instance")
    defs = load_project_agent_definitions(tmp_path)
    assert len(defs) == 1
    assert defs[0]["metadata"]["name"] == "Alpha Instance"
    assert defs[0]["source"] == "instances/alpha.agent.md"


def test_collect_fails_fast_on_invalid_metadata(tmp_path):
    from specify_cli import load_project_agent_definitions

    specify = tmp_path / ".specify" / "agents"
    _write_def(specify / "templates", "good", "Good")
    bad = specify / "templates" / "bad.agent.md"
    bad.write_text("---\nname: Bad\ndescription: d\nmaxTurns: 9\n---\nbody")
    with pytest.raises(AgentMetadataError) as exc:
        load_project_agent_definitions(tmp_path)
    assert "bad.agent.md" in str(exc.value)
    assert "maxTurns" in str(exc.value)


def test_collect_ignores_non_agent_files_and_subdirs(tmp_path):
    from specify_cli import load_project_agent_definitions

    specify = tmp_path / ".specify" / "agents"
    _write_def(specify / "templates", "alpha", "Alpha")
    (specify / "templates" / "notes.md").write_text("not an agent")
    exec_dir = specify / "execution" / "logs"
    exec_dir.mkdir(parents=True)
    (exec_dir / "run.agent.md").write_text("---\nname: X\ndescription: d\n---\nb")
    defs = load_project_agent_definitions(tmp_path)
    assert {d["slug"] for d in defs} == {"alpha"}
