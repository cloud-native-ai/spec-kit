import json
import subprocess
from pathlib import Path


def test_discover_contract_returns_unified_tools_payload():
    root = Path(__file__).resolve().parents[2]
    script = root / ".specify" / "scripts" / "bash" / "refresh-tools.sh"
    result = subprocess.run(
        [str(script), "--system", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert "tools" in payload
    assert isinstance(payload["tools"], list)
    assert "system_binaries" in payload

    for item in payload["tools"]:
        assert "sourceType" in item
        assert "sourceName" in item
        assert "canonicalName" in item
