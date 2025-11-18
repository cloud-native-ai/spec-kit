"""
Unit test for Markdown table format validation
"""

import json
import os
import re
import subprocess
import tempfile


def test_markdown_table_format_validation():
    """Test that features.md is generated with correct Markdown table format"""
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
            # Add a feature
            feature_description = "Test feature for Markdown format validation"
            result = subprocess.run(
                [test_script, "--json"],
                input=feature_description,
                text=True,
                capture_output=True,
                cwd=temp_dir,
            )
            assert result.returncode == 0
            output = json.loads(result.stdout.strip())
            memory_dir = os.path.join(temp_dir, ".specify", "memory")
            features_file = os.path.join(memory_dir, "features.md")
            assert output["FEATURES_FILE"] == features_file

            # Read the generated features.md
            with open(features_file, "r") as f:
                content = f.read()

            # Validate overall structure
            lines = content.strip().split("\n")

            # Check header
            assert lines[0] == "# Project Feature Index"
            assert lines[2].startswith("**Last Updated**: ")
            assert lines[3] == "**Total Features**: 1"
            assert lines[5] == "## Features"
            assert (
                lines[7]
                == "| ID | Name | Description | Status | Spec Path | Last Updated |"
            )
            assert (
                lines[8]
                == "|----|------|-------------|--------|-----------|--------------|"
            )

            # Check feature row format
            feature_row = lines[9]
            assert feature_row.startswith("| 001 |")
            assert feature_row.endswith(" |")

            # Parse columns
            columns = [col.strip() for col in feature_row.split("|")[1:-1]]
            assert len(columns) == 6

            id_col, name_col, desc_col, status_col, spec_path_col, last_updated_col = (
                columns
            )

            # Validate each column
            assert id_col == "001"
            assert len(name_col) > 0  # Should have generated name
            assert desc_col == "Test feature for Markdown format validation"
            assert status_col == "Draft"
            assert spec_path_col == "(Not yet created)"
            assert re.match(r"\d{4}-\d{2}-\d{2}", last_updated_col)

            # Validate that there are no extra lines after the feature
            assert len(lines) == 10  # 9 lines + empty line at end

        finally:
            os.chdir(original_cwd)


def test_markdown_table_with_special_characters():
    """Test that features.md handles special characters in descriptions correctly"""
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
            # Test with special characters in description
            special_description = (
                "Feature with | pipe, * asterisk, _ underscore, and $ dollar"
            )
            result = subprocess.run(
                [test_script, "--json"],
                input=special_description,
                text=True,
                capture_output=True,
                cwd=temp_dir,
            )
            assert result.returncode == 0
            output = json.loads(result.stdout.strip())
            memory_dir = os.path.join(temp_dir, ".specify", "memory")
            features_file = os.path.join(memory_dir, "features.md")
            assert output["FEATURES_FILE"] == features_file

            # Read the generated features.md
            with open(features_file, "r") as f:
                content = f.read()

            # Find the feature row
            lines = content.split("\n")
            feature_row = None
            for line in lines:
                if "| 001 |" in line:
                    feature_row = line
                    break

            assert feature_row is not None

            # Parse columns - should handle special characters correctly
            columns = [col.strip() for col in feature_row.split("|")[1:-1]]
            assert len(columns) == 6
            assert (
                columns[2] == special_description
            )  # Description should be preserved exactly

        finally:
            os.chdir(original_cwd)
