"""Integration test — User Story 3: build the derivation chain under checkable
integrity rules and assemble a traceable architecture (048 / Feature 049, P1).

Driving contract: .specify/specs/048-derive-command/contracts/derivation-model.md
                  (C1-C7, A1-A16, §9 capability degradation C-45..C-48)
Success criteria: SC-002 (errors[] classified by rule; the complete fixture exits 0)
                  and SC-005 (a run with no online capability anchors zero steps,
                  records every source as unverified, produces no architecture, and
                  reports the degradation).

End-to-end: init -> moves-add -> chain -> architecture -> validate. The green run
exits 0 with the two semantic checks still pending; a broken fixture exits 4; the
degraded run exits 0 with an empty architecture; a degraded-looking artifact that
nonetheless carries a step is rejected.
"""

from __future__ import annotations

import pytest

from tests.derive_fixtures import (
    CHAIN,
    TOPIC,
    build_artifact,
    build_degraded_artifact,
    codes,
    load_engine_module,
    scaffold,
    seed_library,
    validate,
    warning_codes,
    write_artifact,
)

ENGINE = load_engine_module("derive_utils_us3")

pytestmark = pytest.mark.integration


@pytest.fixture
def ws(tmp_path):
    code, env = scaffold(tmp_path)
    assert code == 0, env
    seed_library(tmp_path)
    return tmp_path


# --------------------------------------------------------------------------
# the green end-to-end run
# --------------------------------------------------------------------------

def test_end_to_end_chain_and_architecture_validates_clean(ws):
    write_artifact(ws, build_artifact(), TOPIC)
    code, env = validate(ws, TOPIC)
    assert code == 0, env.get("errors")
    assert env["ok"] is True and env["errors"] == []
    # the architecture is assembled and every element traces to a step
    elements = env["payload"]["elements"]
    assert elements["total"] == 2 and elements["untraceable"] == 0
    assert env["payload"]["steps"]["total"] == 2 and env["payload"]["steps"]["anchorable"] == 2
    assert all(v == "pass" for v in env["payload"]["audit"]["engine"].values())


def test_semantic_checks_remain_pending_on_the_green_run(ws):
    """A11/A14/A16 can never be inherited as green, even when every engine check passes."""
    write_artifact(ws, build_artifact(), TOPIC)
    code, env = validate(ws, TOPIC)
    assert code == 0
    assert env["semanticChecksPending"] == ["A11", "A14", "A16"], "must be non-empty"
    assert env["payload"]["audit"]["semantic"] == {"A11": "attested", "A14": "attested",
                                                       "A16": "attested"}


# --------------------------------------------------------------------------
# SC-002 — a broken fixture is rejected and classified by rule
# --------------------------------------------------------------------------

def test_a_broken_chain_is_rejected_and_classified(ws):
    # inject a banned justification into D-1's derivation (C3 / A5)
    broken = build_artifact(chain=CHAIN.replace(
        "The source treats a popularity ladder",
        "best practice. The source treats a popularity ladder"))
    write_artifact(ws, broken, TOPIC)
    code, env = validate(ws, TOPIC)
    assert code == 4
    assert env["ok"] is False and env["errors"]
    assert "banned-justification" in codes(env)
    assert "C3" in {e["rule"] for e in env["errors"]}
    # the derived audit reflects the defect (and the stale `pass` row diverges)
    assert env["payload"]["audit"]["engine"]["A5"] == "fail"


def test_an_untraceable_element_is_a_hard_failure(ws):
    broken = build_artifact().replace("- derived-from: D-1\n- confidence: derived",
                                      "- derived-from: \n- confidence: derived")
    write_artifact(ws, broken, TOPIC)
    code, env = validate(ws, TOPIC)
    assert code == 4
    assert "element-derived-from-missing" in codes(env)


# --------------------------------------------------------------------------
# SC-005 — the degraded run (no online capability)
# --------------------------------------------------------------------------

def test_probe_links_degrades_when_the_seam_cannot_reach_the_network(monkeypatch, ws):
    """SC-005's trigger: with the transport seam patched to fail, probe-links reports
    no online capability rather than declaring the sources dead (C-31/C-34)."""
    monkeypatch.setattr(ENGINE, "_http_get", lambda url, timeout, encode_param=None:
                        (None, "OfflineError: no route to host"))
    code, env = ENGINE.probe_links(ws, {"urls": ["http://example.invalid/a",
                                                 "http://example.invalid/b"]})
    assert code == ENGINE.EXIT_OK
    assert env["payload"]["online"] is False and env["payload"]["degraded"] is True
    assert all(r["access"] == "unknown" for r in env["payload"]["results"])


def test_the_degraded_run_is_an_honest_empty_success(ws):
    write_artifact(ws, build_degraded_artifact(), TOPIC)
    code, env = validate(ws, TOPIC)
    assert code == 0, env.get("errors")
    assert env["payload"]["degraded"] is True
    # SC-005: zero anchored steps, no architecture, the degradation is reported
    assert env["payload"]["steps"]["total"] == 0
    assert env["payload"]["steps"]["anchorable"] == 0
    assert env["payload"]["elements"]["total"] == 0
    assert env["payload"]["sources"]["byGrade"]["unverified"] == 2
    assert "degraded-run" in warning_codes(env)
    assert any(n.startswith("no-online-capability") for n in env["notes"])


def test_a_degraded_artifact_that_carries_a_step_is_rejected(ws):
    """C-47: degradation is not a backdoor around the anchoring rule."""
    step = ("### D-1\n- premises: S-001\n- move: M-001\n"
            "- derivation: A step that must never exist because no source is anchoring-grade "
            "in a degraded run.\n- conclusion: Something unfounded.\n"
            "- falsification: An observation that would refute it. Not checked here.\n"
            "- confidence: derived\n")
    write_artifact(ws, build_degraded_artifact(chain=step), TOPIC)
    code, env = validate(ws, TOPIC)
    assert code == 4
    assert env["payload"]["degraded"] is False
    assert "premise-grade-ineligible" in codes(env)
