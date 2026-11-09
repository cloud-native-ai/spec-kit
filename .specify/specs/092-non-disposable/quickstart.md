# Quickstart — Non-Disposable

**Feature**: 092-non-disposable | **Date**: 2026-11-09 | **Plan**: [`plan.md`](plan.md) · **Data model**: [`data-model.md`](data-model.md)

Ten scenarios (§ 1…§ 10). Each one is written as a **reading**, not as a wish: the command, the expected exit code, and what the
output must show for the scenario to count. Scenarios 1 and 2 run against the tree as it stands today; the rest name
the minimal mutation they need, because an engine proven only on synthetic fixtures proves it can fire, never that it
fires on the defect this feature was written for (`research.md` R13).

Nothing here is a second statement of a rule. The classes, the dispositions, the review surface and the four stages are
owned elsewhere and are **referenced** (see [`feature-ref.md`](feature-ref.md) § Binding).

Environment for all scenarios: `/usr/bin/python3` (3.11.0rc1) and `git`; run from the repository root.

---

## § 1 — Reproduction on the real tree: `false-closed-set` and `status-unreadable` (corpus A2)

**Why first.** This is the one scenario that runs before the engine exists in any form: the defect reproduces with
today's own tools, so it is the fixture the engine must later match.

```bash
python3 scripts/python/harness-triple-check.py --action verify; echo "exit=$?"
```

Use the **source** copy. The `.specify/scripts/python/` copy resolves its root to `.specify/`
(C-028) and ends `input-error: .../no-harness-asset.yaml: carrier 'skills/external/database-utils/
scripts/query.py' does not resolve`, exit `2` — a mirror-side root artefact recorded in
`test-evidence/plan-gates.txt`, not a reading of the corpus entry.

Today (measured 2026-11-09, `62f95298`):

```text
declarations: 23   candidates: 86
consistency-declarations-to-carriers: 31/31   consistency-carriers-to-declarations: 16/16
findings: 3
finding: unclassified-candidate: skills/external/ssh-utils/SKILL.md
finding: unclassified-candidate: templates/commands/measure.md
finding: unclassified-candidate: templates/commands/status.md
exit=1
```

while `.specify/specs/084-harness-triple-structure/verification.md:70` records `unclassified 0`. That single
comparison is the corpus's A2 entry.

| Reading | Expected |
|---------|----------|
| the verify run | `findings: 3`, `unclassified-candidate` ×3, exit `1` |
| the verification record | still says `unclassified 0` |
| an independent `--json` run of the engine's `false-closed-set` class | one entry per claim, `evidence_refs` naming both the verify reading and the record line |
| `status-unreadable` on the same pair | the feature is **not** reported (its registry status agrees with its closure verdict) — the defect here is the identity, not the status |

**Pass**: both classes reach this pair and neither loses it. **Fail**: the record is "fixed" by editing its number
without a reading — that is `correct` without evidence and `contracts/four-stage-command.contract.md` C-407 rejects it.

---

## § 2 — `stale-constant` and the class that has no corpus row (corpus F2; the `deferral-marker` gap)

```bash
sed -n '95,101p' scripts/bash/generate-instructions.sh
wc -c .specify/instructions.md
```

Today: the reason block derives `37888` (and `36864` fails by 73 B), the declaration below it is
`INSTRUCTIONS_BUDGET_BYTES=38400`, and the live file is `35821` B — two self-inconsistent subtractions in one block.

| Reading | Expected |
|---------|----------|
| `stale-constant` | **green** here: `38400` is a *chosen ceiling*, not a copied measurement, so this pair is not a duplicate-owner defect. The engine MUST say so rather than fire on a number that merely differs |
| `stale-constant` on a **copy** where `decomposition-check.py`'s `FR_CEILING` is restated independently in a spec body | red, naming both sites, both values and the owner |
| `deferral-marker` | **no corpus row exists** (`plan.md` § A–H two-way check). Prove it on a fixture: a body saying "保留到下一轮再处理" with no expiry → red; adding `expiry_kind: on-review` + `expiry_recheck` → green |
| a class with nothing to report | `count: 0` **with the roots searched** (§ `contracts/detection-categories.contract.md` C-108) |

**Pass**: a class that finds nothing says so over a stated surface; and the one class without corpus coverage is proven
by a fixture that is visible in the guard's own data.

---

## § 3 — `superseded-live` (corpus B1/B2/B3, 档 I)

Mutation on a copy tree: take a contract whose old text is still asserted byte-identically by its guard (B1's shape:
`086/contracts/runner-contract-086.contract.md` § C-016 against `test_run_tests_runner_contract.py`'s `…_byte_identical`),
and do **not** add the supersede marker.

| Reading | Expected |
|---------|----------|
| run | exit `1`; one entry; `evidence_refs` names the **body** path:line and the **guard** path:line |
| then add the marker + pointer to the new carrier, and replace the old-behaviour assertion | exit `0` for this class |
| then add a second spelling of the evidence path without a pointer | red again, naming the second spelling |

**Pass**: the three landing faces (body / guard / evidence path) are separable — each mutation lands on its own entry.
**Fail**: one entry covering "the contract is stale" without naming the guard.

---

## § 4 — `multi-owner` (corpus D1–D6, 档 II — detection only)

Mutation: inject a second independent definition of one constant into a copy spec body, leaving the owner untouched.

| Reading | Expected |
|---------|----------|
| run | exit `1`; one entry; both sites named, **both values** printed |
| replace the second definition with a pointer to the owner | exit `0` |
| make the pointer target non-existent | red as `orphan-path`, naming the target |

**Pass**: detection is delivered for 档 II classes even though the repair belongs to another line
([`feature-ref.md`](feature-ref.md) § Shift List). **Fail**: the repair lane edits the 档 II body — RK-5.

---

## § 5 — `renumber-live-binding` and the history-record leg (corpus C1–C4, 档 I)

Four mutations, one per live-binding shape: task header, contract header, team slug, feature-reference line. Then two
mutations on the judgement face itself.

| Mutation | Expected |
|----------|----------|
| task header carries the previous feature's id | red, naming file:line |
| contract header `**Feature**: <previous id>` | red, naming file:line |
| team directory slug / `name:` | red, naming the directory |
| feature-ref binding line | red, naming the line |
| **history record**: `test-evidence/` body keeps the old number | **green** — a dated record is legitimate (FR-020) |
| **history record rewritten** to the new number | **red** — FR-023's third limb; no corpus row covers it, so the guard carries it |

**Pass**: all six lines are separably readable. **Fail**: the check cannot distinguish "kept" from "rewritten" — then
FR-024's predicate face is being guessed, not enumerated.

---

## § 6 — `orphan-path` (corpus B4/B5/H1/H2)

| Reading | Expected |
|---------|----------|
| a body naming a path that does not exist | red, naming the referring path:line **and** the missing target |
| the same body after OI-3's reading (the file exists, the spelling is the wrong one) | classified as `superseded-live` / `correct`, the original spelling retained in the disposition record — **not** silently rewritten |
| three spellings of one evidence path | one entry per non-owner spelling, each pointing at the owner spelling |
| `.specify/.tmp/086-*` historical measurement paths | **no entry** — corpus H3 is a recorded exclusion, the third legitimate duplicate form |

**Pass**: a legitimate history path never becomes a finding; a dead path never becomes a silent deletion.

---

## § 7 — `status-unreadable` (corpus A1, A3–A6) and the consumption proof

```bash
python3 scripts/python/closure-acceptance-check.py --json --feature <id> | head -20
```

| Reading | Expected |
|---------|----------|
| a registry row claiming `Implemented` while the closure verdict is `block` | red, emitting the existing reason code `status-claims-implemented-but-blocked` **verbatim**, naming the feature |
| a `verification.md` missing the machine-readable block or a smoke field | red, naming the **missing field**, not "unreadable" |
| a claimed identity such as `applicable + exempt == candidates` that does not hold | red with **both** readings on the same line |
| the same features re-read with the checker replaced by a stub returning a chosen verdict | the report reflects **the stub's** verdict |

The last row is RK-2's discriminating reading: if the report still shows the tree's real verdict while the checker is a
stub, the engine re-derived closure and the scenario fails.

---

## § 8 — The four-stage seam: review → design → user confirm → execute

Scenario, run against a copy tree with at least one open entry:

1. **Review** — run the review face of `/speckit.history`.
   ```bash
   git status --porcelain=v1 > /tmp/snap-before.txt
   ```
   Expected: a report (coverage declaration first, then entries), no working-tree change.
2. **Design** — ask for the design segment. Expected: per entry, a proposed disposition, the touched paths, and
   reversibility; the segment ends with one confirmation request. If a plan file is needed it is under
   `.specify/.tmp/` and nothing tracked changed.
   ```bash
   git status --porcelain=v1 > /tmp/snap-after-design.txt
   diff /tmp/snap-before.txt /tmp/snap-after-design.txt   # MUST be empty
   ```
3. **Confirm** — answer `group` (or `item`, or `none-of` naming some entries). Expected:
   - `group`: one confirmation covers that class; execute runs for that class only;
   - `item`: entry-by-entry;
   - `none-of`: everything proposed, only the named entries confirmed;
   - **no answer** defaults to `group`;
   - after a partial confirmation, the unconfirmed entries are visible as `unconfirmed` and the "not closed" count
     includes them.
4. **Execute** — expected: writes only the confirmed paths, at **group boundaries**, one evidence file per group in
   `.specify/specs/092-non-disposable/test-evidence/` with all four segments; `git status --porcelain` shows rename
   pairs for `archive`, never deletions; `.specify/.tmp/<plan>` is gone.

**Pass**: the two snapshots are byte-identical and the execute segment only ran after a confirmation.
**Fail**: any tracked write before the confirmation, or an evidence file missing one of the four segments.

---

## § 9 — The concurrency slice: sharded semantic face on the 085 team

Precondition (FR-051): the team exists only after `clarify` **and** `plan` both passed U4 — its slug is
`092-non-disposable`.

```bash
python3 scripts/python/non-disposable-check.py --roots
python3 scripts/python/non-disposable-check.py --scope shard-01 --json > /tmp/s01.json
python3 scripts/python/non-disposable-check.py --json > /tmp/all.json
```

| Reading | Expected |
|---------|----------|
| `--roots` | the ten roots in declaration order with presence and per-root count; candidate total equals an independent `find` over the same roots (today 4,357 files — a reference point, not a threshold) |
| shard partition | disjoint; union equals the candidate set; no empty shard |
| two runs at different concurrency (24 and 4) | entry sets identical **by `entry_id`** |
| one shard's subagent returns a malformed payload | that shard is `unevaluated` and visible; the "not closed" total includes it; the run does not report `closed: true` |
| effective concurrency | `min(requested 24, host, stage max_parallel, ready packages + verifier reserve, resources)`; a downgrade names its reason |

**Pass**: the result is concurrency-independent and an un-evaluated shard is never read as clean. **Fail**: the union of
shards differs from a single-run candidate set, or a shard silently disappears from the report.

---

## § 10 — After the repair lane: the zero the feature is for

```bash
python3 scripts/python/non-disposable-check.py --json > /tmp/before.json   # before the run
# ... confirmed dispositions execute ...
python3 scripts/python/non-disposable-check.py --json > /tmp/after.json    # after
```

| Reading | Expected |
|---------|----------|
| 档 I entries after the run | zero **by name** (or only registered exemptions with a stated expiry) |
| 档 II entries after the run | still present or shifted — they are **not** counted in this feature's zero |
| the two readings | both stored in the run's evidence file, with the changed-path list, the corpus ids and the disposition class |
| `closed` | `true` only when `open` / `unconfirmed` / `unevaluated` are all zero |

**Pass**: "zero" is a named set difference between two readings, not a human's assurance. **Fail**: "已被人工看过"
appears anywhere as the reason for closure (FR-055).
