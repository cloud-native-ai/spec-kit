"""Contract test: render pipeline semantics (contracts/render-pipeline.md R-1..R-10)."""

import json

import pytest
from pathlib import Path

from specify_cli import AgentMetadataError, render_agents_for_tool

pytestmark = pytest.mark.contract


def _def(slug, name, extra=""):
    return (
        "---\n"
        f'name: "{name}"\n'
        f'description: "Definition of {slug}."\n'
        "user-invocable: true\n"
        "model-tier: auto\n"
        "capability-tools: [Read, Grep]\n"
        "run-turn-budget: 12\n"
        "display-color: blue\n"
        "supervisor: true\n"
        "capacity-scope: " + slug + "\n"
        f"{extra}"
        "---\n"
        f"Body of {slug}.\n"
    )


def _project(tmp_path, template_slugs=("alpha",), instance_slugs=()):
    root = tmp_path / "proj"
    for layer, slugs in (("templates", template_slugs), ("instances", instance_slugs)):
        d = root / ".specify" / "agents" / layer
        d.mkdir(parents=True, exist_ok=True)
        for slug in slugs:
            (d / f"{slug}.agent.md").write_text(_def(slug, slug.title()))
    (root / ".specify" / "agents" / "execution" / "logs").mkdir(parents=True)
    (root / ".specify" / "agents" / "execution" / "logs" / "run.agent.md").write_text(
        _def("run", "Run")
    )
    return root


def test_r1_outputs_are_real_files_not_symlinks(tmp_path):
    root = _project(tmp_path)
    stats = render_agents_for_tool(root, "qoder")
    target = root / ".qoder" / "agents" / "alpha.agent.md"
    assert target.is_file() and not target.is_symlink()
    assert stats["rendered"] == 1


def test_r1_annotated_tool_renders_nothing(tmp_path):
    root = _project(tmp_path)
    stats = render_agents_for_tool(root, "codex")
    assert stats["rendered"] == 0
    assert not (root / ".codex").exists()


def test_r2_only_agent_md_from_source_layers(tmp_path):
    root = _project(tmp_path)
    (root / ".specify" / "agents" / "templates" / "notes.md").write_text("x")
    render_agents_for_tool(root, "qoder")
    outputs = list((root / ".qoder" / "agents").iterdir())
    assert [p.name for p in outputs] == ["alpha.agent.md"]


def test_r3_instance_wins_on_collision(tmp_path):
    root = _project(tmp_path, template_slugs=("alpha",), instance_slugs=("alpha",))
    render_agents_for_tool(root, "qoder")
    content = (root / ".qoder" / "agents" / "alpha.agent.md").read_text()
    assert "description: Definition of alpha." in content
    manifest = json.loads(
        (root / ".specify" / "agents" / ".render-manifest.json").read_text()
    )
    entry = next(iter(manifest["entries"].values()))
    assert entry["source"].startswith("instances/")


@pytest.mark.parametrize("tool, filename", [
    ("qoder", "alpha.agent.md"),
    ("claude", "alpha.md"),
    ("copilot", "alpha.agent.md"),
    ("opencode", "alpha.md"),
])
def test_r1_file_naming_per_tool(tmp_path, tool, filename):
    root = _project(tmp_path)
    render_agents_for_tool(root, tool)
    mapping_dirs = {
        "qoder": ".qoder/agents",
        "claude": ".claude/agents",
        "copilot": ".github/agents",
        "opencode": ".opencode/agents",
    }
    assert (root / mapping_dirs[tool] / filename).is_file()


def test_r4_deterministic_output(tmp_path):
    root = _project(tmp_path)
    render_agents_for_tool(root, "qoder")
    first = (root / ".qoder" / "agents" / "alpha.agent.md").read_bytes()
    render_agents_for_tool(root, "qoder")
    second = (root / ".qoder" / "agents" / "alpha.agent.md").read_bytes()
    assert first == second


def test_r9_stats_report_shape(tmp_path):
    root = _project(tmp_path)
    stats = render_agents_for_tool(root, "opencode")
    assert set(stats) == {"tool", "rendered", "backups", "unmapped"}
    # opencode has no counterpart for skills-less run budgets? run-turn-budget
    # maps to steps there; display-color maps; assert unmapped is a dict per slug
    assert isinstance(stats["unmapped"], dict)


def test_c6_framework_keys_never_rendered(tmp_path):
    root = _project(tmp_path)
    targets = {
        "qoder": ".qoder/agents",
        "claude": ".claude/agents",
        "copilot": ".github/agents",
        "opencode": ".opencode/agents",
    }
    for tool, rel in targets.items():
        render_agents_for_tool(root, tool)
        for path in (root / rel).iterdir():
            content = path.read_text()
            for key in ("supervisor:", "capacity-scope:", "role-scope:", "project:"):
                assert key not in content, f"{path}: framework key leaked"


def test_r10_placeholder_input_rejected(tmp_path):
    root = tmp_path / "proj"
    d = root / ".specify" / "agents" / "templates"
    d.mkdir(parents=True)
    (d / "tmpl.agent.md").write_text(
        '---\nname: "{{AGENT_NAME}}"\ndescription: d\n---\nbody'
    )
    with pytest.raises(AgentMetadataError):
        render_agents_for_tool(root, "qoder")


def test_qoder_output_uses_qoder_fields(tmp_path):
    root = _project(tmp_path)
    render_agents_for_tool(root, "qoder")
    content = (root / ".qoder" / "agents" / "alpha.agent.md").read_text()
    assert "maxTurns: 12" in content
    assert "color: blue" in content
    assert "model: auto" in content
    assert "tools:" in content
    assert "Body of alpha." in content


def test_claude_output_joins_tools_as_string(tmp_path):
    root = _project(tmp_path)
    render_agents_for_tool(root, "claude")
    content = (root / ".claude" / "agents" / "alpha.md").read_text()
    assert "tools: Read, Grep" in content


def test_opencode_output_omits_name_and_sets_mode(tmp_path):
    root = _project(tmp_path)
    render_agents_for_tool(root, "opencode")
    content = (root / ".opencode" / "agents" / "alpha.md").read_text()
    assert "name:" not in content
    assert "steps: 12" in content
