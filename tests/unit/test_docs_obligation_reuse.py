"""Unit tests: obligation reuse and the untouched guards (spec 087, US4).

Owner of the assertion names and of each assertion's red-when condition: `plan.md` § Test Plan table A
(row `C-014` for the guard pins, and the `SC-005` / `SC-007` rows). Three duties live here, and they are one
file because all three read the repository rather than judge a fixture space:

* **`C-014` — the guards this feature must leave intact.** One assertion per guard row, each a *read-only
  citation*: the pin names the guard's own file, its literal and the owner clause. None of them re-implements a
  guard or copies its rule set — a second copy of a guard's rule is a second source of truth, which is exactly
  what `C-014` forbids.
* **`SC-005` — the single-capability guard.** This feature must not introduce a second drawing engine, renderer
  entry point, or engine-selection table anywhere in `templates/`, `skills/`, `shared/` or `scripts/`, and every
  diagram-producing surface must reach `skills/external/draw-diagram` by reference.
* **`SC-007` — the traceability-record guard.** A produced diagram's record entry carries the four faces the
  producing run must decide (`engine`, `engine_reason`, `ldm_summary`, `delivery.accepted`), a record missing one
  is unjudgeable rather than satisfied, and updating an existing diagram reuses the engine the record already
  names.
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "create-docs" / "scripts" / "docs-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "docs-obligation"
CONTRACT = REPO_ROOT / ".specify" / "specs" / "087-arch-diagram-docs" / "contracts" / "diagram-obligation.contract.md"
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "087-arch-diagram-docs"

_spec = importlib.util.spec_from_file_location("docs_obligation_fixtures_reuse", FIXTURES / "helpers.py")
fixtures = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fixtures)

DOC = "docs/concepts/widget-overview.md"


def record_arg(space: Path) -> str:
    runs = space / "docs" / ".speckit" / "runs"
    names = sorted(p.name for p in runs.glob("*.json"))
    assert len(names) == 1, f"expected exactly one trace record in {runs}, got {names}"
    return str(runs / names[0])


def obligation(space: Path, *extra: str) -> dict:
    proc = subprocess.run([sys.executable, str(SCRIPT), "--action", "obligation", "--root", str(space), *extra],
                          capture_output=True, text=True)
    assert proc.returncode == 0, f"engine exited {proc.returncode}: {proc.stderr}{proc.stdout}"
    return json.loads(proc.stdout)


def verdict_of(payload: dict, doc_path: str) -> tuple[str, str]:
    for entry in payload["documents"]:
        if entry["path"] == doc_path:
            return entry["verdict"], entry["reason"]
    raise AssertionError(f"{doc_path} not judged; documents={payload['documents']}")


# ---------------------------------------------------------------------------
# C-014 — one read-only citation per guard row
#
# Each row names the guard file, the literal that file pins, and the clause that places the guard. The
# assertion is that the guard is still there and still says what it said — not that its rule set is repeated
# here. Guard rows whose owner file exists at the feature's base commit are pinned by content; the per-tool
# command copies are generated, so their row is pinned by presence (a generated file's text belongs to its
# generator, not to this file).
# ---------------------------------------------------------------------------

GUARD_ROWS = (
    ("tests/contract/test_expression_gate_wiring.py", "A1", "def test_a1_docs_template_wiring_subsection"),
    ("tests/contract/test_expression_gate_wiring.py", "A3", "def test_a3_create_docs_skill_wires_owner_and_checker"),
    ("tests/contract/test_expression_gate_wiring.py", "A5", "def test_a5_wiring_text_has_no_class_words_or_attribution"),
    ("tests/contract/test_docs_command_template.py", "C3", "def test_c3_section_order"),
    ("tests/contract/test_docs_command_template.py", "C4a", "def test_c4a_mandatory_delegation"),
    ("tests/contract/test_confirmation_gates_sweep.py", "KEEP_LIST", "KEEP_LIST = ["),
    ("tests/contract/test_confirmation_gates_sweep.py", "KEEP_LIST", '("templates/commands/docs.md", "stop-and-confirm")'),
    ("tests/contract/test_directory_governance.py", "area-map", '"docs/concepts/documentation-model.md"'),
    ("tests/contract/test_expression_compatibility.py", "C5", "ALLOWED_POST_BASELINE_CHANGES = {"),
)


@pytest.mark.contract
@pytest.mark.parametrize("guard_file,guard_id,literal", GUARD_ROWS)
def test_c014_guard_rows_intact(guard_file: str, guard_id: str, literal: str):
    """Every guard pinned by `C-014` is still present, at its own path, with its pinning literal.

    One row per guard id, read from the guard's own file. The citation is deliberately shallow: this file must
    not become a second copy of the guard's rule set, so it asserts the anchor exists and nothing more.

    red-when: a guard file loses its pinning literal (a guard was renamed, moved or deleted while this feature
    was landing), so the delivery claims a guard it no longer has.
    """
    path = REPO_ROOT / guard_file
    assert path.is_file(), f"guard file {guard_file} is missing; {guard_id} has no owner to cite"
    body = path.read_text(encoding="utf-8")
    assert literal in body, f"{guard_id} no longer pins {literal!r} in {guard_file}"


@pytest.mark.contract
def test_c014_per_tool_copies_present():
    """`C-014`'s delivery surface includes the per-tool command copies; each is generated and each is present.

    The copies are produced by `regen-command-copies.py`, so their text is the generator's business and this
    assertion only pins their presence — that is the whole difference between a read-only citation and a
    second source of truth.

    red-when: a per-tool copy of the docs command stops existing, i.e. a delivery surface silently narrowed.
    """
    copies = (
        ".claude/commands/speckit.docs.md",
        ".github/prompts/speckit.docs.prompt.md",
        ".opencode/command/speckit.docs.md",
        ".qoder/commands/speckit.docs.md",
    )
    for rel in copies:
        assert (REPO_ROOT / rel).is_file(), f"the generated per-tool copy {rel} is missing"


@pytest.mark.contract
def test_c014_contract_names_each_guard_file():
    """The contract's own `C-014` table names the five guard files this delivery must keep intact.

    Reading the owner instead of re-typing its table is the point: if the contract loses a row, the delivery no
    longer has a clause to satisfy for that file.

    red-when: a guard file drops out of `C-014`'s table (the obligation would then be undefined for it).
    """
    text = CONTRACT.read_text(encoding="utf-8")
    section = text.split("## C-014", 1)[1].split("## C-015", 1)[0]
    for guard_file in (
        "tests/contract/test_expression_gate_wiring.py",
        "tests/contract/test_docs_command_template.py",
        "tests/contract/test_confirmation_gates_sweep.py",
        "tests/contract/test_directory_governance.py",
    ):
        assert guard_file in section, f"C-014's table no longer names {guard_file}"
    # the frozen-baseline guard is cited by `plan.md` T-001 (an allowlist entry is what keeps C5 green),
    # not by the contract body; the citation is pinned where it actually lives.
    plan = REPO_ROOT / ".specify" / "specs" / "087-arch-diagram-docs" / "plan.md"
    plan_body = plan.read_text(encoding="utf-8")
    assert "tests/contract/test_expression_compatibility.py" in plan_body, (
        "the frozen-baseline guard must stay cited by plan.md T-001, which authorizes its allowlist entry"
    )
    assert "ALLOWED_POST_BASELINE_CHANGES" in plan_body, (
        "the citation must name the mechanism (the allowlist), not only the file"
    )


# T034 — the five guard FILES (as distinct from the guard ids of `GUARD_ROWS` above). One row per file, each
# naming the literal that file pins and the owner that places it. This is the "which files may this feature not
# weaken" register: the ids above say *what* is pinned, this says *where the pin lives*, and the two are not the
# same question — `C3` and `C4a` both live in one file while `A1`/`A3`/`A5` share another.
GUARD_FILES = (
    ("tests/contract/test_expression_gate_wiring.py", "A1/A3/A5", "def test_a1_docs_template_wiring_subsection",
     "contracts/diagram-obligation.contract.md"),
    ("tests/contract/test_docs_command_template.py", "C3/C4a", "def test_c3_section_order",
     "contracts/diagram-obligation.contract.md"),
    ("tests/contract/test_confirmation_gates_sweep.py", "KEEP_LIST", '("templates/commands/docs.md", "stop-and-confirm")',
     "contracts/diagram-obligation.contract.md"),
    ("tests/contract/test_directory_governance.py", "area-map", '"docs/concepts/documentation-model.md"',
     "contracts/diagram-obligation.contract.md"),
    ("tests/contract/test_expression_compatibility.py", "C5", "def test_c5_non_wiring_files_keep_their_frozen_hashes",
     ".specify/specs/087-arch-diagram-docs/plan.md"),
)

# The files this feature authored. A row of this feature that appears here while a `GUARD_FILES` path also appears
# here is a feature editing a guard's assertion set — the one thing `C-014` forbids.
AUTHORED_BY_THIS_FEATURE = (
    "tests/unit/test_docs_utils_obligation.py",
    "tests/unit/test_docs_utils_carriers.py",
    "tests/unit/test_docs_obligation_reuse.py",
    "tests/integration/test_docs_obligation_scenarios.py",
    "tests/integration/test_docs_command_scenarios.py",
)


@pytest.mark.contract
@pytest.mark.parametrize("guard_file,guard_ids,literal,owner", GUARD_FILES)
def test_c014_five_guard_files_declared(guard_file: str, guard_ids: str, literal: str, owner: str):
    """Each of the five guard files is declared here with the literal it pins and the owner that places it.

    The declaration is the deliverable, and it is checked against reality rather than trusted: the file must
    exist, it must still carry the literal, and the clause that places the guard must be nameable. A register
    that only lists names is a wish list.

    red-when: one of the five guard files is gone, has lost its pinning literal, or its placing owner no longer
    names it — the delivery would then be constrained by a guard that is not there.
    """
    path = REPO_ROOT / guard_file
    assert path.is_file(), f"guard file {guard_file} ({guard_ids}) is missing"
    assert literal in path.read_text(encoding="utf-8"), f"{guard_ids} no longer pins {literal!r} in {guard_file}"
    owner_path = SPEC_DIR / owner.replace(".specify/specs/087-arch-diagram-docs/", "")
    assert owner_path.is_file(), f"the owner placing {guard_ids} is missing: {owner}"
    body = owner_path.read_text(encoding="utf-8")
    assert guard_file in body, f"{owner} no longer places the guard {guard_file}"


@pytest.mark.contract
def test_c014_no_row_of_this_feature_edits_a_guard_assertion_set():
    """None of this feature's own row files is one of the five guard files.

    `C-014` says the feature "只加义务指针" — it may add a pointer, it may not rewrite an assertion. The
    mechanical form of that sentence is a disjointness check between the set of files this feature authored and
    the set of files whose assertions are the guards: an intersection is the violation.

    red-when: a file that both this feature authored and the guard register names appears in
    `AUTHORED_BY_THIS_FEATURE` — i.e. a guard's assertion set was edited in the name of adding a pointer.
    """
    guard_paths = {row[0] for row in GUARD_FILES}
    overlap = sorted(guard_paths & set(AUTHORED_BY_THIS_FEATURE))
    assert not overlap, (
        "this feature edits a guard's assertion set, which C-014 forbids: " + ", ".join(overlap)
    )
    assert len(guard_paths) == 5, f"the guard register must name five distinct files, got {sorted(guard_paths)}"


# ---------------------------------------------------------------------------
# SC-005 — the single-capability guard
# ---------------------------------------------------------------------------

# The engine layer names of `skills/external/draw-diagram/references/routing-matrix.md` § 0.2. They are read
# from that owner rather than typed here: a routing row restated in this file would be a second source of truth
# for the very fact this assertion defends.
ROUTING_MATRIX = REPO_ROOT / "skills" / "external" / "draw-diagram" / "references" / "routing-matrix.md"
SCANNED_ROOTS = ("templates", "skills", "shared", "scripts")
DRAW_DIAGRAM_TREE = "skills/external/draw-diagram/"
BASE_COMMIT = "24cb4edc"  # the branch base this feature is delivered against
SURFACES = (
    "skills/external/create-docs/SKILL.md",
    "skills/external/improve-docs/SKILL.md",
    "templates/commands/docs.md",
)


def engine_names() -> set[str]:
    """The six engine layer names, read out of the routing matrix's value table."""
    text = ROUTING_MATRIX.read_text(encoding="utf-8")
    section = text.split("### 0.2", 1)[1].split("### 0.3", 1)[0]
    names = set()
    for line in section.splitlines():
        match = re.match(r"^\|\s*`([a-z0-9]+)`\s*\|", line)
        if match:
            names.add(match.group(1))
    assert len(names) >= 6, f"routing matrix's engine table did not parse: {sorted(names)}"
    return names


def tracked_files() -> list[str]:
    """Every tracked text file under the scanned roots, as repository-relative POSIX paths."""
    proc = subprocess.run(["git", "ls-files", "-z", *SCANNED_ROOTS], cwd=REPO_ROOT,
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return sorted(p for p in proc.stdout.split("\0") if p)


def files_changed_by_this_feature(roots: tuple[str, ...]) -> list[str]:
    """Tracked files under `roots` that this feature's branch changed since the base commit."""
    proc = subprocess.run(["git", "diff", "--name-only", f"{BASE_COMMIT}...HEAD", "--", *roots],
                          cwd=REPO_ROOT, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return sorted(line for line in proc.stdout.splitlines() if line)


def files_changed_in_worktree(roots: tuple[str, ...]) -> list[str]:
    """Tracked files under `roots` changed in the working tree (the stage's findings are not committed yet)."""
    proc = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", *roots],
                          cwd=REPO_ROOT, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return sorted(line for line in proc.stdout.splitlines() if line)


_COMPILED_BANNER = "<!-- AUTO-GENERATED"


def _authored_lines(rel: str) -> list[str] | None:
    """The text this feature CONTRIBUTED to ``rel``, excluding machine-owned compiled lines.

    The claim below is about what the feature *authored*, so a whole-file read is the wrong
    reading: a file the feature only touched by recompiling the Wrap-up banner still carries
    whatever its body said before, and judging that body would indict the feature for a
    sentence it never wrote. Measured 2026-11-07 on the merged tree: `run-team/SKILL.md`
    differs from `BASE_COMMIT` by exactly one compiled banner line, yet a whole-file read
    reported `['mermaid', 'plantuml']` — names that were already on that line at the base
    commit and belong to 063's engine-face contract, not to this feature.

    So the scan reads the union of the hunks' *added* lines from the base commit and from the
    working tree, dropping the compiled banner (machine-owned, never authored).
    """
    added: list[str] = []
    for rev_range in (f"{BASE_COMMIT}...HEAD", "HEAD"):
        proc = subprocess.run(
            ["git", "diff", "-U0", rev_range, "--", rel],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        assert proc.returncode == 0, proc.stderr
        for line in proc.stdout.splitlines():
            if not line.startswith("+") or line.startswith("+++"):
                continue
            body = line[1:]
            if body.lstrip().startswith(_COMPILED_BANNER):
                continue
            added.append(body)
    return added


@pytest.mark.contract
def test_sc005_no_second_engine():
    """No second drawing engine, renderer entry point, or engine-selection table was introduced.

    The scan is bounded twice, so it says something about **this feature** rather than about the repository:
    the candidate set is the files this branch changed under `templates/`, `skills/`, `shared/` and `scripts/`
    (draw-diagram's own tree excluded — it is the owner of the engine names, not a copy of them), and a file
    counts as a hit only when it names engine layers alongside router vocabulary. Pre-existing engine
    enumerations elsewhere in the repository are untouched by this delivery and are not its claim to make.

    red-when: a file this feature changed outside draw-diagram's tree names two or more engine layers alongside
    router vocabulary, i.e. it added a second engine-selection surface.
    """
    names = engine_names()
    router_words = ("routing matrix", "路由矩阵", "tie-break", "引擎层", "engine layer")
    changed = [rel for rel in sorted(set(files_changed_by_this_feature(SCANNED_ROOTS))
                                      | set(files_changed_in_worktree(SCANNED_ROOTS)))
               if not rel.startswith(DRAW_DIAGRAM_TREE)]
    assert changed, "the premise: this feature changed at least one file under the scanned roots"
    hits = []
    for rel in changed:
        path = REPO_ROOT / rel
        if not path.is_file():
            continue
        try:
            body = path.read_text(encoding="utf-8").lower()
        except (OSError, UnicodeDecodeError):
            continue
        mentioned = {name for name in names if re.search(rf"\b{re.escape(name)}\b", body)}
        if len(mentioned) >= 2 and any(word in body for word in router_words):
            hits.append(f"{rel}: mentions {sorted(mentioned)}")
    assert not hits, (
        "a second engine-selection surface appeared outside draw-diagram's own tree:\n" + "\n".join(hits)
    )


@pytest.mark.contract
def test_sc005_surfaces_reach_by_reference():
    """Every diagram-producing surface reaches the capability by reference, never by a copy of its rows.

    Two readings, deliberately different in kind. The **pointer** reading is unconditional: each of the three
    surfaces must reach `skills/external/draw-diagram` by path once this feature's pointer text has landed —
    that is what makes the capability findable from the document flows. The **no-restatement** reading is
    the one that holds today and must keep holding: a surface that names two or more engine layers is carrying
    a routing table, and one that defines `ldm_summary` as a field is carrying the semantic model.

    red-when: a surface loses the pointer, or grows a copied routing row / `ldm_summary` schema.
    """
    names = engine_names()
    for rel in SURFACES:
        path = REPO_ROOT / rel
        body = path.read_text(encoding="utf-8")
        assert "skills/external/draw-diagram" in body, (
            f"{rel} is a diagram-producing surface and must reach the capability by path "
            f"(the pointer text is this feature's delivery, not the routing rules themselves)"
        )
        lowered = body.lower()
        mentioned = {name for name in names if re.search(rf"\b{re.escape(name)}\b", lowered)}
        assert len(mentioned) < 2, (
            f"{rel} names {sorted(mentioned)} — two or more engine layers is a restated routing table, "
            f"not a reference"
        )
        assert "ldm_summary:" not in body, f"{rel} restates the semantic-model summary schema"


@pytest.mark.contract
def test_sc005_engine_domain_is_single_owner():
    """This feature added no second enumeration of the engine layers.

    The inventory half of `SC-005`, read as a change-scoped inventory: whatever the repository already carries
    inside draw-diagram's own tree belongs to that capability's owner, and the contract's `C-010` example is a
    schema illustration. What matters for this delivery is that no file it touched added one, so the assertion
    reads the changed-file set and pins the verdict on the code this feature authored.

    The population and the claim are kept apart on purpose. The **population** is every tracked file under the
    scanned roots — non-empty, so an empty read means the scan broke rather than that the claim held. The
    **claim** is about the subset this feature actually authored: files whose own text (not a test's fixture
    string, not this capability's owner tree) enumerates two or more engine layers. That subset must be empty
    both because no such file exists today and because the assertion has to be able to say so out loud instead
    of failing on a vacuous premise.

    red-when: a file this feature changed enumerates two or more engine layers, i.e. it published a second
    engine list.
    """
    names = engine_names()
    population = tracked_files()
    assert population, "the premise: the scanned roots carry tracked files to inventory"

    # `docs-utils.py` carries the `.mmd` / `.puml` *file suffixes* a diagram reference may name. A suffix is not
    # an engine layer, and its own obligation block cites the engine names it reads out of a record; neither is a
    # second enumeration. `tests/` is this feature's evidence, not a surface a reader consults to pick an engine.
    allowed_paths = {"skills/external/create-docs/scripts/docs-utils.py"}
    allowed_prefixes = (DRAW_DIAGRAM_TREE, ".specify/skills/draw-diagram/", "tests/")
    authored = [rel for rel in sorted(set(files_changed_by_this_feature(SCANNED_ROOTS))
                                      | set(files_changed_in_worktree(SCANNED_ROOTS)))
                if rel not in allowed_paths and not rel.startswith(allowed_prefixes)]
    assert set(authored) <= set(population), "the scan reported files outside the scanned roots: " + str(
        sorted(set(authored) - set(population)))

    carriers = []
    for rel in authored:
        path = REPO_ROOT / rel
        if not path.is_file():
            continue
        # Only the lines this feature wrote are judged — see `_authored_lines`.
        lowered = "\n".join(_authored_lines(rel)).lower()
        mentioned = {name for name in names if re.search(rf"\b{re.escape(name)}\b", lowered)}
        if len(mentioned) >= 2:
            carriers.append(f"{rel}: {sorted(mentioned)}")
    assert not carriers, "an engine enumeration was added outside draw-diagram's tree:\n" + "\n".join(carriers)


# ---------------------------------------------------------------------------
# SC-007 — the traceability-record guard (four faces, and engine stickiness)
# ---------------------------------------------------------------------------

FOUR_FACES = ("engine", "engine_reason", "ldm_summary", "delivery")


@pytest.mark.integration
@pytest.mark.parametrize("face", FOUR_FACES)
def test_record_carries_the_four_faces(tmp_path: Path, face: str):
    """A produced diagram's record entry decides four things; losing any one makes it unjudgeable.

    The four are the producing run's own answers (`engine` and `engine_reason` from the routing decision,
    `ldm_summary` from the semantic model, `delivery.accepted` from the delivery self-check). A record that is
    missing one did not decide that question, so the checker cannot accept the diagram: the reading must be
    `not-evaluated` / `trace-incomplete`, never `satisfied`.

    red-when: a record missing one of the four still satisfies the obligation, i.e. the field was treated as
    optional by the reader.
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    record_file = Path(record_arg(space))
    payload = json.loads(record_file.read_text(encoding="utf-8"))
    entry = payload["diagrams"][0]
    assert face in entry, f"premise: the fixture record carries {face!r}"
    if face == "delivery":
        entry["delivery"].pop("accepted")
    else:
        entry.pop(face)
    record_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    assert verdict_of(obligation(space, "--record", str(record_file)), DOC) == (
        "not-evaluated", "trace-incomplete"), f"a record without {face!r} must not be accepted"


@pytest.mark.integration
def test_engine_sticky_on_update(tmp_path: Path):
    """Re-rendering an existing diagram reuses the engine the record already names; it never re-routes it.

    `data-model.md` E2's invariant in executable form: the record's `engine` / `engine_reason` survive an update
    of the same diagram, and the judgement does not depend on the engine whatsoever — the checker reads the
    record, it does not choose. Both readings are taken: the payload is unchanged when the record is rewritten
    in place with a refreshed render (same engine), and the checker's verdict is independent of the engine name
    the record carries.

    red-when: updating the diagram changes the engine field (re-routing), or the verdict moves when only the
    engine name changes (the checker would then be routing, which `FR-010` forbids it).
    """
    space = fixtures.copy_fixture("clean", tmp_path)
    record_file = Path(record_arg(space))
    before = json.loads(record_file.read_text(encoding="utf-8"))
    engine_before = before["diagrams"][0]["engine"]
    reason_before = before["diagrams"][0]["engine_reason"]
    verdict_before = verdict_of(obligation(space, "--record", str(record_file)), DOC)

    # an update: the rendered face is re-emitted, the record's digest refreshed, the engine kept
    rendered = space / "docs" / "assets" / "widget.svg"
    rendered.write_text(rendered.read_text(encoding="utf-8") + "<!-- re-rendered -->\n", encoding="utf-8")
    updated = json.loads(record_file.read_text(encoding="utf-8"))
    entry = updated["diagrams"][0]
    import hashlib

    for face in entry["rendered"]:
        if face["path"] == "docs/assets/widget.svg":
            face["sha256"] = hashlib.sha256(rendered.read_bytes()).hexdigest()
    record_file.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")

    after = json.loads(record_file.read_text(encoding="utf-8"))
    assert after["diagrams"][0]["engine"] == engine_before, "an update MUST NOT re-route the engine"
    assert after["diagrams"][0]["engine_reason"] == reason_before, (
        "the routing reason is sticky with the engine"
    )
    assert verdict_of(obligation(space, "--record", str(record_file)), DOC) == verdict_before, (
        "refreshing the digest is not a stale state: the update leaves the verdict where it was"
    )

    reengineered = json.loads(record_file.read_text(encoding="utf-8"))
    reengineered["diagrams"][0]["engine"] = "engine-not-in-the-routing-matrix"
    record_file.write_text(json.dumps(reengineered, indent=2) + "\n", encoding="utf-8")
    assert verdict_of(obligation(space, "--record", str(record_file)), DOC) == verdict_before, (
        "the checker reads the record; it does not route, so the engine name cannot move the verdict"
    )
