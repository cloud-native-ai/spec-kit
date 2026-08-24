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

import ast
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
IMAGE_REGISTRY = CI_TEMPLATES / "hugo-image.txt"
ASSETS = SKILL_DIR / "assets" / "hugo"
BOOK_ASSETS = SKILL_DIR / "assets" / "book"
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

# Book mode ships only what the theme cannot do by itself: the label override, the
# child-index shortcode and the mounted section-index stub.
EXPECTED_BOOK_ASSETS = (
    "hugo.toml.tmpl",
    "dotgitignore",
    "layouts/_partials/docs/title.html",
    "layouts/_shortcodes/speckit-children.html",
    "dotspeckit/nav/section-index.md",
)

ACTIONS = ("scaffold", "check", "mounts", "build", "theme")
STDLIB_ALLOWED = {
    "__future__", "argparse", "json", "os", "re", "shutil", "subprocess", "sys",
    "pathlib",
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
def test_script_is_stdlib_only_with_declared_actions():
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
@requires_mount_mode
def test_hugo_book_is_the_preferred_theme_with_a_fallback():
    """Book mode is the recommendation, built-in layouts remain the degraded path."""
    source = SCRIPT.read_text(encoding="utf-8")
    assert "alex-shpak/hugo-book" in source, "the preferred theme must be named in the script"
    ref = re.search(r'THEME_REF = "([^"]+)"', source)
    assert ref, "the theme ref must be a named constant"
    assert ref.group(1) not in ("main", "master", "HEAD"), \
        "pin a release tag: a moving branch makes the vendored snapshot irreproducible"
    for mode in ("auto", "book", "builtin"):
        assert f'"{mode}"' in source, f"--theme mode {mode} missing"
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "Hugo Book" in text and "alex-shpak/hugo-book" in text, \
        "the skill must name the preferred theme and its upstream"
    assert "builtin" in text, "the skill must document the fallback mode"


@pytest.mark.contract
@requires_mount_mode
def test_theme_assets_do_not_shadow_the_theme():
    """Book mode overrides two templates on purpose; a stray baseof/list/single or a
    render hook of our own would silently replace the theme's page shell or its
    portable-link resolution."""
    missing = [rel for rel in EXPECTED_BOOK_ASSETS if not (BOOK_ASSETS / rel).is_file()]
    assert not missing, f"missing Book asset templates: {missing}"
    shipped = {path.relative_to(BOOK_ASSETS).as_posix()
               for path in BOOK_ASSETS.rglob("*") if path.is_file()}
    assert shipped == set(EXPECTED_BOOK_ASSETS), \
        f"unexpected Book assets: {sorted(shipped - set(EXPECTED_BOOK_ASSETS))}"
    config = (BOOK_ASSETS / "hugo.toml.tmpl").read_text(encoding="utf-8")
    assert 'theme = "book"' in config, "the Book config must select the theme"
    assert 'BookSection = "*"' in config, \
        "content is mounted at content/<type>, so the menu must span all sections"
    assert "BookPortableLinks" in config, \
        "repo-native relative .md links need the theme's portable-link hooks"
    for placeholder in ("{{SITE_TITLE}}", "{{SITE_DESCRIPTION}}", "{{MOUNTS}}"):
        assert placeholder in config, f"template placeholder {placeholder} missing"


@pytest.mark.contract
@requires_mount_mode
def test_book_titles_survive_the_heading_anchor():
    """The theme's heading hook appends an anchor, so a rendered <h1> plainifies to
    'Title#'. The label override must read the raw Markdown instead."""
    partial = (BOOK_ASSETS / "layouts/_partials/docs/title.html").read_text(encoding="utf-8")
    assert ".RawContent" in partial, "read the H1 from the raw Markdown, not .Content"
    assert "findRE" in partial, "the H1 fallback must still be a regex over the source"
    assert "return" in partial, "the theme calls docs/title as a returning partial"


@pytest.mark.contract
@requires_mount_mode
def test_navigation_completion_is_config_and_mount_only():
    """Nav completion must not write documentation: order/labels/collapse come from a
    cascade, and missing section indexes from one mounted stub."""
    source = SCRIPT.read_text(encoding="utf-8")
    assert "[[cascade]]" in source, "navigation order must be declared as a cascade"
    assert "[cascade.target]" in source, \
        "cascade._target was deprecated in Hugo v0.156.0; emit cascade.target"
    assert "bookCollapseSection" in source, "crowded sections must collapse in the sidebar"
    assert "_index.md" in source and "NAV_STUB" in source, \
        "directories without an index.md must get a mounted section index"
    stub = (BOOK_ASSETS / "dotspeckit/nav/section-index.md").read_text(encoding="utf-8")
    assert not stub.lstrip().startswith("{"), \
        "a content file starting with '{' is parsed as JSON front matter and fails the build"
    assert "speckit-children" in stub, "the stub must render the child index shortcode"


@pytest.mark.contract
@requires_mount_mode
def test_vendored_theme_carries_no_third_party_markdown():
    """docs-utils validate audits every .md under the docs directory, so the vendored
    theme is reduced to its runtime parts."""
    source = SCRIPT.read_text(encoding="utf-8")
    keep = re.search(r"THEME_KEEP = \(([^)]*)\)", source, re.S)
    assert keep, "the vendoring whitelist must be a named constant"
    kept = re.findall(r'"([^"]+)"', keep.group(1))
    assert "layouts" in kept and "LICENSE" in kept, \
        "the theme needs its layouts, and its licence must travel with it"
    assert not [name for name in kept if name.endswith(".md")], \
        "no third-party Markdown may be kept inside the docs space"
    assert "exampleSite" not in kept and "archetypes" not in kept


@pytest.mark.contract
@requires_mount_mode
def test_builtin_layouts_stay_compatible_with_older_hugo():
    """Regression: .Site.Language.Locale only exists from Hugo v0.158, and the
    built-in mode is exactly the path for environments that cannot run the theme."""
    for layout in sorted(ASSETS.rglob("*.html")):
        body = layout.read_text(encoding="utf-8")
        assert ".Site.Language.Locale" not in body, \
            f"{layout.name}: Locale is unavailable before Hugo 0.158; use .Language.Lang"


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
    """Stage 2 renders; only stage 3's adapter may write a pipeline file. Stage 2 does
    *read* the rendered pipeline — that is how a local build picks up the same image CI
    uses — so the pin is structural: the CI paths may only be touched by the reader."""
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    readers = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        names = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
        if "CI_FILES" in names:
            readers.add(node.name)
    assert readers == {"ci_image"}, \
        f"CI pipeline paths may only be read (by ci_image), not used in {sorted(readers)}"
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in ("write_text", "write_bytes"):
            target = ast.unparse(node.value)
            assert "ci" not in target.lower() or "CI_FILES" not in target, \
                f"the render scaffolder must never write a CI file: {ast.unparse(node)}"
    reference = REFERENCE.read_text(encoding="utf-8")
    assert "working-directory: docs" in reference, "CI must run Hugo from the docs/ root"
    assert "docs/public" in reference, "CI guidance must name the artifact directory"
    assert "verify each action version" in reference, \
        "the github snippet is unverified guidance and must say so"
    assert (CI_TEMPLATES / "aoneci" / "deploy-pages.yaml.tpl").is_file(), \
        "the implemented platform must keep its template"
    assert not (CI_TEMPLATES / "github" / "deploy-pages.yaml.tpl").exists(), \
        "github is a stub: writing a template requires verifying action versions first"


@pytest.mark.contract
@requires_mount_mode
def test_local_builds_default_to_the_ci_image():
    """A workstation Hugo is usually older than the image (and often older than the
    theme's floor), so 'works locally' only means something when local == CI."""
    source = SCRIPT.read_text(encoding="utf-8")
    assert '"auto", "docker", "local"' in source, "runner modes must be declared"
    assert 'default="auto"' in source, "the default runner must prefer the CI image"
    assert "docker" in source and "-v" in source, "the docker runner must mount the workspace"
    # one image for both stages, declared in one place
    assert IMAGE_REGISTRY.is_file(), "ci-templates/hugo-image.txt (shared default) missing"
    declared = [line.strip() for line in IMAGE_REGISTRY.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.strip().startswith("#")]
    assert len(declared) == 1, "the image registry must hold exactly one image reference"
    assert "hugo-image.txt" in CI_SCRIPT.read_text(encoding="utf-8"), \
        "stage 3 must take its default image from the same file as stage 2"
    assert "IMAGE_FILE" in source, "stage 2 must resolve the shared image file"
    template = (CI_TEMPLATES / "aoneci" / "deploy-pages.yaml.tpl").read_text(encoding="utf-8")
    assert "__IMAGE__" in template, "the pipeline image must stay a rendered placeholder"
