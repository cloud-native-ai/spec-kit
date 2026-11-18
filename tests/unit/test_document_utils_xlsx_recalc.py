"""Contract of xlsx/recalc.py: the JSON verdict, and what it asks LibreOffice to do.

LibreOffice is not a test dependency.  The subprocess step is replaced by a fake
that writes the cached values a real ``calculateAll()`` + ``store()`` would write
-- a ``<v>`` beside each ``<f>`` in the sheet part, which is exactly the difference
between a workbook openpyxl wrote and one a spreadsheet engine has evaluated.
Everything else runs for real: the macro module on disk, the command line handed
to soffice, and the two openpyxl reads that produce the report.

What is pinned: the result keys and their meaning, the error tokens and their
locations, the location cap, the formula count, the fact that formulas survive,
and the exit code (0 for a verdict, 1 for a missing operand).
"""

import importlib.util
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

openpyxl = pytest.importorskip("openpyxl", reason="openpyxl reads the recalculated workbook")

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "skills" / "external" / "document-utils" / "scripts"


def _load(script_name: str, module_name: str):
    path = SCRIPTS / "xlsx" / script_name
    assert path.is_file(), f"script missing: {path}"
    saved_path, saved_argv = list(sys.path), list(sys.argv)
    sys.argv = [str(path)]
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    finally:
        sys.argv = saved_argv
        sys.path[:] = saved_path
    return module


@pytest.fixture(scope="module")
def recalc():
    return _load("recalc.py", "_f3_xlsx_recalc")


@pytest.fixture(autouse=True)
def isolated_profile(tmp_path, monkeypatch, recalc):
    """Never touch the real user's LibreOffice profile."""
    directory = tmp_path / "lo-profile" / "basic" / "Standard"
    monkeypatch.setattr(recalc, "macro_directory", lambda: directory)
    return directory


def write_cached_values(path: Path, values: dict, sheet: str = "xl/worksheets/sheet1.xml"):
    """Store evaluated values beside the formulas, the way a spreadsheet engine does."""
    with zipfile.ZipFile(path) as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    xml = parts[sheet].decode("utf-8")
    for reference, (value, kind) in values.items():
        pattern = re.compile(r'(<c r="%s"[^>]*>)(.*?)(</c>)' % reference, re.S)

        def replace(match):
            opening, inner, closing = match.groups()
            if kind:
                opening = opening[:-1] + ' t="%s">' % kind
            inner = re.sub(r"<v>.*?</v>", "", inner, flags=re.S)
            return opening + inner + "<v>%s</v>" % value + closing

        xml, count = pattern.subn(replace, xml)
        assert count == 1, f"cell {reference} not found in {sheet}"
    parts[sheet] = xml.encode("utf-8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, blob in parts.items():
            archive.writestr(name, blob)


@pytest.fixture
def book(tmp_path: Path) -> Path:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Model"
    sheet["A1"] = 10
    sheet["A2"] = 0
    sheet["B1"] = "=A1*2"
    sheet["B2"] = "=A1/A2"
    sheet["B3"] = "=SUM(A1:A2)"
    sheet["C1"] = "=NOPE(1)"
    path = tmp_path / "model.xlsx"
    workbook.save(path)
    return path


@pytest.fixture
def fake_soffice(monkeypatch, recalc, book):
    """Record the soffice invocations and store the values the case decides on."""
    real_run = subprocess.run
    calls: list[list[str]] = []
    state = {
        "values": {"B1": ("20", None), "B3": ("10", None)},
        "returncode": 0,
        "stderr": "",
        "timeout": False,
    }

    def run(cmd, **kwargs):
        if not cmd or cmd[0] != "soffice":
            return real_run(cmd, **kwargs)
        calls.append(list(cmd))
        if "--terminate_after_init" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "", "")
        if state["timeout"]:
            write_cached_values(book, state["values"])
            raise subprocess.TimeoutExpired(cmd, kwargs.get("timeout", 30))
        if state["returncode"] == 0:
            write_cached_values(book, state["values"])
        return subprocess.CompletedProcess(cmd, state["returncode"], "", state["stderr"])

    monkeypatch.setattr(recalc.subprocess, "run", run)
    return state, calls


# --------------------------------------------------------------------------- #
# The verdict
# --------------------------------------------------------------------------- #
def test_a_clean_recalculation_reports_success(book, recalc, fake_soffice):
    result = recalc.recalc(book, 15)

    assert result == {
        "status": "success",
        "total_errors": 0,
        "error_summary": {},
        "total_formulas": 4,
    }


def test_error_values_are_counted_and_located(book, recalc, fake_soffice):
    fake_soffice[0]["values"] = {
        "B1": ("20", None),
        "B2": ("#DIV/0!", "e"),
        "B3": ("10", None),
        "C1": ("#NAME?", "e"),
    }

    result = recalc.recalc(book)

    assert result["status"] == "errors_found"
    assert result["total_errors"] == 2
    assert result["total_formulas"] == 4
    assert result["error_summary"] == {
        "#DIV/0!": {"count": 1, "locations": ["Model!B2"]},
        "#NAME?": {"count": 1, "locations": ["Model!C1"]},
    }


def test_every_error_token_is_recognized(book, recalc, fake_soffice):
    tokens = ("#VALUE!", "#DIV/0!", "#REF!", "#NAME?", "#NULL!", "#NUM!", "#N/A")
    workbook = openpyxl.load_workbook(book)
    sheet = workbook["Model"]
    for index, token in enumerate(tokens, start=1):
        sheet.cell(row=index, column=5, value=f"=A{index}")
    workbook.save(book)
    fake_soffice[0]["values"] = {
        f"E{index}": (token, "e") for index, token in enumerate(tokens, start=1)
    }

    result = recalc.recalc(book)

    assert result["total_errors"] == len(tokens)
    assert set(result["error_summary"]) == set(tokens)
    assert result["error_summary"]["#N/A"]["locations"] == ["Model!E7"]


def test_locations_are_capped_but_the_count_is_not(tmp_path, recalc, fake_soffice, book):
    workbook = openpyxl.load_workbook(book)
    sheet = workbook["Model"]
    for row in range(1, 26):
        sheet.cell(row=row, column=6, value=f"=A{row}")
    workbook.save(book)
    fake_soffice[0]["values"] = {f"F{row}": ("#REF!", "e") for row in range(1, 26)}

    summary = recalc.recalc(book)["error_summary"]["#REF!"]

    assert summary["count"] == 25
    assert len(summary["locations"]) == 20
    assert summary["locations"][0] == "Model!F1"


def test_a_cell_is_counted_once_under_the_first_token_it_holds(book, recalc, fake_soffice):
    fake_soffice[0]["values"] = {"B1": ("#REF! beside #DIV/0!", "str")}

    result = recalc.recalc(book)

    assert result["total_errors"] == 1
    assert set(result["error_summary"]) == {"#DIV/0!"}


def test_formulas_survive_the_recalculation(book, recalc, fake_soffice):
    recalc.recalc(book)

    workbook = openpyxl.load_workbook(book, data_only=False)
    assert workbook["Model"]["B2"].value == "=A1/A2"
    values = openpyxl.load_workbook(book, data_only=True)
    assert values["Model"]["B1"].value == 20


def test_locations_carry_the_sheet_name(book, recalc):
    workbook = openpyxl.load_workbook(book)
    second = workbook.create_sheet("Rates")
    second["A1"] = "=Model!A1/0"
    workbook.save(book)

    write_cached_values(book, {"A1": ("#DIV/0!", "e")}, sheet="xl/worksheets/sheet2.xml")
    result = recalc.scan_workbook(book)

    assert result["error_summary"]["#DIV/0!"]["locations"] == ["Rates!A1"]


# --------------------------------------------------------------------------- #
# What LibreOffice is asked to do
# --------------------------------------------------------------------------- #
def test_the_macro_command_names_the_sub_and_the_absolute_file(book, recalc, fake_soffice):
    recalc.recalc(book, 42)

    _, calls = fake_soffice
    # The first run also initializes a profile that does not exist yet.
    macro_calls = [cmd for cmd in calls if "--terminate_after_init" not in cmd]
    assert len(macro_calls) == 1
    command = macro_calls[0]
    assert command[:3] == ["soffice", "--headless", "--norestore"]
    assert command[3] == (
        "vnd.sun.star.script:Standard.Module1.RecalculateAndSave"
        "?language=Basic&location=application"
    )
    assert command[4] == str(book.resolve())


def test_the_macro_is_installed_once_and_then_reused(book, recalc, fake_soffice, isolated_profile):
    recalc.recalc(book)
    module = isolated_profile / "Module1.xba"
    first = module.read_bytes()

    recalc.recalc(book)

    assert module.read_bytes() == first
    assert b"Sub RecalculateAndSave" in first
    assert b"calculateAll()" in first


def test_an_existing_module_keeps_its_own_code(book, recalc, fake_soffice, isolated_profile):
    isolated_profile.mkdir(parents=True)
    module = isolated_profile / "Module1.xba"
    module.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<script:module xmlns:script="http://openoffice.org/2000/script" '
        'script:name="Module1" script:language="StarBasic">\n'
        "Sub UsersOwnMacro\nEnd Sub\n"
        "</script:module>\n",
        encoding="utf-8",
    )

    assert recalc.install_macro() is True

    text = module.read_text(encoding="utf-8")
    assert "Sub UsersOwnMacro" in text
    assert "Sub RecalculateAndSave" in text
    assert text.index("UsersOwnMacro") < text.index("RecalculateAndSave")


def test_a_profile_that_cannot_be_initialized_is_reported(book, recalc, monkeypatch, isolated_profile):
    def missing(cmd, **kwargs):
        raise FileNotFoundError(2, "No such file or directory", "soffice")

    monkeypatch.setattr(recalc.subprocess, "run", missing)

    assert recalc.recalc(book) == {"error": "Failed to setup LibreOffice macro"}


def test_a_failed_conversion_reports_the_engine_stderr(book, recalc, fake_soffice):
    fake_soffice[0].update(returncode=1, stderr="macro execution failed")

    assert recalc.recalc(book) == {"error": "macro execution failed"}


def test_a_timeout_still_reads_what_was_stored(book, recalc, fake_soffice):
    fake_soffice[0].update(timeout=True, values={"B1": ("20", None), "B2": ("#DIV/0!", "e")})

    result = recalc.recalc(book, 1)

    assert result["status"] == "errors_found"
    assert result["error_summary"]["#DIV/0!"]["locations"] == ["Model!B2"]


def test_a_missing_workbook_is_reported_without_starting_anything(tmp_path, recalc, fake_soffice):
    absent = tmp_path / "absent.xlsx"

    assert recalc.recalc(absent) == {"error": f"File {absent} does not exist"}
    assert fake_soffice[1] == []


def test_the_profile_init_call_precedes_the_macro_call(book, recalc, fake_soffice, isolated_profile):
    assert not isolated_profile.exists()

    recalc.recalc(book)

    _, calls = fake_soffice
    assert calls[0] == ["soffice", "--headless", "--terminate_after_init"]
    assert (isolated_profile / "Module1.xba").is_file()


def test_soffice_env_delegates_to_the_office_wrapper(recalc, monkeypatch):
    import types

    sentinel = {"SAL_USE_VCLPLUGIN": "svp"}
    package = types.ModuleType("office")
    package.__path__ = []
    wrapper = types.ModuleType("office.soffice")
    wrapper.get_soffice_env = lambda: sentinel
    monkeypatch.setitem(sys.modules, "office", package)
    monkeypatch.setitem(sys.modules, "office.soffice", wrapper)

    assert recalc._soffice_env() is sentinel


# --------------------------------------------------------------------------- #
# The command line
# --------------------------------------------------------------------------- #
def test_no_operand_prints_usage_and_exits_one(recalc, capsys):
    assert recalc.main([]) == 1

    captured = capsys.readouterr()
    assert "Usage: python recalc.py <excel_file> [timeout_seconds]" in captured.out
    assert "#DIV/0!" in captured.out


def test_the_cli_prints_the_json_verdict(book, recalc, fake_soffice, capsys):
    fake_soffice[0]["values"] = {"B1": ("20", None), "B2": ("#DIV/0!", "e")}

    assert recalc.main([str(book), "20"]) == 0

    printed = json.loads(capsys.readouterr().out)
    assert printed["status"] == "errors_found"
    assert printed["total_formulas"] == 4


def test_a_non_integer_timeout_is_rejected(book, recalc, fake_soffice, capsys):
    assert recalc.main([str(book), "soon"]) == 1
    assert "timeout_seconds must be an integer" in capsys.readouterr().err


def test_the_default_timeout_is_thirty_seconds(book, recalc, fake_soffice, monkeypatch):
    seen = {}
    real = recalc.subprocess.run

    def watch(cmd, **kwargs):
        seen["timeout"] = kwargs.get("timeout")
        return real(cmd, **kwargs)

    monkeypatch.setattr(recalc.subprocess, "run", watch)
    recalc.main([str(book)])

    assert seen["timeout"] == 30


def test_the_flag_entry_layer_answers_without_openpyxl():
    for flag, code in (("--help", 0), ("--version", 0), ("--not-an-option", 2)):
        finished = subprocess.run(
            [sys.executable, str(SCRIPTS / "xlsx" / "recalc.py"), flag],
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert finished.returncode == code, flag