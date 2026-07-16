"""Integration tests: fresh init ships the framework-owned .specify/.gitignore.

The transient /speckit.history and /speckit.team `.work/` scratch dirs are created
inside a target project's own `.specify/` tree during daily development, so the
ignore rules must travel with `init` rather than living only in spec-kit's repo
root `.gitignore`.
"""

from pathlib import Path

from specify_cli import copy_local_templates

TEMPLATE_NAME = "gitignore-specify-template"
TEMPLATE_BODY = (
    "# /speckit.history scratch (de-noised transcripts); .md docs + .manifest.json are tracked\n"
    "history/.work/\n"
    "\n"
    "# /speckit.team run intermediate workspace (transient); team defs + runs/ reports stay tracked\n"
    "teams/.work/\n"
)


def _make_resource(tmp_path: Path) -> Path:
    r = tmp_path / "resource"
    (r / "templates" / "commands").mkdir(parents=True)
    (r / "templates" / "commands" / "requirements.md").write_text(
        "placeholder\n", encoding="utf-8"
    )
    (r / "templates" / TEMPLATE_NAME).write_text(TEMPLATE_BODY, encoding="utf-8")
    (r / "memory").mkdir(parents=True)
    (r / "memory" / "constitution.md").write_text("# C", encoding="utf-8")
    (r / "memory" / "features.md").write_text("# F", encoding="utf-8")
    (r / "scripts").mkdir(parents=True)
    (r / "skills").mkdir(parents=True)
    return r


def test_fresh_init_ships_specify_gitignore(monkeypatch, tmp_path: Path):
    resource = _make_resource(tmp_path)
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource)

    project = tmp_path / "proj"
    copy_local_templates(project, "claude", "sh")

    installed = project / ".specify" / ".gitignore"
    assert installed.is_file(), ".specify/.gitignore must be shipped on init"
    body = installed.read_text(encoding="utf-8")
    assert "history/.work/" in body
    assert "teams/.work/" in body


def test_reinit_refreshes_specify_gitignore(monkeypatch, tmp_path: Path):
    resource = _make_resource(tmp_path)
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource)

    project = tmp_path / "proj"
    copy_local_templates(project, "claude", "sh")

    # Re-init over the existing workspace must keep the framework-owned file current.
    copy_local_templates(project, "claude", "sh")
    installed = project / ".specify" / ".gitignore"
    assert installed.is_file()
    assert "teams/.work/" in installed.read_text(encoding="utf-8")
