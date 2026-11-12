# Quickstart — Feature 101 (Anchor / Goal realignment)

**Premise legend** — every emitted command below is one of:

- **[today]** — executable against the current tree; the `Expected` reading was measured at plan time.
- **[premise]** — depends on the implement-stage tree (`anchor.md`, four-member `--scope`, the
  `cleanup` action group, `/speckit.anchor`). Not runnable now; executable after WP-01…WP-05.
- **[pin]** — a premise a contract test must fail on if it is not delivered; the test is named.

Repository root: `/storage/project/cloud-native-ai/spec-kit`. All engine commands go through
`python3 .specify/scripts/python/goal-utils.py`; all test runs go through `scripts/bash/run-tests.sh`
(never the bare test CLI).

## S-0 — Baseline orientation [today]

```bash
python3 .specify/scripts/python/goal-utils.py --scope goal list --json
ls .specify/teams/*/team.md | wc -l                 # 20 team definitions
grep -l '^goal_slug:' .specify/teams/*/team.md | wc -l   # 16 of them carry a binding
```

**Expected**: the anchor layer lists **14** definitions (all 14 directories are definitions); the team
layer holds **20** definitions, **16** of which carry `goal_slug`. The engine's `list` action ignores
`--scope` today and always enumerates the anchor store — so the team count is read from the frontmatter,
not from `list`. All three commands are read-only.
**Note for implement**: `list` gaining a Goal-store reading is C-27's change; a team **listing** surface is
deliberately not added (`--scope teams list` exits 2 `scope-not-applicable`).

## S-1 — Authoring an Anchor [premise]

```bash
python3 .specify/scripts/python/goal-utils.py --scope anchor create <new-anchor> \
  --objective "<outcome, not steps>" --criterion "<verifiable criterion>" --json
test -f .specify/anchoring/<new-anchor>/anchor.md && ! test -e .specify/anchoring/<new-anchor>/goal.md
```

**Expected**: one new directory, one `anchor.md`, no `goal.md`. The objective is rejected when it
describes steps rather than an outcome (GD-2/GD-3 unchanged).
**Pin**: `tests/contract/test_anchor_definitions.py` — the anchor store's definition filename is
`anchor.md`, and `create` never writes `goal.md`.

```
/speckit.anchor create
```

**Pin**: `tests/contract/test_anchor_command_surface.py` — `templates/commands/anchor.md` exists, its
`argument-hint` names exactly seven modes (`create` / `view` / `modify` / `targets` / `migrate` /
`migrate-archive` / `coordinate`), the four per-tool copies exist, and `templates/commands/anchor.md`
does **not** enumerate the `--scope` value set (it cites the owner instead).

## S-2 — Anchor view, lifecycle, Targets [premise]

```bash
python3 .specify/scripts/python/goal-utils.py --scope anchor list --json
python3 .specify/scripts/python/goal-utils.py --scope anchor status <anchor> --set achieved --json
python3 .specify/scripts/python/goal-utils.py --scope anchor targets <anchor> --list --json
```

**Expected**: `status --set` performs a lifecycle transition into a terminal state (`achieved` /
`abandoned`); reopening out of a terminal state is accepted only when the definition's binding says
`owner: human`, otherwise exit 2 naming the binding. Targets render as `T-NNN` with
`open|done|dropped`; `--check "<statement>"` validates shape with zero writes.

## S-3 — Action-level Goal [premise]

```bash
python3 .specify/scripts/python/goal-utils.py --scope goals goal-create <goal> \
  --guidance "<what to do now>" --done "<completion condition>" --title "<heading>" --json
test -f .specify/goals/<goal>/goal.md
python3 .specify/scripts/python/goal-utils.py --scope goals goal-list --json
python3 .specify/scripts/python/goal-utils.py --scope goals goal-status <goal> --json
```

**Expected**: the definition lands in `.specify/goals/<goal>/goal.md` ([[STR-002]]) with
`status: active` and a binding record; `goal-create` requires at least one `--done`; the anchor store
is byte-unchanged. `goal-status` without `--set` only reports.
**Pin**: `tests/contract/test_goal_store_write_boundary.py` — a `goal-*` write whose target resolves
into `.specify/anchoring/**` fails `cross-layer-write` (exit 2) with zero writes; a slug existing in
both stores is refused with both candidates named.

## S-4 — The four-mode Goal command and its named rejection [premise]

```
/speckit.goal create      → accepted
/speckit.goal view        → accepted
/speckit.goal modify      → accepted
/speckit.goal status      → accepted
/speckit.goal targets     → refused
```

**Expected** on `targets`: exit 2 with the literal `anchor-only-mode` ([[STR-007]]), a message naming
`/speckit.anchor`, no fallback to `view`, zero writes. The same refusal applies to `migrate`,
`migrate-archive` and `coordinate`.
**Pin**: `tests/contract/test_goal_command_surface.py` — exactly four modes in `argument-hint`; each
Anchor-only mode produces the literal refusal; `/speckit.goal` resolving as the anchor-authoring entry
turns the test red.
**Contract**: `contracts/goal-command.contract.md` C-14.

## S-5 — Cleanup: check → apply → re-apply [premise]

```bash
python3 .specify/scripts/python/goal-utils.py cleanup --check \
  --classification .specify/specs/101-anchor-goal-realignment/classification.json --json \
  | tee .specify/specs/101-anchor-goal-realignment/test-evidence/cleanup-check-$(date +%F).json

python3 .specify/scripts/python/goal-utils.py cleanup --apply \
  --classification .specify/specs/101-anchor-goal-realignment/classification.json --json

python3 .specify/scripts/python/goal-utils.py cleanup --apply \
  --classification .specify/specs/101-anchor-goal-realignment/classification.json --json
```

**Expected**: the check names 9 `anchor` / 2 `action-goal` / 2 `obsolete` entries plus the team
dispositions, with zero writes; the first apply performs the actions and writes one receipt per acted
entry; the second apply reports every entry `already-*`, exits 0, and produces **no diff** (SC-007).
**Pin**: `tests/contract/test_cleanup_idempotency.py` (two applies, no second write) and
`tests/contract/test_cleanup_resume.py` (interrupted before `remove-source`, and after
`write-receipt`; I5 state is exit 4 and is never silently repaired).
**Contract**: `contracts/migration-cleanup.contract.md` C-41 / C-42 / C-44.

## S-6 — Post-convergence invariants [premise]

```bash
ls .specify/anchoring/*/goal.md 2>/dev/null            # expect: nothing
grep -rn "goal_slug" .specify/teams .specify/anchoring .specify/goals .specify/agents \
  .specify/skills .specify/teams.md 2>/dev/null        # expect: nothing
python3 .specify/scripts/python/goal-utils.py --scope anchor binding <anchor> --json
```

**Expected**: no action-level definition remains in the anchor store; no `goal_slug` remains on a live
definition surface; every `anchor_slug` on disk resolves to an existing `anchor.md`. An **archived**
team carries no binding line — its provenance (`bound_slug`, reason) lives in
`.specify/teams/<slug>/disposition-receipt.json`, which is what keeps FR-066 satisfiable without a
false reference.
**Pin**: `tests/integration/test_101_convergence.py` — all three readings asserted on a fixture tree.

## S-7 — Protected history is untouched [today]

```bash
git diff --stat d7c9da7a3 -- .specify/specs/037-* .specify/specs/038-* .specify/specs/042-* \
  .specify/specs/074-* .specify/specs/085-* .specify/specs/094-* .specify/teams/*/runs \
  .specify/archive .specify/history docs/notes
```

**Expected**: empty output for every **baseline-existing** path ([[FR-061]] / FR-069). The one
permitted shape is an **addition** under `.specify/archive/anchoring/**` (the new archival destination the
feature itself creates, PLAN-EDIT 4); it shows as `??`/new files, never as a modification or deletion of an
existing entry — those must be counted and listed separately by G-8. A record being old is never a reason
to rewrite it.

## S-8 — Residue scan (the SC-001 criterion) [pin]

```bash
bash scripts/bash/run-tests.sh tests/contract/test_live_semantic_residue.py -q
```

**Expected** at implement exit: the four classes read `C1 0 · C2 0 · C3 0 · C4 0` over the live roots
declared in `research.md` §5, against the plan-time baseline `C1 4 · C2 0 · C3 7 · C4 15 · total 26`
(`test-evidence/live-semantic-scan-baseline-2026-11-12.txt`). The test file **does not exist at plan
entry** — G-6 creates it in WP-05 with the injection case. The scan roots, the excluded sets and the
patterns have one owner (that declaration + the contract test); adding a root or an exclusion is a plan
revision, never an ad-hoc exemption. The **injection case** must still fire: a freshly injected
old-semantic sentence under a live root turns the scan red.
