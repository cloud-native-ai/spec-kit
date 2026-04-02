import json
import shutil
import subprocess
import uuid
from pathlib import Path


def test_create_new_skill_generates_json_tool_manifests():
    root = Path(__file__).resolve().parents[2]
    script = root / ".specify" / "scripts" / "bash" / "create-new-skill.sh"
    output_dir = root / "tmp" / f"skill-test-{uuid.uuid4().hex}"
    try:
        output_dir.mkdir(parents=True, exist_ok=False)
        result = subprocess.run(
            [
                str(script),
                "--json",
                "--output-dir",
                str(output_dir),
                "git-workflow-sync - 同步上游代码到目标分支",
            ],
            cwd=root,
            stdin=subprocess.DEVNULL,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)

        skill_dir = output_dir / "git-workflow-sync"
        assert payload["status"] == "created"
        assert payload["SKILL_NAME"] == "git-workflow-sync"
        assert (skill_dir / "SKILL.md").exists()
        assert (skill_dir / "tools" / "system.json").exists()
        assert (skill_dir / "tools" / "project.json").exists()
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)