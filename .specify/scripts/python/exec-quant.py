#!/usr/bin/env python3
"""exec-quant.py — Agent+LLM execution quant recording engine (Feature 059).

Recording Only: every completed execution of a covered unit (the same unit
semantics as run-determination) lands ONE quant record — agent program fields,
LLM detail fields, quality fields — into the engine-owned durable store
``.specify/memory/exec-quant/`` (records.jsonl + scores.jsonl, append-only).

Design adjudications live in the feature plan (D1–D12); behavior truth is this
file. Law of the record (data-model §1.1): every measurable field is either a
``{"value", "provenance"}`` object or the literal ``not_evaluated`` — zero
null, zero empty string, zero missing key. A quantity with no source is never
guessed (测量而非印象).

Non-blocking (FR-012): any failure path exits 1 with a message on stderr and
never raises into the caller's run.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

ACTIONS = ("collect", "list-records", "score")

KIND = "speckit.exec-quant"  # [[STR-001]]
SCHEMA_VERSION = 1
NOT_EVALUATED = "not_evaluated"  # [[STR-002]]
PROVENANCES = ("measured", "carried", "user-given")
UNIT_TYPES = ("command", "skill", "custom-unit")
RESOLUTIONS = ("explicit", "adopted", "synthesized")
AGENT_RESOLUTIONS = ("resolved", "ambiguous", "unresolved")

#: plan D2 single adjudication: adoption window for a same-unit determination
#: record when the caller passes no --run-id (bounded against stale binding).
RECENT_WINDOW_MINUTES = 90

#: data-model V5: single-record serialization cap.
RECORD_SIZE_CAP_BYTES = 64 * 1024

STORAGE_REL = Path(".specify") / "memory" / "exec-quant"
RECORDS_NAME = "records.jsonl"
SCORES_NAME = "scores.jsonl"

_UNIT_ID_RE = re.compile(
    r"^(?:/speckit\.[a-z0-9][a-z0-9._-]*"
    r"|skill:[a-z0-9][a-z0-9._-]*"
    r"|custom:[a-z0-9][a-z0-9._-]*/[a-z0-9][a-z0-9._-]*)$"
)

#: D8 known host-CLI process-name patterns (framework-supported agents).
HOST_CLI_PATTERNS = ("qodercli", "claude", "codex", "copilot", "opencode", "hermes")

#: D6 endpoint whitelist: only these variable names are read, values origin-only.
ENDPOINT_ENV_NAMES = (
    "ANTHROPIC_BASE_URL", "ANTHROPIC_URL", "OPENAI_BASE_URL", "OPENAI_URL",
    "ALIYUN_ANTHROPIC_COMPATIBLE_URL", "ALIYUN_OPENAI_COMPATIBLE_URL",
    "DASHSCOPE_API_URL", "CLAUDE_ALIBABA_BASE_URL", "CLAUDE_OFFICIAL_BASE_URL",
)

#: D9 value-level credential shapes masked before write (defense in depth on
#: top of the D6 whitelist collection; hits are replaced in place).
CREDENTIAL_PATTERNS = tuple(
    (name, re.compile(pattern))
    for name, pattern in (
        ("sk_style_key", r"(?i)\b(?:sk|pk)-[A-Za-z0-9_-]{16,}\b"),
        ("aws_access_key", r"\bAKIA[0-9A-Z]{16}\b"),
        ("bearer_token", r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"),
        ("slack_token", r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
        ("github_token", r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
        ("google_api_key", r"\bAIza[0-9A-Za-z_\-]{30,}\b"),
        ("url_userinfo", r"[A-Za-z][A-Za-z0-9+.\-]*://[^\s/:@]+:[^\s/@]+@"),
        ("kv_assignment",
         r"(?i)\b(?:api[_-]?key|secret|token|authorization|password)\b\s*[:=]\s*['\"]?[^\s'\"]{8,}"),
    )
)


class ExecQuantError(Exception):
    """Engine failure surfaced as exit 1 with a stderr message."""


class InputError(ExecQuantError):
    """Usage error surfaced as exit 2."""


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sibling_engine(filename: str):
    """Load a sibling engine from this file's own directory (two-hats-safe:
    self-location fires only on a literal component of the resolved path)."""
    path = Path(__file__).resolve().parent / filename
    if not path.is_file():
        raise ExecQuantError(f"sibling engine not found beside this one: {path}")
    import importlib.util
    name = "_eq_" + filename.replace("-", "_").replace(".py", "")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ExecQuantError(f"cannot load sibling engine: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def resolve_workspace_root(explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit).resolve()
    try:
        memory = sibling_engine("memory-utils.py")
    except ExecQuantError:
        return Path.cwd().resolve()
    return memory.resolve_workspace_root(None)


def validate_unit_id(unit_id: str) -> bool:
    return bool(unit_id) and bool(_UNIT_ID_RE.match(unit_id.strip()))


def unit_type_of(unit_id: str) -> str:
    uid = (unit_id or "").strip()
    if uid.startswith("/speckit."):
        return "command"
    if uid.startswith("skill:"):
        return "skill"
    if uid.startswith("custom:"):
        return "custom-unit"
    raise InputError(
        f"invalid --unit-id: {unit_id!r} — expected /speckit.<command>, "
        f"skill:<name> or custom:<owner>/<name>")


def storage_dir(workspace_root: Path) -> Path:
    return workspace_root / STORAGE_REL


def bootstrap_storage(workspace_root: Path) -> Tuple[Path, Path]:
    directory = storage_dir(workspace_root)
    try:
        directory.mkdir(parents=True, exist_ok=True)
        records = directory / RECORDS_NAME
        scores = directory / SCORES_NAME
        for path in (records, scores):
            if not path.exists():
                path.touch()
        return records, scores
    except OSError as exc:
        raise ExecQuantError(f"cannot bootstrap the exec-quant store: {exc}") from exc


# ---------------------------------------------------------------------------
# run identity (plan D2)
# ---------------------------------------------------------------------------

def _parse_iso(value: Any) -> Optional[datetime]:
    if not isinstance(value, str) or not value:
        return None
    text = value.strip()
    try:
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None


def load_determinations_for_unit(workspace_root: Path, unit_id: str) -> List[Dict[str, Any]]:
    """Read-only access to the adjacent engine's records (FR-015: no writes)."""
    try:
        rd = sibling_engine("run-determination.py")
        found = rd.load_determinations(workspace_root, unit_id)
    except Exception:
        return []
    records = []
    for item in found or []:
        record = item.get("record") if isinstance(item, dict) else None
        if isinstance(record, dict) and record.get("kind") == "speckit.run-determination":
            records.append(record)
    return records


def resolve_run_identity(workspace_root: Path, unit_id: str,
                         explicit_run_id: Optional[str]
                         ) -> Tuple[str, str, Optional[Dict[str, Any]]]:
    """Return (run_id, resolution, determination_record)."""
    determinations = load_determinations_for_unit(workspace_root, unit_id)
    if explicit_run_id:
        exact = next((r for r in determinations if r.get("run_id") == explicit_run_id), None)
        return explicit_run_id, "explicit", exact
    now = datetime.now(timezone.utc)
    window = timedelta(minutes=RECENT_WINDOW_MINUTES)
    recent = []
    for record in determinations:
        stamp = _parse_iso(record.get("determined_at"))
        if stamp is not None and timedelta(0) <= now - stamp <= window:
            recent.append((stamp, record.get("run_id") or "", record))
    if recent:
        recent.sort(key=lambda item: (item[0], item[1]))
        _, run_id, record = recent[-1]
        if run_id:
            return run_id, "adopted", record
    return "{}-{}".format(_slug(unit_id), now.strftime("%Y%m%dT%H%M%SZ")), "synthesized", None


def _slug(unit_id: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", unit_id.strip().lower()).strip("-")


# ---------------------------------------------------------------------------
# agent collection (D8)
# ---------------------------------------------------------------------------

def _proc_file(pid: int, name: str) -> Optional[str]:
    try:
        return (Path("/proc") / str(pid) / name).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _proc_argv(pid: int) -> List[str]:
    raw = _proc_file(pid, "cmdline")
    if raw is None:
        return []
    return [part for part in raw.split("\x00") if part]


def _proc_ppid(pid: int) -> Optional[int]:
    stat = _proc_file(pid, "stat")
    if not stat:
        return None
    tail = stat[stat.rfind(")") + 1:].split() if ")" in stat else []
    try:
        return int(tail[1])
    except (IndexError, ValueError):
        return None


def _proc_cwd(pid: int) -> Optional[str]:
    try:
        return os.readlink(f"/proc/{pid}/cwd")
    except OSError:
        return None


def _matches_host(name: str) -> bool:
    lowered = name.lower()
    return any(pattern in lowered for pattern in HOST_CLI_PATTERNS)


def _candidate_names(pid: int) -> List[str]:
    argv = _proc_argv(pid)
    names = []
    if argv:
        names.append(Path(argv[0]).name)
    comm = _proc_file(pid, "comm")
    if comm:
        names.append(comm.strip())
    return [n for n in names if n]


def probe_version(binary: str) -> Optional[str]:
    """<binary> --version with a bounded timeout; never guessed (D8)."""
    executable = binary
    if not os.path.isfile(executable):
        executable = shutil.which(binary) or ""
    if not executable:
        return None
    try:
        result = subprocess.run([executable, "--version"], capture_output=True,
                                text=True, timeout=10, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    for line in (result.stdout or "").splitlines() + (result.stderr or "").splitlines():
        line = line.strip()
        if line:
            return line[:200]
    return None


def collect_agent() -> Tuple[Dict[str, Any], Optional[int], Optional[str]]:
    """Walk the parent chain; attribute the host CLI without guessing."""
    group: Dict[str, Any] = {key: NOT_EVALUATED
                             for key in ("name", "version", "binary", "argv", "cwd")}
    group["resolution"] = "unresolved"
    if not os.path.isdir("/proc"):
        return group, None, None
    matches: List[Tuple[int, str, List[str]]] = []
    seen = set()
    pid = os.getppid()
    while pid and pid > 1 and pid not in seen:
        seen.add(pid)
        names = _candidate_names(pid)
        hit = next((n for n in names if _matches_host(n)), None)
        if hit:
            matches.append((pid, hit, _proc_argv(pid)))
        pid = _proc_ppid(pid) or 0
    if not matches:
        return group, None, None
    distinct = {name for _, name, _ in matches}
    if len(distinct) > 1:
        group["resolution"] = "ambiguous"
        return group, None, None
    pid, name, argv = matches[0]
    group["resolution"] = "resolved"
    group["name"] = {"value": name, "provenance": "measured"}
    if argv:
        group["binary"] = {"value": argv[0], "provenance": "measured"}
        rest = argv[1:]
        if rest:
            group["argv"] = {"value": rest, "provenance": "measured"}
        version = probe_version(argv[0])
        if version:
            group["version"] = {"value": version, "provenance": "measured"}
    cwd = _proc_cwd(pid)
    if cwd:
        group["cwd"] = {"value": cwd, "provenance": "measured"}
    return group, pid, name


# ---------------------------------------------------------------------------
# LLM collection (D6 + D7)
# ---------------------------------------------------------------------------

def _read_environ(pid: Optional[int]) -> Dict[str, str]:
    if pid is not None:
        raw = _proc_file(pid, "environ")
        if raw is not None:
            mapping = {}
            for chunk in raw.split("\x00"):
                if "=" in chunk:
                    key, _, value = chunk.partition("=")
                    mapping[key] = value
            return mapping
    return dict(os.environ)


def _url_origin(value: str) -> Optional[str]:
    """scheme://host[:port] only — path, query and credentials stripped (D6)."""
    try:
        parsed = urlparse(value.strip())
    except ValueError:
        return None
    if not parsed.scheme or not parsed.hostname:
        return None
    host = parsed.hostname
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
    netloc = host if parsed.port is None else f"{host}:{parsed.port}"
    return f"{parsed.scheme}://{netloc}"


def collect_endpoint_candidates(pid: Optional[int]) -> Dict[str, Any]:
    env = _read_environ(pid)
    mapping = {}
    for name in ENDPOINT_ENV_NAMES:
        value = env.get(name, "").strip()
        if not value:
            continue
        origin = _url_origin(value)
        if origin:
            mapping[name] = origin
    return mapping if mapping else NOT_EVALUATED


def collect_connection_evidence(pid: Optional[int]) -> Dict[str, Any]:
    """Established remote ip:port of connections owned by the host pid (no
    DNS, no effectiveness verdict — evidence only, D6)."""
    if pid is None or shutil.which("ss") is None:
        return NOT_EVALUATED
    try:
        result = subprocess.run(["ss", "-tnp"], capture_output=True, text=True,
                                timeout=10, check=False)
    except (OSError, subprocess.SubprocessError):
        return NOT_EVALUATED
    peers: List[str] = []
    for line in (result.stdout or "").splitlines():
        parts = line.split()
        if len(parts) < 5 or parts[0] != "ESTAB":
            continue
        owner = " ".join(parts[5:])
        if re.search(rf"\bpid={pid}\b", owner):
            peer = parts[4]
            if peer and peer not in peers:
                peers.append(peer)
    return {"value": peers, "provenance": "measured"} if peers else NOT_EVALUATED


def qoder_settings_path() -> Path:
    return Path.home() / ".qoder" / "settings.json"


def collect_llm(agent: Dict[str, Any], pid: Optional[int]) -> Dict[str, Any]:
    group: Dict[str, Any] = {
        "model": NOT_EVALUATED, "context_window": NOT_EVALUATED,
        "reasoning_effort": NOT_EVALUATED, "config_source": NOT_EVALUATED,
        "endpoint_candidates": NOT_EVALUATED, "connection_evidence": NOT_EVALUATED,
    }
    if agent.get("resolution") != "resolved":
        return group
    host_name = ""
    name = agent.get("name")
    if isinstance(name, dict):
        host_name = str(name.get("value") or "")
    group["endpoint_candidates"] = collect_endpoint_candidates(pid)
    group["connection_evidence"] = collect_connection_evidence(pid)
    if "qodercli" not in host_name.lower():
        return group
    try:
        data = json.loads(qoder_settings_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return group
    group["config_source"] = {"value": str(qoder_settings_path()), "provenance": "measured"}
    model = data.get("model") if isinstance(data, dict) else None
    model_name = model.get("name") if isinstance(model, dict) else None
    preferences = model.get("preferences") if isinstance(model, dict) else None
    own = preferences.get(model_name) if isinstance(preferences, dict) else None
    if isinstance(model_name, str) and model_name:
        group["model"] = {"value": model_name, "provenance": "measured"}
    if isinstance(own, dict):
        window = own.get("contextWindow")
        if isinstance(window, int) and not isinstance(window, bool) and window > 0:
            group["context_window"] = {"value": window, "provenance": "measured"}
        reasoning = own.get("reasoning")
        effort = reasoning.get("effort") if isinstance(reasoning, dict) else None
        if isinstance(effort, str) and effort:
            group["reasoning_effort"] = {"value": effort, "provenance": "measured"}
    return group


# ---------------------------------------------------------------------------
# quality carried fields (A6 + D5)
# ---------------------------------------------------------------------------

def collect_quality(record: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    group: Dict[str, Any] = {
        "elapsed_ms": NOT_EVALUATED, "tokens": NOT_EVALUATED,
        "errors": NOT_EVALUATED, "satisfaction": NOT_EVALUATED,
    }
    if not record:
        return group
    axes = record.get("axes") if isinstance(record.get("axes"), dict) else {}

    elapsed = ((axes.get("elapsed") or {}).get("measurement") or {}).get("ms")
    if isinstance(elapsed, int) and not isinstance(elapsed, bool) and elapsed >= 0:
        group["elapsed_ms"] = {"value": elapsed, "provenance": "carried"}

    total = ((axes.get("token_consumption") or {}).get("measurement") or {}).get("total_tokens")
    if isinstance(total, int) and not isinstance(total, bool) and total >= 0:
        group["tokens"] = {"value": total, "provenance": "carried"}

    verdict = (axes.get("satisfaction") or {}).get("verdict")
    if verdict and verdict != NOT_EVALUATED:
        group["satisfaction"] = {"value": verdict, "provenance": "carried"}

    errors: List[Dict[str, Any]] = []
    diff = ((axes.get("artifact_correctness") or {}).get("failed_set_diff")) or {}
    if diff.get("status") in ("empty", "non_empty"):
        count = diff.get("added_count")
        if not isinstance(count, int) or isinstance(count, bool):
            count = len(diff.get("added") or [])
        errors.append({"source": "run-determination.failed_set_diff", "count": count})
    red = (axes.get("satisfaction") or {}).get("unresolved_red") or {}
    if red.get("present") == "true":
        errors.append({"source": "run-determination.unresolved_red", "count": 1})
    if errors:
        group["errors"] = errors
    return group


def collect_qualification(record: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    value = record.get("qualification") if record else None
    if isinstance(value, str) and value:
        return {"value": value, "provenance": "carried"}
    return NOT_EVALUATED


# ---------------------------------------------------------------------------
# record assembly + defenses (D9)
# ---------------------------------------------------------------------------

def build_record(workspace_root: Path, unit_id: str, unit_type: str,
                 explicit_run_id: Optional[str]) -> Dict[str, Any]:
    run_id, resolution, determination = resolve_run_identity(
        workspace_root, unit_id, explicit_run_id)
    return assemble_record(unit_id, unit_type, run_id, resolution, determination)


def assemble_record(unit_id: str, unit_type: str, run_id: str, resolution: str,
                    determination: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    agent, host_pid, _host_name = collect_agent()
    synthesized = resolution == "synthesized"
    record = {
        "kind": KIND,
        "schema_version": SCHEMA_VERSION,
        "unit_id": unit_id,
        "unit_type": unit_type,
        "run_id": run_id,
        "run_id_resolution": resolution,
        "collected_at": now_iso(),
        "agent": agent,
        "llm": collect_llm(agent, host_pid),
        "quality": collect_quality(None if synthesized else determination),
        "qualification": (NOT_EVALUATED if synthesized
                          else collect_qualification(determination)),
        "truncated": [],
    }
    return record


def mask_credentials(node: Any) -> Any:
    if isinstance(node, str):
        for name, pattern in CREDENTIAL_PATTERNS:
            if pattern.search(node):
                node = pattern.sub(f"[masked-credential:{name}]", node)
        return node
    if isinstance(node, dict):
        return {key: mask_credentials(value) for key, value in node.items()}
    if isinstance(node, list):
        return [mask_credentials(item) for item in node]
    return node


def _longest_string(container: Any, path: str
                    ) -> Optional[Tuple[Any, Any, str, str, int]]:
    best = None
    if isinstance(container, dict):
        items = container.items()
    elif isinstance(container, list):
        items = enumerate(container)
    else:
        return best
    for key, value in items:
        child_path = f"{path}.{key}" if isinstance(container, dict) else f"{path}[{key}]"
        if isinstance(value, str):
            if best is None or len(value) > best[4]:
                best = (container, key, child_path, value, len(value))
        else:
            nested = _longest_string(value, child_path)
            if nested and (best is None or nested[4] > best[4]):
                best = nested
    return best


def enforce_size_cap(record: Dict[str, Any]) -> List[str]:
    """Halve the largest string field until the serialization fits (V5)."""
    truncated: List[str] = []
    while True:
        blob = json.dumps(record, ensure_ascii=False).encode("utf-8")
        if len(blob) <= RECORD_SIZE_CAP_BYTES:
            return truncated
        target = _longest_string(record, "$")
        if target is None or target[4] <= 8:
            return truncated
        container, key, path, value, _ = target
        container[key] = value[:len(value) // 2]
        if path not in truncated:
            truncated.append(path)


def existing_record(records_path: Path, unit_id: str, run_id: str) -> bool:
    try:
        with records_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except ValueError:
                    continue
                if (record.get("unit_id") == unit_id and record.get("run_id") == run_id):
                    return True
    except OSError:
        return False
    return False


# ---------------------------------------------------------------------------
# actions
# ---------------------------------------------------------------------------

def action_collect(args: argparse.Namespace) -> int:
    workspace_root = resolve_workspace_root(args.workspace_root)
    unit_id = (args.unit_id or "").strip()
    if not validate_unit_id(unit_id):
        raise InputError(f"invalid --unit-id: {args.unit_id!r}")
    resolved_type = unit_type_of(unit_id)
    if args.unit_type and args.unit_type != resolved_type:
        raise InputError(
            f"--unit-type {args.unit_type!r} contradicts the unit-id form "
            f"{unit_id!r} (expected {resolved_type!r})")
    records_path, _scores_path = bootstrap_storage(workspace_root)
    run_id, resolution, determination = resolve_run_identity(
        workspace_root, unit_id, args.run_id)
    if existing_record(records_path, unit_id, run_id):
        print(f"exec-quant: duplicate record for ({unit_id}, {run_id}); "
              f"no second row written -> {records_path}")
        return 0
    record = assemble_record(unit_id, resolved_type, run_id, resolution, determination)
    record = mask_credentials(record)
    truncated = enforce_size_cap(record)
    record["truncated"] = truncated
    line = json.dumps(record, ensure_ascii=False)
    try:
        with records_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except OSError as exc:
        raise ExecQuantError(f"cannot append to {records_path}: {exc}") from exc
    print(f"exec-quant: recorded {unit_id} run={record['run_id']} "
          f"resolution={resolution} -> {records_path}")
    return 0


def _parse_since(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    text = value.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            stamp = datetime.strptime(text, fmt)
            return stamp.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        raise InputError(f"invalid --since: {value!r} (expected ISO date or timestamp)")


def _field_text(node: Any) -> str:
    if node == NOT_EVALUATED:
        return "-"
    if isinstance(node, dict):
        return str(node.get("value"))
    return str(node)


def load_store(workspace_root: Path):
    records_file = storage_dir(workspace_root) / RECORDS_NAME
    scores_file = storage_dir(workspace_root) / SCORES_NAME
    records = read_jsonl_safe(records_file)
    scores = read_jsonl_safe(scores_file)
    return records, scores


def read_jsonl_safe(path: Path) -> List[Dict[str, Any]]:
    if not path.is_file():
        return []
    entries = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                if isinstance(entry, dict):
                    entries.append(entry)
    except OSError:
        return []
    return entries


def action_list_records(args: argparse.Namespace) -> int:
    workspace_root = resolve_workspace_root(args.workspace_root)
    since = _parse_since(args.since)
    if args.format not in ("text", "json"):
        raise InputError(f"invalid --format: {args.format!r}")
    records, scores = load_store(workspace_root)
    joined: List[Dict[str, Any]] = []
    for record in records:
        if args.unit_id and record.get("unit_id") != args.unit_id:
            continue
        if args.unit_type and record.get("unit_type") != args.unit_type:
            continue
        if args.run_id and record.get("run_id") != args.run_id:
            continue
        collected = _parse_iso(record.get("collected_at"))
        if since and collected and collected < since:
            continue
        matches = [s for s in scores
                   if s.get("unit_id") == record.get("unit_id")
                   and s.get("run_id") == record.get("run_id")]
        matches.sort(key=lambda s: (str(s.get("scored_at") or ""),))
        entry = dict(record)
        entry["scores"] = matches
        joined.append(entry)
    if args.format == "json":
        print(json.dumps(joined, ensure_ascii=False, indent=2))
        return 0
    for entry in joined:
        latest = entry["scores"][-1] if entry["scores"] else None
        quality = entry.get("quality") or {}
        agent = entry.get("agent") or {}
        llm = entry.get("llm") or {}
        endpoints = llm.get("endpoint_candidates")
        endpoint_count = len(endpoints) if isinstance(endpoints, dict) else 0
        print(f"{entry.get('unit_id')} type={entry.get('unit_type')} "
              f"run={entry.get('run_id')} resolution={entry.get('run_id_resolution')} "
              f"collected={entry.get('collected_at')}")
        print(f"  agent: resolution={agent.get('resolution')} "
              f"name={_field_text(agent.get('name'))} "
              f"version={_field_text(agent.get('version'))}")
        print(f"  llm: model={_field_text(llm.get('model'))} "
              f"context_window={_field_text(llm.get('context_window'))} "
              f"effort={_field_text(llm.get('reasoning_effort'))} "
              f"endpoints={endpoint_count}")
        print(f"  quality: elapsed_ms={_field_text(quality.get('elapsed_ms'))} "
              f"tokens={_field_text(quality.get('tokens'))} "
              f"satisfaction={_field_text(quality.get('satisfaction'))} "
              f"qualification={_field_text(entry.get('qualification'))}")
        if latest:
            print(f"  score: {latest.get('score')} "
                  f"provenance={latest.get('provenance')} "
                  f"at={latest.get('scored_at')}"
                  + (f" note={latest.get('note')}" if latest.get("note") else ""))
    print(f"exec-quant: {len(joined)} record(s) listed", file=sys.stderr)
    return 0


def action_score(args: argparse.Namespace) -> int:
    workspace_root = resolve_workspace_root(args.workspace_root)
    unit_id = (args.unit_id or "").strip()
    if not validate_unit_id(unit_id):
        raise InputError(f"invalid --unit-id: {args.unit_id!r}")
    if not args.run_id:
        raise InputError("score requires --run-id (the record being scored)")
    if args.score is None:
        raise InputError("score requires --score (1-5)")
    if not (1 <= args.score <= 5):
        raise InputError(f"--score must be within 1-5, got {args.score}")
    records_file = storage_dir(workspace_root) / RECORDS_NAME
    target = next((r for r in read_jsonl_safe(records_file)
                   if r.get("unit_id") == unit_id and r.get("run_id") == args.run_id), None)
    if target is None:
        raise InputError(
            f"no record for ({unit_id}, {args.run_id}) — score appends to an "
            f"existing record, run collect first")
    scores_file = storage_dir(workspace_root) / SCORES_NAME
    entry = {
        "kind": KIND,
        "entry_type": "score",
        "unit_id": unit_id,
        "unit_type": target.get("unit_type"),
        "run_id": args.run_id,
        "score": args.score,
        "scored_at": now_iso(),
        "provenance": "user-given",
    }
    if args.note:
        entry["note"] = args.note
    try:
        scores_file.parent.mkdir(parents=True, exist_ok=True)
        with scores_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as exc:
        raise ExecQuantError(f"cannot append to {scores_file}: {exc}") from exc
    print(f"exec-quant: scored {unit_id} run={args.run_id} "
          f"score={args.score} provenance=user-given -> {scores_file}")
    return 0


USAGE_LINE = ("usage: exec-quant.py --action {" + ",".join(ACTIONS) + "} "
              "[--unit-id ID] [--unit-type TYPE] [--run-id ID] [--score 1-5] "
              "[--note TEXT] [--since DATE] [--format text|json] "
              "[--workspace-root PATH]")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="exec-quant.py", allow_abbrev=False)
    parser.add_argument("--workspace-root", default=None)
    parser.add_argument("--action", required=True,
                        choices=["collect", "list-records", "score"])
    parser.add_argument("--unit-id", default=None)
    parser.add_argument("--unit-type", default=None, choices=list(UNIT_TYPES))
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--score", type=int, default=None)
    parser.add_argument("--note", default=None)
    parser.add_argument("--since", default=None)
    parser.add_argument("--format", default="text", choices=["text", "json"])
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.action == "collect":
            return action_collect(args)
        if args.action == "list-records":
            return action_list_records(args)
        return action_score(args)
    except InputError as exc:
        print(USAGE_LINE, file=sys.stderr)
        print(f"exec-quant: usage error: {exc}", file=sys.stderr)
        return 2
    except ExecQuantError as exc:
        print(f"exec-quant: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # non-blocking guarantee: never raise into the caller
        print(f"exec-quant: unexpected failure: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
