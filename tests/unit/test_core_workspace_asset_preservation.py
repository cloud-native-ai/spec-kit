"""Unit tests for core workspace asset preservation decisions.

Validates the detection and classification of .specify core assets during
initialization and assistant addition flows (Feature 022).
"""

from pathlib import Path

from specify_cli import (
    core_asset_relpaths,
    detect_configured_assistants,
    detect_initialized_core_assets,
    is_core_asset_initialized,
)


class TestCoreAssetRelpaths:
    def test_returns_list_of_strings(self):
        paths = core_asset_relpaths()
        assert isinstance(paths, list)
        assert all(isinstance(p, str) for p in paths)

    def test_includes_essential_paths(self):
        paths = core_asset_relpaths()
        assert ".specify/memory" in paths
        assert ".specify/templates" in paths
        assert ".specify/scripts" in paths
        assert ".specify/skills" in paths
        assert ".specify/instructions.md" in paths

    def test_no_duplicates(self):
        paths = core_asset_relpaths()
        assert len(paths) == len(set(paths))


class TestIsCoreAssetInitialized:
    def test_existing_asset_detected(self, tmp_path: Path):
        (tmp_path / ".specify" / "memory").mkdir(parents=True)
        assert is_core_asset_initialized(tmp_path, ".specify/memory")

    def test_missing_asset_not_detected(self, tmp_path: Path):
        assert not is_core_asset_initialized(tmp_path, ".specify/memory")

    def test_existing_file_detected(self, tmp_path: Path):
        (tmp_path / ".specify").mkdir(parents=True)
        (tmp_path / ".specify" / "instructions.md").write_text("test")
        assert is_core_asset_initialized(tmp_path, ".specify/instructions.md")


class TestDetectInitializedCoreAssets:
    def test_empty_project_returns_empty(self, tmp_path: Path):
        result = detect_initialized_core_assets(tmp_path)
        assert result == []

    def test_partial_core_returns_only_existing(self, tmp_path: Path):
        (tmp_path / ".specify" / "memory").mkdir(parents=True)
        (tmp_path / ".specify" / "instructions.md").write_text("test")
        result = detect_initialized_core_assets(tmp_path)
        assert ".specify/memory" in result
        assert ".specify/instructions.md" in result
        assert ".specify/templates" not in result

    def test_full_core_returns_all(self, tmp_path: Path):
        for p in core_asset_relpaths():
            target = tmp_path / p
            target.parent.mkdir(parents=True, exist_ok=True)
            if p.endswith(".md"):
                target.write_text("test")
            else:
                target.mkdir(exist_ok=True)
        result = detect_initialized_core_assets(tmp_path)
        assert len(result) == len(core_asset_relpaths())


class TestDetectConfiguredAssistants:
    def test_empty_project_returns_empty(self, tmp_path: Path):
        result = detect_configured_assistants(tmp_path)
        assert result == []

    def test_copilot_folder_detected(self, tmp_path: Path):
        (tmp_path / ".github").mkdir()
        result = detect_configured_assistants(tmp_path)
        assert "copilot" in result

    def test_multiple_assistants_detected(self, tmp_path: Path):
        (tmp_path / ".github").mkdir()
        (tmp_path / ".claude").mkdir()
        (tmp_path / ".qwen").mkdir()
        result = detect_configured_assistants(tmp_path)
        assert "copilot" in result
        assert "claude" in result
        assert "qwen" in result
