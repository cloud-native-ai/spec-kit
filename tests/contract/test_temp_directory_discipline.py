"""Contract tests for the temporary-directory discipline.

Guards the house pattern:
  * ``shared/guidelines/temp-directory-discipline.md`` — owner (+ runtime mirror)
  * ``templates/instructions-template.md`` — ambient section (+ mirror)
  * ``scripts/python/scan-temp-usage.py`` — deterministic scanner
  * ``templates/gitignore-specify-template`` — repo-local ignore coverage

Wording safety matters here: the new owner document and ambient section live in
the confirmation-gate scanner's surface, whose budget headroom is zero, so any
blocking-confirmation literal in them would add a gate.
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
DOC = ROOT / "shared" / "guidelines" / "temp-directory-discipline.md"
DOC_LINK = "shared/guidelines/temp-directory-discipline.md"
TEMPLATE = ROOT / "templates" / "instructions-template.md"
MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"
LIVE = ROOT / ".specify" / "instructions.md"
GITIGNORE_TEMPLATE = ROOT / "templates" / "gitignore-specify-template"
IGNORE_PATTERNS = ROOT / "shared" / "constants" / "ignore-patterns.md"
SCANNER = ROOT / "scripts" / "python" / "scan-temp-usage.py"
GATE_SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

HEADING = "## Temporary Directory Discipline"

FORBIDDEN = (
    "spec-kit", "specify-cli", "specify_cli", "cloud-native-ai",
    "Feature 0", ".specify/specs/0",
)

# Detail that must stay in the owner document, not be inlined into the ambient section.
OWNER_ONLY_MARKERS = (
    "| 场景 | 落点 | 忽略要求 |",
    "## 3. 写入前检查",
    "## 5. 例外",
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
    assert "临时目录" in opening, "the owner doc must name what it owns"
    for token in (
        "~/tmp", ".specify/.tmp", "git check-ignore", "trap",
        "例外", "原子写", "容器内",
    ):
        assert token in body, f"owner doc missing required rule token: {token}"


def test_owner_doc_separates_gitignore_duties():
    body = read(DOC)
    assert "不在 git 仓库内,不适用 `.gitignore`" in body, (
        "the doc must say ~/tmp is outside any repo, so gitignore does not apply"
    )
    assert "`.tmp/` 规则匹配" in body, (
        "the doc must require the repo-local root to be matched by .specify/.gitignore"
    )


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


# --- gitignore coverage ---


def test_gitignore_and_ignore_patterns_cover_tmp():
    assert ".tmp/" in read(GITIGNORE_TEMPLATE), (
        "the init-managed .specify/.gitignore template must ignore .tmp/"
    )
    assert ".tmp/" in read(IGNORE_PATTERNS), (
        "the universal ignore-pattern reference must include .tmp/"
    )


# --- scanner ---


def test_scanner_real_tree_is_clean():
    result = subprocess.run(
        [sys.executable, str(SCANNER), "--summary"],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "temp-directory violations: 0" in result.stdout


def test_scanner_flags_violations(tmp_path: Path):
    (tmp_path / "shared").mkdir()
    (tmp_path / "shared" / "bad.md").write_text(
        "path: /tmp/foo\nrun: mktemp -d\n", encoding="utf-8"
    )
    result = subprocess.run(
        [sys.executable, str(SCANNER), "--root", str(tmp_path), "--json"],
        capture_output=True, text=True,
    )
    assert result.returncode == 2, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert len(payload["violations"]) == 2
    reasons = {reason for item in payload["violations"] for reason in item["reasons"]}
    assert "bare-system-temp" in reasons
    assert "mktemp-d" in reasons


def test_scanner_allows_sanctioned_roots(tmp_path: Path):
    (tmp_path / "shared").mkdir()
    (tmp_path / "shared" / "good.md").write_text(
        "echo ~/tmp/foo\n"
        "echo .specify/.tmp/foo\n"
        'mktemp -d "$ROOT/.specify/.tmp/run.XXXXXX"\n',
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(SCANNER), "--root", str(tmp_path), "--json"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["violations"] == []


def test_scanner_allowlist_rows_have_reasons():
    module = load_module(SCANNER, "_scan_temp_usage_allowlist")
    assert module.ALLOWLIST, "the allowlist must not be empty"
    assert all(reason.strip() for reason in module.ALLOWLIST.values()), (
        "every allowlist row must carry a reason"
    )
    assert DOC_LINK in module.ALLOWLIST, (
        "the owner document itself must be allowlisted (it quotes forbidden forms)"
    )


# --- wording safety ---


def test_new_surfaces_are_project_neutral_and_non_blocking():
    gate = load_module(GATE_SCANNER, "_scan_gates_temp_discipline")
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
