"""Contract test for Codex CLI compatibility file (T048).

Assert that codex has an entry in _INSTRUCTIONS_FILE_MAP and _IGNORE_FILE_MAP.
"""

import pytest

from specify_cli import _INSTRUCTIONS_FILE_MAP, _IGNORE_FILE_MAP

pytestmark = pytest.mark.contract


def test_codex_in_instructions_file_map():
    assert "codex" in _INSTRUCTIONS_FILE_MAP


def test_codex_in_ignore_file_map():
    assert "codex" in _IGNORE_FILE_MAP
    assert _IGNORE_FILE_MAP["codex"] == ".codexignore"
