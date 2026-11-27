#!/usr/bin/env python3
"""render-client.py — bounded, safe transport for engine-documented render routes.

The draw-diagram front door does not render; engine layers own their request
shapes. This client only carries ONE request that the caller fully specifies:

  * --service-url   the render service base URL (http/https, host[:port] only —
                    no path, query, fragment or userinfo). The caller supplies it
                    at run time; nothing is discovered or guessed.
  * --route         the request path starting with '/', exactly as the engine doc
                    defines it (already percent-encoded where the protocol needs
                    it). The client never re-encodes, compresses or rewrites it.
  * --method        GET (default) or POST; POST needs --body and --content-type.
  * --body          raw bytes, sent verbatim. Engine protocols (zlib/base64,
                    scene JSON, XML) stay in the engine layer; this client is not
                    a second implementation of them.
  * --expect        closed set svg|png|html|javascript|json|text|any. The response
                    must have a matching media type (and, for svg/png/html/json, a
                    matching magic prefix) before anything is written.
  * --timeout       bounded 1..120 s. No retries.
  * --max-bytes     bounded response size (1 KiB..512 MiB).
  * --output        a NEW file; an existing file is refused before any request.
  * --receipt       optional NEW JSON file recording transport evidence only:
                    every other axis is marked not_evaluated on purpose.
  * --preflight-route
                    optional path probed with GET first; if it does not answer
                    2xx the main request is not sent and no output is written.
  * --preflight-only
                    probe the preflight route and exit; useful for the front-door
                    preflight step without compound shell lines.

Behavior is deliberately narrow: redirects are refused (a 3xx is an error),
credentials/cookies/auth headers are not supported, and there is no layout,
rendering, endpoint inference, retry or deployment logic here.

Exit codes:
  0 response written (and receipt, when requested)
  2 usage/argument error
  3 preflight unavailable — rendering stopped, nothing written
  4 request/response failure — non-2xx, unexpected media type/magic, size cap,
    timeout or redirect; nothing written
  5 output/receipt already exists or cannot be written
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

VERSION = "1.0.0"
RECORD = f"draw-diagram.render-client/{VERSION}"
EXPECTED = ("svg", "png", "html", "javascript", "json", "text", "any")
EXPECTED_MEDIA = {
    "svg": ("image/svg+xml",),
    "png": ("image/png",),
    "html": ("text/html", "application/xhtml+xml"),
    "javascript": ("application/javascript", "text/javascript"),
    "json": ("application/json",),
    "text": ("text/",),
}
MAX_TIMEOUT = 120
MAX_RESPONSE_BYTES = 512 * 1024 * 1024
MAX_REQUEST_BYTES = 64 * 1024 * 1024
CONTENT_TYPE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]*/[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]*(?:\s*;\s*[^\r\n]{1,200})?$")
AXES_NOT_EVALUATED = {
    "transport": None,
    "runtime_identity": "not_evaluated",
    "permission_events": "not_evaluated",
    "required_steps": "not_evaluated",
    "business_result": "not_evaluated",
}


class UsageError(ValueError):
    pass


class StageError(RuntimeError):
    def __init__(self, stage, kind, detail):
        super().__init__(detail)
        self.stage = stage
        self.kind = kind
        self.detail = detail


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def text(value):
    return isinstance(value, str) and value.strip() != ""


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise UsageError(message)


_INTERNAL_HOST_SUFFIX = ".aliyun-inc.com"
_PRIVATE_PATTERNS = (
    re.compile(r"127(?:\.\d{1,3}){3}"),
    re.compile(r"10(?:\.\d{1,3}){3}"),
    re.compile(r"192\.168(?:\.\d{1,3}){2}"),
    re.compile(r"172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}"),
)


def require_internal_host(host):
    """Hard rule (user ruling 2026-11-27): public render backends are forbidden.

    Allowed: localhost, loopback/private IPv4 and *.aliyun-inc.com. Anything else
    is a data-egress path for diagram sources, so it fails as a usage error.
    """
    h = (host or "").lower().rstrip(".")
    if h in ("localhost", "::1"):
        return
    if any(p.fullmatch(h) for p in _PRIVATE_PATTERNS):
        return
    if h.endswith(_INTERNAL_HOST_SUFFIX) and h != _INTERNAL_HOST_SUFFIX:
        return
    raise UsageError(
        f"--service-url host is not internal: {host!r} "
        "(public render backends are forbidden; use xuanji-render.aliyun-inc.com, "
        "a private address or localhost)"
    )


def validate_service_url(value):
    require(text(value), "--service-url is required")
    require(value.isascii(), "--service-url must be ASCII (use an IDNA/punycode host)")
    parts = urllib.parse.urlsplit(value)
    require(parts.scheme in ("http", "https"), "--service-url must use http or https")
    require(parts.netloc != "", "--service-url must include a host (and optional port)")
    require(parts.path in ("", "/"), "--service-url must not carry a path; pass it with --route")
    require(parts.query == "" and parts.fragment == "", "--service-url must not carry a query or fragment")
    require("@" not in parts.netloc, "--service-url must not embed credentials")
    require(parts.hostname is not None, "--service-url must include a hostname")
    require_internal_host(parts.hostname)
    try:
        port = parts.port
    except ValueError as exc:
        raise UsageError(f"--service-url has an invalid port: {exc}") from exc
    require(port is None or 1 <= port <= 65535, "--service-url port must be 1..65535")
    require(not any(ch.isspace() or ord(ch) < 0x20 for ch in value), "--service-url must not contain whitespace or control characters")
    return value.rstrip("/")


def validate_route(value, flag):
    require(text(value), f"{flag} is required")
    require(value.isascii(), f"{flag} must be ASCII; percent-encode non-ASCII protocol input")
    require(value.startswith("/"), f"{flag} must start with '/'")
    require(not value.startswith("//"), f"{flag} must not start with '//'")
    require("#" not in value, f"{flag} must not carry a fragment")
    require(not any(ch.isspace() or ord(ch) < 0x20 for ch in value), f"{flag} must not contain whitespace or control characters")
    require(".." not in value.split("/"), f"{flag} must not contain '..' segments")
    require(len(value) <= 1_000_000, f"{flag} is longer than the 1,000,000 byte cap")
    return value


def validate_content_type(value):
    require(text(value), "--content-type is required for POST")
    require(bool(CONTENT_TYPE.match(value)), "--content-type is not a plain media type")
    return value


def validate_timeout(value):
    require(1 <= value <= MAX_TIMEOUT, f"--timeout must be within 1..{MAX_TIMEOUT} seconds")
    return float(value)


def validate_max_bytes(value):
    require(1024 <= value <= MAX_RESPONSE_BYTES, "--max-bytes must be within 1 KiB..512 MiB")
    return value


def media_matches(expect, content_type):
    if expect == "any":
        return True
    media = (content_type or "").split(";", 1)[0].strip().lower()
    candidates = EXPECTED_MEDIA[expect]
    return any(media == item or (item.endswith("/") and media.startswith(item)) for item in candidates)


def magic_matches(expect, data):
    if expect == "svg":
        return b"<svg" in data[:4096]
    if expect == "png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    if expect == "html":
        return b"<" in data[:4096]
    if expect == "json":
        stripped = data.lstrip()
        return stripped[:1] in (b"{", b"[")
    return True


def build_opener():
    return urllib.request.build_opener(_NoRedirect)


def read_bounded(response, max_bytes):
    chunks = []
    total = 0
    while True:
        chunk = response.read(65536)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise StageError("response", "size-cap", f"response exceeded --max-bytes ({max_bytes})")
        chunks.append(chunk)
    return b"".join(chunks)


def fetch(opener, url, method, body, content_type, timeout, max_bytes, stage, expect):
    headers = {"User-Agent": f"draw-diagram-render-client/{VERSION}"}
    data = None
    if method == "POST":
        headers["Content-Type"] = content_type
        data = body
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    started = time.monotonic()
    try:
        with opener.open(request, timeout=timeout) as response:
            status = response.status
            content_type_value = response.headers.get("Content-Type", "")
            if not 200 <= status < 300:
                raise StageError(stage, "http-status", f"HTTP {status}")
            if stage == "preflight":
                data_bytes = response.read(4096)
            else:
                data_bytes = read_bounded(response, max_bytes)
    except urllib.error.HTTPError as exc:
        duration = int((time.monotonic() - started) * 1000)
        if 300 <= exc.code < 400:
            raise StageError(stage, "redirect", f"HTTP {exc.code}: redirects are not followed (Location={exc.headers.get('Location', '?')!r})") from exc
        raise StageError(stage, "http-status", f"HTTP {exc.code} after {duration} ms") from exc
    except StageError:
        raise
    except Exception as exc:  # noqa: BLE001 - every transport failure becomes a typed stage error
        raise StageError(stage, type(exc).__name__, str(exc) or type(exc).__name__) from exc
    duration = int((time.monotonic() - started) * 1000)
    if not media_matches(expect, content_type_value):
        raise StageError(
            stage,
            "content-type",
            f"expected {expect}, received {content_type_value or '(missing content-type)'}",
        )
    if stage != "preflight" and not magic_matches(expect, data_bytes):
        raise StageError(stage, "magic", f"response body does not look like {expect}")
    return {
        "status": status,
        "content_type": content_type_value,
        "bytes": data_bytes,
        "duration_ms": duration,
    }


def ensure_new_file(path, label):
    if path is None:
        return None
    path = Path(path)
    if path.exists() or path.is_symlink():
        raise StageError("write", "overwrite-refused", f"{label} already exists: {path}")
    if not path.parent.is_dir():
        raise StageError("write", "missing-parent", f"{label} parent directory does not exist: {path.parent}")
    return path


def write_new_bytes(path, data):
    try:
        with open(path, "xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise StageError("write", "overwrite-refused", f"refusing to overwrite: {path}") from exc
    except OSError as exc:
        raise StageError("write", "io", f"cannot write {path}: {exc}") from exc


def write_receipt(path, payload):
    try:
        with open(path, "xb") as handle:
            handle.write((json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    except FileExistsError as exc:
        raise StageError("write", "overwrite-refused", f"refusing to overwrite receipt: {path}") from exc
    except OSError as exc:
        raise StageError("write", "io", f"cannot write receipt {path}: {exc}") from exc


def receipt_payload(args, service_url, route, body):
    axes = dict(AXES_NOT_EVALUATED)
    axes["transport"] = "not_started"
    payload = {
        "record": RECORD,
        "service_url": service_url,
        "request": {
            "method": args.method,
            "route_sha256": digest_bytes(route.encode("utf-8")),
            "route_bytes": len(route.encode("utf-8")),
            "body_bytes": None if body is None else len(body),
            "body_sha256": None if body is None else digest_bytes(body),
            "content_type": args.content_type,
            "expect": args.expect,
        },
        "preflight": "not_performed",
        "timeout_seconds": validate_timeout(args.timeout),
        "axes": axes,
        "notes": [
            "Transport evidence only: this receipt does not assert semantic, visual, interaction, reproducibility or satisfaction results.",
            "No engine encoding, endpoint inference, layout or rendering was performed by this client.",
        ],
    }
    return payload


def finish_receipt(path, payload, failure_code):
    if path is None:
        return failure_code
    try:
        write_receipt(path, payload)
    except StageError as exc:
        print(f"receipt error: {exc.detail}", file=sys.stderr)
        return 5
    return failure_code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Bounded transport for one engine-documented render route. The caller supplies the "
        "service URL, route, method and raw body; the client does not encode, lay out or guess endpoints. "
        "Redirects and overwrites are refused. Exit 0 written, 2 usage, 3 preflight unavailable, "
        "4 request/response failure, 5 output/receipt refusal.",
        allow_abbrev=False,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--service-url", required=True, help="http(s)://host[:port] only; internal hosts only (xuanji-render.aliyun-inc.com / private / localhost)")
    parser.add_argument("--route", default=None, help="request path starting with '/', from the engine doc")
    parser.add_argument("--method", choices=("GET", "POST"), default="GET", help="HTTP method (default GET)")
    parser.add_argument("--body", default=None, help="raw request body file (POST only; sent verbatim)")
    parser.add_argument("--content-type", default=None, help="request Content-Type (required for POST)")
    parser.add_argument("--expect", default=None, help="expected response: svg|png|html|javascript|json|text|any")
    parser.add_argument("--timeout", type=int, default=30, help="request timeout in seconds, 1..120 (default 30)")
    parser.add_argument("--max-bytes", type=int, default=64 * 1024 * 1024, help="response size cap in bytes (default 64 MiB)")
    parser.add_argument("--output", default=None, help="new output file; an existing file is refused")
    parser.add_argument("--receipt", default=None, help="optional new JSON receipt (transport axis only)")
    parser.add_argument("--preflight-route", default=None, help="optional GET route probed before the request")
    parser.add_argument("--preflight-expect", default="text", help="expected media kind for the preflight route (default text)")
    parser.add_argument("--preflight-only", action="store_true", help="probe the preflight route and exit (no output file)")
    args = parser.parse_args(argv)

    try:
        service_url = validate_service_url(args.service_url)
        timeout = validate_timeout(args.timeout)
        max_bytes = validate_max_bytes(args.max_bytes)
        if args.preflight_expect not in EXPECTED:
            raise UsageError(f"--preflight-expect must be one of {', '.join(EXPECTED)}")
        if args.preflight_route is not None:
            preflight_route = validate_route(args.preflight_route, "--preflight-route")
        else:
            preflight_route = None
        if args.preflight_only:
            require(preflight_route is not None, "--preflight-only requires --preflight-route")
            for flag, value in (("--route", args.route), ("--output", args.output), ("--body", args.body),
                                ("--content-type", args.content_type), ("--expect", args.expect)):
                require(value is None, f"{flag} is not allowed with --preflight-only")
            require(args.method == "GET", "--preflight-only is a GET probe")
        else:
            require(args.route is not None, "--route is required")
            require(args.expect in EXPECTED, f"--expect is required and must be one of {', '.join(EXPECTED)}")
            require(args.output is not None, "--output is required")
            if args.method == "POST":
                require(args.body is not None, "--body is required for POST")
                require(args.content_type is not None, "--content-type is required for POST")
            else:
                require(args.body is None, "--body is only allowed with --method POST")
                require(args.content_type is None, "--content-type is only allowed with --method POST")
        route = None if args.preflight_only else validate_route(args.route, "--route")
        body = None
        if args.body is not None:
            body_path = Path(args.body)
            require(body_path.is_file(), f"--body file not found: {body_path}")
            body = body_path.read_bytes()
            require(0 < len(body) <= MAX_REQUEST_BYTES, f"--body must be 1 byte..{MAX_REQUEST_BYTES} bytes")
        if args.content_type is not None:
            validate_content_type(args.content_type)
    except UsageError as exc:
        print(f"usage error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"I/O error: {exc}", file=sys.stderr)
        return 2

    try:
        output_path = None if args.output is None else ensure_new_file(args.output, "output")
        receipt_path = None if args.receipt is None else ensure_new_file(args.receipt, "receipt")
    except StageError as exc:
        print(f"{exc.kind}: {exc.detail}", file=sys.stderr)
        return 5

    opener = build_opener()
    receipt = receipt_payload(args, service_url, route or (preflight_route or ""), body)
    started = time.monotonic()

    if preflight_route is not None:
        try:
            preflight = fetch(
                opener,
                service_url + preflight_route,
                "GET",
                None,
                None,
                timeout,
                4096,
                "preflight",
                args.preflight_expect,
            )
            receipt["preflight"] = {
                "status": preflight["status"],
                "content_type": preflight["content_type"],
                "duration_ms": preflight["duration_ms"],
                "route_sha256": digest_bytes(preflight_route.encode("utf-8")),
            }
        except StageError as exc:
            receipt["preflight"] = {"error": {"kind": exc.kind, "detail": exc.detail}}
            receipt["error"] = {"stage": "preflight", "kind": exc.kind, "detail": exc.detail}
            receipt["duration_ms"] = int((time.monotonic() - started) * 1000)
            code = finish_receipt(receipt_path, receipt, 3)
            print(f"preflight unavailable: {exc.kind}: {exc.detail}", file=sys.stderr)
            return code
        if args.preflight_only:
            receipt["axes"]["transport"] = "completed"
            receipt["duration_ms"] = int((time.monotonic() - started) * 1000)
            code = finish_receipt(receipt_path, receipt, 0)
            print(f"preflight ok: status={preflight['status']} duration_ms={preflight['duration_ms']}")
            return code

    url = service_url + route
    try:
        result = fetch(
            opener,
            url,
            args.method,
            body,
            args.content_type,
            timeout,
            max_bytes,
            "request",
            args.expect,
        )
    except StageError as exc:
        receipt["error"] = {"stage": "request", "kind": exc.kind, "detail": exc.detail}
        receipt["duration_ms"] = int((time.monotonic() - started) * 1000)
        code = finish_receipt(receipt_path, receipt, 4)
        print(f"request failed: {exc.kind}: {exc.detail}", file=sys.stderr)
        return code

    data = result["bytes"]
    try:
        write_new_bytes(output_path, data)
    except StageError as exc:
        receipt["error"] = {"stage": "write", "kind": exc.kind, "detail": exc.detail}
        receipt["response"] = {
            "status": result["status"],
            "content_type": result["content_type"],
            "bytes": len(data),
            "sha256": digest_bytes(data),
        }
        receipt["duration_ms"] = int((time.monotonic() - started) * 1000)
        code = finish_receipt(receipt_path, receipt, 5)
        print(f"output refused: {exc.detail}", file=sys.stderr)
        return code

    receipt["response"] = {
        "status": result["status"],
        "content_type": result["content_type"],
        "bytes": len(data),
        "sha256": digest_bytes(data),
        "expect": args.expect,
        "magic": "checked" if args.expect != "any" else "not_checked",
    }
    receipt["output"] = {
        "path": os.fspath(output_path),
        "bytes": len(data),
        "sha256": digest_bytes(data),
    }
    receipt["axes"]["transport"] = "completed"
    receipt["duration_ms"] = int((time.monotonic() - started) * 1000)
    code = finish_receipt(receipt_path, receipt, 0)
    print(
        f"written: {output_path} bytes={len(data)} sha256={digest_bytes(data)} "
        f"status={result['status']} duration_ms={result['duration_ms']}"
    )
    return code


if __name__ == "__main__":
    raise SystemExit(main())
