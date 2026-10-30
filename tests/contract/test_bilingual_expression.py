"""Contract tests for Feature 078 bilingual-expression (red-first, T002).

Owns the assertions pinned by
``.specify/specs/078-bilingual-expression/contracts/{owner-document,checker,distribution}.md``
and quickstart.md S2/S3/S7/S8. Legs:

* owner-document structure leg (T003 turns green): plan.md § Document Structure
  Chapter Tree nine chapters verbatim, header owner declaration naming the six
  fact groups verbatim within the first 40 non-empty lines, non-empty
  ``**Readers**`` / ``**Reading scenario**`` rows, four ``- `` led enumerations
  (方向规则 / 覆盖定义面 / 豁免面 / 唯一形态字面量条款), S1…S4 signal list,
  verbatim [[STR-002]]/[[STR-003]] forms and exactly one form-regex
  registration line.
* scan fixture legs (T007 turns green): S2 compliant rc=0 no findings,
  full-width fixture rc=1 with ``file:line [full-width-parens]``,
  same-language fixture rc=1 with ``same-language-bracket``.
* coverage leg (T007): ``coverage`` rejects ``--path`` (rc=2) and reads the
  coverage list from the owner document instead of embedding a copy.
* census leg (T007/S8): rc=0, total equals the bilingual Canonical count of
  the real glossary parsed with ``glossary-utils.py`` table parsing.
* SC-001 keyword leg (T009): the keyword table is derived programmatically
  from the owner document's four enumeration list items — never hand-written.
* drift guard legs (T017, distribution.md C-006): (i) the three STR literals
  have unique consumption points; (ii) the three mirror copies are byte-equal
  to their framework sources, with the mirror list derived from
  ``sync-mirrors.py`` ``MIRROR_PAIRS`` (not hardcoded); (iii) the ambient
  section is summary + pointer (``[[STR-001]]`` present, zero keyword hits).
* sampling leg (T011, measurement.md C-004): the checker module exposes
  ``sample_lines(lines)`` selecting every k-th line with k = ceil(n/10),
  pinned deterministic.

Red-first (Constitution IV): at T002 the owner document, checker and ambient
section do not exist, so legs red as "artifact missing" — never as an import
or collection error. Each helper asserts the artifact path first.
"""
from __future__ import annotations

import importlib.util
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

OWNER_DOC = REPO_ROOT / "shared" / "guidelines" / "bilingual-expression.md"
OWNER_DOC_REL = Path("shared") / "guidelines" / "bilingual-expression.md"
CHECKER = REPO_ROOT / "scripts" / "python" / "bilingual-expression-check.py"
CHECKER_REL = Path("scripts") / "python" / "bilingual-expression-check.py"
AMBIENT_TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
SYNC_MIRRORS = REPO_ROOT / "scripts" / "python" / "sync-mirrors.py"
GLOSSARY_UTILS = REPO_ROOT / "scripts" / "python" / "glossary-utils.py"
REAL_GLOSSARY = REPO_ROOT / ".specify" / "memory" / "glossary.md"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "bilingual"
FIXTURE_COMPLIANT = FIXTURES / "compliant-definition.md"
FIXTURE_FULLWIDTH = FIXTURES / "fullwidth-definition.md"
FIXTURE_SAME_LANG = FIXTURES / "same-language-definition.md"
SELF_REL = Path("tests") / "contract" / "test_bilingual_expression.py"

STR_001 = "shared/guidelines/bilingual-expression.md"
STR_002 = "中文(English)"
STR_003 = "English(中文)"

# plan.md § Document Structure / Chapter Tree (nine chapters, verbatim).
CHAPTER_TREE = [
    "头部与 owner 声明",
    "定义处与可判定信号",
    "方向规则与唯一形态",
    "覆盖定义面（封闭集）",
    "豁免面（封闭集）",
    "一致性与词汇表",
    "迁移边界与存量差异",
    "与相邻纪律的交界",
    "检查器与守卫",
]

SIX_FACT_GROUPS = ["方向规则", "唯一形态", "覆盖定义面封闭集", "豁免面封闭集", "一致性规则", "迁移边界"]

# The four enumeration groups and their owning headings in the owner document.
ENUM_HEADINGS = {
    "direction": "### 方向规则",
    "coverage": "## 覆盖定义面（封闭集）",
    "exemption": "## 豁免面（封闭集）",
    "form": "### 唯一形态字面量条款",
}

FINDING_RE = re.compile(r"\.md:\d+ \[([a-z-]+)\]")
BILINGUAL_CANONICAL_RE = re.compile(r"^[^\s|]+[(][^()]+[)]$")


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _owner_lines() -> list[str]:
    assert OWNER_DOC.is_file(), f"owner document missing: {OWNER_DOC_REL}"
    return OWNER_DOC.read_text(encoding="utf-8").splitlines()


def _items_under(lines: list[str], heading: str) -> list[str]:
    """Return the ``- `` list items under ``heading`` until the next heading
    of the same or higher level."""
    items: list[str] = []
    in_section = False
    level = heading.count("#")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            cur_level = len(stripped) - len(stripped.lstrip("#"))
            if in_section and cur_level <= level:
                break
            if stripped == heading:
                in_section = True
            continue
        if in_section and line.startswith("- "):
            items.append(line[2:].strip())
    return items


def derive_keywords() -> dict[str, list[str]]:
    """Derive the SC-001 keyword table from the owner document's four
    enumeration list items (programmatic, never hand-written)."""
    lines = _owner_lines()
    return {group: _items_under(lines, heading) for group, heading in ENUM_HEADINGS.items()}


def all_keywords() -> list[str]:
    keywords: list[str] = []
    for items in derive_keywords().values():
        keywords.extend(items)
    return keywords


def _run_checker(*args: str) -> subprocess.CompletedProcess:
    assert CHECKER.is_file(), f"checker missing: {CHECKER_REL}"
    return subprocess.run(
        [sys.executable, str(CHECKER), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def _ambient_section_lines() -> list[str]:
    assert AMBIENT_TEMPLATE.is_file(), "ambient template missing: templates/instructions-template.md"
    lines = AMBIENT_TEMPLATE.read_text(encoding="utf-8").splitlines()
    heading = "## Bilingual Expression (双语表述)"
    try:
        start = lines.index(heading)
    except ValueError:
        pytest.fail(f"ambient heading not found verbatim: {heading}")
    body: list[str] = []
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        body.append(line)
    return body


# --------------------------------------------------------------------------- #
# owner-document structure leg (T003)
# --------------------------------------------------------------------------- #


def test_owner_doc_chapter_tree_verbatim():
    lines = _owner_lines()
    headings = {line.strip() for line in lines if line.startswith("## ")}
    missing = [f"## {name}" for name in CHAPTER_TREE if f"## {name}" not in headings]
    assert missing == [], f"chapter tree chapters missing: {missing}"


def test_owner_doc_header_declaration():
    lines = _owner_lines()
    non_empty = [line for line in lines if line.strip()][:40]
    header = "\n".join(non_empty)
    assert "唯一" in header, "header must declare sole ownership"
    missing = [g for g in SIX_FACT_GROUPS if g not in header]
    assert missing == [], f"six fact groups not named verbatim in header: {missing}"
    reader_rows = [line for line in non_empty if line.startswith("**Readers**")]
    scenario_rows = [line for line in non_empty if line.startswith("**Reading scenario**")]
    assert len(reader_rows) == 1 and reader_rows[0].split(":", 1)[-1].strip(), "Readers row missing or empty"
    assert len(scenario_rows) == 1 and scenario_rows[0].split(":", 1)[-1].strip(), (
        "Reading scenario row missing or empty"
    )


def test_owner_doc_four_enumerations_are_lists():
    lines = _owner_lines()
    for group, heading in ENUM_HEADINGS.items():
        items = _items_under(lines, heading)
        assert items, f"enumeration group {group!r} has no '- ' items under {heading!r}"


def test_owner_doc_signal_list_s1_s4():
    text = "\n".join(_owner_lines())
    for sid in ("S1", "S2", "S3", "S4"):
        assert re.search(rf"\b{sid}\b", text), f"signal {sid} missing"
    assert "首次定义" in text, "first-definition semantics must be addressed"
    assert "不在机械范围" in text or "不属于任何可判定信号" in text, (
        "must declare first-definition judgement out of mechanical scope"
    )


def test_owner_doc_str_forms_and_single_regex_registration():
    lines = _owner_lines()
    text = "\n".join(lines)
    assert STR_002 in text, "verbatim form STR-002 missing"
    assert STR_003 in text, "verbatim form STR-003 missing"
    registration = [line for line in lines if "唯一登记行" in line]
    assert len(registration) == 1, f"form-regex registration lines: {len(registration)} (must be 1)"
    match = re.search(r"`([^`]+)`", registration[0])
    assert match, "registration line must carry the regex literal in backticks"
    pattern = re.compile(match.group(1))
    assert pattern.search(STR_002), "registered regex must match STR-002 form"
    assert pattern.search(STR_003), "registered regex must match STR-003 form"


# --------------------------------------------------------------------------- #
# scan fixture legs (S2; T007 turns green)
# --------------------------------------------------------------------------- #


def test_scan_compliant_fixture():
    result = _run_checker("--action", "scan", "--path", str(FIXTURE_COMPLIANT))
    assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    assert FINDING_RE.search(result.stdout) is None, f"unexpected findings:\n{result.stdout}"


def test_scan_fullwidth_fixture_red():
    result = _run_checker("--action", "scan", "--path", str(FIXTURE_FULLWIDTH))
    assert result.returncode == 1, f"expected rc=1, got {result.returncode}\n{result.stdout}{result.stderr}"
    assert re.search(r"fullwidth-definition\.md:\d+ \[full-width-parens\]", result.stdout), (
        f"missing full-width-parens finding with file:line location:\n{result.stdout}"
    )


def test_scan_same_language_fixture_red():
    result = _run_checker("--action", "scan", "--path", str(FIXTURE_SAME_LANG))
    assert result.returncode == 1, f"expected rc=1, got {result.returncode}\n{result.stdout}{result.stderr}"
    assert re.search(r"same-language-definition\.md:\d+ \[same-language-bracket\]", result.stdout), (
        f"missing same-language-bracket finding with file:line location:\n{result.stdout}"
    )


# --------------------------------------------------------------------------- #
# coverage leg (S3) and census leg (S8); T007 turns green
# --------------------------------------------------------------------------- #


def test_coverage_action():
    ok = _run_checker("--action", "coverage")
    assert ok.returncode == 0, f"coverage must pass on the live tree:\n{ok.stdout}{ok.stderr}"
    rejected = _run_checker("--action", "coverage", "--path", str(FIXTURE_COMPLIANT))
    assert rejected.returncode == 2, (
        f"coverage must reject --path with rc=2, got {rejected.returncode}\n{rejected.stdout}{rejected.stderr}"
    )
    source = CHECKER.read_text(encoding="utf-8")
    assert str(OWNER_DOC_REL) in source, (
        "checker must read the coverage list from the owner document "
        f"({OWNER_DOC_REL}), not embed a copy"
    )


def test_census_action():
    glossary_utils = _load_module(GLOSSARY_UTILS, "glossary_utils_for_census")
    entries = glossary_utils.parse_entries(REAL_GLOSSARY.read_text(encoding="utf-8"))
    expected_total = sum(
        1 for e in entries if BILINGUAL_CANONICAL_RE.match(e["canonical"].strip())
    )
    assert expected_total > 0, "real glossary has no bilingual Canonical entries?"
    result = _run_checker("--action", "census", "--json")
    assert result.returncode == 0, f"census must pass:\n{result.stdout}{result.stderr}"
    summary = json.loads(result.stdout)
    assert summary["census_total"] == expected_total, (
        f"census_total {summary.get('census_total')} != glossary bilingual count {expected_total}"
    )


# --------------------------------------------------------------------------- #
# SC-001 keyword leg (S7): programmatic derivation only
# --------------------------------------------------------------------------- #


def test_sc001_keyword_snapshot():
    keywords_by_group = derive_keywords()
    assert set(keywords_by_group) == set(ENUM_HEADINGS), "keyword table must derive from all four groups"
    for group, items in keywords_by_group.items():
        assert items, f"group {group!r} derived an empty keyword list"
        for item in items:
            assert item.strip(), f"group {group!r} has an empty keyword item"
    ambient_body = "\n".join(_ambient_section_lines())
    leaked = [kw for kw in all_keywords() if kw and kw in ambient_body]
    assert leaked == [], f"ambient section must not repeat enumeration keywords: {leaked}"


# --------------------------------------------------------------------------- #
# drift guard legs (distribution.md C-006; T008/T012/T017 turn green)
# --------------------------------------------------------------------------- #


def _corpus_files() -> list[Path]:
    roots = [
        REPO_ROOT / "shared",
        REPO_ROOT / "templates",
        REPO_ROOT / "scripts",
        REPO_ROOT / "tests",
    ]
    files: list[Path] = []
    for root in roots:
        files.extend(p for p in root.rglob("*") if p.is_file() and p.suffix in {".md", ".py"})
    return files


def _str_allowed_paths() -> set[Path]:
    """The unique consumption points of the three STR literals."""
    allowed = {
        OWNER_DOC,
        REPO_ROOT / ".specify" / OWNER_DOC_REL,
        CHECKER,
        REPO_ROOT / ".specify" / CHECKER_REL,
        REPO_ROOT / SELF_REL,
        AMBIENT_TEMPLATE,
        REPO_ROOT / ".specify" / "templates" / "instructions-template.md",
    }
    allowed.update(p for p in FIXTURES.rglob("*") if p.is_file())
    return allowed


def test_drift_str_literal_unique_consumers():
    literals = {"STR-001": STR_001, "STR-002": STR_002, "STR-003": STR_003}
    allowed = _str_allowed_paths()
    violations: list[str] = []
    for path in _corpus_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for name, literal in literals.items():
            if literal in text and path not in allowed:
                violations.append(f"{name} consumed at {path.relative_to(REPO_ROOT)}")
    assert violations == [], f"STR literals escaped their unique consumption points: {violations}"


def _mirror_pairs() -> list[tuple[str, str]]:
    sync_mirrors = _load_module(SYNC_MIRRORS, "sync_mirrors_for_drift_guard")
    return [(src, dst) for src, dst, _strict, _excl in sync_mirrors.MIRROR_PAIRS]


def _mirror_path_for(source_rel: Path) -> Path | None:
    """Derive the mirror destination for a framework-source path from
    ``sync-mirrors.py`` MIRROR_PAIRS (never a hardcoded mapping)."""
    source_posix = source_rel.as_posix()
    for src_root, dst_root, _strict, exclude_parts in [
        (s, d, st, ex) for s, d, st, ex in _mirror_pairs()
    ]:
        parts = Path(source_posix).parts
        if any(part in exclude_parts for part in parts):
            continue
        if source_posix == src_root:
            return REPO_ROOT / dst_root
        prefix = src_root + "/"
        if source_posix.startswith(prefix):
            return REPO_ROOT / dst_root / source_posix[len(prefix) :]
    return None


def test_drift_mirror_identity_derived_from_mirror_pairs():
    sources = [OWNER_DOC_REL, Path("templates") / "instructions-template.md", CHECKER_REL]
    for source_rel in sources:
        source = REPO_ROOT / source_rel
        assert source.is_file(), f"framework source missing: {source_rel}"
        mirror = _mirror_path_for(source_rel)
        assert mirror is not None, f"no MIRROR_PAIRS entry covers {source_rel}"
        assert mirror.is_file(), f"mirror missing for {source_rel}: {mirror.relative_to(REPO_ROOT)}"
        assert mirror.read_bytes() == source.read_bytes(), (
            f"mirror drift: {mirror.relative_to(REPO_ROOT)} != {source_rel}"
        )


def test_drift_ambient_summary_plus_pointer_form():
    lines = AMBIENT_TEMPLATE.read_text(encoding="utf-8").splitlines()
    heading = "## Bilingual Expression (双语表述)"
    assert lines.count(heading) == 1, f"ambient heading must appear exactly once, got {lines.count(heading)}"
    body = "\n".join(_ambient_section_lines())
    assert "[[STR-001]]" in body, "ambient section must carry the [[STR-001]] owner pointer"
    leaked = [kw for kw in all_keywords() if kw and kw in body]
    assert leaked == [], f"ambient section repeats enumeration keywords: {leaked}"


# --------------------------------------------------------------------------- #
# deterministic sampling leg (measurement.md C-004; T007 exposes sample_lines)
# --------------------------------------------------------------------------- #


def test_sample_lines_deterministic():
    checker_module = _load_module(CHECKER, "bilingual_expression_check_for_sampling")
    sample_lines = getattr(checker_module, "sample_lines", None)
    assert callable(sample_lines), "checker module must expose sample_lines(lines)"
    lines = [f"line-{i:02d}" for i in range(25)]
    k = math.ceil(len(lines) / 10)
    expected = lines[k - 1 :: k]
    assert expected, "expected sample must be non-empty"
    assert sample_lines(lines) == expected, "sample_lines must pick every k-th line, k=ceil(n/10)"
    assert sample_lines(lines) == sample_lines(list(lines)), "sample_lines must be deterministic"
    short = lines[:5]
    assert sample_lines(short) == short, "n<10 (k=1) must sample every line"
