#!/usr/bin/env python3
"""compose-flowchart.py — deterministic Mermaid flowchart source generation.

Turns an authoritative semantics JSON (elements / zones with parents /
relations in R order, optional per-relation colour families) into a `.mmd`
flowchart. The generator exists because the previous hand-authored sources put
three things under human control that the machine can own correctly:

  * the relation order — declared order IS the stable relation index, so it is
    emitted exactly in input order (caller-side relation numbering stays traceable);
  * the `linkStyle` indices — they are computed from the emitted edge order, so
    a colour family can never drift onto the wrong relation;
  * the layout scaffolding — see --scaffold below.

`--scaffold isolated` (default) emits `~~~` chains ONLY for items that no
business relation touches. Connected members keep dagre's flow ranking: a
hand-written chain that locks connected siblings into one rank is exactly what
makes long edges cross over their neighbours. `--scaffold all` chains every
sibling item in declaration order (the classic SDS "row lock" approach, kept
for diagrams that need a fixed narrative order). `--member-order flow` sorts
each zone's members by the intra-zone relation direction (deterministic
topological order, input order as tie-break) instead of declaration order.

Zones become nested subgraphs following `zones[].parent`; container endpoints
(relations whose endpoint is a zone id) are emitted verbatim — never expanded
to a member. No business data, path, count or server address is compiled into
this script: everything comes from the semantics file.

Exit codes: 0 written; 1 semantics invalid/unsupported; 2 usage error;
4 output file already exists; 5 input unreadable.
"""

import argparse
import json
import os
import re
import sys
from collections import OrderedDict

SCRIPT_NAME = "compose-flowchart.py"
ID_RE = re.compile(r'^[A-Za-z0-9_.\-]+$')

USAGE = """usage: compose-flowchart.py --semantics <semantics.json> --output <new.mmd>
                         [--direction TB|TD|LR|RL] [--scaffold isolated|all|none]
                         [--member-order declared|flow] [--title TITLE]

options:
  --semantics PATH   authoritative semantics JSON (elements/zones/relations)
  --output PATH      new .mmd path; an existing file is refused (exit 4)
  --direction        flowchart direction (default TD)
  --scaffold         isolated = ~~~ chains only for members no relation touches (default);
                     all = chain every sibling item in order; none = no ~~~ edges
  --member-order     declared = input order of elements (default); flow = intra-zone
                     relation order (deterministic topological order)
  --title TEXT       optional title recorded as a comment and init-safe (not rendered)
  -h, --help         print this help and exit
  --version          print the script name and the framework version, then exit

side-effects: writes exactly the --output file; a flag-only invocation writes nothing
exit-codes: 0 written; 1 semantics invalid or unsupported form; 2 usage error; 4 output exists; 5 input unreadable
"""

PALETTE = [
    ("#fff4e6", "#c2740a"), ("#eef4ff", "#3b6fd8"), ("#eafaf1", "#1f8a5b"),
    ("#f3efff", "#6d4bd1"), ("#fff1ee", "#c0503c"), ("#e9f8fa", "#1a7f8e"),
    ("#fdf2f8", "#a21caf"), ("#f7fee7", "#4d7c0f"), ("#f4f4f5", "#71717a"),
]
NESTED_STYLE = ("#ffffff", "#94a3b8")
COMPONENT_STYLE = "fill:#ffffff,stroke:#475569,stroke-width:2px,color:#0f172a"
EDGE_STROKE_WIDTH = "1.5px"
FONT_STACK = "Noto Sans CJK SC, PingFang SC, Microsoft YaHei, Arial, sans-serif"

INIT_TEMPLATE = (
    '%%{init: {"theme": "base", "htmlLabels": false, "themeVariables": {'
    '"fontSize": 16, "fontFamily": "' + FONT_STACK + '", "primaryColor": "#ffffff", '
    '"primaryTextColor": "#0f172a", "primaryBorderColor": "#475569", '
    '"lineColor": "#64748b", "clusterBkg": "#ffffff", "clusterBorder": "#94a3b8", '
    '"edgeLabelBackground": "#ffffff", "tertiaryColor": "#f8fafc", "textColor": "#0f172a"}, '
    '"flowchart": {"curve": "linear", "nodeSpacing": 28, "useMaxWidth": false, '
    '"rankSpacing": 44, "wrappingWidth": 1000, "padding": 10}, '
    '"themeCSS": ".cluster-label text{font-size:18px;font-weight:700;}"}}%%')


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


def validate(sem):
    errors = []
    elements = sem.get("elements") or []
    zones = sem.get("zones") or []
    relations = sem.get("relations") or []
    eids = []
    for el in elements:
        eid = el.get("id")
        if not eid or not ID_RE.match(str(eid)):
            errors.append("element id missing or not a plain token: %r" % eid)
            continue
        if eid in eids:
            errors.append("duplicate element id: %s" % eid)
        eids.append(eid)
        if el.get("zone") is None:
            errors.append("element %s has no zone" % eid)
    zids = [z.get("id") for z in zones]
    for zid in zids:
        if not zid or not ID_RE.match(str(zid)):
            errors.append("zone id missing or not a plain token: %r" % zid)
    for zone in zones:
        parent = zone.get("parent")
        if parent is not None and parent not in zids:
            errors.append("zone %s parent unknown: %s" % (zone.get("id"), parent))
    for el in elements:
        if el.get("zone") is not None and el.get("zone") not in zids:
            errors.append("element %s zone unknown: %s" % (el.get("id"), el.get("zone")))
    counts = sem.get("counts") or {}
    for key, actual in (("elements", len(elements)), ("zones", len(zones)),
                        ("relations", len(relations))):
        if key in counts and counts[key] != actual:
            errors.append("counts.%s=%s but file has %d" % (key, counts[key], actual))
    eidset, zidset = set(eids), set(zids)
    for rel in relations:
        for side in ("from", "to"):
            end = rel.get(side)
            if end not in eidset and end not in zidset:
                errors.append("relation %s endpoint unknown: %s" % (rel.get("id"), end))
        label = rel.get("label") or ""
        if "|" in label or '"' in label:
            errors.append("relation %s label contains an unsupported character: %r"
                          % (rel.get("id"), label))
    for el in elements:
        label = el.get("label") or el.get("id") or ""
        if '"' in label:
            errors.append("element %s label contains a double quote" % el.get("id"))
    for zone in zones:
        label = zone.get("label") or zone.get("id") or ""
        if '"' in label:
            errors.append("zone %s label contains a double quote" % zone.get("id"))
    return errors


def member_order(sem, zone_id, policy):
    elements = [el for el in sem.get("elements") or [] if el.get("zone") == zone_id]
    ordered = [el.get("id") for el in elements]
    if policy != "flow" or len(ordered) < 2:
        return ordered
    index = {eid: i for i, eid in enumerate(ordered)}
    incoming = {eid: 0 for eid in ordered}
    edges = []
    for rel in sem.get("relations") or []:
        a, b = rel.get("from"), rel.get("to")
        if a in index and b in index and a != b:
            edges.append((a, b))
            incoming[b] += 1
    ready = sorted((eid for eid in ordered if incoming[eid] == 0), key=index.get)
    result = []
    while ready:
        current = ready.pop(0)
        result.append(current)
        for a, b in edges:
            if a == current:
                incoming[b] -= 1
                if incoming[b] == 0:
                    ready.append(b)
                    ready.sort(key=index.get)
    for eid in ordered:
        if eid not in result:
            result.append(eid)
    return result


def zone_children(sem):
    children = OrderedDict()
    for zone in sem.get("zones") or []:
        children.setdefault(zone.get("parent"), []).append(zone.get("id"))
    return children


def chain_leaves(sem, zone_id, policy, order_policy, children, incident_members, incident_subtree):
    """Ordered chainable node ids for one zone, honouring the scaffold policy."""
    direct = member_order(sem, zone_id, order_policy)
    items = []
    for eid in direct:
        if policy == "all" or eid not in incident_members:
            items.append(eid)
    for child in children.get(zone_id, []):
        if policy == "all" or child not in incident_subtree:
            leaves = chain_leaves(sem, child, policy, order_policy, children,
                                  incident_members, incident_subtree)
            if leaves:
                items.append(leaves[0])
                if len(leaves) > 1 and leaves[-1] != leaves[0]:
                    items.append(leaves[-1])
    return items


def emit(sem, args):
    zones = sem.get("zones") or []
    elements = sem.get("elements") or []
    relations = sem.get("relations") or []
    zone_by_id = OrderedDict((z.get("id"), z) for z in zones)
    element_by_id = OrderedDict((el.get("id"), el) for el in elements)
    children = zone_children(sem)
    top_zones = children.get(None, [])
    parent_of = dict((zone.get("id"), zone.get("parent")) for zone in zones)

    incident_members = set()
    incident_subtree = set()

    def mark_zone(zid):
        while zid is not None and zid not in incident_subtree:
            incident_subtree.add(zid)
            zid = parent_of.get(zid)

    zone_ids = set(zone_by_id)
    for rel in relations:
        for side in ("from", "to"):
            end = rel.get(side)
            if end in zone_ids:
                mark_zone(end)
            else:
                incident_members.add(end)
    for eid in incident_members:
        el = element_by_id.get(eid)
        if el:
            mark_zone(el.get("zone"))

    chain_lines = []
    if args.scaffold != "none":
        visited = set()

        def walk(zid):
            if zid in visited:
                return
            visited.add(zid)
            leaves = chain_leaves(sem, zid, args.scaffold, args.member_order,
                                  children, incident_members, incident_subtree)
            for a, b in zip(leaves, leaves[1:]):
                pair = "  %s ~~~ %s" % (a, b)
                if pair not in chain_lines:
                    chain_lines.append(pair)
            for child in children.get(zid, []):
                walk(child)

        for zid in top_zones:
            walk(zid)
        for zid in zone_by_id:
            walk(zid)

    lines = [INIT_TEMPLATE, "flowchart %s" % args.direction]
    if args.title:
        lines.append("%%%% %s - generated by compose-flowchart.py" % args.title)

    def emit_zone(zid, depth):
        pad = "  " * (depth + 1)
        label = zone_by_id[zid].get("label") or zid
        lines.append('%ssubgraph %s["%s"]' % (pad, zid, label))
        for eid in member_order(sem, zid, args.member_order):
            el = element_by_id[eid]
            lines.append('%s  %s["%s"]' % (pad, eid, el.get("label") or eid))
        for child in children.get(zid, []):
            emit_zone(child, depth + 1)
        lines.append("%send" % pad)

    for zid in top_zones:
        emit_zone(zid, 0)
    for el in elements:
        if el.get("zone") is None:
            lines.append('  %s["%s"]' % (el.get("id"), el.get("label") or el.get("id")))

    lines.append("%% ---- business relations, declaration order preserved ----")
    for rel in relations:
        label = rel.get("label") or ""
        if label:
            lines.append("  %s -->|%s| %s" % (rel.get("from"), label, rel.get("to")))
        else:
            lines.append("  %s --> %s" % (rel.get("from"), rel.get("to")))

    if chain_lines:
        lines.append("%% ---- invisible layout edges (never business relations) ----")
        lines.extend(chain_lines)

    lines.append("%% ---- component style ----")
    lines.append("  classDef comp %s" % COMPONENT_STYLE)
    ids = [el.get("id") for el in elements]
    chunk = 8
    for i in range(0, len(ids), chunk):
        lines.append("  class %s comp" % ",".join(ids[i:i + chunk]))

    lines.append("%% ---- zone styles ----")
    top_index = {zid: i for i, zid in enumerate(top_zones)}
    for zid, zone in zone_by_id.items():
        if zone.get("parent") is None:
            fill, stroke = PALETTE[top_index.get(zid, 0) % len(PALETTE)]
            lines.append("  style %s fill:%s,stroke:%s,stroke-width:3px,color:#0f172a"
                         % (zid, fill, stroke))
        else:
            lines.append("  style %s fill:%s,stroke:%s,stroke-width:2px,color:#334155"
                         % (zid, NESTED_STYLE[0], NESTED_STYLE[1]))

    lines.append("%% ---- relation colour families (indices = emitted edge order) ----")
    families = OrderedDict()
    for idx, rel in enumerate(relations):
        color = (rel.get("color") or "").lower()
        if color:
            families.setdefault(color, []).append(idx)
    for color, indices in families.items():
        lines.append("  linkStyle %s stroke:%s,stroke-width:%s"
                     % (",".join(str(i) for i in indices), color, EDGE_STROKE_WIDTH))
    return "\n".join(lines) + "\n"


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
    known = {"--semantics", "--output", "--direction", "--scaffold", "--member-order", "--title"}
    for token in args_list:
        if token.startswith("-"):
            name = token.split("=", 1)[0]
            if name not in known:
                sys.stderr.write("error: unrecognized option: %s\n" % token)
                sys.stderr.write(USAGE)
                return 2
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--semantics")
    parser.add_argument("--output")
    parser.add_argument("--direction", choices=["TB", "TD", "LR", "RL"], default="TD")
    parser.add_argument("--scaffold", choices=["isolated", "all", "none"], default="isolated")
    parser.add_argument("--member-order", choices=["declared", "flow"], default="declared")
    parser.add_argument("--title")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        sys.stderr.write(USAGE)
        return 2
    if not args.semantics or not args.output:
        sys.stderr.write("error: --semantics and --output are required\n")
        sys.stderr.write(USAGE)
        return 2
    if os.path.exists(args.output):
        sys.stderr.write("error: refusing to overwrite existing source: %s\n" % args.output)
        return 4
    if not os.path.isfile(args.semantics):
        sys.stderr.write("error: semantics not found: %s\n" % args.semantics)
        return 5
    try:
        with open(args.semantics, "r", encoding="utf-8") as fh:
            sem = json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write("error: semantics unreadable: %s\n" % exc)
        return 5
    errors = validate(sem)
    if errors:
        for err in errors:
            sys.stderr.write("error: %s\n" % err)
        return 1
    text = emit(sem, args)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(text)
    relations = sem.get("relations") or []
    colors = OrderedDict()
    for idx, rel in enumerate(relations):
        color = (rel.get("color") or "").lower()
        if color:
            colors.setdefault(color, []).append(idx)
    scaffold_edges = text.count("~~~")
    sys.stdout.write(json.dumps(OrderedDict([
        ("output", args.output),
        ("counts", OrderedDict([("elements", len(sem.get("elements") or [])),
                                ("zones", len(sem.get("zones") or [])),
                                ("relations", len(relations))])),
        ("scaffold", args.scaffold),
        ("memberOrder", args.member_order),
        ("layoutEdges", scaffold_edges),
        ("colorFamilies", OrderedDict((c, len(i)) for c, i in colors.items())),
    ]), ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
