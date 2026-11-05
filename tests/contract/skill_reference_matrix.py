"""Test-only executable projection of the skill-reference normalization (T024).

This is **not** a pytest module, **not** a gate, and **not** a runtime implementation.
It is the single executable form of the grammar owned by
``shared/definitions/skill-reference-definitions.md`` (§ Normalization, steps NP-1…NP-8),
imported by the five ``tests/contract/test_skill_reference_*.py`` modules. The meta-skills
normalize in place per the owner body; this module only proves that the process the owner
states can be replayed line by line by a machine (plan.md § D11, GM-14 gap).

Discipline carried here:

* stdlib only — ``json``, ``pathlib``, ``re`` — and **nothing imported from the
  repository**: the known location set is declared here as data, reached by reference to
  its owner (see :data:`KNOWN_LOCATIONS`);
* fixture rows that must not depend on what the live tree contains carry ``repo_root:
  "scratch"``; for those, ``dev-canonical`` is ``skills/external`` and ``installed`` is
  ``.specify/skills`` (both ladder entries — the scratch narrows *which* entry names each
  layer, it does not add one);
* a pure function from ``(raw string, form)`` to the closed three-valued outcome with the
  normalized identifier and the paired-report fields;
* **no assertions and no I/O at module level** — the filesystem is read only when a caller
  passes ``repo_root``, and nothing is written ever.

Step order (owner § Normalization; **not exchangeable** — NP-3 / NP-4 run before NP-6):
form determination → trim/quote → ``skill:`` → ``@``// → ``SKILL.md``// → channel → hit →
output.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# --- Closed value domains -----------------------------------------------------------

#: § Normalization — "Output shape — exactly three values, closed".
OUTCOMES = ("command-surface", "skill", "failure")

#: § Failure semantics — four classes; names literal with ``data-model.md`` E-10.
FAILURE_CLASSES = ("zero-hit", "out-of-ladder", "unreadable", "dual-layer")

#: § Accepted forms — the six literal ``form`` values (frozen table, owner § Accepted forms).
FORMS = (
    "bare name",
    "slash reference",
    "at reference",
    "labelled reference",
    "canonical path",
    "directory path",
)

#: NP-1 — the two operation forms ("the two forms differ only in failure reachability").
OPERATIONS = ("invocation", "cli")

#: Failure-semantics foot rule for ``@name`` in the ``cli`` form.
UNREACHABLE_IN_CLI_NOTE = "this form is unreachable in the cli form"

#: § Disambiguation rules (b) — the command namespace and its template target.
COMMAND_NAMESPACE = "speckit.*"
COMMAND_TEMPLATE = "templates/commands/{stem}.md"

#: Required report items per class (owner § Failure semantics table). Enforced for every
#: class by this module, not only stated: the first two are FR-025's paired report.
COMMON_REPORT_ITEMS = ("raw", "normalized")
REQUIRED_REPORT_ITEMS = {
    "zero-hit": COMMON_REPORT_ITEMS + ("searched_coordinates",),
    "out-of-ladder": COMMON_REPORT_ITEMS + ("path", "known_locations"),
    "unreadable": COMMON_REPORT_ITEMS + ("path", "defect"),
    "dual-layer": COMMON_REPORT_ITEMS + ("candidate_paths",),
}

#: The known location set. **Owner**: ``skills/internal/run-skills/SKILL.md`` § 1 — this
#: tuple is the trust boundary expressed as data, reached *by reference* and never a
#: priority claim (GR-09 / FR-022). Only a residual outside every entry is out-of-ladder.
KNOWN_LOCATIONS = (
    "skills/internal",
    "skills/external",
    ".specify/skills/internal",
    ".specify/skills",
)

#: Layers (§ Disambiguation rules (c) — the criterion is the layer, not the path literal:
#: a source directory and its ``.specify/`` mirror are two layers).
LAYERS = ("dev-canonical", "installed")

_LABEL_RE = re.compile(r"^skill:")
_QUOTE_PAIRS = (('"', '"'), ("'", "'"))
#: A dotted name in the ``/speckit.*`` namespace. No other character-class assertion is
#: made — the name channel must not reject legal dotted names (§ Normalization).
_COMMAND_NAME_RE = re.compile(r"^speckit\.[A-Za-z0-9][A-Za-z0-9._-]*$")


# --- Fixture access ----------------------------------------------------------------


def matrix_path(repo_root):
    """The fixture's single sanctioned location (plan.md § D13, GM-13)."""
    return Path(repo_root) / "tests" / "fixtures" / "skill-reference" / "normalization-matrix.json"


def load_matrix(path):
    """Read a matrix fixture and return its ``rows`` (no validation, no assertion)."""
    return json.loads(Path(path).read_text(encoding="utf-8"))["rows"]


#: Which directory under a repository root represents each layer for a scratch fixture.
#: Both are already ladder entries, so this map adds no location; a scratch layer is one
#: directory, which is what makes "two different layers" genuinely two (V-33).
LAYER_DIRS = {
    "dev-canonical": "skills/external",
    "installed": ".specify/skills",
}


def materialize_scratch(scratch, root):
    """Materialize a row's ``scratch`` block under ``root`` and return ``root``.

    ``{"layer": {<layer>: {<name>: {"frontmatter": bool, "body": str}}}, "unreadable": [...]}``
    writes ``<LAYER_DIRS[layer]>/<name>/SKILL.md``; a name whose ``frontmatter`` is false gets
    a body with no frontmatter so that NP-7 reads it as ``unreadable``. This writer exists so
    that the case-insensitive, dual-layer and unreadable rows are decided by the fixture,
    never by whatever the live tree happens to contain today.
    """
    for layer, skills in (scratch.get("layer") or {}).items():
        for name, spec in skills.items():
            target = Path(root) / LAYER_DIRS[layer] / name
            target.mkdir(parents=True, exist_ok=True)
            body = spec.get("body") or ""
            if spec.get("frontmatter"):
                text = f"---\nname: {name}\ndescription: scratch fixture skill\n---\n\n{body}"
            else:
                text = body or "no frontmatter here\n"
            (target / "SKILL.md").write_text(text, encoding="utf-8")
    return Path(root)


# --- Path helpers (pure) ------------------------------------------------------------


def layer_of(path):
    """Return the layer a repository-relative path belongs to, or ``None`` if unknown."""
    text = str(path).replace("\\", "/")
    while text.startswith("./"):
        text = text[2:]
    if text.startswith(".specify/"):
        return "installed"
    if text.startswith("skills/") or text.startswith("templates/"):
        return "dev-canonical"
    return None


def split_identifier(identifier):
    """Split a normalized path-channel identifier into ``(name, layer)``.

    ``skills/external/merge-skills`` → ``("merge-skills", "dev-canonical")``.
    """
    segments = [s for s in str(identifier).replace("\\", "/").split("/") if s]
    if segments and segments[-1] == "SKILL.md":
        segments = segments[:-1]
    return ((segments[-1] if segments else ""), layer_of(identifier))


def is_command_name(name):
    """Is this normalized name in the ``/speckit.*`` command namespace?"""
    return bool(_COMMAND_NAME_RE.match(str(name)))


# --- NP-2 … NP-5: the string steps --------------------------------------------------


def _trim_and_requote(raw):
    """NP-2 — trim whitespace, then one **paired** wrapping quote.

    Returns ``(text, ok)``. An unpaired quote is not a silent trim: ``ok`` is ``False``.
    """
    text = str(raw).strip()
    for opening, closing in _QUOTE_PAIRS:
        if text.startswith(opening) or text.endswith(closing):
            if len(text) >= 2 and text.startswith(opening) and text.endswith(closing):
                return text[1:-1], True
            return text, False
    return text, True


def _strip_label(text):
    """NP-3 — strip **one** ``skill:`` label (never recursive)."""
    return _LABEL_RE.sub("", text, count=1)


def _strip_prefix(text):
    """NP-4 — strip **one** ``@`` or ``/`` prefix; ``@/name`` is one segment."""
    if text.startswith("@"):
        text = text[1:]
        return text[1:] if text.startswith("/") else text
    if text.startswith("/"):
        return text[1:]
    return text


def _strip_suffix(text):
    """NP-5 — strip one ``SKILL.md`` suffix or one trailing ``/``, in that order.

    Any other ``.md`` is **not** stripped: omit-extension is a settlement convention, not
    a normalization step.
    """
    for suffix in ("/SKILL.md", "SKILL.md"):
        if text.endswith(suffix):
            return text[: -len(suffix)]
    if text.endswith("/"):
        return text[:-1]
    return text


# --- Result constructors ------------------------------------------------------------


def _result(raw, outcome, normalized, **payload):
    record = {
        "raw": raw,
        "outcome": outcome,
        "normalized": normalized,
        "decision_class": outcome,
    }
    record.update(payload)
    return record


def command_surface(raw, normalized):
    """A normalized name in the ``/speckit.*`` namespace is a command, not a Skill.

    It MUST NOT be resolved as a Skill and MUST NOT be force-executed (FR-023(b)).
    """
    stem = normalized.split(".", 1)[1] if "." in normalized else ""
    return _result(
        raw,
        "command-surface",
        normalized,
        command=normalized,
        command_target=COMMAND_TEMPLATE.format(stem=stem),
        namespace=COMMAND_NAMESPACE,
        enters_skill_resolution=False,
    )


def skill(raw, normalized, channel, located, *, case_pass="exact", operation="invocation"):
    """A resolved Skill: the name and layer, with the ladder reached by reference only."""
    return _result(
        raw,
        "skill",
        normalized,
        id=split_identifier(normalized)[0],
        channel=channel,
        layer=layer_of(located),
        located=located,
        case_pass=case_pass,
        operation=operation,
        # FR-022 / V-29: where a name would be found is the ladder's product, not this one.
        by_ladder={"reference": "skills/internal/run-skills/SKILL.md § 1"},
    )


def failure(raw, normalized, failure_class, operation="invocation", note=None, **items):
    """One closed failure row: class + every required report item + paired raw/normalized.

    ``operation`` and ``note`` sit on the row, next to ``failure_class``, so that
    ``report_items`` carries exactly the class's required items and nothing else — a report
    whose required items cannot be told apart from its annotations is not checkable.
    """
    if failure_class not in FAILURE_CLASSES:
        raise ValueError(f"not a failure class: {failure_class!r}")
    report = dict(items)
    report["raw"] = raw
    report["normalized"] = normalized
    missing = [item for item in REQUIRED_REPORT_ITEMS[failure_class] if item not in report]
    if missing:
        raise ValueError(f"{failure_class} row missing required report items: {missing}")
    row = _result(
        raw,
        "failure",
        normalized,
        failure_class=failure_class,
        operation=operation,
        report_items=report,
    )
    if note is not None:
        row["note"] = note
    return row


# --- NP-6 / NP-7: the hit test (filesystem read only when repo_root is given) --------


def _frontmatter_defect(skill_md):
    """Return a defect string for an unreadable ``SKILL.md`` / invalid frontmatter."""
    try:
        text = Path(skill_md).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return f"unreadable file: {exc.__class__.__name__}"
    if not text.startswith("---"):
        return "frontmatter: missing opening ---"
    end = text.find("\n---", 3)
    if end == -1:
        return "frontmatter: missing closing ---"
    keys = {line.split(":", 1)[0].strip() for line in text[3:end].splitlines() if ":" in line}
    missing = [key for key in ("name", "description") if key not in keys]
    return "frontmatter: missing " + ", ".join(missing) if missing else None


def _name_candidates(name, repo_root, insensitive=False):
    """Name channel: every existing ``<location>/<name>/SKILL.md`` in one comparison pass.

    ``insensitive=False`` is the first (exact) pass; ``insensitive=True`` is the second
    pass and runs **only** on zero hits (§ Normalization, case rule). Both passes are
    still expressed as (name per location), never as "pick the nearest".
    """
    folded = name.lower()
    hits = []
    for location in KNOWN_LOCATIONS:
        if not insensitive:
            # The exact pass compares every candidate that exists in the layer, never a
            # constructed path: on a case-insensitive filesystem ``mkdir('x')`` followed by
            # ``is_file('X/SKILL.md')`` would make an "exact" hit out of a case variant and
            # skip NP-7's second pass. The comparison is on the string, the layer is the unit.
            root = Path(repo_root) / location
            if not root.is_dir():
                continue
            for child in sorted(root.iterdir()):
                if child.name == name and (child / "SKILL.md").is_file():
                    hits.append((child / "SKILL.md").relative_to(Path(repo_root)).as_posix())
            continue
        root = Path(repo_root) / location
        if not root.is_dir():
            continue
        children = sorted(child for child in root.iterdir() if (child / "SKILL.md").is_file())
        for child in children:
            if child.name.lower() != folded:
                continue
            # A case-only continuation of a same-layer match is still one hit: the layer is
            # the criterion, so one layer already matching must not be read as a second one.
            located = (child / "SKILL.md").relative_to(Path(repo_root)).as_posix()
            if located not in hits:
                hits.append(located)
    return hits


def _hit_plane(residual, repo_root):
    """Path channel: the trust boundary first, then the directory, then readability."""
    if any(segment == ".." for segment in residual.split("/")):
        return "out-of-ladder"
    if not any(residual == loc or residual.startswith(loc + "/") for loc in KNOWN_LOCATIONS):
        return "out-of-ladder"
    if not (Path(repo_root) / residual).is_dir():
        return "zero-hit"
    if _frontmatter_defect(Path(repo_root) / residual / "SKILL.md") is not None:
        return "unreadable"
    return None


# --- The public pure function -------------------------------------------------------


def normalize(raw, form="bare name", operation="invocation", repo_root=None):
    """Normalize one skill reference → the closed three-valued outcome.

    Parameters
    ----------
    raw:
        The reference exactly as received, whitespace and wrapping quotes included.
    form:
        One of :data:`FORMS`. Every form reaches the same normalized identifier, so this
        only selects the operation form when it is ``"cli"`` / ``"invocation"``.
    operation:
        NP-1 — ``invocation`` (a chat-message parameter) or ``cli`` (a command token).
    repo_root:
        ``None`` → no I/O at all: the string steps run and a name- or path-shaped residual
        is returned as its own normalized identifier (NP-6's channel decision), leaving the
        hit test to the caller. Otherwise NP-7 reads the position ladder under this root.

    Returns
    -------
    dict
        ``raw``, ``outcome`` ∈ :data:`OUTCOMES`, ``normalized``, ``decision_class`` (the
        same value, named for the paired report), plus the outcome's payload.
    """
    raw = str(raw)
    if form in OPERATIONS:
        operation = form
    elif form not in FORMS:
        raise ValueError(f"unknown accepted form: {form!r}")
    if operation not in OPERATIONS:
        raise ValueError(f"unknown operation form: {operation!r}")

    found = list(KNOWN_LOCATIONS)

    # NP-2 — trim + one paired wrapping quote.
    text, paired = _trim_and_requote(raw)
    if not paired:
        # An unpaired quote is a failure, not a silent trim: the residual keeps the quote.
        return failure(raw, text, "zero-hit", operation=operation,
                       searched_coordinates=found, note="unpaired wrapping quote")

    # NP-1 / C11 — the CLI consumes ``@`` before the meta-skill sees it.
    if operation == "cli" and text.lstrip().startswith("@"):
        residual = _strip_suffix(_strip_prefix(_strip_label(text.lstrip())))
        return failure(raw, residual, "zero-hit", searched_coordinates=[], operation=operation,
                       note=UNREACHABLE_IN_CLI_NOTE)

    # NP-3, then NP-4 — strictly before NP-6.
    text = _strip_prefix(_strip_label(text))
    if not text:
        return failure(raw, "", "zero-hit", searched_coordinates=found)

    # NP-5.
    text = _strip_suffix(text)
    if not text:
        return failure(raw, "", "zero-hit", searched_coordinates=found)

    # NP-6 — channel test is one criterion: does the residual contain ``/``?
    channel = "path" if "/" in text else "name"

    # NP-8 for the command namespace: a command name is never resolved as a Skill, whether
    # or not hits would exist (FR-023(b)). A dotted name is an ordinary name otherwise.
    if channel == "name" and is_command_name(text):
        return command_surface(raw, text)

    if repo_root is None:
        # No I/O: the residual is the normalized identifier; the hit test is the caller's.
        return skill(raw, text, channel, None, operation=operation)

    # NP-7 — hit test.
    if channel == "path":
        plane = _hit_plane(text, repo_root)
        if plane == "out-of-ladder":
            return failure(raw, text, "out-of-ladder", path=text, known_locations=found)
        if plane == "zero-hit":
            return failure(raw, text, "zero-hit", searched_coordinates=found)
        if plane == "unreadable":
            defect = _frontmatter_defect(Path(repo_root) / text / "SKILL.md")
            return failure(raw, text, "unreadable", path=text, defect=defect)
        return skill(raw, text, channel, f"{text}/SKILL.md", operation=operation)

    case_pass = "exact"
    hits = _name_candidates(text, repo_root)
    if not hits:
        # Second pass, only on zero hits: one case-insensitive comparison.
        case_pass = "insensitive"
        hits = _name_candidates(text, repo_root, insensitive=True)
    if not hits:
        return failure(raw, text, "zero-hit", searched_coordinates=found)

    by_layer = {}
    for hit in hits:
        by_layer.setdefault(layer_of(hit) or "unknown", []).append(hit)
    if len(by_layer) > 1:
        return failure(raw, text, "dual-layer",
                       candidate_paths=sorted(hit for group in by_layer.values() for hit in group))
    located = sorted(next(iter(by_layer.values())))[0]
    # Two hits inside one layer are one hit (FR-023(c)); the layer is the criterion.
    return skill(raw, text, channel, located, case_pass=case_pass, operation=operation)
