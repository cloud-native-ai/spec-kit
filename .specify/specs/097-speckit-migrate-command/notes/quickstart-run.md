# Quickstart run — scenarios 1–5, real execution (2026-11-10)

**Task**: T045 (FR-023, DoD-9) · **Spec**: `097-speckit-migrate-command` · **Worktree**: `097-speckit-migrate-command` (base `1b2d998c6`)

## Execution form and disclosure

The installed `specify` CLI is the released 0.0.22 package, not this repository's source (tasks.md § Environment Prerequisites @ 2026-11-10). Every command below therefore invokes the **repository source**:

```bash
PYTHONPATH=src python3 -c "import sys; sys.argv[0]='specify'; from specify_cli import main; main()" migrate <options>
```

This substitution is the recorded one from § Environment Prerequisites (probe verified exit 0 @ 2026-11-10), restated here as that section requires.

Fixtures are built by the feature's declaration-driven builders (`tests/fixtures/migrate-097/builders.py`, FR-023): `demo` = `build_latest_project`, every `legacy-demo*` = `build_legacy_project`. The builder default assistant is `qoder` (its declared default), not scenario 0's `claude` init; the fixtures are equivalent projections of the installed assets. Scenario 2's apply needs the real second key, so it runs on a pty (stdlib `pty`, answer `y` when the prompt appears); every other run uses captured pipes, and non-interactive applies read `/dev/null` exactly as `< /dev/null` does.

Driver: `.specify/.tmp/pkg07/quickstart_driver.py` (temporary, git-ignored). Raw transcript: `.specify/.tmp/pkg07/quickstart-raw.txt`. Working root: `.specify/.tmp/pkg07/quickstart/` — each scenario tears its fixture down before the next.

## Scenario 1 — latest workspace: dry-run is `clean`, zero writes

```bash
PYTHONPATH=src python3 -c "import sys; sys.argv[0]='specify'; from specify_cli import main; main()" migrate --workspace demo
```

```text
migrate plan — mode=dry-run, workspace-kind=client, items=0
note: compat-links: instruction target .specify/instructions.md absent; skipped QODER.md
outcome: clean (exit 0)
pointer: goal/team archive migration stays with /speckit.goal migrate-archive
exit=0
tree_hash_before=76b68cc3e1084ab2ec910eee182724e5a4374fec9251bb2b5565c61448a3aef1
tree_hash_after=76b68cc3e1084ab2ec910eee182724e5a4374fec9251bb2b5565c61448a3aef1
tree_unchanged=True
receipt_files=0
receipts_dir_exists=False
teardown: rm -rf .specify/.tmp/pkg07/quickstart/demo -> exists=False
```

Verdict: exit 0, tree hash unchanged, no receipt file, no `.specify/memory/migrate/` directory created.

## Scenario 2 — legacy workspace: plan → apply → clean

Step 1 — dry-run, machine envelope:

```bash
PYTHONPATH=src python3 -c "import sys; sys.argv[0]='specify'; from specify_cli import main; main()" migrate --workspace legacy-demo --format json
```

```text
exit=1
outcome=planned exitCode=1
summary={"total": 11, "byDimension": {"templates-generated": 3, "anchor-layout": 2, "compat-links": 1, "mirror-consistency": 1, "migration-residue": 4}, "byDisposition": {"write": 2, "replace": 1, "archive": 8}}
workspaceKind=client mode=dry-run
tree_hash_before=0e779534a37f502fa7beb194b74800624a933794e577a4ba9be390c411ef764c
tree_hash_after=0e779534a37f502fa7beb194b74800624a933794e577a4ba9be390c411ef764c
tree_unchanged=True
receiptPath=None
receipt_files=False
```

All five dimensions carry at least one item; the dry-run wrote nothing.

Step 2 — apply on a pty, second key answered `y`:

```bash
PYTHONPATH=src python3 -c "import sys; sys.argv[0]='specify'; from specify_cli import main; main()" migrate --workspace legacy-demo --apply
```

```text
specify migrate: 9 destructive item(s) require the second key before they can be applied.
  templates-generated: .qoder/commands/speckit.converge.md [archive]
  templates-generated: .qoder/commands/speckit.taskstoissues.md [archive]
  templates-generated: .specify/templates/plan-template.md [replace]
  anchor-layout: .specify/memory/constitution.md [archive]
  anchor-layout: .specify/memory/features.md [archive]
  migration-residue: .specify/skills/agent-cli-setup [archive]
  migration-residue: .specify/skills/create-agent [archive]
  migration-residue: .specify/skills/docx-utils [archive]
  migration-residue: .specify/skills/web-test [archive]
Apply these destructive items now? [y/N]: y
migrate plan — mode=apply, workspace-kind=client, items=11
[templates-generated] (3)
  .qoder/commands/speckit.converge.md: registry-listed -> absent (archived, recoverable) [archive] (archive) evidence=src/specify_cli/__init__.py#plan_obsolete_framework_asset_removals:obsolete-command
  .qoder/commands/speckit.taskstoissues.md: registry-listed -> absent (archived, recoverable) [archive] (archive) evidence=src/specify_cli/__init__.py#plan_obsolete_framework_asset_removals:obsolete-command
  .specify/templates/plan-template.md: differs -> byte-equal to installed asset [replace] (replace) evidence=templates/plan-template.md
[anchor-layout] (2)
  .specify/memory/constitution.md: legacy-location -> moved-to: .specify/constitution.md [archive] (relocate) evidence=scripts/python/anchor-layout-migrate.py#--action check
  .specify/memory/features.md: legacy-location -> moved-to: .specify/features.md [archive] (relocate) evidence=scripts/python/anchor-layout-migrate.py#--action check
[compat-links] (1)
  .qoder/skills: missing -> symlink -> .specify/skills [write] (symlink) evidence=scripts/python/sanitize-utils.py#check_broken_symlinks
[mirror-consistency] (1)
  .specify/scripts/python/flow-class-check.py: missing -> byte-equal to installed asset [write] (copy) evidence=scripts/python/flow-class-check.py
[migration-residue] (4)
  .specify/skills/agent-cli-setup: registry-listed -> absent (archived, recoverable) [archive] (archive) evidence=src/specify_cli/__init__.py#plan_obsolete_framework_asset_removals:obsolete-skill-dir
  .specify/skills/create-agent: flat duplicate of a nested internal skill -> absent (archived, recoverable) [archive] (archive) evidence=src/specify_cli/__init__.py#plan_flat_internal_skill_migrations:remove-stale
  .specify/skills/docx-utils: registry-listed -> absent (archived, recoverable) [archive] (archive) evidence=src/specify_cli/__init__.py#plan_obsolete_framework_asset_removals:obsolete-skill-dir
  .specify/skills/web-test: registry-listed -> absent (archived, recoverable) [archive] (archive) evidence=src/specify_cli/__init__.py#plan_obsolete_framework_asset_removals:obsolete-skill-dir
note: compat-links: instruction target .specify/instructions.md absent; skipped QODER.md
outcome: applied (exit 0)
pointer: goal/team archive migration stays with /speckit.goal migrate-archive
receipt: .specify/memory/migrate/receipts/20261110T152449Z-e61509ba.json
exit=0
second_key_used=pty
receipt_file=.specify/memory/migrate/receipts/20261110T152449Z-e61509ba.json
receipt.status=completed outcome=applied exitCode=0
items_total=11 archives_total=9
recover_lines=9
archive_exists[relocated] .specify/constitution.md -> True
archive_exists[relocated] .specify/features.md -> True
archive_exists[archived] .specify/archive/migrate/20261110T152449Z-e61509ba/.qoder/commands/speckit.converge.md -> True
archive_exists[archived] .specify/archive/migrate/20261110T152449Z-e61509ba/.qoder/commands/speckit.taskstoissues.md -> True
archive_exists[replaced] .specify/archive/migrate/20261110T152449Z-e61509ba/templates/plan-template.md -> True
```

Step 3 — recheck:

```bash
PYTHONPATH=src python3 -c "import sys; sys.argv[0]='specify'; from specify_cli import main; main()" migrate --workspace legacy-demo
```

```text
migrate plan — mode=dry-run, workspace-kind=client, items=0
note: compat-links: instruction target .specify/instructions.md absent; skipped QODER.md
outcome: clean (exit 0)
pointer: goal/team archive migration stays with /speckit.goal migrate-archive
exit=0
tree_hash_before=ca20b9c3d814755d37884294cabf4d970e0b2ab4b7cfce725e061bc30de74085
tree_hash_after=ca20b9c3d814755d37884294cabf4d970e0b2ab4b7cfce725e061bc30de74085
tree_unchanged=True
outcome_token=clean
teardown: rm -rf .specify/.tmp/pkg07/quickstart/legacy-demo -> exists=False
```

Verdict: exits 1 → 0 → 0; every receipt-named archive path exists; the post-apply recheck is `clean` with zero writes.

## Scenario 3 — non-interactive apply: destructive blocked, reversible executed

```bash
PYTHONPATH=src python3 -c "import sys; sys.argv[0]='specify'; from specify_cli import main; main()" migrate --workspace legacy-demo-noninteractive --apply < /dev/null
```

```text
migrate plan — mode=apply, workspace-kind=client, items=11
[templates-generated] (3)
  .qoder/commands/speckit.converge.md: registry-listed -> absent (archived, recoverable) [blocked] (none) reason=destructive action requires the second key (interactive confirmation); none available
  .qoder/commands/speckit.taskstoissues.md: registry-listed -> absent (archived, recoverable) [blocked] (none) reason=destructive action requires the second key (interactive confirmation); none available
  .specify/templates/plan-template.md: differs -> byte-equal to installed asset [blocked] (none) reason=destructive action requires the second key (interactive confirmation); none available
[anchor-layout] (2)
  .specify/memory/constitution.md: legacy-location -> moved-to: .specify/constitution.md [blocked] (none) reason=destructive action requires the second key (interactive confirmation); none available
  .specify/memory/features.md: legacy-location -> moved-to: .specify/features.md [blocked] (none) reason=destructive action requires the second key (interactive confirmation); none available
[compat-links] (1)
  .qoder/skills: missing -> symlink -> .specify/skills [write] (symlink) evidence=scripts/python/sanitize-utils.py#check_broken_symlinks
[mirror-consistency] (1)
  .specify/scripts/python/flow-class-check.py: missing -> byte-equal to installed asset [write] (copy) evidence=scripts/python/flow-class-check.py
[migration-residue] (4)
  .specify/skills/agent-cli-setup: registry-listed -> absent (archived, recoverable) [blocked] (none) reason=destructive action requires the second key (interactive confirmation); none available
  .specify/skills/create-agent: flat duplicate of a nested internal skill -> absent (archived, recoverable) [blocked] (none) reason=destructive action requires the second key (interactive confirmation); none available
  .specify/skills/docx-utils: registry-listed -> absent (archived, recoverable) [blocked] (none) reason=destructive action requires the second key (interactive confirmation); none available
  .specify/skills/web-test: registry-listed -> absent (archived, recoverable) [blocked] (none) reason=destructive action requires the second key (interactive confirmation); none available
note: compat-links: instruction target .specify/instructions.md absent; skipped QODER.md
outcome: blocked (exit 3)
pointer: goal/team archive migration stays with /speckit.goal migrate-archive
next: review refused/blocked items and re-run --apply
exit=3
confirmation_prompt_absent=True
receipt.status=completed outcome=blocked exitCode=3
item_status_counts={"blocked": 9, "done": 2}
archives_total=0
teardown: rm -rf .specify/.tmp/pkg07/quickstart/legacy-demo-noninteractive -> exists=False
```

Verdict: no confirmation prompt; 9 destructive items `blocked` and zero executed; the 2 reversible items (`symlink`, `copy`) ran; receipt `outcome=blocked`, exit 3, zero archives.

## Scenario 4 — conflict and interruption

### 4a. Conflict: refused, both candidates named, no winner picked

Dry-run:

```bash
PYTHONPATH=src python3 -c "import sys; sys.argv[0]='specify'; from specify_cli import main; main()" migrate --workspace legacy-demo-conflict --format json
```

```text
exit=1
outcome=planned
refuse_items=1
refuse.target=.specify/memory/features.md
refuse.reason=conflict — existing candidate: .specify/memory/features.md; expected candidate: .specify/features.md; anchor target already exists; both candidates are kept
tree_unchanged=True
```

Apply (pty, `y`):

```text
specify migrate: 8 destructive item(s) require the second key before they can be applied.
...
Apply these destructive items now? [y/N]: y
migrate plan — mode=apply, workspace-kind=client, items=11
  .specify/memory/features.md: .specify/memory/features.md -> .specify/features.md [refuse] (none) reason=conflict — existing candidate: .specify/memory/features.md; expected candidate: .specify/features.md; anchor target already exists; both candidates are kept
outcome: blocked (exit 3)
exit=3
second_key_used=pty
receipt.outcome=blocked exitCode=3
refused_items=1 statuses=['refused']
conflicting_target_bytes_unchanged=True
legacy_anchor_bytes_unchanged=True
refused_target_got_archive=False
teardown: rm -rf .specify/.tmp/pkg07/quickstart/legacy-demo-conflict -> exists=False
```

Verdict: dry-run exit 1 names both candidates; apply exit 3, `refused`, neither candidate moved or overwritten, no archive entry for the refused target.

### 4b. Interrupted apply: second run resumes, no second move

```text
$ interruption setup: delete .specify/templates/plan-template.md and mark the first receipt status=running
exit=0
first_apply_exit=0 second_key_used=pty
interrupted_run=20261110T152509Z-28f484cb
archive_entry=replaced .specify/archive/migrate/20261110T152509Z-28f484cb/templates/plan-template.md exists=True
target_deleted=True
```

Second apply:

```bash
PYTHONPATH=src python3 -c "import sys; sys.argv[0]='specify'; from specify_cli import main; main()" migrate --workspace legacy-demo-interrupted --apply
```

```text
migrate plan — mode=apply, workspace-kind=client, items=1
[templates-generated] (1)
  .specify/templates/plan-template.md: missing -> byte-equal to installed asset [write] (copy) evidence=templates/plan-template.md
note: resume: interrupted apply 20261110T152509Z-28f484cb (status=running) — recorded stage 11/11 items done, 9 archived object(s) kept; continuing from that receipt
note: compat-links: instruction target .specify/instructions.md absent; skipped QODER.md
outcome: applied (exit 0)
pointer: goal/team archive migration stays with /speckit.goal migrate-archive
receipt: .specify/memory/migrate/receipts/20261110T152511Z-9d2ae189.json
exit=0
second_key_used=pty-no-prompt
new_receipt=20261110T152511Z-9d2ae189.json
resumedFrom=20261110T152509Z-28f484cb (old_run=20261110T152509Z-28f484cb)
resume_note=['resume: interrupted apply 20261110T152509Z-28f484cb (status=running) — recorded stage 11/11 items done, 9 archived object(s) kept; continuing from that receipt']
target_restored=True bytes_match=True
archived_object_still_present=True
carried_archive_entries=1 archiveTo_match=True
resumed_item.status=done
old_receipt_untouched=True
teardown: rm -rf .specify/.tmp/pkg07/quickstart/legacy-demo-interrupted -> exists=False
```

Verdict: the second run reports the interrupted receipt in `resumedFrom` and `notes`, completes the missing write byte-identically, keeps the archived object in place (one carried archive entry, same `archiveTo`), and never modifies the interrupted run's receipt file.

## Scenario 5 — agent session `/speckit.migrate`

Template command surface (parsed from `templates/commands/migrate.md`, bash/sh fences):

```text
declared_commands=["specify migrate --format json", "specify migrate --apply"]
```

The template declares exactly the two CLI entries and no inspection step. The template-declared dry-run was executed twice on one legacy fixture (`--workspace legacy-demo-agent` supplied as the documented optional parameter) and compared:

```text
dry_run_exits=1,1 outcomes=planned,planned
items_equal=True summary_equal=True
summary={"total": 11, "byDimension": {"templates-generated": 3, "anchor-layout": 2, "compat-links": 1, "mirror-consistency": 1, "migration-residue": 4}, "byDisposition": {"write": 2, "replace": 1, "archive": 8}}
tree_unchanged=True
```

The template-declared apply in a non-interactive session:

```bash
PYTHONPATH=src python3 -c "import sys; sys.argv[0]='specify'; from specify_cli import main; main()" migrate --workspace legacy-demo-agent --apply < /dev/null
```

```text
... (same blocked item set as scenario 3)
outcome: blocked (exit 3)
exit=3
receipt.outcome=blocked exitCode=3
template_transcription_guidance_present=True
teardown: rm -rf .specify/.tmp/pkg07/quickstart/legacy-demo-agent -> exists=False
```

Verdict: the template's declared surface is the two CLI commands only; the plan is deterministic across runs (identical `items` + `summary`); in a non-interactive session the outcome is `blocked` exit 3 and the template carries the "transcribe honestly, MUST NOT claim success" guidance (`templates/commands/migrate.md` § Delegation step 2). The full two-entry equivalence reading is in `test-evidence/us4-equivalence.txt` (T040).

## Summary

| Scenario | Command exits | Verdict |
|----------|---------------|---------|
| 1 — latest dry-run | 0 | clean, zero writes, no receipt |
| 2 — legacy plan/apply/recheck | 1 → 0 → 0 | planned → applied (9 archives, all recoverable) → clean zero-write |
| 3 — non-interactive apply | 3 | blocked, no prompt, destructive 9 blocked / reversible 2 done |
| 4a — conflict | 1 → 3 | refuse names both candidates; no overwrite, no archive |
| 4b — interrupted apply | 0 → 0 | resumed from `status=running` receipt; target restored; archive not re-moved |
| 5 — agent session | 1,1 → 3 | template = two CLI entries; deterministic plan; blocked transcribed honestly |

Driver verdict: `all_pass=True`. Every fixture was torn down after its scenario (`exists=False`).
