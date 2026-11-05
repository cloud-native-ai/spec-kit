"""Contract test: instructions section propagation (Constitution XI v1.10.0).

Guards the mechanism fixed on 2026-08-14: template sections MUST propagate
into the live instructions file. Before the fix, sections added to
``templates/instructions-template.md`` after a project's initial bootstrap
(e.g. ``## Dogfooding Practice``, ``## Spec Kit Framework Map``) never
reached the live ``.specify/instructions.md`` — the generator only rendered
the template for brand-new files and otherwise did nothing but back up.

C-1 (real-tree guard): every top-level ``##`` section heading present in the
template MUST exist verbatim in the live instructions file.
C-2 (mechanism behavior): the generator injects missing template sections
into an existing live file additively — never modifying or removing
existing sections — and is idempotent.

Feature 082 adds the ``instructions-propagation.md`` clauses this file
carries. ``test_cN_*`` maps one-to-one onto that contract's C-N:

* **C-10** — the section exists in the template (heading verbatim + the
  runtime owner pointer in its body).
* **C-11** — the section is summary plus pointer, not a copy: none of the
  owner's own level-2 heading lines appears inside it.
* **C-14** — the mutation leg fires on the **template** side. A guard that
  only reads the live file stays green when the template loses its section,
  because the live copy is still there — so the C-14 assertion is made
  against the template and against the generator's actual reconcile input
  (the *rendered* template), and never reads the live file.

Isolation note: the render below reimplements the generator's three
substitutions rather than calling it, because the generator renders from
``.specify/templates/`` (an installed project's path) while this guard's
subject is the framework source at ``templates/``. The two are kept in step
by ``test_c14_rendered_template_matches_the_generator_substitution_set``,
which derives the ``{{PLACEHOLDER}}`` set from the generator itself — so a
fourth placeholder added there turns this file red instead of silently
making the rendered fixture unfaithful.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
LIVE = REPO_ROOT / ".specify" / "instructions.md"
GENERATOR = REPO_ROOT / "scripts" / "bash" / "generate-instructions.sh"
OWNER_SOURCE = REPO_ROOT / "shared" / "definitions" / "self-explanatory-definitions.md"
OWNER_MIRROR = REPO_ROOT / ".specify" / "shared" / "definitions" / "self-explanatory-definitions.md"

# [[STR-001]] — the heading both the template and the live file must carry.
SECTION_HEADING = "## Self-Explanatory Structure (不言自明)"
# [[STR-004]] — the runtime owner path the section body must point at. The
# framework-source path ([[STR-002]]) is deliberately NOT accepted here: the
# template is copied verbatim into client projects, which have no framework
# source tree (requirements A11).
RUNTIME_OWNER = ".specify/shared/definitions/self-explanatory-definitions.md"

# The generator's own substitution table (`render_template`). Read from the
# script, not restated: see the module docstring's isolation note.
_SUBSTITUTION_RE = re.compile(r'-e "s/\{\{([A-Za-z0-9_]+)\}\}/')


def _template_headings() -> list[str]:
    return re.findall(r"(?m)^## .+$", TEMPLATE.read_text(encoding="utf-8"))


@pytest.mark.contract
def test_c1_live_instructions_carry_all_template_sections():
    live = LIVE.read_text(encoding="utf-8")
    live_headings = set(re.findall(r"(?m)^## .+$", live))
    missing = [h for h in _template_headings() if h not in live_headings]
    assert not missing, (
        "live .specify/instructions.md is missing template-managed sections "
        f"(run scripts/bash/generate-instructions.sh to reconcile): {missing}"
    )


@pytest.mark.contract
def test_c2_generator_injects_missing_sections_additively(tmp_path: Path):
    (tmp_path / ".specify" / "templates").mkdir(parents=True)
    (tmp_path / ".specify" / "templates" / "instructions-template.md").write_text(
        "# Instructions\n\n"
        "## Alpha\n\nalpha body\n\n"
        "## Beta\n\nbeta body\n\n"
        "## Gamma\n\ngamma body\n",
        encoding="utf-8",
    )
    live = tmp_path / ".specify" / "instructions.md"
    live.write_text(
        "# Instructions\n\n## Alpha\n\nalpha body (customized)\n\n"
        "## Project Custom\n\nkept section\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    # refresh-tools.sh (invoked by the generator) resolves tools-utils.py from
    # the project root — mirror a real installed project's layout.
    specify_py = tmp_path / ".specify" / "scripts" / "python"
    specify_py.mkdir(parents=True, exist_ok=True)
    (specify_py / "tools-utils.py").symlink_to(
        REPO_ROOT / "scripts" / "python" / "tools-utils.py")

    result = subprocess.run(
        ["bash", str(GENERATOR)], cwd=tmp_path, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr

    text = live.read_text(encoding="utf-8")
    # missing template sections injected
    assert "## Beta" in text and "beta body" in text
    assert "## Gamma" in text and "gamma body" in text
    # existing sections untouched (customized content + project-specific section)
    assert "alpha body (customized)" in text
    assert "## Project Custom" in text and "kept section" in text
    # injected in template order: Beta before Gamma
    assert text.index("## Beta") < text.index("## Gamma")

    # idempotent: a second run changes nothing
    before = live.read_bytes()
    subprocess.run(["bash", str(GENERATOR)], cwd=tmp_path,
                   capture_output=True, text=True, check=True)
    assert live.read_bytes() == before


# --- C-10 / C-11: the section exists and is summary-plus-pointer ---


def _section_body(text: str, heading: str) -> str:
    """Body of the top-level section ``heading``, heading line excluded.

    Missing heading raises AssertionError carrying the heading name: at red-first
    time the failure must read as "artifact missing", not as a mis-written
    assertion.
    """
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        raise AssertionError(
            f"no {heading!r} section on the surface under test; this clause cannot be "
            "judged until the section lands"
        ) from None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start + 1:end])


@pytest.mark.contract
def test_c10_template_carries_the_section_and_its_runtime_pointer():
    text = TEMPLATE.read_text(encoding="utf-8")
    assert SECTION_HEADING in _template_headings(), (
        f"{TEMPLATE.relative_to(REPO_ROOT)} has no top-level {SECTION_HEADING!r} section"
    )
    body = _section_body(text, SECTION_HEADING)
    assert RUNTIME_OWNER in body, (
        f"the section body must carry the runtime owner pointer {RUNTIME_OWNER!r}; the template "
        "is copied into client projects, which cannot resolve the framework-source path"
    )


@pytest.mark.contract
def test_c11_section_is_summary_plus_pointer_not_a_copy():
    """C-11's decidable form, shared with C-20: copying the owner's body necessarily
    copies its headings, so their absence is the mechanical form of "points rather
    than restates". No prose wording is judged, and no phrase list is maintained.

    The sentence bound is C-21's (``test_self_explanatory_constitution.py``); this
    clause does not restate it here.
    """
    source = OWNER_SOURCE.read_text(encoding="utf-8")
    mirror = OWNER_MIRROR.read_text(encoding="utf-8")
    owner_headings = [ln for ln in source.splitlines() if ln.startswith("## ")]
    assert owner_headings, f"{OWNER_SOURCE.relative_to(REPO_ROOT)} carries no `##` heading"
    assert source == mirror, (
        "the owner and its runtime mirror must be byte-identical before this clause can be "
        "judged against both; run `python3 scripts/python/sync-mirrors.py --write`"
    )

    body = _section_body(TEMPLATE.read_text(encoding="utf-8"), SECTION_HEADING)
    copied = [h for h in owner_headings if h in body]
    assert not copied, (
        f"the {SECTION_HEADING!r} section reproduces the owner's own heading(s) {copied}; the "
        "section carries a summary and a pointer, never the owner's body"
    )
    assert RUNTIME_OWNER in body, (
        "a section with no pointer at all is not summary-plus-pointer; it is a summary with "
        "nothing to reach"
    )


# --- C-14: the mutation leg fires on the template side ---


def _generator_substitutions() -> set[str]:
    """The `{{NAME}}` placeholders the generator's `render_template` substitutes."""
    found = set(_SUBSTITUTION_RE.findall(GENERATOR.read_text(encoding="utf-8")))
    assert found, (
        "generate-instructions.sh no longer declares its substitutions in the `sed -e "
        "\"s/{{NAME}}/...\"` form this guard reads; the rendered-template fixture would be "
        "measuring a rendering the generator does not perform"
    )
    return found


def _render(template_text: str) -> str:
    """Render the template the way the generator does, for the source tree path.

    The values are irrelevant to this guard — it asserts the *heading* survives
    rendering — but they must be present, or `{{...}}` tokens would leak into the
    rendered text and make the fixture unfaithful to the generator's input.
    """
    subs = _generator_substitutions()
    return re.sub(
        r"\{\{([A-Za-z0-9_]+)\}\}",
        lambda m: f"<<{m.group(1)}>>" if m.group(1) in subs else m.group(0),
        template_text,
    )


@pytest.mark.contract
def test_c14_rendered_template_matches_the_generator_substitution_set():
    """Anti-drift companion to `_render`: every `{{PLACEHOLDER}}` the template uses
    must be one the generator substitutes. A new placeholder on either side turns
    this red instead of leaving the rendered fixture silently unfaithful."""
    template_placeholders = set(
        re.findall(r"\{\{([A-Za-z0-9_]+)\}\}", TEMPLATE.read_text(encoding="utf-8"))
    )
    unhandled = sorted(template_placeholders - _generator_substitutions())
    assert not unhandled, (
        f"the template uses placeholder(s) {unhandled} that generate-instructions.sh does not "
        "substitute; the rendered fixture in this file and the generator's real input have "
        "diverged"
    )


@pytest.mark.contract
def test_c14_template_side_presence_survives_rendering(tmp_path: Path):
    """C-14: assert on the TEMPLATE and on the generator's reconcile input — never on
    the live file. A live-file assertion stays green after a template-side deletion,
    because the live copy is unchanged, which is exactly the blind spot this clause
    exists to close.
    """
    text = TEMPLATE.read_text(encoding="utf-8")
    assert SECTION_HEADING in text, (
        f"C-14: the template lost its {SECTION_HEADING!r} heading; deleting it from the "
        "template must fail this clause even while the live file still carries the section"
    )

    rendered = _render(text)
    assert SECTION_HEADING in rendered, (
        "C-14: the heading does not survive the generator's rendering step, so the reconcile "
        "input would lack it even though the template carries it"
    )

    # The mutation leg, on a copy only: remove the section from the rendered text and
    # confirm the very assertion above goes red — a guard that cannot fail is no guard.
    lines = rendered.splitlines()
    start = lines.index(SECTION_HEADING)
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    mutated = "\n".join(lines[:start] + lines[end:])
    assert SECTION_HEADING not in mutated, (
        "the mutation removed nothing — the section boundaries were mis-detected, so the "
        "mutation leg proves nothing about the assertion above"
    )

    # Anti-vacuity sentinel: the mutation ran on a copy, so the real template still carries it.
    assert SECTION_HEADING in TEMPLATE.read_text(encoding="utf-8"), (
        "the mutation leg wrote to the real template instead of a temporary copy"
    )
