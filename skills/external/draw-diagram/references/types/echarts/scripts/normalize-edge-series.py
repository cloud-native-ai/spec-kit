#!/usr/bin/env python3
"""Normalize the edge decorations of an ECharts fixed-layout graph option.

Repairs, all deterministic and reported per item:
  1. arrow-rotation     - recompute symbolRotate so the rendered apex points along
                          the relation's final approach (measured ECharts 5.6.0
                          convention, see references/sds-realization.md section 4)
  2. final-segment      - when the arrow inset overshoots a short final approach and
                          the stored line end falls behind the previous vertex, move
                          the line end back onto the approach
  3. label-anchor       - snap an edge label anchor onto its own polyline when it is
                          farther than 3 px from it or another relation's line is
                          closer than its own

Usage:
  normalize-edge-series.py --check --source <option.json|served.html>
  normalize-edge-series.py --write --source <option.json|served.html> --output <new.json>

Exit codes:
  0  check clean, or the normalized copy was written
  1  check found drift (the printed plan lists every repair)
  2  usage or I/O error (including refusing to overwrite an existing output)
  3  cannot evaluate (missing arrow/line series, symbol family, or arrow/line match)
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import edge_series as es

VERSION = "1.0.0"
INSET_MAX = 10.0


def plan_normalization(option):
    found = es.find_series(option)
    if found["arrows"] is None or found["lines"] is None:
        return {
            "status": "not_applicable",
            "reason": "no custom arrow scatter + polyline lines series pair found",
            "mutations": [],
        }
    actual = es.extract(option)
    relations = {r["semanticId"]: r for r in actual["relations"]}
    mutations = []
    unsupported = []
    for sid, arrow in sorted(actual["arrows"].items(), key=lambda kv: str(kv[0])):
        rel = relations.get(sid)
        if rel is None:
            unsupported.append(f"arrow {sid} has no matching polyline")
            continue
        if not arrow["supportedSymbol"]:
            unsupported.append(f"arrow {sid} uses an unsupported symbol family: {arrow['symbol']!r}")
            continue
        center, line_end = arrow["center"], (rel["coords"][-1] if rel["coords"] else None)
        if center is None or line_end is None or arrow["h"] is None:
            unsupported.append(f"arrow {sid} lacks center/symbol height or polyline coordinates")
            continue
        approach, approach_source = es.final_approach(rel, arrow)
        if approach is None:
            unsupported.append(f"arrow {sid} has no resolvable approach direction")
            continue
        target_rotate = es.correct_symbol_rotate(approach)
        if target_rotate is None:
            unsupported.append(f"arrow {sid} approach normalizes to zero")
            continue
        if arrow["symbolRotate"] is None or abs(es.normalize_degrees(arrow["symbolRotate"] - target_rotate)) > 0.01:
            mutations.append({
                "kind": "arrow-rotation",
                "semanticId": sid,
                "from": arrow["symbolRotate"],
                "to": target_rotate,
                "approach": [round(approach[0], 4), round(approach[1], 4)],
                "approachSource": approach_source,
            })
        half = arrow["h"] / 2.0
        apex = [center[0] + approach[0] * half, center[1] + approach[1] * half]
        if len(rel["coords"]) >= 2:
            last, prev = rel["coords"][-1], rel["coords"][-2]
            segment = [last[0] - prev[0], last[1] - prev[1]]
            segment_len = math.hypot(segment[0], segment[1])
            ahead = [apex[0] - prev[0], apex[1] - prev[1]]
            if segment_len > 1e-9 and (segment[0] * ahead[0] + segment[1] * ahead[1]) < 0:
                if segment_len >= es.DEGENERATE_SEGMENT_TOL:
                    unsupported.append(
                        f"arrow {sid} final segment runs against the arrow direction (route error, not repaired)"
                    )
                    continue
                direction = es.unit(ahead)
                distance = math.hypot(ahead[0], ahead[1])
                if direction is None or distance <= half + 0.6:
                    unsupported.append(
                        f"arrow {sid} has a reversed final segment too short to repair without moving the arrow"
                    )
                    continue
                inset_new = min(INSET_MAX, max(half + 0.5, distance - 0.5))
                new_point = [
                    round(apex[0] - direction[0] * inset_new, 2),
                    round(apex[1] - direction[1] * inset_new, 2),
                ]
                mutations.append({
                    "kind": "final-segment",
                    "semanticId": sid,
                    "from": list(rel["coords"][-1]),
                    "to": new_point,
                    "reason": "arrow inset overshoot reversed the stored final segment",
                })
                rel["coords"] = rel["coords"][:-1] + [new_point]
    for label in actual["labels"]:
        sid = label["semanticId"]
        rel = relations.get(sid)
        if rel is None or len(rel["coords"]) < 2 or label["point"] is None:
            unsupported.append(f"label {sid} has no matching polyline or anchor point")
            continue
        point = label["point"]
        nearest, own = es.nearest_point_on_polyline(point, rel["coords"])
        other = None
        for other_id, other_rel in relations.items():
            if other_id == sid or len(other_rel["coords"]) < 2:
                continue
            distance = es.point_polyline_distance(point, other_rel["coords"])
            other = distance if other is None else min(other, distance)
        misattributed = other is not None and other + es.LABEL_MISATTRIBUTION_MARGIN < own
        if own > es.LABEL_BIND_TOL or misattributed:
            mutations.append({
                "kind": "label-anchor",
                "semanticId": sid,
                "from": [round(point[0], 2), round(point[1], 2)],
                "to": [round(nearest[0], 2), round(nearest[1], 2)],
                "ownDistanceBefore": round(own, 3),
                "otherMinBefore": None if other is None else round(other, 3),
            })
            label["point"] = [round(nearest[0], 2), round(nearest[1], 2)]
    status = "unsupported" if unsupported and not mutations else "planned"
    return {"status": status, "mutations": mutations, "unsupported": unsupported}


def apply_mutations(option, mutations):
    for mutation in mutations:
        sid = mutation["semanticId"]
        kind = mutation["kind"]
        if kind == "arrow-rotation":
            series = _arrow_series(option)
            for item in series["data"]:
                if isinstance(item, dict) and item.get("semanticId") == sid:
                    item["symbolRotate"] = mutation["to"]
        elif kind == "final-segment":
            series = _line_series(option)
            for item in series["data"]:
                if isinstance(item, dict) and item.get("semanticId") == sid:
                    item["coords"] = list(item["coords"][:-1]) + [mutation["to"]]
        elif kind == "label-anchor":
            series = _label_series(option)
            if series is None:
                continue
            for item in series["data"]:
                if isinstance(item, dict) and item.get("semanticId") == sid:
                    value = item.get("value") or []
                    item["value"] = [mutation["to"][0], mutation["to"][1]] + list(value[2:])


def _arrow_series(option):
    return es.find_series(option)["arrows"]


def _line_series(option):
    return es.find_series(option)["lines"]


def _label_series(option):
    return es.find_series(option)["labels"]


def build_parser():
    parser = argparse.ArgumentParser(
        prog="normalize-edge-series.py",
        description="Deterministically normalize arrow rotations, degenerate final segments and edge-label anchors of an ECharts fixed-layout option.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report drift without writing")
    mode.add_argument("--write", action="store_true", help="write a normalized copy to --output")
    parser.add_argument("--source", required=True, help="ECharts option JSON or served HTML with an embedded OPTION")
    parser.add_argument("--output", help="new file for --write (must not exist)")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.write and not args.output:
        parser.error("--write requires --output")
    if args.check and args.output:
        parser.error("--output is only valid with --write")
    try:
        option, fmt, digest = es.load_option(args.source)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: cannot read source: {exc}", file=sys.stderr)
        return 2
    try:
        plan = plan_normalization(option)
    except ValueError as exc:
        print(f"error: cannot evaluate option: {exc}", file=sys.stderr)
        return 3
    summary = {
        "script": "normalize-edge-series.py",
        "version": VERSION,
        "source": {"path": str(args.source), "format": fmt, "sha256": digest},
        "mode": "check" if args.check else "write",
        "status": plan["status"],
        "mutations": plan["mutations"],
        "unsupported": plan.get("unsupported", []),
    }
    if args.check:
        summary["drift"] = bool(plan["mutations"])
        print(json.dumps(summary, ensure_ascii=False, indent=1))
        if plan["status"] == "unsupported" and not plan["mutations"]:
            return 3
        return 1 if plan["mutations"] else 0
    if plan["status"] == "unsupported" and not plan["mutations"]:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
        return 3
    apply_mutations(option, plan["mutations"])
    output = Path(args.output)
    try:
        if output.resolve() == Path(args.source).resolve():
            raise FileExistsError("refusing to overwrite the source file")
        with open(output, "x", encoding="utf-8") as handle:
            handle.write(json.dumps(option, ensure_ascii=False, indent=1) + "\n")
    except FileExistsError as exc:
        print(f"error: refusing to write: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"error: cannot write output: {exc}", file=sys.stderr)
        return 2
    summary["output"] = {"path": str(output), "sha256": es.sha256_file(output)}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
