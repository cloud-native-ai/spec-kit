#!/usr/bin/env python3
"""Seal engine for `/speckit.seal` (requirement 099) — CLI skeleton (work package P2).

Owner of the four-action closed set, the three-value exit domain and the write-path
allowlist. The action bodies land in later work packages on top of this surface.

Actions (exactly four; a fifth MUST NOT appear):
  merge-plan     read-only   slice set, per-artifact actions, ID maps and conflicts
  merge-apply    write       deterministic merge into the parent spec, merge-manifest.json,
                             one `**Merged into**` line per slice
  seal           write       judgment first (read-only), then one atomic write batch:
                             seal.md + registry row + feature detail
  archive-gate   read-only   archive admission verdict (0 allow / 1 refuse / 2 input error)

Exit codes (exactly three; a fourth MUST NOT appear):
  0 success or idempotent (already-sealed included; an allowed archive-gate)
  1 a precondition refused (a read-only report is still complete)
  2 input or environment error (state-drift included; never read as a pass)

Two hats (C-009): the mirror position is decided by the LITERAL `.specify` component at
a fixed structural index of the engine's own resolved path — never by walking up to the
nearest `.specify` ancestor, a heuristic that self-matches in this repository. A mirror
copy refuses write actions (exit 2, reason `mirror-copy`): writing through the mirror
would break the byte-identical source/mirror pair.

Contract: `.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md` (C-001…C-010)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple

ENGINE_NAME = "seal-utils.py"

#: C-001: the action set is closed at exactly four values.
ACTIONS = ("merge-plan", "merge-apply", "seal", "archive-gate")
#: C-005: the two-phase declaration — which actions are pure judgments and which write.
READ_ONLY_ACTIONS = ("merge-plan", "archive-gate")
WRITE_ACTIONS = ("merge-apply", "seal")

#: C-002: the exit domain is closed at exactly three values.
EXIT_OK = 0
EXIT_REFUSED = 1
EXIT_INPUT_ERROR = 2
EXIT_CODES = (EXIT_OK, EXIT_REFUSED, EXIT_INPUT_ERROR)

#: C-010: the verdict a payload carries, and the exit code each verdict maps to.
VERDICTS = ("ok", "refused", "error")

#: C-009: the spec contract file that makes a directory a spec directory.
SPEC_CONTRACT_FILE = "requirements.md"

#: C-008: the write surface, as data. Any path the engine may write, relative to the
#: resolved roots; a new entry is a contract change, never an implementation detail.
WRITE_PATH_ALLOWLIST = (
    "{spec_dir}/seal.md",                 # E2 seal record
    "{spec_dir}/merge-manifest.json",     # E3 merge manifest
    "{spec_dir}/{merged_artifact}",       # E5 merged artifacts (file-level units)
    "{slice_dir}/requirements.md",        # E14 exactly one `**Merged into**` line
    "{factory_doc}",                      # C-017 recorded reference resolutions only
)

#: Stable condition codes for the engine-level (non-action) errors.
MIRROR_CODE = "mirror-copy"
SPEC_DIR_CODE = "spec-dir-invalid"
PENDING_CODE = "not-implemented"

#: C-004: the full declared option vocabulary (the pre-parse guard judges against it).
DECLARED_OPTIONS = ("--action", "--spec-dir", "--repo", "--feature-detail",
                    "--feature-registry", "--json")


# ---------------------------------------------------------------------------
# The guard helper (C-003): `--help` / `--version` zero-side-effect, unknown
# options rejected with 2 before any action. The rule lives in the helper.
# ---------------------------------------------------------------------------

def _import_guard():
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    try:
        from script_interface_cli import add_version_argument, configure_parser, guard_argv
        return configure_parser, guard_argv, add_version_argument
    except ImportError:  # a bare copy without the helper still runs its actions
        def _configure(parser, **_kwargs):
            return parser

        def _guard(_argv=None, declared=None, **_kwargs):
            return None

        def _add_version(parser):
            return parser

        return _configure, _guard, _add_version


_sig_configure, _sig_guard, _sig_add_version = _import_guard()


# ---------------------------------------------------------------------------
# Report rendering (C-006 / C-010): one payload, two renderings, stdout only
# ---------------------------------------------------------------------------

def _condition(code: str, evidence: str, fix_path: str, rerun: str) -> Dict[str, str]:
    return {"code": code, "evidence": evidence, "fix_path": fix_path, "rerun": rerun}


def _payload(action: Optional[str], spec_dir: Optional[Path], verdict: str,
             exit_code: int, conditions=None) -> Dict[str, Any]:
    return {
        "action": action,
        "spec_dir": str(spec_dir) if spec_dir is not None else None,
        "verdict": verdict,
        "exit_code": exit_code,
        "conditions": list(conditions or []),
    }


def render(payload: Dict[str, Any], as_json: bool) -> None:
    """Print the one judgment; the machine form is canonical (C-010)."""
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        return
    print("%s %s: %s (exit %d)" % (
        ENGINE_NAME, payload["action"], payload["verdict"], payload["exit_code"]))
    for condition in payload["conditions"]:
        print("  - %s: %s" % (condition["code"], condition["evidence"]))
        print("    fix: %s" % condition["fix_path"])
        print("    rerun: %s" % condition["rerun"])


# ---------------------------------------------------------------------------
# Path resolution (C-009): explicit paths only, fixed structural signal
# ---------------------------------------------------------------------------

def is_mirror_copy(self_path: Optional[Path] = None) -> bool:
    """Whether this engine is the `<repo>/.specify/scripts/python/` mirror copy.

    The signal is the literal `.specify` component at the fixed index that the mirror
    position dictates (`scripts/python/<name>.py` sits directly under it). Walking up
    to the nearest `.specify` ancestor is forbidden: the worktree itself may live under
    `.specify/.tmp/...`, and that heuristic would misclassify the framework source.
    """
    path = Path(self_path if self_path is not None else __file__).resolve()
    parents = path.parents
    return len(parents) >= 3 and parents[2].name == ".specify"


def resolve_spec_dir(raw: str) -> Optional[Path]:
    """Resolve `--spec-dir` against the invocation cwd; require a spec directory shape.

    The shape is `requirements.md` presence only — never a `^\\d{3}-` name prefix.
    """
    path = Path(raw)
    if not path.is_absolute():
        path = Path.cwd() / path
    path = path.resolve()
    if not path.is_dir():
        return None
    if not (path / SPEC_CONTRACT_FILE).is_file():
        return None
    return path


# ---------------------------------------------------------------------------
# Actions (closed dispatch; bodies land in later work packages)
# ---------------------------------------------------------------------------

def _pending(action: str, spec_dir: Optional[Path]) -> Tuple[Dict[str, Any], int]:
    return _payload(
        action, spec_dir, "error", EXIT_INPUT_ERROR,
        [_condition(
            PENDING_CODE,
            "the %s action body is not implemented on this skeleton" % action,
            "run the action once its implementing work package lands",
            "rerun the same command after the action body is implemented",
        )],
    ), EXIT_INPUT_ERROR


def action_merge_plan(args: argparse.Namespace, spec_dir: Path) -> Tuple[Dict[str, Any], int]:
    return _pending("merge-plan", spec_dir)


def action_merge_apply(args: argparse.Namespace, spec_dir: Path) -> Tuple[Dict[str, Any], int]:
    return _pending("merge-apply", spec_dir)


def evaluate_seal(args: argparse.Namespace, spec_dir: Path) -> Tuple[Dict[str, Any], int]:
    """C-005 judgment phase: read-only; computes every precondition, writes nothing."""
    return _pending("seal", spec_dir)


def apply_seal(args: argparse.Namespace, spec_dir: Path,
               evaluation: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    """C-005 write phase: one atomic batch; only reached when judgment passed."""
    return _pending("seal", spec_dir)


def action_seal(args: argparse.Namespace, spec_dir: Path) -> Tuple[Dict[str, Any], int]:
    evaluation, code = evaluate_seal(args, spec_dir)
    if evaluation["verdict"] != "ok":
        return evaluation, code
    return apply_seal(args, spec_dir, evaluation)


def action_archive_gate(args: argparse.Namespace, spec_dir: Path) -> Tuple[Dict[str, Any], int]:
    return _pending("archive-gate", spec_dir)


HANDLERS = {
    "merge-plan": action_merge_plan,
    "merge-apply": action_merge_apply,
    "seal": action_seal,
    "archive-gate": action_archive_gate,
}


# ---------------------------------------------------------------------------
# CLI surface (C-003 / C-004) and dispatch
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=ENGINE_NAME,
        description="Seal engine for /speckit.seal: merge-back, seal judgment and "
                    "archive admission.",
    )
    _sig_configure(
        parser,
        effects="merge-plan and archive-gate write nothing; merge-apply and seal write "
                "only within the allowlisted paths (the parent spec directory, one slice "
                "requirements.md marker line and recorded factory-doc resolutions); a "
                "flag-only invocation writes nothing",
        codes="0 success or idempotent; 1 a precondition refused; 2 an input or "
              "environment error",
    )
    parser.add_argument("--action", required=True, choices=ACTIONS,
                        help="one of the four closed actions")
    parser.add_argument("--spec-dir", required=True,
                        help="target spec directory (required, no default)")
    parser.add_argument("--repo", default=None,
                        help="repository root for state and registry lookups "
                             "(default: the invocation cwd)")
    parser.add_argument("--feature-detail", default=None,
                        help="override the feature-detail carrier path (test fixtures only)")
    parser.add_argument("--feature-registry", default=None,
                        help="override the feature-registry path (test fixtures only)")
    parser.add_argument("--json", action="store_true",
                        help="emit one stable JSON payload instead of the human rendering")
    _sig_add_version(parser)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    line = list(sys.argv[1:] if argv is None else argv)
    _sig_guard(line, declared=DECLARED_OPTIONS)
    parser = build_parser()
    args = parser.parse_args(line)

    if args.action in WRITE_ACTIONS and is_mirror_copy():
        payload = _payload(
            args.action, None, "error", EXIT_INPUT_ERROR,
            [_condition(
                MIRROR_CODE,
                "this engine is the .specify/scripts/python/ mirror copy; write actions "
                "MUST run from the framework source to keep the pair byte-identical",
                "run scripts/python/seal-utils.py from the framework source tree",
                "rerun the same command against the framework source copy",
            )],
        )
        render(payload, args.json)
        return EXIT_INPUT_ERROR

    spec_dir = resolve_spec_dir(args.spec_dir)
    if spec_dir is None:
        payload = _payload(
            args.action, None, "error", EXIT_INPUT_ERROR,
            [_condition(
                SPEC_DIR_CODE,
                "not a spec directory (missing, or carries no %s): %s"
                % (SPEC_CONTRACT_FILE, args.spec_dir),
                "pass --spec-dir pointing at a directory that contains %s"
                % SPEC_CONTRACT_FILE,
                "rerun the same command with a corrected --spec-dir",
            )],
        )
        render(payload, args.json)
        return EXIT_INPUT_ERROR

    payload, code = HANDLERS[args.action](args, spec_dir)
    render(payload, args.json)
    return code


if __name__ == "__main__":
    sys.exit(main())
