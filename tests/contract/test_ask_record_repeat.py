"""Contract tests for Ask/Record/Repeat and the two-hats reachability fix.

These guard a *reachability* property rather than a behaviour: both rules already
existed and were correctly owned, and were still missed, because nothing linked
them from the surface an agent reads every turn. Correct ownership does not equal
reachability — that is the failure mode these tests exist to keep closed.

Guards, per the house pattern (owner doc -> ambient section -> contract test):
  * shared/guidelines/ask-record-repeat.md      — philosophy owner (+ mirror)
  * shared/definitions/dogfooding-definitions.md § 2.1 — two-hats owner, rule 4
  * templates/instructions-template.md          — two ambient sections (+ mirror)
  * the negative path-resolution assertion that rule 4 requires

Wording safety matters here: templates/*.md and shared/ are both inside the gate
scanner's range and the budget's integer headroom is 0, so any blocking-confirmation
literal in these surfaces breaks it directly.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

DOC = ROOT / "shared" / "guidelines" / "ask-record-repeat.md"
DOC_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / "ask-record-repeat.md"
DOC_LINK = "shared/guidelines/ask-record-repeat.md"

HATS_DOC = ROOT / "shared" / "definitions" / "dogfooding-definitions.md"
HATS_DOC_MIRROR = ROOT / ".specify" / "shared" / "definitions" / "dogfooding-definitions.md"
HATS_LINK = "shared/definitions/dogfooding-definitions.md"

SRC = ROOT / "templates" / "instructions-template.md"
MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"

ENGINE = ROOT / "scripts" / "python" / "trigger-utils.py"
SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

ARR_HEADING = "## Ask, Record, Repeat"
HATS_HEADING = "## Two Hats: Framework Source vs Client Runtime"
DOGFOOD_HEADING = "## Dogfooding Practice"

# Shipped surfaces must stay project-neutral.
FORBIDDEN = [
    "spec-kit", "specify-cli", "specify_cli", "Feature 0",
    "cloud-native-ai", ".specify/specs/0",
]

# The doc's detail must not be inlined into the ambient section (pointer shape).
DOC_ONLY_MARKERS = [
    "| 得到的答案属于 | 落点 |",
    "| 失效模式 | 由哪一环关掉 |",
    "## 为什么是\"理念\"而不是一条硬规则",
]


def read(p: Path) -> str:
    assert p.is_file(), f"missing file: {p}"
    return p.read_text(encoding="utf-8")


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i
            break
    assert start is not None, f"section heading {heading!r} not found"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start:end])


def subsection(text: str, heading: str) -> str:
    """Body of a heading at any depth, up to the next heading of same-or-higher level."""
    lines = text.splitlines()
    start = level = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i
            level = len(line) - len(line.lstrip("#"))
            break
    assert start is not None, f"subsection heading {heading!r} not found"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        stripped = lines[j].lstrip("#")
        if lines[j].startswith("#") and (len(lines[j]) - len(stripped)) <= level:
            end = j
            break
    return "\n".join(lines[start:end])


def _load_scanner():
    spec = importlib.util.spec_from_file_location("_scan_gates_arr", SCANNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- owner doc: exists, mirrored, declares ownership ---


def test_doc_exists_with_byte_identical_mirror():
    assert DOC.is_file(), f"missing philosophy owner doc: {DOC}"
    assert DOC_MIRROR.is_file(), f"missing mirror: {DOC_MIRROR}"
    assert DOC.read_bytes() == DOC_MIRROR.read_bytes(), "philosophy doc mirror drift"


def test_doc_declares_itself_the_owner():
    body = norm(read(DOC)).lower()
    assert "单一真源" in body or "single source of truth" in body, (
        "the owner doc must declare itself the single source of truth"
    )


def test_doc_carries_all_three_ideas_as_one_loop():
    body = read(DOC)
    for idea in ("Ask", "Record", "Repeat"):
        assert re.search(rf"(?m)^## \d+\. {idea} ", body), (
            f"the doc must carry a numbered section for {idea}"
        )
    # The merge into one lifecycle is the point — not three unrelated rules.
    for token in ("获取", "保留", "保活"):
        assert token in body, f"the loop stage {token!r} is missing"


def test_doc_states_the_user_proverbs_verbatim():
    """The three ideas arrived as the user's own phrasing; keep them findable."""
    body = read(DOC)
    for proverb in ("问好过于猜", "好记性不如烂笔头", "重要的事情说三遍"):
        assert proverb in body, f"the user's own wording {proverb!r} must be retained"
    for generalization in ("举一反三", "触类旁通"):
        assert generalization in body, f"the generalization duty {generalization!r} is missing"


def test_doc_defines_the_xiv_boundary():
    """Repetition is pointer-shaped or it is a drifting copy."""
    body = read(DOC)
    assert "指针形态" in body and "内容形态" in body, (
        "the doc must distinguish pointer-shaped repetition from content-shaped duplication"
    )
    assert "one-source-of-truth.md" in body, (
        "the boundary must reference the One Source of Truth owner by path"
    )
    low = norm(body).lower()
    assert "改这个事实需要编辑几个文件" in body or "more than one file" in low or \
        "more than the owner" in low, (
        "the mechanical discriminator (how many files must change) must be stated"
    )


def test_doc_gives_record_a_landing_place_table():
    assert "| 得到的答案属于 | 落点 |" in read(DOC), (
        "the doc must say where each kind of answer belongs, else 'record it' is unactionable"
    )


# --- ambient sections: present, pointer-shaped, propagated by reconcile ---


def test_template_carries_both_sections_and_their_pointers():
    for rel, p in (("templates", SRC), (".specify/templates", MIRROR)):
        body = read(p)
        headings = re.findall(r"(?m)^## .+$", body)
        assert ARR_HEADING in headings, f"{ARR_HEADING!r} missing in {rel}"
        assert HATS_HEADING in headings, f"{HATS_HEADING!r} missing in {rel}"
        assert DOC_LINK in section(body, ARR_HEADING), f"pointer to {DOC_LINK} missing in {rel}"
        assert HATS_LINK in section(body, HATS_HEADING), f"pointer to {HATS_LINK} missing in {rel}"


def test_template_mirror_parity():
    assert SRC.read_bytes() == MIRROR.read_bytes(), "instructions-template mirrors diverged"


def test_sections_are_pointer_shaped_not_content_copies():
    """The ambient sections must not inline the owner docs' detail."""
    body = read(SRC)
    for heading in (ARR_HEADING, HATS_HEADING):
        sec = section(body, heading)
        for marker in DOC_ONLY_MARKERS:
            assert marker not in sec, (
                f"{heading!r} inlines owner-doc detail {marker!r}; keep it a pointer"
            )


def test_two_hats_section_disambiguates_from_dogfooding_practice():
    """The naming collision is the trap: both sections use the word dogfooding."""
    body = read(SRC)
    hats = section(body, HATS_HEADING)
    assert DOGFOOD_HEADING.strip("# ") in hats, (
        "the two-hats section must explicitly distinguish itself from Dogfooding Practice"
    )
    # And the two must not be the same section.
    headings = re.findall(r"(?m)^## .+$", body)
    assert DOGFOOD_HEADING in headings and HATS_HEADING in headings
    assert headings.index(HATS_HEADING) != headings.index(DOGFOOD_HEADING)


def test_two_hats_section_names_the_path_resolution_trap():
    body = section(read(SRC), HATS_HEADING)
    assert ".specify" in body, "the trap is about the .specify runtime surface"
    assert re.search(r"self-match|自匹配", body), (
        "the section must name the self-matching hazard, not just the general rule"
    )


def test_proactive_trigger_section_position_is_undisturbed():
    """Feature 050's C-3 pins the trigger section between two neighbours."""
    headings = re.findall(r"(?m)^## .+$", read(SRC))
    trigger = "## Proactive Flow Trigger"
    assert trigger in headings
    assert headings.index(trigger) == headings.index("## Documentation Map") + 1
    assert headings.index("## Fact, Correctness & Logic Checks (Input Sanity)") == \
        headings.index(trigger) + 1


# --- wording safety and neutrality on shipped surfaces ---


def test_zero_blocking_pattern_hits_on_new_surfaces():
    blocking_re = _load_scanner().BLOCKING_RE
    surfaces = [
        ("philosophy doc", DOC),
        ("two-hats owner doc", HATS_DOC),
    ]
    for name, path in surfaces:
        hits = []
        for lineno, line in enumerate(read(path).splitlines(), 1):
            hits.extend(f"L{lineno}:{m.group(0)!r}" for m in blocking_re.finditer(line))
        assert not hits, f"{name} trips BLOCKING_PATTERNS (budget headroom is 0): {hits}"

    body = read(SRC)
    for heading in (ARR_HEADING, HATS_HEADING):
        sec = section(body, heading)
        hits = [m.group(0) for m in blocking_re.finditer(sec)]
        assert not hits, f"{heading} trips BLOCKING_PATTERNS: {hits}"


def test_new_surfaces_are_project_neutral():
    for name, text in (
        ("philosophy doc", read(DOC)),
        ("ask-record-repeat section", section(read(SRC), ARR_HEADING)),
        ("two-hats section", section(read(SRC), HATS_HEADING)),
    ):
        low = text.lower()
        for token in FORBIDDEN:
            assert token.lower() not in low, f"project token {token!r} leaked into {name}"


# --- the two-hats owner doc carries the new normative rule ---


def test_two_hats_owner_doc_has_mirror_parity():
    assert HATS_DOC.read_bytes() == HATS_DOC_MIRROR.read_bytes(), (
        "dogfooding-definitions mirrors diverged"
    )


def test_two_hats_rule_four_is_normative_and_guarded():
    body = subsection(read(HATS_DOC), "### 2.1 两顶帽子规则(宪法 XI,规范性)")
    assert re.search(r"(?m)^4\.\s", body), "§2.1 must carry a fourth numbered rule"
    assert "自匹配" in body, "rule 4 must name the self-match hazard"
    assert "MUST" in body, "rule 4 must be normative, not advisory"
    assert "反向断言" in body, (
        "rule 4 must require the negative assertion — the defect is invisible to "
        "tests that only ever run from one side"
    )


# --- the reverse assertion rule 4 demands ---


def test_canonical_engine_does_not_self_resolve_to_the_framework_repo(tmp_path: Path):
    """Run the CANONICAL engine from a workspace that is not this repo.

    Before the fix, resolve_root walked up looking for any ancestor containing
    `.specify/` — which the framework repo always does — so every invocation
    resolved here and wrote workspace state into the repo.
    """
    (tmp_path / ".specify" / "templates").mkdir(parents=True)
    (tmp_path / ".specify" / "memory").mkdir(parents=True)

    import importlib.util
    import sys
    spec = importlib.util.spec_from_file_location("_engine_hats_check", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    prev = Path.cwd()
    import os
    os.chdir(tmp_path)
    try:
        resolved = module.resolve_root(None)
    finally:
        os.chdir(prev)

    assert Path(resolved).resolve() == tmp_path.resolve(), (
        f"canonical engine self-resolved to {resolved} instead of the caller's "
        f"workspace {tmp_path} — the two-hats path-resolution trap (rule 4)"
    )
    assert Path(resolved).resolve() != ROOT.resolve(), (
        "the framework repo must never be the default workspace for a caller elsewhere"
    )


def test_mirrored_engine_still_resolves_its_own_project(tmp_path: Path):
    """The positive half: the mirrored copy must climb out of `.specify`."""
    import importlib.util
    import sys
    mirror = ROOT / ".specify" / "scripts" / "python" / "trigger-utils.py"
    assert mirror.is_file(), f"missing STRICT mirror: {mirror}"
    spec = importlib.util.spec_from_file_location("_engine_mirror_hats", mirror)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    resolved = module.resolve_root(None)
    assert Path(resolved).resolve() == ROOT.resolve(), (
        f"the mirrored copy must resolve to its project root, got {resolved}"
    )
    assert Path(resolved).name != ".specify", "must climb out of the .specify runtime"
