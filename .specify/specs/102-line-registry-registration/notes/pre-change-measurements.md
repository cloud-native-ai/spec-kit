# Pre-change measurements — 102-line-registry-registration (implement, package 1)

Collected at HEAD `e0ab20bdf` on the implement baseline of 2026-11-16. Every figure below
comes from the command printed above it in this run; nothing is copied from an earlier stage.
The judged file surface follows A-21: a regular file (symlinks skipped) with a `.sh` / `.bash` /
`.py` suffix or a `#!` first line, walked recursively over `scripts/bash/`, `scripts/python/`,
`skills/`.

## M-1 — Judged files per declared scan root (158 total)

Command:

```bash
python3 - <<'PY'
import os, pathlib
roots = ["scripts/bash", "scripts/python", "skills"]
for root in roots:
    n = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not os.path.islink(os.path.join(dirpath, d)))
        for name in sorted(filenames):
            p = pathlib.Path(dirpath) / name
            if p.is_symlink() or not p.is_file():
                continue
            if p.suffix in (".sh", ".bash", ".py"):
                n += 1
                continue
            try:
                with p.open("rb") as fh:
                    first = fh.readline(120)
            except OSError:
                continue
            if first.startswith(b"#!"):
                n += 1
    print(f"{root}: {n}")
    total += n
print("total:", total)
PY
```

Readout:

```text
scripts/bash: 16
scripts/python: 49
skills: 93
total: 158
```

## M-2 — `[[STR-004]]` content marker (`terraform apply`) — 0 hits

```bash
grep -rn "terraform apply" scripts/bash scripts/python skills || echo "(none)"
```

```text
(none)
```

Exit 1 (no match), zero judged files carry the marker.

## M-3 — `[[STR-005]]` marker (`run-tests.sh --full`) — 4 hits, all `.md`

```bash
grep -rn "run-tests.sh --full" scripts/bash scripts/python skills
```

```text
skills/external/sdd-loop-driver/references/efficiency-model.md:91:| `baseline` | implement 起点（首个任务前） | `run-tests.sh --full --names-out <spec-dir>/baseline-failed.txt`，按名称捕获失败名单 |
skills/external/sdd-loop-driver/references/efficiency-model.md:92:| `closure` | `review` 通过之后、合并之前，由驱动或独立校验单元执行 | `run-tests.sh --full --names-out <spec-dir>/final-failed.txt`，`comm -13` 名称级比较 |
skills/external/sdd-loop-driver/references/stage-prompts.md:165:  bash scripts/bash/run-tests.sh --full --names-out <spec-dir>/baseline-failed.txt
skills/external/sdd-loop-driver/references/stage-prompts.md:206:  bash scripts/bash/run-tests.sh --full --names-out <spec-dir>/final-failed.txt
```

All four hits are `.md` prose, outside the A-21 judged surface — the live reading can be zero.

## M-4 — Both engine candidates answer the same version

```bash
python3 skills/external/sdd-loop-driver/scripts/line-registry.py --version
python3 .specify/skills/sdd-loop-driver/scripts/line-registry.py --version
```

```text
line-registry.py 0.0.22   (rc=0)
line-registry.py 0.0.22   (rc=0)
```

## M-5 — Distribution baselines (detail in `test-evidence/mirror-baseline.txt`)

```bash
python3 scripts/python/sync-mirrors.py --check
```

rc 2; 5 `DIFF` rows (`skills/external/`) and 2 `ORPHAN` mirrors
(`.specify/scripts/line-registry.py`, `.specify/scripts/stage-runner.sh`).

```bash
python3 scripts/python/regen-command-copies.py --check
```

rc 0.

```bash
python3 scripts/python/flow-class-check.py --action check
```

rc 0; `91 unit(s) scanned, 0 finding(s)`.

## M-6 — Both deliverables are absent before this feature

```bash
ls scripts/bash/line-run.sh scripts/python/line-registration-scan.py
```

```text
ls: cannot access 'scripts/bash/line-run.sh': No such file or directory
ls: cannot access 'scripts/python/line-registration-scan.py': No such file or directory
```

## M-7 — Implement baseline failure names (T003 slot, taken by the driver)

`.specify/specs/102-line-registry-registration/baseline-failed.txt` exists (24035 bytes,
241 test-id lines, of which 9 are `test_loop_state_engine.py`); it is the full-suite
`--names-out` reading taken once at the implement baseline. Name-level comparison for every
intermediate reading uses `comm -13` against this file, never a count.
