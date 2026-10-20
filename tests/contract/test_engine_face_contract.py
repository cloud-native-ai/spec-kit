"""Contract test: the compiled wrap-up face & engine arguments (Feature 063 US3).

Pins ``engine-face-contract.md`` C-20..C-24 (F4, FR-014..FR-017 / SC-007, SC-008):

* C-20 — every kind=engine handler line renders the action's full required set
  plus its declared source arguments, run-scoped values carried as angle-bracket
  placeholders (``--run-id <RUN_ID>``); the placeholder convention (syntax,
  substitution rule, rendered-set membership) is declared ONCE in the registry's
  § Handler note and rendered verbatim, once per section, only when an engine
  line carries a placeholder.
* C-21 — the rendered set per (engine, action) is exactly the engine's manifest:
  a flag the action does not accept never renders, and the renderer holds no
  hand-written argument table.
* C-22 — each wrap-up engine (run-determination, feedback-utils, exec-quant)
  exposes ``--action args-manifest`` emitting JSON ``{action: {required,
  source}}`` built from its own parser; an engine/action pair without a
  manifest fails the compile loudly (registry/engine divergence is a fast-fail
  surface).
* C-23 — ``determine`` (run-determination) and ``record`` (feedback-utils)
  report ALL missing required arguments in ONE error; the input-error exit code
  stays 2.
* C-24 — the (unit_id, run_id) idempotency is byte-for-byte: a duplicate call
  returns ``{"duplicate": true}`` exit 0 and writes no second record; no engine
  code path mints/derives a run-id; feedback's duplicate no-op is unchanged.

Red before the mechanisms land (Tests Mode = ON, Constitution Principle IV).
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tests.script_api import probe_utils

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINES = {
    "run-determination": REPO_ROOT / "scripts" / "python" / "run-determination.py",
    "feedback-utils": REPO_ROOT / "scripts" / "python" / "feedback-utils.py",
    "exec-quant": REPO_ROOT / "scripts" / "python" / "exec-quant.py",
}
REGISTRY = REPO_ROOT / "shared" / "definitions" / "probe-definitions.md"
PROBE_UTILS = REPO_ROOT / "scripts" / "python" / "probe-utils.py"


# --------------------------------------------------------------------------- #
# Manifest helpers (C-22)
# --------------------------------------------------------------------------- #

def _manifest(engine_path: Path) -> dict:
    out = subprocess.run(
        [sys.executable, str(engine_path), "--action", "args-manifest"],
        capture_output=True, text=True, check=False)
    assert out.returncode == 0, (
        f"{engine_path.name} --action args-manifest failed (rc={out.returncode}): "
        f"{out.stderr.strip()[:300]}"
    )
    return json.loads(out.stdout)


def _load_engine(engine_path: Path):
    name = "_efc_" + engine_path.stem.replace("-", "_")
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, engine_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _parser_flags(module) -> set:
    return {opt for action in module.build_parser()._actions
            for opt in action.option_strings}


@pytest.mark.contract
def test_c22_all_wrap_up_engines_expose_args_manifest():
    for name, path in ENGINES.items():
        manifest = _manifest(path)
        assert isinstance(manifest, dict) and manifest, (
            f"{name}: args-manifest must emit a non-empty JSON object"
        )
        for action, spec in manifest.items():
            assert isinstance(spec, dict), f"{name}:{action} spec must be a dict"
            for key in ("required", "source"):
                assert isinstance(spec.get(key), list), (
                    f"{name}:{action}.{key} must be a list"
                )
                assert all(isinstance(f, str) and f.startswith("--")
                           for f in spec[key]), (
                    f"{name}:{action}.{key} must list `--flag` strings"
                )


@pytest.mark.contract
def test_c22_manifest_flags_live_on_the_engine_parser():
    """Built from the engine's OWN parser: a flag absent from the live parser
    can never appear in the manifest (no stale parallel table)."""
    for name, path in ENGINES.items():
        module = _load_engine(path)
        live = _parser_flags(module)
        manifest = _manifest(path)
        for action, spec in manifest.items():
            for key in ("required", "source"):
                unknown = [f for f in spec[key] if f not in live]
                assert not unknown, (
                    f"{name}:{action}.{key} names flags the parser does not "
                    f"accept: {unknown}"
                )


@pytest.mark.contract
def test_c22_determine_manifest_carries_the_normative_sets():
    spec = _manifest(ENGINES["run-determination"])["determine"]
    assert {"--run-id", "--complexity"} <= set(spec["required"]), (
        "the determine face MUST carry at least the required set (C-20)"
    )
    assert {"--session-file", "--session-rows", "--tool",
            "--declared-check", "--green-check"} <= set(spec["source"]), (
        "the determine face MUST carry at least the source exemplars (C-20)"
    )


@pytest.mark.contract
def test_c22_record_manifest_required_set():
    spec = _manifest(ENGINES["feedback-utils"])["record"]
    assert {"--unit-id", "--run-id", "--review", "--points"} <= set(spec["required"])


# --------------------------------------------------------------------------- #
# Renderer (C-20 / C-21) — over the compile-embeds sandbox fixture
# --------------------------------------------------------------------------- #

def _embeds_suite():
    path = REPO_ROOT / "tests" / "contract" / "test_compile_embeds.py"
    spec = importlib.util.spec_from_file_location("_efc_compile_embeds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["_efc_compile_embeds"] = module
    spec.loader.exec_module(module)
    return module


CE = _embeds_suite()


def _wrap_up_section(text: str) -> str:
    m = re.search(r"(?ms)^## Wrap-up\n.*?(?=^## |\Z)", text)
    assert m, "no compiled `## Wrap-up` section in the artifact"
    return m.group(0)


def _sandbox_face(tmp_path: Path, capsys, registry_text: str = None) -> str:
    if registry_text is None:
        registry_text = REGISTRY.read_text(encoding="utf-8")
    ws = CE._build_workspace(tmp_path, registry_text)
    rc, payload = CE._run(ws, capsys)
    assert rc == 0, f"sandbox compile must be green before face assertions: {payload}"
    return CE._unit_paths(ws)["/speckit.sandbox-a"].read_text(encoding="utf-8")


def _engine_lines(face: str) -> dict:
    """{(engine_name, action): rendered line} for every kind=engine line."""
    out = {}
    for line in face.splitlines():
        m = re.match(r"^\d+\. .+? — `python3 \S+/(\S+)\.py --action (\S+)", line)
        if m:
            out[(m.group(1), m.group(2))] = line
    return out


@pytest.mark.contract
def test_c20_face_renders_required_and_source_placeholders(tmp_path, capsys):
    face = _sandbox_face(tmp_path, capsys)
    lines = _engine_lines(face)
    assert ("run-determination", "determine") in lines
    rundet = lines[("run-determination", "determine")]
    assert "--run-id <RUN_ID>" in rundet and "--complexity <COMPLEXITY>" in rundet, (
        "the determine line MUST render the required set as placeholders (C-20)"
    )
    assert "source args when available" in rundet
    for flag in ("--session-file", "--session-rows", "--tool",
                 "--declared-check", "--green-check"):
        assert re.search(re.escape(flag) + r" <[A-Z_]+>", rundet), (
            f"determine line MUST render source exemplar {flag} (C-20)"
        )
    fb = lines[("feedback-utils", "record")]
    assert "--run-id <RUN_ID>" in fb and "--review <REVIEW>" in fb \
        and "--points <POINTS>" in fb, (
        "the record line MUST render its required set as placeholders (C-20)"
    )
    eq = lines[("exec-quant", "collect")]
    assert "--run-id <RUN_ID>" in eq, (
        "collect's declared source argument --run-id MUST render (C-20)"
    )


@pytest.mark.contract
def test_c20_convention_is_declared_in_the_registry_note():
    text = REGISTRY.read_text(encoding="utf-8")
    note = re.search(r"(?ms)^## Handler\n(.*?)^\|", text).group(1)
    m = re.search(r"Compiled-face convention line[:：]\s*(.+)", note)
    assert m, (
        "the placeholder convention MUST be declared in the registry § Handler "
        "note, not per command hand-written (C-20)"
    )
    assert "代入后照抄执行" in note, "the substitution rule MUST be declared (C-20)"
    assert re.search(r"大写|uppercase", note), (
        "the placeholder syntax MUST be declared (C-20)"
    )
    assert re.search(r"required|source", note), (
        "the rendered-set membership rule MUST be declared (C-20)"
    )


@pytest.mark.contract
def test_c20_convention_line_rendered_once_verbatim(tmp_path, capsys):
    face = _sandbox_face(tmp_path, capsys)
    text = REGISTRY.read_text(encoding="utf-8")
    convention = re.search(r"Compiled-face convention line[:：]\s*(.+)", text).group(1)
    face_lines = face.splitlines()
    hits = [l for l in face_lines if convention in l]
    assert len(hits) == 1, (
        "exactly ONE convention line per section when a placeholder is present "
        f"(got {len(hits)}: {hits})"
    )
    first_placeholder = next(i for i, l in enumerate(face_lines)
                             if re.search(r"--[a-z-]+ <[A-Z_]+>", l))
    emitted_at = face_lines.index(hits[0])
    assert first_placeholder < emitted_at <= first_placeholder + 2, (
        "the convention line renders directly after the first placeholder line"
    )


@pytest.mark.contract
def test_c20_no_placeholder_free_section_carries_no_convention(tmp_path, capsys):
    # Agent-only wrap-up projection: no engine line, no placeholder, no convention.
    registry = "\n".join(
        line for line in REGISTRY.read_text(encoding="utf-8").splitlines()
        if not re.match(r"^\|\s*h-(run-determination|exec-quant|feedback-record)\s*\|",
                        line))
    assert "h-run-determination | engine" not in registry
    face = _sandbox_face(tmp_path, capsys, registry)
    assert not _engine_lines(face), "agent-only projection must render no engine line"
    assert not re.search(r"--[a-z-]+ <[A-Z_]+>", face), \
        "agent-only projection must carry no placeholder"
    m = re.search(r"Compiled-face convention line[:：]\s*(.+)",
                  REGISTRY.read_text(encoding="utf-8"))
    assert m and m.group(1) not in face, (
        "a section with no placeholder MUST NOT carry the convention line (C-20)"
    )


@pytest.mark.contract
def test_c21_rendered_flags_are_exactly_the_manifest_set(tmp_path, capsys):
    """Bidirectional C-21 pin: per (engine, action) the rendered flag set is
    exactly the manifest's required ∪ source (minus the identity pair the base
    call line already carries with real values) — nothing extra (a non-accepted
    argument never renders), nothing missing."""
    face = _sandbox_face(tmp_path, capsys)
    manifests = {name: _manifest(path) for name, path in ENGINES.items()}
    assert _engine_lines(face), "no engine lines rendered"
    for (engine, action), line in _engine_lines(face).items():
        spec = manifests[engine][action]
        # The base call form carries --action/--unit-id/--unit-type with real
        # values; EVERY further flag comes from the manifest (the renderer
        # skips identity-pair duplicates) — extra flags are C-21 violations,
        # missing ones are C-20 violations.
        expected = ({"--action", "--unit-id", "--unit-type"}
                    | set(spec["required"]) | set(spec["source"]))
        rendered = set(re.findall(r"--[a-z][a-z0-9-]*", line))
        assert rendered == expected, (
            f"{engine} --action {action}: rendered set drifted from the engine "
            f"manifest — extra={sorted(rendered - expected)} "
            f"missing={sorted(expected - rendered)}"
        )


@pytest.mark.contract
def test_c21_renderer_holds_no_handwritten_argument_table():
    src = PROBE_UTILS.read_text(encoding="utf-8")
    for flag in ("--run-id", "--complexity", "--review", "--points",
                 "--session-file", "--session-rows", "--tool",
                 "--declared-check", "--green-check", "--score",
                 "--snapshot", "--config-id"):
        assert f'"{flag}"' not in src, (
            f"probe-utils.py hand-writes engine argument {flag} — the rendered "
            "set MUST come from the engine manifests (C-21)"
        )


@pytest.mark.contract
def test_c22_missing_manifest_fails_the_compile_loudly(tmp_path, capsys):
    registry = REGISTRY.read_text(encoding="utf-8")
    ws = CE._build_workspace(tmp_path, registry)
    engine = ws / "scripts" / "python" / "run-determination.py"
    stripped = engine.read_text(encoding="utf-8").replace(
        '"args-manifest"', '"args-manifest-disabled"')
    assert stripped != engine.read_text(encoding="utf-8"), (
        "mutation must actually strip the manifest action"
    )
    engine.write_text(stripped, encoding="utf-8")
    rc = probe_utils.main(["--action", "compile-embeds",
                           "--workspace-root", str(ws), "--format", "json"])
    assert rc == 2, (
        f"an engine/action pair without a manifest MUST fail the compile loudly "
        f"(rc=2), got rc={rc}"
    )
    err = capsys.readouterr().err
    assert "h-run-determination" in err, (
        f"the refusal MUST name the handler: {err[:400]}"
    )
    assert re.search(r"manifest", err, re.I), (
        f"the refusal MUST name the manifest divergence: {err[:400]}"
    )


@pytest.mark.contract
def test_c20_repo_compiled_face_carries_the_full_argument_form():
    """The live deliverable face (not only the sandbox renderer): a compiled
    command unit carries the required set, source args and the convention line."""
    unit = REPO_ROOT / "templates" / "commands" / "implement.md"
    section = _wrap_up_section(unit.read_text(encoding="utf-8"))
    assert "--run-id <RUN_ID>" in section and "--complexity <COMPLEXITY>" in section
    assert "source args when available" in section
    convention = re.search(r"Compiled-face convention line[:：]\s*(.+)",
                           REGISTRY.read_text(encoding="utf-8")).group(1)
    assert convention in section, "the repo face MUST carry the convention line"


# --------------------------------------------------------------------------- #
# One-shot missing-argument errors (C-23)
# --------------------------------------------------------------------------- #

def _run_engine(engine_path: Path, args: list, ws: Path):
    return subprocess.run(
        [sys.executable, str(engine_path), *args, "--workspace-root", str(ws)],
        capture_output=True, text=True, check=False)


def _scratch_ws(tmp_path: Path) -> Path:
    ws = tmp_path / "ws"
    (ws / ".specify").mkdir(parents=True)
    return ws


@pytest.mark.contract
def test_c23_determine_lists_all_missing_args_in_one_error(tmp_path):
    ws = _scratch_ws(tmp_path)
    out = _run_engine(ENGINES["run-determination"],
                      ["--action", "determine", "--unit-id", "/speckit.us3-c23",
                       "--unit-type", "command"], ws)
    assert out.returncode == 2, "input-error exit code MUST stay 2 (C-23)"
    err = out.stderr
    assert "--run-id" in err and "--complexity" in err, (
        f"a call missing 2 required args MUST name BOTH in one error: {err[:300]}"
    )
    assert err.count("error:") == 1, (
        f"exactly ONE error message, not sequential one-at-a-time checks: {err[:300]}"
    )


@pytest.mark.contract
def test_c23_determine_missing_unit_id_joins_the_one_error(tmp_path):
    ws = _scratch_ws(tmp_path)
    out = _run_engine(ENGINES["run-determination"],
                      ["--action", "determine"], ws)
    assert out.returncode == 2
    err = out.stderr
    for flag in ("--unit-id", "--run-id", "--complexity"):
        assert flag in err, f"missing {flag} MUST be named in the one error: {err[:300]}"
    assert err.count("error:") == 1


@pytest.mark.contract
def test_c23_record_lists_all_missing_args_in_one_error(tmp_path):
    ws = _scratch_ws(tmp_path)
    out = _run_engine(ENGINES["feedback-utils"],
                      ["--action", "record", "--unit-id", "/speckit.us3-c23",
                       "--unit-type", "command"], ws)
    assert out.returncode == 2, "input-error exit code MUST stay 2 (C-23)"
    err = out.stderr
    for flag in ("--run-id", "--review", "--points"):
        assert flag in err, f"missing {flag} MUST be named in the one error: {err[:300]}"
    assert err.count("error:") == 1, (
        f"exactly ONE error message, not sequential one-at-a-time checks: {err[:300]}"
    )


# --------------------------------------------------------------------------- #
# Idempotency & no-minting (C-24)
# --------------------------------------------------------------------------- #

def _determine(ws: Path, run_id: str, fmt: list = None):
    return _run_engine(ENGINES["run-determination"],
                       ["--action", "determine", "--unit-id", "/speckit.us3-c24",
                        "--unit-type", "command", "--run-id", run_id,
                        "--complexity", "complex", *(fmt or [])], ws)


@pytest.mark.contract
def test_c24_duplicate_determine_is_exit_zero_no_second_record(tmp_path):
    ws = _scratch_ws(tmp_path)
    first = _determine(ws, "s63-c24-run-1")
    assert first.returncode == 0
    session_dir = ws / ".specify" / "memory" / "session"
    assert session_dir.is_dir()
    assert len(list(session_dir.glob("*.md"))) == 1

    second = _determine(ws, "s63-c24-run-1", ["--json"])
    assert second.returncode == 0, "a duplicate key MUST be exit 0, never an error"
    payload = json.loads(second.stdout)
    assert payload.get("duplicate") is True
    assert payload.get("run_id") == "s63-c24-run-1"
    assert len(list(session_dir.glob("*.md"))) == 1, (
        "the duplicate path MUST NOT write a second record (C-24)"
    )
    body = next(session_dir.glob("*.md")).read_text(encoding="utf-8")
    assert "s63-c24-run-1" in body


@pytest.mark.contract
def test_c24_engine_never_mints_a_run_id(tmp_path):
    # Missing --run-id is an input error and never a write — the engine does
    # not substitute a synthesized run-id under any circumstance (C-24).
    ws = _scratch_ws(tmp_path)
    out = _run_engine(ENGINES["run-determination"],
                      ["--action", "determine", "--unit-id", "/speckit.us3-c24",
                       "--unit-type", "command", "--complexity", "complex"], ws)
    assert out.returncode == 2
    session_dir = ws / ".specify" / "memory" / "session"
    assert not session_dir.is_dir() or not list(session_dir.glob("*.md")), (
        "a call missing --run-id must not leave any record behind"
    )
    # Source-level mutation drill: no run-id synthesis helper feeds run_id, and
    # --run-id carries no non-None default.
    src = ENGINES["run-determination"].read_text(encoding="utf-8")
    assert not re.search(r"run_id.{0,60}(uuid|token_hex|secrets\.|timestamp_id)",
                         src), "no engine path may synthesize a run_id"
    assert not re.search(r'"--run-id"[^\n]*default=(?!None)', src), (
        "--run-id must have no value default (a default would be a silent mint)"
    )


@pytest.mark.contract
def test_c24_feedback_record_duplicate_is_a_no_op(tmp_path):
    ws = _scratch_ws(tmp_path)
    common = ["--action", "record", "--unit-id", "/speckit.us3-c24",
              "--unit-type", "command", "--run-id", "s63-c24-fb",
              "--review", "test review", "--points",
              "No significant optimization points identified this run."]
    first = _run_engine(ENGINES["feedback-utils"], common, ws)
    assert first.returncode == 0
    entries_dir = ws / ".specify" / "memory" / "feedback"
    assert entries_dir.is_dir()
    assert len(list(entries_dir.glob("*.md"))) == 1

    second = _run_engine(ENGINES["feedback-utils"], common + ["--format", "json"], ws)
    assert second.returncode == 0, "the duplicate no-op MUST stay exit 0"
    payload = json.loads(second.stdout)
    assert payload.get("duplicate") is True
    assert len(list(entries_dir.glob("*.md"))) == 1, (
        "the duplicate no-op MUST NOT create a second entry (C-24)"
    )
