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
``.specify/specs/079-humanize-run-output/tasks.md`` § Contract Coverage Map: IP-01…IP-10
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

import importlib.util
import re
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
