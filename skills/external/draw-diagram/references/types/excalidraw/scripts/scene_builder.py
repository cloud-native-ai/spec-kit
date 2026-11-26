#!/usr/bin/env python3
"""Programmatic Excalidraw scene builder (draw-diagram semantic input -> native scene).

This module owns the engine's *generation* mechanics for the scene-JSON path:
deterministic nested-zone layout, orthogonal obstacle-avoiding routing, and
genuine native bindings:

  * component label text  <-> component rectangle   (containerId + boundElements)
  * relation arrow        <-> source/target element (start/endBinding + boundElements)
  * relation label text   <-> relation arrow        (containerId = arrow id and the
    arrow's boundElements lists the text; the reciprocal pair is what the renderer
    uses to re-center the label on the arrow's anchor point)

Arrow-bound text is re-positioned by the renderer; the anchor used by the render
service is the middle vertex of the arrow's points array (the average of the two
middle vertices for an even count). The builder therefore verifies every labeled
relation against a label box centered on that anchor, never against the written
x/y alone.

No business identifiers, counts, colors or paths are baked in: everything comes
from the caller-supplied semantics document.

Library entry points:
  validate_semantics(data)            -> raises SemanticsError
  generate_scene(data)                -> (scene, report)   raises BuildError on a
                                         hard defect (arrow through a component,
                                         label over a component, broken bindings)

Both are exercised by the engine-local tests; the CLI wrapper is
`generate-scene.py` next to this file.
"""
from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict

VERSION = "1.1.0"
ENGINE = "excalidraw"

# ---- generic geometry constants (no instance data) -------------------------
NODE_H = 56
NODE_MIN_W = 110
NODE_MAX_W = 320
NODE_FONT = 20
ZONE_TITLE_FONT = 16
ZONE_TITLE_H = 30
PAD = 26
CELL_GAP_X = 30
CELL_GAP_Y = 22
CHILD_GAP_X = 56
CHILD_GAP_Y = 34
ROOT_GAP_X = 170
ROOT_GAP_Y = 160
ROOT_SHELF_W = 3200
TITLE_FONT = 28
LABEL_FONT = 18
MARGIN = 60
TITLE_BAND = 46
ROUTE_CELL = 10
ROUTE_MARGIN = 70
OUT_LEG = 14

ZONE_COLOR_TOP = "#f1f3f5"
ZONE_COLOR_NESTED = "#ffffff"
ZONE_COLOR_STROKE = "#868e96"
NODE_STROKE = "#1e1e1e"
NODE_FILL = "#ffffff"
TITLE_COLOR = "#495057"


class SemanticsError(ValueError):
    """The caller-supplied semantics document is not usable as-is."""


class BuildError(RuntimeError):
    """A hard geometry/binding defect survived generation (never silently shipped)."""


# ---- semantics --------------------------------------------------------------

def validate_semantics(data):
    if not isinstance(data, dict):
        raise SemanticsError("semantics must be a JSON object")
    elements = data.get("elements")
    zones = data.get("zones")
    relations = data.get("relations")
    if not isinstance(elements, list) or not isinstance(zones, list) or not isinstance(relations, list):
        raise SemanticsError("semantics needs elements[], zones[] and relations[] arrays")

    zone_ids = []
    for z in zones:
        if not isinstance(z, dict) or not _text(z.get("id")):
            raise SemanticsError("every zone needs a non-empty id")
        zone_ids.append(z["id"])
    if len(set(zone_ids)) != len(zone_ids):
        raise SemanticsError("duplicate zone id")
    zone_set = set(zone_ids)
    for z in zones:
        parent = z.get("parent")
        if parent is not None and parent not in zone_set:
            raise SemanticsError(f"zone {z['id']} has unknown parent {parent!r}")
        if parent == z["id"]:
            raise SemanticsError(f"zone {z['id']} is its own parent")
    # cycle check
    parents = {z["id"]: z.get("parent") for z in zones}
    for zid in zone_ids:
        seen = set()
        cur = zid
        while cur is not None:
            if cur in seen:
                raise SemanticsError(f"zone parent cycle at {zid}")
            seen.add(cur)
            cur = parents.get(cur)
            if cur is not None and cur not in zone_set:
                raise SemanticsError(f"zone parent {cur!r} missing")

    element_ids = []
    for e in elements:
        if not isinstance(e, dict) or not _text(e.get("id")):
            raise SemanticsError("every element needs a non-empty id")
        element_ids.append(e["id"])
        if e.get("zone") not in zone_set:
            raise SemanticsError(f"element {e['id']} has unknown zone {e.get('zone')!r}")
    if len(set(element_ids)) != len(element_ids):
        raise SemanticsError("duplicate element id")
    known = set(element_ids) | zone_set

    rel_ids = []
    for r in relations:
        if not isinstance(r, dict) or not _text(r.get("id")):
            raise SemanticsError("every relation needs a non-empty id")
        rel_ids.append(r["id"])
        for side in ("from", "to"):
            if r.get(side) not in known:
                raise SemanticsError(f"relation {r['id']} {side} endpoint {r.get(side)!r} is unknown")
        if r.get("from") == r.get("to"):
            raise SemanticsError(f"relation {r['id']} is a self loop (unsupported)")
    if len(set(rel_ids)) != len(rel_ids):
        raise SemanticsError("duplicate relation id")

    # reserved derived ids must not collide with the semantic ids
    derived = {"diagram-title"}
    for eid in element_ids:
        derived.add(f"label-{eid}")
    for rid in rel_ids:
        derived.add(f"label-{rid}")
    for zid in zone_ids:
        derived.add(f"title-{zid}")
    clash = derived & known
    if clash:
        raise SemanticsError(f"derived element ids collide with semantic ids: {sorted(clash)[:3]}")

    counts = data.get("counts")
    if isinstance(counts, dict):
        if counts.get("elements") is not None and counts["elements"] != len(elements):
            raise SemanticsError("counts.elements does not match elements[]")
        if counts.get("zones") is not None and counts["zones"] != len(zones):
            raise SemanticsError("counts.zones does not match zones[]")
        if counts.get("relations") is not None and counts["relations"] != len(relations):
            raise SemanticsError("counts.relations does not match relations[]")


def _text(value):
    return isinstance(value, str) and value.strip() != ""


def _seed(text, salt=0):
    digest = hashlib.sha1(f"{ENGINE}:{salt}:{text}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


# ---- text metrics (estimate; inflated for safety) --------------------------

def est_text_width(text, font_size):
    width = 0.0
    for ch in text or "":
        width += font_size if ord(ch) > 127 else font_size * 0.62
    return width


def est_box(text, font_size, inflate=1.0):
    width = max(8.0, est_text_width(text, font_size) * inflate)
    height = font_size * 1.3 * inflate
    return width, height


# ---- layout -----------------------------------------------------------------

def _seriate(zone_ids, relations, endpoint_zone, parent_of):
    """Order sibling zones into a chain so related subtrees sit next to each other.

    Generic chain seriation: take relation-weighted pairs in descending order
    and attach each pair to either end of the current chain. Unrelated zones are
    appended at the tail. Row packing later snakes, so chain neighbours stay
    adjacent across row breaks.
    """
    if len(zone_ids) <= 1:
        return list(zone_ids)

    def root_of(zid):
        cur = zid
        while parent_of.get(cur):
            cur = parent_of[cur]
        return cur

    roots = {root_of(z) for z in zone_ids}
    weight = defaultdict(int)
    for rel in relations:
        za = endpoint_zone.get(rel["from"])
        zb = endpoint_zone.get(rel["to"])
        if not za or not zb:
            continue
        ra, rb = root_of(za), root_of(zb)
        if ra != rb:
            weight[(ra, rb)] += 1
            weight[(rb, ra)] += 1
    if not weight:
        return list(zone_ids)

    pairs = sorted(weight.items(), key=lambda kv: (-kv[1], kv[0]))
    chain = []
    for (a, b), _n in pairs:
        if a in chain and b in chain:
            continue
        if not chain:
            chain = [a, b]
        elif a == chain[0] and b not in chain:
            chain.insert(0, b)
        elif a == chain[-1] and b not in chain:
            chain.append(b)
        elif b == chain[0] and a not in chain:
            chain.insert(0, a)
        elif b == chain[-1] and a not in chain:
            chain.append(a)
    placed = set(chain)
    tail = [z for z in zone_ids if z not in placed]
    tail.sort(key=lambda z: (-sum(weight.get((z, o), 0) for o in chain), zone_ids.index(z)))
    return chain + tail


def compute_layout(data):
    elements = data["elements"]
    zones = data["zones"]
    members = defaultdict(list)
    for e in elements:
        members[e["zone"]].append(e)
    parent_of_all = {z["id"]: z.get("parent") for z in zones}
    endpoint_zone = {e["id"]: e["zone"] for e in elements}
    for z in zones:
        endpoint_zone[z["id"]] = z["id"]

    children = defaultdict(list)
    roots = []
    for z in zones:
        if z.get("parent"):
            children[z["parent"]].append(z)
        else:
            roots.append(z)
    root_order = _seriate([z["id"] for z in roots], data["relations"], endpoint_zone, parent_of_all)
    roots = sorted(roots, key=lambda z: root_order.index(z["id"]))
    for pid in list(children):
        child_order = _seriate([z["id"] for z in children[pid]], data["relations"], endpoint_zone, parent_of_all)
        children[pid] = sorted(children[pid], key=lambda z: child_order.index(z["id"]))

    def member_cols(n):
        if n <= 3:
            return max(1, n)
        if n <= 9:
            return 3
        return 4

    def layout_zone(zone):
        zid = zone["id"]
        own = members.get(zid, [])
        cell_w = NODE_MIN_W
        for m in own:
            cell_w = max(cell_w, est_text_width(m.get("label", m["id"]), NODE_FONT) + 30)
        cell_w = min(cell_w, NODE_MAX_W)
        cols = member_cols(len(own))
        rows = math.ceil(len(own) / cols) if own else 0
        grid_w = cols * cell_w + max(0, cols - 1) * CELL_GAP_X if own else 0
        grid_h = rows * NODE_H + max(0, rows - 1) * CELL_GAP_Y if own else 0

        child_blocks = [layout_zone(c) for c in children.get(zid, [])]
        max_row_w = max(grid_w, 760)
        packs = []
        row, row_w = [], 0.0
        for block in child_blocks:
            add = block["w"] + (CHILD_GAP_X if row else 0)
            if row and row_w + add > max_row_w:
                packs.append((row, row_w))
                row, row_w = [block], block["w"]
            else:
                row.append(block)
                row_w += add
        if row:
            packs.append((row, row_w))
        children_w = max((w for _, w in packs), default=0.0)
        children_h = sum(max(b["h"] for b in r) for r, _ in packs) + max(0, len(packs) - 1) * CHILD_GAP_Y

        content_w = max(grid_w, children_w)
        y_cursor = ZONE_TITLE_H
        member_pos = {}
        if own:
            for idx, m in enumerate(own):
                r, c = divmod(idx, cols)
                row_items = min(cols, len(own) - r * cols)
                row_w2 = row_items * cell_w + max(0, row_items - 1) * CELL_GAP_X
                x0 = PAD + (content_w - row_w2) / 2.0
                member_pos[m["id"]] = (x0 + c * (cell_w + CELL_GAP_X), y_cursor + r * (NODE_H + CELL_GAP_Y), cell_w, NODE_H)
            y_cursor += grid_h
            if child_blocks:
                y_cursor += CHILD_GAP_Y
        child_pos = {}
        if child_blocks:
            for row_blocks, row_w2 in packs:
                x0 = PAD + (content_w - row_w2) / 2.0
                x = x0
                for b in row_blocks:
                    child_pos[b["id"]] = (x, y_cursor)
                    x += b["w"] + CHILD_GAP_X
                y_cursor += max(b["h"] for b in row_blocks) + CHILD_GAP_Y

        block = {
            "id": zid,
            "w": content_w + 2 * PAD,
            "h": y_cursor + PAD,
            "members": member_pos,
            "children": child_blocks,
            "child_pos": child_pos,
            "depth": 0,
        }
        return block

    blocks = [layout_zone(z) for z in roots]

    # shelf-pack root blocks
    packed = []
    row, row_w = [], 0.0
    for block in blocks:
        add = block["w"] + (ROOT_GAP_X if row else 0)
        if row and row_w + add > ROOT_SHELF_W:
            packed.append(row)
            row, row_w = [block], block["w"]
        else:
            row.append(block)
            row_w += add
    if row:
        packed.append(row)

    zone_rects = {}
    comp_rects = {}
    depths = {}

    def place(block, ox, oy, depth, ancestors):
        zid = block["id"]
        zone_rects[zid] = (ox, oy, block["w"], block["h"])
        depths[zid] = depth
        group_chain = ancestors + [f"zg-{zid}"]
        for eid, (mx, my, mw, mh) in block["members"].items():
            comp_rects[eid] = (ox + mx, oy + my, mw, mh)
        for child in block["children"]:
            cx, cy = block["child_pos"][child["id"]]
            place(child, ox + cx, oy + cy, depth + 1, group_chain)

    y_cursor = MARGIN + TITLE_BAND
    max_row_w = max((sum(b["w"] for b in r) + max(0, len(r) - 1) * ROOT_GAP_X) for r in packed)
    for row_index, row_blocks in enumerate(packed):
        row_h = max(b["h"] for b in row_blocks)
        if row_index % 2 == 0:
            x_cursor = MARGIN
            for b in row_blocks:
                place(b, x_cursor, y_cursor, 0, [])
                x_cursor += b["w"] + ROOT_GAP_X
        else:
            # snake: first chain block of the row sits at the right edge so the
            # chain neighbour above stays close
            x_right = MARGIN + max_row_w
            for b in row_blocks:
                x_right -= b["w"]
                place(b, x_right, y_cursor, 0, [])
                x_right -= ROOT_GAP_X
        y_cursor += row_h + ROOT_GAP_Y

    max_x = max((r[0] + r[2] for r in zone_rects.values()), default=0)
    max_y = max((r[1] + r[3] for r in zone_rects.values()), default=0)

    # ancestor lookup per zone (self last)
    parent_of = {z["id"]: z.get("parent") for z in zones}
    zone_ancestors = {}
    for zid in zone_rects:
        chain = []
        cur = parent_of.get(zid)
        while cur:
            chain.append(cur)
            cur = parent_of.get(cur)
        zone_ancestors[zid] = chain  # nearest first

    layout = {
        "zones": zone_rects,
        "components": comp_rects,
        "depths": depths,
        "zone_ancestors": zone_ancestors,
        "parent_of": parent_of,
        "canvas": (max_x + MARGIN, max_y + MARGIN),
        "zone_of": {e["id"]: e["zone"] for e in elements},
        "title": data.get("title") or "",
    }
    title_boxes = {}
    by_zone = {z["id"]: z for z in zones}
    for zid, (x, y, _w, _h) in zone_rects.items():
        label = (by_zone.get(zid) or {}).get("label") or zid
        tw, th = est_box(label, ZONE_TITLE_FONT)
        title_boxes[zid] = (x + PAD, y + 6, tw, th)
    layout["title_boxes"] = title_boxes
    return layout


# ---- geometry helpers --------------------------------------------------------

def _seg_rect_hit(p1, p2, rect, pad=0.0):
    x0, y0, x1, y1 = rect[0] - pad, rect[1] - pad, rect[0] + rect[2] + pad, rect[1] + rect[3] + pad
    ax, ay = p1
    bx, by = p2
    if abs(ax - bx) < 1e-9:
        if ax < x0 or ax > x1:
            return False
        lo, hi = sorted((ay, by))
        return not (hi <= y0 or lo >= y1)
    if abs(ay - by) < 1e-9:
        if ay < y0 or ay > y1:
            return False
        lo, hi = sorted((ax, bx))
        return not (hi <= x0 or lo >= x1)
    # diagonal segment: conservative sampling
    steps = max(8, int(math.hypot(bx - ax, by - ay) / 4))
    for i in range(steps + 1):
        t = i / steps
        px = ax + (bx - ax) * t
        py = ay + (by - ay) * t
        if x0 <= px <= x1 and y0 <= py <= y1:
            return True
    return False


def _proper_cross(p, q, r, s):
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    d1 = cross(r, s, p)
    d2 = cross(r, s, q)
    d3 = cross(p, q, r)
    d4 = cross(p, q, s)
    return ((d1 > 0 > d2) or (d1 < 0 < d2)) and ((d3 > 0 > d4) or (d3 < 0 < d4))


def _collinear_overlap(p, q, r, s):
    if abs(p[1] - q[1]) < 1e-9 and abs(r[1] - s[1]) < 1e-9 and abs(p[1] - r[1]) < 0.5:
        lo1, hi1 = sorted((p[0], q[0]))
        lo2, hi2 = sorted((r[0], s[0]))
        return max(0.0, min(hi1, hi2) - max(lo1, lo2))
    if abs(p[0] - q[0]) < 1e-9 and abs(r[0] - s[0]) < 1e-9 and abs(p[0] - r[0]) < 0.5:
        lo1, hi1 = sorted((p[1], q[1]))
        lo2, hi2 = sorted((r[1], s[1]))
        return max(0.0, min(hi1, hi2) - max(lo1, lo2))
    return 0.0


def label_anchor(points):
    """Renderer anchor for arrow-bound text: middle vertex (average of middles)."""
    n = len(points)
    if n == 0:
        return None
    if n % 2 == 1:
        return points[n // 2]
    a, b = points[n // 2 - 1], points[n // 2]
    return ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)


def _box_center(box):
    return (box[0] + box[2] / 2.0, box[1] + box[3] / 2.0)


def _rects_overlap(a, b, pad=0.0):
    ox = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]) + 2 * pad
    oy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]) + 2 * pad
    return max(0.0, ox) * max(0.0, oy), ox > 0 and oy > 0


# ---- routing -----------------------------------------------------------------

def _simplify(points, tol=0.6):
    if len(points) < 3:
        return list(points)
    out = [points[0]]
    for i in range(1, len(points) - 1):
        prev, cur, nxt = out[-1], points[i], points[i + 1]
        if (abs(prev[0] - cur[0]) < tol and abs(cur[0] - nxt[0]) < tol) or (
            abs(prev[1] - cur[1]) < tol and abs(cur[1] - nxt[1]) < tol
        ):
            continue
        out.append(cur)
    out.append(points[-1])
    return out


class _Grid:
    def __init__(self, canvas, components, zones, title_boxes):
        self.cell = ROUTE_CELL
        self.w = int(canvas[0] + 2 * ROUTE_MARGIN) // self.cell + 2
        self.h = int(canvas[1] + 2 * ROUTE_MARGIN) // self.cell + 2
        self.blocked = bytearray(self.w * self.h)
        self.near = bytearray(self.w * self.h)
        self.zone_mask = [0] * (self.w * self.h)
        zone_ids = sorted(zones)
        self.zone_bit = {zid: 1 << i for i, zid in enumerate(zone_ids)}
        for zid, rect in zones.items():
            bit = self.zone_bit[zid]
            for j, i in self._cells_in(rect):
                self.zone_mask[j * self.w + i] |= bit
        for rect in title_boxes:
            for j, i in self._cells_in(rect):
                self.near[j * self.w + i] = min(255, self.near[j * self.w + i] + 6)
        for rect in components.values():
            for j, i in self._cells_center_inside((rect[0] - 4, rect[1] - 4, rect[2] + 8, rect[3] + 8)):
                self.blocked[j * self.w + i] = 1
            for j, i in self._cells_center_inside((rect[0] - 12, rect[1] - 12, rect[2] + 24, rect[3] + 24)):
                self.near[j * self.w + i] = min(255, self.near[j * self.w + i] + 1)
        self.h_used = defaultdict(int)
        self.v_used = defaultdict(int)
        self.cross_boost = 1.0

    def _cells_center_inside(self, rect):
        x0, y0, w, h = rect
        i0 = max(0, int((x0 + ROUTE_MARGIN) // self.cell) - 1)
        i1 = min(self.w - 1, int((x0 + w + ROUTE_MARGIN) // self.cell) + 1)
        j0 = max(0, int((y0 + ROUTE_MARGIN) // self.cell) - 1)
        j1 = min(self.h - 1, int((y0 + h + ROUTE_MARGIN) // self.cell) + 1)
        for j in range(j0, j1 + 1):
            for i in range(i0, i1 + 1):
                cx, cy = self.point_of(i, j)
                if x0 <= cx <= x0 + w and y0 <= cy <= y0 + h:
                    yield j, i

    def _cells_in(self, rect):
        x0, y0, w, h = rect
        i0 = max(0, int((x0 + ROUTE_MARGIN) // self.cell))
        i1 = min(self.w - 1, int((x0 + w + ROUTE_MARGIN) // self.cell))
        j0 = max(0, int((y0 + ROUTE_MARGIN) // self.cell))
        j1 = min(self.h - 1, int((y0 + h + ROUTE_MARGIN) // self.cell))
        for j in range(j0, j1 + 1):
            for i in range(i0, i1 + 1):
                yield j, i

    def cell_of(self, pt):
        i = int((pt[0] + ROUTE_MARGIN) // self.cell)
        j = int((pt[1] + ROUTE_MARGIN) // self.cell)
        return max(0, min(self.w - 1, i)), max(0, min(self.h - 1, j))

    def point_of(self, i, j):
        return (i * self.cell - ROUTE_MARGIN + self.cell / 2.0,
                j * self.cell - ROUTE_MARGIN + self.cell / 2.0)

    def free_near(self, i, j, radius=5):
        if not self.blocked[j * self.w + i]:
            return i, j
        best = None
        for r in range(1, radius + 1):
            for dj in range(-r, r + 1):
                for di in range(-r, r + 1):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.w and 0 <= nj < self.h and not self.blocked[nj * self.w + ni]:
                        d = di * di + dj * dj
                        if best is None or d < best[0]:
                            best = (d, ni, nj)
            if best:
                return best[1], best[2]
        return i, j

    def cost(self, i, j, allowed_mask):
        idx = j * self.w + i
        mask = self.zone_mask[idx]
        extra = 0.0
        if mask:
            unallowed = mask & ~allowed_mask
            extra = 0.2 * bin(unallowed).count("1")
        return 1.0 + extra + 0.3 * self.near[idx]

    def route(self, src_out, dst_out, start_dir, allowed_mask, extra_blocked=None, max_expand=160000):
        import heapq

        si, sj = self.free_near(*self.cell_of(src_out))
        gi, gj = self.free_near(*self.cell_of(dst_out))
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        start = (si, sj, start_dir)
        best = {start: 0.0}
        prev = {start: None}
        heap = [(abs(gi - si) + abs(gj - sj), 0.0, start)]
        goal = None
        expanded = 0
        blocked = self.blocked
        w = self.w
        while heap:
            _, g, state = heapq.heappop(heap)
            if g > best.get(state, float("inf")):
                continue
            i, j, d = state
            if (i, j) == (gi, gj):
                goal = state
                break
            expanded += 1
            if expanded > max_expand:
                break
            for nd, (dx, dy) in enumerate(dirs):
                ni, nj = i + dx, j + dy
                if ni < 0 or nj < 0 or ni >= self.w or nj >= self.h:
                    continue
                idx = nj * w + ni
                if blocked[idx]:
                    continue
                if extra_blocked is not None and extra_blocked[idx]:
                    continue
                step = self.cost(ni, nj, allowed_mask)
                if dx:
                    step += 8.0 * self.h_used.get(idx, 0) + 30.0 * self.cross_boost * self.v_used.get(idx, 0)
                else:
                    step += 8.0 * self.v_used.get(idx, 0) + 30.0 * self.cross_boost * self.h_used.get(idx, 0)
                if nd != d:
                    step += 3.0
                ng = g + step
                ns = (ni, nj, nd)
                if ng < best.get(ns, float("inf")):
                    best[ns] = ng
                    prev[ns] = state
                    heapq.heappush(heap, (ng + abs(gi - ni) + abs(gj - nj), ng, ns))
        if goal is None:
            return None
        cells = []
        cur = goal
        while cur is not None:
            cells.append((cur[0], cur[1]))
            cur = prev[cur]
        cells.reverse()
        return cells

    def _commit(self, cells):
        for k in range(len(cells) - 1):
            i, j = cells[k]
            ni, nj = cells[k + 1]
            idx = j * self.w + i
            if nj == j:
                self.h_used[idx] += 1
            else:
                self.v_used[idx] += 1


def _side_vectors():
    return {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}


def _side_point(rect, side, offset):
    x, y, w, h = rect
    if side == "N":
        return (x + w / 2.0 + offset, y)
    if side == "S":
        return (x + w / 2.0 + offset, y + h)
    if side == "W":
        return (x, y + h / 2.0 + offset)
    return (x + w, y + h / 2.0 + offset)


def _side_len(rect, side):
    return rect[2] if side in ("N", "S") else rect[3]


def _candidate_sides(rect_a, rect_b):
    ca = _box_center(rect_a)
    cb = _box_center(rect_b)
    dx = cb[0] - ca[0]
    dy = cb[1] - ca[1]
    horizontal = "E" if dx >= 0 else "W"
    vertical = "S" if dy >= 0 else "N"
    if abs(dx) >= abs(dy):
        start = [horizontal, vertical, "N" if vertical == "S" else "S", "W" if horizontal == "E" else "E"]
        end = [{"E": "W", "W": "E", "N": "S", "S": "N"}[horizontal],
               {"E": "W", "W": "E", "N": "S", "S": "N"}[vertical],
               {"E": "W", "W": "E", "N": "S", "S": "N"}[("N" if vertical == "S" else "S")],
               {"E": "W", "W": "E", "N": "S", "S": "N"}[("W" if horizontal == "E" else "E")]]
    else:
        start = [vertical, horizontal, "W" if horizontal == "E" else "E", "S" if vertical == "N" else "N"]
        end = [{"E": "W", "W": "E", "N": "S", "S": "N"}[vertical],
               {"E": "W", "W": "E", "N": "S", "S": "N"}[horizontal],
               {"E": "W", "W": "E", "N": "S", "S": "N"}[("W" if horizontal == "E" else "E")],
               {"E": "W", "W": "E", "N": "S", "S": "N"}[("S" if vertical == "N" else "N")]]
    return start, end


def _orthogonalize(points):
    out = [points[0]]
    for p in points[1:]:
        prev = out[-1]
        dx = abs(p[0] - prev[0])
        dy = abs(p[1] - prev[1])
        if dx > 0.4 and dy > 0.4:
            if len(out) >= 2:
                pprev = out[-2]
                last_vertical = abs(prev[0] - pprev[0]) < 0.4
            else:
                last_vertical = dx < dy
            out.append((prev[0], p[1]) if last_vertical else (p[0], prev[1]))
        out.append(p)
    return out


def _route_path(grid, rect_a, rect_b, side_a, side_b, offset_a, offset_b, allowed_mask, zone_block_rects=None):
    vec = _side_vectors()
    s = _side_point(rect_a, side_a, offset_a)
    t = _side_point(rect_b, side_b, offset_b)
    s_out = (s[0] + vec[side_a][0] * OUT_LEG, s[1] + vec[side_a][1] * OUT_LEG)
    t_out = (t[0] + vec[side_b][0] * OUT_LEG, t[1] + vec[side_b][1] * OUT_LEG)
    extra = None
    if zone_block_rects:
        extra = bytearray(grid.w * grid.h)
        for rect in zone_block_rects:
            for j, i in grid._cells_in(rect):
                extra[j * grid.w + i] = 1
    dirs = {"E": 0, "S": 1, "W": 2, "N": 3}
    cells = grid.route(s_out, t_out, dirs[side_a], allowed_mask, extra)
    if cells is None:
        return None
    pts = [s, s_out]
    for i, j in cells:
        pts.append(grid.point_of(i, j))
    pts.append(t_out)
    pts.append(t)
    return _simplify(_orthogonalize(pts)), cells


def _overlaps_and_crossings(points, others):
    cross = set()
    overlap = 0.0
    for oid, opts in others.items():
        for k in range(len(points) - 1):
            p, q = points[k], points[k + 1]
            for m in range(len(opts) - 1):
                r, s = opts[m], opts[m + 1]
                if _proper_cross(p, q, r, s):
                    cross.add(oid)
                overlap += _collinear_overlap(p, q, r, s)
    return cross, overlap


def _label_box_at(anchor, label):
    w, h = est_box(label, LABEL_FONT, inflate=1.12)
    return (anchor[0] - w / 2.0, anchor[1] - h / 2.0, w, h)


def _label_clear(anchor, label, components, known_labels, skip_endpoints):
    box = _label_box_at(anchor, label)
    for cid, rect in components.items():
        if cid in skip_endpoints:
            continue
        _, hit = _rects_overlap(box, rect, pad=6)
        if hit:
            return False, box
    for other in known_labels:
        _, hit = _rects_overlap(box, other, pad=6)
        if hit:
            return False, box
    return True, box


def route_relations(data, layout):
    grid = _Grid(layout["canvas"], layout["components"], layout["zones"], layout.get("title_boxes", {}).values())
    comps = layout["components"]
    zones = layout["zones"]
    anchors_of = {**comps, **zones}
    zone_ids = set(zones)
    zone_of = layout["zone_of"]
    parent_of = layout["parent_of"]

    def ancestors_plus(zid):
        chain = []
        cur = zid
        while cur:
            chain.append(cur)
            cur = parent_of.get(cur)
        return chain

    rels = data["relations"]
    state = {}
    label_of = {r["id"]: r["label"] for r in rels if _text(r.get("label"))}

    def manhattan(rel):
        a = layout["components"].get(rel["from"]) or layout["zones"].get(rel["from"])
        b = layout["components"].get(rel["to"]) or layout["zones"].get(rel["to"])
        ca, cb = _box_center(a), _box_center(b)
        return abs(ca[0] - cb[0]) + abs(ca[1] - cb[1])

    labeled_first = [r for r in rels if _text(r.get("label"))]
    rest = sorted((r for r in rels if not _text(r.get("label"))), key=manhattan, reverse=True)
    ordered = labeled_first + rest
    routes = {}
    side_use = defaultdict(int)
    label_boxes = []
    issues = []

    for rel in ordered:
        a_id, b_id = rel["from"], rel["to"]
        if a_id not in anchors_of or b_id not in anchors_of:
            raise BuildError(f"relation {rel['id']} endpoint has no rectangle")
        rect_a, rect_b = anchors_of[a_id], anchors_of[b_id]
        za = a_id if a_id in zone_ids else zone_of.get(a_id)
        zb = b_id if b_id in zone_ids else zone_of.get(b_id)
        allowed = 0
        for z in ancestors_plus(za) + ancestors_plus(zb):
            allowed |= grid.zone_bit.get(z, 0)
        zone_block = []
        if b_id in zone_ids:
            zone_block.append(zones[b_id])
        if a_id in zone_ids:
            zone_block.append(zones[a_id])

        starts, ends = _candidate_sides(rect_a, rect_b)
        combos = []
        for i, sa in enumerate(starts[:3]):
            for j, sb in enumerate(ends[:3]):
                combos.append((i + j, sa, sb))
        combos.sort(key=lambda c: c[0])

        labeled = _text(rel.get("label"))
        best = None
        for _, sa, sb in combos[:5]:
            oa = side_use[(a_id, sa)]
            ob = side_use[(b_id, sb)]
            off_a = 0 if oa == 0 else (1 if oa % 2 else -1) * ((oa + 1) // 2) * 16
            off_b = 0 if ob == 0 else (1 if ob % 2 else -1) * ((ob + 1) // 2) * 16
            lim_a = _side_len(rect_a, sa) / 2.0 - 16
            lim_b = _side_len(rect_b, sb) / 2.0 - 16
            off_a = max(-lim_a, min(lim_a, off_a))
            off_b = max(-lim_b, min(lim_b, off_b))
            routed = _route_path(grid, rect_a, rect_b, sa, sb, off_a, off_b, allowed, zone_block)
            if routed is None:
                continue
            points, cells = routed
            score = len(points) * 6.0
            for k in range(len(points) - 1):
                seglen = abs(points[k][0] - points[k + 1][0]) + abs(points[k][1] - points[k + 1][1])
                score += seglen
            cross, overlap = _overlaps_and_crossings(points, routes)
            score += 60 * len(cross) + 1.0 * overlap
            hard = False
            label_box = None
            if labeled:
                anchor = label_anchor(points)
                ok, label_box = _label_clear(anchor, rel["label"], comps, label_boxes, {a_id, b_id})
                if not ok:
                    hard = True
            if best is None or (hard, score) < (best[0], best[1]):
                best = (hard, score, points, sa, sb, label_box, cells)
        if best is None or best[0]:
            alt = None
            if labeled:
                alt = _labeled_corridor_route(rel, rect_a, rect_b, layout, comps, zones, routes, label_boxes, {a_id, b_id})
            if alt is None:
                if best is None:
                    raise BuildError(f"relation {rel['id']}: no orthogonal route found")
                raise BuildError(
                    f"relation {rel['id']}: labeled route cannot keep label {rel['label']!r} off components")
            points, sa, sb, label_box = alt
            cells = None
        else:
            _, _, points, sa, sb, label_box, cells = best

        if cells:
            grid._commit(cells)
        routes[rel["id"]] = points
        state[rel["id"]] = {
            "a_id": a_id, "b_id": b_id, "rect_a": rect_a, "rect_b": rect_b,
            "allowed": allowed, "zone_block": zone_block,
            "label": rel.get("label") if labeled else None,
        }
        side_use[(a_id, sa)] += 1
        side_use[(b_id, sb)] += 1
        if label_box is not None:
            label_boxes.append(label_box)

    _ripup_pass(grid, routes, state, label_of, comps)

    return routes


def _crossing_counts(routes):
    ids = sorted(routes)
    counts = {rid: 0 for rid in ids}
    pairs = set()
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            A, B = routes[ids[i]], routes[ids[j]]
            hit = False
            for k in range(len(A) - 1):
                for m in range(len(B) - 1):
                    if _proper_cross(A[k], A[k + 1], B[m], B[m + 1]):
                        hit = True
                        break
                if hit:
                    break
            if hit:
                pairs.add((ids[i], ids[j]))
                counts[ids[i]] += 1
                counts[ids[j]] += 1
    return counts, pairs


def _ripup_pass(grid, routes, state, label_of, comps, top_n=8):
    """Bounded rip-up/reroute: retry the heaviest crossing contributors once."""
    counts, _pairs = _crossing_counts(routes)
    targets = [rid for rid, n in sorted(counts.items(), key=lambda kv: -kv[1])[:top_n] if n > 0]
    for rid in targets:
        st = state[rid]
        old = routes.pop(rid)
        current_boxes = [_label_box_at(label_anchor(routes[r]), label_of[r]) for r in sorted(routes) if r in label_of]
        endpoints = {st["a_id"], st["b_id"]}
        starts, ends = _candidate_sides(st["rect_a"], st["rect_b"])
        best = None
        grid.cross_boost = 6.0
        try:
            for _, sa, sb in sorted((i + j, sa, sb) for i, sa in enumerate(starts[:3]) for j, sb in enumerate(ends[:3]))[:5]:
                routed = _route_path(grid, st["rect_a"], st["rect_b"], sa, sb, 0, 0, st["allowed"], st["zone_block"])
                if routed is None:
                    continue
                points, _cells = routed
                box = None
                if st["label"]:
                    anchor = label_anchor(points)
                    clear, box = _label_clear(anchor, st["label"], comps, current_boxes, endpoints)
                    if not clear:
                        continue
                cross, overlap = _overlaps_and_crossings(points, routes)
                length = sum(abs(points[k][0] - points[k + 1][0]) + abs(points[k][1] - points[k + 1][1])
                             for k in range(len(points) - 1))
                score = 1000.0 * len(cross) + length + 0.5 * overlap
                if best is None or score < best[0]:
                    best = (score, points, cross, box)
        finally:
            grid.cross_boost = 1.0
        if best is not None:
            old_cross, _ = _overlaps_and_crossings(old, routes)
            if len(best[2]) < len(old_cross):
                routes[rid] = best[1]
                continue
        routes[rid] = old


def _corridor_lines(layout, comps=None):
    xs, ys = set(), set()
    for rect in layout["zones"].values():
        xs.update({rect[0] - 22, rect[0] + rect[2] + 22})
        ys.update({rect[1] - 22, rect[1] + rect[3] + 22})
    for rect in (comps or layout["components"]).values():
        xs.update({rect[0] + rect[2] / 2.0})
        ys.update({rect[1] + rect[3] / 2.0})
    canvas = layout["canvas"]
    xs.update({MARGIN / 2.0, canvas[0] - MARGIN / 2.0})
    ys.update({MARGIN / 2.0, canvas[1] - MARGIN / 2.0})
    return sorted(xs), sorted(ys)


def _labeled_corridor_route(rel, rect_a, rect_b, layout, comps, zones, routes, label_boxes, endpoints):
    """Explicit 5-point labeled shapes whose middle vertex is the renderer anchor."""
    xs, ys = _corridor_lines(layout, comps)
    ca = _box_center(rect_a)
    cb = _box_center(rect_b)
    mid = ((ca[0] + cb[0]) / 2.0, (ca[1] + cb[1]) / 2.0)
    xs = sorted(xs, key=lambda v: abs(v - mid[0]))[:10] + [rect_a[0], rect_a[0] + rect_a[2], rect_b[0], rect_b[0] + rect_b[2]]
    ys = sorted(ys, key=lambda v: abs(v - mid[1]))[:10] + [rect_a[1], rect_a[1] + rect_a[3], rect_b[1], rect_b[1] + rect_b[3]]
    starts, ends = _candidate_sides(rect_a, rect_b)
    best = None
    for sa in starts[:2]:
        for sb in ends[:2]:
            s = _side_point(rect_a, sa, 0)
            t = _side_point(rect_b, sb, 0)
            for mx in xs:
                for my in ys:
                    variants = []
                    # vertical-first through (Sx,my),(mx,my),(mx,Ty)
                    variants.append([s, (s[0], my), (mx, my), (mx, t[1]), t])
                    # horizontal-first through (mx,Sy),(mx,my),(Ty,my)
                    variants.append([s, (mx, s[1]), (mx, my), (t[0], my), t])
                    for points in variants:
                        points = _simplify(points)
                        if len(points) % 2 == 0:
                            continue
                        ok = True
                        for k in range(len(points) - 1):
                            for cid, rect in comps.items():
                                if cid in endpoints:
                                    continue
                                if _seg_rect_hit(points[k], points[k + 1], rect, pad=2):
                                    ok = False
                                    break
                            if not ok:
                                break
                        if not ok:
                            continue
                        anchor = label_anchor(points)
                        clear, box = _label_clear(anchor, rel["label"], comps, label_boxes, endpoints)
                        if not clear:
                            continue
                        cross, overlap = _overlaps_and_crossings(points, routes)
                        score = sum(abs(points[k][0] - points[k + 1][0]) + abs(points[k][1] - points[k + 1][1])
                                    for k in range(len(points) - 1)) + 60 * len(cross) + 0.5 * overlap
                        if best is None or score < best[0]:
                            best = (score, points, sa, sb, box)
    if best is None:
        return None
    return best[1], best[2], best[3], best[4]


# ---- scene emission ----------------------------------------------------------

def build_scene(data, layout, routes):
    elements = data["elements"]
    zones = data["zones"]
    by_element = {e["id"]: e for e in elements}
    by_zone = {z["id"]: z for z in zones}
    parent_of = layout["parent_of"]
    zone_group_of = {}
    for zid in layout["zones"]:
        chain = []
        cur = zid
        while cur:
            chain.append(f"zg-{cur}")
            cur = parent_of.get(cur)
        zone_group_of[zid] = chain

    out = []
    title = layout.get("title") or ""

    if title:
        tw, th = est_box(title, TITLE_FONT)
        out.append({
            "id": "diagram-title", "type": "text",
            "x": MARGIN, "y": MARGIN - 8, "width": tw, "height": th,
            "text": title, "fontSize": TITLE_FONT, "fontFamily": 1,
            "textAlign": "left", "verticalAlign": "top", "containerId": None,
            "originalText": title, "lineHeight": 1.25,
            "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "roughness": 0, "opacity": 100,
            "angle": 0, "seed": _seed("diagram-title"), "version": 1,
            "groupIds": [], "frameId": None, "roundness": None,
            "boundElements": [], "isDeleted": False, "updated": 1, "link": None, "locked": False,
            "customData": {"role": "diagram-title"},
        })

    zone_order = sorted(layout["zones"], key=lambda z: (layout["depths"][z], z))
    endpoint_bindings = defaultdict(list)
    for rid in routes:
        rel = next(r for r in data["relations"] if r["id"] == rid)
        endpoint_bindings[rel["from"]].append({"id": rid, "type": "arrow"})
        endpoint_bindings[rel["to"]].append({"id": rid, "type": "arrow"})
    for zid in zone_order:
        x, y, w, h = layout["zones"][zid]
        depth = layout["depths"][zid]
        out.append({
            "id": zid, "type": "rectangle",
            "x": x, "y": y, "width": w, "height": h,
            "strokeColor": ZONE_COLOR_STROKE, "backgroundColor": ZONE_COLOR_TOP if depth == 0 else ZONE_COLOR_NESTED,
            "fillStyle": "solid", "strokeWidth": 3 if depth == 0 else 2, "strokeStyle": "dashed",
            "roughness": 0, "opacity": 100, "angle": 0, "seed": _seed(zid), "version": 1,
            "groupIds": zone_group_of[zid], "frameId": None, "roundness": None,
            "boundElements": endpoint_bindings.get(zid, []), "isDeleted": False, "updated": 1,
            "link": None, "locked": False,
            "customData": {"role": "zone", "zoneId": zid},
        })
    for zid in zone_order:
        x, y, w, h = layout["zones"][zid]
        label = by_zone[zid].get("label") or zid
        tw, th = est_box(label, ZONE_TITLE_FONT)
        out.append({
            "id": f"title-{zid}", "type": "text",
            "x": x + PAD, "y": y + 6, "width": tw, "height": th,
            "text": label, "fontSize": ZONE_TITLE_FONT, "fontFamily": 1,
            "textAlign": "left", "verticalAlign": "top", "containerId": None,
            "originalText": label, "lineHeight": 1.25,
            "strokeColor": TITLE_COLOR, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "roughness": 0, "opacity": 100,
            "angle": 0, "seed": _seed(f"title-{zid}"), "version": 1,
            "groupIds": zone_group_of[zid], "frameId": None, "roundness": None,
            "boundElements": [], "isDeleted": False, "updated": 1, "link": None, "locked": False,
            "customData": {"role": "zone-title", "zoneId": zid},
        })

    comp_bindings = endpoint_bindings

    for e in elements:
        x, y, w, h = layout["components"][e["id"]]
        zid = e["zone"]
        label = e.get("label") or e["id"]
        groups = [f"cg-{e['id']}"] + zone_group_of[zid]
        bound = [{"id": f"label-{e['id']}", "type": "text"}] + comp_bindings.get(e["id"], [])
        out.append({
            "id": e["id"], "type": "rectangle",
            "x": x, "y": y, "width": w, "height": h,
            "strokeColor": NODE_STROKE, "backgroundColor": NODE_FILL,
            "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100, "angle": 0, "seed": _seed(e["id"]), "version": 1,
            "groupIds": groups, "frameId": None, "roundness": None,
            "boundElements": bound, "isDeleted": False, "updated": 1, "link": None, "locked": False,
            "customData": {"role": "component", "elementId": e["id"]},
        })
    for e in elements:
        x, y, w, h = layout["components"][e["id"]]
        label = e.get("label") or e["id"]
        tw, th = est_box(label, NODE_FONT)
        groups = [f"cg-{e['id']}"] + zone_group_of.get(e["zone"], [])
        out.append({
            "id": f"label-{e['id']}", "type": "text",
            "x": x + (w - tw) / 2.0, "y": y + (h - th) / 2.0, "width": tw, "height": th,
            "text": label, "fontSize": NODE_FONT, "fontFamily": 1,
            "textAlign": "center", "verticalAlign": "middle", "containerId": e["id"],
            "originalText": label, "lineHeight": 1.25,
            "strokeColor": NODE_STROKE, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "roughness": 0, "opacity": 100,
            "angle": 0, "seed": _seed(f"label-{e['id']}"), "version": 1,
            "groupIds": groups, "frameId": None, "roundness": None,
            "boundElements": [], "isDeleted": False, "updated": 1, "link": None, "locked": False,
            "customData": {"role": "component-label", "elementId": e["id"]},
        })

    label_ref = {r["id"]: r for r in data["relations"] if _text(r.get("label"))}
    for rel in data["relations"]:
        points = routes[rel["id"]]
        rel_points = [(round(p[0] - points[0][0], 2), round(p[1] - points[0][1], 2)) for p in points]
        width = max(abs(p[0]) for p in rel_points)
        height = max(abs(p[1]) for p in rel_points)
        bound = []
        if rel["id"] in label_ref:
            bound.append({"id": f"label-{rel['id']}", "type": "text"})
        out.append({
            "id": rel["id"], "type": "arrow",
            "x": round(points[0][0], 2), "y": round(points[0][1], 2),
            "width": round(width, 2), "height": round(height, 2),
            "points": [[round(p[0], 2), round(p[1], 2)] for p in rel_points],
            "startBinding": {"elementId": rel["from"], "focus": 0, "gap": 4},
            "endBinding": {"elementId": rel["to"], "focus": 0, "gap": 4},
            "startArrowhead": None, "endArrowhead": "triangle", "lastCommittedPoint": None,
            "strokeColor": rel.get("color") or NODE_STROKE, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100, "angle": 0, "seed": _seed(rel["id"]), "version": 1,
            "groupIds": [], "frameId": None, "roundness": None,
            "boundElements": bound, "isDeleted": False, "updated": 1, "link": None, "locked": False,
            "customData": {"role": "relation", "relationId": rel["id"], "from": rel["from"], "to": rel["to"]},
        })
    for rel in data["relations"]:
        if rel["id"] not in label_ref:
            continue
        points = routes[rel["id"]]
        anchor = label_anchor(points)
        tw, th = est_box(rel["label"], LABEL_FONT, inflate=1.12)
        out.append({
            "id": f"label-{rel['id']}", "type": "text",
            "x": round(anchor[0] - tw / 2.0, 2), "y": round(anchor[1] - th / 2.0, 2),
            "width": tw, "height": th,
            "text": rel["label"], "fontSize": LABEL_FONT, "fontFamily": 1,
            "textAlign": "center", "verticalAlign": "middle", "containerId": rel["id"],
            "originalText": rel["label"], "lineHeight": 1.25,
            "strokeColor": rel.get("color") or NODE_STROKE, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "roughness": 0, "opacity": 100,
            "angle": 0, "seed": _seed(f"label-{rel['id']}"), "version": 1,
            "groupIds": [], "frameId": None, "roundness": None,
            "boundElements": [], "isDeleted": False, "updated": 1, "link": None, "locked": False,
            "customData": {"role": "relation-label", "labelFor": rel["id"]},
        })

    scene = {
        "type": "excalidraw",
        "version": 2,
        "source": "draw-diagram/excalidraw-scene-builder",
        "elements": out,
        "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
        "files": {},
    }
    return scene


# ---- analysis -----------------------------------------------------------------

def analyze(data, layout, scene):
    elements = scene["elements"]
    by_id = {e["id"]: e for e in elements}
    comp_rects = layout["components"]
    zone_rects = layout["zones"]
    rels = {r["id"]: r for r in data["relations"]}

    def arrow_pts(a):
        return [(a["x"] + p[0], a["y"] + p[1]) for p in a.get("points") or []]

    arrows = {e["id"]: e for e in elements if e.get("type") == "arrow"}
    pts = {aid: arrow_pts(a) for aid, a in arrows.items()}

    # bindings
    binding_problems = []
    for aid, a in arrows.items():
        for side in ("startBinding", "endBinding"):
            b = a.get(side) or {}
            target = by_id.get(b.get("elementId", ""))
            if target is None:
                binding_problems.append(f"{aid}:{side} target missing")
                continue
            if not any(x.get("id") == aid for x in (target.get("boundElements") or [])):
                binding_problems.append(f"{aid}:{side} missing reciprocal registration")
        for b in a.get("boundElements") or []:
            t = by_id.get(b.get("id", ""))
            if t is None or t.get("containerId") != aid:
                binding_problems.append(f"{aid}: text ref without reciprocal containerId")
    for rel in data["relations"]:
        a = arrows.get(rel["id"])
        if a is None:
            binding_problems.append(f"{rel['id']}: arrow missing")
            continue
        if (a["startBinding"] or {}).get("elementId") != rel["from"]:
            binding_problems.append(f"{rel['id']}: start endpoint wrong")
        if (a["endBinding"] or {}).get("elementId") != rel["to"]:
            binding_problems.append(f"{rel['id']}: end endpoint wrong")
    for t in elements:
        if t.get("type") == "text" and t.get("containerId"):
            c = by_id.get(t["containerId"])
            if c is None:
                binding_problems.append(f"{t['id']}: container missing")
            elif not any(x.get("id") == t["id"] for x in (c.get("boundElements") or [])):
                binding_problems.append(f"{t['id']}: container lacks reciprocal ref")

    # edge-through-component
    through = []
    for aid, points in pts.items():
        a = arrows[aid]
        ends = {(a.get("startBinding") or {}).get("elementId"), (a.get("endBinding") or {}).get("elementId")}
        for k in range(len(points) - 1):
            for cid, rect in comp_rects.items():
                if cid in ends:
                    continue
                if _seg_rect_hit(points[k], points[k + 1], rect, pad=-1):
                    through.append({"relation": aid, "component": cid, "segment": k})

    # crossings
    cross_pairs = set()
    overlap_len = 0.0
    aids = sorted(pts)
    for i in range(len(aids)):
        for j in range(i + 1, len(aids)):
            A, B = pts[aids[i]], pts[aids[j]]
            for k in range(len(A) - 1):
                for m in range(len(B) - 1):
                    if _proper_cross(A[k], A[k + 1], B[m], B[m + 1]):
                        cross_pairs.add((aids[i], aids[j]))
                    overlap_len += _collinear_overlap(A[k], A[k + 1], B[m], B[m + 1])

    # labels
    label_boxes = {}
    label_problems = []
    for rid, rel in rels.items():
        if not _text(rel.get("label")):
            continue
        anchor = label_anchor(pts[rid])
        box = _label_box_at(anchor, rel["label"])
        label_boxes[rid] = box
        for cid, rect in comp_rects.items():
            if cid in (rel["from"], rel["to"]):
                continue
            _, hit = _rects_overlap(box, rect, pad=3)
            if hit:
                label_problems.append({"relation": rid, "over_component": cid})
    rids = sorted(label_boxes)
    for i in range(len(rids)):
        for j in range(i + 1, len(rids)):
            _, hit = _rects_overlap(label_boxes[rids[i]], label_boxes[rids[j]], pad=2)
            if hit:
                label_problems.append({"relations": [rids[i], rids[j]], "issue": "labels overlap"})

    anchors = {rid: label_anchor(pts[rid]) for rid in rels if rid in pts}

    report = {
        "engine": ENGINE,
        "builder_version": VERSION,
        "counts": {
            "elements": len(data["elements"]),
            "zones": len(data["zones"]),
            "relations": len(data["relations"]),
            "labels": sum(1 for r in data["relations"] if _text(r.get("label"))),
        },
        "canvas": {"w": round(layout["canvas"][0], 1), "h": round(layout["canvas"][1], 1)},
        "binding_problems": binding_problems,
        "edge_through_component": through,
        "crossings": {"measured": True, "method": "strict proper intersections of delivered orthogonal segments",
                      "pair_count": len(cross_pairs), "pairs": sorted([list(p) for p in cross_pairs])},
        "collinear_overlap_px": round(overlap_len, 1),
        "label_boxes": {rid: [round(v, 1) for v in box] for rid, box in label_boxes.items()},
        "label_anchors": {rid: [round(p[0], 1), round(p[1], 1)] for rid, p in anchors.items()},
        "label_problems": label_problems,
        "label_anchor_rule": "middle vertex of the arrow points array (average of the two middle vertices when even)",
        "route_lengths": {rid: round(sum(abs(p[k][0] - p[k + 1][0]) + abs(p[k][1] - p[k + 1][1])
                                          for k in range(len(p) - 1)), 1) for rid, p in pts.items()},
        "limitations": [
            "Text widths are estimates (CJK=fontSize, ASCII=0.62*fontSize) inflated 12% for labels; the renderer re-measures with real fonts.",
            "The label anchor rule was calibrated on the shared render service's actual SVG for the prior scene; the readback re-verifies it per render.",
            "Zone-background crossings are not counted as hard issues; only component interiors are obstacles.",
        ],
    }
    return report


def generate_scene(data):
    validate_semantics(data)
    layout = compute_layout(data)
    routes = route_relations(data, layout)
    scene = build_scene(data, layout, routes)
    report = analyze(data, layout, scene)
    hard = []
    if report["binding_problems"]:
        hard.append(f"binding problems: {len(report['binding_problems'])}")
    if report["edge_through_component"]:
        hard.append(f"edge-through-component: {len(report['edge_through_component'])}")
    if report["label_problems"]:
        hard.append(f"label problems: {len(report['label_problems'])}")
    if hard:
        detail = json.dumps({"hard": hard,
                             "edge_through_component": report["edge_through_component"][:10],
                             "label_problems": report["label_problems"][:10],
                             "binding_problems": report["binding_problems"][:10]},
                            ensure_ascii=False, indent=1)
        raise BuildError(detail)
    return scene, report
