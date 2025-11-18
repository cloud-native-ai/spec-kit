"""
Contract test for /speckit.feature command output format
"""

import json
import os
import subprocess
import tempfile


def test_feature_command_json_output_format():
    """Test that /speckit.feature command outputs valid JSON with expected keys"""
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a mock features.md file
        memory_dir = os.path.join(temp_dir, ".specify", "memory")
        os.makedirs(memory_dir, exist_ok=True)
        features_file = os.path.join(memory_dir, "features.md")

        # Create a mock script directory structure
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
            # Test with feature description input
            feature_description = "Add user authentication system"

            # Run the script with JSON output
            result = subprocess.run(
                [test_script, "--json"],
                input=feature_description,
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

            # Verify JSON structure
            assert "FEATURES_FILE" in output
            assert "TOTAL_FEATURES" in output

            # Verify features file was created
            assert os.path.exists(output["FEATURES_FILE"])
            assert output["FEATURES_FILE"] == features_file

            # Verify total features count
            assert output["TOTAL_FEATURES"] == 1

            # Verify features.md content format
            with open(features_file, "r") as f:
                content = f.read()

            # Check for required header elements
            assert "# Project Feature Index" in content
            assert "**Last Updated**:" in content
            assert "**Total Features**: 1" in content
            assert "## Features" in content

            # Check for table header
            assert (
                "| ID | Name | Description | Status | Spec Path | Last Updated |"
                in content
            )
            assert (
                "|----|------|-------------|--------|-----------|--------------|"
                in content
            )

            # Check for feature row
            assert "| 001 |" in content
            assert "| Add user authentication system |" in content
            assert "| Draft |" in content
            assert "| (Not yet created) |" in content

        finally:
            os.chdir(original_cwd)


def test_feature_command_human_readable_output():
    """Test that /speckit.feature command outputs human-readable format correctly"""
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
            # Test with feature description input
            feature_description = "Implement payment processing"

            # Run the script without JSON flag
            result = subprocess.run(
                [test_script],
                input=feature_description,
                text=True,
                capture_output=True,
                cwd=temp_dir,
            )

            # Check that command executed successfully
            assert result.returncode == 0, (
                f"Command failed with stderr: {result.stderr}"
            )

            # Verify human-readable output
            assert "FEATURES_FILE:" in result.stdout
            assert "TOTAL_FEATURES:" in result.stdout
            assert "Feature index created/updated successfully" in result.stdout

            # Verify features.md was created
            memory_dir = os.path.join(temp_dir, ".specify", "memory")
            features_file = os.path.join(memory_dir, "features.md")
            assert os.path.exists(features_file)

        finally:
            os.chdir(original_cwd)


def test_feature_command_empty_input():
    """Test that /speckit.feature command handles empty input correctly"""
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

            # Verify features file was created (empty index)
            memory_dir = os.path.join(temp_dir, ".specify", "memory")
            features_file = os.path.join(memory_dir, "features.md")
            assert os.path.exists(features_file)

            # Verify total features count is 0
            assert output["TOTAL_FEATURES"] == 0

            # Verify features.md content format for empty index
            with open(features_file, "r") as f:
                content = f.read()

            assert "# Project Feature Index" in content
            assert "**Total Features**: 0" in content
            assert (
                "| ID | Name | Description | Status | Spec Path | Last Updated |"
                in content
            )

        finally:
            os.chdir(original_cwd)
