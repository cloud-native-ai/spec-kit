"""Isolated-HOME bash invocation helpers for the cli-setup unified env-var flow.

These helpers source ``skills/cli-setup/scripts/config-agent.sh`` inside a
subprocess with a controlled ``$HOME`` and a controlled ``AGENT_*`` environment,
run one of the unified-env functions, and capture stdout/stderr/exit code.

The real process environment is NOT inherited (except ``PATH``) so that stray
``AGENT_*`` variables in the developer's shell cannot leak into a test.
"""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "cli-setup" / "scripts" / "config-agent.sh"


@dataclass
class RunResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def combined(self) -> str:
        return self.stdout + self.stderr


def run_config_agent(
    call: str,
    home: Path,
    env: dict[str, str] | None = None,
) -> RunResult:
    """Source config-agent.sh with an isolated ``$HOME`` and run ``call``.

    Parameters
    ----------
    call:
        A bash command line invoking one of the functions, e.g.
        ``"config_agent_env_apply --all"``.
    home:
        Directory to use as ``$HOME`` (config files are written under it).
    env:
        Extra environment variables (typically the ``AGENT_*`` inputs). Only
        ``PATH`` is inherited from the real environment; everything else must be
        supplied here so tests are hermetic.
    """
    proc_env: dict[str, str] = {
        "HOME": str(home),
        "PATH": os.environ.get("PATH", ""),
    }
    if env:
        proc_env.update({k: str(v) for k, v in env.items()})

    script = f'source "{SCRIPT}"\n{call}\n'
    completed = subprocess.run(
        ["bash", "-c", script],
        capture_output=True,
        text=True,
        env=proc_env,
        cwd=str(home),
    )
    return RunResult(
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def valid_env(home: Path, *, with_anthropic: bool = True) -> dict[str, str]:
    """A complete, well-formed set of unified AGENT_* variables for tests."""
    env = {
        "AGENT_API_KEY": "sk-test-SECRET-0123456789",
        "AGENT_MODEL": "glm-5.2",
        "AGENT_BASE_URL": "https://example.test/compatible-mode/v1",
    }
    if with_anthropic:
        env["AGENT_ANTHROPIC_BASE_URL"] = "https://example.test/apps/anthropic"
    return env


# The literal secret embedded in :func:`valid_env` — tests assert it never
# appears in any captured output.
SECRET_VALUE = "sk-test-SECRET-0123456789"
