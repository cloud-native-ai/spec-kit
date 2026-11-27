"""Positive/negative cases for scripts/check-readback-contract.py.

Per-engine native-readback.py files are supplied by the engine workers; this
common probe owns only the interface. The tests therefore use mock
implementations placed under a types/<engine>/scripts/ path and assert that the
probe (a) accepts a conforming mock, (b) refuses an overwriting mock, a mock
that accepts unknown flags and a mock that misstates the source hash, and
(c) reports an unexecuted run as not_evaluated instead of a pass.

Run through the repository runner:
    bash scripts/bash/run-tests.sh skills/external/draw-diagram/tests/test_readback_contract.py -q
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
PROBE = SKILL_ROOT / "scripts" / "check-readback-contract.py"

MOCK_TEMPLATE = '''\
#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path

ENGINE = {engine!r}


def main(argv=None):
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--version", action="version", version="native-readback-mock 1.0.0")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--semantics", type=Path, required=True)
    parser.add_argument("--svg", type=Path, default=None)
    parser.add_argument("--output", type=Path, required=True)
    args = {parse}
    {overwrite_guard}
    data = args.source.read_bytes()
    json.loads(args.semantics.read_text(encoding="utf-8"))
    rows = [line for line in data.decode("utf-8").splitlines() if line.strip()]
    digest = hashlib.sha256(data).hexdigest()
    {digest_override}
    report = {{
        "engine": ENGINE,
        "source": {{"path": str(args.source), "sha256": digest}},
        "actual": {{"elements": [{{"id": row.split("|")[0]}} for row in rows], "zones": [], "relations": []}},
        "semantic": {{"status": "pass", "diff": {{}}}},
        "visual": {{"status": "not_evaluated", "checks": [], "issues": [], "limitations": ["mock"]}},
        "overall": "pass",
        "unsupported": [],
        "not_evaluated": ["visual"],
    }}
    args.output.write_text(json.dumps(report), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def write_mock(root: Path, behavior: str) -> Path:
    engine = "mockengine"
    script = root / "types" / engine / "scripts" / "native-readback.py"
    script.parent.mkdir(parents=True)
    parse = "parser.parse_known_args(argv)" if behavior == "accept_unknown" else "parser.parse_args(argv)"
    overwrite_guard = (
        "if args.output.exists() or args.output.is_symlink():\n"
        "        print('refusing to overwrite', file=sys.stderr)\n"
        "        return 2"
        if behavior != "overwrite"
        else "pass"
    )
    digest_override = 'digest = "0" * 64' if behavior == "wrong_hash" else ""
    script.write_text(
        textwrap.dedent(MOCK_TEMPLATE.format(
            engine=engine,
            parse=parse,
            overwrite_guard=overwrite_guard,
            digest_override=digest_override,
        )),
        encoding="utf-8",
    )
    return script


class ReadbackContractCases(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.workdir = self.root / "work"
        self.workdir.mkdir()
        self.source = self.root / "diagram.native"
        self.source.write_text("alpha|beta\nbeta|gamma\n", encoding="utf-8")
        self.semantics = self.root / "semantics.json"
        self.semantics.write_text(json.dumps({"elements": ["alpha", "beta", "gamma"]}), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def probe(self, script, *extra, fixtures=True):
        argv = [sys.executable, str(PROBE), "--script", str(script), "--workdir", str(self.workdir), "--json"]
        if fixtures:
            argv += ["--source", str(self.source), "--semantics", str(self.semantics)]
        argv += list(extra)
        return subprocess.run(argv, capture_output=True, text=True, timeout=120)

    def checks(self, proc):
        return {item["id"]: item["status"] for item in json.loads(proc.stdout)["checks"]}

    def test_conforming_mock_passes(self):
        script = write_mock(self.root, "good")
        proc = self.probe(script)
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        verdict = json.loads(proc.stdout)
        self.assertEqual(verdict["status"], "pass")
        self.assertTrue(all(item["status"] == "pass" for item in verdict["checks"]))

    def test_missing_fixtures_are_not_evaluated(self):
        script = write_mock(self.root, "good")
        proc = self.probe(script, fixtures=False)
        self.assertEqual(proc.returncode, 3, proc.stderr or proc.stdout)
        statuses = self.checks(proc)
        self.assertEqual(statuses["success-path"], "not_evaluated")
        self.assertEqual(statuses["unknown-option"], "not_evaluated")
        self.assertEqual(statuses["overwrite-refusal"], "not_evaluated")

    def test_overwriting_mock_is_refused(self):
        script = write_mock(self.root, "overwrite")
        proc = self.probe(script)
        self.assertEqual(proc.returncode, 1, proc.stderr or proc.stdout)
        self.assertEqual(self.checks(proc)["overwrite-refusal"], "fail")

    def test_mock_accepting_unknown_flags_is_refused(self):
        script = write_mock(self.root, "accept_unknown")
        proc = self.probe(script)
        self.assertEqual(proc.returncode, 1, proc.stderr or proc.stdout)
        self.assertEqual(self.checks(proc)["unknown-option"], "fail")

    def test_misreported_source_hash_is_refused(self):
        script = write_mock(self.root, "wrong_hash")
        proc = self.probe(script)
        self.assertEqual(proc.returncode, 1, proc.stderr or proc.stdout)
        self.assertEqual(self.checks(proc)["report-shape"], "fail")

    def test_dirty_workdir_is_refused_without_deleting_anything(self):
        script = write_mock(self.root, "good")
        existing = self.workdir / "native-readback-report.json"
        existing.write_text("keep", encoding="utf-8")
        proc = self.probe(script)
        self.assertEqual(proc.returncode, 1, proc.stderr or proc.stdout)
        self.assertEqual(self.checks(proc)["success-path"], "fail")
        self.assertEqual(existing.read_text(encoding="utf-8"), "keep")

    def test_probe_argument_errors(self):
        script = write_mock(self.root, "good")
        missing_half = subprocess.run(
            [sys.executable, str(PROBE), "--script", str(script), "--workdir", str(self.workdir), "--source", str(self.source)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(missing_half.returncode, 2, missing_half.stderr)
        bad_timeout = subprocess.run(
            [sys.executable, str(PROBE), "--script", str(script), "--workdir", str(self.workdir), "--timeout", "1"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(bad_timeout.returncode, 2, bad_timeout.stderr)
        unknown = subprocess.run(
            [sys.executable, str(PROBE), "--definitely-not-a-real-option"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(unknown.returncode, 2, unknown.stderr)


if __name__ == "__main__":
    unittest.main()
