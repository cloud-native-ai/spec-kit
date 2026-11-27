#!/usr/bin/env python3
"""build-native.py — deterministic SDS → d3js native HTML builder (layout + routing + labels).

The d3js engine is an absolute-coordinate engine: the SDS carries the logical model,
and with layout_policy=optimize this builder plans the engine geometry, freezes it
back into the SDS, assembles the self-contained HTML (vendor-first D3, byte-identical
delivery.css inline, in-page interactions/exports) and writes a layout report with
quantified geometry (crossings, collinear overlap, label collisions, detours).

Business specifics (which zone sits in which column, per-zone element order, fills)
belong to the CALLER's layout plan JSON — this script contains no private graph data,
no user paths and no server addresses.

Layout plan (all keys optional):
  {
    "columns": [[zone_id, ...], ...],       # top-level zones stacked per column, left→right
    "bands":   [[zone_id, ...], ...],       # top-level zones as horizontal bands below the columns
    "zone_cols": {zone_id: int},            # element grid columns per zone (auto otherwise)
    "zone_order": {zone_id: [element_id, ...]},  # element order inside a zone (input order otherwise)
    "children_layout": {zone_id: "stack"|"row"}, # nested child-zone arrangement (stack default)
    "zone_fill": {top_zone_id: "#rrggbb"},  # top-level fills
    "card": {"w": int, "h": int, "gap_x": int, "gap_y": int},
    "gaps": {"column": int, "row": int, "canvas": int}
  }
Without a plan, top-level zones are grouped into columns by their longest-path rank
over the zone-level relation DAG (a generic fallback; no bands).

Usage:
  build-native.py --sds <sds.json> --out <existing dir> --html <name.html>
                  (--d3-vendor <d3.v7.min.js> | --d3-url <fixed-version-url>)
                  [--layout-plan <plan.json>] [--notes-file <fragment.html>]
                  [--caption <text>] [--source-note <text>] [--report-name <name.json>]

Exit codes: 0 built; 2 usage / invalid SDS / refusing to overwrite; 1 build defect
(layout validation failed and no artifact was claimed).
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import shutil
import sys
from collections import defaultdict
from pathlib import Path

VERSION = "1.0.0"
ENGINE = "d3js"

CARD_W, CARD_H = 188, 46
GAP_X, GAP_Y = 14, 14
PAD, TB, BP, CG = 18, 50, 16, 16
GRID = 2
STUB = 10
LABEL_FONT = 15.0
LABEL_PAD = 12.0
LABEL_H = 20.0
LEGEND_W, LEGEND_H = 318, 246
PALETTE = ["#fff7ed", "#eff6ff", "#f0fdf4", "#faf5ff", "#f8fafc",
           "#fffbeb", "#f5f3ff", "#ecfeff"]

SIDES = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}


class BuildError(Exception):
    pass


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def est_text_width(text, font_size=LABEL_FONT):
    total = 0.0
    for ch in text or "":
        total += font_size * (1.0 if ord(ch) > 127 else 0.6)
    return total


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise BuildError("cannot read JSON %s: %s" % (path, exc))


def validate_sds(sds):
    for key in ("elements", "zones", "relations"):
        if not isinstance(sds.get(key), list):
            raise BuildError("SDS must contain a %s array" % key)
    zones = {}
    for zone in sds["zones"]:
        zid = zone.get("id")
        if not zid or zid in zones:
            raise BuildError("zone id missing or duplicated: %r" % (zid,))
        zones[zid] = zone
    for zone in sds["zones"]:
        parent = zone.get("parent")
        if parent is not None and parent not in zones:
            raise BuildError("zone %s has unknown parent %r" % (zone["id"], parent))
    elements = {}
    for element in sds["elements"]:
        eid = element.get("id")
        if not eid or eid in elements:
            raise BuildError("element id missing or duplicated: %r" % (eid,))
        if element.get("zone") not in zones:
            raise BuildError("element %s references unknown zone %r" % (eid, element.get("zone")))
        elements[eid] = element
    relations = set()
    for relation in sds["relations"]:
        rid = relation.get("id")
        if not rid or rid in relations:
            raise BuildError("relation id missing or duplicated: %r" % (rid,))
        relations.add(rid)
        for side in ("from", "to"):
            endpoint = relation.get(side)
            if endpoint not in elements and endpoint not in zones:
                raise BuildError("relation %s has unknown %s endpoint %r" % (rid, side, endpoint))
    # parent cycle guard
    for zone in sds["zones"]:
        seen = set()
        cur = zone
        while cur.get("parent"):
            if cur["id"] in seen:
                raise BuildError("zone parent cycle at %s" % cur["id"])
            seen.add(cur["id"])
            cur = zones[cur["parent"]]
    return elements, zones


class Layout(object):
    def __init__(self, sds, plan):
        self.sds = sds
        self.plan = plan or {}
        self.elements, self.zones = validate_sds(sds)
        self.children = defaultdict(list)
        self.top_zones = []
        for zone in sds["zones"]:
            if zone.get("parent"):
                self.children[zone["parent"]].append(zone["id"])
            else:
                self.top_zones.append(zone["id"])
        card = self.plan.get("card") or {}
        self.card_w = int(card.get("w", CARD_W))
        self.card_h = int(card.get("h", CARD_H))
        self.gap_x = int(card.get("gap_x", GAP_X))
        self.gap_y = int(card.get("gap_y", GAP_Y))
        gaps = self.plan.get("gaps") or {}
        self.col_gap = int(gaps.get("column", 64))
        self.row_gap = int(gaps.get("row", 24))
        self.canvas_gap = int(gaps.get("canvas", 40))
        self.zone_cols = self.plan.get("zone_cols") or {}
        self.zone_order = self.plan.get("zone_order") or {}
        self.children_layout = self.plan.get("children_layout") or {}
        self.children_order = self.plan.get("children_order") or {}
        for parent, order in self.children_order.items():
            if parent not in self.zones:
                raise BuildError("children_order references unknown zone %s" % parent)
            unknown = [zid for zid in order if zid not in self.children.get(parent, [])]
            if unknown:
                raise BuildError("children_order[%s] lists non-children: %s" % (parent, unknown))
            ordered = list(order)
            extras = [zid for zid in self.children.get(parent, []) if zid not in ordered]
            self.children[parent] = ordered + extras
        self.direct = defaultdict(list)
        for element in sds["elements"]:
            self.direct[element["zone"]].append(element["id"])
        for zone_id in list(self.direct):
            ordered = [eid for eid in (self.zone_order.get(zone_id) or [])
                       if eid in self.direct[zone_id]]
            extras = [eid for eid in self.direct[zone_id] if eid not in ordered]
            self.direct[zone_id] = ordered + extras
        self.box = {}
        self.element_box = {}
        self.legend = {"x": 0, "y": 0, "w": LEGEND_W, "h": LEGEND_H}
        self.warnings = []
        self._validate_plan()

    # -- plan validation -----------------------------------------------------
    def _validate_plan(self):
        columns = self.plan.get("columns")
        bands = self.plan.get("bands")
        if columns is None and bands is None:
            return
        placed = []
        for column in columns or []:
            placed.extend(column)
        for band in bands or []:
            placed.extend(band)
        unknown = [zid for zid in placed if zid not in self.top_zones]
        missing = [zid for zid in self.top_zones if zid not in placed]
        duplicates = sorted({zid for zid in placed if placed.count(zid) > 1})
        if unknown:
            raise BuildError("layout plan references unknown top-level zones: %s" % unknown)
        if missing:
            raise BuildError("layout plan does not place top-level zones: %s" % missing)
        if duplicates:
            raise BuildError("layout plan places zones twice: %s" % duplicates)
        for zone_id, order in self.zone_order.items():
            if zone_id not in self.zones:
                raise BuildError("zone_order references unknown zone %s" % zone_id)
            for eid in order:
                if eid not in self.elements:
                    raise BuildError("zone_order[%s] references unknown element %s" % (zone_id, eid))
                if self.elements[eid]["zone"] != zone_id:
                    raise BuildError("zone_order[%s] lists %s from zone %s"
                                     % (zone_id, eid, self.elements[eid]["zone"]))
        for zone_id in self.children_layout:
            if zone_id not in self.zones:
                raise BuildError("children_layout references unknown zone %s" % zone_id)

    # -- sizing --------------------------------------------------------------
    def auto_cols(self, zone_id):
        count = len(self.direct[zone_id])
        if zone_id in self.zone_cols:
            return max(1, int(self.zone_cols[zone_id]))
        if count <= 1:
            return 1
        if count <= 4:
            return 2
        return 3

    def measure(self, zone_id):
        cols = self.auto_cols(zone_id)
        count = len(self.direct[zone_id])
        card_w, card_h = self.card_w, self.card_h
        cards_w = cols * card_w + (cols - 1) * self.gap_x if count else 0
        rows = int(math.ceil(count / float(cols))) if count else 0
        direct_h = rows * card_h + (rows - 1) * self.gap_y if rows else 0
        child_ids = self.children.get(zone_id, [])
        layout_mode = self.children_layout.get(zone_id, "stack")
        content_w, content_h = cards_w, direct_h
        sizes = [(child, self.measure(child)) for child in child_ids]
        if sizes:
            if layout_mode == "row":
                row_w = sum(size[0] for _, size in sizes) + self.gap_x * (len(sizes) - 1)
                content_w = max(content_w, row_w)
                content_h += CG + max(size[1] for _, size in sizes)
            else:
                content_w = max([content_w] + [size[0] for _, size in sizes])
                content_h += sum(CG + size[1] for _, size in sizes)
        size = (content_w + 2 * PAD, TB + content_h + BP)
        self._size = getattr(self, "_size", {})
        self._size[zone_id] = size
        self._content = getattr(self, "_content", {})
        self._content[zone_id] = (content_w, content_h)
        return size

    def place(self, zone_id, x, y):
        width, height = self._size[zone_id]
        self.box[zone_id] = {"x": x, "y": y, "w": width, "h": height}
        cols = self.auto_cols(zone_id)
        count = len(self.direct[zone_id])
        for index, eid in enumerate(self.direct[zone_id]):
            row, col = divmod(index, cols)
            self.element_box[eid] = {"x": x + PAD + col * (self.card_w + self.gap_x),
                                     "y": y + TB + row * (self.card_h + self.gap_y),
                                     "w": self.card_w, "h": self.card_h}
        cursor_y = y + TB
        if count:
            rows = int(math.ceil(count / float(cols)))
            cursor_y += rows * self.card_h + (rows - 1) * self.gap_y
        content_w, _ = self._content[zone_id]
        child_ids = self.children.get(zone_id, [])
        layout_mode = self.children_layout.get(zone_id, "stack")
        if layout_mode == "row":
            cursor_y += CG
            row_width = (sum(self._size[child][0] for child in child_ids)
                         + self.gap_x * (len(child_ids) - 1)) if child_ids else 0
            cursor_x = x + PAD + max(0, (content_w - row_width) // 2)
            for child in child_ids:
                self.place(child, cursor_x, cursor_y)
                cursor_x += self._size[child][0] + self.gap_x
        else:
            for child in child_ids:
                child_w = self._size[child][0]
                cursor_y += CG
                self.place(child, x + PAD + (content_w - child_w) // 2, cursor_y)
                cursor_y += self._size[child][1]
        return self.box[zone_id]

    def fallback_columns(self):
        """Rank top-level zones by longest path over zone-level relation edges."""
        top_of = {}
        for element in self.sds["elements"]:
            zid = element["zone"]
            while self.zones[zid].get("parent"):
                zid = self.zones[zid]["parent"]
            top_of[element["id"]] = zid
        rank = {zid: 0 for zid in self.top_zones}
        def top_zd(endpoint):
            if endpoint in top_of:
                return top_of[endpoint]
            if endpoint in self.zones:
                zid = endpoint
                while self.zones[zid].get("parent"):
                    zid = self.zones[zid]["parent"]
                return zid
            return None

        edges = set()
        for relation in self.sds["relations"]:
            ends = [top_zd(relation["from"]), top_zd(relation["to"])]
            if ends[0] and ends[1] and ends[0] != ends[1]:
                edges.add((ends[0], ends[1]))
        changed = True
        guard = 0
        while changed and guard < len(self.top_zones) + 1:
            changed = False
            guard += 1
            for source, target in sorted(edges):
                if rank[target] < rank[source] + 1:
                    rank[target] = rank[source] + 1
                    changed = True
        grouped = defaultdict(list)
        for zid in self.top_zones:
            grouped[rank[zid]].append(zid)
        return [grouped[key] for key in sorted(grouped)]

    def compute(self):
        for zone_id in self.top_zones:
            self.measure(zone_id)
        columns = self.plan.get("columns") or self.fallback_columns()
        bands = self.plan.get("bands") or []
        margin = self.canvas_gap
        x = margin
        y = margin
        bottom = margin
        for column in columns:
            column_width = 0
            column_y = margin
            for zone_id in column:
                self.place(zone_id, x, column_y)
                column_y += self._size[zone_id][1] + self.row_gap
                column_width = max(column_width, self._size[zone_id][0])
            bottom = max(bottom, column_y - self.row_gap)
            x += column_width + self.col_gap
        band_y = bottom + self.row_gap if bands else bottom
        for band in bands:
            band_x = margin
            band_height = 0
            for zone_id in band:
                self.place(zone_id, band_x, band_y)
                band_x += self._size[zone_id][0] + self.gap_x
                band_height = max(band_height, self._size[zone_id][1])
            band_y += band_height + self.row_gap
            bottom = band_y - self.row_gap
        right = margin + max(
            [box["x"] + box["w"] for box in self.box.values()] + [0])
        # legend below the whole drawing (deterministic, collision-free)
        self.legend = {"x": margin, "y": bottom + self.row_gap,
                       "w": LEGEND_W, "h": LEGEND_H}
        canvas_w = max(right, margin + LEGEND_W) + margin
        canvas_h = self.legend["y"] + self.legend["h"] + margin
        return canvas_w, canvas_h

    # -- helpers -------------------------------------------------------------
    def zone_chain(self, zone_id):
        chain = [zone_id]
        while self.zones[zone_id].get("parent"):
            zone_id = self.zones[zone_id]["parent"]
            chain.append(zone_id)
        return chain

    def elem_chain(self, element_id):
        return self.zone_chain(self.elements[element_id]["zone"])

    def top_zone(self, zone_id):
        while self.zones[zone_id].get("parent"):
            zone_id = self.zones[zone_id]["parent"]
        return zone_id

    def box_of(self, ident):
        return self.element_box[ident] if ident in self.element_box else self.box[ident]

    def kind_of(self, ident):
        return "element" if ident in self.element_box else "zone"

    def zone_fill(self, top_zone, index):
        return (self.plan.get("zone_fill") or {}).get(top_zone) or PALETTE[index % len(PALETTE)]


# ---------------------------------------------------------------- routing utils

def spread_slots(desired, low, high, min_gap=18):
    count = len(desired)
    if count == 0:
        return {}
    order = sorted(range(count), key=lambda i: desired[i])
    pos = [max(low, min(high, desired[i])) for i in range(count)]
    for _ in range(80):
        changed = False
        for k in range(1, count):
            i, j = order[k - 1], order[k]
            if pos[j] - pos[i] < min_gap:
                mid = (pos[i] + pos[j]) / 2
                pos[i] = mid - min_gap / 2
                pos[j] = mid + min_gap / 2
                changed = True
        for k in range(count):
            pos[k] = max(low, min(high, pos[k]))
        if not changed:
            break
    return {idx: int(round(pos[idx] / 2) * 2) for idx in range(count)}


def side_point(rect, side, coord):
    if side == "E":
        return (rect["x"] + rect["w"], coord)
    if side == "W":
        return (rect["x"], coord)
    if side == "N":
        return (coord, rect["y"])
    return (coord, rect["y"] + rect["h"])


def side_span(rect, side):
    if side in ("N", "S"):
        return rect["x"], rect["x"] + rect["w"]
    return rect["y"], rect["y"] + rect["h"]


def facing_side(a, b):
    ax, ay = a["x"] + a["w"] / 2, a["y"] + a["h"] / 2
    bx, by = b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
    dx, dy = bx - ax, by - ay
    if abs(dx) >= abs(dy):
        return "E" if dx > 0 else "W"
    return "S" if dy > 0 else "N"


def attach_side(rect, other):
    ocx, ocy = other["x"] + other["w"] / 2, other["y"] + other["h"] / 2
    if ocy < rect["y"]:
        return "N"
    if ocy > rect["y"] + rect["h"]:
        return "S"
    if ocx < rect["x"]:
        return "W"
    if ocx > rect["x"] + rect["w"]:
        return "E"
    dx = min(ocx - rect["x"], rect["x"] + rect["w"] - ocx)
    dy = min(ocy - rect["y"], rect["y"] + rect["h"] - ocy)
    return "W" if dx < dy else "N"


def snap_free_coord(value):
    return int(round(value / float(GRID)) * GRID)


def snap_point(point, side):
    if side in ("E", "W"):
        return (point[0], snap_free_coord(point[1]))
    return (snap_free_coord(point[0]), point[1])


def normalize_orthogonal(points):
    """Insert elbows so every consecutive pair is axis-aligned; returns (points, inserted)."""
    if not points:
        return points, 0
    out = [points[0]]
    inserted = 0
    for point in points[1:]:
        last = out[-1]
        if point[0] != last[0] and point[1] != last[1]:
            out.append((point[0], last[1]))
            inserted += 1
        out.append(point)
    return out, inserted


def simplify(points, eps=0.5):
    out = []
    for point in points:
        if out and abs(out[-1]["x"] - point[0]) < eps and abs(out[-1]["y"] - point[1]) < eps:
            continue
        out.append({"x": point[0], "y": point[1]})
    changed = True
    while changed and len(out) >= 3:
        changed = False
        result = [out[0]]
        for index in range(1, len(out) - 1):
            a, b, c = result[-1], out[index], out[index + 1]
            if (a["x"] == b["x"] == c["x"]) or (a["y"] == b["y"] == c["y"]):
                changed = True
                continue
            result.append(b)
        result.append(out[-1])
        out = result
    return out


def rect_blocks_segment(rect, p, q):
    x0, y0, x1, y1 = rect["x"], rect["y"], rect["x"] + rect["w"], rect["y"] + rect["h"]
    if p["y"] == q["y"]:
        y = p["y"]
        lo, hi = min(p["x"], q["x"]), max(p["x"], q["x"])
        return y0 < y < y1 and max(lo, x0) < min(hi, x1)
    if p["x"] == q["x"]:
        x = p["x"]
        lo, hi = min(p["y"], q["y"]), max(p["y"], q["y"])
        return x0 < x < x1 and max(lo, y0) < min(hi, y1)
    return False


def seg_intersection(a, b, c, d):
    ah = a["y"] == b["y"]
    ch = c["y"] == d["y"]
    if ah == ch:
        return None
    if not ah:
        a, b, c, d = c, d, a, b
    y = a["y"]
    ax0, ax1 = min(a["x"], b["x"]), max(a["x"], b["x"])
    x = c["x"]
    cy0, cy1 = min(c["y"], d["y"]), max(c["y"], d["y"])
    if ax0 < x < ax1 and cy0 < y < cy1:
        return {"x": x, "y": y}
    return None


class Router(object):
    def __init__(self, layout, canvas_w, canvas_h):
        self.layout = layout
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.W = canvas_w // GRID + 2
        self.H = canvas_h // GRID + 2
        self.base = self._base_block()
        self.top_ids = layout.top_zones
        self.nested_ids = [zid for zid in layout.zones if layout.zones[zid].get("parent")]

    def _fill(self, array, rect, inflate, value):
        x0 = max(0, int((rect["x"] - inflate) // GRID))
        y0 = max(0, int((rect["y"] - inflate) // GRID))
        x1 = min(self.W - 1, int((rect["x"] + rect["w"] + inflate) // GRID))
        y1 = min(self.H - 1, int((rect["y"] + rect["h"] + inflate) // GRID))
        row = bytes([value]) * (x1 - x0 + 1)
        for iy in range(y0, y1 + 1):
            array[iy * self.W + x0: iy * self.W + x1 + 1] = row

    def _base_block(self):
        base = bytearray(self.W * self.H)
        for box in self.layout.element_box.values():
            self._fill(base, box, 2, 1)
        for zid, box in self.layout.box.items():
            zone = self.layout.zones[zid]
            depth = 0
            cur = zid
            while self.layout.zones[cur].get("parent"):
                depth += 1
                cur = self.layout.zones[cur]["parent"]
            font = 19 if depth == 0 else 16
            label = zone.get("label") or ""
            width = sum(font * (0.98 if ord(ch) > 127 else 0.6) for ch in label) + 24
            self._fill(base, {"x": box["x"] + 12, "y": box["y"] + 6, "w": int(width), "h": 30}, 2, 1)
        self._fill(base, self.layout.legend, 4, 1)
        return base

    def _blocked_for(self, plan, corridor):
        blocked = bytearray(self.base)
        if corridor:
            for zid in self.top_ids:
                self._fill(blocked, self.layout.box[zid], 3, 1)
            return blocked
        passable = set()
        for side, kind, ident in (("src", plan["ks"], plan["src"]), ("dst", plan["kd"], plan["dst"])):
            if kind == "element":
                passable.update(self.layout.elem_chain(ident))
            else:
                passable.update(self.layout.zone_chain(ident)[1:])
        for zid in self.nested_ids:
            if zid not in passable:
                self._fill(blocked, self.layout.box[zid], 2, 1)
        return blocked

    def _region(self, zone_id, shrink=0):
        box = self.layout.box[zone_id]
        return (int((box["x"] + shrink) // GRID), int((box["y"] + shrink) // GRID),
                int((box["x"] + box["w"] - shrink) // GRID),
                int((box["y"] + box["h"] - shrink) // GRID))

    def _union_region(self, plan):
        a = self.layout.box[plan["ts"]]
        b = self.layout.box[plan["td"]]
        x0 = max(0, int((min(a["x"], b["x"]) - 10) // GRID))
        y0 = max(0, int((min(a["y"], b["y"]) - 10) // GRID))
        x1 = min(self.W - 1, int((max(a["x"] + a["w"], b["x"] + b["w"]) + 10) // GRID))
        y1 = min(self.H - 1, int((max(a["y"] + a["h"], b["y"] + b["h"]) + 10) // GRID))
        return (x0, y0, x1, y1)

    def astar(self, start, goal, blocked, region, turn_cost, occ, occ_pen, max_exp=600000):
        sx, sy = (max(region[0], min(region[2], int(round(start[0] / GRID)))),
                  max(region[1], min(region[3], int(round(start[1] / GRID)))))
        gx, gy = (max(region[0], min(region[2], int(round(goal[0] / GRID)))),
                  max(region[1], min(region[3], int(round(goal[1] / GRID)))))

        def free(ix, iy):
            if ix < region[0] or ix > region[2] or iy < region[1] or iy > region[3]:
                return False
            return not blocked[iy * self.W + ix]

        if not free(sx, sy):
            sx, sy = self._nearest_free(sx, sy, free, region)
        if not free(gx, gy):
            gx, gy = self._nearest_free(gx, gy, free, region)
        if not free(sx, sy) or not free(gx, gy):
            return None

        import heapq
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        start_state = (sx, sy, 4)
        seen = {start_state: 0.0}
        parent = {}
        heap = [(abs(sx - gx) + abs(sy - gy), 0.0, start_state)]
        goal_state = None
        expansions = 0
        while heap:
            _, gcur, state = heapq.heappop(heap)
            if seen.get(state, 1e18) < gcur:
                continue
            expansions += 1
            if expansions > max_exp:
                return None
            ix, iy, direction = state
            if ix == gx and iy == gy:
                goal_state = state
                break
            for nd, (dx, dy) in enumerate(directions):
                if direction != 4 and nd == (direction + 2) % 4:
                    continue
                nx, ny = ix + dx, iy + dy
                if not free(nx, ny):
                    continue
                cost = 1.0
                if direction != 4 and nd != direction:
                    cost += turn_cost
                if occ is not None:
                    cost += occ_pen * occ[ny * self.W + nx]
                ng = gcur + cost
                ns = (nx, ny, nd)
                if ng < seen.get(ns, 1e18) - 1e-9:
                    seen[ns] = ng
                    parent[ns] = state
                    heapq.heappush(heap, (ng + abs(nx - gx) + abs(ny - gy), ng, ns))
        if goal_state is None:
            return None
        path = []
        state = goal_state
        while state != start_state:
            path.append((state[0], state[1]))
            state = parent[state]
        path.append((sx, sy))
        path.reverse()
        return [(ix * GRID, iy * GRID) for ix, iy in path]

    @staticmethod
    def _nearest_free(ix, iy, free, region, radius=8):
        for radius in range(1, radius + 1):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    nx, ny = ix + dx, iy + dy
                    if region[0] <= nx <= region[2] and region[1] <= ny <= region[3] and free(nx, ny):
                        return nx, ny
        return ix, iy

    def route(self):
        layout = self.layout
        plans = []
        for relation in layout.sds["relations"]:
            source, target = relation["from"], relation["to"]
            kind_s, kind_t = layout.kind_of(source), layout.kind_of(target)
            top_s = layout.top_zone(layout.elements[source]["zone"]) if kind_s == "element" else layout.top_zone(source)
            top_t = layout.top_zone(layout.elements[target]["zone"]) if kind_t == "element" else layout.top_zone(target)
            plans.append({"rel": relation, "src": source, "dst": target,
                          "ks": kind_s, "kd": kind_t, "ts": top_s, "td": top_t,
                          "cross": top_s != top_t})
        # endpoint sides
        side_pick = {}
        for plan in plans:
            sbox = layout.box_of(plan["src"])
            dbox = layout.box_of(plan["dst"])
            side_pick[(plan["rel"]["id"], "src")] = facing_side(sbox, dbox)
            side_pick[(plan["rel"]["id"], "dst")] = facing_side(dbox, sbox)
        # cross-zone gates
        gate_groups = defaultdict(list)
        for plan in plans:
            if not plan["cross"]:
                continue
            ts_box, td_box = layout.box[plan["ts"]], layout.box[plan["td"]]
            plan["sside"] = facing_side(ts_box, td_box)
            plan["dside"] = facing_side(td_box, ts_box)
            sbox, dbox = layout.box_of(plan["src"]), layout.box_of(plan["dst"])
            sdes = (sbox["x"] + sbox["w"] / 2) if plan["sside"] in ("N", "S") else (sbox["y"] + sbox["h"] / 2)
            ddes = (dbox["x"] + dbox["w"] / 2) if plan["dside"] in ("N", "S") else (dbox["y"] + dbox["h"] / 2)
            gate_groups[(plan["ts"], plan["sside"])].append((plan["rel"]["id"], sdes))
            gate_groups[(plan["td"], plan["dside"])].append((plan["rel"]["id"], ddes))
        gate_spacing = {}

        def assign_gate_slots(desired_by_key):
            slots_out = {}
            for (zone_id, side), items in desired_by_key.items():
                low, high = side_span(layout.box[zone_id], side)
                low2, high2 = low + 26, high - 26
                if high2 < low2:
                    low2, high2 = low + 6, high - 6
                ordered = sorted(items, key=lambda item: item[1])
                positioned = spread_slots([item[1] for item in ordered], low2, high2, min_gap=26)
                for index, (rid, _) in enumerate(ordered):
                    slots_out[(rid, zone_id, side)] = positioned[index]
            return slots_out

        # First pass orders gates by the partner endpoint's projection. A second
        # "aim at the partner gate" pass was tried and dropped: it made gate index
        # order disagree between the two sides, which raised corridor crossings.
        slot = assign_gate_slots(gate_groups)
        for (zone_id, side), items in gate_groups.items():
            values = sorted(slot[(rid, zone_id, side)] for rid, _ in items)
            deltas = [values[i + 1] - values[i] for i in range(len(values) - 1)]
            gate_spacing["%s/%s" % (zone_id, side)] = min(deltas) if deltas else None
        for plan in plans:
            if not plan["cross"]:
                continue
            rid = plan["rel"]["id"]
            plan["sport"] = side_point(layout.box[plan["ts"]], plan["sside"],
                                       slot[(rid, plan["ts"], plan["sside"])])
            plan["dport"] = side_point(layout.box[plan["td"]], plan["dside"],
                                       slot[(rid, plan["td"], plan["dside"])])
        # element anchor slots
        anchor_groups = defaultdict(list)
        for plan in plans:
            if plan["ks"] == "element":
                anchor_groups[(plan["src"], side_pick[(plan["rel"]["id"], "src")])].append((plan["rel"]["id"], "src"))
            if plan["kd"] == "element":
                anchor_groups[(plan["dst"], side_pick[(plan["rel"]["id"], "dst")])].append((plan["rel"]["id"], "dst"))
        anchor_pos = {}
        for (eid, side), items in anchor_groups.items():
            rect = layout.element_box[eid]
            low, high = side_span(rect, side)
            low2, high2 = low + 7, high - 7

            def desired(item):
                rid, role = item
                plan = next(p for p in plans if p["rel"]["id"] == rid)
                other = plan["dst"] if role == "src" else plan["src"]
                obox = layout.box_of(other)
                return (obox["x"] + obox["w"] / 2) if side in ("N", "S") else (obox["y"] + obox["h"] / 2)

            ordered = sorted(items, key=desired)
            slots = spread_slots([desired(item) for item in ordered], low2, high2, min_gap=10)
            for index, item in enumerate(ordered):
                anchor_pos[(item[0], item[1])] = slots[index]
        zone_attach = {}
        for plan in plans:
            rid = plan["rel"]["id"]
            if plan["ks"] == "zone":
                box = layout.box[plan["src"]]
                other = layout.box_of(plan["dst"])
                side = attach_side(box, other)
                low, high = side_span(box, side)
                coord = other["x"] + other["w"] / 2 if side in ("N", "S") else other["y"] + other["h"] / 2
                zone_attach[(rid, "src")] = (side, max(low + 12, min(high - 12, coord)))
            if plan["kd"] == "zone":
                box = layout.box[plan["dst"]]
                other = layout.box_of(plan["src"])
                side = attach_side(box, other)
                low, high = side_span(box, side)
                coord = other["x"] + other["w"] / 2 if side in ("N", "S") else other["y"] + other["h"] / 2
                zone_attach[(rid, "dst")] = (side, max(low + 12, min(high - 12, coord)))
        for plan in plans:
            rid = plan["rel"]["id"]
            if plan["ks"] == "element":
                plan["sside_final"] = side_pick[(rid, "src")]
                plan["sanchor"] = snap_point(
                    side_point(layout.element_box[plan["src"]],
                               plan["sside_final"], anchor_pos[(rid, "src")]),
                    plan["sside_final"])
            else:
                side, coord = zone_attach[(rid, "src")]
                plan["sside_final"] = side
                plan["sanchor"] = snap_point(side_point(layout.box[plan["src"]], side, coord), side)
            if plan["kd"] == "element":
                plan["dside_final"] = side_pick[(rid, "dst")]
                plan["danchor"] = snap_point(
                    side_point(layout.element_box[plan["dst"]],
                               plan["dside_final"], anchor_pos[(rid, "dst")]),
                    plan["dside_final"])
            else:
                side, coord = zone_attach[(rid, "dst")]
                plan["dside_final"] = side
                plan["danchor"] = snap_point(side_point(layout.box[plan["dst"]], side, coord), side)

        def stub(anchor, side, distance=STUB):
            dx, dy = SIDES[side]
            return (anchor[0] + dx * distance, anchor[1] + dy * distance)

        # deconflict anchor stubs: two facing stubs on the same line overlap pixel-for-pixel
        # and would register as collinear shared segments. Shift the later edge's anchor by
        # 4 px along its border (inside the element/zone box) before routing.
        def anchor_of(plan, role):
            return plan["sanchor"] if role == "src" else plan["danchor"]

        def side_of(plan, role):
            return plan["sside_final"] if role == "src" else plan["dside_final"]

        def stub_segment(plan, role):
            anchor = anchor_of(plan, role)
            side = side_of(plan, role)
            dx, dy = SIDES[side]
            return anchor, (anchor[0] + dx * STUB, anchor[1] + dy * STUB), side

        def segments_overlap(seg_a, seg_b):
            (a0, a1, side_a) = seg_a
            (b0, b1, side_b) = seg_b
            horizontal = side_a in ("E", "W") and side_b in ("E", "W")
            vertical = side_a in ("N", "S") and side_b in ("N", "S")
            if not (horizontal or vertical):
                return False
            if horizontal:
                if a0[1] != b0[1]:
                    return False
                lo_a, hi_a = sorted((a0[0], a1[0]))
                lo_b, hi_b = sorted((b0[0], b1[0]))
            else:
                if a0[0] != b0[0]:
                    return False
                lo_a, hi_a = sorted((a0[1], a1[1]))
                lo_b, hi_b = sorted((b0[1], b1[1]))
            return min(hi_a, hi_b) - max(lo_a, lo_b) > 2

        def nudge(plan, role, delta):
            side = side_of(plan, role)
            box = layout.box_of(plan["src"] if role == "src" else plan["dst"])
            ax, ay = anchor_of(plan, role)
            if side in ("E", "W"):
                ay = max(box["y"] + 7, min(box["y"] + box["h"] - 7, ay + delta))
            else:
                ax = max(box["x"] + 7, min(box["x"] + box["w"] - 7, ax + delta))
            if role == "src":
                plan["sanchor"] = (ax, ay)
            else:
                plan["danchor"] = (ax, ay)

        stub_shifts = []
        for i in range(len(plans)):
            for j in range(i + 1, len(plans)):
                for role_a in ("src", "dst"):
                    for role_b in ("src", "dst"):
                        if not segments_overlap(stub_segment(plans[i], role_a),
                                                stub_segment(plans[j], role_b)):
                            continue
                        side = side_of(plans[j], role_b)
                        box = layout.box_of(plans[j]["src"] if role_b == "src" else plans[j]["dst"])
                        free = (anchor_of(plans[j], role_b)[1] if side in ("E", "W")
                                else anchor_of(plans[j], role_b)[0])
                        low, high = ((box["y"] + 7, box["y"] + box["h"] - 7) if side in ("E", "W")
                                     else (box["x"] + 7, box["x"] + box["w"] - 7))
                        for delta in (4, -4, 8, -8):
                            if low <= free + delta <= high:
                                nudge(plans[j], role_b, delta)
                                stub_shifts.append({"edge": plans[j]["rel"]["id"],
                                                    "role": role_b, "delta": delta})
                                break
        self.stub_shifts = stub_shifts

        # lanes for cross-zone corridors
        lane_groups = defaultdict(list)
        for plan in plans:
            if not plan["cross"]:
                continue
            pair = tuple(sorted([plan["ts"], plan["td"]]))
            orientation = "v" if plan["sside"] in ("E", "W") else "h"
            lane_groups[(pair, orientation)].append(plan)
        for (pair, orientation), group in lane_groups.items():
            box_a, box_b = layout.box[pair[0]], layout.box[pair[1]]
            if orientation == "v":
                left = pair[0] if box_a["x"] <= box_b["x"] else pair[1]
                right = pair[1] if left == pair[0] else pair[0]
                low = layout.box[left]["x"] + layout.box[left]["w"] + 8
                high = layout.box[right]["x"] - 8
                group.sort(key=lambda p: (p["sport"][1] + p["dport"][1]) / 2.0)
            else:
                top = pair[0] if box_a["y"] <= box_b["y"] else pair[1]
                bottom = pair[1] if top == pair[0] else pair[0]
                low = layout.box[top]["y"] + layout.box[top]["h"] + 8
                high = layout.box[bottom]["y"] - 8
                group.sort(key=lambda p: (p["sport"][0] + p["dport"][0]) / 2.0)
            count = len(group)
            for index, plan in enumerate(group):
                lane = low + (high - low) * (index + 1) / (count + 1.0)
                plan["lane"] = int(round(lane / 2) * 2)
                plan["orient"] = orientation

        def corridor_poly(plan):
            sp, dp = plan["sport"], plan["dport"]
            lane = plan["lane"]
            if plan["orient"] == "v":
                return [sp, (lane, sp[1]), (lane, dp[1]), dp]
            return [sp, (sp[0], lane), (dp[0], lane), dp]

        def corridor_hits(plan):
            hits = []
            poly = corridor_poly(plan)
            for index in range(len(poly) - 1):
                a, b = poly[index], poly[index + 1]
                pa = {"x": a[0], "y": a[1]}
                pb = {"x": b[0], "y": b[1]}
                for eid, box in layout.element_box.items():
                    if rect_blocks_segment(box, pa, pb):
                        hits.append(eid)
            return sorted(set(hits))

        corridor_notes = {"straight": [], "adjusted": [], "fallback": []}
        for plan in plans:
            if not plan["cross"]:
                continue
            rid = plan["rel"]["id"]
            hits = corridor_hits(plan)
            if not hits:
                corridor_notes["straight"].append(rid)
                continue
            fixed = False
            for role in ("src", "dst"):
                zone_id = plan["ts"] if role == "src" else plan["td"]
                side = plan["sside"] if role == "src" else plan["dside"]
                other = plan["dport"] if role == "src" else plan["sport"]
                coord = other[1] if side in ("N", "S") else other[0]
                low, high = side_span(layout.box[zone_id], side)
                if high - 12 < low + 12:
                    continue
                coord = snap_free_coord(max(low + 12, min(high - 12, coord)))
                old = plan["sport"] if role == "src" else plan["dport"]
                plan["sport" if role == "src" else "dport"] = side_point(
                    layout.box[zone_id], side, coord)
                if not corridor_hits(plan):
                    fixed = True
                    corridor_notes["adjusted"].append(
                        {"edge": rid, "moved": role, "cards": hits})
                    break
                plan["sport" if role == "src" else "dport"] = old
            if not fixed:
                plan["corridor_fallback"] = True
                corridor_notes["fallback"].append({"edge": rid, "cards": hits})
        self.corridor_notes = corridor_notes

        occ = bytearray(self.W * self.H)
        routes = {}
        failures = []

        def mark(poly):
            for i in range(len(poly) - 1):
                a, b = poly[i], poly[i + 1]
                x0, x1 = sorted((a["x"], b["x"]))
                y0, y1 = sorted((a["y"], b["y"]))
                for gx in range(int(x0 // GRID), int(x1 // GRID) + 1):
                    for gy in range(int(y0 // GRID), int(y1 // GRID) + 1):
                        occ[gy * self.W + gx] = min(3, occ[gy * self.W + gx] + 1)

        for plan in plans:
            rid = plan["rel"]["id"]
            s_stub = stub(plan["sanchor"], plan["sside_final"])
            d_stub = stub(plan["danchor"], plan["dside_final"])
            poly = [plan["sanchor"], s_stub, d_stub, plan["danchor"]]
            ok = False
            for attempt in range(4):
                turn_cost = (20, 14, 10, 6)[attempt]
                occ_pen = (16, 10, 4, 0)[attempt]
                if plan["cross"] and not plan.get("corridor_fallback"):
                    sp, dp = plan["sport"], plan["dport"]
                    lane = plan["lane"]
                    if plan["orient"] == "v":
                        corridor = [sp, (lane, sp[1]), (lane, dp[1]), dp]
                    else:
                        corridor = [sp, (sp[0], lane), (dp[0], lane), dp]
                    p1 = self.astar(s_stub, sp, self._blocked_for(plan, False), self._region(plan["ts"]),
                                    turn_cost, occ, occ_pen)
                    p3 = self.astar(dp, d_stub, self._blocked_for(plan, False), self._region(plan["td"]),
                                    turn_cost, occ, occ_pen)
                    if p1 and p3:
                        poly = [plan["sanchor"], s_stub] + p1 + corridor + p3 + [plan["danchor"]]
                        ok = True
                        break
                elif plan["cross"]:
                    p1 = self.astar(s_stub, d_stub, self._blocked_for(plan, False),
                                    self._union_region(plan), turn_cost, occ, occ_pen)
                    if p1:
                        poly = [plan["sanchor"]] + p1 + [plan["danchor"]]
                        ok = True
                        break
                else:
                    p1 = self.astar(s_stub, d_stub, self._blocked_for(plan, False), self._region(plan["ts"]),
                                    turn_cost, occ, occ_pen)
                    if p1:
                        poly = [plan["sanchor"], s_stub] + p1 + [plan["danchor"]]
                        ok = True
                        break
            if not ok:
                failures.append(rid)
            poly, elbows = normalize_orthogonal([(p[0], p[1]) for p in poly])
            self.elbows = getattr(self, "elbows", 0) + elbows
            poly = simplify(poly)
            poly, elbows2 = normalize_orthogonal([(p["x"], p["y"]) for p in poly])
            self.elbows += elbows2
            poly = simplify(poly)
            routes[rid] = poly
            mark(poly)
        return plans, routes, failures, gate_spacing


def route_metrics(routes):
    ids = sorted(routes)
    crossings = []
    collinear = []
    total_collinear = 0.0
    non_orthogonal = []
    for rid in ids:
        poly = routes[rid]
        if any(poly[k]["x"] != poly[k + 1]["x"] and poly[k]["y"] != poly[k + 1]["y"]
               for k in range(len(poly) - 1)):
            non_orthogonal.append(rid)
    for i in range(len(ids)):
        ri = routes[ids[i]]
        for j in range(i + 1, len(ids)):
            rj = routes[ids[j]]
            for ai in range(len(ri) - 1):
                for bj in range(len(rj) - 1):
                    point = seg_intersection(ri[ai], ri[ai + 1], rj[bj], rj[bj + 1])
                    if point:
                        crossings.append({"a": ids[i], "b": ids[j], **point})
            for ai in range(len(ri) - 1):
                a, b = ri[ai], ri[ai + 1]
                for bj in range(len(rj) - 1):
                    c, d = rj[bj], rj[bj + 1]
                    if a["y"] == b["y"] == c["y"] == d["y"]:
                        lo = max(min(a["x"], b["x"]), min(c["x"], d["x"]))
                        hi = min(max(a["x"], b["x"]), max(c["x"], d["x"]))
                        if hi - lo > 2:
                            total_collinear += hi - lo
                            collinear.append({"a": ids[i], "b": ids[j], "axis": "h",
                                              "at": a["y"], "length": round(hi - lo, 1)})
                    elif a["x"] == b["x"] == c["x"] == d["x"]:
                        lo = max(min(a["y"], b["y"]), min(c["y"], d["y"]))
                        hi = min(max(a["y"], b["y"]), max(c["y"], d["y"]))
                        if hi - lo > 2:
                            total_collinear += hi - lo
                            collinear.append({"a": ids[i], "b": ids[j], "axis": "v",
                                              "at": a["x"], "length": round(hi - lo, 1)})
    return {"crossings": crossings, "collinear": collinear,
            "collinear_total_px": round(total_collinear, 1),
            "non_orthogonal_routes": non_orthogonal}


def place_labels(layout, routes, legend):
    relations = layout.sds["relations"]
    element_boxes = dict(layout.element_box)
    zone_label_boxes = []
    for zid, box in layout.box.items():
        label = layout.zones[zid].get("label") or ""
        depth = 0
        cur = zid
        while layout.zones[cur].get("parent"):
            depth += 1
            cur = layout.zones[cur]["parent"]
        font = 19 if depth == 0 else 16
        width = sum(font * (0.98 if ord(ch) > 127 else 0.6) for ch in label) + 12
        zone_label_boxes.append({"x": box["x"] + 12, "y": box["y"] + 6,
                                 "w": width, "h": 30})
    placed = []
    results = {}
    issues = []
    for relation in relations:
        if not relation.get("label"):
            continue
        rid = relation["id"]
        route = routes[rid]
        segments = []
        for index in range(len(route) - 1):
            a, b = route[index], route[index + 1]
            length = abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])
            if length >= 30:
                segments.append((length, a, b))
        segments.sort(key=lambda item: -item[0])
        text = relation["label"]
        width = est_text_width(text, LABEL_FONT) + LABEL_PAD
        height = LABEL_H
        best = None
        for length, a, b in segments:
            horizontal = a["y"] == b["y"]
            for fraction in (0.5, 0.35, 0.65, 0.25, 0.75, 0.15, 0.85):
                px = a["x"] + (b["x"] - a["x"]) * fraction
                py = a["y"] + (b["y"] - a["y"]) * fraction
                offsets = ((12, 20, 28) if horizontal
                           else (width / 2.0 + 10, width / 2.0 + 22))
                for signed in (-1, 1):
                    for offset in offsets:
                        if horizontal:
                            cx, cy = px, py + signed * offset
                        else:
                            cx, cy = px + signed * offset, py
                        cx = int(round(cx))
                        cy = int(round(cy))
                        rect = {"x": cx - width / 2, "y": cy - 14, "w": width, "h": height}
                        candidate = {"edge": rid, "text": text, "x": cx, "y": cy, "rect": rect}
                        collision = None
                        for eid, box in element_boxes.items():
                            if rect_overlap(rect, box, 2):
                                collision = {"type": "card", "id": eid}
                                break
                        if collision is None:
                            for box in zone_label_boxes:
                                if rect_overlap(rect, box, 2):
                                    collision = {"type": "zone-label"}
                                    break
                        if collision is None and rect_overlap(rect, legend, 4):
                            collision = {"type": "legend"}
                        if collision is None:
                            for other in placed:
                                if rect_overlap(rect, other["rect"], 4):
                                    collision = {"type": "label", "id": other["edge"]}
                                    break
                        if collision is None:
                            for other_id, poly in routes.items():
                                for k in range(len(poly) - 1):
                                    if rect_blocks_segment(rect, poly[k], poly[k + 1]):
                                        collision = {"type": "edge", "id": other_id}
                                        break
                                if collision:
                                    break
                        if collision is None:
                            best = candidate
                            break
                    if best:
                        break
                if best:
                    break
            if best:
                break
        if best is None and segments:
            length, a, b = segments[0]
            horizontal = a["y"] == b["y"]
            cx = int(round((a["x"] + b["x"]) / 2 + (0 if horizontal else 14)))
            cy = int(round((a["y"] + b["y"]) / 2 + (-12 if horizontal else 0)))
            best = {"edge": rid, "text": text, "x": cx, "y": cy,
                    "rect": {"x": cx - width / 2, "y": cy - 14, "w": width, "h": height},
                    "fallback": True}
            issues.append({"edge": rid, "text": text,
                           "issue": "no collision-free label position found; fallback used"})
        if best is None:
            issues.append({"edge": rid, "text": text, "issue": "no segment long enough"})
            continue
        placed.append(best)
        results[rid] = best
    # measured collisions of the chosen placements (same estimator as native-readback.py)
    collisions = {"label_vs_card": [], "label_vs_label": [], "label_vs_edge": []}
    for label in placed:
        for eid, box in element_boxes.items():
            if rect_overlap(label["rect"], box, 0):
                collisions["label_vs_card"].append({"edge": label["edge"], "card": eid})
        for other in placed:
            if other is label:
                continue
            if rect_overlap(label["rect"], other["rect"], 0):
                collisions["label_vs_label"].append({"a": label["edge"], "b": other["edge"]})
        for rid, poly in routes.items():
            if rid == label["edge"]:
                continue
            for k in range(len(poly) - 1):
                if rect_blocks_segment(label["rect"], poly[k], poly[k + 1]):
                    collisions["label_vs_edge"].append({"edge": label["edge"], "over": rid})
                    break
    for key in collisions:
        collisions[key] = sorted({json.dumps(item, sort_keys=True, ensure_ascii=False)
                                  for item in collisions[key]})
        collisions[key] = [json.loads(item) for item in collisions[key]]
    return results, issues, collisions


def rect_overlap(a, b, inflate=0):
    return not (a["x"] + a["w"] + inflate <= b["x"] or b["x"] + b["w"] + inflate <= a["x"]
                or a["y"] + a["h"] + inflate <= b["y"] or b["y"] + b["h"] + inflate <= a["y"])


def length_stats(routes):
    stats = []
    for rid in sorted(routes):
        poly = routes[rid]
        length = sum(abs(poly[i]["x"] - poly[i + 1]["x"]) + abs(poly[i]["y"] - poly[i + 1]["y"])
                     for i in range(len(poly) - 1))
        a, b = poly[0], poly[-1]
        straight = math.hypot(a["x"] - b["x"], a["y"] - b["y"]) or 1.0
        stats.append({"id": rid, "length": length, "straight": round(straight, 1),
                      "ratio": round(length / straight, 2)})
    return {
        "total_length": round(sum(item["length"] for item in stats), 1),
        "max": sorted(stats, key=lambda item: -item["length"])[0] if stats else None,
        "ratio_gt_1_8": [item for item in stats if item["ratio"] > 1.8],
        "ratio_gt_2_5": [item for item in stats if item["ratio"] > 2.5],
        "top_lengths": sorted(stats, key=lambda item: -item["length"])[:8],
    }


def validate_layout(layout, routes):
    issues = []
    element_ids = list(layout.element_box)
    for i, eid in enumerate(element_ids):
        box = layout.element_box[eid]
        zone_box = layout.box[layout.elements[eid]["zone"]]
        if not (box["x"] >= zone_box["x"] + PAD - 2 and box["y"] >= zone_box["y"] + TB - 2
                and box["x"] + box["w"] <= zone_box["x"] + zone_box["w"] - PAD + 2
                and box["y"] + box["h"] <= zone_box["y"] + zone_box["h"] - BP + 2):
            issues.append("out-of-zone %s" % eid)
        for other in element_ids[i + 1:]:
            other_box = layout.element_box[other]
            if not (box["x"] + box["w"] <= other_box["x"] or other_box["x"] + other_box["w"] <= box["x"]
                    or box["y"] + box["h"] <= other_box["y"] or other_box["y"] + other_box["h"] <= box["y"]):
                issues.append("overlap %s %s" % (eid, other))
    for zid, box in layout.box.items():
        parent = layout.zones[zid].get("parent")
        if parent:
            parent_box = layout.box[parent]
            if not (box["x"] >= parent_box["x"] and box["y"] >= parent_box["y"]
                    and box["x"] + box["w"] <= parent_box["x"] + parent_box["w"]
                    and box["y"] + box["h"] <= parent_box["y"] + parent_box["h"]):
                issues.append("zone-not-nested %s" % zid)

    def ancestors(zid):
        out = set()
        cur = layout.zones[zid]
        while cur.get("parent"):
            out.add(cur["parent"])
            cur = layout.zones[cur["parent"]]
        return out

    zids = list(layout.box)
    for i in range(len(zids)):
        for j in range(i + 1, len(zids)):
            a, b = zids[i], zids[j]
            if a in ancestors(b) or b in ancestors(a):
                continue
            ra, rb = layout.box[a], layout.box[b]
            if not (ra["x"] + ra["w"] <= rb["x"] or rb["x"] + rb["w"] <= ra["x"]
                    or ra["y"] + ra["h"] <= rb["y"] or rb["y"] + rb["h"] <= ra["y"]):
                issues.append("zone-overlap %s %s" % (a, b))
    for zid, box in layout.box.items():
        if rect_overlap(layout.legend, box, 0):
            issues.append("legend-overlap %s" % zid)
    for eid, box in layout.element_box.items():
        if rect_overlap(layout.legend, box, 0):
            issues.append("legend-overlap-card %s" % eid)
    solid_hits = []
    for rid, poly in routes.items():
        for k in range(len(poly) - 1):
            for eid, box in layout.element_box.items():
                if rect_blocks_segment(box, poly[k], poly[k + 1]):
                    solid_hits.append({"edge": rid, "card": eid})
    return issues, solid_hits


def assemble_html(sds_frozen, viewer_js, viewer_css, delivery_css, d3_script_tag,
                  notes_fragment, caption, source_note, appendix_lines, title):
    """Assemble the page with plain concatenation (CSS/JS braces must never be re-parsed)."""
    sds_literal = json.dumps(sds_frozen, ensure_ascii=False, indent=1)
    counts = {key: len(sds_frozen.get(key) or []) for key in ("elements", "zones", "relations")}
    labels = sum(1 for rel in sds_frozen.get("relations") or [] if rel.get("label"))
    notes = notes_fragment or ""
    caption_html = ("\n    <figcaption>%s</figcaption>" % html.escape(caption)) if caption else ""
    appendix_items = "".join("\n      <li>%s</li>" % line for line in appendix_lines)
    meta = ("%s · %d 个组件 · %d 个分区 · %d 条关系（%d 条带语义标签）"
            % (source_note or "数据来源见附录", counts["elements"], counts["zones"],
               counts["relations"], labels))
    page = "\n".join([
        "<!DOCTYPE html>",
        '<html lang="zh">',
        "<head>",
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        "  <title>%s — d3js</title>" % html.escape(title),
        "  " + d3_script_tag,
        '  <style id="delivery-css">',
        delivery_css + "</style>",
        '  <style id="chart-css">',
        viewer_css + "</style>",
        "</head>",
        "<body>",
        '<main class="container">',
        "  <h1>%s</h1>" % html.escape(title),
        '  <div class="toolbar">',
        '    <button id="btn-export-svg" type="button">导出 SVG</button>',
        '    <button id="btn-export-png" type="button">导出 PNG</button>',
        '    <button id="btn-zoom-in" type="button">放大</button>',
        '    <button id="btn-zoom-out" type="button">缩小</button>',
        '    <button id="btn-zoom-reset" type="button">复位视图</button>',
        '    <label class="toolbar-check"><input id="toggle-ids" type="checkbox"> 常显关系编号</label>',
        "  </div>",
        '  <figure class="figure-chart diagram">',
        '    <div class="chart-scroll">',
        '      <div id="chart"></div>',
        "    </div>" + caption_html,
        "  </figure>" + notes,
        '  <details class="repro-appendix">',
        "    <summary>复现附录：数据、几何与渲染说明</summary>",
        "    <ul>" + appendix_items,
        "    </ul>",
        "  </details>",
        '  <p class="meta">%s</p>' % html.escape(meta),
        "</main>",
        '<div id="arch-tooltip" role="tooltip"></div>',
        "<script>",
        "const SDS = " + sds_literal + ";",
        viewer_js,
        "</script>",
        "</body>",
        "</html>",
        "",
    ])
    return page


def external_references(page):
    import re
    found = []
    for match in re.finditer(r'(?:src|href)="([^"]+)"', page):
        value = match.group(1)
        if re.match(r"^https?://", value):
            found.append(value)
    return sorted(set(found))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build a deterministic d3js native HTML artifact from an SDS "
                    "(layout + orthogonal routing + collision-aware labels + report).",
        allow_abbrev=False,
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    parser.add_argument("--sds", type=Path, required=True, help="input SDS JSON")
    parser.add_argument("--out", type=Path, required=True, help="existing output directory")
    parser.add_argument("--html", required=True, help="new HTML file name (relative to --out)")
    parser.add_argument("--layout-plan", type=Path, default=None, help="optional layout plan JSON")
    parser.add_argument("--d3-vendor", type=Path, default=None,
                        help="local D3 bundle copied to <out>/vendor/d3.v7.min.js (vendor mode)")
    parser.add_argument("--d3-url", default=None,
                        help="fixed-version D3 URL (CDN mode; the report records it as an external dependency)")
    parser.add_argument("--delivery-css", type=Path, default=None, help="override delivery.css path")
    parser.add_argument("--notes-file", type=Path, default=None, help="optional HTML prose fragment")
    parser.add_argument("--caption", default=None, help="optional figcaption text")
    parser.add_argument("--source-note", default=None, help="short provenance label for the page")
    parser.add_argument("--report-name", default=None, help="layout report file name (default <stem>.layout-report.json)")
    parser.add_argument("--sds-out", default=None, help="frozen SDS file name (default <stem>.sds.json)")
    args = parser.parse_args(argv)

    script_dir = Path(__file__).resolve().parent
    engine_dir = script_dir.parent
    skill_dir = engine_dir.parents[2]
    try:
        if not args.sds.is_file():
            raise BuildError("SDS not found: %s" % args.sds)
        if not args.out.is_dir():
            raise BuildError("--out must be an existing directory: %s" % args.out)
        for label, value in (("--html", args.html), ("--report-name", args.report_name),
                             ("--sds-out", args.sds_out)):
            if value and (Path(value).name != value or Path(value).is_absolute()):
                raise BuildError("%s must be a plain file name inside --out: %r" % (label, value))
        sds = load_json(args.sds)
        plan = load_json(args.layout_plan) if args.layout_plan else {}
        if not isinstance(plan, dict):
            raise BuildError("layout plan must be a JSON object")
        layout = Layout(sds, plan)
        canvas_w, canvas_h = layout.compute()

        # 1:1 canvas and deterministic routing
        router = Router(layout, canvas_w, canvas_h)
        plans, routes, failures, gate_spacing = router.route()
        metrics = route_metrics(routes)
        label_pos, label_issues, label_collisions = place_labels(layout, routes, layout.legend)
        issues, solid_hits = validate_layout(layout, routes)

        # frozen SDS: input order preserved, geometry added; no semantic field rewritten
        depth = {}
        for zid in layout.box:
            depth[zid] = len(layout.zone_chain(zid)) - 1
        top_index = {zid: index for index, zid in enumerate(layout.top_zones)}
        semantic_keys = ("title", "diagram_class", "fidelity_intent", "layout_policy",
                         "layout_authorization", "confirmed_decisions", "weight_plan",
                         "interactivity_intent", "artifact_intent", "style_intent",
                         "counts", "uncertain")
        frozen = {key: sds[key] for key in semantic_keys if key in sds}
        dropped_keys = sorted(set(sds) - set(frozen) - {"elements", "zones", "relations"})
        frozen["engine"] = ENGINE
        frozen["canvas"] = {"w": canvas_w, "h": canvas_h}
        frozen["geometry_meta"] = {
            "owner": "engine (layout_policy=%s)" % sds.get("layout_policy", "optimize"),
            "generator": "draw-diagram references/types/d3js/scripts/build-native.py %s" % VERSION,
            "card": {"w": layout.card_w, "h": layout.card_h,
                     "gap_x": layout.gap_x, "gap_y": layout.gap_y},
            "grid": GRID,
        }
        frozen["zones"] = [
            {"id": zone["id"], "label": zone.get("label"), "parent": zone.get("parent"),
             "box": layout.box[zone["id"]], "depth": depth[zone["id"]]}
            for zone in sds["zones"]
        ]
        frozen["elements"] = [
            {"id": element["id"], "label": element.get("label"), "zone": element["zone"],
             "box": layout.element_box[element["id"]]}
            for element in sds["elements"]
        ]
        relation_entries = []
        for plan_item in plans:
            relation = plan_item["rel"]
            entry = dict(relation)
            entry["route"] = routes[relation["id"]]
            entry["fromKind"] = plan_item["ks"]
            entry["toKind"] = plan_item["kd"]
            if relation["id"] in label_pos:
                entry["labelPos"] = {"x": label_pos[relation["id"]]["x"],
                                     "y": label_pos[relation["id"]]["y"],
                                     "w": int(round(est_text_width(relation["label"], LABEL_FONT) + LABEL_PAD))}
            relation_entries.append(entry)
        frozen["relations"] = relation_entries
        ports = []
        for plan_item in plans:
            rid = plan_item["rel"]["id"]
            if plan_item["cross"] and not plan_item.get("corridor_fallback"):
                ports.append({"x": plan_item["sport"][0], "y": plan_item["sport"][1],
                              "zone": plan_item["ts"], "edge": rid, "kind": "gate"})
                ports.append({"x": plan_item["dport"][0], "y": plan_item["dport"][1],
                              "zone": plan_item["td"], "edge": rid, "kind": "gate"})
            if plan_item["ks"] == "zone":
                ports.append({"x": plan_item["sanchor"][0], "y": plan_item["sanchor"][1],
                              "zone": plan_item["src"], "edge": rid, "kind": "zone-end"})
            if plan_item["kd"] == "zone":
                ports.append({"x": plan_item["danchor"][0], "y": plan_item["danchor"][1],
                              "zone": plan_item["dst"], "edge": rid, "kind": "zone-end"})
        dedup = []
        for port in ports:
            if any(item["edge"] == port["edge"] and abs(item["x"] - port["x"]) < 2
                   and abs(item["y"] - port["y"]) < 2 for item in dedup):
                continue
            dedup.append(port)
        frozen["ports"] = dedup
        frozen["legend"] = layout.legend
        frozen["zoneFill"] = {zid: layout.zone_fill(zid, top_index[zid]) for zid in layout.top_zones}

        # outputs (refuse to overwrite anything)
        html_path = args.out / args.html
        stem = html_path.stem
        sds_path = args.out / (args.sds_out or (stem + ".sds.json"))
        report_path = args.out / (args.report_name or (stem + ".layout-report.json"))
        for path in (html_path, sds_path, report_path):
            if path.exists():
                raise BuildError("refusing to overwrite existing file: %s" % path)
        vendor_target = args.out / "vendor" / "d3.v7.min.js"
        if args.d3_vendor and vendor_target.exists():
            raise BuildError("refusing to overwrite existing vendor asset: %s" % vendor_target)

        if args.d3_vendor:
            if not args.d3_vendor.is_file():
                raise BuildError("d3 vendor asset not found: %s" % args.d3_vendor)
            d3_script_tag = '<script src="vendor/d3.v7.min.js"></script>'
            mode = "local-vendor"
        elif args.d3_url:
            d3_script_tag = '<script src="%s"></script>' % html.escape(args.d3_url)
            mode = "cdn-fixed-url"
        else:
            raise BuildError("one of --d3-vendor or --d3-url is required (declare the JS asset strategy)")

        delivery_css_path = args.delivery_css or (skill_dir / "assets" / "delivery.css")
        delivery_css = delivery_css_path.read_text(encoding="utf-8")
        viewer_css = (engine_dir / "assets" / "viewer.css").read_text(encoding="utf-8")
        viewer_js = (engine_dir / "assets" / "viewer.js").read_text(encoding="utf-8")
        notes_fragment = ""
        if args.notes_file:
            notes_fragment = args.notes_file.read_text(encoding="utf-8")
        appendix_lines = [
            "打开本文件即可渲染，无构建步骤；D3 采用%s策略%s，不访问公网。" % (
                "本地 vendor" if mode == "local-vendor" else "固定版本 URL",
                "（vendor/d3.v7.min.js 与 HTML 同目录）" if mode == "local-vendor" else ""),
            "数据位置：正文脚本顶部的数据对象（分区/组件/关系/端口/正交路由都在其中）；"
            "修改该数据块后刷新浏览器即重新渲染。",
            "几何规则：engine 生成（layout_policy=%s），绝对坐标 viewBox 1:1；"
            "关系为正交折线，跨分区处有端口点；渲染前已跑重叠/越界/逐 box 校验，"
            "交叉与共线由 %s 量化。" % (sds.get("layout_policy", "optimize"), report_path.name),
            "数据溯源：%s。" % (args.source_note or "调用方提供的 SDS"),
        ]
        page = assemble_html(frozen, viewer_js, viewer_css, delivery_css, d3_script_tag,
                             notes_fragment, args.caption, args.source_note,
                             appendix_lines, sds.get("title") or "架构图")
        external = external_references(page)

        if args.d3_vendor:
            vendor_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(args.d3_vendor), str(vendor_target))

        report = {
            "builder": {"name": "build-native.py", "version": VERSION, "engine": ENGINE},
            "sds": {"path": str(args.sds), "sha256": sha256_text(
                json.dumps(sds, ensure_ascii=False, sort_keys=True)),
                "dropped_input_keys": dropped_keys},
            "canvas": {"w": canvas_w, "h": canvas_h},
            "counts": {"elements": len(layout.element_box), "zones": len(layout.box),
                       "relations": len(routes), "labeled": len(label_pos),
                       "ports": len(dedup)},
            "card": {"w": layout.card_w, "h": layout.card_h,
                     "gap_x": layout.gap_x, "gap_y": layout.gap_y},
            "route_failures": failures,
            "layout_issues": issues,
            "solid_hits": solid_hits,
            "crossings": {"count": len(metrics["crossings"]), "items": metrics["crossings"]},
            "collinear": {"total_px": metrics["collinear_total_px"],
                          "items": metrics["collinear"]},
            "non_orthogonal_routes": metrics["non_orthogonal_routes"],
            "elbows_inserted": getattr(router, "elbows", 0),
            "stub_shifts": getattr(router, "stub_shifts", []),
            "labels": {"placed": sorted(label_pos), "issues": label_issues,
                       "collisions": label_collisions,
                       "method": "estimated bbox (15px font; CJK 1.0em/ASCII 0.6em; +12px pad, h=20); "
                                 "candidates avoid cards, zone titles, legend, other labels, all edges"},
            "lengths": length_stats(routes),
            "gate_spacing_px": gate_spacing,
            "corridors": getattr(router, "corridor_notes", {}),
            "plan_warnings": layout.warnings,
            "d3_asset": {"mode": mode, "external_dependencies": external},
            "artifacts": {"html": str(html_path), "sds": str(sds_path),
                          "report": str(report_path),
                          "vendor": (str(vendor_target) if args.d3_vendor else None)},
        }
        if issues or failures or solid_hits:
            # write the evidence anyway, but do not claim a clean build
            html_path.write_text(page, encoding="utf-8")
            sds_path.write_text(json.dumps(frozen, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"status": "defect", "issues": issues, "failures": failures,
                              "solid_hits": solid_hits, "report": str(report_path)},
                             ensure_ascii=False))
            return 1
        html_path.write_text(page, encoding="utf-8")
        sds_path.write_text(json.dumps(frozen, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "ok", "html": str(html_path),
                          "counts": report["counts"], "canvas": report["canvas"],
                          "crossings": report["crossings"]["count"],
                          "collinear_px": report["collinear"]["total_px"],
                          "label_issues": len(label_issues),
                          "label_collisions": {key: len(value) for key, value in label_collisions.items()},
                          "external_dependencies": external,
                          "report": str(report_path)}, ensure_ascii=False))
        return 0
    except BuildError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    except (OSError, UnicodeError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
