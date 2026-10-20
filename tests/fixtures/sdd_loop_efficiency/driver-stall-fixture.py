#!/usr/bin/env python3
"""Driver-side stall observation fixture (SC-010, [[STR-007]]).

This fixture is the single execution body for the stall behavior baseline. It
drives three controlled scenarios against the real ``watch-target.sh`` of a
supplied worktree, executes the documented U4/U5 driver program below, and
reads the seven observed fields back from the artifacts it wrote.

Documented driver program (identical for record and replay)
-----------------------------------------------------------
U2  write the dispatch marker to the line state spine, then start the stub
    runner (write-before-action).
U3  run ``watch-target.sh`` in a bounded window and parse its verdict line.
U4  INCOMPLETE -> write ``verdict`` / ``stall_state=incomplete-fake-done`` to
    the spine; do not dispatch a next stage.
U5  FAILED -> consume retries starting from ``--initial-retries`` (only 0 is
    allowed); when the retry limit is reached, write
    ``stall_state=stalled-retry-limit`` and the four-element escalation package.
U5  TIMEOUT -> take a ``--once`` snapshot, then write
    ``stall_state=stalled-timeout`` and the four-element escalation package.

Field values are observed, never transcribed: the fixture does not contain an
expected verdict/state tuple and never reads field values out of a baseline
file except when comparing a replay against it (SB-5).

Modes
-----
  driver-stall-fixture.py --record --worktree PATH --out JSON
  driver-stall-fixture.py --replay --worktree PATH --baseline JSON --out JSON
                           [--initial-retries 0]
  driver-stall-fixture.py --self-test

Python >= 3.8, standard library only.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

RETRY_LIMIT = 2
SCENARIOS = ("timeout", "retry-limit", "fake-done")
WATCHER_REL = "skills/external/sdd-loop-driver/scripts/watch-target.sh"


def now_epoch():
    return int(time.time())


def write_text(path, text):
    Path(path).write_text(text, encoding="utf-8")


def append_text(path, text):
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(text)


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return ""


def atomic_write(path, text):
    tmp = path + ".tmp"
    write_text(tmp, text)
    os.replace(tmp, path)


def parse_kv(text, key):
    value = ""
    for line in text.splitlines():
        match = re.match(r"^%s=(.*)$" % re.escape(key), line.strip())
        if match:
            value = match.group(1).strip()
    return value


def watcher_verdict(stdout):
    for line in stdout.splitlines():
        if line.startswith("WATCH "):
            match = re.search(r"\bverdict=([A-Z_]+)", line)
            if match:
                return match.group(1)
    return ""


STUB_RUNNER = r"""#!/usr/bin/env bash
set -u
scenario="$1"
dir="$2"
attempt="$3"
printf 'pid=%s at=%s\n' "$$" "$(date +%s)" > "$dir/pid-$attempt"
printf '%s' "$(date +%s)" > "$dir/heartbeat-$attempt"
: > "$dir/log-$attempt.log"
case "$scenario" in
  timeout)
    sleep "${STUB_TIMEOUT_SLEEP:-2}"
    printf 'runner_rc=124\n' > "$dir/runner-rc-$attempt"
    exit 124
    ;;
  retry-limit)
    printf 'exit=1 at=%s sentinel=0\n' "$(date +%s)" > "$dir/status-$attempt.tmp"
    mv "$dir/status-$attempt.tmp" "$dir/status-$attempt"
    printf 'runner_rc=1\n' > "$dir/runner-rc-$attempt"
    exit 1
    ;;
  fake-done)
    printf 'exit=0 at=%s sentinel=0\n' "$(date +%s)" > "$dir/status-$attempt.tmp"
    mv "$dir/status-$attempt.tmp" "$dir/status-$attempt"
    printf 'runner_rc=0\n' > "$dir/runner-rc-$attempt"
    exit 0
    ;;
  *)
    printf 'runner_rc=2\n' > "$dir/runner-rc-$attempt"
    exit 2
    ;;
esac
"""


def prepare_stub(state_dir):
    path = os.path.join(state_dir, "stub-runner.sh")
    write_text(path, STUB_RUNNER)
    os.chmod(path, 0o755)
    return path


def wait_for(path, timeout):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if os.path.exists(path):
            return True
        time.sleep(0.05)
    return False


def run_watcher(worktree, state_dir, attempt, timeout_s=15):
    watcher = os.path.join(worktree, WATCHER_REL)
    help_text = subprocess.run(
        ["bash", watcher, "--help"], capture_output=True, text=True
    ).stdout
    cmd = [
        "bash", watcher,
        "--label", "fixture",
        "--pid-file", os.path.join(state_dir, "pid-%d" % attempt),
        "--status-file", os.path.join(state_dir, "status-%d" % attempt),
        "--log", os.path.join(state_dir, "log-%d.log" % attempt),
        "--heartbeat", os.path.join(state_dir, "heartbeat-%d" % attempt),
        "--sentinel", "FIXTURE-DONE",
        "--window", "4",
        "--interval", "1",
        "--start-grace", "1",
        "--timeout", "1",
    ]
    if "--deadline-grace" in help_text:
        cmd += ["--deadline-grace", "0"]
    completed = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)
    return completed.returncode, completed.stdout + completed.stderr


def write_escalation(path, verdict, retries, evidence):
    text = (
        "## 发现了什么\n"
        "watcher verdict=%s after %d consumed retries.\n\n"
        "## 为何吃重\n"
        "stage did not reach a completion sentinel; evidence: %s\n\n"
        "## 已产生的中间产物\n"
        "- %s\n\n"
        "## 可选处置\n"
        "inspect the preserved state directory and decide retry or stop.\n"
    ) % (verdict, retries, evidence, evidence)
    write_text(path, text)


def escalation_complete(path):
    text = read_text(path)
    if not text:
        return "not-applicable"
    markers = ["## 发现了什么", "## 为何吃重", "## 已产生的中间产物", "## 可选处置"]
    return "true" if all(marker in text for marker in markers) else "false"


def spine_write(spine_path, events_path, step, text):
    append_text(spine_path, text.rstrip("\n") + "\n")
    append_text(events_path, "WRITE step=%d %s\n" % (step, text.split("=")[0]))


def spine_action(events_path, step, action):
    append_text(events_path, "ACTION step=%d %s\n" % (step, action))


def write_before_action(events_path):
    lines = [line for line in read_text(events_path).splitlines() if line]
    last_write = {}
    ok = True
    for index, line in enumerate(lines):
        parts = line.split()
        if len(parts) < 2 or not parts[1].startswith("step="):
            continue
        step = int(parts[1].split("=", 1)[1])
        if parts[0] == "WRITE":
            last_write[step] = index
        elif parts[0] == "ACTION":
            if step not in last_write or last_write[step] > index:
                ok = False
    return "yes" if ok else "no"


def run_scenario(worktree, scenario, root_dir, initial_retries):
    if initial_retries != 0:
        raise ValueError("initial_retries must be 0")
    state_dir = os.path.join(root_dir, scenario)
    os.makedirs(state_dir, exist_ok=True)
    spine_path = os.path.join(state_dir, "spine.md")
    events_path = os.path.join(state_dir, "events.log")
    dispatch_path = os.path.join(state_dir, "dispatch.log")
    escalation_path = os.path.join(state_dir, "escalation-package.md")
    write_text(spine_path, "# fixture line state spine\n")
    write_text(events_path, "")
    write_text(dispatch_path, "")
    stub = prepare_stub(state_dir)

    retries = initial_retries
    attempt = 0
    verdict = ""
    watcher_rc = 0
    step = 1
    spine_write(spine_path, events_path, step, "dispatch stage=attempt-%d" % attempt)
    spine_action(events_path, step, "launch-runner")
    subprocess.Popen(["bash", stub, scenario, state_dir, str(attempt)])

    while True:
        wait_for(os.path.join(state_dir, "pid-%d" % attempt), 3.0)
        if scenario != "timeout":
            wait_for(os.path.join(state_dir, "status-%d" % attempt), 3.0)
        watcher_rc, output = run_watcher(worktree, state_dir, attempt)
        verdict = watcher_verdict(output)
        write_text(os.path.join(state_dir, "watcher-%d.out" % attempt), output)
        if verdict in ("DONE", "INCOMPLETE"):
            step += 1
            spine_write(spine_path, events_path, step, "verdict=%s" % verdict)
            spine_write(spine_path, events_path, step,
                        "stall_state=incomplete-fake-done")
            break
        if verdict == "FAILED":
            if retries < RETRY_LIMIT:
                retries += 1
                step += 1
                spine_write(spine_path, events_path, step,
                            "retry_consumed=%d reason=FAILED" % retries)
                attempt += 1
                step += 1
                spine_write(spine_path, events_path, step,
                            "dispatch stage=attempt-%d" % attempt)
                spine_action(events_path, step, "redispatch-runner")
                subprocess.Popen(["bash", stub, scenario, state_dir, str(attempt)])
                continue
            step += 1
            spine_write(spine_path, events_path, step,
                        "stall_state=stalled-retry-limit")
            write_escalation(escalation_path, verdict, retries, spine_path)
            spine_action(events_path, step, "emit-escalation")
            break
        if verdict == "TIMEOUT":
            step += 1
            spine_write(spine_path, events_path, step,
                        "once_snapshot verdict=%s" % verdict)
            spine_action(events_path, step, "once-snapshot")
            step += 1
            spine_write(spine_path, events_path, step,
                        "stall_state=stalled-timeout")
            write_escalation(escalation_path, verdict, retries, spine_path)
            spine_action(events_path, step, "emit-escalation")
            break
        step += 1
        spine_write(spine_path, events_path, step,
                    "stall_state=unexpected-%s" % (verdict.lower() or "none"))
        break

    step += 1
    spine_write(spine_path, events_path, step, "retries_consumed=%d" % retries)
    wait_for(os.path.join(state_dir, "runner-rc-%d" % attempt), 6.0)
    runner_rc = parse_kv(read_text(os.path.join(state_dir, "runner-rc-%d" % attempt)),
                        "runner_rc")
    status_rc = parse_kv(read_text(os.path.join(state_dir, "status-%d" % attempt)),
                         "exit").split(" ")[0]
    if status_rc:
        runner_rc = status_rc
    spine_text = read_text(spine_path)
    dispatch_text = read_text(dispatch_path)
    return {
        "scenario": scenario,
        "watcher_verdict": verdict,
        "exit_code": {
            "watcher": watcher_rc,
            "runner": int(runner_rc) if runner_rc else "na",
        },
        "spine_stall_state": parse_kv(spine_text, "stall_state"),
        "retries_consumed": int(parse_kv(spine_text, "retries_consumed")),
        "escalation_package_complete": escalation_complete(escalation_path),
        "next_stage_dispatched": "yes" if "next_stage=" in dispatch_text else "no",
        "spine_write_before_action": write_before_action(events_path),
        "evidence_ptr": spine_path,
    }


def run_all_scenarios(worktree, root_dir, initial_retries):
    observations = []
    for scenario in SCENARIOS:
        scenario_root = os.path.join(root_dir, scenario + "-run")
        os.makedirs(scenario_root, exist_ok=True)
        observations.append(run_scenario(worktree, scenario, scenario_root,
                                         initial_retries))
    return observations


def git_commit(worktree):
    return subprocess.run(
        ["git", "-C", worktree, "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def normalize_record(record):
    clone = json.loads(json.dumps(record))
    for scenario in clone.get("scenarios", []):
        pointer = scenario.get("evidence_ptr", "")
        scenario["evidence_ptr"] = os.path.basename(pointer)
    return clone


def compare_records(baseline, replay):
    differences = []
    if baseline.get("initial_retries") != replay.get("initial_retries"):
        differences.append("initial_retries")
    base_scenarios = {item["scenario"]: item for item in baseline.get("scenarios", [])}
    new_scenarios = {item["scenario"]: item for item in replay.get("scenarios", [])}
    for name in sorted(set(base_scenarios) | set(new_scenarios)):
        if name not in base_scenarios or name not in new_scenarios:
            differences.append("%s:scenario-missing" % name)
            continue
        for field in sorted(base_scenarios[name]):
            if base_scenarios[name][field] != new_scenarios[name][field]:
                differences.append("%s:%s" % (name, field))
    return differences


def record(worktree, out):
    root_dir = tempfile.mkdtemp(prefix="stall-fixture-")
    try:
        scenarios = run_all_scenarios(worktree, root_dir, 0)
        record_data = {
            "base_commit": git_commit(worktree),
            "recorded_at": now_epoch(),
            "initial_retries": 0,
            "scenarios": scenarios,
        }
        write_text(out, json.dumps(record_data, indent=2, ensure_ascii=False) + "\n")
        return record_data
    finally:
        shutil.rmtree(root_dir, ignore_errors=True)


def replay(worktree, baseline_path, out, initial_retries):
    baseline = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
    root_dir = tempfile.mkdtemp(prefix="stall-replay-")
    try:
        scenarios = run_all_scenarios(worktree, root_dir, initial_retries)
        replay_data = {
            "base_commit": git_commit(worktree),
            "recorded_at": now_epoch(),
            "initial_retries": initial_retries,
            "scenarios": scenarios,
        }
        normalized_base = normalize_record(baseline)
        normalized_replay = normalize_record(replay_data)
        differences = compare_records(normalized_base, normalized_replay)
        write_text(
            out,
            json.dumps(
                {"differences": differences, "replay": normalized_replay},
                indent=2,
                ensure_ascii=False,
            ) + "\n",
        )
        return differences
    finally:
        shutil.rmtree(root_dir, ignore_errors=True)


def self_test():
    repo_root = Path(__file__).resolve().parents[3]
    root_dir = tempfile.mkdtemp(prefix="stall-selftest-")
    failures = []
    try:
        first = run_all_scenarios(str(repo_root), root_dir, 0)
        second_root = tempfile.mkdtemp(prefix="stall-selftest-2-")
        try:
            second = run_all_scenarios(str(repo_root), second_root, 0)
        finally:
            shutil.rmtree(second_root, ignore_errors=True)

        record_a = {"initial_retries": 0, "scenarios": first}
        record_b = {"initial_retries": 0, "scenarios": second}
        if compare_records(normalize_record(record_a), normalize_record(record_b)):
            failures.append("record is not reproducible under normalization")

        for scenario in first:
            name = scenario["scenario"]
            if scenario["spine_write_before_action"] != "yes":
                failures.append("%s: write-before-action violated" % name)
            if scenario["exit_code"]["watcher"] not in (0, 10, 11, 12, 13, 14, 15, 16):
                failures.append("%s: watcher exit code not from the verdict table" % name)
            if not isinstance(scenario["exit_code"], dict) or "runner" not in scenario["exit_code"]:
                failures.append("%s: exit_code must carry both watcher and runner" % name)
        if not failures:
            for scenario in first:
                if scenario["watcher_verdict"] == "TIMEOUT":
                    if scenario["escalation_package_complete"] != "true":
                        failures.append("timeout: escalation package incomplete")
                elif scenario["watcher_verdict"] == "FAILED":
                    if scenario["retries_consumed"] != RETRY_LIMIT:
                        failures.append("retry-limit: retries_consumed not at limit")
                    if scenario["escalation_package_complete"] != "true":
                        failures.append("retry-limit: escalation package incomplete")
                elif scenario["watcher_verdict"] == "INCOMPLETE":
                    if scenario["next_stage_dispatched"] != "no":
                        failures.append("fake-done: next stage dispatched")
                else:
                    failures.append("unexpected verdict shape: %s" % scenario["watcher_verdict"])

        mutated = normalize_record({"initial_retries": 0, "scenarios": first})
        mutated["scenarios"][0]["watcher_verdict"] = "MUTATED"
        if not compare_records(normalize_record(record_a), mutated):
            failures.append("comparison did not flag a changed verdict")
    finally:
        shutil.rmtree(root_dir, ignore_errors=True)

    if failures:
        for failure in failures:
            print("FAIL: %s" % failure)
        return 1
    print("PASS: driver-stall-fixture self-test")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--worktree")
    parser.add_argument("--out")
    parser.add_argument("--baseline")
    parser.add_argument("--initial-retries", type=int, default=0)
    args = parser.parse_args(argv)

    modes = [args.record, args.replay, args.self_test]
    if sum(1 for mode in modes if mode) != 1:
        parser.error("choose exactly one of --record, --replay, --self-test")

    if args.initial_retries != 0:
        parser.error("--initial-retries only accepts 0")

    if args.self_test:
        return self_test()
    if not args.worktree or not args.out:
        parser.error("--worktree and --out are required")
    if args.record:
        record(args.worktree, args.out)
        return 0
    if not args.baseline:
        parser.error("--replay requires --baseline")
    differences = replay(args.worktree, args.baseline, args.out, args.initial_retries)
    if differences:
        for difference in differences:
            print("DIFF: %s" % difference)
        return 1
    print("PASS: replay matches baseline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
