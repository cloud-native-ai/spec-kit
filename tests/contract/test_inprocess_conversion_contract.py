"""Contract cases for the in-process conversion (098 US5).

Owner of the propositions: ``.specify/specs/098-suite-speed-optimizations/contracts/
inprocess-conversion.contract.md`` C-001…C-010. Carrier of the classification data:
``.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-conversion.md``.

The scanner below is the completeness denominator (C-006): a deterministic AST pass over
``tests/**/*.py`` (including ``tests/fixtures/`` and the read-only ``tests/conftest.py``)
that enumerates every ``subprocess.run`` call site. The manifest is generated from this
scan and completed by hand for the verdicts; this file re-scans and judges the manifest,
so a discovered site with no row, or a reverted conversion, turns red and is named.

Scope note (C-001 final green): WP-7 closed the contract-area groups and the fixture
layer; WP-8 (T050–T052) closed the integration/unit areas and every remaining
contract-leftover file, so the full-tree completeness case judges the whole census. Every
*covered* file is still required to classify all of its sites, and the C-008 leg requires
every converted row to keep its in-process route.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = (
    ROOT
    / ".specify"
    / "specs"
    / "098-suite-speed-optimizations"
    / "test-evidence"
    / "inprocess-conversion.md"
)

COLUMNS = ("file", "call_site", "verdict", "boundary_class", "reason")
VERDICTS = ("convert", "keep")
CONVERT_CLASS = "—"
KEEP_CLASSES = (
    "cli-contract",
    "signal-timeout-interrupt",
    "git-external",
    "process-isolation-subject",
    "other-interpreter",
    "global-state-unrecoverable",
    "copy-topology",
)
#: A keep row must carry a class from the closed set; these are the boundary kinds the
#: requirements name explicitly (C-010) and the keep-side sample the guard checks for.
NAMED_BOUNDARY_KINDS = (
    "cli-contract",
    "git-external",
    "other-interpreter",
    "global-state-unrecoverable",
    "copy-topology",
)
#: First argv tokens that are themselves the external program under test (a non-Python
#: interpreter), so the normalized target stays a command kind instead of a file name.
_EXTERNAL_COMMANDS = ("grep", "rg", "cp", "mv", "find", "node", "bash", "sh")


# --------------------------------------------------------------------------- #
# The AST scanner (completeness denominator)
# --------------------------------------------------------------------------- #
def _literal_strings(node: ast.AST | None) -> list[str]:
    if node is None:
        return []
    return [
        sub.value
        for sub in ast.walk(node)
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str)
    ]


def _const_map(tree: ast.Module) -> dict[str, list[str]]:
    """Names whose assignment mentions a script path, for a stable normalized target."""
    mapping: dict[str, list[str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                strings = _literal_strings(node.value)
                if any(s.endswith((".py", ".sh")) for s in strings):
                    mapping.setdefault(target.id, strings)
    return mapping


def _normalized_target(call: ast.Call, consts: dict[str, list[str]]) -> str:
    """The command kind: a script file name, ``specify-cli``, ``git`` or ``<computed>``.

    Only literal strings and file-wide constant names contribute, so line drift never
    changes the value and a refactor that changes the invoked script does.
    """
    arg = call.args[0] if call.args else None
    for keyword in call.keywords:
        if keyword.arg == "args":
            arg = keyword.value
    strings = list(_literal_strings(arg))
    if arg is not None:
        for sub in ast.walk(arg):
            if isinstance(sub, ast.Name) and sub.id in consts:
                strings.extend(consts[sub.id])
    candidates = [
        s
        for s in strings
        if s.endswith((".py", ".sh"))
        and not s.startswith("-")
        and "*" not in s
        and " " not in s
    ]
    if candidates:
        return Path(candidates[-1].replace("\\", "/")).name
    firsts = [s for s in strings if s and not s.startswith("-")]
    if firsts and firsts[0] in _EXTERNAL_COMMANDS:
        return firsts[0]
    if "specify" in strings or "specify_cli" in strings:
        return "specify-cli"
    if "git" in strings:
        return "git"
    if "-c" in strings:
        return "python-inline"
    return "<computed>"


class _Collector(ast.NodeVisitor):
    def __init__(self, consts: dict[str, list[str]]) -> None:
        self.consts = consts
        self.module_aliases: set[str] = set()
        self.run_names: set[str] = set()
        self.stack: list[str] = []
        self.sites: list[tuple[str, int]] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if alias.name == "subprocess":
                self.module_aliases.add(alias.asname or "subprocess")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module == "subprocess":
            for alias in node.names:
                if alias.name == "run":
                    self.run_names.add(alias.asname or "run")
        self.generic_visit(node)

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    visit_FunctionDef = _visit_function
    visit_AsyncFunctionDef = _visit_function

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        is_run = False
        if isinstance(func, ast.Attribute) and func.attr == "run":
            is_run = (
                isinstance(func.value, ast.Name)
                and func.value.id in self.module_aliases
            )
        elif isinstance(func, ast.Name):
            is_run = func.id in self.run_names
        if is_run:
            call_site = "%s :: %s" % (
                ".".join(reversed(self.stack)) or "<module>",
                _normalized_target(node, self.consts),
            )
            self.sites.append((call_site, node.lineno))
        self.generic_visit(node)


def scan_sites(root: Path = ROOT) -> list[tuple[str, str, int]]:
    """Every ``subprocess.run`` call site under ``tests/`` — the completeness denominator."""
    files = sorted(
        path
        for path in (root / "tests").rglob("*.py")
        if "__pycache__" not in path.parts
    )
    sites: list[tuple[str, str, int]] = []
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        collector = _Collector(_const_map(tree))
        collector.visit(tree)
        rel = path.relative_to(root).as_posix()
        for call_site, lineno in collector.sites:
            sites.append((rel, call_site, lineno))
    return sites


# --------------------------------------------------------------------------- #
# The manifest (generated from the scan, completed by hand for the verdicts)
# --------------------------------------------------------------------------- #
def parse_manifest(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header_seen = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not header_seen:
            assert tuple(cells) == COLUMNS, (
                "the manifest header must be exactly %r, got %r" % (COLUMNS, tuple(cells))
            )
            header_seen = True
            continue
        if all(set(cell) <= {"-", ":"} and cell for cell in cells):
            continue
        assert len(cells) == len(COLUMNS), (
            "manifest row does not have %d cells: %r" % (len(COLUMNS), raw)
        )
        cells = [cell[1:-1] if len(cell) >= 2 and cell[0] == cell[-1] == "`" else cell
                 for cell in cells]
        rows.append(dict(zip(COLUMNS, cells)))
    assert header_seen, "the manifest carries no pipe table with the declared columns"
    return rows


def _manifest_rows() -> list[dict[str, str]]:
    assert MANIFEST.is_file(), (
        "the conversion manifest is missing: %s — generated by T045 from the AST census "
        "(C-006)" % MANIFEST.relative_to(ROOT)
    )
    return parse_manifest(MANIFEST.read_text(encoding="utf-8"))


def _rows_by_site(rows: list[dict[str, str]]) -> dict[tuple[str, str], list[dict[str, str]]]:
    by_site: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        by_site.setdefault((row["file"], row["call_site"]), []).append(row)
    return by_site


def classify(
    sites: list[tuple[str, str, int]], rows: list[dict[str, str]]
) -> list[str]:
    """The completeness/revert findings (C-001, C-006, C-007), as named strings."""
    findings: list[str] = []
    by_site = _rows_by_site(rows)
    scanned: dict[tuple[str, str], int] = {}
    for file, call_site, _lineno in sites:
        scanned[(file, call_site)] = scanned.get((file, call_site), 0) + 1
    for (file, call_site), count in sorted(scanned.items()):
        group = by_site.get((file, call_site), [])
        keep = sum(1 for row in group if row["verdict"] == "keep")
        convert = sum(1 for row in group if row["verdict"] == "convert")
        if keep == 0 and convert == 0:
            findings.append("unclassified call site: %s :: %s" % (file, call_site))
        elif count > keep and convert > 0:
            findings.append(
                "reverted conversion: %s :: %s is still a subprocess.run site but the "
                "manifest marks it convert (C-007)" % (file, call_site)
            )
        elif count > keep:
            findings.append("unclassified call site: %s :: %s" % (file, call_site))
    for (file, call_site), group in sorted(by_site.items()):
        keep = sum(1 for row in group if row["verdict"] == "keep")
        if keep > scanned.get((file, call_site), 0):
            findings.append(
                "stale keep row: %s :: %s has %d keep row(s) but %d discovered site(s)"
                % (file, call_site, keep, scanned.get((file, call_site), 0))
            )
    return findings


# --------------------------------------------------------------------------- #
# C-005 — the manifest table shape
# --------------------------------------------------------------------------- #
def test_c005_the_manifest_is_a_pipe_table_with_the_declared_columns():
    rows = _manifest_rows()
    assert rows, "the manifest carries no data rows"
    for row in rows:
        assert row["file"].startswith("tests/"), (
            "manifest row file must be repo-relative under tests/: %r" % row
        )
        assert (ROOT / row["file"]).is_file(), (
            "manifest row names a file that does not exist: %r" % row["file"]
        )


# --------------------------------------------------------------------------- #
# C-002 — the closed keep-class set and the convert marker
# --------------------------------------------------------------------------- #
def test_c002_keep_rows_use_the_closed_class_set_and_convert_rows_use_a_dash():
    offenders = []
    for row in _manifest_rows():
        if row["verdict"] == "keep":
            if row["boundary_class"] not in KEEP_CLASSES:
                offenders.append(
                    "%s :: %s keep class %r is outside the closed set (C-002)"
                    % (row["file"], row["call_site"], row["boundary_class"])
                )
        elif row["verdict"] == "convert":
            if row["boundary_class"] != CONVERT_CLASS:
                offenders.append(
                    "%s :: %s convert row must carry %r as its boundary_class"
                    % (row["file"], row["call_site"], CONVERT_CLASS)
                )
        else:
            offenders.append(
                "%s :: %s verdict %r is not convert|keep"
                % (row["file"], row["call_site"], row["verdict"])
            )
    assert not offenders, "\n".join(offenders)


# --------------------------------------------------------------------------- #
# C-003 / C-008 — reasons and the equivalence route
# --------------------------------------------------------------------------- #
def test_c003_c008_every_row_carries_a_reason_and_convert_names_its_route():
    offenders = []
    for row in _manifest_rows():
        reason = row["reason"].strip()
        if not reason:
            offenders.append("%s :: %s carries no reason" % (row["file"], row["call_site"]))
            continue
        if row["verdict"] == "convert":
            lowered = reason.lower()
            if "in-process" not in lowered or not (
                "main(" in reason or "clirunner" in lowered
            ):
                offenders.append(
                    "%s :: %s convert reason must name the in-process route "
                    "(main(argv)/CliRunner) (C-003): %r"
                    % (row["file"], row["call_site"], reason)
                )
    assert not offenders, "\n".join(offenders)


# --------------------------------------------------------------------------- #
# C-001 / C-004 — completeness over covered files, and the fixture-layer default
# --------------------------------------------------------------------------- #
def test_c001_every_covered_file_classifies_all_of_its_sites():
    """A file with at least one manifest row must classify every site it carries.

    This is the WP-7-scope half of C-001: the conversion groups plus the fixture layer
    are closed here, and drift inside a covered file reddens immediately. Files with no
    rows at all are named by the full-tree case below (T052 owner).
    """
    rows = _manifest_rows()
    covered = {row["file"] for row in rows}
    sites = scan_sites()
    in_scope = [site for site in sites if site[0] in covered]
    findings = classify(in_scope, rows)
    assert not findings, (
        "covered-file drift:\n%s" % "\n".join(findings)
    )


def test_c006_the_full_tree_scan_names_its_uncovered_files():
    """Full-tree completeness (C-001/C-006) — closed by T052 over the whole census.

    A site with no row, or a revert, is named, so no site can be silently forgotten.
    """
    findings = classify(scan_sites(), _manifest_rows())
    unclassified_files = sorted(
        {finding.split("unclassified call site: ")[1].split(" :: ")[0]
         for finding in findings
         if finding.startswith("unclassified call site: ")}
    )
    assert not findings, (
        "%d site(s) unclassified; %d file(s) still uncovered (T052 owner): %s"
        % (len(findings), len(unclassified_files), ", ".join(unclassified_files))
    )


def test_c004_fixture_layer_helpers_are_keep_with_the_global_state_class():
    """``tests/fixtures/client_project.py`` ``run_engine``/``run_script`` are keep rows."""
    rows = {
        (row["file"], row["call_site"]): row
        for row in _manifest_rows()
    }
    expected = {
        "tests/fixtures/client_project.py": (
            "run_engine :: <computed>",
            "run_script :: <computed>",
        ),
        "tests/fixtures/line_fixtures.py": (
            "run_engine :: <computed>",
        ),
    }
    offenders = []
    for file, call_sites in expected.items():
        for call_site in call_sites:
            row = rows.get((file, call_site))
            if row is None:
                offenders.append("missing fixture-layer row: %s :: %s" % (file, call_site))
                continue
            if row["verdict"] != "keep" or row["boundary_class"] != "global-state-unrecoverable":
                offenders.append(
                    "%s :: %s must be keep/global-state-unrecoverable, got %s/%s"
                    % (file, call_site, row["verdict"], row["boundary_class"])
                )
    assert not offenders, "\n".join(offenders)


# --------------------------------------------------------------------------- #
# C-007 — revert detection is exercised on a synthetic census
# --------------------------------------------------------------------------- #
def test_c007_a_reverted_conversion_turns_red_and_names_the_site():
    rows = [
        {
            "file": "tests/contract/test_demo.py",
            "call_site": "_run :: flow-class-check.py",
            "verdict": "convert",
            "boundary_class": CONVERT_CLASS,
            "reason": "in-process main(argv) with the same stdout assertions",
        }
    ]
    scanned_again = [("tests/contract/test_demo.py", "_run :: flow-class-check.py", 10)]
    findings = classify(scanned_again, rows)
    assert findings, "a reverted conversion MUST redden (C-007)"
    assert any(
        "reverted conversion" in finding
        and "tests/contract/test_demo.py" in finding
        and "_run :: flow-class-check.py" in finding
        for finding in findings
    ), findings

    converted = [("tests/contract/test_demo.py", "_run :: flow-class-check.py", 10)]
    keep_rows = [dict(rows[0], verdict="keep", boundary_class="global-state-unrecoverable")]
    assert not classify(converted, keep_rows), (
        "a keep row covers its still-present site; the revert signal must be specific"
    )


def test_c010_the_keep_side_sample_covers_the_named_boundary_kinds():
    classes = {row["boundary_class"] for row in _manifest_rows() if row["verdict"] == "keep"}
    missing = [kind for kind in NAMED_BOUNDARY_KINDS if kind not in classes]
    assert not missing, (
        "the keep-side sample must cover the named boundary kinds (C-010); missing: %s"
        % ", ".join(missing)
    )


# --------------------------------------------------------------------------- #
# C-008 — a converted row still carries the in-process route, not an import-only stub
# --------------------------------------------------------------------------- #
def _function_defs(tree: ast.Module) -> dict[str, ast.AST]:
    return {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _calls_route(node: ast.AST) -> bool:
    for sub in ast.walk(node):
        if not isinstance(sub, ast.Call):
            continue
        func = sub.func
        if isinstance(func, ast.Name) and func.id in (
            "run_engine_in_process",
            "run_specify_init",
            "run_specify_check",
        ):
            return True
        if isinstance(func, ast.Attribute) and func.attr == "invoke":
            return True
    return False


def test_c008_converted_rows_still_make_the_in_process_call():
    """A converted row must name a function that still calls the equivalence route.

    The canonical weakening (C-008) replaces the route with an import-only check
    (``import engine; assert engine.main is not None``). That rewrite removes the
    route call, so the row reddens and is named; the file must also keep at least
    one assertion so an empty shell cannot pass.
    """
    offenders = []
    cache: dict[str, tuple[ast.Module, dict[str, ast.AST]]] = {}
    for row in _manifest_rows():
        if row["verdict"] != "convert":
            continue
        file = row["file"]
        if file not in cache:
            tree = ast.parse((ROOT / file).read_text(encoding="utf-8"))
            cache[file] = (tree, _function_defs(tree))
        tree, defs = cache[file]
        name = row["call_site"].split(" :: ", 1)[0].rsplit(".", 1)[-1]
        func = defs.get(name)
        if func is None:
            offenders.append(
                "%s :: %s names no function %r (C-008)"
                % (file, row["call_site"], name)
            )
        elif not _calls_route(func):
            offenders.append(
                "%s :: %s no longer calls the in-process route "
                "(run_engine_in_process/CliRunner) — import-only weakening (C-008)"
                % (file, row["call_site"])
            )
        if not any(isinstance(node, ast.Assert) for node in ast.walk(tree)):
            offenders.append("%s carries no assertion at all (C-008)" % file)
    assert not offenders, "\n".join(offenders)
