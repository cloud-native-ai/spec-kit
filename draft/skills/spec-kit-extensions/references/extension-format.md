# Extension format reference

Extensions add new functionality — namespaced commands, config files, and lifecycle hooks — without modifying core Spec Kit files. An extension is a directory containing an `extension.yml` manifest plus `commands/`, `scripts/`, and config templates. Installed under `.specify/extensions/<ext-id>/`.

> Adapted from upstream `main:extensions/README.md`, `main:extensions/git/extension.yml`, `main:extensions/template/extension.yml`, `main:extensions/template/config-template.yml`, `main:extensions/catalog.community.json`.

## Manifest structure

```yaml
schema_version: "1.0"

extension:
  id: git                       # lowercase, hyphen-separated; the namespace root
  name: "Git Branching Workflow"
  version: "1.0.0"              # semantic version X.Y.Z
  description: "…"             # under 200 chars
  author: spec-kit-core
  repository: https://github.com/github/spec-kit
  license: MIT
  homepage: "…"               # optional (can equal repository)
  category: "process"          # optional: docs | code | process | integration | visibility
  effect: "read-write"         # optional: read-only | read-write

requires:
  speckit_version: ">=0.2.0"   # >=X.Y.Z, or range >=X.Y.Z,<Y.0.0
  tools:                        # optional external deps (MCP servers / binaries)
    - name: git
      required: false
    - name: "example-mcp-server"
      version: ">=1.0.0"
      required: true

provides:
  commands: [...]              # see below
  config: [...]               # see below

hooks: {...}                   # see "Hook mechanism"

tags: ["git", "branching", "workflow"]   # 2–5, used for catalog discovery

defaults: {...}                # default settings merged with user config
```

### `extension.*` metadata fields

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | Lowercase, hyphen-separated. Becomes the command namespace root. |
| `name` | yes | Human-readable. |
| `version` | yes | Semantic versioning. |
| `description` | yes | Under 200 characters. |
| `author` | yes | Name or organization. |
| `repository` | yes | GitHub URL (create before publishing). |
| `license` | recommended | MIT recommended for open source. |
| `homepage` | no | Can equal `repository`. |
| `category` | no | `docs` \| `code` \| `process` \| `integration` \| `visibility`. |
| `effect` | no | `read-only` \| `read-write` — whether it modifies project files. |

### `requires`

- `speckit_version` — minimum or range constraint.
- `tools[]` — external dependencies. Each `{name, version?, required}`. `required: false` means the extension degrades gracefully if the tool is absent (the git extension marks `git` itself as `required: false`).

## Commands (`provides.commands`)

Each command declares a name, a prompt file, and a description:

```yaml
provides:
  commands:
    - name: speckit.git.feature
      file: commands/speckit.git.feature.md
      description: "Create a feature branch with sequential or timestamp numbering"
      aliases: ["speckit.git.feature-short"]   # optional, same namespaced format
```

| Field | Required | Notes |
|-------|----------|-------|
| `name` | yes | MUST follow `speckit.<ext-id>.<cmd>` (see naming convention). |
| `file` | yes | Path (relative to the extension root) to the command prompt Markdown. |
| `description` | yes | Shown in listings. |
| `aliases` | no | Alternate namespaced names. |

### The `speckit.<ext-id>.<cmd>` naming convention

Command names are dot-segmented and the segment count is load-bearing:

- **Core commands** have **2 segments** — `speckit.specify`, `speckit.plan`. Always registered.
- **Extension commands** have **3+ segments** — `speckit.<ext-id>.<cmd>`. The middle segment MUST equal the extension `id`. Example: an extension `id: git` provides `speckit.git.feature`, `speckit.git.commit`, `speckit.git.validate`, `speckit.git.remote`, `speckit.git.initialize`.

The 3+ segment rule is a safety mechanism: when a preset or bundle tries to register an extension command, the system extracts the extension id from the second segment and checks that `.specify/extensions/<ext-id>/` exists. If the extension is not installed, the command is skipped, preventing orphan files that reference a missing extension.

## Config (`provides.config`)

Extensions can ship config file templates that get materialized into the project:

```yaml
provides:
  config:
    - name: "git-config.yml"          # filename created in the project
      template: "config-template.yml"  # source template in the extension
      description: "Git branching configuration"
      required: false                  # true = must be present/configured
```

Config templates support environment-variable overrides with the pattern `SPECKIT_<EXT_ID>_<SECTION>_<KEY>` (uppercase, dots → underscores) and local overrides via `<name>.local.yml` (gitignored). Defaults declared in the manifest are merged with the user's config.

## Hook mechanism

Hooks run an extension command **around an SDD phase**. Keys are `before_<phase>` or `after_<phase>`, where `<phase>` is a core command name without the `speckit.` prefix (`constitution`, `specify`, `clarify`, `plan`, `tasks`, `implement`, `checklist`, `analyze`, `taskstoissues`).

```yaml
hooks:
  before_constitution:
    command: speckit.git.initialize
    optional: false                    # false = auto-run without prompting
    description: "Initialize Git repository before constitution setup"

  before_specify:
    command: speckit.git.feature
    optional: false
    description: "Create feature branch before specification"

  before_plan:
    command: speckit.git.commit
    optional: true                     # true = user is prompted first
    prompt: "Commit outstanding changes before planning?"
    description: "Auto-commit before implementation planning"
    condition: null                    # reserved for future conditional execution
```

### Hook entry fields

| Field | Notes |
|-------|-------|
| `command` | The extension command to run at this hook point. |
| `optional` | `false` = execute automatically. `true` = prompt the user first. |
| `prompt` | Question shown when `optional: true`. |
| `priority` | Integer ≥ 1 (default 10). Lower runs first when several commands share an event. |
| `description` | Human-readable. |
| `condition` | Reserved for future conditional execution. |

### Multiple commands on one event

Use a list; order with `priority` (lowest first):

```yaml
hooks:
  after_plan:
    - command: "speckit.my-extension.verify"
      priority: 5
    - command: "speckit.my-extension.report"
      priority: 10
```

## Worked example — the git extension

The `git` extension (`main:extensions/git/extension.yml`) is the canonical concrete example:

- **id** `git` → namespace `speckit.git.*`.
- **requires** `speckit_version: ">=0.2.0"` and `git` as a non-required tool.
- **provides.commands**: `speckit.git.feature`, `speckit.git.validate`, `speckit.git.remote`, `speckit.git.initialize`, `speckit.git.commit`.
- **provides.config**: `git-config.yml` from `config-template.yml`, not required.
- **hooks**: `before_constitution → speckit.git.initialize` (auto), `before_specify → speckit.git.feature` (auto), and a `before_*`/`after_*` pair on nearly every phase calling `speckit.git.commit` with `optional: true` + a tailored `prompt` (e.g. "Commit outstanding changes before planning?"). This turns the extension into an auto-commit layer that brackets the whole SDD cycle.
- **defaults**: `branch_numbering: sequential`, `init_commit_message: "[Spec Kit] Initial commit"`.

## Catalog entry schema

Extensions are discovered through `catalog.json` (official/your-org) and `catalog.community.json` (community). A catalog is keyed by extension id; each entry mirrors the manifest metadata plus catalog bookkeeping (`main:extensions/catalog.community.json`):

```json
{
  "schema_version": "1.0",
  "updated_at": "2026-07-01T00:00:00Z",
  "catalog_url": "https://raw.githubusercontent.com/…/catalog.community.json",
  "extensions": {
    "aide": {
      "name": "AI-Driven Engineering (AIDE)",
      "id": "aide",
      "description": "…",
      "author": "mnriem",
      "version": "1.0.0",
      "download_url": "https://github.com/…/aide.zip",
      "repository": "https://github.com/…",
      "homepage": "…",
      "documentation": "…",
      "changelog": "…",
      "license": "MIT",
      "category": "process",
      "effect": "read-write",
      "requires": { "speckit_version": ">=0.2.0" },
      "provides": { "commands": 7, "hooks": 0 },
      "tags": ["workflow", "planning", "experimental"],
      "verified": false,
      "downloads": 0,
      "stars": 0,
      "created_at": "2026-03-18T00:00:00Z",
      "updated_at": "2026-03-18T00:00:00Z"
    }
  }
}
```

Note that in a catalog entry `provides.commands` / `provides.hooks` are **counts** (integers), not full definitions — the manifest inside the downloaded ZIP holds the real definitions. `verified: false` on every community entry reflects that maintainers only check format, not code.

## Install / discovery commands

```bash
specify extension search                                   # browse the active catalog
specify extension add <name>                               # install by name from catalog
specify extension add <name> --from https://…/v1.0.0.zip   # install directly from a URL
specify extension list                                     # list installed extensions
export SPECKIT_CATALOG_URL="https://your-org/catalog.json" # point at your org catalog
```
