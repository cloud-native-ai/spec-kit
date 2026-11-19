"""Regression: command body extraction closes frontmatter on a whole ``---`` line.

Adapted-from: 7873c447bd5ea8f919d7bdde8b118525c463d9c0 — upstream located the
closing delimiter with a substring search, which stops at a ``---`` embedded in
a frontmatter value. Master's ``generate_commands`` had the same defect in its
body split (``cleaned_content.split("---")``); the line-anchored rule already
owned by ``split_agent_frontmatter`` now serves both call sites.

Each case builds a one-template resource root. ``MODULE_DIR`` is redirected so
the generator's repo-template fallback stays out of the fixture: the real 32
templates are guarded byte-for-byte by
``scripts/python/regen-command-copies.py --check``, not by this unit.
"""

from pathlib import Path

import specify_cli


def _generate(
    tmp_path: Path,
    monkeypatch,
    template_text: str,
    *,
    agent: str = "claude",
    ext: str = "md",
    name: str = "dashy",
) -> str:
    root = tmp_path / "resource"
    commands = root / "templates" / "commands"
    commands.mkdir(parents=True)
    (commands / f"{name}.md").write_text(template_text, encoding="utf-8")
    monkeypatch.setattr(specify_cli, "get_resource_path", lambda: root)
    monkeypatch.setattr(
        specify_cli, "MODULE_DIR", tmp_path / "pkg" / "specify_cli"
    )
    out = tmp_path / "out"
    specify_cli.generate_commands(agent, ext, "$ARGUMENTS", out, "sh")
    return (out / f"speckit.{name}.{ext}").read_text(encoding="utf-8")


def test_description_with_embedded_dashes_does_not_spill_into_body(
    tmp_path, monkeypatch
):
    template = (
        "---\n"
        "description: Separate sections with --- markers\n"
        "short-description: Separate sections\n"
        "---\n"
        "Body line one.\n"
        "\n"
        "---\n"
        "\n"
        "Body line two.\n"
    )
    content = _generate(tmp_path, monkeypatch, template)

    assert "Body line one." in content
    assert "Body line two." in content
    # The frontmatter remainder must not become body text, and the body's own
    # horizontal rule must survive verbatim.
    assert "markers" not in content
    assert "short-description" not in content
    assert content.endswith("Body line one.\n\n---\n\nBody line two.")


def test_body_without_frontmatter_keeps_text_before_the_first_rule(
    tmp_path, monkeypatch
):
    template = (
        "Intro paragraph.\n"
        "\n"
        "---\n"
        "\n"
        "Middle paragraph.\n"
        "\n"
        "---\n"
        "\n"
        "Tail paragraph.\n"
    )
    content = _generate(tmp_path, monkeypatch, template)

    # A substring split treats the two rules as frontmatter delimiters and
    # drops everything before the second one.
    assert "Intro paragraph." in content
    assert "Middle paragraph." in content
    assert content.endswith("Tail paragraph.")


def test_closing_delimiter_with_trailing_spaces_still_closes(tmp_path, monkeypatch):
    template = (
        "---\n"
        "description: plain\n"
        "---   \n"
        "Body after a padded delimiter.\n"
    )
    content = _generate(tmp_path, monkeypatch, template)

    assert content.endswith("Body after a padded delimiter.")
    assert "description: plain" not in content


def test_unterminated_frontmatter_keeps_whole_content(tmp_path, monkeypatch):
    template = "---\ndescription: never closed\nBody text.\n"
    content = _generate(tmp_path, monkeypatch, template)

    # No closing delimiter: the fallback keeps the document as-is (unchanged
    # by the port), so nothing is silently dropped.
    assert "Body text." in content
    assert "description: never closed" in content


def test_qoder_frontmatter_contract_survives_the_port(tmp_path, monkeypatch):
    template = (
        "---\n"
        "description: Full description with --- inside\n"
        "short-description: Short one\n"
        "---\n"
        "Body.\n"
    )
    content = _generate(tmp_path, monkeypatch, template, agent="qoder")

    assert content.startswith("---\ndescription: Short one\n---\n")
    assert content.endswith("Body.")


def test_shared_splitter_owns_the_line_anchored_rule():
    lines, body = specify_cli.split_agent_frontmatter(
        "---\ndescription: a --- b\n---\nbody\n"
    )
    assert lines == ["description: a --- b"]
    # splitlines() drops the final newline; generate_commands strips the body.
    assert body == "body"

    # No leading delimiter line -> no frontmatter, document returned intact.
    lines, body = specify_cli.split_agent_frontmatter("a --- b\n---\nc\n")
    assert lines == []
    assert body == "a --- b\n---\nc\n"