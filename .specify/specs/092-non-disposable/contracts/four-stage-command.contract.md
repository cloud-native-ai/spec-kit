# Contract: Four-Stage Command Seam

**Feature**: 092-non-disposable | **Contract file**: `contracts/four-stage-command.contract.md`
**Guard carrier**: `tests/contract/test_non_disposable_contract.py` (C-403 / C-406 / C-407 carry mutation legs)
**Owner**: the four-stage execution form is stated once in `skills/internal/manage-history/SKILL.md` (the seam steps)
and once, as a delegation bullet list, in `templates/commands/history.md`; the definition of "confirmed" and the
confirmation-granularity domain live in the owner page § Confirmation. This file fixes what the guard may assert about
the seam, and MUST NOT be read as a second statement of the stages.
**FR coverage**: each clause carries its own trailing citation group.

**Reuse boundary.** `/speckit.history` stays the single history entry (FR-043 / FR-059). The seam is added **inside**
the existing command and skill, never as a second command, a second skill or a second distill storage.

## C-401 — Exactly four stages, named identically in both faces

The seam is, in order: **review → design (方案) → user confirm → execute**. Both the skill and the command template
MUST name all four, in that order, and MUST use the same words. The guard asserts the four names appear in order in
both files; a mutation leg deletes one stage name from one file and asserts red.

(FR-029, SC-019)

## C-402 — The four segments are wired to a named position in the existing step list

`skills/internal/manage-history/SKILL.md` already carries **Steps 1–6** (tool identification, clean extraction,
distillation, aggregation, rendering, write). The four-stage form MUST NOT compete with that list: it is attached at
three named positions, and the execute segment takes **Step 6's** position because that is where the skill already
writes.

| Four-stage segment | Position in the existing step list | Why there |
|---|---|---|
| 回顾 (review) | a new **Step 0**, before Step 1 | the review surface must be read before anything is extracted, and Step 1 does not write |
| 设计 (design / 方案) | a new **Step A**, after Step 6 and before the execute step | the design is produced from the review's findings, not from the extraction pipeline; it writes nothing (C-402) and may hold one temporary artifact (C-403) |
| 用户确认 (user confirm) | a new **Step B**, between A and execute | the confirmation is its own gate, and must be visible as a step rather than implied by the execute segment |
| 执行 (execute) | **Step 6**, unchanged in name and position | the execute segment *is* the existing write step; renumbering it would break every reference in `templates/commands/history.md` |

The steps are named `0` / `A` / `B` rather than renumbering to `0`–`7` for one reason: a document that says
"Steps 1–6" in its own prose, its command template and its tests would otherwise carry a stale list in every place
this feature does not edit. `0`, `A` and `B` are insertions that leave the existing numbering intact, and the skill's
own sentence "Steps 1–6" stays true. A rewrite of that sentence to "Steps 0, A, B, 1–6" is **not** required and MUST
NOT be performed — the four-stage form is stated as three insertions plus the existing Step 6, and that statement is
what `history.md`'s delegation list carries.

(FR-029, FR-031)

## C-403 — Review and design write nothing

The review segment and the design segment MUST create no change in the working tree: before the review and after the
design the engine takes a snapshot (`git status --porcelain=v1` full text + content hashes over the managed path set)
and the two snapshots MUST be byte-identical. The requirement is on the **reading**, not on the command's own claim.

(FR-031, SC-004)

## C-404 — The only permitted unreviewed-on-disk artifact is a temporary plan

If carrying the design to the confirmation step needs a file, that file MUST live under `.specify/.tmp/` (already
matched by `.gitignore`) and MUST be removed by the execute segment. The guard asserts no run leaves a tracked-path
write before confirmation: a mutation leg writes the plan to a tracked path and asserts red.

(FR-031, FR-042, SC-004)

## C-405 — Three confirmation granularities, `group` by default

The confirmation granularity domain is closed: `group` (one confirmation covers every entry in that class) /
`item` (entry by entry) / `none-of` (everything is proposed, only the named ones are confirmed). Absent input MUST
resolve to `group`. There is no fourth value, and "one confirmation = execute everything" MUST NOT exist — full
execution is only ever the sum of per-group or per-item confirmations.

(FR-032, SC-019)

## C-406 — Unconfirmed is a visible state, not a drop and not a retry

After a partial confirmation, every unconfirmed entry MUST appear in the report as `unconfirmed`
(§ `data-model.md` Entry State Machine) — not as "no design yet", not as any disposition value. It MUST NOT be
silently dropped, MUST NOT be retried automatically next round, MUST NOT count toward this round's closure.

(FR-033, FR-042, SC-019)

## C-407 — The execute segment runs only after confirmation, group by group

Execute MUST start only on the confirmed set. It MUST write at **group boundaries** and record one evidence file per
group at each boundary, so an interruption stops between groups, never mid-entry. The guard asserts the ordering by
running a confirmation that covers one group and verifying no path outside that group was touched (mutation leg:
touch a path from an unconfirmed group and assert red).

(FR-034, FR-042, FR-045, SC-019)

## C-408 — Evidence: one channel, one file per run, four segments

Repair evidence lands in `.specify/specs/<spec-dir>/test-evidence/` — for this feature
`.specify/specs/092-non-disposable/test-evidence/` — **one file per run**, and MUST carry four segments:
(i) the detection readings before and after, (ii) the changed-path list, (iii) the corpus entry ids, (iv) the
disposition class (§ `data-model.md` E-7). Evidence MUST NOT be written into `.specify/memory/sanitize/findings.json`
or into `.specify/history/`, and no second evidence store may be created. A mutation leg removes one of the four
segments and asserts red.

(FR-035, FR-054, SC-010)

## C-409 — The existing capability is preserved, not replaced

Distilling a tool session's history into the topical knowledge base, and the incremental manifest, remain part of the
command (review / execute faces). The seam MUST NOT remove them and MUST NOT open a second entry to the same storage;
`.specify/history/` remains the sole distill storage and this feature only **reads** it.

(FR-043, FR-044, FR-059, SC-012)

## C-410 — The seam is not a bypass for rewriting delivered bodies

Any change to an existing spec body, owner document or guard MUST be a confirmed design item and MUST carry
before/after readings. An execute run that touches a path not named in a confirmed design row is a violation, which is the same reading as the execute-segment rule in clause C-407, not a second one.

(FR-045, FR-052, FR-056)
