# Preset format reference

Presets are stackable, priority-ordered collections of **template and command overrides**. They customize both the artifacts produced by the SDD workflow (specs, plans, tasks, checklists, constitutions) and the commands that guide the LLM in creating them — without forking or editing core files. Installed under `.specify/presets/<preset-id>/`.

> Adapted from upstream `main:presets/README.md`, `main:presets/ARCHITECTURE.md`, `main:presets/lean/preset.yml`.

## Manifest structure

```yaml
schema_version: "1.0"

preset:
  id: "lean"
  name: "Lean Workflow"
  version: "1.0.0"
  description: "Minimal core workflow commands - just the prompt, just the artifact"
  author: "github"
  repository: "https://github.com/github/spec-kit"
  license: "MIT"

requires:
  speckit_version: ">=0.6.0"

provides:
  templates: [...]     # template / command / script override entries

tags: ["lean", "minimal", "workflow", "core"]
```

## `provides.templates` entries

Despite the key name, this list holds **template, command, and script** overrides. Each entry:

```yaml
provides:
  templates:
    - type: "command"                 # template | command | script
      name: "speckit.specify"         # which artifact in the resolution stack to compose with
      file: "commands/speckit.specify.md"   # actual content file (may differ from name path)
      description: "Lean specify - create spec.md from a feature description"
      replaces: "speckit.specify"     # for command overrides: the command being replaced
      strategy: "replace"             # compose strategy (default: replace)
```

| Field | Required | Notes |
|-------|----------|-------|
| `type` | yes | `template`, `command`, or `script`. |
| `name` | yes | Identifies the target artifact in the priority stack (e.g. `spec-template`, `speckit.specify`). |
| `file` | yes | Path to the content that provides/composes it. Convention is `templates/<name>.md` but may differ. |
| `description` | recommended | Shown in listings. |
| `replaces` | command only | The command name being overridden. |
| `strategy` | no | `replace` (default) \| `prepend` \| `append` \| `wrap`. |

## Resolution stack (recap)

At runtime a resolver walks, first match wins:

1. `.specify/templates/overrides/` — project-local one-off overrides (highest)
2. `.specify/presets/<preset-id>/templates/` — installed presets, sorted by `priority` (lowest number wins)
3. `.specify/extensions/<ext-id>/templates/` — extension-provided templates
4. `.specify/templates/` — core templates (lowest)

If no preset is installed, core templates are used unchanged. Files are copied into `.specify/presets/<id>/` at install, but the stack is walked on **every** lookup rather than pre-merged.

## Priority and stacking

Multiple presets can be installed at once. `--priority` (lower = higher precedence) decides who wins when two presets provide the same `name`:

```bash
specify preset add enterprise-safe --priority 10       # base layer
specify preset add healthcare-compliance --priority 5   # overrides enterprise-safe
specify preset add pm-workflow --priority 1             # overrides everything
```

Presets **override by default** — with the `replace` strategy the lowest-priority-number preset wins entirely. To augment instead of replace, use compose strategies.

## Composition strategies

| Strategy | Effect | template | command | script |
|----------|--------|:--------:|:-------:|:------:|
| `replace` (default) | Fully replaces the lower-priority artifact | ✓ | ✓ | ✓ |
| `prepend` | Places content **before** the resolved lower-priority artifact, blank-line separated | ✓ | ✓ | — |
| `append` | Places content **after** the resolved lower-priority artifact, blank-line separated | ✓ | ✓ | — |
| `wrap` | Content contains `{CORE_TEMPLATE}` (templates/commands) or `$CORE_SCRIPT` (scripts), replaced with the lower-priority content | ✓ | ✓ | ✓ |

Scripts support only `replace` and `wrap`. Composition is **recursive**: the resolver walks the full priority stack bottom-up and applies each layer's strategy in turn (`PresetResolver.resolve_content()` in Python; template-only equivalents in Bash/PowerShell, with command/script composition delegated to Python).

### `wrap` placeholder

A `wrap` file embeds the lower-priority content at a chosen point:

```markdown
<!-- security preamble -->
## Threat model note
All features must document a threat model.

{CORE_TEMPLATE}

<!-- security appendix -->
## Security sign-off checklist
- [ ] Reviewed by security team
```

For scripts, use `$CORE_SCRIPT` instead of `{CORE_TEMPLATE}`.

## Worked example — security prepend + compliance append

Two presets both compose with `spec-template`. Because composition chains bottom-up, the result is: **security header → core content → compliance footer.**

`security-preset/preset.yml`:

```yaml
schema_version: "1.0"
preset:
  id: "security"
  name: "Security Header"
  version: "1.0.0"
  description: "Prepends a threat-model section to every spec"
  author: "sec-team"
  license: "MIT"
requires:
  speckit_version: ">=0.6.0"
provides:
  templates:
    - type: "template"
      name: "spec-template"
      file: "templates/spec-security-header.md"
      strategy: "prepend"
tags: ["security", "compliance"]
```

`compliance-preset/preset.yml`:

```yaml
schema_version: "1.0"
preset:
  id: "compliance"
  name: "Compliance Footer"
  version: "1.0.0"
  description: "Appends a regulatory sign-off section to every spec"
  author: "grc-team"
  license: "MIT"
requires:
  speckit_version: ">=0.6.0"
provides:
  templates:
    - type: "template"
      name: "spec-template"
      file: "templates/spec-compliance-footer.md"
      strategy: "append"
tags: ["compliance", "governance"]
```

Install both — priority does not matter for a `prepend` + `append` pair since they add to different ends:

```bash
specify preset add security   --priority 10
specify preset add compliance --priority 20
specify preset resolve spec-template   # shows the composed result
```

Resolved `spec-template` becomes:

```
<security prepend content>

<core spec-template content>

<compliance append content>
```

## Command overrides — the lean preset

`main:presets/lean/preset.yml` replaces the five core workflow commands with leaner variants. Every entry is `type: "command"` with `replaces:` set to the core command name and `strategy` left at the default `replace`:

```yaml
provides:
  templates:
    - type: "command"
      name: "speckit.specify"
      file: "commands/speckit.specify.md"
      description: "Lean specify - create spec.md from a feature description"
      replaces: "speckit.specify"
    - type: "command"
      name: "speckit.plan"
      file: "commands/speckit.plan.md"
      replaces: "speckit.plan"
    # …tasks, implement, constitution similarly
```

Command overrides register **at install time** into every detected agent directory (`.claude/commands/`, `.gemini/commands/`, …) in that agent's format (Markdown `$ARGUMENTS`, TOML `{{args}}`, or Copilot `.agent.md` + `.prompt.md`). Extension commands (`speckit.<ext>.<cmd>`, 3+ segments) are skipped unless the extension is installed; core 2-segment commands always register. `specify preset remove` deletes the registered files.

## Creating a preset

1. Copy `scaffold/` (upstream) or `assets/preset-template.yml` (this skill) to a new directory.
2. Edit `preset.yml` metadata.
3. Add/replace files in `templates/` and `commands/`.
4. Test locally: `specify preset add --dev .`
5. Verify resolution: `specify preset resolve spec-template`

## Catalog & environment

```bash
specify preset search <term>
specify preset add <name> --priority N
specify preset list
specify preset info <name>
specify preset catalog list
specify preset catalog add https://example.com/catalog.json --name my-org --install-allowed
```

| Variable | Effect |
|----------|--------|
| `SPECKIT_PRESET_CATALOG_URL` | Replace the whole catalog stack with one URL. |
| `GH_TOKEN` / `GITHUB_TOKEN` | Auth for private GitHub-hosted catalogs/ZIPs (attached only to GitHub domains). |

| Config file | Scope |
|-------------|-------|
| `.specify/preset-catalogs.yml` | Project catalog stack. |
| `~/.specify/preset-catalogs.yml` | User catalog stack. |
