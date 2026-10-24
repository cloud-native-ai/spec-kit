"""Contract tests for the knowledge-recording & promotion discipline.

Owner: ``shared/guidelines/knowledge-promotion.md``. The ambient section is
``templates/instructions-template.md`` § ``## Knowledge Recording & Promotion``.

The end-to-end test proves the evidence convention works with the existing
memory engine unchanged: two ``session`` entries sharing an ASCII ``key:`` tag
are both returned by a tag recall.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "shared" / "guidelines" / "knowledge-promotion.md"
DOC_LINK = "shared/guidelines/knowledge-promotion.md"
ARR = ROOT / "shared" / "guidelines" / "ask-record-repeat.md"
TEMPLATE = ROOT / "templates" / "instructions-template.md"
MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"
LIVE = ROOT / ".specify" / "instructions.md"
MEMORY_RECORD = ROOT / "skills" / "internal" / "memory-record" / "SKILL.md"
MEMORY_RECALL = ROOT / "skills" / "internal" / "memory-recall" / "SKILL.md"
MEMORY_DOC = ROOT / "docs" / "reference" / "skills" / "memory.md"
ENGINE = ROOT / "scripts" / "python" / "memory-utils.py"
GATE_SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

HEADING = "## Knowledge Recording & Promotion"

FORBIDDEN = (
    "spec-kit", "specify-cli", "specify_cli", "cloud-native-ai",
    "Feature 0", ".specify/specs/0",
)

OWNER_ONLY_MARKERS = (
    "## 1. 记录义务",
    "## 2. 强调升级",
    "user-emphasis",
    "key:<ascii-slug>",
)


def read(path: Path) -> str:
    assert path.is_file(), f"missing file: {path}"
    return path.read_text(encoding="utf-8")


def section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == heading), None)
    assert start is not None, f"section heading {heading!r} not found"
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## ") or lines[i].startswith("# "):
            end = i
            break
    return "\n".join(lines[start:end])


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# --- owner document ---


def test_owner_doc_declares_ownership_and_scope():
    body = read(DOC)
    opening = "\n".join(body.splitlines()[:6])
    assert ("单一真源" in opening or "唯一真源" in opening
            or "single source of truth" in opening.lower()), (
        "the owner doc must declare itself the single source of truth in its opening lines"
    )
    assert "知识" in opening, "the owner doc must name what it owns"


def test_owner_doc_covers_recording_duty():
    body = read(DOC)
    for token in (
        "不可从项目状态推导", "memory-record", "memory-recall",
        "ask-record-repeat.md", "--source", "MUST NOT 伪造 source",
    ):
        assert token in body, f"owner doc missing recording-duty token: {token}"


def test_owner_doc_covers_promotion_threshold_and_evidence():
    body = read(DOC)
    for token in (
        "user-emphasis", "key:<ascii-slug>", "any-of", "第 2 次强调",
        "主流程", "owner 文档", "常驻指令章节", "守卫", "执行面",
        "只写文档、只写 memory 不算升格",
    ):
        assert token in body, f"owner doc missing promotion token: {token}"
    assert "ASCII" in body, "the evidence convention must require ASCII keys"
    assert "中文 key" in body, "the doc must warn that Chinese keys are not retrievable"


def test_owner_doc_has_neighbor_boundaries():
    body = read(DOC)
    for token in ("fast-fail.md", "self-improvement.md", "improve-skills", "code-review"):
        assert token in body, f"owner doc missing boundary with {token}"


# --- ambient section ---


def test_template_and_mirror_carry_section_and_pointer():
    for label, path in (("template", TEMPLATE), ("mirror", MIRROR)):
        text = read(path)
        assert re.findall(r"(?m)^## .+$", text).count(HEADING) == 1, (
            f"{HEADING!r} must appear exactly once in the {label}"
        )
        assert DOC_LINK in section(text, HEADING), (
            f"the {label} section must carry the owner pointer"
        )


def test_live_instructions_carry_section_and_pointer():
    text = read(LIVE)
    assert HEADING in re.findall(r"(?m)^## .+$", text), (
        "live instructions must carry the injected section (run generate-instructions.sh)"
    )
    assert DOC_LINK in section(text, HEADING)


def test_section_is_pointer_shaped():
    body = section(read(TEMPLATE), HEADING)
    for marker in OWNER_ONLY_MARKERS:
        assert marker not in body, (
            f"the ambient section inlines owner detail {marker!r}; keep it a pointer"
        )


# --- consumers point at the owner ---


def test_ask_record_repeat_points_to_the_owner():
    assert DOC_LINK in read(ARR), (
        "ask-record-repeat.md must delegate the promotion threshold to its owner"
    )


def test_memory_consumers_point_at_the_owner():
    record = read(MEMORY_RECORD)
    assert DOC_LINK in record
    assert "user-emphasis" in record and "key:<ascii-slug>" in record

    recall = read(MEMORY_RECALL)
    assert DOC_LINK in recall
    assert "key:<ascii-slug>" in recall

    assert DOC_LINK in read(MEMORY_DOC), (
        "the memory reference doc must point at the promotion owner"
    )


# --- the evidence convention works with the existing engine ---


def test_memory_tag_convention_counts_two_occurrences(tmp_path: Path):
    workspace = tmp_path / "ws"
    workspace.mkdir()

    for index in range(2):
        result = subprocess.run(
            [
                sys.executable, str(ENGINE),
                "--workspace-root", str(workspace),
                "--action", "record",
                "--scope", "session",
                "--source", "/speckit.requirements",
                "--title", f"User emphasis {index}",
                "--tags", "user-emphasis,key:temp-dirs",
                "--content", "User restated the same point.",
            ],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stderr

    result = subprocess.run(
        [
            sys.executable, str(ENGINE),
            "--workspace-root", str(workspace),
            "--action", "recall",
            "--scope", "session",
            "--tags", "key:temp-dirs",
            "--format", "json",
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["count"] == 2, payload
    assert all("key:temp-dirs" in (item.get("tags") or [])
               for item in payload["matches"])


# --- wording safety ---


def test_new_surfaces_are_project_neutral_and_non_blocking():
    gate = load_module(GATE_SCANNER, "_scan_gates_knowledge_promotion")
    surfaces = (
        ("owner doc", read(DOC)),
        ("ambient section", section(read(TEMPLATE), HEADING)),
    )
    for name, text in surfaces:
        lowered = text.lower()
        for token in FORBIDDEN:
            assert token.lower() not in lowered, f"project token {token!r} leaked into {name}"
        hits = [m.group(0) for line in text.splitlines()
                for m in gate.BLOCKING_RE.finditer(line)]
        assert not hits, f"{name} trips BLOCKING_PATTERNS: {hits}"
