"""
Integration test for feature index creation with empty input
"""

import json
import os
import subprocess
import tempfile


def test_feature_index_creation_empty_input():
    """Test creating feature index with empty input creates proper empty structure"""
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock script directory
        script_dir = os.path.join(temp_dir, ".specify", "scripts", "bash")
        os.makedirs(script_dir, exist_ok=True)

        # Copy the actual create-feature-index.sh script
        actual_script = "/storage/project/cloud-native-ai/spec-kit/.specify/scripts/bash/create-feature-index.sh"
        test_script = os.path.join(script_dir, "create-feature-index.sh")
        with open(actual_script, "r") as src, open(test_script, "w") as dst:
            dst.write(src.read())
        os.chmod(test_script, 0o755)

        # Create common.sh if it exists
        common_sh = "/storage/project/cloud-native-ai/spec-kit/scripts/bash/common.sh"
        if os.path.exists(common_sh):
            test_common = os.path.join(temp_dir, ".specify", "scripts", "common.sh")
            os.makedirs(os.path.dirname(test_common), exist_ok=True)
            with open(common_sh, "r") as src, open(test_common, "w") as dst:
                dst.write(src.read())

        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            # Run the script with empty input
            result = subprocess.run(
                [test_script, "--json"],
                input="",
                text=True,
                capture_output=True,
                cwd=temp_dir,
            )

            # Check that command executed successfully
            assert result.returncode == 0, (
                f"Command failed with stderr: {result.stderr}"
            )

            # Parse JSON output
            output = json.loads(result.stdout.strip())

            # Verify features file was created
            memory_dir = os.path.join(temp_dir, ".specify", "memory")
            features_file = os.path.join(memory_dir, "features.md")
            assert os.path.exists(features_file)
            assert output["FEATURES_FILE"] == features_file

            # Verify total features count is 0
            assert output["TOTAL_FEATURES"] == 0

            # Verify features.md content format for empty index
            with open(features_file, "r") as f:
                content = f.read()

            # Check required structure
            assert "# Project Feature Index" in content
            assert "**Total Features**: 0" in content
            assert "## Features" in content
            assert (
                "| ID | Name | Description | Status | Spec Path | Last Updated |"
                in content
            )
            assert (
                "|----|------|-------------|--------|-----------|--------------|"
                in content
            )

            # Check that there are no feature rows (only header and separator)
            lines = content.split("\n")
            feature_rows = [
                line
                for line in lines
                if line.strip().startswith("| ")
                and "ID |" not in line
                and "----|" not in line
            ]
            assert len(feature_rows) == 0

        finally:
            os.chdir(original_cwd)
