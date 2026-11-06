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
    ``omitted``, ``cap``, ``stale_bound_seconds``, ``generated_at``, ``vocabulary``.
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
    """
    state, _error = read_state(args.cap, args.stale_bound, Path(args.workspace).expanduser().resolve())
    profile = profile_in_force(state) if state else PROFILE_LONG_RUN
    fields = [
        "structure=%s" % args.structure,
        "run=%s" % args.run_stamp,
        "trigger=%s" % args.trigger,
        "profile=%s" % profile,
    ]
    if args.cadence:
        # An override is recorded NEXT TO the profile, so a reader can tell an override from the definition (C-24).
        fields.append("cadence=%s" % args.cadence)
    if args.delay_reason:
        fields.append("delay=%s" % args.delay_reason)
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


def proposition_ro_06(line_set_path):
    name = "RO-06"
    if not line_set_path:
        return _not_evaluated(name, "no captured supervision report supplied (--line-set)")
    text = _read_text(Path(line_set_path))
    if text is None:
        return _not_evaluated(name, "captured supervision report %s is unreadable" % line_set_path)
    rows = [ln for ln in text.splitlines() if "sub-flow=" in ln]
    if not rows:
        return _fail(name, "no per-sub-flow row found in the captured supervision report")
    return _pass(name, "%d sub-flow row(s) present" % len(rows))


def proposition_ro_07(owner_text):
    name = "RO-07"
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


def proposition_ro_08(line_set_path):
    name = "RO-08"
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

    verdicts = [
        proposition_ro_01(owner_text),
        proposition_ro_02(owner_text, args.flow_sample),
        proposition_ro_03(owner_text),
        proposition_ro_04(args.roster, roster_baseline),
        proposition_ro_05(owner_text, args.line_set),
        proposition_ro_06(args.line_set),
        proposition_ro_07(owner_text),
        proposition_ro_08(args.line_set),
        proposition_ro_09(owner_text, state),
        proposition_ro_10(args.line_set),
        proposition_ro_11(args.line_set),
        proposition_ro_12(args, args.run_record),
        proposition_ro_13(owner_text),
    ]

    if args.format == "json":
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
    return action_guard(args)


if __name__ == "__main__":
    sys.exit(main())
