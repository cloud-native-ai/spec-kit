"""Contract test: render-agents CLI subcommand + team-scope neutral key
(contracts/render-trigger-cli.md C-1..C-6, contracts/seat-instantiation.md C-1..C-2)."""

import pytest
from pathlib import Path

from specify_cli import load_project_agent_definitions

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
        f"{extra}"
        "---\n"
        f"Body of {slug}.\n"
    )


def _project(tmp_path, template_slugs=("alpha",), instance_slugs=(), extra_by_slug=None):
    root = tmp_path / "proj"
    for layer, slugs in (("templates", template_slugs), ("instances", instance_slugs)):
        d = root / ".specify" / "agents" / layer
        d.mkdir(parents=True, exist_ok=True)
        for slug in slugs:
            extra = (extra_by_slug or {}).get(slug, "")
            (d / f"{slug}.agent.md").write_text(_def(slug, slug.title(), extra))
    return root


def _invoke(args, cwd):
    """Invoke the render-agents subcommand through the real typer CLI surface.

    In-process via CliRunner (the package has no __main__.py, so
    `python -m specify_cli` is not an executable form); chdir to the project
    root because render_agents resolves the project as Path.cwd().
    """
    import os

    from typer.testing import CliRunner

    from specify_cli import app

    prev = os.getcwd()
    os.chdir(cwd)
    try:
        result = CliRunner().invoke(app, args)
        return result
    finally:
        os.chdir(prev)


# --- C-1/C-2: command shape and value domain ---------------------------------

def test_c1_subcommand_exists_and_renders(tmp_path):
    root = _project(tmp_path)
    proc = _invoke(["render-agents", "--ai", "qoder"], cwd=root)
    assert proc.exit_code == 0, proc.output
    target = root / ".qoder" / "agents" / "alpha.agent.md"
    assert target.is_file() and not target.is_symlink()
    content = target.read_text()
    assert "name: Alpha" in content
    # C-6: capacity fields carried by the registered type
    assert "tools" in content and "maxTurns" in content


def test_c2_annotated_tool_rejected_with_legal_values(tmp_path):
    root = _project(tmp_path)
    proc = _invoke(["render-agents", "--ai", "codex"], cwd=root)
    assert proc.exit_code != 0
    combined = proc.output
    for legal in ("qoder", "claude", "copilot", "opencode"):
        assert legal in combined, f"legal value {legal} not listed: {combined}"


def test_c2_unknown_tool_rejected(tmp_path):
    root = _project(tmp_path)
    proc = _invoke(["render-agents", "--ai", "no-such-tool"], cwd=root)
    assert proc.exit_code != 0


def test_c4_empty_layers_is_legal_success(tmp_path):
    root = tmp_path / "empty-proj"
    (root / ".specify").mkdir(parents=True)
    proc = _invoke(["render-agents", "--ai", "qoder"], cwd=root)
    assert proc.exit_code == 0, proc.output
    assert "rendered 0" in (proc.output)


def test_c5_placeholder_definition_rejected(tmp_path):
    root = _project(
        tmp_path,
        template_slugs=(),
        instance_slugs=("seat",),
        extra_by_slug={"seat": 'name: "{{AGENT_NAME}}"\n'},
    )
    proc = _invoke(["render-agents", "--ai", "qoder"], cwd=root)
    assert proc.exit_code != 0
    combined = proc.output
    assert "seat" in combined and "PLACEHOLDER" in combined.upper()


# --- C-3: delegation semantics (renderer, not a copy) -------------------------

def test_c3_delegates_to_renderer_stats_summary(tmp_path):
    root = _project(tmp_path)
    proc = _invoke(["render-agents", "--ai", "qoder"], cwd=root)
    assert proc.exit_code == 0, proc.output
    assert "rendered 1" in (proc.output)
    # manifest written by the renderer itself
    manifest = root / ".specify" / "agents" / ".render-manifest.json"
    assert manifest.is_file()


# --- seat-instantiation C-1/C-2: team-scope neutral key -----------------------

def test_seat_c1_team_scope_key_accepted(tmp_path):
    root = _project(
        tmp_path,
        instance_slugs=("seat",),
        extra_by_slug={"seat": "team-scope: my-team\n"},
    )
    defs = load_project_agent_definitions(root)
    slugs = [d["slug"] for d in defs]
    assert "seat" in slugs


def test_seat_c1_team_scope_not_rendered(tmp_path):
    root = _project(
        tmp_path,
        instance_slugs=("seat",),
        extra_by_slug={"seat": "team-scope: my-team\n"},
    )
    proc = _invoke(["render-agents", "--ai", "qoder"], cwd=root)
    assert proc.exit_code == 0, proc.output
    content = (root / ".qoder" / "agents" / "seat.agent.md").read_text()
    assert "team-scope" not in content


def test_seat_c1_unknown_key_still_rejected(tmp_path):
    root = _project(
        tmp_path,
        instance_slugs=("seat",),
        extra_by_slug={"seat": "bogus-key: whatever\n"},
    )
    with pytest.raises(Exception) as excinfo:
        load_project_agent_definitions(root)
    assert "bogus-key" in str(excinfo.value)
