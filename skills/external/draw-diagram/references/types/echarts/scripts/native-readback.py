#!/usr/bin/env python3
"""Native readback for the ECharts engine.

Reads the actual ECharts option (or the served HTML that embeds it), optionally a
rendered SVG export, and reports:
  - actual native records (components with category-index -> zoneId resolution,
    categories with parent, container endpoints, lines, arrows, labels, legend,
    zone rects)
  - semantic diff against the authoritative semantics JSON
  - geometry evidence: arrow apex landing and direction (native declared rotation
    under the measured ECharts 5.6.0 convention, and the actual rendered SVG arrow
    paths when --svg is supplied), source ends, container endpoints, crossings,
    edge-through-node hits, label binding and attribution
  - explicit unsupported / not_evaluated items

Usage:
  native-readback.py --source <option.json|served.html> --semantics <semantics.json>
                     [--svg <rendered.svg>] --output <new-report.json>

Exit codes:
  0  no hard discrepancy (report written; overall may still be partial only when
     the limitations are declared)
  1  hard discrepancy (semantic delta or hard visual failure)
  2  usage or I/O error (including refusing to overwrite the output)
  3  partial evidence: unsupported syntax or insufficient identity prevents judging
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import edge_series as es

VERSION = "1.0.0"
COLOR_MEANING = re.compile(
    r"#[0-9a-fA-F]{3,8}|\b(red|green|gray|grey|dark)\b|红|绿|灰|深灰|暗红",
    re.IGNORECASE,
)
ARROW_ROTATION_METHOD = (
    "arrow apex = center + (sin(-symbolRotate), -cos(-symbolRotate)) * symbolHeight/2; "
    "convention measured on ECharts 5.6.0 SVG exports (theta_svg = -symbolRotate)"
)


def normalize_color(value):
    if not isinstance(value, str):
        return None
    text = value.strip().lower()
    match = re.match(r"^rgb\((\d+),\s*(\d+),\s*(\d+)\)$", text)
    if match:
        return "#" + "".join(f"{int(part):02x}" for part in match.groups())
    return text


def build_parser():
    parser = argparse.ArgumentParser(
        prog="native-readback.py",
        description="ECharts native readback: actual records, semantic diff and geometry evidence.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--source", required=True, help="ECharts option JSON or served HTML with an embedded OPTION")
    parser.add_argument("--semantics", required=True, help="authoritative semantics JSON")
    parser.add_argument("--svg", help="rendered SVG export of the same option")
    parser.add_argument("--output", required=True, help="new report file (must not exist)")
    return parser


def compare_semantics(actual, semantics):
    hard = []
    warnings = []
    unsupported = []
    diffs = {
        "missing_element_ids": [],
        "extra_element_ids": [],
        "element_label_mismatches": [],
        "element_zone_mismatches": [],
        "duplicate_element_ids": list(actual["duplicate_node_ids"]),
        "missing_zone_ids": [],
        "extra_zone_ids": [],
        "zone_label_mismatches": [],
        "zone_parent_mismatches": [],
        "missing_relation_ids": [],
        "extra_relation_ids": [],
        "relation_endpoint_mismatches": [],
        "relation_direction_mismatches": [],
        "relation_label_mismatches": [],
        "relation_color_mismatches": [],
        "expanded_container_endpoints": [],
        "graph_link_endpoint_mismatches": [],
        "count_mismatches": [],
        "legend_missing_entries": [],
        "legend_extra_entries": [],
        "legend_color_semantics": [],
    }
    if diffs["duplicate_element_ids"]:
        hard.append(f"duplicate native node ids merged: {diffs['duplicate_element_ids']}")

    expected_elements = {e["id"]: e for e in semantics.get("elements", [])}
    components = es.components(actual)
    actual_elements = {}
    for node in components:
        if not isinstance(node["id"], str):
            unsupported.append("a component datum has no string id")
            continue
        actual_elements[node["id"]] = node
    for eid, expected in expected_elements.items():
        node = actual_elements.get(eid)
        if node is None:
            diffs["missing_element_ids"].append(eid)
            continue
        if node["label"] != expected.get("label"):
            diffs["element_label_mismatches"].append(
                {"id": eid, "actual": node["label"], "expected": expected.get("label")}
            )
        if node["zone"] != expected.get("zone"):
            diffs["element_zone_mismatches"].append(
                {"id": eid, "actual": node["zone"], "expected": expected.get("zone"),
                 "categoryIndex": node["categoryIndex"], "categoryName": node["categoryName"]}
            )
    for eid in actual_elements:
        if eid not in expected_elements:
            diffs["extra_element_ids"].append(eid)

    expected_zones = {z["id"]: z for z in semantics.get("zones", [])}
    actual_zones = {}
    for category in actual["categories"]:
        zid = category["zoneId"]
        if zid is None:
            unsupported.append(f"category index {category['index']} has no zoneId")
            continue
        if zid in actual_zones:
            hard.append(f"duplicate category zoneId: {zid}")
            continue
        actual_zones[zid] = category
    for zid, expected in expected_zones.items():
        category = actual_zones.get(zid)
        if category is None:
            diffs["missing_zone_ids"].append(zid)
            continue
        label = category["zoneLabel"] if category["zoneLabel"] is not None else category["name"]
        if label != expected.get("label"):
            diffs["zone_label_mismatches"].append({"id": zid, "actual": label, "expected": expected.get("label")})
        if category["parent"] != expected.get("parent"):
            diffs["zone_parent_mismatches"].append(
                {"id": zid, "actual": category["parent"], "expected": expected.get("parent")}
            )
    for zid in actual_zones:
        if zid not in expected_zones:
            diffs["extra_zone_ids"].append(zid)

    expected_relations = {r["id"]: r for r in semantics.get("relations", [])}
    actual_relations = {}
    identity = "semanticId"
    for rel in actual["relations"]:
        sid = rel["semanticId"]
        if sid is None:
            identity = "endpoint_label_multiset"
            continue
        actual_relations[sid] = rel
    if identity != "semanticId":
        actual_relations = _multiset_match(actual["relations"], expected_relations, diffs, warnings)
    expanded_targets = {category["zoneId"]: set() for category in actual["categories"] if category["zoneId"]}
    for node in components:
        if node["zone"] in expanded_targets and node["id"]:
            expanded_targets[node["zone"]].add(node["id"])
    for rid, expected in expected_relations.items():
        rel = actual_relations.get(rid)
        if rel is None:
            diffs["missing_relation_ids"].append(rid)
            continue
        actual_from, actual_to = rel["from"], rel["to"]
        if (actual_from, actual_to) == (expected.get("to"), expected.get("from")):
            diffs["relation_direction_mismatches"].append(
                {"id": rid, "actual": [actual_from, actual_to], "expected": [expected.get("from"), expected.get("to")]}
            )
        elif (actual_from, actual_to) != (expected.get("from"), expected.get("to")):
            diffs["relation_endpoint_mismatches"].append(
                {"id": rid, "actual": [actual_from, actual_to], "expected": [expected.get("from"), expected.get("to")]}
            )
        for endpoint, actual_endpoint in (("from", actual_from), ("to", actual_to)):
            expected_endpoint = expected.get(endpoint)
            if isinstance(expected_endpoint, str) and expected_endpoint in expected_zones:
                if actual_endpoint != expected_endpoint and actual_endpoint in expanded_targets.get(expected_endpoint, set()):
                    diffs["expanded_container_endpoints"].append(
                        {"id": rid, "side": endpoint, "expected": expected_endpoint, "actual": actual_endpoint}
                    )
            if isinstance(expected_endpoint, str) and expected_endpoint in expected_elements:
                if actual_endpoint in expected_zones:
                    diffs["relation_endpoint_mismatches"].append(
                        {"id": rid, "side": endpoint, "actual": actual_endpoint, "expected": expected_endpoint}
                    )
        if rel["label"] != expected.get("label"):
            diffs["relation_label_mismatches"].append(
                {"id": rid, "actual": rel["label"], "expected": expected.get("label")}
            )
        expected_color = normalize_color(expected.get("color"))
        actual_color = normalize_color(rel["color"])
        if expected_color is not None and actual_color is not None and expected_color != actual_color:
            diffs["relation_color_mismatches"].append(
                {"id": rid, "actual": rel["color"], "expected": expected.get("color")}
            )
        if expected_color is not None and actual_color is None:
            unsupported.append(f"relation {rid} has no native line color; color family not judged")
    for rid in actual_relations:
        if rid not in expected_relations:
            diffs["extra_relation_ids"].append(rid)

    declared_links = [link for link in actual.get("graph_links", []) if link.get("semanticId")]
    if declared_links and identity == "semanticId":
        for link in declared_links:
            rel = actual_relations.get(link["semanticId"])
            if rel is None:
                warnings.append(f"graph link {link['semanticId']} has no visible line")
                continue
            resolved_source, source_note = _resolve_endpoint(link.get("source"), actual)
            resolved_target, target_note = _resolve_endpoint(link.get("target"), actual)
            if source_note or target_note:
                unsupported.append(
                    f"graph link {link['semanticId']} endpoint identity ambiguous: {source_note or target_note}"
                )
                continue
            if (resolved_source, resolved_target) != (rel["from"], rel["to"]):
                diffs["graph_link_endpoint_mismatches"].append(
                    {"id": link["semanticId"],
                     "declared": [link.get("source"), link.get("target")],
                     "resolved": [resolved_source, resolved_target],
                     "drawn": [rel["from"], rel["to"]]}
                )
        linked = {link["semanticId"] for link in declared_links}
        for rid in actual_relations:
            if rid not in linked:
                warnings.append(f"visible relation {rid} has no graph link declaration")
        for item in diffs["graph_link_endpoint_mismatches"]:
            hard.append(f"graph_link_endpoint_mismatches: {item}")

    expected_label_counts = Counter(r.get("label") for r in expected_relations.values() if r.get("label"))
    actual_label_counts = Counter(r.get("label") for r in actual["relations"] if r.get("label"))
    for label, count in expected_label_counts.items():
        if actual_label_counts.get(label, 0) != count:
            warnings.append(
                f"relation label multiset differs for {label!r}: actual {actual_label_counts.get(label, 0)} expected {count}"
            )

    counts = semantics.get("counts") or {}
    actual_counts = {
        "elements": len(components),
        "zones": len(actual["categories"]),
        "relations": len(actual["relations"]),
    }
    for key, expected_count in counts.items():
        if key in actual_counts and actual_counts[key] != expected_count:
            diffs["count_mismatches"].append({"key": key, "actual": actual_counts[key], "expected": expected_count})

    category_names = [c["name"] for c in actual["categories"] if c["name"]]
    legend = actual["legend"]
    for entry in legend:
        if entry not in category_names:
            diffs["legend_extra_entries"].append(entry)
            if COLOR_MEANING.search(entry):
                diffs["legend_color_semantics"].append(entry)
    for name in category_names:
        if name not in legend:
            diffs["legend_missing_entries"].append(name)

    for key in (
        "missing_element_ids", "extra_element_ids", "element_label_mismatches", "element_zone_mismatches",
        "duplicate_element_ids", "missing_zone_ids", "extra_zone_ids", "zone_label_mismatches",
        "zone_parent_mismatches", "missing_relation_ids", "extra_relation_ids",
        "relation_endpoint_mismatches", "relation_direction_mismatches", "relation_label_mismatches",
        "relation_color_mismatches", "expanded_container_endpoints", "count_mismatches",
        "legend_color_semantics",
    ):
        if diffs[key]:
            hard.append(f"{key}: {diffs[key]}")
    if diffs["legend_extra_entries"] and not diffs["legend_color_semantics"]:
        warnings.append(f"extra legend entries without color meanings: {diffs['legend_extra_entries']}")
    if diffs["legend_missing_entries"]:
        warnings.append(f"legend entries missing (filter incomplete): {diffs['legend_missing_entries']}")

    if hard:
        status = "fail"
    elif unsupported:
        status = "partial"
    else:
        status = "pass"
    return {
        "status": status,
        "identity": identity,
        "diffs": diffs,
        "hard": hard,
        "warnings": warnings,
        "unsupported": unsupported,
        "counts": {"expected": counts, "actual": actual_counts},
    }


def _resolve_endpoint(raw, actual):
    """Resolve a graph-link endpoint declared as node id, unique node name or data index."""
    if raw is None or isinstance(raw, bool):
        return None, "missing"
    if isinstance(raw, (int, float)):
        index = int(raw)
        nodes = actual["nodes"]
        if 0 <= index < len(nodes):
            return nodes[index]["id"], None
        return None, f"data index {index} out of range"
    if isinstance(raw, str):
        ids = {node["id"] for node in actual["nodes"] if isinstance(node["id"], str)}
        if raw in ids:
            return raw, None
        matches = [node["id"] for node in actual["nodes"] if node["id"] and node["label"] == raw]
        if len(matches) == 1:
            return matches[0], None
        if len(matches) > 1:
            return None, f"name {raw!r} matches several node ids {matches}"
        return raw, None
    if isinstance(raw, dict):
        value = raw.get("id") or raw.get("name")
        return (value, None) if isinstance(value, str) else (None, "unsupported endpoint object")
    return None, "unsupported endpoint form"


def _multiset_match(actual_relations, expected_relations, diffs, warnings):
    matched = {}
    remaining = [r for r in actual_relations if r.get("semanticId") is None]
    for rid, expected in expected_relations.items():
        for rel in remaining:
            if rel["from"] == expected.get("from") and rel["to"] == expected.get("to") and (
                (rel.get("label") or None) == (expected.get("label") or None)
            ):
                matched[rid] = rel
                remaining.remove(rel)
                break
    if remaining:
        warnings.append(
            f"{len(remaining)} native relations could not be identified by endpoint+label multiset"
        )
    return matched


def geometry(actual, svg_metrics=None):
    relations = [r for r in actual["relations"] if len(r["coords"]) >= 2]
    components = es.components(actual)
    issues = []
    limitations = []
    zone_members = defaultdict(list)
    for node in components:
        if node["zone"]:
            zone_members[node["zone"]].append(node)
    direction_checks = []
    tip_checks = []
    source_checks = []
    container_checks = []
    per_relation = []
    for rel in relations:
        sid = rel["semanticId"]
        arrow = actual["arrows"].get(sid)
        if arrow is None:
            issues.append({"kind": "missing-arrow", "id": sid})
            continue
        if not arrow["supportedSymbol"]:
            limitations.append(f"arrow {sid} symbol family unsupported: {arrow['symbol']!r}")
            continue
        approach, approach_source = es.final_approach(rel, arrow)
        if approach is None:
            limitations.append(f"arrow {sid} approach undetermined")
            continue
        declared = arrow["symbolRotate"]
        apex_native = es.rendered_apex(arrow["center"], declared, arrow["h"])
        rendered_dir = es.rendered_direction(declared) if declared is not None else None
        mismatch = es.direction_mismatch_deg(rendered_dir, approach) if rendered_dir else None
        apex = apex_native
        apex_source = "native-declared"
        if svg_metrics is not None:
            measured = svg_metrics["arrows"].get(sid)
            if measured is None:
                issues.append({"kind": "svg-arrow-unmatched", "id": sid})
            else:
                apex = measured["apex"]
                apex_source = "rendered-svg"
                rendered_dir = measured["direction"]
                mismatch = es.direction_mismatch_deg(rendered_dir, approach)
                if apex_native is not None and measured["apex"] is not None:
                    delta = math.hypot(apex_native[0] - measured["apex"][0], apex_native[1] - measured["apex"][1])
                    if delta > 0.75:
                        limitations.append(
                            f"arrow {sid} declared-vs-rendered apex differ by {round(delta, 2)} px; rendered geometry used"
                        )
        if mismatch is not None and mismatch > es.DIRECTION_TOL_DEG:
            direction_checks.append({"id": sid, "mismatchDeg": round(mismatch, 1)})
        target_rect, target_kind = es.target_rect(actual, rel["to"])
        landing = None
        if apex is None or target_rect is None:
            limitations.append(f"relation {sid} target geometry undetermined ({target_kind})")
        else:
            landing = es.rect_relation(apex, target_rect)
            if target_kind == "element":
                if not landing["onBorder"]:
                    tip_checks.append({"id": sid, "apex": _round_pair(apex), "target": rel["to"], **landing})
            else:
                member_hit = None
                for member in zone_members.get(rel["to"], []):
                    box = es.node_box(member)
                    if box is None:
                        continue
                    inside = es.rect_relation(apex, box, tolerance=0.5)["inside"]
                    if inside and member["id"] not in (rel["from"], rel["to"]):
                        member_hit = member["id"]
                        break
                container_checks.append({
                    "id": sid, "zone": rel["to"], "apex": _round_pair(apex),
                    "insideZone": landing["inside"], "memberHit": member_hit,
                })
                if not landing["inside"]:
                    issues.append({"kind": "container-arrow-outside-zone", "id": sid, "zone": rel["to"]})
                if member_hit:
                    issues.append({"kind": "container-arrow-lands-on-member", "id": sid, "member": member_hit})
        source_point = rel["coords"][0]
        source_rect, source_kind = es.target_rect(actual, rel["from"])
        source_ok = None
        if source_rect is None:
            limitations.append(f"relation {sid} source geometry undetermined ({source_kind})")
        else:
            source_rel = es.rect_relation(source_point, source_rect)
            if source_kind == "element":
                source_ok = source_rel["onBorder"]
                if not source_ok:
                    source_checks.append({"id": sid, "start": _round_pair(source_point), "source": rel["from"], **source_rel})
            else:
                source_ok = source_rel["inside"]
                if not source_ok:
                    issues.append({"kind": "container-source-outside-zone", "id": sid, "zone": rel["from"]})
        per_relation.append({
            "id": sid,
            "from": rel["from"],
            "to": rel["to"],
            "label": rel["label"],
            "color": rel["color"],
            "segments": len(rel["coords"]) - 1,
            "approachSource": approach_source,
            "symbolRotate": declared,
            "apex": _round_pair(apex) if apex else None,
            "apexSource": apex_source,
            "targetKind": target_kind,
            "directionMismatchDeg": round(mismatch, 2) if mismatch is not None else None,
            "landing": landing,
            "sourceOnBorder": source_ok,
        })
    for item in direction_checks:
        issues.append({"kind": "arrow-direction", **item})
    for item in tip_checks:
        issues.append({"kind": "arrow-tip-off-target", **item})
    for item in source_checks:
        issues.append({"kind": "source-end-off-target", **item})

    crossings = []
    collinear = []
    for i in range(len(relations)):
        a = relations[i]
        for j in range(i + 1, len(relations)):
            b = relations[j]
            for sa in range(len(a["coords"]) - 1):
                for sb in range(len(b["coords"]) - 1):
                    result = es.segment_intersection(a["coords"][sa], a["coords"][sa + 1], b["coords"][sb], b["coords"][sb + 1])
                    if not result:
                        continue
                    if "collinear" in result:
                        collinear.append({"a": a["semanticId"], "b": b["semanticId"], "length": round(result["collinear"], 2)})
                    else:
                        crossings.append({"a": a["semanticId"], "b": b["semanticId"], "at": _round_pair(result["point"])})
    through = []
    component_boxes = [(n["id"], es.node_box(n)) for n in components if n["id"]]
    for rel in relations:
        for node_id, box in component_boxes:
            if box is None or node_id in (rel["from"], rel["to"]):
                continue
            for index in range(len(rel["coords"]) - 1):
                if es.segment_rect_hit(rel["coords"][index], rel["coords"][index + 1], box, pad=1.0):
                    through.append({"id": rel["semanticId"], "node": node_id, "segment": index})
                    break
    if through:
        issues.append({"kind": "edge-through-node", "count": len(through)})

    label_details = []
    misattributed = []
    unbound = []
    relation_by_id = {r["semanticId"]: r for r in relations}
    for label in actual["labels"]:
        sid = label["semanticId"]
        rel = relation_by_id.get(sid)
        if rel is None or label["point"] is None:
            limitations.append(f"label {sid} has no matching polyline or point")
            continue
        own = es.point_polyline_distance(label["point"], rel["coords"])
        other_min = None
        other_id = None
        for candidate_id, candidate in relation_by_id.items():
            if candidate_id == sid:
                continue
            distance = es.point_polyline_distance(label["point"], candidate["coords"])
            if other_min is None or distance < other_min:
                other_min = distance
                other_id = candidate_id
        entry = {
            "id": sid,
            "text": label["text"],
            "point": _round_pair(label["point"]),
            "ownDistance": round(own, 2),
            "nearestOther": other_id,
            "nearestOtherDistance": round(other_min, 2) if other_min is not None else None,
        }
        label_details.append(entry)
        if other_min is not None and other_min + es.LABEL_MISATTRIBUTION_MARGIN < own:
            misattributed.append(entry)
            issues.append({"kind": "label-misattributed", **entry})
        elif own > es.LABEL_BIND_TOL:
            unbound.append(entry)
            limitations.append(f"label {sid} anchor {round(own, 2)} px off its own polyline (> {es.LABEL_BIND_TOL})")

    visual_issues = [i for i in issues if i["kind"] in (
        "arrow-direction", "arrow-tip-off-target", "source-end-off-target",
        "edge-through-node", "label-misattributed", "container-arrow-outside-zone",
        "container-arrow-lands-on-member", "missing-arrow", "svg-arrow-unmatched",
    )]
    hard = visual_issues
    if svg_metrics is not None:
        hard.extend(svg_metrics["hard"])
        limitations.extend(svg_metrics["limitations"])
    status = "fail" if hard else ("partial" if limitations else "pass")
    return {
        "status": status,
        "method": ARROW_ROTATION_METHOD,
        "relations": per_relation,
        "arrowDirection": {"checked": len(relations), "mismatches": direction_checks},
        "tips": {"checked": len(relations), "offTarget": tip_checks},
        "sources": {"checked": len(relations), "offTarget": source_checks},
        "containerEndpoints": container_checks,
        "crossings": {
            "method": "pairwise polyline segment intersections; collinear overlap length > 1 px counted separately",
            "count": len(crossings),
            "items": crossings,
            "collinear": collinear,
        },
        "edgeThroughNode": through,
        "labels": {
            "checked": len(label_details),
            "details": label_details,
            "misattributed": misattributed,
            "unbound": unbound,
        },
        "issues": issues,
        "limitations": limitations,
    }


def _round_pair(point):
    if point is None:
        return None
    return [round(point[0], 2), round(point[1], 2)]


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _parse_matrix(value):
    match = re.match(r"^matrix\(\s*([-\d.eE, ]+)\s*\)$", value.strip())
    if not match:
        return None
    parts = [float(p) for p in re.split(r"[,\s]+", match.group(1).strip()) if p]
    if len(parts) != 6:
        return None
    return parts


def _apply(matrix, point):
    return [
        matrix[0] * point[0] + matrix[2] * point[1] + matrix[4],
        matrix[1] * point[0] + matrix[3] * point[1] + matrix[5],
    ]


def _path_vertices(d):
    vertices = []
    for match in re.finditer(r"([MLHV])\s*([-\d.eE]+)?[\s,]*([-\d.eE]+)?", d):
        command, a, b = match.group(1), match.group(2), match.group(3)
        if command == "M" or command == "L":
            if a is not None and b is not None:
                vertices.append([float(a), float(b)])
        elif command == "H" and a is not None:
            vertices.append([float(a), vertices[-1][1] if vertices else 0.0])
        elif command == "V" and a is not None:
            vertices.append([vertices[-1][0] if vertices else 0.0, float(a)])
    return vertices


def _is_reflex(points, index, orientation):
    count = len(points)
    prev_point = points[(index - 1) % count]
    point = points[index]
    next_point = points[(index + 1) % count]
    cross = (point[0] - prev_point[0]) * (next_point[1] - point[1]) - (point[1] - prev_point[1]) * (next_point[0] - point[0])
    return cross * orientation < 0


def _orientation(points):
    area = 0.0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        area += x1 * y2 - x2 * y1
    return 1.0 if area >= 0 else -1.0


def _arrow_geometry(points):
    count = len(points)
    if count == 3:
        cx = sum(p[0] for p in points) / 3
        cy = sum(p[1] for p in points) / 3
        order = sorted(range(3), key=lambda i: -((points[i][0] - cx) ** 2 + (points[i][1] - cy) ** 2))
        apex = order[0]
        base = [order[1], order[2]]
        return apex, base
    if count == 4:
        orientation = _orientation(points)
        reflex = [i for i in range(4) if _is_reflex(points, i, orientation)]
        if len(reflex) != 1:
            return None, None
        notch = reflex[0]
        order = sorted(range(4), key=lambda i: -((points[i][0] - points[notch][0]) ** 2 + (points[i][1] - points[notch][1]) ** 2))
        apex = order[0]
        base = [(apex + 1) % 4, (apex - 1) % 4]
        return apex, base
    return None, None


def _arrow_color(actual, semantic_id):
    for rel in actual["relations"]:
        if rel["semanticId"] == semantic_id:
            return rel["color"]
    return None


def svg_checks(svg_path, actual, expected_relation_colors):
    raw = Path(svg_path).read_bytes()
    if b"<!DOCTYPE" in raw or b"<!ENTITY" in raw:
        raise ValueError("SVG carries a DTD or entity declaration; refusing to parse it")
    root = ET.fromstring(raw)
    if _local(root.tag) != "svg":
        raise ValueError("SVG root element not found")
    width = root.get("width")
    height = root.get("height")
    canvas = actual["canvas"]
    limitations = []
    hard = []
    identity = {"status": "partial", "reason": "SVG export carries no stable semantic ids"}
    if width is not None and height is not None and canvas["width"] and canvas["height"]:
        if abs(float(width) - float(canvas["width"])) > 0.5 or abs(float(height) - float(canvas["height"])) > 0.5:
            limitations.append(
                f"SVG size {width}x{height} differs from meta canvas {canvas['width']}x{canvas['height']}; coordinate checks skipped"
            )
            return {
                "available": True, "identity": identity, "texts": None, "arrows": {},
                "hard": hard, "limitations": limitations,
                "canvas": {"width": width, "height": height},
            }
    texts = []
    for element in root.iter():
        if _local(element.tag) == "text":
            text = "".join(element.itertext()).strip()
            if text:
                texts.append(text)
    expected_texts = Counter()
    for title in actual["zone_titles"].values():
        expected_texts[title] += 1
    for node in es.components(actual):
        if node["labelVisible"] and isinstance(node["label"], str):
            expected_texts[node["label"]] += 1
    for label in actual["labels"]:
        if label["text"]:
            expected_texts[label["text"]] += 1
    for entry in actual["legend"]:
        expected_texts[entry] += 1
    actual_texts = Counter(texts)
    missing = expected_texts - actual_texts
    extra = actual_texts - expected_texts
    text_report = {
        "actual": len(texts),
        "expected": sum(expected_texts.values()),
        "missing": {k: v for k, v in list(missing.items())[:20]},
        "missingTotal": sum(missing.values()),
        "extra": {k: v for k, v in list(extra.items())[:20]},
        "extraTotal": sum(extra.values()),
    }
    if missing:
        hard.append({"kind": "svg-text-missing", "items": list(missing)[:10], "count": sum(missing.values())})
    if extra:
        hard.append({"kind": "svg-text-extra", "items": list(extra)[:10], "count": sum(extra.values())})
    arrows = {}
    shared_anchor_groups = []
    native_arrows = [a for a in actual["arrows"].values() if a["center"] is not None]
    groups = {}
    for arrow in native_arrows:
        key = (round(arrow["center"][0] * 2) / 2, round(arrow["center"][1] * 2) / 2, normalize_color(_arrow_color(actual, arrow["semanticId"])))
        groups.setdefault(key, []).append(arrow)
    for key, members in groups.items():
        if len(members) > 1:
            shared_anchor_groups.append({"anchor": [key[0], key[1]], "ids": [m["semanticId"] for m in members]})
    rendered_by_group = defaultdict(list)
    for element in root.iter():
        if _local(element.tag) != "path":
            continue
        fill = normalize_color(element.get("fill"))
        if fill is None or fill not in expected_relation_colors:
            continue
        matrix = _parse_matrix(element.get("transform") or "")
        if matrix is None or abs(matrix[0] * matrix[3] - matrix[1] * matrix[2]) < 0.1:
            continue
        vertices = _path_vertices(element.get("d") or "")
        if len(vertices) < 3:
            continue
        transformed = [_apply(matrix, v) for v in vertices]
        apex_index, base = _arrow_geometry(transformed)
        if apex_index is None:
            limitations.append("unsupported arrow path geometry in the SVG (not a triangle/notch family)")
            continue
        apex = transformed[apex_index]
        base_mid = [
            (transformed[base[0]][0] + transformed[base[1]][0]) / 2,
            (transformed[base[0]][1] + transformed[base[1]][1]) / 2,
        ]
        direction = es.unit([apex[0] - base_mid[0], apex[1] - base_mid[1]])
        center = [matrix[4], matrix[5]]
        key = (round(center[0] * 2) / 2, round(center[1] * 2) / 2, fill)
        if key not in groups:
            hard.append({"kind": "svg-arrow-extra", "center": _round_pair(center), "fill": fill})
            continue
        rendered_by_group[key].append({"apex": _round_pair(apex), "direction": direction, "center": _round_pair(center)})
    for key, members in groups.items():
        rendered = rendered_by_group.get(key, [])
        if len(rendered) < len(members):
            hard.append({"kind": "svg-arrow-missing", "ids": [m["semanticId"] for m in members], "rendered": len(rendered)})
        elif len(rendered) > len(members):
            hard.append({"kind": "svg-arrow-extra-count", "anchor": [key[0], key[1]], "rendered": len(rendered), "native": len(members)})
        if rendered:
            for member in members:
                arrows[member["semanticId"]] = rendered[0]
    if shared_anchor_groups:
        identity_notes = shared_anchor_groups
    else:
        identity_notes = []
    return {
        "available": True,
        "identity": identity,
        "identityNotes": identity_notes,
        "canvas": {"width": width, "height": height},
        "texts": text_report,
        "arrows": arrows,
        "hard": hard,
        "limitations": limitations,
    }


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        option, fmt, digest = es.load_option(args.source)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: cannot read source: {exc}", file=sys.stderr)
        return 2
    try:
        semantics = json.loads(Path(args.semantics).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"error: cannot read semantics: {exc}", file=sys.stderr)
        return 2
    output = Path(args.output)
    if output.exists():
        print(f"error: refusing to overwrite existing output: {output}", file=sys.stderr)
        return 2
    try:
        actual = es.extract(option)
    except ValueError as exc:
        print(f"error: cannot extract native records: {exc}", file=sys.stderr)
        return 3
    semantic = compare_semantics(actual, semantics)
    svg_report = None
    svg_metrics = None
    if args.svg:
        expected_colors = {normalize_color(r["color"]) for r in actual["relations"] if normalize_color(r["color"])}
        try:
            svg_report = svg_checks(args.svg, actual, expected_colors)
        except (OSError, ET.ParseError, ValueError) as exc:
            print(f"error: cannot read SVG: {exc}", file=sys.stderr)
            return 2
        if svg_report["texts"] is not None:
            svg_metrics = {"arrows": svg_report["arrows"], "hard": svg_report["hard"], "limitations": svg_report["limitations"]}
    visual = geometry(actual, svg_metrics)
    if svg_report is not None:
        if svg_report["texts"] is not None and (svg_report["texts"]["missingTotal"] or svg_report["texts"]["extraTotal"]):
            if visual["status"] != "fail":
                visual["status"] = "fail"
        for issue in svg_report["hard"]:
            visual["issues"].append(issue)
        visual["svg"] = {
            "identity": svg_report["identity"],
            "identityNotes": svg_report["identityNotes"],
            "canvas": svg_report["canvas"],
            "texts": svg_report["texts"],
            "arrowCount": len(svg_report["arrows"]),
        }
    unsupported = list(semantic.get("unsupported", []))
    not_evaluated = ["interaction: not exercised by the readback (use the browser measure for tooltip/legend evidence)"]
    if not args.svg:
        not_evaluated.append("rendered SVG geometry: --svg not provided; arrow apexes come from the declared rotation convention")
    limitations = visual.get("limitations", [])
    if semantic["status"] == "fail" or visual["status"] == "fail":
        overall = "fail"
    elif semantic["status"] == "partial" or visual["status"] == "partial" or unsupported:
        overall = "partial"
    else:
        overall = "pass"
    report = {
        "engine": "echarts",
        "schema": "draw-diagram-native-readback/1",
        "script": {"name": "native-readback.py", "version": VERSION},
        "source": {"path": str(args.source), "format": fmt, "sha256": digest},
        "semantics": {"path": str(args.semantics), "sha256": es.sha256_file(args.semantics)},
        "svgSource": {"path": str(args.svg), "sha256": es.sha256_file(args.svg)} if args.svg else None,
        "actual": actual,
        "semantic": semantic,
        "visual": visual,
        "interaction": {"status": "not_evaluated", "reason": "readback does not drive a browser"},
        "unsupported": unsupported,
        "not_evaluated": not_evaluated,
        "limitations": limitations,
        "overall": overall,
        "exit": {"code": 1 if overall == "fail" else (3 if overall == "partial" else 0),
                 "meaning": "0 pass / 1 hard discrepancy / 2 usage or I/O / 3 partial evidence"},
    }
    try:
        with open(output, "x", encoding="utf-8") as handle:
            handle.write(json.dumps(report, ensure_ascii=False, indent=1) + "\n")
    except FileExistsError:
        print(f"error: refusing to overwrite existing output: {output}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"error: cannot write output: {exc}", file=sys.stderr)
        return 2
    summary = {
        "engine": "echarts",
        "source": report["source"],
        "semantic": semantic["status"],
        "visual": visual["status"],
        "overall": overall,
        "crossings": visual["crossings"]["count"],
        "arrowDirectionMismatches": len(visual["arrowDirection"]["mismatches"]),
        "tipsOffTarget": len(visual["tips"]["offTarget"]),
        "labelsMisattributed": len(visual["labels"]["misattributed"]),
        "svg": bool(args.svg),
        "output": str(output),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 1 if overall == "fail" else (3 if overall == "partial" else 0)


if __name__ == "__main__":
    sys.exit(main())
