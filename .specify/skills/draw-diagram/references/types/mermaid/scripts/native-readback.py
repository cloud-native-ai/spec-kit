#!/usr/bin/env python3
"""native-readback.py — Mermaid native readback and geometry evidence.

Reads the ACTUAL produced `.mmd` (and, when given, the ACTUAL rendered SVG),
extracts what the files really contain, diffs the native source against the
authoritative semantics JSON, and measures rendered geometry. Nothing is
inferred from the expected input: every record comes from the two artifacts.

Semantic readback (always): flowchart direction, subgraphs (zones + parents),
node declarations (elements + labels + immediate zone), business arrow edges in
declaration order (declaration order is Mermaid's documented stable-ID basis),
invisible `~~~` layout edges (accounted separately, never merged into
relations), `linkStyle` colour families per edge index, class/style presence.
A business pair that exists only as `~~~` is a layout-edge leak, not a present
relation.

Geometry readback (with --svg): node and cluster rectangles are resolved
through the SVG's ancestor `translate()` chain (Mermaid v11 wraps isolated
components in extra `<g class="root" transform=...>` groups; ignoring that
chain shifts coordinates). Business-edge polylines come from the path `d`
(M/L commands of `curve:linear`). Measured quantities:

  * edge-through-node — every business edge segment vs every node rect that is
    not one of the edge's own declared endpoints: Liang-Barsky clip; a pair is
    reported when the clipped length exceeds --min-clip-px. Two units are
    reported: pair count and distinct-edge count (one edge can clip several
    nodes).
  * layout-edge-through-node — the same test on invisible `~~~` edges, in its
    own block so it can never stand in for a missing business relation.
  * edge crossings — strict interior segment intersections between business
    edges; an intersection within --crossing-endpoint-exclusion px of either
    polyline's first/last vertex is not counted (shared-endpoint artefact).
  * container endpoints — for relations whose authoritative endpoint is a
    zone, the arrow endpoint is measured against that zone's cluster rect and
    its member rects: `cluster-border` (within --container-tolerance px of the
    border), `member-landing` (hard defect) or `unresolved`.
  * label binding — every labelled relation's SVG label group is matched to
    the edge (from/to), its text compared whitespace-insensitively, and the
    label anchor's distance to the polyline midpoint reported.
  * extra visible text — SVG `<text>` contents outside the expected label set
    (element/zone/relation labels) are listed; a legend-like extra is a hard
    defect, any other unexplained extra is a non-hard issue.

Unsupported Mermaid constructs (anonymous subgraphs, `&` fans, unmodelled
lines) and unsupported SVG geometry (C/Q/S/T/A path commands) are reported as
`unsupported`; a false-positive diff produced under unsupported parsing caps
the semantic status at `partial` instead of fabricating a pass or a
graph-corruption failure.

Exit codes: 0 overall pass; 1 overall fail (hard semantic diff or hard visual
defect); 3 overall partial (unsupported constructs/geometry or measured
non-hard visual issues — partial is NOT pass); 2 usage error; 4 output file
already exists; 5 input missing/unreadable.
"""

import argparse
import hashlib
import json
import math
import os
import re
import sys
from collections import OrderedDict

SCRIPT_NAME = "native-readback.py"
SCHEMA = "draw-diagram-native-readback/1"

USAGE = """usage: native-readback.py --source <native.mmd> --semantics <authoritative.json>
                         [--svg <rendered.svg>] --output <new-report.json>
                         [--display-width 1400] [--container-tolerance 6]
                         [--crossing-endpoint-exclusion 3] [--min-clip-px 0.5]

options:
  --source PATH      the actual Mermaid .mmd file that produced the render
  --semantics PATH   the authoritative semantics JSON (elements/zones/relations)
  --svg PATH         the actual rendered SVG (geometry checks are skipped without it)
  --output PATH      new report path; an existing file is refused (exit 4)
  --display-width    target display width in px for the effective-font estimate (default 1400)
  --container-tolerance  px tolerance for "arrow lands on the cluster border" (default 6)
  --crossing-endpoint-exclusion  px radius excluded around polyline endpoints (default 3)
  --min-clip-px      minimum clipped segment length to report an edge/node pair (default 0.5)
  -h, --help         print this help and exit
  --version          print the script name and the framework version, then exit

side-effects: writes exactly the --output file; a flag-only invocation writes nothing
exit-codes: 0 overall pass; 1 overall fail; 3 overall partial (not pass); 2 usage error; 4 output exists; 5 input unreadable
"""

ATTR_RE = re.compile(r'([a-zA-Z_:][-\w:.]*)="([^"]*)"')
TRANS_RE = re.compile(r"translate\(\s*(-?\d+(?:\.\d+)?)[,\s]+(-?\d+(?:\.\d+)?)\s*\)")
NUM = r"-?\d+(?:\.\d+)?"
ID_TOKEN = r"[A-Za-z0-9_.\-]+"

SUBGRAPH_RE = re.compile(
    r'^\s*subgraph\s+(%s)\s*(?:\[\s*(?:"([^"]*)"|([^\]]*))\s*\])?\s*$' % ID_TOKEN)
SUBGRAPH_BARE_RE = re.compile(r'^\s*subgraph\s+(?:"([^"]*)"|(%s))\s*$' % ID_TOKEN)
NODE_DECL_RES = [
    ("rect", re.compile(r'^\s*(%s)\s*\[\s*(?:"([^"]*)"|([^\]]*))\s*\]\s*$' % ID_TOKEN)),
    ("round", re.compile(r'^\s*(%s)\s*\(\s*(?:"([^"]*)"|([^\)]*))\s*\)\s*$' % ID_TOKEN)),
    ("circle", re.compile(r'^\s*(%s)\s*\(\(\s*(?:"([^"]*)"|([^\)]*))\s*\)\)\s*$' % ID_TOKEN)),
    ("diamond", re.compile(r'^\s*(%s)\s*\{\s*(?:"([^"]*)"|([^\}]*))\s*\}\s*$' % ID_TOKEN)),
    ("subroutine", re.compile(r'^\s*(%s)\s*\[\[\s*(?:"([^"]*)"|([^\]]*))\s*\]\]\s*$' % ID_TOKEN)),
    ("stadium", re.compile(r'^\s*(%s)\s*\(\s*\[\s*(?:"([^"]*)"|([^\]]*))\s*\]\s*\)\s*$' % ID_TOKEN)),
    ("asymmetric", re.compile(r'^\s*(%s)\s*>\s*(?:"([^"]*)"|([^\]]*))\s*\]\s*$' % ID_TOKEN)),
]
ARROW = r"(<-->|==>|-->|---|-\.->|\.->|--x|--o|o--|x--)"
ARROW_RE = re.compile(r'^\s*(%s)\s*%s\s*(?:\|\s*([^|]*?)\s*\|)?\s*(%s)\s*$' % (ID_TOKEN, ARROW, ID_TOKEN))
EDGE_TEXT_RE = re.compile(r'^\s*(%s)\s*%s\s*-+\s*([^->][^-]*?)\s*-+(>|\.->)\s*(%s)\s*$'
                          % (ID_TOKEN, ARROW, ID_TOKEN))
LAYOUT_RE = re.compile(r'^\s*(%s)\s*~{3,}\s*(%s)\s*$' % (ID_TOKEN, ID_TOKEN))
STYLE_ID_RE = re.compile(r'^\s*style\s+(%s)\s+(.+)$' % ID_TOKEN)
CLASSDEF_RE = re.compile(r'^\s*classDef\s+(%s)\s+(.+)$' % ID_TOKEN)
CLASS_RE = re.compile(r'^\s*class\s+([A-Za-z0-9_.\-,]+)\s+(%s)\s*$' % ID_TOKEN)
LINKSTYLE_RE = re.compile(r'^\s*linkStyle\s+([0-9,\s]+)\s+(.+)$')
HEADER_RE = re.compile(r'^(?:flowchart|graph)\s+(TB|TD|BT|LR|RL)\s*$')
HEADER_ANY_RE = re.compile(r'^(?:flowchart|graph)\b')


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def read_text(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    return raw.decode("utf-8", "replace"), raw


def script_version(start_dir):
    here = os.path.abspath(start_dir)
    for _ in range(13):
        if os.path.isfile(os.path.join(here, "pyproject.toml")) and os.path.exists(os.path.join(here, ".git")):
            try:
                text = open(os.path.join(here, "pyproject.toml"), "r", encoding="utf-8").read()
            except OSError:
                return "unknown"
            in_project = False
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("[") and line.endswith("]"):
                    in_project = line == "[project]"
                    continue
                if not in_project:
                    continue
                key, sep, value = line.partition("=")
                if sep and key.strip() == "version":
                    value = value.strip()
                    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                        value = value[1:-1]
                    return value or "unknown"
            return "unknown"
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    return "unknown"


def strip_quotes(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    return text


def norm(text):
    return re.sub(r"\s+", "", text or "")


class NativeModel(object):
    def __init__(self):
        self.direction = None
        self.init_directive = None
        self.nodes = OrderedDict()
        self.zones = OrderedDict()
        self.zone_parent = {}
        self.node_zone = {}
        self.business = []
        self.layout = []
        self.link_order = []
        self.link_colors = {}
        self.class_defs = OrderedDict()
        self.class_members = {}
        self.id_styles = {}
        self.unsupported = []
        self.notes = []


def parse_mermaid(text):
    model = NativeModel()
    zone_stack = []

    def zone_of():
        return zone_stack[-1] if zone_stack else None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("%%{") and line.endswith("}%%"):
            model.init_directive = line
            continue
        if line.startswith("%%"):
            continue
        if line.startswith("---"):
            model.notes.append("frontmatter-line")
            continue
        m = HEADER_RE.match(line)
        if m and model.direction is None:
            model.direction = m.group(1)
            continue
        if HEADER_ANY_RE.match(line):
            model.unsupported.append("flowchart-header:%s" % line)
            continue
        if line.startswith("subgraph"):
            m = SUBGRAPH_RE.match(line)
            if m and (m.group(2) is not None or m.group(3) is not None):
                zid = m.group(1)
                label = m.group(2) if m.group(2) is not None else m.group(3)
            else:
                m = SUBGRAPH_BARE_RE.match(line)
                if not m:
                    model.unsupported.append("anonymous-or-unparsed-subgraph:%s" % line)
                    zone_stack.append(None)
                    continue
                label = m.group(1) if m.group(1) is not None else m.group(2)
                zid = label
            model.zones[zid] = label.strip()
            model.zone_parent[zid] = zone_of()
            zone_stack.append(zid)
            continue
        if line == "end":
            if zone_stack:
                zone_stack.pop()
            else:
                model.unsupported.append("stray-end")
            continue
        m = LAYOUT_RE.match(line)
        if m:
            model.layout.append({"from": m.group(1), "to": m.group(2)})
            model.link_order.append(("layout", len(model.layout) - 1))
            continue
        m = EDGE_TEXT_RE.match(line)
        if m:
            rec = {"from": m.group(1), "to": m.group(5), "label": m.group(3).strip(),
                   "arrow": m.group(2) + m.group(4)}
            model.business.append(rec)
            model.link_order.append(("business", len(model.business) - 1))
            continue
        if "&" in line and re.search(r"-->|~~~|---", line):
            model.unsupported.append("fan-out-edge:%s" % line)
            continue
        m = ARROW_RE.match(line)
        if m:
            rec = {"from": m.group(1), "to": m.group(4),
                   "label": strip_quotes(m.group(3) or ""), "arrow": m.group(2)}
            model.business.append(rec)
            model.link_order.append(("business", len(model.business) - 1))
            continue
        m = CLASSDEF_RE.match(line)
        if m:
            model.class_defs[m.group(1)] = m.group(2)
            continue
        m = CLASS_RE.match(line)
        if m:
            for target in m.group(1).split(","):
                target = target.strip()
                if target:
                    model.class_members.setdefault(target, []).append(m.group(2))
            continue
        m = STYLE_ID_RE.match(line)
        if m:
            model.id_styles[m.group(1)] = m.group(2)
            continue
        m = LINKSTYLE_RE.match(line)
        if m:
            for idx in re.findall(r"\d+", m.group(1)):
                color = re.search(r"stroke\s*:\s*(#[0-9a-fA-F]{3,8})", m.group(2))
                model.link_colors[int(idx)] = color.group(1).lower() if color else None
            continue
        matched = False
        for _shape, pattern in NODE_DECL_RES:
            m = pattern.match(line)
            if m:
                nid = m.group(1)
                label = m.group(2) if m.group(2) is not None else m.group(3)
                label = label if label is not None else nid
                if nid not in model.nodes:
                    model.nodes[nid] = label.strip()
                    model.node_zone[nid] = zone_of()
                else:
                    model.notes.append("redeclared-node:%s" % nid)
                matched = True
                break
        if matched:
            continue
        if re.match(r'^\s*%s\s*$' % ID_TOKEN, line):
            continue
        model.unsupported.append("unparsed-line:%s" % line)
    return model


def business_color_map(model):
    out = {}
    for idx, kind in enumerate(model.link_order):
        if kind[0] == "business" and idx in model.link_colors:
            out[kind[1]] = model.link_colors[idx]
    return out


def semantics_errors(sem):
    errors = []
    elements = sem.get("elements") or []
    zones = sem.get("zones") or []
    relations = sem.get("relations") or []
    eids = set()
    for el in elements:
        eid = el.get("id")
        if not eid or eid in eids:
            errors.append("element id missing/duplicate: %r" % eid)
        eids.add(eid)
    zids = set(z.get("id") for z in zones if z.get("id"))
    for rel in relations:
        for side in ("from", "to"):
            end = rel.get(side)
            if end not in eids and end not in zids:
                errors.append("relation %s endpoint unknown: %s" % (rel.get("id"), end))
    counts = sem.get("counts") or {}
    for key, actual in (("elements", len(elements)), ("zones", len(zones)),
                        ("relations", len(relations))):
        if key in counts and counts[key] != actual:
            errors.append("counts.%s=%s but file has %d" % (key, counts[key], actual))
    return errors


def semantic_diff(model, sem):
    diffs = OrderedDict()
    sem_elements = OrderedDict((el["id"], el) for el in sem.get("elements") or [])
    sem_zones = OrderedDict((z["id"], z) for z in sem.get("zones") or [])
    sem_relations = sem.get("relations") or []

    diffs["missingElements"] = [eid for eid in sem_elements if eid not in model.nodes]
    diffs["extraElements"] = [nid for nid in model.nodes if nid not in sem_elements]
    label_changes = []
    zone_changes = []
    for eid, el in sem_elements.items():
        if eid in model.nodes:
            if model.nodes[eid] != (el.get("label") if el.get("label") is not None else eid):
                label_changes.append({"id": eid, "expected": el.get("label"), "actual": model.nodes[eid]})
            if el.get("zone") != model.node_zone.get(eid):
                zone_changes.append({"id": eid, "expected": el.get("zone"),
                                     "actual": model.node_zone.get(eid)})
    diffs["elementLabelChanges"] = label_changes
    diffs["elementZoneChanges"] = zone_changes
    diffs["missingZones"] = [zid for zid in sem_zones if zid not in model.zones]
    diffs["extraZones"] = [zid for zid in model.zones if zid not in sem_zones]
    zone_labels = []
    zone_parents = []
    for zid, zone in sem_zones.items():
        if zid in model.zones:
            if model.zones[zid] != (zone.get("label") if zone.get("label") is not None else zid):
                zone_labels.append({"id": zid, "expected": zone.get("label"), "actual": model.zones[zid]})
            if zone.get("parent") != model.zone_parent.get(zid):
                zone_parents.append({"id": zid, "expected": zone.get("parent"),
                                     "actual": model.zone_parent.get(zid)})
    diffs["zoneLabelChanges"] = zone_labels
    diffs["zoneParentChanges"] = zone_parents

    colors = business_color_map(model)
    missing_rels = []
    relation_changes = []
    color_changes = []
    container_expanded = []
    zone_ids = set(sem_zones)
    for idx, rel in enumerate(sem_relations):
        if idx >= len(model.business):
            missing_rels.append(rel.get("id"))
            continue
        native = model.business[idx]
        if native["from"] != rel.get("from") or native["to"] != rel.get("to"):
            relation_changes.append({"relation": rel.get("id"),
                                     "expected": [rel.get("from"), rel.get("to")],
                                     "actual": [native["from"], native["to"]]})
        expected_label = rel.get("label") or ""
        if (native.get("label") or "") != expected_label:
            relation_changes.append({"relation": rel.get("id"), "field": "label",
                                     "expected": expected_label, "actual": native.get("label") or ""})
        expected_color = (rel.get("color") or "").lower() or None
        actual_color = colors.get(idx)
        if expected_color and actual_color and expected_color != actual_color:
            color_changes.append({"relation": rel.get("id"), "index": idx,
                                  "expected": expected_color, "actual": actual_color})
        for side in ("from", "to"):
            end = rel.get(side)
            if end in zone_ids and native[side] != end:
                container_expanded.append({"relation": rel.get("id"), "side": side,
                                           "expected": end, "actual": native[side]})
    diffs["missingRelations"] = missing_rels
    extra_rels = []
    for idx in range(len(sem_relations), len(model.business)):
        extra_rels.append({"index": idx, "from": model.business[idx]["from"],
                           "to": model.business[idx]["to"]})
    diffs["extraRelations"] = extra_rels
    diffs["relationChanges"] = relation_changes
    diffs["colorFamilyChanges"] = color_changes
    diffs["containerEndpointExpanded"] = container_expanded
    sem_pairs = set((r.get("from"), r.get("to")) for r in sem_relations)
    leaks = []
    for edge in model.layout:
        pair = (edge["from"], edge["to"])
        if pair in sem_pairs and not any(b["from"] == pair[0] and b["to"] == pair[1]
                                         for b in model.business):
            leaks.append({"from": edge["from"], "to": edge["to"]})
    diffs["layoutEdgeLeaks"] = leaks
    diffs["hardDiffCount"] = sum(len(v) for v in diffs.values() if isinstance(v, list))
    return diffs


class SvgGeom(object):
    def __init__(self):
        self.view_box = None
        self.root_font_px = None
        self.node_rects = OrderedDict()
        self.cluster_rects = OrderedDict()
        self.business_paths = OrderedDict()
        self.layout_paths = []
        self.path_unsupported = []
        self.texts = []
        self.label_texts = OrderedDict()
        self.label_anchors = OrderedDict()
        self.extra_node_groups = []


def _attrs(chunk):
    return dict(ATTR_RE.findall(chunk))


def _class_tokens(a):
    return set((a.get("class") or "").split())


def _edge_resolver(model):
    """(from,to,index) -> regex matching the SVG link id, tolerant of the mermaid index."""
    resolver = []
    for idx, rec in enumerate(model.business):
        pattern = re.compile(r'^(?:mmd-)?L_%s_%s_\d+$' % (re.escape(rec["from"]), re.escape(rec["to"])))
        resolver.append({"from": rec["from"], "to": rec["to"], "index": idx,
                         "base": "L_%s_%s_%d" % (rec["from"], rec["to"], idx),
                         "re": pattern})
    return resolver


def _resolve_edge(ident, resolver):
    for item in resolver:
        if item["re"].match(ident):
            return item
    return None


def parse_svg(svg_text, model):
    geom = SvgGeom()
    vb = re.search(r'viewBox="([-\d.\s]+)"', svg_text)
    if vb:
        parts = [float(p) for p in vb.group(1).split()]
        if len(parts) == 4:
            geom.view_box = parts
    fs = re.search(r'#[\w-]+\{[^}]*font-size:\s*([\d.]+)', svg_text)
    if fs:
        geom.root_font_px = float(fs.group(1))

    node_res = [(nid, re.compile(r'^(?:mmd-)?flowchart-%s-\d+$' % re.escape(nid)))
                for nid in sorted(model.nodes.keys(), key=len, reverse=True)]
    zone_res = [(zid, re.compile(r'^(?:mmd-)?%s$' % re.escape(zid)))
                for zid in sorted(model.zones.keys(), key=len, reverse=True)]
    edge_res = _edge_resolver(model)

    tag_re = re.compile(r"<(/?)(g|rect|path)\b([^>]*)>")
    stack = []
    pending_node = None
    pending_cluster = None
    for m in tag_re.finditer(svg_text):
        closing, tag, raw = m.group(1), m.group(2), m.group(3)
        if tag == "g":
            if closing:
                if stack:
                    stack.pop()
                pending_node = None
                pending_cluster = None
                continue
            a = _attrs(raw)
            ax = ay = 0.0
            if "transform" in a:
                tm = TRANS_RE.search(a["transform"])
                if tm:
                    ax, ay = float(tm.group(1)), float(tm.group(2))
            px = stack[-1][2] if stack else 0.0
            py = stack[-1][3] if stack else 0.0
            cls = _class_tokens(a)
            ident = a.get("id", "")
            stack.append((cls, ident, px + ax, py + ay))
            if "node" in cls and ident:
                resolved = None
                for nid, rx in node_res:
                    if rx.match(ident):
                        resolved = nid
                        break
                if resolved is None:
                    geom.extra_node_groups.append(ident)
                pending_node = resolved
            elif "cluster" in cls and ident:
                resolved = None
                for zid, rx in zone_res:
                    if rx.match(ident):
                        resolved = zid
                        break
                pending_cluster = resolved
            continue
        if tag == "rect":
            a = _attrs(raw)
            try:
                w = float(a.get("width", "0"))
                h = float(a.get("height", "0"))
            except ValueError:
                continue
            if w <= 0 or h <= 0 or (pending_node is None and pending_cluster is None):
                continue
            owner = None
            for item in reversed(stack):
                if item[1]:
                    owner = item
                    break
            if owner is None:
                continue
            try:
                rx = float(a.get("x", "0"))
                ry = float(a.get("y", "0"))
            except ValueError:
                continue
            rect = (owner[2] + rx, owner[3] + ry, w, h)
            if pending_node is not None and pending_node not in geom.node_rects:
                geom.node_rects[pending_node] = rect
            elif pending_cluster is not None and pending_cluster not in geom.cluster_rects:
                geom.cluster_rects[pending_cluster] = rect
            continue
        if tag == "path":
            a = _attrs(raw)
            if a.get("data-et") != "edge":
                continue
            ident = a.get("id", "")
            points, unsupported = _path_points(a.get("d", ""))
            offset_x = stack[-1][2] if stack else 0.0
            offset_y = stack[-1][3] if stack else 0.0
            if offset_x or offset_y:
                points = [(x + offset_x, y + offset_y) for x, y in points]
            invisible = "edge-thickness-invisible" in (a.get("class") or "")
            if unsupported:
                geom.path_unsupported.append({"id": ident, "commands": unsupported})
            hit = _resolve_edge(ident, edge_res)
            rec = {"id": ident, "base": hit["base"] if hit else ident,
                   "declared": hit is not None, "points": points}
            if invisible:
                geom.layout_paths.append(rec)
            elif hit is not None:
                geom.business_paths[hit["base"]] = rec
            else:
                geom.business_paths[ident] = rec

    for m in re.finditer(r'<text\b[^>]*>(.*?)</text>', svg_text, re.S):
        content = _clean_text(m.group(1))
        if content:
            geom.texts.append(content)

    section_start = svg_text.find('<g class="edgeLabels"')
    section = svg_text[section_start:] if section_start >= 0 else svg_text
    nodes_start = section.find('<g class="nodes"')
    if nodes_start >= 0:
        section = section[:nodes_start]
    starts = list(re.finditer(r'<g class="label"\s+data-id="([^"]+)"([^>]*)>', section))
    for i, m in enumerate(starts):
        block_end = starts[i + 1].start() if i + 1 < len(starts) else len(section)
        block = section[m.end():block_end]
        texts = [_clean_text(t) for t in re.findall(r'<text\b[^>]*>(.*?)</text>', block, re.S)]
        text = " ".join(t for t in texts if t)
        hit = _resolve_edge(m.group(1), edge_res)
        if hit is None:
            continue
        key = hit["base"]
        if text:
            geom.label_texts[key] = text
        prefix = section[max(0, m.start() - 400):m.start()]
        wrappers = re.findall(r'<g class="edgeLabel"([^>]*)>', prefix)
        px = py = 0.0
        if wrappers:
            wt = TRANS_RE.search(wrappers[-1])
            if wt:
                px, py = float(wt.group(1)), float(wt.group(2))
        own = TRANS_RE.search(m.group(2))
        if own:
            px += float(own.group(1))
            py += float(own.group(2))
        if wrappers or own:
            geom.label_anchors[key] = (px, py)
    return geom


def _clean_text(raw):
    text = re.sub(r"<[^>]*>", " ", raw)
    text = (text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                .replace("&quot;", '"').replace("&#39;", "'"))
    return re.sub(r"\s+", " ", text).strip()


def _path_points(d):
    if not d:
        return [], []
    bad = sorted(set(c for c in re.findall(r"[A-Za-z]", d) if c not in ("M", "L")))
    points = [(float(x), float(y)) for x, y in re.findall(
        r"[ML]\s*(%s)[,\s]\s*(%s)" % (NUM, NUM), d)]
    return points, bad


def liang_barsky(p0, p1, rect):
    x, y, w, h = rect
    xmin, xmax = x, x + w
    ymin, ymax = y, y + h
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, p0[0] - xmin), (dx, xmax - p0[0]),
                 (-dy, p0[1] - ymin), (dy, ymax - p0[1])):
        if p == 0:
            if q < 0:
                return None
            continue
        r = q / p
        if p < 0:
            if r > t1:
                return None
            if r > t0:
                t0 = r
        else:
            if r < t0:
                return None
            if r < t1:
                t1 = r
    return (t0, t1)


def seg_intersection(a, b, c, d):
    def cross(o, p, q):
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
    d1, d2 = cross(c, d, a), cross(c, d, b)
    d3, d4 = cross(a, b, c), cross(a, b, d)
    if ((d1 > 0 > d2) or (d1 < 0 < d2)) and ((d3 > 0 > d4) or (d3 < 0 < d4)):
        den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
        if den == 0:
            return None
        t = ((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0])) / den
        return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
    return None


def polyline_length(points):
    return sum(math.hypot(points[i + 1][0] - points[i][0],
                          points[i + 1][1] - points[i][1])
               for i in range(len(points) - 1))


def edge_midpoint(points):
    total = polyline_length(points)
    if total == 0:
        return points[0] if points else (0.0, 0.0)
    half = total / 2.0
    walked = 0.0
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if walked + seg >= half:
            t = (half - walked) / seg if seg else 0.0
            return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
        walked += seg
    return points[-1]


def point_polyline_distance(pt, points):
    if len(points) == 1:
        return math.hypot(pt[0] - points[0][0], pt[1] - points[0][1])
    best = None
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length2 = dx * dx + dy * dy
        if length2 == 0:
            d = math.hypot(pt[0] - a[0], pt[1] - a[1])
        else:
            t = max(0.0, min(1.0, ((pt[0] - a[0]) * dx + (pt[1] - a[1]) * dy) / length2))
            d = math.hypot(pt[0] - (a[0] + t * dx), pt[1] - (a[1] + t * dy))
        best = d if best is None else min(best, d)
    return best if best is not None else 0.0


def rect_border_distance(pt, rect):
    x, y, w, h = rect
    if x <= pt[0] <= x + w and y <= pt[1] <= y + h:
        return min(pt[0] - x, x + w - pt[0], pt[1] - y, y + h - pt[1])
    dx = max(x - pt[0], 0.0, pt[0] - (x + w))
    dy = max(y - pt[1], 0.0, pt[1] - (y + h))
    return math.hypot(dx, dy)


def measure_geometry(geom, model, sem, args):
    out = OrderedDict()

    def through(paths, exclude_endpoints):
        merged = OrderedDict()
        for rec in paths:
            pts = rec["points"]
            if len(pts) < 2:
                continue
            for i in range(len(pts) - 1):
                p0, p1 = pts[i], pts[i + 1]
                seg_len = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
                if seg_len == 0:
                    continue
                for nid, rect in geom.node_rects.items():
                    if nid in exclude_endpoints.get(rec["base"], ()):  # own endpoints
                        continue
                    clip = liang_barsky(p0, p1, rect)
                    if not clip:
                        continue
                    clipped = (clip[1] - clip[0]) * seg_len
                    if clipped > args.min_clip_px:
                        key = (rec["base"], nid)
                        if key not in merged or clipped > merged[key]["clippedLengthPx"]:
                            merged[key] = {"edge": rec["base"], "node": nid,
                                           "segment": i, "clippedLengthPx": round(clipped, 2)}
        return list(merged.values())

    endpoints = {}
    for idx, rec in enumerate(model.business):
        endpoints["L_%s_%s_%d" % (rec["from"], rec["to"], idx)] = (rec["from"], rec["to"])
    pairs = through(geom.business_paths.values(), endpoints)
    out["edgeThroughNode"] = OrderedDict([
        ("method", "business edge polyline segments (SVG path d, M/L) vs node rects "
                   "(ancestor translate chain + rect x/y/w/h); Liang-Barsky clip; a "
                   "(edge,node) pair counts when clipped length > %.2fpx; the edge's own "
                   "declared endpoints are excluded; pair count and distinct-edge count are "
                   "reported separately" % args.min_clip_px),
        ("count", len(pairs)),
        ("distinctEdges", len(set(p["edge"] for p in pairs))),
        ("pairs", pairs),
    ])
    layout_pairs = through(geom.layout_paths, {})
    out["layoutEdgeThroughNode"] = OrderedDict([
        ("method", "invisible ~~~ layout edges measured separately; they are not visible "
                   "line-work and are never counted as business relations"),
        ("count", len(layout_pairs)),
        ("distinctEdges", len(set(p["edge"] for p in layout_pairs))),
        ("pairs", layout_pairs),
    ])

    crossings = []
    bases = sorted(geom.business_paths.keys())
    for i in range(len(bases)):
        for j in range(i + 1, len(bases)):
            e1, e2 = geom.business_paths[bases[i]], geom.business_paths[bases[j]]
            p1, p2 = e1["points"], e2["points"]
            if len(p1) < 2 or len(p2) < 2:
                continue
            done = False
            for s1 in range(len(p1) - 1):
                for s2 in range(len(p2) - 1):
                    pt = seg_intersection(p1[s1], p1[s1 + 1], p2[s2], p2[s2 + 1])
                    if pt is None:
                        continue
                    near1 = min(math.hypot(pt[0] - p1[0][0], pt[1] - p1[0][1]),
                                math.hypot(pt[0] - p1[-1][0], pt[1] - p1[-1][1]))
                    near2 = min(math.hypot(pt[0] - p2[0][0], pt[1] - p2[0][1]),
                                math.hypot(pt[0] - p2[-1][0], pt[1] - p2[-1][1]))
                    if (near1 <= args.crossing_endpoint_exclusion or
                            near2 <= args.crossing_endpoint_exclusion):
                        continue
                    crossings.append({"a": e1["base"], "b": e2["base"],
                                      "at": [round(pt[0], 1), round(pt[1], 1)]})
                    done = True
                    break
                if done:
                    break
    out["edgeCrossings"] = OrderedDict([
        ("method", "strict interior intersections between business-edge polyline segments; "
                   "an intersection within %.1fpx of either polyline's first/last vertex is "
                   "excluded as a shared-endpoint artefact" % args.crossing_endpoint_exclusion),
        ("count", len(crossings)),
        ("pairs", crossings),
    ])

    sem_zones = OrderedDict((z["id"], z) for z in sem.get("zones") or [])
    zone_members = {}
    for el in sem.get("elements") or []:
        zone_members.setdefault(el.get("zone"), []).append(el["id"])
    containers = []
    for idx, rel in enumerate(sem.get("relations") or []):
        if idx >= len(model.business):
            break
        rec = geom.business_paths.get("L_%s_%s_%d" % (model.business[idx]["from"],
                                                      model.business[idx]["to"], idx))
        if not rec or len(rec["points"]) < 2:
            continue
        for side, which in (("from", 0), ("to", -1)):
            end = rel.get(side)
            if end not in sem_zones:
                continue
            pt = rec["points"][which]
            cluster = geom.cluster_rects.get(end)
            item = OrderedDict([("relation", rel.get("id")), ("side", side), ("zone", end),
                                ("endpoint", [round(pt[0], 1), round(pt[1], 1)]),
                                ("clusterRectFound", cluster is not None)])
            nearest, nearest_d = None, None
            inside_member = False
            for mid in zone_members.get(end, []):
                rect = geom.node_rects.get(mid)
                if rect is None:
                    continue
                d = rect_border_distance(pt, rect)
                if nearest_d is None or d < nearest_d:
                    nearest, nearest_d = mid, d
                if (rect[0] <= pt[0] <= rect[0] + rect[2]
                        and rect[1] <= pt[1] <= rect[1] + rect[3]):
                    inside_member = True
            item["nearestMember"] = nearest
            item["memberDistancePx"] = round(nearest_d, 2) if nearest_d is not None else None
            if cluster is None:
                item["assessment"] = "unresolved"
            else:
                border = rect_border_distance(pt, cluster)
                item["borderDistancePx"] = round(border, 2)
                if inside_member:
                    item["assessment"] = "member-landing"
                elif border <= args.container_tolerance:
                    item["assessment"] = "cluster-border"
                else:
                    item["assessment"] = "unresolved"
            containers.append(item)
    out["containerEndpoints"] = OrderedDict([
        ("method", "arrow endpoint of every relation whose authoritative endpoint is a zone, "
                   "measured against that zone's cluster rect and its member rects; border "
                   "tolerance %.1fpx; member-landing is a hard defect" % args.container_tolerance),
        ("count", len(containers)),
        ("items", containers),
    ])

    labels = []
    for idx, rel in enumerate(sem.get("relations") or []):
        if idx >= len(model.business):
            break
        expected = model.business[idx].get("label") or ""
        if not expected:
            continue
        base = "L_%s_%s_%d" % (model.business[idx]["from"], model.business[idx]["to"], idx)
        actual = geom.label_texts.get(base)
        item = OrderedDict([("relation", rel.get("id")), ("expected", expected),
                            ("svgText", actual), ("found", actual is not None),
                            ("textMatches", norm(actual) == norm(expected) if actual is not None else False)])
        rec = geom.business_paths.get(base)
        anchor = geom.label_anchors.get(base)
        if rec and len(rec["points"]) >= 2:
            mid = edge_midpoint(rec["points"])
            item["midpoint"] = [round(mid[0], 1), round(mid[1], 1)]
            if anchor:
                item["labelAnchor"] = [round(anchor[0], 1), round(anchor[1], 1)]
                item["distanceToEdgePx"] = round(point_polyline_distance(anchor, rec["points"]), 2)
        labels.append(item)
    out["labelBinding"] = OrderedDict([
        ("method", "SVG label group matched to the edge by from/to (edge id L_<from>_<to>_<n>); "
                   "text compared whitespace-insensitively; the distance from the label anchor "
                   "(edgeLabel translate + label translate) to the edge polyline is reported as "
                   "binding evidence"),
        ("count", len(labels)),
        ("items", labels),
    ])

    expected = set()
    for el in sem.get("elements") or []:
        if el.get("label"):
            expected.add(norm(el["label"]))
    for zone in sem.get("zones") or []:
        if zone.get("label"):
            expected.add(norm(zone["label"]))
    for rel in sem.get("relations") or []:
        if rel.get("label"):
            expected.add(norm(rel["label"]))
    extra_texts = []
    for text in geom.texts:
        if norm(text) and norm(text) not in expected:
            extra_texts.append(text)
    legend_like = any(re.search(r"图例|legend|含义", t, re.I) for t in extra_texts)
    out["visibleText"] = OrderedDict([
        ("method", "SVG <text> contents compared (whitespace-insensitive) against the expected "
                   "label set; unexplained extras are listed, legend-like extras are flagged"),
        ("svgTextCount", len(geom.texts)),
        ("extraTexts", sorted(set(extra_texts))),
        ("legendLike", legend_like),
    ])

    identity = OrderedDict([
        ("elementsFound", sum(1 for nid in model.nodes if nid in geom.node_rects)),
        ("elementsDeclared", len(model.nodes)),
        ("zonesFound", sum(1 for zid in model.zones if zid in geom.cluster_rects)),
        ("zonesDeclared", len(model.zones)),
        ("missingElementIds", [nid for nid in model.nodes if nid not in geom.node_rects]),
        ("missingZoneIds", [zid for zid in model.zones if zid not in geom.cluster_rects]),
        ("extraNodeGroups", geom.extra_node_groups),
        ("businessEdgesRendered", sum(1 for p in geom.business_paths.values() if p.get("declared"))),
        ("businessEdgesDeclared", len(model.business)),
        ("businessPathsUnresolved", [p["id"] for p in geom.business_paths.values()
                                     if not p.get("declared")]),
    ])
    out["svgIdentity"] = identity
    out["unsupportedGeometry"] = geom.path_unsupported
    limitations = []
    if geom.path_unsupported:
        limitations.append("some edge paths use SVG commands outside M/L; their geometry is "
                           "not evaluated (partial, not clean)")
    for item in containers:
        if item["assessment"] == "unresolved":
            limitations.append("container endpoint %s %s could not be classified within "
                               "tolerance" % (item["relation"], item["side"]))
    out["limitations"] = limitations
    return out


def visual_verdict(geo):
    hard = []
    issues = []
    if geo["svgIdentity"]["businessEdgesRendered"] < geo["svgIdentity"]["businessEdgesDeclared"]:
        hard.append("%d business edge(s) declared but not rendered as resolvable visible paths"
                    % (geo["svgIdentity"]["businessEdgesDeclared"]
                       - geo["svgIdentity"]["businessEdgesRendered"]))
    if geo["svgIdentity"]["missingElementIds"]:
        hard.append("elements missing from the rendered SVG: %s"
                    % ", ".join(geo["svgIdentity"]["missingElementIds"][:8]))
    if geo["svgIdentity"]["missingZoneIds"]:
        hard.append("zones missing from the rendered SVG: %s"
                    % ", ".join(geo["svgIdentity"]["missingZoneIds"][:8]))
    for item in geo["labelBinding"]["items"]:
        if not item["found"]:
            hard.append("edge label missing for %s" % item["relation"])
        elif not item["textMatches"]:
            hard.append("edge label text mismatch for %s (%r != %r)"
                        % (item["relation"], item["svgText"], item["expected"]))
    for item in geo["containerEndpoints"]["items"]:
        if item["assessment"] == "member-landing":
            hard.append("container endpoint %s %s lands on member %s"
                        % (item["relation"], item["side"], item["nearestMember"]))
    if geo["visibleText"]["legendLike"]:
        hard.append("legend-like extra visible text present")
    if geo["edgeThroughNode"]["count"]:
        issues.append("%d edge-through-node pair(s) over %d business edge(s)"
                      % (geo["edgeThroughNode"]["count"], geo["edgeThroughNode"]["distinctEdges"]))
    if geo["edgeCrossings"]["count"]:
        issues.append("%d business edge crossing pair(s)" % geo["edgeCrossings"]["count"])
    extras = geo["visibleText"]["extraTexts"]
    if extras and not geo["visibleText"]["legendLike"]:
        issues.append("unexplained extra visible text: %s" % ", ".join(extras[:5]))
    if geo["unsupportedGeometry"]:
        issues.append("unsupported SVG path commands on %d edge(s)"
                      % len(geo["unsupportedGeometry"]))
    if geo["layoutEdgeThroughNode"]["count"]:
        issues.append("%d invisible layout-edge/node overlap(s) (not visible line-work)"
                      % geo["layoutEdgeThroughNode"]["count"])
    return hard, issues


def build_report(args, model, sem, sem_errors, diffs, geom, geo):
    report = OrderedDict()
    report["schema"] = SCHEMA
    report["engine"] = "mermaid"
    report["engineVersion"] = "not_exposed"
    report["source"] = OrderedDict([("path", args.source), ("format", "mmd"),
                                    ("sha256", args.source_sha256)])
    report["semantics"] = OrderedDict([
        ("path", args.semantics), ("sha256", args.semantics_sha256),
        ("counts", OrderedDict([("elements", len(sem.get("elements") or [])),
                                ("zones", len(sem.get("zones") or [])),
                                ("relations", len(sem.get("relations") or []))])),
        ("inputErrors", sem_errors),
    ])
    colors = business_color_map(model)
    report["records"] = OrderedDict([
        ("direction", model.direction),
        ("elements", [{"id": nid, "label": model.nodes[nid], "zone": model.node_zone.get(nid)}
                      for nid in model.nodes]),
        ("zones", [{"id": zid, "label": model.zones[zid], "parent": model.zone_parent.get(zid)}
                   for zid in model.zones]),
        ("relations", [{"index": i, "from": r["from"], "to": r["to"],
                        "label": r.get("label", ""), "arrow": r["arrow"],
                        "colorFamily": colors.get(i)}
                       for i, r in enumerate(model.business)]),
        ("layoutEdges", list(model.layout)),
        ("linkStyleColors", OrderedDict((str(k), v) for k, v in sorted(model.link_colors.items()))),
        ("classDefinitionCount", len(model.class_defs)),
        ("idStyleCount", len(model.id_styles)),
        ("unsupportedConstructs", model.unsupported),
        ("notes", model.notes),
    ])

    unsupported = list(model.unsupported) + list(sem_errors)
    for item in (geo or {}).get("unsupportedGeometry", []):
        unsupported.append("svg-path-commands:%s" % ",".join(item["commands"]))
    semantic = OrderedDict()
    if diffs["hardDiffCount"]:
        semantic["status"] = "partial" if unsupported else "fail"
    else:
        semantic["status"] = "partial" if unsupported else "pass"
    semantic["diffs"] = diffs
    if unsupported and diffs["hardDiffCount"]:
        semantic["note"] = ("diffs exist while unsupported constructs were parsed; capped at "
                           "partial because a parser limitation cannot be told apart from "
                           "graph corruption")
    report["semantic"] = semantic

    visual = OrderedDict()
    if geom is None:
        visual["status"] = "not_evaluated"
        visual["reason"] = "no --svg supplied"
    else:
        hard, issues = visual_verdict(geo)
        visual["status"] = "fail" if hard else ("partial" if issues else "pass")
        visual["hardDefects"] = hard
        visual["issues"] = issues
        visual["checks"] = geo
        svg = OrderedDict([("path", args.svg), ("sha256", args.svg_sha256)])
        if geom.view_box:
            vbw, vbh = geom.view_box[2], geom.view_box[3]
            svg["viewBox"] = [vbw, vbh]
            svg["aspect"] = round(vbw / vbh, 3) if vbh else None
        if geom.root_font_px and geom.view_box and geom.view_box[2]:
            ratio = args.display_width / geom.view_box[2]
            svg["rootFontPx"] = geom.root_font_px
            svg["displayWidthPx"] = args.display_width
            svg["effectiveFontPx"] = round(geom.root_font_px * ratio, 2)
        visual["svg"] = svg
    report["visual"] = visual
    report["unsupported"] = unsupported
    report["notEvaluated"] = [] if geom is not None else ["svg-geometry"]
    statuses = [semantic["status"], visual["status"]]
    if "fail" in statuses:
        overall = "fail"
    elif all(s == "pass" for s in statuses):
        overall = "pass"
    else:
        overall = "partial"
    report["overall"] = OrderedDict([
        ("status", overall),
        ("semantic", semantic["status"]),
        ("visual", visual["status"]),
        ("exitCodeSemantics", "0 pass; 1 fail; 3 partial (not pass); 2 usage; 4 output exists; 5 input unreadable"),
    ])
    # Canonical quality-gate shape: `overall` is a status string, the detail is kept beside it.
    report["overall_status_detail"] = report["overall"]
    report["overall"] = overall
    report["not_evaluated"] = report.pop("notEvaluated")
    # Canonical quality-gate field: what was actually parsed out of the .mmd file.
    report["actual"] = report["records"]
    return report


def main(argv):
    args_list = list(argv)
    if "--" in args_list:
        args_list = args_list[:args_list.index("--")]
    for token in args_list:
        if token in ("-h", "--help"):
            sys.stdout.write(USAGE)
            return 0
        if token == "--version":
            sys.stdout.write("%s %s\n" % (
                SCRIPT_NAME, script_version(os.path.dirname(os.path.abspath(__file__)))))
            return 0
    known = {"--source", "--semantics", "--svg", "--output", "--display-width",
             "--container-tolerance", "--crossing-endpoint-exclusion", "--min-clip-px"}
    for token in args_list:
        if token.startswith("-"):
            name = token.split("=", 1)[0]
            if name not in known:
                sys.stderr.write("error: unrecognized option: %s\n" % token)
                sys.stderr.write(USAGE)
                return 2
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--source")
    parser.add_argument("--semantics")
    parser.add_argument("--svg")
    parser.add_argument("--output")
    parser.add_argument("--display-width", type=int, default=1400)
    parser.add_argument("--container-tolerance", type=float, default=6.0)
    parser.add_argument("--crossing-endpoint-exclusion", type=float, default=3.0)
    parser.add_argument("--min-clip-px", type=float, default=0.5)
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        sys.stderr.write(USAGE)
        return 2
    if not args.source or not args.semantics or not args.output:
        sys.stderr.write("error: --source, --semantics and --output are required\n")
        sys.stderr.write(USAGE)
        return 2
    if os.path.exists(args.output):
        sys.stderr.write("error: refusing to overwrite existing report: %s\n" % args.output)
        return 4
    for label in ("source", "semantics", "svg"):
        path = getattr(args, label)
        if path and not os.path.isfile(path):
            sys.stderr.write("error: %s not found: %s\n" % (label, path))
            return 5
    try:
        source_text, source_raw = read_text(args.source)
        with open(args.semantics, "rb") as fh:
            sem_raw = fh.read()
        sem = json.loads(sem_raw.decode("utf-8"))
        args.source_sha256 = sha256_bytes(source_raw)
        args.semantics_sha256 = sha256_bytes(sem_raw)
        model = parse_mermaid(source_text)
        sem_errors = semantics_errors(sem)
        diffs = semantic_diff(model, sem)
        geom = None
        geo = None
        if args.svg:
            svg_text, svg_raw = read_text(args.svg)
            args.svg_sha256 = sha256_bytes(svg_raw)
            geom = parse_svg(svg_text, model)
            geo = measure_geometry(geom, model, sem, args)
        report = build_report(args, model, sem, sem_errors, diffs, geom, geo)
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    except (OSError, ValueError) as exc:
        sys.stderr.write("error: input unreadable: %s\n" % exc)
        return 5
    status = report["overall"]
    sys.stdout.write("native-readback: %s (hard semantic diffs=%d, edge-through-node pairs=%s)\n" % (
        status, diffs["hardDiffCount"],
        (geo or {}).get("edgeThroughNode", {}).get("count", "not_evaluated")))
    return {"pass": 0, "fail": 1, "partial": 3}[status]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
