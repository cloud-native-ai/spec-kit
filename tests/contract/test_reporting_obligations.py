"""Contract test: the reporting obligation's owner document (087, T007).

Layer-2 of the Feature 087 test map. This file owns the assertions over
``shared/guidelines/reporting-obligations.md`` (framework source) and its mirror
``.specify/shared/guidelines/reporting-obligations.md``.

**The eight-fact count is asserted by clause id and count, never by re-listing.** Contract
``contracts/reporting-obligations.contract.md`` C-01 is the owner of "exactly eight owned facts"; this test asserts
that the delivered declaration names eight of them, and that the four documents the owner does **not** own are
reached by path. If this file carried its own copy of the eight-item list, the red-first assertion and C-01 could
disagree while both looked green — the defect the row's ``[covers:]`` note names. The only itemised expectation kept
here is the *non-owned* side, because that side's failure mode is a missing path, and a path is checkable.

Scope: this row asserts the owner document's structure, its single-source-of-truth declaration, the scope predicate,
the cadence anchor and the single 30-second definition site, the four content-element labels, the transition
classes, the prohibition clause, and the absence of a copy of ``progress-reporting.md``'s element descriptions.
The remaining owner-document clauses (digest contract shape, reporter-seat population, master duty over sub-flows)
are asserted by the rows that own them (T012, T022, T037) — this file grows in those rows, so a failure here is
never attributable to work this row did not do.

**Red-first (Constitution IV)**: authored before T008 exists. Every test asserts the owner path first, so red is
"artifact missing", never an import or collection error.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER = REPO_ROOT / "shared" / "guidelines" / "reporting-obligations.md"
OWNER_MIRROR = REPO_ROOT / ".specify" / "shared" / "guidelines" / "reporting-obligations.md"

PROGRESS_REPORTING = REPO_ROOT / "shared" / "guidelines" / "progress-reporting.md"
SUBAGENT_DEFINITIONS = REPO_ROOT / "shared" / "definitions" / "subagent-definitions.md"
PATTERNS = REPO_ROOT / "skills" / "internal" / "create-team" / "references" / "patterns.md"
LINE_REGISTRY = (
    REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "line-registry.py"
)
CONFIRMATION_GATES = REPO_ROOT / "shared" / "guidelines" / "confirmation-gates.md"

#: Contract C-01 fixes the owned-fact count as a closed set of exactly eight.
OWNED_FACT_COUNT = 8

#: The four documents the owner explicitly does NOT own, each reached by path (contract C-01).
NON_OWNED_OWNERS = {
    "progress-reporting.md": "cadence anchor, content floor, deferral rule, interactive default",
    "subagent-definitions.md": "artifact triplet and execution modes",
    "patterns.md": "stall threshold numbers",
    "line-registry.py": "registry state vocabulary",
}

#: The four content elements named as labels (contract C-05 allows labels, forbids restating the definitions).
ELEMENT_LABELS = ("position", "delta", "remainder", "blocker")

#: The three out-of-cadence transition classes (contract C-08 / FR-010).
TRANSITION_CLASSES = ("sub-flow failure", "stall crossing", "dispatch failure")

#: The nine prohibitions of contract C-13, by the words the audit looks for.
MACHINERY_TERMS = (
    "scheduler",
    "timer",
    "daemon",
    "dependency",
    "store",
    "console channel",
    "registry",
    "state spine",
    "ledger",
)


def _read(path: Path) -> str:
    assert path.is_file(), (
        "expected artifact missing: %s (red is the intended pre-implementation state for T007)"
        % path.relative_to(REPO_ROOT)
    )
    return path.read_text(encoding="utf-8")


def _owner() -> str:
    return _read(OWNER)


# --------------------------------------------------------------------------- #
# existence on both sides of the mirror pair
# --------------------------------------------------------------------------- #
def test_owner_exists_at_both_mirror_paths():
    """The framework source exists and its mirror exists (contract OM-01 / plan § Mirror Obligations)."""
    assert OWNER.is_file(), "%s must exist" % OWNER.relative_to(REPO_ROOT)
    assert OWNER_MIRROR.is_file(), (
        "the mirror %s must be produced by sync-mirrors.py (plan T039) — a source-only artifact is"
        " unreachable by a downstream project" % OWNER_MIRROR.relative_to(REPO_ROOT)
    )


def test_owner_and_mirror_are_byte_identical():
    """The pair is byte-identical; drift is the defect the mirror discipline names."""
    assert OWNER.read_bytes() == OWNER_MIRROR.read_bytes(), (
        "shared/ vs .specify/shared/ copies of reporting-obligations.md differ"
    )


# --------------------------------------------------------------------------- #
# C-01 — the single-source-of-truth declaration
# --------------------------------------------------------------------------- #
def test_declaration_block_is_present_at_the_head():
    """The document opens with a single-source-of-truth declaration (its siblings' shape)."""
    lines = _owner().splitlines()
    head = "\n".join(lines[:40]).lower()
    assert "single source of truth" in head or "single-source-of-truth" in head or "唯一定义" in head, (
        "the owner must open with a single-source-of-truth declaration naming what it owns"
    )


def test_declaration_names_exactly_eight_owned_facts():
    """Exactly eight owned facts — asserted by count, with C-01 as the list's owner."""
    text = _owner()
    block = _declaration_block(text)
    numbered = re.findall(r"^\s*\d+[.)]\s+\S", block, re.M)
    assert len(numbered) == OWNED_FACT_COUNT, (
        "contract C-01 fixes the owned-fact count at %d; the declaration lists %d item(s). "
        "The list itself is owned by contracts/reporting-obligations.contract.md C-01 and is"
        " deliberately not re-listed here." % (OWNED_FACT_COUNT, len(numbered))
    )


def test_declaration_names_the_four_non_owned_owners_by_path():
    """Each fact the owner does not own is reached by a real path (C-01)."""
    text = _owner()
    for filename, subject in NON_OWNED_OWNERS.items():
        assert filename in text, (
            "the declaration must name %s by path (it owns the %s)" % (filename, subject)
        )
    for path in (PROGRESS_REPORTING, SUBAGENT_DEFINITIONS, PATTERNS, LINE_REGISTRY):
        assert path.is_file(), "the non-owned owner %s must still exist" % path


def test_declaration_forbids_restating_the_borrowed_rules():
    """The declaration says the borrowed disciplines are reached by reference, never copied."""
    block = _declaration_block(_owner()).lower()
    assert "must not" in block or "must not be copied" in block or "不得复制" in block or "m ust not" in block, (
        "the declaration must state that borrowed rules are referenced, never restated"
    )


# --------------------------------------------------------------------------- #
# C-02 — the scope predicate, verbatim-shaped
# --------------------------------------------------------------------------- #
def test_scope_predicate_is_stated_as_two_conjuncts():
    """In scope = two or more concurrent units OR one or more asynchronous delegations continued past dispatch.

    The owner is bilingual at the definition site (`shared/guidelines/bilingual-expression.md`), so each disjunct is
    accepted in either form: the assertion is on the *fact*, not on the typography that carries it.
    """
    text = _owner().lower()
    assert "in scope" in text or "在范围内" in text, (
        "the owner must state the predicate positively ('in scope when …')"
    )
    assert "two or more concurrent" in text or "两个或更多并发单元" in text, (
        "the first disjunct ('two or more concurrent units') must appear"
    )
    assert "asynchronous delegation" in text or "异步委托" in text, (
        "the second disjunct ('asynchronous delegations continued past dispatch') must appear"
    )
    assert "dispatch" in text, (
        "the second disjunct's 'continued past their dispatch' qualifier must appear"
    )


def test_single_synchronous_step_is_declared_out_of_scope():
    """The predicate's negative case and its one-line escape (FR-002)."""
    text = _owner().lower()
    assert "single synchronous step" in text or "单个同步步骤" in text, (
        "a single synchronous step must be named as out of scope"
    )
    assert "one line" in text or "一行" in text, (
        "an out-of-scope flow must be allowed to say so in one line rather than emit an empty report"
    )
    assert "roster" in text or "花名册" in text, (
        "the owner must state that no per-flow exempt roster is maintained (requirements.md A3, A9)"
    )


# --------------------------------------------------------------------------- #
# C-03 — the long-run cadence default and its single definition site
# --------------------------------------------------------------------------- #
def test_long_run_default_is_defined_once_in_the_owner():
    """The 30-second literal appears exactly once in the owner document."""
    occurrences = _owner().count("30 秒") + _owner().count("30 seconds")
    assert occurrences == 1, (
        "the long-run default must have exactly one definition site inside the owner; found %d"
        % occurrences
    )


def test_overridability_is_stated():
    """The value is overridable per run and per structure without a source edit (FR-003)."""
    text = _owner().lower()
    assert "override" in text or "覆盖" in text, (
        "the owner must state the per-run / per-structure override"
    )
    assert "without a source edit" in text or "无需改源码" in text or "no source edit" in text, (
        "the override must be stated as requiring no source edit"
    )


def test_no_second_framework_source_carries_the_literal():
    """Only the owner plus the two whitelisted prose hits carry the literal (SC-006)."""
    whitelisted = (
        Path("skills/external/draw-diagram/references/types/plantuml/references/howto/19-salt-diagram.md"),
        Path("skills/external/improve-skills/references/skill-slimming-principles.md"),
    )
    hits = []
    for root_name in ("shared", "templates", "skills", "agents"):
        for path in (REPO_ROOT / root_name).rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".txt"}:
                continue
            rel = path.relative_to(REPO_ROOT)
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):  # pragma: no cover - binary leftovers
                continue
            if "30 秒" in text or "30 seconds" in text:
                hits.append(rel)
    definition_sites = [rel for rel in hits if rel not in whitelisted]
    assert definition_sites == [Path("shared/guidelines/reporting-obligations.md")], (
        "the only non-whitelisted occurrence must be the owner document; found %r"
        % ([str(p) for p in definition_sites],)
    )


# --------------------------------------------------------------------------- #
# C-05 — the four content elements by reference, labels only
# --------------------------------------------------------------------------- #
def test_four_element_labels_are_named():
    """The owner may name the labels; a consumer that cannot name what it emits cannot comply.

    Contract C-05 allows the labels and forbids the descriptions; the bilingual owner carries both forms, so a label
    is accepted in English or in Chinese (`shared/guidelines/bilingual-expression.md`).
    """
    text = _owner().lower()
    accepted = {
        "position": ("position", "位置"),
        "delta": ("delta", "增量"),
        "remainder": ("remainder", "剩余"),
        "blocker": ("blocker", "风险", "阻塞"),
    }
    for label, forms in accepted.items():
        assert any(form in text for form in forms), (
            "the owner must name the content-element label %r" % label
        )


def test_owner_anchors_the_element_definitions_instead_of_copying_them():
    """The elements are reached by section anchor to progress-reporting.md § 汇报内容下限."""
    text = _owner()
    assert "progress-reporting.md" in text, "the owner must point at progress-reporting.md by path"
    assert "汇报内容下限" in text, (
        "the owner must reach the content floor by its section anchor, not by restating it"
    )


def test_owner_does_not_copy_the_element_descriptions():
    """No sentence of progress-reporting.md's element descriptions is reproduced in the owner."""
    owner_text = _owner()
    owner_lower = owner_text.lower()
    source = _read(PROGRESS_REPORTING)
    element_section = _section(source, "## 汇报内容下限(四要素)")
    assert element_section, "progress-reporting.md must still carry the 汇报内容下限 section"
    distinctive = [
        "当前处在计划的哪一步",
        "自上次汇报以来的",
        "还剩什么",
        "无事则显式写",
        "倾倒日志或逐文件罗列",
    ]
    copied = [frag for frag in distinctive if frag in owner_text]
    assert not copied, (
        "the owner must not restate the element descriptions; copied fragment(s): %r" % (copied,)
    )
    # And the two documents must not be able to converge by accident: the owner is not a
    # byte-superset of the owner discipline it consumes.
    assert len(element_section) > 200, "sanity: the consumed section is a real section"
    assert element_section.strip() not in owner_lower, (
        "the owner contains progress-reporting.md's content-floor section verbatim"
    )


# --------------------------------------------------------------------------- #
# C-08 — the out-of-cadence transition classes
# --------------------------------------------------------------------------- #
def test_three_transition_classes_are_named():
    """Sub-flow failure, stall crossing and dispatch failure each appear (contract C-08)."""
    text = _owner().lower()
    accepted = {
        "sub-flow failure": ("sub-flow failure", "子流程失败"),
        "stall crossing": ("stall crossing", "跨越停滞阈值"),
        "dispatch failure": ("dispatch failure", "派发失败"),
    }
    for klass, forms in accepted.items():
        assert any(form in text for form in forms), (
            "the owner must name the transition class %r" % klass
        )


def test_transition_reports_before_the_next_tick():
    """A transition never waits for the clock (FR-010)."""
    text = _owner().lower()
    assert (
        "before the next tick" in text
        or "immediately" in text
        or "下一个 tick 之前" in text
        or "即时" in text
    ), "the owner must state that a significant transition reports before the next tick"


# --------------------------------------------------------------------------- #
# C-13 — the zero-new-machinery prohibition, phrased testably
# --------------------------------------------------------------------------- #
def test_prohibition_clause_names_all_nine_terms():
    """One clause forbids scheduler / timer / daemon / dependency / store / channel / registry / spine / ledger."""
    text = _owner().lower()
    missing = [term for term in MACHINERY_TERMS if term not in text]
    assert not missing, (
        "the zero-new-machinery prohibition must name every prohibited item; missing %r" % (missing,)
    )


def test_prohibition_is_phrased_as_a_testable_clause():
    """The clause reads as a prohibition ('MUST NOT …'), not as an aspiration."""
    text = _owner()
    lowered = text.lower()
    assert "must not" in lowered, "the prohibition must be phrased with MUST NOT"
    # The clause must be near the machinery vocabulary rather than merely present somewhere.
    index = lowered.find("scheduler")
    window = lowered[max(0, index - 400): index + 800]
    assert "must not" in window or "no scheduler" in window, (
        "the machinery vocabulary must appear inside a prohibition sentence"
    )


# --------------------------------------------------------------------------- #
# C-10 — the not-a-gate clause reaches confirmation-gates.md by path
# --------------------------------------------------------------------------- #
def test_not_a_gate_clause_points_at_the_gate_owner():
    """Reporting authorizes nothing; the gate discipline is reached by path (contract C-10)."""
    text = _owner()
    assert "confirmation-gates.md" in text, (
        "the not-a-gate clause must point at shared/guidelines/confirmation-gates.md"
    )
    assert CONFIRMATION_GATES.is_file(), "the pointed-at gate owner must exist"
    lowered = text.lower()
    assert (
        "never becomes an approval request" in lowered
        or "never an approval request" in lowered
        or "authorizes no action" in lowered
        or "永不构成" in lowered
        or "审批请求" in lowered
    ), "the owner must state that a report is a one-way statement that authorizes nothing"


# --------------------------------------------------------------------------- #
# T012 (US1) — the status report: attribution, the four elements, the boundary
# trigger, the Template's authority, and the Template on both sides of the pair
# --------------------------------------------------------------------------- #
REPORTER_TEMPLATE = REPO_ROOT / "agents" / "reporter.agent.md"
REPORTER_TEMPLATE_MIRROR = REPO_ROOT / ".specify" / "agents" / "templates" / "reporter.agent.md"
STATUS_DIGEST = REPO_ROOT / "scripts" / "python" / "status-digest.py"

#: The two structures the attribution fixture renders. Two lines MUST be tellable apart by their own fields.
STRUCTURES = (
    ("alpha-team", "r20261106T000000Z-aaaa"),
    ("beta-team", "r20261106T000000Z-bbbb"),
)


def _status_line(digest: Path, structure: str, run_stamp: str, **elements) -> str:
    """Render one status line through the delivered renderer (``--action report``)."""
    args = [
        sys.executable,
        str(digest),
        "--action",
        "report",
        "--structure",
        structure,
        "--run-stamp",
        run_stamp,
        "--position",
        elements.get("position", "stage-2 of 4"),
        "--delta",
        elements.get("delta", "one deliverable landed"),
        "--remainder",
        elements.get("remainder", "two stages left; about 10 minutes"),
        "--trigger",
        elements.get("trigger", "tick"),
    ]
    if "blocker" in elements:
        args.extend(["--blocker", elements["blocker"]])
    if "delay_reason" in elements:
        args.extend(["--delay-reason", elements["delay_reason"]])
    if "cadence" in elements:
        args.extend(["--cadence", elements["cadence"]])
    return args


def _render(digest: Path, structure: str, run_stamp: str, **elements):
    """Run the renderer over an empty registry so the profile is deterministic and no live state leaks in."""
    env = dict(os.environ)
    env["SPECIFY_LINE_REGISTRY_DIR"] = str(_EMPTY_REGISTRY)
    return subprocess.run(
        _status_line(digest, structure, run_stamp, **elements),
        capture_output=True,
        text=True,
        env=env,
    )


def _digest_ready() -> Path:
    assert STATUS_DIGEST.is_file(), (
        "status-digest.py missing: %s — expected at T009" % STATUS_DIGEST.relative_to(REPO_ROOT)
    )
    return STATUS_DIGEST


_EMPTY_REGISTRY: Path | None = None


@pytest.fixture(scope="module", autouse=True)
def _empty_registry(tmp_path_factory):
    """An empty, readable registry: the renderer resolves it, finds nothing, and selects the interactive profile.

    An autouse fixture (rather than a named one) because the helper is called from module-level code paths that
    pytest would not otherwise inject into; the directory is created once per module and never written to.
    """
    global _EMPTY_REGISTRY
    _EMPTY_REGISTRY = tmp_path_factory.mktemp("registry")
    yield _EMPTY_REGISTRY


def test_attribution_is_present_and_two_structures_are_distinguishable():
    """C-22 / SR-01: every line names its structure slug and run stamp; two structures never render identically."""
    digest = _digest_ready()
    rendered = []
    for structure, run_stamp in STRUCTURES:
        proc = _render(digest, structure, run_stamp)
        assert proc.returncode == 0, (
            "the renderer must emit one line for %r; rc=%s stderr=%r"
            % (structure, proc.returncode, proc.stderr)
        )
        line = proc.stdout.strip()
        assert line, "the renderer printed nothing"
        assert "\n" not in line, "a status line is ONE line; got %r" % line
        assert structure in line, "the line must name the structure slug %r; got %r" % (structure, line)
        assert run_stamp in line, "the line must name the run stamp %r; got %r" % (run_stamp, line)
        rendered.append(line)

    assert len(set(rendered)) == 2, (
        "two structures must not be able to produce an identical line; got %r" % (rendered,)
    )


def test_an_empty_attribution_field_is_refused():
    """C-22: an absent attribution field is an input error, never a silently unattributed line."""
    digest = _digest_ready()
    env = dict(os.environ)
    env["SPECIFY_LINE_REGISTRY_DIR"] = str(_EMPTY_REGISTRY)
    proc = subprocess.run(
        [
            sys.executable,
            str(digest),
            "--action",
            "report",
            "--structure",
            "alpha-team",
            "--position",
            "stage-2 of 4",
            "--delta",
            "one deliverable landed",
            "--remainder",
            "two stages left",
        ],
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode != 0, (
        "omitting the run stamp must be refused rather than rendered as an unattributed line;"
        " stdout=%r" % proc.stdout
    )


def test_four_content_elements_and_the_explicit_no_blocker():
    """C-23 / SR-02 by way of the labels: all four present, and `no blocker` written when none exists."""
    digest = _digest_ready()
    proc = _render(digest, "alpha-team", "r20261106T000000Z-aaaa")
    assert proc.returncode == 0, "renderer failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    line = proc.stdout.strip()
    for label in ELEMENT_LABELS:
        assert "%s=" % label in line, (
            "the line must carry the %r element (its definition is reached by anchor, contract C-23); got %r"
            % (label, line)
        )
    assert "no blocker" in line, (
        "when there is no blocker the line MUST write the explicit negation, not an empty value; got %r" % line
    )


def test_an_explicit_blocker_is_rendered_verbatim():
    """C-23's other half: an actual blocker is carried, and the explicit negation is not additionally written."""
    digest = _digest_ready()
    proc = _render(digest, "alpha-team", "r20261106T000000Z-aaaa", blocker="upstream registry is unreadable")
    assert proc.returncode == 0, "renderer failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    line = proc.stdout.strip()
    assert "upstream registry is unreadable" in line
    assert "no blocker" not in line, (
        "a real blocker must replace the explicit negation, never appear beside it; got %r" % line
    )


def test_boundary_trigger_is_rendered_without_a_cadence_reset():
    """C-25 / SR-04: a boundary line names its trigger; it does not restart the periodic cadence."""
    digest = _digest_ready()
    tick = _render(digest, "alpha-team", "r20261106T000000Z-aaaa", trigger="tick")
    boundary = _render(digest, "alpha-team", "r20261106T000000Z-aaaa", trigger="boundary")
    assert tick.returncode == 0 and boundary.returncode == 0
    assert "trigger=tick" in tick.stdout, "the default trigger must render as `tick`; got %r" % tick.stdout
    assert "trigger=boundary" in boundary.stdout, (
        "a crossed stage boundary must render its own trigger kind; got %r" % boundary.stdout
    )
    # The out-of-cadence line is an EXTRA line: it carries the same attribution and its own trigger, and nothing in
    # the rendering re-anchors the clock (the anchor is the owner's, reached by path — this asserts the shape only).
    assert "alpha-team" in boundary.stdout and "r20261106T000000Z-aaaa" in boundary.stdout
    assert "anchor" not in boundary.stdout.lower(), (
        "the boundary line must not re-declare a cadence anchor; the cadence continues on its original one"
    )


def test_a_tick_delayed_to_the_next_boundary_states_its_delay():
    """C-25: a tick delivered at the next step boundary states the delay instead of splitting the step."""
    digest = _digest_ready()
    proc = _render(
        digest,
        "alpha-team",
        "r20261106T000000Z-aaaa",
        trigger="tick",
        delay_reason="delivered at the next step boundary (an indivisible step was running)",
    )
    assert proc.returncode == 0, "renderer failed: rc=%s stderr=%r" % (proc.returncode, proc.stderr)
    assert "deliver" in proc.stdout.lower() or "delay" in proc.stdout.lower(), (
        "a delayed tick must state the delay; got %r" % proc.stdout
    )


def test_reporter_template_authority_deny_list():
    """C-19 / SR-06 (read here, authored by T014): no dispatch, spawn, authorize, retry or terminate tool."""
    assert REPORTER_TEMPLATE.is_file(), (
        "the reporting Agent Template is missing: %s — expected at T014"
        % REPORTER_TEMPLATE.relative_to(REPO_ROOT)
    )
    frontmatter = REPORTER_TEMPLATE.read_text(encoding="utf-8").split("---", 2)[1]
    match = re.search(r"^capability-tools:\s*\[(.*?)\]", frontmatter, re.M | re.S)
    assert match, "the Template must declare capability-tools as a list value"
    tools = {item.strip() for item in match.group(1).split(",") if item.strip()}
    denied = {"Agent", "Task", "Bash", "Kill", "Retry", "Approve", "Dispatch", "Workflow"}
    assert not (tools & denied), (
        "the reporter must not hold dispatching/authorizing tools; held %r" % sorted(tools & denied)
    )
    assert {"Read"} <= tools, "the reporter must be able to read the state it reports"


def test_reporter_template_exists_on_both_sides_of_the_pair():
    """C-14 / RS-01 (existence + byte equal): source and mirror both resolve, byte-identically."""
    assert REPORTER_TEMPLATE.is_file(), (
        "the framework-source Template is missing: %s" % REPORTER_TEMPLATE.relative_to(REPO_ROOT)
    )
    assert REPORTER_TEMPLATE_MIRROR.is_file(), (
        "the mirror %s must be produced by sync-mirrors.py (agents/ → .specify/agents/templates/);"
        " a source-only file never reaches a downstream project"
        % REPORTER_TEMPLATE_MIRROR.relative_to(REPO_ROOT)
    )
    assert REPORTER_TEMPLATE.read_bytes() == REPORTER_TEMPLATE_MIRROR.read_bytes(), (
        "the agents/ and .specify/agents/templates/ copies of reporter.agent.md differ"
    )


def test_reporter_template_is_framework_neutral():
    """The Template is distributed to every project, so it carries no repository-specific identifier."""
    assert REPORTER_TEMPLATE.is_file(), "the reporting Agent Template is missing (expected at T014)"
    text = REPORTER_TEMPLATE.read_text(encoding="utf-8")
    for token in ("spec-kit", "cloud-native-ai", "/Users/"):
        assert token not in text, "project-specific token %r leaked into the Template" % token


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _declaration_block(text: str) -> str:
    """Return the declaration region: from the single-source line to the first horizontal rule.

    The declaration sits inside a blockquote in the house shape its siblings use, so the block is unwrapped to its
    logical lines before the caller counts or scans it — a `> 1. …` line is a list item, not a quotation.
    """
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        lowered = line.lower()
        if "single source of truth" in lowered or "单一定义源" in line or "唯一定义" in line:
            start = index
            break
    assert start is not None, "no single-source-of-truth declaration line found"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    block = []
    for line in lines[start:end]:
        stripped = line.lstrip()
        if stripped.startswith(">"):
            stripped = stripped[1:]
            if stripped.startswith(" "):
                stripped = stripped[1:]
            block.append(stripped)
        else:
            block.append(line)
    return "\n".join(block)


def _section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.strip() == heading), None)
    if start is None:
        return ""
    end = next(
        (j for j in range(start + 1, len(lines)) if lines[j].startswith(("## ", "# "))),
        len(lines),
    )
    return "\n".join(lines[start:end])
