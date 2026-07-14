"""Integration tests: fresh init installs the shared reference directory and re-init retains it.

Feature 029, contract C-INSTALL.
"""

from pathlib import Path

from specify_cli import copy_local_templates

TEN_DOCS = [
    "user-input-protocol.md",
    "feature-integration.md",
    "agent-configuration.md",
    "checklist-methodology.md",
    "requirements-guidelines.md",
    "dfx-catalog.md",
    "clarify-taxonomy.md",
    "ignore-patterns.md",
    "tool-definitions.md",
    "feedback-step.md",
]


def _make_resource_with_shared(tmp_path: Path) -> Path:
    r = tmp_path / "resource"
    (r / "templates" / "commands").mkdir(parents=True)
    (r / "templates" / "commands" / "requirements.md").write_text(
        "See shared/workflow/user-input-protocol.md\n", encoding="utf-8"
    )
    (r / "memory").mkdir(parents=True)
    (r / "memory" / "constitution.md").write_text("# C", encoding="utf-8")
    (r / "memory" / "features.md").write_text("# F", encoding="utf-8")
    (r / "scripts").mkdir(parents=True)
    (r / "skills").mkdir(parents=True)
    shared = r / "shared" / "workflow"
    shared.mkdir(parents=True)
    for name in TEN_DOCS:
        (shared / name).write_text(f"# {name}\n", encoding="utf-8")
    return r


def test_fresh_init_installs_shared_directory(monkeypatch, tmp_path: Path):
    resource = _make_resource_with_shared(tmp_path)
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource)

    project = tmp_path / "proj"
    copy_local_templates(project, "claude", "sh")

    installed = project / ".specify" / "shared" / "workflow"
    assert installed.is_dir()
    present = {p.name for p in installed.glob("*.md")}
    assert set(TEN_DOCS).issubset(present)


def test_reinit_retains_shared_directory(monkeypatch, tmp_path: Path):
    resource = _make_resource_with_shared(tmp_path)
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource)

    project = tmp_path / "proj"
    copy_local_templates(project, "claude", "sh")

    sentinel = project / ".specify" / "shared" / "workflow" / ".sentinel"
    sentinel.write_text("keep", encoding="utf-8")

    # Re-init over the existing workspace must not wipe the shared directory.
    copy_local_templates(project, "claude", "sh")
    assert sentinel.exists()
