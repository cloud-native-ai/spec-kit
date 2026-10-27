"""Contract test: the feedback boundary and the protected invariants (Feature 071).

Pins `contracts/feedback-and-boundaries.md` C-55…C-63 against the surfaces that
carry them — `templates/commands/review.md`, `skills/internal/code-review/SKILL.md`,
and (for the predecessor invariants only) `.specify/shared/workflow/feedback-step.md`,
which owns the feedback mechanism and is cited here rather than redefined:

* C-55 — the review command's closing step set stays exactly as published (run
  determination, execution quantification, feedback record, threshold notice,
  token reflection, docs-sync evaluation: six steps, in that order), and each
  delegated skill keeps its own five-step face. This feature adds no closing
  step, no side channel and no second record type; the compiled face is not
  edited, so the new rule text MUST sit outside it.
* C-56 — a feedback entry records friction of the framework itself; a code
  defect found by the code segment MUST NOT be posted as a feedback entry. It
  stays in `code-review.md`, where its severity, file and line are meaningful.
* C-57 — the classification duty is written into **two** surfaces (the command
  template and the code-review skill text), so posting a code defect as feedback
  is a detectable violation of a stated rule rather than a matter of taste. The
  two constructed samples below are judged against *that written rule*: the
  judge is parameterised by the duty it reads out of the surfaces, so deleting
  or weakening either surface takes the judgement away instead of leaving a
  green assertion behind.
* C-58 — in a nested run the unit census is **three**: `/speckit.review`,
  `skill:review-sdd-process`, `skill:code-review`. Each unit completes its own
  closing record; the command suppresses neither skill's wrap-up, writes no
  skill's run determination on its behalf and back-fills none after the fact.
* C-59 — three records coexist because the entry key is `(unit_id, run_id)`:
  within one run the units differ in `unit_id`, so none dedups another and none
  has to be merged or dropped. Driven against the real engine, both for the
  feedback store and for the run-determination session store. The clause MUST
  NOT be read as "a nested run produces only two entries".
* C-60 — the predecessor invariants stay in force unchanged (same-commit
  register entry, the introspection step as the legal entry for a framework-wide
  recommendation, `scope: local`, zero automated transmission, target = the
  framework rather than the feature).
* C-61 — no intake store, no second aggregation directory, no second id family,
  no upload path, and no new engine.
* C-62 — the code segment is an **additional** segment: for a feature with no
  code delta it is recorded `not-applicable`, and the reader-baseline judgement
  is neither replaced nor short-circuited. The expression-class review face
  keeps its owner (`shared/definitions/flow-class-definitions.md`), so this file
  cites it and restates no criterion of it.
* C-63 — the receipt's coverage counts **reviewed files** — the share of the
  changed-file set carrying a verdict — never test coverage and never compile
  coverage. The disambiguation runs in both directions: the receipt is never
  evidence for the reader-baseline judgement, and FR-027's prohibition targets
  the other object and therefore never forbids the receipt.

Red before the duty and the invariants land (Tests Mode = ON, Constitution
Principle IV): at the time this file was written `templates/commands/review.md`
ended its feedback obligations at the compiled `## Wrap-up` face and named no
classification duty and no unit census, and `skills/internal/code-review/SKILL.md`
carried neither the duty, nor its own closing obligation under a shared run id,
nor the receipt-versus-coverage disambiguation.

What this file deliberately does NOT pin: the receipt's grammar, its exit
alphabet and its count identity (C-31…C-44 own them), the merge gate's verdict
(C-26/C-27, C-46), the gate criteria (C-45…C-53), and the feedback mechanism
itself (`shared/workflow/feedback-step.md` owns it). A second copy here would be
the drift this feature exists to remove.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
REVIEW_CMD = ROOT / "templates" / "commands" / "review.md"
CODE_SKILL = ROOT / "skills" / "internal" / "code-review" / "SKILL.md"
PROCESS_SKILL = ROOT / "skills" / "internal" / "review-sdd-process" / "SKILL.md"
FEEDBACK_STEP = ROOT / ".specify" / "shared" / "workflow" / "feedback-step.md"
FEEDBACK_UTILS = ROOT / "scripts" / "python" / "feedback-utils.py"
RUN_DETERMINATION = ROOT / "scripts" / "python" / "run-determination.py"

#: The three units of one composed review run (requirements.md FR-018, C-58).
UNITS = ("/speckit.review", "skill:review-sdd-process", "skill:code-review")

#: The published closing step set, in order — owned by the compiled `## Wrap-up`
#: faces themselves; restated here only as the expectation a drift must break.
COMMAND_CLOSING_STEPS = (
    "Run Determination",
    "Exec Quant",
    "Feedback Record",
    "Threshold Notice",
    "Token Reflection",
    "Docs Sync Eval",
)
SKILL_CLOSING_STEPS = COMMAND_CLOSING_STEPS[:5]

#: The six-level code vocabulary, owned by the code-review skill's own contract.
CODE_SEVERITIES = ("blocking", "important", "suggestion", "nitpick", "question", "praise")

#: The three wrap-up engines the closing chain may invoke; the compiled marker
#: comment names `probe-utils.py` as its generator and is not part of the chain.
CLOSING_ENGINES = {"run-determination.py", "exec-quant.py", "feedback-utils.py"}

#: The one legitimate feedback destination (FR-020 / C-61).
CANONICAL_STORE = ".specify/memory/feedback/"

#: A code finding's locating form: a path with an extension plus a line number.
CODE_LOCATION_RE = re.compile(r"[\w./-]+\.(?:py|sh|js|ts|md|go|rs):\d+")

#: Framework-object vocabulary a friction sample talks about (C-56's examples).
FRAMEWORK_TOKENS = (
    "renderer",
    "base",
    "receipt",
    "non-interactive",
    "template",
    "workflow",
    "engine",
    "skill",
    "command",
    "渲染器",
    "基准",
    "回执",
)

#: The two constructed samples (SC-007). Both are written here, and the
#: judgement is made here, so a later reader can re-run the classification.
SAMPLES = (
    {
        "name": "framework-friction",
        "unit_id": "/speckit.review",
        "text": (
            "The receipt step has no non-interactive path on a host without the "
            "renderer, and the workflow leaves the base ambiguous, so the run can "
            "only record not-evaluated."
        ),
        "expected": "legal",
    },
    {
        "name": "code-defect",
        "unit_id": "skill:code-review",
        "text": (
            "src/specify_cli/__init__.py:412 — blocking: the option default is None "
            "and the handler dereferences it, so the command crashes on first use."
        ),
        "expected": "violation",
    },
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def _flat(text: str) -> str:
    """Collapse whitespace so a phrase can be asserted across a line wrap."""
    return re.sub(r"\s+", " ", text)


def _has(text: str, phrase: str) -> bool:
    return phrase.lower() in _flat(text).lower()


def _one_of(text: str, patterns) -> bool:
    flat = _flat(text)
    return any(re.search(pattern, flat) for pattern in patterns)


def _section(text: str, start: str, end: str | None = "## ") -> str:
    """One section body; ``end=None`` runs to the end of the file."""
    tail = rf"(?=^{re.escape(end)})" if end else r"(?=\Z)"
    m = re.search(rf"(?ms)^{re.escape(start)}.*?{tail}", text)
    assert m, f"section {start!r} not found (or no {end!r} after it)"
    return m.group(0)


def _outside_wrap_up(text: str) -> str:
    """The body with the compiled closing face removed.

    C-55 says the face is not edited, so every rule this feature writes has to be
    findable *outside* it; searching the whole file would let an edit inside the
    generated block pass as new content.
    """
    m = re.search(r"(?ms)^## Wrap-up.*?(?=^## |\Z)", text)
    assert m, "`## Wrap-up` not found"
    return text[: m.start()] + text[m.end() :]


def _cmd() -> str:
    return REVIEW_CMD.read_text(encoding="utf-8")


def _code_skill() -> str:
    return CODE_SKILL.read_text(encoding="utf-8")


def _process_skill() -> str:
    return PROCESS_SKILL.read_text(encoding="utf-8")


def _steps(face: str) -> tuple:
    """The ordered step labels of one compiled closing face."""
    return tuple(re.findall(r"(?m)^\d+\. ([A-Za-z][A-Za-z ]*[A-Za-z]) — ", face))


def _duty() -> dict:
    """Read the classification duty out of the two surfaces that must carry it.

    The duty is not hard-coded: it is *parsed* from the command template and the
    code-review skill, so a surface that loses its statement removes the rule the
    samples are judged against (C-57) rather than leaving a green assertion.
    """
    duty = {"legal": [], "forbidden": []}
    for label, text in (
        ("templates/commands/review.md", _cmd()),
        ("skills/internal/code-review/SKILL.md", _code_skill()),
    ):
        flat = _flat(text)
        sentences = [s.strip() for s in re.split(r"(?<=[.!?。])\s*", flat) if s.strip()]
        for sentence in sentences:
            mentions_feedback = re.search(r"feedback|反馈", sentence, re.IGNORECASE)
            if not mentions_feedback:
                continue
            if re.search(r"framework|框架", sentence, re.IGNORECASE) and re.search(
                r"friction|摩擦", sentence, re.IGNORECASE
            ):
                duty["legal"].append((label, sentence))
            if re.search(r"code defect|代码缺陷", sentence, re.IGNORECASE) and re.search(
                r"MUST NOT|must not|never|不得|禁止|MUST stay|stays in", sentence
            ):
                duty["forbidden"].append((label, sentence))

    missing = [name for name, hits in duty.items() if not hits]
    assert not missing, (
        "the classification duty is not written where it must be readable: missing "
        f"{missing!r} on one or both of templates/commands/review.md and "
        "skills/internal/code-review/SKILL.md (C-57 requires BOTH surfaces)"
    )
    surfaces = {label for hits in duty.values() for label, _ in hits}
    assert surfaces == {
        "templates/commands/review.md",
        "skills/internal/code-review/SKILL.md",
    }, f"the duty MUST be written on both surfaces, found it on {sorted(surfaces)!r}"
    return duty


def _judge(sample: dict) -> str:
    """Judge one constructed sample against the written duty (SC-007)."""
    duty = _duty()
    text = sample["text"]
    located = bool(CODE_LOCATION_RE.search(text))
    severity = any(
        re.search(rf"(?<![\w-]){s}(?![\w-])", text, re.IGNORECASE) for s in CODE_SEVERITIES
    )
    if located and severity:
        return "violation" if duty["forbidden"] else "unclassified"
    if any(token in text.lower() for token in FRAMEWORK_TOKENS):
        return "legal" if duty["legal"] else "unclassified"
    return "unclassified"


def _ws(tmp_path: Path) -> Path:
    ws = tmp_path / "ws"
    (ws / ".specify").mkdir(parents=True)
    return ws


def _record_feedback(ws: Path, unit_id: str, run_id: str, points: str):
    unit_type = "command" if unit_id.startswith("/") else "skill"
    return subprocess.run(
        [
            sys.executable,
            str(FEEDBACK_UTILS),
            "--action",
            "record",
            "--workspace-root",
            str(ws),
            "--unit-id",
            unit_id,
            "--unit-type",
            unit_type,
            "--run-id",
            run_id,
            "--review",
            "probe",
            "--points",
            points,
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def _determine(ws: Path, unit_id: str, run_id: str):
    unit_type = "command" if unit_id.startswith("/") else "skill"
    return subprocess.run(
        [
            sys.executable,
            str(RUN_DETERMINATION),
            "--action",
            "determine",
            "--workspace-root",
            str(ws),
            "--unit-id",
            unit_id,
            "--unit-type",
            unit_type,
            "--run-id",
            run_id,
            "--complexity",
            "complex",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def _frontmatter_field(entry: str, field: str) -> str:
    m = re.search(rf'(?m)^{field}: "(.*)"$', entry)
    assert m, f"entry carries no `{field}` field"
    return m.group(1)


# --------------------------------------------------------------------------- #
# C-55 — the closing step set is exactly as published
# --------------------------------------------------------------------------- #

def test_c55_the_command_closing_step_set_is_the_published_six():
    face = _section(_cmd(), "## Wrap-up", "## Handoffs")
    assert _steps(face) == COMMAND_CLOSING_STEPS, (
        "the command's closing step set MUST stay exactly as published — six steps "
        f"in this order; found {_steps(face)!r}"
    )


def test_c55_both_delegated_skill_faces_keep_their_five_step_set():
    for path, text in (
        ("skills/internal/review-sdd-process/SKILL.md", _process_skill()),
        ("skills/internal/code-review/SKILL.md", _code_skill()),
    ):
        face = _section(text, "## Wrap-up", None)
        assert _steps(face) == SKILL_CLOSING_STEPS, (
            f"{path} MUST keep its five-step closing face; found {_steps(face)!r}"
        )


def test_c55_the_command_states_the_set_is_unchanged_and_adds_no_channel():
    body = _outside_wrap_up(_cmd())
    assert _has(body, "closing step set"), (
        "the command MUST name the closing step set it leaves untouched (C-55)"
    )
    assert _one_of(
        body,
        (
            r"closing step set[^.]{0,80}(?:unchanged|as published|exactly as)",
            r"(?:unchanged|as published)[^.]{0,80}closing step set",
        ),
    ), "the statement MUST say the set is unchanged / stays as published"
    for channel in ("no closing step", "no side channel", "no second record type"):
        assert _has(body, channel), (
            f"the command MUST state that this composition adds {channel!r} (C-55)"
        )


def test_c55_the_rule_text_sits_outside_the_compiled_face():
    face = _section(_cmd(), "## Wrap-up", "## Handoffs")
    assert "AUTO-GENERATED by probe-utils.py --action compile-embeds" in face, (
        "the compiled face MUST keep its compilation marker"
    )
    for token in ("classification", "framework friction", "unit census", "three units"):
        assert not _has(face, token), (
            f"{token!r} MUST NOT be written inside the compiled `## Wrap-up` face — "
            "that block is generated from the probe registry, not hand-edited"
        )


# --------------------------------------------------------------------------- #
# C-56 / C-57 — one classification duty, two surfaces, two judged samples
# --------------------------------------------------------------------------- #

def test_c56_the_command_limits_the_payload_to_framework_friction():
    body = _outside_wrap_up(_cmd())
    assert _one_of(
        body,
        (
            r"framework[^.]{0,120}friction",
            r"friction[^.]{0,120}framework",
        ),
    ), "the command MUST name framework friction as the legal payload (C-56)"
    assert _has(body, "feedback entry"), (
        "the rule MUST speak about a feedback entry, not about feedback in general"
    )


def test_c56_a_code_defect_stays_in_the_record():
    body = _outside_wrap_up(_cmd())
    holders = [
        sentence
        for sentence in re.split(r"(?<=[.!?])\s+", _flat(body))
        if re.search(r"code defect", sentence, re.IGNORECASE)
    ]
    assert holders, "the command MUST name the code defect as the forbidden payload"
    joined = " ".join(holders)
    assert re.search(r"MUST NOT|must not|never", joined), (
        "the prohibition MUST be stated, not merely mentioned"
    )
    assert _has(joined, "feedback"), "the prohibition MUST name the feedback entry"
    assert _has(joined, "code-review.md"), (
        "the defect MUST be sent back to `code-review.md` (STR-004), where its "
        "severity, file and line are meaningful"
    )


def test_c57_the_duty_is_written_on_two_surfaces():
    duty = _duty()
    assert len(duty["legal"]) >= 1 and len(duty["forbidden"]) >= 1, (
        "both classes — the legal payload and the forbidden one — MUST be readable"
    )
    for label, text in (
        ("templates/commands/review.md", _cmd()),
        ("skills/internal/code-review/SKILL.md", _code_skill()),
    ):
        flat = _flat(text)
        assert re.search(r"framework|框架", flat, re.IGNORECASE) and re.search(
            r"friction|摩擦", flat, re.IGNORECASE
        ), f"{label} MUST carry the legal class of the duty (C-57)"
        assert re.search(r"code defect|代码缺陷", flat, re.IGNORECASE), (
            f"{label} MUST carry the forbidden class of the duty (C-57)"
        )


def test_c57_the_framework_friction_sample_is_judged_legal(tmp_path):
    sample = SAMPLES[0]
    assert sample["expected"] == "legal"
    assert _judge(sample) == "legal", (
        "a framework-friction item is a legal feedback entry (SC-007's first half)"
    )

    # The legal side is drivable against the real store: it is an entry like any
    # other, which is exactly why the rule has to be written rather than assumed.
    ws = _ws(tmp_path)
    out = _record_feedback(ws, sample["unit_id"], "r20261027T000000Z-us5-c57", sample["text"])
    assert out.returncode == 0, f"recording a legal friction item failed: {out.stderr[:300]}"
    entries = sorted((ws / ".specify" / "memory" / "feedback").glob("*.md"))
    assert len(entries) == 1, f"the legal sample MUST produce one entry, got {len(entries)}"
    entry = entries[0].read_text(encoding="utf-8")
    assert _frontmatter_field(entry, "unit_id") == sample["unit_id"]
    assert _frontmatter_field(entry, "scope") == "local", (
        "every entry stays `scope: local` (C-60)"
    )


def test_c57_the_code_defect_sample_is_judged_a_violation():
    sample = SAMPLES[1]
    assert sample["expected"] == "violation"
    assert _judge(sample) == "violation", (
        "a code defect copied out of the record violates the written classification "
        "duty (SC-007's second half)"
    )


def test_c57_the_two_samples_are_judged_oppositely():
    verdicts = [_judge(sample) for sample in SAMPLES]
    assert verdicts == ["legal", "violation"], (
        "the two samples MUST land on opposite verdicts; a judge that answers the "
        f"same way for both decides nothing — got {verdicts!r}"
    )
    assert "unclassified" not in verdicts, (
        "the written duty MUST classify both samples; an unclassified sample means "
        "the rule does not cover a class it claims to cover"
    )


def test_c57_the_store_itself_cannot_enforce_the_duty():
    """The rule is written, not machine-enforced — which is why C-57 exists."""
    body = _outside_wrap_up(_cmd())
    assert _one_of(
        body,
        (
            r"written rule",
            r"two surfaces",
            r"matter of taste",
            r"detectable violation",
        ),
    ), "the command MUST state that the duty is written so the mistake is detectable"


# --------------------------------------------------------------------------- #
# C-58 / C-59 — three units, three records, one key
# --------------------------------------------------------------------------- #

def test_c58_the_command_names_the_three_units():
    body = _outside_wrap_up(_cmd())
    for unit in UNITS:
        assert unit in body, (
            f"the command MUST name the unit {unit!r} in the per-run census (C-58)"
        )
    assert _one_of(body, (r"three units", r"unit census[^.]{0,40}three", r"三个单元")), (
        "the census MUST be stated as three units, not left to inference"
    )


def test_c58_the_command_forbids_suppression_backfill_and_substitution():
    body = _flat(_outside_wrap_up(_cmd()))
    assert re.search(r"MUST NOT suppress|MUST NOT be suppressed|不得抑制|不抑制", body), (
        "the command MUST NOT suppress either skill's closing record (C-58)"
    )
    assert _one_of(
        body,
        (
            r"on (?:its|their|a skill's) behalf",
            r"writes? (?:no )?skill'?s? run determination",
            r"MUST NOT write",
            r"代为补记",
            r"不得代",
        ),
    ), "the command MUST NOT write a skill's run determination on its behalf"
    assert re.search(r"back-fill|backfill|补记", body), (
        "the command MUST NOT back-fill a record after the fact (C-58)"
    )


def test_c58_the_code_skill_completes_its_own_closing_record():
    body = _flat(_code_skill())
    assert re.search(r"skill:code-review", body), (
        "the code-review skill MUST carry its own unit id"
    )
    assert re.search(r"shared run id|同一个 run id|同一 run id|one run id", body), (
        "the skill's closing obligation is stated under the run's shared run id (C-58)"
    )
    assert re.search(
        r"its own closing record|自己的收尾记录|completes its own|各自完成", body
    ), "the skill MUST state that it completes its own closing record"


def test_c58_each_unit_owns_exactly_one_compiled_closing_face():
    faces = {
        "/speckit.review": _cmd(),
        "skill:review-sdd-process": _process_skill(),
        "skill:code-review": _code_skill(),
    }
    for unit, text in faces.items():
        assert f'--unit-id "{unit}"' in _flat(text), (
            f"{unit} MUST be the unit id its own face invokes"
        )
        others = [other for other in UNITS if other != unit]
        for other in others:
            assert f'--unit-id "{other}"' not in _flat(text), (
                f"the face of {unit} MUST NOT invoke another unit's id ({other}) — a "
                "record written on another's behalf is what C-58 forbids"
            )


def test_c58_run_determination_keeps_three_unit_records_driven(tmp_path):
    ws = _ws(tmp_path)
    run_id = "r20261027T000000Z-us5-c58"
    for unit in UNITS:
        out = _determine(ws, unit, run_id)
        assert out.returncode == 0, f"determine failed for {unit}: {out.stderr[:300]}"
    session = ws / ".specify" / "memory" / "session"
    records = sorted(session.glob("*.md"))
    assert len(records) == 3, (
        "one nested run MUST leave three run-determination records, one per unit; "
        f"found {len(records)}"
    )
    for unit in UNITS:
        hits = [
            path
            for path in records
            if _frontmatter_field(path.read_text(encoding="utf-8"), "source") == unit
        ]
        assert len(hits) == 1, f"{unit} MUST own exactly one session record, got {hits!r}"
        body = hits[0].read_text(encoding="utf-8")
        assert run_id in body, "the three records share the run id"


def test_c59_three_units_one_run_produce_three_entries_driven(tmp_path):
    ws = _ws(tmp_path)
    run_id = "r20261027T000000Z-us5-c59"
    for unit in UNITS:
        out = _record_feedback(ws, unit, run_id, "framework friction: receipt gap")
        assert out.returncode == 0, f"record failed for {unit}: {out.stderr[:300]}"
    entries = sorted((ws / ".specify" / "memory" / "feedback").glob("*.md"))
    assert len(entries) == 3, (
        "the (unit_id, run_id) key means three units of one run produce three "
        f"entries; found {len(entries)}"
    )
    seen = set()
    for path in entries:
        body = path.read_text(encoding="utf-8")
        seen.add(_frontmatter_field(body, "unit_id"))
        assert _frontmatter_field(body, "run_id") == run_id, (
            "the three entries share one run id"
        )
        assert _frontmatter_field(body, "scope") == "local"
    assert seen == set(UNITS), f"each unit owns its entry; found {sorted(seen)!r}"


def test_c59_a_repeated_unit_dedups_only_itself_driven(tmp_path):
    ws = _ws(tmp_path)
    run_id = "r20261027T000000Z-us5-c59b"
    for unit in UNITS:
        assert _record_feedback(ws, unit, run_id, "framework friction").returncode == 0
    again = _record_feedback(ws, "/speckit.review", run_id, "framework friction")
    assert again.returncode == 0, "a duplicate call stays exit 0, never an error"
    entries = sorted((ws / ".specify" / "memory" / "feedback").glob("*.md"))
    assert len(entries) == 3, (
        "re-running one unit MUST NOT create a fourth entry and MUST NOT remove or "
        f"merge another unit's; found {len(entries)}"
    )


def test_c59_the_census_is_three_not_two():
    for label, text in (
        ("templates/commands/review.md", _outside_wrap_up(_cmd())),
        ("skills/internal/code-review/SKILL.md", _code_skill()),
    ):
        flat = _flat(text)
        assert re.search(r"three units|三个单元|unit census[^.]{0,40}three", flat), (
            f"{label} MUST state the census as three (C-59)"
        )
        assert not re.search(
            r"two units|two records|only two|两个单元|两条记录|只产生两条", flat
        ), (
            f"{label} MUST NOT describe the nested run as two units or two records — "
            "that reading is the ambiguity C-59 removes"
        )


# --------------------------------------------------------------------------- #
# C-60 / C-61 — the predecessor invariants and the closed destination set
# --------------------------------------------------------------------------- #

def test_c60_the_five_predecessor_invariants_still_hold():
    mechanism = _flat(FEEDBACK_STEP.read_text(encoding="utf-8"))
    assert re.search(r"scope: local", mechanism), "every entry stays `scope: local`"
    assert re.search(r"Zero automated transmission|zero automated transmission", mechanism), (
        "zero automated transmission is the invariant, not a setting"
    )
    assert re.search(r"Target = the Spec Kit framework itself", mechanism), (
        "the feedback target stays the framework rather than the feature"
    )
    assert re.search(r"自省|Introspection", mechanism), (
        "the introspection step stays the legal entry for a framework-wide recommendation"
    )
    handoffs = _section(_cmd(), "## Handoffs", None)
    assert "register.md" in handoffs and _has(handoffs, "same commit"), (
        "a recommendation id is registered in the same commit that lands it"
    )
    assert "REC-" in handoffs


def test_c61_the_two_surfaces_name_no_second_feedback_destination():
    for label, text in (
        ("templates/commands/review.md", _cmd()),
        ("skills/internal/code-review/SKILL.md", _code_skill()),
    ):
        for match in re.finditer(r"[\w./-]*feedback/[\w./-]*", text):
            token = match.group(0)
            assert CANONICAL_STORE.rstrip("/") in token or token.startswith("feedback/"), (
                f"{label} names {token!r} — the only feedback destination is the "
                f"local store {CANONICAL_STORE} (C-61)"
            )
        assert not re.search(r"feedback/(?:intake|aggregat|upload|second)", text), (
            f"{label} MUST NOT introduce a second intake, aggregation or upload path"
        )


def test_c61_no_second_id_family_and_no_network_path():
    for label, text in (
        ("templates/commands/review.md", _cmd()),
        ("skills/internal/code-review/SKILL.md", _code_skill()),
    ):
        for family in ("FB-", "FDB-", "FEEDBACK-"):
            assert family not in text, (
                f"{label} MUST NOT coin a second feedback id family ({family}); the "
                "existing entry id stays the only one"
            )
        assert not re.search(r"https?://|curl |requests\.|urllib", text), (
            f"{label} MUST NOT introduce an upload path or a network call (C-61)"
        )


def test_c61_no_new_engine_is_introduced():
    for label, text in (
        ("templates/commands/review.md", _outside_wrap_up(_cmd())),
        ("skills/internal/code-review/SKILL.md", _outside_wrap_up(_code_skill())),
    ):
        engines = set(re.findall(r"[\w-]+\.py", text))
        extra = engines - CLOSING_ENGINES
        assert not extra, (
            f"{label} invokes {sorted(extra)!r} outside the published closing chain; "
            "this feature adds no second record type and no new engine (C-55/C-61)"
        )


# --------------------------------------------------------------------------- #
# C-62 / C-63 — the expression face, the receipt and the two questions
# --------------------------------------------------------------------------- #

def test_c62_the_code_segment_is_an_additional_segment():
    body = _flat(_code_skill())
    assert re.search(r"additional segment|附加段", body), (
        "the code segment MUST be described as an additional segment (C-62)"
    )
    assert re.search(r"reader baseline|读者基准", body, re.IGNORECASE), (
        "the skill MUST name the reader-baseline judgement it must not replace"
    )
    # The expression-class wiring surface is closed (C-5 of
    # tests/contract/test_expression_compatibility.py: no engine and no owner
    # document may be named outside W1–W4), so this skill states the boundary by
    # description and MUST NOT acquire a wiring reference of its own. The owner
    # side already points at this face; a path here would be the second wiring.
    for token in (
        "flow-class-definitions.md",
        "expression-gates.md",
        "flow-class-check.py",
        "doc-consistency-check.py",
    ):
        assert token not in body, (
            f"skills/internal/code-review/SKILL.md MUST NOT name the closed wiring "
            f"token {token!r} — the expression-class owner declares the review face, "
            "not the other way round (C-5)"
        )


def test_c62_a_no_delta_feature_records_not_applicable_without_short_circuiting():
    body = _flat(_code_skill())
    holders = [
        sentence
        for sentence in re.split(r"(?<=[.!?])\s+|(?<=。)", body)
        if re.search(r"not-applicable", sentence)
    ]
    assert holders, "the skill MUST keep `not-applicable` in its triage vocabulary"
    joined = " ".join(holders)
    assert re.search(r"reader|读者", joined, re.IGNORECASE), (
        "the `not-applicable` rule MUST state what happens to the reader-baseline "
        "judgement (C-62)"
    )
    assert re.search(r"neither replaced nor short-circuited|不替代|不短路|neither", joined), (
        "the reader-baseline judgement is neither replaced nor short-circuited by a "
        "`not-applicable` code segment"
    )


def test_c63_the_receipt_counts_reviewed_files():
    body = _flat(_code_skill())
    assert re.search(r"reviewed files|已评审文件", body), (
        "the receipt's coverage counts reviewed files (C-63)"
    )
    assert re.search(r"share of the changed-file set|变更文件集", body), (
        "the unit is the share of the changed-file set that carries a verdict"
    )


def test_c63_the_receipt_is_never_test_or_compile_coverage():
    body = _flat(_code_skill())
    for token, pattern in (
        ("test coverage", r"never test coverage|从不是测试覆盖率|不是测试覆盖率"),
        ("compile coverage", r"never compile coverage|不是编译覆盖率|从不是编译覆盖率"),
    ):
        assert re.search(pattern, body), (
            f"the receipt MUST be kept apart from {token} explicitly (C-63)"
        )


def test_c63_the_receipt_is_not_evidence_for_the_reader_baseline_judgement():
    body = _flat(_code_skill())
    holders = [
        sentence
        for sentence in re.split(r"(?<=[.!?])\s+|(?<=。)", body)
        if re.search(r"reader baseline|读者基准", sentence, re.IGNORECASE)
    ]
    assert holders, (
        "the skill MUST name the reader-baseline judgement it is not evidence for"
    )
    joined = " ".join(holders)
    assert re.search(
        r"never evidence|not evidence|不得被引作|不构成证据|不是.{0,12}证据", joined
    ), "the receipt MUST NOT be cited as evidence for the reader-baseline judgement"


def test_c63_fr027_targets_the_other_object_and_never_forbids_the_receipt():
    body = _flat(_code_skill())
    holders = [
        sentence
        for sentence in re.split(r"(?<=[.!?])\s+|(?<=。)", body)
        if "FR-027" in sentence
    ]
    assert holders, (
        "the reverse direction MUST be stated: FR-027's prohibition targets the "
        "other object, so a reader cannot cite it to forbid the receipt (C-63)"
    )
    joined = " ".join(holders)
    assert re.search(r"receipt|回执", joined), "the sentence MUST name the receipt"
    assert re.search(r"never forbids|does not forbid|不禁止|MUST NOT be cited", joined), (
        "FR-027 MUST be stated as not forbidding the receipt"
    )
    assert re.search(r"compile|test|编译|测试", joined), (
        "the sentence MUST name the object the prohibition actually targets"
    )


def test_c63_the_two_directions_are_stated_together():
    body = _flat(_code_skill())
    forward = re.search(
        r"(?:never|not)\s+evidence[^.]{0,120}(?:reader baseline|读者基准)", body
    ) or re.search(r"(?:reader baseline|读者基准)[^.]{0,120}(?:never evidence|not evidence)", body)
    reverse = re.search(r"FR-027[^.]{0,160}(?:receipt|回执)", body)
    assert forward, "direction 1: the receipt is not evidence for the reader baseline"
    assert reverse, "direction 2: FR-027 does not forbid the receipt"
    assert forward.group(0) != reverse.group(0), (
        "the two directions must be two statements — a single sentence cannot carry "
        "both a prohibition and its non-application"
    )
