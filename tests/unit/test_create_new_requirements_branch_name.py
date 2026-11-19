"""Branch-name generation: Unicode preservation, portable acronym probing, byte limits.

Ported fix families (upstream github/spec-kit):
  * acf43471b — preserve Unicode feature names instead of stripping every non-ASCII
    character, which left a Chinese description with a degenerate "NNN-" suffix;
    measure GitHub's 244 limit in BYTES, not characters.
  * 4038d370b — bash 3.2 portability: ``tr`` uppercase pipeline instead of ``${word^^}``,
    ``grep -qw`` instead of the ``\\b`` word boundary BSD grep reads as a backspace.
  * 18ea13fdc — ``sed 's/--*/-/g'`` instead of the GNU-only ``\\+``, and LC_ALL=C so
    ``[^a-z0-9]`` is a byte range rather than a collation range.
  * 8629796da — warn when the suffix is empty and point at --short-name.

Adapted-by: hand adaptation onto this fork's create-new-requirements.sh, which keeps
its own key names (REQUIREMENTS_DIR / requirements.md) and its own numbering sources.
"""
from __future__ import annotations

import pytest

from tests.unit.requirements_scaffold import (
    byte_len,
    branch_name,
    make_project,
    run_script,
    spec_dirs,
    suffix,
)


def test_ascii_description_still_filters_stop_words(tmp_path):
    """The ASCII fast path must stay byte-identical to the pre-port behaviour."""
    proj = make_project(tmp_path)
    proc = run_script(proj, "Add user authentication system")
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == "user-authentication-system"


@pytest.mark.parametrize(
    ("description", "expected"),
    [
        # A two-character word survives only when it appears uppercase in the original.
        ("Fix GO sync", "fix-go-sync"),
        ("Fix DB sync", "fix-db-sync"),
        # Mixed case is not an uppercase acronym, so the short word is dropped.
        ("Fix eD sync", "fix-sync"),
        # Four characters need no acronym probe at all.
        ("Fix eDBe sync", "fix-edbe-sync"),
    ],
)
def test_short_acronym_probe_is_portable_and_case_exact(tmp_path, description, expected):
    """4038d370b + 18ea13fdc: the probe uses tr + grep -qw under LC_ALL=C.

    ``${word^^}`` is a bash 4 "bad substitution" on macOS bash 3.2, and ``\\b`` is a
    backspace to BSD grep, so both defects silently dropped uppercase acronyms.
    """
    proj = make_project(tmp_path)
    proc = run_script(proj, description)
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == expected


@pytest.mark.parametrize(
    ("description", "expected"),
    [
        ("添加用户认证系统", "添加用户认证系统"),
        # One- and two-character CJK words are meaningful, not noise.
        ("用户 认证 系统", "用户-认证-系统"),
        ("混合 English 描述", "混合-english-描述"),
    ],
)
def test_unicode_description_is_preserved(tmp_path, description, expected):
    """acf43471b: non-ASCII letters and digits survive; short non-ASCII words are kept."""
    proj = make_project(tmp_path)
    proc = run_script(proj, description)
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == expected
    assert spec_dirs(proj) == [branch_name(proc.stdout)]


@pytest.mark.parametrize(
    ("description", "expected"),
    [
        # Expectations pinned from upstream's own final parity suite
        # (tests/test_create_new_feature_python_parity.py, "Fix éDBé sync" family).
        ("Fix éDBé sync", "fix-édbé-sync"),
        ("É DB sync", "É-db-sync"),
        ("é DB sync", "é-db-sync"),
    ],
)
def test_accented_parity_matches_upstream_expectations(tmp_path, description, expected):
    """Lowercasing is ASCII-only, so an accented capital keeps its case (upstream parity)."""
    proj = make_project(tmp_path)
    proc = run_script(proj, description)
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == expected


def test_unicode_short_name_is_cleaned_not_stripped(tmp_path):
    proj = make_project(tmp_path)
    proc = run_script(proj, "添加认证", "--short-name", "用户认证V2")
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == "用户认证v2"


def test_repeated_separators_collapse_on_a_unicode_short_name(tmp_path):
    """18ea13fdc: ``--*`` collapses runs of separators where GNU-only ``\\+`` did not."""
    proj = make_project(tmp_path)
    proc = run_script(proj, "Add auth", "--short-name", "用户--认证__系统")
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == "用户-认证-系统"


def test_ascii_short_name_collapses_repeated_separators(tmp_path):
    proj = make_project(tmp_path)
    proc = run_script(proj, "Add auth", "--short-name", "user---auth__system")
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == "user-auth-system"


def test_punctuation_only_description_warns_about_the_empty_suffix(tmp_path):
    """8629796da: an empty suffix is warned about, and --short-name is named as the remedy."""
    proj = make_project(tmp_path)
    proc = run_script(proj, "!!! ???")
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == ""
    assert "Feature name is empty" in proc.stderr
    assert "--short-name" in proc.stderr


def test_long_unicode_branch_is_truncated_by_bytes_not_characters(tmp_path):
    """acf43471b: GitHub's limit is 244 BYTES. A CJK suffix is 3 bytes per character, so
    a character-count truncation would overshoot the limit by up to 3x."""
    proj = make_project(tmp_path)
    proc = run_script(proj, "认证系统模块" * 40)
    assert proc.returncode == 0, proc.stderr
    name = branch_name(proc.stdout)
    assert byte_len(name) <= 244, f"{byte_len(name)} bytes: {name}"
    assert "244-byte limit" in proc.stderr
    # The reported figures are real byte counts, and the cut never splits a character.
    assert f"({byte_len(name)} bytes)" in proc.stderr
    name.encode("utf-8").decode("utf-8")
    assert not name.endswith("-")


def test_long_ascii_branch_truncation_keeps_the_244_byte_contract(tmp_path):
    """A long --short-name is not word-capped, so it reaches the truncation path.

    (A long *description* does not: generate_branch_name keeps at most 3-4 words.)
    """
    proj = make_project(tmp_path)
    proc = run_script(proj, "Add auth", "--short-name", "-".join(["authentication"] * 40))
    assert proc.returncode == 0, proc.stderr
    name = branch_name(proc.stdout)
    assert byte_len(name) <= 244
    assert "244-byte limit" in proc.stderr
    assert f"({byte_len(name)} bytes)" in proc.stderr
    assert not name.endswith("-")


def test_short_branch_is_not_truncated_and_does_not_warn(tmp_path):
    proj = make_project(tmp_path)
    proc = run_script(proj, "Add user authentication system")
    assert proc.returncode == 0, proc.stderr
    assert "244-byte limit" not in proc.stderr
    assert branch_name(proc.stdout) == "001-user-authentication-system"