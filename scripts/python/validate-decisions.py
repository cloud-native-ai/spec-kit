#!/usr/bin/env python3
"""validate-decisions.py — read-only deterministic checker for decision governance (Feature 107).

The propositions judged here are fixed, textual and decidable, so a program judges them and
prints a verdict. The vocabulary, the class presentation, the option-set contract, the record
field closure, the transmission obligations and the M/B boundary are owned by
``shared/definitions/decision-definitions.md`` — this checker consumes them and never
restates them.

Actions (the declared interface; judgement legs land with their user stories):
  records     judge decision records in their carriers (M-01…M-04, M-08, M-09)
  payload     judge decision-backed dispatch payloads (M-06)
  chain       judge the record → dispatch attempt → implementation-receipt chain (M-05, M-07)
  inventory   judge the closed Decision Producer Inventory (FR-003)

Options:
  --action {records,payload,chain,inventory}   required; the judgement to run
  --spec PATH          the spec directory holding the carrier files
  --carrier PATH       a decision-record carrier file; repeatable
  --fixture PATH       a fixture directory or file to judge
  --register PATH      the register file that indexes ``D-NNN`` ids
  --glossary PATH      the glossary file whose variant rows M-08 consults
  --json               machine-readable output
  -h / --help          this body (same body for both spellings), exit 0
  --version            one line ``<script-name> <framework-version>``, exit 0

Exit codes: 0 = every judged check passed / 1 = a documented check failed /
2 = input or argument error (including a declared action not implemented yet).

Read-only: no write point of any kind, no resident process, standard library only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_CHECK_FAILED = 1
EXIT_INPUT = 2

#: The closed declared action set (C-404 / T007). A fifth value MUST NOT be accepted before
#: the owner page and this tuple are revised in the same change.
ACTIONS = ("records", "payload", "chain", "inventory")

#: Every option the parser accepts, for the pre-parse guard (an undeclared ``-*`` token is
#: refused before any action runs — ``shared/definitions/script-interface-definitions.md`` § 4).
DECLARED_OPTIONS = (
    "--action", "--spec", "--carrier", "--fixture", "--register", "--glossary", "--json",
)


def repo_root(start=None) -> Path:
    """The enclosing repository root, resolved from this file's own path.

    ``scripts/python/validate-decisions.py`` → the repository root is two levels up. The
    ``.specify/scripts/python/`` mirror copy would resolve to ``.specify``; a directory
    named ``.specify`` is never a repository root, so the guard steps one level further.
    """
    here = Path(start) if start is not None else Path(__file__)
    root = here.resolve().parents[2]
    if root.name == ".specify":
        root = root.parent
    return root


REPO_ROOT = repo_root()

# --version and the undeclared-option refusal come from the one shared helper; a copy that
# lacks the helper still runs its actions (same pattern as validate-decision-tensions.py).
_SIG_DIR = str(Path(__file__).resolve().parent)
if _SIG_DIR not in sys.path:
    sys.path.insert(0, _SIG_DIR)
try:
    from script_interface_cli import configure_parser as _sig_configure
    from script_interface_cli import guard_argv as _sig_guard
except ImportError:
    def _sig_configure(parser, **_kwargs):
        return parser

    def _sig_guard(_argv=None, declared=None, **_kwargs):
        return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validate-decisions.py",
        description="Judge the deterministic propositions of decision items, decision "
                    "records, transmission payloads and the closed producer inventory.",
    )
    _sig_configure(
        parser,
        effects="none; the checker is read-only — every action writes no file",
        codes="0 all judged checks passed; 1 a documented check failed; "
              "2 input or argument error",
    )
    parser.add_argument("--action", required=True, choices=ACTIONS,
                        help="the judgement to run")
    parser.add_argument("--spec", metavar="PATH",
                        help="the spec directory holding the carrier files")
    parser.add_argument("--carrier", metavar="PATH", action="append", default=[],
                        help="a decision-record carrier file (repeatable)")
    parser.add_argument("--fixture", metavar="PATH",
                        help="a fixture directory or file to judge")
    parser.add_argument("--register", metavar="PATH",
                        help="the register file that indexes D-NNN ids")
    parser.add_argument("--glossary", metavar="PATH",
                        help="the glossary file whose variant rows the subject check consults")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    return parser


def main(argv=None) -> int:
    _sig_guard(argv, declared=DECLARED_OPTIONS)
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    # Interface final, judgement legs pending: every declared action reports
    # not-implemented and exits as an input error, so an unimplemented check can never be
    # mistaken for a pass. The legs land with US1–US5 of feature 107.
    if args.json:
        print(json.dumps({"action": args.action, "status": "not-implemented",
                          "root": str(REPO_ROOT)}, ensure_ascii=False))
    print("error: action %r is declared but not implemented yet (read-only skeleton)"
          % args.action, file=sys.stderr)
    return EXIT_INPUT


if __name__ == "__main__":
    sys.exit(main())
