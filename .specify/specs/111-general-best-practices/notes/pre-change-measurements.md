# Pre-change measurements — 111-general-best-practices / implement P1 (T003)

Frozen before any executable or module edit in this package. Every row carries its
re-derivation command, the real output and the measurement date. Worktree:
`.specify/.tmp/sdd-loop/worktrees/general-best-practices`, branch
`111-general-best-practices`, HEAD `7db9d8dec` at capture time (2026-11-27T08:37Z).

| # | Premise | Command | Real output (2026-11-27) |
|---|---------|---------|--------------------------|
| 1 | Mirror baseline before the module lands | `python3 scripts/python/sync-mirrors.py --check` | rc 0; `ok    shared/ == .specify/shared/ (117 files, byte-identical)` (all other pairs ok too) |
| 2 | Framework-map sibling block, and zero module hits | `grep -n '' shared/definitions/framework-map.md \| sed -n '48,55p'`; `grep -c 'best-practices' shared/definitions/framework-map.md .specify/shared/definitions/framework-map.md .specify/instructions.md` | Sibling `.specify/shared/` rows occupy lines 48–55 of the single layout table (Header/Where/Notes form; Notes cells end with `(framework source: shared/…)` pointers); `best-practices` hits = `0` / `0` / `0` |
| 3 | Source module inventory and adaptation points | `wc -l /storage/project/cloud-native-ai/ai-harness/shared/best-practices/*.md`; `grep -nE 'ai-harness\|\.ah/\|/ah\.\|Feature 040' …/*.md` | Five documents / 61 lines (README 38, programming-tools 8, the other three 5/5/5). Residue: `README.md:3` `ai-harness`, `README.md:5` `Feature 040`, `README.md:33` `.ah/shared/best-practices/`; `/ah.` hits = 0 |
| 4 | Source-run CLI reading | `PYTHONPATH=$PWD/src /usr/local/bin/python3 -c 'import specify_cli; specify_cli.main()' --version` | `specify-cli 0.0.22` / `framework commit: 7db9d8decd0cd3b174b06fc4cb7ceb313c491202 (git)` / `python: 3.11.11 on linux (x86_64)`; rc 0. **Premise decay (annotated, not suppressed)**: tasks.md T003 quotes the plan-time reading `1638077e4`; HEAD moved to `7db9d8dec` by this feature's own checkpoint 04–06 commits — attributable to this feature, so the source-run form (not the SHA) is the invariant |
| 5 | Accumulation owners in place | `python3 .specify/scripts/python/feedback-utils.py --help`; `ls -la shared/guidelines/knowledge-promotion.md .specify/shared/guidelines/knowledge-promotion.md` | Action set contains `record` (full set: record,status,list,dispose,mark-submitted,reindex,package,cleanup,upstream,migrate-legacy,introspect-register,args-manifest,ingest-exec-quant,client-metrics); both `knowledge-promotion.md` copies exist at 4849 B each |
| 6 | Baseline object and live containment | `git cat-file -e 0419adae5`; `git diff --name-only 0419adae5..HEAD` | Object present (rc 0). Live reading = **92** paths = 72 `.specify/specs/111-general-best-practices/**` + 7 `.specify/session/**` + 7 `.specify/feedback/**` + 6 `.specify/exec-quant/records/**`; set difference against FR-009's declared set = **0** out-of-set paths. **Trap form**: the count grows with each stage (plan-time 18 → tasks-time 43 → now 92); the invariant is "all ∈ declared set", not the number |
| 7 | Target absence (pre-creation reading) | `ls shared/best-practices .specify/shared/best-practices tests/contract/test_general_best_practices.py`; `test -d …/notes`; `test -e …/coverage-baseline.txt` | 3/3 target paths `No such file or directory`; `notes/` ABSENT; `coverage-baseline.txt` ABSENT — measured immediately before T001/T002 created them |
| 8 | Second-engine absence | `ls scripts/python/best-practices*.py scripts/python/best_practices*.py` | both globs: `No such file or directory` (the guard's leg (d) reading is 0 already at entry) |

Supporting readings (same date): contract clause definitions per file =
manifest 6 / entry-shape 5 / accumulation 6 / distribution-guard 7 (24 total, counted
on line-start `**C-NNN**` definition lines).