"""
Unit test for sequential feature ID generation
"""

import json
import os
import subprocess
import tempfile


def test_sequential_feature_id_generation():
    """Test that feature IDs are generated sequentially starting from 001"""
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
            result1 = subprocess.run(
                [test_script, "--json"],
                input="First feature",
                text=True,
                capture_output=True,
                cwd=temp_dir,
            )
            assert result1.returncode == 0
            output1 = json.loads(result1.stdout.strip())
            memory_dir = os.path.join(temp_dir, ".specify", "memory")
            features_file = os.path.join(memory_dir, "features.md")
            assert output1["FEATURES_FILE"] == features_file
            assert output1["TOTAL_FEATURES"] == 1

            # Add second feature
            result2 = subprocess.run(
                [test_script, "--json"],
                input="Second feature",
                text=True,
                capture_output=True,
                cwd=temp_dir,
            )
            assert result2.returncode == 0
            output2 = json.loads(result2.stdout.strip())
            assert output2["FEATURES_FILE"] == features_file
            assert output2["TOTAL_FEATURES"] == 2

            # Add third feature
            result3 = subprocess.run(
                [test_script, "--json"],
                input="Third feature",
                text=True,
                capture_output=True,
                cwd=temp_dir,
            )
            assert result3.returncode == 0
            output3 = json.loads(result3.stdout.strip())
            assert output3["FEATURES_FILE"] == features_file
            assert output3["TOTAL_FEATURES"] == 3

            # Verify features.md content has correct sequential IDs
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

            assert len(feature_rows) == 3

            # Check IDs are sequential
            ids = []
            for row in feature_rows:
                cols = [col.strip() for col in row.split("|")[1:-1]]
                ids.append(cols[0])

            assert ids == ["001", "002", "003"]

        finally:
            os.chdir(original_cwd)


def test_feature_id_generation_with_existing_features_file():
    """Test that ID generation respects existing features in features.md"""
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create existing features.md with some features
        memory_dir = os.path.join(temp_dir, ".specify", "memory")
        os.makedirs(memory_dir, exist_ok=True)
        existing_features = """# Project Feature Index

**Last Updated**: 2025-11-17
**Total Features**: 2

## Features

| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|
| 001 | auth system | Add user authentication | Draft | (Not yet created) | 2025-11-17 |
| 002 | payment processing | Implement payments | Planned | .specify/specs/002-payment-processing/spec.md | 2025-11-17 |
"""
        features_file = os.path.join(memory_dir, "features.md")
        with open(features_file, "w") as f:
            f.write(existing_features)

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
            # Add new feature - should get ID 003
            result = subprocess.run(
                [test_script, "--json"],
                input="New feature after existing ones",
                text=True,
                capture_output=True,
                cwd=temp_dir,
            )
            assert result.returncode == 0
            output = json.loads(result.stdout.strip())
            assert output["FEATURES_FILE"] == features_file
            assert output["TOTAL_FEATURES"] == 3

            # Verify new feature has ID 003
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

            assert len(feature_rows) == 3
            last_row = feature_rows[-1]
            cols = [col.strip() for col in last_row.split("|")[1:-1]]
            assert cols[0] == "003"
            assert "New feature after existing ones" in cols[2]

        finally:
            os.chdir(original_cwd)
