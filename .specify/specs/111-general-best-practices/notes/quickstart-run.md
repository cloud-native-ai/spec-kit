# Quickstart run — 111-general-best-practices (T016, 2026-11-27)

Every scenario of `quickstart.md` executed as written. Repo root = this worktree
(`general-best-practices`), HEAD `63fdca3f7` + P2 working tree. Interpreter:
`/usr/local/bin/python3` (pytest 8.4.2); every test execution through
`scripts/bash/run-tests.sh` only.

## S-0 — Environment and current readings (re-taken)

```bash
python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:111-general-best-practices"
```

Exit `0`. Real output:

```
unit_id: spec:111-general-best-practices
flow_class: execution
flow_type: -
source: declaration
marker: null
basis: null
neutral: false
```

```bash
ls shared/best-practices .specify/shared/best-practices
```

Exit `0`. Both directories now exist (plan-time reading was "No such file or directory";
the port created them). Each lists exactly `README.md`, `programming-languages.md`,
`system-interfaces.md`, `programming-frameworks.md`, `programming-tools.md`.

```bash
python3 .specify/scripts/python/feedback-utils.py --help
```

Exit `0`. The action set starts with
`{record,status,list,dispose,mark-submitted,reindex,package,cleanup,upstream,migrate-legacy,introspect-register,args-manifest,ingest-exec-quant,client-metrics}`
and `record` is present.

```bash
ls -la shared/guidelines/knowledge-promotion.md .specify/shared/guidelines/knowledge-promotion.md
```

Exit `0`. Both present, `4849` bytes each.

```bash
python3 scripts/python/sync-mirrors.py --check
```

Exit `0`. The shared line reads (post-implementation, the documented 122-file shape):

```
ok    shared/ == .specify/shared/ (122 files, byte-identical)
```

```bash
python3 scripts/python/sync-mirrors.py
```

Exit `0`. Write mode on the converged tree wrote nothing: no `DIFF` line, the trailing
line reads `ok    shared/ == .specify/shared/ (122 files, byte-identical)`.

```bash
git diff --name-only 0419adae5..HEAD | wc -l
```

`118` committed paths at this run's HEAD (`63fdca3f7`) — the plan-time count (18) and the
tasks-generation count (43) both grew with later stages; the containment invariant is
"every path ∈ FR-009's declared set", re-derived in `test-evidence/containment.txt`.

```bash
/usr/local/bin/python3 -c 'import pytest,sys; print(pytest.__version__, sys.version.split()[0])'
```

Exit `0`: `8.4.2 3.11.11` (the profile `python3` still imports no pytest; the runner is
given `SPECKIT_PYTHON=/usr/local/bin/python3`).

## S-1 — Module shape: five documents, one table, four links (route b)

Pin executed through the single entry (legs (a) and (f)):

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh -q \
  -k "module_document_set or relative_links" tests/contract/test_general_best_practices.py
```

Exit `0`; `2 passed in 6.27s`. The guard's own steps confirm: 5/5 documents
(`ls` above), the sole table 3 columns / 4 data rows, one relative link per row, the
link-target set = the four owner files, `封闭集` present; 4/4 manifest → owner-file
links resolve.

## S-2 — Placeholder ⇔ zero entries (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh -q \
  -k "owner_files" tests/contract/test_general_best_practices.py
```

Exit `0`; `1 passed in 6.27s`. Leg (b) asserts the equivalence (never a frozen count):
delivery state = 3 placeholder lines ⇔ 3 empty owner files, `programming-tools.md` at
1 entry and 0 placeholders.

## S-3 — Seed entry: three facts and the SSH extension (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh -q \
  -k "seed_entry" tests/contract/test_general_best_practices.py
```

Exit `0`; `1 passed in 6.26s`. Leg (c): default-HTTPS practice, the special-repository
flag-the-protocol duty, the `~/.git-credentials` HTTP-vs-HTTPS counter-example and the
SSH 延伸 are all present; no fabricated `**来源**` line.

## S-4 — Accumulation pointers resolve; no second mechanism (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh -q \
  -k "accumulation_pointer" tests/contract/test_general_best_practices.py
```

Exit `0`; `1 passed in 6.29s`. Leg (d): `feedback-utils.py --help` lists `record`
(also read directly in S-0); `shared/guidelines/knowledge-promotion.md` exists; the
manifest carries `[best-practice]`; zero `best-practices*.py` under `scripts/python/`
(2/2 pointers, marker present, engine-file count 0).

## S-5 — Framework-map registration row in source and mirror (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh -q \
  -k "framework_map_registration" tests/contract/test_general_best_practices.py
```

Exit `0`; `1 passed in 6.27s`. Direct readings (2026-11-27): each of
`shared/definitions/framework-map.md` and its mirror carries exactly `1` row containing
both `.specify/shared/best-practices/` and `Feature 111` (line 56 in both), with the
manifest `README.md` pointer and `(framework source: shared/best-practices/)` in the
Notes cell.

## S-6 — Mirror regeneration and zero drift (route b)

Executed in S-0 above: write mode exit `0` with nothing to write (converged), then
`--check` exit `0` with zero `DIFF` and `ok  shared/ == .specify/shared/ (122 files,
byte-identical)`. Byte identity is adjudicated solely by
`tests/contract/test_mirror_parity_suite.py` — `888 passed`, rc `0`, 0 failed names
(T013 reading, `notes/us3-green.txt`).

## S-7 — Init distribution proof (route b)

Evidence 1 — code path (executed now):

```bash
sed -n '2743,2757p' src/specify_cli/__init__.py
```

Exit `0`; shows the wholesale copy of `resource_path / "shared"` into
`<project>/.specify/shared` via `copy_tree_with_rewrite` (lines 2743–2754 cited in
`test-evidence/init-distribution-proof.txt`).

Evidence 2 — existing integration test `tests/integration/test_init_new_layout.py`
through the single entry: exit `0`, `1 passed in 7.50s` (executed in T014, recorded in
`test-evidence/init-distribution-proof.txt`).

Evidence 3 — the recorded read-only drill under `.specify/.tmp/` (source-run CLI,
`--here --ai qoder --script sh --no-git`): exit `0`; the drill's
`.specify/shared/best-practices/` listing is exactly the five documents; the drill
directory was torn down after the reading. Recorded in
`test-evidence/init-distribution-proof.txt`.

## S-8 — Guard red-first then green (route b)

Green form as written (the `<evidence path>` placeholder resolved to the T015 names
file):

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_general_best_practices.py -q \
  --names-out .specify/specs/111-general-best-practices/test-evidence/us3-names.txt
```

Exit `0`; `6 passed in 6.25s`; `# failed-name list written: …/us3-names.txt (0 entries)
passes=1`.

Red-first record: `notes/red-first-evidence.md` — the same guard executed before the
module landed failed with `6 errors` on the missing module (command, real output and
exit code recorded there).

## Teardown

The init drill directory (`.specify/.tmp/p2-package/init-drill`) was removed after its
reading; only the git-ignored raw log `.specify/.tmp/p2-package/init-drill.log` remains
under the sanctioned temp root. No other scratch was created.