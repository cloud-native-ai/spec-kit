"""T005 — build the eleven `docs-obligation` fixture spaces on disk.

Ownership: this module is the **builder and the registry** of the eleven spaces `data-model.md` E6 names.
It exists so the spaces are reproducible (delete the directories, re-run this file) and so their shared
miniature-documentation-space skeleton has exactly one definition — the eleven directories themselves are the
committed artifacts, `data-model.md` E6 is the owner of *what each one must contain*.

Run:  /usr/bin/python3 tests/fixtures/docs-obligation/build_fixtures.py
Check (CI-safe, writes nothing):  /usr/bin/python3 tests/fixtures/docs-obligation/build_fixtures.py --check

E6 invariant this builder honours: the repository copy of every space IS its registered state. Nine spaces
are registered as red (`deleted-rendered/`, `orphan-rendered/`, `orphan-source/`, `no-diagram/`, `no-trace/`,
`trace-incomplete/`, `exempt-bad/`, `exempt-superseded/` and `stale-source/` whose mtime step lives in
`conftest.py`); only `clean/` and `exempt-ok/` are green. A writing or deleting test case therefore copies a
space into `tmp_path` first — the repository copy is never mutated.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

TYPE_DIRS = ("concepts", "tutorials", "tasks", "reference", "decisions", "contribute")

DOC_PATH = "docs/concepts/widget-overview.md"
SOURCE_PATH = "docs/assets/widget.mmd"
SVG_PATH = "docs/assets/widget.svg"
PNG_PATH = "docs/assets/widget.png"
RECORD_PATH = "docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json"
EXEMPTION_PATH = "docs/.speckit/exemptions/concepts/widget-overview.md"

SOURCE_TEXT = """graph LR
  A[Request] --> B[Validator]
  B --> C[Widget store]
"""

SVG_TEXT = """<svg xmlns="http://www.w3.org/2000/svg" width="120" height="40">
  <text x="4" y="24">Request -> Validator -> Widget store</text>
</svg>
"""

PNG_TEXT = "PNG-PLACEHOLDER 087 fixture rendered face (never decoded; only hashed)\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def doc_text(link_target: str | None) -> str:
    body = [
        "# Widget overview",
        "",
        "The widget subsystem validates every request before it reaches the store.",
        "",
    ]
    if link_target is not None:
        body += [f"The pipeline is drawn in [the widget pipeline diagram](../{link_target}).", ""]
    body += [
        "## Notes",
        "",
        "This document is a fixture, not an article: its only job is to carry (or not carry)",
        "a relative reference to a diagram render, so the obligation checker has something to judge.",
        "",
    ]
    return "\n".join(body)


def record_payload(diagram_overrides: dict | None = None, drop: tuple = ()) -> dict:
    """One trace record whose single `diagrams[]` entry describes the `clean/` pair."""
    diagram = {
        "document": DOC_PATH,
        "engine": "mermaid",
        "engine_reason": "routing matrix row: flow graph, no zone grammar required",
        "ldm_summary": "diagram_class=flow; elements=3; relations=2; zones=0",
        "delivery": {"accepted": True, "unmet": []},
        "source": SOURCE_PATH,
        "rendered": [
            {"path": SVG_PATH, "sha256": sha256_text(SVG_TEXT)},
            {"path": PNG_PATH, "sha256": sha256_text(PNG_TEXT)},
        ],
    }
    if diagram_overrides:
        diagram.update(diagram_overrides)
    for key in drop:
        diagram.pop(key, None)
    return {
        "run_id": "20261106T090000Z-0870a1b2",
        "feature": "087-arch-diagram-docs",
        "diagrams": [diagram],
    }


def exemption_text(document: str = DOC_PATH, reason: str = "exempt-chronological",
                   recorded_at: str = "2026-11-06",
                   justification: str = "Release flow ordered in time; no structure to draw") -> str:
    lines = ["---", f"document: {document}", f"reason: {reason}", f"recorded_at: {recorded_at}"]
    if justification is not None:
        lines.append(f'justification: "{justification}"')
    lines += ["---", "", "# Exemption", ""]
    return "\n".join(lines)


def write(space: Path, relpath: str, text: str) -> None:
    target = space / relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def base_space(space: Path) -> None:
    """The miniature documentation space every fixture starts from (E6 'complete miniature space')."""
    if space.exists():
        shutil.rmtree(space)
    write(space, "README.md", "# Fixture project\n\nSee [the docs](docs/concepts/widget-overview.md).\n")
    for d in TYPE_DIRS:
        (space / "docs" / d).mkdir(parents=True, exist_ok=True)
    (space / "docs" / "assets").mkdir(parents=True, exist_ok=True)
    (space / "docs" / ".speckit").mkdir(parents=True, exist_ok=True)
    # one other carrier per typed directory, so the carrier walk has something to count and
    # so `--only` has a second document to leave alone
    for d in TYPE_DIRS:
        if d == "concepts":
            continue
        write(space, f"docs/{d}/index.md", f"# {d} index\n\nFixture index for the {d} subtree.\n")


def build_all() -> list[str]:
    built = []

    def finish(name: str) -> None:
        built.append(name)

    # 1. clean/ — the green reference space: both faces, resolving reference, complete record
    s = HERE / "clean"
    base_space(s)
    write(s, DOC_PATH, doc_text("assets/widget.svg"))
    write(s, SOURCE_PATH, SOURCE_TEXT)
    write(s, SVG_PATH, SVG_TEXT)
    write(s, PNG_PATH, PNG_TEXT)
    write(s, RECORD_PATH, json.dumps(record_payload(), indent=2) + "\n")
    finish("clean")

    # 2. no-diagram/ — nothing in the document points at any diagram file
    s = HERE / "no-diagram"
    base_space(s)
    write(s, DOC_PATH, doc_text(None))
    write(s, SOURCE_PATH, SOURCE_TEXT)
    write(s, SVG_PATH, SVG_TEXT)
    write(s, PNG_PATH, PNG_TEXT)
    write(s, RECORD_PATH, json.dumps(record_payload(), indent=2) + "\n")
    finish("no-diagram")

    # 3. deleted-rendered/ — render deleted, source present, reference still points at the deleted render
    s = HERE / "deleted-rendered"
    base_space(s)
    write(s, DOC_PATH, doc_text("assets/widget.svg"))
    write(s, SOURCE_PATH, SOURCE_TEXT)
    write(s, RECORD_PATH, json.dumps(record_payload(), indent=2) + "\n")
    finish("deleted-rendered")

    # 4. orphan-rendered/ — render deleted, source present, reference points at the SOURCE (resolves!)
    #
    # The record names the diagram by its SOURCE only (`rendered: []`). Two reasons:
    #   1. `rendered[].sha256` is optional in the record schema but, when present, is checked against the file on
    #      disk (C-008 rule 2), so a rendered entry whose file is not on disk can only be written by hashing
    #      something that does not exist — a fabricated record.
    #   2. The reading this space exists to pin is C-007 condition 2 (`satisfied` needs a reference that
    #      resolves to one of the record's `rendered[].path` values). With no rendered face in the record the
    #      condition is false for every reference, so the document lands `missing` / `orphan-rendered` from the
    #      SOURCE-ONLY reference alone (C-005's named face) — the verdict never depends on which tier ran first.
    s = HERE / "orphan-rendered"
    base_space(s)
    write(s, DOC_PATH, doc_text("assets/widget.mmd"))
    write(s, SOURCE_PATH, SOURCE_TEXT)
    write(s, RECORD_PATH, json.dumps(record_payload({"rendered": []}), indent=2) + "\n")
    finish("orphan-rendered")

    # 5. orphan-source/ — source deleted, render present, reference resolves to the render
    s = HERE / "orphan-source"
    base_space(s)
    write(s, DOC_PATH, doc_text("assets/widget.svg"))
    write(s, SVG_PATH, SVG_TEXT)
    write(s, PNG_PATH, PNG_TEXT)
    write(s, RECORD_PATH, json.dumps(record_payload(), indent=2) + "\n")
    finish("orphan-source")

    # 6. stale-source/ — both faces on disk; conftest.py pins the mtime inequality
    s = HERE / "stale-source"
    base_space(s)
    write(s, DOC_PATH, doc_text("assets/widget.svg"))
    write(s, SOURCE_PATH, SOURCE_TEXT)
    write(s, SVG_PATH, SVG_TEXT)
    write(s, PNG_PATH, PNG_TEXT)
    write(s, RECORD_PATH, json.dumps(record_payload(), indent=2) + "\n")
    finish("stale-source")

    # 7. no-trace/ — both faces + resolving reference, and deliberately NO record file
    s = HERE / "no-trace"
    base_space(s)
    write(s, DOC_PATH, doc_text("assets/widget.svg"))
    write(s, SOURCE_PATH, SOURCE_TEXT)
    write(s, SVG_PATH, SVG_TEXT)
    write(s, PNG_PATH, PNG_TEXT)
    finish("no-trace")

    # 8. trace-incomplete/ — a record exists but cannot point at this diagram (no same-named entry)
    s = HERE / "trace-incomplete"
    base_space(s)
    write(s, DOC_PATH, doc_text("assets/widget.svg"))
    write(s, SOURCE_PATH, SOURCE_TEXT)
    write(s, SVG_PATH, SVG_TEXT)
    write(s, PNG_PATH, PNG_TEXT)
    write(s, RECORD_PATH, json.dumps(
        record_payload({"rendered": [{"path": "docs/assets/other.svg"}]}), indent=2) + "\n")
    finish("trace-incomplete")

    # 9. exempt-ok/ — a valid exemption record; the document has no diagram at all
    s = HERE / "exempt-ok"
    base_space(s)
    write(s, DOC_PATH, doc_text(None))
    write(s, EXEMPTION_PATH, exemption_text())
    finish("exempt-ok")

    # 10. exempt-bad/ — the exemption record is missing `justification`
    s = HERE / "exempt-bad"
    base_space(s)
    write(s, DOC_PATH, doc_text(None))
    write(s, EXEMPTION_PATH, exemption_text(justification=None))
    finish("exempt-bad")

    # 11. exempt-superseded/ — a valid-looking exemption whose document now carries a resolving reference
    s = HERE / "exempt-superseded"
    base_space(s)
    write(s, DOC_PATH, doc_text("assets/widget.svg"))
    write(s, SOURCE_PATH, SOURCE_TEXT)
    write(s, SVG_PATH, SVG_TEXT)
    write(s, PNG_PATH, PNG_TEXT)
    write(s, RECORD_PATH, json.dumps(record_payload(), indent=2) + "\n")
    write(s, EXEMPTION_PATH, exemption_text())
    finish("exempt-superseded")

    return built


CHECKS = "--check"
REBUILD = "--rebuild"


def _expected_files(name: str) -> dict[str, bytes] | None:
    """`{relpath: bytes}` the builder would write for `name`, computed without touching the working tree.

    `build_all()` is redirected to a scratch directory (`tempfile.mkdtemp`, removed here), so this function is the
    only way to see the builder's deterministic output without rewriting the committed fixtures. A name the builder
    does not know returns None.
    """
    scratch = Path(tempfile.mkdtemp(prefix="docs-obligation-fixtures-"))
    global HERE
    saved = HERE
    try:
        HERE = scratch
        built = build_all()
    finally:
        HERE = saved
    if name not in built:
        shutil.rmtree(scratch, ignore_errors=True)
        return None
    space = scratch / name
    files = {
        path.relative_to(space).as_posix(): path.read_bytes()
        for path in sorted(space.rglob("*")) if path.is_file()
    }
    shutil.rmtree(scratch, ignore_errors=True)
    return files


def check() -> int:
    """Assert every registered space is on disk with its registered shape (writes nothing).

    Presence alone is not the invariant E6 registers: a record can be rewritten in place while every path the
    table names still exists, so `--check` also compares each fixture's BYTES with what this builder would write.
    The composition table (`must` / `absent`) stays as the legible half of the assertion; the byte comparison below
    is what makes a content drift visible.
    """
    expected = [
        "clean", "no-diagram", "deleted-rendered", "orphan-rendered", "orphan-source",
        "stale-source", "no-trace", "trace-incomplete", "exempt-ok", "exempt-bad",
        "exempt-superseded",
    ]
    problems: list[str] = []
    for name in expected:
        space = HERE / name
        if not space.is_dir():
            problems.append(f"{name}: missing")
            continue
        for need in ("README.md", DOC_PATH):
            if not (space / need).is_file():
                problems.append(f"{name}: missing {need}")
        for d in TYPE_DIRS:
            if not (space / "docs" / d).is_dir():
                problems.append(f"{name}: missing docs/{d}/")
    # per-space registered composition
    must = {
        "clean": [SOURCE_PATH, SVG_PATH, PNG_PATH, RECORD_PATH],
        "no-diagram": [SOURCE_PATH, SVG_PATH, PNG_PATH, RECORD_PATH],
        "deleted-rendered": [SOURCE_PATH, RECORD_PATH],
        "orphan-rendered": [SOURCE_PATH, RECORD_PATH],
        "orphan-source": [SVG_PATH, PNG_PATH, RECORD_PATH],
        "stale-source": [SOURCE_PATH, SVG_PATH, PNG_PATH, RECORD_PATH],
        "no-trace": [SOURCE_PATH, SVG_PATH, PNG_PATH],
        "trace-incomplete": [SOURCE_PATH, SVG_PATH, PNG_PATH, RECORD_PATH],
        "exempt-ok": [EXEMPTION_PATH],
        "exempt-bad": [EXEMPTION_PATH],
        "exempt-superseded": [SOURCE_PATH, SVG_PATH, PNG_PATH, RECORD_PATH, EXEMPTION_PATH],
    }
    absent = {
        "deleted-rendered": [SVG_PATH, PNG_PATH],
        "orphan-rendered": [SVG_PATH, PNG_PATH],
        "orphan-source": [SOURCE_PATH],
        "no-trace": [RECORD_PATH],
    }
    for name, rels in must.items():
        for rel in rels:
            if not (HERE / name / rel).is_file():
                problems.append(f"{name}: expected {rel}")
    for name, rels in absent.items():
        for rel in rels:
            if (HERE / name / rel).exists():
                problems.append(f"{name}: {rel} must not exist")
    # byte comparison: the composition table says WHAT is there, this says it is still the SAME content. A record
    # whose path is registered but whose faces were rewritten in place passes every presence check above.
    for name in expected:
        want = _expected_files(name)
        if want is None:
            problems.append(f"{name}: the builder does not register this space")
            continue
        have = {
            path.relative_to(HERE / name).as_posix(): path
            for path in sorted((HERE / name).rglob("*")) if path.is_file()
        }
        for relpath in sorted(set(want) - set(have)):
            problems.append(f"{name}: missing {relpath}")
        for relpath in sorted(set(have) - set(want)):
            problems.append(f"{name}: unexpected {relpath} (the builder would not write it)")
        for relpath in sorted(set(want) & set(have)):
            if have[relpath].read_bytes() != want[relpath]:
                problems.append(f"{name}: {relpath} differs from the builder's output (content drift)")
    if problems:
        for p in problems:
            print(f"FIXTURE-{p}", file=sys.stderr)
        return 1
    print(f"OK: {len(expected)} docs-obligation fixture spaces match their registered composition and bytes")
    return 0


if __name__ == "__main__":
    # Exactly two accepted invocations. An unknown flag is an input error (exit 2) rather than a rebuild: a bare
    # `--help` probe used to fall through to `build_all()` and rewrite a committed record, which is how a fixture
    # can be silently changed by a read-only-looking command.
    unknown = [arg for arg in sys.argv[1:] if arg not in (CHECKS, REBUILD)]
    if unknown:
        print(f"build_fixtures.py: error: unknown argument(s) {unknown}; accepted: {CHECKS} | {REBUILD}",
              file=sys.stderr)
        sys.exit(2)
    if REBUILD not in sys.argv[1:]:
        sys.exit(check())
    names = build_all()
    print(f"built {len(names)} fixture spaces: {', '.join(names)}")
    sys.exit(check())
