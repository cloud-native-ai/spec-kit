#!/usr/bin/env python3
"""generate-scene.py — build a native .excalidraw scene from caller semantics.

Usage:
  generate-scene.py --semantics <semantics.json> --output <scene.excalidraw>
                    [--report <layout-report.json>] [--title <override>]

The semantics document is the draw-diagram semantic input (elements/zones/
relations). Layout and routing are planned by this engine (layout_policy
optimize); no geometry is inherited from the input. The produced scene carries
genuine native bindings and is self-checked before it is written: an arrow
through a component, a relation label over a component, or a broken reciprocal
binding fails the run instead of shipping a defective scene.

Exit codes:
  0  scene written; --report written when requested
  1  a hard geometry/binding defect survived generation; the scene is NOT
     written, the --report file (when requested) carries the diagnostics
  2  usage error, unreadable/invalid input, or an existing output/report path
     (this command never overwrites)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import scene_builder  # noqa: E402

VERSION = "1.1.0"


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="generate-scene.py",
        description="Build a native Excalidraw scene from draw-diagram semantics (deterministic layout + routing + genuine bindings).",
        epilog="exit codes: 0 scene written; 1 hard defect (scene not written); 2 usage/input/existing-output error",
    )
    parser.add_argument("--semantics", required=True, help="semantic input JSON (elements/zones/relations)")
    parser.add_argument("--output", required=True, help="new .excalidraw file to create (must not exist)")
    parser.add_argument("--report", help="new JSON report path (must not exist when given)")
    parser.add_argument("--title", help="diagram title override (default: semantics title)")
    parser.add_argument("--version", action="version", version=f"generate-scene.py {VERSION}")
    args = parser.parse_args(argv)

    semantics_path = Path(args.semantics)
    output_path = Path(args.output)
    report_path = Path(args.report) if args.report else None

    if output_path.exists():
        print(f"error: refusing to overwrite existing output: {output_path}", file=sys.stderr)
        return 2
    if report_path is not None and report_path.exists():
        print(f"error: refusing to overwrite existing report: {report_path}", file=sys.stderr)
        return 2
    try:
        data = json.loads(semantics_path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"error: cannot read semantics: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: semantics is not valid JSON: {exc}", file=sys.stderr)
        return 2
    if args.title:
        data["title"] = args.title

    try:
        scene, report = scene_builder.generate_scene(data)
    except scene_builder.SemanticsError as exc:
        print(f"error: invalid semantics: {exc}", file=sys.stderr)
        return 2
    except scene_builder.BuildError as exc:
        print("error: hard generation defect; scene not written", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        if report_path is not None:
            failure = {
                "engine": scene_builder.ENGINE,
                "builder_version": scene_builder.VERSION,
                "status": "hard-defect",
                "detail": json.loads(str(exc)) if _is_json(str(exc)) else str(exc),
            }
            report_path.write_text(json.dumps(failure, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return 1

    output_path.write_text(json.dumps(scene, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    summary = {
        "output": str(output_path),
        "report": str(report_path) if report_path else None,
        "counts": report["counts"],
        "canvas": report["canvas"],
        "crossings": report["crossings"]["pair_count"],
        "edge_through_component": len(report["edge_through_component"]),
        "label_problems": len(report["label_problems"]),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


def _is_json(text):
    try:
        json.loads(text)
        return True
    except (ValueError, TypeError):
        return False


if __name__ == "__main__":
    sys.exit(main())
