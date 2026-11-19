"""Regression: generated TOML command files stay parseable.

Adapted-from: 034fbfcbb4c62de4f07dead3ace6b45477b81b42 (backslashes: a multiline
*basic* string processes escapes, so a Windows path made the file unparseable)
and 94c7ec288fd34221e62fef50f3212f8a899eda95 (control characters are illegal in
every TOML string form and must be \\u-escaped).

No supported assistant currently maps to ``toml`` (``_ASSISTANT_EXTENSIONS``),
so the branch is latent; these cases pin it before a TOML assistant arrives.

``tomllib`` is stdlib from Python 3.11. On an older interpreter the round-trip
assertion degrades to the two properties that make the file parseable (no raw
illegal control character, the key is rendered) rather than passing silently.

Integration descriptions are quoted on purpose: master's ``description`` regex
stops at the first quote, and an unquoted value would over-capture across lines
(a separate pre-existing defect, out of this port's scope).

Value semantics pinned here: the multiline forms keep master's layout (a
newline before the closing delimiter), so the parsed prompt carries one
trailing newline; the escaped single-line basic form carries none.
"""

import re
from pathlib import Path

import specify_cli

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    tomllib = None


def _assert_value(text: str, key: str, expected: str) -> None:
    if tomllib is not None:
        assert tomllib.loads(text)[key] == expected
        return
    assert not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", text), (
        "raw illegal control character in generated TOML"
    )
    assert re.search(rf"^{key} = ", text, re.M), f"{key} not rendered"


def _generate_toml(
    tmp_path: Path, monkeypatch, template_text: str, name: str = "wintoml"
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
    specify_cli.generate_commands("claude", "toml", "$ARGUMENTS", out, "sh")
    return (out / f"speckit.{name}.toml").read_text(encoding="utf-8")


# --- helper rules -------------------------------------------------------------


def test_control_char_detection_allowances():
    assert specify_cli._has_illegal_toml_control("plain\ttext\n") is False
    assert specify_cli._has_illegal_toml_control("crlf\r\npair") is False
    assert specify_cli._has_illegal_toml_control("bare\rcr") is True
    for ch in ("\x00", "\x07", "\x1b", "\x7f"):
        assert specify_cli._has_illegal_toml_control(f"a{ch}b") is True


def test_basic_string_escape_round_trips_every_nasty_character():
    value = 'quote " backslash \\ tab \t nl \n cr \r bell \x07 esc \x1b del \x7f'
    rendered = specify_cli._escape_toml_basic(value)
    assert rendered.startswith('"') and rendered.endswith('"')
    assert "\n" not in rendered, "a basic string must stay on one line"
    _assert_value(f"key = {rendered}\n", "key", value)


def test_prompt_routing_prefers_multiline_then_literal_then_escaped():
    plain = specify_cli._render_toml_prompt("just text")
    assert plain.startswith('prompt = """\n')
    assert plain.endswith('\n"""')
    _assert_value(plain + "\n", "prompt", "just text\n")

    windows = specify_cli._render_toml_prompt(r"run C:\Users\dev\setup.ps1")
    assert windows.startswith("prompt = '''\n"), "backslash must not stay basic"
    _assert_value(windows + "\n", "prompt", "run C:\\Users\\dev\\setup.ps1\n")

    both = specify_cli._render_toml_prompt('a """ b \'\'\' c \\ d')
    assert both.startswith('prompt = "'), "both delimiters force the escape"
    assert "\n" not in both
    _assert_value(both + "\n", "prompt", 'a """ b \'\'\' c \\ d')

    control = specify_cli._render_toml_prompt("bell \x07 here")
    assert control.startswith('prompt = "'), "control chars force the escape"
    _assert_value(control + "\n", "prompt", "bell \x07 here")


def test_trailing_backslash_is_not_eaten_by_line_continuation():
    rendered = specify_cli._render_toml_prompt("ends with \\")
    # A multiline *basic* string would read the trailing backslash as a line
    # continuation and drop both it and the newline.
    _assert_value(rendered + "\n", "prompt", "ends with \\\n")


# --- through the generator ----------------------------------------------------


def test_windows_path_body_and_description_produce_parseable_toml(
    tmp_path, monkeypatch
):
    body = r"Run C:\Users\dev\project\setup.ps1 now"
    template = (
        "---\n"
        'description: "Run C:\\Users\\dev\\setup.ps1"\n'
        "---\n"
        f"{body}\n"
    )
    text = _generate_toml(tmp_path, monkeypatch, template)

    _assert_value(text, "description", r"Run C:\Users\dev\setup.ps1")
    _assert_value(text, "prompt", body + "\n")


def test_control_characters_in_body_survive_the_round_trip(tmp_path, monkeypatch):
    template = (
        "---\n"
        'description: "plain description"\n'
        "---\n"
        "bell \x07 esc \x1b del \x7f end\n"
    )
    text = _generate_toml(tmp_path, monkeypatch, template)

    assert not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", text)
    _assert_value(text, "prompt", "bell \x07 esc \x1b del \x7f end")


def test_plain_body_keeps_the_multiline_basic_layout(tmp_path, monkeypatch):
    template = (
        "---\n"
        'description: "plain description"\n'
        "---\n"
        "First line.\n"
        "\n"
        "Second line.\n"
    )
    text = _generate_toml(tmp_path, monkeypatch, template)

    assert text.startswith("# AUTO-GENERATED from templates/commands/wintoml.md")
    assert 'description = "plain description"\n' in text
    assert 'prompt = """\nFirst line.\n\nSecond line.\n"""\n' in text
    _assert_value(text, "prompt", "First line.\n\nSecond line.\n")