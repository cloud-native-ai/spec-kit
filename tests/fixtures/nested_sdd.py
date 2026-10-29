"""Throwaway target-project harness for the 074a authorization / nested-invocation contracts.

Owned by: Feature 074 slice `074a-authorized-routing`, task T006
(`.specify/specs/074a-authorized-routing/tasks.md`).
Consumers: `tests/contract/test_sdd_authorization.py` (T007),
`tests/contract/test_nested_sdd_invocation.py` (T012).

What it is
----------
A deterministic, stdlib-only builder for a **minimal target project** — a disposable
`.specify/` tree carrying exactly the four surfaces the slice's authorization and entry
validation read:

1. `.specify/teams/<slug>/team.md` — frontmatter with a `seats:` **block map** keyed by
   seat slug, each entry holding the same key; three roster members: one seat declared
   allowed, one declared forbidden, one with **no entry at all**;
2. two `.agent.md` definitions — one declaring the capability key as allowed, one
   omitting the key entirely (absent key);
3. `.specify/goal/<slug>/goal.md` — one Goal with one `open` Target (the goal grammar is
   the one `scripts/python/goal-utils.py` renders, so the file is valid by construction);
4. one **pre-recorded routing verdict** (data-model E4 field face) whose verdict is the
   SDD value, so entry validation can be tested without the routing engine (US1 must be
   independently testable from US2).

Three `seats:` shapes are reachable, because a malformed-map guard that can only be
driven in one direction proves nothing:
``variant="block"``     the accepted shape (three seats as described above)
``variant="flow"``      a flow-style map `seats: {seat-allowed: ...}` (malformed, C-6)
``variant="dangling"``  a block map carrying an entry for a seat no roster member has (C-6)
``variant="no-seats"``  no `seats:` key at all (absent map ⇒ forbidden, C-5)

Rules this module holds itself to
---------------------------------
1. **It never writes the framework repository.** Every project it builds lives under a
   caller-supplied root (pytest ``tmp_path``); construction refuses a root that resolves
   inside the framework source tree. The process working directory is never changed —
   every subprocess invocation receives an explicit ``cwd``.
2. **Literals are cited, never redefined.** The strings this module writes
   (`sdd-invocation`, `allowed`, `forbidden`, `seats`, verdict values) are the slice's
   ``[[STR-NNN]]`` literals from `requirements.md` § Shared Strings; this file pins them
   as fixture data and defines no vocabulary of its own. In particular the fixture
   verdict record's ``reason_code`` is a fixture datum — the closed reason-code
   vocabulary is owned by `shared/definitions/sdd-routing-definitions.md` § Reason codes
   and is deliberately not restated here.
3. **Determinism.** No clock, no randomness: every built file is byte-identical across
   runs, so a byte-level comparison of two builds is a meaningful assertion.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "sdd-route.py"

#: ``[[STR-001]]`` / ``[[STR-002]]`` / ``[[STR-003]]`` / ``[[STR-004]]`` / ``[[STR-010]]``
#: from `requirements.md` § Shared Strings.
KEY = "sdd-invocation"
ALLOWED = "allowed"
FORBIDDEN = "forbidden"
VERDICT_SDD = "sdd"
SEATS_KEY = "seats"

VARIANTS = ("block", "flow", "dangling", "no-seats")
DEFAULT_TEAM_SLUG = "fixture-team"
DEFAULT_GOAL_SLUG = "fixture-goal"


@dataclass(frozen=True)
class NestedSddProject:
    """Handle to one built target project. Every path is absolute."""

    root: Path
    variant: str
    team_slug: str
    team_md: Path
    seat_allowed: str
    seat_forbidden: str
    seat_absent: str
    agent_allowed: Path
    agent_forbidden: Path
    goal_slug: str
    goal_path: Path
    target_id: str
    verdict_record: Path

    # -- dispatch payload (data-model E9: team_slug + seat_slug are the two coordinates) --

    def authorize_argv(self, seat: str, agent: Path | None = None, fmt: str = "json") -> list:
        """The `--action authorize` invocation for one (team, seat) resolution."""
        agent_path = agent if agent is not None else self.agent_allowed
        return [
            "python3",
            str(ENGINE),
            "--action",
            "authorize",
            "--agent",
            str(agent_path),
            "--team",
            self.team_slug,
            "--seat",
            seat,
            "--format",
            fmt,
        ]

    def run_authorize(self, seat: str, agent: Path | None = None, fmt: str = "json"):
        """Run `--action authorize` with this project as the working directory.

        Returns ``(returncode, stdout, stderr)``. The engine resolves
        `.specify/teams/<slug>/team.md` relative to its working directory, which is why
        the caller's root is passed as ``cwd`` instead of inventing a flag.
        """
        proc = subprocess.run(
            self.authorize_argv(seat, agent=agent, fmt=fmt),
            cwd=str(self.root),
            capture_output=True,
            text=True,
        )
        return proc.returncode, proc.stdout, proc.stderr

    def run_authorize_json(self, seat: str, agent: Path | None = None) -> dict:
        """Same as :meth:`run_authorize` but parses stdout as JSON (caller asserts rc)."""
        rc, out, err = self.run_authorize(seat, agent=agent)
        try:
            payload = json.loads(out)
        except json.JSONDecodeError as exc:  # pragma: no cover - diagnostic path
            raise AssertionError(
                f"--action authorize emitted non-JSON output (rc={rc}): {out!r} / {err!r}"
            ) from exc
        return payload


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def _refuse_framework_root(root: Path) -> None:
    resolved = root.resolve()
    if resolved == REPO_ROOT or REPO_ROOT in resolved.parents:
        raise ValueError(
            f"fixture root {resolved} resolves inside the framework source tree "
            f"({REPO_ROOT}); pass a disposable directory (pytest tmp_path)"
        )


def build(
    root: Path,
    variant: str = "block",
    team_slug: str = DEFAULT_TEAM_SLUG,
    goal_slug: str = DEFAULT_GOAL_SLUG,
) -> NestedSddProject:
    """Materialise one minimal target project under ``root`` and return its handle."""
    if variant not in VARIANTS:
        raise ValueError(f"unknown variant {variant!r}; expected one of {VARIANTS}")
    root = Path(root)
    _refuse_framework_root(root)
    root.mkdir(parents=True, exist_ok=True)

    seat_allowed = "seat-allowed"
    seat_forbidden = "seat-forbidden"
    seat_absent = "seat-absent"
    target_id = "T-001"

    team_dir = root / ".specify" / "teams" / team_slug
    team_dir.mkdir(parents=True, exist_ok=True)
    team_md = team_dir / "team.md"
    team_md.write_text(
        _render_team(
            variant=variant,
            team_slug=team_slug,
            goal_slug=goal_slug,
            target_id=target_id,
            seats=(seat_allowed, seat_forbidden, seat_absent),
        ),
        encoding="utf-8",
    )

    agents_dir = root / ".specify" / "agents" / "instances"
    agents_dir.mkdir(parents=True, exist_ok=True)
    agent_allowed = agents_dir / f"{seat_allowed}.agent.md"
    agent_allowed.write_text(
        _render_agent(seat_allowed, capability=ALLOWED), encoding="utf-8"
    )
    agent_forbidden = agents_dir / f"{seat_forbidden}.agent.md"
    agent_forbidden.write_text(_render_agent(seat_forbidden, capability=None), encoding="utf-8")

    goal_dir = root / ".specify" / "goal" / goal_slug
    goal_dir.mkdir(parents=True, exist_ok=True)
    goal_path = goal_dir / "goal.md"
    goal_path.write_text(_render_goal(goal_slug, target_id), encoding="utf-8")

    execution_dir = root / ".specify" / "agents" / "execution"
    execution_dir.mkdir(parents=True, exist_ok=True)
    verdict_record = execution_dir / "20261029T000000Z-routing-verdict-d1.md"
    verdict_record.write_text(_render_verdict_record(seat_allowed), encoding="utf-8")

    return NestedSddProject(
        root=root,
        variant=variant,
        team_slug=team_slug,
        team_md=team_md,
        seat_allowed=seat_allowed,
        seat_forbidden=seat_forbidden,
        seat_absent=seat_absent,
        agent_allowed=agent_allowed,
        agent_forbidden=agent_forbidden,
        goal_slug=goal_slug,
        goal_path=goal_path,
        target_id=target_id,
        verdict_record=verdict_record,
    )


# ---------------------------------------------------------------------------
# Renderers (deterministic text; no clock, no randomness)
# ---------------------------------------------------------------------------


def _render_team(
    *,
    variant: str,
    team_slug: str,
    goal_slug: str,
    target_id: str,
    seats: tuple,
) -> str:
    seat_allowed, seat_forbidden, seat_absent = seats
    members = "\n".join(
        f"  - agent: {seat}\n    role: {role}\n    lifecycle: temporary"
        for seat, role in (
            (seat_allowed, "driver-host"),
            (seat_forbidden, "reviewer"),
            (seat_absent, "observer"),
        )
    )
    if variant == "block":
        seats_block = (
            f"{SEATS_KEY}:\n"
            f"  {seat_allowed}:\n"
            f"    {KEY}: {ALLOWED}\n"
            f"  {seat_forbidden}:\n"
            f"    {KEY}: {FORBIDDEN}\n"
        )
    elif variant == "flow":
        seats_block = (
            f"{SEATS_KEY}: {{ {seat_allowed}: {{ {KEY}: {ALLOWED} }} }}\n"
        )
    elif variant == "no-seats":
        seats_block = ""  # C-5: an absent map means forbidden for every seat
    else:  # dangling — an entry for a seat no member carries
        seats_block = (
            f"{SEATS_KEY}:\n"
            f"  {seat_allowed}:\n"
            f"    {KEY}: {ALLOWED}\n"
            f"  ghost-seat:\n"
            f"    {KEY}: {ALLOWED}\n"
        )
    return (
        "---\n"
        f"name: {team_slug}\n"
        f"slug: {team_slug}\n"
        "description: Fixture team for the 074a authorization contract tests.\n"
        "goal: Exercise the two-half authorization resolution against a disposable project.\n"
        f"goal_slug: {goal_slug}\n"
        f"focus_target: {target_id}\n"
        "pattern: serial\n"
        "created: 2026-10-29\n"
        "updated: 2026-10-29\n"
        "territory:\n"
        "  write:\n"
        "    - src/\n"
        f"{seats_block}"
        "members:\n"
        f"{members}\n"
        "---\n"
        "\n"
        "## Goal\n\n"
        "Fixture goal: drive the authorization and entry-validation contracts.\n"
        "\n"
        "## Static Structure\n\n"
        "| Role | Stage | Type |\n"
        "|------|-------|------|\n"
        "| driver-host | implement | executor |\n"
        "| reviewer | review | reviewer |\n"
        "\n"
        "## Dynamic Structure\n\n"
        "Serial: one duty at a time; no concurrency in the fixture.\n"
    )


def _render_agent(seat: str, capability: str | None) -> str:
    lines = [
        "---",
        f"name: {seat}",
        f"description: Fixture agent definition for seat {seat}.",
    ]
    if capability is not None:
        lines.append(f"{KEY}: {capability}")
    lines += [
        "---",
        "",
        f"# {seat}",
        "",
        "Fixture body: this definition exists so the authorization probe has a real",
        "frontmatter to read. The body carries no metadata.",
        "",
    ]
    return "\n".join(lines)


def _render_goal(goal_slug: str, target_id: str) -> str:
    return (
        "---\n"
        "status: active\n"
        "created: 2026-10-29\n"
        "updated: 2026-10-29\n"
        "---\n"
        "\n"
        f"# Goal: {goal_slug}\n"
        "\n"
        "## Objective\n\n"
        "Prove the slice's authorization and entry-validation contracts against a "
        "disposable project.\n"
        "\n"
        "## Success Criteria\n\n"
        "1. The authorization resolution names the failing half on every refusal.\n"
        "\n"
        "## Targets\n\n"
        "| ID | Target | Status |\n"
        "|----|--------|--------|\n"
        f"| {target_id} | drive the authorization contracts end to end | open |\n"
        "\n"
        "## History\n\n"
        "- 2026-10-29 — created.\n"
        f"- 2026-10-29 target {target_id} added: drive the authorization contracts end to end\n"
    )


def _render_verdict_record(actor: str) -> str:
    """One pre-recorded routing verdict (data-model E4 field face).

    The five declared inputs carry the literals the contract names; ``verdict`` is the
    SDD value so entry validation can consume it without the routing engine. The reason
    code is a fixture datum (see the module docstring: the closed vocabulary is owned by
    the owner document and is not restated here).
    """
    return (
        "---\n"
        "record: routing-verdict\n"
        "duty: drive-the-authorization-contracts\n"
        f"actor: {actor}\n"
        "recorded_at: 2026-10-29T00:00:00Z\n"
        "change_nature: feature\n"
        "traceability: required\n"
        "blast_radius: cross-cutting\n"
        "reversibility: hard\n"
        "complexity: standard\n"
        f"verdict: {VERDICT_SDD}\n"
        "reason_code: fixture-recorded-decision\n"
        "---\n"
        "\n"
        "Pre-recorded routing verdict for the fixture duty (data-model E4 field face).\n"
        "It exists so US1's entry validation does not depend on US2's engine.\n"
    )
