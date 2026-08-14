"""Contract test: migration from the retired symlink model (render-pipeline.md R-8/R-6/R-5).

Replaces tests/contract/test_agents_symlink.py (Feature 044, R-11 retirement).
"""

import json

import pytest
from pathlib import Path

from specify_cli import render_agents_for_tool

pytestmark = pytest.mark.contract

NEUTRAL_DEF = (
    "---\n"
    'name: "Alpha"\n'
    'description: "Alpha definition."\n'
    "run-turn-budget: 10\n"
    "---\n"
    "Body of alpha.\n"
)


def _seed(tmp_path, slugs=("alpha",)):
    root = tmp_path / "proj"
    d = root / ".specify" / "agents" / "templates"
    d.mkdir(parents=True)
    for slug in slugs:
        (d / f"{slug}.agent.md").write_text(NEUTRAL_DEF.replace("Alpha", slug.title()).replace("alpha", slug))
    return root


def test_legacy_per_file_symlinks_replaced_by_real_files(tmp_path):
    root = _seed(tmp_path)
    tool_dir = root / ".qoder" / "agents"
    tool_dir.mkdir(parents=True)
    source = root / ".specify" / "agents" / "templates" / "alpha.agent.md"
    (tool_dir / "alpha.agent.md").symlink_to(source)

    render_agents_for_tool(root, "qoder")

    output = tool_dir / "alpha.agent.md"
    assert output.is_file() and not output.is_symlink()
    assert "maxTurns: 10" in output.read_text()


def test_legacy_whole_dir_symlink_replaced(tmp_path):
    root = _seed(tmp_path)
    (root / ".qoder").mkdir(parents=True)
    (root / ".qoder" / "agents").symlink_to(root / ".specify" / "agents" / "templates")

    render_agents_for_tool(root, "qoder")

    tool_dir = root / ".qoder" / "agents"
    assert tool_dir.is_dir() and not tool_dir.is_symlink()
    assert (tool_dir / "alpha.agent.md").is_file()


def test_stale_outputs_pruned_when_source_removed(tmp_path):
    root = _seed(tmp_path, slugs=("alpha", "beta"))
    render_agents_for_tool(root, "qoder")
    assert (root / ".qoder" / "agents" / "beta.agent.md").exists()

    (root / ".specify" / "agents" / "templates" / "beta.agent.md").unlink()
    render_agents_for_tool(root, "qoder")

    assert not (root / ".qoder" / "agents" / "beta.agent.md").exists()
    assert (root / ".qoder" / "agents" / "alpha.agent.md").exists()


def test_modified_stale_output_is_backed_up_before_prune(tmp_path):
    root = _seed(tmp_path, slugs=("alpha", "beta"))
    render_agents_for_tool(root, "qoder")
    stale = root / ".qoder" / "agents" / "beta.agent.md"
    stale.write_text(stale.read_text() + "\nuser edit\n")

    (root / ".specify" / "agents" / "templates" / "beta.agent.md").unlink()
    stats = render_agents_for_tool(root, "qoder")

    assert not stale.exists()
    assert len(stats["backups"]) == 1
    assert Path(stats["backups"][0]).read_text().endswith("user edit\n")


def test_modified_rendered_output_backed_up_then_refreshed(tmp_path):
    root = _seed(tmp_path)
    render_agents_for_tool(root, "qoder")
    output = root / ".qoder" / "agents" / "alpha.agent.md"
    output.write_text(output.read_text() + "\nhand modification\n")

    stats = render_agents_for_tool(root, "qoder")

    assert len(stats["backups"]) == 1
    backup = Path(stats["backups"][0])
    assert backup.exists() and "hand modification" in backup.read_text()
    assert "hand modification" not in output.read_text()
    manifest = json.loads(
        (root / ".specify" / "agents" / ".render-manifest.json").read_text()
    )
    assert manifest["entries"], "manifest must track the refreshed output"


def test_execution_layer_never_rendered(tmp_path):
    root = _seed(tmp_path)
    exec_dir = root / ".specify" / "agents" / "execution" / "logs"
    exec_dir.mkdir(parents=True)
    (exec_dir / "ghost.agent.md").write_text(NEUTRAL_DEF)

    render_agents_for_tool(root, "qoder")

    names = {p.name for p in (root / ".qoder" / "agents").iterdir()}
    assert names == {"alpha.agent.md"}


def test_r7_tool_switch_keeps_previous_tool_outputs(tmp_path):
    root = _seed(tmp_path)
    render_agents_for_tool(root, "qoder")
    qoder_output = root / ".qoder" / "agents" / "alpha.agent.md"
    assert qoder_output.is_file()

    render_agents_for_tool(root, "claude")

    assert qoder_output.is_file(), (
        "rendering for a second tool must not prune the first tool's outputs (R-7)"
    )
    assert (root / ".claude" / "agents" / "alpha.md").is_file()
    import json as _json

    manifest = _json.loads(
        (root / ".specify" / "agents" / ".render-manifest.json").read_text()
    )
    assert any(k.startswith(".qoder/") for k in manifest["entries"])
    assert any(k.startswith(".claude/") for k in manifest["entries"])
