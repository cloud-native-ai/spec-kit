"""Contract tests for Feature 082 US4 — the SC-003 closed-set drift guard (T020).

SC-003 says: "运行本特性之后，`skills/` 与 `templates/commands/` 下**只**有允许差异集内的
路径发生变化". That is a **containment claim** and MUST be decidable
(`.specify/shared/guidelines/closed-set-claims.md`). This module is its carrier and
implements the five declaration requirements from
``contracts/guard-and-measurement.contract.md`` GM-03 / GM-04:

=====  =========================================  =====================================
#      requirement                                how it is discharged here
=====  =========================================  =====================================
1      baseline reference object                  the module constant ``BASELINE``; never a
                                                  "current" variable, never a diff parent
2      comparison unit                            both product families, path by path:
                                                  ``skills/**`` and ``templates/commands/**``
3      allowed-difference set source              parsed out of ``data-model.md`` § GM-03
                                                  rows 1–8 — the single path landing point,
                                                  never copied into this module
4      complement assertion + invariants          complement byte-identical to the baseline;
                                                  only registered in-unit paths moved
5      undefined aggregate words cleared          this feature's own contracts and
                                                  ``data-model.md`` carry no "rest / etc."
                                                  wording used as a comparison scope
=====  =========================================  =====================================

Every reading prints a ``compared=<N> complement=<N> allowed_in_unit=<N> mismatches=<N>``
line, so a guard that compared nothing (an empty unit, a missing baseline) cannot pass
silently — the count is the evidence, and a zero denominator is itself a failure.

The full green reading belongs to T041 (Part 6); this row lands the guard and its
negative cases only.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

# Requirement 1: the baseline is a literal object name. It is never "HEAD", "main" or a
# variable that could be re-pointed; re-baselining is a change to this line and nothing else.
BASELINE = "3ffeb26e"

UNIT_ROOTS = ("skills", "templates/commands")

# The baseline tree carries no allowlist of its own — the comparison unit is read from git at
# ``BASELINE``. An **untracked** path is a different fact from a *registered* one: it is not in
# the baseline because it was never committed anywhere, so it cannot be a change this feature
# made. Every uncommitted path must still be registered (the working-tree loop below), and
# every registered new path must either be tracked or be this guard's own negative-case copy.
# 
DATA_MODEL_REL = Path(".specify/specs/082-mechanism-policy-separation/data-model.md")
CONTRACTS_DIR = REPO_ROOT / ".specify/specs/082-mechanism-policy-separation/contracts"

# Requirement 5: aggregate words that would turn the claim back into prose if used as a
# comparison scope. A word inside a *negation* ("must not use 'rest'") is quoting the rule,
# not applying it — hence the sentence-level scan below.
AGGREGATE_WORDS = ("其余", "其它", "其他", "未受影响", "untouched", "everything else", "the rest of")
NEGATION_CUES = ("MUST NOT", "MUST 不", "不得", "禁止", "never", "不许", "不复述")

# Marker prefixes of lines that quote the rule, name a boundary section, or count items of
# a table whose rows are already the named unit — never a comparison scope.
QUOTED_RULE_MARKERS = ("「", "## GR-09", "- 本文 MUST NOT 包含归属")

# A sentence that states an explicit exclusion ("out of this scan's scope …") supports the
# complement assertion; it is the opposite of an undefined aggregate scope.
EXCLUSION_CUES = ("在本条扫描面内", "在…之外", "之外", "excluded from", "out of scope")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _git(*args: str, cwd: Path = REPO_ROOT) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, check=False
    )
    assert proc.returncode == 0, "git %s failed: %s" % (" ".join(args), proc.stderr.strip())
    return proc.stdout


def baseline_paths(cwd: Path = REPO_ROOT, baseline: str = BASELINE) -> list[str]:
    """Every path of the comparison unit in the baseline tree, sorted."""
    out = _git("ls-tree", "-r", "--name-only", baseline, "--", *UNIT_ROOTS, cwd=cwd)
    return sorted(p for p in out.splitlines() if p.strip())


def working_tree_paths(cwd: Path = REPO_ROOT) -> list[str]:
    """Every path of the comparison unit in the working tree, sorted."""
    found: list[str] = []
    for root in UNIT_ROOTS:
        for path in (cwd / root).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                found.append(path.relative_to(cwd).as_posix())
    return sorted(found)


def registered_allowed_set(data_model_text: str) -> tuple[set, set]:
    """Parse GM-03 into (inside-unit, outside-unit) allowed paths. Rows 1–8 / 9–18."""
    m = re.search(r"^## GM-03 .*$", data_model_text, re.MULTILINE)
    assert m, "artifact missing: data-model.md carries no GM-03 section"
    body = data_model_text[m.end():]
    nxt = re.search(r"^## ", body, re.MULTILINE)
    body = body[: nxt.start()] if nxt else body
    inside: set = set()
    outside: set = set()
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 4 or not cells[0].isdigit():
            continue
        row_no = int(cells[0])
        target = inside if row_no <= 8 else outside
        for match in re.finditer(r"`([^`]+)`", cells[1]):
            target.add(match.group(1))
    return inside, outside


def _blob(path: str, cwd: Path) -> bytes | None:
    proc = subprocess.run(
        ["git", "cat-file", "blob", "%s:%s" % (BASELINE, path)],
        cwd=str(cwd), capture_output=True, check=False,
    )
    return proc.stdout if proc.returncode == 0 else None


def compare_working_tree(cwd: Path = REPO_ROOT) -> dict:
    """Compare both unit families path by path against the baseline blob.

    Returns a reading dict; ``problems`` lists every way the claim is violated.
    """
    base = baseline_paths(cwd)
    current = working_tree_paths(cwd)
    allowed_in_unit, _ = registered_allowed_set(
        (REPO_ROOT / DATA_MODEL_REL).read_text(encoding="utf-8")
    )
    problems: list[str] = []

    if not base:
        problems.append(
            "the baseline %r enumerates zero paths under %s — a guard that compares nothing "
            "proves nothing" % (BASELINE, " / ".join(UNIT_ROOTS))
        )
    if not current:
        problems.append(
            "the working tree enumerates zero paths under %s — the comparison unit is empty"
            % " / ".join(UNIT_ROOTS)
        )
    if not allowed_in_unit:
        problems.append(
            "data-model.md § GM-03 registers zero in-unit allowed paths — requirement 3 is unmet"
        )

    base_set, current_set = set(base), set(current)
    added = sorted(current_set - base_set)
    removed = sorted(base_set - current_set)
    changed: list[str] = []
    compared = 0
    for rel in base:
        if rel not in current_set:
            continue
        compared += 1
        blob = _blob(rel, cwd)
        if blob is None:
            problems.append(
                "%r exists in the working tree but not in the baseline tree — an unregistered "
                "new path inside the comparison unit" % rel
            )
            continue
        disk = (cwd / rel).read_bytes()
        if disk != blob:
            changed.append(rel)

    for rel in removed:
        problems.append(
            "%r was deleted from the comparison unit — deletions are not in the allowed set"
            % rel
        )
    for rel in added:
        problems.append(
            "%r is new inside the comparison unit — new paths are allowed only when registered "
            "(GM-03 rows 1–8)" % rel
        )

    complement = [rel for rel in base if rel not in allowed_in_unit]
    mismatches = [rel for rel in complement if rel in changed]
    for rel in mismatches:
        problems.append(
            "%r differs from the baseline blob but is not registered in data-model.md § GM-03 "
            "rows 1–8 — the containment claim is false for the complement" % rel
        )

    unregistered_changed = [rel for rel in changed if rel not in allowed_in_unit]
    for rel in unregistered_changed:
        if rel not in mismatches:
            problems.append("%r changed without being registered in GM-03" % rel)

    committed = _git(
        "diff", "--name-status", "%s..HEAD" % BASELINE, "--", *UNIT_ROOTS, cwd=cwd
    )
    committed_paths = []
    for line in committed.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            committed_paths.append((parts[0].strip(), parts[-1].strip()))
    for status, rel in committed_paths:
        if rel not in allowed_in_unit:
            problems.append(
                "committed change %s %r between %s and HEAD lies outside the registered "
                "allowed set (GATE-4)" % (status, rel, BASELINE)
            )

    return {
        "compared": compared,
        "unit": len(base_set),
        "complement": len(complement),
        "complement_size": len(complement),
        "allowed_in_unit": len(allowed_in_unit),
        "mismatches": len(mismatches),
        "changed": changed,
        "committed": committed_paths,
        "problems": problems,
    }


def reading_line(reading: dict) -> str:
    return "compared=%d unit=%d complement=%d allowed_in_unit=%d mismatches=%d" % (
        reading["compared"],
        reading["unit"],
        reading["complement"],
        reading["allowed_in_unit"],
        reading["mismatches"],
    )


def sentences(text: str) -> list[str]:
    parts = re.split(r"[。！？\n]|(?<=\.)\s+", text)
    return [p.strip() for p in parts if p.strip()]


def assert_no_aggregate_scope(text: str, label: str, skip_markers: tuple = ()) -> list[str]:
    """Return every sentence that uses an aggregate word as a comparison scope."""
    problems: list[str] = []
    kept: list[str] = []
    for line in text.splitlines():
        if skip_markers and line.strip().startswith(skip_markers):
            continue
        kept.append(line)
    for sentence in sentences("\n".join(kept)):
        hits = [w for w in AGGREGATE_WORDS if w in sentence]
        if not hits:
            continue
        if any(cue in sentence for cue in NEGATION_CUES):
            continue  # quoting the rule is not applying it
        if any(cue in sentence for cue in EXCLUSION_CUES):
            continue  # "outside this scan" names the exclusion, it does not claim a scope
        problems.append(
            "%s uses %s as a comparison scope — the claim must name its unit "
            "(closed-set-claims requirement 5)" % (label, " / ".join(hits))
        )
    return problems


# --------------------------------------------------------------------------- #
# requirement 2 + 4 — the complement is byte-identical, both families
# --------------------------------------------------------------------------- #
def test_sc003_complement_is_byte_identical_to_the_baseline():
    reading = compare_working_tree()
    line = reading_line(reading)
    print(line)
    assert reading["unit"] > 0, "empty comparison unit: %s" % line
    assert reading["allowed_in_unit"] > 0, "empty allowed set: %s" % line
    assert reading["complement"] > 0, "empty complement: %s" % line
    assert not reading["problems"], "SC-003 containment failures (%s):\n- %s" % (
        line, "\n- ".join(reading["problems"])
    )


def _git_tracked(cwd: Path = REPO_ROOT) -> set:
    out = _git("ls-files", "-z", "--", *UNIT_ROOTS, cwd=cwd)
    return {p for p in out.split("\0") if p.strip()}


def ownership_reading(
    cwd: Path = REPO_ROOT, data_model_text: str | None = None, baseline: str = BASELINE
) -> dict:
    """Separate **unregistered additions** (a defect of this feature) from **co-worktree paths**.

    A path that is inside the comparison unit, absent from the baseline, and untracked in the
    repository is present in this worktree because a *different* concurrent thread added it —
    it is not a path this feature created or changed. The guard must still see it (the count
    is printed), and it must still fail every path this feature's own allowed set does not
    cover *if* that path is tracked.
    """
    base = set(baseline_paths(cwd, baseline))
    current = set(working_tree_paths(cwd))
    tracked = _git_tracked(cwd)
    allowed_in_unit, _ = registered_allowed_set(
        data_model_text if data_model_text is not None
        else (REPO_ROOT / DATA_MODEL_REL).read_text(encoding="utf-8")
    )
    added = sorted(current - base)
    co_worktree = [rel for rel in added if rel not in tracked]
    unregistered = [rel for rel in added if rel in tracked and rel not in allowed_in_unit]
    return {
        "baseline": len(base),
        "current": len(current),
        "added": added,
        "co_worktree": co_worktree,
        "unregistered_additions": unregistered,
        "allowed_in_unit": len(allowed_in_unit),
    }


def test_sc003_unregistered_additions_are_absent_and_co_worktree_paths_are_reported():
    reading = ownership_reading()
    allowed_in_unit, _ = registered_allowed_set(
        (REPO_ROOT / DATA_MODEL_REL).read_text(encoding="utf-8")
    )
    print(
        "baseline=%d current=%d added=%d co_worktree=%d in_allowed=%d unregistered_additions=%d "
        "allowed_in_unit=%d"
        % (
            reading["baseline"],
            reading["current"],
            len(reading["added"]),
            len(reading["co_worktree"]),
            sum(1 for rel in reading["co_worktree"] if rel in allowed_in_unit),
            len(reading["unregistered_additions"]),
            reading["allowed_in_unit"],
        )
    )
    assert reading["current"] > 0 and reading["baseline"] > 0, "empty comparison unit"
    assert not reading["unregistered_additions"], (
        "tracked paths inside the comparison unit are new and not registered in GM-03 rows 1–8: %s"
        % reading["unregistered_additions"]
    )
    # A co-worktree path that *is* in the allowed set would be a path this feature claims but
    # never committed — the claim would then rest on a file another thread may delete. Every
    # allowed path must therefore be tracked once it exists.
    tracked = _git_tracked()
    existed = [rel for rel in allowed_in_unit if (REPO_ROOT / rel).is_file()]
    unproven = [rel for rel in existed if rel not in tracked]
    print("allowed_paths_present=%d unproven=%s" % (len(existed), unproven or "none"))
    assert not unproven, "allowed paths present on disk but absent from git: %s" % unproven


def test_sc003_both_families_are_inside_the_comparison_unit():
    reading = compare_working_tree()
    base = baseline_paths()
    families = {root: [p for p in base if p == root or p.startswith(root + "/")] for root in UNIT_ROOTS}
    print(reading_line(reading))
    for root, paths in families.items():
        assert paths, (
            "the comparison unit enumerates zero paths for family %r — requirement 2 says "
            "both product families are in the unit" % root
        )


# --------------------------------------------------------------------------- #
# requirement 3 — the allowed set is parsed from its single landing point
# --------------------------------------------------------------------------- #
def test_gm03_allowed_set_parses_to_eight_in_unit_rows():
    inside, outside = registered_allowed_set((REPO_ROOT / DATA_MODEL_REL).read_text(encoding="utf-8"))
    assert len(inside) == 8, (
        "GM-03 rows 1–8 must register the in-unit allowed set; parsed %d path(s): %s"
        % (len(inside), sorted(inside))
    )
    assert outside, "GM-03 rows 9–18 register the out-of-unit new paths; parsed none"
    for rel in inside:
        assert not rel.startswith("tests/"), (
            "%r sits in the in-unit set but lives outside the comparison unit" % rel
        )


# --------------------------------------------------------------------------- #
# requirement 5 — no undefined aggregate word used as a comparison scope
# --------------------------------------------------------------------------- #
def test_requirement5_no_aggregate_scope_word_in_feature_contracts():
    problems: list[str] = []
    scanned = 0
    for path in sorted(CONTRACTS_DIR.glob("*.md")):
        scanned += 1
        # Requirement 5 bans an aggregate word used as a *comparison scope* — a shell that
        # stands in for a path list. These three files also *quote the rule* back, name a
        # boundary section, and count rows; those uses are not scopes and are excluded by
        # their own markers rather than by loosening the scan for everyone.
        problems += assert_no_aggregate_scope(
            path.read_text(encoding="utf-8"),
            str(path.relative_to(REPO_ROOT)),
            skip_markers=QUOTED_RULE_MARKERS,
        )
    dt = (REPO_ROOT / DATA_MODEL_REL).read_text(encoding="utf-8")
    m = re.search(r"^## GM-03 .*$", dt, re.MULTILINE)
    assert m, "artifact missing: data-model.md carries no GM-03 section"
    body = dt[m.end():]
    nxt = re.search(r"^## ", body, re.MULTILINE)
    gm03_body = body[: nxt.start()] if nxt else body
    gm03_rows = [ln for ln in gm03_body.splitlines() if ln.strip().startswith("|")]
    gm03_prose = [
        ln for ln in gm03_body.splitlines()
        if not ln.strip().startswith("|") and "本表行" not in ln
    ]
    assert gm03_rows, "artifact missing: GM-03 carries no table rows"
    problems += assert_no_aggregate_scope(
        "\n".join(gm03_prose), DATA_MODEL_REL.as_posix() + " § GM-03"
    )
    print("scanned=%d contract files" % scanned)
    assert scanned > 0, "scanned zero contract files — the requirement 5 scan is vacuous"
    assert not problems, "aggregate-scope violations:\n- %s" % "\n- ".join(problems)


# --------------------------------------------------------------------------- #
# negative cases (GM-07) — the assertion must be able to go red
# --------------------------------------------------------------------------- #
def _fake_tree(tmp_path: Path) -> Path:
    """A minimal repo-shaped tree with a two-commit history and a GM-03 data model."""
    tree = tmp_path / "repo"
    (tree / "skills/external/a").mkdir(parents=True)
    (tree / "skills/external/b").mkdir(parents=True)
    (tree / "templates/commands").mkdir(parents=True)
    (tree / "skills/external/a/SKILL.md").write_text("a\n", encoding="utf-8")
    (tree / "skills/external/b/SKILL.md").write_text("b\n", encoding="utf-8")
    (tree / "templates/commands/x.md").write_text("x\n", encoding="utf-8")
    (tree / ".specify/specs/082-mechanism-policy-separation").mkdir(parents=True)
    (tree / DATA_MODEL_REL).write_text(
        "## GM-03 — 允许差异集\n\n"
        "| # | 路径 | 类别 | 属比较单元 |\n|---|---|---|---|\n"
        "| 1 | `skills/external/a/SKILL.md` | 改写 | 是 |\n"
        "| 2 | `skills/external/b/SKILL.md` | 改写 | 是 |\n"
        "| 3 | `skills/external/c/SKILL.md` | 改写 | 是 |\n"
        "| 4 | `skills/external/d/SKILL.md` | 改写 | 是 |\n"
        "| 5 | `skills/external/e/SKILL.md` | 改写 | 是 |\n"
        "| 6 | `skills/external/f/SKILL.md` | 改写 | 是 |\n"
        "| 7 | `skills/external/g/SKILL.md` | 改写 | 是 |\n"
        "| 8 | `skills/external/h/SKILL.md` | 改写 | 是 |\n"
        "| 9 | `tests/contract/test_x.py` | 新增 | 否 |\n",
        encoding="utf-8",
    )
    _git("init", "-q", cwd=tree)
    _git("-c", "user.email=t@example.com", "-c", "user.name=t", "add", "-A", cwd=tree)
    _git(
        "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-qm", "base", cwd=tree
    )
    return tree


def test_negative_case_one_byte_change_in_the_complement_turns_red(tmp_path):
    tree = _fake_tree(tmp_path)
    baseline = _git("rev-parse", "HEAD", cwd=tree).strip()
    clean = compare_working_tree_in(tree, baseline)
    assert not clean["problems"], "the fake tree must start clean: %s" % clean["problems"]
    # one byte in a complement file: ``b`` is registered, so the command template is not
    (tree / "templates/commands/x.md").write_text("y\n", encoding="utf-8")
    broken = compare_working_tree_in(tree, baseline)
    assert broken["mismatches"] >= 1, (
        "the one-byte change in the complement did not turn the guard red: %s"
        % reading_line(broken)
    )
    assert any("templates/commands/x.md" in p for p in broken["problems"])


def test_negative_case_unregistered_new_path_turns_red(tmp_path):
    tree = _fake_tree(tmp_path)
    baseline = _git("rev-parse", "HEAD", cwd=tree).strip()
    (tree / "skills/external/z/SKILL.md").parent.mkdir(parents=True)
    (tree / "skills/external/z/SKILL.md").write_text("z\n", encoding="utf-8")
    broken = compare_working_tree_in(tree, baseline)
    assert any("skills/external/z/SKILL.md" in p for p in broken["problems"]), (
        "the unregistered new path did not turn the guard red: %s" % broken["problems"]
    )


def test_negative_case_a_concurrent_addition_is_reported_not_swallowed(tmp_path):
    """An untracked addition to the unit is named as co-worktree, never folded into "clean".

    The fake tree starts clean; a second writer adds an untracked path outside the allowed
    set. The containment assertion (which fails such a path) and the ownership reading (which
    names it) must both see it: the guard never becomes green by not looking.
    """
    tree = _fake_tree(tmp_path)
    baseline = _git("rev-parse", "HEAD", cwd=tree).strip()
    (tree / "skills/external/other/SKILL.md").parent.mkdir(parents=True)
    (tree / "skills/external/other/SKILL.md").write_text("o\n", encoding="utf-8")
    reading = ownership_reading(
        tree,
        data_model_text=(REPO_ROOT / DATA_MODEL_REL).read_text(encoding="utf-8"),
        baseline=_git("rev-parse", "HEAD", cwd=tree).strip(),
    )
    assert "skills/external/other/SKILL.md" in reading["co_worktree"], (
        "an untracked addition to the comparison unit was not reported as co-worktree: %s"
        % reading["added"]
    )
    broken = compare_working_tree_in(tree, baseline)
    assert any("skills/external/other/SKILL.md" in p for p in broken["problems"]), (
        "the containment assertion no longer sees an untracked addition — the guard could be "
        "made green by ignoring it"
    )


def test_negative_case_aggregate_scope_word_turns_red():
    clean = assert_no_aggregate_scope("只有登记过的路径可以变化。", "sample")
    assert not clean
    dirty = assert_no_aggregate_scope("其余路径保持未受影响。", "sample")
    assert dirty, "an aggregate word used as a comparison scope did not turn the scan red"
    quoted = assert_no_aggregate_scope("MUST NOT 使用「其余」一类聚合词。", "sample")
    assert not quoted, "quoting the rule must not be reported as applying it"


def compare_working_tree_in(tree: Path, baseline: str) -> dict:
    """Same comparison as ``compare_working_tree`` but against an explicit tree and baseline.

    Used only by the negative cases; the real assertions read the module-level literal
    ``BASELINE`` so the baseline can never be re-pointed by a caller.
    """
    def _run(*args: str) -> str:
        proc = subprocess.run(
            ["git", *args], cwd=str(tree), capture_output=True, text=True, check=False
        )
        assert proc.returncode == 0, proc.stderr
        return proc.stdout

    base = sorted(
        p for p in _run("ls-tree", "-r", "--name-only", baseline, "--", *UNIT_ROOTS).splitlines()
        if p.strip()
    )
    current = sorted(
        path.relative_to(tree).as_posix()
        for root in UNIT_ROOTS
        for path in (tree / root).rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )
    allowed_in_unit, _ = registered_allowed_set(
        (tree / DATA_MODEL_REL).read_text(encoding="utf-8")
    )
    problems: list[str] = []
    changed: list[str] = []
    for rel in base:
        if rel not in current:
            problems.append("%r was deleted from the comparison unit" % rel)
            continue
        blob = subprocess.run(
            ["git", "cat-file", "blob", "%s:%s" % (baseline, rel)],
            cwd=str(tree), capture_output=True, check=False,
        ).stdout
        if (tree / rel).read_bytes() != blob:
            changed.append(rel)
    for rel in sorted(set(current) - set(base)):
        problems.append("%r is new inside the comparison unit" % rel)
    complement = [rel for rel in base if rel not in allowed_in_unit]
    mismatches = [rel for rel in complement if rel in changed]
    for rel in mismatches:
        problems.append("%r differs from the baseline but is not registered" % rel)
    return {
        "compared": len(base),
        "unit": len(base),
        "complement": len(complement),
        "allowed_in_unit": len(allowed_in_unit),
        "mismatches": len(mismatches),
        "changed": changed,
        "committed": [],
        "problems": problems,
    }
