# Probe System

The umbrella probe infrastructure (spec 056): every detection point in the framework is a
first-class, queryable, modifiable entity. This page is the documentation face; the truth
sources own every fact and are never restated here.

| Layer | Truth source | One-line |
|-------|--------------|----------|
| Probe Class × Probe Object | `shared/definitions/probe-definitions.md` § Classes / § Objects | feature × instantiation of every detection point |
| Handler | same file § Handler | reusable reactions (`h-` ids; kind ∈ {engine, agent, gate}; behavior-owner pointers, never rule copies) |
| HandlerBinding | same file § HandlerBinding | subscriptions: `@point:<lifecycle_point>` + scope; identity = (handler, selector, scope) |

Lifecycle points: `wrap-up` / `situation` / `phase-boundary` / `confirm-gate`. The
`wrap-up` face is **compiled**: `compile-embeds` renders each unit's single
AUTO-GENERATED `## Wrap-up` section (banner-fingerprinted); the other points are
declarative runtime subscriptions.

## Engine CLI — `probe-utils.py`

| Action | Purpose |
|--------|---------|
| `probes` | Print / validate (`--validate`, exit 2) / reconcile (`--reconcile`) the registry |
| `map` | Rebuild the rendered `probe-map.md` deterministically |
| `probe-inject` | Register an external probe object for a client-project custom unit |
| `handlers` | List/filter/validate Handlers and HandlerBindings |
| `compile-embeds` | Render the compiled `## Wrap-up` faces; `--check` pre-checks drift |

## Compile flow (fixed order)

1. `probe-utils.py --action compile-embeds` — framework-source faces (`templates/`, `skills/`)
2. `scripts/python/regen-command-copies.py` — per-tool command copies
3. `scripts/python/sync-mirrors.py` — `.specify/` mirrors

`--check` semantics: regenerable drift (stale render of an older registry state) exits 1;
structural classes (orphan/missing handler lines in a current-fingerprint artifact,
illegal action, order conflict, wording gate) exit 2. Adding a mechanism = register rows +
recompile — never hand-edit a compiled section (the banner says so).

## Host boundary (read-only)

A downstream project MAY run the query faces (`probes` / `handlers` lists) to answer
"which detection points and handlers does this installation have". It MUST NOT get the
Handler/HandlerBinding registration or compile write faces — registration lives on the
framework truth-source side only (056 Q6 ruling). Host-side handler authoring is recorded
as Future Evolution in the feature detail file.

Related: the feedback-domain instance and its engine are documented in
[feedback.md](feedback.md); glossary anchors: Probe (umbrella) / Handler / HandlerBinding
in `.specify/memory/glossary.md`.
