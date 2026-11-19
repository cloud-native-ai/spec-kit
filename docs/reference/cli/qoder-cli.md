# Qoder CLI

- **Agent key:** `qoder`
- **Tier:** 1
- **Agent folder:** `.qoder/` (commands in `.qoder/commands`, `.md` files)
- **Official docs:** https://docs.qoder.com/en/cli/quick-start
- **Memory sources:** https://docs.qoder.com/cli/memory
- **Product page:** https://qoder.com/
- **Captured:** 2026-07-11 (memory sources corrected 2026-08-05 per docs.qoder.com/cli/memory)

> **Link + summary page.** The product overview below is an original summary
> written for this project; no Qoder documentation text is reproduced here.
> Install routes, sign-in options and settings drift — read the official sources
> above before acting on a detail. The two dated sections at the bottom are this
> project's own verified records, not vendor documentation.

> **Qoder CLI ≠ Qoder IDE.** They are two distinct tools that share the `.qoder/` folder. Spec Kit's `qoder` agent key targets the **CLI** (`qodercli` binary). The IDE's instruction format (`.qoder/project_rules.md`) is NOT read by the CLI — see "Project rules & memory sources" below.

## What it is (summary)

Qoder is an agentic coding platform; the **CLI** (`qodercli`) brings its agent to
the terminal for multi-file generation, question answering and edits, alongside
the Editor and Quest workspaces of the IDE experience. It supports autonomous
delegation for longer multi-step tasks, MCP servers, and a knowledge engine that
accumulates project knowledge. Installation, sign-in (browser or personal access
token, with an environment-variable route for automation) and update behaviour
are documented in the official quick start.

## Read the official documentation for

- Installation per operating system and architecture, and version verification.
- Sign-in, personal access tokens and automation credentials.
- Auto-update and the settings file that controls it.
- Quest delegation, MCP configuration and the knowledge engine.

## Project rules & memory sources (CLI)

Per the CLI memory docs (docs.qoder.com/cli/memory), `qodercli` loads project-level rules from:

| File | Scope |
|------|-------|
| `~/.qoder/AGENTS.md` | User level |
| `<project>/AGENTS.md` | Project level (searched upward from the working directory to the directory containing `.git`) |
| `<project>/AGENTS.local.md` | Project-local, private |
| `<project>/.qoder/rules/**/*.md` | Rule files; frontmatter controls triggering (`alwaysApply`, glob, …) |

- When `AGENTS.md` and `.qoder/rules/` coexist, **both are injected** (additive context). The CLI docs define **no override priority** between them; the "rules win on conflict" statement exists only in the **IDE** docs.
- **`.qoder/project_rules.md` is not a CLI source.** It is the Qoder IDE's old format and does not appear in the CLI docs — there is no CLI-side priority relationship between it and `AGENTS.md`, because the CLI simply never reads it.

## Verified dispatch flags & settings (dated record, 2026-10-18)

Observed on `qodercli 1.1.73` (macOS arm64). This is a **dated record, not a runtime
guarantee**; the runtime owner for per-CLI capabilities is `CAPABILITY_MATRIX` in
`scripts/python/execution-config.py`.

- `qodercli --help` lists `-m, --model <model>`, `--reasoning-effort <level>`, and
  `--context-window <size>` — the three flags a resolved external dispatch may pass.
- The host settings file `~/.qoder/settings.json` carries the current model selection
  (`model.name`), the per-model context window
  (`model.preferences[<name>].contextWindow`), and the per-model reasoning effort
  (`model.preferences[<name>].reasoning.effort`, when set).
- Per-dispatch configuration resolution is owned by `scripts/python/execution-config.py`;
  the resolved configuration is recorded per dispatch by
  `scripts/python/exec-quant.py --action collect-dispatch`.

## Spec Kit integration

Spec Kit renders `/speckit.*` commands into `.qoder/commands/*.md`. The canonical
instructions file `.specify/instructions.md` is surfaced to the **CLI** via the root
`AGENTS.md` symlink. The `.qoder/project_rules.md` symlink points at the same canonical
file, but it exists only for **Qoder IDE** compatibility — it is redundant for the CLI.
Because both are aliases of `.specify/instructions.md`, no content divergence or
conflict is possible in a Spec Kit project.
