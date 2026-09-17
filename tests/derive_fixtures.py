"""Shared synthetic Derivation corpus + engine runner for the derive test suite.

Engine:            scripts/python/derive-utils.py
Concept authority: shared/definitions/derivation-definitions.md
Contracts:         .specify/specs/048-derive-command/contracts/derive-engine.md
                   .specify/specs/048-derive-command/contracts/derivation-model.md
                   .specify/specs/048-derive-command/contracts/move-library.md

Consumers: tests/unit/test_derive_validate.py, tests/unit/test_derive_moves.py,
tests/contract/test_derive_engine_contract.py, tests/integration/test_derive_us{1,2,3}.py.

The corpus is synthetic and slot-shaped on purpose — no real URLs, no real
titles, no feature identifiers. The concept anchor's no-leakage discipline
applies to everything shipped in the repo, test fixtures included.

Interface notes (verified against the live engine — derive-engine.md C-7/C-14):
  * the CLI flag is ``--slug`` (there is no ``--topic`` and no ``--timeout``);
  * every JSON response is one envelope with the fixed top-level keys
    ``ok / action / workspaceRoot / generatedAt / errors / warnings /
    semanticChecksPending / notes / payload``; per-action facts live under
    ``payload``;
  * ``moves-add`` input is ``{"moves": [...]}`` with camelCase candidate keys
    (``name / inferenceForm / prevents / appliesWhen / anchor / intent``) and a
    QUALIFIED ``<topic-slug>.S-<nnn>`` anchor (a bare ``S-<nnn>`` is rejected).

Hermeticity rules for every consumer:
  * workspaces are pytest ``tmp_path`` directories, never the real repo;
  * behavioural assertions go through the CLI subprocess (``sys.executable``) so
    the shipped entry point is what is tested;
  * no test may reach the network — ``probe-links`` is exercised only in-process
    with ``_http_get`` monkeypatched (the single transport seam, C-30/C-33).
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
ENGINE = REPO_ROOT / "scripts" / "python" / "derive-utils.py"
ENGINE_MIRROR = REPO_ROOT / ".specify" / "scripts" / "python" / "derive-utils.py"

#: Topic slug used by the synthetic corpus.
TOPIC = "rest-architecture"

DERIVE_DIR = Path(".specify") / "derive"
MOVES_REL = DERIVE_DIR / "moves.md"

#: The eight artifact sections, in the frozen order the anchor defines. Pinned
#: here as a literal so a scaffold regression is caught even if the engine's own
#: tuple is edited.
ARTIFACT_SECTIONS = (
    "## Sources",
    "## Unverifiable Sources",
    "## Reasoning Moves Applied",
    "## Derivation Chain",
    "## Termination",
    "## Derived Architecture",
    "## Open Questions",
    "## Self-Audit",
)

MOVE_COLUMNS = ("move_id", "name", "inference_form", "prevents",
                "applies_when", "anchor", "status")

#: The complete enums the engine pins. ``byGrade`` / ``byConfidence`` key sets
#: equal these exactly. ``byAccess`` equals ``ACCESS_BUCKETS`` exactly: a legal
#: ``wayback:<ts>`` value is collapsed to the single ``wayback`` bucket so the key
#: set stays the complete enum (derive-engine.md C-19).
GRADES = ("primary", "authoritative-secondary", "community", "unverified")
ACCESS_VALUES = ("live", "dead", "paywalled", "unknown")
ACCESS_BUCKETS = ("live", "wayback", "dead", "paywalled", "unknown")
CONFIDENCES = ("derived", "provisional", "contested")
SEMANTIC_CHECKS_PENDING = ("A11", "A14", "A16")
ENGINE_CHECKS = ("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A12", "A13",
                 "A15")
ALL_CHECKS = tuple("A%d" % n for n in range(1, 17))

#: The six closed warning codes (derivation-model.md C-44).
WARNING_CODES = frozenset({
    "secondary-sole-anchor", "unresolved-title", "verification-evidence-token-absent",
    "step-budget-reached", "attestation-method-degenerate", "degraded-run",
})

NO_ONLINE_CAPABILITY = "no-online-capability"

# --------------------------------------------------------------------------
# the four-class source corpus (live primary / wayback-rescued retitled /
# community listicle / dead unverifiable)
# --------------------------------------------------------------------------

SOURCES = """| id | claimed_title | resolved_title | title_mismatch | grade | url | access | resolved_via | verification |
|---|---|---|---|---|---|---|---|---|
| S-001 | On the maturity of the style | On the maturity of the style | false | primary | <url-1> | live | direct | direct fetch returned HTTP 200 on 2026-09-05 |
| S-002 | Community digest of the 2009 essay | In search of the ideal identifier | true | primary | <url-2> | wayback:20190401 | wayback | snapshot at <archive-url> retrieved after direct fetch returned HTTP 404 |
| S-003 | A practitioner roundup | A practitioner roundup | false | community | <url-3> | live | direct | direct fetch returned HTTP 200; aggregated listicle, no named originator |
| S-004 | An unverifiable attribution |  | false | unverified | <url-4> | dead | websearch | no snapshot and no canonical copy found via title+author search on 2026-09-05 |
"""

UNVERIFIABLE = """- `S-004` — dead link, no archive snapshot, no canonical copy found by title+author search.
"""

#: A bare-identity citation list (always legal, A9). No restated rows here, so
#: the green path never trips the projection-marker rules.
MOVES_APPLIED = """Applied from `.specify/derive/moves.md`:

- `M-001` Demote-by-counterexample (reused)
- `M-002` Derive-from-constraint-not-preference (reused)
"""

#: Two-step chain: D-1 anchored on the live primary (derived), D-2 on the
#: wayback-rescued retitled source (cited by its resolved title, as A3 demands)
#: plus D-1, at provisional confidence so a blocked provisional element below is
#: satisfiable under A8 (element confidence == min over its steps) and A10.
CHAIN = """### D-1
- premises: S-001
- leads: S-003
- move: M-001
- derivation: The source treats a popularity ladder as if it were a definition. Applying the counter-instance move: a design can satisfy every rung of the ladder while lacking the property the definition claims, so the ladder does not entail the property.
- conclusion: A maturity ladder is not a definition of the style.
- falsification: Finding a rung of the ladder that no counter-instance can satisfy while omitting the defining property. Not found in S-001.
- confidence: derived

### D-2
- premises: S-002, D-1
- move: M-002
- derivation: In search of the ideal identifier names the forces at play (evolvability, opacity, cacheability). Structure follows from resolving those forces rather than from naming taste, so an identifier whose shape is interpreted by clients violates the opacity force identified in S-002.
- conclusion: Identifiers must be opaque to clients.
- falsification: A documented case where clients interpreting identifier shape improved evolvability without cost. Not observed.
- confidence: provisional
"""

TERMINATION = "- condition: b\n- steps: 2 / 12\n"

ARCH = """### A-1 Ladder is not a definition
- statement: A maturity ladder ranks designs but does not define the style, so it is not an architectural constraint.
- derived-from: D-1
- confidence: derived

### A-2 Opaque identifiers
- statement: Clients treat identifiers as opaque tokens and never parse their shape.
- derived-from: D-2
- confidence: provisional
- open-questions: Q-1
"""

QUESTIONS = """### Q-1
- question: Does a versioned identifier scheme violate opacity, or merely risk it?
- why-undetermined: No grounded source addresses versioned identifiers directly; S-002 predates the practice.
- would-resolve: A-2
- discriminator: A primary source that derives identifier stability under a versioning scheme.
"""

#: The criterion/decision-point layer fixtures. IDENTITY signs the agent-prior
#: criterion; CRITERIA mixes a source-grounded truth-claim (C-001) with a signed
#: decision-claim (C-002); DECISIONS enumerates, filters (citing D-2/C-001),
#: ranks (citing C-001/C-002), selects from the enumeration, and carries one
#: alternate with a switch trigger.
IDENTITY = """- agent: test-agent 1.0
- model: test-model
- run-id: test-run-001
- run-at: 2026-09-05T00:00:00Z
- topic: %s
""" % TOPIC

CRITERIA = """| id | statement | kind | provenance | owner | weight | defeater |
|---|---|---|---|---|---|---|
| C-001 | Identifiers must stay opaque to clients | constraint | source | S-002 | high | a primary source deriving controlled exposure of identifier shape |
| C-002 | Prefer the candidate with the smaller operational surface | preference | agent-prior | Agent Identity test-run-001 | medium | re-declaration by the decision owner |
"""

DECISIONS = """### DP-1 Identifier scheme
- question: Which identifier scheme occupies the opaque-identifier slot?
- candidates: Opaque token [S-002]; Semantic slug [ungrounded]
- filters: D-2 with C-001 prunes Semantic slug (clients would parse its shape)
- ranking: Opaque token ranks first by C-001 and C-002
- selected: Opaque token
- alternates: Semantic slug — switch trigger C-001 (re-declaration required)
"""

#: The 16-row self-audit table for a CLEAN run: A1-A10/A12/A13/A15 transcribe
#: the engine-derived value ``pass``; A11/A14/A16 are agent-``attested`` with a
#: non-degenerate ``method`` sentence (never ``engine`` / ``n/a`` / empty).
AUDIT = """| # | check | method | result |
|---|---|---|---|
| A1 | source grades and verification evidence | engine | pass |
| A2 | no step anchored on community/unverified; every unverified source recorded | engine | pass |
| A3 | retitled sources cited by resolved title | engine | pass |
| A4 | no orphan premises, no forward or self references | engine | pass |
| A5 | no banned justifications | engine | pass |
| A6 | non-vacuous falsification on every step | engine | pass |
| A7 | every element has a resolving derived-from | engine | pass |
| A8 | element confidence equals the minimum over its steps | engine | pass |
| A9 | every cited move exists in the library and is not superseded | engine | pass |
| A10 | open-question links resolve both ways; contested steps routed | engine | pass |
| A11 | online grounding actually happened this run | every source was probed with the host fetch tool and each outcome recorded with its HTTP status in the verification column | attested |
| A12 | step count against budget and termination condition declared | engine | pass |
| A13 | every move reported as newly issued resolves to a library row | engine | pass |
| A14 | artifact states method, not content summary | each move is recorded as an inference schema with named slots re-applicable outside this domain, and every step instantiates those slots rather than restating a source | attested |
| A15 | criteria and decision points well-formed | engine | pass |
| A16 | decision-claims signed, not laundered into truth-claims | every agent-prior criterion is owned by the Agent Identity block and phrased as a signed decision, and each DP ranking cites the criteria that genuinely support it | attested |
"""

#: The two-move seed library. Slot letters are deliberate: the dedup tests
#: re-write the same shapes with different slot letters (`Q`/`E`) to prove
#: slot-isomorphic dedup. Anchors are the QUALIFIED cross-topic form.
SEED_MOVES = (
    {
        "name": "Demote-by-counterexample",
        "inferenceForm": "Given a claimed property `P` of design `D`, exhibit a counter-instance "
                         "satisfying `D` but not `P` => `P` is not entailed by `D`.",
        "prevents": "accepting a popularity ladder as a definition",
        "appliesWhen": "a definition is conflated with a ranking; NOT licensed when no "
                       "counter-instance exists",
        "anchor": TOPIC + ".S-001",
        "intent": "new",
    },
    {
        "name": "Derive-from-constraint-not-preference",
        "inferenceForm": "Given forces `F` in domain `X`, derive structure `S` as the resolution "
                         "of `F`; reject `S` justified by taste alone.",
        "prevents": "architecture justified by aesthetics",
        "appliesWhen": "the domain has measurable forces; NOT licensed for purely social conventions",
        "anchor": TOPIC + ".S-002",
        "intent": "new",
    },
)

#: The seed form written with different slot letters — the same inference shape.
SLOT_VARIANT_FORM = (
    "Given a claimed property `Q` of design `E`, exhibit a counter-instance "
    "satisfying `E` but not `Q` => `Q` is not entailed by `E`."
)


def build_artifact(**overrides: str) -> str:
    """Render the well-formed artifact, replacing any section body by keyword.

    ``identity`` / ``criteria`` / ``decisions`` default to empty, which omits
    the optional criterion-layer sections entirely — the backward-compatibility
    path where A15 passes vacuously.
    """
    parts = {
        "identity": "",
        "sources": SOURCES,
        "unverifiable": UNVERIFIABLE,
        "moves": MOVES_APPLIED,
        "criteria": "",
        "chain": CHAIN,
        "termination": TERMINATION,
        "decisions": "",
        "arch": ARCH,
        "questions": QUESTIONS,
        "audit": AUDIT,
    }
    unknown = set(overrides) - set(parts)
    if unknown:
        raise AssertionError("unknown artifact section(s): %s" % sorted(unknown))
    parts.update(overrides)

    def opt(heading: str, body: str) -> str:
        return "%s\n\n%s\n\n" % (heading, body.strip("\n")) if body.strip() else ""

    return (
        "# Derivation: %s\n\n"
        "Concept authority: `shared/definitions/derivation-definitions.md`.\n\n"
        "%s"
        "## Sources\n\n%s\n\n## Unverifiable Sources\n\n%s\n\n"
        "## Reasoning Moves Applied\n\n%s\n\n"
        "%s"
        "## Derivation Chain\n\n%s\n\n"
        "## Termination\n\n%s\n\n"
        "%s"
        "## Derived Architecture\n\n%s\n\n"
        "## Open Questions\n\n%s\n\n## Self-Audit\n\n%s\n"
        % (TOPIC,
           opt("## Agent Identity", parts["identity"]),
           parts["sources"], parts["unverifiable"], parts["moves"],
           opt("## Criteria", parts["criteria"]),
           parts["chain"], parts["termination"],
           opt("## Decision Points", parts["decisions"]),
           parts["arch"], parts["questions"], parts["audit"])
    )


# --------------------------------------------------------------------------
# the degraded corpus (no online capability this run)
# --------------------------------------------------------------------------

DEGRADED_SOURCES = """| id | claimed_title | resolved_title | title_mismatch | grade | url | access | resolved_via | verification |
|---|---|---|---|---|---|---|---|---|
| S-001 | Title handed in first |  | false | unverified | <url-1> | unknown | direct | no-online-capability |
| S-002 | Title handed in second |  | false | unverified | <url-2> | unknown | direct | no-online-capability |
"""

DEGRADED_UNVERIFIABLE = """- `S-001` — no-online-capability: the host exposed no fetch/search tool this run.
- `S-002` — no-online-capability: the host exposed no fetch/search tool this run.
"""

#: A degraded run cannot inherit A11 as green; the honest attestation is
#: ``not-attested`` with a checkable method sentence (C-21 / C-46).
DEGRADED_AUDIT = AUDIT.replace(
    "| A11 | online grounding actually happened this run | every source was probed with the "
    "host fetch tool and each outcome recorded with its HTTP status in the verification column "
    "| attested |",
    "| A11 | online grounding actually happened this run | the host exposed no WebSearch or "
    "WebFetch tool this run, so no source could be grounded and none is claimed as verified "
    "| not-attested |",
)


def build_degraded_artifact(chain: str = "_None — degraded run, the chain was not built._\n",
                            arch: str = "_None — degraded run, no element is derived._\n") -> str:
    """An honest empty result: every source unverified/no-online-capability, no
    step, empty architecture (derivation-model.md C-45/C-46)."""
    return build_artifact(
        sources=DEGRADED_SOURCES,
        unverifiable=DEGRADED_UNVERIFIABLE,
        moves="_None — no move may be extracted from an ungrounded source._\n",
        chain=chain,
        termination="- condition: b\n- steps: 0 / 12\n",
        arch=arch,
        questions="_None._\n",
        audit=DEGRADED_AUDIT,
    )


# --------------------------------------------------------------------------
# engine invocation
# --------------------------------------------------------------------------

def load_engine_module(name: str = "derive_utils_under_test"):
    """Load the engine in-process (the filename carries a hyphen).

    Used for constants, pure functions, and the monkeypatched ``_http_get``
    transport seam — every behavioural assertion goes through the CLI subprocess
    so the shipped entry point is what is tested.
    """
    assert ENGINE.is_file(), f"engine missing: {ENGINE}"
    spec = importlib.util.spec_from_file_location(name, ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(workspace: Path, *args: str, fmt: str = "json",
        env: dict[str, str] | None = None) -> tuple[int, Any]:
    """Run the engine against `workspace`; return (exit code, parsed envelope).

    With fmt="text" the raw stdout string is returned instead of parsed JSON.
    """
    cmd = [sys.executable, str(ENGINE), "--workspace-root", str(workspace),
           "--format", fmt, *args]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180, env=env)
    if fmt != "json":
        return proc.returncode, proc.stdout
    try:
        return proc.returncode, json.loads(proc.stdout)
    except ValueError:  # pragma: no cover - diagnostics only
        return proc.returncode, {"_stdout": proc.stdout, "_stderr": proc.stderr,
                                 "_returncode": proc.returncode}


def scaffold(workspace: Path, slug: str = TOPIC, *extra: str) -> tuple[int, Any]:
    return run(workspace, "--action", "init", "--slug", slug, *extra)


def artifact_path(workspace: Path, slug: str = TOPIC) -> Path:
    return workspace / DERIVE_DIR / slug / "derive.md"


def write_artifact(workspace: Path, text: str, slug: str = TOPIC) -> Path:
    path = artifact_path(workspace, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def moves_spec_file(workspace: Path, moves: list[dict], name: str = "moves.json") -> Path:
    """Write a moves-add input file. The schema is ``{"moves": [...]}`` — there is
    no topic key; anchors arrive already qualified (C-28)."""
    path = workspace / name
    path.write_text(json.dumps({"moves": moves}, ensure_ascii=False), encoding="utf-8")
    return path


def move(name: str, form: str, anchor: str | None = None, intent: str = "new",
         prevents: str = "the failure this move blocks",
         appliesWhen: str = "when the shape applies; NOT licensed when it does not",
         **extra) -> dict:
    """Build one moves-add candidate (camelCase keys, qualified anchor by default)."""
    cand = {
        "name": name,
        "inferenceForm": form,
        "prevents": prevents,
        "appliesWhen": appliesWhen,
        "anchor": anchor if anchor is not None else TOPIC + ".S-001",
        "intent": intent,
    }
    cand.update(extra)
    return cand


def seed_library(workspace: Path, moves: tuple[dict, ...] | list[dict] = SEED_MOVES,
                 name: str = "moves.json") -> tuple[int, Any]:
    """Add moves through the engine's sole writer; assert the run succeeded."""
    spec_file = moves_spec_file(workspace, list(moves), name=name)
    code, env = run(workspace, "--action", "moves-add", "--file", str(spec_file))
    assert code == 0, f"seed moves-add failed ({code}): {env}"
    return code, env


def validate(workspace: Path, slug: str = TOPIC, *extra: str) -> tuple[int, dict]:
    code, env = run(workspace, "--action", "validate", "--slug", slug, *extra)
    assert isinstance(env, dict), env
    return code, env


def library_text(workspace: Path) -> str:
    return (workspace / MOVES_REL).read_text(encoding="utf-8")


def library_rows(workspace: Path) -> list[dict]:
    """Positional read of the library's data rows (synthetic cells carry no `\\|`)."""
    rows = []
    for line in library_text(workspace).splitlines():
        if not line.startswith("| M-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        assert len(cells) == len(MOVE_COLUMNS), cells
        rows.append(dict(zip(MOVE_COLUMNS, cells)))
    return rows


def library_ids(workspace: Path) -> list[str]:
    return [row["move_id"] for row in library_rows(workspace)]


def codes(env: dict) -> list[str]:
    return [e["code"] for e in env.get("errors", [])]


def rules(env: dict) -> list[str]:
    return sorted({e["rule"] for e in env.get("errors", [])})


def triples(env: dict) -> list[tuple[str, str, str]]:
    return [(e["rule"], e["code"], e["locator"]) for e in env.get("errors", [])]


def warning_codes(env: dict) -> list[str]:
    return sorted({w["code"] for w in env.get("warnings", [])})
