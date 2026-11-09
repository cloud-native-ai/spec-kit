"""Throwaway repository + local bare remote per workflow model, and the executing half.

The executing half performs the *derived* steps with real git so the assertions can read
end state (`closeout-verification.contract.md` C-2). It is deliberately small: it does not
reimplement the skill's prose, it executes the plan ``plan.derive_closeout`` produced.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Sequence

from tests.fixtures.git_closeout.plan import CloseoutPlan, Step, derive_closeout

#: Model -> (trunk, daily, archive, tiers) as the fixture seeds them.
MODEL_BRANCHES: dict[str, dict] = {
    "single-branch": {"trunk": "master"},
    "dual-branch": {"trunk": "develop", "daily": "develop", "archive": "archive"},
    "temp-branch": {"trunk": "master"},
    "three-tier": {"tiers": ("main", "pre", "dev")},
}

#: The message of the committed artifact the close-out must not re-commit. A caller that
#: passes no `paths` presents "nothing new to include", which is the artifacts-without-records
#: fork (C-5 fork 2) — so the constant is named once here instead of being duplicated as a
#: private opinion in the driver.
ARTIFACT_MESSAGE = "docs(091-fixture): artifact commit"

_IDENTITY = {
    "GIT_AUTHOR_NAME": "closeout-fixture",
    "GIT_AUTHOR_EMAIL": "closeout@example.invalid",
    "GIT_COMMITTER_NAME": "closeout-fixture",
    "GIT_COMMITTER_EMAIL": "closeout@example.invalid",
}


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env.update(_IDENTITY)
    # never inherit a host hook path or a host identity into a fixture repository
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


def _git(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, env=_env(), check=False
    )
    if check and proc.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed in {cwd}:\n{proc.stdout}{proc.stderr}")
    return proc


@dataclass
class CloseoutRepo:
    """One fixture project: a working repository plus one local bare remote per declared name.

    ``root`` is the temporary directory; it is removed by :meth:`cleanup` (tests use the
    context manager, which always tears down).
    """

    root: Path
    repo: Path
    remotes: dict[str, Path]
    trunk: str = "master"
    _tmp: tempfile.TemporaryDirectory | None = field(default=None, repr=False)

    # --- readings -----------------------------------------------------------
    def head_of(self, branch: str) -> str | None:
        proc = _git("rev-parse", "--verify", "--quiet", f"refs/heads/{branch}", cwd=self.repo, check=False)
        return proc.stdout.strip() or None

    def branches(self) -> set[str]:
        proc = _git("for-each-ref", "--format=%(refname:short)", "refs/heads", cwd=self.repo)
        return {line for line in proc.stdout.splitlines() if line}

    def remote_refs(self, remote: str) -> set[str]:
        bare = self.remotes[remote]
        proc = _git("--git-dir", str(bare), "for-each-ref", "--format=%(refname) %(objectname)", cwd=self.root)
        return {line for line in proc.stdout.splitlines() if line}

    def remote_branch_sha(self, remote: str, branch: str) -> str | None:
        for line in self.remote_refs(remote):
            ref, sha = line.split(" ", 1)
            if ref == f"refs/heads/{branch}":
                return sha
        return None

    def log_subjects(self, branch: str = "HEAD") -> list[str]:
        proc = _git("log", "--format=%s", branch, cwd=self.repo)
        return [line for line in proc.stdout.splitlines() if line]

    def status_porcelain_as_text(self) -> str:
        """The working tree's porcelain listing, as one string — the "left where it was" read."""
        return _git("status", "--porcelain", cwd=self.repo).stdout

    def status_porcelain(self) -> set[str]:
        proc = _git("status", "--porcelain", cwd=self.repo)
        return {line for line in proc.stdout.splitlines() if line}

    def remote_branch_names(self, remote: str) -> list[str]:
        """Ref names on the bare remote, sorted — the short-branch arm reads names only."""
        return sorted({line.split(" ", 1)[0] for line in self.remote_refs(remote)})

    def git(self, *args: str) -> str:
        """Run one git command inside the fixture repository and return its stdout."""
        return _git(*args, cwd=self.repo).stdout

    def is_ancestor(self, ancestor: str, descendant: str) -> bool:
        """True when ``ancestor`` is reachable from ``descendant`` (commit graph, not text)."""
        proc = _git("merge-base", "--is-ancestor", ancestor, descendant, cwd=self.repo, check=False)
        return proc.returncode == 0

    def remote_branches(self, remote: str) -> set[str]:
        """Ref *names* on the bare remote — the end state C-7 compares across runs."""
        return {line.split(" ", 1)[0] for line in self.remote_refs(remote)}

    # --- lifecycle ----------------------------------------------------------
    def cleanup(self) -> None:
        if self._tmp is not None:
            self._tmp.cleanup()
        else:  # pragma: no cover - defensive
            shutil.rmtree(self.root, ignore_errors=True)

    def __enter__(self) -> "CloseoutRepo":
        return self

    def __exit__(self, *_exc) -> None:
        self.cleanup()


def _refuse_framework_root(root: Path) -> None:
    resolved = root.resolve()
    repo_root = Path(__file__).resolve().parents[3]
    if repo_root in resolved.parents or resolved == repo_root:
        raise AssertionError(
            f"refusing to build a fixture repository inside the framework tree: {resolved}"
        )


def build_repo(
    model: str,
    *,
    root: Path | None = None,
    remotes: Sequence[str] = ("mirror",),
    readonly: Sequence[str] = (),
    files: Mapping[str, str] | None = None,
    dirty: Mapping[str, str] | None = None,
    own_tmp: bool = True,
) -> CloseoutRepo:
    """Seed one repository laid out as ``model`` declares, plus one bare remote per name.

    ``files`` are committed as the seeded artifact commit; ``dirty`` are written but left
    uncommitted (the "another line's files" arm of C-5 fork 3). ``readonly`` names the remotes
    the block marks read-only — they are still configured, so an accidental push is possible
    and therefore detectable.
    """
    if root is None:
        tmp = tempfile.TemporaryDirectory(prefix=f"091-closeout-{model}-")
        root = Path(tmp.name)
    else:
        tmp = None
        root.mkdir(parents=True, exist_ok=True)
    _refuse_framework_root(root)

    repo = root / "repo"
    repo.mkdir()
    bare_dirs: dict[str, Path] = {}
    for name in remotes:
        bare = root / f"{name}.git"
        _git("init", "-q", "--bare", str(bare), cwd=root)
        bare_dirs[name] = bare

    shape = MODEL_BRANCHES[model]
    if model == "three-tier":
        trunk = shape["tiers"][-1]  # commit lands on DEV
    elif model == "dual-branch":
        trunk = shape["daily"]
    else:
        trunk = shape["trunk"]

    _git("init", "-q", "-b", trunk, str(repo), cwd=root)
    (repo / "README.md").write_text("fixture\n", encoding="utf-8")
    _git("add", "README.md", cwd=repo)
    _git("commit", "-q", "-m", "seed: fixture repository", cwd=repo)

    if model == "dual-branch":
        _git("branch", shape["archive"], cwd=repo)
    if model == "three-tier":
        main, pre, dev = shape["tiers"]
        # MAIN and PRE already exist as long-lived branches ahead of DEV's seed
        _git("branch", pre, cwd=repo)
        _git("branch", main, cwd=repo)

    for name, bare in bare_dirs.items():
        _git("remote", "add", name, str(bare), cwd=repo)

    for rel, payload in (files or {}).items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")

    if files:
        _git("add", "--", *files.keys(), cwd=repo)
        _git("commit", "-q", "-m", ARTIFACT_MESSAGE, cwd=repo)

    for rel, payload in (dirty or {}).items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")

    return CloseoutRepo(root=root, repo=repo, remotes=bare_dirs, trunk=trunk, _tmp=tmp)


@dataclass
class CloseoutOutcome:
    """What an executed close-out reports — the report field set of `closeout-lifecycle` C-4."""

    exit_code: int
    stage: str
    command: str
    stdout: str
    deviations: tuple[str, ...] = ()
    pushed: tuple[str, ...] = ()
    merged: bool = False
    dry_run: bool = False
    records_commit: str | None = None
    commits: tuple[str, ...] = ()


def _fmt(args: Sequence[str]) -> str:
    return "git " + " ".join(args)


def run_closeout(
    repo: CloseoutRepo,
    plan: CloseoutPlan,
    *,
    paths: Sequence[str] = (),
    message: str = "feat(091): fixture close-out",
    commit_message: str | None = None,
    remote_name: str | None = None,
    dry_run: bool = False,
    attempt_retry: int = 0,
    conflict: bool = False,
) -> CloseoutOutcome:
    """Execute ``plan`` against ``repo``; stop at the first failure and report it verbatim.

    ``dry_run`` renders the plan and performs nothing (`closeout-verification.contract.md`
    C-5). ``attempt_retry`` is a **mutation hook**: when >0 the driver retries the failing
    step that many times, which is exactly the behaviour FR-011 forbids, so a guard can prove
    the mutation turns red.
    """
    commit_message = commit_message or message
    if dry_run:
        return CloseoutOutcome(exit_code=0, stage="dry-run", command="git closeout --dry-run",
                               stdout=plan.render(), dry_run=True)

    if plan.terminal_state == "presented":
        return CloseoutOutcome(exit_code=0, stage="presented", command="git closeout --dry-run",
                               stdout=plan.render())

    deviations: tuple[str, ...] = ()
    dirty = repo.status_porcelain()
    produced = {p for p in paths}
    deviations = tuple(sorted(line for line in dirty if not any(line.endswith(p) for p in produced)))

    commits: list[str] = []
    pushed: list[str] = []
    merged = False
    target_remote = plan.targets[0] if plan.targets else None
    current = repo.trunk

    for step in plan.steps:
        if step.kind in plan.skipped:
            continue
        if step.kind == "commit":
            if paths:
                add = ["add", "--", *paths]
                proc = _git(*add, cwd=repo.repo, check=False)
                if proc.returncode != 0:
                    return CloseoutOutcome(proc.returncode, "add", _fmt(add), proc.stderr, deviations)
            if not paths:
                # nothing new to include: the "artifacts without records" fork (C-5 fork 2).
                # The close-out never invents a record and never creates an empty commit.
                records_commit = "not-created (this close-out carried no records commit)"
            else:
                argv = ["commit", "-q", "-m", commit_message]
                proc = _git(*argv, cwd=repo.repo, check=False)
                if proc.returncode != 0:
                    return CloseoutOutcome(proc.returncode, "commit", _fmt(argv),
                                           proc.stdout + proc.stderr, deviations)
                head = _git("rev-parse", "HEAD", cwd=repo.repo).stdout.strip()
                records_commit = head
                commits.append(head)
            if step.target in repo.branches():
                current = step.target
            continue
        if step.kind == "branch":
            argv = ["checkout", "-q", "-b", step.target]
            proc = _git(*argv, cwd=repo.repo, check=False)
            if proc.returncode != 0:
                found = re.search(r"a branch named '([^']+)' already exists", proc.stderr or "")
                return CloseoutOutcome(
                    proc.returncode, "branch",
                    _fmt(argv),
                    f"branch collision: {found.group(1) if found else step.target}",
                    deviations,
                )
            current = step.target
            continue
        if step.kind == "merge":
            # The merge runs *on its target* and brings in the branch the sequence is coming from
            # (the current cursor). Checking out first is what makes the dual-branch archive arm
            # real: without it the merge lands on the daily branch and the archive never moves.
            _git("checkout", "-q", step.target, cwd=repo.repo)
            argv = ["merge", "--no-ff", "-q", "-m", f"merge: {step.detail}", current]
            if conflict:
                # the fixture seeded a divergent edit on each side, so this merge really conflicts
                proc = _git(*argv, cwd=repo.repo, check=False)
                paths_out = _git("diff", "--name-only", "--diff-filter=U", cwd=repo.repo, check=False)
                return CloseoutOutcome(
                    proc.returncode if proc.returncode else 1, "merge", _fmt(argv),
                    (proc.stdout or "") + (paths_out.stdout or ""), deviations,
                )
            proc = _git(*argv, cwd=repo.repo, check=False)
            if proc.returncode != 0:
                return CloseoutOutcome(proc.returncode, "merge", _fmt(argv), proc.stdout + proc.stderr, deviations)
            merged = True
            current = step.target
            continue
        if step.kind == "delete-branch":
            proc = _git("branch", "-d", step.target, cwd=repo.repo, check=False)
            if proc.returncode != 0:
                return CloseoutOutcome(proc.returncode, "delete-branch", _fmt(["branch", "-d", step.target]),
                                       proc.stderr, deviations)
            continue
        if step.kind == "push":
            if target_remote is None:
                continue
            remotes = [target_remote] if remote_name is None else [remote_name]
            # C-3: a model pushes each branch its sequence declares, one push per branch in the
            # derived order (three-tier: DEV, PRE, MAIN), so a mid-sequence rejection names the
            # branch it was pushing.
            for name in remotes:
                for branch in plan.push_branches:
                    spec = f"{branch}:{branch}"
                    argv = ["push", "-q", name, spec]
                    proc = _git(*argv, cwd=repo.repo, check=False)
                    if proc.returncode != 0 and attempt_retry > 0:
                        for _ in range(attempt_retry):
                            if _git(*argv, cwd=repo.repo, check=False).returncode == 0:
                                proc = None
                                break
                    if proc is None:
                        pushed.append(name)
                        continue
                    if proc.returncode != 0:
                        return CloseoutOutcome(proc.returncode, "push", _fmt(argv),
                                               (proc.stdout or "") + (proc.stderr or ""), deviations,
                                               tuple(pushed), merged)
                    pushed.append(name)
    return CloseoutOutcome(0, "done", "git closeout", plan.render(), deviations, tuple(pushed),
                           merged, False, records_commit, tuple(commits))
