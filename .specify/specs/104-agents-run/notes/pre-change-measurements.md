# Pre-change measurements — implement entry (104-agents-run, package 1)

Captured: 2026-11-24T07:07Z (UTC), at implement start on branch `104-agents-run`.
All commands run from the repository root; outputs pasted verbatim (blank tails trimmed).
Purpose: freeze the comparison base for the zero-new-mechanism, containment and
before/after literal judgements of this feature (T001).

## 1. Repository state

```console
$ git rev-parse --short HEAD
b6907ee53

$ git status --short
 M .specify/skills/coaching-skills/SKILL.md
 M .specify/skills/coaching-skills/references/trainee-resolution.md
?? .specify/agents/instances/sdd-observer-104-agents-run.agent.md
?? .specify/memory/exec-quant/records/20261124T065207935567Z-b36e3245.json
?? .specify/memory/feedback/20261124T054130Z-skill-sdd-loop-driver.md
?? .specify/memory/feedback/20261124T065213Z-speckit-analyze.md
?? .specify/memory/feedback/20261124T065225Z-speckit-analyze.md
?? .specify/memory/session/20261124T065204Z-run-determination-speckit-analyze-r20261124t054500z-9b2d.md
?? .specify/specs/104-agents-run/journal.md
?? .specify/specs/104-agents-run/test-evidence/analyze-findings.jsonl
?? .specify/specs/104-agents-run/test-evidence/analyze-report.md
?? .specify/specs/104-agents-run/test-evidence/analyze.jsonl
```

The two `coaching-skills` modifications and the untracked observer/memory/session
records pre-exist this package (recorded in the line state spine). They are not this
package's artifacts: never staged, never restored.

**Disclosed side effect of the one full-suite baseline run (below)**: the tracked file
`.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` is rewritten by its
own test fixture on every full run (`generated: ...` → `generated: <none>`). It is a
foreign artifact, left untouched (not committed, not restored). The same run makes the
working tree non-byte-identical, which is why
`tests/contract/test_non_disposable_contract.py::test_t089_a_full_run_is_byte_identical_on_git_status`
is one of the 222 baseline failures named in `baseline-failed.txt`. Both are pre-existing
suite facts, not regressions of this feature.

## 2. Mirror / generated-copy parity (before any edit)

```console
$ python3 scripts/python/sync-mirrors.py --check; echo rc=$?
rc=0
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (23 files, byte-identical)
ok    skills/external/ == .specify/skills/ (394 files, byte-identical)
ok    skills/internal/ == .specify/skills/internal/ (139 files, byte-identical)
ok    agents/ == .specify/agents/templates/ (20 files, byte-identical)
ok    scripts/ == .specify/scripts/ (132 files, byte-identical)
projected[bash-version-guard] .specify/scripts/bash/check-prerequisites.sh <- scripts/bash/check-prerequisites.sh: ok
projected[bash-version-guard] .specify/scripts/bash/generate-instructions.sh <- scripts/bash/generate-instructions.sh: ok
projected[bash-version-guard] .specify/scripts/bash/run-tests.sh <- scripts/bash/run-tests.sh: ok
projected[python-version-bridge] .specify/scripts/python/script-interface-check.py <- scripts/python/script-interface-check.py: ok
projected[python-version-bridge] .specify/scripts/python/script_interface_cli.py <- scripts/python/script_interface_cli.py: ok
projected[python-version-bridge] .specify/scripts/python/sync-mirrors.py <- scripts/python/sync-mirrors.py: ok
ok    shared/ == .specify/shared/ (114 files, byte-identical)

$ python3 scripts/python/regen-command-copies.py --check; echo rc=$?
OK: all per-tool command copies match the source templates.
rc=0
```

## 3. Command-reference heading count (C-23 / C-34 premise)

```console
$ grep -cE '^# /speckit.agents' docs/reference/commands/agents.md
3
```

Three concatenated copies today (line 1, 114, 205). Required after-state: 1.

## 4. `argument-hint` state (C-01 premise)

```console
$ grep -c 'argument-hint' templates/commands/agents.md
0

$ grep -n 'argument-hint' templates/commands/team.md templates/commands/goal.md templates/commands/anchor.md
templates/commands/team.md:4:argument-hint: "[create|modify|run|view] [team-slug] [--target <T-<nnn>>]"
templates/commands/goal.md:4:argument-hint: "[create|view|modify|status] [goal-slug]"
templates/commands/anchor.md:4:argument-hint: "[create|view|modify|targets|migrate|migrate-archive|coordinate] [anchor-slug|team-slug] [--scope <layer>] [--spec-dir <path>]"
```

The three sibling forms place the key at frontmatter line 4 (after `description` /
`short-description`); `agents.md` currently has no such key.

## 5. Five new test modules — absence census

```console
$ for f in command_contract docs_contract skill_wiring multi_child_edges scope_contract; do p=tests/contract/test_agents_run_${f}.py; test -e "$p" && echo "PRESENT $p" || echo "ABSENT $p"; done
ABSENT tests/contract/test_agents_run_command_contract.py
ABSENT tests/contract/test_agents_run_docs_contract.py
ABSENT tests/contract/test_agents_run_skill_wiring.py
ABSENT tests/contract/test_agents_run_multi_child_edges.py
ABSENT tests/contract/test_agents_run_scope_contract.py
```

5/5 absent — the red-first premise holds.

## 6. C-34 stale-literal predicates — Before counts (owner table, line by line)

Counting form: occurrence count per file, `grep -oF | wc -l` for fixed predicates
(`grep -c` would count matching *lines*, not occurrences — the cross-line-repeat trap);
`grep -oiF | wc -l` for the case-insensitive predicates; the last predicate counts
lines matching `no arguments` together with `generate` under `grep -inE`.

Seven named files: `docs/reference/commands/agents.md` (R1),
`docs/reference/agents/command-and-skills.md` (R2), `overview.md` (R3), `design.md` (R4),
`docs/tutorials/installation.md` (R5), `docs/tutorials/quickstart.md` (R6),
`tests/scenarios/agents-command/single-entry-routing-scenario.md` (R7).

| Predicate | R1 | R2 | R3 | R4 | R5 | R6 | R7 | Total |
|---|---|---|---|---|---|---|---|---|
| `capabilities (create / refine)` (STR-005) | 2 | 1 | 0 | 0 | 0 | 0 | 1 | 4 |
| `create and refine one agent` (STR-006) | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| `creates or refines **one** agent` (bold variant) | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `Generate role-based agents or create custom agents` (STR-007) | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 2 |
| `generates the seven role-based workflow agents` (STR-008) | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| ci `generate role-based agents` | 2 | 0 | 0 | 0 | 1 | 4 | 0 | 7 |
| ci `generate project-aware role agents` | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| ci `generate seven` | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 2 |
| line with both `no arguments` and `generate` | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 2 |

Every "Before (files)" cell of `contracts/agents-run-docs.contract.md` § C-34 is
reproduced: STR-005 4 (R1/R2/R7), STR-006 2 (R1), bold variant 1 (R2), STR-007 2
(R5/R6), STR-008 2 (R1), `generate role-based agents` in R1/R5/R6, `generate
project-aware role agents` in R6, `generate seven` in R5/R6, and the
`no arguments`+`generate` line in R5/R6.

## 7. flow-class baseline (zero new unit rows)

```console
$ python3 .specify/scripts/python/flow-class-check.py --action check; echo rc=$?
flow-class check: 92 unit(s) scanned, 0 finding(s) [matched=92 inventory_units=92, clean]
coverage: ledger_rows=92 matched=92 inventory_units=92 gaps=0 parse_errors=0 floor=39
rc=0
```

## 8. Test budget — E2 baseline slot (the one and only full suite of this stage)

```console
$ bash scripts/bash/run-tests.sh --full --names-out .specify/specs/104-agents-run/baseline-failed.txt
# test runner: mode=parallel workers=auto dist=load passes=2 tier=full excluded_slow=0
...
==== 222 failed, 9929 passed, 3 skipped, 1152 warnings in 63.18s (0:01:03) =====
(second pass, declared serial member) 1 passed, 10154 deselected
# failed-name list written: .specify/specs/104-agents-run/baseline-failed.txt (222 entries) passes=2
rc=1
```

- rc captured directly (no pipe): **1**; passed **9930** (9929 + 1 serial pass), failed **222**,
  skipped **3**.
- Failed names (sorted, unique): `.specify/specs/104-agents-run/baseline-failed.txt` (222 entries).
- Complete raw stdout/stderr: `.specify/specs/104-agents-run/test-evidence/implement-baseline-full-run.txt`
  (7,387 lines; copied from the run-time capture at execution).
- E2 row written to `.specify/state/104-agents-run.md` `<!-- test-budget:begin -->` fence,
  `seq=1`, `slot=baseline`, `selection_basis=full-suite`, `merge_source`/`merged_at=na`.
- The baseline is **not full green**: 222 failures pre-exist this feature. Zero-new-failure
  claims are name-level (`comm -13 baseline current`), never count-level.
