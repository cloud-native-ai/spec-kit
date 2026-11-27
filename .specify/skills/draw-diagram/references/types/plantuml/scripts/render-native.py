#!/usr/bin/env python3
"""render-native.py - thin, safe client for a caller-supplied PlantUML server.

The caller supplies the server URL at runtime; this script never hardcodes a
service address and never falls back to a public server or a local renderer.
It performs a real preflight, then renders the exact source file as SVG and PNG
through the standard PlantUML HTTP protocol:
    GET {server}/svg/{encoded}
    GET {server}/png/{encoded}
where {encoded} is the PlantUML deflate + custom-base64 encoding.

Only the source is styled by the caller: this client does not rewrite style
lines, except that for PNG it may replace the source's `scale N` line with a
smaller integer N when the SVG viewBox would exceed --png-max.

Interface:
  render-native.py --source <file.puml> --server <base-url>
                   --output-dir <dir> --prefix <name>
                   [--report <new.json>] [--timeout 30] [--png-max 4095]

Exit codes:
  0  SVG and PNG rendered and validated
  2  usage or I/O error (including refusing to overwrite existing outputs)
  3  preflight failed: the caller-supplied renderer is unavailable (nothing rendered)
  4  rendering or output validation failed after a successful preflight
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import zlib
from pathlib import Path

VERSION = "1.0.0"
USER_AGENT = "render-native.py/1.0 (draw-diagram plantuml thin client)"
PREFLIGHT_SOURCE = "@startuml\nA -> B : ping\n@enduml\n"


def encode_puml(text: str) -> str:
    def e6(b: int) -> str:
        if b < 10:
            return chr(48 + b)
        b -= 10
        if b < 26:
            return chr(65 + b)
        b -= 26
        if b < 26:
            return chr(97 + b)
        b -= 26
        return "-" if b == 0 else ("_" if b == 1 else "?")

    def a3(b1: int, b2: int, b3: int) -> str:
        return (e6((b1 >> 2) & 0x3F) + e6(((b1 & 0x3) << 4 | b2 >> 4) & 0x3F)
                + e6(((b2 & 0xF) << 2 | b3 >> 6) & 0x3F) + e6(b3 & 0x3F))

    compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
    data = compressor.compress(text.encode("utf-8")) + compressor.flush()
    out = []
    for i in range(0, len(data), 3):
        chunk = data[i:i + 3]
        out.append(a3(chunk[0], chunk[1] if len(chunk) > 1 else 0, chunk[2] if len(chunk) > 2 else 0))
    return "".join(out)


def http_get(url: str, timeout: float):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
        return response.status, response.headers.get("Content-Type", ""), body


def normalize_server(server: str) -> str:
    server = server.rstrip("/")
    if not re.match(r"^https?://[^\s/]+(/[^\s?#]*)?$", server) or "?" in server or "#" in server:
        raise ValueError("--server must be an http(s) base URL without query/fragment")
    return server


def viewbox_of(svg_text: str):
    match = re.search(r'viewBox="([\d.\s-]+)"', svg_text)
    if not match:
        return None
    parts = [float(v) for v in match.group(1).split()]
    return parts if len(parts) == 4 else None


def png_scaled_source(source: str, viewbox, png_max: int, current_scale: float):
    base = max(viewbox[2], viewbox[3]) / current_scale
    target = int(png_max // base) if base else 1
    target = max(1, min(target, int(current_scale)))
    if target == int(current_scale):
        return source, current_scale, False
    if re.search(r"(?m)^\s*scale\s+[0-9.]+\s*$", source):
        adjusted = re.sub(r"(?m)^\s*scale\s+[0-9.]+\s*$", f"scale {target}", source, count=1)
    else:
        adjusted = re.sub(r"(?m)^(@start\w+.*)$", r"\1\nscale %d" % target, source, count=1)
    return adjusted, target, True


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="render-native.py",
        description="Render a PlantUML source through a caller-supplied PlantUML server. "
                    "No hardcoded server, no public fallback, no local renderer.",
        epilog="Exit codes: 0 rendered, 2 usage/IO error, 3 preflight failed, 4 render/validation failed.",
    )
    parser.add_argument("--source", required=True, help=".puml file to render as-is")
    parser.add_argument("--server", required=True,
                        help="PlantUML server base URL, e.g. http://host:port/plantuml")
    parser.add_argument("--output-dir", required=True, help="directory for the SVG/PNG outputs")
    parser.add_argument("--prefix", required=True, help="output basename without extension")
    parser.add_argument("--report", default=None, help="optional new JSON provenance report path")
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout seconds (default 30)")
    parser.add_argument("--png-max", type=int, default=4095,
                        help="maximum PNG edge in pixels before reducing scale (default 4095)")
    parser.add_argument("--version", action="version", version=f"render-native.py {VERSION}")
    args = parser.parse_args(argv)

    source_path = Path(args.source)
    if not source_path.is_file():
        print(f"error: source not found: {source_path}", file=sys.stderr)
        return 2
    try:
        server = normalize_server(args.server)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    output_dir = Path(args.output_dir)
    svg_path = output_dir / f"{args.prefix}.svg"
    png_path = output_dir / f"{args.prefix}.png"
    report_path = Path(args.report) if args.report else None
    for path in [svg_path, png_path] + ([report_path] if report_path else []):
        if path.exists():
            print(f"error: refusing to overwrite existing output: {path}", file=sys.stderr)
            return 2
    source = source_path.read_text(encoding="utf-8")
    scale_match = re.search(r"(?m)^\s*scale\s+([0-9.]+)\s*$", source)
    current_scale = float(scale_match.group(1)) if scale_match else 1.0

    summary = {
        "schema": "plantuml-render-native/1",
        "tool": {"name": "render-native.py", "version": VERSION},
        "server": server,
        "source": str(source_path),
        "preflight": None,
        "svg": None,
        "png": None,
        "status": "not_started",
        "limits": [
            "Only the caller-supplied server is used; a failed preflight stops before rendering.",
            "The source file is rendered as-is; PNG scale may be reduced to respect --png-max.",
        ],
    }

    try:
        status, content_type, body = http_get(f"{server}/svg/{encode_puml(PREFLIGHT_SOURCE)}", args.timeout)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        summary["preflight"] = {"url": f"{server}/svg/<preflight>", "ok": False, "error": str(exc)}
        summary["status"] = "preflight_failed"
        print(f"error: renderer preflight failed at {server}: {exc}", file=sys.stderr)
        if report_path:
            report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 3
    preflight_ok = status == 200 and b"<svg" in body[:4096]
    summary["preflight"] = {
        "url": f"{server}/svg/<preflight>", "ok": preflight_ok,
        "status": status, "content_type": content_type,
    }
    if not preflight_ok:
        summary["status"] = "preflight_failed"
        print(f"error: renderer preflight returned status {status} ({content_type})", file=sys.stderr)
        if report_path:
            report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 3

    try:
        status, content_type, svg_bytes = http_get(f"{server}/svg/{encode_puml(source)}", args.timeout)
        svg_text = svg_bytes.decode("utf-8", errors="replace")
        if status != 200 or "<svg" not in svg_text[:4096]:
            raise ValueError(f"SVG render returned status {status} ({content_type})")
        viewbox = viewbox_of(svg_text)
        if not viewbox:
            raise ValueError("rendered SVG has no viewBox")
        output_dir.mkdir(parents=True, exist_ok=True)
        svg_path.write_bytes(svg_bytes)
        summary["svg"] = {
            "path": str(svg_path), "bytes": len(svg_bytes), "status": status,
            "content_type": content_type, "viewbox": viewbox,
            "scale": current_scale,
        }

        png_source, png_scale, changed = png_scaled_source(source, viewbox, args.png_max, current_scale)
        status, content_type, png_bytes = http_get(f"{server}/png/{encode_puml(png_source)}", args.timeout)
        if status != 200 or not png_bytes.startswith(b"\x89PNG\r\n\x1a\n") or len(png_bytes) < 1000:
            raise ValueError(f"PNG render returned status {status}, {len(png_bytes)} bytes ({content_type})")
        png_path.write_bytes(png_bytes)
        summary["png"] = {
            "path": str(png_path), "bytes": len(png_bytes), "status": status,
            "content_type": content_type, "scale": png_scale, "scale_adjusted": changed,
            "png_max": args.png_max,
        }
        summary["status"] = "rendered"
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        summary["status"] = "render_failed"
        summary["error"] = str(exc)
        print(f"error: {exc}", file=sys.stderr)
        if report_path:
            report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 4

    if report_path:
        report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "svg": summary["svg"]["path"],
                      "png": summary["png"]["path"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
