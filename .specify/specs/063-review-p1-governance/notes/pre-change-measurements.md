# Pre-change measurements (T001)

Owner of this record: T001. Commands were actually run at the dates below; outputs are
copied from the real runs, not reconstructed from the tasks.md measured premises.

Run date: **2026-10-19** (UTC). Repo root: `/storage/project/cloud-native-ai/spec-kit`.
Branch: `063-review-p1-governance`, HEAD `728ad4ea`.

## 1. Per-tool command copies (`regen-command-copies.py --check`)

Command:

```
python3 scripts/python/regen-command-copies.py --check
```

Raw output captured to `notes/baseline-regen-check.txt`, exit **0**:

```
OK: all per-tool command copies match the source templates.
```

## 2. Mirror sync (`sync-mirrors.py --check`)

Command:

```
python3 scripts/python/sync-mirrors.py --check
```

Raw output captured to `notes/baseline-mirror-check.txt`, exit **2**:

```
202 DIFF lines (grep -c '^DIFF' notes/baseline-mirror-check.txt → 202)
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
```

This is the pre-change drift set. Judgement for this feature is **zero NEW DIFF** relative
to this file; the pairs this feature touches must become byte-identical after T045 sync.

## 3. Compiled Wrap-up faces (`probe-utils.py --action compile-embeds --check`)

Command:

```
python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check
```

Raw output captured to `notes/baseline-compile-check.txt`, exit **0**:

```
compile-embeds --check: 74 units, zero drift
```

## 4. Coverage lane dark run on 062 and baseline inventory

Command (062 has no frozen baseline — this is the dark state the consume side must
recognise as an error, never as an empty exemption list):

```
python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/062-humanize-command
```

Exit **2**. Real output landmarks:

```
scanned 144 files: parsed 81 + named-unparseable 63 == 144  [relational sentinel OK]
clause universe: 842 distinct names over 81 parsed files (866 ids extracted)
baseline: .specify/specs/062-humanize-command/coverage-baseline.txt (0 names, MISSING)
uncovered beyond baseline: 495
FR universe: 29
FR claimed: 13
FR uncovered: 16
ERROR frozen baseline not found: .specify/specs/062-humanize-command/coverage-baseline.txt —
an absent baseline is NOT an empty exemption list, so this run cannot judge the delta
status: baseline-missing
512 error(s), 0 warning(s)
```

Baseline inventory:

```
$ find .specify/specs -name coverage-baseline.txt | sort
.specify/specs/053-machine-decidable-artifacts/coverage-baseline.txt
.specify/specs/063-review-p1-governance/coverage-baseline.txt
```

Before the 063 freeze (recorded in tasks.md measured premises) only 053 existed; 062
remains baseline-missing, which is the state the consume-side pre-flight (C-5/C-29) must
report loudly.

## 5. ID Register `REC-` count

```
$ grep -n 'REC-' .specify/memory/register.md | wc -l
0
```

Zero `REC-` rows are registered before this feature — the forward-only starting fact for
C-11/C-12.

## 6. Backlog line 89 snapshot (pre-flip)

```
$ grep -n '' .specify/memory/feedback/backlog.md | sed -n '89p'
89:| 2026-10-15 | introspection-20261015T081832Z#F-01(15 条成员 + G-D 聚类) | **Wrap-up 编译嵌入缺 `--run-id`/必填参数全集,两引擎逐参单错**:... | direct-fix | ... | open(修复须同步全部编译单元重编译 + `--reconcile` 收口;15 条本地条目 + 全部命令单元同面) | — |
```

Status segment reads `open(...)`. T044 must flip this same line to `closed` in the same
commit as the full recompile.

## 7. Pre-frozen artifacts referenced, not re-run

- `notes/baseline-failed-tests.txt` — 63 lines, frozen 2026-10-19 at the tasks stage
  (`git diff` against the plan-stage freeze was empty; name-set equality, not merely count
  equality). Baseline is **63 failed / 3954 passed** and MUST NOT be relaxed.
- `coverage-baseline.txt` — 497 lines, first frozen at the tasks stage, `base-sha
  bf88f2c63857`, 140 files (parsed 77 + named 63). Comparison form is `LC_ALL=C comm -13`.

## Summary table

| Premise | Pre-change value | Evidence file |
|---|---|---|
| regen copies | OK (exit 0) | `notes/baseline-regen-check.txt` |
| mirror drift | 202 DIFF (exit 2) | `notes/baseline-mirror-check.txt` |
| compiled faces | 74 units, zero drift (exit 0) | `notes/baseline-compile-check.txt` |
| 062 coverage lane | `status: baseline-missing`, exit 2 | this file § 4 |
| coverage baselines on disk | 053, 063 | this file § 4 |
| `REC-` in register | 0 | this file § 5 |
| backlog line 89 | `open(...)` | this file § 6 |
| failed-test baseline | 63 names | `notes/baseline-failed-tests.txt` |
