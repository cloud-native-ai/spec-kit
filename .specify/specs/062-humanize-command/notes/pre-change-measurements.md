# Pre-change measurements — 062-humanize-command (IMPLEMENT phase, T001)
# Captured: 2026-10-19T17:19:43+08:00
# Environment: CWS_LIB_BASH_HOME=/storage/project/cloud-native-tools/cws-lib-bash (cws-lib-bash restored 2026-10-19 15:58)

## 1. Generation face — python3 scripts/python/regen-command-copies.py --check
```
OK: all per-tool command copies match the source templates.
exit=0
```

## 2. Mirror face — python3 scripts/python/sync-mirrors.py --check
```
ok    templates/ == .specify/templates/ (22 files)
DIFF  .specify/skills/create-pages/SKILL.md
DIFF  .specify/skills/create-pages/references/hugo-site.md
...(total DIFF lines: 113)
```

## 3. Compile face — python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check
```
compile-embeds drift in 73 of 73 units (--check; nothing written):
- /speckit.analyze
- /speckit.checklist
- /speckit.clarify
...(drift units: 73)
```
Pre-change test suite run (canonical runner, `bash scripts/bash/run-tests.sh --names-out /tmp/humanize-prechange-failed.txt`, captured 2026-10-19):

## 4. Test suite (name-level, vs frozen baseline)

```
=========== 71 failed, 3929 passed, 3 warnings in 157.66s (0:02:37) ============
# failed-name list written: /tmp/humanize-prechange-failed.txt (71 entries)
comm -13 notes/baseline-failed-tests.txt /tmp/humanize-prechange-failed.txt  →  EMPTY (zero NEW names)
comm -23 ...  →  empty too (zero fixed; byte-identical name set)
```

**Environment verdict**: `cws-lib-bash` is **restored** (`CWS_LIB_BASH_HOME=/storage/project/cloud-native-tools/cws-lib-bash` resolvable; `bin/cws_bash_env` present, mtime 2026-10-19 15:58). The tasks.md § Environment Prerequisites degradation record ("94 failed / 3906 passed, 23 environment-induced additions") is **expired**: the current run reproduces the frozen 71-name set exactly. The frozen baseline (`notes/baseline-failed-tests.txt`) is NOT rewritten — it stays authoritative; the caveat resolves to "environment restored".

## 5. Mirror-face premise note (honest drift accounting)

The frozen mirror baseline records 209 DIFF lines; the pre-change capture reports **113**. Name-level comparison:
- NEW vs frozen baseline: exactly **1** — `.specify/skills/internal/manage-feedback/SKILL.md`. Provenance check (git log): source last touched by b2e5ef6b (059 era), mirror last landed by af70a81c ("update specify version") — divergence predates this implement run and is NOT attributable to this feature; that pair is a 不触碰 file for 062. Recorded as inherited state; the feature's relative criterion (zero NEW drift **attributable to 062**) is judged against the pre-change capture above, not against the stale 209-line count.
- Fixed since baseline: 97 names (mirror syncs landed between plan-time freeze and implement start — upstream repairs, out of 062 scope).
- The frozen touched pair `shared/definitions/probe-definitions.md` (baseline line 181) is **currently byte-identical** (not in the 113) — after 062 adds its two registry rows it will DIFF again and the feature-scoped sync restores byte equality.
