"""Contract test: the optional mount-mode site scaffolder of the create-pages skill.

Spec 033 revision 2026-08-20 decoupled presentation from structure: a documentation
space is complete and valid *without* a site, so nothing here may require one. What
remains binding is narrower — **if** the mount-mode scaffolder ships, it must behave
deterministically (stdlib-only, four actions, mount-not-copy render hooks), and the
structure skill (``create-docs``) must not grow the capability back.

Withdrawn with that revision: C-13's "baseline MUST contain a Hugo layer", plus
C-14…C-17 as location mandates on ``create-docs``.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "create-pages"
MIRROR_DIR = REPO_ROOT / ".specify" / "skills" / "create-pages"
SKILL_MD = SKILL_DIR / "SKILL.md"
SCRIPT = SKILL_DIR / "scripts" / "scaffold-hugo.py"
CI_SCRIPT = SKILL_DIR / "scripts" / "scaffold-ci.sh"
CI_TEMPLATES = SKILL_DIR / "scripts" / "ci-templates"
ASSETS = SKILL_DIR / "assets" / "hugo"
REFERENCE = SKILL_DIR / "references" / "hugo-site.md"

CREATE_DOCS_MD = REPO_ROOT / "skills" / "create-docs" / "SKILL.md"

EXPECTED_ASSETS = (
    "hugo.toml.tmpl",
    "dotgitignore",
    "layouts/index.html",
    "layouts/partials/title.html",
    "layouts/_default/baseof.html",
    "layouts/_default/list.html",
    "layouts/_default/single.html",
    "layouts/_default/_markup/render-link.html",
    "layouts/_default/_markup/render-image.html",
    "static/css/site.css",
)

ACTIONS = ("scaffold", "check", "mounts", "build")
STDLIB_ALLOWED = {
    "__future__", "argparse", "json", "shutil", "subprocess", "sys", "pathlib",
}

# The capability is optional: when the scaffolder is not installed, its behavioural
# guarantees have nothing to bind and the checks below are skipped rather than failed.
requires_mount_mode = pytest.mark.skipif(
    not SCRIPT.is_file(),
    reason="optional capability: create-pages mount-mode scaffolder is not installed",
)


@pytest.mark.contract
def test_site_layer_is_optional_for_the_structure_skill():
    """create-docs must hand site work off, never carry a scaffolder itself."""
    text = CREATE_DOCS_MD.read_text(encoding="utf-8")
    assert "scaffold-hugo.py" not in text, \
        "create-docs must not invoke the site scaffolder; site work belongs to create-pages"
    assert "create-pages" in text, "create-docs must name create-pages as the site owner"
    assert not (REPO_ROOT / "skills" / "create-docs" / "assets").exists(), \
        "site assets must not live under create-docs"


@pytest.mark.contract
def test_reconcile_loop_still_skips_site_tooling_directories():
    """The one protective requirement kept from C-13: those dirs are not documentation."""
    text = CREATE_DOCS_MD.read_text(encoding="utf-8")
    for owned in ("layouts", "static", "public", "resources", "themes", "archetypes"):
        assert owned in text, f"site-tooling directory {owned} must stay declared as skippable"
    assert "not documentation" in text, \
        "site-tooling dirs must be excluded from content triage and archiving"


@pytest.mark.contract
@requires_mount_mode
def test_skill_declares_the_three_stage_pipeline():
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "Hugo project root" in text, "stage 2 must name the docs dir as the Hugo project root"
    assert "references/hugo-site.md" in text, "skill must link the on-demand reference"
    assert "scaffold-hugo.py" in text, "stage 2 must dispatch to the render scaffolder"
    assert "scaffold-ci.sh" in text, "stage 3 must dispatch to the CI adapter"
    for stage in ("本地文档库", "Hugo 渲染", "Pages 服务"):
        assert stage in text, f"pipeline stage missing from the skill: {stage}"
    for target in ("`local`", "`aoneci`", "`github`"):
        assert target in text, f"stage 3 target missing: {target}"
    frontmatter = text.split("---", 2)[1]
    assert "Hugo" in frontmatter, "description must advertise the Hugo capability"
    assert "静态网站" in frontmatter, "description must carry site trigger keywords"


@pytest.mark.contract
@requires_mount_mode
def test_single_renderer_and_docs_scoped_output():
    """One renderer, output inside the docs directory — no staging copy, no root dist/."""
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "one** renderer" in text or "one renderer" in text, \
        "skill must state that exactly one renderer exists"
    assert "build-docs.sh" not in text, "the retired staging build script must not return"
    assert not (SKILL_DIR / "scripts" / "scaffold.sh").exists(), \
        "scaffold.sh was superseded by scaffold-ci.sh"
    for template in sorted(CI_TEMPLATES.rglob("*.tpl")):
        body = template.read_text(encoding="utf-8")
        assert "public" in body, f"{template.name}: pipeline must publish the docs public dir"
        assert "deploy-dir: dist" not in body, \
            f"{template.name}: repository-root dist/ output is not allowed"


@pytest.mark.contract
@requires_mount_mode
def test_titles_render_through_the_fallback_partial():
    """Documents here carry no front matter, so .Title/.LinkTitle alone render empty."""
    partial = (ASSETS / "layouts/partials/title.html").read_text(encoding="utf-8")
    assert "findRE" in partial and "h1" in partial, \
        "title partial must fall back to the first <h1> of the content"
    for layout in ("layouts/_default/baseof.html", "layouts/_default/list.html",
                   "layouts/index.html"):
        body = (ASSETS / layout).read_text(encoding="utf-8")
        assert 'partial "title.html"' in body, f"{layout} must render titles via the partial"
    assert ".LinkTitle" not in (ASSETS / "layouts/index.html").read_text(encoding="utf-8"), \
        "bare .LinkTitle produces blank link text for front-matter-less pages"


@pytest.mark.contract
def test_ci_adapter_registry_rejects_gitlab():
    """aoneci is the internal platform; open-source gitlab is not a target here."""
    assert CI_SCRIPT.is_file(), "skills/create-pages/scripts/scaffold-ci.sh missing"
    registry = (CI_TEMPLATES / "README.md").read_text(encoding="utf-8")
    assert "| aoneci |" in registry, "aoneci must stay registered as implemented"
    assert not (CI_TEMPLATES / "gitlab").exists(), \
        "gitlab is not a platform in this registry (aoneci is the internal one)"
    proc = subprocess.run(["bash", str(CI_SCRIPT), "--site-name", "x", "--platform", "gitlab"],
                          capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == 2, "an unknown platform must fail fast"
    assert "unknown --platform" in proc.stderr


@pytest.mark.contract
@requires_mount_mode
def test_scaffold_script_and_assets_present():
    assert REFERENCE.is_file(), "skills/create-pages/references/hugo-site.md missing"
    missing = [rel for rel in EXPECTED_ASSETS if not (ASSETS / rel).is_file()]
    assert not missing, f"missing Hugo asset templates: {missing}"


@pytest.mark.contract
@requires_mount_mode
def test_script_is_stdlib_only_with_four_actions():
    source = SCRIPT.read_text(encoding="utf-8")
    imported = set(re.findall(r"^\s*(?:import|from)\s+([\w.]+)", source, re.M))
    assert {name.split(".")[0] for name in imported} <= STDLIB_ALLOWED, \
        f"scaffolder must stay stdlib-only: {imported}"
    for action in ACTIONS:
        assert f'"{action}"' in source, f"action {action} missing from the CLI"
    proc = subprocess.run([sys.executable, str(SCRIPT), "--help"],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    for action in ACTIONS:
        assert action in proc.stdout, f"--help must advertise {action}"


@pytest.mark.contract
@requires_mount_mode
def test_config_template_semantics():
    template = (ASSETS / "hugo.toml.tmpl").read_text(encoding="utf-8")
    for placeholder in ("{{SITE_TITLE}}", "{{SITE_DESCRIPTION}}", "{{MOUNTS}}"):
        assert placeholder in template, f"template placeholder {placeholder} missing"
    assert "unsafe = true" in template, "raw HTML in documentation must survive rendering"
    assert "relativeURLs = true" in template, "output must stay relocatable"
    # Regression pin: the map form of uglyURLs is silently ignored by Hugo, so link
    # shapes are handled by the render hooks instead.
    assert "[uglyURLs]" not in template, "uglyURLs map is not honored by Hugo; do not reintroduce"


@pytest.mark.contract
@requires_mount_mode
def test_render_hooks_resolve_semantically():
    link_hook = (ASSETS / "layouts/_default/_markup/render-link.html").read_text(encoding="utf-8")
    assert "GetPage" in link_hook, "link hook must resolve through Hugo's page graph"
    assert ".md" in link_hook, "link hook must recognise Markdown destinations"
    image_hook = (ASSETS / "layouts/_default/_markup/render-image.html").read_text(encoding="utf-8")
    assert "path.Join" in image_hook and "relURL" in image_hook, \
        "image hook must resolve relative media against the content file's directory"


@pytest.mark.contract
def test_mirror_parity_for_the_whole_skill():
    assert MIRROR_DIR.is_dir(), ".specify/skills/create-pages mirror missing"
    drift = []
    for source in sorted(SKILL_DIR.rglob("*")):
        if not source.is_file():
            continue
        mirror = MIRROR_DIR / source.relative_to(SKILL_DIR)
        if not mirror.is_file() or mirror.read_bytes() != source.read_bytes():
            drift.append(source.relative_to(SKILL_DIR).as_posix())
    assert not drift, f"skill mirror drift: {drift}"


@pytest.mark.contract
@requires_mount_mode
def test_stage_separation_renderer_never_writes_ci():
    """Stage 2 renders; only stage 3's adapter may write a pipeline file."""
    assert ".github" not in SCRIPT.read_text(encoding="utf-8"), \
        "the render scaffolder must never write CI files"
    reference = REFERENCE.read_text(encoding="utf-8")
    assert "working-directory: docs" in reference, "CI must run Hugo from the docs/ root"
    assert "docs/public" in reference, "CI guidance must name the artifact directory"
    assert "verify each action version" in reference, \
        "the github snippet is unverified guidance and must say so"
    assert (CI_TEMPLATES / "aoneci" / "deploy-pages.yaml.tpl").is_file(), \
        "the implemented platform must keep its template"
    assert not (CI_TEMPLATES / "github" / "deploy-pages.yaml.tpl").exists(), \
        "github is a stub: writing a template requires verifying action versions first"
