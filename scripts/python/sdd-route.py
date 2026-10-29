#!/usr/bin/env python3
"""SDD routing / authorization engine (Feature 074, slice 074a-authorized-routing).

One read-only, stdlib-only engine. It never writes a file, and it never creates a second copy
of a fact another surface owns.

Actions landed here by slice `074a-authorized-routing`:

    authorize   resolve the effective SDD invocation authorization for one (team, seat)

The routing verdict and the golden-table judge are added to this same file by the later user
story of the same slice — one engine, no second data file, no second exit alphabet.

--action authorize
------------------
    python3 scripts/python/sdd-route.py --action authorize \
        --agent <agent-definition.md> --team <team-slug> --seat <seat-slug> [--format json|text]

It reads exactly two sources: the agent definition's frontmatter (the agent half) and
`.specify/teams/<team-slug>/team.md`, resolved from the working directory (the seat half). Both
coordinates are required — the policy resolves by (team, seat), so a payload carrying only the
seat cannot satisfy the predicate.

Owner pointers (cited, never restated here):

  * the closed value set, the absent-key default, and the framework-only (never
    host-rendered) status of the key: NEUTRAL_AGENT_METADATA_KEYS /
    NEUTRAL_AGENT_FRAMEWORK_KEYS in src/specify_cli/__init__.py;
  * the seat-side block map in team.md and its malformed/dangling rules:
    skills/internal/create-team/references/create-mode.md, section "Persisted team.md schema";
  * the two-half AND, the refused-but-not-an-error exit alphabet, and the requirement that a
    refusal be recheckable: `.specify/specs/074a-authorized-routing/contracts/
    hierarchy-and-authorization.md`, clauses C-6, C-7, C-8 and C-14.

Exit alphabet — exactly two meanings, and no third:

  0  a verdict was produced. An allow and a refusal are both verdicts: a refusal is carried by
     the record's verdict / reason / failed_half fields, never by the process status, because a
     caller that must record a policy decision cannot also read it as an engine failure.
  2  malformed or unreadable input — a missing coordinate, an unreadable or frontmatter-less
     file, a flow-style seat map, a seat entry matching no roster member, or a declared value
     outside the closed set. Malformed input is never a policy value.

Stdlib-only on purpose: the engine must run wherever the project's Python runs, with no spec-kit
installation and no third-party import.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_INPUT_ERROR = 2

#: [[STR-001]] — the neutral metadata key carrying SDD invocation capability / seat policy.
ALLOW_KEY = "sdd-invocation"
#: [[STR-010]] — the `team.md` frontmatter map keyed by seat slug.
SEATS_KEY = "seats"
#: [[STR-002]] / [[STR-003]] — the two literals the key set's owner enumerates. They are
#: *consumed* here, not defined here: the closed set's owner is NEUTRAL_AGENT_METADATA_KEYS
#: (src/specify_cli/__init__.py), and a value outside it is malformed input.
ALLOW = "allowed"
DENY = "forbidden"
CLOSED_VALUES = (ALLOW, DENY)

#: Roster keys a seat slug may resolve against (create-mode.md § Persisted team.md schema).
ROSTER_KEYS = ("agent", "role", "slug")


class InputError(Exception):
    """Malformed or unreadable input — the only condition that exits 2."""


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise InputError(f"cannot read {path}: {exc.strerror or exc}") from exc


def _frontmatter(lines: list, path: Path) -> list:
    """The lines between the leading `---` fence and its closing twin."""
    if not lines or lines[0].strip() != "---":
        raise InputError(f"{path}: no frontmatter block (the file must open with '---')")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index]
    raise InputError(f"{path}: unterminated frontmatter block")


def _top_level(lines: list, key: str):
    """`(index, inline_value)` of a top-level frontmatter key, or `(None, None)`."""
    for index, line in enumerate(lines):
        if not line.strip() or line[:1] in (" ", "\t"):
            continue
        name, sep, value = line.partition(":")
        if sep and name.strip() == key:
            return index, value.strip()
    return None, None


def _indented_block(lines: list, start: int) -> list:
    """The indented lines following `lines[start]`, up to the next top-level line."""
    block = []
    for line in lines[start + 1 :]:
        if line.strip() and line[:1] not in (" ", "\t"):
            break
        block.append(line)
    return block


# ---------------------------------------------------------------------------
# Seat side (team.md)
# ---------------------------------------------------------------------------


def _parse_seat_map(lines: list, path: Path, seat_slug: str):
    """The block `seats:` map as `{slug: {key: value}}`; `None` when the map is absent.

    Block style only. A flow-style / inline map is malformed input and is refused with the seat
    under resolution named — never parsed "as well as it can" and never degraded to a policy
    value.
    """
    index, inline = _top_level(lines, SEATS_KEY)
    if index is None:
        return None
    if inline:
        raise InputError(
            f"{path}: '{SEATS_KEY}' is a flow-style map ({inline!r}); only a block map keyed "
            f"by seat slug is accepted (seat under resolution: {seat_slug!r})"
        )
    entries: dict = {}
    current = None
    seat_indent = None
    for line in _indented_block(lines, index):
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("-"):
            raise InputError(
                f"{path}: '{SEATS_KEY}' must be a block map keyed by seat slug; a sequence "
                f"entry is malformed input (seat under resolution: {seat_slug!r}): {stripped!r}"
            )
        name, sep, value = stripped.partition(":")
        if not sep:
            raise InputError(
                f"{path}: malformed line inside '{SEATS_KEY}' (seat under resolution: "
                f"{seat_slug!r}): {stripped!r}"
            )
        indent = len(line) - len(line.lstrip(" \t"))
        if seat_indent is None:
            seat_indent = indent
        if indent == seat_indent:
            current = name.strip()
            if not current:
                raise InputError(
                    f"{path}: '{SEATS_KEY}' carries an empty seat slug (seat under "
                    f"resolution: {seat_slug!r})"
                )
            if value.strip():
                raise InputError(
                    f"{path}: seat {current!r} declares an inline value ({value.strip()!r}); "
                    f"each seat MUST be a block entry carrying '{ALLOW_KEY}' inside it"
                )
            entries.setdefault(current, {})
        else:
            if current is None:
                raise InputError(
                    f"{path}: indented line before any seat slug inside '{SEATS_KEY}' (seat "
                    f"under resolution: {seat_slug!r}): {stripped!r}"
                )
            entries[current][name.strip()] = value.strip()
    return entries


def _roster_ids(lines: list, path: Path, seat_slug: str) -> set:
    """Every identifier a seat slug may resolve to (member `agent` / `role` / `slug` values)."""
    index, inline = _top_level(lines, "members")
    if index is None or inline:
        raise InputError(
            f"{path}: no block 'members' roster, so a seat entry cannot be checked for "
            f"dangling membership (seat under resolution: {seat_slug!r})"
        )
    ids = set()
    for line in _indented_block(lines, index):
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            stripped = stripped[2:]
        name, sep, value = stripped.partition(":")
        if not sep:
            continue
        name = name.strip()
        value = value.strip()
        if name in ROSTER_KEYS and value:
            ids.add(value)
    return ids


def _resolve_agent_half(agent_path: Path):
    """`(value, supplying)` for the agent definition half; an absent key means deny."""
    lines = _frontmatter(_read(agent_path).splitlines(), agent_path)
    index, inline = _top_level(lines, ALLOW_KEY)
    if index is None:
        return DENY, {"source": "absent-key"}
    value = inline.strip().strip('"').strip("'")
    if value not in CLOSED_VALUES:
        raise InputError(
            f"{agent_path}: {ALLOW_KEY} = {value!r} is outside the closed value set owned by "
            f"NEUTRAL_AGENT_METADATA_KEYS (src/specify_cli/__init__.py)"
        )
    return value, {"source": "declared"}


def _resolve_seat_half(root: Path, team_slug: str, seat_slug: str):
    """`(value, supplying, team_md_path)`; an absent map / entry / key means deny."""
    team_path = root / ".specify" / "teams" / team_slug / "team.md"
    if not team_path.is_file():
        raise InputError(
            f"{team_path}: team slug {team_slug!r} does not resolve to a persisted team "
            f"definition"
        )
    lines = _frontmatter(_read(team_path).splitlines(), team_path)
    seats = _parse_seat_map(lines, team_path, seat_slug)
    roster = _roster_ids(lines, team_path, seat_slug)
    if seats is None:
        return DENY, {"source": "absent-map"}, team_path
    for key in seats:
        if key not in roster:
            raise InputError(
                f"{team_path}: seat entry {key!r} matches no roster member — reported as "
                f"dangling rather than ignored (seat under resolution: {seat_slug!r})"
            )
    if seat_slug not in seats:
        return DENY, {"source": "absent-entry"}, team_path
    entry = seats[seat_slug]
    if ALLOW_KEY not in entry:
        return DENY, {"source": "absent-key"}, team_path
    value = entry[ALLOW_KEY].strip().strip('"').strip("'")
    if value not in CLOSED_VALUES:
        raise InputError(
            f"{team_path}: seats[{seat_slug!r}].{ALLOW_KEY} = {value!r} is outside the closed "
            f"value set owned by NEUTRAL_AGENT_METADATA_KEYS (src/specify_cli/__init__.py)"
        )
    return value, {"source": "declared"}, team_path


# ---------------------------------------------------------------------------
# Action: authorize
# ---------------------------------------------------------------------------

_REASON = {
    "allowed": "both halves allow SDD invocation: the agent definition declares the capability "
    "and the seat policy allows it",
    "agent": "the agent half does not allow SDD invocation (absent key or explicit refusal; the "
    "owner's absent-key default is deny)",
    "seat": "the seat half does not allow SDD invocation (absent map, absent entry for this "
    "seat, or explicit refusal)",
    "both": "neither half allows SDD invocation: the agent definition and the seat policy both "
    "deny",
}


def action_authorize(args) -> int:
    if not args.agent:
        raise InputError("--agent is required: the authorization resolves two halves")
    if not args.team:
        raise InputError(
            "--team is required: the seat policy resolves by (team, seat), so a payload "
            "carrying only the seat cannot satisfy the predicate"
        )
    if not args.seat:
        raise InputError("--seat is required: the seat policy resolves by (team, seat)")

    agent_path = Path(args.agent)
    agent_value, agent_supplying = _resolve_agent_half(agent_path)
    seat_value, seat_supplying, team_path = _resolve_seat_half(
        Path.cwd(), args.team, args.seat
    )

    effective = ALLOW if (agent_value == ALLOW and seat_value == ALLOW) else DENY
    if effective == ALLOW:
        failed_half = None
    elif agent_value != ALLOW and seat_value != ALLOW:
        failed_half = "both"
    elif agent_value != ALLOW:
        failed_half = "agent"
    else:
        failed_half = "seat"

    record = {
        "action": "authorize",
        "agent_capability": agent_value,
        "seat_policy": seat_value,
        "effective": effective,
        "verdict": effective,
        "reason": _REASON[failed_half or "allowed"],
        "failed_half": failed_half,
        "team_slug": args.team,
        "seat_slug": args.seat,
        "supplying": {
            "agent": agent_supplying["source"],
            "seat": seat_supplying["source"],
        },
        "sources": {
            "agent": str(agent_path.resolve()),
            "team": str(team_path.resolve()),
        },
    }

    if args.format == "text":
        print(f"agent_capability: {record['agent_capability']} ({agent_supplying['source']})")
        print(f"seat_policy:      {record['seat_policy']} ({seat_supplying['source']})")
        print(f"effective:        {record['effective']}")
        print(f"verdict:          {record['verdict']}")
        print(f"failed_half:      {record['failed_half'] or '-'}")
        print(f"reason:           {record['reason']}")
        print(f"team / seat:      {record['team_slug']} / {record['seat_slug']}")
        print(f"agent source:     {record['sources']['agent']}")
        print(f"team source:      {record['sources']['team']}")
    else:
        print(json.dumps(record, indent=2, ensure_ascii=False))
    return EXIT_OK


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sdd-route.py",
        description=(
            "Read-only SDD routing / authorization engine (slice 074a-authorized-routing). "
            "Exit 0 for any produced verdict, 2 for malformed or unreadable input."
        ),
    )
    parser.add_argument("--action", required=True, choices=("authorize",))
    parser.add_argument("--agent", help="agent definition (.agent.md) carrying the capability")
    parser.add_argument("--team", help="team slug — the first authorization coordinate")
    parser.add_argument("--seat", help="seat slug — the second authorization coordinate")
    parser.add_argument("--format", choices=("json", "text"), default="json")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.action == "authorize":
            return action_authorize(args)
        raise InputError(f"unhandled action {args.action!r}")
    except InputError as exc:
        print(f"sdd-route: {exc}", file=sys.stderr)
        return EXIT_INPUT_ERROR


if __name__ == "__main__":
    sys.exit(main())
