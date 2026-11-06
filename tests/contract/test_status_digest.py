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
