"""Feature-description handling: whitespace validation and option-like text.

Ported fix families (upstream github/spec-kit):
  * 6757c90db — a description of only whitespace is rejected, not scaffolded.
  * 5eb3d1478 + 3be2bd9b4 — ``printf`` instead of ``echo`` so a description beginning
    with "-n"/"-e"/"-E" is text rather than an option, both when deriving the branch
    name and when writing requirements.md.

Adaptation note: upstream trims with a per-line ``sed``. This fork combines argv and
stdin into one possibly multi-line description, so the emptiness test here is
non-mutating — interior Markdown indentation must survive into requirements.md.
"""
from __future__ import annotations

import pytest

from tests.unit.requirements_scaffold import (
    make_project,
    run_script,
    spec_dirs,
    spec_file,
)


@pytest.mark.parametrize("blank", ["   ", "\t", "\n", " \t\n "])
def test_whitespace_only_description_is_rejected(tmp_path, blank):
    """6757c90db: ASCII whitespace only, matching upstream's own scope.

    Boundary kept deliberately: ``tr``/``sed`` character classes are byte-wise, so a
    multi-byte space such as U+3000 IDEOGRAPHIC SPACE is not recognised here — exactly
    as in upstream. Such a description still raises the empty-suffix warning
    (8629796da), so it is not silent. Widening this to Unicode whitespace would be new
    behaviour, not a port.
    """
    proj = make_project(tmp_path)
    proc = run_script(proj, blank)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "only whitespace" in proc.stderr
    assert spec_dirs(proj) == []


def test_multibyte_space_only_description_warns_rather_than_passing_silently(tmp_path):
    """Documents the byte-wise boundary above: the empty-suffix warning is the signal."""
    proj = make_project(tmp_path)
    proc = run_script(proj, "\u3000")
    assert "Feature name is empty" in proc.stderr
    assert "--short-name" in proc.stderr


def test_whitespace_only_stdin_is_rejected(tmp_path):
    proj = make_project(tmp_path)
    proc = run_script(proj, stdin="  \n\t\n")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "only whitespace" in proc.stderr
    assert spec_dirs(proj) == []


def test_missing_description_still_reports_usage(tmp_path):
    """The pre-existing empty-description contract is unchanged."""
    proj = make_project(tmp_path)
    proc = run_script(proj)
    assert proc.returncode == 1
    assert "Usage:" in proc.stderr
    assert spec_dirs(proj) == []


@pytest.mark.parametrize("option_like", ["-n", "-e", "-E"])
def test_option_like_description_from_stdin_is_written_as_text(tmp_path, option_like):
    """5eb3d1478: ``echo "-n"`` emits nothing, so the spec file used to come out empty."""
    proj = make_project(tmp_path)
    proc = run_script(proj, stdin=option_like)
    assert proc.returncode == 0, proc.stderr
    path = spec_file(proc.stdout)
    assert path, proc.stdout
    with open(path, encoding="utf-8") as handle:
        assert handle.read() == option_like + "\n"


@pytest.mark.parametrize("option_like", ["-n", "-e", "-E"])
def test_option_like_description_after_separator_is_written_as_text(tmp_path, option_like):
    """3be2bd9b4: after ``--`` the token is an operand, and stays text all the way down."""
    proj = make_project(tmp_path)
    proc = run_script(proj, "--", option_like)
    assert proc.returncode == 0, proc.stderr
    with open(spec_file(proc.stdout), encoding="utf-8") as handle:
        assert handle.read() == option_like + "\n"


def test_option_like_token_without_separator_is_still_rejected_by_the_guard(tmp_path):
    """The script-interface contract is not relaxed by the printf port: an undeclared
    leading option is still exit 2, so the text path is reached via stdin or ``--``."""
    proj = make_project(tmp_path)
    proc = run_script(proj, "-n")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert spec_dirs(proj) == []


def test_multiline_description_keeps_interior_indentation(tmp_path):
    """The non-mutating emptiness test must not strip every line's leading whitespace."""
    proj = make_project(tmp_path)
    proc = run_script(proj, stdin="Add auth\n    indented line\n\ttabbed line\n")
    assert proc.returncode == 0, proc.stderr
    with open(spec_file(proc.stdout), encoding="utf-8") as handle:
        content = handle.read()
    assert "    indented line" in content
    assert "\ttabbed line" in content


def test_description_with_quotes_and_backslashes_survives_into_the_spec(tmp_path):
    proj = make_project(tmp_path)
    text = 'Price is $100 with "quotes" and a \\ backslash'
    proc = run_script(proj, stdin=text)
    assert proc.returncode == 0, proc.stderr
    with open(spec_file(proc.stdout), encoding="utf-8") as handle:
        assert text in handle.read()


def test_template_substitution_works_when_the_repo_path_contains_a_quote(tmp_path):
    """The template path travels through the environment, not interpolated Python source."""
    base = tmp_path / 'q"dir'
    base.mkdir()
    proj = make_project(base)
    templates = proj / ".specify" / "templates"
    templates.mkdir(parents=True)
    (templates / "requirements-template.md").write_text(
        "# Requirements\n\n$ARGUMENTS\n", encoding="utf-8"
    )
    proc = run_script(proj, "Add user authentication")
    assert proc.returncode == 0, proc.stderr
    with open(spec_file(proc.stdout), encoding="utf-8") as handle:
        content = handle.read()
    assert "Add user authentication" in content
    assert "$ARGUMENTS" not in content


def test_rerunning_preserves_the_earlier_spec_and_allocates_a_new_number(tmp_path):
    """The reachable guarantee around the touched write block.

    Numbering takes the global maximum over spec dirs, archives and branch names, so a
    re-run always targets a NEW directory — the no-clobber guard itself is defensive and
    cannot be staged deterministically. What a user actually relies on is that the
    earlier specification is never rewritten, which is what this asserts.
    """
    proj = make_project(tmp_path)
    first = run_script(proj, "Add user authentication system")
    assert first.returncode == 0, first.stderr
    first_path = spec_file(first.stdout)
    with open(first_path, "w", encoding="utf-8") as handle:
        handle.write("hand written specification\n")

    second = run_script(proj, "Add user authentication system")
    assert second.returncode == 0, second.stderr
    second_path = spec_file(second.stdout)
    assert second_path != first_path
    assert spec_dirs(proj) == [
        "001-user-authentication-system",
        "002-user-authentication-system",
    ]
    with open(first_path, encoding="utf-8") as handle:
        assert handle.read() == "hand written specification\n"