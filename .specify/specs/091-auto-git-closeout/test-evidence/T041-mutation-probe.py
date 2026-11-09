"""T041 / SC-003 — the mutation probe for FR-011 ("fail at the first failure, never retry").

Nothing in the tree is modified: the fixture driver exposes ``attempt_retry`` as a mutation hook,
so the mutation is applied to *behaviour* rather than to a string. Each arm runs the landed driver
(retry = 0) and then the mutated driver (retry = 2), and the probe asserts on the axis the
mutation actually moves — ``CloseoutOutcome.retries``.

Read-only with respect to the repository: the fixture repositories live under
``tempfile.TemporaryDirectory()`` and are torn down per arm.

Two readings recorded by this probe (the second one is a limit, not a pass):
  * rejected push   — the hook fires (``retries == 2``), so a guard CAN notice a retry here.
  * merge conflict  — the hook never fires (``retries == 0``); the merge arm's guarantee is
    "stops at the merge, no push after it", which a retry of the push would not change.

Run: /usr/bin/python3 .specify/specs/091-auto-git-closeout/test-evidence/T041-mutation-probe.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT))

from tests.fixtures.git_closeout import build_repo, derive_closeout, run_closeout  # noqa: E402

SEED = ".specify/memory/session/091-mutation-record.md"


def _seed(repo) -> tuple[str, ...]:
    path = repo.repo / SEED
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("run: 091 mutation arm\n", encoding="utf-8")
    return (SEED,)


def _advance_remote(repo, remote: str = "mirror", branch: str = "master") -> None:
    repo.git("push", "-q", remote, f"{branch}:{branch}")
    side = repo.root / "side-clone"
    subprocess.run(
        ["git", "clone", "-q", str(repo.remotes[remote]), str(side)],
        check=True, capture_output=True, text=True,
    )
    env = {
        "GIT_AUTHOR_NAME": "side", "GIT_AUTHOR_EMAIL": "side@example.invalid",
        "GIT_COMMITTER_NAME": "side", "GIT_COMMITTER_EMAIL": "side@example.invalid",
        "GIT_CONFIG_NOSYSTEM": "1",
    }
    subprocess.run(
        ["git", "commit", "-q", "--allow-empty", "-m", "side: diverging commit"],
        cwd=str(side), check=True, capture_output=True, text=True, env=env,
    )
    subprocess.run(
        ["git", "push", "-q", "origin", f"{branch}:{branch}"],
        cwd=str(side), check=True, capture_output=True, text=True, env=env,
    )


def rejected_push(attempt_retry: int):
    with build_repo("single-branch") as repo:
        _advance_remote(repo)
        before = repo.remote_branch_sha("mirror", "master")
        plan = derive_closeout(
            model="single-branch", strategy="commit+merge+push", remotes=["mirror"], readonly=[]
        )
        outcome = run_closeout(repo, plan, paths=_seed(repo), attempt_retry=attempt_retry)
        return outcome, before, repo.remote_branch_sha("mirror", "master")


def merge_conflict(attempt_retry: int):
    with build_repo("dual-branch") as repo:
        repo.git("commit", "-q", "--allow-empty", "-m", "seed: archive line base")
        repo.git("update-ref", "refs/heads/archive", "HEAD")
        repo.git("checkout", "-q", "archive")
        target = repo.repo / "conflict.txt"
        target.write_text("archive line\n", encoding="utf-8")
        repo.git("add", "--", "conflict.txt")
        repo.git("commit", "-q", "-m", "archive: divergent edit")
        repo.git("checkout", "-q", "develop")
        target.write_text("daily line\n", encoding="utf-8")
        repo.git("add", "--", "conflict.txt")
        repo.git("commit", "-q", "-m", "daily: divergent edit")
        plan = derive_closeout(
            model="dual-branch", strategy="commit+merge+push", remotes=["mirror"], readonly=[]
        )
        return run_closeout(repo, plan, paths=_seed(repo), conflict=True, attempt_retry=attempt_retry)


def main() -> int:
    failures: list[str] = []
    print("arm | retry | exit | stage | retries | remote unchanged")
    print("----|-------|------|-------|---------|-----------------")

    landed, before, after = rejected_push(0)
    ok = (
        landed.exit_code != 0
        and landed.stage == "push"
        and after == before
        and landed.retries == 0
    )
    print(f"A rejected-push | 0 | {landed.exit_code} | {landed.stage} | {landed.retries} "
          f"| {after == before} | {'GREEN' if ok else 'RED'}")
    if not ok:
        failures.append("arm A: the landed driver does not satisfy the clause predicate")

    mutated, before_m, after_m = rejected_push(2)
    ok = (
        mutated.exit_code != 0
        and mutated.stage == "push"
        and after_m == before_m
        and mutated.retries > 0
    )
    print(f"A rejected-push | 2 | {mutated.exit_code} | {mutated.stage} | {mutated.retries} "
          f"| {after_m == before_m} | {'GREEN' if ok else 'RED'}")
    if not ok:
        failures.append("arm A: the injected retry never fired — the arm proves nothing")

    landed_m = merge_conflict(0)
    ok = landed_m.stage == "merge" and landed_m.pushed == () and landed_m.retries == 0
    print(f"B merge-conflict | 0 | {landed_m.exit_code} | {landed_m.stage} | {landed_m.retries} "
          f"| n/a | {'GREEN' if ok else 'RED'}")
    if not ok:
        failures.append("arm B: the landed merge arm does not satisfy the clause predicate")

    mutated_m = merge_conflict(2)
    ok = mutated_m.stage == "merge" and mutated_m.pushed == () and mutated_m.retries == 0
    print(f"B merge-conflict | 2 | {mutated_m.exit_code} | {mutated_m.stage} | {mutated_m.retries} "
          f"| n/a | {'GREEN' if ok else 'RED'}")
    if not ok:
        failures.append("arm B: the merge arm changed under the mutation — re-read the limit")

    print()
    print("Verdict:")
    print("  arm A — the retry hook fires (retries=2) and the driver still reports the failing")
    print("          stage, the exact command and an unchanged remote; the landed guard asserts")
    print("          retries == 0, so a retry in the tree would red it.")
    print("  arm B — recorded limit: the hook is a push-step hook, so the merge arm is unchanged;")
    print("          its guarantee ('stops at the merge, no push after it') is what it proves.")
    if failures:
        for line in failures:
            print(f"MUTATION-PROBE-FAIL: {line}")
        return 1
    print("MUTATION-PROBE: pass")
    return 0


# ---------------------------------------------------------------------------------------------
# R-15 probe (adjudication input, not part of T041): the four strategy values as *behaviour*
# ---------------------------------------------------------------------------------------------
# The reference states the value -> authorized-action transition as a table. Read here against the
# fixture driver so the verification record can cite a measurement rather than the prose alone.
# Run with `--r15` to print it; the default run is the T041 probe above.
def r15_probe() -> int:
    seed = ".specify/memory/retention/closeout/20261109T120000Z-091-r15-probe.md"
    printed = 0
    with build_repo("single-branch") as repo:
        path = repo.repo / seed
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("receipt probe\n", encoding="utf-8")
        for strategy in ("commit+merge+push", "commit+merge", "commit-only", "ask"):
            plan = derive_closeout(
                model="single-branch", strategy=strategy, remotes=["mirror"], readonly=["origin"]
            )
            outcome = run_closeout(repo, plan, paths=(seed,))
            print(
                f"{strategy:18} terminal={plan.terminal_state:9} exit={outcome.exit_code} "
                f"stage={outcome.stage:9} merged={outcome.merged} pushed={outcome.pushed} "
                f"records_commit={bool(outcome.records_commit)}"
            )
            printed += 1
    return 0 if printed == 4 else 1


if __name__ == "__main__":
    raise SystemExit(r15_probe() if "--r15" in sys.argv else main())
