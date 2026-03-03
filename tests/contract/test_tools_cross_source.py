import json
import subprocess
from pathlib import Path


def test_cross_source_discovery_uses_supported_source_types():
    root = Path(__file__).resolve().parents[2]
    script = root / ".specify" / "scripts" / "bash" / "refresh-tools.sh"
    result = subprocess.run(
        [str(script), "--mcp", "--system", "--shell", "--project", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert isinstance(payload.get("tools"), list)
    allowed = {"mcp", "system", "shell", "project"}
    observed = {tool["sourceType"] for tool in payload["tools"]}
    assert observed.issubset(allowed)
