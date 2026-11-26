#!/usr/bin/env python3
"""check-readback-contract.py — reusable CLI conformance probe for native-readback.py.

Each engine layer supplies references/types/<engine>/scripts/native-readback.py
with this interface:

  --source <native-file> --semantics <authoritative-json> [--svg <rendered-svg>]
  --output <new-report>

and --help / --version without side effects. Unknown options exit 2. An existing
--output is refused, never overwritten. This probe checks exactly that interface
and the minimum report shape; it does NOT judge the semantics of a real engine.

Checks:
  * --help and --version exit 0 with output
  * with fixtures present, an unknown option plus all required arguments exits 2
    and writes nothing (without fixtures this check is not_evaluated: a bare
    exit 2 could also mean a missing argument)
  * a run without required arguments exits 2
  * when caller-provided fixtures are given: one real run exits 0 (pass) or 3
    (partial) and writes a JSON object with the minimum keys, names the real
    source hash, and a second run against the same --output is refused with the
    first file unchanged
  * without fixtures the run-dependent checks are reported not_evaluated and the
    probe exits 3 — an unexecuted check is never reported as a pass

The probe creates only its named report file inside --workdir; it never deletes
or rewrites caller files. Inspect the target script before probing it: it is
executed with the current interpreter.

Exit codes: 0 every check passed; 1 at least one violation; 2 usage or I/O
error; 3 no violation but one or more checks not_evaluated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

VERSION = "1.0.0"
REPORT_NAME = "native-readback-report.json"
STATUSES = ("pass", "partial", "fail", "unsupported", "not_evaluated")
SEMANTIC_STATUSES = ("pass", "partial", "fail", "unsupported", "not_evaluated")


class ProbeError(ValueError):
    pass


def text(value):
    return isinstance(value, str) and value.strip() != ""


def require(condition, message):
    if not condition:
        raise ProbeError(message)


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(script, argv, timeout):
    started = time.monotonic()
    try:
        proc = subprocess.run(
            [sys.executable, str(script), *argv],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        timed_out = False
        exit_code = proc.returncode
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        exit_code = None
        stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
    return {
        "argv": argv,
        "exit": exit_code,
        "timed_out": timed_out,
        "duration_ms": int((time.monotonic() - started) * 1000),
        "stdout": stdout[:2000],
        "stderr": stderr[:2000],
    }


def record(checks, ident, status, outcome, detail):
    checks.append({"id": ident, "status": status, "exit": outcome.get("exit"), "detail": detail})


def check_report(report_path, source_path, engine_from_path):
    problems = []
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"report is not readable JSON: {exc}"]
    if not isinstance(report, dict):
        return ["report must be a JSON object"]
    required = {
        "engine": str,
        "source": dict,
        "actual": (dict, list),
        "semantic": dict,
        "visual": dict,
        "overall": str,
        "unsupported": list,
        "not_evaluated": list,
    }
    for key, kind in required.items():
        if key not in report:
            problems.append(f"missing required key: {key}")
        elif not isinstance(report[key], kind):
            problems.append(f"{key}: expected {kind}")
    engine = report.get("engine")
    if text(engine) and engine_from_path and engine != engine_from_path:
        problems.append(f"engine {engine!r} does not match the types/<engine> path ({engine_from_path!r})")
    if not text(engine):
        problems.append("engine must be a non-empty string")
    source = report.get("source")
    if isinstance(source, dict):
        if not text(source.get("path")):
            problems.append("source.path must be a non-empty string")
        if source.get("sha256") != sha256_file(source_path):
            problems.append("source.sha256 does not match the actual --source file")
    semantic = report.get("semantic")
    if isinstance(semantic, dict) and semantic.get("status") not in SEMANTIC_STATUSES:
        problems.append(f"semantic.status {semantic.get('status')!r} not in {SEMANTIC_STATUSES}")
    if report.get("overall") not in STATUSES:
        problems.append(f"overall {report.get('overall')!r} not in {STATUSES}")
    return problems


def engine_from_types_path(script):
    parts = Path(script).resolve().parts
    for index in range(len(parts) - 3):
        if parts[index] == "types" and parts[index + 2] == "scripts":
            return parts[index + 1]
    return None


def probe(args):
    checks = []
    fixtures = args.source is not None and args.semantics is not None
    help_run = run(args.script, ["--help"], args.timeout)
    if help_run["timed_out"] or help_run["exit"] != 0 or not help_run["stdout"].strip():
        record(checks, "help", "fail", help_run, "--help must exit 0 and print usage")
    else:
        record(checks, "help", "pass", help_run, "--help exited 0")
    version_run = run(args.script, ["--version"], args.timeout)
    if version_run["timed_out"] or version_run["exit"] != 0 or not version_run["stdout"].strip():
        record(checks, "version", "fail", version_run, "--version must exit 0 and print a version")
    else:
        record(checks, "version", "pass", version_run, "--version exited 0")
    if fixtures:
        unknown_output = args.workdir / "native-readback-unknown-flag-report.json"
        if unknown_output.exists() or unknown_output.is_symlink():
            record(checks, "unknown-option", "fail", {}, f"workdir is not clean: {unknown_output} already exists")
        else:
            unknown_run = run(
                args.script,
                [
                    "--definitely-not-a-readback-option",
                    "--source", str(args.source),
                    "--semantics", str(args.semantics),
                    "--output", str(unknown_output),
                ],
                args.timeout,
            )
            if unknown_run["timed_out"] or unknown_run["exit"] != 2 or unknown_output.exists():
                record(checks, "unknown-option", "fail", unknown_run,
                       "an unknown option must exit 2 with required arguments present and write nothing")
            else:
                record(checks, "unknown-option", "pass", unknown_run, "unknown option exited 2 and wrote nothing")
    else:
        record(checks, "unknown-option", "not_evaluated", {},
               "needs --source/--semantics to distinguish an unknown-option rejection from a missing-argument rejection")
    missing_run = run(args.script, [], args.timeout)
    if missing_run["timed_out"] or missing_run["exit"] != 2:
        record(checks, "missing-required", "fail", missing_run, "missing required arguments must exit 2")
    else:
        record(checks, "missing-required", "pass", missing_run, "missing arguments exited 2")

    if not fixtures:
        record(checks, "success-path", "not_evaluated", {}, "no --source/--semantics fixtures supplied")
        record(checks, "report-shape", "not_evaluated", {}, "no fixtures supplied")
        record(checks, "overwrite-refusal", "not_evaluated", {}, "no fixtures supplied")
        return checks
    report_path = args.workdir / REPORT_NAME
    if report_path.exists() or report_path.is_symlink():
        record(checks, "success-path", "fail", {}, f"workdir is not clean: {report_path} already exists")
        record(checks, "report-shape", "not_evaluated", {}, "success run refused to start")
        record(checks, "overwrite-refusal", "not_evaluated", {}, "success run refused to start")
        return checks
    argv = ["--source", str(args.source), "--semantics", str(args.semantics), "--output", str(report_path)]
    if args.svg is not None:
        argv[4:4] = ["--svg", str(args.svg)]
    first = run(args.script, argv, args.timeout)
    if first["timed_out"] or first["exit"] not in (0, 3) or not report_path.is_file():
        record(checks, "success-path", "fail", first,
               "the documented invocation must exit 0 (pass) or 3 (partial) and write --output; "
               "this probe checks the interface, not whether the diagram is good")
        record(checks, "report-shape", "not_evaluated", {}, "no report was written")
        record(checks, "overwrite-refusal", "not_evaluated", {}, "no report was written")
        return checks
    engine_verdict = json.loads(report_path.read_text(encoding="utf-8")).get("overall")
    record(checks, "success-path", "pass", first,
           f"documented invocation exited {first['exit']} and wrote the report "
           f"(engine verdict: {engine_verdict!r}; an interface probe does not pass or fail the diagram)")
    problems = check_report(report_path, args.source, engine_from_types_path(args.script))
    if problems:
        record(checks, "report-shape", "fail", {}, "; ".join(problems))
    else:
        record(checks, "report-shape", "pass", {}, "minimum report shape and source hash are truthful")
    before = hashlib.sha256(report_path.read_bytes()).hexdigest()
    second = run(args.script, argv, args.timeout)
    after = hashlib.sha256(report_path.read_bytes()).hexdigest() if report_path.is_file() else ""
    if second["timed_out"] or second["exit"] == 0:
        record(checks, "overwrite-refusal", "fail", second, "a second run against the same --output must fail")
    elif before != after:
        record(checks, "overwrite-refusal", "fail", second, "the existing report changed despite the refusal")
    else:
        record(checks, "overwrite-refusal", "pass", second, "second run refused and left the report unchanged")
    return checks


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Conformance probe for references/types/<engine>/scripts/native-readback.py: CLI shape, "
        "minimum report shape, truthful source hash and no-overwrite refusal. Fixtures are caller-supplied; "
        "without them the run-dependent checks are not_evaluated (exit 3).",
        allow_abbrev=False,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--script", type=Path, required=True, help="native-readback.py to probe")
    parser.add_argument("--workdir", type=Path, required=True, help="existing directory for the probe report")
    parser.add_argument("--source", type=Path, default=None, help="known-good native source fixture")
    parser.add_argument("--semantics", type=Path, default=None, help="authoritative semantics fixture")
    parser.add_argument("--svg", type=Path, default=None, help="optional rendered SVG fixture")
    parser.add_argument("--timeout", type=int, default=120, help="per-invocation timeout, 5..600 s (default 120)")
    parser.add_argument("--json", action="store_true", help="print the machine verdict as JSON")
    args = parser.parse_args(argv)
    try:
        require(not (args.source is None) ^ (args.semantics is None),
                "--source and --semantics must be supplied together")
        require(args.svg is None or args.source is not None, "--svg requires --source/--semantics")
        require(5 <= args.timeout <= 600, "--timeout must be within 5..600 seconds")
        require(args.script.is_file(), f"script not found: {args.script}")
        require(args.workdir.is_dir(), f"workdir is not a directory: {args.workdir}")
        for label, path in (("--source", args.source), ("--semantics", args.semantics), ("--svg", args.svg)):
            if path is not None:
                require(path.is_file(), f"{label} fixture not found: {path}")
    except ProbeError as exc:
        print(f"usage error: {exc}", file=sys.stderr)
        return 2
    checks = probe(args)
    statuses = {item["status"] for item in checks}
    if "fail" in statuses:
        status = "fail"
        code = 1
    elif "not_evaluated" in statuses:
        status = "not_evaluated"
        code = 3
    else:
        status = "pass"
        code = 0
    verdict = {"script": str(args.script), "workdir": str(args.workdir), "status": status, "checks": checks}
    if args.json:
        print(json.dumps(verdict, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"readback contract: {args.script}")
        for item in checks:
            print(f"  [{item['status']}] {item['id']}: {item['detail']}")
        print(f"verdict: {status}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
