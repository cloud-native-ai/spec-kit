#!/usr/bin/env python3
"""check-manifest.py — deterministic check of a draw-diagram result manifest.

The manifest is the machine-checkable face of references/quality-gate.md: one
JSON file shipped next to the delivered artifacts. This checker refuses claims
that are not backed by the actual delivered files, and refuses the two ways a
manifest can lie without anyone noticing:

  * input echo — the "diagram source" is byte-identical to the semantic input
    (ldm_sha256 == source.sha256), so no drawing step actually happened;
  * readback theatre — axes.semantic=pass while readback.method is empty or
    names an input copy, or while directions/parents were never checked.

It also independently re-counts drawio native sources (mxCell vertices/edges)
and compares them with the manifest's readback counts, so a drawio semantic
pass rests on a real native-source readback, not on the author's word. Other
engine formats are not parsed here — the verdict states that honestly and the
engine entry owns its readback (quality-gate.md lists the per-engine scripts).

Usage:
  check-manifest.py --manifest <dir>/manifest.json [--json]

Paths inside the manifest are RELATIVE to the manifest's directory. Absolute
paths, drive letters and '..' escapes are refused: a delivered manifest stays
portable and never pins one machine's layout.

Exit codes: 0 all checks pass; 1 one or more violations; 2 usage or I/O error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

VERSION = "1.0.0"

ENGINES = ("d3js", "drawio", "echarts", "excalidraw", "mermaid", "plantuml")
SOURCE_FORMATS = ("mmd", "puml", "drawio", "xml", "excalidraw", "json", "html")
EXPORT_FORMATS = ("svg", "png", "pdf", "html")
READBACK_STATES = ("verified", "partial", "not_checked")
AXES = {
    "semantic": ("pass", "partial", "fail", "not_checked"),
    "visual": ("pass", "partial", "fail", "not_performed"),
    "interaction": ("pass", "partial", "fail", "not_applicable"),
    "engineering": ("pass", "partial", "fail"),
}
MAX_BYTES = 1_000_000
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAGIC = {
    "png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
    "pdf": lambda data: data.startswith(b"%PDF"),
    "svg": lambda data: b"<svg" in data[:4096],
    "html": lambda data: b"<html" in data[:4096].lower() or b"<!doctype" in data[:4096].lower(),
}
ECHO_METHODS = {"", "none", "input", "input-copy", "ldm", "ldm-copy", "copy"}


class ManifestError(ValueError):
    pass


def fail(violations, code, detail):
    violations.append({"code": code, "detail": detail})


def require(condition, message):
    if not condition:
        raise ManifestError(message)


def text(value):
    return isinstance(value, str) and value.strip() != ""


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_path(manifest_dir, value, field, violations):
    """Resolve a manifest path field: relative, no drive letter, no '..'."""
    if not text(value):
        fail(violations, "schema-type", f"{field}: expected a non-empty relative path string")
        return None
    if re.match(r"^[A-Za-z]:", value) or value.startswith(("/", "\\")):
        fail(violations, "path-absolute", f"{field}: absolute paths are refused: {value!r}")
        return None
    parts = Path(value).as_posix().split("/")
    if ".." in parts:
        fail(violations, "path-escape", f"{field}: '..' escapes the delivery directory: {value!r}")
        return None
    return manifest_dir / value


def check_schema(manifest, violations):
    required = {
        "engine": str,
        "engine_version": str,
        "layout_policy": str,
        "ldm_sha256": str,
        "runtime_conditions": dict,
        "source": dict,
        "exports": list,
        "readback": dict,
        "axes": dict,
        "crossings": dict,
        "hard_failures": list,
        "unresolved": list,
        "user_evaluation": str,
    }
    for key, kind in required.items():
        if key not in manifest:
            fail(violations, "schema-missing", f"missing required field: {key}")
        elif not isinstance(manifest[key], kind):
            fail(violations, "schema-type", f"{key}: expected {kind.__name__}")
    extra = sorted(set(manifest) - set(required))
    if extra:
        fail(violations, "schema-extra", f"unknown fields (closed set): {extra}")


def check_runtime(manifest, violations):
    conditions = manifest.get("runtime_conditions")
    if not isinstance(conditions, dict):
        return
    for key in ("executor", "model", "context_window", "reasoning_effort", "config_root"):
        if key not in conditions:
            fail(violations, "runtime-missing", f"runtime_conditions.{key} missing")
        elif not text(conditions[key]):
            fail(violations, "runtime-missing", f"runtime_conditions.{key} must be a value or not_provided")
    extra = sorted(set(conditions) - {"executor", "model", "context_window", "reasoning_effort", "config_root"})
    if extra:
        fail(violations, "schema-extra", f"runtime_conditions: unknown fields {extra}")


def check_source(manifest, manifest_dir, violations):
    source = manifest.get("source")
    if not isinstance(source, dict):
        return None
    if set(source) != {"path", "format", "sha256"}:
        fail(violations, "schema-extra", f"source: expected keys path/format/sha256, got {sorted(source)}")
        return None
    if source.get("format") not in SOURCE_FORMATS:
        fail(violations, "enum", f"source.format {source.get('format')!r} not in {SOURCE_FORMATS}")
    if not HEX64.match(str(source.get("sha256", ""))):
        fail(violations, "schema-type", "source.sha256 must be 64 lowercase hex characters")
    path = relative_path(manifest_dir, source.get("path"), "source.path", violations)
    if path is None:
        return None
    if not path.is_file():
        fail(violations, "source-missing", f"source file not found: {source.get('path')!r}")
        return None
    actual = sha256_file(path)
    if HEX64.match(str(source.get("sha256", ""))) and actual != source["sha256"]:
        fail(violations, "source-hash", f"source.sha256 mismatch: manifest {source['sha256']} != actual {actual}")
    return path


def check_echo(manifest, source_path, violations):
    ldm = manifest.get("ldm_sha256")
    if not text(ldm):
        fail(violations, "schema-type", "ldm_sha256 must be a non-empty hash")
        return
    if not HEX64.match(ldm):
        fail(violations, "schema-type", "ldm_sha256 must be 64 lowercase hex characters")
    source = manifest.get("source") or {}
    if source_path is not None and ldm and source.get("sha256") == ldm:
        fail(
            violations,
            "ldm-echo",
            "ldm_sha256 equals source.sha256 — the delivered 'source' is the semantic input "
            "byte-for-byte; no native drawing source was produced (input echo)",
        )


def check_exports(manifest, manifest_dir, violations):
    exports = manifest.get("exports")
    if not isinstance(exports, list):
        return []
    if not exports:
        fail(violations, "exports-empty", "exports: at least one real export is required")
        return []
    usable = []
    for index, item in enumerate(exports):
        if not isinstance(item, dict):
            fail(violations, "schema-type", f"exports[{index}]: expected an object")
            continue
        expected = {"path", "format", "width", "height", "produced_by"}
        if set(item) != expected:
            fail(violations, "schema-extra", f"exports[{index}]: expected keys {sorted(expected)}, got {sorted(item)}")
            continue
        fmt = item.get("format")
        if fmt not in EXPORT_FORMATS:
            fail(violations, "enum", f"exports[{index}].format {fmt!r} not in {EXPORT_FORMATS}")
            continue
        if not text(item.get("produced_by")):
            fail(violations, "schema-type", f"exports[{index}].produced_by must name the command/request")
        for dimension in ("width", "height"):
            value = item.get(dimension)
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value <= 0):
                fail(violations, "schema-type", f"exports[{index}].{dimension} must be a positive integer or null")
        path = relative_path(manifest_dir, item.get("path"), f"exports[{index}].path", violations)
        if path is None:
            continue
        if not path.is_file():
            fail(violations, "export-missing", f"exports[{index}]: file not found: {item.get('path')!r}")
            continue
        data = path.read_bytes()[:4096]
        if path.stat().st_size == 0:
            fail(violations, "export-empty", f"exports[{index}]: file is empty: {item.get('path')!r}")
            continue
        if fmt in MAGIC and not MAGIC[fmt](data):
            fail(violations, "export-magic", f"exports[{index}]: content does not look like {fmt}: {item.get('path')!r}")
            continue
        usable.append(fmt)
    return usable


def check_readback(manifest, violations):
    readback = manifest.get("readback")
    axes = manifest.get("axes") or {}
    if not isinstance(readback, dict):
        return
    expected = {"method", "elements", "zones", "relations", "labels", "parents", "directions"}
    if set(readback) != expected:
        fail(violations, "schema-extra", f"readback: expected keys {sorted(expected)}, got {sorted(readback)}")
        return
    for key in ("elements", "zones", "relations", "labels"):
        value = readback.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            fail(violations, "schema-type", f"readback.{key} must be a non-negative integer")
    for key in ("parents", "directions"):
        if readback.get(key) not in READBACK_STATES:
            fail(violations, "enum", f"readback.{key} {readback.get(key)!r} not in {READBACK_STATES}")
    if axes.get("semantic") == "pass" and str(readback.get("method", "")).strip().lower() in ECHO_METHODS:
        fail(
            violations,
            "readback-missing",
            "axes.semantic=pass requires readback.method naming the real native-source/render "
            "reader; input-copy/none/empty is refused",
        )
    if axes.get("semantic") == "pass" and readback.get("directions") == "not_checked":
        fail(violations, "semantic-no-directions", "axes.semantic=pass requires readback.directions verified/partial")
    zones = readback.get("zones")
    if axes.get("semantic") == "pass" and isinstance(zones, int) and zones > 0 and readback.get("parents") == "not_checked":
        fail(violations, "semantic-no-parents", "axes.semantic=pass with zones>0 requires readback.parents verified/partial")


def check_axes(manifest, usable_exports, violations):
    axes = manifest.get("axes")
    if not isinstance(axes, dict):
        return
    if set(axes) != set(AXES):
        fail(violations, "schema-extra", f"axes: expected keys {sorted(AXES)}, got {sorted(axes)}")
        return
    for key, domain in AXES.items():
        if axes.get(key) not in domain:
            fail(violations, "enum", f"axes.{key} {axes.get(key)!r} not in {domain}")
    crossings = manifest.get("crossings") or {}
    if axes.get("visual") == "pass":
        if crossings.get("measured") is not True:
            fail(
                violations,
                "visual-no-crossings",
                "axes.visual=pass requires crossings.measured=true — the visual axis is quantified, "
                "not asserted (count/collinear_length may be null but must be measured)",
            )
        if not any(fmt in ("svg", "png", "pdf") for fmt in usable_exports):
            fail(violations, "visual-no-export", "axes.visual=pass requires a decodable svg/png/pdf export")
    failures = manifest.get("hard_failures")
    if isinstance(failures, list):
        for item in failures:
            if not text(item):
                fail(violations, "schema-type", "hard_failures entries must be non-empty strings")
        if failures and (axes.get("semantic") == "pass" or axes.get("visual") == "pass"):
            fail(
                violations,
                "hard-failure-contradiction",
                "hard_failures is non-empty while semantic/visual is 'pass' — a hard failure "
                "cannot be offset by another axis",
            )


def check_crossings(manifest, manifest_dir, violations):
    crossings = manifest.get("crossings")
    if not isinstance(crossings, dict):
        return
    expected = {"measured", "count", "collinear_length", "report_ref"}
    if set(crossings) != expected:
        fail(violations, "schema-extra", f"crossings: expected keys {sorted(expected)}, got {sorted(crossings)}")
        return
    if not isinstance(crossings.get("measured"), bool):
        fail(violations, "schema-type", "crossings.measured must be true/false")
    count = crossings.get("count")
    if count is not None and (not isinstance(count, int) or isinstance(count, bool) or count < 0):
        fail(violations, "schema-type", "crossings.count must be a non-negative integer or null")
    length = crossings.get("collinear_length")
    if length is not None and (not isinstance(length, (int, float)) or isinstance(length, bool) or length < 0):
        fail(violations, "schema-type", "crossings.collinear_length must be a non-negative number or null")
    ref = crossings.get("report_ref")
    if ref is not None:
        path = relative_path(manifest_dir, ref, "crossings.report_ref", violations)
        if path is not None and not path.is_file():
            fail(violations, "crossings-report-missing", f"crossings.report_ref file not found: {ref!r}")


def check_user_evaluation(manifest, violations):
    value = manifest.get("user_evaluation")
    if not isinstance(value, str):
        return
    if value == "not_available":
        return
    if value.startswith("provided:") and text(value[len("provided:"):]):
        return
    fail(
        violations,
        "user-eval-claim",
        "user_evaluation must be 'not_available' or 'provided:<summary>' — silence is not "
        "satisfaction and a bare 'satisfied/通过/满意' is refused",
    )


def recount_drawio(source_path, violations):
    """Independent native-source recount for drawio mxCell XML."""
    try:
        payload = source_path.read_text(encoding="utf-8")
        if re.search(r"<!DOCTYPE|<!ENTITY", payload, re.I):
            fail(violations, "drawio-parse", "DTD/ENTITY declarations are refused in drawio sources")
            return None
        root = ET.fromstring(payload)
    except (ET.ParseError, UnicodeError, OSError) as exc:
        fail(violations, "drawio-parse", f"cannot parse drawio source: {exc}")
        return None
    model = root if root.tag == "mxGraphModel" else root.find(".//mxGraphModel")
    if model is None:
        fail(violations, "drawio-parse", "no mxGraphModel found in the source")
        return None
    root_cell = model.find("root")
    if root_cell is None:
        fail(violations, "drawio-parse", "no mxGraphModel/root found in the source")
        return None
    elements = zones = relations = 0
    for cell in root_cell.findall("mxCell"):
        style = cell.get("style", "")
        if cell.get("vertex") == "1":
            if "container=1" in style.replace(" ", ""):
                zones += 1
            else:
                elements += 1
        elif cell.get("edge") == "1":
            relations += 1
    return {"elements": elements, "zones": zones, "relations": relations}


def run(manifest_path):
    violations = []
    try:
        require(manifest_path.is_file(), f"manifest not found: {manifest_path}")
        require(manifest_path.stat().st_size <= MAX_BYTES, "manifest exceeds 1 MB")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (ManifestError, json.JSONDecodeError, OSError, UnicodeError) as exc:
        return {"status": "fail", "manifest": str(manifest_path), "violations": [{"code": "manifest-unreadable", "detail": str(exc)}]}
    require(isinstance(manifest, dict), "manifest must be a JSON object")
    manifest_dir = manifest_path.parent
    check_schema(manifest, violations)
    if manifest.get("engine") not in ENGINES:
        fail(violations, "enum", f"engine {manifest.get('engine')!r} not in {ENGINES}")
    if manifest.get("layout_policy") not in ("preserve", "optimize"):
        fail(violations, "enum", f"layout_policy {manifest.get('layout_policy')!r} not in ('preserve', 'optimize')")
    if not text(manifest.get("engine_version")):
        fail(violations, "schema-type", "engine_version must be a version string or not_exposed")
    check_runtime(manifest, violations)
    source_path = check_source(manifest, manifest_dir, violations)
    check_echo(manifest, source_path, violations)
    usable = check_exports(manifest, manifest_dir, violations)
    check_readback(manifest, violations)
    check_axes(manifest, usable, violations)
    check_crossings(manifest, manifest_dir, violations)
    check_user_evaluation(manifest, violations)
    native = "not_supported"
    if manifest.get("engine") == "drawio" and source_path is not None:
        actual = recount_drawio(source_path, violations)
        if actual is not None:
            readback = manifest.get("readback") or {}
            for key in ("elements", "zones", "relations"):
                claimed = readback.get(key)
                if isinstance(claimed, int) and claimed != actual[key]:
                    fail(
                        violations,
                        "native-recount-mismatch",
                        f"drawio native recount: {key}={actual[key]} in the source, "
                        f"manifest readback says {claimed}",
                    )
            native = {"status": "recounted", "cells": actual}
    verdict = {
        "status": "pass" if not violations else "fail",
        "manifest": str(manifest_path),
        "engine": manifest.get("engine"),
        "violations": violations,
        "native_recount": native,
    }
    return verdict


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check a draw-diagram result manifest against the delivered artifacts "
        "(quality-gate.md). Exit 0 pass, 1 violations, 2 usage/I-O error.",
        allow_abbrev=False,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--manifest", type=Path, required=True, help="path to the manifest JSON")
    parser.add_argument("--json", action="store_true", help="emit the verdict as JSON")
    args = parser.parse_args(argv)
    try:
        verdict = run(args.manifest)
    except ManifestError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(verdict, ensure_ascii=False, indent=2))
    else:
        print(f"manifest: {verdict['manifest']}")
        print(f"status:   {verdict['status']}")
        for violation in verdict["violations"]:
            print(f"  [{violation['code']}] {violation['detail']}")
        native = verdict.get("native_recount")
        if isinstance(native, dict):
            print(f"native recount: {native['cells']}")
        elif native == "not_supported":
            print("native recount: not_supported (engine native format is not parsed here; "
                  "the engine entry owns its readback)")
    return 0 if verdict["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
