#!/usr/bin/env python3
"""render-client.py — safe thin client for the shared Excalidraw render service.

The service URL is supplied by the caller at runtime; this client never embeds
a host. It follows the shared service contract (owner:
references/self-deploy-render-service.md): POST /svg and POST /png with the
Excalidraw scene JSON as the request body, and GET /healthz as a preflight.

Behaviour:
  * preflight GET /healthz (short timeout) — an unavailable service stops the
    run with exit 2; the client never guesses another endpoint and never falls
    back to a different renderer;
  * POST /svg and POST /png; both outputs must be non-empty and carry the right
    magic bytes (SVG root element / PNG signature) before they are kept;
  * existing output files are refused (this client never overwrites);
  * a JSON summary (preflight, per-request status/bytes/sha256/duration, output
    paths and PNG dimensions) is printed; the same object is written when
    --summary is given.

Usage:
  render-client.py --server <base-url> --scene <scene.excalidraw>
                   --out-dir <dir> --prefix <name> [--scale N] [--summary <json>]

Exit codes:
  0 both exports written and verified
  1 a render request failed, or an output failed its magic-byte/empty check
  2 usage error, unreadable scene, unavailable service, or an existing output
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

VERSION = "1.0.0"
UA = "draw-diagram-excalidraw-client/1.0"


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def png_size(data):
    if len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        width, height = struct.unpack(">II", data[16:24])
        return width, height
    return None


def request_json(url, payload, timeout):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="render-client.py",
        description="POST an Excalidraw scene to the shared render service and keep verified SVG+PNG.",
        epilog="exit codes: 0 both exports verified; 1 render/magic failure; 2 usage, unreadable scene, "
               "unavailable service, or existing output",
    )
    parser.add_argument("--server", required=True, help="runtime base URL, e.g. http://host:PORT (never hardcoded)")
    parser.add_argument("--scene", required=True, help=".excalidraw scene file")
    parser.add_argument("--out-dir", required=True, help="existing directory for <prefix>.svg/.png")
    parser.add_argument("--prefix", required=True, help="output name stem")
    parser.add_argument("--scale", type=int, default=None, help="optional PNG scale hint passed in the request body")
    parser.add_argument("--padding", type=int, default=None, help="optional export padding hint")
    parser.add_argument("--timeout", type=float, default=180.0, help="per-request timeout seconds")
    parser.add_argument("--summary", help="new JSON path for the request summary (must not exist)")
    parser.add_argument("--version", action="version", version=f"render-client.py {VERSION}")
    args = parser.parse_args(argv)

    base = args.server.rstrip("/")
    if not (base.startswith("http://") or base.startswith("https://")):
        print("error: --server must be an http(s) base URL", file=sys.stderr)
        return 2
    scene_path = Path(args.scene)
    out_dir = Path(args.out_dir)
    if not scene_path.is_file():
        print(f"error: scene not found: {scene_path}", file=sys.stderr)
        return 2
    if not out_dir.is_dir():
        print(f"error: --out-dir must exist: {out_dir}", file=sys.stderr)
        return 2
    svg_out = out_dir / f"{args.prefix}.svg"
    png_out = out_dir / f"{args.prefix}.png"
    for target in (svg_out, png_out):
        if target.exists():
            print(f"error: refusing to overwrite existing output: {target}", file=sys.stderr)
            return 2
    if args.summary and Path(args.summary).exists():
        print(f"error: refusing to overwrite existing summary: {args.summary}", file=sys.stderr)
        return 2
    try:
        scene = json.loads(scene_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read scene: {exc}", file=sys.stderr)
        return 2

    summary = {"server": base, "scene": str(scene_path), "scene_sha256": sha256_bytes(scene_path.read_bytes()),
               "preflight": None, "requests": [], "outputs": []}

    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(urllib.request.Request(f"{base}/healthz", headers={"User-Agent": UA}),
                                    timeout=8) as resp:
            body = resp.read(200).decode("utf-8", "replace")
            summary["preflight"] = {"status": resp.status, "body": body}
            if resp.status != 200 or "ok" not in body.lower():
                print(f"error: render service unhealthy: {resp.status} {body!r}", file=sys.stderr)
                _write_summary(args.summary, summary)
                return 2
    except (urllib.error.URLError, OSError) as exc:
        summary["preflight"] = {"error": f"{type(exc).__name__}: {exc}"}
        print(f"error: render service unavailable at {base}: {exc}", file=sys.stderr)
        _write_summary(args.summary, summary)
        return 2
    summary["preflight"]["duration_s"] = round(time.monotonic() - t0, 3)

    payload = dict(scene)
    for fmt, target, magic in (("svg", svg_out, b"<svg"), ("png", png_out, b"\x89PNG\r\n\x1a\n")):
        body_obj = dict(payload)
        if args.scale is not None:
            body_obj["scale"] = args.scale
        if args.padding is not None:
            body_obj["padding"] = args.padding
        start = time.monotonic()
        try:
            with request_json(f"{base}/{fmt}", body_obj, args.timeout) as resp:
                data = resp.read()
                row = {"format": fmt, "status": resp.status, "content_type": resp.headers.get("Content-Type"),
                       "bytes": len(data), "sha256": sha256_bytes(data),
                       "duration_s": round(time.monotonic() - start, 3)}
        except urllib.error.HTTPError as exc:
            row = {"format": fmt, "http_error": exc.code,
                   "body": exc.read(400).decode("utf-8", "replace"),
                   "duration_s": round(time.monotonic() - start, 3)}
            summary["requests"].append(row)
            print(f"error: {fmt} render failed: HTTP {exc.code}", file=sys.stderr)
            _write_summary(args.summary, summary)
            return 1
        except (urllib.error.URLError, OSError) as exc:
            row = {"format": fmt, "error": f"{type(exc).__name__}: {exc}",
                   "duration_s": round(time.monotonic() - start, 3)}
            summary["requests"].append(row)
            print(f"error: {fmt} render failed: {exc}", file=sys.stderr)
            _write_summary(args.summary, summary)
            return 1
        summary["requests"].append(row)
        if not data:
            print(f"error: {fmt} output is empty", file=sys.stderr)
            _write_summary(args.summary, summary)
            return 1
        if fmt == "svg":
            if magic not in data[:4096]:
                print("error: svg body does not contain an <svg> root", file=sys.stderr)
                _write_summary(args.summary, summary)
                return 1
        else:
            size = png_size(data)
            if size is None:
                print("error: png body is not a PNG", file=sys.stderr)
                _write_summary(args.summary, summary)
                return 1
            row["width"], row["height"] = size
        target.write_bytes(data)
        summary["outputs"].append({"path": str(target), "bytes": len(data),
                                   "sha256": row["sha256"]})

    _write_summary(args.summary, summary)
    print(json.dumps(summary, ensure_ascii=False))
    return 0


def _write_summary(path, summary):
    if path:
        Path(path).write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
