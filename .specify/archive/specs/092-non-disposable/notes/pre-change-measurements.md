# 092 pre-change measurements (T037)

Taken at the start of the P1 implement package, before the first edit of this session.

The four readings the owner page § Capture Rule requires. Raw command output, unedited.

The baseline is taken **after** the first P1 edits of this session (the owner page, the fact, the framework-map
row, the glossary rows, the team.md handoff record and the notes land in this package). Both the failing node-id
list and the mirror-baseline line therefore describe the tree **as it stands when the freeze is taken**, not the
tree at session start — and that is what GATE-1 compares against. The session-start mirror reading was `DRIFT
detected` because the three P1 files had just been written; the freeze-time reading is clean.

## mirror-baseline

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files, byte-identical)
ok    skills/external/ == .specify/skills/ (416 files, byte-identical)
ok    skills/internal/ == .specify/skills/internal/ (139 files, byte-identical)
ok    agents/ == .specify/agents/templates/ (17 files, byte-identical)
ok    scripts/ == .specify/scripts/ (121 files, byte-identical)
projected[bash-version-guard] .specify/scripts/bash/check-prerequisites.sh <- scripts/bash/check-prerequisites.sh: ok
projected[bash-version-guard] .specify/scripts/bash/generate-instructions.sh <- scripts/bash/generate-instructions.sh: ok
projected[bash-version-guard] .specify/scripts/bash/run-tests.sh <- scripts/bash/run-tests.sh: ok
projected[python-version-bridge] .specify/scripts/python/script-interface-check.py <- scripts/python/script-interface-check.py: ok
projected[python-version-bridge] .specify/scripts/python/script_interface_cli.py <- scripts/python/script_interface_cli.py: ok
projected[python-version-bridge] .specify/scripts/python/sync-mirrors.py <- scripts/python/sync-mirrors.py: ok
MISS  .specify/shared/declarations/facts/non-disposable-review-surface.yaml
MISS  .specify/shared/definitions/non-disposable-definitions.md
DIFF .specify/shared/definitions/framework-map.md
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
exit=2
```

## instructions-bytes

```text
$ wc -c .specify/instructions.md
35821 .specify/instructions.md
exit=0
```

## constitution-pins

```text
$ grep -c '^### ' .specify/memory/constitution.md; grep -c '^### ' templates/constitution-template.md
27
21
exit=0
```

## worktree

```text
$ git status --porcelain
 M .specify/memory/glossary.md
 M .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt
 M .specify/specs/092-non-disposable/team/092-non-disposable/team.md
 M shared/definitions/framework-map.md
?? shared/declarations/facts/non-disposable-review-surface.yaml
?? shared/definitions/non-disposable-definitions.md
exit=0
```

## freeze-time re-reads

The same four commands, re-read after the P1 writes and the `shared/` mirror sync, immediately before the failing
node-id list was frozen.

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
... ok  shared/ == .specify/shared/ (100 files, byte-identical)
exit=0
```

```text
$ wc -c .specify/instructions.md
35821 .specify/instructions.md
```

```text
$ grep -c '^### ' .specify/memory/constitution.md ; grep -c '^### ' templates/constitution-template.md
27
21
```

## failing node-id list (GATE-1's designation)

`notes/baseline-failed-tests.txt` — 50 node ids, sorted, name list only (never a count), produced by:

```text
$ /usr/local/bin/pytest tests/contract -q -p no:cacheprovider -rf
50 failed, 6369 passed, 3 skipped in 495.45s
```

The failures are pre-existing on this trunk and each one is named; GATE-1 re-reads the list after the implement
packages and compares **names**, not the number. `tests/contract/test_expression_compatibility.py::test_c2_no_project_side_classification_store`
is one of the 50 and is **not** repaired by this feature: its two offender lines
(`.specify/memory/features.md:96`, `.specify/memory/features/088.md:62`) belong to features 077/088, sit outside
this feature's territory, and are named here so the next reader does not read them as a 092 regression.
