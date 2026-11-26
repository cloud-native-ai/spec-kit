#!/usr/bin/env python3
"""native-readback.py — d3js native-source readback and semantic/visual validation.

Reads the ACTUAL d3js native artifact (HTML with an executable data script, a JSON
data file, or a JS data file), extracts the drawing records from that file only, and
compares them with the authoritative semantics JSON. When a rendered SVG is given,
it also reads the SVG identity/labels/geometry and checks them.

Extraction rules (the defect this closes): only <script> content is considered. A
data block must be a strictly parseable JSON object literal (`const NAME = {...}` /
`NAME = {...}`) or a `<script type="application/json">` object. Documentation
copies inside <pre>/<code>, HTML-escaped text (&quot;), commented-out code and
non-literal assignments are recorded as rejected occurrences and are never used.
If two DIFFERENT valid data objects exist, the result is 'ambiguous' (exit 3) — the
reader does not pick one merely because it appears first. Records are never copied
from --semantics.

Identity contract (documented for this engine):
  * preferred: data-node-id / data-zone-id / data-edge-id attributes (or, on an
    element, data-* on its nearest ancestor group);
  * legacy: id="node-<id>", id="zone-<id>", id="edge-<id>" with the FULL remainder
    equal to the record id — arbitrary substring coincidence is not accepted.
Legend contract: legend rows declare data-legend-kind="style"|"interaction". Any
undeclared legend text, any other kind, or a legacy legend that cannot be verified
is reported (declared-format extra semantics are a hard issue).

Usage:
  native-readback.py --source <native> --semantics <semantics.json>
                     [--svg <rendered.svg>] --output <new-report.json>

Exit codes: 0 overall pass; 1 hard discrepancy (semantic/identity/visual fail);
3 partial or unsupported (not a pass); 2 usage or I/O error (including refusing to
overwrite an existing --output).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

VERSION = "1.0.0"
TOOL = "native-readback"
ENGINE = "d3js"

JS_MIME_PREFIXES = ("text/javascript", "application/javascript", "module", "text/ecmascript")
JSON_SCRIPT_TYPES = ("application/json", "application/ld+json")
REQUIRED_RECORD_KEYS = ("elements", "zones", "relations")
COLOR_HEX6 = re.compile(r"^#[0-9a-f]{6}$")
COLOR_HEX3 = re.compile(r"^#[0-9a-f]{3}$")
COLOR_RGB = re.compile(r"^rgba?\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})")
ASSIGN = re.compile(r"(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*$")
BARE_ASSIGN = re.compile(r"((?:window\.)?[A-Za-z_$][\w$]*)\s*=\s*$")


class UsageError(Exception):
    pass


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_color(value):
    if not isinstance(value, str):
        return None
    text = value.strip().lower()
    if COLOR_HEX6.match(text):
        return text
    if COLOR_HEX3.match(text):
        return "#" + "".join(ch * 2 for ch in text[1:])
    match = COLOR_RGB.match(text)
    if match:
        return "#" + "".join("%02x" % max(0, min(255, int(part))) for part in match.groups())
    return text


def est_text_width(text, font_size=13.0):
    """Estimator shared with build-native.py (documented approximation, not a measurement)."""
    total = 0.0
    for ch in text or "":
        total += font_size * (1.0 if ord(ch) > 127 else 0.6)
    return total


class ScriptCollector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.scripts = []
        self._current = None

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self._current = {"attrs": dict(attrs), "text": []}

    def handle_endtag(self, tag):
        if tag == "script" and self._current is not None:
            raw = "".join(self._current["text"])
            self.scripts.append({"index": len(self.scripts),
                                 "type": (self._current["attrs"].get("type") or "").strip().lower(),
                                 "src": self._current["attrs"].get("src"),
                                 "id": self._current["attrs"].get("id"),
                                 "text": raw})
            self._current = None

    def handle_data(self, data):
        if self._current is not None:
            self._current["text"].append(data)

    def handle_entityref(self, name):
        if self._current is not None:
            self._current["text"].append("&%s;" % name)

    def handle_charref(self, name):
        if self._current is not None:
            self._current["text"].append("&#%s;" % name)


def scan_object_literal(text, start):
    """Return the balanced {...} literal starting at text[start] == '{' (strings/comments aware)."""
    depth = 0
    i = start
    quote = None
    escaped = False
    while i < len(text):
        ch = text[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
        else:
            if ch in ("'", '"', "`"):
                quote = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
        i += 1
    return None


def record_shape_ok(data):
    if not isinstance(data, dict):
        return False, "not-an-object"
    missing = [key for key in REQUIRED_RECORD_KEYS if not isinstance(data.get(key), list)]
    if missing:
        return False, "missing-arrays:" + ",".join(missing)
    for key in REQUIRED_RECORD_KEYS:
        if not all(isinstance(item, dict) for item in data[key]):
            return False, "non-object-entry-in:" + key
    return True, "ok"


def js_code_mask(text):
    """1 = outside strings/comments; 0 = inside a string or comment (conservative)."""
    mask = bytearray(b"\x01") * len(text)
    index = 0
    quote = None
    escaped = False
    line_comment = False
    block_comment = False
    while index < len(text):
        ch = text[index]
        nxt = text[index + 1] if index + 1 < len(text) else ""
        if quote:
            mask[index] = 0
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
        elif line_comment:
            mask[index] = 0
            if ch == "\n":
                line_comment = False
        elif block_comment:
            mask[index] = 0
            if ch == "*" and nxt == "/":
                mask[index + 1] = 0
                block_comment = False
                index += 1
        elif ch in ("'", '"', "`"):
            mask[index] = 0
            quote = ch
        elif ch == "/" and nxt == "/":
            mask[index] = 0
            mask[index + 1] = 0
            line_comment = True
            index += 1
        elif ch == "/" and nxt == "*":
            mask[index] = 0
            mask[index + 1] = 0
            block_comment = True
            index += 1
        index += 1
    return mask


def extract_from_js(text, script_index, rejected):
    """Yield candidate data objects found in a classic script block."""
    candidates = []
    mask = js_code_mask(text)
    for match in re.finditer(r"=\s*", text):
        if not mask[match.start()]:
            continue
        if not mask[match.end() - 1]:
            continue
        assign_ctx = text[max(0, match.start() - 120):match.start() + 1]
        if "==" in text[match.start():match.start() + 2] or text[match.start() + 1:match.start() + 2] == "=":
            continue
        brace = text.find("{", match.end(), match.end() + 400)
        if brace < 0 or not mask[brace]:
            continue
        between = text[match.end():brace]
        if between.strip() != "":
            if "JSON.parse" in between or "parse(" in between:
                rejected.append({"script": script_index, "kind": "non-literal-assignment",
                                 "reason": "value is not a JSON object literal (e.g. JSON.parse/build)",
                                 "at": match.start()})
            continue
        literal = scan_object_literal(text, brace)
        if literal is None:
            rejected.append({"script": script_index, "kind": "unbalanced-literal",
                             "reason": "object literal is not closed", "at": brace})
            continue
        try:
            data = json.loads(literal)
        except Exception as exc:  # noqa: BLE001
            rejected.append({"script": script_index, "kind": "not-json",
                             "reason": "%s: %s" % (type(exc).__name__, str(exc)[:160]),
                             "snippet": literal[:80].replace("\n", " ")})
            continue
        ok, reason = record_shape_ok(data)
        if ok:
            name_match = ASSIGN.search(assign_ctx) or BARE_ASSIGN.search(assign_ctx)
            candidates.append({"script": script_index,
                               "name": name_match.group(1) if name_match else "",
                               "data": data})
    return candidates


def extract_native(source_path):
    suffix = source_path.suffix.lower()
    rejected = []
    candidates = []
    scripts = []
    if suffix in (".html", ".htm"):
        parser = ScriptCollector()
        parser.feed(source_path.read_text(encoding="utf-8", errors="replace"))
        scripts = parser.scripts
        for script in scripts:
            stype = script["type"]
            if script.get("src"):
                continue
            if stype in JSON_SCRIPT_TYPES:
                try:
                    data = json.loads(script["text"])
                except Exception as exc:  # noqa: BLE001
                    rejected.append({"script": script["index"], "kind": "json-script-invalid",
                                     "reason": "%s: %s" % (type(exc).__name__, str(exc)[:160])})
                    continue
                ok, _ = record_shape_ok(data)
                if ok:
                    candidates.append({"script": script["index"], "name": script.get("id") or "",
                                       "data": data})
                else:
                    rejected.append({"script": script["index"], "kind": "json-script-shape",
                                     "reason": "application/json block without elements/zones/relations arrays"})
                continue
            if stype and not stype.startswith(JS_MIME_PREFIXES):
                continue
            candidates.extend(extract_from_js(script["text"], script["index"], rejected))
    elif suffix == ".json":
        try:
            data = json.loads(source_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            rejected.append({"script": 0, "kind": "json-file-invalid",
                             "reason": "%s: %s" % (type(exc).__name__, str(exc)[:160])})
            data = None
        if data is not None:
            ok, _ = record_shape_ok(data)
            if ok:
                candidates.append({"script": 0, "name": "", "data": data})
    else:
        text = source_path.read_text(encoding="utf-8", errors="replace")
        candidates.extend(extract_from_js(text, 0, rejected))

    # keep only the first occurrence of each distinct canonical payload
    distinct = {}
    for cand in candidates:
        key = hashlib.sha256(json.dumps(cand["data"], sort_keys=True,
                                        ensure_ascii=False).encode("utf-8")).hexdigest()
        if key not in distinct:
            distinct[key] = dict(cand, canonical_sha256=key)
            distinct[key]["occurrences"] = 1
        else:
            distinct[key]["occurrences"] += 1

    # an SDS mention that produced no candidate is an explicit unsupported outcome
    mentions = []
    for script in scripts:
        if re.search(r"\bSDS\b", script["text"]):
            mentions.append(script["index"])

    extraction = {
        "method": "script-only JSON-literal extraction (HTMLParser; <pre>/<code>/escaped text excluded)",
        "scripts_scanned": len(scripts),
        "candidates": [
            {"script": cand["script"], "name": cand["name"], "sha256": cand["canonical_sha256"],
             "occurrences": cand["occurrences"],
             "counts": {key: len(cand["data"][key]) for key in REQUIRED_RECORD_KEYS}}
            for cand in distinct.values()
        ],
        "rejected": rejected,
        "sds_mentions_without_literal": mentions,
    }
    if len(distinct) > 1:
        extraction["status"] = "ambiguous"
        extraction["detail"] = ("two or more DIFFERENT parseable data objects were found; "
                                "refusing to choose one")
        return None, extraction
    if not distinct:
        extraction["status"] = "unsupported" if (rejected or mentions) else "missing"
        extraction["detail"] = ("no parseable data-script object; see rejected occurrences"
                                if (rejected or mentions) else "no data-script object found")
        return None, extraction
    extraction["status"] = "ok"
    chosen = next(iter(distinct.values()))
    return chosen, extraction


def load_json(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise UsageError("cannot read JSON %s: %s" % (path, exc))
    if not isinstance(data, dict):
        raise UsageError("%s: expected a JSON object" % path)
    return data


def record_maps(sds):
    elements, zones, relations = {}, {}, {}
    issues = {"malformed_elements": [], "malformed_zones": [], "malformed_relations": []}
    for item in sds.get("elements") or []:
        if not isinstance(item, dict) or not item.get("id"):
            issues["malformed_elements"].append(item)
            continue
        if item["id"] in elements:
            issues["malformed_elements"].append({"duplicate_id": item["id"]})
            continue
        elements[item["id"]] = {"label": item.get("label"), "zone": item.get("zone")}
    for item in sds.get("zones") or []:
        if not isinstance(item, dict) or not item.get("id"):
            issues["malformed_zones"].append(item)
            continue
        if item["id"] in zones:
            issues["malformed_zones"].append({"duplicate_id": item["id"]})
            continue
        zones[item["id"]] = {"label": item.get("label"), "parent": item.get("parent")}
    for item in sds.get("relations") or []:
        if not isinstance(item, dict) or not item.get("id"):
            issues["malformed_relations"].append(item)
            continue
        if item["id"] in relations:
            issues["malformed_relations"].append({"duplicate_id": item["id"]})
            continue
        relations[item["id"]] = {
            "from": item.get("from"), "to": item.get("to"),
            "label": item.get("label"), "color": item.get("color"),
        }
    return elements, zones, relations, issues


def compare_records(expected, actual):
    exp_el, exp_zn, exp_rel, exp_mal = record_maps(expected)
    act_el, act_zn, act_rel, act_mal = record_maps(actual)

    diff = {
        "elements": {"missing": sorted(set(exp_el) - set(act_el)),
                     "extra": sorted(set(act_el) - set(exp_el)),
                     "label_mismatch": [], "zone_mismatch": []},
        "zones": {"missing": sorted(set(exp_zn) - set(act_zn)),
                  "extra": sorted(set(act_zn) - set(exp_zn)),
                  "label_mismatch": [], "parent_mismatch": []},
        "relations": {"missing": sorted(set(exp_rel) - set(act_rel)),
                      "extra": sorted(set(act_rel) - set(exp_rel)),
                      "endpoint_mismatch": [], "label_mismatch": [], "color_mismatch": []},
        "malformed": {key: value for key, value in act_mal.items() if value},
        "duplicate_ids": (
            [item["duplicate_id"] for item in act_mal["malformed_elements"]
             if isinstance(item, dict) and "duplicate_id" in item]
            + [item["duplicate_id"] for item in act_mal["malformed_zones"]
               if isinstance(item, dict) and "duplicate_id" in item]
            + [item["duplicate_id"] for item in act_mal["malformed_relations"]
               if isinstance(item, dict) and "duplicate_id" in item]
        ),
        "container_expanded": [],
        "endpoint_collapsed": [],
    }
    for key in act_mal:
        if exp_mal.get(key):
            diff["malformed"]["expected_" + key] = exp_mal[key]
    for eid in sorted(set(exp_el) & set(act_el)):
        if (exp_el[eid]["label"] or "") != (act_el[eid]["label"] or ""):
            diff["elements"]["label_mismatch"].append(
                {"id": eid, "expected": exp_el[eid]["label"], "actual": act_el[eid]["label"]})
        if exp_el[eid]["zone"] != act_el[eid]["zone"]:
            diff["elements"]["zone_mismatch"].append(
                {"id": eid, "expected": exp_el[eid]["zone"], "actual": act_el[eid]["zone"]})
    for zid in sorted(set(exp_zn) & set(act_zn)):
        if (exp_zn[zid]["label"] or "") != (act_zn[zid]["label"] or ""):
            diff["zones"]["label_mismatch"].append(
                {"id": zid, "expected": exp_zn[zid]["label"], "actual": act_zn[zid]["label"]})
        if exp_zn[zid]["parent"] != act_zn[zid]["parent"]:
            diff["zones"]["parent_mismatch"].append(
                {"id": zid, "expected": exp_zn[zid]["parent"], "actual": act_zn[zid]["parent"]})
    for rid in sorted(set(exp_rel) & set(act_rel)):
        exp, act = exp_rel[rid], act_rel[rid]
        if (exp["from"], exp["to"]) != (act["from"], act["to"]):
            diff["relations"]["endpoint_mismatch"].append(
                {"id": rid, "expected": [exp["from"], exp["to"]], "actual": [act["from"], act["to"]]})
        if (exp.get("label") or "") != (act.get("label") or ""):
            diff["relations"]["label_mismatch"].append(
                {"id": rid, "expected": exp.get("label"), "actual": act.get("label")})
        if canonical_color(exp.get("color")) != canonical_color(act.get("color")):
            diff["relations"]["color_mismatch"].append(
                {"id": rid, "expected": exp.get("color"), "actual": act.get("color")})
    # container-endpoint contract: a zone endpoint must not be replaced by one of its members
    for rid in sorted(set(exp_rel) & set(act_rel)):
        exp, act = exp_rel[rid], act_rel[rid]
        for side in ("from", "to"):
            exp_id, act_id = exp[side], act[side]
            if exp_id in exp_zn and exp_id not in exp_el:
                if act_id in exp_el and exp_el[act_id]["zone"] == exp_id:
                    diff["container_expanded"].append({"id": rid, "side": side,
                                                       "zone": exp_id, "member": act_id})
            elif exp_id in exp_el and exp_id not in exp_zn:
                if act_id in exp_zn and exp_el[exp_id]["zone"] == act_id:
                    diff["endpoint_collapsed"].append({"id": rid, "side": side,
                                                       "element": exp_id, "zone": act_id})

    def duplicate_labels(mapping):
        buckets = {}
        for rid, rec in mapping.items():
            label = rec.get("label")
            if label:
                buckets.setdefault(label, []).append(rid)
        return {label: sorted(ids) for label, ids in buckets.items() if len(ids) > 1}

    duplicate_labels_report = {
        "expected_elements": duplicate_labels(exp_el),
        "actual_elements": duplicate_labels(act_el),
        "expected_zones": duplicate_labels(exp_zn),
        "actual_zones": duplicate_labels(act_zn),
    }
    hard = any([
        diff["elements"]["missing"], diff["elements"]["extra"],
        diff["zones"]["missing"], diff["zones"]["extra"],
        diff["relations"]["missing"], diff["relations"]["extra"],
        diff["elements"]["label_mismatch"], diff["elements"]["zone_mismatch"],
        diff["zones"]["label_mismatch"], diff["zones"]["parent_mismatch"],
        diff["relations"]["endpoint_mismatch"], diff["relations"]["label_mismatch"],
        diff["relations"]["color_mismatch"], diff["container_expanded"],
        diff["endpoint_collapsed"], diff["duplicate_ids"],
        any(diff["malformed"].values()),
        duplicate_labels_report["expected_elements"] != duplicate_labels_report["actual_elements"],
        duplicate_labels_report["expected_zones"] != duplicate_labels_report["actual_zones"],
    ])
    return diff, duplicate_labels_report, ("fail" if hard else "pass")


# ---------------------------------------------------------------- SVG readback

def local_name(tag):
    return tag.split("}", 1)[1] if "}" in tag else tag


def class_tokens(element):
    return set((element.get("class") or "").split())


def collect_svg_ids(root):
    nodes, zones, edges = {}, {}, {}
    modes = {"node": set(), "zone": set(), "edge": set()}
    duplicates = []
    for element in root.iter():
        tag = local_name(element.tag)
        if tag in ("defs", "style", "title", "desc", "marker"):
            continue
        node_id = element.get("data-node-id")
        if node_id:
            if node_id in nodes:
                duplicates.append({"kind": "node", "id": node_id})
            else:
                nodes[node_id] = element
                modes["node"].add("data-attr")
            continue
        zone_id = element.get("data-zone-id")
        if zone_id:
            if zone_id in zones:
                duplicates.append({"kind": "zone", "id": zone_id})
            else:
                zones[zone_id] = element
                modes["zone"].add("data-attr")
            continue
        elem_id = element.get("id") or ""
        if tag == "g" and elem_id.startswith("node-"):
            rid = elem_id[len("node-"):]
            if rid not in nodes:
                nodes[rid] = element
                modes["node"].add("legacy-prefix")
            continue
        if tag == "g" and elem_id.startswith("zone-"):
            rid = elem_id[len("zone-"):]
            if rid not in zones:
                zones[rid] = element
                modes["zone"].add("legacy-prefix")
            continue
        data_edge = element.get("data-edge-id")
        tokens = class_tokens(element)
        is_edge_group = (tag == "g" and ("edge" in tokens or elem_id.startswith("edge-")))
        if is_edge_group:
            rid = data_edge or (elem_id[len("edge-"):] if elem_id.startswith("edge-") else None)
            if rid and rid not in edges:
                edges[rid] = element
                modes["edge"].add("data-attr" if data_edge else "legacy-prefix")
    return nodes, zones, edges, modes, duplicates


def find_text(element):
    for descendant in element.iter():
        if local_name(descendant.tag) == "text":
            return "".join(descendant.itertext()).strip()
    return None


def parse_number(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_transform(transform):
    if not transform:
        return None
    match = re.search(r"translate\(\s*(-?[0-9.]+)[ ,]+(-?[0-9.]+)", transform)
    if match:
        return parse_number(match.group(1)), parse_number(match.group(2))
    return None


def svg_box(group):
    if group is None:
        return None
    transform = parse_transform(group.get("transform"))
    for descendant in group.iter():
        if local_name(descendant.tag) != "rect":
            continue
        x = parse_number(descendant.get("x"), 0.0)
        y = parse_number(descendant.get("y"), 0.0)
        w = parse_number(descendant.get("width"), 0.0)
        h = parse_number(descendant.get("height"), 0.0)
        if w and h:
            if transform:
                x, y = x + transform[0], y + transform[1]
            return {"x": round(x, 2), "y": round(y, 2), "w": round(w, 2), "h": round(h, 2)}
    return None


PATH_TOKEN = re.compile(r"[A-Za-z]|-?[0-9.]+(?:e-?[0-9]+)?")


def parse_path(d):
    """Absolute-path parser: M/L/H/V/Q only; returns (points, skipped_commands, quad_count)."""
    tokens = PATH_TOKEN.findall(d or "")
    points = []
    skipped = []
    quads = 0
    cursor = (0.0, 0.0)
    index = 0
    command = None
    while index < len(tokens):
        token = tokens[index]
        if token.isalpha():
            command = token
            index += 1
            if command not in "MLHVQmlhvq":
                skipped.append(command)
                return points, skipped, quads
            continue
        if command is None:
            return points, ["no-command"], quads
        if command == "M":
            x, y = float(tokens[index]), float(tokens[index + 1]); index += 2
            cursor = (x, y); points.append({"x": x, "y": y}); command = "L"
        elif command == "L":
            x, y = float(tokens[index]), float(tokens[index + 1]); index += 2
            cursor = (x, y); points.append({"x": x, "y": y})
        elif command == "H":
            x = float(tokens[index]); index += 1
            cursor = (x, cursor[1]); points.append({"x": cursor[0], "y": cursor[1]})
        elif command == "V":
            y = float(tokens[index]); index += 1
            cursor = (cursor[0], y); points.append({"x": cursor[0], "y": cursor[1]})
        elif command == "Q":
            cx, cy, x, y = (float(tokens[index + k]) for k in range(4)); index += 4
            x0, y0 = cursor
            for t in (0.5, 1.0):
                mx = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x
                my = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y
                points.append({"x": mx, "y": my})
            cursor = (x, y); quads += 1
        else:
            skipped.append(command)
            return points, skipped, quads
    return points, skipped, quads


def edge_geometry(edge_group):
    path = None
    color = edge_group.get("data-color")
    for descendant in edge_group.iter():
        if local_name(descendant.tag) != "path":
            continue
        tokens = class_tokens(descendant)
        if "edge-line" in tokens or path is None:
            path = descendant
            if "edge-line" in tokens:
                break
    if path is None:
        return None
    color = color or path.get("stroke")
    points, skipped, quads = parse_path(path.get("d"))
    return {"points": points, "skipped": skipped, "quad_count": quads,
            "color": canonical_color(color)}


def rect_overlap(a, b):
    return not (a["x"] + a["w"] <= b["x"] or b["x"] + b["w"] <= a["x"]
                or a["y"] + a["h"] <= b["y"] or b["y"] + b["h"] <= a["y"])


def segment_hits_rect(rect, p, q):
    if p["y"] == q["y"]:
        y = p["y"]
        lo, hi = min(p["x"], q["x"]), max(p["x"], q["x"])
        return rect["y"] < y < rect["y"] + rect["h"] and max(lo, rect["x"]) < min(hi, rect["x"] + rect["w"])
    if p["x"] == q["x"]:
        x = p["x"]
        lo, hi = min(p["y"], q["y"]), max(p["y"], q["y"])
        return rect["x"] < x < rect["x"] + rect["w"] and max(lo, rect["y"]) < min(hi, rect["y"] + rect["h"])
    return False


def border_distance(box, point):
    x, y = point["x"], point["y"]
    inside_x = box["x"] - 0.01 <= x <= box["x"] + box["w"] + 0.01
    inside_y = box["y"] - 0.01 <= y <= box["y"] + box["h"] + 0.01
    dx = min(abs(x - box["x"]), abs(x - (box["x"] + box["w"])))
    dy = min(abs(y - box["y"]), abs(y - (box["y"] + box["h"])))
    if inside_x and inside_y:
        return min(dx, dy)
    return math.hypot(max(box["x"] - x, 0, x - box["x"] - box["w"]),
                      max(box["y"] - y, 0, y - box["y"] - box["h"]))


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


def route_metrics(routes, node_boxes):
    rids = sorted(routes)
    crossings = []
    collinear = []
    total_collinear = 0.0
    skipped = []
    for i in range(len(rids)):
        ri = routes[rids[i]]
        if any(ri[k]["x"] != ri[k + 1]["x"] and ri[k]["y"] != ri[k + 1]["y"]
               for k in range(len(ri) - 1)):
            skipped.append(rids[i])
            continue
        for j in range(i + 1, len(rids)):
            rj = routes[rids[j]]
            if rids[j] in skipped:
                continue
            for ai in range(len(ri) - 1):
                for bj in range(len(rj) - 1):
                    pt = seg_intersection(ri[ai], ri[ai + 1], rj[bj], rj[bj + 1])
                    if pt:
                        crossings.append({"a": rids[i], "b": rids[j], **pt})
            for ai in range(len(ri) - 1):
                a, b = ri[ai], ri[ai + 1]
                for bj in range(len(rj) - 1):
                    c, d = rj[bj], rj[bj + 1]
                    if a["y"] == b["y"] == c["y"] == d["y"]:
                        lo = max(min(a["x"], b["x"]), min(c["x"], d["x"]))
                        hi = min(max(a["x"], b["x"]), max(c["x"], d["x"]))
                        if hi - lo > 2:
                            total_collinear += hi - lo
                            collinear.append({"a": rids[i], "b": rids[j], "axis": "h",
                                              "at": a["y"], "length": round(hi - lo, 1)})
                    elif a["x"] == b["x"] == c["x"] == d["x"]:
                        lo = max(min(a["y"], b["y"]), min(c["y"], d["y"]))
                        hi = min(max(a["y"], b["y"]), max(c["y"], d["y"]))
                        if hi - lo > 2:
                            total_collinear += hi - lo
                            collinear.append({"a": rids[i], "b": rids[j], "axis": "v",
                                              "at": a["x"], "length": round(hi - lo, 1)})
    through = []
    for rid, poly in routes.items():
        for k in range(len(poly) - 1):
            for nid, box in node_boxes.items():
                if segment_hits_rect(box, poly[k], poly[k + 1]):
                    through.append({"edge": rid, "node": nid})
                    break
    return {
        "method": "orthogonal segment intersection over native route polylines (axis-aligned only)",
        "crossings_count": len(crossings),
        "crossings": crossings,
        "collinear_total_px": round(total_collinear, 1),
        "collinear": collinear,
        "edges_skipped_non_orthogonal": skipped,
        "edge_through_node": through,
    }


def read_svg(svg_path, semantics, actual_records, native_report):
    payload = svg_path.read_text(encoding="utf-8", errors="replace")
    if re.search(r"<!DOCTYPE|<!ENTITY", payload, re.I):
        raise UsageError("SVG with DTD/ENTITY declarations is refused: %s" % svg_path)
    root = ET.fromstring(payload)
    nodes, zones, edges, modes, duplicates = collect_svg_ids(root)

    exp_el, exp_zn, exp_rel, _ = record_maps(semantics)
    act_el, act_zn, act_rel, _ = record_maps(actual_records)

    issues = []
    checks = {"identity": {}, "labels": {}, "legend": {}, "geometry": {}}

    def hard(code, detail):
        issues.append({"severity": "hard", "code": code, "detail": detail})

    def soft(code, detail):
        issues.append({"severity": "soft", "code": code, "detail": detail})

    identity = {
        "modes": {key: sorted(value) for key, value in modes.items()},
        "nodes": {"expected": len(act_el), "found": len(nodes),
                  "missing": sorted(set(act_el) - set(nodes)),
                  "extra": sorted(set(nodes) - set(act_el)), "duplicates": []},
        "zones": {"expected": len(act_zn), "found": len(zones),
                  "missing": sorted(set(act_zn) - set(zones)),
                  "extra": sorted(set(zones) - set(act_zn)), "duplicates": []},
        "edges": {"expected": len(act_rel), "found": len(edges),
                  "missing": sorted(set(act_rel) - set(edges)),
                  "extra": sorted(set(edges) - set(act_rel)), "duplicates": []},
    }
    for dup in duplicates:
        identity[dup["kind"] + "s"]["duplicates"].append(dup["id"])
    checks["identity"] = identity
    if identity["nodes"]["missing"] or identity["nodes"]["extra"]:
        hard("svg-node-identity", {"missing": identity["nodes"]["missing"],
                                   "extra": identity["nodes"]["extra"]})
    if identity["zones"]["missing"] or identity["zones"]["extra"]:
        hard("svg-zone-identity", {"missing": identity["zones"]["missing"],
                                   "extra": identity["zones"]["extra"]})
    if identity["edges"]["missing"] or identity["edges"]["extra"]:
        hard("svg-edge-identity", {"missing": identity["edges"]["missing"],
                                   "extra": identity["edges"]["extra"]})
    if any(identity[kind]["duplicates"] for kind in ("nodes", "zones", "edges")):
        hard("svg-duplicate-identity", {kind: identity[kind]["duplicates"]
                                        for kind in ("nodes", "zones", "edges")})

    # labels per id + duplicate-label preservation
    node_labels = {nid: find_text(group) for nid, group in nodes.items()}
    zone_labels = {zid: find_text(group) for zid, group in zones.items()}
    label_mismatches = []
    for nid, rec in act_el.items():
        if nid in node_labels and (node_labels[nid] or "") != (rec.get("label") or ""):
            label_mismatches.append({"kind": "node", "id": nid,
                                     "expected": rec.get("label"), "actual": node_labels[nid]})
    for zid, rec in act_zn.items():
        if zid in zone_labels and (zone_labels[zid] or "") != (rec.get("label") or ""):
            label_mismatches.append({"kind": "zone", "id": zid,
                                     "expected": rec.get("label"), "actual": zone_labels[zid]})

    edge_labels = {}
    extra_edge_labels = []
    for element in root.iter():
        if local_name(element.tag) != "text":
            continue
        if "edge-label" not in class_tokens(element):
            continue
        rid = element.get("data-edge-id")
        if rid is None:
            parent = element.get("id") or ""
            match = re.match(r"edge-(.+)-label$", parent)
            if match:
                rid = match.group(1)
        text = "".join(element.itertext()).strip()
        if rid is None:
            extra_edge_labels.append({"edge": None, "text": text})
        elif rid in edge_labels:
            extra_edge_labels.append({"edge": rid, "text": text, "duplicate": True})
        else:
            edge_labels[rid] = text

    label_checks = {"node_label_mismatches": label_mismatches,
                    "edge_labels": edge_labels,
                    "edge_label_missing": [], "edge_label_mismatch": [],
                    "extra_edge_labels": extra_edge_labels}
    for rid, rec in act_rel.items():
        expected_label = rec.get("label")
        actual_label = edge_labels.get(rid)
        if expected_label:
            if actual_label is None:
                label_checks["edge_label_missing"].append(rid)
            elif actual_label != expected_label:
                label_checks["edge_label_mismatch"].append(
                    {"id": rid, "expected": expected_label, "actual": actual_label})
        elif actual_label is not None:
            label_checks["extra_edge_labels"].append({"edge": rid, "text": actual_label})
    if label_mismatches or label_checks["edge_label_missing"] or label_checks["edge_label_mismatch"]:
        hard("svg-label-binding", {key: value for key, value in label_checks.items() if value})
    if extra_edge_labels or any(item["edge"] for item in extra_edge_labels):
        hard("svg-extra-edge-label", extra_edge_labels)

    # duplicate label multiset (per-id equality already asserted against native records)
    checks["labels"] = label_checks

    # color family of every edge
    color_mismatches = []
    for rid, group in edges.items():
        if rid not in act_rel:
            continue
        actual_color = canonical_color(group.get("data-color"))
        if actual_color in (None, ""):
            for descendant in group.iter():
                if local_name(descendant.tag) == "path":
                    actual_color = canonical_color(descendant.get("stroke"))
                    if actual_color not in (None, "", "none"):
                        break
        if canonical_color(act_rel[rid].get("color")) != actual_color:
            color_mismatches.append({"id": rid, "expected": act_rel[rid].get("color"),
                                     "actual": actual_color})
    if color_mismatches:
        hard("svg-edge-color", color_mismatches)

    # legend contract
    legend_container = None
    for element in root.iter():
        if element.get("id") == "legend-panel" or element.get("data-legend") not in (None, "", "0"):
            legend_container = element
            break
    legend = {"format": "none", "entries": [], "undeclared_texts": [], "issues": []}
    if legend_container is not None:
        declared = []
        declared_texts = set()
        for element in legend_container.iter():
            kind = element.get("data-legend-kind")
            if not kind:
                continue
            text = find_text(element)
            swatch = element.get("data-swatch-color")
            if swatch is None:
                for descendant in element.iter():
                    if local_name(descendant.tag) in ("line", "circle", "rect"):
                        swatch = descendant.get("stroke") or descendant.get("fill")
                        if descendant.get("stroke") not in (None, "none"):
                            break
            declared.append({"kind": kind, "text": text, "swatch": canonical_color(swatch)})
            if text:
                declared_texts.add(text)
        legend["entries"] = declared
        all_texts = []
        for element in legend_container.iter():
            if local_name(element.tag) != "text":
                continue
            if "legend-title" in class_tokens(element):
                continue
            text = "".join(element.itertext()).strip()
            if text and text not in declared_texts:
                all_texts.append(text)
        legend["undeclared_texts"] = all_texts
        if declared:
            legend["format"] = "declared"
            semantic_colors = {canonical_color(rec.get("color")) for rec in act_rel.values()}
            for entry in declared:
                if entry["kind"] not in ("style", "interaction"):
                    legend["issues"].append({"code": "extra-legend-semantics",
                                             "detail": entry})
                    hard("extra-legend-semantics", entry)
                if entry["swatch"] in semantic_colors and entry["kind"] == "style":
                    # style swatches may reuse structural ink; they must not claim business meaning
                    # (the text is reported verbatim so the claim is auditable)
                    legend["entries"][legend["entries"].index(entry)]["swatch_matches_relation_color"] = True
            if all_texts:
                legend["issues"].append({"code": "undeclared-legend-text", "detail": all_texts})
                hard("undeclared-legend-text", all_texts)
        else:
            legend["format"] = "undeclared"
            if all_texts:
                legend["issues"].append({"code": "legacy-legend-unverifiable",
                                         "detail": all_texts})
                soft("legacy-legend-unverifiable",
                     "legend text exists but declares no data-legend-kind; verifiability is limited")
    checks["legend"] = legend

    # geometry: boxes vs native SDS boxes
    act_sds_boxes = {}
    for item in actual_records.get("elements") or []:
        box = item.get("box")
        if isinstance(box, dict) and all(k in box for k in ("x", "y", "w", "h")):
            act_sds_boxes[item["id"]] = box
    box_deltas = []
    max_delta = 0.0
    for nid, box in act_sds_boxes.items():
        if nid not in nodes:
            continue
        svg_box_value = svg_box(nodes[nid])
        if svg_box_value is None:
            continue
        delta = max(abs(svg_box_value[k] - box[k]) for k in ("x", "y", "w", "h"))
        max_delta = max(max_delta, delta)
        if delta > 1.0:
            box_deltas.append({"id": nid, "delta": round(delta, 2),
                               "sds": box, "svg": svg_box_value})
    if box_deltas:
        hard("svg-box-delta", box_deltas)

    # geometry: route
    routes = {}
    for item in actual_records.get("relations") or []:
        route = item.get("route")
        if isinstance(route, list) and len(route) >= 2:
            routes[item["id"]] = route
    node_boxes = {}
    for nid, group in nodes.items():
        box = svg_box(group)
        if box:
            node_boxes[nid] = box
    route_check = {"native_routes_present": bool(routes)}
    if routes:
        route_check.update(route_metrics(routes, node_boxes))
        if route_check["edge_through_node"]:
            soft("edge-through-node", route_check["edge_through_node"])
        if route_check["edges_skipped_non_orthogonal"]:
            route_check["limitation"] = ("non-orthogonal route segments were skipped in the "
                                         "crossing/collinear metric")
    # SVG path endpoints vs source/target boxes
    endpoint_issues = []
    edge_paths = {}
    for rid, group in edges.items():
        if rid not in act_rel:
            continue
        geo = edge_geometry(group)
        if not geo or len(geo["points"]) < 2:
            endpoint_issues.append({"id": rid, "issue": "path-unparseable",
                                    "skipped_commands": geo["skipped"] if geo else None})
            continue
        edge_paths[rid] = geo
        start, end = geo["points"][0], geo["points"][-1]
        for side, point in (("from", start), ("to", end)):
            target = act_rel[rid][side]
            group_box = node_boxes.get(target) or svg_box(zones.get(target))
            if group_box is None:
                continue
            distance = border_distance(group_box, point)
            if distance > 3.0:
                endpoint_issues.append({"id": rid, "side": side, "target": target,
                                        "distance": round(distance, 2)})
    route_check["endpoint_issues"] = endpoint_issues
    route_check["path_parser"] = "M/L/H/V/Q absolute; arcs/relative commands are reported as skipped"
    if endpoint_issues:
        hard("svg-endpoint-attachment", endpoint_issues)
    checks["geometry"] = route_check

    # label collision estimation (shared estimator with build-native.py; documented approximation)
    label_boxes = []
    for rid, group in edges.items():
        for element in group.iter():
            if local_name(element.tag) != "text" or "edge-label" not in class_tokens(element):
                continue
            text = "".join(element.itertext()).strip()
            x = parse_number(element.get("x"))
            y = parse_number(element.get("y"))
            width = est_text_width(text, 15.0) + 12
            label_boxes.append({"edge": rid, "text": text,
                                "rect": {"x": x - width / 2, "y": y - 14, "w": width, "h": 20}})
    collisions = {"label_vs_node": [], "label_vs_label": [], "label_vs_other_edge": []}
    for label in label_boxes:
        for nid, box in node_boxes.items():
            if rect_overlap(label["rect"], box):
                collisions["label_vs_node"].append({"edge": label["edge"], "node": nid})
        for other in edge_paths.values():
            points = other["points"]
            for k in range(len(points) - 1):
                if segment_hits_rect(label["rect"], points[k], points[k + 1]):
                    other_edge = next((rid for rid, geo in edge_paths.items()
                                       if geo is other), None)
                    if other_edge and other_edge != label["edge"]:
                        collisions["label_vs_other_edge"].append(
                            {"edge": label["edge"], "over": other_edge})
                    break
    for i in range(len(label_boxes)):
        for j in range(i + 1, len(label_boxes)):
            if rect_overlap(label_boxes[i]["rect"], label_boxes[j]["rect"]):
                collisions["label_vs_label"].append({"a": label_boxes[i]["edge"],
                                                     "b": label_boxes[j]["edge"]})
    checks["geometry"]["label_collisions"] = collisions
    checks["geometry"]["label_boxes"] = label_boxes
    checks["geometry"]["label_collision_method"] = (
        "estimated text width (15px edge-label font; CJK 1.0em, ASCII 0.6em) + 12px padding, "
        "height 20px; an approximation, not a browser bbox measurement")
    if collisions["label_vs_node"] or collisions["label_vs_label"] or collisions["label_vs_other_edge"]:
        soft("label-collision", collisions)

    visual_status = "fail" if any(i["severity"] == "hard" for i in issues) else (
        "partial" if issues else "pass")
    limitations = [
        "Label bounding boxes are estimated from font metrics; exact bboxes are browser measurements "
        "recorded separately by the run's measurements.json.",
        "Crossings/collinear are computed on the native route polylines (axis-aligned); SVG rounded "
        "corners are not part of that metric, and counts are per-method, not cross-engine rankings.",
        "The SVG path parser supports absolute M/L/H/V/Q; other commands are reported as skipped.",
    ]
    if legend["format"] == "undeclared":
        limitations.append("Legend semantics cannot be verified: the SVG carries no data-legend-kind rows.")
    return {"status": visual_status, "issues": issues, "checks": checks, "limitations": limitations}


def build_report(source_path, semantics_path, svg_path):
    semantics = load_json(semantics_path)
    if not all(isinstance(semantics.get(key), list) for key in REQUIRED_RECORD_KEYS):
        raise UsageError("semantics JSON must contain elements/zones/relations arrays")
    chosen, extraction = extract_native(source_path)
    report = {
        "engine": ENGINE,
        "tool": {"name": TOOL, "version": VERSION},
        "source": {"path": str(source_path), "sha256": sha256_file(source_path),
                   "format": source_path.suffix.lower().lstrip(".")},
        "semantics": {"path": str(semantics_path), "sha256": sha256_file(semantics_path)},
        "svg": ({"path": str(svg_path), "sha256": sha256_file(svg_path), "provided": True}
                if svg_path else {"path": None, "sha256": None, "provided": False}),
        "extraction": extraction,
    }
    if chosen is None:
        report["records"] = None
        report["actual"] = None
        report["semantic"] = {"status": "unsupported" if extraction["status"] != "missing" else "fail",
                              "diff": None}
        report["visual"] = {"status": "not_evaluated", "checks": {}, "issues": [],
                            "limitations": ["no native data records were extracted"]}
        report["overall"] = "unsupported" if extraction["status"] in ("ambiguous", "unsupported") else "fail"
        report["unsupported"] = [extraction.get("detail", extraction["status"])]
        report["not_evaluated"] = ["semantic", "visual"]
        report["interaction"] = {"status": "not_evaluated",
                                 "detail": "readback does not drive the browser"}
        report["reproducibility"] = {"status": "not_evaluated"}
        report["exit_code"] = 3 if report["overall"] == "unsupported" else 1
        return report

    actual = chosen["data"]
    diff, duplicate_labels, semantic_status = compare_records(semantics, actual)
    report["records"] = {
        "elements": [dict(id=item.get("id"), label=item.get("label"), zone=item.get("zone"))
                     for item in actual.get("elements") or [] if isinstance(item, dict)],
        "zones": [dict(id=item.get("id"), label=item.get("label"), parent=item.get("parent"))
                  for item in actual.get("zones") or [] if isinstance(item, dict)],
        "relations": [dict(id=item.get("id"), **{"from": item.get("from")}, to=item.get("to"),
                           label=item.get("label"), color=item.get("color"))
                      for item in actual.get("relations") or [] if isinstance(item, dict)],
    }
    report["semantic"] = {"status": semantic_status, "diff": diff,
                          "duplicate_labels": duplicate_labels,
                          "method": "actual native records vs authoritative semantics; "
                                    "records are never copied from --semantics"}
    if svg_path:
        visual = read_svg(svg_path, semantics, actual, report)
    else:
        visual = {"status": "not_evaluated",
                  "issues": [],
                  "checks": {},
                  "limitations": ["no --svg supplied; visual identity/geometry not evaluated"]}
    report["visual"] = visual
    report["interaction"] = {"status": "not_evaluated",
                             "detail": "readback does not drive the browser; interaction evidence "
                                       "belongs to the run's browser measurements"}
    report["reproducibility"] = {"status": "not_evaluated",
                                 "detail": "manifest/export evidence is assembled by the caller"}

    hard_fail = semantic_status == "fail" or visual["status"] == "fail"
    partial = (semantic_status != "pass" or visual["status"] in ("partial", "not_evaluated"))
    if hard_fail:
        overall = "fail"
    elif partial:
        overall = "partial"
    else:
        overall = "pass"
    report["overall"] = overall
    report["unsupported"] = []
    report["not_evaluated"] = ([] if svg_path else ["visual"]) + ["interaction", "reproducibility"]
    report["exit_code"] = 0 if overall == "pass" else (1 if overall == "fail" else 3)
    # Canonical quality-gate field: the records actually extracted from the native file.
    report["actual"] = report["records"]
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="d3js native-source readback: extract the actual data script, diff against "
                    "semantics, and verify the rendered SVG identity/labels/geometry.",
        allow_abbrev=False,
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    parser.add_argument("--source", type=Path, required=True,
                        help="native d3js artifact (.html with a data script, .json, or .js data file)")
    parser.add_argument("--semantics", type=Path, required=True,
                        help="authoritative semantics JSON (elements/zones/relations)")
    parser.add_argument("--svg", type=Path, default=None,
                        help="rendered SVG export (optional; enables visual identity/geometry checks)")
    parser.add_argument("--output", type=Path, required=True,
                        help="new report JSON path (must not exist)")
    args = parser.parse_args(argv)

    try:
        if not args.source.is_file():
            raise UsageError("source not found: %s" % args.source)
        if not args.semantics.is_file():
            raise UsageError("semantics not found: %s" % args.semantics)
        if args.svg is not None and not args.svg.is_file():
            raise UsageError("svg not found: %s" % args.svg)
        if args.output.exists():
            raise UsageError("refusing to overwrite existing output: %s" % args.output)
        report = build_report(args.source, args.semantics, args.svg)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    except UsageError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    except (OSError, UnicodeError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    summary = {
        "overall": report.get("overall"),
        "semantic": (report.get("semantic") or {}).get("status"),
        "visual": (report.get("visual") or {}).get("status"),
        "exit_code": report.get("exit_code"),
        "report": str(args.output),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return report.get("exit_code", 1)


if __name__ == "__main__":
    raise SystemExit(main())
