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


BOOK_FILES = (
    "hugo.toml",
    ".gitignore",
    ".speckit/nav/section-index.md",
    "layouts/_partials/docs/title.html",
    "layouts/_shortcodes/speckit-children.html",
)


def fake_theme(root: Path, min_version: str = "0.158.0") -> None:
    """A theme present on disk, without touching the network: only the marker file and
    its declared Hugo minimum matter to the scaffolder."""
    theme = root / "docs" / "themes" / "book"
    (theme / "layouts").mkdir(parents=True)
    (theme / "theme.toml").write_text(
        f'name = "Book"\nmin_version = "{min_version}"\n', encoding="utf-8")


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


# --------------------------------------------------------------------------------------
# Book mode: the preferred theme, plus the navigation it needs to be complete.
# --------------------------------------------------------------------------------------


@pytest.mark.integration
def test_auto_mode_falls_back_to_builtin_without_the_theme(tmp_path: Path):
    make_docs(tmp_path)
    out = run(tmp_path, "--action", "scaffold")
    assert out["theme"]["mode"] == "builtin" and out["theme"]["present"] is False
    assert out["nav"]["applied"] is False, "nav completion is a Book-mode capability"
    assert (tmp_path / "docs" / "layouts" / "_default" / "baseof.html").is_file()
    assert not (tmp_path / "docs" / ".speckit").exists(), \
        "the nav stub belongs to Book mode only"


@pytest.mark.integration
def test_explicit_book_request_without_the_theme_refuses_to_write(tmp_path: Path):
    make_docs(tmp_path)
    before = fingerprint(tmp_path / "docs")
    out = run(tmp_path, "--action", "scaffold", "--theme", "book")
    assert out["clean"] is False and "error" in out
    assert "theme" in out["guidance"], "the report must name the install path"
    assert fingerprint(tmp_path / "docs") == before, "a refused run must write nothing"


@pytest.mark.integration
def test_theme_status_never_touches_the_network(tmp_path: Path):
    make_docs(tmp_path)
    out = run(tmp_path, "--action", "theme")
    assert out["fetched"] is False and out["present"] is False and out["clean"] is True
    assert "--fetch" in out["guidance"]
    fake_theme(tmp_path)
    out = run(tmp_path, "--action", "theme")
    assert out["present"] is True and out["min_hugo"] == "0.158.0"
    assert out["fetched"] is False, "status alone must not install anything"


@pytest.mark.integration
def test_book_mode_completes_the_navigation(tmp_path: Path):
    make_docs(tmp_path)
    fake_theme(tmp_path)
    out = run(tmp_path, "--action", "scaffold", "--site-title", "Probe")
    assert out["theme"]["mode"] == "book" and out["nav"]["applied"] is True
    missing = [rel for rel in BOOK_FILES if not (tmp_path / "docs" / rel).is_file()]
    assert not missing, f"Book scaffold did not place: {missing}"

    config = (tmp_path / "docs" / "hugo.toml").read_text(encoding="utf-8")
    assert 'theme = "book"' in config
    # a nested directory without an index.md is not a Hugo section at all, so the
    # sidebar would lose the grouping: the shared stub restores it
    assert "reference/commands" in out["nav"]["generated_indexes"]
    assert 'target = "content/reference/commands/_index.md"' in config
    assert f'source = "{".speckit/nav/section-index.md"}"' in config
    # the docs root has no index.md either, so the home page gets one too
    assert 'target = "content/_index.md"' in config
    # reading order, not alphabetical: concepts before tutorials before archive
    order = out["nav"]["order"]
    assert order["concepts"] < order["tutorials"] < order["archive"]
    assert '    path = "/concepts"' in config and "[cascade.target]" in config
    # generated sections get a machine label; curated ones keep their H1
    assert 'title = "Commands"' in config
    assert 'title = "Tasks"' not in config, \
        "tasks/index.md exists: its H1 is the label, not a generated title"
    # documents are never touched
    assert not (tmp_path / "docs" / "reference" / "commands" / "index.md").exists()
    assert not (tmp_path / "docs" / "reference" / "commands" / "_index.md").exists()


@pytest.mark.integration
def test_collapse_threshold_marks_only_crowded_sections(tmp_path: Path):
    make_docs(tmp_path)
    fake_theme(tmp_path)
    for index in range(6):
        (tmp_path / "docs" / "reference" / "commands" / f"cmd-{index}.md").write_text(
            f"# Command {index}\n", encoding="utf-8")
    out = run(tmp_path, "--action", "scaffold", "--collapse-threshold", "6")
    assert "reference/commands" in out["nav"]["collapsed"]
    assert "tutorials" not in out["nav"]["collapsed"], "a two-page section stays expanded"
    config = (tmp_path / "docs" / "hugo.toml").read_text(encoding="utf-8")
    assert "bookCollapseSection = true" in config


@pytest.mark.integration
def test_mode_switch_is_atomic_and_needs_force(tmp_path: Path):
    """Half a switch (theme config, no layouts / builtin config, no layouts) is an
    unbuildable site, so a blocked switch must write nothing at all."""
    make_docs(tmp_path)
    run(tmp_path, "--action", "scaffold", "--site-title", "Probe")
    fake_theme(tmp_path)
    before = fingerprint(tmp_path / "docs")

    blocked = run(tmp_path, "--action", "scaffold", "--site-title", "Probe")
    assert blocked["clean"] is False
    assert [f["action"] for f in blocked["files"] if f["path"].endswith("hugo.toml")] == \
        ["mode-mismatch"]
    assert "--force" in blocked["guidance"]
    assert fingerprint(tmp_path / "docs") == before, "a blocked switch must write nothing"

    switched = run(tmp_path, "--action", "scaffold", "--site-title", "Probe", "--force")
    actions = {f["path"]: f["action"] for f in switched["files"]}
    assert actions["docs/hugo.toml"] == "rewritten"
    assert actions["docs/layouts/_default/baseof.html"] == "removed", \
        "a leftover baseof.html would replace the theme's whole page shell"
    assert not (tmp_path / "docs" / "layouts" / "_default").exists()
    assert not (tmp_path / "docs" / "static" / "css").exists()
    assert switched["clean"] is True
    assert run(tmp_path, "--action", "scaffold", "--site-title", "Probe")["clean"] is True


@pytest.mark.integration
def test_locally_edited_layout_survives_a_mode_switch(tmp_path: Path):
    make_docs(tmp_path)
    run(tmp_path, "--action", "scaffold")
    edited = tmp_path / "docs" / "layouts" / "_default" / "single.html"
    edited.write_text("<!-- mine -->\n", encoding="utf-8")
    fake_theme(tmp_path)

    out = run(tmp_path, "--action", "scaffold", "--force")
    assert out["stale_edited"] == ["docs/layouts/_default/single.html"]
    assert edited.read_text(encoding="utf-8") == "<!-- mine -->\n", \
        "an edited file is reported, never silently deleted"
    assert out["clean"] is False, "the leftover needs a human decision"


@pytest.mark.integration
def test_book_mode_space_still_validates_clean(tmp_path: Path):
    """Cross-engine invariant, Book mode: the mounted stub and the vendored theme must
    not produce documentation-space violations."""
    make_docs(tmp_path)
    fake_theme(tmp_path)
    run(tmp_path, "--action", "scaffold")
    proc = subprocess.run(
        [sys.executable, str(DOCS_UTILS), "--action", "validate", "--root", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["violations"] == []


@pytest.mark.integration
@pytest.mark.skipif(shutil.which("hugo") is None, reason="hugo binary not installed")
def test_build_refuses_when_hugo_is_older_than_the_theme(tmp_path: Path):
    make_docs(tmp_path)
    fake_theme(tmp_path, min_version="99.0.0")   # no Hugo will ever satisfy this
    run(tmp_path, "--action", "scaffold")
    out = run(tmp_path, "--action", "build")
    assert out["built"] is False and out["reason"] == "hugo-older-than-theme"
    assert out["clean"] is True, "an old local binary is an environment gap, not drift"
    assert "--theme builtin" in out["guidance"]
