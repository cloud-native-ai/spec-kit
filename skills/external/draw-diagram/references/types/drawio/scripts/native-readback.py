#!/usr/bin/env python3
"""native-readback.py - independent readback of a produced draw.io native file.

Reads the ACTUAL native mxGraph cells of one produced .drawio file (ids, labels,
parents, edge sources/targets, style identity, geometry) and compares them with the
caller-supplied authoritative semantics. With --svg it additionally reads the
ACTUAL rendered SVG: calibrated vertex rects, zone outline paths, edge body paths,
edge label text/background geometry, extra cell groups, and measures crossings,
shared route segments and label/border crossings from those rendered paths.

Nothing here copies the expected semantics into the extracted records: records come
from the files, expectations are used only for comparison.

Usage:
  native-readback.py --source FILE.drawio --semantics FILE.json \
                     [--svg FILE.svg] --output NEW-report.json

Exit codes:
  0  pass (semantic pass; visual checks performed and clean when --svg is given)
  1  hard discrepancy found (semantic difference or hard visual/geometry issue)
     or a partial result - partial is not a pass
  2  usage, argument, output-refusal or input I/O error
  3  unsupported native/SVG structure (explicitly reported, never fabricated)

Limitations are always listed in the report; a clean verdict covers only the checks
this file actually performed.
"""
import argparse
import hashlib
import itertools
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import unicodedata

VERSION = "1.0.0"
MAX_BYTES = 50 * 1024 * 1024
EPS = 1e-6
LABEL_FONT_SIZE = 16
LABEL_TOLERANCE = 5.0
ENDPOINT_TOLERANCE = 0.75
ARROW_TOLERANCE = 4.0
BODY_END_TOLERANCE = 12.0
CALIBRATION_TOLERANCE = 1.1
COLLINEAR_EPS = 0.5


class ReadbackError(ValueError):
    pass


class Unsupported(ReadbackError):
    pass


def require(condition, message):
    if not condition:
        raise ReadbackError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def local(tag):
    return tag.split("}")[-1]


def text(value):
    require(isinstance(value, str), "expected a string")
    return value


def number(value):
    require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value), "expected a finite number")
    return float(value)


def xml_number(value, label):
    try:
        return float(value)
    except (TypeError, ValueError, OverflowError):
        raise Unsupported("non-numeric " + label + ": " + repr(value))


def read_text(path, label):
    require(path.is_file(), label + " does not exist: " + str(path))
    data = path.read_bytes()
    require(0 < len(data) <= MAX_BYTES, label + " is empty or exceeds the size cap")
    try:
        return data, data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Unsupported(label + " is not UTF-8 text") from exc


def parse_style(value):
    result = {}
    for item in (value or "").split(";"):
        if not item:
            continue
        if "=" not in item:
            result.setdefault("_tokens", []).append(item)
            continue
        key, item_value = item.split("=", 1)
        result[key] = item_value
    return result


def fraction(value):
    number_value = xml_number(value, "style fraction")
    require(0 <= number_value <= 1, "style fraction outside [0,1]")
    return number_value


# ---------------------------------------------------------------- native parse

def unsupported(condition, message):
    if not condition:
        raise Unsupported(message)


def parse_native(path):
    data, raw = read_text(path, "--source")
    unsupported(not re.search(r"<!DOCTYPE|<!ENTITY|<!--", raw, re.I), "unsupported native DTD/entity/comment")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise Unsupported("native XML does not parse: " + str(exc)) from exc
    unsupported(root.tag == "mxfile", "unsupported native root: " + local(root.tag))
    unsupported(root.get("compressed", "false").lower() != "true", "compressed mxfile is unsupported; the engine emits uncompressed XML")
    diagrams = [child for child in root if child.tag == "diagram"]
    unsupported(len(diagrams) == 1, "expected exactly one diagram")
    graph = diagrams[0].find("mxGraphModel")
    unsupported(graph is not None, "diagram carries no mxGraphModel")
    roots = [child for child in graph if child.tag == "root"]
    unsupported(len(roots) == 1, "expected exactly one root")
    cells = {}
    order = []
    for cell in roots[0]:
        unsupported(cell.tag == "mxCell", "unsupported root child: " + local(cell.tag))
        ident = cell.get("id")
        unsupported(ident is not None and ident not in cells, "invalid or duplicate cell id")
        cells[ident] = cell
        order.append(ident)
    unsupported("0" in cells and "1" in cells, "missing structural root cells 0/1")
    records = {}
    for ident in order:
        cell = cells[ident]
        if ident in ("0", "1"):
            continue
        parent = cell.get("parent")
        unsupported(parent in cells, "cell parent is missing or unknown: " + ident)
        vertex = cell.get("vertex") == "1"
        edge = cell.get("edge") == "1"
        unsupported(vertex != edge, "cell must be exactly one of vertex/edge: " + ident)
        style = parse_style(cell.get("style", ""))
        geometry = cell.find("mxGeometry")
        unsupported(geometry is not None, "cell carries no mxGeometry: " + ident)
        record = {
            "id": ident,
            "kind": "edge" if edge else ("zone" if style.get("container") == "1" or style.get("shape") == "swimlane" else "element"),
            "label": cell.get("value", ""),
            "parent": parent,
            "style": {key: style[key] for key in ("strokeColor", "fillColor", "startSize", "exitX", "exitY", "entryX", "entryY") if key in style},
        }
        if edge:
            record["source"] = cell.get("source")
            record["target"] = cell.get("target")
            points = []
            arrays = geometry.findall("Array")
            require(len(arrays) <= 1, "edge has more than one waypoint array: " + ident)
            if arrays:
                require(arrays[0].get("as") == "points", "edge array is not the points array: " + ident)
                for point in arrays[0]:
                    require(point.tag == "mxPoint" and point.get("x") is not None and point.get("y") is not None, "invalid waypoint: " + ident)
                    points.append((xml_number(point.get("x"), "waypoint x"), xml_number(point.get("y"), "waypoint y")))
            record["waypoints_relative"] = points
            label = {"x": None, "offset": (0.0, 0.0)}
            if geometry.get("x") is not None:
                label["x"] = xml_number(geometry.get("x"), "label x")
            for point in geometry.findall("mxPoint"):
                if point.get("as") == "offset":
                    label["offset"] = (xml_number(point.get("x"), "label offset x"), xml_number(point.get("y"), "label offset y"))
            record["label_geometry"] = label
        else:
            missing = [key for key in ("x", "y", "width", "height") if geometry.get(key) is None]
            require(not missing, "vertex geometry missing " + ",".join(missing) + ": " + ident)
            record["box_relative"] = tuple(xml_number(geometry.get(key), "vertex " + key) for key in ("x", "y", "width", "height"))
        records[ident] = record
    boxes = {}

    def absolute(ident):
        if ident in boxes:
            return boxes[ident]
        record = records[ident]
        require("box_relative" in record, "edge used as geometry parent: " + ident)
        x, y, width, height = record["box_relative"]
        require(width > 0 and height > 0, "non-positive vertex size: " + ident)
        parent = records[ident]["parent"]
        if parent == "1":
            offset = (0.0, 0.0)
        else:
            require(parent in records, "unknown geometry parent: " + ident)
            offset = absolute(parent)[:2]
        boxes[ident] = (x + offset[0], y + offset[1], x + offset[0] + width, y + offset[1] + height)
        return boxes[ident]

    for ident, record in records.items():
        if record["kind"] != "edge":
            record["box"] = list(absolute(ident))
    parents = {}
    for ident, record in records.items():
        if record["kind"] != "edge":
            parents[ident] = record["parent"]

    def ancestors(ident):
        result = []
        seen = {ident}
        current = ident
        while current != "1":
            require(current in parents, "missing parent chain for " + ident)
            current = parents[current]
            require(current not in seen, "cyclic parent chain: " + ident)
            result.append(current)
            seen.add(current)
        return result

    return {"path": str(path), "sha256": digest(data), "bytes": len(data), "cells": records, "order": order, "parents": parents, "ancestors": ancestors}


# ------------------------------------------------------------- geometry helpers

def axis(a, b):
    if abs(a[1] - b[1]) <= EPS and abs(a[0] - b[0]) > EPS:
        return 1
    if abs(a[0] - b[0]) <= EPS and abs(a[1] - b[1]) > EPS:
        return 2
    return 0


def inside(point, rect):
    return rect[0] + EPS < point[0] < rect[2] - EPS and rect[1] + EPS < point[1] < rect[3] - EPS


def hits(a, b, rect):
    if inside(a, rect) or inside(b, rect):
        return True
    if axis(a, b) == 1:
        return rect[1] + EPS < a[1] < rect[3] - EPS and min(max(a[0], b[0]), rect[2]) > max(min(a[0], b[0]), rect[0]) + EPS
    if axis(a, b) == 2:
        return rect[0] + EPS < a[0] < rect[2] - EPS and min(max(a[1], b[1]), rect[3]) > max(min(a[1], b[1]), rect[1]) + EPS
    return False


def endpoint_of(record, boxes, role):
    style = record["style"]
    box = boxes.get(role)
    if box is None:
        return None
    x_key, y_key = ("exitX", "exitY") if role == record["source"] else ("entryX", "entryY")
    if x_key not in style or y_key not in style:
        return None
    fx, fy = fraction(style[x_key]), fraction(style[y_key])
    return box[0] + (box[2] - box[0]) * fx, box[1] + (box[3] - box[1]) * fy


def route_of(record, boxes):
    start = endpoint_of(record, boxes, record["source"])
    end = endpoint_of(record, boxes, record["target"])
    return start, end


def interaction(a, b, c, d, spacing):
    first, second = axis(a, b), axis(c, d)
    if not first or not second:
        return 0, 0.0, 0.0
    if first == second:
        varying, fixed = (0, 1) if first == 1 else (1, 0)
        length = max(0.0, min(max(a[varying], b[varying]), max(c[varying], d[varying])) - max(min(a[varying], b[varying]), min(c[varying], d[varying])))
        separation = abs(a[fixed] - c[fixed])
        return 0, length if separation < EPS else 0.0, length if EPS <= separation < spacing - EPS else 0.0
    if first == 2:
        a, b, c, d = c, d, a, b
    crossing = min(a[0], b[0]) - EPS <= c[0] <= max(a[0], b[0]) + EPS and min(c[1], d[1]) - EPS <= a[1] <= max(c[1], d[1]) + EPS
    return int(crossing), 0.0, 0.0


def polyline_metrics(routes):
    crossings = 0
    collinear = 0.0
    near = 0.0
    shared = []
    for first, second in itertools.combinations(sorted(routes), 2):
        first_ends, second_ends = routes[first], routes[second]
        if not first_ends or not second_ends:
            continue
        first_terminals = {first_ends[0], first_ends[-1]}
        second_terminals = {second_ends[0], second_ends[-1]}
        if first_terminals & second_terminals:
            continue
        pair_crossings = 0
        pair_collinear = 0.0
        pair_near = 0.0
        for a, b in zip(first_ends, first_ends[1:]):
            for c, d in zip(second_ends, second_ends[1:]):
                crossing, overlap, parallel = interaction(a, b, c, d, 10)
                pair_crossings += crossing
                pair_collinear += overlap
                pair_near += parallel
        crossings += pair_crossings
        collinear += pair_collinear
        near += pair_near
        if pair_collinear > COLLINEAR_EPS:
            shared.append({"ids": [first, second], "length": round(pair_collinear, 2)})
    return {"crossings": crossings, "collinear_length": round(collinear, 2), "near_parallel_length": round(near, 2), "shared_segments": shared}


# ---------------------------------------------------------------- SVG parsing

def parse_svg(path):
    data, raw = read_text(path, "--svg")
    raw = raw.replace('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">', "", 1)
    unsupported(not re.search(r"<!DOCTYPE|<!ENTITY", raw, re.I), "unsupported SVG DTD or entity")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise Unsupported("SVG does not parse: " + str(exc)) from exc
    unsupported(local(root.tag) == "svg", "expected an SVG root")
    return {"path": str(path), "sha256": digest(data), "root": root}


def compose(outer, inner):
    return (outer[0] * inner[0], outer[1] * inner[1], outer[0] * inner[2] + outer[2], outer[1] * inner[3] + outer[3])


def svg_transform(element, parents, unsupported):
    result = (1.0, 1.0, 0.0, 0.0)
    while element is not None:
        css = dict(item.split(":", 1) for item in element.get("style", "").split(";") if ":" in item)
        for key, value in css.items():
            if key.strip() == "transform" and value.strip() not in ("", "none"):
                unsupported.add("css-transform")
        raw = element.get("transform", "")
        local_transform = (1.0, 1.0, 0.0, 0.0)
        for name, values in re.findall(r"([A-Za-z]+)\s*\(([^)]*)\)", raw):
            values = [float(item) for item in re.split(r"[\s,]+", values.strip()) if item]
            require(all(math.isfinite(item) for item in values), "non-finite SVG transform")
            if name == "translate" and len(values) in (1, 2):
                operation = (1.0, 1.0, values[0], values[1] if len(values) == 2 else 0.0)
            elif name == "scale" and len(values) in (1, 2):
                operation = (values[0], values[-1], 0.0, 0.0)
            elif name == "matrix" and len(values) == 6 and abs(values[1]) < EPS and abs(values[2]) < EPS:
                operation = (values[0], values[3], values[4], values[5])
            else:
                unsupported.add("svg-transform:" + name)
                return None
            require(operation[0] > 0 and operation[1] > 0, "reflected SVG transform unsupported")
            local_transform = compose(local_transform, operation)
        require(not re.sub(r"[A-Za-z]+\s*\([^)]*\)", "", raw).strip(" ,\n\t"), "invalid SVG transform syntax")
        result = compose(local_transform, result)
        element = parents.get(element)
    return result


PATH_TOKEN = re.compile(r"([MmLlHhVvZzCcSsQqAaTt])|(-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)")


def parse_path(d):
    tokens = []
    for command, value in PATH_TOKEN.findall(d or ""):
        tokens.append(command if command else float(value))
    points = []
    unsupported = set()
    current = (0.0, 0.0)
    start = None
    closed = False
    index = 0
    mode = None
    while index < len(tokens):
        token = tokens[index]
        if isinstance(token, str):
            mode = token
            index += 1
            if mode in "Zz":
                closed = True
                if points:
                    points.append(points[-1])
                continue
        if mode is None:
            raise Unsupported("SVG path data without a command")
        if mode in "Mm":
            x, y = tokens[index], tokens[index + 1]
            index += 2
            current = (x, y) if mode == "M" else (current[0] + x, current[1] + y)
            points.append(current)
            start = current
            mode = "L" if mode == "M" else "l"
        elif mode in "Ll":
            x, y = tokens[index], tokens[index + 1]
            index += 2
            current = (x, y) if mode == "L" else (current[0] + x, current[1] + y)
            points.append(current)
        elif mode in "Hh":
            x = tokens[index]
            index += 1
            current = (x if mode == "H" else current[0] + x, current[1])
            points.append(current)
        elif mode in "Vv":
            y = tokens[index]
            index += 1
            current = (current[0], y if mode == "V" else current[1] + y)
            points.append(current)
        elif mode in "CcSsQqAaTt":
            counts = {"C": 6, "S": 4, "Q": 4, "A": 7, "T": 2}
            count = counts[mode.upper()]
            values = tokens[index:index + count]
            if len(values) != count or any(isinstance(value, str) for value in values):
                raise Unsupported("truncated or interleaved SVG curve command")
            index += count
            unsupported.add(mode.upper())
            if mode.isupper():
                current = (values[-2], values[-1])
            else:
                current = (current[0] + values[-2], current[1] + values[-1])
        else:
            raise Unsupported("unsupported SVG path command: " + str(mode))
    return {"points": points, "unsupported": unsupported, "closed": closed, "start": start}


def rect_of(element, parents, unsupported):
    transform = svg_transform(element, parents, unsupported)
    if transform is None:
        return None
    x = xml_number(element.get("x", "0"), "rect x")
    y = xml_number(element.get("y", "0"), "rect y")
    width = xml_number(element.get("width", "0"), "rect width")
    height = xml_number(element.get("height", "0"), "rect height")
    return (transform[0] * x + transform[2], transform[1] * y + transform[3], transform[0] * (x + width) + transform[2], transform[1] * (y + height) + transform[3])


def group_index(root):
    parents = {child: parent for parent in root.iter() for child in parent}
    groups = {}

    def nearest(element):
        current = element
        while current is not None:
            ident = current.get("data-cell-id")
            if ident is not None:
                return ident
            current = parents.get(current)
        return None

    for element in root.iter():
        ident = element.get("data-cell-id")
        if ident is not None:
            groups.setdefault(ident, element)
    return parents, groups, nearest


def svg_text(element):
    return "".join(element.itertext()).strip()


def collect_svg(payload, expected_ids, unsupported):
    root = payload["root"]
    parents, groups, nearest = group_index(root)
    group_texts = {}
    group_rects = {}
    group_paths = {}
    extras = []
    for element in root.iter():
        tag = local(element.tag)
        if tag == "text":
            owner = nearest(element)
            group_texts.setdefault(owner, []).append(svg_text(element))
        elif tag == "rect":
            owner = nearest(element)
            group_rects.setdefault(owner, []).append(element)
        elif tag == "path":
            owner = nearest(element)
            group_paths.setdefault(owner, []).append(element)
    for ident in groups:
        if ident not in expected_ids and ident not in ("0", "1"):
            extras.append({"id": ident, "texts": group_texts.get(ident, [])})
    return {
        "parents": parents,
        "groups": groups,
        "texts": group_texts,
        "rects": group_rects,
        "paths": group_paths,
        "extras": extras,
        "unsupported": unsupported,
    }


def calibration(native, svg, unsupported):
    maps = []
    for ident, record in native["cells"].items():
        if record["kind"] == "edge":
            continue
        rects = svg["rects"].get(ident) or []
        if not rects or "box" not in record:
            continue
        rect = rect_of(rects[0], svg["parents"], unsupported)
        if rect is None:
            continue
        box = record["box"]
        if (rect[2] - rect[0]) <= EPS or (rect[3] - rect[1]) <= EPS:
            continue
        sx = (rect[2] - rect[0]) / (box[2] - box[0])
        sy = (rect[3] - rect[1]) / (box[3] - box[1])
        maps.append((sx, sy, rect[0] - sx * box[0], rect[1] - sy * box[1]))
    if len(maps) < 3:
        return None, len(maps)
    sx, sy, tx, ty = maps[0]
    require(abs(sx - sy) < 0.01 and sx > 0, "non-uniform or non-positive SVG canvas scale")
    for other in maps:
        require(abs(other[0] - sx) < 0.01 and abs(other[1] - sy) < 0.01, "inconsistent SVG scales")
        require(abs(other[2] - tx) <= CALIBRATION_TOLERANCE and abs(other[3] - ty) <= CALIBRATION_TOLERANCE, "inconsistent SVG canvas offset")
    return (sx, sy, tx, ty), len(maps)


def to_native(point, mapping):
    sx, sy, tx, ty = mapping
    return ((point[0] - tx) / sx, (point[1] - ty) / sy)


# ------------------------------------------------------------------- semantics

def load_semantics(path):
    data, raw = read_text(path, "--semantics")
    try:
        semantics = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ReadbackError("semantics JSON does not parse: " + str(exc)) from exc
    require(isinstance(semantics, dict), "semantics must be an object")
    for key in ("elements", "zones", "relations"):
        require(isinstance(semantics.get(key), list), "semantics missing array: " + key)
    elements, zones, relations = {}, {}, {}
    for row in semantics["elements"]:
        require(isinstance(row, dict) and isinstance(row.get("id"), str) and isinstance(row.get("label"), str) and isinstance(row.get("zone"), str), "invalid semantics element")
        require(row["id"] not in elements, "duplicate semantics element id")
        elements[row["id"]] = {"label": row["label"], "parent": row["zone"]}
    for row in semantics["zones"]:
        require(isinstance(row, dict) and isinstance(row.get("id"), str) and isinstance(row.get("label"), str), "invalid semantics zone")
        require(row["id"] not in zones, "duplicate semantics zone id")
        parent = row.get("parent")
        require(parent is None or isinstance(parent, str), "invalid semantics zone parent")
        zones[row["id"]] = {"label": row["label"], "parent": parent or "1"}
    for row in semantics["relations"]:
        require(isinstance(row, dict) and isinstance(row.get("id"), str) and isinstance(row.get("from"), str) and isinstance(row.get("to"), str), "invalid semantics relation")
        require(row["id"] not in relations, "duplicate semantics relation id")
        relations[row["id"]] = {"from": row["from"], "to": row["to"], "label": row.get("label", ""), "color": row.get("color")}
    return {"path": str(path), "sha256": digest(data), "elements": elements, "zones": zones, "relations": relations}


def semantic_compare(native, semantics):
    differences = []
    expected = {**{key: "element" for key in semantics["elements"]}, **{key: "zone" for key in semantics["zones"]}, **{key: "edge" for key in semantics["relations"]}}
    actual = {ident: (record["kind"]) for ident, record in native["cells"].items()}
    extras = []
    for ident in sorted(actual):
        if ident not in expected:
            record = native["cells"][ident]
            extras.append({"id": ident, "kind": record["kind"], "label": record["label"], "style": record["style"]})
            differences.append({"code": "extra_" + record["kind"], "id": ident, "label": record["label"]})
            if record["label"]:
                differences.append({"code": "extra_cell_text", "id": ident, "label": record["label"]})
    for ident in sorted(expected):
        if ident not in actual:
            differences.append({"code": "missing", "id": ident, "expected_kind": expected[ident]})
            continue
        if actual[ident] != expected[ident]:
            differences.append({"code": "kind_changed", "id": ident, "expected": expected[ident], "actual": actual[ident]})
            continue
        record = native["cells"][ident]
        if ident in semantics["elements"]:
            wanted = semantics["elements"][ident]
            if record["parent"] != wanted["parent"]:
                differences.append({"code": "element_zone_changed", "id": ident, "expected": wanted["parent"], "actual": record["parent"]})
            if record["label"] != wanted["label"]:
                differences.append({"code": "label_changed", "id": ident, "expected": wanted["label"], "actual": record["label"]})
        elif ident in semantics["zones"]:
            wanted = semantics["zones"][ident]
            if record["parent"] != wanted["parent"]:
                differences.append({"code": "zone_parent_changed", "id": ident, "expected": wanted["parent"], "actual": record["parent"]})
            if record["label"] != wanted["label"]:
                differences.append({"code": "label_changed", "id": ident, "expected": wanted["label"], "actual": record["label"]})
        else:
            wanted = semantics["relations"][ident]
            if record["source"] != wanted["from"] or record["target"] != wanted["to"]:
                differences.append({"code": "endpoints_changed", "id": ident, "expected": [wanted["from"], wanted["to"]], "actual": [record["source"], record["target"]]})
            if record["label"] != wanted["label"]:
                differences.append({"code": "label_changed", "id": ident, "expected": wanted["label"], "actual": record["label"]})
            color = wanted.get("color")
            if color and str(record["style"].get("strokeColor", "")).lower() != color.lower():
                differences.append({"code": "color_changed", "id": ident, "expected": color, "actual": record["style"].get("strokeColor")})
        for endpoint in ("source", "target"):
            if record["kind"] == "edge" and record[endpoint] not in native["cells"]:
                differences.append({"code": "dangling_endpoint", "id": ident, "endpoint": endpoint})
    return {"status": "fail" if differences else "pass", "differences": differences, "extra_cells": extras}


def native_geometry(native, spacing=10):
    cells = native["cells"]
    boxes = {ident: tuple(record["box"]) for ident, record in cells.items() if record["kind"] != "edge"}
    routes = {}
    issues = []
    limitations = []
    for ident, record in sorted(cells.items()):
        if record["kind"] != "edge":
            continue
        if record["source"] not in boxes or record["target"] not in boxes:
            limitations.append("edge " + ident + ": endpoint is not a native vertex; native route not resolved")
            continue
        start, end = route_of(record, boxes)
        if start is None or end is None:
            limitations.append("edge " + ident + ": exit/entry style missing; endpoint checks skipped")
            continue
        parent = record["parent"]
        offset = (0.0, 0.0)
        if parent != "1" and parent in boxes:
            offset = boxes[parent][:2]
        waypoints = [(x + offset[0], y + offset[1]) for x, y in record["waypoints_relative"]]
        route = [start] + waypoints + [end]
        routes[ident] = route
        for index, (a, b) in enumerate(zip(route, route[1:])):
            if not axis(a, b):
                issues.append({"code": "non_orthogonal_segment", "id": ident, "segment": index})
        source_zone_chain = set(native["ancestors"](record["source"])) if record["source"] in native["parents"] else set()
        target_zone_chain = set(native["ancestors"](record["target"])) if record["target"] in native["parents"] else set()
        allowed = {record["source"], record["target"]} | source_zone_chain | target_zone_chain
        for other, record_other in cells.items():
            if other in allowed or record_other["kind"] == "edge" or "box" not in record_other:
                continue
            rect = tuple(record_other["box"])
            for index, (a, b) in enumerate(zip(route, route[1:])):
                if hits(a, b, rect):
                    issues.append({"code": "edge_through_node", "id": ident, "obstacle": other, "segment": index})
        for zone, record_zone in cells.items():
            if record_zone["kind"] != "zone" or zone not in allowed:
                continue
            start_size = record_zone["style"].get("startSize")
            if start_size is None:
                limitations.append("zone " + zone + ": startSize missing; header band not checked")
                continue
            header = (record_zone["box"][0], record_zone["box"][1], record_zone["box"][2], record_zone["box"][1] + float(start_size))
            for index, (a, b) in enumerate(zip(route, route[1:])):
                if hits(a, b, header):
                    issues.append({"code": "edge_through_zone_title", "id": ident, "obstacle": zone, "segment": index})
    metrics = polyline_metrics(routes)
    return {"status": "fail" if issues else "pass", "issues": issues, "limitations": limitations, "metrics": metrics,
            "metrics_method": "native routes from exit/entry style fractions + waypoints; crossings = per segment-pair orthogonal intersection count between relations with disjoint endpoint sets (no location de-duplication); collinear = exact same-line overlap length; near_parallel = parallel separation below 10px"}


# ------------------------------------------------------------------ visual SVG

def transformed_points(element, points, parents, unsupported):
    transform = svg_transform(element, parents, unsupported)
    if transform is None:
        return None
    return [(transform[0] * x + transform[2], transform[1] * y + transform[3]) for x, y in points]


def zone_outlines(native, svg, mapping, unsupported):
    outlines = {}
    limitations = []
    for ident, record in native["cells"].items():
        if record["kind"] != "zone":
            continue
        paths = svg["paths"].get(ident) or []
        if not paths:
            limitations.append("zone " + ident + ": no rendered outline path")
            continue
        points = []
        for element in paths:
            parsed = parse_path(element.get("d"))
            unsupported.update("path:" + item for item in parsed["unsupported"])
            transformed = transformed_points(element, parsed["points"], svg["parents"], unsupported)
            if transformed is None:
                limitations.append("zone " + ident + ": outline uses an unsupported transform")
                points = []
                break
            points.extend(transformed)
        if len(points) < 2:
            limitations.append("zone " + ident + ": outline path has no stable points")
            continue
        mapped = [to_native(point, mapping) for point in points]
        xs = [point[0] for point in mapped]
        ys = [point[1] for point in mapped]
        outlines[ident] = (min(xs), min(ys), max(xs), max(ys))
    return outlines, limitations


def crosses_border(rect, zone):
    x, y, r, b = rect
    zx, zy, zr, zb = zone
    if y < zb - EPS and b > zy + EPS and ((x < zx - EPS and r > zx + EPS) or (x < zr - EPS and r > zr + EPS)):
        return True
    if x < zr - EPS and r > zx + EPS and ((y < zy - EPS and b > zy + EPS) or (y < zb - EPS and b > zb + EPS)):
        return True
    return False


def point_on_polyline(point, polyline, tolerance):
    for a, b in zip(polyline, polyline[1:]):
        if axis(a, b) == 1:
            if min(a[0], b[0]) - tolerance <= point[0] <= max(a[0], b[0]) + tolerance and abs(point[1] - a[1]) <= tolerance:
                return True
        elif axis(a, b) == 2:
            if min(a[1], b[1]) - tolerance <= point[1] <= max(a[1], b[1]) + tolerance and abs(point[0] - a[0]) <= tolerance:
                return True
        elif abs(point[0] - a[0]) <= tolerance and abs(point[1] - a[1]) <= tolerance:
            return True
    return False


def svg_visual(native, semantics, svg_payload):
    unsupported = set()
    svg = collect_svg(svg_payload, set(native["cells"]), unsupported)
    mapping, calibration_points = calibration(native, svg, unsupported)
    limitations = []
    issues = []
    if mapping is None:
        return {"status": "partial", "checks": {"calibration_points": calibration_points}, "issues": [], "metrics": {},
                "limitations": ["fewer than three native vertex rects available for calibration; rendered geometry not evaluated"]}
    checks = {"calibration_points": calibration_points, "edges_checked": 0, "labels_checked": 0}
    boxes = {ident: tuple(record["box"]) for ident, record in native["cells"].items() if record["kind"] != "edge"}
    outlines, outline_limitations = zone_outlines(native, svg, mapping, unsupported)
    limitations.extend(outline_limitations)
    for ident, record in native["cells"].items():
        if record["kind"] != "zone":
            continue
        if ident in outlines and ident in boxes:
            outline, box = outlines[ident], boxes[ident]
            if max(abs(a - b) for a, b in zip(outline, box)) > 2.0:
                issues.append({"code": "zone_outline_mismatch", "id": ident, "rendered": [round(v, 2) for v in outline], "native": [round(v, 2) for v in box]})
    rendered_routes = {}
    for ident, record in sorted(native["cells"].items()):
        if record["kind"] != "edge":
            continue
        native_start, native_end = route_of(record, boxes)
        if native_start is None or native_end is None:
            limitations.append("edge " + ident + ": native endpoint unresolved; rendered path not compared")
            continue
        paths = svg["paths"].get(ident) or []
        bodies = [element for element in paths if (element.get("fill") or "").lower() == "none"]
        arrows = [element for element in paths if (element.get("fill") or "").lower() not in ("", "none")]
        if not bodies:
            issues.append({"code": "edge_path_missing", "id": ident})
            continue
        parsed = parse_path(bodies[0].get("d"))
        unsupported.update("path:" + item for item in parsed["unsupported"])
        if len(parsed["points"]) < 2:
            issues.append({"code": "edge_path_unreadable", "id": ident})
            continue
        transformed = transformed_points(bodies[0], parsed["points"], svg["parents"], unsupported)
        if transformed is None:
            limitations.append("edge " + ident + ": body path uses an unsupported transform")
            continue
        points = [to_native(point, mapping) for point in transformed]
        rendered_routes[ident] = points
        checks["edges_checked"] += 1
        native_route = [native_start] + [(x + (boxes[record["parent"]][0] if record["parent"] != "1" and record["parent"] in boxes else 0.0), y + (boxes[record["parent"]][1] if record["parent"] != "1" and record["parent"] in boxes else 0.0)) for x, y in record["waypoints_relative"]] + [native_end]
        off_native = [point for point in points if not point_on_polyline(point, native_route, 2.0)]
        if off_native:
            issues.append({"code": "rendered_path_off_native", "id": ident, "points": [[round(v, 2) for v in point] for point in off_native[:5]]})
        if abs(points[0][0] - native_start[0]) > 2.0 or abs(points[0][1] - native_start[1]) > 2.0:
            issues.append({"code": "edge_rendered_start_off", "id": ident, "rendered": [round(v, 2) for v in points[0]], "native": [round(v, 2) for v in native_start]})
        if max(abs(points[-1][0] - native_end[0]), abs(points[-1][1] - native_end[1])) > BODY_END_TOLERANCE:
            issues.append({"code": "edge_rendered_end_off", "id": ident, "rendered": [round(v, 2) for v in points[-1]], "native": [round(v, 2) for v in native_end]})
        if arrows:
            arrow = parse_path(arrows[0].get("d"))
            unsupported.update("path:" + item for item in arrow["unsupported"])
            transformed_arrow = transformed_points(arrows[0], arrow["points"], svg["parents"], unsupported)
            if transformed_arrow is not None and len(transformed_arrow) >= 3:
                tips = [to_native(point, mapping) for point in transformed_arrow]
                gaps = [math.hypot(tip[0] - native_end[0], tip[1] - native_end[1]) for tip in tips]
                nearest = min(range(len(tips)), key=lambda index: gaps[index])
                if gaps[nearest] > ARROW_TOLERANCE:
                    issues.append({"code": "arrow_tip_off_target", "id": ident, "gap": round(gaps[nearest], 2)})
                else:
                    tip = tips[nearest]
                    target_box = boxes.get(record["target"])
                    if target_box is not None:
                        outside = not inside(tip, target_box)
                        near_border = min(abs(tip[0] - target_box[0]), abs(tip[0] - target_box[2]), abs(tip[1] - target_box[1]), abs(tip[1] - target_box[3])) <= ARROW_TOLERANCE
                        if not (outside and near_border):
                            issues.append({"code": "arrow_not_at_target_border", "id": ident, "tip": [round(v, 2) for v in tip]})
        label_value = record["label"]
        if not label_value:
            continue
        rendered_text = svg["texts"].get(ident) or []
        if "\n".join(rendered_text) != label_value:
            issues.append({"code": "label_text_changed", "id": ident, "rendered": rendered_text, "native": label_value})
            continue
        rects = svg["rects"].get(ident) or []
        backgrounds = [element for element in rects if (element.get("fill") or "").lower() in ("#ffffff", "#fff", "white")]
        if len(backgrounds) != 1:
            issues.append({"code": "label_background_missing", "id": ident, "count": len(backgrounds)})
            continue
        bounds = rect_of(backgrounds[0], svg["parents"], unsupported)
        if bounds is None:
            limitations.append("edge " + ident + ": label background uses an unsupported transform")
            continue
        native_bounds = [to_native(point, mapping) for point in ((bounds[0], bounds[1]), (bounds[2], bounds[3]))]
        rect = (native_bounds[0][0], native_bounds[0][1], native_bounds[1][0], native_bounds[1][1])
        checks["labels_checked"] += 1
        for zone, outline in sorted(outlines.items()):
            if crosses_border(rect, outline):
                issues.append({"code": "label_crosses_zone_border", "id": ident, "zone": zone})
        for other, other_box in sorted(boxes.items()):
            if other in (record["source"], record["target"]) or native["cells"][other]["kind"] != "element":
                continue
            if min(rect[2], other_box[2]) > max(rect[0], other_box[0]) + 2 and min(rect[3], other_box[3]) > max(rect[1], other_box[1]) + 2:
                issues.append({"code": "label_overlaps_node", "id": ident, "node": other})
        native_center = native_label_center(record, boxes)
        if native_center is None:
            limitations.append("edge " + ident + ": native label geometry missing")
        else:
            center = ((rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2)
            gap = math.hypot(center[0] - native_center[0], center[1] - native_center[1])
            checks.setdefault("label_center_deltas", {})[ident] = round(gap, 2)
            if gap > LABEL_TOLERANCE:
                issues.append({"code": "rendered_label_geometry_off", "id": ident, "gap": round(gap, 2)})
        font_sizes = []
        for element in (svg["groups"][ident].iter() if ident in svg["groups"] else []):
            if local(element.tag) == "g" and element.get("font-size"):
                font_sizes.append(element.get("font-size"))
        if font_sizes and all(abs(float(size[:-2] if size.endswith("px") else size) - LABEL_FONT_SIZE) > 0.5 for size in font_sizes):
            issues.append({"code": "label_font_size_changed", "id": ident, "sizes": font_sizes})
    for extra in svg["extras"]:
        issues.append({"code": "extra_svg_cell", "id": extra["id"], "texts": extra["texts"]})
        if extra["texts"]:
            issues.append({"code": "extra_svg_legend_text", "id": extra["id"], "texts": extra["texts"]})
    metrics = polyline_metrics(rendered_routes)
    if unsupported:
        limitations.append("unsupported SVG syntax present (spans excluded from geometry): " + ",".join(sorted(unsupported)))
    if not rendered_routes and any(record["kind"] == "edge" for record in native["cells"].values()):
        issues.append({"code": "no_readable_rendered_edges"})
    status = "fail" if issues else "pass"
    return {"status": status, "checks": checks, "issues": issues, "limitations": limitations, "metrics": metrics,
            "metrics_method": "rendered body paths mapped to native coordinates; crossings = per segment-pair orthogonal intersection count between relations with disjoint endpoint sets (no location de-duplication); collinear = exact same-line overlap length; curve spans (jump arcs) excluded"}


def native_label_center(record, boxes):
    label = record.get("label_geometry") or {}
    if label.get("x") is None:
        return None
    start, end = route_of(record, boxes)
    if start is None or end is None:
        return None
    parent = record["parent"]
    offset = (0.0, 0.0)
    if parent != "1" and parent in boxes:
        offset = boxes[parent][:2]
    route = [start] + [(x + offset[0], y + offset[1]) for x, y in record["waypoints_relative"]] + [end]
    total = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(route, route[1:]))
    if total <= EPS:
        return None
    remaining = (label["x"] + 1) * total / 2
    anchor = None
    for a, b in zip(route, route[1:]):
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        if remaining <= length + EPS or a is route[-2]:
            t = min(1.0, max(0.0, remaining / length)) if length > EPS else 0.0
            anchor = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
            break
        remaining -= length
    if anchor is None:
        return None
    return (anchor[0] + label["offset"][0], anchor[1] + label["offset"][1])


# ------------------------------------------------------------------------ main

def readback(source, semantics, svg_path):
    native = parse_native(source)
    semantics_data = load_semantics(semantics)
    report = {
        "engine": "drawio",
        "interface": "native-readback/1",
        "generator": "native-readback.py " + VERSION,
        "source": {"path": str(source), "sha256": native["sha256"], "bytes": native["bytes"], "format": "mxfile (uncompressed)"},
        "semantics": {"path": semantics_data["path"], "sha256": semantics_data["sha256"]},
        "svg": None,
        "counts": {
            "native": {
                "elements": sum(1 for record in native["cells"].values() if record["kind"] == "element"),
                "zones": sum(1 for record in native["cells"].values() if record["kind"] == "zone"),
                "relations": sum(1 for record in native["cells"].values() if record["kind"] == "edge"),
            },
            "semantics": {
                "elements": len(semantics_data["elements"]),
                "zones": len(semantics_data["zones"]),
                "relations": len(semantics_data["relations"]),
            },
        },
        "actual": [native["cells"][ident] for ident in native["order"] if ident in native["cells"]],
        "records": [native["cells"][ident] for ident in native["order"] if ident in native["cells"]],
        "semantic": semantic_compare(native, semantics_data),
        "geometry_native": None,
        "visual": {"status": "not_performed", "reason": "no --svg supplied"},
        "unsupported": [],
        "not_evaluated": ["interaction: not exercised by readback", "font_metrics: not measured (declared character estimate only)", "user_satisfaction: not_evaluated"],
        "limitations": [],
        "overall": "fail",
        "exit_code": 1,
    }
    geometry = native_geometry(native)
    report["geometry_native"] = {"status": geometry["status"], "issues": geometry["issues"], "limitations": geometry["limitations"], "metrics": geometry["metrics"]}
    report["limitations"].extend(geometry["limitations"])
    if svg_path is not None:
        svg_payload = parse_svg(svg_path)
        report["svg"] = {"path": str(svg_path), "sha256": svg_payload["sha256"]}
        visual = svg_visual(native, semantics_data, svg_payload)
        report["visual"] = visual
        report["limitations"].extend(visual["limitations"])
    statuses = [report["semantic"]["status"], geometry["status"]]
    if svg_path is not None:
        statuses.append(report["visual"]["status"])
    if "fail" in statuses:
        report["overall"] = "fail"
    elif "partial" in statuses:
        report["overall"] = "partial"
    else:
        report["overall"] = "pass"
    report["exit_code"] = 0 if report["overall"] == "pass" else 1
    if svg_path is None:
        report["not_evaluated"].append("visual: no --svg supplied; visual axis is not_performed")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Independent readback of a produced .drawio native file, optionally checked against its rendered SVG. "
        "Compares actual extracted cells and rendered geometry with the authoritative semantics; never copies expectations into records. "
        "Exit 0 pass, 1 hard discrepancy or partial, 2 usage/I-O, 3 unsupported structure.",
        allow_abbrev=False,
    )
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--source", type=Path, required=True, help="produced native .drawio file")
    parser.add_argument("--semantics", type=Path, required=True, help="authoritative semantics JSON")
    parser.add_argument("--svg", type=Path, default=None, help="actual rendered SVG to check")
    parser.add_argument("--output", type=Path, required=True, help="new report file; an existing file is refused")
    args = parser.parse_args(argv)
    try:
        require(args.output.parent.is_dir(), "output parent does not exist: " + str(args.output.parent))
        require(not args.output.exists() and not args.output.is_symlink(), "refusing to overwrite: " + str(args.output))
        inputs = [args.source, args.semantics] + ([args.svg] if args.svg is not None else [])
        resolved = [path.resolve() for path in inputs + [args.output]]
        require(len(set(resolved)) == len(resolved), "input/output paths must be distinct")
        report = readback(args.source, args.semantics, args.svg)
    except Unsupported as exc:
        report = {"engine": "drawio", "interface": "native-readback/1", "overall": "unsupported", "error": str(exc), "exit_code": 3}
        _write(args.output, report)
        print(json.dumps({"status": "unsupported", "error": str(exc), "report": str(args.output)}, ensure_ascii=False))
        return 3
    except (ReadbackError, OSError, ValueError, ET.ParseError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    _write(args.output, report)
    print(json.dumps({"status": report["overall"], "report": str(args.output), "differences": len(report["semantic"]["differences"]), "visual": report["visual"]["status"]}, ensure_ascii=False))
    return report["exit_code"]


def _write(path, report):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")


if __name__ == "__main__":
    sys.exit(main())
