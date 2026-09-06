# Derivation Definitions Reference

Canonical definition of the **Derivation** concept in Spec Kit: the four record schemas (Source, Reasoning Move, Derivation Step, Architecture Element), the **provenance grade** set, the chain-integrity rules **C1–C7**, the self-audit set **A1–A14**, the closed **banned-justification** literal set, and the capability-degradation rule. This file is the single source of truth for the Derivation concept; other documents (`/speckit.derive`, the engine's module docstring, the glossary, `docs/reference/commands/derive.md`) link here rather than re-defining any of it. It sits alongside the other concept anchors: `goal-definitions.md`, `tool-definitions.md`, `agent-definitions.md`, `subagent-definitions.md`.

## What a Derivation Is

A **Derivation** is a project-level artifact that reaches an architecture by **replaying a reasoning method**, not by collecting conclusions. Its object is a *topic* — a domain question broad enough to outlive any single feature ("how should a distributed HTTP API be structured?") — and it is persisted under `.specify/derive/<topic-slug>/derive.md`.

The distinction that gives the concept its reason to exist:

| | Reading for **content** | Reading for **method** |
|---|---|---|
| What is extracted | what the source concludes | how the source gets from premise to conclusion |
| Artifact shape | summary, annotated list, comparison table | inference schema with named slots, re-applicable elsewhere |
| Failure it invites | the reader inherits the conclusion and cannot re-derive it in a new domain | — |
| Where it lands here | `/speckit.research` (feature-scoped evidence) | **Derivation** (this concept) |

A Derivation is composed of exactly four record kinds, in dependency order:

```
Source Record (S-nnn)  →  Reasoning Move (M-nnn)  →  Derivation Step (D-k)  →  Architecture Element (A-k)
     grounded online        extracted from S            applies M to premises       traced to D
```

Two operating properties follow:

- **Every element is traceable.** No architecture element may exist without a resolving chain of steps back to a verified source. An untraceable element is a preference wearing an architecture's clothes.
- **Gaps stay visible.** Where the chain runs out of verified premises, the residue is recorded as an open question — never filled with a plausible-sounding invention.

### Litmus tests

When deciding whether a sentence belongs in a Derivation:

1. **Replay test** — could an independent reader redo the inference from what is written, or must they trust the author? Must be redoable → Derivation step. Must be trusted → it is a citation, not a step (see C7).
2. **Slot test** — does the extracted pattern keep its force when the domain nouns are swapped out? Yes → a Reasoning Move. No → it is the source's conclusion, which belongs in a `premises` reference, not in a move.
3. **Falsification test** — can you state an observation that would refute it? Yes → a conclusion. No → an aspiration; it does not belong in the chain.
4. **Provenance test** — is the justification a verified source, or a claim about what people generally do? The latter is banned outright (see Banned Justifications).

## Derivation vs Research vs Plan

Three adjacent artifacts, disjoint authority:

| Dimension | Derivation (this document) | `/speckit.research` | `/speckit.plan` |
|---|---|---|---|
| Object | a **topic** — a domain question | a **feature's** open questions | a **feature's** implementation approach |
| Question answered | *what follows, and by what reasoning* | *what is true / what should we choose* | *how will we build it* |
| Home | `.specify/derive/<topic-slug>/` | `.specify/specs/<key>/research.md` | `.specify/specs/<key>/plan.md` |
| Lifetime | outlives features; reusable across them | bound to one feature | bound to one feature |
| Output shape | source-grounded reasoning chain + derived architecture | decisions & rationale + references | technical design + phase structure |
| Anti-pattern | a literature summary; an architecture with no chain | a derivation chain (use this concept) | re-deriving first principles (cite a Derivation) |

A Plan MAY cite an Architecture Element by identity (`A-k`) instead of re-arguing it. A Derivation MUST NOT cite a Plan — the dependency runs one way, from the feature-bound artifact toward the topic-bound one.

## Source Grounding

Every source is grounded **online** before it may anchor anything. Grounding establishes three things: that the text exists where claimed, who actually originated it, and what it actually says (as opposed to what is commonly said about it).

### Provenance Grades

A closed four-value enum. The engine validates membership; the **grade itself is a judgment** the agent makes from the evidence the engine supplies (see Script / Prompt Boundary).

| grade | definition | may anchor a `D-` step? |
|---|---|---|
| `primary` | the text by the originator of the claim — the author's own site or dissertation chapter; a standards body's own finding text | **yes** |
| `authoritative-secondary` | named, attributable exposition by a recognized practitioner or publisher, or a normative specification restating a primary | **yes**, but MUST NOT be the sole anchor for a claim that a primary contradicts |
| `community` | aggregated, compiled, listicle-shaped, translated, or retitled content | **no** — a finding aid only |
| `unverified` | not resolvable online: dead with no snapshot, paywalled with no abstract, attribution uncheckable, or no online capability this run | **no** |

**Anchor rule (C1, engine-enforced).** Every source reference in a step's `premises` MUST resolve to a row graded `primary` or `authoritative-secondary`. A `community` or `unverified` row may appear only in a step's optional `leads` field — recorded as *how the primary was found*, never as *why the step holds*.

**Grade is capped by content, not by rescue.** A snapshot that recovers an author's own page is still `primary`; a snapshot that recovers a listicle is still `community`. Recovering a dead link improves `access`, never `grade`.

### Source Record

`## Sources` table in `derive.md`:

```
| id | claimed_title | resolved_title | title_mismatch | grade | url | access | resolved_via | verification |
```

| field | content |
|---|---|
| `id` | `S-<nnn>`, engine-issued **per topic**, monotonic, never reused. Because the move library is project-wide while sources are per-topic, a reference that crosses topics uses the qualified form `<topic-slug>.S-<nnn>` — dot-namespaced after the `<goal-slug>.T-<nnn>` precedent in `goal-definitions.md`, and legal under the same identity grammar (which admits `.` but not `#` or `/`) |
| `claimed_title` | **verbatim from the input**, preserved exactly — this field is what makes a retitled source detectable at all. Sources dedup by URL; when one URL arrives under several claimed titles, all variants are retained here joined by an escaped separator (`\|`) so the table stays parseable — the divergence between variants is itself retitling evidence |
| `resolved_title` | the title that online grounding actually established |
| `title_mismatch` | normalized-string inequality between the two, **computed by the engine**, never asserted by the agent |
| `grade` | one of the four provenance grades |
| `access` | `live` \| `wayback:<snapshot-ts>` \| `dead` \| `paywalled` \| `unknown` — every value has a producing path in the Dead-Link Protocol |
| `resolved_via` | `direct` \| `websearch` \| `wayback` |
| `verification` | a **concrete artifact reference**: an HTTP status, a snapshot URL, or the search result that established attribution |

`verification` is the anti-fabrication mechanism. A bare attestation is rejected by the engine (minimum length plus a banned-literal check — the word `verified` alone carries no evidence). If nothing concrete can be cited, the honest grade is `unverified`.

### Dead-Link Protocol

Ordered and deterministic; the engine's `probe-links` action supplies the evidence for steps 1–2 and the agent drives 3:

1. **Direct fetch.** Succeeds → `access: live`, `resolved_via: direct`. Resolves but the body sits behind a paywall with only an abstract public → `access: paywalled`: the abstract may support an attribution judgment, never a move that needs the full argument.
2. **Archive lookup.** Query the archive availability API for a snapshot. Found → `access: wayback:<ts>`, `resolved_via: wayback`; grade follows the snapshot's content.
3. **Attribution search.** No snapshot → one search on title + author for a canonical live copy elsewhere. Found → re-resolve with `resolved_via: websearch` (this is not a dead end). Not found → `access: dead`, `grade: unverified`.
4. **A network failure is not a dead link.** If the probe itself could not run (no connectivity, unreachable host, timeout), record `access: unknown` and `grade: unverified`. An unprobed URL is not evidence of death — recording `dead` there would fabricate a fact the run never established.
5. **Record, never drop.** Every `unverified` source lands in `## Unverifiable Sources` **with its reason**. Silently dropping a source is how a dead link in the input becomes an invisible hole in the chain.

### Title-Mismatch Protocol

Community-compiled titles are the most common defect in a handed-in reading list: a title invented by an aggregator, attributed to an author who never used it. When `title_mismatch: true`:

- the row keeps **both** titles — `claimed_title` is the audit trace of what was handed in, `resolved_title` is what exists;
- every `D-` step citing that `S-<k>` MUST cite `resolved_title`;
- engine check A3 requires `resolved_title` to appear literally in the `derivation` text of each step that uses it.

## Reasoning Move (思维算子)

A **Reasoning Move** is an extracted inference pattern — *how* a source argues, never *what* it concludes. This is the concept's central object: it is what makes a Derivation reusable rather than a one-off reading note.

### Move Record

```
| move_id | name | inference_form | prevents | applies_when | anchor | status |
```

| field | content |
|---|---|
| `move_id` | `M-<nnn>`, engine-issued **project-wide**, monotonic, never reused, never renumbered |
| `name` | short verb-shaped label — `Demote-by-counterexample`, `Separate-the-planes`, `Derive-from-constraint-not-preference` |
| `inference_form` | the *shape* of the inference in 1–2 lines, **with named slots**. The slots are what make it re-applicable to a different domain. Example shape: "Given a claimed property `P` of design `D`, exhibit a counter-instance satisfying `D` but not `P` ⇒ `P` is not entailed by `D`." |
| `prevents` | the failure mode this move blocks — e.g. "accepting a maturity ladder as a definition" |
| `applies_when` | the applicability condition **plus an over-application guard**: when the move is *not* licensed |
| `anchor` | source reference(s) — the source whose *way of arguing* exhibited the move, never the source's claim. Because the library is project-wide while `S-<nnn>` is per-topic, anchors are stored in the **qualified** form `<topic-slug>.S-<nnn>` so they stay resolvable from any later topic |
| `status` | the move's **durable** state: `active` \| `superseded` (a later run found it wrong — retained, never deleted, and never citable again) |

**Durable state vs run-relative disposition.** `status` is the move's durable library state and has exactly two values. How a given run related to a move — `new` (issued this run), `reused` (applied unchanged), `reinforced` (applied and a new anchor added) — is **run-relative**: it is reported by `moves-add` and `stats` output and never stored as a library column. Storing a run-relative value in a durable row is how a library begins contradicting itself on the second run.

An `applies_when` without an over-application guard is incomplete: an unguarded move gets applied everywhere and quietly becomes a dogma, which is the exact failure the concept exists to prevent.

### Move Library

**Location: `.specify/derive/moves.md`** — one table file, project-level, accumulating, git-tracked, **written only by the engine**.

- **One table file, not one file per move.** A run must see the whole library as a single projection at start; N files means N reads or a generated index — new machinery for no gain.
- **At the `.specify/derive/` root, not inside `<topic-slug>/`.** The library is cross-topic by design: a domain-level derivation and a later feature-level one must draw on the same moves.
- **Not under `.specify/memory/`.** That root holds generic project state. Moves are the derivation domain's own accumulated instrument, consumed only by `/speckit.derive` — exactly as `.specify/goal/` holds only goal-domain state. Splitting the library and the archive across two roots would give one concept two homes.
- **Tracked, never ignored.** Unlike re-derivable caches, moves are **not re-derivable** — losing them loses accumulated reasoning capital.

### Projection, Not Copy

An accumulating store that runs also *read* invites a run to snapshot moves into its own `derive.md`, producing a stale copy the next run trusts. Three mechanisms close that:

1. **Read path** — the engine's `moves-list` action emits a summary projection; the run consumes the projection. A bounded full read of `moves.md` is legitimate only while the file stays within the small-file threshold whose sole definition point is `shared/guidelines/token-efficiency.md`; past that, the projection is mandatory.
2. **Write path** — the engine's `moves-add` action is the **only** writer. It dedups on normalized `inference_form`; on a near-duplicate it **refuses** and returns the existing `move_id`, so the run reinforces the recorded move instead of forking a variant.
3. **Citation in the artifact** — a run's `## Reasoning Moves Applied` section cites `M-<nnn>`. Where inline readability needs the form spelled out, it is marked as a projection (`<!-- projection of moves.md#M-012 -->`). Engine check A9 rejects any `derive.md` carrying a full move row whose `inference_form` differs from the library's row for that id.

## Derivation Chain

The chain is where the method is actually replayed. Each step instantiates one move against explicit premises and yields one falsifiable conclusion that later steps may consume.

### Step Record

`## Derivation Chain` section:

```markdown
### D-<k>
- premises:       S-<a>, S-<b>, D-<j>   # verified sources and/or EARLIER steps
- leads:          S-<c>                  # optional: community/unverified finding aids
- move:           M-<nnn>                # exactly one
- derivation:     <the inference, slots instantiated — 2–6 lines>
- conclusion:     <one falsifiable statement>
- falsification:  <what observation would refute this, and whether it was checked>
- confidence:     derived | provisional | contested
- contested-with: D-<m>                  # present iff confidence == contested
```

### Chain Integrity Rules

Rules marked *engine* are mechanically enforced by `validate`; *semantic* ones are the agent's responsibility and are listed in `semanticChecksPending` so they must be attested rather than inherited as green.

| # | Rule | Owner |
|---|---|---|
| **C1** | **No orphan premises.** Every `S-<k>` in `premises` exists in `## Sources` with grade ∈ {`primary`, `authoritative-secondary`}. Every `D-<j>` has `j < k` — the chain is a DAG in step order: no forward references, no cycles. | engine |
| **C2** | **Exactly one move per step.** Zero moves is an unreasoned assertion; two moves are two steps. | engine |
| **C3** | **No banned justifications.** `derivation` and `conclusion` MUST NOT contain any literal from the closed set below. | engine (literal scan) |
| **C4** | **Non-vacuous falsification.** Not `none` / `n/a` / `-`, and not a restatement of `conclusion` (the engine catches identity and near-identity); whether it is a *genuine* refutation condition is semantic. | engine + agent |
| **C5** | **Contradictions are recorded, never averaged.** See Contradiction Handling. | engine (propagation) + agent (discriminator) |
| **C6** | **Termination is declared.** Stop on either (a) every in-scope architecture element traces to a `D-<k>`, or (b) the next step would need a premise no verified source supplies — that gap becomes an open question, **never an invented premise**. A step budget (`--max-steps`) prevents runaway; hitting it is reported, not hidden. The run states which condition fired. | engine (budget) + agent (a-vs-b) |
| **C7** | **No conclusion laundering.** A `conclusion` that merely restates a source's claim with no inference is a citation wearing a derivation's clothes. The engine catches the degenerate forms (empty or under-length `derivation`, or a conclusion identical to a source title); the general case is semantic. | engine + agent |

### Banned Justifications

The closed literal set owned by C3. These are the phrases that let an unexamined preference pass as a derived conclusion. The engine scans `derivation` and `conclusion` for each, case-insensitively where the literal is Latin script:

`best practice` · `best practices` · `industry standard` · `commonly accepted` · `it is generally agreed` · `everyone knows` · `as is well known` · `obviously` · `业界通用` · `业界最佳实践` · `最佳实践` · `众所周知` · `经验之谈` · `权威做法` · `不言而喻`

The set is **closed**: adding a literal is a change to this document and to the engine together, never a per-run decision. A run that genuinely needs to report what the industry generally does must cite a verified source that says so — which converts a banned phrase into an anchored premise.

### Contradiction Handling

When two grounded sources' moves yield conflicting conclusions, the chain MUST NOT pick one silently and MUST NOT average them:

1. Emit `confidence: contested` on the step.
2. Record both branches with reciprocal `contested-with` links.
3. State the **discriminating question** — the specific evidence that would settle it.
4. Route the residue to `## Open Questions`.

**Uncertainty propagates (engine-enforced).** A `contested` step MUST NOT be a premise of a `derived`-confidence step. Any step consuming a `contested` premise is itself at best `provisional`. This is why element confidence is inherited as a **minimum** (see Traceability Rule): a contested step can never silently yield a solid element.

## Derived Architecture

The terminal product. It is *derived*, not designed: every element exists because a chain step entailed it.

### Element Record

`## Derived Architecture` section:

```markdown
### A-<k> <element name>
- statement:      <what the architecture asserts>
- derived-from:   D-<a>, D-<b>              # MANDATORY, >=1, all must resolve
- confidence:     derived | provisional | contested   # = MIN over its D-steps
- open-questions: Q-<j>, ...                # iff any part is undetermined
```

`A-<k>` is issued **per topic**. A citation that crosses scopes — a Plan referencing an element from a derivation it did not produce — uses the qualified form `<topic-slug>.A-<k>`, the same convention the move library uses for source anchors. Within its own artifact the bare form is correct.

### Traceability Rule

Every `A-<k>` carries a non-empty, fully resolving `derived-from`. An element with none is a **hard validation failure** — the engine refuses the file rather than emitting a warning. Confidence is inherited as the **minimum** over the element's steps, so `contested` can never be laundered into `derived` by composition.

### Open Questions

Where the chain ran out of grounded premises:

```markdown
### Q-<k>
- question:          <what is not determined>
- why-undetermined:  <which premise is missing, or which sources conflict>
- would-resolve:     A-<a>, A-<b>            # which elements it blocks
- discriminator:     <what evidence would settle it>
```

Links are **bidirectional and engine-checked**: every `Q-<k>` referenced from an element must exist, and every `Q-` listing `would-resolve: A-<x>` must be listed back on `A-<x>.open-questions`. A blocked element MUST be `provisional` or `contested`.

**Never silently filled.** A plausible-sounding gap-fill is the precise failure mode this concept exists to prevent: it produces an architecture that looks derived and is not.

## Self-Audit

`## Self-Audit` is a fixed table `| # | check | method | result |`. The engine emits results for A1–A10, A12, A13; the agent attests A11 and A14.

| # | Check | Method |
|---|---|---|
| A1 | every source row has a grade and a non-empty, non-generic `verification` | engine |
| A2 | no step is anchored solely on `community` / `unverified` | engine |
| A3 | every `title_mismatch: true` row's `resolved_title` is cited in all steps using it | engine (literal) |
| A4 | zero orphan premises; zero forward or cyclic `D-` references | engine |
| A5 | zero banned justifications | engine |
| A6 | every `D-<k>` has a non-vacuous `falsification` | engine |
| A7 | every `A-<k>` has ≥1 resolving `derived-from` | engine |
| A8 | no `derived`-confidence element rests on a `contested` step | engine |
| A9 | every cited `M-<nnn>` exists in the move library; no divergent restated row | engine |
| A10 | every undetermined point appears in `## Open Questions`; `Q ↔ A` links resolve both ways | engine |
| A11 | online grounding actually happened this run — ≥1 search or fetch per source, recorded in `verification` | **agent attestation** |
| A12 | step count reported against budget, and the termination condition that fired is declared as (a) or (b) | engine (count vs budget) + agent (which condition) |
| A13 | every move this run reports as newly issued resolves to a row in the move library — it went through `moves-add`, the sole writer, rather than being hand-written into the artifact | engine |
| A14 | the artifact states the sources' **way of thinking**, not a summary of their content | **agent (semantic) — the reason this command exists** |

`validate` returns `semanticChecksPending` listing A11 and A14 so they must be attested explicitly rather than inherited as green. **A run whose `## Self-Audit` shows any engine check red MUST report the failure honestly and MUST NOT present its architecture as derived.**

## Capability Degradation

Not every supported host CLI exposes an online search or fetch capability. A command whose central requirement is online grounding must degrade honestly rather than fake it:

If no online capability is available this run, the run MUST NOT fabricate grounding. Every source is graded `unverified` with reason `no-online-capability`, all land in `## Unverifiable Sources`, **no `D-` step may anchor** (C1 fails by construction), and the run stops before building the chain and reports the degradation. A degraded run produces an honest empty result — never a confident unverified one.

## Script / Prompt Boundary

Which parts are deterministic (engine) and which are judgment (agent). The boundary follows the project's token-efficiency discipline (`shared/guidelines/token-efficiency.md`), cited here rather than restated.

**Engine-owned** — pattern matching, structural validation, counting, dedup, comparison, identity issuance:

- identity grammar and monotonic ID issuance for `S-`, `M-`, `D-`, `A-`, `Q-`
- link liveness probing and archive lookup (evidence gathering, offline-tolerant)
- `title_mismatch` computation
- all of C1–C7's mechanical halves and A1–A10, A12, A13
- move-library dedup and sole-writer append
- the banned-justification literal scan

**Agent-owned** — irreducibly semantic:

- reading a source's actual argument and abstracting its inference pattern into a move
- **assigning the provenance grade** — the engine supplies evidence (status, snapshot, attribution hit); the agent judges whether the text is the originator's
- a move's `applies_when` and its over-application guard
- choosing which branch of a `contested` step to carry, and naming the discriminating question
- deciding termination condition (a) vs (b)
- attesting A11 and A14

The engine's link probe is a **corroborator** that leaves an unfabricable trace, not a replacement for the agent's own reading. No test may invoke it against the real network.

## Storage

```
.specify/derive/
├── moves.md                    # the accumulating project-level move library (engine-written only)
└── <topic-slug>/
    └── derive.md               # one Derivation — sources, moves applied, chain, architecture, audit
```

Both are git-tracked. The library is cross-topic; each topic directory holds one Derivation. Terminal or superseded content is retained, never deleted — a superseded move stays in the library with `status: superseded` so the reason it was abandoned remains discoverable.

## Terminology Boundaries

| Term | Meaning | Where defined |
|---|---|---|
| **Derivation** (this document) | A topic-scoped artifact reaching an architecture by replaying verified sources' reasoning methods | here; store `.specify/derive/<topic-slug>/derive.md` |
| **Reasoning Move** (思维算子) | An extracted inference pattern with named slots — *how* a source argues, never what it concludes | here; store `.specify/derive/moves.md` |
| **Move Library** | The accumulating project-level table of moves, engine-written only | here |
| **Provenance Grade** | The four-value authority classification of a grounded source | here |
| **Derivation Step** (`D-k`) | One move applied to explicit premises, yielding one falsifiable conclusion | here |
| **Architecture Element** (`A-k`) | A derived architectural assertion, traceable to ≥1 step | here |
| **Open Question** (`Q-k`) | A recorded gap where grounded premises ran out — never silently filled | here |
| **Research** | Feature-scoped evidence gathering and decision rationale | `/speckit.research`; `.specify/specs/<key>/research.md` |
| **Plan** | Feature-scoped implementation approach; MAY cite an `A-k`, never the reverse | `/speckit.plan` |
| **Goal** | Project-level authored end state, measured by degree — a different plane entirely | `goal-definitions.md` |
| **"derive" elsewhere** | `derive` as an ordinary verb in other engines (generating a view from a truth source, e.g. a probe map or a feature index) — **unrelated** to this concept | their owning docs |
