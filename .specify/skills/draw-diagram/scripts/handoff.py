#!/usr/bin/env python3
"""handoff.py — cold-start handoff: frozen semantics -> per-engine SDS + dispatch index.

This is the executable form of the comparison-mode rule "semantics are frozen,
geometry is not shared" (references/routing-matrix.md §5, references/semantic-model.md
§ 几何归属). Given a semantics JSON (elements / relations / zones / weight_plan /
confirmed decisions — the shape of a shared-semantics file), it:

  * validates graph integrity (unique ids, relation endpoints exist, declared
    counts match) and refuses to hand over a broken model;
  * STRIPS any geometry it finds (element/zone box, relation via/anchor/ports/
    label_position) and records what it dropped in the handoff index, so a new
    drawing run starts from semantics only and each engine plans its own
    geometry under layout_policy=optimize;
  * writes one `sds-<engine>.json` per engine plus a `handoff.json` index that
    names the engine entry doc, the required artifacts (native source + real
    export + checked manifest) and the manifest checker.

Outputs are deterministic (sorted keys) and refuse to overwrite existing files.
Engine drawing logic and style stay in each engine layer; this script never
writes diagram syntax or coordinates.

Usage:
  handoff.py --semantics <shared-semantics.json> --out <existing-dir>
             [--engines d3js,drawio,...] [--policy optimize|preserve]

Exit codes: 0 written; 1 semantics validation failed; 2 usage or I/O error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

VERSION = "1.0.0"

ENGINES = ("d3js", "drawio", "echarts", "excalidraw", "mermaid", "plantuml")
MAX_BYTES = 10_000_000
GEOMETRY_KEYS = {
    "element": ("box", "x", "y", "w", "h", "width", "height", "pos", "position"),
    "zone": ("box", "x", "y", "w", "h", "width", "height", "pos", "position"),
    "relation": ("via", "points", "waypoints", "anchor", "source_side", "target_side", "label_position"),
}
CARRY_KEYS = (
    "title",
    "diagram_class",
    "fidelity_intent",
    "layout_authorization",
    "layout_intent",
    "auto_layout_intent",
    "style_intent",
    "weight_plan",
    "interactivity_intent",
    "editability_intent",
    "artifact_intent",
    "confirmed_decisions",
    "constraints",
)


class HandoffError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise HandoffError(message)


def text(value):
    return isinstance(value, str) and value.strip() != ""


def digest(data):
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def load_semantics(path):
    require(path.is_file(), f"semantics file not found: {path}")
    require(path.stat().st_size <= MAX_BYTES, "semantics file exceeds 10 MB")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HandoffError(f"semantics is not valid JSON: {exc}") from exc
    require(isinstance(data, dict), "semantics must be a JSON object")
    return data


def strip_geometry(item, kind, dropped, label):
    stripped = dict(item)
    for key in GEOMETRY_KEYS[kind]:
        if key in stripped:
            dropped.append(f"{kind}:{label}.{key}")
            del stripped[key]
    return stripped


def validate(data):
    elements = data.get("elements")
    relations = data.get("relations")
    zones = data.get("zones", [])
    require(isinstance(elements, list) and elements, "semantics.elements must be a non-empty list")
    require(isinstance(relations, list) and relations, "semantics.relations must be a non-empty list")
    require(isinstance(zones, list), "semantics.zones must be a list when present")
    element_ids, element_zones = set(), {}
    for index, element in enumerate(elements):
        require(isinstance(element, dict), f"elements[{index}] must be an object")
        ident = element.get("id")
        require(text(ident), f"elements[{index}].id must be a non-empty string")
        require(ident not in element_ids, f"duplicate element id: {ident}")
        element_ids.add(ident)
        require(text(element.get("label")), f"element {ident}: label must be a non-empty string")
        if text(element.get("zone")):
            element_zones[ident] = element["zone"]
    zone_ids = set()
    declared_members = {}
    for index, zone in enumerate(zones):
        require(isinstance(zone, dict), f"zones[{index}] must be an object")
        ident = zone.get("id")
        require(text(ident), f"zones[{index}].id must be a non-empty string")
        require(ident not in zone_ids, f"duplicate zone id: {ident}")
        zone_ids.add(ident)
        require(text(zone.get("label")), f"zone {ident}: label must be a non-empty string")
        members = zone.get("members")
        if members is not None:
            require(isinstance(members, list) and all(text(m) for m in members), f"zone {ident}: members must be id strings")
            declared_members[ident] = list(members)
    known = element_ids | zone_ids
    if zone_ids:
        for ident, zone in element_zones.items():
            require(zone in zone_ids, f"element {ident}: unknown zone {zone!r}")
        for zone, members in declared_members.items():
            for member in members:
                require(member in element_ids, f"zone {zone}: member {member!r} is not an element")
    relation_ids = set()
    for index, relation in enumerate(relations):
        require(isinstance(relation, dict), f"relations[{index}] must be an object")
        ident = relation.get("id")
        require(text(ident), f"relations[{index}].id must be a non-empty string")
        require(ident not in relation_ids, f"duplicate relation id: {ident}")
        relation_ids.add(ident)
        for side in ("from", "to"):
            endpoint = relation.get(side)
            require(text(endpoint), f"relation {ident}: {side} must be a non-empty id")
            require(endpoint in known, f"relation {ident}: {side} {endpoint!r} is not a known element/zone")
    counts = data.get("counts")
    if counts is not None:
        require(isinstance(counts, dict), "counts must be an object when present")
        actual = {"elements": len(elements), "zones": len(zones), "relations": len(relations)}
        for key, value in actual.items():
            if key in counts:
                require(counts[key] == value, f"counts.{key}={counts[key]} does not match the file ({value})")
    return element_ids, zone_ids


def build_sds(data, engine, policy, dropped):
    sds = {
        "engine": engine,
        "layout_policy": policy,
        "dispatch": {
            "generate_geometry": "engine"
            if policy == "optimize"
            else "caller (this handoff carries no geometry; supply a measured SDS before drawing)",
            "required_artifacts": ["native-source", "real-export(svg|png)", "manifest(checked by scripts/check-manifest.py)"],
            "engine_entry": f"references/types/{engine}/{engine}.md",
            "quality_gate": "references/quality-gate.md",
            "manifest_checker": "scripts/check-manifest.py",
        },
    }
    for key in CARRY_KEYS:
        if key in data:
            sds[key] = data[key]
    sds["elements"] = [strip_geometry(e, "element", dropped, e["id"]) for e in data["elements"]]
    sds["relations"] = [strip_geometry(r, "relation", dropped, r["id"]) for r in data["relations"]]
    if data.get("zones"):
        sds["zones"] = [strip_geometry(z, "zone", dropped, z["id"]) for z in data["zones"]]
    else:
        sds["zones"] = []
    return sds


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Cold-start handoff: validate shared semantics, strip geometry, and emit "
        "per-engine SDS skeletons + a dispatch index. Exit 0 written, 1 invalid semantics, "
        "2 usage/I-O error.",
        allow_abbrev=False,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--semantics", type=Path, required=True, help="semantics JSON path")
    parser.add_argument("--out", type=Path, required=True, help="existing output directory")
    parser.add_argument("--engines", default=",".join(ENGINES), help="comma-separated engine list (default: all six)")
    parser.add_argument("--policy", choices=("optimize", "preserve"), default=None, help="override layout_policy (default: semantics value or optimize)")
    args = parser.parse_args(argv)
    engines = [item.strip() for item in args.engines.split(",") if item.strip()]
    unknown = [engine for engine in engines if engine not in ENGINES]
    if not engines or unknown:
        print(f"unknown engine(s): {unknown or '(none given)'}; valid: {', '.join(ENGINES)}", file=sys.stderr)
        return 2
    if not args.out.is_dir():
        print(f"output directory does not exist: {args.out}", file=sys.stderr)
        return 2
    try:
        data = load_semantics(args.semantics)
        validate(data)
        policy = args.policy or data.get("layout_policy") or "optimize"
        if policy not in ("optimize", "preserve"):
            raise HandoffError(f"layout_policy {policy!r} not in ('optimize', 'preserve')")
        dropped = []
        outputs = {}
        for engine in engines:
            sds = build_sds(data, engine, policy, dropped)
            outputs[engine] = sds
        index = {
            "generated_by": f"handoff.py {VERSION}",
            "semantics": {"path": str(args.semantics), "sha256": digest(data)},
            "layout_policy": policy,
            "counts": {
                "elements": len(data["elements"]),
                "zones": len(data.get("zones") or []),
                "relations": len(data["relations"]),
            },
            "dropped_geometry": sorted(set(dropped)),
            "engines": {
                engine: {
                    "sds": f"sds-{engine}.json",
                    "engine_entry": f"references/types/{engine}/{engine}.md",
                    "required_artifacts": ["native-source", "real-export(svg|png)", "manifest(checked by scripts/check-manifest.py)"],
                }
                for engine in engines
            },
            "rule": "geometry is not shared across engines; each engine plans its own under layout_policy",
        }
        paths = {args.out / f"sds-{engine}.json": outputs[engine] for engine in engines}
        paths[args.out / "handoff.json"] = index
        for path in paths:
            if path.exists() or path.is_symlink():
                raise HandoffError(f"refusing to overwrite existing file: {path}")
        for path, payload in paths.items():
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"status": "written", "out": str(args.out), "files": [p.name for p in paths], "dropped_geometry": index["dropped_geometry"]}, ensure_ascii=False))
        return 0
    except HandoffError as exc:
        print(f"handoff error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"I/O error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
