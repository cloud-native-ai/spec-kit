"""Contract tests for the expression-gate wiring (069a, T015 — A1…A7).

Owns the wiring assertions of
``.specify/specs/069a-flow-classification-docs-gates/contracts/flow-class-ledger.md``
C-15 and ``contracts/expression-gate-operators.md`` C-12/C-14/C-15 that
``tasks.md`` T015 names:

* **A1** W1 ``templates/commands/docs.md`` — a wiring subsection inside
  ``## Outline`` (after the heading, before ``## Wrap-up``) carrying the lookup
  call, the unit id, both owner paths, and the checker;
* **A2** W2 ``templates/commands/humanize.md`` — a wiring subsection carrying
  **only** the two owner paths: no lookup, no script call at all; the template
  stays Simple (one ``SKILL.md`` mention, no ``## Wrap-up``, <= 120 non-table
  lines);
* **A3** W3 ``skills/external/create-docs/SKILL.md`` — gate-owner pointer plus the
  checker on the R6 verify path;
* **A4** W4 ``skills/external/humanize/SKILL.md`` — the flow's only lookup
  (``--unit-id "/speckit.humanize"``) placed in Stage 6, with the gate-owner
  pointer, the 062 fidelity section, and ``diff_protected.py`` kept;
* **A5** wiring text hygiene — after removing the owner paths no independent
  ``expression`` / ``execution`` word and no class-attribution assertion remains;
  no class-key assignment form and no ledger-style row anywhere;
* **A6** closed wiring — the other 25 templates and 49 skills reference neither
  engine nor the gate owner;
* **A7** the eight generated command copies carry the same wiring (docs: lookup +
  owner pointer; humanize: the two owner pointers and no engine call);
* **A8** the wired checker command is **executed**, not grepped: the exact string
  the docs template names is parsed, its placeholders are filled, and it runs in
  both distribution shapes (delivered ``.specify/…`` copy and source copy) — a
  scope-less call (exit 2) or an unexecutable wiring turns this leg red.

A further leg pins the frozen ``requirements.md`` hashes of 062 / 067 / 068
(SC-008). Red-first (Constitution IV): the wiring is deliberately absent until
T022–T025, so the assertions fail with an explicit "wiring subsection missing"
message rather than an index error.
"""
from __future__ import annotations

import hashlib
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DOCS_TEMPLATE = REPO_ROOT / "templates" / "commands" / "docs.md"
HUMANIZE_TEMPLATE = REPO_ROOT / "templates" / "commands" / "humanize.md"
CREATE_DOCS_SKILL = REPO_ROOT / "skills" / "external" / "create-docs" / "SKILL.md"
HUMANIZE_SKILL = REPO_ROOT / "skills" / "external" / "humanize" / "SKILL.md"
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
SKILLS_DIR = REPO_ROOT / "skills"

CLASS_OWNER = "shared/definitions/flow-class-definitions.md"
GATE_OWNER = "shared/workflow/expression-gates.md"
OWNER_PATHS = (CLASS_OWNER, GATE_OWNER)
ENGINE_TOKENS = (
    "flow-class-check.py",
    "expression-gates.md",
    "doc-consistency-check.py",
)

COPY_LAYOUTS = (
    (".claude", "commands", "speckit.{stem}.md"),
    (".github", "prompts", "speckit.{stem}.prompt.md"),
    (".opencode", "command", "speckit.{stem}.md"),
    (".qoder", "commands", "speckit.{stem}.md"),
)

# SC-008 frozen hashes (notes/pre-change-measurements.md § 5).
FROZEN_SPEC_HASHES = {
    ".specify/specs/062-humanize-command/requirements.md":
        "987b24ea1f98abb2a01d14779814eab28416f4ad1cbd81a36d51efb72d5f9da0",
    ".specify/specs/067-loop-efficiency-hardening/requirements.md":
        "29e26b701ebef9d80782b9a215ef97759290a384d898cb3320cfedde161fa0cd",
    ".specify/specs/068-exec-quant-feedback-channel/requirements.md":
        "ec20d5e28bd0eb5e2afdbd851cb753ef6e1c37a1c24e66b196f9305f18b45af7",
}

# requirements.md § Shared Strings (pinned copies).
STR_003 = "flow_class"
PATH_RE = re.compile(r"(?:shared|scripts|skills|templates|tests|docs)/[A-Za-z0-9._/-]+")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _read(path: Path) -> str:
    assert path.is_file(), "wiring target missing: %s" % path.relative_to(REPO_ROOT)
    return path.read_text(encoding="utf-8")


def _lines_with_heading(text: str, prefix: str) -> list[tuple[int, str]]:
    return [
        (index, line)
        for index, line in enumerate(text.splitlines())
        if line.startswith(prefix)
    ]


def _outline_wiring_section(text: str, path: Path) -> tuple[str, str]:
    """Return ``(heading, body)`` of the wiring subsection inside ``## Outline``.

    The wiring subsection is the ``###`` block under ``## Outline`` whose body
    mentions an owner path or an engine. Content-anchored on purpose: the heading
    wording is the implementer's to choose, the location is not.
    """
    lines = text.splitlines()
    outline_start = None
    outline_end = len(lines)
    for index, line in enumerate(lines):
        if line.strip() == "## Outline":
            outline_start = index
            continue
        if outline_start is not None and line.startswith("## ") and index > outline_start:
            outline_end = index
            break
    assert outline_start is not None, "%s lacks a `## Outline` section" % path.name
    starts = [
        index
        for index, line in enumerate(lines[outline_start:outline_end], outline_start)
        if line.startswith("### ")
    ]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else outline_end
        body = "\n".join(lines[start:end])
        if any(token in body for token in (CLASS_OWNER, GATE_OWNER, "flow-class-check.py",
                                           "doc-consistency-check.py")):
            return lines[start], body
    raise AssertionError(
        "wiring subsection missing in %s — expected a `###` block under `## Outline` "
        "naming %s or the engines (T022/T025, 069a). Red is the pre-wiring state."
        % (path.name, GATE_OWNER)
    )


def _token_sections(text: str, token: str) -> list[tuple[str, str]]:
    """Return every ``###``-or-under block whose body mentions *token*."""
    lines = text.splitlines()
    headings = [
        (index, line) for index, line in enumerate(lines) if re.match(r"^#{2,3} ", line)
    ]
    found = []
    for position, (start, heading) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        body = "\n".join(lines[start:end])
        if token in body:
            found.append((heading, body))
    return found


def _wiring_texts() -> list[tuple[str, str]]:
    """Every wiring block across the four designated files (A5's subject)."""
    blocks: list[tuple[str, str]] = []
    for path in (DOCS_TEMPLATE, HUMANIZE_TEMPLATE):
        heading, body = _outline_wiring_section(_read(path), path)
        blocks.append(("%s %s" % (path.name, heading), body))
    for path in (CREATE_DOCS_SKILL, HUMANIZE_SKILL):
        text = _read(path)
        for heading, body in _token_sections(text, GATE_OWNER):
            blocks.append(("%s %s" % (path.name, heading), body))
        for heading, body in _token_sections(text, "flow-class-check.py"):
            entry = ("%s %s" % (path.name, heading), body)
            if entry not in blocks:
                blocks.append(entry)
    return blocks


def _strip_paths(text: str) -> str:
    return PATH_RE.sub("<path>", text)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --------------------------------------------------------------------------- #
# A1 — W1: docs command template
# --------------------------------------------------------------------------- #
def test_a1_docs_template_wiring_subsection():
    text = _read(DOCS_TEMPLATE)
    heading, body = _outline_wiring_section(text, DOCS_TEMPLATE)
    assert "flow-class-check.py" in body, "W1 must call flow-class-check.py"
    assert "--action lookup" in body, "W1 must name the lookup action"
    assert '"/speckit.docs"' in body, "W1 must pass the documented unit id"
    for owner in OWNER_PATHS:
        assert owner in body, "W1 must point at %s" % owner
    assert "doc-consistency-check.py" in body, "W1 must run the doc-consistency checker"
    lines = text.splitlines()
    outline = lines.index("## Outline")
    wrap = next(i for i, line in enumerate(lines) if line.startswith("## Wrap-up"))
    position = lines.index(heading)
    assert outline < position < wrap, (
        "the W1 wiring subsection must sit inside `## Outline` (before `## Wrap-up`)"
    )


def test_a1_docs_template_keeps_its_top_level_sections():
    text = _read(DOCS_TEMPLATE)
    tops = [line for line in text.splitlines() if line.startswith("## ")]
    assert tops == ["## User Input", "## Glossary", "## Outline", "## Wrap-up", "## Handoffs"], (
        "the docs template's top-level section sequence must not change: %r" % tops
    )


# --------------------------------------------------------------------------- #
# A2 — W2: humanize command template stays Simple
# --------------------------------------------------------------------------- #
def test_a2_humanize_template_wiring_is_pointers_only():
    text = _read(HUMANIZE_TEMPLATE)
    heading, body = _outline_wiring_section(text, HUMANIZE_TEMPLATE)
    for owner in OWNER_PATHS:
        assert owner in body, "W2 must point at %s" % owner
    for forbidden in ("flow-class-check.py", "--action lookup", "--unit-id",
                      "doc-consistency-check.py", "feedback-utils.py", "probe-utils.py"):
        assert forbidden not in body, (
            "the W2 subsection must not carry %r — the humanize command keeps zero script calls"
            % forbidden
        )
    paths = {token.rstrip(".,;:，。；：)）】]") for token in PATH_RE.findall(body)}
    assert paths == set(OWNER_PATHS), (
        "the W2 subsection must name only the two owner paths, got %r" % sorted(paths)
    )


def test_a2_humanize_template_stays_simple():
    text = _read(HUMANIZE_TEMPLATE)
    assert text.count("SKILL.md") == 1, "the humanize template must name exactly one skill"
    assert "## Wrap-up" not in text, "the humanize template must stay Simple (no ## Wrap-up)"
    non_table = [line for line in text.splitlines() if not line.startswith("|")]
    assert len(non_table) <= 120, (
        "the humanize template must stay thin: %d non-table lines > 120" % len(non_table)
    )


# --------------------------------------------------------------------------- #
# A3 — W3: create-docs skill
# --------------------------------------------------------------------------- #
def test_a3_create_docs_skill_wires_owner_and_checker():
    text = _read(CREATE_DOCS_SKILL)
    assert GATE_OWNER in text, "W3 must point at the gate owner"
    assert CLASS_OWNER in text, "W3 must point at the classification owner"
    assert "doc-consistency-check.py" in text, "W3 must run the doc-consistency checker"
    r6_sections = [
        (heading, body)
        for heading, body in _token_sections(text, "doc-consistency-check.py")
    ]
    assert r6_sections, "the checker mention must live in a section, not loose in the file"
    assert any(re.search(r"R6", heading + body) for heading, body in r6_sections), (
        "W3 must wire the checker on the R6 verify path"
    )


# --------------------------------------------------------------------------- #
# A4 — W4: humanize skill
# --------------------------------------------------------------------------- #
def test_a4_humanize_skill_owns_the_single_lookup():
    text = _read(HUMANIZE_SKILL)
    assert "flow-class-check.py" in text, "W4 must call flow-class-check.py"
    assert "--action lookup" in text, "W4 must name the lookup action"
    assert '"/speckit.humanize"' in text, "W4 must pass the humanize unit id"
    assert GATE_OWNER in text, "W4 must point at the gate owner"
    assert CLASS_OWNER in text, "W4 must point at the classification owner"


def test_a4_humanize_skill_keeps_stage6_and_fidelity():
    text = _read(HUMANIZE_SKILL)
    assert "Stage 6 — 保真自检" in text, "the 062 fidelity stage heading must survive"
    assert "diff_protected.py" in text, "the 062 fidelity engine reference must survive"
    lines = text.splitlines()
    stage6 = next(
        i for i, line in enumerate(lines) if line.startswith("### Stage 6 — 保真自检")
    )
    stage7 = next(
        i for i, line in enumerate(lines) if line.startswith("### Stage 7 ")
    )
    lookups = [i for i, line in enumerate(lines) if "flow-class-check.py" in line]
    assert lookups, "the humanize skill must carry the lookup"
    assert any(stage6 < index < stage7 for index in lookups), (
        "the lookup must land in Stage 6 (before the fidelity self-check), got lines %r" % lookups
    )


# --------------------------------------------------------------------------- #
# A5 — wiring text hygiene
# --------------------------------------------------------------------------- #
def test_a5_wiring_text_has_no_class_words_or_attribution():
    for name, body in _wiring_texts():
        stripped = _strip_paths(body)
        for word in ("expression", "execution"):
            assert not re.search(r"\b%s\b" % word, stripped), (
                "%s carries an independent %r word after the owner paths are stripped"
                % (name, word)
            )
        for phrase in ("属表达类", "属于表达类", "是表达类", "归为表达类", "表达类流程"):
            assert phrase not in body, "%s asserts a class attribution (%r)" % (name, phrase)


def test_a5_no_class_key_assignment_or_ledger_row():
    targets = [
        DOCS_TEMPLATE,
        HUMANIZE_TEMPLATE,
        CREATE_DOCS_SKILL,
        HUMANIZE_SKILL,
    ]
    assign = re.compile(r"""%s["']?\s*[:=]\s*["']?(?:execution|expression)\b""" % STR_003)
    ledger_row = re.compile(
        r"^\s*\|\s*`?(?:/speckit\.[a-z0-9-]+|skill:[a-z0-9-]+)`?\s*\|\s*"
        r"(?:execution|expression)\s*\|"
    )
    for path in targets:
        text = _read(path)
        assert not assign.search(text), "%s assigns the class key" % path.name
        for line in text.splitlines():
            assert not ledger_row.match(line), (
                "%s carries a ledger-style unit/class row: %r" % (path.name, line)
            )


# --------------------------------------------------------------------------- #
# A6 — closed wiring set
# --------------------------------------------------------------------------- #
def test_a6_wiring_set_is_closed():
    offenders: list[str] = []
    for path in sorted(COMMANDS_DIR.glob("*.md")):
        if path.name in ("docs.md", "humanize.md"):
            continue
        text = path.read_text(encoding="utf-8")
        for token in ENGINE_TOKENS:
            if token in text:
                offenders.append("%s → %s" % (path.relative_to(REPO_ROOT), token))
    for skill_file in sorted(SKILLS_DIR.glob("external/*/SKILL.md")) + sorted(
        SKILLS_DIR.glob("internal/*/SKILL.md")
    ):
        if skill_file in (CREATE_DOCS_SKILL, HUMANIZE_SKILL):
            continue
        text = skill_file.read_text(encoding="utf-8")
        for token in ENGINE_TOKENS:
            if token in text:
                offenders.append("%s → %s" % (skill_file.relative_to(REPO_ROOT), token))
    assert not offenders, "wiring is closed to W1…W4; extra references found:\n- " + "\n- ".join(
        offenders
    )


def test_a6_wiring_inventory_matches_the_frozen_denominator():
    templates = sorted(COMMANDS_DIR.glob("*.md"))
    skills = sorted(SKILLS_DIR.glob("external/*/SKILL.md")) + sorted(
        SKILLS_DIR.glob("internal/*/SKILL.md")
    )
    assert len(templates) == 27, "template inventory drifted: %d (expected 27)" % len(templates)
    assert len(skills) == 51, "skill inventory drifted: %d (expected 51)" % len(skills)


# --------------------------------------------------------------------------- #
# A7 — generated command copies
# --------------------------------------------------------------------------- #
def _copies(stem: str) -> list[Path]:
    return [
        REPO_ROOT / folder / sub / pattern.format(stem=stem)
        for folder, sub, pattern in COPY_LAYOUTS
    ]


def test_a7_docs_copies_carry_lookup_and_owner_pointer():
    for path in _copies("docs"):
        assert path.is_file(), "generated command copy missing: %s" % path.relative_to(REPO_ROOT)
        text = path.read_text(encoding="utf-8")
        assert "flow-class-check.py" in text, "%s lacks the lookup call" % path.name
        assert "--action lookup" in text, "%s lacks the lookup action" % path.name
        assert GATE_OWNER in text, "%s lacks the gate-owner pointer" % path.name


def test_a7_humanize_copies_carry_pointers_only():
    for path in _copies("humanize"):
        assert path.is_file(), "generated command copy missing: %s" % path.relative_to(REPO_ROOT)
        text = path.read_text(encoding="utf-8")
        for owner in OWNER_PATHS:
            assert owner in text, "%s lacks the owner pointer %s" % (path.name, owner)
        assert "flow-class-check.py" not in text, (
            "%s must not call the engine (Simple command)" % path.name
        )


# --------------------------------------------------------------------------- #
# A8 — execute the exact command the wiring names
# --------------------------------------------------------------------------- #
CHECKER_INVOCATION_RE = re.compile(
    r"python3\s+(?P<tail>\S*scripts/python/doc-consistency-check\.py[^\n`]*)"
)
PATH_PLACEHOLDER_RE = re.compile(r"--path\s+<[^>\s]+>")
SPEC_PLACEHOLDER_RE = re.compile(r"\[--spec-dir\s+<[^>\s]+>\]")
WIRED_FIXTURE_DOC = """# Wired gate fixture

**Readers**: 迁移评审者，需要在合并前判断这份文档是否可用。
**Reading scenario**: 合并前核对读者声明与事实标注。

该切片把两个引擎放在框架源里（证据：实测，as-of {as_of}，source: `python3 scripts/python/flow-class-check.py --action check` exit 0）。
"""


def _wired_checker_command() -> str:
    """The literal invocation the docs template tells the operator to run."""
    heading, body = _outline_wiring_section(_read(DOCS_TEMPLATE), DOCS_TEMPLATE)
    match = CHECKER_INVOCATION_RE.search(body)
    assert match, (
        "the W1 wiring block (%r) names no `python3 …/doc-consistency-check.py` "
        "invocation; A8 has nothing to execute" % heading
    )
    return match.group(0)


def _wired_argv(command: str, doc: Path, spec: Path) -> list[str]:
    """Fill the template's placeholders and split the result into argv."""
    tail, path_hits = PATH_PLACEHOLDER_RE.subn("--path %s" % doc, command, count=1)
    assert path_hits == 1, (
        "the wired invocation must name `--path <每个受触文档>` — the checker rejects "
        "a scope-less run with exit 2; got %r" % command
    )
    tail, spec_hits = SPEC_PLACEHOLDER_RE.subn("--spec-dir %s" % spec, tail, count=1)
    assert spec_hits == 1, (
        "the wired invocation must offer `[--spec-dir <spec-dir>]` for the spec side; "
        "got %r" % command
    )
    assert "--strict" in tail, (
        "the wired invocation must carry --strict so a not-evaluated blocking face "
        "cannot exit 0; got %r" % command
    )
    argv = shlex.split(tail[len("python3 "):])
    # The wiring keeps the human-readable default; the harness appends only the
    # payload-shape flag so the same run can be asserted field by field.
    if "--format" not in argv:
        argv += ["--format", "json"]
    return argv


def _wired_fixture(root: Path) -> tuple[Path, Path]:
    """A git-backed clean spec + document, committed with a matching as-of."""
    repo = root / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=str(repo), check=True)
    spec = repo / "specs" / "001-wired"
    spec.mkdir(parents=True)
    (spec / "requirements.md").write_text(
        "# Requirements\n\n"
        "- **FR-001**: first requirement.\n"
        "- **SC-001**: first criterion.\n",
        encoding="utf-8",
    )
    (spec / "plan.md").write_text("# Plan\n\nNo count claim here.\n", encoding="utf-8")
    (spec / "tasks.md").write_text(
        "# Tasks\n\n- [ ] T001 first task\n", encoding="utf-8"
    )
    doc = repo / "docs" / "note.md"
    doc.parent.mkdir(parents=True)
    doc.write_text(WIRED_FIXTURE_DOC.format(as_of="2000-01-01"), encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=str(repo), check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "fixture"],
        cwd=str(repo),
        check=True,
    )
    commit_date = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", "docs/note.md"],
        cwd=str(repo), check=True, capture_output=True, text=True,
    ).stdout.strip()
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", commit_date), (
        "fixture precondition: the document must have a commit date, got %r" % commit_date
    )
    doc.write_text(WIRED_FIXTURE_DOC.format(as_of=commit_date), encoding="utf-8")
    return doc, spec


def _run_wired(argv: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *argv],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )


def _wired_shapes(argv: list[str]) -> dict[str, list[str]]:
    """The delivered (mirror) invocation and the same command from the source tree."""
    assert argv and argv[0].endswith("doc-consistency-check.py"), argv
    return {
        "delivered": list(argv),
        "source": ["scripts/python/doc-consistency-check.py", *argv[1:]],
    }


def test_a8_the_wired_command_executes_in_both_shapes(tmp_path):
    """Parse → execute: the exact wired command must run, not merely be mentioned."""
    command = _wired_checker_command()
    doc, spec = _wired_fixture(tmp_path)
    shapes = _wired_shapes(_wired_argv(command, doc, spec))
    for shape, argv in shapes.items():
        proc = _run_wired(argv)
        assert proc.returncode in (0, 1), (
            "%s shape: the wired command must produce a verdict, not an input error; "
            "exit=%d stdout=%r stderr=%r"
            % (shape, proc.returncode, proc.stdout[:400], proc.stderr)
        )
        payload = json.loads(proc.stdout)
        assert payload["action"] == "verify", payload
        assert payload["scope"]["files_scanned"] >= 1, payload["scope"]
        assert proc.returncode == 0, (
            "%s shape: a clean, fully evaluated fixture must pass; findings=%r "
            "degradations=%r" % (shape, payload["findings"], payload["degradations"])
        )
        assert set(payload["faces"]) >= {"reader", "evidence", "duplicate", "count"}, (
            "%s shape: the wired run must evaluate the four faces, got %r"
            % (shape, payload["faces"])
        )


def test_a8_the_wired_command_goes_red_on_a_broken_document(tmp_path):
    """The executed command can fail — otherwise the green above proves nothing."""
    command = _wired_checker_command()
    doc, spec = _wired_fixture(tmp_path)
    doc.write_text("# Broken\n\n没有任何读者声明。\n", encoding="utf-8")
    shapes = _wired_shapes(_wired_argv(command, doc, spec))
    for shape, argv in shapes.items():
        proc = _run_wired(argv)
        assert proc.returncode == 1, (
            "%s shape: a document without a reader declaration must fail the blocking "
            "gate; exit=%d stderr=%r" % (shape, proc.returncode, proc.stderr)
        )
        payload = json.loads(proc.stdout)
        assert "reader-declaration-missing" in {
            item["rule"] for item in payload["findings"]
        }, "%s shape: expected reader-declaration-missing, got %r" % (
            shape, payload["findings"]
        )


# --------------------------------------------------------------------------- #
# SC-008 — earlier specs stay byte-identical
# --------------------------------------------------------------------------- #
def test_pre_completion_specs_stay_byte_identical():
    for rel, expected in FROZEN_SPEC_HASHES.items():
        path = REPO_ROOT / rel
        assert path.is_file(), "frozen spec missing: %s" % rel
        assert _sha256(path) == expected, "frozen spec changed: %s" % rel
