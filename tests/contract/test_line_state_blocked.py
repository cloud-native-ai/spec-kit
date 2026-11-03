"""Contract tests for contracts/state-vocabulary.contract.md — SV-12…SV-17 (Feature 081, T005).

Subject: the **eight dispositions** A6 of ``requirements.md`` § Assumptions demands when line state
``blocked`` joins the closed set of ``skills/external/sdd-loop-driver/scripts/line-registry.py``.
A6 is the owner of *what* must change; ``plan.md`` § D6 is a landing map (which symbol each item
touches) and restates nothing. This module is the single carrier: it pins one item per test, and
every assertion is a **behaviour** — an exit code, a payload field, or the state the line is left
in. No leg asserts a bare string's presence (the vocabulary could be spelled anywhere and still be
unimplemented), and no leg reads the literal that implements an item instead of exercising it.

Item → leg, the 8/8 the definition of done reads:

| A6 item | Leg |
|---|---|
| 1 — ``STATE_VALUES`` 7 → 8 | ``test_a6_item_1_state_values_admits_blocked`` |
| 2 — ``ACTIVE_STATES`` unchanged, no concurrency slot | ``test_a6_item_2_blocked_is_not_active_and_takes_no_slot`` |
| 3 — ``HOLDING_STATES`` unchanged, holds no resource | ``test_a6_item_3_entering_blocked_releases_every_held_resource`` |
| 4 — ``blocked ⇒ merge_ready`` false | ``test_a6_item_4_merge_ready_and_blocked_are_mutually_exclusive`` |
| 5 — the three ``integration-*`` actions unreachable | ``test_a6_item_5_the_integration_actions_are_unreachable_from_blocked`` |
| 6 — the terminal guard set stays three-valued | ``test_a6_item_6_the_terminal_guard_set_stays_three_valued`` |
| 7 — recovery is ``update --state active``; ``promote-waiting`` unchanged | ``test_a6_item_7_recovery_is_update_state_active_through_the_ownership_gate`` |
| 8 — ``stale_from_state`` may carry ``blocked``, no enum expansion | ``test_a6_item_8_stale_cleanup_records_blocked_without_an_enum_expansion`` |

Two legs beyond the eight, both required by their own owner rather than by taste:

- ``test_the_block_landing_order_is_record_then_transition`` — GW-03's order as a *constraint*: on a
  ``completed`` line the failed result is recorded first and the transition follows; the reverse
  order is refused by the registry itself. Without this leg the order is prose, and an implementer
  who marks first gets a red from item 5's unreachability assertion with no recorded obligation
  having forbidden the order.
- ``test_no_line_level_never_regress_rule_was_added`` — SV-17. ``closed`` stays the only state that
  refuses every transition; ``blocked`` is left with no regression guard of its own.

Registry hygiene: every leg drives the engine through a temporary ``SPECIFY_LINE_REGISTRY_DIR``
built by ``fixtures.line_fixtures`` — never the repository registry. The temp root is pytest's
``tmp_path`` rather than ``<repo>/.specify/.tmp/``: the binding obligation is "never the repository
registry" (FR-025's ``.specify/.tmp/`` rule governs repo-local artifacts), and a registry inside the
tree would break the zero-write property other gates read through ``git status``.

Red-first: written before T006 landed, so every leg below was red at its authoring tree (the
seven-value domain rejects ``blocked`` outright). The reading is recorded in
``.specify/specs/081-acceptance-hardening/notes/red-first-evidence-081d.md`` § 2.5.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

from fixtures.line_fixtures import (
    engine_json,
    engine_path,
    make_line_id,
    make_project,
    make_run_id,
    run_engine,
)

pytestmark = pytest.mark.contract

#: The engine takes every CLI value as a string; the lease/reserve probes use this process.
_PID = str(os.getpid())

REPO_ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------- helpers


def _register(reg: Path, project: Path, **overrides) -> dict:
    """Register a line. Registration itself admits only ``active`` / ``waiting``."""
    args = [
        "--line-id", overrides.pop("line_id", make_line_id()),
        "--run-id", overrides.pop("run_id", make_run_id()),
        "--project-dir", str(overrides.pop("project_dir", project)),
        "--repo-root", str(overrides.pop("repo_root", project)),
        "--state", overrides.pop("state", "active"),
    ]
    for flag, value in overrides.items():
        args += [f"--{flag.replace('_', '-')}", str(value)]
    return engine_json("register", *args, reg=reg)


def _completed(reg: Path, project: Path, stage: str | None = None, **overrides) -> dict:
    """A ``completed`` line. ``stage`` is set by a second update: registration ignores it."""
    line_id = _register(reg, project, **overrides)["line_id"]
    entry = engine_json("update", "--line-id", line_id, "--state", "completed", reg=reg)
    if stage:
        entry = engine_json("update", "--line-id", line_id, "--stage", stage, reg=reg)
    return entry


def _blocked(reg: Path, project: Path, stage: str | None = None, **overrides) -> dict:
    entry = _completed(reg, project, stage=stage, **overrides)
    return engine_json("update", "--line-id", entry["line_id"], "--state", "blocked",
                       "--reason", "closure-blocked", reg=reg)


def _stored(reg: Path, line_id: str) -> dict:
    return json.loads((reg / f"{line_id}.json").read_text(encoding="utf-8"))


def _load_engine():
    import importlib.util

    path = engine_path()
    spec = importlib.util.spec_from_file_location("line_registry_blocked", path)
    assert spec and spec.loader, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
    sys.modules["line_registry_blocked"] = module
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------- A6 item 1


def test_a6_item_1_state_values_admits_blocked(tmp_path):
    """A6 item 1: the closed set is eight values and ``blocked`` is one of them."""
    engine = _load_engine()
    assert engine.STATE_VALUES == {
        "active", "waiting", "stalled", "completed", "orphaned", "stale", "closed", "blocked",
    }, "STATE_VALUES must be eight values: the previous seven plus `blocked`"
    assert len(engine.STATE_VALUES) == 8

    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _completed(reg, project)
    # The behaviour the literal exists for: the transition is accepted, not merely spelled.
    proc = run_engine("update", "--line-id", entry["line_id"], "--state", "blocked",
                      "--reason", "closure-blocked", reg=reg)
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["state"] == "blocked"
    assert _stored(reg, entry["line_id"])["state"] == "blocked"


# --------------------------------------------------------------------------- A6 item 2


def test_a6_item_2_blocked_is_not_active_and_takes_no_slot(tmp_path):
    """A6 item 2: ``ACTIVE_STATES`` is unchanged, so ``blocked`` is not active anywhere.

    Three consequences, asserted as behaviour rather than as set membership:
    ``--active`` does not list it; it is not an active entry for message resolution; and the
    ``promote-waiting`` concurrency counter (which counts only ``state == "active"`` with a stage)
    does not see it — a blocked line must not consume the slot a waiting line needs.
    """
    engine = _load_engine()
    assert engine.ACTIVE_STATES == {"active", "waiting"}, "ACTIVE_STATES must stay unchanged"
    assert "blocked" not in engine.ACTIVE_STATES

    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    blocked = _blocked(reg, project, stage="implement")
    assert blocked["state"] == "blocked"

    listed = engine_json("list", "--active", reg=reg)
    assert [row["line_id"] for row in listed] == [], (
        "a blocked line must not appear in `list --active`"
    )

    # One slot, occupied by nothing: a waiting line is promoted while the blocked line exists.
    waiting = _register(reg, project, state="waiting", waiting_reason="concurrency-cap",
                        queued_at="2026-11-03T00:00:00Z")
    env = dict(os.environ, SPECIFY_LINE_REGISTRY_DIR=str(reg), SPECIFY_LINE_CONCURRENCY_CAP="1")
    proc = run_engine("promote-waiting", "--line-id", waiting["line_id"], env=env)
    assert proc.returncode == 0, (
        "the blocked line holds no concurrency slot, so the cap of 1 leaves room:\n%s%s"
        % (proc.stdout, proc.stderr)
    )
    assert json.loads(proc.stdout)["state"] == "active"


# --------------------------------------------------------------------------- A6 item 3


def test_a6_item_3_entering_blocked_releases_every_held_resource(tmp_path):
    """A6 item 3 / SV-14: a blocked line holds no lease, no reservation, no ownership claim.

    The cleanup mirrors ``closed``: ``holder_line_id`` / ``waiting_reason`` / ``queued_at`` are
    cleared and the lease record is dropped. Without it a blocked line pins its waiters exactly the
    way a leaked lease does.
    """
    engine = _load_engine()
    assert engine.HOLDING_STATES == {"active", "completed"}, "HOLDING_STATES must stay unchanged"
    assert "blocked" not in engine.HOLDING_STATES

    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _completed(reg, project, stage="implement")
    line_id = entry["line_id"]
    other = _register(reg, project)["line_id"]
    engine_json("update", "--line-id", line_id, "--waiting-reason", "ownership-overlap",
                "--holder-line-id", other, "--queued-at", "2026-11-03T00:00:00Z", reg=reg)
    engine_json("lease-acquire", "--line-id", line_id, "--session", "s-1",
                "--pid", _PID, reg=reg)
    engine_json("reserve", "--line-id", line_id, "--stage", "implement",
                "--run-id", make_run_id(), "--pid", _PID, reg=reg)
    assert (reg / f"{line_id}.driver.lock").exists()
    assert list((reg / "reservations").glob(f"{line_id}.*.json"))

    blocked = engine_json("update", "--line-id", line_id, "--state", "blocked",
                          "--reason", "closure-blocked", reg=reg)

    for field in ("holder_line_id", "waiting_reason", "queued_at"):
        assert field not in blocked, (
            "entering `blocked` must clear %r, exactly as `closed` does; payload kept it: %r"
            % (field, blocked.get(field))
        )
    assert not blocked.get("lease"), "the lease record must be dropped on entering `blocked`"
    assert not (reg / f"{line_id}.driver.lock").exists(), (
        "the lease file must be released: a blocked line holds no lease (SV-14)"
    )
    assert not [p for p in (reg / "reservations").glob(f"{line_id}.*.json")
                if ".reservation-history" not in p.name], (
        "the stage reservation must be released: a blocked line holds no reservation (SV-14)"
    )
    history = (reg / "reservations" / f"{line_id}.implement.reservation-history.jsonl")
    assert history.exists() and "released" in history.read_text(encoding="utf-8"), (
        "the released reservation must be recorded in its history, not silently dropped"
    )


# --------------------------------------------------------------------------- A6 item 4


def test_a6_item_4_merge_ready_and_blocked_are_mutually_exclusive(tmp_path):
    """A6 item 4: ``state=blocked`` with ``merge_ready=true`` is rejected at the validation point.

    Both directions are asserted, because only the second one is a real hole: the first is already
    excluded by ``merge_ready ⇒ completed``, while a ``completed`` line that is ``merge_ready`` and
    then asked to become ``blocked`` would keep the flag and land in a state the invariant forbids.
    """
    project = make_project(tmp_path)
    reg = tmp_path / "reg"

    # (a) asking for merge_ready on a blocked line
    blocked = _blocked(reg, project)
    proc = run_engine("update", "--line-id", blocked["line_id"], "--merge-ready", "true", reg=reg)
    assert proc.returncode == 2, "merge_ready on a blocked line must be refused: %s" % proc.stdout
    assert "completed" in proc.stderr

    # (b) asking a merge_ready completed line to become blocked
    queued = _completed(reg, project)
    engine_json("integration-enqueue", "--line-id", queued["line_id"], reg=reg)
    assert _stored(reg, queued["line_id"])["merge_ready"] is True
    proc = run_engine("update", "--line-id", queued["line_id"], "--state", "blocked",
                      "--reason", "closure-blocked", reg=reg)
    assert proc.returncode == 2, (
        "entering `blocked` with merge_ready=true must be refused at the same validation point "
        "that enforces merge_ready ⇒ completed; got exit %d\nstdout:%s\nstderr:%s"
        % (proc.returncode, proc.stdout, proc.stderr)
    )
    assert _stored(reg, queued["line_id"])["state"] == "completed", (
        "a refused transition must leave the line where it was"
    )


# --------------------------------------------------------------------------- A6 item 5


def test_a6_item_5_the_integration_actions_are_unreachable_from_blocked(tmp_path):
    """A6 item 5: the three ``integration-*`` actions keep requiring ``state=completed``."""
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _blocked(reg, project)
    line_id = entry["line_id"]

    for action, extra in (
        ("integration-enqueue", []),
        ("integration-record", ["--result", "failed", "--reason", "closure-blocked"]),
    ):
        proc = run_engine(action, "--line-id", line_id, *extra, reg=reg)
        assert proc.returncode == 2, (
            "%s must remain structurally unreachable from `blocked`; got exit %d\n%s"
            % (action, proc.returncode, proc.stdout)
        )
        assert "completed" in proc.stderr, proc.stderr

    # integration-plan has no line argument: a blocked line simply leaves the queue.
    queued = _completed(reg, project)
    engine_json("integration-enqueue", "--line-id", queued["line_id"], reg=reg)
    before = engine_json("integration-plan", reg=reg)
    assert [row["line_id"] for row in before if row["order"]] == [queued["line_id"]]
    engine_json("integration-record", "--line-id", queued["line_id"], "--result", "failed",
                "--reason", "closure-blocked", reg=reg)
    engine_json("update", "--line-id", queued["line_id"], "--state", "blocked",
                "--reason", "closure-blocked", reg=reg)
    after = engine_json("integration-plan", reg=reg)
    assert queued["line_id"] not in [row["line_id"] for row in after], (
        "a blocked line must not remain in the integration queue"
    )


# --------------------------------------------------------------------------- A6 item 6


def test_a6_item_6_the_terminal_guard_set_stays_three_valued(tmp_path):
    """A6 item 6: ``{closed, stale, orphaned}`` must **not** gain ``blocked``.

    ``blocked`` is recoverable by design, so the five ``not in {closed, stale, orphaned}`` guards
    must keep letting it act. Two of the five are exercised here as behaviour (the ownership gate
    and the lease gate); the assertion that the set is still three-valued is the contrast — the
    same calls on a ``closed`` line are refused.
    """
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    blocked = _blocked(reg, project, stage="implement")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"line_id": blocked["line_id"],
                                    "owned_paths": [str(project / "src")]}), encoding="utf-8")

    acquired = run_engine("lease-acquire", "--line-id", blocked["line_id"], "--session", "s-1",
                          "--pid", _PID, reg=reg)
    assert acquired.returncode == 0, (
        "a blocked line must still be leaseable — `blocked` is not in the terminal guard set: %s"
        % acquired.stdout
    )
    owned = run_engine("ownership-check", "--line-id", blocked["line_id"],
                       "--manifest", str(manifest), reg=reg)
    assert owned.returncode == 0, (
        "a blocked line must still pass `ownership-check`'s guard: %s%s"
        % (owned.stdout, owned.stderr)
    )

    closed = _completed(reg, project)
    engine_json("deregister", "--line-id", closed["line_id"], "--reason", "u6-closed", reg=reg)
    for action, extra in (
        ("lease-acquire", ["--session", "s-2", "--pid", _PID]),
        ("reserve", ["--stage", "implement", "--run-id", make_run_id(), "--pid", _PID]),
    ):
        proc = run_engine(action, "--line-id", closed["line_id"], *extra, reg=reg)
        assert proc.returncode == 2, (
            "%s must still refuse a closed line — the guard set stays three-valued: %s"
            % (action, proc.stdout)
        )


# --------------------------------------------------------------------------- A6 item 7


def test_a6_item_7_recovery_is_update_state_active_through_the_ownership_gate(tmp_path):
    """A6 item 7 / SV-15: recovery is ``update --state active`` — not ``promote-waiting``.

    The "entering ``active``" guard must admit ``blocked`` alongside ``{waiting, stalled}`` (the
    single line A6 touches from both sides), the recovery must carry its recorded unblock reason,
    and it must still pass the ownership gate: a released manifest keeps the line out until
    ``ownership-check`` re-claims it.
    """
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    blocked = _blocked(reg, project)
    line_id = blocked["line_id"]

    direct = run_engine("promote-waiting", "--line-id", line_id, reg=reg)
    assert direct.returncode == 2, (
        "`promote-waiting` requires state=waiting and must not revive a blocked line: %s"
        % direct.stdout
    )
    assert _stored(reg, line_id)["state"] == "blocked", "the refused promotion changed the state"

    recovered = run_engine("update", "--line-id", line_id, "--state", "active",
                           "--reason", "closure re-run passed", reg=reg)
    assert recovered.returncode == 0, (
        "the entering-active guard must admit `blocked` — otherwise the recovery path A6 names "
        "does not exist:\n%s%s" % (recovered.stdout, recovered.stderr)
    )
    payload = json.loads(recovered.stdout)
    assert payload["state"] == "active"
    assert payload.get("unblock_reason") == "closure re-run passed", (
        "recovery must record its unblock reason (SV-15); payload: %r" % (payload,)
    )

    # The ownership gate is not bypassed by the recovery: a released line must re-claim first.
    gated = _blocked(reg, project, stage="implement")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"line_id": gated["line_id"],
                                    "owned_paths": [str(project / "src")]}), encoding="utf-8")
    engine_json("ownership-check", "--line-id", gated["line_id"],
                "--manifest", str(manifest), reg=reg)
    engine_json("release-ownership", "--line-id", gated["line_id"], "--reason", "handover",
                "--evidence-ref", "evidence:handover", reg=reg)
    refused = run_engine("update", "--line-id", gated["line_id"], "--state", "active",
                         "--reason", "retry", reg=reg)
    assert refused.returncode == 3, (
        "recovery must still pass the ownership gate — a released line re-acquires via "
        "`ownership-check` before it can become active: %s%s" % (refused.stdout, refused.stderr)
    )
    assert json.loads(refused.stdout)["error"]["message"].startswith("ownership was released")


# --------------------------------------------------------------------------- A6 item 8


def test_a6_item_8_stale_cleanup_records_blocked_without_an_enum_expansion(tmp_path):
    """A6 item 8 / SV-16: ``stale_from_state`` may carry ``blocked``; no enum is added for it.

    The field stores the *previous* state, so it needs no domain of its own — which is exactly what
    the leg proves: the value arrives intact, and the state vocabulary gained no second list.
    """
    engine = _load_engine()
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    blocked = _blocked(reg, project)
    stale = engine_json("deregister", "--line-id", blocked["line_id"],
                        "--reason", "stale-cleanup", reg=reg)
    assert stale["state"] == "stale"
    assert stale["stale_from_state"] == "blocked", (
        "`stale_from_state` must carry `blocked` verbatim; got %r" % stale.get("stale_from_state")
    )

    # No enum expansion: the same engine still rejects a value outside STATE_VALUES, and there is
    # no second state-like domain that grew to accommodate the new value.
    proc = run_engine("update", "--line-id", _completed(reg, project)["line_id"],
                      "--state", "blocked-out", reg=reg)
    assert proc.returncode == 2, proc.stdout
    domains = [name for name, value in vars(engine).items()
               if isinstance(value, (set, frozenset, tuple))
               and "blocked" in value and name != "STATE_VALUES"]
    assert not domains, (
        "no second state domain may carry `blocked` — the enum expansion SV-16 forbids: %r" % domains
    )


# --------------------------------------------------------------------------- GW-03's order


def test_the_block_landing_order_is_record_then_transition(tmp_path):
    """GW-03: the failed result is recorded **while the line is still ``completed``**.

    ``integration-record`` refuses a line that is not ``completed``, so the order is a constraint
    and not a style: marking first loses both the reason and the result. Both directions are run.
    """
    project = make_project(tmp_path)
    reg = tmp_path / "reg"

    # Forward: record, then transition.
    entry = _completed(reg, project)
    engine_json("integration-enqueue", "--line-id", entry["line_id"], reg=reg)
    recorded = engine_json("integration-record", "--line-id", entry["line_id"],
                           "--result", "failed", "--reason", "closure-blocked", reg=reg)
    assert recorded["state"] == "completed", (
        "recording a failed result must not itself move the line off `completed`"
    )
    assert recorded["integration_result"]["status"] == "failed"
    assert recorded["integration_result"]["reason"] == "closure-blocked"
    landed = engine_json("update", "--line-id", entry["line_id"], "--state", "blocked",
                         "--reason", "closure-blocked", reg=reg)
    assert landed["state"] == "blocked"
    final = _stored(reg, entry["line_id"])
    assert final["state"] == "blocked"
    assert final["integration_result"]["status"] == "failed", (
        "the blocked line must keep the recorded result — marking first is what loses it"
    )

    # Reverse: mark, then record — refused by the registry itself.
    other = _completed(reg, project)
    engine_json("integration-enqueue", "--line-id", other["line_id"], reg=reg)
    engine_json("integration-record", "--line-id", other["line_id"], "--result", "failed",
                "--reason", "closure-blocked", reg=reg)
    engine_json("update", "--line-id", other["line_id"], "--state", "blocked",
                "--reason", "closure-blocked", reg=reg)
    late = run_engine("integration-record", "--line-id", other["line_id"], "--result", "failed",
                      "--reason", "closure-blocked", reg=reg)
    assert late.returncode == 2, (
        "the reverse order must be refused (`integration-record requires state=completed`); "
        "got exit %d\n%s" % (late.returncode, late.stdout)
    )
    assert "requires state=completed" in late.stderr, late.stderr


# --------------------------------------------------------------------------- SV-17


def test_no_line_level_never_regress_rule_was_added(tmp_path):
    """SV-17: this feature adds no "a line state never regresses" rule.

    ``closed`` stays the only state that refuses every transition. Anything stricter — a guard that
    re-opened the old set instead of widening it — would show up here as a refusal of a transition
    the engine accepted before ``blocked`` existed.
    """
    project = make_project(tmp_path)
    reg = tmp_path / "reg"

    blocked = _blocked(reg, project)
    moved = run_engine("update", "--line-id", blocked["line_id"], "--state", "stalled", reg=reg)
    assert moved.returncode == 0, (
        "no never-regress rule was added, so leaving `blocked` for a non-active state is not "
        "refused by the state engine: %s%s" % (moved.stdout, moved.stderr)
    )
    assert json.loads(moved.stdout)["state"] == "stalled"

    closed = _completed(reg, project)
    engine_json("deregister", "--line-id", closed["line_id"], "--reason", "u6-closed", reg=reg)
    terminal = run_engine("update", "--line-id", closed["line_id"], "--state", "active",
                          "--reason", "reopen", reg=reg)
    assert terminal.returncode != 0, "`closed` stays terminal — it is the one refusal that remains"
