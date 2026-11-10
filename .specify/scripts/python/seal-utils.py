#!/usr/bin/env python3
"""Seal engine for `/speckit.seal` (requirement 099) — CLI skeleton (work package P2).

Owner of the four-action closed set, the three-value exit domain and the write-path
allowlist. The action bodies land in later work packages on top of this surface.

Actions (exactly four; a fifth MUST NOT appear):
  merge-plan     read-only   slice set, per-artifact actions, ID maps and conflicts
  merge-apply    write       deterministic merge into the parent spec, merge-manifest.json,
                             one `**Merged into**` line per slice
  seal           write       judgment first (read-only), then one atomic write batch:
                             seal.md + registry row + feature detail
  archive-gate   read-only   archive admission verdict (0 allow / 1 refuse / 2 input error)

Exit codes (exactly three; a fourth MUST NOT appear):
  0 success or idempotent (already-sealed included; an allowed archive-gate)
  1 a precondition refused (a read-only report is still complete)
  2 input or environment error (state-drift included; never read as a pass)

Two hats (C-009): the mirror position is decided by the LITERAL `.specify` component at
a fixed structural index of the engine's own resolved path — never by walking up to the
nearest `.specify` ancestor, a heuristic that self-matches in this repository. A mirror
copy refuses write actions (exit 2, reason `mirror-copy`): writing through the mirror
would break the byte-identical source/mirror pair.

Contract: `.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md` (C-001…C-010)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple

ENGINE_NAME = "seal-utils.py"

#: C-001: the action set is closed at exactly four values.
ACTIONS = ("merge-plan", "merge-apply", "seal", "archive-gate")
#: C-005: the two-phase declaration — which actions are pure judgments and which write.
READ_ONLY_ACTIONS = ("merge-plan", "archive-gate")
WRITE_ACTIONS = ("merge-apply", "seal")

#: C-002: the exit domain is closed at exactly three values.
EXIT_OK = 0
EXIT_REFUSED = 1
EXIT_INPUT_ERROR = 2
EXIT_CODES = (EXIT_OK, EXIT_REFUSED, EXIT_INPUT_ERROR)

#: C-010: the verdict a payload carries, and the exit code each verdict maps to.
VERDICTS = ("ok", "refused", "error")

#: C-009: the spec contract file that makes a directory a spec directory.
SPEC_CONTRACT_FILE = "requirements.md"

#: C-008: the write surface, as data. Any path the engine may write, relative to the
#: resolved roots; a new entry is a contract change, never an implementation detail.
WRITE_PATH_ALLOWLIST = (
    "{spec_dir}/seal.md",                 # E2 seal record
    "{spec_dir}/merge-manifest.json",     # E3 merge manifest
    "{spec_dir}/{merged_artifact}",       # E5 merged artifacts (file-level units)
    "{slice_dir}/requirements.md",        # E14 exactly one `**Merged into**` line
    "{factory_doc}",                      # C-017 recorded reference resolutions only
)

#: Stable condition codes for the engine-level (non-action) errors.
MIRROR_CODE = "mirror-copy"
SPEC_DIR_CODE = "spec-dir-invalid"
PENDING_CODE = "not-implemented"

#: C-004: the full declared option vocabulary (the pre-parse guard judges against it).
DECLARED_OPTIONS = ("--action", "--spec-dir", "--repo", "--feature-detail",
                    "--feature-registry", "--json")


# ---------------------------------------------------------------------------
# The guard helper (C-003): `--help` / `--version` zero-side-effect, unknown
# options rejected with 2 before any action. The rule lives in the helper.
# ---------------------------------------------------------------------------

def _import_guard():
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    try:
        from script_interface_cli import add_version_argument, configure_parser, guard_argv
        return configure_parser, guard_argv, add_version_argument
    except ImportError:  # a bare copy without the helper still runs its actions
        def _configure(parser, **_kwargs):
            return parser

        def _guard(_argv=None, declared=None, **_kwargs):
            return None

        def _add_version(parser):
            return parser

        return _configure, _guard, _add_version


_sig_configure, _sig_guard, _sig_add_version = _import_guard()


# ---------------------------------------------------------------------------
# Report rendering (C-006 / C-010): one payload, two renderings, stdout only
# ---------------------------------------------------------------------------

def _condition(code: str, evidence: str, fix_path: str, rerun: str) -> Dict[str, str]:
    return {"code": code, "evidence": evidence, "fix_path": fix_path, "rerun": rerun}


def _payload(action: Optional[str], spec_dir: Optional[Path], verdict: str,
             exit_code: int, conditions=None) -> Dict[str, Any]:
    return {
        "action": action,
        "spec_dir": str(spec_dir) if spec_dir is not None else None,
        "verdict": verdict,
        "exit_code": exit_code,
        "conditions": list(conditions or []),
    }


def render(payload: Dict[str, Any], as_json: bool) -> None:
    """Print the one judgment; the machine form is canonical (C-010)."""
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        return
    print("%s %s: %s (exit %d)" % (
        ENGINE_NAME, payload["action"], payload["verdict"], payload["exit_code"]))
    plan = payload.get("plan")
    if isinstance(plan, dict) and "slices" in plan:
        basis = plan["slices"][0]["order_basis"] if plan["slices"] else "-"
        print("  slices: %d (order_basis=%s)" % (len(plan["slices"]), basis))
        for entry in plan["slices"]:
            print("    %d. %s" % (entry["order"], entry["slug"]))
        print("  artifacts: %d rows" % len(plan["artifacts"]))
        for row in plan["artifacts"]:
            print("    %-14s %s" % (row["action"], row["name"]))
        print("  id_maps: %d entries" % sum(
            len(entries) for entries in plan["id_maps"].values()))
        print("  factory_doc_refs: %d" % len(plan["factory_doc_refs"]))
        print("  conflicts: %d open" % len(
            [item for item in plan["conflicts"] if item.get("status") == "open"]))
    for condition in payload["conditions"]:
        print("  - %s: %s" % (condition["code"], condition["evidence"]))
        print("    fix: %s" % condition["fix_path"])
        print("    rerun: %s" % condition["rerun"])


# ---------------------------------------------------------------------------
# Path resolution (C-009): explicit paths only, fixed structural signal
# ---------------------------------------------------------------------------

def is_mirror_copy(self_path: Optional[Path] = None) -> bool:
    """Whether this engine is the `<repo>/.specify/scripts/python/` mirror copy.

    The signal is the literal `.specify` component at the fixed index that the mirror
    position dictates (`scripts/python/<name>.py` sits directly under it). Walking up
    to the nearest `.specify` ancestor is forbidden: the worktree itself may live under
    `.specify/.tmp/...`, and that heuristic would misclassify the framework source.
    """
    path = Path(self_path if self_path is not None else __file__).resolve()
    parents = path.parents
    return len(parents) >= 3 and parents[2].name == ".specify"


def resolve_spec_dir(raw: str) -> Optional[Path]:
    """Resolve `--spec-dir` against the invocation cwd; require a spec directory shape.

    The shape is `requirements.md` presence only — never a `^\\d{3}-` name prefix.
    """
    path = Path(raw)
    if not path.is_absolute():
        path = Path.cwd() / path
    path = path.resolve()
    if not path.is_dir():
        return None
    if not (path / SPEC_CONTRACT_FILE).is_file():
        return None
    return path


# ---------------------------------------------------------------------------
# Merge-plan surface (C-011 … C-018). Everything below reads or returns data;
# the plan action writes nothing.
# ---------------------------------------------------------------------------

#: C-013: the merge candidate universe is this closed list of fifteen names.
CANDIDATES = (
    "requirements.md", "plan.md", "tasks.md", "data-model.md", "contracts",
    "research.md", "quickstart.md", "feature-ref.md", "verification.md",
    "review.md", "code-review.md", "checklists", "checkpoints", "test-evidence",
    "notes",
)
#: C-013: directory candidates merge by file-level unit.
DIRECTORY_CANDIDATES = ("contracts", "checklists", "checkpoints", "test-evidence", "notes")
#: C-020: dated records live under these directories; they are pointed at, never copied.
DATED_RECORD_DIRS = ("checkpoints", "test-evidence")
#: C-013 mandatory floor: with a non-empty slice set these parent views are produced.
POINTER_VIEW_CANDIDATES = ("verification.md", "review.md", "code-review.md")
#: C-015: declarative ID families — a slice id must declare its parent target.
SEMANTIC_FAMILIES = ("FR", "SC", "STR")
#: C-015: mechanical ID families — collisions renumber by merge order.
MECHANICAL_FAMILIES = ("T", "C", "E")
FAMILIES = SEMANTIC_FAMILIES + MECHANICAL_FAMILIES
#: C-017: framework-source and mirror roots scanned for factory-doc references.
FACTORY_DOC_ROOTS = (
    "skills", "templates", "shared", "scripts", "agents",
    ".specify/skills", ".specify/templates", ".specify/shared",
    ".specify/scripts", ".specify/agents",
    ".claude/commands", ".github/prompts", ".opencode/command", ".qoder/commands",
)
ARTIFACT_ACTIONS = ("merge", "create", "keep", "not-applicable")
SLICE_CODE = "slice-candidate-unconfirmed"

_DEFINITION_RE = re.compile(r"^-\s+\*\*(FR|SC)-(\d{3})\*\*")
_TASK_ROW_RE = re.compile(r"^-\s+\[(.)\]\s+(T\d{3})\b")
_CLAUSE_RE = re.compile(r"^\*\*(C-\d{3})\*\*")
_ENTITY_RE = re.compile(r"^\|\s*(E\d+)\s*\|")
_STR_REF_RE = re.compile(r"\[\[(STR-\d{3})\]\]")
_DATE_RE = re.compile(r"\d{4}-?\d{2}-?\d{2}")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _rel_path(repo: Path, path: Path) -> str:
    try:
        return str(path.relative_to(repo))
    except ValueError:
        return str(path)


def _section(text: str, heading_pattern: str):
    """Return (body_lines, zero_based_heading_index) of the first `## ` section."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if re.match(r"^##\s+", line) and re.search(heading_pattern, line):
            body = []
            for inner in lines[index + 1:]:
                if re.match(r"^##\s+", inner):
                    break
                body.append(inner)
            return body, index
    return None, None


def _canonical_id(cell: str) -> Optional[str]:
    match = re.match(r"^\s*`?((?:FR|SC|STR)-\d{3}|T\d{3}|C-\d{3}|E\d+)`?\s*$", cell)
    return match.group(1) if match else None


def _target_id(cell: str) -> Optional[str]:
    match = re.search(r"(FR|SC|STR)[- ]?(\d{3})", cell)
    if match:
        return "%s-%s" % (match.group(1), match.group(2))
    match = re.search(r"\b(T\d{3}|C-\d{3}|E\d+)\b", cell)
    return match.group(1) if match else None


def _parse_section_rewrite(text: str):
    if "\u00a7" not in text:
        return None
    left, _, right = text.partition("\u00a7")
    artifact = left.strip().strip("`").strip()
    heading = right.strip().strip("`").strip()
    heading = re.sub(r"^#+\s*", "", heading)
    if not artifact or not heading:
        return None
    return artifact, heading


def _parse_parent_mapping(text: str) -> Dict[str, Any]:
    """Parse the `## Parent Mapping` declaration: id rows and declared section rewrites."""
    body, start = _section(text, r"Parent Mapping")
    result = {"declared": body is not None, "mappings": [], "sections": []}
    if body is None:
        return result
    heading = ""
    for offset, line in enumerate(body):
        line_no = (start or 0) + 2 + offset
        if re.match(r"^###\s+", line):
            heading = line
            continue
        if heading and "Section Rewrites" in heading:
            bullet = re.match(r"^\s*-\s+(.+)$", line)
            parsed = _parse_section_rewrite(bullet.group(1)) if bullet else None
            if parsed:
                result["sections"].append(
                    {"artifact": parsed[0], "heading": parsed[1], "line": line_no})
            continue
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        local = _canonical_id(cells[0])
        target = _target_id(cells[1])
        if local and target:
            result["mappings"].append(
                {"slice_id": local, "parent_id": target, "line": line_no})
    return result


def _parse_shared_strings(text: str) -> Dict[str, Dict[str, Any]]:
    body, start = _section(text, r"Shared Strings")
    registry: Dict[str, Dict[str, Any]] = {}
    for offset, line in enumerate(body or []):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        match = re.match(r"^`?(STR-\d{3})`?$", cells[0])
        if not match:
            continue
        literal = cells[1].strip().strip("`").strip()
        if len(literal) >= 2 and literal.startswith("\"") and literal.endswith("\""):
            literal = literal[1:-1]
        registry[match.group(1)] = {"literal": literal,
                                    "line": (start or 0) + 2 + offset}
    return registry


def _definition_lines(text: str):
    entries = []
    for line_no, line in enumerate(text.splitlines(), 1):
        match = _DEFINITION_RE.match(line)
        if match:
            entries.append({"id": "%s-%s" % (match.group(1), match.group(2)),
                            "line": line_no, "text": _normalize(line)})
    return entries


def _task_rows(text: str, state: Optional[str] = None):
    entries = []
    for line_no, line in enumerate(text.splitlines(), 1):
        match = _TASK_ROW_RE.match(line)
        if match and (state is None or match.group(1) == state):
            entries.append({"id": match.group(2), "line": line_no, "text": _normalize(line)})
    return entries


def _contract_clauses(path: Path):
    entries = []
    if not path.is_file():
        return entries
    for line_no, line in enumerate(_read_text(path).splitlines(), 1):
        match = _CLAUSE_RE.match(line)
        if match:
            entries.append({"id": match.group(1), "line": line_no, "text": _normalize(line)})
    return entries


def _entity_rows(path: Path):
    entries = []
    if not path.is_file():
        return entries
    for line_no, line in enumerate(_read_text(path).splitlines(), 1):
        match = _ENTITY_RE.match(line)
        if match:
            entries.append({"id": match.group(1), "line": line_no, "text": _normalize(line)})
    return entries


def _id_number(family: str, identifier: str) -> int:
    if family == "T":
        return int(identifier[1:])
    if family == "E":
        return int(identifier[1:])
    return int(identifier.split("-")[1])


def _format_id(family: str, number: int) -> str:
    if family == "T":
        return "T%03d" % number
    if family == "E":
        return "E%d" % number
    return "%s-%03d" % (family, number)


# ---------------------------------------------------------------------------
# Slice discovery (C-011) and order derivation (C-012)
# ---------------------------------------------------------------------------

def _slice_name_pattern(parent_slug: str):
    match = re.match(r"^(\d{3})", parent_slug)
    if not match:
        return None
    return re.compile(r"^%s[A-Za-z]+-[a-z0-9][a-z0-9-]*$" % match.group(1))


def _declares_parent(text: str, parent_slug: str) -> bool:
    field = re.search(r"^\*\*Parent spec\*\*:\s*(.+)$", text, re.M)
    if field and parent_slug in field.group(1):
        return True
    body, _ = _section(text, r"Parent Mapping")
    return body is not None and parent_slug in "\n".join(body)


def _discover_slices(spec_dir: Path):
    parent_slug = spec_dir.name
    pattern = _slice_name_pattern(parent_slug)
    slices, excluded = [], []
    specs_root = spec_dir.parent
    if not specs_root.is_dir():
        return slices, excluded
    for entry in sorted(specs_root.iterdir(), key=lambda item: item.name):
        if not entry.is_dir() or entry.resolve() == spec_dir.resolve():
            continue
        requirements = entry / "requirements.md"
        if not requirements.is_file():
            continue
        text = _read_text(requirements)
        name_hit = bool(pattern and pattern.match(entry.name))
        declared = _declares_parent(text, parent_slug)
        if name_hit and declared:
            slices.append({"slug": entry.name, "path": entry,
                           "requirements": requirements, "text": text})
        elif name_hit or declared:
            excluded.append({"slug": entry.name, "path": entry,
                             "requirements": requirements,
                             "missing": "parent-declaration" if name_hit else "name-family"})
    return slices, excluded


def _derive_order(repo: Path, parent_slug: str, slices):
    state_path = repo / ".specify" / "state" / ("%s.md" % parent_slug)
    slugs = [item["slug"] for item in slices]
    basis = "letter-order"
    source = "directory-name sort (no split record at .specify/state/%s.md)" % parent_slug
    ordered = sorted(slugs)
    if state_path.is_file():
        body, _ = _section(_read_text(state_path), r"拆分记录")
        found = []
        for index, line in enumerate(body or []):
            if not re.match(r"^\s*(?:[-*]\s*)?proposed_slices\s*:", line):
                continue
            for inner in body[index + 1:]:
                if not inner.strip():
                    continue
                if not re.match(r"^\s+[-*]\s+", inner):
                    break
                match = re.search(r"\d{3}[A-Za-z]+-[a-z0-9-]+", inner)
                if match and match.group(0) in slugs and match.group(0) not in found:
                    found.append(match.group(0))
            break
        if found:
            remainder = sorted(slug for slug in slugs if slug not in found)
            ordered = found + remainder
            basis = "split-record"
            source = ".specify/state/%s.md#拆分记录.proposed_slices" % parent_slug
            if remainder:
                source += " (record omits %s; appended in letter order)" % ",".join(remainder)
    ordered_slices = []
    for position, slug in enumerate(ordered, 1):
        item = next(entry for entry in slices if entry["slug"] == slug)
        ordered_slices.append({
            "slug": slug,
            "order": position,
            "order_basis": basis,
            "order_source": source,
            "path": item["path"],
            "requirements": item["requirements"],
            "text": item["text"],
        })
    return ordered_slices


# ---------------------------------------------------------------------------
# Artifact classification (C-013 / C-020)
# ---------------------------------------------------------------------------

def _artifact_row(name, action, unit, sources, per_slice,
                  basis=None, pointer=None, pointer_view=False):
    row = {"name": name, "action": action, "unit": unit,
           "sources": list(sources), "per_slice": per_slice}
    if basis:
        row["basis"] = basis
    if pointer:
        row["pointer"] = pointer
    if pointer_view:
        row["pointer_view"] = True
    return row


def _dated_record(name: str) -> bool:
    return _DATE_RE.search(name) is not None


def _classify_artifacts(repo: Path, spec_dir: Path, slices):
    rows = []
    for name in CANDIDATES:
        if name in DIRECTORY_CANDIDATES:
            parent_dir = spec_dir / name
            files = set()
            if parent_dir.is_dir():
                files.update(item.name for item in parent_dir.iterdir() if item.is_file())
            for item in slices:
                candidate_dir = item["path"] / name
                if candidate_dir.is_dir():
                    files.update(child.name for child in candidate_dir.iterdir()
                                 if child.is_file())
            if not files:
                rows.append(_artifact_row(
                    name, "not-applicable", "directory", [],
                    [{"slice": item["slug"], "present": False} for item in slices],
                    basis="no files on the parent or on any slice"))
                continue
            for fname in sorted(files):
                per_slice = [{"slice": item["slug"],
                              "present": (item["path"] / name / fname).is_file()}
                             for item in slices]
                sources = [entry["slice"] for entry in per_slice if entry["present"]]
                parent_has = (parent_dir / fname).is_file()
                unit_name = "%s/%s" % (name, fname)
                dated = name in DATED_RECORD_DIRS and _dated_record(fname)
                if dated and parent_has and sources:
                    rows.append(_artifact_row(
                        unit_name, "keep", "directory-file", sources, per_slice,
                        basis="dated record: the parent copy is kept; slice originals "
                              "are referenced, never copied",
                        pointer={"kind": "slice-original",
                                 "paths": [_rel_path(repo, item["path"] / name / fname)
                                           for item in slices
                                           if (item["path"] / name / fname).is_file()]}))
                elif dated and sources:
                    rows.append(_artifact_row(
                        unit_name, "create", "directory-file", sources, per_slice,
                        basis="dated record: the parent pointer view carries a summary "
                              "row and a pointer, never a copy",
                        pointer={"kind": "pointer-view",
                                 "paths": [_rel_path(repo, item["path"] / name / fname)
                                           for item in slices
                                           if (item["path"] / name / fname).is_file()]},
                        pointer_view=True))
                elif parent_has and sources:
                    rows.append(_artifact_row(unit_name, "merge", "directory-file",
                                              sources, per_slice))
                elif parent_has:
                    rows.append(_artifact_row(unit_name, "keep", "directory-file",
                                              sources, per_slice))
                else:
                    rows.append(_artifact_row(unit_name, "create", "directory-file",
                                              sources, per_slice))
            continue

        parent_has = (spec_dir / name).is_file()
        per_slice = [{"slice": item["slug"],
                      "present": (item["path"] / name).is_file()} for item in slices]
        sources = [entry["slice"] for entry in per_slice if entry["present"]]
        if slices and name in POINTER_VIEW_CANDIDATES:
            rows.append(_artifact_row(
                name, "merge" if parent_has else "create", "file", sources, per_slice,
                basis=("aggregated pointer view over the slice records "
                       "(summary rows + pointers)") if parent_has else
                      ("required pointer view (parent record absent; summary rows "
                       "+ pointers)"),
                pointer={"kind": "pointer-view",
                         "paths": [_rel_path(repo, item["path"] / name)
                                   for item in slices
                                   if (item["path"] / name).is_file()]},
                pointer_view=True))
        elif parent_has and sources:
            rows.append(_artifact_row(name, "merge", "file", sources, per_slice))
        elif parent_has:
            rows.append(_artifact_row(name, "keep", "file", sources, per_slice))
        elif sources:
            rows.append(_artifact_row(name, "create", "file", sources, per_slice))
        else:
            basis = "absent on the parent and on every slice"
            if name == "tasks.md":
                basis = ("required floor: absent on the parent and on every slice; "
                         "the candidate is still disposed, never skipped")
            rows.append(_artifact_row(name, "not-applicable", "file",
                                      sources, per_slice, basis=basis))
    return rows


# ---------------------------------------------------------------------------
# ID-family maps (C-014 / C-015 / C-016) and conflicts
# ---------------------------------------------------------------------------

def _conflict(code, artifact, unit, side_a, side_b, candidates):
    return {
        "code": code,
        "artifact": artifact,
        "unit": unit,
        "side_a": side_a,
        "side_b": side_b,
        "candidates": list(candidates),
        "status": "open",
    }


def _side(path: str, line: int, excerpt: str) -> Dict[str, Any]:
    return {"path": path, "line": line, "excerpt": excerpt}


def _parent_registry_context(spec_dir: Path, with_slices: bool):
    requirements = _read_text(spec_dir / "requirements.md")
    tasks_path = spec_dir / "tasks.md"
    contracts = {}
    contracts_dir = spec_dir / "contracts"
    if contracts_dir.is_dir():
        for contract in sorted(contracts_dir.glob("*.md")):
            contracts[contract.name] = _contract_clauses(contract)
    return {
        "requirements": requirements,
        "definitions": _definition_lines(requirements),
        "strings": _parse_shared_strings(requirements),
        "tasks": _task_rows(_read_text(tasks_path),
                            state=("X" if with_slices else None))
        if tasks_path.is_file() else [],
        "all_tasks": {entry["id"]: entry for entry in (
            _task_rows(_read_text(tasks_path)) if tasks_path.is_file() else [])},
        "contracts": contracts,
        "entities": _entity_rows(spec_dir / "data-model.md"),
    }


def _family_entries(slice_item, family):
    """Ordered (id, line, text, file_rel) family entries inside one slice."""
    entries = []
    if family in ("FR", "SC"):
        for entry in _definition_lines(slice_item["text"]):
            if entry["id"].startswith(family + "-"):
                entries.append((entry["id"], entry["line"], entry["text"], "requirements.md"))
    elif family == "STR":
        for string_id, record in _parse_shared_strings(slice_item["text"]).items():
            entries.append((string_id, record["line"], record["literal"], "requirements.md"))
    elif family == "T":
        tasks_path = slice_item["path"] / "tasks.md"
        if tasks_path.is_file():
            for entry in _task_rows(_read_text(tasks_path)):
                entries.append((entry["id"], entry["line"], entry["text"], "tasks.md"))
    elif family == "C":
        contracts_dir = slice_item["path"] / "contracts"
        if contracts_dir.is_dir():
            for contract in sorted(contracts_dir.glob("*.md")):
                for entry in _contract_clauses(contract):
                    entries.append((entry["id"], entry["line"], entry["text"],
                                    contract.name))
    elif family == "E":
        model = slice_item["path"] / "data-model.md"
        for entry in _entity_rows(model):
            entries.append((entry["id"], entry["line"], entry["text"], "data-model.md"))
    return entries


def _parent_has(family, parent_id, file_rel, parent_sequences) -> bool:
    if family == "C":
        return any(parent_id in ids for ids in parent_sequences["C"].values())
    return parent_id in parent_sequences[family]


def _text_differs(family, text, parent_id, file_rel, context) -> bool:
    if family == "STR":
        parent = context["strings"].get(parent_id)
        return parent is not None and parent["literal"] != text
    if family in ("FR", "SC"):
        parent = next((entry for entry in context["definitions"]
                       if entry["id"] == parent_id), None)
        return parent is not None and parent["text"] != text
    if family == "T":
        parent = context["all_tasks"].get(parent_id)
        return parent is not None and parent["text"] != text
    if family == "C":
        parent = next((entry for entry in context["contracts"].get(file_rel, [])
                       if entry["id"] == parent_id), None)
        return parent is not None and parent["text"] != text
    if family == "E":
        parent = next((entry for entry in context["entities"]
                       if entry["id"] == parent_id), None)
        return parent is not None and parent["text"] != text
    return False


def _conflict_artifact(family: str, file_rel: str) -> str:
    if family in ("FR", "SC", "STR"):
        return "requirements.md"
    if family == "T":
        return "tasks.md"
    if family == "C":
        return "contracts/" + file_rel
    return "data-model.md"


def _build_id_maps(repo: Path, spec_dir: Path, slices):
    context = _parent_registry_context(spec_dir, with_slices=bool(slices))
    strings = context["strings"]
    parent_sequences = {
        "FR": [entry["id"] for entry in context["definitions"]
               if entry["id"].startswith("FR-")],
        "SC": [entry["id"] for entry in context["definitions"]
               if entry["id"].startswith("SC-")],
        "STR": list(strings),
        "T": [entry["id"] for entry in context["tasks"]],
        "C": {name: [entry["id"] for entry in entries]
              for name, entries in context["contracts"].items()},
        "E": [entry["id"] for entry in context["entities"]],
    }
    taken = {family: set(parent_sequences[family]) for family in ("FR", "SC", "STR", "T", "E")}
    for name, ids in parent_sequences["C"].items():
        taken[("C", name)] = set(ids)
    counters = {}
    for family in ("FR", "SC", "STR", "T", "E"):
        numbers = [_id_number(family, item) for item in parent_sequences[family]]
        counters[family] = (max(numbers) + 1) if numbers else 1
    for name, ids in parent_sequences["C"].items():
        numbers = [_id_number("C", item) for item in ids]
        counters[("C", name)] = (max(numbers) + 1) if numbers else 1
    claimed: Dict[str, Dict[str, Any]] = {family: {} for family in FAMILIES}

    def _allocate(family: str, file_key: Optional[str] = None) -> str:
        key = (family, file_key) if family == "C" else family
        if key not in counters:
            counters[key] = 1
            taken[key] = set()
        while True:
            number = counters[key]
            counters[key] = number + 1
            candidate = _format_id(family, number)
            if candidate not in taken[key]:
                taken[key].add(candidate)
                return candidate

    id_maps: Dict[str, list] = {family: [] for family in FAMILIES}
    conflicts = []
    parent_requirements = _rel_path(repo, spec_dir / "requirements.md")

    for family in FAMILIES:
        for slice_item in slices:
            slug = slice_item["slug"]
            slice_requirements = _rel_path(repo, slice_item["requirements"])
            mapping = {row["slice_id"]: row for row in
                       _parse_parent_mapping(slice_item["text"])["mappings"]}
            for slice_id, line, text, file_rel in _family_entries(slice_item, family):
                artifact = _conflict_artifact(family, file_rel)
                target = mapping.get(slice_id)
                if target is not None:
                    parent_id = target["parent_id"]
                    if not _parent_has(family, parent_id, file_rel, parent_sequences):
                        conflicts.append(_conflict(
                            "mapping-target-missing", artifact,
                            "%s -> %s" % (slice_id, parent_id),
                            _side(slice_requirements, target["line"],
                                  "declared mapping %s -> %s" % (slice_id, parent_id)),
                            _side(parent_requirements, 0,
                                  "the parent sequence carries no %s" % parent_id),
                            ["fix the declared mapping to an existing parent id",
                             "or record a user-waiver after review"]))
                        continue
                    if parent_id in claimed[family]:
                        same_shared_string = (
                            family == "STR"
                            and parent_id in strings
                            and strings[parent_id]["literal"] == text)
                        if not same_shared_string:
                            prior = claimed[family][parent_id]
                            conflicts.append(_conflict(
                                "duplicate-mapping", artifact, parent_id,
                                _side(slice_requirements, target["line"],
                                      "declared mapping %s -> %s"
                                      % (slice_id, parent_id)),
                                _side(prior["path"], prior["line"],
                                      "the target is already claimed by %s %s"
                                      % (prior["slice"], prior["slice_id"])),
                                ["declare a multi-to-one merge explicitly",
                                 "or record a user-waiver after review"]))
                            continue
                    claimed[family][parent_id] = {"slice": slug, "slice_id": slice_id,
                                                  "path": slice_requirements,
                                                  "line": target["line"]}
                    kind = ("localization"
                            if _text_differs(family, text, parent_id, file_rel, context)
                            else "mapped")
                    entry = {"slice": slug, "slice_id": slice_id,
                             "parent_id": parent_id, "kind": kind}
                    if family == "C":
                        entry["file"] = "contracts/" + file_rel
                    id_maps[family].append(entry)
                    continue

                if family == "STR":
                    existing = strings.get(slice_id)
                    if existing is not None:
                        if existing["literal"] == text:
                            id_maps["STR"].append({"slice": slug, "slice_id": slice_id,
                                                   "parent_id": slice_id, "kind": "mapped"})
                        else:
                            conflicts.append(_conflict(
                                "str-same-number-different-meaning", artifact, slice_id,
                                _side(slice_requirements, line,
                                      '%s = "%s"' % (slice_id, text)),
                                _side(parent_requirements, existing["line"],
                                      '%s = "%s"' % (slice_id, existing["literal"])),
                                ["declare the mapping in `## Parent Mapping` "
                                 "(canonical-map)",
                                 "or record a user-waiver after review — never silently "
                                 "renumber"]))
                    else:
                        new_id = _allocate("STR")
                        id_maps["STR"].append({"slice": slug, "slice_id": slice_id,
                                               "parent_id": new_id, "kind": "appended"})
                elif family in ("FR", "SC"):
                    if slice_id in parent_sequences[family]:
                        parent_entry = next(entry for entry in context["definitions"]
                                            if entry["id"] == slice_id)
                        conflicts.append(_conflict(
                            "no-mapping", artifact, slice_id,
                            _side(slice_requirements, line, text),
                            _side(parent_requirements, parent_entry["line"],
                                  parent_entry["text"]),
                            ["declare the slice id's parent target in `## Parent Mapping`",
                             "or record a user-waiver after review"]))
                    else:
                        new_id = _allocate(family)
                        id_maps[family].append({"slice": slug, "slice_id": slice_id,
                                                "parent_id": new_id, "kind": "appended"})
                else:
                    file_key = file_rel if family == "C" else None
                    new_id = _allocate(family, file_key)
                    entry = {"slice": slug, "slice_id": slice_id,
                             "parent_id": new_id, "kind": "appended"}
                    if family == "C":
                        entry["file"] = "contracts/" + file_rel
                    id_maps[family].append(entry)
    return id_maps, conflicts, context


# ---------------------------------------------------------------------------
# Token→registry binding for factory docs (C-017)
# ---------------------------------------------------------------------------

def _factory_doc_refs(repo: Path, slices, parent_strings, id_maps):
    refs, conflicts = [], []
    registries = [(item["slug"], item["requirements"],
                   _parse_shared_strings(item["text"])) for item in slices]
    for root in FACTORY_DOC_ROOTS:
        base = repo / root
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md"), key=lambda item: str(item)):
            if not path.is_file():
                continue
            for line_no, line in enumerate(_read_text(path).splitlines(), 1):
                for match in _STR_REF_RE.finditer(line):
                    token = match.group(1)
                    hits = [(slug, requirements, registry[token])
                            for slug, requirements, registry in registries
                            if token in registry]
                    if not hits:
                        # no slice registry carries this token: it is not a
                        # slice-local id and its meaning cannot change here
                        continue
                    if len(hits) > 1 and len({hit[2]["literal"] for hit in hits}) > 1:
                        conflicts.append(_conflict(
                            "factory-doc-ref-ambiguous", _rel_path(repo, path), token,
                            _side(_rel_path(repo, hits[0][1]), hits[0][2]["line"],
                                  '%s = "%s" in %s' % (token, hits[0][2]["literal"],
                                                       hits[0][0])),
                            _side(_rel_path(repo, hits[1][1]), hits[1][2]["line"],
                                  '%s = "%s" in %s' % (token, hits[0 + 1][2]["literal"],
                                                       hits[1][0])),
                            ["declare the registry (spec path + section anchor) in the "
                             "factory doc",
                             "repoint the reference to one merged parent id",
                             "or record a user-waiver after review"]))
                        continue
                    slug, slice_requirements, hit = hits[0]
                    literal = hit["literal"]
                    parent_record = parent_strings.get(token)
                    if parent_record is not None and parent_record["literal"] == literal:
                        continue  # resolves identically after the merge
                    merged = next((entry for entry in id_maps["STR"]
                                   if entry["slice"] == slug and entry["slice_id"] == token),
                                  None)
                    parent_id = merged["parent_id"] if merged else None
                    status = "resolved" if parent_id else "open"
                    refs.append({
                        "path": _rel_path(repo, path),
                        "line": line_no,
                        "token": token,
                        "slice": slug,
                        "slice_id": token,
                        "slice_literal": literal,
                        "parent_id": parent_id,
                        "parent_literal": (parent_record["literal"]
                                           if parent_record is not None else None),
                        "resolution": {"kind": "repoint", "target": parent_id},
                        "status": status,
                    })
                    if status == "open":
                        conflicts.append(_conflict(
                            "factory-doc-ref-unresolved", _rel_path(repo, path), token,
                            _side(_rel_path(repo, path), line_no,
                                  "the reference resolves only through %s" % slug),
                            _side(_rel_path(repo, slice_requirements), 0,
                                  "no merged parent id is derivable for %s" % token),
                            ["declare the registry or repoint the reference",
                             "or record a user-waiver after review"]))
    return refs, conflicts


def _pending(action: str, spec_dir: Optional[Path]) -> Tuple[Dict[str, Any], int]:
    return _payload(
        action, spec_dir, "error", EXIT_INPUT_ERROR,
        [_condition(
            PENDING_CODE,
            "the %s action body is not implemented on this skeleton" % action,
            "run the action once its implementing work package lands",
            "rerun the same command after the action body is implemented",
        )],
    ), EXIT_INPUT_ERROR


def _finalize_conflicts(conflicts):
    ordered = sorted(
        conflicts,
        key=lambda item: (item["artifact"], item["code"], item["unit"],
                          item["side_a"].get("path", ""),
                          item["side_a"].get("line", 0),
                          item["side_b"].get("path", ""),
                          item["side_b"].get("line", 0)))
    for index, item in enumerate(ordered, 1):
        item["id"] = "CF-%03d" % index
    return ordered


def _excluded_conflicts(repo: Path, excluded):
    conflicts = []
    for item in excluded:
        requirements = _rel_path(repo, item["requirements"])
        if item["missing"] == "parent-declaration":
            satisfied = ("name-family satisfied: the directory name matches "
                         "`<parent-number><letters>-<slug>`")
            unmet = ("parent-declaration unmet: no `## Parent Mapping` section and "
                     "no `**Parent spec**:` field names the parent")
            candidates = [
                "add a `## Parent Mapping` section or a `**Parent spec**:` field "
                "naming the parent",
                "or rename the directory out of the slice name family",
            ]
        else:
            satisfied = "parent-declaration satisfied: the file names the parent"
            unmet = ("name-family unmet: the directory name does not match "
                     "`<parent-number><letters>-<slug>`")
            candidates = [
                "rename the directory to `<parent-number><letters>-<slug>` inside "
                "`.specify/specs/`",
                "or remove the parent declaration if the directory is not a slice",
            ]
        conflicts.append(_conflict(
            SLICE_CODE, "slices", item["slug"],
            _side(requirements, 0, satisfied),
            _side(requirements, 0, unmet),
            candidates))
    return conflicts


def _section_rewrite_conflicts(repo: Path, spec_dir: Path, slices):
    conflicts = []
    for item in slices:
        parsed = _parse_parent_mapping(item["text"])
        for section in parsed["sections"]:
            parent_file = spec_dir / section["artifact"]
            if not parent_file.is_file():
                continue  # a slice-unique section lands in the merged appendix
            heading_line = 0
            heading_text = ""
            for line_no, line in enumerate(_read_text(parent_file).splitlines(), 1):
                if re.match(r"^##\s+" + re.escape(section["heading"]) + r"\s*$", line):
                    heading_line = line_no
                    heading_text = _normalize(line)
                    break
            if not heading_line:
                continue
            conflicts.append(_conflict(
                "same-anchor-dual-edit", section["artifact"],
                "\u00a7 %s" % section["heading"],
                _side(_rel_path(repo, item["requirements"]), section["line"],
                      "the slice declares a rewrite of `%s`" % section["heading"]),
                _side(_rel_path(repo, parent_file), heading_line,
                      "the parent owns the same anchor: %s" % heading_text),
                ["record a user-waiver after review",
                 "recheck-clean (drop the rewrite declaration or the parent edit)"]))
    return conflicts


def _build_plan(repo: Path, spec_dir: Path) -> Dict[str, Any]:
    slices, excluded = _discover_slices(spec_dir)
    ordered_slices = _derive_order(repo, spec_dir.name, slices)
    artifacts = _classify_artifacts(repo, spec_dir, ordered_slices)
    id_maps, map_conflicts, context = _build_id_maps(repo, spec_dir, ordered_slices)
    factory_refs, factory_conflicts = _factory_doc_refs(
        repo, ordered_slices, context["strings"], id_maps)
    conflicts = []
    conflicts.extend(map_conflicts)
    conflicts.extend(factory_conflicts)
    conflicts.extend(_excluded_conflicts(repo, excluded))
    conflicts.extend(_section_rewrite_conflicts(repo, spec_dir, ordered_slices))
    conflicts = _finalize_conflicts(conflicts)

    def _carrier(item) -> Optional[str]:
        tasks_path = item["path"] / "tasks.md"
        return _rel_path(repo, tasks_path) if tasks_path.is_file() else None

    plan = {
        "schema_version": 1,
        "spec": spec_dir.name,
        "slices": [{
            "slug": item["slug"],
            "order": item["order"],
            "order_basis": item["order_basis"],
            "order_source": item["order_source"],
            "carrier_tasks": _carrier(item),
            "retention": "pending-review",
        } for item in ordered_slices],
        "artifacts": artifacts,
        "id_maps": id_maps,
        "factory_doc_refs": factory_refs,
        "conflicts": conflicts,
        "checks": {
            "candidate_count": len(CANDIDATES),
            "slice_count": len(ordered_slices),
            "slice_conditions": ["name-family", "parent-declaration"],
            "excluded_candidates": len(excluded),
            "artifact_rows": len(artifacts),
            "id_map_entries": sum(len(entries) for entries in id_maps.values()),
            "factory_doc_refs": len(factory_refs),
            "open_conflicts": len([c for c in conflicts if c["status"] == "open"]),
        },
    }
    return plan


def action_merge_plan(args: argparse.Namespace, spec_dir: Path) -> Tuple[Dict[str, Any], int]:
    repo = Path(args.repo).resolve() if args.repo else Path.cwd()
    try:
        plan = _build_plan(repo, spec_dir)
    except (OSError, ValueError, StopIteration) as exc:
        return _payload(
            "merge-plan", spec_dir, "error", EXIT_INPUT_ERROR,
            [_condition(
                "merge-plan-error",
                "the merge plan cannot be derived from this tree: %s" % exc,
                "repair the named input (spec tree, split record or registries)",
                "rerun the same command after the input is repaired",
            )],
        ), EXIT_INPUT_ERROR
    open_conflicts = [c for c in plan["conflicts"] if c["status"] == "open"]
    conditions = [
        _condition(
            item["code"],
            "%s %s: %s <<>> %s" % (
                item["artifact"], item["unit"],
                item["side_a"].get("excerpt", ""), item["side_b"].get("excerpt", "")),
            "; ".join(item["candidates"]),
            "resolve the named records, then rerun merge-plan",
        ) for item in open_conflicts
    ]
    verdict = "refused" if open_conflicts else "ok"
    code = EXIT_REFUSED if open_conflicts else EXIT_OK
    payload = _payload("merge-plan", spec_dir, verdict, code, conditions)
    payload["plan"] = plan
    return payload, code


def action_merge_apply(args: argparse.Namespace, spec_dir: Path) -> Tuple[Dict[str, Any], int]:
    return _pending("merge-apply", spec_dir)


def evaluate_seal(args: argparse.Namespace, spec_dir: Path) -> Tuple[Dict[str, Any], int]:
    """C-005 judgment phase: read-only; computes every precondition, writes nothing."""
    return _pending("seal", spec_dir)


def apply_seal(args: argparse.Namespace, spec_dir: Path,
               evaluation: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    """C-005 write phase: one atomic batch; only reached when judgment passed."""
    return _pending("seal", spec_dir)


def action_seal(args: argparse.Namespace, spec_dir: Path) -> Tuple[Dict[str, Any], int]:
    evaluation, code = evaluate_seal(args, spec_dir)
    if evaluation["verdict"] != "ok":
        return evaluation, code
    return apply_seal(args, spec_dir, evaluation)


def action_archive_gate(args: argparse.Namespace, spec_dir: Path) -> Tuple[Dict[str, Any], int]:
    return _pending("archive-gate", spec_dir)


HANDLERS = {
    "merge-plan": action_merge_plan,
    "merge-apply": action_merge_apply,
    "seal": action_seal,
    "archive-gate": action_archive_gate,
}


# ---------------------------------------------------------------------------
# CLI surface (C-003 / C-004) and dispatch
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=ENGINE_NAME,
        description="Seal engine for /speckit.seal: merge-back, seal judgment and "
                    "archive admission.",
    )
    _sig_configure(
        parser,
        effects="merge-plan and archive-gate write nothing; merge-apply and seal write "
                "only within the allowlisted paths (the parent spec directory, one slice "
                "requirements.md marker line and recorded factory-doc resolutions); a "
                "flag-only invocation writes nothing",
        codes="0 success or idempotent; 1 a precondition refused; 2 an input or "
              "environment error",
    )
    parser.add_argument("--action", required=True, choices=ACTIONS,
                        help="one of the four closed actions")
    parser.add_argument("--spec-dir", required=True,
                        help="target spec directory (required, no default)")
    parser.add_argument("--repo", default=None,
                        help="repository root for state and registry lookups "
                             "(default: the invocation cwd)")
    parser.add_argument("--feature-detail", default=None,
                        help="override the feature-detail carrier path (test fixtures only)")
    parser.add_argument("--feature-registry", default=None,
                        help="override the feature-registry path (test fixtures only)")
    parser.add_argument("--json", action="store_true",
                        help="emit one stable JSON payload instead of the human rendering")
    _sig_add_version(parser)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    line = list(sys.argv[1:] if argv is None else argv)
    _sig_guard(line, declared=DECLARED_OPTIONS)
    parser = build_parser()
    args = parser.parse_args(line)

    if args.action in WRITE_ACTIONS and is_mirror_copy():
        payload = _payload(
            args.action, None, "error", EXIT_INPUT_ERROR,
            [_condition(
                MIRROR_CODE,
                "this engine is the .specify/scripts/python/ mirror copy; write actions "
                "MUST run from the framework source to keep the pair byte-identical",
                "run scripts/python/seal-utils.py from the framework source tree",
                "rerun the same command against the framework source copy",
            )],
        )
        render(payload, args.json)
        return EXIT_INPUT_ERROR

    spec_dir = resolve_spec_dir(args.spec_dir)
    if spec_dir is None:
        payload = _payload(
            args.action, None, "error", EXIT_INPUT_ERROR,
            [_condition(
                SPEC_DIR_CODE,
                "not a spec directory (missing, or carries no %s): %s"
                % (SPEC_CONTRACT_FILE, args.spec_dir),
                "pass --spec-dir pointing at a directory that contains %s"
                % SPEC_CONTRACT_FILE,
                "rerun the same command with a corrected --spec-dir",
            )],
        )
        render(payload, args.json)
        return EXIT_INPUT_ERROR

    payload, code = HANDLERS[args.action](args, spec_dir)
    render(payload, args.json)
    return code


if __name__ == "__main__":
    sys.exit(main())
