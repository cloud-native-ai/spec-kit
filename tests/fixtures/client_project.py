"""Simulated client-project harness for the Feature 072 (client self-improvement)
contract groups.

Owned by: Feature 072, task T003 (`.specify/specs/072-client-self-improvement/tasks.md`).
Consumers (planned): `tests/contract/test_client_capture.py` (T004),
`tests/contract/test_client_armed_state.py` (T009),
`tests/contract/test_client_package_exclusion.py` (T013),
`tests/contract/test_client_improve_loop.py` (T016),
`tests/contract/test_client_metrics.py` (T020).

What it is
----------
A deterministic, stdlib-only builder for a **disposable git repository** wearing
one of two hats — a client project with a minimal installed `.specify/` runtime
and no root-level framework source directories, or its framework-hat twin that
carries the five source directories. Feature 072's whole client channel is
untestable from framework-repository self-tests: the hat predicate takes the
other branch there and the client path never executes (C-58/C-59). This harness
is how the five contract groups execute the client branch for real.

The two hats (predicate owned elsewhere)
----------------------------------------
The hat criterion itself is NOT defined here. The single source of truth is
`.specify/shared/definitions/dogfooding-definitions.md` § 2.1 (root ownership
of `templates` / `skills` / `shared` / `scripts` / `src/specify_cli`), and
Feature 072's C-1 adds that a `feedback/` directory MUST NOT participate in the
judgement. This module only *materialises* both sides of that predicate so a
contract test can prove it in both directions (a predicate that can only be
driven one way proves nothing):

- ``make_client_project(root)``     -> ``project.hat == "client"``
- ``make_framework_hat_twin(root)`` -> ``project.hat == "framework"``

A predicate that can only be driven in one direction proves nothing, so a
client fixture also carries a root-level ``feedback/`` directory in its
self-check: per C-1 the verdict must stay ``client``.

The minimal installed runtime
-----------------------------
The fixture copies, per construction from the live framework tree (a throwaway
never goes stale — it is rebuilt from the current source on every build):

- ``.specify/shared/definitions/probe-definitions.md`` — the probe truth source,
  so ``probe-utils.py --action probes`` reports the registry available;
- ``.specify/scripts/`` — the real engine mirror (what ``specify init`` lays
  down), installed where the engines' self-location rule anchors the fixture
  root exactly as in a real client project (a literal ``.specify`` component
  in the invoked script's resolved path, per dogfooding-definitions § 2.1
  item 4). The whole mirror — not just the four Feature 072 engines — because
  the probe registry's non-entity catalog references engine script paths that
  registry validation requires reachable from the workspace root;
- ``.specify/memory/feedback/`` — the per-entry feedback store directory.

Tests may invoke the installed copy (``project.engine_path(name)``, exercising
the real self-location path) or the framework copy by absolute path
(``ClientProject.framework_engine_path(name)`` with ``--workspace-root
<repo>``) — both forms are available so the same assertion can pin the runtime
topology and bypass it deterministically.

Two rules this module holds itself to
-------------------------------------
1. **It never writes the framework repository.** Every repository it builds lives
   under a caller-supplied root (pytest ``tmp_path``) or a library-managed
   ``tempfile.mkdtemp()``, and construction refuses a root that resolves inside
   the framework source tree. The process working directory is never changed:
   every git and engine invocation receives an explicit ``cwd``.
2. **The hat predicate is read-only and engine facts come from the probe
   engine's machine-readable output** (C-9): ``external_probe_count()`` and
   ``probe_registry_available()`` parse `probe-utils.py --action probes
   --format json`; nothing here keeps a hand-maintained probe list.

Run the module directly for its own round-trip self-check:

    python3 tests/fixtures/client_project.py
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

# --------------------------------------------------------------------------- #
# Framework locations (read-only; nothing here is ever written)
# --------------------------------------------------------------------------- #

FRAMEWORK_ROOT = Path(__file__).resolve().parents[2]

#: The five framework source directories that decide the hat
#: (owner: `.specify/shared/definitions/dogfooding-definitions.md` § 2.1;
#: C-1 of contracts/client-identity-and-armed-state.md — cited, never redefined).
FRAMEWORK_SOURCE_DIRS: tuple = ("templates", "skills", "shared", "scripts", "src/specify_cli")

#: Engines a minimal client runtime needs for Feature 072's five behavior groups
#: (all stdlib-only single-module scripts). The whole `.specify/scripts/` mirror
#: is installed — the probe-definitions non-entity catalog references engine
#: script paths that registry validation requires reachable from the root.
ENGINE_NAMES: tuple = (
    "feedback-utils.py",
    "probe-utils.py",
    "run-determination.py",
    "evidence-utils.py",
)

#: The installed scripts mirror copied into the fixture (what `specify init`
#: lays down; also where the engines used by the five behavior groups live).
FRAMEWORK_SCRIPTS_MIRROR = FRAMEWORK_ROOT / ".specify" / "scripts"

#: The probe truth source installed into the fixture runtime.
PROBE_DEFS_SOURCE = FRAMEWORK_ROOT / ".specify" / "shared" / "definitions" / "probe-definitions.md"

HAT_CLIENT = "client"
HAT_FRAMEWORK = "framework"


# --------------------------------------------------------------------------- #
# Hat predicate (owner elsewhere — this module only applies it)
# --------------------------------------------------------------------------- #


def hat_of(root: Path) -> str:
    """Apply the two-hats owner criterion: root ownership of any one of the five
    framework source directories means the framework hat; otherwise client.

    A root-level ``feedback/`` directory is deliberately NOT consulted
    (contracts/client-identity-and-armed-state.md C-1)."""
    root = Path(root).resolve()
    if any((root / name).is_dir() for name in FRAMEWORK_SOURCE_DIRS):
        return HAT_FRAMEWORK
    return HAT_CLIENT


def is_framework_hat(root: Path) -> bool:
    return hat_of(root) == HAT_FRAMEWORK


def is_client_hat(root: Path) -> bool:
    return hat_of(root) == HAT_CLIENT


# --------------------------------------------------------------------------- #
# Engine invocation result
# --------------------------------------------------------------------------- #


@dataclass
class EngineRun:
    """One invocation of an engine script against the fixture repository."""

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

    def json_stdout(self) -> Dict:
        """Parse stdout as the engine's machine-readable JSON payload."""
        return json.loads(self.stdout)

    def describe(self) -> str:
        return (
            f"rc={self.returncode}\n"
            f"cmd={self.command_line}\n"
            f"stdout:\n{self.stdout}\n"
            f"stderr:\n{self.stderr}"
        )


# --------------------------------------------------------------------------- #
# The simulated client project
# --------------------------------------------------------------------------- #


class ClientProject:
    """A disposable git repository wearing the client hat (default) or the
    framework hat (its twin), with a minimal installed `.specify/` runtime.

    Use as a context manager::

        with make_client_project(tmp_path) as project:
            assert project.hat == "client"
            project.arm("custom:fixture/unit")
            assert project.external_probe_count() == 1
    """

    DEFAULT_UNIT = "custom:fixture/unit"

    def __init__(
        self,
        root: Optional[Path] = None,
        hat: str = HAT_CLIENT,
        keep: bool = False,
    ) -> None:
        if hat not in (HAT_CLIENT, HAT_FRAMEWORK):
            raise ValueError(f"hat must be 'client' or 'framework', got {hat!r}")
        self._owns_root = root is None
        self._keep = keep
        self._hat_role = hat
        if root is None:
            # Library-managed temp directory: an enumerated exception to the
            # temp-directory discipline (shared/guidelines/temp-directory-discipline.md §5).
            base = Path(tempfile.mkdtemp(prefix="client-project-"))
            self.root = base
        else:
            self.root = Path(root).resolve()
        self.path = self.root / "repo"
        self._closed = False
        self._isolation_dir: Optional[Path] = None
        self._guard("root", self.root)
        self._guard("repo", self.path)
        self._ensure_isolation_config()

    # -- factories' shared entry ------------------------------------------ #

    def create(self) -> "ClientProject":
        """Initialise the git repository and install the minimal `.specify/` runtime."""
        if self.path.exists():
            shutil.rmtree(self.path)
        self.path.mkdir(parents=True)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Fixture Author")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")

        # The feedback store directory exists from install time (Feature 072
        # armed-state and capture behaviors assume the store is present).
        self.feedback_dir.mkdir(parents=True, exist_ok=True)

        # Probe definitions in place -> the probe registry is "available".
        defs_target = self.path / ".specify" / "shared" / "definitions"
        defs_target.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PROBE_DEFS_SOURCE, defs_target / "probe-definitions.md")

        # The real engines, installed where their self-location rule anchors
        # this repository (a literal `.specify` component in the resolved
        # script path, dogfooding-definitions § 2.1 item 4). The whole scripts
        # mirror is installed — the probe registry's non-entity catalog points
        # at engine script paths that validation requires reachable.
        shutil.copytree(
            FRAMEWORK_SCRIPTS_MIRROR,
            self.path / ".specify" / "scripts",
        )

        if self._hat_role == HAT_FRAMEWORK:
            for name in FRAMEWORK_SOURCE_DIRS:
                marker = self.path / name
                marker.mkdir(parents=True, exist_ok=True)
                (marker / ".hat-marker").write_text(
                    f"framework source marker for the {name} hat directory\n",
                    encoding="utf-8",
                )
        return self

    # -- lifecycle --------------------------------------------------------- #

    def __enter__(self) -> "ClientProject":
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
        shutil.rmtree(self.path, ignore_errors=True)
        if self._owns_root:
            shutil.rmtree(self.root, ignore_errors=True)
        elif self._isolation_dir is not None:
            shutil.rmtree(self._isolation_dir, ignore_errors=True)

    # -- guards ------------------------------------------------------------ #

    def _guard(self, what: str, path: Path) -> None:
        """Refuse any path that would write the framework repository."""
        resolved = path.resolve()
        framework = FRAMEWORK_ROOT.resolve()
        if resolved == framework or framework in resolved.parents:
            raise ValueError(
                f"refusing to build a simulated client project at {what}={resolved}: "
                f"it lies inside the framework repository {framework}"
            )

    def _ensure_isolation_config(self) -> None:
        """Point git at empty config files, so host configuration cannot leak in."""
        self._isolation_dir = self.root / "git-config"
        self._isolation_dir.mkdir(parents=True, exist_ok=True)
        for name in ("gitconfig-global", "gitconfig-system"):
            (self._isolation_dir / name).write_text("", encoding="utf-8")

    # -- hat --------------------------------------------------------------- #

    @property
    def hat(self) -> str:
        """The hat verdict applied by the owner criterion to this repository."""
        return hat_of(self.path)

    @property
    def framework_source_dirs_present(self) -> List[str]:
        return [name for name in FRAMEWORK_SOURCE_DIRS if (self.path / name).is_dir()]

    # -- git plumbing ------------------------------------------------------- #

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

    def write(self, relative_path: str, content: str) -> Path:
        target = self.path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def commit(self, message: str, paths: List[str]) -> str:
        self.git("add", "--", *paths)
        self.git("commit", "-q", "-m", message)
        return self.head

    @property
    def head(self) -> str:
        return self.git("rev-parse", "HEAD").stdout.strip()

    def status_short(self) -> List[str]:
        return [line for line in self.git("status", "--short").stdout.splitlines() if line.strip()]

    def is_clean(self) -> bool:
        return self.status_short() == []

    # -- engine locations --------------------------------------------------- #

    def engine_path(self, name: str) -> Path:
        """The engine installed inside this fixture's `.specify/` runtime."""
        return self.path / ".specify" / "scripts" / "python" / name

    @staticmethod
    def framework_engine_path(name: str) -> Path:
        """The framework copy of an engine, invocable by absolute path with
        ``--workspace-root <repo>`` to bypass self-location."""
        return FRAMEWORK_ROOT / ".specify" / "scripts" / "python" / name

    @property
    def feedback_dir(self) -> Path:
        return self.path / ".specify" / "memory" / "feedback"

    @property
    def probes_dir(self) -> Path:
        return self.feedback_dir / "probes"

    # -- driving engines ---------------------------------------------------- #

    def run_engine(
        self,
        name: str,
        *args: str,
        installed: bool = True,
        extra_env: Optional[Dict[str, str]] = None,
        timeout: int = 120,
    ) -> EngineRun:
        """Invoke an engine against this repository.

        ``installed=True`` (default) runs the copy installed inside the
        fixture's `.specify/` runtime — the real client topology where the
        engine self-locates the fixture root. ``installed=False`` runs the
        framework copy by absolute path; pass ``--workspace-root`` in ``args``
        to aim it at this repository.
        """
        script = self.engine_path(name) if installed else self.framework_engine_path(name)
        self._guard("engine-cwd", self.path)
        argv = ["python3", str(script), *args]
        completed = subprocess.run(
            argv,
            cwd=str(self.path),
            env=self.env(extra_env),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return EngineRun(
            argv=argv,
            cwd=str(self.path),
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

    # -- probe registry facts (machine-readable output only, C-9) ----------- #

    def probe_registry_json(self, installed: bool = True) -> Dict:
        run = self.run_engine("probe-utils.py", "--action", "probes", "--format", "json",
                              installed=installed)
        if not run.ok:
            raise AssertionError("probe registry read failed:\n" + run.describe())
        return run.json_stdout()

    def probe_registry_available(self, installed: bool = True) -> bool:
        return bool(self.probe_registry_json(installed=installed).get("available"))

    def external_probe_count(self, installed: bool = True) -> int:
        # The plain `probes` payload exposes merged objects, not an
        # external_objects count (the registry output face stays untouched,
        # DoD-4) — derive the count from the ext- object_id prefix (C-9).
        payload = self.probe_registry_json(installed=installed)
        return len(self._external_objects(payload))

    def external_probe_units(self, installed: bool = True) -> List[str]:
        payload = self.probe_registry_json(installed=installed)
        return sorted(
            str(obj.get("unit", "")) for obj in self._external_objects(payload)
        )

    @staticmethod
    def _external_objects(payload: Dict) -> List[Dict]:
        return [
            obj for obj in payload.get("objects", [])
            if str(obj.get("object_id", "")).startswith("ext-")
        ]

    # -- armed-state material ------------------------------------------------ #

    def arm(self, unit: str = DEFAULT_UNIT) -> Dict:
        """Inject the external probe object for ``unit`` — the preparation step
        that makes the client channel armed (C-3 makes the probe object a
        necessary condition; the guidance for unarmed states names this action)."""
        run = self.run_engine(
            "probe-utils.py", "--action", "probe-inject", "--unit", unit,
            "--workspace-root", str(self.path),
        )
        if not run.ok:
            raise AssertionError(f"probe injection failed for {unit!r}:\n" + run.describe())
        return run.json_stdout()

    def disarm_all(self) -> None:
        """Remove every external probe object (back to the unarmed state)."""
        if self.probes_dir.is_dir():
            shutil.rmtree(self.probes_dir)

    def break_probe_registry(self) -> None:
        """Simulate an un-upgraded `.specify/` runtime: registry unavailable (C-4)."""
        target = self.path / ".specify" / "shared" / "definitions" / "probe-definitions.md"
        if target.exists():
            target.unlink()

    # -- feedback store facts ------------------------------------------------- #

    def feedback_list_json(self, kind: str = "external") -> Dict:
        run = self.run_engine(
            "feedback-utils.py", "--action", "list", "--kind", kind, "--format", "json",
            "--workspace-root", str(self.path),
        )
        if not run.ok:
            raise AssertionError(f"feedback list failed for kind={kind!r}:\n" + run.describe())
        return run.json_stdout()


# --------------------------------------------------------------------------- #
# Factories
# --------------------------------------------------------------------------- #


def make_client_project(root: Optional[Path] = None, keep: bool = False) -> ClientProject:
    """A disposable git repository with a minimal installed `.specify/` runtime
    and **no** root-level framework source directories (``hat == "client"``)."""
    return ClientProject(root=root, hat=HAT_CLIENT, keep=keep)


def make_framework_hat_twin(root: Optional[Path] = None, keep: bool = False) -> ClientProject:
    """The twin: same runtime, but the five framework source directories are
    present at the root (``hat == "framework"``) — the branch framework
    self-testing takes, used to prove the client channel stays silent there."""
    return ClientProject(root=root, hat=HAT_FRAMEWORK, keep=keep)


# --------------------------------------------------------------------------- #
# Self-check (invoked as ``python3 tests/fixtures/client_project.py``)
# --------------------------------------------------------------------------- #

_CHECKS: List = []


def _check(label: str, condition: bool, detail: str = "") -> None:
    _CHECKS.append((label, bool(condition), detail))


def self_check() -> int:
    """Round-trip proof: real git, real engines, both hat directions, real probes."""
    # 1. client fixture: hat, runtime, engine self-location
    with make_client_project() as project:
        _check("client fixture builds three commits of runtime", True,
               str(sorted(p.relative_to(project.path).as_posix()
                          for p in project.path.rglob("*") if p.is_file()))[:200])

        _check("client hat verdict", project.hat == HAT_CLIENT, project.hat)
        _check(
            "no framework source directory at client root",
            project.framework_source_dirs_present == [],
            str(project.framework_source_dirs_present),
        )
        _check("feedback store directory exists", project.feedback_dir.is_dir())

        # C-1 negative proof: a root-level feedback/ directory must not move the hat.
        (project.path / "feedback").mkdir(exist_ok=True)
        _check("feedback/ does not participate in the hat judgement (C-1)",
               project.hat == HAT_CLIENT, project.hat)

        # Probe registry available, zero external probes (T003 test anchor).
        _check("probe registry available in fixture",
               project.probe_registry_available(), "")
        _check("external probe count is zero before arming",
               project.external_probe_count() == 0,
               str(project.probe_registry_json()))

        # Engine self-location: the installed copy anchors the fixture root
        # even without --workspace-root (real client topology).
        run = project.run_engine("probe-utils.py", "--action", "probes", "--format", "json")
        _check("installed engine self-locates the fixture root",
               run.ok and run.json_stdout().get("available") is True, run.describe())

        # Framework copy by absolute path + --workspace-root agrees (C-9 shape).
        fw_run = project.run_engine("probe-utils.py", "--action", "probes", "--format", "json",
                                    "--workspace-root", str(project.path), installed=False)
        _check("framework engine by absolute path agrees on external count",
               fw_run.ok and len(ClientProject._external_objects(fw_run.json_stdout())) == 0,
               fw_run.describe())

        # Arm -> one external probe; second unit -> two (ambiguous material).
        project.arm(project.DEFAULT_UNIT)
        _check("arming injects exactly one external probe",
               project.external_probe_count() == 1
               and project.external_probe_units() == [project.DEFAULT_UNIT],
               str(project.external_probe_units()))
        project.arm("custom:fixture/other")
        _check("second probe raises external count to two",
               project.external_probe_count() == 2, str(project.external_probe_units()))
        project.disarm_all()
        _check("disarm_all returns to zero external probes",
               project.external_probe_count() == 0, "")

        # Broken registry -> unavailable (C-4 material).
        project.break_probe_registry()
        _check("broken registry reads as unavailable (C-4 material)",
               not project.probe_registry_available(), "")

        # Feedback engine reaches the fixture store.
        listing = project.feedback_list_json(kind="external")
        _check("feedback engine lists the fixture store",
               int(listing.get("count", -1)) == 0, str(listing))

        _check("fixture keeps the framework tree clean",
               not FRAMEWORK_ROOT.joinpath(".specify", "memory", "feedback", "probes",
                                           "ext-fixture-unit.md").exists(), "")

        # 7. the harness refuses to write the framework repository
        refused = False
        try:
            ClientProject(root=FRAMEWORK_ROOT / "tests" / "fixtures")
        except ValueError:
            refused = True
        _check("a framework-tree root is refused", refused)

    # 2. framework-hat twin: same runtime, opposite verdict (bidirectional proof)
    with make_framework_hat_twin() as twin:
        _check("framework-hat twin verdict", twin.hat == HAT_FRAMEWORK, twin.hat)
        _check(
            "all five framework source directories present at twin root",
            twin.framework_source_dirs_present == list(FRAMEWORK_SOURCE_DIRS),
            str(twin.framework_source_dirs_present),
        )
        _check("twin runtime also has probe registry available",
               twin.probe_registry_available(), "")
        _check("twin external probe count is zero",
               twin.external_probe_count() == 0, "")
        _check("twin feedback store exists", twin.feedback_dir.is_dir())

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
