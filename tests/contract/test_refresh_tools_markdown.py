import subprocess
from pathlib import Path


def test_refresh_tools_rejects_markdown_format_option():
    root = Path(__file__).resolve().parents[2]
    script = root / ".specify" / "scripts" / "bash" / "refresh-tools.sh"
    result = subprocess.run(
        [str(script), "--system", "--format", "markdown"],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Usage:" in result.stderr