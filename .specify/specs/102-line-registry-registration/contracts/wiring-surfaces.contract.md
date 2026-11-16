# Contract — wiring surfaces (owner doc, status command, ambient bullet, run-team)

**Subject**: the four text surfaces that carry the registration duty to a reader or executor. Every clause is judged by a contract test (`tests/contract/test_line_registration_wiring.py`), which is the red leg for each pinned literal. Shared literals are referenced as `[[STR-NNN]]`.

**Reference direction (all clauses)**: the criterion and its adjudication boundary are owned by `shared/guidelines/reporting-obligations.md` § 九. No downstream surface in this contract may restate the threshold, the mechanical marker set, or the digest's rendering rules; each names the owner path and stops there.

## C-01 — Owner document (`shared/guidelines/reporting-obligations.md` § 九)

C-01 The digest contract MUST gain one long-task registration criterion: a run meeting the criterion MUST register a line at start, refresh it at stage boundaries and close it at the end; an unregistered run never enters the digest, so `[[STR-006]]` is an accurate conclusion, not a missed report.
C-02 The criterion MUST name the carrier (`[[STR-001]]`) and MUST state that the registry writer is the engine (`[[STR-002]]`) — never `scripts/python/journal-utils.py`.
C-03 The threshold value and the adjudication boundary MUST be stated and owned in this document. No other surface of this contract restates them.
C-04 The section MUST NOT add a scheduler, daemon, threshold table or second liveness channel; § 十一 remains in force.

## C-05 — `/speckit.status` command template (`templates/commands/status.md`)

C-05 The template MUST contain exactly this sentence, verbatim:

```text
**Single source**: the digest reads the Line Registry and nothing else — it MUST NOT be changed to scan processes, because determinism is the contract; the obligation is owned by `shared/guidelines/reporting-obligations.md` § 九 and is reached by path, never restated here.
```

C-06 The template MUST NOT gain a second renderer, a process-scanning step, a restatement of § 九's criterion bullets, or a change to the script's action set.

## C-07 — Ambient bullet (`templates/instructions-template.md`)

C-07 Inside `## Progress Reporting Discipline`, immediately after the `Exemptions and precedence` bullet, the template MUST gain exactly one bullet, verbatim:

```text
- **Long tasks must register a line (长任务须登记)**: a long-running task that registers no line is invisible to `/speckit.status`, so wrap it with `scripts/bash/line-run.sh`; the criterion and its bounds are owned by `shared/guidelines/reporting-obligations.md` § 九.
```

C-08 No new section may be created, and no other bullet may be edited. The bullet MUST NOT contain the owner's threshold value, the mechanical marker literals, or a second copy of the criterion.
C-09 `.specify/instructions.md` MUST carry the same bullet exactly once, obtained through the `/speckit.instructions` section-level refresh (never a hand edit); `AGENTS.md`, `CLAUDE.md`, `QODER.md` and `.github/copilot-instructions.md` MUST remain symlinks whose content shows the bullet.

## C-10 — run-team (`skills/internal/run-team/SKILL.md`)

C-10 At the top of **§5 Present & Execute** the skill MUST register the run's line through the line-registry engine at its A-17 candidates — `skills/external/sdd-loop-driver/scripts/line-registry.py`, then `.specify/skills/sdd-loop-driver/scripts/line-registry.py` (a downstream project holds only the second) — with the composed `<team-slug>-<run-id>` id, and MUST fail closed before dispatching any seat. The site MUST read the engine's actions, parameters and exit codes from its `--help` rather than restating them.
C-11 Inside **§6 Orchestrate** the skill MUST refresh the run line's last event at each orchestration step boundary via the engine's `update`, and MUST state that no timer, daemon or second channel exists.
C-12 At the start of **§7 Report** the skill MUST close the run's line through the engine and MUST require the composed `[[STR-007]]` to appear in the report body. A close failure MUST be stated in the report, not swallowed.
C-13 The skill MUST NOT modify `skills/internal/create-team`'s Report contract, and MUST NOT add an engine parameter table.

## C-14 — Cross-surface invariants

C-14 Removing any one of C-01, C-05, C-07, C-10, C-11 or C-12 MUST turn its guarding test red.
C-15 The four surfaces MUST agree on the same owner path and the same carrier path; a divergent path is a defect of the surface, not of the owner.
C-16 None of the four surfaces may be edited only in a mirror: each authored edit lands in the framework source and is projected by `sync-mirrors.py` / `regen-command-copies.py` / the `/speckit.instructions` refresh.

## Examples

**E-1 (not runnable in this planning run — the texts do not exist yet).** Premises: implementation landed all four edits.

```bash
grep -n "Single source" templates/commands/status.md
grep -n "line-run.sh" templates/instructions-template.md .specify/instructions.md
grep -n "line-registry.py" skills/internal/run-team/SKILL.md
```

Expected: one hit each for the first and second patterns in their files; at least three hits for the engine path in run-team. Pinned by `tests/contract/test_line_registration_wiring.py`.

**E-2 (runnable now — measured 2026-11-16; shows the pre-edit baseline).** Premises: this repository before implementation.

```bash
grep -c "line-run.sh" templates/instructions-template.md .specify/instructions.md skills/internal/run-team/SKILL.md
grep -c "Single source" templates/commands/status.md
```

Measured: `0` for all four counts, and `grep -c` exits `1` because a count of zero is its "no line selected" status — the surfaces do not yet carry the duty, which is the state this feature changes.
