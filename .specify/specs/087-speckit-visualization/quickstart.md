# Quickstart — Speckit 框架可视化（Speckit Framework Visualization）

**Feature**: 087 | **Date**: 2026-11-06 | **Plan**: `plan.md`

Eight scenarios (A–H) of the obligation read on one screen, each with its executed/unexecuted status stated **per
scenario** — a file-level disclaimer is deliberately absent, because the plan-stage gate treats one as vouching for
the examples it does not cover. Two scenarios (E and G) carry an **executed** measurement taken during this plan
stage; the other six carry the premises they rest on.

**What exists at plan time**: this plan stage authored documents only. None of the delivered *implementation*
artifacts exists yet (`shared/guidelines/reporting-obligations.md`, `agents/reporter.agent.md`,
`templates/commands/status.md`, `scripts/python/status-digest.py`, the create-team guard script), so the commands
below that invoke them cannot run. Everything that *does* exist — the sync engine, the registry engine, the
confirmation-gate scanner, the validators — **was executed** during this stage and its real output is quoted.

---

## Scenario A — Read the obligation's owner (unexecuted; premises stated)

**Goal**: a maintainer finds every fact the obligation owns, and no fact it does not.

```bash
sed -n '1,40p' shared/guidelines/reporting-obligations.md
```

**Expected**: the file opens with a single-source-of-truth declaration naming eight owned facts (the list contract
C-01 fixes) and four documents it does **not** own, each with a path.

**Status**: NOT EXECUTED — the file does not exist at plan time.

**Premises this scenario rests on**:
1. the owner's path is `shared/guidelines/reporting-obligations.md` (fixed by `plan.md` D1 and contract RO-01);
2. the mirror at `.specify/shared/guidelines/reporting-obligations.md` is produced by
   `scripts/python/sync-mirrors.py`, never by hand (contract C-47, premise EP-001);
3. the declaration names four *other* documents — `progress-reporting.md`, `subagent-definitions.md`,
   `patterns.md`, `line-registry.py` — whose sections must still exist when the file lands;
4. the file uses the `sed`-addressable Markdown shape its `shared/guidelines/` siblings use (a level-1 heading, then
   a declaration block), so `sed -n '1,40p'` shows the declaration.

**Verification route (b)**: pinned by `tests/contract/test_reporting_obligations.py`, which asserts the file exists,
carries the declaration, and names the four non-owned owners by path.

---

## Scenario B — Roster validation names a missing reporter seat (unexecuted; premises stated)

**Goal**: a team roster without a reporter seat fails with the seat **named**, and a roster with a recorded reason
passes.

```bash
python3 skills/internal/create-team/scripts/validate-roster.py .specify/teams/<team-slug>/team.md
echo "exit=$?"
```

**Expected**: status `0` when the roster carries a `role: reporter` member (or a `reporting-reason`); status `1`
with a defect line naming `reporter` and the team slug when it does not — and also for the two other defects of the
closed set (an unresolvable `agent`, and two or more reporter rows, each named distinctly by C-16); status `2` on an
unreadable or unparsable file.

**Status**: NOT EXECUTED — the guard script does not exist at plan time.

**Premises this scenario rests on**:
1. the guard's path is `skills/internal/create-team/scripts/validate-roster.py`, beside the two existing helpers
   (`match-team-preset.py`, `verify-territory-disjoint.py`) in the same directory;
2. it takes a team file path as its single positional argument, mirroring `verify-territory-disjoint.py`'s calling
   shape rather than inventing a subcommand grammar;
3. a team file lives at `.specify/teams/<slug>/team.md` (the path `skills/internal/create-team/references/create-mode.md`
   § Team Schema fixes);
4. the defect line is single-line and contains the literal `reporter` (contract RS-03 names the seat literal);
5. the script is stdlib-only (contract RS-08), so plain `python3` runs it with no installed package.

**Verification route (b)**: pinned by `tests/contract/test_roster_reporter_seat.py` over four defect fixtures
(compliant / missing-seat / unresolvable-agent / two-seats — the closed defect set C-16 fixes) plus the
`reporting-reason` value-domain fixture C-17 requires (one per accepted value and one out-of-domain). That is five
fixture cases in total, not three.

---

## Scenario C — Render a digest while runs are active (unexecuted; premises stated)

**Goal**: one bounded summary answers "what is running right now?" without opening a log.

```bash
python3 scripts/python/status-digest.py --action digest --cap 5
echo "exit=$?"
```

**Expected**: a header line (`generated_at`, `cap=5`, `profile_summary`), then at most five entries — active lines
first, descending last-activity age, ties by `line_id` ascending — each showing `line_id`, `run_id`, `state`,
`stage`, `age`, `stale`, and the per-entry agent activity when the entry declares triplet paths. When the cap
truncates the set, a trailing `omitted=<n>` line. Status `0`.

**Status**: NOT EXECUTED — the script does not exist at plan time.

**Premises this scenario rests on**:
1. the script's path is `scripts/python/status-digest.py` and it is mirrored to `.specify/scripts/python/` by the
   **STRICT** `scripts/` pair (a source-only file FAILS `--check`, so both sides must exist);
2. the default registry directory exists and contains at least one entry — measured today:
   `python3 skills/external/sdd-loop-driver/scripts/line-registry.py --action list --all --format json` returned 9
   fields per entry, and `~/.local/state/spec-kit/lines/` holds one `<line_id>.json` per line;
3. `--cap` is the override flag name (contract DG-03 fixes "a declared default, overridable per invocation"; the
   flag spelling is fixed here so the example is runnable);
4. entries carry `updated_at`, and entries for runner-driven lines carry triplet paths (`status_path` /
   `log_path` / `heartbeat_path`) — true for lines registered by `run-stage.sh`, false for hand-registered lines,
   which render `-`;
5. the registry is resolved exactly as `line-registry.py` resolves it, so a `$SPECIFY_LINE_REGISTRY_DIR` override
   in the caller's shell changes what this command reads.

**Verification route (b)**: pinned by `tests/unit/test_status_digest_unit.py` over a 12-entry fixture registry
(cap 5 → 5 entries + `omitted=7`; two renders byte-identical).

---

## Scenario D — Render a digest with nothing running (unexecuted; premises stated)

**Goal**: an idle repository answers explicitly rather than with an empty page.

```bash
SPECIFY_LINE_REGISTRY_DIR="$(mktemp -d)" python3 scripts/python/status-digest.py --action digest
echo "exit=$?"
```

**Expected**: the literal `nothing-running` rendering (one line; no table, no empty header), status `3`.

**Status**: NOT EXECUTED — the script does not exist at plan time.

**Premises this scenario rests on**:
1. the script honours `$SPECIFY_LINE_REGISTRY_DIR` as its first resolution step (contract DG-02, which restates the
   engine's `resolve_registry_dir` order because the script cannot import the engine);
2. a freshly created empty directory counts as "an empty registry", not as an input error (status `3`, not `2`);
3. `mktemp -d` is available (it is; the framework's own scripts assume a POSIX shell);
4. the exit status is `3` — the declared "nothing active" value, distinct from `0` (a rendered digest) and `2`
   (input error) — contract DG-05;
5. the caller's temporary directory is cleaned by the OS; the scenario writes nothing into the repository, so no
   sanctioned temp-root requirement applies (`.specify/shared/guidelines/temp-directory-discipline.md` governs
   **repository** scratch, not a caller's shell temp).

**Verification route (b)**: pinned by `tests/unit/test_status_digest_unit.py` (empty-registry fixture asserts the
literal and the status).

---

## Scenario E — The owner-literal scan (EXECUTED, plan stage; see the measured baseline)

**Goal**: the long-run default has exactly one definition site in the framework sources, and the scan is written
against a **measured** baseline rather than an assumed zero.

### E.1 — Baseline measured during this plan stage (executed)

```bash
grep -rn "30 秒\|30 seconds" shared/ templates/ skills/ agents/
```

Actual output on 2026-11-06 (framework sources, this checkout):

```text
skills/external/draw-diagram/references/types/plantuml/references/howto/19-salt-diagram.md:12:**定位说明**：Salt 不追求高保真视觉——它故意保持手绘线框风格，让用户聚焦**布局与控件**而非配色图标。需要高保真 UI 时请用专业设计工具；Salt 的价值是"30 秒把界面结构写成文本、可进版本库"。
skills/external/improve-skills/references/skill-slimming-principles.md:73:**Failure mode prevented**: SKILL.md becomes a wall of detail; the reader cannot tell what the Skill actually does in 30 seconds.
```

**Reading**: two hits, both unrelated prose (a diagram-tool blurb and a skill-authoring heuristic). **Zero**
framework-source definition of a reporting interval exists today.

**Premises**: (1) the search roots are the four framework-source trees that could hold such a literal; (2) the
pattern matches both the Chinese and English forms; (3) `grep`'s pattern here is an alternation, so
`grep -rn "30 秒\|30 seconds"` relies on basic-regex alternation — the same form the framework's own docs use.

### E.2 — Post-change assertion (unexecuted; premises stated)

```bash
grep -rn "30 秒\|30 seconds" shared/ templates/ skills/ agents/ \
  | grep -v "draw-diagram/references" | grep -v "improve-skills/references/skill-slimming-principles.md"
```

**Expected**: exactly **one** line — the definition site inside `shared/guidelines/reporting-obligations.md`.
A second line means the literal was duplicated and the guard must fail.

**Status**: NOT EXECUTED — the owner document does not exist at plan time, so no post-change reading is possible.

**Premises**: (1) the two exclusions are by path and are exactly the two baseline hits above — a future unrelated
hit would legitimately fail this scan, which is the scan working as designed; (2) the delivered owner carries the
value once and every other consumer (the Template body, the create-team note, the coaching payload, the digest's
profile summary) reaches it by anchor.

**Verification route (b)**: `status-digest.py --action guard` proposition RO-03 implements this scan, and
`tests/contract/test_status_digest.py` includes a **seeded-duplicate drill**: adding the literal to a second file
must turn RO-03 red. That drill is the proof the check is not decoration.

---

## Scenario F — The guard returns a verdict on the line's own artifacts (unexecuted; premises stated)

**Goal**: the mechanically decidable propositions of the obligation get a verdict, and each verdict names itself.

```bash
python3 scripts/python/status-digest.py --action guard
echo "exit=$?"
```

**Expected**: one line per proposition, each `RO-01` … `RO-13` with `pass` / `fail` / `not-evaluated` plus a
reason, then a summary line; status `0` when every proposition is `pass`, `1` when at least one is `fail`, `2` on
input error.

**Status**: NOT EXECUTED — the script does not exist at plan time.

**Premises this scenario rests on**:
1. the thirteen proposition ids are exactly the `RO-01`…`RO-13` names
   `contracts/reporting-obligations.contract.md` C-01…C-13 defines — that file is the propositions' **single owner**,
   and contract C-46 is its consumer, naming each id with only what the guard reads (one vocabulary, one owner: a
   proposition is defined in one place and cited by id everywhere else);
2. `not-evaluated` is a legal verdict and is never counted as a pass (`requirements.md` reports the same rule for
   expression-class gates; here it is the guard's own rule);
3. the guard reads only files on disk — no network, no process spawn (contract OM-04), so it is runnable in a
   sandbox with no host CLI;
4. the exit-status set `0`/`1`/`2` follows the framework's existing convention (`flow-class-check.py`,
   `pre-analyze-check.py`, `gate-check.py`), so no new convention is introduced;
5. a line's own artifacts must exist for a proposition to be `pass` — RO-04 needs at least one roster **path in
   `FR-006`'s population** (a `--roster` argument, or a roster this feature created), RO-05 needs a captured line
   set. With no population path supplied, RO-04 reports `not-evaluated` with that reason rather than `pass`; the
   rosters already in the repository are not in the population and are never judged (`FR-006`, contract
   `contracts/reporting-obligations.contract.md` C-04).

**Verification route (b)**: pinned by `tests/contract/test_status_digest.py` (every proposition name appears in the
output for a compliant fixture; a mutation fixture turns the matching proposition red).

---

## Scenario G — Mirror and copy integrity after the change (unexecuted post-change; baseline EXECUTED)

**Goal**: no NEW drift on any mirror pair this feature touches, and the new command reaches the per-tool copy trees
that exist in this repository.

### G.1 — Baseline (EXECUTED during this plan stage)

```bash
python3 scripts/python/sync-mirrors.py --check
python3 scripts/python/regen-command-copies.py --check
```

Actual output on 2026-11-06:

```text
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (415 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (16 files)
ok    scripts/ == .specify/scripts/ (121 files)
ok    shared/ == .specify/shared/ (94 files)
```

Both commands exited `0`.

### G.2 — Post-change assertion (unexecuted; premises stated)

```bash
python3 scripts/python/sync-mirrors.py --write
python3 scripts/python/sync-mirrors.py --check
python3 scripts/python/regen-command-copies.py
python3 scripts/python/regen-command-copies.py --check
ls .claude/commands/speckit.status.md .github/prompts/speckit.status.prompt.md \
   .opencode/command/speckit.status.md .qoder/commands/speckit.status.md
```

**Expected**: `--check` prints `ok` for every pair and `OK: all per-tool command copies match the source
templates.` (both exit `0`); the four `ls` paths all resolve; the file counts rise by exactly the **new** files this
feature adds, per pair: `agents/` 16 → 17 (one new Template), `shared/` 94 → 95 (one new owner document),
`scripts/` 121 → 122 (one new script), `skills/internal/` 138 → 139 (one new guard script under
`create-team/scripts/`), `templates/commands/` is not mirrored into `.specify/` any more (that pair is retired), and
the edited-but-already-present files (`subagent-definitions.md`, `external-dispatch-recipes.md`, the three
`create-team` files, `coaching-skills/SKILL.md`) change bytes without changing any count.

**Status**: NOT EXECUTED — the pre-change tree is already `ok` on both checks, so there is nothing to regenerate
until the implementation lands.

**Premises this scenario rests on**:
1. the four `ls` paths are exactly the tool directories that exist in this repository —
   `_ASSISTANT_COMMAND_DIRS` (`src/specify_cli/__init__.py:796`) configures six (`copilot`, `claude`, `hermes`,
   `opencode`, `qoder`, `codex`) but only four directories exist in this checkout; naming all six would assert
   files that `regen-command-copies.py` never writes here;
2. the command template's filename is `templates/commands/status.md`, so the generated copies are `speckit.status.*`
   (the generator prefixes `speckit.` and applies `_ASSISTANT_EXTENSIONS`);
3. `sync-mirrors.py --write` is the delivery step and never the target of a hand edit (constitution XI, two hats);
4. the `scripts/` pair is STRICT: a new source file with no mirror FAILS `--check`, so the mirror must be produced
   by `--write` (or `--only scripts/python/status-digest.py`) in the same change;
5. `skills/external/<name>/` mirrors to `.specify/skills/<name>/` (the `external/` component is dropped), so the
   coaching skill's mirror path is `.specify/skills/coaching-skills/SKILL.md`;
6. the per-pair counts rise **by exactly** the new files this feature adds — a larger rise means an unintended file
   shipped, and an unchanged count for a pair that should have gained a new file means the mirror is missing.

**Verification route (b)**: pinned by `tests/contract/test_reporting_obligations.py` (file existence on both sides
of each pair) and by the mirror check itself, whose baseline is the measured `ok` above.

---

## Scenario H — Zero new machinery audit (unexecuted; premises stated)

**Goal**: the changed-file set introduces none of the things the feature prohibits.

```bash
python3 .specify/scripts/python/scan-confirmation-gates.py --summary
git diff --name-only 56f3f881..HEAD
```

**Expected**: the scanner still reports `blocking confirmation gates: 27` (unchanged — the baseline measured
2026-11-06 was `27` with `destructive: 20`, `governance_kept: 7`, `violations: 0`), and the changed-path list
contains no file that spawns a process, keeps a store, or opens a channel (audited by contract
`ownership-map.contract.md` OM-03/OM-04, i.e. C-49/C-50).

**Status**: the scanner half was EXECUTED during this plan stage (measured `27`); the changed-path half is NOT
EXECUTED — it is an implementation-time audit.

**Premises**: (1) the scanner's `--summary` face prints the three counts plus the violation count; (2) the baseline
`27` is the number a compliant change leaves unchanged — an increment is a defect, a decrement means a gate was
removed; (3) `56f3f881` is this line's stage base (`plan.md` header and the state spine's `stage_base_commit`).

**Verification route (b)**: contract `ownership-map.contract.md` C-51 (`OM-05`) plus the AST-level import audit in
`tests/contract/test_status_digest.py`.
