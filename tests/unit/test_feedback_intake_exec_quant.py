"""Unit tests for the exec-quant intake primitives (Feature 068, US2).

Owns the pure-function face of the intake leg:
``.specify/specs/068-exec-quant-feedback-channel/contracts/intake-contract.md``
C-13 (identity_key = sha256 of the five-tuple ``source_project / unit_id /
unit_type / run_id / collected_at`` joined with ``\\x1f``; content_hash is an
INDEPENDENT canonical-JSON sha256 — the F-01 remediation, never mixed into
identity_key; keep-first on same-key/different-content), research D5 via
data-model § E6 validation note (source-slug = slugged project name + 8-char
short hash of the identity string; empty identity → literal
``unknown-project``) and data-model § E6 (envelope field set with the source
record sealed verbatim under ``record``, unknown fields zero-drop, C-15).

Fixtures are all self-constructed; the subject is the framework source
``scripts/python/feedback-utils.py`` loaded by ``tests/script_api.py`` —
never the ``.specify/`` mirror (two-hats rule).

Red-first evidence: notes/red-first-evidence.md (§ T010).
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from tests.script_api import ROOT, feedback_utils as fu

STR001 = "speckit.exec-quant"  # [[STR-001]] (requirements § Shared Strings)
ENVELOPE_KIND = "speckit.exec-quant-aggregated"  # data-model § E6
ENVELOPE_SCHEMA_VERSION = 1  # data-model § E6

SEP = "\x1f"  # C-13 / D6 five-tuple separator

E6_ENVELOPE_FIELDS = {
    "schema_version", "kind", "source_project", "source_commit",
    "identity_status", "identity_key", "content_hash", "package_file",
    "ingested_at",
}

HEX40 = "1234567890abcdef1234567890abcdef12345678"


# --------------------------------------------------------------------------- #
# fixture helpers (self-constructed)
# --------------------------------------------------------------------------- #
def _rec(collected_at: str = "2026-01-01T00:00:00Z", unit: str = "/speckit.plan",
         unit_type: str = "command", run: str = "r1", **extra) -> dict:
    record = {"kind": STR001, "schema_version": 2, "unit_id": unit,
              "unit_type": unit_type, "run_id": run, "collected_at": collected_at}
    record.update(extra)
    return record


def _identity(source_project: str = "cws-lib-python", source_commit=None,
              status: str = "identified") -> dict:
    # data-model § E2 shape
    return {"project_name": source_project, "source_commit": source_commit,
            "identity_status": status}


# --------------------------------------------------------------------------- #
# subject guard: framework source, never the mirror
# --------------------------------------------------------------------------- #
def test_subject_is_framework_source_engine():
    assert (Path(fu.__file__).resolve()
            == (ROOT / "scripts" / "python" / "feedback-utils.py").resolve())


# --------------------------------------------------------------------------- #
# C-13 / D6: identity_key (five-tuple, content excluded — F-01)
# --------------------------------------------------------------------------- #
def test_identity_key_is_sha256_of_unit_separator_tuple():
    record = _rec()
    expected = hashlib.sha256(SEP.join(
        ["cws-lib-python", "/speckit.plan", "command", "r1",
         "2026-01-01T00:00:00Z"]).encode("utf-8")).hexdigest()
    assert fu._identity_key(record, "cws-lib-python") == expected


def test_identity_key_deterministic_and_64hex():
    first = fu._identity_key(_rec(), "cws-lib-python")
    second = fu._identity_key(_rec(), "cws-lib-python")
    assert first == second
    assert re.fullmatch(r"[0-9a-f]{64}", first)


def test_identity_key_excludes_content_f01():
    # F-01 remediation: content_hash is a separate comparison field and MUST
    # NOT enter identity_key — same five-tuple with a different payload body
    # still collides on identity (the conflict branch stays constructible).
    base = _rec()
    altered = dict(base, schema_version=1, pad="different-content")
    assert (fu._identity_key(base, "cws-lib-python")
            == fu._identity_key(altered, "cws-lib-python"))
    assert fu._content_hash(base) != fu._content_hash(altered)


def test_identity_key_missing_fields_join_as_empty():
    # same convention as the U-02 sort rule: a missing field participates as ""
    bare = {"kind": STR001, "unit_id": "/speckit.plan"}
    expected = hashlib.sha256(SEP.join(
        ["cws-lib-python", "/speckit.plan", "", "", ""]).encode("utf-8")).hexdigest()
    assert fu._identity_key(bare, "cws-lib-python") == expected


def test_identity_key_varies_with_every_tuple_component():
    base_key = fu._identity_key(_rec(), "cws-lib-python")
    variants = [
        fu._identity_key(_rec(unit="/speckit.implement"), "cws-lib-python"),
        fu._identity_key(_rec(unit_type="skill"), "cws-lib-python"),
        fu._identity_key(_rec(run="r2"), "cws-lib-python"),
        fu._identity_key(_rec(collected_at="2026-01-02T00:00:00Z"),
                         "cws-lib-python"),
        fu._identity_key(_rec(), "other-project"),
    ]
    assert all(v != base_key for v in variants)


# --------------------------------------------------------------------------- #
# C-13 / D6: canonical JSON + independent content_hash
# --------------------------------------------------------------------------- #
def test_canonical_json_sort_keys_compact_raw_unicode():
    assert fu._canonical_json({"b": 1, "a": 2}) == '{"a":2,"b":1}'
    cjk = fu._canonical_json({"名称": "量化"})
    assert "名称" in cjk and "量化" in cjk  # ensure_ascii=False: raw characters
    assert "\\u" not in cjk  # never \\uXXXX-escaped


def test_canonical_json_insertion_order_insensitive():
    one = {"z": 1, "a": {"y": 2, "b": 3}}
    two = {"a": {"b": 3, "y": 2}, "z": 1}
    assert fu._canonical_json(one) == fu._canonical_json(two)


def test_content_hash_is_sha256_of_canonical_form():
    record = _rec(pad="x")
    expected = hashlib.sha256(
        fu._canonical_json(record).encode("utf-8")).hexdigest()
    assert fu._content_hash(record) == expected
    assert re.fullmatch(r"[0-9a-f]{64}", fu._content_hash(record))
    # canonicalization: dict insertion order is irrelevant to the content hash
    assert fu._content_hash({"a": 1, "b": 2}) == fu._content_hash({"b": 2, "a": 1})


# --------------------------------------------------------------------------- #
# D5 / E6: source-slug
# --------------------------------------------------------------------------- #
def test_source_slug_is_name_plus_identity_hash8():
    key = fu._identity_key(_rec(), "cws-lib-python")
    assert fu._source_slug("cws-lib-python", key) == f"cws-lib-python-{key[:8]}"


def test_source_slug_lowercases_and_substitutes_separators():
    key = "a" * 64
    assert fu._source_slug("CWS Lib Python", key) == f"cws-lib-python-{key[:8]}"


def test_source_slug_stays_in_restricted_charset():
    key = "b" * 64
    slug = fu._source_slug("CWS Lib_Python! v2", key)
    assert re.fullmatch(r"[a-z0-9-]+", slug)  # D5: 小写、[a-z0-9-]
    assert slug.endswith(f"-{key[:8]}")  # identity short hash rides last
    assert fu._source_slug("CWS Lib_Python! v2", key) == slug  # deterministic


def test_source_slug_empty_identity_is_literal_unknown_project():
    # C-12 / E6: literal `unknown-project`, no hash suffix, deterministic
    assert fu._source_slug("", "c" * 64) == "unknown-project"
    assert fu._source_slug("", "c" * 64) == fu._source_slug("", "d" * 64)


# --------------------------------------------------------------------------- #
# data-model § E6: envelope field set, verbatim record, zero-drop
# --------------------------------------------------------------------------- #
def test_envelope_field_set_matches_e6():
    envelope = fu._build_envelope(_rec(pad="unknown-but-kept"), _identity(),
                                  "pkg-2026.zip")
    assert set(envelope.keys()) == {"aggregation_envelope", "record"}
    env = envelope["aggregation_envelope"]
    assert set(env.keys()) == E6_ENVELOPE_FIELDS
    assert env["schema_version"] == ENVELOPE_SCHEMA_VERSION
    assert env["kind"] == ENVELOPE_KIND


def test_envelope_record_is_verbatim_zero_drop():
    # C-15: the intake must not rewrite, complete or drop ANY source field;
    # unknown fields ride into the envelope untouched.
    record = _rec(pad="kept", nested={"un": ["known", "字段"]}, empty="")
    envelope = fu._build_envelope(record, _identity(), "pkg.zip")
    assert envelope["record"] == record


def test_envelope_identity_and_hash_fields():
    record = _rec()
    envelope = fu._build_envelope(_rec(), _identity(source_commit=HEX40),
                                  "feedback-2026.zip")
    env = envelope["aggregation_envelope"]
    assert env["source_project"] == "cws-lib-python"
    assert env["source_commit"] == HEX40
    assert env["identity_status"] == "identified"
    assert env["identity_key"] == fu._identity_key(record, "cws-lib-python")
    assert env["content_hash"] == fu._content_hash(record)
    assert env["package_file"] == "feedback-2026.zip"  # bare filename, no path
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", env["ingested_at"])


def test_envelope_unknown_project_literal_source():
    envelope = fu._build_envelope(
        _rec(), _identity(source_project="", status="unknown-project"), "pkg.zip")
    env = envelope["aggregation_envelope"]
    assert env["source_project"] == "unknown-project"
    assert env["identity_status"] == "unknown-project"
