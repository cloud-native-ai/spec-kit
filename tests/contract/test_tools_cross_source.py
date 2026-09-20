"""Contract test for the cross-source discovery payload of ``refresh-tools.sh --json``.

Runs the real script once with all three sources enabled and pins both the payload
shape a consumer depends on and the closed set of ``sourceType`` values it may carry.
"""

import json
import subprocess
from pathlib import Path


def test_cross_source_discovery_uses_supported_source_types():
    root = Path(__file__).resolve().parents[2]
    script = root / ".specify" / "scripts" / "bash" / "refresh-tools.sh"
    result = subprocess.run(
        [str(script), "--system", "--shell", "--project", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    # Unified payload: one flat `tools` list alongside the per-source buckets.
    assert "tools" in payload
    assert isinstance(payload["tools"], list)
    assert "system_binaries" in payload

    allowed = {"system", "shell", "project"}
    observed = {tool["sourceType"] for tool in payload["tools"]}
    assert observed.issubset(allowed)

    for item in payload["tools"]:
        assert "sourceType" in item
        assert "sourceName" in item
        assert "canonicalName" in item
