"""Contract test: self-explanatory documents reach a client project (Feature 082, US3).

Implements C-26 of
``.specify/specs/082-self-explanatory-integration/contracts/mirror-distribution.contract.md``:
the three owner documents MUST arrive in a fresh project through the same two steps every
framework document uses — mirror, then ``specify init``.

Why three layers, and why the real CLI runs in the last one
-----------------------------------------------------------
C-26's subject is the *installed entry point*, so a test that reads the repository's own
``.specify/shared/`` tree would prove nothing (C-25: a mirror-only file is never "distributed").
This module therefore asserts the same proposition three times, each at a strictly weaker premise
than the one above it:

1. **Entry point exists** — a ``.venv`` can be created and ``pip install -e <repo>`` succeeds. If
   either half is unavailable the check reports ``ANOMALY:`` (T029's own instruction) and skips
   rather than passing: "the interpreter cannot build the entry point" is not evidence that the
   documents ship.
2. **End-to-end** — the ``specify`` console script built from *this working tree* runs
   ``init --here`` in a temporary project, and each of the three paths is asserted present.
3. **Reach** — the same packaged entry point, asked in-process for its resource root (the very
   value ``copy_local_templates`` copies ``shared/`` from), resolves to a tree that carries all
   three documents. Layer 3 exists because layer 2's green could otherwise be produced by a path
   the copy section does not take. Two layouts are accepted and named in its report: a built wheel
   (root == ``MODULE_DIR``) and an editable install (root == ``MODULE_DIR.parent.parent``, the repo
   root whose ``templates/`` makes ``get_resource_path``'s fallback fire). Any third value fails
   rather than skips.

Red-first provenance (Constitution IV): the RED this module captures was recorded before the
artifacts landed — three ``MISS`` lines from the mirror engine and "absent in ``.specify/shared/``"
from the tree — in
``.specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md`` § R-2. The red is
attributable to the missing documents; no assertion here can fail as an import or collection error.

Known limit, stated rather than hidden
-------------------------------------
C-26's contract text speaks of "the installed entry point". An editable install resolves the
module to *this checkout*, so layer 2 proves the distribution **mechanism** (packaging manifest ->
resource root -> copy section -> client ``.specify/shared/``) over the current working tree, not
that a released wheel on PyPI already carries the documents. That second fact is owned by the
release, not by this repository; the plan stage measured it — the pre-installed ``/usr/local/bin/
specify`` is ``partial`` and its packaged resources predate this feature
(``tasks.md`` § Environment Prerequisites). Encoding that stale install as an exemption is exactly
what T029 forbids, so this module does not read the ambient CLI at all: it builds its own.

No second pair table (C-22/One Source Of Truth): the three paths below are the *contract's* subject
list, not a mirror enumeration. The mirror enumeration stays in the engine's ``MIRROR_PAIRS``; the
mirror-parity suite derives its parameters from there.

The second half of this module (``C-27``, T034) turns the same question around: the repository's
``docs/concepts/self-explanatory.md`` pointer page names the owner paths in inline code, and every one
of those names must resolve on **both** sides of the mirror. It reuses this module's pytest surface
rather than starting a link-checking engine (FR-012), and it derives the source→mirror mapping from
the engine's ``MIRROR_PAIRS`` instead of restating it.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]

# C-26's subject list, verbatim from the contract (client-side runtime paths).
DISTRIBUTED_PATHS = (
    ".specify/shared/definitions/self-explanatory-definitions.md",
    ".specify/shared/guidelines/self-explanatory.md",
    ".specify/shared/workflow/best-practice-optimization.md",
)


def _load_cli_module():
    """Import ``specify_cli`` from this working tree.

    The CLI module carries package-relative imports (``from . import _provenance``), so a
    by-path load fails; the house idiom used by ``test_capability_matrix_contract.py`` and
    ``test_upgrade_end_state.py`` — ``src/`` on ``sys.path``, then a normal import — is the
    correct shape here.
    """
    src = ROOT / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    import specify_cli  # noqa: PLC0415 - deliberate late import, see docstring

    assert Path(specify_cli.__file__).resolve().parent == (src / "specify_cli"), (
        f"imported specify_cli from {specify_cli.__file__}, not from this working tree"
    )
    return specify_cli


CLI = _load_cli_module()


def _absent(project: Path) -> list[str]:
    return [rel for rel in DISTRIBUTED_PATHS if not (project / rel).is_file()]


# --------------------------------------------------------------------------- #
# Layer 1 — the entry point can be built from this working tree
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def entry_point(tmp_path_factory) -> dict:
    """Create an isolated venv and install this working tree into it (editable).

    Isolation is deliberate: the interpreter that runs pytest may already carry a released
    ``specify-cli``, and inheriting it would make the test run the stale CLI that T029 forbids as
    evidence. No ``--system-site-packages`` is used, so the distribution dependencies must come
    from the package metadata — which is itself part of what "shippable" means.

    The build is offline-friendly (no index access is needed when the dependencies are already
    resolvable) but is NOT forced offline: a cold host may fetch wheels, and the call is allowed
    the whole 10-minute budget the dispatch brief grants it.
    """
    root = tmp_path_factory.mktemp("c26-entry-point")
    venv_dir = root / ".venv"
    repo = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    repo_root = Path(repo.stdout.strip() or ROOT) if repo.returncode == 0 else ROOT

    def _record(payload: dict) -> Path:
        path = root / "c26-entry-point.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    records: list[str] = []

    cmd = [sys.executable, "-m", "venv", str(venv_dir)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    records.append(f"$ {' '.join(cmd)}\nrc={proc.returncode}\n{proc.stdout}{proc.stderr}")
    if proc.returncode != 0:
        _record({"available": False, "stage": "venv", "log": records})
        pytest.skip(
            f"ANOMALY: cannot create a venv with {sys.executable} (rc={proc.returncode}); "
            "C-26's entry point is unavailable on this host"
        )

    venv_python = venv_dir / "bin" / "python"
    if not venv_python.is_file():
        _record({"available": False, "stage": "venv-python", "log": records})
        pytest.skip(
            f"ANOMALY: {venv_dir} carries no bin/python (Windows-style layout?); "
            "C-26's entry point is unavailable on this host"
        )

    cmd = [str(venv_python), "-m", "pip", "install", "-e", str(repo_root)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=540)
    records.append(f"$ {' '.join(cmd)}\nrc={proc.returncode}\n{proc.stdout}{proc.stderr}")
    if proc.returncode != 0:
        _record({"available": False, "stage": "pip-install", "log": records})
        pytest.skip(
            "ANOMALY: `pip install -e` of the working tree failed "
            f"(rc={proc.returncode}); C-26's entry point is unavailable on this host. Tail:\n"
            f"{proc.stdout[-1200:]}{proc.stderr[-1200:]}"
        )

    specify_bin = venv_dir / "bin" / "specify"
    record_path = _record(
        {
            "available": True,
            "repo_root": str(repo_root),
            "venv": str(venv_dir),
            "log": records,
        }
    )
    return {
        "root": root,
        "venv": venv_dir,
        "python": venv_python,
        "specify": specify_bin,
        "record": record_path,
    }


# --------------------------------------------------------------------------- #
# Layer 2 — C-26: `specify init` on the installed entry point distributes the three documents
# --------------------------------------------------------------------------- #
def test_c26_specify_init_distributes_the_three_documents(entry_point, tmp_path):
    """C-26: a fresh project created by the installed entry point carries all three documents."""
    project = tmp_path / "client"
    project.mkdir()

    cmd = [
        str(entry_point["specify"]),
        "init",
        "--here",
        "--ai",
        "claude",
        # The dispatch brief's exact flags (--no-git, --skip-tls) plus the one this environment
        # needs: the claude tier reports `requires_cli` and this host has no agent CLI. Without
        # it init aborts for an unrelated reason and would prove nothing about distribution.
        "--no-git",
        "--skip-tls",
        "--ignore-agent-tools",
    ]
    env = dict(os.environ)
    env.pop("VIRTUAL_ENV", None)  # the console script must not re-enter the pytest env
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    proc = subprocess.run(
        cmd, cwd=project, capture_output=True, text=True, timeout=300, env=env
    )

    report = {
        "command": " ".join(cmd),
        "cwd": str(project),
        "rc": proc.returncode,
        "paths": {rel: (project / rel).is_file() for rel in DISTRIBUTED_PATHS},
        "sizes": {
            rel: (project / rel).stat().st_size
            for rel in DISTRIBUTED_PATHS
            if (project / rel).is_file()
        },
        "entry_point_record": str(entry_point["record"]),
    }
    record = entry_point["root"] / "c26-init-report.json"
    record.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    assert proc.returncode == 0, (
        f"`{' '.join(cmd)}` failed with rc={proc.returncode}; C-26 cannot be judged. "
        f"stderr tail:\n{proc.stderr[-2000:]}"
    )

    missing = _absent(project)
    assert not missing, (
        "C-26: `specify init` distributed only "
        f"{len(DISTRIBUTED_PATHS) - len(missing)}/{len(DISTRIBUTED_PATHS)} documents; missing:\n  "
        + "\n  ".join(missing)
        + f"\nreport: {record}"
    )

    # Distribution must not be a byte-mangling copy: the documents travel through
    # `copy_tree_with_rewrite`, which rewrites source-form path prefixes. A document that
    # arrives empty or truncated would satisfy presence but not distribution.
    for rel in DISTRIBUTED_PATHS:
        assert report["sizes"][rel] > 0, f"{rel} arrived empty in the client project"


def test_c26_an_absent_document_fails_this_clause(tmp_path):
    """Anti-vacuity companion: the presence test above can actually fail.

    Builds the exact client layout that would exist if one document never shipped and asserts the
    module-level presence check reports it. Without this, a typo in ``DISTRIBUTED_PATHS`` or an
    always-true file test would keep C-26 green on a broken tree.
    """
    project = tmp_path / "would-be-client"
    for rel in DISTRIBUTED_PATHS[:2]:
        (project / rel).parent.mkdir(parents=True, exist_ok=True)
        (project / rel).write_text("present\n", encoding="utf-8")

    assert _absent(project) == [DISTRIBUTED_PATHS[2]], (
        "the presence check must name the one document that is missing"
    )


# --------------------------------------------------------------------------- #
# Layer 3 — the entry point's resource root carries the documents the copy section reads
# --------------------------------------------------------------------------- #
def test_c26_entry_point_resource_root_carries_the_three_documents(entry_point):
    """The packaged ``shared/`` tree is the distribution input — and it must carry all three.

    ``copy_local_templates`` copies ``shared/`` from ``get_resource_path()``; this asserts that
    root, so the clause holds even if a future init flow changes its copy call. The in-process
    read of ``MODULE_DIR`` mirrors ``get_resource_path``'s first branch exactly, and is performed
    through the *entry-point* interpreter so nothing about the host's environment can leak in.
    """
    probe = (
        "import json, specify_cli\n"
        "print(json.dumps({'module_dir': str(specify_cli.MODULE_DIR),\n"
        "                  'resource_path': str(specify_cli.get_resource_path())}))\n"
    )
    proc = subprocess.run(
        [str(entry_point["python"]), "-c", probe],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=entry_point["root"],
    )
    assert proc.returncode == 0, (
        "the installed entry point could not report its resource root; C-26's distribution "
        f"input is unknown. stderr tail:\n{proc.stderr[-2000:]}"
    )
    payload = json.loads(proc.stdout.strip().splitlines()[-1])
    # How the entry point locates its resources, measured rather than assumed:
    #
    #   * a built wheel puts the force-included trees at ``specify_cli/templates`` etc., so
    #     ``get_resource_path`` returns ``MODULE_DIR`` — the installed package carries them;
    #   * an editable install leaves ``specify_cli.__file__`` at ``<repo>/src/`` via a ``.pth``
    #     while the build's force-include materialised ``<repo>/src/specify_cli/{templates,
    #     shared,...}`` — a SIBLING of the module dir, not inside it. So ``MODULE_DIR/templates``
    #     is absent and ``get_resource_path`` takes its source-checkout fallback.
    #
    # Both layouts are legitimate; what C-26 requires is that the resource root the copy section
    # actually reads carries the documents. Assert that for whichever layout this host produced,
    # and record which one it was, rather than skipping the editable case as unjudgeable.
    resource_path = Path(payload["resource_path"])
    module_dir = Path(payload["module_dir"])
    # Editable layout: ``specify_cli.__file__`` stays under ``<repo>/src/`` while the build's
    # force-include materialised ``<repo>/src/specify_cli/{templates,shared,...}``. So
    # ``MODULE_DIR/templates`` is absent, the source-checkout fallback fires, and
    # ``get_resource_path`` returns ``MODULE_DIR.parent.parent`` — the repo root, not ``src/``.
    checkout_root = module_dir.parent.parent

    assert payload["resource_path"] not in {"", "None"}, (
        "the installed entry point reports no resource root; C-26's distribution input is "
        "unknown"
    )

    if resource_path == module_dir:
        layout = "packaged wheel (resource root == MODULE_DIR)"
    elif resource_path == checkout_root:
        layout = "editable install (resource root == MODULE_DIR.parent.parent, the repo root)"
    else:
        pytest.fail(
            f"resource root {resource_path} is neither MODULE_DIR ({module_dir}) nor the repo "
            f"root of an editable install ({checkout_root}); the two known layouts are a built "
            "wheel and an editable install. C-26's premise changed — re-measure before trusting "
            "this clause."
        )

    report = entry_point["root"] / "c26-resource-root.json"
    report.write_text(
        json.dumps(
            {
                "module_dir": str(module_dir),
                "resource_path": str(resource_path),
                "layout": layout,
                "paths": {
                    rel: (resource_path / rel[len(".specify/"):]).is_file()
                    for rel in DISTRIBUTED_PATHS
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    absent = [
        rel for rel in DISTRIBUTED_PATHS if not (resource_path / rel[len(".specify/"):]).is_file()
    ]
    assert not absent, (
        f"the entry point's resource root does not carry: {', '.join(absent)} "
        f"\nlayout: {layout}\nroot: {resource_path}\nreport: {report}"
    )


# --------------------------------------------------------------------------- #
# C-28 face — distribution is not wiring
# --------------------------------------------------------------------------- #
def test_c28_distribution_is_not_wiring():
    """C-28's assertion is that this CLAUSE asserts nothing about ``/speckit.improve``.

    Recorded as an executable statement of scope rather than a comment: the optimization-workflow
    document is distributed as a *document*, and no command template consults it. The wiring
    question is ``OI-082-01`` and lives outside this feature.
    """
    improve = ROOT / "templates" / "commands" / "improve.md"
    if improve.is_file():
        assert "best-practice-optimization" not in improve.read_text(encoding="utf-8"), (
            "templates/commands/improve.md now references the optimization-workflow document; "
            "that is OI-082-01's wiring, not this feature's distribution"
        )

    # And the distributed subject really is a document, not a wired engine action.
    for rel in DISTRIBUTED_PATHS:
        assert rel.endswith(".md"), f"{rel} is not a document path"


# --------------------------------------------------------------------------- #
# C-27 — the docs page's pointers resolve, on both sides of the mirror (T034)
# --------------------------------------------------------------------------- #
DOCS_PAGE = ROOT / "docs" / "concepts" / "self-explanatory.md"

# C-27's "at minimum" floor, taken from the contract clause itself (not from the page, or the
# assertion would be circular): the framework-source concept owner ``STR-002`` and the
# optimization-workflow owner. Both are framework-source paths, so both must resolve in source AND
# in the mirror tree.
C27_REQUIRED_PATHS = (
    "shared/definitions/self-explanatory-definitions.md",
    "shared/workflow/best-practice-optimization.md",
)

# C-27's one escape hatch: a referenced path that legitimately has no mirror, listed explicitly
# with the reason it is exempt from the mirror half. It is an ALLOW-LIST of paths whose mirror
# halves are exempt — never a suppression of the source-tree half, and never a place to hide a
# missing owner document.
C27_MIRROR_EXEMPTIONS = {
    # Reason: `docs/` is this project's development documentation and is NOT distributed
    # (`AGENTS.md` § Documentation Map); it has no pair in the engine's MIRROR_PAIRS, so a path
    # under docs/ resolves in the source tree only. Kept explicit so the next docs-internal link
    # is a visible decision rather than a silent gap. Currently empty by measurement, not by
    # omission — the page names no docs-internal path today.
}

# A repository-relative .md path written in inline code is a code span whose whole content is the
# path. Restricting the span to path characters keeps prose mentions and absolute paths out.
_INLINE_MD_PATH = re.compile(r"`((?!/)[\w][\w./-]*\.md)`")


def _load_mirror_engine():
    """Load the mirror engine the same way ``test_mirror_parity_suite.py`` does.

    The engine owns ``MIRROR_PAIRS``; deriving the source→mirror mapping from it is what keeps
    this guard from becoming a second pair table (C-22 / One Source Of Truth).
    """
    import importlib.util  # noqa: PLC0415 - local import keeps the module's top import list small

    path = ROOT / "scripts" / "python" / "sync-mirrors.py"
    spec = importlib.util.spec_from_file_location("_sync_mirrors_c27_engine", path)
    assert spec is not None and spec.loader is not None, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SYNC_MIRRORS = _load_mirror_engine()


def _mirror_of(rel_path: str) -> tuple[str, str] | None:
    """Map a repo-relative path to ``(source_root, mirror_root)``; ``None`` if it has no pair.

    The engine's pairs are (source_dir, mirror_dir) with the file's path relative to the source
    dir preserved in the mirror. A path outside every source dir therefore has no mirror.
    """
    for src_name, dst_name, _strict, exclude_parts in SYNC_MIRRORS.MIRROR_PAIRS:
        if rel_path == src_name or not rel_path.startswith(src_name + "/"):
            continue
        if any(part in exclude_parts for part in rel_path.split("/")):
            continue
        return src_name, dst_name
    return None


def docs_page_paths(page_text: str) -> list[str]:
    """Every repository-relative ``.md`` path written in inline code, in page order, deduplicated.

    ``docs_page_paths`` is deliberately a plain function over text (not a path): the M-6 mutation
    leg feeds it a mutated COPY's text, so the leg exercises the real extractor rather than
    re-typing its regex.
    """
    seen: dict[str, None] = {}
    for match in _INLINE_MD_PATH.finditer(page_text):
        seen.setdefault(match.group(1), None)
    return list(seen)


def unresolved_docs_page_paths(page_text: str) -> list[str]:
    """Return one human-readable line per pointer that does not resolve where C-27 requires.

    The return value is the assertion's whole subject: an empty list means every extracted path
    resolves in the source tree and — unless explicitly exempted — in its mirror tree.
    """
    problems: list[str] = []
    for rel_path in docs_page_paths(page_text):
        if not (ROOT / rel_path).is_file():
            problems.append(f"{rel_path}: MISSING in the source tree")
            continue
        if rel_path in C27_MIRROR_EXEMPTIONS:
            continue
        pair = _mirror_of(rel_path)
        if pair is None:
            problems.append(
                f"{rel_path}: resolves in the source tree but belongs to no mirror pair, and it is "
                "not in C27_MIRROR_EXEMPTIONS — either it has a mirror, or the exemption (with its "
                "one-line reason) belongs in that allow-list"
            )
            continue
        _src_name, dst_name = pair
        mirror_path = ROOT / dst_name / rel_path.split("/", 1)[1]
        if not mirror_path.is_file():
            problems.append(f"{rel_path}: MISSING in its mirror tree ({mirror_path})")
    return problems


def test_c27_docs_page_names_both_required_owner_paths():
    """C-27's floor: the page really carries the two owner pointers the clause names.

    Separated from the resolution test so a page that resolves its (empty) set of pointers cannot
    pass: this asserts the subject list is non-empty before extraction can.
    """
    assert DOCS_PAGE.is_file(), (
        f"C-27's subject page is absent: {DOCS_PAGE}. `docs/concepts/self-explanatory.md` is the "
        "pointer page the feature delivers; a missing page is not an empty one"
    )
    found = docs_page_paths(DOCS_PAGE.read_text(encoding="utf-8"))
    for required in C27_REQUIRED_PATHS:
        assert required in found, (
            f"docs/concepts/self-explanatory.md does not name {required!r} in inline code; it "
            f"names {found}. C-27 requires at least the concept owner (STR-002) and the "
            "optimization-workflow owner"
        )


def test_c27_docs_page_pointers_resolve_in_source_and_mirror():
    """C-27: every inline ``.md`` path on the page resolves in source AND in its mirror tree."""
    problems = unresolved_docs_page_paths(DOCS_PAGE.read_text(encoding="utf-8"))
    assert not problems, (
        "C-27: the docs page carries pointers that do not resolve:\n  "
        + "\n  ".join(problems)
        + f"\npage: {DOCS_PAGE}\nextracted: {docs_page_paths(DOCS_PAGE.read_text(encoding='utf-8'))}"
        f"\nexemptions: {sorted(C27_MIRROR_EXEMPTIONS)}"
    )


def test_c27_extraction_is_not_vacuous():
    """Anti-vacuity: the extractor really finds paths, and really reports a broken one.

    Without this, a typo in ``_INLINE_MD_PATH`` would make the resolution test above pass on an
    empty list forever. Both halves run on synthetic text — no repository file is read here.
    """
    sample = (
        "Owner: `shared/definitions/self-explanatory-definitions.md` and "
        "`shared/definitions/absent-by-construction.md`.\n"
        "Not a path: `npm run build`, `/absolute/path.md`, and shared/outside-code.md.\n"
    )
    extracted = docs_page_paths(sample)
    assert extracted == [
        "shared/definitions/self-explanatory-definitions.md",
        "shared/definitions/absent-by-construction.md",
    ], f"the extractor must take inline whole-span .md paths only; it took {extracted}"

    problems = unresolved_docs_page_paths(sample)
    # Exactly the absent one is reported: the synthetic sample's other pointer is the real owner
    # path, so a guard that also flagged a resolving path would be wrong in the other direction.
    assert len(problems) == 1 and "absent-by-construction.md: MISSING in the source tree" in problems[0], (
        "the resolution check must report the absent pointer and only that one; "
        f"it reported {problems}"
    )


def test_c27_docs_page_does_not_restate_the_owner_body():
    """C-27 / FR-012: the page is a POINTER page, not a second copy of the owner's definition.

    The decidable form of "reference, not copy" that C-20 already established: the owner's own
    level-2 heading text must not appear on the page. Prose may be reworded; a heading transplanted
    from the definition file is a copy.
    """
    owner = ROOT / "shared" / "definitions" / "self-explanatory-definitions.md"
    assert owner.is_file(), f"the concept owner is absent, so this page cannot be judged: {owner}"
    owner_headings = {
        line[3:].strip()
        for line in owner.read_text(encoding="utf-8").splitlines()
        if line.startswith("## ")
    }
    page_text = DOCS_PAGE.read_text(encoding="utf-8")
    transplanted = sorted(h for h in owner_headings if h and f"## {h}" in page_text)
    assert not transplanted, (
        "docs/concepts/self-explanatory.md restates the owner's heading(s) "
        f"{transplanted}; the page points at the owner and MUST NOT copy its body (C-27/FR-012)"
    )


def _tree_digest(root: Path) -> dict[str, str]:
    import hashlib  # noqa: PLC0415 - only needed by the mutation legs

    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_m6_docs_pointer_removal_turns_c27_red(tmp_path):
    """Mutation leg M-6: delete one owner pointer from a COPY of the page; the guard goes red.

    Implements the contract's M-6 row: "Delete the ``STR-002`` inline path from a copy of the docs
    page and run the link guard against the copy" → C-27's path extraction → existence assertion
    must go red. The leg calls the module's own ``unresolved_docs_page_paths`` and
    ``docs_page_paths`` over the mutated text, so it exercises the real assertion rather than a
    paraphrase of it.

    The real page is never the subject: its digest is taken before and after, and the temp copy
    lives under pytest's own temporary root.
    """
    before = _tree_digest(DOCS_PAGE.parent)
    original = DOCS_PAGE.read_text(encoding="utf-8")
    subject = C27_REQUIRED_PATHS[0]  # the concept owner, STR-002
    assert subject in original, (
        f"the mutation's subject {subject!r} is not on the page; the leg would be vacuous"
    )

    copy = tmp_path / DOCS_PAGE.name
    mutated = original.replace(f"`{subject}`", "`shared/definitions/removed-by-m6.md`", 1)
    assert mutated != original, "the M-6 mutation did not take effect"
    copy.write_text(mutated, encoding="utf-8")

    # The extractor still finds pointers on the copy — the leg breaks RESOLUTION, not extraction.
    extracted = docs_page_paths(copy.read_text(encoding="utf-8"))
    assert subject not in extracted, (
        f"the deleted pointer is still extracted from the copy: {extracted}"
    )

    # C-27's resolution assertion turns red — the exact `assert not problems` line the real guard
    # runs, applied to the copy. Green here would mean the leg proves nothing.
    problems = unresolved_docs_page_paths(copy.read_text(encoding="utf-8"))
    assert problems, (
        "M-6 did not turn C-27 red: with the concept-owner pointer deleted, the guard must report "
        f"the missing path. Extracted from the copy: {extracted}"
    )
    assert any("removed-by-m6.md" in p for p in problems), (
        f"the red must name the path the mutation introduced (C-24's re-runnability rule applied "
        f"here); it reported {problems}"
    )

    # Anti-vacuity: the SAME guard is green on the same page as it stands in the repository.
    assert not unresolved_docs_page_paths(original), (
        "C-27 is red on the unmutated page, so this leg proves nothing about the mutation"
    )

    # The repository page is untouched by the leg.
    assert _tree_digest(DOCS_PAGE.parent) == before, (
        "the M-6 leg modified docs/concepts/; mutation legs operate on temp copies only"
    )
    assert copy.is_file() and copy.parent == Path(tmp_path)
