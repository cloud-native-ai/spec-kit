"""Contract tests: the two-half authorization resolution (slice 074a, task T007).

What this pins
--------------
`contracts/hierarchy-and-authorization.md` C-5…C-8 and C-14, executed through the
read-only engine action `scripts/python/sdd-route.py --action authorize`:

1. **Both halves, one AND** — effective authorization is *Agent definition capability*
   AND *Team seat policy*; only `allowed` on both sides lets an SDD run start (C-8).
2. **Defaults are `forbidden`, never `allowed`** — an absent key in the agent
   definition, an absent `seats:` map, an absent entry for the seat, and an absent key
   inside the entry all resolve to `forbidden` (C-3 / C-5, V-14 / V-15).
3. **A refusal names the failing half** — `agent`, `seat`, or `both`, with the two
   source paths and the seat slug, so the verdict is recheckable; a record saying only
   "not authorized" is non-conforming (C-8 / C-14, V-17 / V-18).
4. **Malformed input is not a policy value** — a flow-style `seats:` map and a seat
   entry matching no roster member are refused (exit `2`) with the seat named, and
   neither degrades to `allowed` (C-6, V-20 / V-21).
5. **Both coordinates are required** — the policy resolves by `(team, seat)`; a payload
   carrying only the seat cannot satisfy the predicate (C-7).
6. **Two-valued exit alphabet, zero writes** — `0` for **any** authorization verdict
   (allowed and refused alike; the refusal lives in the JSON verdict/reason fields) and
   `2` for malformed or unreadable input only (C-8 / C-28). The action writes no file.

The record's field names asserted here (`agent_capability`, `seat_policy`, `effective`,
`verdict`, `reason`, `failed_half`, `team_slug`, `seat_slug`, `sources`) are this
slice's authorization-probe record shape (C-8 / C-14); the engine of task T011 is the
producer and must satisfy them.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from fixtures.nested_sdd import ALLOWED, ENGINE, FORBIDDEN, build

pytestmark = pytest.mark.contract


@pytest.fixture(autouse=True)
def _engine_present():
    """Fail on absence for the right reason.

    Without this guard every ``rc == 2`` assertion below would pass while the engine
    does not exist yet (``python3 <missing file>`` also exits 2), which is exactly the
    false green this slice's red-first discipline exists to prevent.
    """
    assert ENGINE.is_file(), (
        f"--action authorize engine is missing: {ENGINE} (delivered by task T011)"
    )


def _project(tmp_path: Path, variant: str = "block"):
    return build(tmp_path / variant, variant=variant)


def _fingerprint(root: Path) -> dict:
    """Path -> sha256 of every file under ``root`` (the zero-write assertion's sensor)."""
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _record(project, seat: str, agent: Path | None = None):
    """Run the probe and return ``(rc, parsed_json_or_None, stdout, stderr)``."""
    rc, out, err = project.run_authorize(seat, agent=agent)
    try:
        parsed = json.loads(out)
    except json.JSONDecodeError:
        parsed = None
    return rc, parsed, out, err


# ---------------------------------------------------------------------------
# The four AND combinations
# ---------------------------------------------------------------------------


def test_both_halves_allowed_resolves_allowed(tmp_path):
    project = _project(tmp_path)
    rc, record, out, err = _record(project, project.seat_allowed)
    assert rc == 0, f"a produced verdict exits 0 (C-28): rc={rc} out={out!r} err={err!r}"
    assert record is not None, f"--format json MUST emit a JSON record: {out!r} {err!r}"
    assert record["agent_capability"] == ALLOWED
    assert record["seat_policy"] == ALLOWED
    assert record["effective"] == ALLOWED
    assert record["verdict"] == ALLOWED
    assert record.get("failed_half") in (None, ""), (
        f"an allowed resolution names no failing half: {record!r}"
    )


def test_seat_forbidden_names_the_seat_half(tmp_path):
    project = _project(tmp_path)
    rc, record, out, err = _record(project, project.seat_forbidden)
    assert rc == 0, (
        f"a refusal is a produced verdict, not an error status (C-8 / C-28): "
        f"rc={rc} out={out!r} err={err!r}"
    )
    assert record is not None, f"--format json MUST emit a JSON record: {out!r} {err!r}"
    assert record["agent_capability"] == ALLOWED
    assert record["seat_policy"] == FORBIDDEN
    assert record["effective"] == FORBIDDEN
    assert record["verdict"] == FORBIDDEN
    assert record["failed_half"] == "seat", (
        f"the refusal MUST name the seat half (C-8 / V-17): {record!r}"
    )
    assert record.get("reason"), "a refusal carries a reason field (C-8)"


def test_agent_key_absent_names_the_agent_half(tmp_path):
    project = _project(tmp_path)
    rc, record, out, err = _record(project, project.seat_allowed, agent=project.agent_forbidden)
    assert rc == 0, f"rc={rc} out={out!r} err={err!r}"
    assert record is not None, f"--format json MUST emit a JSON record: {out!r} {err!r}"
    assert record["agent_capability"] == FORBIDDEN, (
        "an absent capability key means forbidden, never allowed (C-3 / V-14)"
    )
    assert record["seat_policy"] == ALLOWED
    assert record["effective"] == FORBIDDEN
    assert record["failed_half"] == "agent"


def test_both_halves_failing_names_both(tmp_path):
    project = _project(tmp_path)
    rc, record, out, err = _record(project, project.seat_forbidden, agent=project.agent_forbidden)
    assert rc == 0, f"rc={rc} out={out!r} err={err!r}"
    assert record is not None, f"--format json MUST emit a JSON record: {out!r} {err!r}"
    assert record["effective"] == FORBIDDEN
    assert record["failed_half"] == "both", (
        f"two failing halves MUST be named as both, not collapsed (C-8 / V-17): {record!r}"
    )


# ---------------------------------------------------------------------------
# Defaults on the seat side
# ---------------------------------------------------------------------------


def test_absent_seats_map_defaults_to_forbidden(tmp_path):
    project = _project(tmp_path, variant="no-seats")
    rc, record, out, err = _record(project, project.seat_allowed)
    assert rc == 0, f"rc={rc} out={out!r} err={err!r}"
    assert record is not None, f"--format json MUST emit a JSON record: {out!r} {err!r}"
    assert record["seat_policy"] == FORBIDDEN, (
        "an absent seats map means forbidden for every seat (C-5 / V-15)"
    )
    assert record["effective"] == FORBIDDEN
    assert record["failed_half"] == "seat"


def test_absent_seat_entry_defaults_to_forbidden(tmp_path):
    project = _project(tmp_path)
    rc, record, out, err = _record(project, project.seat_absent)
    assert rc == 0, f"rc={rc} out={out!r} err={err!r}"
    assert record is not None, f"--format json MUST emit a JSON record: {out!r} {err!r}"
    assert record["seat_policy"] == FORBIDDEN, (
        "an absent entry for the seat means forbidden (C-5 / V-15)"
    )
    assert record["failed_half"] == "seat"


# ---------------------------------------------------------------------------
# Malformed input: refused, seat named, never degraded to allowed
# ---------------------------------------------------------------------------


def test_flow_style_seats_map_is_refused_with_the_seat_named(tmp_path):
    project = _project(tmp_path, variant="flow")
    rc, _record_json, out, err = _record(project, project.seat_allowed)
    assert rc == 2, (
        f"a flow-style seats map is malformed input and exits 2 (C-6 / C-28): "
        f"rc={rc} out={out!r} err={err!r}"
    )
    assert project.seat_allowed in (out + err), (
        f"the refused seat MUST be named in the diagnostic (C-6): {out!r} {err!r}"
    )


def test_dangling_seat_entry_is_refused_with_the_seat_named(tmp_path):
    project = _project(tmp_path, variant="dangling")
    rc, _record_json, out, err = _record(project, project.seat_allowed)
    assert rc == 2, (
        f"a seat entry matching no roster member is refused, not ignored "
        f"(C-6 / V-21): rc={rc} out={out!r} err={err!r}"
    )
    assert "ghost-seat" in (out + err), (
        f"the dangling entry's seat MUST be named (C-6 / V-21): {out!r} {err!r}"
    )


# ---------------------------------------------------------------------------
# Both coordinates required (C-7)
# ---------------------------------------------------------------------------


def test_payload_with_only_the_seat_is_refused(tmp_path):
    project = _project(tmp_path)
    argv = project.authorize_argv(project.seat_allowed)
    team_index = argv.index("--team")
    seat_only = argv[:team_index] + argv[team_index + 2 :]
    assert "--team" not in seat_only

    proc = subprocess.run(
        seat_only, cwd=str(project.root), capture_output=True, text=True
    )
    assert proc.returncode == 2, (
        f"a payload carrying only the seat cannot satisfy the predicate and is "
        f"refused as input error (C-7 / C-28): rc={proc.returncode} "
        f"out={proc.stdout!r} err={proc.stderr!r}"
    )
    assert ALLOWED not in proc.stdout, (
        "a one-coordinate payload MUST NOT produce an allowed verdict (C-7)"
    )


# ---------------------------------------------------------------------------
# The record is recheckable and the action writes nothing
# ---------------------------------------------------------------------------


def test_refusal_record_carries_two_source_paths_and_the_seat_slug(tmp_path):
    project = _project(tmp_path)
    rc, record, out, err = _record(project, project.seat_forbidden)
    assert rc == 0, f"rc={rc} out={out!r} err={err!r}"
    assert record is not None, f"--format json MUST emit a JSON record: {out!r} {err!r}"
    assert record["seat_slug"] == project.seat_forbidden, (
        f"the record MUST carry the resolved seat slug (C-8 / V-18): {record!r}"
    )
    assert record.get("team_slug") == project.team_slug, (
        f"the record MUST carry the team coordinate it resolved against (C-7): {record!r}"
    )
    sources = record.get("sources") or {}
    assert set(sources) >= {"agent", "team"}, (
        f"the record MUST carry both source paths (agent definition + team.md) so the "
        f"verdict is recheckable (C-8 / V-18): {record!r}"
    )
    agent_path = Path(sources["agent"])
    team_path = Path(sources["team"])
    assert agent_path.resolve() == project.agent_allowed.resolve(), (
        f"agent source path does not point at the definition read: {agent_path}"
    )
    assert team_path.resolve() == project.team_md.resolve(), (
        f"team source path does not point at the team.md read: {team_path}"
    )


def test_authorize_writes_no_file(tmp_path):
    project = _project(tmp_path)
    malformed = _project(tmp_path, variant="flow")
    before = {p.root.name + "/" + k: v for p, snap in ((project, _fingerprint(project.root)), (malformed, _fingerprint(malformed.root))) for k, v in snap.items()}
    for seat, agent in (
        (project.seat_allowed, None),
        (project.seat_forbidden, project.agent_forbidden),
    ):
        _record(project, seat, agent=agent)
    _record(malformed, malformed.seat_allowed)
    after = {p.root.name + "/" + k: v for p, snap in ((project, _fingerprint(project.root)), (malformed, _fingerprint(malformed.root))) for k, v in snap.items()}
    assert after == before, (
        "--action authorize is read-only: no file under the target project may be "
        "created, removed or modified (C-8 / C-28)"
    )
