"""Contract test: Handler / HandlerBinding registry chapters (Feature 056 / US2, [C2]).

Pins the registry-side shape of the two NEW chapters in probe-definitions.md:
- Handler six-column table: handler_id (`h-` prefix, unique) / kind / action /
  mode / order / behavior_owner — kind+mode closed sets, owner reachability,
  kind=agent action = a real `##` heading of its owner file;
- HandlerBinding subscription table: selector = `@point:<closed set>`, scope =
  closed set or a per-object object_id, identity triple unique, handlers resolve.

[C2] rule 5 (kind=engine action hits the real engine action closed set) is owned
by ``test_probe_engine_action_sets.py`` — the engine-set contract file — so the
union parse lives in exactly one place.

Engine-side behavior (``probe-utils.py --action handlers --validate`` exit 0 on
the real tree; duplicate identity triple → exit 2 named) is drilled here against
the engine binary; both tests are natural red until T013 lands the engine.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from tests.script_api import ROOT

DEFS = ROOT / "shared" / "definitions" / "probe-definitions.md"
PROBE_ENGINE = ROOT / "scripts" / "python" / "probe-utils.py"
PY_PROBE = [sys.executable, str(PROBE_ENGINE)]

KINDS = {"engine", "agent", "gate"}
MODES = {"non-blocking", "blocking"}
POINTS = {"wrap-up", "situation", "phase-boundary", "confirm-gate"}
SCOPES = {"complex-commands", "skills", "all"}
SELECTOR_RE = re.compile(r"^@point:([a-z-]+)$")

HANDLER_COLUMNS = ["handler_id", "kind", "action", "mode", "order", "behavior_owner"]
BINDING_COLUMNS = ["handler_id", "selector", "scope", "覆盖说明"]


def _section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == f"## {heading}":
            start = i + 1
            break
    if start is None:
        return ""
    body: list[str] = []
    for line in lines[start:]:
        if line.strip().startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def _table_rows(text: str, heading: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    headers: list[str] | None = None
    for line in _section(text, heading).splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if set(cells) <= {"", "-", "—"} or all(set(c) <= set("-: ") for c in cells):
            continue
        if headers is None:
            headers = cells
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def _load_handlers() -> list[dict[str, str]]:
    return _table_rows(DEFS.read_text(encoding="utf-8"), "Handler")


def _load_bindings() -> list[dict[str, str]]:
    return _table_rows(DEFS.read_text(encoding="utf-8"), "HandlerBinding")


def _object_ids() -> set[str]:
    return {
        r.get("object_id", "")
        for r in _table_rows(DEFS.read_text(encoding="utf-8"), "Objects")
    }


def _headings_of(path: Path) -> set[str]:
    return set(re.findall(r"^## (.+)$", path.read_text(encoding="utf-8"), re.MULTILINE))


# --- [C2] rule 1: handler_id unique + h- prefix ------------------------------

def test_handler_ids_unique_and_prefixed() -> None:
    handlers = _load_handlers()
    assert handlers, "no Handler rows registered"
    seen: set[str] = set()
    for h in handlers:
        hid = h.get("handler_id", "")
        assert hid.startswith("h-"), f"handler_id '{hid}' must carry the h- prefix"
        assert hid not in seen, f"duplicate handler_id: {hid}"
        seen.add(hid)


# --- [C2] rule 2: kind/mode closed sets (action closure lives in the engine-set
# contract file; selector/scope closure under the binding tests) ---------------

def test_handler_closed_fields() -> None:
    for h in _load_handlers():
        hid = h.get("handler_id", "")
        assert h.get("kind", "") in KINDS, f"{hid}: kind '{h.get('kind')}' outside closed set"
        assert h.get("mode", "") in MODES, f"{hid}: mode '{h.get('mode')}' outside closed set"
        assert re.fullmatch(r"-?\d+", h.get("order", "")), f"{hid}: order must be an integer"


# --- [C2] rule 4: behavior_owner reachable; # anchor matches a real heading;
# kind=agent action = a real `##` heading of the owner file --------------------

def test_behavior_owner_reachable_and_anchors_real() -> None:
    for h in _load_handlers():
        hid = h.get("handler_id", "")
        owner = h.get("behavior_owner", "")
        rel, _, anchor = owner.partition("#")
        path = ROOT / rel
        assert path.is_file(), f"{hid}: behavior_owner unreachable: {rel}"
        if anchor:
            assert anchor in _headings_of(path), (
                f"{hid}: owner anchor '{anchor}' is not a `##` heading of {rel}"
            )
        if h.get("kind", "") == "agent":
            action = h.get("action", "").strip("`")
            assert action in _headings_of(path), (
                f"{hid}: kind=agent action '{action}' is not a `##` heading of {rel}"
            )


# --- [C2] rule 3: binding triple unique + handlers resolve --------------------

def test_binding_triples_unique_and_handlers_resolve() -> None:
    handler_ids = {h.get("handler_id", "") for h in _load_handlers()}
    bindings = _load_bindings()
    assert bindings, "no HandlerBinding rows registered"
    seen: set[tuple[str, str, str]] = set()
    for b in bindings:
        triple = (b.get("handler_id", ""), b.get("selector", ""), b.get("scope", ""))
        assert triple[0] in handler_ids, f"binding references unknown handler: {triple[0]}"
        assert triple not in seen, f"duplicate binding identity triple: {triple}"
        seen.add(triple)


# --- [C2] rule 2 (binding side): selector/scope closed sets -------------------

def test_binding_selector_and_scope_closed() -> None:
    object_ids = _object_ids()
    for b in _load_bindings():
        m = SELECTOR_RE.match(b.get("selector", ""))
        assert m, f"malformed selector: {b.get('selector')!r}"
        assert m.group(1) in POINTS, (
            f"selector point '{m.group(1)}' outside closed set {sorted(POINTS)}"
        )
        scope = b.get("scope", "")
        assert scope in SCOPES or scope in object_ids, (
            f"scope '{scope}' is neither a scope keyword nor a registered object_id"
        )


# --- [C2] rule 6: order uniqueness within a point + FR-008/FR-014 ordering ----

def test_order_unique_within_each_point() -> None:
    handlers = {h.get("handler_id", ""): h for h in _load_handlers()}
    per_point: dict[str, dict[str, int]] = {}
    for b in _load_bindings():
        m = SELECTOR_RE.match(b.get("selector", ""))
        assert m
        point = m.group(1)
        hid = b.get("handler_id", "")
        order = int(handlers[hid].get("order", "0"))
        owners = per_point.setdefault(point, {})
        assert hid not in owners or owners[hid] == order
        for other, other_order in owners.items():
            assert other_order != order, (
                f"order conflict at @{point}: {hid} and {other} both order {order}"
            )
        owners[hid] = order


def test_seed_order_constraint_run_determination_first() -> None:
    handlers = {h.get("handler_id", ""): int(h.get("order", "0")) for h in _load_handlers()}
    for required in ("h-run-determination", "h-feedback-record", "h-threshold-notice"):
        assert required in handlers, f"seed handler missing: {required}"
    rd = handlers["h-run-determination"]
    assert rd < handlers["h-feedback-record"], "FR-008/FR-014: run-determination must precede feedback-record"
    assert rd < handlers["h-threshold-notice"], "FR-008/FR-014: run-determination must precede threshold-notice"


# --- engine behavior: validate green on the real tree ------------------------

def test_handlers_validate_exits_zero_on_real_tree() -> None:
    proc = subprocess.run(
        [*PY_PROBE, "--action", "handlers", "--validate", "--workspace-root", str(ROOT)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, (
        f"handlers --validate exit {proc.returncode}:\n{proc.stdout}\n{proc.stderr}"
    )


# --- engine behavior: duplicate identity triple → exit 2, named ---------------

def test_duplicate_binding_triple_exits_two(tmp_path: Path) -> None:
    registry_dir = tmp_path / ".specify" / "shared" / "definitions"
    registry_dir.mkdir(parents=True)
    text = DEFS.read_text(encoding="utf-8")
    bindings = _table_rows(text, "HandlerBinding")
    assert bindings, "no bindings to duplicate"
    first = bindings[0]
    dup_row = (
        f"| {first.get('handler_id', '')} | {first.get('selector', '')} "
        f"| {first.get('scope', '')} | duplicate-drill |\n"
    )
    lines = text.splitlines()
    idx = max(i for i, l in enumerate(lines) if l.strip().startswith("|"))
    lines.insert(idx + 1, dup_row.rstrip("\n"))
    (registry_dir / "probe-definitions.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    proc = subprocess.run(
        [*PY_PROBE, "--action", "handlers", "--validate", "--workspace-root", str(tmp_path)],
        capture_output=True, text=True,
    )
    combined = proc.stdout + proc.stderr
    assert proc.returncode == 2, (
        f"duplicate triple must exit 2, got {proc.returncode}:\n{combined}"
    )
    assert "duplicate" in combined, f"exit 2 output must name the duplicate:\n{combined}"
