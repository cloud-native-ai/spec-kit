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
import hashlib
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
        from script_interface_cli import (add_version_argument, configure_parser,
                                          guard_argv, version_text)
        return configure_parser, guard_argv, add_version_argument, version_text
    except ImportError:  # a bare copy without the helper still runs its actions
        def _configure(parser, **_kwargs):
            return parser

        def _guard(_argv=None, declared=None, **_kwargs):
            return None

        def _add_version(parser):
            return parser

        def _version_text(script_name, _start=None):
            return "%s %s" % (Path(script_name).name, "unknown")

        return _configure, _guard, _add_version, _version_text


_sig_configure, _sig_guard, _sig_add_version, _sig_version_text = _import_guard()


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
    applied = payload.get("apply")
    if isinstance(applied, dict):
        print("  manifest: %s" % applied["manifest"])
        print("  idempotent: %s" % ("yes" if applied["idempotent"] else "no"))
        print("  slices: %s" % (", ".join(applied["slices"]) or "-"))
        print("  writes: %d" % len(applied["writes"]))
        checks = applied.get("checks", {})
        print("  checks: id_continuity=%s open_rows=%s duplicate_ids=%s "
              "dangling_refs=%s dated_records_stable=%s" % (
                  checks.get("id_continuity", "-"), checks.get("open_rows", "-"),
                  checks.get("duplicate_ids", "-"), checks.get("dangling_refs", "-"),
                  checks.get("dated_record_hashes_stable", "-")))
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


# ---------------------------------------------------------------------------
# Merge-apply surface (C-013 … C-023): deterministic writes into the parent
# ---------------------------------------------------------------------------

MANIFEST_NAME = "merge-manifest.json"
SUPERSEDE_HEADING = "## Superseded pre-split record"
MERGE_APPENDIX_HEADING = "## Merged from slices"
POINTER_BEGIN = "<!-- begin: merge-apply aggregated pointer view (generated) -->"
POINTER_END = "<!-- end: merge-apply aggregated pointer view -->"
SLICE_STATUS_RE = re.compile(r"^(SC-\d{3}|FR-\d{3})_status=(.*)$")
_ID_TOKEN_RE = re.compile(r"\b(?:STR-\d{3}|FR-\d{3}|SC-\d{3}|C-\d{3}|T\d{3}|E\d+)\b")
_MERGED_INTO_RE = re.compile(r"^\*\*Merged into\*\*:\s*(.+?)\s*$")
_TASK_ANY_RE = re.compile(r"^-\s+\[(.)\]\s+T\d{3}\b")


def _ensure_newline(text: str) -> str:
    stripped = text.rstrip("\n")
    return stripped + "\n" if stripped else ""


def _slice_rewrite_map(id_maps: Dict[str, list], slug: str,
                       contract_file: Optional[str] = None) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for family in ("FR", "SC", "STR", "T", "E"):
        for entry in id_maps.get(family, []):
            if entry["slice"] == slug:
                mapping[entry["slice_id"]] = entry["parent_id"]
    for entry in id_maps.get("C", []):
        if entry["slice"] == slug and (contract_file is None
                                       or entry.get("file") == contract_file):
            mapping[entry["slice_id"]] = entry["parent_id"]
    return mapping


def _rewrite_ids(text: str, mapping: Dict[str, str]) -> str:
    if not mapping:
        return text

    def _replace(match):
        return mapping.get(match.group(0), match.group(0))

    return _ID_TOKEN_RE.sub(_replace, text)


def _raw_definition_line(text: str, slice_id: str) -> Optional[str]:
    for line in text.splitlines():
        match = re.match(r"^-\s+\*\*(FR|SC)-(\d{3})\*\*", line)
        if match and "%s-%s" % (match.group(1), match.group(2)) == slice_id:
            return line
    return None


def _h2_sections(text: str):
    sections = []
    current = None
    for line in text.splitlines():
        if re.match(r"^##\s+", line):
            current = [re.sub(r"^##\s+", "", line).strip(), []]
            sections.append(current)
        elif current is not None:
            current[1].append(line)
    return [(heading, body) for heading, body in sections]


def _demote_heading(line: str) -> str:
    return "#" + line if re.match(r"^#{1,6}\s", line) else line


def _summary_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped[:1] in ("-", "*"):
            stripped = stripped.lstrip("-*").strip()
        return stripped
    return "(no summary line)"


def _write_if_changed(path: Path, content: str, written: list, repo: Path) -> bool:
    data = content.encode("utf-8")
    if path.is_file() and path.read_bytes() == data:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    written.append(_rel_path(repo, path))
    return True


def _engine_version() -> str:
    try:
        return _sig_version_text(ENGINE_NAME).rsplit(" ", 1)[-1]
    except (OSError, ValueError):
        return "unknown"


def _dated_files(ordered) -> list:
    paths = []
    for item in ordered:
        base = item["path"]
        for name in ("review.md", "code-review.md", "verification.md"):
            if (base / name).is_file():
                paths.append(base / name)
        for dirname in DATED_RECORD_DIRS:
            if (base / dirname).is_dir():
                paths.extend(sorted(p for p in (base / dirname).rglob("*") if p.is_file()))
    return sorted(set(paths), key=lambda item: str(item))


def _dated_snapshot(ordered) -> Dict[str, str]:
    return {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in _dated_files(ordered)}


def _open_task_rows(text: str) -> list:
    rows = []
    for line_no, line in enumerate(text.splitlines(), 1):
        match = _TASK_ROW_RE.match(line)
        if match and match.group(1) in (" ", ">"):
            rows.append({"line": line_no, "text": line, "id": match.group(2)})
    return rows


def _deferred_recorded(item, task_id: str) -> bool:
    verification = item["path"] / "verification.md"
    if not verification.is_file():
        return False
    return any("deferred_tasks=" in line and task_id in line
               for line in _read_text(verification).splitlines())


def _unclosed_slice_rows(repo: Path, ordered) -> list:
    findings = []
    for item in ordered:
        tasks_path = item["path"] / "tasks.md"
        if not tasks_path.is_file():
            continue
        for line_no, line in enumerate(_read_text(tasks_path).splitlines(), 1):
            match = _TASK_ROW_RE.match(line)
            if not match:
                continue
            state = match.group(1)
            if state in (" ", ">"):
                findings.append((_rel_path(repo, tasks_path), line_no, match.group(2), state))
            elif state == "~" and not _deferred_recorded(item, match.group(2)):
                findings.append((_rel_path(repo, tasks_path), line_no, match.group(2), state))
    return findings


# --- per-artifact content builders -----------------------------------------

def _prose_content(repo, spec_dir, name, action, ordered, id_maps):
    parent_path = spec_dir / name
    parent_text = _read_text(parent_path) if parent_path.is_file() else ""
    contributors = [item for item in ordered if (item["path"] / name).is_file()]
    blocks = []
    for item in contributors:
        mapping = _slice_rewrite_map(id_maps, item["slug"])
        body = _rewrite_ids(_read_text(item["path"] / name), mapping).rstrip("\n")
        blocks.append("<!-- merged from %s (source: %s) -->\n\n%s" % (
            item["slug"], _rel_path(repo, item["path"] / name), body))
    if action == "create" or not parent_text:
        if not blocks:
            return None
        return _ensure_newline("\n\n".join(blocks))
    parent_headings = {heading for heading, _ in _h2_sections(parent_text)}
    appendix = []
    for item in contributors:
        mapping = _slice_rewrite_map(id_maps, item["slug"])
        slice_text = _rewrite_ids(_read_text(item["path"] / name), mapping)
        unique = [(heading, body) for heading, body in _h2_sections(slice_text)
                  if heading not in parent_headings]
        if not unique:
            continue
        block = ["<!-- source: %s -->" % item["slug"], ""]
        for heading, body in unique:
            block.append(_demote_heading("## " + heading))
            block.append("")
            lines = list(body)
            while lines and not lines[-1].strip():
                lines.pop()
            block.extend(_demote_heading(line) for line in lines)
            block.append("")
        appendix.append("\n".join(block).rstrip("\n"))
    if not appendix:
        return None
    return _ensure_newline(parent_text) + "\n" + MERGE_APPENDIX_HEADING + "\n\n" \
        + "\n\n".join(appendix) + "\n"


def _requirements_content(repo, spec_dir, action, ordered, id_maps):
    parent_path = spec_dir / "requirements.md"
    if not parent_path.is_file():
        return _prose_content(repo, spec_dir, "requirements.md", action, ordered, id_maps)
    parent_text = _read_text(parent_path)
    lines = parent_text.splitlines()
    anchors: Dict[int, list] = {}
    for family in ("FR", "SC"):
        appended_lines = []
        for entry in id_maps.get(family, []):
            if entry["kind"] != "appended":
                continue
            item = next(i for i in ordered if i["slug"] == entry["slice"])
            raw = _raw_definition_line(item["text"], entry["slice_id"])
            if raw is None:
                continue
            appended_lines.append(_rewrite_ids(
                raw, _slice_rewrite_map(id_maps, entry["slice"])))
        if not appended_lines:
            continue
        anchor = max((index for index, line in enumerate(lines)
                      if re.match(r"^-\s+\*\*%s-\d{3}\*\*" % family, line)),
                     default=len(lines))
        anchors.setdefault(anchor, []).extend(appended_lines)
    string_rows = []
    for entry in id_maps.get("STR", []):
        if entry["kind"] != "appended":
            continue
        item = next(i for i in ordered if i["slug"] == entry["slice"])
        record = _parse_shared_strings(item["text"]).get(entry["slice_id"])
        if record is None:
            continue
        string_rows.append("| `%s` | `\"%s\"` | appended from %s by merge |" % (
            entry["parent_id"], record["literal"], entry["slice"]))
    if string_rows:
        body, start = _section(parent_text, r"Shared Strings")
        if body is not None:
            offsets = [offset for offset, line in enumerate(body) if line.startswith("|")]
            if offsets:
                anchor = start + 1 + max(offsets)
            else:
                anchor = start + len(body)
            anchors.setdefault(anchor, []).extend(string_rows)
        else:
            anchors.setdefault(len(lines), []).extend(
                ["", "## Shared Strings", "",
                 "| String ID | Value (verbatim) | Consumed by |",
                 "|-----------|------------------|-------------|"] + string_rows)
    if not anchors:
        return None
    out = []
    for index, line in enumerate(lines):
        out.append(line)
        out.extend(anchors.get(index, []))
    out.extend(anchors.get(len(lines), []))
    return _ensure_newline("\n".join(out))


def _tasks_content(repo, spec_dir, action, ordered, id_maps, carriers):
    parent_path = spec_dir / "tasks.md"
    parent_text = _read_text(parent_path) if parent_path.is_file() else ""
    kept = []
    for line in parent_text.splitlines():
        match = _TASK_ROW_RE.match(line)
        if match and match.group(1) in (" ", ">"):
            continue
        kept.append(line)
    appended = []
    for item in ordered:
        tasks_path = item["path"] / "tasks.md"
        if not tasks_path.is_file():
            continue
        mapping = _slice_rewrite_map(id_maps, item["slug"])
        for line in _read_text(tasks_path).splitlines():
            if _TASK_ROW_RE.match(line):
                appended.append(_rewrite_ids(line, mapping))
    anchor_rows = [index for index, line in enumerate(kept) if _TASK_ROW_RE.match(line)]
    insert_at = anchor_rows[-1] + 1 if anchor_rows else len(kept)
    out = kept[:insert_at] + appended + kept[insert_at:]
    superseded = _open_task_rows(parent_text)
    if superseded:
        carrier_note = ", ".join(carriers) if carriers else "-"
        block = ["", SUPERSEDE_HEADING, ""]
        for row in superseded:
            block.append("> " + row["text"])
            block.append(">")
            block.append("> superseded: tasks.md:%d (original position); superseded_by: "
                         "%s line 0 (whole-file fact); carriers: %s" % (
                             row["line"], MANIFEST_NAME, carrier_note))
            block.append("")
        out.extend(block)
    if not appended and not superseded and action == "keep":
        return None
    return _ensure_newline("\n".join(out))


def _contract_content(repo, spec_dir, fname, action, ordered, id_maps):
    unit = "contracts/" + fname
    parent_path = spec_dir / "contracts" / fname
    contributors = [item for item in ordered
                    if (item["path"] / "contracts" / fname).is_file()]
    if action == "create" or not parent_path.is_file():
        blocks = []
        for item in contributors:
            mapping = _slice_rewrite_map(id_maps, item["slug"], contract_file=unit)
            body = _rewrite_ids(
                _read_text(item["path"] / "contracts" / fname), mapping).rstrip("\n")
            blocks.append("<!-- merged from %s (source: %s) -->\n\n%s" % (
                item["slug"], _rel_path(repo, item["path"] / "contracts" / fname), body))
        return _ensure_newline("\n\n".join(blocks)) if blocks else None
    parent_text = _read_text(parent_path)
    appended = []
    for item in contributors:
        mapping = _slice_rewrite_map(id_maps, item["slug"], contract_file=unit)
        for entry in id_maps.get("C", []):
            if entry["slice"] != item["slug"] or entry.get("file") != unit:
                continue
            if entry["kind"] != "appended":
                continue
            raw = next((line for line in
                        _read_text(item["path"] / "contracts" / fname).splitlines()
                        if re.match(r"^\*\*%s\*\*" % re.escape(entry["slice_id"]), line)),
                       None)
            if raw is not None:
                appended.append(_rewrite_ids(raw, mapping))
    if not appended:
        return None
    return _ensure_newline(parent_text) + "\n" + "\n".join(appended) + "\n"


def _data_model_content(repo, spec_dir, action, ordered, id_maps):
    parent_path = spec_dir / "data-model.md"
    if action == "create" or not parent_path.is_file():
        return _prose_content(repo, spec_dir, "data-model.md", action, ordered, id_maps)
    parent_text = _read_text(parent_path)
    lines = parent_text.splitlines()
    appended = []
    for entry in id_maps.get("E", []):
        if entry["kind"] != "appended":
            continue
        item = next(i for i in ordered if i["slug"] == entry["slice"])
        mapping = _slice_rewrite_map(id_maps, entry["slice"])
        for line in _read_text(item["path"] / "data-model.md").splitlines():
            match = re.match(r"^\|\s*(E\d+)\s*\|", line)
            if match and match.group(1) == entry["slice_id"]:
                appended.append(_rewrite_ids(line, mapping))
    if not appended:
        return None
    rows = [index for index, line in enumerate(lines) if re.match(r"^\|\s*E\d+\s*\|", line)]
    insert_at = rows[-1] + 1 if rows else len(lines)
    out = lines[:insert_at] + appended + lines[insert_at:]
    return _ensure_newline("\n".join(out))


def _dated_pointer_view(repo, row):
    blocks = []
    for rel in row.get("pointer", {}).get("paths", []):
        path = repo / rel
        if not path.is_file():
            continue
        summary = next((line.strip() for line in _read_text(path).splitlines()
                        if line.strip()), "(empty record)")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        blocks.append("summary: %s\npointer: %s\nsha256: %s" % (summary, rel, digest))
    return _ensure_newline("\n\n".join(blocks)) if blocks else None


def _directory_file_content(repo, spec_dir, dirname, fname, action, row,
                            ordered, id_maps):
    if row.get("pointer_view"):
        return _dated_pointer_view(repo, row)
    parent_path = spec_dir / dirname / fname
    contributors = [item for item in ordered
                    if (item["path"] / dirname / fname).is_file()]
    blocks = []
    for item in contributors:
        mapping = _slice_rewrite_map(id_maps, item["slug"])
        body = _rewrite_ids(
            _read_text(item["path"] / dirname / fname), mapping).rstrip("\n")
        blocks.append("<!-- merged from %s (source: %s) -->\n\n%s" % (
            item["slug"], _rel_path(repo, item["path"] / dirname / fname), body))
    if action == "create" or not parent_path.is_file():
        return _ensure_newline("\n\n".join(blocks)) if blocks else None
    if not blocks:
        return None
    return _ensure_newline(_read_text(parent_path).rstrip("\n") + "\n\n"
                           + "\n\n".join(blocks))


def _pointer_view_block(repo, name, ordered, id_maps):
    if name == "verification.md":
        lines = []
        for item in ordered:
            path = item["path"] / "verification.md"
            if not path.is_file():
                continue
            mapping = _slice_rewrite_map(id_maps, item["slug"])
            for line in _read_text(path).splitlines():
                match = SLICE_STATUS_RE.match(re.sub(r"^[-*]\s+", "", line.strip()))
                if not match:
                    continue
                parent_id = mapping.get(match.group(1), match.group(1))
                lines.append("%s_status=%s" % (parent_id, match.group(2).strip()))
                lines.append("%s_note=%s (%s local row %s)" % (
                    parent_id, _rel_path(repo, path), item["slug"], match.group(1)))
        return lines or ["(no slice verification records in this merge)"]
    lines = []
    for item in ordered:
        path = item["path"] / name
        if not path.is_file():
            continue
        lines.append("- %s: %s — %s" % (
            item["slug"], _rel_path(repo, path), _summary_line(_read_text(path))))
    return lines or ["- (no slice %s records in this merge)" % name]


def _pointer_view_content(repo, spec_dir, name, action, ordered, id_maps):
    block = _pointer_view_block(repo, name, ordered, id_maps)
    parent_path = spec_dir / name
    parent_text = _read_text(parent_path) if parent_path.is_file() else ""
    if action == "create" or not parent_text:
        title = {"verification.md": "# Verification — aggregated pointer view",
                 "review.md": "# Review — aggregated pointer view",
                 "code-review.md": "# Code review — aggregated pointer view"}[name]
        return _ensure_newline("%s (%s)\n\n%s\n" % (
            title, spec_dir.name, "\n".join(block)))
    generated = POINTER_BEGIN + "\n" + "\n".join(block) + "\n" + POINTER_END
    if POINTER_BEGIN in parent_text and POINTER_END in parent_text:
        prefix, _, rest = parent_text.partition(POINTER_BEGIN)
        _, _, suffix = rest.partition(POINTER_END)
        return _ensure_newline(prefix + generated + suffix)
    return _ensure_newline(parent_text) + "\n" + generated + "\n"


def _artifact_content(repo, spec_dir, row, ordered, id_maps, carriers):
    name, action = row["name"], row["action"]
    if "/" in name:
        dirname, fname = name.split("/", 1)
        if dirname == "contracts":
            return _contract_content(repo, spec_dir, fname, action, ordered, id_maps)
        return _directory_file_content(repo, spec_dir, dirname, fname, action, row,
                                       ordered, id_maps)
    if name == "requirements.md":
        return _requirements_content(repo, spec_dir, action, ordered, id_maps)
    if name == "tasks.md":
        return _tasks_content(repo, spec_dir, action, ordered, id_maps, carriers)
    if name in POINTER_VIEW_CANDIDATES:
        return _pointer_view_content(repo, spec_dir, name, action, ordered, id_maps)
    if name == "data-model.md":
        return _data_model_content(repo, spec_dir, action, ordered, id_maps)
    if name in ("plan.md", "research.md", "quickstart.md", "feature-ref.md"):
        return _prose_content(repo, spec_dir, name, action, ordered, id_maps)
    return None


# --- the merge state, the slice marker and factory-doc rewrites -------------

def _slice_marker_content(spec_dir: Path, item) -> Optional[str]:
    path = item["path"] / "requirements.md"
    text = _read_text(path)
    if any(line.startswith("**Merged into**:") for line in text.splitlines()):
        return None
    marker = "**Merged into**: .specify/specs/%s（%s）" % (spec_dir.name, MANIFEST_NAME)
    lines = text.split("\n")
    status = next((index for index, line in enumerate(lines)
                   if line.startswith("**Status**:")), None)
    if status is not None:
        insert_at = status + 1
    else:
        insert_at = next((index for index, line in enumerate(lines)
                          if re.match(r"^##\s+", line)), len(lines))
    lines.insert(insert_at, marker)
    return "\n".join(lines)


def _factory_writes(repo: Path, plan):
    grouped: Dict[str, list] = {}
    for ref in plan.get("factory_doc_refs", []):
        if ref.get("status") != "resolved":
            continue
        if (ref.get("resolution") or {}).get("kind") != "repoint":
            continue
        grouped.setdefault(ref["path"], []).append(ref)
    writes, resolutions = [], []
    for rel, refs in sorted(grouped.items()):
        path = repo / rel
        if not path.is_file():
            continue
        lines = _read_text(path).split("\n")
        for ref in sorted(refs, key=lambda item: item["line"]):
            index = ref["line"] - 1
            if index < 0 or index >= len(lines):
                continue
            before = lines[index]
            after = before.replace("[[%s]]" % ref["token"],
                                   "[[%s]]" % ref["parent_id"])
            if after == before:
                continue
            lines[index] = after
            resolutions.append({"path": rel, "line": ref["line"], "before": before,
                                "after": after, "kind": "repoint"})
        writes.append((path, "\n".join(lines)))
    return writes, resolutions


def _merge_state(spec_dir: Path, ordered):
    manifest_path = spec_dir / MANIFEST_NAME
    manifest = None
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except ValueError:
            manifest = None
    marks = []
    for item in ordered:
        found = [match.group(1) for line in
                 _read_text(item["path"] / "requirements.md").splitlines()
                 if (match := _MERGED_INTO_RE.match(line))]
        if len(found) > 1 or (found and spec_dir.name not in found[0]):
            raise ValueError(
                "slice %s carries an unusable `**Merged into**` marker" % item["slug"])
        marks.append(bool(found))
    if any(marks) and not all(marks):
        raise ValueError("some slices are marked merged and others are not; "
                         "partial merge state cannot be merged again deterministically")
    if ordered:
        completed = all(marks)
        if completed and (manifest is None or manifest.get("spec") != spec_dir.name):
            raise ValueError("slices are marked merged but %s is missing or foreign"
                             % MANIFEST_NAME)
        return completed, manifest
    return manifest is not None, manifest


# --- the manifest and its post-merge checks --------------------------------

def _continuous(numbers) -> bool:
    values = sorted(set(numbers))
    return not values or values == list(range(1, values[-1] + 1))


def _scan_merged_checks(spec_dir: Path, dated_stable: bool) -> Dict[str, Any]:
    requirements = _read_text(spec_dir / "requirements.md")
    defs: Dict[str, list] = {"FR": [], "SC": []}
    for line in requirements.splitlines():
        match = re.match(r"^-\s+\*\*(FR|SC)-(\d{3})\*\*", line)
        if match:
            defs[match.group(1)].append(int(match.group(2)))
    strings = _parse_shared_strings(requirements)
    string_numbers = [int(string_id.split("-")[1]) for string_id in strings]
    continuity = (_continuous(defs["FR"]) and _continuous(defs["SC"])
                  and _continuous(string_numbers))
    duplicates = sum(len(values) - len(set(values)) for values in defs.values())
    duplicates += len(string_numbers) - len(set(string_numbers))

    tasks_path = spec_dir / "tasks.md"
    tasks_text = _read_text(tasks_path) if tasks_path.is_file() else ""
    task_numbers, open_rows = [], 0
    for line in tasks_text.splitlines():
        match = _TASK_ROW_RE.match(line)
        if not match:
            continue
        task_numbers.append(int(match.group(2)[1:]))
        if match.group(1) in (" ", ">"):
            open_rows += 1
    continuity = continuity and _continuous(task_numbers)
    duplicates += len(task_numbers) - len(set(task_numbers))

    texts = [requirements, tasks_text]
    contracts_dir = spec_dir / "contracts"
    if contracts_dir.is_dir():
        for contract in sorted(contracts_dir.glob("*.md")):
            texts.append(_read_text(contract))
            clause_numbers = [int(clause["id"].split("-")[1])
                              for clause in _contract_clauses(contract)]
            continuity = continuity and _continuous(clause_numbers)
            duplicates += len(clause_numbers) - len(set(clause_numbers))
    model_path = spec_dir / "data-model.md"
    if model_path.is_file():
        texts.append(_read_text(model_path))
        entity_numbers = [int(entity["id"][1:]) for entity in _entity_rows(model_path)]
        continuity = continuity and _continuous(entity_numbers)
        duplicates += len(entity_numbers) - len(set(entity_numbers))

    defined_fr = set(defs["FR"])
    defined_sc = set(defs["SC"])
    dangling = 0
    for text in texts:
        for line in text.splitlines():
            for match in re.finditer(r"\bFR-(\d{3})\b", line):
                if int(match.group(1)) not in defined_fr:
                    dangling += 1
            for match in re.finditer(r"\bSC-(\d{3})\b", line):
                if int(match.group(1)) not in defined_sc:
                    dangling += 1
            for match in _STR_REF_RE.finditer(line):
                if match.group(1) not in strings:
                    dangling += 1
    return {
        "id_continuity": "pass" if continuity else "fail",
        "duplicate_ids": duplicates,
        "dangling_refs": dangling,
        "open_rows": open_rows,
        "dated_record_hashes_stable": dated_stable,
    }


def _manifest_document(repo: Path, spec_dir: Path, plan, dispositions,
                       resolutions, checks) -> Dict[str, Any]:
    artifacts = []
    for row in plan["artifacts"]:
        entry = dict(row)
        entry["checks"] = {}
        if row["name"] == "requirements.md":
            entry["checks"] = {"id_continuity": checks["id_continuity"],
                               "duplicate_ids": checks["duplicate_ids"],
                               "dangling_refs": checks["dangling_refs"]}
        elif row["name"] == "tasks.md":
            entry["checks"] = {"open_rows": checks["open_rows"]}
        artifacts.append(entry)
    merge = {"status": "merged"}
    if not plan["slices"]:
        merge = {
            "status": "not-applicable",
            "basis": "the slice set is empty: no directory in `.specify/specs/` "
                     "satisfies both the name-family and parent-declaration conditions",
        }
    return {
        "schema_version": 1,
        "spec": spec_dir.name,
        "merge": merge,
        "generated_by": {
            "engine": ENGINE_NAME,
            "version": _engine_version(),
            "command": "%s --action merge-apply --spec-dir %s" % (
                ENGINE_NAME, _rel_path(repo, spec_dir)),
        },
        "slices": plan["slices"],
        "artifacts": artifacts,
        "factory_doc_resolutions": resolutions,
        "id_maps": plan["id_maps"],
        "conflicts": [],
        "dispositions": dispositions,
        "checks": checks,
    }


def _apply_merge(repo: Path, spec_dir: Path, plan, ordered) -> Dict[str, Any]:
    id_maps = plan["id_maps"]
    carriers = [entry["carrier_tasks"] for entry in plan["slices"]
                if entry.get("carrier_tasks")]
    dated_before = _dated_snapshot(ordered)
    parent_tasks = spec_dir / "tasks.md"
    superseded_rows = (_open_task_rows(_read_text(parent_tasks))
                       if plan["slices"] and parent_tasks.is_file() else [])
    written: list = []

    outputs = []
    for row in plan["artifacts"]:
        if row["action"] in ("keep", "not-applicable"):
            continue
        content = _artifact_content(repo, spec_dir, row, ordered, id_maps, carriers)
        if content is not None:
            outputs.append((spec_dir / row["name"], content))
    for item in ordered:
        content = _slice_marker_content(spec_dir, item)
        if content is not None:
            outputs.append((item["path"] / "requirements.md", content))
    factory_writes, resolutions = _factory_writes(repo, plan)

    for path, content in outputs + factory_writes:
        _write_if_changed(path, content, written, repo)

    dated_stable = _dated_snapshot(ordered) == dated_before
    if not dated_stable:
        raise ValueError("a slice dated record changed during the run; "
                         "merge-apply must never rewrite measurements")
    checks = _scan_merged_checks(spec_dir, dated_stable)
    dispositions = []
    for row in superseded_rows:
        dispositions.append({
            "disposition": "supersede",
            "superseded": {"path": _rel_path(repo, parent_tasks), "line": row["line"]},
            "superseded_by": {"path": MANIFEST_NAME, "line": 0},
            "evidence": carriers,
            "guard_status": "replaced",
        })
    document = _manifest_document(repo, spec_dir, plan, dispositions, resolutions, checks)
    canonical = json.dumps(document, separators=(",", ":"), sort_keys=True,
                           ensure_ascii=False)
    document["digest"] = "sha256:" + hashlib.sha256(
        canonical.encode("utf-8")).hexdigest()
    manifest_path = spec_dir / MANIFEST_NAME
    _write_if_changed(manifest_path,
                      json.dumps(document, indent=2, sort_keys=True,
                                 ensure_ascii=False) + "\n",
                      written, repo)
    return {
        "manifest": _rel_path(repo, manifest_path),
        "idempotent": False,
        "slices": [item["slug"] for item in ordered],
        "writes": sorted(written),
        "dispositions": len(dispositions),
        "factory_doc_resolutions": len(resolutions),
        "checks": checks,
    }


def action_merge_apply(args: argparse.Namespace, spec_dir: Path) -> Tuple[Dict[str, Any], int]:
    repo = Path(args.repo).resolve() if args.repo else Path.cwd()
    try:
        plan = _build_plan(repo, spec_dir)
    except (OSError, ValueError, StopIteration) as exc:
        return _payload(
            "merge-apply", spec_dir, "error", EXIT_INPUT_ERROR,
            [_condition(
                "merge-apply-error",
                "the merge plan cannot be derived from this tree: %s" % exc,
                "repair the named input (spec tree, split record or registries)",
                "rerun the same command after the input is repaired",
            )],
        ), EXIT_INPUT_ERROR
    open_conflicts = [c for c in plan["conflicts"] if c["status"] == "open"]
    if open_conflicts:
        conditions = [
            _condition(
                item["code"],
                "%s %s: %s <<>> %s" % (
                    item["artifact"], item["unit"],
                    item["side_a"].get("excerpt", ""), item["side_b"].get("excerpt", "")),
                "; ".join(item["candidates"]),
                "resolve the named records, then rerun merge-apply",
            ) for item in open_conflicts
        ]
        payload = _payload("merge-apply", spec_dir, "refused", EXIT_REFUSED, conditions)
        payload["plan"] = plan
        return payload, EXIT_REFUSED

    slices, _excluded = _discover_slices(spec_dir)
    ordered = _derive_order(repo, spec_dir.name, slices)

    unclosed = _unclosed_slice_rows(repo, ordered)
    if unclosed:
        conditions = [
            _condition(
                "slice-unclosed",
                "%s:%d %s is not closed (state `- [%s]`)" % (path, line, task_id, state),
                "close the slice task, or record its `deferred_tasks=` entry in the "
                "slice verification.md",
                "rerun merge-apply after the slice is closed",
            ) for path, line, task_id, state in unclosed
        ]
        return _payload("merge-apply", spec_dir, "refused", EXIT_REFUSED,
                        conditions), EXIT_REFUSED

    try:
        completed, manifest = _merge_state(spec_dir, ordered)
    except ValueError as exc:
        return _payload(
            "merge-apply", spec_dir, "error", EXIT_INPUT_ERROR,
            [_condition(
                "merge-state-inconsistent",
                str(exc),
                "inspect the slice markers and merge-manifest.json; restore one "
                "coherent state before rerunning",
                "rerun merge-apply after the merged state is repaired",
            )],
        ), EXIT_INPUT_ERROR

    if completed:
        manifest = manifest if isinstance(manifest, dict) else {}
        payload = _payload("merge-apply", spec_dir, "ok", EXIT_OK, [])
        payload["apply"] = {
            "manifest": _rel_path(repo, spec_dir / MANIFEST_NAME),
            "idempotent": True,
            "slices": [item["slug"] for item in ordered],
            "writes": [],
            "dispositions": len(manifest.get("dispositions", [])),
            "factory_doc_resolutions": len(manifest.get("factory_doc_resolutions", [])),
            "checks": manifest.get("checks", {}),
        }
        return payload, EXIT_OK

    try:
        summary = _apply_merge(repo, spec_dir, plan, ordered)
    except (OSError, ValueError, StopIteration) as exc:
        return _payload(
            "merge-apply", spec_dir, "error", EXIT_INPUT_ERROR,
            [_condition(
                "merge-write-failed",
                "the merge could not be written deterministically: %s" % exc,
                "repair the named write failure, then rerun; the engine never "
                "rewrites a dated record",
                "rerun merge-apply after the failure is repaired",
            )],
        ), EXIT_INPUT_ERROR
    payload = _payload("merge-apply", spec_dir, "ok", EXIT_OK, [])
    payload["apply"] = summary
    return payload, EXIT_OK


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
