#!/usr/bin/env python3
"""native-readback.py — independent readback of a produced Excalidraw scene.

Reads the ACTUAL native scene (and optionally the ACTUAL rendered SVG) and
compares it with the authoritative semantics document. The expected semantics
are used only for comparison; actual records are extracted from the native file
first (IDs, bindings, reciprocal registrations, groups, geometry-derived
parent/zone membership, arrow-bound labels, extra text).

Usage:
  native-readback.py --source <scene.excalidraw> --semantics <semantics.json>
                     [--svg <rendered.svg>] --output <new-report.json>

Exit codes (documented contract):
  0  pass          — no hard discrepancy; optional evidence complete
  1  hard failure  — a semantic/geometry/binding discrepancy (never a pass)
  2  usage or I/O error (unknown flag, missing file, invalid JSON, existing output)
  3  partial       — no hard discrepancy, but requested evidence is missing or a
                     check is unsupported/limited (partial is NOT a pass)

Hard discrepancy classes: missing/extra element, zone or relation; wrong
direction; endpoint expanded from a zone to a member (or the reverse); label
text mismatch; broken reciprocal binding; a relation label that is not
genuinely bound to its arrow; an arrow through a component interior; a label
over a component; an arrow endpoint off its target boundary; extra unrequested
text (e.g. an invented legend).

Limitations (reported, never hidden): Excalidraw SVG has no stable semantic
IDs, so SVG identity is a text multiset plus geometry; label boxes use
estimated font widths (inflated); arrow tip positions are measured on native
coordinates, not re-extracted from SVG path geometry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

VERSION = "1.0.0"
ENGINE = "excalidraw"
EDGE_ON_BOUNDARY_TOL = 6.0
LABEL_INFLATE = 1.12
FONT_LABEL = 18
FONT_NODE = 20
FONT_ZONE = 16
FONT_TITLE = 28


def est_width(text, font_size):
    total = 0.0
    for ch in text or "":
        total += font_size if ord(ch) > 127 else font_size * 0.62
    return total


def est_height(font_size):
    return font_size * 1.3


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rect_of(e):
    return (e.get("x", 0.0), e.get("y", 0.0), e.get("width", 0.0), e.get("height", 0.0))


def rect_contains(outer, inner, eps=0.5):
    return (inner[0] >= outer[0] - eps and inner[1] >= outer[1] - eps
            and inner[0] + inner[2] <= outer[0] + outer[2] + eps
            and inner[1] + inner[3] <= outer[1] + outer[3] + eps)


def overlap_area(a, b, pad=0.0):
    ox = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]) + 2 * pad
    oy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]) + 2 * pad
    if ox <= 0 or oy <= 0:
        return 0.0
    return ox * oy


def seg_rect_hit(p1, p2, rect, pad=0.0):
    x0, y0, x1, y1 = rect[0] - pad, rect[1] - pad, rect[0] + rect[2] + pad, rect[1] + rect[3] + pad
    ax, ay = p1
    bx, by = p2
    if abs(ax - bx) < 1e-9:
        if not (x0 < ax < x1):
            return False
        lo, hi = sorted((ay, by))
        return hi > y0 and lo < y1
    if abs(ay - by) < 1e-9:
        if not (y0 < ay < y1):
            return False
        lo, hi = sorted((ax, bx))
        return hi > x0 and lo < x1
    steps = max(8, int(math.hypot(bx - ax, by - ay) / 4))
    for i in range(steps + 1):
        t = i / steps
        px, py = ax + (bx - ax) * t, ay + (by - ay) * t
        if x0 < px < x1 and y0 < py < y1:
            return True
    return False


def proper_cross(p, q, r, s):
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    d1, d2 = cross(r, s, p), cross(r, s, q)
    d3, d4 = cross(p, q, r), cross(p, q, s)
    return ((d1 > 0 > d2) or (d1 < 0 < d2)) and ((d3 > 0 > d4) or (d3 < 0 < d4))


def collinear_len(p, q, r, s):
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
    """The render service anchors arrow-bound text on the middle vertex."""
    n = len(points)
    if n == 0:
        return None
    if n % 2 == 1:
        return points[n // 2]
    a, b = points[n // 2 - 1], points[n // 2]
    return ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)


def boundary_distance(pt, rect):
    x, y, w, h = rect
    dx = max(x - pt[0], 0.0, pt[0] - (x + w))
    dy = max(y - pt[1], 0.0, pt[1] - (y + h))
    if dx == 0 and dy == 0:
        return min(pt[0] - x, x + w - pt[0], pt[1] - y, y + h - pt[1])
    return math.hypot(dx, dy)


# ---- SVG parsing (hardened) --------------------------------------------------

def _parse_transform(text):
    ops = []
    for name, args in re.findall(r"([a-zA-Z]+)\(([^()]*)\)", text or ""):
        nums = [float(v) for v in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", args)]
        if name == "translate" and nums:
            ops.append((1.0, 0.0, 0.0, 1.0, nums[0], nums[1] if len(nums) > 1 else 0.0))
        elif name == "scale" and nums:
            sy = nums[1] if len(nums) > 1 else nums[0]
            ops.append((nums[0], 0.0, 0.0, sy, 0.0, 0.0))
        elif name == "matrix" and len(nums) >= 6:
            ops.append(tuple(nums[:6]))
    return ops


def _mul(m1, m2):
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return (a1 * a2 + c1 * b2, b1 * a2 + d1 * b2, a1 * c2 + c1 * d2,
            b1 * c2 + d1 * d2, a1 * e2 + c1 * f2 + e1, b1 * e2 + d1 * f2 + f1)


def _apply(m, x, y):
    a, b, c, d, e, f = m
    return (a * x + c * y + e, b * x + d * y + f)


def svg_extract(path):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    if "<!DOCTYPE" in raw or "<!ENTITY" in raw:
        raise ValueError("SVG contains DTD/ENTITY declarations; refusing to parse")
    root = ET.fromstring(raw)
    texts, boxes = [], []

    def walk(el, mat):
        local = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
        for op in _parse_transform(el.get("transform") or ""):
            local = _mul(local, op)
        cur = _mul(mat, local)
        tag = el.tag.split("}")[-1]
        if tag == "text":
            content = "".join(el.itertext()).strip()
            size = float(re.sub(r"[^0-9.]", "", el.get("font-size") or "0") or 0)
            x = float(el.get("x") or 0)
            y = float(el.get("y") or 0)
            ax, ay = _apply(cur, x, y)
            texts.append({"text": content, "x": round(ax, 2), "y": round(ay, 2),
                          "font_size": size, "fill": el.get("fill"),
                          "anchor": el.get("text-anchor")})
        elif tag == "rect":
            x = float(el.get("x") or 0)
            y = float(el.get("y") or 0)
            w = float(el.get("width") or 0)
            h = float(el.get("height") or 0)
            pts = [_apply(cur, x, y), _apply(cur, x + w, y), _apply(cur, x + w, y + h), _apply(cur, x, y + h)]
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            boxes.append({"x": round(min(xs), 2), "y": round(min(ys), 2),
                          "w": round(max(xs) - min(xs), 2), "h": round(max(ys) - min(ys), 2),
                          "fill": el.get("fill"), "kind": "rect"})
        elif tag == "path":
            d = el.get("d") or ""
            coords = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", d)
            nums = [float(v) for v in coords]
            pts = [_apply(cur, nums[i], nums[i + 1]) for i in range(0, len(nums) - 1, 2)]
            if pts:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                boxes.append({"x": round(min(xs), 2), "y": round(min(ys), 2),
                              "w": round(max(xs) - min(xs), 2), "h": round(max(ys) - min(ys), 2),
                              "fill": el.get("fill"), "kind": "path"})
        for child in el:
            walk(child, cur)

    walk(root, (1.0, 0.0, 0.0, 1.0, 0.0, 0.0))
    return {"texts": texts, "boxes": boxes}


# ---- readback -----------------------------------------------------------------

def readback(source_path, semantics, svg_path=None):
    scene = json.loads(Path(source_path).read_text(encoding="utf-8"))
    elements = scene.get("elements")
    if not isinstance(elements, list):
        raise ValueError("scene has no elements array")
    by_id = {e.get("id"): e for e in elements if isinstance(e, dict) and e.get("id")}

    sem_elements = semantics.get("elements") or []
    sem_zones = semantics.get("zones") or []
    sem_relations = semantics.get("relations") or []
    sem_zone_ids = {z["id"] for z in sem_zones}
    sem_element_ids = {e["id"] for e in sem_elements}
    sem_ids = sem_zone_ids | sem_element_ids
    sem_labels = {e["id"]: (e.get("label") or e["id"]) for e in sem_elements}
    sem_zone_labels = {z["id"]: (z.get("label") or z["id"]) for z in sem_zones}

    hard = []
    soft = []

    # actual rectangles and their bound texts
    rects = {}
    for e in elements:
        if e.get("type") == "rectangle" and e.get("id") in sem_ids:
            rects[e["id"]] = e
    for eid in sem_ids:
        if eid not in rects:
            hard.append({"code": "element-missing", "id": eid})
    for e in elements:
        if e.get("type") == "rectangle" and e.get("id") not in sem_ids:
            hard.append({"code": "element-extra", "id": e.get("id")})

    text_by_id = {e.get("id"): e for e in elements if e.get("type") == "text"}
    bound_texts = defaultdict(list)
    for t in elements:
        if t.get("type") == "text" and t.get("containerId"):
            bound_texts[t["containerId"]].append(t)
        if t.get("type") == "text" and t.get("containerId") and t["containerId"] not in by_id:
            hard.append({"code": "text-container-missing", "text": t.get("id"), "container": t["containerId"]})

    def reciprocal(container, text_id):
        return any((b or {}).get("id") == text_id for b in (container.get("boundElements") or []))

    components = []
    for eid in sorted(sem_element_ids):
        rect = rects.get(eid)
        if rect is None:
            continue
        texts = [t for t in bound_texts.get(eid, []) if t.get("containerId") == eid]
        label_actual = texts[0].get("text") if texts else None
        bound_ok = all(reciprocal(rect, t.get("id")) for t in texts) and bool(texts)
        components.append({"id": eid, "rect": [round(v, 2) for v in rect_of(rect)],
                           "label_semantic": sem_labels[eid], "label_native": label_actual,
                           "label_bound": bound_ok, "groupIds": rect.get("groupIds") or []})
        if label_actual != sem_labels[eid]:
            hard.append({"code": "label-mismatch", "id": eid, "expected": sem_labels[eid], "actual": label_actual})
        if not texts:
            hard.append({"code": "label-unbound", "id": eid})
        elif not bound_ok:
            hard.append({"code": "label-binding-not-reciprocal", "id": eid})

    zones = []
    zone_rects = {zid: rect_of(rects[zid]) for zid in sem_zone_ids if zid in rects}
    for z in sem_zones:
        zid = z["id"]
        rect = rects.get(zid)
        if rect is None:
            continue
        r = rect_of(rect)
        containers = [oid for oid, orect in zone_rects.items()
                      if oid != zid and rect_contains(orect, r) and (orect[2], orect[3]) != (r[2], r[3])]
        actual_parent = min(containers, key=lambda oid: zone_rects[oid][2] * zone_rects[oid][3]) if containers else None
        zones.append({"id": zid, "rect": [round(v, 2) for v in r],
                      "parent_semantic": z.get("parent"), "parent_native": actual_parent,
                      "groupIds": rect.get("groupIds") or []})
        if actual_parent != z.get("parent"):
            hard.append({"code": "zone-parent-mismatch", "id": zid,
                         "expected": z.get("parent"), "actual": actual_parent})

    for eid in sorted(sem_element_ids):
        rect = rects.get(eid)
        if rect is None:
            continue
        cx = rect["x"] + rect.get("width", 0) / 2.0
        cy = rect["y"] + rect.get("height", 0) / 2.0
        containers = [zid for zid, zr in zone_rects.items()
                      if zr[0] <= cx <= zr[0] + zr[2] and zr[1] <= cy <= zr[1] + zr[3]]
        actual_zone = min(containers, key=lambda zid: zone_rects[zid][2] * zone_rects[zid][3]) if containers else None
        expected_zone = next((e["zone"] for e in sem_elements if e["id"] == eid), None)
        if expected_zone != actual_zone:
            hard.append({"code": "zone-membership-mismatch", "id": eid,
                         "expected": expected_zone, "actual": actual_zone})

    # group sanity: a component rectangle and its bound label must share a group
    for comp in components:
        rect = rects.get(comp["id"])
        label_texts = bound_texts.get(comp["id"], [])
        if rect is not None and label_texts:
            shared = set(rect.get("groupIds") or []) & set(label_texts[0].get("groupIds") or [])
            if not shared:
                soft.append({"code": "group-not-shared-with-label", "id": comp["id"]})

    # relations
    arrows = {e.get("id"): e for e in elements if e.get("type") == "arrow"}
    sem_rel_ids = {r["id"] for r in sem_relations}
    for aid in arrows:
        if aid not in sem_rel_ids:
            hard.append({"code": "relation-extra", "id": aid})
    relations = []
    for rel in sem_relations:
        rid = rel["id"]
        a = arrows.get(rid)
        if a is None:
            hard.append({"code": "relation-missing", "id": rid})
            continue
        sb = a.get("startBinding") or {}
        eb = a.get("endBinding") or {}
        start_target = sb.get("elementId")
        end_target = eb.get("elementId")
        direction_ok = (start_target == rel["from"] and end_target == rel["to"])
        reversed_dir = (start_target == rel["to"] and end_target == rel["from"])
        if not direction_ok:
            hard.append({"code": "direction-reversed" if reversed_dir else "endpoint-mismatch",
                         "id": rid, "expected": [rel["from"], rel["to"]],
                         "actual": [start_target, end_target]})
        for target in (start_target, end_target):
            if target and target not in by_id:
                hard.append({"code": "endpoint-target-missing", "id": rid, "target": target})
            elif target and not any((b or {}).get("id") == rid for b in (by_id[target].get("boundElements") or [])):
                hard.append({"code": "endpoint-binding-not-reciprocal", "id": rid, "target": target})
        expected_zone_side = {(side, rel[label_side]) for side, label_side in (("start", "from"), ("end", "to"))
                              if rel[label_side] in sem_zone_ids}
        zone_parent = {z["id"]: z.get("parent") for z in sem_zones}
        elem_zone = {e["id"]: e["zone"] for e in sem_elements}

        def inside_zone(zone_id, ancestor):
            cur = zone_id
            while cur:
                if cur == ancestor:
                    return True
                cur = zone_parent.get(cur)
            return False

        for side, expected in (("start", rel["from"]), ("end", rel["to"])):
            actual = start_target if side == "start" else end_target
            if expected in sem_zone_ids and actual in sem_element_ids:
                owner = elem_zone.get(actual)
                if owner and inside_zone(owner, expected):
                    hard.append({"code": "endpoint-expanded-to-member", "id": rid,
                                 "side": side, "expected_zone": expected, "actual_element": actual})
        expected_label = rel.get("label") if isinstance(rel.get("label"), str) and rel["label"].strip() else None
        native_labels = [t for t in bound_texts.get(rid, []) if t.get("containerId") == rid]
        native_label = native_labels[0].get("text") if native_labels else None
        genuine = False
        if native_label is not None:
            genuine = any((b or {}).get("id") == native_labels[0].get("id") and (b or {}).get("type") == "text"
                          for b in (a.get("boundElements") or [])) and reciprocal_text(native_labels[0], rid, by_id)
        if expected_label != native_label:
            hard.append({"code": "relation-label-mismatch", "id": rid,
                         "expected": expected_label, "actual": native_label})
        elif expected_label is not None and not genuine:
            hard.append({"code": "relation-label-not-genuinely-bound", "id": rid})
        relations.append({
            "id": rid, "from_native": start_target, "to_native": end_target,
            "label_semantic": expected_label, "label_native": native_label,
            "label_genuinely_bound": genuine if expected_label is not None else None,
            "reciprocal": all(any((b or {}).get("id") == rid for b in (by_id[t].get("boundElements") or []))
                              for t in (start_target, end_target) if t in by_id),
            "points": [[round(v, 2) for v in (a["x"] + p[0], a["y"] + p[1])] for p in a.get("points") or []],
        })

    # zone-title content check (titles bound to a zone must carry the zone label)
    for t in elements:
        if t.get("type") != "text":
            continue
        cid = t.get("containerId")
        if cid in sem_zone_ids:
            expected = sem_zone_labels[cid]
            if (t.get("text") or "") != expected:
                hard.append({"code": "zone-title-mismatch", "id": cid,
                             "expected": expected, "actual": t.get("text")})

    # extra text detection (association + content, not an ID naming convention):
    # a text is expected when it is attached to a known object, or when its
    # content matches an expected string within the expected multiplicity.
    expected_content = Counter()
    for e in sem_elements:
        expected_content[sem_labels[e["id"]]] += 1
    for z in sem_zones:
        expected_content[sem_zone_labels[z["id"]]] += 1
    for rel in sem_relations:
        if isinstance(rel.get("label"), str) and rel["label"].strip():
            expected_content[rel["label"]] += 1
    title_text = (semantics.get("title") or "").strip()
    if title_text:
        expected_content[title_text] += 1
    used = Counter()
    extra_texts = []
    for t in elements:
        if t.get("type") != "text":
            continue
        cid = t.get("containerId")
        if cid in sem_ids or cid in sem_rel_ids:
            continue  # attached labels are validated by their own checks
        content = t.get("text") or ""
        if used[content] < expected_content.get(content, 0):
            used[content] += 1
            continue
        extra_texts.append({"id": t.get("id"), "text": content[:120], "containerId": cid})
    if extra_texts:
        hard.append({"code": "extra-text", "items": extra_texts})

    # geometry
    comp_rects = {c["id"]: tuple(c["rect"]) for c in components}
    zone_rect_map = {z["id"]: tuple(z["rect"]) for z in zones}
    through = []
    for rel in relations:
        pts = [tuple(p) for p in rel["points"]]
        ends = {rel["from_native"], rel["to_native"]}
        for k in range(len(pts) - 1):
            for cid, crect in comp_rects.items():
                if cid in ends:
                    continue
                if seg_rect_hit(pts[k], pts[k + 1], crect, pad=-1):
                    through.append({"relation": rel["id"], "component": cid, "segment": k})
    if through:
        hard.append({"code": "edge-through-component", "items": through})

    endpoint_rows = []
    for rel in relations:
        pts = [tuple(p) for p in rel["points"]]
        for side, target in (("start", rel["from_native"]), ("end", rel["to_native"])):
            rect = comp_rects.get(target) or zone_rect_map.get(target)
            if rect is None:
                continue
            pt = pts[0] if side == "start" else pts[-1]
            dist = boundary_distance(pt, rect)
            endpoint_rows.append({"relation": rel["id"], "side": side, "target": target,
                                  "boundary_distance": round(dist, 2)})
            if dist > EDGE_ON_BOUNDARY_TOL:
                hard.append({"code": "endpoint-off-boundary", "id": rel["id"], "side": side,
                             "distance": round(dist, 2)})

    label_rows = []
    for rel in relations:
        if rel["label_semantic"] is None:
            continue
        pts = [tuple(p) for p in rel["points"]]
        anchor = label_anchor(pts)
        box = (anchor[0] - est_width(rel["label_semantic"], FONT_LABEL) * LABEL_INFLATE / 2.0,
               anchor[1] - est_height(FONT_LABEL) * LABEL_INFLATE / 2.0,
               est_width(rel["label_semantic"], FONT_LABEL) * LABEL_INFLATE,
               est_height(FONT_LABEL) * LABEL_INFLATE)
        hits = [cid for cid, crect in comp_rects.items()
                if cid not in (rel["from_native"], rel["to_native"]) and overlap_area(box, crect, pad=3) > 0]
        label_rows.append({"relation": rel["id"], "anchor": [round(v, 2) for v in anchor],
                           "anchor_box": [round(v, 2) for v in box], "over_components": hits})
        if hits:
            hard.append({"code": "label-over-component", "id": rel["id"], "components": hits})

    crossing_pairs = []
    overlaps = 0.0
    rels = [r for r in relations if r["points"]]
    for i in range(len(rels)):
        for j in range(i + 1, len(rels)):
            A = [tuple(p) for p in rels[i]["points"]]
            B = [tuple(p) for p in rels[j]["points"]]
            hit = False
            for k in range(len(A) - 1):
                for m in range(len(B) - 1):
                    if proper_cross(A[k], A[k + 1], B[m], B[m + 1]):
                        hit = True
                    overlaps += collinear_len(A[k], A[k + 1], B[m], B[m + 1])
            if hit:
                crossing_pairs.append([rels[i]["id"], rels[j]["id"]])

    # SVG evidence (optional)
    svg_checks = {"provided": bool(svg_path), "status": "not_evaluated"}
    if svg_path:
        svg = svg_extract(svg_path)
        expected_strings = Counter()
        for e in sem_elements:
            expected_strings[sem_labels[e["id"]]] += 1
        for z in sem_zones:
            expected_strings[sem_zone_labels[z["id"]]] += 1
        for rel in sem_relations:
            if isinstance(rel.get("label"), str) and rel["label"].strip():
                expected_strings[rel["label"]] += 1
        title = (semantics.get("title") or "").strip()
        if title:
            expected_strings[title] += 1
        rendered = Counter(t["text"] for t in svg["texts"] if t["text"])
        missing = [s for s in expected_strings if rendered.get(s, 0) < expected_strings[s]]
        extra = [s for s in rendered if s not in expected_strings]
        # renderer anchor rule check: shift = svg_center - middle_vertex (scene space).
        # Duplicate label strings exist (a component label may equal a relation label),
        # so a relation label is matched by content AND arrow colour first.
        shifts = []
        text_centers = {}
        for t in svg["texts"]:
            text_centers.setdefault(t["text"], []).append(t)
        for rel in relations:
            if rel["label_semantic"] is None:
                continue
            cands = text_centers.get(rel["label_semantic"]) or []
            if not cands:
                continue
            arrow_color = (arrows.get(rel["id"], {}).get("strokeColor") or "").lower()
            colored = [t for t in cands if (t["fill"] or "").lower() == arrow_color and arrow_color]
            t = (colored or cands)[0]
            anchor = label_anchor([tuple(p) for p in rel["points"]])
            center_x = t["x"]
            center_y = t["y"] + (t["font_size"] or FONT_LABEL) * 1.25 / 2.0
            shifts.append({"relation": rel["id"],
                           "shift": [round(center_x - anchor[0], 2), round(center_y - anchor[1], 2)]})
        shift_consistent = None
        if len(shifts) >= 2:
            xs = [s["shift"][0] for s in shifts]
            ys = [s["shift"][1] for s in shifts]
            shift_consistent = (max(xs) - min(xs) <= 3.0) and (max(ys) - min(ys) <= 3.0)
        # label boxes vs component-sized boxes in the same SVG space
        comp_sizes = {(round(c[2]), round(c[3])) for c in comp_rects.values()}
        comp_boxes_svg = [b for b in svg["boxes"]
                          if (round(b["w"]), round(b["h"])) in comp_sizes and b["w"] > 4 and b["h"] > 4]
        label_overlaps = []
        chosen = {}
        for rel in relations:
            if rel["label_semantic"] is None:
                continue
            cands = text_centers.get(rel["label_semantic"]) or []
            if not cands:
                continue
            arrow_color = (arrows.get(rel["id"], {}).get("strokeColor") or "").lower()
            colored = [t for t in cands if (t["fill"] or "").lower() == arrow_color and arrow_color]
            t = (colored or cands)[0]
            chosen[rel["id"]] = t
            w = est_width(rel["label_semantic"], t["font_size"] or FONT_LABEL)
            h = (t["font_size"] or FONT_LABEL) * 1.3
            box = (t["x"] - w / 2.0, t["y"], w, h)
            hits = [b for b in comp_boxes_svg if overlap_area(box, (b["x"], b["y"], b["w"], b["h"]), pad=2) > 0]
            if hits:
                label_overlaps.append({"relation": rel["id"], "component_boxes_in_svg": len(hits)})
        # If no component-sized shape could be matched (parser/format limitation), the
        # direct check is blind. Say so, and fall back to mapping the native component
        # rects through the measured constant export shift (only valid while the shift
        # is consistent), so a rendered label over a box is still detected.
        mapped_overlaps = []
        consensus_shift = None
        if shift_consistent and shifts:
            consensus_shift = (round(sum(s["shift"][0] for s in shifts) / len(shifts), 2),
                               round(sum(s["shift"][1] for s in shifts) / len(shifts), 2))
            for rel in relations:
                if rel["label_semantic"] is None or rel["id"] not in chosen:
                    continue
                t = chosen[rel["id"]]
                w = est_width(rel["label_semantic"], t["font_size"] or FONT_LABEL)
                h = (t["font_size"] or FONT_LABEL) * 1.3
                box = (t["x"] - w / 2.0, t["y"], w, h)
                ends = {rel["from_native"], rel["to_native"]}
                hits = []
                for cid, crect in comp_rects.items():
                    if cid in ends:
                        continue
                    mapped = (crect[0] + consensus_shift[0], crect[1] + consensus_shift[1], crect[2], crect[3])
                    if overlap_area(box, mapped, pad=2) > 0:
                        hits.append(cid)
                if hits:
                    mapped_overlaps.append({"relation": rel["id"], "components": hits})
        if comp_boxes_svg:
            direct_status = "pass" if not label_overlaps else "fail"
        else:
            direct_status = "unsupported: no component-sized shape matched in the SVG (parser/format limitation)"
        svg_checks = {
            "provided": True,
            "text_nodes": len(svg["texts"]),
            "expected_multiset": dict(expected_strings),
            "missing_strings": missing,
            "extra_strings": extra,
            "anchor_shift_per_label": shifts,
            "anchor_shift_consistent": shift_consistent,
            "consensus_shift": consensus_shift,
            "component_sized_boxes_in_svg": len(comp_boxes_svg),
            "label_over_component_boxes_svg": label_overlaps,
            "label_over_component_boxes_svg_mapped": mapped_overlaps,
            "component_box_check": direct_status,
            "identity": "partial-by-design: Excalidraw SVG flattens text; identity is a text multiset",
            "status": "pass" if not missing and not extra and not label_overlaps and not mapped_overlaps else "fail",
        }
        if missing:
            hard.append({"code": "svg-missing-text", "items": missing})
        if extra:
            hard.append({"code": "svg-extra-text", "items": extra})
        if label_overlaps:
            hard.append({"code": "svg-label-over-component", "items": label_overlaps})
        if mapped_overlaps:
            hard.append({"code": "svg-label-over-component-mapped", "items": mapped_overlaps})
        if not comp_boxes_svg:
            soft.append({"code": "svg-component-boxes-unmatched",
                         "detail": "no component-sized shape matched in the SVG; the direct box check is blind, "
                                   "the mapped check used the measured export shift" + ("" if consensus_shift else " (unavailable: shift inconsistent)")})
        if shift_consistent is False:
            soft.append({"code": "renderer-anchor-shift-inconsistent"})
    else:
        soft.append({"code": "svg-evidence-missing"})

    interactions = "not_evaluated"
    soft_limitations = [
        "Label boxes use estimated font widths inflated 12%; the renderer re-measures with real fonts.",
        "Arrow tip positions are checked on native coordinates; they are not re-extracted from SVG path geometry.",
        "SVG has no stable semantic IDs (engine limitation); SVG identity is a text multiset plus label/box geometry.",
        "Excalidraw editor import/drag/selection was not exercised: interaction is not_evaluated.",
    ]

    status = "fail" if hard else ("partial" if soft else "pass")
    report = {
        "engine": ENGINE,
        "readback_version": VERSION,
        "source": {"path": str(source_path), "sha256": sha256_file(source_path),
                   "bytes": Path(source_path).stat().st_size},
        "semantics": {"path": str(semantics.get("__path__", "")) if semantics.get("__path__") else None,
                      "sha256": semantics.get("__sha256__")},
        "actual_counts": {
            "components": len([c for c in components]),
            "zones": len(zones),
            "relations": len(relations),
            "relation_labels_genuine": sum(1 for r in relations if r["label_genuinely_bound"]),
        },
        "records": {"components": components, "zones": zones, "relations": relations},
        "actual": {
            "counts": {
                "components": len([c for c in components]),
                "zones": len(zones),
                "relations": len(relations),
                "relation_labels_genuine": sum(1 for r in relations if r["label_genuinely_bound"]),
            },
            "records": {"components": components, "zones": zones, "relations": relations},
        },
        "semantic": {
            "status": "fail" if any(h["code"] in (
                "element-missing", "element-extra", "label-mismatch", "label-unbound",
                "label-binding-not-reciprocal", "zone-parent-mismatch", "zone-membership-mismatch",
                "relation-missing", "relation-extra", "direction-reversed", "endpoint-mismatch",
                "endpoint-target-missing", "endpoint-binding-not-reciprocal",
                "endpoint-expanded-to-member", "relation-label-mismatch",
                "relation-label-not-genuinely-bound", "extra-text", "text-container-missing") for h in hard) else "pass",
            "diff": hard,
        },
        "geometry": {
            "status": "fail" if any(h["code"] in ("edge-through-component", "label-over-component",
                                                  "endpoint-off-boundary") for h in hard) else "pass",
            "edge_through_component": through,
            "endpoints": endpoint_rows,
            "labels": label_rows,
            "crossings": {"measured": True,
                          "method": "strict proper intersections of native orthogonal segments",
                          "pair_count": len(crossing_pairs), "pairs": crossing_pairs},
            "collinear_overlap_px": round(overlaps, 1),
        },
        "svg": svg_checks,
        "binding_summary": {
            "component_labels_bound": sum(1 for c in components if c["label_bound"]),
            "component_labels_total": len(components),
            "relation_endpoints_reciprocal": sum(1 for r in relations if r["reciprocal"]),
            "relation_labels_genuine": sum(1 for r in relations if r["label_genuinely_bound"]),
            "relation_labels_expected": sum(1 for r in relations if r["label_semantic"]),
        },
        "issues": hard,
        "soft_issues": soft,
        "unsupported_or_not_evaluated": soft_limitations + [
            "user satisfaction: not_evaluated",
            "interaction: " + interactions,
        ],
"overall_status": status,
        "overall": status,
        "visual": {
            "status": "fail" if any(h["code"] in ("edge-through-component", "label-over-component",
                                                  "endpoint-off-boundary", "svg-missing-text",
                                                  "svg-extra-text", "svg-label-over-component",
                                                  "svg-label-over-component-mapped") for h in hard)
                      else ("partial" if soft else "pass"),
            "svg": svg_checks,
            "geometry": {
                "edge_through_component": through,
                "endpoints": endpoint_rows,
                "labels": label_rows,
                "crossings": {"measured": True,
                              "method": "strict proper intersections of native orthogonal segments",
                              "pair_count": len(crossing_pairs), "pairs": crossing_pairs},
                "collinear_overlap_px": round(overlaps, 1),
            },
            "issues": hard,
            "limitations": [s.get("detail") or s.get("code") for s in soft] + soft_limitations,
        },
        "unsupported": [],
        "not_evaluated": list(soft_limitations) + ["user_satisfaction:", "interaction:" + interactions],
        "exit_code_meaning": {
            "0": "pass: no hard discrepancy and no partial evidence gap",
            "1": "hard failure: a semantic/geometry/binding discrepancy (never a pass)",
            "2": "usage or I/O error (unknown flag, missing file, invalid JSON, existing output)",
            "3": "partial: no hard discrepancy, but evidence is missing/limited (not a pass)",
        },
    }
    return report, status


def reciprocal_text(text, arrow_id, by_id):
    """A bound label is genuine only when its arrow registers the text back."""
    arrow = by_id.get(arrow_id)
    if arrow is None:
        return False
    refs = [b for b in (arrow.get("boundElements") or []) if (b or {}).get("type") == "text"]
    return any((b or {}).get("id") == text.get("id") for b in refs)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="native-readback.py",
        description="Independent readback of an Excalidraw scene (and optional SVG) against semantics.",
        epilog="exit codes: 0 pass; 1 hard discrepancy; 2 usage/IO/parse error; 3 partial (evidence gap). Partial is not a pass.",
    )
    parser.add_argument("--source", required=True, help="produced .excalidraw scene")
    parser.add_argument("--semantics", required=True, help="authoritative semantics JSON")
    parser.add_argument("--svg", help="actual rendered SVG (optional; without it visual is partial)")
    parser.add_argument("--output", required=True, help="new report JSON path (must not exist)")
    parser.add_argument("--version", action="version", version=f"native-readback.py {VERSION}")
    args = parser.parse_args(argv)

    out = Path(args.output)
    if out.exists():
        print(f"error: refusing to overwrite existing report: {out}", file=sys.stderr)
        return 2
    try:
        semantics = json.loads(Path(args.semantics).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read semantics: {exc}", file=sys.stderr)
        return 2
    semantics["__path__"] = str(args.semantics)
    semantics["__sha256__"] = sha256_file(args.semantics)
    if not Path(args.source).is_file():
        print(f"error: source not found: {args.source}", file=sys.stderr)
        return 2
    if args.svg and not Path(args.svg).is_file():
        print(f"error: svg not found: {args.svg}", file=sys.stderr)
        return 2
    try:
        report, status = readback(args.source, semantics, args.svg)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: readback failed: {exc}", file=sys.stderr)
        return 2
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(out), "overall_status": status,
                      "semantic": report["semantic"]["status"],
                      "geometry": report["geometry"]["status"],
                      "svg": report["svg"].get("status"),
                      "hard": len(report["issues"]),
                      "crossings": report["geometry"]["crossings"]["pair_count"]},
                     ensure_ascii=False))
    return {"pass": 0, "fail": 1, "partial": 3}[status]


if __name__ == "__main__":
    sys.exit(main())
