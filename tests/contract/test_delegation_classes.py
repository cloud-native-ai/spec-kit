"""Contract tests for command → skill delegation classes (069b, T015).

Owns the assertions of
``.specify/specs/069b-isomorphism-migration-metrics/contracts/ledger-reconciler.md``
C-8…C-10 that ``tasks.md`` T015 names:

* C-8  ``--action delegation`` parses delegation edges out of the command
  templates with the declared grammar
  ``(?:\\.specify/)?skills/(?:external/|internal/)?<name>/SKILL.md`` → ``skill:<name>``,
  de-duplicates the same skill inside one template, and emits one record per edge
  ``{command, skill, command_class, skill_class, verdict, source_line}``. The
  verdict order is fixed — ``unknown-skill`` → ``neutral-exempt`` (a closed-list
  member is exempt *whatever* the two classes are) → ``same-class`` / ``mismatch``.
  A placeholder path (``skills/<name>/SKILL.md``) is not an edge and never a
  finding. ``commands_scanned`` is a top-level integer.
* C-9  the verification never reads a hand-maintained command→skill table: a
  repository file carrying ≥3 command/skill pairs outside the templates is
  ``delegation-hand-list``.
* C-10 the neutral exemption is taken from the owner's closed § 类中立清单, never
  from a copy inside the engine or the contract.

The whole-repository assertions compare the engine against an independent oracle
built here from the same two sources (templates + owner ledger). Falsification
fixtures live in ``tmp_path``: one skill is flipped to the opposite class (red),
a neutral edge is kept (still green). Red-first (Constitution IV): 069a's engine
has no ``delegation`` action yet, so every call reds as "action missing" — never
as an import or collection error. ``_run`` asserts the script path first.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"
OWNER_REL = Path("shared") / "definitions" / "flow-class-definitions.md"
COMMANDS_REL = Path("templates") / "commands"

EXECUTION = "execution"
EXPRESSION = "expression"

# Contract C-8: the declared grammar, with the name class the contract pins.
EDGE_RE = re.compile(
    r"(?:\.specify/)?skills/(?:external/|internal/)?([a-z0-9][a-z0-9-]*)/SKILL\.md"
)
EDGE_KEYS = ("command", "skill", "command_class", "skill_class", "verdict", "source_line")
VERDICTS = ("same-class", "neutral-exempt", "mismatch", "unknown-skill")

LEDGER_COLUMNS = ("unit_id", "flow_class", "basis", "neutral", "notes")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run(*args: str) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), (
        "flow-class engine missing: %s — expected from 069a. "
        "Red is the intended pre-implementation state for 069b T015."
        % ENGINE.relative_to(REPO_ROOT)
    )
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )


def _json(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), (
        "expected a JSON document on stdout, got empty output (stderr: %r)" % proc.stderr
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            "stdout is not JSON (%s); head=%r" % (exc, proc.stdout[:400])
        ) from exc


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _render_owner(
    rows: list[dict],
    neutral_rows: list[tuple[str, str, str]],
    *,
    version: str = "**台账版本**: 1（2026-10-25）",
) -> str:
    lines = [
        "# Flow Class Definitions (069b delegation fixture)",
        "",
        "fixture: not the repository owner.",
        "",
        "## 逐流程台账",
        "",
        version,
        "",
        "| " + " | ".join(LEDGER_COLUMNS) + " |",
        "| " + " | ".join("---" for _ in LEDGER_COLUMNS) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(c, "")) for c in LEDGER_COLUMNS) + " |")
    lines.extend(
        [
            "",
            "## 类中立清单",
            "",
            "| unit_id | category | rationale |",
            "| --- | --- | --- |",
        ]
    )
    for unit, category, rationale in neutral_rows:
        lines.append("| %s | %s | %s |" % (unit, category, rationale))
    return "\n".join(lines)


def _build_repo(
    root: Path,
    templates: dict[str, list[str]],
    command_classes: dict[str, str],
    skill_classes: dict[str, str],
    *,
    neutral_rows: list[tuple[str, str, str]] | None = None,
    owner_text: str | None = None,
) -> None:
    for stem, snippets in templates.items():
        body = ["# /speckit.%s" % stem, ""]
        body.extend(snippets)
        body.append("")
        _write(root / COMMANDS_REL / ("%s.md" % stem), "\n".join(body))
    for name in skill_classes:
        _write(
            root / "skills" / "internal" / name / "SKILL.md",
            "---\nname: %s\ndescription: fixture skill\n---\n" % name,
        )
    rows: list[dict] = []
    for stem, flow_class in command_classes.items():
        rows.append(
            {
                "unit_id": "/speckit.%s" % stem,
                "flow_class": flow_class,
                "basis": "behavior-oracle",
                "neutral": "",
                "notes": "",
            }
        )
    for name, flow_class in skill_classes.items():
        rows.append(
            {
                "unit_id": "skill:%s" % name,
                "flow_class": flow_class,
                "basis": "behavior-oracle",
                "neutral": "",
                "notes": "",
            }
        )
    _write(
        root / OWNER_REL,
        owner_text
        if owner_text is not None
        else _render_owner(rows, neutral_rows or []),
    )


def _delegation(root: Path):
    proc = _run("--action", "delegation", "--repo", str(root), "--format", "json")
    record = _json(proc) if proc.stdout.strip() else None
    return proc, record


def _edge_records(record: dict) -> list[dict]:
    """Collect every emitted edge record, whichever array carries it.

    Contract C-8 pins the *record* shape, not the container name, so the
    assertion walks the payload instead of guessing a key.
    """
    found: list[dict] = []

    def walk(node):
        if isinstance(node, dict):
            if all(key in node for key in EDGE_KEYS):
                found.append(node)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(record)
    return found


def _kinds(record: dict) -> list[str]:
    return [finding.get("kind") for finding in record.get("findings", [])]


# --------------------------------------------------------------------------- #
# the owner / template oracles
# --------------------------------------------------------------------------- #
def _owner_tables() -> tuple[dict[str, str], set[str]]:
    text = (REPO_ROOT / OWNER_REL).read_text(encoding="utf-8")
    lines = text.splitlines()
    ledger = {}
    for row in _table_rows(lines, "逐流程台账"):
        ledger[row["unit_id"]] = row["flow_class"]
    neutral = {row["unit_id"] for row in _table_rows(lines, "类中立清单")}
    return ledger, neutral


def _table_rows(lines: list[str], keyword: str) -> list[dict]:
    body: list[str] = []
    inside = False
    for line in lines:
        if line.startswith("## "):
            if inside:
                break
            inside = keyword in line
            continue
        if inside:
            body.append(line)
    header = None
    rows: list[dict] = []
    for line in body:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def _template_edges(root: Path) -> list[tuple[str, str, int]]:
    """Independent oracle for C-8: (command, skill, source_line) per template."""
    edges: list[tuple[str, str, int]] = []
    for path in sorted((root / COMMANDS_REL).glob("*.md")):
        command = "/speckit.%s" % path.stem
        seen: set[str] = set()
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in EDGE_RE.finditer(line):
                name = match.group(1)
                if name in seen:
                    continue
                seen.add(name)
                edges.append((command, "skill:%s" % name, number))
    return edges


def _expected_verdict(
    ledger: dict[str, str],
    command_class: str,
    skill: str,
    skill_class: str,
    neutral: set[str],
) -> str:
    if skill not in ledger:
        return "unknown-skill"
    if skill in neutral:
        return "neutral-exempt"
    return "same-class" if command_class == skill_class else "mismatch"


# --------------------------------------------------------------------------- #
# whole repository: 27 templates, every edge same-class or neutral-exempt
# --------------------------------------------------------------------------- #
def test_every_template_edge_is_same_class_or_neutral_exempt():
    ledger, neutral = _owner_tables()
    assert ledger, "the owner ledger must parse for this test to mean anything"

    proc, record = _delegation(REPO_ROOT)
    assert proc.returncode == 0, (
        "delegation on the real tree must be green; findings=%r stderr=%r"
        % (None if record is None else record.get("findings"), proc.stderr)
    )
    assert record is not None
    assert record.get("findings") == [], (
        "the real delegation graph must carry zero findings; got %r"
        % record.get("findings")
    )
    assert record.get("commands_scanned") == 27, (
        "commands_scanned MUST be the scanned template count (27); got %r"
        % record.get("commands_scanned")
    )

    edges = _edge_records(record)
    expected = _template_edges(REPO_ROOT)
    assert len(edges) == len(expected), (
        "engine parsed %d edge(s), the C-8 oracle parsed %d: engine=%r oracle=%r"
        % (len(edges), len(expected), sorted(map(str, edges)), expected)
    )

    observed = {
        (edge["command"], edge["skill"], edge["verdict"], edge["command_class"], edge["skill_class"])
        for edge in edges
    }
    oracle = set()
    for command, skill, _line in expected:
        command_class = ledger[command]
        skill_class = ledger[skill]
        oracle.add(
            (
                command,
                skill,
                _expected_verdict(ledger, command_class, skill, skill_class, neutral),
                command_class,
                skill_class,
            )
        )
    assert observed == oracle, "engine edges differ from the C-8 oracle"

    # `source_line` is the line the edge was read from — whichever occurrence the
    # engine cites, that line must really name the skill.
    for edge in edges:
        template = REPO_ROOT / COMMANDS_REL / (
            "%s.md" % edge["command"].removeprefix("/speckit.")
        )
        lines = template.read_text(encoding="utf-8").splitlines()
        line_no = edge["source_line"]
        assert isinstance(line_no, int) and 1 <= line_no <= len(lines), (
            "source_line %r is not a line of %s (C-8)" % (line_no, template.name)
        )
        names = {match.group(1) for match in EDGE_RE.finditer(lines[line_no - 1])}
        assert edge["skill"].removeprefix("skill:") in names, (
            "source_line %d of %s does not name %r (C-8)"
            % (line_no, template.name, edge["skill"])
        )

    assert all(edge["verdict"] in VERDICTS for edge in edges)
    assert not any(edge["verdict"] == "mismatch" for edge in edges)
    assert not any(edge["verdict"] == "unknown-skill" for edge in edges)

    # The exemption must be real, not vacuous: at least one neutral edge crosses
    # the two classes and is nevertheless exempt (C-8).
    crossing = [
        edge
        for edge in edges
        if edge["verdict"] == "neutral-exempt"
        and edge["command_class"] != edge["skill_class"]
    ]
    assert crossing, (
        "expected at least one neutral-exempt edge whose two sides differ — "
        "otherwise the exemption order is untested"
    )


def test_placeholder_skill_paths_are_not_edges():
    owner_text = (REPO_ROOT / OWNER_REL).read_text(encoding="utf-8")
    commands = sorted((REPO_ROOT / COMMANDS_REL).glob("*.md"))
    assert commands, "no command templates found"
    text = "\n".join(path.read_text(encoding="utf-8") for path in commands)
    # A literal placeholder path must never become an edge (C-8).
    assert "skills/<name>/SKILL.md" in text, (
        "this assertion anchors on the real placeholder; it is expected in templates/commands/skills.md"
    )
    assert not EDGE_RE.search("skills/<name>/SKILL.md")


# --------------------------------------------------------------------------- #
# falsification: one flipped skill turns the action red
# --------------------------------------------------------------------------- #
BASE_TEMPLATES = {
    "alpha": ["Delegates to `.specify/skills/internal/skill-alpha/SKILL.md`."],
    "beta": ["Delegates to `skills/internal/skill-beta/SKILL.md`."],
}
BASE_COMMANDS = {"alpha": EXECUTION, "beta": EXPRESSION}
BASE_SKILLS = {"skill-alpha": EXECUTION, "skill-beta": EXECUTION}


def test_flipped_skill_reports_delegation_mismatch(tmp_path):
    _build_repo(tmp_path, BASE_TEMPLATES, BASE_COMMANDS, BASE_SKILLS)
    proc, record = _delegation(tmp_path)
    assert proc.returncode == 1, (
        "a command delegating to the opposite class must exit 1; findings=%r"
        % (None if record is None else record.get("findings"))
    )
    assert record is not None
    matches = [
        finding
        for finding in record.get("findings", [])
        if finding.get("kind") == "delegation-mismatch"
    ]
    assert matches, (
        "expected `delegation-mismatch` for beta → skill-beta; got %r" % _kinds(record)
    )
    assert any(finding.get("unit_id") in ("/speckit.beta", "skill:skill-beta") for finding in matches)

    edges = {(edge["command"], edge["skill"]): edge for edge in _edge_records(record)}
    assert edges[("/speckit.alpha", "skill:skill-alpha")]["verdict"] == "same-class"
    assert edges[("/speckit.beta", "skill:skill-beta")]["verdict"] == "mismatch"


def test_aligned_skill_is_green(tmp_path):
    skills = {"skill-alpha": EXECUTION, "skill-beta": EXPRESSION}
    _build_repo(tmp_path, BASE_TEMPLATES, BASE_COMMANDS, skills)
    proc, record = _delegation(tmp_path)
    assert proc.returncode == 0, (
        "aligned classes must reconcile green; findings=%r stderr=%r"
        % (None if record is None else record.get("findings"), proc.stderr)
    )
    assert record is not None and record.get("findings") == []
    assert {edge["verdict"] for edge in _edge_records(record)} == {"same-class"}


def test_neutral_edge_stays_green_across_classes(tmp_path):
    neutral = [("skill:skill-beta", "memory", "fixture neutral carrier")]
    _build_repo(
        tmp_path,
        BASE_TEMPLATES,
        BASE_COMMANDS,
        BASE_SKILLS,
        neutral_rows=neutral,
    )
    proc, record = _delegation(tmp_path)
    assert proc.returncode == 0, (
        "a class-neutral edge must stay green even across classes (C-8); findings=%r"
        % (None if record is None else record.get("findings"))
    )
    assert record is not None
    edges = {(edge["command"], edge["skill"]): edge for edge in _edge_records(record)}
    assert edges[("/speckit.beta", "skill:skill-beta")]["verdict"] == "neutral-exempt", (
        "a closed-list member is neutral-exempt whatever the two classes are (C-8)"
    )


def test_unknown_skill_reports_delegation_unknown_skill(tmp_path):
    templates = {"alpha": ["Delegates to `skills/internal/ghost-skill/SKILL.md`."]}
    _build_repo(tmp_path, templates, {"alpha": EXECUTION}, {"skill-alpha": EXECUTION})
    proc, record = _delegation(tmp_path)
    assert proc.returncode == 1
    assert record is not None
    assert "delegation-unknown-skill" in _kinds(record), (
        "a skill absent from the ledger must be `delegation-unknown-skill` (C-8); got %r"
        % _kinds(record)
    )
    edges = _edge_records(record)
    assert [edge["verdict"] for edge in edges] == ["unknown-skill"], (
        "unknown-skill wins the verdict order (C-8); got %r" % edges
    )


def test_unknown_skill_outranks_the_neutral_exemption(tmp_path):
    templates = {"alpha": ["Delegates to `skills/internal/ghost-skill/SKILL.md`."]}
    neutral = [("skill:ghost-skill", "memory", "listed but absent from the ledger")]
    _build_repo(
        tmp_path,
        templates,
        {"alpha": EXECUTION},
        {"skill-alpha": EXECUTION},
        neutral_rows=neutral,
    )
    proc, record = _delegation(tmp_path)
    assert record is not None
    edges = _edge_records(record)
    assert edges and edges[0]["verdict"] == "unknown-skill", (
        "the fixed order is unknown-skill → neutral-exempt (C-8); got %r" % edges
    )


def test_hand_written_delegation_table_is_rejected(tmp_path):
    _build_repo(
        tmp_path,
        BASE_TEMPLATES,
        BASE_COMMANDS,
        {"skill-alpha": EXECUTION, "skill-beta": EXPRESSION},
    )
    _write(
        tmp_path / "shared" / "definitions" / "delegation-handbook.md",
        "\n".join(
            [
                "# Hand-written delegation table (fixture)",
                "",
                "| command | skill |",
                "| --- | --- |",
                "| /speckit.alpha | skill:skill-alpha |",
                "| /speckit.beta | skill:skill-beta |",
                "| /speckit.alpha | skill:skill-beta |",
                "",
            ]
        ),
    )
    proc, record = _delegation(tmp_path)
    assert proc.returncode == 1
    assert record is not None
    assert "delegation-hand-list" in _kinds(record), (
        "a ≥3-row command→skill table outside the templates must be "
        "`delegation-hand-list` (C-9); got %r" % _kinds(record)
    )


def test_same_skill_twice_in_one_template_is_one_edge(tmp_path):
    templates = {
        "alpha": [
            "First: `.specify/skills/internal/skill-alpha/SKILL.md`.",
            "Again: `skills/internal/skill-alpha/SKILL.md`.",
            "Layered: `skills/external/skill-alpha/SKILL.md`.",
        ]
    }
    _build_repo(tmp_path, templates, {"alpha": EXECUTION}, {"skill-alpha": EXECUTION})
    proc, record = _delegation(tmp_path)
    assert proc.returncode == 0, (
        "duplicates inside one template are de-duplicated, not a finding; stderr=%r"
        % proc.stderr
    )
    assert record is not None
    assert len(_edge_records(record)) == 1, (
        "the same skill named three times is one edge (C-8); got %r"
        % _edge_records(record)
    )


def test_placeholder_path_produces_no_edge_and_no_finding(tmp_path):
    templates = {
        "skills": [
            "Layout: `skills/<name>/SKILL.md`.",
            "Also: `skills/external/<name>/SKILL.md`.",
        ]
    }
    _build_repo(tmp_path, templates, {"skills": EXECUTION}, {"skill-alpha": EXECUTION})
    proc, record = _delegation(tmp_path)
    assert proc.returncode == 0, (
        "a placeholder path is not an edge and not a finding (C-8); findings=%r"
        % (None if record is None else record.get("findings"))
    )
    assert record is not None and record.get("findings") == []
    assert _edge_records(record) == []


def test_delegation_is_read_only(tmp_path):
    import hashlib

    _build_repo(tmp_path, BASE_TEMPLATES, BASE_COMMANDS, BASE_SKILLS)
    before = {
        path.relative_to(tmp_path).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(tmp_path.rglob("*"))
        if path.is_file()
    }
    _delegation(tmp_path)
    after = {
        path.relative_to(tmp_path).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(tmp_path.rglob("*"))
        if path.is_file()
    }
    assert before == after, "delegation MUST NOT write, cache or create files (C-15)"


def test_delegation_on_a_payload_root_is_framework_source_required(tmp_path):
    payload = tmp_path / "project"
    _write(
        payload / ".specify" / OWNER_REL,
        _render_owner(
            [
                {
                    "unit_id": "/speckit.alpha",
                    "flow_class": EXECUTION,
                    "basis": "behavior-oracle",
                    "neutral": "",
                    "notes": "",
                }
            ],
            [],
        ),
    )
    proc, record = _delegation(payload)
    assert proc.returncode == 2, "a payload root MUST exit 2 (C-14)"
    assert record is not None
    assert record.get("findings") == []
    assert (record.get("error") or {}).get("label") == "framework-source-required", (
        "expected framework-source-required; got %r" % (record.get("error"),)
    )
