#!/usr/bin/env python3
"""team-view.py — deterministic read-only reader behind `/speckit.team view` (103-team-view).

Owner of the fixed-rule extraction for the view mode: team definition facts, archive
enumeration, report listing, ledger aggregation and the latest-report summary. Binding and
anchor facts are composed from the goal-utils reads (`binding`, `list`, `targets --list`);
this program re-implements none of their semantics and writes nothing.

Contract: `.specify/specs/103-team-view/contracts/team-view-program.contract.md`
(C-24 read-only, C-25 engine composition, C-26 closed CLI surface, C-27 script interface,
C-28 closed exit codes, C-29 output modes).

Usage:
  team-view.py [options] [<team-slug>]

Exit codes:
  0  rendering produced (single team, overview, empty archive, dangling binding)
  2  input error (undeclared option, invalid --scope, extra positional, no-slug --scope auto)
  3  team not found (single mode)
  4  definition corrupt (single mode: team.md missing, unreadable or unparseable)
  5  rendered, but a required fact group is unreadable because an engine read failed

Python >= 3.8, standard library only; the only sibling import is ``script_interface_cli``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_INPUT = 2
EXIT_NOT_FOUND = 3
EXIT_CORRUPT = 4
EXIT_DEGRADED = 5

APPROVED_EXIT_CODES = (EXIT_OK, EXIT_INPUT, EXIT_NOT_FOUND, EXIT_CORRUPT, EXIT_DEGRADED)

SCOPE_VALUES = ("teams", "auto", "anchor", "goals")
DEFAULT_SCOPE = "teams"

PROGRAM_NAME = "team-view.py"

DECLARED_OPTIONS = (
    "--repo-root",
    "--scope",
    "--spec-dir",
    "--json",
)

try:  # pragma: no cover - exercised through every CLI test
    from script_interface_cli import (
        VersionAction,
        configure_parser,
        preparse_version_guard,
    )
except ImportError:  # pragma: no cover - the helper ships beside this file
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from script_interface_cli import (  # type: ignore[no-redef]
        VersionAction,
        configure_parser,
        preparse_version_guard,
    )


def resolve_repo_root(explicit: str | None) -> Path:
    """The repository root: the explicit option, or derived from this file's own path.

    Two Hats rule (`shared/definitions/dogfooding-definitions.md` § 2.1): self-location
    may fire only on a literal ``.specify`` component of this file's own resolved path
    (the mirror copy). The framework-source copy `<repo>/scripts/python/team-view.py`
    takes the plain three-level parent instead; walking up to "any ancestor containing
    .specify" is forbidden because it self-matches in this repository. A derived root
    named ``.specify`` is never a repository root.
    """
    if explicit:
        return Path(explicit).expanduser().resolve()
    own = Path(__file__).resolve()
    parts = own.parts
    if ".specify" in parts[:-1]:
        index = parts.index(".specify")
        root = Path(*parts[:index]) if index > 0 else Path(parts[0])
    else:
        root = own.parents[2]
    while root.name == ".specify":
        root = root.parent
    return root


def resolve_scope(requested, team_slug):
    """Return ``(effective_scope, error_message)`` for the closed ``--scope`` surface.

    ``teams`` is serviced; ``auto`` is serviced only for a single slug (a no-slug ``auto``
    is not decidable); ``anchor`` / ``goals`` are refused by name as not applicable to the
    team archive layer. A value the team archive cannot serve is reported, never ignored.
    """
    value = requested or DEFAULT_SCOPE
    if value == "teams":
        return "teams", None
    if value == "auto":
        if team_slug is None:
            return value, (
                "--scope auto 不可用于无 slug 的概览：auto 需要且仅需要单个 team slug"
                " 以解析团队身份；请改用 --scope teams 或提供一个 slug"
            )
        return value, None
    return value, (
        "--scope %s 对 view 不适用：view 只在团队档案层（teams）解析团队，"
        "无法服务的取值必须显式报告；请改用 --scope teams（或单 slug 的 --scope auto）"
        % value
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=(
            "Read-only team view: six information groups for one team, or an overview "
            "of every team in the archive."
        ),
    )
    configure_parser(
        parser,
        effects="none; reads the team archive and prints; a flag-only invocation writes nothing",
        codes=(
            "0 rendering produced; 2 input error; 3 team not found; "
            "4 definition corrupt; 5 rendered with a degraded engine read"
        ),
    )
    parser.add_argument(
        "team_slug",
        nargs="?",
        default=None,
        metavar="<team-slug>",
        help="exact slug under .specify/teams/; omitted = overview of every team",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="repository root (default: derived from this file's own resolved path)",
    )
    parser.add_argument(
        "--scope",
        default=None,
        choices=SCOPE_VALUES,
        help="archive layer selector; teams is the serviced layer, auto only for one slug",
    )
    parser.add_argument(
        "--spec-dir",
        default=None,
        help="forwarded to engine reads that accept it; never decides a landing point",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the internal test envelope instead of the human-facing rendering",
    )
    VersionAction.attach(parser)
    return parser


def emit_view(args, mode: str, repo_root: Path, scope: str) -> int:
    """Render one view. The extraction and rendering face lands with the story tasks."""
    raise NotImplementedError("view extraction and rendering are not implemented yet")


def main(argv=None) -> int:
    line = list(sys.argv[1:] if argv is None else argv)
    preparse_version_guard(line, declared=DECLARED_OPTIONS)
    parser = build_parser()
    args = parser.parse_args(line)

    scope, error = resolve_scope(args.scope, args.team_slug)
    if error is not None:
        print("error: " + error, file=sys.stderr)
        return EXIT_INPUT

    repo_root = resolve_repo_root(args.repo_root)
    mode = "overview" if args.team_slug is None else "single"

    if scope == "auto" and not (repo_root / ".specify" / "teams" / args.team_slug).is_dir():
        print(
            "error: --scope auto 无法在团队档案中解析 slug %r；auto 只服务身份可解析的单团队"
            % args.team_slug,
            file=sys.stderr,
        )
        return EXIT_INPUT

    return emit_view(args, mode, repo_root, scope)


if __name__ == "__main__":
    sys.exit(main())
