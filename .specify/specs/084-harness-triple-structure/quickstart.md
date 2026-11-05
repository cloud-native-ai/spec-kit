# Quickstart — 084 Harness 三重结构（markdown + yaml + script）

**Date**: 2026-11-05 | **Branch**: `084-harness-triple-structure` @ `171c2ff8`
**How to read this file**: each scenario states its route. **Executed** means the command was run on this branch and its
real output is pasted. **Route (b)** means the component does not exist yet on this branch, so the step is pinned by
the contract test named next to it — and its premises are listed, so a later stage re-measures them instead of
inheriting them. No scenario mixes the two.

---

## S1 — Toolchain pins（Executed）

```bash
python3 --version
python3 -m pytest --version
git --version
```

Output (2026-11-05):

```text
Python 3.11.13
pytest 9.2.0
git version 2.43.7
```

The interpreter satisfies the declared `requires-python >= "3.8"`; pytest matches the pin already recorded in the
spec's runtime row. `bash scripts/bash/run-tests.sh --collect-only -q tests/contract/test_requirements_checker.py`
prints `# test runner: python3 -m pytest …` on stderr, i.e. the runner resolves `python3` on this host.

## S2 — Mirror baseline before any edit（Executed）

```bash
python3 scripts/python/sync-mirrors.py --check
```

Output: six pairs reported `ok` (per-tool command copies match; `scripts/ == .specify/scripts/` 119 files;
`shared/ == .specify/shared/` 62 files), exit 0. This is the baseline every later mirror claim is compared against.

## S3 — What the candidate screen enumerates today（Executed）

```bash
ls templates/commands/*.md | wc -l
ls skills/external/*/SKILL.md skills/internal/*/SKILL.md | wc -l
ls shared/workflow/*.md | wc -l
ls shared/definitions/*.md | wc -l
```

Output: `27`, `53`, `19`, `12`. The first three groups are unit carriers; the fourth is the fact-owner surface and is
explicitly not a unit. These are readings of today's tree — the screen recomputes them on every run and no number here
is embedded in the implementation.

## S4 — Distribution: two routes, two different trees（Executed）

Route A — the console script on `PATH`:

```bash
mkdir -p .specify/.tmp/084-quickstart && cd .specify/.tmp/084-quickstart
specify init demo --ai claude --script sh --no-git --ignore-agent-tools
find demo/.specify/shared -name '*.md' | wc -l
```

Output: `Project ready.` and `55`. Fifty-five is the **installed** snapshot's file count, not this branch's (62).

Route B — the source checkout ahead of the installed package:

```bash
PYTHONPATH=/storage/project/cloud-native-ai/spec-kit/src:$PYTHONPATH \
  python3 -c "from specify_cli import main; main()" init demo3 --ai claude --script sh --no-git --ignore-agent-tools
find demo3/.specify/shared -name '*.md' | wc -l
ls demo3/.specify/shared/definitions | wc -l
```

Output: exit 0, `62`, `12` — the working tree, with its nested subdirectories copied. Transcript kept at
`test-evidence/specify-init-source-route.txt`. Teardown:

```bash
rm -rf .specify/.tmp/084-quickstart
```

Conclusion for readers of the closure verdict: distribution is measured on route B (see `EP-002`).

## S5 — The checker's three actions（Route (b)）

`scripts/python/harness-triple-check.py` does not exist on this branch. Pinned by
`tests/contract/test_harness_triple_structure.py`; premises per line:

```bash
# premises: the engine exists at this path and is mirrored into .specify/scripts/python/;
#           exit 0 needs every candidate declared or excluded, which holds only after batch 1.
python3 scripts/python/harness-triple-check.py --action coverage

# premises: --json-out writes exactly one report; the report schema is the contract's, not a second file's.
python3 scripts/python/harness-triple-check.py --action verify --json-out .specify/specs/084-harness-triple-structure/test-evidence/triple-verify.json

# premises: the unit path resolves on the tree under judgement; the summary names slugs and kinds, never values.
python3 scripts/python/harness-triple-check.py --action lookup --unit-id shared/workflow/feedback-step.md
```

Expected shape (not an expected exit code — that is measured, never pre-written here): `coverage` prints one line per
candidate with its disposition and, for in-scope units, the completeness state; `verify` prints only the closed reason
instances; `lookup` prints one unit's or one fact's summary.

## S6 — Migrating one batch-1 fact, end to end（Route (b)）

Worked on `feedback-prompt-threshold`, the smallest row of `contracts/migration-batches.contract.md` MB-01.

1. **Read today's two faces** before touching anything:
   `grep -n "DEFAULT_THRESHOLD" scripts/python/feedback-utils.py` and
   `grep -n "defaults to" shared/workflow/feedback-step.md`. Premise: the line numbers in `research.md` § R5 are from
   this branch and move with any edit.
2. **Write the declaration** `shared/declarations/facts/feedback-prompt-threshold.yaml` — kind `threshold`,
   `consumers: [scripts/python/feedback-utils.py, shared/workflow/feedback-step.md]`,
   `former_carriers: [shared/workflow/feedback-step.md]`. Premise: the file passes the subset (schema DS-08).
3. **Delete the engine's inline constant and read through the shared entry** — premise: `import declaration_reader`
   resolves because the script's own directory is `sys.path[0]` under `python3 scripts/python/<name>.py`.
4. **Turn the carrier's literal into a pointer** — premise: the reused `duplicate-fact` reading, run as
   `python3 scripts/python/doc-consistency-check.py --action verify --faces duplicate --spec-dir <spec>`, reports zero
   hits for that fact (the same command exits 0 with zero findings today).
5. **Run the batch reading**: `--action coverage` shows the unit as in-scope with state `complete`, and
   `--action lookup --unit-id shared/workflow/feedback-step.md` names the slug. Premise: a locatable read point exists
   in the engine (a reference to the read entry plus the slug) — the contract states plainly that this is a textual
   locator, not a proof of semantics.
6. **Prove the gate still behaves**: `bash scripts/bash/run-tests.sh -q tests/contract` and compare failures id-by-id
   against the implement-start baseline. Premise: the baseline is taken at implement start; nothing in this plan is a
   substitute for it.

## S7 — Gate wiring stays opt-in（Route (b)）

```bash
# default: today's behaviour, byte-for-byte; the closed four-name finding set is untouched.
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --stage plan --spec-dir <spec>

# opt-in: one added finding source, findings forwarded verbatim.
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --stage plan --spec-dir <spec> --triple-structure
```

Premises: (a) `tests/contract/test_acceptance_premises.py` asserts that the findings a fixture produces are a subset of
the four existing names — so the new source must stay off by default, and that assertion is the guard, not a comment;
(b) the host's module docstring is corrected in the same change to describe the optional delegation (its "no framework
imports" mechanism stays true); (c) the checker absent ⇒ exit-2 label plus an advisory, never a pass.

## S8 — Closing readings（Route (b)）

```bash
python3 scripts/python/sync-mirrors.py --check          # no NEW drift vs S2's baseline
python3 scripts/python/harness-triple-check.py --action verify
git diff --stat 171c2ff8 -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py
```

Premises: the second command exits 0 only when the in-scope set has no `pending` (`SC-002`); the third prints nothing
when the 081 acceptance files are untouched (collected counts today: 40 and 37).
