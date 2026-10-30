"""Contract tests for the dispatch payload (Feature 078, User Story 3).

Clause source: ``.specify/specs/078-coaching-skills/contracts/dispatch-payload.contract.md``
(C-1..C-5). The payload is a closed field set carried into one subagent dispatch, so the
tests do two things:

* assert that ``SKILL.md`` § Dispatch Payload names every required field, every forbidden
  content class, the single-dispatch cardinality, the return handling and the transport
  record, and
* run a small payload validator over one compliant payload and four counterexamples (the
  expectation file, an ``OC-*`` row, a coach conclusion, a run-directory path). Each
  counterexample MUST be judged red, otherwise the closed field set is decoration.

Literal authority for the artifact names and the run directory is ``requirements.md``
§ Shared Strings (STR-013..STR-017); ``<work>`` in the compliant payload is the fixture
brief, byte for byte.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL = REPO_ROOT / "skills" / "external" / "coaching-skills" / "SKILL.md"
WORK = REPO_ROOT / "tests" / "fixtures" / "coaching" / "work.md"

REQUIRED_FIELDS = (
    "trainee",
    "work",
    "instruction",
    "return-contract",
    "anomaly-line",
    "fast-fail-clause",
    "confirmation-relay",
)

#: Content classes the payload must never carry (C-2). Each marker is a detector, not the
#: clause text: the clause prose lives in the contract, the detectors live here.
FORBIDDEN_MARKERS = {
    "expectation": ("expectation", ".specify/memory/coaching/"),
    "criteria-row": ("OC-", "PE-"),
    "coach-conclusion": ("deviation", "my reading", "coach concludes"),
}

TRANSPORT_MODES = ("native", "run-agent-fallback", "run-skills-explicit-path")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == f"## {heading}":
            start = index + 1
            break
    if start is None:
        return None
    body: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def _require_section(text: str, heading: str) -> str:
    body = _section(text, heading)
    assert body is not None and body.strip(), f"missing required section: ## {heading}"
    return re.sub(r"\s+", " ", body).strip()


def validate_payload(fields: dict[str, str], work: str) -> list[str]:
    """Judge one rendered payload against C-1 and C-2.

    The whole payload is one rendered text, so the detectors run over the concatenation;
    a field name is also part of the payload vocabulary and is judged the same way.
    """
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if not fields.get(field, "").strip():
            errors.append(f"missing required field: {field}")
    if "work" in fields and fields["work"] != work:
        errors.append("<work> is not verbatim")
    instruction = fields.get("instruction", "")
    if "instruction" in fields and "Trainee's own `SKILL.md`" not in instruction:
        errors.append("the instruction is not 'follow the Trainee's own SKILL.md'")

    rendered = "\n".join(f"{name}: {value}" for name, value in fields.items())
    for label, markers in FORBIDDEN_MARKERS.items():
        for marker in markers:
            if marker in rendered:
                errors.append(f"forbidden {label} content: {marker}")
    return errors


WORK_TEXT = _text(WORK)

COMPLIANT_PAYLOAD = {
    "trainee": "fixture-trainee (skills/external/fixture-trainee, external)",
    "work": WORK_TEXT,
    "instruction": "Follow the Trainee's own `SKILL.md` as the highest execution guidance.",
    "return-contract": (
        "Return step-by-step actions, tool calls, state changes, artifacts, elapsed time "
        "and the terminal state."
    ),
    "anomaly-line": "State one explicit anomaly line on return; state `none` when there is none.",
    "fast-fail-clause": (
        "If a step is ambiguous or blocked, stop at that point and report it; never patch "
        "it silently."
    ),
    "confirmation-relay": (
        "If the Trainee flow reaches a destructive step, stop and report it back instead "
        "of approving it yourself."
    ),
}


# --------------------------------------------------------------------------- #
# C-1 Required Fields
# --------------------------------------------------------------------------- #


def test_c1_every_required_field_is_named_with_its_rule():
    body = _require_section(_text(SKILL), "Dispatch Payload")
    for field in REQUIRED_FIELDS:
        assert f"`{field}`" in body, f"the payload contract lacks {field}"
    assert re.search(r"byte-for-byte the second positional parameter", body)
    assert re.search(r"no alternatives offered", body)
    assert re.search(r"highest execution guidance", body)
    assert re.search(r"injected at dispatch time", body)
    assert re.search(r"the answer comes from the user", body)


def test_c1_compliant_payload_passes_and_a_missing_field_is_red():
    assert validate_payload(COMPLIANT_PAYLOAD, WORK_TEXT) == []
    broken = dict(COMPLIANT_PAYLOAD)
    del broken["anomaly-line"]
    assert "missing required field: anomaly-line" in validate_payload(broken, WORK_TEXT)


def test_c1_a_rewritten_work_parameter_is_red():
    broken = dict(COMPLIANT_PAYLOAD, work="prepare a release checklist")
    assert "<work> is not verbatim" in validate_payload(broken, WORK_TEXT)


# --------------------------------------------------------------------------- #
# C-2 Forbidden Fields
# --------------------------------------------------------------------------- #


def test_c2_the_four_forbidden_classes_are_declared():
    body = _require_section(_text(SKILL), "Dispatch Payload")
    flat = body
    assert re.search(r"the expectation file, any `OC-\*` / `PE-\*` row", flat)
    assert re.search(r"deviation guesses or conclusions", flat)
    assert re.search(r"coach-authored simplification or reordering", flat)
    assert re.search(r"any artifact path inside the run directory", flat)


@pytest.mark.parametrize(
    "addition",
    [
        {"expectation": "see expectation.md for the OC rows"},
        {"OC-1": "checklist.md has five rows"},
        {"coach-note": "my reading is that item 4 is covered"},
        {"payload-ref": ".specify/memory/coaching/20261030T101500Z-fixture-trainee/x.md"},
    ],
    ids=["expectation-file", "criteria-row", "coach-conclusion", "run-directory-path"],
)
def test_c2_each_forbidden_class_is_red(addition):
    broken = dict(COMPLIANT_PAYLOAD)
    broken.update(addition)
    assert validate_payload(broken, WORK_TEXT), f"{addition} was not judged red"


# --------------------------------------------------------------------------- #
# C-3 Dispatch Cardinality
# --------------------------------------------------------------------------- #


def test_c3_single_payload_and_no_retry_with_a_modified_payload():
    body = _require_section(_text(SKILL), "Dispatch Payload")
    assert re.search(r"Exactly one payload is dispatched per run", body)
    assert re.search(r"not re-sent with a modified payload", body)
    assert re.search(r"the failure is recorded", body)


# --------------------------------------------------------------------------- #
# C-4 Return Handling
# --------------------------------------------------------------------------- #


def test_c4_return_is_recorded_and_never_inflated():
    body = _require_section(_text(SKILL), "Dispatch Payload")
    assert re.search(r"anomaly line is written into the DispatchRecord unchanged", body)
    assert re.search(r"become `self-report` rows", body)
    assert re.search(r"`observation-gap` row rather than an inferred one", body)
    assert re.search(r"recorded as `partial`", body)


# --------------------------------------------------------------------------- #
# C-5 Transport Record
# --------------------------------------------------------------------------- #


def test_c5_transport_and_payload_reference_are_recorded():
    body = _require_section(_text(SKILL), "Dispatch Payload")
    for mode in TRANSPORT_MODES:
        assert mode in body, f"the transport record lacks {mode}"
    assert re.search(r"recorded in the DispatchRecord `mode` field", body)
    assert re.search(r"`payload-ref`", body)
    assert re.search(r"never enters the coach's user-facing report", body)
