# Quickstart — 111-general-best-practices

**Rule**: every command example below is either executed once at plan time (route **a**, with its real output quoted) or pinned by a named test / recorded evidence (route **b**, written by `/speckit.tasks` / `/speckit.implement`). Route-b examples are not executable before the implementation lands; each carries its own premises and names exactly what pins it. Repo root = the worktree `general-best-practices`.

## S-0 — Environment and current readings (executed at plan time, 2026-11-27)

Purpose: fix the floor the plan stands on — flow class, module absence, accumulation owners, mirror baseline, containment baseline, test-stack availability.

```bash
python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:111-general-best-practices"
# exit 0 (measured): flow_class: execution; source: declaration; marker: null

ls shared/best-practices .specify/shared/best-practices
# measured: both "No such file or directory" — the port creates both

python3 .specify/scripts/python/feedback-utils.py --help
# exit 0 (measured). The action set starts:
#   {record,status,list,dispose,mark-submitted,reindex,package,cleanup,upstream,
#    migrate-legacy,introspect-register,args-manifest,ingest-exec-quant,client-metrics}
# and `record` is present.

ls shared/guidelines/knowledge-promotion.md .specify/shared/guidelines/knowledge-promotion.md
# measured: both exist, 4849 bytes each

python3 scripts/python/sync-mirrors.py --check
# exit 0 (measured); the shared line reads:
#   ok    shared/ == .specify/shared/ (117 files, byte-identical)
# full log: test-evidence/plan-mirror-check.txt

python3 scripts/python/sync-mirrors.py
# exit 0 (measured) — write mode on the clean baseline wrote nothing;
# `git status --short` showed no modified mirror file
# full log: test-evidence/plan-mirror-write.txt

git diff --name-only 0419adae5..HEAD | wc -l
# measured: 18 — 10 spec paths + 2 session + 2 feedback + 2 exec-quant per-entry records,
# all inside FR-009's declared set

/usr/local/bin/python3 -c 'import pytest,sys; print(pytest.__version__, sys.version.split()[0])'
# measured: 8.4.2 3.11.11; the profile python3 imports no pytest
```

Premises for S-0: the worktree is a git checkout containing `0419adae5`; `python3` can execute the engines; `shared/` is at the measured 117-file baseline. These are plan-time readings; `/speckit.implement` re-measures them (research § Re-measure list 1–6).

## S-1 — Module shape: five documents, one table, four links (route b)

Scenario: after the module lands, its top level holds exactly the five documents, the manifest's only table declares the four categories, and every relative link resolves.

```bash
# the guard's own steps (internal to the test):
# 1. list shared/best-practices/ top-level regular files → exactly README.md
#    + programming-languages.md + system-interfaces.md + programming-frameworks.md
#    + programming-tools.md
# 2. parse the manifest's only Markdown table → 3 columns, 4 data rows, one relative
#    link per row; link-target set == the four owner files; literal 封闭集 present
# 3. resolve each manifest → owner-file link
# expected after implementation: all assertions green; 5/5 files, 4/4 rows, 4/4 links
```

Pinned by `tests/contract/test_general_best_practices.py` legs (a) and (f) — SC-001. Premises: the manifest is written with exactly one table; the four links are relative to `shared/best-practices/`; the mirror exists at `.specify/shared/best-practices/` with the same five names (parity is S-6's concern).

## S-2 — Placeholder ⇔ zero entries (route b)

```bash
# the guard's own steps:
# 1. for each of the three initially empty owner files: exactly one italic line
#    containing [[STR-006]] and zero `## ` entry headings
# 2. for programming-tools.md: at least one `## ` entry and no placeholder
# expected after implementation: 3 placeholders / 3 empty files; the seed file has 1 entry
# and 0 placeholders; the guard asserts the equivalence, never the count 3 as a frozen value
```

Pinned by the guard's leg (b) — SC-001; the count 3 is only the delivery-state measurement in the stage record. Premises: the module ships the three empty categories as designed (A-11); a later legitimate promotion removes a placeholder, and the guard must still pass because it checks equivalence.

## S-3 — Seed entry: three facts and the SSH extension (route b)

```bash
# the guard's own steps (text assertions on shared/best-practices/programming-tools.md):
# 1. the entry heading is the literal `## ` + [[STR-007]]
# 2. the body states: default HTTPS clone URL; special-repo HTTP/SSH MUST be flagged with
#    protocol and credential requirement; the ~/.git-credentials HTTPS-vs-HTTP mismatch
# 3. the 延伸 bullet states the SSH preference when HTTPS needs credentials and SSH works
# 4. the seed carries no 来源 bullet and no fabricated feedback id
# expected after implementation: 3/3 facts + extension present
```

Pinned by the guard's leg (c) — SC-002. Premises: the seed ports in substance from the source module (research M2 / R-4); the literal tokens follow the requirements' Shared Strings ([[STR-007]]); the adaptation touches only the manifest's two residue lines.

## S-4 — Accumulation pointers resolve; no second mechanism (route b)

```bash
# the guard's own steps:
# 1. feedback-utils.py --help lists the `record` action
# 2. shared/guidelines/knowledge-promotion.md exists
# 3. the manifest text contains the [[STR-001]] marker
# 4. no scripts/python/best-practices.py or best_practices.py exists
# expected after implementation: 2/2 pointers resolve; marker present; engine-file count 0
```

Pinned by the guard's leg (d) — SC-003. Premises: the feedback engine keeps its declared action set (research M3); the promotion owner stays at the cited path; the marker literal is [[STR-001]]; textual second-mechanism claims are review's, not the guard's.

## S-5 — Framework-map registration row in source and mirror (route b)

```bash
# the guard's own steps:
# 1. shared/definitions/framework-map.md contains exactly one layout-table row whose
#    Where cell is `.specify/shared/best-practices/` and whose Notes cell carries
#    Feature 111 + README.md + (framework source: shared/best-practices/)
# 2. .specify/shared/definitions/framework-map.md carries the same row after regeneration
# expected after implementation: 1 row in each table; token triple present in both
```

Pinned by the guard's leg (e) — SC-004. Premises: the map keeps its single three-column layout table; the row lands adjacent to the `.specify/shared/` rows; the mirror row exists only after the S-6 regeneration.

## S-6 — Mirror regeneration and zero drift (route b)

```bash
python3 scripts/python/sync-mirrors.py
# expected after implementation: exit 0; writes .specify/shared/best-practices/* and
# the regenerated .specify/shared/definitions/framework-map.md
python3 scripts/python/sync-mirrors.py --check
# expected after implementation: exit 0; the shared pair reports zero DIFF
```

Pinned by C-402 and the existing `tests/contract/test_mirror_parity_suite.py` (per-file parameters derived from the engine) — SC-004. Premises: the five documents and the map edit exist in source before the write-mode run; the parity suite is green at the implement entry (re-measured per research § Re-measure list 2); the guard does not re-implement the comparison.

## S-7 — Init distribution proof (route b)

```bash
# evidence 1 — code path (cited, read-only):
sed -n '2743,2757p' src/specify_cli/__init__.py
# shows the wholesale copy of resource_path/shared into <project>/.specify/shared

# evidence 2 — existing integration test that runs the same copy step:
#   tests/integration/test_init_new_layout.py (run through scripts/bash/run-tests.sh)

# evidence 3 — one recorded read-only initialization drill, under the sanctioned temp root:
#   run the same invocation form (--here --ai qoder --script sh --no-git) inside
#   .specify/.tmp/, then list <drill>/.specify/shared/best-practices/
# expected after implementation: exactly the five documents; no CLI or packaging change
```

Pinned by C-407 and the implement stage's recorded drill — SC-004. Premises: `specify init` is installed from this checkout; the drill root is `.specify/.tmp/` (git-ignored); the existing init test does not name the module, which is why the drill is the direct reading; no second test file is added.

## S-8 — Guard red-first then green (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_general_best_practices.py -q --names-out <evidence path>
# expected: before the module lands → non-zero exit with the guard failing on the missing
# files (red-first record); after the module lands → exit 0 with zero new failure names
```

Pinned by SC-007's stage record (the runner's exit code + the red-first capture + the name-level comparison) — SC-007. Premises: `SPECKIT_PYTHON=/usr/local/bin/python3` carries pytest 8.4.2 (research M7); the guard file is written before the module; the runner's default parallel form is kept.