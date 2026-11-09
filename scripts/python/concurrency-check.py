#!/usr/bin/env python3
"""The concurrency judgement engine (feature 093-concurrency-by-default).

The one program that turns the concurrency declaration facts into verdicts. It is
read-only over the repository, standard-library only, and writes nothing except the
file named by ``--json-out``.

Contracts this engine implements (clause ids are owned by
``.specify/specs/093-concurrency-by-default/contracts/judgement-engine.contract.md``):

* C-019 — ``-h`` / ``--help`` and ``--version`` answer without acting; an undeclared
  option exits 2 before any action; the exit taxonomy is exactly 0 = pass,
  1 = a documented check failed, 2 = input or environment error.
* C-020 — exactly five read-only actions: ``classify`` / ``serial-reason`` /
  ``reading`` / ``coverage`` / ``capability``.
* C-021 — every action accepts ``--repo <root>`` (default resolved from this file's
  own location, never an ancestor walk) and ``--json-out <file>`` (the only write);
  the three record-judging actions require ``--record <file>`` and an action invoked
  without its record flag exits 2.
* C-022 — every action emits the JSON envelope ``action`` / ``decision`` /
  ``findings`` / ``measured`` / ``checked_at``; a ``not-applicable`` decision is
  distinguishable from ``pass``.

The facts are read through ``scripts/python/declaration_reader.py`` (the single
declaration read entry); no class name, root pattern, code vocabulary or threshold is
carried in this file as a second definition.

Usage:
  python3 scripts/python/concurrency-check.py <action> [options]

  actions:
    classify       map execution bodies to their declared class (needs no record)
    serial-reason  judge one serial-reason record (needs --record)
    reading        judge one concurrency reading record (needs --record)
    coverage       judge per-stage decomposition coverage and goal-target partitions
    capability     judge dispatch capability and the coordinator verdict (needs --record)

  options:
    --repo PATH        repository root whose shared/declarations/ is read
                       (default: resolved from this script's own location)
    --record PATH      the record to judge (serial-reason / reading / capability)
    --json-out PATH    write the judgement envelope here (the only write)
    --stage NAME       coverage: judge one stage from decomposition-coverage.yaml
    --goal SLUG        coverage: judge one goal's target partition
    --ceiling N        reading/coverage: the slot cap ceiling at call time
                       (default: read from wp-gate.py's declared default)

Exit codes:
  0  the judgement passed
  1  a documented check failed (decision ``fail``)
  2  input or environment error, or no owner verdict readable
     (decision ``owner-unavailable`` / ``not-applicable``)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_NAME = "concurrency-check.py"

#: C-020's closed action set. A sixth action MUST NOT be added without a clause revision.
ACTIONS = ("classify", "serial-reason", "reading", "coverage", "capability")

#: The three record-judging actions (C-021). The other two take no record flag.
RECORD_ACTIONS = ("serial-reason", "reading", "capability")

#: E-4's closed pattern domain (data-model.md). Two literals, because the pattern is a
#: record field, not a declaration-layer value.
PATTERNS = ("concurrent", "serial")

#: Tool names that constitute a dispatch tool (FR-021(a), [[STR-004]]). The concept's
#: definition owner is ``shared/definitions/subagent-definitions.md``; this set is the
#: engine's executable spelling of the host tool names that create sibling executors.
DISPATCH_TOOLS = frozenset({"agent", "task", "subagent", "dispatch", "spawn_agent"})

#: Marker words an explicit handoff declaration carries (FR-021(b)); matched
#: case-insensitively in the body text.
HANDOFF_MARKERS = ("handoff", "hands off", "hand-off", "移交派发", "移交")

#: Marker words an external-process declaration carries (FR-021(c) / C-094).
EXTERNAL_PROCESS_MARKERS = (
    "external-process", "external process", "subprocess", "child process",
    "外部进程", "子进程", "stage-runner",
)


# --------------------------------------------------------------------------- #
# the script-interface helper (C-019 / Constitution XXI)
# --------------------------------------------------------------------------- #
_SIG_DIR = str(Path(__file__).resolve().parent)
if _SIG_DIR not in sys.path:
    sys.path.insert(0, _SIG_DIR)
try:  # the helper owns the rule; a sandbox copy without it still runs the actions
    from script_interface_cli import configure_parser as _sig_configure
    from script_interface_cli import guard_argv as _sig_guard
except ImportError:  # pragma: no cover - a handler copy carries the engine but not the helper
    def _sig_configure(parser, **_kwargs):
        return parser

    def _sig_guard(_argv=None, declared=None, **_kwargs):
        return None

# --------------------------------------------------------------------------- #
# the declaration read entry (the single fact reader)
# --------------------------------------------------------------------------- #
try:
    import declaration_reader
except ImportError:  # pragma: no cover - defensive; the sibling always ships together
    declaration_reader = None


class EngineInputError(Exception):
    """An input or environment error (exit 2) with a stable code for the envelope."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


# --------------------------------------------------------------------------- #
# repository resolution (C-021 / T023 — never an ancestor walk)
# --------------------------------------------------------------------------- #
def default_repo():
    """The repository root derived from this engine's own location.

    Framework source form: ``<root>/scripts/python/concurrency-check.py``.
    Mirror form: ``<root>/.specify/scripts/python/concurrency-check.py`` — the literal
    ``.specify`` component directly above ``scripts/`` is stripped. This is the
    F-093-002 path trap's required shape: a worktree that itself lives under
    ``.specify/.tmp/...`` still resolves to the worktree root, because the component
    below ``scripts/`` is what is read, never the first ``.specify`` anywhere above.
    """
    parts = Path(__file__).resolve().parts
    if len(parts) >= 3 and parts[-3:-1] == ("scripts", "python"):
        root = Path(*parts[:-3])
        if root.name == ".specify":
            root = root.parent
        return root
    return Path(__file__).resolve().parent


def resolve_repo(value):
    """The ``--repo`` root as given (never walked), or the derived default."""
    root = Path(value) if value else default_repo()
    root = root.resolve()
    if not root.is_dir():
        raise EngineInputError("repo-unavailable", "repo root does not exist: %s" % root)
    return root


# --------------------------------------------------------------------------- #
# fact loading
# --------------------------------------------------------------------------- #
def load_fact(repo, slug):
    """One fact body through the declaration reader; absence is the typed exit-2 case."""
    if declaration_reader is None:
        raise EngineInputError("declaration-reader-unavailable",
                               "declaration_reader.py is not importable beside this engine")
    try:
        return declaration_reader.load_fact(repo, slug)["body"]
    except declaration_reader.DeclarationError as error:
        raise EngineInputError("owner-unavailable", str(error))


def fact_statement(body, slug):
    statement = body.get("statement")
    if not isinstance(statement, dict):
        raise EngineInputError(
            "owner-unavailable", "fact %r carries no readable statement mapping" % slug)
    return statement


def load_record(path):
    """Parse a record through the same block subset the declaration layer accepts (T109).

    A run cannot smuggle a shape the declaration layer would reject: the record is
    parsed by ``declaration_reader.parse_subset``, the single subset implementation.
    """
    if declaration_reader is None:
        raise EngineInputError("declaration-reader-unavailable",
                               "declaration_reader.py is not importable beside this engine")
    if not path:
        raise EngineInputError("record-required", "--record is required for this action")
    record_path = Path(path)
    try:
        text = record_path.read_text(encoding="utf-8")
    except OSError as error:
        raise EngineInputError(
            "record-unreadable", "cannot read record %s (%s)" % (path, error.strerror or error))
    try:
        body = declaration_reader.parse_subset(text, str(record_path))
    except declaration_reader.DeclarationError as error:
        raise EngineInputError("record-outside-subset", str(error))
    if not isinstance(body, dict):
        raise EngineInputError(
            "record-malformed",
            "record %s must be a block mapping (block-subset/v1), got %s"
            % (path, type(body).__name__))
    return body


# --------------------------------------------------------------------------- #
# the judgement envelope (C-022)
# --------------------------------------------------------------------------- #
def finding(code, subject, message, evidence_ptr="", **detail):
    """One finding: the four mandatory fields plus optional comparison detail (T097)."""
    item = {
        "code": code,
        "subject": subject,
        "message": message,
        "evidence_ptr": evidence_ptr,
    }
    item.update(detail)
    return item


def envelope(action, decision, findings, measured, **extra):
    """The stable envelope C-022 fixes. ``checked_at`` is ISO-8601 UTC."""
    body = {
        "action": action,
        "decision": decision,
        "findings": findings,
        "measured": measured,
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    body.update(extra)
    return body


def emit(envelope_body, json_out):
    """Write the envelope to ``--json-out`` (the only write) or print it to stdout."""
    text = json.dumps(envelope_body, ensure_ascii=False, indent=2, sort_keys=True)
    if json_out:
        out = Path(json_out)
        try:
            out.write_text(text + "\n", encoding="utf-8")
        except OSError as error:
            raise EngineInputError(
                "json-out-unwritable",
                "cannot write --json-out %s (%s)" % (out, error.strerror or error))
        print("%s: decision=%s findings=%d -> %s"
              % (envelope_body["action"], envelope_body["decision"],
                 len(envelope_body["findings"]), out))
    else:
        print(text)


def decision_exit(decision):
    """The exit taxonomy (C-019): pass 0, fail 1, owner-unavailable / input 2."""
    if decision == "pass":
        return 0
    if decision == "fail":
        return 1
    return 2


# --------------------------------------------------------------------------- #
# actions (stubs until each row group lands; the dispatch table itself is C-020)
# --------------------------------------------------------------------------- #
def _not_implemented(action):
    return envelope(
        action, "fail",
        [finding("not-implemented", action, "action %r is not implemented yet" % action)],
        {})


def action_classify(repo, args):
    return _not_implemented("classify")


def action_serial_reason(repo, args):
    return _not_implemented("serial-reason")


def action_reading(repo, args):
    return _not_implemented("reading")


def action_coverage(repo, args):
    return _not_implemented("coverage")


def action_capability(repo, args):
    return _not_implemented("capability")


DISPATCH = {
    "classify": action_classify,
    "serial-reason": action_serial_reason,
    "reading": action_reading,
    "coverage": action_coverage,
    "capability": action_capability,
}


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser():
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=(
            "The concurrency judgement engine: classify bodies, judge serial reasons, "
            "readings, per-stage coverage and dispatch capability from the declaration "
            "facts (owner: shared/declarations/facts/)."
        ),
    )
    _sig_configure(
        parser,
        effects="reads the repository; writes only the file named by --json-out",
        codes="0 the judgement passed; 1 a documented check failed; "
              "2 input or environment error, or no owner verdict readable",
    )
    parser.add_argument("action", choices=ACTIONS,
                        help="the read-only action to run")
    parser.add_argument("--repo", default=None,
                        help="repository root whose shared/declarations/ is read "
                             "(default: resolved from this script's own location)")
    parser.add_argument("--record", default=None,
                        help="the record to judge (serial-reason / reading / capability)")
    parser.add_argument("--json-out", default=None,
                        help="write the judgement envelope here (the only write)")
    parser.add_argument("--stage", default=None,
                        help="coverage: judge one stage from decomposition-coverage.yaml")
    parser.add_argument("--goal", default=None,
                        help="coverage: judge one goal's target partition")
    parser.add_argument("--ceiling", type=int, default=None,
                        help="reading/coverage: the slot cap ceiling at call time "
                             "(default: read from wp-gate.py's declared default)")
    return parser


def main(argv=None):
    line = list(sys.argv[1:] if argv is None else argv)
    _sig_guard(line, declared=["--repo", "--record", "--json-out", "--stage",
                               "--goal", "--ceiling"])
    parser = build_parser()
    args = parser.parse_args(line)

    json_out = args.json_out
    try:
        repo = resolve_repo(args.repo)
        if args.action in RECORD_ACTIONS and not args.record:
            raise EngineInputError(
                "record-required", "action %r requires --record <file>" % args.action)
        if args.action not in RECORD_ACTIONS and args.record:
            raise EngineInputError(
                "record-not-applicable",
                "action %r takes no --record flag (C-021)" % args.action)
        result = DISPATCH[args.action](repo, args)
    except EngineInputError as error:
        decision = ("owner-unavailable" if error.code == "owner-unavailable"
                    else "not-applicable")
        result = envelope(args.action, decision,
                          [finding(error.code, str(args.repo or ""), error.message)],
                          {})
        try:
            emit(result, json_out)
        except EngineInputError as emit_error:
            print("error: %s" % emit_error.message, file=sys.stderr)
        return 2
    try:
        emit(result, json_out)
    except EngineInputError as emit_error:
        print("error: %s" % emit_error.message, file=sys.stderr)
        return 2
    return decision_exit(result["decision"])


if __name__ == "__main__":
    sys.exit(main())
