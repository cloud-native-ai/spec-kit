"""Contract tests for Feature 107 — Decision Governance (foundational owner-page guards).

This file asserts the contract surface of the owner page
``shared/definitions/decision-definitions.md`` and, later, the pointer discipline of its
adjacent owners and the instruction-section landing. It never asserts prose quality:
section presence is pinned on the ``^## `` heading sequence, the closed vocabulary is pinned
as a row set read out of its own table, and "pointer, not a copy" is decided by comparing
an adjacent owner's headings against the page instead of by reading both documents.

Scenario groups (declared in ``tasks.md``; later packages APPEND new classes/tests without
touching the earlier assertions):

* **F — foundational** (T005): the page exists; § Ownership Declaration names every owned
  surface and the pointer-only duty with its adjacent owners; § Closed Vocabulary carries
  exactly the nine closed terms; no adjacent owner's criteria-table heading is restated.

Red-first tests live in their own modules (``test_decision_governance_guards.py``,
``test_validate_decisions.py``); this module pins the owner-page surface only.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]

OWNER = ROOT / "shared" / "definitions" / "decision-definitions.md"

#: The nine closed terms (T004), verbatim.
NINE_TERMS = (
    "Decision Item",
    "Decision Record",
    "Option",
    "Decision Block",
    "Acknowledgement",
    "Implementation Receipt",
    "Decision Producer",
    "Archive Projection",
    "Decision Class",
)

#: The nine owned surfaces the § Ownership Declaration MUST name (T004), as the English
#: phrases the declaration carries in parentheses.
OWNED_SURFACE_PHRASES = (
    "closed vocabulary",
    "class presentation",
    "option-set contract",
    "record field closure",
    "field-to-owner mapping",
    "archive projection and producer inventory",
    "transmission obligations",
    "enforcement boundary",
    "legacy rules",
)

#: The adjacent owners whose facts the page MUST reach by pointer only (FR-002). The page's
#: pointer table MUST name each path.
ADJACENT_OWNER_PATHS = (
    "shared/guidelines/confirmation-gates.md",
    "shared/guidelines/decision-tension.md",
    "shared/guidelines/fast-fail.md",
    "shared/definitions/superagent-definitions.md",
)

#: Adjacent owner files whose criteria-table H2 headings MUST NOT be restated in the page.
ADJACENT_HEADING_FILES = (
    "shared/guidelines/confirmation-gates.md",
    "shared/guidelines/decision-tension.md",
    "shared/guidelines/fast-fail.md",
    "shared/definitions/superagent-definitions.md",
)

VOCABULARY_ROW_RE = re.compile(r"^\| \*\*(.+?)\*\* \|")


# --------------------------------------------------------------------------- #
# helpers (shared by the groups appended in later packages)
# --------------------------------------------------------------------------- #

def read(path: Path) -> str:
    """Read an artifact, failing as 'missing file' rather than as a wrong assertion."""
    assert path.is_file(), f"missing file: {path}"
    return path.read_text(encoding="utf-8")


def norm(text: str) -> str:
    """Whitespace-normalise an artifact body: the docs hard-wrap prose, the pins are spans."""
    return " ".join(text.split())


def h2_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.startswith("## ")]


def h2_section(text: str, *tokens: str) -> str:
    """Body of the first H2 heading carrying every token, up to the next H2 or EOF."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and all(token in line for token in tokens):
            start = index
            break
    assert start is not None, f"missing H2 section carrying {tokens!r}"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start + 1:end])


# --------------------------------------------------------------------------- #
# F — foundational owner-page guards (T005)
# --------------------------------------------------------------------------- #

def test_owner_page_exists() -> None:
    body = read(OWNER)
    assert body.strip(), "owner page is empty"
    assert body.lstrip().startswith("# "), "owner page carries no level-1 heading"


def test_ownership_declaration_names_every_owned_surface() -> None:
    body = read(OWNER)
    declaration = h2_section(body, "所有权声明", "Ownership Declaration")
    flat = norm(declaration)
    for phrase in OWNED_SURFACE_PHRASES:
        assert phrase in flat, f"§ Ownership Declaration does not name the {phrase!r} surface"
    assert "pointer-only duty" in flat, "§ Ownership Declaration lacks the pointer-only duty"
    for path in ADJACENT_OWNER_PATHS:
        assert path in flat, f"§ Ownership Declaration does not name adjacent owner {path}"


def test_closed_vocabulary_has_exactly_nine_terms() -> None:
    body = read(OWNER)
    section = h2_section(body, "封闭词汇表", "Closed Vocabulary")
    terms = [m.group(1).strip() for m in map(VOCABULARY_ROW_RE.match, section.splitlines()) if m]
    assert len(terms) == len(NINE_TERMS), (
        f"§ Closed Vocabulary carries {len(terms)} term row(s): {terms}"
    )
    assert set(terms) == set(NINE_TERMS), (
        f"§ Closed Vocabulary term set differs: missing={set(NINE_TERMS) - set(terms)}, "
        f"extra={set(terms) - set(NINE_TERMS)}"
    )


def test_no_adjacent_owner_criteria_heading_restated() -> None:
    page_headings = set(h2_lines(read(OWNER)))
    for rel in ADJACENT_HEADING_FILES:
        for heading in h2_lines(read(ROOT / rel)):
            assert heading not in page_headings, (
                f"owner page restates the adjacent heading {heading!r} from {rel}"
            )


# --------------------------------------------------------------------------- #
# US1 — decision text contract and the two decision classes (T009)
# --------------------------------------------------------------------------- #

INSTRUCTION_TEMPLATE = ROOT / "templates" / "instructions-template.md"
FIXTURES = ROOT / "tests" / "fixtures" / "decision-governance"

#: C-102's full-name rule, as the owner page states it (whitespace-normalised pin).
FULL_NAME_PIN = "MUST 使用对象的完整名称，MUST NOT 只用简称"

#: C-103's same-name family, as both the owner page and the instruction section carry it.
SAME_NAME_PINS = ("`same_name_conflict: true`", "`resource_locator`",
                  "business resource group", "region id")


def instruction_section() -> str:
    """Body of the ``## Decision Items（决策项）`` section of the instruction template."""
    return h2_section(read(INSTRUCTION_TEMPLATE), "Decision Items", "决策项")


def test_class_declaration_closed() -> None:
    """C-101: exactly one class from the closed set, judged by holder (A-4)."""
    section = h2_section(read(OWNER), "决策类别", "Decision Classes")
    flat = norm(section)
    assert "持有者(holder)" in flat, (
        "§ Decision Classes does not state that the class is judged by the holder"
    )
    assert "MUST 声明恰一个 `decision_class`" in flat, (
        "§ Decision Classes does not require exactly one decision_class declaration"
    )
    assert "闭集 `human-interactive` / `ai-autonomous`" in flat, (
        "§ Decision Classes does not name the closed class set"
    )
    assert "类缺失、类混合或值域外是缺陷" in flat, (
        "§ Decision Classes does not name the three defect forms"
    )
    assert "类别决定适用的模板与检查集" in flat, (
        "§ Decision Classes does not state that the class picks the template and check set"
    )
    assert "传递不改变类别" in flat, (
        "§ Decision Classes does not state that transmission never re-classes"
    )


def test_full_name_minimum_bar_four_surfaces() -> None:
    """C-102: the two production rules land on four surfaces together."""
    # Surface 1 — the owner page's § Decision Text Contract.
    text_contract = norm(h2_section(read(OWNER), "决策文本契约", "Decision Text Contract"))
    assert FULL_NAME_PIN in text_contract, (
        "owner page § Decision Text Contract does not carry the full-name rule"
    )
    for token in SAME_NAME_PINS:
        assert token in text_contract, (
            f"owner page § Decision Text Contract does not carry {token!r}"
        )
    assert "同名对象 MUST NOT 在没有定位信息时被呈现" in text_contract, (
        "owner page does not ban presenting a same-name object without a locator"
    )

    # Surface 2 — the instruction section (a whole section, not a bullet elsewhere).
    raw = instruction_section()
    instr = norm(raw)
    assert "full name" in instr and "abbreviation" in instr, (
        "instruction section does not carry the full-name rule"
    )
    for token in SAME_NAME_PINS:
        assert token in instr, f"instruction section does not carry {token!r}"
    assert ".specify/shared/definitions/decision-definitions.md" in instr, (
        "instruction section does not point at the owner page"
    )
    assert "**本节字节上限：1,500 B**" in raw, (
        "instruction section does not declare its byte ceiling"
    )
    assert not any(line.strip().startswith("|") for line in raw.splitlines()), (
        "instruction section copies a table from the owner page"
    )

    # Surface 3 — the decision-item templates (owner page § Decision Classes).
    classes = norm(h2_section(read(OWNER), "决策类别", "Decision Classes"))
    assert "完整名称与定位信息(full names and locator)" in classes, (
        "the decision-item templates do not carry the full-name/locator element"
    )
    assert "§ 决策文本契约" in classes, (
        "the decision-item templates do not reach the text contract by pointer"
    )

    # Surface 4 — the guard fixtures plus the named B-01/B-02 review surfaces.
    assert (FIXTURES / "m02" / "red-empty-locator.md").is_file(), (
        "missing M-02 guard fixture"
    )
    assert (FIXTURES / "m08" / "red-variant.md").is_file(), (
        "missing M-08 guard fixture"
    )
    for surface in ("B-01", "B-02"):
        assert surface in text_contract, (
            f"owner page § Decision Text Contract does not name the {surface} review surface"
        )


def test_human_template_elements() -> None:
    """C-104: the human-interactive template carries every readability element."""
    flat = norm(h2_section(read(OWNER), "决策类别", "Decision Classes"))
    for token in (
        "平实语言",
        "上下文(context)",
        "后果(consequences)与可逆性(reversibility)",
        "默认项(default)",
        "完整名称与定位信息(full names and locator)",
        "shared/guidelines/user-facing-comprehension.md",
        "MUST NOT 只给形式化谓词",
    ):
        assert token in flat, f"human-interactive template lacks {token!r}"


def test_ai_template_elements() -> None:
    """C-105: the ai-autonomous template carries every rigor element."""
    flat = norm(h2_section(read(OWNER), "决策类别", "Decision Classes"))
    for token in (
        "封闭选项集(closed options)",
        "决策谓词/规则",
        "显式假设(assumptions)",
        "可机器核查的证据指针(evidence pointers)",
        "确定性结论与重开条件",
        "MUST NOT 只有散文",
    ):
        assert token in flat, f"ai-autonomous template lacks {token!r}"


# --------------------------------------------------------------------------- #
# US2 — option-set contract pointer discipline (T021)
# --------------------------------------------------------------------------- #

#: The gate-observation protocol's signal value domain (owned by
#: ``shared/guidelines/confirmation-gates.md`` § 门控观察协议). The owner page reaches it
#: by pointer only; any of these literals in the section is a restatement.
GATE_SIGNAL_LITERALS = ("approved-as-is", "asked-questions", "denied", "修改后放行")


def test_human_signal_pointer_only() -> None:
    """C-108: the human choice signal is reached by pointer, never restated."""
    section = norm(h2_section(read(OWNER), "选项集契约", "Option-Set Contract"))
    assert "shared/guidelines/confirmation-gates.md" in section, (
        "§ Option-Set Contract does not reach the gate-observation protocol by path"
    )
    assert "门控观察协议" in section, (
        "§ Option-Set Contract does not name the gate-observation protocol section"
    )
    for literal in GATE_SIGNAL_LITERALS:
        assert literal not in section, (
            "§ Option-Set Contract restates the gate-observation signal value "
            f"{literal!r} instead of pointing at its owner"
        )


# --------------------------------------------------------------------------- #
# US3 — record grammar, archive projection and read-only dispositions (T025)
# --------------------------------------------------------------------------- #

#: The ten base-layer fields (C-202); ``decision_id`` is carried by the heading.
BASE_FIELDS = (
    "decision_id", "decision_class", "context", "options", "chosen_option",
    "rationale", "evidence", "actor", "created_at", "transmission_status",
)

#: The conditional-layer fields, by trigger family (C-202).
CONDITIONAL_FIELDS = (
    "same_name_conflict", "resource_locator", "superseded_by",
    "dispatched_at", "acknowledged_at", "implemented_at",
)


def test_record_line_grammar() -> None:
    """C-201: the serialization grammar is stated on the owner page, field names included."""
    flat = norm(h2_section(read(OWNER), "决策记录", "Decision Record"))
    for token in (
        "### D-NNN — <一行标题>",
        "- **<小写字段名>**: <值>",
        "缩进子行",
        "缩进 ≥2 空格",
        "围栏代码块",
        "未到相位不设占位",
        "MUST NOT 以对话记忆补足",
        "MUST NOT 复制",
        "密集",
        "载体指针",
    ):
        assert token in flat, f"§ Decision Record lacks {token!r}"
    for field in BASE_FIELDS + CONDITIONAL_FIELDS:
        assert f"`{field}`" in flat, f"§ Decision Record does not name the field `{field}`"
    assert "取代" in flat, "§ Decision Record does not state the supersession rule"


def test_no_second_store() -> None:
    """C-207: the archive is a projection; the register stays the sole id index."""
    section = h2_section(read(OWNER), "档案即投影", "Archive as Projection")
    flat = norm(section)
    for token in (
        "生产者 × 既有载体",
        "并集",
        ".specify/register.md",
        "不是第二套存储",
        "MUST NOT 新建第二套登记、队列、存储或调度器",
        "编号唯一索引",
    ):
        assert token in flat, f"§ Archive as Projection lacks {token!r}"
    producers = re.findall(r"^\| (P-\d{2}) \|", section, re.M)
    assert set(producers) == {f"P-{n:02d}" for n in range(1, 13)}, (
        f"the producer inventory rows differ from P-01…P-12: {producers}"
    )


def test_read_only_disposition_carrier() -> None:
    """C-208: a read-only command's disposition lands in its own report, never by rewrite."""
    flat = norm(h2_section(read(OWNER), "档案即投影", "Archive as Projection"))
    for token in (
        "只读命令的处置",
        "自己的报告载体",
        "MUST NOT 通过修改被分析的工件来归档",
    ):
        assert token in flat, f"§ Archive as Projection lacks {token!r}"


# --------------------------------------------------------------------------- #
# US5 — enforcement honesty: B surfaces, gate neutrality, review surfaces (T039)
# --------------------------------------------------------------------------- #

import json
import subprocess
import sys

ENFORCEMENT_SECTION_TOKENS = ("强制边界", "Enforcement Boundary")
SUPERAGENT = ROOT / "shared" / "definitions" / "superagent-definitions.md"
SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
GATE_RECORD = (
    ROOT / ".specify" / "specs" / "107-decision-governance" / "test-evidence"
    / "gate-neutrality.txt"
)

#: The FR-025 preservation owners (three files, byte-for-byte containment claim) and the
#: effective baseline the claim is read against (default `fbab7a45c`, replaceable only by a
#: recorded re-baseline ruling).
FR025_PATHS = (
    "shared/declarations/facts/driver-completion-sentinels.yaml",
    "skills/external/sdd-loop-driver/references/watch-model.md",
    "skills/external/sdd-loop-driver/references/efficiency-model.md",
)
FR025_BASELINE = "fbab7a45c"

#: The seven role fields, the four pre-existing injections and the five uplink items
#: (EP-002 payload shape; ownership stays with superagent-definitions.md).
ROLE_FIELDS = (
    "parent_identity", "child_label", "role_declaration", "dispatch_duty",
    "depth_position", "authority_ref", "return_channel",
)
INJECTION_REFS = (
    "shared/guidelines/fast-fail.md",
    "subagent-definitions.md` § The Concurrency Obligation",
    "shared/guidelines/reporting-obligations.md",
    "shared/definitions/re-anchoring-definitions.md",
)
#: The feature-touched code faces the gate scan covers (paths relative to the repo root).
FEATURE_TOUCHED_FACES = frozenset({
    "shared/definitions/decision-definitions.md",
    "shared/definitions/superagent-definitions.md",
    "shared/guidelines/confirmation-gates.md",
    "shared/guidelines/decision-tension.md",
    "shared/guidelines/fast-fail.md",
    "shared/definitions/goal-definitions.md",
    "shared/definitions/anchor-definitions.md",
    "shared/definitions/agent-definitions.md",
    "templates/instructions-template.md",
    "skills/internal/run-agent/SKILL.md",
    "skills/internal/run-team/SKILL.md",
    "skills/internal/analyze-artifacts/SKILL.md",
    "skills/internal/review-feature-quality/SKILL.md",
    "skills/internal/review-sdd-process/SKILL.md",
    "skills/external/sdd-loop-driver/references/checkpoint-protocol.md",
    "skills/external/sdd-loop-driver/references/dispatch-recipes.md",
    "skills/external/sdd-loop-driver/references/stage-prompts.md",
})


def behavior_rows() -> dict[str, tuple[str, str]]:
    """(surface cell, coverage cell) per B row of the owner page's § Enforcement Boundary."""
    section = h2_section(read(OWNER), *ENFORCEMENT_SECTION_TOKENS)
    rows: dict[str, tuple[str, str]] = {}
    for line in section.splitlines():
        match = re.match(r"^\| (B-\d{2})[^|]*\|([^|]*)\|([^|]*)\|", line)
        if match:
            rows[match.group(1)] = (match.group(2).strip(), match.group(3).strip())
    return rows


def test_behavior_surfaces_named() -> None:
    """C-402: every behavior rule names its review surface and disclaims machine coverage."""
    rows = behavior_rows()
    assert set(rows) == {f"B-{n:02d}" for n in range(1, 8)}, sorted(rows)
    for rule, (surface, coverage) in rows.items():
        assert surface, f"{rule} names no review surface"
        assert "/speckit.review" in surface or "/speckit.analyze" in surface or (
            "人工决策评审" in surface
        ), (rule, surface)
        assert "不声称机器覆盖" in coverage, (
            f"{rule} does not carry the explicit no-machine-coverage statement: {coverage!r}"
        )
    for rule in ("B-04", "B-05", "B-07"):
        assert "/speckit.analyze" in rows[rule][0], (rule, rows[rule][0])
    for rule in ("B-01", "B-02", "B-03", "B-06"):
        assert "/speckit.review" in rows[rule][0], (rule, rows[rule][0])

    # The machine table keeps the complementary claim: machine-covered, one judge each.
    section = h2_section(read(OWNER), *ENFORCEMENT_SECTION_TOKENS)
    for line in section.splitlines():
        match = re.match(r"^\| (M-\d{2})[^|]*\|([^|]*)\|([^|]*)\|([^|]*)\|", line)
        if match:
            assert "机器覆盖" in match.group(4), (match.group(1), match.group(4))

    # No test asserts a machine verdict for a behavior rule.
    guards = read(ROOT / "tests" / "contract" / "test_decision_governance_guards.py")
    assert not re.search(r'"B-\d{2}"', guards), (
        "the guards module quotes a behavior rule id; behavior rules are never machine-judged"
    )


def run_scanner_summary() -> dict[str, int]:
    completed = subprocess.run(
        [sys.executable, str(SCANNER), "--summary"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert completed.returncode == 0, completed.stderr
    readings: dict[str, int] = {}
    patterns = {
        "blocking": r"blocking confirmation gates:\s*(\d+)",
        "destructive": r"destructive:\s*(\d+)",
        "governance_kept": r"governance_kept:\s*(\d+)",
        "reversible": r"reversible:\s*(\d+)",
        "violations": r"violations[^:]*:\s*(\d+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, completed.stdout)
        assert match, f"the scan summary carries no {key!r} reading: {completed.stdout!r}"
        readings[key] = int(match.group(1))
    return readings


def test_gate_neutrality() -> None:
    """C-405: zero new gate hits against the re-baselined reading; FR-025 stays byte-identical."""
    record = read(GATE_RECORD)
    effective = {
        key: int(re.search(rf"^{key}: (\d+)$", record, re.M).group(1))
        for key in (
            "effective_baseline_blocking",
            "effective_baseline_destructive",
            "effective_baseline_governance_kept",
            "effective_baseline_reversible",
            "effective_baseline_violations",
        )
    }
    assert effective["effective_baseline_blocking"] == 30, (
        "the recorded effective baseline is not the merged-tree re-baselined 30"
    )

    current = run_scanner_summary()
    assert current["violations"] == effective["effective_baseline_violations"] == 0, (
        current
    )
    for key in ("blocking", "destructive", "governance_kept", "reversible"):
        assert current[key] == effective[f"effective_baseline_{key}"], (key, current, effective)

    # Zero NEW hits on the feature-touched faces: only the two pre-existing
    # dispatch-recipes members appear, nothing else touched by this feature does.
    scan = subprocess.run(
        [sys.executable, str(SCANNER), "--json"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert scan.returncode == 0, scan.stderr
    gates = json.loads(scan.stdout)["gates"]
    hits = [gate for gate in gates if gate["file"] in FEATURE_TOUCHED_FACES]
    assert len(hits) == 2, [(gate["file"], gate["line"]) for gate in hits]
    assert all(gate["file"].endswith("dispatch-recipes.md") for gate in hits), hits

    # FR-025 preservation: the three owner artifacts are byte-identical to the effective
    # baseline (default fbab7a45c; no recorded re-baseline ruling replaces it).
    quiet = subprocess.run(
        ["git", "diff", "--quiet", f"{FR025_BASELINE}..HEAD", "--", *FR025_PATHS],
        cwd=str(ROOT),
    )
    assert quiet.returncode == 0, (
        "the FR-025 preservation owners drifted from the effective baseline"
    )
    numstat = subprocess.run(
        ["git", "diff", "--numstat", f"{FR025_BASELINE}..HEAD", "--", *FR025_PATHS],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert numstat.stdout.strip() == "", numstat.stdout

    # EP-002: the payload field counts (seven role fields + four injections + five-item
    # uplink) are unchanged.
    superagent = read(SUPERAGENT)
    for field in ROLE_FIELDS:
        assert f"`{field}`" in superagent, f"the role field `{field}` vanished"
    for ref in INJECTION_REFS:
        assert ref in superagent, f"the injection pointer {ref!r} vanished"
    uplink = norm(h2_section(superagent, "The super↔sub Protocol"))
    for item in ("evidence pointer", "anomaly line", "concurrency reading triple",
                 "returning executor's identity", "deliverable path"):
        assert item in uplink, f"the uplink paragraph lost {item!r}"


def test_review_surfaces_named() -> None:
    """C-109: the class/presentation mismatch is named on review surfaces, never machine-claimed."""
    rows = behavior_rows()
    for rule in ("B-03", "B-04", "B-06"):
        assert rows.get(rule), f"§ Enforcement Boundary names no {rule} row"
    assert "/speckit.review" in rows["B-03"][0], rows["B-03"]
    assert "/speckit.analyze" in rows["B-04"][0], rows["B-04"]
    assert "/speckit.review" in rows["B-06"][0], rows["B-06"]

    classes = norm(h2_section(read(OWNER), "决策类别", "Decision Classes"))
    assert "B-03" in classes and "B-04" in classes and "B-06" in classes, (
        "§ Decision Classes does not name the three review surfaces of a mismatch"
    )
    assert "MUST NOT 被机器声称覆盖" in classes, (
        "§ Decision Classes does not disclaim machine coverage"
    )

    owners = {
        "skills/internal/analyze-artifacts/SKILL.md": ("B-04", "B-05", "B-07"),
        "skills/internal/review-feature-quality/SKILL.md": tuple(f"B-{n:02d}" for n in range(1, 8)),
        "skills/internal/review-sdd-process/SKILL.md": tuple(f"B-{n:02d}" for n in range(1, 8)),
    }
    for rel, ids in owners.items():
        body = read(ROOT / rel)
        assert "shared/definitions/decision-definitions.md" in body, (
            f"{rel} does not reach the owner page by pointer"
        )
        for rule in ids:
            assert rule in body, f"{rel} does not name the {rule} review surface"


# --------------------------------------------------------------------------- #
# US6 — landing closures: mirrors, copies, byte budgets, client init (T048)
# --------------------------------------------------------------------------- #

import os

SYNC_MIRRORS = ROOT / "scripts" / "python" / "sync-mirrors.py"
REGEN_COPIES = ROOT / "scripts" / "python" / "regen-command-copies.py"
MIRROR_BASELINE = (
    ROOT / ".specify" / "specs" / "107-decision-governance" / "test-evidence"
    / "sync-mirrors-baseline.txt"
)
LIVE_INSTRUCTIONS = ROOT / ".specify" / "instructions.md"
GENERATE_INSTRUCTIONS = ROOT / "scripts" / "bash" / "generate-instructions.sh"

#: A-13 / T-001 byte ceilings.
SECTION_CAP_BYTES = 1500
TOTAL_CAP_BYTES = 40960

DRIFT_LINE_RE = re.compile(r"^(MISS|DIFF\[projected\]|DIFF|ORPHAN)\s+(\S+)$", re.M)
BUDGET_RE = re.compile(r"^INSTRUCTIONS_BUDGET_BYTES=(\d+)$", re.M)


def run_engine(script: Path, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(ROOT),
    )


def drift_members(text: str) -> set[str]:
    return {f"{match.group(1)} {match.group(2)}" for match in DRIFT_LINE_RE.finditer(text)}


def raw_section(text: str, token: str = "Decision Items") -> str | None:
    """One H2 section heading line included, up to the next H2 (byte comparison unit)."""
    lines = text.splitlines(keepends=True)
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and token in line:
            start = index
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "".join(lines[start:end])


def test_mirror_and_copy_closure() -> None:
    """C-506: mirrors/copies converge with no NEW drift, and the two byte budgets hold."""
    check = run_engine(SYNC_MIRRORS, "--check")
    assert check.returncode == 0, (
        f"sync-mirrors --check exited {check.returncode}: {check.stdout[-3000:]}"
    )
    baseline = drift_members(read(MIRROR_BASELINE))
    current = drift_members(check.stdout)
    assert current - baseline == set(), (
        f"NEW mirror drift members against the baseline: {sorted(current - baseline)}"
    )

    regen = run_engine(REGEN_COPIES, "--check")
    assert regen.returncode == 0, (
        f"regen-command-copies --check exited {regen.returncode}: {regen.stdout[-2000:]}"
    )

    template_section = raw_section(read(INSTRUCTION_TEMPLATE))
    live_section = raw_section(read(LIVE_INSTRUCTIONS))
    assert template_section, "the instruction template carries no Decision Items section"
    assert template_section == live_section, (
        "the template and the generated live file disagree on the Decision Items section"
    )
    assert len(template_section.encode("utf-8")) <= SECTION_CAP_BYTES, (
        f"the section is {len(template_section.encode('utf-8'))} B, over the "
        f"{SECTION_CAP_BYTES} B ceiling"
    )

    generator = read(GENERATE_INSTRUCTIONS)
    budget = BUDGET_RE.search(generator)
    assert budget, "the generator declares no INSTRUCTIONS_BUDGET_BYTES"
    assert int(budget.group(1)) == TOTAL_CAP_BYTES, (
        f"the declared budget is {budget.group(1)}, expected the raised {TOTAL_CAP_BYTES}"
    )
    live_bytes = LIVE_INSTRUCTIONS.stat().st_size
    assert live_bytes < TOTAL_CAP_BYTES, (
        f"the live instructions are {live_bytes} B, not under the {TOTAL_CAP_BYTES} B budget"
    )


def test_client_init_receives_section(tmp_path: Path) -> None:
    """SC-010: an empty client project initialized today receives the section and its rules."""
    project = tmp_path / "fresh-client"
    project.mkdir()
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src") + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    init = subprocess.run(
        [
            sys.executable,
            "-c",
            "from specify_cli import main; main()",
            "init",
            "--here",
            "--ai",
            "qoder",
            "--script",
            "sh",
            "--no-git",
        ],
        cwd=str(project),
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    assert init.returncode == 0, (
        f"specify init failed (rc={init.returncode})\n"
        f"stdout:\n{init.stdout[-3000:]}\nstderr:\n{init.stderr[-3000:]}"
    )

    delivered = raw_section(
        (project / ".specify" / "templates" / "instructions-template.md").read_text(
            encoding="utf-8"
        )
    )
    assert delivered, "the initialized project's instruction template lacks the section"

    generated = subprocess.run(
        ["bash", ".specify/scripts/bash/generate-instructions.sh"],
        cwd=str(project),
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    assert generated.returncode == 0, (
        f"the client instruction generator failed (rc={generated.returncode})\n"
        f"{generated.stdout[-2000:]}\n{generated.stderr[-2000:]}"
    )

    live = raw_section(
        (project / ".specify" / "instructions.md").read_text(encoding="utf-8")
    )
    assert live, "the generated client instructions lack the Decision Items section"
    flat = norm(live)
    assert "full name" in flat and "abbreviation" in flat, (
        "the client section does not carry the full-name production rule"
    )
    for token in SAME_NAME_PINS:
        assert token in flat, f"the client section does not carry {token!r}"
    assert len(live.encode("utf-8")) <= SECTION_CAP_BYTES, (
        f"the client section is {len(live.encode('utf-8'))} B, over the ceiling"
    )

    per_tool = project / "QODER.md"
    assert per_tool.is_file(), "the init workspace carries no per-tool instruction copy"
    assert raw_section(per_tool.read_text(encoding="utf-8")), (
        "the per-tool instruction copy does not carry the section"
    )
