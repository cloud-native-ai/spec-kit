# Derivation: rest-architecture

Concept authority: `shared/definitions/derivation-definitions.md` — the record schemas, provenance grades, chain rules C1–C7 and audit checks A1–A14 are defined there and referenced here, never restated.

**Run**: 2026-09-05 · dogfood run against the handed-in REST/Web-architecture reading list that motivated this capability.

**Headline result**: of six handed-in sources, **one** could be grounded. Two are dead with no archived snapshot; three are blocked at the origin (HTTP 403) and could not be resolved further in this environment. Exactly one architectural conclusion is therefore derivable, and the rest of the intended chain is recorded as an open question rather than invented.

## Sources

| id | claimed_title | resolved_title | title_mismatch | grade | url | access | resolved_via | verification |
|---|---|---|---|---|---|---|---|---|
| S-001 | Fielding on REST: The "REST Maturity Model" is NOT REST |  | false | unverified | https://roy.gbiv.com/untangled/2013/rest-maturity-model-is-not-rest | unknown | direct | host fetch returned HTTP 403 on 2026-09-05; engine probe degraded to unknown (SOCKS egress); the handed-in list itself states this title is a community compilation, not the original |
| S-002 | In Search of the Perfect URL |  | false | unverified | https://roy.gbiv.com/untangled/2009/in-search-of-the-perfect-url | unknown | direct | host fetch returned HTTP 403 on 2026-09-05; engine probe degraded to unknown (SOCKS egress); no canonical copy resolved |
| S-003 | How I Explained REST to My Brother |  | false | unverified | https://tomayko.com/writings/rest-in-plain-text | dead | wayback | host fetch returned HTTP 404 on 2026-09-05; archive availability API returned no snapshot; the handed-in list had already disclosed this link was dead |
| S-004 | The C10K Problem | The C10K problem | false | primary | http://www.kegel.com/c10k.html | live | direct | host fetch returned HTTP 200 with the full page body on 2026-09-05 — "The C10K problem", Dan Kegel, 1999, on the author's own site |
| S-005 | A Brief Introduction to Representational State Transfer (W3C TAG Finding) |  | false | unverified | https://www.w3.org/2001/tag/doc/REST.html | dead | wayback | host fetch returned HTTP 404 on 2026-09-05; archive availability API returned no snapshot; the handed-in list presented this as the authoritative W3C definition and did NOT disclose that it is dead |
| S-006 | Hypermedia and HATEOAS: Why Bother? |  | false | unverified | http://amundsen.com/hypermedia/ | unknown | direct | host fetch returned HTTP 403 on 2026-09-05; engine probe degraded to unknown (SOCKS egress); no canonical copy resolved |

On `title_mismatch`: it is engine-computed by normalized comparison of the two title cells, and an empty `resolved_title` yields `false` plus an `unresolved-title` warning — absence of evidence is not evidence of retitling. S-001 is the one source the handed-in list flags as carrying a community-compiled title, but because the origin returned 403 the original title could not be established, so no mismatch is asserted. The suspicion is recorded as prose here rather than encoded as a computed fact this run cannot support.

## Unverifiable Sources

Five of six. None is dropped; each carries the reason it could not ground.

- **S-001** — origin returned HTTP 403; the engine probe could not egress (SOCKS proxy). Additionally flagged by the handed-in list as a community-compiled title, so even its *identity* is unresolved, not only its content.
- **S-002** — origin returned HTTP 403; the engine probe could not egress. No canonical copy resolved.
- **S-003** — HTTP 404 and **no archived snapshot**. The handed-in list disclosed this link was dead; grounding confirms it is unrecoverable by the protocol's first two steps.
- **S-005** — HTTP 404 and **no archived snapshot**. This is the defect the handed-in list did *not* disclose: it presented this as the authoritative W3C definition and ranked it for readers needing a normative citation. It is dead at the cited location.
- **S-006** — origin returned HTTP 403; the engine probe could not egress. No canonical copy resolved.

## Reasoning Moves Applied

Cited by identity from `.specify/derive/moves.md`:

- `M-001` Locate-the-binding-constraint — disposition `new` this run, anchored on `rest-architecture.S-004`.

Disposition log for this run — read by `stats`; a two-column run-relative log, not a restatement of any library row:

| move_id | disposition |
|---|---|
| M-001 | new |


Five further moves were *candidates* on the handed-in list's own framing (demote-by-counterexample, identifier-opacity, coupling-inversion, dialogue-reduction, normative-check). **None was extracted.** A move must be abstracted from a source's actual argument, and five of the six arguments could not be read. Extracting them from the list's *descriptions* would have manufactured reasoning moves out of a bibliography — precisely the substitution this command exists to refuse.

## Derivation Chain

### D-1
- premises: S-004
- leads: S-001, S-005
- move: M-001
- derivation: S-004 documents that at the 10,000-concurrent-client scale the binding constraint stopped being hardware and became OS limits on file descriptors and threads — cost that accrues per simultaneous connection rather than per unit of compute or bandwidth. Instantiating the move with `S` = a web server, `F` = raw hardware capacity, `R` = per-connection kernel-visible resource: the factor the field believed was limiting is not the one whose cost grows with load, so designs are constrained by `R` and must be evaluated by their consumption of it. Two leads (S-001, S-005) point at protocol-level consequences of this, but neither could be grounded, so neither is used as a premise.
- conclusion: The binding constraint on web-scale server architecture is per-connection resource cost, not raw hardware capacity.
- falsification: A measured server whose simultaneous-connection count scales linearly with hardware capacity while file-descriptor and thread limits remain fixed and non-binding. Not observed in S-004, which documents the opposite.
- confidence: derived

## Termination

- condition: b
- steps: 1 / 12

Terminated on **(b)**: the next step would need a premise no verified source supplies. Moving from "per-connection cost is the binding constraint" to any claim about statelessness, cacheability, layered systems or hypermedia requires a source that derives protocol constraints from connection economics. Every candidate for that argument (S-001, S-002, S-003, S-005, S-006) is unverified. Inventing the premise was available and was not done.

## Derived Architecture

### A-1 Per-connection cost is the evaluating constraint
- statement: A web-scale server architecture must be evaluated by its per-connection resource cost; designs holding kernel-visible state per simultaneous client are constrained first, and hardware capacity is not the limiting axis.
- derived-from: D-1
- confidence: derived

One element. That is the honest yield of this input in this environment — not a shortcoming of the method, but its correct output when five of six sources cannot be read.

## Open Questions

### Q-1
- question: Does the per-connection cost constraint entail that the application protocol must be stateless, cacheable and layered, and that hypermedia is the mechanism for keeping client-server coupling bounded?
- why-undetermined: S-004 establishes the constraint but says nothing about protocol design. The sources that would carry that argument are all unverified — S-003 and S-005 are dead with no snapshot; S-001, S-002 and S-006 are blocked at the origin and could not be resolved further here.
- would-resolve:
- discriminator: A retrievable primary text deriving protocol constraints from connection economics — the author's own dissertation chapter on the architectural style, or the standards body's finding on resource and representation, obtained from a location that does not return 403 or 404.

`would-resolve` is deliberately empty: no derived element is blocked by this question, because the elements it would have produced were never derived. That is a signal worth keeping — an open question that blocks nothing marks scope the run could not reach, not scope it reached and left uncertain.

## Self-Audit

| # | check | method | result |
|---|---|---|---|
| A1 | source grades and verification evidence | engine | pass |
| A2 | no step anchored on community/unverified; every unverified source recorded | engine | pass |
| A3 | retitled sources cited by resolved title | engine | pass |
| A4 | no orphan premises, no forward or self references | engine | pass |
| A5 | no banned justifications | engine | pass |
| A6 | non-vacuous falsification on every step | engine | pass |
| A7 | every element has a resolving derived-from | engine | pass |
| A8 | element confidence equals the minimum over its steps | engine | pass |
| A9 | every cited move exists in the library and is not superseded | engine | pass |
| A10 | open-question links resolve both ways; contested steps routed | engine | pass |
| A11 | online grounding actually happened this run | six URLs attempted with the host fetch tool; two additionally queried against the archive availability API; every outcome recorded with its HTTP status in the verification column | attested |
| A12 | step count against budget and termination condition declared | engine | pass |
| A13 | every move reported as newly issued resolves to a library row | engine | pass |
| A14 | the artifact states the sources' way of thinking, not a summary of their content | M-001 is recorded as an inference schema with named slots (S, F, R) re-applicable outside web architecture, and D-1 instantiates those slots rather than restating S-004; no section of this artifact summarizes what the sources say | attested |

## Defects this run surfaced

Recorded because a dogfood run that finds nothing is not looking:

1. **`probe-links` cannot egress in a SOCKS-proxied environment.** stdlib `urllib` has no SOCKS support, and this project's own runtime depends on `httpx[socks]` for exactly that reason. All six probes returned `access: unknown`. Fixed during this run: the engine detects a SOCKS proxy and emits a note naming the variable, and the command template states that `unknown` is not evidence of death and must be followed by grounding with the host's own fetch tool.
2. **The handed-in list's own reliability claims did not survive contact.** It disclosed one dead link (S-003) and one community-compiled title (S-001), but presented S-005 as an authoritative normative citation without disclosing that the cited location is 404 with no snapshot. A reader who trusted its ranking for "需要权威引用和规范依据的人" would have anchored on a dead URL.
3. **Malformed move input is rejected loudly, not silently.** An unquoted JSON value in a `moves-add` payload produced exit 2 with the exact parse position rather than a partial write — the all-or-nothing input contract working as specified.
4. **A bare `S-<nnn>` anchor cannot be accepted.** `moves-add` carries no topic, so it cannot qualify a bare reference; accepting one would write a row that fails the library's own `anchor-form` invariant on the next `validate`. The engine rejects it at input with exit 2 instead.
