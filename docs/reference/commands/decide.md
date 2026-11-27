# `/speckit.decide` — Batch Decision Panel

Aggregate every pending decision item into one presentation, attach each item's recommended default, capture an objection-only reply verbatim, and record the batch through the existing decision carriers so the whole batch can be replayed from its record alone.

- **Source of truth (rules)**: `shared/definitions/decision-definitions.md` § 批量决策面 — the closed pending-source roster, the pending-item block grammar, the batch presentation contract, the recommended default and grounding join, the reply/disposition contract, the batch record contract, the register reflection, the replay contract, the completeness/refusal rules and redecision supersession. This page restates none of those criteria tables; it reaches them by pointer.
- **Command template**: `templates/commands/decide.md`
- **Interaction carrier**: `skills/internal/decide-batch/SKILL.md`
- **Engine**: `scripts/python/decision-batch.py` (standard library only, network-free)
- **Feature**: 112 Batch Decision Panel（批量决策面板）

## What it does, in one paragraph

`/speckit.decide` runs one batch: `scan` reads the two closed pending sources (open decision rows in `.specify/register.md` and authored `### PENDING —` blocks under `.specify/specs`, `.specify/goals`, `.specify/anchoring`, `.specify/teams`), renders one deterministic presentation with the batch-level context floor and every item's slots, and prints it. The user replies explicitly — objecting only to the items they contest, parking some, or declaring no objections. The skill relays that text verbatim into a reply file; the engine validates membership and eligibility, mints one batch id, writes one dated batch record into the existing knowledge store (carrying the decision records and the three batch-family fields), appends register rows / status-cell updates and the block `resolution` annotations, and appends the single `superseded_by` line to each prior record the batch overturns. `replay` reconstructs the whole batch from the record and resolvable pointers alone.

## Usage

```text
python3 .specify/scripts/python/decision-batch.py scan   --workspace-root <root> [--format {text,json}]
python3 .specify/scripts/python/decision-batch.py record --workspace-root <root> --presentation <scan payload> --reply <reply file> --authorization interactive [--format {text,json}]
python3 .specify/scripts/python/decision-batch.py replay --workspace-root <root> --batch <batch record> [--format {text,json}]
```

| Flag | Actions | Meaning |
|------|---------|---------|
| `--workspace-root PATH` | all | the workspace the panel reads (default: the current directory) |
| `--format {text,json}` | all | output format (default: text) — the text body is the user-facing channel, the JSON payload the machine channel |
| `--presentation PATH` | record | the scan payload the reply is bound to |
| `--reply PATH` | record | the reply file carrying the user's verbatim text and structured objections |
| `--authorization {interactive,unattended}` | record | caller-declared interaction authorization; missing is treated as unattended and refused |
| `--batch PATH` | replay | the batch record to replay |
| `-h` / `--help` | all | the same body on the entry and on every action |
| `--version` | all | one line `decision-batch.py <framework-version>` |

## Exit semantics (as declared by the engine's `--help` face)

```text
exit-codes: 0 success (including nothing-pending); 1 a documented refusal; 2 usage or environment error
```

`0` covers a rendered presentation, an explicit `nothing-pending` empty result (no batch record is created) and a recorded batch. `1` covers every named refusal — carrier-level unreadability, drift between presentation and record, unknown or duplicate reply identities, non-member option labels, unattended or undeclared authorization, duplicate batch ids, unwritable prior carriers for a redecision and unresolvable replay pointers; a refusal writes nothing. `2` covers an undeclared option and a usage/environment problem.

## Boundaries

- **Only two sources, one presentation per call**: nothing is fetched, scheduled or retried; there is no daemon, no reminder, no UI and no second store.
- **`ai-autonomous` never enters the panel**: it is excluded `not-human-held` and counted; the panel settles only `human-interactive` items.
- **Silence means acceptance only inside a completed interactive batch**: an unattended call may scan but is refused at `record`; a missing authorization level is treated as unattended.
- **One batch, one record**: the batch record is a dated entry in the existing knowledge store written through the memory engine; a same-id second write is refused before the write surface; the sole sanctioned post-write mutation is the single `superseded_by` line appended to an overturned prior record.
- **Honest completeness**: every source is read or named absent with its reason; every candidate is classified exactly once; a carrier present but unreadable refuses the whole batch; zero candidates is an explicit `nothing-pending`.
- **Zero network, zero feedback-store write, zero automatic transmission.**

## Related surfaces

| What | Where |
|------|-------|
| Batch rules (roster, block grammar, presentation, grounding, disposition, record, replay, completeness, redecision) | `shared/definitions/decision-definitions.md` § 批量决策面 |
| 107 decision-record grammar, field closure and the M/B enforcement boundary | same owner page |
| Interaction skill | `skills/internal/decide-batch/SKILL.md` |
| Design record (data model, contracts, quickstart) | `.specify/specs/112-decision-batch-panel/` |