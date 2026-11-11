"""Integration: US3 cross-version — one-pass N→N+k convergence and interrupted-apply resume (097 T029).

Green claim: contracts/migrate-engine.md C-7 (archive layout, per-run receipt
store, idempotence, and resumption judged from the interrupted receipt's own
records — never from paths the new run computes).

Fixture stories:

* the multi-generation fixture layers two generations of residue on one tree —
  the legacy builders' constructs plus a second batch built from the SAME owner
  declarations (``_OBSOLETE_SKILLS`` / ``_OBSOLETE_COMMANDS`` /
  ``_OBSOLETE_TEMPLATES`` / ``_OBSOLETE_SKILL_FILES`` /
  ``_FRAMEWORK_INTERNAL_SKILLS``), each name asserted present in its owner and
  in the checker output at build time (FR-023 / C-8);
* the interruption fixture is the quickstart one: run a full apply, then delete
  the written target and leave the receipt back at ``status=running`` with its
  archive entry — the second run must report the interrupted stage, complete
  the write, and leave the archived object where the old receipt says it is.

Red-first: authored before receipt source/target recording and the resume path
exist, so the version-field and resume assertions fail on absent behaviour
(readings in notes/red-first-evidence.md). The source-version mutation test is
deliberately green at red stage (it consumes only the plan surface pkg03
already ships) and exists to prove the record-only assertion has
discriminative power.
"""

import hashlib
import importlib.util
import json
import os
import shutil
from pathlib import Path

import pytest

import specify_cli

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
BUILDERS_PATH = ROOT / "tests" / "fixtures" / "migrate-097" / "builders.py"

# Second-generation constructs, all framework-owned names. Every constant is
# asserted present in its owner declaration before use — never guessed.
GEN2_SKILL_NAMES = ("agent-setup", "cli-setup")  # older than gen-1's agent-cli-setup
GEN2_COMMAND_STEM = "mcpcall"
GEN2_TEMPLATE_NAME = "agent-plan-template.md"
GEN2_SKILL_FILE = "create-pages/scripts/scaffold.sh"
GEN2_FLAT_INTERNAL = "summarize-project"
FIXTURE_ASSISTANT = "qoder"

# The replaced template is the interruption victim: after apply it exists in its
# converged form while its old content sits in the run's archive.
INTERRUPTED_TARGET = ".specify/templates/plan-template.md"


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _builders():
    spec = importlib.util.spec_from_file_location(
        "_migrate_us3_builders", BUILDERS_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _invoke(args, input_text=None):
    from typer.testing import CliRunner

    return CliRunner().invoke(specify_cli.app, args, input=input_text)


def _json_payload(result, expected_code):
    assert result.exit_code == expected_code, (
        f"exit {result.exit_code}, expected {expected_code}\n{result.output}"
    )
    return json.loads(result.stdout)


def _dry_run(workspace):
    return _invoke(["migrate", "--workspace", str(workspace), "--format", "json"])


def _apply(workspace):
    return _invoke(
        ["migrate", "--workspace", str(workspace), "--apply", "--format", "json"]
    )


def _allow_apply(monkeypatch):
    monkeypatch.setattr(specify_cli, "migrate_symlink_supported", lambda: True)


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            digest.update(f"L {rel} -> {os.readlink(path)}\n".encode("utf-8"))
        elif path.is_dir():
            digest.update(f"D {rel}\n".encode("utf-8"))
        else:
            content = hashlib.sha256(path.read_bytes()).hexdigest()
            digest.update(f"F {rel} {content}\n".encode("utf-8"))
    return digest.hexdigest()


# ---------------------------------------------------------------------------
# Multi-generation fixture — two batches of residue from owner declarations
# ---------------------------------------------------------------------------


def _build_multi_generation(dest):
    """Legacy builders' constructs + a second, older generation of the same classes."""
    builders = _builders()
    workspace = builders.build_legacy_project(dest)
    specify = workspace / ".specify"
    sanitize = builders._engine_module("sanitize-utils.py")

    # Generation 2, class 1: obsolete skill directories (an older naming wave).
    for name in GEN2_SKILL_NAMES:
        assert name in specify_cli._OBSOLETE_SKILLS, (
            f"fixture skill {name!r} is not in _OBSOLETE_SKILLS"
        )
        skill_dir = specify / "skills" / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"# {name} (generation-2 fixture residue)\n", encoding="utf-8"
        )
    residue_targets = {
        finding["target"] for finding in sanitize.check_legacy_install_residue(workspace)
    }
    for name in GEN2_SKILL_NAMES:
        assert f".specify/skills/{name}" in residue_targets, (
            f"check_legacy_install_residue does not report .specify/skills/{name}"
        )

    # Generation 2, class 2: an obsolete command copy in the active tool directory.
    assert GEN2_COMMAND_STEM in specify_cli._OBSOLETE_COMMANDS, (
        f"fixture command {GEN2_COMMAND_STEM!r} is not in _OBSOLETE_COMMANDS"
    )
    command_rel = specify_cli._ASSISTANT_COMMAND_DIRS[FIXTURE_ASSISTANT]
    command_ext = specify_cli._ASSISTANT_EXTENSIONS[FIXTURE_ASSISTANT]
    command_path = workspace / command_rel / f"speckit.{GEN2_COMMAND_STEM}.{command_ext}"
    command_path.parent.mkdir(parents=True, exist_ok=True)
    command_path.write_text(
        f"# obsolete command: {GEN2_COMMAND_STEM}\n", encoding="utf-8"
    )

    # Generation 2, class 3: an obsolete top-level template.
    assert GEN2_TEMPLATE_NAME in specify_cli._OBSOLETE_TEMPLATES, (
        f"fixture template {GEN2_TEMPLATE_NAME!r} is not in _OBSOLETE_TEMPLATES"
    )
    template_path = specify / "templates" / GEN2_TEMPLATE_NAME
    template_path.write_text("# obsolete generation-2 template\n", encoding="utf-8")

    # Generation 2, class 4: a file a still-shipping skill no longer owns.
    assert GEN2_SKILL_FILE in specify_cli._OBSOLETE_SKILL_FILES, (
        f"fixture skill file {GEN2_SKILL_FILE!r} is not in _OBSOLETE_SKILL_FILES"
    )
    skill_file_path = specify / "skills" / GEN2_SKILL_FILE
    skill_file_path.parent.mkdir(parents=True, exist_ok=True)
    skill_file_path.write_text("# obsolete generation-2 skill file\n", encoding="utf-8")

    # Generation 2, class 5: a flat duplicate of another nested internal skill.
    assert GEN2_FLAT_INTERNAL in specify_cli._FRAMEWORK_INTERNAL_SKILLS, (
        f"fixture internal skill {GEN2_FLAT_INTERNAL!r} is not in "
        "_FRAMEWORK_INTERNAL_SKILLS"
    )
    nested = specify / "skills" / "internal" / GEN2_FLAT_INTERNAL
    flat = specify / "skills" / GEN2_FLAT_INTERNAL
    if not nested.is_dir():
        raise FileNotFoundError(f"nested internal skill missing: {nested}")
    shutil.copytree(nested, flat)
    duplicate_targets = {
        finding["target"]
        for finding in sanitize.check_flat_internal_duplicates(workspace)
    }
    assert f".specify/skills/{GEN2_FLAT_INTERNAL}" in duplicate_targets, (
        "check_flat_internal_duplicates does not report the generation-2 flat duplicate"
    )

    # Every generation-2 construct must be visible to the same decision function
    # the planner consumes (never a guessed name).
    decisions = {
        decision["path"]: decision["kind"]
        for decision in specify_cli.plan_obsolete_framework_asset_removals(
            workspace, FIXTURE_ASSISTANT
        )
    }
    assert decisions.get(command_path.relative_to(workspace).as_posix()) == (
        "obsolete-command"
    )
    assert decisions.get(template_path.relative_to(workspace).as_posix()) == (
        "obsolete-template"
    )
    assert decisions.get(skill_file_path.relative_to(workspace).as_posix()) == (
        "obsolete-skill-file"
    )
    return workspace


def _generation2_targets(workspace):
    return {
        ".specify/skills/" + GEN2_SKILL_NAMES[0],
        ".specify/skills/" + GEN2_SKILL_NAMES[1],
        (
            specify_cli._ASSISTANT_COMMAND_DIRS[FIXTURE_ASSISTANT].rstrip("/")
            + f"/speckit.{GEN2_COMMAND_STEM}."
            + specify_cli._ASSISTANT_EXTENSIONS[FIXTURE_ASSISTANT]
        ),
        ".specify/templates/" + GEN2_TEMPLATE_NAME,
        ".specify/skills/" + GEN2_SKILL_FILE,
        ".specify/skills/" + GEN2_FLAT_INTERNAL,
    }


# ---------------------------------------------------------------------------
# SC-004: two generations converge in one run; receipt records both versions
# ---------------------------------------------------------------------------


def test_multi_generation_fixture_converges_in_one_run_and_records_versions(
    tmp_path, monkeypatch
):
    workspace = _build_multi_generation(tmp_path / "multi")
    stamp_before = (workspace / ".specify" / "source.json").read_bytes()
    stamp = json.loads(stamp_before)

    dry = _json_payload(_dry_run(workspace), 1)
    targets = {item["target"] for item in dry["items"]}
    missing = sorted(_generation2_targets(workspace) - targets)
    assert not missing, f"generation-2 residue missing from the plan: {missing}"

    _allow_apply(monkeypatch)
    payload = _json_payload(_apply(workspace), 0)
    receipt = payload["receipt"]

    assert receipt["outcome"] == "applied"
    assert receipt["status"] == "completed"
    assert all(item["status"] == "done" for item in receipt["items"]), [
        (item["target"], item["status"]) for item in receipt["items"]
    ]

    # One run converged both generations — no intermediate-version step exists.
    receipt_files = sorted(
        specify_cli.migrate_receipts_dir(workspace).glob("*.json")
    )
    assert [path.stem for path in receipt_files] == [receipt["runId"]]

    # Source version: read from the workspace stamp and recorded verbatim.
    assert receipt["source"]["stampFile"] == ".specify/source.json"
    assert receipt["source"]["frameworkCommit"] == stamp["commit"]
    assert receipt["source"]["stampedAt"] == stamp["stamped_at"]

    # Target version: the running CLI's own version and framework commit.
    resolved = specify_cli.resolve_source_commit()
    assert receipt["target"]["frameworkCommit"] == (
        resolved["commit"] or "unavailable"
    )
    assert receipt["target"]["origin"] == resolved["origin"]
    assert isinstance(receipt["target"]["cliVersion"], str)
    assert receipt["target"]["cliVersion"]

    # Record-only: apply neither re-stamps the workspace nor runs init.
    assert (workspace / ".specify" / "source.json").read_bytes() == stamp_before

    before = _tree_digest(workspace)
    clean = _json_payload(_dry_run(workspace), 0)
    assert clean["outcome"] == "clean"
    assert clean["summary"]["total"] == 0
    assert _tree_digest(workspace) == before, (
        "the post-apply re-run wrote to the workspace (FR-017 idempotence)"
    )


# ---------------------------------------------------------------------------
# FR-020: source version is record-only; absent / unreadable is data
# ---------------------------------------------------------------------------


def test_source_stamp_is_record_only_and_unavailable_when_absent_or_unreadable(
    tmp_path,
):
    stamped = _builders().build_legacy_project(tmp_path / "stamped")
    stamp = json.loads(
        (stamped / ".specify" / "source.json").read_text(encoding="utf-8")
    )
    present = _json_payload(_dry_run(stamped), 1)
    source = present["receipt"]["source"]
    assert source["stampFile"] == ".specify/source.json"
    assert source["frameworkCommit"] == stamp["commit"]
    assert source["stampedAt"] == stamp["stamped_at"]
    if stamp["commit"] != "unavailable":
        assert source["reason"] is None

    absent_fixture = _builders().build_legacy_project(tmp_path / "absent")
    (absent_fixture / ".specify" / "source.json").unlink()
    absent_plan = _json_payload(_dry_run(absent_fixture), 1)
    absent_source = absent_plan["receipt"]["source"]
    assert absent_source["stampFile"] is None
    assert absent_source["frameworkCommit"] == "unavailable"
    assert absent_source["stampedAt"] is None
    assert absent_source["reason"], "an absent stamp must carry its reason"

    # Record-only: dropping the stamp changes the receipt's source record but
    # no deterministic plan part (dispositions never read the source version).
    assert present["items"] == absent_plan["items"]
    assert present["summary"] == absent_plan["summary"]
    assert present["outcome"] == absent_plan["outcome"]

    unreadable = _builders().build_legacy_project(tmp_path / "unreadable")
    (unreadable / ".specify" / "source.json").write_text(
        "{not-json\n", encoding="utf-8"
    )
    unreadable_source = _json_payload(_dry_run(unreadable), 1)["receipt"]["source"]
    assert unreadable_source["stampFile"] == ".specify/source.json"
    assert unreadable_source["frameworkCommit"] == "unavailable"
    assert unreadable_source["reason"], "an unreadable stamp must carry its reason"


# ---------------------------------------------------------------------------
# SC-004 mutation: selecting paths by source version turns plan identity red
# ---------------------------------------------------------------------------


def test_mutation_selecting_paths_by_source_version_turns_plan_identity_red(
    tmp_path, monkeypatch
):
    stamped = _builders().build_legacy_project(tmp_path / "stamped")
    unstamped = _builders().build_legacy_project(tmp_path / "unstamped")
    (unstamped / ".specify" / "source.json").unlink()

    control = (
        _json_payload(_dry_run(stamped), 1),
        _json_payload(_dry_run(unstamped), 1),
    )
    _assert_source_independent(*control)

    original = specify_cli._MIGRATE_DIMENSION_PLANNERS["migration-residue"]

    def version_branched(ctx):
        # The forbidden shape: an "old" (unstamped) source skips the residue
        # pass instead of converging to the same expected state.
        if not (ctx.workspace / ".specify" / "source.json").is_file():
            return []
        return original(ctx)

    with monkeypatch.context() as patch:
        patch.setitem(
            specify_cli._MIGRATE_DIMENSION_PLANNERS,
            "migration-residue",
            version_branched,
        )
        mutated = (
            _json_payload(_dry_run(stamped), 1),
            _json_payload(_dry_run(unstamped), 1),
        )

    with pytest.raises(AssertionError):
        _assert_source_independent(*mutated)


def _assert_source_independent(first, second):
    assert first["items"] == second["items"], (
        "the plan changed with the recorded source version — dispositions "
        "must not read it (FR-020)"
    )
    assert first["summary"] == second["summary"]
    assert first["outcome"] == second["outcome"]
    assert first["exitCode"] == second["exitCode"]
    assert first["notes"] == second["notes"]


# ---------------------------------------------------------------------------
# SC-006: interrupted apply resumes from its own receipt, no second move
# ---------------------------------------------------------------------------


def _make_interrupted_workspace(tmp_path, monkeypatch):
    """Full apply, then quickstart's interruption: target deleted, receipt running."""
    workspace = _builders().build_legacy_project(tmp_path / "interrupted")
    _allow_apply(monkeypatch)

    first = _json_payload(_apply(workspace), 0)
    receipt_path = workspace / first["receiptPath"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    old_run = receipt["runId"]

    entry = next(
        archive
        for archive in receipt["archives"]
        if archive["path"] == INTERRUPTED_TARGET
    )
    target = workspace / INTERRUPTED_TARGET
    if not target.is_file():
        raise FileNotFoundError(f"converged target missing: {target}")
    expected_bytes = target.read_bytes()
    if not (workspace / entry["archiveTo"]).exists():
        raise FileNotFoundError(f"archive missing: {entry['archiveTo']}")

    target.unlink()
    receipt["status"] = "running"
    receipt["finishedAt"] = None
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return workspace, old_run, entry, expected_bytes, receipt_path


def test_interrupted_apply_resumes_and_never_re_moves_the_archived_object(
    tmp_path, monkeypatch
):
    workspace, old_run, entry, expected_bytes, receipt_path = (
        _make_interrupted_workspace(tmp_path, monkeypatch)
    )
    interrupted_receipt_bytes = receipt_path.read_bytes()

    payload = _json_payload(_apply(workspace), 0)
    receipt = payload["receipt"]

    assert receipt["resumedFrom"] == old_run, (
        "the resumed run must name the interrupted receipt it continued from"
    )
    assert any(
        old_run in note and "status=running" in note for note in receipt["notes"]
    ), f"the interrupted stage is not reported in notes: {receipt['notes']!r}"
    _assert_resume_invariants(workspace, old_run, entry, expected_bytes, receipt)

    # The interrupted run's file is never touched by the new run (E-3).
    assert receipt_path.read_bytes() == interrupted_receipt_bytes, (
        "the resumed run rewrote another run's receipt file"
    )

    before = _tree_digest(workspace)
    clean = _json_payload(_dry_run(workspace), 0)
    assert clean["outcome"] == "clean"
    assert _tree_digest(workspace) == before


def _assert_resume_invariants(workspace, old_run, entry, expected_bytes, receipt):
    target = workspace / INTERRUPTED_TARGET
    assert target.is_file(), "the interrupted write was not completed"
    assert target.read_bytes() == expected_bytes, (
        "the resumed write did not restore the expected content"
    )
    archived = workspace / entry["archiveTo"]
    assert archived.exists() or archived.is_symlink(), (
        "the archived object was moved a second time"
    )
    carried = [
        archive
        for archive in receipt["archives"]
        if archive["path"] == INTERRUPTED_TARGET
    ]
    assert len(carried) == 1, (
        f"the resumed target gained {len(carried)} archive entries: {carried!r}"
    )
    assert carried[0]["archiveTo"] == entry["archiveTo"], (
        "the resumed run opened a new archive under its own run id"
    )
    resumed_item = next(
        item for item in receipt["items"] if item["target"] == INTERRUPTED_TARGET
    )
    assert resumed_item["status"] == "done"
    assert resumed_item["archiveTo"] == entry["archiveTo"]
    assert receipt["resumedFrom"] == old_run
    assert len(receipt["recover"]) == len(receipt["archives"])


# ---------------------------------------------------------------------------
# SC-006 mutation: re-moving the archived object turns the resume checks red
# ---------------------------------------------------------------------------


def test_mutation_re_moving_the_archived_object_turns_the_resume_checks_red(
    tmp_path, monkeypatch
):
    workspace, old_run, entry, expected_bytes, _receipt_path = (
        _make_interrupted_workspace(tmp_path, monkeypatch)
    )

    def re_move_then_write(ctx, item, archive_entry):
        # The forbidden shape: "resuming" by moving the already-archived object
        # back to the target instead of completing the write.
        archived = ctx.workspace / archive_entry["archiveTo"]
        shutil.move(str(archived), str(ctx.workspace / item.target))
        specify_cli._migrate_write_copy(ctx, item)
        item.archiveTo = archive_entry["archiveTo"]
        ctx.archives.append(dict(archive_entry))

    monkeypatch.setattr(
        specify_cli, "_migrate_resume_complete_write", re_move_then_write
    )

    payload = _json_payload(_apply(workspace), 0)

    with pytest.raises(AssertionError):
        _assert_resume_invariants(
            workspace, old_run, entry, expected_bytes, payload["receipt"]
        )
