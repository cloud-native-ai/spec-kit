"""Structural contract tests for the /speckit.humanize command surface.

**Ownership, part 1 — feature 062.** The ``test_c01..c10`` block owns the C-1..C-10
structural assertions of
``.specify/specs/062-humanize-command/contracts/command-surface.md`` — thin-entry
template shape, single-skill delegation, skill frontmatter + self-sufficiency,
generated per-tool copies, docs page content points, registry rows, the skill-side
probe unit + compiled Wrap-up face (Simple command ⇒ no command-side wrap-up),
zero-new-runtime-surface, the two downstream pinned tests' updated literals, and the
detector-honesty wording scan.

**Ownership, part 2 — feature 079 (run mode).** The ``test_ip* / test_ex* / test_rp* /
test_wc*`` block owns the 079 clauses assigned to this file by
``.specify/specs/080-humanize-run-output/tasks.md`` § Contract Coverage Map: IP-01…IP-10
and EX-01…EX-05 (US1 implementation rows T006–T008), the tests-side frontier of the
later US1 rows — EX-06…EX-10 (T009/T010), RP-01…RP-04 (T011) and WC-01…WC-04 (T012) —
and the US2 group RP-05…RP-18 (T013, landed before its implementation rows T014–T018).
Function names are the contract traceability names verbatim, so T036's
``test_wc12_clause_test_map_is_total`` can claim each clause. A group whose
implementation row has not run yet is this file's recorded red-first frontier; no
assertion here is allowed to pass by weakening the contract.

Red-Green discipline (Constitution IV, template-only form): assertions land BEFORE the
artifacts they describe; red = the asserted section/anchor/fixture value is not there
yet. Shared-String literals below are pinned copies of the owner tables in each
feature's requirements.md § Shared Strings — a legitimate duplicate under the
drift-detection rule of ``.specify/shared/guidelines/one-source-of-truth.md``.

Red-Green discipline (Constitution IV, template-only form): this file landed BEFORE
the artifacts exist; red = an asserted path/literal is not there yet. Shared-String
literals below are pinned copies of the owner table in
``.specify/specs/062-humanize-command/requirements.md`` § Shared Strings — a
legitimate duplicate under the drift-detection rule of
``.specify/shared/guidelines/one-source-of-truth.md``.

C-4's baseline zero-drift leg (``regen-command-copies.py --check`` vs
``notes/baseline-regen-check.txt``) and C-9's full-suite ``comm -13`` leg are
runtime gates recorded in ``verification.md``, not in-test assertions.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]

TEMPLATE = REPO_ROOT / "templates" / "commands" / "humanize.md"
SKILL_SRC = REPO_ROOT / "skills" / "external" / "humanize" / "SKILL.md"
SKILL_RUNTIME = REPO_ROOT / ".specify" / "skills" / "humanize" / "SKILL.md"
DOCS_PAGE = REPO_ROOT / "docs" / "reference" / "commands" / "humanize.md"
COPIES = [
    REPO_ROOT / ".claude" / "commands" / "speckit.humanize.md",
    REPO_ROOT / ".github" / "prompts" / "speckit.humanize.prompt.md",
    REPO_ROOT / ".opencode" / "command" / "speckit.humanize.md",
    REPO_ROOT / ".qoder" / "commands" / "speckit.humanize.md",
]
REGISTRY = REPO_ROOT / ".specify" / "memory" / "features.md"
FEATURE_DETAILS = REPO_ROOT / ".specify" / "memory" / "features" / "062.md"
PROBE_DEFS = REPO_ROOT / "shared" / "definitions" / "probe-definitions.md"
CONTRACT_027 = (
    REPO_ROOT / ".specify" / "specs" / "027-feedback-mechanism"
    / "contracts" / "command-classification.md"
)
BASELINE_FAILED = (
    REPO_ROOT / ".specify" / "specs" / "062-humanize-command"
    / "notes" / "baseline-failed-tests.txt"
)

# Shared Strings (pinned from requirements.md § Shared Strings).
STR_001 = "/speckit.humanize"
STR_002_VALUES = ("professional", "humorous", "empathetic", "colloquial")
STR_003_EXTS = (".md", ".markdown", ".txt")
STR_004_FLAGS = ("--tone", "--audience", "--file", "--inline", "--output", "--force")

DELEGATION_PATH = ".specify/skills/humanize/SKILL.md"
SKILL_ID_LITERAL = f'skill_id: "<SKILL:{DELEGATION_PATH}>"'

# Thinness: behavioral-detail keywords a thin entry must never restate
# (C-1: the FR-003..FR-006 workflow lives in the skill, not the template).
THIN_FORBIDDEN_DETAIL = ("rubric", "评审记录", "评分表", "盲评")


def _frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[:end] if end != -1 else ""


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# C-1 — thin entry: frontmatter, sections, Simple shape, no workflow restate
# ---------------------------------------------------------------------------

def test_c01_thin_entry_shape():
    assert TEMPLATE.is_file(), f"thin command template missing: {TEMPLATE}"
    text = _read(TEMPLATE)
    fm = _frontmatter(text)
    assert "description:" in fm, "template frontmatter lacks description (trigger words)"
    assert "short-description:" in fm, "template frontmatter lacks short-description"
    assert "scripts:" not in fm, "template must not declare a scripts: block (Simple)"
    for section in ("## User Input", "## Glossary", "## Handoffs"):
        assert section in text, f"template body lacks {section}"
    assert "$ARGUMENTS" in text, "template lacks $ARGUMENTS wiring"
    assert "user-input-protocol" in text, "template lacks User Input Protocol reference"
    assert "FR-018" in text, "template lacks FR-018 call-syntax declaration pointer"
    assert "--" in text, "template lacks the -- option-termination declaration"
    for flag in STR_004_FLAGS:
        assert flag in text, f"template lacks call-syntax option {flag} (STR-004)"
    # Simple-class shape: no command-side wrap-up / feedback step at all.
    assert "## Wrap-up" not in text, "Simple command must not carry ## Wrap-up"
    assert "feedback-utils.py" not in text, "Simple command must not carry feedback step"
    assert "probe-utils.py" not in text, "Simple command must not carry a wrap-up face"
    assert STR_001 in text, f"template lacks the command identity literal {STR_001}"
    # Zero restatement of the FR-003..FR-006 behavioral details (C-1 thinness).
    body_lines = [ln for ln in text.splitlines() if not ln.startswith("|")]
    assert len(body_lines) <= 120, (
        f"template body has {len(body_lines)} non-table lines — thin entry exceeded"
    )
    lowered = text.lower()
    for word in THIN_FORBIDDEN_DETAIL:
        assert word not in lowered and word not in text, (
            f"template restates behavioral workflow detail ({word!r}) — belongs to the skill"
        )


# ---------------------------------------------------------------------------
# C-2 — exactly one skill delegation, command→skill direction only
# ---------------------------------------------------------------------------

def test_c02_single_skill_delegation():
    text = _read(TEMPLATE)
    skill_mentions = text.count("SKILL.md")
    assert skill_mentions == 1, (
        f"delegation must name exactly one skill (found {skill_mentions} SKILL.md mentions)"
    )
    assert DELEGATION_PATH in text, f"template must delegate to {DELEGATION_PATH}"
    # No back-reference: the skill body never points at the command template.
    skill_text = _read(SKILL_SRC)
    assert "templates/commands/humanize.md" not in skill_text, (
        "skill body must not back-reference the command template (C-2 direction)"
    )


# ---------------------------------------------------------------------------
# C-3 — skill frontmatter + self-sufficient body
# ---------------------------------------------------------------------------

def test_c03_skill_frontmatter_and_self_sufficient():
    assert SKILL_SRC.is_file(), f"external skill missing: {SKILL_SRC}"
    text = _read(SKILL_SRC)
    fm = _frontmatter(text)
    assert "name: humanize" in fm, "skill frontmatter lacks name: humanize"
    assert "classification: external" in fm, "skill frontmatter lacks classification: external"
    assert SKILL_ID_LITERAL in fm, f"skill frontmatter lacks {SKILL_ID_LITERAL}"
    assert "description:" in fm, "skill frontmatter lacks description with trigger words"
    # Self-sufficiency: inline minimal operational facts a bare host needs.
    for value in STR_002_VALUES:
        assert value in text, f"skill body lacks tone value {value}"
    for flag in STR_004_FLAGS:
        assert flag in text, f"skill body lacks call option {flag}"
    assert "保真" in text, "skill body lacks the fidelity floor (FR-007)"
    assert "按数据" in text or "数据处理" in text, (
        "skill body lacks the data-not-instructions declaration (FR-029)"
    )
    for ext in STR_003_EXTS:
        assert ext in text, f"skill body lacks supported extension {ext} (FR-019)"


# ---------------------------------------------------------------------------
# C-4 — generated per-tool copies (existence + generated header)
# ---------------------------------------------------------------------------

def test_c04_generated_copies_present():
    for copy in COPIES:
        assert copy.is_file(), f"generated copy missing: {copy}"
        text = _read(copy)
        assert "AUTO-GENERATED" in text or "regen-command-copies" in text, (
            f"{copy} lacks the do-not-hand-edit generated header"
        )
        assert STR_001 in text, f"{copy} lacks the command identity literal"


# ---------------------------------------------------------------------------
# C-5 — docs page content points
# ---------------------------------------------------------------------------

def test_c05_docs_page_content():
    assert DOCS_PAGE.is_file(), f"docs page missing: {DOCS_PAGE}"
    text = _read(DOCS_PAGE)
    assert "内联" in text and "文件" in text, "docs page lacks input-form coverage"
    assert "不写入" in text, "docs page lacks the default no-file-write statement"
    for value in STR_002_VALUES:
        assert value in text, f"docs page lacks tone value {value}"
    assert "FR-007" in text, "docs page lacks the fidelity boundary pointer (FR-007)"
    assert "FR-029" in text, "docs page lacks the data-not-instructions pointer (FR-029)"
    assert "不承诺" in text, "docs page lacks the detector no-promise statement (SC-009)"


# ---------------------------------------------------------------------------
# C-6 — feature registry rows resolve
# ---------------------------------------------------------------------------

def test_c06_registry_rows_resolve():
    assert FEATURE_DETAILS.is_file(), f"feature details file missing: {FEATURE_DETAILS}"
    assert REGISTRY.is_file(), f"feature registry missing: {REGISTRY}"
    reg = _read(REGISTRY)
    row = [ln for ln in reg.splitlines() if "062-humanize-command" in ln]
    assert row, "registry lacks a 062-humanize-command row"
    assert any(".specify/specs/062-humanize-command/requirements.md" in ln for ln in row), (
        "062 registry row does not point at its requirements.md"
    )


# ---------------------------------------------------------------------------
# C-7 — skill-side probe unit + compiled Wrap-up face; no command unit (Simple)
# ---------------------------------------------------------------------------

def test_c07_skill_probe_unit_and_compiled_wrapup():
    defs = _read(PROBE_DEFS)
    unit_row = [ln for ln in defs.splitlines()
                if ln.startswith("| skill-humanize-wrapup ")]
    assert unit_row, "probe-definitions lacks the skill-humanize-wrapup unit row"
    assert any("skill:humanize" in ln and "wrap-up" in ln for ln in unit_row), (
        "skill-humanize-wrapup unit row does not bind skill:humanize at wrap-up"
    )
    assert any("h-docs-sync-eval" in ln and "skill-humanize-wrapup" in ln
               for ln in defs.splitlines()), (
        "skill-humanize-wrapup lacks the h-docs-sync-eval @point:wrap-up binding"
    )
    # Simple class: no command-side unit row was added.
    assert not any(ln.startswith("| /speckit.humanize ") for ln in defs.splitlines()), (
        "Simple command must not get a probe command unit"
    )
    # The compiled face lands in the skill (source and synced runtime copy).
    for path in (SKILL_SRC, SKILL_RUNTIME):
        text = _read(path)
        assert "## Wrap-up" in text, f"{path} lacks the compiled ## Wrap-up face"
        assert "AUTO-GENERATED by probe-utils.py" in text, (
            f"{path} Wrap-up face must be compiled, not hand-written"
        )
        assert "feedback-utils.py" in text, (
            f"{path} Wrap-up face lacks the feedback record invocation"
        )


# ---------------------------------------------------------------------------
# C-8 — zero new runtime surface; existing distribution consumed as-is
# ---------------------------------------------------------------------------

def test_c08_no_runtime_surface():
    for path in (REPO_ROOT / "src" / "specify_cli", REPO_ROOT / "scripts"):
        for py in path.rglob("*.py"):
            if "test" in py.name:
                continue
            assert "humanize" not in py.read_text(encoding="utf-8", errors="replace").lower() or py.name == "conftest.py", (
                f"unexpected humanize runtime surface in {py} (C-8: no new runtime)"
            )
    pyproject = _read(REPO_ROOT / "pyproject.toml")
    assert "humanize" not in pyproject.lower(), "no new dependency may mention humanize"
    assert "generate_commands" in _read(REPO_ROOT / "src" / "specify_cli" / "__init__.py"), (
        "existing generate_commands distribution mechanism must stay untouched"
    )
    for engine in ("scripts/python/regen-command-copies.py",
                   "scripts/python/sync-mirrors.py"):
        assert (REPO_ROOT / engine).is_file(), f"distribution engine missing: {engine}"


# ---------------------------------------------------------------------------
# C-9 — baseline + the two downstream pinned tests updated in the same batch
# ---------------------------------------------------------------------------

def _import_test_module(name: str):
    path = REPO_ROOT / "tests" / "contract" / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_c09_baseline_no_new_failures():
    assert BASELINE_FAILED.is_file(), (
        f"frozen failed-test baseline missing: {BASELINE_FAILED}"
    )
    contract = _read(CONTRACT_027)
    row = [ln for ln in contract.splitlines() if ln.startswith("| `humanize`")]
    assert row, "027 classification table lacks a humanize row"
    assert any("**Simple**" in ln for ln in row), "humanize must be classified Simple"
    result = [ln for ln in contract.splitlines() if "**Result**" in ln]
    assert result and "23 complex" in result[0] and "4 simple" in result[0], (
        "027 Result line must read 23 complex / 4 simple after humanize"
    )
    feedback_mod = _import_test_module("test_feedback_command_classification.py")
    assert "humanize" in feedback_mod.SIMPLE_COMMANDS, (
        "test_feedback_command_classification must derive humanize as Simple"
    )
    guards_mod = _import_test_module("test_skill_layer_visibility_guards.py")
    assert "humanize" in guards_mod.EXTERNAL_SKILLS, (
        "test_skill_layer_visibility_guards EXTERNAL_SKILLS must include humanize"
    )


# ---------------------------------------------------------------------------
# C-10 — detector-honesty wording across all static faces
# ---------------------------------------------------------------------------

DETECTOR_TERMS = ("检测器", "detector", "AI 内容检测")
FORBIDDEN_DETECTOR_CLAIMS = (
    "绕过检测", "规避检测", "bypass detection", "undetectable",
    "不被 AI 检测", "保证通过检测", "100% 通过",
)
HONEST_MARKERS = ("不承诺", "不保证", "无法保证", "不能保证")


def test_c10_detector_honesty_wording():
    surfaces = [p for p in (TEMPLATE, SKILL_SRC, SKILL_RUNTIME, DOCS_PAGE, *COPIES)
                if p.is_file()]
    assert surfaces, "no humanize surfaces exist yet (expected red before implementation)"
    for path in surfaces:
        lines = _read(path).splitlines()
        for i, line in enumerate(lines):
            if any(term in line for term in DETECTOR_TERMS):
                window = "\n".join(lines[i:i + 2])
                assert any(marker in window for marker in HONEST_MARKERS), (
                    f"{path}:{i + 1} mentions a detector without a no-promise statement "
                    f"(C-10/SC-009): {line.strip()[:80]!r}"
                )
            lowered = line.lower()
            for claim in FORBIDDEN_DETECTOR_CLAIMS:
                assert claim.lower() not in lowered, (
                    f"{path}:{i + 1} carries a forbidden detector claim {claim!r}"
                )


# ===========================================================================
# 079 — Humanize Run Output (US1 clause block)
#
# Clause groups and their owners:
#   IP-01…IP-10  run-mode § Parse / § Mode Routing / § Migration Hint (T006/T007)
#   EX-01…EX-05  run-mode § Dispatch (T008)
#   EX-06…EX-10  run-mode § Payload / § Envelope (T009/T010)   — later frontier
#   RP-01…RP-04  report-shape § Metadata Block / § Sections (T011) — later frontier
#   WC-01…WC-04  templates/commands/humanize.md (T012)          — later frontier
#
# The fixture set under tests/fixtures/humanize/run/ is the second half of the
# contract: each envelope is a "message, not a file" sample (E5) whose fields a
# clause test can evaluate deterministically.
# ===========================================================================

RUN_MODE_DOC = SKILL_SRC.parent / "references" / "run-mode.md"
REPORT_SHAPE_DOC = SKILL_SRC.parent / "references" / "report-shape.md"
RUN_FIXTURES = REPO_ROOT / "tests" / "fixtures" / "humanize" / "run"
GATES_SCANNER = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

# Pinned literals (owner: requirements.md § Shared Strings / A4).
MIGRATION_HINT = "已按指令执行；改写文本请用 --file/--inline"
FIVE_SECTIONS = (
    "## Conclusion",
    "## Key Changes",
    "## Evidence",
    "## Risks & Limits",
    "## Next Steps",
)
CARRIER_NATIVE = "mode: subagent"
CARRIER_DEGRADED = "mode: in-session-degraded"
TONE_VALUES = ("professional", "humorous", "empathetic", "colloquial")
PARSE_FIELDS = (
    "`tone`", "`audience`", "`file`", "`inline`", "`output`", "`force`",
    "`instruction_text`", "`mode`", "`reject_code`",
)


def _section_body(text: str, heading: str) -> str:
    """Exact-H2 section body, up to the next H2 (or EOF). Fails when absent."""
    lines = text.splitlines()
    start = next((i + 1 for i, ln in enumerate(lines) if ln.strip() == heading), None)
    assert start is not None, f"section {heading!r} missing"
    end = next((j for j in range(start, len(lines)) if lines[j].startswith("## ")),
               len(lines))
    return "\n".join(lines[start:end])


def _envelope_text(stem: str) -> str:
    path = RUN_FIXTURES / stem / "envelope.md"
    assert path.is_file(), f"run fixture envelope missing: {path}"
    return _read(path)


def _envelope(stem: str) -> dict:
    data = yaml.safe_load(_frontmatter(_envelope_text(stem)))
    assert isinstance(data, dict), f"{stem}/envelope.md frontmatter is not a mapping"
    for field in ("status", "final_output", "products", "evidence", "failures",
                  "blocked_at", "anomaly_line"):
        assert field in data, f"{stem}/envelope.md lacks E5 field {field!r}"
    return data


# ---------------------------------------------------------------------------
# IP-01 .. IP-04 — § Parse (T006)
# ---------------------------------------------------------------------------

def test_ip01_parse_is_pure_syntax():
    assert RUN_MODE_DOC.is_file(), f"run-mode reference missing: {RUN_MODE_DOC}"
    parse = _section_body(_read(RUN_MODE_DOC), "## Parse")
    for flag in ("--tone", "--audience", "--file", "--inline", "--output", "--force"):
        assert flag in parse, f"§ Parse lacks option {flag} (IP-01)"
    for anchor in (
        "只出现在指令之前",
        "`--` 终止选项解析",
        "第一个不可识别为选项的 token 即指令起点",
        "纯语法过程",
        "同样的 argv 得到同样的结果",
        "MUST NOT 读取指令内容来猜测意图",
    ):
        assert anchor in parse, f"§ Parse lacks the determinism anchor {anchor!r} (IP-01)"


def test_ip02_instruction_is_verbatim():
    parse = _section_body(_read(RUN_MODE_DOC), "## Parse")
    for anchor in (
        "逐字",
        "含换行与引号",
        "MUST NOT 改写、摘要或规范化",
        "裸文本 MUST NOT 再被解释为待改写内容",
    ):
        assert anchor in parse, f"§ Parse lacks the verbatim anchor {anchor!r} (IP-02)"
    nested = RUN_FIXTURES / "nested" / "instruction.txt"
    assert nested.is_file(), f"nested instruction fixture missing: {nested}"
    assert "speckit.humanize" in _read(nested).lower(), (
        "nested instruction fixture must carry the closed invocation token (IP-13)"
    )


def test_ip03_option_domain_unchanged():
    parse = _section_body(_read(RUN_MODE_DOC), "## Parse")
    for value in TONE_VALUES:
        assert value in parse, f"§ Parse lacks tone value {value} (IP-03)"
    for anchor in (
        "空字符串或纯空白",
        "未提供",
        "`--force`",
        "覆盖",
        "`--output` 的写入语义按模式分属",
        "FR-024",
    ):
        assert anchor in parse, f"§ Parse lacks the option-semantics anchor {anchor!r} (IP-03)"


def test_ip04_parse_fields_closed():
    parse = _section_body(_read(RUN_MODE_DOC), "## Parse")
    for field in PARSE_FIELDS:
        assert field in parse, f"§ Parse lacks the E2 field {field} (IP-04)"
    assert "`mode` 只有 `run` / `content` / `reject` 三值" in parse, (
        "§ Parse must close the mode domain to run / content / reject (IP-04)"
    )


# ---------------------------------------------------------------------------
# IP-05 .. IP-10 — § Mode Routing + § Migration Hint (T007)
# ---------------------------------------------------------------------------

def _routing_rows() -> list[list[str]]:
    routing = _section_body(_read(RUN_MODE_DOC), "## Mode Routing")
    rows = [ln for ln in routing.splitlines() if re.match(r"^\|\s*[1-4]\s*\|", ln)]
    return [[cell.strip() for cell in ln.strip("|").split("|")] for ln in rows]


def test_ip05_routing_table_order():
    rows = _routing_rows()
    assert len(rows) == 4, f"§ Mode Routing must carry the four-row closed table, got {len(rows)}"
    expected = (
        ("有", "非空", "both-sources-and-instruction"),
        ("有", "空", "content"),
        ("无", "非空", "run"),
        ("无", "空", "no-input"),
    )
    for cells, (source, instruction, verdict) in zip(rows, expected):
        assert cells[1] == source, f"row {cells[0]} content-source cell is {cells[1]!r} (IP-05)"
        assert cells[2] == instruction, f"row {cells[0]} instruction cell is {cells[2]!r} (IP-05)"
        assert verdict in cells[3], f"row {cells[0]} verdict is {cells[3]!r} (IP-05)"
    routing = _section_body(_read(RUN_MODE_DOC), "## Mode Routing")
    assert "顺序不可调换" in routing, "§ Mode Routing must declare the evaluation order fixed (IP-05)"


def test_ip06_source_and_instruction_rejected():
    routing = _section_body(_read(RUN_MODE_DOC), "## Mode Routing")
    for anchor in (
        "点名两者",
        "源名与指令前缀",
        "MUST NOT 走「内容优先」或「指令优先」",
        "该拒绝优先于其他路由判断",
    ):
        assert anchor in routing, f"§ Mode Routing lacks the both-sources anchor {anchor!r} (IP-06)"


def test_ip07_no_input_usage_and_hint():
    routing = _section_body(_read(RUN_MODE_DOC), "## Mode Routing")
    for anchor in ("用法行", "支持的内容源", "迁移提示整句", "`--file`", "`--inline`"):
        assert anchor in routing, f"§ Mode Routing lacks the no-input anchor {anchor!r} (IP-07)"
    assert MIGRATION_HINT in _read(RUN_MODE_DOC), (
        "run-mode reference must carry the pinned migration-hint literal (IP-07/IP-09)"
    )


def test_ip08_empty_source_rejected():
    routing = _section_body(_read(RUN_MODE_DOC), "## Mode Routing")
    assert "`empty-input`" in routing, "§ Mode Routing lacks the empty-input reject code (IP-08)"
    assert "空内容不是内容" in routing, "§ Mode Routing must state that empty content is not content (IP-08)"
    assert "MUST NOT 因「有一个内容源参数」而落进内容模式" in routing, (
        "§ Mode Routing must forbid falling into content mode on an empty source (IP-08)"
    )


def test_ip09_migration_hint_once():
    doc = _read(RUN_MODE_DOC)
    assert doc.count(MIGRATION_HINT) == 1, (
        f"the migration hint must appear exactly once in run-mode.md, found {doc.count(MIGRATION_HINT)}"
    )
    hint = _section_body(doc, "## Migration Hint")
    for anchor in ("运行模式且调用中**无**任何显式内容源", "内容模式与拒绝路径不输出该行"):
        assert anchor in hint, f"§ Migration Hint lacks the hint-scope anchor {anchor!r} (IP-09)"


def test_ip10_hint_placement():
    hint = _section_body(_read(RUN_MODE_DOC), "## Migration Hint")
    for anchor in (
        "载体标记行之后",
        "五个 H2 之前",
        "MUST NOT 构成第六节",
        "同一运行至多一行",
    ):
        assert anchor in hint, f"§ Migration Hint lacks the hint-placement anchor {anchor!r} (IP-10)"


# ---------------------------------------------------------------------------
# EX-01 .. EX-05 — § Dispatch (T008)
# ---------------------------------------------------------------------------

def test_ex01_exactly_one_dispatch():
    dispatch = _section_body(_read(RUN_MODE_DOC), "## Dispatch")
    for anchor in ("恰好一个", "顶层执行体", "一次调用两次派发", "先试一个再补一个"):
        assert anchor in dispatch, f"§ Dispatch lacks the exactly-one anchor {anchor!r} (EX-01)"
    success = _envelope("success")
    commands = [e for e in success["evidence"]
                if isinstance(e, dict) and e.get("kind") == "command"]
    assert len(commands) == 1, (
        f"success fixture must model exactly one top-level command evidence, got {len(commands)}"
    )


def test_ex02_run_agent_carrier_only():
    dispatch = _section_body(_read(RUN_MODE_DOC), "## Dispatch")
    for anchor in (
        "run-agent",
        "Run Mode",
        "MUST NOT 引入第二套派发机制",
        "MUST NOT 新建派发脚本",
        "私有会话 API",
    ):
        assert anchor in dispatch, f"§ Dispatch lacks the carrier anchor {anchor!r} (EX-02)"


def test_ex03_temporary_executor_no_agent_file():
    dispatch = _section_body(_read(RUN_MODE_DOC), "## Dispatch")
    for anchor in (
        "会话级临时执行体",
        ".specify/agents/",
        ".agent.md",
        "不占 Agent 席位",
        "不声明 SDD 执行席位",
        "磁盘上创建",
    ):
        assert anchor in dispatch, f"§ Dispatch lacks the temporary-executor anchor {anchor!r} (EX-03)"


def test_ex04_carrier_modes():
    dispatch = _section_body(_read(RUN_MODE_DOC), "## Dispatch")
    for anchor in ("`native`", "`in-session`", "独立 CLI 进程"):
        assert anchor in dispatch, f"§ Dispatch lacks the carrier-mode anchor {anchor!r} (EX-04)"
    assert "MUST NOT 被本命令使用" in dispatch, (
        "§ Dispatch must exclude the external CLI process mode (EX-04)"
    )


def test_ex05_marker_matches_carrier():
    dispatch = _section_body(_read(RUN_MODE_DOC), "## Dispatch")
    for anchor in (CARRIER_NATIVE, CARRIER_DEGRADED,
                   "MUST NOT 冒充", "MUST NOT 双写", "MUST NOT 漏写"):
        assert anchor in dispatch, f"§ Dispatch lacks the carrier-marker anchor {anchor!r} (EX-05)"
    assert CARRIER_NATIVE not in _envelope_text("degraded"), (
        "degraded fixture must not impersonate the native carrier (EX-05/EX-17)"
    )


# ---------------------------------------------------------------------------
# EX-06 .. EX-10 — § Payload / § Envelope (T009 / T010) — later frontier
# ---------------------------------------------------------------------------

def test_ex06_payload_six_items():
    payload = _section_body(_read(RUN_MODE_DOC), "## Payload")
    items = (
        "快速失败注入子句",
        "指令原文",
        "回传信封的字段与封闭取值",
        "不得撰写最终报告",
        "不得重试",
        "指令自身再调用本命令即拒绝并回传",
    )
    positions = [payload.find(item) for item in items]
    assert all(pos != -1 for pos in positions), (
        f"§ Payload lacks one of the six ordered items: {items}"
    )
    assert positions == sorted(positions), "§ Payload must carry the six items in contract order (EX-06)"


def test_ex07_payload_keeps_instruction_verbatim():
    payload = _section_body(_read(RUN_MODE_DOC), "## Payload")
    for anchor in ("MUST NOT 把指令改写成步骤清单", "MUST NOT 预先替指令挑选实现路径"):
        assert anchor in payload, f"§ Payload lacks the no-rewrite anchor {anchor!r} (EX-07)"


def test_ex08_payload_defers_to_instruction_gates():
    payload = _section_body(_read(RUN_MODE_DOC), "## Payload")
    for anchor in ("确认步骤与权限边界优先", "停在该步"):
        assert anchor in payload, f"§ Payload lacks the deferral anchor {anchor!r} (EX-08)"


def test_ex09_envelope_is_message():
    envelope = _section_body(_read(RUN_MODE_DOC), "## Envelope")
    for anchor in ("MUST NOT 以「写了报告文件」代替回传", "消息", "零写入"):
        assert anchor in envelope, f"§ Envelope lacks the message-not-file anchor {anchor!r} (EX-09)"
    reports = list(RUN_FIXTURES.rglob("report.md"))
    assert not reports, f"run fixtures must not model a report file: {reports}"


def test_ex10_missing_anomaly_line_blocks_consumption():
    envelope = _section_body(_read(RUN_MODE_DOC), "## Envelope")
    for anchor in ("缺显式异常行", "MUST NOT 被消费", "点名缺失项"):
        assert anchor in envelope, f"§ Envelope lacks the anomaly-line anchor {anchor!r} (EX-10)"
    for stem in ("success", "failure", "non-action", "needs-confirmation", "denied",
                 "degraded", "injection"):
        data = _envelope(stem)
        assert isinstance(data["anomaly_line"], str) and data["anomaly_line"].strip(), (
            f"{stem}/envelope.md must carry a non-empty anomaly_line (E5)"
        )


# ---------------------------------------------------------------------------
# RP-01 .. RP-04 — report-shape § Metadata Block / § Sections (T011) — frontier
# ---------------------------------------------------------------------------

def test_rp01_five_sections_in_order():
    assert REPORT_SHAPE_DOC.is_file(), f"report-shape reference missing: {REPORT_SHAPE_DOC}"
    text = _read(REPORT_SHAPE_DOC)
    positions = [text.find(heading) for heading in FIVE_SECTIONS]
    assert all(pos != -1 for pos in positions), "report-shape must name all five H2 sections (RP-01)"
    assert positions == sorted(positions), "the five H2 sections must appear in fixed order (RP-01)"
    for anchor in ("逐字", "不加编号", "不翻译", "缺任一小节即不合格"):
        assert anchor in text, f"report-shape lacks the section anchor {anchor!r} (RP-01)"


def test_rp02_metadata_block():
    text = _read(REPORT_SHAPE_DOC)
    for anchor in ("恰一条载体标记行", "迁移提示行", "MUST NOT 构成第六节"):
        assert anchor in text, f"report-shape lacks the metadata-block anchor {anchor!r} (RP-02)"
    assert CARRIER_NATIVE in text and CARRIER_DEGRADED in text, (
        "report-shape must pin both carrier markers (RP-02)"
    )


def test_rp03_main_session_writes_report():
    text = _read(REPORT_SHAPE_DOC)
    for anchor in ("报告由 humanize 主会话撰写", "执行体 MUST NOT 写最终报告", "以执行体身份的自述"):
        assert anchor in text, f"report-shape lacks the authorship anchor {anchor!r} (RP-03)"


def test_rp04_zero_write_default():
    text = _read(REPORT_SHAPE_DOC)
    for anchor in ("MUST NOT 写隐式副本", "MUST NOT 写到默认位置", "`--output`"):
        assert anchor in text, f"report-shape lacks the zero-write anchor {anchor!r} (RP-04)"


# ---------------------------------------------------------------------------
# WC-01 .. WC-04 — command template (T012) — frontier
# ---------------------------------------------------------------------------

def _blocking_re():
    spec = importlib.util.spec_from_file_location("scan_confirmation_gates", GATES_SCANNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.BLOCKING_RE


def test_wc01_template_declares_breaking_change():
    text = _read(TEMPLATE)
    for anchor in ("破坏性", "裸文本", "待执行指令", "--file", "--inline", "迁移"):
        assert anchor in text, f"template lacks the breaking-change anchor {anchor!r} (WC-01)"
    assert "$ARGUMENTS" in text, "the migration example must stay copy-pasteable from $ARGUMENTS (WC-01)"


def test_wc02_thin_entry_invariant():
    text = _read(TEMPLATE)
    fm = _frontmatter(text)
    assert "scripts:" not in fm, "template must not declare a scripts: block (WC-02)"
    assert "## Wrap-up" not in text, "template must not carry ## Wrap-up (WC-02)"
    assert text.count("SKILL.md") == 1, (
        f"template must name exactly one skill, found {text.count('SKILL.md')} (WC-02)"
    )
    for heading in FIVE_SECTIONS:
        assert heading not in text, f"template must not restate report section {heading!r} (WC-02)"
    assert "## Payload" not in text and "## Envelope" not in text, (
        "template must not copy the run-mode Step tables (WC-02)"
    )


def test_wc03_wiring_card_preserved():
    outline = _section_body(_read(TEMPLATE), "## Outline")
    for anchor in ("flow-class-definitions.md", "expression-gates.md", "不读取类别"):
        assert anchor in outline, f"template § Outline lost the 077 wiring card anchor {anchor!r} (WC-03)"


def test_wc04_no_blocking_literals():
    blocking = _blocking_re()
    hits = [(i + 1, ln) for i, ln in enumerate(_read(TEMPLATE).splitlines())
            if blocking.search(ln)]
    assert not hits, f"template carries blocking-gate literals (WC-04): {hits}"


# ---------------------------------------------------------------------------
# RP-05 .. RP-18 — report-shape § Conclusion … § Fidelity & Honesty (T013)
#
# T013 lands this group BEFORE the implementation rows (T014 § Conclusion/§ Key
# Changes, T015 § Evidence, T016 § Risks & Limits, T017 § Next Steps/§ Language,
# T018 § Fidelity & Honesty). Clauses whose row has not run yet are the recorded
# red-first frontier. The governance fixture directory is projected into the two
# source states FR-014 distinguishes — all sources readable, and one source
# unavailable — so the source-list obligation is asserted on data, not prose.
# ---------------------------------------------------------------------------

GOVERNANCE = RUN_FIXTURES / "governance"
GOVERNANCE_STEMS = ("instructions", "constitution", "glossary", "features")


def _report_shape() -> str:
    assert REPORT_SHAPE_DOC.is_file(), f"report-shape reference missing: {REPORT_SHAPE_DOC}"
    return _read(REPORT_SHAPE_DOC)


def _rs_section(heading: str) -> str:
    return _section_body(_report_shape(), heading)


def _governance_state(missing: tuple = ()) -> dict:
    """Project the governance stubs into FR-014 source states (two-state fixture)."""
    states = {}
    for stem in GOVERNANCE_STEMS:
        path = GOVERNANCE / f"{stem}.md"
        assert path.is_file(), f"governance projection missing: {path}"
        body = _read(path)
        assert "source:" in body and "status: read" in body, (
            f"{path} is not a readable governance projection stub (FR-014)"
        )
        states[stem] = "unavailable" if stem in missing else "read"
    return states


def test_rp05_conclusion_verdict():
    body = _rs_section("## Conclusion")
    for anchor in (
        "先于一切细节",
        "首行",
        "`verdict: <token>`",
        "英文原样",
        "报告语言",
        "FR-019",
        "未执行任何动作",
        "MUST NOT 被写成「执行成功」",
        "MUST NOT 使用成功措辞",
        "部分完成",
    ):
        assert anchor in body, f"§ Conclusion lacks the verdict anchor {anchor!r} (RP-05)"


def test_rp06_key_changes_by_impact():
    body = _rs_section("## Key Changes")
    for anchor in (
        "按影响降序",
        "FR-019",
        "字典序",
        "封闭影响尺",
        "无变化",
        "MUST NOT 留空",
        "指令造成的写入",
        "`products`",
    ):
        assert anchor in body, f"§ Key Changes lacks the impact-order anchor {anchor!r} (RP-06)"


def test_rp07_evidence_pointers():
    body = _rs_section("## Evidence")
    for anchor in (
        "每条关键结论配可定位指针",
        "产物路径",
        "命令与退出码",
        "测试读数",
        "`none`",
        "逐项",
    ):
        assert anchor in body, f"§ Evidence lacks the pointer anchor {anchor!r} (RP-07)"


def test_rp08_dispatch_record_line():
    body = _rs_section("## Evidence")
    for anchor in (
        "`dispatches:`",
        "顶层派发",
        "成功路径恒为 1",
        "降级为 `0`",
        "MUST NOT 重复计数",
    ):
        assert anchor in body, f"§ Evidence lacks the dispatch-record anchor {anchor!r} (RP-08)"


def test_rp09_no_known_risks_explicit():
    body = _rs_section("## Risks & Limits")
    for anchor in (
        "风险",
        "限制",
        "未验证项",
        "缺失上下文",
        "no known risks",
        "MUST NOT 省略",
    ):
        assert anchor in body, f"§ Risks & Limits lacks the risk anchor {anchor!r} (RP-09)"
    success = _envelope("success")
    assert success["failures"] == [], (
        "the success fixture models the 'no known risks' state (RP-09/SC-009)"
    )


def test_rp10_sources_read_list():
    body = _rs_section("## Risks & Limits")
    for anchor in (
        "来源清单",
        "只列",
        "实际读取",
        "MUST NOT 列进来源清单",
        "`not-read`",
        "`unavailable`",
        "FR-014",
    ):
        assert anchor in body, f"§ Risks & Limits lacks the source anchor {anchor!r} (RP-10)"

    full = _governance_state()
    assert len(full) == 4, f"the full state must carry the four governance sources, got {full}"
    assert set(full.values()) == {"read"}, f"the full state must be all-read, got {full}"

    partial = _governance_state(missing=("glossary",))
    assert partial["glossary"] == "unavailable", (
        "the partial state must model one unavailable governance source (FR-014)"
    )
    assert [s for s, state in partial.items() if state == "read"] == [
        "instructions", "constitution", "features",
    ], f"the partial state must keep the other three readable, got {partial}"
    missing = [s for s, state in partial.items() if state != "read"]
    listed = [s for s, state in partial.items() if state == "read"]
    assert missing == ["glossary"] and "glossary" not in listed, (
        "a missing source is declared as missing, never listed as read (RP-10)"
    )


def test_rp11_next_steps_or_none():
    body = _rs_section("## Next Steps")
    for anchor in ("可执行的下一步", "无下一步", "泛泛建议"):
        assert anchor in body, f"§ Next Steps lacks the actionable anchor {anchor!r} (RP-11)"


def test_rp12_language_priority():
    body = _rs_section("## Language")
    for anchor in ("指令主语言", "项目治理", "回退", "`en`", "声明"):
        assert anchor in body, f"§ Language lacks the priority anchor {anchor!r} (RP-12)"


def test_rp13_headings_stay_english():
    body = _rs_section("## Language")
    for anchor in ("英文原样", "小节标题", "载体标记", "派发记录", "键名"):
        assert anchor in body, f"§ Language lacks the invariant-literal anchor {anchor!r} (RP-13)"


def test_rp14_language_keeps_identifiers():
    body = _rs_section("## Language")
    for anchor in ("术语", "专有名词", "代码标识符", "路径", "命令", "MUST NOT 改变事实层"):
        assert anchor in body, f"§ Language lacks the identifier anchor {anchor!r} (RP-14)"


def test_rp15_fidelity_floor():
    body = _rs_section("## Fidelity & Honesty")
    for anchor in ("保真底线", "FR-017", "受保护集合", "已蕴含"):
        assert anchor in body, f"§ Fidelity & Honesty lacks the fidelity anchor {anchor!r} (RP-15)"


def test_rp16_no_fabrication():
    body = _rs_section("## Fidelity & Honesty")
    for anchor in ("MUST NOT 编造", "未读取", "不存在的路径", "未能核实"):
        assert anchor in body, f"§ Fidelity & Honesty lacks the honesty anchor {anchor!r} (RP-16)"


def test_rp17_expression_and_detector_honesty():
    body = _rs_section("## Fidelity & Honesty")
    for anchor in ("四维度", "`--tone`", "`--audience`", "MUST NOT 承诺", "检测器"):
        assert anchor in body, f"§ Fidelity & Honesty lacks the expression anchor {anchor!r} (RP-17)"


def test_rp18_reader_comprehension():
    body = _rs_section("## Fidelity & Honesty")
    for anchor in (
        "面向读者",
        "user-facing-comprehension.md",
        "内部引擎调用形式",
    ):
        assert anchor in body, f"§ Fidelity & Honesty lacks the reader anchor {anchor!r} (RP-18)"


# ===========================================================================
# 079 US3 — safety & honesty clauses (T019)
#
# Clause groups and their owners:
#   EX-11…EX-14  run-mode § Failure & No Retry (T020)
#   EX-15、EX-16  run-mode § Confirmation Missing (T021)
#   EX-17…EX-19  run-mode § Degradation & Boundaries (T022)
#   EX-20、EX-21  run-mode § Reservation & Nesting (T023)
#   IP-11…IP-14  run-mode § Reservation & Nesting (T023)
#   SC-004       denied fixture + § Confirmation Missing (FR-012 / FR-019 / SC-004)
#
# This group lands BEFORE its implementation rows (T020–T023): red = the asserted
# section or anchor is not on disk yet. The SC-004 pair is named with the SC prefix
# because the clause tables carry no `denied`-specific clause; it therefore stays
# outside T036's `test_(ip|ex|rp|cm|wc)` reverse-claim surface. The zero-exfiltration
# and no-retry instruments are fixed here: a literal scan over the command template
# and the skill source, a `git status --porcelain` snapshot around the assertions,
# and the report `dispatches:` line as the only dispatch/retry counter source.
# ===========================================================================

NETWORK_CALL_TOKENS = ("curl", "wget", "httpx", "requests.", "urllib", "fetch(")


def _run_mode_section(heading: str) -> str:
    assert RUN_MODE_DOC.is_file(), f"run-mode reference missing: {RUN_MODE_DOC}"
    return _section_body(_read(RUN_MODE_DOC), heading)


def _reservation(stem: str) -> dict:
    path = RUN_FIXTURES / "reservations" / f"{stem}.run"
    assert path.is_file(), f"reservation fixture missing: {path}"
    data = yaml.safe_load(_read(path))
    assert isinstance(data, dict), f"{path} is not a reservation mapping (E4)"
    for field in ("path", "created_at", "output_target", "ttl_hours"):
        assert field in data, f"{path} lacks E4 field {field!r}"
    return data


def _git_status_snapshot() -> set:
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
        capture_output=True, text=True, check=True,
    )
    return set(out.stdout.splitlines())


def _tree_digest(root: Path) -> dict:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


def _network_hits(text: str) -> list:
    return [
        (i + 1, token)
        for i, line in enumerate(text.splitlines())
        for token in NETWORK_CALL_TOKENS
        if token in line
    ]


# ---------------------------------------------------------------------------
# EX-11 .. EX-14 — § Failure & No Retry (T020)
# ---------------------------------------------------------------------------

def test_ex11_no_compensating_redispatch():
    body = _run_mode_section("## Failure & No Retry")
    for anchor in ("至多一次执行尝试", "不自动重试", "补发一次", "停止消费"):
        assert anchor in body, f"§ Failure & No Retry lacks the no-retry anchor {anchor!r} (EX-11)"


def test_ex12_failure_coordinates_no_retry():
    body = _run_mode_section("## Failure & No Retry")
    for anchor in ("失败坐标", "载体", "阶段", "错误信息", "已完成部分", "MUST NOT 改写为成功"):
        assert anchor in body, (
            f"§ Failure & No Retry lacks the failure-coordinate anchor {anchor!r} (EX-12)"
        )
    failure = _envelope("failure")
    assert failure["status"] == "failed", "the failure fixture must carry status failed (EX-12)"
    assert failure["failures"], "the failure fixture must carry at least one failure coordinate"
    for item in failure["failures"]:
        assert item.get("where") and item.get("what"), (
            f"failure fixture coordinate lacks where/what: {item!r} (EX-12)"
        )


def test_ex13_aborted_reported_as_aborted():
    body = _run_mode_section("## Failure & No Retry")
    for anchor in ("已中止", "中止点", "已完成部分"):
        assert anchor in body, f"§ Failure & No Retry lacks the abort anchor {anchor!r} (EX-13)"


def test_ex14_evidence_locatability_check():
    body = _run_mode_section("## Failure & No Retry")
    for anchor in ("可定位性", "未能核实", "MUST NOT 作为证据", "路径存在", "退出码自洽"):
        assert anchor in body, (
            f"§ Failure & No Retry lacks the locatability anchor {anchor!r} (EX-14)"
        )
    success = _envelope("success")
    kinds = [e.get("kind") for e in success["evidence"] if isinstance(e, dict)]
    assert "command" in kinds and "reading" in kinds, (
        f"success fixture must pair a command pointer with a reading pointer, got {kinds}"
    )


# ---------------------------------------------------------------------------
# EX-15 .. EX-16 — § Confirmation Missing (T021)
# ---------------------------------------------------------------------------

def test_ex15_confirmation_missing_fail_closed():
    body = _run_mode_section("## Confirmation Missing")
    for anchor in ("不执行该步", "`blocked_at`", "需要确认，未获答复", "其余已完成部分照常报告"):
        assert anchor in body, (
            f"§ Confirmation Missing lacks the fail-closed anchor {anchor!r} (EX-15)"
        )
    pending = _envelope("needs-confirmation")
    assert pending["status"] == "needs-confirmation"
    assert pending["blocked_at"], "needs-confirmation fixture must record the blocking point"
    assert pending["products"] == [], (
        "needs-confirmation fixture must not claim writes from the unexecuted step"
    )


def test_ex16_no_proxy_answer():
    body = _run_mode_section("## Confirmation Missing")
    for anchor in ("MUST NOT 代替", "用户可能同意", "等价动作"):
        assert anchor in body, (
            f"§ Confirmation Missing lacks the no-proxy-answer anchor {anchor!r} (EX-16)"
        )


# ---------------------------------------------------------------------------
# EX-17 .. EX-19 — § Degradation & Boundaries (T022)
# ---------------------------------------------------------------------------

def test_ex17_degraded_honesty():
    body = _run_mode_section("## Degradation & Boundaries")
    for anchor in ("声明降级", "可观察", "MUST NOT 把推断", "独立上下文", "独立工具集"):
        assert anchor in body, (
            f"§ Degradation & Boundaries lacks the honesty anchor {anchor!r} (EX-17)"
        )
    degraded = _envelope("degraded")
    assert degraded["status"] == "completed"
    assert degraded["failures"] == [], "degraded fixture models an observable clean run"


def test_ex18_degraded_keeps_report_contract():
    body = _run_mode_section("## Degradation & Boundaries")
    for anchor in ("五节", "证据义务", "保真底线", "不改报告契约"):
        assert anchor in body, (
            f"§ Degradation & Boundaries lacks the unchanged-contract anchor {anchor!r} (EX-18)"
        )


def test_ex19_no_network_from_humanize():
    body = _run_mode_section("## Degradation & Boundaries")
    for anchor in (
        "MUST NOT 发起网络请求",
        "MUST NOT 调用外部服务",
        "模型 API",
        "披露",
        "MUST NOT 记作",
    ):
        assert anchor in body, (
            f"§ Degradation & Boundaries lacks the boundary anchor {anchor!r} (EX-19)"
        )
    before = _git_status_snapshot()
    surfaces = [TEMPLATE, SKILL_SRC, *sorted(SKILL_SRC.parent.rglob("*.md"))]
    hits = [(str(path), line_no, token)
            for path in surfaces if path.is_file()
            for line_no, token in _network_hits(_read(path))]
    assert hits == [], (
        f"humanize surfaces carry network-call literals (SC-007/EX-19): {hits}"
    )
    assert _git_status_snapshot() == before, (
        "the contract check must not write to the working tree (zero-write/EX-19)"
    )


# ---------------------------------------------------------------------------
# EX-20 .. EX-21 — § Reservation & Nesting (T023)
# ---------------------------------------------------------------------------

def test_ex20_reservation_released_all_paths():
    body = _run_mode_section("## Reservation & Nesting")
    for anchor in ("任一出口", "正常", "失败", "中止", "异常", "释放", "不留残骸"):
        assert anchor in body, (
            f"§ Reservation & Nesting lacks the release anchor {anchor!r} (EX-20)"
        )
    run_a = _reservation("run-a")
    run_b = _reservation("run-b")
    assert run_a["ttl_hours"] == run_b["ttl_hours"] == 24, (
        "the reservation fixtures must use the 24h TTL (E4)"
    )
    assert run_a["path"] != run_b["path"], "the two reservations must be distinct files (一文一件)"
    assert run_a["created_at"] != run_b["created_at"], (
        "the two reservations must carry distinct start times for conflict naming"
    )


def test_ex21_dispatch_record_line():
    body = _run_mode_section("## Reservation & Nesting")
    for anchor in ("`report-shape.md` § Evidence", "只计 humanize 发起的顶层派发"):
        assert anchor in body, (
            f"§ Reservation & Nesting lacks the dispatch-count pointer {anchor!r} (EX-21)"
        )
    evidence = _section_body(_read(REPORT_SHAPE_DOC), "## Evidence")
    assert "`dispatches:`" in evidence, (
        "§ Evidence must own the dispatches: record line (EX-21/RP-08)"
    )
    assert "MUST NOT 重复计数" in evidence, (
        "§ Evidence must state that instruction-owned dispatches are not recounted (EX-21)"
    )


# ---------------------------------------------------------------------------
# IP-11 .. IP-14 — § Reservation & Nesting (T023)
# ---------------------------------------------------------------------------

def test_ip11_active_run_rejected():
    body = _run_mode_section("## Reservation & Nesting")
    for anchor in (
        "`.specify/.tmp/humanize/<run_id>.run`",
        "`active-run`",
        "冲突 `run_id`",
        "起始时间",
        "仓库级",
    ):
        assert anchor in body, (
            f"§ Reservation & Nesting lacks the active-run anchor {anchor!r} (IP-11)"
        )
    assert _reservation("run-a")["path"].startswith(".specify/.tmp/humanize/"), (
        "reservation fixture path must model the sanctioned temp root (E4)"
    )


def test_ip12_output_occupied_rejected():
    body = _run_mode_section("## Reservation & Nesting")
    for anchor in ("`output-occupied`", "目标路径", "冲突 `run_id`", "目标级"):
        assert anchor in body, (
            f"§ Reservation & Nesting lacks the output-occupied anchor {anchor!r} (IP-12)"
        )
    assert _reservation("run-b")["output_target"], (
        "run-b must model a target-level reservation with an output target"
    )
    assert _reservation("run-a")["output_target"] is None, (
        "run-a must model a repository-level reservation without an output target"
    )


def test_ip13_nested_invocation_rejected():
    body = _run_mode_section("## Reservation & Nesting")
    for anchor in ("`nested-invocation`", "speckit.humanize", "大小写不敏感", "保守判定", "命中的字面量"):
        assert anchor in body, (
            f"§ Reservation & Nesting lacks the nesting anchor {anchor!r} (IP-13)"
        )
    nested = (RUN_FIXTURES / "nested" / "instruction.txt").read_text(encoding="utf-8")
    assert "speckit.humanize" in nested.lower(), (
        "the nested fixture must carry the closed invocation token (IP-13)"
    )


def test_ip14_reject_paths_write_nothing():
    body = _run_mode_section("## Reservation & Nesting")
    for anchor in (
        "拒绝路径",
        "MUST NOT 产生派发",
        "MUST NOT 留下占位",
        "MUST NOT 写入任何文件",
    ):
        assert anchor in body, (
            f"§ Reservation & Nesting lacks the reject-path anchor {anchor!r} (IP-14)"
        )
    before = _git_status_snapshot()
    _ = _reservation("run-a")
    _ = _reservation("run-b")
    assert _git_status_snapshot() == before, (
        "reading the reject-path fixtures must not write to the working tree (IP-14)"
    )


# ---------------------------------------------------------------------------
# SC-004 — user denied the confirmation (FR-012 / FR-019 / SC-004)
# ---------------------------------------------------------------------------

def test_sc04_denied_no_side_effect():
    body = _run_mode_section("## Confirmation Missing")
    for anchor in ("零副作用", "MUST NOT 执行任何替代动作", "MUST NOT 写入任何文件"):
        assert anchor in body, (
            f"§ Confirmation Missing lacks the denied-no-side-effect anchor {anchor!r} (SC-004)"
        )
    denied = _envelope("denied")
    assert denied["status"] == "denied", "the denied fixture must carry status denied"
    assert denied["products"] == [], "a denied step must produce no products (SC-004)"
    whats = " ".join(item.get("what", "") for item in denied["failures"])
    assert "未执行任何替代动作" in whats, (
        f"the denied fixture must state that no substitute action ran (SC-004): {whats!r}"
    )
    target = RUN_FIXTURES / "needs-confirmation"
    before_status = _git_status_snapshot()
    before_tree = _tree_digest(target)
    _ = _envelope("denied")
    after_tree = _tree_digest(target)
    assert after_tree == before_tree, (
        "the denied path must leave the target tree byte-identical (SC-004): "
        f"{sorted(set(after_tree.items()) ^ set(before_tree.items()))}"
    )
    assert _git_status_snapshot() == before_status, (
        "the denied path must leave the working tree unchanged (SC-004)"
    )


def test_sc04_denied_verdict_and_scope():
    body = _run_mode_section("## Confirmation Missing")
    for anchor in ("用户拒绝确认", "未执行范围", "`## Evidence`", "aborted", "FR-019"):
        assert anchor in body, (
            f"§ Confirmation Missing lacks the denied-report anchor {anchor!r} (SC-004)"
        )
    denied = _envelope("denied")
    assert denied["status"] == "denied"
    assert denied["blocked_at"], "the denied fixture must keep the refusal point in blocked_at"
    whats = " ".join(item.get("what", "") for item in denied["failures"])
    assert "用户拒绝确认" in whats and "未执行范围" in whats, (
        f"the denied fixture must record the refusal reason and unexecuted scope: {whats!r}"
    )


# ===========================================================================
# 079 US4 — content-mode preservation & output target (T024)
#
# Clause groups and their owners:
#   CM-01…CM-04   SKILL.md content-mode branch (T025)
#   CM-05…CM-08   SKILL.md mode boundary & shared defenses (T026)
#   CM-09         command template + docs migration example (T029)
#   CM-10         content-mode wording (T030)
#   IP-15         content mode takes no reservation (T025)
#   IP-16、IP-17  run-mode § Output (T027)
#   RP-19、RP-20  run-mode § Output (T027)
#
# Red-first frontier: T025/T026/T027/T029/T030 have not run yet. The two
# invariant guards that already hold on the current tree (CM-01 equivalence
# anchors, CM-05 single routing owner) are annotated as guards and are not
# claimed as red-first. `tmp_path` calibrates the scaffold scanner used by
# CM-03 (positive and negative samples), so the predicate itself is exercised.
# ===========================================================================

INJECTION_INSTRUCTION = RUN_FIXTURES / "injection" / "instruction.md"
INJECTION_ENVELOPE = RUN_FIXTURES / "injection" / "envelope.md"
INJECTION_PRODUCT = RUN_FIXTURES / "injection" / "executor-note.txt"
CONTENT_INJECTION = (
    REPO_ROOT / "tests" / "fixtures" / "humanize" / "inline" / "s08-threat-inline.md",
    REPO_ROOT / "tests" / "fixtures" / "humanize" / "files" / "instruction-threat-file.md",
)
REPORT_SCAFFOLD_MARKERS = (
    *FIVE_SECTIONS,
    CARRIER_NATIVE,
    CARRIER_DEGRADED,
    "verdict:",
    "dispatches:",
)


def _skill_text() -> str:
    assert SKILL_SRC.is_file(), f"external skill missing: {SKILL_SRC}"
    return _read(SKILL_SRC)


def _scaffold_hits(text: str) -> list:
    return [marker for marker in REPORT_SCAFFOLD_MARKERS if marker in text]


# ---------------------------------------------------------------------------
# CM-01 .. CM-04 — SKILL.md content-mode branch (T025)
# ---------------------------------------------------------------------------

def test_cm01_content_mode_equivalence():
    text = _skill_text()
    for anchor in ("既有改写入口", "Stage 1", "Stage 7", "逐字不动", "四维度"):
        assert anchor in text, (
            f"SKILL.md lacks the content-mode equivalence anchor {anchor!r} (CM-01)"
        )
    for stage in ("输入解析", "主语言判定", "窗口估算", "保真自检", "输出与文件行为"):
        assert stage in text, f"SKILL.md lost the Stage anchor {stage!r} (CM-01)"


def test_cm02_content_output_text_only():
    text = _skill_text()
    for anchor in ("内容模式", "只写改写文本", "`--output`"):
        assert anchor in text, (
            f"SKILL.md lacks the content-mode output anchor {anchor!r} (CM-02)"
        )
    assert "原子写" in text or "原子重命名" in text, (
        "SKILL.md must keep the content-mode output write rules (CM-02)"
    )


def test_cm03_no_report_scaffold_in_content_mode(tmp_path):
    text = _skill_text()
    for anchor in ("不含五节", "载体标记", "迁移提示"):
        assert anchor in text, (
            f"SKILL.md lacks the no-scaffold anchor {anchor!r} (CM-03)"
        )
    # Calibrate the scanner on both sides (tmp_path): a rewritten-only sample
    # has zero hits, a report-shaped sample is recognised marker by marker.
    rewritten = tmp_path / "rewritten-only.md"
    rewritten.write_text("这是一段只含改写文本的段落，没有任何报告脚手架。\n", encoding="utf-8")
    shaped = tmp_path / "report-shaped.md"
    shaped.write_text(
        "\n".join([
            CARRIER_NATIVE,
            CARRIER_DEGRADED,
            "verdict: success",
            "## Conclusion",
            "## Key Changes",
            "## Evidence",
            "dispatches: 1",
            "## Risks & Limits",
            "## Next Steps",
        ]) + "\n",
        encoding="utf-8",
    )
    assert _scaffold_hits(_read(rewritten)) == [], (
        "a rewritten-only sample must carry no report scaffold (CM-03)"
    )
    assert set(_scaffold_hits(_read(shaped))) == set(REPORT_SCAFFOLD_MARKERS), (
        "the scaffold scanner must recognise every report marker (CM-03)"
    )


def test_cm04_content_mode_no_dispatch():
    text = _skill_text()
    for anchor in ("不派发执行体", "不取得并发占位", "不读取动作结果", "两次内容模式调用互不影响"):
        assert anchor in text, (
            f"SKILL.md lacks the content-mode isolation anchor {anchor!r} (CM-04)"
        )


# ---------------------------------------------------------------------------
# CM-05 .. CM-08 — mode boundary & shared defenses (T026)
# ---------------------------------------------------------------------------

def test_cm05_routing_owned_by_ip05():
    text = _skill_text()
    assert "references/run-mode.md" in text and "Mode Routing" in text, (
        "SKILL.md must point at the single routing owner (CM-05)"
    )
    assert "both-sources-and-instruction" not in text, (
        "SKILL.md must not restate the routing rejection table (CM-05)"
    )
    assert "本次内容源判定的唯一所有者" not in text, (
        "SKILL.md must not claim a second routing owner (CM-05)"
    )


def test_cm06_injection_defense_both_modes():
    text = _skill_text()
    for anchor in ("两种模式", "指令原文", "`final_output`", "`evidence`", "`products`", "产物内容"):
        assert anchor in text, (
            f"SKILL.md lacks the both-mode injection anchor {anchor!r} (CM-06)"
        )
    samples = [INJECTION_INSTRUCTION, INJECTION_ENVELOPE, INJECTION_PRODUCT, *CONTENT_INJECTION]
    for path in samples:
        assert path.is_file(), f"injection fixture missing: {path}"
        body = _read(path).lower()
        assert "忽略" in body or "ignore" in body, (
            f"{path} must carry instruction-like text (SC-010)"
        )


def test_cm07_fidelity_both_modes():
    text = _skill_text()
    for anchor in ("两种模式", "受保护集合", "不复制", "FR-017"):
        assert anchor in text, (
            f"SKILL.md lacks the both-mode fidelity anchor {anchor!r} (CM-07)"
        )


def test_cm08_detector_honesty_both_modes():
    text = _skill_text()
    for anchor in ("两种模式", "检测器", "不承诺"):
        assert anchor in text, (
            f"SKILL.md lacks the both-mode detector anchor {anchor!r} (CM-08)"
        )


# ---------------------------------------------------------------------------
# CM-09 .. CM-10 — migration example & wording (T029 / T030)
# ---------------------------------------------------------------------------

def test_cm09_migration_example_present():
    template = _read(TEMPLATE)
    for anchor in ("迁移示例", "--inline", "裸文本", "指令"):
        assert anchor in template, (
            f"command template lacks the migration-example anchor {anchor!r} (CM-09)"
        )
    docs = _read(DOCS_PAGE)
    for anchor in ("迁移示例", "裸文本", "指令", "--inline"):
        assert anchor in docs, (
            f"docs page lacks the copy-pasteable migration anchor {anchor!r} (CM-09)"
        )


def test_cm10_content_mode_wording_intact():
    text = _skill_text()
    for anchor in ("既有入口", "不是兼容垫片"):
        assert anchor in text, (
            f"SKILL.md lacks the retained-entry anchor {anchor!r} (CM-10)"
        )
    for banned in ("legacy shim", "deprecated entry"):
        assert banned not in text, (
            f"SKILL.md must not downgrade content mode with {banned!r} (CM-10)"
        )
    # "兼容垫片" is admissible only inside an explicit negation ("不是兼容垫片");
    # any affirmative use would downgrade the retained entry (CM-10).
    for i, line in enumerate(text.splitlines()):
        if "兼容垫片" in line:
            assert "不是兼容垫片" in line, (
                f"SKILL.md:{i + 1} uses 兼容垫片 without an explicit negation (CM-10): "
                f"{line.strip()[:80]!r}"
            )


# ---------------------------------------------------------------------------
# IP-15 .. IP-17 — reservation and output targets
# ---------------------------------------------------------------------------

def test_ip15_content_mode_unreserved():
    text = _skill_text()
    for anchor in ("不取得并发占位", "两次内容模式调用互不影响"):
        assert anchor in text, (
            f"SKILL.md lacks the content-mode no-reservation anchor {anchor!r} (IP-15)"
        )


def test_ip16_run_output_extension():
    body = _run_mode_section("## Output")
    for anchor in ("`.md`", "`.markdown`", "`.txt`", "`bad-extension`"):
        assert anchor in body, (
            f"§ Output lacks the run-mode extension anchor {anchor!r} (IP-16)"
        )
    assert "MUST NOT 复用内容模式的「扩展名跟随输入」规则" in body, (
        "§ Output must exclude the content-mode extension-follows-input rule (IP-16)"
    )


def test_ip17_content_output_unchanged():
    body = _run_mode_section("## Output")
    assert "内容模式的 `--output` 语义完全不变" in body, (
        "§ Output must state that content-mode --output semantics are unchanged (IP-17)"
    )
    text = _skill_text()
    for anchor in ("与输入格式族一致", "只含改写文本"):
        assert anchor in text, (
            f"SKILL.md lost the content-mode output anchor {anchor!r} (IP-17)"
        )


# ---------------------------------------------------------------------------
# RP-19 .. RP-20 — run-mode output target (T027)
# ---------------------------------------------------------------------------

def test_rp19_output_full_report_and_summary():
    body = _run_mode_section("## Output")
    for anchor in (
        "完整五节报告",
        "载体标记行",
        "`verdict:`",
        "`dispatches:`",
        "MUST NOT 写入迁移提示行",
        "摘要",
        "MUST NOT 成为报告的第六节",
    ):
        assert anchor in body, (
            f"§ Output lacks the full-report anchor {anchor!r} (RP-19)"
        )


def test_rp20_atomic_write_and_force():
    body = _run_mode_section("## Output")
    for anchor in ("原子写", "临时文件", "重命名", "`--force`", "逐字节不变", "不留部分文件"):
        assert anchor in body, (
            f"§ Output lacks the atomic-write anchor {anchor!r} (RP-20)"
        )


# ===========================================================================
# 079 — WC-05 .. WC-15 (T036): derived faces, docs, registration, the suite
# pin, the frozen surfaces and the fixture set — plus the clause ↔ test map
# machine check.
#
# The wiring contract splits each clause into a structural leg (asserted here)
# and a runtime leg recorded as stage evidence in verification.md: the two
# ``--check`` engines, the unlimited discovery inventory and the probe drift
# count. Asserting the structural leg in-suite is what keeps a hand-edited
# copy, mirror, docs page, registry row, frozen surface or fixture from passing
# silently; the evidence leg is where the engines' own exit codes live.
#
# WC-16..WC-20 land here as well: the map check below refuses any WC-prefixed
# suite function that no clause and no waiver claims, so their contracted
# traceability names MUST resolve to real functions.
# ===========================================================================

SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "080-humanize-run-output"
CONTRACTS_DIR = SPEC_DIR / "contracts"
TASKS_DOC = SPEC_DIR / "tasks.md"
BASELINE_COMMIT = "35ff11bc"

CONTRACT_FILES = (
    "invocation-parse.contract.md",
    "execution-dispatch.contract.md",
    "report-assembly.contract.md",
    "content-mode.contract.md",
    "wiring-compat.contract.md",
)
CLAUSE_TOTALS = {"IP": 17, "EX": 21, "RP": 20, "CM": 10, "WC": 20}

FROZEN_SURFACES = (
    "tests/contract/test_expression_gate_wiring.py",
    "tests/contract/test_expression_gates_doc.py",
    "tests/contract/test_expression_compatibility.py",
    "tests/contract/test_flow_class_ledger.py",
    "tests/contract/test_flow_class_correctness.py",
    "tests/contract/test_feedback_command_classification.py",
    "tests/contract/test_migration_distribution.py",
    "tests/contract/test_run_skills_wiring.py",
    "tests/contract/test_skill_layer_visibility_guards.py",
)

# WC-15's seven classes: success, failure, non-action, needs-confirmation,
# nested, degraded, concurrency.
RUN_FIXTURE_CLASSES = {
    "success": ("envelope.md",),
    "failure": ("envelope.md",),
    "non-action": ("envelope.md",),
    "needs-confirmation": ("envelope.md",),
    "nested": ("instruction.txt",),
    "degraded": ("envelope.md",),
    "reservations": ("run-a.run", "run-b.run"),
}
HISTORICAL_FIXTURES = (
    "files", "inline", "selftest", "tone", "rubric.md", "diff_protected.py",
)

CLAUSE_DEF_RE = re.compile(r"^- \*\*((?:IP|EX|RP|CM|WC)-\d{2})\*\*:", re.MULTILINE)
CLAUSE_ROW_RE = re.compile(r"^\| ((?:IP|EX|RP|CM|WC)-\d{2}) \|")
MAP_ROW_RE = re.compile(
    r"^\| `contracts/([a-z-]+\.contract\.md)` \| ([^|]+?) \| (T\d{3}) \|",
    re.MULTILINE,
)
TASK_ROW_RE = re.compile(r"^- \[[ X]\] (T\d{3}) ")
FUNC_RE = re.compile(r"^def (test_[a-z0-9_]+)\(", re.MULTILINE)
TEST_NAME_RE = re.compile(r"`(test_[a-z0-9_]+)(\[[^\]]*\])?`")


def _git_names(rev: str, *paths: str) -> list:
    """Tracked paths whose bytes differ from ``rev`` (untracked files excluded)."""
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "diff", "--name-only", rev, "--", *paths],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


def _git_tracked(rev: str, path: str) -> set:
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-tree", "--name-only", rev, path],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return {ln.strip() for ln in out.stdout.splitlines() if ln.strip()}


def _git_added_lines(rev: str, *paths: str) -> list:
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "diff", rev, "--", *paths],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return [ln[1:] for ln in out.stdout.splitlines()
            if ln.startswith("+") and not ln.startswith("+++")]


def _gates_module():
    spec = importlib.util.spec_from_file_location("scan_confirmation_gates", GATES_SCANNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _mirror_tree(root: Path) -> dict:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def _feature_row_062() -> list:
    for line in _read(REGISTRY).splitlines():
        if line.startswith("| 062 |"):
            cells = [c.strip() for c in line.split("|")]
            assert len(cells) > 6, f"062 registry row is malformed: {line[:120]!r}"
            return cells
    raise AssertionError("registry lacks the `| 062 |` row")


def test_wc05_copies_regenerated():
    anchor = "裸文本 = 待执行指令"
    assert anchor in _read(TEMPLATE), f"source template lacks the 079 marker {anchor!r} (WC-05)"
    for copy in COPIES:
        rel = str(copy.relative_to(REPO_ROOT))
        text = _read(copy)
        assert "AUTO-GENERATED from templates/commands/humanize.md" in text, (
            f"{rel} lacks the regeneration header naming its source template (WC-05)"
        )
        assert anchor in text, (
            f"{rel} is stale: the 079 marker is missing, so it was not regenerated (WC-05)"
        )
        assert DELEGATION_PATH in text, (
            f"{rel} does not delegate to the single skill {DELEGATION_PATH} (WC-05)"
        )
        assert _git_names(BASELINE_COMMIT, rel), (
            f"{rel} equals the baseline copy — 079 never regenerated it (WC-05)"
        )


def test_wc06_mirror_in_sync():
    src_root = SKILL_SRC.parent
    mirror_root = REPO_ROOT / ".specify" / "skills" / "humanize"
    src, mirror = _mirror_tree(src_root), _mirror_tree(mirror_root)
    assert src, f"skill source tree is empty: {src_root}"
    assert set(src) == set(mirror), (
        f"mirror file set drifted — missing: {sorted(set(src) - set(mirror))}; "
        f"extra: {sorted(set(mirror) - set(src))} (WC-06)"
    )
    drift = sorted(rel for rel in src if src[rel] != mirror[rel])
    assert not drift, f"mirror bytes drifted from the source: {drift} (WC-06)"
    assert "references/run-mode.md" in src and "references/report-shape.md" in src, (
        "the mirror must carry the run-mode and report-shape references (WC-06)"
    )
    engine = _read(REPO_ROOT / "scripts" / "python" / "sync-mirrors.py")
    assert '("skills/external", ".specify/skills"' in engine, (
        "sync-mirrors.py no longer declares the skills/external pair (WC-06)"
    )


def test_wc07_skill_body_budget():
    script = REPO_ROOT / "skills" / "external" / "improve-skills" / "scripts" / "skill-shape.py"
    out = subprocess.run(
        [sys.executable, str(script), str(SKILL_SRC), "--json"],
        capture_output=True, text=True, encoding="utf-8", cwd=str(REPO_ROOT), timeout=180,
    )
    assert out.returncode == 0, f"skill-shape.py failed (WC-07): {out.stderr[-800:]}"
    report = json.loads(out.stdout)
    assert report["verdict"] == "pass", f"skill-shape verdict is {report['verdict']!r} (WC-07)"
    metrics = report["metrics"]
    assert metrics["budget_tokens"] <= 5000, (
        f"the body budget may not be raised above 5000 tokens (WC-07): {metrics['budget_tokens']}"
    )
    assert metrics["est_tokens_controllable"] <= 5000, (
        f"SKILL.md controllable body is {metrics['est_tokens_controllable']} tokens (WC-07)"
    )


def test_wc08_docs_new_positioning():
    text = _read(DOCS_PAGE)
    for anchor in (
        "Run mode（缺省）",
        "五节",
        "Content mode（显式",
        "## Migration Example",
        "缺省不写入任何文件",
        "不承诺任何检测结果",
        "Instruction-like text",
        "--inline",
        "--file",
    ):
        assert anchor in text, f"docs page lacks the new-positioning anchor {anchor!r} (WC-08)"
    assert "绕过检测" not in text, "docs page carries a forbidden detector-evasion claim (WC-08)"


def test_wc09_docs_output_semantics():
    text = _read(DOCS_PAGE)
    headings = [ln.strip() for ln in text.splitlines()
                if ln.startswith("## ") and "`--output` Semantics" in ln]
    assert headings, "docs page lacks the `--output` Semantics section (WC-09)"
    body = _section_body(text, headings[0])
    for anchor in ("运行模式", "完整五节报告", "摘要", "改写文本", "内容模式"):
        assert anchor in body, f"§ `--output` Semantics lacks the anchor {anchor!r} (WC-09)"


def test_wc10_feature_062_status_held():
    detail = _read(FEATURE_DETAILS)
    assert "**Status**: Implemented" in detail, "Feature 062 detail lost its Implemented status (WC-10)"
    for heading in ("## Latest Review", "## Key Changes"):
        assert heading in detail, f"062 detail lacks {heading} (WC-10)"
    review = _section_body(detail, "## Latest Review")
    changes = _section_body(detail, "## Key Changes")
    assert "079" in review, "## Latest Review carries no 079 extension record (WC-10)"
    assert "079" in changes, "## Key Changes carries no 079 extension record (WC-10)"
    cells = _feature_row_062()
    assert "Implemented" in cells, f"the 062 registry row left the Implemented state (WC-10): {cells[:5]}"
    last_updated = [c for c in cells if c][-1]
    assert "079" in last_updated, (
        f"the 062 registry row's Last Updated cell carries no 079 marker (WC-10): {last_updated[:200]!r}"
    )


def test_wc11_feature_row_name_description():
    cells = _feature_row_062()
    name, description = cells[2], cells[3]
    assert "动作输出人类友好化" in name, f"062 row name is not the new positioning (WC-11): {name!r}"
    assert "人类友好" in description, f"062 row description is not the new positioning (WC-11)"
    assert "结论/关键变化/证据/风险/下一步" in description, (
        f"062 row description must name the five-section report (WC-11): {description[:160]!r}"
    )


def test_wc12_contract_suite_extended():
    names = FUNC_RE.findall(_read(Path(__file__)))
    for namespace, total in CLAUSE_TOTALS.items():
        owned = {n for n in names if n.startswith(f"test_{namespace.lower()}")}
        assert len(owned) >= total, (
            f"the suite carries {len(owned)} {namespace}-prefixed test functions, "
            f"below the {total} {namespace} clauses (WC-12)"
        )
    legacy = (
        "test_c01_thin_entry_shape",
        "test_c02_single_skill_delegation",
        "test_c03_skill_frontmatter_and_self_sufficient",
        "test_c04_generated_copies_present",
        "test_c05_docs_page_content",
        "test_c06_registry_rows_resolve",
        "test_c07_skill_probe_unit_and_compiled_wrapup",
        "test_c08_no_runtime_surface",
        "test_c09_baseline_no_new_failures",
        "test_c10_detector_honesty_wording",
        "test_sc04_denied_no_side_effect",
        "test_sc04_denied_verdict_and_scope",
    )
    missing = [n for n in legacy if n not in names]
    assert not missing, f"pre-079 assertions were deleted (WC-12): {missing}"


def test_wc13_stage_class_pin_remeasured():
    module = _import_test_module("test_stage_class_wiring.py")
    pinned = module.UNCHANGED_SHA256.get("humanize")
    measured = hashlib.sha256(TEMPLATE.read_bytes()).hexdigest()
    assert pinned, "UNCHANGED_SHA256 lost its humanize row (WC-13)"
    assert pinned == measured, (
        f"the humanize byte pin is stale — re-measure it, do not drop it (WC-13): "
        f"pinned={pinned} measured={measured}"
    )
    assert "humanize re-measured 2026-10-31 (079" in _read(
        REPO_ROOT / "tests" / "contract" / "test_stage_class_wiring.py"
    ), "the humanize pin row lost its date-and-reason comment (WC-13)"
    # The judgement shape that must survive: stripping the 077 wiring card from a
    # stage template restores the frozen baseline byte for byte. humanize is a
    # pre-077 entry point, so it is held by the byte pin above (and by WC-03's
    # ## Outline anchors), not by a card strip.
    assert callable(getattr(module, "strip_wiring", None)), (
        "the strip-away-the-wiring card leg was removed (WC-13)"
    )
    assert module.STAGE_STEMS, "the stage-stem roster is empty (WC-13)"
    for stem in module.STAGE_STEMS:
        stripped, block = module.strip_wiring(
            (REPO_ROOT / "templates" / "commands" / f"{stem}.md").read_text(encoding="utf-8")
        )
        assert block.strip(), f"{stem}: the strip found no wiring card (WC-13)"
        assert hashlib.sha256(stripped.encode("utf-8")).hexdigest() == module.BASELINE_SHA256[stem], (
            f"{stem}: stripping the wiring card no longer restores the frozen baseline (WC-13)"
        )


def test_wc14_frozen_surfaces_unchanged():
    for rel in FROZEN_SURFACES:
        path = REPO_ROOT / rel
        assert path.is_file(), f"frozen surface missing: {rel} (WC-14)"
        assert FUNC_RE.findall(_read(path)), f"{rel} carries no test function (WC-14)"
        changed = _git_names(BASELINE_COMMIT, rel)
        assert not changed, (
            f"frozen surface {rel} differs from {BASELINE_COMMIT} (WC-14): the roster/count "
            f"of a verification-only suite may not move with this feature"
        )


def test_wc15_run_fixtures_present():
    for class_name, files in RUN_FIXTURE_CLASSES.items():
        for name in files:
            path = RUN_FIXTURES / class_name / name
            assert path.is_file(), f"run fixture missing: {path} ({class_name}, WC-15)"
    assert _envelope("denied")["status"] == "denied", "the denied fixture lost its status (WC-15)"
    for name in HISTORICAL_FIXTURES:
        assert (REPO_ROOT / "tests" / "fixtures" / "humanize" / name).exists(), (
            f"historical fixture corpus entry missing: {name} (WC-15)"
        )
    rewritten = _git_names(
        BASELINE_COMMIT, "tests/fixtures/humanize",
        ":(exclude)tests/fixtures/humanize/run",
    )
    assert not rewritten, (
        f"the historical fixture corpus was rewritten (WC-15): {rewritten}"
    )


def test_wc16_command_roster_unchanged():
    live = {p.name for p in (REPO_ROOT / "templates" / "commands").glob("*.md")}
    base = {Path(n).name for n in _git_tracked(BASELINE_COMMIT, "templates/commands/")}
    assert base, "the baseline tree lists no command templates"
    assert live == base, (
        f"command roster drifted — added: {sorted(live - base)}; "
        f"removed: {sorted(base - live)} (WC-16)"
    )
    assert len(live) == 27, f"the roster must stay at 27 command templates, found {len(live)} (WC-16)"


def test_wc17_new_line_gate_zero():
    gates = _gates_module()
    added = _git_added_lines(BASELINE_COMMIT, *gates.SCAN_DIRS, "templates/*.md")
    assert added, "no added lines on the scan surface — the diff base or paths are wrong"
    hits = [line[:120] for line in added if gates.BLOCKING_RE.search(line)]
    assert not hits, f"new blocking confirmation-gate lines introduced (WC-17): {hits}"


def test_wc18_no_runtime_surface_added():
    changed = _git_names(BASELINE_COMMIT, "src/specify_cli", "scripts")
    assert not changed, (
        f"the runtime surface moved — this feature adds no runtime and no dependency (WC-18): {changed}"
    )


def test_wc19_ledgers_unchanged():
    changed = _git_names(
        BASELINE_COMMIT,
        "shared/definitions/flow-class-definitions.md",
        "shared/definitions/probe-definitions.md",
    )
    assert not changed, f"a class/probe registry moved (WC-19): {changed}"
    ledger = _read(REPO_ROOT / "shared" / "definitions" / "flow-class-definitions.md")
    rows = [ln for ln in ledger.splitlines()
            if ln.startswith("|") and "skill:humanize" in ln]
    assert rows, "the flow-class ledger lost its skill:humanize row (WC-19)"
    for row in rows:
        assert "expression" in row and "reader-oracle" in row, (
            f"skill:humanize left expression/reader-oracle (WC-19): {row}"
        )
    assert not any(ln.startswith("| /speckit.humanize ") for ln in
                   _read(PROBE_DEFS).splitlines()), (
        "a probe command unit was registered for the Simple command (WC-19)"
    )


def test_wc20_command_stays_simple():
    text = _read(TEMPLATE)
    assert "scripts:" not in _frontmatter(text), "a scripts: block would classify it Complex (WC-20)"
    assert "## Wrap-up" not in text, "a ## Wrap-up face would classify it Complex (WC-20)"
    assert "## Feedback" not in text, "a ## Feedback step would classify it Complex (WC-20)"
    feedback = _import_test_module("test_feedback_command_classification.py")
    assert "humanize" in feedback.SIMPLE_COMMANDS, (
        "the 027 classification table no longer derives humanize as Simple (WC-20)"
    )
    assert "humanize" not in feedback.COMPLEX_COMMANDS, "humanize moved to Complex (WC-20)"
    names = set(FUNC_RE.findall(
        _read(REPO_ROOT / "tests" / "contract" / "test_feedback_command_classification.py")
    ))
    for required in ("test_simple_command_omits_feedback_step",
                     "test_table_covers_every_command_template"):
        assert required in names, f"the WC-20 carrier {required} disappeared (WC-20)"


# ---------------------------------------------------------------------------
# WC-12 machine leg — the clause ↔ test map is total.
#
# The three inputs are the five contracts (clause definitions + traceability
# names), this file's § Contract Coverage Map (clause → task row) and the
# § Clause Test Waivers table. "Zero gap" is this assertion turning green, not
# a human reading of the table: a clause with no test name, a test name that
# resolves to no function, a WC-prefixed function nobody claims, or a clause
# assigned twice all fail here.
# ---------------------------------------------------------------------------

def _clause_definitions() -> tuple:
    definitions, traceability = {}, {}
    for fname in CONTRACT_FILES:
        path = CONTRACTS_DIR / fname
        assert path.is_file(), f"contract missing: {path} (WC-12)"
        text = _read(path)
        for clause in CLAUSE_DEF_RE.findall(text):
            assert clause not in definitions, (
                f"{clause} is defined twice: {definitions.get(clause)} and {fname} (WC-12)"
            )
            definitions[clause] = fname
        for line in text.splitlines():
            if not CLAUSE_ROW_RE.match(line):
                continue
            clause = CLAUSE_ROW_RE.match(line).group(1)
            found = TEST_NAME_RE.search(line)
            traceability[clause] = (found.group(1) + (found.group(2) or "")) if found else ""
    return definitions, traceability


def _waiver_rows() -> list:
    lines = _read(TASKS_DOC).splitlines()
    start = next(
        i for i, ln in enumerate(lines) if ln.strip().startswith("### Clause Test Waivers")
    )
    rows = []
    for line in lines[start + 1:]:
        if line.startswith("## ") or (line.startswith("### ")
                                      and "Clause Test Waivers" not in line):
            break
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] == "条款" or set("".join(cells)) <= set("-: "):
            continue
        rows.append(cells)
    return rows


def test_wc12_clause_test_map_is_total():
    definitions, traceability = _clause_definitions()
    assert len(definitions) == sum(CLAUSE_TOTALS.values()), (
        f"the five contracts define {len(definitions)} clauses, expected "
        f"{sum(CLAUSE_TOTALS.values())} (WC-12)"
    )
    for namespace, total in CLAUSE_TOTALS.items():
        measured = len([c for c in definitions if c.startswith(namespace + "-")])
        assert measured == total, (
            f"{namespace} defines {measured} clauses, the partition says {total} (WC-12)"
        )
    assert set(traceability) == set(definitions), (
        f"clauses with no traceability row: {sorted(set(definitions) - set(traceability))}; "
        f"traceability rows for undefined clauses: {sorted(set(traceability) - set(definitions))}"
    )
    unnamed = sorted(c for c, name in traceability.items() if not name.strip())
    assert not unnamed, f"clauses with an empty test name in the traceability table: {unnamed}"

    tasks_text = _read(TASKS_DOC)
    coverage = _section_body(tasks_text, "## Contract Coverage Map")
    row_of, mapped = {}, {}
    for line in coverage.splitlines():
        match = MAP_ROW_RE.match(line)
        if not match:
            continue
        contract_file, clause_cell, row_id = match.group(1), match.group(2), match.group(3)
        clauses = re.findall(r"(?:IP|EX|RP|CM|WC)-\d{2}", clause_cell)
        assert clauses, f"coverage-map row for {row_id} names no clause (WC-12)"
        for clause in clauses:
            assert clause in definitions, (
                f"coverage map names undefined clause {clause} under {contract_file}"
            )
            assert clause not in mapped, (
                f"{clause} is assigned to two rows: {mapped[clause]} and {row_id} (WC-12)"
            )
            assert definitions[clause] == contract_file, (
                f"{clause} is defined in {definitions[clause]} but mapped under {contract_file}"
            )
            mapped[clause] = row_id
    assert set(mapped) == set(definitions), (
        f"clauses with no coverage-map row: {sorted(set(definitions) - set(mapped))}; "
        f"map rows naming no defined clause: {sorted(set(mapped) - set(definitions))}"
    )

    task_bodies = {}
    for line in tasks_text.splitlines():
        match = TASK_ROW_RE.match(line)
        if match:
            task_bodies[match.group(1)] = line
    for clause, row_id in mapped.items():
        assert row_id in task_bodies, (
            f"{clause} is assigned to {row_id}, which is not a task row (WC-12)"
        )
        assert clause in task_bodies[row_id], (
            f"task row {row_id} does not repeat the clause {clause} it owns (WC-12)"
        )

    waivers = {}
    for cells in _waiver_rows():
        assert len(cells) == 5, f"malformed waiver row (want 5 cells): {cells}"
        found = TEST_NAME_RE.search(cells[1])
        assert found, f"waiver row names no test function: {cells}"
        assert cells[2] and cells[3] and cells[4], (
            f"waiver row lacks a reason, a remedy or an evidence slot (M-21): {cells}"
        )
        waivers[found.group(1)] = cells

    resolvable = {}
    for rel in (
        "tests/contract/test_humanize_command_surface.py",
        "tests/contract/test_stage_class_wiring.py",
        "tests/contract/test_feedback_command_classification.py",
    ):
        for name in FUNC_RE.findall(_read(REPO_ROOT / rel)):
            resolvable[name] = rel
    claimed, unresolved = set(), []
    for clause, test_id in traceability.items():
        base = test_id.split("[")[0]
        if base in resolvable or base in waivers:
            claimed.add(base)
        else:
            unresolved.append(f"{clause}->{test_id}")
    assert not unresolved, (
        f"traceability names that resolve to no suite function and carry no waiver (WC-12): "
        f"{unresolved}"
    )

    orphans = sorted(
        name for name in FUNC_RE.findall(_read(Path(__file__)))
        if re.match(r"test_(ip|ex|rp|cm|wc)", name)
        and name not in claimed
        and name not in waivers
    )
    assert not orphans, (
        f"WC-prefixed suite functions that no clause and no waiver claims (WC-12): {orphans}"
    )
