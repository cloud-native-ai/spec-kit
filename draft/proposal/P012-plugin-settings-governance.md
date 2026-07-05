# P012 — Plugin Packaging, Settings & Portfolio Governance

- **Status:** Draft
- **Pillars:** Infra
- **Source projects:** claude-code-py, intellegix-code-agent-toolkit
- **Value:** M–H · **Effort:** M–H · **Phase:** 2
- **Related:** [[P001]], [[P002]], [[P013]]

## Problem / Gap

spec-kit can *author* rich components — skills (`skills/*/SKILL.md`), agents
(`.specify/agents/*.agent.md`), commands (`templates/commands/*.md`), tool records, and the
drafted extensions/presets/bundles/workflows ecosystem (`draft/skills/spec-kit-extensions/`).
But it lacks the *infrastructure* to distribute, govern, and constrain those components at
scale:

1. **No distribution/versioning story.** A team that builds a domain-specific spec-kit
   configuration (its skills + commands + agents + workflows) has no packaged, versioned,
   installable unit and no index to discover others'. The `spec-kit-extensions` skill defines
   *catalogs* (`catalog.json` / `catalog.community.json`) and per-artifact install, but there
   is no manifest that packages a whole role/domain configuration as one bundle, and no
   marketplace convention above the catalog.
2. **No layered/managed settings.** Configuration today is effectively per-project
   (`.claude/settings.local.json` and the like). There is no precedence hierarchy, no
   enterprise-locked tier, and no ready-made strict/lax/sandbox profiles — so an org cannot
   set non-overridable policy once [[P001]] hooks and packaged plugins exist.
3. **No portfolio/lifecycle governance.** spec-kit's constitution encodes *per-project
   principles*, but there is no *cross-project* layer: project tiers, lifecycle phases with
   phase-appropriate Allowed/Forbidden constraints, or an anti-pattern checklist. Autonomous
   agents over-engineer (auth/CI/monitoring in a prototype) precisely because nothing gates
   work by phase.

## Proposal

Add three Infra layers, each expressed as manifests + templates + a small resolver script,
layering on top of the existing ecosystem without disturbing `/speckit.*`:

- **A. Plugin manifest + marketplace.** A `speckit-pack.json` manifest that packages a set of
  spec-kit components with auto-discovery of `commands/ agents/ skills/ hooks/ mcp`, plus a
  `marketplace.json` index and an `install-pack.sh` installer. Sits *above* the
  spec-kit-extensions catalog: an extension/preset/bundle is a *kind of* packable component;
  a pack is the versioned distribution envelope + marketplace entry.
- **B. Layered + managed settings.** A `.specify/settings.json` schema with a precedence
  resolver (managed > project > user > defaults), an enterprise-locked `managed-settings.json`
  tier with policy keys (`allowManagedHooksOnly`, `allowManagedPermissionRulesOnly`,
  `strictKnownMarketplaces`, `disableBypassPermissionsMode`), and three ready-made profiles
  (strict / lax / sandbox).
- **C. Portfolio governance.** A `.specify/portfolio.md` registry (project **tiers T1–T4**,
  lifecycle **phases** with per-phase Allowed/Forbidden tables), an anti-pattern checklist, and
  a **Phase-Gate** preamble step that `/speckit.plan` / `/speckit.implement` can optionally run
  to reject phase-forbidden work.

## Design sketch

### A. Plugin manifest + marketplace

```
my-pack/
  speckit-pack.json         # manifest (auto-discovers the dirs below)
  commands/  agents/  skills/  hooks/  mcp/servers.yml
```

```json
// speckit-pack.json
{
  "name": "backend-sdd-pack",
  "version": "1.2.0",
  "author": "platform-team",
  "keywords": ["backend", "fastapi", "sdd"],
  "speckit_version": ">=0.4",
  "components": {
    "commands": "commands/", "agents": "agents/",
    "skills": "skills/", "hooks": "hooks/hooks.json",
    "extensions": ["extensions/*/extension.yml"],
    "presets": ["presets/*/preset.yml"]
  }
}
```

```json
// marketplace.json  (index of packs; org or community)
{ "packs": [
  { "name": "backend-sdd-pack", "version": "1.2.0",
    "source": "github:org/backend-sdd-pack", "category": "backend",
    "install_allowed": true }
] }
```

```
specify pack init                     # scaffold a pack skeleton
specify pack validate <dir>           # manifest + component-schema checks (reuse P013 validator)
specify pack install <name|source>    # resolve → verify → install components into .specify/
specify pack list [--json]            # installed packs + versions
```

Auto-discovery follows the claude-code-py convention (components at pack root, manifest
declares paths, portable references). Packs reuse [[P013]]'s `generated_by` version stamps so
`install`/`update` is idempotent and can prune components of a pack version no longer selected.
Crucially, a pack can *contain* spec-kit-extensions artifacts — the pack is the outer
distribution unit; extensions/presets/bundles remain the inner composition mechanism.

### B. Layered + managed settings

```
Precedence (highest → lowest):
  managed-settings.json   (enterprise, non-overridable)
  .specify/settings.json  (project)
  ~/.specify/settings.json (user)
  packaged defaults
```

```jsonc
// managed-settings.json  — org-locked policy tier
{
  "allowManagedHooksOnly": true,          // only org-supplied hooks run
  "allowManagedPermissionRulesOnly": true,
  "strictKnownMarketplaces": true,        // packs only from allow-listed marketplaces
  "disableBypassPermissionsMode": true,
  "permissions": { "deny": ["Bash(rm -rf:*)"] }
}
```

Resolver in `scripts/bash/common.sh` (+ a Python mirror) merges the layers with managed keys
winning and *locked* (a locked key cannot be re-set by a lower layer). Three profile templates
ship under `templates/settings/`:

| Profile | Intent |
|---|---|
| `settings-strict.json` | ask/deny-heavy; managed hooks only; no bypass |
| `settings-lax.json` | permissive defaults for trusted solo use |
| `settings-sandbox.json` | bash sandboxed; network/deny rules for untrusted packs |

This is the policy substrate [[P001]]'s hooks and (A)'s packs need: `allowManagedHooksOnly`
governs which hooks fire; `strictKnownMarketplaces` governs which packs install.

### C. Portfolio governance

```
.specify/portfolio.md         # registry: projects, tier, phase, active-branch budget
templates/portfolio.md        # starter
templates/phase-gate.md       # the Allowed/Forbidden preamble step
```

```md
# Portfolio
| Project | Tier | Phase | Active feature branches (max) |
|---------|------|-------|-------------------------------|
| billing | T1   | Hardening   | 2 |
| sandbox | T4   | Prototype   | 1 |

## Phase constraints
| Phase       | Allowed                          | Forbidden                         |
|-------------|----------------------------------|-----------------------------------|
| Prototype   | core feature, throwaway spikes   | auth, CI, monitoring, perf tuning |
| Development | tests, CI, structured modules    | premature scaling, multi-region   |
| Hardening   | perf, security, observability    | new unscoped features             |
| Maintenance | bug fixes, dependency bumps      | large refactors                   |

## Anti-patterns (constitution defaults)
- Building infra before the feature works
- >N active feature branches (velocity constraint)
- Adding auth/monitoring in Prototype
```

**Phase-Gate step** (a template preamble, opt-in): before planning/implementing, read the
project's tier+phase from `portfolio.md`, and if the requested work appears in the current
phase's *Forbidden* column, stop and require explicit override. Ships as
`templates/phase-gate.md` that `/speckit.plan` / `/speckit.implement` can *include*; the base
commands are unchanged unless a project opts in by adding a `portfolio.md`.

## Source evidence

- Plugin/marketplace manifest + auto-discovery of commands/agents/skills/hooks/mcp →
  `_research/claude-code-py.md` idea #3 (`.claude-plugin/marketplace.json`,
  `plugins/*/.claude-plugin/plugin.json`, `plugins/plugin-dev/skills/plugin-structure/SKILL.md`).
- Component scaffold/validate meta-toolkit (pack validate) →
  `_research/claude-code-py.md` idea #4 (`plugins/plugin-dev/commands/create-plugin.md`,
  `.../hook-development/scripts/validate-hook-schema.sh`).
- Layered + managed/enterprise settings, precedence, lock keys, strict/lax/sandbox profiles →
  `_research/claude-code-py.md` idea #5 (`examples/settings/settings-{strict,lax,bash-sandbox}.json`,
  `examples/mdm/managed-settings.json` + README).
- Portfolio governance: tiers T1–T4, phases with Allowed/Forbidden, anti-patterns, velocity
  constraints, phase-gate preamble →
  `_research/intellegix-commands-agents-mcp.md` idea #2
  (`portfolio/PORTFOLIO.md.example`, `portfolio/DECISIONS.md`, `portfolio/PROJECT_TEMPLATE.md`;
  enforced in `commands/implement.md` / `commands/smart-plan.md` "Phase 0: Portfolio Gate").
- spec-kit surfaces built on: `draft/skills/spec-kit-extensions/SKILL.md` (catalog + install
  layer this sits above), `.specify/agents/*.agent.md`, `skills/*/SKILL.md`,
  `scripts/bash/common.sh` (settings resolver host), the capability matrix in
  `src/specify_cli/__init__.py` (`audit_capability_matrix`, `_ASSISTANT_TIERS`),
  `generated_by` idempotency from [[P013]].

## Adoption plan

All three layers land in `draft/`; each is independently adoptable and the `/speckit.*` flow
is untouched unless a project opts in.

1. **Settings (B).** Add `templates/settings/{strict,lax,sandbox}.json`, the
   `.specify/settings.json` schema, and a precedence resolver in `common.sh` + Python mirror.
   Pure config — no runtime behavior until a consumer (hooks/packs) reads it. Land first
   because (A) and [[P001]] depend on it.
2. **Portfolio (C).** Add `templates/portfolio.md`, `templates/phase-gate.md`, and the
   anti-pattern list as optional constitution defaults. A project opts in by creating
   `.specify/portfolio.md`; `/speckit.plan`/`/speckit.implement` include the gate only when it
   exists. Markdown-only, zero-risk.
3. **Packs (A).** Add `speckit-pack.json` + `marketplace.json` schemas, `install-pack.sh`,
   and `specify pack init|validate|install|list`; reuse [[P013]]'s validator for `validate`
   and its `generated_by` stamps for idempotent install/prune. Ship spec-kit's own
   skills/commands as the first pack to dogfood the format. Honor `strictKnownMarketplaces`
   from (B).

## Risks & mitigations

- **Ecosystem sprawl / overlap with spec-kit-extensions.** Keep a crisp boundary: packs are
  the *distribution + versioning + marketplace* envelope; extensions/presets/bundles remain
  the *composition* mechanism. A pack simply contains and pins them. Document this in the
  extensions skill's provenance note.
- **Supply-chain risk from third-party packs.** Default `strictKnownMarketplaces: true` in the
  strict profile; community marketplace entries are format-verified, not audited (inherit the
  extensions skill's caveat); `pack validate` runs before install; managed settings can lock
  installs to an org marketplace.
- **Managed-settings foot-guns.** A too-strict locked profile can brick a project. Ship the
  resolver with clear precedence reporting (a `specify settings explain` view echoing which
  layer set each key) and keep MDM/OS packaging explicitly out of scope initially.
- **Governance friction.** Phase gates that block too aggressively frustrate users. Make the
  gate *advisory-with-override* by default, opt-in per project, and ship sane default
  phase tables teams can edit.
- **Config drift across harnesses.** Reuse the [[P013]] adapter registry so any per-harness
  settings/pack file is generated from one source, not hand-maintained per assistant.

## Value / Effort rationale

**Value M–H:** turns spec-kit from a single repo into an *ecosystem* (packs + marketplace),
gives orgs the policy substrate they need before hooks and third-party packs are safe
(managed settings), and closes the named cross-project governance gap (portfolio tiers/phases)
that directly curbs a top autonomous-agent failure mode (over-engineering). Rated M–H rather
than H because each layer is adopted by teams that have outgrown single-project use, not by
every user on day one.

**Effort M–H:** the settings resolver and portfolio templates are small and mostly
declarative; the pack/marketplace layer (manifest schema, installer, idempotent update/prune,
marketplace resolution, and interaction with the existing catalog layer) is the substantive
piece, landing the overall estimate at M–H and sequencing packs last within the proposal.
