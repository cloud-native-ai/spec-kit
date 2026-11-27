"""Contract guard: the general best-practices content module (Feature 111).

Pins structure, pointers and literal presence only — whether an entry's claim is true,
and whether an entry is hollow, are accumulation-discipline and review judgements
(contracts/entry-shape.contract.md C-205). Mirror byte identity is NOT compared here;
it stays with tests/contract/test_mirror_parity_suite.py (C-402, C-404).

Legs (C-404 / FR-007):
  (a) top-level document set, the manifest's sole category table, the literal 封闭集
  (b) owner-file identity, accumulation block, placeholder <=> zero entries, entry shape
  (c) seed entry: three facts plus the SSH extension, no fabricated source line
  (d) accumulation pointer chain, the [best-practice] marker, no second engine file
  (e) framework-map registration row in source and mirror
  (f) every manifest <-> owner-file relative link resolves
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = REPO_ROOT / "shared" / "best-practices"
MIRROR_DIR = REPO_ROOT / ".specify" / "shared" / "best-practices"
MAP_SOURCE = REPO_ROOT / "shared" / "definitions" / "framework-map.md"
MAP_MIRROR = REPO_ROOT / ".specify" / "shared" / "definitions" / "framework-map.md"

MANIFEST_NAME = "README.md"
OWNER_FILES = (
    "programming-languages.md",
    "system-interfaces.md",
    "programming-frameworks.md",
    "programming-tools.md",
)
DOCUMENTS = (MANIFEST_NAME,) + OWNER_FILES
CATEGORY_BY_FILE = {
    "programming-languages.md": "编程语言",
    "system-interfaces.md": "系统接口",
    "programming-frameworks.md": "编程框架",
    "programming-tools.md": "编程工具",
}
PLACEHOLDER = "尚无条目"
MARKER = "[best-practice]"
SEED_HEADING = "Git clone 的默认协议"
SOURCE_RESIDUE = ("ai-harness", ".ah/", "/ah.")
MINIMUM_CITED_PATHS = (
    ".specify/scripts/python/feedback-utils.py",
    "shared/guidelines/knowledge-promotion.md",
    ".specify/shared/best-practices/",
    "tests/contract/test_general_best_practices.py",
)

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
REPO_PATH_PREFIXES = (".specify/", "shared/", "scripts/", "tests/")
BULLET_PRACTICE = re.compile(r"(?m)^\s*-\s+\*\*实践\*\*")
BULLET_COUNTER = re.compile(r"(?m)^\s*-\s+\*\*反例 / 证据\*\*")
BULLET_EXTENSION = re.compile(r"(?m)^\s*-\s+\*\*延伸\*\*")
BULLET_SOURCE = re.compile(r"(?m)^\s*-\s+\*\*来源\*\*")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _markdown_tables(text: str):
    """Return parsed tables as (header_cells, data_rows) with outer pipes stripped."""
    blocks = []
    block = []
    for line in text.splitlines():
        if line.strip().startswith("|"):
            block.append(line.strip())
        elif block:
            blocks.append(block)
            block = []
    if block:
        blocks.append(block)
    tables = []
    for block in blocks:
        if len(block) < 2:
            continue
        header = _cells(block[0])
        rows = [_cells(line) for line in block[2:]]
        tables.append((header, rows))
    return tables


def _cells(row: str):
    stripped = row.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _links(text: str):
    return LINK_RE.findall(text)


def _entries(text: str):
    """Split owner-file text into (heading, body) tuples at level-2 headings."""
    entries = []
    heading = None
    body = []
    for line in text.splitlines():
        if re.match(r"^## (?!#)", line):
            if heading is not None:
                entries.append((heading, "\n".join(body)))
            heading = line[3:].strip()
            body = []
        elif re.match(r"^# (?!#)", line):
            if heading is not None:
                entries.append((heading, "\n".join(body)))
                heading = None
                body = []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        entries.append((heading, "\n".join(body)))
    return entries


def _italic_lines(text: str):
    lines = []
    for line in text.splitlines():
        if re.match(r"^\s*\*[^*].*\*\s*$", line):
            lines.append(line)
    return lines


def _cited_repo_paths(text: str):
    cited = set()
    for token in CODE_SPAN_RE.findall(text):
        token = token.strip()
        if token.startswith(REPO_PATH_PREFIXES) and not any(mark in token for mark in " *<>"):
            cited.add(token.rstrip(".,;，。；"))
    return cited


@pytest.fixture(scope="module", autouse=True)
def module_prelude():
    """Shared module-read prelude (C-404): read the five documents, assert zero source
    residue, the Feature 111 attribution, and the existence of every cited repo path."""
    assert MODULE_DIR.is_dir(), "missing module directory: shared/best-practices/"
    docs = {}
    for name in DOCUMENTS:
        path = MODULE_DIR / name
        assert path.is_file(), "missing module document: %s" % name
        docs[name] = _read(path)
    for name, text in docs.items():
        for token in SOURCE_RESIDUE:
            assert token not in text, "%s carries the source residue %r" % (name, token)
    assert "Feature 111" in docs[MANIFEST_NAME], "manifest does not declare Feature 111"
    cited = set(MINIMUM_CITED_PATHS)
    for text in docs.values():
        cited |= _cited_repo_paths(text)
    for rel in sorted(cited):
        assert (REPO_ROOT / rel).exists(), "cited repository path does not exist: %s" % rel
    return docs


def test_module_document_set_and_closed_category_table(module_prelude):
    top = sorted(path.name for path in MODULE_DIR.iterdir())
    assert top == sorted(DOCUMENTS), "module top level is not exactly the five documents: %r" % top
    assert not any((MODULE_DIR / name).is_dir() for name in top), "module top level holds a subdirectory"
    mirror_top = sorted(path.name for path in MIRROR_DIR.iterdir())
    assert mirror_top == sorted(DOCUMENTS), "mirror does not carry the same five names: %r" % mirror_top

    manifest = module_prelude[MANIFEST_NAME]
    tables = _markdown_tables(manifest)
    assert len(tables) == 1, "manifest must carry exactly one Markdown table, found %d" % len(tables)
    header, rows = tables[0]
    assert header == ["模块", "文件", "内容"], "unexpected table header: %r" % (header,)
    assert len(rows) == 4, "category table must have exactly four data rows, found %d" % len(rows)

    targets = []
    for row in rows:
        module_cell, file_cell, _content = row
        row_links = _links(" | ".join(row))
        assert len(row_links) == 1, "each category row must carry exactly one relative link: %r" % (row,)
        target = row_links[0]
        assert not re.match(r"^[a-z]+:", target) and not target.startswith("/"), \
            "category link must be relative: %r" % target
        name = target.split("#")[0]
        assert name in OWNER_FILES, "category link target outside the four owner files: %r" % target
        assert module_cell.strip("* ").strip() == CATEGORY_BY_FILE[name], \
            "category cell %r does not match its owner file %r" % (module_cell, name)
        targets.append(name)
    assert sorted(targets) == sorted(OWNER_FILES), "link-target set is not the four owner files: %r" % (targets,)
    assert "封闭集" in manifest, "manifest does not carry the literal 封闭集"


def test_owner_files_placeholders_and_entry_shape(module_prelude):
    for name in OWNER_FILES:
        text = module_prelude[name]
        h1 = [line for line in text.splitlines() if re.match(r"^# (?!#)", line)]
        assert len(h1) == 1, "%s must carry exactly one H1, found %d" % (name, len(h1))
        assert CATEGORY_BY_FILE[name] in h1[0], "%s H1 does not name its category" % name

        block = "\n".join(line for line in text.splitlines() if line.startswith(">"))
        assert "README.md" in block, "%s accumulation block does not link README.md" % name
        assert "积累机制" in block, "%s accumulation block misses the literal 积累机制" % name
        assert "标题 + 实践 + 反例/证据" in block, "%s accumulation block misses the entry-shape triple" % name

        entries = _entries(text)
        for heading, body in entries:
            assert BULLET_PRACTICE.search(body), "%s entry %r misses the **实践** bullet" % (name, heading)
            assert BULLET_COUNTER.search(body), "%s entry %r misses the **反例 / 证据** bullet" % (name, heading)
            if heading == SEED_HEADING and name == "programming-tools.md":
                assert not BULLET_SOURCE.search(body), "seed entry must not carry a **来源** bullet"
            else:
                assert BULLET_SOURCE.search(body), \
                    "%s entry %r (non-seed) must carry a **来源** bullet" % (name, heading)

        placeholders = [line for line in _italic_lines(text) if PLACEHOLDER in line]
        if entries:
            assert not placeholders, "%s has entries and must not carry the placeholder" % name
        else:
            assert len(placeholders) == 1, \
                "%s is empty and must carry exactly one placeholder line, found %d" % (name, len(placeholders))


def test_seed_entry_three_facts_and_ssh_extension(module_prelude):
    text = module_prelude["programming-tools.md"]
    entries = dict(_entries(text))
    assert SEED_HEADING in entries, "seed heading %r is absent from programming-tools.md" % SEED_HEADING
    body = entries[SEED_HEADING]

    assert "默认用 HTTPS" in body, "seed misses the default-HTTPS practice"
    assert "必须显式提示" in body, "seed misses the flag-the-protocol duty for special repositories"
    assert "协议" in body and "凭据" in body, "seed misses the protocol/credential wording"
    assert "`~/.git-credentials`" in body, "seed misses the ~/.git-credentials counter-example"
    assert "HTTP" in body and "HTTPS" in body, "counter-example does not name both protocols"
    assert "导致 clone 失败" in body, "counter-example does not state the clone failure"
    assert "SSH" in body, "seed misses the SSH extension wording"
    assert BULLET_EXTENSION.search(body), "seed misses the **延伸** bullet"
    assert not BULLET_SOURCE.search(body), "seed must not carry a fabricated **来源** line"


def test_accumulation_pointer_chain_and_no_second_engine(module_prelude):
    engine = REPO_ROOT / ".specify" / "scripts" / "python" / "feedback-utils.py"
    proc = subprocess.run(
        [sys.executable, str(engine), "--help"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, "feedback-utils.py --help failed: %s" % proc.stderr
    assert re.search(r"\brecord\b", proc.stdout), "feedback-utils.py --help does not list the record action"

    assert (REPO_ROOT / "shared" / "guidelines" / "knowledge-promotion.md").is_file(), \
        "the knowledge-recording obligation owner path is missing"
    assert MARKER in module_prelude[MANIFEST_NAME], "manifest does not carry the [best-practice] marker"

    scripts = REPO_ROOT / "scripts" / "python"
    engine_files = sorted(scripts.glob("best-practices*.py")) + sorted(scripts.glob("best_practices*.py"))
    assert engine_files == [], "a second best-practices engine file exists: %r" % engine_files


def test_framework_map_registration_rows_source_and_mirror(module_prelude):
    for path in (MAP_SOURCE, MAP_MIRROR):
        text = _read(path)
        rows = [
            line
            for line in text.splitlines()
            if line.lstrip().startswith("|")
            and ".specify/shared/best-practices/" in line
            and "Feature 111" in line
        ]
        assert len(rows) == 1, \
            "%s must carry exactly one best-practices registration row, found %d" % (path.name, len(rows))


def test_relative_links_resolve(module_prelude):
    for name in DOCUMENTS:
        for target in _links(module_prelude[name]):
            if re.match(r"^[a-z]+:", target) or target.startswith("#") or target.startswith("/"):
                continue
            path_part = target.split("#")[0]
            if not path_part:
                continue
            assert (MODULE_DIR / path_part).exists(), \
                "%s: relative link does not resolve: %s" % (name, target)