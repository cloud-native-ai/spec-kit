"""bash 3.2 portability and locale behaviour of create-new-requirements.sh.

Ported fix families (upstream github/spec-kit):
  * 4038d370b — no bash 4-only construct (``${var^^}`` is a "bad substitution" on the
    bash 3.2 that macOS ships as /bin/bash) and no ``\\b`` word boundary, which BSD grep
    reads as a backspace so the acronym probe silently failed.
  * 18ea13fdc — no GNU-only ``sed 's/-\\+/-/g'``; POSIX/BSD sed reads ``\\+`` as a literal
    plus and leaves repeated separators uncollapsed. The same defect class in the
    numbering probe (``grep -o '^[0-9]\\+'``) is ported to upstream's ERE form
    ``grep -Eo '^[0-9]+'``. LC_ALL=C keeps ``[^a-z0-9]`` a byte range instead of a
    collation range that would let accented lowercase letters survive.
  * acf43471b — an explicit caller LC_ALL is respected, not silently rewritten; a Unicode
    name under an unusable locale is a clear error, not a degenerate "NNN-" suffix.
  * 5eb3d1478 + 3be2bd9b4 — user-controlled text goes through printf, never echo.

The static scan is paired with a self-test on synthetic samples: a scanner that cannot
go red when the defect is present proves nothing.
"""
from __future__ import annotations

import json
import re
import subprocess

import pytest

from tests.unit.requirements_scaffold import (
    ROOT,
    SCRIPT_PATH,
    SCRIPT_REL,
    make_project,
    minimal_env,
    run_script,
    suffix,
)

# (pattern, reason). Applied to code only: full-line comments are skipped and a trailing
# comment is cut at the first '#'. No '#' appears inside a string literal in this script,
# so that cut cannot hide a defect from the scan.
BASH32_PATTERNS = [
    (r"\$\{[A-Za-z_][A-Za-z0-9_]*\^\^", "bash4 uppercase expansion ${var^^}"),
    (r"\$\{[A-Za-z_][A-Za-z0-9_]*,,", "bash4 lowercase expansion ${var,,}"),
    (r"\bmapfile\b", "bash4 mapfile"),
    (r"\breadarray\b", "bash4 readarray"),
    (r"\bdeclare -A", "bash4 associative array"),
    (r"\blocal -A", "bash4 associative array"),
    (r"\|\&", "bash4 |& pipe"),
    (r"&>>", "bash4 &>> redirect"),
    (r"grep[^\n]*\\b", "non-POSIX grep \\b word boundary"),
    (r"grep[^\n]*\\\+", "GNU-only grep BRE \\+ (POSIX/BSD needs ERE +)"),
    (r"sed[^\n]*'s/-\\\+/", "GNU-only sed \\+ separator collapse"),
]

ECHO_HAZARDS = [
    'echo "$FEATURE_DESCRIPTION"',
    'echo "$SHORT_NAME"',
    'echo "$description"',
    'echo "$word"',
]


def _findings(text: str) -> list[str]:
    out = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        code = line.split("#", 1)[0]
        for pattern, reason in BASH32_PATTERNS:
            if re.search(pattern, code):
                out.append(f"{lineno}: {reason}")
        for hazard in ECHO_HAZARDS:
            if hazard in code:
                out.append(f"{lineno}: echo on user-controlled text ({hazard})")
    return out


def test_script_has_no_bash4_only_or_non_posix_construct():
    findings = _findings(SCRIPT_PATH.read_text(encoding="utf-8"))
    assert findings == [], "\n".join(findings)


@pytest.mark.parametrize(
    "sample",
    [
        'elif echo "$description" | grep -q "\\b${word^^}\\b"; then',
        "mapfile -t lines < file",
        "readarray -t lines < file",
        "declare -A map",
        "cmd |& tee log",
        "cmd &>> log",
        """echo "$name" | sed 's/-\\+/-/g'""",
        """number=$(echo "$name" | grep -o '^[0-9]\\+' || echo 0)""",
        'echo "$FEATURE_DESCRIPTION" > "$SPEC_FILE"',
        'BRANCH_SUFFIX=$(echo "$SHORT_NAME" | tr "[:upper:]" "[:lower:]")',
    ],
)
def test_the_scan_goes_red_when_a_defect_is_present(sample):
    """Self-test: every pattern the port removed must still be detected."""
    assert _findings(sample), f"scanner missed: {sample}"


def test_comments_are_not_scanned_as_code():
    """The port documents the removed constructs in comments; those must not trip it."""
    assert _findings("# bash 4+ ${word^^} and grep \\b are gone\n") == []


@pytest.mark.parametrize("locale", ["C", "en_US.UTF-8"])
def test_ascii_result_is_identical_across_locales(tmp_path, locale):
    """18ea13fdc: collation must not change an ASCII branch name."""
    proj = make_project(tmp_path)
    proc = run_script(proj, "Add user authentication system", env={"LC_ALL": locale})
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == "user-authentication-system"


def test_acronym_probe_works_under_the_c_locale(tmp_path):
    proj = make_project(tmp_path)
    proc = run_script(proj, "Fix DB sync", env={"LC_ALL": "C"})
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == "fix-db-sync"


def test_explicit_c_locale_with_a_unicode_name_is_a_clear_error(tmp_path):
    """acf43471b: respect the pin, and refuse rather than emit a degenerate suffix."""
    proj = make_project(tmp_path)
    proc = run_script(proj, "添加用户认证系统", env={"LC_ALL": "C"})
    assert proc.returncode == 1
    assert "UTF-8 locale is required" in proc.stderr
    assert "LC_ALL=C is not usable" in proc.stderr


def test_explicit_c_locale_is_not_silently_rewritten_for_ascii(tmp_path):
    """The caller's pin survives: an ASCII name still succeeds under C.

    "add" is a stop word, so the suffix is "auth" — the same answer a UTF-8 run gives.
    """
    proj = make_project(tmp_path)
    proc = run_script(proj, "Add auth", env={"LC_ALL": "C"})
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == "auth"


def test_unicode_name_under_an_explicit_utf8_locale(tmp_path):
    proj = make_project(tmp_path)
    proc = run_script(proj, "添加用户认证系统", env={"LC_ALL": "en_US.UTF-8"})
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == "添加用户认证系统"


def _run_clean_env(proj, args, env):
    """A true ``env -i`` run: only the variables the script genuinely needs."""
    return subprocess.run(
        ["/bin/bash", SCRIPT_REL, *args],
        cwd=proj, capture_output=True, encoding="utf-8", timeout=120, input="", env=env,
    )


def test_bare_environment_c_locale_ascii(tmp_path):
    proj = make_project(tmp_path)
    proc = _run_clean_env(proj, ["Add user authentication system"],
                          minimal_env(LC_ALL="C"))
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == "user-authentication-system"


def test_bare_environment_without_locale_selects_utf8_for_unicode(tmp_path):
    proj = make_project(tmp_path)
    proc = _run_clean_env(proj, ["添加用户认证系统"], minimal_env())
    assert proc.returncode == 0, proc.stderr
    assert suffix(proc.stdout) == "添加用户认证系统"


def test_bare_environment_c_locale_json_still_parses(tmp_path):
    proj = make_project(tmp_path)
    proc = _run_clean_env(proj, ["--json", "Add user authentication system"],
                          minimal_env(LC_ALL="C"))
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["BRANCH_NAME"] == "001-user-authentication-system"


def test_help_and_version_answer_without_writing(tmp_path):
    """The script-interface contract is untouched by the port."""
    proj = make_project(tmp_path)
    for flag in ("--help", "-h", "--version"):
        proc = run_script(proj, flag)
        assert proc.returncode == 0, f"{flag}: {proc.stderr}"
        assert (proj / ".specify" / "specs").is_dir()
        assert list((proj / ".specify" / "specs").iterdir()) == []


def test_undeclared_option_is_rejected(tmp_path):
    proj = make_project(tmp_path)
    proc = run_script(proj, "--not-a-flag")
    assert proc.returncode == 2
    assert list((proj / ".specify" / "specs").iterdir()) == []


def test_mirror_copy_is_identical_to_the_source():
    """The framework source and its client-runtime projection must not drift."""
    mirror = ROOT / ".specify" / "scripts" / "bash" / "create-new-requirements.sh"
    if not mirror.is_file():
        pytest.skip("no client-runtime mirror installed in this tree")
    assert mirror.read_bytes() == SCRIPT_PATH.read_bytes()