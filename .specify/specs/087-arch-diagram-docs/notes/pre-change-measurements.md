# Pre-change measurements — 087 arch-diagram-docs

Captured **2026-11-06** in `/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs`
(branch `line/087-arch-diagram-docs`, base `24cb4edc`), before any product byte of this feature was
written. Every block below is a command plus the output it actually produced in this worktree — nothing is
copied from `plan.md`, `quickstart.md` or `data-model.md`.

Interpreter for every reading that needs the repo's own imports:

```text
$ /usr/bin/python3 -c "import sys, typer, pytest; print(sys.version); print('typer', typer.__version__); print('pytest', pytest.__version__)"
3.11.13 (main, May 13 2026, 09:30:18) [GCC 10.2.1 20200825 (Alibaba 10.2.1-3.9 2.32)]
typer 0.27.3
pytest 9.2.0
```

---

## T002 — the four premises later rows diff against

### (a) `--action obligation` does not exist yet

```text
$ /usr/bin/python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root . --json
usage: docs-utils.py [-h] --action
                     {scan,expire,clean,archive-check,stats,validate,fix-links,audit}
                     [--root ROOT] [--yes] [--apply] [--moves MOVES]
                     [--scope SCOPE] [--summary SUMMARY]
                     [--items-file ITEMS_FILE] [--allow-special NAME]
docs-utils.py: error: argument --action: invalid choice: 'obligation' (choose from 'scan', 'expire', 'clean', 'archive-check', 'stats', 'validate', 'fix-links', 'audit')
exit=2
```

The `choices` list it refuses against, and the count of the string in that file:

```text
$ grep -n "choices=\[" -A 2 skills/external/create-docs/scripts/docs-utils.py
398:        choices=["scan", "expire", "clean", "archive-check", "stats", "validate",
399-                 "fix-links", "audit"],
400-    )

$ grep -c "obligation" skills/external/create-docs/scripts/docs-utils.py
0            (grep-exit=1 — zero matches)
```

### (b) carrier population, re-derived now

```text
$ for d in concepts tutorials tasks reference decisions contribute; do printf '%s/ %s\n' "$d" "$(find docs/$d -name '*.md' -type f 2>/dev/null | wc -l)"; done
concepts/ 12
tutorials/ 2
tasks/ 1
reference/ 64
decisions/ 5
contribute/ 1

$ ls docs/ARCHITECTURE.md
ls: cannot access 'docs/ARCHITECTURE.md': No such file or directory
(therefore ARCHITECTURE.md absent ⇒ carriers = 12+2+1+64+5+1 = 85)
```

The naive one-level trap, measured on the directory where it bites:

```text
$ /usr/bin/python3 -c "from pathlib import Path; print(len(list(Path('docs/reference').glob('*.md'))))"
1
$ /usr/bin/python3 -c "from pathlib import Path; print(len(list(Path('docs/reference').rglob('*.md'))))"
64
```

`glob('*.md')` on `docs/reference/` yields **1** (`glossary.md`, the only first-level file) and `rglob` yields
**64** — the whole tree of subdirectories (`commands/`, `skills/`, `history/`, …). A `glob`-based carrier walk
therefore silently loses 63 reference documents; the carrier walk MUST be recursive.

### (c) `docs/.speckit/` does not exist yet

```text
$ ls -d docs/.speckit
ls: cannot access 'docs/.speckit': No such file or directory
exit=2
```

Both `docs/.speckit/runs/` and `docs/.speckit/exemptions/` are therefore new paths, not existing ones.

### (d) one diagram landing exists, no second landing

```text
$ find docs -type d -name diagrams | wc -l
0

$ ls docs/assets
quickstart-workflow.png
quickstart-workflow.puml
quickstart-workflow.svg
```

`docs/assets/` is the live precedent (source `.puml` + two rendered faces), and no per-type `diagrams/`
subtree exists in any documentation directory.

---

## T003 — guard baseline (failure **name sets**, not counts) and mirror baseline

Invocation, exactly as run:

```text
$ /usr/bin/python3 -m pytest tests/contract/test_expression_compatibility.py \
    tests/contract/test_expression_gate_wiring.py tests/contract/test_docs_command_template.py \
    tests/contract/test_confirmation_gates_sweep.py tests/contract/test_directory_governance.py \
    -q --no-header -p no:cacheprovider
FAILED tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target
1 failed, 120 passed, 1 warning in 2.66s
rc=1
```

Per-file, so a later row can diff one guard family without re-running the sibling:

| File | Reading |
|------|---------|
| `tests/contract/test_expression_compatibility.py` | `16 passed` (rc=0) |
| `tests/contract/test_expression_gate_wiring.py` | `16 passed` (rc=0) |
| `tests/contract/test_docs_command_template.py` | `22 passed` (rc=0) |
| `tests/contract/test_confirmation_gates_sweep.py` | `1 failed, 45 passed` (rc=1) |
| `tests/contract/test_directory_governance.py` | `21 passed` (rc=0) |

**Baseline failure name set (this feature MUST add nothing to it):**

```text
tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target
```

The one red is pre-existing and matches the driver's recorded full-suite baseline
(`test-evidence/baseline-failed.txt`, same node id, 26 failed / 7471 passed / 4 skipped overall). Its own
assertion text is `SC-002 target missed: residual 27 > 25% of baseline 93` — a residual-count budget in the
confirmation-gates sweep, untouched by this feature.

### Mirror checks, same interpreter

```text
$ /usr/bin/python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (415 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (16 files)
ok    scripts/ == .specify/scripts/ (121 files)
ok    shared/ == .specify/shared/ (94 files)
rc=0

$ /usr/bin/python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
rc=0
```

**Baseline: six mirror pairs `ok`, both checks rc=0, zero drift.**

### The known trap — a bare `python3` reports a false red

`python3` on `PATH` in this environment is `/storage/project/profiles/.venv/bin/python3` (CPython 3.11.13) and
it **cannot** `import typer`:

```text
$ python3 scripts/python/sync-mirrors.py --check
  File "/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs/src/specify_cli/__init__.py", line 40, in <module>
    import typer
ModuleNotFoundError: No module named 'typer'
ok    templates/ == .specify/templates/ (22 files)
… six pairs all "ok" …
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
rc=2
```

Six pairs `ok` in the same output that ends in `DRIFT detected` and `rc=2`: the verdict comes only from the
embedded `regen` subprocess failing on the missing module. **This is an environment gap, never drift.** The
handler is to re-run with an interpreter that can `import typer` (`/usr/bin/python3`, above) — MUST NOT be
"fixed" with `--write`, which would turn one environment gap into a real write. The earlier planning-phase
scratch venv `/tmp/087-toolenv` no longer exists (system temp was cleaned) and is not referenced anywhere in
this stage.

---

## T004 — coverage baseline already frozen

`coverage-baseline.txt` is on disk from the analyze repair round; it is **not** re-frozen here:

```text
$ wc -l .specify/specs/087-arch-diagram-docs/coverage-baseline.txt
575 .specify/specs/087-arch-diagram-docs/coverage-baseline.txt

$ head -2 .specify/specs/087-arch-diagram-docs/coverage-baseline.txt
# coverage-baseline: frozen UNCOVERED clause names, codepoint-sorted, one per line; …
# frozen-from: .specify/specs/*/contracts/* excluding 087-arch-diagram-docs | … | base-sha: 47a59449c324 | files: 266 (parsed 159 + named 107)
```

575 lines = 2 header lines + **573 frozen uncovered clause names**, matching the analyze-stage record. The
freezer's own summary line is pasted as the pointer in
`test-evidence/coverage-baseline-pointer.txt`, not as a second copy of the data.

---

## T033 — the zero-change boundary for `skills/external/draw-diagram/**` (measured 2026-11-06, Part 3)

`T-004` decision: the drawing capability is **cited, never edited**. This row does not change a source file; it
establishes the fact every later row of this feature relies on — the tree is byte-identical to the branch base.

```text
$ git diff --name-only 24cb4edc -- skills/external/draw-diagram/

exit 0
```

The output is **empty**: zero changed paths, zero added paths, zero deleted paths. Measured twice with the same
result (`… | wc -l` → `0`), the second time after Part 2 had already landed its engine and mirror changes, so the
reading is not an artifact of an unmodified working tree.

Read-as-one-sentence: nothing this feature delivered before this row — not the checker, not its fixtures, not its
contracts — reached into the drawing capability, and the rows after it are constrained by the same boundary.
`GATE-5` re-reads this fact at closure with the same command; the two readings must agree.
