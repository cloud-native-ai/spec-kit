#!/usr/bin/env python3
"""closure-acceptance-check.py — the one deterministic answer to
"may this feature be called `Implemented`?".

Program-First discipline (`shared/guidelines/token-efficiency.md`): the question has a fixed,
decidable answer, so a program produces it and prints a verdict. No caller may decide it another
way — not a model judgement, not a different script, not an ad-hoc grep (contract
`contracts/gate-wiring.contract.md` GW-04).

Schema owner: `shared/workflow/acceptance-hardening.md` — § Closure Verdict (this program's
verdict, closed reason set, exit codes and `final_path` counts), § Verification Vocabulary (the
status set, the five measurement-ladder fields, the smoke record), § Feature Status (the claimed
status). This script **implements** those schemas; it never redefines them.

Calling surface (contract `contracts/closure-acceptance-check.contract.md` C-01…C-06, C-10):

  --spec-dir <dir>          REQUIRED. Holds requirements.md, plan.md, tasks.md, verification.md.
  --repo <root>             Repository root for repo-relative path resolution (default: the
                            checkout this script lives in).
  --feature-detail <path>   The claimed feature status, read from a feature detail file.
  --feature-registry <path> The claimed feature status, read from a registry file. Either flag
                            may be given; when neither is, the status is resolved from the
                            registry by the spec directory's key.
  --audit-existing          Read-only audit mode: report, write nothing, and let the exit code
                            reflect input validity only.
  --json                    Machine-readable payload on stdout.
  --json-out <path>         Write the identical payload to a file as well.
  --waive CODE:TARGET       Repeatable. Removes one reason from the blocking set while still
                            counting it as waived.

Exit codes (C-10): 0 = accept, 1 = block, 2 = an input is missing or unparsable. A missing input
is never reported as `block`, and in audit mode the exit code reflects input validity only.

IMPLEMENTATION STATE — read this before trusting an exit code
--------------------------------------------------------------
This is the **calling surface only** (slice 081a, task T006). Argument parsing, input resolution
and the exit-2 contract are implemented; the verdict computation is not, so a run whose inputs all
parse exits `2` with an explicit "verdict logic not implemented" message. That is deliberate: an
unfinished checker MUST NOT emit a fabricated `accept`, because a green check that would not go red
when its subject breaks proves nothing. The verdict lands with task T015, which fills `run()` and
leaves this surface unchanged.

Read-only and stdlib-only (C-01, V-14): no network, no model, no write — `--json-out` is the one
declared output file, and it is written only when a payload exists.

Usage:
  python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/<key>
  python3 scripts/python/closure-acceptance-check.py --spec-dir <dir> --feature-registry <path> --json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

EXIT_ACCEPT = 0
EXIT_BLOCK = 1
EXIT_INPUT = 2

#: Inputs the check cannot run without (C-02). Missing any of them is an input error, never a
#: `block`: the artifact is incomplete, which is a different fact from the feature failing.
REQUIRED_INPUTS = ("requirements.md", "plan.md", "tasks.md", "verification.md")

#: Resolved once so a `--json-out` relative path and an evidence path are read the same way.
_REPO_ROOT = Path(__file__).resolve().parents[2]
# Guard: invoked through the `.specify/scripts/python/` mirror, `parents[2]` is `.specify` and
# every repo-relative resolution would land inside `.specify/` instead of the checkout. A
# directory named `.specify` is never a repository root.
if _REPO_ROOT.name == ".specify":
    _REPO_ROOT = _REPO_ROOT.parent


class InputError(Exception):
    """An input is missing or unparsable — exit 2, never a verdict about the feature."""


class VerdictNotImplemented(Exception):
    """The calling surface exists and the inputs parsed; the judgement does not exist yet."""


def parse_waiver(raw):
    """`CODE:TARGET` → `(code, target)`, or an InputError.

    Shape only, in this slice: the code is everything before the first colon and the target is
    everything after it (a target may legitimately contain colons of its own — a relative path
    plus a line number is the sibling script's waiver shape). Membership of the code in the closed
    reason set is checked with the verdict logic, together with the waiver's effect.
    """
    code, sep, target = raw.partition(":")
    code = code.strip()
    target = target.strip()
    if not sep or not code or not target:
        raise InputError(
            "--waive expects CODE:TARGET with both halves non-empty, got %r" % raw
        )
    return code, target


def resolve_inputs(args):
    """Resolve and validate every declared input. Returns a dict of absolute paths.

    Every failure names the path or the argument, so the caller never has to guess which input
    the exit code was about (C-02).
    """
    if not args.spec_dir:
        raise InputError(
            "--spec-dir <dir> is required (no spec directory given); "
            "it must contain %s" % ", ".join(REQUIRED_INPUTS)
        )

    spec_dir = Path(os.path.abspath(args.spec_dir))
    if not spec_dir.is_dir():
        raise InputError("spec dir not found: %s" % spec_dir)

    resolved = {"spec_dir": spec_dir}
    for name in REQUIRED_INPUTS:
        path = spec_dir / name
        if not path.is_file():
            raise InputError("required input not found: %s" % path)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise InputError("required input is not readable as UTF-8: %s (%s)" % (path, exc))
        if not text.strip():
            raise InputError("required input is empty: %s" % path)
        resolved[name] = path

    repo = Path(os.path.abspath(args.repo)) if args.repo else _REPO_ROOT
    if not repo.is_dir():
        raise InputError("repo root not found: %s" % repo)
    resolved["repo"] = repo

    for flag, value in (("--feature-detail", args.feature_detail),
                        ("--feature-registry", args.feature_registry)):
        if value is None:
            continue
        path = Path(os.path.abspath(value))
        if not path.is_file():
            raise InputError("%s names a file that does not exist: %s" % (flag, path))
        resolved[flag] = path

    resolved["waivers"] = [parse_waiver(raw) for raw in (args.waive or [])]
    return resolved


def run(args):
    """Compute the record. Not implemented in slice 081a — see the module docstring.

    When it lands (T015) this function returns the payload the schema owner describes:
    `verdict`, `reasons[]`, `final_path` counts, `flow_class`. It never returns a verdict it
    cannot justify from the inputs.
    """
    resolve_inputs(args)
    raise VerdictNotImplemented(
        "input validation passed; verdict logic is not implemented in this slice "
        "(081a T006 landed the calling surface, T015 lands the judgement). "
        "Refusing to emit a verdict rather than emit a fabricated one."
    )


def emit(record, args, exit_code):
    """Print the payload and honour `--json` / `--json-out` (C-05).

    `record` is `None` in the not-implemented state, which writes no file at all.
    """
    if record is None:
        return
    payload = json.dumps(record, indent=2, ensure_ascii=False, sort_keys=True)
    if args.json:
        print(payload)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            handle.write(payload + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Deterministic closure verdict for a feature: may it be called Implemented?",
    )
    # `--spec-dir` is validated in resolve_inputs rather than by argparse's `required=True`, so
    # the exit-2 message names the path argument and the inputs it must carry (C-02) instead of
    # argparse's usage banner.
    parser.add_argument("--spec-dir", default="",
                        help="spec directory holding requirements/plan/tasks/verification")
    parser.add_argument("--repo", default="",
                        help="repository root for repo-relative path resolution")
    parser.add_argument("--feature-detail", default=None,
                        help="feature detail file carrying the claimed status")
    parser.add_argument("--feature-registry", default=None,
                        help="feature registry file carrying the claimed status")
    parser.add_argument("--audit-existing", action="store_true",
                        help="read-only audit mode; exit code reflects input validity only")
    parser.add_argument("--json", action="store_true",
                        help="machine-readable payload on stdout")
    parser.add_argument("--json-out", default="",
                        help="write the identical payload to this file")
    parser.add_argument("--waive", action="append", default=[], metavar="CODE:TARGET",
                        help="remove one reason from the blocking set, counting it as waived")
    args = parser.parse_args(argv)

    try:
        record = run(args)
    except InputError as exc:
        print("closure-acceptance-check: input error: %s" % exc, file=sys.stderr)
        return EXIT_INPUT
    except VerdictNotImplemented as exc:
        print("closure-acceptance-check: not implemented: %s" % exc, file=sys.stderr)
        return EXIT_INPUT

    exit_code = EXIT_ACCEPT if record["verdict"] == "accept" else EXIT_BLOCK
    emit(record, args, exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
