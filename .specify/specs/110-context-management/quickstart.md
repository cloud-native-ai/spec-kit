# Quickstart — Context Management (上下文的声明、组合与只读审计)

The mechanism's documented single entry is one read-only script:
`python3 .specify/scripts/python/context-audit.py`. The engine is an implementation output of this
feature, so every example that invokes it carries a **per-example premise list** and is pinned by a
contract test named in the same block. Examples over existing carriers were executed at plan time
(2026-11-27) and their measured output is quoted; the full captures live at
`test-evidence/plan-time-reads.txt` and `test-evidence/mirror-baseline-plan.txt`.

## Existing carrier reads (executed at plan time)

```bash
python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:110-context-management"
```

Measured: `flow_class: execution`, `source: declaration` — exit 0.

```bash
python3 scripts/python/declaration_reader.py --action get --fact memory-types --repo .
```

Measured: the parsed `closed-set` fact body (`fact`, `kind`, `consumers`, `former_carriers`,
`statement`, `note`; statement `session`, `knowledge`) — exit 0. This is the shape the four context facts
take.

```bash
grep -c '^## ' .specify/templates/instructions-template.md .specify/instructions.md
wc -c .specify/instructions.md
```

Measured: `39` template sections, `40` live sections (the live-only `## Recurring Operational Lessons` is
pre-existing drift the additive generator preserves); `40170` bytes against the generator's
`INSTRUCTIONS_BUDGET_BYTES=40960` (`scripts/bash/generate-instructions.sh:119`) — a headroom of 789 bytes.
The ambient section's size verdict is the generator's own `BUDGET:` line, never restated here.

```bash
python3 scripts/python/sync-mirrors.py --check
```

Measured: exit 0 — all six pairs byte-identical (templates 23, skills/external 439, skills/internal 139,
agents 20, scripts 133, shared 117) and six per-file projections `ok` (full capture:
`test-evidence/mirror-baseline-plan.txt`). The implementation criterion is no NEW drift against this
baseline.

## Scenario 1 — Audit the repository's own layout

```bash
python3 .specify/scripts/python/context-audit.py --action check
```

Expected: zero findings and exit 0 on this tree; the reading names the owner document and the four facts
it validated.

> **Not executed at plan time** — the engine is an implementation output of this feature. Pinned by
> `tests/contract/test_context_management_engine.py` (check-clean leg) and by SC-001's captured run.
> Premises: the engine is installed at `.specify/scripts/python/context-audit.py`; the workspace root
> resolves from the current directory upward to the nearest ancestor holding `.specify/`, and the layer
> root — owner document plus facts — is that workspace's own declaration layer (`shared/` when the
> framework-source layer is present, else `.specify/shared/`); on this repository the layer reads
> `shared/definitions/context-management-definitions.md` and `shared/declarations/facts/`, whose
> `.specify/shared/` copies are byte-identical mirrors; exit `0` clean.

## Scenario 2 — Manifest the project layer

```bash
python3 .specify/scripts/python/context-audit.py --action manifest --layer project
```

Expected: one line per project-layer roster class in roster order, each reading `present` on this tree,
with the three concept-pointer rows `project-vocabulary`, `concept-definitions` and `concept-explanations`
listing resolvable sources and their cap references; the text ends with one `source-reading: <digest>`
line.

> **Not executed at plan time** — same engine, same premises as Scenario 1, plus: the project-layer
> sources named by the layout table resolve on this tree (`.specify/constitution.md`,
> `.specify/instructions.md`, `.specify/glossary.md`, `.specify/shared/definitions/`, `.specify/skills.md`,
> `.specify/tools.md`, `.specify/skills/`, `.specify/agents/templates/`, `.specify/agents/instances/`,
> `.specify/tools/`, `.specify/features.md`, `.specify/features/`, `.specify/register.md`,
> `.specify/workflow/git.md`, `.specify/shared/declarations/facts/runtime-store-layout.yaml`,
> `.specify/shared/definitions/framework-map.md`, `.specify/shared/guidelines/directory-governance.md`).
> Pinned by `tests/contract/test_context_management_engine.py` (manifest-present leg) and SC-010's
> captured run.

## Scenario 3 — Machine-readable manifest for any layer

```bash
python3 .specify/scripts/python/context-audit.py --action manifest --layer task --json
```

Expected: a JSON object with the ordered top-level keys `action`, `layer`, `rows`, `counts`,
`source_reading`; each row carries `class`, `layer`, `form`, `sources`, `token`, `reason` (null when
present), `cap`; `counts` tallies rows per presence token; exit 0.

> **Not executed at plan time** — pinned by `tests/contract/test_context_management_engine.py`
> (JSON-schema leg). Premises: ordered keys; no timestamps or host values; absence rows included with
> their reasons; `--json` composes with either action; on a fresh-init or fixture tree where
> `.specify/state/` and populated memory tiers are absent, the corresponding rows read `absent` /
> `empty` / `not-evaluated` with reasons (never skipped).

## Scenario 4 — Seeded violation fixtures

```bash
python3 .specify/scripts/python/context-audit.py --action check --workspace-root <fixture-root>
```

Expected, per fixture: an unknown layer token, an unknown form token, a class roster mismatch and an
illegal form for a layer each produce exactly the expected finding and exit `1` — a layout-table unknown
token is a finding, never an input error; declaration-layer unknown members are the exit-`2` input cases
and are exercised by the declarations guard, not by these four fixtures.

> **Not executed at plan time** — pinned by `tests/contract/test_context_management_engine.py`
> (four seeded fixtures; the rule set is C-032). Premises: each fixture carries a minimal owner document
> and the four facts at its own workspace root in the framework-source shape, so the fixture's own
> declaration layer drives the reading; `--workspace-root` selects the audited tree; finding lines name
> file, row and violated rule.

## Scenario 5 — A fresh project, offline

```bash
specify init fresh-dir --ai qoder --no-git --ignore-agent-tools
cd fresh-dir
python3 .specify/scripts/python/context-audit.py --action check
python3 .specify/scripts/python/context-audit.py --action manifest --layer project
```

Expected: `check` exits 0 with zero findings against the declared facts; `manifest --layer project`
completes and prints explicit absence lines for the genuinely absent sources (a fresh project may lack
`.specify/instructions.md`, `.specify/glossary.md`, `.specify/register.md`, `.specify/skills.md`,
`.specify/tools/`, populated memory tiers, `.specify/state/` and `docs/` — measured on a 2026-11-27 probe
of the installed CLI); no socket is opened during either run and nothing is transmitted.

> **Partially exercised at plan time** — the `specify init` step was executed on 2026-11-27 in a scratch
> root (`.specify/.tmp/plan-init-probe/`, since removed) and its fresh-tree anchor set measured; the two
> audit invocations are not executable until this feature ships. Pinned by
> `tests/integration/test_context_management_init.py` (init fixture under a network block; the fixture
> initializes through the repository's own init path, not the stale installed build). Premises: the
> running `specify` must be the build that ships this feature (the installed 0.0.22 in this environment,
> framework commit `fed513bc`, predates it — measured 2026-11-27); `specify init` installs the `shared/`,
> `scripts/` and `templates/` trees under `.specify/`; a fresh project may lack `.specify/tools/` (no Tool
> records yet),
> `docs/` and populated memory tiers, which read as absence tokens with reasons; the absence vocabulary
> is the FR-020 set.

## Scenario 6 — Determinism and containment

```bash
mkdir -p .specify/.tmp
python3 .specify/scripts/python/context-audit.py --action check > .specify/.tmp/run-a.txt
python3 .specify/scripts/python/context-audit.py --action check > .specify/.tmp/run-b.txt
diff .specify/.tmp/run-a.txt .specify/.tmp/run-b.txt
```

Expected: no diff output and exit 0 from `diff`; a SHA-256 manifest of the tree taken before and after
each action is identical and no new file appears (bytecode caches excluded by name).

> **Not executed at plan time** — pinned by `tests/contract/test_context_management_engine.py`
> (determinism legs) and `tests/contract/test_context_management_readonly.py` (hash-manifest legs, C-041).
> Premises: rows print in roster order; no timestamps or host values enter the output; the hash manifest
> excludes `__pycache__`; the run's working directory is outside the fixture tree; `.specify/.tmp/` is a
> sanctioned, git-ignored scratch root (the redirect targets a scratch file, not an artifact).