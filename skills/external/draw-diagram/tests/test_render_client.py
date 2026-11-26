"""Positive/negative cases for scripts/render-client.py (safe render transport).

A local in-process HTTP server stands in for the render service; the client is
exercised as a real subprocess. Positive cases cover GET/POST, verbatim body
bytes, preflight and the transport-only receipt. Negative cases cover argument
rejection, overwrite refusal before any request, preflight stop, HTTP/redirect/
content/magic/size failures and the timeout bound. No engine protocol is
implemented here and no business fixture is used.

Run through the repository runner:
    bash scripts/bash/run-tests.sh skills/external/draw-diagram/tests/test_render_client.py -q
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
CLIENT = SKILL_ROOT / "scripts" / "render-client.py"

SVG_BODY = b'<svg xmlns="http://www.w3.org/2000/svg"><text>ok</text></svg>'
PNG_BODY = b"\x89PNG\r\n\x1a\n" + b"0" * 32


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def _send(self, code, content_type, body, location=None):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        if location:
            self.send_header("Location", location)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        route = urllib.parse.urlsplit(self.path).path
        self.server.received.append(("GET", route))
        if route == "/healthz":
            self._send(200, "text/plain", b"ok")
        elif route == "/svg":
            self._send(200, "image/svg+xml", SVG_BODY)
        elif route == "/png":
            self._send(200, "image/png", PNG_BODY)
        elif route == "/html":
            self._send(200, "text/html", b"<!doctype html><html><body>ok</body></html>")
        elif route == "/liar":
            self._send(200, "image/svg+xml", b"not an svg")
        elif route == "/redirect":
            self._send(302, "text/plain", b"", location="/svg")
        elif route == "/missing":
            self._send(404, "text/plain", b"missing")
        elif route == "/slow":
            time.sleep(2.0)
            self._send(200, "text/plain", b"late")
        elif route == "/big":
            self._send(200, "text/plain", b"x" * 200_000)
        elif route == "/preflight-fail":
            self._send(500, "text/plain", b"down")
        else:
            self._send(404, "text/plain", b"unknown")

    def do_POST(self):
        route = urllib.parse.urlsplit(self.path).path
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length)
        self.server.received.append(("POST", route))
        if route == "/echo":
            payload = json.dumps(
                {"length": len(body), "sha256": hashlib.sha256(body).hexdigest()},
                sort_keys=True,
            ).encode("utf-8")
            self._send(200, "application/json", payload)
        else:
            self._send(404, "text/plain", b"unknown")


class _Server(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.received = []

    def handle_error(self, request, client_address):
        pass


class RenderClientCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = _Server(("127.0.0.1", 0), _Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.server.received = []

    def tearDown(self):
        self.tmp.cleanup()

    def client(self, *argv, timeout=60):
        return subprocess.run(
            [sys.executable, str(CLIENT), *argv],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    def common(self, *extra):
        return ("--service-url", self.base, *extra)

    def test_help_version_and_unknown_option(self):
        self.assertEqual(self.client("--help").returncode, 0)
        self.assertEqual(self.client("--version").returncode, 0)
        unknown = self.client("--service-url", self.base, "--definitely-not-a-real-option")
        self.assertEqual(unknown.returncode, 2, unknown.stderr)
        self.assertIn("unrecognized", unknown.stderr)

    def test_get_with_preflight_writes_output_and_transport_receipt(self):
        output = self.dir / "render.svg"
        receipt = self.dir / "receipt.json"
        proc = self.client(
            *self.common(
                "--preflight-route", "/healthz",
                "--route", "/svg",
                "--expect", "svg",
                "--output", str(output),
                "--receipt", str(receipt),
                "--timeout", "10",
            )
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(output.read_bytes(), SVG_BODY)
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        self.assertEqual(payload["preflight"]["status"], 200)
        self.assertEqual(payload["response"]["status"], 200)
        self.assertEqual(payload["response"]["content_type"], "image/svg+xml")
        self.assertEqual(payload["axes"]["transport"], "completed")
        for axis in ("runtime_identity", "permission_events", "required_steps", "business_result"):
            self.assertEqual(payload["axes"][axis], "not_evaluated")
        self.assertEqual([item[1] for item in self.server.received], ["/healthz", "/svg"])
        before = output.read_bytes()
        requests_before = len(self.server.received)
        second = self.client(
            *self.common("--route", "/svg", "--expect", "svg", "--output", str(output), "--timeout", "10")
        )
        self.assertEqual(second.returncode, 5, second.stderr)
        self.assertEqual(output.read_bytes(), before)
        self.assertEqual(len(self.server.received), requests_before)

    def test_png_magic_is_accepted(self):
        output = self.dir / "render.png"
        proc = self.client(*self.common("--route", "/png", "--expect", "png", "--output", str(output)))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(output.read_bytes(), PNG_BODY)

    def test_post_body_is_sent_verbatim(self):
        body = self.dir / "scene.bin"
        raw = b"\x00\x01\xff\x10not-utf8"
        body.write_bytes(raw)
        output = self.dir / "echo.json"
        proc = self.client(
            *self.common(
                "--route", "/echo",
                "--method", "POST",
                "--body", str(body),
                "--content-type", "application/octet-stream",
                "--expect", "json",
                "--output", str(output),
            )
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        echoed = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(echoed["length"], len(raw))
        self.assertEqual(echoed["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(self.server.received, [("POST", "/echo")])

    def test_preflight_only_ok_and_unavailable(self):
        ok = self.client(*self.common("--preflight-route", "/healthz", "--preflight-only"))
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertIn("preflight ok", ok.stdout)
        self.assertEqual(self.server.received, [("GET", "/healthz")])
        self.server.received = []
        down = self.client(*self.common("--preflight-route", "/preflight-fail", "--preflight-only"))
        self.assertEqual(down.returncode, 3, down.stderr)
        self.assertIn("preflight unavailable", down.stderr)
        self.assertEqual(self.server.received, [("GET", "/preflight-fail")])

    def test_preflight_failure_stops_the_render_request(self):
        output = self.dir / "never.svg"
        receipt = self.dir / "receipt.json"
        proc = self.client(
            *self.common(
                "--preflight-route", "/preflight-fail",
                "--route", "/svg",
                "--expect", "svg",
                "--output", str(output),
                "--receipt", str(receipt),
            )
        )
        self.assertEqual(proc.returncode, 3, proc.stderr)
        self.assertFalse(output.exists())
        self.assertEqual(self.server.received, [("GET", "/preflight-fail")])
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        self.assertEqual(payload["axes"]["transport"], "not_started")
        self.assertEqual(payload["error"]["stage"], "preflight")

    def test_http_error_redirect_and_magic_are_refused(self):
        cases = [
            ("/missing", "svg", "http-status"),
            ("/redirect", "svg", "redirect"),
            ("/liar", "svg", "magic"),
            ("/big", "text", "size-cap"),
        ]
        for route, expect, needle in cases:
            with self.subTest(route=route):
                output = self.dir / f"{route.strip('/')}.out"
                extra = ["--max-bytes", "1024"] if route == "/big" else []
                proc = self.client(
                    *self.common("--route", route, "--expect", expect, "--output", str(output), *extra)
                )
                self.assertEqual(proc.returncode, 4, proc.stderr)
                self.assertIn(needle, proc.stderr)
                self.assertFalse(output.exists())

    def test_timeout_is_bounded_and_effective(self):
        output = self.dir / "slow.txt"
        proc = self.client(*self.common("--route", "/slow", "--expect", "text", "--output", str(output), "--timeout", "1"))
        self.assertEqual(proc.returncode, 4, proc.stderr)
        self.assertFalse(output.exists())

    def test_output_refused_before_any_request(self):
        output = self.dir / "existing.svg"
        output.write_text("keep", encoding="utf-8")
        proc = self.client(*self.common("--route", "/svg", "--expect", "svg", "--output", str(output)))
        self.assertEqual(proc.returncode, 5, proc.stderr)
        self.assertEqual(output.read_text(encoding="utf-8"), "keep")
        self.assertEqual(self.server.received, [])

    def test_argument_rejections(self):
        body = self.dir / "body.txt"
        body.write_text("x", encoding="utf-8")
        output = self.dir / "out.bin"
        cases = {
            "service-url-with-path": ["--service-url", self.base + "/prefix", "--route", "/svg", "--expect", "svg", "--output", str(output)],
            "service-url-userinfo": ["--service-url", "http://user:pass@127.0.0.1:1", "--route", "/svg", "--expect", "svg", "--output", str(output)],
            "route-without-slash": ["--service-url", self.base, "--route", "svg", "--expect", "svg", "--output", str(output)],
            "route-scheme-relative": ["--service-url", self.base, "--route", "//evil", "--expect", "svg", "--output", str(output)],
            "route-traversal": ["--service-url", self.base, "--route", "/../etc/passwd", "--expect", "svg", "--output", str(output)],
            "expect-unknown": ["--service-url", self.base, "--route", "/svg", "--expect", "pdf", "--output", str(output)],
            "get-with-body": ["--service-url", self.base, "--route", "/svg", "--expect", "svg", "--output", str(output), "--body", str(body)],
            "post-without-content-type": ["--service-url", self.base, "--route", "/echo", "--method", "POST", "--body", str(body), "--expect", "json", "--output", str(output)],
            "post-without-body": ["--service-url", self.base, "--route", "/echo", "--method", "POST", "--content-type", "application/json", "--expect", "json", "--output", str(output)],
            "timeout-low": ["--service-url", self.base, "--route", "/svg", "--expect", "svg", "--output", str(output), "--timeout", "0"],
            "timeout-high": ["--service-url", self.base, "--route", "/svg", "--expect", "svg", "--output", str(output), "--timeout", "999"],
            "max-bytes-low": ["--service-url", self.base, "--route", "/svg", "--expect", "svg", "--output", str(output), "--max-bytes", "10"],
            "missing-expect": ["--service-url", self.base, "--route", "/svg", "--output", str(output)],
            "preflight-only-without-route": ["--service-url", self.base, "--preflight-only"],
            "preflight-only-with-output": ["--service-url", self.base, "--preflight-route", "/healthz", "--preflight-only", "--output", str(output)],
        }
        for name, argv in cases.items():
            with self.subTest(case=name):
                proc = self.client(*argv)
                self.assertEqual(proc.returncode, 2, proc.stderr)
                self.assertFalse(output.exists())
        self.assertEqual(self.server.received, [])


if __name__ == "__main__":
    unittest.main()
