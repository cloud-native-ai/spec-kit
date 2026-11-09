# quickstart.md run notes

Owner of this file: the **implement** stage's walk records, one `##` section per task that records measured readings.
Created by T082 (seat C). Earlier tasks that also record here — T062 (first coverage declaration) and T071
(§ 2 readings) — have no section yet; they are not back-filled by this file, because a reading taken today is not the
reading those tasks were meant to take. Their absence is reported, not papered over.

---

## § T082 — quickstart.md § 8 seam walk on a copy tree (2026-11-09, implement seat C)

**Scope**: `quickstart.md` § 8 — the four-stage seam review → design → user confirm → execute.
**Subject**: the seam as it exists in the tree at `999d3c6a`, i.e. the contract text
(`contracts/four-stage-command.contract.md` C-401…C-410), the owner face
(`skills/internal/manage-history/SKILL.md` Steps 0 / A / B / execute) and the command face
(`templates/commands/history.md`).
**Tree**: `/tmp/seatC-copy`, an `rsync -a --exclude .git` copy of the repo (221 MB). `git init` + one baseline commit
was added **to the copy only**, because both snapshots are `git status --porcelain=v1` readings and a tree without
git has no reading to take. The copy's `.git` is an artifact of the walk, not part of the subject.

**Verdict up front**: the seam **is not executable end to end**. § 8's stages 1–3 (review, design, confirm) are
runnable and were run; stage 4 (execute) **cannot start** in a copy tree, and the four evidence segments have **no
producer anywhere in the tree**. The evidence store written by the execute segment is never read by any guard.

### 1 — Stage 1 (review): zero write — PASS

Command (verbatim from `skills/internal/manage-history/SKILL.md` § Step 0 item 1):

```bash
mkdir -p .specify/.tmp
{ git status --porcelain=v1
  python3 scripts/python/non-disposable-check.py --roots | cut -d' ' -f1 \
    | while read -r root; do [ -d "$root" ] && find "$root" -type f -print; done \
    | LC_ALL=C sort | while IFS= read -r file; do sha256sum "$file"; done
} > .specify/.tmp/history-seam-snapshot-before.txt
```

- Exit `0`; 4,417 lines: 0 `git status` lines + 4,417 content hashes over the declared root set.
- The review face itself: `python3 scripts/python/non-disposable-check.py --json` → exit `1` (findings).
  `coverage.candidates = 2033`, `declaration_status = ok`, `entries = 780`, `closed = false`,
  `not_closed = {open: 780, disposed: 0, unconfirmed: 0, unevaluated: 0, shards: 0}`;
  class counts `orphan-path 586 / renumber-live-binding 120 / status-unreadable 52 / deferral-marker 14 /
  false-closed-set 8 / stale-constant 0 / superseded-live 0 / multi-owner 0`.
- The review report went to `.specify/.tmp/history-review.json` (the skill's own path); nothing tracked moved.

**Ignore premises** (§ 8 step 2, checked on the real tree before trusting the green):

| probe | result |
|---|---|
| `git check-ignore -v --no-index .specify/.tmp/probe` | `.specify/.gitignore:30:.tmp/` , rc `0` |
| `git check-ignore -v --no-index .specify/history/.work/probe` | `.specify/.gitignore:6:history/.work/` , rc `0` |
| `git check-ignore -v --no-index history/.work/probe` | no output, rc `1` (bare root path is **not** ignored) |
| `mkdir .specify/archive/.tmp-probe; touch …/marker; git check-ignore …` | no output, rc `1` — **not** ignored, and `archive/` is a declared root, so scratch there is tracked |

### 2 — Stage 2 (design): zero write — PASS, with a rule reading correction

- Design segment: prototyped as one `{entry, disposition, touched paths, reversibility, group}` row per entry, per
  detection class (the engine's `category`), ending in one confirmation request. No design row was confirmed, so no
  prototype row is reproduced here as a plan.
- Snapshot #2, same command, after the design work:

| reading | value |
|---|---|
| `diff before after-design` | no output, rc `0` (0 bytes) |
| sha256(before) | `36f7f67355076f6c90ec3a08cd5319e99dd3105bd9aa5d244aa18b121121f98b` |
| sha256(after-design) | `36f7f67355076f6c90ec3a08cd5319e99dd3105bd9aa5d244aa18b121121f98b` |

**Negative control** (so the green above is a reading, not a coincidence). Appending one line to a *tracked* evidence
file inside `.specify/` and re-snapshotting:

```text
0a1
>  M .specify/specs/092-non-disposable/test-evidence/u15-report.txt
4315c4316
< da264d4d…  .specify/specs/092-non-disposable/test-evidence/u15-report.txt
> 088b0868…  .specify/specs/092-non-disposable/test-evidence/u15-report.txt
```

The snapshot goes red for a tracked write (status line **and** content hash), and goes byte-identical again after the
probe is reverted (`git status` → 0 lines; snapshot digest back to `36f7f673…`). The probe was reverted in full; the
copy tree ends the walk with `git status --porcelain=v1` = 0 lines.

- **Correction to the rule as written**: the skill's Step 0 Step-A wording ("`.specify/.tmp/` is this stage's only
  scratch and it is git-ignored") is true; but `history/.work/` — the distillation scratch § Step 2 writes — is
  ignored **only** through the `.specify/` prefix (row 2/3 above). A bare `history/.work/` at the repo root is tracked.
  The § 8 prose already states this; the skill's Step 0 parenthetical is the weaker statement of the same fact.

### 3 — Stage 3 (confirm): one reading per granularity — READ (not executed)

No confirmation was issued by this walk (a confirmation is the user's answer; a seat cannot supply it). The four
documented readings were checked **as documented text**, not as behaviour, because no execution consumes them here:

| granularity | documented reading | where |
|---|---|---|
| `group` (default, and the value an absent answer resolves to) | one confirmation covers every entry of that detection class | skill § Step B table + "Absent input resolves to `group`" |
| `item` | entry-by-entry | skill § Step B table |
| `none-of` | nothing implicitly; only the named entries confirmed | skill § Step B table |
| after a partial confirmation | unconfirmed entries appear as `unconfirmed`; "not closed" includes them | skill § Step B bullet 3; engine `not_closed.unconfirmed` |

Consistency check on the machine side: the engine's `not_closed` already carries the `unconfirmed` bucket
(reading `unconfirmed: 0` with 780 open entries above), so the state Step B promises has a slot to land in.

**What was not done, and why it is not faked**: no entry was selected, no group was confirmed, and therefore the
`group` / `item` / `none-of` distinction has **no behavioural reading** in this walk. Reporting one would be a
self-report, not evidence. T083+ and the P5 guard (C-405) are where that distinction gets a red-able leg.

### 4 — Stage 4 (execute): BLOCKED — the seam cannot reach its own execute segment

Two independent stoppers, both measured on the copy tree:

1. **The execute segment needs a tool session store, and a copy tree has none.** `history-utils.py --action locate`
   resolves the per-project store by path hash, so the copy tree is a *different project* to the engine: every tool
   returns `session_count = 0`, store `~/.claude/projects/-tmp-seatC-copy` / `~/.qoder/projects/-tmp-seatC-copy`
   (absent), `supported = false`. Steps 1–2 of the pipeline therefore stop at Step 1's gate ("No history found"),
   and the execute segment — which *is* Steps 1–6 — has nothing to run. This is not a defect of § 8; it is the
   honest shape of "run the seam on a copy tree" when the pipeline reads a host-side store.
2. **The repair writes the seam's execute segment carries have no producer.** The seam describes them as
   "the repair writes Step B confirmed", but there is no code path that takes a confirmed design row and performs
   `archive` / `supersede` / `correct` / `exempt`. The engine `.specify/scripts/python/non-disposable-check.py` is
   read-only (`--help` → "side-effects: none (read-only)"), its declared option surface is the closed eight rows with
   no write action, and `history-utils.py`'s four actions (`locate` / `extract` / `manifest-read` /
   `manifest-update`) touch only the manifest. No third engine exists. So the execute segment is **prose**.

Because of (2) the walk stops before any confirmation; issuing one would promise an execution nobody can perform.

### 5 — The four evidence segments: actual landing and content summary

| question | measured answer |
|---|---|
| Where must the file land? | `.specify/specs/<spec-dir>/test-evidence/`, one file per group — here `.specify/specs/092-non-disposable/test-evidence/` (FR-035 / C-408) |
| What are the four segments? | `readings` (before/after `--json` digest of the same scope), `paths` (changed-path list incl. rename pairs), `corpus` (corpus ids, empty allowed), `dispositions` (one E-4 row per entry) — `data-model.md` § E-7 |
| Who writes one? | **nobody, today**: no producer exists (see § 4.2), so zero evidence files in the store were written by the seam |
| Who reads one? | **nobody**: no guard parses the E-7 shape. `non-disposable-check.py` never mentions `test-evidence`; the only occurrence in the P5 contract suite (`tests/contract/test_non_disposable_contract.py`) is a literal `"evidence": "test-evidence/x.md"` in the supersede-registry fixture, which is checked as a non-empty string, not as a four-segment file |
| Does a store in the target directory exist and is it used? | yes — 32 files, `p1…`/`p2…`/`u0x…`/`seat*`; only `p2-20261109T125609.txt` carries a header block (segments `readings` / `paths` / `corpus` / `dispositions`); the rest, including every seat report, carry none |

**Shape probe** (what a repair evidence file costs to fabricate — run in the copy, reverted): a four-line markdown file
with the four `- readings: / - paths: / - corpus: / - dispositions:` bullets is accepted by every check that exists,
and deleting the `readings` line changes nothing observable. The C-408 mutation leg ("remove one of the four segments
and assert red") is therefore **not green-able at HEAD**: there is nothing whose colour could change.

**Substitute reading actually taken** (not the execute segment's, and labelled as the substitute): the closest thing
to a before/after pair — two consecutive `--json --scope s000-of-008` readings, hashed:

| reading | value |
|---|---|
| before | exit `1`, `entries = 73`, `closed = false`, `not_closed.open = 73`, `surface_digest = f60bcc1b…`, sha256 = `ad72a1ee…` |
| after (same scope, no write between) | byte-identical, sha256 = `ad72a1ee…` |
| class split inside the scope | `orphan-path 49 / renumber-live-binding 16 / status-unreadable 7 / deferral-marker 1 / others 0` |

That pair proves the reading is **reproducible and scope-addressable** — the property a `readings` segment needs — and
proves nothing about a repair, because no repair happened.

### 6 — What § 8's pass/fail line does and does not measure

§ 8's pass line ("the two snapshots are byte-identical and the execute segment only ran after a confirmation") is
**one half decidable and one half not**: the first clause was measured green (§ 2 above); the second clause has no
execution to be ordered before, so it holds vacuously. A reader who takes "PASS" from § 8's line would be reading the
vacuity as the evidence. The two anomalies in the report are exactly this gap.

### 7 — Machine observations raised alongside (not seam-local)

- **Freshness, not wrongness**: the P2 baseline in `test-evidence/p2-20261109T125609.txt` (`candidates 2032`,
  `orphan-path 631`, `superseded-live 177`, `multi-owner 13`, `eleven` root set printed as nine + two) versus today's
  reading (`candidates 2033`, `orphan-path 586`, `superseded-live 0`, `multi-owner 0`, `false-closed-set 8`) reflects
  the 15-way repair wave (`76b4ec60`) and later commits, not a contradiction. It is stated here because § 8's
  readings are compared against that file.
- **`deferral-marker` is the only one of the ten classes whose count is stable across the two readings** (14 → 14);
  the class with no reproduction arm (corpus F2) is therefore the one the repair wave did not move.
- **`--scope` does not populate `shards`**: single-shard `--json` output carries `shards: []`, so an E-6 reader cannot
  see a shard's `evaluated` / `unevaluated` verdict from a scoped run. Not exercised by § 8; noted for the P5 legs.
- **The T082 inputs do not exist in this file's prior state**: `T080` (regenerate per-tool command copies) and
  `T062` / `T071` (the sections this file was expected to already carry) are still `[ ]` in `tasks.md`. The seam walk
  itself does not depend on T080's output, but the four command-face copies `templates/commands/history.md` generates
  were not checked as part of this walk.
