#!/usr/bin/env python3
"""Read-only role-edge judgement engine (Feature 095).

Rule owner: ``shared/definitions/superagent-definitions.md`` ([[STR-004]]). Executable
interface: ``contracts/role-edge-engine.contract.md`` C-1 … C-11; the parsed carrier
shapes and the violation predicates are owned by ``data-model.md`` § 2 / § 3 / § 5.

The engine answers, from existing run records only: does an edge exist between two
executors, which roles does each edge endpoint hold, how deep is each executor, and
which recorded anomaly exists. It is a projection — no store, no cache, no write point.

Carriers (read-only, no new store):

* team run-report mapping table inside ``## Execution Detail`` (``--teams-dir``);
* driver stage envelope sidecar ``prompt-<line>-<stage>.md.meta.json`` with its
  ``role_edge`` object, plus the four-piece artifact set when the sidecar is absent
  (``--state-dir``);
* ``run-agent`` dispatch record written by ``exec-quant.py --action collect-dispatch``,
  located at the store the record shape already declares — ``<state-dir>/../exec-quant/records`` (``run-agent-label`` carrier); the child's artifact triplet
  under ``--logs-dir`` confirms the dispatch took hold;
* the line registry (``--registry-dir``) cross-checks identities only; when absent it
  is empty, never fatal.

Implementation readings disclosed here, each pinned by the guarding contract test:

* ``dispatch_duty`` and ``role_declaration`` are declared only by carriers that carry
  the field. A carrier without the field contributes the edge defaults
  ``subagent`` / ``not-granted`` (the R3-02 disposition: the exec-quant dispatch record
  carries neither field, and a ``dispatch_duty: granted`` declaration is never inferred).
* ``attempt`` is the carrier's explicit attempt identifier when it records one, else the
  literal ``1`` (a retry is a new label, so an unrecorded attempt is a single attempt).
* When the same field of one edge is declared differently by two carriers, the conflict
  row names the field and every declaring path, and the edge value comes from the
  primary carrier precedence ``team-report`` > ``driver-spine`` > ``run-agent-label``
  (parent-side records are primary per FR-003) — the choice is never silent.
* ``state`` / ``last_activity`` / ``age`` / ``stale`` are digest-view fields, not engine
  output keys (data-model § 4); the digest renders them from its existing sources.

The additive ``--action settle`` (spec 106) is the settlement judgment face owned by
``superagent-definitions.md`` § Termination. It reads the same existing roots plus the
additive attempt/end/claim records, derives exactly one closed settlement value per
attempt from positive evidence, audits recorded claims against that derivation, and
emits the three closed settlement violation kinds. Its exit codes reuse the engine's
0 / 1 / 2: 0 every attempt judged (a correctly derived ``silent-end`` included),
1 settlement violations found, 2 ``unknown`` findings (unreadable evidence or a claimed
attempt with no resolvable start record). ``report`` and ``query`` are untouched.

Implementation readings disclosed here for the settlement action:

* A team-report row is a claim surface, never the seat's start record; the seat needs
  its own E2 ``<label>.attempt`` (carrier ``c3-team-seat``) or the same label's C1/C2
  start evidence, else it settles ``unknown`` with ``start-record-missing``.
* A parent-written ``<label>.settlement`` claim carrying ``value: cancelled`` is the
  explicit parent-side cancellation record; a version-less claim (or a 5-column report
  row) is annotated ``legacy`` and is exempt from the three settlement predicates while
  still deriving its value from raw evidence.
* For pid-less carriers the return channel counts as an open live leg only before the
  attempt's declared wait deadline; after it, no return and no live signal settle
  ``silent-end``.

Zero write points: this module opens no file for writing, creates no temporary file and
mutates no input. The importable interface (``read_carrier_inputs`` +
``evaluate_role_model``) is the single materialization the digest consumes.
"""

from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import os
import re
import sys
import time
from collections import deque
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
# Guard: the .specify/scripts/python/ mirror copy resolves parents[2] to `.specify`
# and would project every runtime path a second level deep.
if REPO_ROOT.name == ".specify":
    REPO_ROOT = REPO_ROOT.parent

SCHEMA_VERSION = 1

DECLARED_ROLES = ("subagent", "superagent")
DUTY_VALUES = ("granted", "not-granted")
DEFAULT_ROLE = "subagent"
DEFAULT_DUTY = "not-granted"
DUAL_ROLE_MARKER = "dual-role"
ROOT_LITERAL = "root"

VIOLATION_KINDS = (
    "self-dispatch",
    "dangling-parent",
    "unbacked-role-claim",
    "depth-inconsistent",
)

CARRIER_TEAM = "team-report"
CARRIER_DRIVER = "driver-spine"
CARRIER_RUN_AGENT = "run-agent-label"
CARRIER_PRECEDENCE = {CARRIER_TEAM: 3, CARRIER_DRIVER: 2, CARRIER_RUN_AGENT: 1}

MAPPING_COLUMNS = ("label", "role", "dispatch_duty", "workspace", "parent")
ROLE_EDGE_FIELDS = (
    "parent_identity",
    "child_label",
    "role_declaration",
    "dispatch_duty",
    "depth_position",
    "authority_ref",
    "return_channel",
)
TRIPLET_SUFFIXES = (".status", ".jsonl", ".live.log")
STAGE_ARTIFACT_PREFIXES = ("pid-", "status-", "log-", "heartbeat-")
SIDECAR_SUFFIX = ".md.meta.json"
SPINE_BLOCK_RE = re.compile(
    r"<!-- loop-state:begin -->(.*?)<!-- loop-state:end -->", re.S
)
SEPARATOR_CELL_RE = re.compile(r"^:?-{3,}:?$")
VERSION_RE = re.compile(r'^version\s*=\s*"([^"]+)"', re.M)


class RoleEdgeInputError(Exception):
    """Unreadable or malformed input; the CLI reports it as a named exit 2."""


# --------------------------------------------------------------------------- #
# small readers
# --------------------------------------------------------------------------- #
def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RoleEdgeInputError("unreadable input %s: %s" % (path, exc))


def _parse_spines(state_dir: Path) -> dict:
    spines = {}
    for path in sorted(state_dir.glob("*.md")):
        text = _read_text(path)
        match = SPINE_BLOCK_RE.search(text)
        if not match:
            continue
        fields = {}
        for line in match.group(1).splitlines():
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
        run_id = fields.get("run_id")
        if not run_id:
            continue
        spines[path.stem] = {
            "path": str(path),
            "line_id": path.stem,
            "run_id": run_id,
            "attempt": fields.get("attempt") or None,
        }
    return spines


def _tables_in_execution_detail(text: str):
    """Yield ``(header_cells, [(line_number, cells), ...])`` for the section's tables."""
    in_detail = False
    block = []
    start_line = 0
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("## "):
            if in_detail and block:
                yield _table_block(block, start_line)
                block = []
            in_detail = stripped == "## Execution Detail"
            continue
        if in_detail and stripped.startswith("|"):
            if not block:
                start_line = lineno
            block.append((lineno, stripped))
            continue
        if block:
            yield _table_block(block, start_line)
            block = []
    if block:
        yield _table_block(block, start_line)


def _table_block(block, start_line):
    header = _split_table_row(block[0][1])
    rows = []
    for lineno, line in block[1:]:
        cells = _split_table_row(line)
        if all(SEPARATOR_CELL_RE.match(cell) for cell in cells if cell):
            continue
        rows.append((lineno, cells))
    return header, rows, start_line


def _split_table_row(line: str):
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip() for cell in text.split("|")]


def _parse_team_rows(teams_dir: Path) -> list:
    rows = []
    for path in sorted(teams_dir.glob("*/runs/*-report.md")):
        text = _read_text(path)
        for header, table_rows, _start in _tables_in_execution_detail(text):
            if tuple(header) != MAPPING_COLUMNS:
                continue
            for lineno, cells in table_rows:
                if len(cells) != len(MAPPING_COLUMNS):
                    raise RoleEdgeInputError(
                        "malformed carrier row in %s:%d: expected %d columns, found %d"
                        % (path, lineno, len(MAPPING_COLUMNS), len(cells))
                    )
                label, role, duty, _workspace, parent = cells
                if not label or not parent:
                    raise RoleEdgeInputError(
                        "malformed carrier row in %s:%d: label and parent are required"
                        % (path, lineno)
                    )
                if role not in DECLARED_ROLES:
                    raise RoleEdgeInputError(
                        "malformed carrier row in %s:%d: role %r is outside {%s}"
                        % (path, lineno, role, ", ".join(DECLARED_ROLES))
                    )
                if duty not in DUTY_VALUES:
                    raise RoleEdgeInputError(
                        "malformed carrier row in %s:%d: dispatch_duty %r is outside {%s}"
                        % (path, lineno, duty, ", ".join(DUTY_VALUES))
                    )
                rows.append(
                    {
                        "carrier": CARRIER_TEAM,
                        "path": str(path),
                        "line": lineno,
                        "parent_raw": parent,
                        "child_raw": label,
                        "attempt": "1",
                        "role_declaration": role,
                        "dispatch_duty": duty,
                        "depth_position": None,
                    }
                )
    return rows


def _line_for_stem(stem: str, line_ids) -> str:
    candidates = [
        line_id
        for line_id in line_ids
        if stem == line_id or stem.startswith(line_id + "-")
    ]
    if not candidates:
        return None
    return max(candidates, key=len)


def _parse_sidecars(state_dir: Path, spines: dict, line_ids) -> tuple:
    rows = []
    stems = set()
    for path in sorted(state_dir.glob("prompt-*" + SIDECAR_SUFFIX)):
        stem = path.name[len("prompt-") : -len(SIDECAR_SUFFIX)]
        stems.add(stem)
        text = _read_text(path)
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise RoleEdgeInputError("malformed carrier record %s: %s" % (path, exc))
        if not isinstance(payload, dict):
            raise RoleEdgeInputError(
                "malformed carrier record %s: top level is not an object" % (path,)
            )
        role_edge = payload.get("role_edge")
        if role_edge is None:
            continue
        if not isinstance(role_edge, dict):
            raise RoleEdgeInputError(
                "malformed carrier record %s: role_edge is not an object" % (path,)
            )
        for field in ROLE_EDGE_FIELDS:
            if field not in role_edge:
                raise RoleEdgeInputError(
                    "malformed carrier record %s: role_edge is missing %r"
                    % (path, field)
                )
        role = role_edge["role_declaration"]
        duty = role_edge["dispatch_duty"]
        depth_position = role_edge["depth_position"]
        if role not in DECLARED_ROLES:
            raise RoleEdgeInputError(
                "malformed carrier record %s: role_edge.role_declaration %r is outside {%s}"
                % (path, role, ", ".join(DECLARED_ROLES))
            )
        if duty not in DUTY_VALUES:
            raise RoleEdgeInputError(
                "malformed carrier record %s: role_edge.dispatch_duty %r is outside {%s}"
                % (path, duty, ", ".join(DUTY_VALUES))
            )
        if (
            not isinstance(depth_position, int)
            or isinstance(depth_position, bool)
            or depth_position < 0
        ):
            raise RoleEdgeInputError(
                "malformed carrier record %s: role_edge.depth_position %r is not a "
                "non-negative integer" % (path, depth_position)
            )
        parent_raw = role_edge["parent_identity"]
        child_raw = role_edge["child_label"]
        if not isinstance(parent_raw, str) or not parent_raw:
            raise RoleEdgeInputError(
                "malformed carrier record %s: role_edge.parent_identity is empty" % (path,)
            )
        if not isinstance(child_raw, str) or not child_raw:
            raise RoleEdgeInputError(
                "malformed carrier record %s: role_edge.child_label is empty" % (path,)
            )
        line_id = _line_for_stem(stem, line_ids)
        spine = spines.get(line_id) if line_id else None
        attempt = (spine or {}).get("attempt") or "1"
        rows.append(
            {
                "carrier": CARRIER_DRIVER,
                "path": str(path),
                "line": None,
                "parent_raw": parent_raw,
                "child_raw": child_raw,
                "attempt": str(attempt),
                "role_declaration": role,
                "dispatch_duty": duty,
                "depth_position": depth_position,
            }
        )
    return rows, stems


def _parse_stage_artifacts(state_dir: Path, spines: dict, line_ids, sidecar_stems) -> list:
    """Derive the edge from the four-piece artifact set when the sidecar is absent."""
    rows = []
    seen = set()
    for path in sorted(state_dir.iterdir()):
        if not path.is_file():
            continue
        prefix = next(
            (item for item in STAGE_ARTIFACT_PREFIXES if path.name.startswith(item)),
            None,
        )
        if prefix is None:
            continue
        rest = path.name[len(prefix) :]
        if rest.endswith(".log"):
            rest = rest[:-4]
        line_id = _line_for_stem(rest, line_ids)
        if line_id is None:
            continue
        stage = rest[len(line_id) :].lstrip("-")
        if not stage or rest in sidecar_stems or rest in seen:
            continue
        spine = spines.get(line_id)
        if spine is None:
            continue
        seen.add(rest)
        rows.append(
            {
                "carrier": CARRIER_DRIVER,
                "path": str(path),
                "line": None,
                "parent_raw": spine["run_id"],
                "child_raw": rest,
                "attempt": str(spine.get("attempt") or "1"),
                "role_declaration": None,
                "dispatch_duty": None,
                "depth_position": None,
            }
        )
    return rows


def _scan_triplets(logs_dir: Path) -> dict:
    labels = {}
    for path in sorted(logs_dir.iterdir()):
        if not path.is_file():
            continue
        for suffix in TRIPLET_SUFFIXES:
            if path.name.endswith(suffix):
                label = path.name[: -len(suffix)]
                labels.setdefault(label, []).append(str(path))
                break
    return labels


def _parse_registry(registry_dir) -> tuple:
    if registry_dir is None:
        return [], "absent", [], []
    directory = Path(registry_dir)
    if not directory.is_dir():
        return [], "absent", [], []
    entries = []
    unreadable = []
    payloads = []
    for path in sorted(directory.glob("*.json")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            unreadable.append(str(path))
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            unreadable.append(str(path))
            continue
        if not isinstance(payload, dict):
            unreadable.append(str(path))
            continue
        # The parsed payload rides the same read: the digest's legacy line rows derive from it, so the registry
        # root is read once and both views (line rows, role cross-check) consume that one pass.
        payloads.append({"path": str(path), "payload": payload})
        line_id = payload.get("line_id")
        if not isinstance(line_id, str) or not line_id:
            continue
        entries.append({"path": str(path), "line_id": line_id})
    return entries, "present", unreadable, payloads


def _parse_dispatch_records(state_dir: Path, triplet_labels) -> tuple:
    store = state_dir.parent / "exec-quant" / "records"
    rows = []
    unconfirmed = 0
    if not store.is_dir():
        return rows, False, unconfirmed, str(store)
    for path in sorted(store.glob("*.json")):
        text = _read_text(path)
        try:
            record = json.loads(text)
        except json.JSONDecodeError as exc:
            raise RoleEdgeInputError("malformed carrier record %s: %s" % (path, exc))
        if not isinstance(record, dict):
            raise RoleEdgeInputError(
                "malformed carrier record %s: top level is not an object" % (path,)
            )
        if record.get("unit_type") != "agent":
            continue
        unit_id = record.get("unit_id")
        label = record.get("run_id")
        if not isinstance(unit_id, str) or not unit_id.startswith("agent:"):
            continue
        if not isinstance(label, str) or not label:
            raise RoleEdgeInputError(
                "malformed carrier record %s: run_id is missing" % (path,)
            )
        if label not in triplet_labels:
            unconfirmed += 1
            continue
        rows.append(
            {
                "carrier": CARRIER_RUN_AGENT,
                "path": str(path),
                "line": None,
                "parent_raw": unit_id[len("agent:") :],
                "child_raw": label,
                "attempt": "1",
                "role_declaration": None,
                "dispatch_duty": None,
                "depth_position": None,
            }
        )
    return rows, True, unconfirmed, str(store)


def _default_registry_dir():
    """Ask the owning engine for the default registry root; never restate its chain."""
    candidates = (
        REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "line-registry.py",
        REPO_ROOT / ".specify" / "skills" / "sdd-loop-driver" / "scripts" / "line-registry.py",
    )
    for engine in candidates:
        if not engine.is_file():
            continue
        try:
            spec = importlib.util.spec_from_file_location(
                "line_registry_owner", str(engine)
            )
            if spec is None or spec.loader is None:
                return None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            resolver = getattr(module, "resolve_registry_dir", None)
            if resolver is None:
                return None
            return resolver()
        except Exception:  # an unreadable owner narrows cross-checking, never fatal
            return None
    return None


# --------------------------------------------------------------------------- #
# importable interface (contract C-1)
# --------------------------------------------------------------------------- #
def read_carrier_inputs(*, state_dir, teams_dir, logs_dir, registry_dir=None) -> dict:
    """Parse the three carrier forms plus the registry cross-check into one snapshot."""
    state_path = Path(state_dir)
    teams_path = Path(teams_dir)
    logs_path = Path(logs_dir)
    for option, path in (
        ("--state-dir", state_path),
        ("--teams-dir", teams_path),
        ("--logs-dir", logs_path),
    ):
        if not path.is_dir():
            raise RoleEdgeInputError(
                "required root %s is missing or not a directory: %s" % (option, path)
            )

    resolved_registry = registry_dir if registry_dir is not None else _default_registry_dir()
    registry_entries, registry_state, registry_unreadable, registry_payloads = _parse_registry(
        resolved_registry
    )
    triplets = _scan_triplets(logs_path)
    spines = _parse_spines(state_path)
    line_ids = set(spines) | {entry["line_id"] for entry in registry_entries}

    team_rows = _parse_team_rows(teams_path)
    sidecar_rows, sidecar_stems = _parse_sidecars(state_path, spines, line_ids)
    artifact_rows = _parse_stage_artifacts(state_path, spines, line_ids, sidecar_stems)
    dispatch_rows, store_present, unconfirmed, store_path = _parse_dispatch_records(
        state_path, set(triplets)
    )

    return {
        "roots": {
            "state_dir": str(state_dir),
            "teams_dir": str(teams_dir),
            "logs_dir": str(logs_dir),
            "registry_dir": None if resolved_registry is None else str(resolved_registry),
            "registry": registry_state,
            "dispatch_store": store_path,
            "dispatch_store_present": store_present,
        },
        "rows": team_rows + sidecar_rows + artifact_rows + dispatch_rows,
        "spines": spines,
        "line_ids": sorted(line_ids),
        "run_ids": sorted({spine["run_id"] for spine in spines.values()}),
        "registry_entries": registry_entries,
        # The same read's parsed payloads, consumed by ``status-digest.py`` for its legacy line rows — one
        # registry read feeds both the role cross-check and the line projection (digest contract C-1).
        "registry_payloads": registry_payloads,
        "triplets": sorted(triplets),
        "carrier_rows": {
            CARRIER_TEAM: len(team_rows),
            CARRIER_DRIVER: len(sidecar_rows) + len(artifact_rows),
            CARRIER_RUN_AGENT: len(dispatch_rows),
        },
        "notes": {
            "registry_unreadable": len(registry_unreadable),
            "registry_unreadable_paths": registry_unreadable,
            "unconfirmed_dispatch_records": unconfirmed,
        },
    }


def _resolve_identity(raw: str, inputs: dict):
    """data-model § 3: label → line id → spine run_id → literal root → dangling."""
    raw = str(raw)
    if raw in {row["child_raw"] for row in inputs["rows"]}:
        return raw
    if raw in set(inputs["line_ids"]):
        return raw
    if raw in set(inputs["run_ids"]):
        return raw
    if raw == ROOT_LITERAL:
        return raw
    return None


def _roles_for(is_parent: bool, is_child: bool) -> list:
    roles = []
    if is_parent:
        roles.append("superagent")
    if is_child:
        roles.append("subagent")
    return sorted(roles)


def _primary_row(group: list) -> dict:
    def key(row):
        line = row["line"] if row["line"] is not None else 0
        return (-CARRIER_PRECEDENCE.get(row["carrier"], 0), row["path"], line)

    return sorted(group, key=key)[0]


def _input_snapshot(inputs: dict) -> dict:
    roots = inputs["roots"]
    return {
        "state_dir": roots["state_dir"],
        "teams_dir": roots["teams_dir"],
        "logs_dir": roots["logs_dir"],
        "registry_dir": roots["registry_dir"],
        "registry": roots["registry"],
        "dispatch_store": roots["dispatch_store"],
        "dispatch_store_present": roots["dispatch_store_present"],
        "spines": len(inputs["spines"]),
        "registry_entries": len(inputs["registry_entries"]),
        "triplets": len(inputs["triplets"]),
        "carrier_rows": dict(inputs["carrier_rows"]),
        "registry_unreadable": inputs["notes"]["registry_unreadable"],
        "unconfirmed_dispatch_records": inputs["notes"]["unconfirmed_dispatch_records"],
    }


def evaluate_role_model(inputs: dict) -> dict:
    """Judge the parsed snapshot into the report model (contract C-3)."""
    rows = inputs["rows"]
    violated_paths = {}

    def add_violation(kind, subjects, paths):
        key = (kind, tuple(sorted(subjects)))
        violated_paths.setdefault(key, set()).update(paths)

    edge_groups = {}
    dangling_rows = []
    for row in rows:
        parent = _resolve_identity(row["parent_raw"], inputs)
        if parent is None:
            add_violation(
                "dangling-parent",
                [row["parent_raw"], row["child_raw"]],
                [row["path"]],
            )
            dangling_rows.append(row)
            continue
        key = (parent, row["child_raw"], str(row["attempt"]))
        edge_groups.setdefault(key, []).append(row)
        if parent == row["child_raw"]:
            add_violation("self-dispatch", [row["child_raw"]], [row["path"]])

    edges = []
    conflicts = []
    for key in sorted(edge_groups):
        group = edge_groups[key]
        chosen = _primary_row(group)
        for field in ("role_declaration", "dispatch_duty", "depth_position"):
            declared = [(row[field], row["path"]) for row in group if row[field] is not None]
            if len({value for value, _path in declared}) > 1:
                conflicts.append(
                    {
                        "field": field,
                        "paths": sorted({path for _value, path in declared}),
                        "edge": {
                            "parent": key[0],
                            "child": key[1],
                            "attempt": key[2],
                        },
                    }
                )
        edges.append(
            {
                "parent": key[0],
                "child": key[1],
                "attempt": key[2],
                "role_declaration": chosen["role_declaration"] or DEFAULT_ROLE,
                "dispatch_duty": chosen["dispatch_duty"] or DEFAULT_DUTY,
                "depth": None,
                "source": {
                    "carrier": chosen["carrier"],
                    "path": chosen["path"],
                    "line": chosen["line"],
                },
            }
        )

    parents = {key[0] for key in edge_groups}
    children = {key[1] for key in edge_groups}
    dangling_children = {row["child_raw"] for row in dangling_rows}

    adjacency = {}
    incoming = {}
    for key in sorted(edge_groups):
        adjacency.setdefault(key[0], set()).add(key[1])
        incoming.setdefault(key[1], []).append((key[0], key[2]))

    roots = sorted(
        node
        for node in (parents | children)
        if node not in incoming and node not in dangling_children
    )
    depth = {}
    queue = deque()
    for node in roots:
        depth[node] = 0
        queue.append(node)
    while queue:
        node = queue.popleft()
        for child in sorted(adjacency.get(node, ())):
            if child not in depth:
                depth[child] = depth[node] + 1
                queue.append(child)

    # A cycle detached from every root makes depth unresolvable (data-model § 5).
    def reachable(start, skip_direct_self):
        seen = set()
        frontier = [start]
        while frontier:
            node = frontier.pop()
            for child in adjacency.get(node, ()):
                if skip_direct_self and node == start and child == start:
                    continue
                if child not in seen:
                    seen.add(child)
                    frontier.append(child)
        return seen

    cycle_nodes = set()
    for node in sorted((parents | children) - set(depth)):
        if node in reachable(node, skip_direct_self=True):
            cycle_nodes.add(node)

    remaining = set(cycle_nodes)
    while remaining:
        seed = sorted(remaining)[0]
        component = {seed}
        frontier = [seed]
        while frontier:
            node = frontier.pop()
            neighbours = set(adjacency.get(node, ()))
            for other in cycle_nodes:
                if node in adjacency.get(other, ()):
                    neighbours.add(other)
            for other in neighbours:
                if other in cycle_nodes and other not in component:
                    component.add(other)
                    frontier.append(other)
        remaining -= component
        paths = sorted(
            {
                row["path"]
                for key, group in edge_groups.items()
                if key[0] in component and key[1] in component
                for row in group
            }
        )
        add_violation("depth-inconsistent", sorted(component), paths)

    for row in rows:
        if row["depth_position"] is None:
            continue
        if _resolve_identity(row["parent_raw"], inputs) is None:
            continue
        node = row["child_raw"]
        computed = depth.get(node)
        if computed is None or computed != row["depth_position"]:
            add_violation("depth-inconsistent", [node], [row["path"]])

    for row in rows:
        if row["role_declaration"] != "superagent":
            continue
        node = row["child_raw"]
        if node not in parents:
            add_violation("unbacked-role-claim", [node], [row["path"]])

    executor_ids = parents | children | dangling_children
    executors = []
    for node in sorted(executor_ids):
        is_parent = node in parents
        is_child = node in children or node in dangling_children
        roles = _roles_for(is_parent, is_child)
        marker = DUAL_ROLE_MARKER if roles == ["subagent", "superagent"] else None
        incoming_edges = sorted(incoming.get(node, []))
        sources = set()
        for key, group in edge_groups.items():
            if node in (key[0], key[1]):
                for row in group:
                    sources.add((row["carrier"], row["path"], row["line"]))
        for row in dangling_rows:
            if row["child_raw"] == node:
                sources.add((row["carrier"], row["path"], row["line"]))
        executors.append(
            {
                "id": node,
                "parent": incoming_edges[0][0] if incoming_edges else None,
                "roles": roles,
                "role_set_marker": marker,
                "depth": depth.get(node),
                "sources": [
                    {"carrier": carrier, "path": path, "line": line}
                    for carrier, path, line in sorted(
                        sources,
                        key=lambda item: (
                            item[0],
                            item[1],
                            -1 if item[2] is None else item[2],
                        ),
                    )
                ],
            }
        )

    for edge in edges:
        edge["depth"] = depth.get(edge["child"])

    violations = [
        {"kind": kind, "subjects": list(subjects), "paths": sorted(paths)}
        for (kind, subjects), paths in violated_paths.items()
    ]
    violations.sort(key=lambda row: (row["kind"], row["subjects"]))
    conflicts.sort(
        key=lambda row: (
            row["field"],
            row["edge"]["parent"],
            row["edge"]["child"],
            row["edge"]["attempt"],
        )
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "action": "report",
        "inputs": _input_snapshot(inputs),
        "roots": roots,
        "executors": executors,
        "edges": edges,
        "violations": violations,
        "conflicts": conflicts,
        "summary": {
            "edges": len(edges),
            "executors": len(executors),
            "violations": len(violations),
            "conflicts": len(conflicts),
        },
    }


def build_query_answer(model: dict, inputs: dict, parent_arg: str, child_arg: str) -> dict:
    """Answer one pair query (contract C-4); unknown queried identities are exit 2."""
    executors = {entry["id"]: entry for entry in model["executors"]}

    def resolve(option, value):
        identity = _resolve_identity(value, inputs)
        if identity is None or identity not in executors:
            raise RoleEdgeInputError(
                "%s %r does not resolve to a known executor" % (option, value)
            )
        return identity

    parent_id = resolve("--parent", parent_arg)
    child_id = resolve("--child", child_arg)
    edge = next(
        (
            item
            for item in model["edges"]
            if item["parent"] == parent_id and item["child"] == child_id
        ),
        None,
    )

    def view(entry):
        return {
            "id": entry["id"],
            "roles": entry["roles"],
            "role_set_marker": entry["role_set_marker"],
            "depth": entry["depth"],
        }

    violations = [
        row
        for row in model["violations"]
        if parent_id in row["subjects"] or child_id in row["subjects"]
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "action": "query",
        "edge_exists": edge is not None,
        "edge": edge,
        "parent": view(executors[parent_id]),
        "child": view(executors[child_id]),
        "violations": violations,
    }


# --------------------------------------------------------------------------- #
# settlement judgment (spec 106 — additive ``--action settle``)
# --------------------------------------------------------------------------- #
SETTLEMENT_VALUES = (
    "completed",
    "failed",
    "anomaly",
    "cancelled",
    "running",
    "silent-end",
    "unknown",
)
SETTLEMENT_CLASSES = {
    "completed": "terminal",
    "failed": "terminal",
    "anomaly": "terminal",
    "cancelled": "terminal",
    "running": "non-terminal",
    "silent-end": "terminal",
    "unknown": "detection-defect",
}
SETTLEMENT_VIOLATION_KINDS = (
    "settlement-unrecorded",
    "settlement-out-of-set",
    "settlement-unbacked",
)
C1_VERDICT_MAP = {
    "DONE": "completed",
    "FAILED": "failed",
    "ANOMALY": "anomaly",
    "INCOMPLETE": "failed",
    "DEAD": "silent-end",
    "NO_SIGNAL": "silent-end",
    "TIMEOUT": "running",
    "RUNNING": "running",
}
CARRIER_C1 = "c1-fork"
CARRIER_C2 = "c2-subprocess"
CARRIER_C3 = "c3-team-seat"
CARRIER_C4 = "c4-native"
SETTLE_CARRIERS = (CARRIER_C1, CARRIER_C2, CARRIER_C3, CARRIER_C4)
CLAIM_MECHANISM_BY_CARRIER = {
    CARRIER_C1: "u4",
    CARRIER_C2: "return-record",
    CARRIER_C3: "team-verification",
    CARRIER_C4: "five-element",
}
SETTLE_MAPPING_5 = ("label", "role", "dispatch_duty", "workspace", "parent")
SETTLE_MAPPING_7 = SETTLE_MAPPING_5 + ("end_state", "evidence")
LOG_RECORD_SUFFIXES = (
    (".attempt", "attempt"),
    (".settlement", "claim"),
    (".status", "status"),
    (".end", "end"),
    (".live.log", "live"),
    (".jsonl", "live"),
)
ANOMALY_PREFIX = "ANOMALY:"


def _positive_int(text):
    try:
        value = int(text)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("expected a positive integer")
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def _is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _parse_iso_timestamp(value):
    if not isinstance(value, str) or not value:
        return None
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        return datetime.datetime.fromisoformat(text).timestamp()
    except ValueError:
        return None


def _try_read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8"), None
    except OSError as exc:
        return None, "unreadable input %s: %s" % (path, exc)


def _try_json_object(path: Path):
    text, error = _try_read_text(path)
    if error is not None:
        return None, error
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, "unparseable record %s: %s" % (path, exc)
    if not isinstance(payload, dict):
        return None, "malformed record %s: top level is not an object" % (path,)
    return payload, None


def _pid_start_ticks(pid: int):
    try:
        stat = Path("/proc/%d/stat" % pid).read_text(encoding="utf-8")
    except OSError:
        return None
    close = stat.rfind(")")
    if close < 0:
        return None
    fields = stat[close + 2 :].split()
    if len(fields) < 20:
        return None
    try:
        return int(fields[19])
    except ValueError:
        return None


def _pid_liveness(pid) -> str:
    if not _is_int(pid) or pid <= 0:
        return "gone"
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return "gone"
    except PermissionError:
        pass
    except OSError:
        return "gone"
    try:
        stat = Path("/proc/%d/stat" % pid).read_text(encoding="utf-8")
    except OSError:
        return "alive"
    close = stat.rfind(")")
    if close >= 0 and stat[close + 2 : close + 3] == "Z":
        return "gone"
    return "alive"


def _last_nonempty_line(path: Path):
    text, error = _try_read_text(path)
    if error is not None:
        return None, error
    for line in reversed(text.splitlines()):
        if line.strip():
            return line.strip(), None
    return "", None


def _resolve_claim_pointer(pointer, bases):
    if not isinstance(pointer, str) or not pointer:
        return None
    candidate = Path(pointer)
    if candidate.is_absolute():
        return candidate if candidate.exists() else None
    for base in bases:
        if base is None:
            continue
        resolved = Path(base) / pointer
        if resolved.exists():
            return resolved
    return None


def _blank_attempt(label: str, carrier: str, logs_dir: Path) -> dict:
    return {
        "attempt_id": label,
        "carrier": carrier,
        "path": None,
        "logs_dir": logs_dir,
        "bases": [],
        "start": [],
        "terminal": [],
        "live": [],
        "unreadable": [],
        "claims": [],
        "pid": None,
        "pid_start_ticks": None,
        "started_at": None,
        "wait_deadline_s": None,
        "start_grace_s": None,
        "anomaly_line": False,
    }


def _load_attempt_record(path: Path, logs_dir: Path) -> dict:
    label = path.name[: -len(".attempt")]
    attempt = _blank_attempt(label, CARRIER_C2, logs_dir)
    attempt["path"] = path
    payload, error = _try_json_object(path)
    if error is not None:
        attempt["unreadable"].append(
            {"pointer": str(path), "kind": "unreadable", "note": error}
        )
        return attempt
    carrier = payload.get("carrier")
    if carrier not in SETTLE_CARRIERS:
        attempt["unreadable"].append(
            {
                "pointer": str(path),
                "kind": "unreadable",
                "note": "carrier outside the closed inventory: %r" % (carrier,),
            }
        )
        return attempt
    missing = [
        field
        for field in ("attempt_id", "parent_identity", "started_at")
        if not isinstance(payload.get(field), str) or not payload.get(field)
    ]
    if missing:
        attempt["unreadable"].append(
            {
                "pointer": str(path),
                "kind": "unreadable",
                "note": "attempt record missing required fields: %s"
                % ", ".join(sorted(missing)),
            }
        )
        return attempt
    attempt["carrier"] = carrier
    attempt["start"].append({"pointer": str(path), "kind": "start"})
    attempt["started_at"] = payload.get("started_at")
    pid = payload.get("pid")
    if _is_int(pid):
        attempt["pid"] = pid
    ticks = payload.get("pid_start_ticks")
    if _is_int(ticks):
        attempt["pid_start_ticks"] = ticks
    for field in ("wait_deadline_s", "start_grace_s"):
        value = payload.get(field)
        if _is_int(value) and value > 0:
            attempt[field] = value
    return attempt


def _apply_end_record(attempt: dict, path: Path) -> None:
    payload, error = _try_json_object(path)
    if error is not None:
        attempt["unreadable"].append(
            {"pointer": str(path), "kind": "unreadable", "note": error}
        )
        return
    entry = {"pointer": str(path), "kind": "terminal"}
    exit_code = payload.get("exit")
    signal = payload.get("signal")
    if _is_int(exit_code):
        entry["exit"] = exit_code
    if isinstance(signal, str) and signal:
        entry["signal"] = signal
    if "exit" in entry or "signal" in entry:
        attempt["terminal"].append(entry)
    else:
        attempt["unreadable"].append(
            {
                "pointer": str(path),
                "kind": "unreadable",
                "note": "termination record carries neither exit nor signal",
            }
        )


def _apply_status_record(attempt: dict, path: Path) -> None:
    text, error = _try_read_text(path)
    if error is not None:
        attempt["unreadable"].append(
            {"pointer": str(path), "kind": "unreadable", "note": error}
        )
        return
    match = re.search(r"\bexit=(\d+)\b", text)
    if not match:
        attempt["unreadable"].append(
            {
                "pointer": str(path),
                "kind": "unreadable",
                "note": "status line carries no exit code",
            }
        )
        return
    attempt["terminal"].append(
        {"pointer": str(path), "kind": "terminal", "exit": int(match.group(1))}
    )


def _load_claim_file(path: Path):
    payload, error = _try_json_object(path)
    if error is not None:
        return None, error
    evidence = payload.get("evidence", [])
    if not isinstance(evidence, list) or not all(
        isinstance(item, str) for item in evidence
    ):
        return None, "claim evidence is not a list of pointers: %s" % (path,)
    claim = {
        "surface": "attempt-file",
        "path": str(path),
        "line": None,
        "value": payload.get("value"),
        "evidence": list(evidence),
        "mechanism": payload.get("mechanism")
        if isinstance(payload.get("mechanism"), str)
        else None,
        "settlement_version": payload.get("settlement_version"),
        "version_bearing": "settlement_version" in payload,
    }
    return claim, None


def _collect_team_claims(teams_dir: Path):
    claims = []
    unreadable = []
    for path in sorted(teams_dir.glob("*/runs/*-report.md")):
        text, error = _try_read_text(path)
        if error is not None:
            unreadable.append({"pointer": str(path), "kind": "unreadable", "note": error})
            continue
        for header, table_rows, _start in _tables_in_execution_detail(text):
            header_tuple = tuple(header)
            if header_tuple not in (SETTLE_MAPPING_5, SETTLE_MAPPING_7):
                continue
            for lineno, cells in table_rows:
                if len(cells) != len(header_tuple):
                    unreadable.append(
                        {
                            "pointer": "%s:%d" % (path, lineno),
                            "kind": "unreadable",
                            "note": "mapping row width differs from its header",
                        }
                    )
                    continue
                label = cells[0]
                if not label:
                    continue
                if header_tuple == SETTLE_MAPPING_5:
                    claim = {
                        "surface": "team-report-row",
                        "path": str(path),
                        "line": lineno,
                        "value": None,
                        "evidence": [],
                        "mechanism": None,
                        "settlement_version": None,
                        "version_bearing": False,
                    }
                else:
                    evidence = [
                        item.strip()
                        for item in re.split(r"[,;]", cells[6])
                        if item.strip()
                    ]
                    claim = {
                        "surface": "team-report-row",
                        "path": str(path),
                        "line": lineno,
                        "value": cells[5] or None,
                        "evidence": evidence,
                        "mechanism": CLAIM_MECHANISM_BY_CARRIER[CARRIER_C3],
                        "settlement_version": None,
                        "version_bearing": True,
                    }
                claims.append((label, claim))
    return claims, unreadable


def _settle_state_stems(state_dir: Path) -> list:
    stems = set()
    for path in sorted(state_dir.iterdir()):
        if not path.is_file():
            continue
        name = path.name
        if name.startswith("prompt-") and name.endswith(SIDECAR_SUFFIX):
            stems.add(name[len("prompt-") : -len(SIDECAR_SUFFIX)])
            continue
        for prefix in STAGE_ARTIFACT_PREFIXES:
            if not name.startswith(prefix):
                continue
            rest = name[len(prefix) :]
            if rest.endswith(".log"):
                rest = rest[:-4]
            if rest:
                stems.add(rest)
    return sorted(stems)


def _load_c1_attempt(state_dir: Path, stem: str, logs_dir: Path) -> dict:
    attempt = _blank_attempt(stem, CARRIER_C1, logs_dir)
    sidecar = state_dir / ("prompt-%s%s" % (stem, SIDECAR_SUFFIX))
    pid_path = state_dir / ("pid-%s" % stem)
    status_path = state_dir / ("status-%s" % stem)
    log_path = state_dir / ("log-%s.log" % stem)
    heartbeat_path = state_dir / ("heartbeat-%s.log" % stem)
    started_at = None
    if sidecar.is_file():
        attempt["start"].append({"pointer": str(sidecar), "kind": "start"})
        attempt["path"] = sidecar
        payload, error = _try_json_object(sidecar)
        if error is not None:
            attempt["unreadable"].append(
                {"pointer": str(sidecar), "kind": "unreadable", "note": error}
            )
        else:
            started_at = payload.get("started_at")
            role_edge = payload.get("role_edge")
            if started_at is None and isinstance(role_edge, dict):
                started_at = role_edge.get("started_at")
    else:
        for candidate in (pid_path, status_path, log_path, heartbeat_path):
            if candidate.is_file():
                attempt["start"].append({"pointer": str(candidate), "kind": "start"})
                attempt["path"] = candidate
                break
    attempt["started_at"] = started_at if isinstance(started_at, str) else None
    if pid_path.is_file():
        text, error = _try_read_text(pid_path)
        if error is not None:
            attempt["unreadable"].append(
                {"pointer": str(pid_path), "kind": "unreadable", "note": error}
            )
        elif text.strip().isdigit():
            attempt["pid"] = int(text.strip())
        else:
            attempt["unreadable"].append(
                {
                    "pointer": str(pid_path),
                    "kind": "unreadable",
                    "note": "pid file is not an integer",
                }
            )
    if status_path.is_file():
        text, error = _try_read_text(status_path)
        if error is not None:
            attempt["unreadable"].append(
                {"pointer": str(status_path), "kind": "unreadable", "note": error}
            )
        else:
            exit_match = re.search(r"\bexit=(\d+)\b", text)
            sentinel_match = re.search(r"\bsentinel=([01])\b", text)
            if exit_match is None:
                attempt["unreadable"].append(
                    {
                        "pointer": str(status_path),
                        "kind": "unreadable",
                        "note": "status file carries no exit code",
                    }
                )
            else:
                entry = {
                    "pointer": str(status_path),
                    "kind": "terminal",
                    "exit": int(exit_match.group(1)),
                }
                if sentinel_match is not None:
                    entry["sentinel"] = int(sentinel_match.group(1))
                attempt["terminal"].append(entry)
    if log_path.is_file():
        attempt["live"].append(str(log_path))
        line, error = _last_nonempty_line(log_path)
        if error is not None:
            attempt["unreadable"].append(
                {"pointer": str(log_path), "kind": "unreadable", "note": error}
            )
        elif line and line.startswith(ANOMALY_PREFIX):
            attempt["anomaly_line"] = True
    if heartbeat_path.is_file():
        attempt["live"].append(str(heartbeat_path))
    return attempt


def read_settlement_inputs(*, state_dir, teams_dir, logs_dir, registry_dir=None) -> dict:
    """Parse the existing roots plus the additive records into one settlement snapshot."""
    state_path = Path(state_dir)
    teams_path = Path(teams_dir)
    logs_path = Path(logs_dir)
    for option, path in (
        ("--state-dir", state_path),
        ("--teams-dir", teams_path),
        ("--logs-dir", logs_path),
    ):
        if not path.is_dir():
            raise RoleEdgeInputError(
                "required root %s is missing or not a directory: %s" % (option, path)
            )
    bases = [logs_path, state_path, teams_path, REPO_ROOT]
    attempts = {}
    claims_by_label = {}
    stray_unreadable = []

    for path in sorted(logs_path.iterdir()):
        if not path.is_file():
            continue
        name = path.name
        match = next(
            ((suffix, kind) for suffix, kind in LOG_RECORD_SUFFIXES if name.endswith(suffix)),
            None,
        )
        if match is None:
            continue
        suffix, kind = match
        label = name[: -len(suffix)]
        if not label:
            continue
        if kind == "attempt":
            attempts[label] = _load_attempt_record(path, logs_path)
            continue
        if kind == "claim":
            claim, error = _load_claim_file(path)
            if error is not None:
                attempt = attempts.get(label) or _blank_attempt(
                    label, CARRIER_C2, logs_path
                )
                attempts[label] = attempt
                attempt["unreadable"].append(
                    {"pointer": str(path), "kind": "unreadable", "note": error}
                )
            else:
                claims_by_label.setdefault(label, []).append(claim)
            continue
        attempt = attempts.get(label) or _blank_attempt(label, CARRIER_C2, logs_path)
        attempts[label] = attempt
        if attempt["path"] is None:
            attempt["path"] = path
        if kind == "status":
            _apply_status_record(attempt, path)
        elif kind == "end":
            _apply_end_record(attempt, path)
        else:
            attempt["live"].append(str(path))

    for attempt in attempts.values():
        live_paths = [Path(item) for item in attempt["live"] if item.endswith(".live.log")]
        if not live_paths:
            continue
        line, error = _last_nonempty_line(live_paths[0])
        if error is not None:
            attempt["unreadable"].append(
                {"pointer": str(live_paths[0]), "kind": "unreadable", "note": error}
            )
        elif line and line.startswith(ANOMALY_PREFIX):
            attempt["anomaly_line"] = True

    for stem in _settle_state_stems(state_path):
        if stem in attempts:
            continue
        attempts[stem] = _load_c1_attempt(state_path, stem, logs_path)

    team_claims, team_unreadable = _collect_team_claims(teams_path)
    stray_unreadable.extend(team_unreadable)
    for label, claim in team_claims:
        attempt = attempts.get(label) or _blank_attempt(label, CARRIER_C3, logs_path)
        attempts[label] = attempt
        claims_by_label.setdefault(label, []).append(claim)

    for label, claims in claims_by_label.items():
        attempt = attempts.get(label) or _blank_attempt(label, CARRIER_C2, logs_path)
        attempts[label] = attempt
        attempt["claims"].extend(
            sorted(
                claims,
                key=lambda claim: (
                    0 if claim["surface"] == "attempt-file" else 1,
                    claim["path"],
                    claim["line"] or 0,
                ),
            )
        )

    for index, item in enumerate(stray_unreadable):
        label = "unreadable-%d" % (index + 1)
        attempt = _blank_attempt(label, CARRIER_C3, logs_path)
        attempt["unreadable"].append(item)
        attempts[label] = attempt

    for attempt in attempts.values():
        attempt["bases"] = bases

    return {
        "roots": {
            "state_dir": str(state_path),
            "teams_dir": str(teams_path),
            "logs_dir": str(logs_path),
            "registry_dir": None if registry_dir is None else str(registry_dir),
        },
        "attempts": [attempts[label] for label in sorted(attempts)],
    }


def _claim_primary(attempt: dict):
    return attempt["claims"][0] if attempt["claims"] else None


def _evidence_resolves(claim: dict, bases) -> bool:
    if not claim["evidence"]:
        return False
    return all(_resolve_claim_pointer(pointer, bases) for pointer in claim["evidence"])


def _claim_backed(claim: dict, attempt: dict, derived: str) -> bool:
    value = claim["value"]
    if value == "completed":
        if claim["surface"] == "team-report-row":
            expected = CLAIM_MECHANISM_BY_CARRIER[CARRIER_C3]
        else:
            expected = CLAIM_MECHANISM_BY_CARRIER[attempt["carrier"]]
        if claim["mechanism"] != expected:
            return False
        return _evidence_resolves(claim, attempt["bases"])
    if value == "running":
        return derived == "running"
    if value == "silent-end":
        return derived == "silent-end" and _evidence_resolves(claim, attempt["bases"])
    return True


def _derive_settlement(attempt: dict, *, wait_deadline_s: int, start_grace_s: int, now: float):
    if attempt["unreadable"]:
        return "unknown", "unreadable"
    if not attempt["start"]:
        return "unknown", "start-record-missing"
    primary = _claim_primary(attempt)
    if primary is not None and primary["value"] == "cancelled":
        return "cancelled", "cancellation-record"
    if attempt["terminal"]:
        exit_code = None
        signal = None
        for entry in attempt["terminal"]:
            if exit_code is None and "exit" in entry:
                exit_code = entry["exit"]
            if signal is None and entry.get("signal"):
                signal = entry["signal"]
        if exit_code is not None and exit_code != 0:
            return "failed", "non-zero-terminal"
        if signal:
            return "failed", "signal-terminal"
        if attempt["anomaly_line"]:
            return "anomaly", "anomaly-signal"
        if (
            primary is not None
            and primary["value"] == "completed"
            and _claim_backed(primary, attempt, "completed")
        ):
            return "completed", "verified-completion"
        return "failed", "incomplete"
    if primary is not None:
        value = primary["value"]
        if value in ("failed", "anomaly") and _evidence_resolves(primary, attempt["bases"]):
            return value, "claim-recorded-%s" % value
        if (
            value == "completed"
            and attempt["carrier"] in (CARRIER_C3, CARRIER_C4)
            and _claim_backed(primary, attempt, "completed")
        ):
            return "completed", "verified-completion"
    if attempt["pid"] is not None:
        if _pid_liveness(attempt["pid"]) == "alive":
            if attempt["pid_start_ticks"] is not None:
                current = _pid_start_ticks(attempt["pid"])
                if current is not None and current != attempt["pid_start_ticks"]:
                    return "silent-end", "pid-reused"
            return "running", "live-check"
        return "silent-end", "pid-gone"
    started = _parse_iso_timestamp(attempt["started_at"])
    if attempt["carrier"] in (CARRIER_C1, CARRIER_C2):
        grace = attempt["start_grace_s"] or start_grace_s
        if started is not None and now < started + grace:
            return "running", "within-start-grace"
        return "silent-end", "start-grace-expired"
    deadline = attempt["wait_deadline_s"] or wait_deadline_s
    if started is not None and now < started + deadline:
        return "running", "return-channel-open"
    return "silent-end", "deadline-passed"


def _settlement_violation_problem(claim: dict, kind: str) -> dict:
    return {"kind": kind, "path": claim["path"], "line": claim["line"]}


def _audit_claims(attempt: dict, derived: str):
    problems = []
    consistent = True
    primary = _claim_primary(attempt)
    legacy = bool(primary is not None and not primary["version_bearing"])
    if derived == "unknown":
        # A detection defect is the single deterministic refusal, never a settlement
        # judgment: the claim is not audited against an ending that does not exist.
        return consistent, problems, legacy
    for claim in attempt["claims"]:
        value = claim["value"]
        if claim["surface"] == "team-report-row" and claim["version_bearing"]:
            if value is None or not claim["evidence"]:
                problems.append(_settlement_violation_problem(claim, "settlement-unrecorded"))
                if value is not None and value != derived:
                    consistent = False
                continue
        elif claim["version_bearing"] and value is None:
            problems.append(_settlement_violation_problem(claim, "settlement-unrecorded"))
            continue
        if not claim["version_bearing"]:
            if value is not None and value != derived:
                consistent = False
            continue
        if value is None:
            continue
        if value not in SETTLEMENT_VALUES:
            problems.append(_settlement_violation_problem(claim, "settlement-out-of-set"))
            consistent = False
            continue
        if not _claim_backed(claim, attempt, derived):
            problems.append(_settlement_violation_problem(claim, "settlement-unbacked"))
            consistent = False
        if value != derived:
            consistent = False
            problems.append(_settlement_violation_problem(claim, "settlement-unbacked"))
    deduped = []
    seen = set()
    for problem in problems:
        key = (problem["kind"], problem["path"], problem["line"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(problem)
    return consistent, deduped, legacy


def _finding_evidence(attempt: dict, derived: str) -> list:
    items = []
    items.extend(attempt["start"])
    items.extend(attempt["terminal"])
    for claim in attempt["claims"]:
        items.append(
            {
                "pointer": claim["path"],
                "kind": "claim",
                "note": claim["surface"],
            }
        )
    items.extend(attempt["unreadable"])
    if derived == "running":
        pointer = (
            attempt["live"][0]
            if attempt["live"]
            else (str(attempt["path"]) if attempt["path"] is not None else attempt["attempt_id"])
        )
        items.append({"pointer": pointer, "kind": "live"})
    if derived == "silent-end":
        for suffix in (".end", ".status"):
            items.append(
                {
                    "pointer": str(Path(attempt["logs_dir"]) / (attempt["attempt_id"] + suffix)),
                    "kind": "lack",
                    "note": "absent",
                }
            )
    return items


def _claim_snapshot(attempt: dict):
    primary = _claim_primary(attempt)
    if primary is None:
        return None
    return {
        "surface": primary["surface"],
        "path": primary["path"],
        "line": primary["line"],
        "value": primary["value"],
        "evidence": list(primary["evidence"]),
        "mechanism": primary["mechanism"],
        "settlement_version": primary["settlement_version"],
    }


def evaluate_settlements(
    inputs: dict, *, live_window_s: int = 120, wait_deadline_s: int = 1800, start_grace_s: int = 30
) -> dict:
    """Judge the parsed settlement snapshot into the per-attempt findings payload."""
    now = time.time()
    findings = []
    violations = []
    value_counts = {value: 0 for value in SETTLEMENT_VALUES}
    unknown_count = 0
    for attempt in inputs["attempts"]:
        derived, detail = _derive_settlement(
            attempt,
            wait_deadline_s=wait_deadline_s,
            start_grace_s=start_grace_s,
            now=now,
        )
        consistent, problems, legacy = _audit_claims(attempt, derived)
        problem_rows = []
        for problem in problems:
            pointer = problem["path"] or ""
            if problem.get("line"):
                pointer = "%s:%d" % (pointer, problem["line"])
            row = {
                "kind": problem["kind"],
                "attempt_id": attempt["attempt_id"],
                "subjects": [attempt["attempt_id"]],
                "paths": [pointer] if pointer else [],
            }
            problem_rows.append(row)
            violations.append(row)
        finding = {
            "attempt_id": attempt["attempt_id"],
            "carrier": attempt["carrier"],
            "verdict": derived,
            "value": derived,
            "class": SETTLEMENT_CLASSES[derived],
            "evidence": _finding_evidence(attempt, derived),
            "claim": _claim_snapshot(attempt),
            "consistent": consistent,
            "legacy": legacy,
            "detail": detail,
            "violations": problem_rows,
        }
        if derived == "unknown":
            finding["unknown_cause"] = detail
            unknown_count += 1
        value_counts[derived] += 1
        findings.append(finding)
    findings.sort(key=lambda row: row["attempt_id"])
    violations.sort(
        key=lambda row: (row["kind"], row["attempt_id"], tuple(row["paths"]))
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "action": "settle",
        "inputs": {
            "state_dir": inputs["roots"]["state_dir"],
            "teams_dir": inputs["roots"]["teams_dir"],
            "logs_dir": inputs["roots"]["logs_dir"],
            "registry_dir": inputs["roots"]["registry_dir"],
            "live_window_s": live_window_s,
            "wait_deadline_s": wait_deadline_s,
            "start_grace_s": start_grace_s,
        },
        "findings": findings,
        "violations": violations,
        "summary": {
            "attempts": len(findings),
            "values": {
                value: count for value, count in value_counts.items() if count
            },
            "violations": len(violations),
            "unknown": unknown_count,
        },
    }


def settle_exit_code(payload: dict) -> int:
    if payload["summary"]["unknown"]:
        return 2
    if payload["violations"]:
        return 1
    return 0


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #
def _dash(value):
    return "-" if value is None else value


def _edge_line(edge: dict) -> str:
    return (
        "edge parent=%s child=%s attempt=%s role_declaration=%s dispatch_duty=%s "
        "depth=%s source=%s:%s"
        % (
            edge["parent"],
            edge["child"],
            edge["attempt"],
            edge["role_declaration"],
            edge["dispatch_duty"],
            _dash(edge["depth"]),
            edge["source"]["carrier"],
            edge["source"]["path"],
        )
    )


def _violation_line(row: dict) -> str:
    return "violation kind=%s subjects=%s paths=%s" % (
        row["kind"],
        ",".join(row["subjects"]),
        ",".join(row["paths"]),
    )


def _settlement_line(row: dict) -> str:
    return (
        "attempt %s carrier=%s verdict=%s class=%s consistent=%s legacy=%s "
        "evidence=%s"
        % (
            row["attempt_id"],
            row["carrier"],
            row["verdict"],
            row["class"],
            "true" if row["consistent"] else "false",
            "true" if row["legacy"] else "false",
            ",".join(item["pointer"] for item in row["evidence"]),
        )
    )


def render(payload: dict, output_format: str) -> None:
    if output_format == "json":
        sys.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        return
    if payload.get("action") == "settle":
        lines = [_settlement_line(row) for row in payload["findings"]]
        for row in payload["violations"]:
            lines.append(_violation_line(row))
        summary = payload["summary"]
        lines.append(
            "summary attempts=%d violations=%d unknown=%d"
            % (
                summary["attempts"],
                summary["violations"],
                summary["unknown"],
            )
        )
        sys.stdout.write("\n".join(lines) + "\n")
        return
    lines = []
    if payload.get("action") == "query":
        lines.append("edge_exists=%s" % ("true" if payload["edge_exists"] else "false"))
        if payload.get("edge") is not None:
            lines.append(_edge_line(payload["edge"]))
    else:
        for edge in payload["edges"]:
            lines.append(_edge_line(edge))
    for row in payload["violations"]:
        lines.append(_violation_line(row))
    if payload.get("action") == "report":
        summary = payload["summary"]
        lines.append(
            "summary edges=%d executors=%d violations=%d conflicts=%d"
            % (
                summary["edges"],
                summary["executors"],
                summary["violations"],
                summary["conflicts"],
            )
        )
    sys.stdout.write("\n".join(lines) + "\n")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _framework_version() -> str:
    current = Path(__file__).resolve().parent
    for candidate in [current] + list(current.parents):
        if not (candidate / ".git").exists():
            continue
        pyproject = candidate / "pyproject.toml"
        try:
            text = pyproject.read_text(encoding="utf-8")
        except OSError:
            return "unknown"
        match = VERSION_RE.search(text)
        return match.group(1) if match else "unknown"
    return "unknown"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="role-edge-check.py",
        description=(
            "Read-only role-edge judgement over existing run records: edge existence, "
            "per-edge roles, role sets, depth and the closed four violation kinds."
        ),
        epilog=(
            "Side effects: read-only; no file is written and no temporary file is "
            "created.\n"
            "Exit codes: 0 judged clean (an empty edge set is explicitly summarized; a "
            "settlement run judged every attempt, a correctly derived silent-end "
            "included); 1 violations found; 2 unreadable or malformed input "
            "(settlement: unknown findings)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="role-edge-check.py " + _framework_version(),
    )
    parser.add_argument("--action", choices=("report", "query", "settle"), default="report")
    parser.add_argument("--parent", help="query: parent identity")
    parser.add_argument("--child", help="query: child identity")
    parser.add_argument("--state-dir", default=".specify/state")
    parser.add_argument("--teams-dir", default=".specify/teams")
    parser.add_argument("--logs-dir", default=".specify/agents/execution/logs")
    parser.add_argument(
        "--registry-dir",
        default=None,
        help="line-registry cross-check root (default: the owning engine's resolution)",
    )
    parser.add_argument(
        "--live-window",
        type=_positive_int,
        default=120,
        help="settle: liveness window in seconds (positive integer)",
    )
    parser.add_argument(
        "--wait-deadline",
        type=_positive_int,
        default=1800,
        help="settle: pid-less wait deadline in seconds (positive integer)",
    )
    parser.add_argument(
        "--start-grace",
        type=_positive_int,
        default=30,
        help="settle: process start grace in seconds (positive integer)",
    )
    parser.add_argument("--format", choices=("json", "text"), default="json")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.action == "query" and (not args.parent or not args.child):
            raise RoleEdgeInputError(
                "--action query requires both --parent and --child"
            )
        if args.action == "settle":
            settlement_inputs = read_settlement_inputs(
                state_dir=args.state_dir,
                teams_dir=args.teams_dir,
                logs_dir=args.logs_dir,
                registry_dir=args.registry_dir,
            )
            payload = evaluate_settlements(
                settlement_inputs,
                live_window_s=args.live_window,
                wait_deadline_s=args.wait_deadline,
                start_grace_s=args.start_grace,
            )
        else:
            inputs = read_carrier_inputs(
                state_dir=args.state_dir,
                teams_dir=args.teams_dir,
                logs_dir=args.logs_dir,
                registry_dir=args.registry_dir,
            )
            model = evaluate_role_model(inputs)
            payload = (
                build_query_answer(model, inputs, args.parent, args.child)
                if args.action == "query"
                else model
            )
    except RoleEdgeInputError as exc:
        sys.stderr.write("role-edge-check.py: error: %s\n" % exc)
        return 2
    render(payload, args.format)
    if args.action == "settle":
        return settle_exit_code(payload)
    return 1 if payload["violations"] else 0


if __name__ == "__main__":
    sys.exit(main())
