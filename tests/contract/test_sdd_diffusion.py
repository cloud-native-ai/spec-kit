"""Contract tests: diffusion of SDD vocabulary into the Goal/Team/Agent surfaces (slice 074b, T010).

What this pins
--------------
`contracts/diffusion.md` C-13…C-20 at the decidable face:

1. the team Stage dimension keeps its three values and gains the disambiguation that it is *not*
   the SDD stage roster, whose only owner is the driver (C-13);
2. no surface this slice touches enumerates the roster — the roster is read from the driver's own
   fixed-order statement, never restated here as a literal list (C-14);
3. the shipped stage-executor preset declares no hosting capability, asserted against the artifact
   (C-15);
4. a hosting declaration and its three responsibility statements are read **together**: a
   declaration without the statements fails, and the statements without the declaration fail
   (C-16);
5. the hosting rule sits immediately after the existing key paragraph in the authoring baseline and
   reaches the closed value domain by pointer (C-17);
6. the instructions carry exactly one pointer-level routing surface, restate none of the owner's
   facts, and declare their own byte ceiling (C-18);
7. the trigger discipline gains one conjunction sentence inside an existing section, without adding
   a section and without moving the gate-scan total (C-19);
8. the pointer is delivered as a generated section that the live file carries verbatim and that
   stays within its declared ceiling, while the compatibility instruction paths keep pointing at
   the live file (C-20);
9. every `[[STR-NNN]]` citation in this slice resolves to a row of `requirements.md` § Shared
   Strings.

Measurement rules used below
----------------------------
* **The roster is read, never copied.** `_sdd_stage_roster()` parses the driver's own fixed-order
  statement (`skills/external/sdd-loop-driver/references/dispatch-recipes.md`), so a change to the
  roster reaches this suite instead of silently disagreeing with a frozen list here.
* **The reverse audit's query set comes from the landed owner.** `_routing_owner_query_set()`
  extracts the backticked tokens of the routing owner's `§ Inputs` / `§ Verdict table` /
  `§ Reason codes`, and only then counts them in the new text — the One-Source-Of-Truth prohibition
  on "phrases I think were written" is exactly what makes a copy detector work.
* **"Added text" is located by its own anchor**, not by diffing a frozen snapshot: the Stage bullet
  line, the authoring-baseline paragraph that carries the hosting rule, the template section that
  names the routing owner, and the trigger sentence that names both halves of the conjunction. Each
  anchor is itself asserted, so removing the anchor fails rather than silently skipping a check.
* **The C-16 criterion is executed, not asserted.** `_hosting_violations()` applies the criterion to
  synthetic definitions in both directions plus to the shipped preset; a prose-only test of "the
  declaration is read together with the text" would prove nothing.

Red shape (recorded in `notes/red-first-evidence.md` § E-4): none of the four diffusion surfaces is
landed yet, so the surface cases fail as *absent statements/sections*. The invariance cases
(C-14's absence, C-15's leaf preset, C-19's section set and gate total, the STR resolution) are green
before the edit by construction and stay green after it — they are the pins that would go red if this
slice broke their subject, which is the only way an invariant case is worth writing.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SLICE_DIR = REPO_ROOT / ".specify" / "specs" / "074b-nested-governance"

CONCEPTUAL_MODEL = REPO_ROOT / "skills" / "internal" / "create-team" / "references" / "conceptual-model.md"
RUN_AGENT = REPO_ROOT / "skills" / "internal" / "run-agent" / "SKILL.md"
INSTRUCTIONS_TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
LIVE_INSTRUCTIONS = REPO_ROOT / ".specify" / "instructions.md"
TRIGGER_DOC = REPO_ROOT / "shared" / "guidelines" / "proactive-trigger.md"

#: The delivered artifact C-15's negative assertion is made against.
STAGE_EXECUTOR_PRESET = REPO_ROOT / "agents" / "sdd-executor.agent.md"
#: The routing owner the instructions pointer reaches by path (C-18).
ROUTING_OWNER = REPO_ROOT / "shared" / "definitions" / "sdd-routing-definitions.md"
#: The driver's own stage-chain statement — the roster's single owner (C-13 / C-14).
ROSTER_OWNER = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "dispatch-recipes.md"
#: The neutral key set's owner, cited for the closed value domain and its default (C-17).
KEY_SET_OWNER = REPO_ROOT / "src" / "specify_cli" / "__init__.py"
#: `[[STR-NNN]]`'s registry.
SHARED_STRINGS_OWNER = SLICE_DIR / "requirements.md"
#: The confirmation-gate scanner, used for C-19's "the edit moves no gate" clause.
GATE_SCANNER = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
#: `tests/contract/test_proactive_trigger_section.py` owns the closed, ordered section set of the
#: trigger document (its C-2). Reading that owner beats copying its list here.
TRIGGER_SECTION_SET_OWNER = REPO_ROOT / "tests" / "contract" / "test_proactive_trigger_section.py"

#: `[[STR-001]]` / `[[STR-002]]` — the capability key and its positive declaration value.
INVOCATION_KEY = "sdd-invocation"
DECLARED_ALLOWED = "allowed"
#: The domain's *other* member. C-17 forbids restating the domain, so the rule may name the
#: declaration it obliges and must not enumerate both values.
DOMAIN_SIBLING = "forbidden"

#: C-13's team Stage vocabulary, verbatim and in order. Renaming or overloading one of these is the
#: violation; a fourth value is as much a violation as a rename.
TEAM_STAGE_VALUES = ("executor", "evaluator", "optimizer")

#: C-16's three responsibility statements, as the authoring baseline must phrase them.
RESPONSIBILITY_STATEMENTS = ("承载驱动", "自身不执行", "止于 review")

#: C-19's conjunction halves, as the trigger sentence must name them.
CONJUNCTION_HALVES = ("分流裁决", "`allowed`")

#: The gate-scan total measured at the pre-change commit (2026-10-29, before this slice's trigger
#: edit; the same 27 recorded in `test-evidence/targeted-set-v1-baseline.txt`). The frozen 23 in
#: `baseline-gates.json` is a **pre-existing** red belonging to four earlier features and is not
#: this slice's to repair — C-19's criterion is therefore "the total measured after the edit equals
#: the total measured before it".
PRE_CHANGE_GATE_TOTAL = 27

#: C-20's four compatibility instruction paths (they are symlinks at the live file).
COMPATIBILITY_PATHS = ("AGENTS.md", "CLAUDE.md", "QODER.md", ".github/copilot-instructions.md")


# ---------------------------------------------------------------------------
# Parsing helpers — fence-aware, so fenced template text never reads as a heading
# ---------------------------------------------------------------------------


def _read(path: Path) -> str:
    assert path.is_file(), f"missing document: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _fence_flags(text: str) -> list:
    rows = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            rows.append(True)
            continue
        rows.append(in_fence)
    return rows


def _sections(text: str) -> list:
    """`[(title, body)]` for real level-2 headings only."""
    lines = text.splitlines()
    flags = _fence_flags(text)
    heads = [
        (index, line[3:].strip())
        for index, line in enumerate(lines)
        if line.startswith("## ") and not flags[index]
    ]
    blocks = []
    for position, (index, title) in enumerate(heads):
        end = len(lines)
        if position + 1 < len(heads):
            end = heads[position + 1][0]
        blocks.append((title, "\n".join(lines[index + 1 : end])))
    return blocks


def _section(path: Path, title: str) -> str:
    hits = [body for name, body in _sections(_read(path)) if name == title]
    assert len(hits) == 1, (
        f"{path.relative_to(REPO_ROOT)} must carry exactly one `## {title}` section, found {len(hits)}"
    )
    return hits[0]


def _paragraphs(body: str) -> list:
    return [block.strip() for block in re.split(r"\n\s*\n", body) if block.strip()]


def _section_starting(path: Path, prefix: str) -> str:
    """Body of the one section whose title *starts with* ``prefix``.

    The literal registry's heading carries a parenthetical suffix
    (`## Shared Strings *(optional, recommended …)*`), so an exact-title lookup would be a
    spelling test rather than a structural one.
    """
    hits = [body for name, body in _sections(_read(path)) if name.startswith(prefix)]
    assert len(hits) == 1, (
        f"{path.relative_to(REPO_ROOT)} must carry exactly one `## {prefix}…` section, found "
        f"{len(hits)}"
    )
    return hits[0]


def _sdd_stage_roster() -> list:
    """The SDD stage roster, parsed from the driver's own fixed-order statement."""
    text = _read(ROSTER_OWNER)
    match = re.search(r"阶段链固定顺序[:：]\s*`([^`]+)`", text)
    assert match, (
        "the driver's fixed-order stage statement was not found in "
        f"{ROSTER_OWNER.relative_to(REPO_ROOT)}; the roster has no readable owner for this audit"
    )
    roster = [part.strip() for part in match.group(1).split("→")]
    assert len(roster) >= 5, f"the parsed roster looks truncated: {roster}"
    return roster


def _routing_owner_query_set() -> set:
    """Backticked tokens of the routing owner's F-1 / F-2 / F-4 sections."""
    owner = _read(ROUTING_OWNER)
    audited = ("Inputs", "Verdict table", "Reason codes")
    tokens = set()
    for title, body in _sections(owner):
        if title.strip() in audited:
            tokens |= set(re.findall(r"`([^`\n]+)`", body))
    assert tokens, "the routing owner's audited sections yielded no tokens; the audit would be vacuous"
    return tokens


def _restated_owner_facts(text: str) -> list:
    """Owner tokens that reappear in ``text`` — the reverse count C-18 requires to be zero."""
    hits = []
    for token in sorted(_routing_owner_query_set()):
        if f"`{token}`" in text:
            hits.append(f"`{token}`")
        elif re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{2,}", token) and re.search(
            rf"(?<![A-Za-z0-9_-]){re.escape(token)}(?![A-Za-z0-9_-])", text
        ):
            hits.append(token)
    return hits


def _frontmatter_keys(text: str) -> set:
    assert text.startswith("---\n"), "document has no frontmatter block"
    block = text.split("---\n", 2)[1]
    return {
        line.split(":", 1)[0].strip()
        for line in block.splitlines()
        if line.strip() and not line.lstrip().startswith("#") and ":" in line
    }


def _frontmatter_value(text: str, key: str):
    block = text.split("---\n", 2)[1]
    for line in block.splitlines():
        if line.split(":", 1)[0].strip() == key and ":" in line:
            return line.split(":", 1)[1].strip()
    return None


# ---------------------------------------------------------------------------
# C-13 / C-14 — the Stage dimension is disambiguated; nothing is renamed
# ---------------------------------------------------------------------------


def _stage_bullet() -> str:
    lines = [line for line in _read(CONCEPTUAL_MODEL).splitlines() if line.startswith("- **Stage**")]
    assert len(lines) == 1, f"expected exactly one Stage bullet, found {len(lines)}"
    return lines[0]


def test_stage_bullet_keeps_the_three_values_and_gains_the_disambiguation():
    bullet = _stage_bullet()
    stated = re.findall(r"`([^`]+)`", bullet.split("(canonical names")[0])
    assert tuple(stated) == TEAM_STAGE_VALUES, (
        "the Stage dimension MUST keep exactly its three canonical values, in order, with none "
        f"renamed and no SDD stage name added (C-13); found {stated}"
    )
    assert "SDD" in bullet and re.search(r"阶段名册|roster", bullet), (
        "the added text MUST state that this dimension is not the SDD stage roster (C-13)"
    )
    assert re.search(r"不是|not the", bullet), "the statement must be a negation, not a hint (C-13)"
    assert "sdd-loop-driver" in bullet, (
        "the statement MUST name the roster's owner — the driver — by path (C-13)"
    )


def _added_texts() -> list:
    """`[(label, text)]` — the four diffusion surfaces this slice adds text to."""
    hosting = _hosting_paragraph()
    routing = _routing_pointer_section()
    return [
        ("conceptual-model Stage bullet", _stage_bullet()),
        ("run-agent authoring baseline (hosting rule)", hosting),
        ("instructions routing pointer section", routing[0] + "\n" + routing[1]),
        ("trigger conjunction sentence", _conjunction_sentence()),
    ]


def test_no_added_surface_enumerates_the_sdd_stage_roster():
    roster = _sdd_stage_roster()
    chain = " → ".join(roster)
    for label, text in _added_texts():
        assert chain not in text, (
            f"{label} repeats the driver's stage chain verbatim; the roster is reached by path and "
            "never restated (C-14)"
        )
        for line in text.splitlines():
            names = {
                name
                for name in roster
                if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(name)}(?![A-Za-z0-9_-])", line, re.I)
            }
            assert len(names) < 2, (
                f"{label} carries a roster-shaped enumeration ({sorted(names)} on one line); at "
                "most a single stage name may appear, and only where a contract requires it (C-14)"
            )


# ---------------------------------------------------------------------------
# C-15 — the shipped stage-executor preset stays a leaf, asserted on the artifact
# ---------------------------------------------------------------------------


def test_shipped_stage_executor_preset_declares_no_hosting_capability():
    text = _read(STAGE_EXECUTOR_PRESET)
    assert INVOCATION_KEY not in _frontmatter_keys(text), (
        f"the shipped preset {STAGE_EXECUTOR_PRESET.relative_to(REPO_ROOT)} MUST NOT declare "
        f"{INVOCATION_KEY!r}: a stage executor is a leaf (C-15)"
    )
    assert INVOCATION_KEY not in text, (
        "the leaf boundary MUST be asserted against the delivered artifact, so the artifact must "
        f"not carry the key anywhere (C-15); found at "
        f"{[n for n, line in enumerate(text.splitlines(), 1) if INVOCATION_KEY in line]}"
    )
    assert _hosting_violations(_frontmatter_value(text, INVOCATION_KEY), text) == [], (
        "the preset must satisfy the hosting criterion trivially: no declaration, no responsibility "
        "claim, nothing to fail (C-15 / C-16)"
    )


# ---------------------------------------------------------------------------
# C-16 — the declaration and the responsibility text are read together
# ---------------------------------------------------------------------------


def _hosting_violations(declaration, body: str) -> list:
    """The C-16 criterion, applied to one definition.

    Both directions fail: a declaration without the three statements, and the three statements
    without the declaration. Nothing here inspects the file's name or its declared responsibility —
    the criterion is the co-presence of the declaration and the statements.
    """
    declares = declaration is not None and declaration.strip().strip('"') == DECLARED_ALLOWED
    missing = [item for item in RESPONSIBILITY_STATEMENTS if item not in body]
    problems = []
    if declares and missing:
        problems.append(f"declares {DECLARED_ALLOWED!r} without stating {missing}")
    if not declares and not missing:
        problems.append(f"states all three hosting responsibilities without declaring {DECLARED_ALLOWED!r}")
    return problems


def _hosting_paragraph() -> str:
    paragraphs = _paragraphs(_section(RUN_AGENT, "Authoring Baseline"))
    hits = [p for p in paragraphs if INVOCATION_KEY in p and RESPONSIBILITY_STATEMENTS[0] in p]
    assert len(hits) == 1, (
        "the authoring baseline must carry exactly one hosting-responsibility paragraph (C-17), "
        f"found {len(hits)}"
    )
    return hits[0]


def test_hosting_rule_states_the_three_responsibilities_and_the_together_reading():
    paragraph = _hosting_paragraph()
    for statement in RESPONSIBILITY_STATEMENTS:
        assert statement in paragraph, (
            f"the hosting rule MUST state the responsibility {statement!r} (C-16)"
        )
    assert re.search(r"一起被读取|read together|同时.*读取", paragraph), (
        "the rule MUST require the declaration and the responsibility text to be read together "
        "(C-16)"
    )
    assert re.search(r"只有声明[^。]{0,40}判不合规", paragraph), (
        "the rule MUST state the declaration-without-statements failure (C-16)"
    )
    assert re.search(r"没有声明[^。]{0,40}判不合规|反之", paragraph), (
        "the rule MUST state the statements-without-declaration failure as well (C-16)"
    )
    assert STAGE_EXECUTOR_PRESET.name in paragraph, (
        "the leaf prohibition MUST be asserted against the shipped preset "
        f"`{STAGE_EXECUTOR_PRESET.name}`, not against a convention (C-15)"
    )
    assert DOMAIN_SIBLING not in paragraph, (
        f"the rule MUST NOT enumerate the closed domain: {DOMAIN_SIBLING!r} appears in it, which "
        "restates the pair whose owner is the neutral key set (C-17)"
    )


def test_the_hosting_criterion_fails_in_both_directions():
    statements = " / ".join(RESPONSIBILITY_STATEMENTS)
    assert _hosting_violations(DECLARED_ALLOWED, statements) == [], (
        "a declaration together with the three statements must pass the criterion (C-16)"
    )
    declared_only = _hosting_violations(DECLARED_ALLOWED, "hosts work, nothing else")
    assert declared_only, "a declaration without the three statements must fail (C-16)"
    statements_only = _hosting_violations(None, statements)
    assert statements_only, "the three statements without the declaration must fail (C-16)"
    assert _hosting_violations(None, "no declaration, no claim") == [], (
        "a definition that hosts nothing must pass: the rule obliges hosts, it does not require "
        "every agent to host (C-16)"
    )


# ---------------------------------------------------------------------------
# C-17 — the rule sits where an author reads, and reaches the domain by pointer
# ---------------------------------------------------------------------------


def test_hosting_rule_sits_immediately_after_the_existing_key_paragraph():
    paragraphs = _paragraphs(_section(RUN_AGENT, "Authoring Baseline"))
    key_index = [
        index
        for index, paragraph in enumerate(paragraphs)
        if INVOCATION_KEY in paragraph and "capability key" in paragraph
    ]
    assert len(key_index) == 1, (
        "the pre-existing `sdd-invocation` paragraph must still be present exactly once (C-17)"
    )
    hosting_index = paragraphs.index(_hosting_paragraph())
    assert hosting_index == key_index[0] + 1, (
        "the hosting rule MUST land immediately after the existing key paragraph (C-17); found at "
        f"index {hosting_index}, expected {key_index[0] + 1}"
    )


def test_hosting_rule_points_at_the_key_set_owner_and_restates_no_domain():
    paragraph = _hosting_paragraph()
    assert "src/specify_cli/__init__.py" in paragraph, (
        "the rule MUST point at the key set's owner for the closed values (C-17)"
    )
    assert "NEUTRAL_AGENT_METADATA_KEYS" in paragraph, (
        "the rule MUST name the key-set constant whose entry owns the domain (C-17)"
    )
    for enum_shape in (
        re.compile(rf"`?{DECLARED_ALLOWED}`?\s*(?:/|、|,|\||或)\s*`?{DOMAIN_SIBLING}`?"),
        re.compile(r"\{\s*\"?allowed\"?\s*,\s*\"?forbidden\"?\s*\}"),
    ):
        assert not enum_shape.search(paragraph), (
            "the rule MUST NOT restate the closed value domain as an enumeration (C-17)"
        )
    assert "不渲染" in paragraph or "never rendered" in paragraph, (
        "the rule MUST reach the non-rendering fact by pointer rather than omitting it (C-17)"
    )


# ---------------------------------------------------------------------------
# C-18 — one pointer-level routing surface, restating nothing
# ---------------------------------------------------------------------------


def _routing_pointer_sections(path: Path) -> list:
    return [
        (title, body, f"## {title}\n{body}".strip())
        for title, body in _sections(_read(path))
        if "sdd-routing-definitions.md" in body
    ]


def _routing_pointer_section() -> tuple:
    hits = _routing_pointer_sections(INSTRUCTIONS_TEMPLATE)
    assert len(hits) == 1, (
        "the instructions MUST carry exactly one pointer-level routing surface (C-18); sections "
        f"naming the routing owner: {[title for title, _b, _t in hits]}"
    )
    return hits[0][0], hits[0][1]


def test_instructions_carry_exactly_one_routing_pointer_section():
    heading, body = _routing_pointer_section()
    assert heading.startswith("SDD") or "Routing" in heading or "分流" in heading, (
        f"the pointer section's title must name its subject; got {heading!r}"
    )
    assert re.search(r"写留存|write-bearing", body), (
        "the pointer MUST name the trigger: a write-bearing change is what sends the reader to the "
        "owner (C-18)"
    )
    assert re.search(r"所有者|owner", body), (
        "the pointer MUST name the routing owner as the decision's owner (C-18)"
    )
    assert "sdd-route.py" in body, (
        "the pointer MUST name the executable form the reader runs at the owner's path (C-18)"
    )


def test_instructions_pointer_restates_no_owner_fact():
    _heading, body = _routing_pointer_section()
    restated = _restated_owner_facts(body)
    assert restated == [], (
        "the pointer MUST NOT restate the owner's input set, closed value domains, verdict table, "
        f"precedence or reason-code vocabulary (C-18); restated tokens: {restated}"
    )
    assert not re.search(r"(?m)^\|\s*[^|\n]+\|\s*[^|\n]+\|", body), (
        "the pointer MUST NOT carry a table — the verdict table and the input set live in the "
        "owner (C-18)"
    )


def test_instructions_section_declares_and_respects_its_own_byte_ceiling():
    _heading, body = _routing_pointer_section()
    match = re.search(r"字节上限[:：]?\s*\**\s*([0-9][0-9,]*)\s*B", body)
    assert match, (
        "the section MUST declare its own byte ceiling: both instruction files already exceeded the "
        "generator's budget before this slice, so the acceptance criterion is a declared ceiling "
        "plus a measured delta (C-18 / C-20)"
    )
    ceiling = int(match.group(1).replace(",", ""))
    measured = len(body.encode("utf-8"))
    assert measured <= ceiling, (
        f"the section measures {measured} B, above its own declared ceiling of {ceiling} B (C-18)"
    )
    assert not re.search(r"装得下|fits the budget", body), (
        "the section MUST NOT claim budget conformance — that claim is false before and after this "
        "slice (C-18)"
    )


# ---------------------------------------------------------------------------
# C-19 — one conjunction sentence in the existing trigger section, no new gate
# ---------------------------------------------------------------------------


def _conjunction_sentence() -> str:
    body = _section(TRIGGER_DOC, "Promotion & Safety Boundary")
    hits = [
        sentence
        for sentence in re.split(r"(?<=。)", body)
        if all(half in sentence for half in CONJUNCTION_HALVES)
    ]
    assert len(hits) == 1, (
        "the trigger discipline MUST gain exactly one sentence carrying both halves of the "
        f"promotion conjunction (C-19); found {len(hits)}"
    )
    return hits[0]


def test_trigger_gains_the_conjunction_sentence_inside_an_existing_section():
    sentence = _conjunction_sentence()
    assert "SDD" in sentence, "the conjunction is about promoting an SDD run (C-19)"
    assert re.search(r"同时|both", sentence), (
        "the sentence MUST state the two halves as a conjunction, not as two separate hints (C-19)"
    )
    assert "shared/definitions/sdd-routing-definitions.md" in sentence, (
        "the conjunction is owned by the routing owner and reached from here by pointer (C-19)"
    )
    assert re.search(r"指针|pointer", sentence), (
        "the sentence MUST declare itself a pointer rather than a rule copy (C-19)"
    )
    whole = _read(TRIGGER_DOC)
    duplicates = [
        line
        for line in whole.splitlines()
        if all(half in line for half in CONJUNCTION_HALVES)
    ]
    assert len(duplicates) == 1, (
        "the conjunction MUST be stated once in this document (C-19); lines carrying both halves: "
        f"{[line[:70] for line in duplicates]}"
    )
    assert _restated_owner_facts(sentence) == [], (
        "the pointer MUST NOT drag the owner's input set, verdict table or reason codes into the "
        f"trigger discipline (C-19); restated tokens: {_restated_owner_facts(sentence)}"
    )


def test_trigger_section_set_stays_the_delivered_closed_set():
    owner = importlib.util.spec_from_file_location(
        "trigger_section_set_owner", TRIGGER_SECTION_SET_OWNER
    )
    module = importlib.util.module_from_spec(owner)
    owner.loader.exec_module(module)
    expected = list(module.DOC_SECTIONS)
    found = [title for title, _body in _sections(_read(TRIGGER_DOC))]
    assert found == expected, (
        "the trigger document's `## ` section set is a delivered closed, ordered set (its owner is "
        f"`{TRIGGER_SECTION_SET_OWNER.name}` C-2); this slice may add a sentence inside a section "
        f"and nothing else. expected {expected}, found {found}"
    )
    assert "SDD" not in " ".join(found), (
        "no new SDD-shaped section may be created in the trigger discipline (C-19)"
    )


def test_trigger_edit_moves_no_gate():
    proc = subprocess.run(
        ["python3", str(GATE_SCANNER), "--root", str(REPO_ROOT), "--json"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    total = json.loads(proc.stdout)["total"]
    assert total == PRE_CHANGE_GATE_TOTAL, (
        f"the confirmation-gate scan total moved from the pre-change {PRE_CHANGE_GATE_TOTAL} to "
        f"{total}; the headroom on that budget is 0, so this slice's sentence must add no "
        "gate-scannable declaration (C-19)"
    )


# ---------------------------------------------------------------------------
# C-20 — the pointer is a generated section, carried verbatim by the live file
# ---------------------------------------------------------------------------


def test_generated_instructions_carry_the_section_verbatim_and_follow_the_symlinks():
    heading, body = _routing_pointer_section()
    live_sections = {title: block for title, block in _sections(_read(LIVE_INSTRUCTIONS))}
    assert heading in live_sections, (
        f"the live instructions file does not carry the `## {heading}` section; the pointer is "
        "delivered by regeneration, and hand-editing the live file is forbidden (C-20)"
    )
    assert live_sections[heading].strip() == body.strip(), (
        "the live section MUST be the template's section verbatim: it is produced by "
        "`scripts/bash/generate-instructions.sh`, not written by hand (C-20)"
    )
    ceiling = int(
        re.search(r"字节上限[:：]?\s*\**\s*([0-9][0-9,]*)\s*B", body).group(1).replace(",", "")
    )
    measured = len((f"## {heading}\n{live_sections[heading]}").strip().encode("utf-8"))
    assert measured <= ceiling, (
        f"the live section measures {measured} B, above the section's declared {ceiling} B (C-20)"
    )
    broken = []
    for rel in COMPATIBILITY_PATHS:
        path = REPO_ROOT / rel
        if not path.is_symlink():
            broken.append(f"{rel}: not a symlink")
            continue
        if path.resolve() != LIVE_INSTRUCTIONS.resolve():
            broken.append(f"{rel}: resolves to {path.resolve()}")
    assert not broken, (
        "the compatibility instruction paths MUST keep pointing at the live instructions file, so "
        f"the regenerated section reaches every tool (C-20); broken: {broken}"
    )


# ---------------------------------------------------------------------------
# Shared strings — every `[[STR-NNN]]` citation resolves to a row
# ---------------------------------------------------------------------------


def _shared_string_ids() -> set:
    section = _section_starting(SHARED_STRINGS_OWNER, "Shared Strings")
    return set(re.findall(r"(?m)^\|\s*`(STR-\d{3})`\s*\|", section))


def test_every_shared_string_citation_resolves_to_a_registry_row():
    ids = _shared_string_ids()
    assert ids, "requirements.md § Shared Strings yielded no rows; the check would be vacuous"
    citing_documents = sorted(SLICE_DIR.rglob("*.md")) + [Path(__file__).resolve()]
    dangling = {}
    for document in citing_documents:
        text = document.read_text(encoding="utf-8", errors="ignore")
        cited = set(re.findall(r"\[\[(STR-\d{3})\]\]", text))
        unresolved = sorted(cited - ids)
        if unresolved:
            dangling[str(document.relative_to(REPO_ROOT))] = unresolved
    assert not dangling, (
        "every `[[STR-NNN]]` citation MUST resolve to a row of `requirements.md` § Shared Strings "
        f"(the literal registry); unresolved: {dangling}"
    )
