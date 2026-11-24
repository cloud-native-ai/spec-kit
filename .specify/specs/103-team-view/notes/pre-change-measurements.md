# Pre-change measurements — 103-team-view (T001)

- Captured: 2026-11-24 (session at ~03:55Z–03:57Z UTC)
- Workspace: `/storage/project/cloud-native-ai/spec-kit`, branch `103-team-view`,
  entry commit `1ed62808c` (checklist stage; analyze passed with 0 CRITICAL / 0 HIGH)
- Purpose: freeze the comparison surface for every later reading row. A quantity not
  re-measured here stays `not-evaluated` downstream; no later row may inherit the
  tasks.md premise values without re-measuring against this file.
- `notes/` and `test-evidence/` were created by this task (FR-021).

## Archive size and shape (re-measured, tasks.md § Premises)

| Quantity | Command | Reading (2026-11-24) |
|----------|---------|----------------------|
| team directories | `ls -d .specify/teams/*/ \| wc -l` | **20** |
| `team.md` files | `ls .specify/teams/*/team.md \| wc -l` | **20** (both readings agree; `.work/` is not a team root) |
| run reports, all `*.md` | `ls .specify/teams/*/runs/*.md \| wc -l` | **46** |
| run reports, contract name `*-report.md` | `ls .specify/teams/*/runs/*-report.md \| wc -l` | **41** — the 5 non-conforming names are the `未识别` branch's live source |
| item ledgers | `ls .specify/teams/*/items.jsonl \| wc -l` | **5**, one zero-line file (`viz-skill-arena`) — `为空` exists live |
| ledger line counts | `wc -l` per file | `viz-skill-arena` 0 · `draw-diagram-interactive` 3 · `post-refactor-mechanism-integrity` 3 · `command-logic-as-classified-skills` 5 · `skill-layer-install-separation` 6 |
| continuous spines | `ls .specify/teams/*/constraints.md \| wc -l` | **3** |
| example teams | `test -d <path>` | `.specify/teams/cws-workspace-cluster/` **present**; `.specify/teams/086-efficient-test-execution/` **present** |

## Stale literal and template premises

| Quantity | Command | Reading (2026-11-24) |
|----------|---------|----------------------|
| `exactly three modes` per file | `grep -c 'exactly three modes' <file>` (each file separately) | `templates/commands/team.md` **1** · `docs/reference/commands/team.md` **1** · `.claude/commands/speckit.team.md` **1** · `.github/prompts/speckit.team.prompt.md` **1** · `.qoder/commands/speckit.team.md` **1** · `.opencode/command/speckit.team.md` **1** (6 files × 1) |
| `argument-hint` in the template | `grep -c 'argument-hint' templates/commands/team.md` | **0** (grep exits 1 on zero matches; `\|\| true` used) — the key is new to this file; `anchor.md` / `goal.md` are the sibling form |
| docs false assertions | `grep -c -F <literal> docs/reference/commands/team.md` | `never executes before you confirm` **1** · `Only then does orchestration run` **1** · `Declining stops without executing` **1** |

## To-be-built deliverables (all absent before this package)

Command: `test -e <path>` for each (2026-11-24)

| Path | State |
|------|-------|
| `scripts/python/team-view.py` | absent |
| `skills/internal/view-team/` | absent |
| `tests/fixtures/team_view_fixtures.py` | absent |
| `tests/unit/test_team_view_parsers.py` | absent |
| `tests/contract/test_team_view_program_contract.py` | absent |
| `tests/contract/test_team_view_command.py` | absent |
| `tests/integration/test_team_view_program.py` | absent |

## Engine and runtime versions (probes, 2026-11-24)

| Probe | Reading |
|-------|---------|
| `python3 --version` | `Python 3.11.11` (pyproject declares `requires-python = ">=3.8"`) |
| `python3 -m pytest --version` | `pytest 8.4.2` |
| `python3 -c "import xdist; print(xdist.__version__)"` | `3.8.0` |
| `bash --version \| head -1` | `GNU bash, version 4.4.20(1)-release (x86_64-koji-linux-gnu)` |
| `git --version` | `git version 2.43.5` |
| `python3 scripts/python/goal-utils.py --version` | `goal-utils.py 0.0.22` |

## Distribution baselines (before any edit; T003 freezes the byte-level copies)

| Command | Reading (2026-11-24) |
|---------|----------------------|
| `python3 scripts/python/sync-mirrors.py --check` | **rc 0** — five mirror pairs `ok`, six projected rows `ok` (`shared/ == .specify/shared/`: 114 files byte-identical), per-tool copies `OK` |
| `python3 scripts/python/regen-command-copies.py --check` | **rc 0** — `OK: all per-tool command copies match the source templates.` |
| `python3 scripts/python/probe-utils.py --action compile-embeds --check` | **rc 0** — `85 units, zero drift` |
| `python3 scripts/python/probe-utils.py --action probes --validate` | **rc 0** — `Probe registry valid: 11 classes, 129 internal + 0 external objects` |
| `python3 scripts/python/probe-utils.py --action probes --reconcile` | **rc 0** — `zero-gap: 11 classes, 129 internal + 0 external objects, 86 embeds` |

## Existing dirty / untracked files (entry inventory — never committed, never reverted)

`git status --porcelain` at 2026-11-24T03:56Z, 41 entries; the pre-existing ones are:

```text
 M .specify/memory/session/20261110T083655Z-run-determination-skill-clarify-artifact-r20261110t081104z-b.md
 M .specify/memory/session/20261116T085759Z-run-determination-speckit-clarify-r20261116t075500z-102a.md
 M .specify/memory/session/20261116T092824Z-run-determination-speckit-tasks-r20261116t075500z-102a.md
 M .specify/memory/session/20261116T102430Z-run-determination-speckit-analyze-r20261116t102425z-47c2.md
 M .specify/skills/coaching-skills/SKILL.md
 M .specify/skills/coaching-skills/references/trainee-resolution.md
 M .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt
?? .specify/agents/instances/sdd-observer-103-team-view.agent.md
?? .specify/memory/exec-quant/records/20261124T025528953265Z-90c2b785.json
?? .specify/memory/exec-quant/records/20261124T025605320389Z-a347161a.json
?? .specify/memory/exec-quant/records/20261124T030152178165Z-932d68bd.json
?? .specify/memory/exec-quant/records/20261124T031021634137Z-87c94bdb.json
?? .specify/memory/exec-quant/records/20261124T031021962251Z-92fbc8cb.json
?? .specify/memory/exec-quant/records/20261124T032626220707Z-faf6cb93.json
?? .specify/memory/exec-quant/records/20261124T033614513281Z-c062874e.json
?? .specify/memory/exec-quant/records/20261124T034025149109Z-0eb737cd.json
?? .specify/memory/exec-quant/records/20261124T035107748712Z-88045b8e.json
?? .specify/memory/feedback/20261124T025602Z-speckit-requirements.md
?? .specify/memory/feedback/20261124T025611Z-skill-create-requirements.md
?? .specify/memory/feedback/20261124T030159Z-speckit-requirements.md
?? .specify/memory/feedback/20261124T031029Z-speckit-clarify.md
?? .specify/memory/feedback/20261124T031033Z-skill-clarify-artifact.md
?? .specify/memory/feedback/20261124T032631Z-speckit-plan.md
?? .specify/memory/feedback/20261124T033621Z-speckit-tasks.md
?? .specify/memory/feedback/20261124T034111Z-speckit-checklist.md
?? .specify/memory/feedback/20261124T035115Z-speckit-analyze.md
?? .specify/memory/session/20261124T025526Z-run-determination-speckit-requirements-r20261124t024654z-7c3.md
?? .specify/memory/session/20261124T025604Z-run-determination-skill-create-requirements-r20261124t024654.md
?? .specify/memory/session/20261124T030144Z-run-determination-speckit-requirements-r20261124t025733z-a2.md
?? .specify/memory/session/20261124T031015Z-run-determination-speckit-clarify-r20261124t024654z-7c3e.md
?? .specify/memory/session/20261124T031018Z-run-determination-skill-clarify-artifact-r20261124t024654z-7.md
?? .specify/memory/session/20261124T032625Z-run-determination-speckit-plan-r20261124t024654z-7c3e.md
?? .specify/memory/session/20261124T033612Z-run-determination-speckit-tasks-r20261124t024654z-7c3e.md
?? .specify/memory/session/20261124T034023Z-run-determination-speckit-checklist-r20261124t024654z-7c3e.md
?? .specify/memory/session/20261124T035055Z-run-determination-speckit-analyze-r20261124t024654z-7c3e.md
?? .specify/specs/103-team-view/journal.md
?? .specify/specs/103-team-view/test-evidence/analyze-findings.jsonl
?? .specify/specs/103-team-view/test-evidence/analyze-report.md
?? .specify/specs/103-team-view/test-evidence/analyze.jsonl
```

Files created by this implement stage and therefore **ours** (not in the pre-existing
list above): `.specify/specs/103-team-view/baseline-failed.txt`,
`.specify/specs/103-team-view/test-evidence/implement-baseline.txt`.

The two `.specify/skills/coaching-skills/**` dirty files belong to another change line
(they are not coaching-skill work of this feature); run-determination session records and
exec-quant/feedback records are machine-managed artifacts settled by earlier stages. None
of them is committed or reverted by this stage.

## Test entry baseline (the one full suite of this stage)

`bash scripts/bash/run-tests.sh --full --names-out .specify/specs/103-team-view/baseline-failed.txt`
→ **222 failed, 9818 passed, 3 skipped** (parallel pass) + **1 passed, 10043 deselected**
(serial pass); **rc 1** (derived — see `test-evidence/implement-baseline.txt` for the
disclosed derivation); 222 unique failed names written. This is the GATE-1 comparison
surface; a second full suite is forbidden in this stage.

