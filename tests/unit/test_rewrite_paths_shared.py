"""Unit tests for the shared/ path-rewrite rule (Feature 029, contract C-REWRITE)."""

from specify_cli import rewrite_paths


def test_shared_path_rewritten_to_specify_prefix():
    assert (
        rewrite_paths("shared/workflow/user-input-protocol.md")
        == ".specify/shared/workflow/user-input-protocol.md"
    )


def test_shared_rewrite_is_guarded_against_double_prefix():
    already = ".specify/shared/workflow/feature-integration.md"
    assert rewrite_paths(already) == already


def test_shared_rewrite_is_idempotent():
    once = rewrite_paths("shared/workflow/tool-definitions.md")
    twice = rewrite_paths(once)
    assert once == twice == ".specify/shared/workflow/tool-definitions.md"


def test_shared_rewrite_alongside_existing_rules():
    text = "See shared/workflow/x.md and scripts/bash/y.sh and templates/z.md"
    out = rewrite_paths(text)
    assert ".specify/shared/workflow/x.md" in out
    assert ".specify/scripts/bash/y.sh" in out
    assert ".specify/templates/z.md" in out
