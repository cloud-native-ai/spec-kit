"""Shell path regression tests for .specify/specs and requirements.md resolution.

Verifies that shell scripts resolve spec paths consistently across the
.specify/scripts/bash/ layer (Feature 022 / T017).
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read_shell_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSpecifyScriptPaths:
    def test_specify_common_uses_dot_specify_specs(self):
        """Verify .specify/scripts/bash/common.sh uses .specify/specs/ paths."""
        content = _read_shell_source(
            ROOT / ".specify" / "scripts" / "bash" / "common.sh"
        )
        assert ".specify/specs" in content, (
            "Missing .specify/specs reference in .specify/scripts/bash/common.sh"
        )

    def test_specify_common_does_not_use_legacy_specs_path(self):
        """Verify no legacy specs/<branch>/spec.md references remain."""
        content = _read_shell_source(
            ROOT / ".specify" / "scripts" / "bash" / "common.sh"
        )
        # The old spec file was spec.md; should not be referenced
        assert "spec.md" not in content, (
            "Legacy spec.md reference found in .specify/scripts/bash/common.sh"
        )

    def test_requirements_md_is_the_spec_reference(self):
        """Verify the feature spec points to requirements.md."""
        content = _read_shell_source(
            ROOT / ".specify" / "scripts" / "bash" / "common.sh"
        )
        assert "FEATURE_SPEC=" in content
        # FEATURE_SPEC should refer to requirements.md
        assert "requirements.md" in content, (
            "FEATURE_SPEC must reference requirements.md"
        )

    def test_get_feature_dir_produces_correct_path(self):
        """Verify get_feature_dir function returns the right path structure."""
        content = _read_shell_source(
            ROOT / ".specify" / "scripts" / "bash" / "common.sh"
        )
        # Should contain: get_feature_dir() { echo "$1/.specify/specs/$2"; }
        match = re.search(r"get_feature_dir\s*\(\).*\{.*\.specify/specs", content)
        assert match is not None, "get_feature_dir() must reference .specify/specs/"

    def test_scripts_packaged_common_uses_dot_specify_specs(self):
        """Verify scripts/bash/common.sh also uses .specify/specs/ paths."""
        packaged = ROOT / "scripts" / "bash" / "common.sh"
        if not packaged.exists():
            return  # skip if not present in dev layout
        content = _read_shell_source(packaged)
        assert ".specify/specs" in content, (
            "Missing .specify/specs reference in scripts/bash/common.sh"
        )
