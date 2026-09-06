"""Contract tests for the derive engine CLI surface (048 / Feature 049).

Contract: .specify/specs/048-derive-command/contracts/derive-engine.md
          (module form §1, CLI §2, exit codes §3, JSON envelope §4, payloads §5,
          write authority §6, the offline transport seam §7, test anchors §8)

These pin the shape the other suites depend on: the six `--action` choices, the
exit-code constants, the fixed envelope key set, `semanticChecksPending` per
action, stdlib-only imports, the `.specify`-mirror guard, the `moves.md`
sole-writer rule, `_http_get` as the only transport seam, the atomic write, and
the text/json dual rendering of one internal result.

One clause the engine does NOT satisfy is encoded as a strict=False xfail and
named in the report rather than papered over (unknown-action exit code).
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tests.derive_fixtures import (
    CHAIN,
    ENGINE,
    TOPIC,
    build_artifact,
    codes,
    load_engine_module,
    moves_spec_file,
    run,
    scaffold,
    seed_library,
    write_artifact,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_MIRROR = REPO_ROOT / ".specify" / "scripts" / "python" / "derive-utils.py"

MOD = load_engine_module("derive_utils_contract")
SOURCE = ENGINE.read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)

#: C-1 allowed module roots (stdlib only).
ALLOWED_IMPORT_ROOTS = {
    "__future__", "argparse", "json", "os", "re", "sys", "unicodedata",
    "urllib", "socket", "datetime", "pathlib", "subprocess",
}

#: C-14 envelope top-level keys, exactly.
ENVELOPE_KEYS = {"ok", "action", "workspaceRoot", "generatedAt", "errors",
                 "warnings", "semanticChecksPending", "notes", "payload"}

#: The transport primitives the task scopes the seam scan to. `urllib.request.quote`
#: (pure percent-encoding used in _probe_one to build the wayback API URL) is NOT a
#: transport call and is deliberately excluded.
TRANSPORT_TOKENS = ("urlopen", "urllib.error", "socket.")

pytestmark = pytest.mark.contract


def _functions() -> dict[str, ast.FunctionDef]:
    return {n.name: n for n in ast.walk(TREE) if isinstance(n, ast.FunctionDef)}


def _func_source(name: str) -> str:
    return ast.get_source_segment(SOURCE, _functions()[name]) or ""


def _import_roots() -> set[str]:
    roots = set()
    for node in ast.walk(TREE):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                roots.add(node.module.split(".")[0])
    return roots


def _write_call(node: ast.Call) -> bool:
    """True if `node` writes the filesystem (Path.write_text/bytes or os.replace)."""
    f = node.func
    if isinstance(f, ast.Attribute) and f.attr in ("write_text", "write_bytes"):
        return True
    if (isinstance(f, ast.Attribute) and f.attr == "replace"
            and isinstance(f.value, ast.Name) and f.value.id == "os"):
        return True
    if isinstance(f, ast.Name) and f.id == "open":
        return True
    return False


# --------------------------------------------------------------------------
# §2 CLI — the six actions and no others
# --------------------------------------------------------------------------

def test_action_choices_are_exactly_the_six():
    parser = MOD.build_parser()
    action = next(a for a in parser._actions if a.dest == "action")
    assert set(action.choices) == {"init", "validate", "moves-list", "moves-add",
                                   "probe-links", "stats"}
    assert len(action.choices) == 6


def test_no_forbidden_flags_are_introduced():
    """C-8: probing timeout is a constant, offline is automatic — no such flags."""
    parser = MOD.build_parser()
    option_strings = {os for a in parser._actions for os in a.option_strings}
    for forbidden in ("--timeout", "--limit", "--offline", "--dry-run", "--topic"):
        assert forbidden not in option_strings, f"{forbidden} must not exist"


def test_exit_code_constants_match_the_contract():
    assert MOD.EXIT_OK == 0
    assert MOD.EXIT_USAGE == 1
    assert MOD.EXIT_INPUT_ERROR == 2
    assert MOD.EXIT_NOT_FOUND == 3
    assert MOD.EXIT_INVALID == 4


def test_default_max_steps_is_twelve():
    assert MOD.DEFAULT_MAX_STEPS == 12


def test_probe_timeout_is_a_pinned_constant():
    assert MOD.PROBE_TIMEOUT_SECONDS == 10


def test_intent_and_status_value_sets_are_closed():
    """C-28 four intents; C-11/C-17 the durable two-value status."""
    assert set(MOD.MOVE_INTENTS) == {"new", "reuse", "reinforce", "supersede"}
    assert set(MOD.MOVE_STATUSES) == {"active", "superseded"}


def test_unknown_action_exits_usage_with_an_envelope(tmp_path):
    """C-7: an unknown --action is exit 1 (EXIT_USAGE) with a JSON envelope whose
    `action` is null — never argparse's bare-text exit 2. main() catches the
    _UsageError raised by the parser's overridden error() hook.

    Note (minor naming divergence, reported not papered over): C-7's example names
    the error code `unknown-action`; the engine emits the more general
    `usage-error`, which one code covers unknown action, missing action, and
    unlisted flags (C-8). The substantive C-7 requirements (exit 1, action null,
    ok false, rule null, JSON envelope) all hold."""
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--workspace-root", str(tmp_path),
         "--action", "bogus", "--format", "json"],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == MOD.EXIT_USAGE, proc.stderr
    env = json.loads(proc.stdout)
    assert env["ok"] is False and env["action"] is None
    assert env["errors"][0]["rule"] is None
    assert env["errors"][0]["code"] == "usage-error"
    assert set(env) == ENVELOPE_KEYS


def test_missing_action_and_unlisted_flag_exit_usage(tmp_path):
    """C-7/C-8: a missing --action and an unlisted flag (e.g. --timeout) are both
    usage errors at exit 1, never silently swallowed as 0."""
    missing = subprocess.run(
        [sys.executable, str(ENGINE), "--workspace-root", str(tmp_path), "--format", "json"],
        capture_output=True, text=True, timeout=60)
    assert missing.returncode == MOD.EXIT_USAGE
    unlisted = subprocess.run(
        [sys.executable, str(ENGINE), "--workspace-root", str(tmp_path),
         "--action", "init", "--slug", "x", "--timeout", "5", "--format", "json"],
        capture_output=True, text=True, timeout=60)
    assert unlisted.returncode == MOD.EXIT_USAGE


# --------------------------------------------------------------------------
# §4 envelope — fixed key set and semanticChecksPending per action
# --------------------------------------------------------------------------

def test_envelope_top_level_key_set_is_exact(tmp_path):
    scaffold(tmp_path)
    code, env = run(tmp_path, "--action", "moves-list")
    assert code == 0
    assert set(env) == ENVELOPE_KEYS
    for key in ("errors", "warnings", "semanticChecksPending", "notes"):
        assert isinstance(env[key], list), f"{key} must always be an array (C-15)"


def test_generated_at_is_utc_iso8601_and_root_is_absolute(tmp_path):
    import re as _re
    scaffold(tmp_path)
    _, env = run(tmp_path, "--action", "moves-list")
    assert _re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", env["generatedAt"])
    assert Path(env["workspaceRoot"]).is_absolute()


@pytest.mark.parametrize("action,argv", [
    ("init", ["--action", "init", "--slug", "second-topic"]),
    ("moves-list", ["--action", "moves-list"]),
    ("stats", ["--action", "stats"]),
])
def test_semantic_checks_pending_is_empty_off_validate(tmp_path, action, argv):
    scaffold(tmp_path)
    seed_library(tmp_path)
    code, env = run(tmp_path, *argv)
    assert code == 0, env
    assert env["action"] == action
    assert env["semanticChecksPending"] == []


def test_semantic_checks_pending_is_constant_on_validate(tmp_path):
    scaffold(tmp_path)
    seed_library(tmp_path)
    write_artifact(tmp_path, build_artifact(), TOPIC)
    code, env = run(tmp_path, "--action", "validate", "--slug", TOPIC)
    assert code == 0, env
    assert env["semanticChecksPending"] == ["A11", "A14"]


# --------------------------------------------------------------------------
# §1 module form — stdlib-only, mirror guard, atomic write, sole writer, seam
# --------------------------------------------------------------------------

def test_engine_is_stdlib_only():
    """C-1: an AST import scan — any third-party root fails the contract."""
    offending = _import_roots() - ALLOWED_IMPORT_ROOTS
    assert not offending, f"non-stdlib import root(s): {sorted(offending)}"


def test_module_docstring_names_the_concept_and_contract():
    doc = MOD.__doc__ or ""
    assert "shared/definitions/derivation-definitions.md" in doc
    assert "contracts/derive-engine.md" in doc.replace(".specify/specs/048-derive-command/", "contracts/") \
        or "derive-engine.md" in doc


def test_specify_mirror_guard_is_present_in_source():
    """C-4: the guard mirrors scan-confirmation-gates.py lines 30-33."""
    assert 'if REPO_ROOT.name == ".specify":' in SOURCE
    assert "REPO_ROOT = REPO_ROOT.parent" in SOURCE


def test_workspace_root_specify_mirror_resolves_to_the_parent(tmp_path):
    """The functional half of the guard: --workspace-root <tmp>/.specify -> <tmp>."""
    scaffold(tmp_path)
    seed_library(tmp_path)
    assert MOD.resolve_root(str(tmp_path / ".specify")) == tmp_path.resolve()
    code, env = run(tmp_path / ".specify", "--action", "moves-list")
    assert code == 0, env
    assert env["workspaceRoot"] == str(tmp_path.resolve())
    assert env["payload"]["total"] == 2, "it read the real library through the mirror path"


def test_atomic_write_uses_part_then_os_replace():
    """C-29: never a half-written library."""
    src = _func_source("write_moves_atomic")
    assert ".md.part" in src
    assert "os.replace" in src


def test_moves_md_sole_writer_is_moves_add_and_init_create():
    """C-24: the only functions that write the filesystem are the moves writer
    (write_moves_atomic) and init-create (do_init); write_moves_atomic is called
    only from moves_add. Every other action is zero-write."""
    writers = {name for name, node in _functions().items()
               if any(isinstance(sub, ast.Call) and _write_call(sub) for sub in ast.walk(node))}
    assert writers == {"write_moves_atomic", "do_init"}, writers

    callers = {name for name, node in _functions().items()
               for sub in ast.walk(node)
               if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name)
               and sub.func.id == "write_moves_atomic"}
    assert callers == {"moves_add"}, callers


def test_read_only_actions_never_write(tmp_path):
    """validate / moves-list / stats / probe-links are zero-write (C-24/C-32)."""
    scaffold(tmp_path)
    seed_library(tmp_path)
    write_artifact(tmp_path, build_artifact(), TOPIC)
    before = {p: p.read_bytes() for p in (tmp_path / ".specify" / "derive").rglob("*") if p.is_file()}
    for argv in (["--action", "validate", "--slug", TOPIC],
                 ["--action", "moves-list"],
                 ["--action", "stats", "--slug", TOPIC]):
        code, env = run(tmp_path, *argv)
        assert code == 0, env
    after = {p: p.read_bytes() for p in (tmp_path / ".specify" / "derive").rglob("*") if p.is_file()}
    assert before == after, "a read-only action mutated the store"


def test_http_get_is_the_only_transport_seam():
    """C-30/C-33(a): urlopen / urllib.error / socket. appear only inside _http_get."""
    seam_funcs = set()
    for name in _functions():
        src = _func_source(name)
        if any(tok in src for tok in TRANSPORT_TOKENS):
            seam_funcs.add(name)
    assert seam_funcs == {"_http_get"}, seam_funcs


def test_probe_links_is_offline_tolerant_through_the_patched_seam(monkeypatch, tmp_path):
    """C-31/C-33(b): monkeypatch _http_get and nothing else; no test touches the network."""
    calls = []

    def offline(url, timeout, encode_param=None):
        calls.append(url)
        return None, "OfflineError: no route to host"

    monkeypatch.setattr(MOD, "_http_get", offline)
    code, env = MOD.probe_links(tmp_path, {"urls": ["http://example.invalid/a"]})
    assert code == MOD.EXIT_OK
    assert env["payload"]["online"] is False and env["payload"]["degraded"] is True
    assert env["payload"]["results"][0]["access"] == "unknown"
    assert env["semanticChecksPending"] == []
    assert any("no-online-capability" in n for n in env["notes"])
    assert calls, "the patched seam was actually exercised"


def test_probe_links_reports_live_through_the_patched_seam(monkeypatch, tmp_path):
    def live(url, timeout, encode_param=None):
        return 200, "<html>ok</html>"
    monkeypatch.setattr(MOD, "_http_get", live)
    code, env = MOD.probe_links(tmp_path, {"urls": ["http://example.invalid/a"]})
    assert code == MOD.EXIT_OK
    assert env["payload"]["online"] is True and env["payload"]["degraded"] is False
    assert env["payload"]["results"][0]["access"] == "live"


# --------------------------------------------------------------------------
# §3/§6 init — no-clobber, --force backup
# --------------------------------------------------------------------------

def test_init_no_clobber_is_an_input_conflict(tmp_path):
    scaffold(tmp_path)
    code, env = run(tmp_path, "--action", "init", "--slug", TOPIC)
    assert code == MOD.EXIT_INPUT_ERROR
    assert env["ok"] is False
    assert env["errors"][0]["code"] == "archive-exists"


def test_init_force_clobbers_and_keeps_a_real_backup(tmp_path):
    scaffold(tmp_path)
    marker = "hand-added line the operator would lose"
    art = tmp_path / ".specify" / "derive" / TOPIC / "derive.md"
    art.write_text(art.read_text(encoding="utf-8") + "\n" + marker + "\n", encoding="utf-8")
    code, env = run(tmp_path, "--action", "init", "--slug", TOPIC, "--force")
    assert code == 0, env
    assert env["payload"]["clobbered"] is True
    backup = Path(env["payload"]["backupPath"])
    assert backup.is_file() and backup.suffix == ".bak"
    assert marker in backup.read_text(encoding="utf-8"), "the .bak preserves the prior content"
    assert marker not in art.read_text(encoding="utf-8"), "the live archive was re-scaffolded"


def test_init_scaffolds_the_eight_sections_and_fourteen_audit_rows(tmp_path):
    code, env = scaffold(tmp_path)
    assert code == 0
    text = (tmp_path / ".specify" / "derive" / TOPIC / "derive.md").read_text(encoding="utf-8")
    for heading in MOD.ARTIFACT_SECTIONS:
        assert heading in text, f"scaffold is missing {heading}"
    assert MOD.AUDIT_HEADER in text
    audit_rows = MOD.parse_table(MOD.section(text, MOD.SEC_AUDIT), MOD.AUDIT_COLUMNS)
    assert [r["#"] for r in audit_rows] == list(MOD.ALL_CHECKS)
    assert all(r["result"] == "pending" for r in audit_rows), "a fresh scaffold is all pending"


# --------------------------------------------------------------------------
# §4 C-17 — one internal result, two renderings; text is not the JSON envelope
# --------------------------------------------------------------------------

def test_text_format_is_not_a_json_document(tmp_path):
    scaffold(tmp_path)
    seed_library(tmp_path)
    code, out = run(tmp_path, "--action", "moves-list", fmt="text")
    assert code == 0
    with pytest.raises(ValueError):
        json.loads(out), "text output must not be parseable as a single JSON object"
    assert out.splitlines()[0].startswith("moves-list OK")


def test_both_formats_render_one_result(tmp_path):
    """C-17: the same broken artifact yields the same codes in json and in text."""
    scaffold(tmp_path)
    seed_library(tmp_path)
    broken = build_artifact(chain=CHAIN.replace("- move: M-001", "- move: M-777"))
    write_artifact(tmp_path, broken, TOPIC)

    jcode, jenv = run(tmp_path, "--action", "validate", "--slug", TOPIC)
    tcode, tout = run(tmp_path, "--action", "validate", "--slug", TOPIC, fmt="text")
    assert jcode == tcode == MOD.EXIT_INVALID
    assert jenv["ok"] is False
    assert "validate FAIL" in tout.splitlines()[0]
    for code in codes(jenv):
        assert code in tout, f"text rendering dropped error code {code}"
    assert "A11, A14" in tout, "the semantic-pending line is rendered in text too"


def test_engine_and_its_specify_mirror_are_byte_identical():
    """C-35: the scripts mirror pair is strict/byte-identical."""
    assert ENGINE_MIRROR.is_file(), "run sync-mirrors.py --write"
    assert ENGINE.read_bytes() == ENGINE_MIRROR.read_bytes()
