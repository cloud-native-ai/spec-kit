"""Integration tests: mount-mode Hugo scaffold behaviour on a real docs tree.

Exercises the create-pages mode-B scaffolder: the mount rules that keep the docs
tree pure Markdown, the anti-churn guarantee (a repeat run converges nothing), the
never-clobber guarantee, the cross-engine invariant with docs-utils.py, and — when
the binary is present — a real build. The capability is optional; these scenarios
skip when the scaffolder is not installed.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "create-pages" / "scripts" / "scaffold-hugo.py"
DOCS_UTILS = REPO_ROOT / "scripts" / "python" / "docs-utils.py"

pytestmark = pytest.mark.skipif(
    not SCRIPT.is_file(),
    reason="optional capability: create-pages mount-mode scaffolder is not installed",
)

SCAFFOLD_FILES = (
    "hugo.toml",
    ".gitignore",
    "layouts/index.html",
    "layouts/_default/baseof.html",
    "layouts/_default/list.html",
    "layouts/_default/single.html",
    "layouts/_default/_markup/render-link.html",
    "layouts/_default/_markup/render-image.html",
    "static/css/site.css",
)


def run(root: Path, *args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), *args],
        capture_output=True, text=True,
    )
    assert proc.stdout, proc.stderr
    return json.loads(proc.stdout)


def make_docs(root: Path) -> None:
    """A documentation space shaped like the desired-state baseline."""
    (root / "README.md").write_text("# Probe\n\nSee [overview](docs/concepts/overview.md).\n",
                                    encoding="utf-8")
    for name in ("concepts", "tutorials", "tasks", "decisions", "notes", "archive",
                 "reference/commands", "assets"):
        (root / "docs" / name).mkdir(parents=True)
    docs = root / "docs"
    (docs / "concepts/overview.md").write_text(
        "# Overview\n\nBack to [quickstart](../tutorials/quickstart.md).\n", encoding="utf-8")
    # media stored beside its prose
    (docs / "concepts/diagram.svg").write_text("<svg xmlns='http://www.w3.org/2000/svg'/>",
                                               encoding="utf-8")
    (docs / "concepts/inline.md").write_text("# Inline\n\n![d](diagram.svg)\n", encoding="utf-8")
    (docs / "tutorials/quickstart.md").write_text(
        "# Quickstart\n\n![flow](../assets/flow.svg)\n\n"
        "See [overview](../concepts/overview.md) and [tasks](../tasks/index.md).\n",
        encoding="utf-8")
    (docs / "tasks/index.md").write_text("# Tasks\n", encoding="utf-8")
    (docs / "tasks/task-one.md").write_text("# Task one\n", encoding="utf-8")
    (docs / "decisions/index.md").write_text("# ADR index\n", encoding="utf-8")
    (docs / "decisions/0001-pick-hugo.md").write_text("# ADR-0001: pick hugo\n", encoding="utf-8")
    (docs / "decisions/template.md").write_text("# ADR-NNNN: title\n", encoding="utf-8")
    (docs / "notes/index.md").write_text("# Notes\n", encoding="utf-8")
    (docs / "archive/old-note.md").write_text("# Old\n", encoding="utf-8")
    (docs / "reference/commands/docs.md").write_text(
        "# docs command\n\nUp to [overview](../../concepts/overview.md).\n", encoding="utf-8")
    # media-only directory (no Markdown at all)
    (docs / "assets/flow.svg").write_text("<svg xmlns='http://www.w3.org/2000/svg'/>",
                                          encoding="utf-8")


def fingerprint(docs: Path) -> dict[str, str]:
    return {
        path.relative_to(docs).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(docs.rglob("*")) if path.is_file()
    }


@pytest.mark.integration
def test_scaffold_creates_the_full_project(tmp_path: Path):
    make_docs(tmp_path)
    out = run(tmp_path, "--action", "scaffold", "--site-title", "Probe")
    assert out["clean"] is True
    assert {f["action"] for f in out["files"]} == {"created"}
    missing = [rel for rel in SCAFFOLD_FILES if not (tmp_path / "docs" / rel).is_file()]
    assert not missing, f"scaffold did not place: {missing}"
    # docs/ stays pure Markdown: Hugo's content/ never materialises on disk
    assert not (tmp_path / "docs" / "content").exists()


@pytest.mark.integration
def test_mount_rules_keep_markdown_in_place(tmp_path: Path):
    make_docs(tmp_path)
    run(tmp_path, "--action", "scaffold")
    config = (tmp_path / "docs" / "hugo.toml").read_text(encoding="utf-8")

    # the default static mount is re-declared, since an explicit mount replaces it
    assert 'source = "static"\n  target = "static"' in config
    # every directory holding Markdown gets a content mount ...
    for name in ("concepts", "tutorials", "tasks", "decisions", "notes", "archive", "reference"):
        assert f'target = "content/{name}"' in config, f"{name} not mounted as content"
    # ... plus a Markdown-excluding static mount so media beside prose is published
    assert 'target = "static/concepts"' in config
    assert '"*.md", "**/*.md"' in config
    # a media-only directory is static only, never content
    assert 'target = "static/assets"' in config
    assert 'target = "content/assets"' not in config
    # index.md keeps its name on disk but reaches Hugo as a branch bundle
    for name in ("tasks", "decisions", "notes"):
        assert f'source = "{name}/index.md"' in config
        assert f'target = "content/{name}/_index.md"' in config
    assert (tmp_path / "docs" / "tasks" / "index.md").is_file()
    assert not (tmp_path / "docs" / "tasks" / "_index.md").exists()
    # directories carrying an index.md exclude it from the recursive content mount
    assert '"index.md", "**/index.md"' in config


@pytest.mark.integration
def test_repeat_run_converges_nothing(tmp_path: Path):
    make_docs(tmp_path)
    run(tmp_path, "--action", "scaffold", "--site-title", "Probe")
    before = fingerprint(tmp_path / "docs")
    for _ in range(2):
        out = run(tmp_path, "--action", "scaffold", "--site-title", "Probe")
        assert {f["action"] for f in out["files"]} == {"unchanged"}
    assert fingerprint(tmp_path / "docs") == before, "repeat run must not write anything"
    check = run(tmp_path, "--action", "check")
    assert check["clean"] is True and check["dry_run"] is True


@pytest.mark.integration
def test_new_directory_is_detected_and_synced_without_losing_custom_config(tmp_path: Path):
    make_docs(tmp_path)
    run(tmp_path, "--action", "scaffold")
    config_path = tmp_path / "docs" / "hugo.toml"
    config_path.write_text(
        config_path.read_text(encoding="utf-8")
        + '\n[services.googleAnalytics]\n  ID = "keep-me"\n', encoding="utf-8")

    (tmp_path / "docs" / "newtype").mkdir()
    (tmp_path / "docs" / "newtype" / "page.md").write_text("# New\n", encoding="utf-8")

    drift = run(tmp_path, "--action", "check")
    assert drift["clean"] is False
    assert "newtype" in drift["content_mounts"]
    assert [f["action"] for f in drift["files"] if f["path"].endswith("hugo.toml")] == \
        ["mounts-synced"]

    run(tmp_path, "--action", "scaffold")
    synced = config_path.read_text(encoding="utf-8")
    assert 'target = "content/newtype"' in synced, "new directory must be mounted"
    assert 'ID = "keep-me"' in synced, "content outside the managed block must survive"


@pytest.mark.integration
def test_user_edited_files_are_kept_unless_forced(tmp_path: Path):
    make_docs(tmp_path)
    run(tmp_path, "--action", "scaffold")
    layout = tmp_path / "docs" / "layouts" / "_default" / "single.html"
    layout.write_text("<!-- mine -->\n", encoding="utf-8")

    out = run(tmp_path, "--action", "scaffold")
    assert "docs/layouts/_default/single.html" in out["kept_user_versions"]
    assert layout.read_text(encoding="utf-8") == "<!-- mine -->\n"

    forced = run(tmp_path, "--action", "scaffold", "--force")
    actions = {f["path"]: f["action"] for f in forced["files"]}
    assert actions["docs/layouts/_default/single.html"] == "overwritten"
    assert "mine" not in layout.read_text(encoding="utf-8")


@pytest.mark.integration
def test_config_without_managed_markers_is_never_touched(tmp_path: Path):
    make_docs(tmp_path)
    run(tmp_path, "--action", "scaffold")
    config_path = tmp_path / "docs" / "hugo.toml"
    config_path.write_text('title = "hand written"\n', encoding="utf-8")

    out = run(tmp_path, "--action", "scaffold")
    assert [f["action"] for f in out["files"] if f["path"].endswith("hugo.toml")] == ["unmanaged"]
    assert config_path.read_text(encoding="utf-8") == 'title = "hand written"\n'


@pytest.mark.integration
def test_reserved_component_name_is_reported(tmp_path: Path):
    make_docs(tmp_path)
    out = run(tmp_path, "--action", "check")
    assert [c["path"] for c in out["reserved_collisions"]] == ["docs/assets"]


@pytest.mark.integration
def test_scaffolded_space_still_validates_clean(tmp_path: Path):
    """Cross-engine invariant: the site layer introduces no docs-space violation."""
    make_docs(tmp_path)
    run(tmp_path, "--action", "scaffold")
    proc = subprocess.run(
        [sys.executable, str(DOCS_UTILS), "--action", "validate", "--root", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["violations"] == []


@pytest.mark.integration
def test_build_reports_guidance_when_hugo_is_absent(tmp_path: Path, monkeypatch):
    make_docs(tmp_path)
    run(tmp_path, "--action", "scaffold")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "--action", "build"],
        capture_output=True, text=True, env={"PATH": "", "SYSTEMROOT": ""},
    )
    out = json.loads(proc.stdout)
    assert out["built"] is False
    assert out["reason"] == "hugo-not-installed"
    assert out["clean"] is True, "an absent binary is not a convergence failure"


@pytest.mark.integration
@pytest.mark.skipif(shutil.which("hugo") is None, reason="hugo binary not installed")
def test_real_build_renders_links_and_media(tmp_path: Path):
    make_docs(tmp_path)
    run(tmp_path, "--action", "scaffold", "--site-title", "Probe")
    out = run(tmp_path, "--action", "build")
    assert out["built"] is True, out

    public = tmp_path / "docs" / "public"
    assert (public / "index.html").is_file()
    assert (public / "tasks" / "index.html").is_file(), "index.md must render as a section page"
    assert (public / "tasks" / "task-one" / "index.html").is_file(), \
        "siblings of an index.md must stay pages (branch bundle, not leaf bundle)"

    quickstart = (public / "tutorials" / "quickstart" / "index.html").read_text(encoding="utf-8")
    assert ".md" not in quickstart, "Markdown links must be rewritten to real page URLs"
    assert "concepts/overview/" in quickstart, "relative .md link must resolve to its page"
    assert "assets/flow.svg" in quickstart, "relative media path must resolve"

    assert (public / "assets" / "flow.svg").is_file(), "media-only directory must be published"
    assert (public / "concepts" / "diagram.svg").is_file(), "media beside prose must be published"
    assert not list(public.rglob("*.md")), "raw Markdown must never be copied into the output"
