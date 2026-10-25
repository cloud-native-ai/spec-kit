"""Contract tests for the sdd-loop-driver per-window iteration token.

Hosts such as Qoder reject byte-identical Shell calls as a repeated tool call
(observed 2026-10-25 on a multi-window SSH status poll). A windowed watch
repeats the same command by design, so every window must carry a literal,
incrementing iteration token in the command text. Clauses are local to this
file (no spec-owned clause numbering):

  C-1 watcher accepts --iter and echoes it on WATCH and EVIDENCE
  C-2 the token never changes the verdict or exit code
  C-3 watch-model owns the rule (literal token, increment, re-entry, no runtime expansion)
  C-4 every windowed watch form in dispatch-recipes carries the token; ad-hoc fallback does too
  C-5 SKILL hard requirement and stage-prompts carry the rule
  C-6 watch-hook.sh consumes the token (6th positional arg / WATCH_ITER)
"""

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
WATCH = SKILL_DIR / "scripts" / "watch-target.sh"
HOOK = SKILL_DIR / "scripts" / "watch-hook.sh"
WATCH_MODEL = SKILL_DIR / "references" / "watch-model.md"
RECIPES = SKILL_DIR / "references" / "dispatch-recipes.md"
PROMPTS = SKILL_DIR / "references" / "stage-prompts.md"
SKILL_MD = SKILL_DIR / "SKILL.md"


def _run(args):
    return subprocess.run(args, capture_output=True, text=True, timeout=30)


def _fixture(tmp_path):
    log = tmp_path / "log-stage"
    log.write_text("working\nPLAN-DONE\n", encoding="utf-8")
    status = tmp_path / "status-stage"
    status.write_text("exit=0 at=1 sentinel=1\n", encoding="utf-8")
    return log, status


def _watch_once(log, status, token):
    return _run(
        [
            "bash",
            str(WATCH),
            "--label",
            "iter",
            "--status-file",
            str(status),
            "--log",
            str(log),
            "--sentinel",
            "PLAN-DONE",
            "--once",
            "--iter",
            token,
        ]
    )


# ---------------------------------------------------------------- C-1


def test_c1_watcher_accepts_and_echoes_iter(tmp_path):
    log, status = _fixture(tmp_path)
    proc = _watch_once(log, status, "070-w01")
    assert proc.returncode == 0, proc.stderr
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    watch_line = next(line for line in lines if line.startswith("WATCH "))
    evidence_line = next(line for line in lines if line.startswith("EVIDENCE "))
    assert "iter=070-w01" in watch_line
    assert "iter=070-w01" in evidence_line
    help_text = _run(["bash", str(WATCH), "--help"]).stdout
    assert "--iter TOKEN" in help_text
    assert "byte-identical" in help_text


# ---------------------------------------------------------------- C-2


def test_c2_token_is_verdict_neutral(tmp_path):
    log, status = _fixture(tmp_path)
    first = _watch_once(log, status, "070-w01")
    second = _watch_once(log, status, "070-w02")
    assert first.returncode == 0 and second.returncode == 0
    assert "verdict=DONE" in first.stdout
    assert "verdict=DONE" in second.stdout
    assert first.stdout != second.stdout, (
        "consecutive windows must differ by the iteration token"
    )


# ---------------------------------------------------------------- C-3


def test_c3_watch_model_owns_iteration_rule():
    text = WATCH_MODEL.read_text(encoding="utf-8")
    for needle in (
        "### 3.2",
        "迭代标识",
        "字面量",
        "字节相同",
        "运行时展开",
        "重入续号",
        "POLL_ITER",
    ):
        assert needle in text, f"watch-model iteration rule missing: {needle}"
    section = text[text.index("### 3.2"): text.index("## 4. 机制阶梯")]
    assert "--iter" in section
    assert "MUST NOT" in section
    forbidden = text[text.index("4. **禁止形态**"): text.index("**窗口尺寸**")]
    assert "字节相同" in forbidden, (
        "the forbidden-forms list must name byte-identical monitoring commands"
    )


# ---------------------------------------------------------------- C-4


def test_c4_dispatch_recipes_carry_iter_on_every_window():
    text = RECIPES.read_text(encoding="utf-8")
    blocks = re.findall(r"```bash\n(.*?)```", text, re.S)
    windowed = [block for block in blocks if "watch-target.sh" in block and "--window" in block]
    assert windowed, "no windowed watch command block found in dispatch-recipes"
    missing = [block.splitlines()[0] for block in windowed if "--iter" not in block]
    assert not missing, f"windowed watch block lacks --iter: {missing!r}"
    assert "POLL_ITER" in text, "ad-hoc status-poll fallback must carry a literal token"
    assert "sleep N; ssh" in text, (
        "the prohibited ad-hoc poll shape must be named"
    )


# ---------------------------------------------------------------- C-5


def test_c5_skill_and_prompt_reachability():
    skill = SKILL_MD.read_text(encoding="utf-8")
    match = re.search(r"^9\. \*\*监听签名唯一\*\*(.*)$", skill, re.MULTILINE)
    assert match, "Hard Requirement 9 (监听签名唯一) missing"
    requirement = match.group(1)
    assert "--iter" in requirement
    assert "运行时展开" in requirement or "$(date +%s)" in requirement
    prompts = PROMPTS.read_text(encoding="utf-8")
    assert "--iter" in prompts and "watch-model.md" in prompts


# ---------------------------------------------------------------- C-6


def test_c6_watch_hook_consumes_token(tmp_path):
    proc = _run(
        [
            "bash",
            str(HOOK),
            "impl",
            "1",
            "0",
            str(tmp_path / "missing.fifo"),
            str(tmp_path / "missing.json"),
            "070-w05",
        ]
    )
    assert proc.returncode == 0, proc.stderr
    assert "HOOK_TIMEOUT iter=070-w05" in proc.stdout
    script = HOOK.read_text(encoding="utf-8")
    assert "WATCH_ITER" in script and "${6:-" in script
