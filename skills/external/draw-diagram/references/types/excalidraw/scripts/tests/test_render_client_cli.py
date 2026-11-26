"""Engine-local tests: render client CLI contract (no external service needed)."""
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
CLIENT = SCRIPTS / "render-client.py"


def run(args, cwd):
    return subprocess.run([sys.executable, str(CLIENT)] + args, cwd=cwd,
                          capture_output=True, text=True, timeout=120)


def test_help_and_version(tmp_path):
    help_run = run(["--help"], tmp_path)
    assert help_run.returncode == 0 and "exit codes" in help_run.stdout
    version_run = run(["--version"], tmp_path)
    assert version_run.returncode == 0 and "render-client.py" in version_run.stdout


def test_rejects_unknown_flag(tmp_path):
    out = run(["--server", "http://127.0.0.1:1", "--scene", "x", "--out-dir", "y",
               "--prefix", "p", "--bogus"], tmp_path)
    assert out.returncode == 2


def test_rejects_non_http_server(tmp_path):
    scene = tmp_path / "s.excalidraw"
    scene.write_text("{}", encoding="utf-8")
    out = run(["--server", "ftp://example", "--scene", str(scene), "--out-dir", str(tmp_path),
               "--prefix", "p"], tmp_path)
    assert out.returncode == 2
    assert "http" in out.stderr.lower()


def test_refuses_existing_output_before_any_request(tmp_path):
    scene = tmp_path / "s.excalidraw"
    scene.write_text("{}", encoding="utf-8")
    (tmp_path / "p.svg").write_text("<svg/>", encoding="utf-8")
    out = run(["--server", "http://127.0.0.1:1", "--scene", str(scene), "--out-dir", str(tmp_path),
               "--prefix", "p"], tmp_path)
    assert out.returncode == 2
    assert "refusing to overwrite" in out.stderr


def test_unreachable_service_is_a_blocker(tmp_path):
    scene = tmp_path / "s.excalidraw"
    scene.write_text('{"elements": []}', encoding="utf-8")
    out = run(["--server", "http://127.0.0.1:1", "--scene", str(scene), "--out-dir", str(tmp_path),
               "--prefix", "new"], tmp_path)
    assert out.returncode == 2
    assert "unavailable" in out.stderr
    assert not (tmp_path / "new.svg").exists()
