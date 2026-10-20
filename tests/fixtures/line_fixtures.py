"""Shared fixtures for Feature 064 (line registry / envelope / lifecycle).

All builders use temp directories; nothing touches the real registry or project.
The engine and watcher are resolved through ``SDD_ENGINE`` / ``SDD_WATCHER`` so
mutation drills can point tests at copied artifacts.
"""
from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"

SENTINEL_STAGES = ("PLAN-DONE", "ANALYZE-DONE", "IMPLEMENT-DONE")


def engine_path() -> Path:
    return Path(os.environ.get("SDD_ENGINE", SKILL_DIR / "scripts" / "line-registry.py"))


def watcher_path() -> Path:
    return Path(
        os.environ.get("SDD_WATCHER", SKILL_DIR / "scripts" / "watch-target.sh")
    )


def stamp(offset: int = 0) -> str:
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time() + offset))


def make_line_id(slug: str = "demo", suffix: str | None = None, offset: int = 0) -> str:
    if suffix is None:
        suffix = os.urandom(2).hex()
    return f"{slug}-{stamp(offset)}-{suffix}"


def make_run_id(suffix: str | None = None, offset: int = 0) -> str:
    if suffix is None:
        suffix = os.urandom(2).hex()
    return f"r{stamp(offset)}-{suffix}"


def base_env(reg: Path | None = None, extra: dict | None = None) -> dict:
    env = os.environ.copy()
    if reg is not None:
        env["SPECIFY_LINE_REGISTRY_DIR"] = str(reg)
        env.setdefault("SPECIFY_LINE_RUNTIME_DIR", str(reg / "runtime"))
        (reg / "runtime").mkdir(parents=True, exist_ok=True)
    if extra:
        env.update({k: str(v) for k, v in extra.items()})
    return env


def run_engine(
    action: str,
    *args,
    reg: Path | None = None,
    env: dict | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(engine_path()), "--action", action, *args]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, env=env or base_env(reg)
    )
    if check and proc.returncode != 0:
        raise AssertionError(
            f"engine {action} failed rc={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
        )
    return proc


def engine_json(action: str, *args, reg: Path | None = None, env: dict | None = None):
    proc = run_engine(action, *args, reg=reg, env=env, check=True)
    return json.loads(proc.stdout)


def make_project(tmp_path: Path, name: str = "proj") -> Path:
    proj = tmp_path / name
    (proj / ".specify" / "memory").mkdir(parents=True, exist_ok=True)
    return proj


def make_git_repo(tmp_path: Path, name: str = "repo") -> Path:
    repo = tmp_path / name
    repo.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.com"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
    (repo / "README.md").write_text("base\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "base"], check=True)
    return repo


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    )


def write_status(
    path: Path,
    line: str,
    run: str,
    stage: str,
    rc: int = 0,
    sentinel: int = 0,
    envelope: bool = True,
    at: int | None = None,
) -> Path:
    tail = f" line={line} run={run} stage={stage} event=status" if envelope else ""
    path.write_text(f"exit={rc} at={at or int(time.time())} sentinel={sentinel}{tail}\n", encoding="utf-8")
    return path


def process_token(pid: int) -> str:
    """Platform start token: Linux start ticks, otherwise `ps -p <pid> -o lstart=`."""
    stat = Path(f"/proc/{pid}/stat")
    if stat.exists():
        try:
            return stat.read_text(encoding="utf-8").split()[21]
        except (OSError, IndexError):
            pass
    proc = subprocess.run(
        ["ps", "-p", str(pid), "-o", "lstart="], capture_output=True, text=True
    )
    return " ".join(proc.stdout.split())


def write_pid(
    path: Path,
    pid: int,
    start: str = "1",
    line: str = "",
    run: str = "",
    stage: str = "",
    envelope: bool = True,
) -> Path:
    tail = ""
    if envelope and line:
        tail = f" line={line} run={run} stage={stage} event=pid"
    start_field = f" start={start}" if start != "" else ""
    path.write_text(f"pid={pid}{start_field} at={int(time.time())}{tail}\n", encoding="utf-8")
    return path


def write_heartbeat(
    path: Path, line: str = "", run: str = "", stage: str = "", envelope: bool = True
) -> Path:
    if envelope and line:
        path.write_text(
            f"at={int(time.time())} line={line} run={run} stage={stage} event=heartbeat\n",
            encoding="utf-8",
        )
    else:
        path.write_text(f"{int(time.time())}\n", encoding="utf-8")
    os.utime(path, None)
    return path


def write_log(path: Path, *lines: str) -> Path:
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return path


def append_meta(
    path: Path,
    line: str,
    run: str,
    stage: str,
    event: str,
    sentinel_seen: int | None = None,
    exit_code: int | None = None,
) -> Path:
    record = {
        "line_id": line,
        "run_id": run,
        "stage": stage,
        "event": event,
        "at": int(time.time()),
    }
    if sentinel_seen is not None:
        record["sentinel_seen"] = sentinel_seen
    if exit_code is not None:
        record["exit"] = exit_code
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")
    return path


def four_piece(
    root: Path,
    line: str,
    run: str,
    stage: str = "plan",
    pid: int | None = None,
    sentinel: bool = False,
    rc: int = 0,
    envelope: bool = True,
) -> dict:
    """Write pid/status/log/heartbeat + log meta and return their paths."""
    root.mkdir(parents=True, exist_ok=True)
    paths = {
        "pid": root / f"pid-{line}-{stage}",
        "status": root / f"status-{line}-{stage}",
        "log": root / f"log-{line}-{stage}.log",
        "heartbeat": root / f"heartbeat-{line}-{stage}.log",
        "meta": root / f"log-{line}-{stage}.log.meta.jsonl",
        "prompt_meta": root / f"prompt-{line}-{stage}.md.meta.json",
    }
    pid_value = pid if pid is not None else os.getpid()
    start = process_token(pid_value) if pid_alive(pid_value) else "1"
    write_pid(paths["pid"], pid_value, start=start, line=line, run=run, stage=stage, envelope=envelope)
    write_log(paths["log"], "working", f"{stage.upper()}-DONE" if sentinel else "working")
    write_heartbeat(paths["heartbeat"], line=line, run=run, stage=stage, envelope=envelope)
    if sentinel:
        write_status(paths["status"], line, run, stage, rc=rc, sentinel=1, envelope=envelope)
    append_meta(paths["meta"], line, run, stage, "log-start")
    append_meta(
        paths["meta"], line, run, stage, "log-terminal",
        sentinel_seen=1 if sentinel else 0, exit_code=rc,
    )
    paths["prompt_meta"].write_text(
        json.dumps({"line_id": line, "run_id": run, "stage": stage, "event": "prompt", "at": int(time.time())}),
        encoding="utf-8",
    )
    return paths


def watcher_args(paths: dict, line: str, run: str, sentinel: str, *extra: str) -> list[str]:
    match = __import__("re").search(r"log-" + __import__("re").escape(line) + r"-(.+)\.log$", paths["log"].name)
    stage = match.group(1) if match else ""
    return [
        "bash", str(watcher_path()), "--once",
        "--line-id", line, "--run-id", run, "--stage", stage,
        "--label", line,
        "--pid-file", str(paths["pid"]),
        "--status-file", str(paths["status"]),
        "--log", str(paths["log"]),
        "--sentinel", sentinel,
        "--heartbeat", str(paths["heartbeat"]),
        "--meta", str(paths["meta"]),
        *extra,
    ]


def run_watcher(paths: dict, line: str, run: str, sentinel: str, *extra: str, env=None):
    return subprocess.run(
        watcher_args(paths, line, run, sentinel, *extra),
        capture_output=True, text=True, env=env or os.environ.copy(),
    )


def install_process_stubs(tmp_path: Path, names=("ps", "pgrep", "pidof")) -> dict:
    """PATH-first stubs that log every invocation; used to prove zero scans."""
    bin_dir = tmp_path / "stub-bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    log = tmp_path / "stub-invocations.log"
    log.write_text("", encoding="utf-8")
    for name in names:
        stub = bin_dir / name
        stub.write_text(
            "#!/bin/sh\n"
            f'printf "%s %s\\n" "{name}" "$*" >> "{log}"\n'
            "exit 1\n",
            encoding="utf-8",
        )
        stub.chmod(0o755)
    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"
    env["STUB_LOG"] = str(log)
    return {"env": env, "log": log, "bin_dir": bin_dir}


def stub_calls(handle: dict) -> list[str]:
    text = handle["log"].read_text(encoding="utf-8")
    return [line for line in text.splitlines() if line.strip()]


def start_fake_stage(
    tmp_path: Path,
    line: str,
    run: str,
    stage: str = "plan",
    *,
    mode: str | None = None,
    duration: float = 3.0,
    finish: str = "done",
) -> dict:
    """Launch a driver shell plus a fake stage runner.

    ``mode=detached`` puts the runner in its own session (survives a driver
    process-group kill); ``mode=foreground`` joins the driver's process group
    (dies with it).  ``SDD_RUNNER_MODE`` overrides the argument so the mutation
    drill can force the foreground shape.
    """
    root = tmp_path / f"stage-{line}-{stage}"
    root.mkdir(parents=True, exist_ok=True)
    paths = four_piece(root, line, run, stage, pid=os.getpid(), envelope=True)
    runner = root / "fake-runner.sh"
    if finish == "done":
        body = f"""
printf 'PLAN-DONE\\n' >> "{paths['log']}"
printf 'exit=0 at=%s sentinel=1 line={line} run={run} stage={stage} event=status\\n' "$(date +%s)" > "{paths['status']}.tmp" && mv "{paths['status']}.tmp" "{paths['status']}"
"""
    elif finish == "stdout-only":
        body = "printf 'PLAN-DONE\\n' >> \"" + str(paths["log"]) + "\"\n"
    else:
        body = "exit 3\n"
    runner.write_text(
        "#!/usr/bin/env bash\n"
        "set -u\n"
        f'pidf="{paths["pid"]}"\n'
        f'hb="{paths["heartbeat"]}"\n'
        f'meta="{paths["meta"]}"\n'
        'if [ -r "/proc/$$/stat" ]; then start=$(awk \'{print $22}\' "/proc/$$/stat"); '
        'else start=$(ps -p $$ -o lstart= | tr -s "[:space:]" " " | sed "s/^ //; s/ $//"); fi\n'
        f'printf "pid=%s start=%s at=%s line={line} run={run} stage={stage} event=pid\\n" "$$" "$start" "$(date +%s)" > "$pidf"\n'
        f'printf "{{}} " > /dev/null\n'
        f'( while kill -0 $$ 2>/dev/null; do printf "at=%s line={line} run={run} stage={stage} event=heartbeat\\n" "$(date +%s)" > "$hb"; sleep 0.5; done ) &\n'
        f'hbpid=$!\n'
        f'sleep {duration}\n'
        f'kill "$hbpid" 2>/dev/null || true\n'
        f'{body}'
        f'exit 0\n',
        encoding="utf-8",
    )
    runner.chmod(0o755)

    driver = subprocess.Popen(
        ["bash", "-c", f'echo $$ > "{root / "driver.pid"}"; sleep 30'],
        start_new_session=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    selected = os.environ.get("SDD_RUNNER_MODE", mode or "detached")
    kwargs = dict(
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if selected == "detached":
        kwargs["start_new_session"] = True
        runner_proc = subprocess.Popen(["bash", str(runner)], **kwargs)
    else:
        runner_proc = subprocess.Popen(
            ["bash", str(runner)],
            preexec_fn=lambda: os.setpgid(0, driver.pid),
            **kwargs,
        )
    return {
        "root": root,
        "paths": paths,
        "driver": driver,
        "runner": runner_proc,
        "runner_script": runner,
        "mode": selected,
    }


def kill_driver_group(stage: dict, sig=signal.SIGHUP) -> None:
    try:
        os.killpg(os.getpgid(stage["driver"].pid), sig)
    except ProcessLookupError:
        pass


def teardown_stage(stage: dict) -> None:
    for proc in (stage.get("runner"), stage.get("driver")):
        if proc is None:
            continue
        try:
            proc.terminate()
        except Exception:
            pass
    for proc in (stage.get("runner"), stage.get("driver")):
        if proc is None:
            continue
        try:
            proc.wait(timeout=3)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass


def wait_until(predicate, timeout: float = 5.0, interval: float = 0.05) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def snapshot(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def remove_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
