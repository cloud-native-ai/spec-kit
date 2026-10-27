"""Throwaway-git-repository harness for the Feature 071 (review x code-review) contract groups.

Owned by: Feature 071, task T003 (`.specify/specs/071-review-code-integration/tasks.md`).
Consumers: `tests/contract/test_code_review_skill_contract.py` (T010),
`tests/contract/test_coverage_receipt.py` (T014); regression edge T036.

What it is
----------
A deterministic, stdlib-only builder for a **disposable** git repository plus a
thin driver around `skills/internal/code-review/scripts/git-delta-review.sh`,
so the base, header, receipt and verdict assertions are proven against real git
behaviour instead of against prose (T003's checkpoint).

Two rules this module holds itself to
-------------------------------------
1. **It never writes the framework repository.** Every repository it builds lives
   under a caller-supplied root (pytest `tmp_path`) or a library-managed
   `tempfile.mkdtemp()`, and construction refuses a root that resolves inside the
   framework source tree. The process working directory is never changed: every
   git and script invocation receives an explicit ``cwd``.
2. **`DELTA_BIN` is explicit, defaulting to a binary that does not exist.** The
   renderer-absence path must be drivable on a host that *has* the renderer, so
   the default points at a non-existent path inside the temporary repository
   (`.delta-missing`); pass ``delta_bin=repo.host_delta_bin()`` for the rendered
   case. Selection also needs a TTY, so a present renderer alone must not flip
   the mode.

The three delta shapes (FR-003's applicability predicate)
--------------------------------------------------------
``Repo.shape("code")``       base..head adds a code path AND a spec artifact -> ``run``
``Repo.shape("spec-only")``  base..head adds only spec artifacts        -> ``not-applicable``
``Repo.shape("empty")``      base == head, zero changed files           -> ``not-applicable``

A predicate that can only be driven in one direction proves nothing, so all three
are materialised by ``build_standard_history()`` and each is reachable from the
same repository state.

Receipt grammar
---------------
``parse_receipt`` reads the block owned by `contracts/coverage-receipt.md`
C-31…C-33: the literal ``<!-- coverage-receipt:begin -->`` / ``...end -->``
delimiters, one ``name=value`` per line, a closed scalar name set, and
``file.<NN>.path`` / ``.verdict`` / ``.reason`` rows in zero-padded ordinal order.
The parser raises on a malformed line (the grammar is meant to be stable enough
that no heuristics are needed, C-42) and never raises merely because a *name* is
outside the closed set: unknown names land in ``Receipt.unknown_names`` so the
test can assert closedness rather than have the parser hide it.

Run the module directly for its own round-trip self-check:

    python3 tests/fixtures/review_git_repo.py
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

# --------------------------------------------------------------------------- #
# Framework locations (read-only; nothing here is ever written)
# --------------------------------------------------------------------------- #

FRAMEWORK_ROOT = Path(__file__).resolve().parents[2]
REVIEW_SCRIPT_SOURCE = (
    FRAMEWORK_ROOT / "skills" / "internal" / "code-review" / "scripts" / "git-delta-review.sh"
)

#: The mirror path the quickstart (T034) drives; available for a caller that wants
#: to pin the projection rather than the source.
REVIEW_SCRIPT_MIRROR = (
    FRAMEWORK_ROOT / ".specify" / "skills" / "internal" / "code-review" / "scripts" / "git-delta-review.sh"
)

# --------------------------------------------------------------------------- #
# Receipt grammar (owner: contracts/coverage-receipt.md C-31…C-33, C-42)
# --------------------------------------------------------------------------- #

RECEIPT_BEGIN = "<!-- coverage-receipt:begin -->"
RECEIPT_END = "<!-- coverage-receipt:end -->"

#: The closed scalar name set (C-32). Assert membership in a test rather than
#: here, so a contract test can red when the set drifts.
RECEIPT_SCALAR_FIELDS: Tuple[str, ...] = (
    "receipt_version",
    "base",
    "head",
    "base_source",
    "renderer",
    "changed_files",
    "judged_files",
    "skipped_files",
    "gap_files",
    "lines_added",
    "lines_deleted",
)

RECEIPT_COUNT_FIELDS: Tuple[str, ...] = (
    "changed_files",
    "judged_files",
    "skipped_files",
    "gap_files",
)

_FILE_ROW_RE = re.compile(r"^file\.(\d+)\.(path|verdict|reason)=(.*)$")

#: Triage values owned by requirements.md (STR-001 / STR-005) and the recording
#: target name owned by STR-004.
TRIAGE_RUN = "run"
TRIAGE_NOT_APPLICABLE = "not-applicable"
TRIAGE_NOT_EVALUATED = "not-evaluated"
RECORD_FILENAME = "code-review.md"


class ReceiptParseError(AssertionError):
    """The receipt block is structurally unreadable — a grammar violation (C-42)."""


@dataclass
class FileRow:
    """One per-file receipt entry (C-32/C-33)."""

    ordinal: int
    ordinal_token: str
    path: str
    verdict: Optional[str] = None
    reason: Optional[str] = None

    def as_dict(self) -> Dict[str, Optional[str]]:
        return {"path": self.path, "verdict": self.verdict, "reason": self.reason}


@dataclass
class Receipt:
    """A parsed coverage-receipt block."""

    fields: Dict[str, str]
    rows: List[FileRow]
    raw: str

    # -- precedence-preserving access ------------------------------------- #

    def get(self, name: str, default: Optional[str] = None) -> Optional[str]:
        return self.fields.get(name, default)

    def count(self, name: str) -> int:
        """Read one of the four counts as an int, failing loudly when absent."""
        value = self.fields.get(name)
        if value is None:
            raise ReceiptParseError(f"receipt field {name!r} is missing")
        return int(value)

    def verdict_of(self, path: str) -> Optional[str]:
        for row in self.rows:
            if row.path == path:
                return row.verdict
        return None

    def row_for(self, path: str) -> Optional[FileRow]:
        for row in self.rows:
            if row.path == path:
                return row
        return None

    # -- derived properties a contract test can assert --------------------- #

    @property
    def paths(self) -> List[str]:
        return [row.path for row in self.rows]

    @property
    def unknown_names(self) -> List[str]:
        """Names outside the closed scalar + per-file set (C-32)."""
        known = set(RECEIPT_SCALAR_FIELDS)
        unknown = [name for name in self.fields if name not in known]
        return unknown

    @property
    def ordinals(self) -> List[int]:
        return [row.ordinal for row in self.rows]

    @property
    def ordinals_are_contiguous(self) -> bool:
        return self.ordinals == list(range(1, len(self.rows) + 1))

    @property
    def paths_are_sorted(self) -> bool:
        return self.paths == sorted(self.paths)

    @property
    def counting_identity_holds(self) -> bool:
        """C-42: judged_files + skipped_files + gap_files == changed_files."""
        try:
            return (
                self.count("judged_files")
                + self.count("skipped_files")
                + self.count("gap_files")
                == self.count("changed_files")
            )
        except (ReceiptParseError, ValueError):
            return False

    def equality_violations(self) -> List[str]:
        """Everything a byte-identical re-run (C-33) and the identity (C-42) need."""
        problems: List[str] = []
        if not self.paths_are_sorted:
            problems.append(f"per-file rows are not in sorted path order: {self.paths}")
        if not self.ordinals_are_contiguous:
            problems.append(f"ordinals are not contiguous from 1: {self.ordinals}")
        if not self.counting_identity_holds:
            problems.append(
                "counting identity fails: "
                f"judged={self.fields.get('judged_files')} "
                f"skipped={self.fields.get('skipped_files')} "
                f"gap={self.fields.get('gap_files')} "
                f"changed={self.fields.get('changed_files')}"
            )
        if self.unknown_names:
            problems.append(f"names outside the closed set: {self.unknown_names}")
        return problems


def parse_receipt(text: str) -> Optional[Receipt]:
    """Parse the receipt block out of a record/report body.

    Returns ``None`` when the delimiters are absent entirely — the state C-35
    requires for exit ``2`` ("writes no block"). A begin marker without its end
    marker, or a line that is neither a comment nor ``name=value``, raises:
    a partial block must never be tolerated (C-35).
    """
    lines = text.splitlines()
    try:
        start = lines.index(RECEIPT_BEGIN)
    except ValueError:
        if RECEIPT_END in [line.strip() for line in lines]:
            raise ReceiptParseError("receipt end marker present without a begin marker")
        return None

    end = None
    for idx in range(start + 1, len(lines)):
        if lines[idx].strip() == RECEIPT_END:
            end = idx
            break
    if end is None:
        raise ReceiptParseError("receipt begin marker present without an end marker")

    body = [line.strip() for line in lines[start + 1 : end]]
    fields: Dict[str, str] = {}
    rows: Dict[str, FileRow] = {}

    for line in body:
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ReceiptParseError(f"receipt line is not name=value: {line!r}")
        name, _, value = line.partition("=")

        file_match = _FILE_ROW_RE.match(line)
        if file_match:
            ordinal_token, attr, file_value = file_match.groups()
            row = rows.setdefault(
                ordinal_token,
                FileRow(ordinal=int(ordinal_token), ordinal_token=ordinal_token, path=""),
            )
            if attr == "path":
                row.path = file_value
            elif attr == "verdict":
                row.verdict = file_value
            else:
                row.reason = file_value
            continue

        if name in fields:
            raise ReceiptParseError(f"receipt name {name!r} appears twice")
        fields[name] = value

    ordered = [rows[token] for token in sorted(rows, key=int)]
    return Receipt(fields=fields, rows=ordered, raw="\n".join(lines[start : end + 1]))


def build_receipt_block(
    fields: Dict[str, object],
    rows: Sequence[Dict[str, object]],
) -> str:
    """Render a grammar-conformant block (test-side fixture text, never production output).

    Used by tests that need a known-good block to compare against — e.g. the
    three-way count agreement C-74 requires. Ordinals are zero-padded to the width
    the row count needs, matching C-33.
    """
    width = max(2, len(str(len(rows))))
    lines = [RECEIPT_BEGIN]
    for name in RECEIPT_SCALAR_FIELDS:
        if name in fields:
            lines.append(f"{name}={fields[name]}")
    for name, value in fields.items():
        if name not in RECEIPT_SCALAR_FIELDS:
            lines.append(f"{name}={value}")
    for index, row in enumerate(rows, start=1):
        token = str(index).zfill(width)
        lines.append(f"file.{token}.path={row['path']}")
        lines.append(f"file.{token}.verdict={row['verdict']}")
        if row.get("reason") is not None:
            lines.append(f"file.{token}.reason={row['reason']}")
    lines.append(RECEIPT_END)
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Script driver result
# --------------------------------------------------------------------------- #


@dataclass
class ScriptRun:
    """One invocation of `git-delta-review.sh` inside the temporary repository."""

    argv: List[str]
    cwd: str
    returncode: int
    stdout: str
    stderr: str

    @property
    def command_line(self) -> str:
        return " ".join(self.argv)

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    # -- receipt access --------------------------------------------------- #

    def receipt(self) -> Optional[Receipt]:
        return parse_receipt(self.stdout)

    def receipt_from_stdout_or_raise(self) -> Receipt:
        parsed = parse_receipt(self.stdout)
        if parsed is None:
            raise ReceiptParseError(
                "no receipt block on stdout; stderr was:\n" + self.stderr
            )
        return parsed

    def describe(self) -> str:
        return (
            f"rc={self.returncode}\n"
            f"cmd={self.command_line}\n"
            f"stdout:\n{self.stdout}\n"
            f"stderr:\n{self.stderr}"
        )


# --------------------------------------------------------------------------- #
# The temporary repository
# --------------------------------------------------------------------------- #


class ReviewGitRepo:
    """A disposable git repository shaped for the code-review contract groups.

    Use as a context manager::

        with ReviewGitRepo(root=tmp_path) as repo:
            shapes = repo.build_standard_history()
            run = repo.run_script("triage", "--base", shapes["code"].base,
                                  "--head", shapes["code"].head)
            assert run.returncode == 0
    """

    FEATURE_KEY = "071-fixture-demo"
    CODE_PATH = "src/fixture_demo.py"
    SPEC_REQUIREMENTS = f".specify/specs/{FEATURE_KEY}/requirements.md"
    SPEC_PLAN = f".specify/specs/{FEATURE_KEY}/plan.md"
    SEED_PATH = "README.md"

    def __init__(
        self,
        root: Optional[Path] = None,
        key: Optional[str] = None,
        script: Optional[Path] = None,
        keep: bool = False,
    ) -> None:
        self._owns_root = root is None
        self._keep = keep
        if root is None:
            # Library-managed temp directory: an enumerated exception to the
            # temp-directory discipline (shared/guidelines/temp-directory-discipline.md §5).
            base = Path(tempfile.mkdtemp(prefix="review-git-repo-"))
            self.root = base
        else:
            self.root = Path(root).resolve()
        self.path = self.root / "repo"
        self.key = key or self.FEATURE_KEY
        self.script = Path(script) if script is not None else REVIEW_SCRIPT_SOURCE
        self._closed = False
        self._isolation_dir: Optional[Path] = None
        self._commits: Dict[str, str] = {}
        # Only write targets are guarded. The script itself is *read* from the
        # framework tree, so it is asserted to be there rather than refused.
        self._guard("root", self.root)
        self._guard("repo", self.path)
        if not str(self.script).startswith(str(FRAMEWORK_ROOT)):
            raise ValueError(
                f"script must live inside the framework tree, got {self.script}"
            )
        self._ensure_isolation_config()

    # -- lifecycle -------------------------------------------------------- #

    def __enter__(self) -> "ReviewGitRepo":
        self.create()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        if self._keep:
            return
        target = self.root if self._owns_root else self.root
        if self._owns_root:
            shutil.rmtree(target, ignore_errors=True)
        else:
            # A caller-supplied root (pytest tmp_path) is removed by pytest; drop
            # only what this harness created inside it.
            shutil.rmtree(self.path, ignore_errors=True)
            if self._isolation_dir is not None:
                shutil.rmtree(self._isolation_dir, ignore_errors=True)

    # -- guards ----------------------------------------------------------- #

    def _guard(self, what: str, path: Path) -> None:
        """Refuse any path that would write the framework repository."""
        resolved = path.resolve()
        framework = FRAMEWORK_ROOT.resolve()
        if resolved == framework or framework in resolved.parents:
            raise ValueError(
                f"refusing to build a throwaway repository at {what}={resolved}: "
                f"it lies inside the framework repository {framework}"
            )

    def _ensure_isolation_config(self) -> None:
        """Point git at empty config files, so host configuration cannot leak in."""
        self._isolation_dir = self.root / "git-config"
        self._isolation_dir.mkdir(parents=True, exist_ok=True)
        for name in ("gitconfig-global", "gitconfig-system"):
            (self._isolation_dir / name).write_text("", encoding="utf-8")

    # -- git plumbing ----------------------------------------------------- #

    def env(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        assert self._isolation_dir is not None
        env["GIT_CONFIG_GLOBAL"] = str(self._isolation_dir / "gitconfig-global")
        env["GIT_CONFIG_SYSTEM"] = str(self._isolation_dir / "gitconfig-system")
        env["GIT_AUTHOR_NAME"] = "Fixture Author"
        env["GIT_AUTHOR_EMAIL"] = "fixture@example.invalid"
        env["GIT_COMMITTER_NAME"] = "Fixture Committer"
        env["GIT_COMMITTER_EMAIL"] = "fixture@example.invalid"
        env["GIT_TERMINAL_PROMPT"] = "0"
        if extra:
            env.update(extra)
        return env

    def git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(self.path),
            env=self.env(),
            capture_output=True,
            text=True,
        )
        if check and completed.returncode != 0:
            raise AssertionError(
                "git " + " ".join(args) + " failed:\n"
                + completed.stdout
                + completed.stderr
            )
        return completed

    def create(self) -> "ReviewGitRepo":
        """Initialise the repository and its local identity; makes no commit."""
        if self.path.exists():
            shutil.rmtree(self.path)
        self.path.mkdir(parents=True)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Fixture Author")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        return self

    def write(self, relative_path: str, content: str) -> Path:
        target = self.path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def commit(self, message: str, paths: Iterable[str]) -> str:
        """Stage exactly ``paths`` and commit; returns the full commit id."""
        path_list = list(paths)
        self.git("add", "--", *path_list)
        self.git("commit", "-q", "-m", message)
        return self.head

    # -- reads ------------------------------------------------------------ #

    @property
    def head(self) -> str:
        return self.git("rev-parse", "HEAD").stdout.strip()

    @property
    def branch(self) -> str:
        return self.git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()

    def short(self, ref: str) -> str:
        return self.git("rev-parse", "--short", ref).stdout.strip()

    def delta_paths(self, base: str, head: str) -> List[str]:
        out = self.git("diff", "--name-only", f"{base}..{head}").stdout
        return [line for line in out.splitlines() if line.strip()]

    def status_short(self) -> List[str]:
        return [line for line in self.git("status", "--short").stdout.splitlines() if line.strip()]

    def is_clean(self) -> bool:
        return self.status_short() == []

    # -- the standard history and its three delta shapes ------------------- #

    def build_standard_history(self) -> Dict[str, "DeltaShape"]:
        """Seed three commits and return the three applicability-predicate shapes.

        commit 1 — ``README.md`` (seed; no spec, no code)
        commit 2 — ``.specify/specs/<key>/requirements.md`` + a code file  -> the spec's
                   first-add commit, which is the feature-first-commit base tier
        commit 3 — ``.specify/specs/<key>/plan.md`` only                    -> spec-only delta
        """
        self.create()

        self.write(self.SEED_PATH, "# Fixture repository\n\nDisposable; never the framework repo.\n")
        seed = self.commit("chore: seed the fixture repository", [self.SEED_PATH])

        self.write(
            f".specify/specs/{self.key}/requirements.md",
            "# Requirements (fixture)\n\n"
            "- **FR-001**: the fixture carries a committed code delta.\n",
        )
        self.write(
            self.CODE_PATH,
            "def demo(value):\n"
            '    """A real code path, so the triage predicate has something to find."""\n'
            "    return value + 1\n",
        )
        feature_commit = self.commit(
            "feat(fixture): add the spec's first artifact and a code file",
            [f".specify/specs/{self.key}/requirements.md", self.CODE_PATH],
        )

        self.write(
            f".specify/specs/{self.key}/plan.md",
            "# Plan (fixture)\n\nNo code path appears in this commit.\n",
        )
        spec_only_commit = self.commit(
            "docs(fixture): add a spec-only artifact",
            [f".specify/specs/{self.key}/plan.md"],
        )

        self._commits = {
            "seed": seed,
            "feature": feature_commit,
            "spec_only": spec_only_commit,
        }

        return {
            "code": DeltaShape(
                name="code",
                base=seed,
                head=feature_commit,
                rationale="the delta adds a code path and a spec artifact",
            ),
            "spec-only": DeltaShape(
                name="spec-only",
                base=feature_commit,
                head=spec_only_commit,
                rationale="the delta adds spec artifacts only, so no code path appears",
            ),
            "empty": DeltaShape(
                name="empty",
                base=spec_only_commit,
                head=spec_only_commit,
                rationale="base and head are the same commit, so the delta has zero files",
            ),
        }

    @property
    def commits(self) -> Dict[str, str]:
        return dict(self._commits)

    @property
    def spec_dir(self) -> Path:
        return self.path / ".specify" / "specs" / self.key

    @property
    def record_path(self) -> Path:
        return self.spec_dir / RECORD_FILENAME

    @property
    def review_dir(self) -> Path:
        return self.path / ".specify" / "review"

    def archives(self) -> List[Path]:
        """Rotated records: ``<spec>/code-review-<YYYYMMDDTHHMMSSZ>.md`` (C-13)."""
        if not self.spec_dir.is_dir():
            return []
        return sorted(self.spec_dir.glob("code-review-*.md"))

    # -- the dirty working-tree hook -------------------------------------- #

    def make_dirty(
        self,
        relative_path: str = "src/uncommitted_work.py",
        content: str = "TOUCHED = True\n",
        stage: bool = False,
        untracked: Optional[str] = None,
    ) -> List[str]:
        """Dirty the working tree; returns the paths the commit range cannot see.

        ``stage=True`` leaves a staged-but-uncommitted modification of a tracked
        file; ``untracked`` writes an untracked file (which ``git diff base..head``
        does not report at all). Used to prove the uncommitted-scope disclosure
        (C-44) is a disclosure and not an absorption of the change.
        """
        dirty: List[str] = []
        self.write(relative_path, content)
        if stage:
            self.git("add", "--", relative_path)
        dirty.append(relative_path)
        if untracked is not None:
            self.write(untracked, "UNTRACKED = True\n")
            dirty.append(untracked)
        return dirty

    def clean_worktree(self) -> None:
        self.git("checkout", "--", ".")
        self.git("clean", "-qfd")

    # -- driving the script ------------------------------------------------ #

    @property
    def missing_delta_bin(self) -> Path:
        """A path that certainly has no renderer — the deterministic text-mode driver."""
        return self.root / ".delta-missing"

    @staticmethod
    def host_delta_bin() -> Optional[str]:
        """The host's renderer, when one exists. Presence says nothing about mode."""
        return shutil.which("delta")

    def run_script(
        self,
        *args: str,
        delta_bin: Optional[object] = None,
        review_dir: Optional[Path] = None,
        extra_env: Optional[Dict[str, str]] = None,
        stdin_text: Optional[str] = None,
        script: Optional[Path] = None,
        timeout: int = 120,
    ) -> ScriptRun:
        """Invoke the review script with an explicit cwd, env, and ``DELTA_BIN``.

        ``delta_bin`` defaults to :attr:`missing_delta_bin` (a non-existent path), so
        the absent-renderer path is the default and the rendered path must be asked
        for explicitly.
        """
        used_script = Path(script) if script is not None else self.script
        self._guard("run-cwd", self.path)
        env_extra = {
            "DELTA_BIN": str(self.missing_delta_bin if delta_bin is None else delta_bin),
            "REVIEW_DIR": str(review_dir or self.review_dir),
        }
        if extra_env:
            env_extra.update(extra_env)
        argv = ["bash", str(used_script), *args]
        completed = subprocess.run(
            argv,
            cwd=str(self.path),
            env=self.env(env_extra),
            capture_output=True,
            text=True,
            input=stdin_text if stdin_text is not None else "",
            timeout=timeout,
        )
        return ScriptRun(
            argv=argv,
            cwd=str(self.path),
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

    # -- record helpers ---------------------------------------------------- #

    def write_record(self, body: str) -> Path:
        """Write ``<spec>/code-review.md`` with ``body`` verbatim (test setup only)."""
        target = self.record_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        return target

    def record_receipt(self) -> Optional[Receipt]:
        if not self.record_path.is_file():
            return None
        return parse_receipt(self.record_path.read_text(encoding="utf-8"))


@dataclass
class DeltaShape:
    """One named slice of history, usable as an explicit ``--base`` / ``--head`` pair."""

    name: str
    base: str
    head: str
    rationale: str = ""
    paths: List[str] = field(default_factory=list)

    def is_empty_by_definition(self) -> bool:
        return self.base == self.head


# --------------------------------------------------------------------------- #
# Self-check (invoked as ``python3 tests/fixtures/review_git_repo.py``)
# --------------------------------------------------------------------------- #

_CHECKS: List[Tuple[str, bool, str]] = []


def _check(label: str, condition: bool, detail: str = "") -> None:
    _CHECKS.append((label, bool(condition), detail))


def self_check() -> int:
    """Round-trip proof: real git, real script invocation, real receipt parsing."""
    with ReviewGitRepo() as repo:
        shapes = repo.build_standard_history()

        # 1. the harness built three commits and a clean tree
        _check("history has three commits", len(repo.commits) == 3, str(repo.commits))
        _check("working tree is clean after building", repo.is_clean(), str(repo.status_short()))

        # 2. the three shapes are shaped as claimed (this is the predicate's input)
        code_paths = repo.delta_paths(shapes["code"].base, shapes["code"].head)
        spec_paths = repo.delta_paths(shapes["spec-only"].base, shapes["spec-only"].head)
        empty_paths = repo.delta_paths(shapes["empty"].base, shapes["empty"].head)
        _check(
            "code shape carries a code path and a spec artifact",
            repo.CODE_PATH in code_paths
            and f".specify/specs/{repo.key}/requirements.md" in code_paths,
            str(code_paths),
        )
        _check(
            "spec-only shape carries spec artifacts and no code path",
            spec_paths == [f".specify/specs/{repo.key}/plan.md"],
            str(spec_paths),
        )
        _check("empty shape has zero changed files", empty_paths == [], str(empty_paths))

        # 3. the real script is drivable with an explicit cwd and refs, no renderer
        stat_run = repo.run_script(
            "diff",
            "--stat",
            "--since",
            shapes["code"].base,
            "--head",
            shapes["code"].head,
        )
        _check(
            "script diff --stat runs with explicit cwd/base/head",
            stat_run.returncode == 0 and repo.CODE_PATH in stat_run.stdout,
            stat_run.describe(),
        )

        # 4. DELTA_BIN is honoured: the default points at a binary that does not exist
        missing_run = repo.run_script(
            "diff", "--since", shapes["code"].base, "--head", shapes["code"].head
        )
        _check(
            "absent DELTA_BIN is refused by the renderer path",
            missing_run.returncode != 0 and "delta" in missing_run.stderr.lower(),
            missing_run.describe(),
        )

        # 5. the receipt grammar round-trips, and its tampered form is detected
        block = build_receipt_block(
            {
                "receipt_version": "1",
                "base": shapes["code"].base,
                "head": shapes["code"].head,
                "base_source": "feature-first-commit",
                "renderer": "text",
                "changed_files": "2",
                "judged_files": "2",
                "skipped_files": "0",
                "gap_files": "0",
                "lines_added": "9",
                "lines_deleted": "0",
            },
            [
                {"path": f".specify/specs/{repo.key}/requirements.md", "verdict": "judged"},
                {"path": repo.CODE_PATH, "verdict": "judged"},
            ],
        )
        parsed = parse_receipt("# Record\n\n" + block + "\n")
        _check("receipt parses to a mapping", parsed is not None and parsed.count("changed_files") == 2)
        _check(
            "per-file rows are ordered, contiguous and sorted",
            parsed is not None
            and parsed.ordinals == [1, 2]
            and parsed.paths == sorted(parsed.paths),
            "" if parsed is None else str(parsed.paths),
        )
        _check(
            "closed name set is recognised as closed",
            parsed is not None and parsed.unknown_names == [] and parsed.counting_identity_holds,
            "" if parsed is None else str(parsed.unknown_names),
        )
        broken = block.replace("judged_files=2", "judged_files=1")
        tampered = parse_receipt(broken)
        _check(
            "a broken counting identity is detected",
            tampered is not None and not tampered.counting_identity_holds,
        )
        _check("an absent block parses to None", parse_receipt("# no block here\n") is None)

        # 6. the dirty hook is visible to git and invisible to the committed range
        dirty_paths = repo.make_dirty(untracked="src/untracked_work.py")
        _check(
            "dirty hook dirties the tree without moving HEAD",
            not repo.is_clean() and len(dirty_paths) == 2,
            str(repo.status_short()),
        )
        _check(
            "the committed range still sees only the committed delta",
            repo.delta_paths(shapes["code"].base, shapes["code"].head) == code_paths,
        )
        repo.clean_worktree()
        _check("clean_worktree restores a clean tree", repo.is_clean(), str(repo.status_short()))

        # 7. the harness refuses to write the framework repository
        refused = False
        try:
            ReviewGitRepo(root=FRAMEWORK_ROOT / "tests" / "fixtures")
        except ValueError:
            refused = True
        _check("a framework-tree root is refused", refused)

    failures = [entry for entry in _CHECKS if not entry[1]]
    for label, ok, detail in _CHECKS:
        print(f"[{'ok' if ok else 'FAIL'}] {label}")
        if not ok and detail:
            print("       " + detail.replace("\n", "\n       "))
    print(f"\n{len(_CHECKS) - len(failures)}/{len(_CHECKS)} self-checks passed")
    if failures:
        print("SELF-CHECK FAILED")
        return 1
    print("SELF-CHECK OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(self_check())
