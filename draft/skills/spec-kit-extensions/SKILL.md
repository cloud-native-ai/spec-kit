---
name: spec-kit-extensions
description: |
  Concept-import skill for the upstream spec-kit ecosystem: Extensions (add namespaced commands, config, and phase hooks), Presets (stackable template/command overrides with compose strategies), Bundles (role-based aggregates of extensions + presets + workflows + steps), and Workflows (resumable YAML orchestration pipelines with gates). Explains the runtime template-resolution priority stack (override > preset > extension > core), the compose strategies (replace/prepend/append/wrap), and the catalog discovery layer. Use this when the user mentions ["extension", "preset", "bundle", "workflow orchestration", "template override", "compose templates", "compose strategy", "resolution stack", "extension.yml", "preset.yml", "workflow.yml", "bundle.yml", "phase hook", "before_/after_ hook", "catalog", "speckit namespace command", "gate step", "fan-out", "resumable pipeline", "扩展", "预设", "捆绑包", "工作流编排", "模板覆盖", "组合模板", "组合策略", "解析栈", "阶段钩子", "目录/编目", "门禁步骤", "可恢复流水线", "扇出扇入"]
skill_id: "<SKILL:draft/skills/spec-kit-extensions/SKILL.md>"
---

# spec-kit-extensions

> **Status: draft** — adapted from upstream spec-kit (main branch) extensions/presets/bundles + workflows. Incubating in draft/; a concept import, not wired into the master /speckit.* flow.

## Overview

上游 spec-kit 用**四种可组合工件**在不 fork、不改核心文件的前提下扩展 SDD 工作流。本技能把这套生态**概念化移植**到定制 fork，供作者理解与编写这些工件，但**尚未接入** master 分支的 `/speckit.*` 运行时。

The upstream ecosystem lets teams grow the Spec-Driven Development workflow without forking core files. Four artifact kinds layer on top of the shipped `.specify/templates/` and `/speckit.*` commands:

| 工件 Artifact | 文件 File | 作用 What it adds |
|---------------|-----------|-------------------|
| **Extension** | `extension.yml` | New namespaced commands (`speckit.<ext-id>.<cmd>`), config files, and lifecycle **hooks** on SDD phases |
| **Preset** | `preset.yml` | Stackable, priority-ordered **template & command overrides** with compose strategies |
| **Bundle** | `bundle.yml` | Role-based **aggregate** referencing extensions + presets + workflows + steps |
| **Workflow** | `workflow.yml` | Resumable **YAML orchestration** of steps (commands, gates, loops, branches) |

All four are discovered through **catalogs** (`catalog.json` official + `catalog.community.json` community) and installed under `.specify/` via `specify extension|preset|workflow add …`.

---

## The three layering mechanisms

Extensions, presets, and bundles are three ways to layer capability onto core. (Workflows orchestrate; see the next section.)

| Mechanism | Adds what | Layered when | Removable | Install target |
|-----------|-----------|--------------|-----------|----------------|
| **Extension** | Commands + config + hooks | Commands at install; hooks fire at runtime on SDD phases | Yes (`extension remove`) | `.specify/extensions/<ext-id>/` |
| **Preset** | Template overrides (runtime) + command overrides (install-time) | Templates resolved at every lookup; commands registered into agent dirs at install | Yes (`preset remove`) | `.specify/presets/<preset-id>/` |
| **Bundle** | Nothing itself — it **references** extensions/presets/workflows/steps | Resolves and installs its members | Yes | Aggregate manifest |

Key distinction: **extensions add** new surface (commands/hooks); **presets override** existing surface (templates/commands); **bundles compose** existing artifacts into a role-ready setup.

### Extension (extension.yml)

- `extension:` metadata (`id`, `name`, `version`, `description`, `author`, `repository`, `license`, optional `category`, `effect`, `homepage`).
- `requires:` — `speckit_version` range and optional `tools:` list (MCP servers / binaries, each `required: true|false`).
- `provides.commands` — each `{name, file, description, aliases?}`. Names MUST follow `speckit.<ext-id>.<cmd>`.
- `provides.config` — config file templates `{name, template, description, required}`.
- `hooks.before_<phase>` / `hooks.after_<phase>` — run a command around an SDD phase; `optional`, `prompt`, `priority`, and list form for multiple commands per event.
- `defaults:` / `config.defaults:` — default settings merged with user config.

See `references/extension-format.md` for the full field reference, the hook mechanism, and the git extension as a worked example.

### Preset (preset.yml)

- `preset:` metadata + `requires.speckit_version`.
- `provides.templates` — entries with `type` (`template` | `command` | `script`), `name` (which artifact in the stack to compose with), `file` (actual content path), `description`, `replaces` (for command overrides), and `strategy` (compose strategy).
- Installed with a `--priority` (lower number = higher precedence). Multiple presets **stack**.

See `references/preset-format.md` for the manifest reference and a worked security-prepend + compliance-append example.

### Bundle (bundle.yml)

- `bundle:` metadata including a `role` (e.g. `developer`).
- `requires:` — `speckit_version`, `tools`, `mcp`.
- `provides:` — `extensions[]` (`{id, version}`), `presets[]` (`{id, version, priority, strategy}`), `steps[]` (`{id}`), `workflows[]` (`{id, version}`).
- A bundle installs nothing new by itself; it resolves and installs its referenced members. See `assets/bundle-template.yml`.

---

## Template resolution priority

When Spec Kit needs a template (e.g. `spec-template`), a resolver walks a **priority stack** and returns the first match. Resolution happens **at runtime** on every lookup, not by pre-merging files.

| Priority | Source | Path | Use case |
|----------|--------|------|----------|
| 1 (highest) | **Override** | `.specify/templates/overrides/` | One-off project-local tweaks |
| 2 | **Preset** | `.specify/presets/<id>/templates/` | Shareable, stackable customizations (lowest `priority` number wins) |
| 3 | **Extension** | `.specify/extensions/<id>/templates/` | Extension-provided templates |
| 4 (lowest) | **Core** | `.specify/templates/` | Shipped defaults |

If nothing overrides, core templates are used — identical to pre-ecosystem behavior. Resolution is implemented consistently in Python (`PresetResolver`), Bash (`resolve_template()`), and PowerShell (`Resolve-Template`).

### Compose strategies

By default a preset **replaces** the lower-priority content. A `strategy` per entry instead **composes** with it. The `name` field identifies which template in the stack to compose with; `file` points at the actual content.

| Strategy | Effect | template | command | script |
|----------|--------|:--------:|:-------:|:------:|
| `replace` (default) | Fully replaces lower-priority content | ✓ | ✓ | ✓ |
| `prepend` | Content **before** lower-priority (blank-line separated) | ✓ | ✓ | — |
| `append` | Content **after** lower-priority (blank-line separated) | ✓ | ✓ | — |
| `wrap` | Content holds `{CORE_TEMPLATE}` (templates/commands) or `$CORE_SCRIPT` (scripts), replaced with lower-priority content | ✓ | ✓ | ✓ |

Composition is **recursive** — multiple composing presets chain bottom-up. A security preset (`prepend`) + a compliance preset (`append`) yields: security header + core content + compliance footer.

### Command override timing

Templates resolve at runtime, but preset **command** overrides (`type: "command"`) are registered **at install time** into every detected agent directory (`.claude/commands/`, `.gemini/commands/`, …) in the right format (Markdown / TOML / Copilot companion files). Commands with 3+ dot segments (`speckit.<ext>.<cmd>`) are skipped unless the extension is installed; core 2-segment commands always register. Removal cleans up the registered files.

### Catalog discovery layer

Artifacts are found through catalogs:

- `catalog.json` — the **official / your-org** catalog (empty upstream by design; you populate a fork or point `SPECKIT_CATALOG_URL` / `SPECKIT_PRESET_CATALOG_URL` / `SPECKIT_WORKFLOW_CATALOG_URL` at your own).
- `catalog.community.json` — **community discovery** catalog; entries are format-verified only, not audited. Review source before installing.

Each entry carries `priority` (merge ordering) and `install_allowed`. Catalogs are fetched with a 1-hour cache. See `references/extension-format.md` for the catalog entry schema.

---

## Workflow orchestration

Workflows are multi-step, **resumable** automation pipelines in YAML. The engine executes steps in order, dispatches commands to AI integrations, evaluates control flow, and **pauses at human review gates**. State persists after each step, so a run can resume after interruption.

```yaml
steps:
  - id: specify
    command: speckit.specify
    input:
      args: "{{ inputs.spec }}"
  - id: review
    type: gate
    message: "Review the spec before planning."
    options: [approve, reject]
    on_reject: abort
  - id: plan
    command: speckit.plan
```

### Step types (11 built-in)

| Type | Purpose |
|------|---------|
| `command` (default) | Invoke an installed `speckit.*` command via integration CLI |
| `prompt` | Send an arbitrary inline prompt to an integration |
| `shell` | Run a shell command, capture output |
| `init` | Bootstrap a project (like `specify init`) |
| `gate` | Pause for human review/approval |
| `if` | Conditional then/else branching |
| `switch` | Multi-branch dispatch on an expression value |
| `while` | Loop while a condition is truthy |
| `do-while` | Loop, body always runs at least once |
| `fan-out` | Dispatch a step template per item in a collection |
| `fan-in` | Aggregate results from a fan-out |

### Gates, expressions, state

- **Gates** pause the run; `on_reject` is `abort` (default, halts), `skip` (author branches downstream on `{{ steps.<id>.output.choice }}`), or `retry` (re-runs the gate on resume).
- **Expressions** use `{{ }}` syntax: `inputs.*`, `steps.<id>.output.*`, `context.run_id`, comparisons, boolean logic, and filters (`default`, `join`, `contains`, `map`, `from_json`).
- **State** persists to `.specify/workflows/runs/<run_id>/`; lifecycle is `created → running → completed | paused | failed | aborted`. Resume with `specify workflow resume <run_id>`.
- **Error handling**: a failed step halts the run unless `continue_on_error: true` (literal boolean); the exit code stays on `steps.<id>.output.exit_code` for downstream branching.

See `references/workflow-format.md` for the full step reference, input types, and resume semantics.

---

## Authoring guide

Pick the artifact that matches intent, then copy the matching starter from `assets/` and edit.

### Author an extension — add new commands/hooks

1. Copy `assets/extension-template.yml` → `extension.yml`; set `id`, metadata, `requires`.
2. Add each command under `provides.commands` as `speckit.<ext-id>.<cmd>` with a `file:` under `commands/`.
3. Add config templates under `provides.config` and defaults under `defaults:`.
4. Wire lifecycle hooks under `hooks.before_<phase>` / `after_<phase>` (mark `optional: true` + `prompt:` to ask first).
5. Reference: `references/extension-format.md`.

### Author a preset — override templates/commands

1. Copy `assets/preset-template.yml` → `preset.yml`; set `preset.id` + `requires`.
2. For each override add a `provides.templates` entry: pick `type`, set `name` (the artifact in the stack), `file` (your content), and `strategy` (`replace`/`prepend`/`append`/`wrap`).
3. For command overrides set `replaces:` to the command name; put content in `commands/`.
4. Install with `--priority N`; verify with `specify preset resolve <name>`.
5. Reference: `references/preset-format.md`.

### Author a workflow — orchestrate a pipeline

1. Copy `assets/workflow-template.yml` → `workflow.yml`; declare `inputs:` with types/defaults/enums.
2. Compose `steps:` from the 11 step types; add `gate` steps at review points.
3. Use `{{ }}` expressions to thread `inputs.*` and `steps.<id>.output.*`.
4. Test: `specify workflow run ./workflow.yml --input key=value`; inspect with `specify workflow info`.
5. Reference: `references/workflow-format.md`.

### Author a bundle — package a role

1. Copy `assets/bundle-template.yml` → `bundle.yml`; set `bundle.id` + `role`.
2. List members under `provides.extensions|presets|workflows|steps` (presets carry `priority` + `strategy`).
3. Keep member `version` pins aligned with catalog entries.

---

## Resources

### References (`./references/`)
- `extension-format.md` — extension manifest field reference, hook mechanism, `speckit.<ext-id>.<cmd>` naming, catalog entry schema, git extension example.
- `preset-format.md` — preset manifest reference + compose strategies with a security-prepend / compliance-append worked example.
- `workflow-format.md` — workflow YAML: inputs, the 11 step types, `{{ }}` expressions, gates & `on_reject`, state persistence/resume.

### Assets (`./assets/`)
- `extension-template.yml` — starter extension manifest with placeholder commands, config, and hooks.
- `preset-template.yml` — starter preset manifest showing all compose strategies.
- `workflow-template.yml` — starter resumable workflow with inputs, gates, and control flow.
- `bundle-template.yml` — starter bundle aggregating extensions + presets + workflows + steps.

### Upstream provenance
Adapted from spec-kit `main` branch: `extensions/README.md`, `presets/README.md`, `presets/ARCHITECTURE.md`, `workflows/README.md`, `workflows/ARCHITECTURE.md`, and the `extensions/git`, `presets/lean`, `workflows/speckit`, `examples/bundles/developer` examples.
