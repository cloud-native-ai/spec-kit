"""Contract tests: `specify migrate` command surface (097 T014).

Green claims: contracts/migrate-cli.md C-1 (closed option set), C-2
(precondition), C-3 (outcome -> exit code), C-4 (stdout envelope keys).

Red-first: authored before the subcommand exists; every CLI invocation then
fails at the framework's "no such command" exit 2 and the constants below
raise AttributeError — the failures prove the behaviour is absent, not that an
assertion is broken.

Owners referenced, never restated: the outcome/exit table is extracted from
``requirements.md`` FR-019 and the JSON envelope keys from the C-4 block, so
the implementation constant is compared against the owner files rather than a
test-local guess.
"""

import json
import re
from pathlib import Path

import pytest

import specify_cli

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / ".specify" / "specs" / "097-speckit-migrate-command"


def _invoke(args, input_text=None):
    from typer.testing import CliRunner

    return CliRunner().invoke(specify_cli.app, args, input=input_text)


def _combined(result):
    return (result.output or "") + (getattr(result, "stderr", None) or "")


def _c4_envelope_keys():
    text = (SPEC_DIR / "contracts" / "migrate-cli.md").read_text(encoding="utf-8")
    section = text[text.index("## C-4"):text.index("## C-5")]
    block = re.search(r"```json\n(.*?)```", section, re.S).group(1)
    return set(json.loads(block))


def _fr019_outcome_codes():
    text = (SPEC_DIR / "requirements.md").read_text(encoding="utf-8")
    line = next(
        line for line in text.splitlines() if line.startswith("- **FR-019**:")
    )
    mapping = {}
    for token, code in re.findall(
        r"`(clean|planned|applied|blocked)`（[^）]*?退出\s*(\d)", line
    ):
        mapping[token] = int(code)
    assert len(mapping) == 4, mapping
    error = re.search(r"输入或前置条件错误退出\s*(\d)", line)
    assert error, "FR-019 input-error exit code is not readable"
    return mapping, int(error.group(1))


def _client_workspace(tmp_path):
    """A client workspace: `.specify/` exists, nothing else."""
    (tmp_path / ".specify").mkdir()
    return tmp_path


def _sample_workspace(tmp_path):
    """The legacy-shaped fixture is expensive; a bare `.specify/` already
    exercises the full plan/receipt path (everything is missing)."""
    return _client_workspace(tmp_path)


# ---------------------------------------------------------------------------
# C-6: --help answers with zero side effects and declares the outcome table
# ---------------------------------------------------------------------------


def test_help_exits_zero_declares_outcomes_and_has_zero_side_effects(
    tmp_path, monkeypatch
):
    workspace = tmp_path / "empty"
    workspace.mkdir()
    monkeypatch.chdir(workspace)
    before = sorted(path.name for path in workspace.iterdir())

    result = _invoke(["migrate", "--help"])

    assert result.exit_code == 0, _combined(result)
    assert sorted(path.name for path in workspace.iterdir()) == before
    text = _combined(result)
    for option in ("--dry-run", "--apply", "--workspace", "--format"):
        assert option in text, f"{option} missing from --help output"
    assert re.search(r"--dry-run[^\n]*default", text), (
        "--help must state that --dry-run is the default mode"
    )
    for token, code in _fr019_outcome_codes()[0].items():
        assert re.search(rf"{token}\s+exit\s+{code}", text), (
            f"--help must declare outcome {token!r} with exit {code}: {text}"
        )
    assert re.search(r"exit\s+2", text), "--help must declare the input-error exit"


# ---------------------------------------------------------------------------
# C-1 / C-4: closed option set, default mode, JSON envelope
# ---------------------------------------------------------------------------


def test_default_mode_is_dry_run_and_json_envelope_matches_c4(tmp_path):
    workspace = _sample_workspace(tmp_path)

    result = _invoke(["migrate", "--workspace", str(workspace), "--format", "json"])

    assert result.exit_code == 1, _combined(result)
    payload = json.loads(result.stdout)
    assert set(payload) == _c4_envelope_keys(), sorted(payload)
    assert payload["mode"] == "dry-run"
    assert payload["outcome"] == "planned"
    assert payload["exitCode"] == 1
    assert payload["receiptPath"] is None
    assert isinstance(payload["receipt"], dict)
    assert payload["receipt"]["mode"] == "dry-run"
    assert payload["receipt"]["workspace"] == str(workspace.resolve()), (
        "the dry-run receipt body must identify its workspace (C-4 / E-3)"
    )
    assert payload["summary"]["total"] == len(payload["items"])
    assert not (workspace / ".specify" / "memory" / "migrate").exists(), (
        "dry-run must not create the receipt store"
    )

    explicit = _invoke(
        ["migrate", "--dry-run", "--workspace", str(workspace), "--format", "json"]
    )
    assert explicit.exit_code == 1, _combined(explicit)
    repeat = json.loads(explicit.stdout)
    assert repeat["items"] == payload["items"], (
        "explicit --dry-run must equal the default mode byte-for-byte on the "
        "deterministic part"
    )
    assert repeat["summary"] == payload["summary"]


def test_apply_and_dry_run_together_exit_2_with_zero_writes(tmp_path):
    workspace = _sample_workspace(tmp_path)
    before = sorted(path.name for path in workspace.iterdir())

    result = _invoke(
        ["migrate", "--workspace", str(workspace), "--apply", "--dry-run"]
    )

    assert result.exit_code == 2, _combined(result)
    assert "mutually exclusive" in _combined(result)
    assert sorted(path.name for path in workspace.iterdir()) == before


@pytest.mark.parametrize(
    "flag", ["--bogus", "--yes", "--force", "--non-interactive", "-h"]
)
def test_undeclared_or_confirmation_flags_exit_2(tmp_path, flag):
    workspace = _sample_workspace(tmp_path)

    result = _invoke(["migrate", "--workspace", str(workspace), flag])

    assert result.exit_code == 2, _combined(result)
    assert "No such option" in _combined(result), (
        f"{flag} must be rejected as an undeclared option (C-1/C-5)"
    )


def test_invalid_format_exits_2(tmp_path):
    workspace = _sample_workspace(tmp_path)

    result = _invoke(["migrate", "--workspace", str(workspace), "--format", "yaml"])

    assert result.exit_code == 2, _combined(result)
    assert "format" in _combined(result).lower()


# ---------------------------------------------------------------------------
# C-2: the .specify/ precondition names specify init as the repair entry
# ---------------------------------------------------------------------------


def test_missing_specify_exits_2_naming_specify_init_with_zero_writes(tmp_path):
    workspace = tmp_path / "not-initialized"
    workspace.mkdir()
    before = sorted(path.name for path in workspace.iterdir())

    result = _invoke(["migrate", "--workspace", str(workspace)])

    assert result.exit_code == 2, _combined(result)
    assert "specify init" in _combined(result)
    assert sorted(path.name for path in workspace.iterdir()) == before
    assert not (workspace / ".specify").exists()


# ---------------------------------------------------------------------------
# C-3: outcome -> exit mapping matches requirements FR-019
# ---------------------------------------------------------------------------


def test_outcome_to_exit_mapping_matches_fr019():
    mapping, error_exit = _fr019_outcome_codes()

    assert dict(specify_cli.MIGRATE_OUTCOME_EXIT_CODES) == mapping
    assert specify_cli.MIGRATE_INPUT_ERROR_EXIT == error_exit
