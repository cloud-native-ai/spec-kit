import json
import subprocess
from pathlib import Path


def test_create_new_tools_find_returns_structured_not_found_payload():
    root = Path(__file__).resolve().parents[2]
    script = root / ".specify" / "scripts" / "bash" / "create-new-tools.sh"
    tool_name = "definitely-not-a-real-tool-7ac4f7b4"

    result = subprocess.run(
        [str(script), "--json", "--name", tool_name, "--action", "find"],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)

    assert payload["status"] == "not_found"
    assert payload["tool_name"] == tool_name