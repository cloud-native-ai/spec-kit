"""Interface and safety tests for references/types/plantuml/scripts/render-native.py.

No real rendering is performed here: the tests cover help/version, unknown flags,
overwrite refusal and the preflight-failure stop (a closed local port). Actual
rendering evidence belongs to the closure run, not to the unit tests.
"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "render-native.py"

SOURCE = """@startuml
A -> B : ping
@enduml
"""


def test_help_version_and_unknown_flag(tmp_path):
    for flag in ("--help", "--version"):
        proc = subprocess.run([sys.executable, "-B", str(SCRIPT), flag], capture_output=True, text=True)
        assert proc.returncode == 0
        assert proc.stdout.strip()
    proc = subprocess.run([sys.executable, "-B", str(SCRIPT), "--bogus"], capture_output=True, text=True)
    assert proc.returncode == 2


def test_overwrite_refused_before_network(tmp_path):
    source_path = tmp_path / "diagram.puml"
    source_path.write_text(SOURCE, encoding="utf-8")
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    (output_dir / "diagram.svg").write_text("keep", encoding="utf-8")
    proc = subprocess.run([
        sys.executable, "-B", str(SCRIPT),
        "--source", str(source_path),
        "--server", "http://127.0.0.1:9/plantuml",
        "--output-dir", str(output_dir),
        "--prefix", "diagram",
    ], capture_output=True, text=True)
    assert proc.returncode == 2
    assert (output_dir / "diagram.svg").read_text(encoding="utf-8") == "keep"


def test_preflight_failure_stops_before_render(tmp_path):
    source_path = tmp_path / "diagram.puml"
    source_path.write_text(SOURCE, encoding="utf-8")
    output_dir = tmp_path / "out"
    report_path = tmp_path / "render.json"
    proc = subprocess.run([
        sys.executable, "-B", str(SCRIPT),
        "--source", str(source_path),
        "--server", "http://127.0.0.1:9/plantuml",
        "--output-dir", str(output_dir),
        "--prefix", "diagram",
        "--report", str(report_path),
        "--timeout", "2",
    ], capture_output=True, text=True)
    assert proc.returncode == 3
    assert not (output_dir / "diagram.svg").exists()
    assert not (output_dir / "diagram.png").exists()
    report = report_path.read_text(encoding="utf-8")
    assert "preflight_failed" in report
    assert "preflight" in report


def test_server_url_validation(tmp_path):
    source_path = tmp_path / "diagram.puml"
    source_path.write_text(SOURCE, encoding="utf-8")
    for server in ("ftp://example.invalid", "http://example.invalid/path?query=1"):
        proc = subprocess.run([
            sys.executable, "-B", str(SCRIPT),
            "--source", str(source_path),
            "--server", server,
            "--output-dir", str(tmp_path / "out"),
            "--prefix", "diagram",
        ], capture_output=True, text=True)
        assert proc.returncode == 2
