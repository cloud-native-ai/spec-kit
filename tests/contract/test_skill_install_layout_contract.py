import json
import shutil
import subprocess
import uuid
from pathlib import Path


def test_install_contract_reports_primary_status_and_outcome_with_custom_output_dir():
    root = Path(__file__).resolve().parents[2]
    script = root / ".specify" / "scripts" / "bash" / "create-new-skill.sh"
    output_dir = root / "tmp" / f"skill-layout-contract-{uuid.uuid4().hex}"

    try:
        output_dir.mkdir(parents=True, exist_ok=False)
        result = subprocess.run(
            [
                str(script),
                "--json",
                "--output-dir",
                str(output_dir),
                "contract-layout-test - verify contract payload",
            ],
            cwd=root,
            stdin=subprocess.DEVNULL,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)

        assert payload["status"] == "created"
        assert payload["primary_copy_status"] == "created"
        assert payload["overall_status"] in {"success", "partial-success"}
        assert payload["migration_state"] in {
            "not-needed",
            "completed",
            "manual-required",
        }
        assert payload["entrypoint_github_status"] == "skipped"
        assert payload["SKILL_DIR"].endswith("/contract-layout-test")
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)
