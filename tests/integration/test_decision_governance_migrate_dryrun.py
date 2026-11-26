"""Integration: the instruction section reaches an initialized workspace; the base corpus stays intact.

Pins the two migration-side clauses that need a real workspace and the real git history:

* ``test_instructions_generated_dimension`` — C-503 (BC-04): a client workspace whose
  instruction template predates the ``Decision Items`` section converges through
  ``specify migrate``'s existing ``templates-generated`` dimension. Measured reading: the
  dry-run plan lists the ``.specify/templates/instructions-template.md`` replace item — that
  file is the source of truth the generated ``.specify/instructions.md`` is rendered from
  (the generator reconciles whole sections), so converging the template is what converges
  the generated instructions; the migrate command's own Handoffs section delegates the
  regeneration of ``.specify/instructions.md`` to ``/speckit.instructions``, and the 097
  engine contract lists the compared surfaces without the generated file. The test therefore
  proves the section end to end: the plan lists the convergence item under
  ``templates-generated``, ``--apply`` converges the template, the client's own instruction
  generator then carries the section into ``.specify/instructions.md`` (custom content
  preserved), and the migrate dimension set gains no seventh member.
* ``test_base_corpus_zero_rewrite`` — C-502: line-level containment over the base corpus at
  ``08b59695c`` — register rows, ``T-NNN`` carriers (``plan.md``), checkpoint files, run and
  review/analyze report bodies (``test-evidence/``), acceptance reports
  (``verification.md``) and the clarifications record body of every pre-existing
  ``requirements.md``. No pre-existing line is removed or changed; appended lines and newly
  added files are allowed. A real base-corpus carrier with old-form ``D-`` headings is
  reported ``legacy`` and is never judged, which is the C-206 behaviour exercised against the
  actual corpus rather than a fixture.

Red-first: C-502's and C-501's red form is a mutation (the corpus predates this package); the
mutations live inside the contract-side guards and in ``test-evidence/migration-closure.md``.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import specify_cli

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
BASE = "08b59695c"

#: The closed migrate dimension set (C-503: no seventh member).
CLOSED_DIMENSIONS = (
    "templates-generated",
    "anchor-layout",
    "compat-links",
    "mirror-consistency",
    "migration-residue",
    "store-layout",
)

SECTION_TOKEN = "Decision Items"
SECTION_RULES = (
    "full name",
    "abbreviation",
    "`same_name_conflict: true`",
    "`resource_locator`",
    "business resource group",
    "region id",
)
CUSTOM_MARKER = "PROJECT-CUSTOM-MARKER-107"


def _run(cmd, cwd: Path, timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, check=False
    )


def _init_client(project: Path) -> None:
    project.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src") + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    proc = subprocess.run(
        [
            sys.executable,
            "-c",
            "from specify_cli import main; main()",
            "init",
            "--here",
            "--ai",
            "qoder",
            "--script",
            "sh",
            "--no-git",
        ],
        cwd=str(project),
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    assert proc.returncode == 0, (
        f"specify init failed (rc={proc.returncode})\n"
        f"stdout:\n{proc.stdout[-3000:]}\nstderr:\n{proc.stderr[-3000:]}"
    )


def section(text: str, token: str) -> str | None:
    """One H2 section (heading line included) up to the next H2, or None when absent."""
    lines = text.splitlines(keepends=True)
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and token in line:
            start = index
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "".join(lines[start:end])


def remove_section(path: Path, token: str) -> None:
    body = path.read_text(encoding="utf-8")
    chunk = section(body, token)
    assert chunk, f"{path} carries no {token!r} section to remove"
    path.write_text(body.replace(chunk, ""), encoding="utf-8")


def git(*args: str) -> subprocess.CompletedProcess:
    return _run(["git", *args], ROOT)


def clarify_body(text: str) -> str | None:
    """The § Clarifications record body (the C-502 'clarifications' corpus unit)."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## Clarifications"):
            start = index
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end])


def is_corpus_path(rel: str) -> bool:
    """The base-corpus carrier families of C-502 (requirements.md handled separately)."""
    if rel == ".specify/register.md":
        return True
    parts = rel.split("/")
    if parts[:2] != [".specify", "specs"] or len(parts) < 4:
        return False
    name = parts[-1]
    if name in ("plan.md", "verification.md") and len(parts) == 4:
        return True
    return "checkpoints" in parts[3:-1] or "test-evidence" in parts[3:-1]


# --------------------------------------------------------------------------- #
# C-503 — the instruction section converges through templates-generated
# --------------------------------------------------------------------------- #

def test_instructions_generated_dimension(tmp_path: Path) -> None:
    """C-503: a pre-section client converges via the existing templates-generated dimension."""
    project = tmp_path / "client"
    _init_client(project)

    template = project / ".specify" / "templates" / "instructions-template.md"
    instructions = project / ".specify" / "instructions.md"
    assert section(template.read_text(encoding="utf-8"), SECTION_TOKEN), (
        "the delivered instruction template does not carry the Decision Items section"
    )

    # Simulate an initialized workspace that predates the section: template without the
    # section, and a generated instruction file rendered from that template.
    remove_section(template, SECTION_TOKEN)
    generated = _run(["bash", ".specify/scripts/bash/generate-instructions.sh"], project)
    assert generated.returncode == 0, (
        f"the client instruction generator failed (rc={generated.returncode})\n"
        f"{generated.stdout[-2000:]}\n{generated.stderr[-2000:]}"
    )
    stale = instructions.read_text(encoding="utf-8")
    assert section(stale, SECTION_TOKEN) is None, (
        "the stale client unexpectedly carries the section before migration"
    )
    instructions.write_text(
        stale + f"\n## Project Custom Section\n\n{CUSTOM_MARKER}\n", encoding="utf-8"
    )

    # Dry-run plan: the dimension set is the closed six, and templates-generated carries the
    # instruction-template convergence item.
    from typer.testing import CliRunner

    runner = CliRunner()
    planned = runner.invoke(
        specify_cli.app, ["migrate", "--workspace", str(project), "--dry-run", "--format", "json"]
    )
    assert planned.exit_code == 1, (
        f"the dry-run planned exit {planned.exit_code}, expected 1: {planned.output}"
    )
    payload = json.loads(planned.stdout)
    assert payload["outcome"] == "planned", payload.get("outcome")

    assert tuple(specify_cli.MIGRATE_DIMENSIONS) == CLOSED_DIMENSIONS, (
        "the migrate dimension set changed; C-503 forbids a seventh member: "
        f"{specify_cli.MIGRATE_DIMENSIONS}"
    )
    observed = {item["dimension"] for item in payload["items"]}
    assert observed <= set(CLOSED_DIMENSIONS), observed

    convergence = [
        item
        for item in payload["items"]
        if item["dimension"] == "templates-generated"
        and item["target"] == ".specify/templates/instructions-template.md"
    ]
    assert convergence, (
        "the dry-run plan lists no instruction-template convergence item under "
        f"templates-generated: {payload['items']}"
    )
    assert convergence[0]["disposition"] == "replace", convergence[0]

    # Apply converges the instruction template; the client's own generator then carries the
    # whole section into the generated file without touching custom content.
    applied = runner.invoke(
        specify_cli.app, ["migrate", "--workspace", str(project), "--apply", "--format", "json"]
    )
    assert applied.exit_code == 0, (
        f"migrate --apply exited {applied.exit_code}, expected 0: {applied.output}"
    )
    assert json.loads(applied.stdout)["outcome"] == "applied", applied.stdout
    assert section(template.read_text(encoding="utf-8"), SECTION_TOKEN), (
        "the converged template does not carry the Decision Items section"
    )

    regenerated = _run(["bash", ".specify/scripts/bash/generate-instructions.sh"], project)
    assert regenerated.returncode == 0, (
        f"the post-migration instruction generation failed (rc={regenerated.returncode})\n"
        f"{regenerated.stdout[-2000:]}\n{regenerated.stderr[-2000:]}"
    )
    final = instructions.read_text(encoding="utf-8")
    delivered = section(final, SECTION_TOKEN)
    assert delivered, "the generated instructions do not carry the Decision Items section"
    for token in SECTION_RULES:
        assert token in delivered, f"the delivered section lacks {token!r}"
    assert CUSTOM_MARKER in final, (
        "the instruction regeneration dropped the project's custom section"
    )

    # The per-tool compatibility copy follows the generated file (SC-010).
    qoder_copy = project / "QODER.md"
    assert qoder_copy.is_file(), "the init workspace carries no per-tool instruction copy"
    assert section(qoder_copy.read_text(encoding="utf-8"), SECTION_TOKEN), (
        "the per-tool instruction copy does not carry the Decision Items section"
    )


# --------------------------------------------------------------------------- #
# C-502 — the base corpus is not rewritten
# --------------------------------------------------------------------------- #

def test_base_corpus_zero_rewrite() -> None:
    """C-502: line-level containment over the base corpus; legacy records stay readable."""
    base_files = git("ls-tree", "-r", "--name-only", BASE)
    assert base_files.returncode == 0, base_files.stderr
    base_list = [line for line in base_files.stdout.splitlines() if line]
    assert len(base_list) > 1000, "the measured base tree is implausibly small"

    corpus = [rel for rel in base_list if is_corpus_path(rel)]
    assert len(corpus) > 1000, (
        f"the base-corpus carrier set is implausibly small: {len(corpus)} file(s)"
    )

    # Every pre-existing corpus file still exists at HEAD (no rename-out, no deletion).
    head_files = git("ls-tree", "-r", "--name-only", "HEAD")
    assert head_files.returncode == 0, head_files.stderr
    missing = set(corpus) - set(head_files.stdout.splitlines())
    assert missing == set(), f"pre-existing corpus files vanished: {sorted(missing)[:5]}"

    # No pre-existing corpus file lost a line: the numstat deletion column is 0 everywhere.
    numstat = git("diff", "--numstat", f"{BASE}..HEAD", "--", ".specify/register.md", ".specify/specs")
    assert numstat.returncode == 0, numstat.stderr
    changes = []
    for line in numstat.stdout.splitlines():
        added, deleted, path = line.split("\t", 2)
        if is_corpus_path(path):
            changes.append((path, added, deleted))
            assert deleted == "0", f"{path} lost {deleted} pre-existing line(s)"
    assert changes, "no corpus file changed at all; the reading is vacuous"

    deleted_files = git(
        "diff", "--diff-filter=D", "--name-only", f"{BASE}..HEAD", "--",
        ".specify/register.md", ".specify/specs",
    )
    assert deleted_files.returncode == 0, deleted_files.stderr
    assert [p for p in deleted_files.stdout.splitlines() if is_corpus_path(p)] == [], (
        "a corpus carrier file was deleted"
    )

    # The register is append-only (its legacy D-/T- rows are never rewritten).
    register = git("diff", "--numstat", f"{BASE}..HEAD", "--", ".specify/register.md")
    assert register.returncode == 0, register.stderr
    rows = register.stdout.split()
    if rows:
        assert rows[1] == "0", f"the register lost {rows[1]} line(s): {register.stdout!r}"

    # The clarifications record body of every pre-existing requirements.md is append-only.
    requirements = [rel for rel in base_list if rel.endswith("/requirements.md")]
    with_clarifications = 0
    for rel in requirements:
        shown = git("show", f"{BASE}:{rel}")
        assert shown.returncode == 0, shown.stderr
        base_body = clarify_body(shown.stdout)
        if base_body is None:
            continue
        with_clarifications += 1
        current = (ROOT / rel).read_text(encoding="utf-8")
        head_body = clarify_body(current)
        assert head_body is not None, f"{rel} lost its Clarifications section"
        assert head_body.startswith(base_body), (
            f"{rel}: a pre-existing clarification line was removed or changed"
        )
    assert with_clarifications > 50, (
        f"only {with_clarifications} clarifications body(ies) measured; the reading is vacuous"
    )

    # Old-form records are reported legacy, never judged — against the real base corpus.
    legacy_carrier = ".specify/specs/065-loop-interruption-recovery/research.md"
    assert (ROOT / legacy_carrier).is_file(), f"missing corpus carrier: {legacy_carrier}"
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    judged = subprocess.run(
        [
            sys.executable, "scripts/python/validate-decisions.py",
            "--action", "records", "--carrier", legacy_carrier, "--json",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert judged.returncode == 0, (
        f"a legacy corpus carrier was judged (rc={judged.returncode}): {judged.stdout}"
    )
    payload = json.loads(judged.stdout)
    assert payload["status"] == "pass", payload["violations"]
    legacy_headings = [e for e in payload["legacy"] if e["kind"] == "heading"]
    assert legacy_headings, "the legacy corpus carrier reported no legacy heading"
    assert not any(legacy_carrier in violation["path"] for violation in payload["violations"]), (
        payload["violations"]
    )
