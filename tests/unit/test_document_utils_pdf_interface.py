"""Entry-layer contract of the document-utils pdf scripts (original MIT rewrite).

The eight scripts are operand-only: they declare no options of their own, and
the framework's generated signature block answers -h / --help / --version and
refuses an undeclared option before any parsing or write. Two of those properties
are load-bearing for this family and are pinned here:

  * the entry layer answers even when the optional third-party libraries are
    absent -- the registered script create_validation_image.py carries a
    declared exception on that basis, so its imports must stay inside functions;
  * a flag-only invocation writes nothing anywhere.

The version line is compared against an independent read of pyproject.toml, not
against the helper the scripts themselves use, so a drifting bridge is caught.
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "skills" / "external" / "document-utils" / "scripts" / "pdf"
REGISTERED = "create_validation_image.py"

NAMES = [
    "check_bounding_boxes.py",
    "check_fillable_fields.py",
    "convert_pdf_to_images.py",
    "create_validation_image.py",
    "extract_form_field_info.py",
    "extract_form_structure.py",
    "fill_fillable_fields.py",
    "fill_pdf_form_with_annotations.py",
]

#: Operands each script needs; a wrong count is the usage-error probe.
WRONG_OPERANDS = {
    "check_bounding_boxes.py": [],
    "check_fillable_fields.py": [],
    "convert_pdf_to_images.py": ["only-one.pdf"],
    "create_validation_image.py": ["1", "fields.json"],
    "extract_form_field_info.py": ["only-one.pdf"],
    "extract_form_structure.py": [],
    "fill_fillable_fields.py": ["a.pdf", "b.json"],
    "fill_pdf_form_with_annotations.py": ["a.pdf"],
}


def _framework_version() -> str:
    """Read [project] version straight from pyproject.toml, independently."""
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    in_project = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("[") and line.endswith("]"):
            in_project = line == "[project]"
            continue
        if in_project and line.startswith("version"):
            key, sep, value = line.partition("=")
            if sep and key.strip() == "version":
                return value.strip().strip("\"'")
    raise AssertionError("no [project] version in pyproject.toml")


def _run(script: str, args: list, cwd: Path, *, no_site: bool = False):
    command = [sys.executable]
    if no_site:
        command.append("-S")
    command.append(str(SCRIPTS / script))
    command.extend(args)
    return subprocess.run(command, cwd=str(cwd), capture_output=True, text=True, timeout=120)


@pytest.mark.parametrize("name", NAMES)
def test_help_forms_answer_identically(name, tmp_path):
    short = _run(name, ["-h"], tmp_path)
    long = _run(name, ["--help"], tmp_path)
    assert short.returncode == 0, short.stderr
    assert long.returncode == 0, long.stderr
    assert short.stdout == long.stdout
    for label in ("usage:", "options:", "side-effects:", "exit-codes:"):
        assert label in short.stdout
    assert name in short.stdout


@pytest.mark.parametrize("name", NAMES)
def test_version_reports_the_framework_version(name, tmp_path):
    proc = _run(name, ["--version"], tmp_path)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == f"{name} {_framework_version()}"


@pytest.mark.parametrize("name", NAMES)
def test_undeclared_option_is_refused(name, tmp_path):
    proc = _run(name, ["--not-a-declared-option"], tmp_path)
    assert proc.returncode == 2
    assert "--not-a-declared-option" in proc.stderr
    assert "usage:" in proc.stderr


@pytest.mark.parametrize("name", NAMES)
def test_flag_only_invocations_write_nothing(name, tmp_path):
    for args in (["-h"], ["--help"], ["--version"], ["--not-a-declared-option"]):
        _run(name, args, tmp_path)
    assert list(tmp_path.iterdir()) == [], f"{name} wrote something on a flag-only run"


@pytest.mark.parametrize("name", NAMES)
def test_wrong_operand_count_is_a_usage_error(name, tmp_path):
    proc = _run(name, WRONG_OPERANDS[name], tmp_path)
    assert proc.returncode == 1
    assert f"Usage: {name}" in proc.stdout


@pytest.mark.parametrize("flag,expected", [("--version", 0), ("-h", 0), ("--help", 0),
                                           ("--not-a-declared-option", 2)])
def test_registered_script_answers_without_optional_dependencies(flag, expected, tmp_path):
    """-S removes site-packages: Pillow and pypdf cannot be imported at all."""
    probe = subprocess.run([sys.executable, "-S", "-c", "import PIL"],
                           capture_output=True, text=True, timeout=60)
    assert probe.returncode != 0, "this host can import PIL without site-packages; probe is void"
    proc = _run(REGISTERED, [flag], tmp_path, no_site=True)
    assert proc.returncode == expected, proc.stderr
    assert list(tmp_path.iterdir()) == []


def test_registered_script_still_needs_pillow_to_act(tmp_path):
    """The dependency-free entry layer must not silently fake a successful run."""
    proc = _run(REGISTERED, ["1", "fields.json", "in.png", "out.png"], tmp_path, no_site=True)
    assert proc.returncode == 1
    assert "Pillow" in proc.stderr
    assert not (tmp_path / "out.png").exists()


@pytest.mark.parametrize("name", NAMES)
def test_generated_blocks_are_present_and_path_correct(name):
    text = (SCRIPTS / name).read_text(encoding="utf-8")
    assert "# script-interface:86:begin" in text
    assert "# script-interface:86:end" in text
    assert "_bridge_version" in text
    relative = f"skills/external/document-utils/scripts/pdf/{name}"
    assert f"_SIG_SCRIPT = '{relative}'" in text
    # Operand-only scripts declare no options; the flag vocabulary stays empty.
    assert "_SIG_DECLARED = ()" in text


@pytest.mark.parametrize("name", NAMES)
def test_third_party_imports_stay_inside_functions(name):
    """A module-level third-party import would break the dependency-free entry layer."""
    text = (SCRIPTS / name).read_text(encoding="utf-8")
    body = text.split("# script-interface:86:begin")[0]
    stdlib = {
        "contextlib", "dataclasses", "importlib", "io", "json", "os", "pathlib", "sys",
    }
    for line in body.splitlines():
        if not line.startswith(("import ", "from ")):
            continue                      # indented imports are the allowed lazy ones
        module = line.split()[1].split(".")[0]
        assert module in stdlib, f"{name}: module-level third-party import {line!r}"