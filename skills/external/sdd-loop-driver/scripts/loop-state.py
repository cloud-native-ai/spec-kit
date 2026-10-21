#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""loop-state.py — read-only loop state snapshot engine (Feature 065 / Slice 065a).

One deterministic, read-only call aggregates: state spine, Line Registry entry,
pid/status/log/heartbeat four-piece signals, watchbeat marker, stage artifacts,
git commit evidence and the watcher verdict when obtainable. Emits a single
JSON envelope (schema_version: 1). This slice implements `snapshot`,
`--probe` and `--self-test`; `recover` and `check-spine` return structured
refusals (recover -> 065c, check-spine -> 065b, per notes/decomposition-gate.md).

Read-only boundary: the only write path is an explicit --out file, which must
resolve outside the state dir and the repo working tree (realpath before any
temp file is created; atomic replace via a same-directory temp file).

Derived loop_state mapping: the SINGLE OWNER is slice requirements.md FR-004
(parent #FR-004). The mapping implemented below is a mirror of that table;
references/state-awareness.md mirrors it too. Nothing here claims ownership of
the table (contract test pins this attribution).

Thresholds: start-grace / deadline-grace / heartbeat-max-age defaults are owned
by scripts/watch-target.sh (--help "Defaults:" line). This engine never embeds
a second set of numbers; when discovery fails the value stays unknown and the
dependent checks do not fire. retry_limit default is owned by
references/stage-prompts.md § Stall Handling.

Exit codes: 0 / 1 / 2 only (see --help). Watcher verdict codes (10-16) are
data recorded in watch_verdict.exit_code, never reused as this CLI's code.

Python >= 3.8, standard library only. No daemon, no network, no polling.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1

EXIT_OK = 0          # evaluation succeeded (any loop_state is data)
EXIT_REFUSED = 1     # refused / validation failed (unimplemented action refusal)
EXIT_USAGE = 2       # argument error or unreadable required CLI input

WATCHER_EXIT_CODES = "10-16"  # data only; owner: watch-target.sh --help

# Refusal ownership per action (C-2): check-spine -> 065b, recover -> 065c.
REFUSAL_OWNER = {"recover": "065c", "check-spine": "065b"}

# retry_limit default — owner: references/stage-prompts.md § Stall Handling
# ("同阶段重试上限缺省 2 次"). Contract test pins this constant to the owner
# literal; do not change it here without the owner document.
RETRY_LIMIT_DEFAULT = 2

LOOP_STATES = [
    "RUNNING", "DONE", "INCOMPLETE", "ANOMALY", "FAILED", "DEAD", "TIMEOUT",
    "NO_SIGNAL", "STALLED", "REENTRY_REQUIRED", "UNKNOWN",
]
RECOVERY_ACTIONS = ["none", "watch", "verify", "resume", "retry", "stop"]
INTERRUPTION_FORMS = [
    "unwatched", "dead-no-exit-record", "deadline-overrun-live",
    "heartbeat-stalled", "artifacts-without-completion", "stale-signal",
    "lifecycle-spine-violation", "remote-unreachable",
]
# Forms 065a detects (C-33); heartbeat-stalled / lifecycle-spine-violation are
# 065b's — the vocabulary stays closed here, 065a never emits them.
FORMS_065A = [
    "unwatched", "dead-no-exit-record", "deadline-overrun-live",
    "artifacts-without-completion", "stale-signal", "remote-unreachable",
]

HELP_EPILOG = """Exit codes:
  0  evaluation succeeded (any loop_state is data, never encoded as exit code)
  1  rejected or validation failed (includes the 065a refusal envelopes for
     recover / check-spine)
  2  argument error, or a required CLI input (--line-id, or an explicitly
     provided --probe file) missing / unreadable / unparsable. Evidence
     sources are NOT required inputs: an unreadable evidence file is reported
     as status=missing and the evaluation still completes with exit 0.

Watcher verdict codes (%s) are DATA: this CLI records them verbatim in
watch_verdict.exit_code and never reuses or redefines them as its own exit
codes. Threshold defaults are owned by watch-target.sh (--help Defaults line);
this engine embeds no second set of numbers.

Read-only guarantee: snapshot writes nothing — the only write path is an
explicit --out file, which must resolve outside the state dir and the repo
working tree (checked via realpath before any temp file is created).
""" % (WATCHER_EXIT_CODES,)


def now_epoch():
    return int(datetime.now(timezone.utc).timestamp())


def now_iso_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def emit_json(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def fail_usage(message):
    sys.stderr.write("error: %s\n" % message)
    sys.exit(EXIT_USAGE)


def signal_obj(status, value_state, path=None, **fields):
    obj = {"status": status, "value_state": value_state, "path": path}
    obj.update(fields)
    return obj


# ---------------------------------------------------------------------------
# Path resolution (R-02 priority; Registry fallback lands with T009)
# ---------------------------------------------------------------------------

def resolve_registry_dir():
    override = os.environ.get("SPECIFY_LINE_REGISTRY_DIR")
    if override:
        return Path(override).expanduser()
    xdg = os.environ.get("XDG_STATE_HOME")
    base = Path(xdg).expanduser() if xdg else Path.home() / ".local" / "state"
    return base / "spec-kit" / "lines"


def resolve_paths(args):
    """Explicit args only in the 065a skeleton; Registry/env fallbacks arrive
    with T009 (R-02). Unresolved entries stay None and their evidence reads
    as status=missing (never guessed)."""
    registry_dir = resolve_registry_dir()
    registry_path = registry_dir / ("%s.json" % args.line_id)
    return {
        "state_dir": Path(args.state_dir).expanduser() if args.state_dir else None,
        "spec_dir": Path(args.spec_dir).expanduser() if args.spec_dir else None,
        "repo": Path(args.repo).expanduser() if args.repo else None,
        "spine": Path(args.spine).expanduser() if args.spine else None,
        "probe": None,  # probe mode never resolves local paths
        "registry_dir": registry_dir,
        "registry_path": registry_path,
    }


def read_text_if_present(path):
    if path is None:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


# ---------------------------------------------------------------------------
# State spine read (structural skeleton; full v1/legacy parse lands with T009)
# ---------------------------------------------------------------------------

SPINE_FIELDS = [
    "stage_started_at", "stage_deadline_epoch", "stage_base_commit", "attempt",
    "retry_limit", "last_verdict", "salvage", "salvage_evidence", "salvage_at",
    "pid_path", "status_path", "log_path", "heartbeat_path", "run_id",
]


def read_spine(paths):
    path = paths["spine"]
    text = read_text_if_present(path)
    if text is None:
        return {
            "path": str(path) if path else None,
            "status": "missing",
            "schema": "missing",
            "state": None,
            "state_value_state": "na",
            "consistent": None,
            "fields": {},
            "missing_fields": list(SPINE_FIELDS),
        }
    # TODO(T009): full v1 fence + legacy state[:=] parsing (T005 red-tests it).
    has_fence = "loop-state:begin" in text
    return {
        "path": str(path),
        "status": "present",
        "schema": "v1" if has_fence else "legacy",
        "state": None,
        "state_value_state": "unknown",
        "consistent": None,
        "fields": {},
        "missing_fields": list(SPINE_FIELDS),
    }


def spine_field(spine, key):
    value = spine.get("fields", {}).get(key)
    return value


# ---------------------------------------------------------------------------
# Registry projection (T009 implements the real read; skeleton reports missing)
# ---------------------------------------------------------------------------

def read_registry(paths):
    path = paths["registry_path"]
    # TODO(T009): parse the entry JSON (stage/run_id/spine_path/state).
    return {
        "status": "missing",
        "path": str(path) if path else None,
        "state": None,
        "stage": None,
        "run_id": None,
        "spine_path": None,
    }


# ---------------------------------------------------------------------------
# Thresholds (C-16): explicit args -> watch-target.sh --help Defaults -> unknown
# ---------------------------------------------------------------------------

def watcher_defaults_from_help(watch_script):
    if watch_script is None:
        return {}
    try:
        proc = subprocess.run(
            ["bash", str(watch_script), "--help"],
            capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return {}
    text = proc.stdout or ""
    defaults = {}
    for key in ("window", "interval", "start-grace", "deadline-grace",
                "heartbeat-max-age"):
        m = re.search(r"%s=(\d+)s" % re.escape(key), text)
        if m:
            defaults[key] = int(m.group(1))
    return defaults


def resolve_thresholds(args, watch_script):
    defaults = watcher_defaults_from_help(watch_script)
    explicit_any = any(
        v is not None for v in
        (args.start_grace, args.deadline_grace, args.heartbeat_max_age)
    )
    source = "explicit" if explicit_any else (
        "watch-target-help" if defaults else "unknown"
    )
    value_state = "known" if (explicit_any or defaults) else "unknown"
    return {
        "source": source,
        "value_state": value_state,
        "start_grace": args.start_grace if args.start_grace is not None
        else defaults.get("start-grace"),
        "deadline_grace": args.deadline_grace if args.deadline_grace is not None
        else defaults.get("deadline-grace"),
        "heartbeat_max_age": args.heartbeat_max_age
        if args.heartbeat_max_age is not None
        else defaults.get("heartbeat-max-age"),
        "retry_limit": args.retry_limit if args.retry_limit is not None
        else RETRY_LIMIT_DEFAULT,
    }


# ---------------------------------------------------------------------------
# Evidence projection (skeleton: structural placeholders).
# Real four-piece / watchbeat / hook readers land with T010; artifacts and
# commit evidence with T011 (STAGE_ARTIFACTS + git baseline).
# ---------------------------------------------------------------------------

def four_piece_paths(state_dir, line_id, stage):
    if state_dir is None or stage is None:
        return {}
    base = "%s-%s-%s" % ("%s", line_id, stage)
    return {
        "pid": state_dir / ("pid-%s-%s" % (line_id, stage)),
        "status": state_dir / ("status-%s-%s" % (line_id, stage)),
        "log": state_dir / ("log-%s-%s.log" % (line_id, stage)),
        "heartbeat": state_dir / ("heartbeat-%s-%s.log" % (line_id, stage)),
        "watchbeat": state_dir / ("watchbeat-%s-%s" % (line_id, stage)),
    }


def stage_started_at_of(spine):
    # TODO(T009): real spine field parse; skeleton inspects raw text.
    text = read_text_if_present(Path(spine["path"])) if spine.get("path") else None
    if not text:
        return None
    m = re.search(r"stage_started_at[:=]\s*(\d+)", text)
    return int(m.group(1)) if m else None


def active_watch_target(spine, fp):
    """C-14 target existence: pid/status record, sentinel, or readable
    stage_started_at."""
    if spine.get("status") == "present" and stage_started_at_of(spine) is not None:
        return True
    for key in ("pid", "status"):
        p = fp.get(key)
        if p is not None and p.exists():
            return True
    log = fp.get("log")
    if log is not None and log.exists():
        text = read_text_if_present(log) or ""
        last = last_nonempty_line(text)
        if last and last.endswith("-DONE"):
            return True
    return False


def last_nonempty_line(text):
    lines = [ln for ln in (text or "").splitlines() if ln.strip()]
    return lines[-1] if lines else None


def evidence_block(paths, spine, registry, fp, thresholds, dispatched):
    # TODO(T010): real envelope readers; TODO(T011): artifacts + commits.
    if not dispatched:
        na = lambda: signal_obj("na", "na")  # noqa: E731
        return {
            "evidence_source": "local",
            "pid": na(), "status": na(), "log": na(), "heartbeat": na(),
            "watchbeat": na(),
            "hook": signal_obj("na", "na", path=None, observed_at=None),
            "artifacts": {
                "status": "na", "value_state": "na", "stage": None,
                "complete": None, "commit_required": None,
                "no_change_allowed": None, "items": [],
            },
            "commits": {
                "status": "na", "value_state": "na", "base": None,
                "pathspec": [], "commits": [], "touching": None,
            },
        }
    missing = lambda path=None: signal_obj("missing", "na", path=path)  # noqa: E731
    block = {
        "evidence_source": "local",
        "pid": missing(str(fp["pid"]) if fp.get("pid") else None),
        "status": missing(str(fp["status"]) if fp.get("status") else None),
        "log": missing(str(fp["log"]) if fp.get("log") else None),
        "heartbeat": missing(str(fp["heartbeat"]) if fp.get("heartbeat") else None),
        "watchbeat": missing(str(fp["watchbeat"]) if fp.get("watchbeat") else None),
        "hook": signal_obj("na", "na", path=None, observed_at=None),
        "artifacts": {
            "status": "missing", "value_state": "na", "stage": None,
            "complete": None, "commit_required": None,
            "no_change_allowed": None, "items": [],
        },
        "commits": {
            "status": "missing", "value_state": "na", "base": None,
            "pathspec": [], "commits": [], "touching": None,
        },
    }
    return block


# ---------------------------------------------------------------------------
# Watcher delegation (skeleton: compatibility form only, C-14 row 2).
# The attribution three-state matrix and stale gating land with T012.
# ---------------------------------------------------------------------------

def delegate_watcher(args, paths, spine, registry, fp, thresholds):
    if not active_watch_target(spine, fp):
        return {
            "present": False, "status": "na", "value_state": "na",
            "verdict": None, "reason": None, "exit_code": None,
            "attribution": None, "detail": None,
        }
    script = args.watch_script
    if not script or not Path(script).exists():
        return unavailable_verdict("script-missing")
    # Compatibility form (no attribution args) — only valid while no stale
    # signals exist, which holds in the skeleton (no stale detection yet).
    cmd = [
        "bash", str(script), "--once",
        "--label", args.line_id,
        "--pid-file", str(fp["pid"]),
        "--status-file", str(fp["status"]),
        "--log", str(fp["log"]),
        "--sentinel", "%s-DONE" % (args.stage or "").upper(),
    ]
    if fp.get("heartbeat"):
        cmd += ["--heartbeat", str(fp["heartbeat"])]
    deadline = spine_field(spine, "stage_deadline_epoch")
    if deadline:
        cmd += ["--deadline-epoch", str(deadline)]
    if args.stage:
        cmd += ["--stage", args.stage]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=420)
    except (OSError, subprocess.SubprocessError):
        return unavailable_verdict("invocation-failed")
    parsed = parse_watch_line(proc.stdout or "")
    if parsed is None:
        return unavailable_verdict("unparseable")
    if parsed.get("verdict") in (None, "") or parsed.get("verdict") == "USAGE":
        return unavailable_verdict("usage")
    return {
        "present": True,
        "status": "present",
        "value_state": "known",
        "verdict": parsed.get("verdict"),
        "reason": parsed.get("reason"),
        "exit_code": proc.returncode,
        "attribution": parsed.get("attribution"),
        "detail": None,
    }


def unavailable_verdict(detail):
    return {
        "present": False, "status": "missing", "value_state": "na",
        "verdict": None, "reason": "unavailable", "exit_code": None,
        "attribution": None, "detail": detail,
    }


def parse_watch_line(text):
    for line in text.splitlines():
        if line.startswith("WATCH "):
            fields = {}
            for token in line.split()[1:]:
                if "=" in token:
                    k, _, v = token.partition("=")
                    fields[k] = v
            return fields
    return None


# ---------------------------------------------------------------------------
# Derived loop_state + recovery suggestion (skeleton stubs).
# TODO(T013): the FR-004 fixed-priority ladder (mirrored, owner = FR-004).
# TODO(T015): the C-46 candidate order + C-47/C-48/C-49 gates.
# ---------------------------------------------------------------------------

def not_dispatched(paths, spine, registry, fp, dispatched_evidence):
    """C-35 basic predicate (probe/--stage refinements land with T005/T016)."""
    if spine.get("status") == "present" and stage_started_at_of(spine) is not None:
        return False
    if spine.get("status") == "present" and spine.get("state"):
        return False
    for key in ("pid", "status", "log", "heartbeat"):
        p = fp.get(key)
        if p is not None and p.exists():
            return False
    if registry.get("stage"):
        return False
    return True


def has_dispatch_evidence(spine, registry, fp):
    if registry.get("stage"):
        return True
    for key in ("pid", "status", "log", "heartbeat"):
        p = fp.get(key)
        if p is not None and p.exists():
            return True
    log = fp.get("log")
    if log is not None and log.exists():
        text = read_text_if_present(log) or ""
        last = last_nonempty_line(text)
        if last and last.endswith("-DONE"):
            return True
    return False


def derive_loop_state(watch, spine, registry, fp, evidence, thresholds):
    # TODO(T013): FR-004 ladder (rules 1-8) after the two C-35/C-36 shorts.
    if watch.get("present"):
        return "UNKNOWN", "unknown", "watcher"  # replaced by T013 verbatim rule
    return "UNKNOWN", "unknown", "derived"


def suggest_action(loop_state, loop_state_reason, evidence, spine, thresholds,
                   not_dispatched_flag):
    # TODO(T015): C-46 candidate order + attempt/salvage gates.
    if not_dispatched_flag:
        return "none", "not-dispatched", [], []
    return "stop", "unknown", [], []


# ---------------------------------------------------------------------------
# --out boundary (C-10): realpath BEFORE any temp file; atomic replace.
# ---------------------------------------------------------------------------

def out_boundary_reject(out_raw, protected_dirs):
    target = Path(out_raw).expanduser()
    try:
        resolved_target = target.resolve(strict=False)
        resolved_parent = target.parent.resolve(strict=False)
    except OSError:
        return "unresolvable"
    for protected in protected_dirs:
        if protected is None:
            continue
        for candidate in (resolved_target, resolved_parent):
            if candidate == protected or protected in candidate.parents:
                return "inside-protected"
    return None


def atomic_write(path, content):
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(parent), prefix=".loop-state-out-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, str(path))
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------
# Envelope assembly
# ---------------------------------------------------------------------------

def build_envelope(args, paths, spine, registry, thresholds, evidence, watch,
                   loop_state, loop_state_reason, verdict_source, action,
                   action_reason, preconditions, blocked_by,
                   not_dispatched_flag, fp):
    run_id = registry.get("run_id") or spine_field(spine, "run_id")
    stage = args.stage or registry.get("stage")
    return {
        "schema_version": SCHEMA_VERSION,
        "line_id": args.line_id,
        "run_id": run_id,
        "stage": stage,
        "loop_state": loop_state,
        "verdict_source": verdict_source,
        "loop_state_reason": loop_state_reason,
        "watch_verdict": watch,
        "recovery_action": action,
        "recovery_reason": action_reason,
        "recovery_decision": {
            "action": action,
            "reason": action_reason,
            "preconditions": preconditions,
            "blocked_by": blocked_by,
        },
        "false_completion": False,  # TODO(T011/T014): sentinel x artifacts rule
        "spine": spine,
        "registry": registry,
        "paths": {
            "state_dir": str(paths["state_dir"]) if paths["state_dir"] else None,
            "spec_dir": str(paths["spec_dir"]) if paths["spec_dir"] else None,
            "repo": str(paths["repo"]) if paths["repo"] else None,
            "spine": str(paths["spine"]) if paths["spine"] else None,
            "probe": paths["probe"],
        },
        "thresholds": thresholds,
        "evidence": evidence,
        "interruptions": [],      # TODO(T014): six 065a detectors
        "missing_artifacts": [],  # TODO(T011)
        "uncommitted_artifacts": [],  # TODO(T011)
        "stale_signals": [],      # TODO(T010)
        "evaluated_at": now_iso_utc(),
    }


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

def refusal_envelope(action):
    return {
        "schema_version": SCHEMA_VERSION,
        "action": action,
        "applied": False,
        "result": "failed",
        "steps": [],
        "reason": "not-implemented-in-065a",
        "owner": REFUSAL_OWNER[action],
        "message": (
            "%s is not implemented in slice 065a-state-awareness; behavior "
            "lands in %s per notes/decomposition-gate.md."
            % (action, REFUSAL_OWNER[action])
        ),
    }


def do_snapshot(args, parser):
    paths = resolve_paths(args)
    spine = read_spine(paths)
    registry = read_registry(paths)
    stage = args.stage or registry.get("stage")
    fp = four_piece_paths(paths["state_dir"], args.line_id, stage)
    thresholds = resolve_thresholds(args, args.watch_script)

    dispatched_evidence = has_dispatch_evidence(spine, registry, fp)
    nd = not_dispatched(paths, spine, registry, fp, dispatched_evidence)
    evidence = evidence_block(paths, spine, registry, fp, thresholds, not nd)
    watch = delegate_watcher(args, paths, spine, registry, fp, thresholds)
    loop_state, loop_state_reason, verdict_source = derive_loop_state(
        watch, spine, registry, fp, evidence, thresholds)
    if nd:
        loop_state, loop_state_reason, verdict_source = "UNKNOWN", "not-dispatched", "derived"
    action, action_reason, pre, blocked = suggest_action(
        loop_state, loop_state_reason, evidence, spine, thresholds, nd)

    envelope = build_envelope(args, paths, spine, registry, thresholds, evidence,
                              watch, loop_state, loop_state_reason,
                              verdict_source, action, action_reason, pre,
                              blocked, nd, fp)
    content = json.dumps(envelope, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        protected = []
        for key in ("state_dir", "repo"):
            p = paths[key]
            if p is not None:
                protected.append(Path(p).expanduser().resolve(strict=False))
        violation = out_boundary_reject(args.out, protected)
        if violation:
            fail_usage("--out %s rejected (%s): target must stay outside the "
                       "state dir and the repo working tree" % (args.out, violation))
        atomic_write(Path(args.out).expanduser(), content)
    sys.stdout.write(content)
    sys.exit(EXIT_OK)


def do_self_test(args):
    """Structural cases now (help ladder + refusal envelopes); the six-form
    and evidence cases land with T017 (C-18)."""
    passed, failed = 0, 0

    def check(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
            print("ok %s" % name)
        else:
            failed += 1
            print("FAIL %s — %s" % (name, detail or "assertion failed"))

    help_proc = subprocess.run(
        [sys.executable, __file__, "--help"],
        capture_output=True, text=True,
    )
    help_text = help_proc.stdout
    check("help-ladder", "Exit codes:" in help_text
          and "0" in help_text and "1" in help_text and "2" in help_text,
          "exit ladder text missing from --help")
    check("help-watcher-codes-are-data",
          "DATA" in help_text and WATCHER_EXIT_CODES in help_text,
          "watcher codes as data note missing")
    for action, owner in sorted(REFUSAL_OWNER.items()):
        proc = subprocess.run(
            [sys.executable, __file__, "--action", action, "--line-id", "self-test"],
            capture_output=True, text=True,
        )
        try:
            env = json.loads(proc.stdout)
            ok = (proc.returncode == EXIT_REFUSED and env.get("result") == "failed"
                  and env.get("owner") == owner
                  and env.get("reason") == "not-implemented-in-065a")
        except ValueError:
            ok = False
        check("refusal-%s" % action, ok,
              "expected refusal envelope with owner=%s, exit 1" % owner)

    print("SELF-TEST: %d passed, %d failed" % (passed, failed))
    sys.exit(EXIT_OK if failed == 0 else EXIT_REFUSED)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="loop-state.py",
        description="Read-only loop state snapshot engine (Feature 065 / slice "
                    "065a): one call aggregates spine, Registry, four-piece "
                    "signals, watchbeat, artifacts, git commits and the watcher "
                    "verdict into a single JSON envelope.",
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--action", choices=["snapshot", "recover", "check-spine"],
                        default="snapshot")
    parser.add_argument("--self-test", action="store_true", dest="self_test",
                        help="run built-in self-test fixtures (no real processes)")
    parser.add_argument("--line-id", help="line identifier (required for snapshot)")
    parser.add_argument("--stage", help="caller intent for the current stage")
    parser.add_argument("--state-dir", help="runtime state directory override")
    parser.add_argument("--spec-dir", help="feature spec directory override")
    parser.add_argument("--repo", help="repository root override")
    parser.add_argument("--spine", help="state spine file override")
    parser.add_argument("--probe", help="caller-collected probe JSON (mutually "
                                        "exclusive with local path arguments)")
    parser.add_argument("--watch-script", help="watch-target.sh path for verdict "
                                               "delegation")
    parser.add_argument("--out", help="write the envelope to this file (must "
                                      "resolve outside state dir and repo)")
    parser.add_argument("--start-grace", type=int)
    parser.add_argument("--deadline-grace", type=int)
    parser.add_argument("--heartbeat-max-age", type=int)
    parser.add_argument("--retry-limit", type=int)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        do_self_test(args)

    if args.action in REFUSAL_OWNER:
        emit_json(refusal_envelope(args.action))
        sys.exit(EXIT_REFUSED)

    if not args.line_id:
        fail_usage("--line-id is required (exit 2: missing required input)")

    if args.probe:
        local_flags = [args.spine, args.state_dir, args.spec_dir, args.repo,
                       args.watch_script]
        if any(v is not None for v in local_flags):
            fail_usage("--probe is mutually exclusive with --spine/--state-dir/"
                       "--spec-dir/--repo/--watch-script (exit 2)")
        # TODO(T016): probe shapes (a)/(b) consumption. Skeleton rejects.
        fail_usage("--probe consumption is not implemented in this build")

    if args.action == "snapshot":
        do_snapshot(args, parser)
    fail_usage("unreachable action: %s" % args.action)


if __name__ == "__main__":
    main()
