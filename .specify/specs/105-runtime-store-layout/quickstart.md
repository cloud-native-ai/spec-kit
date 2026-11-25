# Quickstart — Runtime Store Layout (105)

**Spec**: `requirements.md` · **Plan**: `plan.md` · **Date**: 2026-11-25

Every scenario states its **premises** and the **route** by which its commands are validated. Route (a) = executed during the implementing run with real output kept; route (b) = pinned by the named contract/integration test, with the premises listed so the next stage re-measures instead of inheriting. No example is assumed to work because it looks right.

Scratch workspaces use the sanctioned root `.specify/.tmp/` (git-ignored, per temp-directory discipline); each scenario deletes only the directory it created.

## Scenario 0 — Read the baseline (route a, measured 2026-11-25)

```bash
git ls-tree -d 23938f22e:.specify/memory
git ls-files .specify/memory | awk -F/ '{print $3}' | sort | uniq -c | sort -nr
git check-ignore -v .specify/memory/sanitize/findings.json .specify/memory/trigger/telemetry.jsonl .specify/tools/system.json
```

Observed: 12 baseline children; per-store counts 1630/568/526/146/45/26/10/10/4/3/2/1; ignore rules `memory/sanitize/`, `memory/trigger/telemetry.jsonl`, `tools/` (full output `test-evidence/plan-gates.txt`).

## Scenario 1 — A client project upgrade (old layout only)

**Premises**: client workspace `WS` containing `.specify/memory/` with at least one entry per store; the updated CLI installed (`specify migrate` with the `store-layout` dimension); no concurrent engine writer; same filesystem for source and target.

```bash
WS="$PWD/.specify/.tmp/quickstart-105/legacy"     # built by tests/fixtures/store-layout-105/builders.py
specify migrate --workspace "$WS"                  # dry-run: zero writes, exit 1 "planned"
specify migrate --workspace "$WS" --apply          # exit 0 "applied"
diff -r "$WS/expected-snapshot" "$WS"              # fixture-provided content snapshot; byte-identical stores
ls "$WS/.specify"                                  # session knowledge feedback ... migrate; no memory
test ! -e "$WS/.specify/memory"
specify migrate --workspace "$WS"                  # exit 0 "clean"; a second --apply moves nothing
rm -rf "$WS"
```

**Pinned by**: `tests/integration/test_store_layout_migration_us1_us2.py`（legacy fixture: dry-run zero-write, apply relocates, byte comparison, container absent, rerun no-op). **Route b**.

## Scenario 2 — Old and new both contain data (refusal)

**Premises**: `WS` = `build_dual`（one store has authoritative entries under both `.specify/memory/<store>/` and `.specify/<store>/`）.

```bash
specify migrate --workspace "$WS" --format json    # exit 1 "planned"; one refuse item
# the item names .specify/memory/<store>/ and .specify/<store>/ and the repair entry
specify migrate --workspace "$WS" --apply           # exit 3 "blocked"; both trees unchanged
```

**Pinned by**: `test_store_layout_migration_us1_us2.py::test_dual_content_refuses`（both trees hashed before/after）. **Route b**.

## Scenario 3 — Fresh initialization

**Premises**: empty directory; the updated package seed (`seed/`).

```bash
WS="$PWD/.specify/.tmp/quickstart-105/fresh"; mkdir -p "$WS"
specify init "$WS" --here --ai qoder --script sh --no-git
find "$WS/.specify" -maxdepth 1 -type d | sort
test ! -e "$WS/.specify/memory"
rm -rf "$WS"
```

Observed expectation after the feature: `.specify/session` and `.specify/knowledge` exist; no `.specify/memory`; other stores appear only when their owners run.

**Pinned by**: `tests/integration/test_init_new_layout.py` (fresh-init tree, anchors at `.specify/`, core-asset list). **Route b**.

## Scenario 4 — Temporary memory and persistence under the new roots

**Premises**: a fixture workspace after init; `SPECKIT_PYTHON` resolves an interpreter with pytest for the test entry.

```bash
python3 .specify/scripts/python/memory-utils.py --action record \
  --workspace-root "$WS" --scope session --source "/speckit.plan" \
  --title "new root" --tags "layout" --content "session entry lives under .specify/session"
python3 .specify/scripts/python/memory-utils.py --action recall \
  --workspace-root "$WS" --scope all --query "new root" --format json
python3 .specify/scripts/python/run-determination.py --action determine \
  --workspace-root "$WS" --unit-id "/speckit.quickstart" --unit-type command --run-id demo
```

Observed expectation after the feature: the entry file is under `$WS/.specify/session/`; recall returns it; the determination record lands in the same tier and is retrievable by `--action history`.

**Pinned by**: `tests/integration/test_memory_preservation.py` and `test-evidence` fixture rows in `contracts/memory-and-injection.contract.md` P-5. **Route b**.

## Scenario 5 — Dispatch with a memory-recall child

**Premises**: a dispatch fixture whose child declares `memory-recall`; a pre-seeded session entry.

```bash
# fixture harness renders the payload; assertions are in the test
python3 -m pytest tests/integration/test_dispatch_injection_paths.py -q
```

Observed expectation after the feature: the seven downlink fields, four injections and five uplink elements are present; every injected memory reference resolves under `.specify/session/` or `.specify/knowledge/`; a token written only to feedback/exec-quant is never recalled.

**Pinned by**: `tests/integration/test_dispatch_injection_paths.py`. **Route b**.

## Scenario 6 — Tools domain: records tracked, inventories ignored

**Premises**: a fixture workspace with `.specify/tools/<name>.md` and `.specify/tools/system.json`.

```bash
git -C "$WS" check-ignore -v .specify/tools/system.json   # matches tools/*.json
git -C "$WS" ls-files .specify/tools                      # lists <name>.md only
cmp .specify/.gitignore "$WS/.specify/.gitignore"         # template and installed copy identical
```

**Pinned by**: `tests/contract/test_tools_domain.py` and `tests/contract/test_specify_gitignore_template.py` (updated patterns). **Route b**.

## Scenario 7 — Dogfood: this repository converges

**Premises**: all feature tasks closed up to the dogfood task; the repo's `.specify/memory/` still holds its runtime records; no concurrent process writes `.specify/`.

```bash
PYTHONPATH=src /usr/local/bin/python3 -c "from specify_cli import main; main()" \
  migrate --workspace . --apply
ls .specify | sort                       # 14 store roots; no memory
test ! -e .specify/memory
python3 scripts/python/sync-mirrors.py --check   # member set vs the recorded 450-DIFF baseline
.venv/bin/python3 scripts/python/regen-command-copies.py --check
```

Observed expectation after the feature: all 2,971 tracked entries live under the new roots; `git log --follow` traces them; the receipt records each store's manifest; the retired root is absent; mirror readings are compared as **member sets** against the recorded baseline (L-6).

**Pinned by**: the implement-stage dogfood task plus `tests/contract/test_runtime_store_layout.py::test_repo_has_no_retired_root`. **Route b**.

## Scenario 8 — Live-reference containment (SC-006)

```bash
# framework source class
grep -rn --include='*.md' --include='*.py' --include='*.sh' --include='*.yaml' --include='*.template' \
  '\.specify/memory/' templates/ skills/ shared/ scripts/ src/
# runtime guides
grep -n '\.specify/memory/' .specify/instructions.md .specify/glossary.md
# current docs
grep -rn '\.specify/memory/' docs/ | grep -vE 'docs/(reference/history|decisions|archive|static)/'
```

Observed expectation after the feature: the framework-source output lists only the four allowlisted files (tombstone row, migrate segment, anchor migration engine, legacy residue scanner); the other two classes are empty. The guard asserts measured = declared and fails on mutation.

**Pinned by**: `tests/contract/test_store_layout_live_refs.py`. **Route b**.

## Notes

- Routes (a) were used only for Scenario 0 and the plan-stage dry-run; full output is kept in `test-evidence/plan-gates.txt` and `test-evidence/plan-migrate-dryrun.json`.
- Every future-state example above is covered by a named test; the premise lists are what `/speckit.tasks` and `/speckit.implement` re-measure.
- Teardown in each scenario removes only the scratch directory the scenario created under `.specify/.tmp/`, never a workspace store.
