"""Boundary guard contract tests for the 068 exec-quant feedback channel (US4).

Owns ``.specify/specs/068-exec-quant-feedback-channel/contracts/compatibility-security.md``
C-24 (zero auto-transmission: manual package / local unpack / explicit
aggregate — all pure local, zero network import or call face, zero daemon /
persistent connection / timer, and the manual package leg is the only
artifact carrying quant records) and C-25 (zero credential occurrences in the
package product, the aggregated layer and the summary products, with the 059
collection-side masking and size caps left un-weakened).

Regression-net form (tasks.md Phase 5 header note): the guarded behavior is
the three legs' landed implementation. These tests are NOT red-first; a red
here is attributed first (subject regression vs assertion defect, SKILL
§ TDD) before any fix — never silently dropped.

Subjects = the framework sources ``scripts/python/feedback-utils.py`` and
``scripts/python/exec-quant.py`` (loaded via ``tests/script_api.py``, never
the ``.specify/`` mirrors). The credential chain runs the REAL 059 collector
once (host-CLI impersonation wrapper, same technique as
``test_exec_quant_engine.py``) with a credential-shaped endpoint env, then
ships the stored record through package → ingest-exec-quant → aggregate.

Run evidence: notes/red-first-evidence.md (§ part 5, T022).
"""
from __future__ import annotations

import ast
import builtins
import contextlib
import io
import json
import os
import socket
import subprocess
import sys
import threading
import zipfile
from pathlib import Path

import pytest

from tests.script_api import _load_module, feedback_utils as fu

pytestmark = pytest.mark.contract

_HERE = Path(__file__).resolve()
REPO_ROOT = _HERE.parents[2]
FU_ENGINE = REPO_ROOT / "scripts" / "python" / "feedback-utils.py"
EQ_ENGINE = REPO_ROOT / "scripts" / "python" / "exec-quant.py"

EQ = _load_module("exec_quant_boundary_contract", "exec-quant.py")

STR001 = "speckit.exec-quant"  # [[STR-001]] (requirements § Shared Strings)

#: The planted credential shape: planted on the impersonated host's environ,
#: masked to origin-only by the 059 collector before anything is stored.
CRED_USERINFO = "user:pw"

# --------------------------------------------------------------------------- #
# C-24: static zero-network audit of both engine sources
# --------------------------------------------------------------------------- #
NETWORK_IMPORT_BLOCKLIST = frozenset({
    "socket", "ssl", "http.client", "http.server", "urllib.request",
    "urllib.error", "urllib.response", "urllib.robotparser", "requests",
    "httpx", "aiohttp", "ftplib", "smtplib", "telnetlib", "xmlrpc.client",
    "xmlrpc.server", "websockets", "curl_cffi", "asyncio",
})
#: pure string parsing, no I/O — the only urllib face the engines may carry
ALLOWED_IMPORT_MODULES = frozenset({"urllib.parse"})
NETWORK_BINARIES = frozenset({
    "curl", "wget", "nc", "netcat", "ssh", "scp", "sftp", "rsync",
    "ftp", "telnet", "http", "https",
})
SUBPROCESS_CALLS = {"run", "Popen", "call", "check_call", "check_output"}


def _imported_modules(source: str) -> set[str]:
    tree = ast.parse(source)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                names.add(node.module)
    return names


def _subprocess_command_tokens(source: str) -> set[str]:
    """Every string constant handed to a subprocess.* call (the observable
    command face of the engines)."""
    tree = ast.parse(source)
    tokens = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute)
                and isinstance(func.value, ast.Name)
                and func.value.id == "subprocess"
                and func.attr in SUBPROCESS_CALLS):
            continue
        for arg in node.args:
            for const in ast.walk(arg):
                if isinstance(const, ast.Constant) and isinstance(const.value, str):
                    tokens.add(const.value)
    return tokens


def test_engine_sources_have_zero_network_import_or_call_face():
    for engine in (FU_ENGINE, EQ_ENGINE):
        source = engine.read_text(encoding="utf-8")
        offenders = sorted(_imported_modules(source) & NETWORK_IMPORT_BLOCKLIST)
        assert not offenders, (
            f"{engine.name} imports a network-capable module: {offenders}")
        outbound = sorted(_subprocess_command_tokens(source) & NETWORK_BINARIES)
        assert not outbound, (
            f"{engine.name} shells out to a network tool: {outbound}")


def test_local_process_faces_are_the_only_subprocess_constants():
    # the subprocess face is confined to local read-only observation
    # (`ss -tnp`, host-CLI --version probes); no network tool may enter it
    for engine in (FU_ENGINE, EQ_ENGINE):
        tokens = _subprocess_command_tokens(engine.read_text(encoding="utf-8"))
        assert not tokens & NETWORK_BINARIES, engine.name


def test_host_cli_pattern_names_are_not_network_tools():
    # probe_version() execs whatever the host chain names — the declared
    # pattern list must never name a network tool
    assert not (set(EQ.HOST_CLI_PATTERNS) & NETWORK_BINARIES)


def test_network_audit_would_flag_a_violation():
    # a green check is a claim: the same scanners must go red on a real
    # offender, otherwise the zero-network pass proves nothing
    assert "socket" in (_imported_modules("import socket\n")
                        & NETWORK_IMPORT_BLOCKLIST)
    assert "curl" in (_subprocess_command_tokens(
        'subprocess.run(["curl", "-d", "@x", "https://example.com"])\n')
        & NETWORK_BINARIES)


# --------------------------------------------------------------------------- #
# C-24: runtime observation — the three legs make no network / timer /
# prompt / thread surface and write nothing outside their declared stores
# --------------------------------------------------------------------------- #
def _forbid_surface(*_args, **_kwargs):
    raise AssertionError("network/timer/prompt surface used by a channel leg")


def _tree(root: Path) -> set[str]:
    return {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()}


def _make_workspace(ws: Path) -> Path:
    (ws / ".specify").mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fu.main(["--action", "record", "--workspace-root", str(ws),
                      "--unit-id", "/speckit.plan", "--unit-type", "command",
                      "--run-id", "run-boundary",
                      "--review", "channel boundary review", "--points", "ok"])
    assert rc == 0
    rdir = ws / ".specify" / "memory" / "exec-quant" / "records"
    rdir.mkdir(parents=True, exist_ok=True)
    record = {"kind": STR001, "schema_version": 2, "unit_id": "/speckit.plan",
              "unit_type": "command", "run_id": "run-boundary",
              "collected_at": "2026-01-01T00:00:00Z"}
    (rdir / "2026-a.json").write_text(json.dumps(record) + "\n", encoding="utf-8")
    legacy = ws / ".specify" / "memory" / "exec-quant" / "records.jsonl"
    legacy.write_text(json.dumps(dict(record, run_id="run-legacy")) + "\n",
                      encoding="utf-8")
    return ws


def test_three_legs_run_with_zero_network_timer_prompt_or_thread_surface(
        tmp_path, capsys, monkeypatch):
    # runtime observation: any socket dial, timer arm, blocking prompt or new
    # thread during package / ingest-exec-quant / aggregate fails the leg
    monkeypatch.setattr(socket, "socket", _forbid_surface)
    monkeypatch.setattr(socket, "create_connection", _forbid_surface)
    monkeypatch.setattr(socket, "getaddrinfo", _forbid_surface)
    monkeypatch.setattr(threading, "Timer", _forbid_surface)
    monkeypatch.setattr(builtins, "input", _forbid_surface)

    ws1 = _make_workspace(tmp_path / "source-ws")
    ws2 = tmp_path / "target-ws"
    (ws2 / ".specify").mkdir(parents=True)
    threads_before = sorted(t.name for t in threading.enumerate())
    tree_before = _tree(tmp_path)

    # leg 1 — package (user-manual trigger, local)
    capsys.readouterr()
    rc = fu.main(["--action", "package", "--workspace-root", str(ws1),
                  "--format", "json"])
    assert rc == 0
    packaged = json.loads(capsys.readouterr().out)
    assert packaged["zip"], "fixture must produce a payload-bearing package"
    assert packaged["exec_quant_payload"]["record_count"] == 2

    # leg 2 — ingest-exec-quant (local unpack of an already-delivered package)
    capsys.readouterr()
    rc = fu.main(["--action", "ingest-exec-quant",
                  "--package", str(ws1 / packaged["zip"]),
                  "--workspace-root", str(ws2), "--format", "json"])
    assert rc == 0
    ingested = json.loads(capsys.readouterr().out)
    assert ingested["ingested"] == 2

    # leg 3 — aggregate (user-explicit action, local)
    capsys.readouterr()
    rc = EQ.main(["--action", "aggregate", "--workspace-root", str(ws2),
                  "--format", "json"])
    assert rc == 0
    view = json.loads(capsys.readouterr().out)
    assert view["totals"]["record_count"] == ingested["ingested"]

    # zero daemon / persistent connection / timer: no thread came or went
    assert sorted(t.name for t in threading.enumerate()) == threads_before

    # zero egress path: everything written stays inside the two declared
    # stores (the feedback store's packages/ for the zip, aggregated/ for the
    # received layer)
    new_paths = sorted(_tree(tmp_path) - tree_before)
    allowed = ("source-ws/.specify/memory/feedback/packages/",
               "target-ws/.specify/memory/exec-quant/aggregated/")
    outside = [p for p in new_paths if not p.startswith(allowed)]
    assert not outside, f"channel legs wrote outside their stores: {outside}"


def test_manual_package_leg_is_the_only_artifact_carrying_payload(
        tmp_path, capsys):
    # C-24 subclause split: the 059 revision is scoped to the MANUAL package
    # leg only; the pre-068 submission archive keeps its structural exclusion
    # of quant records ("排除于一切上送路径" subclause preserved verbatim).
    ws = _make_workspace(tmp_path / "ws")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fu.main(["--action", "mark-submitted", "--workspace-root", str(ws),
                      "--format", "json"])
    assert rc == 0
    result = json.loads(buf.getvalue())
    with zipfile.ZipFile(ws / result["zip"]) as zf:
        names = zf.namelist()
    assert not any(name.startswith("exec-quant/") for name in names)


# --------------------------------------------------------------------------- #
# C-25: the credential chain — one real collector run through all three legs
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def masked_chain(tmp_path_factory):
    """One real 059 collector run (credential-shaped endpoint env) shipped
    through package → ingest-exec-quant → aggregate; all three products kept
    for the per-surface credential scans (C-25 / SC-005)."""
    if not Path("/proc").is_dir():
        pytest.skip("host-CLI impersonation needs /proc (Linux)")
    root = tmp_path_factory.mktemp("masked-chain")
    ws1 = root / "source-ws"
    (ws1 / ".specify").mkdir(parents=True)
    home = root / "home"
    home.mkdir()
    runner = root / "host_runner.py"
    engine_argv = [sys.executable, str(EQ_ENGINE), "--action", "collect",
                   "--unit-id", "/speckit.plan", "--workspace-root", str(ws1)]
    runner.write_text(
        "import json, subprocess, sys\n"
        f"argv = {json.dumps([str(a) for a in engine_argv])}\n"
        "proc = subprocess.run(argv, capture_output=True, text=True)\n"
        "sys.stdout.write(proc.stdout)\nsys.stderr.write(proc.stderr)\n"
        "sys.exit(proc.returncode)\n", encoding="utf-8")
    env = dict(os.environ)
    env["HOME"] = str(home)
    env["ANTHROPIC_BASE_URL"] = f"https://{CRED_USERINFO}@api.example.com/v1"
    proc = subprocess.run(
        ["bash", "-c", f'exec -a qodercli "{sys.executable}" "{runner}"'],
        capture_output=True, text=True, timeout=240, env=env)
    assert proc.returncode == 0, f"collect failed: {proc.stderr}"

    records = sorted((ws1 / ".specify" / "memory" / "exec-quant" / "records"
                      ).glob("*.json"))
    assert len(records) == 1, "fixture expected exactly one collected record"
    record = json.loads(records[0].read_text(encoding="utf-8"))
    # 059 masking held at collection time (D6 origin-only)
    endpoints = record["llm"]["endpoint_candidates"]
    assert endpoints["ANTHROPIC_BASE_URL"] == "https://api.example.com"
    assert CRED_USERINFO not in json.dumps(record)

    # leg 1 — manual package (a benign entry rides along)
    with contextlib.redirect_stdout(io.StringIO()):  # record prints entry+hints
        rc = fu.main(["--action", "record", "--workspace-root", str(ws1),
                      "--unit-id", "/speckit.plan", "--unit-type", "command",
                      "--run-id", "run-chain",
                      "--review", "chain boundary review", "--points", "ok"])
    assert rc == 0
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fu.main(["--action", "package", "--workspace-root", str(ws1),
                      "--format", "json"])
    assert rc == 0
    packaged = json.loads(buf.getvalue())
    zip_path = ws1 / packaged["zip"]
    assert packaged["exec_quant_payload"]["record_count"] == 1

    # leg 2 — local unpack in a second workspace
    ws2 = root / "target-ws"
    (ws2 / ".specify").mkdir(parents=True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fu.main(["--action", "ingest-exec-quant", "--package", str(zip_path),
                      "--workspace-root", str(ws2), "--format", "json"])
    assert rc == 0
    assert json.loads(buf.getvalue())["ingested"] == 1

    # leg 3 — explicit aggregate
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = EQ.main(["--action", "aggregate", "--workspace-root", str(ws2),
                      "--format", "json"])
    assert rc == 0

    aggregated = ws2 / ".specify" / "memory" / "exec-quant" / "aggregated"
    envelopes = sorted(aggregated.glob("*/records/*.json"))
    summaries = sorted((aggregated / "summaries").glob("*.json"))
    assert envelopes and summaries
    return {"ws1": ws1, "ws2": ws2, "zip": zip_path, "record": record,
            "envelopes": envelopes, "summaries": summaries,
            "aggregated": aggregated}


def _credential_hits(text: str) -> list[str]:
    """Scan with the engine's own D9 mask shapes — the authority on what
    counts as a credential-shaped value."""
    return [name for name, pattern in EQ.CREDENTIAL_PATTERNS
            if pattern.search(text)]


def _zip_texts(zip_path: Path) -> list[tuple[str, str]]:
    with zipfile.ZipFile(zip_path) as zf:
        return [(name, zf.read(name).decode("utf-8", errors="replace"))
                for name in zf.namelist()]


def _dir_texts(directory: Path) -> list[tuple[str, str]]:
    return [(str(p.relative_to(directory)),
             p.read_text(encoding="utf-8", errors="replace"))
            for p in sorted(directory.rglob("*")) if p.is_file()]


def test_package_product_zero_credential_hits(masked_chain):
    surfaces = _zip_texts(masked_chain["zip"])
    assert surfaces
    offenders = {name: hits for name, text in surfaces
                 if (hits := _credential_hits(text))}
    assert not offenders, f"credential-shaped hits in the package zip: {offenders}"
    flat = "\n".join(text for _, text in surfaces)
    assert CRED_USERINFO not in flat  # the planted shape never leaked


def test_aggregated_layer_zero_credential_hits(masked_chain):
    layer = [item for item in _dir_texts(masked_chain["aggregated"])
             if not item[0].startswith("summaries/")]
    assert layer
    offenders = {name: hits for name, text in layer
                 if (hits := _credential_hits(text))}
    assert not offenders, f"credential-shaped hits in aggregated/: {offenders}"


def test_summary_products_zero_credential_hits(masked_chain):
    products = [item for item in _dir_texts(masked_chain["aggregated"])
                if item[0].startswith("summaries/")]
    assert products
    offenders = {name: hits for name, text in products
                 if (hits := _credential_hits(text))}
    assert not offenders, f"credential-shaped hits in summaries/: {offenders}"


def test_payload_carries_only_masked_data(masked_chain):
    # the masked endpoint value survives the whole chain byte-verbatim —
    # the legs neither re-expose nor enrich it (FR-015: 载荷只携带已遮载数据)
    with zipfile.ZipFile(masked_chain["zip"]) as zf:
        members = [n for n in zf.namelist() if n.startswith("exec-quant/records/")]
        assert len(members) == 1
        carried = json.loads(zf.read(members[0]))
    assert carried == masked_chain["record"]
    endpoint = carried["llm"]["endpoint_candidates"]["ANTHROPIC_BASE_URL"]
    assert endpoint == "https://api.example.com"  # origin-only: host, no path
    envelope = json.loads(masked_chain["envelopes"][0].read_text(encoding="utf-8"))
    assert envelope["record"] == masked_chain["record"]


# --------------------------------------------------------------------------- #
# C-25: 059 masking and caps are not weakened by 068
# --------------------------------------------------------------------------- #
def test_059_cap_and_mask_constants_unchanged():
    # drift pins: any change to the 059 collection protections must land as a
    # conscious edit here, never as a silent constant rewrite
    assert EQ.RECORD_SIZE_CAP_BYTES == 65536  # data-model V5 single-record cap
    assert fu.MAX_PAYLOAD_RECORDS == 1000
    assert fu.MAX_PAYLOAD_BYTES == 16777216
    assert [name for name, _pattern in EQ.CREDENTIAL_PATTERNS] == [
        "sk_style_key", "aws_access_key", "bearer_token", "slack_token",
        "github_token", "google_api_key", "url_userinfo", "kv_assignment"]
    assert tuple(EQ.ENDPOINT_ENV_NAMES) == (
        "ANTHROPIC_BASE_URL", "ANTHROPIC_URL", "OPENAI_BASE_URL", "OPENAI_URL",
        "ALIYUN_ANTHROPIC_COMPATIBLE_URL", "ALIYUN_OPENAI_COMPATIBLE_URL",
        "DASHSCOPE_API_URL", "CLAUDE_ALIBABA_BASE_URL",
        "CLAUDE_OFFICIAL_BASE_URL")
