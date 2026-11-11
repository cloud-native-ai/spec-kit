"""Integration: US2 safety — archive-first auto-execution, merge preservation, structural refusal, user-content protection (097 T023).

Green claims: contracts/migrate-cli.md C-5 (single `--apply` authorization;
archive-first items execute automatically in every environment; only items
with no archive path are blocked) and contracts/migrate-engine.md C-6
(owner-referenced destructive criteria, old/new anchors merge and preserve both
sides, an unmergeable structural target refuses and names both candidates, user
content is never a residue candidate and replacement archives first).

Mutation discipline (FR-024 / SC-002 / SC-005 / SC-008): every safety
assertion is proven red-able inside this suite. Removing the archive step,
injecting a full delete, picking one side of a merge, and replacing the symlink
probe with a workspace-writing variant must each make the corresponding
assertion fail — a mutation that stays green means the assertion has no
discriminative power. The existence-only weakening is a check-power drill over
the same reading: the weakened form stays green while the byte assertion reds.
"""

import hashlib
import importlib.util
import json
import os
import shutil
import tempfile
from pathlib import Path

import pytest

import specify_cli

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[2]
BUILDERS_PATH = ROOT / "tests" / "fixtures" / "migrate-097" / "builders.py"

USER_SKILL = Path(".specify") / "skills" / "user-acme-notes"
USER_SKILL_FILE = USER_SKILL / "SKILL.md"
USER_SITE_FILE = USER_SKILL / "site" / "data.json"
FRAMEWORK_SITE_FILE = (
    Path(".specify") / "skills" / "internal" / "create-agent" / "site" / "cache.bin"
)
USER_MEMORY_FILE = Path(".specify") / "memory" / "user-notes.md"
HAND_EDITED_TEMPLATE = Path(".specify") / "templates" / "plan-template.md"
FIXTURE_EDIT_MARKER = b"<!-- fixture edit -->"


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _builders():
    spec = importlib.util.spec_from_file_location(
        "_migrate_us2_builders", BUILDERS_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _invoke(args, input_text=None):
    from typer.testing import CliRunner

    return CliRunner().invoke(specify_cli.app, args, input=input_text)


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            digest.update(f"L {rel} -> {os.readlink(path)}\n".encode("utf-8"))
        elif path.is_dir():
            digest.update(f"D {rel}\n".encode("utf-8"))
        else:
            digest.update(f"F {rel} {hashlib.sha256(path.read_bytes()).hexdigest()}\n".encode("utf-8"))
    return digest.hexdigest()


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


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _add_user_content(workspace: Path) -> dict:
    """User-owned content that must survive a full convergence untouched (FR-016).

    A user-built skill, its runtime ``site/`` data, runtime data under a
    framework skill, and a hand-written memory file. Returns rel-path -> sha256.
    """
    (workspace / USER_SKILL).mkdir(parents=True, exist_ok=True)
    (workspace / USER_SKILL_FILE).write_text(
        "# user-acme-notes\n\nA user-built skill, never a residue candidate.\n",
        encoding="utf-8",
    )
    (workspace / USER_SITE_FILE).parent.mkdir(parents=True, exist_ok=True)
    (workspace / USER_SITE_FILE).write_text('{"user": "site-data"}\n', encoding="utf-8")
    (workspace / FRAMEWORK_SITE_FILE).parent.mkdir(parents=True, exist_ok=True)
    (workspace / FRAMEWORK_SITE_FILE).write_bytes(b"framework-skill runtime cache")
    (workspace / USER_MEMORY_FILE).write_text(
        "# user notes\n\nPersonal working notes.\n", encoding="utf-8"
    )
    return _user_content_snapshot(workspace)


def _legacy_with_user_content(dest: Path) -> tuple:
    workspace = _builders().build_legacy_project(dest)
    snapshot = _add_user_content(workspace)
    return workspace, snapshot


def _user_content_snapshot(workspace: Path) -> dict:
    rels = (
        USER_SKILL_FILE,
        USER_SITE_FILE,
        FRAMEWORK_SITE_FILE,
        USER_MEMORY_FILE,
    )
    return {rel.as_posix(): _file_sha256(workspace / rel) for rel in rels}


def _user_content_exists(workspace: Path, snapshot: dict) -> bool:
    """The existence-only reading (the weakened form proven inanimate below)."""
    return all((workspace / rel).exists() for rel in snapshot)


def _assert_user_content_intact(workspace: Path, snapshot: dict):
    for rel, before in snapshot.items():
        path = workspace / rel
        assert path.exists(), f"user content disappeared: {rel}"
        assert _file_sha256(path) == before, (
            f"user content bytes changed: {rel} ({before} -> {_file_sha256(path)})"
        )


def _destructive_keys(payload) -> set:
    """(dimension, target) keys of the dry-run plan's destructive items."""
    return {
        (item["dimension"], item["target"])
        for item in payload["items"]
        if item["disposition"] in specify_cli.MIGRATE_DESTRUCTIVE_DISPOSITIONS
    }


def _digests(workspace: Path, keys) -> dict:
    return {key: specify_cli._migrate_digest(workspace / key[1]) for key in keys}


def _assert_auto_applied_with_archives(result, workspace, snapshot):
    """The C-5 reading: archive-first items execute automatically and are recoverable."""
    payload = _json_payload(result, 0)
    assert payload["outcome"] == "applied"
    assert payload["exitCode"] == 0
    receipt = payload["receipt"]
    assert receipt["status"] == "completed"
    assert all(item["status"] == "done" for item in receipt["items"]), [
        (item["target"], item["status"]) for item in receipt["items"]
    ]
    _assert_archives_exist_and_enumerated(payload, workspace)
    _assert_user_content_intact(workspace, snapshot)


def _assert_archives_exist_and_enumerated(payload, workspace: Path):
    """Every executed destructive item has one receipt entry recoverable on disk."""
    receipt = payload["receipt"]
    archives = receipt["archives"]
    executed = [
        item
        for item in receipt["items"]
        if item["disposition"] in specify_cli.MIGRATE_DESTRUCTIVE_DISPOSITIONS
        and item["status"] == "done"
    ]
    assert executed, "fixture executed no destructive item"
    archived_paths = {entry["path"] for entry in archives}
    for item in executed:
        assert item["target"] in archived_paths, (
            f"executed destructive item has no archive entry: {item['target']}"
        )
    assert len(receipt["recover"]) == len(archives), (
        "every archive entry needs exactly one recovery path"
    )
    for entry in archives:
        located = workspace / entry["archiveTo"]
        assert located.exists() or located.is_symlink(), (
            f"receipt names a missing archive object: {entry}"
        )
        assert entry["change"] in (
            "replaced", "archived", "removed-stale", "relocated",
            "merged", "removed-duplicate",
        ), entry
        assert entry["digest"], entry
        assert entry["digest"] == specify_cli._migrate_digest(located), (
            f"archived object bytes differ from the receipt digest: {entry}"
        )
    for line in receipt["recover"]:
        assert any(entry["archiveTo"] in line for entry in archives), (
            f"recovery line names no archive entry: {line!r}"
        )


# ---------------------------------------------------------------------------
# Destructive classifier and the symlink-support probe (T024 / T026 surfaces)
# ---------------------------------------------------------------------------


def test_destructive_classifier_projects_the_confirmation_gates_owner():
    segment = (ROOT / "src" / "specify_cli" / "__init__.py").read_text(encoding="utf-8")
    assert (
        specify_cli.MIGRATE_DESTRUCTIVE_CRITERIA_POINTER
        == ".specify/shared/guidelines/confirmation-gates.md"
    )
    assert specify_cli.MIGRATE_DESTRUCTIVE_CRITERIA_POINTER in segment, (
        "the classifier must point at the destructive-criteria owner, not restate it"
    )

    def item(disposition):
        if disposition == "refuse":
            return specify_cli.make_refuse_item(
                "compat-links", ".qoder/skills",
                current=".qoder/skills", expected="symlink -> .specify/skills",
            )
        if disposition == "blocked":
            return specify_cli.make_blocked_item(
                "migration-residue", ".specify/skills/x",
                current="registry-listed", expected="absent (archived, recoverable)",
            )
        return specify_cli.MigrateItem(
            "templates-generated", ".specify/templates/x.md",
            "differs", "byte-equal to installed asset", disposition,
        )

    for destructive in ("archive", "replace"):
        assert specify_cli.migrate_is_destructive(item(destructive)) is True
    for reversible in ("write", "converged", "refuse", "blocked"):
        assert specify_cli.migrate_is_destructive(item(reversible)) is False


def _fixed_temporary_directory(path: Path):
    """A TemporaryDirectory stand-in that hands the probe a known scratch path.

    The real object deletes what the probe creates on exit, so its write would
    stay unobservable; the stand-in keeps the link in place and lets the
    assertion prove *where* the probe wrote, not merely that nothing moved.
    """

    class _FixedDirectory:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return str(path)

        def __exit__(self, *exc_info):
            return False

    return _FixedDirectory


def _assert_probe_is_workspace_isolated(workspace: Path, sentinel: Path, probe):
    """The zero-write reading, observable on both sides.

    The probe must create its link inside the transient directory it was
    handed (``sentinel``) and leave the workspace digest byte-identical. A
    probe that scribbles into the current directory — chdir'd to the
    workspace by the caller — moves the digest; a probe that stops using its
    transient directory leaves the sentinel empty. Either regression reds.
    """
    before = _tree_digest(workspace)
    verdict = probe()
    assert isinstance(verdict, bool), verdict
    assert (sentinel / "link").is_symlink(), (
        "the probe created no link inside the transient directory it was handed"
    )
    assert os.readlink(sentinel / "link") == "target"
    assert _tree_digest(workspace) == before, (
        "the symlink-support probe wrote to the workspace"
    )


def test_symlink_support_probe_is_zero_write(tmp_path, monkeypatch):
    workspace = _builders().build_legacy_project(tmp_path / "legacy")
    sentinel = tmp_path / "probe-scratch"
    sentinel.mkdir()
    monkeypatch.setattr(
        tempfile, "TemporaryDirectory", _fixed_temporary_directory(sentinel)
    )
    monkeypatch.chdir(workspace)

    _assert_probe_is_workspace_isolated(
        workspace, sentinel, specify_cli.migrate_symlink_supported
    )


def test_mutation_workspace_writing_probe_turns_the_zero_write_check_red(
    tmp_path,
):
    workspace = _builders().build_legacy_project(tmp_path / "legacy")
    sentinel = tmp_path / "probe-scratch"
    sentinel.mkdir()

    def workspace_writing_probe():
        # The injected variant keeps its transient link but also writes one
        # stray link into the workspace — the regression the guard exists for.
        os.symlink("target", str(sentinel / "link"))
        os.symlink("target", str(workspace / ".specify" / "probe-link"))
        return True

    with pytest.raises(AssertionError, match="wrote to the workspace"):
        _assert_probe_is_workspace_isolated(
            workspace, sentinel, workspace_writing_probe
        )


# ---------------------------------------------------------------------------
# C-5: non-interactive apply executes archive-first items and never prompts
# ---------------------------------------------------------------------------


def test_noninteractive_apply_executes_archive_first_items_and_archives_are_recoverable(
    tmp_path, monkeypatch
):
    workspace, snapshot = _legacy_with_user_content(tmp_path / "legacy")
    dry = _json_payload(_dry_run(workspace), 1)
    assert _destructive_keys(dry), "fixture planned no destructive item"
    hand_edited_before = _file_sha256(workspace / HAND_EDITED_TEMPLATE)
    assert FIXTURE_EDIT_MARKER in (workspace / HAND_EDITED_TEMPLATE).read_bytes()

    monkeypatch.setattr(specify_cli, "migrate_symlink_supported", lambda: True)
    confirm_calls = []
    monkeypatch.setattr(
        specify_cli.typer, "confirm", lambda *a, **kw: confirm_calls.append(a) or True
    )

    result = _apply(workspace)

    assert confirm_calls == [], "an archive-first apply must not prompt"
    _assert_auto_applied_with_archives(result, workspace, snapshot)

    payload = _json_payload(result, 0)
    hand_edited_entry = next(
        entry
        for entry in payload["receipt"]["archives"]
        if entry["path"] == HAND_EDITED_TEMPLATE.as_posix()
    )
    archived_copy = workspace / hand_edited_entry["archiveTo"]
    assert _file_sha256(archived_copy) == hand_edited_before, (
        "the replaced user-edited content was not archived byte-identically"
    )
    assert FIXTURE_EDIT_MARKER not in (workspace / HAND_EDITED_TEMPLATE).read_bytes()


# ---------------------------------------------------------------------------
# C-6 / SC-005: a real/real anchor conflict is merged, never silently won
# ---------------------------------------------------------------------------


def test_real_anchor_conflict_is_merged_and_preserves_both_candidates(
    tmp_path, monkeypatch
):
    workspace = _builders().build_legacy_project(tmp_path / "conflict")
    legacy_anchor = workspace / ".specify" / "memory" / "features.md"
    target = workspace / ".specify" / "features.md"
    legacy_anchor.write_text(
        "# Legacy registry\n\n**Last Updated**: 2026-01-01\n"
        "**Total Features**: 2\n\n| ID | Name |\n|----|------|\n"
        "| 001 | Legacy-one |\n| 903 | Legacy-only |\n",
        encoding="utf-8",
    )
    target.write_text(
        "# Current registry\n\n**Last Updated**: 2026-02-01\n"
        "**Total Features**: 2\n\n| ID | Name |\n|----|------|\n"
        "| 001 | Current-one |\n| 002 | Current-two |\n",
        encoding="utf-8",
    )

    dry = _json_payload(_dry_run(workspace), 1)
    merges = [
        item
        for item in dry["items"]
        if item["dimension"] == "anchor-layout"
        and item["disposition"] == "replace"
        and item["mechanism"] == "anchor-engine"
        and "features-table-union" in item["expected"]
    ]
    assert merges, f"the conflict fixture produced no merge item: {dry['items']}"

    monkeypatch.setattr(specify_cli, "migrate_symlink_supported", lambda: True)
    payload = _json_payload(_apply(workspace), 0)

    merged = target.read_text(encoding="utf-8")
    assert "Current-one" in merged and "Current-two" in merged
    assert "Legacy-only" in merged, "the legacy-only row was dropped"
    assert "| 001 | Current-one |" in merged, "the target row must win on a duplicate id"
    assert "Legacy-one" not in merged, "a duplicate legacy row must be archived, not appended"
    assert "**Total Features**: 3" in merged
    assert "**Last Updated**: 2026-02-01" in merged

    archived_paths = {entry["path"] for entry in payload["receipt"]["archives"]}
    assert ".specify/memory/features.md" in archived_paths
    assert ".specify/features.md" in archived_paths
    for entry in payload["receipt"]["archives"]:
        if entry["path"] in archived_paths:
            assert (workspace / entry["archiveTo"]).exists(), entry


def test_real_prose_anchor_conflict_is_merged_with_marker(tmp_path, monkeypatch):
    workspace = _builders().build_legacy_project(tmp_path / "conflict-prose")
    legacy_anchor = workspace / ".specify" / "memory" / "constitution.md"
    target = workspace / ".specify" / "constitution.md"
    legacy_anchor.write_text(
        "# Legacy constitution\n\nLegacy principle.\n", encoding="utf-8"
    )
    target.write_text(
        "# Current constitution\n\nCurrent principle.\n", encoding="utf-8"
    )

    dry = _json_payload(_dry_run(workspace), 1)
    merges = [
        item
        for item in dry["items"]
        if item["dimension"] == "anchor-layout"
        and item["disposition"] == "replace"
        and "append-marker" in item["expected"]
    ]
    assert merges, f"the prose conflict produced no merge item: {dry['items']}"

    monkeypatch.setattr(specify_cli, "migrate_symlink_supported", lambda: True)
    _json_payload(_apply(workspace), 0)

    merged = target.read_text(encoding="utf-8")
    assert "Current principle." in merged
    assert "Legacy principle." in merged
    assert "specify-migrate: legacy anchor" in merged
    assert not legacy_anchor.exists(), "the merged legacy original must be archived away"


# ---------------------------------------------------------------------------
# C-6 / SC-008: user content is never a candidate; hand edits stay recoverable
# ---------------------------------------------------------------------------


def test_user_content_never_becomes_a_candidate_and_hand_edits_stay_recoverable(
    tmp_path, monkeypatch
):
    workspace, snapshot = _legacy_with_user_content(tmp_path / "legacy")
    dry = _json_payload(_dry_run(workspace), 1)
    targets = {item["target"] for item in dry["items"]}
    for rel in snapshot:
        assert rel not in targets, f"user content became a migration candidate: {rel}"
    assert not any("/site/" in f"/{target}/" for target in targets), (
        f"runtime site/ data became a candidate: {sorted(targets)}"
    )
    hand_edited = next(
        item for item in dry["items"] if item["target"] == HAND_EDITED_TEMPLATE.as_posix()
    )
    assert hand_edited["disposition"] == "replace", (
        "a hand-edited framework file must be replaced (archived first), never archived as residue"
    )
    assert hand_edited["mechanism"] == "replace"

    hand_edited_before = _file_sha256(workspace / HAND_EDITED_TEMPLATE)
    monkeypatch.setattr(specify_cli, "migrate_symlink_supported", lambda: True)
    payload = _json_payload(_apply(workspace), 0)

    _assert_user_content_intact(workspace, snapshot)
    entry = next(
        entry
        for entry in payload["receipt"]["archives"]
        if entry["path"] == HAND_EDITED_TEMPLATE.as_posix()
    )
    assert _file_sha256(workspace / entry["archiveTo"]) == hand_edited_before


# ---------------------------------------------------------------------------
# C-6 / SC-008: platform without symlink support refuses instead of crashing
# ---------------------------------------------------------------------------


def test_platform_without_symlink_support_refuses_with_reason_instead_of_crashing(
    tmp_path, monkeypatch
):
    workspace = _builders().build_legacy_project(tmp_path / "legacy")
    monkeypatch.setattr(specify_cli, "migrate_symlink_supported", lambda: False)

    dry_result = _dry_run(workspace)
    dry = _json_payload(dry_result, 1)
    platform_items = [
        item
        for item in dry["items"]
        if item["dimension"] == "compat-links" and item["disposition"] == "refuse"
    ]
    assert platform_items, (
        "a host without symlink support must degrade to refuse items, not crash"
    )
    for item in platform_items:
        assert item["status"] == "refused"
        assert "platform-no-symlink" in item["reason"]
        assert item["current"] in item["reason"] and item["expected"] in item["reason"]

    payload = _json_payload(_apply(workspace), 3)

    assert payload["outcome"] == "blocked"
    assert all(
        item["status"] == "refused"
        for item in payload["items"]
        if item["dimension"] == "compat-links"
    )
    assert not (workspace / ".qoder" / "skills").exists(), (
        "no symlink may be created on an unsupported host"
    )


# ---------------------------------------------------------------------------
# Mutation 1: picking one side of a merge must turn the both-sides check red
# ---------------------------------------------------------------------------


def _assert_merge_preserves_both(merged_text: str) -> None:
    assert "Current principle." in merged_text
    assert "Legacy principle." in merged_text


def test_mutation_picking_one_side_turns_the_merge_check_red():
    with pytest.raises(AssertionError):
        _assert_merge_preserves_both("# Current constitution only\n")


# ---------------------------------------------------------------------------
# Mutation 2: removing the archive step must turn the archive check red
# ---------------------------------------------------------------------------


def test_mutation_removing_the_archive_step_turns_the_archive_check_red(
    tmp_path, monkeypatch
):
    workspace = _builders().build_legacy_project(tmp_path / "legacy")

    def archive_without_archiving(ctx, item, change):
        source = ctx.workspace / item.target
        digest = specify_cli._migrate_digest(source)
        if source.is_dir() and not source.is_symlink():
            shutil.rmtree(source)
        else:
            source.unlink()
        item.status = "done"
        item.archiveTo = (
            f".specify/archive/migrate/{ctx.run_id}/ghost/{Path(item.target).name}"
        )
        return {
            "path": item.target,
            "archiveTo": item.archiveTo,
            "change": change,
            "digest": digest,
        }

    monkeypatch.setattr(specify_cli, "migrate_symlink_supported", lambda: True)
    monkeypatch.setattr(
        specify_cli, "_migrate_archive_object", archive_without_archiving
    )

    payload = _json_payload(_apply(workspace), 0)

    with pytest.raises(AssertionError):
        _assert_archives_exist_and_enumerated(payload, workspace)


# ---------------------------------------------------------------------------
# Mutation 3: injecting a full delete must turn archive + user-content checks red
# ---------------------------------------------------------------------------


def test_mutation_injecting_full_delete_turns_the_archive_and_user_content_checks_red(
    tmp_path, monkeypatch
):
    workspace, snapshot = _legacy_with_user_content(tmp_path / "legacy")

    def full_delete(ctx, item):
        if item.status != "planned":
            return
        if item.dimension == "anchor-layout" or item.mechanism == "mirror-engine":
            return
        if item.dimension == "migration-residue":
            # The injected "full delete" disposal: wipe the residue surface
            # wholesale instead of archiving each object.
            shutil.rmtree(ctx.workspace / ".specify" / "skills", ignore_errors=True)
            item.status = "done"
            return
        target = ctx.workspace / item.target
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        elif target.is_symlink() or target.exists():
            target.unlink()
        item.status = "done"

    monkeypatch.setattr(specify_cli, "migrate_symlink_supported", lambda: True)
    monkeypatch.setattr(specify_cli, "_migrate_execute_item", full_delete)

    payload = _json_payload(_apply(workspace), 0)

    with pytest.raises(AssertionError):
        _assert_archives_exist_and_enumerated(payload, workspace)
    with pytest.raises(AssertionError):
        _assert_user_content_intact(workspace, snapshot)


# ---------------------------------------------------------------------------
# Mutation 4: weakening to existence-only would miss content corruption
# ---------------------------------------------------------------------------


def test_mutation_weakening_to_existence_only_would_miss_content_corruption(
    tmp_path,
):
    workspace, snapshot = _legacy_with_user_content(tmp_path / "legacy")
    assert _user_content_exists(workspace, snapshot)

    victim = workspace / USER_SKILL_FILE
    victim.write_text("# user skill, silently rewritten\n", encoding="utf-8")

    assert _user_content_exists(workspace, snapshot), (
        "the existence-only reading must still pass on corrupted content — "
        "that is exactly why the byte check is required"
    )
    with pytest.raises(AssertionError):
        _assert_user_content_intact(workspace, snapshot)
