"""Contract tests for the directory-governance discipline (Constitution Principle XVII).

Guards the house pattern:
  * ``shared/guidelines/directory-governance.md`` — owner (+ runtime mirror)
  * ``templates/constitution-template.md`` / ``.specify/memory/constitution.md`` — principle
  * ``skills/internal/manage-constitution/SKILL.md`` — generator MUST-include entry
  * ``templates/instructions-template.md`` (+ mirror + live) — ambient pointer

Wording safety: the owner document lives inside the confirmation-gate scanner's surface, whose
integer headroom is zero, so any blocking-confirmation literal would move the pinned total.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
OWNER = ROOT / "shared" / "guidelines" / "directory-governance.md"
OWNER_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / "directory-governance.md"
TEMPLATE = ROOT / "templates" / "constitution-template.md"
LIVE = ROOT / ".specify" / "memory" / "constitution.md"
SKILL = ROOT / "skills" / "internal" / "manage-constitution" / "SKILL.md"
INSTR_TEMPLATE = ROOT / "templates" / "instructions-template.md"
INSTR_MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"
INSTR_LIVE = ROOT / ".specify" / "instructions.md"
TEMP_DOC = ROOT / "shared" / "guidelines" / "temp-directory-discipline.md"
LOOP_SKILL = ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
SETUP_SKILL = ROOT / "skills" / "external" / "sdd-project-setup" / "SKILL.md"
GATE_SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

TITLE = "Directory Governance (Named, Documented, Ignored When Temporary)"
OWNER_LINK = ".specify/shared/guidelines/directory-governance.md"
TEMP_OWNER = "shared/guidelines/temp-directory-discipline.md"
HEADING = "## Temporary Directory Discipline"

TEMPLATE_TITLE_RE = re.compile(r"^### [IVXLC0-9]+\. (.+)$", re.M)
SKILL_ENTRY_RE = re.compile(rf"^  - \*\*{re.escape(TITLE)}\*\* —", re.M)


def _text(path: Path) -> str:
    assert path.is_file(), f"missing file: {path}"
    return path.read_text(encoding="utf-8")


def _principle_block(text: str, title: str) -> str:
    m = re.search(
        rf"^### [IVXLC0-9]+\. {re.escape(title)}\s*$(.*?)(?=^### |^## |\Z)",
        text, re.M | re.S,
    )
    assert m, f"principle {title!r} not found"
    return m.group(0)


def _section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.strip() == heading), None)
    assert start is not None, f"section heading {heading!r} not found"
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## ") or lines[i].startswith("# "):
            end = i
            break
    return "\n".join(lines[start:end])


def _load_gate_scanner():
    spec = importlib.util.spec_from_file_location("_scan_gates_dir_gov", GATE_SCANNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- owner document ---


def test_owner_declares_single_source_of_truth():
    opening = "\n".join(_text(OWNER).splitlines()[:6])
    assert "single source of truth" in opening.lower(), (
        "the owner doc must declare itself the single source of truth in its opening lines"
    )
    assert "目录" in opening, "the owner doc must name what it owns"


def test_owner_defines_naming_rules():
    body = _text(OWNER)
    for token in (
        "^[a-z0-9]+(-[a-z0-9]+)*$",
        "kebab-case",
        "MUST NOT be created",
        "MUST NOT be renamed",
    ):
        assert token in body, f"owner doc missing naming-rule token: {token!r}"


def test_owner_requires_registration_in_the_same_change():
    body = _text(OWNER)
    assert "in the same change that creates it" in body, (
        "the registration obligation must be same-change, not follow-up"
    )
    assert "documented nowhere MUST NOT be created" in body, (
        "the doc must forbid a directory with no documented meaning"
    )


def test_owner_routes_temporary_directories_to_their_owner():
    body = _text(OWNER)
    assert TEMP_OWNER in body, "the doc must route temporary directories to their owner"
    assert ".gitignore" in body, "the doc must carry the ignore requirement for temp data"
    assert "sanctioned root" in body, "the doc must require a sanctioned temp root"


def test_owner_indexes_area_maps_without_copying_them():
    body = _text(OWNER)
    for path in (
        ".specify/instructions.md",
        "docs/concepts/documentation-model.md",
        "shared/definitions/framework-map.md",
    ):
        assert path in body, f"the owner index is missing its area map: {path}"
    # The temp owner's detail table must stay there, not be restated here.
    assert "| 场景 | 落点 | 忽略要求 |" not in body, (
        "the owner doc copied the temp-directory detail table instead of routing to it"
    )


def test_owner_registers_the_loop_runtime_roots():
    body = _text(OWNER)
    assert "`<repo>/.specify/.tmp/sdd-loop/`" in body, (
        "temporary runtime data must live under .specify/.tmp/"
    )
    assert "`<repo>/.specify/state/`" in body, (
        "long-lived runtime state must live under .specify/state/"
    )
    assert "one file per line" in body, (
        "the state archive must be per-entry, never one shared aggregate"
    )
    assert ".spec-kit/" in body and "MUST NOT be re-created" in body, (
        "the retired root must be named and explicitly retired"
    )
    assert "sdd-loop-driver" in body, "the runtime roots must name their owning skill"
    assert "MUST NOT be created" in body, "ad-hoc runtime alternatives must be forbidden"
    assert ".specify/.gitignore" in body, (
        "temporary runtime data must be covered by the .specify-scoped ignore rules"
    )
    assert "directory-governance.md" in _text(TEMP_DOC), (
        "the temp-directory owner must route owner-declared runtime roots to this owner"
    )


def test_loop_driver_defaults_no_longer_name_the_retired_root():
    for rel in (
        "skills/external/sdd-loop-driver/references/dispatch-recipes.md",
        "skills/external/sdd-loop-driver/scripts/line-registry.py",
    ):
        assert ".spec-kit" not in _text(ROOT / rel), (
            f"{rel} still carries the retired .spec-kit root"
        )


@pytest.mark.parametrize(
    "path", [LOOP_SKILL, SETUP_SKILL], ids=["loop-driver", "project-setup"],
)
def test_remote_capable_skills_bind_target_governance(path: Path):
    body = _text(path)
    assert "目标项目治理优先" in body, (
        "a skill that can act on a remote target must bind the target's governance"
    )
    assert ".specify/memory/constitution.md" in body
    assert ".specify/instructions.md" in body
    assert re.search(r"MUST NOT[^。\n]*ad-hoc 目录|ad-hoc 目录[^。\n]*MUST NOT", body), (
        "the skill must forbid ad-hoc directory creation in the target repository"
    )
    assert "ssh" in body, "the constraint must cover the remote (ssh) topology"


def test_loop_driver_state_spine_stays_in_the_state_archive():
    body = _text(LOOP_SKILL)
    assert "<repo>/.specify/state/<line_id>.md" in body, (
        "the state spine must live in the long-lived .specify/state/ archive"
    )
    assert "<repo>/.specify/.tmp/sdd-loop/" in body, (
        "temporary runtime data must live under .specify/.tmp/"
    )
    assert "--state-dir" in body, (
        "the state spine must be bound to the archive or an explicit --state-dir"
    )
    assert "git check-ignore -q" in body, (
        "the driver must verify ignore coverage before writing inside a repository"
    )


def test_framework_map_registers_the_runtime_roots():
    for path in (
        ROOT / "shared" / "definitions" / "framework-map.md",
        ROOT / ".specify" / "shared" / "definitions" / "framework-map.md",
    ):
        body = _text(path)
        assert "`.specify/state/`" in body, f"{path} does not register .specify/state/"
        assert "`.specify/.tmp/`" in body, f"{path} does not register .specify/.tmp/"
        assert "`.specify/goal/<slug>/`" in body, f"{path} does not register .specify/goal/"


def test_skill_state_and_scratch_defaults_live_under_declared_roots():
    config = _text(ROOT / "skills" / "internal" / "manage-agents" / "scripts" / "config-agent.sh")
    assert ".agent-config" not in config, (
        "manage-agents must not create a repo-local hidden state directory"
    )
    assert "spec-kit/agents" in config, (
        "manage-agents state must live under the user-level state root"
    )
    for rel in (
        "skills/internal/create-team/scripts/dispatch.sh",
        "skills/external/sdd-loop-driver/scripts/watch-target.sh",
    ):
        text = _text(ROOT / rel)
        assert not re.search(r"\$HOME/tmp/spec-kit-", text), (
            f"{rel} uses a flat ~/tmp/<name> root instead of ~/tmp/<project>/<purpose>"
        )


def test_owner_mirror_is_in_sync():
    assert _text(OWNER) == _text(OWNER_MIRROR), (
        "shared/guidelines/directory-governance.md drifted from its .specify mirror; "
        "run: python3 scripts/python/sync-mirrors.py --write --only "
        "shared/guidelines/directory-governance.md"
    )


# --- principle landing ---


@pytest.mark.parametrize("path", [TEMPLATE, LIVE], ids=["template", "live"])
def test_principle_lands_and_anchors_the_owner(path: Path):
    text = _text(path)
    titles = {m.group(1).strip() for m in TEMPLATE_TITLE_RE.finditer(text)}
    assert TITLE in titles, f"{path.name} is missing principle {TITLE!r}"
    block = _principle_block(text, TITLE)
    assert OWNER_LINK in block, "the principle must anchor the owner document"
    assert re.search(r"reference it, do not restate it", re.sub(r"\s+", " ", block)), (
        "the principle must state reference-not-restate semantics"
    )
    assert re.search(r"MUST NOT\s+justify|MUST NOT\s+be used to justify",
                     re.sub(r"\s+", " ", block)), (
        "the principle must carry the no-new-machinery scope limit"
    )


def test_generator_must_include_lists_the_principle():
    assert SKILL_ENTRY_RE.search(_text(SKILL)), (
        "manage-constitution SKILL.md must carry the principle as a "
        "`  - **<title>** — …` MUST-include entry"
    )


# --- ambient pointer ---


@pytest.mark.parametrize(
    "path", [INSTR_TEMPLATE, INSTR_MIRROR, INSTR_LIVE],
    ids=["template", "mirror", "live"],
)
def test_ambient_section_points_to_the_owner(path: Path):
    body = _section(_text(path), HEADING)
    assert TEMP_OWNER in body, "the ambient section must keep its temp-dir pointer"
    assert OWNER_LINK in body, (
        "the ambient section must point at the directory-governance owner"
    )


# --- wording safety ---


def test_new_surfaces_add_no_blocking_gate():
    blocking_re = _load_gate_scanner().BLOCKING_RE
    surfaces = {
        "owner doc": _text(OWNER),
        "template principle": _principle_block(_text(TEMPLATE), TITLE),
        "live principle": _principle_block(_text(LIVE), TITLE),
    }
    for name, text in surfaces.items():
        hits = [m.group(0) for line in text.splitlines()
                for m in blocking_re.finditer(line)]
        assert not hits, f"{name} trips BLOCKING_PATTERNS: {hits}"
