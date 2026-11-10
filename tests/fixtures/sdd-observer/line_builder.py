"""Build a stub SDD line under a caller-provided ``tmp_path`` (Feature 096, wp01 T007).

The builder writes only inside the given root: a spec directory, a state spine carrying the U0
block and one observer record section, the runner-quartet envelopes per stage, per-stage sentinel
logs, checkpoint files, dispatch meta envelopes and a small git history. The declared stage
sequence and the completion-sentinel template are read from the declaration layer
(`shared/declarations/facts/driver-stage-sequence.yaml#/statement`,
`shared/declarations/facts/driver-completion-sentinels.yaml#/statement`) through the one reader —
this module restates neither (FR-013).

Consumers: ``tests/contract/test_journal_engine.py`` (wp01) and the later package builders that
compose this line (`dual_line_builder.py`, `failure_builder.py`).
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
READER_PATH = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"
SOURCE_FACTS = REPO_ROOT / "shared" / "declarations" / "facts"

#: The fact files every consumer of this fixture reads; copied byte-identically into the client-style
#: project tree so the engine reads the real owner text through the declaration reader.
REQUIRED_FACTS = ("journal-format", "driver-stage-sequence", "driver-completion-sentinels")

LINE_ID = "line-demo"
RUN_ID = "run-demo"
SPEC_KEY = "096-sdd-observer-agent"

ISO = "%Y-%m-%dT%H:%M:%SZ"


def _load_reader():
    spec = importlib.util.spec_from_file_location("sdd_observer_declaration_reader", READER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def utc(epoch: int) -> str:
    return time.strftime(ISO, time.gmtime(int(epoch)))


def declared_stages(repo_root: Path = REPO_ROOT):
    """The declared stage sequence, read from the fact owner — never restated here."""
    fact = _load_reader().load_fact(str(repo_root), "driver-stage-sequence")
    return [str(stage) for stage in fact["body"]["statement"]]


def sentinel_for(stage: str, repo_root: Path = REPO_ROOT) -> str:
    """The stage's completion sentinel, rendered from the fact owner's template and transform."""
    statement = _load_reader().load_fact(str(repo_root), "driver-completion-sentinels")["body"]["statement"]
    value = stage.upper() if str(statement.get("transform")) == "uppercase" else stage
    return str(statement["pattern"]).replace("{stage}", value)


def write_quartet(state_dir: Path, line_id: str, stage: str, epoch: int, exit_code: int = 0,
                  sentinel_present: bool = True, anomaly: str = "", extra_pid_lines=(),
                  repo_root: Path = REPO_ROOT) -> None:
    """One stage's runner quartet: pid / status / log / heartbeat (R-02 shapes)."""
    state_dir.mkdir(parents=True, exist_ok=True)
    sentinel = sentinel_for(stage, repo_root)
    pid_lines = [
        "pid=%d start=token-%s-%d at=%d line=%s stage=%s event=pid" % (
            4000 + epoch % 1000, stage, epoch, epoch, line_id, stage)
    ]
    for offset, token in enumerate(extra_pid_lines, 1):
        pid_lines.append(
            "pid=%d start=%s at=%d line=%s stage=%s event=pid" % (
                5000 + offset, token, epoch + offset, line_id, stage))
    (state_dir / ("pid-%s-%s" % (line_id, stage))).write_text(
        "\n".join(pid_lines) + "\n", encoding="utf-8")
    (state_dir / ("heartbeat-%s-%s.log" % (line_id, stage))).write_text(
        "at=%d line=%s stage=%s event=heartbeat\n" % (epoch, line_id, stage), encoding="utf-8")
    log_lines = ["stage %s started" % stage, "stage %s working" % stage]
    if anomaly:
        log_lines.append("ANOMALY: %s" % anomaly)
    if sentinel_present:
        log_lines.append(sentinel)
    (state_dir / ("log-%s-%s.log" % (line_id, stage))).write_text(
        "\n".join(log_lines) + "\n", encoding="utf-8")
    (state_dir / ("status-%s-%s" % (line_id, stage))).write_text(
        "exit=%d at=%d sentinel=%d line=%s stage=%s event=status progress=stream detached=yes\n"
        % (exit_code, epoch + 1, 1 if sentinel_present else 0, line_id, stage), encoding="utf-8")


def write_meta(state_dir: Path, line_id: str, stage: str, epoch: int) -> Path:
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / ("prompt-%s-%s.md.meta.json" % (line_id, stage))
    path.write_text(json.dumps({"line": line_id, "stage": stage, "at": int(epoch)}), encoding="utf-8")
    return path


def append_observer_record(spine: Path, line_id: str, run_id: str, spec_key: str, execution_label: str,
                           started_at: str, state: str = "started", reason: str = "-") -> None:
    """Append one append-only observer record section (E-9 shape) to the state spine."""
    section = [
        "",
        "## Observer Record — %s" % started_at,
        "- state: %s" % state,
        "- line_id: %s" % line_id,
        "- run_id: %s" % run_id,
        "- spec: %s" % spec_key,
        "- instance: sdd-observer-%s" % line_id,
        "- execution_label: %s" % execution_label,
        "- started_at: %s" % started_at,
        "- reason: %s" % reason,
    ]
    with spine.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(section) + "\n")


def _git(root: Path, *args, env=None) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "-c", "user.name=Observer Fixture",
         "-c", "user.email=observer@example.invalid", "-c", "commit.gpgsign=false", *args],
        capture_output=True, text=True, env=env, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), result.stderr.strip()))
    return result.stdout


def _commit(root: Path, epoch: int, message: str) -> None:
    import os
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(int(epoch)))
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = stamp
    env["GIT_COMMITTER_DATE"] = stamp
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", message, env=env)


def build_line(root: Path, line_id: str = LINE_ID, run_id: str = RUN_ID, spec_key: str = SPEC_KEY,
               start_epoch=None, stages=None, execution_label=None) -> dict:
    """Build the whole stub line under ``root`` and return its paths and identity."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    stages = list(stages) if stages is not None else declared_stages()
    start_epoch = int(start_epoch if start_epoch is not None else time.time() - 3600)
    label = execution_label or "%s--%s--observer" % (line_id, run_id)

    spec_dir = root / ".specify" / "specs" / spec_key
    state_dir = root / ".specify" / "state"
    facts_dir = root / ".specify" / "shared" / "declarations" / "facts"
    checkpoints = spec_dir / "checkpoints"
    checkpoints.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)
    facts_dir.mkdir(parents=True, exist_ok=True)
    for slug in REQUIRED_FACTS:
        source = SOURCE_FACTS / (slug + ".yaml")
        (facts_dir / source.name).write_bytes(source.read_bytes())

    artifact = spec_dir / "plan.md"
    artifact.write_text("# Fixture plan — %s\n" % spec_key, encoding="utf-8")
    (spec_dir / "requirements.md").write_text("# Fixture requirements — %s\n" % spec_key, encoding="utf-8")

    for index, stage in enumerate(stages):
        write_quartet(state_dir, line_id, stage, start_epoch + 10 * index)
        (checkpoints / ("%02d-%s.md" % (index + 1, stage))).write_text(
            "# Checkpoint — %s\n\n- fixture reading\n" % stage, encoding="utf-8")
        write_meta(state_dir, line_id, stage, start_epoch + 10 * index)

    spine = state_dir / ("%s.md" % line_id)
    spine.write_text(
        "# Line State — %s (fixture)\n\n"
        "<!-- loop-state:begin -->\n"
        "spine_state: running\n"
        "line_id: %s\n"
        "run_id: %s\n"
        "stage: %s\n"
        "attempts: 0\n"
        "<!-- loop-state:end -->\n\n"
        "- line_id: `%s`\n"
        "- run_id: `%s`\n\n"
        "## U0 入口声明\n\n"
        "- 目标项目：fixture project\n"
        "- 特性切片：%s\n"
        % (line_id, line_id, run_id, stages[0], line_id, run_id, spec_key),
        encoding="utf-8",
    )
    append_observer_record(spine, line_id, run_id, spec_key, label, utc(start_epoch))

    triplet_dir = root / ".specify" / "agents" / "execution" / "logs"
    triplet_dir.mkdir(parents=True, exist_ok=True)
    (triplet_dir / ("%s.live.log" % label)).write_text("observer start\n", encoding="utf-8")
    (triplet_dir / ("%s.jsonl" % label)).write_text('{"event":"start"}\n', encoding="utf-8")
    (triplet_dir / ("%s.status" % label)).write_text("state=running\n", encoding="utf-8")

    _git(root, "init", "-q")
    _commit(root, start_epoch + 5, "fixture: landing the spec")
    (spec_dir / "artifacts").mkdir(exist_ok=True)
    (spec_dir / "artifacts" / "stage-note.md").write_text("# Fixture artifact\n", encoding="utf-8")
    _commit(root, start_epoch + 15, "fixture: stage artifact")

    return {
        "root": root,
        "line_id": line_id,
        "run_id": run_id,
        "spec_key": spec_key,
        "spec_dir": spec_dir,
        "spine": spine,
        "state_dir": state_dir,
        "journal": spec_dir / "journal.md",
        "execution_label": label,
        "triplet_dir": triplet_dir,
        "stages": stages,
        "start_epoch": start_epoch,
    }
