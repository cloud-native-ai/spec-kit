# Non-goals and zero-second-mechanism audit — 105 (T040)

- Date: 2026-11-25
- Run: `r20261125T022857Z-06dd`
- Contract clause: `contracts/store-layout.contract.md` C-8 (normative non-goals).
- Diff base: `a8f4a962f` — the tip before this feature's P1–P4 delivery commits. All commands were
  run at the current tree after P5's US6/guard work; outputs are pasted verbatim (trimmed to the
  decisive lines).

## 1. Zero new store engine / registry / scheduler / second injection mechanism

```console
$ git diff --name-status a8f4a962f..HEAD -- scripts/python src/specify_cli | grep -E '^A'
(no output)
```

- Reading: the feature adds **no file** to the engine surface; every store root is reached through
  the existing single-store engines (path constants only) or through
  `scripts/python/declaration_reader.py` for cross-store readers. `src/specify_cli/__init__.py` is
  the existing CLI/engine, extended in place; no second CLI, registry or scheduler exists.
- Second injection mechanism: `… run-tests.sh tests/integration/test_dispatch_injection_paths.py -q`
  → **7 passed in 6.49s** — the seven downlink fields, four injections and five uplink elements are
  unchanged, every injected memory reference resolves to the two memory tiers, and the reverse-token
  fixture proves feedback/exec-quant records are never recalled as memory. No new payload field or
  retrieval source was added (P-3/P-4).

## 2. Zero new third-party runtime dependencies

```console
$ git diff a8f4a962f..HEAD -- pyproject.toml
@@ -44,7 +44,7 @@ packages = ["src/specify_cli"]
 [tool.hatch.build.targets.wheel.force-include]
-"memory" = "specify_cli/memory"
+"seed" = "specify_cli/seed"
```

```console
$ sed -n '/^dependencies = \[/,/^\]/p' pyproject.toml
dependencies = [
    "typer",
    "rich",
    "httpx[socks]",
    "readchar",
    "truststore>=0.10.4; python_version >= '3.10'",
]
```

- Reading: the only `pyproject.toml` change is the packaged seed namespace (C-7); the runtime
  dependency set is byte-identical to the base (the `dev` extra is pre-existing). The feature's
  added import lines across the engine surface are `+import fnmatch` (CPython stdlib) and nothing
  else:

```console
$ git diff a8f4a962f..HEAD -- scripts/python src/specify_cli | grep -E '^\+(import |from )' | sort -u
+import fnmatch
```

## 3. Entry format and write protocol unchanged (055 protocol; FR-025)

- The changed engine lines are path constants, docstrings and declaration reads. Representative
  diff (memory / feedback / exec-quant / evidence / retention / tools):

```console
-    .specify/memory/session/     # short-term / working memory (append-only)
+    .specify/session/     # short-term / working memory (append-only)
-MEMORY_SUBDIR = Path(".specify") / "memory"
+MEMORY_ROOT = Path(".specify")
-FEEDBACK_SUBDIR = Path(".specify") / "memory" / "feedback"
+FEEDBACK_SUBDIR = Path(".specify") / "feedback"
-EXEC_QUANT_STORAGE_REL = Path(".specify") / "memory" / "exec-quant"
+EXEC_QUANT_STORAGE_REL = Path(".specify") / "exec-quant"
-RETENTION_REL = Path(".specify") / "memory" / "retention"
+RETENTION_REL = Path(".specify") / "retention"
```

- Per-entry-per-file writing still holds for every store — the FR-025 guard is green:

```console
$ … run-tests.sh tests/contract/test_runtime_store_layout.py::test_two_writers_distinct_paths -q
1 passed
```

- Behavior round trips on the new roots are green (SC-002/SC-003/SC-008 modules in
  `test-evidence/t038-sc-suite.txt`, 41 passed overall): memory record→recall, feedback records,
  evidence lanes, exec-quant collection, trigger evaluation, retention lane, determination
  persistence. No shared mutable aggregate was introduced.

## 4. `draft/` has no new home

```console
$ test ! -e .specify/draft ; echo $?
0
$ grep -n 'legacy_retired' -A2 shared/declarations/facts/runtime-store-layout.yaml
113:  legacy_retired:
114-    - draft
$ grep -c 'draft' shared/definitions/framework-map.md
0
```

- Reading: the retired legacy directory has no top-level home, no framework-map row, and only the
  migration's residue path names it (BC16: `migrate:refuse:unknown-residue`, demonstrated by the
  T035 residue fixture — container preserved, every path listed, zero deletion).

## 5. Legacy `git-workflow.md` not rewritten

```console
$ test -e .specify/memory/git-workflow.md ; echo $?
1
$ git cat-file -e 23938f22e:.specify/memory/git-workflow.md ; echo $?
128
$ git diff --stat a8f4a962f..HEAD -- .specify/workflow/git.md
(no output)
```

- Reading: the legacy single file does not exist at the baseline commit and does not exist now, so
  this feature neither rewrote nor resurrected it; its live successor `.specify/workflow/git.md` is
  untouched by this feature's diff. The declaration records it as the unchanged non-store member
  (`legacy_non_store`), and the migration contract deliberately gives it no BC row.

## Verdict

All five C-8 non-goals hold on the current tree: zero new store engine/registry/scheduler/second
injection, zero new third-party dependencies, unchanged entry format and write protocol, no new home
for `draft/`, and no rewrite of `git-workflow.md`. [green: contracts/store-layout.contract.md#C-8]
