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
(parent #FR-004). The `DERIVED_MAPPING` table below is a mirror of that table;
references/state-awareness.md mirrors it too. Nothing here claims ownership of
the table (contract test pins this attribution).

Stage artifact map: `STAGE_ARTIFACTS` is the runtime owner of the stage ->
required artifacts / owned-only paths / commit obligation mapping (contract
C-50); the reference section of the same name is its human-readable mirror.

Thresholds: start-grace / deadline-grace / heartbeat-max-age defaults are owned
by scripts/watch-target.sh (--help "Defaults:" line). This engine never embeds
a second set of numbers; when discovery fails the value stays unknown and the
dependent checks do not fire. retry_limit default is owned by
references/stage-prompts.md § Stall Handling.

Thresholds and evidence semantics mirror `watch-target.sh` (R-03/R-05): the
four-piece files are space envelopes, the sentinel is the last non-empty log
line == "<STAGE>-DONE", and watcher verdict codes (10-16) are data recorded in
watch_verdict.exit_code, never reused as this CLI's code.

Exit codes: 0 / 1 / 2 only (see --help).

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

# ---------------------------------------------------------------------------
# Stage artifact map (C-50/C-51/C-52)
#
# Runtime owner of "stage -> artifacts[] / owned_paths[] / commit_required /
# no_change_allowed". Paths are relative to the resolved spec_dir; implement
# expresses completeness through code/test commit evidence and has no file
# artifact. references/state-awareness.md §Stage Artifact Map mirrors this table
# item by item (contract test pins the five dimensions).
# ---------------------------------------------------------------------------

IMPLEMENT_CODE_PATHSPEC = [
    "src/", "skills/", "scripts/", "tests/", "templates/", "agents/",
]

STAGE_ARTIFACTS = {
    "requirements": {
        "artifacts": ["requirements.md"],
        "owned_paths": [],
        "commit_required": True,
        "no_change_allowed": False,
    },
    "clarify": {
        "artifacts": ["requirements.md"],
        "owned_paths": [],
        "commit_required": True,
        "no_change_allowed": True,
    },
    "plan": {
        "artifacts": ["plan.md", "data-model.md", "contracts/",
                      "quickstart.md", "feature-ref.md"],
        "owned_paths": ["research.md"],
        "commit_required": True,
        "no_change_allowed": False,
    },
    "tasks": {
        "artifacts": ["tasks.md"],
        "owned_paths": [],
        "commit_required": True,
        "no_change_allowed": False,
    },
    "checklist": {
        "artifacts": ["checklists/"],
        "owned_paths": [],
        "commit_required": True,
        "no_change_allowed": False,
    },
    "analyze": {
        "artifacts": [],
        "owned_paths": [],
        "commit_required": False,
        "no_change_allowed": True,
    },
    "implement": {
        "artifacts": [],
        "owned_paths": [],
        "commit_required": True,
        "no_change_allowed": False,
    },
    "review": {
        "artifacts": ["review.md"],
        "owned_paths": [],
        "commit_required": True,
        "no_change_allowed": False,
    },
}

# ---------------------------------------------------------------------------
# Derived loop_state mapping — MIRROR of requirements.md FR-004 (the single
# owner). Row shape is {order, state, condition}: `order` is the FR-004 clause
# number and rows sharing an order are alternatives inside that clause.
# Contract test pins this table against the FR-004 clauses (three-way check
# with references/state-awareness.md §Derived Mapping, created by T018).
# ---------------------------------------------------------------------------

DERIVED_MAPPING = [
    {"order": 1, "state": "STALLED", "condition": "spine_state=stalled"},
    {"order": 1, "state": "REENTRY_REQUIRED",
     "condition": "spine_state=reentry-required"},
    {"order": 2, "state": "ANOMALY",
     "condition": "exit record or dead pid, last log line starts with ANOMALY:"},
    {"order": 2, "state": "FAILED",
     "condition": "exit record with non-zero exit code"},
    {"order": 2, "state": "DONE",
     "condition": "exit record exit=0 + final-line sentinel + artifacts complete"},
    {"order": 2, "state": "INCOMPLETE",
     "condition": "exit record exit=0 + (no final-line sentinel or artifacts incomplete)"},
    {"order": 3, "state": "DONE",
     "condition": "no exit record + final-line sentinel + artifacts complete"},
    {"order": 3, "state": "INCOMPLETE",
     "condition": "no exit record + final-line sentinel + artifacts incomplete"},
    {"order": 4, "state": "DEAD",
     "condition": "no exit record + pid record dead or start token mismatch"},
    {"order": 5, "state": "TIMEOUT",
     "condition": "now >= stage_deadline_epoch + deadline-grace, no terminal evidence"},
    {"order": 6, "state": "NO_SIGNAL",
     "condition": "no pid record and no exit record, past start grace"},
    {"order": 7, "state": "RUNNING",
     "condition": "pid alive or fresh heartbeat, no terminal evidence"},
    {"order": 8, "state": "UNKNOWN", "condition": "none of the above"},
]

SPINE_FIELDS = [
    "stage_started_at", "stage_deadline_epoch", "stage_base_commit", "attempt",
    "retry_limit", "last_verdict", "salvage", "salvage_evidence", "salvage_at",
    "pid_path", "status_path", "log_path", "heartbeat_path", "run_id",
]
# Fields whose absence is reported in missing_fields (a v1 spine that omits them
# is degraded, not merely terse).
REQUIRED_SPINE_FIELDS = [
    "stage_started_at", "stage_deadline_epoch", "stage_base_commit", "attempt",
    "retry_limit", "run_id",
]
INT_SPINE_FIELDS = {
    "stage_started_at", "stage_deadline_epoch", "attempt", "retry_limit",
}

# Evidence signals in the fixed order this engine reports them.
SIGNAL_ORDER = ["pid", "status", "heartbeat", "watchbeat"]
STALE_REASONS = ["run-mismatch", "before-stage-start", "legacy-stale"]

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


def to_int(value):
    if value is None:
        return None
    text = str(value).strip()
    if re.match(r"^-?\d+$", text):
        return int(text)
    return None


def is_digits(value):
    return value is not None and str(value).strip().isdigit()


def mtime_ns_of(path):
    try:
        return path.stat().st_mtime_ns
    except OSError:
        return None


def read_text_if_present(path):
    if path is None:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def last_nonempty_line(text):
    lines = [ln for ln in (text or "").splitlines() if ln.strip()]
    return lines[-1] if lines else None


def parse_space_envelope(text):
    """Parse a space-separated `key=value` envelope (first occurrence wins —
    R-03 mirrors watch-target.sh, which reads the first `exit=`/`pid=` line)."""
    tokens = {}
    for raw in (text or "").split():
        if "=" not in raw:
            continue
        key, _, value = raw.partition("=")
        if not key:
            continue
        tokens.setdefault(key, value)
    return tokens


def normalize_spine_state(value):
    if not value:
        return None
    return str(value).strip().lower().replace("_", "-")


# ---------------------------------------------------------------------------
# Liveness (mirrors watch-target.sh is_alive: kill -0, zombie check, start
# token comparison). The start token is only compared when the recorded and
# the platform token are the same kind of value: on macOS the watcher obtains
# a formatted `ps -p <pid> -o lstart=` string, so a numeric runner token is
# NOT comparable there — the engine reports identity=unknown instead of
# inventing a pid reuse (no guess; C-41 needs a comparable token to fire).
# ---------------------------------------------------------------------------

def process_start_token(pid):
    if pid is None or pid <= 0:
        return None
    stat_path = Path("/proc/%s/stat" % pid)
    try:
        if stat_path.is_file():
            fields = stat_path.read_text(encoding="utf-8",
                                         errors="replace").split()
            if len(fields) > 21:
                return fields[21]
    except OSError:
        pass
    try:
        proc = subprocess.run(
            ["ps", "-p", str(pid), "-o", "lstart="],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    token = " ".join((proc.stdout or "").split())
    return token or None


def process_stat_state(pid):
    stat_path = Path("/proc/%s/stat" % pid)
    try:
        if stat_path.is_file():
            fields = stat_path.read_text(encoding="utf-8",
                                         errors="replace").split()
            if len(fields) > 2:
                return fields[2]
    except OSError:
        pass
    try:
        proc = subprocess.run(
            ["ps", "-p", str(pid), "-o", "stat="],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    first = (proc.stdout or "").split()
    return first[0] if first else None


def process_alive(pid):
    """True / False, or None when no pid is readable (unknown, never a guess)."""
    if pid is None or pid <= 0:
        return None
    try:
        os.kill(pid, 0)
    except PermissionError:
        return True
    except OSError:
        return False
    state = process_stat_state(pid)
    if state and state.startswith("Z"):
        return False
    return True


def compare_start_identity(pid, recorded, alive):
    """ok / mismatch / unknown — only comparable tokens yield a verdict."""
    if pid is None or alive is not True or not recorded:
        return "unknown"
    actual = process_start_token(pid)
    if not actual:
        return "unknown"
    if str(recorded) == str(actual):
        return "ok"
    if is_digits(recorded) and is_digits(actual):
        return "mismatch"
    return "unknown"


# ---------------------------------------------------------------------------
# Path resolution (C-4 / R-02) and Registry projection (C-24)
# ---------------------------------------------------------------------------

def resolve_registry_dir():
    override = os.environ.get("SPECIFY_LINE_REGISTRY_DIR")
    if override:
        return Path(override).expanduser()
    xdg = os.environ.get("XDG_STATE_HOME")
    base = Path(xdg).expanduser() if xdg else Path.home() / ".local" / "state"
    return base / "spec-kit" / "lines"


def read_registry(path):
    """Return (RegistryView, raw entry). An unreadable entry is `missing`, not
    fatal (C-5); the raw dict is kept only for path fallbacks and meta paths."""
    raw = None
    if path is not None and path.is_file():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            loaded = None
        if isinstance(loaded, dict):
            raw = loaded
    view = {
        "status": "present" if raw is not None else "missing",
        "path": str(path) if path is not None else None,
        "state": raw.get("state") if raw else None,
        "stage": raw.get("stage") if raw else None,
        "run_id": raw.get("run_id") if raw else None,
        "spine_path": raw.get("spine_path") if raw else None,
    }
    return view, raw


def resolve_runtime_dir():
    """R-02 `state_dir` fallbacks 3-4: `$SPECIFY_LINE_RUNTIME_DIR` -> `$HOME`.

    Mirrors `line-registry.py` `resolve_runtime_dir` (the on-disk convention
    owner R-02 cites), so the engine looks where the runner writes. Nothing is
    invented: when neither variable is set the item stays `None` (null
    semantics) — `$HOME` unset is not replaced by a pwd-derived guess."""
    override = os.environ.get("SPECIFY_LINE_RUNTIME_DIR")
    if override:
        return Path(override).expanduser()
    home = os.environ.get("HOME")
    if home:
        return Path(home).expanduser()
    return None


def resolve_paths(args):
    """R-02 per-item priority (C-4 delegates the item order to R-02).

    `state_dir`: explicit --state-dir -> Registry `status_path` parent ->
    `$SPECIFY_LINE_RUNTIME_DIR` -> `$HOME`. `spine`: explicit -> Registry
    `spine_path` -> null. `spec_dir` / `repo`: explicit only -> null. A value
    that the chain cannot produce stays null; nothing is guessed."""
    registry_dir = resolve_registry_dir()
    registry_path = registry_dir / ("%s.json" % args.line_id)
    registry, raw = read_registry(registry_path)

    state_dir = Path(args.state_dir).expanduser() if args.state_dir else None
    if state_dir is None and isinstance(raw, dict):
        status_path = raw.get("status_path")
        if isinstance(status_path, str) and status_path:
            state_dir = Path(status_path).expanduser().parent
    if state_dir is None:
        state_dir = resolve_runtime_dir()

    spine = Path(args.spine).expanduser() if args.spine else None
    if spine is None and isinstance(raw, dict):
        spine_path = raw.get("spine_path")
        if isinstance(spine_path, str) and spine_path:
            spine = Path(spine_path).expanduser()

    # spec_dir and repo have no reliable default (R-02: never guessed from the
    # spine, the cwd or the Registry).
    spec_dir = Path(args.spec_dir).expanduser() if args.spec_dir else None
    repo = Path(args.repo).expanduser() if args.repo else None

    return {
        "state_dir": state_dir,
        "spec_dir": spec_dir,
        "repo": repo,
        "spine": spine,
        "probe": None,  # probe mode never resolves local paths (C-13)
        "registry_dir": registry_dir,
        "registry_path": registry_path,
    }, registry, raw


# ---------------------------------------------------------------------------
# State spine (C-23 / data-model §3.2): v1 machine fence or legacy state[:=]
# ---------------------------------------------------------------------------

FENCE_BEGIN = "<!-- loop-state:begin -->"
FENCE_END = "<!-- loop-state:end -->"


def empty_spine_fields():
    return {key: None for key in SPINE_FIELDS}


def fence_body(text):
    start = text.find(FENCE_BEGIN)
    if start < 0:
        return None
    start += len(FENCE_BEGIN)
    end = text.find(FENCE_END, start)
    body = text[start:end] if end >= 0 else text[start:]
    return body


def parse_spine_pairs(body):
    pairs = {}
    for line in (body or "").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*[:=]\s*(.*)$", stripped)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if value.startswith("`") and value.endswith("`") and len(value) > 1:
            value = value[1:-1]
        pairs.setdefault(key, value)
    return pairs


def coerce_spine_value(key, value):
    if value is None or value == "":
        return None
    if key in INT_SPINE_FIELDS:
        return to_int(value)
    return value


def read_spine(paths):
    path = paths["spine"]
    text = read_text_if_present(path)
    fields = empty_spine_fields()
    if text is None:
        return {
            "path": str(path) if path else None,
            "status": "missing",
            "schema": "missing",
            "state": None,
            "state_value_state": "na",
            "consistent": None,
            "fields": fields,
            "missing_fields": list(REQUIRED_SPINE_FIELDS),
        }
    body = fence_body(text)
    schema = "v1" if body is not None else "legacy"
    pairs = parse_spine_pairs(body if body is not None else text)
    for key, value in pairs.items():
        if key in fields:
            fields[key] = coerce_spine_value(key, value)
    raw_state = pairs.get("spine_state") if schema == "v1" else pairs.get("state")
    state = raw_state.strip() if isinstance(raw_state, str) else None
    state = state or None
    return {
        "path": str(path),
        "status": "present",
        "schema": schema,
        "state": state,
        "state_value_state": "known" if state else "unknown",
        "consistent": None,
        "fields": fields,
        "missing_fields": [key for key in REQUIRED_SPINE_FIELDS
                           if fields.get(key) is None],
    }


def spine_field(spine, key):
    return spine.get("fields", {}).get(key)


# ---------------------------------------------------------------------------
# Thresholds (C-16): explicit args -> watch-target.sh --help Defaults -> unknown
# ---------------------------------------------------------------------------

def watcher_defaults_from_help(watch_script):
    if watch_script is None or not Path(watch_script).is_file():
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
    # C-16: explicit -> `watch-target.sh --help` -> unknown. The help probe is
    # skipped when every threshold was given explicitly: it would be a pointless
    # invocation of the watcher script (observable side effect).
    explicit_any = any(
        v is not None for v in
        (args.start_grace, args.deadline_grace, args.heartbeat_max_age)
    )
    explicit_all = all(
        v is not None for v in
        (args.start_grace, args.deadline_grace, args.heartbeat_max_age)
    )
    defaults = {} if explicit_all else watcher_defaults_from_help(watch_script)
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
# Evidence readers (T010): four-piece space envelopes + watchbeat marker.
# Evidence sources degrade to missing / unknown; they never raise and never
# turn the evaluation into exit 2 (C-6).
# ---------------------------------------------------------------------------

def sentinel_literal(stage):
    if not stage:
        return None
    return "%s-DONE" % str(stage).upper()


def four_piece_paths(state_dir, line_id, stage):
    if state_dir is None or stage is None:
        return {}
    return {
        "pid": state_dir / ("pid-%s-%s" % (line_id, stage)),
        "status": state_dir / ("status-%s-%s" % (line_id, stage)),
        "log": state_dir / ("log-%s-%s.log" % (line_id, stage)),
        "heartbeat": state_dir / ("heartbeat-%s-%s.log" % (line_id, stage)),
        "watchbeat": state_dir / ("watchbeat-%s-%s" % (line_id, stage)),
    }


PID_FIELDS = {"pid": None, "start": None, "at": None, "alive": None,
              "identity": None, "attribution": None}
STATUS_FIELDS = {"exit_code": None, "at": None, "sentinel": None,
                 "run_id": None, "stage": None, "event": None,
                 "legacy": None, "attribution": None}
LOG_FIELDS = {"last_line": None, "sentinel_present": False, "sentinel": None,
              "anomaly": False}
HEARTBEAT_FIELDS = {"at": None, "mtime_ns": None, "fresh": None,
                    "attribution": None}
WATCHBEAT_FIELDS = {"run_id": None, "stage": None, "window": None, "at": None,
                    "event": None, "fresh": None}


def clone_fields(defaults):
    return dict(defaults)


def missing_signal(defaults, path=None):
    obj = signal_obj("missing", "na", path=str(path) if path is not None else None)
    obj.update(clone_fields(defaults))
    return obj


def na_signal(defaults):
    obj = signal_obj("na", "na", path=None)
    obj.update(clone_fields(defaults))
    return obj


def classify_attribution(tokens, current_run):
    """own / legacy / stale-run / unattributed (data-model §4.2). A current
    envelope carrying line=/stage= but no run= is `legacy`, never `own`."""
    run = tokens.get("run")
    has_line = "line" in tokens
    if run is not None and current_run is not None:
        return "own" if run == current_run else "stale-run"
    if run is not None or has_line:
        return "legacy"
    return "unattributed"


def read_pid_signal(file_path, current_run, now, thresholds):
    if file_path is None or not file_path.is_file():
        return missing_signal(PID_FIELDS, file_path), {}
    tokens = parse_space_envelope(read_text_if_present(file_path) or "")
    pid = to_int(tokens.get("pid"))
    start = tokens.get("start")
    alive = process_alive(pid) if pid is not None else None
    identity = compare_start_identity(pid, start, alive)
    obj = signal_obj("present", "known" if pid is not None else "unknown",
                     path=str(file_path))
    obj.update({
        "pid": pid,
        "start": start,
        "at": to_int(tokens.get("at")),
        "alive": alive,
        "identity": identity,
        "attribution": classify_attribution(tokens, current_run),
    })
    meta = {
        "status": "present",
        "path": str(file_path),
        "run": tokens.get("run"),
        "has_line": "line" in tokens,
        "at": obj["at"],
        "mtime_ns": mtime_ns_of(file_path),
    }
    return obj, meta


def read_status_signal(file_path, current_run, now, thresholds):
    if file_path is None or not file_path.is_file():
        return missing_signal(STATUS_FIELDS, file_path), {}
    text = read_text_if_present(file_path) or ""
    tokens = parse_space_envelope(text)
    exit_line = None
    for line in text.splitlines():
        if line.startswith("exit="):
            exit_line = line
            break
    exit_code = None
    if exit_line is not None:
        exit_code = to_int(parse_space_envelope(exit_line).get("exit"))
    sentinel = tokens.get("sentinel")
    obj = signal_obj("present", "known" if exit_code is not None else "unknown",
                     path=str(file_path))
    obj.update({
        "exit_code": exit_code,
        "at": to_int(tokens.get("at")),
        "sentinel": to_int(sentinel) if is_digits(sentinel) else None,
        "run_id": tokens.get("run"),
        "stage": tokens.get("stage"),
        "event": tokens.get("event"),
        "legacy": tokens.get("run") is None and "line" not in tokens,
        "attribution": classify_attribution(tokens, current_run),
    })
    meta = {
        "status": "present",
        "path": str(file_path),
        "run": tokens.get("run"),
        "has_line": "line" in tokens,
        "at": obj["at"],
        "mtime_ns": mtime_ns_of(file_path),
    }
    return obj, meta


def read_log_signal(file_path, stage):
    if file_path is None or not file_path.is_file():
        return missing_signal(LOG_FIELDS, file_path), {}
    text = read_text_if_present(file_path) or ""
    last = last_nonempty_line(text)
    sentinel = sentinel_literal(stage)
    obj = signal_obj("present", "known", path=str(file_path))
    obj.update({
        "last_line": last,
        "sentinel_present": bool(sentinel is not None and last is not None
                                 and last.strip() == sentinel),
        "sentinel": sentinel,
        "anomaly": bool(last is not None and last.lstrip().startswith("ANOMALY:")),
    })
    return obj, {"status": "present", "path": str(file_path)}


def read_heartbeat_signal(file_path, current_run, now, thresholds):
    if file_path is None or not file_path.is_file():
        return missing_signal(HEARTBEAT_FIELDS, file_path), {}
    tokens = parse_space_envelope(read_text_if_present(file_path) or "")
    mtime_ns = mtime_ns_of(file_path)
    max_age = thresholds.get("heartbeat_max_age")
    fresh = None
    if max_age is not None and mtime_ns is not None:
        fresh = (now * 10 ** 9 - mtime_ns) <= max_age * 10 ** 9
    obj = signal_obj("present", "known" if mtime_ns is not None else "unknown",
                     path=str(file_path))
    obj.update({
        "at": to_int(tokens.get("at")),
        "mtime_ns": mtime_ns,
        "fresh": fresh,
        "attribution": classify_attribution(tokens, current_run),
    })
    meta = {
        "status": "present",
        "path": str(file_path),
        "run": tokens.get("run"),
        "has_line": "line" in tokens,
        "at": obj["at"],
        "mtime_ns": mtime_ns,
    }
    return obj, meta


def read_watchbeat_signal(file_path, current_run, now, thresholds):
    if file_path is None or not file_path.is_file():
        return missing_signal(WATCHBEAT_FIELDS, file_path), {}
    tokens = parse_space_envelope(read_text_if_present(file_path) or "")
    at = to_int(tokens.get("at"))
    window = to_int(tokens.get("window"))
    grace = thresholds.get("deadline_grace")
    fresh = None
    if at is not None and window is not None and grace is not None:
        fresh = (now - at) <= (window + grace)
    obj = signal_obj("present", "known" if at is not None else "unknown",
                     path=str(file_path))
    obj.update({
        "run_id": tokens.get("run"),
        "stage": tokens.get("stage"),
        "window": window,
        "at": at,
        "event": tokens.get("event"),
        "fresh": fresh,
    })
    meta = {
        "status": "present",
        "path": str(file_path),
        "run": tokens.get("run"),
        "has_line": "line" in tokens,
        "at": at,
        "mtime_ns": mtime_ns_of(file_path),
    }
    return obj, meta


def hook_signal():
    return signal_obj("na", "na", path=None, observed_at=None)


def collect_signals(fp, spine, stage, thresholds, dispatched, now):
    """Read all evidence signals once. When the line was never dispatched the
    whole evidence block is `na` (C-35) — no reader is invoked."""
    if not dispatched:
        return {
            "pid": na_signal(PID_FIELDS),
            "status": na_signal(STATUS_FIELDS),
            "log": na_signal(LOG_FIELDS),
            "heartbeat": na_signal(HEARTBEAT_FIELDS),
            "watchbeat": na_signal(WATCHBEAT_FIELDS),
            "hook": hook_signal(),
        }, {}
    current_run = spine_field(spine, "run_id")
    signals = {}
    metas = {}
    readers = {
        "pid": lambda p: read_pid_signal(p, current_run, now, thresholds),
        "status": lambda p: read_status_signal(p, current_run, now, thresholds),
        "log": lambda p: read_log_signal(p, stage),
        "heartbeat": lambda p: read_heartbeat_signal(
            p, current_run, now, thresholds),
        "watchbeat": lambda p: read_watchbeat_signal(
            p, current_run, now, thresholds),
    }
    for name, reader in readers.items():
        obj, meta = reader(fp.get(name))
        signals[name] = obj
        if meta:
            metas[name] = meta
    signals["hook"] = hook_signal()
    return signals, metas


def registry_meta_present(raw):
    if not isinstance(raw, dict):
        return False
    meta = raw.get("meta_paths")
    if not isinstance(meta, dict):
        return False
    for value in meta.values():
        if isinstance(value, str) and value and Path(value).is_file():
            return True
    return False


def first_meta_path(raw):
    if not isinstance(raw, dict):
        return None
    meta = raw.get("meta_paths")
    if not isinstance(meta, dict):
        return None
    for value in meta.values():
        if isinstance(value, str) and value and Path(value).is_file():
            return value
    return None


def detect_stale_signals(metas, spine, raw_registry, signals):
    """C-43: run mismatch / mtime before stage start / legacy envelope. The
    current attempt is known from the spine or Registry, or corroborated by at
    least two four-piece envelopes; a lone run= claim cannot establish
    attribution and is stale (doubtful-strict). The watchbeat marker is a
    driver marker, not an attempt envelope: its run= is judged only against a
    known attempt, and its freshness is owned by its own window= (C-40)."""
    current_run = spine_field(spine, "run_id")
    if current_run is None and isinstance(raw_registry, dict):
        current_run = raw_registry.get("run_id")
    started_at = spine_field(spine, "stage_started_at")
    has_meta = registry_meta_present(raw_registry)

    run_counts = {}
    for name in ("pid", "status", "heartbeat"):
        meta = metas.get(name)
        if not meta:
            continue
        run = meta.get("run")
        if run is not None:
            run_counts[run] = run_counts.get(run, 0) + 1

    stale = []
    for name in SIGNAL_ORDER:
        meta = metas.get(name)
        if not meta or meta.get("status") != "present":
            continue
        run = meta.get("run")
        reason = None
        if run is not None:
            if current_run is not None:
                reason = "run-mismatch" if run != current_run else None
            elif name != "watchbeat" and run_counts.get(run, 0) < 2:
                reason = "run-mismatch"
        if reason is None and meta.get("mtime_ns") is not None \
                and started_at is not None:
            if meta["mtime_ns"] < started_at * 10 ** 9:
                reason = "before-stage-start"
        if reason is None and run is None and not meta.get("has_line") \
                and not has_meta:
            reason = "legacy-stale"
        if reason is not None:
            stale.append({
                "signal": name,
                "path": meta.get("path"),
                "reason": reason,
                "run_id": run,
                "at": meta.get("at"),
                "mtime_ns": meta.get("mtime_ns"),
            })
    return stale, current_run


# ---------------------------------------------------------------------------
# Effective (stale-excluded) view of the evidence
# ---------------------------------------------------------------------------

def ev_present(signals, stale_names, name):
    return name not in stale_names and signals.get(name, {}).get("status") == "present"


def ev_value(signals, stale_names, name, key):
    if not ev_present(signals, stale_names, name):
        return None
    return signals[name].get(key)


def build_view(signals, stale_names, spine, thresholds, now):
    started_at = spine_field(spine, "stage_started_at")
    deadline = spine_field(spine, "stage_deadline_epoch")
    grace = thresholds.get("deadline_grace")
    start_grace = thresholds.get("start_grace")
    spine_state = normalize_spine_state(spine.get("state"))

    pid_present = ev_present(signals, stale_names, "pid")
    pid_alive = ev_value(signals, stale_names, "pid", "alive")
    pid_identity = ev_value(signals, stale_names, "pid", "identity")
    exit_code = ev_value(signals, stale_names, "status", "exit_code")
    heartbeat_fresh = ev_value(signals, stale_names, "heartbeat", "fresh")
    last_line = ev_value(signals, stale_names, "log", "last_line")
    anomaly_last = ev_value(signals, stale_names, "log", "anomaly")
    sentinel_present = bool(
        ev_value(signals, stale_names, "log", "sentinel_present"))
    watchbeat_present = ev_present(signals, stale_names, "watchbeat")
    watchbeat_fresh = ev_value(signals, stale_names, "watchbeat", "fresh")

    deadline_overrun = bool(
        deadline is not None and grace is not None and now >= deadline + grace)
    start_grace_passed = bool(
        started_at is not None and start_grace is not None
        and now >= started_at + start_grace)
    pid_dead = bool(pid_present and (pid_alive is False
                                     or pid_identity == "mismatch"))
    exit_record = exit_code is not None

    return {
        "now": now,
        "started_at": started_at,
        "deadline_overrun": deadline_overrun,
        "start_grace_passed": start_grace_passed,
        "spine_state": spine_state,
        "pid_present": pid_present,
        "pid_alive": pid_alive,
        "pid_identity": pid_identity,
        "pid_dead": pid_dead,
        "exit_code": exit_code,
        "exit_record": exit_record,
        "sentinel_present": sentinel_present,
        "last_line": last_line,
        "anomaly_last": bool(anomaly_last),
        "heartbeat_fresh": heartbeat_fresh,
        "watchbeat_present": watchbeat_present,
        "watchbeat_fresh": watchbeat_fresh,
    }


def running_and_unterminated(view):
    running = view["pid_alive"] is True or view["heartbeat_fresh"] is True
    terminal = (view["sentinel_present"] or view["exit_record"]
                or view["spine_state"] in ("stalled", "reentry-required"))
    return running, terminal


# ---------------------------------------------------------------------------
# Stage artifacts + commit evidence (T011 / C-50..C-60)
# ---------------------------------------------------------------------------

def run_git(repo, args, timeout=30):
    if repo is None:
        return None
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo)] + list(args),
            capture_output=True, text=True, timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def repo_relative(repo, target):
    try:
        return str(Path(target).resolve().relative_to(Path(repo).resolve()))
    except (ValueError, OSError):
        return None


def spec_path(spec_dir, rel, repo):
    target = Path(spec_dir) / rel
    if repo is not None:
        relative = repo_relative(repo, target)
        if relative:
            return relative
    return str(target)


def build_pathspec(stage, spec_dir, repo):
    entry = STAGE_ARTIFACTS.get(stage)
    if entry is None:
        return []
    if stage == "implement":
        # C-58/C-60: code/test paths only (docs-only commits never count).
        return list(IMPLEMENT_CODE_PATHSPEC)
    if spec_dir is None:
        return []
    rels = list(entry["artifacts"])
    for owned in entry["owned_paths"]:
        # Optional owned path: enters the commit path set only when present.
        if (Path(spec_dir) / owned).is_file():
            rels.append(owned)
    return [spec_path(spec_dir, rel, repo) for rel in rels]


def resolve_base(repo, base):
    if not base:
        return "missing"
    out = run_git(repo, ["rev-parse", "--verify", "--quiet",
                         "%s^{commit}" % base])
    return "resolved" if out is not None else "unresolved"


def parse_git_name_list(out):
    if not out:
        return set()
    return {line.strip() for line in out.splitlines() if line.strip()}


def worktree_changes(repo, base, pathspec):
    changed = set()
    out = run_git(repo, ["diff", "--name-only", base, "--"] + list(pathspec))
    changed |= parse_git_name_list(out)
    out = run_git(repo, ["ls-files", "--others", "--exclude-standard", "--"]
                  + list(pathspec))
    changed |= parse_git_name_list(out)
    return changed


def commit_context(stage, spec_dir, repo, spine, dispatched):
    entry = STAGE_ARTIFACTS.get(stage) if stage else None
    ctx = {
        "stage": stage,
        "commit_required": entry["commit_required"] if entry else None,
        "no_change_allowed": entry["no_change_allowed"] if entry else None,
        "base": None,
        "base_state": "na",
        "pathspec": [],
        "commits": [],
        "touching": None,
        "changed_committed": None,
        "changed_any": None,
        "repo_readable": False,
        "implement_complete": None,
    }
    if not dispatched or entry is None:
        return ctx
    base = spine_field(spine, "stage_base_commit")
    ctx["base"] = base
    ctx["base_state"] = resolve_base(repo, base)
    ctx["pathspec"] = build_pathspec(stage, spec_dir, repo)
    if ctx["base_state"] != "resolved" or not entry["commit_required"]:
        if entry["commit_required"] and ctx["base_state"] == "unresolved":
            # No provable commit evidence: "complete" is the no-positive-evidence
            # side (FR-051), never a HEAD guess (C-57).
            ctx["implement_complete"] = False
        return ctx
    log = run_git(repo, ["log", "--format=%H\t%s", "%s..HEAD" % base, "--"]
                  + ctx["pathspec"])
    if log is None:
        return ctx
    ctx["repo_readable"] = True
    commits = []
    for line in log.splitlines():
        sha, _, subject = line.partition("\t")
        if sha:
            commits.append({"sha": sha, "subject": subject})
    ctx["commits"] = commits
    ctx["touching"] = bool(commits)
    changed = run_git(repo, ["log", "--name-only", "--format=",
                             "%s..HEAD" % base, "--"] + ctx["pathspec"])
    ctx["changed_committed"] = parse_git_name_list(changed)
    ctx["changed_any"] = ctx["changed_committed"] | worktree_changes(
        repo, base, ctx["pathspec"])
    if entry["commit_required"]:
        ctx["implement_complete"] = bool(commits)
    return ctx


def nonempty_files(directory):
    count, total = 0, 0
    try:
        for base, _dirs, files in os.walk(str(directory)):
            for name in files:
                try:
                    size = (Path(base) / name).stat().st_size
                except OSError:
                    continue
                if size > 0:
                    count += 1
                    total += size
    except OSError:
        return 0, 0
    return count, total


def artifact_item(spec_dir, rel):
    missing = {"path": rel, "required": True, "status": "missing", "size": 0}
    if spec_dir is None:
        return dict(missing)
    target = Path(spec_dir) / rel
    if rel.endswith("/"):
        if not target.is_dir():
            return dict(missing)
        count, total = nonempty_files(target)
        if count == 0:
            return dict(missing)
        return {"path": rel, "required": True, "status": "present",
                "size": total}
    try:
        size = target.stat().st_size
    except OSError:
        return dict(missing)
    if not target.is_file() or size <= 0:
        return dict(missing)
    return {"path": rel, "required": True, "status": "present", "size": size}


def na_artifacts():
    return {
        "status": "na", "value_state": "na", "stage": None, "complete": None,
        "commit_required": None, "no_change_allowed": None, "items": [],
    }


def artifacts_block(stage, spec_dir, commit_ctx, dispatched):
    if not dispatched:
        return na_artifacts()
    entry = STAGE_ARTIFACTS.get(stage) if stage else None
    readable = spec_dir is not None and Path(spec_dir).is_dir()
    if entry is None:
        # C-56: no artifact map for an unknown stage; never substitute one.
        return {
            "status": "present" if readable else "missing",
            "value_state": "unknown" if readable else "na",
            "stage": stage, "complete": None, "commit_required": None,
            "no_change_allowed": None, "items": [],
        }
    base_state = commit_ctx.get("base_state")
    if stage == "implement":
        # C-60: completeness is code/test commit evidence; artifacts is `na`.
        complete = commit_ctx.get("implement_complete")
        return {
            "status": "na",
            "value_state": "known" if complete is not None else "unknown",
            "stage": stage,
            "complete": complete,
            "commit_required": True,
            "no_change_allowed": False,
            "items": [],
        }
    items = [artifact_item(spec_dir, rel) for rel in entry["artifacts"]]
    present_all = all(item["status"] == "present" for item in items)
    complete = present_all
    value_state = "known"
    if not entry["artifacts"]:
        # C-53: analyze has no required file artifact -> vacuous truth.
        complete = True
    elif base_state == "missing":
        # C-54: no baseline recorded -> completeness is not judgeable.
        complete = None
        value_state = "unknown"
    elif stage == "checklist":
        # C-54: pre-existing checklist files alone are not completeness.
        if base_state != "resolved" or commit_ctx.get("changed_any") is None:
            complete = None
            value_state = "unknown"
        else:
            complete = present_all and bool(commit_ctx["changed_any"])
    if not readable:
        return {
            "status": "missing",
            "value_state": "na",
            "stage": stage,
            "complete": None if base_state == "missing" else False,
            "commit_required": entry["commit_required"],
            "no_change_allowed": entry["no_change_allowed"],
            "items": items,
        }
    return {
        "status": "present",
        "value_state": value_state,
        "stage": stage,
        "complete": complete,
        "commit_required": entry["commit_required"],
        "no_change_allowed": entry["no_change_allowed"],
        "items": items,
    }


def commits_block(commit_ctx, dispatched):
    if not dispatched:
        return {"status": "na", "value_state": "na", "base": None,
                "pathspec": [], "commits": [], "touching": None}
    required = commit_ctx.get("commit_required")
    if required is None:
        return {"status": "missing", "value_state": "na", "base": None,
                "pathspec": [], "commits": [], "touching": None}
    if required is False:
        # C-57: commit_required=false -> status=na (treated as commit-ready).
        return {"status": "na", "value_state": "na",
                "base": commit_ctx.get("base"), "pathspec": [],
                "commits": [], "touching": None}
    base_state = commit_ctx.get("base_state")
    if base_state in ("missing", "unresolved"):
        # C-57: never fall back to HEAD / "the most recent commit".
        return {"status": "present", "value_state": "unknown",
                "base": commit_ctx.get("base"),
                "pathspec": commit_ctx.get("pathspec") or [],
                "commits": [], "touching": None}
    if not commit_ctx.get("repo_readable"):
        return {"status": "missing", "value_state": "na",
                "base": commit_ctx.get("base"),
                "pathspec": commit_ctx.get("pathspec") or [],
                "commits": [], "touching": None}
    return {"status": "present", "value_state": "known",
            "base": commit_ctx.get("base"),
            "pathspec": commit_ctx.get("pathspec") or [],
            "commits": commit_ctx.get("commits") or [],
            "touching": commit_ctx.get("touching")}


def artifacts_ready_for_state(artifacts, stage):
    """File-level "产物齐备" used by the FR-004 derived rules. It deliberately
    recomputes presence from `items` instead of reading `complete`, because C-54
    keeps `complete=null` when the commit baseline is unknown while a DONE
    verdict still needs the file side of completeness (C1a residual risk)."""
    if artifacts.get("status") == "na" and stage != "implement":
        return None
    if stage == "implement":
        return artifacts.get("complete")
    items = artifacts.get("items") or []
    if items:
        return all(item["status"] == "present" for item in items)
    if stage in STAGE_ARTIFACTS and not STAGE_ARTIFACTS[stage]["artifacts"]:
        return True
    return None


def missing_artifacts_of(artifacts):
    return [item["path"] for item in artifacts.get("items") or []
            if item["status"] != "present"]


def uncommitted_artifacts_of(artifacts, commit_ctx):
    """C-59: only computable with a known baseline. A no_change_allowed stage
    with no change since the baseline has nothing to commit (C-46 row 2)."""
    if commit_ctx.get("base_state") != "resolved":
        return []
    if artifacts.get("status") != "present":
        return []
    changed_any = commit_ctx.get("changed_any") or set()
    committed = commit_ctx.get("changed_committed") or set()
    no_change_allowed = bool(artifacts.get("no_change_allowed"))
    if no_change_allowed and not changed_any:
        return []
    uncommitted = []
    for item in artifacts.get("items") or []:
        if item["status"] != "present":
            continue
        rel = item["path"]
        relative = None
        pathspec = commit_ctx.get("pathspec") or []
        for candidate in pathspec:
            if candidate.endswith(rel) or ("/" + rel) in candidate:
                relative = candidate
                break
        if relative is None:
            continue
        prefix = relative.rstrip("/") + "/"
        hits = {path for path in committed
                if path == relative or path.startswith(prefix)}
        if not hits:
            uncommitted.append(rel)
    return uncommitted


def false_completion_of(sentinel_present, artifacts):
    """C-31/C-42: sentinel present and at least one required artifact missing.
    `complete=null` (no baseline) is not "incomplete" and never triggers it."""
    return bool(sentinel_present and artifacts.get("complete") is False)


# ---------------------------------------------------------------------------
# Watcher delegation (T012 / C-14/C-15)
#
# Only called with an active watch target, when the line was dispatched, no
# --probe was given, and never when unattributable evidence coexists with stale
# signals. verdict / rc / reason / attribution are parsed from the WATCH line;
# an unavailable watcher is expressed as the tri-state envelope, never as a
# fabricated verdict and never as DEAD.
# ---------------------------------------------------------------------------

def no_target_verdict():
    return {
        "present": False, "status": "na", "value_state": "na",
        "verdict": None, "reason": None, "exit_code": None,
        "attribution": None, "detail": None,
    }


def unavailable_verdict(detail):
    return {
        "present": False, "status": "missing", "value_state": "na",
        "verdict": None, "reason": "unavailable", "exit_code": None,
        "attribution": None, "detail": detail,
    }


def parse_watch_line(text):
    for line in (text or "").splitlines():
        if line.startswith("WATCH "):
            fields = {}
            for token in line.split()[1:]:
                if "=" in token:
                    key, _, value = token.partition("=")
                    fields.setdefault(key, value)
            return fields
    return None


def active_watch_target(view, spine, fp):
    """C-14: pid/status record present, sentinel present, or stage_started_at
    readable."""
    for key in ("pid", "status"):
        path = fp.get(key)
        if path is not None and path.is_file():
            return True
    if view["sentinel_present"]:
        return True
    return spine_field(spine, "stage_started_at") is not None


def delegate_watcher(args, paths, spine, registry, raw_registry, fp, view,
                     signals, metas, stale, dispatched, now):
    if args.probe or not dispatched:
        return no_target_verdict()
    if not active_watch_target(view, spine, fp):
        return no_target_verdict()
    script = args.watch_script
    if not script or not Path(script).is_file():
        return unavailable_verdict("script-missing")

    current_run = spine_field(spine, "run_id")
    if current_run is None:
        current_run = registry.get("run_id")
    pins = [name for name in ("pid", "status")
            if signals.get(name, {}).get("status") == "present"
            and metas.get(name, {}).get("run") == current_run
            and current_run is not None]
    meta_path = first_meta_path(raw_registry)
    attributed = bool(current_run is not None and (meta_path or len(pins) == 2))

    if not attributed and stale:
        return unavailable_verdict("stale-evidence")

    stage = args.stage or registry.get("stage")
    cmd = ["bash", str(script), "--once",
           "--pid-file", str(fp.get("pid")),
           "--status-file", str(fp.get("status")),
           "--log", str(fp.get("log"))]
    sentinel = sentinel_literal(stage)
    if sentinel:
        cmd += ["--sentinel", sentinel]
    heartbeat = fp.get("heartbeat")
    if heartbeat is not None and heartbeat.is_file():
        cmd += ["--heartbeat", str(heartbeat)]
    deadline = spine_field(spine, "stage_deadline_epoch")
    if deadline is not None:
        cmd += ["--deadline-epoch", str(deadline)]
    if stage:
        cmd += ["--stage", stage]
    if attributed:
        cmd += ["--line-id", args.line_id, "--run-id", str(current_run)]
        registry_dir = paths.get("registry_dir")
        if registry_dir is not None and Path(registry_dir).is_dir():
            cmd += ["--registry", str(registry_dir)]
        if meta_path:
            cmd += ["--meta", meta_path]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=420)
    except subprocess.TimeoutExpired:
        return unavailable_verdict("timeout")
    except (OSError, subprocess.SubprocessError):
        return unavailable_verdict("invocation-failed")

    parsed = parse_watch_line(proc.stdout or "")
    if parsed is None:
        return unavailable_verdict("unparseable")
    verdict = parsed.get("verdict")
    if not verdict or verdict == "USAGE":
        return unavailable_verdict("usage")
    rc = to_int(parsed.get("rc"))
    return {
        "present": True,
        "status": "present",
        "value_state": "known",
        "verdict": verdict,
        "reason": parsed.get("reason"),
        "exit_code": rc if rc is not None else proc.returncode,
        "attribution": parsed.get("attribution"),
        "detail": None,
    }


# ---------------------------------------------------------------------------
# Dispatch evidence + not-dispatched short circuit (C-35/C-36)
# ---------------------------------------------------------------------------

def four_piece_any_exists(fp):
    for key in ("pid", "status", "log", "heartbeat", "watchbeat"):
        path = fp.get(key)
        if path is not None and path.is_file():
            return True
    return False


def has_dispatch_evidence(registry, fp, view):
    """C-36: Registry stage/attempt, any four-piece file, sentinel or commit
    evidence proves a dispatch happened; a missing spine is then a gap, never
    "not dispatched"."""
    if registry.get("stage"):
        return True
    if four_piece_any_exists(fp):
        return True
    if view.get("sentinel_present"):
        return True
    return False


def not_dispatched(probe_mode, spine, registry, fp, view):
    """C-35: every condition must hold, and a non-empty spine_state excludes it
    even when stage_started_at and the four-piece files are absent."""
    if probe_mode:
        return False
    if spine.get("state"):
        return False
    if spine_field(spine, "stage_started_at") is not None:
        return False
    if four_piece_any_exists(fp):
        return False
    if view.get("sentinel_present"):
        return False
    if has_dispatch_evidence(registry, fp, view):
        return False
    return True


# ---------------------------------------------------------------------------
# Derived loop_state (T013) — mirror of requirements.md FR-004 (the owner)
# ---------------------------------------------------------------------------

def derive_loop_state(view, watch, artifacts, not_dispatched_flag,
                      evidence_gap, remote_unreachable):
    if remote_unreachable:
        return "STALLED", "remote-unreachable", "derived"
    if not_dispatched_flag:
        return "UNKNOWN", "not-dispatched", "derived"
    if watch.get("present"):
        # FR-004 watcher invariant: verbatim, never rewritten.
        return watch.get("verdict"), "watcher-verdict", "watcher"
    if evidence_gap:
        return "UNKNOWN", "evidence-gap", "derived"
    ready = artifacts_ready_for_state(artifacts, artifacts.get("stage"))

    state = view["spine_state"]
    if state == "stalled":
        return "STALLED", "spine-stalled", "derived"
    if state == "reentry-required":
        return "REENTRY_REQUIRED", "spine-reentry-required", "derived"

    if view["exit_record"] or view["pid_dead"]:
        if view["anomaly_last"]:
            return "ANOMALY", "anomaly-line", "derived"
        if view["exit_record"]:
            if view["exit_code"] != 0:
                return "FAILED", "exit-nonzero", "derived"
            if view["sentinel_present"] and ready is True:
                return "DONE", "sentinel-and-artifacts", "derived"
            return "INCOMPLETE", "exit-zero-incomplete", "derived"

    if not view["exit_record"] and view["sentinel_present"]:
        if ready is True:
            return "DONE", "sentinel-no-exit", "derived"
        return "INCOMPLETE", "sentinel-no-exit", "derived"

    if not view["exit_record"] and view["pid_dead"]:
        return "DEAD", "dead-no-exit-record", "derived"

    if view["deadline_overrun"]:
        return "TIMEOUT", "deadline-overrun", "derived"

    if not view["pid_present"] and not view["exit_record"] \
            and view["start_grace_passed"]:
        return "NO_SIGNAL", "no-signal", "derived"

    if view["pid_alive"] is True or view["heartbeat_fresh"] is True:
        return "RUNNING", "running", "derived"

    return "UNKNOWN", "unknown", "derived"


# ---------------------------------------------------------------------------
# Read-only detectors (T014 / C-33/C-34/C-40/C-41/C-42/C-43/C-44)
# heartbeat-stalled and lifecycle-spine-violation keep their vocabulary and
# missing/unknown semantics but are 065b's to detect — never emitted here.
# ---------------------------------------------------------------------------

def finding(form, detail, evidence):
    return {
        "form": form,
        "detail": detail,
        "evidence": evidence,
        "detector": "065a",
    }


def signal_pointer(name, signals):
    path = signals.get(name, {}).get("path")
    return {"signal": name, "path": path}


def detect_interruptions(view, artifacts, stale, signals, dispatched,
                         remote_unreachable, probe_path):
    findings = []
    if remote_unreachable:
        findings.append(finding(
            "remote-unreachable",
            "probe reported the remote evidence host unreachable",
            [{"signal": "probe", "path": probe_path}],
        ))
    if not dispatched and not remote_unreachable:
        return findings

    running, terminal = running_and_unterminated(view)
    if running and not terminal:
        if not view["watchbeat_present"]:
            findings.append(finding(
                "unwatched",
                "stage is running and no watchbeat marker exists",
                [signal_pointer("watchbeat", signals),
                 signal_pointer("heartbeat", signals)],
            ))
        elif view["watchbeat_fresh"] is False:
            findings.append(finding(
                "unwatched",
                "stage is running and the watchbeat marker is past its window",
                [signal_pointer("watchbeat", signals)],
            ))

    if not view["exit_record"] and view["pid_present"] and view["pid_dead"]:
        findings.append(finding(
            "dead-no-exit-record",
            "pid record exists, the process is gone and no exit record was "
            "written",
            [signal_pointer("pid", signals), signal_pointer("status", signals)],
        ))

    if (view["deadline_overrun"] and view["pid_alive"] is True
            and not view["exit_record"] and not view["sentinel_present"]):
        findings.append(finding(
            "deadline-overrun-live",
            "stage deadline plus grace has passed while the process is still "
            "alive and no terminal evidence exists",
            [signal_pointer("pid", signals),
             signal_pointer("heartbeat", signals)],
        ))

    if artifacts.get("complete") is True and not view["sentinel_present"]:
        findings.append(finding(
            "artifacts-without-completion",
            "all required stage artifacts are complete but no final-line "
            "sentinel exists",
            [{"signal": "artifacts", "path": artifacts.get("path")}],
        ))

    for reason in STALE_REASONS:
        group = [entry for entry in stale if entry["reason"] == reason]
        if not group:
            continue
        findings.append(finding(
            "stale-signal",
            "%d signal file(s) fail the current attempt's attribution (%s) and "
            "are excluded from this evaluation" % (len(group), reason),
            [{"signal": entry["signal"], "path": entry["path"]}
             for entry in group],
        ))
    return findings


# ---------------------------------------------------------------------------
# Recovery suggestion (T015 owns C-46..C-49). Only the three pre-branches are
# implemented here; the candidate ladder lands with T015.
# ---------------------------------------------------------------------------

def suggest_action(loop_state, loop_state_reason, view, artifacts,
                   not_dispatched_flag, evidence_gap, remote_unreachable):
    if not_dispatched_flag:
        return "none", "not-dispatched", [], []
    if remote_unreachable:
        return "stop", "remote-unreachable", [], []
    if evidence_gap:
        return "stop", "evidence-gap", [], []
    # TODO(T015): C-46 candidate ladder (rows 3-13), C-47 attempt limit,
    # C-48 salvage gate, C-49 live-TIMEOUT watch priority.
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

def build_envelope(args, paths, parts):
    spine = parts["spine"]
    registry = parts["registry"]
    watch = parts["watch"]
    return {
        "schema_version": SCHEMA_VERSION,
        "line_id": args.line_id,
        "run_id": parts["run_id"],
        "stage": parts["stage"],
        "loop_state": parts["loop_state"],
        "verdict_source": parts["verdict_source"],
        "loop_state_reason": parts["loop_state_reason"],
        "watch_verdict": watch,
        "recovery_action": parts["action"],
        "recovery_reason": parts["action_reason"],
        "recovery_decision": {
            "action": parts["action"],
            "reason": parts["action_reason"],
            "preconditions": parts["preconditions"],
            "blocked_by": parts["blocked_by"],
        },
        "false_completion": parts["false_completion"],
        "spine": spine,
        "registry": registry,
        "paths": {
            "state_dir": str(paths["state_dir"]) if paths["state_dir"] else None,
            "spec_dir": str(paths["spec_dir"]) if paths["spec_dir"] else None,
            "repo": str(paths["repo"]) if paths["repo"] else None,
            "spine": str(paths["spine"]) if paths["spine"] else None,
            "probe": paths["probe"],
        },
        "thresholds": parts["thresholds"],
        "evidence": parts["evidence"],
        "interruptions": parts["interruptions"],
        "missing_artifacts": parts["missing_artifacts"],
        "uncommitted_artifacts": parts["uncommitted_artifacts"],
        "stale_signals": parts["stale"],
        "evaluated_at": now_iso_utc(),
    }


def spine_consistent(spine, loop_state):
    """C-39: report only — never pick one side."""
    last_verdict = spine_field(spine, "last_verdict")
    if loop_state is None or last_verdict is None:
        return None
    return str(last_verdict).strip().upper() == str(loop_state).strip().upper()


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
    now = now_epoch()
    paths, registry, raw_registry = resolve_paths(args)
    spine = read_spine(paths)
    stage = args.stage or registry.get("stage")
    threshold_set = resolve_thresholds(args, args.watch_script)
    fp = four_piece_paths(paths["state_dir"] if paths["state_dir"] else None,
                          args.line_id, stage)

    probe_mode = bool(args.probe)
    # Without a stage the four-piece names cannot be built: no per-stage
    # evidence is expected, so the shells stay `na` (never missing/guessed).
    if not fp:
        signals = {
            "pid": na_signal(PID_FIELDS),
            "status": na_signal(STATUS_FIELDS),
            "log": na_signal(LOG_FIELDS),
            "heartbeat": na_signal(HEARTBEAT_FIELDS),
            "watchbeat": na_signal(WATCHBEAT_FIELDS),
            "hook": hook_signal(),
        }
        metas = {}
    else:
        signals, metas = collect_signals(
            fp, spine, stage, threshold_set, True, now)

    stale, current_run = detect_stale_signals(
        metas, spine, raw_registry, signals)
    stale_names = {entry["signal"] for entry in stale}
    view = build_view(signals, stale_names, spine, threshold_set, now)
    view["sentinel_present"] = bool(
        ev_value(signals, stale_names, "log", "sentinel_present"))

    nd = not_dispatched(probe_mode, spine, registry, fp, view)
    if nd:
        signals = {
            "pid": na_signal(PID_FIELDS),
            "status": na_signal(STATUS_FIELDS),
            "log": na_signal(LOG_FIELDS),
            "heartbeat": na_signal(HEARTBEAT_FIELDS),
            "watchbeat": na_signal(WATCHBEAT_FIELDS),
            "hook": hook_signal(),
        }
        stale = []
        stale_names = set()
        view = build_view(signals, stale_names, spine, threshold_set, now)

    dispatched = not nd
    evidence_gap = bool(dispatched and spine.get("status") != "present")

    commit_ctx = commit_context(stage, paths["spec_dir"], paths["repo"], spine,
                                dispatched)
    artifacts = artifacts_block(stage, paths["spec_dir"], commit_ctx,
                                dispatched)
    commits = commits_block(commit_ctx, dispatched)
    missing_artifacts = missing_artifacts_of(artifacts)
    uncommitted_artifacts = uncommitted_artifacts_of(artifacts, commit_ctx)
    false_completion = false_completion_of(
        view["sentinel_present"], artifacts)

    watch = delegate_watcher(args, paths, spine, registry, raw_registry, fp,
                             view, signals, metas, stale, dispatched, now)
    loop_state, loop_state_reason, verdict_source = derive_loop_state(
        view, watch, artifacts, nd, evidence_gap, False)
    interruptions = detect_interruptions(
        view, artifacts, stale, signals, dispatched, False, None)

    action, action_reason, preconditions, blocked_by = suggest_action(
        loop_state, loop_state_reason, view, artifacts, nd, evidence_gap, False)

    spine["consistent"] = spine_consistent(spine, loop_state)

    evidence = {"evidence_source": "local"}
    for name in ("pid", "status", "log", "heartbeat", "watchbeat", "hook"):
        evidence[name] = signals[name]
    evidence["artifacts"] = artifacts
    evidence["commits"] = commits

    parts = {
        "spine": spine,
        "registry": registry,
        "run_id": (registry.get("run_id")
                   if registry.get("run_id") is not None
                   else spine_field(spine, "run_id")),
        "stage": stage,
        "loop_state": loop_state,
        "verdict_source": verdict_source,
        "loop_state_reason": loop_state_reason,
        "watch": watch,
        "action": action,
        "action_reason": action_reason,
        "preconditions": preconditions,
        "blocked_by": blocked_by,
        "false_completion": false_completion,
        "thresholds": threshold_set,
        "evidence": evidence,
        "interruptions": interruptions,
        "missing_artifacts": missing_artifacts,
        "uncommitted_artifacts": uncommitted_artifacts,
        "stale": stale,
    }
    envelope = build_envelope(args, paths, parts)
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
                       "state dir and the repo working tree"
                       % (args.out, violation))
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
