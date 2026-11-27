import argparse
from collections import defaultdict
import heapq
import itertools
import json
import math
from pathlib import Path
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET


VERSION = "1.2.0"
LABEL_FONT_SIZE = 16
LABEL_PADDING = 4
LABEL_GAP = 6
EPS = 1e-6
MAX_GRID = 160000
MAX_BYTES = 10000000
SIDES = {"left": (-1, 0), "right": (1, 0), "top": (0, -1), "bottom": (0, 1)}
DEFAULTS = {"clearance": 8, "edgeSpacing": 10, "bendPenalty": 30, "crossingPenalty": 120, "collinearPenalty": 5, "fontFamily": "Arial, Microsoft YaHei, sans-serif"}


class DiagramError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise DiagramError(message)


def fields(value, required, optional=()):
    require(isinstance(value, dict), "expected an object")
    require(set(required) <= set(value), "missing fields: " + str(sorted(set(required) - set(value))))
    require(set(value) <= set(required) | set(optional), "unknown fields: " + str(sorted(set(value) - set(required) - set(optional))))


def text(value):
    require(isinstance(value, str), "expected a string")
    require(all(c in "\t\n\r" or 32 <= ord(c) <= 0xD7FF or 0xE000 <= ord(c) <= 0xFFFD or 0x10000 <= ord(c) <= 0x10FFFF for c in value), "invalid XML character")
    return value


def number(value, positive=False):
    require(isinstance(value, (int, float)) and not isinstance(value, bool), "expected a number")
    require(abs(value) <= 1000000 and math.isfinite(value), "non-finite or out-of-range coordinate")
    require(not positive or value > EPS, "expected a positive size")
    return float(value)


def fmt(value):
    return format(value, ".15g")


def box(value):
    fields(value, ("x", "y", "w", "h"))
    x, y = number(value["x"]), number(value["y"])
    return (x, y, x + number(value["w"], True), y + number(value["h"], True))


def point(value):
    fields(value, ("x", "y"))
    return number(value["x"]), number(value["y"])


def inflate(rect, gap):
    x, y, r, b = rect
    return x - gap, y - gap, r + gap, b + gap


def contains(outer, inner):
    return all((outer[0] <= inner[0] + EPS, outer[1] <= inner[1] + EPS, outer[2] + EPS >= inner[2], outer[3] + EPS >= inner[3]))


def overlaps(a, b):
    return min(a[2], b[2]) > max(a[0], b[0]) + EPS and min(a[3], b[3]) > max(a[1], b[1]) + EPS


def inside(p, rect):
    return rect[0] + EPS < p[0] < rect[2] - EPS and rect[1] + EPS < p[1] < rect[3] - EPS


def axis(a, b):
    if abs(a[1] - b[1]) <= EPS and abs(a[0] - b[0]) > EPS:
        return 1
    if abs(a[0] - b[0]) <= EPS and abs(a[1] - b[1]) > EPS:
        return 2
    return 0


def hits(a, b, rect):
    if inside(a, rect) or inside(b, rect):
        return True
    if axis(a, b) == 1:
        return rect[1] + EPS < a[1] < rect[3] - EPS and min(max(a[0], b[0]), rect[2]) > max(min(a[0], b[0]), rect[0]) + EPS
    if axis(a, b) == 2:
        return rect[0] + EPS < a[0] < rect[2] - EPS and min(max(a[1], b[1]), rect[3]) > max(min(a[1], b[1]), rect[1]) + EPS
    return False


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def simplify(points):
    result = []
    for p in points:
        if result and distance(result[-1], p) <= EPS:
            continue
        while len(result) >= 2 and axis(result[-2], result[-1]) == axis(result[-1], p) and abs(distance(result[-2], p) - distance(result[-2], result[-1]) - distance(result[-1], p)) < EPS:
            result.pop()
        result.append(p)
    return result


def interaction(a, b, c, d, spacing):
    first, second = axis(a, b), axis(c, d)
    if not first or not second:
        return 0, 0, 0
    if first == second:
        varying, fixed = (0, 1) if first == 1 else (1, 0)
        length = max(0, min(max(a[varying], b[varying]), max(c[varying], d[varying])) - max(min(a[varying], b[varying]), min(c[varying], d[varying])))
        separation = abs(a[fixed] - c[fixed])
        return 0, length if separation < EPS else 0, length if EPS <= separation < spacing - EPS else 0
    if first == 2:
        a, b, c, d = c, d, a, b
    crossing = min(a[0], b[0]) - EPS <= c[0] <= max(a[0], b[0]) + EPS and min(c[1], d[1]) - EPS <= a[1] <= max(c[1], d[1]) + EPS
    return int(crossing), 0, 0


class Model:
    def __init__(self, data):
        fields(data, ("title", "canvas", "fidelity_intent", "zones", "elements", "relations"), ("layout_policy", "uncertain", "style"))
        self.title = text(data["title"])
        require(data["fidelity_intent"] == "reproduction", "fidelity_intent must remain reproduction")
        self.policy = data.get("layout_policy", "preserve")
        require(self.policy in ("preserve", "optimize"), "unknown layout_policy")
        fields(data["canvas"], ("w", "h"))
        self.canvas = (0, 0, number(data["canvas"]["w"], True), number(data["canvas"]["h"], True))
        self.style = dict(DEFAULTS)
        fields(data.get("style", {}), (), DEFAULTS)
        self.style.update(data.get("style", {}))
        for key, value in self.style.items():
            if key == "fontFamily":
                require(bool(text(value)) and not any(c in value for c in ";=\n\r"), "invalid fontFamily")
            else:
                number(value, True)
        self.uncertain = data.get("uncertain", [])
        require(isinstance(self.uncertain, list), "uncertain must be a list")
        try:
            json.dumps(self.uncertain, ensure_ascii=False, allow_nan=False).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise DiagramError("uncertain must contain finite JSON values") from exc
        require(all(isinstance(data[key], list) for key in ("zones", "elements", "relations")), "zones, elements and relations must be arrays")
        require(len(data["zones"]) + len(data["elements"]) <= 500 and len(data["relations"]) <= 1000, "model budget exceeded: at most 500 vertices and 1000 relations")
        self.rows, self.parents, self.boxes = {}, {}, {}
        self.zones, self.elements, self.relations = {}, {}, {}
        for name, destination in (("zones", self.zones), ("elements", self.elements), ("relations", self.relations)):
            require(isinstance(data[name], list), name + " must be an array")
            for row in data[name]:
                if name == "relations":
                    fields(row, ("id", "from", "to"), ("label", "color", "source_side", "target_side", "via", "label_position"))
                else:
                    fields(row, ("id", "label", "box") + (("zone",) if name == "elements" else ()), ("fontSize", "bold") if name == "elements" else ("parent", "fill", "fontSize"))
                ident = text(row["id"])
                require(ident.strip() == ident and bool(ident) and ident not in self.rows and ident not in ("0", "1"), "duplicate or reserved id: " + ident)
                self.rows[ident] = row
                destination[ident] = row
                if "label" in row:
                    text(row["label"])
                for key in ("fill", "color"):
                    if key in row:
                        require(isinstance(row[key], str) and re.fullmatch(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?|none", row[key]) is not None, "invalid color")
                if "fontSize" in row:
                    number(row["fontSize"], True)
                if "bold" in row:
                    require(isinstance(row["bold"], bool), "bold must be boolean")
                if name != "relations":
                    self.boxes[ident] = box(row["box"])
                    self.parents[ident] = text(row.get("parent", "1") if name == "zones" else row["zone"])
        for ident, parent in self.parents.items():
            require(ident not in self.zones or "parent" not in self.zones[ident] or parent in self.zones, "explicit parent must reference a zone: " + ident)
            require(parent == "1" and ident in self.zones or parent in self.zones, "invalid zone parent: " + ident)
            self.ancestors(ident)
        for ident, row in self.relations.items():
            require(text(row["from"]) in self.boxes and text(row["to"]) in self.boxes, "invalid relation endpoint: " + ident)
            require(row["from"] != row["to"], "self loops are unsupported: " + ident)
            require(row.get("color") != "none", "invisible relations are unsupported: " + ident)
            for key in ("source_side", "target_side"):
                if key in row:
                    require(isinstance(row[key], str) and row[key] in SIDES, "invalid port side: " + ident)
            require(isinstance(row.get("via", []), list), "via must be an array")
            for item in row.get("via", []):
                point(item)
            if "label_position" in row:
                require(bool(row.get("label")), "label_position requires nonempty label: " + ident)
                fields(row["label_position"], ("x", "offset"))
                require(-1 <= number(row["label_position"]["x"]) <= 1, "label_position.x must be in [-1,1]")
                point(row["label_position"]["offset"])
            if self.policy == "preserve":
                require(all(k in row for k in ("via", "source_side", "target_side")), "preserve requires explicit sides and via (may be empty): " + ident)

    def ancestors(self, ident):
        result = []
        seen = {ident}
        while ident != "1":
            require(ident in self.parents, "unknown parent: " + ident)
            ident = self.parents[ident]
            require(ident not in seen, "cyclic zone parent")
            result.append(ident)
            seen.add(ident)
        return result

    def lca(self, row):
        targets = set(self.ancestors(row["to"]))
        return next(parent for parent in self.ancestors(row["from"]) if parent in targets)

    def header(self, ident, boxes=None):
        rect = (boxes or self.boxes)[ident]
        return rect[0], rect[1], rect[2], rect[1] + self.title_height(ident)

    def title_height(self, ident):
        return max(32, self.zones[ident].get("fontSize", 18) * 1.5 + 8)

    def geometry_errors(self, boxes=None):
        boxes = self.boxes if boxes is None else boxes
        errors = []
        for ident, rect in sorted(boxes.items()):
            parent = self.parents[ident]
            boundary = self.canvas if parent == "1" else boxes.get(parent)
            if boundary is None or not contains(boundary, rect):
                errors.append({"code": "containment", "id": ident, "parent": parent})
            if parent in boxes and overlaps(rect, self.header(parent, boxes)):
                errors.append({"code": "title_overlap", "id": ident, "zone": parent})
            if ident in self.zones and self.title_height(ident) >= rect[3] - rect[1]:
                errors.append({"code": "title_exceeds_zone", "id": ident})
        for a, b in itertools.combinations(sorted(boxes), 2):
            if a not in self.ancestors(b) and b not in self.ancestors(a) and overlaps(boxes[a], boxes[b]):
                errors.append({"code": "overlap", "ids": [a, b]})
        return errors

    def obstacles(self, row, gap=0, boxes=None):
        boxes = self.boxes if boxes is None else boxes
        ancestors = set(self.ancestors(row["from"]) + self.ancestors(row["to"]))
        result = [(ident, inflate(rect, gap)) for ident, rect in sorted(boxes.items()) if ident in self.elements or ident not in ancestors]
        result.extend((ident + ":title", inflate(self.header(ident, boxes), gap)) for ident in sorted(self.zones) if ident in boxes)
        return result

    def ports(self):
        groups = defaultdict(list)
        for ident, row in sorted(self.relations.items()):
            a, b = self.boxes[row["from"]], self.boxes[row["to"]]
            dx, dy = b[0] + b[2] - a[0] - a[2], b[1] + b[3] - a[1] - a[3]
            source = ("right" if dx >= 0 else "left") if abs(dx) >= abs(dy) else ("bottom" if dy >= 0 else "top")
            target = {"right": "left", "left": "right", "bottom": "top", "top": "bottom"}[source]
            for role, end, side in (("source", "from", source), ("target", "to", target)):
                groups[(row[end], row.get(role + "_side", side))].append((ident, role))
        result = defaultdict(dict)
        for (terminal, side), uses in sorted(groups.items()):
            rect = self.boxes[terminal]
            length = rect[3] - rect[1] if side in ("left", "right") else rect[2] - rect[0]
            low = self.style["clearance"]
            if terminal in self.zones and side in ("left", "right"):
                low += self.title_height(terminal)
            high = length - self.style["clearance"]
            require(high > low, "no port space: " + terminal)
            require(len(uses) == 1 or (high - low) / (len(uses) + 1) >= self.style["edgeSpacing"], "insufficient parallel port spacing: " + terminal)
            for index, (ident, role) in enumerate(uses):
                fraction = (low + (high - low) * (index + 1) / (len(uses) + 1)) / length
                x = 0 if side == "left" else 1 if side == "right" else fraction
                y = 0 if side == "top" else 1 if side == "bottom" else fraction
                result[ident][role] = (x, y, side)
        return result


def endpoint(rect, port):
    return rect[0] + (rect[2] - rect[0]) * port[0], rect[1] + (rect[3] - rect[1]) * port[1]


def path_errors(model, row, points, boxes=None):
    errors = []
    obstacles = model.obstacles(row, boxes=boxes)
    for p in points:
        if not contains(model.canvas, (p[0], p[1], p[0], p[1])):
            errors.append({"code": "route_outside_canvas", "id": row["id"]})
    for index, (a, b) in enumerate(zip(points, points[1:])):
        if not axis(a, b):
            errors.append({"code": "nonorthogonal_or_zero_segment", "id": row["id"], "segment": index})
        for ident, rect in obstacles:
            if hits(a, b, rect):
                errors.append({"code": "through_box", "id": row["id"], "obstacle": ident, "segment": index})
    return errors


def route_warnings(routes, spacing):
    metrics = {"crossings": 0, "collinear_length": 0, "near_parallel_length": 0}
    warnings = []
    for first, second in itertools.combinations(sorted(routes), 2):
        counts = [0, 0, 0]
        crossings = set()
        shared_terminals = set((routes[first][0], routes[first][-1])) & set((routes[second][0], routes[second][-1]))
        for a, b in zip(routes[first], routes[first][1:]):
            for c, d in zip(routes[second], routes[second][1:]):
                crossing, collinear, near = interaction(a, b, c, d, spacing)
                if crossing:
                    location = (c[0], a[1]) if axis(a, b) == 1 else (a[0], c[1])
                    if location not in shared_terminals:
                        crossings.add(location)
                counts[1] += collinear
                counts[2] += near
        counts[0] = len(crossings)
        for key, value in zip(metrics, counts):
            metrics[key] += value
        if any(counts):
            warnings.append({"code": "edge_interaction", "ids": [first, second], **dict(zip(metrics, counts))})
    return {"metrics": metrics, "warnings": warnings}


def shortest_path(start, finish, obstacles, occupied, model, initial_axis=0, final_axis=0, overlap_scale=1.0):
    gap = model.style["edgeSpacing"]
    xs, ys = {0, model.canvas[2], start[0], finish[0]}, {0, model.canvas[3], start[1], finish[1]}
    for _, rect in obstacles:
        xs.update((rect[0], rect[2]))
        ys.update((rect[1], rect[3]))
    for a, b in occupied:
        xs.update((a[0] - gap, a[0], a[0] + gap, b[0]))
        ys.update((a[1] - gap, a[1], a[1] + gap, b[1]))
    xs = sorted(x for x in xs if 0 <= x <= model.canvas[2])
    ys = sorted(y for y in ys if 0 <= y <= model.canvas[3])
    require(len(xs) * len(ys) <= MAX_GRID, "routing grid budget exceeded; split or simplify geometry explicitly")
    require(all(contains(model.canvas, (p[0], p[1], p[0], p[1])) and not any(inside(p, r) for _, r in obstacles) for p in (start, finish)), "route anchor blocked or outside canvas")
    origin = (xs.index(start[0]), ys.index(start[1]), initial_axis)
    goal = (xs.index(finish[0]), ys.index(finish[1]))
    costs, previous, queue = {origin: 0}, {}, [(0, origin)]
    segment_cache = {}
    best, best_cost = None, float("inf")
    while queue:
        cost, state = heapq.heappop(queue)
        if cost != costs[state] or cost >= best_cost:
            continue
        x, y, direction = state
        if (x, y) == goal:
            total = cost + (model.style["bendPenalty"] if final_axis and direction != final_axis else 0)
            if total < best_cost:
                best, best_cost = state, total
            continue
        a = (xs[x], ys[y])
        for xx, yy, next_axis in ((x - 1, y, 1), (x + 1, y, 1), (x, y - 1, 2), (x, y + 1, 2)):
            if not (0 <= xx < len(xs) and 0 <= yy < len(ys)):
                continue
            b = (xs[xx], ys[yy])
            key = tuple(sorted((a, b)))
            if key not in segment_cache:
                if any(hits(a, b, rect) for _, rect in obstacles):
                    segment_cache[key] = None
                else:
                    penalty = 0
                    for c, d in occupied:
                        crossing, collinear, near = interaction(a, b, c, d, gap)
                        penalty += crossing * model.style["crossingPenalty"] + (collinear + near) * model.style["collinearPenalty"] * overlap_scale
                    segment_cache[key] = distance(a, b) + penalty
            step = segment_cache[key]
            if step is None:
                continue
            candidate = cost + step + (model.style["bendPenalty"] if direction and direction != next_axis else 0)
            target = (xx, yy, next_axis)
            if candidate < costs.get(target, float("inf")):
                costs[target], previous[target] = candidate, state
                heapq.heappush(queue, (candidate, target))
    require(best is not None, "no safe orthogonal route; no straight-line fallback")
    path = []
    while best != origin:
        path.append((xs[best[0]], ys[best[1]]))
        best = previous[best]
    return simplify([start] + list(reversed(path)))


def route_relation(model, ident, ports, occupied, overlap_scale=1.0):
    row = model.relations[ident]
    ends = [endpoint(model.boxes[row[end]], ports[ident][role]) for end, role in (("from", "source"), ("to", "target"))]
    via = [point(p) for p in row.get("via", [])]
    if model.policy == "preserve":
        route = [ends[0]] + via + [ends[1]]
    else:
        obstacles = model.obstacles(row, model.style["clearance"])
        stubs = []
        for index, (role, terminal, other) in enumerate((("source", row["from"], row["to"]), ("target", row["to"], row["from"]))):
            dx, dy = SIDES[ports[ident][role][2]]
            sign = -1 if terminal in model.ancestors(other) else 1
            stub = (ends[index][0] + sign * dx * model.style["clearance"], ends[index][1] + sign * dy * model.style["clearance"])
            require(not any(hits(ends[index], stub, rect) for name, rect in obstacles if name != terminal), "blocked terminal escape: " + ident)
            stubs.append(stub)
        anchors = [stubs[0]] + via + [stubs[1]]
        route = [ends[0], stubs[0]]
        for index, (start, finish) in enumerate(zip(anchors, anchors[1:])):
            part = shortest_path(start, finish, obstacles, occupied, model, axis(route[-2], route[-1]) if len(route) > 1 else 0, axis(stubs[1], ends[1]) if index == len(anchors) - 2 else 0, overlap_scale)
            route.extend(part[1:])
        route.append(ends[1])
    errors = path_errors(model, row, route)
    require(not errors, "unsafe route " + ident + ": " + json.dumps(errors, ensure_ascii=False))
    return route


def shared_segment_pairs(model, routes):
    spacing = model.style["edgeSpacing"]
    pairs = []
    for first, second in itertools.combinations(sorted(routes), 2):
        first_row, second_row = model.relations[first], model.relations[second]
        if {first_row["from"], first_row["to"]} & {second_row["from"], second_row["to"]}:
            continue
        total = 0.0
        for a, b in zip(routes[first], routes[first][1:]):
            for c, d in zip(routes[second], routes[second][1:]):
                total += interaction(a, b, c, d, spacing)[1]
        if total > EPS:
            pairs.append((first, second, total))
    return pairs


def repair_shared_segments(model, routes):
    for _ in range(2):
        pairs = shared_segment_pairs(model, routes)
        if not pairs:
            break
        ports = model.ports()
        changed = False
        for later in sorted({second for _, second, _ in pairs}):
            occupied = [segment for ident, points in routes.items() if ident != later for segment in zip(points, points[1:])]
            try:
                trial = route_relation(model, later, ports, occupied, overlap_scale=8.0)
            except DiagramError:
                continue
            candidate = dict(routes)
            candidate[later] = trial
            before = route_warnings(routes, model.style["edgeSpacing"])["metrics"]
            after = route_warnings(candidate, model.style["edgeSpacing"])["metrics"]
            if after["collinear_length"] < before["collinear_length"] - EPS and after["crossings"] <= before["crossings"] + 1 and after["near_parallel_length"] <= before["near_parallel_length"] + EPS:
                routes = candidate
                changed = True
        if not changed:
            break
    return routes


def route_all(model, ports):
    routes, occupied = {}, []
    for ident in sorted(model.relations):
        route = route_relation(model, ident, ports, occupied)
        routes[ident] = route
        compact = simplify(route)
        occupied.extend(zip(compact, compact[1:]))
    if model.policy == "optimize":
        routes = repair_shared_segments(model, routes)
    return routes


def label_dimensions(value):
    lines = value.split("\n")
    widths = [sum(0 if unicodedata.combining(c) else 1 if unicodedata.east_asian_width(c) in "WF" else 0.7 for c in line) * LABEL_FONT_SIZE for line in lines]
    return max(widths) + 2 * LABEL_PADDING + 4, len(lines) * LABEL_FONT_SIZE * 1.25 + 2 * LABEL_PADDING + 4


def route_point(points, relative_x):
    lengths = [distance(a, b) for a, b in zip(points, points[1:])]
    remaining = (relative_x + 1) * sum(lengths) / 2
    for index, (a, b, length) in enumerate(zip(points, points[1:], lengths)):
        if remaining <= length + EPS or index == len(lengths) - 1:
            t = min(1, max(0, remaining / length)) if length > EPS else 0
            return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])
        remaining -= length
    raise DiagramError("label route has no segments")


def label_record(row, route, position):
    anchor = route_point(route, position["x"])
    dx, dy = point(position["offset"])
    center = [anchor[0] + dx, anchor[1] + dy]
    width, height = label_dimensions(row["label"])
    return {"x": position["x"], "offset": {"x": dx, "y": dy}, "center": center, "bounds": [center[0] - width / 2, center[1] - height / 2, center[0] + width / 2, center[1] + height / 2], "orientation": "horizontal", "font_size": LABEL_FONT_SIZE, "explicit": "label_position" in row}


def crosses_border(rect, zone):
    x, y, r, b = rect
    zx, zy, zr, zb = zone
    if y < zb - EPS and b > zy + EPS and ((x < zx - EPS and r > zx + EPS) or (x < zr - EPS and r > zr + EPS)):
        return True
    if x < zr - EPS and r > zx + EPS and ((y < zy - EPS and b > zy + EPS) or (y < zb - EPS and b > zb + EPS)):
        return True
    return False


def label_conflicts(model, rect, routes, placed):
    issues = []
    if not contains(model.canvas, rect):
        issues.append("canvas")
    for ident in sorted(model.elements):
        if overlaps(rect, inflate(model.boxes[ident], 2)):
            issues.append("node:" + ident)
    for ident in sorted(model.zones):
        if overlaps(rect, inflate(model.header(ident), 2)):
            issues.append("title:" + ident)
        if crosses_border(rect, model.boxes[ident]):
            issues.append("zone_border:" + ident)
    for ident, points in sorted(routes.items()):
        if any(hits(a, b, inflate(rect, 2)) for a, b in zip(points, points[1:])):
            issues.append("route:" + ident)
    for ident, other in sorted(placed.items()):
        if overlaps(inflate(rect, 2), other["bounds"]):
            issues.append("label:" + ident)
    return issues


def plan_labels(model, routes):
    placed = {}
    labelled = [ident for ident, row in model.relations.items() if row.get("label")]
    for ident in sorted(labelled, key=lambda k: ("label_position" not in model.relations[k], k)):
        row, route = model.relations[ident], simplify(routes[ident])
        if "label_position" in row:
            record = label_record(row, route, row["label_position"])
            issues = label_conflicts(model, record["bounds"], routes, placed)
            require(not issues, "unsafe explicit label_position " + ident + ": " + ",".join(issues))
            record["issues"] = issues
            placed[ident] = record
            continue
        width, height = label_dimensions(row["label"])
        total = sum(distance(a, b) for a, b in zip(route, route[1:]))
        prefix, candidates = 0, []
        for index, (a, b) in enumerate(zip(route, route[1:])):
            direction = axis(a, b)
            varying = 0 if direction == 1 else 1
            length = distance(a, b)
            half = (width if direction == 1 else height) / 2
            low, high = min(a[varying], b[varying]) + half + 8, max(a[varying], b[varying]) - half - 8
            short = low > high
            positions = {(a[varying] + b[varying]) / 2}
            if not short:
                positions.update((low, high))
                boundaries = [rect for key, rect in model.boxes.items() if key in model.elements]
                boundaries.extend(model.header(key) for key in model.zones)
                boundaries.extend(record["bounds"] for record in placed.values())
                for rect in boundaries:
                    positions.update((rect[varying] - half - 4, rect[varying + 2] + half + 4))
                for other in routes.values():
                    for p in other:
                        positions.update((p[varying] - half - LABEL_GAP, p[varying] + half + LABEL_GAP))
                positions = {p for p in positions if low - EPS <= p <= high + EPS}
            for location in sorted(positions):
                along = abs(location - a[varying])
                relative_x = 2 * (prefix + along) / total - 1
                for extra in (0, 8, 20, 40):
                    shift = (width if direction == 1 else height) / 2 + LABEL_GAP + extra
                    for side in (-1, 1):
                        displacement = side * ((height if direction == 1 else width) / 2 + LABEL_GAP + extra)
                        for along_shift in ((0.0, shift, -shift) if short else (0.0,)):
                            position = {"x": relative_x, "offset": {"x": along_shift if direction == 1 else displacement, "y": displacement if direction == 1 else along_shift}}
                            record = label_record(row, route, position)
                            issues = label_conflicts(model, record["bounds"], routes, placed)
                            record["issues"] = issues
                            score = (len(issues), direction != 1, extra, abs(along_shift), abs(relative_x), -length, index, location, side)
                            candidates.append((score, record))
            prefix += length
        require(bool(candidates), "no label candidate segments: " + ident)
        placed[ident] = min(candidates, key=lambda item: item[0])[1]
    return placed


def assess_labels(model, routes, positions):
    records, warnings, errors = {}, [], []
    for ident, position in sorted(positions.items()):
        records[ident] = label_record(model.relations[ident], routes[ident], position)
    for ident, record in records.items():
        others = {key: value for key, value in records.items() if key != ident}
        record["issues"] = label_conflicts(model, record["bounds"], routes, others)
        explicit = model.relations[ident].get("label_position")
        if explicit and (abs(record["x"] - explicit["x"]) > EPS or distance(point(record["offset"]), point(explicit["offset"])) > EPS):
            errors.append({"code": "explicit_label_changed", "id": ident})
        if record["issues"]:
            item = {"code": "label_unresolved", "id": ident, "issues": record["issues"]}
            (errors if explicit else warnings).append(item)
    unresolved = sum(bool(row["issues"]) for row in records.values())
    return {"total": len(records), "estimated_clear": len(records) - unresolved, "unresolved": unresolved, "measurement": "conservative text estimate; not font measurement", "labels": records}, warnings, errors


def proper_crossings(routes):
    result = []
    for first, second in itertools.combinations(sorted(routes), 2):
        seen = set()
        for a, b in zip(routes[first], routes[first][1:]):
            for c, d in zip(routes[second], routes[second][1:]):
                if axis(a, b) == axis(c, d) or not axis(a, b) or not axis(c, d):
                    continue
                h1, h2, v1, v2 = (a, b, c, d) if axis(a, b) == 1 else (c, d, a, b)
                if min(h1[0], h2[0]) + EPS < v1[0] < max(h1[0], h2[0]) - EPS and min(v1[1], v2[1]) + EPS < h1[1] < max(v1[1], v2[1]) - EPS:
                    seen.add((v1[0], h1[1]))
        result.extend({"ids": [first, second], "point": list(p)} for p in sorted(seen))
    return result


def style_string(values):
    return ";".join(key + "=" + str(value) for key, value in values.items()) + ";"


def vertex_style(model, ident):
    row = model.rows[ident]
    zone = ident in model.zones
    result = {"shape": "swimlane" if zone else "rectangle", "html": "0", "whiteSpace": "wrap", "rounded": "0", "fontFamily": model.style["fontFamily"], "fontSize": fmt(row.get("fontSize", 18 if zone else 12)), "fontStyle": "1" if row.get("bold", zone) else "0", "strokeWidth": "3" if zone else "2", "fillColor": row.get("fill", "#ffffff"), "strokeColor": "#444444", "fontColor": "#222222"}
    if zone:
        result.update({"container": "1", "collapsible": "0", "horizontal": "1", "startSize": fmt(model.title_height(ident)), "recursiveResize": "0"})
    return result


def edge_style(model, row, ports):
    result = {"edgeStyle": "none", "noEdgeStyle": "1", "orthogonal": "1", "rounded": "0", "html": "0", "startArrow": "none", "endArrow": "classic", "endFill": "1", "strokeWidth": "1.5", "strokeColor": row.get("color", "#666666"), "fontFamily": model.style["fontFamily"], "fontSize": str(LABEL_FONT_SIZE), "horizontal": "1", "align": "center", "verticalAlign": "middle", "whiteSpace": "nowrap", "spacing": "0", "labelBackgroundColor": "#ffffff", "labelBorderColor": "none", "labelPadding": str(LABEL_PADDING), "jumpStyle": "arc", "jumpSize": "6", "jumpLayers": "1"}
    for role, prefix in (("source", "exit"), ("target", "entry")):
        port = ports[row["id"]][role]
        result.update({prefix + "X": fmt(port[0]), prefix + "Y": fmt(port[1]), prefix + "Perimeter": "0", prefix + "Dx": "0", prefix + "Dy": "0"})
    return result


def xml_diagram(model, routes, ports):
    labels = plan_labels(model, routes)
    root = ET.Element("mxfile", compressed="false")
    diagram = ET.SubElement(root, "diagram", id="architecture", name=model.title)
    graph = ET.SubElement(diagram, "mxGraphModel", page="1", pageScale="1", pageWidth=fmt(model.canvas[2]), pageHeight=fmt(model.canvas[3]))
    cells = ET.SubElement(graph, "root")
    ET.SubElement(cells, "mxCell", id="0")
    ET.SubElement(cells, "mxCell", id="1", parent="0")
    for ident in sorted(model.boxes, key=lambda k: (len(model.ancestors(k)), k)):
        row, rect, parent = model.rows[ident], model.boxes[ident], model.parents[ident]
        offset = model.boxes[parent][:2] if parent != "1" else (0, 0)
        cell = ET.SubElement(cells, "mxCell", id=ident, value=row["label"], vertex="1", parent=parent, style=style_string(vertex_style(model, ident)))
        ET.SubElement(cell, "mxGeometry", x=fmt(rect[0] - offset[0]), y=fmt(rect[1] - offset[1]), width=fmt(rect[2] - rect[0]), height=fmt(rect[3] - rect[1]), attrib={"as": "geometry"})
    for ident, row in sorted(model.relations.items()):
        parent = model.lca(row)
        offset = model.boxes[parent][:2] if parent != "1" else (0, 0)
        cell = ET.SubElement(cells, "mxCell", id=ident, value=row.get("label", ""), edge="1", parent=parent, source=row["from"], target=row["to"], style=style_string(edge_style(model, row, ports)))
        geometry = ET.SubElement(cell, "mxGeometry", relative="1", attrib={"as": "geometry"})
        array = ET.SubElement(geometry, "Array", attrib={"as": "points"})
        for x, y in routes[ident][1:-1]:
            ET.SubElement(array, "mxPoint", x=fmt(x - offset[0]), y=fmt(y - offset[1]))
        if ident in labels:
            label = labels[ident]
            geometry.set("x", fmt(label["x"]))
            geometry.set("y", "0")
            ET.SubElement(geometry, "mxPoint", x=fmt(label["offset"]["x"]), y=fmt(label["offset"]["y"]), attrib={"as": "offset"})
    return ET.tostring(root, encoding="unicode") + "\n"


def new_report(data):
    expected = {key: len(data.get(key, [])) if isinstance(data, dict) and isinstance(data.get(key), list) else None for key in ("elements", "zones", "relations")}
    return {"status": "fail", "counts": {"expected": expected, "actual": None}, "semantic_differences": [], "geometry_errors": [], "errors": [], "warnings": [], "metrics": {}, "visual_validation": "not_performed", "router": "fixed-geometry orthogonal visibility-grid Dijkstra; not ELK/libavoid"}


def finish_report(report):
    report["status"] = "fail" if any(report[key] for key in ("errors", "semantic_differences", "geometry_errors")) else "pass"
    return report


def parse_style(value):
    result = {}
    for item in value.split(";"):
        if item:
            require("=" in item, "unsupported style token")
            key, value = item.split("=", 1)
            require(key not in result, "duplicate style key")
            result[key] = value
    return result


def xml_number(value):
    try:
        return number(float(value))
    except (ValueError, TypeError, OverflowError) as exc:
        raise DiagramError("invalid XML numeric value") from exc


def svg_transform(element, parents):
    def compose(a, b):
        return (a[0] * b[0], a[1] * b[1], a[0] * b[2] + a[2], a[1] * b[3] + a[3])
    result = (1, 1, 0, 0)
    while element is not None:
        css = dict(item.split(":", 1) for item in element.get("style", "").split(";") if ":" in item)
        require(not any(key.strip() == "transform" and value.strip() != "none" for key, value in css.items()), "unsupported CSS transform")
        raw = element.get("transform", "")
        local = (1, 1, 0, 0)
        for name, values in re.findall(r"([A-Za-z]+)\s*\(([^)]*)\)", raw):
            values = [float(v) for v in re.split(r"[\s,]+", values.strip()) if v]
            require(all(math.isfinite(v) for v in values), "nonfinite SVG transform")
            if name == "translate" and len(values) in (1, 2):
                operation = (1, 1, values[0], values[1] if len(values) == 2 else 0)
            elif name == "scale" and len(values) in (1, 2):
                operation = (values[0], values[-1], 0, 0)
            elif name == "matrix" and len(values) == 6 and abs(values[1]) < EPS and abs(values[2]) < EPS:
                operation = (values[0], values[3], values[4], values[5])
            else:
                raise DiagramError("rotated or unsupported SVG transform: " + name)
            require(operation[0] > 0 and operation[1] > 0, "reflected SVG text unsupported")
            local = compose(local, operation)
        require(not re.sub(r"[A-Za-z]+\s*\([^)]*\)", "", raw).strip(" ,\n\t"), "invalid SVG transform")
        result = compose(local, result)
        element = parents.get(element)
    return result


def svg_value(element, key, parents, default=None):
    while element is not None:
        css = dict((k.strip(), v.strip()) for item in element.get("style", "").split(";") if ":" in item for k, v in [item.split(":", 1)])
        if key in css or key in element.attrib:
            return css.get(key, element.get(key))
        element = parents.get(element)
    return default


def validate_rendered_labels(model, routes, labels, svg):
    result = {"status": "fail", "errors": [], "labels": {}, "scope": "SVG text/background/position compatibility only; not full visual acceptance"}
    try:
        require(len(svg.encode("utf-8")) <= MAX_BYTES, "SVG input too large")
        svg = svg.replace('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">', "", 1)
        require(not re.search(r"<!DOCTYPE|<!ENTITY", svg, re.I), "unsupported SVG DTD or entity")
        root = ET.fromstring(svg)
        require(root.tag.split("}")[-1] == "svg", "expected SVG")
        parents = {child: parent for parent in root.iter() for child in parent}
        groups = {}
        for element in root.iter():
            ident = element.get("data-cell-id")
            if ident:
                require(ident not in groups, "duplicate SVG cell identity")
                groups[ident] = element
        def numeric(element, key):
            value = element.get(key, "")
            return xml_number(value[:-2] if value.endswith("px") else value)
        def rectangle(element):
            sx, sy, tx, ty = svg_transform(element, parents)
            x, y = numeric(element, "x"), numeric(element, "y")
            return (sx * x + tx, sy * y + ty, sx * (x + numeric(element, "width")) + tx, sy * (y + numeric(element, "height")) + ty)
        mappings = []
        for ident in sorted(model.elements):
            group = groups.get(ident)
            rects = [] if group is None else [e for e in group.iter() if e.tag.split("}")[-1] == "rect"]
            if rects:
                actual, expected = rectangle(rects[0]), model.boxes[ident]
                sx, sy = (actual[2] - actual[0]) / (expected[2] - expected[0]), (actual[3] - actual[1]) / (expected[3] - expected[1])
                require(abs(sx - sy) < 0.01 and sx > 0, "nonuniform SVG canvas scaling")
                mappings.append((sx, sy, actual[0] - sx * expected[0], actual[1] - sy * expected[1]))
        require(bool(mappings), "SVG needs native node rects and data-cell-id for calibration")
        mapping = mappings[0]
        require(all(all(abs(a - b) < 1.1 for a, b in zip(mapping, item)) for item in mappings), "inconsistent SVG node calibration")
        result["canvas_mapping"] = list(mapping)
        rendered_bounds = {}
        for ident, expected in sorted(labels.items()):
            try:
                require(ident in groups, "label cell missing from SVG")
                group = groups[ident]
                texts = [e for e in group.iter() if e.tag.split("}")[-1] == "text"]
                require("\n".join("".join(e.itertext()) for e in texts) == model.relations[ident]["label"], "label text missing or changed (HTML/raster label unsupported)")
                fonts, text_positions = [], []
                for node in texts:
                    sx, sy, tx, ty = svg_transform(node, parents)
                    require(abs(sx / mapping[0] - sy / mapping[1]) < 0.01, "distorted label text")
                    value = svg_value(node, "font-size", parents, "0")
                    size = xml_number(value[:-2] if value.endswith("px") else value) * sy / mapping[1]
                    fonts.append(size)
                    require(abs(size - LABEL_FONT_SIZE) < 0.5, "unexpected rendered label font size: " + str(size))
                    require(svg_value(node, "text-anchor", parents) == "middle", "rendered label alignment changed")
                    x = (sx * numeric(node, "x") + tx - mapping[2]) / mapping[0]
                    y = (sy * numeric(node, "y") + ty - mapping[3]) / mapping[1]
                    text_positions.append([x, y])
                    require(abs(x - expected["center"][0]) <= 3, "rendered label horizontal offset differs")
                backgrounds = [e for e in group.iter() if e.tag.split("}")[-1] == "rect" and e.get("fill", "").lower() in ("#ffffff", "#fff", "white")]
                require(len(backgrounds) == 1, "expected one white native label background")
                b = rectangle(backgrounds[0])
                bounds = [(b[0] - mapping[2]) / mapping[0], (b[1] - mapping[3]) / mapping[1], (b[2] - mapping[2]) / mapping[0], (b[3] - mapping[3]) / mapping[1]]
                center = [(bounds[0] + bounds[2]) / 2, (bounds[1] + bounds[3]) / 2]
                require(max(abs(a - b) for a, b in zip(center, expected["center"])) <= 4, "rendered label geometry/offset differs")
                require(bounds[2] - bounds[0] > 2 * LABEL_PADDING and bounds[3] - bounds[1] >= len(texts) * LABEL_FONT_SIZE * 1.1 + 2 * LABEL_PADDING - 2, "rendered white background padding too small")
                require(all(contains(bounds, (p[0], p[1], p[0], p[1])) for p in text_positions), "rendered text baseline outside background")
                issues = label_conflicts(model, bounds, routes, rendered_bounds)
                require(not issues, "rendered label collision: " + ",".join(issues))
                rendered_bounds[ident] = {"bounds": bounds}
                result["labels"][ident] = {"font_sizes": fonts, "center": center, "bounds": bounds, "text_positions": text_positions, "horizontal": True}
            except (DiagramError, ValueError) as exc:
                result["errors"].append({"id": ident, "error": str(exc)})
        curve_edges = [ident for ident in sorted(routes) if ident in groups and any(e.tag.split("}")[-1] == "path" and e.get("fill") == "none" and re.search(r"[ACQacq]", e.get("d", "")) for e in groups[ident].iter())]
        result["line_jumps"] = {"curve_edges": curve_edges, "proper_crossings": len(proper_crossings(routes)), "coverage": "not_proven; curve commands alone do not verify every jump"}
    except (DiagramError, ET.ParseError, ValueError, UnicodeError) as exc:
        result["errors"].append({"error": str(exc)})
    result["status"] = "fail" if result["errors"] else "pass"
    return result


def validate_diagram(data, xml, rendered_svg=None):
    report = new_report(data)
    try:
        model = Model(data)
        report["uncertain"] = model.uncertain
        require(isinstance(xml, str) and len(xml.encode("utf-8")) <= MAX_BYTES, "XML input too large")
        require(not re.search(r"<!DOCTYPE|<!ENTITY|<!--", xml, re.I), "DTD, entities and comments are unsupported")
        root = ET.fromstring(xml)
        require(root.tag == "mxfile" and root.attrib == {"compressed": "false"} and len(root) == 1, "expected one uncompressed mxfile diagram")
        diagram = root.find("diagram")
        require(diagram is not None and len(diagram) == 1 and diagram[0].tag == "mxGraphModel", "expected one mxGraphModel")
        if diagram.get("name") != model.title:
            report["semantic_differences"].append({"code": "title"})
        require(set(diagram.attrib) == {"id", "name"} and diagram.get("id") == "architecture", "unsupported diagram metadata")
        graph = diagram[0]
        require(set(graph.attrib) == {"page", "pageScale", "pageWidth", "pageHeight"} and graph.get("page") == "1" and graph.get("pageScale") == "1", "unsupported graph attributes")
        require(len(graph) == 1 and graph[0].tag == "root" and not graph[0].attrib, "unsupported graph structure")
        if (xml_number(graph.get("pageWidth")), xml_number(graph.get("pageHeight"))) != model.canvas[2:]:
            report["geometry_errors"].append({"code": "canvas"})
        cells = {}
        for cell in graph[0]:
            require(cell.tag == "mxCell" and cell.get("id") is not None and cell.get("id") not in cells, "invalid or duplicate XML cell id")
            cells[cell.get("id")] = cell
        require("0" in cells and "1" in cells and cells["0"].attrib == {"id": "0"} and cells["1"].attrib == {"id": "1", "parent": "0"}, "invalid root cells")
        expected = set(model.rows) | {"0", "1"}
        for ident in sorted(expected - set(cells)):
            report["semantic_differences"].append({"code": "missing", "id": ident})
        for ident in sorted(set(cells) - expected):
            report["semantic_differences"].append({"code": "extra", "id": ident})
        actual = {"elements": 0, "zones": 0, "relations": 0}
        styles, geometries = {}, {}
        for ident, cell in sorted(cells.items()):
            if ident in ("0", "1"):
                continue
            require(cell.get("parent") in cells, "unknown XML parent: " + ident)
            require((cell.get("vertex") == "1") != (cell.get("edge") == "1"), "invalid vertex/edge role: " + ident)
            allowed = {"id", "value", "parent", "style", "vertex"} if cell.get("vertex") == "1" else {"id", "value", "parent", "style", "edge", "source", "target"}
            require(set(cell.attrib) == allowed, "unsupported cell attributes: " + ident)
            styles[ident] = parse_style(cell.get("style", ""))
            require(len(cell) == 1 and cell[0].tag == "mxGeometry" and cell[0].get("as") == "geometry", "unsupported cell geometry: " + ident)
            geometries[ident] = cell[0]
            actual["relations" if cell.get("edge") == "1" else "zones" if styles[ident].get("container") == "1" else "elements"] += 1
        report["counts"]["actual"] = actual
        boxes = {}
        def absolute(ident, seen=()):
            if ident == "1":
                return (0, 0, 0, 0)
            require(ident not in seen and ident in geometries and cells[ident].get("vertex") == "1", "cyclic or invalid geometry parent")
            if ident not in boxes:
                geometry = geometries[ident]
                require(len(geometry) == 0 and set(geometry.attrib) == {"x", "y", "width", "height", "as"}, "unsupported relative vertex geometry")
                x, y, width, height = [xml_number(geometry.get(k)) for k in ("x", "y", "width", "height")]
                require(width > EPS and height > EPS, "invalid vertex dimensions")
                offset = absolute(cells[ident].get("parent"), seen + (ident,))
                boxes[ident] = (x + offset[0], y + offset[1], x + offset[0] + width, y + offset[1] + height)
            return boxes[ident]
        for ident in sorted(model.boxes.keys() & cells.keys()):
            rect = absolute(ident)
            if any(abs(a - b) > EPS for a, b in zip(rect, model.boxes[ident])):
                report["geometry_errors"].append({"code": "box_changed", "id": ident, "actual": rect, "expected": model.boxes[ident]})
        known_boxes = {ident: rect for ident, rect in boxes.items() if ident in model.boxes}
        report["geometry_errors"].extend(model.geometry_errors(known_boxes))
        ports = model.ports()
        routes, label_positions = {}, {}
        for ident in sorted(model.rows.keys() & cells.keys()):
            row, cell = model.rows[ident], cells[ident]
            expected_attributes = {"value": row.get("label", ""), "parent": model.parents[ident] if ident in model.boxes else model.lca(row)}
            expected_attributes.update({"vertex": "1"} if ident in model.boxes else {"edge": "1", "source": row["from"], "target": row["to"]})
            for key, value in expected_attributes.items():
                if cell.get(key) != value:
                    report["semantic_differences"].append({"code": key, "id": ident, "expected": value, "actual": cell.get(key)})
            expected_style = vertex_style(model, ident) if ident in model.boxes else edge_style(model, row, ports)
            if styles[ident] != expected_style:
                report["semantic_differences"].append({"code": "style_or_port", "id": ident})
            if ident in model.relations:
                require(row["from"] in boxes and row["to"] in boxes, "missing edge endpoint geometry")
                geometry = geometries[ident]
                arrays = geometry.findall("Array")
                require(len(arrays) == 1 and arrays[0].attrib == {"as": "points"}, "expected explicit edge waypoint array")
                base_attributes = {"relative": "1", "as": "geometry"}
                if row.get("label"):
                    require(set(geometry.attrib) == set(base_attributes) | {"x", "y"} and all(geometry.get(k) == v for k, v in base_attributes.items()) and len(geometry) == 2, "expected native label geometry")
                    relative_x, perpendicular = xml_number(geometry.get("x")), xml_number(geometry.get("y"))
                    require(-1 <= relative_x <= 1 and abs(perpendicular) < EPS, "invalid native label position")
                    offsets = geometry.findall("mxPoint")
                    require(len(offsets) == 1 and set(offsets[0].attrib) == {"x", "y", "as"} and offsets[0].get("as") == "offset", "expected native label offset")
                    label_positions[ident] = {"x": relative_x, "offset": {"x": xml_number(offsets[0].get("x")), "y": xml_number(offsets[0].get("y"))}}
                else:
                    require(geometry.attrib == base_attributes and len(geometry) == 1, "unexpected unlabelled edge geometry")
                parent = cell.get("parent")
                offset = absolute(parent)
                points = [endpoint(boxes[row["from"]], ports[ident]["source"])]
                for p in arrays[0]:
                    require(p.tag == "mxPoint" and set(p.attrib) == {"x", "y"}, "unsupported waypoint")
                    points.append((xml_number(p.get("x")) + offset[0], xml_number(p.get("y")) + offset[1]))
                points.append(endpoint(boxes[row["to"]], ports[ident]["target"]))
                report["geometry_errors"].extend(path_errors(model, row, points, known_boxes))
                if model.policy == "preserve":
                    wanted = [points[0]] + [point(p) for p in row["via"]] + [points[-1]]
                    if len(wanted) != len(points) or any(distance(a, b) > EPS for a, b in zip(wanted, points)):
                        report["geometry_errors"].append({"code": "preserved_route_changed", "id": ident})
                else:
                    for p in row.get("via", []):
                        if not any(distance(point(p), q) <= EPS for q in points):
                            report["geometry_errors"].append({"code": "missing_via", "id": ident})
                routes[ident] = simplify(points)
        report.update(route_warnings(routes, model.style["edgeSpacing"]))
        report["label_placement"], warnings, errors = assess_labels(model, routes, label_positions)
        report["warnings"].extend(warnings)
        report["geometry_errors"].extend(errors)
        report["line_jumps"] = {"style": "arc", "size": 6, "proper_crossings": proper_crossings(routes), "render_verified": False}
        if rendered_svg is not None:
            report["render_validation"] = validate_rendered_labels(model, routes, report["label_placement"]["labels"], rendered_svg)
            if report["render_validation"]["status"] != "pass":
                report["errors"].append("rendered SVG label compatibility failed; see render_validation")
    except (DiagramError, ET.ParseError, UnicodeError, RecursionError) as exc:
        report["errors"].append(str(exc))
    return finish_report(report)


def compile_diagram(data):
    report = new_report(data)
    try:
        model = Model(data)
        report["uncertain"] = model.uncertain
        report["geometry_errors"] = model.geometry_errors()
        if report["geometry_errors"]:
            return None, report
        ports = model.ports()
        xml = xml_diagram(model, route_all(model, ports), ports)
        report = validate_diagram(data, xml)
        return (xml if report["status"] == "pass" else None), report
    except (DiagramError, RecursionError) as exc:
        report["errors"].append(str(exc))
        return None, report


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def read_input(path):
    require(path.is_file(), "input file does not exist: " + str(path))
    require(path.stat().st_size <= MAX_BYTES, "input exceeds 10 MB")
    return path.read_text(encoding="utf-8")


def new_paths(outputs, inputs):
    resolved = [p.resolve() for p in outputs + inputs]
    require(len(set(resolved)) == len(resolved), "input/output paths must be distinct")
    for path in outputs:
        require(path.parent.is_dir(), "output parent does not exist: " + str(path.parent))
        require(not path.exists() and not path.is_symlink(), "refusing to overwrite: " + str(path))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Fixed-geometry architecture SDS compiler/validator (stdlib; not a renderer or libavoid). Outputs must be new files. Exit 0 pass, 1 input/validation/routing failure, 2 arguments or output I/O failure.", allow_abbrev=False)
    parser.add_argument("--version", action="version", version=VERSION)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("compile", "validate"):
        sub = commands.add_parser(command, allow_abbrev=False)
        sub.add_argument("--input", type=Path, required=True)
        sub.add_argument("--output" if command == "compile" else "--diagram", type=Path, required=True)
        sub.add_argument("--report", type=Path, required=True)
        if command == "validate":
            sub.add_argument("--rendered-svg", type=Path, help="Read an existing draw.io SVG and check native edge label rendering; never renders")
    args = parser.parse_args(argv)
    try:
        outputs = [args.output, args.report] if args.command == "compile" else [args.report]
        inputs = [args.input] if args.command == "compile" else [args.input, args.diagram]
        if args.command == "validate" and args.rendered_svg is not None:
            inputs.append(args.rendered_svg)
        new_paths(outputs, inputs)
        report = new_report({})
        xml = None
        try:
            data = json.loads(read_input(args.input), object_pairs_hook=unique_object)
            if args.command == "compile":
                xml, report = compile_diagram(data)
            else:
                svg = read_input(args.rendered_svg) if args.rendered_svg is not None else None
                report = validate_diagram(data, read_input(args.diagram), svg)
        except (DiagramError, ValueError, OSError, UnicodeError, RecursionError) as exc:
            report["errors"].append(str(exc))
        if xml is not None:
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(xml)
        with args.report.open("x", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
        print(json.dumps({"status": report["status"], "report": str(args.report)}, ensure_ascii=False))
        return 0 if report["status"] == "pass" else 1
    except (DiagramError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
