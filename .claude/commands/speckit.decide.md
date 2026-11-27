<!-- AUTO-GENERATED from templates/commands/decide.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
> **Concurrency obligation（执行义务，按指针抵达）**: this command is an execution body — consider concurrency first, default to it when the class and capability allow, and, when serial, name a reason code and record the `requested` / `effective` / `effective_reason` reading. Authored text: `.specify/shared/definitions/subagent-definitions.md` § The Concurrency Obligation; class table: `.specify/shared/declarations/facts/concurrency-class.yaml`; reason codes: `.specify/shared/declarations/facts/serial-reason.yaml`; reading fields: `.specify/shared/declarations/facts/effective-concurrency.yaml`. This template restates none of their rules.

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions. An empty input runs the default action, `scan`; the other inputs select `record` or `replay` (below).

## Delegation

`/speckit.decide` is a **thin entry**. It names an action and relays; it judges nothing itself.

- **Rules** live in `.specify/shared/definitions/decision-definitions.md` § 批量决策面 — the closed pending-source roster, the pending-item block grammar, the presentation contract, the recommended default and grounding join, the reply and disposition contract, the batch record contract, completeness/refusal and replay. Reach that page by pointer; this template MUST NOT restate its criteria tables.
- **Interaction** lives in the internal skill `.specify/skills/internal/decide-batch/SKILL.md`: it relays the presentation, captures the user's reply verbatim and delegates the engine actions.
- **Fixed-rule judgements** (scan, grounding join, reply membership, bookkeeping, pointer resolution) belong to the deterministic engine `.specify/scripts/python/decision-batch.py`; the model never recomputes them.

**Script**: `.specify/scripts/python/decision-batch.py`, run from the repository root with plain `python3` (stdlib only). `scan` and `replay` write nothing; `record` is the only writer and writes only through the named carriers.

**The three actions** (closed set — neither a fourth nor a missing one is legal):

| Action | Invocation | What it answers |
|--------|------------|-----------------|
| `scan` | `python3 .specify/scripts/python/decision-batch.py scan --workspace-root <root> [--format text\|json]` | one complete presentation of every pending decision item, with the batch-level context floor and the completeness bookkeeping |
| `record` | `python3 .specify/scripts/python/decision-batch.py record --workspace-root <root> --presentation <scan payload> --reply <reply file> --authorization interactive` | validate the reply, write the batch record and the source updates, and disclose every post-write failure |
| `replay` | `python3 .specify/scripts/python/decision-batch.py replay --workspace-root <root> --batch <batch record>` | reconstruct the recorded batch from the record and resolvable pointers alone |

**Exit semantics**: owned by the engine's own `--help` face and pinned in `docs/reference/commands/decide.md`; this template names the codes by pointer instead of restating them. A refusal is a first-class result — never soften it into an empty presentation or a retry loop.

**Reply capture (record)**: the skill turns the user's explicit reply into the reply file the engine validates — the verbatim text plus entries bound by item identity. A follow-up question is not a reply; an aborted session writes nothing. Authorization is declared by the caller; a missing level is treated as unattended and the engine refuses to record.

**Output class (scan / replay)**: echo — in a superagent session, print the engine's stdout verbatim as this session's own message inside the stable envelope owned by `.specify/shared/guidelines/user-facing-output.md` at a presentation boundary; a tool result is not user-facing presentation. The `--format json` channel is for the skill/engine hand-off and is not a user-facing block.

**What this command never does**: never invents a default, an option or a missing slot value; never presents, converts or settles an `ai-autonomous` item; never records acceptance in an unattended run; never writes a second store, never accesses the network and never transmits anything automatically.