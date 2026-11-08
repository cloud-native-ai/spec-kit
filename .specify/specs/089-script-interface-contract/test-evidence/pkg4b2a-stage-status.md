# PKG-4b2a stage status — skills backfill (T061)

date: 2026-11-07
line: `flow_class=execution; source=declaration; marker=null; error=-`

## Closed in this package

- T061 — every applicable script under `skills/**/scripts/` backfilled through the two declared
  mechanisms. Measured 87 files (16 `.sh`, 71 `.py`), all backfilled in place; 0 pure-library
  exemptions, 0 declared exceptions. Per-file list with basis and disposition:
  `T058-skills-backfill.txt`.
- Mirrors re-projected: `sync-mirrors.py --write` then `--check` exits 0 (87 skill mirrors
  changed, plus the engine's own mirror).

## What each file received

| language | declared mechanism | local adapter |
|---|---|---|
| bash (16) | `bash-version-guard`, right after the shebang | `script-interface:86:begin` .. `:end`: four labelled help lines, C-9 token judgement before `--` |
| python (71) | `python-version-bridge`, before `if __name__ == "__main__":` (header placement when no anchor; above the imports for the 16 upstream-fragile Office/PDF/DB scripts) | same marker pair: help BODY only, judgement delegated to `script_interface_cli.guard_argv` |

The python adapter deliberately asks the owner for the verdict
(`_sig.guard_argv(line, declared=_SIG_DECLARED)`) instead of restating the rule, so no second
copy of the flag forms, the terminator or the unknown-option exit lives in `skills/`. The
version line is re-derived at run time by the bridge; no version literal was copied.

## Readings

- `pytest -q tests/contract/test_script_interface_contract.py tests/unit/test_script_interface_cli.py` — 94 passed.
- `python3 scripts/python/sync-mirrors.py --check` — exit 0 (no DIFF, no ORPHAN).
- Flag sweep over all 87 files: `--help` rc 0, `-h` body identical, four closed-set labels,
  `--version` one line rc 0, unknown option non-zero. Work tree byte-identical across the sweep.
- `script-interface-check.py --check-projection` — 6 rows, all `idempotent=True`, no findings.

## Not closed by this package (unchanged, still open)

- T062 (instructions budget), T063 (full mirror-parity assertion), T064 (SC-007 record),
  T065, T066, and the remaining US5 tail.

## Notes for the next package

1. `scripts/python/sync-mirrors.py` gained one helper: `_strip_projection_block()`. A source
   under `skills/external/` can be BOTH the projection source and a script that already runs
   the projection, and without the strip the engine sees its own marker in the source, returns
   the text unchanged, and reports the pair as drift forever. `project_for()` now strips the
   carried block before projecting, so `project(project(x)) == project(x)` for those pairs.
   This is engine hardening required by the two-hats tree, not a change to the projection rule.
2. `skills/internal/code-review/scripts/git-delta-review.sh` declares `-s` twice upstream
   (`--side-by-side|-s` and `--severity|-s`); the declaration keeps both spellings and the
   script's own parser still resolves the ambiguity, which this package did not change.
3. A probe of `hook-stop.sh` with an unknown flag created `/home/agent/tmp/sdd-loop-hook` in
   this session; it was removed. The script documents that it records an event on invocation.
