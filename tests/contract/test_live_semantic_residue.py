"""G-6 (T067) — the live old-semantic residue scan (classes C1…C7).

Roots, exclusions and the class roster are read from `research.md` § 5 at test time — this
module owns only the compiled patterns, and it fails if the declaration grows a class it does
not compile. Every class must read zero on the live tree; the retired corpus proves each class
can still go red, and a retired sentence appended to a copy of a live file proves the walker
(not just a text helper) reports it.

Two scanning decisions are readings, recorded here rather than hidden:

* **Non-prose files.** The walk reads prose/code surfaces only (`SURFACE_SUFFIXES`). `.json`
  files under these roots are machine audit records — a `binding-rename-receipt.json` quotes the
  retired pointer in its `before` field on purpose — so scanning them would demand rewriting the
  audit trail. That is the same reason the declared exclusion list carries `history/` and
  `archive/`.
* **C3's qualifier.** C3's meaning is "/speckit.goal as the *anchor-archive* authoring entry".
  The inverted model states the opposite in the same shape ("`/speckit.goal` is the sole
  authoring entry for **action-level Goal** definitions"), so a candidate whose sentence carries
  the new-model qualifier (`action-level` / `行动级` / `short-horizon`) is the new claim, not
  residue. The qualifier is sentence-scoped; a retired claim does not carry it.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("SPECKIT_GUARD_ROOT") or REPO_ROOT)
RESEARCH = REPO_ROOT / ".specify/specs/101-anchor-goal-realignment/research.md"
FIXTURE_CORPUS = REPO_ROOT / "tests/fixtures/anchor-goal-realignment/residue-corpus"

SURFACE_SUFFIXES = {
    ".md", ".py", ".sh", ".ps1", ".yaml", ".yml", ".toml", ".cfg", ".puml", ".txt",
}
C5_SCOPE = re.compile(r"^\.specify/anchoring/[^/]+/(goal|anchor)\.md$")
C7_SCOPE = ".specify/features.md"
C3_NEW_MODEL_QUALIFIER = re.compile(r"(?i)action-level|行动级|short-horizon")

#: The compiled set. The class MEANINGS are owned by research.md § 5; these are the patterns
#: that decide them, and the corpus below pins that each still fires on the retired form.
CLASS_PATTERNS = {
    "C1": [
        r"(?i)^[\s>#*+-]*(a|an|the)?\s*\**[Gg]oal\**\s+(is|means|refers to)\s+(a|an|the)?\s*(project-level|long-horizon|long-term objective)",
        r"(?i)^\|\s*\**[Gg]oal\**\s*\|[^\|\n]*project-level",
        r"^\|\s*(Goal|目标)\s*\|[^\|\n]*项目级",
        r"(目标|Goal)[^\n。\|]{0,12}(是|定义为)[^\n。\|]{0,15}(项目级|远期目标)",
    ],
    "C2": [
        r"(?i)\b(goal|目标)\b[^\n]{0,30}\b(top of|highest (level|layer)|最高层)\b[^\n]{0,30}\b(anchor|锚点)\b",
        r"(?i)\b(anchor|锚点)\b[^\n]{0,40}\b(is|as)\s+(a\s+)?(sub-?goal|child goal|goal slice|下级目标)\b",
    ],
    "C3": [
        r"(?i)speckit\.goal[^\n]{0,160}(sole authoring|only authoring|唯一撰写)",
        r"(?i)(sole authoring entry|唯一撰写入口)[^\n]{0,160}speckit\.goal",
        r"speckit\.goal[^\n]{0,120}(锚点档案|anchoring archive)",
        r"(锚点档案|anchoring archive)[^\n]{0,120}speckit\.goal",
    ],
    "C4": [r"\.specify/goal/<[^>]+>/summary/"],
    "C5": [r"^\#\s*Goal:", r"\.specify/goal(?![a-z])"],
    "C6": [r"/speckit\.goal\s+(targets|migrate|migrate-archive|coordinate)\b"],
    "C7": [
        r"\.specify/goal/<[^>]+>",
        r"\.specify/anchoring/<[^>]+>/goal\.md",
        r"(?i)project-level goal",
        r"goal\s*=\s*设计师",
    ],
}
COMPILED = {name: [re.compile(p) for p in patterns]
            for name, patterns in CLASS_PATTERNS.items()}


def declaration() -> dict:
    """The `live_surface_roots` block declared in research.md § 5 (the only root table)."""
    text = RESEARCH.read_text(encoding="utf-8")
    match = re.search(r"```yaml\n(.*?)```", text, re.S)
    assert match, "research.md carries no yaml declaration block"
    block = yaml.safe_load(match.group(1))
    assert "live_surface_roots" in block, block
    return block["live_surface_roots"]


def declared_classes() -> list[str]:
    text = RESEARCH.read_text(encoding="utf-8")
    return sorted(set(re.findall(r"(?m)^\|\s*(C\d)\s*\|", text)))


def _split(value) -> list[str]:
    items = value if isinstance(value, list) else [value]
    out = []
    for item in items:
        for part in str(item).split(","):
            part = part.strip().strip("/")
            if part and not part.startswith("#"):
                out.append(part)
    return out


def walk(root: Path, decl: dict) -> list[Path]:
    root = Path(root)
    excluded_dirs = set(_split(decl.get("excluded_dirs_any_depth") or []))
    excluded_files = [str(item).split("#")[0].strip()
                      for item in (decl.get("excluded_files") or [])]
    excluded_files = [pattern for pattern in excluded_files if pattern]
    seen: dict[str, Path] = {}
    for rel in _split(decl["dirs"]):
        base = root / rel
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in SURFACE_SUFFIXES:
                continue
            relative = path.relative_to(root)
            if set(relative.parts[:-1]) & excluded_dirs:
                continue
            posix = relative.as_posix()
            if any(re.fullmatch(_glob_to_regex(pattern), posix) for pattern in excluded_files):
                continue
            seen[posix] = path
    for rel in _split(decl["files"]):
        path = root / rel
        if path.is_file():
            seen[rel] = path
    return [seen[key] for key in sorted(seen)]


def _glob_to_regex(pattern: str) -> str:
    """`**/` crosses zero or more directories; `*` stays inside one segment."""
    out: list[str] = []
    index = 0
    while index < len(pattern):
        if pattern.startswith("**/", index):
            out.append("(?:.*/)?")
            index += 3
        elif pattern.startswith("**", index):
            out.append(".*")
            index += 2
        elif pattern[index] == "*":
            out.append("[^/]*")
            index += 1
        else:
            out.append(re.escape(pattern[index]))
            index += 1
    return "".join(out)


def scan_text(text: str, class_id: str) -> list[str]:
    """Hit lines for one class; C3 applies its new-model qualifier per sentence."""
    patterns = COMPILED[class_id]
    if class_id == "C3":
        hits = []
        for sentence in re.split(r"(?<=[.!?。])\s+|\n\s*\n", text):
            if not any(pattern.search(sentence) for pattern in patterns):
                continue
            if C3_NEW_MODEL_QUALIFIER.search(sentence):
                continue
            hits.extend(line for line in sentence.splitlines() if line.strip())
        return hits
    hits = []
    for line in text.splitlines():
        if any(pattern.search(line) for pattern in patterns):
            hits.append(line)
    return hits


def scan_tree(root: Path, decl: dict | None = None) -> dict[str, list[str]]:
    decl = decl or declaration()
    results = {class_id: [] for class_id in COMPILED}
    for path in walk(root, decl):
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for class_id in COMPILED:
            if class_id == "C5" and not C5_SCOPE.match(relative):
                continue
            if class_id == "C7" and relative != C7_SCOPE:
                continue
            for hit in scan_text(text, class_id):
                results[class_id].append(f"{relative}: {hit.strip()[:160]}")
    return results


def test_declaration_is_the_root_table() -> None:
    decl = declaration()
    assert len(_split(decl["dirs"])) >= 20, _split(decl["dirs"])
    assert _split(decl["files"]), "no file roots declared"
    assert _split(decl["excluded_dirs_any_depth"]), "no exclusions declared"


def test_module_compiles_exactly_the_declared_classes() -> None:
    assert declared_classes() == sorted(COMPILED), (
        declared_classes(), sorted(COMPILED))


def test_live_tree_has_no_old_semantic_residue() -> None:
    results = scan_tree(ROOT)
    offenders = {class_id: hits for class_id, hits in results.items() if hits}
    assert not offenders, "\n".join(
        f"{class_id} ({len(hits)}):\n  " + "\n  ".join(hits[:12])
        for class_id, hits in offenders.items())


def test_scan_is_deterministic() -> None:
    assert scan_tree(ROOT) == scan_tree(ROOT)


def test_every_class_goes_red_on_the_retired_corpus() -> None:
    missing = []
    for class_id in COMPILED:
        text = (FIXTURE_CORPUS / "retired" / f"{class_id}.md").read_text(encoding="utf-8")
        if not scan_text(text, class_id):
            missing.append(class_id)
    assert not missing, f"classes that no longer fire on the retired form: {missing}"


def test_current_wording_is_not_residue() -> None:
    false_positives = {}
    for class_id in COMPILED:
        text = (FIXTURE_CORPUS / "current" / f"{class_id}.md").read_text(encoding="utf-8")
        hits = scan_text(text, class_id)
        if hits:
            false_positives[class_id] = hits
    assert not false_positives, false_positives


def test_injection_of_one_retired_sentence_into_a_live_file_copy_is_red(tmp_path: Path) -> None:
    decl = declaration()
    source = REPO_ROOT / "templates/commands/anchor.md"
    injected = tmp_path / "templates/commands"
    injected.mkdir(parents=True)
    (injected / "anchor.md").write_text(
        source.read_text(encoding="utf-8")
        + "\n`/speckit.goal` is the sole authoring entry for goal definitions in the goal archive.\n",
        encoding="utf-8")
    results = scan_tree(tmp_path, decl)
    assert results["C3"], results
    assert all("templates/commands/anchor.md" in hit for hit in results["C3"])
    assert not scan_tree(REPO_ROOT, decl)["C3"], "the live tree already fails C3"
