# /speckit.derive

Reach an architecture by **replaying the reasoning methods of authoritative sources** instead of summarizing their conclusions. Every source is grounded online first, each source's *way of arguing* is extracted as a reusable Reasoning Move, the moves are applied step by step in an auditable derivation chain, and every architecture element traces back to a chain step. Where grounded premises run out, the gap is recorded as an open question — never filled with a plausible-sounding invention.

- **Source of truth**: `templates/commands/derive.md`
- **Engine**: `scripts/python/derive-utils.py` (installed as `.specify/scripts/python/derive-utils.py`) · Tool record `.specify/memory/tools/derive-utils.py.md`
- **Concept authority**: `.specify/shared/definitions/derivation-definitions.md` — the six record schemas, the provenance grades, the chain-integrity rules C1–C7, the self-audit set A1–A16, the banned-justification set and the capability-degradation rule are defined there. This page references them and restates none of them.
- **Feature**: 049 Derivation Command · **Requirement**: `048-derive-command`

## When to Use

- When you hold a **topic-level** question ("how should a distributed HTTP API be structured?") whose answer should outlive and serve many features.
- When you have been handed a reading list — by a colleague, a community compilation, or another model — and you want an architecture whose provenance you can actually check. Handed-in lists routinely contain a dead link and an article a community aggregator retitled; this command is the one that surfaces both instead of inheriting them.
- When a previous decision keeps being re-argued from scratch and you want the *reasoning* captured once, as moves a later run can reuse.
- When you need to know whether an architecture is derived or merely asserted: an element with no resolving chain of steps is rejected, not annotated.

Not for feature-scoped evidence gathering or technology selection — see [Boundary](#boundary-derive-vs-research).

## Syntax

```text
/speckit.derive <topic> [source list] [--max-steps <N>] [--force]
```

| Argument | Meaning |
|----------|---------|
| `<topic>` | the domain question to derive an architecture for; becomes `<topic-slug>` and the archive directory name |
| `[source list]` | titles, authors and URLs handed in by you, a colleague, or another model — **input to be verified, not facts to inherit** |
| `--max-steps <N>` | derivation step budget (engine default applies when omitted); hitting it is reported, never silently truncated |
| `--force` | re-scaffold an existing archive — the current content is kept as `derive.md.bak` in the same directory and reported as `clobbered`; the default is to amend in place |

The engine behind the run (six actions, all deterministic):

```bash
python3 .specify/scripts/python/derive-utils.py --action init        --slug <topic-slug>  --workspace-root . --format json
python3 .specify/scripts/python/derive-utils.py --action probe-links --file <urls.json>   --workspace-root . --format json
python3 .specify/scripts/python/derive-utils.py --action moves-list                        --workspace-root . --format json
python3 .specify/scripts/python/derive-utils.py --action moves-add   --file <moves.json>   --workspace-root . --format json
python3 .specify/scripts/python/derive-utils.py --action validate    --slug <topic-slug>  --workspace-root . --format json
python3 .specify/scripts/python/derive-utils.py --action stats       --slug <topic-slug>  --workspace-root . --format json
```

## Execution Flow

Nine stages. Writes are reversible (a new archive file plus appends to the move library), so the run executes throughout without blocking gates and closes with a three-element execution report.

1. **Preflight** — probes `python3`, the engine, and the host's **online capability** (whether a WebSearch/WebFetch-class tool is exposed). A missing engine stops the run with an actionable hint; a missing online capability switches on the degradation path in stage 3 rather than silently skipping verification.

2. **Resolve topic & load the move library** — `init` scaffolds `.specify/derive/<topic-slug>/derive.md` with the fixed section set and creates `.specify/derive/moves.md` if the project has none. An existing archive is **never clobbered** without `--force`; the normal path is to amend it in place. `moves-list` then returns a *projection* of the library — the run consumes the projection, not the whole file — so already-recorded moves are reused or re-anchored before any new shape is issued.

3. **Ground the sources online** — for every source, in the fixed order the anchor's Dead-Link Protocol owns: direct fetch → archive availability lookup → one attribution search on title + author. `probe-links` supplies the unfabricable evidence trace (HTTP status, snapshot address, or the failure that stopped the probe); the agent then reads the actual text and assigns the **provenance grade**, because grading is a judgment about origin, not a pattern match. Two properties of this stage decide whether the rest of the run is worth anything:
   - `title_mismatch` is **computed by the engine** from normalized string comparison, never asserted by the agent; when it is true both titles stay on the row.
   - every source that could not be grounded is **recorded with its reason** under `## Unverifiable Sources`. A probe that could not run is not a dead link, and a dropped source is how a dead link becomes an invisible hole in the chain.

   **Degradation clause**: if the host exposes no online capability at all, the run MUST NOT fabricate grounding — every source is graded `unverified` with the reason `no-online-capability`, no step may anchor, and the run stops before building the chain and reports the degradation. An honest empty result, never a confident unverified one.

4. **Extract reasoning moves** — the semantic core, and the reason this command is not a research tool. The agent reads what a source *does* to get from premise to conclusion and writes that shape down with named slots (the slots are what make it re-applicable in another domain), plus the failure mode it prevents, its applicability condition **and an over-application guard**, and the source that exhibited it. `moves-add` is the library's **only** writer: it dedups on two levels — the exact normalized inference form, and the *slot-isomorphic* form, since a slot name carries no semantics — and on a near-duplicate it refuses the new row and returns the existing `move_id`, so the run reinforces the recorded move instead of forking a variant. Each candidate declares an `intent` (`new` / `reuse` / `reinforce` / `supersede`) and anchors itself in the qualified form `<topic-slug>.S-<nnn>`: the library is project-wide while sources are per-topic, and `moves-add` carries no topic with which to qualify a bare `S-<nnn>`, so a bare reference is refused rather than guessed at.

5. **Build the derivation chain** — one `### D-<k>` block per step: explicit premises (grounded sources plus *earlier* steps), optional leads, exactly one move, the instantiated derivation, one falsifiable conclusion, the observation that would refute it, and a confidence. Chain-integrity rules C1–C7 are defined by the anchor and enforced by the engine; the three most often routed around are the banned-justification scan, the refusal to average two conflicting conclusions (they are recorded as contested, linked both ways, with a discriminating question named), and the rule that running out of premises ends the chain rather than licensing an invented one. `## Termination` declares which termination condition fired and the step count against the budget.

6. **Compose the derived architecture** — one `### A-<k>` block per element, each carrying a mandatory, fully resolving `derived-from` and a confidence inherited as the **minimum** over its steps. An element with nothing to trace to is a hard failure: the engine refuses the file rather than warning. Undetermined points go to `## Open Questions`, linked bidirectionally to the elements they block.

7. **Self-audit** — `validate` decides the mechanical half of the audit set and returns `errors[]`, `warnings[]` and `semanticChecksPending`; exit code 4 means a structural violation. `semanticChecksPending` is always `["A11", "A14", "A16"]` — *online grounding actually happened this run*, *the artifact states the sources' way of thinking rather than a summary of their content*, and *decision-claims are signed by the Agent Identity rather than laundered into truth-claims* — and those three must be **attested by the agent**, never inherited as green.

   Because `validate` is zero-write, the audit is a **two-pass loop**, not one call. A1–A10/A12/A13/A15 are *derived* from `errors[]`, and the artifact's own `## Self-Audit` rows must equal those derived values or the engine reports `audit-result-diverges`. A freshly scaffolded archive carries `pending` in all sixteen rows and therefore does **not** validate clean. So: run `validate` once, transcribe `payload.audit.engine` into the A1–A10/A12/A13/A15 rows, set A11, A14 and A16 to `attested` with a `method` sentence a reader could actually check (an empty, `engine` or `n/a` method draws the `attestation-method-degenerate` warning), then run `validate` again to converge. Transcribing the results into the artifact is the agent's step, never the engine's.

   Read the verdict from `ok` and the exit code, not from the table: a violation the audit set does not map — two moves on one step, a confidence outside the enum — rejects the file while every A row still reads `pass`. `stats` reports the counts and distributions. A run with any engine check red must report the failure and its location, and must not present `## Derived Architecture` as derived.

8. **Report** — three elements: what ran (topic, source count and grade distribution, moves reused vs newly issued, step count and termination condition, element and open-question counts, audit result including the A11/A14/A16 attestations); what changed (each artifact by path); how to undo it (both are git-tracked, and the library is accumulative — superseded rows are retained, never deleted). A run that failed or stopped midway reports where and why, plus whatever intermediate artifacts exist.

9. **Wrap-up** — the standard Feedback and Documentation steps shared by every complex command.

## Boundary: derive vs research

The distinction users get wrong most often, because both commands read sources and both produce a document with citations.

- **`/speckit.research`** answers *what is true, and what should we choose* for **one feature**. Its output is decisions plus rationale, it lives inside that feature's spec directory, and it dies with the feature.
- **`/speckit.derive`** answers *what follows, and by what reasoning* for a **topic**. Its output is a replayable inference chain plus an architecture whose elements cite chain steps, it lives at project level, and later features reuse it.

Litmus test: if what you want to keep is the *conclusion*, you want research. If what you want to keep is the *move that produced the conclusion* — applicable again in a domain nobody has named yet — you want derive. A derivation that ends up reading as an annotated bibliography has failed the test the command exists to enforce, and its own self-audit says so.

The dependency runs one way: a plan may cite an architecture element by identity instead of re-arguing it, and a derivation must never cite a plan. Full comparison matrix, including the third neighbor (`/speckit.plan`): `.specify/shared/definitions/derivation-definitions.md` §Derivation vs Research vs Plan.

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Derivation archive — sources, unverifiable sources, moves applied, chain, termination, derived architecture, open questions, self-audit | `.specify/derive/<topic-slug>/derive.md` |
| Reasoning Move library — project-level, accumulating, cross-topic, written only by the engine | `.specify/derive/moves.md` |

Both are git-tracked. The library is deliberately **not** a `sync-mirrors.py` mirror pair and is never shipped: `.specify/derive/` is project state, so `specify init` must not push an example library into every downstream project.

## Prerequisites

- `specify init` (project initialized), and `python3` on PATH — the engine is stdlib-only.
- A host CLI exposing an online search or fetch capability. Without one the command still runs, but only along the degradation path: no source can be grounded, so no step can anchor and no architecture is produced.
- Optional: a handed-in source list. A feature's existing `research.md` references are a legitimate starting corpus.

## Next Steps

- [`/speckit.plan`](plan.md) — encode the derived elements into an implementation plan, citing each `A-<k>` by identity instead of re-arguing it
- [`/speckit.clarify`](clarify.md) — work the `## Open Questions` that block an element, then re-run `/speckit.derive` to extend the chain
- Re-run the same topic later: the move library is cumulative, so a second run spends its budget on new shapes rather than re-extracting old ones
