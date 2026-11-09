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


# --------------------------------------------------------------------------- #
# enumeration and body reading (classify)
# --------------------------------------------------------------------------- #
def expand_braces(pattern):
    """Expand ``{a,b}`` alternatives in a declaration pattern (one level, nested-safe)."""
    match = re.search(r"\{([^{}]+)\}", pattern)
    if not match:
        return [pattern]
    expanded = []
    for option in match.group(1).split(","):
        expanded.extend(
            expand_braces(pattern[:match.start()] + option.strip() + pattern[match.end():]))
    return expanded


def expand_root_pattern(pattern):
    """``[(base, selector)]`` for one declaration pattern.

    The roots fact declares PATH PATTERNS, never counts (V-4). Two placeholder forms
    occur: ``<name>/`` (a directory child) and ``<stem>.md`` (a file-glob child); a
    literal ``*`` segment is a glob as written. The engine expands whatever the fact
    says and hard-codes no root path.
    """
    selectors = []
    for alternative in expand_braces(str(pattern).strip()):
        alternative = alternative.rstrip("/")
        placeholder = re.search(r"<[^>]+>", alternative)
        if placeholder:
            head = alternative[:placeholder.start()].rstrip("/")
            rest = alternative[placeholder.end():]
            if not rest:
                selectors.append((head or ".", "dir"))
            else:
                selectors.append((head or ".", "*" + rest))
            continue
        base, _, last = alternative.rpartition("/")
        selectors.append((base or ".", last))
    return selectors


def enumerate_root(repo, root):
    """Enumerate one root's members: ``[(relative-path, is_dir, base)]``, sorted."""
    members = []
    exclusions = [str(layer).strip().rstrip("/")
                  for layer in (root.get("excluded_layers") or [])]
    for base, selector in expand_root_pattern(root.get("pattern", "")):
        base_path = repo / base
        if not base_path.is_dir():
            continue
        if selector == "dir":
            candidates = sorted(p for p in base_path.iterdir() if p.is_dir())
        else:
            candidates = sorted(p for p in base_path.glob(selector) if p.is_file())
        for path in candidates:
            if path.name.startswith(".") or path.name == "__pycache__":
                continue
            rel = path.relative_to(repo).as_posix()
            if any(rel == layer or rel.startswith(layer + "/") for layer in exclusions):
                continue
            members.append((rel, path.is_dir(), base))
    return sorted(members)


def read_body_text(repo, rel, is_dir):
    """The body's own text: the file itself, or every markdown file of a directory member."""
    path = repo / rel
    try:
        if not is_dir:
            return path.read_text(encoding="utf-8")
        chunks = []
        for markdown in sorted(path.rglob("*.md")):
            chunks.append(markdown.read_text(encoding="utf-8"))
        return "\n".join(chunks)
    except (OSError, UnicodeDecodeError) as error:
        raise EngineInputError(
            "body-unreadable", "cannot read body %s (%s)" % (rel, error))


def frontmatter_value(text, key):
    """One scalar from the leading ``---`` frontmatter block, or ``None``."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        head, sep, value = line.partition(":")
        if sep and head.strip() == key:
            return value.strip().strip("\"'")
    return None


def resolve_anchor(repo, anchor):
    """``(path, fragment, resolved, detail)`` for a class ``owner_anchor`` value.

    A file path or a ``path#fragment`` pair. Resolution: the file exists (framework
    source form first, then its ``.specify/`` projection) and, when a fragment is
    given, a heading line carries it (``# class-<fragment>``-style section) or an
    explicit ``{#<fragment>}`` / ``id="<fragment>"`` marker does. An unresolvable
    anchor is reported, never assumed to hold the obligation.
    """
    text = str(anchor or "").strip()
    if not text:
        return "", "", False, "no owner_anchor declared"
    path_text, _, fragment = text.partition("#")
    candidates = [repo / path_text]
    if path_text.startswith(".specify/"):
        candidates.append(repo / path_text[len(".specify/"):])
    else:
        candidates.append(repo / ".specify" / path_text)
    target = next((c for c in candidates if c.is_file()), None)
    if target is None:
        return path_text, fragment, False, "anchor file does not resolve: %s" % path_text
    if not fragment:
        return path_text, fragment, True, "anchor file resolves"
    try:
        anchor_text = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return path_text, fragment, False, "anchor file unreadable: %s" % path_text
    heading = re.compile(r"^#{1,6}\s+.*%s.*$" % re.escape(fragment), re.MULTILINE)
    marker = re.compile(r"(\{#%s\}|id=[\"']%s[\"'])" % (re.escape(fragment), re.escape(fragment)))
    if heading.search(anchor_text):
        return path_text, fragment, True, "anchor heading resolves: #%s" % fragment
    if marker.search(anchor_text):
        return path_text, fragment, True, "anchor marker resolves: #%s" % fragment
    return path_text, fragment, False, "anchor section #%s not found in %s" % (fragment, path_text)


def resolve_body_class(root_id, body_text, rule_rows, class_names):
    """SM-3's class resolution for one body under one root.

    Returns ``(class_name, finding_code, detail)``. A single decision-rule row for the
    root assigns its class. Multiple rows require the body's declared produced shape
    (frontmatter ``produced-shape``); the shape must select exactly one row, else the
    body is ``uncovered`` (undecidable) or ``ambiguous`` (two class members). No rule
    row is ``uncovered``. Nothing falls into a catch-all member (C-024).
    """
    rows = [row for row in rule_rows if str(row.get("root_id", "")).strip() == root_id]
    if not rows:
        return None, "uncovered", "no decision-rule row for root %r" % root_id
    if len(rows) == 1:
        name = str(rows[0].get("class", "")).strip()
        if name not in class_names:
            return None, "class-unknown", "rule names class %r absent from the class table" % name
        return name, None, "single decision-rule row"
    shape = frontmatter_value(body_text, "produced-shape") or frontmatter_value(
        body_text, "produced_shape")
    if not shape:
        return None, "uncovered", (
            "%d decision-rule rows for root %r and no readable produced-shape" % (len(rows), root_id))
    matching = [row for row in rows
                if str(row.get("produced_shape", "")).strip() == shape]
    if len(matching) == 1:
        name = str(matching[0].get("class", "")).strip()
        if name not in class_names:
            return None, "class-unknown", "rule names class %r absent from the class table" % name
        return name, None, "produced shape %r selects one row" % shape
    if len(matching) > 1:
        names = [str(row.get("class", "")).strip() for row in matching]
        return None, "ambiguous", (
            "produced shape %r matches %d class members: %s" % (shape, len(matching), names))
    return None, "uncovered", "produced shape %r matches no decision-rule row" % shape


def action_classify(repo, args):
    """C-023…C-026: enumerate the five roots and judge every body's class and obligation."""
    roots_statement = fact_statement(load_fact(repo, "executor-enumeration-roots"),
                                     "executor-enumeration-roots")
    class_statement = fact_statement(load_fact(repo, "concurrency-class"),
                                     "concurrency-class")
    classes = class_statement.get("classes") or []
    class_names = {str(c.get("name", "")).strip() for c in classes if isinstance(c, dict)}
    class_table = {str(c.get("name", "")).strip(): c for c in classes if isinstance(c, dict)}
    rule_rows = class_statement.get("decision_rule") or []
    roots = roots_statement.get("roots") or []

    findings = []
    measured_roots = {}
    measured_bodies = []
    for root in roots:
        if not isinstance(root, dict):
            continue
        root_id = str(root.get("root_id", "")).strip()
        members = enumerate_root(repo, root)
        by_base = {}
        for rel, _is_dir, base in members:
            by_base[base] = by_base.get(base, 0) + 1
        measured_roots[root_id] = {
            "pattern": str(root.get("pattern", "")),
            "member_count": len(members),
            "by_base": by_base,
            "member_ids": [rel for rel, _d, _b in members],
        }
        applies = [str(c.get("name", "")).strip() for c in classes
                   if isinstance(c, dict) and root_id in (c.get("applies_to") or [])]
        for rel, is_dir, _base in members:
            body_text = read_body_text(repo, rel, is_dir)
            name, problem, detail = resolve_body_class(
                root_id, body_text, rule_rows, class_names)
            body_id = "%s/%s" % (root_id, rel)
            record = {"unit": body_id, "path": rel, "root": root_id,
                      "class": name, "resolution": detail}
            if problem:
                findings.append(finding(
                    problem, body_id, detail, rel,
                    compared=[applies, [str(r.get("class", "")) for r in rule_rows
                                        if str(r.get("root_id", "")) == root_id]]))
                measured_bodies.append(record)
                continue
            if applies and name not in applies:
                findings.append(finding(
                    "class-disagreement", body_id,
                    "applies_to %s and the decision rule %r disagree" % (applies, name),
                    rel, compared=[applies, name]))
            # obligation presence (C-025): the body's own text or the class's owner anchor
            entry = class_table.get(name, {})
            anchor = str(entry.get("owner_anchor", ""))
            anchor_path, fragment, anchor_ok, anchor_detail = resolve_anchor(repo, anchor)
            tokens = [name, anchor, anchor_path,
                      fragment and "#" + fragment, fragment]
            in_body = any(token and token in body_text for token in tokens)
            source = ("both" if (in_body and anchor_ok) else
                      "body-text" if in_body else
                      "owner-anchor" if anchor_ok else "none")
            record.update({
                "obligation": {
                    "class_obligation": str(entry.get("obligation", "")),
                    "in_body": in_body,
                    "anchor_resolves": anchor_ok,
                    "anchor": anchor,
                    "anchor_detail": anchor_detail,
                    "source": source,
                }
            })
            if source == "none":
                findings.append(finding(
                    "obligation-missing", body_id,
                    "class %r obligation is readable neither in the body nor at %r (%s)"
                    % (name, anchor, anchor_detail), rel,
                    compared=[name, anchor]))
            measured_bodies.append(record)

    if not roots:
        findings.append(finding("uncovered", "roots", "the roots fact declares no roots"))
    decision = "fail" if findings else "pass"
    measured = {
        "roots": measured_roots,
        "total_bodies": sum(r["member_count"] for r in measured_roots.values()),
        "bodies": measured_bodies,
    }
    return envelope("classify", decision, findings, measured)


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
