"""Shared ECharts edge-series helpers for the fixed-layout graph recipe.

One implementation of: option loading (raw option JSON or the served HTML with an
embedded ``var OPTION = ...``), actual native record extraction (category index ->
zoneId, endpoint identity forms, container endpoints, labels, legend, zone rects),
the measured symbolRotate convention, geometry primitives and the deterministic
edge-decoration normalization used by normalize-edge-series.py and native-readback.py.

Renderer convention (measured on ECharts 5.6.0 from actual SVG exports of this
engine's recipe): a scatter symbol carrying ``symbolRotate = R`` renders with SVG
rotation ``theta = -R``; an upward-pointing custom path symbol therefore points along
``(sin(theta), -cos(theta))`` for its apex. The rule and its evidence live in
references/sds-realization.md section 4.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

PRESENTATION_KINDS = ("layout-anchor", "container-endpoint")
ARROW_PATH_APEX = (0.0, -1.0)
BORDER_TOL = 1.5
DIRECTION_TOL_DEG = 5.0
LABEL_BIND_TOL = 3.0
LABEL_MISATTRIBUTION_MARGIN = 2.0
DEGENERATE_SEGMENT_TOL = 6.0


def load_option(path):
    """Load an ECharts option from JSON or from a served HTML embedding ``var OPTION``."""
    raw = Path(path).read_bytes()
    text = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    fmt = "option-json"
    stripped = text.lstrip()
    if stripped.startswith("<"):
        fmt = "served-html"
        match = re.search(r"var\s+OPTION\s*=\s*", text)
        if not match:
            raise ValueError("served HTML does not contain 'var OPTION = ...'")
        decoder = json.JSONDecoder()
        try:
            option, _ = decoder.raw_decode(text, match.end())
        except json.JSONDecodeError as exc:
            raise ValueError(f"cannot decode the embedded OPTION object: {exc}") from exc
    else:
        option = json.loads(text)
    if not isinstance(option, dict):
        raise ValueError("option must be a JSON object")
    return option, fmt, digest


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def symbol_size(value, default=None):
    if isinstance(value, (int, float)):
        return float(value), float(value)
    if isinstance(value, (list, tuple)) and value:
        w = float(value[0])
        h = float(value[1]) if len(value) > 1 else w
        return w, h
    return default


def find_series(option):
    series = option.get("series")
    if isinstance(series, dict):
        series = [series]
    if not isinstance(series, list):
        raise ValueError("option.series is missing")
    graph = None
    for s in series:
        if isinstance(s, dict) and s.get("type") == "graph" and isinstance(s.get("data"), list):
            graph = s
            break
    if graph is None:
        raise ValueError("no graph series with data found")
    arrows = None
    for s in series:
        if not isinstance(s, dict) or s.get("type") != "scatter":
            continue
        data = s.get("data") or []
        if data and isinstance(data[0], dict) and "srcId" in data[0] and "dstId" in data[0] and "symbolRotate" in data[0]:
            arrows = s
            break
    lines = None
    for s in series:
        if not isinstance(s, dict) or s.get("type") != "lines":
            continue
        data = s.get("data") or []
        if data and isinstance(data[0], dict) and "srcId" in data[0] and "dstId" in data[0] and "coords" in data[0]:
            lines = s
            break
    labels = None
    for s in series:
        if not isinstance(s, dict) or s.get("type") != "scatter" or s is arrows:
            continue
        data = s.get("data") or []
        if data and isinstance(data[0], dict) and "srcId" in data[0] and "name" in data[0] and "symbolRotate" not in data[0]:
            labels = s
            break
    return {"graph": graph, "arrows": arrows, "lines": lines, "labels": labels, "series": series}


def option_canvas(option, graph):
    meta = option.get("meta") or {}
    width = meta.get("canvasWidth")
    height = meta.get("canvasHeight")
    if width is None:
        width = graph.get("width")
    if height is None:
        height = graph.get("height")
    return width, height


def resolve_category(raw, categories):
    """Resolve a node's category declaration to (index, category record).

    Supported forms: integer index, zoneId string, or an object with zoneId/id.
    """
    if isinstance(raw, bool):
        return None, None
    if isinstance(raw, (int, float)):
        idx = int(raw)
        if 0 <= idx < len(categories):
            return idx, categories[idx]
        return idx, None
    if isinstance(raw, str):
        for idx, cat in enumerate(categories):
            if cat.get("zoneId") == raw:
                return idx, cat
        return None, None
    if isinstance(raw, dict):
        zid = raw.get("zoneId") or raw.get("id")
        for idx, cat in enumerate(categories):
            if zid is not None and cat.get("zoneId") == zid:
                return idx, cat
    return None, None


def extract_zone_rects(option):
    rects = {}
    titles = {}
    graphic = option.get("graphic")
    if isinstance(graphic, dict):
        graphic = [graphic]
    for item in graphic or []:
        if not isinstance(item, dict):
            continue
        gid = item.get("id") or ""
        match = re.match(r"^zone-rect-(.+)$", gid)
        if match:
            shape = item.get("shape") or {}
            left = item.get("left")
            top = item.get("top")
            width = shape.get("width")
            height = shape.get("height")
            if None not in (left, top, width, height):
                rects[match.group(1)] = [float(left), float(top), float(left) + float(width), float(top) + float(height)]
            continue
        match = re.match(r"^zone-title-(.+)$", gid)
        if match:
            text = ((item.get("style") or {}).get("text"))
            if isinstance(text, str):
                titles[match.group(1)] = text
    return rects, titles


def legend_entries(option):
    legend = option.get("legend")
    if isinstance(legend, list):
        entries = []
        for item in legend:
            entries.extend(_legend_data(item))
        return entries
    return _legend_data(legend)


def _legend_data(legend):
    if not isinstance(legend, dict):
        return []
    data = legend.get("data") or []
    out = []
    for item in data:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict) and isinstance(item.get("name"), str):
            out.append(item["name"])
    return out


def extract(option):
    """Extract the actual native records. Never consults the expected semantics."""
    found = find_series(option)
    graph = found["graph"]
    raw_categories = graph.get("categories") or []
    categories = []
    for idx, cat in enumerate(raw_categories):
        categories.append({
            "index": idx,
            "name": cat.get("name"),
            "zoneId": cat.get("zoneId"),
            "zoneLabel": cat.get("zoneLabel"),
            "parent": cat.get("parent"),
        })
    nodes = []
    id_counts = {}
    for idx, datum in enumerate(graph.get("data") or []):
        if not isinstance(datum, dict):
            continue
        nid = datum.get("id")
        if isinstance(nid, str):
            id_counts[nid] = id_counts.get(nid, 0) + 1
        cat_index, cat = resolve_category(datum.get("category"), categories)
        zone = datum.get("zoneId") or (cat or {}).get("zoneId")
        size = symbol_size(datum.get("symbolSize"))
        label = datum.get("label") or {}
        nodes.append({
            "index": idx,
            "id": nid,
            "label": datum.get("name"),
            "kind": datum.get("kind") or "component",
            "categoryIndex": cat_index,
            "categoryName": (cat or {}).get("name"),
            "zone": zone,
            "x": _num(datum.get("x")),
            "y": _num(datum.get("y")),
            "w": size[0] if size else None,
            "h": size[1] if size else None,
            "labelVisible": bool(label.get("show", True)),
        })
    arrows = {}
    arrow_series = found["arrows"]
    if arrow_series is not None:
        series_size = symbol_size(arrow_series.get("symbolSize"))
        series_symbol = arrow_series.get("symbol")
        for item in arrow_series.get("data") or []:
            if not isinstance(item, dict):
                continue
            size = symbol_size(item.get("symbolSize"), series_size)
            sid = item.get("semanticId")
            arrows[sid] = {
                "semanticId": sid,
                "from": item.get("srcId"),
                "to": item.get("dstId"),
                "center": _pair(item.get("value")),
                "symbolRotate": _num(item.get("symbolRotate")),
                "symbol": item.get("symbol") or series_symbol,
                "w": size[0] if size else None,
                "h": size[1] if size else None,
                "supportedSymbol": is_supported_arrow_symbol(item.get("symbol") or series_symbol),
            }
    relations = []
    line_series = found["lines"]
    if line_series is not None:
        for item in line_series.get("data") or []:
            if not isinstance(item, dict):
                continue
            coords = [_pair(p) for p in (item.get("coords") or []) if _pair(p) is not None]
            style = item.get("lineStyle") or {}
            relations.append({
                "semanticId": item.get("semanticId"),
                "from": item.get("srcId"),
                "to": item.get("dstId"),
                "name": item.get("name"),
                "label": None,
                "color": style.get("color"),
                "width": _num(style.get("width")),
                "coords": coords,
            })
    labels = []
    label_series = found["labels"]
    if label_series is not None:
        for item in label_series.get("data") or []:
            if not isinstance(item, dict):
                continue
            labels.append({
                "semanticId": item.get("semanticId"),
                "from": item.get("srcId"),
                "to": item.get("dstId"),
                "text": item.get("name"),
                "point": _pair(item.get("value")),
            })
    labels_by_id = {l["semanticId"]: l for l in labels}
    for rel in relations:
        lab = labels_by_id.get(rel["semanticId"])
        if lab is not None:
            rel["label"] = lab["text"]
    graph_links = []
    for link in graph.get("links") or []:
        if not isinstance(link, dict):
            continue
        graph_links.append({
            "semanticId": link.get("semanticId"),
            "source": link.get("source"),
            "target": link.get("target"),
            "label": link.get("semanticLabel") or link.get("name"),
        })
    rects, titles = extract_zone_rects(option)
    width, height = option_canvas(option, graph)
    return {
        "series_found": {k: (v is not None) for k, v in found.items() if k != "series"},
        "nodes": nodes,
        "duplicate_node_ids": sorted(k for k, v in id_counts.items() if v > 1),
        "categories": categories,
        "zone_rects": rects,
        "zone_titles": titles,
        "relations": relations,
        "arrows": arrows,
        "labels": labels,
        "graph_links": graph_links,
        "legend": legend_entries(option),
        "canvas": {"width": width, "height": height},
        "arrow_series_symbol": (found["arrows"] or {}).get("symbol"),
    }


def components(actual):
    return [n for n in actual["nodes"] if n["kind"] not in PRESENTATION_KINDS]


def presentation_nodes(actual):
    return [n for n in actual["nodes"] if n["kind"] in PRESENTATION_KINDS]


def node_box(node):
    if None in (node["x"], node["y"], node["w"], node["h"]):
        return None
    half_w = node["w"] / 2.0
    half_h = node["h"] / 2.0
    return [node["x"] - half_w, node["y"] - half_h, node["x"] + half_w, node["y"] + half_h]


def target_rect(actual, endpoint):
    """Return (rect, kind) for a relation endpoint: element box or zone rect."""
    for node in actual["nodes"]:
        if node["id"] == endpoint:
            if node["kind"] == "container-endpoint":
                rect = actual["zone_rects"].get(node["zone"] or endpoint)
                return (rect, "container") if rect else (None, "container")
            box = node_box(node)
            return (box, "element") if box else (None, "element")
    rect = actual["zone_rects"].get(endpoint)
    if rect:
        return rect, "container"
    return None, "unresolved"


def polygon_area(points):
    area = 0.0
    count = len(points)
    for i in range(count):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % count]
        area += x1 * y2 - x2 * y1
    return area / 2.0


def is_supported_arrow_symbol(symbol):
    return isinstance(symbol, str) and symbol.startswith("path://")


def _num(value):
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _pair(value):
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        a, b = _num(value[0]), _num(value[1])
        if a is not None and b is not None:
            return [a, b]
    return None


def unit(vector):
    length = math.hypot(vector[0], vector[1])
    if length < 1e-12:
        return None
    return [vector[0] / length, vector[1] / length]


def correct_symbol_rotate(approach):
    """symbolRotate that makes the rendered apex point along ``approach``.

    Measured convention: svg theta = -symbolRotate and apex direction is
    (sin(theta), -cos(theta)); therefore rotate = atan2(-ux, -uy).
    """
    direction = unit(approach)
    if direction is None:
        return None
    ux, uy = direction
    degrees = math.degrees(math.atan2(-ux, -uy))
    return normalize_degrees(degrees)


def normalize_degrees(degrees):
    value = math.fmod(degrees, 360.0)
    if value <= -180.0:
        value += 360.0
    if value > 180.0:
        value -= 360.0
    return round(value, 3)


def rendered_apex(center, symbol_rotate, height):
    """Apex implied by the declared rotation under the measured convention."""
    if None in (center, symbol_rotate, height):
        return None
    theta = math.radians(-symbol_rotate)
    direction = [math.sin(theta), -math.cos(theta)]
    half = height / 2.0
    return [center[0] + direction[0] * half, center[1] + direction[1] * half]


def rendered_direction(symbol_rotate):
    theta = math.radians(-symbol_rotate)
    return [math.sin(theta), -math.cos(theta)]


def direction_mismatch_deg(a, b):
    ua, ub = unit(a), unit(b)
    if ua is None or ub is None:
        return None
    dot = max(-1.0, min(1.0, ua[0] * ub[0] + ua[1] * ub[1]))
    return math.degrees(math.acos(dot))


def final_approach(rel, arrow):
    """Approach direction of the visible route plus its evidence class.

    Precedence: the vector from the line end to the arrow center (the recipe keeps
    the line end farther from the tip than the center), then a trustworthy final
    segment, then the vector from the line end to the declared apex.
    """
    coords = rel["coords"]
    if len(coords) < 2:
        return None, "no-polyline"
    last, prev = coords[-1], coords[-2]
    seg = [last[0] - prev[0], last[1] - prev[1]]
    seg_len = math.hypot(seg[0], seg[1])
    center = (arrow or {}).get("center")
    if center is not None:
        centered = [center[0] - last[0], center[1] - last[1]]
        if math.hypot(centered[0], centered[1]) >= 1.5:
            return unit(centered), "center-minus-line-end"
    if seg_len >= DEGENERATE_SEGMENT_TOL:
        return unit(seg), "final-segment"
    apex = rendered_apex(center, (arrow or {}).get("symbolRotate"), (arrow or {}).get("h")) if arrow else None
    if apex is not None:
        vec = [apex[0] - last[0], apex[1] - last[1]]
        if math.hypot(vec[0], vec[1]) >= 1e-6:
            return unit(vec), "line-end-to-declared-apex"
    return unit(seg), "degenerate"


def nearest_point_on_polyline(point, coords):
    best = None
    best_dist = float("inf")
    for a, b in zip(coords, coords[1:]):
        candidate = closest_point_on_segment(point, a, b)
        dist = math.hypot(point[0] - candidate[0], point[1] - candidate[1])
        if dist < best_dist:
            best_dist = dist
            best = candidate
    return best, best_dist


def closest_point_on_segment(point, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length_sq = dx * dx + dy * dy
    if length_sq < 1e-12:
        return [a[0], a[1]]
    t = ((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / length_sq
    t = max(0.0, min(1.0, t))
    return [a[0] + t * dx, a[1] + t * dy]


def point_polyline_distance(point, coords):
    return nearest_point_on_polyline(point, coords)[1]


def rect_relation(point, rect, tolerance=BORDER_TOL):
    """Classify a point against an axis-aligned rect."""
    x1, y1, x2, y2 = rect
    inside = x1 - tolerance <= point[0] <= x2 + tolerance and y1 - tolerance <= point[1] <= y2 + tolerance
    border = min(abs(point[0] - x1), abs(point[0] - x2), abs(point[1] - y1), abs(point[1] - y2))
    ox = max(x1 - point[0], 0.0, point[0] - x2)
    oy = max(y1 - point[1], 0.0, point[1] - y2)
    outside = math.hypot(ox, oy)
    return {
        "inside": inside,
        "border": round(border, 3),
        "outside": round(outside, 3),
        "onBorder": (inside and border <= tolerance) or (not inside and outside <= tolerance),
    }


def segment_rect_hit(p1, p2, rect, pad=1.0):
    x1, y1, x2, y2 = rect[0] + pad, rect[1] + pad, rect[2] - pad, rect[3] - pad
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, p1[0] - x1), (dx, x2 - p1[0]), (-dy, p1[1] - y1), (dy, y2 - p1[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return False
        else:
            r = q / p
            if p < 0:
                if r > t1:
                    return False
                if r > t0:
                    t0 = r
            else:
                if r < t0:
                    return False
                if r < t1:
                    t1 = r
    return t0 <= t1 and not (t0 == 0.0 and t1 == 0.0)


def segment_intersection(p1, p2, p3, p4):
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    d1 = orient(p3, p4, p1)
    d2 = orient(p3, p4, p2)
    d3 = orient(p1, p2, p3)
    d4 = orient(p1, p2, p4)
    eps = 1e-9
    if ((d1 > eps and d2 < -eps) or (d1 < -eps and d2 > eps)) and ((d3 > eps and d4 < -eps) or (d3 < -eps and d4 > eps)):
        denominator = (p4[1] - p3[1]) * (p2[0] - p1[0]) - (p4[0] - p3[0]) * (p2[1] - p1[1])
        if abs(denominator) < 1e-12:
            return None
        ua = ((p4[0] - p3[0]) * (p1[1] - p3[1]) - (p4[1] - p3[1]) * (p1[0] - p3[0])) / denominator
        return {"point": [p1[0] + ua * (p2[0] - p1[0]), p1[1] + ua * (p2[1] - p1[1])]}
    if abs(d1) < eps and abs(d2) < eps:
        use_x = abs(p2[0] - p1[0]) >= abs(p2[1] - p1[1])
        a = sorted((p1[0], p2[0])) if use_x else sorted((p1[1], p2[1]))
        b = sorted((p3[0], p4[0])) if use_x else sorted((p3[1], p4[1]))
        lo, hi = max(a[0], b[0]), min(a[1], b[1])
        if hi - lo > 1.0:
            return {"collinear": hi - lo}
    return None
