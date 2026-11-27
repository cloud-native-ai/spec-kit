# Pre-Change Measurements — 109-prompt-adherence

Purpose: record the measured pre-change baselines (mirror checks, deliverable existence, clause and section counts, store roster, probe registry, implement-entry suite baseline, frozen clause coverage) that every later "no NEW drift" or "count unchanged" claim is judged against.

All measurements below were taken on 2026-11-27 in the worktree
`.specify/.tmp/sdd-loop/worktrees/prompt-adherence`, baseline commit `3aae78863`, before any feature file
was created.

## (a) Mirror and command-copy baselines — the no-NEW-drift referent

Command:

```bash
python3 scripts/python/sync-mirrors.py --check
python3 scripts/python/regen-command-copies.py --check
```

Real output (sync-mirrors.py --check), exit code `0`:

```text
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (23 files, byte-identical)
ok    skills/external/ == .specify/skills/ (439 files, byte-identical)
ok    skills/internal/ == .specify/skills/internal/ (139 files, byte-identical)
ok    agents/ == .specify/agents/templates/ (20 files, byte-identical)
ok    scripts/ == .specify/scripts/ (133 files, byte-identical)
projected[bash-version-guard] .specify/scripts/bash/check-prerequisites.sh <- scripts/bash/check-prerequisites.sh: ok
projected[bash-version-guard] .specify/scripts/bash/generate-instructions.sh <- scripts/bash/generate-instructions.sh: ok
projected[bash-version-guard] .specify/scripts/bash/run-tests.sh <- scripts/bash/run-tests.sh: ok
projected[python-version-bridge] .specify/scripts/python/script-interface-check.py <- scripts/python/script-interface-check.py: ok
projected[python-version-bridge] .specify/scripts/python/script_interface_cli.py <- scripts/python/script_interface_cli.py: ok
projected[python-version-bridge] .specify/scripts/python/sync-mirrors.py <- scripts/python/sync-mirrors.py: ok
ok    shared/ == .specify/shared/ (117 files, byte-identical)
```

Real output (regen-command-copies.py --check), exit code `0`:

```text
OK: all per-tool command copies match the source templates.
```

## (b) Deliverable existence — 15/15 ABSENT

Command (existence check per path; the mechanism is new, so all are absent):

```bash
for p in shared/definitions/prompt-adherence-definitions.md \
  shared/declarations/facts/prompt-adherence-layers.yaml \
  shared/declarations/facts/prompt-adherence-strengths.yaml \
  shared/declarations/facts/prompt-adherence-signals.yaml \
  shared/declarations/facts/prompt-adherence-deviation-classes.yaml \
  shared/declarations/facts/prompt-adherence-reading-status.yaml \
  scripts/python/prompt-adherence.py \
  tests/contract/test_prompt_adherence_declarations.py \
  tests/contract/test_prompt_adherence_engine.py \
  tests/contract/test_prompt_adherence_owner.py \
  tests/contract/test_prompt_adherence_readonly.py \
  tests/integration/test_prompt_adherence_init.py \
  tests/fixtures/prompt-adherence \
  .specify/shared/definitions/prompt-adherence-definitions.md \
  .specify/scripts/python/prompt-adherence.py; do
  if test -e "$p"; then echo "PRESENT $p"; else echo "ABSENT $p"; fi
done
```

Real output (15 lines, all ABSENT):

```text
ABSENT shared/definitions/prompt-adherence-definitions.md
ABSENT shared/declarations/facts/prompt-adherence-layers.yaml
ABSENT shared/declarations/facts/prompt-adherence-strengths.yaml
ABSENT shared/declarations/facts/prompt-adherence-signals.yaml
ABSENT shared/declarations/facts/prompt-adherence-deviation-classes.yaml
ABSENT shared/declarations/facts/prompt-adherence-reading-status.yaml
ABSENT scripts/python/prompt-adherence.py
ABSENT tests/contract/test_prompt_adherence_declarations.py
ABSENT tests/contract/test_prompt_adherence_engine.py
ABSENT tests/contract/test_prompt_adherence_owner.py
ABSENT tests/contract/test_prompt_adherence_readonly.py
ABSENT tests/integration/test_prompt_adherence_init.py
ABSENT tests/fixtures/prompt-adherence
ABSENT .specify/shared/definitions/prompt-adherence-definitions.md
ABSENT .specify/scripts/python/prompt-adherence.py
```

## (c) Contract clause count — 7/7/10/5/3/7 = 39

Command (the counting unit is the line-initial `## C-NNN` definition line):

```bash
grep -cE '^## C-[0-9]+' .specify/specs/109-prompt-adherence/contracts/*.contract.md
grep -hE '^## C-[0-9]+' .specify/specs/109-prompt-adherence/contracts/*.contract.md | wc -l
grep -ohE '\bC-[0-9]+\b' .specify/specs/109-prompt-adherence/contracts/*.contract.md | wc -l
```

Real output (per-file, alphabetical; total; naive-reference trap):

```text
.specify/specs/109-prompt-adherence/contracts/declarations-and-vocabularies.contract.md:7
.specify/specs/109-prompt-adherence/contracts/distribution.contract.md:3
.specify/specs/109-prompt-adherence/contracts/engine-and-read.contract.md:5
.specify/specs/109-prompt-adherence/contracts/guards-and-boundaries.contract.md:7
.specify/specs/109-prompt-adherence/contracts/owner-and-catalog.contract.md:7
.specify/specs/109-prompt-adherence/contracts/reading-semantics.contract.md:10
--- total:
39
--- naive trap:
46
```

The naive form (every `C-NNN` token, including in-body references) reads **46**, not 39 — recorded so a
later count is never judged by the trap value.

## (d) Instructions section-count baseline — 39 / 40

Command:

```bash
grep -c '^## ' templates/instructions-template.md
grep -c '^## ' .specify/instructions.md
```

Real output:

```text
39
40
```

The template carries 39 `## ` sections and the installed instructions file carries 40 at the pre-change
baseline; the no-new-section reading later compares against these two numbers.

## (e) Store roster and probe-registry counts

Command (store roster read through the one declaration reader, framework-source form; `statement.stores`
is a mapping keyed by store name):

```bash
python3 - <<'EOF'
import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location("declaration_reader", "scripts/python/declaration_reader.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
fact = mod.load_fact(Path.cwd(), "runtime-store-layout")
stores = fact["body"]["statement"]["stores"]
print("store_count:", len(stores))
print("names:", sorted(stores))
print("any_root_key:", any("root" in entry for entry in stores.values()))
EOF
```

Real output:

```text
store_count: 14
names: ['coaching', 'evidence', 'exec-quant', 'feedback', 'housekeeping', 'knowledge', 'migrate', 'renumber', 'retention', 'sanitize', 'session', 'todo', 'tools', 'trigger']
any_root_key: False
```

The roster carries **14** store names and **no per-store `root` key** — every root is the documented
`.specify/<store-name>/` projection.

Command (probe registry counts):

```bash
python3 .specify/scripts/python/probe-utils.py --action probes --format json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('available:', d.get('available')); print('classes:', len(d.get('classes', []))); print('objects:', len(d.get('objects', []))); print('errors:', d.get('error_count', d.get('errors', 0)))"
```

Real output:

```text
available: True
classes: 11
objects: 130
errors: 0
```

## (f) Implement-entry full-suite baseline — single run

Command (the stage's one full-suite baseline capture; `--names-out` is the comparison surface):

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh --full \
  --names-out .specify/specs/109-prompt-adherence/baseline-failed.txt
```

Real output (runner header, summary line and names-file line; the process exit code is `1` — pytest's
own failure exit, carried by the pre-existing suite state, not by this feature's files, which are all
still ABSENT at this point):

```text
# test runner: /usr/local/bin/python3 -m pytest -n auto --dist load  
# test runner: mode=parallel workers=auto dist=load passes=2 tier=full excluded_slow=0
==== 222 failed, 10277 passed, 3 skipped, 1538 warnings in 83.79s (0:01:23) ====
# failed-name list written: .specify/specs/109-prompt-adherence/baseline-failed.txt (222 entries) passes=2
```

Recorded reading: **exit code 1; 10277 passed; 222 failed; 3 skipped; 222 failed names** in
`.specify/specs/109-prompt-adherence/baseline-failed.txt` (the GATE-1 comparison baseline; later
regression is judged by `comm -13 baseline current`, never by count).

## (g) Frozen clause-coverage baseline

Command (positional target form; the accountant only prints, the redirect is the freeze):

```bash
python3 scripts/python/account-clause-coverage.py .specify/specs/109-prompt-adherence --freeze \
  > .specify/specs/109-prompt-adherence/coverage-baseline.txt
```

Real output: exit code `0`. Frozen file
`.specify/specs/109-prompt-adherence/coverage-baseline.txt` — **787 lines** (2 header lines + 785 frozen
`UNCOVERED:` clause names). Header fields:

```text
# frozen-from: .specify/specs/*/contracts/* excluding 109-prompt-adherence | ... | base-sha: 3aae7886357b | files: 338 (parsed 227 + named 111)
```

Recorded header values: `base-sha: 3aae7886357b`; `files: 338 (parsed 227 + named 111)`; the frozen set
excludes this spec's own contracts, so a later accounting can claim this feature's clauses without its own
baseline exempting them.