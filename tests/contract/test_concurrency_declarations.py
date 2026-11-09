"""Declaration-layer contract for Feature 093 (contracts/declaration-facts.contract.md).

Rows pinned here (WP4): T016, T018, T020, T092, T094, T129.
Rows added at release (WP5): T017 (C-011), T019 (C-013).

The surface under test is the existing read entry, never a second parser:

- **C-010 / T016** — "registered" is a *read behaviour*: a slug is registered only when
  ``--action get --fact <slug>`` exits 0 with a body AND the slug appears in the ``facts``
  array of ``--action list``. The mutation renames the file or breaks its ``fact:`` key,
  never merely deletes it; a stem/``fact:`` disagreement is ``registration-invisible``
  (C-012) and MUST be reported rather than skipped.
- **C-002 / T018** — a construct outside ``block-subset/v1`` is reported with a finding
  exit (1) and a message naming the file; it is never silently dropped from the list.
- **C-018 / T020** — each of the eight facts is byte-identical between
  ``shared/declarations/facts/`` and ``.specify/shared/declarations/facts/``, and the
  mirror-only layout is readable on its own.
- **C-054/C-055/C-056 / T092** — the shared string table is a closed, singly-owned set;
  a reason code is not a class name and a class name is not a string id.
- **C-094 role separation / T094** — each string is used in its declared role, and the
  landing discipline both live under is reachable by path.
- **C-087 / T129** — each fact file carries its registration line in ``contract.yaml``
  in the same change that adds the file; a file without a line is red.
- **C-011 / T017** — an unregistered slug is ``owner-unavailable``: the reader exits 1,
  and the judgement engine translates that into its own verdict with exit 2 — no
  consumer defaults the value when the read fails.
- **C-013 / T019** — removing a fact from the read surface (broken ``fact:`` key,
  deleted file, unparsable body) makes the dependent judgement report
  ``owner-unavailable`` with a named message and a non-zero exit; it never falls back
  to a default. The mutation asserts the read behaviour, not the act of unregistering.

Every assertion here reads the live tree through ``scripts/python/declaration_reader.py``
or a copy of it inside ``tmp_path``; nothing writes into the repository.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"
ENGINE = REPO_ROOT / "scripts" / "python" / "concurrency-check.py"

EIGHT_FACTS = (
    "concurrency-class",
    "serial-reason",
    "effective-concurrency",
    "concurrency-slot-and-reserve",
    "decomposition-coverage",
    "executor-enumeration-roots",
    "concurrency-contract",
    "coordinator-dispatch-verdict",
)

SHARED_STRING_IDS = (
    "STR-001", "STR-002", "STR-003", "STR-004", "STR-005", "STR-006",
    "STR-007", "STR-008", "STR-009", "STR-010", "STR-011",
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _reader_module():
    spec = importlib.util.spec_from_file_location("declaration_reader", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _cli(*args, repo):
    return subprocess.run(
        [sys.executable, str(READER), *args, "--repo", str(repo)],
        capture_output=True, text=True,
    )


def _copy_layer(dst: Path) -> Path:
    """Copy the declaration layer into ``dst`` (source form) and return the repo root."""
    target = dst / "shared" / "declarations"
    shutil.copytree(REPO_ROOT / "shared" / "declarations", target)
    return dst


def _judge_registration(repo: Path):
    """C-010/C-012/C-087 — the registration judgement this module authors.

    A fact is registered only when (a) ``--action get`` resolves its slug, (b) the slug
    appears in ``--action list``'s ``facts`` array, (c) its file stem equals its ``fact:``
    key, and (d) ``contract.yaml`` carries a key named after the slug pointing at that
    file. Each violation is returned as ``(code, path)``; an empty list is green.
    """
    reader = _reader_module()
    contract = reader.load_contract(repo)
    findings = []
    facts_dir = Path(repo) / "shared" / "declarations" / "facts"
    for path in sorted(facts_dir.glob("*.yaml")):
        try:
            body = reader.parse_subset(
                path.read_text(encoding="utf-8"), str(path.relative_to(repo)))
        except reader.DeclarationError as error:
            findings.append(("registration-invisible", str(path.relative_to(repo)), str(error)))
            continue
        stem = path.stem
        declared = str(body.get("fact", "")).strip() if isinstance(body, dict) else ""
        rel = "shared/declarations/facts/%s.yaml" % stem
        if declared != stem:
            findings.append(("registration-invisible", rel, "fact %r != stem %r" % (declared, stem)))
        listed = False
        try:
            listed = reader.load_fact(repo, declared).get("path") == rel if declared else False
        except reader.DeclarationError:
            listed = False
        if declared and not listed:
            findings.append(("unregistered", rel, "slug %r does not resolve through --action get" % declared))
        # C-087 binds this feature's eight facts: each carries its contract.yaml line.
        # Pre-existing facts register through the facts directory alone (C-010).
        if stem in EIGHT_FACTS and contract.get(stem) != rel:
            findings.append(("unregistered", rel, "contract.yaml has no registration line for %r" % stem))
    return findings


def _facts_by_slug():
    reader = _reader_module()
    return {fact["body"]["fact"]: fact for fact in reader.load_facts(str(REPO_ROOT))}


def _statement(slug):
    return _facts_by_slug()[slug]["body"]["statement"]


# --------------------------------------------------------------------------- #
# T016 — registration is a read behaviour
# --------------------------------------------------------------------------- #
def test_eight_facts_resolve_through_get_and_list():
    """C-010 — get resolves each slug and list carries it in its facts array."""
    listing = _cli("--action", "list", repo=REPO_ROOT)
    assert listing.returncode == 0, listing.stderr
    payload = json.loads(listing.stdout)
    listed = {str(fact["body"].get("fact", "")).strip() for fact in payload["facts"]}
    for slug in EIGHT_FACTS:
        got = _cli("--action", "get", "--fact", slug, repo=REPO_ROOT)
        assert got.returncode == 0, got.stderr
        assert json.loads(got.stdout)["body"]["fact"] == slug
        assert slug in listed, "slug %r missing from --action list facts array" % slug


def test_rename_mutation_is_registration_invisible_not_deleted(tmp_path):
    """C-010/C-012 — renaming the file breaks stem==fact; the pair is reported."""
    repo = _copy_layer(tmp_path)
    source = repo / "shared" / "declarations" / "facts" / "concurrency-class.yaml"
    source.rename(source.with_name("concurrency-class-renamed.yaml"))
    # the `fact:` key still says concurrency-class, so get keeps resolving — the rename
    # did not delete the slug, which is exactly why the stem/`fact:` judgement exists.
    got = _cli("--action", "get", "--fact", "concurrency-class", repo=repo)
    assert got.returncode == 0, got.stderr
    findings = _judge_registration(repo)
    assert any(
        code == "registration-invisible" and path.endswith("concurrency-class-renamed.yaml")
        for code, path, _ in findings
    ), findings


def test_broken_fact_key_unregisters_the_slug(tmp_path):
    """C-010/C-012 — breaking the `fact:` key unregisters the slug on both read faces."""
    repo = _copy_layer(tmp_path)
    fact_file = repo / "shared" / "declarations" / "facts" / "serial-reason.yaml"
    fact_file.write_text(
        fact_file.read_text(encoding="utf-8").replace(
            "fact: serial-reason", "fact: serial-reason-broken", 1),
        encoding="utf-8")
    got = _cli("--action", "get", "--fact", "serial-reason", repo=repo)
    assert got.returncode == 1, "a broken fact: key must not resolve: %s" % got.stdout
    listing = _cli("--action", "list", repo=repo)
    payload = json.loads(listing.stdout)
    declared = {str(fact["body"].get("fact", "")).strip() for fact in payload["facts"]}
    assert "serial-reason" not in declared
    findings = _judge_registration(repo)
    assert any(code == "registration-invisible" for code, _, _ in findings), findings


def test_live_tree_registration_judgement_is_green():
    """C-010/C-012/C-087 — the live tree passes the same judgement the mutations fail."""
    assert _judge_registration(REPO_ROOT) == []


# --------------------------------------------------------------------------- #
# T018 — a malformed fact is reported, never skipped
# --------------------------------------------------------------------------- #
def test_construct_outside_the_subset_is_reported_not_dropped(tmp_path):
    """C-002 — a flow list is outside block-subset/v1; the read entry reports it."""
    repo = _copy_layer(tmp_path)
    fact_file = repo / "shared" / "declarations" / "facts" / "serial-reason.yaml"
    text = fact_file.read_text(encoding="utf-8")
    mutated = text.replace(
        "  groups:\n    - condition-bound\n    - factual\n",
        "  groups: [condition-bound, factual]\n", 1)
    assert mutated != text, "fixture premise: the groups block must be present"
    fact_file.write_text(mutated, encoding="utf-8")
    listing = _cli("--action", "list", repo=repo)
    assert listing.returncode == 1, "a subset violation must be a finding exit, not exit 0"
    assert "serial-reason.yaml" in (listing.stdout + listing.stderr)


def test_stem_disagreement_is_reported_by_the_judgement(tmp_path):
    """C-012 — stem/`fact:` disagreement is registration-invisible, not a silent skip."""
    repo = _copy_layer(tmp_path)
    fact_file = repo / "shared" / "declarations" / "facts" / "effective-concurrency.yaml"
    fact_file.write_text(
        fact_file.read_text(encoding="utf-8").replace(
            "fact: effective-concurrency", "fact: effective-concurrency-v2", 1),
        encoding="utf-8")
    findings = _judge_registration(repo)
    codes = {code for code, _, _ in findings}
    assert "registration-invisible" in codes, findings


# --------------------------------------------------------------------------- #
# T020 — source and projection are byte-identical and both readable
# --------------------------------------------------------------------------- #
def test_source_and_projection_are_byte_identical():
    """C-018 — the same fact is reachable from shared/ and .specify/shared/ identically."""
    for slug in EIGHT_FACTS:
        source = REPO_ROOT / "shared" / "declarations" / "facts" / ("%s.yaml" % slug)
        mirror = REPO_ROOT / ".specify" / "shared" / "declarations" / "facts" / ("%s.yaml" % slug)
        assert source.is_file(), "missing fact source: %s" % source
        assert mirror.is_file(), "missing fact projection: %s" % mirror
        assert source.read_bytes() == mirror.read_bytes(), (
            "mirror drift on %s: edit the source and regenerate, never the projection" % slug)


def test_mirror_only_layer_is_readable(tmp_path):
    """C-018 — the runtime projection alone answers get and list."""
    target = tmp_path / ".specify" / "shared" / "declarations"
    shutil.copytree(REPO_ROOT / "shared" / "declarations", target)
    got = _cli("--action", "get", "--fact", "serial-reason", repo=tmp_path)
    assert got.returncode == 0, got.stderr
    assert json.loads(got.stdout)["body"]["fact"] == "serial-reason"
    listing = _cli("--action", "list", repo=tmp_path)
    assert listing.returncode == 0, listing.stderr


# --------------------------------------------------------------------------- #
# T092 — shared-string ownership, closed registration, no cross-role use
# --------------------------------------------------------------------------- #
def test_shared_string_table_is_closed_and_singly_owned():
    """C-054/C-055 — one owner per string, the table registered as a closed set."""
    statement = _statement("concurrency-contract")
    rows = statement["shared_strings"]
    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids)), "a shared string id appears more than once: %s" % ids
    assert tuple(sorted(ids)) == tuple(sorted(SHARED_STRING_IDS)), ids
    for row in rows:
        owner = REPO_ROOT / row["owner"]
        assert owner.is_file(), "string %s names a missing owner: %s" % (row["id"], row["owner"])
    rule = statement["shared_strings_rule"].lower()
    assert "closed set" in rule, "the string table must be registered as a closed set: %r" % rule


def test_reason_codes_and_class_names_do_not_cross_roles():
    """C-056 — a reason code is not a class name, a class name is not a string id."""
    classes = {entry["name"] for entry in _statement("concurrency-class")["classes"]}
    codes = {entry["code"] for entry in _statement("serial-reason")["codes"]}
    assert not (classes & codes), "a name is used as both class and reason code: %s" % (classes & codes)
    for name in classes | codes:
        assert not name.startswith("STR-"), "a member id leaked into a role name: %s" % name


# --------------------------------------------------------------------------- #
# T094 — landing discipline reachable by path
# --------------------------------------------------------------------------- #
def test_landing_discipline_is_reachable_by_path():
    """C-054…C-056 landing face — every discipline pointer resolves."""
    statement = _statement("concurrency-contract")
    assert (REPO_ROOT / statement["disposal_surface"]).is_file()
    assert statement["mirror_rule"], "the mirror rule must be stated"
    assert "shared/" in statement["framework_sources"]
    assert statement["template_source"]["path"] == "templates/"
    faces = {row["slug"]: row["fact"] for row in statement["judgment_faces"]}
    for slug, fact_path in faces.items():
        assert slug in EIGHT_FACTS, "unknown judgement face: %s" % slug
        assert (REPO_ROOT / fact_path).is_file(), "face %s names a missing fact: %s" % (slug, fact_path)


# --------------------------------------------------------------------------- #
# T129 — every new fact is registered in the same change
# --------------------------------------------------------------------------- #
def test_every_fact_file_carries_its_registration_line():
    reader = _reader_module()
    contract = reader.load_contract(str(REPO_ROOT))
    for slug in EIGHT_FACTS:
        rel = "shared/declarations/facts/%s.yaml" % slug
        assert (REPO_ROOT / rel).is_file()
        assert contract.get(slug) == rel, "fact %r lacks its contract.yaml registration line" % slug


def test_unregistered_fact_file_turns_the_judgement_red(tmp_path):
    repo = _copy_layer(tmp_path)
    contract_file = repo / "shared" / "declarations" / "contract.yaml"
    text = contract_file.read_text(encoding="utf-8")
    mutated = text.replace(
        "concurrency-class: shared/declarations/facts/concurrency-class.yaml\n", "", 1)
    assert mutated != text, "fixture premise: the registration line must be present"
    contract_file.write_text(mutated, encoding="utf-8")
    findings = _judge_registration(repo)
    assert any(
        code == "unregistered" and path.endswith("concurrency-class.yaml")
        for code, path, _ in findings
    ), findings


# --------------------------------------------------------------------------- #
# T017 (WP5) — the unregistered shape is owner-unavailable, never a default
# --------------------------------------------------------------------------- #
def _engine(*args):
    assert ENGINE.is_file(), "the judgement engine must exist for the translation reading"
    return subprocess.run(
        [sys.executable, str(ENGINE), *[str(arg) for arg in args]],
        capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=120,
    )


def _fixture_agent(repo: Path) -> None:
    agents = repo / "agents"
    agents.mkdir(exist_ok=True)
    (agents / "fixture.agent.md").write_text(
        "---\nname: fixture\ndescription: \"fixture agent\"\ncapability-tools: []\n---\n"
        "# Fixture\n\nNever dispatch another agent.\n", encoding="utf-8")


def test_unregistered_slug_reads_owner_unavailable_with_a_named_message(tmp_path):
    """C-011 — reader exits 1 naming the fact; the engine translates to exit 2, no default."""
    repo = _copy_layer(tmp_path)
    _fixture_agent(repo)
    (repo / "shared" / "declarations" / "facts" / "concurrency-class.yaml").unlink()

    reader_got = _cli("--action", "get", "--fact", "concurrency-class", repo=repo)
    assert reader_got.returncode == 1, (
        "the reader's observed unregistered shape is exit 1: %s"
        % (reader_got.stdout + reader_got.stderr))
    assert "no declaration for fact 'concurrency-class'" in (
        reader_got.stdout + reader_got.stderr)

    out = tmp_path / "classify.json"
    proc = _engine("classify", "--repo", repo, "--json-out", out)
    assert proc.returncode == 2, "the engine must translate to exit 2: %s" % (
        proc.stdout + proc.stderr)
    envelope = json.loads(out.read_text(encoding="utf-8"))
    assert envelope["decision"] == "owner-unavailable"
    assert any(
        finding["code"] == "owner-unavailable"
        and "concurrency-class" in (finding.get("message") or "")
        for finding in envelope["findings"]
    ), envelope["findings"]
    assert "classes" not in json.dumps(envelope.get("measured") or {}), (
        "no default class table may be produced when the owner is unavailable")


# --------------------------------------------------------------------------- #
# T019 (WP5) — the removal direction: no fallback to a default
# --------------------------------------------------------------------------- #
def test_removed_fact_never_falls_back_to_a_default(tmp_path):
    """C-013 — a fact hidden from the read surface refuses, in every removal form."""
    repo = _copy_layer(tmp_path)
    _fixture_agent(repo)

    # form 1: the `fact:` key no longer names the slug (the file is present)
    serial = repo / "shared" / "declarations" / "facts" / "serial-reason.yaml"
    serial.write_text(
        serial.read_text(encoding="utf-8").replace(
            "fact: serial-reason", "fact: serial-reason-broken", 1),
        encoding="utf-8")
    record = repo / "serial.yaml"
    record.write_text(
        "pattern: serial\ncodes:\n  - single-unit\nevidence:\n  single-unit:\n"
        "    units:\n      - only-unit\n", encoding="utf-8")
    out = tmp_path / "serial.json"
    proc = _engine("serial-reason", "--repo", repo, "--record", record, "--json-out", out)
    assert proc.returncode == 2, "a removed fact must refuse: %s" % (proc.stdout + proc.stderr)
    envelope = json.loads(out.read_text(encoding="utf-8"))
    assert envelope["decision"] == "owner-unavailable"
    assert any(
        finding["code"] == "owner-unavailable"
        and "serial-reason" in (finding.get("message") or "")
        for finding in envelope["findings"]
    ), envelope["findings"]

    # form 2: the body is unparsable (a flow collection outside block-subset/v1)
    repo2 = _copy_layer(tmp_path / "second")
    _fixture_agent(repo2)
    serial = repo2 / "shared" / "declarations" / "facts" / "serial-reason.yaml"
    text = serial.read_text(encoding="utf-8")
    mutated = text.replace(
        "  groups:\n    - condition-bound\n    - factual\n",
        "  groups: [condition-bound, factual]\n", 1)
    assert mutated != text, "fixture premise: the groups block must be present"
    serial.write_text(mutated, encoding="utf-8")
    out2 = tmp_path / "serial2.json"
    proc = _engine("serial-reason", "--repo", repo2, "--record", record,
                   "--json-out", out2)
    assert proc.returncode == 2, "an unparsable fact must refuse: %s" % (
        proc.stdout + proc.stderr)
    envelope = json.loads(out2.read_text(encoding="utf-8"))
    assert envelope["decision"] == "owner-unavailable"
    assert any(
        finding["code"] == "owner-unavailable"
        and "subset" in (finding.get("message") or "")
        for finding in envelope["findings"]
    ), envelope["findings"]
