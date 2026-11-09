"""Carrier contract for the three SDD-driving external skills (re-pinned by Feature 093, T152).

The ruling (FR-035 / C-094) fixes two legal carriers and one ban:

- **Fork carrier (same-family default)** — each concurrent unit is a separate ``qodercli``
  child process launched through ``skills/external/sdd-loop-driver/scripts/stage-runner.sh``.
- **Subprocess carrier (heterogeneous agents)** — an independent child process of the
  agent's own CLI when that CLI is a different family than ``qodercli``.
- **Banned** — the host-internal in-process subagent path is not a concurrency carrier
  (neither a default nor a degradation option).

Rule 2 is unchanged: a complete remote triple travels ssh (su) + cd + the subagent CLI.
Every assertion that pinned the old "MUST NOT launch qodercli locally" /
"host-native first" rule is replaced below by the carriers plus the ban, and the old
phrases are asserted *absent* so the synchronous-local-native rule cannot return silently.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOPOLOGY = ROOT / "shared" / "workflow" / "execution-topology.md"
DISPATCH = ROOT / "shared" / "workflow" / "external-dispatch-recipes.md"
DEFAULTS = ROOT / "templates" / "execution-config-defaults.yaml"
SETUP = ROOT / "skills" / "external" / "sdd-project-setup" / "SKILL.md"
SETUP_RECIPES = ROOT / "skills" / "external" / "sdd-project-setup" / "references" / "setup-recipes.md"
HOUSE = ROOT / "skills" / "external" / "sdd-house-keeping" / "SKILL.md"
HOUSE_RECIPES = ROOT / "skills" / "external" / "sdd-house-keeping" / "references" / "maintenance-recipes.md"
LOOP = ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
LOOP_RECIPES = ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "dispatch-recipes.md"
PREFLIGHT = ROOT / "skills" / "internal" / "run-agent" / "references" / "dispatch-preflight.md"

#: The disposed old rule (FR-033 disposal list); none may return.
OLD_RULE_PHRASES = (
    "MUST NOT launch `qodercli` locally",
    "MUST NOT launch qodercli",
    "MUST NOT 启动 `qodercli`",
    "MUST NOT 启动 qodercli",
    "MUST NOT 以 `qodercli` 作为 SDD 缺省子代理",
    "MUST NOT 以 qodercli 作为 SDD 缺省子代理",
    "not the SDD local default",
    "host-native subagent capability first",
)

BAN_WINDOW = re.compile(
    r"in-process[\s\S]{0,240}(BANNED|禁止|MUST NOT|not counted|不被计为|不计为)"
    r"|(BANNED|禁止|MUST NOT|not counted|不被计为|不计为)[\s\S]{0,240}in-process")


def _read(path: Path) -> str:
    assert path.is_file(), f"missing: {path}"
    return path.read_text(encoding="utf-8")


def _assert_two_carriers(text: str, where: str):
    assert "qodercli" in text, f"{where}: the fork carrier names qodercli"
    assert "stage-runner.sh" in text, f"{where}: the fork carrier runs through stage-runner.sh"
    assert re.search(r"子进程|child process|child-process", text), (
        f"{where}: a carrier is an independent child process")
    assert re.search(r"SUBPROCESS|subprocess|独立子进程", text), (
        f"{where}: the subprocess carrier must be named")
    assert re.search(r"heterogeneous|异构", text), (
        f"{where}: the subprocess carrier serves heterogeneous agents")


def _assert_in_process_banned(text: str, where: str):
    assert "in-process" in text, f"{where}: the banned path must be named"
    assert BAN_WINDOW.search(text), (
        f"{where}: the host-internal in-process path must be BANNED as a carrier")


def _assert_old_rule_gone(text: str, where: str):
    for phrase in OLD_RULE_PHRASES:
        assert phrase not in text, (
            f"{where}: the disposed old rule returned: {phrase!r}")


# --------------------------------------------------------------------------- #
def test_shared_carrier_owner_has_both_rules():
    text = _read(TOPOLOGY)
    assert "## Carrier decision (local vs remote)" in text
    assert "No remote information" in text and "local" in text
    assert "current project" in text or "current working directory" in text
    _assert_two_carriers(text, "execution-topology.md")
    _assert_in_process_banned(text, "execution-topology.md")
    assert "Complete remote triple" in text
    assert "ssh <alias>" in text and "su - <run-user>" in text
    assert "cd <project-dir>" in text
    assert "cli: qodercli" in text
    _assert_old_rule_gone(text, "execution-topology.md")


def test_execution_config_default_is_qodercli():
    text = _read(DEFAULTS)
    assert "cli: qodercli" in text


def test_sdd_skills_reference_the_carrier_owner():
    for path in (SETUP, HOUSE, LOOP):
        assert "execution-topology.md" in _read(path), (
            f"{path.name} must reference the carrier owner")


def test_setup_local_and_remote_shapes():
    text = _read(SETUP) + _read(SETUP_RECIPES)
    assert "当前项目" in text
    assert "ssh <alias>" in text and "su - <run-user>" in text
    assert "cd <project-dir>" in text
    _assert_two_carriers(text, "sdd-project-setup")
    _assert_in_process_banned(text, "sdd-project-setup")
    _assert_old_rule_gone(text, "sdd-project-setup")


def test_house_keeping_local_and_remote_shapes():
    text = _read(HOUSE) + _read(HOUSE_RECIPES)
    assert "当前项目" in text
    assert "ssh <alias>" in text and "su - <run-user>" in text
    assert "cd <project-dir>" in text
    _assert_two_carriers(text, "sdd-house-keeping")
    _assert_in_process_banned(text, "sdd-house-keeping")
    _assert_old_rule_gone(text, "sdd-house-keeping")
    # H4 hook-health must be run on the target side, not against a remote path locally
    assert "hook-health.py" in text
    assert "ssh <alias>" in text


def test_loop_driver_local_carriers_and_remote_cli():
    text = _read(LOOP) + _read(LOOP_RECIPES)
    assert "会话 cwd" in text
    assert "向上搜索" in text
    # the fork carrier replaces the old local-native default; qodercli is now the local
    # same-family carrier, not a remote-only tool
    _assert_two_carriers(text, "sdd-loop-driver")
    _assert_in_process_banned(text, "sdd-loop-driver")
    assert "ssh <alias>" in text and "su - <run-user>" in text
    _assert_old_rule_gone(text, "sdd-loop-driver")
    preflight = _read(PREFLIGHT)
    assert "su - <run-user>" in preflight and "cd <project-dir>" in preflight


def test_shared_dispatch_doc_declares_the_two_carriers_and_the_ban():
    text = _read(DISPATCH)
    assert "SDD-driving skills boundary" in text
    _assert_two_carriers(text, "external-dispatch-recipes.md")
    _assert_in_process_banned(text, "external-dispatch-recipes.md")
    _assert_old_rule_gone(text, "external-dispatch-recipes.md")
