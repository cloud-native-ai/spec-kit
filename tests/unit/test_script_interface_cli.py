"""Unit tests for ``scripts/python/script_interface_cli.py`` (Feature 086, T011).

Owns the module-level details a repository-wide contract test cannot isolate:

* the constants table is the ONE source both the emitted rule and the executed rule read —
  ``rule_table()`` carries exactly the eight keys C-21 fixes, and the eight keys are the
  whole payload (a ninth key is a drift, not an extension);
* ``--version`` prints exactly one line ``<script-name> <framework-version>``, exit 0, and
  the version is read from ``pyproject.toml`` at RUN TIME — editing a copy's version changes
  the line (C-8 / SC-011's mechanism);
* the version source is BOUNDED: the search stops at the enclosing repository root and never
  reads a foreign checkout's ``pyproject.toml`` (C-36's self-sufficiency rule). A directory
  holding a ``pyproject.toml`` but no ``.git`` is NOT a root — the measured failure mode R4
  records is a script copied into a subdirectory reporting the HOST checkout's version;
* an unreachable version source yields the literal ``unknown`` and still exits 0 (C-8: an
  observation, never a violation);
* the module carries no version-shaped literal of its own — the repository-wide scan's
  subject is every script body, this one included;
* ``VersionAction`` works on a parser with ``add_subparsers(required=True)`` when registered
  on the top parser AND every subparser, and ``preparse_version_guard`` serves the scripts
  whose parser reads ``sys.argv`` by hand; the guard stops at a bare ``--`` and rejects an
  unknown ``-*`` token with a non-zero exit (C-9).

Red-first (Constitution IV): the guard clause `test_module_exists` asserts the artifact path
before any behaviour, so a missing module is "artifact missing", not a collection error.

Fixtures are built in ``tmp_path``; nothing here writes inside the repository.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HELPER = REPO_ROOT / "scripts" / "python" / "script_interface_cli.py"

#: C-21 fixes eight keys; the set is closed. The three added by US6 (`exception_limbs`,
#: `forbidden_criteria`, `decided_by`) are not a second vocabulary beside those eight — they
#: PUBLISH the vocabularies the engine already executes (C-30's recomputation limbs, C-3's
#: three refused criteria, and the observation that decided a file), which is what lets the
#: owner page's own guard compare against the run instead of against prose.
RULE_KEYS = {
    "labels",
    "flag_forms",
    "separator",
    "version_line",
    "version_source",
    "exempt_basis",
    "findings",
    "exceptions",
    "exception_limbs",
    "forbidden_criteria",
    "decided_by",
    "observations",
}

#: C-21's original eight. They stay a closed set of their own: a key may be added to
#: `RULE_KEYS` deliberately, but none of the eight may disappear.
RULE_KEYS_C21 = (
    "labels",
    "flag_forms",
    "separator",
    "version_line",
    "version_source",
    "exempt_basis",
    "findings",
    "exceptions",
)

VERSION_LITERAL_RE = re.compile(r"""["']\d+\.\d+\.\d+["']""")


def _load_module():
    """Import the helper by path (it is not a package member)."""
    assert HELPER.is_file(), "artifact missing: %s" % HELPER
    spec = importlib.util.spec_from_file_location("script_interface_cli_under_test", HELPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(*args, cwd=None, env=None):
    return subprocess.run(
        [sys.executable, str(HELPER), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
        env=env,
    )


def _make_repo(root: Path, version: str = "9.9.9") -> Path:
    """A minimal repository root: pyproject.toml + .git + a scripts/python/ dir."""
    root.mkdir(parents=True, exist_ok=True)
    (root / ".git").mkdir(exist_ok=True)
    (root / "pyproject.toml").write_text(
        '[project]\nname = "probe"\nversion = "%s"\n' % version, encoding="utf-8"
    )
    (root / "scripts" / "python").mkdir(parents=True, exist_ok=True)
    return root


# ---------------------------------------------------------------------------------------
# Artifact guards (red-first: these fail before the module exists)
# ---------------------------------------------------------------------------------------


def test_module_exists():
    assert HELPER.is_file(), "artifact missing: %s" % HELPER
    assert HELPER.stat().st_size > 0


def test_module_has_no_third_party_import():
    """C-14's stdlib-only rule, applied to this module too.

    Docstrings and comments are stripped first: the consumer recipe in the module docstring
    spells `from script_interface_cli import …`, which is documentation, not an import.
    """
    source = HELPER.read_text(encoding="utf-8")
    import ast

    tree = ast.parse(source)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:  # a relative import has no top-level package name
                continue
            if node.module:
                names.add(node.module.split(".")[0])
    allowed = {"argparse", "sys", "pathlib", "typing", "json", "__future__", "os", "re"}
    assert names <= allowed, "unexpected import(s): %s" % sorted(names - allowed)


# ---------------------------------------------------------------------------------------
# The constants table (C-21)
# ---------------------------------------------------------------------------------------


def test_rule_table_has_exactly_the_named_closed_keys():
    module = _load_module()
    table = module.rule_table()
    assert set(table) == RULE_KEYS
    # C-21's eight are all still there: a key may be added on purpose, never dropped.
    missing = [key for key in RULE_KEYS_C21 if key not in table]
    assert not missing, f"C-21: the emitted rule lost {missing}"
    for key in ("labels", "flag_forms", "exempt_basis", "findings", "exceptions",
                "exception_limbs", "forbidden_criteria", "decided_by", "observations"):
        assert isinstance(table[key], list) and table[key], "%s must be a non-empty list" % key


def test_rule_table_matches_the_module_constants():
    """The table is a PROJECTION of the module constants, never a second list."""
    module = _load_module()
    table = module.rule_table()
    assert table["labels"] == list(module.LABELS)
    assert table["flag_forms"] == list(module.FLAG_FORMS)
    assert table["separator"] == module.SEPARATOR
    assert table["version_line"] == module.VERSION_LINE
    assert table["version_source"] == module.VERSION_SOURCE
    assert table["exempt_basis"] == list(module.EXEMPT_BASIS)
    assert table["findings"] == list(module.FINDINGS)
    assert table["exceptions"] == list(module.EXCEPTION_COLUMNS)
    assert table["exception_limbs"] == list(module.EXCEPTION_LIMBS)
    assert table["forbidden_criteria"] == list(module.FORBIDDEN_CRITERIA)
    assert table["decided_by"] == list(module.DECIDED_BY)
    assert table["observations"] == list(module.OBSERVATIONS)


def test_rule_table_is_json_serialisable_and_stable():
    module = _load_module()
    first = json.dumps(module.rule_table(), sort_keys=True)
    second = json.dumps(module.rule_table(), sort_keys=True)
    assert first == second


def test_emit_rule_cli_prints_the_table():
    result = _run("--emit-rule")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert set(payload) == RULE_KEYS


# ---------------------------------------------------------------------------------------
# The version text and its single source (C-8 / C-36)
# ---------------------------------------------------------------------------------------


def test_version_text_shape_is_name_and_version():
    module = _load_module()
    line = module.version_text("some-script.py", REPO_ROOT / "scripts" / "python")
    assert re.fullmatch(r"some-script\.py \S+", line), line
    assert "\n" not in line


def test_version_is_read_at_run_time_not_baked_in(tmp_path):
    root = _make_repo(tmp_path / "repo", version="1.2.3")
    sys.path.insert(0, str(root / "scripts" / "python"))
    try:
        module = _load_module()
        assert module.version_text("probe.py", root / "scripts" / "python") == "probe.py 1.2.3"
        (root / "pyproject.toml").write_text(
            '[project]\nname = "probe"\nversion = "4.5.6"\n', encoding="utf-8"
        )
        assert module.version_text("probe.py", root / "scripts" / "python") == "probe.py 4.5.6"
    finally:
        sys.path.remove(str(root / "scripts" / "python"))


def test_unknown_version_when_no_pyproject_is_reachable(tmp_path):
    module = _load_module()
    lonely = tmp_path / "no-repo" / "scripts"
    lonely.mkdir(parents=True)
    assert module.version_text("probe.py", lonely) == "probe.py unknown"


def test_pyproject_without_git_is_not_a_repository_root(tmp_path):
    """R4's measured failure mode: a stray pyproject.toml must not be read as the root."""
    module = _load_module()
    decoy = tmp_path / "decoy"
    decoy.mkdir()
    (decoy / "pyproject.toml").write_text('[project]\nversion = "6.6.6"\n', encoding="utf-8")
    nested = decoy / "leaf"
    nested.mkdir()
    assert module.find_repo_root(nested) is None
    assert module.version_text("probe.py", nested) == "probe.py unknown"


def test_search_is_bounded_and_stops_at_the_nearest_root(tmp_path):
    module = _load_module()
    outer = _make_repo(tmp_path / "outer", version="1.1.1")
    inner = outer / "vendor" / "inner"
    inner.mkdir(parents=True)
    (inner / ".git").mkdir()
    (inner / "pyproject.toml").write_text('[project]\nversion = "2.2.2"\n', encoding="utf-8")
    assert module.find_repo_root(inner) == inner
    assert module.version_text("probe.py", inner) == "probe.py 2.2.2"


def test_version_field_is_read_from_the_project_table_only(tmp_path):
    module = _load_module()
    root = _make_repo(tmp_path / "repo", version="3.3.3")
    (root / "pyproject.toml").write_text(
        '[tool.something]\nversion = "0.0.1"\n[project]\nname = "probe"\nversion = "3.3.3"\n',
        encoding="utf-8",
    )
    assert module.resolve_version(root) == "3.3.3"


def test_unreadable_pyproject_degrades_to_unknown(tmp_path):
    module = _load_module()
    root = _make_repo(tmp_path / "repo", version="1.0.0")
    (root / "pyproject.toml").write_bytes(b"\xff\xfe not utf-8")
    assert module.resolve_version(root) == "unknown"


def test_cli_version_prints_one_line_and_exits_zero():
    result = _run("--version")
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert len(lines) == 1, lines
    assert re.fullmatch(r"script_interface_cli\.py \S+", lines[0]), lines


def test_cli_version_tracks_a_copy_tree_pyproject(tmp_path):
    """SC-011's mechanism at unit scale: the same script, a different version file."""
    root = _make_repo(tmp_path / "copy", version="7.7.7")
    target = root / "scripts" / "python" / "probe.py"
    target.write_text(HELPER.read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run([sys.executable, str(target), "--version"],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "probe.py 7.7.7"


def test_module_carries_no_version_literal():
    """C-8's scan subject: no version-shaped literal inside a script body."""
    text = HELPER.read_text(encoding="utf-8")
    assert not VERSION_LITERAL_RE.findall(text)


# ---------------------------------------------------------------------------------------
# The argparse surface and the pre-parse guard (C-8 / C-9)
# ---------------------------------------------------------------------------------------


def test_version_action_survives_required_subparsers(tmp_path):
    """The measured trap: a required-subparsers parser rejects a leading --version."""
    script = tmp_path / "subcmd.py"
    script.write_text(textwrap.dedent(
        """
        import sys
        sys.path.insert(0, %r)
        import argparse
        from script_interface_cli import VersionAction, add_version_argument

        def build():
            parser = argparse.ArgumentParser(prog="subcmd.py")
            add_version_argument(parser)
            subs = parser.add_subparsers(dest="action", required=True)
            for name in ("alpha", "beta"):
                sub = subs.add_parser(name)
                add_version_argument(sub)
                sub.add_argument("--write", action="store_true")
            return parser

        sys.exit(build().parse_args() and 0 or 0)
        """
    ) % str(REPO_ROOT / "scripts" / "python"), encoding="utf-8")
    result = subprocess.run([sys.executable, str(script), "--version"],
                            capture_output=True, text=True)
    # `unknown` is acceptable here (tmp dir is not a repository); exit 0 is not.
    assert result.returncode == 0, (result.returncode, result.stderr, result.stdout)
    assert result.stdout.strip().startswith("subcmd.py "), result.stdout


def test_version_action_register_forms():
    """The class form and `VersionAction.attach` register; an INSTANCE cannot (argparse
    re-instantiates whatever it receives by calling it with its own kwargs)."""
    module = _load_module()
    import argparse

    parser = argparse.ArgumentParser(prog="probe.py")
    parser.add_argument("--version", action=module.VersionAction)
    hits = [a for a in parser._actions if isinstance(a, module.VersionAction)]
    assert len(hits) == 1

    other = argparse.ArgumentParser(prog="probe.py")
    module.VersionAction.attach(other)
    assert len([a for a in other._actions if isinstance(a, module.VersionAction)]) == 1

    broken = argparse.ArgumentParser(prog="probe.py")
    with pytest.raises(TypeError):
        broken.add_argument("--version", action=module.VersionAction())


def test_add_version_argument_is_idempotent():
    module = _load_module()
    import argparse
    parser = argparse.ArgumentParser(prog="probe.py")
    module.add_version_argument(parser)
    module.add_version_argument(parser)
    hits = [a for a in parser._actions if isinstance(a, module.VersionAction)]
    assert len(hits) == 1


def test_preparse_guard_answers_version_before_any_parser(tmp_path):
    module = _load_module()
    with pytest.raises(SystemExit) as excinfo:
        module.preparse_version_guard(["--version"], script_name="hand-rolled.py")
    assert excinfo.value.code == 0


def test_preparse_guard_rejects_unknown_option_nonzero():
    module = _load_module()
    with pytest.raises(SystemExit) as excinfo:
        module.preparse_version_guard(["--no-such-flag"], script_name="hand-rolled.py")
    assert excinfo.value.code != 0


def test_preparse_guard_does_not_rescue_unknown_after_a_known_option():
    """No order rescues an undeclared token — `--version` included (C-9).

    The guard used to answer `--version` as soon as it met it, so `--version --bogus` exited 0
    and printed the version while silently dropping a token nobody declared: exactly the
    "recognized option lets the unknown one through" shape C-9 forbids. The scan now reads every
    token before the bare `--` first, and only a wholly legal line is answered.
    """
    module = _load_module()
    for argv in (["--version", "--bogus"], ["--bogus", "--version"], ["-x", "--version"]):
        with pytest.raises(SystemExit) as excinfo:
            module.preparse_version_guard(argv, script_name="hand-rolled.py")
        assert excinfo.value.code != 0, argv
        assert excinfo.value.code == 2, argv
    # The legal line on its own is still answered.
    with pytest.raises(SystemExit) as excinfo3:
        module.preparse_version_guard(["--version"], script_name="hand-rolled.py")
    assert excinfo3.value.code == 0


def test_preparse_guard_stops_at_a_bare_separator(tmp_path):
    module = _load_module()
    # Everything after a bare `--` is positional by convention: never an unknown option.
    module.preparse_version_guard(["--", "--no-such-flag"],
                                  script_name="hand-rolled.py")  # no raise
    module.preparse_version_guard(["--", "--version"],
                                  script_name="hand-rolled.py")  # no raise, no print


def test_cli_rejects_an_unknown_option_at_exit_two():
    result = _run("--no-such-flag")
    assert result.returncode == 2, (result.returncode, result.stderr)


def test_preparse_guard_accepts_a_declared_option(tmp_path):
    """A declared token is legal — the guard judges the vocabulary, not the spelling (C-9)."""
    module = _load_module()
    module.preparse_version_guard(["--stdin"], declared=["--stdin"],
                                  script_name="hand-rolled.py")  # no raise
    with pytest.raises(SystemExit) as excinfo:
        module.preparse_version_guard(["--stdin", "--bogus"], declared=["--stdin"],
                                      script_name="hand-rolled.py")
    assert excinfo.value.code == 2


# --------------------------------------------------------------------------------------
# configure_parser / fill_help_labels: C-7's four labels, owed by every help body
# --------------------------------------------------------------------------------------


def test_configure_parser_adds_the_two_label_lines_to_an_argparse_help(capsys):
    module = _load_module()
    import argparse

    parser = argparse.ArgumentParser(prog="probe.py", description="a probe")
    parser.add_argument("--thing", help="a thing")
    module.configure_parser(parser)
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_args(["--help"])
    assert excinfo.value.code == 0
    body = capsys.readouterr().out
    lines = [line.strip() for line in body.splitlines()]
    assert any(line.startswith("usage:") for line in lines), body
    assert any(line.startswith("options:") for line in lines), body
    assert any(line.startswith("side-effects:") for line in lines), body
    assert any(line.startswith("exit-codes:") for line in lines), body


def test_configure_parser_keeps_the_scripts_own_label_text():
    """An override is the script's own statement and MUST NOT be replaced by the default."""
    module = _load_module()
    import argparse

    parser = argparse.ArgumentParser(prog="probe.py")
    module.configure_parser(parser, effects="writes out.txt", codes="0 done; 3 nope")
    assert "side-effects: writes out.txt" in parser.epilog
    assert "exit-codes: 0 done; 3 nope" in parser.epilog


def test_configure_parser_defaults_are_the_honest_generic_ones():
    module = _load_module()
    import argparse

    labels = module.help_labels()
    assert "side-effects: " in labels
    assert "exit-codes: " in labels
    assert labels.count("side-effects:") == 1 and labels.count("exit-codes:") == 1


def test_fill_help_labels_is_idempotent_and_keeps_an_existing_label():
    module = _load_module()
    once = module.fill_help_labels("usage: x\n  --a\nside-effects: none")
    twice = module.fill_help_labels(once)
    assert once == twice
    assert once.count("side-effects:") == 1
    assert once.count("exit-codes:") == 1


def test_fill_help_labels_leaves_an_empty_body_empty():
    module = _load_module()
    assert module.fill_help_labels("") == ""
    assert module.fill_help_labels("   \n") == ""
