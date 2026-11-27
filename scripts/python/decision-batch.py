#!/usr/bin/env python3
"""decision-batch.py — deterministic batch decision panel engine (Feature 112).

The batch capability's rules are owned by ``shared/definitions/decision-definitions.md``
(batch extension): the closed pending-source roster, the pending-item block grammar, the
presentation contract, the recommended default and grounding join, the disposition and
reply contract, the batch record contract, the completeness/refusal rules and the replay
contract. This engine performs the Program-First judgements over them (scan, membership
validation, bookkeeping, pointer resolution) and never restates their tables.

Actions (closed set):
  scan    read-only: scan the closed source roster and render one presentation
          (text body + machine payload).
  record  the only writer: re-scan, validate the reply, mint the batch id and write the
          batch record through the memory engine, then the register rows/status cells and
          the pending-block resolution annotations.
  replay  read-only: reconstruct one recorded batch from the batch record and resolvable
          pointers alone; any unresolvable pointer is reported and the exit is non-zero.

Options of every action:
  --workspace-root PATH   the workspace the panel reads (default: the current directory)
  --format {text,json}    output format (default: text)
  --presentation PATH     the scan payload a reply is bound to (record)
  --reply PATH            the reply file carrying the user's verbatim text (record)
  --authorization {interactive,unattended}
                          caller-declared interaction authorization (record); missing
                          is treated as unattended and the record is refused
  --batch PATH            the batch record to replay (replay)
  -h / --help             this body (same body for both spellings), exit 0
  --version               one line ``<script-name> <framework-version>``, exit 0

Exit codes: 0 = success (including the explicit ``nothing-pending`` result) /
1 = a documented refusal / 2 = usage or environment error.

Side effects: scan and replay write nothing; record writes only through the named
carriers. Standard library only.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_REFUSED = 1
EXIT_USAGE = 2

#: The closed declared action set (C-608). A fourth value MUST NOT be accepted before the
#: owner page and this tuple are revised in the same change.
ACTIONS = ("scan", "record", "replay")

#: Every declared flag; an undeclared ``-*`` token is refused before any action runs.
DECLARED_OPTIONS = (
    "--workspace-root", "--format", "--presentation", "--reply", "--authorization",
    "--batch", "--version", "-h", "--help",
)

# --version and the undeclared-option refusal come from the one shared helper; a copy that
# lacks the helper still runs its actions (same pattern as validate-decisions.py).
_SIG_DIR = str(Path(__file__).resolve().parent)
if _SIG_DIR not in sys.path:
    sys.path.insert(0, _SIG_DIR)
try:
    from script_interface_cli import attach_to_parser_tree as _sig_attach
    from script_interface_cli import configure_parser as _sig_configure
    from script_interface_cli import guard_argv as _sig_guard
except ImportError:
    def _sig_configure(parser, **_kwargs):
        return parser

    def _sig_attach(parser, **_kwargs):
        return parser

    def _sig_guard(_argv=None, declared=None, **_kwargs):
        return None


def build_parser() -> argparse.ArgumentParser:
    """The closed action set with the declared flag surface on every action."""
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--workspace-root", default=".", metavar="PATH",
        help="the workspace the panel reads (default: the current directory)")
    common.add_argument(
        "--format", choices=("text", "json"), default="text",
        help="output format (default: text)")
    common.add_argument(
        "--presentation", metavar="PATH",
        help="the scan payload a reply is bound to (record)")
    common.add_argument(
        "--reply", metavar="PATH",
        help="the reply file carrying the user's verbatim text (record)")
    common.add_argument(
        "--authorization", choices=("interactive", "unattended"),
        help="caller-declared interaction authorization (record); "
             "missing is treated as unattended")
    common.add_argument(
        "--batch", metavar="PATH",
        help="the batch record to replay (replay)")

    parser = argparse.ArgumentParser(
        prog="decision-batch.py",
        description="Scan pending decision items, record one batch through the existing "
                    "carriers, and replay a recorded batch from its record alone.",
    )
    _sig_configure(
        parser,
        effects="scan and replay write nothing; record writes only through the named "
                "carriers (batch record, register rows/status cells, block resolution)",
        codes="0 success (including nothing-pending); 1 a documented refusal; "
              "2 usage or environment error",
    )
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("scan", parents=[common],
                   help="read-only: scan the closed source roster and present one batch")
    sub.add_parser("record", parents=[common],
                   help="the only writer: validate the reply and write the batch record")
    sub.add_parser("replay", parents=[common],
                   help="read-only: reconstruct a recorded batch from its record")
    _sig_attach(parser)
    return parser


def run_action(args: argparse.Namespace) -> int:
    """Dispatch one action. The cores land with their user-story packages."""
    print(
        f"decision-batch.py: action '{args.action}' is declared but not implemented in "
        "this build; its core lands with the owning user-story package",
        file=sys.stderr,
    )
    return EXIT_USAGE


def main(argv=None) -> int:
    _sig_guard(argv, declared=DECLARED_OPTIONS)
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    return run_action(args)


if __name__ == "__main__":
    raise SystemExit(main())