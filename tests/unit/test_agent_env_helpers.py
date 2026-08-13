"""Unit tests for pure Bash helpers in config-agent.sh (T018).

Exercises the standalone helpers used by the unified env-var flow:
  - `_ca_url_has_scheme` — scheme sanity check
  - `_ca_dotenv_upsert`  — idempotent dotenv key upsert that preserves lines

These are invoked directly via a sourced bash subprocess.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "agent-cli-setup" / "scripts" / "config-agent.sh"


def _bash(snippet: str, home: Path) -> subprocess.CompletedProcess:
    script = f'source "{SCRIPT}"\n{snippet}\n'
    return subprocess.run(
        ["bash", "-c", script],
        capture_output=True,
        text=True,
        env={"HOME": str(home), "PATH": __import__("os").environ.get("PATH", "")},
        cwd=str(home),
    )


class TestUrlHasScheme:
    def test_https_ok(self, tmp_path: Path):
        assert _bash('_ca_url_has_scheme "https://x.test/v1"', tmp_path).returncode == 0

    def test_http_ok(self, tmp_path: Path):
        assert _bash('_ca_url_has_scheme "http://x.test"', tmp_path).returncode == 0

    def test_missing_scheme_fails(self, tmp_path: Path):
        assert _bash('_ca_url_has_scheme "x.test/v1"', tmp_path).returncode != 0

    def test_wrong_scheme_fails(self, tmp_path: Path):
        assert _bash('_ca_url_has_scheme "ftp://x.test"', tmp_path).returncode != 0

    def test_empty_fails(self, tmp_path: Path):
        assert _bash('_ca_url_has_scheme ""', tmp_path).returncode != 0


class TestDotenvUpsert:
    def test_creates_file_and_key(self, tmp_path: Path):
        f = tmp_path / ".env"
        r = _bash(f'_ca_dotenv_upsert "{f}" OPENAI_MODEL glm-5.2', tmp_path)
        assert r.returncode == 0, r.stderr
        assert "OPENAI_MODEL=glm-5.2" in f.read_text(encoding="utf-8")

    def test_updates_existing_key_in_place(self, tmp_path: Path):
        f = tmp_path / ".env"
        f.write_text("KEEP=1\nOPENAI_MODEL=old\nOTHER=2\n", encoding="utf-8")
        r = _bash(f'_ca_dotenv_upsert "{f}" OPENAI_MODEL new', tmp_path)
        assert r.returncode == 0, r.stderr
        text = f.read_text(encoding="utf-8")
        assert "OPENAI_MODEL=new" in text
        assert "OPENAI_MODEL=old" not in text
        # unrelated lines preserved
        assert "KEEP=1" in text
        assert "OTHER=2" in text
        # exactly one occurrence of the key
        assert text.count("OPENAI_MODEL=") == 1

    def test_idempotent(self, tmp_path: Path):
        f = tmp_path / ".env"
        _bash(f'_ca_dotenv_upsert "{f}" OPENAI_BASE_URL https://x.test/v1', tmp_path)
        first = f.read_text(encoding="utf-8")
        _bash(f'_ca_dotenv_upsert "{f}" OPENAI_BASE_URL https://x.test/v1', tmp_path)
        assert f.read_text(encoding="utf-8") == first

    def test_preserves_url_value_with_slashes(self, tmp_path: Path):
        f = tmp_path / ".env"
        url = "https://host.test/compatible-mode/v1"
        r = _bash(f'_ca_dotenv_upsert "{f}" OPENAI_BASE_URL {url}', tmp_path)
        assert r.returncode == 0, r.stderr
        assert f"OPENAI_BASE_URL={url}" in f.read_text(encoding="utf-8")
