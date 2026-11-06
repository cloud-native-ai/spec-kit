#!/usr/bin/env python3
"""status-digest.py — current-state digest, reporting-obligation guard, status line (087).

One stdlib-only file with **exactly three actions** (contract ``status-digest.contract.md`` C-41):

* ``--action digest`` — render the bounded current-state summary;
* ``--action guard``  — judge the mechanically decidable propositions of the reporting obligation and report each
  with a named status (``pass`` / ``fail`` / ``not-evaluated`` plus a reason);
* ``--action report`` — render one status line from the owner's four labels plus attribution and the profile in force.

All three share **one reader** (``read_state`` and the functions under it). A second parser or a second renderer is
the defect C-41 names, so no action re-reads a registry entry by a different code path.

Authority map (this file owns no rule; it names the owner of each):

* The propositions the guard decides — their ids and their subjects — are owned by
  ``.specify/specs/087-speckit-visualization/contracts/reporting-obligations.contract.md`` C-01…C-13. This file
  names each proposition by id and states only *what it reads on disk*; it restates no proposition.
* The reporting obligation itself (scope predicate, cadence default, seat obligation, master duty, transition
  triggers, digest contract, machinery prohibition) is owned by ``shared/guidelines/reporting-obligations.md``.
* The content floor, the cadence anchor and the interactive default are owned by
  ``shared/guidelines/progress-reporting.md``.
* The artifact triplet and the three execution modes are owned by ``shared/definitions/subagent-definitions.md``.
* The stall threshold numbers are owned by ``skills/internal/create-team/references/patterns.md`` § Monitoring →
  Stall Detection; this file carries none of them.
* The line state vocabulary is owned by ``skills/external/sdd-loop-driver/scripts/line-registry.py``
  (``STATE_VALUES`` / ``ACTIVE_STATES``); this file never re-enumerates it — it projects whatever the entry says and
  derives activity from the same two names, which it reads from that engine's source.

  **The one legal duplicate (contract ``ownership-map.contract.md`` C-47).** The registry directory resolution order
  below restates ``line-registry.py``'s ``resolve_registry_dir`` because this script MUST NOT import the engine
  (``plan.md`` § Technical Context: a direct import would couple the digest to an internal module path rather than to
  its JSON on disk). That restatement is the single duplicate this feature is allowed, and it is marked here.

Read-only boundary (contract C-42, ``data-model.md`` E7): every input is opened for reading only. This file never
writes, never renames, never creates a directory, never spawns a process and never touches the network — those
properties are asserted by ``tests/unit/test_status_digest_unit.py`` and audited by the ``RO-13`` proposition.

Exit statuses, closed (contract C-45):

==========================  ==============================================================
``--action digest``
``0``                       a digest was rendered with at least one entry
``3``                       nothing active — the explicit ``nothing-running`` rendering
``2``                       input error (unreadable registry, unparsable entry, bad arguments)
``--action guard``
``0``                       zero findings
``1``                       at least one finding (a ``fail``)
``2``                       input error
``--action report``
``0``                       one status line was rendered
``2``                       input error
==========================  ==============================================================
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------- declared constants
#: The digest's entry cap default. Owner of this value: this constant (contract
#: ``ownership-map.contract.md`` C-47 row "Digest cap default"); overridable per invocation with ``--cap``.
DEFAULT_CAP = 20
CAP_ENV = "SPECIFY_STATUS_DIGEST_CAP"

#: The stale bound default: an entry whose last-observed activity is older than this is marked stale with its age.
#: Owner of this value: this constant (contract C-47 row "Digest stale bound default"). No other file carries it.
DEFAULT_STALE_BOUND_SECONDS = 900

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_INPUT_ERROR = 2
EXIT_NOTHING_ACTIVE = 3

REPO_ROOT = Path(__file__).resolve().parents[2]
# Guard against the `.specify/scripts/python/` mirror copy doubling the projection (the same trap
# ``sync-mirrors.py`` documents): a directory named `.specify` is never a repository root.
if REPO_ROOT.name == ".specify":
    REPO_ROOT = REPO_ROOT.parent

OWNER_DOC = Path("shared") / "guidelines" / "reporting-obligations.md"
PROGRESS_REPORTING_DOC = Path("shared") / "guidelines" / "progress-reporting.md"
SUBAGENT_DEFINITIONS_DOC = Path("shared") / "definitions" / "subagent-definitions.md"
PATTERNS_DOC = Path("skills") / "internal" / "create-team" / "references" / "patterns.md"
LINE_REGISTRY_ENGINE = Path("skills") / "external" / "sdd-loop-driver" / "scripts" / "line-registry.py"
COMMAND_TEMPLATE = Path("templates") / "commands" / "status.md"

NOTHING_RUNNING = "nothing-running"
DASH = "-"

#: The reporting profile names the owner declares (`data-model.md` E6, contract ``status-report.contract.md`` C-30).
PROFILE_LONG_RUN = "long-run"
PROFILE_INTERACTIVE = "interactive"

#: The four content-element labels the owner names (definitions reached by anchor, contract C-23).
ELEMENT_LABELS = ("position", "delta", "remainder", "blocker")
NO_BLOCKER = "no blocker"

#: The nine prohibited machinery items of contract C-13, as the scan looks for them.
MACHINERY_TERMS = (
    "scheduler",
    "timer",
    "daemon",
    "dependency",
    "store",
    "console channel",
    "registry",
    "state spine",
    "ledger",
)

#: The two legal carrier forms (contract ``status-report.contract.md`` C-26).
CARRIER_CONSOLE = "console"

#: The three out-of-cadence transition classes (contract C-08) as a captured line set spells them.
TRANSITION_CLASSES = ("sub-flow failure", "stall crossing", "dispatch failure")

#: Interrogative / approval markers a status line must never carry (contract C-28).
GATE_MARKERS = (
    "?",
    "？",
    "approve",
    "approval",
    "waive",
    "waiver",
    "shall i",
    "may i",
    "please confirm",
    "批准",
    "豁免",
    "请确认",
)

#: The label convention a dispatched sub-flow's identity comes from (``data-model.md`` E3 / E7): its owner is
#: ``shared/definitions/subagent-definitions.md`` § External Dispatch Visibility Contract point 5. The pattern is
#: read here rather than copied there because the owner states the convention in prose, and the projection needs a
#: decidable form of it; the shape, not the rule, is what this constant fixes.
SUPERVISION_LABEL_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*--[A-Za-z0-9._-]+--[A-Za-z0-9._-]+$")

#: The triplet suffixes the visibility contract declares (point 3); the newest mtime among them is the sub-flow's
#: last observed activity (``data-model.md`` E3).
TRIPLET_SUFFIXES = (".live.log", ".jsonl", ".status")

#: The sub-flow state vocabulary (``data-model.md`` E3) — a projection of the visibility contract and the exit
#: record, not a new closed set. ``slow`` is deliberately absent: it is a qualifier on ``running``.
SUB_FLOW_STATES = ("running", "completed", "stalled", "failed")

#: The threshold row identity default: the row a dispatch that produced no manifest at all falls under. Row
#: identities are the owner table's own ``Condition`` cells (``data-model.md`` E4), so this string is an index into
#: the owner's table, never a threshold value.
MANDATORY_THRESHOLD_ROW = "No manifest created"


# ---------------------------------------------------------------- reader: registry resolution
def resolve_registry_dir() -> Path:
    """Resolve the line-registry directory, in the engine's documented order.

    ``$SPECIFY_LINE_REGISTRY_DIR`` → ``$XDG_STATE_HOME/spec-kit/lines`` → ``~/.local/state/spec-kit/lines``.

    This is the one legal duplicate of the engine's ``resolve_registry_dir`` (contract C-47): the script cannot import
    the engine, so the order is restated here and nowhere else in this script.
    """
    override = os.environ.get("SPECIFY_LINE_REGISTRY_DIR")
    if override:
        return Path(override).expanduser().resolve()
    xdg = os.environ.get("XDG_STATE_HOME")
    if xdg:
        return Path(xdg).expanduser().resolve() / "spec-kit" / "lines"
    home = Path(os.environ.get("HOME", "~")).expanduser()
    try:
        home = home.resolve()
    except OSError:
        pass
    return home / ".local" / "state" / "spec-kit" / "lines"


# ---------------------------------------------------------------- reader: engine vocabulary
def read_engine_vocabulary() -> dict:
    """Read ``STATE_VALUES`` / ``ACTIVE_STATES`` from the engine's own source.

    The two sets are the engine's (``ownership-map.contract.md`` C-47 row "Line state vocabulary"); this function
    parses them out of the engine file so the digest quotes them instead of carrying a second copy. A failed read is
    an *unavailable input*, reported as such — never silently replaced by a hard-coded set.
    """
    path = REPO_ROOT / LINE_REGISTRY_ENGINE
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {"error": "unreadable engine source %s: %s" % (LINE_REGISTRY_ENGINE, exc)}

    def literal(name: str) -> set:
        match = re.search(r"^%s\s*=\s*\{(.*?)\}" % re.escape(name), text, re.S | re.M)
        if not match:
            return set()
        return set(re.findall(r"[\"']([^\"']+)[\"']", match.group(1)))

    state_values = literal("STATE_VALUES")
    active_states = literal("ACTIVE_STATES")
    if not state_values or not active_states:
        return {
            "error": "engine source %s carries no readable STATE_VALUES / ACTIVE_STATES"
            % LINE_REGISTRY_ENGINE
        }
    return {"state_values": state_values, "active_states": active_states}


# ---------------------------------------------------------------- reader: one entry
def _parse_iso(value):
    if not isinstance(value, str) or not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _mtime_iso(path_text):
    if not path_text or path_text == DASH:
        return None
    try:
        stamp = os.stat(path_text).st_mtime
    except OSError:
        return None
    return datetime.fromtimestamp(stamp, timezone.utc)


def project_entry(entry: dict, now: datetime, stale_bound: int) -> dict:
    """Project one registry entry into the read-only shape the three actions share.

    Field ownership: identity / state / stage / timestamps come from the registry entry
    (``data-model.md`` E7); ``is_active`` derives from the engine's ``ACTIVE_STATES``; ``age`` and ``stale`` are
    computed here because they are functions of *now*, which no artifact owns.
    """
    triplet = {}
    for key in ("status_path", "log_path", "heartbeat_path"):
        value = entry.get(key)
        triplet[key] = value if isinstance(value, str) and value else DASH

    candidates = [_parse_iso(entry.get("updated_at"))]
    candidates.extend(
        _mtime_iso(triplet[key]) for key in ("status_path", "log_path", "heartbeat_path")
    )
    seen = [c for c in candidates if c is not None]
    last_activity = max(seen) if seen else None

    age_seconds = None
    if last_activity is not None:
        age_seconds = max(0, int((now - last_activity).total_seconds()))

    return {
        "line_id": entry.get("line_id"),
        "run_id": entry.get("run_id"),
        "project_dir": entry.get("project_dir"),
        "branch": entry.get("branch") or DASH,
        "stage": entry.get("stage") or DASH,
        "state": entry.get("state"),
        "updated_at": entry.get("updated_at") or DASH,
        "last_activity_at": last_activity.isoformat().replace("+00:00", "Z")
        if last_activity
        else DASH,
        "age_seconds": age_seconds,
        "age": format_duration(age_seconds),
        "stale": bool(age_seconds is not None and age_seconds > stale_bound),
        "stale_bound_seconds": stale_bound,
        "triplet": triplet,
    }


def format_duration(seconds) -> str:
    if seconds is None:
        return DASH
    seconds = int(seconds)
    if seconds < 60:
        return "%ds" % seconds
    if seconds < 3600:
        return "%dm%02ds" % (seconds // 60, seconds % 60)
    return "%dh%02dm" % (seconds // 3600, (seconds % 3600) // 60)


# ---------------------------------------------------------------- reader: the whole state
def read_state(cap: int, stale_bound: int, workspace: Path):
    """Read the registry once and return the projection every action consumes.

    Returns ``(state, error)``; ``error`` is a human-readable input-error string, never a traceback. ``state`` is the
    single reading: ``registry_dir``, ``entries`` (already workspace-filtered, ordered and capped), ``all_entries``,
    ``omitted``, ``cap``, ``stale_bound_seconds``, ``generated_at``, ``vocabulary``, ``now``.

    ``now`` is the single instant this reading was taken at. The digest's age, the supervision report's age and the
    stall judgement all measure against it, so one render is one clock reading rather than three (C-41's one-reading
    rule applied to time as well as to state).
    """
    registry_dir = resolve_registry_dir()
    now = datetime.now(timezone.utc)
    vocabulary = read_engine_vocabulary()

    if not registry_dir.is_dir():
        return None, "registry directory is unreadable: %s" % registry_dir

    try:
        paths = sorted(registry_dir.glob("*.json"))
    except OSError as exc:
        return None, "registry directory is unreadable: %s (%s)" % (registry_dir, exc)

    active_states = vocabulary.get("active_states") or set()
    raw = []
    for path in paths:
        try:
            with path.open("r", encoding="utf-8") as handle:
                entry = json.load(handle)
        except (OSError, ValueError) as exc:
            return None, "unparsable registry entry %s: %s" % (path, exc)
        if not isinstance(entry, dict):
            return None, "unparsable registry entry %s: not a JSON object" % path
        raw.append(entry)

    # Workspace rule (FR-011): only entries whose project_dir is this workspace are listed, and only they count
    # against the cap. An entry of another project is not rendered and carries no label of its own.
    def in_workspace(entry: dict) -> bool:
        value = entry.get("project_dir")
        if not isinstance(value, str) or not value:
            return False
        try:
            return Path(value).expanduser().resolve() == workspace
        except OSError:
            return False

    scoped = [e for e in raw if in_workspace(e)]
    projected = [project_entry(e, now, stale_bound) for e in scoped]
    for item in projected:
        item["is_active"] = item.get("state") in active_states

    # Deterministic order (contract C-43): active lines first, then descending last-activity time, ties by line_id.
    def sort_key(item):
        stamp = _parse_iso(item["last_activity_at"]) if item["last_activity_at"] != DASH else None
        epoch = stamp.timestamp() if stamp else 0.0
        return (0 if item["is_active"] else 1, -epoch, str(item["line_id"]))

    projected.sort(key=sort_key)
    omitted = max(0, len(projected) - cap)
    entries = projected[:cap]

    return {
        "registry_dir": str(registry_dir),
        "generated_at": now.isoformat().replace("+00:00", "Z"),
        "cap": cap,
        "stale_bound_seconds": stale_bound,
        "entries": entries,
        "all_entries": projected,
        "omitted": omitted,
        "vocabulary": vocabulary,
        "now": now,
    }, None


# ---------------------------------------------------------------- shared derivations
def profile_in_force(state) -> str:
    """The cadence profile selecting for this reading (``data-model.md`` E6, contract C-30).

    The selecting condition is E6's: at least one live status receiver — a reporter seat whose runtime execution is
    not omitted, or a supervising master holding at least one dispatched sub-flow. Neither is visible from a registry
    entry alone, so the reading reports the *observed* half it can decide: an active line is a live receiver by
    construction (it holds a concurrency slot), and its absence selects the interactive profile.
    """
    if any(item.get("is_active") for item in state["entries"]):
        return PROFILE_LONG_RUN
    return PROFILE_INTERACTIVE


def _read_text(rel_path: Path):
    path = REPO_ROOT / rel_path
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


# ---------------------------------------------------------------- action: digest
def render_digest(state) -> str:
    """Render the bounded summary, derived from the one reading (contracts C-42, C-43, C-44, C-45)."""
    if not state["entries"]:
        return NOTHING_RUNNING

    lines = [
        "generated_at=%s cap=%d stale_bound=%s profile=%s"
        % (
            state["generated_at"],
            state["cap"],
            format_duration(state["stale_bound_seconds"]),
            profile_in_force(state),
        )
    ]
    for item in state["entries"]:
        lines.append(
            "line_id=%s run_id=%s state=%s stage=%s age=%s stale=%s active=%s"
            % (
                item["line_id"] or DASH,
                item["run_id"] or DASH,
                item["state"] or DASH,
                item["stage"],
                item["age"],
                "yes" if item["stale"] else "no",
                "yes" if item["is_active"] else "no",
            )
        )
    if state["omitted"]:
        lines.append("omitted=%d" % state["omitted"])
    return "\n".join(lines)


def action_digest(args) -> int:
    workspace = Path(args.workspace).expanduser().resolve()
    state, error = read_state(args.cap, args.stale_bound, workspace)
    if error:
        print(error, file=sys.stderr)
        return EXIT_INPUT_ERROR

    if args.format == "json":
        payload = dict(state)
        payload["profile"] = profile_in_force(state)
        payload["state_summary"] = "active" if state["entries"] else NOTHING_RUNNING
        payload.pop("vocabulary", None)
        # ``now`` is the reading's clock, not a rendered field: it is consumed by the renderers and never serialized.
        payload.pop("now", None)
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_digest(state))

    return EXIT_OK if state["entries"] else EXIT_NOTHING_ACTIVE


# ---------------------------------------------------------------- action: report
def render_status_line(args) -> str:
    """Render one status line from the owner's four labels plus attribution and the profile in force.

    Shape (contract ``status-report.contract.md``):

    * attribution first — the structure slug and the run stamp (C-22), then the profile in force (C-30);
    * the trigger kind that produced this line (C-25): ``tick`` for a cadence line, ``boundary`` for the extra line a
      crossed stage boundary emits, ``transition:<sub-flow-id>`` for a significant state transition, and
      ``reporter-failure`` when the reporting loop could not emit (C-29);
    * the delay statement when the tick landed inside an indivisible step and was delivered at that step's next
      boundary (C-25 point 2) — the step is never split to keep the clock;
    * the four content-element labels, then the carrier that receives the line (C-26).

    The labels are named here; their definitions are reached by anchor to
    ``shared/guidelines/progress-reporting.md`` § 汇报内容下限 and are deliberately not restated (contract C-23).

    ``--transition`` replaces the trigger with that transition's own class, so a supervising flow reports a
    significant transition through this same line shape rather than growing a second status renderer
    (contract ``supervision-report.contract.md`` C-34).
    """
    state, _error = read_state(args.cap, args.stale_bound, Path(args.workspace).expanduser().resolve())
    # The profile in force is read from the state when the reading decides it. A mid-run loss of the live receiver
    # switches to `interactive` AT THE NEXT BOUNDARY and says so (contract C-30): `--profile` lets the emitting flow
    # record the switch, and `--profile-switch` carries the reason it switched, so the switch line states it rather
    # than a reader inferring it from a changed field value.
    profile = args.profile or (profile_in_force(state) if state else PROFILE_LONG_RUN)
    fields = [
        "structure=%s" % args.structure,
        "run=%s" % args.run_stamp,
        "trigger=%s"
        % (
            "transition:%s" % args.transition
            if args.transition
            else args.trigger
        ),
        "profile=%s" % profile,
    ]
    if args.transition:
        fields.append("class=%s" % args.transition)
    if args.cadence:
        # An override is recorded NEXT TO the profile, so a reader can tell an override from the definition (C-24).
        fields.append("cadence=%s" % args.cadence)
    if args.delay_reason:
        fields.append("delay=%s" % args.delay_reason)
    if args.profile_switch:
        fields.append("switch=%s" % args.profile_switch)
    fields.extend(
        [
            "position=%s" % args.position,
            "delta=%s" % args.delta,
            "remainder=%s" % args.remainder,
            "blocker=%s" % (args.blocker if args.blocker else NO_BLOCKER),
            "carrier=%s" % (args.carrier if args.carrier else CARRIER_CONSOLE),
        ]
    )
    return " | ".join(fields)


def action_report(args) -> int:
    for name in ("structure", "run_stamp", "position", "delta", "remainder"):
        if not getattr(args, name):
            print("--action report requires --%s" % name.replace("_", "-"), file=sys.stderr)
            return EXIT_INPUT_ERROR
    line = render_status_line(args)
    print(line)
    return EXIT_OK


# ---------------------------------------------------------------- reader: the stall threshold table
def read_threshold_rows():
    """Read the declared stall-threshold rows from their owner at render time.

    The numbers are owned by ``skills/internal/create-team/references/patterns.md`` § Monitoring → Stall Detection
    (``data-model.md`` E4); this function parses the table's ``Condition`` and ``Threshold`` cells so the projection
    can name a row and judge against its value without carrying either a copy of the table or a number of its own.
    A failed read is an *unavailable input*, reported as such — never replaced by a hard-coded default.
    """
    path = REPO_ROOT / PATTERNS_DOC
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, "unreadable threshold owner %s: %s" % (PATTERNS_DOC, exc)

    start = text.find("Stall Detection")
    if start < 0:
        return None, "threshold owner %s carries no Stall Detection section" % PATTERNS_DOC
    rows = {}
    for line in text[start:].splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if rows:
                break
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() == "condition" or set(cells[0]) <= set("-: "):
            continue
        row_id = cells[0]
        threshold = cells[1]
        # Only a row whose threshold cell *is* a duration can judge silence; a qualitative cell states a condition
        # (e.g. "manifest exists but deliverables empty") and is never a stall threshold.
        match = re.match(r"^\s*(\d+)\s*(s|sec|secs|seconds?|秒)\b", threshold, re.I)
        if not match:
            continue
        rows[row_id] = {
            "row": row_id,
            "threshold_cell": threshold,
            "threshold_seconds": int(match.group(1)),
        }
    if not rows:
        return None, "threshold owner %s carries no readable duration row" % PATTERNS_DOC
    return rows, None


def resolve_threshold(rows, row_id, override_seconds):
    """Resolve the E4 judgement reference: the named row, its declared value, and the override actually used.

    The override rule is C-24's, applied to the threshold: a per-run value replaces the declared one *and is
    recorded next to it*, so a reader can tell an override from the definition.
    """
    if rows is None:
        return None
    if row_id in rows:
        chosen = rows[row_id]
    elif override_seconds is not None:
        # No such row: the judgement's `judged_against` would not resolve, which `data-model.md` calls a defect;
        # the override keeps a reading available but the missing row is named.
        chosen = {"row": row_id, "threshold_cell": "(row not found)", "threshold_seconds": None}
    else:
        return None
    return {
        "row": chosen["row"],
        "threshold_cell": chosen["threshold_cell"],
        "declared_seconds": chosen["threshold_seconds"],
        "override_seconds": override_seconds,
        "value_seconds": override_seconds if override_seconds is not None else chosen["threshold_seconds"],
    }


# ---------------------------------------------------------------- reader: one supervised sub-flow
def project_sub_flow(label, triplet_dir, now, threshold):
    """Project one dispatched sub-flow into the E3 shape the supervision report renders.

    Field ownership (this function copies no rule):

    * ``label`` — the identity, from the visibility contract's label convention;
    * ``state`` — from the triplet and the exit record the visibility contract already declares: a ``.status`` line
      carrying ``exit=0`` is ``completed``, a non-zero ``exit=`` is ``failed``, and silence past the declared
      threshold is ``stalled``;
    * ``age`` — now minus the newest mtime among the triplet files;
    * ``slow`` — a qualifier on ``running``: not progressing *yet*, below the threshold. It is deliberately not a
      fifth state (``data-model.md`` E3's deviation note), so ``slow`` and ``stalled`` are never merged.
    """
    directory = Path(triplet_dir).expanduser()
    triplet_paths = {suffix: directory / (label + suffix) for suffix in TRIPLET_SUFFIXES}
    present = [path for path in triplet_paths.values() if path.is_file()]

    entry = {
        "label": label,
        "state": None,
        "age_seconds": None,
        "age": DASH,
        "slow": False,
        "exit_code": None,
        "triplet": {suffix: str(triplet_paths[suffix]) for suffix in TRIPLET_SUFFIXES},
        "triplet_present": len(present),
        "judged_against": None,
        "measured_silence": DASH,
        "transition": None,
    }

    if not present:
        # A dispatch that produced no part of its declared triplet is not running and cannot have completed:
        # the dispatch itself did not take hold.
        entry["state"] = "failed"
        return entry

    newest = max(path.stat().st_mtime for path in present)
    age_seconds = max(0, int(now - newest))
    entry["age_seconds"] = age_seconds
    entry["age"] = format_duration(age_seconds)
    entry["measured_silence"] = entry["age"]

    status_path = triplet_paths[".status"]
    if status_path.is_file():
        try:
            status_text = status_path.read_text(encoding="utf-8")
        except OSError:
            status_text = ""
        match = re.search(r"exit=(-?\d+)", status_text)
        if match:
            entry["exit_code"] = int(match.group(1))
            entry["state"] = "completed" if entry["exit_code"] == 0 else "failed"

    if entry["state"] is None:
        if threshold and threshold.get("value_seconds") is not None:
            entry["judged_against"] = threshold
            if age_seconds > threshold["value_seconds"]:
                entry["state"] = "stalled"
            else:
                entry["state"] = "running"
                entry["slow"] = True
        else:
            entry["state"] = "running"

    return entry


def project_supervision(sub_flows, expected_labels, now, threshold, transition, interval_elapsed):
    """Assemble the supervision projection: the rows, the closure defects, and the pre-tick transition.

    One reader backs both renderings (C-41's one-reading rule): the rows this returns are the same rows
    ``render_supervision`` prints and ``proposition_ro_06`` judges, so no second parser appears.
    """
    rows = [project_sub_flow(label, directory, now, threshold) for label, directory in sub_flows]
    by_label = {row["label"]: row for row in rows}

    # Presence is closure (C-33): a label the caller knows was dispatched but that produced no row is an omission,
    # named by that label — never a quietly smaller active set.
    omitted = [label for label in (expected_labels or []) if label not in by_label]

    # The transition classes (C-34), each decided from the row's own observed condition.
    if transition == "sub-flow failure":
        targets = [row for row in rows if row["state"] == "failed" and row["triplet_present"]]
    elif transition == "stall crossing":
        targets = [row for row in rows if row["state"] == "stalled"]
    elif transition == "dispatch failure":
        targets = [row for row in rows if row["triplet_present"] == 0]
    else:
        targets = []

    pre_tick = None
    if targets and not interval_elapsed:
        pre_tick = {
            "class": transition,
            "labels": [row["label"] for row in targets],
            "timing": "pre-tick (emitted before the next tick)",
        }

    return {"rows": rows, "omitted": omitted, "pre_tick": pre_tick, "threshold": threshold,
            "transition": transition, "interval_elapsed": interval_elapsed}


def parse_sub_flow_args(items):
    """Parse ``--sub-flow LABEL=TRIPLET_DIR`` values, judging each label against the declared convention."""
    sub_flows = []
    for item in items or []:
        if "=" not in item:
            return None, "--sub-flow expects LABEL=TRIPLET_DIR; got %r" % item
        label, directory = item.split("=", 1)
        if not SUPERVISION_LABEL_PATTERN.match(label):
            return None, (
                "--sub-flow label %r is not the declared convention"
                " `<team-slug>--<run-stamp>--<member-role>`" % label
            )
        sub_flows.append((label, directory))
    return sub_flows, None


def build_projection(args, now):
    """Build the supervision projection from the arguments, or ``(None, None)`` when no sub-flow was supplied."""
    sub_flows, error = parse_sub_flow_args(args.sub_flow)
    if error:
        return None, error
    if not sub_flows:
        return None, None
    rows, read_error = read_threshold_rows()
    threshold = resolve_threshold(rows, args.threshold_row, args.threshold_seconds)
    projection = project_supervision(
        sub_flows,
        args.expect_sub_flow or [],
        now.timestamp(),
        threshold,
        args.transition,
        args.interval_elapsed,
    )
    return projection, read_error


# ---------------------------------------------------------------- action: supervision report
def render_supervision(state, projection, format_age=format_duration) -> str:
    """Render one sub-flow row per dispatched flow, plus the pre-tick transition and the omission defects.

    Shape (contract ``supervision-report.contract.md`` C-32…C-35 and ``status-report.contract.md`` C-30):

    * ``structure`` / ``run`` / ``profile`` — the attribution pair and the profile in force, the same prefix the
      status line carries, so an interleaved report is still attributable;
    * one ``sub-flow=<label>`` row per dispatched flow carrying ``state=``, ``age=``, ``slow=`` and, where a
      judgement was made, ``judged_against=`` (the owner's table reachable by path), ``row=`` (the threshold row's
      own identity) and ``measured_silence=``;
    * an ``omitted:`` clause on a ``state=missing`` row per known-but-unreported dispatch — the omission named by
      its label, never silently absent;
    * a ``trigger=transition:<label>`` line per pre-tick transition, stating that it did not wait for the clock.

    The durations are rendered through the caller's formatter so this renderer shares one formatting rule with the
    digest (C-41's one-rendering rule: a second age renderer would let the two surfaces disagree about one duration).
    """
    fields = [
        "structure=%s" % (state["structure"] if state else DASH),
        "run=%s" % (state["run"] if state else DASH),
        "trigger=tick",
        "profile=%s" % (state["profile"] if state else PROFILE_LONG_RUN),
    ]
    # The tick line carries the four content elements like every other status line (contract C-23): its position is
    # that this is the tick's own report, its delta the number of sub-flows observed, and its remainder the number
    # still running. Without them this line would be a bare header whose reader learns nothing about the run.
    running = sum(1 for row in projection["rows"] if row["state"] in ("running", "stalled"))
    finished = sum(1 for row in projection["rows"] if row["state"] == "completed")
    failed = sum(1 for row in projection["rows"] if row["state"] == "failed")
    if projection["rows"]:
        fields.extend(
            [
                "position=%d dispatched sub-flow(s) watched (tick report)" % len(projection["rows"]),
                "delta=%d completed, %d running or stalled, %d failed since the last tick"
                % (finished, running, failed),
                "remainder=%d sub-flow(s) still active"
                % (running + (len(projection["omitted"]) if projection["omitted"] else 0)),
                "blocker=%s"
                % (
                    "sub-flow(s) dispatched but not reported: %s" % ", ".join(projection["omitted"])
                    if projection["omitted"]
                    else NO_BLOCKER
                ),
            ]
        )
    lines = [" | ".join(fields)]
    for row in projection["rows"]:
        parts = [
            "sub-flow=%s" % row["label"],
            "state=%s" % row["state"],
            "age=%s" % format_age(row["age_seconds"]),
            "slow=%s" % ("yes" if row["slow"] else "no"),
        ]
        if row["judged_against"]:
            judged = row["judged_against"]
            parts.extend(
                [
                    "judged_against=%s § Monitoring → Stall Detection"
                    % PATTERNS_DOC.as_posix(),
                    "row=%s" % judged["row"],
                    "threshold=%s"
                    % (
                        format_age(judged["override_seconds"])
                        if judged["override_seconds"] is not None
                        else judged["threshold_cell"]
                    ),
                    "override=%s"
                    % (
                        "yes (per-run value recorded beside the declared one)"
                        if judged["override_seconds"] is not None
                        else "none"
                    ),
                    "measured_silence=%s" % format_age(row["age_seconds"]),
                ]
            )
        parts.append("carrier=%s" % CARRIER_CONSOLE)
        lines.append(" | ".join(parts))
    for label in projection["omitted"]:
        # An omission says which flow it is, and what a reader should do about it — never only that something is
        # missing: `state=missing` is not one of the four projected states, it is the omission's own marker (C-33).
        lines.append(
            "sub-flow=%s | state=missing | omitted: dispatched but no row on this tick (C-33)"
            " | position=authored but never reported | delta=none observed on this tick"
            " | remainder=dispatch presumed alive; report it or declare it lost"
            " | blocker=this dispatch was not reportable on this tick | carrier=%s"
            % (label, CARRIER_CONSOLE)
        )
    if projection["pre_tick"]:
        for label in projection["pre_tick"]["labels"]:
            lines.append(
                "sub-flow=%s | trigger=transition:%s | class=%s | timing=%s | carrier=%s"
                % (label, label, projection["pre_tick"]["class"], projection["pre_tick"]["timing"],
                   CARRIER_CONSOLE)
            )
    return "\n".join(lines)


def _supervision_lines(projection, live, format_age):
    """The rendered supervision lines for one projection (empty when no sub-flow was supplied)."""
    if projection is None:
        return []
    return render_supervision(live, projection, format_age).splitlines()


def action_supervision(args) -> int:
    workspace = Path(args.workspace).expanduser().resolve()
    state, _error = read_state(args.cap, args.stale_bound, workspace)
    live = (
        dict(state, structure=args.structure, run=args.run_stamp, profile=profile_in_force(state))
        if state
        else {
            "structure": args.structure,
            "run": args.run_stamp,
            "profile": PROFILE_LONG_RUN,
            "now": datetime.now(timezone.utc),
        }
    )
    projection, error = build_projection(args, live["now"])
    if error:
        print(error, file=sys.stderr)
        return EXIT_INPUT_ERROR
    if projection is None:
        print("--supervision-report requires at least one --sub-flow", file=sys.stderr)
        return EXIT_INPUT_ERROR

    for line in _supervision_lines(projection, live, format_duration):
        print(line)

    verdicts = [
        proposition_ro_06(args.line_set, projection),
        proposition_ro_08(args.line_set, projection),
    ]
    return _emit_verdicts(verdicts, args.format)


def _emit_verdicts(verdicts, output_format) -> int:
    """Print the verdicts in the requested format and return the closed exit status (C-45)."""
    if output_format == "json":
        print(json.dumps({"action": "guard", "propositions": verdicts}, indent=2, sort_keys=True))
    else:
        for verdict in verdicts:
            print(
                "%s %s %s"
                % (verdict["proposition"], verdict["status"], verdict["reason"])
            )
        counts = {}
        for verdict in verdicts:
            counts[verdict["status"]] = counts.get(verdict["status"], 0) + 1
        print(
            "summary pass=%d fail=%d not-evaluated=%d"
            % (
                counts.get("pass", 0),
                counts.get("fail", 0),
                counts.get("not-evaluated", 0),
            )
        )
    return EXIT_FINDINGS if any(v["status"] == "fail" for v in verdicts) else EXIT_OK


# ---------------------------------------------------------------- action: guard
def _verdict(name: str, status: str, reason: str) -> dict:
    return {"proposition": name, "status": status, "reason": reason}


def _pass(name, reason):
    return _verdict(name, "pass", reason)


def _fail(name, reason):
    return _verdict(name, "fail", reason)


def _not_evaluated(name, reason):
    return _verdict(name, "not-evaluated", reason)


def proposition_ro_01(owner_text):
    name = "RO-01"
    if owner_text is None:
        return _not_evaluated(name, "owner document %s is unreadable" % OWNER_DOC)
    block = _declaration_block(owner_text)
    if block is None:
        return _fail(name, "owner document carries no single-source-of-truth declaration block")
    items = re.findall(r"^\s*\d+[.)]\s+\S", block, re.M)
    if len(items) != 8:
        return _fail(
            name,
            "owner declaration lists %d owned fact(s); the closed set is 8" % len(items),
        )
    return _pass(name, "owner declaration lists exactly 8 owned facts")


def proposition_ro_02(owner_text, sample_path):
    name = "RO-02"
    if owner_text is None:
        return _not_evaluated(name, "owner document %s is unreadable" % OWNER_DOC)
    if not sample_path:
        return _not_evaluated(name, "no seeded flow sample supplied (--flow-sample)")
    text = _read_text(Path(sample_path))
    if text is None:
        return _not_evaluated(name, "flow sample %s is unreadable" % sample_path)
    cases = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    unclassifiable = [ln for ln in cases if "in-scope" not in ln and "out-of-scope" not in ln]
    if unclassifiable:
        return _fail(name, "%d flow(s) carry no verdict in the sample" % len(unclassifiable))
    return _pass(name, "%d flow(s) classified, 0 unclassifiable" % len(cases))


def proposition_ro_03(owner_text):
    """The owner-literal scan: exactly one definition site, the two known prose hits whitelisted by path."""
    name = "RO-03"
    if owner_text is None:
        return _not_evaluated(name, "owner document %s is unreadable" % OWNER_DOC)
    whitelist = (
        "skills/external/draw-diagram/references/types/plantuml/references/howto/19-salt-diagram.md",
        "skills/external/improve-skills/references/skill-slimming-principles.md",
    )
    sites = []
    for root_name in ("shared", "templates", "skills", "agents"):
        root = REPO_ROOT / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".txt"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if "30 秒" in text or "30 seconds" in text:
                rel = path.relative_to(REPO_ROOT).as_posix()
                sites.append(rel)
    definition_sites = [rel for rel in sites if rel not in whitelist]
    expected = [OWNER_DOC.as_posix()]
    if definition_sites == expected:
        return _pass(name, "exactly one definition site: %s" % expected[0])
    return _fail(
        name,
        "expected definition sites %r, found %r (whitelisted prose hits: %d)"
        % (expected, definition_sites, len(sites) - len(definition_sites)),
    )


def proposition_ro_04(rosters, roster_baseline):
    name = "RO-04"
    population = [path for path, klass in roster_baseline or [] if klass == "in-population"]
    population.extend(rosters or [])
    population = [p for p in population if p]
    if not population:
        return _not_evaluated(
            name,
            "no roster path is in the obligation's population (no --roster supplied and the"
            " recorded name-list holds none)",
        )
    defects = []
    for path_text in population:
        text = _read_text(Path(path_text))
        if text is None:
            defects.append("%s: unreadable" % path_text)
            continue
        seats = len(re.findall(r"^\s*role:\s*reporter\b", text, re.M))
        has_reason = re.search(r"^\s*reporting-reason:\s*\S", text, re.M) is not None
        if seats == 0 and not has_reason:
            defects.append("%s: absent reporter seat and no recorded reason" % path_text)
        elif seats > 1:
            defects.append("%s: %d reporter seats" % (path_text, seats))
    if defects:
        return _fail(name, "; ".join(defects))
    return _pass(name, "%d roster path(s) in population, no named defect" % len(population))


def proposition_ro_05(owner_text, line_set_path):
    name = "RO-05"
    if owner_text is None:
        return _not_evaluated(name, "owner document %s is unreadable" % OWNER_DOC)
    if "汇报内容下限" not in owner_text:
        return _fail(name, "owner document carries no anchor to the content floor")
    if not line_set_path:
        return _not_evaluated(name, "no captured line set supplied (--line-set)")
    text = _read_text(Path(line_set_path))
    if text is None:
        return _not_evaluated(name, "captured line set %s is unreadable" % line_set_path)
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    if not lines:
        return _not_evaluated(name, "captured line set %s is empty" % line_set_path)
    missing = []
    for index, line in enumerate(lines, 1):
        for label in ELEMENT_LABELS:
            if ("%s=" % label) not in line:
                missing.append("line %d lacks %s" % (index, label))
    if missing:
        return _fail(name, "; ".join(missing))
    return _pass(name, "%d line(s) carry the four labels" % len(lines))


def proposition_ro_06(line_set_path, projection=None):
    name = "RO-06"
    if projection is not None:
        if not projection["rows"]:
            return _fail(name, "no per-sub-flow row was produced for the dispatches supplied")
        if projection["omitted"]:
            return _fail(
                name,
                "sub-flow(s) dispatched but absent from the report: %r" % (projection["omitted"],),
            )
        return _pass(name, "%d sub-flow row(s) present, 0 omitted" % len(projection["rows"]))
    if not line_set_path:
        return _not_evaluated(name, "no captured supervision report supplied (--line-set)")
    text = _read_text(Path(line_set_path))
    if text is None:
        return _not_evaluated(name, "captured supervision report %s is unreadable" % line_set_path)
    rows = [ln for ln in text.splitlines() if "sub-flow=" in ln]
    if not rows:
        return _fail(name, "no per-sub-flow row found in the captured supervision report")
    return _pass(name, "%d sub-flow row(s) present" % len(rows))


def proposition_ro_07(owner_text, projection=None):
    name = "RO-07"
    if projection is not None:
        threshold = projection["threshold"]
        if threshold is None:
            return _not_evaluated(
                name, "no threshold row resolved for this report (the owner table is unreadable)"
            )
        if threshold["value_seconds"] is None:
            return _fail(
                name,
                "the row %r does not resolve in the threshold owner and no per-run value was supplied"
                % threshold["row"],
            )
        return _pass(
            name,
            "row %r resolved from %s; value used %s"
            % (threshold["row"], PATTERNS_DOC.as_posix(), format_duration(threshold["value_seconds"])),
        )
    if owner_text is None:
        return _not_evaluated(name, "owner document %s is unreadable" % OWNER_DOC)
    if "Stall Detection" not in owner_text or PATTERNS_DOC.as_posix() not in owner_text:
        return _fail(name, "owner document does not anchor the stall threshold table")
    patterns = _read_text(PATTERNS_DOC)
    if patterns is None:
        return _not_evaluated(name, "threshold owner %s is unreadable" % PATTERNS_DOC)
    if "Stall Detection" not in patterns:
        return _fail(name, "threshold owner %s carries no Stall Detection section" % PATTERNS_DOC)
    # A second numeric threshold set inside the owner would be a duplicate owner, not a second reading. The cadence
    # literal is excluded by its line: the value this feature owns (C-03) is a cadence, and judging it here would
    # make RO-07 a second owner of C-03's fact — the two propositions have different subjects.
    threshold_literals = []
    for line in owner_text.splitlines():
        if THRESHOLD_EXCLUDE_MARKER in line:
            continue
        threshold_literals.extend(re.findall(r"\b\d+\s*(?:s|seconds?|秒)\b", line))
    if threshold_literals:
        return _fail(
            name, "owner document carries numeric threshold literal(s): %r" % (threshold_literals,)
        )
    return _pass(name, "threshold anchor resolves and the owner carries no numeric threshold")


#: The line carrying the cadence literal, which is C-03's fact and not this proposition's subject.
THRESHOLD_EXCLUDE_MARKER = "长跑档(long-run profile)"


def proposition_ro_08(line_set_path, projection=None):
    name = "RO-08"
    if projection is not None:
        if not projection["transition"]:
            return _not_evaluated(name, "no transition class was observed for this report")
        if not projection["pre_tick"]:
            return _fail(
                name,
                "a %r was observed after the tick had already elapsed; the report waited for the clock"
                % projection["transition"],
            )
        return _pass(
            name,
            "%r reported pre-tick for %r" % (projection["transition"], projection["pre_tick"]["labels"]),
        )
    if not line_set_path:
        return _not_evaluated(name, "no captured line set supplied (--line-set)")
    text = _read_text(Path(line_set_path))
    if text is None:
        return _not_evaluated(name, "captured line set %s is unreadable" % line_set_path)
    missing = [klass for klass in TRANSITION_CLASSES if klass not in text]
    if missing:
        return _fail(name, "transition class(es) absent from the line set: %r" % (missing,))
    return _pass(name, "all three transition classes present")


def proposition_ro_09(owner_text, state):
    name = "RO-09"
    if owner_text is None:
        return _not_evaluated(name, "owner document %s is unreadable" % OWNER_DOC)
    lowered_owner = owner_text.lower()
    for face in ("omitted", NOTHING_RUNNING, "stale"):
        if face not in lowered_owner:
            return _fail(name, "owner digest section does not state the %r face" % face)
    if state is None:
        return _not_evaluated(name, "no digest render is available to compare against the owner section")
    return _pass(name, "owner digest section stated; bounded/omitted/stale/nothing-running faces render")


def proposition_ro_10(line_set_path):
    name = "RO-10"
    if not line_set_path:
        return _not_evaluated(name, "no captured line set supplied (--line-set)")
    text = _read_text(Path(line_set_path))
    if text is None:
        return _not_evaluated(name, "captured line set %s is unreadable" % line_set_path)
    offenders = []
    for index, line in enumerate(text.splitlines(), 1):
        lowered = line.lower()
        for marker in GATE_MARKERS:
            if marker in lowered:
                offenders.append("line %d carries %r" % (index, marker))
                break
    if offenders:
        return _fail(name, "; ".join(offenders))
    return _pass(name, "no interrogative or approval marker in the line set")


def proposition_ro_11(line_set_path):
    name = "RO-11"
    if not line_set_path:
        return _not_evaluated(name, "no suppressed-tick fixture supplied (--line-set)")
    text = _read_text(Path(line_set_path))
    if text is None:
        return _not_evaluated(name, "fixture %s is unreadable" % line_set_path)
    if "reporter-failure" not in text:
        return _fail(name, "the fixture carries no reporter-failure line")
    return _pass(name, "the reporter-failure line is present")


def proposition_ro_12(args, run_record_path):
    name = "RO-12"
    carrier = args.carrier
    if not carrier:
        return _not_evaluated(name, "no run record carrier value supplied (--carrier)")
    if carrier == CARRIER_CONSOLE:
        return _pass(name, "carrier=%s (one of the two legal forms)" % carrier)
    if Path(carrier).suffix:
        return _pass(name, "carrier is a declared stream artifact path")
    return _fail(name, "carrier %r matches neither legal form" % carrier)


def proposition_ro_13(owner_text):
    name = "RO-13"
    if owner_text is None:
        return _not_evaluated(name, "owner document %s is unreadable" % OWNER_DOC)
    lowered = owner_text.lower()
    missing = [term for term in MACHINERY_TERMS if term not in lowered]
    if missing:
        return _fail(name, "prohibition clause omits %r" % (missing,))
    # The spawn audit reads the delivered script's AST, never its text: this file names the forbidden APIs in order
    # to describe the audit, and a text scan would therefore always find itself. An AST scan asks the only question
    # that matters — is any of them *called* or *imported*.
    if _delivered_script_spawns():
        return _fail(name, "delivered script imports or calls a process-spawn API")
    return _pass(name, "prohibition names all nine items; no spawn site in the delivered script")


#: Process-spawn APIs the machinery prohibition forbids on a delivery path (contract C-50).
SPAWN_MODULES = {"subprocess", "multiprocessing", "threading", "asyncio"}
SPAWN_CALLS = {"system", "fork", "execv", "execvp", "execl", "execle", "spawnl", "spawnv", "popen"}


def _delivered_script_spawns() -> bool:
    """AST-level audit: does this script import a spawn/thread module or call a spawn API?"""
    import ast

    try:
        source = Path(__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (OSError, SyntaxError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name.split(".")[0] in SPAWN_MODULES for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in SPAWN_MODULES:
                return True
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in SPAWN_CALLS:
                return True
    return False


def _declaration_block(text):
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        lowered = line.lower()
        if "single source of truth" in lowered or "唯一定义处" in line:
            start = index
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    block = []
    for line in lines[start:end]:
        stripped = line.lstrip()
        if stripped.startswith(">"):
            stripped = stripped[1:]
            if stripped.startswith(" "):
                stripped = stripped[1:]
        block.append(stripped)
    return "\n".join(block)


def _load_roster_baseline(path):
    """Load the recorded name-list, keeping only rows that carry a population class.

    The baseline file is prose around a classified list (``tasks.md`` T003 fixes its form: ``<path> | class=<…> |
    why``), so the parser keys on the ``class=`` cell rather than on any line that happens to contain a pipe. A row
    whose class is ``outside-the-population`` is recorded and not judged: the condition's owner is
    ``contracts/reporting-obligations.contract.md`` C-04, and an out-of-population roster is never made unrunnable.
    """
    text = _read_text(Path(path)) if path else None
    if text is None:
        return []
    rows = []
    for line in text.splitlines():
        if "class=" not in line or "|" not in line:
            continue
        parts = [cell.strip() for cell in line.split("|")]
        path_cell = parts[0].strip("` ").strip()
        if not path_cell or " " in path_cell or "<path>" in path_cell:
            continue
        class_cell = next((cell for cell in parts if cell.startswith("class=")), "")
        rows.append((path_cell, class_cell[len("class="):].strip()))
    return rows


def action_guard(args) -> int:
    owner_text = _read_text(OWNER_DOC)
    workspace = Path(args.workspace).expanduser().resolve()
    state, _error = read_state(args.cap, args.stale_bound, workspace)
    roster_baseline = _load_roster_baseline(args.roster_baseline)

    # The supervision projection is built from the SAME reading the digest consumed, and rendered by the same
    # renderer, so the report a supervising flow pastes into a captured line set is the one these verdicts judge
    # (C-41's one-reading rule; T022's "no second parser").
    now = state["now"] if state else datetime.now(timezone.utc)
    projection, projection_error = build_projection(args, now)
    if projection_error and projection is not None:
        print(projection_error, file=sys.stderr)
        return EXIT_INPUT_ERROR
    if projection is not None:
        live = (
            dict(state, structure=args.structure, run=args.run_stamp, profile=profile_in_force(state))
            if state
            else {"structure": args.structure, "run": args.run_stamp, "profile": PROFILE_LONG_RUN}
        )
        for line in _supervision_lines(projection, live, format_duration):
            print(line)

    verdicts = [
        proposition_ro_01(owner_text),
        proposition_ro_02(owner_text, args.flow_sample),
        proposition_ro_03(owner_text),
        proposition_ro_04(args.roster, roster_baseline),
        proposition_ro_05(owner_text, args.line_set),
        proposition_ro_06(args.line_set, projection),
        proposition_ro_07(owner_text, projection),
        proposition_ro_08(args.line_set, projection),
        proposition_ro_09(owner_text, state),
        proposition_ro_10(args.line_set),
        proposition_ro_11(args.line_set),
        proposition_ro_12(args, args.run_record),
        proposition_ro_13(owner_text),
    ]

    return _emit_verdicts(verdicts, args.format)


# ---------------------------------------------------------------- cli
def build_parser():
    parser = argparse.ArgumentParser(
        prog="status-digest.py",
        description=(
            "Current-state digest, reporting-obligation guard and status-line renderer"
            " (owner: shared/guidelines/reporting-obligations.md)."
        ),
    )
    parser.add_argument("--action", required=True, choices=("digest", "guard", "report"))
    parser.add_argument("--format", default="text", choices=("text", "json"))
    parser.add_argument(
        "--workspace",
        default=os.environ.get("SPECIFY_STATUS_WORKSPACE") or str(Path.cwd()),
        help="workspace whose registry entries are listed (default: the current directory)",
    )
    parser.add_argument(
        "--cap",
        type=int,
        default=int(os.environ.get(CAP_ENV, DEFAULT_CAP)),
        help="maximum entries rendered (declared default %d, overridable per invocation)"
        % DEFAULT_CAP,
    )
    parser.add_argument(
        "--stale-bound",
        type=int,
        default=DEFAULT_STALE_BOUND_SECONDS,
        help="age in seconds beyond which an entry is marked stale (declared default %d)"
        % DEFAULT_STALE_BOUND_SECONDS,
    )
    # guard inputs: each is an optional reading surface; an absent one yields not-evaluated, never pass.
    parser.add_argument("--line-set", default=None, help="captured status line set to judge")
    parser.add_argument("--flow-sample", default=None, help="seeded flow sample classified by RO-02")
    parser.add_argument("--roster", action="append", default=None, help="roster path in the population (repeatable)")
    parser.add_argument(
        "--roster-baseline",
        default=None,
        help="the recorded name-list that declares each roster path's population class",
    )
    parser.add_argument(
        "--carrier",
        default=None,
        help=(
            "the carrier that receives the line: 'console' or the declared stream artifact path (C-26)"
            " — the same value the run record holds and RO-12 reads"
        ),
    )
    parser.add_argument("--run-record", default=None, help="run record path (context for RO-12)")
    # report inputs
    parser.add_argument("--structure", default=None, help="structure slug for the rendered line")
    parser.add_argument("--run-stamp", default=None, help="run stamp for the rendered line")
    parser.add_argument("--position", default=None, help="position element")
    parser.add_argument("--delta", default=None, help="delta element")
    parser.add_argument("--remainder", default=None, help="remainder element")
    parser.add_argument("--blocker", default=None, help="blocker element (omit to write 'no blocker')")
    parser.add_argument(
        "--cadence",
        default=None,
        help="the cadence value in force when it is a per-run/per-structure override (C-24)",
    )
    parser.add_argument(
        "--delay-reason",
        default=None,
        help="stated delay when a tick was delivered at the next step boundary (C-25)",
    )
    parser.add_argument(
        "--trigger",
        default="tick",
        help="which rule produced the line: tick | boundary | transition:<sub-flow-id> | reporter-failure",
    )
    # guard inputs: the supervision report over the dispatches a supervising flow watches (C-32…C-35).
    parser.add_argument(
        "--supervision-report",
        action="store_true",
        help="judge the supervision report over the dispatched sub-flows named by --sub-flow",
    )
    parser.add_argument(
        "--sub-flow",
        action="append",
        default=None,
        metavar="LABEL=TRIPLET_DIR",
        help="one dispatched sub-flow: its label plus the directory holding its triplet (repeatable)",
    )
    parser.add_argument(
        "--expect-sub-flow",
        action="append",
        default=None,
        metavar="LABEL",
        help="a label the caller knows was dispatched; a label with no row is an omission (C-33)",
    )
    parser.add_argument(
        "--transition",
        default=None,
        choices=TRANSITION_CLASSES,
        help="a significant transition the flow observed while rendering this report (C-34)",
    )
    parser.add_argument(
        "--interval-elapsed",
        action="store_true",
        help="set when the cadence tick had already elapsed when the transition was observed",
    )
    parser.add_argument(
        "--profile",
        default=None,
        choices=(PROFILE_LONG_RUN, PROFILE_INTERACTIVE),
        help=(
            "the cadence profile in force, when the emitting flow records a switch rather than reading it"
            " from the state (C-30)"
        ),
    )
    parser.add_argument(
        "--profile-switch",
        default=None,
        help="the record of why the profile changed, so a switch is never silent (C-30)",
    )
    parser.add_argument(
        "--threshold-row",
        default=MANDATORY_THRESHOLD_ROW,
        help="the condition row the caller says is silent; the threshold is read from its table cell",
    )
    parser.add_argument(
        "--threshold-seconds",
        type=int,
        default=None,
        help="a per-run threshold override, recorded next to the row it overrides (C-24's override rule)",
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cap <= 0:
        print("--cap must be a positive integer", file=sys.stderr)
        return EXIT_INPUT_ERROR
    if args.action == "digest":
        return action_digest(args)
    if args.action == "report":
        return action_report(args)
    if args.supervision_report:
        return action_supervision(args)
    return action_guard(args)


if __name__ == "__main__":
    sys.exit(main())
