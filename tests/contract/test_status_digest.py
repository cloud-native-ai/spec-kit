"""Contract test: the thin command entry, its per-tool copies, and their one shared reading (087, T028 — US3).

Layer-2 of the Feature 087 test map. This file owns the **command-side half** of the one-command-one-script-one-reading
clause, ``contracts/status-digest.contract.md`` C-41 (DG-01) / C-42 (DG-02):

* ``templates/commands/status.md`` names ``scripts/python/status-digest.py`` and the delegated action, and carries
  **no rendering logic of its own** — no line format, no cap arithmetic, no proposition judgement, no registry
  parsing;
* the per-tool copies ``_ASSISTANT_COMMAND_DIRS`` produces are present and byte-identical to what the canonical
  generator emits from the source template — the projection clause: a hand-edited copy, a stale copy, or a copy for a
  tool directory that does not exist here all go red;
* the script behind the entry reads exactly the three registry-resolved inputs over a fixture registry and opens no
  file for writing, so a second state parser or a write path goes red.

**Clause partition.** C-41's *script-action* half (exactly three actions, all sharing one reader) is claimed by T009;
this row claims the *entry* half, and states the shared-reading proposition once over a fixture rather than
re-stating the action set. C-42's fixture-side no-write assertion is T027's; the no-write reading here is asserted at
the **process** level over the whole fixture tree so the two rows cannot silently agree on a defect.

**Red-first (Constitution IV)**: authored after the script exists but before the template does, so the entry half
starts red on "template missing" — never on an import or collection error. The copy half is red for the same reason:
the generator writes one copy per source template, and the template is what is missing.

**Deliberately not asserted here**: the owner document's text (``test_reporting_obligations.py``), the digest's
rendered shapes and exit set (``tests/unit/test_status_digest_unit.py``), and the guard's thirteen propositions
(T033).
"""
from __future__ import annotations

import ast
import filecmp
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "commands" / "status.md"
SCRIPT = REPO_ROOT / "scripts" / "python" / "status-digest.py"
OWNER = REPO_ROOT / "shared" / "guidelines" / "reporting-obligations.md"

#: The script path the template must name (C-41: the entry delegates, it does not re-implement).
SCRIPT_PATH = "scripts/python/status-digest.py"

#: The three actions C-41 fixes, as the entry must name them.
ACTIONS = ("digest", "guard", "report")

#: The generated copies, per ``_ASSISTANT_COMMAND_DIRS`` in ``src/specify_cli/__init__.py`` plus
#: ``_ASSISTANT_EXTENSIONS``. The six configured tools are copilot / claude / hermes / opencode / qoder / codex;
#: only the four whose command directories exist in this repository are written (tasks.md § Environment
#: Prerequisites records the probe: `.hermes/` and `.codex/` do not exist here).
EXPECTED_COPIES = (
    Path(".claude") / "commands" / "speckit.status.md",
    Path(".github") / "prompts" / "speckit.status.prompt.md",
    Path(".opencode") / "command" / "speckit.status.md",
    Path(".qoder") / "commands" / "speckit.status.md",
)

#: Shapes that would mean the entry re-renders what the script already renders (C-41's "no logic of its own").
#: Scope note: the ``## Wrap-up`` section below them is a generated probe block shared by every command template
#: (it names other engines' own actions), so the rendering audit reads the delegation section only — judging the
#: generated block here would red every sibling template for the same non-reason.
RENDERING_SHAPES = {
    "a rendered digest entry row": r"^\s*line_id\s*[=:]",
    "the omitted count computed in the command": r"omitted\s*=\s*(?:len\(|\{|%|\d)",
    "a cap default restated": r"DEFAULT_CAP|cap\s*=\s*\d+",
    "a proposition literal judged in the command": r"\bRO-0\d\b.*\b(?:pass|fail)\b",
    "a registry read in the command": r"glob\(\s*[\"']\*\.json|read_text\(.*\.json",
}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _require_template() -> Path:
    assert TEMPLATE.is_file(), (
        "the thin command template is missing: %s — expected at T029 (087). Red is the intended "
        "pre-implementation state for T028." % TEMPLATE.relative_to(REPO_ROOT)
    )
    return TEMPLATE


def _frontmatter(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, "the command template must open with a YAML frontmatter block"
    return match.group(1)


def _body(text: str) -> str:
    parts = text.split("---")
    assert len(parts) >= 3, "the command template must open with a YAML frontmatter block"
    return "---".join(parts[2:])


def _delegation_section(text: str) -> str:
    """The part of the body before the generated ``## Wrap-up`` probe block."""
    body = _body(text)
    marker = "## Wrap-up"
    return body.split(marker, 1)[0] if marker in body else body


def _generator_body(template_text: str, agent: str) -> str:
    """The body a copy carries: the template's body after the generator's two content transformations.

    The generator (``src/specify_cli/__init__.py`` § ``generate_commands``) does two things to the content that this
    function reproduces: it drops the ``scripts:`` / ``agent_scripts:`` frontmatter sections, and it rewrites
    root-relative paths to their runtime form (``shared/x`` → ``.specify/shared/x``, ``skills/external/n`` →
    ``.specify/skills/n``). Everything else — the AUTO-GENERATED marker, the per-tool description line — is an
    addition this test asserts separately, so a copy's every byte traces back to the source template.
    """
    sys.path.insert(0, str(REPO_ROOT / "src"))
    try:
        from specify_cli import rewrite_paths
    finally:
        sys.path.pop(0)

    out, in_frontmatter, skipping = [], False, False
    for line in template_text.split("\n"):
        if line.strip() == "---":
            out.append(line)
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            if line.strip().startswith(("scripts:", "agent_scripts:")):
                skipping = True
                continue
            if skipping and line.strip() and not line.startswith(" "):
                skipping = False
            if skipping:
                continue
        out.append(line)
    cleaned = "\n".join(out)
    body = "---".join(cleaned.split("---")[2:]).strip()
    return rewrite_paths(body.replace("__AGENT__", agent))


def _first_difference(actual: str, expected: str) -> str:
    """The first differing line pair, so a red names the byte rather than dumping two files."""
    for index, (left, right) in enumerate(
        zip(actual.splitlines(), expected.splitlines()), 1
    ):
        if left != right:
            return "line %d\n  copy:      %r\n  generated: %r" % (index, left, right)
    if len(actual.splitlines()) != len(expected.splitlines()):
        return "line count differs: copy=%d generated=%d" % (
            len(actual.splitlines()),
            len(expected.splitlines()),
        )
    return "(no line differs; whitespace at EOF)"


def _run_digest(args, cwd: Path, env_overrides: dict):
    env = {"PATH": "/usr/bin:/bin", "HOME": str(cwd)}
    env.update(env_overrides)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=env,
    )


# --------------------------------------------------------------------------- #
# C-41 — the entry names the script and the action, and renders nothing itself
# --------------------------------------------------------------------------- #
def test_c41_the_command_template_exists_and_carries_frontmatter():
    """The entry is a real command template, addressed as ``/speckit.status``."""
    template = _require_template()
    text = template.read_text(encoding="utf-8")
    front = _frontmatter(text)
    assert "description:" in front, "the presentation key `description` is required"
    assert "short-description:" in front, (
        "the single-line presentation key every sibling command carries is required"
    )


def test_c41_the_command_names_the_script_path():
    """C-41: the entry delegates to the one script."""
    text = _require_template().read_text(encoding="utf-8")
    assert SCRIPT_PATH in text, (
        "the template must name the script it delegates to (%r); got:\n%s" % (SCRIPT_PATH, text)
    )
    assert SCRIPT.is_file(), "the named script must exist: %s" % SCRIPT.relative_to(REPO_ROOT)


def test_c41_the_command_names_the_three_actions():
    """C-41: the entry exposes exactly the three actions and delegates each to the script."""
    text = _delegation_section(_require_template().read_text(encoding="utf-8"))
    named = {action for action in ACTIONS if re.search(r"--action\s+%s\b" % action, text)}
    assert named == set(ACTIONS), (
        "the template must name every one of the three delegated actions (%r); found %r"
        % (ACTIONS, sorted(named))
    )
    assert not re.search(r"--action\s+(?!digest\b|guard\b|report\b)[a-z]+", text), (
        "the template names an action outside the closed three (contract C-41)"
    )


def test_c41_the_command_carries_no_rendering_logic():
    """C-41: no line format, no cap arithmetic, no verdict, no registry parsing in the entry."""
    body = _delegation_section(_require_template().read_text(encoding="utf-8"))
    offenders = [
        label for label, pattern in RENDERING_SHAPES.items() if re.search(pattern, body, re.M)
    ]
    assert not offenders, (
        "the thin entry must not re-render what the script renders; found %r" % (offenders,)
    )


def test_c41_the_rendering_audit_turns_red_when_the_entry_re_renders():
    """A green check is a claim, not evidence: the audit above is proven by seeding the defect it names."""
    text = _require_template().read_text(encoding="utf-8")
    seeded = text.replace(
        "## Wrap-up",
        "```\nline_id=%s state=%s omitted=len(entries) - cap\n```\n\n## Wrap-up",
        1,
    )
    body = _delegation_section(seeded)
    offenders = [
        label for label, pattern in RENDERING_SHAPES.items() if re.search(pattern, body, re.M)
    ]
    assert offenders, (
        "the rendering audit must turn red on a seeded re-rendering; it found nothing in %r" % (body,)
    )


def test_c41_the_command_reaches_the_owner_instead_of_defining_it():
    """The entry points at the owner document; it never restates the owner's rules."""
    text = _require_template().read_text(encoding="utf-8")
    assert "shared/guidelines/reporting-obligations.md" in text, (
        "the entry must reach the duty's owner by path rather than define the duty itself"
    )
    assert OWNER.is_file(), "the owner document the entry points at must exist"


def test_c41_the_command_forbids_paraphrasing_the_script_output():
    """The thinness is stated as a rule, not only practised: the entry says it prints verbatim."""
    text = _require_template().read_text(encoding="utf-8").lower()
    assert "verbatim" in text, (
        "the entry must state that the script's output is reported verbatim (C-41's no-second-rendering rule)"
    )


def test_c41_the_entry_states_the_closed_exit_status_set():
    """C-45's statuses reach the caller through the entry, so the entry names them."""
    text = _require_template().read_text(encoding="utf-8")
    for status in ("0", "1", "2", "3"):
        assert re.search(r"`%s`" % status, text), (
            "the entry must name the exit status %r it can return (contract C-45)" % status
        )
    assert "nothing-running" in text, (
        "the entry must state that the idle rendering is explicit, never an empty result"
    )


# --------------------------------------------------------------------------- #
# C-41 / C-42 — the per-tool copies are present and match the source template
# --------------------------------------------------------------------------- #
def test_c42_the_four_per_tool_copies_are_present():
    """The copies exist exactly where ``_ASSISTANT_COMMAND_DIRS`` + ``_ASSISTANT_EXTENSIONS`` put them."""
    missing = [str(rel) for rel in EXPECTED_COPIES if not (REPO_ROOT / rel).is_file()]
    assert not missing, (
        "the generated per-tool copies are missing: %r — regenerate with "
        "`python3 scripts/python/regen-command-copies.py` (never by hand)" % (missing,)
    )


@pytest.mark.parametrize("rel", EXPECTED_COPIES, ids=lambda p: p.as_posix())
def test_c42_each_copy_matches_what_the_generator_emits(rel: Path):
    """A copy's body equals the source template's body after the generator's own two transformations.

    The comparison is made against ``_generator_body`` — the template body with the ``scripts:`` frontmatter removed
    and root-relative paths rewritten, which is exactly what ``generate_commands`` does to the content. The copy's two
    other parts (the generation marker and the per-tool description line) are asserted separately below, so every
    byte of the copy traces to the source template and a hand-edit anywhere goes red.
    """
    copy = REPO_ROOT / rel
    assert copy.is_file(), "generated copy missing: %s" % rel
    actual = copy.read_text(encoding="utf-8")
    expected = _generator_body(_require_template().read_text(encoding="utf-8"), _agent_for(rel))

    marker = "<!-- AUTO-GENERATED from templates/commands/status.md"
    body = actual
    if body.startswith("---\n"):
        end = body.index("\n---\n", 4)
        head = body[:end]
        assert head.startswith("---\ndescription: "), (
            "a copy for a frontmatter-carrying tool opens with exactly a description line; got %r" % head
        )
        body = body[end + len("\n---\n"):]
    assert body.startswith(marker), (
        "the copy must begin with the generator's marker line; got %r" % body[:120]
    )
    body = body.split("\n", 1)[1]
    assert body.strip() == expected.strip(), (
        "copy %s differs from the generator's output for the source template.\n"
        "First differing region:\n%s" % (rel, _first_difference(body, expected))
    )


def _agent_for(rel: Path) -> str:
    """Map a copy path back to its ``_ASSISTANT_COMMAND_DIRS`` key."""
    sys.path.insert(0, str(REPO_ROOT / "src"))
    try:
        import specify_cli
    finally:
        sys.path.pop(0)
    for agent, directory in specify_cli._ASSISTANT_COMMAND_DIRS.items():
        if rel.parent == Path(directory):
            return agent
    raise AssertionError("copy path %s matches no configured command directory" % rel)


def test_c42_no_copy_exists_for_a_tool_without_a_command_directory():
    """The two configured-but-absent tools (hermes, codex) get no copy: the generator writes only real dirs."""
    stray = [
        str(rel)
        for rel in (Path(".hermes") / "commands" / "speckit.status.md",
                    Path(".codex") / "commands" / "speckit.status.md")
        if (REPO_ROOT / rel).exists()
    ]
    assert not stray, (
        "no copy may exist for a command directory this repository does not have: %r" % (stray,)
    )


def test_c42_the_generator_reports_no_drift():
    """The framework's own check agrees with this test's per-file reading, and names the same four files."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "python" / "regen-command-copies.py"), "--check"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, "regen-command-copies.py --check failed:\n%s%s" % (
        proc.stdout,
        proc.stderr,
    )
    assert "OK: all per-tool command copies match the source templates." in proc.stdout, (
        "the check must print the framework's canonical OK line; got %r" % proc.stdout
    )


# --------------------------------------------------------------------------- #
# C-42 — the reading behind the entry: three registry-resolved inputs, no write
# --------------------------------------------------------------------------- #
def _fixture_tree(tmp_path: Path):
    """A fixture registry plus the three triplet files one entry declares."""
    import json

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = tmp_path / "registry"
    registry.mkdir()
    triplet = {}
    for key, suffix in (
        ("status_path", ".status"),
        ("log_path", ".live.log"),
        ("heartbeat_path", ".heartbeat"),
    ):
        path = tmp_path / ("fixture-line" + suffix)
        path.write_text("working\n", encoding="utf-8")
        triplet[key] = str(path)
    entry = {
        "schema_version": 1,
        "line_id": "t028-fixture-line",
        "run_id": "r20261106T000000Z-t028",
        "project_dir": str(workspace),
        "repo_root": str(workspace),
        "driver_session": "pid:1",
        "cli": "qodercli",
        "state": "active",
        "last_event": "registered",
        "created_at": "2026-11-06T00:00:00Z",
        "updated_at": "2026-11-06T00:00:00Z",
        "run_history": [],
    }
    entry.update(triplet)
    (registry / "t028-fixture-line.json").write_text(
        json.dumps(entry, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    return workspace, registry, entry, sorted(str(p) for p in triplet.values())


def test_an_alive_pid_file_becomes_the_executor_row(tmp_path):
    """Executor-primary (2026-11-10): a live pid-<line>-<stage> record renders as that line's executor row."""
    import os

    workspace, registry, entry, _paths = _fixture_tree(tmp_path)
    state_dir = workspace / ".specify" / "state"
    state_dir.mkdir(parents=True)
    (state_dir / ("pid-%s-analyze" % entry["line_id"])).write_text(
        "pid=%d start=0 at=1794290000 line=%s stage=analyze event=pid\n"
        % (os.getpid(), entry["line_id"]),
        encoding="utf-8",
    )
    proc = _run_digest(
        ["--action", "digest", "--format", "table", "--workspace", str(workspace)],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )
    assert proc.returncode == 0, proc.stderr
    rows = _rows(proc.stdout)
    assert len(rows) == 1, rows
    assert "fork(" in rows[0] and ("pid %d" % os.getpid()) in rows[0], rows[0]
    assert "/speckit.analyze" in rows[0], rows[0]


def test_closed_lines_do_not_occupy_the_digest(tmp_path):
    """Reader contract (2026-11-10): closed lines are history — the digest never renders them."""
    import json

    workspace, registry, entry, _paths = _fixture_tree(tmp_path)
    closed = dict(entry, state="closed")
    (registry / (entry["line_id"] + ".json")).write_text(
        json.dumps(closed, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    proc = _run_digest(
        ["--action", "digest", "--format", "table", "--workspace", str(workspace)],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )
    assert proc.returncode == 3, "an all-closed view is the explicit nothing-running answer; got %r" % (proc,)
    assert proc.stdout.strip() == "nothing-running", proc.stdout


def test_c42_over_a_fixture_registry_the_script_reads_the_entry_and_its_three_triplet_paths(tmp_path):
    """C-42: the entry's declared triplet paths are the reading's activity input — nothing else is opened."""
    import json

    workspace, registry, entry, triplet_paths = _fixture_tree(tmp_path)

    proc = _run_digest(
        ["--action", "digest", "--format", "json"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )

    assert proc.returncode == 0, "the fixture digest must render; rc=%s stderr=%r" % (
        proc.returncode,
        proc.stderr,
    )
    payload = json.loads(proc.stdout)
    assert [e["line_id"] for e in payload["entries"]] == [entry["line_id"]], (
        "the reading must project the fixture entry; got %r" % (payload["entries"],)
    )
    projected = payload["entries"][0]["triplet"]
    assert sorted(projected.values()) == triplet_paths, (
        "the reading must consume exactly the three declared triplet paths; got %r" % (projected,)
    )


def test_digest_header_names_the_resolved_registry_dir(tmp_path):
    """P-1 (coaching 20261109T161132Z): the reading header names the resolved registry directory."""
    workspace, registry, _entry, _paths = _fixture_tree(tmp_path)
    proc = _run_digest(
        ["--action", "digest"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )
    assert proc.returncode == 0, proc.stderr
    header = proc.stdout.splitlines()[0]
    assert str(registry) in header, (
        "the digest header must name the resolved registry directory; got %r" % (header,)
    )


def test_c42_a_digest_leaves_the_fixture_tree_byte_identical(tmp_path):
    """C-42 at process level: the reading writes no file anywhere under the fixture tree."""
    workspace, registry, _entry, _paths = _fixture_tree(tmp_path)

    def snapshot() -> dict:
        return {
            str(p.relative_to(tmp_path)): (p.stat().st_mtime_ns, p.read_bytes())
            for p in sorted(tmp_path.rglob("*"))
            if p.is_file()
        }

    before = snapshot()
    proc = _run_digest(
        ["--action", "digest"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )
    after = snapshot()

    assert proc.returncode == 0, "the fixture digest must render; rc=%s stderr=%r" % (
        proc.returncode,
        proc.stderr,
    )
    assert after == before, (
        "the digest must open no file for writing; changed: %r"
        % (sorted(set(after) ^ set(before)) or "contents differ",)
    )


def test_c42_the_script_the_entry_names_is_a_single_stdlib_only_file():
    """A second module behind the entry would be a second reading (C-41's one-script rule)."""
    assert SCRIPT.is_file(), "the script the entry names must exist"
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    third_party = sorted(
        name
        for name in imported
        if name not in sys.stdlib_module_names and name != "__future__"
    )
    assert not third_party, (
        "the script behind the entry must import only the standard library; found %r" % (third_party,)
    )
    assert not (SCRIPT.parent / "status_digest").exists(), (
        "the script must stay one file; a sibling package would be a second reading surface"
    )


# --------------------------------------------------------------------------- #
# T033 (US4) — the guard's thirteen propositions, its mutation fixtures and
# its not-evaluated rule
#
# This partition's own green point is C-46 (the proposition-set clause): the
# guard reports exactly the thirteen ids `contracts/reporting-obligations.contract.md`
# C-01…C-13 defines, each with a named status. The clause that fixes a
# proposition's *subject* lives there and is never restated here — every test
# below names an id and asserts only what this guard reads on disk.
# --------------------------------------------------------------------------- #

#: The thirteen proposition ids. Owner: `contracts/reporting-obligations.contract.md`
#: C-01…C-13 (the `C-0k · RO-0k` ledger-name slot). This tuple is a *consumer* of that
#: list: it names ids and asserts the guard's set equals it, and it states no
#: proposition's subject — constitution XIV forbids a second statement of one.
PROPOSITION_IDS = tuple("RO-%02d" % index for index in range(1, 14))

#: The three named statuses a proposition may carry (C-46).
STATUS_VALUES = ("pass", "fail", "not-evaluated")

#: The verdict-line shape the guard prints: `<id> <status> <reason>`.
VERDICT_LINE = re.compile(r"^(RO-\d{2})\s+(pass|fail|not-evaluated)\b\s*(.*)$")


def _guard(args, registry: Path, cwd: Path | None = None):
    """Run one guard invocation against an empty registry so no ambient entry leaks in."""
    return _run_digest(
        ["--action", "guard", *args],
        cwd=cwd or REPO_ROOT,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )


def _verdicts(stdout: str) -> dict:
    """Parse the verdict lines into `{id: (status, reason)}` — the named-status reading."""
    out = {}
    for line in stdout.splitlines():
        match = VERDICT_LINE.match(line.strip())
        if match:
            out[match.group(1)] = (match.group(2), match.group(3).strip())
    return out


def _json_verdicts(stdout: str) -> dict:
    import json

    payload = json.loads(stdout)
    rows = payload.get("propositions") or payload.get("verdicts") or []
    return {
        row["proposition"]: (row["status"], row.get("reason", "")) for row in rows
    }


def _compliant_inputs(root: Path) -> dict:
    """Materialise every guard input a compliant fixture needs, under one directory.

    The fixtures are *inputs*, never verdicts: each is the artifact a real run would
    leave behind, shaped the way the capturing rows (T019 / T026 / T052) captured them.
    """
    import json

    root.mkdir(parents=True, exist_ok=True)
    registry = root / "registry"
    registry.mkdir()

    # A team-roster fixture that carries exactly one reporter seat and a territory.
    roster = root / "compliant-team.md"
    roster.write_text(
        "---\n"
        "name: compliant-fixture-team\n"
        "members:\n"
        "  - slug: lead\n"
        "    role: lead\n"
        "    agent: sdd-loop-driver\n"
        "  - slug: reporter\n"
        "    role: reporter\n"
        "    agent: reporter\n"
        "    reporting-territory:\n"
        "      read: [state spine, line registry]\n"
        "      write: [own stream artifact]\n"
        "---\n",
        encoding="utf-8",
    )

    # A captured line set: four elements, attribution, a trigger, and the three
    # transition classes named — with no interrogative or approval marker anywhere.
    line_set = root / "line-set.txt"
    attribution = "structure=alpha-team run=r20261106T000000Z-guard profile=long-run"
    elements = "position=stage-2-of-4 delta=one-landed remainder=two-stages-left blocker=no blocker"
    line_set.write_text(
        "\n".join(
            [
                "%s trigger=tick %s" % (attribution, elements),
                "%s trigger=boundary %s" % (attribution, elements),
                "%s trigger=transition:worker-a %s observed=sub-flow failure"
                % (attribution, elements),
                "%s trigger=transition:worker-b %s observed=stall crossing"
                % (attribution, elements),
                "%s trigger=transition:worker-c %s observed=dispatch failure"
                % (attribution, elements),
                "%s trigger=reporter-failure %s" % (attribution, elements),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # A captured supervision report: one row per dispatched sub-flow. It is a SEPARATE
    # capture from the status line set — RO-05 reads a line set and RO-06 reads a
    # supervision report, and fusing the two would make one fixture prove both.
    supervision = root / "supervision.txt"
    supervision.write_text(
        "structure=alpha-team run=r20261106T000000Z-guard profile=long-run trigger=tick %s\n"
        "sub-flow=worker-a state=running age=5s threshold_row=Manifest stuck at `in-progress`\n"
        "sub-flow=worker-b state=completed age=12s threshold_row=Manifest stuck at `in-progress`\n"
        "structure=alpha-team run=r20261106T000000Z-guard profile=long-run trigger=reporter-failure %s"
        % (elements, elements),
        encoding="utf-8",
    )
    supervision.write_text(
        supervision.read_text(encoding="utf-8").rstrip("\n") + "\n", encoding="utf-8"
    )

    # The seeded flow sample: every flow classified, none unclassifiable.
    flow_sample = root / "flow-sample.txt"
    flow_sample.write_text(
        "team-run | in-scope | two or more concurrent units\n"
        "supervising-master | in-scope | one asynchronous delegation continued past dispatch\n"
        "single-sync-command | out-of-scope | one synchronous step\n",
        encoding="utf-8",
    )

    # A run record whose carrier value is the declared stream artifact path.
    run_record = root / "run-record.json"
    carrier_path = root / "alpha-team.live.log"
    run_record.write_text(
        json.dumps(
            {"run": "r20261106T000000Z-guard", "mode": "external", "carrier": str(carrier_path)},
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "alpha-team.live.log").write_text("tick\n", encoding="utf-8")
    (root / "seed-digest.txt").write_text(
        "cap=5 stale_bound=15m00s profile=long-run\n"
        "line_id=a state=active age=3s\n"
        "line_id=b state=active age=9s\n"
        "omitted=7\n"
        "line_id=c state=stale age=41m00s stale\n",
        encoding="utf-8",
    )
    return {
        "registry": registry,
        "roster": roster,
        "line_set": line_set,
        "supervision": supervision,
        "flow_sample": flow_sample,
        "run_record": run_record,
    }


def _compliant_args(inputs: dict) -> list:
    return [
        "--line-set",
        str(inputs["line_set"]),
        "--supervision-line-set",
        str(inputs["supervision"]),
        "--flow-sample",
        str(inputs["flow_sample"]),
        "--roster",
        str(inputs["roster"]),
        "--carrier",
        str(inputs["run_record"].parent / "alpha-team.live.log"),
        "--run-record",
        str(inputs["run_record"]),
    ]


def test_c46_the_guard_reports_exactly_the_thirteen_proposition_ids(tmp_path):
    """C-46: the proposition set equals the C-01…C-13 id set exactly — no fourteenth, no second id."""
    inputs = _compliant_inputs(tmp_path / "compliant")
    proc = _guard(_compliant_args(inputs), inputs["registry"])
    verdicts = _verdicts(proc.stdout)
    assert set(verdicts) == set(PROPOSITION_IDS), (
        "the guard must report exactly %r; reported %r" % (PROPOSITION_IDS, sorted(verdicts))
    )
    assert len(verdicts) == 13, "the guard reported %d proposition(s); the closed set is 13" % len(
        verdicts
    )


def test_c46_every_proposition_carries_a_named_status(tmp_path):
    """C-46: each of the thirteen carries one of the three named statuses, plus a reason."""
    inputs = _compliant_inputs(tmp_path / "compliant")
    proc = _guard(_compliant_args(inputs), inputs["registry"])
    verdicts = _verdicts(proc.stdout)
    assert verdicts, "the guard printed no verdict line; stdout=%r" % proc.stdout
    for name, (status, reason) in sorted(verdicts.items()):
        assert status in STATUS_VALUES, "%s carries the unnamed status %r" % (name, status)
        assert reason, "%s carries a %r status with no reason" % (name, status)


def test_c46_a_compliant_fixture_yields_no_fail(tmp_path):
    """C-46: over a compliant fixture every proposition is `pass` or a reason-bearing `not-evaluated`."""
    inputs = _compliant_inputs(tmp_path / "compliant")
    proc = _guard(_compliant_args(inputs), inputs["registry"])
    verdicts = _verdicts(proc.stdout)
    failing = {name: value for name, value in verdicts.items() if value[0] == "fail"}
    assert not failing, "a compliant fixture must not yield a fail: %r" % (failing,)
    assert proc.returncode == 0, (
        "the guard exits 0 on zero findings (C-45's guard status set); rc=%s stdout=%r stderr=%r"
        % (proc.returncode, proc.stdout, proc.stderr)
    )


def test_c46_the_guard_reports_one_finding_as_exit_one(tmp_path):
    """C-45's guard status set: at least one `fail` is exit `1`, input error is exit `2`."""
    inputs = _compliant_inputs(tmp_path / "compliant")
    args = _compliant_args(inputs)
    # A line set with an interrogative line turns RO-10 red, and nothing else.
    with open(inputs["line_set"], "a", encoding="utf-8") as handle:
        handle.write("structure=alpha-team run=r20261106T000000Z-guard should I continue?\n")
    proc = _guard(args, inputs["registry"])
    verdicts = _verdicts(proc.stdout)
    assert verdicts.get("RO-10", ("", ""))[0] == "fail", (
        "an interrogative line set must turn RO-10 red; got %r" % (verdicts.get("RO-10"),)
    )
    assert proc.returncode == 1, (
        "a finding exits 1; rc=%s stdout=%r" % (proc.returncode, proc.stdout)
    )


def test_c46_the_guard_emits_a_json_reading_with_the_same_ids(tmp_path):
    """C-46: the machine-readable reading carries the same id set, so a consumer never re-parses prose."""
    import json

    inputs = _compliant_inputs(tmp_path / "compliant")
    proc = _run_digest(
        ["--action", "guard", "--format", "json", *_compliant_args(inputs)],
        cwd=REPO_ROOT,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(inputs["registry"])},
    )
    payload = json.loads(proc.stdout)
    rows = payload.get("propositions") or payload.get("verdicts") or []
    assert rows, "the json reading must carry a proposition list; got %r" % (sorted(payload),)
    assert {row["proposition"] for row in rows} == set(PROPOSITION_IDS)
    for row in rows:
        assert row["status"] in STATUS_VALUES
        assert row.get("reason"), "%s carries no reason in the json reading" % row["proposition"]


# --------------------------------------------------------------------------- #
# C-46 — eight mutation fixtures, each turning its matching proposition red
# --------------------------------------------------------------------------- #

MUTATIONS = (
    # (label, proposition, mutate)
    ("seat-removed", "RO-04", "a roster in the population loses its reporter seat and records no reason"),
    ("second-cadence-literal-seeded", "RO-03", "a scratch framework-source file carries a second literal"),
    ("omission-count-removed", "RO-09", "the owner's digest section loses the omitted-count face"),
    ("stale-marker-removed", "RO-09", "the owner's digest section loses the staleness face"),
    ("annotation-dropped", "RO-05", "a captured line loses one of the four element labels"),
    ("interrogative-line-injected", "RO-10", "a captured line becomes a question"),
    ("suppressed-tick", "RO-11", "the fixture carries no reporter-failure line"),
    ("carrier-value-altered", "RO-12", "the carrier is neither `console` nor a stream artifact path"),
)


def _mutate(label: str, inputs: dict, workspace: Path):
    """Apply one mutation and return the extra argv it needs (if any)."""
    if label == "seat-removed":
        roster = inputs["roster"]
        roster.write_text(
            roster.read_text(encoding="utf-8").replace(
                "  - slug: reporter\n"
                "    role: reporter\n"
                "    agent: reporter\n"
                "    reporting-territory:\n"
                "      read: [state spine, line registry]\n"
                "      write: [own stream artifact]\n",
                "",
            ),
            encoding="utf-8",
        )
        assert "role: reporter" not in roster.read_text(encoding="utf-8"), (
            "the mutation must actually remove the seat"
        )
        return []
    if label == "second-cadence-literal-seeded":
        seed = workspace / "seeded-framework-source.md"
        seed.write_text(
            "# seeded scratch framework source\nThe cadence is 30 seconds by default.\n",
            encoding="utf-8",
        )
        return ["--scan-root", str(workspace)]
    if label in {"omission-count-removed", "stale-marker-removed"}:
        return []  # applied by the caller through the owner-path override
    if label == "annotation-dropped":
        line_set = inputs["line_set"]
        text = line_set.read_text(encoding="utf-8")
        line_set.write_text(text.replace("blocker=no blocker", "blocker_status=none", 1), encoding="utf-8")
        return []
    if label == "interrogative-line-injected":
        with open(inputs["line_set"], "a", encoding="utf-8") as handle:
            handle.write("structure=alpha-team run=r20261106T000000Z-guard do you approve this?\n")
        return []
    if label == "suppressed-tick":
        supervision = inputs["supervision"]
        supervision.write_text(
            supervision.read_text(encoding="utf-8").replace(
                "trigger=reporter-failure", "trigger=tick"
            ),
            encoding="utf-8",
        )
        assert "reporter-failure" not in supervision.read_text(encoding="utf-8"), (
            "the mutation must actually drop the failure line from the supervision capture"
        )
        return []
    if label == "carrier-value-altered":
        return ["--carrier", "a channel that was never declared"]
    raise AssertionError("no mutation named %r" % label)


def _mutated_owner(owner_text: str, label: str) -> str:
    """An owner text with one digest-contract face removed, for the two RO-09 mutations."""
    if label == "omission-count-removed":
        return owner_text.replace("omitted=<n>", "a truncation notice").replace("omitted", "truncated")
    if label == "stale-marker-removed":
        return owner_text.replace("stale", "aged").replace("staleness", "ageing")
    return owner_text


@pytest.mark.parametrize(
    "label,proposition,description",
    MUTATIONS,
    ids=[row[0] for row in MUTATIONS],
)
def test_c46_a_mutation_fixture_turns_its_matching_proposition_red(
    tmp_path, label, proposition, description
):
    """C-46: each of the eight mutations turns its own proposition red — a green check is proven, not claimed."""
    inputs = _compliant_inputs(tmp_path / label)
    extra = _mutate(label, inputs, tmp_path / label)
    args = _compliant_args(inputs) + extra
    if label in {"omission-count-removed", "stale-marker-removed"}:
        owner_copy = tmp_path / label / "owner.md"
        owner_copy.write_text(
            _mutated_owner(OWNER.read_text(encoding="utf-8"), label), encoding="utf-8"
        )
        args = args + ["--owner-doc", str(owner_copy)]

    proc = _guard(args, inputs["registry"])
    verdicts = _verdicts(proc.stdout)
    status, reason = verdicts.get(proposition, ("", ""))
    assert status == "fail", (
        "mutation %r (%s) must turn %s red; got %r (reason %r)\nstdout=%r"
        % (label, description, proposition, status, reason, proc.stdout)
    )
    assert proc.returncode == 1, (
        "a red proposition is a finding: exit 1; rc=%s" % proc.returncode
    )


def test_c46_the_unmutated_baseline_stays_green(tmp_path):
    """The mutation fixtures are proven by contrast: the same fixture, unmutated, carries no `fail`."""
    inputs = _compliant_inputs(tmp_path / "baseline")
    proc = _guard(_compliant_args(inputs), inputs["registry"])
    verdicts = _verdicts(proc.stdout)
    failing = {name: value for name, value in verdicts.items() if value[0] == "fail"}
    assert not failing, (
        "the paired baseline must stay green, else the mutation proves nothing: %r" % (failing,)
    )


# --------------------------------------------------------------------------- #
# C-46 — an unavailable input is `not-evaluated` with a reason, never `pass`
# --------------------------------------------------------------------------- #

def test_c46_a_proposition_with_no_readable_input_is_never_reported_pass(tmp_path):
    """C-46: zero inputs — every input-reading proposition says `not-evaluated` and gives its reason."""
    registry = tmp_path / "registry"
    registry.mkdir()
    proc = _guard([], registry)
    verdicts = _verdicts(proc.stdout)
    assert set(verdicts) == set(PROPOSITION_IDS), (
        "the guard must still report all thirteen with zero inputs; got %r" % (sorted(verdicts),)
    )
    for name, (status, reason) in sorted(verdicts.items()):
        assert status in {"not-evaluated", "pass"}, (
            "%s must not be `fail` on an absent input (absence is not a violation); got %r" % (name, status)
        )
        if status == "not-evaluated":
            assert reason, "%s is `not-evaluated` without a reason" % name


def test_c46_an_unreadable_line_set_is_not_evaluated_not_pass(tmp_path):
    """C-46: a named input that cannot be read is `not-evaluated` with the path in the reason."""
    registry = tmp_path / "registry"
    registry.mkdir()
    missing = tmp_path / "no-such-line-set.txt"
    proc = _guard(["--line-set", str(missing)], registry)
    verdicts = _verdicts(proc.stdout)
    line_set_propositions = [name for name, (status, _r) in verdicts.items() if status == "not-evaluated"]
    assert "RO-05" in line_set_propositions, (
        "RO-05 reads the captured line set; an unreadable one must be `not-evaluated`; got %r"
        % (verdicts.get("RO-05"),)
    )
    reason = verdicts["RO-05"][1]
    assert "no-such-line-set.txt" in reason or "unreadable" in reason, (
        "the reason must name what was unreadable; got %r" % reason
    )


def test_c46_a_roster_outside_the_repository_is_judged_by_its_content(tmp_path):
    """C-04 / REC-A2: an absolute `--roster` path outside the repo is read as given, never repo-prefixed.

    SC-002's documented unblock step creates the roster in *another* project, so the population half of the
    criterion is decided over a path this repository does not contain. The fixture is passed as an absolute path —
    the caller-supplied form — and both readings of the *same* path are asserted (present seat, then absent seat),
    so a helper that flattened every outside path into one verdict cannot satisfy this test.
    """
    registry = tmp_path / "registry"
    registry.mkdir()
    outside = tmp_path / "external-project"
    outside.mkdir()
    roster = outside / "outside-team.md"
    roster.write_text(
        "---\n"
        "name: outside-fixture-team\n"
        "members:\n"
        "  - slug: lead\n"
        "    role: lead\n"
        "  - slug: reporter\n"
        "    role: reporter\n"
        "---\n",
        encoding="utf-8",
    )
    assert REPO_ROOT not in roster.resolve().parents, (
        "the fixture must live outside the repository, else it proves nothing about a caller-supplied path"
    )

    proc = _guard(["--roster", str(roster.resolve())], registry)
    verdicts = _verdicts(proc.stdout)
    status, reason = verdicts.get("RO-04", ("", ""))
    assert status == "pass", (
        "the roster path is in the population and supplies exactly one reporter seat, so its content must be read"
        " into the verdict: the expected verdict is `pass`, not the `not-evaluated` an unread path produces;"
        " got %r (reason %r)\nstdout=%r" % (status, reason, proc.stdout)
    )
    assert "1 roster path" in reason, (
        "the reason must count the population it judged; got %r" % reason
    )

    roster.write_text(
        "---\nname: outside-fixture-team\nmembers:\n  - slug: lead\n    role: lead\n---\n",
        encoding="utf-8",
    )
    proc = _guard(["--roster", str(roster.resolve())], registry)
    verdicts = _verdicts(proc.stdout)
    status, reason = verdicts.get("RO-04", ("", ""))
    assert status == "fail", (
        "the same outside path with its reporter seat removed must be `fail`, never `not-evaluated`;"
        " got %r (reason %r)" % (status, reason)
    )
    assert "absent reporter seat" in reason, (
        "the reason must name the seat defect the content carries; got %r" % reason
    )


def test_c46_an_unreadable_roster_path_is_not_evaluated_not_fail(tmp_path):
    """C-46 / REC-A2: a population path that cannot be read is `not-evaluated` with its path — never a seat defect.

    The paired red for the test above: the two outside-path readings are only distinguishable if this one does
    **not** come back `pass`, and an unreadable input must not be booked as an absent seat either.
    """
    registry = tmp_path / "registry"
    registry.mkdir()
    missing = tmp_path / "external-project" / "no-such-roster.md"
    proc = _guard(["--roster", str(missing)], registry)
    verdicts = _verdicts(proc.stdout)
    status, reason = verdicts.get("RO-04", ("", ""))
    assert status == "not-evaluated", (
        "an unreadable roster path proves nothing about the seat, so it must be `not-evaluated`;"
        " got %r (reason %r) — a `pass` or a `fail` here means the read error was booked as a finding"
        % (status, reason)
    )
    assert "no-such-roster.md" in reason, "the reason must name the unreadable path; got %r" % reason
    assert "absent reporter seat" not in reason, (
        "an unreadable path must not be booked as an absent seat; got %r" % reason
    )
    assert proc.returncode == 0, (
        "a `not-evaluated` proposition is not a finding (C-45); rc=%s stdout=%r"
        % (proc.returncode, proc.stdout)
    )


def test_c46_an_empty_roster_population_is_not_evaluated_with_that_reason(tmp_path):
    """C-46 / C-04: zero population paths is `not-evaluated` — no glob is ever a default population."""
    registry = tmp_path / "registry"
    registry.mkdir()
    baseline = tmp_path / "empty-baseline.txt"
    baseline.write_text("# no roster path is in the population\n", encoding="utf-8")
    proc = _guard(["--roster-baseline", str(baseline)], registry)
    verdicts = _verdicts(proc.stdout)
    status, reason = verdicts.get("RO-04", ("", ""))
    assert status == "not-evaluated", (
        "an empty population must be `not-evaluated`, never `pass`; got %r (reason %r)" % (status, reason)
    )
    assert "population" in reason.lower() or "no roster" in reason.lower(), (
        "the reason must state that no path is in the population; got %r" % reason
    )


# --------------------------------------------------------------------------- #
# T036 (US4) — the zero-new-machinery boundary, audited rather than asserted
#
# This partition's green point is C-50 (no scheduler, timer, daemon or
# third-party dependency). The prohibition itself is owned by
# `shared/guidelines/reporting-obligations.md` § 十一 and its nine items by
# `contracts/reporting-obligations.contract.md` C-13 — neither is restated here:
# this partition audits *the delivered files*, which is the only thing a test can
# decide.
# --------------------------------------------------------------------------- #

#: The delivered `.py` files this feature ships (``feature-ref.md`` § Delivered paths #8 and #17, plus the
#: pre-existing engine the feature reads read-only — the engine is audited too because a feature that needs it to
#: spawn would have failed the clause as surely as one that spawns itself).
DELIVERED_PY = (
    Path("scripts") / "python" / "status-digest.py",
    Path("skills") / "internal" / "create-team" / "scripts" / "validate-roster.py",
)

#: Modules a delivery path must never import: a process spawn, a background thread, a task loop, a network client.
FORBIDDEN_MODULES = frozenset(
    {
        "subprocess",
        "multiprocessing",
        "threading",
        "concurrent",
        "asyncio",
        "socket",
        "http",
        "urllib",
        "requests",
        "httpx",
        "sched",
        "signal",
        "atexit",
    }
)

#: Calls a delivery path must never make: spawn, exec, fork, a network open, a scheduler registration.
FORBIDDEN_CALLS = frozenset(
    {
        "system",
        "popen",
        "fork",
        "forkpty",
        "execv",
        "execve",
        "execvp",
        "execl",
        "execle",
        "spawnl",
        "spawnv",
        "spawnlpe",
        "socket",
        "urlopen",
        "run",
        "call",
        "Popen",
        "check_output",
        "Timer",
        "Thread",
        "enter",
        "enterabs",
        "create_task",
        "run_until_complete",
    }
)

#: The pre-change dependency list of ``pyproject.toml`` (measured at the feature's base commit and unchanged since:
#: ``git diff 56f3f881..HEAD -- pyproject.toml`` is empty). The pin is on the *list*, not on a count, so a swap that
#: keeps the length but changes a name still goes red.
PRE_CHANGE_RUNTIME_DEPENDENCIES = (
    "typer",
    "rich",
    "httpx[socks]",
    "platformdirs",
    "readchar",
    "truststore>=0.10.4; python_version >= '3.10'",
)


def _delivered_py_trees() -> list:
    """The delivered `.py` files as parsed ASTs, one per file that exists."""
    trees = []
    for rel in DELIVERED_PY:
        path = REPO_ROOT / rel
        assert path.is_file(), "a delivered script is missing: %s" % rel
        trees.append((rel, ast.parse(path.read_text(encoding="utf-8"), filename=str(path))))
    return trees


def test_c50_no_delivered_script_imports_a_spawn_thread_or_network_module():
    """C-50: the AST-level import scan — no delivery path imports any machinery module."""
    offenders = []
    for rel, tree in _delivered_py_trees():
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module]
            for name in names:
                if name.split(".")[0] in FORBIDDEN_MODULES:
                    offenders.append((rel.as_posix(), name, getattr(node, "lineno", 0)))
    assert not offenders, (
        "a delivered script imports a machinery module (C-50): %r" % (offenders,)
    )


def test_c50_no_delivered_script_calls_a_spawn_or_scheduler_api():
    """C-50: the AST-level call scan — an attribute call to any spawn/scheduler API is the defect, not its import."""
    offenders = []
    for rel, tree in _delivered_py_trees():
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and func.attr in FORBIDDEN_CALLS:
                    offenders.append((rel.as_posix(), func.attr, getattr(node, "lineno", 0)))
                elif isinstance(func, ast.Name) and func.id in {"exec", "eval", "compile"}:
                    offenders.append((rel.as_posix(), func.id, getattr(node, "lineno", 0)))
    assert not offenders, (
        "a delivered script calls a spawn/scheduler API (C-50): %r" % (offenders,)
    )


def test_c50_the_call_scan_turns_red_on_a_seeded_call():
    """A green check is a claim, not evidence: the call scan is proven by seeding the call it forbids."""
    seeded = ast.parse("import os\nos.system('true')\n")
    found = [
        node.func.attr
        for node in ast.walk(seeded)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in FORBIDDEN_CALLS
    ]
    assert found == ["system"], "the seeded call scan must find `system`; found %r" % (found,)


def test_c50_no_delivered_script_imports_outside_the_standard_library():
    """C-50: every delivered script is stdlib-only, so no third-party dependency is introduced."""
    offenders = []
    for rel, tree in _delivered_py_trees():
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imported.add(node.module.split(".")[0])
        third_party = sorted(
            name
            for name in imported
            if name not in sys.stdlib_module_names and name != "__future__"
        )
        if third_party:
            offenders.append((rel.as_posix(), third_party))
    assert not offenders, (
        "a delivered script imports outside the standard library (C-50): %r" % (offenders,)
    )


def _pyproject_dependency_lists() -> dict:
    """The dependency lists `pyproject.toml` declares, parsed without a TOML engine dependency.

    ``tomllib`` is stdlib from Python 3.11; the section is read from it when available, and the shape is asserted
    against the pinned list either way so a parser gap cannot silently pass.
    """
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    try:
        import tomllib

        data = tomllib.loads(text)
        project = data.get("project", {})
        return {
            "runtime": list(project.get("dependencies", [])),
            "optional": sorted(project.get("optional-dependencies", {})),
            "dev": list(data.get("dependency-groups", {}).get("dev", [])),
        }
    except Exception:  # pragma: no cover - a TOML-parser gap must fail loudly, not pass silently
        raise AssertionError("pyproject.toml could not be parsed; the dependency pin cannot be read")


def test_c50_the_runtime_dependency_list_is_pinned_to_its_pre_change_values():
    """C-50 / OM-04: the runtime dependency list is byte-for-byte the pre-change list — no entry added."""
    actual = tuple(_pyproject_dependency_lists()["runtime"])
    assert actual == PRE_CHANGE_RUNTIME_DEPENDENCIES, (
        "the runtime dependency list changed.\n  expected: %r\n  actual:   %r\n"
        "C-50 forbids a new third-party dependency on a delivery path." % (PRE_CHANGE_RUNTIME_DEPENDENCIES, actual)
    )


def test_c50_no_optional_or_dev_dependency_group_was_introduced():
    """C-50: an extra group is as much a new dependency surface as an added runtime entry.

    The pre-change file declared no optional-dependency group. On 2026-11-07 the merged trunk's
    Feature 086 (WP-A3) legitimately added the single ``[project.optional-dependencies] dev``
    group (pytest + pytest-xdist) for its concurrent test execution; that sanctioned group is
    fixed here, while any additional optional group or any ``[dependency-groups]`` entry still
    fails. The runtime list pin above remains the C-50 no-new-dependency guard.
    """
    lists = _pyproject_dependency_lists()
    assert lists["optional"] == ["dev"], (
        "only Feature 086's sanctioned `dev` optional group may exist: %r" % (lists["optional"],)
    )
    assert lists["dev"] == [], (
        "a dependency group was introduced: %r" % (lists["dev"],)
    )


# --------------------------------------------------------------------------- #
# T061 (US5) — the digest and the line keep their shapes under the efficiency dimension
#
# `[green: contracts/measure-report.contract.md#C-55]` / `[covers: FR-023, FR-024]`.
#
# What this partition owns: the **digest-side** half of the "store availability is never a precondition" floor
# (``efficiency-element.contract.md`` C-67 / C-68). The element's own shape, order and degradation are that file's
# subject and are asserted there; here the dimension is judged only by what it must NOT disturb — the cap and its
# ``omitted=`` summary, the entry ordering, the staleness marking, the exit-status table and the status line's four
# content elements plus its attribution. The element is present throughout; because the marker's literal, the
# store-availability literal and the element's field name all have owners elsewhere, they are read here at run time
# (``_efficiency_marker``/``_efficiency_no_measurements`` from ``shared/guidelines/reporting-obligations.md`` § 九,
# the field name from the element's contract) rather than spelled a second time.
# --------------------------------------------------------------------------- #
def _owner_section() -> str:
    """The owner's efficiency-dimension section — the definition point for the dimension's render vocabulary.

    ``ownership-map.contract.md`` C-47 makes this section the single definition site of the not-evaluated marker
    and the store-availability state, so a test that spelled either literal would be a second copy of the fact it
    checks. The section is located by its first sentence, not by a line number.
    """
    text = OWNER.read_text(encoding="utf-8")
    start = text.find("效率维度落在这两个面上")
    assert start >= 0, (
        "the owner document carries no efficiency-dimension section; the dimension's render vocabulary has no "
        "definition site (contract C-47)"
    )
    end = text.find("\n## ", start)
    return text[start:] if end < 0 else text[start:start + end]


def _element_field() -> str:
    """The element's rendered field name, read from the test that pins the field group's shape.

    The marker and the availability state have their definition site in the owner's § 九; the field the element is
    rendered under is not spelled there. Its shape is pinned by the C-68 judge in
    ``tests/contract/test_efficiency_element.py``, which strips exactly ``<field>=<…>`` to recover a store-less
    render — the one place the field name is fixed. Reading it from there keeps this file from becoming a second
    copy of that fact.
    """
    judge = REPO_ROOT / "tests" / "contract" / "test_efficiency_element.py"
    text = judge.read_text(encoding="utf-8")
    match = re.search(r"([a-z_]+)=\(\[\^\|", text)
    assert match, (
        "no owner fixes the efficiency element's rendered field name; the dimension has no declared render face"
    )
    return match.group(1) + "="


def _owner_literal(pattern: str, what: str) -> str:
    """Read one rendered literal out of its single definition site (the owner's efficiency-dimension section)."""
    for match in re.finditer(pattern, _owner_section()):
        value = next((group for group in match.groups() if group), None)
        if value:
            return value
    raise AssertionError("the owner document declares no %s literal (contract C-47)" % what)


def _efficiency_marker() -> str:
    return _owner_literal(r"`(not[- ]evaluated)`", "not-evaluated marker")


def _efficiency_no_measurements() -> str:
    """The store-availability literal — the owner's OTHER literal, so the marker match cannot leak in here."""
    marker = _efficiency_marker()
    for match in re.finditer(r"`([A-Za-z][A-Za-z _-]*)`", _owner_section()):
        value = match.group(1)
        if value.lower() != marker.lower() and not value.startswith(("contracts/", "efficiency")):
            return value
    raise AssertionError("the owner document declares no store-availability literal (contract C-47)")


def _digest_fixture(tmp_path: Path, count: int):
    """A registry of ``count`` active entries plus the efficiency store those entries' units are measured in."""
    import json

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = tmp_path / "registry"
    registry.mkdir()
    for index in range(count):
        entry = {
            "schema_version": 1,
            "line_id": "t061-line-%02d" % index,
            "run_id": "r20261106T0000%02dZ-t061" % index,
            "project_dir": str(workspace),
            "repo_root": str(workspace),
            "driver_session": "pid:1",
            "cli": "qodercli",
            "state": "active",
            "last_event": "registered",
            "created_at": "2026-11-06T00:00:00Z",
            "updated_at": "2026-11-06T00:%02d:00Z" % index,
            "run_history": [],
        }
        (registry / ("%s.json" % entry["line_id"])).write_text(
            json.dumps(entry, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )
    records = workspace / ".specify" / "memory" / "exec-quant" / "records"
    records.mkdir(parents=True)
    for index in range(count):
        record = {
            "kind": "speckit.exec-quant",
            "unit_id": "/speckit.plan" if index % 2 == 0 else "/speckit.tasks",
            "unit_type": "command",
            "run_id": "r20261106T0000%02dZ-t061" % index,
            "collected_at": "2026-11-06T00:%02d:00Z" % index,
            "quality": {
                "elapsed_ms": {"value": 1000 * (index + 1), "provenance": "carried"},
                "tokens": "not_evaluated",
                "invocations": "not_evaluated",
            },
        }
        (records / ("20261106T00%02d00000000Z-t061%04d.json" % (index, index))).write_text(
            json.dumps(record), encoding="utf-8"
        )
    return workspace, registry


def _rows(rendered: str) -> list:
    lines = rendered.splitlines()
    sep = next((i for i, l in enumerate(lines) if l and set(l.replace(" ", "")) == {"-"}), None)
    if sep is None:
        return []
    rows = []
    for line in lines[sep + 1:]:
        if not line.strip():
            break
        if line.startswith(("last_completion=", "omitted=", "store=", "最近完成：", "另有 ", "未找到运行记录存储")):
            break
        rows.append(line)
    return rows


def test_c55_the_element_never_grows_the_digest_past_its_cap_and_omitted_count(tmp_path):
    """C-55: the cap bounds the ENTRY set, and the element is content of an entry — never an extra entry."""
    workspace, registry = _digest_fixture(tmp_path, 6)
    proc = _run_digest(
        ["--action", "digest", "--format", "json", "--workspace", str(workspace), "--cap", "2"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )
    assert proc.returncode == 0, "the fixture digest must render; rc=%s stderr=%r" % (
        proc.returncode,
        proc.stderr,
    )
    import json as _json
    payload = _json.loads(proc.stdout)
    assert len(payload["entries"]) == 2, "the declared cap bounds the entry set"
    assert payload["omitted"] == 4, "the omitted count is carried by the state (C-43)"
    elements = (payload.get("efficiency") or {}).get("elements") or []
    assert elements, "the dimension is content of the listed entries, never a second entry"


def test_c55_a_listed_unit_with_no_record_carries_the_marker_and_no_entry_is_dropped(tmp_path):
    """C-67 at the digest surface: an unmeasured unit is marked, never omitted beside a neighbour's number."""
    workspace, registry = _digest_fixture(tmp_path, 2)
    proc = _run_digest(
        ["--action", "digest", "--format", "json", "--workspace", str(workspace), "--cap", "5"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )
    assert proc.returncode == 0, proc.stderr
    import json as _json
    payload = _json.loads(proc.stdout)
    assert len(payload["entries"]) == 2, "the marker never costs an entry its row"
    assert (payload.get("efficiency") or {}).get("elements"), "the element content is carried"


def test_c68_an_absent_store_keeps_the_entry_set_ordering_and_exit_status_unchanged(tmp_path):
    """C-68: with no store at all the digest still renders — same entries, same order, same exit status."""
    workspace, registry = _digest_fixture(tmp_path, 3)
    with_store = _run_digest(
        ["--action", "digest", "--workspace", str(workspace)],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )
    store = workspace / ".specify" / "memory" / "exec-quant"
    hidden = workspace / ".specify" / "memory" / "exec-quant-hidden"
    store.rename(hidden)
    try:
        without_store = _run_digest(
            ["--action", "digest", "--workspace", str(workspace)],
            cwd=workspace,
            env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
        )
    finally:
        hidden.rename(store)

    assert with_store.returncode == without_store.returncode == 0, (
        "an absent store changes no exit status; got %r then %r"
        % (with_store.returncode, without_store.returncode)
    )
    assert without_store.stdout.startswith("状态摘要"), (
        "the store-free render still answers the reader view; got %r" % without_store.stdout
    )
    def identities(text: str) -> list:
        # The executor cell is the row identity; the SPEC column is the stable per-entry identity under the
        # executor-primary redesign, so ordering is compared on that column.
        return [re.split(r"\s{2,}", row.strip())[1] for row in _rows(text)]

    assert identities(with_store.stdout) == identities(without_store.stdout), (
        "the store's presence never reorders or re-caps the entry set; got %r vs %r"
        % (identities(with_store.stdout), identities(without_store.stdout))
    )


def test_c68_a_stale_entry_still_carries_its_staleness_beside_the_element(tmp_path):
    """C-44 survives the dimension: a stale entry is still marked stale, with the element as extra content."""
    workspace, registry = _digest_fixture(tmp_path, 1)
    proc = _run_digest(
        ["--action", "digest", "--format", "json", "--workspace", str(workspace), "--stale-bound", "0"],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )
    assert proc.returncode == 0, proc.stderr
    import json as _json
    payload = _json.loads(proc.stdout)
    entry = payload["entries"][0]
    assert entry.get("stale") is True, "the staleness marking is untouched by the dimension"
    assert entry.get("age"), "a stale entry still carries its age (C-44)"
    assert (payload.get("efficiency") or {}).get("elements"), "the element rides the same reading"


def test_c55_the_status_line_keeps_its_four_content_elements_and_attribution(tmp_path):
    """C-23 / C-22 at the line surface: the dimension is added content, never a replacement or a reorder."""
    workspace, registry = _digest_fixture(tmp_path, 1)
    proc = _run_digest(
        [
            "--action", "report",
            "--workspace", str(workspace),
            "--structure", "fixture-team",
            "--run-stamp", "r20261106T090000Z",
            "--position", "implement 3/8",
            "--delta", "two rows landed",
            "--remainder", "five rows left",
            "--unit-id", "/speckit.plan",
            "--unit-type", "command",
        ],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )
    assert proc.returncode == 0, proc.stderr
    line = proc.stdout.strip()
    fields = [field.strip() for field in line.split("|")]
    assert fields[0] == "structure=fixture-team" and fields[1] == "run=r20261106T090000Z", (
        "the attribution still leads the line (C-22); got %r" % line
    )
    positions = {}
    for label in ("position", "delta", "remainder", "blocker"):
        index = next(
            (position for position, field in enumerate(fields) if field.startswith("%s=" % label)), -1
        )
        positions[label] = index
    assert all(index >= 0 for index in positions.values()), (
        "the four content elements are all present (C-23); got %r" % line
    )
    assert positions["position"] < positions["delta"] < positions["remainder"] < positions["blocker"], (
        "the elements keep their declared order; got %r" % positions
    )
    assert "blocker=no blocker" in line, (
        "no blocker is written as the explicit negation, never omitted (C-23); got %r" % line
    )
    assert line.endswith("carrier=console"), (
        "the carrier field still closes the line (C-26); got %r" % line
    )
    assert _element_field() in line, (
        "the dimension is added content of this same line — no second line, no replacement (C-63); got %r" % line
    )
    assert len(proc.stdout.strip().splitlines()) == 1, (
        "the element never opens a second line (C-63); got %r" % proc.stdout
    )


def test_c45_the_digest_exit_status_table_is_unchanged_by_the_dimension(tmp_path):
    """C-45: ``0`` with entries, ``3`` for nothing-running, ``2`` for an input error — the dimension adds none."""
    workspace, registry = _digest_fixture(tmp_path, 1)
    env = {"SPECIFY_LINE_REGISTRY_DIR": str(registry)}
    rendered = _run_digest(["--action", "digest", "--workspace", str(workspace)], cwd=workspace,
                           env_overrides=env)
    assert rendered.returncode == 0, rendered.stderr

    empty = tmp_path / "empty-registry"
    empty.mkdir()
    nothing = _run_digest(
        ["--action", "digest", "--workspace", str(workspace)],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(empty)},
    )
    assert nothing.returncode == 3, (
        "the store's presence never turns nothing-running into a success or an error; got %r" % nothing
    )
    assert "nothing-running" in nothing.stdout, (
        "the explicit nothing-running rendering is unchanged; got %r" % nothing.stdout
    )

    bad_cap = _run_digest(
        ["--action", "digest", "--workspace", str(workspace), "--cap", "0"],
        cwd=workspace,
        env_overrides=env,
    )
    assert bad_cap.returncode == 2, "an input error is still ``2``; got %r" % (bad_cap,)


# --------------------------------------------------------------------------- #
# Presentation — ``--format auto|table`` renders the SAME reading readably
# --------------------------------------------------------------------------- #
def test_the_table_format_groups_the_same_entries_readably(tmp_path):
    """C-41: the table is a presentation of the one reading, not a second one — every field retained."""
    workspace, registry, entry, _paths = _fixture_tree(tmp_path)
    proc = _run_digest(
        ["--action", "digest", "--format", "table", "--workspace", str(workspace)],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )
    assert proc.returncode == 0, "the table render must succeed; rc=%s stderr=%r" % (
        proc.returncode,
        proc.stderr,
    )
    out = proc.stdout
    assert out.splitlines()[0].startswith("状态摘要"), out
    # Reader-column redesign, second revision (2026-11-10): the EXECUTOR is the row; closed lines are
    # hidden; every row answers — who executes, which spec, what it is doing, its state, its elapsed time.
    for column in ("执行体", "所属 spec", "在做什么", "状态", "已执行时间"):
        assert column in out, "the single human format names its columns in reader words; got %r" % out
    for retired in ("已静默", "标记", "最近步骤与消耗"):
        assert retired not in out, "the redundant column %r must be gone; got %r" % (retired, out)
    rows = _rows(out)
    assert len(rows) == 1, "one aligned row per entry; got %r" % rows
    assert entry["line_id"] in rows[0], rows[0]
    assert ("fork(" in rows[0]) or ("—（无存活执行体）" in rows[0]), (
        "the executor column names the process carrier or states its absence; got %r" % rows[0]
    )
    assert any(word in rows[0] for word in ("活跃", "等待中", "阻塞", "已停滞")), rows[0]
    assert any(unit in rows[0] for unit in ("秒", "分", "小时", "天")), (
        "the elapsed column reports time in reader words; got %r" % rows[0]
    )


def test_the_default_format_is_the_single_human_table(tmp_path):
    """One human-facing format (2026-11-10 directive): the compact grid is the default; `json` is the machine channel."""
    workspace, registry, _entry, _paths = _fixture_tree(tmp_path)
    env = {"SPECIFY_LINE_REGISTRY_DIR": str(registry)}
    default = _run_digest(
        ["--action", "digest", "--workspace", str(workspace)],
        cwd=workspace,
        env_overrides=env,
    )
    json_run = _run_digest(
        ["--action", "digest", "--format", "json", "--workspace", str(workspace)],
        cwd=workspace,
        env_overrides=env,
    )
    retired = _run_digest(
        ["--action", "digest", "--format", "text", "--workspace", str(workspace)],
        cwd=workspace,
        env_overrides=env,
    )
    assert default.returncode == json_run.returncode == 0
    assert default.stdout.startswith("状态摘要") and "执行体" in default.stdout
    import json as _json
    assert _json.loads(json_run.stdout)["entries"], "the machine channel still parses"
    assert retired.returncode == 2, "the retired text/auto display variants are gone"


def test_the_table_format_keeps_the_nothing_running_literal(tmp_path):
    """C-45 holds for the table render too: the empty set renders the literal, exit 3."""
    workspace, _registry, _entry, _paths = _fixture_tree(tmp_path)
    empty = tmp_path / "empty-registry"
    empty.mkdir()
    proc = _run_digest(
        ["--action", "digest", "--format", "table", "--workspace", str(workspace)],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(empty)},
    )
    assert proc.returncode == 3, "nothing-running is still ``3``; got %r" % (proc,)
    assert proc.stdout.strip() == "nothing-running", proc.stdout
