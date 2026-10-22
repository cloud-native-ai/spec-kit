"""End-to-end integration test for the exec-quant feedback channel
(Feature 068, US3 — the aggregate chain).

Chain under test (the US3 leg is red-first; the package/ingest legs are the
already-landed US1/US2 behavior and act as the regression net riding the
chain, per the create-tasks migration/regression exception — this row carries
an explicit ``[blockedBy: T013]``):

    self-built customer store (dual-form + mixed field shapes)
      → package (real ``--action package``)
      → manual delivery (file copy into the hub's feedback/ intake dir)
      → ingest-exec-quant (real ``--action ingest-exec-quant``)
      → aggregate (explicit exec-quant engine action)

covered: ≥2 source projects with one group landing in the literal
``unknown-project`` group; same-package re-ingest leaves zero aggregate-layer
delta and rerunning aggregate reproduces identical numbers in a NEW product;
digit-by-digit reconciliation of every view number against the
``record_files`` roster; credential-shape scan over the aggregated layer and
the summary products with zero hits; zero-network execution of the whole
chain (sockets blocked in-process); a payload-free isomorphic package moves
the chain by exactly zero.

Engines are exercised through their real CLIs in-process
(``tests.script_api`` loads the framework sources ``scripts/python/…``, never
the ``.specify/`` mirrors). All fixtures are self-constructed; the real
inbound bundle ``feedback/feedback-20261022T062525Z.zip`` and the runtime
records under ``.specify/memory/`` are never touched.

Red-first evidence: notes/red-first-evidence.md (§ part 4a / T019).
"""
from __future__ import annotations

import json
import re
import shutil
import socket
import zipfile
from pathlib import Path

import pytest

from tests.script_api import _load_module, feedback_utils as fu

pytestmark = pytest.mark.integration

EQ = _load_module("exec_quant_channel_integration", "exec-quant.py")

NOT_EVALUATED = "not_evaluated"  # [[STR-002]] (requirements § Shared Strings)
RECORD_KIND = "speckit.exec-quant"  # [[STR-001]]
PAYLOAD_KIND = "speckit.exec-quant-payload"  # data-model § E4
VIEW_KIND = "speckit.exec-quant-aggregate-view"  # data-model § E7
ENTRY_NAME_FORM = re.compile(r"^\d{8}T\d{6}\d{6}Z-[0-9a-f]{8}\.json$")

#: Credential-shaped NAME patterns (C-24/FR-015, scan criterion CHK030):
#: variable/key names that carry secrets. The measurement field ``tokens``
#: is deliberately NOT a credential name and must not match.
CREDENTIAL_NAME_PATTERNS = (
    "api[_-]?key", "apikey", "secret", "passw(?:or)?d", "authorization",
    "bearer", "credential", "private[_-]?key", "access[_-]?key",
    "auth[_-]?token", "session[_-]?token", "api[_-]?token",
)
#: Credential-shaped VALUE forms (well-known literal secret prefixes).
CREDENTIAL_VALUE_PATTERN = (
    r"(?:sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|gho_[A-Za-z0-9]{30,}"
    r"|AKIA[0-9A-Z]{16}|xox[abp]-[0-9A-Za-z-]{20,}"
    r"|Bearer\s+[A-Za-z0-9._-]{20,})"
)


# --------------------------------------------------------------------------- #
# chain fixtures
# --------------------------------------------------------------------------- #
def _quant_record(unit_id: str, run_id: str, quality: dict,
                  collected_at: str = "2026-01-01T00:00:00Z") -> dict:
    return {"kind": RECORD_KIND, "schema_version": 2, "unit_id": unit_id,
            "unit_type": "command", "run_id": run_id,
            "collected_at": collected_at, "quality": quality}


def _customer_store(ws: Path, dir_records: list[dict],
                    legacy_records: list[dict]) -> None:
    """Dual-form exec-quant store (records/ dir + legacy records.jsonl)."""
    records = ws / ".specify" / "memory" / "exec-quant" / "records"
    records.mkdir(parents=True, exist_ok=True)
    for i, record in enumerate(dir_records):
        (records / f"20260101T0000{i:02d}Z-rec{i:04d}.json").write_text(
            json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
    if legacy_records:
        stream = ws / ".specify" / "memory" / "exec-quant" / "records.jsonl"
        with stream.open("w", encoding="utf-8") as handle:
            for record in legacy_records:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _declare_project(ws: Path, name: str) -> None:
    """C-5 identity: the **Project Name** line of .specify/instructions.md."""
    spec_dir = ws / ".specify"
    spec_dir.mkdir(parents=True, exist_ok=True)
    (spec_dir / "instructions.md").write_text(
        f"# {name}\n\n**Project Name**: {name}\n", encoding="utf-8")


def _fu(args: list[str], capsys) -> tuple[dict | None, int]:
    """Run a feedback-utils action in-process; return (json, rc)."""
    capsys.readouterr()
    rc = fu.main(args)
    out = capsys.readouterr().out
    payload = None
    if out.strip():
        try:
            payload = json.loads(out)
        except ValueError:
            payload = None
    return payload, rc


def _package(customer: Path, capsys) -> tuple[Path | None, dict]:
    """Package a customer workspace; return (zip path, package report)."""
    report, rc = _fu(["--action", "package", "--workspace-root",
                      str(customer), "--format", "json"], capsys)
    assert rc == 0, report
    assert report is not None
    zip_value = report.get("zip")
    if zip_value is None:
        return None, report
    zip_path = Path(zip_value)
    # the report names the zip relative to the customer workspace
    if not zip_path.is_absolute():
        zip_path = customer / zip_path
    assert zip_path.is_file(), zip_path
    return zip_path, report


def _deliver(hub: Path, package: Path, sender: str) -> Path:
    """Manual delivery hop: the bundle is copied into the hub's intake dir
    under a sender-prefixed name — two customers packaging within the same
    second produce identically named zips, and a real inbox never silently
    overwrites one delivery with another."""
    inbox = hub / "feedback"
    inbox.mkdir(parents=True, exist_ok=True)
    target = inbox / f"{sender}-{package.name}"
    shutil.copyfile(package, target)
    return target


def _corrupt_payload_manifest(bundle: Path) -> None:
    """Delivery-hop degradation fixture: rewrite the delivered copy with an
    unreadable payload manifest (C-12 → the literal unknown-project group)."""
    members = [(item, zipfile.ZipFile(bundle).read(item.filename))
               for item in zipfile.ZipFile(bundle).infolist()]
    with zipfile.ZipFile(bundle, "w") as zf:
        for item, body in members:
            if item.filename == "exec-quant/payload-manifest.json":
                body = b"{corrupt json"
            zf.writestr(item, body)


def _ingest(hub: Path, bundle: Path, capsys) -> dict:
    payload, rc = _fu(["--action", "ingest-exec-quant", "--package",
                       str(bundle), "--workspace-root", str(hub),
                       "--format", "json"], capsys)
    assert rc == 0, payload
    assert payload is not None
    return payload


def _aggregate(hub: Path, capsys) -> tuple[dict, int]:
    """Run the explicit aggregate action on the hub; return (view, rc)."""
    capsys.readouterr()
    try:
        rc = EQ.main(["--action", "aggregate", "--workspace-root", str(hub)])
    except SystemExit as exc:  # argparse layer (red phase: unregistered)
        rc = exc.code
    out = capsys.readouterr().out
    try:
        view = json.loads(out)
    except ValueError:
        view = None
    return view, rc


def _aggregated(hub: Path) -> Path:
    return hub / ".specify" / "memory" / "exec-quant" / "aggregated"


def _envelope_files(hub: Path) -> list[Path]:
    aggregated = _aggregated(hub)
    if not aggregated.is_dir():
        return []
    return sorted(p for p in aggregated.glob("*/records/*.json"))


def _summaries(hub: Path) -> list[Path]:
    summaries = _aggregated(hub) / "summaries"
    return sorted(summaries.glob("*.json")) if summaries.is_dir() else []


def _snapshot(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        return {}
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def _stable_face(view: dict) -> dict:
    """The rebuild-comparable face of a view (everything but generated_at)."""
    return {k: v for k, v in view.items() if k != "generated_at"}


def _replay_source(hub: Path, source: dict) -> None:
    """Replay one sources[] entry digit-by-digit from the envelopes its own
    record_files roster names (FR-011; oracle mirrors the contract test)."""
    def shape_evaluates(value: object) -> bool:
        return isinstance(value, dict) and "value" in value

    on_disk = {p.name: json.loads(p.read_text(encoding="utf-8"))
               for p in _envelope_files(hub)}
    envelopes = []
    for name in source["record_files"]:
        assert name in on_disk, f"roster name {name!r} not found on disk"
        envelopes.append(on_disk[name])
    units: dict[str, int] = {}
    per_record: list[dict] = []
    fields: set[str] = set()
    for env in envelopes:
        record = env["record"]
        units[str(record.get("unit_id", ""))] = (
            units.get(str(record.get("unit_id", "")), 0) + 1)
        quality = record.get("quality")
        quality = quality if isinstance(quality, dict) else {}
        per_record.append(quality)
        fields.update(quality)
    quality_view = {}
    for field in sorted(fields):
        evaluated = sum(1 for q in per_record if shape_evaluates(q.get(field)))
        quality_view[field] = {
            "evaluated": evaluated,
            "not_evaluated": len(per_record) - evaluated,
        }
    assert source["record_count"] == len(envelopes)
    assert source["units"] == units
    assert source["quality"] == quality_view
    assert source["coverage"] == {
        "evaluated_total": sum(f["evaluated"] for f in quality_view.values()),
        "not_evaluated_total": sum(f["not_evaluated"]
                                   for f in quality_view.values()),
    }


def _scan_credentials(root: Path) -> list[str]:
    """Credential-shape scan (CHK030 criterion): name patterns + literal
    secret-value forms over every file under root. Returns the hit list."""
    name_res = [re.compile(p, re.I) for p in CREDENTIAL_NAME_PATTERNS]
    value_re = re.compile(CREDENTIAL_VALUE_PATTERN)
    hits: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for name_re in name_res:
            if name_re.search(text):
                hits.append(f"{path.relative_to(root)}:name:{name_re.pattern}")
        if value_re.search(text):
            hits.append(f"{path.relative_to(root)}:value")
    return hits


# --------------------------------------------------------------------------- #
# the chain: stores → package → deliver → ingest (aggregate = test's own step)
# --------------------------------------------------------------------------- #
def _build_customers(tmp_path: Path) -> tuple[Path, Path]:
    """Customer alpha: identified identity + dual-form store + mixed D8
    shapes. Customer beta: basename-fallback identity (its delivered copy is
    degraded in the delivery hop, so the intake lands unknown-project)."""
    alpha = tmp_path / "customer-alpha"
    _declare_project(alpha, "customer-alpha")
    _customer_store(
        alpha,
        dir_records=[
            _quant_record(
                "/speckit.plan", "r1",
                {"elapsed_ms": {"value": 1200, "provenance": "carried"},
                 "tokens": NOT_EVALUATED}),  # satisfaction missing entirely
            _quant_record(
                "/speckit.implement", "r2",
                {"elapsed_ms": NOT_EVALUATED,
                 "tokens": {"value": 42, "provenance": "measured"}}),
        ],
        legacy_records=[
            _quant_record(
                "/speckit.review", "r3",
                {"exit_code": {"value": 0, "provenance": "carried"}}),
        ])
    beta = tmp_path / "customer-beta"
    _customer_store(
        beta,
        dir_records=[
            _quant_record("/speckit.tasks", "r9",
                          {"elapsed_ms": NOT_EVALUATED,
                           "tokens": NOT_EVALUATED}),
        ],
        legacy_records=[])
    return alpha, beta


def _run_chain(tmp_path: Path, capsys) -> dict:
    """customer stores → package → manual delivery → ingest-exec-quant on a
    fresh hub. The aggregate step stays with the tests (C-23: explicit)."""
    alpha, beta = _build_customers(tmp_path)
    hub = tmp_path / "speckit-hub"
    hub.mkdir()

    alpha_pkg, alpha_report = _package(alpha, capsys)
    assert alpha_pkg is not None
    assert alpha_report["exec_quant_payload"]["record_count"] == 3
    assert alpha_report["exec_quant_payload"]["source_form_counts"] == {
        "records-dir": 2, "legacy-jsonl": 1}
    beta_pkg, _ = _package(beta, capsys)
    assert beta_pkg is not None

    alpha_bundle = _deliver(hub, alpha_pkg, "customer-alpha")
    beta_bundle = _deliver(hub, beta_pkg, "customer-beta")
    _corrupt_payload_manifest(beta_bundle)  # degraded delivery hop fixture

    alpha_intake = _ingest(hub, alpha_bundle, capsys)
    beta_intake = _ingest(hub, beta_bundle, capsys)
    assert alpha_intake["ingested"] == 3
    assert alpha_intake["groups_touched"] == 1
    assert beta_intake["manifest_unreadable"] is True
    assert beta_intake["ingested"] == 1
    return {"hub": hub, "alpha": alpha, "beta": beta,
            "alpha_bundle": alpha_bundle, "beta_bundle": beta_bundle}


# --------------------------------------------------------------------------- #
# the full chain (US3 acceptance)
# --------------------------------------------------------------------------- #
def test_full_chain_two_sources_view_and_product(tmp_path, capsys):
    facts = _run_chain(tmp_path, capsys)
    hub = facts["hub"]

    view, rc = _aggregate(hub, capsys)

    assert rc == 0 and view is not None
    assert view["kind"] == VIEW_KIND
    projects = sorted(s["project"] for s in view["sources"])
    assert projects == ["customer-alpha", "unknown-project"]  # ≥2 源项目
    unknown = [s for s in view["sources"]
               if s["project"] == "unknown-project"][0]
    assert unknown["identity_status"] == "unknown-project"  # 字面组,零猜测
    assert unknown["record_count"] == 1
    alpha = [s for s in view["sources"]
             if s["project"] == "customer-alpha"][0]
    assert alpha["identity_status"] == "identified"
    assert alpha["record_count"] == 3  # dual form fully carried by the chain
    assert view["totals"]["record_count"] == 4
    assert view["store_digest"] == {"record_files_total": 4,
                                    "identity_keys_total": 4}
    for source in view["sources"]:
        _replay_source(hub, source)  # digit-by-digit roster reconciliation
    products = _summaries(hub)
    assert len(products) == 1
    assert ENTRY_NAME_FORM.match(products[0].name)
    assert view == json.loads(products[0].read_text(encoding="utf-8"))


def test_same_package_double_ingest_zero_delta_and_rerun_consistent(
        tmp_path, capsys):
    facts = _run_chain(tmp_path, capsys)
    hub = facts["hub"]
    alpha_bundle = facts["alpha_bundle"]
    before = {p.name: p.read_bytes() for p in _envelope_files(hub)}
    assert len(before) == 4
    first_view, rc1 = _aggregate(hub, capsys)
    assert rc1 == 0 and first_view is not None
    first_products = _summaries(hub)
    first_bytes = first_products[0].read_bytes()

    # Fixture-form fixes (both masked at red phase — the test died at the
    # unregistered-aggregate assert before reaching these lines), disclosed in
    # notes/red-first-evidence.md § 4b: `_ingest` returns one report dict
    # (every sibling call site assigns it singly), and the engine's record
    # action requires --unit-type for a /speckit. unit (063 C-23 collects all
    # missing required flags, exit 2 — sibling tests pass "command").
    intake = _ingest(hub, alpha_bundle, capsys)  # same package again
    assert intake["ingested"] == 0
    assert intake["duplicates_skipped"] == intake["record_count"] == 3
    assert {p.name: p.read_bytes() for p in _envelope_files(hub)} == before

    second_view, rc2 = _aggregate(hub, capsys)  # rerun on the same store
    assert rc2 == 0 and second_view is not None
    products = _summaries(hub)
    assert len(products) == 2
    assert products[0].read_bytes() == first_bytes  # append-only products
    assert _stable_face(first_view) == _stable_face(second_view)


def test_ingest_does_not_auto_aggregate_in_chain(tmp_path, capsys):
    # C-17/C-23 behavioral negative inside the real chain: the receive leg
    # never produces a summary; only the explicit action does.
    facts = _run_chain(tmp_path, capsys)
    hub = facts["hub"]

    assert _summaries(hub) == []  # two ingests happened — zero summaries
    _, rc = _aggregate(hub, capsys)
    assert rc == 0
    assert len(_summaries(hub)) == 1


def test_credential_scan_zero_hits_over_products_and_aggregate_layer(
        tmp_path, capsys):
    facts = _run_chain(tmp_path, capsys)
    hub = facts["hub"]
    _, rc = _aggregate(hub, capsys)
    assert rc == 0

    assert _scan_credentials(_aggregated(hub)) == []  # 层 + summaries 产物
    for bundle in sorted((hub / "feedback").glob("*.zip")):
        with zipfile.ZipFile(bundle) as zf:
            for name in zf.namelist():
                body = zf.read(name)
                for pattern in CREDENTIAL_NAME_PATTERNS:
                    assert not re.search(pattern, body.decode(
                        "utf-8", errors="replace"), re.I), (bundle, name)
                assert not re.search(CREDENTIAL_VALUE_PATTERN, body.decode(
                    "utf-8", errors="replace")), (bundle, name)


def test_chain_runs_with_sockets_blocked(tmp_path, capsys, monkeypatch):
    # FR-014/C-23: zero network for the whole chain — package, ingest and
    # aggregate all complete while every socket entry point raises.
    def _no_network(*args, **kwargs):
        raise AssertionError("network attempted during the feedback channel")

    for name in ("socket", "create_connection", "getaddrinfo"):
        monkeypatch.setattr(socket, name, _no_network)

    facts = _run_chain(tmp_path, capsys)
    view, rc = _aggregate(facts["hub"], capsys)

    assert rc == 0 and view is not None
    assert len(_summaries(facts["hub"])) == 1
    assert view["totals"]["record_count"] == 4


def test_no_payload_isomorphic_package_full_chain_zero_diff(tmp_path, capsys):
    facts = _run_chain(tmp_path, capsys)
    hub = facts["hub"]
    first_view, _ = _aggregate(hub, capsys)
    assert first_view is not None
    layer_before = _snapshot(_aggregated(hub))

    gamma = tmp_path / "customer-gamma"
    gamma.mkdir()
    _declare_project(gamma, "customer-gamma")
    _, rc_record = _fu(["--action", "record", "--workspace-root", str(gamma),
                        "--unit-id", "/speckit.plan", "--unit-type", "command",
                        "--run-id", "r-gamma",
                        "--review", "framework friction noted", "--points",
                        "one friction point", "--format", "json"], capsys)
    assert rc_record == 0
    gamma_pkg, gamma_report = _package(gamma, capsys)
    assert gamma_pkg is not None
    assert gamma_report["exec_quant_payload"]["record_count"] == 0

    intake = _ingest(hub, _deliver(hub, gamma_pkg, "customer-gamma"), capsys)
    assert intake["record_count"] == 0 and intake["ingested"] == 0
    assert _snapshot(_aggregated(hub)) == layer_before  # zero layer delta

    second_view, rc = _aggregate(hub, capsys)
    assert rc == 0 and second_view is not None
    assert _stable_face(first_view) == _stable_face(second_view)
    assert sorted(s["project"] for s in second_view["sources"]) == [
        "customer-alpha", "unknown-project"]
