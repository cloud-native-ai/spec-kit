"""
Integration test for feature index update with feature description
"""

import json
import os
import re
import subprocess
import tempfile


def test_feature_index_update_with_description():
    """Test updating feature index with feature description adds proper entry"""
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
            feature_description = "Add user authentication system with OAuth2 support"

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

            # Verify features file was created
            memory_dir = os.path.join(temp_dir, ".specify", "memory")
            features_file = os.path.join(memory_dir, "features.md")
            assert os.path.exists(features_file)
            assert output["FEATURES_FILE"] == features_file

            # Verify total features count is 1
            assert output["TOTAL_FEATURES"] == 1

            # Verify features.md content
            with open(features_file, "r") as f:
                content = f.read()

            # Check required structure
            assert "# Project Feature Index" in content
            assert "**Total Features**: 1" in content
            assert "## Features" in content
            assert (
                "| ID | Name | Description | Status | Spec Path | Last Updated |"
                in content
            )
            assert (
                "|----|------|-------------|--------|-----------|--------------|"
                in content
            )

            # Check for feature row with expected content
            lines = content.split("\n")
            feature_row = None
            for line in lines:
                if line.strip().startswith("| 001 |"):
                    feature_row = line
                    break

            assert feature_row is not None, "Feature row not found in features.md"

            # Parse the feature row
            columns = [col.strip() for col in feature_row.split("|")[1:-1]]
            assert len(columns) == 6, f"Expected 6 columns, got {len(columns)}"

            id_col, name_col, desc_col, status_col, spec_path_col, last_updated_col = (
                columns
            )

            # Verify ID
            assert id_col == "001"

            # Verify name (should be meaningful words from description)
            assert len(name_col) > 0
            assert "user" in name_col.lower()
            assert "authentication" in name_col.lower()

            # Verify description
            assert desc_col == "Add user authentication system with OAuth2 support"

            # Verify status
            assert status_col == "Draft"

            # Verify spec path
            assert spec_path_col == "(Not yet created)"

            # Verify last updated format (YYYY-MM-DD)
            assert re.match(r"\d{4}-\d{2}-\d{2}", last_updated_col)

        finally:
            os.chdir(original_cwd)


def test_feature_index_multiple_features():
    """Test adding multiple features creates sequential IDs"""
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
            # Add first feature
            feature1 = "Add user authentication"
            result1 = subprocess.run(
                [test_script, "--json"],
                input=feature1,
                text=True,
                capture_output=True,
                cwd=temp_dir,
            )
            assert result1.returncode == 0

            # Add second feature
            feature2 = "Implement payment processing"
            result2 = subprocess.run(
                [test_script, "--json"],
                input=feature2,
                text=True,
                capture_output=True,
                cwd=temp_dir,
            )
            assert result2.returncode == 0

            # Parse final output
            output2 = json.loads(result2.stdout.strip())
            memory_dir = os.path.join(temp_dir, ".specify", "memory")
            features_file = os.path.join(memory_dir, "features.md")
            assert output2["FEATURES_FILE"] == features_file
            assert output2["TOTAL_FEATURES"] == 2

            # Verify features.md content
            with open(features_file, "r") as f:
                content = f.read()

            lines = content.split("\n")
            feature_rows = []
            for line in lines:
                if (
                    line.strip().startswith("| ")
                    and "ID |" not in line
                    and "----|" not in line
                ):
                    feature_rows.append(line)

            assert len(feature_rows) == 2

            # Parse first feature
            cols1 = [col.strip() for col in feature_rows[0].split("|")[1:-1]]
            assert cols1[0] == "001"
            assert "authentication" in cols1[2].lower()

            # Parse second feature
            cols2 = [col.strip() for col in feature_rows[1].split("|")[1:-1]]
            assert cols2[0] == "002"
            assert "payment" in cols2[2].lower()

        finally:
            os.chdir(original_cwd)
