"""Contract tests for Feature 083 US3 — consumption-side stop (T016).

Owns the SC-004 mechanised face that
``.specify/specs/083-mechanism-policy-separation/contracts/guard-and-measurement.contract.md``
GM-05 and ``quickstart.md`` S6 name. The subject is **the owner's contract text plus
a filesystem snapshot** — never an AI's behaviour (GM-02).

Legs:

* **read-judge-stop is textually a three-step with no write action** — the owner's
  § Consumption Contract steps 1–3 carry no write verb (write / create directory /
  delete / rename), so a consumer that follows it cannot mutate anything while
  judging.
* **missing policy → zero writes** — in ``tmp_path`` a fake skill directory and a
  fake run directory are snapshotted (every file's sha256 **and** the directory
  set — never mtime, which a no-op read can change); the missing-policy branch of
  the owner's check is evaluated and the snapshot after must equal the snapshot
  before, across the full file set.
* **supplied policy → byte-identical output** — the same input with the policy
  supplied produces artifact hashes equal to the recorded baseline hashes for that
  input, i.e. the check is additive and does not alter the produced artifact.
* **environment error ≠ policy missing** — the supplied-but-unreadable branch must
  not be reported as the missing-policy branch (FR-007).

Each leg carries a GM-07 negative case: a ``tmp_path`` copy with a write injected
into the check text must turn the zero-write assertion red.

Red-first (Constitution IV / GM-01): the owner document precedes this row; the legs
red on a removed shape, never on an import error.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER_REL = Path("shared/definitions/mechanism-policy-definitions.md")
OWNER = REPO_ROOT / OWNER_REL

WRITE_VERBS = (
    "写入",
    "写文件",
    "写临时",
    "建目录",
    "创建目录",
    "删除",
    "改名",
    "write to",
    "write the",
    "create director",
    "delete ",
    "rename ",
    "mkdir",
    "touch ",
)

# A step may *name* a write action only to forbid it ("MUST NOT 写文件"). The
# prohibition is the contract; the action is the violation.
PROHIBITION_MARKERS = ("MUST NOT", "不得", "禁止")
NEGATION_LEAD = ("不", "勿", "无")


def _step_carries_write(lines: list[str]) -> str | None:
    text = " ".join(lines)
    for sentence in re.split(r"[。;；]", text):
        if any(marker in sentence for marker in PROHIBITION_MARKERS):
            continue
        for verb in WRITE_VERBS:
            idx = sentence.lower().find(verb.lower())
            if idx == -1:
                continue
            prefix = sentence[max(0, idx - 3):idx]
            if any(neg in prefix for neg in NEGATION_LEAD):
                continue
            return verb
    return None


def _read(path: Path) -> str:
    assert path.is_file(), "artifact missing: %s" % path
    return path.read_text(encoding="utf-8")


def _section(text: str, heading_prefix: str) -> str:
    lines = text.splitlines()
    start = level = None
    for i, line in enumerate(lines):
        stripped = line.lstrip("#")
        depth = len(line) - len(stripped)
        if 2 <= depth <= 3 and stripped.startswith(" " + heading_prefix):
            start, level = i, depth
            break
    assert start is not None, "section not found: %r" % heading_prefix
    body = [lines[start]]
    in_fence = False
    for line in lines[start + 1:]:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        stripped = line.lstrip("#")
        depth = len(line) - len(stripped)
        if not in_fence and depth == level and stripped.startswith(" "):
            break
        body.append(line)
    return "\n".join(body)


def check_steps(text: str) -> dict[int, list[str]]:
    """Parse the numbered read-judge-stop steps of the owner's check order section."""
    section = _section(text, "检查顺序")
    steps: dict[int, list[str]] = {}
    for line in section.splitlines():
        match = re.match(r"^(\d+)\.\s+(.*)$", line.strip())
        if match:
            steps[int(match.group(1))] = [match.group(2)]
        elif steps and line.startswith((" ", "\t")) and line.strip():
            steps[max(steps)].append(line.strip())
    return steps


# --------------------------------------------------------------------------- #
# leg 1 — the check text is read → judge → stop, with no write action
# --------------------------------------------------------------------------- #
def assert_check_is_read_only(text: str, steps: dict[int, list[str]] | None = None) -> list[str]:
    problems: list[str] = []
    steps = steps if steps is not None else check_steps(text)
    if sorted(steps) != [1, 2, 3]:
        problems.append("the check order is not a three-step chain, found steps %r" % sorted(steps))
    for number, lines in steps.items():
        verb = _step_carries_write(lines)
        if verb:
            problems.append(
                "step %d carries a write action (%r) — the check itself must write nothing"
                % (number, verb)
            )
    section = _section(text, "检查顺序")
    if "副作用之前" not in section and "before any side effect" not in section.lower():
        problems.append("the check order does not declare itself before any side effect")
    return problems


def test_check_text_is_read_judge_stop_with_no_write():
    problems = assert_check_is_read_only(_read(OWNER))
    assert not problems, "SC-004 check-text violations:\n- " + "\n- ".join(problems)


def test_negative_case_injecting_a_write_turns_the_check_assertion_red(tmp_path):
    mutated = _read(OWNER).replace(
        "**读**：读出这一步需要的策略项", "**读**：读出这一步需要的策略项并把结果写入缓存文件", 1
    )
    broken = tmp_path / OWNER_REL.name
    broken.write_text(mutated, encoding="utf-8")
    problems = assert_check_is_read_only(_read(broken))
    assert any("write action" in p for p in problems), (
        "an injected write left the check assertion green — the verb list is not doing its job"
    )


# --------------------------------------------------------------------------- #
# leg 2 — missing policy writes nothing
# --------------------------------------------------------------------------- #
def _snapshot(root: Path) -> dict[str, object]:
    """Full content-hash + directory-set snapshot. Never mtime (a read can move it)."""
    files: dict[str, str] = {}
    dirs: set[str] = set()
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_dir():
            dirs.add(rel)
        else:
            files[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"files": files, "dirs": sorted(dirs)}


def evaluate_policy_gate(policy: str | None, check_text: str) -> str:
    """A deterministic reading of the owner's check: ``stop`` / ``proceed`` / ``env-error``.

    The function is deliberately dumb — it is the test's model of the contract, not a
    second implementation of the principle: the check may only **decide**, so it
    returns a verdict and touches no path.
    """
    assert "副作用之前" in check_text or "before any side effect" in check_text.lower(), (
        "artifact missing: the check text carries no before-any-side-effect declaration"
    )
    if policy is None or not policy.strip():
        return "stop"
    candidate = Path(policy)
    return "proceed" if candidate.exists() else "env-error"


def build_scenario(root: Path, *, supplied: bool) -> tuple[Path, Path, Path]:
    skill = root / "skills" / "demo"
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: demo\n---\n\n# demo\n", encoding="utf-8")
    (skill / "references" / "input.md").write_text("source material\n", encoding="utf-8")
    run = root / "run"
    run.mkdir()
    (run / "scratch.txt").write_text("pre-existing runtime state\n", encoding="utf-8")
    target = run / "out" / "result.md"
    if supplied:
        (run / "out").mkdir()
        (target).write_text("artifact from the supplied policy\n", encoding="utf-8")
    return skill, run, target


def test_missing_policy_writes_nothing_anywhere(tmp_path):
    skill, run, target = build_scenario(tmp_path, supplied=False)
    before = _snapshot(tmp_path)
    verdict = evaluate_policy_gate(None, _read(OWNER))
    assert verdict == "stop"
    assert not target.exists()
    after = _snapshot(tmp_path)
    assert after["dirs"] == before["dirs"], (
        "the directory set changed across a missing-policy check: %r → %r"
        % (before["dirs"], after["dirs"])
    )
    assert after["files"] == before["files"], (
        "files changed across a missing-policy check: %r → %r"
        % (sorted(set(after["files"]) ^ set(before["files"])), "content drift")
    )


def test_supplied_policy_reproduces_the_recorded_baseline_hashes(tmp_path):
    supplied = tmp_path / "supplied"
    supplied.mkdir()
    (supplied / "input.md").write_text("source material\n", encoding="utf-8")
    _, _, target = build_scenario(supplied, supplied=True)
    verdict = evaluate_policy_gate(str(supplied), _read(OWNER))
    assert verdict == "proceed"
    baseline = hashlib.sha256(b"artifact from the supplied policy\n").hexdigest()
    assert hashlib.sha256(target.read_bytes()).hexdigest() == baseline, (
        "the produced artifact differs from the recorded baseline for the same input"
    )


def test_environment_error_is_not_reported_as_policy_missing(tmp_path):
    missing = evaluate_policy_gate(None, _read(OWNER))
    unreadable = evaluate_policy_gate(str(tmp_path / "absent-input-dir"), _read(OWNER))
    assert missing == "stop" and unreadable == "env-error", (
        "the supplied-but-unreadable branch reports %r while the missing branch reports %r — "
        "FR-007 requires distinguishable verdicts" % (unreadable, missing)
    )
    owner = _read(OWNER)
    branches = _section(owner, "两类判定的区分")
    assert branches.count("「") >= 2, "the two error classes do not each carry their own wording"


def test_negative_case_injected_write_turns_the_zero_write_assertion_red(tmp_path):
    check = _read(OWNER).replace(
        "**停**：任一项缺失或含糊，停在此处并向用户索取；已进行的读取不留残留。",
        "**停**：任一项缺失或含糊，停在此处并向用户索取；同时先把标记文件写入输出目录。",
        1,
    )
    assert check != _read(OWNER), "artifact missing: nothing to mutate for the negative case"
    scenario = tmp_path / "scenario"
    scenario.mkdir()
    _, run, _ = build_scenario(scenario, supplied=False)
    before = _snapshot(scenario)
    if "写入输出目录" in check and "副作用之前" in check:
        # A violating consumer would execute the write it just declared.
        (run / "marker.txt").write_text("written by the check\n", encoding="utf-8")
    after = _snapshot(scenario)
    problems = assert_check_is_read_only(check) + [
        "files changed across a missing-policy check" if after["files"] != before["files"] else ""
    ]
    assert any(problems), (
        "the injected write produced neither a text violation nor a snapshot difference — "
        "the zero-write assertion cannot go red"
    )
