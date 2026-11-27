#!/usr/bin/env python3
"""native-readback.py - independent readback of a PlantUML .puml (and optional SVG).

Extracts ACTUAL records from the native source and from the actual rendered SVG,
then compares them with the authoritative semantic input. It never copies the
expected input into the extracted records: expectations are used only for diffing.

Interface (shared draw-diagram engine readback contract):
  native-readback.py --source <native-file> --semantics <authoritative-json>
                     [--svg <rendered-svg>] --output <new-report>

Legend authorization:
  A legend is legitimate only when the semantic input authorizes its content.
  Accepted authorization shapes (top-level keys of the semantics JSON):
    "legend":        [{"color": "#rrggbb", "text": "..."} | "text", ...]
    "legend_items":  same as "legend" (alias)
    "legend_authorized": true  with  "legend_text": "..." | ["...", ...]
  Without authorization, any source legend is reported as invented semantics
  (hard discrepancy) and any visible SVG legend text not derived from the source
  legend is reported separately.

Exit codes:
  0  all checked axes clean (pass)
  1  a hard semantic/visual discrepancy was found
  2  usage or I/O error (including refusing to overwrite the output)
  3  report written, but the result is partial/unsupported (never a pass)

Only the files given on the command line are read; no credentials, config
roots or network access are used.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

VERSION = "1.0.0"
SVG_NS = "{http://www.w3.org/2000/svg}"
LONG_EDGE_UNITS = 1500.0
CROSSING_DEDUPE_UNITS = 3.0
ENDPOINT_DETACH_UNITS = 20.0
LABEL_ON_LINE_UNITS = 2.0

GROUP_KEYWORDS = {
    "package", "rectangle", "frame", "folder", "node", "cloud", "together",
    "storage", "artifact", "component", "database", "queue", "interface",
    "actor", "usecase", "class", "entity", "collections",
}
LEAF_KEYWORDS = {
    "component", "database", "queue", "artifact", "interface", "actor",
    "usecase", "class", "entity", "storage", "collections", "rectangle",
    "node", "cloud", "frame", "folder",
}
SKIP_BLOCK_STARTS = ("skinparam", "style", "note", "legend", "header", "footer", "title", "caption")
DECL_RE = re.compile(
    r"^\s*(?P<kw>" + "|".join(sorted(GROUP_KEYWORDS | LEAF_KEYWORDS, key=len, reverse=True)) + r")\s+(?P<rest>.*)$"
)
QUOTED_LABEL_RE = re.compile(r'^\s*"(?P<label>[^"]*)"(?P<rest>.*)$')
ALIAS_RE = re.compile(r"\bas\s+(?P<alias>[A-Za-z_][\w.]*)\b")
STEREO_RE = re.compile(r"<<\s*(?P<st>[^>]*?)\s*>>")
HEX_COLOR_RE = re.compile(r"#([0-9A-Fa-f]{6})\b")
COLOR_ATTR_RE = re.compile(r"(?:stroke|fill)(?::|=\")(#[0-9A-Fa-f]{6})")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "")).strip()


def strip_markup(value: str) -> str:
    out = re.sub(r"<[^>]*>", "", value or "")
    return norm_text(html.unescape(out))


def norm_color(value):
    if not value:
        return None
    match = re.fullmatch(r"#?([0-9A-Fa-f]{6})", str(value).strip())
    return "#" + match.group(1).lower() if match else str(value).strip().lower()


# ---------------------------------------------------------------------------
# PlantUML source parsing
# ---------------------------------------------------------------------------

def parse_arrow(line: str):
    """Split a relation line into (left, arrow, right, label). Returns None if not a relation."""
    # A label starts at the first ':' that is followed by text and not inside [].
    bracket_depth = 0
    label_at = None
    for idx, ch in enumerate(line):
        if ch == "[":
            bracket_depth += 1
        elif ch == "]":
            bracket_depth = max(0, bracket_depth - 1)
        elif ch == ":" and bracket_depth == 0:
            label_at = idx
            break
    body = line if label_at is None else line[:label_at]
    label = None if label_at is None else norm_text(line[label_at + 1:])
    if label is not None and len(label) >= 2 and label[0] == label[-1] == '"':
        label = label[1:-1]
    tokens = body.split()
    if len(tokens) < 3:
        return None
    for i in range(1, len(tokens) - 1):
        tok = tokens[i]
        if re.fullmatch(r"[A-Za-z_][\w.]*", tok):
            continue
        if not re.fullmatch(r"[<>.\-\[\]A-Za-z0-9_#=,]+", tok):
            continue
        if not any(ch in tok for ch in "<>-."):
            continue
        if not (("-" in tok or "." in tok) and (">" in tok or "<" in tok
                                                or tok.count("-") >= 2 or "[" in tok)):
            continue
        return tokens[i - 1], tok, " ".join(tokens[i + 1:]), label, tokens
    return None


def arrow_details(arrow: str):
    bracket = ""
    match = re.search(r"\[([^\]]*)\]", arrow)
    if match:
        bracket = match.group(1)
    hidden = "hidden" in bracket.lower()
    direction = None
    for candidate in ("up", "down", "left", "right"):
        if candidate in arrow.lower():
            direction = candidate
            break
    color = None
    color_match = HEX_COLOR_RE.search(bracket) or HEX_COLOR_RE.search(arrow)
    if color_match:
        color = "#" + color_match.group(1).lower()
    named = re.search(r"#([A-Za-z][A-Za-z0-9]*)", bracket)
    if color is None and named:
        color = "#" + named.group(1).lower()  # named color: kept for reporting
    thickness = None
    thickness_match = re.search(r"thickness\s*=\s*([0-9.]+)", bracket)
    if thickness_match:
        thickness = float(thickness_match.group(1))
    reversed_arrow = arrow.startswith("<") and not arrow.endswith(">")
    dashed = ".." in arrow or "--" in arrow.replace("-", "", 1)
    return {
        "raw": arrow,
        "hidden": hidden,
        "direction": direction,
        "color": color,
        "thickness": thickness,
        "reversed": reversed_arrow,
        "dashed": dashed,
    }


def parse_puml(text: str):
    lines = text.splitlines()
    groups = []
    elements = []
    relations = []
    hidden = []
    unsupported = []
    legend = {"present": False, "start_line": None, "rows": [], "raw_text": ""}
    stack = []  # items: {"kind": "group", record} or {"kind": "skip"}
    in_legend = False
    legend_lines = []
    legend_start = None
    start_tag = None
    end_tag = None
    skip_until = None  # for <style>, skinparam { }, note blocks

    for lineno, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        stripped = line.strip()
        if skip_until:
            if skip_until == "style" and re.search(r"</style\s*>", stripped, re.I):
                skip_until = None
            elif skip_until == "skinparam" and stripped == "}":
                skip_until = None
            elif skip_until == "note" and re.match(r"^end\s*note\b", stripped, re.I):
                skip_until = None
            continue
        if in_legend:
            if re.match(r"^end\s*legend\b", stripped, re.I):
                in_legend = False
                legend["present"] = True
                legend["start_line"] = legend_start
                legend["raw_text"] = "\n".join(legend_lines)
                for row in legend_lines:
                    cells = [c.strip() for c in row.split("|")]
                    plain = []
                    colors = []
                    for cell in cells:
                        cell_plain = strip_markup(re.sub(r"<back:#[0-9A-Fa-f]{6}>", "", cell))
                        if cell_plain:
                            plain.append(cell_plain)
                        colors.extend("#" + c.lower() for c in HEX_COLOR_RE.findall(cell))
                    text_plain = norm_text(" | ".join(plain))
                    if text_plain or colors:
                        legend["rows"].append({"text": text_plain, "colors": sorted(set(colors)), "raw": row.strip()})
                legend_lines = []
            else:
                legend_lines.append(line)
            continue

        if stripped.startswith("@start"):
            if start_tag is None:
                start_tag = stripped
                if not re.match(r"^@startuml\b", stripped):
                    unsupported.append({"line": lineno, "kind": "unsupported_diagram_type",
                                        "detail": stripped})
            continue
        if stripped.startswith("@end"):
            end_tag = stripped
            continue
        if not stripped or stripped.startswith("'"):
            continue
        if stripped.startswith("/*") and stripped.endswith("*/"):
            continue
        if re.match(r"^<style\b", stripped, re.I):
            if not re.search(r"</style\s*>", stripped, re.I):
                skip_until = "style"
            continue
        if re.match(r"^skinparam\b", stripped, re.I):
            if stripped.endswith("{"):
                skip_until = "skinparam"
            continue
        if re.match(r"^!(define|include|pragma|theme|procedure|function|end)\b", stripped):
            continue
        if re.match(r"^(hide|show|remove|scale|title|caption|header|footer|page|newpage)\b", stripped, re.I):
            continue
        if re.match(r"^together\s*\{", stripped, re.I):
            stack.append({"kind": "skip"})
            continue
        if stripped == "}":
            if stack:
                stack.pop()
            continue
        if re.match(r"^legend\b", stripped, re.I):
            in_legend = True
            legend_start = lineno
            legend["present"] = True
            continue
        if re.match(r"^note\b", stripped, re.I):
            if not re.search(r"\bend\s*note\b", stripped, re.I):
                skip_until = "note"
            continue

        decl = DECL_RE.match(line)
        if decl:
            kw = decl.group("kw")
            rest = decl.group("rest")
            label_match = QUOTED_LABEL_RE.match(rest)
            label = label_match.group("label") if label_match else None
            remainder = label_match.group("rest") if label_match else rest
            alias_match = ALIAS_RE.search(remainder)
            alias = alias_match.group("alias") if alias_match else None
            stereotypes = [norm_text(s) for s in STEREO_RE.findall(remainder)]
            is_block = "{" in remainder
            if label is None:
                # label is the leading bare token, if any
                bare = remainder.strip().split()
                if bare and bare[0] not in ("as",):
                    label = bare[0]
            if alias is None and label is not None and not is_block:
                alias = label  # PlantUML derives identity from the label; flagged later
                inferred = True
            else:
                inferred = alias is None
            record = {
                "id": alias,
                "label": label,
                "parent": next((item["record"]["id"] for item in reversed(stack) if item["kind"] == "group"), None),
                "keyword": kw,
                "stereotypes": stereotypes,
                "source_line": lineno,
                "identity_inferred": inferred,
            }
            if is_block:
                stack.append({"kind": "group", "record": record})
                groups.append(record)
            else:
                elements.append(record)
            continue

        relation = parse_arrow(stripped)
        if relation:
            left, arrow, right, label, _tokens = relation
            details = arrow_details(arrow)
            if not re.fullmatch(r"[A-Za-z_][\w.]*", left) or not re.fullmatch(r"[A-Za-z_][\w.]*", right):
                unsupported.append({"line": lineno, "kind": "unsupported_endpoint",
                                    "detail": stripped})
                continue
            if details["hidden"]:
                hidden.append({"from": left, "to": right, "raw": arrow,
                               "direction": details["direction"], "source_line": lineno})
            else:
                relations.append({
                    "index": len(relations) + 1,
                    "from": right if details["reversed"] else left,
                    "to": left if details["reversed"] else right,
                    "label": label,
                    "color": details["color"],
                    "thickness": details["thickness"],
                    "dashed": details["dashed"],
                    "source_line": lineno,
                })
            continue
        # Unknown but non-empty directive: record it rather than silently dropping it.
        if not stripped.startswith(("skinparam", "!theme")):
            unsupported.append({"line": lineno, "kind": "unrecognized_line", "detail": stripped})

    if in_legend:
        unsupported.append({"line": legend_start, "kind": "unterminated_legend",
                            "detail": "legend block has no endlegend"})
        legend["present"] = True
        legend["start_line"] = legend_start
        legend["raw_text"] = "\n".join(legend_lines)
    if start_tag is None:
        unsupported.append({"line": 0, "kind": "missing_start_tag", "detail": "no @start... line"})
    if end_tag is None:
        unsupported.append({"line": 0, "kind": "missing_end_tag", "detail": "no @end... line"})
    return {
        "start_tag": start_tag,
        "end_tag": end_tag,
        "groups": groups,
        "elements": elements,
        "relations": relations,
        "hidden_constraints": hidden,
        "legend": legend,
        "unsupported": unsupported,
    }


# ---------------------------------------------------------------------------
# SVG parsing
# ---------------------------------------------------------------------------

def parse_path_points(d: str):
    """Return (subpaths, limitations) from an SVG path 'd' (absolute/relative MLCQTSHVAZ)."""
    tokens = re.findall(r"[MmLlCcSsQqTtAaZzHhVv]|[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", d or "")
    subpaths = []
    current = []
    x = y = 0.0
    start_x = start_y = 0.0
    cmd = None
    limitations = []
    i = 0

    def take(n):
        nonlocal i
        vals = []
        for _ in range(n):
            if i >= len(tokens):
                return None
            vals.append(float(tokens[i]))
            i += 1
        return vals

    def point(px, py):
        current.append((px, py))

    while i < len(tokens):
        token = tokens[i]
        if re.fullmatch(r"[A-Za-z]", token):
            cmd = token
            i += 1
        if cmd is None:
            i += 1
            continue
        upper = cmd.upper()
        rel = cmd.islower()
        if upper == "Z":
            if current:
                point(start_x, start_y)
                subpaths.append(current)
                current = []
            cmd = None
            continue
        if upper in ("M", "L", "T"):
            vals = take(2)
            if vals is None:
                break
            nx, ny = vals
            if rel:
                nx, ny = x + nx, y + ny
            if upper == "M":
                if current:
                    subpaths.append(current)
                current = []
                start_x, start_y = nx, ny
                point(nx, ny)
                cmd = "l" if rel else "L"
            else:
                point(nx, ny)
            x, y = nx, ny
            continue
        if upper == "H":
            vals = take(1)
            if vals is None:
                break
            nx = x + vals[0] if rel else vals[0]
            point(nx, y)
            x = nx
            continue
        if upper == "V":
            vals = take(1)
            if vals is None:
                break
            ny = y + vals[0] if rel else vals[0]
            point(x, ny)
            y = ny
            continue
        if upper == "C":
            vals = take(6)
            if vals is None:
                break
            c1x, c1y, c2x, c2y, nx, ny = vals
            if rel:
                c1x, c1y, c2x, c2y, nx, ny = x + c1x, y + c1y, x + c2x, y + c2y, x + nx, y + ny
            for step in range(1, 9):
                t = step / 8.0
                mt = 1 - t
                px = mt**3 * x + 3 * mt**2 * t * c1x + 3 * mt * t**2 * c2x + t**3 * nx
                py = mt**3 * y + 3 * mt**2 * t * c1y + 3 * mt * t**2 * c2y + t**3 * ny
                point(px, py)
            x, y = nx, ny
            continue
        if upper == "S":
            vals = take(4)
            if vals is None:
                break
            limitations.append("smooth_cubic_control_reflection_approximated")
            c2x, c2y, nx, ny = vals
            if rel:
                c2x, c2y, nx, ny = x + c2x, y + c2y, x + nx, y + ny
            point(nx, ny)
            x, y = nx, ny
            continue
        if upper == "Q":
            vals = take(4)
            if vals is None:
                break
            cx, cy, nx, ny = vals
            if rel:
                cx, cy, nx, ny = x + cx, y + cy, x + nx, y + ny
            for step in range(1, 9):
                t = step / 8.0
                mt = 1 - t
                px = mt**2 * x + 2 * mt * t * cx + t**2 * nx
                py = mt**2 * y + 2 * mt * t * cy + t**2 * ny
                point(px, py)
            x, y = nx, ny
            continue
        if upper == "A":
            vals = take(7)
            if vals is None:
                break
            limitations.append("arc_geometry_endpoint_only")
            rx, ry, _rot, _large, _sweep, nx, ny = vals
            if rel:
                nx, ny = x + nx, y + ny
            point(nx, ny)
            x, y = nx, ny
            continue
        i += 1
    if current:
        subpaths.append(current)
    return subpaths, sorted(set(limitations))


def own_text_elements(node):
    """Text elements belonging to this group, not to nested entity/cluster groups."""
    def walk(current):
        for child in list(current):
            tag = child.tag.split("}")[-1]
            if tag == "g":
                continue
            if tag == "text":
                yield child
            yield from walk(child)
    return list(walk(node))


def node_texts(node):
    return [html.unescape("".join(el.itertext())) for el in own_text_elements(node)]


def text_boxes(node):
    boxes = []
    for el in own_text_elements(node):
        content = norm_text(html.unescape("".join(el.itertext())))
        if not content:
            continue
        try:
            x = float(el.get("x", 0))
            y = float(el.get("y", 0))
        except ValueError:
            continue
        try:
            length = float(el.get("textLength", 0))
        except ValueError:
            length = 0.0
        try:
            size = float(el.get("font-size", 0))
        except ValueError:
            size = 0.0
        boxes.append({
            "text": content, "x": x, "y": y,
            "w": length, "h": size or 0.0,
            # SVG text y is the baseline; approximate the glyph box above it.
            "box": [x, y - (size or 0.0), x + (length or 0.0), y],
        })
    return boxes


def shape_bbox(node):
    xs = []
    ys = []
    for child in node.iter():
        tag = child.tag.split("}")[-1]
        if tag == "rect":
            try:
                x = float(child.get("x", 0))
                y = float(child.get("y", 0))
                w = float(child.get("width", 0))
                h = float(child.get("height", 0))
            except ValueError:
                continue
            if w > 0 and h > 0:
                xs.extend([x, x + w])
                ys.extend([y, y + h])
        elif tag == "path":
            subs, _limits = parse_path_points(child.get("d", ""))
            for sub in subs:
                for px, py in sub:
                    xs.append(px)
                    ys.append(py)
        elif tag == "polygon":
            nums = [float(v) for v in re.findall(r"[-+]?\d*\.?\d+", child.get("points", ""))]
            xs.extend(nums[0::2])
            ys.extend(nums[1::2])
        elif tag == "ellipse":
            try:
                cx = float(child.get("cx", 0))
                cy = float(child.get("cy", 0))
                rx = float(child.get("rx", 0))
                ry = float(child.get("ry", 0))
            except ValueError:
                continue
            xs.extend([cx - rx, cx + rx])
            ys.extend([cy - ry, cy + ry])
        elif tag == "line":
            try:
                xs.extend([float(child.get("x1", 0)), float(child.get("x2", 0))])
                ys.extend([float(child.get("y1", 0)), float(child.get("y2", 0))])
            except ValueError:
                pass
    if not xs or not ys:
        return None
    return [min(xs), min(ys), max(xs), max(ys)]


def parse_svg(text: str):
    limitations = []
    if re.search(r"<!DOCTYPE|<!ENTITY", text, re.I):
        raise ValueError("SVG declares a DTD/entity: refusing to parse it (no entity expansion)")
    root = ET.fromstring(text)
    viewbox = None
    if root.get("viewBox"):
        parts = [float(v) for v in root.get("viewBox").replace(",", " ").split()]
        if len(parts) == 4:
            viewbox = parts
    entities = {}
    clusters = {}
    links = []
    legend_texts = []
    id_to_qualified = {}

    def walk(node, in_legend=False):
        tag = node.tag.split("}")[-1]
        klass = node.get("class", "")
        current_legend = in_legend or "legend" in klass.split()
        if tag == "g" and current_legend:
            legend_texts.extend(norm_text(t) for t in node_texts(node))
            return
        if tag == "g" and "cluster" in klass.split():
            qualified = node.get("data-qualified-name")
            if qualified:
                texts = [norm_text(t) for t in node_texts(node) if norm_text(t)]
                bbox = shape_bbox(node)
                clusters[qualified] = {
                    "id": node.get("id"), "qualified_name": qualified,
                    "label": texts[0] if texts else None,
                    "texts": texts, "bbox": bbox,
                    "stroke_width": extract_stroke_width(node),
                }
                if node.get("id"):
                    id_to_qualified[node.get("id")] = qualified
        elif tag == "g" and "entity" in klass.split():
            qualified = node.get("data-qualified-name")
            if qualified:
                texts = [norm_text(t) for t in node_texts(node) if norm_text(t)]
                bbox = shape_bbox(node)
                entities[qualified] = {
                    "id": node.get("id"), "qualified_name": qualified,
                    "label": norm_text(" ".join(texts)) or None,
                    "texts": texts, "bbox": bbox,
                    "stroke_width": extract_stroke_width(node),
                }
                if node.get("id"):
                    id_to_qualified[node.get("id")] = qualified
        elif tag == "g" and "link" in klass.split():
            paths = [c for c in node.iter() if c.tag.split("}")[-1] == "path"]
            polygons = [c for c in node.iter() if c.tag.split("}")[-1] == "polygon"]
            path_groups = []
            for path in paths:
                subs, limits = parse_path_points(path.get("d", ""))
                limitations.extend(limits)
                for sub in subs:
                    if sub:
                        path_groups.append(sub)
            points = [pt for group in path_groups for pt in group]
            stroke = None
            stroke_width = None
            for path in paths:
                style = path.get("style", "") + " " + path.get("stroke", "")
                stroke_match = re.search(r"stroke:\s*(#[0-9A-Fa-f]{6})", style)
                width_match = re.search(r"stroke-width:\s*([0-9.]+)", style)
                if stroke_match and stroke is None:
                    stroke = norm_color(stroke_match.group(1))
                if width_match and stroke_width is None:
                    stroke_width = float(width_match.group(1))
            label = norm_text(" ".join(node_texts(node))) or None
            polygon_points = []
            for polygon in polygons:
                nums = [float(v) for v in re.findall(r"[-+]?\d*\.?\d+", polygon.get("points", ""))]
                polygon_points.extend(zip(nums[0::2], nums[1::2]))
            links.append({
                "id": node.get("id"),
                "from_ent": node.get("data-entity-1"),
                "to_ent": node.get("data-entity-2"),
                "link_type": node.get("data-link-type"),
                "source_line": node.get("data-source-line"),
                "stroke": stroke,
                "stroke_width": stroke_width,
                "label": label,
                "label_boxes": text_boxes(node),
                "points": points,
                "path_groups": path_groups,
                "subpath_count": len(path_groups),
                "polygon_points": polygon_points,
            })
            return
        for child in list(node):
            walk(child, current_legend)

    walk(root)
    return {
        "root_tag": root.tag,
        "viewbox": viewbox,
        "entities": entities,
        "clusters": clusters,
        "links": links,
        "legend_texts": sorted(set(t for t in legend_texts if t)),
        "id_to_qualified": id_to_qualified,
        "limitations": sorted(set(limitations)),
    }


def extract_stroke_width(node):
    widths = set()
    for child in node.iter():
        style = child.get("style", "")
        match = re.search(r"stroke-width:\s*([0-9.]+)", style)
        if match:
            widths.add(float(match.group(1)))
    return sorted(widths)


# ---------------------------------------------------------------------------
# Comparison helpers
# ---------------------------------------------------------------------------

def point_segment_distance(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == dy == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


def polyline_length(points):
    return sum(math.hypot(points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1])
               for i in range(len(points) - 1))


def segments(points):
    return [(points[i], points[i + 1]) for i in range(len(points) - 1)
            if points[i] != points[i + 1]]


def segment_intersection(a, b, c, d):
    """Return intersection point or None (proper crossing only)."""
    (x1, y1), (x2, y2) = a, b
    (x3, y3), (x4, y4) = c, d
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-9:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom
    if 0 < t < 1 and 0 < u < 1:
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None


def segment_rect_intersection(a, b, rect):
    x0, y0, x1, y1 = rect
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    # Liang-Barsky clipping
    dx, dy = b[0] - a[0], b[1] - a[1]
    p = [-dx, dx, -dy, dy]
    q = [a[0] - x0, x1 - a[0], a[1] - y0, y1 - a[1]]
    u1, u2 = 0.0, 1.0
    for pi, qi in zip(p, q):
        if abs(pi) < 1e-12:
            if qi < 0:
                return False
        else:
            t = qi / pi
            if pi < 0:
                u1 = max(u1, t)
            else:
                u2 = min(u2, t)
    return u1 < u2


def point_rect_distance(pt, rect):
    if not rect:
        return None
    x0, y0, x1, y1 = rect
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    dx = max(x0 - pt[0], 0.0, pt[0] - x1)
    dy = max(y0 - pt[1], 0.0, pt[1] - y1)
    return math.hypot(dx, dy)


def dedupe_points(points, tolerance=CROSSING_DEDUPE_UNITS):
    unique = []
    for point in points:
        if all(math.hypot(point[0] - p[0], point[1] - p[1]) > tolerance for p in unique):
            unique.append(point)
    return unique


def zone_chain(zone_id, zone_parent):
    chain = []
    seen = set()
    while zone_id and zone_id not in seen:
        chain.append(zone_id)
        seen.add(zone_id)
        zone_id = zone_parent.get(zone_id)
    return list(reversed(chain))


def expected_qualified(obj_id, zone, zone_parent):
    chain = zone_chain(zone, zone_parent)
    return ".".join(chain + [obj_id]) if chain else obj_id


def source_qualified(record, group_by_id):
    chain = []
    seen = set()
    cur = record
    while cur is not None and cur.get("id") and cur.get("id") not in seen:
        seen.add(cur.get("id"))
        chain.append(cur.get("id"))
        parent_id = cur.get("parent")
        cur = group_by_id.get(parent_id) if parent_id else None
    return ".".join(reversed(chain))


def normalize_authorized_legend(semantics):
    entries = semantics.get("legend")
    if entries is None:
        entries = semantics.get("legend_items")
    authorized = []
    if isinstance(entries, list):
        for item in entries:
            if isinstance(item, str):
                authorized.append({"color": None, "text": norm_text(item)})
            elif isinstance(item, dict):
                authorized.append({
                    "color": norm_color(item.get("color")),
                    "text": norm_text(item.get("text") or item.get("label") or ""),
                })
    if semantics.get("legend_authorized") is True:
        text = semantics.get("legend_text")
        items = text if isinstance(text, list) else ([text] if text else [])
        for item in items:
            if isinstance(item, str) and norm_text(item):
                authorized.append({"color": None, "text": norm_text(item)})
    return {
        "authorized": bool(authorized) or semantics.get("legend_authorized") is True,
        "items": authorized,
    }


def legend_authorization_findings(source_legend, svg_legend_texts, semantics):
    findings = []
    authorization = normalize_authorized_legend(semantics)
    rows = source_legend.get("rows", [])
    svg_has_legend = bool(svg_legend_texts)
    if not authorization["authorized"]:
        if rows:
            offending = [row["raw"] for row in rows]
            findings.append({
                "code": "unauthorized_legend_meaning",
                "severity": "hard",
                "detail": "the semantic input authorizes no legend, but the source defines one; "
                          "legend rows may assign business meanings the input never declared",
                "offending_rows": offending,
                "colors": sorted({c for row in rows for c in row["colors"]}),
            })
        if svg_has_legend:
            findings.append({
                "code": "unauthorized_visible_legend",
                "severity": "hard",
                "detail": "the actual SVG shows legend text although the semantic input authorizes no legend",
                "visible_texts": svg_legend_texts,
            })
        return findings, authorization

    authorized_texts = [item["text"] for item in authorization["items"] if item["text"]]
    authorized_colors = {item["color"] for item in authorization["items"] if item["color"]}
    for row in rows:
        row_text = row["text"]
        text_ok = any(a and (a in row_text or row_text in a) for a in authorized_texts) if authorized_texts else True
        color_ok = True
        for color in row["colors"]:
            if authorized_colors and color not in authorized_colors:
                color_ok = False
        if not text_ok or not color_ok:
            findings.append({
                "code": "legend_row_not_authorized",
                "severity": "hard",
                "detail": "a legend row does not match any input-authorized legend item",
                "offending_row": row["raw"],
                "colors": row["colors"],
            })
    joined = norm_text(" ".join(r["text"] for r in rows))
    for text in svg_legend_texts:
        if not text:
            continue
        if text in joined:
            continue
        if any(text in a or a in text for a in authorized_texts):
            continue
        findings.append({
            "code": "visible_legend_text_extra",
            "severity": "hard",
            "detail": "the actual SVG legend shows text that neither the source legend nor the "
                      "input authorization contains",
            "offending_text": text,
        })
    if rows and authorized_texts:
        present = norm_text(" ".join(r["text"] for r in rows))
        for item in authorization["items"]:
            if item["text"] and item["text"] not in present:
                findings.append({
                    "code": "legend_row_missing",
                    "severity": "partial",
                    "detail": "an input-authorized legend item is absent from the source legend",
                    "missing_text": item["text"],
                })
    return findings, authorization


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def analyze(source_path: Path, semantics_path: Path, svg_path: Path | None, output_path: Path):
    semantics = json.loads(semantics_path.read_text(encoding="utf-8"))
    for key in ("zones", "elements", "relations"):
        if not isinstance(semantics.get(key), list):
            raise ValueError(f"semantics JSON must contain a '{key}' array")
    source_text = source_path.read_text(encoding="utf-8")
    source = parse_puml(source_text)
    svg = parse_svg(svg_path.read_text(encoding="utf-8")) if svg_path else None

    blocking = [item for item in source["unsupported"]
                if item["kind"] in ("unsupported_diagram_type", "missing_start_tag")]
    if blocking:
        return {
            "schema": "plantuml-native-readback/1",
            "tool": {"name": "native-readback.py", "version": VERSION},
            "engine": "plantuml",
            "inputs": {
                "source": {"path": str(source_path), "sha256": sha256_file(source_path)},
                "semantics": {"path": str(semantics_path), "sha256": sha256_file(semantics_path)},
                "svg": {"path": str(svg_path), "sha256": sha256_file(svg_path)} if svg_path else None,
            },
            "records": {
                "source": {
                    "start_tag": source["start_tag"], "end_tag": source["end_tag"],
                    "groups": source["groups"], "elements": source["elements"],
                    "relations": source["relations"],
                    "hidden_constraints": {"count": len(source["hidden_constraints"]),
                                            "items": source["hidden_constraints"]},
                    "legend": source["legend"],
                },
                "svg": None,
            },
            "diff": {},
            "legend": {"authorization": {"authorized": False, "items": []},
                        "source_present": source["legend"]["present"], "visible_present": False},
            "semantic": {"status": "partial", "findings": []},
            "visual": {"status": "not_checked", "findings": []},
            "unsupported": source["unsupported"],
            "not_evaluated": ["semantic_and_visual_comparison_skipped_for_unsupported_diagram_type"],
            "status": "partial",
            "exit_code": 3,
            "limits": ["The source is not a supported PlantUML UML diagram; comparisons were skipped "
                        "rather than reported as graph corruption."],
        }

    zones = semantics.get("zones") or []
    elements = semantics.get("elements") or []
    relations = semantics.get("relations") or []
    zone_parent = {z["id"]: z.get("parent") for z in zones}
    zone_ids = {z["id"] for z in zones}
    element_ids = {e["id"] for e in elements}
    zone_by_id = {z["id"]: z for z in zones}
    element_by_id = {e["id"]: e for e in elements}

    semantic_findings = []
    visual_findings = []
    unsupported = list(source["unsupported"])
    not_evaluated = []

    group_by_id = {g["id"]: g for g in source["groups"] if g.get("id")}
    for record in source["groups"] + source["elements"]:
        if record.get("identity_inferred"):
            unsupported.append({"line": record["source_line"], "kind": "identity_inferred",
                                "detail": "no explicit alias; identity derived from the label"})
        if record.get("id") is None:
            unsupported.append({"line": record["source_line"], "kind": "missing_identity",
                                "detail": "declaration has no alias"})
    source_groups = {}
    source_elements = {}
    for record in source["groups"]:
        if record.get("id"):
            record["qualified_name"] = source_qualified(record, group_by_id)
            source_groups[record["qualified_name"]] = record
    for record in source["elements"]:
        if record.get("id"):
            record["qualified_name"] = source_qualified(record, group_by_id)
            source_elements[record["qualified_name"]] = record

    expected_zones = {}
    for zone in zones:
        expected_zones[expected_qualified(zone["id"], zone.get("parent"), zone_parent)] = zone
    expected_elements = {
        expected_qualified(e["id"], e.get("zone"), zone_parent): e for e in elements
    }

    def diff_maps(expected, actual, kind, label_key):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        for qn in missing:
            semantic_findings.append({
                "code": f"{kind}_missing", "severity": "hard",
                "detail": f"{kind} {expected[qn]['id']} is absent from the native source",
                "id": expected[qn]["id"], "expected_qualified_name": qn,
            })
        for qn in extra:
            semantic_findings.append({
                "code": f"{kind}_extra", "severity": "hard",
                "detail": f"{kind} {actual[qn].get('id')} appears in the native source but not in the input",
                "id": actual[qn].get("id"), "actual_qualified_name": qn,
            })
        label_mismatch = []
        for qn in sorted(set(expected) & set(actual)):
            want = norm_text(expected[qn].get(label_key) or "")
            got = norm_text(actual[qn].get("label") or "")
            if want != got:
                label_mismatch.append({"qualified_name": qn, "expected": want, "actual": got})
                semantic_findings.append({
                    "code": f"{kind}_label_mismatch", "severity": "hard",
                    "detail": f"{kind} label differs at {qn}", "expected": want, "actual": got,
                })
        return missing, extra, label_mismatch

    zone_missing, zone_extra, zone_label_mismatch = diff_maps(expected_zones, source_groups, "zone", "label")
    elem_missing, elem_extra, elem_label_mismatch = diff_maps(expected_elements, source_elements, "element", "label")

    element_label_multiset_expected = Counter(norm_text(e.get("label") or "") for e in elements)
    element_label_multiset_source = Counter(norm_text(r.get("label") or "") for r in source["elements"])
    if element_label_multiset_expected != element_label_multiset_source:
        semantic_findings.append({
            "code": "element_label_multiset_mismatch", "severity": "hard",
            "detail": "the multiset of element labels differs from the input (duplicate labels must be preserved)",
            "missing_labels": dict((element_label_multiset_expected - element_label_multiset_source)),
            "extra_labels": dict((element_label_multiset_source - element_label_multiset_expected)),
        })

    if len(source["relations"]) != len(relations):
        semantic_findings.append({
            "code": "relation_count_mismatch", "severity": "hard",
            "detail": "native relation count differs from the input",
            "expected": len(relations), "actual": len(source["relations"]),
        })
    for index, expected_rel in enumerate(relations):
        if index >= len(source["relations"]):
            break
        actual = source["relations"][index]
        rid = expected_rel.get("id")
        if (actual["from"], actual["to"]) != (expected_rel["from"], expected_rel["to"]):
            semantic_findings.append({
                "code": "relation_endpoint_mismatch", "severity": "hard",
                "detail": f"relation #{index + 1} ({rid}) endpoints differ",
                "expected": [expected_rel["from"], expected_rel["to"]],
                "actual": [actual["from"], actual["to"]],
            })
        want_label = norm_text(expected_rel.get("label") or "")
        got_label = norm_text(actual.get("label") or "")
        if want_label != got_label:
            semantic_findings.append({
                "code": "relation_label_mismatch", "severity": "hard",
                "detail": f"relation #{index + 1} ({rid}) label differs",
                "expected": want_label, "actual": got_label,
            })
        want_color = norm_color(expected_rel.get("color"))
        got_color = norm_color(actual.get("color"))
        if want_color != got_color:
            code = "relation_color_mismatch" if got_color else "relation_color_missing"
            severity = "hard" if got_color else "hard"
            if got_color and not re.fullmatch(r"#[0-9a-f]{6}", got_color):
                code = "relation_color_unverifiable"
                severity = "partial"
            semantic_findings.append({
                "code": code, "severity": severity,
                "detail": f"relation #{index + 1} ({rid}) edge color family differs",
                "expected": want_color, "actual": got_color,
            })
    if len(source["relations"]) > len(relations):
        for actual in source["relations"][len(relations):]:
            semantic_findings.append({
                "code": "relation_extra", "severity": "hard",
                "detail": "a native relation has no counterpart in the input",
                "actual": {"from": actual["from"], "to": actual["to"], "label": actual["label"],
                            "color": actual["color"], "source_line": actual["source_line"]},
            })

    # Duplicate-label identities must not be merged: zone-qualified ids carry the distinction.
    duplicate_expected = {label: count for label, count in element_label_multiset_expected.items() if count > 1}
    duplicate_source = {label: count for label, count in element_label_multiset_source.items() if count > 1}
    duplicate_labels = {
        "expected": duplicate_expected,
        "source": duplicate_source,
        "match": duplicate_expected == duplicate_source,
    }

    legend_findings, legend_authorization = legend_authorization_findings(
        source["legend"], (svg or {}).get("legend_texts") or [], semantics
    )
    for finding in legend_findings:
        if finding["code"] in ("visible_legend_text_extra", "unauthorized_visible_legend"):
            visual_findings.append(finding)
        else:
            semantic_findings.append(finding)

    # SVG must reflect the actual source, not the expectations.
    svg_results = None
    if svg is not None:
        svg_entities = {k: v for k, v in svg["entities"].items()}
        svg_clusters = {k: v for k, v in svg["clusters"].items()}
        source_all = dict(source_groups)
        source_all.update(source_elements)
        svg_all = dict(svg_clusters)
        svg_all.update(svg_entities)
        missing = sorted(set(source_all) - set(svg_all))
        extra = sorted(set(svg_all) - set(source_all))
        for qn in missing:
            visual_findings.append({"code": "svg_entity_missing", "severity": "hard",
                                    "detail": f"{qn} is in the source but not visible in the SVG"})
        for qn in extra:
            visual_findings.append({"code": "svg_entity_extra", "severity": "hard",
                                    "detail": f"{qn} is visible in the SVG but not in the source"})
        svg_label_mismatch = []
        for qn in sorted(set(source_all) & set(svg_all)):
            want = norm_text(source_all[qn].get("label") or "")
            got = norm_text(svg_all[qn].get("label") or "")
            if want != got:
                svg_label_mismatch.append({"qualified_name": qn, "source": want, "svg": got})
                visual_findings.append({"code": "svg_label_mismatch", "severity": "hard",
                                        "detail": f"visible SVG label differs from the actual source at {qn}",
                                        "source": want, "svg": got})

        id_to_qualified = svg["id_to_qualified"]
        matched_links = set()
        link_checks = []
        for rel in source["relations"]:
            # Resolve endpoints through the source id map (aliases are unique across groups/elements).
            from_record = next((r for r in source["groups"] + source["elements"] if r.get("id") == rel["from"]), None)
            to_record = next((r for r in source["groups"] + source["elements"] if r.get("id") == rel["to"]), None)
            from_q = from_record.get("qualified_name") if from_record else None
            to_q = to_record.get("qualified_name") if to_record else None
            candidates = []
            for idx, link in enumerate(svg["links"]):
                if idx in matched_links:
                    continue
                a = id_to_qualified.get(link["from_ent"])
                b = id_to_qualified.get(link["to_ent"])
                if a == from_q and b == to_q:
                    candidates.append((idx, link, "forward"))
                elif a == to_q and b == from_q:
                    candidates.append((idx, link, "reversed"))
            if not candidates:
                visual_findings.append({
                    "code": "svg_link_missing", "severity": "hard",
                    "detail": "a source relation is not visible as an SVG link",
                    "from": from_q, "to": to_q, "label": rel["label"], "color": rel["color"],
                })
                continue
            if len(candidates) > 1:
                labeled = [c for c in candidates if norm_text(c[1].get("label") or "") == norm_text(rel.get("label") or "")]
                candidates = labeled or candidates
            idx, link, direction = candidates[0]
            matched_links.add(idx)
            if direction == "reversed":
                visual_findings.append({
                    "code": "svg_link_direction_reversed", "severity": "hard",
                    "detail": "the SVG arrow points from the declared target to the declared source",
                    "from": from_q, "to": to_q, "link_id": link.get("id"),
                })
            want_color = norm_color(rel.get("color"))
            got_color = norm_color(link.get("stroke"))
            if want_color != got_color:
                visual_findings.append({
                    "code": "svg_link_color_mismatch", "severity": "hard",
                    "detail": "the visible SVG link stroke differs from the source edge color family",
                    "from": from_q, "to": to_q, "expected": want_color, "actual": got_color,
                    "link_id": link.get("id"),
                })
            want_label = norm_text(rel.get("label") or "")
            got_label = norm_text(link.get("label") or "")
            if want_label != got_label:
                visual_findings.append({
                    "code": "svg_link_label_mismatch", "severity": "hard",
                    "detail": "the visible SVG text bound to this link differs from the source relation label",
                    "from": from_q, "to": to_q, "expected": want_label, "actual": got_label,
                    "link_id": link.get("id"),
                })
            link_checks.append({"from": from_q, "to": to_q, "label": want_label,
                                "color": want_color, "link_id": link.get("id")})
        for idx, link in enumerate(svg["links"]):
            if idx not in matched_links:
                visual_findings.append({
                    "code": "svg_link_extra", "severity": "hard",
                    "detail": "an SVG link has no counterpart in the actual source relations",
                    "link_id": link.get("id"),
                    "from_ent": link.get("from_ent"), "to_ent": link.get("to_ent"),
                    "label": link.get("label"), "color": link.get("stroke"),
                })

        # Geometry on the actual SVG.
        def link_segments(link):
            return [seg for group in link["path_groups"] for seg in segments(group)]

        crossings = []
        link_list = list(svg["links"])
        for i in range(len(link_list)):
            for j in range(i + 1, len(link_list)):
                a, b = link_list[i], link_list[j]
                if {a.get("from_ent"), a.get("to_ent")} & {b.get("from_ent"), b.get("to_ent")}:
                    continue
                for seg_a in link_segments(a):
                    for seg_b in link_segments(b):
                        point = segment_intersection(seg_a[0], seg_a[1], seg_b[0], seg_b[1])
                        if point:
                            crossings.append({
                                "link_a": a.get("id"), "link_b": b.get("id"),
                                "pair_a": [id_to_qualified.get(a.get("from_ent")), id_to_qualified.get(a.get("to_ent"))],
                                "pair_b": [id_to_qualified.get(b.get("from_ent")), id_to_qualified.get(b.get("to_ent"))],
                                "point": [round(point[0], 1), round(point[1], 1)],
                            })
        unique_crossings = []
        for crossing in crossings:
            if all(math.hypot(crossing["point"][0] - c["point"][0],
                              crossing["point"][1] - c["point"][1]) > CROSSING_DEDUPE_UNITS
                   for c in unique_crossings):
                unique_crossings.append(crossing)

        boxes = {qn: rec["bbox"] for qn, rec in svg_entities.items() if rec.get("bbox")}
        edge_through_node = []
        for link in link_list:
            src = id_to_qualified.get(link.get("from_ent"))
            dst = id_to_qualified.get(link.get("to_ent"))
            for qn, bbox in boxes.items():
                if qn in (src, dst):
                    continue
                if any(segment_rect_intersection(seg[0], seg[1], bbox) for seg in link_segments(link)):
                    edge_through_node.append({
                        "link_id": link.get("id"), "from": src, "to": dst,
                        "through": qn, "bbox": [round(v, 1) for v in bbox],
                    })

        long_edges = []
        endpoint_rows = []
        label_geometry = []
        for link in link_list:
            for group in link["path_groups"]:
                if len(group) >= 2:
                    length = polyline_length(group)
                    if length > LONG_EDGE_UNITS:
                        long_edges.append({
                            "link_id": link.get("id"),
                            "pair": [id_to_qualified.get(link.get("from_ent")), id_to_qualified.get(link.get("to_ent"))],
                            "length": round(length, 1),
                        })
                        break
            src_q = id_to_qualified.get(link.get("from_ent"))
            dst_q = id_to_qualified.get(link.get("to_ent"))
            src_box = boxes.get(src_q)
            dst_box = boxes.get(dst_q)
            all_points = link["points"]
            if all_points and src_box and dst_box:
                end_gap = point_rect_distance(all_points[-1], dst_box)
                start_gap = point_rect_distance(all_points[0], src_box)
                tip_gap = end_gap
                if link.get("polygon_points"):
                    tip_gap = min(point_rect_distance(p, dst_box) for p in link["polygon_points"])
                endpoint_rows.append({
                    "link_id": link.get("id"), "pair": [src_q, dst_q],
                    "start_gap": round(start_gap, 2) if start_gap is not None else None,
                    "end_gap": round(end_gap, 2) if end_gap is not None else None,
                    "tip_gap": round(tip_gap, 2) if tip_gap is not None else None,
                })
                if tip_gap is not None and tip_gap > ENDPOINT_DETACH_UNITS:
                    visual_findings.append({
                        "code": "svg_endpoint_detached", "severity": "hard",
                        "detail": "an arrow tip is far from the declared target box",
                        "pair": [src_q, dst_q], "tip_gap": round(tip_gap, 2),
                    })
            for box_record in link.get("label_boxes") or []:
                box = box_record["box"]
                own_gap = min((point_segment_distance(
                    (box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0,
                    seg[0][0], seg[0][1], seg[1][0], seg[1][1])
                    for group in link["path_groups"] for seg in segments(group)), default=None)
                overlapped = []
                for qn, entity_box in boxes.items():
                    if qn in (src_q, dst_q):
                        continue
                    if segment_rect_intersection((box[0], box[1]), (box[2], box[3]), entity_box):
                        overlapped.append(qn)
                label_geometry.append({
                    "link_id": link.get("id"), "label": box_record["text"],
                    "own_line_gap": round(own_gap, 2) if own_gap is not None else None,
                    "overlaps": overlapped,
                })
                if overlapped:
                    visual_findings.append({
                        "code": "svg_label_box_overlap", "severity": "partial",
                        "detail": "a relation label box overlaps an unrelated entity box",
                        "link_id": link.get("id"), "label": box_record["text"], "overlaps": overlapped,
                    })
                if own_gap is not None and own_gap < LABEL_ON_LINE_UNITS:
                    visual_findings.append({
                        "code": "svg_label_on_own_line", "severity": "partial",
                        "detail": "a relation label sits on top of its own edge path",
                        "link_id": link.get("id"), "own_line_gap": round(own_gap, 2),
                    })
        sorted_long = sorted(long_edges, key=lambda item: item["length"], reverse=True)
        if unique_crossings:
            visual_findings.append({
                "code": "svg_crossings_present", "severity": "partial",
                "detail": "sampled link polylines cross each other",
                "count": len(unique_crossings),
            })
        if edge_through_node:
            visual_findings.append({
                "code": "svg_edge_through_node", "severity": "partial",
                "detail": "sampled link segments intersect an unrelated entity box",
                "count": len(edge_through_node),
            })
        if sorted_long:
            visual_findings.append({
                "code": "svg_long_edges", "severity": "partial",
                "detail": "some edges exceed the long-edge reporting threshold",
                "count": len(sorted_long), "threshold": LONG_EDGE_UNITS,
            })
        svg_results = {
            "viewbox": svg["viewbox"],
            "aspect": round(svg["viewbox"][2] / svg["viewbox"][3], 3) if svg["viewbox"] and svg["viewbox"][3] else None,
            "counts": {"entities": len(svg_entities), "clusters": len(svg_clusters), "links": len(svg["links"])},
            "entities": {
                qn: {"label": rec.get("label"), "bbox": [round(v, 1) for v in rec["bbox"]] if rec.get("bbox") else None}
                for qn, rec in sorted(svg_entities.items())
            },
            "clusters": {
                qn: {"label": rec.get("label"), "bbox": [round(v, 1) for v in rec["bbox"]] if rec.get("bbox") else None}
                for qn, rec in sorted(svg_clusters.items())
            },
            "missing_entities": missing,
            "extra_entities": extra,
            "label_mismatch": svg_label_mismatch,
            "legend_texts": svg["legend_texts"],
            "link_checks": link_checks,
            "geometry": {
                "method": "SVG path sampled at 8 points per cubic/quadratic segment; "
                          "crossings are proper interior segment intersections with 3-unit dedupe; "
                          "edge-through-node uses Liang-Barsky clipping against actual SVG entity boxes; "
                          "long edges sum sampled polyline length in viewBox units",
                "crossings": unique_crossings,
                "crossing_count": len(unique_crossings),
                "edge_through_node": edge_through_node,
                "edge_through_node_count": len(edge_through_node),
                "long_edges": sorted_long,
                "long_edge_count": len(sorted_long),
                "longest": sorted_long[0] if sorted_long else None,
                "endpoints": endpoint_rows,
                "endpoint_max": {
                    "start_gap": max((r["start_gap"] for r in endpoint_rows if r["start_gap"] is not None), default=None),
                    "end_gap": max((r["end_gap"] for r in endpoint_rows if r["end_gap"] is not None), default=None),
                    "tip_gap": max((r["tip_gap"] for r in endpoint_rows if r["tip_gap"] is not None), default=None),
                },
                "labels": label_geometry,
                "limitations": svg["limitations"] + (
                    ["label_binding_checked_through_link_group_text_only"] if svg["links"] else []
                ) + ["label_boxes_use_textLength_and_approximate_height"],
            },
            "stroke_widths": dict(Counter(
                [f"{w:g}" for rec in list(svg_entities.values()) + list(svg_clusters.values())
                 for w in rec.get("stroke_width") or []]
                + [f"{link['stroke_width']:g}" for link in svg["links"]
                   if link.get("stroke_width") is not None]
            )),
        }
        not_evaluated.append("svg_text_glyph_extents_not_measured")

    if svg is None:
        not_evaluated.append("svg_not_supplied")

    # Status resolution: a hard finding fails; partial/unsupported is never a pass.
    def hard(items):
        return any(item["severity"] == "hard" for item in items)

    semantic_hard = hard(semantic_findings)
    visual_hard = hard(visual_findings)
    semantic_partial = any(item["severity"] == "partial" for item in semantic_findings) or bool(unsupported)
    visual_partial = any(item["severity"] == "partial" for item in visual_findings) or bool(svg and svg["limitations"])

    semantic_status = "fail" if semantic_hard else ("partial" if semantic_partial else "pass")
    if svg is None:
        visual_status = "not_checked"
    else:
        visual_status = "fail" if visual_hard else ("partial" if visual_partial else "pass")
    overall = "fail" if "fail" in (semantic_status, visual_status) else (
        "partial" if "partial" in (semantic_status, visual_status) else
        ("partial" if visual_status == "not_checked" else "pass")
    )
    exit_code = 1 if overall == "fail" else (3 if overall == "partial" else 0)

    report = {
        "schema": "plantuml-native-readback/1",
        "tool": {"name": "native-readback.py", "version": VERSION},
        "engine": "plantuml",
        "inputs": {
            "source": {"path": str(source_path), "sha256": sha256_file(source_path)},
            "semantics": {"path": str(semantics_path), "sha256": sha256_file(semantics_path)},
            "svg": {"path": str(svg_path), "sha256": sha256_file(svg_path)} if svg_path else None,
        },
        "source": {"path": str(source_path), "sha256": sha256_file(source_path),
                   "format": source_path.suffix.lower().lstrip(".")},
        "records": {
            "source": {
                "start_tag": source["start_tag"], "end_tag": source["end_tag"],
                "groups": source["groups"], "elements": source["elements"],
                "relations": source["relations"],
                "hidden_constraints": {"count": len(source["hidden_constraints"]),
                                        "items": source["hidden_constraints"]},
                "legend": source["legend"],
            },
            "svg": svg_results,
        },
        "diff": {
            "zones_missing": zone_missing, "zones_extra": zone_extra,
            "zone_label_mismatch": zone_label_mismatch,
            "elements_missing": elem_missing, "elements_extra": elem_extra,
            "element_label_mismatch": elem_label_mismatch,
            "duplicate_labels": duplicate_labels,
        },
        "legend": {
            "authorization": legend_authorization,
            "source_present": source["legend"]["present"],
            "visible_present": bool((svg or {}).get("legend_texts")),
        },
        "semantic": {"status": semantic_status, "findings": semantic_findings},
        "visual": {"status": visual_status, "findings": visual_findings},
        "unsupported": unsupported,
        "not_evaluated": not_evaluated,
        "status": overall,
        "overall": overall,
        "actual": {
            "groups": source["groups"],
            "elements": source["elements"],
            "relations": source["relations"],
            "hidden_constraints": source["hidden_constraints"],
        },
        "exit_code": exit_code,
        "limits": [
            "Crossings, edge-through-node and long-edge quantities are per-method SVG measurements; "
            "they are not cross-engine rankings and depend on curve sampling.",
            "PlantUML clusters are excluded from edge-through-node checks; only leaf entity boxes are used.",
            "Text glyph widths are taken from the SVG textLength attribute when present; glyph height is "
            "approximated from font-size, so label/line clearance is not a pixel-exact measurement.",
            "Identity is matched by alias-qualified name; an alias-less declaration is reported as "
            "unsupported/partial rather than silently label-matched.",
        ],
    }
    return report


def build_parser():
    parser = argparse.ArgumentParser(
        prog="native-readback.py",
        description="Independently read back a PlantUML .puml and optional rendered SVG and compare "
                    "them with the authoritative semantic JSON.",
        epilog="Exit codes: 0 pass, 1 hard discrepancy, 2 usage/IO error, 3 partial/unsupported.",
    )
    parser.add_argument("--source", required=True, help="native .puml file to read back")
    parser.add_argument("--semantics", required=True, help="authoritative semantic JSON")
    parser.add_argument("--svg", default=None, help="actual rendered SVG (optional)")
    parser.add_argument("--output", required=True, help="new report path; must not already exist")
    parser.add_argument("--version", action="version", version=f"native-readback.py {VERSION}")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    source_path = Path(args.source)
    semantics_path = Path(args.semantics)
    svg_path = Path(args.svg) if args.svg else None
    output_path = Path(args.output)
    for label, path in (("source", source_path), ("semantics", semantics_path)):
        if not path.is_file():
            print(f"error: {label} file not found: {path}", file=sys.stderr)
            return 2
    if svg_path is not None and not svg_path.is_file():
        print(f"error: svg file not found: {svg_path}", file=sys.stderr)
        return 2
    if output_path.exists():
        print(f"error: refusing to overwrite existing report: {output_path}", file=sys.stderr)
        return 2
    try:
        report = analyze(source_path, semantics_path, svg_path, output_path)
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (json.JSONDecodeError, ET.ParseError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": report["status"],
        "semantic": report["semantic"]["status"],
        "visual": report["visual"]["status"],
        "exit_code": report["exit_code"],
        "report": str(output_path),
    }, ensure_ascii=False))
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
