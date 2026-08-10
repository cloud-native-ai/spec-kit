"""Contract test: Hugo presentation layer of the create-docs skill (spec 033).

Driven by ``.specify/specs/033-docs-command/contracts/docs-command-template.md``
(C-13…C-17): the documentation space must be publishable as a static site, the
scaffold must be a deterministic script rather than hand-written HTML, and the
Markdown tree must be mounted rather than copied.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "create-docs"
MIRROR_DIR = REPO_ROOT / ".specify" / "skills" / "create-docs"
SKILL_MD = SKILL_DIR / "SKILL.md"
SCRIPT = SKILL_DIR / "scripts" / "scaffold-hugo.py"
ASSETS = SKILL_DIR / "assets" / "hugo"
REFERENCE = SKILL_DIR / "references" / "hugo-site.md"

EXPECTED_ASSETS = (
    "hugo.toml.tmpl",
    "dotgitignore",
    "layouts/index.html",
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


@pytest.mark.contract
def test_c13_skill_declares_hugo_layer_in_desired_state():
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "Hugo project root" in text, "baseline must name docs/ as the Hugo project root"
    assert "Hugo Presentation Layer" in text, "skill must carry the site dispatch section"
    assert "references/hugo-site.md" in text, "skill must link the on-demand reference"
    for owned in ("layouts", "static", "public", "resources", "themes", "archetypes"):
        assert owned in text, f"scaffold-owned directory {owned} must be declared"
    assert "not documentation" in text, "scaffold-owned dirs must be excluded from content triage"
    frontmatter = text.split("---", 2)[1]
    assert "Hugo" in frontmatter, "description must advertise the Hugo capability"
    assert "静态网站" in frontmatter, "description must carry site trigger keywords"


@pytest.mark.contract
def test_c14_scaffold_script_and_assets_present():
    assert SCRIPT.is_file(), "skills/create-docs/scripts/scaffold-hugo.py missing"
    assert REFERENCE.is_file(), "skills/create-docs/references/hugo-site.md missing"
    missing = [rel for rel in EXPECTED_ASSETS if not (ASSETS / rel).is_file()]
    assert not missing, f"missing Hugo asset templates: {missing}"


@pytest.mark.contract
def test_c14_script_is_stdlib_only_with_four_actions():
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
def test_c15_config_template_semantics():
    template = (ASSETS / "hugo.toml.tmpl").read_text(encoding="utf-8")
    for placeholder in ("{{SITE_TITLE}}", "{{SITE_DESCRIPTION}}", "{{MOUNTS}}"):
        assert placeholder in template, f"template placeholder {placeholder} missing"
    assert "unsafe = true" in template, "raw HTML in documentation must survive rendering"
    assert "relativeURLs = true" in template, "output must stay relocatable"
    # Regression pin: the map form of uglyURLs is silently ignored by Hugo, so link
    # shapes are handled by the render hooks instead.
    assert "[uglyURLs]" not in template, "uglyURLs map is not honored by Hugo; do not reintroduce"


@pytest.mark.contract
def test_c15_render_hooks_resolve_semantically():
    link_hook = (ASSETS / "layouts/_default/_markup/render-link.html").read_text(encoding="utf-8")
    assert "GetPage" in link_hook, "link hook must resolve through Hugo's page graph"
    assert ".md" in link_hook, "link hook must recognise Markdown destinations"
    image_hook = (ASSETS / "layouts/_default/_markup/render-image.html").read_text(encoding="utf-8")
    assert "path.Join" in image_hook and "relURL" in image_hook, \
        "image hook must resolve relative media against the content file's directory"


@pytest.mark.contract
def test_c16_mirror_parity_for_the_whole_skill():
    assert MIRROR_DIR.is_dir(), ".specify/skills/create-docs mirror missing"
    drift = []
    for source in sorted(SKILL_DIR.rglob("*")):
        if not source.is_file():
            continue
        mirror = MIRROR_DIR / source.relative_to(SKILL_DIR)
        if not mirror.is_file() or mirror.read_bytes() != source.read_bytes():
            drift.append(source.relative_to(SKILL_DIR).as_posix())
    assert not drift, f"skill mirror drift: {drift}"


@pytest.mark.contract
def test_c17_ci_guidance_is_documentation_only():
    reference = REFERENCE.read_text(encoding="utf-8")
    assert "No workflow file is generated" in reference, \
        "CI integration is delivered as guidance, not as a generated workflow"
    assert "working-directory: docs" in reference, "CI must run Hugo from the docs/ root"
    assert "docs/public" in reference, "CI guidance must name the artifact directory"
    assert ".github" not in SCRIPT.read_text(encoding="utf-8"), \
        "the scaffolder must never write CI files"
